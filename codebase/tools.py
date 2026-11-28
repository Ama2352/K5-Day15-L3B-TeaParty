"""Công cụ chuẩn hóa nguồn và xử lý bản nháp."""

import json
import math
import re
import unicodedata
from datetime import date
from pathlib import Path

from tracing import tool


_SCHEMA = json.loads(
    Path(__file__).with_name("van_ban_xuat_xu.schema.json").read_text(encoding="utf-8")
)


def _is_number(value):
    return type(value) is int or (type(value) is float and math.isfinite(value))


_TYPE_CHECKS = {
    "object": lambda value: isinstance(value, dict),
    "array": lambda value: isinstance(value, list),
    "string": lambda value: isinstance(value, str),
    "null": lambda value: value is None,
    "boolean": lambda value: type(value) is bool,
    "number": _is_number,
    "integer": lambda value: _is_number(value) and value == int(value),
}


def _errors(value, schema, path):
    if "$ref" in schema:
        definition_name = schema["$ref"].removeprefix("#/$defs/")
        yield from _errors(value, _SCHEMA["$defs"][definition_name], path)

    if "type" in schema:
        types = schema["type"]
        if isinstance(types, str):
            types = [types]
        if not any(_TYPE_CHECKS[name](value) for name in types):
            yield f"{path}: cần kiểu {' hoặc '.join(types)}."
            return

    if "const" in schema:
        expected = schema["const"]
        if type(value) is not type(expected) or value != expected:
            yield f"{path}: phải là {json.dumps(expected, ensure_ascii=False)}."
    if "enum" in schema and value not in schema["enum"]:
        yield f"{path}: chỉ nhận {', '.join(schema['enum'])}."
    if "minimum" in schema and value < schema["minimum"]:
        yield f"{path}: phải lớn hơn hoặc bằng {schema['minimum']}."
    if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
        yield f"{path}: không đúng định dạng {schema['pattern']}."

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                yield f"{_property_path(path, key)}: thiếu trường bắt buộc."
        for key, child in value.items():
            child_path = _property_path(path, key)
            if key in properties:
                yield from _errors(child, properties[key], child_path)
            elif schema.get("additionalProperties") is False:
                yield f"{child_path}: trường không có trong schema."

        if "conflict_note" in properties and value.get("status") == "conflicting":
            note = value.get("conflict_note")
            if isinstance(note, str) and not note.strip():
                yield f"{_property_path(path, 'conflict_note')}: cần nội dung mâu thuẫn."

    if isinstance(value, list):
        minimum = schema.get("minItems", 0)
        if len(value) < minimum:
            yield f"{path}: cần ít nhất {minimum} phần tử."
        if "items" in schema:
            for index, item in enumerate(value):
                yield from _errors(item, schema["items"], f"{path}[{index}]")

    for rule in schema.get("allOf", []):
        if not list(_errors(value, rule["if"], path)):
            yield from _errors(value, rule["then"], path)


def _property_path(parent, key):
    return str(key) if parent == "$" else f"{parent}.{key}"


@tool
def kiem_tra_schema(draft: dict) -> list[str]:
    """Kiểm tra schema. Input là dict bản nháp. Output là danh sách lỗi.

    Danh sách rỗng nghĩa là hợp lệ. Không sửa bản nháp hay gửi dữ liệu ra ngoài.
    """
    return list(_errors(draft, _SCHEMA, "$"))


SOURCE_KINDS = {
    "text": "Văn bản",
    "image": "OCR ảnh mẫu",
    "audio": "Bản chép lời mẫu",
}


def _source(source_id, label, text, incident_date=None, locator=None):
    if not isinstance(text, str) or not text.strip():
        raise ValueError(f"{source_id} cần nội dung văn bản.")
    if locator is not None and not isinstance(locator, str):
        raise ValueError(f"{source_id} cần vị trí trích đoạn dạng văn bản.")
    if incident_date is not None:
        try:
            if date.fromisoformat(incident_date).isoformat() != incident_date:
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError(f"{source_id} cần ngày theo dạng YYYY-MM-DD.") from None
    return {
        "id": source_id,
        "label": label,
        "text": text,
        "incident_date": incident_date,
        "locator": locator,
    }


