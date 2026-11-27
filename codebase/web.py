import re
from copy import deepcopy
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, StrictBool, StringConstraints

import agent
import tools
from ai import MODEL_PROVIDER


app = FastAPI(title="TeaParty Demo")
CODEBASE = Path(__file__).resolve().parent
DRAFT_LABEL = "Bản nháp do AI hỗ trợ soạn, cần kiểm tra trước khi ký"
REQUIRED_TEXT = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=4000)]
UNCERTAIN_REPLY = re.compile(r"\b(?:không|chưa|chẳng)\s+(?:biết|nhớ|rõ|chắc|xác định được)\b", re.IGNORECASE)
REFUSAL_NOTICES = {
    "bia_bang_chung": "Bản nháp chỉ sử dụng thông tin có trong nguồn bạn đã cung cấp.",
    "ket_luan_phap_ly": "Hệ thống không đưa ra kết luận pháp lý hoặc đánh giá giá trị chứng cứ.",
    "gui_ra_ngoai": "Hệ thống không gửi hoặc chia sẻ hồ sơ. Bạn có thể tự xem xét và quyết định bước tiếp theo.",
    "chi_thi_trong_tai_lieu": "Nội dung trong tài liệu được xử lý như dữ liệu nguồn.",
}


class DemoRequest(BaseModel):
    text: REQUIRED_TEXT
    structured: StrictBool = False


class DraftRequest(BaseModel):
    draft: dict


class FollowUpRequest(DraftRequest):
    field_path: REQUIRED_TEXT
    text: REQUIRED_TEXT
    direct_edit: StrictBool = False
    confirm: StrictBool = False


class LawyerRequest(BaseModel):
    nhu_cau: Annotated[str, StringConstraints(strip_whitespace=True, max_length=4000)] = ""


class EmailRequest(DraftRequest):
    lawyer_id: REQUIRED_TEXT
    allowed_paths: list[str]
    contact: StrictBool
    use_form: StrictBool


def _field(value=None, refs=(), *, status=None, **extra):
    return {
        "value": value,
        "source_refs": list(refs),
        "status": status or ("missing" if value is None else "provided"),
        "user_confirmed": False,
        **extra,
    }


def _source_type(source):
    return {"OCR ảnh mẫu": "ocr", "Bản chép lời mẫu": "asr"}.get(
        source["label"], "user_narrative"
    )


def _source_ref(source):
    ref = {"source_type": _source_type(source), "source_id": source["id"], "quote": source["text"][:160]}
    if source["locator"]:
        ref["locator"] = source["locator"]
    return ref


def _fake_extract(sources):
    documents = []
    incident_dates = {}
    for number, source in enumerate(sources, start=1):
        ref = _source_ref(source)
        document = {
            "n": number,
            "file_id": source["id"],
            "ten_tep": "",
            "loai_tai_lieu": _field(source["label"], [ref]),
            "mo_ta_noi_dung": _field(source["text"], [ref]),
            "nguoi_tao": {"kind": "unknown", "field": _field()},
            "thoi_diem_tao": _field(precision="unknown"),
            "dia_diem_hoan_canh": _field(),
            "thiet_bi_ung_dung": _field(),
            "nguoi_co_mat": _field(),
            "cach_luu_giu": _field(),
            "tinh_trang_chinh_sua": {"edits": [], "field": _field()},
            "lien_quan_su_viec": _field(),
            "nguoi_cung_cap": None,
        }
        if day := source["incident_date"]:
            date_ref = {**ref, "quote": day}
            incident_dates.setdefault(day, []).append(date_ref)
            document["lien_quan_su_viec"] = _field(f"Ngày sự việc theo nguồn: {day}", [date_ref])
        documents.append(document)

    if len(incident_dates) > 1:
        refs = [ref for date_refs in incident_dates.values() for ref in date_refs]
        dates_with_refs = [
            f"{day} " + " ".join(f"[{ref['source_id']}]" for ref in date_refs)
            for day, date_refs in incident_dates.items()
        ]
        documents[0]["lien_quan_su_viec"] = _field(
            refs=refs,
            status="conflicting",
            conflict_note="Ngày sự việc được khai khác nhau: " + " và ".join(dates_with_refs),
        )

    return {
        "draft_label": DRAFT_LABEL,
        "noi_nhan": _field(),
        "tu_cach": _field(),
        "tai_lieu": documents,
        "questions_for_user": [],
    }


