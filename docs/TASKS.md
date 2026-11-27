# Kế hoạch dựng · 3 người · CP3 → CP4

> Đọc trước khi vibe. Mỗi người **chỉ sửa file mình sở hữu** (bảng mục 2). Cần đổi file của người khác thì nhắn chủ file.
> Agent (Claude Code, Cursor…) đọc file này cùng `AGENTS.md` và `docs/PROJECT_CONTEXT.md` trước khi sửa code.
> Hạn: **CP3 10:00 Thứ Bảy 28/11** (AI thật + lượt eval 1) · **CP4 14:30 Thứ Bảy 28/11** (đủ luồng + lượt eval 2).

Điền tên trước khi bắt đầu:

- **Người 1 — Lõi AI:** Nguyễn Thảo Quyên
- **Người 2 — Backend + giao diện:** ____
- **Người 3 — Dữ liệu + đánh giá + hồ sơ:** ____

---

## 1. Hợp đồng chung (không ai tự ý đổi)

### 1.1 Định dạng dữ liệu = `codebase/van_ban_xuat_xu.schema.json`

- 11 trường của mỗi tài liệu (`tai_lieu[i]`): `loai_tai_lieu` · `mo_ta_noi_dung` · `nguoi_tao` · `thoi_diem_tao` · `dia_diem_hoan_canh` · `thiet_bi_ung_dung` · `nguoi_co_mat` · `cach_luu_giu` · `tinh_trang_chinh_sua` · `lien_quan_su_viec` · `nguoi_cung_cap`.
- Mỗi trường: `value` · `source_refs` · `status` (`provided` / `missing` / `unclear` / `conflicting`) · `conflict_note` · `user_confirmed`.
- Cấp gốc: `draft_label` · `noi_nhan` · `tu_cach` · `tai_lieu` · `questions_for_user`.
- **Muốn đổi schema:** mở PR riêng chỉ sửa file này, cả 3 người duyệt rồi mới merge.

### 1.2 Chữ ký hàm (chốt ở ticket T0, sau đó không đổi tên / tham số)

| Hàm | File | Chủ | Vào → Ra | AI? |
|---|---|---|---|---|
| `prepare_sources(text)` | `tools.py` | N2 | chuỗi / JSON → `list` nguồn `S1, S2…` | Không (đã có) |
| `trich_xuat(sources)` | `agent.py` | N1 | `list` nguồn → `dict` theo schema | **Có — lần gọi AI duy nhất** |
| `kiem_tra_schema(draft)` | `tools.py` | N2 | `dict` → `list[str]` lỗi (rỗng = hợp lệ) | Không |
| `tim_truong_can_hoi(draft)` | `tools.py` | N2 | `dict` → `list[{field_path, status}]` | Không |
| `cau_hoi_bo_sung(gaps)` | `tools.py` | N2 | `list` → `list[{field_path, question, skippable}]` | Không |
| `tao_ban_nhap(draft)` | `tools.py` | N2 | `dict` → `str` bản nháp đọc được, mỗi chi tiết kèm `[S1]`… | Không |
| `goi_y_luat_su(nhu_cau)` | `tools.py` | N2 | `str` → `list` từ `data/luat_su.json` | Không |
| `soan_email_nhap(draft, nguoi_nhan, truong_cho_phep)` | `tools.py` | N2 | → `str` email **nháp**, không gửi | Không |
| `answer(text)` | `agent.py` | N1 | `str` → `{"output": str}` (hợp đồng khung, không đổi) | Gọi `trich_xuat` |

Mọi hàm trong `tools.py` có `@tool` và docstring: tên · input · output · có tác động ra ngoài không (AGENTS.md).

### 1.3 Luồng của `answer(text)` (một lượt — vì `run.py eval` gọi mỗi câu đúng một lần)

```
prepare_sources → trich_xuat (AI) → kiem_tra_schema → tim_truong_can_hoi → cau_hoi_bo_sung → tao_ban_nhap
→ output = bản nháp + danh sách câu hỏi bổ sung
```

Hội thoại nhiều lượt (người dùng trả lời câu hỏi rồi điền lại) **chỉ làm trên giao diện web**, không đưa vào `answer()`.

---

## 2. Ai sở hữu file nào