@tool
def prepare_sources(text: str) -> list:
    """Chuẩn hóa nguồn. Input là lời kể hoặc JSON. Output là các đoạn có mã nguồn.

    Chỉ xử lý trong bộ nhớ, không có tác động ra ngoài.
    """
    if not text.lstrip().startswith(("{", "[")):
        return [_source("S1", "Lời kể", text)]

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        raise ValueError("JSON phải đúng cú pháp.") from None
    if not isinstance(payload, dict):
        raise ValueError("JSON cần là một đối tượng có trường statement.")
    attachments = payload.get("sources", [])
    if not isinstance(attachments, list):
        raise ValueError("sources phải là danh sách nguồn.")

    sources = [_source("S1", "Lời kể", payload.get("statement"), payload.get("incident_date"))]
    for index, attachment in enumerate(attachments, start=2):
        source_id = f"S{index}"
        if not isinstance(attachment, dict):
            raise ValueError(f"{source_id} phải là một đối tượng nguồn.")
        kind = attachment.get("kind")
        if not isinstance(kind, str) or kind not in SOURCE_KINDS:
            raise ValueError(f"{source_id} cần kind là text, image hoặc audio.")
        sources.append(
            _source(
                source_id,
                SOURCE_KINDS[kind],
                attachment.get("text"),
                attachment.get("incident_date"),
                attachment.get("locator"),
            )
        )
    return sources


_ROOT_FIELD_LABELS = {
    "noi_nhan": "Nơi nhận",
    "tu_cach": "Tư cách",
}

_DOCUMENT_FIELD_LABELS = {
    "loai_tai_lieu": "Loại tài liệu",
    "mo_ta_noi_dung": "Mô tả nội dung",
    "nguoi_tao.field": "Người tạo",
    "thoi_diem_tao": "Thời điểm tạo",
    "dia_diem_hoan_canh": "Địa điểm và hoàn cảnh",
    "thiet_bi_ung_dung": "Thiết bị và ứng dụng",
    "nguoi_co_mat": "Người có mặt",
    "cach_luu_giu": "Cách lưu giữ",
    "tinh_trang_chinh_sua.field": "Tình trạng chỉnh sửa",
    "lien_quan_su_viec": "Liên quan đến sự việc",
}

_PROVIDER_FIELD_LABELS = {
    "nguoi_cung_cap.quan_he_hoac_vai_tro": "Quan hệ hoặc vai trò của người cung cấp",
    "nguoi_cung_cap.thoi_diem_cung_cap": "Thời điểm cung cấp",
    "nguoi_cung_cap.cach_cung_cap": "Cách cung cấp",
    "nguoi_cung_cap.nguon_cua_nguoi_cung_cap": "Nguồn tài liệu của người cung cấp",
}

_FIELD_LABELS = _ROOT_FIELD_LABELS | _DOCUMENT_FIELD_LABELS | _PROVIDER_FIELD_LABELS
_MISSING_FIELD = {"status": "missing", "value": None, "source_refs": ()}
_MISSING_TEXT = "chưa có — cần xác nhận"


def _document_fields(document):
    for field_path in _DOCUMENT_FIELD_LABELS:
        field_key, _, nested_key = field_path.partition(".")
        field = document[field_key]
        yield field_path, field[nested_key] if nested_key else field

    provider = document["nguoi_cung_cap"]
    if provider is None and document["nguoi_tao"]["kind"] != "provided_by_other":
        return
    provider = provider or {}
    for field_path in _PROVIDER_FIELD_LABELS:
        field_key = field_path.split(".")[1]
        yield field_path, provider.get(field_key, _MISSING_FIELD)


def _draft_fields(draft):
    for field_path in _ROOT_FIELD_LABELS:
        yield field_path, draft[field_path]
    for index, document in enumerate(draft["tai_lieu"]):
        for field_path, field in _document_fields(document):
            yield f"tai_lieu[{index}].{field_path}", field


def _citations(source_refs):
    source_ids = dict.fromkeys(ref["source_id"] for ref in source_refs if ref["source_id"].strip())
    return " ".join(f"[{source_id}]" for source_id in source_ids)


