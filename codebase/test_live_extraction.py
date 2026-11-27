import unittest
from copy import deepcopy
from unittest.mock import patch

from fastapi.testclient import TestClient

from web import app


class LiveExtractionTest(unittest.TestCase):
    payload = {"text": "Tôi đã giữ một ghi chú.", "structured": True}

    def setUp(self):
        self.client = TestClient(app)
        self.addCleanup(self.client.close)
        with patch("web.MODEL_PROVIDER", "fake"):
            self.draft = self.client.post("/ask", json=self.payload).json()["draft"]

    def test_extraction_requires_input_source_references(self):
        for refs in ([], [{"source_id": "S9", "source_type": "user_narrative"}],
                     [{"source_id": "S1", "source_type": "file_metadata"}]):
            with self.subTest(refs=refs):
                draft = deepcopy(self.draft)
                draft["tai_lieu"][0]["mo_ta_noi_dung"]["source_refs"] = refs
                with (
                    patch("web.MODEL_PROVIDER", "openai"),
                    patch("web.agent._trich_xuat_day_du", None, create=True),
                    patch("web.agent.trich_xuat", return_value=draft, create=True),
                ):
                    response = self.client.post("/ask", json=self.payload)
                self.assertEqual(response.status_code, 502, response.text)
                self.assertNotIn("draft", response.json())

    def test_full_extraction_preserves_refusal_without_another_model_call(self):
        result = {
            "draft": self.draft,
            "loi": None,
            "ngoai_pham_vi": [
                {"loai": "gui_ra_ngoai", "yeu_cau": "Generated text not for display"},
                {"loai": "other", "ly_do": "Unknown refusal kind"},
            ],
        }
        with (
            patch("web.MODEL_PROVIDER", "openai"),
            patch("web.agent._trich_xuat_day_du", return_value=result, create=True) as extract,
            patch("web.agent.trich_xuat", create=True) as basic_extract,
        ):
            response = self.client.post("/ask", json=self.payload)

        self.assertEqual(response.status_code, 200, response.text)
        data = response.json()
        extract.assert_called_once()
        basic_extract.assert_not_called()
        self.assertEqual(data["mode"], "live")
        self.assertEqual(data["draft"]["tai_lieu"][0]["mo_ta_noi_dung"]["value"], self.payload["text"])
        self.assertEqual(len(data["notices"]), 1)
        self.assertIn("gửi", data["notices"][0])
        self.assertNotIn("Generated text not for display", response.text)
