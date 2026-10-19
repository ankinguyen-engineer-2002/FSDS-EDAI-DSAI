#!/usr/bin/env python3
"""
Canonical Blueprint Seed Bank, 7-Tier Career Rank Matrix, and JD Competency Profiles
for the FSDS · EDAI · DSAI AI Adaptive Practice & Career Mastery Arena.
"""
from __future__ import annotations

import json
from pathlib import Path

CAREER_RANKS = [
    {
        "tier": 1,
        "id": "student",
        "title": "Sinh viên",
        "enTitle": "Student",
        "badgeCode": "T1 · STUDENT",
        "xpThreshold": 0,
        "minTopicsMastered": 0,
        "minMasteryPct": 0,
        "minL3Passed": 0,
        "complexityMultiplier": 1.0,
        "xpMultiplier": 1.0,
        "summary": "Nắm vững khái niệm nền tảng, phân biệt đúng bản chất công cụ và chạy được các thao tác cơ bản.",
        "tierDirective": (
            "Cấp độ Sinh viên (Tier 1/7): Tập trung vào 1 cơ chế cốt lõi duy nhất, ngữ cảnh rõ ràng, "
            "bẫy distractor là các hiểu lầm nhập môn phổ biến. Không ghép nhiều lỗi chồng chéo."
        ),
        "jdExpectations": {
            "DE": "Hiểu mô hình OLTP vs OLAP, viết được lệnh Linux CLI, truy vấn SQL SELECT/JOIN cơ bản và phân biệt CSV với Parquet.",
            "AIE": "Hiểu cấu trúc HTTP/REST API, JSON schema, khái niệm LLM token, context window và gọi API suy luận cơ bản.",
            "MLE": "Nắm vững Đại số tuyến tính, Xác suất thống kê, tránh Data Leakage giữa tập Train/Test và dùng được NumPy/Pandas/Scikit-learn."
        }
    },
    {
        "tier": 2,
        "id": "intern",
        "title": "Intern",
        "enTitle": "Engineering Intern",
        "badgeCode": "T2 · INTERN",
        "xpThreshold": 300,
        "minTopicsMastered": 1,
        "minMasteryPct": 60,
        "minL3Passed": 1,
        "complexityMultiplier": 1.15,
        "xpMultiplier": 1.2,
        "summary": "Theo dõi được luồng dữ liệu đi qua một thành phần hệ thống, đọc được log lỗi và viết được script/test chuẩn.",
        "tierDirective": (
            "Cấp độ Intern (Tier 2/7): Đưa vào 1 đoạn log, câu lệnh CLI/SQL hoặc cấu hình thực tế. "
            "Yêu cầu người học lần theo luồng thực thi từng bước để chỉ ra nguyên nhân lỗi."
        ),
        "jdExpectations": {
            "DE": "Đóng gói được ứng dụng bằng Dockerfile, viết script Bash/Python thu thập dữ liệu có quản lý môi trường ảo (uv/venv) và xử lý ngoại lệ.",
            "AIE": "Xây dựng endpoint FastAPI có kiểm định kiểu dữ liệu Pydantic, kết nối Vector DB cơ bản và viết pytest tự động.",
            "MLE": "Thực hiện EDA bài bản, xử lý Missing Values/Outliers, huấn luyện mô hình Baseline (Linear/Logistic Regression, Decision Tree) và đọc ROC-AUC."
        }
    },
    {
        "tier": 3,
        "id": "fresher",
        "title": "Fresher",
        "enTitle": "Fresher Engineer",
        "badgeCode": "T3 · FRESHER",
        "xpThreshold": 900,
        "minTopicsMastered": 2,
        "minMasteryPct": 68,
        "minL3Passed": 2,
        "complexityMultiplier": 1.35,
        "xpMultiplier": 1.45,
        "summary": "Kết nối được 2–3 thành phần (API + DB + Docker, hoặc Kafka + Spark + Lakehouse) và phòng tránh được các bẫy cấu hình mặc định.",
        "tierDirective": (
            "Cấp độ Fresher (Tier 3/7): Đặt bài toán ở ranh giới tương tác giữa 2 thành phần hệ thống "
            "(ví dụ Python App gọi PostgreSQL, hoặc Airflow điều phối Spark). Kiểm tra các bẫy cấu hình mặc định gây treo hoặc tràn RAM."
        ),
        "jdExpectations": {
            "DE": "Hiểu cơ chế WAL/MVCC trong PostgreSQL, thiết kế bảng Star Schema (Fact/Dim, SCD Type 2) và viết DAG Airflow có tính lũy đẳng (Idempotent).",
            "AIE": "Triển khai pipeline RAG có Chunking/Hybrid Search, xử lý bất đồng bộ (asyncio) không làm nghẽn Event Loop trên FastAPI/Uvicorn.",
            "MLE": "Áp dụng Feature Engineering (Big Five), tối ưu Ensemble (Random Forest, XGBoost, LightGBM) và kiểm định chéo K-Fold không rò rỉ dữ liệu."
        }
    },
    {
        "tier": 4,
        "id": "junior",
        "title": "Junior",
        "enTitle": "Junior Engineer",
        "badgeCode": "T4 · JUNIOR",
        "xpThreshold": 2000,
        "minTopicsMastered": 3,
        "minMasteryPct": 72,
        "minL3Passed": 4,
        "complexityMultiplier": 1.6,
        "xpMultiplier": 1.75,
        "summary": "Vận hành đường ống Production ổn định, đọc hiểu kế hoạch thực thi (EXPLAIN ANALYZE / Spark UI) và thiết kế cơ chế chịu lỗi.",
        "tierDirective": (
            "Cấp độ Junior (Tier 4/7): Yêu cầu phân tích số liệu định lượng (độ trễ, IOPS, kích thước Row Group, Consumer Lag) "
            "và chọn phương án tối ưu hóa hoặc khôi phục sự cố đảm bảo SLA."
        ),
        "jdExpectations": {
            "DE": "Chẩn đoán Data Skew & Disk Spill trên Spark UI, vận hành CDC với Debezium + Kafka không mất sự kiện, và thiết lập cổng kiểm định Great Expectations/Deequ.",
            "AIE": "Tối ưu thông lượng phục vụ LLM (Continuous Batching, KV Cache, PagedAttention trên vLLM), thiết lập Guardrails và đo lường bằng RAGAS.",
            "MLE": "Triển khai Feature Store (Feast) chống Training-Serving Skew với Point-in-Time ASOF Join, đóng gói model serving chịu tải cao."
        }
    },
    {
        "tier": 5,
        "id": "middle",
        "title": "Middle",
        "enTitle": "Middle Engineer",
        "badgeCode": "T5 · MIDDLE",
        "xpThreshold": 3800,
        "minTopicsMastered": 5,
        "minMasteryPct": 78,
        "minL3Passed": 6,
        "complexityMultiplier": 1.9,
        "xpMultiplier": 2.1,
        "summary": "Tự chủ thiết kế hệ thống phân tán End-to-End, cân bằng đánh đổi giữa Độ trễ — Chi phí — Tính nhất quán và xử lý sự cố đa tầng.",
        "tierDirective": (
            "Cấp độ Middle (Tier 5/7): Đưa vào ràng buộc mâu thuẫn (ngân sách giới hạn vs SLA độ trễ thấp vs dữ liệu lệch tải nặng). "
            "Các phương án nhiễu đều hợp lý ở quy mô nhỏ nhưng sẽ gãy ở quy mô Production."
        ),
        "jdExpectations": {
            "DE": "Làm chủ nội tại Open Table Formats (Delta Lake / Apache Iceberg / Hudi: OCC, Copy-on-Write vs Merge-on-Read, Z-Ordering/Liquid Clustering) và Flink Stateful Streaming (RocksDB, Watermark, Chandy-Lamport Checkpoint).",
            "AIE": "Thiết kế hệ thống Multi-Agent có kiểm soát trạng thái, Semantic Caching, Rate Limiting theo Token Budget và quan sát toàn trình (OpenTelemetry/Langfuse).",
            "MLE": "Tinh chỉnh mô hình sâu (LoRA/QLoRA, DPO/RLHF), nén mô hình (Quantization/Distillation) và giám sát Data/Concept Drift trên Production."
        }
    },
    {
        "tier": 6,
        "id": "senior",
        "title": "Senior",
        "enTitle": "Senior Engineer",
        "badgeCode": "T6 · SENIOR",
        "xpThreshold": 6800,
        "minTopicsMastered": 8,
        "minMasteryPct": 82,
        "minL3Passed": 9,
        "complexityMultiplier": 2.25,
        "xpMultiplier": 2.6,
        "summary": "Giải quyết các bài toán quy mô cực lớn (TB–PB, 100.000+ sự kiện/giây), bảo toàn dữ liệu tuyệt đối trước thảm họa dây chuyền.",
        "tierDirective": (
            "Cấp độ Senior (Tier 6/7): Đặt tình huống sự cố dây chuyền (Cascading Failure) hoặc giới hạn vật lý/định lý phân tán (CAP/PACELC, Lock Contention, Write Amplification, Split-Brain). "
            "Đòi hỏi tư duy nguyên lý gốc (First-Principles) để bóc tách nguyên nhân sâu xa và kiến trúc phòng thủ nhiều lớp."
        ),
        "jdExpectations": {
            "DE": "Kiến trúc Lakehouse & Streaming toàn trình đạt Exactly-Once End-to-End (Kafka 2PC + Flink + Iceberg/Delta), tối ưu hóa FinOps giảm 50–70% chi phí Cloud & điều tra sự cố cấp độ Kernel/Storage.",
            "AIE": "Tối ưu tầng GPU & LLM Serving độ trễ cực thấp (Speculative Decoding, FlashAttention, FP8/INT4 Quantization, Kubernetes KServe/vLLM Autoscaling).",
            "MLE": "Thiết kế hạ tầng huấn luyện phân tán đa GPU (PyTorch DDP/FSDP, All-Reduce), tối ưu hóa nhân tính toán bằng CUDA / OpenAI Triton và kiến trúc hệ thống ML quy mô triệu người dùng."
        }
    },
    {
        "tier": 7,
        "id": "senior_plus",
        "title": "Senior+",
        "enTitle": "Staff / Principal Architect",
        "badgeCode": "T7 · SENIOR+ / STAFF",
        "xpThreshold": 11500,
        "minTopicsMastered": 10,
        "minMasteryPct": 88,
        "minL3Passed": 12,
        "complexityMultiplier": 2.7,
        "xpMultiplier": 3.2,
        "summary": "Kiến trúc sư trưởng định hình nền tảng Data & AI toàn doanh nghiệp, thiết lập Data Governance, Data Contracts và chiến lược tiến hóa hệ thống.",
        "tierDirective": (
            "Cấp độ Senior+ / Staff Architect (Tier 7/7): Kiểm tra các phản ví dụ (khi nào một Best Practice nổi tiếng lại gây thảm họa), "
            "bài toán chuyển đổi kiến trúc 0-downtime giữa các thế hệ nền tảng, quản trị đa nhóm (Multi-tenant Governance, Data Contracts, FinOps) và tối ưu hóa sát phần cứng."
        ),
        "jdExpectations": {
            "DE": "Hoạch định kiến trúc Data Platform cấp tập đoàn (Medallion + Data Mesh/Contract + Unity Catalog/DataHub), đảm bảo tuân thủ GDPR/PII, tiến hóa lược đồ và khả năng phục hồi thảm họa đa vùng.",
            "AIE": "Kiến trúc nền tảng AI Gateway & Agentic Platform dùng chung cho toàn công ty: cô lập bảo mật, điều phối lưu lượng đa mô hình, kiểm toán an toàn (Constitutional AI / Red-teaming) và tối ưu chi phí hạ tầng triệu đô.",
            "MLE": "Dẫn dắt nghiên cứu & triển khai kiến trúc mô hình mới, viết nhân GPU Triton tùy chỉnh vượt giới hạn Memory-Bandwidth (Roofline Model) và định chuẩn MLOps toàn tổ chức."
        }
    },
]

PRACTICE_LEVELS = [
    {
        "level": 1,
        "code": "L1",
        "title": "Level 1 · Nền tảng & Cơ chế Gốc",
        "enTitle": "Level 1 · Foundation & Core Mechanics",
        "formatBadge": "Trắc nghiệm Phản hồi Tức thì",
        "baseXp": 45,
        "desc": "Kiểm tra trực diện nguyên lý vật lý, cơ chế vận hành nội tại và mối quan hệ Nhân – Quả. Chọn đáp án xong biết ngay Đúng/Sai kèm giải phẫu từng phương án nhiễu."
    },
    {
        "level": 2,
        "code": "L2",
        "title": "Level 2 · Chuyên sâu & Giải phẫu Sự cố",
        "enTitle": "Level 2 · Production Trade-offs & Debugging",
        "formatBadge": "Trắc nghiệm Tình huống & Log/Code",
        "baseXp": 85,
        "desc": "Đặt bạn vào tình huống vận hành thực tế với đoạn Log, cấu hình, SQL/Code hoặc bảng thông số tải. Đòi hỏi chẩn đoán đúng điểm nghẽn và chọn giải pháp chuẩn xác."
    },
    {
        "level": 3,
        "code": "L3",
        "title": "Level 3 · Phỏng vấn Thực chiến Kết hợp",
        "enTitle": "Level 3 · Hybrid System Design & AI Defense",
        "formatBadge": "Trắc nghiệm + Tự luận (AI Chấm Bản Chất)",
        "baseXp": 160,
        "desc": "Kết hợp chọn quyết định kiến trúc (Phần A) và trình bày lập luận/trade-off bằng lời của bạn (Phần B). AI Semantic Grader chấm điểm theo bản chất cốt lõi, không bắt bẻ câu chữ máy móc."
    },
]

MUTATION_DOMAINS = [
    {"id": "ecom_flash", "name": "Sàn TMĐT Flash Sale 11/11 (Đơn hàng #8888, 85.000 req/s)", "scale": "85.000 đơn/giây, đỉnh tải gấp 25 lần ngày thường"},
    {"id": "fintech_ledger", "name": "Ngân hàng Số & Thanh toán Tức thời (Core Banking Ledger)", "scale": "120 triệu giao dịch/ngày, cam kết RPO = 0 và độ trễ p99 < 15ms"},
    {"id": "iot_telemetry", "name": "Mạng lưới Cảm biến Nhà máy & Đội xe Thông minh (IIoT Telemetry)", "scale": "500.000 thiết bị bắn gói tin mỗi giây, mạng 4G chập chờn gây trễ sự kiện"},
    {"id": "adtech_stream", "name": "Nền tảng Đấu giá Quảng cáo Thời gian thực (Real-Time Bidding)", "scale": "300.000 sự kiện clickstream/giây, tổng hợp ngân sách theo cửa sổ trượt"},
    {"id": "ai_rag_cloud", "name": "Hệ thống Trợ lý AI Doanh nghiệp & Phục vụ LLM (Enterprise RAG)", "scale": "15.000 người dùng đồng thời, kho 80 triệu vector và SLA phản hồi < 1.2 giây"},
    {"id": "med_analytics", "name": "Hệ thống Hồ sơ Bệnh án & Phân tích Dược sinh học (HealthTech Lakehouse)", "scale": "450 TB dữ liệu lịch sử, kiểm toán HIPAA/GDPR nghiêm ngặt"},
]

