# TeaParty — AI Evidence Assistant

Nhóm TeaParty, lớp L3B. Xem [thành viên và phân công](TEAMS.md) và [Canvas CP1](canvas.md).

Lát cắt CP1 giúp nhân viên chuyển lời kể và bằng chứng về một sự việc quấy rối tình dục tại nơi làm việc thành bản nháp báo cáo có cấu trúc. Bản nháp đánh dấu thông tin còn thiếu và gắn nguồn đối chiếu từ văn bản, hình ảnh hoặc âm thanh để nhân viên tự rà trước khi chia sẻ.

---

## Nhóm làm gì, khung làm gì

| Nhóm quyết định và viết | Khung làm sẵn (không cần sửa) |
|---|---|
| Người dùng, pain, bằng chứng, impact (`evidence/`, `spec.md` §1–§2) | — |
| Hình dạng giải pháp, công cụ, prompt, luồng (`spec.md` §4, `codebase/agent.py`, `tools.py`, `ai.py`) | Ghi mọi lần gọi model / công cụ vào trace, cộng token (`codebase/tracing.py`) |
| Bộ câu thử, metric, chuẩn "đạt" (`eval/benchmark.csv`, `eval/metric_spec.yaml`, `spec.md` §7) | Kiểm đủ cột, đủ câu `kho` / `tu_choi`, đủ ≥1/3 câu từ người dùng / data thật (`run.py check`) |
| Chấm cột `pass` theo metric spec | Chạy cả bộ một lệnh, có run ID, model, token từng câu (`run.py eval`) · tính % đạt (`run.py score`) |
| Persona, số người dùng thật, giá model (`cost/personas.yaml`) | Sinh ~50 phiên, chạy thật qua bản chạy thử, tính chi phí / phiên, / task thành công, / tháng 3 kịch bản (`run.py simulate`) |

*Ví dụ track A (ví dụ cỡ, không phải lời giải):* nhóm viết công cụ `search_lesson` tra bài pre-class đã đánh mã đoạn, luồng "tra đoạn → model trả lời kèm mã đoạn, không có thì nói không có", metric "mọi khẳng định có mã đoạn đúng", persona "ôn dồn trước kiểm tra". Khung chạy 25 câu thử ra `run-1.csv`, nhóm chấm `pass`, `score` in % đạt; `simulate` chạy 50 phiên ra chi phí / task thành công cho hai model.

## Chạy trong 3 phút

Bộ khung cần **Python 3.10 trở lên** (Python 3.9 có sẵn trên macOS vẫn chạy được, chỉ in một dòng nhắc). **Không cần `pip install`.**

**Bước 1 — Mở cửa sổ lệnh ngay trong thư mục repo**

| Windows (PowerShell) | macOS |
|---|---|
| Mở thư mục repo bằng File Explorer → bấm vào thanh địa chỉ → gõ `powershell` → Enter | Mở **Terminal** (Cmd + Space, gõ "Terminal") → gõ `cd ` (có dấu cách) → kéo thả thư mục repo vào → Enter |

Gõ `dir` (Windows) hoặc `ls` (macOS / Linux): thấy `run.py` và `README.md` là đang đứng đúng chỗ.

**Bước 2 — Kiểm Python và chạy thử**

| Việc | Windows (PowerShell) | macOS / Linux |
|---|---|---|
| Kiểm Python | `python --version` (không được thì `py --version`) | `python3 --version` |
| Chạy bản chạy thử (chế độ giả, chưa gọi model) | `python run.py` | `python3 run.py` |
| Kiểm bộ câu thử | `python run.py check` | `python3 run.py check` |
| Tạo file `.env` để nối model | `copy .env.example .env` | `cp .env.example .env` |