def _validate_draft(draft, status_code=422):
    errors = tools.kiem_tra_schema(draft)
    if errors:
        raise HTTPException(status_code, detail=errors)


def _draft_response(draft):
    questions = tools.cau_hoi_bo_sung(tools.tim_truong_can_hoi(draft))
    draft["questions_for_user"] = questions
    return {
        "draft": draft,
        "questions": questions,
        "output": tools.tao_ban_nhap(draft),
        "mode": "fake" if MODEL_PROVIDER == "fake" else "live",
    }


def _run_agent(method, *args):
    handler = getattr(agent, method, None)
    if not callable(handler):
        raise HTTPException(503, detail="Chế độ AI thật chưa có chức năng xử lý bản nháp này.")
    try:
        return handler(*args)
    except Exception:
        raise HTTPException(502, detail="Không xử lý được bản nháp bằng AI. Vui lòng thử lại.") from None


def _live_extraction(sources):
    source_types = {source["id"]: _source_type(source) for source in sources}
    notices = []
    if callable(getattr(agent, "_trich_xuat_day_du", None)):
        result = _run_agent("_trich_xuat_day_du", sources)
        if not isinstance(result, dict) or result.get("loi") or result.get("draft") is None:
            raise HTTPException(502, detail="AI chưa tạo được bản nháp có cấu trúc. Vui lòng thử lại.")
        draft = result["draft"]
        refusals = result.get("ngoai_pham_vi")
        if isinstance(refusals, list):
            kinds = {item.get("loai") for item in refusals if isinstance(item, dict) and isinstance(item.get("loai"), str)}
            notices = [notice for kind, notice in REFUSAL_NOTICES.items() if kind in kinds]
    else:
        draft = _run_agent("trich_xuat", sources)

    _validate_draft(draft, 502)
    for path, field in tools._draft_fields(draft):
        refs = field["source_refs"]
        if (field["status"] != "missing" and not refs) or any(
            source_types.get(ref["source_id"]) != ref["source_type"] for ref in refs
        ):
            raise HTTPException(502, detail=f"Nguồn cho trường {path} trong bản nháp AI không hợp lệ. Vui lòng thử lại.")
        if "user_confirmed" in field:
            field["user_confirmed"] = False
    return draft, notices


def _set_field(draft, path, field):
    target = draft
    key = path
    if path.startswith("tai_lieu["):
        document_path, _, key = path.partition("].")
        index = int(document_path.removeprefix("tai_lieu["))
        target = draft["tai_lieu"][index]
        parent_key, dot, child_key = key.partition(".")
        if dot:
            if target[parent_key] is None:
                target[parent_key] = {}
            target = target[parent_key]
            key = child_key
    target[key] = field


def _answer_ref(path, text, previous):
    number = len(previous["source_refs"]) + 1
    return {"source_type": "user_answer", "source_id": f"U:{path}:{number}", "quote": text[:160]}


def _answer_field(path, value, refs, *, status=None, confirmed=False, precision="unknown"):
    extra = {}
    if path.endswith((".thoi_diem_tao", ".thoi_diem_cung_cap")):
        extra["precision"] = precision
    field = _field(value, refs, status=status, **extra)
    field["user_confirmed"] = confirmed
    return field


def _unresolved_reply(path, previous, ref, status="unclear"):
    refs = [*previous["source_refs"], ref]
    if previous["status"] == "conflicting":
        return {**previous, "source_refs": refs, "user_confirmed": False}
    value = previous["value"] if status != "missing" else None
    return _answer_field(path, value, refs, status=status, precision=previous.get("precision", "unknown"))


