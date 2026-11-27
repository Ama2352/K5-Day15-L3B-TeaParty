import json
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from web import app


class DemoWebTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.addCleanup(self.client.close)

    def test_healthcheck(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_demo_uses_the_fake_agent(self):
        response = self.client.post("/ask", json={"text": "Thử TeaParty"})
        self.assertEqual(response.status_code, 200)
        output = response.json()["output"]
        self.assertIn("BẢN NHÁP PHẢN ÁNH", output)
        self.assertIn("[S1] Lời kể", output)
        self.assertIn("Thử TeaParty", output)
        self.assertIn("Ngày xảy ra: chưa cung cấp", output)

    def test_conflicting_dates_are_reported_with_their_sources(self):
        sample = Path(__file__).resolve().parents[1] / "data" / "cp2_demo.json"
        payload = json.loads(sample.read_text(encoding="utf-8"))
        response = self.client.post("/ask", json={"text": json.dumps(payload, ensure_ascii=False)})
        self.assertEqual(response.status_code, 200)
        output = response.json()["output"]
        self.assertIn("Ngày xảy ra: cần xác nhận", output)
        self.assertIn("2026-11-23 [S1]", output)
        self.assertIn("2026-11-24 [S3]", output)
        self.assertIn("[S4] Bản chép lời mẫu", output)

    def test_invalid_structured_input_does_not_generate_a_report(self):
        response = self.client.post("/ask", json={"text": '{"statement":"Lời kể","sources":"ảnh"}'})
        self.assertIn("Đầu vào chưa hợp lệ", response.json()["output"])

    def test_blank_input_is_rejected(self):
        response = self.client.post("/ask", json={"text": "   "})
        self.assertEqual(response.status_code, 422)