# ==============================================================================
# CANONICAL BLUEPRINT BANK FOR ALL 12 FULL-PROSE COURSES + SYLLABUS TRACKS
# ==============================================================================
ARENA_BLUEPRINTS = [
    # --------------------------------------------------------------------------
    # F01 · LINUX FUNDAMENTALS
    # --------------------------------------------------------------------------
    {
        "id": "F01-BP-01",
        "topic": "F01",
        "stage": 1,
        "stationId": "linux-1-3",
        "stationTitle": "Trạm 1.3: Giải phẫu Căn bếp Linux — Hành trình 7 bước của lệnh grep",
        "roleTracks": ["DE", "AIE", "MLE"],
        "skillName": "Kernel Space vs. User Space, System Calls & Process Lifecycle (fork/execve)",
        "invariant": (
            "Tiến trình ở User Space tuyệt đối không được đọc/ghi thẳng xuống ổ cứng vật lý; "
            "Shell phải nhân bản tiến trình qua fork(), nạp mã máy qua execve(), và gọi System Call (openat, read, write) "
            "để Kernel (Ring 0) kiểm tra quyền trên Inode rồi đọc qua Page Cache trên RAM."
        ),
        "misconceptions": [
            "Tưởng rằng lệnh grep tự mình điều khiển đầu đọc ổ cứng SSD mà không cần đi qua Linux Kernel.",
            "Nhầm lẫn giữa Program (file nhị phân nằm im trên đĩa tốn 0% RAM) và Process (tiến trình đang chạy trên RAM có PID).",
            "Cho rằng lệnh thực thi trực tiếp trong tiến trình Bash hiện tại mà không tạo tiến trình con qua fork()/execve()."
        ],
        "L1": {
            "stem": (
                "Khi kỹ sư gõ lệnh `grep ERROR /var/log/app.log` trên Terminal và nhấn Enter, "
                "cơ chế nào diễn ra ở tầng Hệ điều hành để biến tệp `/bin/grep` trên ổ đĩa thành tiến trình đang quét dữ liệu?"
            ),
            "options": [
                "Bash gọi `fork()` để nhân bản tiến trình con, dùng `execve()` nạp mã máy `/bin/grep`, sau đó tiến trình gọi System Call (`openat`, `read`, `write`) để nhờ Kernel (Ring 0) đọc các khối dữ liệu từ đĩa lên RAM.",
                "Trình mô phỏng Terminal trực tiếp biên dịch mã nguồn C của `grep` ngay trên CPU và tự điều khiển bus NVMe SSD để đọc tệp `/var/log/app.log` mà không làm phiền Linux Kernel.",
                "Linux Kernel tự động chép toàn bộ thư mục `/var/log` vào bộ nhớ đệm L1 CPU Cache ngay khi bật máy nên `/bin/grep` đọc thẳng từ thanh ghi CPU không cần System Call.",
                "Bash nạp `/bin/grep` như một hàm nội bộ (built-in) chạy chung cùng một mã định danh `PID` với trình thông dịch Shell hiện hành để tiết kiệm bộ nhớ."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo đúng hành trình 7 bước tại Trạm 1.3: `grep` là một chương trình độc lập (`/bin/grep`). "
                "Shell phải gọi `fork()` tạo tiến trình con (cấp `PID` mới), gọi `execve()` nạp mã thực thi, và mọi thao tác chạm vào tệp `app.log` "
                "đều phải đi qua cửa khẩu System Call để Kernel kiểm tra quyền trên Inode và đọc qua bộ nhớ đệm RAM."
            ),
            "distractorReasons": [
                "Đúng bản chất cơ học UNIX/Linux (fork -> execve -> syscall -> Kernel Ring 0).",
                "Sai: Terminal chỉ hiển thị ký tự, và không một tiến trình User Space nào được phép chọc thẳng vào bus ổ cứng.",
                "Sai: L1 Cache chỉ vài chục KB, không thể chứa cả thư mục `/var/log`, và việc mở tệp vẫn bắt buộc qua System Call.",
                "Sai: `grep` là binary ngoài (`/bin/grep`), không phải shell built-in như `cd`, nên bắt buộc sinh tiến trình con có `PID` riêng."
            ]
        },
        "L2": {
            "stem": (
                "Trên máy chủ Production chạy đường ống thu thập log, kỹ sư chạy một kịch bản gọi lệnh xử lý tệp liên tục "
                "và bất ngờ nhận lỗi hệ thống: `OSError: [Errno 24] Too many open files` (hoặc `Too many open files in system`). "
                "Dưới góc độ Hồ sơ Căn cước Process (`task_struct`) tại Trạm 2.1 và Triết lý Inode tại Trạm 2.2, nguyên nhân gốc và cách chẩn đoán chuẩn xác nhất là gì?"
            ),
            "codeSnippet": (
                "$ ls -l /proc/18492/fd | wc -l\n"
                "1024\n"
                "$ ulimit -n\n"
                "1024"
            ),
            "options": [
                "Tiến trình `PID 18492` mở tệp/socket qua System Call `open()` nhưng quên đóng (`close()`), làm cạn sạch bảng File Descriptor (`fd`) bị chặn trần bởi `ulimit -n` (1024); cần sửa rò rỉ tài nguyên (dùng `with` / `close()`) kết hợp cấu hình `LimitNOFILE` hợp lý.",
                "Ổ cứng vật lý `/dev/sda` đã hết sạch dung lượng lưu trữ byte dữ liệu nên Linux Kernel từ chối tạo thêm tệp mới; cần xóa bớt tệp trong `/tmp`.",
                "Biến môi trường `$PATH` của tiến trình bị thiếu đường dẫn `/usr/sbin` khiến Kernel không tìm thấy trình điều khiển ổ cứng.",
                "Cây thư mục `/proc/18492` chiếm quá nhiều dung lượng trên ổ cứng SSD (vượt quá 10 GB) làm tràn phân vùng gốc `/`."
            ],
            "correctIndex": 0,
            "explanation": (
                "Mỗi tiến trình có bảng `Open Files` (File Descriptor Table) lưu trong hồ sơ căn cước. "
                "Khi mở tệp/kết nối mạng mà không đóng, số lượng cổng `fd` chạm trần `ulimit -n` (1024) gây lỗi `Errno 24`. "
                "Lưu ý: `/proc` là hệ thống tệp ảo trên RAM (0 MB trên đĩa cứng)."
            ),
            "distractorReasons": [
                "Chẩn đoán chính xác từ đầu ra `/proc/18492/fd` (1024 cổng đang mở chạm trần `ulimit -n`).",
                "Sai: Hết dung lượng đĩa sinh lỗi `ENOSPC (No space left on device - Errno 28)`, không phải `EMFILE (Errno 24)`.",
                "Sai: `$PATH` chỉ dùng để tìm chương trình thực thi khi gõ tên lệnh, không liên quan đến giới hạn File Descriptor.",
                "Sai: `/proc` là Virtual Filesystem nằm trên RAM do Kernel sinh động, chiếm 0 byte trên đĩa cứng."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Phỏng vấn Thực chiến: Bạn viết script `/opt/pipeline/run_etl.sh` chạy hoàn hảo khi gõ tay trên Terminal SSH. "
                "Nhưng khi đưa vào `crontab` để tự động chạy lúc `02:00` sáng hàng ngày với dòng cấu hình:\n"
                "`0 2 * * * /opt/pipeline/run_etl.sh > /var/log/etl.log`\n"
                "Sáng hôm sau kiểm tra, bảng đích trống rỗng VÀ tệp `/var/log/etl.log` cũng rỗng `0 byte`, khiến đội vận hành mù tịt không biết lỗi gì."
            ),
            "mcqPrompt": "Phần A (Quyết định Kỹ thuật): Đâu là tổ hợp nguyên nhân gốc rễ giải thích cả việc script thất bại lẫn việc tệp log bị rỗng 0 byte?",
            "options": [
                "Cron khởi chạy với môi trường tối giản (`PATH=/usr/bin:/bin`, thư mục đứng là `$HOME`) khiến lệnh trong script không tìm thấy công cụ/đường dẫn tương đối; đồng thời `> /var/log/etl.log` chỉ chuyển hướng (redirect) cổng `stdout (fd 1)` còn toàn bộ thông báo lỗi chảy ra cổng `stderr (fd 2)` đã bị vứt bỏ vì thiếu `2>&1`.",
                "Daemon `crond` mặc định không có quyền ghi vào thư mục `/var/log` và tự động xóa nội dung tệp log nếu lệnh trả về mã thoát khác 0.",
                "Cú pháp `0 2 * * *` trong Crontab có nghĩa là chạy vào ngày mùng 2 hàng tháng chứ không phải 2 giờ sáng hàng ngày.",
                "Đường ống `>` trong Linux chỉ hoạt động khi có người dùng đang mở màn hình Terminal trực tiếp (Interactive TTY)."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Bảo vệ Thiết kế & Vận hành): Hãy viết lại dòng cấu hình Crontab + các nguyên tắc phòng thủ bên trong file `run_etl.sh` "
                "(về Shebang, biến môi trường, đường dẫn, điều hướng cổng 1 & 2, và kiểm tra mã thoát) để đường ống chạy tự động 24/7 không bao giờ bị 'mù lỗi' hoặc chạy sai ngữ cảnh."
            ),
            "rubric": {
                "coreConcepts": [
                    "Gộp luồng lỗi chuẩn vào đầu ra chuẩn bằng `>> /var/log/etl.log 2>&1` (hoặc điều hướng cả fd 1 và fd 2) để không mất thông báo lỗi.",
                    "Khai báo tường minh `#!/usr/bin/env bash` (hoặc `#!/bin/bash`), `set -euo pipefail`, và thiết lập `PATH` hoặc dùng đường dẫn tuyệt đối (Absolute Path) cho mọi lệnh/tệp.",
                    "Chuyển thư mục làm việc tường minh (`cd /opt/pipeline`) hoặc định vị theo thư mục chứa script trước khi chạy."
                ],
                "tradeoffs": [
                    "Dùng `>>` (O_APPEND) kèm cơ chế xoay vòng log (logrotate) hoặc ghi kèm timestamp thay vì `>` (O_TRUNC) làm mất lịch sử các lần chạy trước.",
                    "Giải thích rủi ro nếu job chạy lâu hơn chu kỳ cron (cần cơ chế khóa `flock` hoặc chuyển sang Orchestrator như Airflow khi phụ thuộc phức tạp)."
                ],
                "referenceAnswer": (
                    "1. Sửa Crontab thành: `0 2 * * * /opt/pipeline/run_etl.sh >> /var/log/etl.log 2>&1` để nối đuôi (`>>`) cả `stdout (1)` lẫn `stderr (2)` vào tệp log.\n"
                    "2. Đầu file `run_etl.sh` bắt buộc có Shebang `#!/usr/bin/env bash`, bật `set -euo pipefail` để dừng ngay khi có lệnh lỗi, khai báo tường minh `export PATH=/usr/local/bin:/usr/bin:/bin` và `cd /opt/pipeline` (dùng đường dẫn tuyệt đối cho mọi tệp/binary).\n"
                    "3. Bổ sung `flock -n /tmp/etl.lock` để chống chồng lấn tiến trình (overlapping runs) nếu lần chạy trước chưa xong."
                )
            }
        }
    },

    # --------------------------------------------------------------------------
    # F02 · PYTHON FUNDAMENTALS
    # --------------------------------------------------------------------------
    {
        "id": "F02-BP-01",
        "topic": "F02",
        "stage": 1,
        "stationId": "python-1-1",
        "stationTitle": "Trạm 1.1–4.2: CPython PyObject, Bảng Băm O(1), Context Manager & Asyncio Event Loop",
        "roleTracks": ["DE", "AIE", "MLE"],
        "skillName": "CPython Memory (PyObject/GC), Hash Table O(1), Streaming File I/O & Asyncio Non-blocking Concurrency",
        "invariant": (
            "CPython quản lý bộ nhớ qua Reference Counting (`ob_refcnt`) kết hợp Cyclic GC; "
            "tra cứu trên `set`/`dict` đạt O(1) nhờ bảng băm trong khi `list` là O(n); "
            "đọc tệp lớn phải duyệt theo dòng (Streaming Iterator) trong khối `with` để giữ RAM O(1); "
            "và trong hàm `async def`, mọi thao tác I/O chặn (như `requests.get` hay `time.sleep`) sẽ làm đóng băng toàn bộ Event Loop đơn luồng."
        ),
        "misconceptions": [
            "Dùng `f.read()` hoặc `f.readlines()` để nạp tệp log 50 GB trên máy chủ chỉ có 8 GB RAM.",
            "Tưởng rằng chỉ cần thêm từ khóa `async def` phía trước hàm chứa `requests.get()` là chương trình tự động chạy bất đồng bộ.",
            "Dùng `x in visited_list` bên trong vòng lặp 1 triệu phần tử khiến độ phức tạp vọt lên O(N^2)."
        ],
        "L1": {
            "stem": (
                "Trong trình thu thập dữ liệu `crawler.py`, bạn cần kiểm tra xem một `url` mới có nằm trong tập hợp 2.000.000 URL đã quét hay chưa. "
                "Tại sao lưu danh sách URL đã quét bằng `set` (hoặc khóa của `dict`) lại nhanh hơn hàng chục nghìn lần so với dùng `list`?"
            ),
            "options": [
                "`set` và `dict` tính giá trị băm `hash(url)` để nhảy thẳng tới ô nhớ trong Bảng băm (Hash Table) với độ phức tạp trung bình `O(1)`, trong khi `url in list` phải duyệt tuần tự từng phần tử từ đầu đến cuối với độ phức tạp `O(n)`.",
                "Vì `set` được CPython lưu trữ trực tiếp trong thanh ghi L1 Cache của CPU, còn `list` bắt buộc phải lưu trên ổ cứng SSD.",
                "Vì các phần tử trong `set` được tự động sắp xếp theo thứ tự bảng chữ cái ABC nên CPython dùng thuật toán tìm kiếm nhị phân `O(log n)`.",
                "Vì `set` bỏ qua cơ chế đếm tham chiếu `ob_refcnt` của `PyObject` nên không tốn thời gian quản lý bộ nhớ."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 2.2 (F02): `list` là mảng động các con trỏ (`O(n)` khi tìm kiếm), còn `set`/`dict` là bảng băm (`Hash Table`) "
                "dùng hàm băm để định vị ô nhớ trong thời gian hằng số `O(1)`. Kiểm tra 2 triệu lần trên `list` tốn tới ~2×10^12 phép so sánh (`O(N^2)`)."
            ),
            "distractorReasons": [
                "Chính xác: Bảng băm O(1) vs Quét mảng động O(n).",
                "Sai: Cả `set` và `list` đều là các cấu trúc `PyObject` nằm trên vùng nhớ Heap của RAM.",
                "Sai: `set` trong Python là bảng băm không có thứ tự sắp xếp từ điển, không phải cây tìm kiếm nhị phân.",
                "Sai: Mọi đối tượng trong CPython đều là `PyObject` và đều chịu sự quản lý của `ob_refcnt`."
            ]
        },
        "L2": {
            "stem": (
                "Một kỹ sư viết dịch vụ thu thập 500 trang web bằng `asyncio` như đoạn code bên dưới, "
                "nhưng khi chạy thực tế thì tổng thời gian vẫn mất đúng 500 giây (chạy tuần tự từng trang một) thay vì hoàn tất trong ~2 giây. "
                "Nguyên nhân cơ học chính xác nằm ở đâu?"
            ),
            "codeSnippet": (
                "import asyncio, requests\n\n"
                "async def fetch_page(url: str) -> int:\n"
                "    resp = requests.get(url, timeout=5)  # Mỗi trang mất 1 giây\n"
                "    return len(resp.text)\n\n"
                "async def main(urls: list[str]):\n"
                "    return await asyncio.gather(*(fetch_page(u) for u in urls))"
            ),
            "options": [
                "Thư viện `requests.get()` thực hiện Blocking Socket I/O thuần túy và không có điểm nhường quyền (`await`), khiến luồng duy nhất của `asyncio` Event Loop bị khóa cứng 1 giây ở mỗi URL; phải chuyển sang trình khách bất đồng bộ như `httpx.AsyncClient` hoặc `aiohttp`.",
                "Do `asyncio.gather()` chỉ chạy tuần tự từng coroutine một; phải đổi sang vòng lặp `for u in urls: await fetch_page(u)` thì mới chạy song song.",
                "Do Global Interpreter Lock (GIL) của Python cấm mọi chương trình mở nhiều hơn 1 kết nối mạng TCP cùng lúc.",
                "Do hàm `fetch_page` trả về kiểu `int` thay vì đối tượng `Future` nên Event Loop tự động hủy chế độ chạy song song."
            ],
            "correctIndex": 0,
            "explanation": (
                "Event Loop của `asyncio` chạy trên một luồng đơn (Single Thread) dựa trên cơ chế hợp tác (Cooperative Multitasking). "
                "Khi gọi `requests.get()`, luồng bị chặn cứng ở tầng OS socket mà không trả quyền điều khiển về Event Loop qua `await`. "
                "Phải dùng `async with httpx.AsyncClient() as client: resp = await client.get(url)`."
            ),
            "distractorReasons": [
                "Chính xác: Blocking I/O bên trong coroutine làm đông cứng toàn bộ Event Loop.",
                "Sai: Ngược lại, `for u in urls: await fetch_page(u)` mới là chạy tuần tự, còn `asyncio.gather()` chạy đồng thời nếu bên trong dùng non-blocking `await`.",
                "Sai: GIL chỉ khóa thực thi bytecode CPU song song, không cấm mở hàng nghìn non-blocking network sockets qua `epoll`/`kqueue`.",
                "Sai: Mọi hàm `async def` khi gọi đều trả về đối tượng Coroutine hợp lệ cho `asyncio.gather`."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Thiết kế Pipeline Python: Bạn cần viết một tiến trình đọc tệp nhật ký giao dịch `transactions_raw.jsonl` nặng `64 GB` trên một container chỉ được cấp giới hạn `memory.max = 512 MB RAM`, "
                "lọc ra các giao dịch hợp lệ, gọi API định giá ngoại tệ cho từng lô 100 giao dịch, và ghi kết quả xuống tệp đích mà không được làm sập container vì OOM hay rò rỉ File Descriptor khi gặp dòng JSON lỗi."
            ),
            "mcqPrompt": "Phần A (Quyết định Kiến trúc): Tổ hợp kỹ thuật Python nào đảm bảo container dùng dưới 100 MB RAM và đạt thông lượng mạng tối đa?",
            "options": [
                "Mở tệp nguồn và tệp đích bằng Context Manager (`with open(...)`), đọc từng dòng qua File Iterator / Generator (`for line in src_file:`), gom lô 100 bản ghi vào bộ đệm nhỏ rồi dùng `asyncio.gather` + `httpx.AsyncClient` (kèm `asyncio.Semaphore`) để gọi API đồng thời.",
                "Dùng `lines = open('transactions_raw.jsonl').readlines()` để nạp toàn bộ danh sách dòng vào RAM rồi chia cho 16 tiến trình `multiprocessing.Pool` xử lý.",
                "Đọc toàn bộ tệp vào `pandas.read_json('transactions_raw.jsonl', lines=True)` rồi dùng hàm `.apply(requests.get)` trên từng dòng.",
                "Viết vòng lặp `while True` mở tệp mới ở mỗi dòng mà không đóng tệp để tránh mất con trỏ vị trí đọc."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Bảo vệ Thiết kế & Xử lý Ngoại lệ): Hãy giải thích: (1) Cơ chế hoạt động của giao thức Context Manager (`__enter__` / `__exit__`) và File Iterator giúp giữ RAM phẳng `O(1)` như thế nào? "
                "(2) Cách bạn bắt ngoại lệ cụ thể (`json.JSONDecodeError`, `httpx.TimeoutException`) và dùng `asyncio.Semaphore` ra sao để vừa không nuốt lỗi hệ thống vừa không bắn sập API đối tác?"
            ),
            "rubric": {
                "coreConcepts": [
                    "Giải thích đúng Lazy Evaluation / Streaming Iterator: đọc từng dòng từ bộ đệm trang, xử lý xong dòng cũ thì `ob_refcnt` về 0 và được giải phóng ngay, giữ mức tiêu thụ RAM hằng số O(1) (< 100 MB dù tệp 64 GB).",
                    "Giải thích đúng giao thức Context Manager (`with`): đảm bảo `__exit__` luôn đóng File Descriptor (`close()`) và đóng kết nối mạng ngay cả khi xảy ra ngoại lệ giữa chừng.",
                    "Giới hạn mức độ đồng thời bằng `asyncio.Semaphore(N)` kết hợp bắt ngoại lệ cụ thể (`json.JSONDecodeError` đẩy sang Dead-Letter log, `httpx.RequestError` thử lại có Exponential Backoff) thay vì `except Exception: pass`."
                ],
                "tradeoffs": [
                    "Nêu rõ đánh đổi kích thước lô (Batch size) và giới hạn Semaphore: số luồng async quá lớn sẽ gây lỗi `429 Too Many Requests` hoặc cạn cổng socket, quá nhỏ thì lãng phí băng thông I/O."
                ],
                "referenceAnswer": (
                    "1. Dùng `with open(...)` kích hoạt `__enter__` khi vào khối và luôn gọi `__exit__` để giải phóng File Descriptor bất kể có lỗi hay không; duyệt `for line in f:` dùng cơ chế Lazy Iterator chỉ giữ 1 dòng/lô nhỏ trên RAM (sau mỗi vòng lặp `ob_refcnt` giảm về 0 và bộ nhớ được thu hồi ngay), giữ RAM phẳng < 50 MB cho tệp 64 GB.\n"
                    "2. Bắt riêng `json.JSONDecodeError` để ghi dòng hỏng vào tệp `quarantine.log` mà không làm dừng cả tiến trình (tuyệt đối không dùng bare `except:` che khuất `MemoryError`/`KeyboardInterrupt`).\n"
                    "3. Dùng `asyncio.Semaphore(20)` kết hợp `httpx.AsyncClient` tái sử dụng Connection Pool để giới hạn tối đa 20 request đồng thời, tránh đánh sập dịch vụ tỷ giá hoặc dính rate-limit 429."
                )
            }
        }
    },

    # --------------------------------------------------------------------------
    # F03 · DATABASE FUNDAMENTALS (POSTGRESQL)
    # --------------------------------------------------------------------------
    {
        "id": "F03-BP-01",
        "topic": "F03",
        "stage": 2,
        "stationId": "db-2-2",
        "stationTitle": "Trạm 2.2 & 3.2: Slotted Page 8KB, WAL, MVCC Snapshot Isolation & B-Tree Index",
        "roleTracks": ["DE", "AIE", "MLE"],
        "skillName": "PostgreSQL Storage Internals (8KB Slotted Page, WAL), MVCC Dead Tuples & Query Optimization",
        "invariant": (
            "PostgreSQL lưu dữ liệu theo trang 8KB Slotted Page, đảm bảo tính bền vững (Durability) bằng cách ghi tuần tự vào Write-Ahead Log (WAL) trước khi flush Dirty Page; "
            "khi UPDATE một dòng, MVCC không ghi đè tại chỗ mà đánh dấu `xmax` lên bản ghi cũ (thành Dead Tuple) và chèn một bản ghi mới (`xmin`), "
            "đòi hỏi tiến trình Autovacuum phải dọn dẹp để tránh phình bảng (Table Bloat)."
        ),
        "misconceptions": [
            "Tưởng rằng lệnh `UPDATE orders SET status = 'PAID'` sửa trực tiếp các byte tại đúng vị trí cũ trên trang 8KB mà không sinh thêm bản ghi mới.",
            "Cho rằng gắn B-Tree Index lên mọi cột hoặc bọc hàm `WHERE EXTRACT(YEAR FROM created_at) = 2026` trên cột có Index thường vẫn dùng được Index Scan.",
            "Tưởng rằng `shared_buffers` hay `work_mem` cứ đặt càng to bằng 100% RAM máy chủ thì truy vấn chạy càng nhanh."
        ],
        "L1": {
            "stem": (
                "Trong PostgreSQL, khi giao dịch `txid = 500` thực hiện câu lệnh `UPDATE orders SET amount = 15000000 WHERE order_id = 8888;`, "
                "cơ chế Đa phiên bản (MVCC — Multi-Version Concurrency Control) xử lý bản ghi trên trang `8KB Slotted Page` như thế nào?"
            ),
            "options": [
                "PostgreSQL không ghi đè lên bản ghi cũ mà gán `xmax = 500` vào Tuple cũ (biến nó thành Dead Tuple sau khi commit) và ghi thêm một Tuple hoàn toàn mới có `xmin = 500` chứa giá trị mới, giúp các giao dịch đang đọc đồng thời vẫn thấy ảnh chụp nhất quán mà không bị khóa (Readers don't block Writers).",
                "PostgreSQL khóa cứng toàn bộ bảng `orders` (Table-level Exclusive Lock), xóa trắng trang 8KB trên ổ cứng SSD rồi ghi lại từ đầu.",
                "PostgreSQL chỉ sửa giá trị trong bộ nhớ `work_mem` của phiên làm việc và không bao giờ ghi xuống tệp WAL.",
                "PostgreSQL tự động chạy lệnh `VACUUM FULL` ngay bên trong mỗi câu lệnh `UPDATE` để thu hồi không gian đĩa tức thì."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 3.2 (F03): MVCC trong PostgreSQL duy trì tính cô lập giao dịch không khóa đọc bằng cách giữ phiên bản cũ (`xmax = 500`) "
                "và tạo phiên bản mới (`xmin = 500`). Các bản ghi cũ (`Dead Tuples`) sẽ được `Autovacuum` thu hồi không gian sau khi không còn giao dịch nào tham chiếu tới."
            ),
            "distractorReasons": [
                "Đúng chuẩn cơ học MVCC của PostgreSQL (`xmin`/`xmax` + Snapshot Isolation + Dead Tuple).",
                "Sai: `UPDATE` chỉ giữ Row-level lock trên dòng đích, không khóa toàn bảng và không xóa trắng trang 8KB.",
                "Sai: Dữ liệu trang nằm trong `shared_buffers` (không phải `work_mem`) và mọi thay đổi bắt buộc ghi vào `WAL Buffer` -> tệp WAL trên đĩa khi commit.",
                "Sai: `VACUUM FULL` khóa độc quyền toàn bảng và tạo tệp mới rất nặng; PostgreSQL dùng `Autovacuum` chạy nền bất đồng bộ."
            ]
        },
        "L2": {
            "stem": (
                "Bảng `orders` có 50 triệu dòng và đã được tạo chỉ mục B-Tree chuẩn `CREATE INDEX idx_orders_created_at ON orders(created_at);`. "
                "Tuy nhiên, khi chạy truy vấn báo cáo bên dưới, `EXPLAIN ANALYZE` lại báo `Seq Scan` quét toàn bộ 50 triệu dòng mất 14.2 giây. "
                "Tại sao B-Tree Index bị vô hiệu hóa và cách sửa nào giữ nguyên kết quả nhưng chuyển về `Index Scan` (< 15ms)?"
            ),
            "codeSnippet": (
                "EXPLAIN ANALYZE\n"
                "SELECT order_id, total_amount\n"
                "FROM orders\n"
                "WHERE DATE_TRUNC('day', created_at) = DATE '2026-10-19';"
            ),
            "options": [
                "Bọc hàm `DATE_TRUNC('day', created_at)` quanh cột được đánh chỉ mục làm biến đổi giá trị gốc khiến bộ tối ưu truy vấn không thể dò trên cây B-Tree (Non-SARGable predicate); cần viết lại thành khoảng nửa mở `WHERE created_at >= '2026-10-19 00:00:00' AND created_at < '2026-10-20 00:00:00'`.",
                "Do B-Tree Index trong PostgreSQL chỉ hỗ trợ kiểu số nguyên `INTEGER` chứ không hỗ trợ kiểu thời gian `TIMESTAMP`.",
                "Do thiếu từ khóa `DISTINCT` ngay sau `SELECT` nên bộ tối ưu hóa bắt buộc phải quét tuần tự.",
                "Cần đổi sang chỉ mục `Hash Index` vì `B-Tree` không thể tìm kiếm theo điều kiện bằng (`=`)."
            ],
            "correctIndex": 0,
            "explanation": (
                "Cây B-Tree sắp xếp các giá trị gốc của cột `created_at`. Khi bọc hàm lên cột (`f(col) = const`), PostgreSQL phải tính giá trị hàm cho từng dòng trong bảng (`Seq Scan`). "
                "Chuyển sang điều kiện khoảng `created_at >= ... AND created_at < ...` (SARGable) giúp nhảy thẳng vào nhánh lá của cây B-Tree."
            ),
            "distractorReasons": [
                "Chính xác: Biến đổi biểu thức thành SARGable range predicate để tận dụng thứ tự sắp xếp của B-Tree.",
                "Sai: B-Tree hỗ trợ mọi kiểu dữ liệu có thứ tự so sánh (`<`, `<=`, `=`, `>=`, `>`), bao gồm `TIMESTAMP`.",
                "Sai: Thêm `DISTINCT` không giúp kích hoạt Index mà còn tốn thêm bước Sort/Hash Aggregate.",
                "Sai: B-Tree hỗ trợ cả phép so sánh bằng (`=`) lẫn truy vấn khoảng (`RANGE`), và bọc hàm trên cột thì Hash Index cũng bị vô hiệu hóa tương tự."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Sự cố Database Production: Hệ thống thanh toán chạy PostgreSQL 16 chịu tải `4.000 UPDATE/giây` trên bảng `wallets`. "
                "Sau 3 ngày chạy chiến dịch khuyến mãi, dung lượng bảng `wallets` phình từ `4 GB` lên `92 GB` dù số lượng ví hoạt động không đổi (10 triệu ví), "
                "đồng thời độ trễ truy vấn tăng gấp 12 lần và chỉ số `Disk Spill` xuất hiện dày đặc trong các truy vấn `ORDER BY / HASH JOIN`."
            ),
            "mcqPrompt": "Phần A (Chẩn đoán Cốt lõi): Cặp nguyên nhân cơ học nào dẫn đến đồng thời hiện tượng bảng phình 92 GB và truy vấn bị tràn đĩa (Disk Spill)?",
            "options": [
                "Tải `UPDATE` cao liên tục sinh ra hàng trăm triệu `Dead Tuples` (MVCC) nhưng có một giao dịch đọc treo dài hạn (`idle in transaction`) hoặc cấu hình `autovacuum` quá chậm khiến không gian trang 8KB không được tái sử dụng (Table Bloat); đồng thời thông số `work_mem` đặt quá thấp khiến các phép Sort/Hash Join vượt ngưỡng phải tràn xuống tệp tạm trên đĩa.",
                "Do PostgreSQL quên xóa tệp Write-Ahead Log (`WAL`) trong thư mục `base/` và bộ nhớ `shared_buffers` bị cấu hình lớn hơn dung lượng ổ cứng.",
                "Do bảng `wallets` thiếu khóa ngoại (`Foreign Key`) nên mỗi lệnh `UPDATE` tự động nhân bản toàn bộ bảng sang phân vùng mới.",
                "Do chỉ mục B-Tree tự động chuyển đổi định dạng lưu trữ từ Row-oriented sang Columnar Parquet khi vượt quá 10 triệu dòng."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Phác đồ Xử lý & Tối ưu hóa): Hãy trình bày phác đồ giải cứu hệ thống theo 3 bước: "
                "(1) Kiểm tra và xử lý tận gốc nguyên nhân chặn `Autovacuum` + tinh chỉnh tham số vacuum cho bảng nóng `wallets`; "
                "(2) Thu hồi dung lượng 92 GB về lại 4 GB mà KHÔNG làm khóa chết bảng (Zero-downtime); "
                "(3) Cách tính và tinh chỉnh `work_mem` an toàn mà không làm máy chủ sập OOM khi có 200 kết nối đồng thời."
            ),
            "rubric": {
                "coreConcepts": [
                    "Kiểm tra `pg_stat_activity` để ngắt các phiên `idle in transaction` / truy vấn treo giữ `xmin` horizon ngăn Autovacuum dọn Dead Tuples; giảm `autovacuum_vacuum_scale_factor` (ví dụ xuống 0.01–0.02) và tăng `autovacuum_vacuum_cost_limit` riêng cho bảng `wallets` (+ tận dụng HOT Update nếu cột update không nằm trong index).",
                    "Giải thích tại sao KHÔNG chạy `VACUUM FULL` giờ cao điểm (vì giữ `ACCESS EXCLUSIVE LOCK` chặn cả đọc lẫn ghi); thay vào đó dùng `pg_repack` để tái cấu trúc bảng online không khóa.",
                    "Công thức an toàn cho `work_mem`: mỗi truy vấn phức tạp có thể cấp phát nhiều vùng `work_mem` cho từng toán tử Sort/Hash trên mỗi kết nối (`max_connections × operations_per_query × work_mem`), nên cần đặt mức vừa phải toàn cục (VD 16–64MB) hoặc `SET LOCAL work_mem` theo phiên kèm Connection Pooler (PgBouncer)."
                ],
                "tradeoffs": [
                    "Phân biệt rõ `VACUUM` thường (chỉ đánh dấu không gian Dead Tuple trong Free Space Map để tái sử dụng nội bộ, không trả dung lượng về cho OS) với `VACUUM FULL` / `pg_repack`."
                ],
                "referenceAnswer": (
                    "1. Truy vấn `pg_stat_activity` và `pg_stat_user_tables` để diệt các phiên `idle in transaction` giữ khóa `xmin`, đồng thời hạ `autovacuum_vacuum_scale_factor = 0.01` cho bảng `wallets` và bỏ các Index dư thừa trên cột số dư để kích hoạt cơ chế `HOT (Heap-Only Tuple) Update`.\n"
                    "2. Tuyệt đối không dùng `VACUUM FULL` trên Production đang chạy vì nó khóa độc quyền toàn bảng; dùng công cụ `pg_repack` để dựng bảng gọn mới và tráo đổi nguyên tử với thời gian khóa chỉ vài mili-giây.\n"
                    "3. Quan sát `temp_files` / `EXPLAIN (ANALYZE, BUFFERS)` (`Sort Method: external merge Disk`) để tăng `work_mem`, nhưng phải đặt qua PgBouncer hoặc `SET LOCAL work_mem = '64MB'` cho riêng truy vấn báo cáo vì RAM tối đa có thể bị nhân theo `active_queries × hash_sort_nodes × work_mem`."
                )
            }
        }
    },

    # --------------------------------------------------------------------------
    # F04 · WEB API (HTTP, REST/GRPC/GRAPHQL, AUTH, FASTAPI)
    # --------------------------------------------------------------------------
    {
        "id": "F04-BP-01",
        "topic": "F04",
        "stage": 4,
        "stationId": "api-4-1",
        "stationTitle": "Trạm 2.1–5.2: REST vs. gRPC, JWT/OAuth2, K8s Liveness/Readiness & FastAPI ASGI",
        "roleTracks": ["DE", "AIE", "MLE"],
        "skillName": "API Architecture Styles, Kubernetes Health Probes (Liveness/Readiness) & FastAPI Event Loop Mechanics",
        "invariant": (
            "Liveness Probe kiểm tra tiến trình có bị kẹt chết (deadlock) để khởi động lại Pod, còn Readiness Probe kiểm tra dịch vụ đã sẵn sàng nhận tải chưa (ví dụ nạp xong mô hình ML hay kết nối DB) để rút/đưa Pod vào Load Balancer; "
            "nếu đặt kiểm tra DB hoặc nạp model nặng vào Liveness Probe sẽ gây bão khởi động lại dây chuyền (Cascading Restart Storm)."
        ),
        "misconceptions": [
            "Nhét câu lệnh kiểm tra kết nối PostgreSQL hoặc kiểm tra trạng thái nạp mô hình LLM 14GB vào chung cổng `/health/liveness`.",
            "Tưởng rằng mã hóa Base64 phần Payload của JWT giúp ẩn giấu thông tin bí mật không ai đọc được.",
            "Khai báo hàm `async def` trong FastAPI nhưng bên trong lại chạy tác vụ tính toán CPU nặng hoặc gọi thư viện đồng bộ làm đơ toàn bộ Worker."
        ],
        "L1": {
            "stem": (
                "Trong kiến trúc xác thực bằng `JWT (JSON Web Token)` gồm 3 phần `Header.Payload.Signature`, "
                "điều gì xảy ra nếu một người dùng phía trình duyệt tự ý giải mã Base64Url phần `Payload`, sửa trường `\"role\": \"user\"` thành `\"role\": \"admin\"`, rồi gửi lại Token đó lên máy chủ API?"
            ),
            "options": [
                "Máy chủ API dùng khóa bí mật (hoặc Public Key với RS256) tính toán lại chữ ký mật mã từ `Header + Payload_mới`; vì kết quả không khớp với phần `Signature` đi kèm nên máy chủ lập tức từ chối Token với mã lỗi `401 Unauthorized`.",
                "Máy chủ API sẽ cấp quyền `admin` nếu kẻ tấn công biết cách mã hóa lại chuỗi JSON sang đúng chuẩn Base64Url.",
                "Trình duyệt không thể đọc được nội dung bên trong `Payload` của JWT vì Base64Url là thuật toán mã hóa bất đối xứng.",
                "Máy chủ API phải tra cứu toàn bộ nội dung `Payload` trong bảng `sessions` của PostgreSQL ở mọi request thì mới phát hiện được."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 3.3 (F04): `Header` và `Payload` của JWT chỉ được mã hóa hiển thị bằng `Base64Url` (ai cũng đọc được nên cấm nhét mật khẩu vào đó), "
                "nhưng tính toàn vẹn (Integrity) được bảo vệ tuyệt đối bởi phần `Signature` ký bằng `HMAC-SHA256` hoặc `RSA/ECDSA`."
            ),
            "distractorReasons": [
                "Chính xác: Chữ ký số (Signature) phát hiện ngay lập tức mọi hành vi sửa đổi dù chỉ 1 bit trong Header hoặc Payload.",
                "Sai: Không có khóa bí mật (`Secret Key` / `Private Key`) trên server thì không thể tạo ra chữ ký `Signature` hợp lệ.",
                "Sai: Base64Url chỉ là phép biến đổi bảng mã văn bản (Encoding), không phải mã hóa bảo mật (Encryption).",
                "Sai: Ưu điểm cốt lõi của JWT là xác thực phi trạng thái (Stateless verification) thông qua chữ ký mật mã."
            ]
        },
        "L2": {
            "stem": (
                "Đội AI triển khai dịch vụ suy luận mô hình bằng FastAPI trên Kubernetes. Mô hình nặng `8 GB` cần `45 giây` để nạp vào VRAM khi khởi động. "
                "Họ cấu hình `livenessProbe` gọi vào cổng `/healthz` với `initialDelaySeconds: 10`, `periodSeconds: 5`, `failureThreshold: 3`, "
                "và bên trong `/healthz` kiểm tra cả biến `is_model_loaded` lẫn kết nối tới cơ sở dữ liệu PostgreSQL. "
                "Hậu quả gì sẽ xảy ra trên môi trường Production?"
            ),
            "codeSnippet": (
                "@app.get('/healthz')\n"
                "def healthcheck():\n"
                "    if not is_model_loaded or not db.ping():\n"
                "        raise HTTPException(status_code=503)\n"
                "    return {'status': 'ok'}"
            ),
            "options": [
                "Sau 25 giây (`10s + 3×5s`), mô hình vẫn chưa nạp xong (cần 45s) nên `livenessProbe` báo thất bại và `kubelet` giết Pod khởi động lại vô tận (CrashLoopBackOff); hơn nữa nếu DB chập chờn 15 giây, toàn bộ dàn Pod sẽ đồng loạt tự sát gây bão khởi động lại dây chuyền (`Cascading Restart Storm`).",
                "Kubernetes sẽ tự động tăng dung lượng GPU VRAM gấp đôi mỗi khi thấy cổng `/healthz` trả về mã lỗi `503`.",
                "Pod vẫn khởi động bình thường vì `kubelet` luôn chờ mọi câu lệnh Python trong hàm `startup` chạy xong rồi mới bắt đầu tính giờ `livenessProbe`.",
                "Cổng `/healthz` viết bằng `def` thay vì `async def` nên FastAPI tự động trả về mã `200 OK` bỏ qua lệnh `raise HTTPException`."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 4.1 (F04): `Liveness Probe` chỉ được kiểm tra xem bản thân tiến trình web còn phản hồi hay đã deadlock; "
                "việc chờ nạp mô hình nặng và kiểm tra kết nối hạ nguồn (`DB/Redis`) bắt buộc phải tách sang `Startup Probe` và `Readiness Probe` "
                "(khi DB chậm, Readiness rút Pod khỏi Load Balancer chứ không giết Pod!)."
            ),
            "distractorReasons": [
                "Chính xác: Giải phẫu đúng 2 thảm họa kinh điển (CrashLoop khi nạp model chậm + Cascading Restart Storm khi DB chập chờn).",
                "Sai: Kubernetes không tự cấp thêm GPU VRAM khi probe thất bại.",
                "Sai: `kubelet` đếm giờ ngay khi container bắt đầu chạy, bất chấp ứng dụng bên trong đã nạp xong model hay chưa.",
                "Sai: Hàm `def` trong FastAPI chạy trên threadpool và vẫn ném `HTTPException(503)` như bình thường."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Thiết kế Hệ thống API Đa tầng: Bạn thiết kế hệ thống đặt đơn & gợi ý sản phẩm theo thời gian thực gồm: "
                "(1) Ứng dụng di động của khách hàng gọi lên cổng API Gateway, "
                "(2) Dịch vụ `Order-Service` gọi sang `Fraud-Scoring-ML-Service` nội bộ với yêu cầu độ trễ `< 8ms` ở tốc độ `25.000 RPS`, "
                "và (3) Màn hình theo dõi trạng thái giao hàng trực tiếp của khách."
            ),
            "mcqPrompt": "Phần A (Quyết định Giao thức): Tổ hợp giao thức nào tối ưu nhất cho từng chặng (1), (2), (3) kể trên?",
            "options": [
                "(1) REST/JSON (hoặc GraphQL cho màn hình tổng hợp nhiều nguồn) ở biên ngoài cho App di động; (2) gRPC (Protocol Buffers nhị phân trên HTTP/2 Multiplexing) cho giao tiếp nội bộ tốc độ cao giữa `Order-Service` và `Fraud-Scoring-ML-Service`; (3) Server-Sent Events (`SSE`) cho luồng đẩy trạng thái đơn hàng một chiều từ Server xuống Client.",
                "Dùng `SOAP XML` cho cả 3 chặng để đồng nhất định dạng văn bản.",
                "Dùng `Webhook` để ứng dụng di động của khách tự mở cổng lắng nghe kết nối ngược từ máy chủ.",
                "Dùng cơ chế `Short Polling` gọi REST API mỗi `10 mili-giây` từ triệu điện thoại khách hàng để cập nhật trạng thái đơn."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Bảo vệ Kiến trúc & Tối ưu FastAPI): Hãy giải thích: "
                "(1) Tại sao `gRPC (Protobuf + HTTP/2)` lại vượt trội hơn `REST/JSON` ở chặng gọi ML nội bộ (25.000 RPS)? "
                "(2) Trong FastAPI, quy tắc vàng khi nào dùng `async def` và khi nào dùng `def` thường là gì để tránh làm nghẽn Event Loop khi chạy suy luận ML?"
            ),
            "rubric": {
                "coreConcepts": [
                    "Giải thích ưu thế của gRPC: tuần tự hóa nhị phân Protocol Buffers nhỏ gọn (giảm 60–80% kích thước gói tin và CPU parse so với chuỗi JSON) + HTTP/2 Multiplexing ghép nhiều luồng RPC trên 1 kết nối TCP duy nhất không bị Head-of-Line blocking ở tầng ứng dụng.",
                    "Giải thích đúng cơ chế `async def` vs `def` trong FastAPI/Starlette: `async def` chạy trực tiếp trên luồng chính của Event Loop (chỉ dùng cho non-blocking I/O có `await`); còn `def` thường được Starlette tự động đẩy sang `anyio` external threadpool (hoặc dùng `ProcessPoolExecutor` / task queue cho tác vụ ML ngốn CPU).",
                    "Giải thích lý do chọn `SSE` thay vì `WebSocket` hoặc `Polling` cho thông báo trạng thái đơn hàng một chiều (nhẹ hơn, chạy chuẩn trên HTTP, tự động kết nối lại)."
                ],
                "tradeoffs": [
                    "Nêu rõ đánh đổi của gRPC: tệp nhị phân không đọc trực tiếp bằng mắt thường được như JSON và trình duyệt web không hỗ trợ đầy đủ nếu thiếu gRPC-Web proxy."
                ],
                "referenceAnswer": (
                    "1. Ở chặng nội bộ 25.000 RPS, `gRPC` nén dữ liệu thành chuỗi byte nhị phân theo schema `.proto` (nhanh gấp 5–10 lần parse văn bản JSON) và chạy trên `HTTP/2 Multiplexing` cho phép gửi hàng nghìn lời gọi song song trên một kết nối TCP bền vững.\n"
                    "2. Trong FastAPI: chỉ dùng `async def` khi toàn bộ thư viện bên trong hỗ trợ bất đồng bộ (`await httpx`, `await asyncpg`); nếu gọi hàm đồng bộ hoặc tiền xử lý dữ liệu chặn luồng thì phải khai báo `def` để FastAPI đẩy vào Threadpool, còn với suy luận mô hình ML nặng CPU/GIL thì phải tách sang Worker/ProcessPool hoặc gọi bất đồng bộ tới máy chủ `vLLM/Triton`.\n"
                    "3. Với luồng cập nhật trạng thái giao hàng 1 chiều (Server -> Client), `SSE (text/event-stream)` tối ưu hơn Polling (triệt tiêu 99% request rỗng) và đơn giản hơn WebSocket hai chiều."
                )
            }
        }
    },

    # --------------------------------------------------------------------------
    # F05 · VALIDATION & VERIFICATION (TESTING, PYTEST, TDD, HOARE LOGIC)
    # --------------------------------------------------------------------------
    {
        "id": "F05-BP-01",
        "topic": "F05",
        "stage": 1,
        "stationId": "val-1-3",
        "stationTitle": "Trạm 1.1–4.2: V-Model, Equivalence Partitioning/BVA, Mutation Testing & Pytest Mocking",
        "roleTracks": ["DE", "AIE", "MLE"],
        "skillName": "Software Verification vs. Validation, Boundary Value Analysis, Mutation Testing & Pytest Architecture",
        "invariant": (
            "Verification trả lời 'Are we building the product right?' (đúng đặc tả kỹ thuật), còn Validation trả lời 'Are we building the right product?' (đúng nhu cầu thực tế của người dùng); "
            "độ phủ dòng lệnh (Line Coverage 100%) không đảm bảo bộ test tốt nếu thiếu kiểm tra quyết định (assertions) — phải đo bằng Mutation Score (tỷ lệ tiêu diệt các dị bản Mutant); "
            "và khi dùng `mocker.patch`, quy tắc bất biến là phải patch tại nơi đối tượng ĐƯỢC IMPORT VÀ SỬ DỤNG (`Patch where it is used`), không phải nơi nó được định nghĩa gốc."
        ),
        "misconceptions": [
            "Tự hào rằng `pytest --cov` đạt 100% Line Coverage nghĩa là phần mềm chắc chắn không còn bug.",
            "Khi module `order_service.py` viết `from payment_sdk import charge_card`, lại đi gọi `mocker.patch('payment_sdk.charge_card')` khiến hàm thật vẫn bị gọi và trừ tiền thật.",
            "Dùng chung một biến danh sách/kết nối toàn cục giữa các hàm test mà không cô lập qua `pytest.fixture`."
        ],
        "L1": {
            "stem": (
                "Một đội kỹ sư khoe rằng bộ kiểm thử đơn vị (`Unit Test`) của họ đạt `100% Line Coverage` trên hàm tính chiết khấu đơn hàng, "
                "nhưng khi chạy công cụ **Mutation Testing** (như `mutmut` tự động đổi dấu `>` thành `>=` hoặc đổi `+` thành `-` để tạo ra các dị bản `Mutants`), "
                "tới `60% Mutants` vẫn sống sót (`Survived` — tức bộ test vẫn báo PASS xanh mượt). Hiện tượng này chứng minh lỗ hổng gì?"
            ),
            "options": [
                "`Line Coverage` chỉ đo xem dòng lệnh có được CPU chạy lướt qua hay không chứ không đo chất lượng câu lệnh kiểm định (`assert`); các bài test hiện tại chỉ gọi hàm lấy lệ (hoặc `assert result is not None`) và thiếu các ca kiểm thử Giá trị Biên (`Boundary Value Analysis`) để bắt lỗi khi toán tử bị biến đổi.",
                "Công cụ Mutation Testing bị lỗi vì một khi `Line Coverage` đã đạt 100% thì về mặt toán học không thể tồn tại bất kỳ lỗi logic nào nữa.",
                "Do máy chủ chạy test thiếu RAM nên các tiến trình Mutant không thể bị tiêu diệt bởi Garbage Collector.",
                "Do đội kỹ sư dùng `pytest` thay vì `unittest` nên không hỗ trợ kiểm tra toán tử so sánh."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 1.3 (F05): Một bài test gọi hàm mà không `assert` giá trị đầu ra cụ thể (hoặc không test ngay tại điểm biên `>= 1000000`) "
                "vẫn đạt 100% Line Coverage nhưng để lọt toàn bộ lỗi thay đổi toán tử. `Mutation Score = Killed Mutants / Total Mutants` mới là thước đo chất lượng thật của bộ test."
            ),
            "distractorReasons": [
                "Chính xác: Thực thi qua dòng lệnh (Execution) hoàn toàn khác với kiểm định tính đúng đắn của kết quả (Verification).",
                "Sai: 100% Line Coverage mà không có `assert` chặt chẽ (Assertion-free testing) thì không bắt được bất kỳ lỗi logic nào.",
                "Sai: Mutant trong Mutation Testing là bản biến đổi mã nguồn (AST mutation), không liên quan đến Garbage Collector.",
                "Sai: `pytest` hỗ trợ đầy đủ phép kiểm định `assert` và tích hợp trực tiếp với các công cụ Mutation Testing."
            ]
        },
        "L2": {
            "stem": (
                "Trong tệp `app/checkout.py`, lập trình viên viết dòng import trực tiếp ở đầu tệp:\n"
                "`from app.gateways.stripe_client import charge_credit_card`\n"
                "Khi viết unit test trong `tests/test_checkout.py`, kỹ sư dùng lệnh:\n"
                "`mocker.patch('app.gateways.stripe_client.charge_credit_card', return_value={'status': 'SUCCESS'})`\n"
                "Nhưng khi chạy `pytest`, bài test vẫn gọi thẳng ra máy chủ Stripe thật trên Internet! Tại sao và phải sửa đường dẫn patch như thế nào?"
            ),
            "codeSnippet": (
                "# Tệp app/checkout.py\n"
                "from app.gateways.stripe_client import charge_credit_card\n\n"
                "def process_order(amount: int):\n"
                "    return charge_credit_card(amount)"
            ),
            "options": [
                "Cú pháp `from ... import charge_credit_card` đã gắn trực tiếp một tham chiếu tên biến cục bộ (`Name Binding`) bên trong không gian tên của module `app.checkout` ngay lúc nạp tệp; do đó phải áp dụng quy tắc **Patch nơi đối tượng được sử dụng**: `mocker.patch('app.checkout.charge_credit_card', ...)`.",
                "Do `pytest-mock` không hỗ trợ patch các hàm trả về kiểu từ điển `dict`.",
                "Phải xóa từ khóa `return_value` và đổi thành `side_effect = None` thì lệnh patch mới có hiệu lực.",
                "Do tệp `test_checkout.py` không nằm chung thư mục với `stripe_client.py` nên Python cấm ghi đè hàm."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 4.1 (F05) kết hợp Mô hình Name Binding (F02): Khi `app.checkout` chạy `from app.gateways.stripe_client import charge_credit_card`, "
                "nó đã tạo biến `app.checkout.charge_credit_card` trỏ thẳng vào hàm gốc. Nếu chỉ thay nhãn ở module `stripe_client`, biến trong `app.checkout` vẫn giữ nguyên con trỏ cũ!"
            ),
            "distractorReasons": [
                "Chính xác: Quy tắc vàng 'Patch where it is looked up / used' (`app.checkout.charge_credit_card`).",
                "Sai: `mocker.patch` hỗ trợ bất kỳ kiểu dữ liệu trả về nào.",
                "Sai: `return_value` là tham số chuẩn của `unittest.mock` / `pytest-mock`.",
                "Sai: Vị trí thư mục test không ngăn cản việc patch namespace trong bộ nhớ."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Thiết kế Chiến lược Kiểm thử Toàn diện: Hàm `calculate_shipping_fee(weight_kg: float, order_total: int, is_vip: bool)` có đặc tả nghiệp vụ:\n"
                "- Khối lượng hợp lệ: `0 < weight_kg <= 50.0` (ngoài khoảng này ném `ValueError`).\n"
                "- Nếu `order_total >= 500_000` HOẶC `is_vip == True`: miễn phí vận chuyển (`0 VNĐ`), TRỪ KHI `weight_kg > 20.0` thì vẫn phụ thu hàng nặng `30_000 VNĐ`.\n"
                "- Ngược lại: tính phí chuẩn `25_000 VNĐ`."
            ),
            "mcqPrompt": "Phần A (Thiết kế Ca kiểm thử Hộp đen): Theo kỹ thuật Phân vùng Tương đương (Equivalence Partitioning) và Phân tích Giá trị Biên (Boundary Value Analysis - BVA), bộ giá trị `weight_kg` nào bắt buộc phải đưa vào `@pytest.mark.parametrize` để bắt gọn các lỗi lệch dấu `<` / `<=`?",
            "options": [
                "Kiểm tra sát các mốc biên chuyển trạng thái: `[-0.1, 0.0, 0.1, 20.0, 20.1, 50.0, 50.1]` kết hợp tổ hợp `(order_total = 499_999 vs 500_000)` và `is_vip`.",
                "Chỉ cần chọn ngẫu nhiên 3 số chẵn `[10.0, 30.0, 40.0]` là đủ đại diện cho mọi trường hợp.",
                "Chỉ cần kiểm tra giá trị trung bình `weight_kg = 25.0` với `order_total = 1_000_000`.",
                "Chỉ cần test các số âm `[-100, -50, -1]` vì lỗi phần mềm chỉ xảy ra khi đầu vào âm."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Kiến trúc Kiểm thử Tầng Dữ liệu & CI): Khi hàm này được tích hợp vào dịch vụ lưu đơn hàng xuống PostgreSQL thật, "
                "hãy giải thích sự khác biệt giữa việc dùng `MagicMock` (Unit Test) và dùng `Testcontainers` + `@pytest.fixture` có `yield` (Integration Test) — "
                "tại sao nếu chỉ dùng Mock cho tầng SQL thì vẫn có thể sập trên Production?"
            ),
            "rubric": {
                "coreConcepts": [
                    "Giải thích đúng nguyên lý BVA: lỗi lập trình viên (off-by-one: `<` thay vì `<=` tại mốc `0.0`, `20.0`, `50.0` và `500_000`) luôn tập trung ngay trên đường biên giữa các phân vùng.",
                    "Giải thích cơ chế `@pytest.fixture` với từ khóa `yield`: phần trước `yield` là `Setup` (khởi tạo dữ liệu/transaction), phần sau `yield` là `Teardown` (rollback/dọn dẹp đảm bảo tính cô lập giữa các bài test).",
                    "Phân tích giới hạn của `MagicMock` với Database: Mock chỉ trả về kết quả giả định do chính lập trình viên tự bịa ra, hoàn toàn không phát hiện được lỗi sai cú pháp SQL, vi phạm ràng buộc `FOREIGN KEY / CHECK / UNIQUE` hay sai lệch kiểu dữ liệu trên PostgreSQL thật — do đó tầng Integration Test bắt buộc dùng `Testcontainers` khởi chạy container Postgres thật."
                ],
                "tradeoffs": [
                    "Cân bằng Tháp Kiểm thử (Testing Pyramid): Unit Test + Mock chạy cực nhanh (mili-giây) cho hàng chục nhánh logic biên, còn Integration Test với Testcontainers chạy chậm hơn (vài giây) để khóa chặt hợp đồng với Database thật."
                ],
                "referenceAnswer": (
                    "1. Với logic tính phí, dùng `@pytest.mark.parametrize` quét các điểm biên `weight_kg` (`0.0`, `0.1`, `20.0`, `20.1`, `50.0`, `50.1`) và `order_total` (`499_999`, `500_000`), đặc biệt kiểm tra nhánh ngoại lệ `is_vip=True` nhưng `weight_kg=20.1` phải thu `30_000 VNĐ`.\n"
                    "2. `MagicMock` chỉ kiểm chứng logic Python thuần trong cô lập; nếu câu lệnh SQL viết sai tên cột hoặc vi phạm ràng buộc `CHECK (amount >= 0)` của PostgreSQL thì Mock vẫn báo PASS giả tạo.\n"
                    "3. Dùng `@pytest.fixture(scope='session')` khởi tạo `PostgresContainer` (Testcontainers) kết hợp fixture cấp hàm dùng `yield` để bọc mỗi bài test trong một DB Transaction rồi `rollback()` sau `yield`, vừa kiểm chứng trên Postgres thật vừa giữ tốc độ nhanh và cô lập 100%."
                )
            }
        }
    },

    # --------------------------------------------------------------------------
    # F06 · CONTAINERIZATION & ORCHESTRATION (DOCKER & KUBERNETES)
    # --------------------------------------------------------------------------
    {
        "id": "F06-BP-01",
        "topic": "F06",
        "stage": 2,
        "stationId": "container-2-1",
        "stationTitle": "Trạm 2.1–4.3: Linux Namespaces, cgroups v2, OverlayFS, Multi-stage Build & K8s Reconciliation",
        "roleTracks": ["DE", "AIE", "MLE"],
        "skillName": "OS-Level Virtualization (Namespaces/cgroups/OverlayFS), Dockerfile Optimization & Kubernetes Architecture",
        "invariant": (
            "Container không có Guest OS Kernel riêng mà chỉ là các tiến trình Linux thông thường trên Host được cô lập tầm nhìn bằng `Namespaces` (`pid`, `net`, `mnt`, `uts`, `ipc`, `user`), "
            "giới hạn mức trần tài nguyên vật lý bằng `Control Groups (cgroups v2)`, và xếp chồng các tầng ảnh bất biến (`lowerdir`) kèm một tầng ghi mỏng (`upperdir`) bằng `OverlayFS`."
        ),
        "misconceptions": [
            "Tưởng rằng mỗi Docker Container chứa nguyên một nhân Linux Kernel riêng biệt giống như máy ảo (VM).",
            "Viết `COPY . .` trước dòng `RUN pip install -r requirements.txt` trong Dockerfile khiến mọi lần sửa 1 dòng code đều phải tải và cài lại toàn bộ thư viện từ đầu.",
            "Chạy `RUN rm -rf /tmp/large_weights.bin` ở một lệnh `RUN` tách biệt phía sau và nghĩ rằng kích thước Docker Image sẽ giảm xuống."
        ],
        "L1": {
            "stem": (
                "Khi bạn khởi chạy một container bằng lệnh `docker run --memory=512m --cpus=2 order-api`, "
                "bên trong container lệnh `ps aux` hiển thị tiến trình Python có `PID = 1`, nhưng khi gõ `ps aux` trên máy chủ Host thì chính tiến trình đó lại mang `PID = 10423`. "
                "Bộ ba cơ chế nào của nhân Linux Kernel đứng sau hiện tượng này?"
            ),
            "options": [
                "`Namespaces` (cụ thể là `PID Namespace`) tạo ảo giác tầm nhìn để tiến trình thấy mình là `PID 1`, `cgroups (Control Groups)` khóa trần `512MB RAM` và `2 CPU cores`, còn `OverlayFS` hợp nhất các tầng ảnh chỉ-đọc (`lowerdir`) với tầng ghi (`upperdir`).",
                "Phần mềm `Hypervisor KVM` cắt cứng 2 nhân CPU vật lý và cài đặt một nhân `Guest OS Kernel` thu nhỏ dành riêng cho `PID 1`.",
                "Daemon `dockerd` dùng trình thông dịch ảo hóa toàn bộ tập lệnh phần cứng x86_64 sang bytecode riêng trước khi giao cho CPU.",
                "Container tự tạo một phân vùng ổ cứng định dạng `NTFS` riêng biệt để ẩn giấu các tiến trình khác trên máy chủ."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 2.1–2.3 (F06): Container bản chất là tiến trình trên Host Kernel. "
                "`Namespaces` quyết định *tiến trình được NHÌN THẤY gì* (ánh xạ Host PID 10423 thành Virtual PID 1), "
                "`cgroups` quyết định *tiến trình được DÙNG TỐI ĐA bao nhiêu tài nguyên*, và `OverlayFS` quản lý hệ thống tệp phân tầng."
            ),
            "distractorReasons": [
                "Chính xác: Bộ tam trụ cột của OS-level Virtualization (Namespaces + cgroups + OverlayFS).",
                "Sai: Đó là cơ chế của Máy ảo (Virtual Machine), còn Container chia sẻ trực tiếp nhân Host OS Kernel.",
                "Sai: Tiến trình trong Container chạy trực tiếp tập lệnh máy trên CPU thật mà không qua lớp dịch mã ảo hóa.",
                "Sai: Container dùng Union Mount (`OverlayFS`) trên hệ thống tệp Linux của Host."
            ]
        },
        "L2": {
            "stem": (
                "Một kỹ sư ML viết `Dockerfile` bên dưới để đóng gói dịch vụ suy luận PyTorch. "
                "Họ phàn nàn 2 vấn đề: (1) Ảnh cuối cùng nặng tới `4.8 GB` dù đã chạy lệnh `RUN rm -rf /root/.cache /tmp/raw_model.tar` ở dòng thứ 5, "
                "và (2) Mỗi khi sửa đúng 1 ký tự trong tệp `app.py`, lệnh `docker build` lại mất `8 phút` tải lại từ đầu toàn bộ gói `torch`. "
                "Nguyên nhân cơ học của cả 2 hiện tượng là gì?"
            ),
            "codeSnippet": (
                "FROM python:3.11\n"
                "WORKDIR /app\n"
                "COPY . /app\n"
                "RUN pip install -r requirements.txt && wget -O /tmp/raw_model.tar https://.../2gb.tar && tar -xf /tmp/raw_model.tar\n"
                "RUN rm -rf /root/.cache /tmp/raw_model.tar\n"
                "CMD [\"uvicorn\", \"app:app\", \"--host\", \"0.0.0.0\"]"
            ),
            "options": [
                "Mỗi chỉ thị trong Dockerfile tạo ra một tầng ảnh bất biến (`Immutable Lowerdir Layer`): tệp 2GB đã ghi ở tầng 4 thì lệnh `rm -rf` ở tầng 5 chỉ tạo một dấu che (`whiteout file`) chứ không xóa byte nào khỏi tầng 4; đồng thời đặt `COPY . /app` trước `RUN pip install` làm vỡ Layer Cache ngay khi `app.py` đổi mã băm.",
                "Do lệnh `rm -rf` trong Docker chỉ xóa được thư mục rỗng và `pip install` không hỗ trợ lưu bộ nhớ đệm trên Linux.",
                "Do ảnh cơ sở `python:3.11` tự động nhân đôi kích thước mọi tệp `.tar` khi giải nén.",
                "Do thiếu cờ `--privileged` khi chạy `docker build` nên tiến trình không có quyền xóa tệp trong `/tmp`."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 2.3 & 3.1 (F06): Trong `OverlayFS`, các tầng bên dưới (`lowerdir`) là bất biến (Read-Only). "
                "Xóa tệp ở lệnh `RUN` sau chỉ ghi thêm một tệp đánh dấu ẩn (`whiteout`) ở tầng trên, còn 2GB dữ liệu vẫn nằm nguyên trong tầng dưới! "
                "Và Docker xét Cache theo thứ tự từ trên xuống: đặt `COPY requirements.txt .` -> `RUN pip install --no-cache-dir` trước `COPY . .` sẽ giữ nguyên cache thư viện khi chỉ sửa `app.py`."
            ),
            "distractorReasons": [
                "Chính xác: Giải thích đúng cơ học Immutable Layer / Whiteout file của OverlayFS và cơ chế Build Layer Cache Invalidation.",
                "Sai: `rm -rf` xóa được mọi thư mục trong tầng hiện hành, nhưng không sửa ngược được các tầng Read-Only đã đóng gói phía trước.",
                "Sai: `tar -xf` chỉ giải nén dữ liệu, nguyên nhân phình dung lượng là cả tệp `.tar` gốc lẫn bản giải nén đều bị lưu vĩnh viễn ở tầng 4.",
                "Sai: Trong quá trình `docker build`, lệnh `RUN` mặc định chạy với quyền `root` nên hoàn toàn có quyền xóa `/tmp`."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Thực chiến Kubernetes & Container Production: Dịch vụ xử lý dữ liệu của bạn được triển khai lên cụm Kubernetes (`Deployment` với `replicas: 3`, giới hạn `resources.limits.memory: 1Gi`). "
                "Đêm qua xảy ra 2 sự cố: (1) Một Worker Node vật lý bị sập nguồn đột ngột, và (2) Một Pod xử lý gặp lô dữ liệu lớn bị dừng đột ngột với mã `Exit Code 137 (OOMKilled)` và toàn bộ tệp báo cáo tạm mà Pod đó ghi vào `/app/output` biến mất sạch."
            ),
            "mcqPrompt": "Phần A (Cơ học Control Plane & Kernel): Tổ hợp cơ chế nào giải thích mã thoát `137` và cách Kubernetes tự động khôi phục số lượng Pod khi Worker Node sập?",
            "options": [
                "Mã `137 = 128 + 9 (SIGKILL)` do `Linux Kernel OOM Killer` bắn tín hiệu giết ngay lập tức khi tiến trình vượt ngưỡng `memory.max` của `cgroups`; còn khi Node sập, vòng lặp đối soát (`Reconciliation Loop`) của `Deployment / ReplicaSet Controller` trên Control Plane phát hiện `Actual State (2) < Desired State (3)` nên phối hợp cùng `kube-scheduler` lập lịch tạo Pod mới trên Node còn sống.",
                "Mã `137` là lỗi cú pháp Python, và `kube-proxy` tự động sửa lại mã nguồn Python để chạy lại trên cùng Node bị hỏng.",
                "Khi Worker Node sập, `etcd` tự động biến mình thành container chạy thay ứng dụng cho đến khi Node kia bật lại.",
                "Tệp trong `/app/output` biến mất là do `kube-scheduler` định kỳ xóa toàn bộ ổ cứng máy chủ mỗi 5 phút."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Thiết kế Bền vững & Tối ưu Hóa): Hãy trình bày: "
                "(1) Tại sao dữ liệu ghi vào `/app/output` lại mất sạch khi Pod bị `OOMKilled` và cách kiến trúc lưu trữ (`PV/PVC` hoặc `Object Storage S3/MinIO`) để giữ an toàn dữ liệu? "
                "(2) Cách viết lại `Dockerfile` theo chuẩn **Multi-stage Build** + **Non-root User** để vừa giảm 80% kích thước ảnh vừa chặn rủi ro leo thang đặc quyền?"
            ),
            "rubric": {
                "coreConcepts": [
                    "Giải thích đúng tính khả biến (Ephemeral) của tầng `upperdir` trong OverlayFS: khi Container bị xóa hoặc tạo lại trên Pod mới, tầng `upperdir` gắn với container cũ bị hủy; dữ liệu bền vững bắt buộc phải gắn qua `PersistentVolumeClaim (PVC)` hoặc đẩy thẳng lên `Object Storage (S3/MinIO)`.",
                    "Giải thích đúng công thức `Exit Code 137 = 128 + SIGKILL(9)` từ `cgroups OOM Killer` và cơ chế `Desired State vs Actual State Reconciliation` của K8s Control Plane (`kube-apiserver`, `etcd`, `kube-controller-manager`, `kube-scheduler`, `kubelet`).",
                    "Trình bày cấu trúc `Multi-stage Dockerfile`: Stage 1 (`builder`) chứa trình biên dịch `gcc/build-essential` để build wheel/binary, Stage 2 (`runtime` dùng `python:3.11-slim`) chỉ `COPY --from=builder` các gói đã biên dịch và chạy dưới tài khoản `USER appuser` (Non-root)."
                ],
                "tradeoffs": [
                    "So sánh dùng `PVC (Block/File Storage)` với `Object Storage (S3)` cho đầu ra của các Pod xử lý phân tán: đẩy kết quả thẳng lên S3 giúp Pod hoàn toàn Stateless, dễ dàng scale ngang hàng trăm replica mà không lo xung đột gắn ổ đĩa (`ReadWriteOnce` vs `ReadWriteMany`)."
                ],
                "referenceAnswer": (
                    "1. Mọi tệp ghi vào `/app/output` mặc định nằm trên tầng `upperdir` tạm thời của `OverlayFS` gắn theo vòng đời Container; khi Pod bị `OOMKilled (128 + 9 = 137)` hoặc được lập lịch sang Node khác, tầng này mất sạch. Để bền vững và giữ Pod phi trạng thái (Stateless), worker nên đẩy thẳng tệp kết quả lên `S3/MinIO` (hoặc gắn `PersistentVolumeClaim` nếu cần ổ đĩa cục bộ).\n"
                    "2. Tối ưu `Dockerfile` bằng **Multi-stage Build**: dùng stage `FROM python:3.11 AS builder` để biên dịch thư viện C/C++, sau đó ở stage cuối `FROM python:3.11-slim` chỉ `COPY --from=builder` thư mục môi trường ảo sang, gộp lệnh dọn dẹp `--no-cache-dir` trong cùng 1 tầng `RUN`, và tạo `USER 10001 (non-root)` để nếu ứng dụng bị khai thác cũng không chiếm được quyền `root` trên Host Kernel."
                )
            }
        }
    },

    # --------------------------------------------------------------------------
    # D01 · INGESTION LAYER (KAFKA & DEBEZIUM CDC)
    # --------------------------------------------------------------------------
    {
        "id": "D01-BP-01",
        "topic": "D01",
        "stage": 4,
        "stationId": "ingestion-4-3",
        "stationTitle": "Trạm 2.3–5.2: Log-Based CDC, Kafka Partition/ISR/Zero-Copy & Debezium WAL Bloat",
        "roleTracks": ["DE", "AIE", "MLE"],
        "skillName": "Change Data Capture (WAL/Binlog), Kafka Durability (acks=all, ISR) & Zero-Copy I/O",
        "invariant": (
            "Log-based CDC (Debezium đọc PostgreSQL WAL / MySQL Binlog) bắt trọn 100% thao tác INSERT/UPDATE/DELETE với tác động gần bằng 0 lên CPU nguồn, "
            "nhưng giữ `Replication Slot` trên Postgres — nếu Connector chết mà không cấu hình `max_slot_wal_keep_size` và `heartbeat.interval.ms` sẽ gây nổ đầy ổ cứng (`WAL Disk Bloat`); "
            "trong Kafka, đơn vị song song tối đa trong 1 Consumer Group là `Partition`, và cam kết không mất dữ liệu đòi hỏi bộ ba `acks=all` + `replication.factor=3` + `min.insync.replicas=2`."
        ),
        "misconceptions": [
            "Tưởng rằng dùng `Query-based Polling (WHERE updated_at > last_run)` vẫn bắt được các dòng bị xóa cứng (`HARD DELETE`) mà không làm nặng DB nguồn.",
            "Cấu hình Topic có `6 Partitions` nhưng lại bật `20 Consumers` trong cùng một `Consumer Group` với hy vọng tốc độ đọc tăng gấp 20 lần.",
            "Cấu hình `acks=all` ở Producer nhưng để `min.insync.replicas=1` và tưởng rằng dữ liệu vẫn an toàn khi Broker Leader cháy ổ cứng."
        ],
        "L1": {
            "stem": (
                "Một Topic Kafka tên là `orders_cdc` được cấu hình gồm `6 Partitions`. Đội kỹ sư muốn tăng tốc độ xử lý nên triển khai một `Consumer Group` tên `lakehouse_sink_group` gồm `10 Consumer instances` chạy song song. "
                "Điều gì sẽ diễn ra trong thực tế?"
            ),
            "options": [
                "Chỉ có tối đa `6 Consumers` được gán mỗi anh `1 Partition` để đọc dữ liệu, còn `4 Consumers` dư ra sẽ ngồi chơi hoàn toàn (`Idle` — nhận 0 bản ghi) vì trong cùng một Consumer Group, một Partition tại một thời điểm chỉ được phép gán cho duy nhất một Consumer để bảo toàn thứ tự đọc.",
                "Cả `10 Consumers` sẽ chia nhau đọc chung cả `6 Partitions` theo cơ chế Round-Robin từng bản ghi một.",
                "Kafka Broker sẽ tự động tách `6 Partitions` thành `10 Partitions` ngay khi thấy Consumer thứ 7 kết nối vào.",
                "Toàn bộ `Consumer Group` sẽ báo lỗi và dừng hoạt động vì số lượng Consumer không được phép lớn hơn số lượng Partition."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 3.2 (D01): `Partition` là đơn vị song song cơ sở của Kafka. "
                "Để đảm bảo thứ tự bất biến của các sự kiện cùng `Key` (ví dụ `order_id = 8888`: `CREATE -> PAY -> SHIP`), "
                "Kafka khóa chặt quy tắc: 1 Partition chỉ được đọc bởi tối đa 1 Consumer trong cùng một Consumer Group."
            ),
            "distractorReasons": [
                "Chính xác: Số Consumer hoạt động thực tế trong 1 Group bị chặn trần bởi số lượng Partition của Topic.",
                "Sai: Nếu nhiều Consumer trong cùng Group đọc chung 1 Partition thì thứ tự sự kiện của cùng một đơn hàng sẽ bị đảo lộn hoàn toàn.",
                "Sai: Kafka không bao giờ tự động tăng số Partition khi Consumer kết nối (vì tăng Partition làm thay đổi phép chia dư `murmur2(key) % N`).",
                "Sai: Hệ thống không lỗi; 4 Consumer dư ra sẽ ở trạng thái chờ dự phòng (Standby/Idle) để thế chỗ nếu 1 trong 6 Consumer đang chạy bị sập."
            ]
        },
        "L2": {
            "stem": (
                "Hệ thống thu thập CDC dùng `Debezium PostgreSQL Connector` đọc từ bảng `orders`. "
                "Ngoài bảng `orders` có lưu lượng trung bình, cùng cơ sở dữ liệu đó còn một bảng `audit_logs` không nằm trong danh sách theo dõi của Debezium nhưng ghi tới `50 GB/giờ`. "
                "Khi bảng `orders` không có giao dịch mới vào ban đêm (hoặc khi Kafka Connect tạm dừng), ổ cứng chứa thư mục `pg_wal` của PostgreSQL nguồn bất ngờ tăng vọt `400 GB` và làm sập toàn bộ Database lúc 3 giờ sáng! "
                "Tại sao sự cố này xảy ra và cặp cấu hình nào chặn đứng tận gốc?"
            ),
            "codeSnippet": (
                "postgres=# SELECT slot_name, active, pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained_wal\n"
                "FROM pg_replication_slots;\n"
                "   slot_name   | active | retained_wal \n"
                "---------------+--------+--------------\n"
                " debezium_slot | f      | 412 GB"
            ),
            "options": [
                "PostgreSQL dùng chung một luồng nhật ký `WAL` cho toàn bộ các bảng; khi Debezium ngừng xác nhận vị trí `Confirmed Flush LSN` (do connector sập hoặc do bảng `orders` yên ắng trong khi bảng `audit_logs` vẫn xả 50 GB WAL/giờ), `Replication Slot` ghim chặt `restart_lsn` ở tít phía sau ngăn Postgres xóa WAL cũ. Cần bật `heartbeat.interval.ms` kèm `heartbeat.action.query` để đẩy LSN liên tục và đặt cầu chì `max_slot_wal_keep_size` trên PostgreSQL.",
                "Do Debezium tự động chép toàn bộ dữ liệu từ Kafka ngược về lại thư mục `pg_wal` của PostgreSQL để đối chiếu.",
                "Do tiến trình `Autovacuum` của PostgreSQL bị xung đột với giao thức TCP/IP của Kafka Broker.",
                "Chỉ cần đổi định dạng tuần tự hóa của Kafka từ `Avro` sang `JSON` là PostgreSQL tự động giải phóng thư mục `pg_wal`."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 5.2 (D01): Đây là bẫy vận hành chí mạng nhất của Log-based CDC trên PostgreSQL (`WAL Bloat`). "
                "Vì WAL là nhật ký chung của cả cụm DB, nếu bảng được Debezium theo dõi không có sự kiện mới, Debezium không cập nhật `LSN` mới cho Postgres trong khi bảng `audit_logs` vẫn đẻ hàng trăm GB WAL. "
                "Bắt buộc dùng `heartbeat.interval.ms` + `heartbeat.action.query` để nhích LSN định kỳ và đặt trần `max_slot_wal_keep_size` để bảo vệ sự sống của DB nguồn."
            ),
            "distractorReasons": [
                "Chính xác: Giải phẫu đúng cơ chế Replication Slot LSN pinning và 2 lớp phòng thủ chuẩn Production.",
                "Sai: Debezium chỉ đọc một chiều từ Replication Slot của Postgres đẩy ra Kafka, không bao giờ ghi ngược từ Kafka vào `pg_wal`.",
                "Sai: `Autovacuum` dọn Dead Tuples trên Heap, còn việc giữ lại tệp `pg_wal` là do `Replication Slot` chưa nhận được LSN xác nhận.",
                "Sai: Định dạng Avro hay JSON ở phía Kafka không ảnh hưởng gì tới con trỏ `restart_lsn` trên PostgreSQL."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Thiết kế Đường ống Ingestion Cấp độ Ngân hàng: Bạn được giao thiết kế đường ống thu thập biến động số dư và giao dịch từ PostgreSQL sang Kafka rồi ghi xuống kho Lakehouse với yêu cầu: "
                "(1) Không được làm tăng tải CPU trên PostgreSQL quá 3%, "
                "(2) Bắt được cả thao tác xóa (`DELETE`) và giữ nguyên thứ tự biến động của từng tài khoản (`account_id`), "
                "(3) Không mất bất kỳ giao dịch nào ngay cả khi 1 máy chủ Kafka Broker bị cháy ổ cứng ngay sau khi Producer vừa nhận báo thành công."
            ),
            "mcqPrompt": "Phần A (Quyết định Cấu hình Cốt lõi): Tổ hợp kiến trúc và thông số nào thỏa mãn đồng thời cả 3 yêu cầu trên?",
            "options": [
                "Dùng `Debezium Log-based CDC (pgoutput WAL)` lấy `account_id` làm `Message Key` để băm cố định vào cùng một Kafka Partition; phía Producer/Broker bật bộ tứ bất tử: `enable.idempotence=true`, `acks=all`, `replication.factor=3`, `min.insync.replicas=2` và tắt `unclean.leader.election.enable=false`.",
                "Chạy câu lệnh `SELECT * FROM transactions WHERE updated_at > ...` mỗi 5 giây với `acks=1` và `min.insync.replicas=1`.",
                "Gắn `AFTER UPDATE/DELETE Trigger` ghi vào bảng phụ ngay trong cùng transaction của khách hàng và đẩy lên Kafka với `acks=0` để đạt tốc độ nhanh nhất.",
                "Dùng `Random Partitioner` rải đều các sự kiện của cùng một `account_id` ra khắp 12 Partitions để tăng tốc độ ghi."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Giải phẫu Cơ học & Xử lý Poison Pill): Hãy giải thích: "
                "(1) Tại sao nếu chỉ bật `acks=all` mà quên đặt `min.insync.replicas=2` (để mặc định bằng 1) thì khi Broker Leader cháy ổ cứng dữ liệu vẫn bị mất trắng? "
                "(2) Nhờ cơ chế `Zero-Copy (sendfile)` nào của Linux Kernel mà Kafka có thể truyền hàng GB dữ liệu/giây mà không tốn CPU chép qua vùng nhớ JVM? "
                "(3) Khi xuất hiện một bản ghi lỗi định dạng (`Poison Pill`), bạn cấu hình Dead Letter Queue (`DLQ`) thế nào để đường ống không bị kẹt chết?"
            ),
            "rubric": {
                "coreConcepts": [
                    "Giải thích đúng lỗ hổng `acks=all` khi `min.insync.replicas=1`: nếu 2 Follower bị trễ và văng khỏi tập `ISR (In-Sync Replicas)`, tập ISR chỉ còn đúng 1 mình Leader; lúc đó `acks=all` suy biến thành `acks=1` (chỉ ghi vào Leader là báo thành công ngay) -> Leader cháy ổ cứng là mất sạch dữ liệu!",
                    "Giải thích đúng cơ chế `Zero-Copy (sendfile syscall + DMA)`: dữ liệu đi thẳng từ `OS Page Cache` trên Kernel Space qua `NIC Buffer` ra card mạng bằng bộ điều khiển DMA (2 lần chuyển ngữ cảnh, 0 lần chép dữ liệu sang vùng nhớ JVM User Space).",
                    "Cơ chế xử lý `Poison Pill`: cấu hình `errors.tolerance=all` + `errors.deadletterqueue.topic.name` kèm headers thông tin lỗi (`errors.deadletterqueue.context.headers.enable=true`) để đẩy riêng bản ghi hỏng sang topic DLQ và giữ luồng chính chạy liên tục."
                ],
                "tradeoffs": [
                    "Đánh đổi giữa Tính sẵn sàng (Availability) và Tính bền vững (Durability): với `RF=3, min.insync.replicas=2`, cụm chịu được tối đa 1 Broker chết; nếu 2 trên 3 Broker chết cùng lúc, Producer sẽ nhận `NotEnoughReplicasException` (tạm dừng ghi thay vì chấp nhận mất dữ liệu)."
                ],
                "referenceAnswer": (
                    "1. `acks=all` yêu cầu toàn bộ các bản sao đang nằm trong danh sách `ISR (In-Sync Replicas)` xác nhận. Nếu `min.insync.replicas=1` và 2 Follower bị rớt mạng, ISR co lại chỉ còn đúng 1 Leader — khi đó Leader ghi xong đã báo `ACK` ngay, nếu Leader hỏng đĩa trước khi Follower kịp chép thì dữ liệu mất vĩnh viễn. Đặt `RF=3, min.insync.replicas=2` ép buộc phải có ít nhất 1 Leader + 1 Follower ghi xong mới báo thành công.\n"
                    "2. Kafka đạt thông lượng cực đại nhờ gọi System Call `sendfile()` (Zero-Copy): Kernel đẩy thẳng dữ liệu từ `OS Page Cache` sang `NIC Buffer` qua phần cứng `DMA`, loại bỏ hoàn toàn việc chép dữ liệu vòng qua vùng nhớ `JVM Heap` (User Space).\n"
                    "3. Với `Poison Pill`, bật `errors.tolerance=all` và định tuyến sang `Dead Letter Queue (DLQ)` kèm đầy đủ metadata (`topic`, `partition`, `offset`, `exception stacktrace`) để cảnh báo kỹ sư xử lý và replay sau mà không làm đóng băng cả Consumer Group."
                )
            }
        }
    },

    # --------------------------------------------------------------------------
    # D02 · STORAGE LAYER (PARQUET, ARROW, HDFS, LAKEHOUSE DELTA/ICEBERG/HUDI)
    # --------------------------------------------------------------------------
    {
        "id": "D02-BP-01",
        "topic": "D02",
        "stage": 2,
        "stationId": "storage-2-2",
        "stationTitle": "Trạm 1.1–7.4: Tháp Độ Trễ, Parquet Footer, Non-Splittable Gzip & Open Lakehouse (Delta/Iceberg/Hudi)",
        "roleTracks": ["DE", "AIE", "MLE"],
        "skillName": "Storage Hierarchy, Apache Parquet Internals, Splittable Compression & Lakehouse ACID Concurrency",
        "invariant": (
            "Apache Parquet lưu dữ liệu theo phân đoạn hàng (`Row Groups`, mỗi cột là `Column Chunk` chứa các `Pages`) và đặt `Footer Metadata` ở ĐÁY tệp (chứa Schema, Min/Max Statistics và Byte Offset); "
            "động cơ truy vấn luôn dùng HTTP Range Request đọc `Footer` đầu tiên để thực hiện `Column Pruning` (chỉ đọc cột cần thiết) và `Predicate Pushdown / Data Skipping` (nhảy cóc qua cả Row Group nếu giá trị cần tìm nằm ngoài khoảng `[Min, Max]`)."
        ),
        "misconceptions": [
            "Tưởng rằng động cơ Spark/Trino phải đọc tuần tự tệp Parquet từ byte đầu tiên (`offset 0`) giống như đọc tệp CSV.",
            "Nén một tệp `orders.csv` nặng `100 GB` thành `orders.csv.gz` bằng thuật toán `Gzip` rồi giao cho cụm 100 máy chủ Spark đọc với hy vọng 100 máy sẽ chia nhau đọc song song.",
            "Tưởng rằng Object Storage (Amazon S3 / GCS) cho phép sửa trực tiếp 1 dòng giữa tệp (`in-place mutation`) hoặc ghi nối đuôi (`append`) vào tệp Parquet hiện có."
        ],
        "L1": {
            "stem": (
                "Bảng `orders` lưu dưới định dạng `Apache Parquet` trên S3 có `100 cột` và nặng `50 GB` (chia làm 100 Row Groups). "
                "Khi kỹ sư chạy câu lệnh `SELECT sum(amount) FROM orders WHERE order_id = 8888;`, "
                "trình tự đọc vật lý nào giúp động cơ truy vấn hoàn tất chỉ trong vài trăm mili-giây và chỉ tốn chưa tới `15 MB` băng thông mạng?"
            ),
            "options": [
                "Động cơ gửi `HTTP Range Request` đọc phần `Footer Metadata` nằm ở ĐÁY tệp trước tiên để lấy danh mục `Byte Offset` và thống kê `[Min, Max]` của từng `Row Group`; nhờ đó nó bỏ qua 99 Row Groups không chứa `#8888` (`Data Skipping`) và ở Row Group còn lại chỉ tải đúng các byte của 2 `Column Chunks` (`order_id` và `amount` — `Column Pruning`).",
                "Động cơ tải toàn bộ `50 GB` tệp Parquet về ổ cứng tạm của máy chủ Driver rồi mới lọc lấy cột `amount`.",
                "Phần `Header 4-byte PAR1` ở đầu tệp chứa sẵn toàn bộ giá trị tổng `sum(amount)` của mọi điều kiện lọc `WHERE`.",
                "S3 Object Storage tự động chạy câu lệnh SQL bên trong ổ cứng cơ học HDD rồi chỉ gửi kết quả số nguyên về cho người dùng."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 2.2 (D02): Cấu trúc lai Hybrid Columnar của Parquet đặt toàn bộ bản đồ chỉ mục (`Schema`, `Row Group Offsets`, và thống kê `Min/Max/Null_Count` của từng Column Chunk) ở `Footer` cuối tệp. "
                "Đọc Footer trước tiên cho phép kết hợp song kiếm hợp bích: `Predicate Pushdown` (loại bỏ Row Group theo Min/Max) và `Column Pruning` (chỉ kéo đúng cột được SELECT)."
            ),
            "distractorReasons": [
                "Chính xác: Đọc Footer ở cuối tệp qua HTTP Range Request -> Data Skipping theo Min/Max -> Column Pruning theo Byte Offset.",
                "Sai: Tải toàn bộ 50 GB cho 2 cột sẽ phá hủy hoàn toàn ý nghĩa của định dạng lưu trữ hướng cột.",
                "Sai: `PAR1` ở đầu và cuối tệp chỉ là 4-byte Magic Number nhận diện định dạng tệp Parquet.",
                "Sai: S3 là tầng lưu trữ đối tượng bất biến (Object Storage), việc đọc Footer và giải mã Column Chunk do động cơ tính toán thực hiện qua HTTP Range Request."
            ]
        },
        "L2": {
            "stem": (
                "Một kỹ sư muốn tiết kiệm chi phí lưu trữ S3 nên đã nén tệp nhật ký văn bản `events_raw.csv` (`120 GB`) thành một tệp duy nhất `events_raw.csv.gz` (`18 GB`) bằng chuẩn nén `Gzip`. "
                "Sau đó họ khởi chạy cụm Apache Spark gồm `64 Executor Cores` để đọc tệp `events_raw.csv.gz` này. "
                "Trên giao diện Spark UI, họ bàng hoàng thấy `63 Cores` ngồi chơi (`0% CPU`), chỉ có duy nhất `1 Task trên 1 Core` phải còng lưng đọc từ đầu đến cuối suốt 45 phút! "
                "Tại sao hiện tượng này xảy ra và cách khắc phục chuẩn kiến trúc là gì?"
            ),
            "codeSnippet": (
                "Stage 0: Scan csv s3a://lake-bronze/events_raw.csv.gz\n"
                "Active Tasks: 1 / 1   |   Available Executor Cores: 64\n"
                "Task 0: Locality ANY  |   Input Size: 18.0 GB (120 GB uncompressed)"
            ),
            "options": [
                "`Gzip` trên tệp văn bản thô là thuật toán nén luồng liên tục không có điểm đánh dấu đồng bộ khối (`Non-Splittable` — bảng từ điển giải nén phụ thuộc nối tiếp từ byte đầu tiên), nên không một máy chủ nào có thể nhảy vào giữa tệp để giải nén; cần chuyển sang định dạng đóng gói khối nội bộ (`Container Format` như `Parquet` nén `ZSTD`/`Snappy` theo từng Row Group độc lập) để đạt tính `Splittable` 100%.",
                "Do giao thức `s3a://` chỉ cho phép mở tối đa 1 kết nối TCP trên mỗi Bucket.",
                "Do tệp `.csv.gz` nhỏ hơn 1 TB nên Spark Optimizer tự động gộp về 1 nhân CPU để tiết kiệm điện.",
                "Chỉ cần đổi tên đuôi tệp từ `.csv.gz` sang `.parquet` mà không cần chuyển đổi định dạng bên trong là 64 nhân sẽ đọc song song."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 2.4 (D02): Một tệp nén khối đơn bằng `Gzip` không thể cắt nhỏ (`Non-splittable`) vì luồng bit DEFLATE phụ thuộc vào lịch sử các byte đứng trước. "
                "Ngược lại, `Parquet` (hoặc `Avro`/`ORC`) chia dữ liệu thành các `Row Groups / Blocks` độc lập và chỉ áp dụng nén (`Snappy`/`ZSTD`) bên trong từng Page/Block đó, giúp 64 máy chủ nhảy vào 64 Byte Offset khác nhau giải nén song song ngay lập tức!"
            ),
            "distractorReasons": [
                "Chính xác: Phân biệt sắc sảo giữa Non-Splittable Whole-File Compression (Gzip CSV) và Splittable Block/Container Compression (Parquet + Snappy/ZSTD).",
                "Sai: S3 hỗ trợ hàng nghìn kết nối HTTP Range Request song song đạt băng thông nhiều GB/giây.",
                "Sai: Kích thước mặc định của mỗi phân vùng đọc trong Spark là 128 MB (`spark.sql.files.maxPartitionBytes`); tệp 18 GB lẽ ra phải chia thành ~140 Tasks nếu nó splittable.",
                "Sai: Đổi tên đuôi tệp mà không chuyển đổi cấu trúc nhị phân bên trong sẽ gây lỗi hỏng định dạng (`Corrupt file: missing PAR1 magic bytes`)."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Thiết kế Kiến trúc Lakehouse & Medallion (Chặng 6 & 7): Công ty bạn đang lưu trữ bảng giao dịch `silver.orders` (`20 TB`) trên Object Storage S3. "
                "Hệ thống có 2 luồng chạy đồng thời: "
                "(1) Luồng CDC Streaming cứ mỗi `2 phút` lại đẩy một lệnh `MERGE INTO silver.orders` để cập nhật trạng thái của khoảng `5.000 đơn hàng` rải rác khắp các ngày, "
                "và (2) Hàng trăm truy vấn BI Dashboard quét báo cáo liên tục theo điều kiện lọc đa chiều `WHERE customer_region = 'VN' AND payment_channel = 'QR'`. "
                "Hiện tại mỗi lệnh `MERGE` mất tới `18 phút`, đẻ ra hàng trăm nghìn tệp nhỏ (`Small File Problem`) và thỉnh thoảng gãy vì xung đột ghi đồng thời."
            ),
            "mcqPrompt": "Phần A (Quyết định Kiến trúc Lakehouse): Tổ hợp kỹ thuật Open Table Format (Delta Lake / Apache Iceberg / Hudi) nào giải quyết triệt để bài toán trên?",
            "options": [
                "Chuyển chiến lược cập nhật từ `Copy-on-Write (COW)` sang `Merge-on-Read (MOR)` hoặc bật `Deletion Vectors` (chỉ ghi tệp đánh dấu dòng xóa/sửa nhỏ gọn thay vì viết lại nguyên tệp Parquet 1GB khi sửa vài dòng), kết hợp tiến trình `Compaction (OPTIMIZE)` chạy nền và gom cụm đa chiều bằng `Z-Ordering / Liquid Clustering` trên `(customer_region, payment_channel)`.",
                "Chia phân vùng vật lý (`Hive-style Partitioning`) theo cột `order_id` để mỗi đơn hàng nằm trong một thư mục S3 riêng biệt.",
                "Bỏ hoàn toàn tầng Metadata (`_delta_log` / `Iceberg Manifest`) và quay về ghi đè trực tiếp lên các tệp CSV thô trên S3.",
                "Chạy lệnh `VACUUM 0 HOURS` ngay lập tức sau mỗi phút trong khi các truy vấn BI đang đọc."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Bảo vệ Kiến trúc & Cơ học Nội tại): Hãy giải thích sâu 3 điểm: "
                "(1) Sự đánh đổi cốt lõi giữa `Copy-on-Write (COW)` và `Merge-on-Read (MOR) / Deletion Vectors` về chi phí khuếch đại ghi (`Write Amplification`) vs tốc độ đọc? "
                "(2) Tại sao `Z-Ordering / Liquid Clustering` lại vượt trội hơn `Hive Partitioning` truyền thống khi lọc trên nhiều cột hoặc cột có độ phân tán (cardinality) cao? "
                "(3) Tại sao chạy `VACUUM RETAIN 0 HOURS` trên bảng đang có người đọc lại phá vỡ cơ chế `MVCC Snapshot Isolation` trên S3?"
            ),
            "rubric": {
                "coreConcepts": [
                    "Phân tích đúng `Copy-on-Write (COW)` vs `Merge-on-Read (MOR) / Deletion Vectors`: vì tệp Parquet trên S3 là bất biến, sửa 1 dòng theo COW bắt buộc đọc và ghi lại cả tệp Parquet 512MB (`Write Amplification` khổng lồ); còn MOR / Deletion Vectors chỉ ghi một tệp bitmap/delta nhỏ đánh dấu vị trí dòng bị thay đổi rồi gộp lại ở bước Compaction nền.",
                    "Giải thích đúng cơ chế đường cong phủ không gian (`Space-Filling Curve: Z-Order / Hilbert Curve` trong Liquid Clustering): đồng định vị (co-locate) các bản ghi gần nhau theo nhiều cột cùng lúc giúp thu hẹp cực đại khoảng `[Min, Max]` trong Parquet Footer để `Data Skipping` nhảy cóc hiệu quả mà không đẻ ra hàng triệu thư mục con như Hive Partitioning (`Over-partitioning`).",
                    "Giải thích đúng nguy cơ của `VACUUM 0 HOURS`: các truy vấn BI đang chạy dựa trên ảnh chụp `Snapshot v_N` vẫn đang đọc các tệp Parquet cũ qua HTTP; nếu xóa vật lý ngay lập tức các tệp vừa hết hiệu lực ở `v_{N+1}`, các truy vấn đang chạy ở `v_N` sẽ vấp lỗi `FileNotFoundException` và mất khả năng `Time Travel`."
                ],
                "tradeoffs": [
                    "Nêu rõ đánh đổi của MOR: ghi cực nhanh nhưng nếu không chạy Compaction định kỳ thì luồng đọc phải trộn (merge) tệp gốc với nhiều tệp delete/delta làm tăng độ trễ đọc."
                ],
                "referenceAnswer": (
                    "1. Với `Copy-on-Write (COW)`, cập nhật 5.000 đơn nằm rải rác trên 500 tệp Parquet buộc hệ thống phải viết lại nguyên 500 tệp đó (khuếch đại ghi cực lớn). Bật `Merge-on-Read (MOR)` hoặc `Deletion Vectors (Roaring Bitmap)` giúp lệnh `MERGE` chỉ ghi tệp bitmap/delta siêu nhỏ trong vài giây, sau đó dùng job `OPTIMIZE / Compaction` bất đồng bộ để gộp thành tệp Parquet lớn chuẩn 256MB–1GB.\n"
                    "2. Nếu dùng `Hive Partitioning` trên nhiều cột sẽ gây bùng nổ thư mục và tệp nhỏ (`Small File Problem`). `Z-Ordering / Liquid Clustering` sắp xếp dữ liệu theo đường cong không gian đa chiều (`Z-curve / Hilbert curve`), ép khoảng `[Min, Max]` của cả `customer_region` lẫn `payment_channel` trong từng Row Group co hẹp lại, giúp Data Skipping bỏ qua >95% tệp mà không cần chia thư mục cứng.\n"
                    "3. Lakehouse thực hiện `MVCC` bằng cách giữ các tệp Parquet của phiên bản cũ cho các luồng đọc đang mở. Chạy `VACUUM 0 HOURS` sẽ xóa vật lý ngay các tệp của snapshot vừa bị thay thế, làm gãy các truy vấn BI đang chạy dở (`FileNotFoundException`) — chuẩn vận hành là giữ ngưỡng an toàn tối thiểu `7 ngày (168 giờ)`."
                )
            }
        }
    },

    # --------------------------------------------------------------------------
    # D03 · TRANSFORMATION LAYER I (BATCH · APACHE SPARK)
    # --------------------------------------------------------------------------
    {
        "id": "D03-BP-01",
        "topic": "D03",
        "stage": 4,
        "stationId": "spark-4-2",
        "stationTitle": "Trạm 1.2–6.3: Narrow vs. Wide Transformation, Unified Memory, Catalyst/Tungsten/AQE & Key Salting",
        "roleTracks": ["DE", "AIE", "MLE"],
        "skillName": "Apache Spark Execution Model (Stages/Shuffles), Catalyst/Tungsten/AQE & Data Skew Tuning",
        "invariant": (
            "`Narrow Transformation` (`map`, `filter`, `select`) xử lý gọn trên từng phân vùng tại chỗ trong 1 Stage bằng cơ chế đường ống (pipelining) không cần truyền mạng; "
            "còn `Wide Transformation` (`groupBy`, `join`, `distinct`, `repartition`) bắt buộc cắt ranh giới Stage mới và kích hoạt `Shuffle` (ghi tệp trung gian xuống đĩa + kéo qua mạng giữa các Executors)."
        ),
        "misconceptions": [
            "Viết hàm `Python UDF (@udf)` xử lý chuỗi trên DataFrame và nghĩ rằng nó có tốc độ ngang ngửa với các hàm dựng sẵn (built-in) `pyspark.sql.functions` chạy trên JVM/Tungsten.",
            "Dùng `df.repartition(1)` thay vì `df.coalesce(1)` hoặc dùng `repartition(1)` trên bảng 500 GB làm toàn bộ dữ liệu dồn về chết cứng 1 Executor.",
            "Khi gặp lỗi `Data Skew` ở 1 khóa `store_id = 'HQ'` (chiếm 80% dữ liệu), lại đi tăng `spark.sql.shuffle.partitions` từ 200 lên 2000 và tưởng rằng khóa `'HQ'` sẽ tự tách ra làm 2000 mảnh."
        ],
        "L1": {
            "stem": (
                "Trong PySpark, tại sao việc dùng các hàm dựng sẵn (built-in) trong `pyspark.sql.functions` (như `F.col()`, `F.when()`, `F.regexp_extract()`) "
                "lại nhanh gấp `10 đến 50 lần` so với việc tự viết một hàm `@udf` bằng Python thường để xử lý cùng một logic trên 100 triệu dòng?"
            ),
            "options": [
                "Hàm dựng sẵn (built-in) được `Catalyst Optimizer` nhìn thấy toàn bộ cây biểu thức để tối ưu hóa và được `Tungsten Engine` biên dịch thành bytecode chạy thẳng trên vùng nhớ nhị phân `UnsafeRow` trong JVM; ngược lại `@udf` Python là một 'hộp đen' buộc JVM phải tuần tự hóa (`Pickle`) từng dòng dữ liệu đẩy qua ống IPC sang tiến trình `Python Subprocess` bên ngoài rồi lại giải tuần tự hóa ngược về JVM.",
                "Vì các hàm trong `pyspark.sql.functions` luôn tự động chạy trên card đồ họa GPU NVIDIA, còn `@udf` chạy trên CPU.",
                "Vì khi dùng `@udf`, Spark bắt buộc phải ghi toàn bộ bảng dữ liệu lên Amazon S3 ở mỗi dòng lệnh.",
                "Vì `@udf` không được phép chạy trên các Worker Executor mà chỉ chạy một mình trên máy chủ Driver."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 2.2 & 4.2 (D03): Với `@udf` Python truyền thống, Catalyst không thể tối ưu hóa bên trong hàm (Black-box), "
                "và chi phí đắt đỏ nhất là phải tuần tự hóa (`Pickle Serialization`) dữ liệu qua lại giữa tiến trình `JVM Executor` và tiến trình con `Python Worker` qua socket IPC."
            ),
            "distractorReasons": [
                "Chính xác: Catalyst/Tungsten `UnsafeRow` trực tiếp trên JVM vs Black-box IPC + Pickle Serialization sang Python Subprocess.",
                "Sai: Mặc định Spark chạy trên CPU; muốn chạy trên GPU phải cài plugin riêng như RAPIDS Accelerator.",
                "Sai: `@udf` truyền dữ liệu qua ống loopback IPC trên cùng máy Worker, không phải ghi lên S3 ở mỗi dòng.",
                "Sai: `@udf` vẫn chạy phân tán trên các Worker Nodes (trong các tiến trình Python con nằm cạnh JVM Executor), không phải trên Driver."
            ]
        },
        "L2": {
            "stem": (
                "Bạn đang chạy một job Spark thực hiện phép nối `orders_df.join(stores_df, 'store_id')` giữa bảng `orders` (`500 GB`) và bảng `stores` (`12 MB`). "
                "Tuy nhiên do bảng `stores` được tạo ra từ một bước biến đổi phức tạp phía trước nên Spark không ước lượng được kích thước lúc lập kế hoạch tĩnh và đã chọn `SortMergeJoin`. "
                "Trên Spark UI, Stage nối bị treo ở `199 / 200 Tasks` đã xong trong 1 phút, còn đúng `Task 142` chạy suốt 2 giờ với `Shuffle Read = 380 GB` và `Disk Spill = 290 GB` vì `store_id = 'FLAGSHIP_01'` chiếm 75% tổng đơn hàng! "
                "Tại sao việc tăng `spark.sql.shuffle.partitions = 2000` hoàn toàn VÔ DỤNG trong trường hợp này, và giải pháp chuẩn là gì?"
            ),
            "codeSnippet": (
                "Stage 4 (SortMergeJoin): 199/200 Succeeded\n"
                "Task 142 | Status: RUNNING (2.1 h) | Shuffle Read: 380.4 GB | Spill (Memory): 810 GB | Spill (Disk): 290 GB"
            ),
            "options": [
                "Phép băm `hash('FLAGSHIP_01') % numPartitions` là tất định nên dù có chia làm 2.000 hay 10.000 phân vùng thì toàn bộ 380 GB của cùng một khóa `'FLAGSHIP_01'` vẫn bị dồn vào đúng 1 phân vùng duy nhất! Với bảng `stores` chỉ nặng `12 MB`, giải pháp tối ưu nhất là ép dùng `BroadcastHashJoin` (`F.broadcast(stores_df)`) hoặc bật `AQE (Adaptive Query Execution)` để triệt tiêu hoàn toàn bước Shuffle bảng 500 GB; nếu cả 2 bảng đều lớn thì dùng `AQE Skew Join` hoặc kỹ thuật `Key Salting`.",
                "Tăng `spark.sql.shuffle.partitions` lên `2000` chắc chắn sẽ tự động cắt khóa `'FLAGSHIP_01'` ra làm 10 phần bằng nhau mà không cần làm gì thêm.",
                "Chỉ cần gọi lệnh `.collect()` trên bảng `orders_df` (`500 GB`) đưa về máy chủ Driver để nối bằng từ điển Python.",
                "Chuyển chế độ lưu đệm sang `persist(StorageLevel.MEMORY_ONLY)` sẽ tự động xóa bỏ các đơn hàng của `'FLAGSHIP_01'`."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 4.3 & 5.1 (D03): Băm theo khóa (`Hash Partitioning`) luôn đưa các dòng có cùng khóa `store_id` về cùng một Task. "
                "Khi một bên bảng nối nhỏ (`12 MB` < ngưỡng Broadcast), dùng `BroadcastHashJoin` sẽ phát bản sao bảng `12 MB` tới mọi Executor để nối ngay tại chỗ (`Narrow Transformation`, `0 Shuffle`), xóa sổ hoàn toàn hiện tượng lệch tải!"
            ),
            "distractorReasons": [
                "Chính xác: Giải thích đúng bản chất toán học của `hash(key) % N` và thứ tự ưu tiên xử lý Skew (Broadcast Join -> AQE Skew Join -> Key Salting).",
                "Sai: Mọi bản ghi có cùng giá trị khóa `'FLAGSHIP_01'` luôn có cùng mã băm `hash('FLAGSHIP_01')`, nên tăng `N` không bao giờ tách được 1 khóa đơn lẻ ra nhiều phân vùng.",
                "Sai: Gọi `.collect()` trên bảng 500 GB sẽ kéo toàn bộ 500 GB về bộ nhớ của duy nhất máy Driver, gây nổ `java.lang.OutOfMemoryError` ngay lập tức!",
                "Sai: `MEMORY_ONLY` chỉ lưu bộ nhớ đệm, không làm hết lệch khóa và còn gây văng dữ liệu khi thiếu RAM."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Tối ưu hóa & Vận hành Spark Production: Bạn tiếp nhận một đường ống PySpark chạy hàng đêm trên cụm Kubernetes tốn `4 giờ` và hay sập OOM:\n"
                "1. Đọc bảng Parquet `events` (`2 TB`, `150 cột`), sau đó gọi `.filter(F.col('dt') == '2026-10-19')`, rồi nối (`JOIN`) với một bảng lớn khác `user_profiles` (`400 GB`, bị lệch nặng ở các tài khoản Bot/System).\n"
                "2. Giữa đường ống, lập trình viên cũ gọi `df.cache()` nhưng quên `unpersist()`, và ở bước cuối gọi `df.repartition(1).write.parquet(...)` khiến bước ghi cuối cùng nghẽn cổ chai suốt 90 phút."
            ),
            "mcqPrompt": "Phần A (Nhận diện Điểm Nghẽn): Đâu là sai lầm nghiêm trọng nhất ở bước cuối `df.repartition(1).write.parquet(...)` trên dữ liệu hàng trăm GB?",
            "options": [
                "`repartition(1)` kích hoạt một pha `Full Shuffle` gom toàn bộ hàng trăm GB dữ liệu của tất cả các Executors qua mạng dồn về duy nhất `1 Task trên 1 Executor Core` để tuần tự hóa và ghi 1 tệp khổng lồ, xóa sạch tính song song của cụm và cực dễ gây nổ OOM/Disk Spill ở Executor đó.",
                "`repartition(1)` làm mất tên các cột trong tệp Parquet đầu ra.",
                "Hàm `write.parquet()` trong Spark không cho phép truyền số `1` vào hàm `repartition`.",
                "`repartition(1)` chỉ ghi dữ liệu vào bộ nhớ RAM chứ không ghi xuống S3."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Kiến trúc Tối ưu hóa Toàn diện): Hãy trình bày phác đồ cải tổ đường ống này theo 3 trụ cột: "
                "(1) Cách giải quyết bài toán nối 2 bảng lớn (`2 TB` join `400 GB`) bị lệch khóa (`Skewed Key`) bằng `AQE` hoặc kỹ thuật `Key Salting (Muối khóa 1..N + Explode)`? "
                "(2) Cơ chế `Unified Memory Manager` (Storage vs Execution Memory) hoạt động ra sao và tại sao lạm dụng `.cache()` mà không `.unpersist()` lại gây `Disk Spill` dây chuyền? "
                "(3) Thay thế `repartition(1)` bằng cấu hình nào để vừa ghi song song tốc độ cao vừa tránh đẻ tệp nhỏ (`Small Files`)?"
            ),
            "rubric": {
                "coreConcepts": [
                    "Giải thích đúng kỹ thuật xử lý nối 2 bảng lớn bị Skew (không Broadcast được vì bảng kia 400 GB): bật `spark.sql.adaptive.enabled=true` + `spark.sql.adaptive.skewJoin.enabled=true` (AQE tự động cắt phân vùng quá cỡ thành các sub-partitions), hoặc dùng `Key Salting` (gắn hậu tố ngẫu nhiên `0..K-1` vào khóa bị lệch ở bảng lớn và nhân bản `explode` khóa đó thành `K` dòng ở bảng đối ứng).",
                    "Giải thích đúng `Unified Memory Manager`: vùng `Storage Memory` (chứa dữ liệu `.cache()`) và `Execution Memory` (dùng cho Shuffle/Join/Sort) dùng chung một bể bộ nhớ động; nếu giữ `.cache()` không giải phóng bằng `.unpersist()`, vùng Execution bị chèn ép buộc các phép SortMergeJoin phải tràn dữ liệu xuống đĩa (`Disk Spill`).",
                    "Thay thế `repartition(1)`: dùng `coalesce(N)` (gộp phân vùng tại chỗ không Shuffle) hoặc dùng `spark.sql.files.maxRecordsPerFile` / `AQE Coalesce Partitions` để các Executors ghi song song ra các tệp Parquet chuẩn 256MB–512MB."
                ],
                "tradeoffs": [
                    "Nêu rõ đánh đổi của `Key Salting`: bảng đối ứng phải nhân bản các khóa bị muối lên `K` lần, nên chỉ áp dụng có chọn lọc (Selective Salting) cho đúng danh sách các khóa thực sự bị lệch nặng (`Hot Keys`) thay vì muối toàn bộ bảng."
                ],
                "referenceAnswer": (
                    "1. Vì bảng `user_profiles` nặng `400 GB` không thể Broadcast, ta bật `AQE Skew Join` (`spark.sql.adaptive.skewJoin.enabled=true`) hoặc áp dụng **Selective Key Salting**: chỉ với các `user_id` nằm trong danh sách Hot Keys, nối thêm muối ngẫu nhiên `concat(user_id, '_', rand(0..15))` ở bảng `events` (2 TB) và `explode(array(0..15))` cho riêng các khóa nóng đó ở bảng `user_profiles` để chia tải đều ra 16 Tasks song song.\n"
                    "2. Trong `Unified Memory Manager`, dữ liệu `cache()` chiếm giữ `Storage Memory`; nếu không gọi `.unpersist()` ngay sau khi dùng xong, vùng `Execution Memory` bị thu hẹp khiến phép `SortMergeJoin` thiếu RAM và phải `Spill-to-Disk`. Ngoài ra cần chọn `StorageLevel.MEMORY_AND_DISK_SER` kết hợp `KryoSerializer` nếu thực sự cần cache.\n"
                    "3. Bỏ ngay `repartition(1)`; thay bằng bật `spark.sql.adaptive.coalescePartitions.enabled=true` kết hợp `option('maxRecordsPerFile', 5000000)` (hoặc `coalesce(K)` với `K` hợp lý theo tổng dung lượng chia 256MB) để toàn bộ Executors ghi song song ra các tệp Parquet đều đặn."
                )
            }
        }
    },

    # --------------------------------------------------------------------------
    # D04 · TRANSFORMATION LAYER II (STREAM · APACHE FLINK)
    # --------------------------------------------------------------------------
    {
        "id": "D04-BP-01",
        "topic": "D04",
        "stage": 2,
        "stationId": "flink-2-2",
        "stationTitle": "Trạm 1.2–6.2: Event Time & Watermark W(t), Allowed Lateness/Side Output, RocksDB Checkpoint & Backpressure",
        "roleTracks": ["DE", "AIE", "MLE"],
        "skillName": "Apache Flink Event-Time Watermarks, Window Lifecycle, Chandy-Lamport Checkpoints & Backpressure",
        "invariant": (
            "Đồng hồ logic `Watermark W(t) = max(event_time) - allowed_delay` đo tiến trình của Event Time: một cửa sổ `[start, end)` sẽ điểm hỏa (fire) ngay khi `W(t) >= end`; "
            "khi hợp nhất nhiều phân vùng nguồn (Kafka Partitions), toán tử hạ nguồn lấy `Watermark = min(W_1, W_2, ..., W_k)` — do đó nếu 1 Partition bị rỗng (Idle), Watermark toàn cục sẽ bị đóng băng nếu không bật `.withIdleness()`."
        ),
        "misconceptions": [
            "Dùng `Processing Time` để tính doanh số theo khung giờ khuyến mãi rồi thắc mắc tại sao mỗi lần chạy lại (Replay) từ Kafka lại ra một con số khác nhau.",
            "Tưởng rằng khi 1 trong 8 Kafka Partitions không có sự kiện mới, đồng hồ Watermark của Flink vẫn tự động chạy tiếp theo giờ máy chủ.",
            "Dùng `GlobalWindows` mà quên gắn `Trigger` tùy chỉnh khiến trạng thái phình vô hạn làm sập TaskManager."
        ],
        "L1": {
            "stem": (
                "Một đường ống Apache Flink dùng `Event Time` với chiến lược `BoundedOutOfOrderness` có độ trễ cho phép `allowed_delay = 10 giây` để tính tổng tiền theo cửa sổ `Tumbling Window [10:00:00 – 10:01:00)`. "
                "Luồng sự kiện lần lượt đi vào toán tử với nhãn thời gian `event_time` là: `10:00:42`, `10:00:58`, `10:00:51`, `10:01:10`. "
                "Tại thời điểm sự kiện nào đi qua thì cửa sổ `[10:00:00 – 10:01:00)` chính thức đóng lại và phát kết quả?"
            ),
            "options": [
                "Ngay khi sự kiện có `event_time = 10:01:10` đi qua: lúc này `max_event_time = 10:01:10`, suy ra đồng hồ `Watermark W(t) = 10:01:10 - 10s = 10:01:00`, thỏa mãn điều kiện điểm hỏa `W(t) >= window_end (10:01:00)`.",
                "Ngay khi sự kiện `10:00:58` đi qua vì nó là sự kiện cuối cùng thuộc về phút `10:00`.",
                "Khi đồng hồ treo tường của máy chủ vật lý chạy Flink TaskManager điểm đúng `10:01:00`.",
                "Khi sự kiện `10:00:51` đi qua vì nó đến sau sự kiện `10:00:58`."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 2.2 (D04): Công thức đồng hồ logic Watermark với độ trễ cố định là `W(t) = max(event_time_seen) - t_d`. "
                "Với `t_d = 10s`: khi gặp `10:00:58`, `W(t) = 10:00:48 < 10:01:00` (chưa đóng). "
                "Khi gặp `10:00:51`, `max` vẫn là `10:00:58` nên `W(t)` giữ nguyên `10:00:48`. "
                "Chỉ khi gặp `10:01:10`, `W(t) = 10:01:10 - 10s = 10:01:00 >= window_end`, kích hoạt `EventTimeTrigger` đóng cửa sổ!"
            ),
            "distractorReasons": [
                "Chính xác: Áp dụng đúng công thức bất biến `W(t) = max(event_time) - allowed_delay >= window_end`.",
                "Sai: Lúc gặp `10:00:58`, Flink vẫn phải chờ thêm 10 giây Event Time nữa phòng trường hợp còn các sự kiện của phút `10:00` bị trễ mạng chưa tới.",
                "Sai: Đó là `Processing Time`, còn `Event Time` chỉ tiến lên dựa theo nhãn thời gian của dữ liệu đi vào.",
                "Sai: Sự kiện đến muộn `10:00:51 < 10:00:58` không làm giảm cũng không làm tăng `max_event_time`."
            ]
        },
        "L2": {
            "stem": (
                "Đường ống Flink đọc từ một Topic Kafka có `4 Partitions`. Vào ban đêm, khu vực miền núi (gắn cố định vào `Partition 3`) không phát sinh bất kỳ đơn hàng nào suốt 2 tiếng đồng hồ, "
                "trong khi `Partition 0, 1, 2` vẫn nhận hàng chục nghìn đơn hàng mỗi phút. "
                "Đột nhiên toàn bộ Dashboard thời gian thực ngừng cập nhật kết quả của cả 4 vùng, và bộ nhớ State của toán tử Window tăng vọt không ngừng dù không có lỗi nào trong log! "
                "Nguyên nhân cơ học và cách sửa chuẩn xác trong Flink là gì?"
            ),
            "codeSnippet": (
                "WatermarkStrategy.<OrderEvent>forBoundedOutOfOrderness(Duration.ofSeconds(10))\n"
                "    .withTimestampAssigner((event, ts) -> event.getCreatedAt())"
            ),
            "options": [
                "Toán tử Window hợp nhất đồng hồ từ các luồng đầu vào theo công thức `Watermark_merged = min(W_0, W_1, W_2, W_3)`; vì `Partition 3` rỗng (`Idle Partition`) nên `W_3` đứng im ở mốc cũ khiến `min(...)` bị đóng băng hoàn toàn, không một cửa sổ nào điểm hỏa hay giải phóng State được! Phải chuỗi thêm `.withIdleness(Duration.ofMinutes(1))` vào `WatermarkStrategy`.",
                "Do Flink tự động tạm dừng toàn bộ JobManager nếu bất kỳ Kafka Partition nào có tốc độ bằng 0.",
                "Do `BoundedOutOfOrderness(10s)` quá lớn, cần giảm xuống `0 giây` (`forMonotonousTimestamps`) thì Partition rỗng mới tự chạy đồng hồ.",
                "Do RocksDB StateBackend tự động khóa các bảng băm khi có số lượng Partition là số chẵn."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 2.2 (D04): Flink cập nhật Watermark tại toán tử nhận nhiều luồng bằng cách lấy giá trị nhỏ nhất `min(W_i)` để đảm bảo không bỏ sót dữ liệu của luồng chậm nhất. "
                "Khi một phân vùng hoàn toàn không có sự kiện mới (`Idle Source`), `W_3` không nhích lên được, kéo tụt đồng hồ của cả cụm. "
                "Bật `.withIdleness(Duration.ofMinutes(1))` giúp đánh dấu phân vùng rỗng là `Idle` để tạm thời loại nó khỏi phép tính `min(W_i)`."
            ),
            "distractorReasons": [
                "Chính xác: Giải thích đúng cơ học `min(W_0..W_k)` khi gặp Idle Kafka Partition và phương thức `.withIdleness()`.",
                "Sai: JobManager và các Sub-tasks khác vẫn đọc dữ liệu bình thường, chỉ có các cửa sổ Event Time không thể đóng lại vì Watermark bị ghim.",
                "Sai: Kể cả dùng `forMonotonousTimestamps()`, nếu Partition 3 không có bản ghi mới thì `W_3` vẫn đứng im.",
                "Sai: RocksDB hoàn toàn không phụ thuộc vào số lượng Partition chẵn hay lẻ."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Kiến trúc Streaming Chịu lỗi & Hiệu năng Cao (Chặng 3, 5, 6): Hệ thống phát hiện gian lận thanh toán chạy trên Apache Flink xử lý `80.000 sự kiện/giây`, giữ trạng thái lịch sử giao dịch (`Keyed State`) nặng `600 GB`. "
                "Bạn phải giải quyết 3 bài toán vận hành: "
                "(1) Vẫn có khoảng 0.5% sự kiện từ thiết bị di động đi qua hầm gửi về trễ hơn `Watermark (10s)`, trong đó có những sự kiện trễ tới 20 giây và có những sự kiện trễ tới 2 giờ; "
                "(2) Khi một TaskManager sập, hệ thống phải khôi phục mà không tính trùng hay mất tiền (`Exactly-Once`); "
                "(3) Hiện tại trên Flink Web UI, toán tử gọi cơ sở dữ liệu bên ngoài đang báo `Backpressure: HIGH (100% Busy)` lan ngược về tận Kafka Source."
            ),
            "mcqPrompt": "Phần A (Phác đồ Xử lý Sự kiện Trễ 3 Tầng): Tổ hợp nào xử lý trọn vẹn cả sự kiện trễ nhẹ (10–40s) lẫn sự kiện trễ sâu (2 giờ) mà không làm nổ RAM?",
            "options": [
                "Kết hợp `Watermark BoundedOutOfOrderness(10s)` + `Allowed Lateness(30s)` (giữ cửa sổ ở pha Waiting để tính lại & phát bản ghi đính chính cho các sự kiện trễ nhẹ) + `Side Output (OutputTag)` để hứng 100% các sự kiện đến sau khi cửa sổ đã `Deleted` (trễ 2 giờ) đẩy sang luồng ghi S3/đối soát mà không giữ State cửa sổ vô hạn.",
                "Tăng độ trễ `BoundedOutOfOrderness` lên thành `2 giờ` để mọi cửa sổ đều phải chờ đủ 2 tiếng mới được phát kết quả.",
                "Tắt hoàn toàn cơ chế xóa cửa sổ để giữ mọi cửa sổ trong RAM vĩnh viễn.",
                "Mặc kệ cho Flink âm thầm vứt bỏ (`Drop`) toàn bộ 0.5% giao dịch thanh toán đến muộn."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Bảo vệ Kiến trúc State, Checkpoint & Trị Backpressure): Hãy giải thích: "
                "(1) Tại sao với `600 GB State` bắt buộc phải chọn `EmbeddedRocksDBStateBackend` (bật `Incremental Checkpoints`) thay vì `HashMapStateBackend`, và rào chắn `Checkpoint Barrier (Chandy-Lamport)` phối hợp với Kafka Offset như thế nào khi phục hồi sự cố? "
                "(2) Phác đồ 3 bước để xử lý dứt điểm điểm nghẽn `Backpressure HIGH` ở toán tử tra cứu I/O bên ngoài là gì?"
            ),
            "rubric": {
                "coreConcepts": [
                    "So sánh đúng `HashMapStateBackend` (lưu đối tượng trên JVM Heap, giới hạn vài GB, dễ OOM & GC pause) với `EmbeddedRocksDBStateBackend` (lưu chuỗi byte trên bộ nhớ Off-heap + đĩa NVMe SSD theo cấu trúc LSM-Tree SSTables, chịu được hàng TB và hỗ trợ `Incremental Checkpoints` chỉ đẩy các tệp SSTable mới sinh lên S3).",
                    "Giải thích đúng cơ chế `Chandy-Lamport Checkpoint Barrier`: JobManager bơm rào chắn `#N` chảy dọc luồng sự kiện; khi toán tử nhận Barrier, nó chụp ảnh State bất đồng bộ xuống S3 đồng thời lưu vị trí `Kafka Offset #N`. Khi Worker sập, Flink nạp lại State từ Checkpoint `#N` và tua ngược (`rewind`) Kafka Source về đúng Offset `#N` (kết hợp `TwoPhaseCommitSink` để đạt End-to-End Exactly-Once).",
                    "Phác đồ trị `Backpressure HIGH` (Credit-based flow control): (a) Đổi lời gọi đồng bộ sang `AsyncDataStream (Async I/O)` kết nối kèm bộ đệm Redis, (b) Tăng `Parallelism` cho toán tử nghẽn và giữ `Operator Chaining` cho các bước biến đổi nhẹ, (c) Tinh chỉnh `RocksDB Block Cache / Write Buffer`."
                ],
                "tradeoffs": [
                    "Nêu rõ yêu cầu đối với hệ thống hạ nguồn khi bật `Allowed Lateness`: mỗi lần sự kiện trễ kích hoạt `Window Refire`, Flink phát bản ghi cập nhật nên bảng đích phải hỗ trợ `Upsert / Retract` theo khóa cửa sổ thay vì chỉ `Append`."
                ],
                "referenceAnswer": (
                    "1. Với `600 GB State`, `HashMapStateBackend` trên JVM Heap chắc chắn sập OOM. Dùng `EmbeddedRocksDBStateBackend` lưu dữ liệu ngoài Heap + ổ NVMe theo cấu trúc `LSM-Tree` (các tệp `SSTable` bất biến), cho phép bật `Incremental Checkpoints` chỉ tải lên S3 những tệp SSTable mới kể từ lần chụp trước. Khi sập node, Flink khôi phục ảnh chụp State `#N` và tua ngược Kafka Consumer về đúng `Offset #N` tại thời điểm rào chắn `Checkpoint Barrier #N` đi qua.\n"
                    "2. Để phá điểm nghẽn `Backpressure HIGH` (do hết Input Credit lan ngược về Source): thay thế lời gọi tra cứu đồng bộ bằng `AsyncDataStream.unorderedWait()` (Async I/O gửi hàng trăm request không chặn luồng), tăng `.setParallelism()` cho toán tử nặng, và đảm bảo các toán tử nhẹ liền kề được hàn gắn (`Operator Chaining`) để truyền bản ghi trực tiếp trong RAM không tốn phí tuần tự hóa."
                )
            }
        }
    },

    # --------------------------------------------------------------------------
    # D05 · CONSUMPTION LAYER (KIMBALL DWH, SCD, CLICKHOUSE/PINOT, FEAST)
    # --------------------------------------------------------------------------
    {
        "id": "D05-BP-01",
        "topic": "D05",
        "stage": 5,
        "stationId": "consumption-5-3",
        "stationTitle": "Trạm 2.2–5.3: Kimball Star Schema, SCD Type 2, ClickHouse/Pinot OLAP & Feast Point-in-Time ASOF Join",
        "roleTracks": ["DE", "AIE", "MLE"],
        "skillName": "Dimensional Modeling (Grain/SCD2), Real-Time OLAP (ClickHouse/Pinot) & Feast Feature Store",
        "invariant": (
            "Trong Kimball Dimensional Modeling, `Fact Table` phải khóa chặt một Độ mịn (`Grain`) đồng nhất và dùng khóa thay thế (`Surrogate Key`) nối tới `Dimension Table` có theo dõi lịch sử `SCD Type 2` (`effective_from`, `effective_to`, `is_current`); "
            "trong ML Feature Store (Feast), khi tạo tập huấn luyện lịch sử (`get_historical_features`), bắt buộc dùng `Point-in-Time Correctness (ASOF Join: feature_ts <= event_ts)` để chặn đứng `Data Leakage (Future Peeking)` và đồng bộ cùng một định nghĩa đặc trưng giữa `Offline Store` và `Online Store (Redis)` để triệt tiêu `Training-Serving Skew`."
        ),
        "misconceptions": [
            "Dùng `INNER JOIN` hoặc lấy bản ghi mới nhất (`WHERE is_current = true`) của bảng đặc trưng khi tạo dữ liệu huấn luyện cho các giao dịch xảy ra từ 6 tháng trước (gây rò rỉ dữ liệu tương lai nghiêm trọng!).",
            "Cộng gộp trực tiếp một thước đo bán cộng tính (`Semi-Additive Measure` như số dư tài khoản `account_balance` hay tồn kho `inventory_level`) qua chiều Thời gian (`SUM(inventory_level) GROUP BY year`).",
            "Tưởng rằng `Sparse Primary Index` của ClickHouse tạo một mục chỉ mục cho từng dòng đơn lẻ giống như B-Tree của PostgreSQL."
        ],
        "L1": {
            "stem": (
                "Trong thiết kế Kho dữ liệu theo phương pháp Kimball (`Star Schema`), tại sao thước đo số lượng tồn kho cuối ngày (`inventory_balance`) hoặc số dư tài khoản ngân hàng (`account_balance`) "
                "được phân loại là **Thước đo Bán cộng tính (`Semi-Additive Fact`)** và quy tắc tổng hợp bắt buộc của nó là gì?"
            ),
            "options": [
                "Vì ta CÓ THỂ cộng tổng (`SUM`) tồn kho của nhiều kho hàng/sản phẩm tại cùng một thời điểm, nhưng TUYỆT ĐỐI KHÔNG ĐƯỢC cộng tổng (`SUM`) tồn kho qua chiều Thời gian (`DimDate` — cộng tồn kho ngày thứ Hai là 100 hộp với ngày thứ Ba là 100 hộp thành 200 hộp là sai bản chất!); qua chiều thời gian phải dùng `AVG`, `LAST_VALUE` hoặc lấy mốc cuối kỳ.",
                "Vì cột tồn kho chỉ cho phép cộng vào các ngày chẵn trong tháng và cấm cộng vào ngày lẻ.",
                "Vì thước đo Bán cộng tính chỉ được phép dùng hàm `COUNT(*)` chứ không bao giờ được dùng hàm `SUM()` trên bất kỳ chiều nào.",
                "Vì tồn kho là dữ liệu văn bản nên phải lưu trong bảng `Dimension` thay vì bảng `Fact`."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 2.1 (D05): Ba loại thước đo trong Fact Table gồm: "
                "(1) `Additive` (Doanh thu, số lượng bán — cộng được qua mọi chiều), "
                "(2) `Semi-Additive` (Số dư, tồn kho — cộng được qua Kho/Sản phẩm nhưng KHÔNG cộng được qua Thời gian), "
                "và (3) `Non-Additive` (Tỷ suất lợi nhuận %, đơn giá — không cộng trực tiếp được qua bất kỳ chiều nào)."
            ),
            "distractorReasons": [
                "Chính xác: Cộng được qua các chiều không gian (Kho, Sản phẩm, Chi nhánh) nhưng cấm cộng dồn qua chiều Thời gian (Point-in-time snapshot).",
                "Sai: Tính chất Semi-Additive phụ thuộc vào chiều phân tích (Dimension), không phải ngày chẵn lẻ.",
                "Sai: Thước đo không cộng được trên mọi chiều là `Non-Additive` (như tỷ lệ %), còn `Semi-Additive` vẫn dùng `SUM()` hợp lệ trên các chiều phi thời gian.",
                "Sai: Số lượng tồn kho là thước đo định lượng nằm trong `Periodic Snapshot Fact Table`."
            ]
        },
        "L2": {
            "stem": (
                "Một kỹ sư ML chuẩn bị dữ liệu huấn luyện cho mô hình phát hiện gian lận thẻ tín dụng. "
                "Giao dịch `txn_9f3a` diễn ra lúc `10:00 sáng ngày 01/06`, và đến `10:05 sáng ngày 01/06` hệ thống mới phát hiện thẻ đó bị lộ và cập nhật đặc trưng `failed_txns_1h = 15`. "
                "Kỹ sư viết câu lệnh `JOIN` thông thường lấy giá trị cuối ngày của bảng đặc trưng ghép vào giao dịch lúc `10:00`. "
                "Mô hình đạt độ chính xác `AUC = 0.998` khi huấn luyện Offline nhưng khi đưa lên Production chấm điểm trực tuyến lại đoán sai thảm hại (`AUC = 0.54`)! "
                "Sai lầm chí mạng nào đã xảy ra và hàm nào của **Feast Feature Store** giải quyết tận gốc?"
            ),
            "codeSnippet": (
                "# Lỗi kinh điển khi tự viết SQL nối dữ liệu huấn luyện:\n"
                "SELECT t.txn_id, t.event_ts, t.is_fraud, f.failed_txns_1h\n"
                "FROM transactions t\n"
                "JOIN user_features_daily f ON t.user_id = f.user_id"
            ),
            "options": [
                "Câu lệnh `JOIN` không ràng buộc mốc thời gian đã lấy giá trị đặc trưng của tương lai (`10:05`) gắn ngược vào quá khứ (`10:00`), gây **Rò rỉ Dữ liệu Tương lai (`Data Leakage / Future Peeking`)**; bắt buộc phải dùng `store.get_historical_features(entity_df=..., features=...)` của Feast để thực hiện phép nối **Point-in-Time ASOF Join (`feature_ts <= event_ts` gần nhất trong cửa sổ TTL)**.",
                "Do mô hình XGBoost không hỗ trợ các cột đặc trưng có kiểu số nguyên `failed_txns_1h`.",
                "Do bộ nhớ đệm `Redis Online Store` làm tròn số thực khác với cơ sở dữ liệu Offline.",
                "Chỉ cần xóa cột `is_fraud` khỏi tập huấn luyện là điểm AUC trên Production sẽ tăng lên 0.998."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 5.2 & 5.3 (D05): Tại thời điểm `10:00:00` khi giao dịch thật diễn ra trên Production, hệ thống không thể biết chuyện sẽ xảy ra lúc `10:05:00`! "
                "Việc ghép đặc trưng tương lai vào lúc huấn luyện tạo ra ảo giác `AUC = 0.998`. "
                "Hàm `get_historical_features()` của Feast thực hiện phép `ASOF Join` lùi về quá khứ: với mỗi giao dịch tại `t_event`, chỉ lấy trạng thái đặc trưng mới nhất thỏa mãn `t_feature <= t_event`."
            ),
            "distractorReasons": [
                "Chính xác: Chẩn đoán đúng bệnh Data Leakage (Future Peeking) và cơ chế Point-in-Time ASOF Join của Feast.",
                "Sai: XGBoost xử lý hoàn hảo cả số nguyên lẫn số thực.",
                "Sai: Nguyên nhân sụt giảm từ 0.998 xuống 0.54 ở đây là do nhìn trộm tương lai lúc train, không phải sai số dấu chấm động.",
                "Sai: `is_fraud` là nhãn mục tiêu (Target Label) của bài toán học có giám sát, không thể xóa."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Thiết kế Tầng Consumption Toàn diện (DWH + Real-Time OLAP + Feature Store): "
                "Bạn thiết kế tầng phục vụ dữ liệu cho siêu ứng dụng Tài chính – Thương mại điện tử gồm 3 nhu cầu: "
                "(1) Báo cáo tài chính lịch sử cần biết chính xác đơn hàng `#8888` năm ngoái thuộc về chi nhánh cũ (`Bình Dương`) của khách hàng dù năm nay khách đã chuyển khẩu về `TP.HCM`; "
                "(2) Dashboard vận hành cho 10.000 nhà bán hàng truy vấn phân tích tức thời (`p99 < 150ms`) trên bảng 20 tỷ dòng vừa kết hợp luồng Kafka thời gian thực vừa kết hợp lịch sử trên S3; "
                "(3) Dịch vụ chấm điểm tín dụng trực tuyến cần lấy 30 đặc trưng của khách hàng trong `< 5ms`."
            ),
            "mcqPrompt": "Phần A (Quyết định Kiến trúc 3 Thành phần): Tổ hợp thiết kế nào giải quyết chính xác cả 3 bài toán (1), (2), (3)?",
            "options": [
                "(1) Dùng `SCD Type 2` trên `DimCustomer` (sinh dòng mới với `Surrogate Key` mới + đóng `effective_to` của dòng cũ) để `FactOrders` trỏ đúng vào `customer_sk` tại thời điểm mua; (2) Dùng động cơ OLAP hướng cột thực thi Vector hóa `SIMD` như `ClickHouse (MergeTree Sparse Index)` hoặc `Apache Pinot (Hybrid Table + Star-Tree Index)`; (3) Dùng `Feast Feature Store` đồng bộ (`materialize-incremental`) từ Offline DWH sang `Online Store (Redis)` để đọc qua `get_online_features()` trong `< 5ms`.",
                "(1) Dùng `SCD Type 1` ghi đè thẳng địa chỉ mới đè mất địa chỉ cũ; (2) Cho 10.000 nhà bán hàng chạy `SELECT GROUP BY` trực tiếp trên PostgreSQL OLTP nguồn; (3) Khi khách bấm vay tiền mới bắt đầu chạy job Spark Batch quét 20 tỷ dòng để tính đặc trưng.",
                "Lưu toàn bộ 20 tỷ dòng vào bộ nhớ `Redis` để chạy câu lệnh `GROUP BY` phức tạp.",
                "Dùng `SCD Type 0` cấm khách hàng đổi địa chỉ suốt đời."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Giải phẫu Cơ học Nội tại): Hãy giải thích sâu 3 cơ chế: "
                "(1) Tại sao trong `SCD Type 2` bắt buộc bảng `Fact` phải nối với bảng `Dimension` qua khóa thay thế (`Surrogate Key: customer_sk`) thay vì khóa tự nhiên (`Natural Key: customer_id`)? "
                "(2) Cơ chế `Sparse Primary Index` (chỉ mục thưa theo Granule `8.192 dòng`) kết hợp `Vectorized Execution (SIMD AVX-512)` của ClickHouse giúp quét hàng tỷ dòng nhanh hơn RDBMS truyền thống như thế nào? "
                "(3) Trong Apache Pinot, `Time Boundary` trong `Hybrid Table` vận hành ra sao để không đếm trùng dữ liệu giữa bảng Real-time và bảng Offline?"
            ),
            "rubric": {
                "coreConcepts": [
                    "Giải thích đúng vai trò của `Surrogate Key` trong SCD Type 2: một khách hàng có cùng `Natural Key (customer_id = 'C01')` sẽ sinh ra nhiều dòng lịch sử trong `DimCustomer`; nếu nối bằng `customer_id` sẽ gây nhân bản dòng (Fan-out) và không biết đơn hàng thuộc giai đoạn lịch sử nào — phải nối bằng `customer_sk` duy nhất cho từng phiên bản lịch sử.",
                    "Giải thích đúng cơ học `ClickHouse MergeTree`: dữ liệu được sắp xếp vật lý theo `ORDER BY` và chia thành các `Granules (8.192 dòng)`; `Sparse Primary Index` chỉ lưu 1 mục cho mỗi 8.192 dòng nên toàn bộ chỉ mục của hàng chục tỷ dòng vẫn nằm gọn trong RAM, kết hợp đọc theo cột và xử lý mảng vector hóa trên thanh ghi CPU `SIMD (AVX-2 / AVX-512)`.",
                    "Giải thích đúng `Apache Pinot Hybrid Table`: Pinot Broker tự động tách truy vấn tại mốc `Time Boundary` (ví dụ `max(end_time)` của các Segment Offline đã đẩy lên) — phần lịch sử `t <= Time_Boundary` đọc từ `Offline Table` (đã nén tối ưu + `Star-Tree Index` tính sẵn), phần mới nhất `t > Time_Boundary` đọc từ `Real-time Table` (nhận trực tiếp từ Kafka), đảm bảo không trùng cũng không sót."
                ],
                "tradeoffs": [
                    "Nêu rõ đặc điểm của ClickHouse vs Pinot: ClickHouse cực mạnh cho truy vấn OLAP quét/nén linh hoạt quy mô lớn, trong khi Pinot được tối ưu chuyên biệt cho User-facing Real-time Analytics có QPS cực cao (hàng chục nghìn truy vấn đồng thời từ người dùng cuối) nhờ chỉ mục `Star-Tree`."
                ],
                "referenceAnswer": (
                    "1. Trong `SCD Type 2`, mỗi lần khách đổi tỉnh thành sẽ sinh một dòng mới có cùng `customer_id` nhưng khác `customer_sk` (`Surrogate Key`). Bảng `FactOrders` lưu `customer_sk` tại đúng thời điểm giao dịch giúp truy vấn `JOIN ON f.customer_sk = d.customer_sk` gắn đúng đơn hàng năm ngoái vào `Bình Dương` và đơn năm nay vào `TP.HCM` mà không cần điều kiện lọc khoảng thời gian phức tạp.\n"
                    "2. `ClickHouse MergeTree` sắp xếp dữ liệu trên đĩa và gom thành từng khối `Granule 8.192 dòng`. Nhờ đó `Sparse Index` nhỏ hơn 8.192 lần so với B-Tree (luôn nằm trọn trong RAM), và khi quét các cột đã nén liền kề, động cơ nạp cả mảng giá trị vào thanh ghi vector `SIMD (AVX-512)` để cộng/lọc hàng chục phần tử trong đúng 1 chu kỳ xung nhịp CPU.\n"
                    "3. Với `Apache Pinot Hybrid Table`, Broker duy trì mốc `Time Boundary` tự động: phần dữ liệu `t <= Time_Boundary` truy vấn trên `Offline Segments`, còn phần `t > Time_Boundary` truy vấn trên `Realtime Segments` đang đọc Kafka, sau đó gộp kết quả trả về trong vài chục mili-giây."
                )
            }
        }
    },

    # --------------------------------------------------------------------------
    # D06 · ORCHESTRATION & GOVERNANCE LAYERS (AIRFLOW, GX/DEEQU, DATAHUB)
    # --------------------------------------------------------------------------
    {
        "id": "D06-BP-01",
        "topic": "D06",
        "stage": 3,
        "stationId": "orchestration-3-4",
        "stationTitle": "Trạm 2.2–5.4: Idempotency/Backfill, Deferrable Sensors, XCom URI, Circuit Breaker & DataHub Lineage",
        "roleTracks": ["DE", "AIE", "MLE"],
        "skillName": "Airflow Architecture (Deferrable Triggerer, XCom, Concurrency Pools), Idempotency & Data Contracts",
        "invariant": (
            "Một tác vụ đường ống dữ liệu bắt buộc phải đạt tính Lũy đẳng (`Idempotency: f(f(x)) = f(x)`) và tham số hóa theo khung thời gian logic (`data_interval_start` / `data_interval_end`, cấm dùng `NOW()` / `CURRENT_DATE`) để khi Retry hoặc Backfill không bao giờ gây nhân bản dòng hay lệch ngày; "
            "trong Apache Airflow, `XCom` nằm trong bảng Metadata DB nên chỉ dùng để truyền siêu dữ liệu/con trỏ đường dẫn nhỏ (`Pass-by-Reference URI < vài KB`), và các Sensor chờ lâu phải dùng `deferrable=True` (Async Triggerer) hoặc `mode='reschedule'` để tránh làm cạn sạch Worker Slots (`Sensor Deadlock`)."
        ),
        "misconceptions": [
            "Viết câu lệnh `INSERT INTO daily_sales SELECT ... WHERE dt = CURRENT_DATE` trong Airflow DAG rồi chạy lệnh `airflow dags backfill` cho 30 ngày tháng trước.",
            "Truyền nguyên một `pandas.DataFrame` nặng `2 GB` giữa hai Task bằng `ti.xcom_push()`.",
            "Cấu hình 32 `S3KeySensor` ở chế độ mặc định `mode='poke'` trên một cụm chỉ có 32 Worker Slots khiến toàn bộ cụm bị khóa chết (Deadlock)."
        ],
        "L1": {
            "stem": (
                "Một kỹ sư viết DAG trong Apache Airflow để tổng hợp doanh số mỗi ngày bằng câu lệnh SQL:\n"
                "`INSERT INTO gold.daily_revenue SELECT CURRENT_DATE, sum(amount) FROM silver.orders WHERE order_date = CURRENT_DATE;`\n"
                "Chuyện gì sẽ xảy ra khi: (1) Task bị lỗi mạng ở bước cuối và Airflow tự động chạy lại (`Retry`) lần thứ 2 trong cùng ngày, hoặc (2) Kỹ sư chạy lệnh `Backfill` cho 7 ngày tuần trước?"
            ),
            "options": [
                "Vi phạm hoàn toàn cả hai nguyên lý **Tính lũy đẳng (`Idempotency`)** và **Thời gian Logic (`Data Interval`)**: khi Retry, lệnh `INSERT` thuần túy không xóa/ghi đè phân vùng cũ sẽ làm **nhân đôi doanh số**; còn khi Backfill cho 7 ngày tuần trước, hàm `CURRENT_DATE` luôn lấy ngày hôm nay nên hệ thống sẽ chèn 7 lần dữ liệu của ngày hôm nay thay vì dữ liệu của tuần trước!",
                "Airflow sẽ tự động dịch từ khóa `CURRENT_DATE` bên trong chuỗi SQL sang ngày của tuần trước và tự động xóa dữ liệu trùng.",
                "Khi chạy `Backfill`, PostgreSQL sẽ tự động đổi đồng hồ hệ điều hành của máy chủ lùi về quá khứ.",
                "Lệnh `INSERT INTO` trong SQL mặc định luôn tự động ghi đè lên các dòng đã tồn tại mà không bao giờ sinh bản ghi trùng."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 2.2 & 2.3 (D06): Mọi Task trong Airflow phải dùng biến ngữ cảnh thời gian logic (`{{ ds }}` / `data_interval_start`) thay vì `CURRENT_DATE`, "
                "và phải dùng mẫu thiết kế lũy đẳng (`DELETE WHERE dt = '{{ ds }}' + INSERT`, hoặc `INSERT OVERWRITE PARTITION`, hoặc `MERGE / UPSERT`) để chạy lại 1 lần hay 100 lần vẫn ra đúng 1 kết quả duy nhất."
            ),
            "distractorReasons": [
                "Chính xác: Chỉ rõ 2 lỗi chí mạng (dùng `INSERT` không lũy đẳng gây nhân bản dòng + dùng `CURRENT_DATE` làm hỏng hoàn toàn Backfill).",
                "Sai: Airflow chỉ biên dịch các biến Jinja template như `{{ ds }}`, không tự ý sửa từ khóa `CURRENT_DATE` của động cơ SQL.",
                "Sai: Không một cơ sở dữ liệu nào tự đổi đồng hồ hệ điều hành khi nhận truy vấn.",
                "Sai: `INSERT INTO` chỉ nối thêm dòng mới (Append); nếu không có khóa chính + `ON CONFLICT` hoặc xóa phân vùng trước thì mỗi lần chạy lại sẽ nhân bản toàn bộ dữ liệu."
            ]
        },
        "L2": {
            "stem": (
                "Trên cụm Apache Airflow Production có cấu hình `32 Worker Slots`, đội kỹ sư triển khai 40 DAGs chạy lúc `01:00 sáng`. "
                "Mỗi DAG bắt đầu bằng một `S3KeySensor` chờ tệp đối soát từ đối tác (thường tới lúc `01:45`), sau đó mới chạy `PythonOperator` đọc tệp `2.5 GB` lên Pandas DataFrame rồi trả về (`return df`) để đẩy qua `XCom` sang Task tiếp theo. "
                "Lúc `01:05`, toàn bộ cụm Airflow bị treo cứng: không một Task nào trong toàn công ty chạy được dù CPU của các Worker chỉ ở mức `1%`, và khi có tệp về thì Worker + Metadata DB đồng loạt sập `OutOfMemoryError`! "
                "Giải phẫu nguyên nhân kép và cách sửa chuẩn kiến trúc là gì?"
            ),
            "codeSnippet": (
                "# Cấu hình gây thảm họa kép trên Airflow:\n"
                "wait_s3 = S3KeySensor(task_id='wait_file', bucket_key='s3://partner/data_{{ ds }}.parquet')  # default mode='poke'\n"
                "def load_data(**ctx):\n"
                "    return pd.read_parquet('s3://partner/data.parquet')  # Pushes 2.5GB DataFrame to XCom!"
            ),
            "options": [
                "Thảm họa 1 (`Sensor Deadlock`): `S3KeySensor` mặc định chạy ở `mode='poke'` giữ chặt `32/32 Worker Slots` chỉ để nằm ngủ (`time.sleep`) chờ tệp, làm tê liệt toàn cụm; phải đổi sang `deferrable=True` (nhường việc đợi I/O cho tiến trình `Asyncio Triggerer` tốn 0 Worker Slot) hoặc `mode='reschedule'`. Thảm họa 2 (`XCom Bloat`): `return df` tuần tự hóa cả `2.5 GB` nhét vào bảng `xcom` của PostgreSQL Metadata DB; phải lưu dữ liệu trên S3 và chỉ truyền chuỗi đường dẫn `S3 URI (< 200 Bytes)` qua XCom.",
                "Do `S3KeySensor` không hỗ trợ định dạng tệp `.parquet` nên làm treo bộ lập lịch `Scheduler`.",
                "Chỉ cần tăng thông số `poke_interval` từ 60 giây lên 3600 giây ở chế độ `mode='poke'` là 32 Worker Slots sẽ được giải phóng ngay lập tức.",
                "Do PostgreSQL Metadata DB không cho phép lưu chuỗi văn bản có chứa ký tự `s3://`."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo Trạm 3.3 & 3.4 (D06) và Mô phỏng 2D Kịch bản 1: "
                "Ở chế độ `mode='poke'` mặc định, Sensor chiếm dụng nguyên 1 Worker Slot suốt thời gian chờ. "
                "Chuyển sang `deferrable=True` giải phóng 100% Worker Slot cho tiến trình `Triggerer` bất đồng bộ. "
                "Đồng thời, `XCom (Cross-Communication)` chỉ dành cho siêu dữ liệu nhỏ (như `s3://bucket/path.parquet`, số dòng, mã phiên); dữ liệu nặng bắt buộc lưu trên Object Storage."
            ),
            "distractorReasons": [
                "Chính xác: Khắc phục triệt để cả Sensor Deadlock (bằng Deferrable Triggerer / Reschedule) lẫn XCom Bloat (bằng Pass-by-Reference URI).",
                "Sai: `S3KeySensor` chỉ kiểm tra sự tồn tại của Object Key trên S3 qua API `HeadObject`, không quan tâm nội dung bên trong là CSV hay Parquet.",
                "Sai: Ở chế độ `mode='poke'`, tăng `poke_interval` chỉ làm Worker ngủ lâu hơn trong lúc VẪN GIỮ CHẶT Worker Slot đó!",
                "Sai: Đường dẫn chuỗi `s3://...` chỉ dài vài chục byte, hoàn toàn là dữ liệu chuẩn mực để truyền qua XCom."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Thiết kế Hệ thống Điều phối & Quản trị Dữ liệu (Chặng 4 & 5): "
                "Bạn phụ trách nền tảng dữ liệu gồm 50 DAGs chạy trên Airflow: "
                "(1) Có 15 DAGs cùng trích xuất dữ liệu từ một máy chủ PostgreSQL OLTP sản xuất (chỉ chịu được tối đa 5 kết nối ETL đồng thời); "
                "(2) Hôm qua, dịch vụ Checkout thượng nguồn tự ý đổi tên cột `user_id` thành `customer_id` và xuất hiện một lô đơn hàng bị lỗi âm tiền (`amount = -450000`), chảy thẳng vào bảng `gold.fact_revenue` làm sai lệch báo cáo CEO và làm hỏng mô hình ML hạ nguồn."
            ),
            "mcqPrompt": "Phần A (Kiểm soát Đồng thời & Ngắt mạch Chất lượng): Tổ hợp kiến trúc nào bảo vệ tuyệt đối cả DB nguồn lẫn kho dữ liệu Gold?",
            "options": [
                "Tạo một `Airflow Resource Pool` tên `postgres_source_pool` với giới hạn cứng `5 Slots` và gắn `pool='postgres_source_pool'` cho toàn bộ các Task chạm vào DB nguồn; thiết lập `Data Contract` kiểm tra 5 thuộc tính ở thượng nguồn kết hợp mẫu thiết kế **Circuit Breaker (`Write-Audit-Publish`)** dùng `Great Expectations / Deequ` + `ShortCircuitOperator / BranchPythonOperator` để ngắt mạch ngay tại bảng Staging nếu vi phạm kỳ vọng (`amount > 0`, `user_id NOT NULL`), đẩy lô lỗi sang Quarantine và bắn cảnh báo kèm đồ thị phả hệ `DataHub (OpenLineage)`.",
                "Đặt thông số toàn cục `parallelism = 5` trong `airflow.cfg` để toàn bộ cụm Airflow chỉ được chạy tối đa 5 Task cho tất cả mọi việc (kể cả các Task chỉ chạy trên S3/Spark).",
                "Dùng lệnh `SELECT DISTINCT` và `ABS(amount)` ở bảng Gold để lặng lẽ biến số tiền âm thành số tiền dương mà không cần báo lỗi.",
                "Xóa bỏ hoàn toàn các bước kiểm tra chất lượng dữ liệu để đường ống chạy nhanh hơn."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Bảo vệ Kiến trúc Quản trị & Phả hệ): Hãy giải thích sâu 3 điểm: "
                "(1) Sự khác biệt giữa 3 tầng kiểm soát đồng thời trong Airflow (`parallelism`, `max_active_runs_per_dag`, và `Pool`) — tại sao `Pool` là công cụ chuẩn xác nhất để bảo vệ một hệ thống đích dùng chung bởi nhiều DAG khác nhau? "
                "(2) Tại sao dùng `ABS(amount)` hoặc `DISTINCT` để che giấu dữ liệu lỗi lại là một 'Band-Aid' nguy hiểm, và luồng **Circuit Breaker (Write-Audit-Publish)** vận hành như thế nào? "
                "(3) Khi một cột thượng nguồn buộc phải thay đổi, đồ thị phả hệ **DataHub (`OpenLineage` / `MCP` / `MCL`)** giúp đội kỹ sư đánh giá phạm vi ảnh hưởng (`Impact Analysis / Blast Radius`) ra sao trước khi merge code?"
            ),
            "rubric": {
                "coreConcepts": [
                    "Phân biệt đúng Phễu đồng thời 3 tầng của Airflow: `parallelism` giới hạn tổng số Task trên toàn cụm Airflow, `max_active_runs` giới hạn số lần chạy đồng thời của 1 DAG đơn lẻ, còn `Pool` là van tiết lưu xuyên suốt nhiều DAGs để bảo vệ một tài nguyên ngoại vi cụ thể (như `postgres_pool = 5 slots`, các Task thứ 6..100 xếp hàng `queued` an toàn trong khi các Task S3/Spark khác vẫn chạy hết công suất).",
                    "Giải thích đúng mẫu `Circuit Breaker / Write-Audit-Publish (WAP)`: ghi dữ liệu mới vào nhánh/bảng tạm (`Staging/Audit`), chạy bộ kiểm định `Great Expectations / PyDeequ` trên 6 chiều chất lượng (`Accuracy`, `Completeness`, `Uniqueness`, `Validity`, `Consistency`, `Timeliness`); nếu FAIL thì ngắt mạch ngay lập tức (không publish vào Gold), cô lập dữ liệu bẩn vào `Quarantine` để điều tra nguyên nhân gốc thay vì dùng `ABS()`/`DISTINCT` làm sai lệch số liệu tài chính.",
                    "Giải thích vai trò của `Data Contract` + `DataHub Lineage`: khóa hợp đồng 5 thuộc tính (`Schema, Nullability, Range, Freshness, Uniqueness`) ngay ở CI/CD của Producer, kết hợp `OpenLineage` phát sự kiện phả hệ cấp cột (`Column-level Lineage`) về `DataHub` qua Kafka `MCP/MCL`, giúp truy vết trong 0.2 giây chính xác bảng Gold, Dashboard và mô hình ML nào phụ thuộc vào cột `user_id`."
                ],
                "tradeoffs": [
                    "Phân biệt các mức độ nghiêm trọng của quy tắc kiểm định (Critical Gate vs Warning): lỗi làm hỏng tính đúng đắn cốt lõi (như âm tiền, mất khóa chính, gãy schema) phải kích hoạt `Hard Circuit Breaker` dừng luồng, trong khi các sai lệch thống kê nhỏ có thể phát cảnh báo mềm (`Soft Warning`) mà không chặn SLA toàn trình."
                ],
                "referenceAnswer": (
                    "1. Hạ `parallelism = 5` sẽ bóp nghẹt toàn bộ cụm Airflow (kể cả hàng trăm Task không chạm vào Postgres), còn `max_active_runs = 1` chỉ giới hạn trong phạm vi từng DAG riêng lẻ (15 DAGs vẫn mở 15 kết nối). Chỉ có `Resource Pool (postgres_source_pool = 5 slots)` mới tạo ra van tiết lưu dùng chung xuyên suốt cả 15 DAGs, giữ đúng tối đa 5 kết nối đồng thời tới PostgreSQL.\n"
                    "2. Dùng `ABS(amount)` hay `DISTINCT` là hành vi vá tạm bợ làm biến dạng báo cáo tài chính (biến giao dịch hoàn tiền/lỗi hệ thống thành doanh thu giả!). Chuẩn Production là áp dụng **Write-Audit-Publish (Circuit Breaker)**: nạp vào vùng Staging, chạy `Great Expectations / Deequ` kiểm định; nếu vi phạm ngưỡng thì ngắt nhánh Load vào Gold, đẩy bản ghi lỗi sang bảng `Quarantine` và bắn cảnh báo.\n"
                    "3. Kết hợp `Data Contract` chặn các thay đổi phá vỡ lược đồ (`Breaking Schema Changes`) ngay trên PR của Producer và dùng `DataHub` thu thập sự kiện `OpenLineage` (qua luồng Kafka `MCP/MCL`) để dựng đồ thị phả hệ cấp cột (`Column-level Lineage`), giúp xác định tức thì toàn bộ Blast Radius từ bảng nguồn tới tận BI Dashboard và Feature Store."
                )
            }
        }
    },

    # --------------------------------------------------------------------------
    # TRACK III & IV · AI SERVING, DISTRIBUTED SYSTEMS, K8S, CLOUD & OBSERVABILITY
    # --------------------------------------------------------------------------
    {
        "id": "A04-BP-01",
        "topic": "A04",
        "stage": 1,
        "stationId": "a04-llm-serving",
        "stationTitle": "A02–A04: RAG Architecture, KV Cache Mechanics, PagedAttention & Continuous Batching (vLLM)",
        "roleTracks": ["AIE", "MLE", "DE"],
        "skillName": "High-Performance LLM Serving (KV Cache, PagedAttention, Continuous Batching) & RAG Evaluation",
        "invariant": (
            "Quá trình suy luận LLM gồm 2 pha có đặc tính phần cứng đối lập: pha `Prefill` xử lý song song toàn bộ câu lệnh đầu vào nên bị giới hạn bởi năng lực tính toán (`Compute-bound`), "
            "còn pha `Decode` sinh từng token nối tiếp nhau nhưng ở mỗi bước phải đọc lại toàn bộ `KV Cache` từ bộ nhớ GPU HBM lên SRAM nên bị bóp nghẹt bởi băng thông bộ nhớ (`Memory-bandwidth bound`); "
            "`PagedAttention (vLLM)` chia KV Cache thành các trang không liền kề để triệt tiêu phân mảnh bộ nhớ (từ 60–80% xuống < 4%) và kết hợp `Continuous Batching` để tăng thông lượng gấp nhiều lần."
        ),
        "misconceptions": [
            "Tưởng rằng pha sinh từng từ (`Decode`) của LLM chậm là do GPU thiếu FLOPS tính toán nhân ma trận chứ không phải do nghẽn băng thông đọc bộ nhớ HBM.",
            "Cấp phát vùng nhớ `KV Cache` liền kề cố định bằng đúng `max_seq_len (32K tokens)` cho mọi câu hỏi ngắn 50 từ.",
            "Đánh giá chất lượng hệ thống RAG chỉ bằng cảm tính mắt thường mà không tách bạch `Context Recall/Precision` (tầng Retrieval) với `Faithfulness` (tầng Generation)."
        ],
        "L1": {
            "stem": (
                "Trong cơ chế phục vụ Mô hình Ngôn ngữ Lớn (`LLM Serving` như `vLLM` / `TensorRT-LLM`), "
                "tại sao pha **Prefill** (xử lý prompt đầu vào) và pha **Decode** (sinh từng token đầu ra) lại có điểm nghẽn phần cứng hoàn toàn khác nhau?"
            ),
            "options": [
                "Pha `Prefill` tính toán ma trận cho toàn bộ chuỗi token đầu vào cùng một lúc (Arithmetic Intensity cao) nên bị giới hạn bởi sức mạnh tính toán (`Compute-bound`); ngược lại pha `Decode` sinh tự hồi quy từng token một nhưng mỗi bước đều phải tải toàn bộ trọng số mô hình và `KV Cache` từ bộ nhớ GPU HBM vào SRAM nên bị giới hạn bởi băng thông bộ nhớ (`Memory-bandwidth bound`).",
                "Pha `Prefill` chỉ chạy trên CPU của máy chủ, còn pha `Decode` mới chạy trên GPU.",
                "Pha `Decode` không cần dùng đến `KV Cache` mà chỉ đọc từ ổ cứng SSD.",
                "Cả hai pha đều chỉ bị giới hạn bởi tốc độ đường truyền cáp quang Internet của người dùng."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo học phần `A04 · Dive into LLM Serving`: Trong pha `Decode`, để sinh ra đúng 1 token tiếp theo, GPU vẫn phải đọc toàn bộ hàng chục GB trọng số mô hình + toàn bộ `KV Cache` của các token trước đó từ HBM lên nhân tính toán, khiến tỷ lệ phép tính trên mỗi byte đọc (`Arithmetic Intensity`) cực thấp -> điểm nghẽn nằm ở băng thông bộ nhớ HBM."
            ),
            "distractorReasons": [
                "Chính xác: Prefill = Compute-bound (Matrix-Matrix multiplication) vs Decode = Memory-bandwidth bound (Matrix-Vector multiplication + KV Cache HBM read).",
                "Sai: Cả Prefill và Decode đều thực thi trên các nhân Tensor Cores / SMs của GPU.",
                "Sai: Pha Decode phụ thuộc sống còn vào việc đọc và nối thêm vector Key/Value mới vào `KV Cache` trên VRAM.",
                "Sai: Đây là cơ học phần cứng bên trong GPU (HBM <-> SRAM), độc lập với mạng Internet bên ngoài."
            ]
        },
        "L2": {
            "stem": (
                "Đội AI triển khai một mô hình LLM 14B trên GPU A100 80GB bằng cơ chế gom lô tĩnh truyền thống (`Static Batching`) và cấp phát `KV Cache` liền kề theo độ dài tối đa `max_tokens = 8192`. "
                "Khi có 16 người dùng gửi câu hỏi cùng lúc (15 người chỉ hỏi câu ngắn trả lời 100 tokens, nhưng 1 người yêu cầu viết báo cáo dài 4000 tokens), "
                "hệ thống vừa báo hết sạch VRAM (`CUDA Out of Memory`) khi mới phục vụ được vài chục câu, vừa bắt 15 người hỏi câu ngắn phải ngồi chờ cho đến khi người thứ 16 sinh xong token thứ 4000 mới trả kết quả! "
                "Bộ đôi kỹ thuật nào trong `vLLM` giải quyết triệt để cả 2 căn bệnh này?"
            ),
            "codeSnippet": (
                "# Static Batching + Contiguous KV Cache:\n"
                "Request 1..15: [Prompt 50 tok][Gen 100 tok][... Wasted Padding waiting for Req 16 ...]\n"
                "Request 16   : [Prompt 80 tok][................ Gen 4000 tok ................]"
            ),
            "options": [
                "`PagedAttention` (lấy cảm hứng từ Virtual Memory Paging của OS, chia `KV Cache` thành các khối `KV Blocks` cố định không cần nằm liền kề trên VRAM, cấp phát động theo nhu cầu thực tế giúp giảm lãng phí phân mảnh từ 70% xuống `< 4%`) kết hợp `Continuous Batching (Iteration-level Scheduling)` (giải phóng ngay các câu đã gặp `EOS token` ở từng vòng lặp để nhét ngay request mới vào lô mà không cần chờ câu dài nhất).",
                "Tăng tham số `temperature = 2.0` để mô hình sinh từ ngẫu nhiên nhanh hơn.",
                "Chuyển toàn bộ `KV Cache` xuống ổ cứng cơ học HDD để không bao giờ bị lỗi hết VRAM.",
                "Cấm người dùng gửi câu hỏi ngắn dưới 4000 tokens."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo `A03 & A04`: `PagedAttention` giải quyết triệt để phân mảnh nội và phân mảnh ngoại của `KV Cache` trên VRAM (giúp tăng số lượng request đồng thời trong một lô lên 3–5 lần), còn `Continuous Batching` lập lịch ở cấp độ từng bước sinh token (iteration-level) thay vì cấp độ cả lô (request-level)."
            ),
            "distractorReasons": [
                "Chính xác: PagedAttention trị phân mảnh VRAM của KV Cache + Continuous Batching trị hiện tượng Head-of-Line chờ câu dài nhất trong lô.",
                "Sai: `temperature` chỉ điều chỉnh phân phối xác suất chọn từ tiếp theo, không giải quyết phân mảnh bộ nhớ hay lập lịch lô.",
                "Sai: Đẩy KV Cache xuống HDD (độ trễ 4–10ms, băng thông 200 MB/s so với 2.000 GB/s của HBM) sẽ làm tốc độ sinh từ chậm đi hàng chục nghìn lần.",
                "Sai: Ép mọi câu trả lời đều dài 4000 tokens càng làm tốn GPU và tăng độ trễ vô ích."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Thiết kế Hệ thống Production RAG & LLM Serving: Bạn xây dựng hệ thống hỏi đáp tài liệu kỹ thuật nội bộ cho 5.000 kỹ sư. "
                "Hiện tại hệ thống gặp 2 vấn đề: "
                "(1) Khi người dùng hỏi các mã lỗi cụ thể (như `ERR_KAFKA_ISR_04` hoặc tên hàm `xcom_pull`), tìm kiếm Vector thuần túy (`Dense Embedding`) thường tìm trượt sang các đoạn văn chung chung làm LLM bịa câu trả lời (`Hallucination`); "
                "(2) Chi phí GPU tăng vọt và độ trễ `Time-To-First-Token (TTFT)` + `Inter-Token Latency (ITL)` vượt ngưỡng SLA khi giờ cao điểm."
            ),
            "mcqPrompt": "Phần A (Kiến trúc Truy hồi & Đánh giá): Kiến trúc truy hồi nào khắc phục điểm mù của Dense Vector đối với các mã định danh/thuật ngữ chính xác?",
            "options": [
                "Áp dụng **Hybrid Search** kết hợp tìm kiếm từ khóa thưa (`Sparse BM25 / SPLADE`) với tìm kiếm ngữ nghĩa đặc (`Dense Vector ANN`), hợp nhất kết quả qua `Reciprocal Rank Fusion (RRF)` rồi lọc tinh bằng mô hình `Cross-Encoder Reranker` trước khi đưa vào Prompt, đồng thời đo lường định lượng 4 chỉ số `RAGAS` (`Context Precision`, `Context Recall`, `Faithfulness`, `Answer Relevance`).",
                "Tăng kích thước mỗi mảnh văn bản (`chunk_size`) lên thành `50.000 từ` để nhét nguyên cả cuốn sách vào 1 vector duy nhất.",
                "Xóa bỏ hoàn toàn cơ sở dữ liệu Vector và bắt LLM tự nhớ toàn bộ mã lỗi nội bộ không cần ngữ cảnh.",
                "Giảm số chiều của vector embedding xuống còn 2 chiều (`2D`) để tìm kiếm chính xác hơn."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Tối ưu hóa Tầng Phục vụ LLM): Hãy giải thích cách kết hợp 3 kỹ thuật ở tầng Serving (`A04`): "
                "`Prefix Caching (Automatic Prefix Sharing)`, `Speculative Decoding`, và `Quantization (AWQ / FP8)` để giảm mạnh cả `TTFT` lẫn `ITL` mà vẫn giữ chất lượng câu trả lời?"
            ),
            "rubric": {
                "coreConcepts": [
                    "Giải thích đúng `Prefix Caching`: trong hệ thống RAG/Agent, phần `System Prompt` dài và các tài liệu dùng chung lặp đi lặp lại giữa các truy vấn — nhờ `PagedAttention`, các khối `KV Cache` của phần tiền tố chung được băm và dùng chung trên VRAM, giúp bỏ qua bước tính lại Prefill và giảm mạnh `TTFT (Time-To-First-Token)`.",
                    "Giải thích đúng `Speculative Decoding`: dùng một mô hình nháp siêu nhỏ (`Draft Model`) đoán nhanh `K` tokens tiếp theo rồi đưa cả `K` tokens đó vào mô hình lớn (`Target Model`) kiểm chứng song song trong đúng 1 lượt đọc trọng số từ HBM, giúp tăng tốc pha `Decode` (`ITL`) gấp 2–3 lần mà phân phối đầu ra toán học giống hệt 100% mô hình gốc.",
                    "Giải thích đúng tác dụng của `Quantization (FP8 / INT4 AWQ)` trong pha Decode: vì Decode bị nghẽn ở băng thông bộ nhớ (`Memory-bandwidth bound`), giảm kích thước trọng số từ 16-bit xuống 8-bit/4-bit giúp giảm một nửa đến 3/4 lượng byte phải đọc từ HBM lên SRAM ở mỗi token, tăng trực tiếp tốc độ sinh từ và dung lượng trống cho KV Cache."
                ],
                "tradeoffs": [
                    "Nêu rõ khi nào `Speculative Decoding` kém hiệu quả: khi `Acceptance Rate` của mô hình nháp thấp hoặc khi hệ thống đang ở mức tải lô cực lớn khiến GPU đã bão hòa tính toán (`Compute-bound`)."
                ],
                "referenceAnswer": (
                    "1. **Giảm TTFT bằng Automatic Prefix Caching**: Nhờ cấu trúc trang của `PagedAttention`, các khối `KV Cache` của System Prompt và tài liệu ngữ cảnh được chia sẻ trực tiếp giữa các request thông qua bảng băm khối, giúp tránh tính toán lại pha Prefill.\n"
                    "2. **Giảm ITL (tăng tốc sinh từ) bằng Quantization (FP8 / AWQ INT4) + Speculative Decoding**: Vì pha Decode bị bóp nghẹt bởi băng thông đọc trọng số từ HBM, nén trọng số xuống FP8/INT4 cắt giảm 50–75% lưu lượng byte đi qua bus HBM; kết hợp `Speculative Decoding` dùng mô hình nhỏ đề xuất chuỗi token và mô hình lớn xác thực song song trong 1 bước đọc bộ nhớ duy nhất, giúp tăng tốc độ sinh từ gấp 2–3 lần mà không làm giảm chất lượng."
                )
            }
        }
    },

    {
        "id": "P01-BP-01",
        "topic": "P01",
        "stage": 1,
        "stationId": "p01-distributed-cap",
        "stationTitle": "P01–P08: Distributed Systems (CAP/PACELC/Raft), Kubernetes, Cloud FinOps & Observability",
        "roleTracks": ["DE", "AIE", "MLE"],
        "skillName": "Distributed Consensus (CAP/PACELC, Raft/Paxos), API Gateway Resilience & 3 Pillars of Observability",
        "invariant": (
            "Trong hệ thống phân tán qua mạng thực tế, đứt mạng cục bộ (`Network Partition - P`) là điều tất yếu xảy ra, buộc kiến trúc sư phải chọn giữa `Consistency (C — từ chối yêu cầu hoặc chờ đồng bộ để không trả dữ liệu cũ/mâu thuẫn)` và `Availability (A — vẫn phản hồi từ nhánh bị cô lập nhưng chấp nhận dữ liệu tạm thời lệch nhau)`; "
            "định lý `PACELC` mở rộng thêm: ngay cả khi mạng bình thường (`Else - E`), hệ thống vẫn phải đánh đổi giữa `Latency (L)` và `Consistency (C)`."
        ),
        "misconceptions": [
            "Tuyên bố thiết kế được một cơ sở dữ liệu phân tán đa vùng đạt đồng thời cả 3 tính chất `CA` ngay trong lúc cáp quang giữa hai trung tâm dữ liệu bị đứt đôi.",
            "Cấu hình `Retry` tức thì vô hạn lần (`Immediate Infinite Retry`) không có `Exponential Backoff + Jitter` và không có `Circuit Breaker` khi dịch vụ hạ nguồn đang quá tải.",
            "Tưởng rằng chỉ cần thu thập `Logs` văn bản là đủ để truy vết độ trễ của một request đi qua 15 microservices mà không cần `Distributed Tracing (OpenTelemetry TraceId/SpanId)`."
        ],
        "L1": {
            "stem": (
                "Theo định lý **CAP** và phần mở rộng **PACELC** trong Hệ phân tán (`P01`), tại sao một cụm cơ sở dữ liệu dùng thuật toán đồng thuận **Raft** gồm `5 Nodes` đặt tại 3 trung tâm dữ liệu lại yêu cầu tối thiểu `Quorum = 3 Nodes` (`⌊N/2⌋ + 1`) đồng ý trước khi xác nhận một giao dịch ghi?"
            ),
            "options": [
                "Nguyên lý Đa số Giao nhau (`Quorum Intersection`): bất kỳ hai nhóm đa số nào gồm 3 trên 5 Nodes cũng luôn có ít nhất `1 Node chung` giữ bản ghi mới nhất; nếu xảy ra đứt mạng tách cụm thành 2 nhánh `(3 Nodes)` và `(2 Nodes)`, chỉ nhánh 3 Nodes mới bầu được Leader và được phép ghi (`CP`), ngăn chặn tuyệt đối thảm họa **Split-Brain** (hai nhánh cùng tự nhận là Leader và ghi dữ liệu mâu thuẫn nhau).",
                "Vì thuật toán Raft chỉ hoạt động được trên các máy chủ có số nhân CPU là số lẻ.",
                "Vì nếu cả 5 Nodes cùng hoạt động thì Raft sẽ tự động tắt bớt 2 Nodes để tiết kiệm tiền điện.",
                "Để đảm bảo khi 4 trên 5 Nodes bị cháy ổ cứng cùng lúc thì 1 Node còn lại vẫn tự phong làm Leader và ghi tiếp bình thường."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo học phần `P01 · Distributed Systems`: Thuật toán đồng thuận `Raft` / `Paxos` dựa trên bất biến `Quorum (⌊N/2⌋ + 1)`. "
                "Với `N = 5`, Quorum là `3`. Nhánh thiểu số (`2 Nodes`) bị đứt mạng sẽ không đủ phiếu bầu nên tự động ngừng nhận lệnh ghi, hy sinh `Availability` ở nhánh thiểu số để bảo vệ tuyệt đối `Consistency` (chống Split-Brain)."
            ),
            "distractorReasons": [
                "Chính xác: Quorum Intersection (`⌊N/2⌋ + 1`) ngăn chặn Split-Brain và đảm bảo Leader mới luôn chứa toàn bộ giao dịch đã commit.",
                "Sai: Số lượng Node lẻ (3, 5, 7) là số lượng máy chủ thành viên trong cụm đồng thuận, không liên quan đến số nhân CPU.",
                "Sai: Cả 5 Nodes đều hoạt động (1 Leader + 4 Followers nhận bản sao nhật ký `AppendEntries`).",
                "Sai: Với `N = 5`, cụm chịu được tối đa `2 Nodes` sập (`5 - 2 = 3 >= Quorum`); nếu 4 Nodes sập thì 1 Node còn lại không đủ Quorum và phải ngừng nhận ghi."
            ]
        },
        "L2": {
            "stem": (
                "Dịch vụ `Checkout-Gateway` gọi sang `Inventory-Service`. Bình thường `Inventory-Service` chịu được `2.000 RPS`. "
                "Khi `Inventory-Service` bị chậm tạm thời (GC pause 3 giây) làm 10% request bị timeout, lập trình viên ở `Checkout-Gateway` đã cấu hình cơ chế thử lại: "
                "`max_retries = 5, retry_delay = 0ms` (thử lại ngay lập tức 5 lần liên tiếp cho mỗi request lỗi). "
                "Chỉ sau 10 giây, `Inventory-Service` sập chết hoàn toàn và không thể gượng dậy nổi ngay cả khi lưu lượng người dùng thật đã giảm xuống! "
                "Hiện tượng này gọi là gì và bộ ba cơ chế phòng thủ nào tại `P05 · Routing & Gateway` chặn đứng nó?"
            ),
            "codeSnippet": (
                "# Cấu hình Retry tự sát (Retry Storm / Cascading Failure):\n"
                "for attempt in range(6):  # 1 gốc + 5 retries tức thì\n"
                "    resp = call_inventory_service()\n"
                "    if resp.status == 200: break"
            ),
            "options": [
                "Đây là hiện tượng **Bão Thử Lại (`Retry Storm / Self-Inflicted DDoS`)** khuếch đại lưu lượng lên gấp 6 lần (`12.000 RPS`) đè chết dịch vụ đang hấp hối. Phải kết hợp bộ ba: (1) **Exponential Backoff + Random Jitter** (giãn cách thời gian chờ lũy thừa kèm nhiễu ngẫu nhiên để phá đồng bộ sóng retry), (2) **Retry Budget** (giới hạn tổng tỷ lệ retry toàn cục dưới 10% lưu lượng), và (3) **Circuit Breaker** (ngắt mạch trả về Fallback ngay khi tỷ lệ lỗi vượt ngưỡng để cho dịch vụ hạ nguồn có thời gian hồi phục).",
                "Do số lần `max_retries = 5` còn quá ít; phải tăng lên `max_retries = 100` để đảm bảo 100% request đều thành công.",
                "Chỉ cần tắt hoàn toàn cơ chế `Timeout` (đặt `timeout = None` chờ vô hạn) trên `Checkout-Gateway` là hệ thống sẽ không bao giờ bị sập.",
                "Do giao thức HTTP không cho phép gửi lại cùng một request quá 2 lần."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo `P05 · Routing & Gateway`: Thử lại tức thì (`retry_delay = 0`) mà không có `Jitter` khiến hàng nghìn client đồng loạt nã pháo vào đúng một mili-giây (`Thundering Herd`). "
                "Chuẩn kiến trúc Resilience bắt buộc có: `Timeout hợp lý` + `Exponential Backoff with Jitter` + `Retry Budget` + `Circuit Breaker (Closed -> Open -> Half-Open)`."
            ),
            "distractorReasons": [
                "Chính xác: Giải phẫu đúng cơ chế Retry Storm và bộ tam phòng thủ (Backoff+Jitter, Retry Budget, Circuit Breaker).",
                "Sai: Tăng lên 100 lần retry sẽ nhân tải lên gấp 100 lần, biến hệ thống thành vũ khí DDoS tự bắn mình.",
                "Sai: Đặt `timeout = None` sẽ làm toàn bộ luồng/kết nối của `Checkout-Gateway` bị treo cứng vĩnh viễn (`Thread/Connection Pool Exhaustion`), kéo sập cả Gateway!",
                "Sai: HTTP hoàn toàn cho phép gửi lại request (đặc biệt khi kèm `Idempotency-Key`)."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Thiết kế Hệ thống Quan sát Toàn diện (`P08 · Observable Systems` & `P09 · SRE`): "
                "Hệ thống AI & Data Platform của bạn chạy trên Kubernetes gồm 12 dịch vụ (`API Gateway -> Auth -> RAG Orchestrator -> Vector DB + vLLM Server -> PostgreSQL + Kafka`). "
                "Khách hàng phàn nàn rằng khoảng 2% yêu cầu hỏi đáp bị chậm trên `8 giây`, nhưng bảng điều khiển CPU/RAM trung bình của các máy chủ đều chỉ ở mức `40%` và không có container nào bị sập."
            ),
            "mcqPrompt": "Phần A (Ba Trụ Cột Quan Sát & Chỉ Số SRE): Tại sao nhìn vào `Average Latency (Độ trễ trung bình)` và `% CPU trung bình` lại hoàn toàn vô dụng để bắt lỗi 2% yêu cầu chậm này, và công cụ nào giúp chỉ điểm chính xác đoạn nghẽn?",
            "options": [
                "Độ trễ trung bình (`Average`) che lấp hoàn toàn các điểm dị biệt ở đuôi phân phối; bắt buộc phải đo theo phân vị đuôi (**Tail Latency Histogram: `p95`, `p99`, `p99.9`**) trong **Metrics (Prometheus)** và gắn mã **`trace_id` / `span_id` xuyên suốt qua chuẩn OpenTelemetry (Distributed Tracing — Jaeger/Langfuse)** để dựng biểu đồ thác nước (`Waterfall Flamegraph`) xem chính xác 8 giây đó bị ngâm ở Span nào (do chờ khóa DB, do Reranker hay do vLLM Queue).",
                "Chỉ cần dùng lệnh `grep ERROR` trên tệp log văn bản của dịch vụ đầu tiên là biết được độ trễ của 11 dịch vụ phía sau.",
                "Độ trễ trung bình (`Average`) luôn lớn hơn hoặc bằng độ trễ phân vị thứ 99 (`p99`).",
                "Chỉ cần xóa bớt 2% tài khoản người dùng đang bị chậm là hệ thống đạt chuẩn SLA 100%."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Kiến trúc Observability, Drift & Error Budget): Hãy trình bày: "
                "(1) Cách liên kết chặt chẽ **3 Trụ cột Quan sát (`Metrics`, `Logs`, `Traces`)** qua `trace_id` để từ một đỉnh nhọn `p99` trên Grafana nhảy thẳng tới đúng dòng Log và Span gây nghẽn? "
                "(2) Sự khác biệt giữa `SLI`, `SLO`, `SLA` và cách vận hành **Ngân sách Lỗi (`Error Budget`)** trong SRE để quyết định khi nào ưu tiên ra tính năng mới vs khi nào dừng lại sửa độ tin cậy?"
            ),
            "rubric": {
                "coreConcepts": [
                    "Giải thích đúng sự kết nối của 3 trụ cột (`Metrics + Traces + Logs`): `Metrics` (Prometheus Histogram) phát hiện *triệu chứng* (`p99 latency > 8s`), thông qua `Exemplars` hoặc `trace_id` nhảy sang `Distributed Trace` (OpenTelemetry/Jaeger/Langfuse) để định vị *ở đâu* trong chuỗi 12 dịch vụ bị chậm (`Span` nào chiếm 7.5s), và dùng cùng `trace_id` đó lọc `Structured JSON Logs` tại đúng dịch vụ đó để biết *tại sao* lỗi.",
                    "Phân biệt chuẩn xác bộ tứ SRE: `SLI (Service Level Indicator)` là con số đo thực tế (VD: tỷ lệ request thành công có độ trễ < 1.5s), `SLO (Service Level Objective)` là mục tiêu cam kết nội bộ (VD: `99.9%` trong 30 ngày), `SLA (Service Level Agreement)` là hợp đồng pháp lý có phạt tiền với khách hàng (thường nới lỏng hơn SLO, VD `99.5%`), và `Error Budget = 100% - SLO` (`0.1%` tương đương ~43 phút/tháng).",
                    "Cơ chế điều hành bằng `Error Budget`: chừng nào ngân sách lỗi còn dư thì đội được phép đẩy nhanh tốc độ phát hành tính năng/thử nghiệm mô hình mới; ngay khi cháy hết Error Budget (do sự cố hoặc chậm SLA) thì tự động đóng băng phát hành tính năng mới để dồn 100% nguồn lực trả nợ kỹ thuật và gia cố độ tin cậy."
                ],
                "tradeoffs": [
                    "Nêu rõ đánh đổi về chi phí lưu trữ khi thu thập `Traces` ở quy mô lớn: sử dụng `Tail-based Sampling` (giữ lại 100% các trace bị lỗi hoặc có độ trễ vượt ngưỡng `p99`, và chỉ lấy mẫu 1–5% các trace thành công bình thường) để vừa bắt trọn 100% sự cố vừa tiết kiệm 90% chi phí lưu trữ."
                ],
                "referenceAnswer": (
                    "1. Để liên kết 3 trụ cột, tại cổng Gateway ta khởi tạo `W3C traceparent (trace_id, span_id)` bằng `OpenTelemetry`, truyền qua header của mọi lời gọi HTTP/gRPC/Kafka và tự động đính kèm `trace_id` vào mọi dòng `Structured JSON Log` cũng như `Prometheus Histogram Exemplars`. Khi biểu đồ `p99` trên Grafana báo động, kỹ sư bấm vào điểm Exemplar để mở thẳng biểu đồ thác nước `Jaeger/Langfuse` xem Span nào chiếm 7.8s/8s và xem toàn bộ Log của đúng `trace_id` đó.\n"
                    "2. `SLI` là chỉ số đo lường thực tế, `SLO` là ngưỡng mục tiêu kỹ thuật nội bộ (VD `99.9%`), còn `SLA` là cam kết thương mại với khách hàng. Khoảng cách `100% - SLO = 0.1%` chính là **Error Budget (Ngân sách Lỗi)**: biến tranh cãi cảm tính giữa đội Product (muốn ship nhanh) và đội SRE (muốn ổn định) thành quy tắc định lượng — còn Error Budget thì ship tính năng, cạn Error Budget thì ưu tiên tuyệt đối cho Reliability."
                )
            }
        }
    },

    # --------------------------------------------------------------------------
    # TRACK V & VI · CLASSICAL ML, CAUSAL, DEEP LEARNING, RLHF/DPO & GPU TRITON
    # (Tích hợp chuẩn hóa từ 00-quizzes-dsai-1.pdf & 00-quizzes-dsai-2.pdf)
    # --------------------------------------------------------------------------
    {
        "id": "S04-BP-01",
        "topic": "S04",
        "stage": 1,
        "stationId": "s04-ml-fundamentals",
        "stationTitle": "S02–S11 (DSAI-1 Quiz & Labs): Math, Regularization (L1/L2), Tree Ensembles (XGBoost/LightGBM) & Causal",
        "roleTracks": ["MLE", "AIE", "DE"],
        "skillName": "Bias-Variance Trade-off, L1/L2 Regularization, Gradient Boosted Trees (XGBoost/LightGBM) & Evaluation Metrics",
        "invariant": (
            "Regularization `L1 (Lasso: λ∑|w_i|)` có đạo hàm hằng số `±λ` đẩy các trọng số yếu về đúng bằng `0` (tạo nghiệm thưa `Sparse Solution` giúp chọn lọc đặc trưng tự động), "
            "còn `L2 (Ridge: λ∑w_i^2)` có đạo hàm `2λw_i` giảm dần khi tiến gần 0 nên ép các trọng số nhỏ lại đồng đều và xử lý tốt đa cộng tuyến (`Multicollinearity`); "
            "trong dữ liệu mất cân bằng nghiêm trọng (như 99.9% giao dịch bình thường, 0.1% gian lận), độ đo `Accuracy` hoàn toàn vô nghĩa — phải dùng `Precision, Recall, F1-Score, PR-AUC` và ma trận chi phí kinh doanh."
        ),
        "misconceptions": [
            "Đánh giá mô hình phát hiện gian lận trên tập dữ liệu có tỷ lệ `0.1% Fraud` bằng chỉ số `Accuracy = 99.9%` (trong khi mô hình chỉ đoán toàn bộ là `Không gian lận`!).",
            "Áp dụng `StandardScaler.fit_transform(X)` trên toàn bộ tập dữ liệu trước khi gọi `train_test_split` hoặc bên ngoài vòng lặp `K-Fold Cross-Validation`.",
            "Tưởng rằng `Random Forest` (Bagging các cây độc lập song song để giảm phương sai `Variance`) giống hệt cơ chế của `XGBoost / LightGBM` (Boosting các cây nối tiếp dựa trên đạo hàm bậc 1 & bậc 2 của hàm mất mát để giảm độ chệch `Bias`)."
        ],
        "L1": {
            "stem": (
                "Dựa trên nền tảng Toán Tối ưu hóa và Học máy (`S02, S04, S05 — DSAI-1 Quiz`), "
                "sự khác biệt hình học và giải tích cốt lõi nào khiến điều chuẩn **L1 (Lasso Regularization)** có khả năng triệt tiêu các trọng số dư thừa về đúng bằng `0` (`Feature Selection`), "
                "trong khi **L2 (Ridge Regularization)** chỉ co nhỏ các trọng số về sát `0`?"
            ),
            "options": [
                "Miền ràng buộc của `L1 (∑|w_i| <= C)` là một hình thoi đa diện sắc nhọn có các đỉnh nằm ngay trên các trục tọa độ (đạo hàm subgradient giữ lực kéo hằng số `±λ` ngay cả khi `w_i` rất nhỏ), nên các đường đồng mức của hàm mất mát rất dễ tiếp xúc ngay tại đỉnh trên trục (`w_j = 0`); ngược lại miền ràng buộc của `L2 (∑w_i^2 <= C)` là mặt cầu trơn có lực kéo `2λw_i` yếu dần về 0 khi `w_i -> 0`.",
                "Vì `L1 Regularization` nhân toàn bộ các cột đặc trưng với số `0` trước khi bắt đầu huấn luyện.",
                "Vì `L2 Regularization` làm tăng phương sai (`Variance`) của mô hình lên vô cùng.",
                "Hai phương pháp `L1` và `L2` cho ra bộ trọng số giống hệt nhau 100% trên mọi tập dữ liệu."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo `S04 & S05`: Xét theo cập nhật Gradient Descent, thành phần phạt của `L2` là `-2ηλw_i` (chỉ co trọng số theo tỷ lệ `(1 - 2ηλ)` tiệm cận 0), "
                "còn `L1` trừ đi một lượng hằng số `-ηλ·sign(w_i)` đẩy thẳng các trọng số có đóng góp gradient nhỏ hơn `λ` chạm đích `0`."
            ),
            "distractorReasons": [
                "Chính xác: Giải thích đúng cả góc nhìn Hình học (Hình thoi có đỉnh trên trục tọa độ vs Hình cầu trơn) lẫn Giải tích (Đạo hàm hằng số `±λ` vs Đạo hàm tuyến tính `2λw`).",
                "Sai: L1 chỉ đưa những trọng số của đặc trưng ít thông tin về 0 trong quá trình tối ưu hóa, không xóa mù quáng mọi cột từ đầu.",
                "Sai: Cả L1 và L2 đều là kỹ thuật Regularization giúp GIẢM phương sai (`Variance`) để chống Overfitting.",
                "Sai: L1 tạo nghiệm thưa (`Sparse weights`), còn L2 tạo nghiệm phân bố đều (`Dense small weights`)."
            ]
        },
        "L2": {
            "stem": (
                "Trong bài toán Dự báo Khách hàng Rời bỏ (`Customer Churn` — Lab `S04/S09`), một kỹ sư viết đoạn mã tiền xử lý và đánh giá chéo `5-Fold Cross Validation` như bên dưới. "
                "Điểm trung bình `CV ROC-AUC` đạt tới `0.94`, nhưng khi kiểm thử trên tập dữ liệu tháng kế tiếp (`Out-of-Time Validation`) thì `ROC-AUC` rơi tự do xuống `0.62`. "
                "Hãy chỉ ra **2 lỗi rò rỉ dữ liệu (`Data Leakage`)** ngay trong 5 dòng code này!"
            ),
            "codeSnippet": (
                "scaler = StandardScaler()\n"
                "X_scaled = scaler.fit_transform(df.drop(columns=['churn']))\n"
                "imputer = SimpleImputer(strategy='mean')\n"
                "X_clean = imputer.fit_transform(X_scaled)\n"
                "scores = cross_val_score(XGBClassifier(), X_clean, df['churn'], cv=5, scoring='roc_auc')"
            ),
            "options": [
                "Lỗi 1 (`Preprocessing Leakage`): Gọi `fit_transform()` của `StandardScaler` và `SimpleImputer` trên TOÀN BỘ bảng `df` trước khi chia `cv=5`, khiến trung bình/độ lệch chuẩn của các Fold kiểm định (`Validation Folds`) bị lộ vào quá trình biến đổi của các Fold huấn luyện; Lỗi 2 (`Temporal Leakage`): Dùng `K-Fold` trộn ngẫu nhiên dữ liệu có tính chu kỳ thời gian khiến mô hình dùng dữ liệu của tháng sau để đoán tháng trước. Phải đóng gói vào `sklearn.pipeline.Pipeline` và chia tách theo thời gian (`TimeSeriesSplit` / Out-of-Time split).",
                "Do `XGBClassifier` bắt buộc mọi đặc trưng đầu vào phải được chuẩn hóa bằng `StandardScaler` thì mới tách nhánh cây quyết định được.",
                "Do tham số `cv=5` quá nhỏ, phải tăng lên `cv=500` thì mới hết rò rỉ dữ liệu.",
                "Do hàm `SimpleImputer` tự động xóa cột `churn` khỏi bộ nhớ máy tính."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo `S04 & S06 (Feature Engineering & ML Pipelines)`: Mọi bước có chữ `.fit()` (tính mean/std, imputer, target encoding, PCA, feature selection) "
                "bắt buộc phải nằm BÊN TRONG `Pipeline` để chỉ `.fit()` trên tập `Train` của từng Fold rồi dùng tham số đó `.transform()` tập `Validation`. "
                "Lưu ý thêm: Các mô hình dựa trên cây (`Decision Tree`, `Random Forest`, `XGBoost`, `LightGBM`) bất biến với phép biến đổi đơn điệu nên vốn không cần `StandardScaler`!"
            ),
            "distractorReasons": [
                "Chính xác: Bắt trúng cả Preprocessing Leakage (fit trên toàn tập trước CV) lẫn Temporal Leakage, kèm giải pháp `Pipeline` + `TimeSeriesSplit`.",
                "Sai: Các thuật toán cây quyết định tách nhánh theo ngưỡng thứ tự (`x_j <= threshold`), hoàn toàn bất biến với phép co giãn tuyến tính như `StandardScaler`.",
                "Sai: Nếu đã gọi `fit_transform` trên toàn bộ tập dữ liệu trước khi đưa vào `cross_val_score` thì tăng `cv` lên bao nhiêu vẫn bị rò rỉ dữ liệu.",
                "Sai: `SimpleImputer` chỉ điền giá trị khuyết trên ma trận `X_scaled`."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Phỏng vấn Thiết kế Hệ thống ML & Giải phẫu Thuật toán (`S08, S09, S02`): "
                "Bạn thiết kế mô hình Chấm điểm Tín dụng & Dự báo Rời bỏ (`Credit Risk & Churn`) trên tập dữ liệu dạng bảng (`Tabular Data`) có `50 triệu dòng`, `200 cột` (nhiều cột phân loại có số lượng giá trị lớn và nhiều giá trị khuyết `NaN`)."
            ),
            "mcqPrompt": "Phần A (Giải phẫu XGBoost vs LightGBM): Tại sao `XGBoost` và `LightGBM` lại vượt trội hơn `Gradient Boosting (GBM)` cổ điển về cả độ chính xác lẫn tốc độ huấn luyện trên 50 triệu dòng?",
            "options": [
                "`XGBoost` khai triển hàm mất mát đến **đạo hàm bậc 2 (`Second-order Taylor Expansion`: cả Gradient $g_i$ và Hessian $h_i$)** kèm thành phần phạt độ phức tạp của cây (`$\\gamma T + \\frac{1}{2}\\lambda \\sum w_j^2$`) và tự học hướng rẽ nhánh mặc định cho giá trị `NaN` (`Sparsity-aware Split Finding`); còn `LightGBM` tăng tốc độ lên gấp nhiều lần nhờ **Histogram-based binning**, lấy mẫu theo độ lớn đạo hàm (**GOSS — Gradient-based One-Side Sampling**), gộp các đặc trưng loại trừ lẫn nhau (**EFB — Exclusive Feature Bundling**) và mọc cây theo nhánh có mức giảm lỗi lớn nhất (**Leaf-wise growth**).",
                "Vì `XGBoost` và `LightGBM` không dùng cây quyết định mà dùng mạng nơ-ron tích chập 3D.",
                "Vì `LightGBM` xóa bỏ ngẫu nhiên 99% số cột của bảng dữ liệu trước khi huấn luyện.",
                "Vì `XGBoost` chỉ dùng đạo hàm bậc 0 (không cần tính đạo hàm)."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Từ Dự báo đến Suy luận Nhân quả & Tác động Kinh doanh — `S03 Causal Reasoning`): "
                "Giả sử mô hình dự báo chính xác khách hàng `A` có xác suất rời bỏ cao (`P(Churn) = 85%`). "
                "Tại sao việc cứ thấy ai có `P(Churn)` cao là tặng ngay mã giảm giá 200.000 VNĐ lại có thể gây lỗ nặng cho công ty, và bạn dùng tư duy **Causal Inference / Uplift Modeling** + **SHAP** như thế nào để tối ưu hóa lợi nhuận ròng?"
            ),
            "rubric": {
                "coreConcepts": [
                    "Phân biệt sắc sảo giữa **Dự báo Tương quan (`Predictive Modeling: P(Y | X)`)** và **Suy luận Nhân quả / Tác động Can thiệp (`Causal Inference / Uplift: P(Y | do(T=1), X) - P(Y | do(T=0), X)`)**: khách hàng có `P(Churn)` cao có thể thuộc nhóm `Lost Causes` (chắc chắn bỏ đi dù có tặng quà -> mất trắng 200k) hoặc nhóm `Sleeping Dogs` (đang quên hủy gói, nhận tin nhắn khuyến mãi lại nhớ ra bấm hủy luôn!). Chỉ nên tác động vào nhóm **Persuadables** (chỉ ở lại khi có can thiệp).",
                    "Giải thích cách dùng `SHAP (SHapley Additive exPlanations)` để giải thích đóng góp cục bộ của từng đặc trưng cho từng khách hàng (ví dụ khách hàng A muốn rời bỏ vì bị lỗi kỹ thuật 3 lần trong tuần chứ không phải vì giá đắt -> cần CSKH gọi hỗ trợ kỹ thuật thay vì phát voucher giảm giá).",
                    "Thiết kế hàm mục tiêu theo **Giá trị Kỳ vọng Kinh doanh (`Expected Profit Matrix`)**: so sánh chi phí can thiệp (`Cost of Incentive`) với giá trị vòng đời khách hàng giữ lại được (`LTV × Uplift`) và kiểm chứng bằng `A/B Testing (Randomized Controlled Trial)`."
                ],
                "tradeoffs": [
                    "Nêu rõ rủi ro Overfitting của chiến lược mọc cây `Leaf-wise` trong LightGBM trên tập dữ liệu nhỏ: bắt buộc phải kiểm soát chặt `num_leaves < 2^{max_depth}` và `min_child_samples`."
                ],
                "referenceAnswer": (
                    "1. Mô hình dự báo `P(Churn)` chỉ trả lời *ai có nguy cơ rời đi*, không trả lời *việc tặng voucher 200k có làm thay đổi quyết định của họ hay không (`Causal Effect / Uplift`)*. Tặng tiền cho nhóm `Lost Causes` (đã quyết định rời đi) hoặc `Sure Things` (vẫn ở lại dù không có quà) làm lãng phí ngân sách.\n"
                    "2. Giải pháp: Kết hợp **SHAP Values** để chẩn đoán nguyên nhân gốc của từng cá nhân (nếu SHAP chỉ ra nguyên nhân là `support_tickets_count` cao thì điều phối đội kỹ thuật xử lý sự cố; nếu do `price_sensitivity` thì mới xét ưu đãi) và xây dựng mô hình **Uplift (`ITE = P(Retention | Treatment=1) - P(Retention | Treatment=0)`)** dựa trên dữ liệu thử nghiệm đối chứng ngẫu nhiên (`A/B Test`) để chỉ trao ưu đãi khi `Uplift × LTV > 200.000 VNĐ`."
                )
            }
        }
    },

    {
        "id": "S21-BP-01",
        "topic": "S21",
        "stage": 1,
        "stationId": "s21-triton-gpu",
        "stationTitle": "S17–S21 (DSAI-2 Quiz & Labs): Transformers, RLHF vs. DPO, GPU Architecture & OpenAI Triton Kernels",
        "roleTracks": ["MLE", "AIE", "DE"],
        "skillName": "Transformer Attention, Alignment (RLHF vs. DPO), GPU Memory Hierarchy (HBM/SRAM) & Triton Kernel Fusion",
        "invariant": (
            "Trên GPU hiện đại (như NVIDIA A100/H100), tốc độ tính toán của Tensor Cores lớn hơn rất nhiều so với băng thông đọc/ghi bộ nhớ ngoài `HBM (DRAM)`; "
            "khi chạy chuỗi các phép toán rời rạc trong PyTorch chuẩn (như `Softmax`, `LayerNorm`, `GELU`), mỗi phép toán đều phải đọc tensor từ `HBM` lên `SRAM (Shared Memory/Registers)` rồi lại ghi kết quả trung gian xuống `HBM`, gây nghẽn cổ chai băng thông (`Memory-bound trên Roofline Model`); "
            "viết nhân gộp (**Fused Kernel** bằng **OpenAI Triton / CUDA**) giữ toàn bộ bước trung gian nằm gọn trong `On-chip SRAM` siêu tốc, chỉ đọc `HBM` 1 lần và ghi `HBM` 1 lần."
        ),
        "misconceptions": [
            "Tưởng rằng phép tính `Scaled Dot-Product Attention` tiêu chuẩn mất nhiều thời gian nhất ở phép nhân ma trận `Q @ K^T`, trong khi thực tế điểm nghẽn chí mạng ở chuỗi dài là việc đọc/ghi ma trận trung gian `N × N` xuống bộ nhớ `HBM`.",
            "Trong lập trình `OpenAI Triton`, quên gắn mặt nạ biên (`mask = offsets < n_elements`) khi gọi `tl.load` / `tl.store` dẫn đến đọc/ghi tràn vùng nhớ khi kích thước mảng không chia hết cho `BLOCK_SIZE`.",
            "Tưởng rằng `DPO (Direct Preference Optimization)` vẫn phải huấn luyện một mô hình phần thưởng (`Reward Model`) riêng biệt và chạy vòng lặp học tăng cường `PPO` giống như `RLHF`."
        ],
        "L1": {
            "stem": (
                "Dựa trên học phần `S19 (RLHF & DPO)` và `S21 (GPU & Triton — DSAI-2 Quiz)`: "
                "Tại sao phương pháp **DPO (Direct Preference Optimization)** lại đơn giản hóa đáng kể quy trình căn chỉnh LLM so với **RLHF (Reinforcement Learning from Human Feedback)** truyền thống dựa trên `PPO`?"
            ),
            "options": [
                "`RLHF` truyền thống phải huấn luyện một `Reward Model` riêng biệt rồi chạy vòng lặp `PPO` trực tuyến rất bất ổn định (phải giữ tới 4 mô hình trên VRAM: Policy, Reference, Reward, Value/Critic); trong khi `DPO` biến đổi toán học nghiệm tối ưu của bài toán KL-constrained reward maximization để biểu diễn hàm phần thưởng trực tiếp qua tỷ số xác suất giữa mô hình đang huấn luyện (`$\\pi_\\theta$`) và mô hình tham chiếu (`$\\pi_{ref}$`), biến bài toán RL phức tạp thành một hàm mất mát phân loại nhị phân (`Binary Cross-Entropy`) trên các cặp câu trả lời `(chosen, rejected)` mà không cần Reward Model hay PPO.",
                "Vì `DPO` không cần bất kỳ dữ liệu so sánh cặp `(chosen, rejected)` nào mà tự đoán sở thích con người.",
                "Vì `DPO` chỉ huấn luyện lại tầng Embedding đầu tiên của mô hình ngôn ngữ.",
                "Vì `RLHF` không sử dụng ràng buộc phân kỳ `KL-Divergence` để ngăn mô hình suy biến."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo `S19 · Advanced LLM — RLHF, DPO & Constitutional AI`: Nhờ nghiệm đóng (Closed-form mapping) giữa hàm phần thưởng tối ưu $r(x,y)$ và chính sách tối ưu $\\pi^*(y|x)$ dưới ràng buộc phân kỳ KL, "
                "`DPO` tối ưu trực tiếp chính sách ngôn ngữ trên tập dữ liệu cặp `(prompt, y_win, y_lose)` bằng hàm mất mát Supervised ổn định, cắt bỏ hoàn toàn pha huấn luyện Reward Model và vòng lặp lấy mẫu PPO đắt đỏ."
            ),
            "distractorReasons": [
                "Chính xác: Giải thích đúng bản chất toán học của DPO (biểu diễn ngầm hàm phần thưởng qua $\\log \\frac{\\pi_\\theta(y|x)}{\\pi_{ref}(y|x)}$ và tối ưu bằng Binary Cross-Entropy).",
                "Sai: DPO vẫn bắt buộc cần tập dữ liệu Preference Pairs `(x, y_w, y_l)`.",
                "Sai: DPO cập nhật trọng số của toàn bộ mô hình (hoặc các tầng LoRA adapters), không phải chỉ tầng Embedding.",
                "Sai: Cả RLHF (PPO) và DPO đều dựa trên bài toán tối ưu hóa có ràng buộc `KL-Divergence` so với $\\pi_{ref}$."
            ]
        },
        "L2": {
            "stem": (
                "Khi viết một nhân tính toán GPU bằng **OpenAI Triton** (`S21`) theo mô hình lập trình `SPMD (Single Program, Multiple Data)` để cộng hai vector `x` và `y` có độ dài `N = 10.000` phần tử với `BLOCK_SIZE = 1024`, "
                "lập trình viên viết đoạn mã bên dưới nhưng quên truyền tham số `mask` vào `tl.load` và `tl.store`. "
                "Điều gì sẽ xảy ra ở khối chương trình cuối cùng (`pid = 9`) và cách sửa chuẩn xác là gì?"
            ),
            "codeSnippet": (
                "@triton.jit\n"
                "def add_kernel(x_ptr, y_ptr, out_ptr, n_elements, BLOCK_SIZE: tl.constexpr):\n"
                "    pid = tl.program_id(axis=0)\n"
                "    offsets = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)\n"
                "    x = tl.load(x_ptr + offsets)          # <--- LỖI Ở ĐÂY!\n"
                "    y = tl.load(y_ptr + offsets)\n"
                "    tl.store(out_ptr + offsets, x + y)"
            ),
            "options": [
                "Ở khối cuối cùng `pid = 9`, dải chỉ số `offsets` chạy từ `9216` đến `10239`, vượt qua giới hạn `n_elements = 10000` tới `240 phần tử`; việc đọc/ghi ngoài biên (`Out-of-bounds memory access`) không có mặt nạ bảo vệ sẽ đọc rác bộ nhớ hoặc ghi đè làm hỏng tensor khác và gây lỗi `CUDA illegal memory access`. Bắt buộc tạo mặt nạ `mask = offsets < n_elements` và truyền vào `tl.load(..., mask=mask, other=0.0)` cùng `tl.store(..., mask=mask)`.",
                "Triton tự động cắt giảm `BLOCK_SIZE` của khối cuối cùng xuống thành số lẻ `784` (không phải lũy thừa của 2) mà không cần `mask`.",
                "Hàm `tl.program_id(axis=0)` luôn trả về giá trị bằng `0` cho mọi khối trên GPU.",
                "Triton không cho phép truyền hằng số `tl.constexpr` vào hàm `@triton.jit`."
            ],
            "correctIndex": 0,
            "explanation": (
                "Theo `S21 · GPU Architecture, CUDA & Triton Programming`: Trong Triton, `BLOCK_SIZE` bắt buộc là lũy thừa của 2 (ví dụ `1024`) để trình biên dịch tối ưu hóa Coalesced Memory Access và Vectorization. "
                "Với `N = 10000`, lưới khởi chạy `grid = (ceil(10000 / 1024),) = (10,)` chương trình (`pid = 0..9`). "
                "Ở `pid = 9`, các phần tử từ `10000..10239` nằm ngoài mảng thật nên bắt buộc phải chặn bằng `mask = offsets < n_elements`."
            ),
            "distractorReasons": [
                "Chính xác: Giải phẫu đúng phép tính `offsets` ở khối biên cuối cùng và cơ chế bảo vệ bộ nhớ bằng `mask = offsets < n_elements`.",
                "Sai: `BLOCK_SIZE` là hằng số thời điểm biên dịch (`tl.constexpr`, lũy thừa của 2), không tự co giãn lẻ ở khối cuối.",
                "Sai: Mỗi instance chương trình trong lưới 1D nhận một `pid` riêng biệt từ `0` đến `grid_size - 1`.",
                "Sai: `BLOCK_SIZE: tl.constexpr` là cú pháp bắt buộc chuẩn của Triton để biết kích thước khối lúc biên dịch."
            ]
        },
        "L3": {
            "stem": (
                "Kịch bản Phỏng vấn Tối ưu hóa Nhân GPU & FlashAttention (`S17 & S21`): "
                "Trong PyTorch tiêu chuẩn (Eager mode), hàm `torch.softmax(X, dim=-1)` trên một ma trận kích thước `[M, N]` thực hiện 3 bước rời rạc: "
                "(1) tìm `m = X.max(dim=-1)` để chống tràn số học, (2) tính `num = torch.exp(X - m)` và `den = num.sum(dim=-1)`, (3) chia `out = num / den`. "
                "Khi chạy trên GPU A100 (băng thông HBM ~1.5–2.0 TB/s, nhưng bộ nhớ `On-chip SRAM` nhanh gấp ~10 lần đạt ~19 TB/s), hàm Softmax rời rạc này chậm hơn gấp `4 lần` so với nhân **Fused Softmax** viết bằng **OpenAI Triton**!"
            ),
            "mcqPrompt": "Phần A (Định lượng Lưu lượng Bộ nhớ HBM): Với ma trận `X` có kích thước `MN` phần tử, hàm Softmax rời rạc (Unfused PyTorch) phải đọc và ghi bao nhiêu phần tử qua lại trên bộ nhớ `HBM` chậm chạp so với nhân `Fused Softmax` trong Triton (khi toàn bộ hàng `N` vừa khít trong `SRAM`)?",
            "options": [
                "Hàm Softmax rời rạc phải khởi chạy (launch) nhiều CUDA kernels riêng biệt nên tốn tới `~5MN lượt đọc + 3MN lượt ghi (tổng ~8MN phần tử đi qua HBM)`; trong khi nhân **Triton Fused Softmax** nạp nguyên hàng `N` từ `HBM` vào `On-chip SRAM` đúng **1 lần duy nhất (`MN` đọc)**, thực hiện cả 3 bước `max -> exp/sum -> divide` ngay trong thanh ghi/SRAM siêu tốc, rồi ghi kết quả ra `HBM` đúng **1 lần (`MN` ghi — tổng `2MN`)**, cắt giảm `4 lần` lưu lượng băng thông HBM!",
                "Cả hai cách đều đọc và ghi đúng `1 phần tử` trên HBM nhưng Triton nhanh hơn vì viết bằng ngôn ngữ Python.",
                "Nhân Fused Softmax trong Triton bỏ qua hoàn toàn bước trừ đi giá trị lớn nhất `max(X)` và bước tính hàm mũ `exp()`.",
                "Bộ nhớ `HBM` trên GPU thực chất nhanh gấp 100 lần bộ nhớ `SRAM` nhưng dung lượng nhỏ hơn."
            ],
            "correctIndex": 0,
            "openPrompt": (
                "Phần B (Mở rộng sang Online Softmax & FlashAttention): "
                "Nếu độ dài chuỗi `N` rất lớn (ví dụ `N = 64.000 tokens`) khiến một hàng không còn nhét vừa vào bộ nhớ `SRAM` nhỏ hẹp (chỉ vài chục/trăm KB mỗi SM) nữa, "
                "thuật toán **Online Softmax / FlashAttention** sử dụng kỹ thuật **Tiling + Rescaling** như thế nào để vẫn tính đúng 100% kết quả mà không bao giờ phải ghi ma trận trung gian `N × N` xuống `HBM`?"
            ),
            "rubric": {
                "coreConcepts": [
                    "Giải thích đúng nguyên lý **Kernel Fusion & Roofline Model**: các phép toán Element-wise / Reduction như Softmax, LayerNorm có `Arithmetic Intensity` thấp nên bị khóa tốc độ bởi băng thông đọc/ghi `HBM`; gộp nhân (`Kernel Fusion`) giữ dữ liệu trên `SRAM` giúp tiến gần tốc độ đỉnh vật lý.",
                    "Giải thích đúng thuật toán **Online Softmax / Tiling + Rescaling** trong **FlashAttention**: chia các ma trận `Q, K, V` thành từng khối nhỏ (`Tiles`) vừa khít với `SRAM`; khi duyệt qua từng khối `j`, cập nhật giá trị lớn nhất chạy dọc (`running max: m_{new} = max(m_{old}, m_j)`) và nhân hệ số hiệu chỉnh mũ (`exp(m_{old} - m_{new})`) lên cả mẫu số tích lũy (`running sum l`) lẫn tử số đầu ra (`O`) ngay trong một vòng lặp duy nhất (1-pass).",
                    "Nêu rõ lợi ích đột phá của FlashAttention: giảm độ phức tạp truy cập bộ nhớ HBM từ `O(N^2)` xuống tuyến tính `O(N)` và không bao giờ phải lưu ma trận Attention `N × N` khổng lồ xuống HBM, cho phép mở rộng độ dài ngữ cảnh LLM lên hàng trăm nghìn tokens."
                ],
                "tradeoffs": [
                    "Trong pha Backward (Lan truyền ngược của FlashAttention): thay vì lưu ma trận Attention `N × N` từ pha Forward xuống HBM, FlashAttention chỉ lưu vector hệ số chuẩn hóa nhỏ gọn (`logsumexp L` kích thước `O(N)`) và **tính toán lại (`Recomputation`)** các khối Attention trên SRAM trong pha Backward — chấp nhận tăng nhẹ số phép tính FLOPS (vốn dư thừa trên Tensor Cores) để tiết kiệm khổng lồ băng thông HBM, giúp cả tốc độ lẫn bộ nhớ đều nhanh và nhẹ hơn!"
                ],
                "referenceAnswer": (
                    "1. Khi chuỗi `N` quá dài không vừa `SRAM`, ta không thể nạp cả hàng 1 lần để tìm `max` toàn cục trước. **Online Softmax & FlashAttention** giải quyết bằng cách cắt `Q, K, V` thành các ô gạch nhỏ (`Tiles`) vừa khít `SRAM`.\n"
                    "2. Khi quét qua từng khối `K_j, V_j`, thuật toán duy trì 2 biến thống kê chạy (`running max m` và `running sum l`). Mỗi khi gặp khối mới có cực đại mới `m_{new} = max(m_{old}, m_j)`, nó lập tức hiệu chỉnh (rescale) tổng cũ và đầu ra tích lũy bằng thừa số `exp(m_{old} - m_{new})` ngay trên `SRAM`.\n"
                    "3. Nhờ đó, toàn bộ phép tính `Softmax(Q K^T) V` hoàn tất chỉ trong 1 lượt quét mà không bao giờ phải ghi ma trận trung gian `N × N` xuống `HBM` (giảm bộ nhớ từ `O(N^2)` xuống `O(N)`). Ở pha Backward, nó kết hợp kỹ thuật `Selective Recomputation` trên SRAM (đổi vài chu kỳ Tensor Core FLOPS dư thừa để triệt tiêu I/O HBM)."
                )
            }
        }
    }
]