def _review_status(field):
    status = field["status"]
    if status == "provided" and not (field["value"] or "").strip():
        return "unclear"
    if status != "missing" and not _citations(field["source_refs"]):
        return "unclear"
    return status


@tool
def tim_truong_can_hoi(draft: dict) -> list[dict]:
    """Tìm trường cần hỏi. Input là bản nháp đúng schema, output là danh sách trường cần làm rõ.

    Chỉ đọc bản nháp trong bộ nhớ, không có tác động ra ngoài.
    """
    gaps = []
    for field_path, field in _draft_fields(draft):
        status = _review_status(field)
        if status in {"missing", "unclear", "conflicting"}:
            gap = {"field_path": field_path, "status": status}
            if status == "conflicting":
                gap.update(source_refs=field["source_refs"], conflict_note=field["conflict_note"])
            if status == "unclear" and _citations(field["source_refs"]):
                gap["value"] = field["value"]
                gap["quote"] = next(
                    (ref["quote"] for ref in field["source_refs"] if ref.get("quote", "").strip()),
                    "",
                )
            gaps.append(gap)
    return gaps


MAX_CAU_HOI = 8
# Thứ tự hỏi trong nhóm "missing": trường quan trọng cho văn bản trước, trường kỹ thuật sau.
_MISSING_ORDER = ["noi_nhan", "thoi_diem_tao", "dia_diem_hoan_canh", "nguoi_co_mat", "nguoi_tao", "tu_cach",
                  "loai_tai_lieu", "mo_ta_noi_dung", "lien_quan_su_viec", "quan_he_hoac_vai_tro",
                  "thoi_diem_cung_cap", "cach_cung_cap", "nguon_cua_nguoi_cung_cap",
                  "thiet_bi_ung_dung", "cach_luu_giu", "tinh_trang_chinh_sua"]

_DAU_TRONG = r"(?:không|chưa)\s+(?:nghe|đọc|nhìn)\s+(?:rõ|được)|bị\s+(?:ồn|mờ|nhòe|nhoè|cắt)|mờ|ồn|nhòe|nhoè"
_DAU_KHONG_RO = re.compile(
    rf"[\[(]\s*(?:{_DAU_TRONG})[^\])]*[\])]"
    r"|\b(?:đoạn|chữ|dòng|phần)\b[^.!?\n]*?(?:(?<!không\s)\bbị\s+(?:ồn|mờ|nhòe|nhoè)|\bkhông\s+nghe\s+rõ|\bkhông\s+đọc\s+được)",
    re.IGNORECASE)


def _ngan(text, limit=90) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit - 1].rstrip() + "…"


# Câu hỏi cho trường "unclear" theo loại trường: hỏi đúng điều còn thiếu thay vì "có muốn làm rõ không".
_HOI_CHUA_RO = {
    "thoi_diem_tao": "Bạn có nhớ thời điểm cụ thể hơn không (ngày, giờ)?",
    "thoi_diem_cung_cap": "Bạn có nhớ thời điểm cụ thể hơn không (ngày, giờ)?",
    "dia_diem_hoan_canh": "Bạn có thể nói rõ hơn nơi chốn hoặc hoàn cảnh không?",
    "nguoi_co_mat": "Bạn có thể cho biết rõ hơn ai có mặt không?",
    "nguoi_tao": "Ai đã lập, chụp, chép hoặc ghi tài liệu này?",
    "thiet_bi_ung_dung": "Tài liệu được tạo bằng thiết bị hoặc ứng dụng nào?",
    "cach_luu_giu": "Tài liệu đang được lưu ở đâu, bằng cách nào?",
    "tinh_trang_chinh_sua": "Tài liệu đã bị cắt, chụp lại, đổi định dạng hay chỉnh sửa gì chưa?",
}
_CACH_GOI_MO_HO = re.compile(r"[\"“]([^\"”]{1,30})[\"”]")
# Ký hiệu định danh người: một chữ in hoa A–Z (không dấu; Ă, Đ… KHÔNG tính) kèm số tuỳ chọn, có thể có tới 2 từ
# chỉ vai trong danh sách đóng đứng trước — "A", "B2", "đồng nghiệp A", "anh quản lý C". Danh sách "A, B", "A và B" cũng là
# ký hiệu; "A hoặc B" (chưa rõ người nào) thì KHÔNG.
_TU_CHI_VAI = ["đồng nghiệp", "anh", "chị", "em", "ông", "bà", "cô", "chú", "bác", "bạn", "sếp", "quản lý",
               "trưởng phòng", "trưởng nhóm", "phó phòng", "giám đốc", "nhân viên", "khách hàng", "bảo vệ",
               "giáo viên", "học sinh", "sinh viên", "người quản lý"]
