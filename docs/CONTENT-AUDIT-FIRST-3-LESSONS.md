# Audit nội dung — F01 Linux, F02 Python, F03 Database

Ngày audit: 2026-09-24  
Phạm vi: `fsds-learning-hub.html`, ba learning digest, ba slide gốc, syllabus và sách liên quan trong `library/`.

## Kết luận điều hành

Ba bài đầu **đã vượt xa cách chuyển slide thành card**. Chúng đã có một trục suy luận rõ: nhìn một hành vi thật → dự đoán → lần theo state/boundary → gọi tên cơ chế → nối sang nghề. Chất lượng nội dung hiện tại phù hợp với một bài viết kỹ thuật dạng editorial/field note hơn là slide bài giảng truyền thống.

Điểm mạnh nhất là **bóc tách ownership và boundary**: Linux tách terminal/shell/process/kernel; Python tách shell/process/interpreter/object/I/O; Database tách logical intent/backend/planner/executor/page/WAL. Đây là lớp kiến thức nền có khả năng tái sử dụng khi học API, container, pipeline và distributed systems.

Điểm yếu chung trước lần chỉnh này:

1. Visual trong bài chưa đạt chất lượng và khả năng khám phá như sản phẩm Archify.
2. Hub chưa thật sự là công cụ học cá nhân: chưa có note drawer, autosave và reading progress.
3. Python thiếu một đoạn nền tảng quan trọng từ slide gốc: virtual environment và dependency reproducibility.
4. Database rất giàu nội dung nhưng dễ tạo cảm giác “đúng nhưng quá nhiều” với người mới; cần bản đồ, câu hỏi dẫn đường và progressive disclosure mạnh.
5. Chưa có catalog visual và quy chuẩn nhúng visual để những bài sau giữ được cùng ngôn ngữ thiết kế.

Các điểm 1–3 đã được xử lý trong lần nâng cấp này. Điểm 4–5 được chuẩn hóa trong UI và tài liệu authoring.

## Thang đánh giá

| Trục | Câu hỏi audit |
|---|---|
| Nền tảng | Có giữ đúng kiến thức lõi, không chạy theo mẹo/công cụ nhất thời? |
| Vĩ mô → vi mô | Người học có biết mình đang ở đâu trước khi zoom sâu? |
| Cơ chế bản chất | Có giải thích state, boundary, ownership, flow và failure không? |
| Dễ hiểu | Non-tech hoặc người yếu tiếng Anh có theo được không? |
| Editorial | Có mạch dẫn như bài viết công nghệ, thay vì danh sách định nghĩa? |
| Visual-first | Visual có mang quan hệ chính, text không chỉ lặp lại visual? |
| Transfer | Mental model có dùng lại được trong lab/công việc không? |
| Evidence | Có chỉ ra cách biết kết luận đúng hay sai? |
| Coverage | Có phủ deck/syllabus và chắt lọc sách liên quan? |
| Cognitive load | Có tránh dồn quá nhiều thuật ngữ trước khi tạo mental model? |

## F01 — Linux Fundamentals

### Đánh giá

| Trục | Điểm | Nhận xét |
|---|---:|---|
| Nền tảng | 9.2/10 | Tập trung đúng vào shell, process, kernel, stream, build và scheduled execution. |
| Vĩ mô → vi mô | 9.4/10 | Trục “ý định → shell → process/kernel → flow → tự động hóa” rất rõ. |
| Cơ chế bản chất | 9.3/10 | Tách terminal khỏi shell; tách user space, syscall, kernel và resource; giải thích exit status/stderr. |
| Dễ hiểu | 8.7/10 | Tiếng Việt gần gũi, mỗi thuật ngữ có nghĩa. Một số đoạn về glibc/fork/exec vẫn cần visual để giảm tải. |
| Editorial | 9.0/10 | Mở bằng `cat /etc/os-release`, có câu hỏi và nhịp kể chuyện. |
| Visual-first | 8.2 → 9.2/10 | Sketch tốt; sau nâng cấp có architecture, sequence và lifecycle Archify. |
| Transfer | 9.1/10 | Dùng lại được cho container, Airflow, cron/systemd, CI và debugging. |
| Evidence | 8.8/10 | stderr, exit status, log và artifact là evidence rõ. |
| Coverage | 8.8/10 | Phủ đúng syllabus; chủ động bỏ phần lịch sử distro dài của slide để ưu tiên cơ chế. |
| Cognitive load | 8.8/10 | Tốt, dù cảnh kernel có mật độ thuật ngữ cao. |

### Điều làm tốt

- Không bắt đầu bằng “Linux là gì?” hay lịch sử GNU/Linux; bắt đầu bằng một command có kết quả quan sát được.
- Phân biệt chính xác:
  - terminal hiển thị;
  - shell parse;
  - process thực thi;
  - kernel cấp dịch vụ/tài nguyên.
- Pipe được dạy như contract của stream (`stdin/stdout/stderr`), không như một ký tự `|` phải nhớ.
- Make được đặt đúng vai trò: dependency scheduler cho build, không phải compiler.
- Cron được giải ảo: trigger theo thời gian, không phải orchestrator có retry/backfill/overlap control.
- Ngôn ngữ có “cầu nối” cho người mới nhưng luôn quay về cơ chế thật.

