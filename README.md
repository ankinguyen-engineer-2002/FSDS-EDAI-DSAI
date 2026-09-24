# FSDS · EDAI · DSAI Personal Learning Hub

Repository này biến slide khóa học và sách tham khảo thành một **visual-first personal study desk** bằng tiếng Việt.

## Source nội dung beginner-first

- `content/lesson-mechanisms.json`: source of truth cho 37 scene cơ chế của Linux, Python, Database và Web API.
- `content/beginner-guides.json`: pain, living metaphor, hướng dẫn đọc, stress test và synthesis của 27 chương.
- `content/term-examples.json`: ví dụ thực tế cho toàn bộ thuật ngữ được hiển thị.
- `content/beginner-layout.css`: layout bài học đã được duyệt theo phong cách Anthropic.
- `content/beginner-renderer.js`: renderer nối prose, glossary và Archify.
- `scripts/embed_beginner_content.py`: nhúng năm source trên vào HTML duy nhất; `--check` được chạy trong validation.

## Xem online

```text
https://ankinguyen-engineer-2002.github.io/FSDS-EDAI-DSAI/
```

## Mở sản phẩm local

Chạy một static server tại thư mục repo:

```bash
python3 -m http.server 8765
```

Sau đó mở `http://127.0.0.1:8765/fsds-learning-hub.html`.

> Không nên mở trực tiếp bằng `file://` vì các Archify iframe là file tương đối và browser có thể áp chính sách origin khác nhau.

## Bốn bài hoàn chỉnh

- F01 · Linux Fundamentals
- F02 · Python Fundamentals
- F03 · Database Fundamentals / PostgreSQL
- F04 · Web API / FastAPI

Hub có:

- syllabus navigation;
- light/dark theme;
- collapsible rail;
- reading progress theo bài;
- ghi chú cá nhân autosave bằng localStorage;
- 44/44 learning visuals được dựng bằng Archify, có pan/zoom, guided focus, brand mark chuẩn và full-screen;
- bốn bài hoàn chỉnh dùng format beginner-first: việc thật → giải thích đời thường → cơ chế → thuật ngữ → ứng dụng công việc → tự kiểm;
- 27 chương hiển thị 167 thuật ngữ cốt lõi, được hỗ trợ bởi bank 237 ví dụ thực tế; từng visual có hướng dẫn đọc và câu tự kể lại riêng;
- bài đọc theo mạch vĩ mô → vi mô.

## Cấu trúc chính

```text
fsds-learning-hub.html          # application/hub chính
learning-digest/                # nguồn prose cô đọng theo bài
course-slides/                  # slide nguồn
library/                        # thư viện sách tham khảo
archify/specs/                  # 44 JSON specs — source of truth
archify/rendered/               # 44 Archify HTML đã deliver
archify/receipts/               # validation/delivery/browser receipts
docs/                           # audit, visual catalog, technical/UI standard
LEARNING-DESIGN-METHOD.md       # phương pháp học nền
```

## Tài liệu bắt buộc đọc trước khi thêm bài

1. `LEARNING-DESIGN-METHOD.md` — rule nội dung duy nhất: pain → living metaphor → mechanism/stress test → golden takeaway.
2. `docs/FSDS-LEARNING-HUB-STANDARD.md` — contract kỹ thuật cho Archify, UI và publish.
3. `docs/VISUAL-CATALOG-FIRST-3-LESSONS.md`

## Lưu ý

- `archive/fsds-learning-hub-before-study-hub.html` là snapshot trước redesign 2026-09-24.
- Archify spec là source of truth; không sửa trực tiếp file trong `archify/rendered/`.

## Publish lên GitHub Pages

```bash
./scripts/validate.sh
./scripts/publish.sh "Mô tả thay đổi"
```

Push lên `main` sẽ kích hoạt GitHub Actions và deploy Pages tự động. Nếu có sửa visual, chạy `./scripts/rebuild-archify.sh` trước. Xem `docs/PUBLISHING-WORKFLOW.md`.

## Nguồn local không publish

`library/` và `course-slides/` được giữ trên máy để tổng hợp kiến thức nhưng không commit vào repository public do dung lượng và bản quyền.
