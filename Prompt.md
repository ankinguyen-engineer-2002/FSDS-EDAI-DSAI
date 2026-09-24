# Prompt chuẩn — Soạn và tích hợp bài học mới vào FSDS Learning Hub

_Cập nhật: 2026-09-24_

Thay các giá trị trong dấu `<...>` rồi giao nguyên prompt này cho Codex.

---

## Prompt

Soạn hoàn chỉnh bài **`<MÃ_BÀI> · <TÊN_BÀI>`** và tích hợp vào FSDS Learning Hub hiện tại.

### 1. Đọc repo và nguồn kiến thức

Trước khi viết, phải đọc kỹ:

- `FSDS-EDAI-DSAI-syllabus.md` để hiểu vị trí của bài trong toàn khóa học;
- slide `<ĐƯỜNG_DẪN_SLIDE>`;
- các sách liên quan trong `library/`;
- tài liệu chính thức khi cần kiểm chứng hành vi kỹ thuật;
- `LEARNING-DESIGN-METHOD.md`;
- `docs/FSDS-LEARNING-HUB-STANDARD.md`;
- `docs/PUBLISHING-WORKFLOW.md`;
- `direction-approved.md`;
- bốn bài Linux, Python, Database và Web API hiện có để giữ tính nhất quán nhưng không sao chép máy móc.

Slide dùng để xác định phạm vi. Sách dùng để đào sâu bản chất. Tài liệu chính thức dùng để kiểm chứng hành vi. Không bê nguyên nội dung nguồn vào bài và không nhồi mọi kiến thức tìm thấy.

### 2. Rule duy nhất để xây dựng nội dung

Chỉ dùng bốn core rules trong `LEARNING-DESIGN-METHOD.md`:

1. **Zero Jargon First:** hình dung quen thuộc → việc nó giải quyết → tên kỹ thuật.
2. **First Principles Anchor:** bắt đầu từ nỗi đau thực tế; nếu chưa có giải pháp thì điều gì hỏng và vì sao cách thủ công không đủ.
3. **Physical Metaphor System:** chọn một thế giới hữu hình dùng xuyên bài; quy đổi 1:1 giữa vật thể/hành động đời thường và khái niệm kỹ thuật; luôn chỉ ra giới hạn của ẩn dụ.
4. **No Academic Fluff:** bỏ mọi câu, thuật ngữ hoặc visual không giúp hiểu pain, mechanism, relationship, failure hay ứng dụng thực tế.

Toàn bài đi theo đúng bốn phần:

```text
I. Cơn đau nguyên bản
II. Bản đồ quy đổi ẩn dụ
III. Cơ chế vận hành + kịch bản thử lửa
IV. Bản chất một dòng
```

Không tạo thêm framework biên tập khác.

### 3. Yêu cầu nhận thức của bài học

Bài phải dành cho người mới hoàn toàn, học sinh lớp 12 hoặc người không chuyên. Không giả định người đọc đã hiểu jargon.

Mỗi khái niệm cốt lõi phải giúp người học trả lời được:

1. Nó là gì bằng ngôn ngữ đời thường?
2. Nó dùng để làm gì?
3. Vì sao phải có nó; nếu không có thì điều gì hỏng?
4. Cơ chế thật sự vận hành như thế nào?
5. Nó nằm ở bước nào trong hệ thống hoặc quy trình lớn hơn?
6. Ví dụ thực tế là gì?
7. Hiểu sai nó sẽ khiến người học chẩn đoán hoặc sửa nhầm ở đâu?

Nội dung phải đi từ vĩ mô tới vi mô và tạo thành một mạch nhân quả. Không biến mục lục slide thành danh sách chương rời rạc. Cuối bài, người học phải tự kể lại được toàn bộ hệ thống và hiểu các phần phối hợp với nhau ra sao.

### 4. Chắt lọc kiến thức

Khi scan slide và sách:

- xác định nỗi đau gốc;
- xác định knowledge spine của bài;
- xác định một chu trình hoàn chỉnh từ đầu tới cuối;
- xác định boundary, state, data flow, decision và failure quan trọng;
- giữ lượng kiến thức nền ít nhất nhưng đủ để hiểu đúng, kể lại được và dùng được;
- loại bỏ phần lặp, phần tra cứu, lịch sử dài, danh sách syntax và chi tiết chưa cần cho mental model;
- phân biệt rõ phần bắt buộc học với phần chỉ nên biết để tra cứu.

Tạo hoặc cập nhật hồ sơ biên tập:

```text
learning-digest/<SLUG_BÀI>.md
```

Digest phải ghi source map, coverage decisions, knowledge spine, chapter map, thuật ngữ cốt lõi, visual inventory và mental model cuối bài.

### 5. Viết source nội dung

Tạo hoặc cập nhật đúng các source of truth:

```text
content/beginner-guides.json
content/lesson-mechanisms.json
content/term-examples.json
```

Yêu cầu liên kết dữ liệu:

- lesson code phải thống nhất ở mọi file;
- chapter ID phải khớp giữa guide, mechanism và visual registry;
- tên `coreTerms` phải khớp chính xác với glossary và `term-examples.json`;
- mỗi core term phải có định nghĩa, ví dụ thực tế và mechanism step hoặc explicit purpose;
- mỗi chapter phải có câu hỏi dẫn đường, hình dung đời thường, giới hạn ẩn dụ, định nghĩa đơn giản, lý do phải biết, vị trí trong bức tranh lớn, ứng dụng công việc, flow, stress test, response, say-back và bridge sang phần tiếp theo;
- final synthesis phải có những gì đã học, quan hệ giữa các phần, ứng dụng ngoài thị trường, mini-lab, năm câu self-check và một golden takeaway.

Không sửa trực tiếp các block generated trong `fsds-learning-hub.html`.

### 6. Visual — Archify only

Mọi learning visual mới hoặc visual làm lại đều phải dùng skill Archify. Không dùng Mermaid, draw.io, Excalidraw, SVG viết tay, canvas tự vẽ hoặc card-grid giả làm diagram.

Không đặt quota visual. Chỉ tạo visual khi nó giải thích flow, relationship, state, boundary, decision hoặc failure tốt hơn prose ngắn.

Với mỗi visual, trước khi vẽ phải xác định:

- câu hỏi nhận thức visual trả lời;
- lý do prose chưa đủ;
- loại diagram phù hợp;
- main path;
- failure path nếu có;
- cách visual nối với đoạn giải thích trước và câu say-back sau.

Mọi visual phải:

- dùng `meta.quality_profile = "showcase"`;
- đọc được trực tiếp trong article rộng, không bắt người học mở tab mới;
- vẫn hiểu được khi motion tắt;
- có connector và direction mang ý nghĩa rõ;
- dùng canonical logo/icon khi công nghệ có nhận diện chuẩn;
- chỉ lấy asset ngoài từ website chính thức, lưu bản audit và pin SHA-256;
- có reading cue trước visual và câu tự kể lại riêng sau visual;
- không lặp kết luận với visual khác.

Source of truth:

```text
archify/specs/
```

Không sửa bằng tay:

```text
archify/rendered/
archify/receipts/
```

Nếu spec thuộc `scripts/generate_archify_specs.py`, phải sửa generator thay vì chỉ sửa JSON sẽ bị ghi đè khi rebuild.

### 7. Tích hợp vào HTML chính

Tích hợp bài mới vào `fsds-learning-hub.html` bằng pipeline hiện có:

- đăng ký topic và trạng thái ready;
- đăng ký ladder/mạch bài;
- nối lesson code với generic beginner renderer;
- đăng ký `archifyVisuals` theo đúng chapter ID và artifact filename;
- cập nhật số bài hoàn chỉnh, số visual và mô tả syllabus;
- cập nhật validator để không còn phụ thuộc sai vào số liệu của ba bài cũ;
- ưu tiên đưa registry/count về manifest hoặc cách tính tự động nếu đang phải hard-code ở nhiều nơi;
- giữ nguyên personal study desk, note autosave, progress, sidebar, light/dark và outer shell đã được duyệt.

