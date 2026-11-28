# Dàn slide → lấy số từ file nào

> Làm ở guide bước 5.1. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.
> Xuất PDF thành `demo-slides.pdf` ở thư mục gốc repo, nộp tại CP4 14:30 Thứ Bảy 28/11. Nộp PDF, không nộp link.
> Bản đã xuất: `demo-slides.pdf` (13 trang), xuất từ deck "Hồ Sơ An Toàn · AI Evidence Assistant · TeaParty · CP4". Nếu deck đổi thì xuất lại và chép đè file này.
> Kịch bản thuyết trình 5 phút: [kich-ban-5-phut.md](kich-ban-5-phut.md).

| # | Trang | Có gì | Số lấy từ | Xong |
|---|---|---|---|---|
| 1 | Chỉ là một trò đùa | Linh, ba tin nhắn giả lập; ghi chú dựng lại, hư cấu (VnExpress 30/4/2022, VietNamNet 22/4/2024) | Hư cấu, không có số | ☑ |
| 2 | Đàn ông thì có gì mà phải sợ? | Minh, câu đồng nghiệp nói "con trai với nhau" | Hư cấu, không có số | ☐ ảnh có watermark, thay rồi xuất lại |
| 3 | Em có bằng chứng không? | Năm câu hỏi hiện theo từng lần bấm | Không có số | ☑ |
| 4 | Không chỉ là kịch | Lời P1–P3 (hỏi lại 28/11), 6/6 người phải viết lại, 8/13 mất từ 1 giờ | `evidence/summary.md` §2–3 · `spec.md` §1 | ☑ |
| 5 | Câu hỏi xuyên suốt | "Khi lên tiếng đã khó, tại sao trình bày lại khó đến thế?" | Không có số | ☑ |
| 6 | Hồ Sơ An Toàn | Tên sản phẩm, câu "không thể hứa" | Không có số | ☑ |
| 7 | Giải pháp | Luồng: trích xuất song song, code kiểm, người dùng quyết; không gửi gì | `spec.md` §4 | ☑ |
| 8 | Demo trên app thật | Ca của Linh (giả lập): đã có / chưa xác định / còn thiếu. App thật, DeepSeek; ảnh và ghi âm nhập dạng chữ | `codebase/web.py`, `spec.md` §4 · eval lượt 3 | ☐ chưa chạy thử trước giờ, cần soạn sẵn đoạn nhập |
| 9 | **Đánh giá thế nào** | 26 câu, 4 metric; lượt 1 → 3: 65% → 69% → 88%; còn trượt B13, B16, B23 | `eval/report.md` §1, `eval/README.md` §5–6 · run-1, run-2, run-3 | ☑ |
| 10 | **Chi phí khi dùng thật** | $0,0106 mỗi phiên; ≈ $0,012 mỗi task thành công (23/26, tính tay); $2,80 mỗi tháng ở 500 người | `cost/cost-estimate.md` §2 · `simulate-3` | ☑ |
| 11 | Vì sao chọn bài này, và hướng phát triển | ≈ 56 phút mỗi tháng trong mẫu; hướng đã loại; ba bước "kiểm chứng trước, mở rộng sau" | `spec.md` §2 · PRD v0.2 §13 (Google Doc) | ☐ mục 3 để sau, giữ nguyên theo ý nhóm |
| 12 | Tiếng nói thuộc về họ | Lời Linh và Minh; "không ai nên phải lựa chọn giữa phẩm giá và công việc" | Không có số | ☑ |
| 13 | Kết | "Your story. Your voice. Your choice." | Không có số | ☑ |

**Trước khi lên:** tải repo về một máy khác (hoặc thư mục mới), chạy theo mục "Chạy trong 3 phút" của `README.md` · `.env` có trên máy demo, đã gọi thử 1 câu trong vòng 1 giờ trước giờ demo · video dự phòng mở được bằng cửa sổ ẩn danh · biết bản chạy thử sẽ làm gì với **1 câu thử lạ** của giám khảo · ca của Linh đã soạn sẵn đoạn nhập (dữ liệu giả lập) và đã chạy thử.

Ai nói trang nào (mỗi người ≥1 phần):

| Trang | Người nói |
|---|---|
| | |