_VAI = "|".join(sorted((re.escape(t) for t in _TU_CHI_VAI), key=len, reverse=True))
_MOT_KY_HIEU = re.compile(rf"(?i:(?:{_VAI})\s+){{0,2}}[A-Z]\d*")
_TRUONG_NGUOI = ("nguoi_co_mat", "mo_ta_noi_dung", "nguoi_tao")


def _la_ky_hieu(text: str) -> bool:
    """Chuỗi chỉ gồm ký hiệu định danh người (hoặc danh sách nối bằng dấu phẩy / "và")."""
    text = unicodedata.normalize("NFC", " ".join(str(text).split()))
    items = [x for x in re.split(r"\s*,\s*|\s+và\s+", text)]
    return bool(items) and all(x and _MOT_KY_HIEU.fullmatch(x) for x in items)


def _cau_hoi_chua_ro(label: str, key: str, gap: dict) -> str:
    """Nêu cụ thể điều chưa rõ: cách gọi trong ngoặc kép (vd một đại từ) → hỏi đó là ai; còn lại hỏi theo trường."""
    value = gap.get("value") or ""
    ghi = f" bản nháp đang ghi \"{_ngan(value)}\"." if value else (
        f" nguồn ghi \"{_ngan(gap['quote'], 60)}\"." if gap.get("quote") else "")
    if key == "mo_ta_noi_dung" and _DAU_KHONG_RO.search(unicodedata.normalize("NFC", value)):
        return (f"{label}: nguồn có đoạn được đánh dấu là không nghe hoặc không đọc rõ. Bạn có nhớ nội dung "
                "đoạn đó không? Nếu không chắc, cứ để trống — bản nháp sẽ giữ nguyên dấu \"không rõ\".")
    goi = [g for g in _CACH_GOI_MO_HO.findall(value) if not _la_ky_hieu(g)]
    if goi and key in _TRUONG_NGUOI:
        return f"{label}:{ghi} \"{goi[0]}\" là ai? Nếu bạn muốn, hãy ghi rõ (có thể dùng ký hiệu như A, B)."
    if value and gap.get("quote"):
        ghi += f" Nguồn: \"{_ngan(gap['quote'], 60)}\"."
    mac_dinh = ("Ai là người được nhắc tới, hoặc chi tiết nào bạn chưa chắc, cần ghi rõ hơn?"
                if key == "mo_ta_noi_dung" else "Bạn có thể nói rõ hơn phần này không?")
    return f"{label} còn chưa rõ:{ghi} " + _HOI_CHUA_RO.get(key, mac_dinh)


