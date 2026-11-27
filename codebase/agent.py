"""Workflow soạn bản nháp phản ánh cho CLI, web và benchmark."""

import json

from ai import call_model
from tools import prepare_sources


SYSTEM = (
    "Soạn bản nháp phản ánh để nhân viên rà lại. "
    "Chỉ dùng lời kể và tài liệu được cung cấp, dẫn mã nguồn cho từng chi tiết. "
    "Ghi rõ thông tin thiếu hoặc mâu thuẫn và giữ nguyên trích đoạn nguồn. "
    "Phân biệt lời kể với dữ kiện đã xác minh. Không kết luận pháp lý hoặc gửi hồ sơ."
)


def answer(text: str) -> dict:
    """Nhận lời kể thuần hoặc JSON, trả bản nháp ở khóa output."""
    try:
        sources = prepare_sources(text)
    except ValueError as error:
        return {"output": f"Đầu vào chưa hợp lệ: {error}"}

    reply = call_model(SYSTEM, json.dumps(sources, ensure_ascii=False))
    return {"output": reply["text"]}
