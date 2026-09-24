# Visual catalog — ba bài đầu

Tài liệu này là bản kê visual theo **mục tiêu nhận thức**, không phải danh sách hình trang trí. Mỗi visual phải trả lời câu hỏi mà prose khó truyền nhanh bằng quan hệ không gian, trình tự hoặc state.

## Nguyên tắc chọn visual

| Khi cần hiểu… | Dùng visual |
|---|---|
| Thành phần nằm ở layer/boundary nào | Architecture / layer stack |
| Ai gọi ai theo thời gian | Sequence |
| State chuyển như thế nào | Lifecycle / state machine |
| Data đi qua các bước biến đổi | Data flow |
| Dependency quyết định thứ tự | DAG |
| Hai cách dùng thời gian khác nhau | Timeline / swimlane |
| Hệ thống chọn giữa nhiều đường | Decision tree / planner DAG |
| Khái niệm gom thành các nhánh nhớ | Mindmap |
| Fact, key và relationship | ER / relational model |
| Evidence thay đổi theo workload | Chart/heatmap/scatter, chỉ khi có dữ liệu thật |

## F01 — Linux

### L01. Super map: ý định tới hệ điều hành

- **Loại:** architecture + layer stack.
- **Mục tiêu:** định vị terminal, shell, GNU tools, process, libc/syscall, kernel, CPU, RAM và I/O.
- **Nội dung:** một main path `user intent → terminal → Bash → process → syscall → kernel`, sau đó fan-out tới CPU/RAM/I/O.
- **Phương thức:** Archify architecture, 2 boundary `user space` và `kernel-managed resources`.
- **Tiêu chí:** label ngắn; mỗi connector là một hành động; không vẽ CPU/RAM/I/O như các bước tuần tự.

### L02. Command execution trace

- **Loại:** sequence.
- **Mục tiêu:** thấy `cat /etc/os-release` không “tự đọc đĩa”.
- **Actors:** user, terminal, shell, process, kernel, filesystem, terminal output.
- **Messages:** key input, parse argv/PATH, exec, open/read, bytes, stdout.
- **Failure branch:** `EACCES → stderr → exit != 0`.
- **Phương thức:** step player hoặc Archify sequence; failure path có màu cảnh báo, không trộn với data path.

### L03. Path + permission anatomy

- **Loại:** annotated filesystem tree + permission matrix.
- **Mục tiêu:** phân biệt absolute/relative path, cwd, owner/group/other và r/w/x.
- **Nội dung:** cây `/home/student/report.log`, vị trí cwd, ba bộ bit, một request read được kernel kiểm tra.
- **Phương thức:** SVG tương tác; click path node đổi inspector.

### L04. User space → kernel → resource

- **Loại:** layer stack.
- **Mục tiêu:** thấy system call là boundary, không phải “một library bình thường”.
- **Nội dung:** process/glibc → syscall → kernel → scheduler/address space/driver.
- **Phương thức:** vertical architecture; chỉ một đường chính, resource fan-out ở đáy.

### L05. Pipeline streams

- **Loại:** sequence/data flow.
- **Mục tiêu:** hiểu `cat | grep | wc` bằng stdin/stdout/stderr.
- **Nội dung:** ba process, hai pipe, stderr lane riêng, redirect là thay destination.
- **Phương thức:** Archify sequence có guided view happy path/error path.

### L06. Script contract

- **Loại:** flowchart/state machine.
- **Mục tiêu:** input validation → pipeline → exit status.
- **Nội dung:** shebang, strict mode, readable input?, run, write output, exit 0/1.
- **Phương thức:** static flowchart + code snippet đồng bộ highlight.

### L07. Compilation pipeline

- **Loại:** artifact flow.
- **Mục tiêu:** phân biệt preprocess/compile/assemble/link.
- **Nội dung:** `.c → .i → .s → .o → executable`, loại lỗi ở từng boundary.
- **Phương thức:** horizontal process diagram; artifact là node, tool là connector label.

### L08. Make dependency DAG

- **Loại:** DAG.
- **Mục tiêu:** Make quyết định “cái gì cũ”, không tự compile.
- **Nội dung:** source/header → object → binary; timestamp/dirty status.
- **Phương thức:** click một source để highlight downstream targets bị invalidated.

### L09. Cron lifecycle