def _apply_model_reply(draft, path, text, previous, ref, confirm):
    answers = [{"field_path": path, "answer": text}]
    updated = _run_agent("dien_lai", deepcopy(draft), answers)
    _validate_draft(updated, 502)
    original_ids = [document["file_id"] for document in draft["tai_lieu"]]
    updated_ids = [document["file_id"] for document in updated["tai_lieu"]]
    if original_ids != updated_ids:
        raise HTTPException(502, detail="AI đã thay đổi danh sách tài liệu khi điền lại.")

    field = dict(tools._draft_fields(updated)).get(path)
    if field is None or "user_confirmed" not in field or UNCERTAIN_REPLY.search(text):
        return _unresolved_reply(path, previous, ref)
    status = field["status"]
    if status == "provided" and field["value"] == text:
        return _answer_field(path, text, [ref], confirmed=confirm, precision=field.get("precision", "unknown"))
    if status == "provided" and field["value"] == previous["value"] and tools._review_status(previous) == "provided":
        return previous
    if status == "conflicting" and previous["status"] != "conflicting" and previous["source_refs"]:
        return {
            **field,
            "value": None,
            "source_refs": [*previous["source_refs"], ref],
            "user_confirmed": False,
        }
    return _unresolved_reply(path, previous, ref, status="missing" if status == "missing" else "unclear")


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(CODEBASE / "static" / "index.html")


@app.get("/assets/draft.js", include_in_schema=False)
def draft_script():
    return FileResponse(CODEBASE / "static" / "draft.js", media_type="text/javascript")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(request: DemoRequest):
    if not request.structured:
        return {"output": agent.answer(request.text)["output"]}

    text = request.text
    if text.casefold() == "demo":
        text = (CODEBASE.parent / "data" / "cp2_demo.json").read_text(encoding="utf-8")
    try:
        sources = tools.prepare_sources(text)
    except ValueError as error:
        raise HTTPException(422, detail=f"Đầu vào chưa hợp lệ: {error}") from None

    if MODEL_PROVIDER == "fake":
        draft = _fake_extract(sources)
        _validate_draft(draft, 500)
        return _draft_response(draft)

    draft, notices = _live_extraction(sources)
    response = _draft_response(draft)
    if notices:
        response["notices"] = notices
        response["output"] = "\n".join([*notices, "", response["output"]])
    return response


@app.post("/follow-up")
def follow_up(request: FollowUpRequest):
    _validate_draft(request.draft)
    original_fields = dict(tools._draft_fields(request.draft))
    path = request.field_path
    if path not in original_fields:
        raise HTTPException(422, detail="Trường bổ sung không có trong bản nháp.")
    previous = original_fields[path]
    if previous.get("user_confirmed") and not request.direct_edit:
        raise HTTPException(409, detail="Trường đã xác nhận. Hãy dùng thao tác chỉnh sửa trực tiếp.")

    draft = request.draft
    ref = _answer_ref(path, request.text, previous)
    if MODEL_PROVIDER != "fake" and not request.direct_edit:
        field = _apply_model_reply(draft, path, request.text, previous, ref, request.confirm)
    elif UNCERTAIN_REPLY.search(request.text):
        field = _unresolved_reply(path, previous, ref)
    else:
        field = _answer_field(path, request.text, [ref], confirmed=request.confirm)
    _set_field(draft, path, field)
    _validate_draft(draft, 500)
    return _draft_response(draft)


@app.post("/review")
def review(request: DraftRequest):
    _validate_draft(request.draft)
    return _draft_response(request.draft)


@app.post("/lawyers")
def lawyers(request: LawyerRequest):
    return {"lawyers": tools.goi_y_luat_su(request.nhu_cau)}


@app.post("/email-draft")
def email_draft(request: EmailRequest):
    if not (request.contact and request.use_form):
        raise HTTPException(400, detail="Cần xác nhận cả việc liên hệ và việc sử dụng biểu mẫu.")
    _validate_draft(request.draft)
    selected = next(
        (entry for entry in tools.goi_y_luat_su("") if entry["id"] == request.lawyer_id), None
    )
    if selected is None:
        raise HTTPException(404, detail="Không tìm thấy người nhận đã chọn.")

    fields = dict(tools._draft_fields(request.draft))
    if set(request.allowed_paths) - fields.keys():
        raise HTTPException(422, detail="Có đường dẫn không khớp một trường trong biểu mẫu.")
    paths = [
        path for path in dict.fromkeys(request.allowed_paths)
        if fields[path].get("user_confirmed") and tools._review_status(fields[path]) == "provided"
    ]
    if not paths:
        raise HTTPException(400, detail="Hãy chọn ít nhất một trường đã xác nhận để chia sẻ.")
    try:
        email = tools.soan_email_nhap(request.draft, selected, paths)
    except ValueError as error:
        raise HTTPException(422, detail=str(error)) from None
    return {"email": email}