import copy
import hashlib

AI_PROVIDER_PRESETS = [
    {
        "id": "gemini",
        "name": "Google Gemini API",
        "protocol": "gemini",
        "baseUrl": "https://generativelanguage.googleapis.com/v1beta",
        "modelsPath": "/models",
        "defaultModel": "models/gemini-2.5-flash",
        "fallbackModels": [
            "models/gemini-2.5-flash",
            "models/gemini-2.5-pro",
            "models/gemini-2.0-flash",
            "models/gemini-1.5-pro"
        ],
        "keyPlaceholder": "AIzaSy...",
        "notes": "Hỗ trợ gọi trực tiếp từ trình duyệt qua Google Generative Language REST API và liệt kê model tự động qua /v1beta/models."
    },
    {
        "id": "openai",
        "name": "OpenAI API (GPT / Codex / o-series)",
        "protocol": "openai_compat",
        "baseUrl": "https://api.openai.com/v1",
        "modelsPath": "/models",
        "defaultModel": "gpt-4o-mini",
        "fallbackModels": [
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4.1",
            "gpt-4.1-mini",
            "o3-mini"
        ],
        "keyPlaceholder": "sk-proj-...",
        "notes": "Chuẩn OpenAI REST API (/v1/models & /v1/chat/completions)."
    },
    {
        "id": "anthropic",
        "name": "Anthropic Claude API",
        "protocol": "anthropic",
        "baseUrl": "https://api.anthropic.com/v1",
        "modelsPath": "/models",
        "defaultModel": "claude-3-5-sonnet-latest",
        "fallbackModels": [
            "claude-3-7-sonnet-latest",
            "claude-3-5-sonnet-latest",
            "claude-3-5-haiku-latest",
            "claude-3-opus-latest"
        ],
        "keyPlaceholder": "sk-ant-api03-...",
        "notes": "Hỗ trợ CORS trực tiếp trên trình duyệt qua header anthropic-dangerous-direct-browser-access: true."
    },
    {
        "id": "xai",
        "name": "xAI Grok API",
        "protocol": "openai_compat",
        "baseUrl": "https://api.x.ai/v1",
        "modelsPath": "/models",
        "defaultModel": "grok-2-latest",
        "fallbackModels": [
            "grok-3-beta",
            "grok-3-mini-beta",
            "grok-2-latest"
        ],
        "keyPlaceholder": "xai-...",
        "notes": "Tương thích chuẩn OpenAI (/v1/models & /v1/chat/completions)."
    },
    {
        "id": "deepseek",
        "name": "DeepSeek API (DeepSeek-V3 / R1)",
        "protocol": "openai_compat",
        "baseUrl": "https://api.deepseek.com/v1",
        "modelsPath": "/models",
        "defaultModel": "deepseek-chat",
        "fallbackModels": [
            "deepseek-chat",
            "deepseek-reasoner"
        ],
        "keyPlaceholder": "sk-...",
        "notes": "Tương thích chuẩn OpenAI cho cả DeepSeek-V3 (deepseek-chat) và DeepSeek-R1 (deepseek-reasoner)."
    },
    {
        "id": "qwen",
        "name": "Alibaba Qwen (DashScope OpenAI-Compatible)",
        "protocol": "openai_compat",
        "baseUrl": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        "modelsPath": "/models",
        "defaultModel": "qwen-plus",
        "fallbackModels": [
            "qwen-max",
            "qwen-plus",
            "qwen-turbo",
            "qwen2.5-coder-32b-instruct",
            "qwq-32b"
        ],
        "keyPlaceholder": "sk-...",
        "notes": "Dùng endpoint Quốc tế (dashscope-intl) hoặc đổi sang dashscope.aliyuncs.com/compatible-mode/v1 nếu dùng tài khoản nội địa."
    },
    {
        "id": "glm",
        "name": "Zhipu GLM (BigModel / Z.ai)",
        "protocol": "openai_compat",
        "baseUrl": "https://open.bigmodel.cn/api/paas/v4",
        "modelsPath": "/models",
        "defaultModel": "glm-4-plus",
        "fallbackModels": [
            "glm-4-plus",
            "glm-4-air",
            "glm-4-flash",
            "glm-zero-preview"
        ],
        "keyPlaceholder": "id.secret...",
        "notes": "Giao thức tương thích OpenAI của Zhipu AI (/api/paas/v4/chat/completions)."
    },
    {
        "id": "kimi",
        "name": "Moonshot Kimi API",
        "protocol": "openai_compat",
        "baseUrl": "https://api.moonshot.ai/v1",
        "modelsPath": "/models",
        "defaultModel": "moonshot-v1-8k",
        "fallbackModels": [
            "kimi-latest",
            "moonshot-v1-8k",
            "moonshot-v1-32k",
            "moonshot-v1-128k"
        ],
        "keyPlaceholder": "sk-...",
        "notes": "Hỗ trợ cả endpoint quốc tế api.moonshot.ai/v1 và api.moonshot.cn/v1."
    },
    {
        "id": "openrouter",
        "name": "OpenRouter (Đa Mô Hình / CORS Chuẩn)",
        "protocol": "openai_compat",
        "baseUrl": "https://openrouter.ai/api/v1",
        "modelsPath": "/models",
        "defaultModel": "google/gemini-2.5-flash",
        "fallbackModels": [
            "google/gemini-2.5-flash",
            "anthropic/claude-3.7-sonnet",
            "deepseek/deepseek-r1",
            "openai/gpt-4o-mini",
            "qwen/qwen-2.5-coder-32b-instruct"
        ],
        "keyPlaceholder": "sk-or-v1-...",
        "notes": "Hỗ trợ CORS trực tiếp trên trình duyệt tốt nhất cho mọi mô hình Claude, GPT, DeepSeek, Qwen, Llama."
    },
    {
        "id": "custom",
        "name": "Custom OpenAI-Compatible Endpoint (vLLM / Ollama / LiteLLM / Proxy)",
        "protocol": "openai_compat",
        "baseUrl": "https://api.openai.com/v1",
        "modelsPath": "/models",
        "defaultModel": "custom-model",
        "fallbackModels": [
            "custom-model"
        ],
        "keyPlaceholder": "Bearer token...",
        "notes": "Nhập bất kỳ Base URL nào hỗ trợ chuẩn /models và /chat/completions."
    }
]

