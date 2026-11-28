# Dàn slide → lấy số từ file nào

> Làm ở guide bước 5.1. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.
> Xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo, nộp tại CP4 14:30 Thứ Bảy 28/11. Nộp PDF, không nộp link.
> [PDF bản chốt](../demo-slides.pdf) có 8 trang theo khung ở guide 5.1. Bản 13 trang trình bày lúc CP4 nằm trong lịch sử git (PR #35).

| # | Trang | Có gì | Số lấy từ |
|---|---|---|---|
| 1 | Em có bằng chứng không? | Tình huống giả lập Linh, Minh; trích dẫn P3; 3 người ngoài nhóm đã làm bước chuẩn bị | `evidence/summary.md` §2–3 · `spec.md` §1 |
| 2 | Vì sao chọn hỗ trợ soạn hồ sơ? | ≈ 56 phút / tháng trong mẫu = 6 người × 0,31 lần × 30 phút; hai hướng đã loại | `spec.md` §2 · `evidence/survey/results.csv` câu 6, 8, 11 |
| 3 | Từ tư liệu rời đến bản nháp | Nguồn → DeepSeek trích xuất → người dùng rà; email nháp chỉ gồm trường đã xác nhận | `spec.md` §4 · `codebase/van_ban_xuat_xu.schema.json` |
| 4 | Hai ca demo, hai cách rà | Ca thường B01, ca khó B05 (hai nguồn lệch ngày); link demo web và video dự phòng | `eval/benchmark.csv` B01, B05 · `README.md` |
| 5 | Đánh giá thế nào? | 26 câu, 16 từ dạng tình huống phỏng vấn/khảo sát; 17/26 → 18/26 → 23/26; điền đúng trường 15/18 < 90% | `eval/report.md` §1, §4 · `spec.md` §7 |
| 6 | Chi phí khi dùng thật | $0,0153 / task thành công (tỉ lệ lượt 2); tháng $0,56 / $2,80 / $11,21 (Flash) | `cost/cost-estimate.md` §2–3 · `cost/simulate-3-summary.md` |
| 7 | Kết luận: Iterate | Bàn giao 5/5; điền đúng trường 15/18, lên Go cần ≥ 17/18; 23/26; $0,0153 | `spec.md` §1, §7 · `eval/report.md` §1 · `cost/cost-estimate.md` §2 |
| 8 | Nếu có thêm một tuần | Sửa B13, B16; thử luồng rà B23 với người ngoài nhóm | `eval/report.md` §4 · `spec.md` §7 |

**Trước khi lên:** tải repo về một máy khác (hoặc thư mục mới), chạy theo mục "Chạy trong 3 phút" của `README.md` · `.env` có trên máy demo, đã gọi thử 1 câu trong vòng 1 giờ trước giờ demo · video dự phòng mở được bằng cửa sổ ẩn danh · biết bản chạy thử sẽ làm gì với **1 câu thử lạ** của giám khảo · ca của Linh đã soạn sẵn đoạn nhập (dữ liệu giả lập) và đã chạy thử.

Ai nói trang nào (mỗi người ≥1 phần):

| Trang | Người nói |
|---|---|
| 1 | Khánh Linh |
| 2 | Quyên |
| 3 | Quyên |
| 4 | Khánh Linh |
| 5 | Quỳnh Anh |
| 6 | Quỳnh Anh |
| 7 | Sang |
| 8 | Sang |
