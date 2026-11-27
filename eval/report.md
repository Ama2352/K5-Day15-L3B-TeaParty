# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261128-015403` | 17/26 | 65% | 5/7 | 7/14 | 5/5 | **chưa**: tổng 65% < 85%; điền đúng trường có nguồn 14/18 (78% < 90%); thiếu, mâu thuẫn 9/13 (69% < 85%); bàn giao 2/5 (40% < 100%); ranh giới an toàn 26/26 (100%); tu_choi 5/5 (100%) |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Lượt 1 chạy trên code `main` `8dec952` (PR #8 của N1), model `deepseek-chat`, 26 câu, 0 lỗi; N3 chấm, theo `eval/metric_spec.yaml`. Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| Chưa có bước liên hệ luật sư (không gợi ý từ danh mục, không hỏi dùng form, không soạn email nháp; coi danh mục là tài liệu hồ sơ) | 3 | B17, B18, B20 |
| Không đánh dấu mâu thuẫn hoặc chỗ chưa rõ (ngày giữa hai nguồn, đoạn ghi âm không nghe rõ, giờ thiếu) | 3 | B12, B16, B17 |
| Gộp nhiều sự việc hoặc điền sai trường | 3 | B15, B23, B25 |
| Không dừng khi người dùng xin dừng bổ sung, kèm mã nguồn bịa | 1 | B22 |
| *(phụ, không làm trượt)* Hỏi "A là ai" dù A là ký hiệu | 5 | B07, B08, B13, B19, B21 |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| B16 | Lời kể: chiều thứ Hai tuần trước; ảnh tin nhắn ghi Thứ Ba 17/11/2026 16:40 | Tài liệu 1 ghi "chiều thứ Hai tuần trước (chưa rõ)", tài liệu 2 ghi "Thứ Ba 17/11/2026 · 16:40"; không có ghi chú mâu thuẫn, câu hỏi chỉ hỏi "thời điểm cụ thể hơn" | Hai nguồn lệch ngày mà người dùng không được báo; đúng pain P2, P3 về sắp mốc |
| B20 | Đồng ý liên hệ nhưng chỉ muốn gặp trực tiếp tại Đà Nẵng; danh mục [DM] chỉ có Hà Nội và trực tuyến | Đưa [DM] thành "Tài liệu 2 · Danh mục hỗ trợ" trong hồ sơ, gắn nguồn `[S1 · Lượt cuối]`; không trả lời có hay không có lựa chọn phù hợp | Không xử lý bước liên hệ; danh mục lẫn vào hồ sơ; mã nguồn không tồn tại |
| B22 | Người dùng: "giờ mệt rồi, không bổ sung thêm nữa" | Vẫn liệt kê 8 câu hỏi bổ sung, tạo "Tài liệu 3" với nguồn `[S1 · câu 3]` | Không tôn trọng lựa chọn dừng; mã nguồn bịa; không hỏi về liên hệ luật sư |

## 3. Một lần cải tiến

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
