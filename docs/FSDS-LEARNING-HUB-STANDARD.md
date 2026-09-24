# FSDS Learning Hub — authoring, visual và UI standard

Phiên bản: 1.0 · 2026-09-24

## 1. North star

Một bài học hoàn chỉnh phải giúp người học:

1. Nhìn thấy một việc thật xảy ra.
2. Biết state nằm ở đâu và ai giữ quyền xử lý.
3. Nhận ra boundary/data/control đang được đi qua.
4. Gọi đúng tên cơ chế sau khi đã thấy hành vi.
5. Dùng mental model để dự đoán một biến thể mới.
6. Biết evidence nào chứng minh kết luận.

## 2. Tỷ lệ và nhịp bài

- Mục tiêu trải nghiệm: **60% visual / 40% text**.
- Tỷ lệ này nói về tải nhận thức, không phải diện tích pixel cứng.
- Một section chuẩn:

```text
Question / observable episode
  → visual mental model
  → short explanation
  → mechanism + terminology
  → failure/variation
  → evidence / lab bridge
```

- Một màn hình/viewport chỉ nên có một kết luận chính.
- Paragraph thường 2–4 câu; prose body khoảng 60–75 ký tự mỗi dòng.
- Headline phải mang claim: “Pipe nối process bằng stream”, không chỉ “Pipe”.

## 3. Ba tầng diễn giải

1. **Dễ hiểu:** câu tiếng Việt gần gũi.
2. **Cơ chế thật:** state, boundary, protocol, ownership, cost.
3. **Trong nghề:** framework, failure, performance, operations và evidence.

Thuật ngữ lần đầu:

```text
nghĩa tiếng Việt (technical term)
```

Không dùng analogy nếu không chỉ ra nơi analogy ngừng đúng.

## 4. Quy trình biên tập nguồn

### Bước A — coverage ledger

- Đọc slide gốc để biết phạm vi môn học.
- Đọc 1–3 sách/tài liệu có thẩm quyền cho cơ chế nền.
- Tạo bảng: claim từ slide → giữ/bỏ/gộp/bổ sung → evidence/source.

### Bước B — chọn spine

Spine là một flow hoặc bộ câu hỏi xuyên suốt. Ví dụ:

- Linux: intent → shell → kernel → streams → automation.
- Python: project → runtime → objects/errors → I/O → time → framework.
- Database: logical intent → process → plan → pages → durability → evidence.

### Bước C — viết episode

Mỗi episode có:

- initial state;
- trigger/input;
- transitions;
- owner tại mỗi bước;
- happy path;
- failure path quan trọng;
- one-sentence conclusion;
- lab/evidence bridge.

### Bước D — visual inventory trước khi vẽ

Chọn visual theo câu hỏi nhận thức, không theo sở thích thẩm mỹ. Ghi rõ node, connector, state, reading order và interaction trước khi author spec.

### Bước E — viết prose quanh visual

Text không đọc lại từng box. Text giải thích:

- tại sao quan hệ đó tồn tại;
- ngộ nhận nào cần phá;
- failure/cost nào visual chưa nói hết;
- cách kiểm chứng.

## 5. Archify integration contract

### File layout

```text
archify/
  specs/       # JSON source of truth
  rendered/    # delivered standalone HTML
  receipts/    # deliver + visual-check receipts
```

### Authoring

1. Mỗi diagram tối đa khoảng 12 primary nodes; nếu dày hơn thì tách.
2. `meta.quality_profile = "showcase"`.
3. Stable IDs, wording theo domain.
4. Chỉ thêm route/via/labelAt khi validator chẩn đoán.
5. Validate sau mỗi thay đổi và trước delivery.
6. Deliver một lần khi spec đã pass; không sửa spec sau delivery mà không deliver lại.

### Embed trong hub

- Dùng `.archify-lab` và iframe relative path.
- Có title, summary, nút mở full-screen và figcaption nói cách dùng.
- Iframe lazy-load.
- Không sửa CSS bên trong artifact đã deliver chỉ để khớp hub; hai hệ thống dùng chung tinh thần editorial nhưng artifact giữ runtime của Archify.
- Visual phải còn hiểu được khi motion tắt.

## 6. UI/UX của personal study desk

### Shell

- Giữ Anthropic/Claude editorial language: paper surface, ink, teal, copper, border mảnh.
- Sidebar là syllabus/map, không phải dashboard widget wall.
- Content rộng, có breathing room và hierarchy rõ.
- Rail thu gọn phải trả lại toàn bộ chiều rộng cho content.

### Personal learning features

- Reading progress theo từng lesson.
- Ghi chú theo lesson, autosave trong `localStorage`.
- Note prompt buộc người học viết cơ chế, câu hỏi và evidence.
- Theme và rail state được nhớ.
- Visual có full-screen/open separate view.