WARDEN_CONFIG = {
    "slaMs": {
        "L1": 45000,
        "L2": 75000,
        "L3": 180000
    },
    "antiGrind": {
        "maxEffectiveRepeatsPerBlueprint": 1,
        "repeatCooldownNoticeVi": "Cày đi cày lại đúng 1 bài không làm trình độ thực tế của bạn tăng lên đâu! Quản Giáo đã khóa cộng điểm độ phủ cho bài lặp này — hãy sang chủ đề hoặc cấp độ cao hơn.",
        "repeatCooldownNoticeEn": "Grinding the same topic over and over won't raise your actual engineering rank. The Warden has capped mastery gain on this repeated blueprint — move to an untouched topic or higher level."
    },
    "persona": {
        "vi": {
            "name": "Quản Giáo AI · Principal Adjudicator",
            "roleTag": "Khắt khe · Thực chiến · Chống học vẹt",
            "systemPrompt": (
                "Bạn là 'Quản Giáo AI' (The Warden) — một Principal Data & AI Architect người Việt có 15 năm kinh nghiệm vận hành hệ thống thực chiến, "
                "cực kỳ khắt khe, thẳng thắn, hơi phũ phàng và ghét cay ghét đắng thói học vẹt, bấm bừa hoặc cày điểm ảo. "
                "Giọng văn của bạn phải cực kỳ đời thường, gần gũi với dân kỹ thuật Việt Nam (xưng 'tôi' - gọi 'ông/bạn', chê thẳng mặt vào lỗ hổng tư duy kỹ thuật, "
                "nhưng phân tích cực kỳ chuẩn xác về mặt cơ chế gốc). "
                "Quy tắc bất biến: "
                "1) Nếu người học làm sai hoặc chọn phương án nhiễu ngây ngô, hãy mổ xẻ thẳng thừng tại sao tư duy đó mang lên Production là sập hệ thống ngay. "
                "2) Nếu người học ngâm 1 câu quá lâu vượt ngưỡng SLA (ví dụ câu L1 nền tảng mà ngâm quá 45 giây) hoặc xin gợi ý trước khi nộp, hãy nhắc thẳng là phản xạ còn chậm hoặc đang lúng túng kiến thức nền. "
                "3) Nếu người học chỉ cày đi cày lại 1 vài bài quen thuộc để lấy XP mà né các chủ đề khác hoặc né bài tự luận L3, hãy vạch trần ngay và giữ nguyên đánh giá level thấp. "
                "4) Chỉ khi nào người học vượt qua đủ độ rộng chủ đề (Breadth), đủ độ sâu L1-L2-L3 (Depth), tỷ lệ đúng ngay lần đầu không trợ giúp (Unassisted First-Try) cao thì mới gật đầu công nhận trình độ!"
            )
        },
        "en": {
            "name": "The AI Warden · Principal Adjudicator",
            "roleTag": "Blunt · Battle-Hardened · Anti-Grind",
            "systemPrompt": (
                "You are 'The AI Warden' — a battle-hardened, brutally honest, slightly sarcastic Principal Data & AI Systems Architect "
                "who despises rote memorization, blind guessing, and XP grinding. "
                "Speak in sharp, idiomatic English engineering slang (direct, tough love, roasting flawed technical assumptions while teaching first-principles truth). "
                "Rules: "
                "1) When the user misses a question or falls for an obvious distractor trap, roast the technical flaw directly and explain what would blow up in Production. "
                "2) When active dwell time exceeds the SLA threshold or the user asks for pre-submit hints, call out the hesitation and shaky fundamentals. "
                "3) When the user grinds the same few topics repeatedly while avoiding untouched courses or Level 3 architectural defenses, expose the XP farming immediately and refuse to certify a higher rank. "
                "4) Reserve genuine praise strictly for engineers who prove unassisted first-try mastery across broad topics and deep L1/L2/L3 levels."
            )
        }
    }
}