- **Loại:** lifecycle.
- **Mục tiêu:** cron trigger khác orchestrator.
- **Nội dung:** time match → thin shell → job → log/exit; side branch overlap/failure.
- **Phương thức:** Archify lifecycle cho main path; bảng đối chiếu cron vs systemd/Airflow cho capability.

### L10. Linux synthesis mindmap

- **Loại:** progressive mindmap.
- **Mục tiêu:** gom kiến thức theo câu hỏi chẩn đoán.
- **Nhánh:** who parses, where state lives, resource, streams, repeat/build, scheduled operation.
- **Phương thức:** mặc định chỉ render root + branch chính; mỗi lần mở tối đa một nhánh.

## F02 — Python

### P01. Project reproducibility boundary

- **Loại:** architecture/data flow.
- **Mục tiêu:** thấy declaration, resolution, lock và environment là bốn vai trò khác nhau.
- **Nội dung:** `pyproject.toml → resolver → lockfile → .venv/site-packages → test/run`.
- **Phương thức:** horizontal flow; tool names (venv/uv/Poetry) là ví dụ dưới role, không trở thành node chính.

### P02. Python runtime architecture

- **Loại:** architecture.
- **Mục tiêu:** shell/process/interpreter/module/object/I/O nằm ở boundary nào.
- **Nội dung:** argv/cwd/env → process → AST/bytecode/interpreter → namespace/frame/object → file/socket/kernel.
- **Phương thức:** Archify architecture với guided views startup/resources.

### P03. Startup sequence

- **Loại:** sequence.
- **Mục tiêu:** `python -m` chạy interpreter trước module.
- **Actors:** shell, OS, CPython, import system, module, `main()`.
- **Phương thức:** step trace; mark import-time side effects.

### P04. Name binding object graph

- **Loại:** object-reference graph.
- **Mục tiêu:** assignment, alias, mutation, rebinding, identity.
- **Nội dung:** names là label; object là node; arrows thay đổi qua 4 frames.
- **Phương thức:** small multiples hoặc scrubber; không dùng animation trang trí.

### P05. Call stack + exception unwinding

- **Loại:** stack trace animation.
- **Mục tiêu:** frame được push/pop, exception đi ngược tới handler.
- **Nội dung:** main → load → parse → raise → finally/context manager → handler/exit.
- **Phương thức:** stack view + source-line highlight.

### P06. Serialization boundary

- **Loại:** boundary/data flow.
- **Mục tiêu:** object không đi trực tiếp qua file/socket/DB.
- **Nội dung:** object → validate/schema → encode → bytes → transport/store → decode → object mới.
- **Phương thức:** two-sided boundary diagram; schema nằm trên crossing point.

### P07. Sync vs async timeline

- **Loại:** swimlane timeline.
- **Mục tiêu:** async chồng khoảng chờ, không chồng đoạn CPU trên một thread.
- **Nội dung:** task A/B, CPU blocks, waiting blocks, ready queue.
- **Phương thức:** timeline có cùng scale thời gian cho hai phương án.

### P08. Async lifecycle

- **Loại:** lifecycle.
- **Mục tiêu:** state `running → waiting → ready → running`.
- **Phương thức:** Archify lifecycle; note rõ không tạo thread/CPU core.

### P09. GIL decision map

- **Loại:** decision tree.
- **Mục tiêu:** chọn async/thread/process/native engine theo workload.
- **Câu hỏi:** chủ yếu chờ I/O? library nhả GIL? CPU Python thuần? isolation cần không?
- **Phương thức:** decision tree, không dùng bảng “cái nào nhanh nhất”.

### P10. Web request sequence

- **Loại:** sequence.
- **Mục tiêu:** framework giữ outer loop, app giữ policy.
- **Actors:** client, socket, Uvicorn, FastAPI/router/dependencies, handler, event loop, DB/API.
- **Phương thức:** Archify sequence; guided view request/blocking risk.

### P11. Python synthesis mindmap

- **Loại:** mindmap.
- **Nhánh:** project, runtime, objects, errors, bytes, time, framework/evidence.

## F03 — Database/PostgreSQL

### D01. Database responsibility map

- **Loại:** high-level architecture.
- **Mục tiêu:** database giữ shared truth, invariant, concurrency và durability.
- **Nội dung:** clients → contract → state → recovery/evidence.

