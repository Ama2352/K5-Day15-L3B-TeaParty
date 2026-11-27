import unittest
from copy import deepcopy
from unittest.mock import patch

from fastapi.testclient import TestClient

from web import app


class FollowUpTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.addCleanup(self.client.close)
        response = self.client.post("/ask", json={"text": "demo", "structured": True})
        self.draft = response.json()["draft"]

    def submit(self, path, text):
        response = self.client.post("/follow-up", json={
            "draft": self.draft, "field_path": path, "text": text,
        })
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()["draft"]

    def test_unknown_answer_does_not_resolve_prior_conflict(self):
        field_key = "lien_quan_su_viec"
        prior_field = self.draft["tai_lieu"][0][field_key]
        updated = self.submit(f"tai_lieu[0].{field_key}", "Tôi không nhớ ngày nào.")
        field = updated["tai_lieu"][0][field_key]
        self.assertEqual(field["status"], "conflicting")
        self.assertEqual(field["conflict_note"], prior_field["conflict_note"])
        self.assertEqual(field["source_refs"][:-1], prior_field["source_refs"])
        self.assertEqual(field["source_refs"][-1]["source_type"], "user_answer")

    def test_unknown_answer_is_not_a_provided_time(self):
        updated = self.submit("tai_lieu[0].thoi_diem_tao", "Không nhớ")
        field = updated["tai_lieu"][0]["thoi_diem_tao"]
        self.assertEqual(field["status"], "unclear")
        self.assertIsNone(field["value"])

    def test_model_cannot_attribute_an_unsupported_value_to_the_user(self):
        model_result = deepcopy(self.draft)
        model_result["noi_nhan"].update(value="Thông tin tự tạo", status="provided")
        model_result["tai_lieu"][0]["mo_ta_noi_dung"]["value"] = "Nội dung thay thế"
        self.draft["tai_lieu"][0]["mo_ta_noi_dung"]["user_confirmed"] = True
        with patch("web.MODEL_PROVIDER", "openai"), patch("web.agent.dien_lai", return_value=model_result, create=True):
            updated = self.submit("noi_nhan", "Tôi sẽ kiểm tra lại.")
        self.assertEqual(updated["noi_nhan"]["status"], "unclear")
        self.assertIsNone(updated["noi_nhan"]["value"])
        self.assertEqual(updated["tai_lieu"][0]["mo_ta_noi_dung"], self.draft["tai_lieu"][0]["mo_ta_noi_dung"])

    def test_model_missing_target_stays_missing(self):
        with patch("web.MODEL_PROVIDER", "openai"), patch("web.agent.dien_lai", return_value=self.draft, create=True):
            updated = self.submit("noi_nhan", "Nơi tiếp nhận A")
        self.assertEqual(updated["noi_nhan"]["status"], "missing")
        self.assertIsNone(updated["noi_nhan"]["value"])

    def test_live_route_passes_the_answer_to_n1(self):
        # Exercise the real N1 parser and merge, using its offline model path.
        with patch("web.MODEL_PROVIDER", "openai"), patch("ai.MODEL_PROVIDER", "fake"):
            updated = self.submit("noi_nhan", "Nơi tiếp nhận A")
        self.assertEqual(updated["noi_nhan"]["value"], "Nơi tiếp nhận A")
        self.assertEqual(updated["noi_nhan"]["source_refs"][0]["source_type"], "user_answer")

    def test_email_rejects_an_unknown_path_mixed_with_an_approved_one(self):
        path = "tai_lieu[0].mo_ta_noi_dung"
        self.draft["tai_lieu"][0]["mo_ta_noi_dung"]["user_confirmed"] = True
        recipient = {"id": "demo", "name": "Luật sư mẫu", "email": "demo@example.invalid"}
        with patch("tools.goi_y_luat_su", return_value=[recipient]):
            response = self.client.post("/email-draft", json={
                "draft": self.draft, "lawyer_id": "demo", "allowed_paths": [path, f"{path}.value"],
                "contact": True, "use_form": True,
            })
        self.assertEqual(response.status_code, 422, response.text)


if __name__ == "__main__":
    unittest.main()