### Điểm cần giữ kỷ luật

- `fork/exec` là mental model Unix phổ biến nhưng implementation path có thể khác theo shell/runtime; bài nên tiếp tục nói ở mức boundary, không hứa mọi command luôn tạo process theo cùng một chuỗi nội bộ.
- `set -Eeuo pipefail` là policy mạnh, không phải template áp dụng mù quáng. Khi mở rộng lab cần có ví dụ edge case của `errexit`.
- Không mở rộng bài thành catalog command, distro hoặc package manager. Các phần này nên là reference/lab, không chen vào trục chính.

### Visual đã nâng cấp

1. `linux-command-architecture` — architecture: command từ terminal xuống kernel/resource.
2. `linux-pipeline-sequence` — sequence: stdout → stdin, stderr đi riêng.
3. `linux-make-cron-lifecycle` — lifecycle: source → artifact → scheduled job → evidence.

## F02 — Python Fundamentals

### Đánh giá

| Trục | Điểm | Nhận xét |
|---|---:|---|
| Nền tảng | 9.1/10 | Sau bổ sung project boundary, bài cân bằng runtime, object model, error, I/O và concurrency. |
| Vĩ mô → vi mô | 9.3/10 | Trục mới: “project → runtime → object/lỗi → I/O → thời gian → web”. |
| Cơ chế bản chất | 9.4/10 | Name binding, frame/unwinding, serialization boundary và async đều được giải thích bằng state. |
| Dễ hiểu | 8.6/10 | Rõ hơn đa số bài nhập môn; AST/bytecode/GIL vẫn là đoạn khó và cần giữ progressive disclosure. |
| Editorial | 9.0/10 | Theo một lệnh `python -m pipeline ingest orders.csv`, không đi theo chương mục syntax. |
| Visual-first | 8.1 → 9.2/10 | Sau nâng cấp có architecture runtime, async lifecycle và request sequence. |
| Transfer | 9.5/10 | Dùng trực tiếp cho FastAPI, Airflow, data pipelines, crawler và model serving. |
| Evidence | 8.8/10 | Traceback, cProfile/tracemalloc, exit/HTTP status và metrics là evidence đúng tầng. |
| Coverage | 8.1 → 9.0/10 | Gap virtual environment/dependency đã được bổ sung; syntax cơ bản vẫn được cố ý đẩy ra reference. |
| Cognitive load | 8.5/10 | Nhiều khái niệm sâu trong một bài; map và sectioning giúp nhưng lab cần chia thời gian. |

### Điều làm tốt

- Không đồng nhất Python với syntax; bài dạy “một chương trình sống như thế nào”.
- Name binding và mutation được giải bằng “hai nhãn, một object”, tốt hơn cách nói mơ hồ “biến chứa giá trị”.
- Exception được nối với frame, call stack, unwinding và cleanup; người học biết traceback là bản đồ chứ không phải một khối chữ đỏ.
- Serialization được đặt ở boundary: object trong RAM không tự đi qua file/socket/DB.
- Async được giải đúng bản chất: chồng thời gian chờ; không tự tạo thread và không biến CPU work thành parallelism.
- GIL được nói có điều kiện theo CPython build/runtime, tránh biến implementation detail thành chân lý ngôn ngữ.
- Request web tách Uvicorn/ASGI/FastAPI/router/handler/downstream; ownership rõ.

### Gap đã sửa

Slide gốc dành dung lượng lớn cho virtualenv, Poetry và uv, trong khi bản bài viết trước đó chưa có section tương ứng. Bản mới thêm **“Chạy đúng code bằng đúng môi trường”**:

```text
pyproject.toml
  → resolver
  → lockfile (nếu workflow dùng lock)
  → .venv / site-packages
  → test và run bằng đúng interpreter
```

Nội dung không biến thành tutorial công cụ. `venv`, uv và Poetry được đặt dưới một mental model chung: declaration, resolution, lock, environment và reproducibility.

### Điểm cần giữ kỷ luật

- Không đưa toàn bộ syntax, OOP và standard library vào mạch chính. Chúng thuộc reference/lab sau khi mental model hình thành.
- Khi dạy performance, luôn đo trước khi chọn async/thread/process.
- Không nói “async nhanh hơn”; phải nói workload nào đang chờ và boundary nào hỗ trợ non-blocking.
- Free-threaded CPython và ecosystem compatibility có thể thay đổi; nội dung phải ghi rõ runtime/build thay vì đưa lời hứa tuyệt đối.

### Visual đã nâng cấp

1. `python-runtime-architecture` — architecture: shell/process/interpreter/module/object/I/O.
2. `python-concurrency-lifecycle` — lifecycle: task chạy → await → task khác → resume.
3. `python-request-sequence` — sequence: socket → Uvicorn → FastAPI → handler → downstream.

## F03 — Database Fundamentals / PostgreSQL

### Đánh giá