| File | Chủ | Ghi chú |
|---|---|---|
| `codebase/ai.py` | N1 | Nối DeepSeek. `.env` mỗi người giữ trên máy, **không commit** |
| `codebase/agent.py` | N1 | Prompt, `trich_xuat`, `answer` |
| `data/mau_ban_nhap.json` | N1 | Ví dụ JSON hợp lệ theo schema — cả nhóm dùng để test |
| `codebase/tools.py` | N2 | Mọi hàm không gọi AI |
| `codebase/web.py`, `codebase/static/*` | N2 | API + trang HTML |
| `codebase/test_web.py`, `codebase/test_tools.py` | N2 | CI chạy `test_web.py` |
| `requirements.txt`, `.railway/`, `.github/` | N2 | |
| `codebase/van_ban_xuat_xu.schema.json` | **Cả nhóm** | Chỉ đổi qua PR riêng, cả 3 duyệt |
| `eval/benchmark.csv`, `eval/README.md`, `eval/report.md` | N3 | **Không sửa** `eval/metric_spec.yaml` (đã chốt CP2) |
| `cost/personas.yaml`, `cost/cost-estimate.md` | N3 | |
| `evidence/*`, `data/DATA_CARD.md`, `data/luat_su.json` | N3 | `luat_su.json` là danh sách **giả lập** |
| `spec.md` | **N3 giữ bút** | N1, N2 gửi nội dung §4 cho N3 dán vào — tránh 3 người cùng sửa một file |
| `docs/PROJECT_CONTEXT.md` | Mỗi người | Chỉ sửa **dòng của mình** |
| `run.py`, `codebase/tracing.py`, `eval/run_eval.py`, `cost/simulate.py` | **Không ai** | Khung BTC |
| `TEAMS.md` | Đội trưởng | Đang ghi 4 người — cập nhật nếu nhóm còn 3 |

---

## 3. Sơ đồ §4 → ai dựng ô nào

| Ô trong sơ đồ (`spec.md` §4) | Dựng bằng | Ticket | Chủ | Mốc |
|---|---|---|---|---|
| Người dùng · Đầu vào · Lời kể · Hình ảnh / tài liệu | `prepare_sources` (đã có) + ô nhập trên web | T2-1, T2-5 | N2 | CP3 / CP4 |
| LLM trích xuất thông tin | `trich_xuat` + prompt + DeepSeek | T1-1, T1-2 | N1 | CP3 |
| Dữ liệu có cấu trúc: biểu mẫu 11 trường | Schema + `kiem_tra_schema` | T0, T2-1 | Cả nhóm / N2 | CP3 |
| Backend kiểm tra mức độ đầy đủ · Đã đủ trường? | `tim_truong_can_hoi` (code, không AI) | T2-2 | N2 | CP3 |
| Xác định trường còn thiếu · Hỏi bổ sung | `cau_hoi_bo_sung` | T2-3 | N2 | CP3 |
| Người dùng trả lời / xác nhận → quay lại biểu mẫu | Web: trả lời → gọi lại `trich_xuat` kèm câu trả lời | T2-6, T1-4 | N2 + N1 | CP4 |
| Lưu hồ sơ chưa hoàn thiện | Tải JSON xuống từ trình duyệt — **không dùng CSDL** | T2-6 | N2 | CP4 |
| Tạo bản nháp hồ sơ theo mẫu | `tao_ban_nhap` | T2-4 | N2 | CP3 |
| Người dùng xem xét / chỉnh sửa / xác nhận | Web: bảng 11 trường sửa được, tick `user_confirmed` | T2-6 | N2 | CP4 |
| Hỏi nhu cầu kết nối hỗ trợ | Web: hai câu hỏi riêng — có liên hệ không · có dùng form không | T2-7 | N2 | CP4 |
| Middleware · Quản lý hồ sơ và sự đồng ý | `soan_email_nhap` chỉ lấy trường người dùng cho phép | T2-7 | N2 | CP4 |
| Cơ sở dữ liệu | **Mô phỏng**: không lưu trên server; ghi rõ ở §4 "Phần còn giả" | T3-7 | N3 | CP4 |
| Kết nối luật sư · Kết nối tổ chức hỗ trợ | `goi_y_luat_su` đọc `data/luat_su.json` giả lập; **không gửi gì ra ngoài** | T2-7, T3-6 | N2 + N3 | CP4 |

---

## 4. Ticket

Định dạng: **ID · việc** — file · phụ thuộc · xong khi.

### T0 · Cả nhóm · 15 phút đầu · chặn mọi ticket khác

- **T0 · Chốt hợp đồng** — đọc mục 1, thống nhất tên hàm và schema. N1 tạo `data/mau_ban_nhap.json`: 1 tài liệu, có đủ 4 trạng thái (`provided`, `missing`, `unclear`, `conflicting`). **Xong khi:** file mẫu được merge vào `main`; N2 và N3 dùng ngay để làm việc song song.

