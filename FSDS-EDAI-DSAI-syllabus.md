# FSDS - EDAI - DSAI Learning Syllabus

> Bản ghi trung tâm của chương trình học. Nội dung trong các slide hiện có sẽ được dễ hiểu hóa, cô đọng hóa, trực quan hóa và bổ sung kiến thức nền tảng theo một mạch liên kết xuyên suốt.

## Cách đọc chương trình

- **Lesson** là một đơn vị học dự kiến; số lesson là ước lượng, không phải giới hạn cứng.
- **Module** là các câu hỏi và năng lực cần hình thành trong lesson.
- **Lab** là bằng chứng thực hành; một chủ đề chưa có lab chưa được xem là đã học xong.
- Mạch học đi từ **engineering foundation → data engineering → data science/ML/LLM → distributed platform → cloud/operations → coursework**.
- Các kiến thức dùng chung như Linux, Python, database, API, testing, containers và observability sẽ được nối lại trong các lab xuyên suốt.

## I. Engineering foundation

| Lesson | Số lesson | Modules | Labs | Tech stack |
|---|---:|---|---|---|
| Fundamentals of Engineering - Linux | 1 | GNU/Linux; Bash scripting; compilation & Makefile; cron job | Cài Ubuntu; Linux commands 101 | Ubuntu, Makefile |
| Fundamentals of Engineering - Python | 1 | Python fundamentals; virtual environment; best practices; async/sync programming | Data crawler bằng Python | Python |
| Fundamentals of Engineering - Database | 1 | OOP for engineering; database concepts; SQL và NoSQL; DDL/DML/DQL/DCL/TCL; cost và performance optimization | Setup SQL database; thực hành truy vấn | SQLAlchemy ORM |
| Fundamentals of Engineering - Web API | 1 | API architecture styles; authentication; FastAPI; validation/type enforcement; middleware; healthcheck; performance metrics và guideline | Implement API theo nhiều architecture styles | FastAPI, Locust |
| Fundamentals of Engineering - Validation & Verification | 1 | Quality paradigms; black-box testing; white-box testing; mutation testing; Hoare logic; symbolic execution; TDD | Nhiều loại test cho API | pytest, unittest |
| Fundamentals of Engineering - Containerization & Orchestration | 2 | VM và containers; Docker architecture; container technologies; commands; volumes/network; private registry; Compose; build/run/optimize/manage | Dockerize API; local stack với Compose; container-based testing | Docker |
| Data Engineering - Ingestion Layer | 2 | Data architectures; source systems; Kafka ecosystem; Kafka fundamentals; Kafka operations; CDC methods | End-to-end CDC system | Kafka, Debezium, PostgreSQL |
| Data Engineering - Storage Layer | 1 | Storage layer; data lake và data swamp; lakehouse; multi-hop architecture | Lakehouse from scratch | Delta Lake, Trino, Hive, MinIO |
| Data Engineering - Transformation Layer (Batch) | 2 | Spark architecture; data abstraction/API; optimization; advanced tuning; operations | Spark batch job xử lý data quality | Spark |
| Data Engineering - Transformation Layer (Stream) | 2 | Notions of time; Flink APIs; windows; late data; state; fault tolerance; optimization; deployment modes | Stream job xử lý data quality | Flink |
| Data Engineering - Consumption Layer | 1 | Dimensional modeling; SCD; OLAP engines; materialized views; feature core/view/transformation; ML integration | Feature store và feature processing pipeline | ClickHouse, Pinot, Feast |
| Data Engineering - Orchestration & Governance | 1 | Orchestration benefits; beyond cron; idempotency; backfill; dynamic pipelines; Airflow architecture/operators/data passing; administration/scaling; validation; contracts; governance | Deploy/administer Airflow; multi-step data/feature pipelines with lineage | Airflow, DataHub |

### Mini Coursework - 1 đến 2 tuần

Kết hợp API, database, container, ingestion, storage, transformation và orchestration thành một data pipeline nhỏ có kiểm thử, lineage và tài liệu vận hành.

## II. Data science, machine learning và LLM

| Lesson | Số lesson | Modules | Labs | Tech stack |
|---|---:|---|---|---|
| Introduction to Data Science & Machine Learning | 1 | NumPy; Pandas; Matplotlib; PyTorch; machine learning; deep learning | End-to-end data science project; OCR application | NumPy, Pandas, Matplotlib, PyTorch |
| Introduction to LLM, RAG & Agent | 1 | Transformer architecture; LLM; RAG; agents; guardrails | Fine-tune open-source LLM; RAG app; agentic AI system | LLM stack |
| Model Serving Design Patterns | 2 | Model serving patterns; model loading patterns | Task queue ML system | LLM, RabbitMQ |
| Dive into LLM Serving | 1 | KV cache; serving challenges và solutions | LLM serving endpoint | vLLM, TensorRT-LLM, SGLang |

