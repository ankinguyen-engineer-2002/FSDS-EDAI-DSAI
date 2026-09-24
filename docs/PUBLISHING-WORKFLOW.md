# Publishing workflow — edit → validate → GitHub Pages

Từ ngày 2026-09-24, `main` trên GitHub là nguồn đồng bộ của Learning Hub. GitHub Pages tự deploy sau mỗi push thành công.

## Production URL

```text
https://ankinguyen-engineer-2002.github.io/FSDS-EDAI-DSAI/
```

## Quy tắc bắt buộc

1. Mọi learning visual của F01–F03 và các bài mới đều dùng Archify.
2. JSON trong `archify/specs/` là source of truth; không sửa `archify/rendered/*.html` bằng tay.
3. Nếu sửa visual, chạy:

   ```bash
   ./scripts/rebuild-archify.sh
   ```

4. Nếu sửa prose/layout beginner-first, sửa `content/lesson-mechanisms.json`, `content/beginner-guides.json`, `content/term-examples.json`, renderer hoặc CSS trong `content/`, rồi chạy:

   ```bash
   python3 scripts/embed_beginner_content.py
   ./scripts/validate.sh
   ```

   Không sửa trực tiếp block generated trong `fsds-learning-hub.html`. Nếu chỉ sửa UI ngoài block generated, vẫn phải chạy `./scripts/validate.sh`.

5. Khi một đơn vị thay đổi đã hoàn thành và QA pass, publish ngay:

   ```bash
   ./scripts/publish.sh "Mô tả thay đổi"
   ```

6. Push lên `main` kích hoạt `.github/workflows/pages.yml`. Workflow chỉ deploy HTML hub và các Archify artifact; thư viện sách và slide nguồn không được đưa lên public Pages.

## Brand/icon trong Archify

- Luôn tra catalogue bằng `archify brands` trước.
- Dùng canonical mark qua trường `brand` cho product/language/framework có nhận diện rõ.
- Python, PostgreSQL và FastAPI dùng canonical mark được bundle/pin bởi Archify.
- Linux/Tux dùng icon từ website chính thức `kernel.org`, được Archify capture và khóa bằng SHA-256; bản audit được lưu tại `archify/brand-assets/linux-kernel-org.png`.
- Không tự lấy icon gần giống hoặc URL không được kiểm chứng. Với brand chưa có trong catalogue, chỉ capture website chính thức, pin digest, lưu bản audit và rebuild/deliver.

## GitHub Pages artifact

Pages build tạo `_site` tạm thời gồm:

```text
index.html                         # copy của fsds-learning-hub.html
fsds-learning-hub.html
archify/rendered/*.html            # 35 standalone visual labs
.nojekyll
```

`library/`, `course-slides/`, `tmp/` không được commit/publish để tránh đưa tài liệu nguồn dung lượng lớn hoặc có bản quyền lên repository công khai.
