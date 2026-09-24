# Learning Design Method

Tài liệu này định nghĩa phương pháp học, phương pháp viết và nguyên tắc thiết kế web dùng chung cho toàn bộ repository.

Nó **không phải khuôn nội dung cố định**. Mỗi chủ đề được tự do chọn cấu trúc, loại visual, số màn hình và độ sâu phù hợp.

## North star

Người học không chỉ nhớ định nghĩa. Sau bài học, họ phải:

- Nhìn được toàn cảnh hệ thống.
- Biết mỗi phần tồn tại để giải quyết vấn đề gì.
- Biết các phần nằm ở layer nào và phụ thuộc nhau ra sao.
- Theo được một flow thực tế từ input đến output.
- Có thể zoom vào chi tiết mà không mất vị trí trên bản đồ chung.
- Dùng bản đồ để suy luận khi gặp tình huống mới.

## Trải nghiệm trước, giải thích sau

Đơn vị học đầu tiên không phải định nghĩa, command hay cú pháp. Đơn vị học đầu tiên là một **episode hoàn chỉnh có thể quan sát**: một yêu cầu đi vào hệ thống, làm state thay đổi và tạo ra kết quả hoặc lỗi.

Thứ tự mặc định:

```text
Nhìn một việc xảy ra
        ↓
Dự đoán bước hoặc state tiếp theo
        ↓
Thấy quan hệ nguyên nhân - kết quả
        ↓
Gọi tên cơ chế vừa quan sát
        ↓
Zoom vào kiến trúc và implementation
        ↓
Cuối cùng mới đọc hoặc viết notation/cú pháp
        ↓
Đổi tình huống để kiểm tra khả năng suy luận
```

Đây là **experience-first learning**. Người học tiếp nhận một hành vi có nghĩa trước, giống cách con người nghe và hiểu ngôn ngữ trong ngữ cảnh trước khi học ngữ pháp.

Không dùng “khái niệm trước” như một phiên bản khác của “cú pháp trước”. Một bài mở đầu bằng danh sách object, function, process hay database vẫn là cách tổ chức từ góc nhìn người viết, chưa phải từ trải nghiệm của người học.

### Episode là đơn vị thiết kế

Mỗi episode nên xác định:

- Tình huống thực tế và kết quả người học có thể quan sát.
- State ban đầu.
- Input hoặc trigger.
- Các transition theo thứ tự.
- Thành phần đang giữ quyền xử lý ở mỗi thời điểm.
- Data hoặc control signal đang di chuyển ở đâu.
- Happy path và ít nhất một failure path quan trọng.
- Thuật ngữ chỉ được giới thiệu sau khi visual đã tạo mental model.
- Syntax hoặc command chỉ xuất hiện sau khi người học hiểu hành vi mà nó biểu diễn.
- Một biến thể mới để người học dự đoán, không chỉ lặp lại ví dụ cũ.

Markdown mô tả episode theo semantics, không biến thành storyboard pixel:

```text
Tình huống → dự đoán → state/transition → kết quả
          → tên cơ chế → implementation → biến thể nghề nghiệp
```

HTML biến semantics đó thành flow có thể chạy, dừng, bước từng state và inspect. Nếu một cơ chế diễn tiến theo thời gian, ảnh tĩnh chỉ là trạng thái dự phòng; trải nghiệm chính phải cho thấy transition.

### Hiểu trước khi sản xuất

Trong thời đại AI có thể sinh syntax và boilerplate, giá trị cần dạy sâu hơn là:

- Code đang kích hoạt cơ chế nào.
- State nằm ở đâu và thuộc ownership của ai.
- Boundary nào đang được đi qua.
- Work đang chờ I/O hay dùng CPU.
- Failure sẽ truyền theo đường nào.
- Chi phí thời gian và memory phát sinh ở đâu.
- Framework gọi code của người học lúc nào và theo contract nào.
- Cách kiểm chứng code do người hoặc AI sinh ra.