Chỉ sửa `content/beginner-renderer.js` hoặc `content/beginner-layout.css` khi bài mới chứng minh hệ thống chung thật sự thiếu component hoặc có lỗi layout. Không tạo CSS riêng tùy tiện cho từng bài.

### 8. UI/UX contract

Giữ phong cách Claude/Anthropic hiện tại:

- paper, ink, teal, copper và border mảnh;
- prose dễ đọc, visual rộng hơn prose;
- sidebar mở vẫn có khoảng cách với bài viết;
- sidebar đóng phải trả chiều rộng cho article;
- không có khoảng trắng desktop vô nghĩa;
- visual phải gắn trực tiếp với nội dung đang giải thích;
- typography và hierarchy nhất quán;
- không horizontal overflow tại 1920, 1440, 1024, 768 và 390px;
- keyboard, focus ring, Escape, reduced motion và contrast phải hoạt động;
- không có JavaScript/page error.

Các yêu cầu kỹ thuật, UI/UX, Archify, responsive và publishing là contract bắt buộc riêng; chúng không phải framework viết nội dung và không được loại bỏ khi tinh gọn content rule.

### 9. Build và validation

Nếu có visual mới hoặc visual thay đổi:

```bash
./scripts/rebuild-archify.sh
```

Embed source nội dung vào HTML:

```bash
python3 scripts/embed_beginner_content.py
```

Chạy validation đầy đủ:

```bash
./scripts/validate.sh
```

Sau đó chạy static server và browser QA:

```bash
python3 -m http.server 8765
```

Kiểm tra:

- tất cả chapter render đúng;
- tất cả core term đủ năm nhóm thông tin trên UI;
- tất cả Archify iframe load được và chứa SVG hoàn chỉnh;
- visual đúng chapter và đúng nội dung prose;
- không overflow ở các breakpoint bắt buộc;
- sidebar, theme, note drawer, autosave, reading progress và full-screen visual hoạt động;
- console không có error;
- người mới có thể đọc từ đầu đến cuối và kể lại một mental model thống nhất.

### 10. Documentation và cleanup

Cập nhật khi cần:

```text
README.md
docs/FSDS-LEARNING-HUB-STANDARD.md
docs/PUBLISHING-WORKFLOW.md
docs/VISUAL-CATALOG-*.md
```

Dọn toàn bộ file tạm, screenshot thử, backup thừa, cache và artifact không còn dùng. Không xóa slide, sách nguồn hoặc lịch sử audit cần thiết.

### 11. Publish

Khi validation và browser QA đều pass:

```bash
./scripts/publish.sh "Add <MÃ_BÀI> <TÊN_BÀI> beginner-first lesson"
```

Sau khi push:

- kiểm tra GitHub Pages workflow thành công;
- mở production và kiểm tra lại bài mới;
- xác nhận không có console error;
- nếu cần, dùng query theo commit hoặc hard refresh để tránh cache;
- báo commit hash, production URL, số chapter, số core term và số Archify visual đã hoàn thành.

Không dừng ở việc sửa local. Mỗi đơn vị thay đổi hoàn chỉnh phải được validate, commit, push và kiểm tra trên GitHub Pages.

### 12. Kết quả cuối cùng phải bàn giao

Báo cáo ngắn gọn:

1. Knowledge spine cuối cùng của bài.
2. Phần đã giữ, cắt và lý do.
3. Danh sách chapter.
4. Danh sách visual và câu hỏi mỗi visual trả lời.
5. Số core terms đã audit.
6. Kết quả validation và browser QA.
7. Commit hash.
8. Production URL.
9. Bất kỳ rủi ro hoặc giới hạn còn lại nào.

Hãy chủ động hoàn thành toàn bộ quy trình. Chỉ hỏi lại khi thiếu nguồn bắt buộc hoặc có quyết định nội dung thực sự không thể suy ra từ repo.

---

## Ví dụ điền nhanh cho bài kế tiếp

```text
<MÃ_BÀI>          = F05
<TÊN_BÀI>         = Validation & Verification
<ĐƯỜNG_DẪN_SLIDE> = course-slides/05-validation-and-verification.pdf
<SLUG_BÀI>        = validation-verification-fundamentals
```