@tool
def cau_hoi_bo_sung(gaps: list) -> list[dict]:
    """Soạn tối đa tám câu bổ sung có thể bỏ qua từ danh sách trường cần làm rõ.

    Ưu tiên mâu thuẫn, chỗ chưa rõ, rồi trường thiếu. Chỉ xử lý trong bộ nhớ.
    """
    documents_without_content = {
        gap["field_path"].partition("].")[0]
        for gap in gaps
        if gap["status"] == "missing" and gap["field_path"].endswith("].mo_ta_noi_dung")
    }
    conflicts, unclear, missing = [], [], []
    seen_paths, seen_notes = set(), set()
    for gap in gaps:
        field_path = gap["field_path"]
        if field_path in seen_paths:
            continue
        seen_paths.add(field_path)
        document_path, in_document, field_key = field_path.partition("].")
        field_key = field_key if in_document else field_path
        key = field_key.removesuffix(".field").rsplit(".", 1)[-1]
        label = _FIELD_LABELS[field_key]
        if in_document:
            document_number = int(document_path.removeprefix("tai_lieu[")) + 1
            label = f"{label} (tài liệu {document_number})"

        status = gap["status"]
        if status == "conflicting":
            note = gap.get("conflict_note", "")
            if note and note in seen_notes:
                continue
            seen_notes.add(note)
            sources = _citations(gap.get("source_refs", ()))
            detail = " · ".join(part for part in (sources, note) if part)
            question = (
                f"{label}: các nguồn đang ghi khác nhau ({detail or 'xem nguồn'}). "
                "Bạn có thể xác nhận thông tin đúng không?"
            )
            conflicts.append((field_path, question))
        elif document_path in documents_without_content:
            if key == "mo_ta_noi_dung":
                question = (
                    f"Tài liệu {document_number} mới được nhắc tới, chưa có nội dung. "
                    "Bạn có thể cung cấp tài liệu này (nội dung, thời điểm tạo, cách lưu giữ) không?"
                )
                missing.append((-1, field_path, question))
        elif status == "unclear":
            unclear.append((field_path, _cau_hoi_chua_ro(label, key, gap)))
        else:
            priority = _MISSING_ORDER.index(key) if key in _MISSING_ORDER else len(_MISSING_ORDER)
            question = f"{label} chưa có thông tin. Nếu bạn biết và muốn ghi vào, bạn có thể bổ sung."
            missing.append((priority, field_path, question))

    missing.sort(key=lambda item: item[0])
    ordered = conflicts + unclear + [(path, question) for _, path, question in missing]
    return [
        {"field_path": path, "question": question + " (Có thể bỏ qua.)", "skippable": True}
        for path, question in ordered[:MAX_CAU_HOI]
    ]


def _render_field(field_path, field):
    label = _FIELD_LABELS[field_path]
    status = _review_status(field)
    if status == "missing":
        return f"{label}: {_MISSING_TEXT}"

    citations = _citations(field["source_refs"])
    value = field["value"] if citations else None
    if status == "conflicting":
        details = "Thông tin mâu thuẫn — cần xác nhận"
        if field["conflict_note"]:
            details = f"{details} ({field['conflict_note']})"
        value = f"{value} — {details}" if value else details
    elif status == "unclear":
        value = f"{value} — cần làm rõ" if value else "Thông tin chưa rõ — cần xác nhận"

    return f"{label}: {value or _MISSING_TEXT} {citations}".rstrip()


@tool
def tao_ban_nhap(draft: dict) -> str:
    """Trình bày bản nháp. Input là bản nháp đúng schema, output là văn bản có dẫn nguồn.

    Chỉ tạo văn bản trong bộ nhớ, không có tác động ra ngoài.
    """
    lines = [draft["draft_label"], ""]
    lines.extend(_render_field(field_path, draft[field_path]) for field_path in _ROOT_FIELD_LABELS)
    for number, document in enumerate(draft["tai_lieu"], start=1):
        title = f"Tài liệu {number}"
        if document["ten_tep"]:
            title = f"{title} — {document['ten_tep']}"
        lines.extend(["", title])
        lines.extend(_render_field(field_path, field) for field_path, field in _document_fields(document))
    return "\n".join(lines)


_LAWYER_CATALOG = Path(__file__).resolve().parents[1] / "data" / "luat_su.json"


def _single_line(value):
    return isinstance(value, str) and bool(value.strip()) and value.splitlines() == [value]


def _valid_recipient(recipient):
    if not isinstance(recipient, dict) or not _single_line(recipient.get("name")):
        return False
    email = recipient.get("email")
    return isinstance(email, str) and re.fullmatch(
        r"[A-Za-z0-9.!#$%&'*+/=?^_{}|~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", email
    ) is not None


def _search_phrase(text):
    folded = unicodedata.normalize("NFD", text.casefold().replace("đ", "d"))
    unaccented = "".join(char for char in folded if not unicodedata.combining(char))
    return " ".join(re.findall(r"[^\W_]+", unaccented))


