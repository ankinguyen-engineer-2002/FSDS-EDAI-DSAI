# Publishing workflow — edit → validate → GitHub Pages

Từ ngày 2026-09-24, `main` trên GitHub là nguồn đồng bộ của Learning Hub. GitHub Pages tự deploy sau mỗi push thành công.

## Quy tắc bắt buộc

1. Mọi learning visual của F01–F03 và các bài mới đều dùng Archify.
2. JSON trong `archify/specs/` là source of truth; không sửa `archify/rendered/*.html` bằng tay.
3. Nếu sửa visual, chạy:

   ```bash
   ./scripts/rebuild-archify.sh
   ```

4. Nếu chỉ sửa prose/UI, chạy:

   ```bash
   ./scripts/validate.sh
   ```

5. Khi một đơn vị thay đổi đã hoàn thành và QA pass, publish ngay:

   ```bash
   ./scripts/publish.sh "Mô tả thay đổi"
   ```

6. Push lên `main` kích hoạt `.github/workflows/pages.yml`. Workflow chỉ deploy HTML hub và các Archify artifact; thư viện sách và slide nguồn không được đưa lên public Pages.

## Brand/icon trong Archify

- Luôn tra catalogue bằng `archify brands` trước.
- Dùng canonical mark qua trường `brand` cho product/language/framework có nhận diện rõ.
- Hiện đã dùng mark chuẩn được bundle và pin bởi Archify cho Python, PostgreSQL và FastAPI.
- Không tự lấy một icon gần giống hoặc URL không được kiểm chứng.
- Catalogue Archify hiện không có canonical Linux/Tux mark; vì vậy Linux diagrams giữ semantic icon thay vì gắn logo không được pin. Khi Archify bổ sung canonical mark hoặc có official asset URL được phê duyệt, thêm qua brand contract rồi rebuild/deliver.

## GitHub Pages artifact

Pages build tạo `_site` tạm thời gồm:

```text
index.html                         # copy của fsds-learning-hub.html
fsds-learning-hub.html
archify/rendered/*.html            # 35 standalone visual labs
.nojekyll
```

`library/`, `course-slides/`, `tmp/` không được commit/publish để tránh đưa tài liệu nguồn dung lượng lớn hoặc có bản quyền lên repository công khai.
