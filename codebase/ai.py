"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str, json_mode: bool = False) -> dict với 4 khoá
        json_mode=True: bật response_format {"type": "json_object"} (chỉ với model thật);
        khi bật, system hoặc user phải chứa chữ "json" thì API mới nhận.
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    tạo bản nháp theo quy tắc đơn giản từ danh sách nguồn, model "fake", token 0.
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env (chép từ .env.example), rồi viết nhánh gọi API ở dưới theo docs/connect-model.md
(có ví dụ OpenAI, Claude, model chạy trên máy, và cách nối nhà cung cấp khác). Không dán API key vào file này.
"""
import json
import os
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()


def _fake_draft(sources: list) -> str:
    dates = {}
    for source in sources:
        if source["incident_date"]:
            dates.setdefault(source["incident_date"], []).append(f'[{source["id"]}]')

    references = "; ".join(f"{day} {' '.join(ids)}" for day, ids in dates.items())
    if len(dates) > 1:
        date_line = f"Ngày xảy ra: cần xác nhận (các nguồn mâu thuẫn: {references})."
    elif dates:
        date_line = f"Ngày xảy ra: theo nguồn {references}."
    else:
        date_line = "Ngày xảy ra: chưa cung cấp."

    statement = sources[0]
    lines = [
        "BẢN NHÁP PHẢN ÁNH — MÔ PHỎNG CP2",
        "",
        "1. Diễn biến theo lời kể",
        f'[S1] {json.dumps(statement["text"], ensure_ascii=False)}',
        "",
        "2. Nguồn đối chiếu",
    ]
    for source in sources:
        locator = f' · {source["locator"]}' if source["locator"] else ""
        excerpt = json.dumps(source["text"], ensure_ascii=False)
        lines.append(f'[{source["id"]}] {source["label"]}{locator}: {excerpt}')
    lines.extend([
        "",
        "3. Thông tin cần rà",
        date_line,
        "Rà lại nội dung và nguồn trước khi chọn có liên hệ luật sư và có dùng bản nháp hay không.",
    ])
    return "\n".join(lines)


SHOW_RAW = False   # đổi thành True để in nguyên phản hồi của API khi cần tìm tên trường

# DeepSeek dùng API theo định dạng OpenAI. Đổi nhà cung cấp tương thích OpenAI thì đặt MODEL_URL trong .env.
URL_OPENAI = (os.environ.get("MODEL_URL") or "https://api.deepseek.com/chat/completions").strip()


def post_json(url, headers, body, timeout=60):
    """Gửi POST JSON, trả về JSON phản hồi. Chỉ dùng thư viện chuẩn (urllib)."""
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST",
        headers=dict({"Content-Type": "application/json"}, **headers))
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


def call_openai(system, user, json_mode=False):
    """Gọi API dạng OpenAI chat completions (DeepSeek). json_mode=True bật response_format json_object —
    khi bật, system hoặc user phải có chữ "json" thì API mới nhận."""
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    body = {"model": MODEL_NAME, "messages": messages}
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    data = post_json(URL_OPENAI, {"Authorization": "Bearer " + API_KEY}, body, timeout=120)
    u = data["usage"]
    return {"text": data["choices"][0]["message"]["content"] or "",
            "tokens_in": u["prompt_tokens"], "tokens_out": u["completion_tokens"]}


@model_call
def call_model(system: str, user: str, json_mode: bool = False) -> dict:
    """json_mode=True: yêu cầu model trả một đối tượng JSON (chỉ có tác dụng với model thật)."""
    if MODEL_PROVIDER == "fake":
        draft = _fake_draft(json.loads(user))
        return {"text": draft, "model": "fake", "tokens_in": 0, "tokens_out": 0}

    if MODEL_PROVIDER == "openai":
        if not MODEL_NAME:
            raise RuntimeError("MODEL_PROVIDER=openai nhưng MODEL_NAME đang trống — điền MODEL_NAME trong .env "
                               "(ví dụ deepseek-chat).")
        r = call_openai(system, user, json_mode=json_mode)
    else:
        raise NotImplementedError(
            "chưa viết phần gọi model thật cho MODEL_PROVIDER=%s trong codebase/ai.py — xem docs/connect-model.md"
            % MODEL_PROVIDER)
    return {"text": r["text"], "model": MODEL_NAME,
            "tokens_in": int(r["tokens_in"]), "tokens_out": int(r["tokens_out"])}
