# F03 · Database Fundamentals: PostgreSQL từ nguyên lý tới vận hành

## Ý định bài học

Bài này không dạy SQL theo kiểu syntax-first. Người học đã biết syntax; mục tiêu là nhìn được database như một hệ thống quản lý state và nối các nguyên lý chung với cách PostgreSQL thực thi, bảo vệ, tối ưu và vận hành state đó.

## Mạch học vĩ mô → micro

Trước khi đi vào page, WAL hay planner, người học phải trả lời được năm câu hỏi theo đúng thứ tự:

1. **Database là gì?** Một nơi giữ sự thật cho nhiều người cùng đọc và thay đổi, có luật và có khả năng sống qua sự cố.
2. **Hợp đồng dữ liệu là gì?** Relation, key, constraint và transaction mô tả cái gì phải luôn đúng.
3. **PostgreSQL dựng hệ thống ra sao?** Client, backend process, shared memory, worker và durable storage là các boundary chính.
4. **Một việc chạy thế nào?** Query đi qua parse, plan, execute; transaction đi qua snapshot, version, WAL và checkpoint.
5. **Biết hệ thống khỏe hay chưa bằng gì?** Planner evidence, buffer hit, wait event, bloat, replication lag, backup và restore drill.

Người mới có thể dừng sau câu hỏi thứ ba và vẫn có mental model đúng. Người muốn đi sâu tiếp tục xuống micro để tối ưu và vận hành PostgreSQL bằng bằng chứng thay vì mẹo rời rạc.

Trục chính:

```text
logical intent
  -> process / protocol
  -> planner / executor
  -> buffer / page / index
  -> MVCC / WAL / checkpoint
  -> evidence / operations / recovery
```

Mental model cuối bài:

1. Dữ liệu đang ở đâu: relation, heap page, index, shared buffer hay WAL?
2. Ai nhìn thấy version nào: snapshot, xmin/xmax, isolation và lock?
3. Đường truy cập nào được chọn: statistics, cardinality, cost và access path?
4. Commit được bảo vệ ra sao: WAL, checkpoint, replica, backup và PITR?
5. Bằng chứng nào xác nhận: EXPLAIN ANALYZE, buffers, wait events, bloat, lag và restore drill?

## Source map

| Nguồn | Vai trò trong bài | Phần đã dùng |
|---|---|---|
| `course-slides/03-database-fundamentals.pdf` | Coverage check cho deck FSDS | database concepts; relational/NoSQL framing; DDL/DML/DQL/DCL/TCL; cost/performance; SQL database lab; SQLAlchemy bridge |
| `PostgreSQL - Up and Running - Regina O. Obe and Leo S. Hsu.pdf` | PostgreSQL feature and operations context | cluster/configuration; tables, constraints, indexes; query performance tuning; replication and external data |
| `Database Internals - Alex Petrov.pdf` | General storage-engine reasoning | pages, buffer/cache, WAL/logging, B-tree/indexing, MVCC and transaction processing |
| `Database Design and Modeling with PostgreSQL and MySQL - Alkin Tezuysal and Ibrar Ahmed.pdf` | Relational modeling bridge | entities/relationships, keys, normalization, constraints, physical design |
| `Database Design and Relational Theory - C.J. Date.pdf` | Relational vocabulary and integrity | relation, tuple, attribute, key, predicate, integrity and logical/physical separation |
| PostgreSQL official docs | Authoritative behavior check | architecture, query path, MVCC, WAL, vacuum, indexes, planner, EXPLAIN, backup and replication |

Official references used for claims:

- <https://www.postgresql.org/docs/current/tutorial-architecture.html>
- <https://www.postgresql.org/docs/current/overview.html>
- <https://www.postgresql.org/docs/current/mvcc.html>
- <https://www.postgresql.org/docs/current/wal-intro.html>
- <https://www.postgresql.org/docs/current/routine-vacuuming.html>
- <https://www.postgresql.org/docs/current/indexes.html>
- <https://www.postgresql.org/docs/current/using-explain.html>
- <https://www.postgresql.org/docs/current/backup.html>
- <https://www.postgresql.org/docs/current/logical-replication.html>
- <https://www.postgresql.org/docs/current/runtime-config-resource.html>

