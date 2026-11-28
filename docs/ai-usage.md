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
| Bổ sung B27–B30 để đủ 30 câu, 28/11/2026 | Codex | Tự soạn 4 ca giả lập theo schema và luồng trong spec; nguồn `tu_viet`, không gán là phỏng vấn hoặc dữ liệu thật. Giữ nguyên B01–B26; đồng bộ data card, phạm vi metric, tiến độ và changelog. | Chưa được Linh kiểm tay và chưa có output hoặc điểm eval; số chấm khớp 5/5 trước đó chỉ thuộc mẫu của bộ 26 câu cũ. | Nguyễn Thị Khánh Linh |
| Rà benchmark và data card, 28/11/2026 | Codex | Rà 26 câu, đối chiếu nguồn P1–P3 và số đếm khảo sát, so với bản CP2 và lượt 1; ghi độ phủ 11 trường và đính chính danh sách ca áp dụng metric thiếu B24. Không sửa CSV hoặc chuẩn đạt. | Chưa có xác nhận Linh kiểm tay toàn bộ bảng nguồn; xác nhận chấm 5 output được ghi riêng ở dòng dưới. Xem `eval/README.md` mục 7 và `data/DATA_CARD.md`. | Nguyễn Thị Khánh Linh |
| Chấm lại 5 output lượt 1, 28/11/2026 | Codex | Chấm B01, B05, B10 đạt; B16, B18 trượt; sau đó đối chiếu nhãn N3 khớp 5/5. Không đọc cột chấm trước khi đưa nhãn nhưng đã có báo cáo lỗi trong ngữ cảnh, không phải đánh giá mù hoàn toàn. Không ghi đè cột `pass`, `ghi_chu`. | Linh xác nhận mình và một bạn đã chấm 5 câu, cùng kết quả trên: hai người khớp 5/5 và khớp AI 5/5. Chưa nêu tên người thứ hai hoặc xác nhận chấm mù. Chi tiết từng câu và nguồn xác nhận ở `eval/README.md` mục 7. | Nguyễn Thị Khánh Linh |
| Hoàn tất hồ sơ Linh và rà trước khi push main, 28/11/2026 | Codex | Đưa B27–B30 từ nhánh riêng vào main; giữ nguyên B01–B26, metric và kết quả cũ; đối chiếu lại bảng nguồn, đồng bộ số đếm, ghi checklist và viết reflection theo mẫu BTC. | Kiểm bằng lệnh và đối chiếu dữ liệu repo, ghi rõ phần do AI rà; không nhận là Linh đã kiểm tay toàn bộ nguồn hoặc chấm bộ 30 câu. Xem eval/README.md mục 9 và reflection/nguyen-thi-khanh-linh.md. | Nguyễn Thị Khánh Linh |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
