# Tóm tắt mô phỏng simulate-2@20261128-093242

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 16 | 1 | 7209 | 1607 | 1.1 | 5.1 |
| dung_vua | 27 | 2 | 13825 | 2713 | 2.0 | 10.0 |
| dung_nhieu | 7 | 4 | 28149 | 6329 | 4.1 | 20.0 |

Tỉ lệ đạt dùng để tính: 18/26 (69%) — lượt run-2@20261128-030638

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (100 người) | Chi phí / tháng — cơ sở (500 người) | Chi phí / tháng — cao (2.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| deepseek-flash (vào 0.3 · ra 1.2 $/1M) | $0.0076 | $0.0109 | $0.0056 | $0.4019 | $2.01 | $8.04 | $0.0040 |
| deepseek-v4-pro (vào 1.32 · ra 3.96 $/1M) | $0.0294 | $0.0425 | $0.0217 | $1.56 | $7.82 | $31.29 | $0.0156 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.0) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: deepseek-chat. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