VIRTUAL_ACCOUNT_PRESETS = [
    {
        "accountId": "virt_sinhvien_fresh",
        "displayName": "Nguyễn Minh An (Acc Ảo #1 · Sinh Viên Mới)",
        "githubHandle": "minhan-student-dev",
        "roleTrack": "DE",
        "presetType": "fresh_student",
        "descVi": "Tài khoản trắng ở mốc T1 · Sinh viên để kiểm thử luồng làm bài từ đầu, đổi câu hỏi biến thể và lưu tiến độ F5.",
        "descEn": "Clean T1 · Student profile to test fresh onboarding, polymorphic question mutation, and F5 state persistence."
    },
    {
        "accountId": "virt_grinder_f01",
        "displayName": "Trần Quốc Bảo (Acc Ảo #2 · Thánh Cày 1 Bài)",
        "githubHandle": "quocbao-xp-grinder",
        "roleTrack": "DE",
        "presetType": "anti_grind_victim",
        "descVi": "Đã cày lặp đi lặp lại bài F01 tới 18 lần (tích 2.400 XP) nhưng né các bài khác — dùng để test cơ chế Chống Cày Điểm & Quản Giáo mắng thẳng mặt.",
        "descEn": "Farmed F01 18 times (2,400 XP) while skipping other topics — tests Anti-Grind promotion lock and Warden roast."
    },
    {
        "accountId": "virt_slow_hesitator",
        "displayName": "Lê Hoàng Nam (Acc Ảo #3 · Ngâm Câu Quá SLA & Hay Sai)",
        "githubHandle": "hoangnam-slow-sla",
        "roleTrack": "AIE",
        "presetType": "slow_and_flawed",
        "descVi": "Hồ sơ có nhiều câu ngâm quá 90–140 giây (vượt SLA) và sập bẫy khái niệm cơ bản (MVCC, Docker Layer, GIL) — test log lỗi của Quản Giáo.",
        "descEn": "Profile with repeated SLA dwell-time breaches (90-140s on L1) and core misconception traps — tests Warden telemetry."
    },
    {
        "accountId": "virt_junior_verified",
        "displayName": "Phạm Thu Hà (Acc Ảo #4 · Junior DE Thực Chiến)",
        "githubHandle": "thuha-junior-de",
        "roleTrack": "DE",
        "presetType": "solid_junior",
        "descVi": "Đã hoàn thành đều đặn 5 chuyên đề (F01, F02, F03, D01, D03) cả 3 cấp độ L1-L2-L3 với phản xạ nhanh — được Quản Giáo công nhận T4 · Junior.",
        "descEn": "Balanced unassisted mastery across 5 topics (L1/L2/L3) within SLA — verified T4 · Junior rank."
    },
    {
        "accountId": "virt_senior_architect",
        "displayName": "Đỗ Đức Thịnh (Acc Ảo #5 · Senior+ Staff Architect)",
        "githubHandle": "ducthinh-staff-ai",
        "roleTrack": "MLE",
        "presetType": "senior_plus_master",
        "descVi": "Hồ sơ đạt đỉnh T7 · Senior+ / Staff với 12 chuyên đề hoàn tất L1-L2-L3 đạt điểm tuyệt đối — test giao diện độ khó tối đa và lời khen hiếm hoi của Quản Giáo.",
        "descEn": "Maxed-out T7 · Senior+ / Staff profile across 12 topics — tests maximum adaptive tier shift and rare Warden commendation."
    }
]