- Windows: gõ `python` mà mở Microsoft Store hoặc báo không có lệnh → dùng `py`. Chưa có Python: cài từ python.org, **tick "Add python.exe to PATH"**, mở lại PowerShell.
- macOS: báo `command not found: python` là bình thường → dùng `python3`.
- Gõ `demo` trong `python run.py` để mở ca [giả lập CP2](data/cp2_demo.json). Bản nháp dẫn mã từng nguồn và ghi ngày **cần xác nhận** vì lời kể và ảnh cho hai ngày khác nhau. Dòng trace hiện `model: fake`. OCR, bản chép lời và ngày gắn với từng nguồn được chuẩn bị sẵn trong JSON.
- Có thể nhập lời kể thuần hoặc JSON một dòng cùng định dạng với ca mẫu. JSON cần `statement`, có thể kèm `incident_date` và danh sách `sources`. Mỗi nguồn có `kind` (`text`, `image`, `audio`), `text` và có thể kèm `locator`, `incident_date` dạng YYYY-MM-DD. Bản giả dùng các ngày khai báo trong trường này. Nối model thật: [docs/connect-model.md](docs/connect-model.md).

Trong README này lệnh viết là `python …`; máy nhóm cần `python3` hay `py` thì gõ thay.

## Lệnh

| Lệnh | Làm gì |
|---|---|
| `python run.py` | Chạy bản chạy thử (gõ đầu vào, nhận kết quả, kèm số lần gọi model / token) |
| `python run.py check` | Kiểm `eval/benchmark.csv` (6 cột, số câu, `kho` / `tu_choi`, mã `source`, ô trống, dòng mẫu) `eval/metric_spec.yaml` (≥3 metric điền đủ) và `TEAMS.md` (đúng format để BTC quét). Chỉ cảnh báo, không sửa file |
| `python run.py eval --try` | **Thử nối model:** chạy 3 câu đầu (`--try 5` = 5 câu) → `eval/run-try.csv`. Thấy "Nối model được" là xong. Không tính là một lượt |
| `python run.py eval` | Chạy cả bộ qua `codebase/agent.py` → `eval/run-1.csv` (lần sau `run-2.csv`…) + `traces/run-1.jsonl`. Mỗi dòng có run ID, model, số lần gọi model / công cụ, token. Model còn giả → chỉ ghi `run-mock.csv`; mọi câu lỗi → `run-error.csv`; Ctrl+C → `run-stopped.csv` — đều **không** được đánh số |
| `python run.py eval --fake` | Thử riêng bộ chạy, không gọi agent → `eval/run-fake.csv` |
| `python run.py score eval/run-1.csv` | Sau khi điền cột `pass` (1 / 0): in % đạt tổng và theo `type`. Còn ô trống → "CHƯA CHẤM XONG", không in % |
| `python run.py simulate --try` | Thử mô phỏng chi phí 10 phiên (làm trước CP3) → `cost/simulate-try.csv` |
| `python run.py simulate` | Mô phỏng chi phí khi dùng thật theo `cost/personas.yaml` (≥50 phiên) → `cost/simulate-N.csv` + `cost/simulate-N-summary.md` |
| `python run.py simulate --rate-from eval/run-2.csv` | Như trên, lấy tỉ lệ đạt từ đúng lượt chỉ định. Không ghi thì khung lấy lượt `run-N` mới nhất đã chấm, cùng model, và ghi rõ đã lấy lượt nào trong bản tóm tắt |

Gói miễn phí báo hết lượt: thêm `--wait 4` sau `eval` hoặc `simulate` (nghỉ 4 giây giữa hai lượt gọi). Sửa CSV bằng Excel: *File → Save As → CSV UTF-8*; Google Sheets: *Tệp → Tải xuống → CSV*.

**Lượt có lỗi kỹ thuật** (cột `error` có chữ): không sửa tay file đó, chạy lại thành lượt mới và ghi vào bảng các lượt ở `eval/README.md`. Không xoá file lượt nào.

Nhóm dùng stack khác (Node, Streamlit, notebook…): sửa hàm `run_app()` trong `run.py` để `python run.py` vẫn chạy được bản chạy thử, và giữ `answer()` trong `codebase/agent.py` để `eval`, `simulate` chạy được.

## Demo web và Railway

