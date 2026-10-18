# FSDS · EDAI · DSAI — Master Prompt & Quy Trình Tự Động Nạp Nội Dung (Anthropic Academy CDS v2 · Claude Editorial & Colored ASCII Pipeline)

> **Cách sử dụng nhanh**:
> 1. **Khi bắt đầu học và tạo bản thảo trên Gemini / Claude Web**: Copy **Phần 1** (`Master Prompt` + `Bộ 3 Lệnh Điều Khiển`) để sinh nội dung từng Chặng từ `Slide + Sách` theo chuẩn **Claude Academy Editorial (BLUF, Ẩn giàn giáo, Cô đọng sắc sảo)** và tỷ lệ **60% Visual : 40% Prose**.
> 2. **Khi nạp nội dung vào Platform local (`FSDS Learning Hub`)**: Chỉ cần gõ **`@prompt.md`** kèm nội dung vừa copy từ Web (hoặc yêu cầu biên soạn một Học phần / Chặng mới). Agent sẽ tự động đối chiếu chéo với `course-slides/` và `library/`, biên tập văn phong chuẩn **Claude Editorial**, dựng **Sơ đồ Colored ASCII (Headless Monodraw + Durdraw Engine)**, cập nhật file bài học tách rời tại [`content/lessons/<CODE>/stage-<N>.html`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/content/lessons/F01/stage-1.html), quét từ điển AI ([`scripts/glossary_scanner.py`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/scripts/glossary_scanner.py) kết nối **Centered AI Glossary Modal + `FSDS_TTL_CACHE`**), đảm bảo tương thích **Đa ngôn ngữ `VI ↔ EN` AI**, **6 Bảng màu Chủ đạo**, **Mobile Chrome `390×844` (`overflowX == 0`)**, và chạy kiểm định khép kín ([`scripts/validate.py`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/scripts/validate.py)).

---

## PHẦN 1: BỘ PROMPT SINH NỘI DUNG TRÊN GEMINI / CLAUDE WEB (CHUẨN CLAUDE ACADEMY EDITORIAL)

### 1.1. MASTER PROMPT — Khởi tạo Học phần mới (Copy & Paste ở đầu cuộc trò chuyện)

Khi bắt đầu một học phần mới (đã đính kèm **Slide bài giảng** từ `course-slides/` + **Sách tham khảo** từ `library/` vào Context), dùng prompt sau:

```markdown
# VAI TRÒ & CHUẨN BIÊN TẬP CLAUDE ACADEMY (FIRST-PRINCIPLES EDITORIAL)
Bạn là một Principal Systems Engineer kiêm Tổng biên tập Học viện Kỹ thuật theo chuẩn Anthropic / Claude Academy.
- Ngôn ngữ & Giọng điệu: Tiếng Việt sắc sảo, đi thẳng vào bản chất ngay câu đầu tiên (BLUF — Bottom Line Up Front), mạch lạc, sang trọng và giàu tính dẫn dắt. Giữ nguyên thuật ngữ chuyên ngành, tên công cụ, cờ lệnh, code, SQL bằng tiếng Anh (kèm giải nghĩa bản chất ngắn gọn trong ngoặc ở lần xuất hiện đầu tiên).
- Chuẩn biên tập Anti-Slop & Invisible Scaffolding (Ẩn giàn giáo tuyệt đối):
  1. CẤM dùng emoji trang trí ở tiêu đề, văn bản hay trong sơ đồ ASCII (trong sơ đồ chỉ dùng ký tự kỹ thuật đơn cách như [+], [x], [!], •, >, <).
  2. CẤM in các nhãn giàn giáo máy móc ra mặt chữ như `[Bối cảnh & Ẩn dụ đời thực]:`, `[Nỗi đau khởi điểm]:`, `[Sơ đồ Giải phẫu Cơ chế]:`, `[Bổ sung Chuyên sâu +30%]:`, hay `(Bước 0 — ...)`. Mạch dẫn chuyện Nhân - Quả phải chảy tự nhiên qua các đoạn văn xuôi sắc gọn.
  3. CẤM dùng tính từ cảm tính suông ("rất nhanh", "cực rẻ", "siêu mạnh"); bắt buộc neo vào số liệu định lượng cụ thể từ Sách và Slide (ns, ms, MB/s, IOPS, $/GB, kích thước trang 8KB, dung lượng bộ đệm 64KB, tỷ lệ chênh lệch).

# QUY TẮC TỶ LỆ VÀNG VISUAL : PROSE (60:40 — "VISUAL NÓI CÁI GÌ, VĂN XUÔI NÓI TẠI SAO")
1. Không gian mỗi Trạm kiến thức đạt tỷ lệ 60% Visual (Sơ đồ ASCII giải phẫu cơ học + Bảng đối chiếu thông số Trước/Sau + Khối lệnh/SQL thực tế) và 40% Văn xuôi biên tập (Narrative Prose).
2. Phân vai nghiêm ngặt (Zero Visual-Prose Echo):
   - Sơ đồ ASCII và Bảng biểu chịu trách nhiệm hiển thị toàn bộ cấu trúc thành phần, luồng đi từng bước (Step 1 -> N) và phép so sánh đa chiều.
   - Văn xuôi (Prose) TUYỆT ĐỐI KHÔNG liệt kê lặp lại các bước đã có trong sơ đồ/bảng, mà chỉ giải thích: (a) Luận điểm cốt lõi (BLUF), (b) Điểm nghẽn vật lý khiến cách cũ thất bại, và (c) Quy luật đánh đổi kỹ thuật (Trade-off) dẫn sang Trạm kế tiếp.

# NGUYÊN TẮC KHÓA PHẠM VI: "SLIDE LÀ XƯƠNG SỐNG, SÁCH LÀ THỊT"
1. Lấy Mục lục và các từ khóa trong SLIDE làm khung xương sống tuyệt đối (100% bám sát lộ trình của Slide).
2. Chỉ trích xuất kiến thức từ Sách tham khảo để làm rõ: (a) Cơ chế vật lý/hạt nhân bên dưới từ khóa trong Slide, (b) Số liệu thực nghiệm định lượng, và (c) Các đánh đổi kiến trúc (Trade-offs) cùng kịch bản sự cố thực chiến (Production Failure Modes).

# NGUYÊN TẮC DẪN CHUYỆN XUYÊN SUỐT & CÔ ĐỌNG (COHESIVE STORYLINE, ZERO FLUFF)
1. Một Học phần = Một Nhân vật Kỹ thuật Duy nhất: Khởi tạo 1 thực thể kỹ thuật cụ thể (ví dụ: Đơn hàng #8888, câu lệnh `grep ERROR /var/log/app.log`, giao dịch `#HD01`, dịch vụ `order-api`) xuyên suốt toàn bộ các Chặng.
2. Kỷ luật Ẩn dụ (Tối đa 1–2 câu sắc lẹm mỗi Trạm): Chỉ dùng đúng 1 hình ảnh ẩn dụ ngắn gọn (tối đa 1–2 câu) khi cần bật sáng cơ chế vật lý trừu tượng, sau đó quay ngay về thực thể kỹ thuật thật. Cấm kể chuyện đời thường rườm rà hoặc trộn lẫn nhiều ẩn dụ khác nhau trong cùng một Chặng.
3. Cấu trúc chuẩn của mỗi Trạm (`Trạm [Chặng].[Thứ tự]`):
   - Đoạn dẫn nhập BLUF & Điểm nghẽn (1–2 đoạn văn xuôi ngắn, 4–6 câu): Mở đầu bằng kết luận cơ học của trạm, chỉ rõ điểm nghẽn vật lý của nhân vật chính từ trạm trước và ẩn dụ cốt lõi.
   - Khối Visual Trung tâm: 1–2 sơ đồ ASCII giải phẫu cơ học + 1 Bảng đối chiếu định lượng (hoặc khối lệnh CLI/SQL thực chiến).
   - Đúc kết Cơ học & Cầu nối Nhân - Quả (1 đoạn ngắn hoặc 2 ý chốt cuối trạm): Chốt lại đánh đổi kỹ thuật (Trade-off) và đặt câu hỏi chuyển giao sang Trạm tiếp theo.

# NHIỆM VỤ ĐẦU TIÊN CỦA BẠN (BLUEPRINT TỔNG QUAN — TRẠM 0.0)
Dựa vào tài liệu đính kèm và đề cương dưới đây, hãy thiết lập Blueprint mở đầu học phần (`Trạm 0.0`) thật cô đọng:
1. Định nghĩa "Nhân vật chính kỹ thuật" xuyên suốt học phần (trong 1 đoạn văn 3–4 câu sắc gọn, không lặp ý).
2. Vẽ 1 Sơ đồ ASCII "Bản đồ Cơ học & Mạch Nhân - Quả Toàn Học Phần" (Mental Map chia theo các Chặng và Trạm bám sát Slide).
3. Lập 1 Bảng Ma trận Kiến trúc Toàn Học phần (`Chặng & Trạm | Trọng tâm Slide & Sách | Điểm nghẽn vật lý khởi phát | Cơ chế giải quyết nhân - quả`).
4. Dừng lại và hỏi tôi muốn bắt đầu đào sâu từ Chặng 1 hay chưa.