Syntax, setup và command cơ bản có thể nằm trong inspector, appendix hoặc reference. Chúng không được chiếm mạch học chính khi AI hoặc tài liệu tra cứu có thể cung cấp ngay.

### Ba tầng diễn giải

Một cơ chế quan trọng nên có ba tầng progressive disclosure:

1. **Nói dễ hiểu:** hành vi bằng tiếng Việt gần gũi, không yêu cầu nền kỹ thuật.
2. **Cơ chế thật:** state, boundary, protocol và thuật ngữ chính xác.
3. **Dùng trong nghề:** cơ chế xuất hiện trong framework, pipeline hoặc failure/performance case nào.

Ví dụ đời thường chỉ là cầu nối. Nó phải được nối ngay với cơ chế thật và dừng lại khi phép so sánh không còn đúng.

### Nghĩa trước, thuật ngữ sau

Thuật ngữ không được dùng như thể người học đã biết nó.

- Lần xuất hiện đầu tiên phải dùng nghĩa tiếng Việt dễ hiểu trước, thuật ngữ chuẩn đặt sau trong ngoặc: `hồ sơ của một lần gọi hàm (frame)`.
- Nếu thuật ngữ không có bản dịch tự nhiên, giải thích nó bằng một câu ngắn ngay tại node hoặc inspector.
- Viết đầy đủ trước khi dùng chữ viết tắt: `giao diện giữa server và ứng dụng Python (ASGI)`.
- Tiêu đề ưu tiên hành vi quan sát được: `Lỗi đi ngược chuỗi gọi` tốt hơn `Exception propagation`.
- Nhãn visual ưu tiên vai trò: `bộ điều phối việc sẵn sàng` tốt hơn chỉ ghi `event loop`.
- Không xếp nhiều thuật ngữ chưa giải thích trong cùng một câu.
- Sau khi người học đã hiểu, inspector có thể hiện tên chuẩn tiếng Anh để họ tra tài liệu nghề nghiệp.

Mỗi màn hình phải qua bài kiểm tra đọc thành tiếng: một người chưa học chủ đề có thể kể lại “đang có việc gì xảy ra” mà không cần tra glossary.

## Thứ tự ưu tiên

Khi các tiêu chí xung đột, ưu tiên theo thứ tự:

1. **Đúng kiến thức.**
2. **Đủ kiến thức lõi.**
3. **Thấy quan hệ và flow.**
4. **Non-tech vẫn hiểu được.**
5. **Cô đọng và đúng trọng tâm.**
6. **Visual thay cho đoạn chữ khi visual giải thích tốt hơn.**
7. **Tương tác và chuyển động có ý nghĩa.**
8. **Thẩm mỹ và hiệu ứng trang trí.**

Không hy sinh kiến thức lõi chỉ để bài ngắn. Không thêm chữ chỉ để bài có vẻ đầy đủ.

## Tỷ lệ 60 visual / 40 text

Đây là tỷ lệ về **vai trò truyền đạt**, không phải tỷ lệ diện tích cứng.

Visual chịu trách nhiệm chính cho:

- Kiến trúc và layer.
- Quan hệ phụ thuộc.
- Trình tự theo thời gian.
- Luồng dữ liệu hoặc trạng thái.
- So sánh nhiều lựa chọn.
- Causal chain và failure path.
- Bản đồ tổng kết.

Text chịu trách nhiệm chính cho:

- Một kết luận trọng tâm.
- Giải thích vì sao quan hệ tồn tại.
- Điều kiện, giới hạn và ngoại lệ.
- Ngôn ngữ gần gũi nối visual với mental model.
- Chi tiết mở ra khi người học chọn một node.

Text không lặp lại nguyên xi điều visual đã thể hiện. Visual không được chỉ là nhiều box chứa text.

## Các nguyên lý học được kết hợp