## Coverage map

| Deck / syllabus claim | Quyết định biên tập |
|---|---|
| Database concepts | Giữ, nhưng mở bằng state và query episode thay vì định nghĩa rời rạc. |
| SQL và nhóm DDL/DML/DQL/DCL/TCL | Không cho syntax chiếm màn hình chính; đưa vào inspector như notation sau mental model. |
| SQL vs NoSQL | Không làm một scene so sánh hời hợt. Relational model và access path được nối với PostgreSQL; NoSQL xuất hiện như trade-off boundary khi cần. |
| Cost/performance optimization | Bổ sung planner, statistics, selectivity, cost, EXPLAIN ANALYZE, buffers và wait events. |
| Database architecture | Bổ sung client/protocol, backend process, shared memory, background workers, cluster files và durable storage. |
| Transactions | Bổ sung MVCC, snapshot, xmin/xmax, isolation, row locks và deadlock. |
| Storage | Bổ sung heap page, line pointer, visibility map, free space map, WAL và checkpoint. |
| PostgreSQL operations | Bổ sung vacuum/autovacuum, pooling, physical/logical replication, backup/PITR và observability. |
| SQLAlchemy lab | Cố ý không biến thành tutorial ORM; chỉ giữ bridge: ORM request vẫn đi qua driver, protocol, backend, planner và transaction. |

## Scene semantics

### 01 · Bức tranh hệ thống

**Episode:** một request đọc/ghi đi từ client tới backend, memory, page/WAL và storage.

**Claim:** database là hệ thống quản lý state, không chỉ là bảng.

**Visual:** layer stack; client/protocol → backend → shared memory → cluster files → durable storage, với CPU/RAM/disk/network làm tài nguyên nền.

**Glossary:** logical model, backend process, shared buffers, heap page, WAL, durability.

### 02 · Mô hình dữ liệu

**Episode:** business fact được biến thành relation, key, foreign key và invariant.

**Claim:** normalization là cách giảm anomaly; denormalization chỉ có giá trị khi access pattern và evidence biện minh.

**Visual:** tree/mindmap từ relational database xuống relation, key, referential integrity, normalize/denormalize và logical-versus-physical.

### 03 · Process PostgreSQL

**Episode:** nhiều client cùng vào một cluster nhưng không dùng chung một backend context.

**Claim:** backend per connection và shared memory là hai boundary khác nhau; background workers xử lý hậu cần.

**Visual:** layer stack với server/postmaster, backend, shared memory, WAL/checkpointer/autovacuum và cluster.

### 04 · Query path

**Episode:** một aggregate query đi qua driver, parser/rewrite, planner, executor, buffer manager và heap/index.

**Claim:** planner tạo plan trước; executor mới thực thi access path.

**Visual:** sequence diagram, labels ngắn và inspector giải thích parse tree, statistics, cost, buffer hit/miss, EXPLAIN ANALYZE.

### 05 · Transactions và MVCC

**Episode:** T1 update/commit trong khi T2 đọc và sau đó gặp write conflict.

**Claim:** snapshot quyết định visibility; lock bảo vệ conflict; vacuum phải chờ version không còn snapshot cần.

**Visual:** timeline hai transaction + visibility lane.

### 06 · Storage và durability

**Episode:** tuple version đi vào heap page; WAL đi trước data page; checkpoint giới hạn crash recovery; vacuum dọn version đủ cũ.

**Claim:** WAL là redo evidence, không phải bản sao data page; VACUUM không đồng nghĩa compact toàn bộ table.

**Visual:** layer stack tuple → page → VM/FSM → WAL → checkpoint/recovery.

### 07 · Index và planner

