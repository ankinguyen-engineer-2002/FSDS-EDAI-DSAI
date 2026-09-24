# FSDS Learning Hub — technical, visual và UI standard

Phiên bản: 1.1 · 2026-09-24

Phần thiết kế nội dung chỉ dùng một nguồn duy nhất: `LEARNING-DESIGN-METHOD.md`. Tài liệu này không tạo thêm framework viết bài; nó chỉ giữ các contract kỹ thuật để hub, Archify và GitHub Pages hoạt động ổn định.

## 1. Archify-only visual policy

Mọi learning visual mới hoặc visual được làm lại phải dùng Archify. Không dùng Mermaid, draw.io, Excalidraw, SVG viết tay, canvas tự vẽ hoặc card-grid giả làm diagram. UI chrome và typography không tính là learning visual.

Visual chỉ được giữ khi nó giải thích flow, quan hệ, state, boundary hoặc failure tốt hơn prose ngắn. Không dựng visual để đạt quota.

Workflow:

```text
câu hỏi visual cần trả lời
→ Archify JSON spec
→ showcase validation
→ deliver HTML
→ embed vào bài
```

Source of truth:

```text
archify/specs/       # JSON specs
archify/rendered/    # standalone HTML đã deliver
archify/receipts/    # validation và delivery receipts
```

Không sửa trực tiếp `archify/rendered/*.html`. Nếu spec thay đổi, rebuild và deliver lại.

## 2. Archify authoring và brand

- `meta.quality_profile = "showcase"`.
- Node, connector và direction phải mang nghĩa rõ.
- Visual phải hiểu được khi motion tắt.
- Dùng canonical brand mark khi công nghệ có logo rõ ràng.
- Tra brand catalogue trước; nếu phải dùng asset ngoài, chỉ lấy từ website chính thức và pin SHA-256.
- Python, PostgreSQL và FastAPI dùng mark do Archify bundle/pin.
- Linux/Tux dùng asset chính thức đã audit tại `archify/brand-assets/linux-kernel-org.png`.

## 3. Embed contract

- Dùng `.archify-lab` và iframe bằng relative path.
- Có title, summary, hướng dẫn đọc, câu tự nói lại và nút mở full-screen.
- Iframe lazy-load và có thuộc tính `title`.
- Không sửa CSS bên trong artifact chỉ để ép nó giống hub.
- Visual chính phải đọc trực tiếp được trong bài, không bắt buộc mở tab mới.

## 4. Personal study desk UI

- Giữ phong cách Claude/Anthropic: paper, ink, teal, copper, border mảnh.
- Sidebar là syllabus/map, có thể thu gọn và phải trả lại chiều rộng cho content.
- Desktop rail mở: bài viết dùng gần hết main, chừa 24–32px với rail và mép phải.
- Desktop rail đóng: article tối đa 1800px; viewport 1920px còn khoảng 60px mỗi bên.
- Prose khoảng 70–76 ký tự mỗi dòng; visual và section shell được mở rộng hơn.
- Archify frame desktop cao tối đa 82vh/920px.
- Hỗ trợ light/dark theme, reading progress và note drawer autosave bằng `localStorage`.

## 5. Accessibility và responsive

- Không horizontal overflow tại 1920, 1440, 1024, 768 và 390px.
- Không cắt hoặc ellipsis nội dung quan trọng.
- Button/control dùng được bằng bàn phím; Escape đóng drawer/modal.
- Focus ring và contrast phải nhìn thấy ở light/dark.
- Tôn trọng `prefers-reduced-motion`.
- Iframe/SVG có title hoặc nhãn truy cập phù hợp.
- Không có JavaScript page error.

## 6. Validation và publish

Sau khi sửa prose/layout:

```bash
python3 scripts/embed_beginner_content.py
./scripts/validate.sh
```

Sau khi sửa Archify spec:

```bash
./scripts/rebuild-archify.sh
./scripts/validate.sh
```

Khi QA pass:

```bash
./scripts/publish.sh "Mô tả thay đổi"
```

Push lên `main` phải kích hoạt GitHub Pages. Chi tiết ở `docs/PUBLISHING-WORKFLOW.md`.
