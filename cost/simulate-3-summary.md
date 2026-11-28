# Tóm tắt mô phỏng simulate-3@20261128-103013

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 16 | 1 | 12146 | 1226 | 2.5 | 6.0 |
| dung_vua | 27 | 2 | 26044 | 2535 | 5.2 | 12.4 |
| dung_nhieu | 7 | 4 | 51908 | 5273 | 10.4 | 24.6 |

Tỉ lệ đạt dùng để tính: 18/26 (69%) — lượt run-2@20261128-030638

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (100 người) | Chi phí / tháng — cơ sở (500 người) | Chi phí / tháng — cao (2.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| deepseek-flash (vào 0.3 · ra 1.2 $/1M) | $0.0106 | $0.0153 | $0.0078 | $0.5603 | $2.80 | $11.21 | $0.0056 |
| deepseek-v4-pro (vào 1.32 · ra 3.96 $/1M) | $0.0432 | $0.0624 | $0.0318 | $2.29 | $11.45 | $45.79 | $0.0229 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.0) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: deepseek-chat. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
