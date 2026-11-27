# Tiến độ chung · TeaParty

Đọc trang này khi bắt đầu một phiên làm việc. Cập nhật đúng dòng phụ trách khi trạng thái, người phụ trách, quyết định hoặc điểm vướng thay đổi. Đưa cập nhật lên repo cùng công việc liên quan để mọi thành viên thấy được sau khi đồng bộ.

## Mốc hiện tại · CP2

- AI Evidence Assistant, Track F. Scope mới dùng lời kể, văn bản, hình ảnh và âm thanh để điền form 11 trường, hỏi bổ sung và giữ nguồn đối chiếu. Khi người dùng dừng bổ sung, họ vẫn có thể rà form, chọn có liên hệ luật sư được đề xuất hay không và có dùng form để soạn email nháp hay không.
- Nhóm đã có Canvas CP1 và thẻ đề Track F trong repo. Trạng thái nộp form CP1 chưa được xác nhận tại đây.
- **Việc cần chốt cùng nhau:** duyệt một ca giả lập chung và đầu ra mong đợi. Đề xuất: lời kể ghi thứ Hai, ảnh ghi thứ Ba, âm thanh không xác định được ngày. Bản nháp dẫn về từng nguồn và để ngày ở trạng thái cần xác nhận. CP2 có thể dùng kết quả OCR và bản chép lời mẫu nếu ghi rõ trong spec.
- Demo và benchmark dùng dữ liệu giả lập. Các nhận định về người dùng, nguồn cần kiểm tra và số đo được giữ trong tài liệu tương ứng.

## Phân công và trạng thái

Vai trò dưới đây là đề xuất CP2. Điền tên khi cả nhóm chốt.

| Vai trò | Người phụ trách | Trạng thái | Đầu ra và bước tiếp theo |
|---|---|---|---|
| Dev | Chưa chốt | Có luồng giả lập để nhóm rà | Chạy `python run.py` rồi nhập `demo`. [Ca mẫu](../data/cp2_demo.json) và sơ đồ ở [spec §4](../spec.md). Bước tiếp theo là BA và hai DS rà cấu trúc bản nháp và dùng ca này làm cơ sở viết câu thử. Có [schema đầu ra văn bản xuất xứ](../codebase/van_ban_xuat_xu.schema.json) bản nháp, chưa nối vào code. |
| Người 1 — Lõi AI | Nguyễn Thảo Quyên | T0–T1-7 xong; bản sửa chốt code sau T1-6 (mục 1–7) chờ n1-tester | `codebase/agent.py`: `trich_xuat` gọi DeepSeek `deepseek-chat` (chế độ JSON), thử lại đúng 1 lần khi JSON hỏng, sai schema, source_id sai, quote không khớp hoặc trường nội dung thiếu trích dẫn; `trich_xuat_day_du` trả thêm danh sách "Cần rà" cho web; `dien_lai` chỉ đổi trường được trả lời và kiểm value có được câu trả lời hỗ trợ. Số đo (`eval --try`, model thật): lượt tester trước bản cải tiến 9/10 schema (trượt B07); lượt N1 tự chạy 28/11 01:42 (10 câu): 10/10 schema, 0/10 thử lại; lượt N1 tự chạy sau bản sửa này (26 câu): 26/26 không lỗi định dạng, 2/26 thử lại (B23 JSON hỏng, B26 quote), TB 7262 vào / 1647 ra. Lượt 1 của N3: 17/26 đạt. Bước tiếp: N2 chuyển 4 hàm tạm sang `tools.py`, nối `dien_lai`/`trich_xuat_day_du` vào web, sửa `tools.py:48` (lời kể mở đầu bằng "[" bị đọc như JSON); nhóm duyệt khoá gaps mở rộng. |
| BA | Chưa chốt | Cần cập nhật | Cập nhật [Canvas](../canvas.md), phần thay đổi so với CP1 và tiến độ thu [bằng chứng](../evidence/summary.md). Cùng Dev thống nhất cấu trúc đầu ra. |
| Data Science 1 | Chưa chốt | Có bản đầu 10 câu thử văn bản giả lập | [Benchmark](../eval/benchmark.csv) có 3 ca thường, 5 ca khó và 2 ca tấn công, tất cả nguồn `tu_viet`; thay đổi được đưa vào `main` theo yêu cầu. `python run.py check` đọc đủ cột, loại ca và 4 metric; còn thiếu ≥1/3 ca nguồn thật và 20–30 câu cho CP3. Bước tiếp theo: cùng Dev và DS 2 rà theo form 11 trường, bổ sung ca ảnh/âm thanh và bước liên hệ luật sư theo scope mới, rồi cập nhật [data card](../data/DATA_CARD.md). |
| Data Science 2 | Chưa chốt | Đã điền 4 metric và chuẩn đạt | Xem [metric](../eval/metric_spec.yaml), [spec §7](../spec.md) và [cách chấm](../eval/README.md). Hai người còn cần chấm độc lập 5 output để đối chiếu. |

## Cách bàn giao

1. Trước khi sửa, đọc dòng công việc và mở file được dẫn. Kiểm tra nhánh hiện tại đã có các cập nhật liên quan.
2. Khi nhận việc hoặc dừng một phiên, cập nhật hàng tương ứng bằng trạng thái thực tế. Mỗi cập nhật đủ năm ý: **người phụ trách · đã làm gì · file/PR để đối chiếu · còn vướng gì · bước tiếp theo**. Ghi kết quả kiểm tra nếu đã chạy.
3. Ghi quyết định vào Canvas, spec hoặc file đánh giá phù hợp, rồi dẫn link từ trang này. Nếu trạng thái ở đây lệch với file gốc, kiểm tra file gốc và sửa lại trạng thái. Chỉ giữ bàn giao và điểm vướng còn hiệu lực.
4. CP2 chốt chuẩn đạt tại `spec.md` §7 trước hạn. Khi agent tiếp tục sau CP2, đọc chuẩn đã commit trước khi sửa benchmark hoặc chạy đánh giá.