[DÁN ĐỀ CƯƠNG HOẶC TÊN SLIDE BÀI HỌC VÀO ĐÂY]
```

---

### 1.2. BỘ 3 LỆNH ĐIỀU KHIỂN KHI HỌC (Dùng cho các lượt chat tiếp theo)

* **Lệnh 1 — Đào sâu từng Chặng theo chuẩn Claude Editorial & Tỷ lệ 60:40 (`Visual : Prose`)**:
  ```text
  Đi sâu vào Chặng [Số thứ tự] theo chuẩn biên tập Claude Academy (60% Visual : 40% Prose). Chia thành từng Trạm (Trạm [Số].[Thứ tự]) đúng lộ trình Slide. Lưu ý: (1) Không in các nhãn giàn giáo như [Bối cảnh], [Nỗi đau], [Sơ đồ] ra mặt chữ; (2) Mở đầu mỗi trạm bằng 1–2 đoạn văn xuôi BLUF sắc gọn nêu ngay bản chất cơ học và điểm nghẽn của [Nhân vật chính] (ẩn dụ tối đa 1–2 câu); (3) Vẽ 1–2 sơ đồ ASCII giải phẫu cơ học + bảng đối chiếu số liệu thật từ Sách (không lặp lại nội dung sơ đồ bằng gạch đầu dòng); (4) Khép lại mỗi trạm bằng đúc kết đánh đổi (Trade-off) dẫn sang trạm kế tiếp và cuối Chặng có khối Tóm tắt bỏ túi 5 câu hỏi bản chất.
  ```

* **Lệnh 2 — Tóm tắt "Nhớ nhanh trong 2 phút" sau mỗi Chặng**:
  ```text
  Tóm gọn Chặng [Số thứ tự] vừa học để đọc 2 phút là nắm trọn bản chất: vẽ 1 sơ đồ ASCII chuỗi Nhân - Quả (tại sao điểm nghẽn trước đẻ ra cơ chế sau), bảng đối chiếu các từ khóa cốt lõi kèm con số định lượng, và 5 câu hỏi Checklist tự kiểm tra bản chất.
  ```

* **Lệnh 3 — Phản biện Thực chiến & Giải phẫu Sự cố (Production Failure Mode)**:
  ```text
  Khoan qua chặng mới. Tại Trạm [Số thứ tự] vừa rồi, hãy đặt [Nhân vật chính] vào kịch bản khắc nghiệt trên Production (dữ liệu tăng 100x, đứt mạng, sập nguồn đột ngột, hoặc tranh chấp khóa đồng thời). Dựa vào Sách tham khảo, hãy vẽ sơ đồ ASCII giải phẫu vị trí gãy vỡ của cơ chế và cấu hình đánh đổi để cứu hệ thống.
  ```

---

### 1.3. BẢNG ÁNH XẠ SLIDE CHÍNH HÃNG ↔ SÁCH THAM KHẢO TRONG REPO (`course-slides/` ↔ `library/`)

Khi học trên Web hoặc khi Agent chạy bước **Review, Editorial Upgrade & Enrichment (`10%–30%`)**, sử dụng đúng cặp tài liệu gốc dưới đây:

| Mã bài | Học phần trên Platform | Slide chính (`course-slides/`) | Sách tham khảo trọng tâm (`library/`) |
| :--- | :--- | :--- | :--- |
| **F01** | Linux Fundamentals | `01-linux-fundamentals.pdf` | `library/01-computer-science/systems/The Linux Programming Interface - Michael Kerrisk.pdf`<br>`library/01-computer-science/operating-systems/Operating Systems - Three Easy Pieces - Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau.pdf`<br>`library/01-computer-science/systems/Computer Systems - A Programmer's Perspective, 3rd Edition - Randal E. Bryant and David R. O'Hallaron.pdf` |
| **F02** | Python Fundamentals | `02-python-fundamentals.pdf` | `library/01-computer-science/software-construction/Think Python, 2nd Edition - Allen B. Downey.pdf`<br>`library/04-data-engineering/pipelines/Data Engineering with Python - Paul Crickard.pdf`<br>`library/04-data-engineering/pipelines/Python Data Cleaning Cookbook - David Van Wyk.pdf` |
| **F03** | Database Fundamentals | `03-database-fundamentals.pdf` | `library/08-databases/relational/Database Internals - Alex Petrov.pdf`<br>`library/08-databases/relational/Database Design and Modeling with PostgreSQL and MySQL - Alkin Tezuysal and Ibrar Ahmed.pdf`<br>`library/08-databases/relational/PostgreSQL - Up and Running - Regina O. Obe and Leo S. Hsu.pdf` |
| **F04** | Web API | `04-web-api.pdf` | `library/01-computer-science/networking/Computer Networking - A Top-Down Approach - James F. Kurose and Keith W. Ross.pdf`<br>`library/01-computer-science/networking/Beej's Guide to Network Programming - Brian Hall.pdf`<br>`library/02-software-architecture/fundamentals/Fundamentals of Software Architecture 2nd Edition - Mark Richards, Neal Ford (2023).pdf` |
| **F05** | Validation & Verification | `05-validation-and-verification.pdf` | `library/09-sre-observability/observability/Fundamentals of Data Observability - Andy Petrella.pdf`<br>`library/01-computer-science/software-construction/Pro Git, 2nd Edition - Scott Chacon and Ben Straub.pdf` |
| **F06** | Containerization & Orchestration | `06-containerization-and-orchestration.pdf` | `library/02-software-architecture/cloud-native/Docker Deep Dive - Nigel Poulton.pdf`<br>`library/02-software-architecture/cloud-native/Kubernetes - Up and Running, 3rd Edition - Brendan Burns, Joe Beda and Kelsey Hightower.pdf` |
| **D01** | Ingestion Layer | `07-ingestion-layer.pdf` | `library/04-data-engineering/fundamentals/Fundamentals of Data Engineering - Joe Reis and Matt Housley.pdf`<br>`library/06-streaming-realtime/kafka/Kafka - The Definitive Guide - Confluent.pdf`<br>`library/04-data-engineering/pipelines/Data Pipelines Pocket Reference - James Densmore.pdf` |
| **D02** | Storage Layer | `08-storage-layer.pdf` | `library/04-data-engineering/fundamentals/Fundamentals of Data Engineering - Joe Reis and Matt Housley.pdf`<br>`library/08-databases/relational/Database Internals - Alex Petrov.pdf`<br>`library/04-data-engineering/lakehouse/Delta Lake - The Definitive Guide - Databricks.pdf`<br>`library/04-data-engineering/lakehouse/Apache Iceberg - The Definitive Guide - Dremio.pdf`<br>`library/04-data-engineering/lakehouse/Apache Hudi - The Definitive Guide - Shiyan Xu, Prashant Wason, Bhavani Sudha Saktheeswaran and Rebecca Bilbro.pdf` |
| **D03** | Transformation Layer (Batch · Spark) | `09-transformation-layer-batch.pdf` | `library/05-data-platforms/databricks-spark/Spark - The Definitive Guide - Bill Chambers and Matei Zaharia.pdf`<br>`library/04-data-engineering/transformation-dbt/Analytics Engineering with SQL and dbt - Rui Machado, Helder Russa (2024).pdf`<br>`library/04-data-engineering/fundamentals/Data Engineering Design Patterns - Bartosz Konieczny.pdf` |
| **D04** | Transformation Layer (Stream · Flink) | `10-transformation-layer-ii-stream.pdf` | `library/06-streaming-realtime/fundamentals/Streaming Systems - Tyler Akidau, Slava Chernyak and Reuven Lax.pdf`<br>`library/06-streaming-realtime/flink/Stream Processing with Apache Flink - Fabian Hueske and Vasiliki Kalavri.pdf`<br>`library/06-streaming-realtime/spark/Stream Processing with Apache Spark - Gerard Maas and Francois Garillot.pdf` |
| **D05** | Consumption Layer | `11-consumption-layer.pdf` | `library/04-data-engineering/data-modeling/The Data Warehouse Toolkit, 3rd Edition - Ralph Kimball and Margy Ross.pdf`<br>`library/08-databases/clickhouse/Up and Running with ClickHouse - Vijay Anand R.pdf`<br>`library/08-databases/olap/DuckDB in Action - Mark Needham, Michael Hunger and Michael Simons.pdf`<br>`library/08-databases/vector/Vector Databases - A Practical Introduction - Nitin Borwankar.pdf` |
| **D06** | Orchestration & Governance | `12-orchestration-layer.pdf` | `library/04-data-engineering/pipelines/Data Pipelines with Apache Airflow, 2nd Edition - Bas Harenslak and Julian de Ruiter.pdf`<br>`library/09-sre-observability/observability/Fundamentals of Data Observability - Andy Petrella.pdf` |
| **A01–A04** | Track 03: AI & ML Engineering | `FSDS-EDAI-DSAI-syllabus.md` | `library/07-ai-ml/mlops-evaluation/Designing Machine Learning Systems - Chip Huyen.pdf`<br>`library/07-ai-ml/generative-ai/AI Engineering - Building Applications with Foundation Models - Chip Huyen.pdf`<br>`library/07-ai-ml/generative-ai/LLM Engineer's Handbook - Paul Iusztin and Maxime Labonne.pdf`<br>`library/07-ai-ml/agents/Building Effective AI Agents - Anthropic.pdf` |
| **P01–P09** | Track 04: Distributed & Cloud Platform | `FSDS-EDAI-DSAI-syllabus.md` | `library/02-software-architecture/distributed-systems/Designing Data-Intensive Applications - Martin Kleppmann.pdf`<br>`library/02-software-architecture/cloud-native/Kubernetes in Action, 2nd Edition - Marko Luksa.pdf`<br>`library/03-cloud-platforms/iac/Terraform Up and Running 3rd Edition - Yevgeniy Brikman (2022).pdf`<br>`library/09-sre-observability/Site Reliability Engineering - Google.pdf`<br>`library/09-sre-observability/observability/Observability Engineering - Charity Majors, Liz Fong-Jones and George Miranda.pdf` |