**Episode:** predicate được ước lượng, planner so seq/index/bitmap/index-only, rồi EXPLAIN ANALYZE đối chiếu actual.

**Claim:** tồn tại index không đồng nghĩa planner phải dùng nó.

**Visual:** dependency DAG statistics → predicate/selectivity → access path → cost → evidence.

### 08 · Production posture

**Episode:** app mượn connection, primary commit và stream WAL, autovacuum dọn, backup archive WAL, observability đo evidence.

**Claim:** replica không thay backup; backup/PITR là đường khôi phục lỗi logic.

**Visual:** sequence diagram giữa app/pooler, primary, autovacuum, standby, backup/archive và observability.

### 09 · Bản đồ suy luận

**Episode:** quay lại năm câu hỏi để chẩn đoán query chậm, lock, bloat, lag hoặc recovery.

**Claim:** database engineering là nối logical intent với physical evidence.

**Visual:** mindmap PostgreSQL với năm nhánh: where, who, path, durable, evidence.

## Nguyên tắc thuật ngữ

- `relation / table`: relation là thuật ngữ mô hình; table là cách PostgreSQL expose relation.
- `tuple / row`: tuple là thuật ngữ relational; row là cách nói SQL.
- `attribute / column`: attribute nói vai trò logic; column nói representation trong table.
- `backend`: process phục vụ connection, không phải toàn bộ PostgreSQL server.
- `shared buffers`: cache page của PostgreSQL, không phải toàn bộ OS page cache.
- `WAL`: log thay đổi để redo/recovery/replication; không được mô tả như “database backup”.
- `VACUUM`: lifecycle cleanup của MVCC và statistics; `VACUUM FULL` là operation khác với lock/rewriting khác.
- `index-only scan`: chỉ có thể tránh heap fetch khi index đủ dữ liệu và visibility map cho phép.

## Các điểm phải nói đúng

1. Process model và worker naming có thể thay đổi theo PostgreSQL version, platform và extension; lesson dùng boundary ổn định thay vì hứa tên nội bộ bất biến.
2. `EXPLAIN` không chạy query; `EXPLAIN ANALYZE` chạy thật. Dùng nó trên write statement có side effect nếu không bọc transaction và rollback.
3. `Read Committed`, `Repeatable Read` và `Serializable` có semantics khác nhau; không gộp thành “transaction lock mọi thứ”.
4. WAL trước data page là write-ahead rule; commit durability còn phụ thuộc cấu hình sync/replication policy và failure model.
5. Index family không có thứ hạng tuyệt đối. B-tree, Hash, GiST, SP-GiST, GIN, BRIN phục vụ access pattern khác nhau.
6. Autovacuum vừa cleanup vừa cập nhật statistics và bảo vệ transaction ID horizon; tuning threshold phải nhìn workload, không copy một con số.
7. Physical streaming replication và logical replication có topology, lag, conflict và failure semantics khác nhau.
8. Replica cải thiện availability/read scale nhưng có thể replay lag và tái tạo cả thao tác xóa hợp lệ; backup/PITR vẫn cần thiết.

## Bridge sang nghề

Khi dùng SQLAlchemy, psycopg hoặc một framework data layer, syntax chỉ tạo request. Câu hỏi cốt lõi vẫn giữ nguyên:

```text
application call
  -> driver / protocol
  -> backend + transaction
  -> parse / plan / execute
  -> buffer / page / index
  -> WAL / commit
  -> result + evidence
```

Các thực hành cần nối ở lab tiếp theo:

- đọc `EXPLAIN (ANALYZE, BUFFERS)` và giải thích estimate lệch;
- tạo workload để quan sát seq/index/bitmap path;
- mở transaction dài để thấy dead tuple và autovacuum horizon;
- mô phỏng lock order và deadlock;
- đo WAL rate, checkpoint, replication lag và restore từ base backup + WAL;
- viết query qua driver/ORM rồi truy ngược về plan thật.
