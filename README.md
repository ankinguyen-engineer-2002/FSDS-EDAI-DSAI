# FSDS · EDAI · DSAI — Personal Study Hub

Kho lưu trữ cá nhân tối giản cho chương trình **Full-Stack Data Science · Enterprise Data & AI**, gồm 3 thành phần cốt lõi:

1. **`fsds-learning-hub.html`** — Sản phẩm học tập chính (Minimalist Anthropic Editorial UI). Nội dung do người học trực tiếp biên soạn và nạp nguyên văn theo từng **Chặng**, đi kèm 2 hệ thống sơ đồ chuẩn:
   - **Mermaid ↔ Excalidraw**: Render trực tiếp bằng Mermaid v11 trên trang và hỗ trợ chuyển đổi 1-click sang `.excalidraw` thông qua `@excalidraw/mermaid-to-excalidraw` hoặc dán trực tiếp vào Excalidraw Web.
   - **ASCII / Unicode Box-Drawing Chuẩn Cột**: Được dựng và kiểm chứng tự động bằng `scripts/ascii_diagram.py` (chuẩn hóa `NFC` tiếng Việt, căn lề và kiểm tra tọa độ từng cột `┌ ┐ │ └ ┘` 100%).
2. **`course-slides/` & `FSDS-EDAI-DSAI-syllabus.md`** — 12 bộ slide PDF chính hãng của khóa học và lộ trình 25 chủ đề từ Engineering Foundation đến Distributed Platform & Cloud.
3. **`library/`** — Thư viện 179 sách và tài liệu kỹ thuật chính hãng phân theo 10 chuyên đề (`01-computer-science` → `10-blockchain`).

---

## Cấu trúc thư mục

```text
FSDS-EDAI-DSAI/
├── fsds-learning-hub.html          # Ứng dụng học tập chính (mở trực tiếp hoặc qua GitHub Pages)
├── FSDS-EDAI-DSAI-syllabus.md      # Đề cương 25 chủ đề khóa học
├── content/
│   └── lessons-data.json           # Dữ liệu bài học & sơ đồ Mermaid + ASCII đã kiểm chứng
├── scripts/
│   ├── ascii_diagram.py            # Engine dựng & kiểm chứng sơ đồ ASCII thẳng cột 100%
│   ├── build_hub.py                # Build content + sơ đồ vào fsds-learning-hub.html
│   ├── validate.py                 # Kiểm tra cú pháp JS, sơ đồ ASCII & Mermaid
│   └── publish.sh                  # Build, validate và đẩy lên GitHub Pages
├── course-slides/                  # [Local - gitignored] 12 bộ slide PDF gốc (01..12)
└── library/                        # [Local - gitignored] 179 tài liệu/sách tham khảo chính hãng
```

---

## Các bài học đã nạp trên Hub

- **D02 · Data Engineering — Storage Layer (`course-slides/08-storage-layer.pdf`)**:
  - **Chặng 1 / 7 (Hoàn thành 100%)**: *Nguyên liệu gốc & Cơ chế vật lý (Raw Ingredients & Physical Mechanics)* — 5 Trạm kiến thức (`Cache Hierarchy`, `RAM & Spill-to-Disk`, `Random Seek vs. Sequential Scan & Cloud Object Storage`, `Data Temperature Hot/Warm/Cold`, `OLTP vs. OLAP`) kèm 5 cặp sơ đồ **Mermaid ↔ Excalidraw** & **Verified ASCII**.
  - **Chặng 2 → 7**: Đã dựng sẵn thanh tiến trình chờ nạp nội dung tiếp theo.
- **I. Engineering Foundation (`F01` → `F06`)**:
  - `F01` · Linux Fundamentals
  - `F02` · Python Fundamentals
  - `F03` · Database Fundamentals (PostgreSQL)
  - `F04` · Web API (FastAPI)
  - `F05` · Validation & Verification
  - `F06` · Containerization & Orchestration (Docker)

---

## Cách sử dụng & Cập nhật bài học mới

### 1. Xem trực tiếp trên máy (Local)
Vì `fsds-learning-hub.html` đã loại bỏ toàn bộ iframe ngoài nên có thể mở trực tiếp hoặc chạy qua local server:

```bash
python3 -m http.server 8765
# Mở: http://127.0.0.1:8765/fsds-learning-hub.html
```

### 2. Build & Kiểm chứng sơ đồ ASCII / Mermaid
```bash
python3 scripts/build_hub.py
python3 scripts/validate.py
```