## III. Distributed platform và cloud

| Lesson | Số lesson | Modules | Labs | Tech stack |
|---|---:|---|---|---|
| Distributed Systems | 1 | Distributed systems; fallacies; vertical/horizontal scaling; stateful/stateless; partitions; packet loss; node crash; CAP; PACELC; BASE; ACID; consensus; replication; sharding; eventual consistency | Design exercise và failure simulation | Distributed systems concepts |
| Kubernetes | 2 | K8s architecture; Pod/Deployment/Service/Ingress/PV/PVC; sidecars; init containers; operators; deployment strategies; Helm/helmfile; secrets; resources | Async job processing; deploy API locally on K8s | Kubernetes, Helm, KServe, HashiCorp Vault |
| Kubeflow & Distributed Training | 2 | Kubeflow architecture/operators; distributed training; distributed storage; GPU scheduling | Deploy Kubeflow; distributed training pipeline | Kubeflow |
| Cloud Services | 1 | Cloud hierarchy/IAM; VPC/networking; storage/lifecycle/locality; GCP ML/data stack; IaaS/PaaS/SaaS; billing/FinOps | Free-tier GCP; Terraform infrastructure; Ansible deployment; gateway | GCP, NGINX |
| Routing & Gateway | 1 | Routing/load balancing/service discovery; retry/circuit breaker/fallback/timeout; AuthN/AuthZ; IP restriction/geofencing; PII; protocol translation; rate limits/quota/budget/prioritization; semantic caching; tracing; A/B test | Scenario design and gateway policy lab | Gateway stack |
| Infrastructure as Code | 1 | IaC fundamentals; Terraform/Ansible architecture, commands, best practices; hybrid workflow; drift detection | Provision and reconcile infrastructure | Terraform, Ansible |
| Versioning & CI/CD | 1 | Code/data/model/experiment versioning; Git/GitHub; CI/CD; AIDE pipelines; Jenkins/DVC/MLflow architectures | Multiple CI/CD pipelines | Jenkins, DVC, MLflow |
| Observable Systems | 2 | Logs, metrics, traces; observable architecture; drift detection; LLM/agent telemetry | Monitoring systems | OpenTelemetry, Evidently, Prometheus, Grafana, Elasticsearch, Filebeat, Kibana, Jaeger, Langfuse |
| Misc Problems | 1 | Security best practices; SRE; repository design; service mesh; open discussion | Architecture review and open problems | Context-dependent |

### Final Coursework - 2 tháng

Xây dựng, triển khai và vận hành một hệ thống Data/AI end-to-end: API, data ingestion, lakehouse/warehouse, batch/stream transformation, feature hoặc model serving, orchestration, Kubernetes/cloud, CI/CD, security và observability.

## IV. Mạch phụ thuộc kiến thức

```text
Linux + Python
      ↓
Database + API + Testing
      ↓
Docker + Compose
      ↓
Kafka/CDC + Storage/Lakehouse
      ↓
Spark/Flink + Consumption/Feature
      ↓
Airflow + Governance + Lineage
      ↓
ML/LLM + Serving
      ↓
Distributed Systems + Kubernetes + Kubeflow
      ↓
Cloud + Gateway + IaC + CI/CD
      ↓
Observability + SRE + Final Coursework
```

## V. Phương pháp biên tập duy nhất

Mọi chủ đề được viết theo một đường học thống nhất:

1. **Bức tranh tổng quát:** một sơ đồ kiến trúc duy nhất cho toàn hệ thống.
2. **Vai trò từng phần:** mỗi thành phần tồn tại để giải quyết vấn đề gì.
3. **Cắt lớp nền tảng:** chỉ giữ các lớp lõi cần để suy luận; bỏ chi tiết thứ yếu.
4. **Luồng chạy thực tế:** theo một kịch bản cụ thể xuyên qua toàn bộ các lớp.
5. **Đào sâu có đối chiếu:** mở chi tiết khi cần và luôn nối lại bản đồ tổng quan.

Nội dung phải cô đọng, dùng tiếng Việt gần gũi, kết hợp chữ với hình và dùng chuyển động để biểu diễn sự thay đổi hoặc dòng dữ liệu. Công nghệ chỉ xuất hiện đúng vai trò của nó trong hệ thống; không học bằng danh sách công cụ hay command rời rạc.

Các file PDF trong `course-slides/` là nguồn kiểm tra độ phủ. Learning hub là phiên bản đã biên tập lại, không sao chép thứ tự hoặc cách trình bày của deck gốc.
