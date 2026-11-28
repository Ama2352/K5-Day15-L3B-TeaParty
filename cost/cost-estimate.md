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
- **Tỉ lệ đạt** dùng để tính: 19/26 (73%) — lượt `run-2@20261128-030638` (lượt 2)
- Đo token trên model `deepseek-chat`, tính giá model `deepseek-flash` và `deepseek-v4-pro`. Trang giá không còn liệt kê `deepseek-chat`; changelog DeepSeek (mục 2026-04-24) ghi tên này trỏ tới `deepseek-v4-flash` và ngừng sau 24/07/2026, nhưng API vẫn nhận ngày 28/11/2026. Việc áp giá Flash cho `deepseek-chat` là *(tự ước tính)*.
- Code khi mô phỏng: `codebase/agent.py` bản `f552139` (T1-6 trên `main` trước PR #14). Lượt 2 đo tỉ lệ đạt trên bản PR #14 (`f9cc0d6`). Hai bản cùng một lần gọi AI mỗi lượt và thử lại ≤1 lần, nên số token mỗi lượt tương đương (lượt 2: TB 7315 vào / 1546 ra mỗi câu).

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-032943` · 50 phiên · seed 42 · 0/50 phiên lỗi

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 16 | 1 | 6701 | 1362 | 1.0 | 1.0 |
| dung_vua | 27 | 2 | 13426 | 2699 | 2.0 | 2.0 |
| dung_nhieu | 7 | 4 | 27838 | 6338 | 4.1 | 4.0 |

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| deepseek-flash | $0.0073 | $0.0100 | $0.3953 | $1.98 | $7.91 | $0.0040 |
| deepseek-v4-pro | $0.0286 | $0.0391 | $1.54 | $7.69 | $30.75 | $0.0154 |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): ≈ 9 phút tiết kiệm cho mỗi người tự chuẩn bị hồ sơ (0,31 lần / tháng × 30 phút mỗi lần, trung vị khảo sát; tổng 56 phút / tháng cho 6 người trong mẫu). Số này gộp mọi loại vấn đề ở nơi làm việc và chưa suy ra quy mô thật.
- Chi phí / người / tháng (cơ sở, model `deepseek-flash`): $0,0040 (với `deepseek-v4-pro`: $0,0154).
- **Kết luận một dòng — đáng làm không:** chi phí model không phải điểm nghẽn (dưới 1 cent mỗi người mỗi tháng, kể cả ở mức `deepseek-v4-pro`); câu hỏi quyết định là chất lượng — lượt 2 mới đạt 73% và bước liên hệ luật sư 2/5, chưa đạt chuẩn `spec.md` §7.

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy *(tự ước tính, từ cùng số token)*: dùng giá giờ thấp điểm → chi phí giảm một nửa; cache hit cho phần system prompt lặp lại (khoảng 5–6 nghìn token vào mỗi lượt) có thể giảm thêm phần lớn chi phí đầu vào; mỗi lần thử lại khi JSON hỏng cộng thêm khoảng một lượt gọi.
- Chi phí ngoài model chưa tính: hosting Railway, lưu trữ (hiện không lưu hồ sơ trên server), giờ công người duyệt và thẩm định pháp lý, bảo mật trước khi dùng dữ liệu thật.