---

## PHẦN 2: QUY TRÌNH TỰ ĐỘNG KHÉP KÍN CHO AGENT KHI NGƯỜI DÙNG GỌI `@prompt.md`

> **Kích hoạt tự động (Zero-Friction Local Trigger — Không cần Copy-Paste từ Gemini Web)**:
> Bất cứ khi nào người dùng gắn thẻ **`@prompt.md`** (dù chỉ gõ 1 câu ngắn như *"@prompt.md Xây dựng học phần F02 hoàn chỉnh"* hay dán ghi chú thô), Agent tại Local **BẮT BUỘC** tự động đọc trực tiếp Slide PDF trong `docs/` + Sách gốc trong `library/`, điều phối **1 Chặng = 1 Subagent độc lập** (để mỗi chặng có trọn vẹn ngữ cảnh thiết kế sâu nhất), và thực thi tuần tự 6 bước dưới đây để tích hợp vào **Anthropic Academy CDS v2**.

### Bước 0: Kiến trúc Tách File Bài học (`Externalized Stage HTML`), Điều phối Subagent & Quy chuẩn `Trạm 0.0 Executive Blueprint`

1. **Cơ chế Điều phối Subagent tại Local (`1 Chặng = 1 Subagent`)**:
   - Khi xây dựng một học phần mới hoặc nhiều chặng cùng lúc, Agent chính trích xuất mục lục và nội dung từ Slide PDF (`docs/<slide>.pdf`) cùng các chương sách đối chiếu trong `library/` bằng script Python local (`pypdf`/`pdfplumber`), lập **Blueprint Toàn Học phần** (nhân vật chính xuyên suốt, ma trận các Chặng & Trạm, danh sách Visual 4 tầng), sau đó khởi chạy **Subagent riêng cho từng Chặng (`stage-1.html` .. `stage-N.html`)** để tránh giới hạn token đầu ra và đạt độ sâu tối đa.
