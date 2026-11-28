# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu theo khảo sát câu 8 (số lần chuẩn bị hoặc bổ sung tài liệu trong 12 tháng, n = 13, chia 12):
  - `dung_it` 38,5% (5/13) · 0,16 phiên / người / tháng · 1 lượt / phiên
  - `dung_vua` 46% (6/13) · 0,42 phiên / người / tháng · 2 lượt / phiên
  - `dung_nhieu` 15,5% (2/13) · 0,94 phiên / người / tháng · 4 lượt / phiên
  - Nguồn: `evidence/survey/results.csv`, `spec.md` §2. Số lượt / phiên: *(tự ước tính)* theo mức 1 / 2 / 4 lượt trong thẻ đề.
- **Số người dùng thật** 3 kịch bản: thấp 100 · cơ sở 500 · cao 2.000. Nguồn: *(tự ước tính)* quy mô thử nghiệm qua 1–3 tổ chức hỗ trợ hoặc văn phòng luật; nhóm chưa có số công khai về người cần chuẩn bị hồ sơ quấy rối tình dục nơi làm việc.
- **Giá** 2 mức model, giá giờ cao điểm, input tính cache miss (mức cao): `deepseek-flash` vào $0,30 · ra $1,20 / 1 triệu token · `deepseek-v4-pro` vào $1,32 · ra $3,96 / 1 triệu token — https://api-docs.deepseek.com/quick_start/pricing, xem 28/11/2026. Giờ thấp điểm bằng một nửa.
- **Tỉ lệ đạt** dùng để tính (trong file khung sinh ra): 18/26 (69%) — lượt `run-2@20261128-030638` (`simulate-3` chạy lúc 10:30, trước khi chấm lượt 3). Lượt 3 (`run-3@20261128-102828`, cùng code với `simulate-3`) đạt 23/26 (88%); số tính theo tỉ lệ này ghi riêng ở §2, có ghi là tính tay.
- Đo token trên model `deepseek-chat`, tính giá model `deepseek-flash` và `deepseek-v4-pro`. Trang giá không còn liệt kê `deepseek-chat`; changelog DeepSeek (mục 2026-04-24) ghi tên này trỏ tới `deepseek-v4-flash` và ngừng sau 24/07/2026, nhưng API vẫn nhận ngày 28/11/2026. Việc áp giá Flash cho `deepseek-chat` là *(tự ước tính)*.
- Code khi mô phỏng: `simulate-3` chạy trên code `fd99197` (PR #27 của N1: trích xuất song song ≤4 lời gọi + 1 lời gọi bàn giao mỗi lượt, hàm thật của N2), cùng code với lượt 3. Mỗi lượt gọi model khoảng 2,5 lần và mỗi lời gọi đọc lại toàn bộ nguồn, nên token vào / phiên gần gấp đôi `simulate-2` (`97c9a9e`, 1 lời gọi / lượt). `simulate-1` chạy trên `f552139`.

## 2. Kết quả mô phỏng

Lượt thử trước đó (T3-5): `python run.py simulate --try` → `simulate-try@20261128-032804`, 10 phiên, token đo từ API `deepseek-chat`. Theo `.gitignore` của khung, lượt `--try` không được tính nên `cost/simulate-try*` và `traces/simulate-try.jsonl` không đưa vào repo.

Lượt mô phỏng: `cost/simulate-3.csv` · run ID `simulate-3@20261128-103013` · 50 phiên · seed 42 · 0/50 phiên lỗi · `--rate-from eval/run-2.csv` · N1 chạy

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 16 | 1 | 12146 | 1226 | 2.5 | 6.0 |
| dung_vua | 27 | 2 | 26044 | 2535 | 5.2 | 12.4 |
| dung_nhieu | 7 | 4 | 51908 | 5273 | 10.4 | 24.6 |

| Model | Chi phí / phiên | Chi phí / task thành công (18/26, file khung) | Chi phí / task thành công (23/26, lượt 3, tính tay) | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|---|
| deepseek-flash | $0.0106 | $0.0153 | ≈ $0.0120 | $0.5603 | $2.80 | $11.21 | $0.0056 |
| deepseek-v4-pro | $0.0432 | $0.0624 | ≈ $0.0488 | $2.29 | $11.45 | $45.79 | $0.0229 |

Cột "tính tay" = chi phí / phiên trong file khung ÷ 23/26, làm tròn từ số đã làm tròn 4 chữ số nên chỉ là xấp xỉ; nhóm không chạy lại mô phỏng với `--rate-from eval/run-3.csv`. Chi phí / tháng không phụ thuộc tỉ lệ đạt.

**So các lượt mô phỏng** (cùng persona, seed 42, 50 phiên):

| Lượt mô phỏng | Code | Gọi model / phiên (TB) | Flash / phiên | Flash / tháng cơ sở | v4-pro / tháng cơ sở |
|---|---|---:|---:|---:|---:|
| `simulate-1@20261128-032943` | `f552139`, 1 lời gọi / lượt | ≈ 2,0 | $0.0073 | $1.98 | $7.69 |
| `simulate-2@20261128-093242` | `97c9a9e`, 1 lời gọi / lượt, hàm thật của N2 | ≈ 2,0 | $0.0076 | $2.01 | $7.82 |
| `simulate-3@20261128-103013` | `fd99197`, song song + bàn giao | ≈ 5,1 | $0.0106 | $2.80 | $11.45 |

Gọi model / phiên TB tính theo tỉ trọng số phiên mỗi persona (16 / 27 / 7) trong file khung. Độ trễ đo ở eval (giây / câu, `eval/report.md` §1): lượt 2 TB 4,56 · p95 7,20; lượt 3 TB 3,71 · p95 9,04. Song song làm mỗi lượt nhanh hơn khoảng 0,85 giây nhưng tốn thêm khoảng 40% chi phí model.

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): ≈ 9 phút tiết kiệm cho mỗi người tự chuẩn bị hồ sơ (0,31 lần / tháng × 30 phút mỗi lần, trung vị khảo sát; tổng 56 phút / tháng cho 6 người trong mẫu). Số này gộp mọi loại vấn đề ở nơi làm việc và chưa suy ra quy mô thật.
- Chi phí / người / tháng (cơ sở, model `deepseek-flash`): $0,0056 (với `deepseek-v4-pro`: $0,0229) — `simulate-3`, code hiện tại.
- **Kết luận một dòng — đáng làm không:** chi phí model không phải điểm nghẽn (dưới 1 cent mỗi người mỗi tháng, kể cả ở mức `deepseek-v4-pro`); câu hỏi quyết định là chất lượng — lượt 3 đạt 88% (23/26), bàn giao 5/5, nhưng metric điền đúng trường có nguồn 15/18 (83% < 90%) nên chưa đạt chuẩn `spec.md` §7.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy *(tự ước tính, từ cùng số token)*: dùng giá giờ thấp điểm → chi phí giảm một nửa; cache hit cho phần system prompt lặp lại (khoảng 5–6 nghìn token vào mỗi lượt) có thể giảm thêm phần lớn chi phí đầu vào; mỗi lần thử lại khi JSON hỏng cộng thêm khoảng một lượt gọi.
- Chi phí ngoài model chưa tính: hosting Railway, lưu trữ (hiện không lưu hồ sơ trên server), giờ công người duyệt và thẩm định pháp lý, bảo mật trước khi dùng dữ liệu thật.
