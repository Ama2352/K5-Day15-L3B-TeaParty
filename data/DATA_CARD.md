# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Một trang. Mỗi dataset một mục. Dữ liệu chạy thử (bài mẫu, thông báo mẫu, đoạn transcript…) để trong thư mục `data/` này.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

## Bộ câu thử · `eval/benchmark.csv`

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | Đo bản chạy thử theo `eval/metric_spec.yaml`; đầu vào cho mô phỏng chi phí. |
| Nguồn và cách tạo | Mọi chi tiết sự việc đều `synthetic`. B01–B10 (`tu_viet`) do nhóm tự dựng, đưa vào repo ở commit `2d787a3`. B11–B26 (thêm 28/11) lấy **dạng tình huống** từ nguồn thật: 9 câu `nguoi_dung` theo P2 (5 câu), P3 (B23, B24) và P1 (B25, B26) (`evidence/interviews/`), 7 câu `data_that` theo câu trả lời khảo sát (`evidence/survey/results.csv`, ghi số câu và mã phiếu ở cột `source`); ngày, lời thoại, OCR và chép lời trong câu vẫn là giả lập. B11–B26 soạn cùng Claude Code, N3 rà. Không dùng seed. |
| Xử lý | Nhân vật ghi bằng ký hiệu A, B; mỗi đoạn nguồn có mã ([LK1] lời kể, [TN1] tin nhắn chép, [GC1] ghi chú, [ANH1] kết quả OCR mẫu, [GA1] bản chép lời mẫu, [DM] danh mục hỗ trợ giả lập); hội thoại nhiều lượt và nguồn gộp trong một ô `input`. Không đưa trích dẫn hay chi tiết nhận diện của P1–P3 hoặc phiếu khảo sát vào câu thử. |
| Quy mô | 26 câu: 7 `thuong` · 14 `kho` · 5 `tu_choi`. Nguồn: `nguoi_dung` 9 · `data_that` 7 · `tu_viet` 10 → 16/26 câu lấy dạng tình huống từ phỏng vấn hoặc khảo sát. |
| Người kiểm / số câu kiểm tay | `python run.py check` xác nhận cấu trúc bộ 26 câu và 4 metric, chưa có điểm đầu ra từ lần kiểm này. Kiểm tay: N3 rà B11–B26 trước khi commit; chưa có người thứ hai kiểm. |
| Giới hạn | Ảnh và âm thanh chỉ có dạng chữ (OCR mẫu, chép lời mẫu), không đo chất lượng OCR hay chép lời. `nguoi_dung`/`data_that` chỉ là nguồn của dạng tình huống, các tình huống mượn từ phỏng vấn chỉ dựa trên P1–P3, còn khảo sát gộp nhiều loại vấn đề tại nơi làm việc. Bằng chứng về khó khăn của người dùng được tổng hợp ở [summary.md](../evidence/summary.md). |

## Danh mục hỗ trợ giả lập · `luat_su.json`

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | Đầu vào của `goi_y_luat_su` (N2) và khớp với danh mục `[DM]` trong câu thử B17, B20. |
| Nguồn và cách tạo | `synthetic`, nhóm tự viết 28/11/2026. Tên hư cấu (Hư Cấu An, Bình, Cường), liên hệ dùng tên miền `.invalid`. Mỗi mục có `synthetic: true`. |
| Xử lý | Khoá `lawyers`; mỗi mục có `id`, `name`, `email`, `specialties` (định dạng `goi_y_luat_su` của N2 đọc) và thêm `loai` (`luat_su` / `to_chuc_ho_tro`), `khu_vuc`, `hinh_thuc`. |
| Quy mô | 3 mục: LS01 Hà Nội, LS02 TP. Hồ Chí Minh, TC01 trực tuyến toàn quốc. Không có mục ở Đà Nẵng (dùng cho B20). |
| Giới hạn | Không phải danh sách hay xếp hạng luật sư thật; app không gửi gì tới các địa chỉ này. Dùng thật cần danh mục được thẩm định. |

## Khảo sát · `evidence/survey/results.csv`

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | Bằng chứng pain và số cho `spec.md` §0–§2. Không đưa vào model. |
| Nguồn và cách tạo | **Thật**, nhóm tự thu bằng Google Form ẩn danh. Câu hỏi: `evidence/survey/questions.md`. |
| Xử lý | Bỏ cột thời gian, thay bằng mã S01–S21. Form không thu tên, email. Không loại phiếu nào. |
| Quy mô / ngày lấy | 21 phiếu, phản hồi từ 19:09 đến 19:27 ngày 27/11/2026. |
| Giới hạn | 16/21 ở độ tuổi 18–24; chỉ 2/21 đúng người dùng của lát cắt; gộp mọi loại vấn đề ở nơi làm việc; S04, S14 có phương án trái nhau; chưa xác nhận đã loại thành viên nhóm hoặc phiếu điền thử. |