[Video demo CP3 · 30 giây](https://drive.google.com/file/d/1rgCkuIVCnbE0lrzgJ7RvHadm4EXtcM4Y/view?usp=sharing)

[Video demo dự phòng CP4](https://drive.google.com/file/d/1lHnv9jdP6VQplZPHeHuXnvyDGJ12u7fL/view?usp=sharing)

Chạy từ thư mục gốc repo với Python 3.13.

```sh
python -m pip install -r requirements.txt
python -m uvicorn --app-dir codebase web:app --host 127.0.0.1 --port 8000
```

Mở `http://127.0.0.1:8000/docs` để thử `POST /ask` với `{"text":"..."}`. Endpoint `GET /health` kiểm tra tiến trình web và không gọi model. Khi chạy local, web mặc định dùng chế độ mô phỏng nếu chưa đặt `MODEL_PROVIDER`. Đặt `MODEL_PROVIDER=fake` để chọn chế độ này rõ ràng. Cấu hình gọi DeepSeek nằm bên dưới.

Mở `http://127.0.0.1:8000/` và chọn **Dùng ca mẫu** để thử giao diện. FastAPI phục vụ bundle React có sẵn trong repo. Khi sửa [mã nguồn phần rà soát](codebase/draft.jsx), cập nhật bundle bằng hai lệnh sau từ thư mục gốc. Trên Windows PowerShell, có thể dùng `npm.cmd` thay cho `npm`.

```sh
npm --prefix codebase ci
npm --prefix codebase run build
```

GitHub Actions kiểm tra các thay đổi liên quan đến runtime, dữ liệu, bộ thử và pipeline trên PR vào `main` hoặc khi push lên `main`. Trình kiểm tra bài nộp in cảnh báo trong log. Smoke test CLI và test API dùng `MODEL_PROVIDER=fake`.

Service `teaparty-demo` lấy code từ GitHub `main`, dùng thư mục gốc repo làm **Root Directory**. [railpack.json](railpack.json) khai báo lệnh chạy Uvicorn trên `$PORT` để Railpack lập kế hoạch build. [railway.toml](railway.toml) chọn builder, các đường dẫn kích hoạt deploy và health check `/health`. Cấu hình tạo project và liên kết nguồn nằm trong [.railway/railway.ts](.railway/railway.ts).

Khi đưa demo lên Railway, bật **Wait for CI** và tạo domain trong **Public Networking**. Đặt `MODEL_PROVIDER=fake` cho demo mô phỏng. Để dùng DeepSeek, đặt `MODEL_PROVIDER=openai`, `MODEL_NAME=deepseek-flash` và `API_KEY` trong **Variables** của service. Mở `/` để dùng giao diện và `/health` để kiểm tra tiến trình.

## Bản chạy thử — viết ở đâu

| File | Viết gì | Bước guide |
|---|---|---|
| `codebase/agent.py` | `answer(text)` — luồng chính, đúng hình dạng ở `spec.md` §4. Khung có sẵn một workflow 2 bước *ví dụ* | 3.2 |
| `codebase/tools.py` | Công cụ của bài toán, mỗi công cụ một hàm có `@tool` | 2.2, 3.2 |
| `codebase/ai.py` | `call_model(system, user)` — chỗ duy nhất gọi model. Chưa điền `.env` thì chạy **chế độ giả** | 3.3 |

- **Trước CP2:** để chế độ giả, công cụ trả dữ liệu giả — `python run.py` đi hết luồng là đủ.
- **Trước CP3:** nối model thật theo [docs/connect-model.md](docs/connect-model.md), `eval --try` thấy token > 0 rồi mới `eval`.
- Bộ chạy gửi **nguyên ô `input`** của câu thử vào `answer(text)`. Dữ liệu nền (bài học, thông báo, lịch…) để trong `data/`, đọc qua công cụ.

## Phần nào thật, phần nào giả

| Thành phần | Thật / Giả | Ghi chú |
|---|---|---|
| Lời gọi model | **Thật khi cấu hình DeepSeek** | Web gọi model để trích xuất và xử lý câu trả lời bổ sung. Luồng CLI/eval còn gọi model để đọc ý định bàn giao. Ba lượt eval đã chạy bằng DeepSeek `deepseek-chat` trên 26 ca giả lập mỗi lượt. Xem [hồ sơ đánh giá](eval/README.md). |
| Chế độ mô phỏng local | **Giả lập** | Với `MODEL_PROVIDER=fake`, CLI và web dùng kết quả mô phỏng và không gọi API model. |
| Đầu vào demo và benchmark | **Giả lập** | Ứng dụng nhận chữ. Nội dung từ ảnh và ghi âm được cung cấp dưới dạng chữ trích mẫu và bản chép lời mẫu. |
| Rà bản nháp và tải JSON | **Chạy được** | Người dùng xem nguồn, sửa và xác nhận từng trường trên web rồi tải bản nháp. |
| Gợi ý luật sư và email | **Danh mục giả lập, email nháp** | Ứng dụng soạn email nháp từ các trường người dùng đã xác nhận và chọn chia sẻ. Việc gửi email diễn ra ngoài ứng dụng. |

## Dùng AI vào việc gì

Nhóm dùng Claude Code để hỗ trợ viết code, soạn prompt, viết test và chấm nháp eval. Sang dùng Codex để rà tích hợp và chuyển logic hỏi bổ sung dùng chung cho CLI và web, rồi sửa và kiểm bằng ca hồi quy.
Quỳnh Anh duyệt lại cả 26 câu mỗi lượt. Quyên chấm độc lập 5 đầu ra lượt 2, khớp 4/5 trước khi nhóm thống nhất chấm lại B16. Chỉ dữ liệu giả lập được gửi lên API. Xem [khai báo chi tiết](docs/ai-usage.md) và [hướng dẫn cho coding agent](AGENTS.md).

## File mẫu — điền ở bước nào

| File | Điền ở bước guide | Mốc |
|---|---|---|
| `TEAMS.md` | 1.0 | CP1 · **đúng format**, BTC quét khi chấm |
| `canvas.md` | 1.4 | CP1, cập nhật CP2 |
| `evidence/hypothesis.md` | 1.1 | trước khi tìm bằng chứng |
| `evidence/data-mining.md` · `evidence/interviews/TEMPLATE.md` → `P1.md`… · `evidence/survey/TEMPLATE.md` | 1.2 | bắt đầu sau Zoom, xong CP3 |
| `evidence/summary.md` | 1.2 | CP3 |
| `spec.md` | §0–§2: 1.1–1.3 · §3–§5: 2.1–2.3 · §7: 2.4 · §8: 4.2 · §10: suốt | §7 chốt CP2 · §0–§7 CP3 · đủ CP4 |
| `data/DATA_CARD.md` | 2.4 | bản đầu CP2 |
| `eval/benchmark.csv` · `eval/metric_spec.yaml` | 2.4 | ≥10 câu + metric chốt CP2 · 20–30 câu CP3 |
| `codebase/` | 3.2, 3.3 | khung CP2 · AI thật CP3 |
| `eval/report.md` · `eval/README.md` | 4.1 (README mục 1–4 từ 2.4) | CP4 |
| `cost/personas.yaml` · `cost/cost-estimate.md` | 4.2 | thử 10 phiên CP3 · đủ CP4 |
| `validation/log.md` *(bonus)* | 4.3 | CP4 |
| `slides/outline.md` → `demo-slides.pdf` | 5.1 | CP4 |
| `reflection/TEMPLATE.md` → `reflection/<ten>.md` | 5.3 | 23:59 Thứ Bảy 28/11 |
| `AGENTS.md` · `docs/ai-usage.md` | khi dùng coding agent / AI | suốt |

## Bảy hạng mục bắt buộc — nằm ở file nào

| # | Hạng mục | File |
|---|---|---|
| 1 | Bằng chứng pain | `evidence/` (tổng hợp ở `evidence/summary.md`) |
| 2 | Impact có số | `spec.md` §2 |
| 3 | Thiết kế giải pháp | `spec.md` §4 |
| 4 | Bản chạy thử làm trọn lát cắt | `codebase/` · lệnh ở mục "Lệnh" |
| 5 | Định nghĩa "tốt" + bộ câu thử | `data/DATA_CARD.md` · `eval/` |
| 6 | Mô phỏng chi phí khi dùng thật | `cost/` |
| 7 | Slide + demo + video dự phòng | `demo-slides.pdf` ở thư mục gốc · [video demo dự phòng CP4](#demo-web-và-railway) |
| + | *Bonus:* người dùng thử | `validation/log.md` |
