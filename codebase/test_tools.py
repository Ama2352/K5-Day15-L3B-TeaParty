import json
import unittest
from copy import deepcopy
from pathlib import Path

import tools
from tracing import begin, end


SAMPLE_PATH = Path(__file__).resolve().parents[1] / "data" / "mau_ban_nhap.json"


def field(value=None, *, status="provided", source_id="S1"):
    refs = [] if status == "missing" else [
        {"source_type": "user_narrative", "source_id": source_id}
    ]
    return {
        "value": value, "source_refs": refs, "status": status, "user_confirmed": False,
    }


def sample_draft():
    photo = {
        "n": 1,
        "file_id": "F1",
        "ten_tep": "anh-mau.png",
        "loai_tai_lieu": field("Ảnh chụp"),
        "mo_ta_noi_dung": field("Ảnh cổng trước", source_id="S2"),
        "nguoi_tao": {"kind": "unknown", "field": field("Một người", status="unclear")},
        "thoi_diem_tao": {
            **field(status="conflicting"),
            "source_refs": [
                {"source_type": "user_narrative", "source_id": "S1", "quote": "2026-11-23"},
                {"source_type": "ocr", "source_id": "S2", "quote": "2026-11-24"},
            ],
            "precision": "unknown",
            "conflict_note": "2026-11-23 [S1]; 2026-11-24 [S2]",
        },
        "dia_diem_hoan_canh": field("Lối vào"),
        "thiet_bi_ung_dung": field("Điện thoại"),
        "nguoi_co_mat": field("Một người đi đường"),
        "cach_luu_giu": field("Trong thư mục gốc"),
        "tinh_trang_chinh_sua": {"edits": ["none_reported"], "field": field("Giữ nguyên")},
        "lien_quan_su_viec": field("Ghi lại lối vào"),
        "nguoi_cung_cap": None,
    }
    recording = deepcopy(photo)
    recording.update(
        n=2,
        file_id="F2",
        ten_tep="am-thanh-mau.wav",
        loai_tai_lieu=field("Ghi âm"),
        mo_ta_noi_dung=field("Âm thanh trước cổng", source_id="S3"),
        nguoi_tao={"kind": "provided_by_other", "field": field("Người đi đường")},
        thoi_diem_tao={**field("2026-11-25", source_id="S3"), "precision": "exact"},
        tinh_trang_chinh_sua={"edits": ["unknown"], "field": field(status="missing")},
        nguoi_cung_cap={
            "quan_he_hoac_vai_tro": field("Người chứng kiến"),
            "thoi_diem_cung_cap": {**field(status="missing"), "precision": "unknown"},
            "cach_cung_cap": field("Chuyển tệp", source_id="S3"),
            "nguon_cua_nguoi_cung_cap": field("Thiết bị của người cung cấp", source_id="S3"),
        },
    )
    return {
        "draft_label": "Bản nháp do AI hỗ trợ soạn, cần kiểm tra trước khi ký",
        "noi_nhan": field(status="missing"),
        "tu_cach": field("Người cung cấp thông tin"),
        "tai_lieu": [photo, recording],
        "questions_for_user": [],
    }


class SchemaValidationTest(unittest.TestCase):
    def test_accepts_schema_with_multiple_documents_and_nested_fields(self):
        self.assertEqual(tools.kiem_tra_schema(sample_draft()), [])

    @unittest.skipUnless(SAMPLE_PATH.is_file(), "N1 chưa cung cấp data/mau_ban_nhap.json")
    def test_accepts_team_sample(self):
        draft = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(tools.kiem_tra_schema(draft), [])

    def test_reports_errors_at_the_affected_fields(self):
        draft = sample_draft()
        del draft["questions_for_user"]
        draft["noi_nhan"]["value"] = "Một cơ quan"
        draft["tai_lieu"][0]["nguoi_tao"]["field"]["status"] = "estimated"
        del draft["tai_lieu"][0]["thoi_diem_tao"]["conflict_note"]
        del draft["tai_lieu"][0]["thoi_diem_tao"]["source_refs"][1]["source_id"]
        del draft["tai_lieu"][1]["nguoi_cung_cap"]["thoi_diem_cung_cap"]["precision"]
        errors = tools.kiem_tra_schema(draft)
        self.assertIsInstance(errors, list)
        for path in (
            "questions_for_user",
            "noi_nhan.value",
            "tai_lieu[0].nguoi_tao.field.status",
            "tai_lieu[0].thoi_diem_tao.conflict_note",
            "tai_lieu[0].thoi_diem_tao.source_refs[1].source_id",
            "tai_lieu[1].nguoi_cung_cap.thoi_diem_cung_cap.precision",
        ):
            with self.subTest(path=path):
                self.assertTrue(any(path in error for error in errors), errors)

    def test_rejects_values_that_violate_schema_types_and_constraints(self):
        cases = (
            ("draft_label", lambda draft: draft.update(draft_label="Văn bản chính thức")),
            ("tai_lieu", lambda draft: draft.update(tai_lieu=[])),
            ("tai_lieu[0].n", lambda draft: draft["tai_lieu"][0].update(n=True)),
            ("tai_lieu[0].n", lambda draft: draft["tai_lieu"][0].update(n=0)),
            ("tu_cach.user_confirmed", lambda draft: draft["tu_cach"].update(user_confirmed=1)),
            ("tai_lieu[0].ho_ten", lambda draft: draft["tai_lieu"][0].update(ho_ten="Tên mẫu")),
            ("questions_for_user[0].skippable", lambda draft: draft["questions_for_user"].append(
                {"field_path": "noi_nhan", "question": "Bạn định gửi văn bản cho ai?", "skippable": False}
            )),
        )
        for path, corrupt in cases:
            with self.subTest(path=path):
                draft = sample_draft()
                corrupt(draft)
                errors = tools.kiem_tra_schema(draft)
                self.assertTrue(any(path in error for error in errors), errors)


