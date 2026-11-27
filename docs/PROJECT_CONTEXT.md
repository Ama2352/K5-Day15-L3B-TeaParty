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
| Người 1 — Lõi AI | Nguyễn Thảo Quyên | T0–T1-7 xong. Eval lượt 1 chạy trên `63afb38` (17/26). T1-6 (`f552139`) nhắm nhóm lỗi "không đánh dấu mâu thuẫn / chưa rõ" (B12, B16, B17) — chờ N3 chạy lượt 2 | `codebase/agent.py`: `trich_xuat` gọi DeepSeek `deepseek-chat` (chế độ JSON), 1 lần + thử lại ≤ 1 khi JSON hỏng, sai schema, mã nguồn sai, trích dẫn không khớp hoặc trường nội dung thiếu trích dẫn; vẫn sai thì trường thành "chưa rõ" + mục "Cần rà". `trich_xuat_day_du` trả thêm danh sách cần rà cho web. `dien_lai` chỉ đổi trường được trả lời. Từ chối fail-safe; câu hỏi ≤ 8. T1-6: luật 3b/3c/3d/4b + chốt code `_ep_mau_thuan_thu`, `_ep_unclear_khi_khong_ro`. Số đo T1-6 (28/11 ~02:30, chạy thẳng `answer()` trên 26 câu benchmark `main`, KHÔNG phải lượt có số): 0 lỗi định dạng, 1/26 thử lại, từ chối đúng 6 câu tu_choi, TB 6980 vào / 1596 ra. Bước tiếp: N3 chạy lượt 2 (`python run.py eval`) trên bản có T1-6; N2 chuyển 4 hàm tạm sang `tools.py`, web dùng `trich_xuat_day_du`, sửa `tools.py:48` (lời kể bắt đầu bằng "[LK1]" bị đọc như JSON); nhóm duyệt thêm `value`/`conflict_note`/`quote` vào gaps. |
| BA | Chưa chốt | Cần cập nhật | Cập nhật [Canvas](../canvas.md), phần thay đổi so với CP1 và tiến độ thu [bằng chứng](../evidence/summary.md). Cùng Dev thống nhất cấu trúc đầu ra. |
| Data Science 1 | Chưa chốt | Có bản đầu 10 câu thử văn bản giả lập | [Benchmark](../eval/benchmark.csv) có 3 ca thường, 5 ca khó và 2 ca tấn công, tất cả nguồn `tu_viet`; thay đổi được đưa vào `main` theo yêu cầu. `python run.py check` đọc đủ cột, loại ca và 4 metric; còn thiếu ≥1/3 ca nguồn thật và 20–30 câu cho CP3. Bước tiếp theo: cùng Dev và DS 2 rà theo form 11 trường, bổ sung ca ảnh/âm thanh và bước liên hệ luật sư theo scope mới, rồi cập nhật [data card](../data/DATA_CARD.md). |
| Data Science 2 | Chưa chốt | Đã điền 4 metric và chuẩn đạt | Xem [metric](../eval/metric_spec.yaml), [spec §7](../spec.md) và [cách chấm](../eval/README.md). Hai người còn cần chấm độc lập 5 output để đối chiếu. |

## Cách bàn giao

1. Trước khi sửa, đọc dòng công việc và mở file được dẫn. Kiểm tra nhánh hiện tại đã có các cập nhật liên quan.
2. Khi nhận việc hoặc dừng một phiên, cập nhật hàng tương ứng bằng trạng thái thực tế. Mỗi cập nhật đủ năm ý: **người phụ trách · đã làm gì · file/PR để đối chiếu · còn vướng gì · bước tiếp theo**. Ghi kết quả kiểm tra nếu đã chạy.
3. Ghi quyết định vào Canvas, spec hoặc file đánh giá phù hợp, rồi dẫn link từ trang này. Nếu trạng thái ở đây lệch với file gốc, kiểm tra file gốc và sửa lại trạng thái. Chỉ giữ bàn giao và điểm vướng còn hiệu lực.
4. CP2 chốt chuẩn đạt tại `spec.md` §7 trước hạn. Khi agent tiếp tục sau CP2, đọc chuẩn đã commit trước khi sửa benchmark hoặc chạy đánh giá.
