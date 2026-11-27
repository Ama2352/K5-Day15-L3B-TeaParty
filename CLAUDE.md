# TeaParty · Hướng dẫn cho Claude Code

@AGENTS.md

@docs/PROJECT_CONTEXT.md

@docs/TASKS.md

## Trước khi sửa

- Hỏi người dùng là **Người 1, 2 hay 3** và làm **ticket nào** trong `docs/TASKS.md`, nếu họ chưa nói.
- Chỉ sửa file của người đó (`docs/TASKS.md` mục 2). Cần đổi file của người khác thì dừng lại và báo.
- `spec.md` chỉ Người 3 sửa. Người 1 và 2 cần đổi §4 thì soạn nội dung ra chat để gửi Người 3.

## Git

- **Không bao giờ tự `git commit`, `git push`, `git merge`, tạo PR.** Chỉ in lệnh để người dùng tự chạy.
- Được chạy lệnh chỉ đọc (`status`, `diff`, `log`, `fetch`) và `pull` / `merge --ff-only` khi người dùng yêu cầu.
- Làm trên nhánh riêng (`n1-ai`, `n2-backend`, `n3-eval`), không làm thẳng trên `main`.

## Hợp đồng code

- Định dạng dữ liệu là `codebase/van_ban_xuat_xu.schema.json`: 11 trường mỗi tài liệu, `status` thuộc `provided` / `missing` / `unclear` / `conflicting`. Không tự đổi schema.
- Giữ đúng tên và tham số hàm trong `docs/TASKS.md` mục 1.2.
- Chỉ `trich_xuat` trong `agent.py` được gọi AI. Kiểm đủ trường, hỏi bổ sung, tạo bản nháp, email nháp viết bằng code thường trong `tools.py`.
- `answer(text)` trả trong **một lượt**: bản nháp + câu hỏi bổ sung. Hội thoại nhiều lượt chỉ làm trên web.
- Model: DeepSeek qua định dạng OpenAI (`MODEL_PROVIDER=openai`, đổi `URL_OPENAI`). Gọi bằng `urllib`, không cài SDK.
- Thêm thư viện thì ghi vào `requirements.txt` và nói lý do. Ưu tiên thư viện chuẩn.
- Sửa `tools.py` hoặc `web.py` thì chạy `python -m unittest discover -s codebase -p "test_*.py"` trước khi báo xong.

## Dữ liệu nhạy cảm

- Đề tài là quấy rối tình dục. **Chỉ dùng dữ liệu giả lập** khi gọi API, viết câu thử, làm demo.
- Lấy câu thử từ `evidence/interviews/` hoặc `evidence/survey/` thì phải bỏ định danh trước.
- AI của sản phẩm không kết luận pháp lý, không bịa tình tiết hay luật sư, không gửi gì ra ngoài. Code cũng không được làm những việc này.

## Không được làm

- Không bịa số eval, run ID, token, chi phí, trích dẫn phỏng vấn. Chưa có số thì để `__` hoặc ghi "chưa chạy".
- Không sửa `eval/metric_spec.yaml` và chuẩn "đạt" ở `spec.md` §7 (đã chốt CP2).
- Không sửa `expected` cho khớp output, không viết prompt khớp nguyên văn câu thử.

## Trả lời

- Trả lời bằng tiếng Việt.
- Dẫn file dạng `path:line`.
- Xong việc thì cập nhật dòng của mình trong `docs/PROJECT_CONTEXT.md` và nói đã làm gì, còn vướng gì.