@tool
def goi_y_luat_su(nhu_cau: str) -> list[dict]:
    """Đọc danh mục luật sư giả lập. Input là nhu cầu, output là danh sách phù hợp.

    Nhu cầu rỗng trả toàn danh mục. Chỉ đọc file nội bộ, không liên hệ ra ngoài.
    File luat_su.json có synthetic=true và lawyers gồm id, name, email, specialties.
    """
    try:
        catalog = json.loads(_LAWYER_CATALOG.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    if not isinstance(catalog, dict) or catalog.get("synthetic") is not True:
        return []

    lawyers = catalog.get("lawyers")
    if not isinstance(lawyers, list):
        return []

    need = _search_phrase(nhu_cau)
    suggestions = []
    for lawyer in lawyers:
        if not _valid_recipient(lawyer) or not _single_line(lawyer.get("id")):
            continue
        specialties = lawyer.get("specialties")
        if not isinstance(specialties, list) or not all(_single_line(item) for item in specialties):
            continue
        phrases = [_search_phrase(item) for item in specialties]
        if need and not any(phrase and f" {phrase} " in f" {need} " for phrase in phrases):
            continue
        suggestions.append({key: lawyer[key] for key in ("id", "name", "email", "specialties")})
    return suggestions


_EMAIL_UNCERTAINTY = {
    "missing": "chưa có — cần xác nhận",
    "unclear": "thông tin chưa rõ — cần xác nhận",
    "conflicting": "thông tin mâu thuẫn — cần xác nhận",
}


def _email_field_value(field):
    status = field["status"]
    if status in _EMAIL_UNCERTAINTY:
        return _EMAIL_UNCERTAINTY[status]
    if _review_status(field) != "provided":
        return _EMAIL_UNCERTAINTY["unclear"]
    if field.get("user_confirmed") is not True:
        return "chưa được người dùng xác nhận"

    value = field["value"].strip()
    precision = field.get("precision")
    if precision == "user_estimate":
        return f"{value} (ước tính)"
    if precision == "unknown":
        return f"{value} (độ chính xác chưa rõ)"
    return value


@tool
def soan_email_nhap(draft: dict, nguoi_nhan: dict, truong_cho_phep: list[str]) -> str:
    """Soạn email nháp từ form đúng schema, người nhận và danh sách đường dẫn được phép.

    Output là văn bản để người dùng rà lại. Chỉ đưa giá trị đã xác nhận cho từng
    đường dẫn được chọn. Danh sách rỗng tạo lời đề nghị trao đổi chung. Không gửi email.
    """
    if not _valid_recipient(nguoi_nhan):
        raise ValueError("Người nhận cần tên và một địa chỉ email hợp lệ.")
    if not isinstance(truong_cho_phep, list) or not all(
        isinstance(path, str) for path in truong_cho_phep
    ):
        raise ValueError("Cần danh sách đường dẫn đến các trường được phép chia sẻ.")

    selected = set(truong_cho_phep)
    fields = dict(_draft_fields(draft)) if selected else {}
    if not selected <= fields.keys():
        raise ValueError("Có đường dẫn không khớp một trường trong biểu mẫu.")

    lines = [
        "Email nháp",
        f"Đến: {nguoi_nhan['email']}",
        "Tiêu đề: Đề nghị trao đổi với luật sư",
        "",
        f"Kính gửi {nguoi_nhan['name']},",
        "",
        "Tôi muốn đặt lịch trao đổi để được tư vấn về một sự việc.",
    ]
    if selected:
        lines.extend(["", "Thông tin tôi đồng ý chia sẻ:"])
    for path, field in fields.items():
        if path not in selected:
            continue
        document_path, in_document, field_key = path.partition("].")
        label = _FIELD_LABELS[field_key if in_document else path]
        if in_document:
            number = int(document_path.removeprefix("tai_lieu[")) + 1
            label = f"Tài liệu {number} · {label}"
        lines.append(f"- {label}: {_email_field_value(field)}")

    lines.extend(["", "Mong nhận được phản hồi về thời gian có thể trao đổi.", "", "Trân trọng,"])
    return "\n".join(lines)
