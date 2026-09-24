# FSDS · EDAI · DSAI Personal Learning Hub

Repository này biến slide khóa học và sách tham khảo thành một **visual-first personal study desk** bằng tiếng Việt.

## Mở sản phẩm

Chạy một static server tại thư mục repo:

```bash
python3 -m http.server 8765
```

Sau đó mở `http://127.0.0.1:8765/fsds-learning-hub.html`.

> Không nên mở trực tiếp bằng `file://` vì các Archify iframe là file tương đối và browser có thể áp chính sách origin khác nhau.

## Ba bài hoàn chỉnh

- F01 · Linux Fundamentals
- F02 · Python Fundamentals
- F03 · Database Fundamentals / PostgreSQL

Hub có:

- syllabus navigation;
- light/dark theme;
- collapsible rail;
- reading progress theo bài;
- ghi chú cá nhân autosave bằng localStorage;
- 35/35 learning visuals được dựng bằng Archify, có pan/zoom, guided focus, brand mark chuẩn và full-screen;
- bài đọc theo mạch vĩ mô → vi mô.

## Cấu trúc chính

```text
fsds-learning-hub.html          # application/hub chính
learning-digest/                # nguồn prose cô đọng theo bài
course-slides/                  # slide nguồn
library/                        # thư viện sách tham khảo
archify/specs/                  # 35 JSON specs — source of truth
archify/rendered/               # 35 Archify HTML đã deliver
archify/receipts/               # validation/delivery/browser receipts
docs/                           # audit, visual catalog, authoring standard
LEARNING-DESIGN-METHOD.md       # phương pháp học nền
```

## Tài liệu bắt buộc đọc trước khi thêm bài

1. `LEARNING-DESIGN-METHOD.md`
2. `docs/FSDS-LEARNING-HUB-STANDARD.md`
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