| Trục | Điểm | Nhận xét |
|---|---:|---|
| Nền tảng | 9.5/10 | Relation/invariant, architecture, query path, MVCC, storage, planner và recovery đều đúng trục. |
| Vĩ mô → vi mô | 9.4/10 | Năm câu hỏi chẩn đoán giữ toàn bài không bị rơi thành catalog. |
| Cơ chế bản chất | 9.6/10 | Logical/physical, visibility/conflict, planner/executor, WAL/checkpoint/backup được tách chính xác. |
| Dễ hiểu | 8.2/10 | Câu chữ tốt nhưng mật độ cao; đây là bài dễ quá tải nhất cho non-tech. |
| Editorial | 8.9/10 | Mở bằng “nơi giữ sự thật cho nhiều người”, sau đó đào xuống implementation. |
| Visual-first | 8.5 → 9.3/10 | Đã thay toàn bộ 14 visual học tập bằng Archify; system, model, query, MVCC, storage, planner và production đều có visual lab riêng. |
| Transfer | 9.7/10 | Dùng trực tiếp cho ORM, tuning, lock, bloat, replication và restore. |
| Evidence | 9.6/10 | EXPLAIN ANALYZE, BUFFERS, wait event, lag, bloat và restore drill. |
| Coverage | 9.4/10 | Chắt lọc deck + sách database internals/modeling/PostgreSQL; bỏ syntax-first đúng chủ ý. |
| Cognitive load | 7.9/10 | Cần đọc theo lớp; người mới không nên cố nuốt toàn bộ page/WAL/MVCC trong một lượt. |

### Điều làm tốt

- Định nghĩa database bằng trách nhiệm giữ shared truth, invariant và durability; gần với nhu cầu thực tế hơn định nghĩa “collection of data”.
- Relational model không bị thu gọn thành table/row/column; có fact, key, constraint, normalization và access pattern.
- Backend process được tách khỏi toàn server; shared buffers không bị gọi là “toàn bộ cache”.
- Planner và executor được tách đúng vai trò. “Có index” không đồng nghĩa “dùng index”.
- MVCC visibility và lock conflict được dạy như hai cơ chế phối hợp, không nói sai rằng transaction “lock mọi thứ”.
- WAL, checkpoint, replica và backup/PITR được phân biệt rõ.
- Bài kết thúc bằng năm câu hỏi chẩn đoán thay vì checklist command.

### Rủi ro sư phạm

- Một buổi duy nhất khó đủ cho cả modeling, PostgreSQL architecture, query planning, MVCC, WAL, vacuum, replication và backup.
- Người mới có thể nhớ từ khóa nhưng chưa tạo được mô hình nếu visual không được đọc theo chapter.
- Phần “production posture” chỉ thật sự có nghĩa sau lab quan sát `EXPLAIN`, lock và restore.

### Quyết định biên tập

- Giữ bài như **bản đồ nền**; không biến thành tutorial SQL.
- Cho phép người mới dừng sau system/model/process; phần query/transaction/storage là lượt đọc sâu.
- Mỗi section tiếp tục có: câu hỏi dẫn đường, claim, visual, flow steps, takeaway và thuật ngữ cốt lõi.
- Lab sau bài là bắt buộc để biến kiến thức thành evidence.

### Visual đã nâng cấp

1. `postgresql-architecture` — architecture: app/driver/backend/planner/buffer/heap/WAL/recovery.
2. `postgresql-query-sequence` — sequence: SQL → parser → planner → executor → pages → EXPLAIN evidence.
3. `postgresql-mvcc-durability-lifecycle` — lifecycle: update → WAL → commit → checkpoint → recovery/PITR.

## Đánh giá phong cách viết kiểu technology Substack

### Đã đạt

- Có thesis rõ ở đầu bài.
- Dùng một tình huống xuyên suốt thay vì glossary.
- Mỗi section có headline mang kết luận, không chỉ tên chủ đề.
- Câu chữ ưu tiên active voice và quan hệ nguyên nhân–kết quả.
- Có nhịp “zoom out → zoom in → quay lại bản đồ”.
- Có các câu phá ngộ nhận: terminal không phải shell; async không phải CPU parallel; replica không phải backup.

### Chưa nên bắt chước Substack theo nghĩa hình thức

- Không kéo dài bằng anecdote không phục vụ cơ chế.
- Không dùng giọng opinion quá mạnh thay cho evidence.
- Không tối ưu tiêu đề giật gân.
- Không đưa quá nhiều aside khiến flow kỹ thuật bị đứt.

## Kết luận chất lượng sau nâng cấp

- **Linux:** sẵn sàng làm bài mở đầu engineering foundation.
- **Python:** sẵn sàng sau khi đã bổ sung project/dependency boundary; cần lab crawler nhỏ để khóa kiến thức.
- **Database:** chất lượng kỹ thuật cao; nên dạy theo hai lượt hoặc một buổi bản đồ + một lab evidence.
- **Hub:** đã chuyển từ “visual syllabus” sang “personal visual study desk” có note, autosave, progress, canvas gần full-width và 35/35 Archify visual labs.