### D02. Relational model / ER

- **Loại:** ER + invariant callouts.
- **Mục tiêu:** entity/fact, relation, tuple, attribute, PK/FK, cardinality, constraint.
- **Nội dung:** orders/customers/order_items; uniqueness/referential/check constraints.
- **Phương thức:** ER diagram có business sentence cạnh relationship.

### D03. Normalization anomaly triptych

- **Loại:** before/after small multiples.
- **Mục tiêu:** thấy update/insert/delete anomaly trước khi gọi tên normalization.
- **Phương thức:** ba panel cùng một fact; highlight duplicate state.

### D04. PostgreSQL architecture

- **Loại:** architecture.
- **Mục tiêu:** client/driver/backend/shared memory/workers/storage/WAL boundary.
- **Phương thức:** Archify architecture; guided views request/durability.

### D05. Query execution sequence

- **Loại:** sequence.
- **Mục tiêu:** parser/rewrite/planner/executor/storage/evidence.
- **Phương thức:** Archify sequence; planner path và EXPLAIN view.

### D06. Planner decision DAG

- **Loại:** dependency DAG.
- **Mục tiêu:** statistics → selectivity/cardinality → candidate path → cost → chosen plan.
- **Nội dung:** seq scan, index scan, bitmap, index-only + visibility map constraint.
- **Phương thức:** click predicate để đổi estimate/path, nếu có dữ liệu lab thật.

### D07. MVCC transaction timeline

- **Loại:** multi-lane timeline.
- **Mục tiêu:** snapshot visibility khác lock conflict.
- **Lanes:** T1, T2, tuple versions, row lock, vacuum horizon.
- **Phương thức:** step trace với xmin/xmax trong inspector, không nhồi vào label.

### D08. Page/storage anatomy

- **Loại:** nested/layer stack.
- **Mục tiêu:** relation → heap/index file → page → line pointer → tuple; shared buffer là cache page.
- **Phương thức:** zoomable nested diagram.

### D09. WAL/checkpoint/recovery lifecycle

- **Loại:** lifecycle.
- **Mục tiêu:** write-ahead rule và recovery boundary.
- **Phương thức:** Archify lifecycle; backup/PITR card riêng.

### D10. VACUUM lifecycle

- **Loại:** lifecycle/state machine.
- **Mục tiêu:** live → dead → no snapshot needs → reusable; autovacuum + stats + xid horizon.
- **Phương thức:** separate from WAL visual để tránh quá tải.

### D11. Index family map

- **Loại:** matrix / radial map.
- **Mục tiêu:** index family theo access pattern, không xếp hạng “tốt nhất”.
- **Trục:** equality/range/order/membership/spatial/physical correlation; cost/storage/update overhead.

### D12. Production topology

- **Loại:** architecture/sequence.
- **Mục tiêu:** pooler, primary, standby, archive, backup, observability.
- **Phương thức:** topology + failure overlays; replica và backup dùng connector semantics khác nhau.

### D13. Evidence dashboard

- **Loại:** table + charts chỉ dùng dữ liệu lab thật.
- **Mục tiêu:** estimate vs actual, buffer hit/read, wait event, WAL rate, lag, dead tuples, restore time.
- **Phương thức:** không dùng số giả. Nếu chưa có dataset, dùng annotated schema thay chart.

### D14. PostgreSQL synthesis mindmap

- **Nhánh:** where, who sees, path, durability, evidence.
- **Phương thức:** progressive disclosure; một nhánh mở tại một thời điểm.

## Visual đã render bằng Archify

Toàn bộ catalog hiện đã được thực thi: **35/35 visual**.

| Bài | Số visual | ID |
|---|---:|---|
| Linux | 10 | L01–L10 |
| Python | 11 | P01–P11 |
| Database/PostgreSQL | 14 | D01–D14 |

- JSON source: `archify/specs/`
- Delivered artifact: `archify/rendered/`
- Deterministic receipt: `archify/receipts/*-deliver.json`
- Chapter mapping: `archifyVisuals` trong `fsds-learning-hub.html`

Tất cả 35 spec đã pass Archify `validate --quality showcase` với `composition: pass`, 0 error và 0 warning; sau đó được deliver thành standalone HTML. Native lesson SVG/HTML diagrams không còn được render trong ba bài đầu.
