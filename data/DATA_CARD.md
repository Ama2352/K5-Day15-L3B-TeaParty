# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử (bài mẫu, thông báo mẫu, đoạn transcript…) để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

## Bộ câu thử · `eval/benchmark.csv`

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | Đo bản chạy thử theo `eval/metric_spec.yaml`; đầu vào cho mô phỏng chi phí. |
| Nguồn và cách tạo | `synthetic`, tình huống hư cấu nhóm tự dựng (`tu_viet` theo cột `source`). Đưa vào repo ở commit `2d787a3`. Có dùng AI để soạn hay không: __. Seed: __ (nếu có). |
| Xử lý | Nhân vật ghi bằng ký hiệu A, B; mỗi đoạn nguồn có mã; hội thoại và nguồn gộp trong một ô `input`. |
| Quy mô | 10 câu: 3 `thuong` · 5 `kho` · 2 `tu_choi`. |
| Người kiểm / số câu kiểm tay | __ |
| Giới hạn | Chỉ có chữ; chưa có ảnh, âm thanh, bước liên hệ luật sư. 0/10 từ người dùng hoặc data thật. Không phải bằng chứng pain. |

## Khảo sát · `evidence/survey/results.csv`

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | Bằng chứng pain và số cho `spec.md` §0–§2. Không đưa vào model. |
| Nguồn và cách tạo | **Thật**, nhóm tự thu bằng Google Form ẩn danh. Câu hỏi: `evidence/survey/questions.md`. |
| Xử lý | Bỏ cột thời gian, thay bằng mã S01–S21. Form không thu tên, email. Không loại phiếu nào. |
| Quy mô / ngày lấy | 21 phiếu, phản hồi từ 19:09 đến 19:27 ngày 27/11/2026. |
| Giới hạn | 16/21 ở độ tuổi 18–24; chỉ 2/21 đúng người dùng của lát cắt; gộp mọi loại vấn đề ở nơi làm việc; S04, S14 có phương án trái nhau; chưa xác nhận đã loại thành viên nhóm hoặc phiếu điền thử. |

## Ghi chép lời kể · `evidence/interviews/P1.md`

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | Ghi nhận cách xoay xở; **không tính** vào ngưỡng phỏng vấn. |
| Nguồn và cách tạo | **Thật**, một lời kể tự do do thành viên nhóm chép lại; người kể đã đồng ý. |
| Xử lý | Bỏ chi tiết sự việc và thông tin nhận diện; giữ 2 trích dẫn ngắn. |
| Quy mô | 1 người. |
| Giới hạn | Người kể là bệnh nhân, không phải người dùng chính; có hỏi theo các câu trong file, nhiều câu lời trả lời không nhắc tới. |

## Ghi chép phỏng vấn · `evidence/interviews/P2.md`

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | Bằng chứng pain. Không đưa vào model. |
| Nguồn và cách tạo | **Thật**, thành viên nhóm hỏi và ghi theo lời kể; người kể đã đồng ý. |
| Xử lý | Bỏ chi tiết nhận diện; ghi bằng mã P2. |
| Quy mô | 1 người. |
| Giới hạn | Chưa xác nhận là nguyên văn; không hỏi số lần và thời gian; chưa rõ đã soạn bản phản ánh trong tháng qua; câu 8–10 là ý kiến. |

## Ca chạy thử CP2 · `cp2_demo.json`

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | Lệnh `demo` của CLI và test API cho ca ngày mâu thuẫn. |
| Nguồn và cách tạo | `synthetic`, viết tay một sự việc hư cấu gồm lời kể, ghi chú, kết quả OCR mẫu và bản chép lời mẫu. Không dùng seed. |
| Xử lý | Khai báo ngày theo từng nguồn. Để trống ngày khi nguồn thiếu thông tin. CLI giữ tệp gốc và gắn mã nguồn khi đọc. |
| Quy mô và kiểm tra | 1 ca, 4 đoạn nguồn rà khi soạn. Test đối chiếu hai ngày tới đúng mã và kiểm tra bản chép lời có trong đầu ra. |
| Giới hạn | Minh họa một tình huống mâu thuẫn về ngày. Không đo chất lượng OCR, chép lời hay bằng chứng về khó khăn của người dùng. |
