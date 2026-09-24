# Audit nội dung — F01 Linux, F02 Python, F03 Database

Ngày audit: 2026-09-24
Rule đánh giá duy nhất: `LEARNING-DESIGN-METHOD.md`

## 1. Kết luận thẳng

Bản beginner rewrite đầu tiên **đúng cấu trúc nhưng chưa thật sự dễ học**. Nó đã thêm tình huống, glossary và visual guide, nhưng vẫn còn bốn lỗi:

1. Phần “cơ chế thật” còn nén nhiều jargon vào một đoạn.
2. Ẩn dụ đổi thế giới giữa các chương, làm mental model bị đứt.
3. 179 thuật ngữ được đưa lên giao diện như một mục tiêu coverage, trái với tinh thần cắt phần thừa.
4. Nhiều visual dùng chung một câu tự kiểm cấp chương, chưa buộc người học kể lại đúng sơ đồ vừa xem.

Vòng sửa hiện tại đã xây lại cả ba bài theo đúng bốn rule:

- pain trước solution;
- hình dung hữu hình trước tên kỹ thuật;
- một physical metaphor xuyên suốt mỗi bài;
- cơ chế có failure/stress test;
- chỉ giữ glossary cốt lõi;
- visual và prose có nhiệm vụ riêng nhưng nối trực tiếp với nhau;
- cuối bài có golden takeaway một dòng.

## 2. Audit theo bốn core rules

| Rule | Trước vòng sửa này | Sau vòng sửa này |
| :--- | :--- | :--- |
| Zero Jargon First | Hero tốt hơn nhưng heading, primer và mechanism vẫn mở bằng term tiếng Anh. | Heading dùng câu hỏi đời thường; card đầu tiên là physical metaphor; tên kỹ thuật xuất hiện sau; mechanism prose được viết lại câu ngắn và plain-first. |
| First Principles Anchor | Có scenario nhưng Linux chưa cho thấy rõ hậu quả của thao tác thủ công. | Cả ba bài mở bằng một sự cố có hậu quả: báo cáo đêm sai, “máy tôi chạy được”, oversell + mất điện. |
| Physical Metaphor System | Metaphor nhảy giữa công ty, nhà hát, tàu điện, bác sĩ và bếp. | Linux chỉ dùng căn bếp; Python chỉ dùng xưởng; Database chỉ dùng nhà hàng + sổ kho. |
| No Academic Fluff | Cơ chế nhồi chi tiết như coreutils/glibc, nhiều index family, free-threaded version note; 179 term card trên màn hình. | 27 scene được viết lại quanh cơ chế nền; chi tiết tra cứu rời khỏi mạch chính; giao diện chỉ hiện 107 core term card, còn bank 182 ví dụ giữ làm nguồn dự phòng. |

## 3. Những thay đổi có tác động lớn

### Mạch bài

Mỗi bài hiện đi đúng bốn phần:

```text
I. Cơn đau nguyên bản
→ II. Bản đồ quy đổi ẩn dụ
→ III. Cơ chế vận hành + thử lửa
→ IV. Bản chất một dòng
```

Mỗi section chi tiết vẫn trả lời các câu người mới cần: nó là gì, vì sao phải biết, nằm ở đâu, dùng ở đâu và hỏng thì sao; đây là nội dung bên trong phần III, không phải một framework viết bài thứ hai.

### Prose

- Viết lại toàn bộ **27 scene** của 19 chương.
- Bỏ các đoạn liệt kê thuật ngữ liên tục.
- Câu đầu mỗi chương là một vấn đề đời thường, không phải tên implementation.
- Thuật ngữ chuẩn được giữ để người học đi làm có thể tra cứu, nhưng xuất hiện sau hình dung và vai trò.
- Database modeling đã được bổ sung flow 5 bước; trước đó section này không có mechanism steps hay glossary.

### Glossary

- Không còn hiển thị mọi từ từng xuất hiện trong nguồn.
- Chỉ giữ **107 core term card**: Linux 27, Python 37, Database 43; mỗi card có cơ chế/tác dụng cụ thể thay vì câu fallback chung.
- `content/term-examples.json` giữ **182 practical examples** để term card luôn có ví dụ cụ thể và để bài sau có thể dùng lại.
- Recap không mở thêm glossary; nhiệm vụ của recap là nối kiến thức, không tạo thêm danh sách từ.

### Visual ↔ text

- 35 Archify visual được giữ sau audit vì mỗi visual trả lời một câu hỏi cơ chế khác nhau; không có visual mới được thêm để đạt quota.
- Trước cụm visual có câu hỏi và reading order.
- Sau **từng** visual, người học phải kể lại đúng title + route của visual đó rồi mới trả lời câu hỏi cấp chương.
- Prose không đọc lại toàn bộ box; prose giải thích “vì sao”, failure và bằng chứng.

## 4. Đánh giá từng bài

### F01 — Linux Fundamentals

