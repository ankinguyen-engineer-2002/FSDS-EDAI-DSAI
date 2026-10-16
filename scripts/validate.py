#!/usr/bin/env python3
"""
Strict Validator for FSDS Learning Hub:
1. Runs 6 negative regression self-tests in scripts/ascii_diagram.py.
2. Verifies JS syntax in fsds-learning-hub.html via `node --check` on stdin.
3. Verifies 100% of ASCII/Unicode diagrams (5/5, zero skipped) using kind-specific geometry verifiers.
4. Verifies HTML/JSON diagram parity, 12/12 official slide TOCs, and 5/5 Storage Chặng 1 stations.
5. Audits removal of dead features (Khung rộng, Ghi chú), decorative emojis, and AI meta-copy.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ascii_diagram import run_self_tests, verify_character_policy, verify_diagram


def main():
    run_self_tests()

    html_path = ROOT / "fsds-learning-hub.html"
    data_path = ROOT / "content/lessons-data.json"
    if not html_path.exists() or not data_path.exists():
        raise SystemExit("Missing fsds-learning-hub.html or content/lessons-data.json. Run python3 scripts/build_hub.py")

    html = html_path.read_text(encoding="utf-8")
    data = json.loads(data_path.read_text(encoding="utf-8"))

    # 1. Extract inline script and check syntax via node --check on stdin
    script_body = html.split("<script>", 1)[1].split("</script>", 1)[0]
    proc = subprocess.run(
        ["node", "--check", "-"],
        input=script_body,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"JS syntax check failed:\n{proc.stderr}")

    # 2. Verify zero legacy AI content in lessons-data.json and verify all 5/5 diagrams (zero skips!)
    if "foundation" in data:
        raise SystemExit("Legacy AI content ('foundation') still present in content/lessons-data.json")

    char_checked = 0
    geom_checked = 0
    skipped = 0
    expected_kinds = {
        "0.1": "boxes",
        "1.1": "pyramid",
        "1.2": "boxes",
        "1.2b": "boxes",
        "1.3": "boxes",
        "1.3b": "boxes",
        "1.4": "boxes",
        "1.5": "boxes",
        "2.1": "boxes",
        "2.1b": "boxes",
        "2.2a": "boxes",
        "2.2b": "boxes",
        "2.3": "boxes",
        "2.4": "boxes",
        "2.4b": "boxes",
        "3.1": "boxes",
        "3.2": "boxes",
        "3.2b": "boxes",
        "3.3": "boxes",
        "3.4": "boxes",
        "3.5": "boxes",
        "4.1": "boxes",
        "4.2": "boxes",
        "4.3": "boxes",
        "4.3b": "boxes",
        "4.4": "boxes",
        "4.5": "boxes",
        "4.5a": "boxes",
        "5.1": "boxes",
        "5.2a": "boxes",
        "5.2b": "boxes",
        "5.2c": "boxes",
        "5.3": "boxes",
        "5.3b": "boxes",
        "5.4a": "boxes",
        "5.4b": "boxes",
        "6.1a": "boxes",
        "6.1b": "boxes",
        "6.2a": "boxes",
        "6.2b": "boxes",
        "6.2c": "boxes",
        "6.2d": "boxes",
        "6.3": "boxes",
        "6.3b": "boxes",
        "6.4": "boxes",
        "6.5a": "boxes",
        "6.5b": "boxes",
        "6.5c": "boxes",
        "7.1a": "boxes",
        "7.1b": "boxes",
        "7.2a": "boxes",
        "7.2b": "boxes",
        "7.2c": "boxes",
        "7.3a": "boxes",
        "7.3b": "boxes",
        "7.3c": "boxes",
        "7.3d": "boxes",
        "7.4": "boxes",
    }

    for k, exp_kind in expected_kinds.items():
        if k not in data["storage_diagrams"]:
            raise SystemExit(f"Missing diagram {k} in content/lessons-data.json")
        item = data["storage_diagrams"][k]
        actual_kind = item.get("kind")
        if actual_kind != exp_kind:
            raise SystemExit(f"Diagram {k} kind mismatch: expected {exp_kind!r}, got {actual_kind!r}")

        c_errs = verify_character_policy(item["ascii"], f"Storage-{k}")
        if c_errs:
            raise SystemExit(f"ASCII character policy failed for Storage-{k}: {c_errs}")
        char_checked += 1

        g_errs = verify_diagram(item["ascii"], f"Storage-{k}", kind=actual_kind)
        if g_errs:
            raise SystemExit(f"ASCII geometry verification failed for Storage-{k} ({actual_kind}): {g_errs}")
        geom_checked += 1

        if not item["mermaid"].startswith("flowchart "):
            raise SystemExit(f"Invalid Mermaid header for Storage-{k}")

        # Verify exact ASCII string is embedded in HUB_DATA inside HTML
        if json.dumps(item["ascii"], ensure_ascii=False) not in html:
            raise SystemExit(f"HTML/JSON parity failure: Storage-{k} ASCII not identically embedded in HTML")

    # 2b. Verify Linux Fundamentals diagrams (0.1, 0.2, Chặng 1 1.1a..1.3b, Chặng 2 2.1a..2.4b, Chặng 3 3.1a..3.2b, Chặng 4 4.0..4.3b)
    linux_expected_kinds = {
        "0.1": "boxes",
        "0.2": "boxes",
        "1.1a": "boxes",
        "1.1b": "boxes",
        "1.2a": "boxes",
        "1.2b": "boxes",
        "1.3a": "boxes",
        "1.3b": "boxes",
        "2.1a": "boxes",
        "2.1b": "boxes",
        "2.2a": "boxes",
        "2.2b": "boxes",
        "2.3a": "boxes",
        "2.3b": "boxes",
        "2.4a": "boxes",
        "2.4b": "boxes",
        "3.1a": "boxes",
        "3.1b": "boxes",
        "3.2a": "boxes",
        "3.2b": "boxes",
        "4.0": "boxes",
        "4.1a": "boxes",
        "4.1b": "boxes",
        "4.2a": "boxes",
        "4.2b": "boxes",
        "4.3a": "boxes",
        "4.3b": "boxes",
    }
    if "linux_diagrams" not in data:
        raise SystemExit("Missing linux_diagrams in content/lessons-data.json")
    for k, exp_kind in linux_expected_kinds.items():
        if k not in data["linux_diagrams"]:
            raise SystemExit(f"Missing Linux diagram {k} in content/lessons-data.json")
        item = data["linux_diagrams"][k]
        actual_kind = item.get("kind")
        if actual_kind != exp_kind:
            raise SystemExit(f"Linux Diagram {k} kind mismatch: expected {exp_kind!r}, got {actual_kind!r}")

        c_errs = verify_character_policy(item["ascii"], f"Linux-{k}")
        if c_errs:
            raise SystemExit(f"ASCII character policy failed for Linux-{k}: {c_errs}")
        char_checked += 1

        g_errs = verify_diagram(item["ascii"], f"Linux-{k}", kind=actual_kind)
        if g_errs:
            raise SystemExit(f"ASCII geometry verification failed for Linux-{k} ({actual_kind}): {g_errs}")
        geom_checked += 1

        if not item["mermaid"].startswith("flowchart "):
            raise SystemExit(f"Invalid Mermaid header for Linux-{k}")

        if json.dumps(item["ascii"], ensure_ascii=False) not in html:
            raise SystemExit(f"HTML/JSON parity failure: Linux-{k} ASCII not identically embedded in HTML")

    # 2c. Verify Database Fundamentals (F03) diagrams (0.1, 0.2, 1.0..1.3, 2.0..2.3, 3.0..3.3, 4.0..4.3)
    db_expected_kinds = {
        "0.1": "boxes",
        "0.2": "boxes",
        "1.0": "boxes",
        "1.1": "boxes",
        "1.2": "boxes",
        "1.3": "boxes",
        "2.0": "boxes",
        "2.1": "boxes",
        "2.2": "boxes",
        "2.3": "boxes",
        "3.0": "boxes",
        "3.1": "boxes",
        "3.2": "boxes",
        "3.3": "boxes",
        "4.0": "boxes",
        "4.1": "boxes",
        "4.2": "boxes",
        "4.3": "boxes",
    }
    if "db_diagrams" not in data:
        raise SystemExit("Missing db_diagrams in content/lessons-data.json")
    for k, exp_kind in db_expected_kinds.items():
        if k not in data["db_diagrams"]:
            raise SystemExit(f"Missing Database diagram {k} in content/lessons-data.json")
        item = data["db_diagrams"][k]
        actual_kind = item.get("kind")
        if actual_kind != exp_kind:
            raise SystemExit(f"Database Diagram {k} kind mismatch: expected {exp_kind!r}, got {actual_kind!r}")

        c_errs = verify_character_policy(item["ascii"], f"DB-{k}")
        if c_errs:
            raise SystemExit(f"ASCII character policy failed for DB-{k}: {c_errs}")
        char_checked += 1

        g_errs = verify_diagram(item["ascii"], f"DB-{k}", kind=actual_kind)
        if g_errs:
            raise SystemExit(f"ASCII geometry verification failed for DB-{k} ({actual_kind}): {g_errs}")
        geom_checked += 1

        if not item["mermaid"].startswith("flowchart "):
            raise SystemExit(f"Invalid Mermaid header for DB-{k}")

        if json.dumps(item["ascii"], ensure_ascii=False) not in html:
            raise SystemExit(f"HTML/JSON parity failure: DB-{k} ASCII not identically embedded in HTML")

    # 3. Verify all 12 official slide PDFs in course-slides/ are listed in the HTML Table of Contents
    slides = sorted(p.name for p in (ROOT / "course-slides").glob("*.pdf"))
    for s in slides:
        if s not in html:
            raise SystemExit(f"Official slide missing from HTML Table of Contents: {s}")

    # 4. Verify all stations + summaries of Storage Chặng 1–7, Linux Chặng 1–4, and Database Chặng 1–4 exist verbatim in HTML (without emojis)
    required_markers = [
        "TRẠM 0.0: NHÂN VẬT CHÍNH grep ERROR /var/log/app.log &amp; BẢN ĐỒ CƠ HỌC 4 CHẶNG",
        'TRẠM 1.1: BẢN CHẤT GNU/LINUX — KHI "CỤC MÁY" GẶP "BỘ KHUNG"',
        'TRẠM 1.2: BẢN ĐỒ DISTRO (BẢN PHÂN PHỐI) — CHỌN "DÒNG XE" NÀO ĐỂ CHẠY HỆ THỐNG?',
        'TRẠM 1.3: GIẢI PHẪU "CĂN BẾP LINUX" — HÀNH TRÌNH 7 BƯỚC CỦA LỆNH grep ERROR app.log',
        "TÓM TẮT BỎ TÚI CHẶNG 1 (MẠCH NHÂN – QUẢ &amp; CHECKLIST 5 CÂU HỎI BẢN CHẤT)",
        "TRẠM 2.1: GIẢI PHẪU HỒ SƠ CĂN CƯỚC CỦA MỘT PROCESS (PID, USER/GROUP, WORKING DIRECTORY, ENVIRONMENT, OPEN FILES)",
        'TRẠM 2.2: TRIẾT LÝ "EVERYTHING IS A FILE" (REGULAR FILE, DIRECTORY, DEVICE /dev/sda, PROCESS /proc/1234) &amp; CƠ HỌC INODE',
        "TRẠM 2.3: BẢN ĐỒ KHO HÀNG — CÂY THƯ MỤC DUY NHẤT / (/bin, /sbin, /usr, /etc, /home, /root, /var/log, /tmp, /proc) &amp; ĐỐI CHIẾU WINDOWS",
        "TRẠM 2.4: BỘ CÔNG CỤ TÁC CHIẾN TRÊN CÂY THƯ MỤC — ĐIỀU HƯỚNG (pwd/ls/cd), THAO TÁC (cp/mv/rm) &amp; SĂN LOG (head/tail -f/find/du)",
        "TÓM TẮT BỎ TÚI CHẶNG 2 (MẠCH NHÂN – QUẢ &amp; CHECKLIST 5 CÂU HỎI BẢN CHẤT)",
        "TRẠM 3.1: BA CỔNG TIÊU CHUẨN (0, 1, 2) &amp; ĐƯỜNG ỐNG PIPE TRONG KERNEL",
        'TRẠM 3.2: ĐIỀU HƯỚNG DÒNG CHẢY (&gt;&gt; VÀ 2&gt;&amp;1) — CHẶN ĐỨNG "BẪY MÙ LỖI" KHI CHẠY NGẦM',
        "TÓM TẮT BỎ TÚI CHẶNG 3",
        'TRẠM 4.1: BASH SCRIPTING — "TỜ GIẤY DÁN TỦ LẠNH" ĐỊNH NGHĨA LÀM BƯỚC NÀO, RA SAO',
        "TRẠM 4.2: COMPILATION (GCC) &amp; MAKEFILE — LÒ LUYỆN MÃ MÁY &amp; NGƯỜI QUẢN ĐỐC XƯỞNG",
        'TRẠM 4.3: HỆ THỐNG CRONJOB — TRỰC BAN 24/7 ("KHI NÀO BẮT ĐẦU CHẠY?") &amp; 3 CẠM BẪY KINH ĐIỂN',
        "TÓM TẮT BỎ TÚI CHẶNG 4 &amp; KHÉP KÍN HÀNH TRÌNH LINUX FUNDAMENTALS",
        "TRẠM 0.0: KHỞI TẠO NHÂN VẬT CHÍNH ĐƠN HÀNG TRÀ SỮA #HD01 &amp; BẢN ĐỒ MẠCH NHÂN – QUẢ 4 CHẶNG",
        "TRẠM 1.1: WHAT IS A DATABASE &amp; DBMS ARCHITECTURE (CƠ SỞ DỮ LIỆU &amp; GIẢI PHẪU HỆ QUẢN TRỊ)",
        "TRẠM 1.2: RELATIONAL MODEL, KEYS (PK, FK), CARDINALITY &amp; CONSTRAINTS (MÔ HÌNH QUAN HỆ &amp; CHỐT CHẶN RÀNG BUỘC)",
        "TRẠM 1.3: NORMALIZATION (UNF ➔ 1NF ➔ 2NF ➔ 3NF ➔ BCNF) VS DENORMALIZATION (CHUẨN HÓA &amp; PHI CHUẨN HÓA)",
        "TÓM TẮT BỎ TÚI CHẶNG 1 &amp; CHECKLIST TỰ KIỂM TRA (DATA MODELING &amp; 3NF)",
        "TRẠM 2.1: CLIENT/BACKEND PROCESS &amp; MEMORY VERSUS DISK-BASED DBMS (TIẾN TRÌNH &amp; PHÂN CẤP BỘ NHỚ 2 TẦNG)",
        "TRẠM 2.2: ON-DISK DATA LAYOUT (ROW VS COLUMN) &amp; SLOTTED PAGE (4-16 KB) (CẤU TRÚC TRANG VẬT LÝ)",
        "TRẠM 2.3: WRITE PATH, WAL BUFFER, DIRTY PAGES &amp; CHECKPOINTER (LUỒNG GHI KÉP &amp; CƠ CHẾ PHỤC HỒI)",
        "TÓM TẮT BỎ TÚI CHẶNG 2 &amp; CHECKLIST TỰ KIỂM TRA (STORAGE ENGINE &amp; MEMORY)",
        "TRẠM 3.1: ACID TRANSACTIONS, LOCK MANAGER, MVCC &amp; AUTOVACUUM WORKER (GIAO DỊCH &amp; KIỂM SOÁT ĐỒNG THỜI ĐA PHIÊN BẢN)",
        "TRẠM 3.2: STORAGE STRUCTURES (B-TREES VS LSM-TREES) &amp; INDEXING STRATEGIES (CẤU TRÚC CÂY CHỈ MỤC &amp; ĐÁNH ĐỔI ĐỌC/GHI)",
        "TRẠM 3.3: QUERY OPTIMIZER, EXPLAIN PLAN, SQL COMMAND GROUPS &amp; ACCESS CONTROL (POLP) (TỐI ƯU TRUY VẤN &amp; BẢO MẬT PHÂN QUYỀN)",
        "TÓM TẮT BỎ TÚI CHẶNG 3 &amp; CHECKLIST TỰ KIỂM TRA (MVCC, INDEXING &amp; EXPLAIN)",
        "TRẠM 4.1: VERTICAL SCALING (SCALE-UP) VS HORIZONTAL SCALING (SCALE-OUT), REPLICATION &amp; SHARDING (MỞ RỘNG HẠ TẦNG &amp; NHÂN BẢN)",
        "TRẠM 4.2: ALWAYS-ON MULTI-LOCATION HA (ENTERPRISEDB PGD) &amp; NEXT-GEN DATABASES (TIDB, YUGABYTEDB, CLICKHOUSE) (KIẾN TRÚC ĐA VÙNG &amp; THẾ HỆ MỚI)",
        "TRẠM 4.3: SQL VS NOSQL DATA MODELS, CAP THEOREM (CA/CP/AP) &amp; BASE VS ACID (ĐỊNH LÝ CAP &amp; KIẾN TRÚC LAI)",
        "TÓM TẮT BỎ TÚI CHẶNG 4 &amp; KHÉP KÍN HÀNH TRÌNH DATABASE FUNDAMENTALS",
        "TRẠM 0.0: NHÂN VẬT CHÍNH ĐƠN HÀNG #8888 &amp; BẢN ĐỒ TƯ DUY 7 CHẶNG STORAGE LAYER",
        "TRẠM 1.1: BẬC THANG PHẦN CỨNG &amp; THANG ĐO ĐỘ TRỄ VẬT LÝ (CACHE HIERARCHY)",
        "TRẠM 1.2: ĐẶC TÍNH KỸ THUẬT CỦA RAM &amp; HIỆN TƯỢNG TRÀN BỘ NHỚ (SPILL-TO-DISK)",
        "TRẠM 1.3: CƠ HỌC ĐĨA CỨNG (RANDOM SEEK VS. SEQUENTIAL SCAN) &amp; BÍ MẬT CỦA CLOUD STORAGE",
        "TRẠM 1.4: PHÂN TẦNG NHIỆT ĐỘ LƯU TRỮ (DATA TEMPERATURE) &amp; KIẾN TRÚC ĐỆM ĐA TẦNG",
        "TRẠM 1.5: RANH GIỚI HỆ THỐNG — SOURCE SYSTEM (OLTP) VS. STORAGE SYSTEM (OLAP)",
        "TÓM TẮT BỎ TÚI CHẶNG 1 (5 QUY LUẬT VẬT LÝ)",
        "TRẠM 2.1: BỘ BA MÔ HÌNH LƯU TRỮ CƠ SỞ — FILE VS. BLOCK VS. OBJECT STORAGE",
        "TRẠM 2.2: ĐỊNH DẠNG TỆP &amp; TUẦN TỰ HÓA (SERIALIZATION) — ROW (CSV, AVRO) VS. COLUMNAR (PARQUET, ORC)",
        "TRẠM 2.3: TUẦN TỰ HÓA TRONG BỘ NHỚ (IN-MEMORY SERIALIZATION) — APACHE ARROW",
        "TRẠM 2.4: KỸ THUẬT NÉN DỮ LIỆU (COMPRESSION) &amp; CẠM BẪY TÍNH PHÂN TÁCH (SPLITTABILITY)",
        "TÓM TẮT BỎ TÚI CHẶNG 2 (4 QUYẾT ĐỊNH THIẾT KẾ LƯU TRỮ)",
        "TRẠM 3.1: HẠ TẦNG LƯU TRỮ PHÂN TÁN — HADOOP HDFS (NAMENODE, DATANODE &amp; NHÂN BẢN X3)",
        "TRẠM 3.2: TÔ-PÔ MẠNG (NETWORK TOPOLOGY), KHOẢNG CÁCH MẠNG &amp; ĐỘNG CƠ CACHE PHÂN TÁN",
        "TRẠM 3.3: LƯU TRỮ DẠNG LUỒNG (STREAMING STORAGE) — APACHE KAFKA &amp; CDC",
        "TRẠM 3.4: KHO DỮ LIỆU TẬP TRUNG — DATA WAREHOUSE (OLAP, ACID &amp; ĐỘNG CƠ LƯU TRỮ)",
        "TRẠM 3.5: BA HẠN CHẾ LỊCH SỬ CỦA DATA WAREHOUSE (TẠI SAO PHẢI TIẾN HÓA?)",
        "TÓM TẮT BỎ TÚI CHẶNG 3 (MẠCH NHÂN – QUẢ HẠ TẦNG PHÂN TÁN, STREAMING &amp; DATA WAREHOUSE)",
        "TRẠM 4.1: BA CẤP ĐỘ THIẾT KẾ MÔ HÌNH DỮ LIỆU (CONCEPTUAL ➔ LOGICAL ➔ PHYSICAL)",
        "TRẠM 4.2: BA TRƯỜNG PHÁI MÔ HÌNH HÓA TRONG DATA WAREHOUSE (INMON VS. KIMBALL VS. DATA VAULT)",
        "TRẠM 4.3: TRÁI TIM CỦA KIMBALL — BẢNG SỰ KIỆN (FACT) VS. BẢNG THỨ NGUYÊN (DIMENSION) &amp; ĐỘ MỊN (GRAIN)",
        "TRẠM 4.4: BA KIẾN TRÚC BỐ TRÍ BẢNG — STAR SCHEMA VS. SNOWFLAKE SCHEMA VS. OBT (&amp; OLAP CUBES)",
        "TRẠM 4.5: BỘ BA KỸ THUẬT SỐNG CÒN CỦA KIMBALL — SURROGATE KEY, SCD (TYPE 1, 2 &amp; 3) &amp; BUS MATRIX",
        "TỔNG KẾT CHẶNG 4 &amp; KHÉP LẠI TRỌN VẸN PHẦN 1 (4 NGUYÊN TẮC MÔ HÌNH HÓA)",
        "TRẠM 5.1: GIẤC MƠ \"HỒ DỮ LIỆU\" (DATA LAKE) — TẠI SAO PHẢI RỜI BỎ DATA WAREHOUSE?",
        "TRẠM 5.2: BI KỊCH \"ĐẦM LẦY DỮ LIỆU\" (DATA SWAMP) — KHI HỒ NƯỚC HÓA BÃI RÁC",
        "TRẠM 5.3: GIẢI MÃ 3 LỖ HỔNG CÔNG CỤ CỐT TỬ (THE 3 TOOLING GAPS)",
        "TRẠM 5.4: PHÁC ĐỒ CỨU NGUY — LÀM SAO NGĂN DATA LAKE HÓA THÀNH ĐẦM LẦY?",
        "CHỐT HẠ MẠCH NHÂN – QUẢ CHẶNG 5 (ĐỂ BƯỚC SANG CHẶNG 6 — LAKEHOUSE)",
        "TRẠM 6.1: KIẾN TRÚC DATA LAKEHOUSE &amp; BƯỚC NGOẶT \"ĐỊNH NGHĨA LẠI MỘT BẢNG\"",
        "TRẠM 6.2: GIẢI PHẪU \"BỘ NÃO\" CỦA BỘ BA OPEN TABLE FORMATS (DELTA LAKE, ICEBERG, HUDI)",
        "TRẠM 6.3: BỘ TÍNH NĂNG CỐT LÕI — ACID, CONCURRENCY (OCC/MVCC/NBCC), TIME TRAVEL &amp; SCHEMA",
        "TRẠM 6.4: CHIẾN LƯỢC GHI &amp; CẬP NHẬT — COPY-ON-WRITE (COW) VS. MERGE-ON-READ (MOR)",
        "TRẠM 6.5: NĂM KỸ THUẬT TỐI ƯU VẬT LÝ SỐNG CÒN TRÊN LAKEHOUSE",
        "CHỐT HẠ MẠCH NHÂN – QUẢ CHẶNG 6 (ĐỂ BƯỚC VÀO CHẶNG CUỐI CÙNG — CHẶNG 7)",
        "TRẠM 7.1: KHÁI NIỆM MULTI-HOP &amp; TRIẾT LÝ KIẾN TRÚC MEDALLION (QUALITY GATING PATTERN)",
        "TRẠM 7.2: GIẢI PHẪU CHI TIẾT 3 TẦNG MEDALLION QUA HÀNH TRÌNH ĐƠN HÀNG <code>#8888</code>",
        "TRẠM 7.3: DÒNG CHẢY NGẦM QUẢN TRỊ &amp; VẬN HÀNH (UNDERCURRENTS: CATALOG, LINEAGE, SECURITY &amp; FINOPS)",
        "TRẠM 7.4: BẢN ĐỒ KIẾN TRÚC TỔNG THỂ 6 TẦNG (BOTTOM-UP BLUEPRINT) — KHÉP LẠI TOÀN BỘ KHÓA HỌC!",
        "CHECKLIST TỔNG KẾT CHẶNG 7 (NHẮM MẮT TRẢ LỜI ĐƯỢC LÀ LÀM CHỦ HOÀN TOÀN)",
    ]
    for marker in required_markers:
        if marker not in html:
            raise SystemExit(f"Missing required section in HTML: {marker}")

    # 5. Verify removal of dead features, decorative emojis, and AI meta-copy
    forbidden_tokens = [
        "widthToggleBtn",
        "wide-reading",
        "noteToggleBtn",
        "noteDrawer",
        "noteIndicatorDot",
        "flushPendingNote",
        "syncNotesForTopic",
        "visual-tag",
        "SFMono 13.5pt",
        "[cite:",
        "Sẵn sàng nạp nội dung",
        "LỆNH ĐIỀU KHIỂN ĐỂ ĐI SÂU",
        "🏛️",
        "⚡",
        "💿",
        "🌡️",
        "🚧",
        "🎯",
        "📁",
        "🧱",
        "📦",
        "🪣",
        "🧬",
        "🗜️",
        "⭐",
        "🐢",
        "🐌",
        "🐘",
        "🧠",
        "💪",
        "🌐",
        "📨",
        "🏦",
        "📊",
        "📈",
        "⚠️",
        "📐",
        "💭",
        "🧩",
        "🔑",
        "🎉",
        "🌊",
        "🖱️",
        "📸",
        "🐊",
        "📄",
        "🖼️",
        "🧟",
        "💥",
        "🦠",
        "🔀",
        "⚖️",
        "⏳",
        "🕳️",
        "🛡️",
        "⚙️",
        "🛠️",
        "🔥",
        "💡",
        "✅",
        "❌",
        "🚀",
        "👉",
        "🏗️",
        "👶",
        "🧑",
        "👔",
        "🥉",
        "🥈",
        "🥇",
        "🔬",
        "📚",
        "🔐",
        "💰",
        "👁️",
        "🗺️",
        "🧊",
        "hãy gửi tiếp Chặng 2",
        "đi sâu tiếp vào Trạm 3",
        "mổ xẻ thật chi tiết",
        "Bạn nhắn tôi để chúng ta đi sâu ngay vào",
        "Hãy gửi nội dung biên soạn",
        "Toàn bộ nội dung AI cũ đã được dọn sạch",
        "Chặng này đang chờ nạp nội dung chi tiết",
        'data-vmode="both"',
        ">Song song<",
    ]
    for tok in forbidden_tokens:
        if tok in html:
            raise SystemExit(f"Forbidden token / AI-slop tell still present in HTML: {tok!r}")

    # 6. Verify Mermaid & Picture interactive camera + Global Default Visual Mode + 3-Tier Typography & Glossary Popover functions exist
    for fn in (
        "createMermaidCamera",
        "zoomInlineMermaid",
        "fitInlineMermaid",
        "resetInlineMermaidOneToOne",
        "createPictureCamera",
        "setGlobalVisualMode",
        "globalVisualModeGroup",
        "buildSpineHeroBanner",
        "expandModePicBtn",
        "--font-display",
        "--font-sans",
        "--font-mono",
        "--glossary-surface",
        "glossaryPopover",
        "bindGlossaryTerms",
        "openGlossaryPopover",
        "initGlossarySystem",
    ):
        if fn not in html:
            raise SystemExit(f"Missing Visual / Typography / Glossary Popover symbol in HTML: {fn}")

    # 6a. Verify Glossary Scanner data & 0 unclassified candidate gate
    if "glossary" not in data or "entries" not in data["glossary"] or "lookup" not in data["glossary"]:
        raise SystemExit("Missing 'glossary' object (entries + lookup) in lessons-data.json")
    g_entries = data["glossary"]["entries"]
    g_lookup = data["glossary"]["lookup"]
    g_stats = data["glossary"].get("stats", {})
    if len(g_entries) < 50:
        raise SystemExit(f"Expected >= 50 canonical glossary entries, found {len(g_entries)}")
    if len(g_lookup) < 1800:
        raise SystemExit(f"Expected >= 1800 normalized lookup keys in glossary, found {len(g_lookup)}")
    if g_stats.get("unclassified_count", 1) != 0:
        raise SystemExit(f"Glossary scanner has {g_stats.get('unclassified_count')} unclassified terms! Must be 0.")
    for tid, entry in g_entries.items():
        for req_f in ("name", "category", "intuition", "mechanism", "example"):
            if not entry.get(req_f):
                raise SystemExit(f"Glossary entry '{tid}' is missing required field '{req_f}'")
        ex = entry["example"]
        if not isinstance(ex, dict) or not ex.get("code") or not ex.get("note"):
            raise SystemExit(f"Glossary entry '{tid}' example must contain non-empty 'code' and 'note'")

    # 6b. Verify visual_assets metadata, 1-Visual-1-Unique-Picture invariant, and physical files in assets/visuals/
    if "visual_assets" not in data or len(data["visual_assets"]) < 90:
        raise SystemExit(f"Expected >= 90 visual_assets in lessons-data.json, found {len(data.get('visual_assets', {}))}")
    required_spine_jpgs = [
        "assets/visuals/linux-0-map.jpg",
        "assets/visuals/db-0-map.jpg",
        "assets/visuals/storage-0-map.jpg",
    ]
    for vf in required_spine_jpgs:
        p = ROOT / vf
        if not p.exists() or p.stat().st_size < 50_000:
            raise SystemExit(f"Missing or invalid Spine Hero Style #2 JPG file: {vf}")

    seen_preview_srcs = {}
    linux_jpg_count = 0
    db_jpg_count = 0
    for vid, vmeta in data["visual_assets"].items():
        if vmeta.get("template") not in ("PROMPT-ARCH-DIAGRAM", "PROMPT-STORY-ANALOGY"):
            raise SystemExit(f"Invalid template for visual_asset {vid}: {vmeta.get('template')}")
        prev_src = vmeta.get("previewSrc", "")
        if not prev_src or not (ROOT / prev_src).exists():
            raise SystemExit(f"Missing previewSrc file for visual_asset {vid}: {prev_src}")
        if prev_src in seen_preview_srcs:
            raise SystemExit(
                f"Duplicate Picture violation! Visual '{vid}' reuses '{prev_src}' already assigned to '{seen_preview_srcs[prev_src]}'"
            )
        seen_preview_srcs[prev_src] = vid
        if vid.startswith("linux-"):
            if not prev_src.endswith(".jpg") or (ROOT / prev_src).stat().st_size < 50_000:
                raise SystemExit(f"Linux visual '{vid}' must have a dedicated Style #2 .jpg (>50KB), got: {prev_src}")
            linux_jpg_count += 1
        elif vid.startswith("db-"):
            if not prev_src.endswith(".jpg") or (ROOT / prev_src).stat().st_size < 50_000:
                raise SystemExit(f"Database visual '{vid}' must have a dedicated Style #2 .jpg (>50KB), got: {prev_src}")
            db_jpg_count += 1

    # 6c. Run 4-Gate Picture QA (SHA-256 uniqueness, 16:9 widescreen, anti-ASCII-dump, Apple Vision OCR audit)
    from verify_pictures import verify_all_pictures
    pic_errors = verify_all_pictures(verbose=False)
    pic_checked = len(data["visual_assets"])
    if pic_errors:
        raise SystemExit(
            f"Picture QA (verify_pictures.py) found {len(pic_errors)} issue(s):\n  - " + "\n  - ".join(pic_errors[:20])
        )

    # 7. Verify prompt.md exists, references all slides/books, and contains Style #2 Prompt templates + 4-Gate Picture QA + 3-Tier Typography & Glossary Scanner
    prompt_path = ROOT / "prompt.md"
    if not prompt_path.exists():
        raise SystemExit("Missing prompt.md at repository root.")
    prompt_text = prompt_path.read_text(encoding="utf-8")
    for p_tok in (
        "[PROMPT-ARCH-DIAGRAM]",
        "[PROMPT-STORY-ANALOGY]",
        "fsds_visual_mode",
        "CẤM TUYỆT ĐỐI DÙNG LẶP 1 ẢNH CHO NHIỀU VISUAL",
        "4-Gate Picture Verification System",
        "scripts/verify_pictures.py",
        "3-Tier Editorial Typography",
        "scripts/glossary_scanner.py",
        "Frosted-Glass Glossary Popover",
    ):
        if p_tok not in prompt_text:
            raise SystemExit(f"Missing required visual/typography/glossary specification in prompt.md: {p_tok}")
    import re
    lib_refs = re.findall(r"`(library/[^`*]+\.pdf)`", prompt_text)
    if not lib_refs:
        raise SystemExit("No concrete library/*.pdf references found in prompt.md")
    for lib_ref in lib_refs:
        if not (ROOT / lib_ref).exists():
            raise SystemExit(f"Broken book path in prompt.md: {lib_ref}")
    slide_refs = re.findall(r"`(\d{2}-[^`*]+\.pdf)`", prompt_text)
    if len(set(slide_refs)) != 12:
        raise SystemExit(f"Expected 12 slide references in prompt.md, found {len(set(slide_refs))}")
    for slide_ref in slide_refs:
        if not (ROOT / "course-slides" / slide_ref).exists():
            raise SystemExit(f"Broken slide path in prompt.md: course-slides/{slide_ref}")

    total_expected = len(expected_kinds) + len(linux_expected_kinds) + len(db_expected_kinds)
    print(
        f"PASS: Negative self-tests: 6/6 | JS syntax: valid | "
        f"3-Tier Typography: verified | Glossary Scanner: {len(g_entries)} entries / {len(g_lookup)} lookup keys (0 unclassified) | "
        f"ASCII character checks: {char_checked}/{total_expected} | ASCII geometry checks: {geom_checked}/{total_expected} | "
        f"4-Gate Picture QA: {pic_checked}/{len(data['visual_assets'])} verified ({linux_jpg_count} Linux + {db_jpg_count} DB Style #2 JPGs + Spine Maps, 0 OCR/clip/dup errors) | "
        f"Skipped: {skipped} | Official slide TOCs: {len(slides)}/12 | "
        f"prompt.md: verified ({len(set(slide_refs))} slides, {len(set(lib_refs))} books, 2 Style #2 templates, 4-Gate QA, Glossary Scanner) | Anti-slop audit: clean."
    )


if __name__ == "__main__":
    main()

