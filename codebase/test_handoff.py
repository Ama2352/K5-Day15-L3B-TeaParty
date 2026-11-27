import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import tools
from test_tools import sample_draft


LAWYER = {
    "id": "ls-demo-1",
    "name": "Luật sư Giả Lập A",
    "email": "luatsu-a@example.invalid",
    "specialties": ["Lao động"],
}


class LawyerCatalogTest(unittest.TestCase):
    def test_empty_need_lists_catalog_and_need_matches_specialty(self):
        other_lawyer = {
            "id": "ls-demo-2",
            "name": "Luật sư Giả Lập B",
            "email": "luatsu-b@example.invalid",
            "specialties": ["Dân sự"],
        }
        with tempfile.TemporaryDirectory() as directory:
            catalog = Path(directory) / "luat_su.json"
            catalog.write_text(
                json.dumps({"synthetic": True, "lawyers": [LAWYER, other_lawyer]}),
                encoding="utf-8",
            )
            with patch.object(tools, "_LAWYER_CATALOG", catalog, create=True):
                self.assertEqual(tools.goi_y_luat_su(""), [LAWYER, other_lawyer])
                self.assertEqual(tools.goi_y_luat_su("Tranh chap LAO DONG"), [LAWYER])
                self.assertEqual(tools.goi_y_luat_su("hôn nhân"), [])

    def test_missing_invalid_or_unlabeled_catalog_has_no_suggestions(self):
        with tempfile.TemporaryDirectory() as directory:
            catalog = Path(directory) / "luat_su.json"
            with patch.object(tools, "_LAWYER_CATALOG", catalog, create=True):
                self.assertEqual(tools.goi_y_luat_su(""), [])
                catalog.write_text("{", encoding="utf-8")
                self.assertEqual(tools.goi_y_luat_su(""), [])
                catalog.write_text(json.dumps({"lawyers": [LAWYER]}), encoding="utf-8")
                self.assertEqual(tools.goi_y_luat_su(""), [])


class EmailDraftTest(unittest.TestCase):
    def test_shares_only_exact_allowlisted_confirmed_value(self):
        draft = sample_draft()
        photo = draft["tai_lieu"][0]
        photo["mo_ta_noi_dung"]["user_confirmed"] = True
        photo["mo_ta_noi_dung"]["source_refs"][0].update(
            source_id="PRIVATE-SOURCE", quote="PRIVATE-QUOTE", locator="PRIVATE-LOCATOR"
        )
        photo["loai_tai_lieu"]["user_confirmed"] = True
        draft["tai_lieu"][1]["mo_ta_noi_dung"]["user_confirmed"] = True

        email = tools.soan_email_nhap(draft, LAWYER, ["tai_lieu[0].mo_ta_noi_dung"])

        self.assertIn(LAWYER["email"], email)
        self.assertIn("Ảnh cổng trước", email)
        for private in (
            "Ảnh chụp",
            "Âm thanh trước cổng",
            "anh-mau.png",
            "PRIVATE-SOURCE",
            "PRIVATE-QUOTE",
            "PRIVATE-LOCATOR",
        ):
            self.assertNotIn(private, email)

    def test_preserves_uncertainty_without_exposing_candidate_values(self):
        draft = sample_draft()
        document = draft["tai_lieu"][0]
        document["thoi_diem_tao"].update(value="ngày nội bộ", user_confirmed=True)
        email = tools.soan_email_nhap(
            draft,
            LAWYER,
            ["noi_nhan", "tu_cach", "tai_lieu[0].nguoi_tao.field", "tai_lieu[0].thoi_diem_tao"],
        )

        for marker in ("chưa có", "chưa được người dùng xác nhận", "chưa rõ", "mâu thuẫn"):
            self.assertIn(marker, email)
        for private in ("Người cung cấp thông tin", "Một người", "ngày nội bộ", "2026-11-23"):
            self.assertNotIn(private, email)

    def test_rejects_parent_or_metadata_path(self):
        draft = sample_draft()
        for path in ("tai_lieu[0]", "tai_lieu[0].ten_tep", "tai_lieu[0].mo_ta_noi_dung.value"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                tools.soan_email_nhap(draft, LAWYER, [path])

    def test_empty_allowlist_creates_generic_contact_draft(self):
        email = tools.soan_email_nhap(sample_draft(), LAWYER, [])
        self.assertIn(LAWYER["email"], email)
        self.assertNotIn("Tài liệu 1", email)
        self.assertNotIn("Ảnh cổng trước", email)

    def test_rejects_recipient_with_extra_email_header(self):
        recipient = {**LAWYER, "email": LAWYER["email"] + "\nBcc: other@example.invalid"}
        with self.assertRaises(ValueError):
            tools.soan_email_nhap(sample_draft(), recipient, [])

    def test_qualifies_a_confirmed_date_estimate(self):
        draft = sample_draft()
        draft["tai_lieu"][1]["thoi_diem_tao"].update(
            user_confirmed=True, precision="user_estimate"
        )
        email = tools.soan_email_nhap(draft, LAWYER, ["tai_lieu[1].thoi_diem_tao"])
        self.assertIn("2026-11-25", email)
        self.assertIn("ước tính", email)


if __name__ == "__main__":
    unittest.main()