**Cơn đau:** thao tác log mỗi đêm dễ sót, báo cáo sai nhưng không ai biết.
**Ẩn dụ xuyên suốt:** căn bếp nhà hàng.
**Spine:** ý định → người đọc lệnh → ca làm → quản lý tài nguyên → băng chuyền → làm lại/hẹn giờ.
**Golden takeaway:** Linux biến yêu cầu thành các công việc nhỏ có người làm, có quyền, có tài nguyên và có dấu vết.

Đã sửa:

- bỏ việc mở đầu bằng `argv`, `glibc`, `fork/exec` và file descriptor;
- giải thích terminal/shell/process/kernel bằng vai trò trong bếp trước;
- tách CPU, RAM và I/O thành ba kiểu triệu chứng;
- giải thích pipe/script bằng cửa nhận, cửa giao và chuông lỗi;
- tách rõ Make quyết định **làm lại gì**, cron quyết định **gọi lúc nào**.

**Đánh giá:** đạt beginner-first. Người học vẫn cần mini-lab để biến mental model thành kỹ năng command thực tế.

### F02 — Python Fundamentals

**Cơn đau:** cùng code nhưng hai máy cho hai kết quả; dữ liệu đổi ngoài ý muốn; chương trình lúc nhanh lúc đứng.
**Ẩn dụ xuyên suốt:** xưởng sản xuất.
**Spine:** hồ sơ dụng cụ → ca làm → vật liệu/state → cửa giao nhận → chia thời gian → request web.
**Golden takeaway:** Python là một ca làm có môi trường rõ, dữ liệu có nơi sống, lỗi có đường đi và thời gian được điều phối theo việc đang tính hay đang chờ.

Đã sửa:

- project/environment được dạy trước runtime;
- source, interpreter và process không còn bị trộn;
- name/object/mutation dùng một hệ nhãn–thùng nhất quán;
- exception dùng chồng phiếu việc và traceback là đường lỗi;
- serialization được giải thích là đóng hàng thành byte qua cửa;
- sync/async/thread/process bắt đầu từ hai loại thời gian: tính và chờ;
- bỏ mốc version Python khỏi mạch chính để tránh chi tiết nhanh lỗi thời;
- request web đi từ socket → server → framework → handler bằng ngôn ngữ plain-first.

**Đánh giá:** đạt beginner-first. Chương time vẫn là phần khó nhất và nên đọc chậm cùng visual trace.

### F03 — Database Fundamentals / PostgreSQL

**Cơn đau:** hai khách cùng mua món cuối, dữ liệu có thể âm; máy tắt sau chữ “thành công”; người vận hành cần biết query chậm ở đâu.
**Ẩn dụ xuyên suốt:** nhà hàng có sổ kho và nhiều quầy.
**Spine:** sự thật và luật → người xử lý → đường lấy dữ liệu → phiên bản/khóa → lưu bền → vận hành.
**Golden takeaway:** Database là người giữ sổ chung: chặn điều sai, điều phối nhiều người, chọn đường lấy dữ liệu và giữ bằng chứng để phục hồi.

Đã sửa:

- modeling đi từ fact đời thường rồi mới tới relation/key/constraint;
- bổ sung 5 mechanism steps cho modeling;
- backend riêng và memory chung được giải thích bằng quầy phục vụ + kho chung;
- planner và executor tách thành người chọn đường và người đi lấy hàng;
- MVCC/snapshot/lock bắt đầu từ nhiều bản sổ và người ghi xung đột;
- page/WAL/checkpoint/vacuum bắt đầu từ trang sổ, nhật ký và mốc kiểm kê;
- planner chỉ giữ B-tree, selectivity, estimate, sequential scan và evidence; bỏ danh sách index family khỏi mạch chính;
- replica và backup được tách bằng quầy dự phòng với kho hồ sơ lịch sử.

**Đánh giá:** đạt beginner-first ở mức bản đồ nền. Vì bài có 9 chương, người mới nên học hai lượt: `system → model → process → query`, sau đó `transaction → storage → planner → operations`.

## 5. Quyết định về 35 visual

Không loại visual nào trong vòng này vì audit theo câu hỏi nhận thức cho thấy:

- Linux: 10 visual tách command, permission, syscall, pipeline, script, build, Make, schedule và synthesis.
- Python: 11 visual tách project boundary, runtime, object/error/boundary, timing/GIL, request path và synthesis.
- Database: 14 visual tách system/model/process/query, concurrency, durability, planner, operations và synthesis.

Visual chỉ được tiếp tục giữ nếu browser QA chứng minh:

1. đọc trực tiếp được trong article rộng;
2. có reading cue trước;
3. có câu tự kể lại riêng sau;
4. không lặp cùng một kết luận với visual khác.

## 6. Rủi ro còn lại và cách dùng đúng

- Bài dễ hiểu hơn không có nghĩa chỉ đọc là thành kỹ năng; mini-lab và self-check vẫn bắt buộc.
- Glossary là công cụ mở khi gặp từ lạ, không phải danh sách phải học thuộc.
- Database dài hơn hai bài còn lại vì phạm vi rộng; không ép người mới đọc một lượt.
- Nếu feedback người mới vẫn dừng ở một thuật ngữ, sửa ngay câu trước thuật ngữ đó; không thêm một framework giải thích mới.