- **Experience-first learning:** thấy một episode có nghĩa trước khi học tên và notation.
- **Prediction before reveal:** yêu cầu người học dự đoán state tiếp theo trước khi visual cho chạy tiếp.
- **Causal tracing:** mỗi chuyển động phải chỉ ra cái gì kích hoạt cái gì.
- **Cognitive apprenticeship:** quan sát flow hoàn chỉnh, inspect quyết định, rồi tự thay đổi tình huống.
- **Advance organizer:** cho bản đồ toàn cảnh trước để tạo “móc treo”.
- **Whole-to-part:** đi từ hệ thống hoàn chỉnh xuống từng phần.
- **Chunking:** gom kiến thức thành các khối có ý nghĩa.
- **Feynman-style explanation:** dùng tiếng Việt đơn giản, ví dụ gần gũi và tránh jargon không cần thiết.
- **Dual coding:** kết hợp hình, chữ, icon và spatial relationship.
- **Progressive disclosure:** nhãn ngắn trên sơ đồ; chi tiết mở khi click hoặc zoom.
- **Flow/sequence learning:** biểu diễn thứ thay đổi theo thời gian bằng chuyển động có hướng.
- **Spiral learning:** đào sâu rồi quay lại bản đồ tổng quan để củng cố quan hệ.
- **C4-like zoom:** context → khối lớn → thành phần → flow/implementation, nhưng không bắt mọi bài phải dùng đúng C4.

## Nguồn kiến thức và coverage

Mỗi bài có một file Markdown nội dung duy nhất.

File đó phải tổng hợp:

- Slide gốc của FSDS.
- Kiến thức nền cốt lõi từ sách đã scan.
- Tài liệu chính thức khi cần xác nhận hành vi của công cụ.
- Phần bổ sung cần thiết cho nghề và thị trường hiện tại.

Coverage không có nghĩa sao chép mọi slide. Người viết có thể:

- Gộp nhiều slide lệnh thành một command map.
- Sửa phát biểu thiếu chính xác.
- Bỏ screenshot hoặc chi tiết không tạo mental model.
- Bổ sung kiến thức nền mà deck gốc thiếu.
- Đổi hoàn toàn thứ tự để mạch học logic hơn.

File Markdown cần có coverage map chỉ rõ phần nào được giữ, gộp, sửa, bổ sung hoặc cố ý không đưa lên màn hình chính.

## Quan hệ giữa Markdown và HTML

```text
Slide FSDS + sách + tài liệu chuẩn
                 ↓
      Một file Markdown semantic
                 ↓
  Biên tập visual và interaction phù hợp
                 ↓
        Một HTML offline duy nhất
```

Markdown giữ:

- Claim và mental model.
- Quan hệ giữa các khái niệm.
- Flow và trạng thái.
- Nội dung chi tiết khi click node.
- Coverage và nguồn.

Markdown không giữ:

- Tọa độ pixel.
- Màu cụ thể của từng node.
- Layout cứng cho mọi chủ đề.
- Animation timing mang tính triển khai.

HTML giữ:

- Bố cục trực quan.
- Icon, connector và layer.
- Interaction, progressive disclosure và motion.
- Responsive behavior.
- Theme và accessibility.

HTML không được phát minh claim mới ngoài nội dung đã kiểm tra trong Markdown.

## Hệ phân cấp nội dung trên màn hình

Một màn hình có thể dùng bốn cấp, không bắt buộc dùng đủ:

1. **Kết luận:** một câu người học cần giữ lại.
2. **Visual chính:** architecture, map, flow, DAG, timeline, matrix, state machine hoặc mô hình phù hợp.
3. **Nhãn trực tiếp:** tên, vai trò hoặc trạng thái ngắn trên visual.
4. **Inspector:** định nghĩa dễ hiểu, layer hiện tại, input/output và mối nối trước/sau.

Nếu inspector dài, chia theo câu hỏi; không đổ một đoạn văn lớn vào node.

## Chọn visual theo bản chất kiến thức

Không dùng một loại sơ đồ cho mọi bài.

