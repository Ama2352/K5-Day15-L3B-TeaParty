# Reflection — Vũ Ngọc Quỳnh Anh

## 1. Vai trò và phần mình làm

- Mình là Người 3 của TeaParty, phụ trách bằng chứng người dùng, đánh giá bản chạy thử và mô phỏng chi phí. Mình phỏng vấn P1–P3, hỏi lại về lần gần nhất họ chuẩn bị phản ánh và tổng hợp 7 trích dẫn nguyên văn đã bỏ thông tin nhận diện. [Tổng hợp bằng chứng](../evidence/summary.md)
- Mình mở rộng bộ thử từ 10 lên 26 câu cho ba lượt eval. Trong bộ 26 câu có 16 câu lấy dạng tình huống từ phỏng vấn hoặc khảo sát, với chi tiết sự việc được viết lại thành dữ liệu giả lập. [Benchmark](../eval/benchmark.csv) · [Data card](../data/DATA_CARD.md)
- Mình chấm và tổng hợp ba lượt eval, lần lượt là 17/26, 18/26 và 23/26. Tổng điểm lượt 3 vượt ngưỡng 85%, còn phần điền đúng trường có nguồn đạt 15/18, dưới ngưỡng 90%. [Báo cáo eval](../eval/report.md)
- Mình mô phỏng chi phí cho 50 phiên và đưa số liệu đánh giá, chi phí vào slide CP4 để nhóm trình bày kết quả và phần còn phải sửa. [Ước tính chi phí](../cost/cost-estimate.md) · [Slide CP4](../demo-slides.pdf)

## 2. AI hỗ trợ mình thế nào

- Mình dùng Claude Code để nháp câu hỏi phỏng vấn, câu thử B11–B26 và nhận xét chấm theo tiêu chí đã chốt. [Khai báo dùng AI](../docs/ai-usage.md)
- Khi rà câu thử, mình sửa B15 và B26, đối chiếu từng câu với nguồn và kiểm tra phần viết lại vẫn giữ được tình huống cần thử. Với phỏng vấn, mình tự hỏi, ghi chép và chép nguyên văn lời người tham gia. [Data card](../data/DATA_CARD.md) · [Tổng hợp bằng chứng](../evidence/summary.md)
- Mình đọc lại cả 26 câu ở mỗi lượt trước khi chốt cột `pass`. Khi rút số lên báo cáo và slide, mình đối chiếu với CSV và kết quả lệnh `score`. [Cách chấm](../eval/README.md) · [Kết quả lượt 3](../eval/run-3.csv)

## 3. Một câu thử trượt và điều mình học được

- Ở B16, lời kể ghi thứ Hai còn ảnh tin nhắn mẫu ghi thứ Ba. Lượt 2 đã đánh dấu được mâu thuẫn ngày nên ban đầu mình chấm câu này qua. [Báo cáo eval](../eval/report.md)
- Khi chấm độc lập, Quyên phát hiện trường `nguoi_tao` ghi người dùng tự chụp hoặc chép tài liệu dù nguồn chưa xác nhận. Nhóm chấm lại B16 thành trượt, đưa kết quả lượt 2 từ 19/26 về 18/26. [Phiếu chấm độc lập](../eval/phieu-cham-doc-lap.md) · [Kết quả lượt 2](../eval/run-2.csv)
- Mình học được rằng khi chấm một bản nháp có dẫn nguồn, mình phải đọc lại đoạn được dẫn và kiểm từng giá trị đã điền. Nếu nguồn chỉ cho thấy ảnh tồn tại mà chưa xác nhận ai tạo, trường người tạo cần để chưa rõ để người dùng rà. [Tiêu chí đánh giá](../eval/metric_spec.yaml)
