# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử (bài mẫu, thông báo mẫu, đoạn transcript…) để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

## Dataset 1 · [tên]

| | |
|---|---|
| Dùng để làm gì | nguồn cho công cụ `…` · bộ câu thử · đào bằng chứng |
| Từ đâu | data BTC cấp (`…` trong repo đề) · tài liệu khoá (trích / viết lại) · nhóm tự viết · sinh có seed |
| Xử lý những bước gì | lọc __ · làm sạch __ · ẩn danh __ · chia __ (script: `…`) |
| Số dòng / số đoạn | __ |
| Phiên bản / ngày lấy | __ |
| Nhãn | thật · `synthetic` |
| Giới hạn | thiếu gì, lệch về phía nào |

**Data `synthetic` (nhóm tự sinh):** ghi cách sinh (prompt / script), seed, người kiểm, số dòng đã kiểm tay. Data tự dựng **không phải bằng chứng pain**.

## Dataset 2 · [tên]

…

## Ca chạy thử CP2 · `cp2_demo.json`

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | Lệnh `demo` của CLI và test API cho ca ngày mâu thuẫn. |
| Nguồn và cách tạo | `synthetic`, viết tay một sự việc hư cấu gồm lời kể, ghi chú, kết quả OCR mẫu và bản chép lời mẫu. Không dùng seed. |
| Xử lý | Khai báo ngày theo từng nguồn. Để trống ngày khi nguồn thiếu thông tin. CLI giữ tệp gốc và gắn mã nguồn khi đọc. |
| Quy mô và kiểm tra | 1 ca, 4 đoạn nguồn rà khi soạn. Test đối chiếu hai ngày tới đúng mã và kiểm tra bản chép lời có trong đầu ra. |
| Giới hạn | Minh họa một tình huống mâu thuẫn về ngày. Không đo chất lượng OCR, chép lời hay bằng chứng về khó khăn của người dùng. |
