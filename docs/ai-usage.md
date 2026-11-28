# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | | | | |
| Prompt / thiết kế lời gọi mô hình | | | | |
| Đào data (viết script đếm, gợi ý nhãn) | | | Kiểm tay __ dòng, khớp __ | |
| Rà câu hỏi phỏng vấn / khảo sát | Claude Code | Soạn nháp khung câu hỏi phỏng vấn và câu hỏi hỏi lại về mốc 1 tháng qua (lần gần nhất, thời gian, số lần); rà câu dẫn dắt | N3 chọn câu, tự hỏi và ghi P1–P3 qua điện thoại, tin nhắn; trích dẫn chép nguyên văn từ câu trả lời, AI không tạo câu trả lời hay trích dẫn | Vũ Ngọc Quỳnh Anh |
| Viết câu thử (benchmark) | Claude Code | Soạn nháp B11–B26 theo dạng tình huống từ P1–P3 và khảo sát, mọi chi tiết sự việc là giả lập; soạn phiếu chấm độc lập 5 output | Mỗi câu thử có `source`; N3 rà B11–B26 trước khi commit, sửa B15, B26; ghi "soạn cùng Claude Code" ở `data/DATA_CARD.md`; không sửa `expected` cũ | Vũ Ngọc Quỳnh Anh |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM (nếu có) | Claude Code | Chấm nháp cả 3 lượt (`run-1`, `run-2`, `run-3`, mỗi lượt 26 câu) theo `pass_criterion` và `eval/metric_spec.yaml`, ghi lý do ở `ghi_chu`; lượt 3 giữ cách chấm lượt 2 | N3 tự duyệt lại cả 26/26 câu mỗi lượt và quyết định cột `pass` trước khi commit. Người thứ hai (Nguyễn Thảo Quyên) chấm độc lập 5 output lượt 2, khớp 4/5; B16 chấm lại theo nhóm | Vũ Ngọc Quỳnh Anh |
| Slide, văn bản | Claude Code | Soạn nháp `spec.md` §4, §7–§10, `eval/report.md`, `eval/README.md`, `cost/cost-estimate.md`, `evidence/summary.md`, `data/DATA_CARD.md`; đối chiếu spec §4 với code; tính bảng độ trễ từ `run-1`–`run-3`; soạn nội dung slide trang 5–6 | N3 đối chiếu số với file kết quả (`run-N.csv`, `simulate-N-summary.md`, `python run.py score`) trước khi commit; số do khung sinh ra không sửa tay, số tính tay ghi rõ | Vũ Ngọc Quỳnh Anh |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
