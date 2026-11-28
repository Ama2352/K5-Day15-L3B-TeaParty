# Reflection — Nguyễn Thị Khánh Linh

1. **Vai trò + phần mình làm (file / commit):**
   Mình phụ trách xây bộ câu thử benchmark và data card của nhóm TeaParty, theo [phân công](../TEAMS.md).
   Ở CP2, mình xây 10 câu thử văn bản giả lập B01–B10, gồm ca thường, ca khó và yêu cầu ngoài phạm vi; mỗi câu có đầu vào, đầu ra mong đợi và tiêu chí đạt ([benchmark](../eval/benchmark.csv), commit `2d787a3`).
   Sau khi nhóm mở rộng lên 26 câu, mình cùng Codex rà nguồn, độ phủ 11 trường và giới hạn dữ liệu; phần mở rộng B11–B26 do N3 soạn cùng Claude Code và rà trước khi commit.
   Trên nhánh `linh-benchmark-review`, mình bổ sung B27–B30 về người cung cấp tài liệu, ghi âm đã cắt/nén, các mốc ngày khác nhau và rút đồng ý dùng form; cập nhật data card, biên bản đánh giá tại commit `24ba7e6`, giữ nguyên 26 câu cũ.
   Mình đã đưa bản bổ sung vào bộ 30 câu để bàn giao lên `main`, đồng bộ data card, khai báo AI và [checklist hoàn tất](../eval/README.md#9-kiểm-tra-hoàn-tất-phần-linh--28112026); B27–B30 chưa có điểm eval, các kết quả đã công bố vẫn thuộc bộ 26 câu ([báo cáo](../eval/report.md)).

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ phải sửa output AI):**
   Mình dùng Codex để rà benchmark với spec và schema, đối chiếu nguồn phỏng vấn/khảo sát, đếm loại câu, gợi ý tình huống còn thiếu và soạn nháp tài liệu, gồm bản reflection này.
   Khi rà phần AI hỗ trợ soạn, mình phải phân biệt nguồn của dạng tình huống với chi tiết giả lập: nhãn `nguoi_dung` hoặc `data_that` không có nghĩa đầu vào là hồ sơ thật, còn OCR và chép lời mẫu chưa kiểm được việc đọc ảnh hay nghe âm thanh.
   Phần tài liệu cũng cần tách rõ 30 câu đã soạn với 26 câu đã chạy; không đưa bốn câu mới vào tỷ lệ đạt, không đổi `expected` cho khớp output và không gán phần rà của AI thành kiểm tay của người.
   Mình và một bạn đã đối chiếu 5 output lượt 1: B01/B05/B10 đạt, B16/B18 trượt, khớp 5/5; kết quả này được ghi ở nhánh riêng, chưa đủ thông tin để gọi là chấm mù và khác đợt chấm độc lập lượt 2 của nhóm.
   Bài học của mình là dùng AI để tìm chỗ cần kiểm, rồi đối chiếu lại với nguồn và kết quả lưu trong repo; một câu giải thích hợp lý vẫn cần bằng chứng trước khi đưa vào hồ sơ nộp bài.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   Mình chọn **B16**: lời kể ghi chiều thứ Hai, ảnh tin nhắn ghi thứ Ba 17/11/2026, còn bản chép lời không xác định được ngày; lượt 1 trượt vì hệ thống không nêu rõ mâu thuẫn giữa các nguồn ([phân tích lỗi](../eval/report.md)).
   Sang lượt 2, hệ thống đã xử lý được mâu thuẫn ngày nhưng vẫn trượt vì trường `nguoi_tao` ghi người dùng “tự chụp/chép” dù nguồn không nói; nhóm chấm lại và cập nhật tổng lượt 2 từ 19/26 xuống 18/26.
   Lượt 3, B16 vẫn trượt vì tự suy người chụp và thiết bị “Điện thoại”; tổng lượt 3 là 23/26 nhưng metric điền đúng trường có nguồn chỉ đạt 15/18, thấp hơn chuẩn 90% ([kết quả ba lượt](../eval/report.md)).
   Mình học được rằng chấm bản nháp phải kiểm từng trường với nguồn: sửa được mâu thuẫn ngày chưa đủ nếu thông tin về người tạo hoặc thiết bị lại bị suy đoán; điều chưa biết cần để thiếu hoặc hỏi lại.
   Mình đã bổ sung và rà tiêu chí B27 về người tạo/người cung cấp, B29 về ngày tạo ảnh/ngày sự việc; bước tiếp theo của phần đánh giá là chạy bộ mở rộng, báo riêng kết quả B01–B26 và bốn câu mới, đồng thời đối soát B24 bị thiếu trong danh sách ca áp dụng metric cũ.
