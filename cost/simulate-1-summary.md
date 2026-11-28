# Tóm tắt mô phỏng simulate-1@20261128-032943

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 16 | 1 | 6701 | 1362 | 1.0 | 1.0 |
| dung_vua | 27 | 2 | 13426 | 2699 | 2.0 | 2.0 |
| dung_nhieu | 7 | 4 | 27838 | 6338 | 4.1 | 4.0 |

Tỉ lệ đạt dùng để tính: 19/26 (73%) — lượt run-2@20261128-030638

- Tự chọn: lượt run-N mới nhất đã chấm xong, chạy bằng đúng model đang đo (run-2.csv). Muốn dùng lượt khác (vd lượt 2): thêm `--rate-from eval/run-2.csv`.

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (100 người) | Chi phí / tháng — cơ sở (500 người) | Chi phí / tháng — cao (2.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| deepseek-flash (vào 0.3 · ra 1.2 $/1M) | $0.0073 | $0.0100 | $0.0051 | $0.3953 | $1.98 | $7.91 | $0.0040 |
| deepseek-v4-pro (vào 1.32 · ra 3.96 $/1M) | $0.0286 | $0.0391 | $0.0199 | $1.54 | $7.69 | $30.75 | $0.0154 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (2.0) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: deepseek-chat. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