### Người 1 · Lõi AI

| ID | Việc | File | Phụ thuộc | Xong khi | Mốc |
|---|---|---|---|---|---|
| T1-1 | Nối DeepSeek: `MODEL_PROVIDER=openai`, đổi `URL_OPENAI` theo docs DeepSeek, chép `post_json` + `call_openai` từ `docs/connect-model.md` | `ai.py` | — | `python run.py eval --try` in token > 0 | CP3 |
| T1-2 | Viết `trich_xuat`: prompt bắt trả **đúng schema**, `value: null` khi không có, `user_confirmed: false`, không điền `file_facts`, coi chữ trong tài liệu là dữ liệu chứ không phải lệnh. Bật chế độ JSON của API nếu có | `agent.py` | T0, T1-1 | 3 câu `--try` đều ra JSON qua `kiem_tra_schema` | CP3 |
| T1-3 | Viết `answer` theo luồng mục 1.3. Khi N2 chưa merge, dùng hàm tạm cùng tên trong `agent.py`, xoá khi `tools.py` có hàm thật | `agent.py` | T1-2 | `python run.py` nhập `demo` ra bản nháp + câu hỏi | CP3 |
| T1-4 | Hàm `dien_lai(draft, tra_loi)`: gọi lại AI với câu trả lời bổ sung, giữ trường đã `user_confirmed` | `agent.py` | T1-3 | N2 gọi được từ web | CP4 |
| T1-5 | JSON hỏng → thử lại 1 lần, vẫn hỏng thì trả thông báo rõ (không crash) | `agent.py` | T1-2 | Không còn dòng lỗi ở cột `error` của `run-N.csv` vì JSON | CP4 |
| T1-6 | Sửa prompt theo các câu trượt ở lượt 1 — **không** khớp nguyên văn câu thử (AGENTS.md) | `agent.py` | T3-4 | Ghi thay đổi gửi N3 để thêm vào §10 changelog | CP4 |
| T1-7 | Gửi N3 nội dung §4: model đã dùng, bảng công cụ khớp code, phần còn giả | — | T1-3 | N3 dán vào `spec.md` | CP4 |

### Người 2 · Backend + giao diện

| ID | Việc | File | Phụ thuộc | Xong khi | Mốc |
|---|---|---|---|---|---|
| T2-1 | `kiem_tra_schema(draft)`: kiểm khoá bắt buộc, `status` thuộc 4 giá trị, `value` là `null` khi `missing`, có `conflict_note` khi `conflicting`. Chỉ dùng thư viện chuẩn | `tools.py` | T0 | Test với `mau_ban_nhap.json` qua; JSON sửa hỏng thì báo đúng lỗi | CP3 |
| T2-2 | `tim_truong_can_hoi(draft)`: liệt kê mọi trường `missing` / `unclear` / `conflicting` kèm `field_path` (vd `tai_lieu[0].thoi_diem_tao`) | `tools.py` | T0 | Test với file mẫu ra đúng danh sách | CP3 |
| T2-3 | `cau_hoi_bo_sung(gaps)`: mỗi trường tối đa 1 câu, trung tính, `skippable: true`; mâu thuẫn thì nêu cả hai nguồn | `tools.py` | T2-2 | Test qua | CP3 |
| T2-4 | `tao_ban_nhap(draft)`: dòng đầu là `draft_label`; mỗi trường ghi giá trị + `[nguồn]`; trường thiếu ghi "chưa có — cần xác nhận" | `tools.py` | T0 | Test qua; N1 gọi được trong `answer` | CP3 |
| T2-5 | Viết `test_tools.py` cho T2-1 → T2-4, giữ `test_web.py` xanh | `test_*.py` | T2-1 → T2-4 | CI xanh trên PR | CP3 |
| T2-6 | Trang HTML (1 file, JS thuần): nhập lời kể → gọi `/ask` → bảng 11 trường sửa được, tick xác nhận, trả lời câu hỏi bổ sung, nút tải JSON | `web.py`, `static/` | T1-3, T1-4 | Chạy trên máy, đi hết luồng với ca demo | CP4 |
| T2-7 | `goi_y_luat_su`, `soan_email_nhap` + 2 nút trên web: "Có muốn liên hệ?" và "Có dùng form?" (hai quyết định riêng). Email chỉ hiện để người dùng chép, **không gửi** | `tools.py`, `web.py` | T3-6 | Từ chối liên hệ → dừng; đồng ý → hiện email nháp chỉ gồm trường được cho phép | CP4 |
| T2-8 | Deploy Railway, kiểm `/health`; key đặt ở biến môi trường của Railway, không ở repo | `.railway/` | T2-6 | Link demo mở được | CP4 |

