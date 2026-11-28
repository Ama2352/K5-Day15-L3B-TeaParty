# Reflection — Nguyễn Thảo Quyên

> Làm ở guide bước 5.3. Mỗi người một file: chép file này thành `reflection/<ten-khong-dau>.md` (viết thường, không dấu). Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.

1. **Vai trò + phần mình làm:** Nguyễn Thảo Quyên, phụ trách lõi AI.
   - **Chuẩn bị trước khi dựng:**
     - Cập nhật canvas (`c8053b0`) và điền spec §0–§7 (`c4b0e65`).
     - Chia kế hoạch 3 người theo ticket và sơ đồ §4 (`docs/TASKS.md`, `871cb85`).
     - Viết `CLAUDE.md` cùng hai agent `n1-builder`, `n1-tester` (`80c749d`).
     - Tạo bản nháp mẫu theo schema để nhóm làm song song (T0, `data/mau_ban_nhap.json`, `11f2853`).
   - **CP3:**
     - Nối DeepSeek `deepseek-chat` qua định dạng OpenAI, bật chế độ JSON (`codebase/ai.py`, `f2c8ec8`).
     - Viết prompt và `trich_xuat`: bản nháp theo schema 11 trường, thử lại 1 lần khi JSON, schema hoặc trích dẫn sai, bắt buộc trích dẫn nguyên văn cho trường nội dung (`63afb38`, `d31b219`, `0f654bc`).
     - Viết `answer`, `dien_lai` và `trich_xuat_day_du` cho web.
     - Điền model và mục dùng AI trong README (`4c1cb02`).
   - **CP4:**
     - Sửa prompt theo các câu trượt ở lượt 1, gồm mâu thuẫn ngày gián tiếp và đoạn "không nghe rõ" (T1-6, `f552139`, `f9cc0d6`). Người chấm thứ hai cho lượt 2 (`8e0bec0`).
     - Tách trích xuất thành nhiều lời gọi song song theo từng đoạn nguồn, ghép bằng code. Thêm bước bàn giao: dừng bổ sung, gợi ý danh mục giả lập, email nháp (PR #27, `fd99197`). Thêm thử lại khi lỗi mạng tạm thời (`8e498c1`).
     - Kết quả: lượt 1 17/26 → lượt 2 18/26 (sau khi chấm lại B16) → lượt 3 23/26. Latency trung bình 4,56 s → 3,71 s (`eval/run-3.csv`).

2. **AI hỗ trợ mình thế nào:** Dùng Claude Code với hai agent riêng. `n1-builder` sửa code của Thảo Quyên (`ai.py`, `agent.py`); `n1-tester` chỉ đọc và chạy test, eval thử. Phải sửa lại output AI ở các chỗ:
   - Bộ lọc từ chối theo từ khoá làm rơi 10/12 yêu cầu vi phạm thật, phải đổi sang cách giữ lại mọi mục (fail-safe).
   - Code âm thầm xoá trích dẫn sai, che mất chi tiết bịa; phải đổi thành báo lỗi và thử lại.
   - Luật chốt cứng ở phía code bắt quá rộng ("lần thứ hai" bị đọc thành thứ Hai).
   - Tự đọc và chấm lại, không để AI tự điền cột `pass`.

3. **Một câu thử trượt và điều học được:** B16. Lời kể ghi thứ Hai, còn ảnh tin nhắn gửi ngay sau sự việc ghi thứ Ba 17/11. Lượt 1, AI chọn một ngày thay vì đánh dấu mâu thuẫn. Điều học được: quy tắc "không tự chọn" trong prompt chưa đủ, mâu thuẫn gián tiếp cần một bước kiểm ở phía code. Nhưng bước kiểm đó phải hẹp, vì bản đầu bắt nhầm và xoá mất giá trị đúng ở câu khác.
