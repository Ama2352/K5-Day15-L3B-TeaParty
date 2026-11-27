"""Công cụ chuẩn hóa lời kể và các đoạn nguồn cho bản thử CP2."""

import json
from datetime import date

from tracing import tool


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