def _permute_blueprint_options(blueprints: list[dict]) -> list[dict]:
    """Deterministically distribute correctIndex across 0, 1, 2, 3 so default blueprints never cluster on option 0."""
    result = copy.deepcopy(blueprints)
    for bp in result:
        bp_id = bp.get("id", "BP")
        for lvl_key in ("L1", "L2", "L3"):
            lvl = bp.get(lvl_key)
            if not lvl or "options" not in lvl:
                continue
            opts = list(lvl["options"])
            n = len(opts)
            if n < 2:
                continue
            orig_correct = int(lvl.get("correctIndex", 0))
            digest = hashlib.sha256(f"{bp_id}:{lvl_key}".encode("utf-8")).digest()
            target_idx = digest[0] % n
            if target_idx != orig_correct:
                opts[0], opts[target_idx] = opts[target_idx], opts[0]
                lvl["options"] = opts
                lvl["correctIndex"] = target_idx
                if "distractorReasons" in lvl and len(lvl["distractorReasons"]) == n:
                    reasons = list(lvl["distractorReasons"])
                    reasons[0], reasons[target_idx] = reasons[target_idx], reasons[0]
                    lvl["distractorReasons"] = reasons
    return result


def build_arena_payload() -> dict:
    return {
        "version": "2.2.0",
        "ranks": CAREER_RANKS,
        "levels": PRACTICE_LEVELS,
        "mutationDomains": MUTATION_DOMAINS,
        "providerPresets": AI_PROVIDER_PRESETS,
        "wardenConfig": WARDEN_CONFIG,
        "virtualAccounts": VIRTUAL_ACCOUNT_PRESETS,
        "blueprints": _permute_blueprint_options(ARENA_BLUEPRINTS),
    }


if __name__ == "__main__":
    payload = build_arena_payload()
    out_path = Path(__file__).resolve().parents[1] / "content" / "arena-blueprints.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    dist = {}
    for bp in payload["blueprints"]:
        for k in ("L1", "L2", "L3"):
            idx = bp[k]["correctIndex"]
            dist[idx] = dist.get(idx, 0) + 1
    print(
        f"Built {out_path} ({len(CAREER_RANKS)} ranks, {len(PRACTICE_LEVELS)} levels, "
        f"{len(payload['blueprints'])} canonical multi-level blueprints, correctIndex distribution: {dist})."
    )