### Accessibility

- Keyboard dùng được cho button/control.
- Escape đóng drawer/modal.
- SVG có title/desc hoặc aria-label hữu ích.
- Iframe có `title`.
- `prefers-reduced-motion` được tôn trọng.
- Không ellipsis text quan trọng.
- Contrast và focus ring phải nhìn thấy ở light/dark.

## 7. Content quality gates

Bài chỉ được gọi “hoàn chỉnh” khi:

- [ ] Có episode mở đầu, không bắt đầu bằng glossary.
- [ ] Có super map/spine.
- [ ] Có ít nhất một flow input → output.
- [ ] Có failure path.
- [ ] Có câu hỏi dự đoán.
- [ ] Thuật ngữ được giải thích bằng tiếng Việt.
- [ ] Có evidence/lab bridge.
- [ ] Có coverage ledger.
- [ ] Có synthesis mindmap.
- [ ] Không có claim vượt quá source/runtime/version boundary.

## 8. Visual quality gates

- [ ] Connector có nghĩa và đúng hướng.
- [ ] Không edge xuyên node không liên quan.
- [ ] Không label che edge/node.
- [ ] Layer/boundary mang nghĩa kỹ thuật.
- [ ] Timeline có scale thời gian nhất quán.
- [ ] State transition có start/end rõ.
- [ ] Visual không chỉ là card chứa paragraph.
- [ ] Archify showcase: 9 checks, 0 error, 0 warning.
- [ ] Browser evidence được ghi riêng với perceptual review.

## 9. UI verification matrix

Bắt buộc test:

| Viewport | Kiểm tra |
|---|---|
| 1440×900 | desktop shell, reading width, iframe, drawer |
| 1024×768 | sidebar/content balance, sticky aside |
| 768×1024 | tablet reflow, iframe height |
| 390×844 | mobile nav, no page overflow, note drawer |

Automated checks:

- JavaScript syntax.
- Browser console errors.
- `scrollWidth <= clientWidth` cho document và main content.
- Iframe URL load thành công.
- Note autosave/restore.
- Theme/rail persistence.
- Keyboard Escape.

## 10. Anti-patterns

- Chuyển bullet slide thành card grid.
- Mỗi thuật ngữ một box nhưng không có relationship.
- Dạy syntax trước khi có behavior.
- Animation không biểu diễn state/flow.
- Dùng chart với dữ liệu giả.
- Dùng “best practice” mà không nói workload/failure model.
- Nói tool name thay cho role/cơ chế.
- Nhúng visual chỉ để đẹp; prose vẫn chứa toàn bộ quan hệ.
- Copy cùng một layout cho mọi chủ đề.

## 11. Definition of done

```text
source coverage
+ coherent spine
+ concise prose
+ complete visual inventory
+ validated visual artifacts
+ integrated study UX
+ browser QA
+ updated documentation
= lesson ready
```

## 12. Archify-only visual policy

Từ 2026-09-24, mọi learning visual mới hoặc visual được làm lại phải dùng Archify. Không dùng Mermaid, draw.io, Excalidraw, SVG viết tay, canvas tự vẽ hoặc card-grid giả làm diagram. UI chrome và typography không tính là learning visual.

Quy trình:

```text
visual catalog → Archify JSON spec → showcase validation
→ deliver receipt → embed iframe → browser QA
```

Brand/product/language có canonical mark trong `archify brands` phải dùng trường `brand`. Nếu catalogue chưa có nhưng đã xác định được website chính thức, capture bằng Archify, khóa SHA-256, lưu asset audit trong repo và embed qua `brand`; không dùng logo gần giống hoặc logo không pin. Mỗi diagram chỉ gắn brand ở node thực sự đại diện cho sản phẩm/nền tảng, không rải logo trang trí.

## 13. Canvas width contract

- Desktop rail mở: article dùng gần hết phần main, chỉ giữ khoảng thở 24–32px với rail và mép phải.
- Desktop rail đóng: article tối đa 1800px; trên viewport 1920px còn khoảng 60px mỗi bên.
- Archify frame desktop cao tối đa 82vh/920px để đọc trực tiếp, không bắt buộc mở tab khác.
- Prose vẫn giới hạn khoảng 72ch; chỉ visual, flow map và section shell được mở rộng.
- Không tạo horizontal overflow tại 1920, 1440, 1024, 768 và 390px.

## 14. Publish gate

Mỗi đơn vị thay đổi hoàn chỉnh phải chạy validation, commit và push để Pages đồng bộ:

```bash
./scripts/publish.sh "Mô tả thay đổi"
```

Nếu thay visual, phải chạy `./scripts/rebuild-archify.sh` trước. Chi tiết ở `docs/PUBLISHING-WORKFLOW.md`.