| Bản chất kiến thức | Visual nên cân nhắc |
|---|---|
| Layer và boundary | Architecture stack, swimlane |
| Dependency | DAG, tree, lineage graph |
| Diễn tiến theo thời gian | Sequence, timeline, animated route |
| Trạng thái và transition | State machine |
| Causal relationship | Causal graph, feedback loop |
| Phân loại hoặc trade-off | Matrix, spectrum, small multiples |
| Không gian hoặc hạ tầng | Topology, deployment map |
| Tóm tắt toàn bài | Mindmap có quan hệ chéo |

Box chỉ được dùng khi box đại diện cho một thực thể, trạng thái hoặc boundary thật.

## Chuyển động và tương tác

Motion phải trả lời một câu hỏi:

- Dữ liệu đi đâu?
- Thứ tự xảy ra thế nào?
- State nào vừa thay đổi?
- Dependency nào đang được kích hoạt?
- Layer nào đang được zoom?

Không dùng animation lặp chỉ để trang trí.

Với cơ chế có state transition, control tối thiểu nên cân nhắc:

- Chạy và tạm dừng.
- Đi từng bước tiến/lùi khi thứ tự có ý nghĩa.
- Reset về state ban đầu.
- Chọn tốc độ khi animation thay cho lời giảng theo thời gian.
- Scrub timeline khi cần so sánh hai thời điểm.

Animation nên được tạo từ trace, state machine hoặc quy tắc đã kiểm chứng. Không phát minh một chuyển động có vẻ hợp lý nhưng sai với runtime thật.

Interaction nên giúp người học:

- Chọn node để xem giải thích.
- Đổi góc nhìn trên cùng một bản đồ.
- Theo một route cụ thể.
- So sánh trạng thái trước/sau.
- Zoom từ overview xuống detail.

Nội dung cốt lõi không được chỉ tồn tại trong hover.

## Inspector cho node

Khi một node có thể click, phần giải thích bên cạnh nên trả lời:

- Nó là gì, bằng ngôn ngữ đơn giản?
- Nó nằm ở layer hoặc giai đoạn nào?
- Input đến từ đâu?
- Output đi đâu?
- Nó liên quan gì tới node trước và node sau?
- Khi nó lỗi, dấu hiệu quan sát được là gì?

Không bắt buộc hiển thị cả sáu câu cùng lúc. Chọn phần giúp hiểu visual hiện tại nhất.

## Tab tổng kết bắt buộc

Mỗi bài phải có một phần **Tóm lại cần nắm**.

Phần này dùng một **super mindmap dạng cây trái → phải** để:

- Đặt chủ đề ở root bên trái.
- Đánh số nhánh lớn `1, 2, 3...` theo thứ tự cần follow.
- Đánh số nhánh con `1.1, 1.2...` để thấy hierarchy.
- Gom leaf keyword bên trong đúng nhánh cha.
- Hiện quan hệ chéo hoặc flow chính khi chúng giúp hiểu bài.
- Cho phép click nhánh để đọc kết luận cô đọng.

Mindmap không phải danh sách box tỏa tròn. Connector, numbering và spatial hierarchy phải mang nghĩa.

Để tránh quá tải, trạng thái mặc định chỉ hiển thị các nhánh lớn. Mỗi lần chỉ mở chi tiết một nhánh; đóng nhánh để quay lại overview. Đây là progressive disclosure, không phải che bớt kiến thức.

Nhánh đang đóng không được giữ placeholder hoặc vùng rỗng giả cho các node con. Canvas phải reflow theo nội dung thật; người học luôn thấy overview gọn trước, rồi chủ động mở đúng phần cần ôn.

## Web template: phần ổn định và phần tự do

Phần ổn định:

- Một HTML offline, không phụ thuộc CDN.
- Anthropic Sans cho toàn bộ chữ.
- Syllabus navigation và trạng thái khóa/mở.
- Sidebar và chapter navigation có thể thu gọn để nhường diện tích cho canvas.
- Dark/light theme.
- Keyboard, focus và semantic controls.
- Fullscreen cho visual chính.
- Responsive từ mobile đến desktop rộng.
- Inspector và mindmap tổng kết.

Phần được tự do sáng tạo:

- Số chương và số màn hình.
- Tên chương.
- Loại visual.
- Cấu trúc navigation bên trong chủ đề.
- Mức tương tác và animation.
- Mật độ kiến thức.
- Cách kể chuyện.
- Mức đào sâu kỹ thuật.

Chủ đề nặng có thể cần nhiều tầng, simulator hoặc nhiều flow. Chủ đề nhỏ có thể chỉ cần vài màn hình. Template cung cấp khả năng, không áp đặt nhịp kể.

## Typography và icon

- Dùng bản Anthropic Sans đã bổ sung đầy đủ glyph tiếng Việt và nhúng trực tiếp vào HTML, kể cả code label.
- Không xem `font-family` computed là bằng chứng font hỗ trợ tiếng Việt: phải kiểm tra cmap để chắc chắn mọi ký tự Latin trong bài có glyph thật, không rơi sang fallback hoặc ghép dấu lỗi.
- Chỉ dùng hai static face weight 400/500 và tắt font synthesis để tránh sai khác giữa các browser.
- Chuỗi tiếng Việt được chuẩn hóa Unicode NFC trước khi render.
- Tiêu đề tiếng Việt cần line-height tối thiểu khoảng `1.15` và một khoảng đệm dọc nhỏ; không crop line box chứa dấu kép.
- Chữ phải đọc được ở kích thước thật, không dựa vào zoom trình duyệt.
- Text trong node được wrap; không cắt mất thuật ngữ quan trọng.
- Icon dùng để nhận diện loại thực thể, không dùng như trang trí.
- Một icon phải giữ cùng ý nghĩa trong toàn bài.
- Màu luôn đi cùng label hoặc icon; không dùng màu làm tín hiệu duy nhất.

## Responsive

Responsive không có nghĩa thu nhỏ toàn bộ slide.

- Desktop rộng có thể dùng map nhiều cột và inspector bên cạnh.
- Desktop hẹp phải đổi grid hoặc tăng chiều cao slide.
- Mobile phải chuyển map sang tree/stack, đưa inspector xuống dưới.
- Khi thu gọn sidebar, cột navigation phải về chiều rộng thực `0`; canvas phải nhận lại phần diện tích đó, không chỉ ẩn bằng opacity hoặc transform.
- Khi thu gọn chapter bar, chỉ tab hiện tại còn hiển thị và vẫn mở lại được bằng một control rõ ràng.
- Không để text, connector, control hoặc node chồng lên nhau.
- Không ẩn kiến thức lõi chỉ vì viewport nhỏ.

Các breakpoint tối thiểu cần kiểm tra: 390, 1024, 1366, 1440 và 1920 px.

## Canvas cho architecture và infra lớn

Khung bài học không ép mọi visual vào tỷ lệ 16:9.

- Chiều cao canvas được quyết định bởi nội dung.
- 16:9 chỉ dùng khi visual thực sự phù hợp với một slide trình chiếu.
- Architecture, infrastructure topology, lineage và mindmap được phép mở rộng tự nhiên.
- Fullscreen phải cho phép cuộn hoặc pan/zoom khi sơ đồ lớn hơn viewport.
- Mobile có thể đổi layout nhưng không được bỏ node hoặc quan hệ lõi.

Sơ đồ lớn phải đạt chất lượng gần công cụ chuyên dụng như draw.io:

- Connector gắn đúng node/port.
- Hướng, nhánh và junction nhìn rõ ở cả light/dark theme.
- Layer, boundary và grouping có ý nghĩa kiến trúc.
- Node giữ vị trí ổn định khi tương tác.
- Label không đè connector hoặc node khác.
- Có numbering, legend hoặc reading order khi graph phức tạp.
- Có inspector, zoom, pan hoặc minimap khi mật độ node yêu cầu.

Có thể dùng SVG, Canvas, React Flow hoặc engine khác trong quá trình authoring. Bản giao cuối vẫn phải bundle thành một HTML offline nếu yêu cầu portability không thay đổi.

## Quality gates

### Nội dung

