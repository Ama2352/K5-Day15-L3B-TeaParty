import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

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
        self.assertIn("chọn có liên hệ luật sư và có dùng bản nháp hay không", output)

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

    def test_home_serves_intake_interface(self):
        response = self.client.get("/", follow_redirects=False)
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
        self.assertIn('<script src="/assets/draft.js"></script>', response.text)

    def test_draft_bundle_is_served_as_javascript(self):
        response = self.client.get("/assets/draft.js", follow_redirects=False)
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/javascript", response.headers["content-type"])
        self.assertIn("TeaPartyDraft", response.text)

    def test_partial_case_survives_followup_and_review(self):
        first = self.client.post("/ask", json={"text": "Tôi giữ một ghi chú.", "structured": True})
        self.assertEqual(first.status_code, 200)
        state = first.json()
        self.assertTrue(state["questions"])
        question = next(q for q in state["questions"] if q["field_path"] == "noi_nhan")
        updated = self.client.post("/follow-up", json={
            "draft": state["draft"], "field_path": question["field_path"], "text": "Nơi tiếp nhận A",
        })
        self.assertEqual(updated.status_code, 200, updated.text)
        draft = updated.json()["draft"]
        self.assertEqual(draft["noi_nhan"]["value"], "Nơi tiếp nhận A")
        self.assertTrue(any(ref["source_type"] == "user_answer" for ref in draft["noi_nhan"]["source_refs"]))
        reviewed = self.client.post("/review", json={"draft": draft})
        self.assertEqual(reviewed.status_code, 200)
        self.assertIn("Nơi tiếp nhận A", reviewed.json()["output"])
        self.assertIn("chưa có", reviewed.json()["output"])

    def test_no_email_without_both_consents(self):
        from test_tools import sample_draft

        for contact, use_form in [(False, False), (False, True), (True, False)]:
            with self.subTest(contact=contact, use_form=use_form):
                response = self.client.post("/email-draft", json={
                    "draft": sample_draft(), "lawyer_id": "ls-demo", "allowed_paths": ["tu_cach"],
                    "contact": contact, "use_form": use_form,
                })
                self.assertFalse(response.json().get("email"))

    def test_email_uses_selected_recipient_and_approved_fields_only(self):
        from test_tools import sample_draft

        draft = sample_draft()
        document = draft["tai_lieu"][0]
        document["mo_ta_noi_dung"]["user_confirmed"] = True
        catalog = {"synthetic": True, "lawyers": [{
            "id": "demo-a", "name": "Luật sư mẫu A", "email": "demo-a@example.invalid",
            "specialties": ["lao động"],
        }]}
        with TemporaryDirectory() as folder:
            path = Path(folder) / "luat_su.json"
            path.write_text(json.dumps(catalog, ensure_ascii=False), encoding="utf-8")
            with patch("tools._LAWYER_CATALOG", path):
                results = self.client.post("/lawyers", json={"nhu_cau": "lao động"})
                self.assertEqual(results.json()["lawyers"][0]["id"], "demo-a")
                payload = {"draft": draft, "lawyer_id": "demo-a", "contact": True, "use_form": True,
                           "allowed_paths": ["tai_lieu[0].mo_ta_noi_dung"]}
                response = self.client.post("/email-draft", json=payload)
                self.assertEqual(response.status_code, 200, response.text)
                email = response.json()["email"]
                self.assertIn("Ảnh cổng trước", email)
                self.assertNotIn("Một người đi đường", email)
                self.assertNotIn("anh-mau.png", email)
                payload["lawyer_id"] = "outside-catalog"
                self.assertGreaterEqual(self.client.post("/email-draft", json=payload).status_code, 400)