class DraftToolsTest(unittest.TestCase):
    def test_uncited_value_remains_a_question(self):
        draft = sample_draft()
        draft["tu_cach"] = field("Chi tiết thiếu nguồn")
        draft["tu_cach"]["source_refs"] = []
        self.assertIn({"field_path": "tu_cach", "status": "unclear"},
                      tools.tim_truong_can_hoi(draft))
        self.assertNotIn("Chi tiết thiếu nguồn", tools.tao_ban_nhap(draft))

    def test_finds_every_gap_across_multiple_documents(self):
        gaps = tools.tim_truong_can_hoi(sample_draft())
        self.assertCountEqual(
            [(gap["field_path"], gap["status"]) for gap in gaps],
            [
                ("noi_nhan", "missing"),
                ("tai_lieu[0].nguoi_tao.field", "unclear"),
                ("tai_lieu[0].thoi_diem_tao", "conflicting"),
                ("tai_lieu[1].tinh_trang_chinh_sua.field", "missing"),
                ("tai_lieu[1].nguoi_cung_cap.thoi_diem_cung_cap", "missing"),
            ],
        )

    def test_asks_at_most_once_per_field_and_preserves_competing_sources(self):
        draft = sample_draft()
        gaps = tools.tim_truong_can_hoi(draft)
        questions = tools.cau_hoi_bo_sung(gaps + gaps)
        self.assertCountEqual(
            [question["field_path"] for question in questions],
            [gap["field_path"] for gap in gaps],
        )
        for question in questions:
            self.assertIs(question["skippable"], True)
            self.assertTrue(question["question"].strip())
        conflict = next(
            question["question"] for question in questions
            if question["field_path"] == "tai_lieu[0].thoi_diem_tao"
        )
        for detail in ("2026-11-23", "2026-11-24", "S1", "S2"):
            with self.subTest(detail=detail):
                self.assertIn(detail, conflict)
        draft["questions_for_user"] = questions
        self.assertEqual(tools.kiem_tra_schema(draft), [])

    def test_prioritizes_and_limits_followup_questions(self):
        gaps = [
            {"field_path": f"tai_lieu[{index}].cach_luu_giu", "status": "missing"}
            for index in range(8)
        ]
        gaps += [
            {"field_path": "noi_nhan", "status": "missing"},
            {"field_path": "tai_lieu[8].mo_ta_noi_dung", "status": "missing"},
            {"field_path": "tai_lieu[8].thoi_diem_tao", "status": "missing"},
            {"field_path": "tai_lieu[9].mo_ta_noi_dung", "status": "unclear", "value": 'Sau chữ "mặc": [không nghe rõ]'},
            {"field_path": "tai_lieu[0].thoi_diem_tao", "status": "conflicting", "conflict_note": "Hai ngày khác nhau"},
            {"field_path": "tai_lieu[1].thoi_diem_tao", "status": "conflicting", "conflict_note": "Hai ngày khác nhau"},
        ]

        questions = tools.cau_hoi_bo_sung(gaps)
        self.assertEqual(
            [question["field_path"] for question in questions],
            ["tai_lieu[0].thoi_diem_tao", "tai_lieu[9].mo_ta_noi_dung", "tai_lieu[8].mo_ta_noi_dung", "noi_nhan"]
            + [f"tai_lieu[{index}].cach_luu_giu" for index in range(4)],
        )
        self.assertIn("không nghe hoặc không đọc rõ", questions[1]["question"])
        self.assertIn("có thể cung cấp tài liệu", questions[2]["question"])

    def test_renders_the_label_missing_fields_citations_and_conflicting_values(self):
        draft = sample_draft()
        output = tools.tao_ban_nhap(draft)
        lines = output.splitlines()
        self.assertEqual(lines[0], draft["draft_label"])
        self.assertIn("chưa có — cần xác nhận", output)
        self.assertTrue(any("Ảnh cổng trước" in line and "[S2]" in line for line in lines))
        self.assertTrue(any("Chuyển tệp" in line and "[S3]" in line for line in lines))
        for detail in ("2026-11-23 [S1]", "2026-11-24 [S2]"):
            with self.subTest(detail=detail):
                self.assertIn(detail, output)

    def test_reports_each_draft_tool_without_model_calls(self):
        draft = sample_draft()
        begin("cp3-draft-tools")
        try:
            tools.kiem_tra_schema(draft)
            gaps = tools.tim_truong_can_hoi(draft)
            tools.cau_hoi_bo_sung(gaps)
            tools.tao_ban_nhap(draft)
        finally:
            summary, events = end()
        self.assertEqual(summary["model_calls"], 0)
        self.assertEqual(summary["tool_calls"], 4)
        self.assertEqual(summary["errors"], [])
        self.assertEqual(
            [event["name"] for event in events if event["kind"] == "tool"],
            ["kiem_tra_schema", "tim_truong_can_hoi", "cau_hoi_bo_sung", "tao_ban_nhap"],
        )