- Bài bắt đầu bằng episode có kết quả quan sát được, không bắt đầu bằng glossary hoặc syntax.
- Người học thấy hành vi trước khi gặp tên cơ chế.
- Mỗi thuật ngữ mới gắn với state hoặc quan hệ đã xuất hiện trên visual.
- Syntax chính chỉ xuất hiện sau khi mental model đã được thiết lập.
- Có ít nhất một điểm dừng để dự đoán state tiếp theo.
- Có architecture/mental map đủ để định vị toàn bài.
- Đủ kiến thức lõi từ deck và sách.
- Có ít nhất một flow thật từ input đến output.
- Mỗi màn hình có đúng một kết luận chính.
- Thuật ngữ kỹ thuật được giải thích bằng tiếng Việt gần gũi.
- Chi tiết không tách khỏi mối quan hệ hệ thống.
- Coverage map được cập nhật.
- Có super mindmap tổng kết.

### Visual

- Cơ chế diễn tiến theo thời gian có state machine hoặc trace player, không chỉ có ảnh tĩnh.
- Animation có state bắt đầu, transition và state kết thúc kiểm chứng được.
- Visual truyền tải phần lớn quan hệ; text không lặp visual.
- Connector có nghĩa và đúng hướng.
- Node nằm đúng layer.
- Icon mang nghĩa ổn định.
- Không dùng box chỉ để chứa đoạn văn.
- Click node cập nhật phần giải thích liên quan.
- Motion mô tả flow hoặc state.

### UI/UX

- Không overlap ở các viewport bắt buộc.
- Không horizontal overflow toàn trang.
- Không text quan trọng bị ellipsis.
- Mọi chữ dùng Anthropic Sans.
- Tiêu đề tiếng Việt không bị cắt, va hoặc lệch dấu ở display size.
- Font preflight phải xác nhận các nhóm `ă â ê ô ơ ư`, năm thanh điệu và các tổ hợp dấu kép đều có glyph ở cả weight 400/500.
- Sidebar thu gọn có chiều rộng bằng 0 và phần nội dung chính tăng chiều rộng tương ứng.
- Mindmap mặc định không render child node hoặc placeholder; mỗi lần chỉ có tối đa một nhánh chi tiết được mở.
- Control dùng được bằng bàn phím.
- `prefers-reduced-motion` được tôn trọng.
- Không có JavaScript page error.

## Anti-patterns

- Bắt đầu bằng định nghĩa, glossary, syntax hoặc setup trước khi có tình huống cần chúng.
- Đổi syntax-first thành một danh sách concept-first nhưng vẫn không cho thấy hành vi thực tế.
- Cho code chạy trước khi người học biết cần quan sát state nào.
- Dùng phép so sánh đời thường mà không chỉ rõ chỗ phép so sánh ngừng đúng.
- Animation “minh họa” không bám trace hoặc state machine của cơ chế thật.
- Chuyển bullet từ slide cũ thành nhiều card.
- Một slide cho mỗi command hoặc định nghĩa nhỏ.
- Diagram nhiều box nhưng không có connector có nghĩa.
- Animation chạy nhưng không biểu diễn state hoặc flow.
- Text quá ít khiến visual chỉ còn nhãn.
- Text quá nhiều khiến visual trở thành trang trí.
- Dùng cùng layout cho mọi chủ đề.
- Giữ thứ tự slide gốc dù mạch kiến thức không logic.
- Rút gọn đến mức mất kiến thức nền.
- Đào sâu kỹ thuật mà không quay lại bức tranh tổng quát.

## Nguyên tắc sáng tạo

Method này là bộ tiêu chí ra quyết định, không phải dây chuyền sản xuất slide.

Mỗi bài được quyền phá bố cục cũ nếu cách mới:

- Làm mental model chính xác hơn.
- Thể hiện quan hệ rõ hơn.
- Giảm tải nhận thức.
- Giúp non-tech theo được flow.
- Cho phép đào sâu kỹ thuật mà không mất toàn cảnh.

Đổi mới được khuyến khích. Rập khuôn thì không.