## Ghi chép phỏng vấn · P1–P3

Ba ghi chép từ người tham gia thật, dùng để tổng hợp bằng chứng về trải nghiệm tại nơi làm việc và việc chuẩn bị phản ánh. Nhóm dùng mã P1–P3 và lược bỏ thông tin nhận diện. Các ghi chép chủ yếu ở dạng tóm tắt. P1, P2 và P3 mỗi người có một đoạn trích nguyên văn. Các ghi chép không đưa vào model. Cách xoay xở của P1–P3 được dùng làm cơ sở dựng 9 câu thử giả lập (P2: B11–B14, B22 · P3: B23, B24 · P1: B25, B26); không đưa trích dẫn vào câu thử.

| Hồ sơ | Nguồn và cách xử lý | Giới hạn |
|---|---|---|
| [P1](../evidence/interviews/P1.md) | Nhân viên tại chính phòng khám được nhắc đến. TV3 hỏi và ghi qua cuộc gọi điện thoại khoảng 10:00 ngày 27/11/2026. Bản tóm tắt ghi nhận việc nhân viên bị mắng, bị cho xem hình ảnh nhạy cảm và các hành vi, lời lẽ được kể lại. | Đoạn trích ghi nhận lo ngại về thu nhập và khả năng tìm việc khác. P1 nhắc gián tiếp đến ý định quay và đăng tố cáo, nhưng không dám làm vì sợ bị bác sĩ gây khó dễ. Khi hỏi lại, P1 xác nhận đã xin lời khuyên từ người thân và bắt đầu ghi Notes, rồi dừng trước khi ghi xong sự việc đầu tiên vì bận và chưa thấy sẽ dùng ghi chú vào việc gì. |
| [P2](../evidence/interviews/P2.md) | Nhân viên gặp hành vi mang tính tình dục tại nơi làm việc. Ghi chép khoảng 22:00 ngày 27/11/2026. Bản tóm tắt ghi nhận việc P2 giữ tin nhắn, ghi chú trong Notes và một đoạn ghi âm, đồng thời từng ngồi định viết email cho HR. | Chưa xác nhận hình thức và người hỏi/ghi. Chưa rõ lần tự chuẩn bị phản ánh gần nhất. Ý kiến về công cụ là kỳ vọng của P2. |
| [P3](../evidence/interviews/P3.md) | Nhân viên kể về hành vi tại nơi làm việc. TV3 hỏi và ghi qua tin nhắn lúc 23:47 ngày 27/11/2026. Ghi chép theo 9 câu là nguồn tham chiếu cho B23 và B24. Đoạn lời kể bổ sung ghi riêng việc P3 trao đổi với quản lý và các tư liệu có sẵn. | Chưa ghi nhận số lần trong tháng hay thời gian chuẩn bị phản ánh. |

Cả ba người đã thực hiện bước chuẩn bị. Cần xác nhận cả ba ngoài nhóm để chốt ngưỡng phỏng vấn. Xem [tổng hợp bằng chứng](../evidence/summary.md) để đối chiếu với khảo sát.

## Ca chạy thử CP2 · `cp2_demo.json`

| Mục | Nội dung |
|---|---|
| Dùng để làm gì | Lệnh `demo` của CLI và test API cho ca ngày mâu thuẫn. |
| Nguồn và cách tạo | `synthetic`, viết tay một sự việc hư cấu gồm lời kể, ghi chú, kết quả OCR mẫu và bản chép lời mẫu. Không dùng seed. |
| Xử lý | Khai báo ngày theo từng nguồn. Để trống ngày khi nguồn thiếu thông tin. CLI giữ tệp gốc và gắn mã nguồn khi đọc. |
| Quy mô và kiểm tra | 1 ca, 4 đoạn nguồn rà khi soạn. Test đối chiếu hai ngày tới đúng mã và kiểm tra bản chép lời có trong đầu ra. |
| Giới hạn | Minh họa một tình huống mâu thuẫn về ngày. Không đo chất lượng OCR, chép lời hay bằng chứng về khó khăn của người dùng. |