2. **Cấu trúc Lưu trữ Tách rời (`content/lessons/<CODE>/stage-<N>.html`)**:
   - Toàn bộ nội dung bài học được lưu thành từng file HTML độc lập theo từng Chặng tại `content/lessons/<CODE>/stage-<N>.html` (ví dụ: [`content/lessons/F01/stage-1.html`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/content/lessons/F01/stage-1.html), [`content/lessons/D02/stage-1.html`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/content/lessons/D02/stage-1.html)).
   - Trong file `stage-<N>.html`, sử dụng 3 thẻ custom nội bộ được trình biên dịch [`compile_lesson_templates_js()`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/scripts/build_hub.py#L322-L368) chuyển đổi tự động:
     - `<x-spine id="..." badge="TRONG BÀI HỌC NÀY · <CODE>" title="..." subtitle="...">Tóm tắt 1–2 câu...</x-spine>`: Khung xương sống đầu bài.
     - `<x-infra2d></x-infra2d>` *(hoặc widget mô phỏng 2D tương tác của học phần)*: Hộp cát mô phỏng tương tác 2D trực tiếp bằng HTML/CSS/JS/SVG.
     - `<x-figure id="..." key="<diagram_key>" title="...">Caption mô tả cơ chế sắc gọn (bắt buộc không được để trống)...</x-figure>`: Thẻ Visual đa lớp màu & chuyển động Durdraw.
   - Khi mở khóa một Học phần mới (ví dụ `F02`, `F04`, `D01`...), đăng ký học phần đó tại 4 vị trí trong [`scripts/build_hub.py`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/scripts/build_hub.py):
     1. Hàm sinh sơ đồ `build_<topic>_diagrams()` (kiểm định bằng `verify_diagram()`) và mô phỏng 2D (nếu có).
     2. Danh sách `_LESSON_FUNC_SPECS` và `LESSON_RENDERERS`.
     3. Mảng `SYLLABUS_GROUPS` (bật `hasContent: true`, cập nhật `contentNote: "Chặng 1–N"`, giữ mô tả `modules` và `lab` tiếng Việt cô đọng 1 dòng cho thẻ `#/catalog`).
     4. Cấu hình `TOPIC_CONFIG[<CODE>]` và `HUB_DATA.topics[<CODE>]` (`swatch`, `mask`, `pictogram`, `heroSvg`, `stages`, `objectives`, `pdf`, `title`, `subtitle`).

3. **Quy chuẩn `Trạm 0.0 Executive Blueprint` ở đầu `stage-1.html` (Cấm lặp ý 3–4 lần)**:
   - Không viết đoạn `<p>` liệt kê danh sách sách tham khảo dài dòng ở dòng 1 (vì Hero Header của trang đã hiển thị đầy đủ tên học phần, link Slide PDF và lộ trình Chặng).
   - `Trạm 0.0` ở đầu `stage-1.html` chỉ gồm đúng **3 khối tinh gọn**:
     1. `<x-spine>` + **1 đoạn văn xuôi ngắn (3–4 câu)** giới thiệu Nhân vật chính kỹ thuật xuyên suốt học phần.
     2. **Sơ đồ Mental Map (`<x-figure>`)** thể hiện mạch Nhân – Quả qua các Chặng.
     3. **Bảng Ma trận Kiến trúc Toàn Học phần (`<table class="clean-table">`)** đối chiếu `Chặng & Trạm | Trọng tâm Slide & Sách | Điểm nghẽn khởi phát | Cơ chế giải quyết`.
   - **Cấm tuyệt đối** viết thêm các danh sách `<ul>` dài dòng lặp lại nội dung đã nằm trong `<x-spine>`, `<x-figure>` và `<table class="clean-table">`.

### Bước 1: Biên tập Chuẩn Claude Academy Editorial (`BLUF`, `Invisible Scaffolding`, `Zero Metaphor Bloat`)

Mọi Trạm kiến thức (`<h2>Trạm X.Y: ...</h2>`) trong `content/lessons/<CODE>/stage-<N>.html` phải tuân thủ giải phẫu **Claude Station Anatomy** gồm 3 phần liền mạch:

1. **Phần Mở đầu Trạm — Luận điểm BLUF & Điểm nghẽn Vật lý (1–2 đoạn `<p>` văn xuôi mạch lạc)**:
   - **Câu đầu tiên (BLUF)**: Nêu thẳng định nghĩa bản chất hoặc quy luật cơ học cốt lõi của trạm kèm số liệu định lượng.
   - **Các câu tiếp theo**: Đặt Nhân vật chính vào điểm nghẽn vật lý từ trạm trước (tại sao cách cũ thất bại khi quy mô tăng hoặc gặp sự cố?), kết hợp tối đa **1–2 câu ẩn dụ sắc lẹm** (nếu cần).
   - **Cấm tuyệt đối**:
     - Cấm chia nhỏ phần mở đầu thành hàng loạt thẻ `<h3>1. Bối cảnh...</h3>`, `<h3>2. Nỗi đau...</h3>`, `<h3>3. Sơ đồ...</h3>`, `<h3>4. Đúc kết...</h3>`.
     - Cấm biến toàn bộ trạm thành một danh sách `<ul><li><strong>[Bối cảnh & Ẩn dụ đời thực]:</strong>...` mang tính lắp ghép công thức.
     - Cấm để lại bất kỳ nhãn nội bộ nào như `[Bổ sung Chuyên sâu +30% — Slide...]`, `(Bước 0 — ...)`, hay `(Tương ứng Mục 01/... trong Slide...)`.

2. **Phần Visual Trung tâm (`<x-infra2d>` + `<x-figure>` + `<table class="clean-table">` + `<pre><code>`) — Chiếm 60% diện tích hiển thị**:
   - Mọi `<x-figure>` bắt buộc có nội dung caption súc tích giải thích điểm cốt lõi cần nhìn trên sơ đồ.
   - Mọi bảng dữ liệu dùng `<div class="table-wrap"><table class="clean-table">...</table></div>`.
   - Phần chữ xung quanh **không liệt kê lại** những gì đã vẽ trong sơ đồ hoặc bảng (`Zero Visual-Prose Echo`).

3. **Phần Đúc kết Cơ học & Cầu nối Chuyển giao (Cuối mỗi Trạm & Cuối mỗi Chặng)**:
   - Cuối mỗi Trạm: Viết **1 đoạn văn xuôi sắc gọn** (hoặc khối `<div class="callout">`) tổng kết sự đánh đổi kỹ thuật (**Engineering Trade-off**) và đặt câu hỏi cơ học dẫn sang Trạm kế tiếp.
   - Cuối mỗi Chặng: Khép lại bằng `<section class="summary-section" id="..."><h2...>Tóm tắt bỏ túi Chặng X &amp; Checklist 5 câu hỏi bản chất</h2><ol>...</ol><p>...</p></section>`.

### Bước 2: Thiết kế Hệ thống Visual 4 Tầng (`4-Layer Visual Architecture` — Không phải ASCII đơn sắc thuần túy)

Hệ thống Visual của FSDS Learning Hub là sự kết hợp của **4 tầng đồ họa & tương tác hiện đại** (loại bỏ hoàn toàn các tab `Picture`/`Mermaid` tĩnh rườm rà cũ, đảm bảo `0 live Picture/Mermaid bloat` trong [`scripts/validate.py`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/scripts/validate.py)):

1. **Tầng 1 — Đồ họa Vector CDS, Bảng màu 21-Stop OKLab, Mặt nạ SVG & Huy hiệu Học thuật (`TOPIC_CONFIG`, `content/pictograms.json`, `assets/masks/*.svg`)**:
   - Mỗi Học phần sở hữu bộ nhận diện thị giác riêng theo chuẩn **Anthropic Creative Design System (CDS)**: bảng màu chủ đạo (`swatch-cactus`, `swatch-peach`, `swatch-heather`, `swatch-oat`, `swatch-sky`, `swatch-fig`), mặt nạ họa tiết nền SVG (`loops.svg`, `swoops.svg`, `threads.svg`, `strata.svg`, `vines.svg`, `snowflake.svg`), biểu tượng Vector 2 lớp (`highlight` + `line` trong [`content/pictograms.json`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/content/pictograms.json) kết xuất qua `renderPictogramSvg()`), huy hiệu con dấu học thuật (`renderBadgeSealHtml()`), thẻ xếp chồng (`renderContentThumbHtml()`), và đồ họa `heroSvg` `120×120` trên Hero Banner.

2. **Tầng 2 — Hộp cát Mô phỏng Tương tác 2D & State-Machine (`<x-infra2d>` / `.infra2d-wrap`)**:
   - Đối với các chủ đề phân biệt kiến trúc hệ thống hoặc mô phỏng luồng trạng thái (như bài phân biệt Bare Metal, Shared Hosting, VPS, Cloud HA, Dedicated Server, Docker Container, Serverless trong [`F06/stage-1.html`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/content/lessons/F06/stage-1.html) được kết xuất bởi [`buildInfra2DSimulatorHtml()`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/scripts/build_hub.py#L3284-L3645) và [`renderInfra2DSimStage()`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/scripts/build_hub.py#L4682-L5485)), hệ thống nhúng trực tiếp **Interactive 2D Simulator bằng HTML/CSS/JS + SVG**.
   - Người học trực tiếp bấm nút kích hoạt kịch bản (cắt máy chủ bằng Hypervisor, bắn DDoS gây lỗi `503 Noisy Neighbor`, làm cháy bo mạch chủ `SPOF`, bật `Live Migration + Auto-Scaling`, đua tốc độ khởi động 1 giây giữa VM và Docker, dùng Bộ lọc Tư vấn Kiến trúc). Khi xây dựng học phần mới, Agent tại Local có đầy đủ năng lực viết thêm các bộ mô phỏng 2D tương tác tương tự ngay trong [`scripts/build_hub.py`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/scripts/build_hub.py).

3. **Tầng 3 — Khung Xương sống Kiến trúc (`<x-spine>`), Bảng Ma trận Định lượng (`.clean-table`) & Khối Callout (`.callout`)**:
   - Mở đầu mỗi Chặng bằng thẻ `<x-spine>` (`buildSpineHeroBanner()`) định vị rõ bài toán cốt lõi, đi kèm các bảng ma trận đối chiếu đa chiều (`.clean-table`) và hộp phân tích đánh đổi kỹ thuật (`.callout`, `.callout.warn`).

4. **Tầng 4 — Thẻ Sơ đồ Đa Lớp Màu (`<x-figure>` + `scripts/ascii_engine/painter.py`, `dur_loader.py`, `content/ascii-art/*.dur`)**:
   - Khác hoàn toàn với ASCII trắng đen thuần túy: mọi sơ đồ `<x-figure>` được đóng gói trong thẻ cửa sổ macOS (`.visual-card`) với thanh công cụ 2 nút tinh gọn (`Sao chép` bảo toàn 100% hình học gốc và `Phóng to` toàn màn hình `openExpandModal`), kết xuất qua **Headless Monodraw + Durdraw Engine**:
     - **Kiểm định Hình học Tuyệt đối (`scripts/ascii_diagram.py`)**: Dùng `make_box`, `join_horizontal`, `pad_center`, `pad_right` (`strict=True`, Unicode NFC) và đi qua `verify_diagram(ascii_text, diagram_id, kind=...)` (`0` tràn khung, `0` lệch cột).
     - **Tách 8 Lớp Màu Ngữ nghĩa (`scripts/ascii_engine/painter.py`)**: Tự động phân tích cú pháp hình học để tô 8 lớp màu chuẩn WCAG AA trên cả nền Sáng/Tối và 6 bảng màu (`ac-border`, `ac-shadow`, `ac-header`, `ac-flow`, `ac-ok`, `ac-warn`, `ac-danger`, `ac-muted`).
     - **Định dạng `.dur` (`content/ascii-art/*.dur`)**: Tự động xuất dữ liệu màu & hình học chuẩn `.dur` phục vụ lưu trữ và kiểm định tự động.

### Bước 3: Quét Từ điển Tự động (`scripts/glossary_scanner.py`) & Kết nối Centered AI Glossary Modal + `FSDS_TTL_CACHE`

1. **Quét & Phân loại 100% Thuật ngữ (`unclassified_count == 0`)**:
   - Mọi cụm từ in đậm (`<strong>`) mang tính kỹ thuật và mã nội dòng (`<code>`) trong các file `content/lessons/<CODE>/stage-<N>.html` đều được [`scripts/glossary_scanner.py`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/scripts/glossary_scanner.py) quét tự động.
   - Khi thêm bài học mới có thuật ngữ/công nghệ mới, bổ sung mục từ chuẩn (`canonical entry` gồm `title`, `category`, `intuition`, `mechanism`, `example`, `related`) vào `RAW_GLOSSARY` hoặc quy tắc ánh xạ vào `PATTERN_RULES` / `SKIP_EXACT` trong [`scripts/glossary_scanner.py`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/scripts/glossary_scanner.py) để giữ vững `0 unclassified terms`.

2. **Tích hợp Tự động với Centered Anthropic AI Modal (`#glossaryPopover`) & `FSDS_TTL_CACHE`**:
   - Khi người dùng bấm vào bất kỳ `.glossary-term` nào trong bài viết, bấm vào thẻ trong `#/glossary`, hoặc nhập bất kỳ thuật ngữ/framework tự do nào vào ô hỏi AI, hệ thống mở **Popup chuẩn Anthropic cố định chính giữa màn hình** (`top: 50%; left: 50%; transform: translate(-50%, -50%)`).
   - Popup tự động gọi Google AI Studio (`gemini-3-flash-preview` / `gemini-2.5-flash`) để sinh phân tích chuyên sâu 4 phần (*1. Bản chất cốt lõi*, *2. Cơ chế hoạt động nội tại*, *3. Ví dụ thực tế & Code minh họa*, *4. Cạm bẫy & Kinh nghiệm thực chiến*) và lưu bền vững vào [`FSDS_TTL_CACHE`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/scripts/build_hub.py#L4691-L4737) (`Memory Map` + `localStorage` + `IndexedDB`, TTL 30 ngày — mở lại đạt `0ms`).
   - **Bảo mật Credential**: Khóa API Google AI Studio chỉ được lưu trong file `.env.local` (đã chặn bởi `.gitignore`) và được [`_build_ai_vault()`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/scripts/build_hub.py#L14-L42) băm XOR thành mảng số nguyên khi build; tuyệt đối không bao giờ ghi khóa thô vào bất kỳ file nào được Git theo dõi.

### Bước 4: Chuẩn Tương thích Đa Ngôn Ngữ (`VI ↔ EN` AI Auto-Translate), 6 Bảng Màu & Bộ Font Tiếng Việt Anthropic CDS

Để tính năng chuyển ngữ tự động `VI ↔ EN` ([`translateActiveViewToEnglish()`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/scripts/build_hub.py#L7458-L7535)) và bộ font `Anthropic*-Vietnamese-*.woff2` hoạt động hoàn hảo 100% trên mọi bài học mới:

1. **Quy tắc Đánh dấu HTML Tương thích Dịch tự động (`VI ↔ EN`)**:
   - Luôn bọc mọi câu lệnh CLI, tên hàm, tên biến, đường dẫn tệp (`/var/log/app.log`), tên bảng/cột SQL và cờ lệnh (`-lh`, `--hard`) vào trong thẻ `<code>...</code>`. Engine dịch AI được lập trình giữ nguyên 100% nội dung bên trong `<code>` và `<pre>` trong khi dịch mượt mà toàn bộ văn xuôi tiếng Việt bên ngoài sang tiếng Anh học thuật (và lưu vào `FSDS_TTL_CACHE`).
   - Không lồng `<ul>`, `<ol>`, `<table>`, hay `<pre>` vào bên trong thẻ `<p>`. Sử dụng các thẻ chuẩn `.prose p`, `.prose li`, `h2`, `h3`, `.callout-title`, `.visual-caption`.

2. **Quy tắc Hệ thống Font chữ Anthropic CDS & Tiếng Việt**:
   - Văn bản thân bài và các nhãn UI chữ hoa tiếng Việt (`.rail-section-heading`, `.page-toc-header`, `.catalog-kicker`, `.glossary-pop-meta`, `.stage-pills-label`) bắt buộc dùng `var(--cds-font-sans)` (`Anthropic Sans` kèm bộ glyph tiếng Việt đầy đủ).
   - Tiêu đề lớn (`H1`, `H2`, `.catalog-card h3`, `.glossary-pop-title`) dùng `var(--cds-font-serif)` (`Anthropic Serif` kèm bộ glyph tiếng Việt đầy đủ).
   - Khung sơ đồ `pre.ascii-diagram` dùng `var(--cds-font-mono)` nghiêm ngặt để bảo toàn độ rộng cột đơn cách; các khối code chú thích ngắn (`.glossary-pop-code`, `.glossary-dict-code`) dùng `"anthropic-mono", "anthropic-sans", ui-monospace, monospace` để comment tiếng Việt hiển thị trọn vẹn dấu.

### Bước 5: Biên dịch, Kiểm định 5 Lớp (Desktop + Tablet + Mobile Chrome `390×844`) & Đẩy lên GitHub Pages

1. **Chạy Chuỗi Lệnh Build & Kiểm định Bắt buộc**:
   ```bash
   .venv/bin/python3 -B scripts/glossary_scanner.py && \
   .venv/bin/python3 -B scripts/build_hub.py && \
   .venv/bin/python3 -B scripts/validate.py
   ```
   Lệnh trên sẽ biên dịch đồng bộ ra cả [`index.html`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/index.html), [`fsds-learning-hub.html`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/fsds-learning-hub.html), [`content/lessons-data.json`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/content/lessons-data.json), [`content/glossary-data.json`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/content/glossary-data.json) và kiểm tra tự động:
   - `Negative self-tests: 6/6`
   - `JS syntax: valid`
   - `Runtime DOM QA (Playwright): toàn bộ các trang bài học + #/catalog + #/glossary trên 3 viewports (1440×900 Desktop, 768×1024 Tablet, 390×844 Mobile Chrome — đảm bảo overflowX == 0)`
   - `Anthropic Academy CDS Typography: verified`
   - `Glossary Scanner: 0 unclassified terms`
   - `Colored ASCII checks: 100% char + 100% geometry`
   - `Quarantine verified: 0 live Picture/Mermaid bloat`
   - `Anti-slop audit: clean`

2. **Quét Bảo mật (`Secret Scan`) & Đẩy lên GitHub Pages (`origin/main`)**:
   - Chỉ `git add` đích danh các file của task (tuyệt đối không `git add .` hoặc stage `.env.local`).
   - Quét bảo mật trước khi commit:
     ```bash
     ! git diff --cached | grep -qE "AQ\.Ab8|AIza" && echo "STAGED_SECRET_SCAN_CLEAN=1"
     ```
   - Commit và đẩy lên `origin/main` để kích hoạt workflow [`.github/workflows/pages.yml`](file:///Users/MAC/Documents/FSDS-EDAI-DSAI/.github/workflows/pages.yml) cập nhật trực tiếp lên GitHub Pages.