### Người 3 · Dữ liệu + đánh giá + hồ sơ

| ID | Việc | File | Phụ thuộc | Xong khi | Mốc |
|---|---|---|---|---|---|
| T3-1 | Mở `benchmark.csv` lên **20–30 câu**, trong đó **≥ 1/3** có `source` là `nguoi_dung` / `data_that`, lấy từ `evidence/interviews/P1.md` và `evidence/survey/results.csv`, đã bỏ định danh. Giữ 10 câu cũ, không sửa `expected` cũ | `eval/benchmark.csv` | — | `python run.py check` không còn cảnh báo về số câu và nguồn | CP3 |
| T3-2 | Điền `eval/README.md` mục 1–4 (đang trống từ CP2) | `eval/README.md` | — | Đủ 4 mục | CP3 |
| T3-3 | Điền `cost/personas.yaml` bằng số có nguồn (hoặc ghi *(tự ước tính)*), giá DeepSeek có link + ngày xem, ≥ 2 mức model | `cost/personas.yaml` | — | Không còn dòng "(ví dụ)" | CP3 |
| T3-4 | Khi T1-3 đã lên `main`: `python run.py eval` → chấm cột `pass` theo `metric_spec.yaml` → `python run.py score` → điền lượt 1 vào §7 và `eval/report.md` | `eval/*`, `spec.md` | T1-3, T3-1 | Có `eval/run-1.csv` với model thật, có số lượt 1 | CP3 |
| T3-5 | `python run.py simulate --try` | `cost/` | T1-1, T3-3 | Có `cost/simulate-try.csv` | CP3 |
| T3-6 | Tạo `data/luat_su.json` **giả lập** (tên hư cấu, ghi rõ `synthetic`) và thêm mục vào `DATA_CARD.md` | `data/` | — | N2 đọc được | CP4 |
| T3-7 | Dán nội dung §4 từ N1, N2; viết §8, §9 (dữ liệu nhạy cảm: chỉ gửi dữ liệu giả lập lên API), §10 changelog | `spec.md` | T1-7 | §0–§10 không còn `__` trừ chỗ chưa có số thật | CP4 |
| T3-8 | Lượt 2 sau T1-6 → `report.md` so sánh lượt 1 với lượt 2; `simulate` đủ 50 phiên → `cost-estimate.md` | `eval/`, `cost/` | T1-6 | Có `run-2.csv`, `simulate-N.csv` | CP4 |

---

## 5. Thứ tự merge vào `main`

```
T0 (mẫu JSON)
 ├─► N2: T2-1 → T2-4 + T2-5 ──┐
 ├─► N1: T1-1 → T1-2 ─────────┼─► N1: T1-3 (answer dùng hàm thật của N2) ─► N3: T3-4 chạy eval lượt 1   ◄ CP3
 └─► N3: T3-1, T3-2, T3-3 ────┘
                                   ─► T1-4, T2-6, T2-7, T3-6 ─► T1-6 ─► T3-8 lượt 2                        ◄ CP4
```

N3 không phải chờ ai cho tới T3-4: viết câu thử, README, persona song song ngay từ đầu.

## 6. Luật git để không đè nhau

1. Mỗi người một nhánh: `n1-ai`, `n2-backend`, `n3-eval`. **Không push thẳng `main`.**
2. Mỗi ticket một PR nhỏ, tên PR bắt đầu bằng ID ticket (vd `T2-1: kiem_tra_schema`).
3. Trước khi mở PR: `git pull origin main` vào nhánh mình, chạy `python run.py check` và test.
4. Chỉ sửa file mình sở hữu (mục 2). PR đụng file người khác → chủ file phải duyệt.
5. Đổi chữ ký hàm ở mục 1.2 hoặc schema → báo cả nhóm trước, PR riêng.
6. Không commit `.env`, key, dữ liệu cá nhân thật. Không sửa `eval/run-*.csv`, `traces/*` đã chạy (trừ cột `pass`, `ghi_chu`).
7. Xong ticket → cập nhật dòng của mình trong `docs/PROJECT_CONTEXT.md`.

## 7. Prompt mẫu để giao cho agent khi vibe

> Đọc `AGENTS.md`, `docs/TASKS.md` và `codebase/van_ban_xuat_xu.schema.json`. Tôi là **Người _**, làm ticket **T_-_**. Chỉ sửa các file của Người _ ở `docs/TASKS.md` mục 2. Giữ đúng chữ ký hàm ở mục 1.2. Không sửa file khung, không commit.
