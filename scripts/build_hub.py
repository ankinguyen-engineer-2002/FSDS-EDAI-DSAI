#!/usr/bin/env python3
"""
Build script for the FSDS · EDAI · DSAI Personal Study Hub.
- Embeds macOS Terminal SF-Mono-*.otf fonts (SFMono-Regular 13.5pt, line-height 1.25, 0 letter-spacing).
- Applies an austere, editorial technical-manual aesthetic (zero decorative icons/emojis, zero AI-slop badges).
- Generates & mechanically verifies all 5/5 ASCII/Unicode diagrams (pyramid + box verifiers, zero skips).
- Pairs every diagram with an interactive Mermaid viewport (Zoom −/100%/+/Vừa khung, Drag-to-Pan, Cmd/Ctrl+Wheel).
- Preserves 100% verbatim educational prose (D02 Storage Layer - Chặng 1) and 100% official Slide TOCs (26 topics).
"""
import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ascii_diagram import (
    display_width,
    join_horizontal,
    make_box,
    pad_center,
    pad_right,
    run_self_tests,
    verify_diagram,
)


def extract_font_faces() -> str:
    """
    Embeds the genuine macOS Terminal.app SF Mono OpenType fonts (UPM=2048, 2252 glyphs)
    so browsers render authentic SFMono-Regular without relying on blocked local() lookups.
    """
    terminal_font_dir = Path("/System/Applications/Utilities/Terminal.app/Contents/Resources/Fonts")
    specs = [
        ("SF-Mono-Regular.otf", 400, "normal", "SFMono-Regular"),
        ("SF-Mono-RegularItalic.otf", 400, "italic", "SFMono-RegularItalic"),
        ("SF-Mono-Medium.otf", 500, "normal", "SFMono-Medium"),
        ("SF-Mono-Semibold.otf", 600, "normal", "SFMono-Semibold"),
        ("SF-Mono-Bold.otf", 700, "normal", "SFMono-Bold"),
    ]
    rules = []
    for filename, weight, style, ps_name in specs:
        fpath = terminal_font_dir / filename
        if fpath.exists():
            b64 = base64.b64encode(fpath.read_bytes()).decode("ascii")
            for family in ("SFMono-Regular", "SF Mono"):
                rules.append(
                    f'@font-face {{ font-family: "{family}"; font-style: {style}; font-weight: {weight}; '
                    f'font-display: block; src: local("{ps_name}"), url("data:font/otf;base64,{b64}") format("opentype"); }}'
                )
    if rules:
        return "\n  ".join(rules)

    snap = ROOT / ".quarantine/2026-10-15/pre-restructure-snapshot/fsds-learning-hub.html"
    if snap.exists():
        lines = snap.read_text(encoding="utf-8").splitlines()
        fonts = [l.strip() for l in lines[:20] if "@font-face" in l]
        return "\n  ".join(fonts)
    return ""


def build_storage_ascii_diagrams() -> dict:
    # Run negative regression suite first to guarantee builder/verifier integrity
    run_self_tests()

    # 1. Trạm 1.1: Pyramid Latency Hierarchy (strict 1:1 slope, zero cell overflow)
    # Inserting the empty slope row ("peak") directly below "▲" ensures:
    #   step=1 -> inner_w=1 (" ")
    #   step=2 -> inner_w=3 ("L1" = 2 cells <= 3)
    #   step=5 -> inner_w=9 ("RAM DDR5" = 8 cells <= 9)
    rows = [
        ("top",  "",         "",                        "▲",                     ""),
        ("peak", "",         "",                        "",                      ""),
        ("row",  "~1 ns",    "L1 CPU Cache",            "L1",                    "◄── Đọc thanh ghi / chỉ lệnh CPU tức thời"),
        ("row",  "~10 ns",   "L2 / L3 CPU Cache",       "CPU",                   "    Băng thông: ~1 TB/s | Giá: Cực đắt (On-die)"),
        ("sep",  "",         "",                        "",                      ""),
        ("row",  "~100 ns",  "RAM (DDR5 / DRAM)",       "RAM DDR5",              "◄── Đọc từ bộ nhớ đệm Redis (Redis read)"),
        ("row",  "(0.1 µs)", "",                        "~100 GB/s",             "    Hàng triệu IOPS | Giá: ~$10 / GB"),
        ("sep",  "",         "",                        "",                      ""),
        ("row",  "~10 µs",   "Mạng nội bộ 1 Gbps",      "Network 1Gbps",         "◄── Memcached gửi gói tin qua mạng LAN"),
        ("row",  "~100 µs",  "NVMe SSD (Flash)",        "SSD (~4 GB/s)",         "◄── RocksDB read (~0.1 ms) | Giá: ~$0.20/GB"),
        ("row",  "~1 ms",    "Ghi CSDL giao dịch",      "Database Insert",       "◄── PostgreSQL thực hiện lệnh INSERT"),
        ("sep",  "",         "",                        "",                      ""),
        ("row",  "~4–10 ms", "Đĩa từ cơ học (HDD)",     "HDD (~200-300 MB/s)",   "◄── Kim đĩa từ di chuyển tìm rãnh (Seek)"),
        ("row",  "",         "Giới hạn ~100 IOPS",      "Giá: ~$0.03/GB",        ""),
        ("sep",  "",         "",                        "",                      ""),
        ("row",  "~100 ms",  "Cloud Object & WAN",      "Object Storage (S3/GCS)", "◄── Gói tin xuyên lục địa (CA -> NL -> CA)"),
        ("row",  "~10 s",    "Chu kỳ làm mới Grafana",  "~3 GB/s* | ~$0.02/GB",  "    hoặc cuộc gọi Zoom quốc tế"),
        ("sep",  "",         "",                        "",                      ""),
        ("row",  "~12 giờ",  "Lưu trữ lạnh (Archival)", "Cloud Archival / Tape", "◄── Phục hồi sao lưu dài hạn"),
        ("base", "",         "",                        "",                      "    Giá: ~$0.004/GB/tháng (rẻ bằng ~1/17)"),
    ]
    N = len(rows) - 1
    pyr_width = 2 * N + 3
    sep_right_tail = 45
    out_1_1 = ["                        THÁP ĐỘ TRỄ VẬT LÝ & CÁC TÁC VỤ THỰC TẾ"]
    for i, (kind, lat, tier, mid_text, note) in enumerate(rows):
        left_spaces = N - i
        inner_w = 2 * i - 1
        ctx = f"Storage-1.1.row[{i}]"
        if kind == "top":
            prefix = pad_right("", 11, context=ctx) + "│ " + pad_right("", 24, context=ctx)
            pyr = (" " * N) + "▲"
            out_1_1.append((prefix + pyr).rstrip())
        elif kind == "sep":
            prefix = "───────────┼─" + ("─" * 24)
            right_dashes = (pyr_width - left_spaces - inner_w - 2) + sep_right_tail
            pyr = ("─" * left_spaces) + "/" + ("─" * inner_w) + "\\" + ("─" * right_dashes)
            out_1_1.append(prefix + pyr)
        elif kind == "base":
            prefix = pad_right("", 11, context=ctx) + "│ " + pad_right("", 24, context=ctx)
            pyr = (" " * left_spaces) + "└" + ("─" * inner_w) + "┘"
            pyr_padded = pad_right(pyr, pyr_width, context=ctx)
            out_1_1.append((prefix + pyr_padded + " " + note).rstrip())
        else:
            prefix = pad_right("  " + lat, 11, context=ctx) + "│ " + pad_right(tier, 24, context=ctx)
            pyr = (" " * left_spaces) + "/" + pad_center(mid_text, inner_w, context=ctx) + "\\"
            pyr_padded = pad_right(pyr, pyr_width, context=ctx)
            line = (prefix + pyr_padded + (" " + note if note else "")).rstrip()
            out_1_1.append(line)
    d1_1 = "\n".join(out_1_1)

    # 2. Trạm 1.2: Spill-to-Disk
    d1_2 = "\n".join([
        "  ┌─────────────────────────────────────────────────────────────────────┐",
        "  │    Dữ liệu 10 triệu đơn hàng đẩy vào RAM của Node tính toán Spark   │",
        "  └──────────────────┬──────────────────────────────────────────────────┘",
        "                     │",
        "                     ├──► [+] Đủ dung lượng RAM",
        "                     │        └──► Xử lý ở tốc độ ~100 ns (~100 GB/s) ──► Hoàn tất cực nhanh!",
        "                     │",
        "                     └──► [!] Vượt quá dung lượng RAM (Ví dụ: Phép JOIN hoặc GROUP BY quá lớn)",
        "                              │",
        "                              ▼",
        "                    ┌──────────────────────────────────────────────────────────────────────┐",
        "                    │ [!] SPILL-TO-DISK (Tràn bộ nhớ xuống đĩa cứng cục bộ SSD / HDD)      │",
        "                    │ • Tốc độ rơi tự do từ 100 ns xuống 100 µs (SSD) hoặc 4–10 ms (HDD)   │",
        "                    │ • Tốn thêm CPU để tuần tự hóa (Serialize) từ RAM xuống đĩa & đọc lại │",
        "                    └──────────────────────────────────────────────────────────────────────┘",
    ])

    # 3. Trạm 1.3: Random Seek vs Sequential Scan
    b3_left = make_box([
        "Đầu đọc đĩa phải liên tục di chuyển tìm vị",
        "trí của từng đơn hàng nằm rải rác trên đĩa:",
        "",
        " [Đơn #12] ──(Seek 4-10ms)──> [Đơn #8888]",
        "     ▲                             │",
        "     └───────(Seek 4-10ms)─────────┘",
        "",
        "[x] Bị bóp nghẹt bởi giới hạn ~100 IOPS!",
    ], inner_width=47, header="1. RANDOM SEEK (Truy xuất ngẫu nhiên từng dòng)", context="Storage-1.3.left")

    b3_right = make_box([
        "Đầu đọc chỉ cần định vị 1 lần, sau đó đọc",
        "trượt một mạch qua các dữ liệu nằm liền kề:",
        "",
        " [Đơn #8886] -> [Đơn #8887] -> [Đơn #8888]...",
        " ══════════════════════════════════════════>",
        " Đạt tối đa băng thông vật lý: 200–300 MB/s",
        "",
        "[+] Tận dụng tối đa Maximum Bandwidth của đĩa!",
    ], inner_width=46, header="2. SEQUENTIAL SCAN (Quét tuần tự liền mạch)", context="Storage-1.3.right")
    d1_3 = "\n".join(join_horizontal([b3_left, b3_right], ["     "], context="Storage-1.3"))

    # 4. Trạm 1.4: Data Temperature (Hot / Warm / Cold)
    b4_hot = make_box([
        "• Phần cứng: RAM / SSD",
        "• Giá: $0.20 – $10 / GB",
        "• Độ trễ: 100 ns – 100 µs",
        "• Dữ liệu: Đơn #8888 vừa",
        "  đặt, đang xử lý nóng",
        "  hoặc nạp đệm tính toán",
    ], inner_width=25, header="[HOT TIER] Lưu trữ Nóng", context="Storage-1.4.hot")

    b4_warm = make_box([
        "• Phần cứng: Cloud Object",
        "• Giá: ~$0.02 / GB / tháng",
        "• Độ trễ: ~100 ms",
        "• Dữ liệu: Lịch sử đơn",
        "  hàng phục vụ chạy",
        "  báo cáo & pipeline tuần",
    ], inner_width=26, header="[WARM TIER] Lưu trữ Ấm", context="Storage-1.4.warm")

    b4_cold = make_box([
        "• Phần cứng: Glacier / Tape",
        "• Giá: ~$0.004 / GB / tháng",
        "• Độ trễ: ~12 giờ chờ",
        "• Dữ liệu: Hóa đơn cũ từ",
        "  3–10 năm trước cất giữ",
        "  để kiểm toán pháp lý",
    ], inner_width=28, header="[COLD / ARCHIVAL] Lưu trữ Lạnh", context="Storage-1.4.cold")
    d1_4 = "\n".join(join_horizontal([b4_hot, b4_warm, b4_cold], ["     ", "     "], {4: [" ──> ", " ──> "]}, context="Storage-1.4"))

    # 5. Trạm 1.5: OLTP vs OLAP
    b5_oltp = make_box([
        "[*] Mục tiêu: Ghi nhận giao dịch Đơn #8888",
        "• Thao tác: INSERT / UPDATE / đọc vài dòng",
        "• Độ trễ yêu cầu: Cực thấp (~1 ms insert)",
        "• Định dạng: Lưu theo DÒNG (Row-oriented)",
        "• Mô hình: Chuẩn hóa (Normalized) nhiều bảng",
        "• Phần cứng: NVMe SSD / Block Storage",
    ], inner_width=44, header="HỆ THỐNG NGUỒN (SOURCE SYSTEM - OLTP)", context="Storage-1.5.oltp")

    b5_olap = make_box([
        "[*] Mục tiêu: Quét 10 triệu đơn tính tổng doanh số",
        "• Thao tác: Quét tuần tự (Sequential Scan) lớn",
        "• Định dạng: Lưu theo CỘT (Columnar) để chỉ đọc",
        "  cột cần tính toán và nén dung lượng cực cao",
        "• Mô hình: Phi chuẩn hóa (Denormalized) giảm JOIN",
        "• Phần cứng: Cloud Object Storage + Cụm phân tán",
    ], inner_width=50, header="HỆ THỐNG LƯUỮ PHÂN TÍCH (STORAGE SYSTEM - OLAP)".replace("LƯUỮ", "LƯU TRỮ"), context="Storage-1.5.olap")
    d1_5 = "\n".join(join_horizontal([b5_oltp, b5_olap], ["      "], {
        3: [" ───> "],
        4: [" Tách "],
        5: [" biệt "],
    }, context="Storage-1.5"))

    # 6. Trạm 2.1: File vs. Block vs. Object Storage
    b21_file = make_box([
        "• Cấu trúc: Cây thư mục phân cấp",
        "  / (Root)",
        "  ├── KinhDoanh",
        "  │   └── 2026/DonHang.csv",
        "  └── NhanSu",
        "• HĐH duyệt con trỏ (pointer)",
        "  qua từng cấp thư mục từ gốc",
        "• Quá tải bảng mục lục (inode)",
        "  khi vượt hàng chục triệu tệp",
    ], inner_width=32, header="1. FILE STORAGE (NAS / ext4)", context="Storage-2.1.file")

    b21_block = make_box([
        "• Cấu trúc: Khối byte cố định",
        "       [Tệp Dữ Liệu Lớn]",
        "         │     │     │",
        "         ▼     ▼     ▼",
        "     [Blk 1][Blk 2][Blk 3]",
        "     (512KB)(512KB)(512KB)",
        "• Mỗi Block có Unique ID riêng",
        "• Độ trễ cực thấp (<1 ms) cho",
        "  OLTP DB & VM nhưng khó chia sẻ",
    ], inner_width=32, header="2. BLOCK STORAGE (SAN / EBS)", context="Storage-2.1.block")

    b21_obj = make_box([
        "• Không gian phẳng (Flat Bucket)",
        "  Bucket: \"ashley-data-lake\"",
        "  ├── ID: \"orders/8888.parquet\"",
        "  ├── Metadata: Tùy biến vô hạn",
        "  │   (ChiNhanh, LoaiDon, ...)",
        "  └── Data: Chuỗi byte bất biến",
        "• Truy cập qua HTTP REST API",
        "• Đọc/ghi luồng song song cực lớn",
        "  (~3 GB/s), giá ~$0.02/GB/tháng",
    ], inner_width=33, header="3. OBJECT STORAGE (S3/ADLS/GCS)", context="Storage-2.1.obj")
    d2_1 = "\n".join(join_horizontal([b21_file, b21_block, b21_obj], ["   ", "   "], context="Storage-2.1"))

    # 7. Trạm 2.2a: Row-Oriented vs. Column-Oriented Serialization
    b22a_row = make_box([
        "Bảng logic: (OrderID | Province | Amount)",
        "• Row 1: [8886 | HaNoi     |  5M]",
        "• Row 2: [8887 | DaNang    | 12M]",
        "• Row 3: [8888 | BinhDuong | 15M]",
        "",
        "Tuần tự hóa trên đĩa (Nối tiếp từng hàng):",
        "[8886|HaNoi|5M][8887|DaNang|12M][8888|BinhDuong|15M]",
        "",
        "[+] Hợp đọc/ghi trọn vẹn 1 bản ghi, CDC/Kafka",
        "[x] Tính tổng 1 cột vẫn phải đọc toàn bộ cột khác",
    ], inner_width=52, header="1. ROW-ORIENTED (CSV, JSONL, Apache Avro)", context="Storage-2.2a.row")

    b22a_col = make_box([
        "Chia bảng thành cụm hàng (Row Group / Split),",
        "sau đó gom từng cột nằm liền kề nhau trên đĩa:",
        "",
        "• Cột OrderID : [8886 | 8887 | 8888 | 8889]",
        "• Cột Province: [HaNoi | DaNang | BinhDuong...]",
        "• Cột Amount  : [5M | 12M | 15M | 8M]",
        "",
        "[+] Chỉ đọc đúng cột cần truy vấn (Column Pruning)",
        "[+] Cùng kiểu dữ liệu nằm sát nhau -> Nén cực chặt",
        "[x] Cập nhật 1 dòng phải giải nén & ghi lại cả khối",
    ], inner_width=51, header="2. COLUMN-ORIENTED (Apache Parquet, Apache ORC)", context="Storage-2.2a.col")
    d2_2a = "\n".join(join_horizontal([b22a_row, b22a_col], ["     "], context="Storage-2.2a"))

    # 8. Trạm 2.2b: Physical Anatomy of an Apache Parquet File
    b22b_layout = make_box([
        "[1] HEADER: Ký hiệu ma thuật 4-byte \"PAR1\" (Nhận diện định dạng tệp Parquet)",
        "──────────────────────────────────────────────────────────────────────────────────────",
        "[2] ROW GROUP 1 (Phân đoạn hàng 1 — ví dụ 128 MB – 1 GB dữ liệu):",
        "    ├── Column Chunk [OrderID]  ──> [Page Header | Data Page 1] [Data Page 2] ...",
        "    ├── Column Chunk [Province] ──> [Dictionary Page] [Data Page 1 (RLE/Bit-pack)]",
        "    └── Column Chunk [Amount]   ──> [Data Page 1] [Data Page 2] ...",
        "──────────────────────────────────────────────────────────────────────────────────────",
        "[3] ROW GROUP 2 (Phân đoạn hàng 2 — nơi chứa Đơn hàng #8888):",
        "    ├── Column Chunk [OrderID]  ──> [Data Page 1 (Min: 5001, Max: 9999)] ...",
        "    └── Column Chunk [Amount]   ──> [Data Page 1] ...",
        "──────────────────────────────────────────────────────────────────────────────────────",
        "[4] FOOTER METADATA (Nằm ở ĐÁY tệp — Động cơ truy vấn luôn đọc phần này ĐẦU TIÊN!):",
        "    • Schema của bảng, phiên bản & cấu trúc Dremel (Definition / Repetition Levels)",
        "    • Thống kê từng Column Chunk: Min, Max, Null Count (Dùng để nhảy cóc Data Skipping)",
        "    • Con trỏ vị trí byte (Byte Offset) bắt đầu của từng Row Group & Column Chunk",
        "    • Kết thúc bằng độ dài Footer (4-byte) + Ký hiệu ma thuật 4-byte \"PAR1\"",
    ], inner_width=88, header="CẤU TRÚC VẬT LÝ BÊN TRONG TỆP APACHE PARQUET", context="Storage-2.2b")
    d2_2b = "\n".join(l.rstrip() for l in b22b_layout)

    # 9. Trạm 2.3: In-Memory Serialization — Apache Arrow
    b23_before = make_box([
        "[Vùng nhớ Apache Spark / JVM]",
        "              │",
        "   (1) CPU Serialize ra chuỗi byte",
        "              ▼",
        "    [Bộ đệm Byte trung gian]",
        "              │",
        "   (2) CPU Deserialize & chép vùng nhớ",
        "              ▼",
        "[Vùng nhớ Python / Pandas / C++]",
        "",
        "[x] Lãng phí 70-80% thời gian CPU chỉ",
        "    để dịch qua lại trên cùng thanh RAM!",
    ], inner_width=42, header="1. TRƯỚC KHI CÓ APACHE ARROW", context="Storage-2.3.before")

    b23_after = make_box([
        "┌──────────────────────────────────────────┐",
        "│ BỐ CỤC BỘ NHỚ CỘT CHUẨN HÓA APACHE ARROW │",
        "│ • OrderID: [8886, 8887, 8888] (Contiguous│",
        "│ • Amount : [5M, 12M, 15M]      Buffers)  │",
        "│ • Shredding: Tách phẳng JSON lồng nhau   │",
        "└──────────────────────────────────────────┘",
        "          ▲                    ▲",
        "          │ Đọc Zero-copy      │ Đọc Zero-copy",
        "   [Apache Spark / JVM]   [Python / Pandas / ML]",
        "[+] Truyền thẳng con trỏ địa chỉ RAM (Zero-copy)",
        "[+] Ánh xạ trực tiếp tệp từ đĩa qua Virtual Memory",
        "[+] Giao tiếp xuyên ngôn ngữ: C/Rust/Java/Python",
    ], inner_width=50, header="2. KHI DÙNG APACHE ARROW (IN-MEMORY STANDARD)", context="Storage-2.3.after")
    d2_3 = "\n".join(join_horizontal([b23_before, b23_after], ["     "], {5: [" ──> "]}, context="Storage-2.3"))

    # 10. Trạm 2.4: Compression & Splittability
    b24_bad = make_box([
        "Tệp nén khối đơn: \"orders.csv.gz\" (100 GB - Gzip)",
        "┌────────────────────────────────────────────────┐",
        "│ [Luồng mã hóa liền mạch từ Byte đầu đến cuối]  │",
        "└────────────────────────────────────────────────┘",
        "        ▲ Không biết mốc bắt đầu ở giữa tệp!",
        "        │",
        "  [Máy chủ 1] phải tự đọc tuần tự hết 100 GB,",
        "  trong khi [Máy chủ 2 ... 100] ngồi chờ không!",
        "[x] Mất hoàn toàn sức mạnh xử lý song song!",
    ], inner_width=50, header="1. NON-SPLITTABLE (Nén khối đơn Gzip nguyên tệp)", context="Storage-2.4.bad")

    b24_good = make_box([
        "Container Format: \"orders.parquet\" / \"orders.avro\"",
        "┌───────────────┬───────────────┬───────────────┐",
        "│ Row Group 1   │ Row Group 2   │ Row Group 3   │",
        "│ (Snappy/ZSTD) │ (Snappy/ZSTD) │ (Snappy/ZSTD) │",
        "└───────────────┴───────────────┴───────────────┘",
        "        ▲               ▲               ▲",
        "        │               │               │",
        "   [Máy chủ 1]     [Máy chủ 2]     [Máy chủ 3]",
        "[+] Đọc & giải nén độc lập cùng lúc trên 100 máy!",
    ], inner_width=51, header="2. SPLITTABLE (Đóng gói khối nội bộ Parquet/Avro)", context="Storage-2.4.good")
    d2_4 = "\n".join(join_horizontal([b24_bad, b24_good], ["     "], context="Storage-2.4"))

    # 11. Trạm 3.1: Hadoop HDFS Architecture (NameNode, DataNodes, x3 Replication & Erasure Coding)
    dn1_box = make_box([
        "DataNode 1 (Rack 1)",
        "• [Block 1] Bản gốc",
        "• Task Map tại chỗ",
    ], inner_width=21, context="Storage-3.1.dn1")
    dn2_box = make_box([
        "DataNode 2 (Rack 2)",
        "• [Block 1] Bản sao 2",
        "• [Block 2] Bản gốc",
    ], inner_width=23, context="Storage-3.1.dn2")
    dn4_box = make_box([
        "DataNode 4 (Rack 2)",
        "• [Block 1] Bản sao 3",
        "• [Block 5] Bản sao",
    ], inner_width=23, context="Storage-3.1.dn4")
    dn_row = ["  " + l for l in join_horizontal(
        [dn1_box, dn2_box, dn4_box],
        ["        ", "        "],
        {2: [" ─────> ", " ─────> "]},
        context="Storage-3.1.dns"
    )]

    b31_hdfs = make_box([
        "[1] NAMENODE (Tổng công trình sư quản lý Metadata trên RAM + EditLog / FsImage):",
        "    • Sổ danh bạ: \"orders.log (1 GB) = 8 Blocks x 128 MB\"",
        "    • Block 1 (#8888) ──> Lưu tại [DataNode 1 (Rack 1), DataNode 2 (Rack 2), DataNode 4 (Rack 2)]",
        "    • Block 2         ──> Lưu tại [DataNode 2 (Rack 2), DataNode 3 (Rack 1), DataNode 5 (Rack 3)]",
        "    • Nhận Heartbeat & Blockreport định kỳ để giám sát sức khỏe toàn cụm",
        "──────────────────────────────────────────────────────────────────────────────────────",
        "[2] TẦNG DATANODES (Đội thủ kho giữ khối vật lý + Đặt chung Compute & Storage):",
        *dn_row,
        "──────────────────────────────────────────────────────────────────────────────────────",
        "[+] Tự chữa lành (Self-Healing): Nếu DataNode 1 hỏng đĩa (hệ số < 3), NameNode lập tức",
        "    chỉ huy DataNode 2 sao chép bù [Block 1] sang node khác để khôi phục đủ 3 bản sao!",
        "[+] Erasure Coding RS(6,3): 6 khối dữ liệu + 3 khối Parity -> Chỉ tốn 1.5x dung lượng (thay vì 3x)",
    ], inner_width=98, header="KIẾN TRÚC PHÂN TÁN, NHÂN BẢN (x3) & TỰ CHỮA LÀNH TRONG HADOOP HDFS", context="Storage-3.1")
    d3_1 = "\n".join(l.rstrip() for l in b31_hdfs)

    # 12. Trạm 3.2: Network Topology & 3 Levels of Data Locality (Data-local, Rack-local, Off-rack)
    b32_rack1 = make_box([
        "[Switch Tủ 1 (Top-of-Rack Switch 1)]",
        "  │",
        "  ├── Máy chủ A (Node A):",
        "  │   • Đang chạy Task tính toán",
        "  │   • Có sẵn [Block #8888] (Bản sao 1)",
        "  │   ──> (1) DATA-LOCAL (Cùng máy chủ)",
        "  │       Nhanh nhất! Không tốn mạng!",
        "  │",
        "  └── Máy chủ B (Node B):",
        "      • Lưu [Block #8888] (Khi Node A bận)",
        "      ──> (2) RACK-LOCAL (Cùng tủ mạng)",
        "          Chỉ qua Switch nội bộ tủ 1",
    ], inner_width=43, header="TỦ MẠNG 1 (RACK 1)", context="Storage-3.2.rack1")

    b32_rack2 = make_box([
        "[Switch Tủ 2 (Top-of-Rack Switch 2)]",
        "  │",
        "  ├── Máy chủ C (Node C):",
        "  │   • Lưu [Block #8888] (Bản sao 2)",
        "  │",
        "  └── Máy chủ D (Node D):",
        "      • Lưu [Block #8888] (Bản sao 3)",
        "",
        "  ──> (3) OFF-RACK (Khác tủ mạng):",
        "      Task ở Rack 1 phải kéo dữ liệu từ",
        "      Rack 2 băng qua [Core Switch Tổng]",
        "      -> Băng thông thấp nhất, dễ nghẽn!",
    ], inner_width=43, header="TỦ MẠNG 2 (RACK 2)", context="Storage-3.2.rack2")
    d3_2 = "\n".join(join_horizontal([b32_rack1, b32_rack2], [" <═══> "], {0: ["[Core] "]}, context="Storage-3.2"))

    # 13. Trạm 3.3: Streaming Storage — Apache Kafka Append-Only Log, Replay & Stream-to-Batch
    b33_kafka = make_box([
        "[DB Giao dịch OLTP] ──(Sự kiện CDC: Thêm/Sửa Đơn #8888)──> APACHE KAFKA TOPIC: \"orders_events\"",
        "    ┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐",
        "    │ Offset 0         │ Offset 1         │ Offset 2         │ Offset 3 (Mới)   │",
        "    │ [Đơn #8886]      │ [Đơn #8887]      │ [Đơn #8888]      │ [Sửa Đ/C #8888]  │",
        "    └──────────────────┴──────────────────┴──────────────────┴──────────────────┘",
        "                                                                       ▲",
        "    • Ghi tuần tự nối đuôi (Append-only Sequential I/O) + Nén LZ4/Snappy/ZSTD",
        "    • Tiered Storage: Tự động đẩy các đoạn Log cũ xuống Object Storage để lưu dài hạn",
        "    • Cơ chế REPLAY: Cho phép tua lại Offset bất kỳ trong quá khứ để chạy lại dữ liệu",
        "──────────────────────────────────────────────────────────────────────────────────────",
        "[KIẾN TRÚC STREAM-TO-BATCH: 1 Luồng Kafka nuôi đồng thời 2 nhánh Consumer độc lập]",
        "    ├──> [Consumer 1 - Real-time]: Apache Flink / Kafka Streams (Lưu state trên RocksDB)",
        "    └──> [Consumer 2 - Batch/DW ]: Kinesis Firehose / BigQuery Streaming Buffer / Lakehouse",
    ], inner_width=98, header="CƠ CHẾ GHI NHẬT KÝ NỐI ĐUÔI (APPEND-ONLY LOG) & REPLAY CỦA APACHE KAFKA", context="Storage-3.3")
    d3_3 = "\n".join(l.rstrip() for l in b33_kafka)

    # 14. Trạm 3.4: Data Warehouse Architecture & Limitations
    b34_dw = make_box([
        "[1] NGUỒN DỮ LIỆU : [Operational Data (DB Bán hàng OLTP)]  +  [External Data (CRM, ERP)]",
        "                                              │",
        "                                              ▼",
        "[2] TẦNG ETL / ELT: Trích xuất, làm sạch và kiểm định cấu trúc chặt chẽ (Schema-on-Write)",
        "                                              │",
        "                                              ▼",
        "[3] KHO DỮ LIỆU TẬP TRUNG (DATA WAREHOUSE — Snowflake / BigQuery / Redshift / Teradata):",
        "    • Chỉ lưu dữ liệu CÓ CẤU TRÚC (Structured Data) & Đảm bảo giao dịch ACID tuyệt đối",
        "    • Động cơ lưu trữ dạng cột (Columnar) + Micro-partitioning (50–500 MB) + Query Cache",
        "    • Hybrid Object Storage (BigQuery Colossus / S3 Select) & Zero-Copy Cloning (Shallow Copy)",
        "                                              │",
        "                        ┌─────────────────────┴─────────────────────┐",
        "                        ▼                                           ▼",
        "        [4a] Khai thác: [BI Dashboards & Reports]   [4b] 3 Rào cản: Bó tay trước Ảnh/Video,",
        "             (Truy vấn SQL phân tích cực nhanh)          Đắt đỏ ở quy mô PB & Đóng kín định dạng",
    ], inner_width=98, header="KIẾN TRÚC LUỒNG DỮ LIỆU TRONG DATA WAREHOUSE & 3 RÀO CẢN LỊCH SỬ", context="Storage-3.4")
    d3_4 = "\n".join(l.rstrip() for l in b34_dw)

    # 15. Trạm 4.1: Conceptual -> Logical -> Physical Data Models & Kimball 4-Step Process
    b41_c = make_box([
        "Giao tiếp với Business / Chủ nhà",
        "Xác định thực thể & mối quan hệ",
        "",
        "[Khách hàng] ──mua──> [Đơn hàng]",
        "                         │",
        "                        gồm",
        "                         ▼",
        "                     [Sản phẩm]",
        "",
        "• Chưa quan tâm cột, kiểu dữ liệu",
        "• Chưa phụ thuộc phần mềm CSDL",
    ], inner_width=34, header="1. CONCEPTUAL MODEL", context="Storage-4.1.conceptual")
    b41_l = make_box([
        "Bản thiết kế kiến trúc chi tiết",
        "Độc lập với phần mềm CSDL cụ thể",
        "",
        "Bảng: Fact_Sales",
        "• Ma_Don (PK / Degenerate Dim)",
        "• Ma_Khach_Hang (FK -> Dim_Cust)",
        "• Ma_San_Pham (FK -> Dim_Prod)",
        "• So_Luong, So_Tien",
        "",
        "• Rõ tên bảng, cột (attributes)",
        "• Rõ khóa chính (PK) & ngoại (FK)",
    ], inner_width=34, header="2. LOGICAL MODEL", context="Storage-4.1.logical")
    b41_p = make_box([
        "Bản vẽ thi công trên CSDL thực tế",
        "(Snowflake / BigQuery / PostgreSQL)",
        "",
        "CREATE TABLE fact_sales (",
        "  ma_don BIGINT,",
        "  so_luong INT,",
        "  so_tien DECIMAL(18,2)",
        ") PARTITION BY (nam_thang)",
        "  CLUSTER BY (ma_khach_hang);",
        "• Chọn kiểu dữ liệu vật lý chính xác",
        "• Partitioning, Clustering, Indexing",
    ], inner_width=36, header="3. PHYSICAL MODEL", context="Storage-4.1.physical")
    d4_1 = "\n".join(join_horizontal([b41_c, b41_l, b41_p], [" ──> ", " ──> "], context="Storage-4.1"))

    # 16. Trạm 4.2: Bill Inmon vs. Ralph Kimball vs. Dan Linstedt (Data Vault)
    b42_inmon = make_box([
        "[Nguồn dữ liệu toàn Công ty]",
        "             │",
        "             ▼",
        "[Enterprise Data Warehouse (EDW)]",
        "• Chuẩn hóa 3NF, tránh trùng lặp",
        "• Subject-oriented & Integrated",
        "• Nonvolatile & Time-variant",
        "      ┌──────┼──────┐",
        "      ▼      ▼      ▼",
        "  [Sales]  [Mkt] [Purch]",
        "  (Các Data Marts phòng ban)",
    ], inner_width=34, header="1. BILL INMON (Top-Down 3NF)", context="Storage-4.2.inmon")
    b42_kimball = make_box([
        "[Nguồn dữ liệu theo Nghiệp vụ]",
        "(Bán lẻ, Tồn kho, Tài chính...)",
        "             │",
        "             ▼",
        "[Data Warehouse Trung tâm]",
        "• Phi chuẩn hóa (Denormalized)",
        "• Thiết kế thẳng Fact & Dimension",
        "  theo Star Schema (Conformed)",
        "             │",
        "             ▼",
        "[Phục vụ truy vấn BI cực nhanh!]",
    ], inner_width=34, header="2. RALPH KIMBALL (Bottom-Up)", context="Storage-4.2.kimball")
    b42_dv = make_box([
        "[Nạp Insert-only thẳng từ Nguồn]",
        "",
        "  [Satellite 1] ──> [Hub 1 (HashKey)]",
        "   (Thuộc tính)            │",
        "                           ▼",
        "                    [Link (Quan hệ)]",
        "                           ▲",
        "  [Satellite 2] ──> [Hub 2 (HashKey)]",
        "   (Lịch sử Đ/C)     (BusinessKey)",
        "",
        "• Tách cấu trúc khỏi thuộc tính",
    ], inner_width=38, header="3. DAN LINSTEDT (Data Vault)", context="Storage-4.2.datavault")
    d4_2 = "\n".join(join_horizontal([b42_inmon, b42_kimball, b42_dv], ["  ", "  "], context="Storage-4.2"))

    # 17. Trạm 4.3: Dimension vs. Fact Table & Grain (Đơn hàng #8888)
    b43_dim = make_box([
        "Trả lời: Ai? Cái gì? Ở đâu? Khi nào?",
        "Hình dáng: Rộng & Ngắn (Wide & Short, Denorm)",
        "─────────────────────────────────────────────",
        "• Dim_Customer : Nguyễn Văn A (Bình Dương)",
        "• Dim_Store    : Chi nhánh Bình Dương",
        "• Dim_Product  : Nội thất Sofa",
        "• Dim_Date     : Ngày 15/10/2026 (Key: 20261015)",
        "─────────────────────────────────────────────",
        "Vai trò: Lọc (WHERE) & Gom nhóm (GROUP BY)",
    ], inner_width=50, header="NGỮ CẢNH ĐỊNH TÍNH — DIMENSION TABLES", context="Storage-4.3.dim")
    b43_fact = make_box([
        "Trả lời: Bao nhiêu? (Tại 1 Grain nguyên tử)",
        "Hình dáng: Hẹp & Rất dài (Narrow & Long)",
        "───────────────────────────────────────────────",
        "• Ma_Don (DD)   : 8888",
        "• Khóa ngoại FK : Customer_SK, Store_SK, Date_SK",
        "• So_Luong      : 1            (Additive Fact)",
        "• So_Tien       : 5.000.000 VNĐ (Additive Fact)",
        "───────────────────────────────────────────────",
        "Quy tắc: Bất biến (Append-only), cấm lệch Grain",
    ], inner_width=50, header="SỰ KIỆN ĐỊNH LƯỢNG — FACT TABLE (FACT_SALES)", context="Storage-4.3.fact")
    d4_3 = "\n".join(join_horizontal([b43_dim, b43_fact], [" ──(PK/FK)──> "], context="Storage-4.3"))

    # 18. Trạm 4.4: Star Schema vs. Snowflake Schema vs. OBT (One Big Table)
    b44_schemas = make_box([
        "[1] STAR SCHEMA (Lược đồ Hình sao — 1 JOIN)     │ [2] SNOWFLAKE SCHEMA (Hình bông tuyết — Nhiều JOIN)",
        "    Dimension phi chuẩn hóa nối thẳng vào Fact  │     Dimension bị tách thành nhánh Sub-dimension",
        "                                                │",
        "               [Dim_Store]                      │        [Sub-Dim_City]       [Sub-Dim_Brand]",
        "                    │ (1 JOIN)                  │              │ (JOIN 2)           │ (JOIN 2)",
        "                    ▼                           │              ▼                    ▼",
        " [Dim_Cust] ──> [FACT_SALES] <── [Dim_Prod]     │         [Dim_Store]         [Dim_Product]",
        "                    ▲                           │              └──────>[FACT]<──────┘",
        "                    │ (1 JOIN)                  │                     (JOIN 1)",
        "               [Dim_Date]                       │",
        "────────────────────────────────────────────────┴──────────────────────────────────────────────────",
        "[3] OBT — ONE BIG TABLE (Bảng phẳng khổng lồ — 0 JOIN):",
        "    Gộp sẵn mọi cột của các bảng Dimension vào thẳng bảng Fact:",
        "    [OBT_SALES: Ma_Don: 8888 | Ten_Khach | Ten_Cua_Hang | Ten_San_Pham | So_Luong: 1 | So_Tien: 5M]",
        "    ──> Loại bỏ hoàn toàn chi phí JOIN (0 JOIN) — Tối ưu tốc độ quét trên Cloud Columnar Engine!",
    ], inner_width=102, header="BA KIẾN TRÚC BỐ TRÍ BẢNG: STAR SCHEMA VS. SNOWFLAKE SCHEMA VS. OBT", context="Storage-4.4")
    d4_4 = "\n".join(l.rstrip() for l in b44_schemas)

    # 19. Trạm 4.5: Enterprise DW Bus Matrix & Conformed Dimensions
    b45_bus = make_box([
        "Quy trình Nghiệp vụ (Facts) \\ Chiều dùng chung │ Dim_Date │ Dim_Product │ Dim_Customer │ Dim_Store",
        "───────────────────────────────────────────────┼──────────┼─────────────┼──────────────┼──────────",
        "1. Bán lẻ (Retail Sales — có Đơn hàng #8888)   │   [X]    │     [X]     │     [X]      │    [X]",
        "2. Quản lý Tồn kho (Store Inventory)           │   [X]    │     [X]     │     [ ]      │    [X]",
        "3. Mua hàng Nhà cung cấp (Procurement)         │   [X]    │     [X]     │     [ ]      │    [X]",
        "───────────────────────────────────────────────┴──────────┴─────────────┴──────────────┴──────────",
        "• Conformed Dimensions (Chiều đồng nhất): Các bảng Dim_Date, Dim_Product, Dim_Customer, Dim_Store",
        "  được chuẩn hóa thống nhất tại Presentation Area và dùng chung xuyên suốt mọi phòng ban (Drill-across).",
    ], inner_width=104, header="MA TRẬN TUYẾN DOANH NGHIỆP (ENTERPRISE DW BUS MATRIX) & CONFORMED DIMENSIONS", context="Storage-4.5")
    d4_5 = "\n".join(l.rstrip() for l in b45_bus)

    # 20. Trạm 5.1: Data Warehouse (Schema-on-Write & ETL) vs. Data Lake (Schema-on-Read & ELT)
    b51_dw = make_box([
        "[Nguồn dữ liệu Đơn #8888]",
        "            │",
        "            ▼",
        "[TRANSFORM (Kiểm duyệt gắt gao)]",
        "• Phải định nghĩa đúng cột trước",
        "• Nếu JSON thêm 1 trường lạ:",
        "  ──> BÁO LỖI, GÃY PIPELINE!",
        "            │",
        "            ▼",
        "[DATA WAREHOUSE (Đắt đỏ)]",
        "• Chỉ chứa bảng có cấu trúc sạch",
        "• Làm mất dữ liệu thô nguyên bản",
        "• Bó tay trước Ảnh / Video / Audio",
    ], inner_width=48, header="1. DATA WAREHOUSE (Schema-on-Write & ETL)", context="Storage-5.1.dw")
    b51_dl = make_box([
        "[Mọi định dạng Đơn #8888: Bảng, JSON, Ảnh, Video]",
        "            │",
        "            ▼",
        "[LOAD THẲNG (Không kiểm tra lúc ghi)]",
        "• Ném nguyên bản vào Cloud Object Storage",
        "  (S3 / ADLS / GCS) giá siêu rẻ ~$0.02/GB/tháng",
        "• Tách rời Lưu trữ & Tính toán (Ephemeral Compute)",
        "            │",
        "            ▼",
        "[DATA LAKE (Hồ dữ liệu — Schema-on-Read)]",
        "• Khi nào cần ĐỌC ra phân tích / huấn luyện ML",
        "  mới áp Schema vào (ELT: Extract -> Load -> Transform)",
        "• Rủi ro: Thiếu cổng kiểm soát dễ hóa Đầm lầy!",
    ], inner_width=56, header="2. DATA LAKE THẾ HỆ MỚI (Schema-on-Read & ELT)", context="Storage-5.1.dl")
    d5_1 = "\n".join(join_horizontal([b51_dw, b51_dl], [" ──(Tiến hóa)──> "], context="Storage-5.1"))

    # 21. Trạm 5.2a: Quá trình thoái hóa từ Data Lake ban đầu thành Data Swamp sau 6 tháng
    b52_lake = make_box([
        "s3://company-data-lake/ (Ngăn nắp ban đầu)",
        "├── /sales/orders/",
        "│   └── 8888.parquet (Đơn hàng chuẩn)",
        "├── /logs/clickstream/",
        "│   └── click_8888.json (Hành vi bấm chuột)",
        "└── /images/contracts/",
        "    └── contract_8888.jpg (Ảnh biên bản giao)",
        "──────────────────────────────────────────────",
        "[+] Hồ nước trong lành, phân vùng rõ ràng",
        "[+] Kỳ vọng WORM (Write Once, Read Many)",
    ], inner_width=48, header="1. DATA LAKE BAN ĐẦU (NGĂN NẮP)", context="Storage-5.2a.lake")
    b52_swamp = make_box([
        "s3://company-data-lake/ (Hỗn loạn sau 6 tháng)",
        "├── /tmp_test_8888/ (Ai tạo? Dùng làm gì?)",
        "├── /data_final_final_v2/",
        "└── /dump_2026_unnamed/",
        "    ├── 8888_part1.json (Lỗi mã hóa UTF, đổi cột)",
        "    ├── 3.parquet       (Tệp ghi dở dang — Zombie!)",
        "    └── 3_v2.parquet    (Tệp chạy lại — Nhân đôi số!)",
        "────────────────────────────────────────────────────",
        "[x] Đầm lầy ô nhiễm: Dark Data & WORN (Read Never)",
        "[x] Không ai biết tệp nào đúng, không ai dám dùng!",
    ], inner_width=54, header="2. DATA SWAMP SAU 6 THÁNG (HỖN LOẠN)", context="Storage-5.2a.swamp")
    d5_2a = "\n".join(join_horizontal([b52_lake, b52_swamp], [" ──(Thoái hóa)──> "], context="Storage-5.2a"))

    # 22. Trạm 5.2b: Cơ chế sinh Tệp ghi dở (Zombie Writes) & Lỗi định dạng bảng Apache Hive
    b52_zombie = make_box([
        "[Job Spark đang ghi Đơn #8888 vào S3] ──(Đứt mạng ở giây thứ 5!)──> Sinh ra '3.parquet' (Ghi dở 50% — Zombie File)",
        "                  │",
        "       (Hệ thống tự động Retry chạy lại Job)",
        "                  │",
        "                  └─────────────────────(Chạy thành công 100%)────> Sinh ra '3_v2.parquet' (Đủ 100% dữ liệu)",
        "──────────────────────────────────────────────────────────────────────────────────────────────────────────────────",
        "[HẬU QUẢ KHI TRUY VẤN TRÊN ĐỊNH DẠNG BẢNG APACHE HIVE (Directory-level Tracking)]:",
        "• Bảng Hive định nghĩa dữ liệu bằng TOÀN BỘ TỆP NẰM TRONG THƯ MỤC (chứ không có danh sách tệp hợp lệ cụ thể).",
        "• Trên S3 không có lệnh đổi tên thư mục nguyên tử (Rename = COPY + DELETE O(N)), thiếu khóa giao dịch đa tệp.",
        "• Khi chạy SQL, động cơ quét TẤT CẢ tệp trong thư mục: đọc cả '3.parquet' lẫn '3_v2.parquet'",
        "  ──> Doanh thu Đơn #8888 bị TÍNH GẤP ĐÔI (Duplicate Counts / Wrong Answers)!",
    ], inner_width=116, header="CƠ CHẾ SINH TỆP GHI DỞ (ZOMBIE WRITES) & ĐIỂM MÙ CỦA APACHE HIVE TABLE FORMAT", context="Storage-5.2b")
    d5_2b = "\n".join(l.rstrip() for l in b52_zombie)

    # 23. Trạm 5.3: Ba Lỗ hổng Công cụ Cốt tử (The 3 Tooling Gaps)
    b53_gap1 = make_box([
        "• Không có giao dịch ACID:",
        "  Job ETL đang ghi đụng độ",
        "  truy vấn đọc; sập giữa",
        "  chừng để lại tệp rác",
        "• Bất biến (Immutable):",
        "  Không thể Upsert / Delete",
        "  từng dòng (Bó tay GDPR)",
        "• Không chặn Schema Drift",
    ], inner_width=32, header="1. LỖ HỔNG ACID & MUTABILITY", context="Storage-5.3.gap1")
    b53_gap2 = make_box([
        "• Không có danh mục tập trung:",
        "  Không biết bảng nào ở đâu,",
        "  ý nghĩa từng cột là gì",
        "• Thiếu người sở hữu rõ ràng",
        "  (Unclear Ownership/Steward)",
        "• Thiếu phân quyền hạt mịn",
        "• Sinh ra Dark Data & WORN",
        "  (Write Once, Read Never)",
    ], inner_width=34, header="2. THIẾU DATA CATALOG & MGMT", context="Storage-5.3.gap2")
    b53_gap3 = make_box([
        "• Mù phả hệ (No Lineage):",
        "  Không biết số tiền #8888",
        "  sinh từ nguồn nào, qua",
        "  bước ETL nào mà bị sai",
        "• Thiếu 5 trụ cột Giám sát",
        "  (Freshness, Volume, Schema,",
        "  Distribution, Lineage)",
        "• Thiếu Quality Checks tự động",
    ], inner_width=34, header="3. THIẾU LINEAGE & OBSERVABILITY", context="Storage-5.3.gap3")
    d5_3 = "\n".join(join_horizontal([b53_gap1, b53_gap2, b53_gap3], ["  ", "  "], context="Storage-5.3"))

    # 24. Trạm 5.4a: Quy hoạch Phân vùng Cách ly trong Data Lake (Zoning: Raw -> Cleansed -> Curated)
    b54_raw = make_box([
        "(Vùng Dữ liệu Thô — Landing)",
        "• Giữ nguyên bản 100% dữ liệu",
        "  Đơn #8888 lúc mới nạp vào hồ",
        "  (JSON, CSV, Ảnh, Log gốc)",
        "• Phục vụ kiểm toán & chạy lại",
        "  (Replay / Backfill) khi cần",
    ], inner_width=32, header="1. RAW ZONE", context="Storage-5.4a.raw")
    b54_clean = make_box([
        "(Vùng Đã Làm Sạch — Silver)",
        "• Đi qua đường ống ETL / ELT",
        "• Lọc bỏ tệp rác, chuẩn hóa",
        "  kiểu dữ liệu, khử trùng lặp",
        "• Áp đặt Schema & kiểm tra",
        "  chất lượng (Quality Checks)",
    ], inner_width=32, header="2. CLEANSED ZONE", context="Storage-5.4a.clean")
    b54_cur = make_box([
        "(Vùng Tinh Chế — Gold)",
        "• Đi qua đường ống ETL / ELT",
        "• Tổ chức theo mô hình chiều",
        "  (Star Schema / OBT) & tổng",
        "  hợp chỉ số kinh doanh chuẩn",
        "• Sẵn sàng phục vụ BI & AI/ML",
    ], inner_width=32, header="3. CURATED ZONE", context="Storage-5.4a.curated")
    d5_4a = "\n".join(join_horizontal([b54_raw, b54_clean, b54_cur], [" ──(ETL/ELT)──> ", " ──(ETL/ELT)──> "], context="Storage-5.4a"))

    # 25. Trạm 5.4b: Data Contracts + Schema Registry & Single Source of Truth vs 40 Buckets
    b54_governance = make_box([
        "[1] QUẢN LÝ LƯỢC ĐỒ & HỢP ĐỒNG DỮ LIỆU (DATA CONTRACTS + SCHEMA REGISTRY):",
        "    • [x] Không có Schema Mgmt: [Producer] ──(Đổi tên cột tự ý)──> [Kafka] ──> [DIY] ──> GÃY PIPELINE, MẤT DỮ LIỆU!",
        "    • [+] Có Data Contract & Schema Registry (Kiểm tra tương thích BACKWARD / FORWARD / FULL):",
        "          [Producer] ──(Sự kiện #8888)──> [Kafka] ──(Validate)──> [Schema Registry] ──(Compatible)──> [Consumer]",
        "──────────────────────────────────────────────────────────────────────────────────────────────────────────────────",
        "[2] NGUỒN SỰ THẬT DUY NHẤT (SINGLE SOURCE OF TRUTH) VS. CẠM BẪY '40 BẢN SAO BUCKET':",
        "    • [x] Sai lầm (Divergent Truths): Xuất phân vùng bảng Đơn hàng ra 40 Cloud Storage Buckets cho 40 phòng ban",
        "          ──> Ác mộng thu hồi quyền (Revoked Permissions), chạy lại (Reprocess) ở 40 nơi & tốn phí mạng Ingress/Egress!",
        "    • [+] Giải pháp (Single Source of Truth): Duy trì DUY NHẤT 1 bảng nền tảng chuẩn xác tại trung tâm;",
        "          mọi phòng ban & công cụ truy cập chung qua phân quyền hạt mịn thay vì nhân bản tệp vật lý.",
    ], inner_width=120, header="KỶ LUẬT CHỐNG ĐẦM LẦY: DATA CONTRACTS, SCHEMA REGISTRY & SINGLE SOURCE OF TRUTH", context="Storage-5.4b")
    d5_4b = "\n".join(l.rstrip() for l in b54_governance)

    # 26. Trạm 6.1a: Sơ đồ Giao thoa Kiến trúc Data Lakehouse (CIDR 2021)
    b61_dw = make_box([
        "• Dữ liệu có cấu trúc",
        "  (Structured data)",
        "• Tổ chức nghiêm ngặt",
        "  (Highly organized)",
        "• Tối ưu sẵn cho BI",
        "  (Built for BI)",
        "• Truy vấn cực nhanh",
        "  (Fast queries)",
        "• [x] Đắt đỏ ở quy mô lớn",
        "  (Expensive at scale)",
    ], inner_width=28, header="1. DATA WAREHOUSE", context="Storage-6.1a.dw")
    b61_lh = make_box([
        "• Giao dịch ACID (Transactions)",
        "• Cưỡng chế & tiến hóa lược đồ",
        "  (Schema enforcement & evolution)",
        "• Tách rời Lưu trữ & Tính toán",
        "  (Decoupled Compute & Storage)",
        "• Đa dạng Workload trên 1 bản sao",
        "  (BI, SQL, Streaming, Data Science, ML)",
        "• Quản trị & kiểm toán tập trung",
        "  (Unified Data Governance & Audits)",
        "• Truy cập trực tiếp tệp mở (Parquet)",
    ], inner_width=40, header="2. DATA LAKEHOUSE (CIDR 2021)", context="Storage-6.1a.lh")
    b61_dl = make_box([
        "• Dữ liệu thô & phi cấu trúc",
        "  (Raw / Unstructured data)",
        "• Lược đồ linh hoạt lúc đọc",
        "  (Flexible Schema-on-Read)",
        "• Phục vụ Data Science &",
        "  Machine Learning / AI",
        "• Chi phí lưu trữ siêu rẻ",
        "  (~$0.02/GB/tháng trên S3)",
        "• [x] Dễ hóa thành Đầm lầy",
        "  (Data Swamp / Zombie files)",
    ], inner_width=30, header="3. DATA LAKE", context="Storage-6.1a.dl")
    d6_1a = "\n".join(join_horizontal([b61_dw, b61_lh, b61_dl], [" ──(Hợp nhất)──> ", " <──(Hợp nhất)── "], context="Storage-6.1a"))

    # 27. Trạm 6.1b: Kiến trúc 3 Tầng của Hệ thống Data Lakehouse & Phân tách File Format vs Table Format
    b61_arch = make_box([
        "[TẦNG 1: ĐỘNG CƠ TRUY VẤN & TÍNH TOÁN (QUERY ENGINES / EPHEMERAL COMPUTE)]",
        "  ┌──────────────────────────────┐  ┌──────────────────────────────┐  ┌──────────────────────────────┐",
        "  │            Node A            │  │            Node B            │  │            Node C            │",
        "  │  [SQL Exec / Vectorized]     │  │  [SQL Exec / Vectorized]     │  │  [SQL Exec / Vectorized]     │",
        "  │  [(Local SSD / RAM Cache)]   │  │  [(Local SSD / RAM Cache)]   │  │  [(Local SSD / RAM Cache)]   │",
        "  └──────────────────────────────┘  └──────────────────────────────┘  └──────────────────────────────┘",
        "  • Đa động cơ (Apache Spark, Trino, Flink, Presto, DuckDB, BI, PyTorch) bật/tắt theo nhu cầu (Ephemeral)",
        "────────────────────────────────────────────────────▲────────────────────────────────────────────────────",
        "                                                    │ Hỏi Transaction Layer: 'Đọc những tệp hợp lệ nào?'",
        "────────────────────────────────────────────────────┴────────────────────────────────────────────────────",
        "[TẦNG 2: TẦNG GIAO DỊCH & ĐỊNH DẠNG BẢNG (TRANSACTION LAYER — 'Trái tim của Data Lakehouse')]",
        "  ┌──────────────────────────────┐  ┌──────────────────────────────┐  ┌──────────────────────────────┐",
        "  │         Table Format         │  │        Table Services        │  │     Transaction Manager      │",
        "  │  (Delta Lake/Iceberg/Hudi)   │  │ (Compaction/Z-Order/Vacuum)  │  │   (ACID / OCC / MVCC / NBCC) │",
        "  └──────────────────────────────┘  └──────────────────────────────┘  └──────────────────────────────┘",
        "  • Định nghĩa Bảng = Danh sách chuẩn tắc các tệp hợp lệ (Canonical List of Files) thay vì quét thư mục!",
        "────────────────────────────────────────────────────▲────────────────────────────────────────────────────",
        "                                                    │ Quản lý siêu dữ liệu trỏ xuống các tệp vật lý",
        "────────────────────────────────────────────────────┴────────────────────────────────────────────────────",
        "[TẦNG 3: TẦNG LƯU TRỮ ĐÁM MÂY (CLOUD OBJECT STORAGE: AWS S3 / Azure ADLS Gen2 / Google Cloud Storage)]",
        "  • [Data Files (File Format: Parquet / ORC / Avro)]  +  [Metadata / Log / Manifest / Delete Files]",
    ], inner_width=107, header="KIẾN TRÚC 3 TẦNG CỦA HỆ THỐNG DATA LAKEHOUSE (DECOUPLED COMPUTE & STORAGE)", context="Storage-6.1b")
    d6_1b = "\n".join(l.rstrip() for l in b61_arch)

    # 28. Trạm 6.2a: Cơ chế Nhật ký Giao dịch tuần tự _delta_log của Delta Lake
    b62_delta = make_box([
        "s3://bucket/orders_delta/ (Thư mục gốc của bảng Delta Lake)",
        " ├── _delta_log/ (Cuốn sổ cái kế toán ghi nối đuôi tuần tự — Nguồn sự thật duy nhất của bảng)",
        " │    ├── 000000.json  ──> Ghi nhận Version 0:",
        " │    │                    • protocol (minReader/Writer) + metaData (Schema bảng, Partition)",
        " │    │                    • ADD 'part-01.parquet' (Đơn #8888: 15.000.000đ | stats Min/Max)",
        " │    ├── 000001.json  ──> Ghi nhận Version 1 (Sau khi khách nhập mã giảm giá còn 14.000.000đ):",
        " │    │                    • REMOVE 'part-01.parquet' (Đánh dấu Tombstone tệp cũ)",
        " │    │                    • ADD    'part-02.parquet' (Đơn #8888: 14.000.000đ | commitInfo)",
        " │    ├── 000010.checkpoint.parquet  ──> Gộp trạng thái các tệp JSON trước đó thành Parquet để đọc siêu tốc",
        " │    └── _last_checkpoint           ──> Con trỏ chỉ định tệp Checkpoint mới nhất (tránh lệnh S3 LIST)",
        " │",
        " ├── part-01.parquet            (Bản cũ — vẫn giữ trên S3 để phục vụ Time Travel về Version 0)",
        " ├── part-02.parquet            (Bản hiện hành hợp lệ duy nhất ở Version 1)",
        " └── 3_zombie_partial.parquet   (Tệp do 1 job Spark đứt mạng ghi dở dang 50% rớt lại trong thư mục)",
        "──────────────────────────────────────────────────────────────────────────────────────────────────────────────────",
        "[+] KẾT QUẢ KHI TRUY VẤN: Động cơ đọc '_delta_log' thấy ở Version 1 chỉ có 'part-02.parquet' là hợp lệ.",
        "    Tệp rác '3_zombie_partial.parquet' chưa bao giờ được commit vào '_delta_log' nên TÀNG HÌNH 100%!",
    ], inner_width=116, header="CÁCH DELTA LAKE (_delta_log) CỨU ĐƠN HÀNG #8888 KHỎI TỆP GHI DỞ (ZOMBIE WRITES)", context="Storage-6.2a")
    d6_2a = "\n".join(l.rstrip() for l in b62_delta)

    # 29. Trạm 6.2b: Cây Siêu dữ liệu 3 Tầng của Apache Iceberg (Petabyte Scale)
    b62_iceberg = make_box([
        "                               ┌───────────────────────────────────────────────┐",
        "                               │                ICEBERG CATALOG                │",
        "                               │  • Giữ con trỏ nguyên tử (Atomic CAS Pointer) │",
        "                               │    trỏ tới Metadata hiện tại: v2.metadata.json│",
        "                               └───────────────────────┬───────────────────────┘",
        "                                                       │",
        "                                                       ▼",
        "TẦNG 1:                        ┌───────────────────────────────────────────────┐",
        "Metadata File                  │               v2.metadata.json                │",
        "(Cấu trúc & Snapshots)         │  • Lưu Table UUID, Schema (Column IDs)        │",
        "                               │  • Lưu Partition Specs & Sort Orders          │",
        "                               │  • Danh sách Snapshots: [s0, s1 (current)]    │",
        "                               └───────────────────────┬───────────────────────┘",
        "                                                       │ Trỏ tới Snapshot hiện tại (s1)",
        "                                                       ▼",
        "TẦNG 2:                        ┌───────────────────────────────────────────────┐",
        "Manifest List                  │          snap-s1-manifest-list.avro           │",
        "(Mục lục của 1 Snapshot)       │  • Một dòng cho mỗi Manifest File             │",
        "                               │  • Lưu khoảng Min/Max từng phân vùng giúp     │",
        "                               │    cắt tỉa cả cụm Manifest ngay lập tức       │",
        "                               └───────────┬───────────────────────┬───────────┘",
        "                                           │                       │",
        "                            ┌──────────────┘                       └──────────────┐",
        "                            ▼                                                     ▼",
        "TẦNG 3:       ┌───────────────────────────────────────┐             ┌───────────────────────────────────────┐",
        "Manifest      │           manifest-01.avro            │             │           manifest-02.avro            │",
        "Files         │  • Danh sách Data/Delete Files        │             │  • Danh sách Data/Delete Files        │",
        "(Thống kê tệp)│  • Lưu Min/Max/Null Count từng cột    │             │    (Chứa tệp của Đơn hàng #8888)      │",
        "              └───────────────────┬───────────────────┘             └───────────────────┬───────────────────┘",
        "                                  │                                                     │",
        "                                  ▼                                                     ▼",
        "DATA LAYER:    [0001.parquet] + [0002.parquet]                       [0003_8888.parquet] + [pos_delete.parquet]",
    ], inner_width=112, header="CÂY SIÊU DỮ LIỆU 3 TẦNG CỦA APACHE ICEBERG (CATALOG -> METADATA -> MANIFEST LIST -> MANIFEST)", context="Storage-6.2b")
    d6_2b = "\n".join(l.rstrip() for l in b62_iceberg)

    # 30. Trạm 6.2c: Kiến trúc Apache Hudi — Timeline, File Groups (Base + Log) & Indexing Subsystem
    b62_hudi_tl = make_box([
        "[1. HUDI TIMELINE (.hoodie/)]:",
        "• Ghi nhận tuần tự mọi Instant",
        "  theo máy trạng thái 3 bước:",
        "  [REQUESTED] ──> [INFLIGHT]",
        "              ──> [COMPLETED]",
        "• Các hành động chính:",
        "  - commit (Bảng COW)",
        "  - deltacommit (Bảng MOR)",
        "  - compaction / clustering",
        "  - clean / rollback / savepoint",
    ], inner_width=34, header="1. HUDI TIMELINE (STATE MACHINE)", context="Storage-6.2c.tl")
    b62_hudi_idx = make_box([
        "[2. INDEXING SUBSYSTEM]:",
        "• Lưu trong bảng Metadata nội bộ",
        "  (.hoodie/metadata dạng HFile)",
        "• Ánh xạ siêu tốc khóa bản ghi:",
        "  RecordKey (#8888) ──> FileGroup ID",
        "• Các loại Index thực chiến:",
        "  - Record-Level Index (RLI - O(1))",
        "  - Bloom Index (Mặc định)",
        "  - Bucket Index (Băm trực tiếp)",
        "  - Simple / HBase Index",
    ], inner_width=36, header="2. HỆ THỐNG CHỈ MỤC (INDEXING)", context="Storage-6.2c.idx")
    b62_hudi_fg = make_box([
        "[3. FILE GROUPS & FILE SLICES (Hybrid)]:",
        "• Mỗi File Group có FileId cố định,",
        "  chia thành các File Slice theo mốc giờ:",
        "  ┌────────────────────────────────────┐",
        "  │ Base File (Parquet - Lưu theo Cột) │",
        "  │  • Chứa Đơn #8888 gốc (15.000.000đ)│",
        "  ├────────────────────────────────────┤",
        "  │ + Log Files (.log.avro - Theo Dòng)│",
        "  │  • Bắt nhanh CDC: #8888 -> 14 triệu│",
        "  └────────────────────────────────────┘",
    ], inner_width=42, header="3. FILE GROUPS (BASE + LOG FILES)", context="Storage-6.2c.fg")
    d6_2c = "\n".join(join_horizontal([b62_hudi_tl, b62_hudi_idx, b62_hudi_fg], ["  ", "  "], context="Storage-6.2c"))

    # 31. Trạm 6.2d: Cơ chế Đọc Đa Định dạng (Delta UniForm / Apache XTable / Pluggable Table Format)
    b62_uniform = make_box([
        "                      ┌───────────────────────────────────────────────────────────┐",
        "                      │   BỘ DỊCH SIÊU DỮ LIỆU ĐA CHIỀU (UNIFORM / APACHE XTABLE) │",
        "                      │   • Chuyển đổi qua lại con trỏ & thống kê ở tầng Metadata │",
        "                      └───────────┬─────────────────┬─────────────────┬───────────┘",
        "                                  │                 │                 │",
        "                                  ▼                 ▼                 ▼",
        "                        [ _delta_log JSON ]  [ Iceberg Tree ]  [ Hudi Timeline ]",
        "                        (Spark / Databricks) (Trino/Snowflake) (Flink / Presto)",
        "                                  │                 │                 │",
        "                                  └─────────────────┼─────────────────┘",
        "                                                    ▼",
        "                      ┌───────────────────────────────────────────────────────────┐",
        "                      │     CÙNG 1 BỘ TỆP VẬT LÝ DUY NHẤT: orders_8888.parquet    │",
        "                      │  [+] Không nhân bản dữ liệu Parquet, không tốn thêm phí S3│",
        "                      └───────────────────────────────────────────────────────────┘",
    ], inner_width=104, header="KỶ NGUYÊN HỢP NHẤT ĐA ĐỊNH DẠNG: DELTA UNIFORM, APACHE XTABLE & PLUGGABLE FORMAT", context="Storage-6.2d")
    d6_2d = "\n".join(l.rstrip() for l in b62_uniform)

    # 32. Trạm 6.3: Ba Cơ chế Kiểm soát Đồng thời trên Data Lakehouse (MVCC, OCC, NBCC)
    b63_mvcc = make_box([
        "• Cô lập Snapshot giữa Đọc & Ghi:",
        "  - Người Đọc (Giám đốc) đọc bản",
        "    chụp [Snapshot v1] bất biến.",
        "  - Người Ghi / Compaction âm thầm",
        "    tạo tệp mới cho [Snapshot v2].",
        "• Kết quả:",
        "  Đọc và Ghi KHÔNG BAO GIỜ KHÓA",
        "  NHAU (Non-blocking Reads)!",
    ], inner_width=36, header="1. MVCC (ĐA PHIÊN BẢN SNAPSHOT)", context="Storage-6.3.mvcc")
    b63_occ = make_box([
        "• Giữa nhiều Người Ghi (Writers):",
        "  - Writer 1 & Writer 2 cùng xuất",
        "    phát từ [Snapshot v1].",
        "  - Writer 1 xong trước ──> [v2].",
        "  - Writer 2 xong sau ──> Kiểm tra",
        "    xung đột cấp độ tệp (File-level):",
        "    + Khác tệp: Cho commit lên [v3]",
        "    + Đụng cùng tệp: Retry / Báo lỗi",
    ], inner_width=38, header="2. OCC (KIỂM SOÁT LẠC QUAN)", context="Storage-6.3.occ")
    b63_nbcc = make_box([
        "• Dành cho Streaming tốc độ cao",
        "  (Apache Hudi MOR Log Files):",
        "  - Cho phép nhiều luồng ghi (multi",
        "    writers) và dịch vụ bảng cùng",
        "    ghi nối đuôi vào các Log files.",
        "  - Sắp xếp thứ tự chuẩn xác theo",
        "    Instant Time mà KHÔNG bắt các",
        "    luồng ghi phải hủy và chạy lại!",
    ], inner_width=38, header="3. NBCC (KHÔNG KHÓA STREAMING)", context="Storage-6.3.nbcc")
    d6_3 = "\n".join(join_horizontal([b63_mvcc, b63_occ, b63_nbcc], ["  ", "  "], context="Storage-6.3"))

    # 33. Trạm 6.4: Chiến lược Ghi & Cập nhật — Copy-on-Write (COW) vs. Merge-on-Read (MOR)
    b64_cow_mor = make_box([
        "[CHIẾN LƯỢC 1: COPY-ON-WRITE (COW — Chép lại toàn bộ tệp Parquet khi ghi / sửa / xóa)]",
        "  ┌──────────────────────────────────────┐                          ┌──────────────────────────────────────┐",
        "  │ file_01.parquet (100 MB - 100k dòng) │   Đọc 99.999 đơn cũ      │ file_02.parquet (100 MB - Tệp mới)   │",
        "  │ • 99.999 đơn hàng khác               │ ── + Đơn #8888 (14M) ──> │ • 99.999 đơn hàng khác               │",
        "  │ • Đơn #8888: 15.000.000đ             │   Viết lại nguyên 100 MB │ • Đơn #8888: 14.000.000đ             │",
        "  └──────────────────────────────────────┘                          └──────────────────┬───────────────────┘",
        "   (Đánh dấu Tombstone trong Metadata)                                                 ▲",
        "                                                                     [+] Lúc ĐỌC: Quét thẳng file_02 siêu tốc!",
        "══════════════════════════════════════════════════════════════════════════════════════════════════════════════════",
        "[CHIẾN LƯỢC 2: MERGE-ON-READ (MOR — Ghi nối đuôi vào Log / Delete File, Trộn lại khi đọc)]",
        "  ┌──────────────────────────────────────┐                          ┌──────────────────────────────────────┐",
        "  │ Base File: file_01.parquet (100 MB)  │   KHÔNG viết lại 100 MB! │ Delta Log / Delete File (Chỉ ~1 KB)  │",
        "  │ • Giữ nguyên bất biến trên S3,       │ ── Chỉ ghi 1 dòng sửa ──>│ • Hudi: log_01.avro (#8888 -> 14M)   │",
        "  │   không đụng chạm tới 99.999 đơn cũ  │   bằng deltacommit       │ • Iceberg/Delta: Pos/Eq Delete Vector│",
        "  └──────────────────┬───────────────────┘                          └──────────────────┬───────────────────┘",
        "                     │                                                                 │",
        "                     └──────────────> [LÚC ĐỌC (Snapshot Query)]: Engine trộn (Merge) <┘",
        "                                      Base File (Cột) + Log/Delete File để trả về 14M!",
    ], inner_width=116, header="ĐỐI CHIẾU CƠ HỌC COPY-ON-WRITE (COW) VS. MERGE-ON-READ (MOR) KHI SỬA ĐƠN HÀNG #8888", context="Storage-6.4")
    d6_4 = "\n".join(l.rstrip() for l in b64_cow_mor)

    # 34. Trạm 6.5a: Partitioning Truyền thống vs. Hidden Partitioning & Partition Evolution (Apache Iceberg)
    b65_part_old = make_box([
        "• Phải tạo thêm cột vật lý dẫn xuất",
        "  'nam_thang' = '2026-10' từ cột gốc",
        "  'ngay_gio_mua'.",
        "• Nếu người dùng viết câu lệnh SQL:",
        "  WHERE ngay_gio_mua >= '2026-10-15'",
        "  mà QUÊN thêm AND nam_thang='2026-10'",
        "  ──> Quét toàn bộ bảng (Full Scan)!",
        "• Muốn đổi từ chia theo Tháng sang",
        "  chia theo Ngày: Phải viết lại 100%",
        "  tệp Parquet lịch sử!",
    ], inner_width=40, header="1. PARTITIONING TRUYỀN THỐNG (HIVE)", context="Storage-6.5a.old")
    b65_part_new = make_box([
        "• Hidden Partitioning: Iceberg lưu hàm biến đổi",
        "  month(ngay_gio_mua) hoặc bucket(16, id) ngay",
        "  trong Metadata (Partition Spec).",
        "  ──> Người dùng chỉ cần lọc trên cột 'ngay_gio_mua'",
        "      tự nhiên, Engine tự động cắt tỉa đúng phân vùng!",
        "• Partition Evolution (Tiến hóa phân vùng tại chỗ):",
        "  ──> Đổi từ month(ts) [Spec 0] sang day(ts) [Spec 1]",
        "      chỉ bằng 1 lệnh cập nhật Metadata; dữ liệu cũ",
        "      giữ Spec 0, dữ liệu mới dùng Spec 1, KHÔNG CẦN",
        "      VIẾT LẠI bất kỳ tệp Parquet lịch sử nào!",
    ], inner_width=56, header="2. HIDDEN PARTITIONING & EVOLUTION (ICEBERG)", context="Storage-6.5a.new")
    d6_5a = "\n".join(join_horizontal([b65_part_old, b65_part_new], [" ──(Đột phá)──> "], context="Storage-6.5a"))

    # 35. Trạm 6.5b: Z-Ordering / Liquid Clustering — Gom cụm Dữ liệu Đa chiều
    b65_zorder = make_box([
        "[1] TRƯỚC KHI CHẠY Z-ORDER / LIQUID CLUSTERING (Dữ liệu rải ngẫu nhiên ở mọi tệp Parquet):",
        "    • File 1 (512 MB): Customer_ID [min: 1, max: 9999]     |  Product_ID [min: 10,  max: 500]",
        "    • File 2 (512 MB): Customer_ID [min: 2, max: 9998]     |  Product_ID [min: 12,  max: 499]",
        "    ──> [x] Truy vấn Đơn #8888 (Customer 501, Product 25): Phải đọc CẢ 2 FILE vì khoảng Min/Max chồng lấn!",
        "──────────────────────────────────────────────────────────────────────────────────────────────────────────────────",
        "[2] SAU KHI CHẠY Z-ORDER BY (Customer_ID, Product_ID) HOẶC LIQUID CLUSTERING (CLUSTER BY):",
        "    • File 1 (512 MB): Customer_ID [min: 1,    max: 1000]  |  Product_ID [min: 10,  max: 100]  <── Chứa Đơn #8888!",
        "    • File 2 (512 MB): Customer_ID [min: 1001, max: 9999]  |  Product_ID [min: 101, max: 500]",
        "    ──> [+] Truy vấn Đơn #8888 (Customer 501, Product 25): Chỉ đọc FILE 1, bỏ qua ngay FILE 2 (Data Skipping tối đa)!",
    ], inner_width=118, header="GOM CỤM ĐA CHIỀU Z-ORDERING & LIQUID CLUSTERING (SPACE-FILLING CURVES: Z-CURVE / HILBERT CURVE)", context="Storage-6.5b")
    d6_5b = "\n".join(l.rstrip() for l in b65_zorder)

    # 36. Trạm 6.5c: Bộ 3 Dịch vụ Bảo trì Vật lý: Compaction (OPTIMIZE), Deletion Vectors & Vacuum
    b65_compact = make_box([
        "• Nỗi đau: Streaming xả 1 phút/file",
        "  ──> 43.200 tệp nhỏ 500 KB/tháng",
        "  gây nghẽn HTTP GET trên S3.",
        "• Giải pháp (OPTIMIZE / Bin-pack):",
        "  Gộp hàng nghìn tệp nhỏ thành",
        "  tệp Parquet chuẩn 128 MB – 1 GB.",
    ], inner_width=36, header="1. COMPACTION (OPTIMIZE)", context="Storage-6.5c.compact")
    b65_dv = make_box([
        "• Bản chất: Khi DELETE/UPDATE #8888,",
        "  không viết lại ngay tệp 512 MB",
        "  mà ghi 1 mảng Roaring Bitmap siêu",
        "  nhỏ đánh dấu: 'Dòng 4.512 đã xóa'.",
        "• Lợi ích: Xóa/Sửa tức thì như MOR;",
        "  hợp nhất vật lý sau khi OPTIMIZE.",
    ], inner_width=38, header="2. DELETION VECTORS (BITMAP)", context="Storage-6.5c.dv")
    b65_vacuum = make_box([
        "• Nỗi đau: Giữ các tệp Parquet cũ",
        "  cho Time Travel làm phình S3.",
        "• Giải pháp (VACUUM RETAIN 168 HRS):",
        "  Xóa vĩnh viễn các tệp đã quá hạn",
        "  lưu giữ (7 ngày) & tệp mồ côi,",
        "  thu hồi dung lượng S3 & chuẩn GDPR.",
    ], inner_width=38, header="3. VACUUM / EXPIRE SNAPSHOTS", context="Storage-6.5c.vacuum")
    d6_5c = "\n".join(join_horizontal([b65_compact, b65_dv, b65_vacuum], ["  ", "  "], context="Storage-6.5c"))

    # 37. Trạm 1.2b: Giải phẫu Cơ học Bộ nhớ RAM (Address Space, DRAM Volatility & In-Memory Cache)
    b12b_addr = make_box([
        "• Ánh xạ thẳng vào không gian",
        "  địa chỉ của CPU (Address Space)",
        "• Chứa cả Mã lệnh (Code) lẫn",
        "  Dữ liệu (Data) đang xử lý",
        "  (Kiến trúc Von Neumann/Harvard)",
        "• Băng thông: ~100 GB/s (DDR5)",
        "  Độ trễ: ~100 ns (Nhanh 1.000x SSD)",
    ], inner_width=38, header="1. KHÔNG GIAN ĐỊA CHỈ CPU & RAM", context="Storage-1.2b.addr")
    b12b_dram = make_box([
        "• Lưu bit trong tụ điện DRAM siêu",
        "  nhỏ, cần nạp làm tươi liên tục",
        "• Tính khả biến (Volatile):",
        "  [Mất điện < 1 giây]",
        "      └──> Bốc hơi 100% dữ liệu!",
        "• Bắt buộc dùng ECC RAM trên máy",
        "  chủ để chống lật bit (Bit rot)",
    ], inner_width=38, header="2. TỤ ĐIỆN DRAM & TÍNH KHẢ BIẾN", context="Storage-1.2b.dram")
    b12b_cache = make_box([
        "• Dùng làm tầng Đệm Nóng (Cache):",
        "  - Redis (Cấu trúc + RDB/AOF)",
        "  - Memcached (Key-Value thuần)",
        "  - Hazelcast (In-Memory Grid)",
        "• Đơn #8888 bắt buộc phải đồng thời",
        "  ghi xuống đĩa bền vững (SSD/S3)",
        "  để không mất đơn khi sập nguồn!",
    ], inner_width=38, header="3. ĐỘNG CƠ IN-MEMORY & BỀN VỮNG", context="Storage-1.2b.cache")
    d1_2b = "\n".join(join_horizontal([b12b_addr, b12b_dram, b12b_cache], ["  ", "  "], context="Storage-1.2b"))

    # 38. Trạm 1.3b: Hai Bí mật Nhà nghề của Cloud Object Storage từ 3 Tài sản Đĩa
    b13b_sec1 = make_box([
        "• 1 ổ đĩa HDD đơn lẻ chỉ đọc được: ~200 MB/s",
        "• Cloud Object Storage băm nhỏ & rải tệp lớn",
        "  ra HÀNG NGHÌN Ổ ĐĨA trên khắp Data Center:",
        "    [Ổ đĩa 1: 200 MB/s] ──┐",
        "    [Ổ đĩa 2: 200 MB/s] ──┼──> Đọc song song",
        "    [... 1.000 ổ đĩa ] ──┘    đạt ~3 GB/s!",
        "• Điểm nghẽn chuyển từ Đĩa sang Mạng & CPU!",
    ], inner_width=52, header="BÍ MẬT 1: ĐỌC SONG SONG HÀNG NGHÌN Ổ ĐĨA (~3 GB/s)", context="Storage-1.3b.sec1")
    b13b_sec2 = make_box([
        "• Cùng chạy trên 1 cụm ổ đĩa vật lý (10 TB,",
        "  100 IOPS, 200 MB/s), nhưng tách gói bán:",
        "  - Gói Standard (~$0.02/GB): Mua trọn IOPS",
        "    & Băng thông để đọc tức thì (~100 ms).",
        "  - Gói Archival (~$0.004/GB — rẻ bằng 1/17):",
        "    Chỉ mua phần Dung lượng (Capacity) dư thừa,",
        "    chờ ~12 giờ lúc đĩa rảnh IOPS mới lấy ra!",
    ], inner_width=52, header="BÍ MẬT 2: TẠI SAO ARCHIVAL CHUNG ĐĨA MÀ RẺ 1/17?", context="Storage-1.3b.sec2")
    d1_3b = "\n".join(join_horizontal([b13b_sec1, b13b_sec2], ["    "], context="Storage-1.3b"))

    # 39. Trạm 2.1b: Triết lý "Less is More" của Cloud Object Storage & Vòng đời Lưu trữ
    b21b_imm = make_box([
        "• Không sửa tại chỗ, không ghi nối đuôi",
        "  ──> Ghi 1 lần thành luồng byte BẤT BIẾN",
        "• Lợi ích vàng: Bỏ hoàn toàn khóa tệp (Lock",
        "  free) ──> Đọc/ghi luồng song song ~3 GB/s",
        "  & Tách rời Compute khỏi Storage!",
        "• Hỗ trợ HTTP Range Request đọc riêng phần",
        "  Footer của tệp Parquet mà không tải cả tệp",
    ], inner_width=46, header="1. BẤT BIẾN (IMMUTABILITY = LOCK-FREE)", context="Storage-2.1b.imm")
    b21b_ver = make_box([
        "• Strong Read-After-Write Consistency:",
        "  Đọc ngay sau khi PUT luôn thấy bản mới nhất",
        "• Object Versioning (Key + Version ID):",
        "  Lưu bản sao nguyên khối (Brute-force full",
        "  copy) ──> Ghi đè tệp 10 GB x 100 lần = 1 TB!",
        "• Bắt buộc gắn Lifecycle Policy:",
        "  Standard ($0.02) ──> IA ──> Glacier ($0.001)",
    ], inner_width=50, header="2. CONSISTENCY, VERSIONING & LIFECYCLE", context="Storage-2.1b.ver")
    d2_1b = "\n".join(join_horizontal([b21b_imm, b21b_ver], [" ──> "], context="Storage-2.1b"))

    # 40. Trạm 2.4b: Ba Đòn bẩy Phần cứng của Nén Dữ liệu (Hardware Leverage)
    b24b_disk = make_box([
        "• Bảng gốc chưa nén: 100 GB",
        "• Nén cột Parquet (4:1 đến 10:1):",
        "  ──> Chỉ còn 10 GB – 25 GB",
        "• Giảm trực tiếp 75% – 90%",
        "  hóa đơn lưu trữ hàng tháng!",
    ], inner_width=36, header="1. GIẢM DUNG LƯỢNG LƯU TRỮ", context="Storage-2.4b.disk")
    b24b_scan = make_box([
        "• Đĩa HDD đọc vật lý: 200 MB/s",
        "  (Đọc 100 GB thô mất 500 giây)",
        "• Nén 4:1 (25 GB) ──> Đọc 125 giây",
        "  + CPU giải nén trên RAM (100 GB/s)",
        "• Băng thông quét logic tăng vọt:",
        "  200 MB/s ──> 800 MB/s (tới 2 GB/s)!",
    ], inner_width=38, header="2. KHUẾCH ĐẠI TỐC ĐỘ QUÉT ĐĨA", context="Storage-2.4b.scan")
    b24b_net = make_box([
        "• Đường truyền mạng giữa máy ảo",
        "  EC2 và S3 vật lý: 10 Gbps",
        "• Khi truyền dữ liệu nén tỷ lệ 10:1:",
        "  ──> Băng thông truyền tải dữ liệu",
        "      hiệu dụng đạt 100 Gbps!",
        "• Đổi vài chu kỳ CPU lấy 10x I/O!",
    ], inner_width=38, header="3. KHUẾCH ĐẠI BĂNG THÔNG MẠNG", context="Storage-2.4b.net")
    d2_4b = "\n".join(join_horizontal([b24b_disk, b24b_scan, b24b_net], ["  ", "  "], context="Storage-2.4b"))

    # 41. Trạm 3.2b: Giải phẫu 3 Động cơ Cache Dưới 1 Mili-giây (Redis vs. Memcached vs. RocksDB)
    b32b_redis = make_box([
        "• Mô hình: Client-Server trên RAM",
        "  (~100 ns access + mạng LAN)",
        "• Đa cấu trúc: String, Hash, List,",
        "  Set, Sorted Set, Bitmap + TTL",
        "• Bền vững: Có (Chụp RDB Snapshot",
        "  & ghi nhật ký AOF mỗi ~2 giây)",
        "• Vai trò: Cache phân tán dùng chung",
    ], inner_width=38, header="1. REDIS (IN-MEMORY STRUCTURES)", context="Storage-3.2b.redis")
    b32b_mem = make_box([
        "• Mô hình: Client-Server đa luồng",
        "  siêu nhẹ (~10 µs gói tin LAN)",
        "• Cấu trúc: Key-Value đơn giản",
        "  (Chỉ lưu String / Integer)",
        "• Bền vững: KHÔNG (Thuần RAM,",
        "  mất điện là mất sạch 100%)",
        "• Vai trò: Đệm kết quả DB & Web API",
    ], inner_width=38, header="2. MEMCACHED (PURE RAM CACHE)", context="Storage-3.2b.mem")
    b32b_rocks = make_box([
        "• Mô hình: Nhúng trực tiếp (Embedded",
        "  LSM-Tree) vào tiến trình tính toán",
        "• Luồng ghi/đọc (~100 µs NVMe SSD):",
        "  [WAL + RAM MemTable] ──> [SSTables]",
        "• Bền vững: Có (Cây LSM trên SSD)",
        "• Vai trò: Lưu trạng thái (State",
        "  Backend) cho Apache Flink & Kafka",
    ], inner_width=38, header="3. ROCKSDB (EMBEDDED LSM-TREE)", context="Storage-3.2b.rocks")
    d3_2b = "\n".join(join_horizontal([b32b_redis, b32b_mem, b32b_rocks], ["  ", "  "], context="Storage-3.2b"))

    # 42. Trạm 3.5: Ba Rào cản Lịch sử của Data Warehouse Thúc đẩy Tiến hóa lên Data Lake & Lakehouse
    b35_unstruct = make_box([
        "• Đơn #8888 phát sinh thêm:",
        "  - Ảnh kiện hàng (contract.jpg)",
        "  - Video camera kho bãi",
        "  - Ghi âm tổng đài CSKH",
        "• [x] Data Warehouse chỉ hiểu bảng",
        "  có cấu trúc / JSON, bó tay trước",
        "  dữ liệu phi cấu trúc cho AI/DL!",
    ], inner_width=38, header="1. BÓ TAY TRƯỚC UNSTRUCTURED DATA", context="Storage-3.5.unstruct")
    b35_cost = make_box([
        "• Sau 5 năm, lịch sử đơn hàng &",
        "  log hành vi phình lên Petabyte",
        "  (Volume, Velocity, Variety).",
        "• [x] Lưu trữ & mở rộng trên phần",
        "  cứng MPP / kho chuyên dụng đắt",
        "  gấp hàng chục lần so với lưu tệp",
        "  thô trên Cloud Object Storage!",
    ], inner_width=38, header="2. ĐẮT ĐỎ Ở QUY MÔ PETABYTE", context="Storage-3.5.cost")
    b35_lock = make_box([
        "• Định dạng lưu trữ bên dưới bị",
        "  đóng kín độc quyền (Proprietary).",
        "• [x] Đội Data Science muốn dùng",
        "  Python / Spark / PyTorch đọc",
        "  trực tiếp tệp gốc để train ML",
        "  phải tốn phí tuần tự hóa lại",
        "  (Reserializing / Export ETL)!",
    ], inner_width=38, header="3. ĐÓNG KÍN & VENDOR LOCK-IN", context="Storage-3.5.lock")
    d3_5 = "\n".join(join_horizontal([b35_unstruct, b35_cost, b35_lock], ["  ", "  "], context="Storage-3.5"))

    # 43. Trạm 4.3b: Ma trận 3 Mức Cộng gộp Số đo (Additivity) & 3 Kiểu Bảng Fact của Ralph Kimball
    b43b_matrix = make_box([
        "[PHẦN A — 3 MỨC ĐỘ CỘNG GỘP SỐ ĐO (ADDITIVITY TRONG BẢNG FACT)]:",
        "  ┌───────────────────────────────────┬───────────────────────────────────────┬──────────────────────────────────────┐",
        "  │ 1. ADDITIVE (Cộng mọi chiều)      │ 2. SEMI-ADDITIVE (Bán cộng)           │ 3. NON-ADDITIVE (Không cộng được)    │",
        "  │ • Cộng (SUM) hợp lệ qua TẤT CẢ    │ • Cộng được theo Cửa hàng / Sản phẩm  │ • Tuyệt đối CẤM dùng hàm SUM()!      │",
        "  │   các chiều (Thời gian, Khu vực)  │   nhưng CẤM CỘNG THEO THỜI GIAN!      │ • Phải cộng Tử số & Mẫu số trước     │",
        "  │ • VD: So_Luong (1), So_Tien (5M)  │ • VD: Tồn kho cuối ngày, Số dư TK     │ • VD: Đơn giá, Tỷ lệ lãi gộp (%)     │",
        "  └───────────────────────────────────┴───────────────────────────────────────┴──────────────────────────────────────┘",
        "──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────",
        "[PHẦN B — 3 KIỂU BẢNG FACT CHUẨN THEO QUY TRÌNH NGHIỆP VỤ]:",
        "  • (1) Transaction Fact Table          : 1 dòng nguyên tử cho mỗi giao dịch phát sinh (VD: Đơn hàng #8888 lúc mua).",
        "  • (2) Periodic Snapshot Fact Table    : Chụp trạng thái định kỳ theo mốc cố định (VD: Tồn kho cuối mỗi ngày/tháng).",
        "  • (3) Accumulating Snapshot Fact Table: 1 dòng theo dõi trọn vòng đời đơn hàng, cập nhật dần các cột mốc thời gian:",
        "        [Ngay_Dat_Hang] ──> [Ngay_Thanh_Toan] ──> [Ngay_Xuat_Kho] ──> [Ngay_Giao_Thanh_Cong].",
    ], inner_width=118, header="PHÂN LOẠI SỐ ĐO (ADDITIVITY) & 3 KIỂU BẢNG FACT CHUẨN CỦA RALPH KIMBALL", context="Storage-4.3b")
    d4_3b = "\n".join(l.rstrip() for l in b43b_matrix)

    # 44. Trạm 4.5a: Đối chiếu Trực quan 3 Chiến lược SCD (Type 1 vs. Type 2 vs. Type 3) khi Khách #8888 Chuyển Tỉnh
    b45a_scd1 = make_box([
        "• Cơ chế: Ghi đè trực tiếp tỉnh",
        "  mới lên dòng cũ (SK = 101):",
        "  [Bình Dương] ──> [TP.HCM]",
        "• Hệ quả với Đơn #8888 (5M):",
        "  [x] MẤT DẤU LỊCH SỬ! Doanh thu",
        "  tháng 10 ở Bình Dương bị cộng",
        "  nhầm sang cho TP.HCM!",
    ], inner_width=36, header="1. SCD TYPE 1 (OVERWRITE)", context="Storage-4.5a.scd1")
    b45a_scd2 = make_box([
        "• Cơ chế: Giữ dòng cũ & Thêm dòng",
        "  mới với Surrogate Key mới:",
        "  - SK 101: Bình Dương (is_current=0)",
        "  - SK 205: TP.HCM     (is_current=1)",
        "• Hệ quả với Đơn #8888 (5M):",
        "  [+] CHUẨN VÀNG! Đơn #8888 nối SK 101",
        "  (Bình Dương); Đơn #9999 nối SK 205!",
    ], inner_width=40, header="2. SCD TYPE 2 (ROW VERSIONING)", context="Storage-4.5a.scd2")
    b45a_scd3 = make_box([
        "• Cơ chế: Giữ 1 dòng (SK = 101),",
        "  mở thêm cột mới trên cùng dòng:",
        "  - Tinh_Hien_Tai : 'TP.HCM'",
        "  - Tinh_Truoc_Do : 'Bình Dương'",
        "• Hệ quả với Đơn #8888 (5M):",
        "  [!] So sánh nhanh cũ/mới, nhưng",
        "  chỉ nhớ được 1 lần đổi gần nhất!",
    ], inner_width=38, header="3. SCD TYPE 3 (COLUMN HISTORY)", context="Storage-4.5a.scd3")
    d4_5a = "\n".join(join_horizontal([b45a_scd1, b45a_scd2, b45a_scd3], ["  ", "  "], context="Storage-4.5a"))

    # 45. Trạm 5.2c: Sáu Khiếm khuyết Kiến trúc của Bảng Hive Thế hệ cũ & Giới hạn Đơn tệp của Object Storage
    b52c_hive = make_box([
        "  ┌────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────┐",
        "  │ [1] QUẢN LÝ CẤP THƯ MỤC (DIRECTORY-LEVEL TRACKING)     │ [4] LIỆT KÊ TỆP ĐẮT ĐỎ & NGHẼN TIỀN TỐ (S3 LIST)        │",
        "  │ • Định nghĩa bảng bằng toàn bộ tệp trong thư mục       │ • Phải gọi S3 LIST tuần tự qua hàng nghìn thư mục;      │",
        "  │   ──> Đọc nhầm cả tệp ghi dở (3.parquet) làm nhân đôi! │   dễ bị bóp băng thông (Throttling) khi quá nhiều file. │",
        "  ├────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┤",
        "  │ [2] ĐỔI TÊN (RENAME) KHÔNG NGUYÊN TỬ TRÊN S3           │ [5] PHỤ THUỘC CỨNG CỘT PHÂN VÙNG (PARTITION COUPLING)   │",
        "  │ • Trên S3 không có cây thư mục thật: lệnh Rename thực  │ • Lọc trên cột 'order_timestamp' mà quên thêm điều kiện │",
        "  │   chất là chuỗi COPY + DELETE tốn O(N) theo byte!      │   lọc cột phân vùng 'year_month' ──> Quét toàn bộ bảng! │",
        "  ├────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┤",
        "  │ [3] THIẾU GIAO DỊCH ĐA PHÂN VÙNG (NO MULTI-PARTITION)  │ [6] THỐNG KÊ LỖI THỜI & GIỚI HẠN ĐƠN TỆP (SINGLE-OBJ)   │",
        "  │ • Hive Metastore chỉ khóa từng phân vùng đơn lẻ; cập   │ • Lệnh ANALYZE TABLE quá chậm; Strong Consistency của   │",
        "  │   nhật 12 tháng cùng lúc sẽ lộ trạng thái nửa cũ/mới!  │   S3 chỉ bảo vệ 1 tệp đơn lẻ, bó tay khi ghi 200 tệp!   │",
        "  └────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────┘",
    ], inner_width=118, header="6 KHIẾM KHUYẾT KIẾN TRÚC CỦA APACHE HIVE TABLE FORMAT TRÊN CLOUD OBJECT STORAGE", context="Storage-5.2c")
    d5_2c = "\n".join(l.rstrip() for l in b52c_hive)

    # 46. Trạm 5.3b: Kiến trúc Data Catalog 3 Tầng & 5 Trụ cột Giám sát Dữ liệu Chủ động (Data Observability)
    b53b_cat = make_box([
        "• Tầng 3 — Cổng Tra cứu & Cộng tác (Web Portal/Wiki):",
        "  Tra cứu định nghĩa bảng, chỉ định Data Owner/Steward",
        "                      ▲",
        "• Tầng 2 — Quét & Suy luận Tự động (Auto-Scanning):",
        "  Tự động khám phá Schema, gợi ý khóa JOIN & quét PII",
        "                      ▲",
        "• Tầng 1 — Tích hợp API Ứng dụng (API Integration):",
        "  Kết nối trực tiếp với Spark, Airflow, dbt, Lakehouse",
    ], inner_width=56, header="KIẾN TRÚC DATA CATALOG HIỆN ĐẠI (3 TẦNG)", context="Storage-5.3b.cat")
    b53b_obs = make_box([
        "• [1] Freshness (Độ tươi mới): Có trễ SLA 6 tiếng không?",
        "• [2] Volume (Sản lượng)     : Có tụt dòng hoặc tăng gấp",
        "      đôi bất thường do tệp rác Zombie Writes không?",
        "• [3] Schema (Cấu trúc)      : Có ai tự ý đổi tên cột",
        "      (total_cost ──> order_amount) làm gãy ETL không?",
        "• [4] Distribution (Phân phối): Tỷ lệ NULL / số âm có vọt?",
        "• [5] Lineage (Phả hệ Cột/Bảng): Truy vết Root Cause &",
        "      khoanh vùng ảnh hưởng hạ nguồn (Blast Radius)!",
    ], inner_width=60, header="5 TRỤ CỘT GIÁM SÁT DỮ LIỆU (DATA OBSERVABILITY)", context="Storage-5.3b.obs")
    d5_3b = "\n".join(join_horizontal([b53b_cat, b53b_obs], ["  "], context="Storage-5.3b"))

    # 47. Trạm 6.3b: Tiến hóa Lược đồ bằng Định danh Cột Bất biến (Column ID) & Luồng Thay đổi (Change Data Feed)
    b63b_schema = make_box([
        "• [x] Bảng Parquet/Hive cũ (Ánh xạ theo Tên chữ):",
        "  Đổi tên 'total_cost' ──> 'order_amount' khiến tệp cũ",
        "  trả về toàn bộ NULL (hoặc dữ liệu cũ đội mồ sống dậy)!",
        "• [+] Iceberg & Delta Column Mapping (Ánh xạ theo ID):",
        "  Gắn mã bất biến: order_id [ID=1], total_cost [ID=2].",
        "  ──> Khi RENAME sang 'order_amount', chỉ sửa nhãn của",
        "      [ID=2] trong Metadata mất 1 ms, KHÔNG VIẾT LẠI TỆP!",
    ], inner_width=58, header="1. SCHEMA EVOLUTION QUA MÃ CỘT BẤT BIẾN (COLUMN ID)", context="Storage-6.3b.schema")
    b63b_cdf = make_box([
        "• Khi bật Change Data Feed (CDF / Changelog Scan):",
        "  Mỗi lần Đơn #8888 sửa từ 15M ──> 14M ở Version 1,",
        "  Lakehouse tự động xuất luồng thay đổi kèm '_change_type':",
        "  - insert           : Bản ghi mới chèn",
        "  - update_preimage  : Giá trị trước khi sửa (15.000.000đ)",
        "  - update_postimage : Giá trị sau khi sửa   (14.000.000đ)",
        "  - delete           : Bản ghi bị xóa (phục vụ ETL Silver->Gold)",
    ], inner_width=64, header="2. LUỒNG THAY ĐỔI TĂNG TRƯỞNG (CHANGE DATA FEED)", context="Storage-6.3b.cdf")
    d6_3b = "\n".join(join_horizontal([b63b_schema, b63b_cdf], ["  "], context="Storage-6.3b"))

    # 48. Trạm 7.1a: Kiến trúc Multi-hop Medallion & Cổng Kiểm soát Chất lượng (Quality Gating Pattern)
    b71a_bronze = make_box([
        "• Tuổi sơ sinh: Vùng hạ cánh thô",
        "  (Raw Landing Zone) từ Kafka/CDC",
        "• Ghi Append-only & Immutable",
        "• Biến đổi tối thiểu; hứng lỗi",
        "  vào cột '_corrupt' / '_debug'",
        "• [+] Chốt chặn Audit & Replay!",
    ], inner_width=33, header="1. BRONZE LAYER (INFANCY)", context="Storage-7.1a.bronze")
    b71a_silver = make_box([
        "• Tuổi thiếu niên: Lọc bỏ dòng",
        "  '_corrupt', khử trùng (Dedup)",
        "• Cưỡng chế Schema, chuẩn hóa kiểu",
        "• Hợp nhất đa nguồn thành góc nhìn",
        "  Enterprise View (~3NF / SCD2)",
        "• [+] Phục vụ Analyst & Data Sci!",
    ], inner_width=34, header="2. SILVER LAYER (TEENAGE)", context="Storage-7.1a.silver")
    b71a_gold = make_box([
        "• Tuổi trưởng thành (30-40): Thiết",
        "  kế chuyên biệt theo bài toán",
        "• Tính sẵn KPI & quy tắc nghiệp vụ",
        "• Phi chuẩn hóa tối ưu đọc (Star",
        "  Schema / OBT - giảm tối đa JOIN)",
        "• [+] Nuôi Dashboard BI & AI/ML!",
    ], inner_width=34, header="3. GOLD LAYER (MATURITY)", context="Storage-7.1a.gold")
    d7_1a = "\n".join(join_horizontal([b71a_bronze, b71a_silver, b71a_gold], [" ──(Cổng 1)──> ", " ──(Cổng 2)──> "], context="Storage-7.1a"))

    # 49. Trạm 7.1b: Đối chiếu Đường ống 1-Hop Mong manh vs. Kiến trúc 3-Tiered Medallion Có Chốt chặn Quay lui
    b71b_1hop = make_box([
        "• [x] Gãy vụn tức thì: Chỉ cần 1 gói tin JSON của",
        "      Đơn #8889 bị lỗi định dạng là sập cả báo cáo CEO",
        "• [x] Không có điểm quay lui (No Fallback): Khi công",
        "      thức tính KPI đổi, phải chọc ngược vào DB OLTP",
        "      đang chạy thật để kéo lại dữ liệu (Gây nghẽn!)",
        "• [x] Trùng lặp công sức: 5 phòng ban phải tự viết lại",
        "      cùng 1 đoạn code làm sạch & khử trùng từ đầu",
    ], inner_width=56, header="1. ĐƯỜNG ỐNG 1-HOP TRỰC TIẾP (NGUỒN ──> THẲNG BI)", context="Storage-7.1b.1hop")
    b71b_3hop = make_box([
        "• [+] Tầng Bronze làm mỏ neo bất biến: Cất giữ trọn vẹn",
        "      lịch sử thô trên S3; khi cần sửa lỗi chỉ việc",
        "      Replay từ Bronze -> Silver mà không chạm DB OLTP!",
        "• [+] Tầng Silver tái sử dụng toàn công ty: Làm sạch &",
        "      khử trùng Đơn #8888 đúng 1 lần cho mọi đội nhóm",
        "• [+] Linh hoạt mở rộng: Có thể nối Gold -> Gold tạo sản",
        "      phẩm mới (hoặc nạp thẳng nguồn đã sạch vào Gold)",
    ], inner_width=58, header="2. KIẾN TRÚC 3-TIERED MEDALLION (CÓ ĐIỂM FALLBACK)", context="Storage-7.1b.3hop")
    d7_1b = "\n".join(join_horizontal([b71b_1hop, b71b_3hop], ["  "], context="Storage-7.1b"))

    # 50. Trạm 7.2a: Cơ chế Cột Bảo toàn Lỗi (_corrupt / _debug) & Cách ly Dữ liệu Bẩn (Quarantine / DLQ)
    d7_2a = "\n".join(l.rstrip() for l in make_box([
        "  [Luồng Kafka / CDC] ──> Gồm Đơn #8888 (Hợp lệ: 15M) + Đơn #8889 (Lỗi JSON: 'ERROR_TIMEOUT')",
        "                                           │",
        "                                           ▼",
        "  [Spark Permissive Mode: option('mode','PERMISSIVE').option('columnNameOfCorruptRecord','_corrupt')]",
        "  ──> Ghi toàn bộ vào bảng 'bronze.sales_transactions_raw' (KHÔNG LÀM GÃY PIPELINE GIỮA ĐÊM!)",
        "      • Đơn #8888: order_id='8888' | raw_amount='15,000,000 VND' | _corrupt = NULL",
        "      • Đơn #8889: order_id='8889' | raw_amount='ERROR_TIMEOUT'  | _corrupt = '{raw_err_payload}'",
        "                                           │",
        "            ┌──────────────────────────────┴──────────────────────────────┐",
        "            │ Cổng lọc 1: WHERE _corrupt IS NULL                          │ Cổng cách ly: WHERE _corrupt IS NOT NULL",
        "            ▼ (Bỏ cột _corrupt + Dedup + Ép kiểu DECIMAL)                 ▼ (Đẩy sang bảng cách ly + Bắn cảnh báo)",
        "  [+] Bảng 'silver.orders_cleaned' (Đơn #8888 sạch)         [!] Bảng 'quarantine.corrupt_orders' (Chờ sửa & Replay)",
    ], inner_width=116, header="CƠ CHẾ CỘT BẢO TOÀN LỖI (PERMISSIVE PASSTHROUGH: _corrupt / _debug) & CÁCH LY DỮ LIỆU BẨN", context="Storage-7.2a"))

    # 51. Trạm 7.2b: Hành trình Lột xác của Đơn hàng #8888 qua 3 Bảng Lakehouse (Bronze -> Silver -> Gold)
    d7_2b = "\n".join(l.rstrip() for l in make_box([
        "  [1] TẦNG BRONZE: Bảng 'bronze.sales_transactions_raw' (Append-only / MOR, giữ nguyên bản từ CDC Kafka)",
        "      • Dòng 1: id='8888' | cust='  nguyen van a ' | amt='15,000,000 VND' | ts=14:00:01 | _corrupt=NULL",
        "      • Dòng 2: id='8888' | cust='  nguyen van a ' | amt='15,000,000 VND' | ts=14:00:02 | _corrupt=NULL (Trùng)",
        "      • Dòng 3: id='8889' | cust=NULL              | amt='ERROR_TIMEOUT'  | ts=14:00:05 | _corrupt='{raw_err}'",
        "                                                       │",
        "      Pipeline Bronze ──> Silver: Lọc bỏ _corrupt != NULL, Khử trùng (Dedup) mã 8888,",
        "      Chuẩn hóa chữ hoa & kiểu số DECIMAL(15000000.00), đối khớp thực thể (~3NF / SCD Type 2)",
        "                                                       ▼",
        "  [2] TẦNG SILVER: Bảng 'silver.orders_cleaned' (Góc nhìn Doanh nghiệp chuẩn hóa ~3NF, đã bỏ cột _corrupt)",
        "      • Dòng chuẩn: order_id=8888 | customer_sk=501 | store_sk=12 | net_amount=15000000.00 | ts=2026-10-15 14:00:01",
        "                                                       │",
        "      Pipeline Silver ──> Gold: Áp quy tắc kinh doanh (Hạng VIP_GOLD), phi chuẩn hóa thành Star Schema",
        "      hoặc gộp phẳng thành OBT (One Big Table) / Tổng hợp KPI doanh thu theo Tỉnh (COW + Z-Ordering)",
        "                                                       ▼",
        "  [3] TẦNG GOLD: Bảng 'gold.obt_customer_sales_analytics' (Phi chuẩn hóa OBT — 0 JOIN cho BI & AI!)",
        "      • Thành phẩm: order_id=8888 | Nguyễn Văn A | Bình Dương | Showroom Bình Dương 1 | 15000000.00 | VIP_GOLD",
    ], inner_width=116, header="HÀNH TRÌNH LỘT XÁC CỦA ĐƠN HÀNG #8888 QUA 3 BẢNG LAKEHOUSE (BRONZE -> SILVER -> GOLD)", context="Storage-7.2b"))

    # 52. Trạm 7.2c: Streaming Medallion & 3 Chốt chặn Kiểm định Chất lượng Tự động (Schema Gate, CHECK, DLT/WAP)
    b72c_schema = make_box([
        "• Tắt trộn lược đồ tự động:",
        "  mergeSchema = false (Mặc định)",
        "• Cấm ghi đè lược đồ bừa bãi:",
        "  overwriteSchema = false",
        "• [+] Ngăn cột rác từ tầng Bronze",
        "  vô tình tràn sang làm bẩn Silver!",
    ], inner_width=36, header="1. KHÓA LƯỢC ĐỒ (SCHEMA GATE)", context="Storage-7.2c.schema")
    b72c_check = make_box([
        "• Khai báo bất biến cấp bảng:",
        "  ALTER TABLE silver.orders",
        "  ADD CONSTRAINT valid_amount",
        "  CHECK (net_amount > 0)",
        "• [+] Vi phạm sẽ chặn ghi tức thì:",
        "  DeltaInvariantViolationException",
    ], inner_width=36, header="2. RÀNG BUỘC CHECK CONSTRAINTS", context="Storage-7.2c.check")
    b72c_expect = make_box([
        "• @dlt.expect: Ghi log cảnh báo",
        "• @dlt.expect_or_drop: Lọc dòng bẩn",
        "• @dlt.expect_or_fail: Dừng pipeline",
        "• Iceberg WAP (Write-Audit-Publish):",
        "  Ghi vào nhánh 'audit', kiểm định",
        "  Pass 100% mới nối sang nhánh 'main'",
    ], inner_width=38, header="3. DLT EXPECTATIONS & ICEBERG WAP", context="Storage-7.2c.expect")
    d7_2c = "\n".join(join_horizontal([b72c_schema, b72c_check, b72c_expect], ["  ", "  "], context="Storage-7.2c"))

    # 53. Trạm 7.3a: Kiến trúc Medallion được nâng đỡ bởi Các Dòng chảy Ngầm (The Undercurrents)
    d7_3a = "\n".join(l.rstrip() for l in make_box([
        "      [ 1. BRONZE LAYER (Raw) ] ─────────> [ 2. SILVER LAYER (~3NF/SCD2) ] ─────────> [ 3. GOLD LAYER (Star/OBT) ]",
        "                  ▲                                       ▲                                       ▲",
        "                  │                                       │                                       │",
        "  ════════════════╪═══════════════════════════════════════╪═══════════════════════════════════════╪════════════════",
        "  DÒNG CHẢY NGẦM QUẢN TRỊ & VẬN HÀNH XUYÊN SUỐT (THE UNDERCURRENTS — REIS & HOUSLEY / DELTA GUIDE CH. 12-13):",
        "  ├── [1] Data Catalog & Lineage : Unity Catalog / Glue / Nessie (catalog.schema.table) + OpenLineage (Job-Run)",
        "  ├── [2] Security & Compliance  : Least Privilege (DCL GRANT/REVOKE), Row Filter, Column Masking & Xóa GDPR",
        "  └── [3] Cloud FinOps Lifecycle : Hot ($0.02/GB) ──> Warm ($0.01/GB) ──> Cold/Archival ($0.004/GB, 1/17 giá)",
    ], inner_width=116, header="KIẾN TRÚC MEDALLION ĐƯỢC NÂNG ĐỠ BỞI CÁC DÒNG CHẢY NGẦM (THE UNDERCURRENTS)", context="Storage-7.3a"))

    # 54. Trạm 7.3b: Phản mẫu "Xuất ra 40 Buckets Riêng lẻ" vs. Nguồn Sự thật Duy nhất (Single Source of Truth)
    b73b_bad = make_box([
        "• Xuất (Export) các phân vùng bảng Đơn hàng ra 40",
        "  Buckets / Prefixes S3 riêng cho 40 đội nhóm:",
        "• [x] Ác mộng phân quyền: Phải cấp & thu hồi quyền",
        "      IAM rời rạc ở cả 40 nơi (Rất dễ lộ lọt dữ liệu)",
        "• [x] Đốt tiền khi Reprocess: Khi Đơn #8888 cần sửa",
        "      lỗi, phải tính toán lại 40 lần & gánh phí băng",
        "      thông mạng 2 chiều (Ingress & Egress) đắt đỏ!",
    ], inner_width=55, header="1. PHẢN MẪU: EXPORT RA 40 BUCKETS RIÊNG LẺ", context="Storage-7.3b.bad")
    b73b_good = make_box([
        "• Duy trì 1 bảng vật lý duy nhất trên S3, quản trị",
        "  qua định danh 3 cấp 'prod.gold.customer_sales':",
        "• [+] Phân quyền tập trung tại 1 nơi bằng SQL DCL",
        "      hoặc chia sẻ zero-copy qua Delta Sharing",
        "• [+] Sửa lỗi 1 lần cho tất cả: Khi Reprocess Đơn",
        "      #8888 tại bảng gốc, cả 40 đội nhóm thấy ngay",
        "      số liệu chuẩn mà tốn $0 phí chép mạng dư thừa!",
    ], inner_width=57, header="2. CHUẨN MỰC: SINGLE SOURCE OF TRUTH + CATALOG", context="Storage-7.3b.good")
    d7_3b = "\n".join(join_horizontal([b73b_bad, b73b_good], ["  "], context="Storage-7.3b"))

    # 55. Trạm 7.3c: Phân quyền Chi tiết trên Cùng 1 Bảng Gold (Row-Level Security & Column Masking)
    d7_3c = "\n".join(l.rstrip() for l in make_box([
        "  BẢNG GỐC DUY NHẤT TRÊN S3: 'prod.gold.customer_sales'",
        "  • Dòng 1: order_id=8888 | cust=Nguyễn Văn A | phone=0909-123-456 | province=Bình Dương | revenue=15.000.000đ",
        "  • Dòng 2: order_id=9999 | cust=Trần Thị B   | phone=0918-888-999 | province=TP.HCM     | revenue=20.000.000đ",
        "               │                                                    │",
        "               ├──> [1] Giám đốc Chi nhánh Bình Dương               ├──> [2] Chuyên viên Phân tích (Data Analyst)",
        "               │    (Áp dụng ROW-LEVEL SECURITY / ROW FILTER:       │    (Áp dụng COLUMN-LEVEL MASKING:",
        "               │     Chỉ trả về dòng có province = 'Bình Dương')    │     Tự động che mờ cột PII phone_number)",
        "               ▼                                                    ▼",
        "     [+] Chỉ thấy Đơn #8888 (Ẩn hoàn toàn Đơn #9999)      [+] Thấy cả 2 đơn, nhưng SĐT hiện 'xxxx-xxx-456'",
    ], inner_width=116, header="PHÂN QUYỀN CHI TIẾT TRÊN CÙNG 1 BẢNG GOLD (ROW-LEVEL SECURITY & COLUMN MASKING)", context="Storage-7.3c"))

    # 56. Trạm 7.3d: Vòng đời Nhiệt độ Dữ liệu & Tối ưu Chi phí Đám mây (Cloud FinOps Lifecycle)
    b73d_hot = make_box([
        "• Dữ liệu: Bảng Gold & Silver",
        "  đang truy vấn BI/ML hàng ngày",
        "• Lưu trữ: S3 Standard / GCS",
        "  Standard + Cache NVMe SSD/RAM",
        "• Chi phí: ~$0.020 - $0.023/GB",
        "• Độ trễ: ~100 us (Cache) - ms",
    ], inner_width=33, header="1. TẦNG NÓNG (HOT TIER)", context="Storage-7.3d.hot")
    b73d_warm = make_box([
        "• Dữ liệu: Bảng Silver / Bronze",
        "  ít truy cập sau 30 - 90 ngày",
        "• Lưu trữ: S3 Standard-IA /",
        "  GCS Nearline / Cool Blob",
        "• Chi phí: ~$0.010 - $0.0125/GB",
        "• Lưu ý: Giữ tối thiểu >= 30 ngày",
    ], inner_width=35, header="2. TẦNG ẤM (WARM TIER)", context="Storage-7.3d.warm")
    b73d_cold = make_box([
        "• Dữ liệu: Bảng Bronze quá hạn",
        "  6-12 tháng (giữ để Audit/Replay)",
        "• Lưu trữ: S3 Glacier Instant /",
        "  Deep Archive / GCS Archive",
        "• Chi phí: ~$0.004 - $0.001/GB",
        "• [+] Rẻ bằng ~1/6 đến 1/17 giá!",
    ], inner_width=36, header="3. TẦNG LẠNH (COLD / ARCHIVAL)", context="Storage-7.3d.cold")
    d7_3d = "\n".join(join_horizontal([b73d_hot, b73d_warm, b73d_cold], [" ──(30d)──> ", " ──(180d)──> "], context="Storage-7.3d"))

    # 57. Trạm 7.4: Bản đồ Kiến trúc Tổng thể 6 Tầng (Bottom-Up Blueprint)
    d7_4 = "\n".join(l.rstrip() for l in make_box([
        "  [TẦNG 6] CONSUMPTION & GOVERNANCE UNDERCURRENTS (Chặng 4 & Chặng 7)",
        "  • Phục vụ: Power BI, Tableau, SQL Analytics, Data Science, Machine Learning / AI Agents",
        "  • Quản trị ngầm: Unity Catalog / Glue / Nessie, OpenLineage, Row/Col Security, GDPR, FinOps",
        "  ────────────────────────────────────────────────────────────────────────────────────────────────────────────────",
        "  [TẦNG 5] DATA ORGANIZATION & MODELING — MEDALLION & KIMBALL (Chặng 4 & Chặng 7)",
        "  • Luồng Multi-hop: Bronze (Raw Append-only/Replay + _corrupt) ──> Silver (Cleaned ~3NF/SCD2) ──> Gold (Curated)",
        "  • Kỹ thuật Kimball tại Gold: Fact vs. Dimension, Star Schema / OBT (0 JOIN), Surrogate Key, Bus Matrix",
        "  ────────────────────────────────────────────────────────────────────────────────────────────────────────────────",
        "  [TẦNG 4] COMPUTE & STREAMING ENGINES — TÁCH RỜI KHỎI STORAGE (Chặng 3 & Chặng 6)",
        "  • Batch & Query MPP: Apache Spark, Trino, Presto, Snowflake, BigQuery, Microsoft Fabric (Ephemeral Compute)",
        "  • Streaming & Cache: Debezium CDC ──> Apache Kafka ──> Apache Flink (RocksDB State Store / Redis Cache)",
        "  ────────────────────────────────────────────────────────────────────────────────────────────────────────────────",
        "  [TẦNG 3] OPEN TABLE FORMATS — BỘ NÃO GIAO DỊCH LAKEHOUSE (Chặng 5 & Chặng 6)",
        "  • Động cơ: Delta Lake (_delta_log) | Apache Iceberg (3-layer Metadata Tree) | Apache Hudi (Timeline + Index)",
        "  • Sức mạnh: ACID, MVCC/OCC/NBCC, Time Travel, Schema Evolution, COW vs. MOR, Z-Order/Hilbert, Deletion Vectors",
        "  ────────────────────────────────────────────────────────────────────────────────────────────────────────────────",
        "  [TẦNG 2] FILE FORMATS, IN-MEMORY & COMPRESSION PRIMITIVES (Chặng 2)",
        "  • Trên đĩa: Row-oriented (CSV, JSON, Avro + Sync Markers) vs. Columnar (Parquet Footer/RowGroup, ORC)",
        "  • Trên RAM: Apache Arrow (Zero-copy SIMD) | Nén: Snappy, LZ4, ZSTD, Gzip & Tính phân tách (Splittability)",
        "  ────────────────────────────────────────────────────────────────────────────────────────────────────────────────",
        "  [TẦNG 1] PHYSICAL HARDWARE & STORAGE MODELS — NỀN MÓNG VẬT LÝ (Chặng 1, Chặng 2 & Chặng 3)",
        "  • Phần cứng: CPU Cache (1 ns) ──> RAM (100 ns, Volatile, Spill-to-Disk) ──> NVMe SSD (100 us) ──> HDD (4-10 ms)",
        "  • Mô hình: Random Seek vs. Sequential Scan | File vs. Block vs. Object Storage (S3/ADLS/GCS ~100 ms) & HDFS (x3)",
    ], inner_width=116, header="BẢN ĐỒ KIẾN TRÚC 6 TẦNG CỦA HỆ THỐNG LƯU TRỮ HIỆN ĐẠI (BOTTOM-UP BLUEPRINT: CHẶNG 1 -> CHẶNG 7)", context="Storage-7.4"))

    # 0.1: Bản đồ Tư duy 7 Chặng Storage Layer — Hành trình Tiến hóa của Đơn hàng #8888
    b0_s1 = make_box([
        "[CHẶNG 1–2] Vật lý & Định dạng Tệp:",
        " • Đơn #8888 sinh ra trên RAM (100 ns) -> NVMe SSD (100 µs)",
        " • Chuyển từ OLTP Row (Avro/CSV) sang Columnar (Parquet)",
        " • Đọc siêu tốc trên RAM nhờ Zero-Copy Apache Arrow",
        "                            │",
        "                            ▼",
        "[CHẶNG 3–4] Hạ tầng Phân tán & Mô hình Hóa (Data Modeling):",
        " • Lưu phân tán HDFS (x3) / Streaming Kafka CDC Append-only",
        " • Đưa vào Data Warehouse theo Kimball Star Schema / SCD2",
        " • Đụng trần 3 giới hạn: Dữ liệu phi cấu trúc, Giá & Đóng kín"
    ], inner_width=62, header="1–4. NỀN MÓNG VẬT LÝ, ĐỊNH DẠNG TỆP & DATA WAREHOUSE", context="Storage-0.1-left")
    b0_s2 = make_box([
        "[CHẶNG 5–6] Từ Data Lake/Swamp lên Data Lakehouse:",
        " • Đổ thô xuống S3/GCS ($0.02/GB) -> Hóa Đầm lầy (Data Swamp)",
        " • Lắp bộ não Open Table Formats (Delta Lake / Iceberg / Hudi)",
        " • Phục hồi ACID, Time Travel, Schema Enforcement, COW/MOR",
        "                            │",
        "                            ▼",
        "[CHẶNG 7] Quy hoạch Multi-Hop Medallion & Governance:",
        " • Tinh chế lũy tiến: Bronze (Raw) -> Silver (Clean) -> Gold",
        " • Quản trị ngầm: Unity Catalog, OpenLineage, RLS/Masking",
        " • Tối ưu FinOps: Tiering Hot/Warm/Cold & Ephemeral Compute"
    ], inner_width=62, header="5–7. TỪ DATA LAKE LÊN LAKEHOUSE & MEDALLION GOVERNANCE", context="Storage-0.1-right")
    d0_1 = "\n".join(join_horizontal([b0_s1, b0_s2], ["     "], {6: [" ──> "]}, context="Storage-0.1"))

    diagrams = {
        "0.1": {"ascii": d0_1, "kind": "boxes"},
        "1.1": {"ascii": d1_1, "kind": "pyramid"},
        "1.2": {"ascii": d1_2, "kind": "boxes"},
        "1.2b": {"ascii": d1_2b, "kind": "boxes"},
        "1.3": {"ascii": d1_3, "kind": "boxes"},
        "1.3b": {"ascii": d1_3b, "kind": "boxes"},
        "1.4": {"ascii": d1_4, "kind": "boxes"},
        "1.5": {"ascii": d1_5, "kind": "boxes"},
        "2.1": {"ascii": d2_1, "kind": "boxes"},
        "2.1b": {"ascii": d2_1b, "kind": "boxes"},
        "2.2a": {"ascii": d2_2a, "kind": "boxes"},
        "2.2b": {"ascii": d2_2b, "kind": "boxes"},
        "2.3": {"ascii": d2_3, "kind": "boxes"},
        "2.4": {"ascii": d2_4, "kind": "boxes"},
        "2.4b": {"ascii": d2_4b, "kind": "boxes"},
        "3.1": {"ascii": d3_1, "kind": "boxes"},
        "3.2": {"ascii": d3_2, "kind": "boxes"},
        "3.2b": {"ascii": d3_2b, "kind": "boxes"},
        "3.3": {"ascii": d3_3, "kind": "boxes"},
        "3.4": {"ascii": d3_4, "kind": "boxes"},
        "3.5": {"ascii": d3_5, "kind": "boxes"},
        "4.1": {"ascii": d4_1, "kind": "boxes"},
        "4.2": {"ascii": d4_2, "kind": "boxes"},
        "4.3": {"ascii": d4_3, "kind": "boxes"},
        "4.3b": {"ascii": d4_3b, "kind": "boxes"},
        "4.4": {"ascii": d4_4, "kind": "boxes"},
        "4.5a": {"ascii": d4_5a, "kind": "boxes"},
        "4.5": {"ascii": d4_5, "kind": "boxes"},
        "5.1": {"ascii": d5_1, "kind": "boxes"},
        "5.2a": {"ascii": d5_2a, "kind": "boxes"},
        "5.2b": {"ascii": d5_2b, "kind": "boxes"},
        "5.2c": {"ascii": d5_2c, "kind": "boxes"},
        "5.3": {"ascii": d5_3, "kind": "boxes"},
        "5.3b": {"ascii": d5_3b, "kind": "boxes"},
        "5.4a": {"ascii": d5_4a, "kind": "boxes"},
        "5.4b": {"ascii": d5_4b, "kind": "boxes"},
        "6.1a": {"ascii": d6_1a, "kind": "boxes"},
        "6.1b": {"ascii": d6_1b, "kind": "boxes"},
        "6.2a": {"ascii": d6_2a, "kind": "boxes"},
        "6.2b": {"ascii": d6_2b, "kind": "boxes"},
        "6.2c": {"ascii": d6_2c, "kind": "boxes"},
        "6.2d": {"ascii": d6_2d, "kind": "boxes"},
        "6.3": {"ascii": d6_3, "kind": "boxes"},
        "6.3b": {"ascii": d6_3b, "kind": "boxes"},
        "6.4": {"ascii": d6_4, "kind": "boxes"},
        "6.5a": {"ascii": d6_5a, "kind": "boxes"},
        "6.5b": {"ascii": d6_5b, "kind": "boxes"},
        "6.5c": {"ascii": d6_5c, "kind": "boxes"},
        "7.1a": {"ascii": d7_1a, "kind": "boxes"},
        "7.1b": {"ascii": d7_1b, "kind": "boxes"},
        "7.2a": {"ascii": d7_2a, "kind": "boxes"},
        "7.2b": {"ascii": d7_2b, "kind": "boxes"},
        "7.2c": {"ascii": d7_2c, "kind": "boxes"},
        "7.3a": {"ascii": d7_3a, "kind": "boxes"},
        "7.3b": {"ascii": d7_3b, "kind": "boxes"},
        "7.3c": {"ascii": d7_3c, "kind": "boxes"},
        "7.3d": {"ascii": d7_3d, "kind": "boxes"},
        "7.4": {"ascii": d7_4, "kind": "boxes"},
    }
    for k, meta in diagrams.items():
        errs = verify_diagram(meta["ascii"], f"Storage-{k}", kind=meta["kind"])
        if errs:
            raise SystemExit(f"ASCII verification failed for Storage-{k} ({meta['kind']}): {errs}")
    return diagrams


def build_linux_ascii_diagrams() -> dict:
    # 0.1: Hành trình 4 Bước Tiến Hóa của Nhân Vật Chính grep ERROR /var/log/app.log
    b0_1_left = make_box([
        "[BƯỚC 1 — CHẶNG 1] Từ Tĩnh sang Động:",
        " • Gõ dòng chữ tĩnh trên Terminal (Quầy lễ tân)",
        " • Shell (Bash) đánh thức Program (/bin/grep)",
        " • Cấp phát RAM/CPU thành Process đang chạy",
        "                     │",
        "                     ▼",
        "[BƯỚC 2 — CHẶNG 2] Va chạm Ranh giới Bảo mật:",
        " • Process trình phiếu System Call (open/read)",
        " • Linux Kernel xét 5 thuộc tính căn cước:",
        "   PID, UID/GID, Working Dir, Env, Open Files",
        " • Mở kho /var/log/app.log trên cây thư mục /",
    ], inner_width=47, header="1–2. TỪ TĨNH SANG ĐỘNG & VƯỢT RANH GIỚI KERNEL", context="Linux-0.1.left")

    b0_1_right = make_box([
        "[BƯỚC 3 — CHẶNG 3] Phối hợp Dây chuyền IPC:",
        " • Một mình grep không xuể -> nối ống Pipe (|)",
        " • Qua 3 cổng: stdin(0), stdout(1), stderr(2)",
        " • Tách riêng luồng lỗi (2>&1), không bẩn KQ",
        "                     │",
        "                     ▼",
        "[BƯỚC 4 — CHẶNG 4] Tự động hóa Công nghiệp:",
        " • Bash Script (.sh): Định nghĩa làm bước nào",
        " • GCC & Makefile: Xét timestamp có làm lại?",
        " • Cronjob (crond): Quét mỗi 60s chạy 03:00",
        " • [+] Khép kín từ 1 phím gõ đến hệ thống 24/7!",
    ], inner_width=47, header="3–4. NỐI ỐNG PIPE (IPC) & TỰ ĐỘNG HÓA 24/7", context="Linux-0.1.right")
    d0_1 = "\n".join(join_horizontal([b0_1_left, b0_1_right], ["     "], {6: [" ──> "]}, context="Linux-0.1"))

    # 0.2: Bản đồ Cơ học Linux — Mô hình "Căn bếp" & Dây chuyền Tự động hóa 4 Chặng
    b0_2_c1 = make_box([
        "Lệnh mẫu: grep ERROR /var/log/app.log",
        "[1] TERMINAL (Quầy giao tiếp): Nhận phím & in",
        "         │",
        "         ▼",
        "[2] SHELL / BASH (Người nhận việc): Tách lệnh",
        "         │",
        "         ▼",
        "[3] PROGRAM (Công thức đĩa): File /bin/grep",
        "         │",
        "         ▼",
        "[4] PROCESS (Đầu bếp chạy trên RAM & CPU)",
    ], inner_width=47, header="[CHẶNG 1] KHỞI NGUỒN & LUỒNG CHẠY 1 LỆNH", context="Linux-0.2.c1")

    b0_2_c2 = make_box([
        "HỒ SƠ MỘT PROCESS ĐANG CHẠY:",
        " • PID & User/Group (UID/GID: root / me)",
        " • Working Dir (cwd) + Environment ($PATH)",
        " • Open Files (Bảng File Descriptors 0, 1, 2)",
        "         │",
        "         ▼",
        "BẢN ĐỒ KHO HÀNG (UNIFIED FILESYSTEM /):",
        " • /bin, /sbin, /usr : Kệ chứa Program",
        " • /home, /root, /etc: Phòng riêng & Cấu hình",
        " • /var/log, /tmp    : Kho log & Bàn nháp",
        " • /proc (0 MB Disk) : Cửa kính ảo trên RAM",
    ], inner_width=47, header="[CHẶNG 2] CĂN CƯỚC PROCESS & KHO HÀNG /", context="Linux-0.2.c2")
    tier1 = join_horizontal([b0_2_c1, b0_2_c2], ["     "], {11: [" ──> "]}, context="Linux-0.2.tier1")

    tier2 = [l.rstrip() for l in make_box([
        "[5] SYSTEM CALL (Phiếu xin cấp phát tài nguyên: open, read, write, fork, execve, pipe, dup2...)",
        "                                                  │",
        "                                                  ▼",
        "[6] LINUX KERNEL (Bếp trưởng / Quản lý kho): Kiểm tra đường dẫn + Quyền (UID/GID) + Cấp phát phần cứng",
        " ├──> [ FILE (Sổ ghi) ]  : Triết lý 'Everything is a file' (/var/log/app.log, /dev/sda, /proc/PID)",
        " ├──> [ CPU (Não tính) ] : Chia lịch thực thi (Process Scheduling) cho hàng trăm tiến trình đồng thời",
        " ├──> [ RAM (Nhớ tạm) ]  : Giữ vùng nhớ Process (Text/Data/Heap/Stack) & bộ đệm đường ống Pipe (64 KB)",
        " └──> [ NETWORK (Mạng) ] : Trao đổi gói tin qua Socket (File Descriptor mạng) với máy chủ khác",
    ], inner_width=103, header="[RANH GIỚI AN NINH] SYSTEM CALL & LINUX KERNEL (BẾP TRƯỞNG TỐI CAO)", context="Linux-0.2.tier2")]

    b0_2_c3 = make_box([
        "Mọi Process mở sẵn 3 cổng File Descriptors:",
        " • [stdin : 0] Luồng nhập chuẩn (Phím / Pipe)",
        " • [stdout: 1] Luồng xuất kết quả chuẩn",
        " • [stderr: 2] Luồng báo lỗi độc lập",
        "         │",
        "         ▼",
        "ĐƯỜNG ỐNG PIPE (|) & ĐIỀU HƯỚNG (>, >>, 2>&1):",
        "[Process 1: stdout(1)] ──(Pipe RAM)──> [stdin]",
        " └─> [stderr(2)] tách riêng, không bẩn kết quả",
    ], inner_width=47, header="[CHẶNG 3] PHỐI HỢP ĐA TIẾN TRÌNH (IPC & I/O)", context="Linux-0.2.c3")

    b0_2_c4 = make_box([
        "BỘ BA TỰ ĐỘNG HÓA CÔNG NGHIỆP:",
        "[1] BASH SCRIPT (.sh): #!/bin/bash, chmod +x",
        "    -> Định nghĩa 'Làm những bước nào'",
        "[2] COMPILATION & MAKE: GCC (.c -> .o -> bin)",
        "    -> Make xét timestamp 'Có cần làm lại?'",
        "[3] CRONJOB (crond): Thức dậy mỗi 60 giây",
        "    -> Xét lịch (* * * * *) 'Khi nào kích hoạt'",
        "         │",
        "         └──> [+] Hệ thống tự vận hành 24/7!",
    ], inner_width=47, header="[CHẶNG 4] ĐÓNG GÓI & TỰ ĐỘNG HÓA 24/7", context="Linux-0.2.c4")
    tier3 = join_horizontal([b0_2_c3, b0_2_c4], ["     "], {5: [" ──> "]}, context="Linux-0.2.tier3")

    d0_2 = "\n".join(
        tier1
        + [
            "                         │  (1. Trình phiếu System Call)  (2. Xuất trình Căn cước) │",
            "                         ▼                                                         ▼",
        ]
        + tier2
        + [
            "                         │  (3. Cấp phát Kernel Pipe I/O) (4. Kích hoạt crond 60s) │",
            "                         ▼                                                         ▼",
        ]
        + tier3
    )

    # 1.1a: Cú ghép lịch sử tạo nên hệ điều hành hoàn chỉnh GNU/Linux
    b1_1a_left = make_box([
        "[+] Bash     : Màn hình dòng lệnh (CLI Shell)",
        "[+] Coreutils: Bộ lệnh ls, cp, mv, rm, grep...",
        "[+] GCC & GDB: Dịch code C/C++ -> 0/1 & soi lỗi",
        "[+] glibc    : Thư viện hàm C bọc System Call",
        "[+] Emacs    : Trình soạn thảo mã nguồn chuẩn",
        "[!] NỖI ĐAU  : Khuyết mất quả tim (Kernel)!",
    ], inner_width=47, header='1. DỰ ÁN GNU (Stallman, 1983 - "Khung sườn xe")', context="Linux-1.1a.left")

    b1_1a_right = make_box([
        "[+] CPU Scheduler : Chia lượt xử lý tiến trình",
        "[+] Memory Mgmt   : Cấp phát & cách ly vùng RAM",
        "[+] VFS & File Sys: Quản lý kho tệp (ext4/xfs)",
        "[+] Device Control: Điều khiển đĩa, phím, mạng",
        "[+] System Calls  : Cổng kiểm soát đặc quyền",
        "[!] NỖI ĐAU       : Không có công cụ để bấm!",
    ], inner_width=47, header='2. HẠT NHÂN LINUX (Torvalds, 1991 - "Cục máy")', context="Linux-1.1a.right")

    tier1_1a_top = join_horizontal([b1_1a_left, b1_1a_right], ["     "], {4: [" ──> "]}, context="Linux-1.1a.top")
    tier1_1a_bot = [l.rstrip() for l in make_box([
        "• Kế thừa triết lý UNIX (Thompson & Ritchie, 1969) & chuẩn POSIX / giấy phép mở GPLv2",
        "• Người dùng gõ lệnh 'grep ERROR app.log' qua bộ công cụ GNU (Bash + /bin/grep + glibc)",
        "• Hạt nhân Linux Kernel điều khiển ổ cứng & CPU đọc tệp trả kết quả an toàn tuyệt đối",
    ], inner_width=103, header="3. HỆ ĐIỀU HÀNH HOÀN CHỈNH: GNU/LINUX (KHI BỘ KHUNG GẶP CỤC MÁY)", context="Linux-1.1a.bot")]

    d1_1a = "\n".join(
        tier1_1a_top
        + [
            "                         │   (Ghép Khung sườn GNU + Cục máy Linux năm 1991)    │",
            "                         ▼                                                     ▼",
        ]
        + tier1_1a_bot
    )

    # 1.1b: Giải phẫu 6 Trụ cột khiến GNU/Linux thống trị thế giới Server
    b1_1b_1 = make_box([
        "• Mã nguồn mở GPLv2 công khai",
        "• $0 chi phí bản quyền cho cả",
        "  1.000 máy chủ xử lý app.log",
        "• Hàng triệu chuyên gia toàn",
        "  cầu cùng soi lỗi & vá lỗ hổng",
    ], inner_width=31, header="1. OPEN SOURCE ($0 LICENSE)", context="Linux-1.1b.1")

    b1_1b_2 = make_box([
        "• 50 kỹ sư kết nối SSH vào",
        "  chung 1 server chạy độc lập",
        "• Hàng trăm Process chạy 24/7",
        "  quanh năm không cần Reboot",
        "• Không giẫm chân vùng nhớ",
    ], inner_width=31, header="2. MULTI-USER & MULTI-TASK", context="Linux-1.1b.2")

    b1_1b_3 = make_box([
        "• Khóa quyền chặt chẽ: User",
        "  thường vs. đặc quyền root",
        "• Ranh giới cứng User Space",
        "  (Ring 3) vs. Kernel (Ring 0)",
        "• Miễn nhiễm phần lớn mã độc",
    ], inner_width=31, header="3. SECURITY & STABILITY", context="Linux-1.1b.3")

    b1_1b_4 = make_box([
        "• Kiểm soát tới từng milimet",
        "  tài nguyên qua Kernel/cgroups",
        "• Ép sát giới hạn 1 ứng dụng",
        "  chỉ được dùng tối đa 10% CPU",
        "  và 1 GB RAM trên máy chủ",
    ], inner_width=31, header="4. GRANULAR RESOURCE CTRL", context="Linux-1.1b.4")

    b1_1b_5 = make_box([
        "• Tách rời GUI, cực kỳ nhẹ",
        "• Chạy từ vi mạch Router Wifi,",
        "  Android tới 100% siêu máy",
        "  tính TOP500 & đám mây Cloud",
        "• Lệnh grep chạy đồng nhất",
    ], inner_width=31, header="5. PORTABILITY (KHẢ CHUYỂN)", context="Linux-1.1b.5")

    b1_1b_6 = make_box([
        "• Hệ sinh thái gói phần mềm",
        "  chuẩn hóa (apt, dnf, Docker)",
        "• Nền tảng gốc của mọi công",
        "  nghệ Data & AI/ML hiện đại",
        "  (Spark, Kafka, Airflow, K8s)",
    ], inner_width=31, header="6. COMMUNITY & ECOSYSTEM", context="Linux-1.1b.6")

    row1_1b_top = join_horizontal([b1_1b_1, b1_1b_2, b1_1b_3], ["  ", "  "], context="Linux-1.1b.r1")
    row1_1b_bot = join_horizontal([b1_1b_4, b1_1b_5, b1_1b_6], ["  ", "  "], context="Linux-1.1b.r2")
    d1_1b = "\n".join(row1_1b_top + [""] + row1_1b_bot)

    # 1.2a: Sự phân nhánh các Hương vị (Distro) từ lõi GNU/Linux
    b1_2a_deb = make_box([
        "• 'Nồi đồng cối đá', chạy 10",
        "  năm bền bỉ không sập",
        "• Gói cài: dpkg / apt (.deb)",
        "• Nền tảng mẹ sinh ra Ubuntu,",
        "  Linux Mint và Kali Linux",
    ], inner_width=31, header="1. NHÁNH DEBIAN (NỀN TẢNG)", context="Linux-1.2a.deb")

    b1_2a_ent = make_box([
        "• 'Xe bọc thép' (Fedora/RHEL)",
        "• Gói cài: rpm / dnf (.rpm)",
        "• Ngân hàng, viễn thông, tập",
        "  đoàn lớn vận hành Core",
        "• Thuê bao hỗ trợ 24/7",
    ], inner_width=31, header="2. NHÁNH DOANH NGHIỆP (RHEL)", context="Linux-1.2a.ent")

    b1_2a_arch = make_box([
        "• 'Xe tự lắp ráp' (Arch Linux)",
        "• Gói cài: pacman (Rolling)",
        "• Tự gõ lệnh lắp ráp từng con",
        "  ốc vít phần mềm từ số 0",
        "• Tối ưu sâu nhưng tốn giờ cài",
    ], inner_width=31, header="3. NHÁNH TỰ LẮP RÁP (ARCH)", context="Linux-1.2a.arch")

    row1_2a_top = join_horizontal([b1_2a_deb, b1_2a_ent, b1_2a_arch], ["  ", "  "], context="Linux-1.2a.top")
    row1_2a_bot = [l.rstrip() for l in make_box([
        "[1] UBUNTU ('Xe máy quốc dân IT') : Cập nhật 6 tháng/lần + bản LTS (5–12 năm) cho Cloud, Data & AI/ML",
        "[2] LINUX MINT ('Ngôi nhà ấm áp') : Giao diện Cinnamon giống Windows 7/10, cài sẵn Office, VLC, Codecs",
        "[3] KALI LINUX ('Đồ nghề Hacker') : Cài sẵn hàng trăm công cụ PenTest (Wireshark, Nmap) cho bảo mật",
    ], inner_width=103, header="BA BẢN PHÂN PHỐI PHÁI SINH PHỔ BIẾN TỪ NHÁNH DEBIAN", context="Linux-1.2a.bot")]

    d1_2a = "\n".join(
        row1_2a_top
        + [
            "                 │ (Phái sinh 3 hương vị chuyên biệt từ nền tảng Debian)",
            "                 ▼",
        ]
        + row1_2a_bot
    )

    # 1.2b: Giải phẫu Cấu trúc 4 Lớp bên trong một Bản phân phối (Distro Anatomy)
    b1_2b_left = make_box([
        "[Lớp 4] Giao diện & Ứng dụng (GUI / Server CLI)",
        " • Desktop: GNOME (Ubuntu), Cinnamon (Mint)",
        " • Server : Không cài GUI (0 MB rác), thuần SSH",
        "[Lớp 3] Trình quản lý gói (Package Manager)",
        " • Tự động tải & giải quyết phụ thuộc (apt/dnf)",
        "[Lớp 2] Hệ thống Khởi động & Bộ công cụ GNU",
        " • systemd (PID 1) + glibc + Bash + Coreutils",
        "[Lớp 1] Hạt nhân Linux Kernel + Device Drivers",
    ], inner_width=47, header="1. CẤU TRÚC 4 LỚP BÊN TRONG MỘT DISTRO", context="Linux-1.2b.left")

    b1_2b_right = make_box([
        "• Đánh đổi 1 — Tiện lợi đóng gói sẵn:",
        "  Linux Mint (cài sẵn Office/VLC) vs. Kali",
        "  (cài sẵn Nmap/Wireshark) vs. Arch (tự lắp)",
        "• Đánh đổi 2 — Bảo hành thương mại 24/7:",
        "  RHEL (Thu phí Subscription) vs. Cộng đồng mở",
        "• Đánh đổi 3 — Chuẩn cân bằng cho Kỹ sư:",
        "  Ubuntu LTS: Miễn phí 100%, nhân gọn nhẹ,",
        "  kho gói AI/Cloud lớn nhất -> Chọn chuẩn!",
    ], inner_width=47, header="2. BA ĐÁNH ĐỔI KHI CHỌN DISTRO VẬN HÀNH app.log", context="Linux-1.2b.right")
    d1_2b = "\n".join(join_horizontal([b1_2b_left, b1_2b_right], ["     "], {4: [" ──> "]}, context="Linux-1.2b"))

    # 1.3a: Giải phẫu Luồng chạy Cơ bản (Basic Flow) trong "Căn bếp Linux"
    b1_3a_left = make_box([
        "[TẦNG 3 & 2: USER SPACE (Ring 3)]",
        " Giao tiếp, Thông dịch & Ứng dụng:",
        " • Phân cấp rõ 3 khái niệm:",
        "   Shell (Xe hơi nói chung)",
        "    └─> Bash (Xe Mec/BMW thuộc GNU)",
        "         └─> Bash Script (Tự động)",
        " • Process chạy trong vùng nhớ cách ly;",
        "   bị cấm chạm thẳng vào ổ cứng / CPU",
        "───────────────────┬───────────────────",
        "                ▼ (Ranh giới Syscall)",
        "[TẦNG 1: KERNEL SPACE (Ring 0)]",
        " • Linux Kernel: Bếp trưởng tối cao",
        " • Nắm quyền sinh sát & cấp phát phần",
        "   cứng dưới đáy (File, CPU, RAM, Net)",
    ], inner_width=39, header="1. KIẾN TRÚC 3 TẦNG (SLIDE & RING)", context="Linux-1.3a.left")

    b1_3a_right = make_box([
        "[1] TERMINAL (Quầy lễ tân): Nhận 'grep ERROR app.log'",
        "         │",
        "         ▼",
        "[2] SHELL / BASH (Người nhận việc): Tách lệnh & tham số",
        "         │",
        "         ▼",
        "[3] PROGRAM (Công thức tĩnh trên đĩa): File /bin/grep",
        "         │  (Shell gọi fork() + execve() nạp lên RAM)",
        "         ▼",
        "[4] PROCESS (Đầu bếp đang làm): Cần đọc file app.log",
        "         │",
        "         ▼",
        "[5] SYSTEM CALL (Phiếu xin tài nguyên: open, read)",
        "         └──> [6] LINUX KERNEL (Xét đường dẫn & quyền)",
    ], inner_width=55, header='2. LUỒNG CƠ HỌC 7 BƯỚC "CĂN BẾP LINUX"', context="Linux-1.3a.right")

    tier1_3a_top = join_horizontal([b1_3a_left, b1_3a_right], ["     "], {9: [" ──> "]}, context="Linux-1.3a.top")
    tier1_3a_bot = [l.rstrip() for l in make_box([
        "[7] PHẦN CỨNG VẬT LÝ (HARDWARE RESOURCES DO LINUX KERNEL TRỰC TIẾP ĐIỀU PHỐI):",
        " • [ FILE (Sổ ghi dữ liệu: app.log) ]        • [ CPU (Não thực hiện phép tính so khớp) ]",
        " • [ RAM (Bộ nhớ tạm giữ Process & Buffer) ] • [ NETWORK (Kênh trao đổi gói tin máy khác) ]",
    ], inner_width=103, header="3. TẦNG ĐÁY VẬT LÝ — 4 TÀI NGUYÊN PHẦN CỨNG DƯỚI QUYỀN KIỂM SOÁT CỦA KERNEL", context="Linux-1.3a.bot")]

    d1_3a = "\n".join(
        tier1_3a_top
        + [
            "                     │                                                       │",
            "                     ▼                                                       ▼",
        ]
        + tier1_3a_bot
    )

    # 1.3b: Phân định Ranh giới Trách nhiệm trong Chiến dịch grep ERROR app.log
    b1_3b_left = make_box([
        "[BƯỚC 1] Bạn gõ lệnh ở Terminal:",
        "         $ grep ERROR app.log",
        "[BƯỚC 2] Shell (Bash) phân tích cú pháp:",
        "         • Lệnh: grep | Mẫu: ERROR | File: log",
        "[BƯỚC 3] Khởi tạo Process từ Program (grep):",
        "         • Công thức grep thành Process sống",
        "         • [!] NỖI ĐAU: Process bị cấm tự thò",
        "               tay xuống ổ cứng lấy app.log!",
        "[BƯỚC 4] Gửi phiếu System Call (open, read)",
        "         xin Kernel mở & đọc dữ liệu app.log",
    ], inner_width=47, header="1. ĐÁNH THỨC PROCESS & TRÌNH PHIẾU SYSCALL", context="Linux-1.3b.left")

    b1_3b_right = make_box([
        "[BƯỚC 5] Phân chia trách nhiệm (ĐIỂM CỐT TỬ):",
        " • TRÁCH NHIỆM CỦA KERNEL (Thủ kho phần cứng):",
        "   Kiểm tra đường dẫn + quyền đọc, mở kho lấy",
        "   khối byte từ app.log đưa lên RAM cho grep.",
        "   (Kernel KHÔNG HỀ BIẾT chữ 'ERROR' là gì!)",
        " • TRÁCH NHIỆM CỦA PROCESS (Đầu bếp lao động):",
        "   Bản thân grep dùng CPU tự dò từng dòng trên",
        "   RAM để lọc ra dòng chứa chữ 'ERROR'.",
        "[BƯỚC 6] Đẩy kết quả khớp về lại màn hình",
        "         Terminal cho người dùng (qua write)!",
    ], inner_width=47, header="2. PHÂN ĐỊNH RANH GIỚI KERNEL VS. PROCESS", context="Linux-1.3b.right")
    d1_3b = "\n".join(join_horizontal([b1_3b_left, b1_3b_right], ["     "], {5: [" ──> "]}, context="Linux-1.3b"))

    # 2.1a: Giải phẫu 5 Thuộc tính Căn cước Process & Quy trình 3 Bước của Shell (Slide 26)
    b2_1a_left = make_box([
        "Khi bạn gõ: $ grep ERROR app.log",
        "[1] PARSE & EXPAND (Phân tách & Bung ký tự):",
        "    • Tách lệnh 'grep', mẫu 'ERROR', file 'app.log'",
        "    • Nếu gõ *.log -> Shell bung thành app.log,...",
        "[2] SEARCH $PATH (Tra danh bạ tìm Program):",
        "    • Quét biến $PATH (/usr/local/bin:/usr/bin:/bin)",
        "    • Định vị trúng tệp nhị phân: /bin/grep",
        "[3] TRANSLATE TO SYSCALLS (fork + execve):",
        "    • Nhân bản tiến trình con & nạp /bin/grep",
        "    • Truyền tham số: execve('/bin/grep', ...)",
    ], inner_width=52, header="1. BA BƯỚC SHELL ĐÁNH THỨC PROCESS (SLIDE 26)", context="Linux-2.1a.left")

    b2_1a_right = make_box([
        "HỒ SƠ CĂN CƯỚC PROCESS (task_struct TRONG KERNEL):",
        "[1] PID & PPID      : PID = 4321 (Cha Bash = 1024)",
        "[2] User / Group    : UID = 1000 (dev), GID = 4(adm)",
        "    (Quyết định quyền được chạm vào tệp nào)",
        "[3] Working Dir(cwd): /var/log (Nơi Process đứng;",
        "    dùng để giải mã đường dẫn tương đối 'app.log')",
        "[4] Environment     : PATH=/usr/bin:/bin, HOME=...",
        "    (Kế thừa biến môi trường từ tiến trình cha)",
        "[5] Open Files (FD) : 0(stdin), 1(stdout), 2(stderr)",
        "    + FD 3 -> trỏ tới tệp '/var/log/app.log'",
    ], inner_width=52, header="2. NĂM THUỘC TÍNH CĂN CƯỚC CỦA MỘT PROCESS", context="Linux-2.1a.right")
    d2_1a = "\n".join(join_horizontal([b2_1a_left, b2_1a_right], ["     "], {5: [" ──> "]}, context="Linux-2.1a"))

    # 2.1b: Giải mã Chuỗi 10 Ký tự Phân quyền ls -l & Phép chiếu Quyền hạn của Kernel
    b2_1b_left = make_box([
        "Kết quả lệnh: $ ls -lh /var/log/app.log",
        "  -  rw-  r--  ---   1  root  adm  1.5G Mar 23 app.log",
        " [1] [2]  [3]  [4]      [5]   [6]   [7]",
        " • [1] Loại File : '-' = File thường | 'd' = Thư mục",
        " • [2] User (u)  : rw- (Chủ sở hữu root: Đọc + Ghi)",
        " • [3] Group (g) : r-- (Nhóm adm: Chỉ được Đọc)",
        " • [4] Others (o): --- (Người lạ: Cấm hoàn toàn!)",
        " • [5–7] Chủ = root | Nhóm = adm | Dung lượng = 1.5G",
    ], inner_width=54, header="1. GIẢI MÃ CHUỖI PHÂN QUYỀN ls -l (SLIDE 28)", context="Linux-2.1b.left")

    b2_1b_right = make_box([
        "KHI PROCESS grep (UID=dev, GID=adm) GỌI open():",
        " • Bước 1: So khớp Chủ sở hữu (User)?",
        "   UID(dev) != Owner(root) ──> Không áp dụng 'rw-'",
        " • Bước 2: So khớp Nhóm (Group)?",
        "   GID(adm) == Group(adm)  ──> Áp dụng cụm 'r--'!",
        "   [+] Có chữ 'r' (Read) -> Kernel MỞ KHO thành công!",
        " • Bước 3: Nếu User khách (UID=guest, GID=guest)?",
        "   Rơi vào cụm Others '---' -> Lỗi Permission denied!",
    ], inner_width=54, header="2. PHÉP CHIẾU QUYỀN HẠN TRONG LINUX KERNEL", context="Linux-2.1b.right")
    d2_1b = "\n".join(join_horizontal([b2_1b_left, b2_1b_right], ["     "], {4: [" ──> "]}, context="Linux-2.1b"))

    # 2.2a: Triết lý "Everything is a file" & Tầng trừu tượng VFS (Slide 19)
    b2_2a_left = make_box([
        "[1] REGULAR FILES (Tệp dữ liệu thường -):",
        "    • VD: /var/log/app.log, document.txt, script.sh",
        "[2] DIRECTORIES (Thư mục d — File đặc biệt):",
        "    • Chứa danh sách tên các file khác & số Inode",
        "[3] DEVICE INTERFACES (Thiết bị phần cứng b/c):",
        "    • VD: /dev/sda (Ổ cứng), /dev/usb0, /dev/null",
        "[4] PROCESSES (Thông tin tiến trình trên RAM):",
        "    • VD: /proc/1234/status, /proc/meminfo, cpuinfo",
    ], inner_width=51, header="1. BỐN THỰC THỂ HÓA THÀNH FILE (SLIDE 19)", context="Linux-2.2a.left")

    b2_2a_right = make_box([
        "TẦNG VIRTUAL FILE SYSTEM (VFS) TRONG KERNEL:",
        " • Cung cấp 1 bộ System Call duy nhất cho tất cả:",
        "   open() ──> read() / write() ──> close()",
        "─────────────────────────┬─────────────────────────",
        "                         ▼",
        "SỨC MẠNH THỰC CHIẾN CHO KỸ SƯ (UNIFIED INTERFACE):",
        " • Dùng CÙNG 1 BỘ LỆNH (cat, grep, cp, echo) để:",
        "   [+] Đọc log trên đĩa : grep ERROR /var/log/app.log",
        "   [+] Soi RAM/CPU sống : cat /proc/meminfo",
        "   [+] Sao lưu ổ cứng   : cp /dev/sda1 backup.img",
    ], inner_width=53, header="2. GIAO DIỆN ĐỒNG NHẤT QUA TẦNG VFS KERNEL", context="Linux-2.2a.right")
    d2_2a = "\n".join(join_horizontal([b2_2a_left, b2_2a_right], ["     "], {4: [" ──> "]}, context="Linux-2.2a"))

    # 2.2b: Giải phẫu Cơ học Directory & Inode (Fun Fact Slide 19 + Bản chất mv / rm)
    b2_2b_left = make_box([
        "FUN FACT (SLIDE 19): THƯ MỤC CHỈ LÀ BẢNG ÁNH XẠ!",
        " Thư mục '/var/log/' không trực tiếp nhốt nội dung",
        " của tệp, mà chỉ là 1 bảng gồm 2 cột:",
        " ┌──────────────────────┬───────────────────────┐",
        " │ Tên hiển thị (Name)  │ Mã số Inode (Con trỏ) │",
        " ├──────────────────────┼───────────────────────┤",
        " │ app.log              │ Inode #98102          │",
        " │ syslog               │ Inode #98105          │",
        " └──────────────────────┴───────────────────────┘",
        "         └──> Trỏ tới Inode #98102 (Chứa quyền rwx,",
        "              1.5 GB, và địa chỉ các Block ổ cứng)",
    ], inner_width=53, header="1. BẢN CHẤT DIRECTORY = BẢNG (FILENAME -> INODE)", context="Linux-2.2b.left")

    b2_2b_right = make_box([
        "HỆ QUẢ CƠ HỌC KHI THAO TÁC FILE (SLIDE 35–37):",
        " • Lệnh đổi tên (mv app.log old.log cùng thư mục):",
        "   Chỉ sửa dòng chữ 'app.log' -> 'old.log' trong bảng",
        "   thư mục (Giữ nguyên Inode #98102, tốn 0 giây I/O!)",
        " • Lệnh sao chép (cp app.log backup.log):",
        "   Cấp Inode mới #99200 + Copy toàn bộ 1.5 GB trên đĩa",
        " • Lệnh xóa (rm app.log — Slide 37):",
        "   Gỡ dòng 'app.log' khỏi bảng (unlink) & giải phóng",
        "   Inode ngay lập tức -> KHÔNG CÓ Recycle Bin!",
        "   [!] CẤM TUYỆT ĐỐI: rm -rf / (Xóa trắng cả HĐH!)",
    ], inner_width=54, header="2. TẠI SAO mv SIÊU NHANH CÒN rm KHÔNG KHÔI PHỤC ĐƯỢC?", context="Linux-2.2b.right")
    d2_2b = "\n".join(join_horizontal([b2_2b_left, b2_2b_right], ["     "], {5: [" ──> "]}, context="Linux-2.2b"))

    # 2.3a: Bản đồ Kho hàng — Cây Thư mục Hợp nhất / (Slide 20, 21, 22)
    b2_3a_top = [l.rstrip() for l in make_box([
        "                                      [ / ] (ROOT FOLDER — CỬA CHÍNH DUY NHẤT)",
        "                 ┌──────────────────────┴──────────────────┬──────────────────────────────────────┐",
        "                 ▼                                         ▼                                      ▼",
        "   [1. USER-RELATED FOLDERS]                   [2. SYSTEM FOLDERS]                 [3. TEMPORARY & VARIABLE]",
    ], inner_width=109, header="BẢN ĐỒ CÂY THƯ MỤC HỢP NHẤT LINUX (THE LINUX FILE SYSTEM HIERARCHY — SLIDE 20, 21, 22)", context="Linux-2.3a.top")]

    b2_3a_c1 = make_box([
        "• /home : Nhà riêng từng User",
        "  VD: /home/fsds, /home/dev",
        "  (Giống C:\\Users trên Windows)",
        "• /root : Phủ riêng của Admin",
        "  (Tách khỏi /home để bảo mật;",
        "   chỉ tài khoản root vào được)",
        "• Đường dẫn viết tắt:",
        "  Ký hiệu '~' = Home hiện tại",
    ], inner_width=33, header="1. KHU NHÀ Ở USER (SLIDE 22)", context="Linux-2.3a.c1")

    b2_3a_c2 = make_box([
        "• /bin  : Lệnh cơ bản (ls,cp,grep)",
        "• /sbin : Lệnh Admin (reboot,fdisk)",
        "• /usr  : Phần mềm (/usr/bin: git,",
        "  python, gcc; /usr/local: tự cài)",
        "• /etc  : Cấu hình (/etc/passwd,",
        "  /etc/hosts, /etc/ssh/sshd_config)",
        "• /proc : Thông tin Process & RAM",
        "  (Virtual FS = 0 MB trên ổ cứng!)",
    ], inner_width=35, header="2. KHU HỆ THỐNG (SLIDE 21)", context="Linux-2.3a.c2")

    b2_3a_c3 = make_box([
        "• /tmp : Bàn nháp tạm thời",
        "  Ai cũng ghi được; tự động xóa",
        "  sạch khi khởi động lại (Reboot)",
        "• /var : Dữ liệu biến đổi liên tục",
        "  ├─ /var/log : Nhật ký (app.log)",
        "  ├─ /var/www : Web (Nginx/Apache)",
        "  └─ /var/lib : CSDL (PostgreSQL)",
        "  [!] Nơi tệp app.log sinh sống!",
    ], inner_width=35, header="3. KHU TẠM & BIẾN ĐỔI (SLIDE 22)", context="Linux-2.3a.c3")

    d2_3a = "\n".join(
        b2_3a_top
        + [
            "                 │                                         │                                      │",
            "                 ▼                                         ▼                                      ▼",
        ]
        + join_horizontal([b2_3a_c1, b2_3a_c2, b2_3a_c3], ["   ", "   "], context="Linux-2.3a.bot")
    )

    # 2.3b: Đối chiếu Đa gốc Windows (C:\, D:\) vs. Cây hợp nhất Linux (/) & Tuyệt đối vs. Tương đối
    b2_3b_left = make_box([
        "1. WINDOWS (Đa gốc — Chia theo Ổ đĩa vật lý):",
        "   [Ổ SSD 1] ──> C:\\Windows\\System32",
        "   [Ổ SSD 2] ──> D:\\Logs\\app.log",
        "   [!] NỖI ĐAU: Đổi ổ đĩa làm gãy toàn bộ đường dẫn!",
        "────────────────────────────────────────────────────",
        "2. LINUX (Một gốc '/' duy nhất — Gắn kết Mount):",
        "   [Ổ SSD 1] ──(mount)──> / (Gốc hệ thống)",
        "   [Ổ SSD 2] ──(mount)──> /var/log (Nhánh chứa log)",
        "   [+] Lắp ổ cứng 10 TB mới vào '/var/log': Đường dẫn",
        "       '/var/log/app.log' trong code KHÔNG HỀ ĐỔI!",
    ], inner_width=53, header="1. ĐỐI CHIẾU WINDOWS (C:\\, D:\\) VS. LINUX (/)", context="Linux-2.3b.left")

    b2_3b_right = make_box([
        "Đang đứng tại: pwd = /home/fsds (Hoặc /var)",
        "1. ĐƯỜNG DẪN TUYỆT ĐỐI (Absolute Path):",
        "   • Luôn bắt đầu bằng dấu gạch chéo gốc '/'",
        "   • VD: grep ERROR /var/log/app.log",
        "   • [+] Đứng ở đâu chạy cũng trúng đích 100%!",
        "2. ĐƯỜNG DẪN TƯƠNG ĐỐI (Relative Path):",
        "   • Tính từ vị trí đứng hiện tại (Working Dir):",
        "     '.' = Thư mục hiện tại | '..' = Lên 1 cấp cha",
        "   • Nếu đứng ở '/var': gõ log/app.log",
        "   • [!] Chạy trong Cronjob dễ lỗi nếu lệch cwd!",
    ], inner_width=53, header="2. ĐƯỜNG DẪN TUYỆT ĐỐI VS. TƯƠNG ĐỐI (SLIDE 29–30)", context="Linux-2.3b.right")
    d2_3b = "\n".join(join_horizontal([b2_3b_left, b2_3b_right], ["     "], {5: [" ──> "]}, context="Linux-2.3b"))

    # 2.4a: Bộ công cụ Điều hướng & Thao tác File trên Cây thư mục (Slide 27–37)
    b2_4a_left = make_box([
        "[1] ĐỊNH VỊ ĐANG ĐỨNG ĐÂU (pwd — Slide 30):",
        "    $ pwd  ──> /home/magnusdtd/Downloads/test",
        "[2] QUAN SÁT XUNG QUANH (ls — Slide 28):",
        "    • ls -l  : Xem chi tiết quyền rwx, chủ, ngày",
        "    • ls -lh : Dung lượng dễ đọc (1.5K, 2.4G)",
        "    • ls -a  : Hiện cả file ẩn bắt đầu bằng dấu '.'",
        "    • ls -t  : Sắp xếp file mới sửa nhất lên đầu",
        "[3] DI CHUYỂN NHANH (cd — Slide 29):",
        "    • cd ~ (Về nhà) | cd .. (Lên cha) | cd - (Quay lại)",
    ], inner_width=55, header="1. NHÓM ĐIỀU HƯỚNG: pwd, ls, cd (SLIDE 28–30)", context="Linux-2.4a.left")

    b2_4a_right = make_box([
        "[1] KHỞI TẠO (touch & mkdir — Slide 33–34):",
        "    • touch new.log : Tạo file rỗng (nếu chưa có)",
        "    • mkdir -p a/b/c: Tạo liền mạch cả cây thư mục cha",
        "[2] SAO CHÉP (cp — Slide 31–32):",
        "    • cp app.log bak.log | cp -r folder1 folder2",
        "[3] DI CHUYỂN / ĐỔI TÊN (mv — Slide 35–36):",
        "    • Cùng thư mục = Đổi tên | Khác thư mục = Di chuyển",
        "[4] XÓA VĨNH VIỄN (rm — Slide 37):",
        "    • rm file | rm -r folder (Xóa hẳn, 0 thùng rác!)",
    ], inner_width=55, header="2. THAO TÁC FILE: touch, mkdir, cp, mv, rm (SLIDE 31–37)", context="Linux-2.4a.right")
    d2_4a = "\n".join(join_horizontal([b2_4a_left, b2_4a_right], ["     "], {5: [" ──> "]}, context="Linux-2.4a"))

    # 2.4b: Chiến thuật Soi & Săn lùng File Nhật ký Lớn app.log (Slide 38–44)
    b2_4b_left = make_box([
        "Tệp mục tiêu: /var/log/app.log (Đang phình 5 GB)",
        " • [1] head -n 20 app.log (Slide 39):",
        "       Chỉ cắt đúng 20 dòng ĐẦU TIÊN (Mặc định: 10)",
        " • [2] cat app.log (Slide 38):",
        "       Đổ TOÀN BỘ file ra màn hình (Chỉ dùng cho",
        "       file nhỏ; dùng cho file 5 GB sẽ treo máy!)",
        " • [3] tail -n 20 app.log & tail -f (Slide 40):",
        "       Lấy 20 dòng CUỐI CÙNG; cờ 'tail -f' giữ luồng",
        "       mở để xem dòng log mới bắn ra REAL-TIME!",
    ], inner_width=53, header="1. CHIẾN THUẬT SOI FILE LOG: head vs. cat vs. tail -f", context="Linux-2.4b.left")

    b2_4b_right = make_box([
        "KHI KHO /var/log BÁO ĐẦY Ổ ĐĨA (SLIDE 41–44):",
        " • [1] Thống kê dung lượng thư mục (du -sh *):",
        "       $ du -sh /var/log/*  ──> Chỉ mặt thư mục ngốn GB",
        " • [2] Truy lùng file log khổng lồ > 1 GB (find):",
        "       $ find /var/log -name '*.log' -size +1G",
        " • [3] Lọc & Biến đổi chuỗi hàng loạt (grep & sed):",
        "       $ sed 's/unix/linux/g' geekfile.txt (Slide 44)",
        " • [4] Tra cứu từ điển gốc ngay tại chỗ (man):",
        "       $ man ls | man grep (Bấm 'q' để thoát — Slide 41)",
    ], inner_width=56, header="2. BỘ TỨ SĂN LÙNG & XỬ LÝ: du, find, sed, man", context="Linux-2.4b.right")
    d2_4b = "\n".join(join_horizontal([b2_4b_left, b2_4b_right], ["     "], {5: [" ──> "]}, context="Linux-2.4b"))

    # 3.1a: Giải phẫu 3 Cổng Tiêu chuẩn (stdin 0, stdout 1, stderr 2)
    b3_1a_in = make_box([
        " • Nguồn dữ liệu đầu vào:",
        "   - Bàn phím (Keyboard)",
        "   - File dữ liệu (< file)",
        "   - Đường ống Pipe (|)",
        " • Đi vào cổng số 0 (stdin)",
        "   của Process đang chạy.",
        " • Process đọc dòng byte",
        "   mà không cần biết nguồn.",
    ], inner_width=34, header="1. ĐẦU VÀO: stdin (FD 0)", context="Linux-3.1a.in")
    b3_1a_proc = make_box([
        " • Bảng File Descriptor (FD):",
        "   - [Cổng 0] stdin  (Nhập liệu)",
        "   - [Cổng 1] stdout (Kết quả sạch)",
        "   - [Cổng 2] stderr (Báo cáo lỗi)",
        " • Ví dụ: grep ERROR app.log",
        "   Đọc từ FD 0 hoặc file,",
        "   xử lý độc lập bên trong",
        "   không gian nhớ của Process.",
    ], inner_width=38, header="2. PROCESS ĐANG CHẠY (TIẾN TRÌNH)", context="Linux-3.1a.proc")
    b3_1a_out = make_box([
        " • [Cổng 1] stdout (FD 1):",
        "   Xuất kết quả bình thường",
        "   ra Màn hình / Pipe / File.",
        " ──────────────────────────────",
        " • [Cổng 2] stderr (FD 2):",
        "   Thông báo lỗi đi đường riêng!",
        "   Không bao giờ trộn lẫn",
        "   làm bẩn dữ liệu ở Cổng 1.",
    ], inner_width=36, header="3. ĐẦU RA: stdout (1) & stderr (2)", context="Linux-3.1a.out")
    d3_1a = "\n".join(join_horizontal([b3_1a_in, b3_1a_proc, b3_1a_out], [" ──> ", " ──> "], {3: [" ──> ", " ──> "], 7: ["     ", " ──> "]}, context="Linux-3.1a"))

    # 3.1b: Cơ chế Phối hợp Đa tiến trình qua Đường ống Pipe giữa Shell và Kernel
    b3_1b_p1 = make_box([
        " • Chỉ làm việc riêng của nó:",
        "   (Ví dụ: grep ERROR app.log)",
        " • Hút dữ liệu từ [stdin: 0]",
        " • Đẩy kết quả sạch ra",
        "   cổng [stdout: 1] ────────────>",
        " • Nếu gặp lỗi (Permission):",
        "   Xả qua [stderr: 2] đi",
        "   đường riêng ra màn hình!",
    ], inner_width=36, header="1. PROCESS 1 (Ví dụ: grep)", context="Linux-3.1b.p1")
    b3_1b_pipe = make_box([
        " • SHELL (Thợ lắp ống):",
        "   Đấu nối cổng stdout (1) của",
        "   Process 1 vào stdin (0) P2.",
        " • KERNEL (Giữ ống Pipe RAM):",
        "   ═══════════════> ════════════>",
        "   Truyền dòng byte trực tiếp",
        "   trên bộ đệm RAM (64 KB),",
        "   không tốn Disk I/O ghi tạm!",
    ], inner_width=38, header="2. SHELL ĐẤU NỐI & KERNEL PIPE", context="Linux-3.1b.pipe")
    b3_1b_p2 = make_box([
        " • Chỉ làm việc riêng của nó:",
        "   (Ví dụ: wc -l đếm số dòng)",
        " • Hút dòng byte sạch từ",
        "   đường ống Pipe qua [stdin: 0]",
        " • Không bị nhiễm bẩn bởi",
        "   thông báo lỗi của Process 1",
        " • Xuất tổng số dòng ra",
        "   cổng [stdout: 1] / [stderr: 2]",
    ], inner_width=36, header="3. PROCESS 2 (Xử lý tiếp)", context="Linux-3.1b.p2")
    d3_1b = "\n".join(join_horizontal([b3_1b_p1, b3_1b_pipe, b3_1b_p2], [" ──> ", " ──> "], {5: [" ──> ", " ──> "]}, context="Linux-3.1b"))

    # 3.2a: Giải phẫu Cơ học Cú pháp Điều hướng >> /var/log/backup.log 2>&1
    b3_2a_left = make_box([
        " • Khi chạy ngầm lúc 03:00 sáng (không có Terminal):",
        "   $ /home/nam/tu_dong_backup.sh",
        " • Luồng kết quả bình thường [stdout: 1]:",
        "   ──> Không có màn hình hiển thị ──> MẤT DẤU VẾT!",
        " • Luồng báo lỗi [stderr: 2] (Network/Disk Error):",
        "   ──> Không có màn hình hiển thị ──> MẤT DẤU VẾT!",
        " • Hậu quả: Sáng hôm sau kỹ sư mở máy thấy",
        "   bản sao lưu thất bại nhưng MÙ TỊT nguyên nhân!",
    ], inner_width=56, header="[X] TRẠNG THÁI 1: CHẠY NGẦM MẶC ĐỊNH (BẪY MÙ LỖI)", context="Linux-3.2a.left")
    b3_2a_right = make_box([
        " • Cú pháp chuẩn: >> /var/log/backup.log 2>&1",
        " • Bước 1 (>> /var/log/backup.log):",
        "   Hướng cổng [stdout: 1] ghi nối đuôi vào file log.",
        " • Bước 2 (2>&1 — gọi hệ thống dup2(1, 2)):",
        "   Bẻ cổng báo lỗi [stderr: 2] chập chung vào",
        "   đúng đường ống của cổng [&1] (đang trỏ vào file).",
        " • Kết quả: Cả kết quả bình thường (1) lẫn báo lỗi (2)",
        "   đều nằm gọn trong /var/log/backup.log theo giờ!",
    ], inner_width=56, header="[V] TRẠNG THÁI 2: ĐIỀU HƯỚNG THU GOM LOG (2>&1)", context="Linux-3.2a.right")
    d3_2a = "\n".join(join_horizontal([b3_2a_left, b3_2a_right], ["     "], {5: [" ──> "]}, context="Linux-3.2a"))

    # 3.2b: Ma trận Toán tử Điều hướng I/O (>, >>, <, << EOF, 2>, 2>&1 — Slide 55)
    b3_2b_left = make_box([
        " • [1] Ghi đè từ đầu (> file):",
        "       Xóa trắng nội dung cũ trước khi ghi stdout (1).",
        " • [2] Ghi nối đuôi (>> file):",
        "       Giữ nguyên lịch sử cũ, ghi tiếp vào cuối file.",
        " • [3] Đọc đầu vào từ file (< file):",
        "       Bơm nội dung file vào cổng stdin (0).",
        " • [4] Đọc khối văn bản nhiều dòng (<< EOF):",
        "       Here-Document bơm nhiều dòng vào stdin (0).",
    ], inner_width=56, header="1. ĐIỀU HƯỚNG ĐẦU RA & ĐẦU VÀO (SLIDE 55)", context="Linux-3.2b.left")
    b3_2b_right = make_box([
        " • [5] Tách riêng luồng lỗi (2> error.log):",
        "       Chỉ bắt cổng stderr (2) ghi vào file lỗi riêng.",
        " • [6] Gộp luồng lỗi vào luồng chuẩn (2>&1):",
        "       Chập cổng 2 vào đích hiện tại của cổng 1.",
        " • [!] Cạm bẫy thứ tự (Order Trap — TLPI Ch. 5.5):",
        "   - ĐÚNG: >> app.log 2>&1 (Cổng 1 vào file, 2 theo 1)",
        "   - SAI : 2>&1 >> app.log (Cổng 2 trỏ màn hình cũ,",
        "           sau đó cổng 1 mới rẽ vào file -> Lỗi lọt sổ!)",
    ], inner_width=56, header="2. ĐIỀU HƯỚNG LỖI & CẠM BẪY THỨ TỰ 2>&1", context="Linux-3.2b.right")
    d3_2b = "\n".join(join_horizontal([b3_2b_left, b3_2b_right], ["     "], {5: [" ──> "]}, context="Linux-3.2b"))

    # 4.0: Phối hợp Nhịp nhàng giữa Bộ ba Công cụ Tự động hóa trong Linux
    b4_0_s1 = make_box([
        " • Đóng gói hàng chục câu lệnh",
        "   rời rạc vào 1 file kịch bản.",
        " • Trả lời câu hỏi cơ học:",
        "   'CẦN LÀM NHỮNG BƯỚC NÀO?'",
        " • Tự động kiểm tra if/else,",
        "   lặp qua danh sách server.",
    ], inner_width=36, header="[1] SHELL SCRIPT (.sh)", context="Linux-4.0.s1")
    b4_0_s2 = make_box([
        " • Đối chiếu thời gian sửa file",
        "   (mtime) giữa mã nguồn & đích.",
        " • Trả lời câu hỏi cơ học:",
        "   'FILE NÀO VỪA SỬA, CÓ CẦN",
        "    BIÊN DỊCH LẠI KHÔNG?'",
        " • Tránh biên dịch thừa vô ích.",
    ], inner_width=38, header="[2] MAKE (Makefile)", context="Linux-4.0.s2")
    b4_0_s3 = make_box([
        " • Tiến trình ngầm crond canh",
        "   đồng hồ hệ thống 24/7.",
        " • Trả lời câu hỏi cơ học:",
        "   'KHI NÀO BẮT ĐẦU KÍCH HOẠT?'",
        " • Đúng 02:00 sáng tự động gọi",
        "   Script & Make chạy ngầm.",
    ], inner_width=36, header="[3] CRONJOB (crond)", context="Linux-4.0.s3")
    d4_0 = "\n".join(join_horizontal([b4_0_s1, b4_0_s2, b4_0_s3], [" ──> ", " ──> "], {4: [" ──> ", " ──> "]}, context="Linux-4.0"))

    # 4.1a: Sơ đồ Phân cấp giữa Shell, Bash và Bash Scripting
    b4_1a_left = make_box([
        " • [Cấp 1] SHELL (Khái niệm chung = 'Xe hơi'):",
        "   Chương trình thông dịch lệnh giữa Người & Kernel",
        "   (gồm nhiều dòng: sh, bash, zsh, fish — Slide 46).",
        " • [Cấp 2] BASH (Bourne-Again SHell = 'Xe Mec/BMW'):",
        "   Loại Shell mặc định phổ biến nhất thuộc dự án GNU.",
        " • [Cấp 3] BASH SCRIPTING ('Tờ giấy dán tủ lạnh'):",
        "   Ghi sẵn chuỗi lệnh + biến + if/for vào file .sh",
        "   để Bash đọc từ đầu đến cuối và thực thi hàng loạt!",
    ], inner_width=56, header="1. PHÂN CẤP: SHELL ──> BASH ──> BASH SCRIPT", context="Linux-4.1a.left")
    b4_1a_right = make_box([
        " • Dòng 1: #!/bin/bash (Shebang chỉ định /bin/bash)",
        " • Biến  : TEN=\"Nam\" (Cấm khoảng trắng quanh dấu =)",
        " • Nhánh : if [ -f \"$FILE\" ]; then ... else ... fi",
        " • Lặp   : for SERVER in server1 server2 server3; do..",
        " • Hai cách chạy kịch bản (Slide 51):",
        "   - Cách 1: $ bash backup.sh (gọi trực tiếp bash)",
        "   - Cách 2: $ chmod +x backup.sh && ./backup.sh",
        "             (cấp quyền thực thi x rồi chạy độc lập)",
    ], inner_width=56, header="2. GIẢI PHẪU KỊCH BẢN MẪU backup.sh (SLIDE 51–58)", context="Linux-4.1a.right")
    d4_1a = "\n".join(join_horizontal([b4_1a_left, b4_1a_right], ["     "], {5: [" ──> "]}, context="Linux-4.1a"))

    # 4.1b: Trình Soạn thảo CLI (Nano vs Vim) & Cú pháp Bash Thực chiến (Slide 48–63)
    b4_1b_left = make_box([
        " • NANO (Đơn giản, hiện phím tắt ở đáy — Slide 48):",
        "   - Ctrl+O (^O): Lưu file  | Ctrl+X (^X): Thoát",
        "   - Ctrl+K (^K): Cắt dòng  | Ctrl+U (^U): Dán dòng",
        " • VIM (Mạnh mẽ, chia 3 chế độ — Slide 49–50):",
        "   - Normal Mode (mặc định khi mở): Di chuyển, xóa",
        "   - Bấm 'i' ──> Insert Mode (gõ sửa nội dung code)",
        "   - Bấm 'ESC' ──> quay về Normal Mode",
        "   - Gõ ':wq' (Lưu & thoát) hoặc ':q!' (Thoát hủy sửa)",
    ], inner_width=56, header="1. SOẠN THẢO CLI: NANO VS. VIM (SLIDE 48–50)", context="Linux-4.1b.left")
    b4_1b_right = make_box([
        " • [!] Cạm bẫy so sánh chuỗi vs số (Slide 56):",
        "   - [[ 10 > 9 ]] ──> FALSE! (So chữ cái '1' < '9')",
        "   - (( 10 > 9 )) ──> TRUE!  (So sánh số học chuẩn)",
        " • Mảng (Arrays — Slide 60): my_array=(10 2 300)",
        "   - Phần tử đầu: ${my_array[0]} | Cuối: ${my_array[-1]}",
        "   - Tổng số phần tử: ${#my_array[@]}",
        " • Hàm & Mã thoát (Functions — Slide 61–62):",
        "   - Đối số $1, $2 | Biến local | Mã thoát $? (0 = OK)",
    ], inner_width=56, header="2. SỐ HỌC (( )), MẢNG & HÀM BASH (SLIDE 56–63)", context="Linux-4.1b.right")
    d4_1b = "\n".join(join_horizontal([b4_1b_left, b4_1b_right], ["     "], {5: [" ──> "]}, context="Linux-4.1b"))

    # 4.2a: Dây chuyền Biên dịch Mã nguồn C sang Mã máy của GCC (Slide 64–67)
    b4_2a_left = make_box([
        " • Mã nguồn C/C++ (chao.c / demo2.cpp — Slide 65):",
        "   Con người đọc hiểu (#include, int main, printf).",
        " • [Bước 1] Pre-processor (.c ──> .i):",
        "   Bung các chỉ thị #include, xóa comment, macro.",
        " • [Bước 2] Compiler (.i ──> .s):",
        "   Dịch mã C đã tiền xử lý sang hợp ngữ Assembly.",
        " • [Bước 3] Assembler (.s ──> .o):",
        "   Đúc thành file mã máy trung gian (Object file .o).",
    ], inner_width=56, header="1. BỐN BƯỚC BIÊN DỊCH CỦA GCC (SLIDE 65–67)", context="Linux-4.2a.left")
    b4_2a_right = make_box([
        " • [Bước 4] Linker (Ghép các file .o + Thư viện):",
        "   $ gcc chao.c -o chuong_trinh_chao",
        "   Liên kết main.o + ham_phu.o + libc thành Binary!",
        " • Kiểm tra định dạng file thực thi (Slide 66):",
        "   $ file chuong_trinh_chao",
        "   ──> ELF 64-bit LSB shared object, x86-64...",
        " • Chạy trực tiếp trên CPU với tốc độ tối đa:",
        "   $ ./chuong_trinh_chao",
    ], inner_width=56, header="2. LINKER & FILE THỰC THI ELF 64-BIT (SLIDE 66)", context="Linux-4.2a.right")
    d4_2a = "\n".join(join_horizontal([b4_2a_left, b4_2a_right], ["     "], {5: [" ──> "]}, context="Linux-4.2a"))

    # 4.2b: Cơ chế Quyết định Thông minh của Make dựa trên Makefile (Slide 68–71)
    b4_2b_left = make_box([
        " • Cấu trúc quy tắc trong Makefile (Slide 69):",
        "   target: prerequisites",
        "   <TAB>recipe",
        " • Ví dụ thực tế:",
        "   ung_dung: main.o ham_phu.o",
        "       gcc main.o ham_phu.o -o ung_dung",
        " • [!] LUẬT THÉP: Dòng lệnh Recipe BẮT BUỘC thụt lề",
        "   bằng phím [TAB] (dùng Space sẽ báo lỗi ngay!).",
    ], inner_width=58, header="1. CẤU TRÚC MAKEFILE & LUẬT PHÍM [TAB]", context="Linux-4.2b.left")
    b4_2b_right = make_box([
        " • Cơ chế so sánh Timestamp (mtime) của Make:",
        "   - main.c vừa sửa (10:05) > main.o (09:00) ──> DỊCH LẠI",
        "   - ham_phu.c (08:00) < ham_phu.o (09:00)  ──> BỎ QUA!",
        " • Khai báo nhãn tác vụ .PHONY (Slide 71):",
        "   .PHONY: all clean build test run deploy",
        "   Giúp lệnh 'make clean' (rm -f *.o ung_dung) luôn",
        "   chạy kể cả khi trùng tên file thật trong thư mục.",
        " • Tái sử dụng biến: CXX = g++ / $(CXX) (Slide 71).",
    ], inner_width=58, header="2. SO SÁNH TIMESTAMP & NHÃN .PHONY (SLIDE 70–71)", context="Linux-4.2b.right")
    d4_2b = "\n".join(join_horizontal([b4_2b_left, b4_2b_right], ["     "], {5: [" ──> "]}, context="Linux-4.2b"))

    # 4.3a: Giải phẫu 5 Trường Thời gian của Crontab (Từ Nhỏ đến Lớn — Slide 73–74)
    b4_3a_left = make_box([
        " • [1] Cron    : Hệ thống lập lịch tự động trên Linux.",
        " • [2] Crontab : Bảng thời gian biểu (file cấu hình)",
        "   - crontab -e (Sửa) | crontab -l (Xem) | -r (Xóa)",
        " • [3] Cronjob : Từng dòng công việc cụ thể hẹn giờ.",
        " • [4] Crond   : Tiến trình ngầm (Daemon) trực 24/7,",
        "   thức dậy đúng mỗi 60 giây để rà bảng Crontab.",
    ], inner_width=56, header="1. BỐN KHÁI NIỆM: CRON, CRONTAB, CRONJOB, CROND", context="Linux-4.3a.left")
    b4_3a_right = make_box([
        " • Cú pháp: [Phút] [Giờ] [Ngày] [Tháng] [Thứ] <Lệnh>",
        "   - Trường 1: Phút (0 - 59)  | Trường 2: Giờ (0 - 23)",
        "   - Trường 3: Ngày (1 - 31)  | Trường 4: Tháng (1 - 12)",
        "   - Trường 5: Thứ  (0 - 6 hoặc 0 - 7, CN = 0 hoặc 7)",
        " • 4 Ký tự điều khiển (Slide 73):",
        "   * (Mọi giá trị) | , (Danh sách: 1,3,5) |",
        "   - (Khoảng: 1-5) | / (Bước nhảy: */5 = mỗi 5 phút).",
    ], inner_width=56, header="2. NĂM DẤU SAO (* * * * *) TỪ NHỎ ĐẾN LỚN", context="Linux-4.3a.right")
    d4_3a = "\n".join(join_horizontal([b4_3a_left, b4_3a_right], ["     "], {4: [" ──> "]}, context="Linux-4.3a"))

    # 4.3b: Vòng lặp Quét 60 Giây của Crond, 3 Cạm bẫy & 2 Giới hạn Cốt tử (Slide 72–76)
    b4_3b_left = make_box([
        " • Chu kỳ 60s của crond ──> Khớp giờ ──> Kích hoạt!",
        " • 3 Cạm bẫy làm Cronjob 'chết im lặng' lúc nửa đêm:",
        "   1. Quên đường dẫn tuyệt đối (/usr/bin/python3,",
        "      /home/nam/backup.sh) vì $PATH của Cron cực hẹp.",
        "   2. Quên thu gom log (>> /var/log/backup.log 2>&1)",
        "      khiến lỗi từ cổng stderr (2) biến mất vô hình.",
        "   3. Đặt nhầm sổ Crontab (crontab -e của User thường",
        "      vs sudo crontab -e của Root dẫn đến thiếu quyền).",
    ], inner_width=56, header="1. CHU KỲ CROND 60S & 3 CẠM BẪY KINH ĐIỂN", context="Linux-4.3b.left")
    b4_3b_right = make_box([
        " • [Giới hạn 1] No Auto-Retry (Slide 75):",
        "   Nếu mạng chập chờn làm lệnh lỗi, Cron KHÔNG tự",
        "   chạy lại! ──> Giải pháp: Bọc vòng lặp Retry 3 lần",
        "   trong Bash Script (for i in 1 2 3; do ... sleep 60).",
        " • [Giới hạn 2] Missed Jobs khi máy tắt (Slide 75–76):",
        "   Máy sập nguồn lúc 02:00 ──> Bỏ lỡ lịch, không bù!",
        "   ──> Giải pháp: Dùng Anacron hoặc systemd Timers",
        "       (tự chạy bù khi bật máy, tích hợp journald).",
    ], inner_width=56, header="2. HAI GIỚI HẠN CỦA CRONJOB & GIẢI PHÁP (SLIDE 75–76)", context="Linux-4.3b.right")
    d4_3b = "\n".join(join_horizontal([b4_3b_left, b4_3b_right], ["     "], {5: [" ──> "]}, context="Linux-4.3b"))

    diagrams = {
        "0.1": {"ascii": d0_1, "kind": "boxes"},
        "0.2": {"ascii": d0_2, "kind": "boxes"},
        "1.1a": {"ascii": d1_1a, "kind": "boxes"},
        "1.1b": {"ascii": d1_1b, "kind": "boxes"},
        "1.2a": {"ascii": d1_2a, "kind": "boxes"},
        "1.2b": {"ascii": d1_2b, "kind": "boxes"},
        "1.3a": {"ascii": d1_3a, "kind": "boxes"},
        "1.3b": {"ascii": d1_3b, "kind": "boxes"},
        "2.1a": {"ascii": d2_1a, "kind": "boxes"},
        "2.1b": {"ascii": d2_1b, "kind": "boxes"},
        "2.2a": {"ascii": d2_2a, "kind": "boxes"},
        "2.2b": {"ascii": d2_2b, "kind": "boxes"},
        "2.3a": {"ascii": d2_3a, "kind": "boxes"},
        "2.3b": {"ascii": d2_3b, "kind": "boxes"},
        "2.4a": {"ascii": d2_4a, "kind": "boxes"},
        "2.4b": {"ascii": d2_4b, "kind": "boxes"},
        "3.1a": {"ascii": d3_1a, "kind": "boxes"},
        "3.1b": {"ascii": d3_1b, "kind": "boxes"},
        "3.2a": {"ascii": d3_2a, "kind": "boxes"},
        "3.2b": {"ascii": d3_2b, "kind": "boxes"},
        "4.0": {"ascii": d4_0, "kind": "boxes"},
        "4.1a": {"ascii": d4_1a, "kind": "boxes"},
        "4.1b": {"ascii": d4_1b, "kind": "boxes"},
        "4.2a": {"ascii": d4_2a, "kind": "boxes"},
        "4.2b": {"ascii": d4_2b, "kind": "boxes"},
        "4.3a": {"ascii": d4_3a, "kind": "boxes"},
        "4.3b": {"ascii": d4_3b, "kind": "boxes"},
    }
    for k, meta in diagrams.items():
        errs = verify_diagram(meta["ascii"], f"Linux-{k}", kind=meta["kind"])
        if errs:
            raise SystemExit(f"ASCII verification failed for Linux-{k} ({meta['kind']}): {errs}")
    return diagrams



HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>FSDS · EDAI · DSAI — Tài liệu Học tập Kỹ thuật</title>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='4' fill='%23181716'/%3E%3Cpath d='M8 10h16M8 16h10M8 22h13' stroke='%23D97757' stroke-width='2.5'/%3E%3C/svg%3E" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600..800;1,9..144,600&family=Noto+Serif:ital,wght@0,600..800;1,600&family=Plus+Jakarta+Sans:ital,wght@0,400..700;1,400..600&display=swap&subset=vietnamese" rel="stylesheet" />
  <style>
  __FONT_FACES__

  /* ==========================================================================
     1. 3-TIER TYPOGRAPHY & COLOR TOKENS (DISPLAY · SANS · MONO + GLASSMORPHISM)
     ========================================================================== */
  :root {
    color-scheme: dark;
    --bg: #181716;
    --surface: #1E1D1B;
    --surface-subtle: #252321;
    --surface-hover: #2C2A27;
    --ink: #ECEAE2;
    --ink-bold: #FAF9F5;
    --ink-secondary: #C8C4B7;
    --muted: #9A968C;
    --selection-bg: #32302C;
    --line: #2E2C29;
    --line-strong: #45423D;
    --accent: #D97757;
    --accent-strong: #C96442;
    --accent-soft: rgba(217, 119, 87, 0.12);

    --glossary-surface: rgba(24, 25, 30, 0.78);
    --glossary-border: rgba(255, 255, 255, 0.15);
    --glossary-highlight: rgba(255, 255, 255, 0.11);
    --glossary-shadow: 0 24px 56px rgba(0, 0, 0, 0.65), 0 6px 18px rgba(0, 0, 0, 0.42);
    --glossary-underline: rgba(217, 119, 87, 0.56);
    --glossary-intuition-bg: rgba(6, 182, 212, 0.10);
    --glossary-intuition-border: rgba(6, 182, 212, 0.35);
    --glossary-badge-bg: rgba(217, 119, 87, 0.16);
    --glossary-badge-text: #F59E7A;

    --rail-width: 310px;
    --header-height: 48px;
    --page-gutter: clamp(28px, 3.5vw, 52px);
    --article-max: 1760px;
    --reading-measure: 100%;
    --motion-duration: 180ms;
    --motion-ease: cubic-bezier(0.22, 1, 0.36, 1);

    --font-display: "Fraunces", "Noto Serif", "New York", "Charter", Georgia, serif;
    --font-sans: "Plus Jakarta Sans", "Avenir Next", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-mono: "SFMono-Regular", "SF Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  }

  html.light {
    color-scheme: light;
    --bg: #FAF9F5;
    --surface: #F4F1EA;
    --surface-subtle: #EBE7DD;
    --surface-hover: #E2DDD1;
    --ink: #181716;
    --ink-bold: #0D0C0B;
    --ink-secondary: #3D3B36;
    --muted: #68645B;
    --selection-bg: #E8DFD1;
    --line: #DFDBD0;
    --line-strong: #C4BFB2;
    --accent: #C96442;
    --accent-strong: #A84C2C;
    --accent-soft: rgba(201, 100, 66, 0.10);

    --glossary-surface: rgba(250, 249, 245, 0.84);
    --glossary-border: rgba(24, 23, 22, 0.16);
    --glossary-highlight: rgba(255, 255, 255, 0.80);
    --glossary-shadow: 0 22px 50px rgba(24, 23, 22, 0.18), 0 4px 14px rgba(24, 23, 22, 0.08);
    --glossary-underline: rgba(201, 100, 66, 0.55);
    --glossary-intuition-bg: rgba(8, 145, 178, 0.08);
    --glossary-intuition-border: rgba(8, 145, 178, 0.30);
    --glossary-badge-bg: rgba(201, 100, 66, 0.13);
    --glossary-badge-text: #A84C2C;
  }

  * {
    box-sizing: border-box;
  }

  ::selection {
    background: var(--selection-bg);
    color: var(--ink-bold);
  }

  html, body {
    margin: 0;
    padding: 0;
    background: var(--bg);
    color: var(--ink);
    font-family: var(--font-sans);
    font-size: 17px;
    line-height: 1.72;
    letter-spacing: -0.004em;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  button, input, select, textarea {
    font-family: var(--font-sans);
    letter-spacing: -0.004em;
  }

  code, pre, kbd, samp {
    font-family: var(--font-mono);
    letter-spacing: 0;
    font-variant-ligatures: none;
    font-feature-settings: "liga" 0, "calt" 0;
  }

  h1, h2, h3, h4 {
    font-family: var(--font-display);
    color: var(--ink-bold);
  }

  strong, b {
    font-weight: 650;
    color: var(--ink-bold);
  }

  a {
    color: var(--accent);
    text-decoration: underline;
    text-underline-offset: 3px;
  }
  a:hover {
    color: var(--ink-bold);
  }

  :where(button, a, input, summary, [tabindex]):focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
  }

  /* ==========================================================================
     2. TOP PROGRESS BAR & MINIMAL CONTEXTUAL TOPBAR (ZERO ICON CLUTTER)
     ========================================================================== */
  .progress-track {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: transparent;
    z-index: 100;
    pointer-events: none;
  }
  .progress-bar {
    height: 100%;
    width: 0%;
    background: var(--accent);
    transition: width 0.1s linear;
  }

  .topbar {
    position: sticky;
    top: 0;
    z-index: 60;
    height: var(--header-height);
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    align-items: center;
    gap: 12px;
    padding: 0 16px;
    background: var(--bg);
    border-bottom: 1px solid var(--line);
    line-height: 1.25;
  }

  .topbar-context {
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 0;
  }

  .topbar-actions {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
  }

  .ui-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    height: 30px;
    padding: 0 10px;
    font-size: 12px;
    font-weight: 500;
    line-height: 1.25;
    color: var(--ink-secondary);
    background: transparent;
    border: 1px solid var(--line);
    border-radius: 3px;
    cursor: pointer;
    text-decoration: none;
    white-space: nowrap;
    transition: background 0.12s, border-color 0.12s, color 0.12s;
  }
  .ui-btn:hover {
    background: var(--surface-subtle);
    border-color: var(--line-strong);
    color: var(--ink-bold);
  }
  .ui-btn[aria-expanded="true"],
  .ui-btn.active {
    border-color: var(--line-strong);
    color: var(--ink-bold);
  }

  kbd.shortcut-key {
    display: inline-block;
    padding: 1px 4px;
    font-size: 10.5px;
    line-height: 1.15;
    color: var(--muted);
    border: 1px solid var(--line);
    border-radius: 2px;
  }

  .breadcrumbs {
    display: flex;
    align-items: center;
    gap: 7px;
    margin: 0;
    padding: 0;
    list-style: none;
    min-width: 0;
    font-size: 12px;
    line-height: 1.25;
    overflow: hidden;
  }
  .crumb-item {
    display: flex;
    align-items: center;
    min-width: 0;
    white-space: nowrap;
    color: var(--muted);
  }
  .crumb-sep {
    color: var(--muted);
    opacity: 0.55;
    user-select: none;
  }
  .crumb-topic {
    color: var(--ink-secondary);
  }
  .crumb-current {
    color: var(--ink-bold);
    font-weight: 600;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* ==========================================================================
     3. APP GRID LAYOUT & SIDEBAR RAIL (DESKTOP VS MOBILE SEPARATED)
     ========================================================================== */
  .layout {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    min-height: calc(100vh - var(--header-height));
  }

  .rail-slot {
    min-width: 0;
  }

  .rail {
    background: var(--surface);
    border-right: 1px solid var(--line);
    height: calc(100vh - var(--header-height));
    overflow-y: auto;
    overscroll-behavior: contain;
    padding: 14px 12px 48px;
    line-height: 1.25;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  @media (min-width: 901px) {
    .layout {
      grid-template-columns: var(--rail-width) minmax(0, 1fr);
      transition: grid-template-columns var(--motion-duration) var(--motion-ease);
    }
    .rail-slot {
      position: sticky;
      top: var(--header-height);
      height: calc(100vh - var(--header-height));
      overflow: hidden;
    }
    .rail {
      width: var(--rail-width);
      transition: transform var(--motion-duration) var(--motion-ease), opacity 140ms linear;
    }
    body.rail-collapsed .layout {
      grid-template-columns: 0px minmax(0, 1fr);
    }
    body.rail-collapsed .rail {
      transform: translateX(-16px);
      opacity: 0;
      pointer-events: none;
      border-right-color: transparent;
    }
  }

  .rail-top-bar {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .rail-brand-title {
    padding: 0 4px;
    font-size: 12px;
    font-weight: 700;
    color: var(--ink-bold);
    letter-spacing: 0.02em;
  }
  .rail-search-btn {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 7px 10px;
    background: var(--bg);
    border: 1px solid var(--line);
    border-radius: 3px;
    color: var(--muted);
    font-size: 12px;
    line-height: 1.25;
    cursor: pointer;
    transition: border-color 0.12s, color 0.12s;
  }
  .rail-search-btn:hover {
    border-color: var(--line-strong);
    color: var(--ink-bold);
  }

  /* In-Page Station Outline */
  .rail-outline-section {
    border-top: 1px solid var(--line);
    border-bottom: 1px solid var(--line);
    padding: 10px 0;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .rail-section-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 4px;
    font-size: 11px;
    font-weight: 600;
    color: var(--muted);
  }
  .rail-outline-list {
    display: flex;
    flex-direction: column;
    gap: 1px;
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .rail-outline-link {
    display: grid;
    grid-template-columns: 44px minmax(0, 1fr);
    align-items: baseline;
    gap: 6px;
    padding: 5px 6px;
    font-size: 12px;
    line-height: 1.3;
    color: var(--ink-secondary);
    text-decoration: none;
    border-left: 2px solid transparent;
    transition: background 0.12s, color 0.12s, border-color 0.12s;
  }
  .rail-outline-link:hover {
    background: var(--surface-subtle);
    color: var(--ink-bold);
  }
  .rail-outline-link[aria-current="location"] {
    color: var(--ink-bold);
    font-weight: 600;
    border-left-color: var(--accent);
    background: var(--surface-subtle);
  }
  .rail-outline-code {
    font-size: 11px;
    color: var(--muted);
  }
  .rail-outline-link[aria-current="location"] .rail-outline-code {
    color: var(--accent);
  }

  /* Collapsible Track Accordions */
  .track-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .track-group {
    border-bottom: 1px solid var(--line);
    padding-bottom: 4px;
  }
  .track-trigger {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 7px 4px;
    background: transparent;
    border: 0;
    color: var(--ink-bold);
    font-size: 12px;
    font-weight: 600;
    line-height: 1.25;
    text-align: left;
    cursor: pointer;
  }
  .track-trigger:hover {
    color: var(--accent);
  }
  .track-indicator {
    color: var(--muted);
    font-size: 12px;
    font-weight: 400;
    flex-shrink: 0;
  }
  .track-panel-wrap {
    display: grid;
    grid-template-rows: 0fr;
    transition: grid-template-rows var(--motion-duration) var(--motion-ease);
  }
  .track-group[data-expanded="true"] .track-panel-wrap {
    grid-template-rows: 1fr;
  }
  .track-panel-inner {
    min-height: 0;
    overflow: hidden;
  }
  .track-items {
    padding: 2px 0 6px;
    display: flex;
    flex-direction: column;
    gap: 1px;
  }

  .rail-item {
    display: grid;
    grid-template-columns: 34px minmax(0, 1fr) auto;
    align-items: baseline;
    gap: 6px;
    width: 100%;
    text-align: left;
    padding: 5px 6px;
    border: 0;
    border-left: 2px solid transparent;
    background: transparent;
    color: var(--ink-secondary);
    font-size: 12px;
    line-height: 1.3;
    cursor: pointer;
    transition: background 0.12s, color 0.12s;
  }
  .rail-item:hover {
    background: var(--surface-subtle);
    color: var(--ink-bold);
  }
  .rail-item[aria-current="page"] {
    background: var(--surface-subtle);
    color: var(--ink-bold);
    font-weight: 600;
    border-left-color: var(--accent);
  }
  .rail-code {
    font-size: 11px;
    color: var(--muted);
  }
  .rail-item[aria-current="page"] .rail-code {
    color: var(--accent);
  }
  .rail-item-title {
    min-width: 0;
    overflow-wrap: break-word;
  }
  .rail-item-note {
    font-size: 10.5px;
    color: var(--accent);
  }

  /* ==========================================================================
     4. ADAPTIVE EDITORIAL GRID (78CH PROSE + FULL-WIDTH BREAKOUT VISUALS)
     ========================================================================== */
  .main-view {
    min-width: 0;
    padding: 32px var(--page-gutter) 110px;
  }
  .article-wrap {
    width: 100%;
    max-width: var(--article-max);
    margin-inline: auto;
  }

  .lesson-header {
    margin-bottom: 28px;
    padding-bottom: 18px;
    border-bottom: 1px solid var(--line);
  }
  .lesson-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: 12px;
    line-height: 1.25;
    color: var(--muted);
    margin-bottom: 8px;
  }
  .lesson-title {
    font-family: var(--font-display);
    font-size: clamp(32px, 3.2vw, 44px);
    font-weight: 800;
    line-height: 1.18;
    letter-spacing: -0.022em;
    color: var(--ink-bold);
    margin: 0 0 14px;
  }
  .lesson-lead {
    font-family: var(--font-sans);
    font-size: clamp(18px, 1.35vw, 19.5px);
    color: var(--ink-secondary);
    line-height: 1.66;
    max-width: 82ch;
    margin: 0 0 22px;
  }

  /* Scalable Stage Switcher Bar + Collapsible Directory (handles 5 to 50+ stages cleanly) */
  .stage-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding: 9px 12px;
    background: var(--surface);
    border: 1px solid var(--line);
    font-size: 13px;
    line-height: 1.35;
  }
  .stage-bar-current {
    display: flex;
    align-items: baseline;
    gap: 8px;
    min-width: 0;
  }
  .stage-bar-idx {
    font-family: var(--font-mono);
    color: var(--accent);
    font-weight: 700;
    flex-shrink: 0;
  }
  .stage-bar-title {
    color: var(--ink-bold);
    font-weight: 600;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .stage-bar-actions {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
  }
  .stage-directory {
    display: none;
    border: 1px solid var(--line);
    border-top: 0;
    background: var(--bg);
    max-height: 280px;
    overflow-y: auto;
  }
  .stage-directory.open {
    display: block;
  }
  .stage-dir-item {
    display: grid;
    grid-template-columns: 72px minmax(0, 1fr) auto;
    align-items: baseline;
    gap: 10px;
    width: 100%;
    padding: 8px 12px;
    border: 0;
    border-bottom: 1px solid var(--line);
    background: transparent;
    color: var(--ink-secondary);
    font-size: 13px;
    line-height: 1.4;
    text-align: left;
    cursor: pointer;
  }
  .stage-dir-item:last-child {
    border-bottom: 0;
  }
  .stage-dir-item:hover {
    background: var(--surface-subtle);
    color: var(--ink-bold);
  }
  .stage-dir-item.active {
    background: var(--surface-subtle);
    color: var(--ink-bold);
    font-weight: 600;
    border-left: 2px solid var(--accent);
  }
  .stage-dir-code {
    font-family: var(--font-mono);
    color: var(--muted);
    font-size: 11.5px;
  }
  .stage-dir-item.active .stage-dir-code {
    color: var(--accent);
    font-weight: 700;
  }
  .stage-dir-meta {
    color: var(--muted);
    font-size: 11.5px;
  }

  /* Full-width Editorial Prose with Distinct Monotonic Heading Hierarchy */
  .prose {
    display: block;
    width: 100%;
  }

  .prose hr {
    border: 0;
    border-top: 1px solid var(--line);
    margin: 40px 0;
  }
  .prose :is(h2, h3, h4, .summary-section)[id] {
    scroll-margin-block-start: calc(var(--header-height) + 20px);
  }
  .prose h2 {
    font-family: var(--font-display);
    font-size: clamp(24px, 2.25vw, 31px);
    font-weight: 700;
    line-height: 1.28;
    letter-spacing: -0.015em;
    margin: 44px 0 18px;
    padding: 10px 14px 12px 16px;
    border-left: 4px solid var(--accent);
    border-bottom: 1px solid var(--line-strong);
    background: linear-gradient(90deg, var(--accent-soft) 0%, transparent 88%);
    color: var(--ink-bold);
  }
  .prose h3 {
    font-family: var(--font-display);
    font-size: clamp(20px, 1.65vw, 24px);
    font-weight: 650;
    line-height: 1.35;
    letter-spacing: -0.01em;
    margin: 28px 0 12px;
    padding-left: 12px;
    border-left: 2.5px solid rgba(217, 119, 87, 0.55);
    color: var(--ink-bold);
  }
  .prose h4 {
    font-family: var(--font-display);
    font-size: clamp(18px, 1.4vw, 20.5px);
    font-weight: 600;
    line-height: 1.4;
    margin: 20px 0 8px;
    color: var(--ink-bold);
  }
  .prose p {
    margin: 0 0 16px;
  }
  .prose ul, .prose ol {
    margin: 0 0 20px;
    padding-left: 24px;
  }
  .prose li {
    margin-bottom: 10px;
  }
  .prose li ul {
    margin-top: 6px;
  }
  .prose code {
    font-family: var(--font-mono);
    font-size: 0.90em;
    line-height: 1.3;
    padding: 2px 6px;
    background: var(--surface-subtle);
    border: 1px solid var(--line);
    border-radius: 3px;
    color: var(--ink-bold);
  }

  /* Tables */
  .table-wrap {
    overflow-x: auto;
    margin: 18px 0 26px;
    border: 1px solid var(--line);
    background: var(--surface);
  }
  table.clean-table {
    width: 100%;
    border-collapse: collapse;
    font-family: var(--font-sans);
    font-size: 14.5px;
    line-height: 1.55;
  }
  table.clean-table th,
  table.clean-table td {
    padding: 11px 14px;
    text-align: left;
    vertical-align: top;
    border-bottom: 1px solid var(--line);
  }
  table.clean-table th {
    background: var(--surface-subtle);
    font-size: 13px;
    font-weight: 650;
    color: var(--ink-bold);
  }
  table.clean-table tr:last-child td {
    border-bottom: 0;
  }

  /* ==========================================================================
     5. VISUAL SANDBOX (SINGLE-BORDER FRAME + MERMAID INTERACTIVE VIEWPORT)
     ========================================================================== */
  .visual-card {
    container-type: inline-size;
    margin: 18px 0 26px;
    border: 1px solid var(--line);
    background: var(--bg);
  }
  .visual-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding: 8px 12px;
    background: var(--surface);
    border-bottom: 1px solid var(--line);
    line-height: 1.25;
  }
  .visual-bar-title {
    font-size: 12.5px;
    font-weight: 600;
    color: var(--ink-bold);
    min-width: 0;
  }
  .visual-controls {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
  }

  .visual-segmented {
    display: inline-flex;
    align-items: center;
    border: 1px solid var(--line);
    border-radius: 3px;
    background: var(--bg);
  }
  .seg-btn {
    border: 0;
    background: transparent;
    color: var(--muted);
    font-size: 11.5px;
    font-weight: 500;
    line-height: 1.25;
    padding: 4px 9px;
    cursor: pointer;
    transition: background 0.12s, color 0.12s;
  }
  .seg-btn + .seg-btn {
    border-left: 1px solid var(--line);
  }
  .seg-btn:hover {
    color: var(--ink-bold);
  }
  .seg-btn[aria-pressed="true"] {
    background: var(--surface-subtle);
    color: var(--ink-bold);
    font-weight: 600;
  }

  .vmenu-wrap {
    position: relative;
  }
  .vmenu-popover {
    position: absolute;
    right: 0;
    top: calc(100% + 4px);
    min-width: 210px;
    background: var(--surface);
    border: 1px solid var(--line-strong);
    padding: 4px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35);
    z-index: 45;
    display: none;
    flex-direction: column;
  }
  .vmenu-popover.open {
    display: flex;
  }
  .vmenu-item {
    display: block;
    width: 100%;
    padding: 7px 10px;
    border: 0;
    background: transparent;
    color: var(--ink);
    font-size: 12px;
    line-height: 1.25;
    text-align: left;
    cursor: pointer;
  }
  .vmenu-item:hover {
    background: var(--surface-hover);
    color: var(--ink-bold);
  }
  .vmenu-sep {
    height: 1px;
    background: var(--line);
    margin: 3px 0;
  }

  .visual-panes {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
  }
  .visual-pane {
    min-width: 0;
  }
  .visual-pane[hidden] {
    display: none !important;
  }

  /* Flush Single-Level ASCII Pre (Strict Monospace Geometry Preservation Boundary) */
  pre.ascii-diagram {
    margin: 0;
    padding: 18px 20px;
    background: var(--bg);
    border: 0;
    font-family: var(--font-mono);
    font-size: clamp(11px, 0.92vw, 15px);
    font-weight: 400;
    font-style: normal;
    line-height: 1.25;
    letter-spacing: 0;
    font-variant-ligatures: none;
    font-feature-settings: "liga" 0, "calt" 0;
    color: var(--ink-bold);
    overflow-x: auto;
    white-space: pre;
    tab-size: 4;
  }
  body.rail-collapsed pre.ascii-diagram {
    font-size: clamp(12px, 0.96vw, 15.5px);
  }

  /* Interactive Mermaid Viewport (Zoom − / 100% / + / Vừa khung + Pan) */
  .mermaid-viewer {
    display: flex;
    flex-direction: column;
    background: var(--bg);
  }
  .mermaid-toolbar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 6px 12px;
    background: var(--surface-subtle);
    border-bottom: 1px solid var(--line);
    font-size: 11.5px;
    line-height: 1.25;
  }
  .mermaid-zoom-group {
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }
  .zoom-btn {
    height: 26px;
    min-width: 28px;
    padding: 0 8px;
    border: 1px solid var(--line);
    border-radius: 2px;
    background: var(--bg);
    color: var(--ink-secondary);
    font-size: 11.5px;
    line-height: 1;
    cursor: pointer;
  }
  .zoom-btn:hover {
    border-color: var(--line-strong);
    color: var(--ink-bold);
    background: var(--surface-hover);
  }
  .mermaid-hint {
    color: var(--muted);
    font-size: 11px;
  }
  .mermaid-viewport {
    position: relative;
    overflow: hidden;
    height: clamp(360px, 56vh, 620px);
    background: var(--bg);
    cursor: grab;
    user-select: none;
  }
  .mermaid-viewport.is-panning {
    cursor: grabbing;
  }
  .mermaid-transform {
    position: absolute;
    top: 0;
    left: 0;
    transform-origin: 0 0;
    will-change: transform;
  }
  .mermaid-transform svg {
    display: block;
    max-width: none !important;
    height: auto;
  }

  .mermaid-code-box {
    display: none;
    padding: 12px 16px;
    background: var(--surface);
    border-top: 1px solid var(--line);
  }
  .mermaid-code-box.show {
    display: block;
  }
  .mermaid-code-box pre {
    margin: 8px 0 0;
    padding: 12px;
    background: var(--bg);
    border: 1px solid var(--line);
    font-size: 12px;
    line-height: 1.25;
    overflow-x: auto;
  }

  /* Interactive Picture Viewport (Style #2 Dark-Slate Blueprint + Smooth Zoom/Pan + Prompt Spec) */
  .topbar-vmode-wrap {
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }
  .topbar-vmode-label {
    font-size: 11.5px;
    font-weight: 600;
    color: var(--muted);
  }
  #globalVisualModeGroup .seg-btn[aria-pressed="true"] {
    background: var(--accent);
    color: #fff;
    font-weight: 600;
  }
  .pic-viewer {
    display: flex;
    flex-direction: column;
    background: #0f1419;
  }
  .pic-toolbar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 6px 12px;
    background: var(--surface-subtle);
    border-bottom: 1px solid var(--line);
    font-size: 11.5px;
    line-height: 1.25;
  }
  .pic-meta {
    display: inline-flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 6px;
  }
  .pic-viewport {
    position: relative;
    overflow: auto;
    min-height: 360px;
    max-height: 680px;
    padding: 16px;
    background: #0f1419;
    display: flex;
    align-items: center;
    justify-content: center;
    user-select: none;
  }
  .pic-viewport.is-panning {
    cursor: grabbing;
  }
  .pic-transform {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    transform-origin: center center;
    transition: transform 0.14s ease-out;
  }
  .pic-transform img {
    display: block;
    width: 100%;
    max-width: 1120px;
    max-height: 610px;
    height: auto;
    object-fit: contain;
    border-radius: 3px;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.55);
    cursor: zoom-in;
  }
  .pic-badge {
    display: inline-flex;
    align-items: center;
    padding: 2px 7px;
    border-radius: 3px;
    font-family: var(--font-mono);
    font-size: 10.5px;
    font-weight: 600;
    letter-spacing: 0.2px;
  }
  .pic-badge.ready,
  .pic-badge.arch {
    background: rgba(6, 182, 212, 0.16);
    color: #22d3ee;
    border: 1px solid rgba(6, 182, 212, 0.4);
  }
  .pic-badge.template,
  .pic-badge.story {
    background: rgba(245, 158, 11, 0.16);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.4);
  }
  .pic-prompt-box {
    display: none;
    padding: 12px 16px;
    background: var(--surface);
    border-top: 1px solid var(--line);
  }
  .pic-prompt-box.show {
    display: block;
  }
  .pic-prompt-head {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: 12px;
  }
  .pic-prompt-box pre {
    margin: 8px 0 0;
    padding: 12px;
    background: var(--bg);
    border: 1px solid var(--line);
    font-size: 12px;
    line-height: 1.35;
    white-space: pre-wrap;
    word-break: break-word;
    overflow-x: auto;
  }

  /* Spine Hero Mindmap Card in TRẠM 0.0 */
  .spine-hero-card {
    margin: 20px 0 24px;
    border: 1px solid var(--line-strong);
    background: #0f1419;
    border-radius: 4px;
    overflow: hidden;
  }
  .spine-hero-header {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 8px 14px;
    background: var(--surface-subtle);
    border-bottom: 1px solid var(--line);
  }
  .spine-hero-badge {
    display: inline-flex;
    align-items: center;
    padding: 2px 7px;
    margin-right: 8px;
    border-radius: 3px;
    font-family: var(--font-mono);
    font-size: 10.5px;
    font-weight: 600;
    background: rgba(16, 185, 129, 0.16);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.35);
  }
  .spine-hero-title {
    font-size: 12.5px;
    font-weight: 700;
    color: var(--ink-bold);
  }
  .spine-hero-body {
    position: relative;
    background: #0f1419;
    padding: 14px;
    text-align: center;
    cursor: zoom-in;
  }
  .spine-hero-body img {
    display: block;
    width: 100%;
    max-width: 1120px;
    max-height: 560px;
    height: auto;
    object-fit: contain;
    margin: 0 auto;
    border-radius: 3px;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.55);
  }
  .spine-hero-footer {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding: 8px 14px;
    font-size: 12px;
    line-height: 1.35;
    color: var(--muted);
    background: var(--surface);
    border-top: 1px solid var(--line);
  }

  .visual-caption {
    padding: 8px 16px;
    font-size: 12px;
    line-height: 1.35;
    color: var(--muted);
    border-top: 1px solid var(--line);
    background: var(--surface);
  }

  /* Editorial Summary Section (No Card-inside-Card) */
  .summary-section {
    margin: 36px 0 24px;
    padding-top: 20px;
    border-top: 2px solid var(--line-strong);
  }
  .summary-section h2 {
    margin-top: 0;
    border-bottom: 0;
    padding-bottom: 0;
  }

  /* ==========================================================================
     6. COMMAND PALETTE MODAL (⌘K) & FULLSCREEN DIAGRAM MODAL
     ========================================================================== */
  .modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(12, 12, 11, 0.76);
    z-index: 110;
    display: none;
    align-items: flex-start;
    justify-content: center;
    padding: 6vh 16px 24px;
  }
  .modal-backdrop.open {
    display: flex;
  }

  .cmd-dialog {
    width: min(660px, 100%);
    background: var(--surface);
    border: 1px solid var(--line-strong);
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5);
    overflow: hidden;
    line-height: 1.25;
  }
  .cmd-input-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 14px;
    border-bottom: 1px solid var(--line);
    background: var(--bg);
  }
  .cmd-input {
    flex: 1;
    border: 0;
    background: transparent;
    color: var(--ink-bold);
    font-size: 14px;
    outline: none;
  }
  .cmd-results {
    max-height: 380px;
    overflow-y: auto;
    padding: 6px;
    margin: 0;
    list-style: none;
  }
  .cmd-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    width: 100%;
    padding: 8px 10px;
    border: 0;
    background: transparent;
    color: var(--ink);
    font-size: 12.5px;
    text-align: left;
    cursor: pointer;
  }
  .cmd-item:hover,
  .cmd-item.selected {
    background: var(--surface-hover);
    color: var(--ink-bold);
  }
  .cmd-item-left {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
  }
  .cmd-item-sub {
    font-size: 11px;
    color: var(--muted);
  }
  .cmd-item-kind {
    font-size: 11px;
    color: var(--muted);
    flex-shrink: 0;
  }
  .cmd-footer {
    display: flex;
    justify-content: space-between;
    padding: 8px 14px;
    font-size: 11px;
    color: var(--muted);
    background: var(--surface-subtle);
    border-top: 1px solid var(--line);
  }

  /* Fullscreen Diagram Expand Dialog */
  .expand-dialog {
    width: min(1760px, 96vw);
    height: 86vh;
    background: var(--surface);
    border: 1px solid var(--line-strong);
    box-shadow: 0 20px 48px rgba(0, 0, 0, 0.6);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  .expand-header {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding: 8px 14px;
    background: var(--surface-subtle);
    border-bottom: 1px solid var(--line);
    font-size: 12.5px;
    font-weight: 600;
  }
  .expand-body {
    flex: 1;
    min-height: 0;
    overflow: auto;
    background: var(--bg);
    display: flex;
    flex-direction: column;
  }
  .expand-body pre.ascii-diagram {
    font-size: 13.5pt;
    line-height: 1.25;
    padding: 24px;
  }
  .expand-body .mermaid-viewer {
    flex: 1;
    min-height: 0;
  }
  .expand-body .mermaid-viewport {
    flex: 1;
    height: 100%;
  }

  .toast {
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 8px 14px;
    background: var(--surface-subtle);
    border: 1px solid var(--line-strong);
    color: var(--ink-bold);
    font-size: 12px;
    line-height: 1.25;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.15s;
    z-index: 130;
  }
  .toast.show {
    opacity: 1;
  }

  /* ==========================================================================
     INTERACTIVE TECHNICAL GLOSSARY TERMS & FROSTED-GLASS POPOVER
     ========================================================================== */
  .glossary-term {
    cursor: pointer;
    position: relative;
    border-bottom: 1.5px dotted var(--glossary-underline);
    transition: color 0.14s ease, background-color 0.14s ease, border-color 0.14s ease, box-shadow 0.14s ease;
    border-radius: 3px;
  }
  strong.glossary-term {
    padding: 0 2px;
    margin: 0 -1px;
  }
  code.glossary-term {
    border-bottom: 1.5px dotted var(--accent);
  }
  .glossary-term:hover,
  .glossary-term:focus-visible,
  .glossary-term.glossary-active {
    color: var(--accent);
    background-color: var(--accent-soft);
    border-bottom-style: solid;
    border-bottom-color: var(--accent);
    outline: none;
  }
  .glossary-term.glossary-pinned {
    color: var(--accent);
    background-color: var(--accent-soft);
    border-bottom-style: solid;
    border-bottom-color: var(--accent);
    box-shadow: 0 0 0 1px var(--accent);
  }

  .glossary-popover {
    position: fixed;
    top: 0;
    left: 0;
    width: min(440px, calc(100vw - 24px));
    max-height: min(500px, calc(100vh - 32px));
    overflow-y: auto;
    z-index: 145;
    background: var(--glossary-surface);
    backdrop-filter: blur(22px) saturate(180%);
    -webkit-backdrop-filter: blur(22px) saturate(180%);
    border: 1px solid var(--glossary-border);
    box-shadow: var(--glossary-shadow), inset 0 1px 0 var(--glossary-highlight);
    border-radius: 12px;
    padding: 15px 17px 14px;
    color: var(--ink);
    font-family: var(--font-sans);
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transform: translateY(6px) scale(0.985);
    transition: opacity 0.16s cubic-bezier(0.22, 1, 0.36, 1),
                transform 0.16s cubic-bezier(0.22, 1, 0.36, 1),
                visibility 0.16s;
  }
  .glossary-popover.open {
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
    transform: translateY(0) scale(1);
  }
  .glossary-popover.pinned {
    border-color: var(--accent);
  }
  .glossary-pop-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 7px;
  }
  .glossary-pop-badges {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
    min-width: 0;
  }
  .glossary-pop-cat {
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--accent);
    background: var(--accent-soft);
    border: 1px solid var(--glossary-border);
    padding: 2px 7px;
    border-radius: 4px;
  }
  .glossary-pop-match {
    font-family: var(--font-mono);
    font-size: 10.5px;
    color: var(--muted);
    background: var(--surface-subtle);
    border: 1px solid var(--line);
    padding: 1px 6px;
    border-radius: 4px;
    max-width: 195px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .glossary-pop-actions {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
  }
  .glossary-pop-pin-state {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--muted);
  }
  .glossary-pop-pin-state.is-pinned {
    color: var(--accent);
    font-weight: 700;
  }
  .glossary-pop-close {
    appearance: none;
    border: 1px solid var(--line-strong);
    background: var(--surface-subtle);
    color: var(--ink-bold);
    width: 22px;
    height: 22px;
    border-radius: 5px;
    font-size: 11px;
    line-height: 1;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  .glossary-pop-close:hover {
    border-color: var(--accent);
    color: var(--accent);
  }
  .glossary-pop-title {
    font-family: var(--font-display);
    font-size: 18px;
    font-weight: 700;
    line-height: 1.28;
    color: var(--ink-bold);
    margin: 0 0 10px;
    letter-spacing: -0.01em;
  }
  .glossary-pop-section {
    margin-bottom: 9px;
  }
  .glossary-pop-label {
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 3px;
  }
  .glossary-pop-intuition {
    font-size: 13.5px;
    line-height: 1.54;
    color: var(--ink-bold);
    background: var(--accent-soft);
    border-left: 3px solid var(--accent);
    padding: 7px 10px;
    border-radius: 0 6px 6px 0;
  }
  .glossary-pop-mechanism {
    font-size: 12.8px;
    line-height: 1.55;
    color: var(--ink);
  }
  .glossary-pop-example {
    background: var(--code-bg);
    border: 1px solid var(--line);
    border-radius: 6px;
    padding: 7px 9px;
    margin-top: 4px;
  }
  .glossary-pop-code {
    display: block;
    font-family: var(--font-mono);
    font-size: 11.5px;
    line-height: 1.45;
    color: var(--accent);
    white-space: pre-wrap;
    word-break: break-word;
    margin-bottom: 4px;
  }
  .glossary-pop-note {
    font-size: 11.8px;
    line-height: 1.45;
    color: var(--muted);
  }
  .glossary-pop-related {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-top: 4px;
  }
  .glossary-pop-chip {
    font-family: var(--font-mono);
    font-size: 10.5px;
    color: var(--ink);
    background: var(--surface-subtle);
    border: 1px solid var(--line);
    padding: 2px 7px;
    border-radius: 4px;
    cursor: pointer;
    transition: border-color 0.12s, color 0.12s;
  }
  .glossary-pop-chip:hover {
    border-color: var(--accent);
    color: var(--accent);
  }
  .glossary-pop-foot {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding-top: 8px;
    margin-top: 6px;
    border-top: 1px solid var(--line);
    font-size: 10.5px;
    color: var(--muted);
  }

  .pic-mobile-hint {
    display: none;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 6px 10px;
    background: rgba(6, 182, 212, 0.10);
    border-top: 1px solid rgba(6, 182, 212, 0.25);
    color: var(--ink-secondary);
    font-size: 11.5px;
    line-height: 1.3;
  }
  .pic-mobile-hint button {
    appearance: none;
    border: 1px solid rgba(6, 182, 212, 0.45);
    background: rgba(6, 182, 212, 0.16);
    color: #22d3ee;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 4px;
    cursor: pointer;
    white-space: nowrap;
    flex-shrink: 0;
  }

  @media (max-width: 900px) {
    .crumb-track, .crumb-sep-track, .hide-mobile {
      display: none !important;
    }
    .rail-slot {
      position: fixed;
      top: var(--header-height);
      left: 0;
      bottom: 0;
      width: min(320px, 88vw);
      z-index: 95;
      transform: translateX(-100%);
      transition: transform var(--motion-duration) var(--motion-ease);
    }
    body.mobile-rail-open .rail-slot {
      transform: translateX(0);
      box-shadow: 12px 0 32px rgba(0, 0, 0, 0.55);
    }
    .rail {
      width: 100%;
      height: 100%;
    }
  }

  @media (max-width: 680px) {
    :root {
      --page-gutter: 12px;
      --header-height: 82px;
    }
    html, body {
      overflow-x: hidden;
    }
    /* Two-row ergonomic mobile topbar: Row 1 (Menu + Breadcrumb + Search/Theme), Row 2 (Full-width Visual Mode Switcher) */
    .topbar {
      height: auto;
      min-height: var(--header-height);
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 6px 8px;
      padding: 6px 10px;
    }
    .topbar-context {
      flex: 1 1 auto;
      min-width: 0;
      gap: 8px;
      order: 1;
    }
    .breadcrumbs {
      font-size: 11.5px;
      gap: 4px;
    }
    .crumb-topic {
      max-width: 92px;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .topbar-actions {
      width: 100%;
      order: 2;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      padding-top: 4px;
      border-top: 1px solid var(--line);
    }
    .topbar-vmode-wrap {
      flex: 1 1 auto;
      display: flex;
    }
    #globalVisualModeGroup {
      width: 100%;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
    }
    #globalVisualModeGroup .seg-btn {
      padding: 5px 4px;
      font-size: 11.5px;
      text-align: center;
    }
    #searchTriggerBtn,
    #themeToggleBtn {
      height: 28px;
      padding: 0 8px;
      font-size: 11.5px;
      flex-shrink: 0;
    }

    /* Main content & typography tuned for mobile phone screens */
    .main-view {
      padding: 18px var(--page-gutter) 96px;
    }
    .lesson-header {
      margin-bottom: 20px;
      padding-bottom: 14px;
    }
    .lesson-title {
      font-size: clamp(24px, 6.8vw, 30px);
      line-height: 1.22;
      margin-bottom: 10px;
    }
    .lesson-lead {
      font-size: 15.5px;
      line-height: 1.6;
      margin-bottom: 16px;
    }
    .prose {
      font-size: 16px;
      line-height: 1.68;
    }
    .prose h2 {
      font-size: clamp(20px, 5.4vw, 24px);
      margin: 30px 0 14px;
      padding: 8px 10px 10px 12px;
    }
    .prose h3 {
      font-size: clamp(17.5px, 4.6vw, 20px);
      margin: 22px 0 10px;
      padding-left: 10px;
    }
    .prose h4 {
      font-size: 16.5px;
    }
    .prose ul, .prose ol {
      padding-left: 18px;
    }

    /* Stage switcher bar stacked cleanly on mobile */
    .stage-bar {
      flex-direction: column;
      align-items: stretch;
      gap: 8px;
      padding: 10px;
    }
    .stage-bar-current {
      flex-wrap: wrap;
      gap: 4px 8px;
    }
    .stage-bar-title {
      white-space: normal;
      line-height: 1.35;
    }
    .stage-bar-actions {
      width: 100%;
      display: grid;
      grid-template-columns: auto auto 1fr;
      gap: 6px;
    }
    .stage-bar-actions .ui-btn {
      justify-content: center;
      height: 32px;
    }
    .stage-dir-item {
      grid-template-columns: 62px minmax(0, 1fr);
      gap: 6px;
      padding: 8px 10px;
    }
    .stage-dir-meta {
      grid-column: 2;
      font-size: 11px;
    }

    /* Visual cards & Spine Hero: full-bleed on mobile with zero horizontal overflow */
    .visual-card,
    .spine-hero-card {
      margin: 16px -6px 22px;
      border-radius: 4px;
    }
    .visual-bar {
      flex-direction: column;
      align-items: stretch;
      gap: 8px;
      padding: 8px 10px;
    }
    .visual-bar-title {
      font-size: 12.5px;
      line-height: 1.35;
    }
    .visual-controls {
      width: 100%;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 6px;
    }
    .visual-controls .visual-segmented {
      flex: 1 1 auto;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
    }
    .visual-controls .seg-btn {
      padding: 5px 6px;
      text-align: center;
    }
    .visual-controls > .ui-btn {
      height: 28px;
      padding: 0 8px;
      font-size: 11.5px;
    }

    /* Mobile Picture Viewer: eliminate 360px empty black box + enable 2x HD touch swipe pan */
    .pic-toolbar,
    .mermaid-toolbar {
      padding: 6px 8px;
      gap: 6px;
    }
    .pic-badge {
      display: none;
    }
    .pic-viewport {
      min-height: 0 !important;
      max-height: none;
      padding: 6px;
      overflow-x: auto;
      overflow-y: hidden;
      -webkit-overflow-scrolling: touch;
      touch-action: pan-x pan-y pinch-zoom;
      display: block;
    }
    .pic-transform {
      display: block;
      width: 100%;
      transform: none !important;
    }
    .pic-transform img {
      width: 100%;
      max-width: 100%;
      max-height: none;
      height: auto;
      margin: 0 auto;
      border-radius: 3px;
    }
    /* When user taps image or 'Phóng rõ 2x' on mobile, expand width to 760px for crisp horizontal touch panning */
    .pic-viewport.mobile-hd-pan {
      padding: 8px;
      background: #0b0f14;
    }
    .pic-viewport.mobile-hd-pan .pic-transform {
      width: 780px;
    }
    .pic-viewport.mobile-hd-pan .pic-transform img {
      width: 780px;
      max-width: none;
    }
    .pic-mobile-hint {
      display: flex;
    }

    /* Spine Hero Mindmap on mobile */
    .spine-hero-header {
      padding: 8px 10px;
      gap: 6px;
    }
    .spine-hero-body {
      padding: 6px;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
    }
    .spine-hero-body.mobile-hd-pan img {
      width: 780px;
      max-width: none;
    }
    .spine-hero-footer {
      padding: 8px 10px;
      font-size: 11.5px;
    }

    /* ASCII & Mermaid on mobile */
    pre.ascii-diagram {
      padding: 12px 10px;
      font-size: 11px;
      -webkit-overflow-scrolling: touch;
    }
    .mermaid-viewport {
      height: clamp(260px, 44vh, 380px);
    }

    /* Edge-to-edge Fullscreen Modal on mobile */
    .modal-backdrop {
      padding: 0;
    }
    .expand-dialog {
      width: 100vw;
      height: 100dvh;
      max-height: 100dvh;
      border: 0;
    }
    .expand-header {
      padding: 8px 10px;
      gap: 6px;
    }
    .expand-body #modalPicViewport {
      height: calc(100dvh - 96px) !important;
      max-height: none !important;
      padding: 8px;
      overflow: auto !important;
      -webkit-overflow-scrolling: touch;
      display: flex;
      align-items: center;
      justify-content: flex-start;
    }
    .expand-body #modalPicTransform {
      width: 860px;
      min-width: 860px;
    }
    .expand-body #modalPicImg {
      width: 860px;
      max-width: none;
      max-height: none;
    }

    /* Frosted-Glass Glossary Popover docked as a sleek Bottom Sheet on mobile */
    .glossary-popover {
      left: 8px !important;
      right: 8px !important;
      bottom: max(8px, env(safe-area-inset-bottom)) !important;
      top: auto !important;
      width: auto !important;
      max-height: 70dvh;
      border-radius: 16px;
      padding: 14px 15px 13px;
      transform: translateY(16px);
    }
    .glossary-popover.open {
      transform: translateY(0);
    }
    .glossary-pop-close {
      width: 28px;
      height: 28px;
      font-size: 13px;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .layout, .rail, .track-panel-wrap {
      transition: none !important;
    }
  }
  </style>
</head>
<body>
  <div class="progress-track"><div class="progress-bar" id="progressBar"></div></div>

  <header class="topbar">
    <div class="topbar-context">
      <button class="ui-btn" id="railToggleBtn" type="button" aria-label="Đóng hoặc mở mục lục (Phím [ hoặc ⌘B)" aria-controls="syllabusRail" aria-expanded="true">
        <span>Mục lục</span>
        <kbd class="shortcut-key hide-mobile">[</kbd>
      </button>
      <nav aria-label="Đường dẫn bài học" style="min-width:0;">
        <ol class="breadcrumbs" id="topbarBreadcrumbs"></ol>
      </nav>
    </div>

    <div class="topbar-actions">
      <div class="topbar-vmode-wrap" role="group" aria-label="Chế độ Visual mặc định toàn bài">
        <span class="topbar-vmode-label hide-mobile">Visual:</span>
        <div class="visual-segmented" id="globalVisualModeGroup">
          <button type="button" class="seg-btn" data-gmode="ascii" aria-pressed="true" onclick="setGlobalVisualMode('ascii')" title="Hiển thị toàn bộ sơ đồ ở chế độ ASCII">ASCII</button>
          <button type="button" class="seg-btn" data-gmode="mermaid" aria-pressed="false" onclick="setGlobalVisualMode('mermaid')" title="Hiển thị toàn bộ sơ đồ ở chế độ Mermaid">Mermaid</button>
          <button type="button" class="seg-btn" data-gmode="pic" aria-pressed="false" onclick="setGlobalVisualMode('pic')" title="Hiển thị toàn bộ sơ đồ ở chế độ Picture (Ảnh minh họa)">Picture</button>
        </div>
      </div>

      <button class="ui-btn" id="searchTriggerBtn" type="button" title="Tìm nhanh học phần, chặng hoặc trạm (⌘K hoặc /)">
        <span>Tìm kiếm</span>
        <kbd class="shortcut-key hide-mobile">⌘K</kbd>
      </button>

      <button class="ui-btn" id="themeToggleBtn" type="button" title="Chuyển chế độ màu Sáng / Tối">
        <span id="themeToggleLabel">Giao diện: Tối</span>
      </button>
    </div>
  </header>

  <div class="layout">
    <div class="rail-slot" id="railSlot">
      <aside class="rail" id="syllabusRail" aria-label="Điều hướng chương trình học"></aside>
    </div>
    <main class="main-view">
      <div class="article-wrap" id="articleContainer"></div>
    </main>
  </div>

  <!-- Command Palette Modal (⌘K / /) -->
  <div class="modal-backdrop" id="searchModal" role="dialog" aria-modal="true" aria-label="Tìm kiếm học phần và trạm kiến thức">
    <div class="cmd-dialog" onclick="event.stopPropagation()">
      <div class="cmd-input-row">
        <input type="text" class="cmd-input" id="cmdSearchInput" placeholder="Tìm học phần (D02, Spark, Kafka...), chặng hoặc trạm (Spill-to-Disk, OLTP...)" autocomplete="off" />
        <kbd class="shortcut-key">ESC</kbd>
      </div>
      <ul class="cmd-results" id="cmdResultsList"></ul>
      <div class="cmd-footer">
        <span>↑↓ Di chuyển · Enter Chọn · Esc Đóng</span>
        <span>26 Học phần · 7 Chặng Storage · 4 Chặng Linux</span>
      </div>
    </div>
  </div>

  <!-- Fullscreen Diagram Expand Modal -->
  <div class="modal-backdrop" id="expandModal" role="dialog" aria-modal="true" aria-label="Phóng to sơ đồ">
    <div class="expand-dialog" onclick="event.stopPropagation()">
      <div class="expand-header">
        <span id="expandModalTitle">Sơ đồ chi tiết</span>
        <div style="display:flex;align-items:center;gap:8px;">
          <div class="visual-segmented" role="group" aria-label="Chế độ sơ đồ phóng to">
            <button type="button" class="seg-btn" id="expandModeAsciiBtn" aria-pressed="true" onclick="setExpandModalMode('ascii')">ASCII</button>
            <button type="button" class="seg-btn" id="expandModeMermaidBtn" aria-pressed="false" onclick="setExpandModalMode('mermaid')">Mermaid</button>
            <button type="button" class="seg-btn" id="expandModePicBtn" aria-pressed="false" onclick="setExpandModalMode('pic')">Picture</button>
          </div>
          <button class="ui-btn" id="expandCopyBtn" type="button">Sao chép</button>
          <button class="ui-btn" id="expandCloseBtn" type="button">Đóng (Esc)</button>
        </div>
      </div>
      <div class="expand-body" id="expandModalBody"></div>
    </div>
  </div>

  <!-- Interactive Frosted-Glass Technical Glossary Popover -->
  <div class="glossary-popover" id="glossaryPopover" role="dialog" aria-modal="false" aria-label="Giải nghĩa thuật ngữ kỹ thuật" aria-hidden="true">
    <div class="glossary-pop-head">
      <div class="glossary-pop-badges">
        <span class="glossary-pop-cat" id="glossaryPopCat">KERNEL & OS</span>
        <span class="glossary-pop-match" id="glossaryPopMatch">inode</span>
      </div>
      <div class="glossary-pop-actions">
        <span class="glossary-pop-pin-state" id="glossaryPopPinState">Click để ghim</span>
        <button type="button" class="glossary-pop-close" id="glossaryPopCloseBtn" title="Đóng (Esc)" aria-label="Đóng bảng giải nghĩa">✕</button>
      </div>
    </div>
    <h4 class="glossary-pop-title" id="glossaryPopTitle">Tên thuật ngữ</h4>
    <div class="glossary-pop-section">
      <div class="glossary-pop-label">Hiểu nhanh trong 5 giây</div>
      <div class="glossary-pop-intuition" id="glossaryPopIntuition"></div>
    </div>
    <div class="glossary-pop-section">
      <div class="glossary-pop-label">Bản chất Kỹ thuật & Cơ chế vận hành</div>
      <div class="glossary-pop-mechanism" id="glossaryPopMechanism"></div>
    </div>
    <div class="glossary-pop-section">
      <div class="glossary-pop-label">Ví dụ thực tế trong bài</div>
      <div class="glossary-pop-example">
        <code class="glossary-pop-code" id="glossaryPopCode"></code>
        <div class="glossary-pop-note" id="glossaryPopNote"></div>
      </div>
    </div>
    <div class="glossary-pop-section" id="glossaryPopRelatedWrap">
      <div class="glossary-pop-label">Thuật ngữ liên quan trong cụm này</div>
      <div class="glossary-pop-related" id="glossaryPopRelated"></div>
    </div>
    <div class="glossary-pop-foot">
      <span>Rê chuột: xem nhanh · Click: ghim cố định</span>
      <span>ESC để đóng</span>
    </div>
  </div>

  <div class="toast" id="toastBox"></div>

  <script>
  const HUB_DATA = __HUB_DATA_JSON__;

  const SYLLABUS_GROUPS = [
    {
      id: "track-1",
      shortTitle: "I. Engineering Foundation",
      title: "I. Engineering Foundation (Slides 01–06)",
      items: [
        {
          code: "F01",
          title: "Linux Fundamentals",
          slide: "01-linux-fundamentals.pdf",
          pages: 78,
          hasContent: true,
          contentNote: "Chặng 1–4",
          slideToc: [
            "01/ Introduction to GNU/Linux",
            "02/ Bash Scripting",
            "03/ Command Line Basics",
            "04/ Compilation & Makefile",
            "05/ CronJob"
          ],
          modules: "GNU/Linux; Bash scripting; compilation & Makefile; cron job",
          lab: "Cài Ubuntu; Linux commands 101",
          stack: "Ubuntu, Bash, GNU Make, Cron"
        },
        {
          code: "F02",
          title: "Python Fundamentals",
          slide: "02-python-fundamentals.pdf",
          pages: 73,
          slideToc: [
            "01/ Introduction to Python",
            "02/ Core Syntax & Data Structure",
            "03/ Error Handling & Context Managers",
            "04/ File Handling",
            "05/ Sync vs. Async Programming"
          ],
          modules: "Python fundamentals; virtual environment; best practices; async/sync programming",
          lab: "Data crawler bằng Python",
          stack: "Python, venv, asyncio"
        },
        {
          code: "F03",
          title: "Database Fundamentals",
          slide: "03-database-fundamentals.pdf",
          pages: 70,
          slideToc: [
            "01/ Introduction to Databases",
            "02/ SQL vs NoSQL",
            "03/ SQL Command Groups (DDL / DML / DQL / DCL / TCL)",
            "04/ Cost & Performance Optimization Techniques"
          ],
          modules: "OOP for engineering; database concepts; SQL và NoSQL; DDL/DML/DQL/DCL/TCL; cost và performance optimization",
          lab: "Setup SQL database; thực hành truy vấn",
          stack: "PostgreSQL, SQLAlchemy ORM"
        },
        {
          code: "F04",
          title: "Web API",
          slide: "04-web-api.pdf",
          pages: 87,
          slideToc: [
            "01/ Introduction & Core Concepts (HTTP / Network Stack)",
            "02/ API Architectures (REST, gRPC, GraphQL, WebSocket, SSE, Webhook)",
            "03/ API Security (AAA, Basic Auth, JWT, OAuth)",
            "04/ API Performance Testing (Healthcheck, Metrics, Load/Stress Testing)",
            "05/ FastAPI Implementation"
          ],
          modules: "API architecture styles; authentication; FastAPI; validation/type enforcement; middleware; healthcheck; performance metrics",
          lab: "Implement API theo nhiều architecture styles",
          stack: "FastAPI, Locust"
        },
        {
          code: "F05",
          title: "Validation & Verification",
          slide: "05-validation-and-verification.pdf",
          pages: 70,
          slideToc: [
            "01/ Validation & Verification Model (V-Model)",
            "02/ Fundamentals of Testing (Black-box, White-box, Mutation, Hoare Logic, Symbolic Execution)",
            "03/ Testing Frameworks: pytest",
            "04/ Test-Driven Development (TDD)"
          ],
          modules: "Quality paradigms; black-box testing; white-box testing; mutation testing; Hoare logic; symbolic execution; TDD",
          lab: "Nhiều loại test cho API",
          stack: "pytest, unittest"
        },
        {
          code: "F06",
          title: "Containerization & Orchestration",
          slide: "06-containerization-and-orchestration.pdf",
          pages: 72,
          slideToc: [
            "01/ Introduction to VM and Containers",
            "02/ Docker & Architecture Design",
            "03/ Understand Different Containerization Technologies",
            "04/ Docker Commands",
            "05/ Docker Volumes and Network",
            "06/ Private Artifact Registry",
            "07/ Docker Compose",
            "08/ Guide to Build, Run, Optimize and Manage Containers"
          ],
          modules: "VM và containers; Docker architecture; container technologies; commands; volumes/network; private registry; Compose; build/run/optimize/manage",
          lab: "Dockerize API; local stack với Compose; container-based testing",
          stack: "Docker, Docker Compose"
        }
      ]
    },
    {
      id: "track-2",
      shortTitle: "II. Data Engineering",
      title: "II. Data Engineering (Slides 07–12)",
      items: [
        {
          code: "D01",
          title: "Ingestion Layer",
          slide: "07-ingestion-layer.pdf",
          pages: 45,
          slideToc: [
            "01/ Introduction & Data Architectures",
            "02/ Source Systems",
            "03/ The Kafka Ecosystem",
            "04/ Fundamentals of Kafka",
            "05/ Kafka's Challenges & Operations",
            "06/ Change Data Capture (CDC) & Debezium"
          ],
          modules: "Data architectures; source systems; Kafka ecosystem; Kafka fundamentals; Kafka operations; CDC methods",
          lab: "End-to-end CDC system",
          stack: "Kafka, Debezium, PostgreSQL"
        },
        {
          code: "D02",
          title: "Storage Layer",
          slide: "08-storage-layer.pdf",
          pages: 59,
          hasContent: true,
          contentNote: "Chặng 1–7",
          slideToc: [
            "01/ Data Warehouse & Modeling (Data Storage System, Data Warehouse, Data Modeling Techniques)",
            "02/ From Data Lake to Data Swamp",
            "03/ Lake House (Delta Lake, Apache Iceberg, Apache Hudi)",
            "04/ Multi-hop Architecture (Bronze / Silver / Gold)"
          ],
          modules: "Storage layer; data lake và data swamp; lakehouse; multi-hop architecture",
          lab: "Lakehouse from scratch",
          stack: "Delta Lake, Trino, Hive, MinIO"
        },
        {
          code: "D03",
          title: "Transformation Layer (Batch · Spark)",
          slide: "09-transformation-layer-batch.pdf",
          pages: 90,
          slideToc: [
            "01/ Why Spark",
            "02/ Architecture & Execution",
            "03/ Abstractions & APIs",
            "04/ Serialization & Memory",
            "05/ Challenges, Optimization & Tuning",
            "06/ Spark Operational Techniques"
          ],
          modules: "Spark architecture; data abstraction/API; optimization; advanced tuning; operations",
          lab: "Spark batch job xử lý data quality",
          stack: "Apache Spark"
        },
        {
          code: "D04",
          title: "Transformation Layer (Stream · Flink)",
          slide: "10-transformation-layer-ii-stream.pdf",
          pages: 75,
          slideToc: [
            "01/ Flink Overview",
            "02/ Time Semantics & Watermarks",
            "03/ Windowing and Late Data",
            "04/ Flink APIs",
            "05/ State and Fault Tolerance",
            "06/ Optimization Techniques",
            "07/ Deployment Modes"
          ],
          modules: "Notions of time; Flink APIs; windows; late data; state; fault tolerance; optimization; deployment modes",
          lab: "Stream job xử lý data quality",
          stack: "Apache Flink"
        },
        {
          code: "D05",
          title: "Consumption Layer",
          slide: "11-consumption-layer.pdf",
          pages: 63,
          slideToc: [
            "01/ Data Warehouse",
            "02/ Data Modeling",
            "03/ Dimensional Modeling",
            "04/ Slowly Changing Dimensions (SCD)",
            "05/ Data Vault",
            "06/ Inmon vs Kimball",
            "07/ OLAP Engines (ClickHouse, Pinot)",
            "08/ Feature Store",
            "09/ Feast: A Practical Feature Store"
          ],
          modules: "Dimensional modeling; SCD; OLAP engines; materialized views; feature core/view/transformation; ML integration",
          lab: "Feature store và feature processing pipeline",
          stack: "ClickHouse, Pinot, Feast"
        },
        {
          code: "D06",
          title: "Orchestration & Governance",
          slide: "12-orchestration-layer.pdf",
          pages: 63,
          slideToc: [
            "01/ Pipeline Orchestration (Motivation & Benefits)",
            "02/ Cron Job & Beyond Cron",
            "03/ Apache Airflow (Architecture, Operators, Data Passing, Administration & Scaling)",
            "04/ Data Validation, Data Contracts & Governance (DataHub)"
          ],
          modules: "Orchestration benefits; beyond cron; idempotency; backfill; dynamic pipelines; Airflow architecture/operators/data passing; administration/scaling; validation; contracts; governance",
          lab: "Deploy/administer Airflow; multi-step data/feature pipelines with lineage",
          stack: "Apache Airflow, DataHub"
        },
        {
          code: "C01",
          title: "Mini Coursework (1–2 tuần)",
          slide: null,
          pages: null,
          slideToc: [
            "01/ Kết hợp API, Database, Container, Ingestion, Storage, Transformation & Orchestration",
            "02/ Kiểm thử toàn trình (Testing & Data Quality Validation)",
            "03/ Data Lineage & Tài liệu vận hành"
          ],
          modules: "Tích hợp end-to-end data pipeline có kiểm thử, lineage và tài liệu vận hành",
          lab: "Mini Coursework Project",
          stack: "FastAPI, PostgreSQL, Docker, Kafka, Delta Lake, Spark/Flink, Airflow"
        }
      ]
    },
    {
      id: "track-3",
      shortTitle: "III. Data Science, ML & LLM",
      title: "III. Data Science, ML & LLM",
      items: [
        {
          code: "A01",
          title: "Introduction to Data Science & ML",
          slide: null,
          slideToc: ["01/ NumPy, Pandas & Matplotlib", "02/ PyTorch Fundamentals", "03/ Machine Learning & Deep Learning"],
          modules: "NumPy; Pandas; Matplotlib; PyTorch; machine learning; deep learning",
          lab: "End-to-end data science project; OCR application",
          stack: "NumPy, Pandas, Matplotlib, PyTorch"
        },
        {
          code: "A02",
          title: "Introduction to LLM, RAG & Agent",
          slide: null,
          slideToc: ["01/ Transformer Architecture & LLM", "02/ Retrieval-Augmented Generation (RAG)", "03/ AI Agents & Guardrails"],
          modules: "Transformer architecture; LLM; RAG; agents; guardrails",
          lab: "Fine-tune open-source LLM; RAG app; agentic AI system",
          stack: "LLM Stack, Vector DB, Agent Framework"
        },
        {
          code: "A03",
          title: "Model Serving Design Patterns",
          slide: null,
          slideToc: ["01/ Model Serving Patterns", "02/ Model Loading Patterns", "03/ Asynchronous Task Queue ML System"],
          modules: "Model serving patterns; model loading patterns",
          lab: "Task queue ML system",
          stack: "LLM, RabbitMQ"
        },
        {
          code: "A04",
          title: "Dive into LLM Serving",
          slide: null,
          slideToc: ["01/ KV Cache Mechanics", "02/ LLM Serving Challenges & Throughput Optimization", "03/ High-Performance Engines (vLLM, TensorRT-LLM, SGLang)"],
          modules: "KV cache; serving challenges và solutions",
          lab: "LLM serving endpoint",
          stack: "vLLM, TensorRT-LLM, SGLang"
        }
      ]
    },
    {
      id: "track-4",
      shortTitle: "IV. Distributed Platform & Cloud",
      title: "IV. Distributed Platform & Cloud",
      items: [
        {
          code: "P01",
          title: "Distributed Systems",
          slide: null,
          slideToc: ["01/ Fallacies of Distributed Computing & Scaling", "02/ CAP, PACELC, ACID vs BASE", "03/ Consensus, Replication, Sharding & Eventual Consistency"],
          modules: "Distributed systems; fallacies; vertical/horizontal scaling; stateful/stateless; partitions; packet loss; node crash; CAP; PACELC; BASE; ACID; consensus; replication; sharding; eventual consistency",
          lab: "Design exercise và failure simulation",
          stack: "Distributed Systems"
        },
        {
          code: "P02",
          title: "Kubernetes",
          slide: null,
          slideToc: ["01/ K8s Architecture & Core Workloads (Pod/Deployment/Service/Ingress/PV/PVC)", "02/ Sidecars, Init Containers & Operators", "03/ Deployment Strategies, Helm/Helmfile, Secrets & Resources"],
          modules: "K8s architecture; Pod/Deployment/Service/Ingress/PV/PVC; sidecars; init containers; operators; deployment strategies; Helm/helmfile; secrets; resources",
          lab: "Async job processing; deploy API locally on K8s",
          stack: "Kubernetes, Helm, KServe, HashiCorp Vault"
        },
        {
          code: "P03",
          title: "Kubeflow & Distributed Training",
          slide: null,
          slideToc: ["01/ Kubeflow Architecture & Operators", "02/ Distributed Training & Distributed Storage", "03/ GPU Scheduling"],
          modules: "Kubeflow architecture/operators; distributed training; distributed storage; GPU scheduling",
          lab: "Deploy Kubeflow; distributed training pipeline",
          stack: "Kubeflow"
        },
        {
          code: "P04",
          title: "Cloud Services (GCP / FinOps)",
          slide: null,
          slideToc: ["01/ Cloud Hierarchy & IAM", "02/ VPC Networking & Storage Lifecycle/Locality", "03/ GCP ML/Data Stack, IaaS/PaaS/SaaS & FinOps"],
          modules: "Cloud hierarchy/IAM; VPC/networking; storage/lifecycle/locality; GCP ML/data stack; IaaS/PaaS/SaaS; billing/FinOps",
          lab: "Free-tier GCP; Terraform infrastructure; Ansible deployment; gateway",
          stack: "GCP, NGINX"
        },
        {
          code: "P05",
          title: "Routing & Gateway",
          slide: null,
          slideToc: ["01/ Routing, Load Balancing & Service Discovery", "02/ Resiliency (Retry, Circuit Breaker, Fallback, Timeout)", "03/ AuthN/AuthZ, Rate Limits, Semantic Caching & Tracing"],
          modules: "Routing/load balancing/service discovery; retry/circuit breaker/fallback/timeout; AuthN/AuthZ; IP restriction/geofencing; PII; protocol translation; rate limits/quota/budget/prioritization; semantic caching; tracing; A/B test",
          lab: "Scenario design and gateway policy lab",
          stack: "API Gateway Stack"
        },
        {
          code: "P06",
          title: "Infrastructure as Code",
          slide: null,
          slideToc: ["01/ IaC Fundamentals", "02/ Terraform & Ansible Architecture, Commands & Best Practices", "03/ Hybrid Workflow & Drift Detection"],
          modules: "IaC fundamentals; Terraform/Ansible architecture, commands, best practices; hybrid workflow; drift detection",
          lab: "Provision and reconcile infrastructure",
          stack: "Terraform, Ansible"
        },
        {
          code: "P07",
          title: "Versioning & CI/CD",
          slide: null,
          slideToc: ["01/ Code, Data, Model & Experiment Versioning (Git/DVC/MLflow)", "02/ CI/CD & AIDE Pipelines", "03/ Jenkins, DVC & MLflow Architectures"],
          modules: "Code/data/model/experiment versioning; Git/GitHub; CI/CD; AIDE pipelines; Jenkins/DVC/MLflow architectures",
          lab: "Multiple CI/CD pipelines",
          stack: "Jenkins, DVC, MLflow"
        },
        {
          code: "P08",
          title: "Observable Systems",
          slide: null,
          slideToc: ["01/ Logs, Metrics & Distributed Traces", "02/ Observable Architecture & Drift Detection", "03/ LLM & Agent Telemetry"],
          modules: "Logs, metrics, traces; observable architecture; drift detection; LLM/agent telemetry",
          lab: "Monitoring systems",
          stack: "OpenTelemetry, Evidently, Prometheus, Grafana, ELK, Jaeger, Langfuse"
        },
        {
          code: "P09",
          title: "Misc Problems & Final Coursework",
          slide: null,
          slideToc: ["01/ Security Best Practices & SRE", "02/ Repository Design & Service Mesh", "03/ Final Coursework (2 tháng): End-to-End Data/AI System"],
          modules: "Security best practices; SRE; repository design; service mesh; Final Coursework (2 tháng)",
          lab: "Xây dựng, triển khai và vận hành hệ thống Data/AI end-to-end",
          stack: "Full Stack Data & AI"
        }
      ]
    }
  ];

  const LINUX_STAGES = [
    { id: 1, shortTitle: "Hạt nhân, Hệ sinh thái & Luồng chạy 1 lệnh", title: "Chặng 1: Hạt nhân, Hệ sinh thái GNU/Linux & Giải phẫu Luồng chạy 1 Lệnh (Trạm 1.1 ➔ 1.3)" },
    { id: 2, shortTitle: "Giải phẫu Process, Triết lý File & Cây thư mục", title: "Chặng 2: Giải phẫu Căn cước Process, Triết lý 'Everything is a file', Cây thư mục / & Bộ lệnh CLI (Trạm 2.1 ➔ 2.4)" },
    { id: 3, shortTitle: "Giao tiếp Đa tiến trình (IPC) & Điều hướng I/O", title: "Chặng 3: Giao tiếp Đa tiến trình (stdin/stdout/stderr), Đường ống Pipe & Điều hướng I/O (Trạm 3.1 ➔ 3.2)" },
    { id: 4, shortTitle: "Dây chuyền Tự động hóa: Script, Make & Cron", title: "Chặng 4: Dây chuyền Tự động hóa 24/7 — Bash Scripting, GCC/Makefile & Cronjob (Trạm 4.1 ➔ 4.3)" }
  ];

  const LINUX_CHANG1_STATIONS = [
    { id: "linux-0-map", code: "0.0", title: "Nhân vật chính & Bản đồ 4 Chặng", fullTitle: "Trạm 0.0: Nhân vật chính grep ERROR /var/log/app.log & Bản đồ Cơ học Căn bếp Linux" },
    { id: "linux-1-1", code: "1.1", title: "Bản chất GNU/Linux: Cục máy & Bộ khung", fullTitle: "Trạm 1.1: Bản chất GNU/Linux — Khi 'Cục máy' gặp 'Bộ khung' & 6 Trụ cột Server" },
    { id: "linux-1-2", code: "1.2", title: "Bản đồ Distro: Chọn dòng xe nào?", fullTitle: "Trạm 1.2: Bản đồ Distro (Bản phân phối) — Chọn 'Dòng xe' nào để chạy hệ thống?" },
    { id: "linux-1-3", code: "1.3", title: "Căn bếp Linux: 7 Bước chạy grep", fullTitle: "Trạm 1.3: Giải phẫu 'Căn bếp Linux' — Hành trình 7 bước của lệnh grep ERROR app.log" },
    { id: "linux-1-summary", code: "Kết", title: "Tóm tắt bỏ túi & Checklist Chặng 1", fullTitle: "Tóm tắt bỏ túi Chặng 1 (Mạch Nhân – Quả & Checklist 5 Câu hỏi Bản chất)" }
  ];

  const LINUX_CHANG2_STATIONS = [
    { id: "linux-2-1", code: "2.1", title: "Hồ sơ Căn cước của một Process", fullTitle: "Trạm 2.1: Giải phẫu Hồ sơ Căn cước Process (PID, User/Group, Working Directory, Environment, Open Files)" },
    { id: "linux-2-2", code: "2.2", title: "Triết lý 'Everything is a file' & Inode", fullTitle: "Trạm 2.2: Triết lý 'Everything is a file' (Regular File, Directory, Device /dev/sda, Process /proc/PID) & Cơ học Inode" },
    { id: "linux-2-3", code: "2.3", title: "Cây thư mục / & Đối chiếu Windows", fullTitle: "Trạm 2.3: Bản đồ Kho hàng — Cây thư mục Duy nhất / (/bin, /etc, /var/log, /proc 0 MB) & Đối chiếu Windows" },
    { id: "linux-2-4", code: "2.4", title: "Bộ lệnh CLI Điều hướng & Săn Log", fullTitle: "Trạm 2.4: Bộ Công cụ Tác chiến trên Cây thư mục — Điều hướng (pwd/ls/cd), Thao tác (cp/mv/rm) & Săn Log (head/tail -f/find/du)" },
    { id: "linux-2-summary", code: "Kết", title: "Tóm tắt bỏ túi & Checklist Chặng 2", fullTitle: "Tóm tắt bỏ túi Chặng 2 (Mạch Nhân – Quả & Checklist 5 Câu hỏi Bản chất)" }
  ];

  const LINUX_CHANG3_STATIONS = [
    { id: "linux-3-1", code: "3.1", title: "Ba cổng tiêu chuẩn (0, 1, 2) & Đường ống Pipe", fullTitle: "Trạm 3.1: Ba Cổng Tiêu chuẩn (0, 1, 2) & Đường ống Pipe trong Kernel" },
    { id: "linux-3-2", code: "3.2", title: "Điều hướng dòng chảy (>> và 2>&1) khi chạy ngầm", fullTitle: "Trạm 3.2: Điều hướng Dòng chảy (>> và 2>&1) — Chặn đứng 'Bẫy Mù Lỗi' khi Chạy ngầm" },
    { id: "linux-3-summary", code: "Kết", title: "Tóm tắt bỏ túi & Checklist Chặng 3", fullTitle: "Tóm tắt bỏ túi Chặng 3 (Mạch Nhân – Quả & Checklist 3 Câu hỏi Bản chất)" }
  ];

  const LINUX_CHANG4_STATIONS = [
    { id: "linux-4-1", code: "4.1", title: "Bash Scripting — 'Tờ giấy dán tủ lạnh' (.sh)", fullTitle: "Trạm 4.1: Bash Scripting — 'Tờ giấy dán tủ lạnh' Định nghĩa Làm bước nào, Ra sao" },
    { id: "linux-4-2", code: "4.2", title: "Compilation (GCC) & Quản đốc Makefile", fullTitle: "Trạm 4.2: Compilation (GCC) & Makefile — Lò luyện Mã máy & Người Quản đốc Xưởng" },
    { id: "linux-4-3", code: "4.3", title: "Hệ thống Cronjob 24/7 & 3 Cạm bẫy kinh điển", fullTitle: "Trạm 4.3: Hệ thống Cronjob — Trực ban 24/7 ('Khi nào bắt đầu chạy?') & 3 Cạm bẫy Kinh điển" },
    { id: "linux-4-summary", code: "Kết", title: "Tóm tắt bỏ túi & Checklist Chặng 4", fullTitle: "Tóm tắt bỏ túi Chặng 4 (Khép kín Toàn bộ Hành trình 4 Chặng Linux Fundamentals)" }
  ];

  function getLinuxStations(stageId = activeStorageStage) {
    if (stageId === 1) return LINUX_CHANG1_STATIONS;
    if (stageId === 2) return LINUX_CHANG2_STATIONS;
    if (stageId === 3) return LINUX_CHANG3_STATIONS;
    if (stageId === 4) return LINUX_CHANG4_STATIONS;
    return [];
  }

  const STORAGE_STAGES = [
    { id: 1, shortTitle: "Nguyên liệu gốc & Cơ chế vật lý", title: "Chặng 1: Nguyên liệu gốc & Cơ chế vật lý" },
    { id: 2, shortTitle: "File/Block/Object & Parquet/Arrow", title: "Chặng 2: Mô hình Lưu trữ (File/Block/Object) & Định dạng File (Avro, Parquet, Arrow)" },
    { id: 3, shortTitle: "HDFS, Kafka/CDC & Data Warehouse", title: "Chặng 3: Hạ tầng Phân tán (HDFS & Network Topology), Streaming (Kafka/CDC) & Data Warehouse" },
    { id: 4, shortTitle: "Data Modeling (Inmon, Kimball & SCD)", title: "Chặng 4: Kỹ thuật Thiết kế Mô hình Dữ liệu (Inmon, Kimball Star Schema, Data Vault & SCD)" },
    { id: 5, shortTitle: "Data Lake, Data Swamp & Lakehouse", title: "Chặng 5: Từ Data Lake đến Data Swamp & Sự trỗi dậy của Kiến trúc Lakehouse" },
    { id: 6, shortTitle: "Delta Lake, Iceberg & Hudi", title: "Chặng 6: Open Table Formats (Delta Lake, Apache Iceberg, Apache Hudi)" },
    { id: 7, shortTitle: "Medallion (Bronze/Silver/Gold)", title: "Chặng 7: Kiến trúc Multi-hop (Bronze / Silver / Gold), Data Catalog & Tối ưu hóa Lưu trữ" }
  ];

  const STORAGE_CHANG1_STATIONS = [
    { id: "storage-0-map", code: "0.0", title: "Nhân vật chính & Bản đồ 7 Chặng", fullTitle: "Trạm 0.0: Nhân vật chính Đơn hàng #8888 & Bản đồ Tư duy 7 Chặng Storage Layer" },
    { id: "storage-1-1", code: "1.1", title: "Bậc thang phần cứng & Độ trễ", fullTitle: "Trạm 1.1: Bậc thang phần cứng & Thang đo độ trễ vật lý (Cache Hierarchy)" },
    { id: "storage-1-2", code: "1.2", title: "RAM & Tràn bộ nhớ (Spill-to-Disk)", fullTitle: "Trạm 1.2: Đặc tính kỹ thuật của RAM & Hiện tượng tràn bộ nhớ (Spill-to-Disk)" },
    { id: "storage-1-3", code: "1.3", title: "Random Seek vs. Sequential Scan", fullTitle: "Trạm 1.3: Cơ học Đĩa cứng (Random Seek vs. Sequential Scan) & Cloud Storage" },
    { id: "storage-1-4", code: "1.4", title: "Nhiệt độ Lưu trữ (Hot/Warm/Cold)", fullTitle: "Trạm 1.4: Phân tầng nhiệt độ lưu trữ (Data Temperature) & Đệm đa tầng" },
    { id: "storage-1-5", code: "1.5", title: "Ranh giới OLTP vs. OLAP", fullTitle: "Trạm 1.5: Ranh giới hệ thống — Source System (OLTP) vs. Storage System (OLAP)" },
    { id: "storage-summary", code: "Kết", title: "Tóm tắt bỏ túi (5 Quy luật)", fullTitle: "Tóm tắt bỏ túi Chặng 1 (5 Quy luật Vật lý)" }
  ];

  const STORAGE_CHANG2_STATIONS = [
    { id: "storage-2-1", code: "2.1", title: "File vs. Block vs. Object Storage", fullTitle: "Trạm 2.1: Bộ ba Mô hình Lưu trữ Cơ sở — File vs. Block vs. Object Storage" },
    { id: "storage-2-2", code: "2.2", title: "Row (Avro) vs. Columnar (Parquet)", fullTitle: "Trạm 2.2: Định dạng Tệp & Tuần tự hóa (Serialization) — Row (CSV, Avro) vs. Columnar (Parquet, ORC)" },
    { id: "storage-2-3", code: "2.3", title: "In-Memory — Apache Arrow", fullTitle: "Trạm 2.3: Tuần tự hóa Trong Bộ nhớ (In-Memory Serialization) — Apache Arrow" },
    { id: "storage-2-4", code: "2.4", title: "Nén Dữ liệu & Splittability", fullTitle: "Trạm 2.4: Kỹ thuật Nén Dữ liệu (Compression) & Cạm bẫy Tính Phân tách (Splittability)" },
    { id: "storage-2-summary", code: "Kết", title: "Tóm tắt bỏ túi (4 Quyết định)", fullTitle: "Tóm tắt bỏ túi Chặng 2 (4 Quyết định Thiết kế Lưu trữ)" }
  ];

  const STORAGE_CHANG3_STATIONS = [
    { id: "storage-3-1", code: "3.1", title: "Hadoop HDFS & Nhân bản x3", fullTitle: "Trạm 3.1: Hạ tầng Lưu trữ Phân tán — Hadoop HDFS (NameNode, DataNode & Nhân bản x3)" },
    { id: "storage-3-2", code: "3.2", title: "Tô-pô Mạng & Động cơ Cache", fullTitle: "Trạm 3.2: Tô-pô Mạng (Network Topology), Khoảng cách Mạng & Động cơ Cache Phân tán" },
    { id: "storage-3-3", code: "3.3", title: "Streaming — Apache Kafka & CDC", fullTitle: "Trạm 3.3: Lưu trữ Dạng Luồng (Streaming Storage) — Apache Kafka & CDC" },
    { id: "storage-3-4", code: "3.4", title: "Kho Dữ liệu Tập trung (Data Warehouse)", fullTitle: "Trạm 3.4: Kho Dữ liệu Tập trung — Data Warehouse (OLAP, ACID & Động cơ Lưu trữ)" },
    { id: "storage-3-5", code: "3.5", title: "3 Hạn chế Lịch sử của Data Warehouse", fullTitle: "Trạm 3.5: Ba Hạn chế Lịch sử của Data Warehouse (Tại sao phải Tiến hóa?)" },
    { id: "storage-3-summary", code: "Kết", title: "Tóm tắt bỏ túi (Mạch Nhân – Quả)", fullTitle: "Tóm tắt bỏ túi Chặng 3 (3 Trụ cột Hạ tầng Phân tán, Streaming & Data Warehouse)" }
  ];

  const STORAGE_CHANG4_STATIONS = [
    { id: "storage-4-1", code: "4.1", title: "Conceptual ➔ Logical ➔ Physical", fullTitle: "Trạm 4.1: Ba Cấp độ Thiết kế Mô hình Dữ liệu (Conceptual ➔ Logical ➔ Physical)" },
    { id: "storage-4-2", code: "4.2", title: "Inmon vs. Kimball vs. Data Vault", fullTitle: "Trạm 4.2: Ba Trường phái Mô hình hóa trong Data Warehouse (Inmon vs. Kimball vs. Data Vault)" },
    { id: "storage-4-3", code: "4.3", title: "Fact vs. Dimension & Độ mịn (Grain)", fullTitle: "Trạm 4.3: Trái tim của Kimball — Bảng Sự kiện (Fact) vs. Bảng Thứ nguyên (Dimension) & Độ mịn (Grain)" },
    { id: "storage-4-4", code: "4.4", title: "Star vs. Snowflake vs. OBT (& Cubes)", fullTitle: "Trạm 4.4: Ba Kiến trúc Bố trí Bảng — Star Schema vs. Snowflake Schema vs. OBT (& OLAP Cubes)" },
    { id: "storage-4-5", code: "4.5", title: "Surrogate Key, SCD (Type 1/2/3) & Bus Matrix", fullTitle: "Trạm 4.5: Bộ ba Kỹ thuật Sống còn của Kimball — Surrogate Key, SCD (Type 1, 2 & 3) & Bus Matrix" },
    { id: "storage-4-summary", code: "Kết", title: "Tổng kết Chặng 4 (Khép lại Phần 1)", fullTitle: "Tổng kết Chặng 4 & Khép lại Trọn vẹn Phần 1 (4 Nguyên tắc Mô hình hóa)" }
  ];

  const STORAGE_CHANG5_STATIONS = [
    { id: "storage-5-1", code: "5.1", title: "Data Lake, Schema-on-Read & ELT", fullTitle: "Trạm 5.1: Giấc mơ Hồ Dữ liệu (Data Lake) — Object Storage, Schema-on-Read & ELT" },
    { id: "storage-5-2", code: "5.2", title: "Data Swamp & 5 Căn bệnh Lâm sàng", fullTitle: "Trạm 5.2: Bi kịch Đầm lầy Dữ liệu (Data Swamp) — 5 Căn bệnh Lâm sàng & 6 Điểm yếu Bảng Hive" },
    { id: "storage-5-3", code: "5.3", title: "Giải mã 3 Lỗ hổng Công cụ (Tooling Gaps)", fullTitle: "Trạm 5.3: Giải mã 3 Lỗ hổng Công cụ Cốt tử (ACID/Mutability, Data Catalog & Data Observability)" },
    { id: "storage-5-4", code: "5.4", title: "Phác đồ Cứu nguy (Zoning, Contracts, SSoT)", fullTitle: "Trạm 5.4: Phác đồ Cứu nguy — Zoning (Raw ➔ Cleansed ➔ Curated), Data Contracts & Single Source of Truth" },
    { id: "storage-5-summary", code: "Kết", title: "Chốt hạ Mạch Nhân – Quả Chặng 5", fullTitle: "Chốt hạ Mạch Nhân – Quả Chặng 5 (Bản lề bước sang Chặng 6 — Lakehouse)" }
  ];

  const STORAGE_CHANG6_STATIONS = [
    { id: "storage-6-1", code: "6.1", title: "Kiến trúc Lakehouse & Table Format", fullTitle: "Trạm 6.1: Kiến trúc Data Lakehouse & Bước ngoặt Định nghĩa lại Một Bảng (CIDR 2021)" },
    { id: "storage-6-2", code: "6.2", title: "Delta Lake, Iceberg, Hudi & UniForm", fullTitle: "Trạm 6.2: Giải phẫu Bộ não của Bộ ba Open Table Formats (Delta Lake, Apache Iceberg, Apache Hudi & UniForm/XTable)" },
    { id: "storage-6-3", code: "6.3", title: "ACID, Concurrency (OCC/MVCC/NBCC) & Time Travel", fullTitle: "Trạm 6.3: Bộ Tính năng Cốt lõi — ACID, Concurrency (MVCC/OCC/NBCC), Time Travel & Schema Evolution" },
    { id: "storage-6-4", code: "6.4", title: "Copy-on-Write (COW) vs. Merge-on-Read (MOR)", fullTitle: "Trạm 6.4: Chiến lược Ghi & Cập nhật — Copy-on-Write (COW) vs. Merge-on-Read (MOR)" },
    { id: "storage-6-5", code: "6.5", title: "5 Kỹ thuật Tối ưu Vật lý (Compaction, Z-Order, Vacuum)", fullTitle: "Trạm 6.5: Năm Kỹ thuật Tối ưu Vật lý Sống còn (Compaction, Hidden Partitioning, Z-Order/Liquid Clustering, Deletion Vectors, Vacuum)" },
    { id: "storage-6-summary", code: "Kết", title: "Chốt hạ Mạch Nhân – Quả Chặng 6", fullTitle: "Chốt hạ Mạch Nhân – Quả Chặng 6 (Bản lề bước vào Chặng 7 — Medallion & Governance)" }
  ];

  const STORAGE_CHANG7_STATIONS = [
    { id: "storage-7-1", code: "7.1", title: "Multi-Hop & Triết lý Medallion (Quality Gating)", fullTitle: "Trạm 7.1: Khái niệm Multi-Hop & Triết lý Kiến trúc Medallion (Quality Gating Pattern)" },
    { id: "storage-7-2", code: "7.2", title: "Giải phẫu 3 Tầng Bronze ➔ Silver ➔ Gold", fullTitle: "Trạm 7.2: Giải phẫu Chi tiết 3 Tầng Medallion qua Hành trình Đơn hàng #8888 (Bronze ➔ Silver ➔ Gold)" },
    { id: "storage-7-3", code: "7.3", title: "Dòng chảy Ngầm: Catalog, Lineage, Security & FinOps", fullTitle: "Trạm 7.3: Dòng chảy Ngầm Quản trị & Vận hành (Undercurrents: Catalog, Lineage, Security & FinOps)" },
    { id: "storage-7-4", code: "7.4", title: "Bản đồ Kiến trúc 6 Tầng (Bottom-Up Blueprint)", fullTitle: "Trạm 7.4: Bản đồ Kiến trúc Tổng thể 6 Tầng (Bottom-Up Blueprint) — Khép lại Toàn bộ Khóa học" },
    { id: "storage-7-summary", code: "Kết", title: "Checklist Tổng kết Chặng 7", fullTitle: "Checklist Tổng kết Chặng 7 & Toàn bộ Chương trình Storage Layer" }
  ];

  function getStorageStations(stageId = activeStorageStage) {
    if (stageId === 1) return STORAGE_CHANG1_STATIONS;
    if (stageId === 2) return STORAGE_CHANG2_STATIONS;
    if (stageId === 3) return STORAGE_CHANG3_STATIONS;
    if (stageId === 4) return STORAGE_CHANG4_STATIONS;
    if (stageId === 5) return STORAGE_CHANG5_STATIONS;
    if (stageId === 6) return STORAGE_CHANG6_STATIONS;
    if (stageId === 7) return STORAGE_CHANG7_STATIONS;
    return [];
  }

  function getTopicStages(topic = activeTopic) {
    if (topic === "F01") return LINUX_STAGES;
    if (topic === "D02") return STORAGE_STAGES;
    return [];
  }

  function getTopicStations(topic = activeTopic, stageId = activeStorageStage) {
    if (topic === "F01") return getLinuxStations(stageId);
    if (topic === "D02") return getStorageStations(stageId);
    return [];
  }

  let activeTopic = "F01";
  let activeStorageStage = 1;
  let activeStationId = "linux-0-map";
  let expandedTracks = new Set(["track-1", "track-2"]);
  let scrollObserver = null;
  let mermaidRenderGeneration = 0;
  let mermaidUniqueCounter = 0;
  let activeInlineCameras = new Map();
  let activeInlinePicCameras = new Map();
  let activeModalCamera = null;
  let currentExpandSafeId = null;
  let currentExpandMode = "ascii";
  let modalRenderToken = 0;
  let lastExpandTriggerEl = null;

  function readStoredVisualMode() {
    try {
      const saved = localStorage.getItem("fsds_visual_mode");
      if (saved === "ascii" || saved === "mermaid" || saved === "pic") {
        return saved;
      }
    } catch (_) {}
    return "ascii";
  }

  let defaultVisualMode = readStoredVisualMode();

  function syncGlobalVisualButtons() {
    const grp = document.getElementById("globalVisualModeGroup");
    if (!grp) return;
    grp.querySelectorAll("[data-gmode]").forEach(btn => {
      const m = btn.getAttribute("data-gmode");
      btn.setAttribute("aria-pressed", m === defaultVisualMode ? "true" : "false");
    });
  }

  function setGlobalVisualMode(mode) {
    if (mode !== "ascii" && mode !== "mermaid" && mode !== "pic") return;
    defaultVisualMode = mode;
    try {
      localStorage.setItem("fsds_visual_mode", mode);
    } catch (_) {}
    syncGlobalVisualButtons();
    const cards = document.querySelectorAll(".visual-card");
    cards.forEach(card => {
      const safeId = card.id.replace(/^vcard-/, "");
      setVisualMode(safeId, mode, mode === "mermaid");
    });
    if (mode === "mermaid") {
      reRenderVisibleMermaidDiagrams();
    }
    const labelMap = {
      ascii: "ASCII (Mặc định toàn trang)",
      mermaid: "Mermaid (Mặc định toàn trang)",
      pic: "Picture · Style #2 Infographic (Mặc định toàn trang)"
    };
    showToast("Visual toàn bài: " + (labelMap[mode] || mode.toUpperCase()));
  }

  function escapeHtml(str) {
    return String(str || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function normalizeSearch(value) {
    return String(value || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[đĐ]/g, "d")
      .toLowerCase()
      .trim();
  }

  function findTopicContext(code) {
    for (const group of SYLLABUS_GROUPS) {
      const item = group.items.find(x => x.code === code);
      if (item) return { group, item };
    }
    return { group: SYLLABUS_GROUPS[1], item: SYLLABUS_GROUPS[1].items[1] };
  }

  function showToast(msg) {
    const t = document.getElementById("toastBox");
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(window.__toastTimer);
    window.__toastTimer = setTimeout(() => t.classList.remove("show"), 2000);
  }

  function copyText(text, label) {
    navigator.clipboard.writeText(text).then(
      () => showToast("Đã sao chép " + label),
      () => showToast("Không thể sao chép tự động")
    );
  }

  /* ==========================================================================
     VISUAL SANDBOX BUILDER & INTERACTIVE MERMAID + PICTURE CAMERA CONTROLLER
     ========================================================================== */
  function resolveVisualAsset(safeId, title, caption, override = null) {
    if (override && override.previewSrc) return override;
    const fromHub = HUB_DATA.visual_assets && HUB_DATA.visual_assets[safeId];
    if (fromHub) return fromHub;

    const isLinux = safeId.startsWith("linux");
    const previewSrc = isLinux ? `assets/visuals/${safeId}.jpg` : `assets/visuals/${safeId}.svg`;
    const isStory = /bếp|kitchen|bẫy|trap|case|sự cố|đánh đổi|vs\.|so sánh|silent|ngầm/i.test(title + " " + (caption || ""));
    const template = isStory ? "PROMPT-STORY-ANALOGY" : "PROMPT-ARCH-DIAGRAM";
    const prompt = `[${template}]\nGenerate a clean, high-resolution 16:9 widescreen dark-slate blueprint infographic (#0f1419 background, Cyan #06b6d4, Emerald #10b981, Amber #f59e0b, Coral #f43f5e accents) for:\nTITLE: "${title}"\nCONTEXT: ${caption || title}\nSTYLE: Style #2 Dark-Slate Engineering Blueprint / Isometric Storytelling, crisp English technical labels, 100% faithful to source metrics and entities.`;

    return {
      src: previewSrc,
      previewSrc,
      status: "ready",
      role: "diagram",
      template,
      badgeLabel: `READY · ${template}`,
      prompt
    };
  }

  function buildSpineHeroBanner(safeId, badgeText, titleText, subtitleText, imgSrc, captionHtml) {
    return `
      <div class="spine-hero-card" id="spine-hero-${safeId}">
        <div class="spine-hero-header">
          <div>
            <span class="spine-hero-badge">${escapeHtml(badgeText)}</span>
            <span class="spine-hero-title">${escapeHtml(titleText)}</span>
          </div>
          <div style="display:flex;gap:6px;align-items:center;">
            <span class="hide-mobile" style="font-size:11.5px;color:var(--muted);">${escapeHtml(subtitleText)}</span>
            <button type="button" class="ui-btn" onclick="openSpineHeroModal('${safeId}', this)">Phóng to Mindmap</button>
          </div>
        </div>
        <div class="spine-hero-body" id="spine-body-${safeId}" onclick="handleSpineHeroClick('${safeId}', this, event)">
          <img src="${escapeHtml(imgSrc)}" alt="${escapeHtml(titleText)}" loading="eager" decoding="async" onerror="if(!this.dataset.retried){this.dataset.retried='1';this.src=this.src.split('?')[0]+'?r='+Date.now();}" />
        </div>
        <div class="pic-mobile-hint">
          <span id="spinemobhint-${safeId}">Chạm ảnh để phóng rõ 2x &amp; vuốt ngang đọc chi tiết</span>
          <button type="button" id="spinemobbtn-${safeId}" onclick="toggleSpineMobilePan('${safeId}', event)">Phóng rõ 2x</button>
        </div>
        <div class="spine-hero-footer">
          <span>${captionHtml}</span>
          <a href="${escapeHtml(imgSrc)}" target="_blank" rel="noopener" class="ui-btn" style="text-decoration:none;flex-shrink:0;">Mở ảnh gốc (Full HD)</a>
        </div>
      </div>
    `;
  }

  function toggleSpineMobilePan(safeId, ev) {
    if (ev) ev.stopPropagation();
    const body = document.getElementById("spine-body-" + safeId);
    const btn = document.getElementById("spinemobbtn-" + safeId);
    const hint = document.getElementById("spinemobhint-" + safeId);
    if (!body) return;
    const isPan = body.classList.toggle("mobile-hd-pan");
    if (btn) btn.textContent = isPan ? "Thu gọn (1x)" : "Phóng rõ 2x";
    if (hint) hint.textContent = isPan ? "Vuốt ngang trên ảnh để xem từng chặng" : "Chạm ảnh để phóng rõ 2x & vuốt ngang đọc chi tiết";
  }

  function handleSpineHeroClick(safeId, el, ev) {
    if (window.innerWidth <= 680) {
      toggleSpineMobilePan(safeId, ev);
      return;
    }
    openSpineHeroModal(safeId, el);
  }

  function openSpineHeroModal(safeId, triggerEl) {
    const card = document.getElementById("vcard-" + safeId);
    if (card) {
      setVisualMode(safeId, "pic");
      openExpandModal(safeId, triggerEl, "pic");
    }
  }

  function buildVisualBlock(id, title, asciiText, mermaidCode, caption, pictureOverride = null) {
    const safeId = id.replace(/[^a-zA-Z0-9_-]/g, "_");
    const asset = resolveVisualAsset(safeId, title, caption, pictureOverride);
    const initMode = (defaultVisualMode === "mermaid" || defaultVisualMode === "pic") ? defaultVisualMode : "ascii";

    window.__diagrams = window.__diagrams || {};
    window.__diagrams[safeId] = {
      ascii: asciiText,
      mermaid: mermaidCode,
      title,
      caption: caption || "",
      asset
    };

    const showAscii = (initMode === "ascii");
    const showMermaid = (initMode === "mermaid");
    const showPic = (initMode === "pic");
    const badgeClass = asset.status === "ready" ? "ready" : "template";

    return `
      <figure class="visual-card" id="vcard-${safeId}" data-mode="${initMode}">
        <div class="visual-bar">
          <div class="visual-bar-title">${escapeHtml(title)}</div>
          <div class="visual-controls">
            <div class="visual-segmented" role="group" aria-label="Chế độ hiển thị sơ đồ">
              <button type="button" class="seg-btn" data-vmode="ascii" aria-pressed="${initMode === 'ascii' ? 'true' : 'false'}" onclick="setVisualMode('${safeId}', 'ascii')">ASCII</button>
              <button type="button" class="seg-btn" data-vmode="mermaid" aria-pressed="${initMode === 'mermaid' ? 'true' : 'false'}" onclick="setVisualMode('${safeId}', 'mermaid')">Mermaid</button>
              <button type="button" class="seg-btn" data-vmode="pic" aria-pressed="${initMode === 'pic' ? 'true' : 'false'}" onclick="setVisualMode('${safeId}', 'pic')">Picture</button>
            </div>
            <button type="button" class="ui-btn" onclick="copyActiveDiagram('${safeId}')">Sao chép</button>
            <button type="button" class="ui-btn" onclick="openExpandModal('${safeId}', this)">Mở rộng</button>
            <div class="vmenu-wrap">
              <button type="button" class="ui-btn" onclick="toggleVisualMenu(event, '${safeId}')" aria-label="Tùy chọn sơ đồ">Tùy chọn</button>
              <div class="vmenu-popover" id="vmenu-${safeId}">
                <button type="button" class="vmenu-item" onclick="copyDiagram('${safeId}', 'ascii');closeAllVisualMenus()">Sao chép sơ đồ ASCII</button>
                <button type="button" class="vmenu-item" onclick="copyDiagram('${safeId}', 'mermaid');closeAllVisualMenus()">Sao chép mã Mermaid</button>
                <button type="button" class="vmenu-item" onclick="copyDiagram('${safeId}', 'prompt');closeAllVisualMenus()">Sao chép Prompt tạo ảnh (${escapeHtml(asset.template)})</button>
                <button type="button" class="vmenu-item" onclick="toggleMermaidCode('${safeId}');closeAllVisualMenus()">Xem / Ẩn mã nguồn Mermaid</button>
                <button type="button" class="vmenu-item" onclick="togglePicturePrompt('${safeId}');closeAllVisualMenus()">Xem / Ẩn Prompt tạo ảnh Style #2</button>
                <div class="vmenu-sep"></div>
                <button type="button" class="vmenu-item" onclick="downloadExcalidrawJson('${safeId}');closeAllVisualMenus()">Tải file .excalidraw</button>
                <button type="button" class="vmenu-item" onclick="exportToExcalidraw('${safeId}');closeAllVisualMenus()">Mở Excalidraw</button>
              </div>
            </div>
          </div>
        </div>

        <div class="visual-panes">
          <div class="visual-pane pane-ascii" id="pane-ascii-${safeId}" ${showAscii ? "" : "hidden"}>
            <pre class="ascii-diagram" tabindex="0" aria-label="${escapeHtml(title)}">${escapeHtml(asciiText)}</pre>
          </div>
          <div class="visual-pane pane-mermaid" id="pane-mermaid-${safeId}" ${showMermaid ? "" : "hidden"}>
            <div class="mermaid-viewer" id="mviewer-${safeId}">
              <div class="mermaid-toolbar" role="group" aria-label="Thu phóng sơ đồ Mermaid">
                <div class="mermaid-zoom-group">
                  <button type="button" class="zoom-btn" onclick="zoomInlineMermaid('${safeId}', -1)" aria-label="Thu nhỏ sơ đồ">−</button>
                  <button type="button" class="zoom-btn" id="mzoom-label-${safeId}" onclick="resetInlineMermaidOneToOne('${safeId}')" title="Đặt về tỷ lệ 100%">100%</button>
                  <button type="button" class="zoom-btn" onclick="zoomInlineMermaid('${safeId}', 1)" aria-label="Phóng to sơ đồ">+</button>
                  <button type="button" class="zoom-btn" onclick="fitInlineMermaid('${safeId}')">Vừa khung</button>
                </div>
                <span class="mermaid-hint hide-mobile">Kéo để di chuyển · ⌘/Ctrl + Cuộn để thu phóng</span>
              </div>
              <div class="mermaid-viewport" id="mviewport-${safeId}" tabindex="0" aria-label="Khung tương tác sơ đồ ${escapeHtml(title)}">
                <div class="mermaid-transform" id="mtransform-${safeId}"></div>
              </div>
            </div>
          </div>
          <div class="visual-pane pane-pic" id="pane-pic-${safeId}" ${showPic ? "" : "hidden"}>
            <div class="pic-viewer" id="pviewer-${safeId}">
              <div class="pic-toolbar" role="group" aria-label="Thu phóng ảnh minh họa">
                <div class="mermaid-zoom-group">
                  <button type="button" class="zoom-btn" onclick="zoomInlinePicture('${safeId}', -1)" aria-label="Thu nhỏ ảnh">−</button>
                  <button type="button" class="zoom-btn" id="pzoom-label-${safeId}" onclick="resetInlinePictureOneToOne('${safeId}')" title="Đặt về tỷ lệ 100%">100%</button>
                  <button type="button" class="zoom-btn" onclick="zoomInlinePicture('${safeId}', 1)" aria-label="Phóng to ảnh">+</button>
                  <button type="button" class="zoom-btn" onclick="fitInlinePicture('${safeId}')">Vừa khung</button>
                </div>
                <div class="pic-meta">
                  <span class="pic-badge ${badgeClass}">${escapeHtml(asset.badgeLabel || ("STYLE #2 · " + asset.template))}</span>
                  <button type="button" class="ui-btn" onclick="togglePicturePrompt('${safeId}')">Prompt Style #2</button>
                  <a href="${escapeHtml(asset.previewSrc)}" target="_blank" rel="noopener" class="ui-btn" style="text-decoration:none;">Ảnh gốc</a>
                </div>
              </div>
              <div class="pic-viewport" id="pviewport-${safeId}" tabindex="0" aria-label="Khung tương tác ảnh minh họa ${escapeHtml(title)}">
                <div class="pic-transform" id="ptransform-${safeId}">
                  <img id="pimg-${safeId}" src="${escapeHtml(asset.previewSrc)}" alt="${escapeHtml(title)}" loading="${showPic ? 'eager' : 'lazy'}" decoding="async" draggable="false" onclick="handlePictureImgClick('${safeId}', event)" onerror="if(!this.dataset.retried){this.dataset.retried='1';this.src=this.src.split('?')[0]+'?r='+Date.now();}" />
                </div>
              </div>
              <div class="pic-mobile-hint">
                <span id="pmobhint-${safeId}">Chạm ảnh để phóng rõ 2x &amp; vuốt ngang đọc chữ</span>
                <button type="button" id="pmobbtn-${safeId}" onclick="toggleMobilePicPan('${safeId}', event)">Phóng rõ 2x</button>
              </div>
              <div class="pic-prompt-box" id="pprompt-${safeId}">
                <div class="pic-prompt-head">
                  <strong>Bộ Prompt Chuyên biệt Style #2 (${escapeHtml(asset.template)}) — Dark-Slate Blueprint (#0f1419)</strong>
                  <button type="button" class="ui-btn" onclick="copyDiagram('${safeId}', 'prompt')">Sao chép Prompt</button>
                </div>
                <pre><code>${escapeHtml(asset.prompt)}</code></pre>
              </div>
            </div>
          </div>
        </div>

        <div class="mermaid-code-box" id="mcode-${safeId}">
          <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px;">
            <strong style="font-size:12px;">Mã nguồn Mermaid (Excalidraw: Insert → Mermaid to Excalidraw)</strong>
            <div style="display:flex;gap:6px;">
              <button type="button" class="ui-btn" onclick="copyDiagram('${safeId}', 'mermaid')">Sao chép mã</button>
              <button type="button" class="ui-btn" onclick="downloadExcalidrawJson('${safeId}')">Tải .excalidraw</button>
            </div>
          </div>
          <pre><code>${escapeHtml(mermaidCode)}</code></pre>
        </div>
        ${caption ? `<figcaption class="visual-caption">${caption}</figcaption>` : ""}
      </figure>
    `;
  }

  function createMermaidCamera(viewportEl, transformEl, labelEl) {
    let scale = 1;
    let tx = 0;
    let ty = 0;
    let naturalWidth = 800;
    let naturalHeight = 400;
    let viewMode = "fit";
    let isDragging = false;
    let startX = 0;
    let startY = 0;
    let startTx = 0;
    let startTy = 0;

    const minScale = 0.25;
    const maxScale = 3.2;

    function measureSvg() {
      const svg = transformEl.querySelector("svg");
      if (!svg) return;
      const vb = svg.viewBox && svg.viewBox.baseVal;
      if (vb && vb.width > 0 && vb.height > 0) {
        naturalWidth = vb.width;
        naturalHeight = vb.height;
      } else {
        const bbox = svg.getBBox ? svg.getBBox() : { width: 800, height: 400 };
        naturalWidth = Math.max(200, bbox.width || 800);
        naturalHeight = Math.max(120, bbox.height || 400);
      }
      svg.style.width = naturalWidth + "px";
      svg.style.height = naturalHeight + "px";
      svg.style.maxWidth = "none";
    }

    function applyTransform() {
      transformEl.style.transform = `matrix(${scale}, 0, 0, ${scale}, ${tx}, ${ty})`;
      if (labelEl) {
        labelEl.textContent = Math.round(scale * 100) + "%";
      }
    }

    function fitToViewport(initialReadable = false) {
      measureSvg();
      const vw = viewportEl.clientWidth || 800;
      const vh = viewportEl.clientHeight || 420;
      const pad = 28;
      const fitS = Math.min(
        (vw - pad * 2) / Math.max(1, naturalWidth),
        (vh - pad * 2) / Math.max(1, naturalHeight)
      );
      if (initialReadable && fitS < 0.85) {
        scale = Math.min(maxScale, Math.max(0.88, fitS));
        tx = Math.max(16, (vw - naturalWidth * scale) / 2);
        ty = 20;
        viewMode = "readable";
      } else {
        scale = Math.min(1.35, Math.max(minScale, fitS));
        tx = (vw - naturalWidth * scale) / 2;
        ty = (vh - naturalHeight * scale) / 2;
        viewMode = "fit";
      }
      applyTransform();
    }

    function resetOneToOne() {
      measureSvg();
      const vw = viewportEl.clientWidth || 800;
      const vh = viewportEl.clientHeight || 420;
      scale = 1;
      tx = Math.max(16, (vw - naturalWidth) / 2);
      ty = Math.max(16, (vh - naturalHeight) / 2);
      viewMode = "custom";
      applyTransform();
    }

    function zoomAt(nextScale, focalX, focalY) {
      const clamped = Math.min(maxScale, Math.max(minScale, nextScale));
      const ratio = clamped / scale;
      tx = focalX - (focalX - tx) * ratio;
      ty = focalY - (focalY - ty) * ratio;
      scale = clamped;
      viewMode = "custom";
      applyTransform();
    }

    function stepZoom(direction) {
      const vw = viewportEl.clientWidth || 800;
      const vh = viewportEl.clientHeight || 420;
      const factor = direction > 0 ? 1.2 : 1 / 1.2;
      zoomAt(scale * factor, vw / 2, vh / 2);
    }

    function onWheel(e) {
      if (!(e.ctrlKey || e.metaKey)) return;
      e.preventDefault();
      const rect = viewportEl.getBoundingClientRect();
      const fx = e.clientX - rect.left;
      const fy = e.clientY - rect.top;
      const factor = e.deltaY < 0 ? 1.12 : 1 / 1.12;
      zoomAt(scale * factor, fx, fy);
    }

    function onPointerDown(e) {
      if (e.button !== 0) return;
      isDragging = true;
      viewMode = "custom";
      startX = e.clientX;
      startY = e.clientY;
      startTx = tx;
      startTy = ty;
      viewportEl.classList.add("is-panning");
      if (viewportEl.setPointerCapture) {
        try { viewportEl.setPointerCapture(e.pointerId); } catch (_) {}
      }
    }

    function onPointerMove(e) {
      if (!isDragging) return;
      tx = startTx + (e.clientX - startX);
      ty = startTy + (e.clientY - startY);
      applyTransform();
    }

    function stopDragging(e) {
      if (!isDragging) return;
      isDragging = false;
      viewportEl.classList.remove("is-panning");
      if (e && viewportEl.releasePointerCapture) {
        try { viewportEl.releasePointerCapture(e.pointerId); } catch (_) {}
      }
    }

    function onKeyDown(e) {
      if (e.key === "+" || e.key === "=") {
        e.preventDefault();
        stepZoom(1);
      } else if (e.key === "-" || e.key === "_") {
        e.preventDefault();
        stepZoom(-1);
      } else if (e.key === "0") {
        e.preventDefault();
        resetOneToOne();
      }
    }

    viewportEl.addEventListener("wheel", onWheel, { passive: false });
    viewportEl.addEventListener("pointerdown", onPointerDown);
    viewportEl.addEventListener("pointermove", onPointerMove);
    viewportEl.addEventListener("pointerup", stopDragging);
    viewportEl.addEventListener("pointercancel", stopDragging);
    viewportEl.addEventListener("lostpointercapture", stopDragging);
    viewportEl.addEventListener("keydown", onKeyDown);

    fitToViewport(true);

    return {
      stepZoom,
      resetOneToOne,
      fitToViewport: () => fitToViewport(false),
      getState: () => ({ scale, tx, ty, naturalWidth, naturalHeight, viewMode }),
      dispose() {
        viewportEl.removeEventListener("wheel", onWheel);
        viewportEl.removeEventListener("pointerdown", onPointerDown);
        viewportEl.removeEventListener("pointermove", onPointerMove);
        viewportEl.removeEventListener("pointerup", stopDragging);
        viewportEl.removeEventListener("pointercancel", stopDragging);
        viewportEl.removeEventListener("lostpointercapture", stopDragging);
        viewportEl.removeEventListener("keydown", onKeyDown);
      }
    };
  }

  function createPictureCamera(viewportEl, transformEl, imgEl, labelEl) {
    let scale = 1;
    let tx = 0;
    let ty = 0;
    let isDragging = false;
    let startX = 0;
    let startY = 0;
    let startTx = 0;
    let startTy = 0;

    const minScale = 0.5;
    const maxScale = 4.0;

    function applyTransform() {
      if (window.innerWidth <= 680) {
        transformEl.style.transform = "";
        return;
      }
      transformEl.style.transform = `translate3d(${tx}px, ${ty}px, 0) scale(${scale})`;
      if (labelEl) {
        labelEl.textContent = Math.round(scale * 100) + "%";
      }
    }

    function fitToViewport() {
      scale = 1;
      tx = 0;
      ty = 0;
      applyTransform();
    }

    function resetOneToOne() {
      scale = 1;
      tx = 0;
      ty = 0;
      applyTransform();
    }

    function zoomAt(nextScale, focalOffsetX = 0, focalOffsetY = 0) {
      const clamped = Math.min(maxScale, Math.max(minScale, nextScale));
      const ratio = clamped / scale;
      tx = focalOffsetX - (focalOffsetX - tx) * ratio;
      ty = focalOffsetY - (focalOffsetY - ty) * ratio;
      scale = clamped;
      if (Math.abs(scale - 1) < 0.01) {
        scale = 1;
        tx = 0;
        ty = 0;
      }
      applyTransform();
    }

    function stepZoom(direction) {
      const factor = direction > 0 ? 1.25 : 1 / 1.25;
      zoomAt(scale * factor, 0, 0);
    }

    function onWheel(e) {
      if (!(e.ctrlKey || e.metaKey)) return;
      e.preventDefault();
      const rect = viewportEl.getBoundingClientRect();
      const fx = (e.clientX - rect.left) - rect.width / 2;
      const fy = (e.clientY - rect.top) - rect.height / 2;
      const factor = e.deltaY < 0 ? 1.15 : 1 / 1.15;
      zoomAt(scale * factor, fx, fy);
    }

    function onPointerDown(e) {
      if (e.button !== 0) return;
      // On mobile or touch when unzoomed, never hijack touch scroll / swipe
      if (window.innerWidth <= 680 || (e.pointerType === "touch" && scale <= 1.02)) {
        return;
      }
      isDragging = true;
      startX = e.clientX;
      startY = e.clientY;
      startTx = tx;
      startTy = ty;
      viewportEl.classList.add("is-panning");
      if (viewportEl.setPointerCapture) {
        try { viewportEl.setPointerCapture(e.pointerId); } catch (_) {}
      }
    }

    function onPointerMove(e) {
      if (!isDragging) return;
      tx = startTx + (e.clientX - startX);
      ty = startTy + (e.clientY - startY);
      applyTransform();
    }

    function stopDragging(e) {
      if (!isDragging) return;
      isDragging = false;
      viewportEl.classList.remove("is-panning");
      if (e && viewportEl.releasePointerCapture) {
        try { viewportEl.releasePointerCapture(e.pointerId); } catch (_) {}
      }
    }

    viewportEl.addEventListener("wheel", onWheel, { passive: false });
    viewportEl.addEventListener("pointerdown", onPointerDown);
    viewportEl.addEventListener("pointermove", onPointerMove);
    viewportEl.addEventListener("pointerup", stopDragging);
    viewportEl.addEventListener("pointercancel", stopDragging);
    viewportEl.addEventListener("lostpointercapture", stopDragging);

    fitToViewport();

    return {
      stepZoom,
      resetOneToOne,
      fitToViewport,
      dispose() {
        viewportEl.removeEventListener("wheel", onWheel);
        viewportEl.removeEventListener("pointerdown", onPointerDown);
        viewportEl.removeEventListener("pointermove", onPointerMove);
        viewportEl.removeEventListener("pointerup", stopDragging);
        viewportEl.removeEventListener("pointercancel", stopDragging);
        viewportEl.removeEventListener("lostpointercapture", stopDragging);
      }
    };
  }

  function disposeAllInlineCameras() {
    for (const cam of activeInlineCameras.values()) {
      cam.dispose();
    }
    activeInlineCameras.clear();
    for (const pcam of activeInlinePicCameras.values()) {
      pcam.dispose();
    }
    activeInlinePicCameras.clear();
  }

  function setMobilePicPanState(safeId, enablePan) {
    const vp = document.getElementById("pviewport-" + safeId);
    const lbl = document.getElementById("pzoom-label-" + safeId);
    const btn = document.getElementById("pmobbtn-" + safeId);
    const hint = document.getElementById("pmobhint-" + safeId);
    if (!vp) return;
    vp.classList.toggle("mobile-hd-pan", Boolean(enablePan));
    if (lbl) lbl.textContent = enablePan ? "200%" : "100%";
    if (btn) btn.textContent = enablePan ? "Thu gọn (1x)" : "Phóng rõ 2x";
    if (hint) hint.textContent = enablePan ? "Vuốt ngang trên ảnh để đọc rõ từng chi tiết" : "Chạm ảnh để phóng rõ 2x & vuốt ngang đọc chữ";
  }

  function toggleMobilePicPan(safeId, ev) {
    if (ev) ev.stopPropagation();
    const vp = document.getElementById("pviewport-" + safeId);
    if (!vp) return;
    const nextState = !vp.classList.contains("mobile-hd-pan");
    setMobilePicPanState(safeId, nextState);
  }

  function handlePictureImgClick(safeId, ev) {
    if (window.innerWidth <= 680) {
      toggleMobilePicPan(safeId, ev);
    }
  }

  function ensurePictureRendered(safeId) {
    const vp = document.getElementById("pviewport-" + safeId);
    const tr = document.getElementById("ptransform-" + safeId);
    const img = document.getElementById("pimg-" + safeId);
    const lbl = document.getElementById("pzoom-label-" + safeId);
    if (!vp || !tr || !img) return;
    img.loading = "eager";
    if (activeInlinePicCameras.has(safeId)) {
      return;
    }
    const cam = createPictureCamera(vp, tr, img, lbl);
    activeInlinePicCameras.set(safeId, cam);
  }

  function zoomInlineMermaid(safeId, dir) {
    const cam = activeInlineCameras.get(safeId);
    if (cam) cam.stepZoom(dir);
  }

  function resetInlineMermaidOneToOne(safeId) {
    const cam = activeInlineCameras.get(safeId);
    if (cam) cam.resetOneToOne();
  }

  function fitInlineMermaid(safeId) {
    const cam = activeInlineCameras.get(safeId);
    if (cam) cam.fitToViewport();
  }

  function zoomInlinePicture(safeId, dir) {
    ensurePictureRendered(safeId);
    if (window.innerWidth <= 680) {
      setMobilePicPanState(safeId, dir > 0);
      return;
    }
    const cam = activeInlinePicCameras.get(safeId);
    if (cam) cam.stepZoom(dir);
  }

  function resetInlinePictureOneToOne(safeId) {
    ensurePictureRendered(safeId);
    if (window.innerWidth <= 680) {
      setMobilePicPanState(safeId, false);
      return;
    }
    const cam = activeInlinePicCameras.get(safeId);
    if (cam) cam.resetOneToOne();
  }

  function fitInlinePicture(safeId) {
    ensurePictureRendered(safeId);
    if (window.innerWidth <= 680) {
      setMobilePicPanState(safeId, false);
      return;
    }
    const cam = activeInlinePicCameras.get(safeId);
    if (cam) cam.fitToViewport();
  }

  function togglePicturePrompt(safeId) {
    const box = document.getElementById("pprompt-" + safeId);
    if (box) box.classList.toggle("show");
  }

  function setVisualMode(safeId, mode, deferRender = false) {
    if (mode !== "ascii" && mode !== "mermaid" && mode !== "pic") {
      mode = "ascii";
    }
    const card = document.getElementById("vcard-" + safeId);
    if (!card) return;
    card.dataset.mode = mode;
    card.querySelectorAll("[data-vmode]").forEach(btn => {
      const isSelected = btn.getAttribute("data-vmode") === mode;
      btn.setAttribute("aria-pressed", isSelected ? "true" : "false");
    });
    const asciiPane = document.getElementById("pane-ascii-" + safeId);
    const mermaidPane = document.getElementById("pane-mermaid-" + safeId);
    const picPane = document.getElementById("pane-pic-" + safeId);

    if (asciiPane) asciiPane.hidden = (mode !== "ascii");
    if (mermaidPane) mermaidPane.hidden = (mode !== "mermaid");
    if (picPane) picPane.hidden = (mode !== "pic");

    if (!deferRender) {
      if (mode === "mermaid") {
        ensureMermaidRendered(safeId);
      } else if (mode === "pic") {
        ensurePictureRendered(safeId);
      }
    }
  }

  function toggleVisualMenu(ev, safeId) {
    ev.stopPropagation();
    const menu = document.getElementById("vmenu-" + safeId);
    if (!menu) return;
    const wasOpen = menu.classList.contains("open");
    closeAllVisualMenus();
    if (!wasOpen) menu.classList.add("open");
  }

  function closeAllVisualMenus() {
    document.querySelectorAll(".vmenu-popover.open").forEach(el => el.classList.remove("open"));
  }

  function toggleMermaidCode(safeId) {
    const box = document.getElementById("mcode-" + safeId);
    if (box) box.classList.toggle("show");
  }

  function copyActiveDiagram(safeId) {
    const card = document.getElementById("vcard-" + safeId);
    const mode = card ? card.dataset.mode : "ascii";
    if (mode === "mermaid") {
      copyDiagram(safeId, "mermaid");
    } else if (mode === "pic") {
      copyDiagram(safeId, "prompt");
    } else {
      copyDiagram(safeId, "ascii");
    }
  }

  function copyDiagram(safeId, kind) {
    const item = window.__diagrams?.[safeId];
    if (!item) return;
    if (kind === "prompt") {
      const p = item.asset ? item.asset.prompt : "";
      copyText(p, "Prompt tạo ảnh Style #2");
      return;
    }
    copyText(item[kind], kind === "ascii" ? "sơ đồ ASCII" : "mã Mermaid");
  }

  function openExpandModal(safeId, triggerEl = null, forceMode = null) {
    const item = window.__diagrams?.[safeId];
    if (!item) return;
    lastExpandTriggerEl = triggerEl || document.activeElement;
    currentExpandSafeId = safeId;
    const card = document.getElementById("vcard-" + safeId);
    const cardMode = forceMode || (card ? card.dataset.mode : "ascii");
    if (cardMode === "pic") {
      currentExpandMode = "pic";
    } else if (cardMode === "mermaid") {
      currentExpandMode = "mermaid";
    } else {
      currentExpandMode = "ascii";
    }

    const modal = document.getElementById("expandModal");
    document.getElementById("expandModalTitle").textContent = item.title;
    modal.classList.add("open");
    renderExpandModalContent();
  }

  function setExpandModalMode(mode) {
    currentExpandMode = mode;
    renderExpandModalContent();
  }

  async function renderExpandModalContent() {
    if (!currentExpandSafeId) return;
    const item = window.__diagrams?.[currentExpandSafeId];
    if (!item) return;
    const myToken = ++modalRenderToken;

    if (activeModalCamera) {
      activeModalCamera.dispose();
      activeModalCamera = null;
    }

    const asciiBtn = document.getElementById("expandModeAsciiBtn");
    const mermaidBtn = document.getElementById("expandModeMermaidBtn");
    const picBtn = document.getElementById("expandModePicBtn");
    if (asciiBtn) asciiBtn.setAttribute("aria-pressed", currentExpandMode === "ascii" ? "true" : "false");
    if (mermaidBtn) mermaidBtn.setAttribute("aria-pressed", currentExpandMode === "mermaid" ? "true" : "false");
    if (picBtn) picBtn.setAttribute("aria-pressed", currentExpandMode === "pic" ? "true" : "false");

    const body = document.getElementById("expandModalBody");
    const copyBtn = document.getElementById("expandCopyBtn");
    if (copyBtn) {
      copyBtn.textContent = currentExpandMode === "pic" ? "Sao chép Prompt" : "Sao chép";
      copyBtn.onclick = () => copyDiagram(currentExpandSafeId, currentExpandMode === "pic" ? "prompt" : currentExpandMode);
    }

    if (currentExpandMode === "ascii") {
      body.innerHTML = `<pre class="ascii-diagram" tabindex="0">${escapeHtml(item.ascii)}</pre>`;
      return;
    }

    if (currentExpandMode === "pic") {
      const asset = item.asset || resolveVisualAsset(currentExpandSafeId, item.title, item.caption);
      body.innerHTML = `
        <div class="pic-viewer">
          <div class="pic-toolbar" role="group" aria-label="Thu phóng ảnh phóng to">
            <div class="mermaid-zoom-group">
              <button type="button" class="zoom-btn" id="modalPicZoomOutBtn" aria-label="Thu nhỏ ảnh">−</button>
              <button type="button" class="zoom-btn" id="modalPicZoomLabelBtn" title="Đặt về tỷ lệ 100%">100%</button>
              <button type="button" class="zoom-btn" id="modalPicZoomInBtn" aria-label="Phóng to ảnh">+</button>
              <button type="button" class="zoom-btn" id="modalPicZoomFitBtn">Vừa khung</button>
            </div>
            <div class="pic-meta">
              <span class="pic-badge ready">${escapeHtml(asset.badgeLabel || ("STYLE #2 · " + asset.template))}</span>
              <a href="${escapeHtml(asset.previewSrc)}" target="_blank" rel="noopener" class="ui-btn" style="text-decoration:none;">Mở ảnh gốc</a>
            </div>
          </div>
          <div class="pic-viewport" id="modalPicViewport" tabindex="0" style="height:70vh;max-height:70vh;">
            <div class="pic-transform" id="modalPicTransform">
              <img id="modalPicImg" src="${escapeHtml(asset.previewSrc)}" alt="${escapeHtml(item.title)}" draggable="false" />
            </div>
          </div>
        </div>
      `;
      const vp = document.getElementById("modalPicViewport");
      const tr = document.getElementById("modalPicTransform");
      const img = document.getElementById("modalPicImg");
      const lbl = document.getElementById("modalPicZoomLabelBtn");
      if (!vp || !tr || !img) return;
      activeModalCamera = createPictureCamera(vp, tr, img, lbl);
      document.getElementById("modalPicZoomOutBtn").onclick = () => activeModalCamera.stepZoom(-1);
      document.getElementById("modalPicZoomInBtn").onclick = () => activeModalCamera.stepZoom(1);
      document.getElementById("modalPicZoomLabelBtn").onclick = () => activeModalCamera.resetOneToOne();
      document.getElementById("modalPicZoomFitBtn").onclick = () => activeModalCamera.fitToViewport();
      return;
    }

    body.innerHTML = `
      <div class="mermaid-viewer">
        <div class="mermaid-toolbar" role="group" aria-label="Thu phóng sơ đồ phóng to">
          <div class="mermaid-zoom-group">
            <button type="button" class="zoom-btn" id="modalZoomOutBtn" aria-label="Thu nhỏ sơ đồ">−</button>
            <button type="button" class="zoom-btn" id="modalZoomLabelBtn" title="Đặt về tỷ lệ 100%">100%</button>
            <button type="button" class="zoom-btn" id="modalZoomInBtn" aria-label="Phóng to sơ đồ">+</button>
            <button type="button" class="zoom-btn" id="modalZoomFitBtn">Vừa khung</button>
          </div>
          <span class="mermaid-hint">Kéo để di chuyển · ⌘/Ctrl + Cuộn để thu phóng</span>
        </div>
        <div class="mermaid-viewport" id="modalMermaidViewport" tabindex="0">
          <div class="mermaid-transform" id="modalMermaidTransform"></div>
        </div>
      </div>
    `;

    if (!window.mermaid) return;
    initMermaidConfig();
    const uid = "mmodal_" + (++mermaidUniqueCounter);
    try {
      const { svg } = await window.mermaid.render(uid, item.mermaid);
      if (myToken !== modalRenderToken) return;
      const vp = document.getElementById("modalMermaidViewport");
      const tr = document.getElementById("modalMermaidTransform");
      const lbl = document.getElementById("modalZoomLabelBtn");
      if (!vp || !tr) return;
      tr.innerHTML = svg;
      activeModalCamera = createMermaidCamera(vp, tr, lbl);
      document.getElementById("modalZoomOutBtn").onclick = () => activeModalCamera.stepZoom(-1);
      document.getElementById("modalZoomInBtn").onclick = () => activeModalCamera.stepZoom(1);
      document.getElementById("modalZoomLabelBtn").onclick = () => activeModalCamera.resetOneToOne();
      document.getElementById("modalZoomFitBtn").onclick = () => activeModalCamera.fitToViewport();
    } catch (e) {
      console.warn("Modal Mermaid render error:", e);
    }
  }

  function closeExpandModal() {
    modalRenderToken++;
    if (activeModalCamera) {
      activeModalCamera.dispose();
      activeModalCamera = null;
    }
    document.getElementById("expandModal").classList.remove("open");
    if (lastExpandTriggerEl && typeof lastExpandTriggerEl.focus === "function") {
      lastExpandTriggerEl.focus();
      lastExpandTriggerEl = null;
    }
  }

  async function exportToExcalidraw(safeId) {
    const item = window.__diagrams?.[safeId];
    if (!item) return;
    window.open("https://excalidraw.com", "_blank", "noopener");
    try {
      await navigator.clipboard.writeText(item.mermaid);
      showToast("Đã sao chép mã Mermaid (Dán vào Excalidraw: More Tools → Mermaid to Excalidraw)");
    } catch (_) {
      showToast("Đã mở Excalidraw");
    }
  }

  async function downloadExcalidrawJson(safeId) {
    const item = window.__diagrams?.[safeId];
    if (!item) return;
    showToast("Đang chuyển đổi sang .excalidraw...");
    try {
      const mod = await import("https://cdn.jsdelivr.net/npm/@excalidraw/mermaid-to-excalidraw/+esm");
      const { elements, files } = await mod.parseMermaidToExcalidraw(item.mermaid);
      const payload = {
        type: "excalidraw",
        version: 2,
        source: "https://ankinguyen-engineer-2002.github.io/FSDS-EDAI-DSAI/",
        elements: elements || [],
        appState: { viewBackgroundColor: "#181716", gridSize: null },
        files: files || {}
      };
      const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${safeId}.excalidraw`;
      a.click();
      setTimeout(() => URL.revokeObjectURL(url), 1500);
      showToast("Đã tải file .excalidraw");
    } catch (err) {
      copyText(item.mermaid, "mã Mermaid");
    }
  }

  /* ==========================================================================
     CONTENT RENDERERS (100% VERBATIM STORAGE CHẶNG 1 · ZERO EMOJI SLOP)
     ========================================================================== */
  function renderStorageChang1() {
    const d = HUB_DATA.storage_diagrams;
    return `
      <div class="prose">
        <p><strong>Chặng 1: Nguyên liệu gốc &amp; Cơ chế vật lý (Raw Ingredients &amp; Physical Mechanics)</strong> mở màn cho toàn bộ học phần <strong>II. Data Engineering — D02 · Storage Layer</strong> (bám sát 100% <code>course-slides/05-storage-layer.pdf</code> — 173 trang, kết hợp nền tảng cơ học từ bộ 5 sách kinh điển: <em>Fundamentals of Data Engineering</em> của Reis &amp; Housley, <em>Designing Data-Intensive Applications</em> của Martin Kleppmann, <em>The Data Warehouse Toolkit</em> của Kimball &amp; Ross, <em>Delta Lake: Up and Running</em> của Bennion et al., và <em>Apache Iceberg: The Definitive Guide</em> của Shiran et al.).</p>

        <h2 id="storage-0-map" tabindex="-1">TRẠM 0.0: NHÂN VẬT CHÍNH ĐƠN HÀNG #8888 &amp; BẢN ĐỒ TƯ DUY 7 CHẶNG STORAGE LAYER</h2>
        <p><em>(Bước 0 — Thiết lập Nhân vật chính xuyên suốt, Bản đồ Cơ học 7 Chặng &amp; Ma trận Nhân – Quả Toàn Học Phần trước khi đi sâu từng Trạm)</em></p>

        ${buildSpineHeroBanner(
          "storage-0-1",
          "SPINE HERO MINDMAP · STYLE #2",
          "Bản đồ Kiến trúc 7 Chặng Storage Layer — Hành trình Đơn hàng #8888",
          "PROMPT-ARCH-DIAGRAM · 16:9 Dark-Slate Blueprint",
          "assets/visuals/storage-0-map.jpg",
          "<strong>Bản đồ Xương sống Học phần D02 (Spine Hero Mindmap):</strong> Toàn cảnh 7 Chặng tiến hóa của <code>Đơn hàng #8888</code> từ phần cứng vật lý <code>CPU Cache / RAM / SSD / HDD</code> (Chặng 1), định dạng <code>Parquet / Arrow</code> (Chặng 2), hạ tầng phân tán <code>HDFS / Kafka / Cloud DWH</code> (Chặng 3), mô hình <code>Kimball Star Schema / SCD2</code> (Chặng 4), vượt đầm lầy <code>Data Swamp</code> (Chặng 5) lên <code>Delta Lake / Iceberg / Hudi</code> (Chặng 6) và quy hoạch <code>Medallion 6 Tầng</code> (Chặng 7)."
        )}

        <h3 id="storage-0-protagonist">1. Nhân vật chính Xuyên suốt Học phần: <code>Đơn hàng #8888</code></h3>
        <p>Thay vì học từng công nghệ lưu trữ như những ốc đảo rời rạc, toàn bộ 7 Chặng của học phần <strong>D02 · Storage Layer</strong> theo chân một nhân vật chính duy nhất: <strong><code>Đơn hàng #8888</code> (khách hàng Nguyễn Văn A tại Bình Dương đặt mua bộ Sofa giá <code>15.000.000 VNĐ</code> lúc <code>10:05:12</code>)</strong> từ khoảnh khắc các bit điện tử đầu tiên vừa lóe lên trên thanh <code>RAM</code> của máy chủ bán hàng <code>OLTP</code> cho đến khi kết tinh thành con số <code>KPI</code> doanh thu tinh khiết trên bảng điều khiển của Tổng Giám đốc.</p>

        <h3 id="storage-0-mental-map">2. Bản đồ Tư duy 1 Dòng (Mental Map) — Mạch Nhân Quả 7 Chặng</h3>
        <p>Mọi kiến trúc lưu trữ hiện đại đều tuân theo một sợi dây nhân – quả bất biến: <strong>Giới hạn vật lý của phần cứng ở tầng dưới sẽ định đoạt cấu trúc tệp, mô hình dữ liệu và kiến trúc quản trị ở tầng trên</strong>:</p>

        ${buildVisualBlock(
          "storage-0-1",
          "Hình 0.1 — Bản đồ Cơ học 7 Chặng Storage Layer: Hành trình Tiến hóa của Đơn hàng #8888 (Mental Map)",
          d["0.1"].ascii,
          d["0.1"].mermaid,
          "Hành trình 7 Chặng của Đơn hàng #8888: Từ giới hạn vật lý CPU/RAM/SSD/HDD (Chặng 1) và định dạng tệp Parquet/Arrow (Chặng 2), qua hạ tầng phân tán HDFS/Kafka/Data Warehouse (Chặng 3) và mô hình hóa Kimball Star Schema/SCD2 (Chặng 4), tiến hóa từ Data Lake/Swamp (Chặng 5) lên Open Table Formats Delta/Iceberg/Hudi (Chặng 6) và quy hoạch Multi-Hop Medallion + Governance (Chặng 7)."
        )}

        <h3 id="storage-0-roadmap">3. Bảng Đối chiếu Lộ trình 7 Chặng (Mạch Nhân – Quả Slide ↔ Sách Kinh điển)</h3>
        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Chặng &amp; Trạm</th>
                <th>Trọng tâm Kiến thức (<code>05-storage-layer.pdf</code> + Sách Kinh điển)</th>
                <th>Nỗi đau (Pain Point) Khởi phát</th>
                <th>Cơ chế Giải quyết Nhân – Quả</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>CHẶNG 1</strong><br><strong>Nguyên liệu gốc &amp; Cơ chế vật lý</strong><br><em>(Trạm 1.1 ➔ 1.5)</em></td>
                <td>• Tháp độ trễ <code>CPU Cache (1 ns)</code> ➔ <code>RAM (100 ns)</code> ➔ <code>SSD (100 µs)</code> ➔ <code>HDD (10 ms)</code> ➔ <code>S3 (100 ms)</code>.<br>• <code>Spill-to-Disk</code>, <code>Random Seek</code> vs. <code>Sequential Scan</code>, <code>Hot/Warm/Cold Tier</code>, ranh giới <code>OLTP</code> vs. <code>OLAP</code>.</td>
                <td>Không có phần cứng nào vừa siêu nhanh như <code>RAM</code>, vừa rẻ như <code>S3</code>, lại vừa bền vững khi mất điện; chạy truy vấn phân tích trên DB bán hàng làm sập cả hệ thống.</td>
                <td>Phân tầng bộ nhớ theo nhiệt độ dữ liệu; ưu tiên đọc tuần tự (<code>Sequential Scan</code>) và tách rời hoàn toàn hệ thống giao dịch <code>OLTP</code> khỏi hệ thống phân tích <code>OLAP</code>.</td>
              </tr>
              <tr>
                <td><strong>CHẶNG 2</strong><br><strong>Mô hình Lưu trữ &amp; Định dạng Tệp</strong><br><em>(Trạm 2.1 ➔ 2.4)</em></td>
                <td>• <code>File</code> vs. <code>Block</code> vs. <code>Object Storage (S3/GCS/ADLS)</code>.<br>• <code>Row-oriented (CSV, Avro)</code> vs. <code>Columnar (Parquet, ORC)</code>.<br>• <code>In-Memory Apache Arrow</code>, nén <code>Snappy/ZSTD/Gzip</code> &amp; <code>Splittability</code>.</td>
                <td>Lưu <code>CSV</code> trên đĩa quét thừa <code>90%</code> cột không dùng; truyền dữ liệu giữa <code>JVM (Spark)</code> và <code>Python</code> tốn <code>80% CPU</code>; nén <code>Gzip</code> nguyên tệp làm <code>99/100</code> máy chủ ngồi chơi.</td>
                <td>Lưu <code>Object Storage</code> phẳng giá rẻ; xoay trục theo cột bằng <code>Parquet</code> (<code>Row Group + Footer Min/Max</code>) nén <code>Snappy/ZSTD</code> chia cắt được, và đọc <code>Zero-Copy</code> trên <code>RAM</code> bằng <code>Apache Arrow</code>.</td>
              </tr>
              <tr>
                <td><strong>CHẶNG 3</strong><br><strong>Hạ tầng Phân tán, Streaming &amp; Data Warehouse</strong><br><em>(Trạm 3.1 ➔ 3.5)</em></td>
                <td>• <code>Hadoop HDFS</code> (<code>NameNode</code>, <code>DataNode</code>, nhân bản <code>x3</code>, <code>Rack Topology</code>).<br>• Streaming <code>Apache Kafka &amp; CDC</code> (<code>Append-only Log</code>).<br>• <code>Data Warehouse</code> (<code>ACID</code>, <code>Schema-on-Write</code>, <code>MPP Columnar</code>) &amp; 3 hạn chế lịch sử.</td>
                <td>Một máy chủ đơn lẻ không chứa nổi <code>Petabyte</code> và chết cứng khi hỏng ổ đĩa; nạp dữ liệu theo lô (<code>Batch</code>) bị trễ hàng giờ; <code>Data Warehouse</code> đắt đỏ và bó tay trước ảnh/video/log thô.</td>
                <td>Phân mảnh khối <code>128 MB</code> nhân bản <code>x3</code> trên <code>HDFS</code>; truyền sự kiện thời gian thực qua <code>Kafka CDC</code>; dùng <code>Data Warehouse</code> cho <code>BI</code> chuẩn mực nhưng cần kiến trúc mở hơn cho <code>Unstructured Data &amp; AI/ML</code>.</td>
              </tr>
              <tr>
                <td><strong>CHẶNG 4</strong><br><strong>Kỹ thuật Thiết kế Mô hình Dữ liệu</strong><br><em>(Trạm 4.1 ➔ 4.5)</em></td>
                <td>• <code>Conceptual ➔ Logical ➔ Physical</code>.<br>• 3 trường phái: <code>Inmon (3NF)</code>, <code>Kimball (Dimensional)</code>, <code>Data Vault (Hub/Link/Satellite)</code>.<br>• <code>Fact</code> vs. <code>Dimension</code>, <code>Grain</code>, <code>Star/Snowflake/OBT</code>, <code>Surrogate Key</code>, <code>SCD Type 1/2/3</code> &amp; <code>Bus Matrix</code>.</td>
                <td>Đổ dữ liệu vào kho mà không có bản vẽ khiến <code>JOIN</code> hàng chục bảng chậm rì, cộng nhầm tỷ lệ phần trăm, và khi khách hàng đổi địa chỉ thì làm lệch toàn bộ doanh thu lịch sử.</td>
                <td>Thiết kế <code>Star Schema / OBT</code> xoay quanh <code>Fact</code> (<code>1 Grain</code> cố định) và <code>Conformed Dimensions</code> dùng khóa <code>Surrogate Key</code> kết hợp <code>SCD Type 2</code> để bảo toàn lịch sử theo thời gian.</td>
              </tr>
              <tr>
                <td><strong>CHẶNG 5</strong><br><strong>Từ Data Lake đến Data Swamp &amp; Lakehouse</strong><br><em>(Trạm 5.1 ➔ 5.4)</em></td>
                <td>• <code>Data Lake (Schema-on-Read, ELT)</code>.<br>• Bi kịch <code>Data Swamp</code> &amp; 3 lỗ hổng công cụ: Không <code>ACID</code> (<code>Zombie Files</code>), <code>Hive Partitioning</code> liệt kê chậm, <code>Schema Drift</code>.<br>• Phác đồ 6 trụ cột cứu nguy Data Lake.</td>
                <td>Đổ thẳng tệp <code>Parquet</code> lên <code>S3</code> giá rẻ nhưng khi Job <code>Spark</code> chết giữa chừng lại sinh tệp rác làm sai số liệu; xóa <code>1</code> dòng theo luật <code>GDPR</code> phải viết lại hàng nghìn tệp.</td>
                <td>Nhận diện giới hạn vật lý của <code>Object Storage</code> nguyên thủy (<code>Immutable Objects</code>, thiếu <code>Transactional Metadata Layer</code>) để dẫn tới sự ra đời tất yếu của <code>Data Lakehouse</code>.</td>
              </tr>
              <tr>
                <td><strong>CHẶNG 6</strong><br><strong>Open Table Formats (Delta Lake, Iceberg, Hudi)</strong><br><em>(Trạm 6.1 ➔ 6.5)</em></td>
                <td>• Định nghĩa lại <code>Bảng = Metadata Log + Parquet</code>.<br>• Giải phẫu <code>Delta Lake (_delta_log)</code>, <code>Apache Iceberg (Catalog ➔ Manifest)</code>, <code>Apache Hudi (Timeline)</code>.<br>• <code>ACID (OCC/MVCC)</code>, <code>Time Travel</code>, <code>COW vs. MOR</code>, <code>Compaction</code>, <code>Z-Order/Liquid Clustering</code>, <code>Deletion Vectors</code>, <code>Vacuum</code>.</td>
                <td>Làm sao mang trọn vẹn giao dịch <code>ACID</code>, kiểm soát lược đồ và cập nhật/xóa từng dòng của <code>Data Warehouse</code> đặt lên trên các tệp <code>Parquet</code> bất biến của <code>Cloud Object Storage</code>?</td>
                <td>Chèn tầng <code>Transactional Metadata</code> đứng gác cổng trước <code>Parquet</code>: mọi thao tác đọc/ghi đều thông qua nhật ký nguyên tử (<code>JSON/Avro Manifest</code>) kết hợp bảo trì vật lý thông minh.</td>
              </tr>
              <tr>
                <td><strong>CHẶNG 7</strong><br><strong>Kiến trúc Multi-Hop Medallion &amp; Governance</strong><br><em>(Trạm 7.1 ➔ 7.4)</em></td>
                <td>• Triết lý <code>Multi-Hop Medallion</code> (<code>Bronze ➔ Silver ➔ Gold</code>) &amp; trạm kiểm dịch <code>Quarantine</code>.<br>• <code>Undercurrents</code>: <code>Data Catalog (Unity Catalog)</code>, <code>OpenLineage</code>, <code>RLS/Column Masking</code>, <code>GDPR</code> &amp; <code>FinOps</code>.<br>• Bản đồ tổng thể 6 tầng (<code>Bottom-Up Blueprint</code>).</td>
                <td>Có công nghệ bảng <code>Lakehouse</code> nhưng nếu biến đổi <code>1-hop</code> từ nguồn bẩn ra thẳng báo cáo <code>CEO</code> thì đường ống gãy liên tục; <code>40</code> phòng ban tạo <code>40</code> bucket trùng lặp làm nổ hóa đơn <code>Cloud</code>.</td>
                <td>Tinh chế lũy tiến qua 3 tầng <code>Bronze (Raw) ➔ Silver (3NF/SCD2) ➔ Gold (Star/OBT)</code> đi kèm 4 dòng chảy ngầm (<code>Catalog, Lineage, Security, FinOps</code>) khép kín kiến trúc 6 tầng.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <hr />

        <h2 id="storage-1-1" tabindex="-1">TRẠM 1.1: BẬC THANG PHẦN CỨNG &amp; THANG ĐO ĐỘ TRỄ VẬT LÝ (CACHE HIERARCHY)</h2>

        <h3 id="storage-1-1-story">1. Câu chuyện của Đơn hàng #8888</h3>
        <p>Khi khách hàng bấm nút thanh toán <strong>Đơn hàng #8888</strong>, vi xử lý (CPU) của máy chủ bán hàng cần xử lý thông tin đơn hàng này ngay lập tức. Tuy nhiên, không có một thiết bị lưu trữ đơn lẻ nào trên thế giới vừa <strong>siêu nhanh</strong>, vừa <strong>siêu rẻ</strong>, lại vừa <strong>không mất dữ liệu khi cúp điện</strong>. Vì vậy, máy tính phải tổ chức lưu trữ thành một <strong>hệ thống phân tầng bộ nhớ đệm (Cache Hierarchy)</strong> — bắt đầu từ tối đa 4 tầng bộ nhớ đệm nằm ngay bên trong nhân CPU, đi xuống RAM, SSD và cuối cùng là Cloud Object Storage và Archival Storage.</p>

        <h3 id="storage-1-1-pyramid">2. Sơ đồ Kim tự tháp Độ trễ &amp; Thao tác Thực tế</h3>
        <p>Mỗi bước đi xuống dưới chân kim tự tháp, chi phí trên mỗi Gigabyte rẻ đi hàng chục đến hàng trăm lần, nhưng độ trễ truy xuất (Latency) lại chậm đi theo cấp số nhân:</p>

        ${buildVisualBlock(
          "storage-1-1",
          "Hình 1.1 — Tháp Độ trễ Vật lý & Các Tác vụ Thực tế (Cache Hierarchy)",
          d["1.1"].ascii,
          d["1.1"].mermaid,
          "Sơ đồ tổng hợp từ bảng phân tầng bộ nhớ thực nghiệm và thang đo độ trễ hệ thống."
        )}

        <h3 id="storage-1-1-table">3. Bảng thông số kỹ thuật chi tiết các tầng lưu trữ</h3>
        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Tầng lưu trữ</th>
                <th>Độ trễ truy xuất (Latency)</th>
                <th>Băng thông (Bandwidth)</th>
                <th>Chi phí ước tính</th>
                <th>Độ bền vững (Persistence)</th>
                <th>Vai trò trong kiến trúc dữ liệu</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>L1 / L2 / L3 CPU Cache</strong></td>
                <td><code>~1–10 ns</code></td>
                <td><code>~1 TB/s</code></td>
                <td>Cực đắt (On-die)</td>
                <td>Mất khi tắt điện</td>
                <td>Lưu chỉ lệnh và dữ liệu CPU đang tính toán tức thời.</td>
              </tr>
              <tr>
                <td><strong>RAM (DDR5 / DRAM)</strong></td>
                <td><code>~100 ns</code> (<code>0.1 µs</code>)</td>
                <td><code>~100 GB/s</code></td>
                <td><code>~$10 / GB</code></td>
                <td><strong>Khả biến (Volatile)</strong> — mất dưới 1 giây khi mất điện</td>
                <td>Vùng làm việc cho Spark, Caching (Redis/Memcached), DB In-memory.</td>
              </tr>
              <tr>
                <td><strong>SSD (NVMe / Flash)</strong></td>
                <td><code>~100 µs</code> (<code>0.1 ms</code>)</td>
                <td><code>~4 GB/s</code></td>
                <td><code>~$0.20 / GB</code></td>
                <td><strong>Bền vững (Nonvolatile)</strong></td>
                <td>Lưu trữ CSDL giao dịch (OLTP như PostgreSQL, RocksDB), bộ đệm đọc/ghi nhanh.</td>
              </tr>
              <tr>
                <td><strong>HDD (Đĩa từ cơ học)</strong></td>
                <td><code>~4–10 ms</code></td>
                <td><code>~200–300 MB/s</code></td>
                <td><code>~$0.03 / GB</code></td>
                <td><strong>Bền vững (Nonvolatile)</strong></td>
                <td>Cụm lưu trữ HDFS truyền thống, lưu trữ tuần tự khối lượng lớn giá rẻ.</td>
              </tr>
              <tr>
                <td><strong>Cloud Object Storage</strong></td>
                <td><code>~100 ms</code></td>
                <td><code>~3 GB/s</code> mỗi instance (nhờ đọc song song)</td>
                <td><code>~$0.02 / GB / tháng</code></td>
                <td>Bền vững tuyệt đối (<code>99.999999999%</code>)</td>
                <td>Xương sống của Data Lake / Lakehouse, lưu tệp Parquet/Delta/Iceberg/Hudi.</td>
              </tr>
              <tr>
                <td><strong>Cloud Archival (Glacier/Tape)</strong></td>
                <td><code>~12 giờ</code></td>
                <td>Ngang Object Storage khi dữ liệu đã sẵn sàng</td>
                <td><code>~$0.004 / GB / tháng</code> (rẻ bằng ~1/17 bản chuẩn)</td>
                <td>Bền vững tuyệt đối</td>
                <td>Lưu trữ tuân thủ pháp lý (Compliance) và sao lưu thảm họa dài hạn.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <hr />

        <h2 id="storage-1-2" tabindex="-1">TRẠM 1.2: ĐẶC TÍNH KỸ THUẬT CỦA RAM &amp; HIỆN TƯỢNG TRÀN BỘ NHỚ (SPILL-TO-DISK)</h2>

        <h3 id="storage-1-2-ram">1. Cơ chế hoạt động của RAM (1.1.3)</h3>
        <p>Bộ nhớ RAM (<code>DDR5 / DRAM</code>) được gắn trực tiếp vào không gian địa chỉ của CPU (<code>CPU address space</code>) theo nguyên lý kiến trúc <em>Von Neumann &amp; Harvard</em> để chứa cả <strong>mã lệnh (<code>code</code>)</strong> lẫn <strong>dữ liệu (<code>data</code>)</strong> với độ trễ chỉ <code>~100 ns</code> (nhanh gấp <strong>1.000 lần</strong> SSD) và băng thông <code>~100 GB/s</code>:</p>

        ${buildVisualBlock(
          "storage-1-2b",
          "Hình 1.2a — Giải phẫu Cơ học Bộ nhớ RAM: Address Space, DRAM Volatility & In-Memory Cache",
          d["1.2b"].ascii,
          d["1.2b"].mermaid,
          "Ánh xạ trực tiếp vào không gian địa chỉ CPU (~100 ns, ~100 GB/s), chu kỳ nạp tụ điện DRAM khả biến (< 1s) và vai trò tầng đệm của Redis / Memcached / Hazelcast."
        )}

        <p><strong>Quy tắc sống còn về Tính khả biến (<code>Volatility</code>):</strong> Vì các ô nhớ DRAM giữ bit bằng tụ điện cần nạp tươi liên tục, mất nguồn điện dưới <strong>1 giây</strong> sẽ xóa sạch dữ liệu trên RAM. Do đó, các hệ thống in-memory như <strong>Redis</strong> (đa cấu trúc dữ liệu kèm <code>RDB/AOF</code>), <strong>Memcached</strong> (key-value thuần) hay <strong>Hazelcast</strong> (in-memory data grid) đóng vai trò là tầng đệm tốc độ cao (<code>Cache</code>), còn dữ liệu gốc bắt buộc phải ghi xuống tầng đĩa bền vững.</p>

        <h3 id="storage-1-2-spill">2. Hiện tượng Tràn bộ nhớ — "Spill-to-Disk" (1.1.5)</h3>
        <p>Trong các hệ thống tính toán phân tán như Apache Spark, RAM đóng vai trò là vùng làm việc chính để thực hiện các phép biến đổi, sắp xếp và gom nhóm dữ liệu.</p>

        ${buildVisualBlock(
          "storage-1-2",
          "Hình 1.2b — Cơ chế Tràn bộ nhớ (Spill-to-Disk) trên Node tính toán Spark",
          d["1.2"].ascii,
          d["1.2"].mermaid,
          ""
        )}

        <ul>
          <li><strong>Hệ quả kỹ thuật:</strong> Khi xảy ra hiện tượng <strong>Spill-to-Disk</strong>, CPU phải ngừng tính toán để chờ ổ đĩa SSD (chậm hơn RAM <strong>1.000 lần</strong>) hoặc đĩa từ HDD (chậm hơn RAM tới <strong>40.000 – 100.000 lần</strong>), khiến thời gian chạy pipeline phân tích bị kéo dài đột biến.</li>
        </ul>

        <hr />

        <h2 id="storage-1-3" tabindex="-1">TRẠM 1.3: CƠ HỌC ĐĨA CỨNG (RANDOM SEEK VS. SEQUENTIAL SCAN) &amp; BÍ MẬT CỦA CLOUD STORAGE</h2>

        <p>Vì RAM quá đắt (<code>~$10/GB</code>) và mất dữ liệu khi tắt nguồn, toàn bộ 10 triệu đơn hàng như Đơn <code>#8888</code> bắt buộc phải được cất xuống đĩa cứng hoặc Cloud Object Storage. Tại đây, bạn phải đối mặt với quy luật cơ học của ổ đĩa.</p>

        <h3 id="storage-1-3-assets">1. Ba Tài sản Cốt lõi của một Ổ đĩa (The 3 Disk Assets)</h3>
        <p>Khi bạn mua hoặc thuê bất kỳ ổ đĩa nào trong cụm lưu trữ đám mây, mỗi ổ đĩa vật lý đều có đúng <strong>3 tài sản giới hạn</strong> mà nhà cung cấp đám mây và người dùng cùng khai thác: <strong>(1) Dung lượng lưu trữ (<code>Storage Capacity</code> — ví dụ <code>10 TB</code>)</strong>, <strong>(2) Số thao tác vào/ra mỗi giây (<code>IOPS</code> — ví dụ HDD chỉ đạt <code>~100 IOPS</code>)</strong>, và <strong>(3) Băng thông tối đa (<code>Maximum Bandwidth</code> — đọc tuần tự đạt <code>200–300 MB/s</code>)</strong>.</p>

        <h3 id="storage-1-3-compare">2. Đối chiếu: Tìm kiếm Ngẫu nhiên (Random Seek) vs. Quét Tuần tự (Sequential Scan / Streaming Transfer)</h3>

        ${buildVisualBlock(
          "storage-1-3",
          "Hình 1.3a — Random Seek (~100 IOPS) vs. Sequential Scan (200–300 MB/s)",
          d["1.3"].ascii,
          d["1.3"].mermaid,
          ""
        )}

        <ul>
          <li><strong>Tại sao <code>Random Seek</code> là kẻ thù của phân tích dữ liệu lớn, còn <code>Sequential Scan</code> là chìa khóa vàng?</strong> Mỗi lần nhảy đầu đọc trên HDD mất <code>4–10 ms</code> (giới hạn <code>~100 IOPS</code>); ngược lại, tổ chức dữ liệu thành các khối liền mạch để quét tuần tự (<code>Sequential Scan / Streaming Transfer</code>) giúp bỏ qua chi phí tìm kiếm và đọc thẳng ở tốc độ tối đa <code>200–300 MB/s</code>.</li>
        </ul>

        <h3 id="storage-1-3-secrets">3. Hai "Bí mật Nhà nghề" của Cloud Object Storage từ 3 Tài sản Đĩa</h3>

        ${buildVisualBlock(
          "storage-1-3b",
          "Hình 1.3b — Hai Bí mật Nhà nghề của Cloud Object Storage từ 3 Tài sản Đĩa",
          d["1.3b"].ascii,
          d["1.3b"].mermaid,
          "Đọc song song qua hàng nghìn ổ đĩa đạt ~3 GB/s (chuyển điểm nghẽn sang Mạng & CPU) và mô hình định giá Archival Storage rẻ bằng 1/17 (~$0.004/GB) trên cùng phần cứng vật lý."
        )}

        <ul>
          <li><strong>Đọc song song (<code>Parallel Reads</code>) &amp; Phân bổ 3 Tài sản Đĩa:</strong> Nhờ tán nhỏ dữ liệu ra hàng nghìn ổ đĩa để đọc song song qua mạng (<code>~3 GB/s</code> mỗi instance), Cloud Object Storage chuyển điểm nghẽn từ tốc độ đĩa đơn lẻ sang <strong>hạ tầng mạng (Network performance) và CPU</strong>. Đồng thời, trên cùng phần cứng vật lý với gói Standard (<code>~$0.02/GB</code>), gói <strong>Archival Storage</strong> trên GCP/AWS có giá rẻ bằng <strong>1/17 (<code>~$0.004/GB</code>)</strong> vì khách hàng chỉ mua phần <strong>dung lượng (Capacity)</strong> dư thừa và chấp nhận chờ tới <strong>12 giờ</strong> khi ổ đĩa rảnh rỗi <code>IOPS</code> mới xuất dữ liệu!</li>
        </ul>

        <hr />

        <h2 id="storage-1-4" tabindex="-1">TRẠM 1.4: PHÂN TẦNG NHIỆT ĐỘ LƯU TRỮ (DATA TEMPERATURE) &amp; KIẾN TRÚC ĐỆM ĐA TẦNG</h2>

        <p>Để cân bằng giữa tốc độ truy xuất và ngân sách lưu trữ cho hàng tỷ đơn hàng, kỹ sư dữ liệu phân loại dữ liệu theo <strong>3 mức nhiệt độ (Data Temperature)</strong>:</p>

        ${buildVisualBlock(
          "storage-1-4",
          "Hình 1.4 — Ba mức Nhiệt độ Lưu trữ: Hot Tier ──► Warm Tier ──► Cold / Archival Tier",
          d["1.4"].ascii,
          d["1.4"].mermaid,
          ""
        )}

        <ul>
          <li><strong>Đánh đổi chi phí (Cost Trade-offs):</strong> Nếu bạn lưu toàn bộ dữ liệu ở tầng Nóng (Hot storage), mọi truy vấn đều cực nhanh nhưng chi phí sẽ làm cạn kiệt ngân sách. Ngược lại, nếu đẩy hết xuống tầng Lạnh (Cold storage) để tiết kiệm tiền lưu trữ hàng tháng, bạn sẽ phải chịu thời gian chờ đợi kéo dài và chi phí xuất dữ liệu (retrieval cost) rất đắt mỗi khi cần đọc lại.</li>
          <li>
            <strong>Mẫu thiết kế thực tế — Đệm đa tầng (Multitier Caching với AWS EMR + S3 + HDFS):</strong>
            <p style="margin-top:6px;">Trong thực tế, các công cụ xử lý dữ liệu lớn kết hợp cả tầng Ấm và tầng Nóng: dữ liệu gốc được lưu trữ dài hạn và bền vững trên <strong>Amazon S3 (Object Storage - Warm tier)</strong>. Khi cần chạy một pipeline biến đổi phức tạp, kỹ sư bật một cụm tính toán tạm thời <strong>Amazon EMR</strong> có gắn ổ cứng <strong>SSD chạy HDFS cục bộ (Hot tier)</strong>. Hệ thống kéo dữ liệu từ S3 về SSD cục bộ để xử lý các bước trung gian với tốc độ cực nhanh, sau đó ghi kết quả cuối cùng trở lại S3 rồi <strong>xóa cụm EMR và ổ SSD tạm</strong> đi để không tốn tiền thuê phần cứng lúc nhàn rỗi.</p>
          </li>
        </ul>

        <hr />

        <h2 id="storage-1-5" tabindex="-1">TRẠM 1.5: RANH GIỚI HỆ THỐNG — SOURCE SYSTEM (OLTP) VS. STORAGE SYSTEM (OLAP)</h2>

        <p>Trạm cuối cùng của Chặng 1 trả lời câu hỏi: <em>Tại sao chúng ta không chạy báo cáo doanh thu trực tiếp trên cơ sở dữ liệu bán hàng vừa sinh ra Đơn hàng #8888, mà bắt buộc phải tách thành hai hệ thống riêng biệt?</em></p>

        ${buildVisualBlock(
          "storage-1-5",
          "Hình 1.5 — Ranh giới Hệ thống: Source System (OLTP) vs. Storage System (OLAP)",
          d["1.5"].ascii,
          d["1.5"].mermaid,
          ""
        )}

        <h3 id="storage-1-5-reasons">Ba lý do cốt tử bắt buộc phải tách rời OLTP và OLAP:</h3>
        <ol>
          <li><strong>Tránh xung đột tài nguyên (Resource Competition):</strong> Việc chạy đồng thời các tác vụ giao dịch (cần phản hồi mili-giây cho khách mua hàng) và các tác vụ phân tích nặng (quét hàng trăm triệu dòng ngốn sạch CPU và băng thông đĩa) trên cùng một cơ sở dữ liệu sẽ gây tranh chấp tài nguyên, làm treo ứng dụng bán hàng.</li>
          <li>
            <strong>Sự đối lập giữa Lưu theo Dòng (Row) và Lưu theo Cột (Columnar):</strong>
            <ul>
              <li>Hệ thống giao dịch (<strong>OLTP</strong>) cần đọc và cập nhật tại chỗ (in-place updates) toàn bộ thông tin của một đơn hàng cụ thể (<code>#8888</code>), nên lưu dữ liệu <strong>theo dòng (row-oriented)</strong> trên ổ SSD là lý tưởng nhất. Tuy nhiên, kiến trúc theo dòng này hoàn toàn thất bại khi phải quét phân tích ở quy mô dữ liệu lớn.</li>
              <li>Hệ thống phân tích (<strong>OLAP</strong>) cần tính toán thống kê trên một vài cột (như cột <code>Thành_Tiền</code>) xuyên qua hàng triệu dòng, nên bắt buộc phải dùng định dạng <strong>theo cột (columnar)</strong> để chỉ đọc đúng những cột cần thiết từ đĩa và đạt tỷ lệ nén cao. Ngược lại, cơ sở dữ liệu dạng cột lại cực kỳ kém hiệu quả cho các giao dịch cập nhật đơn lẻ.</li>
            </ul>
          </li>
          <li><strong>Sự đối lập giữa Chuẩn hóa (Normalization) và Phi chuẩn hóa (Denormalization):</strong> Hệ thống giao dịch chia nhỏ dữ liệu thành nhiều bảng chuẩn hóa để tránh dư thừa khi ghi, trong khi hệ thống phân tích ưu tiên gộp phẳng (phi chuẩn hóa) để tránh các phép nối bảng (<code>JOIN</code>) khổng lồ làm chậm truy vấn.</li>
        </ol>

        <section class="summary-section" id="storage-summary" tabindex="-1">
          <h2>TÓM TẮT BỎ TÚI CHẶNG 1 (5 QUY LUẬT VẬT LÝ)</h2>
          <ol>
            <li><strong>Định luật Kim tự tháp:</strong> Càng gần CPU (<code>Cache 1ns</code> ➔ <code>RAM 100ns</code>) càng nhanh nhưng đắt và mất dữ liệu khi mất điện (<code>Volatile</code>); càng xa CPU (<code>SSD 100µs</code> ➔ <code>HDD 4ms</code> ➔ <code>Object Storage 100ms</code> ➔ <code>Archive 12h</code>) càng rẻ và bền vững (<code>Nonvolatile</code>).</li>
            <li><strong>Định luật RAM &amp; Spill-to-Disk:</strong> RAM nhanh gấp <code>1.000 lần</code> SSD nhưng mất sạch dữ liệu dưới <code>1 giây</code> khi cúp điện; nếu tính toán vượt quá RAM gây tràn xuống đĩa (<code>Spill-to-Disk</code>), hiệu năng sẽ sụp đổ.</li>
            <li><strong>Định luật Cơ học Đĩa:</strong> Đĩa cứng có 3 tài sản (<code>Capacity</code>, <code>IOPS</code>, <code>Bandwidth</code>) — sợ nhảy tìm ngẫu nhiên (<code>Random Seek</code>), thích quét liền mạch (<code>Sequential Scan</code>).</li>
            <li><strong>Định luật Đám mây Song song:</strong> Cloud Object Storage thắng nhờ ghép hàng nghìn ổ đĩa đọc song song qua mạng đạt <code>~3 GB/s</code>, biến giới hạn ổ đĩa thành bài toán băng thông mạng và CPU.</li>
            <li><strong>Định luật Phân tách OLTP / OLAP:</strong> Hệ thống sinh dữ liệu giao dịch (<code>OLTP</code> - lưu theo dòng, SSD, chuẩn hóa) phải tách rời khỏi hệ thống lưu trữ phân tích (<code>OLAP</code> - lưu theo cột, quét tuần tự, phi chuẩn hóa).</li>
          </ol>
          <p style="margin-top:14px;"><strong>Chặng tiếp theo:</strong> <a href="#topic=D02&stage=2" onclick="selectStorageStage(2);return false;">Chặng 2: Mô hình Lưu trữ (File/Block/Object) &amp; Định dạng File (Avro, Parquet, Arrow) ──►</a></p>
        </section>
      </div>
    `;
  }

  function renderStorageChang2() {
    const d = HUB_DATA.storage_diagrams;
    return `
      <div class="prose">
        <p>Ở <strong>Chặng 1</strong>, chúng ta đã rút ra kết luận vật lý sống còn: Vì bộ nhớ RAM quá đắt (<code>~$10/GB</code>) và mất sạch dữ liệu ngay khi cúp điện, <strong>Đơn hàng <code>#8888</code></strong> sau khi sinh ra từ hệ thống bán hàng (OLTP) bắt buộc phải được chuyển sang một kho lưu trữ bền vững giá rẻ để bảo quản lâu dài cùng hàng triệu đơn hàng khác.</p>

        <p>Bước sang <strong>Chặng 2</strong>, người kỹ sư dữ liệu phải trả lời liên tiếp <strong>4 câu hỏi thiết kế cốt lõi</strong>:</p>
        <ol>
          <li><strong>Chọn "nhà kho" nào?</strong> Lưu theo cây thư mục (<strong>File Storage</strong>), xé thành khối byte thô (<strong>Block Storage</strong>), hay đóng gói thành kiện hàng phẳng (<strong>Object Storage</strong>)?</li>
          <li><strong>Xếp dữ liệu trên đĩa ra sao?</strong> Xếp nối tiếp theo hàng (<strong>Row: CSV, JSONL, Avro</strong>) hay xoay dọc theo cột (<strong>Columnar: Parquet, ORC</strong>)?</li>
          <li><strong>Khi bốc dữ liệu lên RAM tính toán thì sao?</strong> Làm thế nào để các công cụ khác ngôn ngữ đọc chung dữ liệu trên RAM mà không tốn CPU dịch lại (<strong>Apache Arrow</strong>)?</li>
          <li><strong>Nén chặt mà vẫn chia nhỏ được?</strong> Chọn thuật toán nén nào (<strong>Snappy, ZSTD, Gzip, Bzip2</strong>) để vừa nhẹ dung lượng, vừa khuếch đại băng thông đĩa/mạng mà không làm tê liệt cụm máy tính phân tán (<strong>Splittability</strong>)?</li>
        </ol>

        <hr />

        <h2 id="storage-2-1" tabindex="-1">TRẠM 2.1: BỘ BA MÔ HÌNH LƯU TRỮ CƠ SỞ — FILE VS. BLOCK VS. OBJECT STORAGE</h2>

        <h3 id="storage-2-1-analogy">1. Ẩn dụ đời thực: 3 Cách quản lý kho hàng</h3>
        <p>Khi dữ liệu nhị phân của Đơn hàng <code>#8888</code> nằm trên các cụm máy chủ, có 3 cách tổ chức logic hoàn toàn khác nhau:</p>
        <ul>
          <li><strong>File Storage ("Tủ hồ sơ văn phòng nhiều ngăn"):</strong> Bạn cất tờ hóa đơn <code>#8888</code> vào ngăn tủ <code>KinhDoanh</code>, mở tiếp cặp tài liệu <code>Năm 2026</code>, tìm kẹp giấy <code>Tháng 10</code>, rồi mới rút tờ <code>DonHang.csv</code> ra. Muốn lấy tài liệu, bạn bắt buộc phải đi theo đúng đường dẫn phân cấp từ gốc đến ngọn.</li>
          <li><strong>Block Storage ("Các mảnh ghép Lego đánh số"):</strong> Bạn lấy kéo cắt tờ hóa đơn <code>#8888</code> thành những mảnh giấy vuông vức bằng nhau (ví dụ <code>4KB</code> hoặc <code>512KB</code>), đánh số mã vạch (<code>Unique ID</code>) lên từng mảnh rồi rải vào các hộp đĩa khác nhau để lấy ra lắp lại nhanh nhất.</li>
          <li><strong>Object Storage ("Siêu kho bưu kiện phẳng kèm phiếu gửi đồ"):</strong> Không có tủ nhiều ngăn cũng không cắt vụn theo rãnh đĩa cấp thấp. Bạn bỏ toàn bộ dữ liệu vào một thùng hàng nguyên vẹn, dán lên vỏ thùng một chiếc tem gồm <strong>Mã định danh duy nhất (ID)</strong> và <strong>Phiếu mô tả chi tiết (Metadata)</strong>, rồi đặt vào một nhà kho mặt phẳng mênh mông (<code>Bucket</code>).</li>
        </ul>

        <h3 id="storage-2-1-visual">2. Sơ đồ trực quan hóa 3 Mô hình Lưu trữ Vật lý</h3>
        ${buildVisualBlock(
          "storage-2-1",
          "Hình 2.1a — Ba Mô hình Lưu trữ Cơ sở: File Storage vs. Block Storage vs. Object Storage",
          d["2.1"].ascii,
          d["2.1"].mermaid,
          "Đối chiếu kiến trúc cây thư mục phân cấp (File), khối byte cố định (Block) và không gian phẳng định danh qua Key-Value (Object)."
        )}

        <h3 id="storage-2-1-trials">3. Hành trình thử nghiệm chọn kho của Đơn hàng #8888</h3>
        <ul>
          <li><strong>[x] Thử nghiệm 1 — File Storage (NTFS/ext4, NAS/NFS/SMB):</strong> Lưu cây thư mục phân cấp (<code>directory tree</code>) kèm quyền truy cập, con trỏ thư mục và nhật ký phục hồi (<code>journaling</code>). Khi tích lũy hàng chục triệu tệp hóa đơn, bảng chỉ mục <code>inode table</code> và khóa đường dẫn (<code>path traversal locks</code>) bị quá tải, không thể mở rộng cho Big Data.</li>
          <li><strong>[x] Thử nghiệm 2 — Block Storage (SAN, AWS EBS, Local NVMe Instance Store):</strong> Chia dữ liệu thành khối cố định (<code>4KB–512KB</code>) cho độ trễ <code>&lt; 1 ms</code>. Trên đám mây có 2 nhánh: <strong>Virtualized Network Block (AWS EBS)</strong> nhân bản trong cùng 1 Availability Zone (tới <code>64 TiB</code>, <code>256.000 IOPS</code>, <code>4.000 MiB/s</code>, hỗ trợ <code>Point-in-time Differential Snapshots</code> xuống S3) và <strong>Local Instance Store (NVMe)</strong> làm bộ đệm tạm (mất sạch khi dừng VM). Lý tưởng cho OLTP DB / VM nhưng đắt đỏ và không thể chia sẻ song song xuyên cụm.</li>
          <li><strong>[+] Giải pháp đích thực — Cloud Object Storage (Amazon S3 / Azure Blob &amp; ADLS / GCS):</strong> Dịch vụ <code>serverless</code> hoạt động như kho <code>key-value</code> phẳng trong <code>Bucket</code>. Mỗi <code>Object</code> gồm <strong>3 thành phần</strong>: <strong>(1) ID (<code>Object Key</code></strong> như <code>orders/8888.parquet</code> — dấu <code>/</code> chỉ là tên chuỗi phẳng), <strong>(2) Metadata</strong> tùy biến không giới hạn, và <strong>(3) Data</strong> (chuỗi byte nhị phân truy cập qua <code>HTTP REST API PUT/GET</code>, tự động băm và rải qua nhiều Availability Zones).</li>
        </ul>

        <h3 id="storage-2-1-less-is-more">4. Triết lý "Less is More" (Ít hơn lại là Nhiều hơn) &amp; Quản trị Vòng đời Object Storage</h3>
        <p>Chính việc lược bỏ khả năng sửa tại chỗ (<code>Immutability</code>) và cây thư mục vật lý lại tạo nên sức mạnh quy mô đám mây của Object Storage:</p>

        ${buildVisualBlock(
          "storage-2-1b",
          "Hình 2.1b — Triết lý 'Less is More' của Cloud Object Storage: Immutability, Versioning & Lifecycle",
          d["2.1b"].ascii,
          d["2.1b"].mermaid,
          "Đánh đổi tính bất biến (Immutability) và độ trễ ~100 ms để loại bỏ cơ chế khóa tệp, đạt băng thông song song ~3 GB/s, tách rời Compute – Storage và quản trị vòng đời dữ liệu qua Storage Classes."
        )}

        <ul>
          <li><strong>Lưu ý vận hành thực tế:</strong> Dù Object Storage hỗ trợ đọc một phần tệp qua <code>HTTP Range Requests</code> (để đọc riêng Footer của Parquet) và đảm bảo <strong><code>Strong Read-After-Write Consistency</code></strong>, tính năng <code>Object Versioning</code> lưu <strong>bản sao nguyên khối (brute-force full copy)</strong> cho mỗi lần ghi đè (khác với Differential Snapshot của EBS) nên bắt buộc phải đi kèm <strong>Lifecycle Policies</strong> hạ cấp sang <code>Standard-IA</code>, <code>One Zone-IA</code> hoặc <code>Glacier Deep Archive</code> (<code>~$1/TB/tháng</code>).</li>
        </ul>

        <h3 id="storage-2-1-table">5. Bảng so sánh tổng hợp: Object Storage vs. Block Storage vs. File Storage</h3>
        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Tiêu chí kỹ thuật</th>
                <th>Object Storage (S3 / ADLS / GCS)</th>
                <th>Block Storage (SAN / EBS)</th>
                <th>File Storage (NAS / NTFS / ext4)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Đơn vị lưu trữ</strong></td>
                <td>Objects (<code>ID + Metadata + Data</code>)</td>
                <td>Blocks (Khối byte cố định có ID)</td>
                <td>Files (Tệp tin)</td>
              </tr>
              <tr>
                <td><strong>Cấu trúc tổ chức</strong></td>
                <td>Phẳng với các Buckets (<code>Flat with buckets</code>)</td>
                <td>Không có cấu trúc thư mục (<code>None</code>)</td>
                <td>Cây thư mục phân cấp (<code>Files and folders</code>)</td>
              </tr>
              <tr>
                <td><strong>Siêu dữ liệu (Metadata)</strong></td>
                <td>Gần như vô hạn và tùy biến tự do</td>
                <td>Hạn chế (Limited)</td>
                <td>Hạn chế (Limited: tên, quyền, con trỏ)</td>
              </tr>
              <tr>
                <td><strong>Hiệu năng &amp; Độ trễ</strong></td>
                <td>Độ trễ đầu tiên cao (<code>~100 ms</code>), nhưng băng thông đọc/ghi song song cực lớn (<code>~3 GB/s</code>)</td>
                <td>Hiệu năng cao, độ trễ cực thấp (<code>&lt; 1 ms</code>, tới <code>256.000 IOPS</code>)</td>
                <td>Chậm hơn Block Storage, nghẽn khi duyệt cây thư mục quá lớn</td>
              </tr>
              <tr>
                <td><strong>Khả năng mở rộng (Scalability)</strong></td>
                <td>Dễ dàng, gần như vô hạn (<code>Easy / Serverless</code>)</td>
                <td>Khó mở rộng xuyên cụm (<code>Not easy</code>)</td>
                <td>Dễ mở rộng ở quy mô vừa (<code>Easy</code>)</td>
              </tr>
              <tr>
                <td><strong>Sửa đổi tại chỗ (Modification)</strong></td>
                <td><strong>Không thể</strong> (Bất biến — phải tạo lại toàn bộ Object)</td>
                <td><strong>Có thể</strong> (Sửa trực tiếp từng Block tại chỗ)</td>
                <td><strong>Có thể</strong> (Sửa và ghi nối tiếp trực tiếp tệp)</td>
              </tr>
              <tr>
                <td><strong>Chi phí (Cost)</strong></td>
                <td>Rẻ (<code>~$0.02 / GB / tháng</code>)</td>
                <td>Đắt đỏ (<code>Expensive</code>)</td>
                <td>Đắt đỏ (<code>Expensive</code>)</td>
              </tr>
              <tr>
                <td><strong>Trường hợp sử dụng chính</strong></td>
                <td>Data Lake, Lakehouse, Backup, lưu trữ đa định dạng quy mô lớn</td>
                <td>Lưu trữ CSDL giao dịch (OLTP Database) và Máy ảo (VM)</td>
                <td>Chia sẻ tệp tin nội bộ (File sharing)</td>
              </tr>
            </tbody>
          </table>
        </div>

        <hr />

        <h2 id="storage-2-2" tabindex="-1">TRẠM 2.2: ĐỊNH DẠNG TỆP &amp; TUẦN TỰ HÓA (SERIALIZATION) — ROW (CSV, AVRO) VS. COLUMNAR (PARQUET, ORC)</h2>

        <h3 id="storage-2-2-story">1. Câu chuyện nối tiếp: Đã có kho S3, nhưng đóng gói Đơn hàng #8888 kiểu gì?</h3>
        <p>Đơn hàng <code>#8888</code> đã được quyết định lưu trên <strong>Object Storage (S3)</strong>. Nhưng dữ liệu khi nằm trong bộ nhớ của phần mềm thường tồn tại dưới dạng các đối tượng phức tạp nối nhau bằng con trỏ, không thể bê nguyên xi xuống đĩa hay truyền qua mạng. Quá trình làm phẳng (flattening) và đóng gói cấu trúc dữ liệu thành một chuỗi các byte tiêu chuẩn để đầu bên kia giải mã được gọi là <strong>Tuần tự hóa (Serialization)</strong>. Cách bạn chọn định dạng tuần tự hóa (File Format) sẽ quyết định trực tiếp chi phí CPU, tỷ lệ nén và tốc độ truy vấn của toàn hệ thống.</p>
        <p>Có 2 trường phái sắp xếp dữ liệu trái ngược nhau trên đĩa: <strong>Theo hàng (Row-oriented)</strong> và <strong>Theo cột theo phân đoạn (Column-oriented / Columnar)</strong>:</p>

        ${buildVisualBlock(
          "storage-2-2a",
          "Hình 2.2a — Đối chiếu Tuần tự hóa: Row-Oriented (CSV, Avro) vs. Column-Oriented (Parquet, ORC)",
          d["2.2a"].ascii,
          d["2.2a"].mermaid,
          "Bố trí nối tiếp từng bản ghi theo hàng (tối ưu ghi luồng/đọc trọn dòng) so với xoay dọc theo từng cột trong Row Group (tối ưu quét phân tích và nén)."
        )}

        <h3 id="storage-2-2-row">2. Trường phái 1: Định dạng theo Hàng (Row-Oriented: CSV, JSONL, Apache Avro)</h3>
        <ul>
          <li><strong>Văn bản thô (<code>CSV</code>, <code>JSON</code>, <code>XML</code>) vs. <code>JSON Lines (JSONL)</code>:</strong> Định dạng theo hàng tối ưu khi đọc trọn vẹn một bản ghi hoặc ghi nối đuôi luồng sự kiện. Tuy nhiên, CSV thiếu schema chặt chẽ, dễ lỗi ký tự thoát và tốn CPU phân tách chuỗi (<code>parse overhead</code>); còn <strong><code>JSONL</code></strong> (mỗi dòng 1 đối tượng JSON ngăn bởi <code>\n</code>) phù hợp làm bước đệm thu thập REST API trước khi chuyển sang dạng nhị phân/cột.</li>
          <li><strong>Chuẩn nhị phân theo hàng <code>Apache Avro</code>:</strong> Nhúng trực tiếp <strong>Schema JSON ở phần Header</strong> (<code>Self-describing</code>, hỗ trợ <code>Schema Evolution</code>) và mã hóa dữ liệu thành <strong>nhị phân (binary)</strong> nhỏ gọn. Đặc biệt, Avro chèn các mốc đồng bộ <strong><code>Sync Markers 16-byte</code></strong> giữa các khối giúp tệp vừa <strong>chia nhỏ đọc song song được (<code>splittable</code>)</strong>, vừa <strong>phục hồi an toàn đến mốc Sync Marker gần nhất</strong> nếu luồng ghi Streaming / Kafka / CDC bị sập nguồn giữa chừng.</li>
        </ul>

        <h3 id="storage-2-2-columnar">3. Trường phái 2: Định dạng theo Cột (Columnar-Oriented: Apache Parquet &amp; Apache ORC)</h3>
        <p>Khi Giám đốc hỏi: <em>"Tính tổng cột <code>Amount</code> của 10 triệu đơn hàng trong năm nay"</em>, định dạng theo hàng (CSV/Avro) buộc ổ đĩa phải đọc lướt qua toàn bộ các cột không liên quan (như <code>Tên khách</code>, <code>Địa chỉ</code>, <code>Ghi chú</code>). Định dạng theo cột (<strong>Apache Parquet</strong> và <strong>Apache ORC</strong>) giải quyết triệt để bài toán này bằng cách chia bảng thành các phân đoạn hàng (<code>Row Groups</code>), sau đó xoay trục dữ liệu và đóng gói riêng từng cột.</p>

        <h4>Giải phẫu bên trong một tệp Apache Parquet:</h4>
        ${buildVisualBlock(
          "storage-2-2b",
          "Hình 2.2b — Giải phẫu Cấu trúc Vật lý Bên trong Tệp Apache Parquet",
          d["2.2b"].ascii,
          d["2.2b"].mermaid,
          "Động cơ truy vấn (Spark/Trino/DuckDB) luôn đọc phần Footer Metadata ở đáy tệp trước tiên để cắt tỉa cột (Column Pruning) và nhảy cóc qua các Row Group không khớp điều kiện lọc (Data Skipping)."
        )}

        <ul>
          <li><strong>3 Vũ khí cốt lõi của Parquet &amp; Thuật toán <code>Google Dremel</code>:</strong> (1) <strong><code>Column Pruning</code></strong> đọc đúng <code>Byte Offset</code> của các cột cần thiết (giảm <strong>80–95% I/O</strong>); (2) <strong>Nén chuyên biệt theo cột</strong> nhờ <code>Dictionary Encoding</code>, <code>Run-Length Encoding (RLE)</code> và <code>Delta Encoding</code>; (3) <strong><code>Data Skipping / Predicate Pushdown</code></strong> nhảy bỏ qua cả Row Group dựa vào thống kê <code>Min / Max / Null Count</code> ở Footer; kết hợp thuật toán <strong>Google Dremel</strong> (dùng <code>Definition Levels</code> và <code>Repetition Levels</code>) để ép phẳng JSON lồng nhau thành các cột độc lập.</li>
          <li><strong>Đánh đổi của định dạng cột &amp; Mô hình <code>Hybrid Serialization</code>:</strong> Parquet tốn RAM giữ đệm <code>Row Group (128MB–1GB)</code>, hỏng tệp nếu sập nguồn trước khi ghi Footer, và cực đắt khi sửa lẻ 1 dòng; so với <code>Apache ORC</code>, Parquet được hỗ trợ rộng rãi hơn trên Cloud (Snowflake/BigQuery hỗ trợ cả <code>import</code> và <code>export</code> Parquet). Để vừa ghi luồng nhanh vừa quét cột nhanh, các bảng Lakehouse (Hudi, Iceberg) áp dụng <strong>Tuần tự hóa Lai (<code>Hybrid Serialization</code>)</strong>: bắt luồng cập nhật vào tệp dòng <code>Avro</code> rồi định kỳ <code>Compaction</code> sang tệp cột <code>Parquet</code>.</li>
        </ul>

        <hr />

        <h2 id="storage-2-3" tabindex="-1">TRẠM 2.3: TUẦN TỰ HÓA TRONG BỘ NHỚ (IN-MEMORY SERIALIZATION) — APACHE ARROW</h2>

        <h3 id="storage-2-3-pain">1. Nỗi đau khi dữ liệu đã lên tới RAM &amp; Giải pháp Chuẩn bộ nhớ cột Zero-Copy</h3>
        <p>Khi tệp <code>Parquet</code> chứa Đơn hàng <code>#8888</code> đã được đọc từ S3 lên RAM của Apache Spark (<code>JVM</code>) và cần truyền sang thư viện Python (<code>Pandas / PyArrow / ML</code>) trên cùng máy chủ: trước đây, vì mỗi ngôn ngữ sắp xếp byte trong RAM một kiểu, CPU lãng phí tới <strong>70–80% thời gian</strong> chỉ để <strong>Serialize / Deserialize</strong> và chép lại vùng nhớ. <strong>Apache Arrow</strong> giải quyết triệt để bằng cách thống nhất một bố cục bộ nhớ cột duy nhất trên RAM cho mọi ngôn ngữ (<code>C, C++, Go, Java, Python, R, Rust</code>):</p>

        ${buildVisualBlock(
          "storage-2-3",
          "Hình 2.3 — Tuần tự hóa Trong Bộ nhớ: Truyền thống vs. Apache Arrow Zero-Copy",
          d["2.3"].ascii,
          d["2.3"].mermaid,
          "Apache Arrow thống nhất một bố cục bộ nhớ cột duy nhất trên RAM, cho phép Spark (JVM), Python (Pandas/Polars) và C++/Rust đọc chung vùng nhớ qua con trỏ mà không tốn CPU dịch lại."
        )}

        <ul>
          <li><strong>Cơ chế <code>Zero-copy</code>, <code>Shredding</code> &amp; <code>Virtual Memory (mmap)</code>:</strong> Các tiến trình khác ngôn ngữ chỉ cần truyền con trỏ địa chỉ RAM để đọc trực tiếp dữ liệu (<strong>Zero-copy</strong>) và ép phẳng JSON lồng nhau thành mảng cột trong bộ nhớ (<strong>Shredding</strong>). Vì định dạng nhị phân của Arrow dùng chung cho cả RAM, mạng (<code>Arrow Flight</code>) và đĩa, hệ điều hành có thể dùng <strong>Virtual Memory (<code>mmap</code>)</strong> ánh xạ thẳng tệp từ đĩa vào không gian địa chỉ với <code>Zero Deserialization Overhead</code> — nền tảng tốc độ của <strong>Dremio, DuckDB, Polars</strong> và <strong>Spark Pandas UDF</strong>.</li>
        </ul>

        <hr />

        <h2 id="storage-2-4" tabindex="-1">TRẠM 2.4: KỸ THUẬT NÉN DỮ LIỆU (COMPRESSION) &amp; CẠM BẪY TÍNH PHÂN TÁCH (SPLITTABILITY)</h2>

        <h3 id="storage-2-4-leverage">1. Nguyên lý Nén Không Mất Dữ Liệu &amp; 3 Đòn bẩy Phần cứng</h3>
        <p>Trong kỹ thuật dữ liệu phân tích, chúng ta bắt buộc dùng <strong>nén không mất dữ liệu (<code>Lossless compression</code></strong> — mã hóa các chuỗi dư thừa lặp lại đạt tỷ lệ <code>2:1</code> đến <code>10:1</code> rồi khôi phục chính xác từng bit khi đọc, thay vì nén mất dữ liệu <code>Lossy</code> như JPEG/MP3). Nén dữ liệu tạo ra <strong>3 hiệu ứng đòn bẩy phần cứng (Hardware Leverage)</strong>:</p>

        ${buildVisualBlock(
          "storage-2-4b",
          "Hình 2.4a — Ba Đòn bẩy Phần cứng của Nén Dữ liệu Không Mất Mát (Lossless Compression)",
          d["2.4b"].ascii,
          d["2.4b"].mermaid,
          "Hiệu ứng khuếch đại phần cứng khi nén cột Parquet/ZSTD: giảm dung lượng đĩa 4–10 lần, tăng tốc độ quét đĩa hiệu dụng từ 200 MB/s lên 800 MB/s – 2 GB/s, và nhân băng thông mạng 10 Gbps lên tương đương 100 Gbps."
        )}

        <h3 id="storage-2-4-table">2. Bảng đặt lên bàn cân các Thuật toán Nén phổ biến</h3>
        <p>Mỗi thuật toán nén là một sự đánh đổi giữa <strong>Tỷ lệ nén (Không gian lưu trữ &amp; I/O)</strong> và <strong>Chi phí thời gian/tài nguyên của CPU (Tốc độ nén &amp; giải nén)</strong>:</p>
        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Thuật toán nén</th>
                <th>Tốc độ CPU (Nén / Giải nén)</th>
                <th>Tỷ lệ nén (Tiết kiệm dung lượng)</th>
                <th>Đặc điểm &amp; Trường hợp sử dụng trong Data Pipeline</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Snappy / LZ4 / LZFSE</strong></td>
                <td><strong>Cực nhanh</strong> (Ưu tiên tốc độ CPU tối đa)</td>
                <td>Trung bình – Khá (<code>Mức 2.5/5</code>)</td>
                <td>Thuật toán thế hệ mới ưu tiên tốc độ, cực kỳ phổ biến khi kết hợp với <strong>Apache Parquet</strong> và Spark để không làm nghẽn CPU khi truy vấn nóng.</td>
              </tr>
              <tr>
                <td><strong>Zstandard (ZSTD)</strong></td>
                <td><strong>Nhanh</strong> (Giải nén tiệm cận LZ4)</td>
                <td><strong>Rất cao</strong> (<code>Mức 4/5</code>)</td>
                <td>Chuẩn nén hiện đại cân bằng xuất sắc giữa tốc độ giải nén nhanh và tỷ lệ nén chặt; đang trở thành mặc định mới cho Parquet trên Lakehouse.</td>
              </tr>
              <tr>
                <td><strong>Gzip</strong></td>
                <td>Chậm (Tốn nhiều chu kỳ CPU)</td>
                <td>Cao (<code>Mức 4/5</code>)</td>
                <td>Rất phổ biến để nén tệp văn bản (<code>CSV</code>, <code>JSON</code>, <code>JSONL</code>, <code>XML</code>, <code>Log</code>), nhưng nén luồng nguyên khối nên <strong>không cắt nhỏ được (Non-splittable)</strong>.</td>
              </tr>
              <tr>
                <td><strong>Bzip2</strong></td>
                <td><strong>Rất chậm</strong> (Ngốn nặng tài nguyên CPU)</td>
                <td><strong>Rất cao</strong> (<code>Mức 5/5</code>)</td>
                <td>Nén văn bản cực chặt và hỗ trợ cắt theo block nhưng quá chậm cho các truy vấn phân tích tương tác quy mô lớn.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3 id="storage-2-4-splittable">3. Vấn đề Sống còn: Tính phân tách (Splittability) khi xử lý Phân tán</h3>
        <p>Khi bạn có một cụm gồm 100 máy chủ tính toán (như Apache Spark hoặc Hadoop) cùng đọc một tệp dữ liệu khổng lồ nặng <code>100 GB</code>, câu hỏi quyết định sống còn là: <strong>Tệp đã nén đó có thể chia nhỏ (<code>Splittable</code>) cho 100 máy cùng nhảy vào đọc các khúc khác nhau được không?</strong></p>

        ${buildVisualBlock(
          "storage-2-4",
          "Hình 2.4 — Tính Phân tách (Splittability): Nén Khối đơn Gzip vs. Container Formats (Parquet/Avro)",
          d["2.4"].ascii,
          d["2.4"].mermaid,
          "Nén nguyên tệp bằng Gzip (orders.csv.gz) biến tệp 100 GB thành một khối không thể cắt giữa chừng; trong khi Parquet và Avro chia dữ liệu thành các khối độc lập (Row Groups / Sync Markers) rồi mới nén từng khối."
        )}

        <ul>
          <li><strong>Tại sao <code>Parquet</code> và <code>Avro</code> giải quyết triệt để bài toán Splittability?</strong> Vì chúng là các <strong>Container Formats (Định dạng đóng gói theo thùng chứa)</strong>: thay vì lấy thuật toán nén bọc bên ngoài toàn bộ tệp lớn, chúng chia dữ liệu bên trong thành từng khối độc lập (<strong>Row Groups / Data Pages</strong> trong Parquet kèm mục lục Byte Offset ở Footer, hoặc các khối ngăn cách bởi <strong>Sync Markers 16-byte</strong> trong Avro) rồi mới nén riêng từng khối đó bằng <code>Snappy</code> hoặc <code>ZSTD</code>. Nhờ vậy, hàng trăm máy chủ có thể dùng HTTP Range Requests nhảy thẳng tới bất kỳ khối nào giữa tệp để đọc và giải nén song song cùng lúc!</li>
        </ul>

        <section class="summary-section" id="storage-2-summary" tabindex="-1">
          <h2>TÓM TẮT BỎ TÚI CHẶNG 2 (4 QUYẾT ĐỊNH THIẾT KẾ LƯU TRỮ)</h2>
          <ol>
            <li><strong>Chọn Mô hình Kho (Storage Model):</strong> Để lưu trữ lâu dài hàng chục triệu đơn hàng như <strong>Đơn <code>#8888</code></strong> với chi phí rẻ (<code>~$0.02/GB/tháng</code>) và mở rộng vô hạn, chọn <strong>Cloud Object Storage (S3/ADLS/GCS)</strong> thay cho File Storage và Block Storage — chấp nhận tính bất biến (<code>Immutability</code>) để đổi lấy băng thông đọc/ghi song song không khóa (lock-free) và tách rời Compute khỏi Storage.</li>
            <li><strong>Chọn Định dạng Luồng / Hàng (Row Serialization):</strong> Để truyền dữ liệu luồng (Streaming / Kafka / CDC) an toàn và chịu lỗi mất điện, đóng gói nhị phân theo hàng bằng <strong>Apache Avro</strong> (nhúng JSON Schema ở Header và chèn <code>Sync Markers 16-byte</code>).</li>
            <li><strong>Chọn Định dạng Phân tích / Cột (Columnar Serialization &amp; Compression):</strong> Để lưu trữ phân tích trên Object Storage, xoay dọc dữ liệu sang <strong>Apache Parquet</strong> nén bằng <strong>Snappy / ZSTD</strong> — kết hợp cắt tỉa cột (<code>Column Pruning</code>), nhảy cóc qua Row Group nhờ thống kê <code>Footer Min/Max</code> (<code>Data Skipping</code>), ép phẳng JSON lồng nhau bằng <code>Google Dremel</code>, và giữ nguyên tính phân tách (<code>Splittability</code>).</li>
            <li><strong>Chọn Chuẩn Bộ nhớ Trong RAM (In-Memory Serialization):</strong> Khi bốc dữ liệu lên RAM để tính toán xuyên ngôn ngữ (Spark JVM ➔ Python Pandas/ML/C++), dùng chuẩn bộ nhớ cột <strong>Apache Arrow</strong> để đọc trực tiếp <code>Zero-copy</code> mà không tốn CPU dịch lại.</li>
          </ol>
          <p style="margin-top:14px;"><strong>Chặng tiếp theo:</strong> <a href="#topic=D02&stage=3" onclick="selectStorageStage(3);return false;">Chặng 3: Hạ tầng Phân tán (HDFS &amp; Network Topology), Streaming (Kafka/CDC) &amp; Data Warehouse ──►</a></p>
        </section>
      </div>
    `;
  }

  function renderStorageChang3() {
    const d = HUB_DATA.storage_diagrams;
    return `
      <div class="prose">
        <p>Ở <strong>Chặng 2</strong>, <strong>Đơn hàng <code>#8888</code></strong> đã tìm được cách đóng gói tối ưu: dùng <strong>Apache Avro</strong> khi cần truyền theo từng dòng và dùng <strong>Apache Parquet</strong> (nén bằng <strong>Snappy/ZSTD</strong>) khi cần lưu trữ phân tích theo cột trên <strong>Cloud Object Storage</strong>.</p>

        <p>Bước sang <strong>Chặng 3 (Hạ tầng Phân tán, Streaming &amp; Kho dữ liệu Data Warehouse)</strong>, chúng ta sẽ giải quyết bài toán ở cấp độ toàn hệ thống:</p>
        <ol>
          <li><strong>Phối hợp hàng trăm máy chủ ra sao?</strong> Làm thế nào để lưu và xử lý các tệp dữ liệu khổng lồ trên cụm máy tính phân tán mà ổ cứng nào hỏng cũng không mất dữ liệu (<strong>Hadoop HDFS, Nhân bản x3, Erasure Coding &amp; Tô-pô mạng</strong>)?</li>
          <li><strong>Tăng tốc truy xuất &amp; Bắt mạch thời gian thực như thế nào?</strong> Làm sao kết hợp bộ nhớ đệm phân tán (<strong>Redis, Memcached, RocksDB</strong>) và đường ống luồng sự kiện (<strong>Apache Kafka &amp; CDC</strong>) để vận chuyển Đơn hàng <code>#8888</code> tức thời?</li>
          <li><strong>Đưa vào "Ngân hàng dữ liệu" (<code>Data Warehouse</code>) ra sao?</strong> Cách thức một Data Warehouse vận hành để phục vụ báo cáo BI chuẩn xác, và tại sao chính những giới hạn của nó lại châm ngòi cho cuộc cách mạng Data Lake / Lakehouse sau này?</li>
        </ol>

        <hr />

        <h2 id="storage-3-1" tabindex="-1">TRẠM 3.1: HẠ TẦNG LƯU TRỮ PHÂN TÁN — HADOOP HDFS (NAMENODE, DATANODE &amp; NHÂN BẢN X3)</h2>

        <h3 id="storage-3-1-analogy">1. Ẩn dụ đời thực: "Tổng công trình sư" và "Đội thủ kho"</h3>
        <p>Trước khi Cloud Object Storage thống trị, các công ty công nghệ lưu trữ hàng trăm Terabyte dữ liệu bằng hệ thống tệp phân tán <strong>HDFS (Hadoop Distributed File System)</strong> — được thiết kế dựa trên kiến trúc <strong>Google File System (GFS)</strong> để chứa khối lượng lớn dữ liệu thô đa dạng với chi phí hiệu quả trên phần cứng phổ thông. Hãy hình dung HDFS như một hệ thống kho vận gồm hai vai trò tách biệt:</p>
        <ul>
          <li><strong>NameNode ("Tổng công trình sư giữ sổ cái"):</strong> Ngồi ở trung tâm, không trực tiếp bê vác hàng hóa mà chỉ giữ cuốn sổ danh bạ (<code>metadata</code>: cây thư mục, quyền truy cập và bảng ánh xạ khối dữ liệu) ngay trong bộ nhớ RAM kèm nhật ký bền vững (<code>EditLog</code> / <code>FsImage</code>) để biết chính xác tệp đơn hàng nào bị cắt thành mấy mảnh và đang cất ở những nhà kho nào.</li>
          <li><strong>DataNodes ("Đội thủ kho trực tiếp giữ hàng"):</strong> Hàng chục hoặc hàng trăm máy chủ gắn ổ đĩa vật lý, chuyên nhận các mảnh dữ liệu thực tế để cất giữ, gửi báo cáo nhịp tim (<code>Heartbeat</code> &amp; <code>Blockreport</code>) định kỳ về NameNode và tự động sao chép dữ liệu cho nhau để phòng hờ hỏng ổ cứng.</li>
        </ul>

        <h3 id="storage-3-1-mechanics">2. Cơ chế hoạt động thực tế với Đơn hàng #8888</h3>
        <p>Giả sử tệp nhật ký chứa Đơn hàng <code>#8888</code> cùng hàng triệu đơn khác trong ngày có dung lượng <strong>1 GB</strong> được đẩy vào cụm HDFS có kích thước mỗi khối (<code>block size</code>) là <strong>128 MB</strong>:</p>

        ${buildVisualBlock(
          "storage-3-1",
          "Hình 3.1 — Kiến trúc Phân tán, Nhân bản (x3) & Tự chữa lành trong Hadoop HDFS",
          d["3.1"].ascii,
          d["3.1"].mermaid,
          "NameNode quản lý sổ danh bạ Metadata trên RAM; các DataNode lưu trữ khối dữ liệu vật lý 128 MB kèm cơ chế nhân bản x3, tự chữa lành (Self-healing) và đặt chung tính toán tại chỗ (In-place Compute)."
        )}

        <ul>
          <li><strong>Chia khối (<code>Block Splitting</code>) &amp; Đặt chung Tính toán – Lưu trữ (<code>Colocation of Compute and Storage</code>):</strong> Tệp 1 GB tự động được chia thành <strong>8 khối (blocks) 128 MB</strong> phân tán trên các máy chủ khác nhau. Khác biệt cốt lõi giữa HDFS và Cloud Object Storage là HDFS <strong>kết hợp tài nguyên tính toán và lưu trữ trên cùng một node</strong>: khi khung tính toán (như Apache Spark hoặc MapReduce) cần phân tích tệp này, nó đẩy các tác vụ quét và lọc (<code>Map tasks</code>) xuống chạy <strong>ngay tại chỗ (in-place processing)</strong> trên đúng 8 máy đang giữ 8 khối dữ liệu, giúp giảm mạnh lượng dữ liệu phải truyền qua mạng ở bước gom nhóm (<code>Shuffle / Reduce</code>).</li>
          <li><strong>Cơ chế nhân bản chống lỗi (<code>Replication Factor x3</code>) &amp; Tự chữa lành (<code>Self-healing</code>):</strong> Để bảo đảm độ bền và tính sẵn sàng cao trên các ổ đĩa từ giá rẻ, mỗi khối dữ liệu mặc định được nhân bản thành <strong>3 bản sao (x3)</strong> trên 3 DataNode khác nhau. Nếu một ổ đĩa hoặc một DataNode bị sập làm hệ số nhân bản của khối <code>#8888</code> tụt xuống dưới 3, <strong>NameNode</strong> sẽ phát hiện ngay và ra lệnh cho các DataNode còn sống tự động sao chép bù khối đó sang một node khỏe mạnh khác để khôi phục đủ hệ số <code>x3</code>.</li>
          <li><strong>Góc nhìn Kỹ sư (Từ sách gốc) — Đánh đổi giữa Nhân bản <code>x3</code> và Mã hóa Xóa (<code>Erasure Coding</code>):</strong> Nhân bản <code>x3</code> cực kỳ đơn giản và đọc nhanh, nhưng tiêu tốn <strong>200% dung lượng phụ trội</strong> (lưu <code>1 TB</code> dữ liệu gốc mất <code>3 TB</code> đĩa vật lý). Với các tập dữ liệu ấm/lạnh ít truy cập, HDFS hiện đại (HDFS 3.x) áp dụng <strong>Erasure Coding (ví dụ chuẩn Reed-Solomon <code>RS(6,3)</code> — 6 khối dữ liệu đi kèm 3 khối chẵn lẻ Parity)</strong>: vẫn chịu được 3 máy chủ hỏng cùng lúc nhưng chỉ tốn thêm <strong>50% dung lượng (<code>1.5x</code>)</strong>, đổi lại CPU phải tính toán phép toán XOR/Reed-Solomon và đọc qua mạng nhiều hơn khi khôi phục khối hỏng.</li>
          <li><strong>Ứng dụng lai trên đám mây (Hybrid S3 + HDFS trên AWS EMR &amp; Apache Druid):</strong> Dù các công ty nhỏ dần chuyển sang Cloud Object Storage để tránh chi phí vận hành cụm Hadoop vật lý, HDFS vẫn đóng vai trò trọng yếu trong các cụm lớn (hàng nghìn node) và các dịch vụ đám mây như <strong>Amazon EMR</strong>: kỹ sư bật cụm HDFS tạm thời trên ổ cứng <strong>SSD</strong>, kéo dữ liệu từ <strong>S3</strong> về xử lý trung gian trên HDFS cục bộ với tốc độ cực cao, rồi ghi kết quả cuối cùng về lại S3 trước khi xóa cụm EMR. Tương tự, động cơ phân tích thời gian thực <strong>Apache Druid</strong> chỉ giữ <strong>1 bản sao duy nhất</strong> trên ổ SSD cục bộ của cụm (giảm 3 lần chi phí SSD đắt đỏ) và dùng Object Storage làm tầng bảo toàn dữ liệu (durability layer) để khôi phục tự động khi node gặp sự cố.</li>
        </ul>

        <hr />

        <h2 id="storage-3-2" tabindex="-1">TRẠM 3.2: TÔ-PÔ MẠNG (NETWORK TOPOLOGY), KHOẢNG CÁCH MẠNG &amp; ĐỘNG CƠ CACHE PHÂN TÁN</h2>

        <h3 id="storage-3-2-networking">1. Tại sao Mạng lưới (Networking) và CPU lại là "Nguyên liệu của Lưu trữ"?</h3>
        <p>Khi mới học về lưu trữ, nhiều người chỉ nghĩ đến ổ cứng. Nhưng trong các hệ thống phân tán hiện đại, <strong>hạ tầng mạng (Networking) và CPU cũng là những nguyên liệu thô cốt lõi của hệ thống lưu trữ</strong>:</p>
        <ul>
          <li><strong>Chuyển dịch điểm nghẽn từ Đĩa sang Mạng:</strong> Một ổ đĩa từ đơn lẻ có tốc độ truyền khá thấp (<code>200–300 MB/s</code>), nhưng khi phân tán dữ liệu qua hàng nghìn ổ đĩa trong các cụm lưu trữ đám mây (trải rộng qua nhiều trung tâm dữ liệu và vùng sẵn sàng — <code>Availability Zones</code>), việc đọc dữ liệu diễn ra song song trên vô số ổ đĩa cùng lúc. Lúc này, tốc độ truyền dữ liệu tăng vọt và <strong>bị giới hạn chủ yếu bởi hiệu năng mạng (network performance) và CPU chứ không còn là tốc độ của từng ổ đĩa</strong>.</li>
        </ul>

        <h3 id="storage-3-2-topology">2. Tô-pô Mạng (Network Topology) &amp; Khoảng cách Mạng trong Trung tâm Dữ liệu</h3>
        <p>Trong một trung tâm dữ liệu, các máy chủ được xếp vào các tủ mạng (<strong>Racks</strong>), kết nối qua thiết bị chuyển mạch đầu tủ (<code>Top-of-Rack Switch - ToR</code>) rồi nối lên bộ chuyển mạch trung tâm (<code>Core Switch</code>) theo mô hình cây mạng. Khi một tác vụ tính toán cần đọc khối dữ liệu chứa Đơn hàng <code>#8888</code>, tốc độ băng thông phụ thuộc trực tiếp vào <strong>khoảng cách mạng</strong> giữa máy tính toán và nơi đặt khối dữ liệu:</p>

        ${buildVisualBlock(
          "storage-3-2",
          "Hình 3.2a — Mô hình Cây Mạng (Network Topology) & 3 Cấp độ Khoảng cách Dữ liệu",
          d["3.2"].ascii,
          d["3.2"].mermaid,
          "Ba cấp độ định vị dữ liệu trong cụm phân tán: Data-local (đọc ngay trên máy chủ), Rack-local (qua Switch nội bộ tủ mạng) và Off-rack (băng qua Core Switch liên tủ)."
        )}

        <p><strong>Quy tắc Đặt bản sao nhận biết Tủ mạng (<code>Rack-aware Replica Placement</code>):</strong> Để vừa ưu tiên đọc <code>Data-local / Rack-local</code> tránh nghẽn <code>Core Switch</code> (<code>Off-rack</code>), vừa chống sập toàn bộ 1 tủ mạng (mất điện hoặc cháy <code>ToR Switch</code>), HDFS đặt <strong>Bản sao 1 trên Node cục bộ ở Rack 1</strong>, đẩy <strong>Bản sao 2 sang một Node ở Rack 2</strong>, và đặt <strong>Bản sao 3 ở một Node khác ngay trong cùng Rack 2</strong>.</p>

        <h3 id="storage-3-2-cache">3. Sơ đồ &amp; Bảng So sánh 3 Động cơ Cache Bộ nhớ trong Đường ống Dữ liệu</h3>
        <p>Để tránh việc phải đọc đi đọc lại qua mạng hoặc ổ đĩa cho các dữ liệu "Nóng" (Hot data — như kết quả truy vấn lặp lại, phản hồi API hoặc trạng thái luồng streaming của Đơn <code>#8888</code>), các hệ thống sử dụng 3 động cơ bộ nhớ đệm tốc độ dưới 1 mili-giây (<code>Sub-millisecond</code>) sau:</p>

        ${buildVisualBlock(
          "storage-3-2b",
          "Hình 3.2b — Giải phẫu 3 Động cơ Cache Dưới 1 Mili-giây: Redis vs. Memcached vs. RocksDB LSM-Tree",
          d["3.2b"].ascii,
          d["3.2b"].mermaid,
          "Đối chiếu 3 động cơ cache dưới 1 mili-giây: Redis (đa cấu trúc dữ liệu + RDB/AOF + TTL), Memcached (Key-Value thuần túy không bền vững), và RocksDB (Embedded LSM-Tree: WAL + MemTable ➔ SSTables làm State Backend cho Apache Flink / Kafka Streams)."
        )}

        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Tiêu chí kỹ thuật</th>
                <th>Redis</th>
                <th>Memcached</th>
                <th>RocksDB</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Mô hình kiến trúc</strong></td>
                <td>In-memory Data Structure Store (Client-Server)</td>
                <td>In-memory Key-Value Cache đơn giản (Client-Server)</td>
                <td>Embedded Key-Value Store nhúng trực tiếp vào tiến trình (<code>LSM-Tree</code>)</td>
              </tr>
              <tr>
                <td><strong>Độ trễ truy xuất</strong></td>
                <td>Dưới 1 mili-giây (<code>~100 ns</code> RAM access + mạng)</td>
                <td>Dưới 1 mili-giây (<code>~10 µs</code> gói tin mạng LAN 1Gbps)</td>
                <td>Dưới 1 mili-giây (<code>~100 µs</code> đọc từ RAM MemTable / NVMe SSD cục bộ)</td>
              </tr>
              <tr>
                <td><strong>Cấu trúc dữ liệu</strong></td>
                <td>Đa dạng: Strings, Hashes, Lists, Sets, Sorted Sets, Bitmaps</td>
                <td>Đơn giản: Chỉ hỗ trợ kiểu chuỗi ký tự (Strings) hoặc số nguyên (Integers)</td>
                <td>Key-Value dạng chuỗi byte nhị phân tùy biến</td>
              </tr>
              <tr>
                <td><strong>Lưu trữ bền vững (Persistence)</strong></td>
                <td><strong>Có</strong> (Chụp <code>RDB Snapshots</code> và ghi nhật ký <code>AOF</code> — cấu hình điển hình ghi đĩa mỗi <strong>~2 giây</strong>, chấp nhận mất lượng nhỏ dữ liệu mới nhất khi sập nguồn)</td>
                <td><strong>Không</strong> (Bộ nhớ thuần túy, mất điện là mất dữ liệu hoàn toàn)</td>
                <td><strong>Có</strong> (Ghi liên tục vào <code>WAL</code> + <code>MemTable</code> và xả xuống đĩa thành các tệp <code>SSTable</code> bất biến theo cấu trúc <code>Log-Structured Merge-tree</code>)</td>
              </tr>
              <tr>
                <td><strong>Vai trò thực tế trong Data Pipeline</strong></td>
                <td>Bộ nhớ đệm phân tán dùng chung, tra cứu nhanh (kèm cấu hình <code>TTL - Time to Live</code> để tránh đầy bộ nhớ nóng)</td>
                <td>Lớp đệm kết quả truy vấn DB và phản hồi API tốc độ cực thấp giúp giảm tải hệ thống backend</td>
                <td>Động cơ lưu trữ trạng thái cục bộ (<strong>State Backend</strong>) bên trong <strong>Apache Flink, Kafka Streams</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <hr />

        <h2 id="storage-3-3" tabindex="-1">TRẠM 3.3: LƯU TRỮ DẠNG LUỒNG (STREAMING STORAGE) — APACHE KAFKA &amp; CDC</h2>

        <h3 id="storage-3-3-story">1. Câu chuyện của Đơn hàng #8888: Làm sao truyền tin tức thời mà không mất dấu?</h3>
        <p>Khi khách hàng vừa tạo Đơn hàng <code>#8888</code> hoặc cập nhật địa chỉ giao hàng trên cơ sở dữ liệu giao dịch (OLTP), luồng <strong>CDC (Change Data Capture)</strong> bắt lấy từng sự kiện thay đổi từ nhật ký giao dịch để đẩy liên tục vào <strong>Apache Kafka</strong> — nền tảng lưu trữ luồng phân tán hoạt động theo nguyên lý <strong>ghi nhật ký tuần tự nối đuôi (<code>append-only log</code>)</strong>:</p>

        ${buildVisualBlock(
          "storage-3-3",
          "Hình 3.3 — Cơ chế Ghi Nhật ký Nối đuôi (Append-only Log), Replay & Stream-to-Batch của Apache Kafka",
          d["3.3"].ascii,
          d["3.3"].mermaid,
          "Sự kiện CDC từ DB giao dịch được ghi nối đuôi tuần tự theo thứ tự Offset vào Kafka Topic, hỗ trợ lưu trữ dài hạn trên Object Storage, tua lại lịch sử (Replay) và đồng thời nuôi cả luồng thời gian thực lẫn kho phân tích."
        )}

        <ul>
          <li><strong>Sequential I/O, <code>Tiered Storage</code> &amp; <code>Replay</code>:</strong> Vì Kafka chỉ ghi nối đuôi tuần tự (<code>append-only log</code>) kết hợp nén tốc độ cao (<code>LZ4 / Snappy / ZSTD</code>), toàn bộ thao tác đĩa đều là <code>Sequential I/O</code> chịu tải hàng triệu sự kiện/giây. Khác với hàng đợi tin nhắn truyền thống (<code>Message Queues</code>) xóa tin ngay sau khi đọc, Kafka (cùng <code>Kinesis, Pulsar, Pub/Sub</code>) đẩy các phân đoạn cũ xuống <strong>Cloud Object Storage (<code>Tiered Storage</code>)</strong> để lưu giữ dài hạn, cho phép kỹ sư tua con trỏ <code>Offset</code> về quá khứ để <strong>phát lại lịch sử (<code>Replay</code>)</strong>.</li>
          <li><strong>Kiến trúc <code>Stream-to-Batch</code>:</strong> Một Topic Kafka đồng thời nuôi cả luồng xử lý thời gian thực (<code>Apache Flink</code>) lẫn nhánh <strong>Batch Storage Consumer</strong> (như <code>AWS Kinesis Firehose</code> gom lô xuống S3, hoặc <code>Google BigQuery Streaming Buffer</code> tự động chuyển đổi sang định dạng cột).</li>
        </ul>

        <hr />

        <h2 id="storage-3-4" tabindex="-1">TRẠM 3.4: KHO DỮ LIỆU TẬP TRUNG — DATA WAREHOUSE (OLAP, ACID &amp; ĐỘNG CƠ LƯU TRỮ)</h2>

        <h3 id="storage-3-4-essence">1. Bản chất của Data Warehouse: "Ngân hàng dữ liệu có cấu trúc"</h3>
        <p>Khi Đơn hàng <code>#8888</code> đi qua quy trình <strong>ETL / ELT (Extract - Transform - Load)</strong> để tập hợp cùng dữ liệu từ các hệ thống vận hành (<code>Operational data</code>) và dữ liệu bên ngoài (<code>External data</code>), nó được nạp vào <strong>Data Warehouse (Kho dữ liệu)</strong>. Về mặt lịch sử lưu trữ, Data Warehouse đã tiến hóa qua 4 thế hệ: từ việc chạy chung trên RDBMS giao dịch truyền thống ➔ hệ thống xử lý song song hàng loạt theo hàng (<strong>Row-based MPP</strong> như <code>Teradata</code>, <code>IBM Netezza</code>) ➔ hệ thống <strong>Columnar MPP</strong> (như <code>Vertica</code>, <code>Teradata Columnar</code>) ➔ và nay là <strong>Cloud Data Warehouses</strong> tách rời tính toán với lưu trữ (như <code>Google BigQuery</code>, <code>Snowflake</code>, <code>Amazon Redshift</code>).</p>

        ${buildVisualBlock(
          "storage-3-4",
          "Hình 3.4 — Kiến trúc Luồng Dữ liệu trong Data Warehouse & 3 Rào cản Lịch sử",
          d["3.4"].ascii,
          d["3.4"].mermaid,
          "Mô hình tiến hóa kho dữ liệu: gom dữ liệu vận hành và đối tác qua ETL (Schema-on-Write) vào Data Warehouse đảm bảo ACID, tối ưu hóa bằng lưu trữ cột, Micro-partitioning và bộ nhớ đệm truy vấn cho BI."
        )}

        <h3 id="storage-3-4-features">2. Các đặc tính kỹ thuật cốt lõi của Data Warehouse</h3>
        <ul>
          <li><strong><code>Schema-on-Write</code>, Giao dịch <code>ACID</code> &amp; <code>Query Results Cache</code>:</strong> Mọi dữ liệu có cấu trúc (<code>Structured data</code>) khi ghi vào bảng bắt buộc phải tuân thủ lược đồ nghiêm ngặt (<code>Schema-on-Write</code>) và đảm bảo giao dịch <strong>ACID</strong>. Động cơ lưu trữ dạng cột kết hợp với <strong>bộ nhớ đệm kết quả truy vấn (<code>Query results cache</code> - Hot data)</strong> giúp các báo cáo BI lặp lại phản hồi tức thì mà không cần quét lại kho.</li>
          <li><strong><code>Partitioning</code>, <code>Clustering</code> &amp; <code>Snowflake Micro-partitioning</code>:</strong> Thay vì dùng chỉ mục B-Tree như OLTP, các Cloud Data Warehouse chia bảng theo phân vùng ngày tháng và sắp xếp các giá trị tương đồng nằm cạnh nhau (<code>Clustering</code>) — điển hình là <strong>Micro-partitioning của Snowflake</strong> tự động chia bảng thành các phân đoạn cột lai (<em>Hybrid Columnar</em>) từ <strong><code>50 MB – 500 MB</code> (chưa nén)</strong> kèm thống kê Metadata trung tâm để cắt tỉa (<code>pruning</code>) siêu tốc.</li>
          <li><strong><code>Hybrid Object Storage</code> (BigQuery Colossus / S3 Select) &amp; <code>Zero-Copy Cloning</code>:</strong> <strong>Google BigQuery</strong> dùng hệ thống tệp <strong>Colossus</strong> đặt gần các khối dữ liệu (<code>colocate</code>), còn AWS có <strong>S3 Select</strong> lọc dữ liệu ngay tại tầng lưu trữ; đồng thời các Cloud DW cho phép tạo bản sao ảo (<code>Zero-Copy Cloning / Shallow Copy</code>) cho môi trường Test/Dev chỉ bằng cách tạo con trỏ metadata mới trỏ vào tệp gốc mà không tốn dung lượng nhân bản.</li>
        </ul>

        <hr />

        <h2 id="storage-3-5" tabindex="-1">TRẠM 3.5: BA HẠN CHẾ LỊCH SỬ CỦA DATA WAREHOUSE (TẠI SAO PHẢI TIẾN HÓA?)</h2>

        <p>Dù Data Warehouse xử lý các bảng số liệu của Đơn hàng <code>#8888</code> rất tuyệt vời cho báo cáo BI, nhưng khi doanh nghiệp bước vào kỷ nguyên Big Data và AI/Machine Learning, Data Warehouse bộc lộ <strong>3 rào cản lớn</strong>:</p>

        ${buildVisualBlock(
          "storage-3-5",
          "Hình 3.5 — Ba Rào cản Lịch sử của Data Warehouse Thúc đẩy Tiến hóa lên Data Lake & Lakehouse",
          d["3.5"].ascii,
          d["3.5"].mermaid,
          "Ba giới hạn cốt tử của Data Warehouse truyền thống: (1) Bó tay trước dữ liệu phi cấu trúc (ảnh, âm thanh, video), (2) Chi phí đắt đỏ ở quy mô Petabyte, và (3) Định dạng lưu trữ đóng kín (Vendor Lock-in) ngăn cản các động cơ AI/ML đọc trực tiếp."
        )}

        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Hạn chế của Data Warehouse</th>
                <th>Chuyện gì xảy ra với Đơn hàng <code>#8888</code>?</th>
                <th>Hệ quả đối với Doanh nghiệp</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>1. Bó tay trước Dữ liệu Phi cấu trúc (<code>Unstructured Data</code>)</strong></td>
                <td>Đơn <code>#8888</code> phát sinh thêm ảnh chụp kiện hàng Sofa, video camera kho bãi, file âm thanh cuộc gọi tổng đài và văn bản đánh giá tự do.</td>
                <td>Data Warehouse truyền thống và đám mây có thể xử lý bảng có cấu trúc và văn bản JSON bán cấu trúc, nhưng <strong>không thể lưu trữ trực tiếp dữ liệu phi cấu trúc thực sự (hình ảnh, âm thanh, video)</strong> phục vụ cho các đường ống Computer Vision / Audio / Deep Learning.</td>
              </tr>
              <tr>
                <td><strong>2. Chi phí đắt đỏ ở quy mô lớn (<code>Expensive at Scale</code>)</strong></td>
                <td>Sau 5 năm, lịch sử hàng chục tỷ đơn hàng và nhật ký hành vi người dùng phình lên hàng Petabyte với tốc độ sinh dữ liệu cực nhanh (Volume, Velocity, Variety).</td>
                <td>Lưu trữ và mở rộng quy mô lớn trên Data Warehouse chuyên dụng (đặc biệt là các hệ thống MPP độc quyền) có <strong>chi phí lưu trữ và tính toán rất đắt đỏ</strong> so với việc lưu tệp thô trên Object Storage hoặc HDFS.</td>
              </tr>
              <tr>
                <td><strong>3. Khó chia sẻ đa động cơ &amp; Khóa chặt nhà cung cấp (<code>Closed Storage Engine &amp; Vendor Lock-in</code>)</strong></td>
                <td>Đội ngũ Data Science muốn dùng Python, Spark hoặc Rust đọc trực tiếp các tệp dữ liệu gốc để huấn luyện mô hình AI.</td>
                <td>Các kho dữ liệu đóng kín định dạng lưu trữ độc quyền bên dưới (không phơi bày tệp mở trực tiếp ra ngoài), buộc kỹ sư phải tốn thời gian và chi phí tuần tự hóa lại (<code>reserializing overhead</code>) hoặc xuất dữ liệu qua nhiều bước ETL phức tạp.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <section class="summary-section" id="storage-3-summary" tabindex="-1">
          <h2>TÓM TẮT BỎ TÚI CHẶNG 3 (MẠCH NHÂN – QUẢ HẠ TẦNG PHÂN TÁN, STREAMING &amp; DATA WAREHOUSE)</h2>
          <ol>
            <li><strong>Lưu trữ &amp; Tính toán Phân tán (Hadoop HDFS &amp; Tô-pô mạng):</strong> Khi dữ liệu vượt quá sức chứa của 1 máy, <strong>HDFS</strong> chia tệp thành các khối <strong>128 MB</strong>, dùng <strong>NameNode</strong> quản lý danh mục metadata và <strong>DataNodes</strong> lưu trữ kèm <strong>nhân bản x3</strong> (hoặc <strong>Erasure Coding <code>1.5x</code></strong>) trên nhiều tủ mạng, ưu tiên đẩy tác vụ về xử lý <strong>Data-local / Rack-local</strong> để tránh nghẽn băng thông mạng.</li>
            <li><strong>Đệm Nóng &amp; Lưu trữ Luồng Thời gian thực (Cache &amp; Apache Kafka / CDC):</strong> Để truyền dữ liệu thời gian thực, luồng <strong>CDC</strong> bắt thay đổi từ DB giao dịch đẩy vào nhật ký nối đuôi <strong>Apache Kafka (<code>append-only log</code>)</strong> hỗ trợ lưu trữ dài hạn và phát lại lịch sử (<code>Replay</code>), kết hợp cùng các bộ nhớ đệm dưới 1 mili-giây (<strong>Redis</strong>, <strong>Memcached</strong>, và <strong>RocksDB LSM-Tree</strong> cho trạng thái streaming).</li>
            <li><strong>Kho Dữ liệu Tập trung &amp; Lực đẩy Tiến hóa (Data Warehouse):</strong> Để phục vụ báo cáo quản trị (BI), dữ liệu có cấu trúc được đưa qua <strong>ETL (<code>Schema-on-Write</code>)</strong> vào <strong>Data Warehouse</strong> (đảm bảo <strong>ACID</strong>, lưu trữ dạng cột, <code>Micro-partitioning</code>, <code>Query results cache</code>, <code>Hybrid Object Storage</code> và <code>Zero-Copy Cloning</code>) — nhưng chính 3 giới hạn về dữ liệu phi cấu trúc, chi phí quy mô lớn và định dạng đóng kín sẽ dẫn tới sự ra đời của Data Lake và Lakehouse.</li>
          </ol>
          <p style="margin-top:14px;"><strong>Câu hỏi mở ra Chặng 4 (Data Modeling &amp; Kimball):</strong> Khi Đơn hàng <code>#8888</code> đã nằm gọn trong <strong>Data Warehouse</strong> rồi, làm thế nào để người kỹ sư thiết kế các bảng dữ liệu bên trong kho đó? Giữa ba trường phái lớn là <strong>Bill Inmon (Top-down 3NF)</strong>, <strong>Ralph Kimball (Bottom-up Star Schema)</strong> và <strong>Dan Linstedt (Data Vault)</strong>, tại sao mô hình <strong>Fact / Dimension, Star Schema, Surrogate Key và SCD (Type 1, 2, 3)</strong> của Kimball lại trở thành chuẩn mực không thể thiếu? <a href="#topic=D02&stage=4" onclick="selectStorageStage(4);return false;">Đọc tiếp Chặng 4: Kỹ thuật Thiết kế Mô hình Dữ liệu (Kimball, Inmon, Data Vault &amp; SCD) ──►</a></p>
        </section>
      </div>
    `;
  }

  function renderStorageChang4() {
    const d = HUB_DATA.storage_diagrams;
    return `
      <div class="prose">
        <p>Ở <strong>Chặng 3</strong>, <strong>Đơn hàng <code>#8888</code></strong> đã vượt qua đường ống ETL để đặt chân vào bên trong <strong>Data Warehouse (Kho dữ liệu)</strong>. Nhưng lúc này, một bài toán thiết kế mới lại nảy sinh: <em>Nếu chúng ta bê nguyên xi hàng trăm bảng dữ liệu có cấu trúc phức tạp từ phần mềm bán hàng (OLTP) vào trong Data Warehouse, chuyện gì sẽ xảy ra?</em></p>

        <p>Khi Giám đốc Kinh doanh mở công cụ BI (như Power BI hoặc Tableau) để hỏi một câu đơn giản: <em>"Doanh thu bán hàng tại khu vực Bình Dương trong tháng này là bao nhiêu?"</em>, hệ thống sẽ phải nối (<code>JOIN</code>) hàng chục bảng chằng chịt với nhau, khiến câu lệnh chạy chậm rì rì và người dùng nghiệp vụ hoàn toàn bị lạc lối.</p>

        <p>Đó là lý do ở <strong>Chặng 4 (Trạm cuối của Phần 1)</strong>, chúng ta phải học nghệ thuật <strong>Mô hình hóa dữ liệu (Data Modeling)</strong> và bộ kỹ thuật kinh điển của <strong>Ralph Kimball</strong> để sắp xếp lại Đơn hàng <code>#8888</code> sao cho <strong>dễ hiểu nhất với con người và truy vấn nhanh nhất với máy tính</strong>.</p>

        <hr />

        <h2 id="storage-4-1" tabindex="-1">TRẠM 4.1: BA CẤP ĐỘ THIẾT KẾ MÔ HÌNH DỮ LIỆU (CONCEPTUAL ➔ LOGICAL ➔ PHYSICAL)</h2>

        <h3 id="storage-4-1-analogy">1. Ẩn dụ đời thực: "Ba bản vẽ của người Kiến trúc sư xây nhà"</h3>
        <p>Trước khi đổ bê tông xây dựng các bảng dữ liệu trong kho để chứa Đơn hàng <code>#8888</code>, người kỹ sư dữ liệu không bao giờ gõ lệnh tạo bảng ngay lập tức mà phải đi qua <strong>3 cấp độ thiết kế từ trừu tượng đến vật lý</strong>:</p>
        <ul>
          <li><strong>Conceptual Model (Mô hình Khái niệm — "Bản phác thảo nói chuyện với Chủ nhà"):</strong> Bản vẽ tổng quan nhất dùng để giao tiếp với ban giám đốc và bộ phận kinh doanh (Business), chỉ xác định các thực thể kinh doanh chính và mối quan hệ giữa chúng mà chưa bận tâm đến cột hay phần mềm nào.</li>
          <li><strong>Logical Model (Mô hình Logic — "Bản thiết kế kiến trúc chi tiết"):</strong> Đi sâu vào chi tiết hóa từng bảng, liệt kê tên các cột thuộc tính (<code>attributes</code>), xác định rõ khóa chính (<code>PK</code>) và khóa ngoại (<code>FK</code>), nhưng vẫn hoàn toàn độc lập với phần mềm cơ sở dữ liệu cụ thể.</li>
          <li><strong>Physical Model (Mô hình Vật lý — "Bản vẽ thi công điện nước thực tế"):</strong> Triển khai bản thiết kế lên một hệ quản trị cơ sở dữ liệu cụ thể, quyết định chính xác kiểu dữ liệu vật lý, cách chia phân vùng (<code>Partitioning</code>), gom cụm (<code>Clustering</code>) và đánh chỉ mục (<code>Indexing</code>).</li>
        </ul>

        <h3 id="storage-4-1-diagram">2. Sơ đồ tiến hóa của Đơn hàng <code>#8888</code> qua 3 cấp độ thiết kế</h3>

        ${buildVisualBlock(
          "storage-4-1",
          "Hình 4.1 — Tiến hóa của Đơn hàng #8888 qua 3 Cấp độ Thiết kế: Conceptual ➔ Logical ➔ Physical",
          d["4.1"].ascii,
          d["4.1"].mermaid,
          "Từ bản vẽ thực thể kinh doanh (Conceptual) sang lược đồ bảng/cột/khóa độc lập hệ quản trị (Logical) và triển khai vật lý trên CSDL (Physical)."
        )}

        <ul>
          <li><strong>Quy trình 4 Bước Thiết kế Mô hình Chiều của Ralph Kimball (<code>Kimball's 4-Step Dimensional Design Process</code>):</strong> Để chuyển hóa từ bài toán nghiệp vụ ở mức <em>Conceptual</em> sang bản thiết kế <em>Logical &amp; Physical</em> cho Đơn hàng <code>#8888</code>, Kimball đặt ra 4 bước bắt buộc theo đúng thứ tự: <strong>(1) Chọn quy trình nghiệp vụ (<code>Select the Business Process</code>)</strong> — ví dụ: quy trình bán lẻ tại cửa hàng; <strong>(2) Tuyên bố Độ mịn (<code>Declare the Grain</code>)</strong> — xác định chính xác 1 dòng trong bảng Fact đại diện cho cái gì; <strong>(3) Xác định các Chiều ngữ cảnh (<code>Identify the Dimensions</code>)</strong> — <em>Ai, Cái gì, Ở đâu, Khi nào</em>; và <strong>(4) Xác định các Số đo sự kiện (<code>Identify the Facts</code>)</strong> — các con số định lượng tại đúng độ mịn đó.</li>
        </ul>

        <hr />

        <h2 id="storage-4-2" tabindex="-1">TRẠM 4.2: BA TRƯỜNG PHÁI MÔ HÌNH HÓA TRONG DATA WAREHOUSE (INMON VS. KIMBALL VS. DATA VAULT)</h2>

        <p>Khi bước vào thiết kế cấu trúc kho dữ liệu cho doanh nghiệp, lịch sử ngành dữ liệu chia thành <strong>3 trường phái lớn</strong> với triết lý tiếp cận rất khác nhau:</p>

        ${buildVisualBlock(
          "storage-4-2",
          "Hình 4.2 — Ba Trường phái Mô hình hóa Data Warehouse: Bill Inmon vs. Ralph Kimball vs. Data Vault",
          d["4.2"].ascii,
          d["4.2"].mermaid,
          "Đối chiếu kiến trúc: Inmon (Top-down 3NF Enterprise DW phân phối xuống Data Marts), Kimball (Bottom-up Star Schema phục vụ BI trực tiếp) và Data Vault (Hubs, Links, Satellites nạp Insert-only)."
        )}

        <ol>
          <li><strong>Trường phái Bill Inmon (<code>Top-down 3NF</code>):</strong> Tích hợp dữ liệu toàn công ty vào một Enterprise Data Warehouse chuẩn hóa dạng chuẩn 3 (<code>3NF</code>) thỏa mãn <strong>4 tính chất (<code>Subject-oriented</code>, <code>Integrated</code>, <code>Nonvolatile</code>, <code>Time-variant</code>)</strong> để tạo <em>"một hình ảnh vật lý thống nhất cho toàn công ty" (single physical corporate image)</em> trước, sau đó mới phân phối xuống các <strong>Data Marts</strong> phòng ban (<em>"Một Data Mart không bao giờ là vật thay thế cho một Data Warehouse"</em>).</li>
          <li><strong>Trường phái Ralph Kimball (<code>Bottom-up Dimensional</code>):</strong> Chấp nhận <strong>phi chuẩn hóa (<code>denormalization</code>)</strong>, mô hình hóa trực tiếp từng quy trình kinh doanh bằng bảng <strong>Fact</strong> và <strong>Dimension</strong> (Star Schema) giúp triển khai nhanh và tối ưu tốc độ truy vấn BI cho dữ liệu theo lô (<code>batch data</code>).</li>
          <li><strong>Trường phái Data Vault (Dan Linstedt — <code>Insert-only Auditability</code>):</strong> Tách cấu trúc khóa khỏi thuộc tính mô tả qua 3 loại bảng chỉ chèn mới (<code>insert-only</code>): <strong><code>Hub</code></strong> (thực thể chính gồm 4 cột: <code>Hash Key MD5/SHA-256</code>, <code>Business Key</code>, <code>Load Date</code>, <code>Record Source</code>), <strong><code>Link</code></strong> (quan hệ giao điểm nhiều-nhiều giữa các Hubs), và <strong><code>Satellite</code></strong> (thuộc tính mô tả biến thiên theo thời gian gắn với Hub/Link), sau đó chiếu sang Star Schema ở tầng trình bày BI.</li>
        </ol>

        <hr />

        <h2 id="storage-4-3" tabindex="-1">TRẠM 4.3: TRÁI TIM CỦA KIMBALL — BẢNG SỰ KIỆN (FACT) VS. BẢNG THỨ NGUYÊN (DIMENSION) &amp; ĐỘ MỊN (GRAIN)</h2>

        <p>Trong phương pháp <strong>Mô hình hóa chiều (Dimensional Modeling)</strong> của Ralph Kimball, toàn bộ dữ liệu xoay quanh Đơn hàng <code>#8888</code> được tách bạch thành hai loại bảng cốt lõi: <strong>Bảng Fact (Sự kiện / Đo lường)</strong> và <strong>Bảng Dimension (Thứ nguyên / Ngữ cảnh)</strong>:</p>

        ${buildVisualBlock(
          "storage-4-3",
          "Hình 4.3a — Phân tách Đơn hàng #8888 thành Bảng Dimension (Ngữ cảnh) và Bảng Fact (Đo lường tại 1 Grain)",
          d["4.3"].ascii,
          d["4.3"].mermaid,
          "Bảng Dimension (Rộng & Ngắn) cung cấp ngữ cảnh lọc/gom nhóm nối qua khóa PK/FK vào bảng Fact (Hẹp & Rất dài) chứa các số đo định lượng bất biến tại một độ mịn nguyên tử cố định."
        )}

        <h3 id="storage-4-3-fact">1. Quy tắc Sống còn của Bảng Fact &amp; Bảng Dimension</h3>
        <ul>
          <li><strong>Bảng Fact (<code>Narrow &amp; Long</code>, <code>Immutable &amp; Append-only</code>):</strong> Lưu các con số định lượng tại <strong>độ mịn nguyên tử thấp nhất (<code>lowest atomic grain</code>)</strong>; tuyệt đối không trộn lẫn số đo lệch độ mịn (như tiền lương cửa hàng trưởng vào bảng giao dịch bán lẻ), không nối trực tiếp 2 bảng Fact với nhau, và giữ mã hóa đơn <code>Ma_Don = 8888</code> làm <strong>Chiều suy biến (<code>Degenerate Dimension - DD</code>)</strong>.</li>
          <li><strong>Bảng Dimension (<code>Wide &amp; Short</code>):</strong> Lưu thuộc tính văn bản phi chuẩn hóa trả lời <em>Ai, Cái gì, Ở đâu, Khi nào</em> phục vụ lọc (<code>WHERE</code>) và gom nhóm (<code>GROUP BY</code>), luôn đi kèm bảng <strong><code>Dim_Date</code></strong> tạo sẵn theo khóa thông minh <code>YYYYMMDD</code> (như <code>20261015</code>).</li>
        </ul>

        <h3 id="storage-4-3-additivity">2. Phân loại Số đo (<code>Additivity</code>) &amp; 3 Kiểu Bảng Fact Chuẩn của Kimball</h3>

        ${buildVisualBlock(
          "storage-4-3b",
          "Hình 4.3b — Phân loại Số đo (Additivity) & 3 Kiểu Bảng Fact Chuẩn của Ralph Kimball",
          d["4.3b"].ascii,
          d["4.3b"].mermaid,
          "Ba mức cộng gộp số đo (Additive, Semi-additive, Non-additive) và ba kiểu bảng Fact chuẩn (Transaction Fact, Periodic Snapshot Fact, Accumulating Snapshot Fact)."
        )}

        <hr />

        <h2 id="storage-4-4" tabindex="-1">TRẠM 4.4: BA KIẾN TRÚC BỐ TRÍ BẢNG — STAR SCHEMA VS. SNOWFLAKE SCHEMA VS. OBT (&amp; OLAP CUBES)</h2>

        <p>Khi ghép bảng <code>Fact</code> và các bảng <code>Dimension</code> lại với nhau, người kỹ sư có <strong>3 lựa chọn kiến trúc sơ đồ</strong> tùy thuộc vào công cụ truy vấn và bài toán hiệu năng:</p>

        <h3 id="storage-4-4-diagram">1. Sơ đồ trực quan hóa 3 Kiến trúc: Star Schema vs. Snowflake Schema vs. OBT</h3>

        ${buildVisualBlock(
          "storage-4-4",
          "Hình 4.4 — Ba Kiến trúc Bố trí Bảng: Star Schema vs. Snowflake Schema vs. OBT (One Big Table)",
          d["4.4"].ascii,
          d["4.4"].mermaid,
          "Đối chiếu cấu trúc kết nối: Star Schema (1 cấp JOIN từ Fact ra các Dimension phi chuẩn hóa), Snowflake Schema (chuẩn hóa tách nhánh Sub-dimension, tốn nhiều JOIN) và OBT (bảng phẳng gộp sẵn toàn bộ cột, 0 JOIN)."
        )}

        <h3 id="storage-4-4-table">2. Đặt lên bàn cân: Khi nào dùng Star, Snowflake, OBT hay OLAP Cube?</h3>
        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Mô hình kiến trúc</th>
                <th>Cấu trúc thiết kế</th>
                <th>Ưu điểm &amp; Lý do chọn</th>
                <th>Đánh đổi / Lưu ý kỹ thuật</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Star Schema (Lược đồ Hình sao)</strong></td>
                <td>1 bảng Fact ở tâm nối trực tiếp với nhiều bảng Dimension phi chuẩn hóa xung quanh qua khóa <code>PK/FK</code>.</td>
                <td><strong>Chuẩn mực vàng cho BI (Power BI / Tableau):</strong> Đơn giản, người dùng nghiệp vụ rất dễ hiểu, cần rất ít phép <code>JOIN</code> nên tốc độ truy vấn cực nhanh.</td>
                <td>Chấp nhận dư thừa dữ liệu văn bản trong các bảng Dimension phi chuẩn hóa.</td>
              </tr>
              <tr>
                <td><strong>Snowflake Schema (Hình bông tuyết)</strong></td>
                <td>Bản mở rộng của Star Schema, trong đó các bảng Dimension được chuẩn hóa (<code>normalized</code>) tách thành nhiều bảng <code>Sub-dimension</code> liên kết nhau.</td>
                <td>Giảm sự trùng lặp dữ liệu trong các bảng chiều phân cấp.</td>
                <td>Phức tạp hơn và đòi hỏi <strong>nhiều phép <code>JOIN</code> hơn</strong> khi truy vấn so với Star Schema.</td>
              </tr>
              <tr>
                <td><strong>OBT (One Big Table)</strong></td>
                <td>Bảng phẳng gộp sẵn toàn bộ các cột Dimension vào thẳng bảng Fact.</td>
                <td><strong>Không tốn chi phí <code>JOIN</code>:</strong> Cực kỳ nhanh khi chạy quét phân tích trên các động cơ lưu trữ cột đám mây (<code>Cloud Columnar Engines</code>) nhờ cơ chế nén từ điển (<code>RLE / Dictionary Encoding</code>) trên các cột lặp lại.</td>
                <td>Tốn dung lượng lưu trữ lặp lại và tốn chi phí ghi lại toàn bộ bảng lớn (<code>table rewrite</code>) khi một thuộc tính chiều thay đổi.</td>
              </tr>
              <tr>
                <td><strong>OLAP Cubes (Khối đa chiều)</strong></td>
                <td>Cấu trúc chiều được triển khai trên hệ cơ sở dữ liệu đa chiều (<code>multidimensional database</code>), truy cập qua ngôn ngữ chuyên biệt như <code>XMLA</code> và <code>MDX</code> thay vì chỉ dùng SQL.</td>
                <td>Khả năng phân tích đa chiều mạnh mẽ, tương đương về mặt nội dung hoặc được dẫn xuất từ Star Schema.</td>
                <td>Kimball khuyến nghị luôn nạp dữ liệu chi tiết nguyên tử vào <strong>Star Schema trên RDBMS làm nền móng vật lý trước</strong>, sau đó mới đổ dữ liệu sang các OLAP Cubes tùy chọn.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <p><strong>Lưu ý thiết kế quan trọng của Kimball:</strong> Một sơ đồ Star Schema <strong>không nên được thiết kế chỉ để phục vụ cho một báo cáo đơn lẻ</strong>, mà phải nắm bắt toàn bộ các sự kiện và thuộc tính của quy trình kinh doanh tại khu vực trình bày (<code>Presentation Area</code>) để đủ linh hoạt trả lời mọi câu hỏi quan trọng; các báo cáo cụ thể sẽ được tạo ở tầng BI phía sau.</p>

        <hr />

        <h2 id="storage-4-5" tabindex="-1">TRẠM 4.5: BỘ BA KỸ THUẬT SỐNG CÒN CỦA KIMBALL — SURROGATE KEY, SCD (TYPE 1, 2 &amp; 3) &amp; BUS MATRIX</h2>

        <p>Đây là trạm kiến thức thực chiến quan trọng nhất thường xuyên xuất hiện trong các buổi phỏng vấn và thiết kế kiến trúc Data Warehouse thực tế:</p>

        <h3 id="storage-4-5-sk">1. Khóa thay thế (<code>Surrogate Keys</code>) vs. Khóa tự nhiên (<code>Natural Keys</code>)</h3>
        <ul>
          <li><strong>Vấn đề thực tế:</strong> Trên hệ thống phần mềm bán hàng nguồn, khách hàng đặt Đơn <code>#8888</code> có mã tự nhiên (<code>Natural Key</code>) là <code>'KH_001'</code>. Nếu bạn dùng thẳng mã <code>'KH_001'</code> làm khóa chính trong Data Warehouse, kho dữ liệu của bạn sẽ bị phụ thuộc chặt vào hệ thống nguồn (ví dụ: nguồn đổi quy tắc đặt mã hoặc gộp nhiều nguồn bị trùng mã) và không thể lưu được nhiều phiên bản lịch sử của cùng một khách hàng.</li>
          <li><strong>Giải pháp <code>Surrogate Key</code>:</strong> Kimball sử dụng một <strong>khóa số nguyên tự sinh vô nghĩa về mặt nghiệp vụ (<code>Surrogate Key</code> — ví dụ: <code>101</code>, <code>205</code>)</strong> để thay thế hoàn toàn cho mã tự nhiên của hệ thống nguồn khi nối bảng <code>Fact</code> và <code>Dimension</code>, giúp <strong>cách ly Data Warehouse khỏi biến động của hệ thống nguồn</strong>, tăng tốc độ phép nối (<code>JOIN</code> trên số nguyên 4-byte/8-byte nhanh hơn nhiều so với chuỗi ký tự) và làm nền tảng bắt buộc để xử lý lịch sử <strong>SCD</strong>.</li>
        </ul>

        <h3 id="storage-4-5-scd">2. Quản lý chiều thay đổi chậm — <code>SCD (Slowly Changing Dimensions: Type 1, Type 2 &amp; Type 3)</code></h3>
        <p>Dữ liệu trong bảng Fact là bất biến, nhưng thông tin trong bảng Dimension lại thay đổi theo thời gian — gọi là <strong>Slowly Changing Dimensions (SCD)</strong>. Hãy xem điều gì xảy ra với Đơn hàng <code>#8888</code> (mua ngày <code>15/10/2026</code> tại <strong>Bình Dương</strong>, <code>5.000.000 VNĐ</code>) khi khách hàng <strong>Nguyễn Văn A (<code>'KH_001'</code>)</strong> chuyển nhà lên <strong>TP.HCM</strong> vào ngày <code>01/11/2026</code> và mua tiếp Đơn <code>#9999</code> (<code>8.000.000 VNĐ</code>):</p>

        ${buildVisualBlock(
          "storage-4-5a",
          "Hình 4.5a — Đối chiếu Trực quan 3 Chiến lược SCD: Type 1 (Ghi đè) vs. Type 2 (Thêm dòng) vs. Type 3 (Thêm cột)",
          d["4.5a"].ascii,
          d["4.5a"].mermaid,
          "Tác động lên báo cáo lịch sử của Đơn hàng #8888 khi khách hàng chuyển từ Bình Dương lên TP.HCM: SCD Type 1 làm mất dấu lịch sử, SCD Type 2 bảo toàn trọn vẹn nhờ Surrogate Key mới (101 ➔ 205), và SCD Type 3 mở thêm cột trạng thái cũ/mới trên cùng dòng."
        )}

        <p><em>Chi tiết bảng <code>Dim_Customer</code> và <code>Fact_Sales</code> khi áp dụng chuẩn vàng <strong><code>SCD Type 2</code></strong> (dùng bộ 3 cột <code>start_date</code>, <code>end_date</code>, <code>is_current</code>):</em></p>
        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Customer_SK (PK)</th>
                <th>Customer_NK</th>
                <th>Ten_Khach</th>
                <th>Tinh_Thanh</th>
                <th><code>start_date</code></th>
                <th><code>end_date</code></th>
                <th><code>is_current</code></th>
                <th>Kết quả JOIN từ <code>Fact_Sales</code></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong><code>101</code></strong></td>
                <td><code>'KH_001'</code></td>
                <td>Nguyễn Văn A</td>
                <td><strong>Bình Dương</strong></td>
                <td><code>2026-01-01</code></td>
                <td><code>2026-10-31</code></td>
                <td><code>False</code></td>
                <td>Đơn <strong><code>#8888</code></strong> (<code>15/10</code>) nối vào <code>SK = 101</code> ➔ Giữ đúng <code>5M</code> cho <strong>Bình Dương</strong>!</td>
              </tr>
              <tr>
                <td><strong><code>205</code></strong></td>
                <td><code>'KH_001'</code></td>
                <td>Nguyễn Văn A</td>
                <td><strong>TP.HCM</strong></td>
                <td><code>2026-11-01</code></td>
                <td><code>9999-12-31</code></td>
                <td><code>True</code></td>
                <td>Đơn <strong><code>#9999</code></strong> (<code>05/11</code>) nối vào <code>SK = 205</code> ➔ Ghi đúng <code>8M</code> cho <strong>TP.HCM</strong>!</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3 id="storage-4-5-bus">3. Kiến trúc Tuyến Doanh nghiệp (<code>Enterprise DW Bus Matrix</code>) &amp; Chiều đồng nhất (<code>Conformed Dimensions</code>)</h3>
        <p>Mảnh ghép cuối cùng của Kimball giải quyết bài toán quy hoạch toàn công ty:</p>
        <ul>
          <li><strong>Nguy cơ phân mảnh:</strong> Nếu phòng Kinh doanh, phòng Kho vận và phòng Tài chính mỗi bên tự xây dựng các bảng Dimension riêng rẽ không theo chuẩn chung, báo cáo toàn công ty sẽ không thể ghép nối với nhau (rơi vào bẫy <em>Isolated Data Marts</em> mà Bill Inmon từng cảnh báo).</li>
          <li><strong>Giải pháp <code>Enterprise Bus Matrix</code>:</strong> Là một bảng ma trận quy hoạch trong đó các hàng là các <strong>quy trình nghiệp vụ (<code>Business Processes</code> — như Bán lẻ <code>Retail Sales</code>, Tồn kho <code>Inventory</code>, Mua hàng <code>Procurement</code>)</strong> và các cột là các <strong>chiều dùng chung (<code>Conformed Dimensions</code> — như <code>Dim_Date</code>, <code>Dim_Product</code>, <code>Dim_Customer</code>, <code>Dim_Store</code>)</strong>.</li>
        </ul>

        ${buildVisualBlock(
          "storage-4-5",
          "Hình 4.5b — Ma trận Tuyến Doanh nghiệp (Enterprise DW Bus Matrix) & Conformed Dimensions",
          d["4.5"].ascii,
          d["4.5"].mermaid,
          "Ma trận quy hoạch kho dữ liệu của Ralph Kimball: kết nối các quy trình nghiệp vụ (Facts) qua hệ thống các chiều chuẩn hóa dùng chung (Conformed Dimensions) tại khu vực trình bày (Presentation Area)."
        )}

        <ul>
          <li><strong>Sức mạnh của <code>Conformed Dimensions</code> &amp; Truy vấn xuyên quy trình (<code>Drill-across</code>):</strong> Nhờ sử dụng các <strong>Conformed Dimensions (Chiều đồng nhất)</strong> trong khu vực trình bày (<code>Presentation Area</code>), nhiều phòng ban khác nhau trong toàn doanh nghiệp có thể truy cập chung một nền tảng dữ liệu thống nhất và thực hiện phép nối <strong><code>Drill-across</code></strong> (ví dụ: đặt <em>Doanh số bán hàng</em> từ <code>Fact_Sales</code> cạnh <em>Số lượng tồn kho</em> từ <code>Fact_Inventory</code> theo cùng một <code>Dim_Product</code> và <code>Dim_Store</code>) mà không bị phân mảnh hay lệch số liệu.</li>
        </ul>

        <section class="summary-section" id="storage-4-summary" tabindex="-1">
          <h2>TỔNG KẾT CHẶNG 4 &amp; KHÉP LẠI TRỌN VẸN PHẦN 1 (4 NGUYÊN TẮC MÔ HÌNH HÓA)</h2>
          <ol>
            <li><strong>Ba cấp độ mô hình hóa &amp; Quy trình 4 bước:</strong> Khi thiết kế kho dữ liệu cho <strong>Đơn hàng <code>#8888</code></strong>, ta đi qua <strong>3 cấp độ mô hình hóa</strong>: <code>Conceptual</code> (tổng quan thực thể cho Business) ➔ <code>Logical</code> (chi tiết bảng, cột, PK/FK) ➔ <code>Physical</code> (triển khai kiểu dữ liệu, Partition, Clustering, Index lên CSDL) kết hợp quy trình 4 bước của Kimball (<em>Chọn quy trình ➔ Tuyên bố Grain ➔ Xác định Dimensions ➔ Xác định Facts</em>).</li>
            <li><strong>Ba trường phái &amp; Cặp bài trùng Fact – Dimension:</strong> Trong 3 trường phái (<strong>Inmon</strong> chuẩn hóa <code>3NF</code> theo 4 tính chất <em>Subject-oriented, Integrated, Nonvolatile, Time-variant</em>; <strong>Kimball</strong> phi chuẩn hóa theo chiều; và <strong>Data Vault</strong> nạp <code>insert-only</code> vào <em>Hubs, Links, Satellites</em>), mô hình chiều của <strong>Kimball</strong> tách dữ liệu thành bảng <strong>Fact</strong> (số đo định lượng <code>Additive / Semi-additive / Non-additive</code> tại một <strong>Grain</strong> nguyên tử cố định, bất biến, hẹp và dài) và bảng <strong>Dimension</strong> (ngữ cảnh rộng và ngắn mô tả ai, cái gì, ở đâu, khi nào).</li>
            <li><strong>Ba sơ đồ bố trí bảng:</strong> Tùy nhu cầu truy vấn, ta bố trí theo <strong>Star Schema</strong> (chuẩn vàng cho BI, ít JOIN), <strong>Snowflake Schema</strong> (chuẩn hóa các bảng Dim thành nhánh con), hoặc <strong>OBT</strong> (gộp phẳng toàn bộ để loại bỏ JOIN trên Cloud Columnar Engine).</li>
            <li><strong>Bộ ba vũ khí bảo toàn lịch sử &amp; chống phân mảnh:</strong> Để bảo vệ kho khỏi biến động nguồn, lưu trọn vẹn lịch sử thay đổi và thống nhất toàn công ty, ta dùng bộ 3 vũ khí: <strong>Surrogate Keys</strong>, <strong>SCD Type 1, Type 2 (<code>start_date</code>, <code>end_date</code>, <code>is_current</code>) &amp; Type 3 (cột cũ/mới)</strong>, và <strong>Enterprise Bus Matrix (<code>Conformed Dimensions</code>)</strong>.</li>
          </ol>
          <p style="margin-top:14px;"><strong>Bước ngoặt mở ra Phần 2 (Chặng 5 — From Data Lake to Data Swamp):</strong> Vậy là chúng ta đã hoàn thành trọn vẹn <strong>100% kiến thức Phần 1 (Chặng 1 ➔ Chặng 4)</strong>! Ở <strong>Phần 2 (Chặng 5)</strong>, câu chuyện rẽ sang một bước ngoặt mới: <em>Khi công ty mang toàn bộ dữ liệu thô, hình ảnh, JSON clickstream của Đơn hàng <code>#8888</code> đổ ồ ạt xuống hồ dữ liệu <code>Data Lake</code> (S3) theo cơ chế <code>Schema-on-Read</code>, tại sao chỉ sau 6 tháng hồ nước trong lành lại biến thành một "Đầm lầy dữ liệu" (<code>Data Swamp</code>) không ai dám đụng vào?</em> <a href="#topic=D02&stage=5" onclick="selectStorageStage(5);return false;">Đọc ngay Chặng 5 ──►</a></p>
        </section>
      </div>
    `;
  }

  function renderStorageChang5() {
    const d = HUB_DATA.storage_diagrams;
    return `
      <div class="prose">
        <div class="callout">
          <div class="callout-title">Liên kết Mạch truyện: Từ Star Schema Ngăn nắp (Chặng 4) đến Cơn sóng thần Dữ liệu Đa định dạng &amp; Cạm bẫy Đầm lầy (Chặng 5)</div>
          <p>Ở cuối <strong>Chặng 4 (Phần 1)</strong>, <strong>Đơn hàng <code>#8888</code></strong> đã được sắp xếp vô cùng ngăn nắp trong sơ đồ hình sao (<strong>Star Schema</strong>) của <strong>Data Warehouse</strong> để phục vụ các báo cáo doanh thu. Tưởng chừng câu chuyện lưu trữ đã viên mãn, nhưng bước sang <strong>Chặng 5 (Phần 2: From Data Lake to Data Swamp)</strong>, một cơn sóng thần dữ liệu mới ập đến làm rung chuyển toàn bộ kiến trúc cũ.</p>
          <p style="margin-top:8px;">Đây là chặng bản lề quan trọng nhất giải thích <strong>tại sao thế giới dữ liệu từng vỡ mộng với thế hệ Data Lake 1.0</strong>, và tại sao nỗi đau của "Đầm lầy dữ liệu" (<strong>Data Swamp</strong>) lại trực tiếp khai sinh ra kiến trúc <strong>Data Lakehouse</strong> ở Chặng 6.</p>
        </div>

        <h2 id="storage-5-1" tabindex="-1">TRẠM 5.1: GIẤC MƠ "HỒ DỮ LIỆU" (DATA LAKE) — TẠI SAO PHẢI RỜI BỎ DATA WAREHOUSE?</h2>
        <p><em>(Tương ứng mục 01/ Data Lake: Lưu trữ đa định dạng trên Object Storage &amp; Schema-on-Read)</em></p>

        <h3 id="storage-5-1-story">1. Câu chuyện của Đơn hàng <code>#8888</code>: Khi một đơn hàng không chỉ còn là những con số!</h3>
        <p>Ở Phần 1, Đơn hàng <code>#8888</code> chỉ là một dòng dữ liệu có cấu trúc gọn gàng (<code>Mã đơn: 8888</code>, <code>Số tiền: 15.000.000đ</code>) nằm trong bảng <code>Fact</code>. Nhưng khi công ty phát triển ứng dụng di động và triển khai AI/Machine Learning, xoay quanh <strong>Đơn hàng <code>#8888</code></strong> phát sinh thêm hàng loạt dữ liệu mới:</p>
        <ul>
          <li><strong>Bán cấu trúc (<code>Semi-structured</code>):</strong> Hàng trăm tệp nhật ký hành vi bấm chuột (<code>click_8888.json</code>) ghi lại khách hàng đã lướt xem những mẫu ghế nào trước khi chốt đơn.</li>
          <li><strong>Phi cấu trúc (<code>Unstructured</code>):</strong> Ảnh chụp biên bản giao hàng tận nhà (<code>contract_8888.jpg</code>), video camera kho bãi lúc đóng gói, và tệp ghi âm cuộc gọi chăm sóc khách hàng.</li>
        </ul>

        <p><strong>Nỗi đau bùng phát:</strong> Nếu nhét hàng chục triệu tệp JSON clickstream và hình ảnh giao hàng của Đơn <code>#8888</code> vào <strong>Data Warehouse</strong>, dung lượng đĩa chuyên dụng đắt đỏ sẽ cạn kiệt ngay lập tức, thậm chí Data Warehouse từ chối nhận vì nó chỉ hiểu dữ liệu bảng có cấu trúc. Công ty quyết định xây dựng <strong>Data Lake (Hồ dữ liệu)</strong> — một kho lưu trữ tập trung trên nền <strong>Cloud Object Storage (S3 / ADLS / GCS)</strong> hoặc <strong>HDFS</strong> để chứa mọi định dạng dữ liệu ở trạng thái nguyên bản với chi phí siêu rẻ (<code>~$0.02/GB/tháng</code>).</p>

        <ul>
          <li><strong>Nguồn gốc thuật ngữ &amp; Phân loại 3 Môi trường Dữ liệu trong Data Lake (Mở rộng từ sách gốc):</strong> Thuật ngữ <strong>Data Lake</strong> do <strong>James Dixon</strong> (CTO của Pentaho) khởi xướng năm 2010: ông ví <em>Data Warehouse</em> như một <em>"chai nước suối đã lọc sạch, đóng chai sẵn để uống ngay"</em>, còn <em>Data Lake</em> là một <em>"hồ nước lớn ở trạng thái tự nhiên"</em> nơi mọi dòng suối dữ liệu chảy thẳng vào để ai cần gì thì tự múc lên phân tích. Theo <strong>Bill Inmon</strong> (<em>Building the Data Lakehouse</em>), toàn bộ dữ liệu chảy vào Data Lake được chia thành <strong>3 môi trường vật lý</strong>: (1) <strong>Structured / Application data</strong> (bảng giao dịch <code>8888.parquet</code>), (2) <strong>Textual data</strong> (văn bản phi cấu trúc như email, hợp đồng, ghi chú CSKH), và (3) <strong>Analog / IoT data</strong> (ảnh <code>contract_8888.jpg</code>, video, âm thanh, cảm biến — nhóm này chiếm tới <strong>trên 90% tổng dung lượng byte vật lý</strong> trong hồ nhưng lại khó khai thác nhất nếu thiếu siêu dữ liệu).</li>
          <li><strong>Sự tiến hóa qua 2 thế hệ Data Lake (<code>Data Lake 1.0</code> ➔ <code>Cloud Data Lake</code>):</strong> Thế hệ <strong>Data Lake 1.0</strong> khởi đầu trên các cụm máy chủ vật lý tại chỗ (<code>On-premises Hadoop HDFS</code>) gắn chặt lưu trữ với tính toán MapReduce phức tạp; trong khi thế hệ <strong>Cloud Data Lake</strong> chuyển toàn bộ tệp lên <strong>Cloud Object Storage (AWS S3, Azure ADLS Gen2, GCS)</strong>, tách rời hoàn toàn lưu trữ và tính toán để các động cơ như <code>Apache Spark</code>, <code>Trino</code>, <code>Presto</code> hay <code>Ray</code> có thể bật lên đọc dữ liệu rồi tắt đi ngay khi tính toán xong.</li>
        </ul>

        <h3 id="storage-5-1-shifts">2. Hai cuộc đại dịch chuyển: <code>Schema-on-Write ➔ Schema-on-Read</code> &amp; <code>ETL ➔ ELT</code></h3>

        ${buildVisualBlock(
          "storage-5-1",
          "Hình 5.1 — Hai cuộc đại dịch chuyển: Schema-on-Write (ETL) sang Schema-on-Read (ELT) trên Data Lake",
          d["5.1"].ascii,
          d["5.1"].mermaid,
          "Đối chiếu quy trình kiểm duyệt lược đồ nghiêm ngặt lúc ghi của Data Warehouse truyền thống (Schema-on-Write & ETL) với cơ chế nạp thẳng đa định dạng giá rẻ ~$0.02/GB/tháng rồi mới áp lược đồ lúc đọc của Data Lake (Schema-on-Read & ELT)."
        )}

        <ul>
          <li><strong>Ưu tiên Định dạng Tự mô tả (<code>Self-Describing Formats</code>) &amp; Cạm bẫy Kiến trúc Hai tầng (<code>Two-Tier Architecture</code>):</strong> Dù <code>Schema-on-Read</code> và <code>ELT</code> mở toang cánh cửa nhận mọi tệp thô, kỹ sư luôn phải ưu tiên định dạng tự mô tả có nhúng sẵn schema (<code>Parquet, Avro, ORC, JSON</code>) thay vì <code>CSV</code>. Tuy nhiên, vì Data Lake đọc trực tiếp cho BI quá chậm và thiếu ACID, các doanh nghiệp buộc phải chắp vá <strong>Kiến trúc Hai tầng (<code>Data Lake + Data Warehouse</code>)</strong> làm nhân đôi chi phí lưu trữ, gây lệch số liệu (<code>Data Drift</code>) và ngăn cản các mô hình AI/ML (<code>PyTorch, TensorFlow</code>) đọc trực tiếp trên kho.</li>
        </ul>

        <h2 id="storage-5-2" tabindex="-1">TRẠM 5.2: BI KỊCH "ĐẦM LẦY DỮ LIỆU" (DATA SWAMP) — KHI HỒ NƯỚC HÓA BÃI RÁC</h2>
        <p><em>(Tương ứng mục 02/ Data Swamp: Dữ liệu rác, ghi dở dang, lệch schema, không thể truy xuất)</em></p>

        <h3 id="storage-5-2-story">1. Câu chuyện Kiểm toán Đơn hàng <code>#8888</code> sau 6 tháng</h3>
        <p>Sau 6 tháng vận hành Data Lake 1.0 theo tôn chỉ <em>"cứ ném hết vào S3 rồi tính sau"</em>, Giám đốc Tài chính đột ngột yêu cầu: <em>"Hãy truy xuất lại toàn bộ hóa đơn, hợp đồng vận chuyển và nhật ký giao hàng của <strong>Đơn hàng <code>#8888</code></strong> để phục vụ đoàn kiểm toán thuế!"</em></p>
        <p>Khi kỹ sư dữ liệu mở thùng chứa (Bucket) S3 ra, họ bàng hoàng nhận ra: <strong>Hồ dữ liệu (Data Lake) đã thoái hóa hoàn toàn thành một Đầm lầy dữ liệu (Data Swamp)</strong>! Trong giới kỹ thuật, hàng loạt thuật ngữ cay đắng đã ra đời để mô tả thảm cảnh này: <strong>Data Swamp (Đầm lầy dữ liệu)</strong>, <strong>Dark Data (Dữ liệu tối/mồ côi)</strong>, và <strong>WORN (Write Once, Read Never — Ghi một lần, Không bao giờ đọc được nữa)</strong>.</p>

        ${buildVisualBlock(
          "storage-5-2a",
          "Hình 5.2a — Quá trình thoái hóa từ Data Lake ngăn nắp thành Data Swamp hỗn loạn sau 6 tháng",
          d["5.2a"].ascii,
          d["5.2a"].mermaid,
          "Sự suy thoái từ một Data Lake được tổ chức phân vùng rõ ràng sang một Data Swamp (Đầm lầy dữ liệu) chứa đầy thư mục rác, tệp lỗi mã hóa, tệp ghi dở (3.parquet) và tệp nhân bản làm sai lệch kết quả kiểm toán."
        )}

        <h3 id="storage-5-2-diseases">2. Giải phẫu 5 "Căn bệnh lâm sàng" giết chết Đơn hàng <code>#8888</code> trong Đầm lầy</h3>

        <h4>Bệnh 1: Dữ liệu Mồ côi (<code>Dark Data / Orphan Data</code>) &amp; Hội chứng <code>WORN</code></h4>
        <p>Thiếu danh mục tự động và thiếu <strong>Chính sách Vòng đời (<code>Data Retention &amp; Lifecycle Policies</code></strong> — hạ cấp sang <code>IA / Glacier</code> sau 30–180 ngày) khiến mô hình kỳ vọng <strong><code>WORM (Write Once, Read Many)</code></strong> suy thoái thành <strong><code>WORN (Write Once, Read Never)</code></strong> và <strong><code>Data Superfund Site</code></strong>: hàng nghìn thư mục rác <code>/test_data/</code>, <code>/data_final_v2/</code> nằm chết không ai biết tệp nào chứa dữ liệu chính thức của Đơn <code>#8888</code>.</p>

        <h4>Bệnh 2: Tệp ghi dở lẩn khuất (<code>Partial Files / Zombie Writes</code>) &amp; 6 Khiếm khuyết của <code>Apache Hive Table Format</code></h4>
        <p>Khi Job Spark đứt mạng ở giây thứ 5 rồi tự chạy lại, cả tệp ghi dở <code>3.parquet</code> lẫn tệp hoàn chỉnh <code>3_v2.parquet</code> đều nằm trong cùng thư mục phân vùng S3, khiến câu lệnh SQL cộng trùng doanh thu Đơn <code>#8888</code> gấp đôi:</p>

        ${buildVisualBlock(
          "storage-5-2b",
          "Hình 5.2b — Cơ chế sinh tệp ghi dở (Zombie Writes) trên S3 & Hậu quả nhân đôi doanh thu trong Bảng Hive",
          d["5.2b"].ascii,
          d["5.2b"].mermaid,
          "Khi Job Spark đứt mạng lúc đang ghi Đơn #8888 xuống S3 rồi chạy lại, cả tệp ghi dở 3.parquet lẫn tệp hoàn chỉnh 3_v2.parquet đều nằm chung trong một thư mục. Vì chuẩn bảng Apache Hive quét toàn bộ thư mục, doanh thu bị cộng trùng gấp đôi."
        )}

        <p>Nguyên nhân gốc rễ nằm ở <strong>6 khiếm khuyết kiến trúc cố hữu của chuẩn bảng <code>Apache Hive Table Format</code></strong> khi đặt lên Cloud Object Storage (theo <em>Apache Iceberg: The Definitive Guide</em>):</p>

        ${buildVisualBlock(
          "storage-5-2c",
          "Hình 5.2c — Giải phẫu 6 Khiếm khuyết Kiến trúc của Apache Hive Table Format trên Cloud Object Storage",
          d["5.2c"].ascii,
          d["5.2c"].mermaid,
          "Sáu điểm yếu cố hữu của chuẩn bảng Apache Hive trên Object Storage: quản lý cấp thư mục, lệnh Rename O(N) không nguyên tử, không có commit nguyên tử đa phân vùng, chi phí S3 LIST đắt đỏ, phụ thuộc cứng vào cột phân vùng vật lý, và thống kê bảng lỗi thời."
        )}

        <h4>Bệnh 3, 4 &amp; 5: Trôi trượt lược đồ (<code>Schema Drift</code>), Bất lực trước <code>GDPR</code> &amp; Giới hạn Nhất quán (<code>Consistency</code>)</h4>
        <ul>
          <li><strong>Bệnh 3 — <code>Schema Drift</code>:</strong> Đội Backend âm thầm đổi trường JSON từ <code>total_cost</code> sang <code>order_amount</code>; vì Data Lake nạp <code>schema-less</code>, dữ liệu vẫn lọt vào hồ và làm gãy hàng loạt báo cáo hạ nguồn hoặc biến số tiền thành <code>NULL</code>.</li>
          <li><strong>Bệnh 4 — Bất lực trước luật <code>GDPR / CCPA</code> (<code>Write-Only</code>):</strong> Khi khách hàng Nguyễn Văn A yêu cầu xóa dữ liệu cá nhân theo quyền được lãng quên (<code>Right to be Forgotten</code>), việc tìm và viết lại hàng triệu tệp Parquet bất biến trên S3 là cơn ác mộng chi phí.</li>
          <li><strong>Bệnh 5 — Từ <code>Eventual Consistency</code> đến giới hạn <code>Single-Object Strong Consistency</code>:</strong> Khi ghi đè cùng một khóa <code>orders/8888.parquet</code>, Object Storage tạo đối tượng mới và thu gom rác (<code>Garbage Collection</code>) ngầm (hoặc giữ bản sao nếu bật <code>Object Versioning</code>). Dù S3/GCS/ADLS hiện đại đã hỗ trợ <strong><code>Strong Read-After-Write Consistency</code></strong>, tính nguyên tử này chỉ áp dụng cho <strong>từng đối tượng đơn lẻ (<code>single-object atomicity</code>)</strong> — không thể khóa giao dịch đồng thời cho <strong>200 tệp Parquet</strong> của một job Spark nếu thiếu lớp định dạng bảng giao dịch!</li>
        </ul>

        <h2 id="storage-5-3" tabindex="-1">TRẠM 5.3: GIẢI MÃ 3 LỖ HỔNG CÔNG CỤ CỐT TỬ (THE 3 TOOLING GAPS)</h2>
        <p><em>(Tương ứng mục 03/ Why Data Lake turns into Data Swamp: Tooling Gaps, Thiếu Catalog, Thiếu Lineage)</em></p>

        <p>Tại sao một hạ tầng đám mây hiện đại lại dễ dàng sụp đổ thành đầm lầy như vậy? Nhìn từ góc độ kiến trúc, nguyên nhân nằm ở <strong>3 lỗ hổng công cụ và quản trị cốt lõi (<code>Tooling Gaps</code>)</strong>:</p>

        ${buildVisualBlock(
          "storage-5-3",
          "Hình 5.3a — Giải mã 3 Lỗ hổng Công cụ cốt tử (The 3 Tooling Gaps) biến Data Lake thành Data Swamp",
          d["5.3"].ascii,
          d["5.3"].mermaid,
          "Ba lỗ hổng kiến trúc khiến Data Lake 1.0 suy thoái thành Data Swamp: (1) Thiếu giao dịch ACID và tính khả biến (Mutability), (2) Thiếu Data Catalog, quản trị Metadata và quyền sở hữu (Ownership), (3) Thiếu Data Lineage, Observability và kiểm soát chất lượng tự động."
        )}

        <h3 id="storage-5-3-table">1. Bảng phân tích chi tiết 3 Lỗ hổng (Trọng tâm Ôn thi &amp; Phỏng vấn)</h3>
        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Lỗ hổng cốt lõi</th>
                <th>Bản chất kỹ thuật bên dưới</th>
                <th>Tác hại trực tiếp lên Hệ thống &amp; Đơn hàng <code>#8888</code></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>1. Tooling Gaps: Thiếu giao dịch ACID &amp; Tính khả biến (<code>Lack of Mutability</code>)</strong></td>
                <td>• <strong>Thiếu hỗ trợ giao dịch (<code>Insufficient transactional support</code>):</strong> Không có đảm bảo <strong>ACID</strong> (Atomicity, Consistency, Isolation, Durability).<br/><br/>• <strong>Thiếu khả năng sửa đổi (<code>Lack of mutability</code>):</strong> Dữ liệu trong hồ được xem là bất biến (<code>immutable</code>), chỉ thiết kế để nạp theo lô (<code>batch</code>) chứ không hỗ trợ cập nhật/chèn (<code>upserts</code>) từng bản ghi theo thời gian thực.</td>
                <td>• Một tác vụ ETL đột biến (<code>bursty ETL job</code>) đang ghi có thể đè hỏng một tiến trình phân tích phức tạp đang đọc cùng lúc, và không thể khôi phục đúng trạng thái khi job sập giữa chừng.<br/><br/>• Đồng bộ dữ liệu từ nguồn về hồ bị trễ (<code>latency</code>), dẫn đến phân tích bị cũ (<code>stale analytics</code>).</td>
              </tr>
              <tr>
                <td><strong>2. Thiếu Data Catalog, Quản trị Metadata &amp; Quyền sở hữu (<code>Lack of Catalog &amp; Governance</code>)</strong></td>
                <td>• Không có công cụ danh mục tập trung (<code>Data Catalog</code>) và quản lý siêu dữ liệu (<code>Metadata Management</code>) để người dùng tra cứu cấu trúc bảng như trong Data Warehouse.<br/><br/>• Không rõ quyền sở hữu và người quản lý dữ liệu (<code>Unclear Ownership and Stewardship</code>), thiếu chính sách phân quyền truy cập chi tiết ngay từ đầu.</td>
                <td>• Người dùng cuối thấy Data Lake bất tiện và không thể hiểu nổi (<code>inscrutable</code>) các thư mục chứa gì.<br/><br/>• Rủi ro rò rỉ dữ liệu (<code>data breaches</code>) và vi phạm tuân thủ pháp lý.</td>
              </tr>
              <tr>
                <td><strong>3. Thiếu Data Lineage, Giám sát &amp; Kiểm soát chất lượng (<code>Lack of Lineage &amp; Observability</code>)</strong></td>
                <td>• Không có công cụ theo dõi phả hệ dữ liệu (<code>Lineage tracking</code>), giám sát (<code>Observability</code>) và kiểm tra chất lượng tự động (<code>Quality checks</code>).</td>
                <td>• Khi số tiền của Đơn <code>#8888</code> trên báo cáo bị sai hoặc bị <code>NULL</code>, kỹ sư không thể truy vết ngược xem lỗi phát sinh từ hệ thống nguồn nào hay bị biến dạng ở bước biến đổi nào.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3 id="storage-5-3-deepdive">2. Giải phẫu Kiến trúc <code>Data Catalog</code> 3 Tầng &amp; 5 Trụ cột <code>Data Observability</code> (Mở rộng từ sách gốc)</h3>

        ${buildVisualBlock(
          "storage-5-3b",
          "Hình 5.3b — Kiến trúc Data Catalog 3 Tầng & 5 Trụ cột Giám sát Dữ liệu Chủ động (Data Observability)",
          d["5.3b"].ascii,
          d["5.3b"].mermaid,
          "Giải pháp lấp đầy lỗ hổng số 2 và số 3: kiến trúc 3 tầng của Data Catalog hiện đại (DataHub, OpenMetadata, Unity Catalog) kết hợp 5 trụ cột giám sát chủ động (Freshness, Volume, Schema, Distribution/Quality, Lineage)."
        )}

        <h2 id="storage-5-4" tabindex="-1">TRẠM 5.4: PHÁC ĐỒ CỨU NGUY — LÀM SAO NGĂN DATA LAKE HÓA THÀNH ĐẦM LẦY?</h2>
        <p><em>(Tương ứng mục 04/ How to prevent this transition: Phân vùng Zoning, ETL/ELT, Data Contracts, Single Source of Truth)</em></p>

        <p>Để cứu Đơn hàng <code>#8888</code> và ngăn chặn quá trình "đầm lầy hóa" (<code>Swampification</code>), người kỹ sư dữ liệu phải thiết lập ngay <strong>4 hàng rào kỷ luật và kiến trúc</strong> sau đây:</p>

        <h3 id="storage-5-4-zoning">1. Quy hoạch Phân vùng Hồ chứa (<code>Zoning</code>: Raw ➔ Cleansed ➔ Curated) &amp; Cưỡng chế <code>ETL/ELT</code></h3>
        <p>Thay vì để một thùng chứa S3 hỗn độn ai muốn vứt gì vào cũng được, bạn phải chia hồ dữ liệu thành <strong>3 phân vùng cách ly rõ ràng</strong> và bắt buộc mọi dữ liệu di chuyển giữa các vùng phải đi qua đường ống kiểm duyệt <strong>ETL/ELT</strong>:</p>

        ${buildVisualBlock(
          "storage-5-4a",
          "Hình 5.4a — Quy hoạch Phân vùng Cách ly trong Data Lake (Zoning: Raw ➔ Cleansed ➔ Curated)",
          d["5.4a"].ascii,
          d["5.4a"].mermaid,
          "Quy hoạch hồ dữ liệu thành 3 phân vùng cách ly (Raw Zone ➔ Cleansed Zone ➔ Curated Zone) kết hợp đường ống kiểm duyệt ETL/ELT — tiền đề trực tiếp của kiến trúc Medallion (Bronze ➔ Silver ➔ Gold)."
        )}

        <p><em>(Chính tư duy phân vùng <code>Raw ➔ Cleansed ➔ Curated</code> này là tiền đề trực tiếp cho kiến trúc <strong>Medallion: Bronze ➔ Silver ➔ Gold</strong> ở Phần 4!)</em>.</p>

        <h3 id="storage-5-4-contracts">2. Ký "Hợp đồng Dữ liệu" (<code>Data Contracts</code>) &amp; Quản lý Lược đồ (<code>Schema Registry</code>)</h3>
        <p>Làm sao trị dứt điểm căn bệnh đội Backend/App tự ý đổi tên cột <code>total_cost</code> thành <code>order_amount</code> (<code>Schema Drift</code>) làm gãy đường ống của Đơn hàng <code>#8888</code>?</p>
        <ul>
          <li><strong>Thiết lập <code>Data Contracts</code> (Hợp đồng dữ liệu):</strong> Là bản giao kèo kỹ thuật chính thức giữa bên sinh dữ liệu (<strong>Producer</strong> — đội App/Backend) và bên tiêu thụ dữ liệu (<strong>Consumer</strong> — đội Data Engineering), quy định rõ cấu trúc, kiểu dữ liệu và cam kết không được tự ý thay đổi làm gãy pipeline hạ nguồn.</li>
          <li><strong>6 Thành phần bắt buộc của một <code>Data Contract</code> chuẩn công nghiệp (theo James Densmore, <em>Fundamentals of Data Engineering</em>):</strong> Để hợp đồng dữ liệu không chỉ là lời hứa miệng mà có thể kiểm tra tự động trong quy trình <code>CI/CD</code> (dưới dạng tệp cấu hình <code>YAML / JSON</code>), bản hợp đồng phải đặc tả rõ 6 yếu tố: (1) <strong>Dữ liệu nào được trích xuất</strong>, (2) <strong>Phương thức trích xuất</strong> (Full dump, Incremental hay CDC), (3) <strong>Tần suất nạp</strong>, (4) <strong>Ràng buộc lược đồ, kiểu dữ liệu &amp; quy tắc chất lượng</strong>, (5) <strong>Đầu mối chịu trách nhiệm (<code>Owner contacts</code>)</strong> của cả hệ thống nguồn lẫn đường ống dữ liệu, và (6) <strong>Cam kết mức dịch vụ (<code>SLAs / SLOs</code></strong> — ví dụ: độ sẵn sàng 99%, thời gian thông báo trước tối thiểu khi thay đổi phiên bản lược đồ).</li>
          <li><strong>Cưỡng chế bằng <code>Schema Registry</code> &amp; 3 Chế độ Tương thích (<code>Compatibility Modes</code>) trên luồng sự kiện:</strong> Khi tích hợp <code>Schema Registry</code> (đi kèm định dạng tuần tự hóa nhị phân như <code>Apache Avro</code>, <code>Protobuf</code> hoặc <code>JSON Schema</code>), mọi sự kiện của Đơn hàng <code>#8888</code> trước khi vào Kafka hoặc Data Lake đều được đối chiếu tự động theo một trong 3 quy tắc tiến hóa lược đồ:
            <ul>
              <li><strong><code>BACKWARD</code> (Tương thích ngược — Mặc định khuyên dùng):</strong> Đảm bảo Consumer nâng cấp lên <em>Schema mới</em> vẫn đọc được trọn vẹn <em>dữ liệu lịch sử cũ</em> trong hồ (ví dụ: cho phép thêm cột mới có giá trị mặc định <code>default</code>, hoặc xóa cột tùy chọn; nhưng <strong>cấm tự ý đổi tên cột bắt buộc</strong> như <code>total_cost ➔ order_amount</code>).</li>
              <li><strong><code>FORWARD</code> (Tương thích xuôi):</strong> Đảm bảo các Consumer đang chạy <em>Schema cũ</em> vẫn đọc được <em>dữ liệu mới</em> do Producer vừa phát ra (bằng cách tự động bỏ qua các trường mới chưa khai báo).</li>
              <li><strong><code>FULL</code> (Tương thích toàn phần hai chiều):</strong> Thỏa mãn đồng thời cả <code>BACKWARD</code> và <code>FORWARD</code> — chuẩn bảo vệ nghiêm ngặt nhất cho các bảng lõi doanh nghiệp.</li>
            </ul>
          </li>
        </ul>

        <h3 id="storage-5-4-ssot">3. Thiết lập "Nguồn Sự Thật Duy Nhất" (<code>Single Source of Truth</code>) — Chấm dứt bài toán "40 Bản sao"</h3>
        <p>Một nguyên nhân ngầm nhưng cực kỳ nguy hiểm biến hệ thống thành đầm lầy là <strong>sự phức tạp do phân kỳ nguồn sự thật (<code>divergent sources of data truth</code>)</strong>:</p>

        ${buildVisualBlock(
          "storage-5-4b",
          "Hình 5.4b — Kỷ luật chống Đầm lầy: Data Contracts + Schema Registry & Single Source of Truth vs. 40 Buckets",
          d["5.4b"].ascii,
          d["5.4b"].mermaid,
          "Hai trụ cột quản trị sống còn: (1) Chặn đứng Schema Drift từ cửa ngõ Kafka bằng Data Contract và Schema Registry; (2) Chấm dứt thảm họa nhân bản dữ liệu ra 40 Cloud Storage Buckets bằng nguyên tắc Single Source of Truth."
        )}

        <ul>
          <li><strong>Cách làm sai lầm (Nhân bản phân vùng ra 40 nơi khác nhau):</strong> Từ 1 bảng Đơn hàng gốc, bạn xuất (<code>export</code>) các phân vùng ra 40 Cloud Storage Buckets riêng biệt cho 40 phòng ban!
            <ul>
              <li><em>Nỗi đau 1:</em> Quản lý quyền truy cập tối thiểu và lỗi thu hồi quyền (<code>revoked permissions</code>) ở 40 nơi là ác mộng.</li>
              <li><em>Nỗi đau 2:</em> Khi Đơn <code>#8888</code> bị lỗi cần chạy lại (<code>reprocess</code>), bạn phải cập nhật lại cả 40 nơi, tốn kém chi phí mạng hai chiều (<code>Ingress &amp; Egress costs</code>) và lệch số liệu giữa các đội!</li>
            </ul>
          </li>
          <li><strong>Giải pháp: <code>Single Source of Truth</code> (Nguồn chân lý duy nhất):</strong>
            <ul>
              <li>Duy trì <strong>DUY NHẤT 1 bảng nền tảng chuẩn xác</strong> đại diện cho tập dữ liệu Đơn hàng tại trung tâm.</li>
              <li>Mọi phòng ban và công cụ cùng tham chiếu về nguồn sự thật duy nhất này (kết hợp phân quyền truy cập hạt mịn theo vai trò <code>RBAC / ABAC</code>) thay vì chép ra hàng chục bản sao vật lý rời rạc!</li>
            </ul>
          </li>
        </ul>

        <section class="summary-section" id="storage-5-summary" tabindex="-1">
          <h2>CHỐT HẠ MẠCH NHÂN – QUẢ CHẶNG 5 (ĐỂ BƯỚC SANG CHẶNG 6 — LAKEHOUSE)</h2>
          <p>Hãy nhìn lại bức tranh tổng kết cực kỳ sắc nét của <strong>Chặng 5 (Phần 2)</strong>:</p>
          <ol>
            <li><strong>Tại sao cần Data Lake?</strong> Để thoát khỏi giới hạn chỉ lưu dữ liệu có cấu trúc và chi phí đắt đỏ của Data Warehouse, công ty đưa mọi định dạng dữ liệu của <strong>Đơn hàng <code>#8888</code></strong> (CSV, JSON, Ảnh, Video — bao gồm cả 3 môi trường <em>Structured, Textual, Analog/IoT</em>) lên <strong>Object Storage (<code>$0.02/GB/tháng</code>)</strong> theo cơ chế <strong><code>Schema-on-Read</code></strong> và <strong><code>ELT</code></strong>.</li>
            <li><strong>Tại sao hóa thành Data Swamp?</strong> Vì Object Storage và định dạng bảng thư mục kiểu cũ (<strong>Apache Hive Table Format</strong> với 6 khiếm khuyết cố hữu) thiếu bộ não quản trị, sinh ra <strong>dữ liệu mồ côi (<code>Dark Data / WORN</code>)</strong>, <strong>tệp ghi dở làm nhân đôi doanh thu (<code>Zombie Writes</code>)</strong>, <strong>lệch cấu trúc (<code>Schema Drift</code>)</strong>, <strong>trễ pha nhất quán (<code>Eventual Consistency</code> / thiếu giao dịch đa tệp)</strong> và <strong>bất lực khi xóa dữ liệu theo luật <code>GDPR</code></strong>.</li>
            <li><strong>Ba lỗ hổng gốc rễ (<code>3 Tooling Gaps</code>):</strong> (1) Thiếu giao dịch <strong>ACID &amp; Mutability</strong>, (2) Thiếu <strong>Data Catalog (3 tầng) &amp; Ownership</strong>, (3) Thiếu <strong>Data Lineage &amp; 5 trụ cột Data Observability</strong>.</li>
            <li><strong>Cách phòng tránh:</strong> Quy hoạch phân vùng (<code>Raw ➔ Cleansed ➔ Curated</code>), áp dụng <strong><code>Data Contracts</code> + <code>Schema Registry</code> (<code>BACKWARD / FORWARD / FULL</code>)</strong>, và giữ vững <strong><code>Single Source of Truth</code></strong> (xóa bỏ nạn nhân bản 40 Buckets).</li>
          </ol>
          <p style="margin-top:14px;"><strong>Câu hỏi bùng nổ dẫn sang Chặng 6 (Phần 3: Kiến trúc Lakehouse &amp; Bộ ba Open Table Formats):</strong> Quy hoạch thư mục và ký hợp đồng mới chỉ giải quyết được phần "tổ chức con người". Còn ở tầng kỹ thuật cốt lõi: <strong>Làm thế nào để biến các tệp <code>Parquet</code> bất biến nằm trên <code>S3</code> có thể thực hiện giao dịch <code>ACID</code>, tự động tàng hình các tệp ghi dở (<code>Zombie files</code>), cho phép sửa/xóa từng dòng (<code>UPDATE / DELETE</code>) và du hành thời gian (<code>Time Travel</code>) giống hệt như một Data Warehouse?</strong> Đó chính là lúc <strong>Delta Lake (<code>_delta_log</code>)</strong>, <strong>Apache Iceberg (<code>3-layer tree</code>)</strong> và <strong>Apache Hudi (<code>Timeline/Index</code>)</strong> bước ra sân khấu ở <strong>Chặng 6</strong>! <a href="#topic=D02&stage=6" onclick="selectStorageStage(6);return false;">Đọc ngay Chặng 6 ──►</a></p>
        </section>
      </div>
    `;
  }

  function renderStorageChang6() {
    const d = HUB_DATA.storage_diagrams;
    return `
      <div class="prose">
        <div class="callout">
          <div class="callout-title">Liên kết Mạch truyện: Từ Đầm lầy Dữ liệu Data Swamp (Chặng 5) đến "Bộ não Giao dịch" của Kiến trúc Data Lakehouse (Chặng 6)</div>
          <p>Ở cuối <strong>Chặng 5 (Phần 2)</strong>, chúng ta đã chứng kiến bi kịch của <strong>Đơn hàng <code>#8888</code></strong>: khi công ty đổ toàn bộ dữ liệu thô xuống <strong>Data Lake (S3)</strong> mà không có "bộ não" kiểm soát, một tác vụ Spark bị đứt mạng giữa chừng đã để lại tệp rác ghi dở <code>3.parquet</code> nằm cạnh tệp chạy lại <code>3_v2.parquet</code>, khiến doanh thu của Đơn <code>#8888</code> bị tính gấp đôi và biến hồ dữ liệu thành một <strong>Đầm lầy dữ liệu (<code>Data Swamp</code>)</strong> không ai dám tin dùng.</p>
          <p style="margin-top:8px;">Bước vào <strong>Chặng 6 (Phần 3: Kiến trúc Lakehouse &amp; Bộ ba Open Table Formats)</strong> — chặng nặng ký nhất, đắt giá nhất trong mọi kỳ phỏng vấn Data Engineering hiện đại — chúng ta sẽ giải mã câu hỏi: <em>Làm thế nào để lắp một "Bộ não giao dịch" lên ngay phía trên các tệp Parquet bất biến của S3, biến một cái hồ hỗn loạn thành một hệ thống vừa rẻ như Data Lake vừa thông minh, kỷ luật như Data Warehouse?</em></p>
        </div>

        <h2 id="storage-6-1" tabindex="-1">TRẠM 6.1: KIẾN TRÚC DATA LAKEHOUSE &amp; BƯỚC NGOẶT "ĐỊNH NGHĨA LẠI MỘT BẢNG"</h2>
        <p><em>(Tương ứng mục 01/ Kiến trúc Lakehouse: Kết hợp Data Lake + Data Warehouse &amp; Tách rời Compute - Storage)</em></p>

        <h3 id="storage-6-1-convergence">1. Phép cộng hoàn hảo: Data Warehouse + Data Lake = Data Lakehouse</h3>
        <p>Thuật ngữ <strong>Lakehouse</strong> lần đầu tiên được đặt ra bởi Michael Armbrust và các cộng sự trong bài báo khoa học <em>"Lakehouse: A New Generation of Open Platforms That Unify Data Warehousing and Advanced Analytics"</em> tại hội nghị CIDR năm 2021. Kiến trúc này ra đời nhằm giải quyết triệt để những giới hạn của cả Data Lake truyền thống lẫn Data Warehouse bằng cách lấy những phẩm chất tốt nhất của cả hai thế giới:</p>

        ${buildVisualBlock(
          "storage-6-1a",
          "Hình 6.1a — Sơ đồ Giao thoa Kiến trúc Data Lakehouse (CIDR 2021)",
          d["6.1a"].ascii,
          d["6.1a"].mermaid,
          "Sự hợp nhất giữa kỷ luật quản trị, giao dịch ACID và tốc độ truy vấn BI của Data Warehouse với chi phí lưu trữ siêu rẻ (~$0.02/GB/tháng), định dạng mở và khả năng phục vụ AI/ML của Data Lake."
        )}

        <ul>
          <li><strong>Tiến hóa 3 Thế hệ Nền tảng Dữ liệu (<em>CIDR 2021</em> &amp; <em>Delta Lake: The Definitive Guide</em>):</strong> <strong>Thế hệ 1 (<code>Data Warehouse</code>)</strong> gắn chặt Compute-Storage đắt đỏ và mù dữ liệu phi cấu trúc; <strong>Thế hệ 2 (<code>Two-Tier: Data Lake + Warehouse</code>)</strong> mắc 4 căn bệnh hệ thống (ETL hai chặng dễ gãy, dữ liệu bị trễ <code>Stale data</code>, ML/PyTorch không đọc trực tiếp được Warehouse, và <code>TCO</code> đội gấp đôi do lưu trùng lặp); <strong>Thế hệ 3 (<code>Data Lakehouse</code>)</strong> đặt trực tiếp tầng giao dịch ACID lên trên <code>Apache Parquet / S3</code>, xóa bỏ hoàn toàn việc chép dữ liệu sang kho thứ hai.</li>
        </ul>

        <h3 id="storage-6-1-3tier">2. Kiến trúc 3 Tầng của Lakehouse &amp; Nguyên lý Tách rời Compute – Storage</h3>
        <p>Để vận hành linh hoạt và tiết kiệm chi phí, Lakehouse tách biệt hoàn toàn <strong>Tầng tính toán (<code>Compute</code>)</strong> và <strong>Tầng lưu trữ (<code>Storage</code>)</strong>, đồng thời chèn thêm một <strong>Tầng giao dịch (<code>Transaction Layer</code>)</strong> ở chính giữa:</p>

        ${buildVisualBlock(
          "storage-6-1b",
          "Hình 6.1b — Kiến trúc 3 Tầng của Hệ thống Data Lakehouse & Phân tách File Format vs. Table Format",
          d["6.1b"].ascii,
          d["6.1b"].mermaid,
          "Kiến trúc 3 tầng chuẩn của một hệ thống Data Lakehouse: (1) Query Engines / Ephemeral Compute có bộ đệm cục bộ, (2) Transaction & Table Format Layer đảm nhận ACID và Table Services, (3) Cloud Object Storage lưu trữ Data Files (Parquet/ORC/Avro) và Metadata Files."
        )}

        <ul>
          <li><strong>Tách rời Compute – Storage &amp; 3 Vũ khí Tăng tốc BI (<em>CIDR 2021</em>):</strong> Đơn hàng <code>#8888</code> nằm trên S3 giá rẻ (<code>~$0.02/GB/tháng</code>), còn các cụm <strong>Ephemeral Clusters</strong> chỉ bật khi chạy job. Dù S3 có độ trễ <code>~100 ms</code>, Lakehouse vẫn đạt tốc độ BI ngang ngửa Data Warehouse nhờ 3 trụ cột: (1) <strong><code>Hot Data Caching</code></strong> trên NVMe SSD/RAM cục bộ của nút tính toán, (2) <strong><code>Auxiliary Data &amp; Layout</code></strong> (Min/Max, Bloom Filter, gom cụm <code>Z-Order / Hilbert Curve</code>) giúp bỏ qua 95–99% tệp (<code>Data Skipping</code>), và (3) <strong><code>Vectorized Execution</code></strong> (<code>Photon</code>, <code>Velox</code>, <code>DuckDB</code>, <code>Trino</code>) xử lý cột trên <code>Apache Arrow</code> bằng lệnh phần cứng <code>SIMD</code>.</li>
          <li><strong>Phân biệt <code>File Format</code> vs. <code>Table Format</code> &amp; Bước ngoặt khỏi <code>Hive</code>:</strong>
            <span id="storage-6-1-paradigm"></span>
            <strong>File Format (<code>Parquet, Avro, ORC</code>)</strong> quy định cách mã hóa byte <em>bên trong 1 tệp đơn lẻ</em>; còn <strong>Table Format (<code>Delta Lake, Iceberg, Hudi</code>)</strong> quản lý <em>hàng nghìn tệp riêng lẻ</em> như một bảng logic có ACID. Khác với <strong>Apache Hive Table Format</strong> định nghĩa bảng bằng <em>toàn bộ nội dung thư mục</em> (dẫn đến đọc nhầm tệp rác <code>3.parquet</code> và nghẽn lệnh <code>S3 LIST</code>), bộ ba <strong>Open Table Formats</strong> định nghĩa bảng bằng <strong>danh sách chuẩn tắc các tệp hợp lệ (<code>canonical list of files</code>)</strong> trong Metadata!</li>
        </ul>

        <h2 id="storage-6-2" tabindex="-1">TRẠM 6.2: GIẢI PHẪU "BỘ NÃO" CỦA BỘ BA OPEN TABLE FORMATS (DELTA LAKE, ICEBERG, HUDI)</h2>
        <p><em>(Tương ứng mục 02.1/ Cơ chế Metadata &amp; Transaction Log: <code>_delta_log</code>, Iceberg 3-layer tree, Hudi Timeline/Index)</em></p>

        <p>Dù có chung mục tiêu quản lý danh sách tệp Parquet trên Object Storage, nhưng <strong>Delta Lake</strong>, <strong>Apache Iceberg</strong> và <strong>Apache Hudi</strong> lại thiết kế "bộ não" lưu trữ siêu dữ liệu theo 3 cơ chế kiến trúc rất đặc trưng:</p>

        <h3 id="storage-6-2-delta">1. Cơ chế của <code>Delta Lake</code>: Nhật ký giao dịch tuần tự <code>_delta_log</code></h3>
        <p>Giống như một <strong>cuốn sổ cái kế toán ghi nối đuôi theo thứ tự thời gian</strong>, mọi giao dịch thay đổi bảng đều sinh ra một tệp JSON 20 chữ số tuần tự (<code>000000.json</code>, <code>000001.json</code>...) trong thư mục <strong><code>_delta_log/</code></strong>:</p>

        ${buildVisualBlock(
          "storage-6-2a",
          "Hình 6.2a — Cách Delta Lake (_delta_log) cứu Đơn hàng #8888 khỏi tệp ghi dở (Zombie Writes)",
          d["6.2a"].ascii,
          d["6.2a"].mermaid,
          "Cơ chế nhật ký giao dịch tuần tự _delta_log của Delta Lake: mọi truy vấn đều đối chiếu danh sách tệp hợp lệ từ tệp Checkpoint và các tệp JSON commit, khiến tệp ghi dở 3_zombie_partial.parquet tự động tàng hình 100%."
        )}

        <ul>
          <li><strong>Giải phẫu 6 loại Action trong JSON &amp; Cơ chế <code>_last_checkpoint</code> (<em>Delta Lake: The Definitive Guide</em>, tr. 36–45):</strong> Mỗi tệp commit JSON chứa 6 loại bản ghi hành động: (1) <strong><code>protocol</code></strong> (<code>minReaderVersion / minWriterVersion</code>), (2) <strong><code>metaData</code></strong> (schema, partitionColumns, cấu hình bảng), (3) <strong><code>add</code></strong> (đăng ký tệp Parquet mới hợp lệ kèm <code>stats</code>: <code>numRecords, minValues, maxValues, nullCount</code> cho 32 cột đầu), (4) <strong><code>remove</code></strong> (bản ghi bia mộ <code>tombstone</code> gỡ tệp cũ khỏi bản hiện hành nhưng giữ tệp vật lý cho Time Travel kèm <code>deletionTimestamp</code>), (5) <strong><code>commitInfo</code></strong> (nhật ký kiểm toán), và (6) <strong><code>cdc</code></strong> (trỏ tới <code>_change_data</code>). Cứ sau mỗi <strong>10 commits</strong>, Delta Lake tự động gộp trạng thái từ đầu bảng thành tệp <strong><code>.checkpoint.parquet</code></strong> (hỗ trợ cả <em>V2 Checkpoints</em> với <em>sidecar Parquet</em>) và cập nhật con trỏ <strong><code>_last_checkpoint</code></strong> để động cơ đọc nhảy thẳng tới mốc gần nhất mà không cần quét lại hàng vạn tệp JSON cũ!</li>
        </ul>

        <h3 id="storage-6-2-iceberg">2. Cơ chế của <code>Apache Iceberg</code>: Cây Siêu dữ liệu 3 Tầng (<code>3-Layer Metadata Tree</code>)</h3>
        <p>Giống như <strong>mục lục phân cấp của một đại thư viện quốc gia</strong>, Iceberg quản lý bảng quy mô Petabyte qua cây 3 tầng từ <code>Catalog</code> ➔ <code>Metadata File (.json)</code> ➔ <code>Manifest List (.avro)</code> ➔ <code>Manifest Files (.avro)</code>:</p>

        ${buildVisualBlock(
          "storage-6-2b",
          "Hình 6.2b — Cây Siêu dữ liệu 3 Tầng của Apache Iceberg ở Quy mô Petabyte",
          d["6.2b"].ascii,
          d["6.2b"].mermaid,
          "Cấu trúc cây siêu dữ liệu phân cấp của Apache Iceberg: Iceberg Catalog (giữ con trỏ nguyên tử CAS) ➔ Tầng 1: Metadata File (.metadata.json) ➔ Tầng 2: Manifest List (.avro) ➔ Tầng 3: Manifest Files (.avro) ➔ Data & Delete Files (.parquet)."
        )}

        <ul>
          <li><strong>Tráo con trỏ Nguyên tử (<code>Atomic CAS Swap</code>) &amp; Cắt tỉa Siêu dữ liệu 2 Cấp (<em>Apache Iceberg: The Definitive Guide</em>, tr. 51–68):</strong> Mọi giao dịch Iceberg hoàn tất bằng một phép hoán đổi nguyên tử (<code>Compare-And-Swap — CAS</code>) tại tầng <strong>Catalog</strong> (<code>REST Catalog</code>, <code>Nessie</code>, <code>Unity Catalog</code>, <code>Snowflake Polaris</code>, <code>Glue</code>) đổi con trỏ từ <code>v1.metadata.json</code> sang <code>v2.metadata.json</code>, đồng thời tái sử dụng các <code>Manifest file</code> cũ không thay đổi. Khi truy vấn Đơn <code>#8888</code>, Iceberg cắt tỉa 2 cấp ngay trên Metadata: <strong>Cấp 1 (<code>Manifest List</code>)</strong> dùng khoảng <code>lower_bound / upper_bound</code> của phân vùng để bỏ qua ngay cả cụm Manifest của các tháng khác; <strong>Cấp 2 (<code>Manifest File</code>)</strong> dùng trạng thái (<code>ADDED / EXISTING / DELETED</code>) và thống kê cột <code>Min/Max/Null</code> để chỉ đích danh tệp <code>0003_8888.parquet</code> mà không cần gửi hàng nghìn lệnh HTTP mở Footer trên S3!</li>
        </ul>

        <h3 id="storage-6-2-hudi">3. Cơ chế của <code>Apache Hudi</code>: Trục thời gian <code>Timeline</code>, <code>File Groups</code> &amp; Hệ thống <code>Indexing</code></h3>
        <p>Giống như một <strong>bưu cục chuyển phát nhanh có bảng điện tử theo dõi từng giây (<code>Timeline</code>) và sổ danh bạ tra cứu kệ hàng (<code>Index</code>)</strong>, Hudi (<em>Hadoop Update Delete Incremental</em>) được thiết kế chuyên biệt cho các luồng <strong>Streaming Upsert / CDC</strong> tốc độ cao:</p>

        ${buildVisualBlock(
          "storage-6-2c",
          "Hình 6.2c — Giải phẫu Kiến trúc Apache Hudi: Timeline (State Machine), Indexing Subsystem & File Groups",
          d["6.2c"].ascii,
          d["6.2c"].mermaid,
          "Ba trụ cột kiến trúc của Apache Hudi: (1) Hudi Timeline quản lý trạng thái giao dịch qua 3 bước REQUESTED ➔ INFLIGHT ➔ COMPLETED; (2) Hệ thống chỉ mục Indexing (.hoodie/metadata) ánh xạ khóa bản ghi #8888 về đúng FileGroup ID; (3) File Groups & File Slices kết hợp Base File (Parquet cột) và Log Files (Avro dòng)."
        )}

        <ul>
          <li><strong>Máy trạng thái 3 bước của <code>Hudi Timeline</code>, <code>Hybrid File Groups</code> &amp; 4 Loại Chỉ mục (<em>Apache Hudi: The Definitive Guide</em>, tr. 34–58):</strong>
            <ul>
              <li><strong>Hudi Timeline &amp; File Groups:</strong> Mọi hành động (<code>commit</code> cho COW, <code>deltacommit</code> cho MOR, <code>compaction</code>, <code>clustering</code>, <code>clean</code>) trong thư mục <code>.hoodie/</code> đều đi qua 3 trạng thái nguyên tử: <strong><code>REQUESTED ➔ INFLIGHT ➔ COMPLETED</code></strong> (người đọc chỉ thấy các Instant đã <code>COMPLETED</code>). Mỗi <strong>File Group</strong> kết hợp tuần tự hóa lai (<code>Hybrid Serialization</code>): <strong>Base File</strong> dạng cột (<code>Parquet/ORC</code>) lưu dữ liệu chính + <strong>Log Files</strong> dạng dòng (<code>.log.avro</code>) bắt tức thì các bản ghi CDC mới.</li>
              <li><strong>4 loại Index trong bảng Metadata nội bộ (<code>.hoodie/metadata</code> dạng <code>HFile</code>):</strong> Giúp định vị ngay Đơn <code>#8888</code> nằm ở <code>File Group</code> nào mà không cần quét bảng: (1) <strong><code>Bloom Index</code></strong> (mặc định: dùng Bloom Filter + Min/Max), (2) <strong><code>Simple Index</code></strong> (đối chiếu khi cập nhật rải rác), (3) <strong><code>Bucket Index</code></strong> (băm trực tiếp <code>hash(record_key) % N</code> vào Bucket không cần tra cứu), và (4) <strong><code>Record-Level Index (RLI)</code></strong> (ánh xạ 1-1 từng khóa <code>RecordKey ➔ FileGroupId</code> với tốc độ <code>O(1)</code> cho bảng hàng trăm tỷ dòng).</li>
            </ul>
          </li>
        </ul>

        <h3 id="storage-6-2-uniform">4. Kỷ nguyên Hợp nhất Đa Định dạng: <code>Delta UniForm</code>, <code>Apache XTable</code> &amp; <code>Pluggable Table Format</code></h3>
        <p>Trước đây, các công ty đau đầu vì nếu chọn ghi bằng Hudi thì công cụ chỉ hỗ trợ Iceberg không đọc được. Ngày nay, rào cản này đã bị xóa bỏ nhờ <strong>kiến trúc chuyển đổi siêu dữ liệu đa chiều</strong> (bản chất cả 3 đều lưu dữ liệu gốc trên tệp <code>Parquet</code>, chỉ khác nhau ở tệp Metadata!):</p>

        ${buildVisualBlock(
          "storage-6-2d",
          "Hình 6.2d — Cơ chế Đọc Đa Định dạng (Delta UniForm / Apache XTable / Pluggable Table Format)",
          d["6.2d"].ascii,
          d["6.2d"].mermaid,
          "Kiến trúc dịch siêu dữ liệu đa chiều (UniForm / Apache XTable): cho phép Spark, Trino, Snowflake và Flink cùng đọc chung 1 bộ tệp vật lý orders_8888.parquet thông qua lớp Metadata tương ứng mà không cần nhân bản dữ liệu trên S3."
        )}

        <ul>
          <li><strong>Delta Lake <code>UniForm</code> (Universal Format):</strong> Chỉ cần bật thuộc tính <code>'delta.universalFormat.enabledFormats' = 'iceberg'</code> (và yêu cầu bật <code>delta.columnMapping.mode = 'name'</code> hoặc <code>'id'</code>), sau mỗi giao dịch Delta thành công, hệ thống tự động sinh bất đồng bộ siêu dữ liệu chuẩn Iceberg hoặc Hudi cho cùng bộ tệp Parquet đó.</li>
          <li><strong>Hudi <code>Pluggable Table Format</code> &amp; <code>Apache XTable</code> (tiền thân là <em>OneTable</em>):</strong> Hudi tách rời động cơ lưu trữ khỏi định dạng bảng, kết hợp với <strong>Apache XTable</strong> để dịch siêu dữ liệu qua lại đa chiều (<code>omnidirectional interoperation</code>) giữa cả 3 định dạng <strong>Hudi, Iceberg và Delta Lake</strong>, giúp tích hợp dễ dàng với mọi danh mục như Snowflake Polaris hay DataHub mà vẫn giữ nguyên bảng gốc.</li>
        </ul>

        <h3 id="storage-6-2-comparison">5. Bảng So sánh Trực diện: Delta Lake vs. Apache Iceberg vs. Apache Hudi</h3>
        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Tiêu chí kỹ thuật</th>
                <th>Delta Lake</th>
                <th>Apache Iceberg</th>
                <th>Apache Hudi</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Cơ chế Metadata cốt lõi</strong></td>
                <td>Nhật ký giao dịch tuần tự <code>_delta_log</code> (<code>000000.json</code> + <code>.checkpoint.parquet</code> + <code>_last_checkpoint</code>).</td>
                <td>Cây siêu dữ liệu 3 tầng: <code>Catalog (CAS)</code> ➔ <code>Metadata file (.json)</code> ➔ <code>Manifest List (.avro)</code> ➔ <code>Manifest file (.avro)</code>.</td>
                <td><code>Timeline</code> (<code>commit</code> / <code>deltacommit</code> qua 3 bước trạng thái) + <code>File Groups</code> (<code>Base Parquet</code> + <code>Log Avro</code>).</td>
              </tr>
              <tr>
                <td><strong>Vũ khí đặc trưng nhất</strong></td>
                <td>Tích hợp hoàn hảo với <strong>Apache Spark Structured Streaming</strong>, tối ưu hóa <code>Z-Order / Liquid Clustering</code>, <code>Deletion Vectors</code>, <code>Change Data Feed (CDF)</code> &amp; <code>UniForm</code>.</td>
                <td><strong>Hidden Partitioning</strong> và <strong>Partition Evolution</strong> (đổi phân vùng không cần viết lại bảng), cắt tỉa 2 cấp ở quy mô Petabyte, chuẩn mở đa động cơ (Trino, Snowflake, Spark, Flink).</td>
                <td>Hệ thống <strong>Indexing</strong> tích hợp sẵn (<code>Record-Level Index</code>, <code>Bucket Index</code>) &amp; kiểm soát đồng thời <strong>NBCC</strong>, cực mạnh cho <strong>Streaming Upsert / CDC</strong> tần suất cao.</td>
              </tr>
              <tr>
                <td><strong>Cơ chế Xóa / Cập nhật dòng (MOR)</strong></td>
                <td>Mặc định <code>COW</code>; chuyển sang <code>MOR</code> bằng <strong>Deletion Vectors</strong> (mảng Roaring Bitmap lưu vị trí dòng xóa).</td>
                <td>Hỗ trợ cả <code>COW</code> lẫn <code>MOR</code> qua <strong>Positional Delete Files</strong> (vị trí dòng) và <strong>Equality Delete Files</strong> (điều kiện khóa).</td>
                <td>Thiết kế gốc phân tách 2 loại bảng <strong><code>COPY_ON_WRITE</code></strong> và <strong><code>MERGE_ON_READ</code></strong> (<code>Base Parquet + Delta Log Avro</code>).</td>
              </tr>
              <tr>
                <td><strong>Tương thích chéo</strong></td>
                <td>Sinh metadata Iceberg/Hudi qua <strong>Delta UniForm</strong>.</td>
                <td>Đọc/dịch qua lại nhờ <strong>Apache XTable</strong> hoặc Snapshot migration.</td>
                <td>Kiến trúc <strong>Pluggable Table Format</strong> &amp; tích hợp <strong>Apache XTable</strong>.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h2 id="storage-6-3" tabindex="-1">TRẠM 6.3: BỘ TÍNH NĂNG CỐT LÕI — ACID, CONCURRENCY (OCC/MVCC/NBCC), TIME TRAVEL &amp; SCHEMA</h2>
        <p><em>(Tương ứng mục 02.2/ Tính năng cốt lõi: ACID Transactions, Time Travel, Schema Enforcement &amp; Evolution)</em></p>

        <h3 id="storage-6-3-concurrency">1. Giao dịch <code>ACID</code> &amp; Ba Cơ chế Kiểm soát Đồng thời (<code>Concurrency Control</code>)</h3>
        <p>Trên Lakehouse, điều gì xảy ra khi <strong>Luồng A (CDC)</strong> đang cập nhật địa chỉ của Đơn hàng <code>#8888</code>, cùng lúc <strong>Luồng B (Job ETL)</strong> đang gộp các tệp nhỏ, và <strong>Luồng C (Giám đốc)</strong> đang chạy câu lệnh SQL đọc báo cáo doanh thu?</p>
        <p>Nhờ lớp Transaction Layer, mọi thay đổi đều tuân thủ <strong>ACID</strong> (Atomicity, Consistency, Isolation, Durability) — nếu một tiến trình bị lỗi giữa chừng, hệ thống tự động hủy bỏ (<code>roll back</code>) để dữ liệu luôn nhất quán. Để xử lý nhiều luồng đọc/ghi cùng lúc mà không giẫm đạp lên nhau, Lakehouse sử dụng 3 kỹ thuật kiểm soát đồng thời:</p>

        ${buildVisualBlock(
          "storage-6-3",
          "Hình 6.3 — Ba Cơ chế Kiểm soát Đồng thời trên Data Lakehouse (MVCC, OCC & NBCC)",
          d["6.3"].ascii,
          d["6.3"].mermaid,
          "Sự kết hợp giữa MVCC (Cô lập Snapshot giúp Đọc và Ghi không bao giờ khóa nhau), OCC (Kiểm soát lạc quan phát hiện xung đột cấp độ tệp giữa các luồng Ghi) và NBCC (Kiểm soát đồng thời không khóa cho nhiều luồng Streaming trên Apache Hudi)."
        )}

        <ul>
          <li><strong>Phát hiện Xung đột Cấp Tệp (<code>File-Level Conflict Detection</code>) &amp; Mức Cô lập:</strong> Trong <strong>OCC</strong>, <code>Writer 2</code> chỉ bị từ chối (<code>ConcurrentModificationException</code>) khi sửa/xóa <strong>đúng tệp Parquet vật lý</strong> mà <code>Writer 1</code> vừa chạm tới; nếu 2 luồng cùng <code>APPEND</code> hoặc <code>UPDATE</code> trên <strong>2 Partition tách biệt</strong>, cả hai đều commit thành công lên <code>v3</code>. Mặc định Delta Lake dùng mức cô lập <strong><code>WriteSerializable</code></strong> (thay vì <code>Serializable</code> cứng nhắc) để cho phép các thao tác <code>blind append</code> chạy song song không chặn lệnh bảo trì <code>OPTIMIZE / Z-ORDER</code>.</li>
        </ul>

        <h3 id="storage-6-3-timetravel">2. Du hành thời gian (<code>Time Travel</code>), <code>Change Data Feed (CDF)</code> &amp; Tiến hóa Lược đồ (<code>Schema Evolution</code>)</h3>
        <p>Vì tệp Parquet là bất biến và mỗi giao dịch tạo một <code>Version / Snapshot</code> mới, đồng thời mỗi cột được định danh bằng mã số nguyên bất biến (<strong><code>Column ID / Field ID</code></strong>), Lakehouse giải quyết trọn vẹn cả bài toán truy vấn lịch sử lẫn đổi tên cột trong <code>1 ms</code>:</p>

        ${buildVisualBlock(
          "storage-6-3b",
          "Hình 6.3b — Du hành Thời gian (Time Travel), Change Data Feed (CDF) & Schema Evolution bằng Column ID",
          d["6.3b"].ascii,
          d["6.3b"].mermaid,
          "Cơ chế Time Travel qua chuỗi Snapshot v0 -> v1 -> v2 kèm luồng thay đổi tăng trưởng Change Data Feed (CDF) và bí mật định danh cột bằng mã số nguyên bất biến (Column ID / Field ID) giúp đổi tên cột chỉ bằng 1 thao tác sửa JSON Metadata mà không viết lại tệp Parquet."
        )}

        <pre><code>-- [A] DELTA LAKE (Truy vấn theo Timestamp, Version &amp; Khôi phục bảng):
SELECT * FROM sales.orders TIMESTAMP AS OF '2026-10-15 14:00:00' WHERE order_id = 8888;
SELECT * FROM sales.orders VERSION AS OF 0 WHERE order_id = 8888;
RESTORE TABLE sales.orders TO VERSION AS OF 0;

-- [B] APACHE ICEBERG (Chuẩn SQL:2011 System-Versioned Tables):
SELECT * FROM sales.orders FOR SYSTEM_TIME AS OF TIMESTAMP '2026-10-15 14:00:00' WHERE order_id = 8888;
SELECT * FROM sales.orders FOR SYSTEM_VERSION AS OF 5789718362515484664 WHERE order_id = 8888;
CALL catalog.system.rollback_to_snapshot('sales.orders', 5789718362515484664);

-- [C] ĐỌC LUỒNG THAY ĐỔI TĂNG TRƯỞNG (CHANGE DATA FEED - CDF TRÊN DELTA LAKE):
SELECT order_id, so_tien, _change_type, _commit_version, _commit_timestamp
FROM table_changes('sales.orders', 0, 1) WHERE order_id = 8888;</code></pre>

        <h3 id="storage-6-3-schema">3. Tổng kết 4 Trụ cột Quản lý Lược đồ &amp; Dòng thời gian</h3>
        <ul>
          <li><strong>Time Travel &amp; Change Data Feed (<code>CDF</code>):</strong> Phục vụ kiểm toán pháp lý, tái lập tập dữ liệu huấn luyện ML, và <code>Rollback</code> tức thời. Khi bật <code>delta.enableChangeDataFeed = true</code> (hoặc <code>Incremental Query</code> trên Hudi / <code>Changelog Scan</code> trên Iceberg), bảng tự động xuất các dòng biến động kèm <code>_change_type</code> (<code>insert</code>, <code>update_preimage = 15M</code>, <code>update_postimage = 14M</code>, <code>delete</code>) để pipeline <em>Silver ➔ Gold</em> chỉ đọc phần chênh lệch.</li>
          <li><strong>Schema Enforcement &amp; Schema Evolution bằng <code>Column ID</code>:</strong> Chặn đứng dữ liệu sai kiểu ngay lúc ghi (như cố chèn chuỗi <code>'Mười lăm triệu'</code> vào cột <code>DECIMAL</code>). Khi đổi tên cột (<code>RENAME COLUMN total_cost TO order_amount</code>), nhờ <strong>Iceberg</strong> (mặc định) và <strong>Delta Lake</strong> (<code>Column Mapping Mode = 'id'</code>) ánh xạ cột theo <strong><code>field-id</code> bất biến</strong> thay vì tên chữ như Hive cũ, hệ thống chỉ đổi nhãn hiển thị của <code>ID 2</code> trong JSON Metadata mà không bao giờ gặp lỗi trả về <code>NULL</code> hay làm "sống dậy" cột cũ đã xóa.</li>
          <li><strong>Unified Batch &amp; Streaming:</strong> Một bảng Lakehouse duy nhất vừa làm nguồn/đích cho luồng thời gian thực (<code>Spark Structured Streaming</code>) vừa phục vụ truy vấn lô (<code>Batch BI</code>) trên cùng một bộ API.</li>
        </ul>

        <h2 id="storage-6-4" tabindex="-1">TRẠM 6.4: CHIẾN LƯỢC GHI &amp; CẬP NHẬT — COPY-ON-WRITE (COW) VS. MERGE-ON-READ (MOR)</h2>
        <p><em>(Tương ứng mục 02.3/ Chiến lược ghi/cập nhật: Copy-on-Write tối ưu đọc vs. Merge-on-Read tối ưu ghi/streaming)</em></p>

        <h3 id="storage-6-4-story">1. Bài toán thực tế của Đơn hàng <code>#8888</code>: Sửa 1 dòng trong tệp Parquet 100 MB!</h3>
        <p>Giả sử tệp <code>file_01.parquet</code> nặng <strong>100 MB</strong> chứa <strong>100.000 đơn hàng</strong>, trong đó có <strong>Đơn hàng <code>#8888</code></strong> (<code>15.000.000đ</code>). Năm phút sau, khách hàng nhập mã giảm giá làm số tiền Đơn <code>#8888</code> đổi thành <strong><code>14.000.000đ</code></strong>. Vì tệp <code>Parquet</code> trên <code>S3</code> là <strong>bất biến (<code>Immutable</code>)</strong>, động cơ Lakehouse có đúng <strong>2 chiến lược</strong> để thực thi lệnh <code>UPDATE</code> này:</p>

        ${buildVisualBlock(
          "storage-6-4",
          "Hình 6.4 — Đối chiếu Cơ học Copy-on-Write (COW) vs. Merge-on-Read (MOR) khi sửa Đơn hàng #8888",
          d["6.4"].ascii,
          d["6.4"].mermaid,
          "Đối chiếu hai chiến lược cập nhật trên Lakehouse: (1) Copy-on-Write (COW) viết lại toàn bộ tệp Parquet 100 MB để tối ưu tốc độ đọc tuyệt đối; (2) Merge-on-Read (MOR) chỉ ghi 1 dòng thay đổi (~1 KB) vào tệp Log/Delete rồi trộn khi đọc để tối ưu tốc độ ghi Streaming/CDC."
        )}

        <h3 id="storage-6-4-table">2. Bảng Đặt lên Bàn cân: Khi nào chọn <code>COW</code>, khi nào chọn <code>MOR</code>?</h3>
        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Tiêu chí so sánh</th>
                <th>Copy-on-Write (COW)</th>
                <th>Merge-on-Read (MOR)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Cơ chế khi <code>UPDATE</code> / <code>DELETE</code></strong></td>
                <td>Viết lại toàn bộ tệp cột (<code>Parquet</code>) mới chứa bản ghi đã sửa và đổi con trỏ Metadata (<code>commit</code>).</td>
                <td>Giữ nguyên tệp gốc (<code>Base Parquet</code>), chỉ ghi nối đuôi bản ghi thay đổi vào <code>Log file (Avro)</code> hoặc <code>Delete file</code> (<code>deltacommit</code>).</td>
              </tr>
              <tr>
                <td><strong>Chi phí GHI (<code>Write Amplification</code>)</strong></td>
                <td><strong>Cao (<code>WAF &gt;&gt; 1</code>):</strong> Sửa 1 dòng <code>1 KB</code> phải viết lại cả tệp <code>100 MB</code> (khuếch đại gấp <code>100.000 lần</code>).</td>
                <td><strong>Cực thấp (<code>WAF ≈ 1</code>):</strong> Ghi nối đuôi tức thì chỉ tốn vài Kilobyte.</td>
              </tr>
              <tr>
                <td><strong>Tốc độ ĐỌC (<code>Query Latency</code>)</strong></td>
                <td><strong>Nhanh tuyệt đối cho OLAP/BI:</strong> Quét thẳng tệp Parquet mới nhất, không tốn CPU ghép trộn.</td>
                <td><strong>Tốn chi phí trộn khi đọc:</strong> Phải hợp nhất <code>Base file</code> + <code>Log / Delete file</code> lúc truy vấn (định kỳ gom lại nhờ <code>Compaction</code>).</td>
              </tr>
              <tr>
                <td><strong>Góc nhìn Đọc &amp; Cơ chế Xóa (Sách gốc)</strong></td>
                <td>Đọc trực tiếp Snapshot Parquet thuần túy.</td>
                <td>• <strong>Hudi 2 chế độ đọc:</strong> <code>Snapshot Query (RT)</code> trộn Base+Log lấy dữ liệu tươi từng giây vs. <code>Read-Optimized (RO)</code> chỉ đọc Base Parquet.<br/><br/>• <strong>Iceberg 2 loại Delete Files:</strong> <code>Positional Delete</code> lưu <code>(file_path, pos = 4512)</code> đọc cực nhanh vs. <code>Equality Delete</code> lưu <code>(order_id = 8888)</code> ghi nhanh tuyệt đối (Zero-read at write time).</td>
              </tr>
              <tr>
                <td><strong>Trường hợp sử dụng lý tưởng</strong></td>
                <td>Tác vụ nạp theo lô (<code>Batch ETL</code>), bảng tầng <strong>Gold</strong> phục vụ Dashboard BI.</td>
                <td>Luồng <strong>Streaming / CDC (Debezium + Kafka)</strong> <code>Upsert / Delete</code> liên tục tại tầng <strong>Bronze / Silver</strong>.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h2 id="storage-6-5" tabindex="-1">TRẠM 6.5: NĂM KỸ THUẬT TỐI ƯU VẬT LÝ SỐNG CÒN TRÊN LAKEHOUSE</h2>
        <p><em>(Tương ứng mục 02.4/ Kỹ thuật tối ưu vật lý: Compaction, Partitioning, Z-Ordering/Clustering, Deletion Vectors, Vacuum)</em></p>

        <p>Ở quy mô thực tế, nếu không chạy các dịch vụ bảo trì bảng (<code>Table Services</code>), Lakehouse sẽ bị suy thoái hiệu năng và đội chi phí S3. Dưới đây là <strong>3 sơ đồ trực quan hóa trọn vẹn 5 kỹ thuật tối ưu vật lý cốt lõi</strong>:</p>

        <h3 id="storage-6-5-partition">1. <code>Hidden Partitioning</code> &amp; <code>Partition Evolution</code> (Apache Iceberg)</h3>
        <p>Khắc phục điểm mù của <strong>Hive Partitioning truyền thống</strong> (bắt người dùng phải nhớ lọc đúng cột thư mục phái sinh <code>nam_thang</code> và không thể đổi cách chia phân vùng nếu không viết lại toàn bộ bảng), Iceberg lưu trực tiếp <strong>6 hàm biến đổi chuẩn</strong> (<code>year</code>, <code>month</code>, <code>day</code>, <code>hour</code>, <code>bucket[N]</code>, <code>truncate[L]</code>) vào trong <code>Partition Spec</code> của Metadata:</p>

        ${buildVisualBlock(
          "storage-6-5a",
          "Hình 6.5a — Đối chiếu Partitioning truyền thống (Hive) vs. Hidden Partitioning & Partition Evolution (Apache Iceberg)",
          d["6.5a"].ascii,
          d["6.5a"].mermaid,
          "Cơ chế Hidden Partitioning và Partition Evolution của Apache Iceberg: lưu hàm biến đổi phân vùng ngay trong Partition Spec của Metadata giúp tự động cắt tỉa phân vùng từ cột thời gian gốc và tiến hóa chiến lược phân vùng mà không cần viết lại dữ liệu cũ."
        )}

        <h3 id="storage-6-5-zorder">2. Gom cụm Đa chiều: Từ <code>Z-Ordering</code> sang <code>Liquid Clustering (Hilbert Curve)</code></h3>
        <p>Khi một phân vùng có hàng nghìn tệp Parquet và dữ liệu khách hàng <code>Bình Dương</code> mua <code>Sofa</code> bị rải đều khắp các tệp, khoảng <code>[Min, Max]</code> của tệp nào cũng trải rộng từ <code>A ➔ Z</code> làm tê liệt <strong>Data Skipping</strong>. Kỹ thuật <strong><code>Z-Ordering</code></strong> (đan xen bit nhị phân theo đường cong chữ Z) và thế hệ mới <strong><code>Liquid Clustering</code></strong> (<code>CLUSTER BY</code> theo đường cong <strong>Hilbert Curve</strong>) gom các dòng cùng khóa đa chiều về chung tệp vật lý:</p>

        ${buildVisualBlock(
          "storage-6-5b",
          "Hình 6.5b — Gom cụm đa chiều Z-Ordering & Liquid Clustering tăng tốc Data Skipping",
          d["6.5b"].ascii,
          d["6.5b"].mermaid,
          "So sánh hiệu quả Data Skipping trước và sau khi chạy Z-Ordering / Liquid Clustering: thu hẹp khoảng giá trị [min, max] trên từng tệp Parquet giúp động cơ truy vấn tìm Đơn hàng #8888 chỉ bằng cách đọc File 1 và bỏ qua ngay File 2."
        )}

        <ul>
          <li><strong>Tại sao <code>Liquid Clustering (Hilbert Curve)</code> vượt trội hơn <code>Z-Ordering</code> (<em>Delta Lake: The Definitive Guide</em>, tr. 127–131, 259–263):</strong> <code>Z-Order</code> suy giảm hiệu quả khi vượt quá 3–4 cột và <strong>không có tính tăng trưởng (<code>not incremental</code>)</strong> — mỗi lần có dữ liệu mới lại phải viết lại cả phân vùng. Ngược lại, <code>Liquid Clustering</code> gom cụm tăng trưởng chỉ trên các tệp mới nạp, bảo toàn tính lân cận không gian tốt hơn nhờ đường cong Hilbert, và cho phép đổi khóa gom cụm (<code>ALTER TABLE ... CLUSTER BY</code>) tức thời không cần viết lại bảng.</li>
        </ul>

        <h3 id="storage-6-5-compaction">3. Bộ 3 Dịch vụ Bảo trì Vật lý: <code>Compaction (OPTIMIZE)</code>, <code>Deletion Vectors</code> &amp; <code>Vacuum</code></h3>
        <span id="storage-6-5-dv"></span><span id="storage-6-5-vacuum"></span>
        <p>Để trị dứt điểm căn bệnh <strong>43.200 tệp nhỏ li ti (<code>Small File Problem</code>)</strong> từ luồng Streaming, tăng tốc xóa/sửa dòng trên bảng <code>COW</code>, và thu hồi dung lượng S3 an toàn (cũng như xóa vĩnh viễn dữ liệu cá nhân theo luật <strong><code>GDPR</code></strong> qua quy trình 3 bước: <code>DELETE ➔ REORG PURGE / OPTIMIZE ➔ VACUUM</code>), kỹ sư dữ liệu vận hành phối hợp 3 dịch vụ dưới đây:</p>

        ${buildVisualBlock(
          "storage-6-5c",
          "Hình 6.5c — Bộ 3 Dịch vụ Bảo trì Vật lý trên Lakehouse: Compaction (OPTIMIZE), Deletion Vectors & Vacuum",
          d["6.5c"].ascii,
          d["6.5c"].mermaid,
          "Sự phối hợp giữa 3 dịch vụ bảo trì vật lý: (1) Compaction (OPTIMIZE) gộp hàng vạn tệp nhỏ thành tệp chuẩn 128 MB – 1 GB; (2) Deletion Vectors dùng Roaring Bitmap đánh dấu xóa mềm tức thì; (3) Vacuum / Expire Snapshots dọn rác vật lý sau chu kỳ lưu giữ 168 giờ."
        )}

        <section class="summary-section" id="storage-6-summary" tabindex="-1">
          <h2>CHỐT HẠ MẠCH NHÂN – QUẢ CHẶNG 6 (ĐỂ BƯỚC VÀO CHẶNG CUỐI CÙNG — CHẶNG 7)</h2>
          <p>Hãy nhìn lại sức mạnh toàn diện mà <strong>Chặng 6 (Phần 3: Lakehouse)</strong> vừa trang bị cho bạn:</p>
          <ol>
            <li><strong>Kiến trúc Lakehouse (CIDR 2021):</strong> Hợp nhất chi phí rẻ và tính mở của <strong>Data Lake (<code>Object Storage + Parquet</code>)</strong> với tính toàn vẹn <strong>ACID, Schema Enforcement và hiệu năng BI</strong> (nhờ <em>Hot Caching, Auxiliary Data &amp; Vectorized Execution</em>) của <strong>Data Warehouse</strong>, đồng thời <strong>tách rời hoàn toàn Compute và Storage</strong>.</li>
            <li><strong>Định nghĩa lại Một Bảng bằng Bộ ba Open Table Formats:</strong> Thay vì định nghĩa bảng bằng thư mục như Hive cũ, bộ ba <strong>Open Table Formats</strong> định nghĩa bảng bằng danh sách tệp hợp lệ trong Metadata: <strong>Delta Lake</strong> dùng nhật ký tuần tự <code>_delta_log</code> (6 loại Action + Checkpoint Parquet + <code>_last_checkpoint</code>), <strong>Apache Iceberg</strong> dùng cây 3 tầng (<code>Catalog CAS ➔ Metadata ➔ Manifest List ➔ Manifest File</code> kèm <code>Hidden Partitioning</code> &amp; <code>Partition Evolution</code>), và <strong>Apache Hudi</strong> dùng <code>Timeline (3 trạng thái) + File Groups + Indexing (RLI/Bloom/Bucket)</code> — và chúng có thể đọc chéo nhau trên cùng 1 bộ tệp Parquet nhờ <code>Delta UniForm</code> / <code>Apache XTable</code>.</li>
            <li><strong>Bộ Tính năng Cốt lõi &amp; Chiến lược Ghi/Đọc:</strong> Bảng Lakehouse cung cấp <strong>ACID &amp; Concurrency (<code>MVCC</code>, <code>OCC</code> phát hiện xung đột cấp tệp, <code>NBCC</code>)</strong>, <strong>Time Travel (Snapshots / Rollback / Change Data Feed)</strong>, <strong>Schema Evolution (nhờ <code>Column ID</code> bất biến)</strong>, và cho phép chọn giữa <strong>Copy-on-Write (<code>COW</code> - tối ưu Đọc)</strong> hoặc <strong>Merge-on-Read (<code>MOR</code> - tối ưu Ghi/Streaming với <code>Positional / Equality Deletes</code>)</strong>.</li>
            <li><strong>Năm kỹ thuật bảo trì vật lý:</strong> Giúp bảng luôn chạy ở tốc độ đỉnh cao: <strong>Compaction (<code>Small File Problem</code>)</strong>, <strong>Hidden Partitioning &amp; Partition Evolution</strong>, <strong>Z-Ordering / Liquid Clustering (<code>Hilbert Curve</code>)</strong>, <strong>Deletion Vectors (<code>Roaring Bitmap</code>)</strong>, và <strong>Vacuum / Snapshot Expiration (<code>168 giờ</code> &amp; tuân thủ <code>GDPR</code>)</strong>.</li>
          </ol>
          <p style="margin-top:14px;"><strong>Câu hỏi dẫn sang Chặng 7 (Phần 4 — Chặng cuối cùng: Multi-hop Medallion Architecture &amp; Governance):</strong> Bây giờ bạn đã có trong tay những bảng Lakehouse (Delta / Iceberg / Hudi) cực kỳ mạnh mẽ! Nhưng trong một doanh nghiệp lớn, bạn không thể chỉ tạo 1 bảng duy nhất vừa hứng dữ liệu thô bẩn từ nguồn vừa cho Tổng Giám đốc cắm Power BI vào đọc. <strong>Làm thế nào để thiết kế dây chuyền tinh chế dữ liệu qua 3 tầng <code>Bronze ➔ Silver ➔ Gold</code> (kết hợp nhuần nhuyễn <code>MOR/COW</code>, <code>3NF/SCD2</code> và <code>Star Schema/OBT</code>), đồng thời quản trị danh mục (<code>Unity Catalog</code>), phả hệ (<code>Lineage</code>), bảo mật (<code>Row/Column Security</code>) và tối ưu tiền bạc (<code>FinOps</code>)?</strong> <a href="#topic=D02&stage=7" onclick="selectStorageStage(7);return false;">Đọc ngay Chặng 7 ──►</a></p>
        </section>
      </div>
    `;
  }

  function renderStorageChang7() {
    const d = HUB_DATA.storage_diagrams;
    return `
      <div class="prose">
        <p>Ở <strong>Chặng 6 (Phần 3)</strong>, chúng ta đã lắp thành công "bộ não giao dịch" (<strong>Delta Lake, Apache Iceberg, Apache Hudi</strong>) lên trên các tệp Parquet của Cloud Object Storage, giúp <strong>Đơn hàng <code>#8888</code></strong> có đầy đủ đặc tính <strong>ACID, Time Travel, Schema Enforcement</strong> và các chiến lược ghi/bảo trì vật lý (<strong>COW, MOR, Compaction, Z-Ordering, Vacuum</strong>).</p>
        <p>Bước vào <strong>Chặng 7 (Phần 4: Multi-Hop Architecture &amp; Governance)</strong> — chặng cuối cùng khép lại toàn bộ chương trình <strong>Storage Layer</strong> — chúng ta sẽ giải quyết bài toán quy hoạch ở cấp độ toàn doanh nghiệp: <em>Khi đã có công nghệ bảng Lakehouse trong tay, làm sao tổ chức luồng chảy của hàng tỷ đơn hàng từ lúc mới văng ra khỏi hệ thống nguồn đầy lỗi và trùng lặp cho đến khi trở thành những con số KPI tinh khiết trên màn hình của Tổng Giám đốc, đồng thời kiểm soát bảo mật, phả hệ và hóa đơn đám mây?</em></p>

        <h2 id="storage-7-1" tabindex="-1">TRẠM 7.1: KHÁI NIỆM MULTI-HOP &amp; TRIẾT LÝ KIẾN TRÚC MEDALLION (QUALITY GATING PATTERN)</h2>
        <p><em>(Tương ứng mục 01/ Khái niệm Multi-hop: Tinh chế dữ liệu lũy tiến qua từng chặng kiểm soát chất lượng)</em></p>

        <h3 id="storage-7-1-metaphor">1. Ẩn dụ đời thực: "Hành trình trưởng thành của Dữ liệu" &amp; "Nhà máy lọc nước 3 cấp"</h3>
        <p>Dữ liệu đang di chuyển trên đường ống (<code>data in flight</code>) ngoài đời thực vô cùng hỗn loạn: nó đổ về với đủ mọi hình dạng, kích thước, mức độ đầy đủ khác nhau, đôi khi đến trễ (<code>late-arriving data</code>) hoặc bị lỗi định dạng. Nếu cố viết một đoạn code duy nhất để biến dữ liệu thô vừa nạp về thành báo cáo cho Giám đốc ngay lập tức (<code>1-Hop</code>), đường ống sẽ liên tục gãy vụn mỗi khi nguồn phát sinh rác.</p>
        <p>Để giải quyết triệt để, <strong>Kiến trúc Medallion (Multi-Hop Architecture)</strong> ra đời như một khuôn mẫu thiết kế dữ liệu (<code>data design pattern</code>) giúp tổ chức dữ liệu logic trong Lakehouse qua các tầng cách ly để <strong>tinh chế dữ liệu lũy tiến qua từng cổng kiểm soát chất lượng (<code>progressively refining datasets via Quality Gating</code>)</strong>. Nhóm tác giả sách <em>Delta Lake: The Definitive Guide</em> (Ch. 9, tr. 228) ví von 3 tầng <strong>Bronze ➔ Silver ➔ Gold</strong> giống hệt như <strong>hành trình trưởng thành của một con người</strong>:</p>

        ${buildVisualBlock(
          "storage-7-1a",
          "Hình 7.1a — Kiến trúc Multi-hop Medallion & Cổng Kiểm soát Chất lượng (Quality Gating Pattern: Infancy ➔ Teenage ➔ Maturity)",
          d["7.1a"].ascii,
          d["7.1a"].mermaid,
          "Luồng tinh chế lũy tiến qua 3 tầng của kiến trúc Medallion: Bronze Layer (tuổi sơ sinh — giữ nguyên bản thô để Audit & Replay), Silver Layer (tuổi thiếu niên — lọc bỏ _corrupt, khử trùng và chuẩn hóa Enterprise View ~3NF/SCD2), và Gold Layer (tuổi trưởng thành — phi chuẩn hóa Star Schema/OBT và tổng hợp KPI phục vụ BI & AI/ML)."
        )}

        <h3 id="storage-7-1-why3">2. Tại sao phải tách thành 3 tầng (<code>Three-tiered framework</code>) thay vì 1 bước?</h3>
        <p>Lý do cốt lõi nhất của việc tách làm 3 tầng (<em>Delta Lake: The Definitive Guide</em>, tr. 228) là giúp đội ngũ kỹ sư <strong>luôn có một nơi an toàn để khôi phục hoặc quay lui (<code>recover or fall back on</code>) khi sự cố xảy ra hoặc khi yêu cầu nghiệp vụ thay đổi</strong> mà không bao giờ phải chọc ngược vào cơ sở dữ liệu OLTP đang chạy thật:</p>

        ${buildVisualBlock(
          "storage-7-1b",
          "Hình 7.1b — Đối chiếu Đường ống 1-Hop Mong manh vs. Kiến trúc 3-Tiered Medallion Có Chốt chặn Quay lui (Fallback & Replay)",
          d["7.1b"].ascii,
          d["7.1b"].mermaid,
          "So sánh đường ống 1-Hop trực tiếp (dễ gãy vụn khi gặp gói tin lỗi, không có điểm quay lui nên phải đọc lại từ DB OLTP) với kiến trúc 3-Tiered Medallion (lấy tầng Bronze làm mỏ neo bất biến để Replay, tầng Silver tái sử dụng toàn doanh nghiệp, và tầng Gold linh hoạt nối chuỗi)."
        )}

        <div class="callout">
          <div class="callout-title">Lưu ý kiến trúc thực chiến: Không cứng nhắc 3 bước máy móc (Delta Guide, tr. 299–300)</div>
          <p>Dù khuôn mẫu <code>Bronze ➔ Silver ➔ Gold</code> là phổ biến nhất, không có quy tắc cứng nhắc nào bắt buộc mọi luồng dữ liệu đều phải đi qua đúng 3 bước: (1) Nếu dữ liệu từ nguồn SaaS (như bảng chuẩn từ Salesforce) đã hoàn toàn sạch và khớp mục đích, có thể nạp thẳng vào tầng Curated/Gold; (2) Ngược lại, ở các hệ thống trưởng thành, kỹ sư thường xuyên <strong>nối các bảng Gold (Data Products) với nhau để tạo ra các bảng Gold mới</strong> phục vụ các bài toán chuyên sâu hơn.</p>
        </div>

        <h2 id="storage-7-2" tabindex="-1">TRẠM 7.2: GIẢI PHẪU CHI TIẾT 3 TẦNG MEDALLION QUA HÀNH TRÌNH ĐƠN HÀNG <code>#8888</code></h2>
        <p><em>(Tương ứng mục 02/ Mô hình Medallion: Bronze Layer ➔ Silver Layer ➔ Gold Layer)</em></p>

        <h3 id="storage-7-2-bronze">1. Tầng Bronze (<code>Bronze Layer / Raw Zone</code>) &amp; Kỹ thuật Cột Bảo toàn Lỗi (<code>_corrupt / _debug</code>)</h3>
        <p>Tầng Bronze đại diện cho điểm khởi đầu của phả hệ dữ liệu (<code>data lineage</code>) trong Lakehouse — đóng vai trò vùng hạ cánh (<code>landing zone</code>) lưu giữ bản sao nguyên trạng từ các nguồn như PostgreSQL CDC (qua Debezium/Flink vào <code>hudi_sales_transactions_bronze</code>) hoặc luồng clickstream từ Kafka (vào <code>hudi_web_clickstreams_bronze</code> — <em>Apache Hudi: The Definitive Guide</em>, tr. 252–253). Tại đây, kỹ sư chỉ áp dụng <strong>biến đổi tối thiểu (<code>minimal transformations</code>)</strong> theo cơ chế <strong>chỉ nối đuôi (<code>Append-only</code>)</strong> kèm cột ngữ cảnh (<code>_ingested_at</code>, <code>_source_topic</code>).</p>
        <p><strong>Tuyệt chiêu vận hành thực chiến — <code>Permissive Mode</code> &amp; Cột <code>_corrupt / _debug</code> (<em>Delta Lake: The Definitive Guide</em>, Example 9-4, tr. 230):</strong> Thay vì để một bản ghi lỗi định dạng (như Đơn <code>#8889</code> bị lỗi chuỗi tiền tệ <code>"ERROR_TIMEOUT"</code>) làm sập toàn bộ job Streaming lúc 2 giờ sáng hoặc bị âm thầm vứt bỏ (<code>DROPMALFORMED</code>), kỹ sư bật chế độ <code>PERMISSIVE</code> để gom phần dữ liệu lỗi vào cột <code>_corrupt</code> (hoặc <code>_debug</code>, <code>_rescued_data</code>) ở tầng Bronze rồi phân luồng tại cổng lên Silver:</p>

        ${buildVisualBlock(
          "storage-7-2a",
          "Hình 7.2a — Cơ chế Cột Bảo toàn Lỗi (Permissive Passthrough: _corrupt / _debug) & Cách ly Dữ liệu Bẩn (Quarantine / DLQ)",
          d["7.2a"].ascii,
          d["7.2a"].mermaid,
          "Cơ chế bảo vệ đường ống tại tầng Bronze bằng Spark Permissive Mode: bản ghi hợp lệ (#8888) có _corrupt = NULL được đi thẳng lên bảng Silver, trong khi bản ghi lỗi định dạng (#8889) được giữ nguyên bằng chứng trong cột _corrupt và tách sang bảng cách ly (Quarantine) để kỹ sư sửa lỗi và Replay."
        )}

        <h3 id="storage-7-2-journey">2. Hình hài của Đơn hàng <code>#8888</code> biến đổi qua 3 Tầng <code>Bronze ➔ Silver ➔ Gold</code></h3>
        <p>Hãy quan sát trực tiếp một bản ghi của <strong>Đơn hàng <code>#8888</code></strong> lột xác về mặt cấu trúc, kiểu dữ liệu và mô hình hóa khi chảy qua 3 bảng Lakehouse ở 3 tầng:</p>

        ${buildVisualBlock(
          "storage-7-2b",
          "Hình 7.2b — Hành trình Lột xác của Đơn hàng #8888 qua 3 Bảng Lakehouse (Bronze ➔ Silver ➔ Gold)",
          d["7.2b"].ascii,
          d["7.2b"].mermaid,
          "Sự biến đổi cụ thể của Đơn hàng #8888: từ 2 dòng JSON thô bị trùng lặp ở bảng bronze.sales_transactions_raw, được khử trùng (Dedup), lọc bỏ _corrupt, ép kiểu DECIMAL và ánh xạ khóa thay thế (~3NF/SCD2) ở bảng silver.orders_cleaned, cho đến khi được phi chuẩn hóa thành bảng phẳng gold.obt_customer_sales_analytics (0 JOIN) phục vụ BI."
        )}

        <h3 id="storage-7-2-matrix">3. Bảng Đối chiếu Toàn diện 3 Tầng Medallion (Bí kíp Phỏng vấn &amp; Thiết kế Kiến trúc)</h3>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Tiêu chí thiết kế</th>
                <th>1. Bronze Layer (Raw Zone)</th>
                <th>2. Silver Layer (Cleaned &amp; Conformed)</th>
                <th>3. Gold Layer (Curated / Serving)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Ẩn dụ &amp; Mục tiêu cốt lõi</strong></td>
                <td><strong>Tuổi sơ sinh (<code>Infancy</code>):</strong> Giữ nguyên bản lịch sử từ nguồn để phục vụ <strong>Audit</strong> và <strong>Replay / Recovery</strong> (không làm phiền DB OLTP).</td>
                <td><strong>Tuổi thiếu niên (<code>Teenage</code>):</strong> Lọc rác, khử trùng (<code>Dedup</code>), đối khớp đa nguồn tạo <strong>Enterprise View</strong> đáng tin cậy.</td>
                <td><strong>Tuổi trưởng thành (<code>Maturity</code>):</strong> Cung cấp dữ liệu thành phẩm tối ưu đọc cho từng dự án / mục tiêu kinh doanh cụ thể.</td>
              </tr>
              <tr>
                <td><strong>Mức độ biến đổi &amp; Xử lý lỗi</strong></td>
                <td>Tối thiểu (đổi sang định dạng bảng Lakehouse, thêm <code>_ingested_at</code>, hứng lỗi vào cột <code>_corrupt</code> / <code>_debug</code>).</td>
                <td>Lọc bỏ dòng <code>_corrupt IS NOT NULL</code> (đẩy sang <code>Quarantine</code>), xóa cột <code>_corrupt</code>, chuẩn hóa kiểu dữ liệu theo hướng <strong>ELT</strong>.</td>
                <td>Tổng hợp sẵn (<strong>Aggregated KPIs</strong>), áp dụng trọn vẹn quy tắc nghiệp vụ và kiểm định chất lượng nghiêm ngặt nhất.</td>
              </tr>
              <tr>
                <td><strong>Mô hình dữ liệu (Data Model)</strong></td>
                <td>Giữ nguyên cấu trúc nguồn (Payload JSON/Avro hoặc bảng thô Append-only).</td>
                <td>Chuẩn hóa thực thể gần <strong>3NF</strong>, <strong>Data Vault</strong> hoặc áp dụng <strong>SCD Type 2</strong> lưu lịch sử khách hàng/cửa hàng.</td>
                <td>Phi chuẩn hóa (<strong>Denormalized</strong>): <strong>Star Schema (Kimball)</strong> hoặc <strong>One Big Table (OBT)</strong> với ít phép <code>JOIN</code> nhất.</td>
              </tr>
              <tr>
                <td><strong>Chiến lược bảng Lakehouse &amp; Khóa mẫu</strong></td>
                <td><strong>Append-only</strong> hoặc <strong>MOR</strong> (nếu nhận CDC cập nhật nặng).<br>Ví dụ: <code>hudi_sales_transactions_bronze</code> (Key: <code>order_id + line_item_id</code>).</td>
                <td><strong>MOR</strong> hoặc <strong>COW + Deletion Vectors</strong> (tối ưu cho lệnh <code>MERGE / Upsert</code> khử trùng &amp; cập nhật SCD2).<br>Ví dụ: <code>silver.orders_cleaned</code>.</td>
                <td><strong>COW + Z-Ordering / Liquid Clustering</strong> (tối ưu tốc độ quét cột cực đại cho BI).<br>Ví dụ: <code>gold.obt_customer_sales_analytics</code>.</td>
              </tr>
              <tr>
                <td><strong>Người tiêu thụ chính</strong></td>
                <td>Pipeline kỹ thuật nội bộ (Data Engineering Ingestion &amp; Debugging — hạn chế cấp quyền rộng rãi).</td>
                <td>Data Engineers, Data Scientists, Self-Service Data Analysts cần dữ liệu sạch cấp độ chi tiết (<code>atomic grain</code>).</td>
                <td>Tổng Giám đốc, Business Users, Dashboard BI (Power BI, Tableau), Production ML / AI Agents.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3 id="storage-7-2-streaming">4. Streaming Medallion &amp; 3 Chốt chặn Kiểm định Chất lượng Tự động (<code>Expectations &amp; Constraints</code>)</h3>
        <p>Khi doanh nghiệp cần giảm độ trễ từ lúc khách bấm mua Đơn <code>#8888</code> đến lúc hiện lên Dashboard xuống mức cận thời gian thực, họ triển khai <strong>Streaming Medallion Architecture</strong> (dùng Spark Structured Streaming / Flink đọc luồng thay đổi tăng trưởng <code>Change Data Feed</code> từ Bronze ➔ Silver ➔ Gold — <em>Delta Lake: The Definitive Guide</em>, tr. 232–237) kết hợp <strong>3 hàng rào kiểm định tự động</strong>:</p>

        ${buildVisualBlock(
          "storage-7-2c",
          "Hình 7.2c — Ba Chốt chặn Kiểm định Chất lượng Tự động trong Streaming Medallion (Schema Gate, CHECK Constraints & DLT/WAP)",
          d["7.2c"].ascii,
          d["7.2c"].mermaid,
          "Ba lớp hàng rào bảo vệ chất lượng dữ liệu tự động khi chuyển tầng: (1) Khóa lược đồ với mergeSchema=false và overwriteSchema=false; (2) Ràng buộc cấp bảng ALTER TABLE ADD CONSTRAINT CHECK (net_amount > 0); (3) Bộ kỳ vọng @dlt.expect / expect_or_drop / expect_or_fail của Delta Live Tables hoặc mô hình nhánh Write-Audit-Publish (WAP) của Apache Iceberg."
        )}

        <h2 id="storage-7-3" tabindex="-1">TRẠM 7.3: DÒNG CHẢY NGẦM QUẢN TRỊ &amp; VẬN HÀNH (UNDERCURRENTS: CATALOG, LINEAGE, SECURITY &amp; FINOPS)</h2>
        <p><em>(Tương ứng mục 03/ Dòng chảy ngầm: Data Catalog, Lineage, Bảo mật Row/Col Security &amp; FinOps)</em></p>

        <p>Theo Joe Reis &amp; Matt Housley (<em>Fundamentals of Data Engineering</em>, Ch. 2, tr. 21) và <em>Delta Lake: The Definitive Guide</em> (Ch. 12–13, tr. 289–346), một nhà máy Medallion 3 tầng không thể đứng vững nếu thiếu các <strong>Dòng chảy ngầm (<code>Undercurrents</code>)</strong> chạy xuyên suốt mọi mắt xích từ Bronze sang Gold:</p>

        ${buildVisualBlock(
          "storage-7-3a",
          "Hình 7.3a — Kiến trúc Medallion được nâng đỡ bởi Các Dòng chảy Ngầm (The Undercurrents: Catalog, Lineage, Security & FinOps)",
          d["7.3a"].ascii,
          d["7.3a"].mermaid,
          "Mối quan hệ giữa luồng tinh chế ngang (Bronze -> Silver -> Gold) và 3 dòng chảy ngầm nâng đỡ bên dưới: (1) Data Catalog & Lineage tập trung; (2) Bảo mật chi tiết cấp dòng/cột & tuân thủ GDPR; (3) Quản trị vòng đời nhiệt độ lưu trữ Cloud FinOps."
        )}

        <h3 id="storage-7-3-ssot">1. Chấm dứt Cơn ác mộng "40 Thùng chứa riêng lẻ" bằng <code>Single Source of Truth</code> &amp; <code>Data Catalog</code></h3>
        <p>Trong thực tế vận hành (<em>Delta Lake: The Definitive Guide</em>, tr. 346 &amp; tr. 227), nhiều tổ chức mắc sai lầm chí mạng: thay vì giữ một bảng chuẩn duy nhất, họ <strong>xuất (<code>export</code>) các phân vùng của bảng Đơn hàng ra 40 vị trí bên ngoài khác nhau</strong> (40 Cloud Storage Buckets/Prefixes riêng biệt) cho 40 đội nhóm tiêu thụ. Hãy đặt phản mẫu này cạnh kiến trúc chuẩn mực dùng <strong>Unity Catalog / AWS Glue / Nessie</strong> (với không gian tên 3 cấp <code>catalog.schema.table</code>, ví dụ <code>prod.gold.customer_sales</code>) và <strong>OpenLineage</strong> (truy vết phả hệ chủ động qua 3 thực thể <code>Dataset ➔ Job ➔ Run</code>, tr. 334):</p>

        ${buildVisualBlock(
          "storage-7-3b",
          "Hình 7.3b — Phản mẫu Xuất bảng ra 40 Buckets riêng lẻ vs. Chuẩn mực Single Source of Truth & Unity Catalog",
          d["7.3b"].ascii,
          d["7.3b"].mermaid,
          "Đối chiếu phản mẫu nhân bản dữ liệu ra 40 Buckets riêng lẻ (gây ác mộng phân quyền IAM ở 40 nơi và tốn 40 lần chi phí tính toán lẫn phí băng thông Ingress/Egress khi cần chạy lại Đơn #8888) với kiến trúc Single Source of Truth kết hợp Catalog tập trung và Delta Sharing."
        )}

        <h3 id="storage-7-3-security">2. Bảo mật Chi tiết (<code>Row-Level Security</code> &amp; <code>Column Masking</code>) và Tuân thủ <code>GDPR</code></h3>
        <p>Thay vì phải nhân bản bảng dữ liệu ra nhiều nơi để che giấu thông tin nhạy cảm của Đơn hàng <code>#8888</code>, hệ thống quản trị Lakehouse áp dụng <strong>nguyên tắc đặc quyền tối thiểu (<code>Least Privilege</code>)</strong> bằng ngôn ngữ <code>SQL DCL (GRANT / REVOKE)</code> kết hợp <strong>bộ lọc dòng (<code>Row Filter</code>)</strong> và <strong>mặt nạ cột (<code>Column Mask</code>)</strong> ngay trên cùng một bảng vật lý:</p>

        ${buildVisualBlock(
          "storage-7-3c",
          "Hình 7.3c — Phân quyền Chi tiết (Row-Level Security & Column Masking) trên Cùng 1 Bảng Gold",
          d["7.3c"].ascii,
          d["7.3c"].mermaid,
          "Minh họa cơ chế phân quyền chi tiết trên cùng một bảng prod.gold.customer_sales: Giám đốc Chi nhánh Bình Dương bị áp Row-Level Security nên chỉ thấy Đơn #8888; Chuyên viên Phân tích bị áp Column Masking nên thấy cả 2 đơn nhưng số điện thoại cá nhân bị che thành xxxx-xxx-456."
        )}

        <ul>
          <li><strong>Tuân thủ Quyền được lãng quên (<code>GDPR / CCPA Right to be Forgotten</code>):</strong> Khi khách hàng Nguyễn Văn A yêu cầu xóa dữ liệu cá nhân, kỹ sư thực thi lệnh xóa xuyên suốt các tầng <code>Bronze ➔ Silver ➔ Gold</code> theo quy trình 3 bước khép kín: <strong>(1) <code>DELETE / MERGE</code></strong> (tạo <code>Deletion Vectors</code> đánh dấu xóa) ➔ <strong>(2) <code>REORG TABLE ... APPLY (PURGE)</code> / <code>OPTIMIZE</code></strong> (viết lại tệp vật lý loại bỏ hẳn bản ghi) ➔ <strong>(3) <code>VACUUM</code></strong> (xóa vĩnh viễn tệp Parquet lịch sử trên S3).</li>
        </ul>

        <h3 id="storage-7-3-finops">3. Cloud FinOps &amp; Quản trị Vòng đời Nhiệt độ Lưu trữ (<code>Storage Lifecycle Management</code>)</h3>
        <p>Mảnh ghép cuối cùng giúp người kỹ sư dữ liệu ghi điểm tuyệt đối với CTO là khả năng <strong>tối ưu hóa ngân sách đám mây (<code>FinOps</code>)</strong> thông qua việc kết hợp quy luật nhiệt độ dữ liệu ở Chặng 1 với vòng đời 6 giai đoạn của tài sản dữ liệu (<code>Creation ➔ Storage ➔ Usage ➔ Sharing ➔ Archiving ➔ Destruction</code> — <em>Delta Lake: The Definitive Guide</em>, Hình 12-2, tr. 297):</p>

        ${buildVisualBlock(
          "storage-7-3d",
          "Hình 7.3d — Vòng đời Nhiệt độ Dữ liệu & Tối ưu Chi phí Đám mây (Cloud FinOps Lifecycle: Hot ➔ Warm ➔ Cold/Archival)",
          d["7.3d"].ascii,
          d["7.3d"].mermaid,
          "Chính sách chuyển tầng lưu trữ tự động theo nhiệt độ dữ liệu: từ tầng Nóng (Hot Tier ~$0.023/GB cho bảng Gold/Silver đang truy vấn tích cực), sang tầng Ấm (Warm Tier ~$0.0125/GB sau 30–90 ngày), và xuống tầng Lạnh/Lưu trữ (Cold/Archival S3 Glacier / GCS Archive ~$0.004–$0.001/GB sau 180 ngày cho dữ liệu lịch sử tầng Bronze, tiết kiệm tới 1/17 chi phí)."
        )}

        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Chiến lược FinOps</th>
                <th>Cơ chế thực thi trên Lakehouse &amp; Cloud Storage</th>
                <th>Hiệu quả tiết kiệm &amp; Cạm bẫy kỹ thuật cần tránh</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>1. Dịch chuyển tự động theo Nhiệt độ (<code>Hot ➔ Warm ➔ Cold/Archival</code>)</strong></td>
                <td>• <strong>Gold / Silver đang hoạt động:</strong> Giữ ở <strong>Hot Tier</strong> (S3 Standard <code>~$0.023/GB/tháng</code> + Cache SSD/RAM).<br>• <strong>Dữ liệu lịch sử 30–90 ngày:</strong> Chuyển sang <strong>Warm Tier</strong> (S3 Standard-IA / GCS Nearline <code>~$0.0125/GB</code>).<br>• <strong>Dữ liệu Bronze quá hạn 6–12 tháng</strong> (chỉ giữ phòng kiểm toán/Replay): Tự động đẩy xuống <strong>Cold / Archival</strong> (S3 Glacier Instant <code>~$0.004/GB</code> hoặc Deep Archive <code>~$0.00099/GB</code>).</td>
                <td>• <strong>Hiệu quả:</strong> Giảm chi phí lưu trữ dài hạn xuống <strong>1/6 đến 1/17 lần</strong> mà vẫn bảo toàn 100% lịch sử.<br>• <strong>Cạm bẫy thực chiến:</strong> Các tầng Warm/Cold áp dụng <strong>Thời gian lưu giữ tối thiểu (<code>Minimum Storage Duration</code>: 30 / 90 / 180 ngày)</strong> và <strong>Phí kéo dữ liệu (<code>Retrieval Fee</code>)</strong> — tuyệt đối không bật Lifecycle chuyển xuống Glacier cho các tệp Parquet đang bị xóa sớm bởi <code>VACUUM 7 ngày</code>!</td>
              </tr>
              <tr>
                <td><strong>2. Dọn dẹp Bảng &amp; Xóa bỏ Bản sao Dư thừa (<code>Vacuum &amp; Fewer Copies</code>)</strong></td>
                <td>• Chạy <code>VACUUM</code> / <code>expire_snapshots</code> định kỳ để xóa các tệp Parquet lịch sử đã quá hạn Time Travel.<br>• Phục vụ cả BI lẫn ML ngay trên 1 nền tảng Lakehouse (kết hợp <code>UniForm</code> / <code>Single Source of Truth</code>) để xóa bỏ các bản sao trùng lặp giữa Data Lake và Data Warehouse.</td>
                <td>• <strong>Hiệu quả:</strong> Cắt giảm dung lượng S3 phình thừa và xóa bỏ hoàn toàn chi phí tính toán + băng thông mạng 2 chiều (<code>Ingress/Egress</code>) do phải chép dữ liệu qua lại giữa nhiều hệ thống (<code>Fewer copies = less drift &amp; lower cost</code>).</td>
              </tr>
              <tr>
                <td><strong>3. Điều phối Cụm tính toán Tạm thời (<code>Ephemeral Compute</code>)</strong></td>
                <td>• Tận dụng triệt để nguyên lý <strong>tách rời Compute và Storage</strong>: chỉ khởi tạo cụm Spark / Flink / Serverless SQL Warehouse khi chạy pipeline Medallion hoặc khi có truy vấn BI, và tự động tắt (<code>Auto-stop / Scale-to-Zero</code>) ngay khi hoàn tất.</td>
                <td>• <strong>Hiệu quả:</strong> Tránh lãng phí hàng chục nghìn USD mỗi tháng cho các cụm máy chủ bật không tải (<code>Idle Compute</code>) 24/7.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h2 id="storage-7-4" tabindex="-1">TRẠM 7.4: BẢN ĐỒ KIẾN TRÚC TỔNG THỂ 6 TẦNG (BOTTOM-UP BLUEPRINT) — KHÉP LẠI TOÀN BỘ KHÓA HỌC!</h2>
        <p><em>(Tương ứng bức tranh tổng thành toàn bộ học phần D02 · Storage Layer từ Chặng 1 đến Chặng 7)</em></p>

        <p>Đi hết <strong>Chặng 7</strong>, bạn đã hoàn thành trọn vẹn <strong>100% chương trình Storage Layer</strong> (bao trọn toàn bộ 59 trang <code>08-storage-layer.pdf</code> và 5 cuốn sách chuyên khảo cốt lõi). Để bạn có thể nhìn thấu suốt toàn bộ 7 Chặng vừa học chỉ trong <strong>1 bức tranh duy nhất đi từ phần cứng vật lý dưới cùng lên tới tầng Quản trị và Phục vụ trên cùng</strong>, dưới đây là <strong>Bản đồ Kiến trúc 6 Tầng (Bottom-Up Blueprint)</strong> cùng bảng tổng kết trọn đời của <strong>Đơn hàng <code>#8888</code></strong>:</p>

        ${buildVisualBlock(
          "storage-7-4",
          "Hình 7.4 — Bản đồ Kiến trúc 6 Tầng của Hệ thống Lưu trữ Hiện đại (Bottom-Up Blueprint: Chặng 1 ➔ Chặng 7)",
          d["7.4"].ascii,
          d["7.4"].mermaid,
          "Bản đồ kiến trúc 6 tầng tổng hợp toàn bộ học phần Storage Layer từ dưới lên trên: (1) Nền móng Vật lý & Mô hình Lưu trữ; (2) Định dạng Tệp, In-Memory Arrow & Nén; (3) Bộ ba Open Table Formats (Delta, Iceberg, Hudi); (4) Động cơ Tính toán & Streaming tách rời Lưu trữ; (5) Mô hình hóa Medallion & Kimball; (6) Tầng Phục vụ & Dòng chảy ngầm Quản trị (Catalog, Lineage, Security, FinOps)."
        )}

        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Chặng học</th>
                <th>Trạm dừng của Đơn hàng <code>#8888</code></th>
                <th>Nỗi đau kỹ thuật phát sinh</th>
                <th>Giải pháp &amp; Vũ khí Kiến trúc Cốt lõi</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Chặng 1</strong><br><em>Vật lý &amp; Phần cứng</em></td>
                <td>Khách bấm mua Đơn <code>#8888</code> (<code>15.000.000đ</code>) trên hệ thống <code>OLTP</code>; cuối tháng chạy báo cáo phân tích <code>OLAP</code>.</td>
                <td>CPU Cache (<code>1 ns</code>) &amp; RAM (<code>100 ns</code>) quá đắt và dễ bay hơi (<code>Spill-to-Disk</code>); Đĩa cứng HDD bị nghẽn bởi <code>Random Seek (4–10 ms, ~100 IOPS)</code>.</td>
                <td>Tách biệt <code>OLTP</code> (đọc/ghi ngẫu nhiên từng dòng) với <code>OLAP</code> (quét tuần tự <code>Sequential Scan</code>); phân tầng nhiệt độ <code>Hot (RAM/SSD) ➔ Warm ➔ Cold (Object Storage)</code>.</td>
              </tr>
              <tr>
                <td><strong>Chặng 2</strong><br><em>Mô hình &amp; File Format</em></td>
                <td>Đóng gói hàng tỷ đơn hàng xuống đĩa và truyền qua RAM giữa các công cụ phân tích.</td>
                <td>Định dạng dòng (<code>CSV/JSON</code>) bắt phải đọc cả 50 cột dù chỉ cần cộng cột <code>So_Tien</code>; chuyển đổi dữ liệu trên RAM tốn 80% CPU (<code>SerDe overhead</code>).</td>
                <td>Lưu trữ trên <strong>Cloud Object Storage (S3)</strong> dưới định dạng cột <strong>Apache Parquet</strong> (<code>Row Group + Column Chunk + Footer Min/Max</code>) nén bằng <code>Snappy / ZSTD</code>; xử lý trên RAM bằng <strong>Apache Arrow</strong> (<code>Zero-copy SIMD</code>).</td>
              </tr>
              <tr>
                <td><strong>Chặng 3</strong><br><em>Phân tán, Stream &amp; DW</em></td>
                <td>Vận chuyển Đơn <code>#8888</code> theo thời gian thực và đưa vào kho phân tích tập trung.</td>
                <td>Một máy chủ không chứa nổi Petabyte dữ liệu; kéo dữ liệu kiểu Batch hàng đêm gây trễ 24 giờ và làm nghẽn DB nguồn.</td>
                <td>Lưu trữ phân tán <strong>HDFS (nhân bản x3, Rack-awareness)</strong>; bắt biến động tức thì bằng <strong>Debezium CDC ➔ Apache Kafka</strong>; phân tích chuẩn mực bằng <strong>Cloud Data Warehouse (Snowflake / BigQuery)</strong>.</td>
              </tr>
              <tr>
                <td><strong>Chặng 4</strong><br><em>Data Modeling &amp; Kimball</em></td>
                <td>Thiết kế cấu trúc bảng cho Đơn <code>#8888</code> để Giám đốc truy vấn doanh thu theo Tỉnh Thành, Sản Phẩm.</td>
                <td>Mô hình chuẩn hóa <code>3NF</code> bắt phải <code>JOIN</code> hàng chục bảng làm treo báo cáo; khi khách Nguyễn Văn A chuyển nhà từ Hà Nội vào Bình Dương làm lệch lịch sử doanh thu cũ.</td>
                <td>Thiết kế <strong>Star Schema (Kimball)</strong> hoặc <strong>OBT</strong> với bảng <code>Fact</code> (khóa độ mịn <code>Grain</code>) + <code>Dimension</code>, dùng khóa thay thế <strong>Surrogate Key</strong>, theo dõi lịch sử bằng <strong>SCD Type 2</strong> và liên kết qua <strong>Enterprise Bus Matrix</strong>.</td>
              </tr>
              <tr>
                <td><strong>Chặng 5</strong><br><em>Data Lake &amp; Data Swamp</em></td>
                <td>Đổ thêm hàng triệu tệp JSON clickstream và ảnh giao hàng của Đơn <code>#8888</code> xuống hồ dữ liệu S3 giá rẻ (<code>$0.02/GB</code>).</td>
                <td>Cơ chế <code>Schema-on-Read</code> buông lỏng biến Data Lake thành <strong>Data Swamp</strong>: job Spark đứt mạng để lại tệp rác <code>3.parquet</code> làm nhân đôi doanh thu Đơn <code>#8888</code>; bảng Hive quét thư mục chậm chạp, không có <code>ACID</code>, bất lực trước lệnh xóa <code>GDPR</code>.</td>
                <td>Áp dụng phác đồ tổ chức bước đầu: <strong>Data Zoning</strong>, ký <strong>Data Contracts (Schema Registry)</strong>, triển khai <strong>Data Observability (5 trụ cột)</strong> và tìm kiếm một lớp giao dịch <code>ACID</code> ngay trên S3.</td>
              </tr>
              <tr>
                <td><strong>Chặng 6</strong><br><em>Lakehouse &amp; Open Table Formats</em></td>
                <td>Lắp "bộ não giao dịch" lên các tệp Parquet của Đơn <code>#8888</code> trên S3.</td>
                <td>Làm sao để tệp Parquet bất biến trên S3 có giao dịch <code>ACID</code>, cập nhật/xóa dòng (<code>UPDATE/DELETE</code>), du hành thời gian (<code>Time Travel</code>) và chống phình hàng vạn tệp nhỏ?</td>
                <td>Sử dụng bộ ba <strong>Open Table Formats</strong>: <strong>Delta Lake (<code>_delta_log</code>)</strong>, <strong>Apache Iceberg (<code>3-layer Metadata Tree + Hidden Partitioning</code>)</strong>, <strong>Apache Hudi (<code>Timeline + Indexing</code>)</strong>; kết hợp <code>MVCC/OCC</code>, <code>COW vs. MOR</code>, <code>Compaction</code>, <code>Z-Ordering / Liquid Clustering</code>, <code>Deletion Vectors</code>, <code>Vacuum</code> và hợp nhất qua <code>UniForm / XTable</code>.</td>
              </tr>
              <tr>
                <td><strong>Chặng 7</strong><br><em>Medallion &amp; Governance</em></td>
                <td>Quy hoạch dây chuyền sản xuất toàn doanh nghiệp cho Đơn <code>#8888</code> từ nguồn thô đến màn hình CEO.</td>
                <td>Làm sao vừa hứng dữ liệu bẩn/trùng lặp không gãy đường ống, vừa tái sử dụng dữ liệu sạch cho nhiều phòng ban, bảo mật PII theo vai trò và tối ưu hóa đơn đám mây?</td>
                <td>Kiến trúc <strong>Multi-hop Medallion</strong>: <code>Bronze (Raw + _corrupt / Replay) ➔ Silver (Cleaned ~3NF/SCD2 + CHECK/Expectations) ➔ Gold (Curated Star/OBT)</code>, được nâng đỡ bởi <strong>Unity Catalog / Lineage</strong>, <strong>Row-Level Security &amp; Column Masking</strong>, <strong>GDPR Purge</strong> và <strong>Cloud FinOps (Hot ➔ Warm ➔ Glacier 1/17 giá)</strong>.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <section class="summary-section" id="storage-7-summary" tabindex="-1">
          <h2>CHECKLIST TỔNG KẾT CHẶNG 7 (NHẮM MẮT TRẢ LỜI ĐƯỢC LÀ LÀM CHỦ HOÀN TOÀN)</h2>
          <ol>
            <li><strong>Tại sao phải lọc dữ liệu qua 3 tầng <code>Bronze ➔ Silver ➔ Gold</code> mà không làm 1 bước (<code>1-Hop</code>)?</strong> ➔ Để kiểm soát chất lượng lũy tiến qua từng cổng (<code>Quality Gating</code>), tái sử dụng dữ liệu sạch cấp doanh nghiệp ở tầng <strong>Silver</strong> cho nhiều phòng ban, và luôn có tầng <strong>Bronze</strong> nguyên bản làm mỏ neo an toàn để <strong>chạy lại (<code>Replay / Recovery</code>)</strong> khi logic tầng trên bị lỗi hoặc khi yêu cầu kinh doanh thay đổi mà không cần chọc lại vào DB OLTP nguồn.</li>
            <li><strong>Mô hình dữ liệu và chiến lược bảng Lakehouse ở tầng <code>Silver</code> và tầng <code>Gold</code> khác nhau thế nào?</strong> ➔ Tầng <strong>Silver</strong> hướng tới góc nhìn thực thể toàn doanh nghiệp nên chuẩn hóa gần <strong>3NF / Data Vault / SCD Type 2</strong> và ưu tiên bảng <strong>MOR hoặc COW + Deletion Vectors</strong> để xử lý lệnh <code>MERGE / Upsert</code> khử trùng nhanh; tầng <strong>Gold</strong> hướng tới tốc độ đọc báo cáo BI và AI cụ thể nên phi chuẩn hóa thành <strong>Star Schema</strong> hoặc <strong>One Big Table (OBT)</strong> (giảm tối đa phép <code>JOIN</code>) và ưu tiên bảng <strong>COW + Z-Ordering / Liquid Clustering</strong>.</li>
            <li><strong>Cột <code>_corrupt</code> (hoặc <code>_debug</code> / <code>_rescued_data</code>) nằm ở tầng nào và vận hành ra sao?</strong> ➔ Nằm ở tầng <strong>Bronze</strong> (khi bật chế độ <code>PERMISSIVE</code>): dùng để hứng và bảo toàn nguyên vẹn các bản ghi bị lỗi định dạng lúc nạp mà không làm gãy đường ống Streaming, sau đó tại cổng chuyển sang Silver sẽ lọc các dòng <code>_corrupt IS NOT NULL</code> đẩy sang bảng cách ly (<code>Quarantine</code>) để kỹ sư xử lý và bỏ cột <code>_corrupt</code> khỏi bảng Silver sạch.</li>
            <li><strong>Tại sao không nên xuất (<code>export</code>) dữ liệu bảng ra 40 Buckets riêng cho 40 phòng ban?</strong> ➔ Vì nó phá vỡ nguyên tắc <strong>Single Source of Truth</strong>, gây ác mộng quản lý/thu hồi quyền truy cập ở 40 nơi và đốt tiền tính toán lẫn phí băng thông mạng hai chiều (<code>ingress/egress costs</code>) mỗi khi cần sửa lỗi và chạy lại (<code>reprocess</code>) dữ liệu. Giải pháp chuẩn là giữ 1 bảng duy nhất và phân quyền qua <strong>Unity Catalog / Delta Sharing</strong> kèm <strong>Row-Level Security &amp; Column Masking</strong>.</li>
            <li><strong>Làm sao vừa giữ lịch sử ở tầng Bronze nhiều năm để kiểm toán vừa không bị cháy túi tiền Cloud?</strong> ➔ Áp dụng chính sách vòng đời <strong>Cloud FinOps</strong>: tự động chuyển dữ liệu lịch sử từ tầng <strong>Hot / Warm Object Storage</strong> (<code>~$0.023 ➔ $0.0125/GB/tháng</code>) xuống tầng <strong>Cold / Archival Storage (S3 Glacier / GCS Archive)</strong> (<code>~$0.004 – $0.001/GB/tháng</code> — rẻ bằng <code>1/6 đến 1/17</code>), kết hợp chạy <code>VACUUM</code> dọn các tệp quá hạn Time Travel trên bảng nóng và dùng cụm tính toán tạm thời (<code>Ephemeral Compute</code>).</li>
          </ol>
          <p style="margin-top:14px;"><strong>Hoàn tất 100% Học phần D02 · Storage Layer (Chặng 1 ➔ Chặng 7):</strong> Bạn đã nắm trọn chuỗi nhân – quả xuyên suốt từ độ trễ nano-giây của CPU/RAM, cấu trúc byte của Parquet/Arrow, hạ tầng phân tán HDFS/Kafka, nghệ thuật mô hình hóa Kimball, sự trỗi dậy của bộ ba Lakehouse (Delta Lake, Apache Iceberg, Apache Hudi) cho đến kiến trúc Multi-hop Medallion và Quản trị Doanh nghiệp. <a href="#topic=D02&stage=1" onclick="selectStorageStage(1);return false;">Quay lại ôn tập từ Chặng 1 ──►</a></p>
        </section>
      </div>
    `;
  }

  function toggleStageDirectory() {
    const dir = document.getElementById("stageDirectoryPanel");
    const btn = document.getElementById("stageDirectoryToggleBtn");
    if (!dir || !btn) return;
    const isOpen = dir.classList.toggle("open");
    btn.setAttribute("aria-expanded", isOpen ? "true" : "false");
  }

  function renderLinuxChang1() {
    const d = HUB_DATA.linux_diagrams;
    return `
      <div class="prose">
        <p><strong>Chặng 1: Hạt nhân, Hệ sinh thái GNU/Linux &amp; Luồng chạy cơ học của một lệnh</strong> mở màn cho toàn bộ chương trình <strong>I. Engineering Foundation — F01 · Linux Fundamentals</strong> (bám sát 100% <code>course-slides/01-linux-fundamentals.pdf</code> — 78 trang, kết hợp nền tảng cơ học từ bộ 3 sách kinh điển: <em>The Linux Programming Interface</em> của Michael Kerrisk, <em>Operating Systems: Three Easy Pieces</em> của Remzi &amp; Andrea Arpaci-Dusseau, và <em>Computer Systems: A Programmer's Perspective</em> của Bryant &amp; O'Hallaron).</p>

        <h2 id="linux-0-map" tabindex="-1">TRẠM 0.0: NHÂN VẬT CHÍNH grep ERROR /var/log/app.log &amp; BẢN ĐỒ CƠ HỌC 4 CHẶNG</h2>
        <p><em>(Bước 0 — Thiết lập Nhân vật chính xuyên suốt, Bản đồ Cơ học 4 Chặng &amp; Ma trận Đối chiếu Slide ↔ Sách trước khi đi sâu từng Trạm)</em></p>

        ${buildSpineHeroBanner(
          "linux-0-1",
          "SPINE HERO MINDMAP · STYLE #2",
          "Bản đồ Tư duy Kiến trúc 4 Chặng Linux Fundamentals — Chiến dịch grep ERROR /var/log/app.log",
          "PROMPT-ARCH-DIAGRAM · 16:9 Dark-Slate Blueprint",
          "assets/visuals/linux-0-map.jpg",
          "<strong>Bản đồ Xương sống Học phần F01 (Spine Hero Mindmap):</strong> Tổng quan 4 Chặng Linux Fundamentals xoay quanh nhân vật chính <code>grep ERROR /var/log/app.log</code> — từ <code>Kernel / Shell / CLI</code> (Chặng 1), <code>Process &amp; Cây thư mục hợp nhất /</code> (Chặng 2), <code>IPC 3 cổng 0/1/2 &amp; Đường ống Pipe</code> (Chặng 3) đến <code>Dây chuyền tự động hóa 24/7: Bash Script + GCC/Makefile + Cronjob</code> (Chặng 4)."
        )}

        <h3 id="linux-0-protagonist">1. Nhân vật chính Xuyên suốt Học phần: Chiến dịch <code>grep ERROR /var/log/app.log</code></h3>
        <p>Để kết nối toàn bộ kiến trúc trong <strong>Slide bài giảng (<code>01-linux-fundamentals.pdf</code>)</strong> với tư duy cơ học <strong>"Căn bếp Linux"</strong>, chúng ta không học từng câu lệnh rời rạc. Thay vào đó, toàn bộ học phần sẽ theo chân một nhân vật chính duy nhất từ lúc sinh ra cho đến khi vận hành tự động hoàn toàn: <strong>Chiến dịch săn lùng dòng nhật ký lỗi <code>grep ERROR /var/log/app.log</code></strong> (với đối tượng mục tiêu là tệp nhật ký hệ thống <code>app.log</code> đang phình to từng giây trong thư mục <code>/var/log</code>).</p>

        ${buildVisualBlock(
          "linux-0-1",
          "Hình 0.1 — Hành trình 4 Bước Tiến Hóa của Nhân Vật Chính grep ERROR /var/log/app.log (Xuyên suốt 4 Chặng)",
          d["0.1"].ascii,
          d["0.1"].mermaid,
          "Bốn cột mốc tiến hóa của lệnh grep ERROR /var/log/app.log xuyên suốt 4 Chặng: (1) Từ dòng chữ tĩnh trên Terminal biến thành Process động trên RAM/CPU; (2) Cầm phiếu System Call vượt ranh giới bảo mật của Linux Kernel; (3) Nối ống Pipe qua 3 cổng stdin(0)/stdout(1)/stderr(2); (4) Đóng gói thành dây chuyền tự động hóa 24/7 với Bash Script, GCC/Makefile và Cronjob."
        )}

        <ul>
          <li><strong>(1) Từ tĩnh sang động (Chặng 1):</strong> Khởi đầu chỉ là dòng chữ tĩnh gõ trên <code>Terminal</code> (Quầy giao tiếp), lệnh <code>grep</code> buộc phải nhờ <code>Shell</code> (Người nhận việc) đánh thức <code>Program</code> (Công thức nấu ăn <code>/bin/grep</code> nằm im trên ổ cứng) thông qua cặp lời gọi <code>fork() + execve()</code> để biến thành một <code>Process</code> (Người đầu bếp thực sự xắn tay vào làm việc trên <code>RAM</code> và <code>CPU</code>).</li>
          <li><strong>(2) Va chạm ranh giới bảo mật (Chặng 2):</strong> Muốn chạm vào tệp <code>/var/log/app.log</code>, <code>Process</code> ở tầng <code>User Space</code> không được tự ý lục kho mà phải cầm tờ phiếu <code>System Call</code> (Lời gọi hệ thống <code>open()</code>, <code>read()</code>) trình lên <code>Linux Kernel</code> (Bếp trưởng/Quản lý kho ở <code>Kernel Space</code>) để xét duyệt hồ sơ căn cước 5 thuộc tính (<code>PID</code>, <code>User/Group UID/GID</code>, <code>Working Directory</code>, <code>Environment $PATH</code>, <code>Open Files</code>) trên cây thư mục hợp nhất <code>/</code>.</li>
          <li><strong>(3) Phối hợp dây chuyền IPC (Chặng 3):</strong> Khi một mình <code>grep</code> làm không xuể, nó phải nối ống <code>Pipe (|)</code> qua 3 cổng giao tiếp tiêu chuẩn (<code>stdin: 0</code>, <code>stdout: 1</code>, <code>stderr: 2</code>) để chuyền dòng dữ liệu trên bộ đệm <code>RAM</code> của <code>Kernel</code> cho các tiến trình khác lọc tiếp mà không làm lẫn thông báo lỗi vào kết quả (<code>2&gt;&amp;1</code>).</li>
          <li><strong>(4) Tự động hóa công nghiệp 24/7 (Chặng 4):</strong> Thay vì bắt kỹ sư thức dậy lúc <code>03:00 sáng</code> gõ tay từng lệnh hay biên dịch lại công cụ phân tích viết bằng C (<code>GCC</code> — trình biên dịch mã nguồn sang mã máy), toàn bộ quy trình được đóng gói vào <code>Bash Script (.sh)</code> (Làm các bước nào), kiểm soát biên dịch thông minh qua <code>Makefile</code> (Xét <code>timestamp</code> xem có cần làm lại không), và đặt lịch kích hoạt tự động mỗi <code>60 giây</code> nhờ <code>Cronjob (crond)</code> (Khi nào bắt đầu chạy).</li>
        </ul>

        <h3 id="linux-0-mental-map">2. Bản đồ Tư duy 1 Dòng (Mental Map) — Mạch Nhân Quả Toàn Học Phần</h3>
        <p>Sơ đồ dưới đây tổng hợp kiến trúc từ <strong>Slide bài giảng (<code>01-linux-fundamentals.pdf</code>)</strong>, mô hình cơ học <strong>"Căn bếp Linux"</strong> và cơ chế hệ điều hành từ sách <em>The Linux Programming Interface (TLPI)</em> &amp; <em>Operating Systems: Three Easy Pieces (OSTEP)</em>:</p>

        ${buildVisualBlock(
          "linux-0-2",
          "Hình 0.2 — Bản đồ Cơ học Linux: Mô hình 'Căn bếp' & Dây chuyền Tự động hóa 4 Chặng (Mental Map)",
          d["0.2"].ascii,
          d["0.2"].mermaid,
          "Bản đồ giải phẫu tổng thể 3 tầng (4 Chặng): Từ luồng chạy 1 lệnh (Chặng 1) và hồ sơ căn cước Process trên cây thư mục / (Chặng 2), đi qua ranh giới System Call & Linux Kernel điều phối 4 tài nguyên (File, CPU, RAM, Network), đến phối hợp đa tiến trình qua cổng 0/1/2 & Pipe (Chặng 3) và tự động hóa 24/7 bằng Bash Script, Make & Cronjob (Chặng 4)."
        )}

        <h3 id="linux-0-roadmap">3. Bảng Đối chiếu Lộ trình 4 Chặng (Khớp nối Slide Bài giảng, Sách Tham khảo &amp; Tư duy Tự học)</h3>
        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Chặng &amp; Trạm</th>
                <th>Trọng tâm Kiến thức (Slide <code>01-linux-fundamentals.pdf</code> + Sách <code>TLPI / OSTEP / CS:APP</code>)</th>
                <th>Nỗi đau (Pain Point) Khởi phát</th>
                <th>Cơ chế Giải quyết Nhân – Quả</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>CHẶNG 1</strong><br><strong>Hạt nhân, Hệ sinh thái &amp; Luồng chạy 1 lệnh</strong><br><em>(Trạm 1.1 ➔ 1.3)</em></td>
                <td>• Lịch sử <code>GNU/Linux</code> (<code>GNU Tools</code> + <code>Linux Kernel</code>), <code>Open Source</code> (<code>$0</code> bản quyền), 6 ưu điểm cốt lõi.<br>• 4 <code>Distro</code> tiêu biểu (<code>Ubuntu</code>, <code>RHEL</code>, <code>Kali</code>, <code>Linux Mint</code>).<br>• Kiến trúc 3 tầng &amp; Luồng chạy thực tế: <code>Terminal</code> ➔ <code>Shell</code> ➔ <code>Program</code> ➔ <code>Process</code> ➔ <code>System Call</code> ➔ <code>Kernel</code> ➔ <code>Hardware</code> (<em>TLPI</em> Ch. 1–3, <em>OSTEP</em> Ch. 4–6).</td>
                <td>Có cục máy <code>Kernel</code> điều khiển phần cứng nhưng con người không thể giao tiếp bằng mã nhị phân <code>0–1</code>; gõ một lệnh <code>grep</code> vào màn hình đen thì chuyện gì thực sự xảy ra bên dưới?</td>
                <td>Ghép bộ công cụ <code>GNU</code> (<code>Bash</code>, <code>Coreutils</code>, <code>GCC</code>) bọc ngoài <code>Linux Kernel</code>. Phân vai chặt chẽ: <code>Kernel</code> chỉ mở kho <code>File</code> theo quyền qua <code>System Call</code>, còn logic tìm chữ <code>ERROR</code> do <code>Process</code> (<code>grep</code>) tự làm trên <code>CPU/RAM</code>.</td>
              </tr>
              <tr>
                <td><strong>CHẶNG 2</strong><br><strong>Giải phẫu Process, Triết lý File &amp; Cây thư mục</strong><br><em>(Trạm 2.1 ➔ 2.3)</em></td>
                <td>• Hồ sơ một <code>Process</code>: <code>PID</code>, <code>User/Group (UID/GID)</code>, <code>Working Directory</code>, <code>Environment ($PATH)</code>, <code>Open Files</code> (<em>TLPI</em> Ch. 6, 8, 9).<br>• Triết lý <code>"Everything is a file"</code> (File thường, Thư mục, Thiết bị <code>/dev/sda</code>, Tiến trình <code>/proc/1234</code>).<br>• Cây thư mục duy nhất <code>/</code>: <code>/home</code>, <code>/root</code>, <code>/tmp</code>, <code>/var</code>, <code>/bin</code>, <code>/sbin</code>, <code>/etc</code>, <code>/usr</code>, <code>/proc</code> (<code>0 MB</code> ổ cứng) &amp; đối chiếu với Windows (<em>TLPI</em> Ch. 12, 14, 18; <em>OSTEP</em> Ch. 39–40).</td>
                <td>Hàng trăm <code>Process</code> của 50 người dùng (<code>Multi-user</code>) cùng chạy một lúc: Làm sao <code>Kernel</code> biết ai được chạm vào phần cứng nào, và làm sao dùng chung một bộ lệnh (<code>cat</code>, <code>cp</code>) cho cả văn bản lẫn ổ cứng, <code>CPU</code>?</td>
                <td>Gắn "chứng minh thư" 5 thuộc tính vào mỗi <code>Process</code>. Biến mọi thực thể vật lý và logic thành <code>File</code> nằm trên một cây thư mục gốc <code>/</code> duy nhất để kiểm soát quyền hạn (<code>rwx</code>) đến từng byte.</td>
              </tr>
              <tr>
                <td><strong>CHẶNG 3</strong><br><strong>Giao tiếp Đa tiến trình (IPC) &amp; Điều hướng I/O</strong><br><em>(Trạm 3.1 ➔ 3.2)</em></td>
                <td>• Ba cổng tiêu chuẩn của mọi <code>Process</code>: <code>stdin (0)</code>, <code>stdout (1)</code>, <code>stderr (2)</code> (<em>TLPI</em> Ch. 4–5; <em>CS:APP</em> Ch. 10).<br>• Cơ chế <code>Pipe (|)</code> (Đường ống truyền byte trên bộ đệm <code>RAM 64 KB</code> trong <code>Kernel</code> — <em>TLPI</em> Ch. 44) và điều hướng luồng dữ liệu/luồng lỗi (<code>&gt;</code>, <code>&gt;&gt;</code>, <code>2&gt;</code>, <code>2&gt;&amp;1</code>).</td>
                <td>Một <code>Program</code> đơn lẻ chỉ làm tốt 1 việc nhỏ. Nếu xuất kết quả trung gian ra ổ cứng rồi đọc lại sẽ rất chậm, và nếu chương trình báo lỗi thì dòng chữ lỗi sẽ làm hỏng dữ liệu đầu vào của bước kế tiếp.</td>
                <td>Thiết kế 3 cổng File Descriptor <code>0, 1, 2</code> độc lập cho mỗi <code>Process</code>. <code>Shell</code> đấu nối cổng <code>stdout (1)</code> của anh trước vào <code>stdin (0)</code> của anh sau qua đường ống <code>Pipe</code> trên <code>RAM</code> do <code>Kernel</code> giữ, đồng thời tách riêng <code>stderr (2)</code> đi đường khác.</td>
              </tr>
              <tr>
                <td><strong>CHẶNG 4</strong><br><strong>Dây chuyền Tự động hóa: Script, Make &amp; Cron</strong><br><em>(Trạm 4.1 ➔ 4.3)</em></td>
                <td>• Phân cấp <code>Shell</code> ➔ <code>Bash</code> ➔ <code>Bash Scripting</code> (<code>#!/bin/bash</code>, biến, <code>if/else</code>, <code>for</code>, <code>chmod +x</code> — <em>TLPI</em> Ch. 27).<br>• Quá trình <code>Compilation</code> với <code>GCC</code> (<code>.c</code> ➔ <code>.o</code> ➔ <code>binary</code> — <em>CS:APP</em> Ch. 1, 7) &amp; quản đốc <code>Makefile</code> (<code>Target</code>, <code>Prerequisites</code>, <code>Recipe</code> với phím <code>TAB</code>).<br>• Hệ thống hẹn giờ <code>Cron</code> (<code>crond</code> quét mỗi <code>60 giây</code>, <code>Crontab</code>, <code>Cronjob * * * * *</code> — <em>TLPI</em> Ch. 37) và 3 cạm bẫy kinh điển.</td>
                <td>Kỹ sư không thể ngồi gõ lại 20 lệnh mỗi sáng, không thể chờ biên dịch lại toàn bộ 100 file code C khi chỉ sửa 1 dòng, và không thể thức lúc <code>03:00 sáng</code> để bấm nút chạy kiểm tra log hay backup.</td>
                <td>Tam giác tự động hóa khép kín:<br>1. <code>Bash Script</code>: Định nghĩa <strong>làm bước nào</strong>.<br>2. <code>Make</code>: Kiểm tra thời gian sửa file (<code>mtime timestamp</code>) xem <strong>có cần làm lại không</strong>.<br>3. <code>Cronjob</code>: Cài đặt <strong>khi nào tự động kích hoạt</strong>.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <hr />

        <h2 id="linux-1-1" tabindex="-1">TRẠM 1.1: BẢN CHẤT GNU/LINUX — KHI "CỤC MÁY" GẶP "BỘ KHUNG"</h2>
        <p><em>(Tương ứng Mục <code>01/ Introduction to GNU/Linux</code> trong Slide <code>01-linux-fundamentals.pdf</code> + Sách <em>The Linux Programming Interface</em>, Ch. 1: History and Standards, tr. 1–20)</em></p>

        <h3 id="linux-1-1-analogy">1. Bối cảnh &amp; Ẩn dụ đời thực: Chiếc xe máy Honda Wave</h3>
        <p>Hãy hình dung hệ điều hành như một chiếc xe máy Honda Wave. Nếu chỉ có một cục động cơ (<code>Linux Kernel</code> — Nhân hệ điều hành) nằm trơ trọi trên sàn để điều phối xăng nhớt và piston (<code>CPU</code>, <code>RAM</code>, ổ cứng), bạn không thể ngồi lên lái đi làm được. Ngược lại, nếu chỉ có bộ khung sườn, tay lái, bàn đạp ga, đèn còi (<code>GNU Tools</code> — Bộ công cụ người dùng) mà thiếu cục máy ở giữa, chiếc xe cũng chỉ là khối sắt đứng im.</p>

        <h3 id="linux-1-1-pain">2. Nỗi đau (Pain Point) khởi phát</h3>
        <p>Nhân vật chính của chúng ta — chiến dịch truy tìm lỗi <code>grep ERROR app.log</code> — cần lục tìm các dòng sự cố trong tệp nhật ký <code>app.log</code>. Tuy nhiên, phần cứng máy tính chỉ hiểu duy nhất ngôn ngữ máy là các chuỗi nhị phân <code>0</code> và <code>1</code> (<code>Machine Code</code>). Kế thừa di sản của hệ điều hành <code>UNIX</code> (do Ken Thompson và Dennis Ritchie khai sinh năm <code>1969</code> tại Bell Labs), vào năm <code>1983</code>, dự án <code>GNU</code> (<em>"GNU's Not Unix"</em>) của Richard Stallman đã chế tạo xong toàn bộ "khung xe" mã nguồn mở theo giấy phép <code>GPL</code> gồm trình biên dịch <code>GCC</code>, thư viện chuẩn <code>glibc</code>, vỏ dòng lệnh <code>Bash</code> và bộ lệnh cơ bản <code>Coreutils</code>, nhưng lại khuyết mất quả tim là động cơ <code>Kernel</code>. Đến năm <code>1991</code> (bản <code>Linux 0.01</code> ngày <code>17/09/1991</code>), chàng sinh viên Phần Lan Linus Torvalds viết xong cục máy <code>Linux Kernel</code> kiểm soát phần cứng xuất sắc theo chuẩn <code>POSIX</code>, nhưng một mình hạt nhân này lại không có giao diện hay công cụ để con người gõ lệnh <code>grep</code> vào.</p>

        <h3 id="linux-1-1-visuals">3. Sơ đồ Giải phẫu Cơ chế &amp; Bảng Dữ liệu thật</h3>

        ${buildVisualBlock(
          "linux-1-1a",
          "Hình 1.1A — Cú ghép lịch sử tạo nên hệ điều hành hoàn chỉnh GNU/Linux (Dự án GNU 1983 + Hạt nhân Linux 1991)",
          d["1.1a"].ascii,
          d["1.1a"].mermaid,
          "Sự kết hợp lịch sử giữa Dự án GNU của Richard Stallman (1983 — bộ khung công cụ người dùng Bash, Coreutils, GCC, glibc, Emacs/GDB) và Hạt nhân Linux của Linus Torvalds (1991 — cục máy điều phối CPU Scheduler, Memory Management, VFS/File System, Device Control) tạo nên hệ điều hành hoàn chỉnh GNU/Linux."
        )}

        ${buildVisualBlock(
          "linux-1-1b",
          "Hình 1.1B — Giải phẫu 6 Trụ cột khiến GNU/Linux thống trị thế giới Server, Cloud & Siêu máy tính",
          d["1.1b"].ascii,
          d["1.1b"].mermaid,
          "Sáu ưu điểm cốt lõi của GNU/Linux trên hạ tầng máy chủ: (1) Open Source $0 phí bản quyền cho 1.000 máy chủ; (2) Multi-user & Multi-tasking cho 50 kỹ sư SSH đồng thời; (3) Security & Stability khóa quyền user thường vs. root; (4) Granular Control ép sát tới 10% CPU và 1 GB RAM; (5) Portability chạy từ Router Wifi đến siêu máy tính; (6) Community & Ecosystem chuẩn hóa cho Data/AI."
        )}

        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Tiêu chí kỹ thuật</th>
                <th>Hệ điều hành đóng (<code>Windows</code>)</th>
                <th>Hệ điều hành mở (<code>GNU/Linux</code>)</th>
                <th>Tác động trực tiếp tới bài toán vận hành <code>app.log</code></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Bản chất Mã nguồn (<code>Source Code</code>)</strong></td>
                <td>Khóa kín như công thức Coca-Cola trong két sắt của Microsoft; cấm xem ruột gan bên trong (<code>Proprietary</code>).</td>
                <td>Công khai như công thức nấu phở trên mạng; tự do xem, sửa code và chia sẻ lại (<code>Free &amp; Open Source Software — GPLv2</code>).</td>
                <td>Hàng triệu chuyên gia toàn cầu cùng soi lỗi giúp hệ thống lưu trữ <code>app.log</code> đạt độ an toàn và ổn định cực cao.</td>
              </tr>
              <tr>
                <td><strong>Chi phí Bản quyền (<code>License Cost</code>)</strong></td>
                <td>Phải mua bản quyền thương mại trên từng máy tính / máy chủ sử dụng.</td>
                <td><code>$0</code> (Miễn phí hoàn toàn bản quyền hạt nhân và công cụ GNU).</td>
                <td>Dựng <code>1.000</code> máy chủ xử lý log phân tán không tốn <code>1</code> đồng tiền bản quyền hệ điều hành.</td>
              </tr>
              <tr>
                <td><strong>Đa người dùng (<code>Multi-user</code>) &amp; Đa nhiệm (<code>Multi-tasking</code>)</strong></td>
                <td>Ưu tiên trải nghiệm đơn người dùng trên Desktop; dễ bị treo giao diện khi quá tải tác vụ nặng kéo dài.</td>
                <td><code>50</code> lập trình viên kết nối <code>SSH</code> vào chung <code>1</code> máy chủ làm việc độc lập; chạy hàng trăm tiến trình quanh năm không cần khởi động lại.</td>
                <td>Nhiều kỹ sư có thể cùng lúc vào máy chủ chạy <code>grep ERROR app.log</code> mà không giẫm chân lên vùng nhớ của nhau.</td>
              </tr>
              <tr>
                <td><strong>Độ mịn kiểm soát tài nguyên (<code>Granular Control</code>)</strong></td>
                <td>Khó can thiệp sâu vào mức cấp phát phần cứng hạt mịn của từng tiến trình đơn lẻ.</td>
                <td>Kiểm soát chi tiết đến từng milimet tài nguyên phần cứng thông qua <code>Kernel</code> (<code>cgroups</code>, <code>namespaces</code>, <code>ulimit</code>).</td>
                <td>Có thể ra lệnh giới hạn một ứng dụng chỉ được phép dùng tối đa <code>10% CPU</code> và <code>1 GB RAM</code> để không làm treo máy chủ.</td>
              </tr>
              <tr>
                <td><strong>Tính khả chuyển (<code>Portability</code>)</strong></td>
                <td>Phụ thuộc vào cấu trúc phần cứng máy tính cá nhân / máy chủ nhất định và giao diện đồ họa đi kèm.</td>
                <td>Cực nhẹ khi tách bỏ GUI; chạy từ vi mạch cục phát Wifi, Tivi, điện thoại Android đến <code>100%</code> trong top <code>500</code> siêu máy tính thế giới.</td>
                <td>Cùng một câu lệnh <code>grep</code> có thể chạy đồng nhất trên cả thiết bị nhúng biên (<code>Edge</code>) lẫn cụm máy chủ đám mây (<code>Cloud</code>).</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3 id="linux-1-1-takeaway">4. Đúc kết Cơ học &amp; Đánh đổi (Trade-off)</h3>
        <ul>
          <li><strong>Bản chất cơ học:</strong> Gọi tắt là "Linux" chỉ mới nhắc tới cục động cơ hạt nhân bên trong; tên gọi chuẩn xác về mặt kiến trúc phải là <strong><code>GNU/Linux</code></strong> (<code>GNU</code> cung cấp vỏ giao tiếp <code>Bash</code>, thư viện <code>glibc</code> và bộ lệnh <code>Coreutils</code> bên ngoài + <code>Linux</code> cung cấp <code>Kernel</code> điều phối phần cứng bên trong).</li>
          <li><strong>Sự đánh đổi dẫn sang Trạm 1.2:</strong> Chính vì mã nguồn <code>GNU/Linux</code> hoàn toàn mở và miễn phí (<code>$0</code>), bất kỳ công ty hay cộng đồng nào cũng có thể lấy cục máy và bộ khung này về để "độ chế" thành hàng chục phiên bản khác nhau. Sự tự do tuyệt đối này sinh ra một nỗi đau mới cho người kỹ sư: <em>Giữa một rừng các bản phân phối (<code>Distro</code>), chúng ta phải đặt tệp <code>app.log</code> và chạy lệnh <code>grep</code> trên bản phân phối nào để không chọn nhầm công cụ?</em></li>
        </ul>

        <hr />

        <h2 id="linux-1-2" tabindex="-1">TRẠM 1.2: BẢN ĐỒ DISTRO (BẢN PHÂN PHỐI) — CHỌN "DÒNG XE" NÀO ĐỂ CHẠY HỆ THỐNG?</h2>
        <p><em>(Tương ứng Mục <code>01/ Introduction to GNU/Linux — Linux Distributions</code> trong Slide <code>01-linux-fundamentals.pdf</code>)</em></p>

        <h3 id="linux-1-2-analogy">1. Bối cảnh &amp; Ẩn dụ đời thực: Thương hiệu Trà sữa &amp; Các dòng xe</h3>
        <p>Nếu <code>GNU/Linux</code> là công thức cốt lõi gồm Trà + Sữa, thì các <strong><code>Distro</code></strong> (Bản phân phối — viết tắt của <em>Distribution</em>) chính là các thương hiệu như Gong Cha, Phê La, Tocotoco. Hoặc nhìn theo góc độ cơ khí: Cùng một khối động cơ <code>Linux Kernel</code>, các hãng khác nhau sẽ đóng vỏ, lắp ghế, gắn trình quản lý gói và phụ kiện riêng để tạo thành chiếc xe máy đi phố, chiếc xe bọc thép ngân hàng, hay chiếc xe chuyên dụng của đặc nhiệm.</p>

        <h3 id="linux-1-2-pain">2. Nỗi đau (Pain Point) từ trạm trước</h3>
        <p>Khi bắt tay vào dựng môi trường để quản lý hệ thống và xử lý <code>app.log</code>, kỹ sư đứng trước hàng loạt cái tên: <code>Ubuntu</code>, <code>Linux Mint</code>, <code>Debian</code>, <code>Red Hat Enterprise Linux (RHEL)</code>, <code>Kali Linux</code>, <code>Arch Linux</code>. Nếu lấy nhầm <code>Kali Linux</code> làm máy tính làm việc hằng ngày hoặc máy chủ thông thường, bạn sẽ đối mặt với một hệ thống cấu hình phức tạp vốn chỉ tối ưu cho việc dò quét lỗ hổng mạng. Ngược lại, nếu chọn <code>Arch Linux</code>, bạn sẽ mất hàng giờ tự gõ lệnh lắp ráp từng con ốc vít phần mềm từ con số <code>0</code> trước khi kịp chạy dòng lệnh đầu tiên.</p>

        <h3 id="linux-1-2-visuals">3. Sơ đồ Giải phẫu Cơ chế &amp; Bảng Dữ liệu thật</h3>

        ${buildVisualBlock(
          "linux-1-2a",
          "Hình 1.2A — Sự phân nhánh các 'Hương vị' (Distro) từ lõi GNU/Linux (Nhánh Debian vs. Doanh nghiệp RHEL vs. Tự lắp ráp Arch)",
          d["1.2a"].ascii,
          d["1.2a"].mermaid,
          "Ba nhánh tiến hóa lớn từ lõi GNU + Linux Kernel: (1) Nhánh Debian ('Nồi đồng cối đá' dùng gói .deb/apt) đẻ ra Ubuntu, Linux Mint và Kali Linux; (2) Nhánh Doanh nghiệp (Fedora/RHEL dùng gói .rpm/dnf) có bảo hành 24/7 cho ngân hàng/viễn thông; (3) Nhánh Tự lắp ráp (Arch Linux dùng pacman) cài đặt từ con số 0."
        )}

        ${buildVisualBlock(
          "linux-1-2b",
          "Hình 1.2B — Giải phẫu Cấu trúc 4 Lớp bên trong một Distro & Ba Đánh đổi khi lựa chọn Môi trường",
          d["1.2b"].ascii,
          d["1.2b"].mermaid,
          "Bốn lớp cấu thành một bản phân phối Linux (Kernel -> systemd & GNU Tools -> Package Manager apt/dnf -> GUI/CLI) và 3 đánh đổi kỹ thuật giúp chọn Ubuntu LTS làm môi trường chuẩn cho Cloud, Data Engineering và AI/ML."
        )}

        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Tiêu chí đối chiếu</th>
                <th><code>Linux Mint</code> ("Ngôi nhà ấm áp")</th>
                <th><code>Ubuntu</code> ("Xe máy quốc dân IT")</th>
                <th><code>Kali Linux</code> ("Hộp đồ nghề Hacker")</th>
                <th><code>Red Hat — RHEL</code> ("Xe bọc thép")</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Đối tượng mục tiêu</strong></td>
                <td>Người mới chuyển từ Windows sang, dân văn phòng.</td>
                <td>Sinh viên, lập trình viên, kỹ sư dữ liệu (<code>Data</code>) / <code>AI</code>.</td>
                <td>Chuyên gia an ninh mạng, thợ săn lỗ hổng bảo mật.</td>
                <td>Quản trị viên (<code>SysAdmin</code>) ngân hàng, viễn thông, tập đoàn.</td>
              </tr>
              <tr>
                <td><strong>Mục đích thiết kế</strong></td>
                <td>Lướt web, gõ văn bản, thay thế Windows hằng ngày.</td>
                <td>Học lập trình, triển khai <code>Cloud</code>, nghiên cứu công nghệ.</td>
                <td>Kiểm thử xâm nhập (<code>Penetration Testing</code>), quét mạng.</td>
                <td>Vận hành máy chủ tối quan trọng (<code>Mission-critical</code>).</td>
              </tr>
              <tr>
                <td><strong>Công cụ / Giao diện &amp; Quản lý gói</strong></td>
                <td>Giao diện <code>Cinnamon</code> (Taskbar + Start Menu giống Windows <code>7</code>/<code>10</code>), cài sẵn <code>LibreOffice</code>, <code>VLC</code>, <code>codecs</code>; gói <code>apt (.deb)</code>.</td>
                <td>Giao diện kiểu macOS (Thanh <code>Dock</code> bên hông + <code>Activities</code>); chỉ cài phần cốt lõi tối giản; gói <code>apt / dpkg (.deb)</code>.</td>
                <td>Tích hợp sẵn hàng trăm công cụ bảo mật (<code>Wireshark</code> soi gói tin, <code>Nmap</code> quét mạng...); gói <code>apt (.deb)</code>.</td>
                <td>Đa số quản trị qua màn hình dòng lệnh (<code>CLI</code>) nghiêm ngặt; trình quản lý gói <code>dnf / yum / rpm (.rpm)</code>.</td>
              </tr>
              <tr>
                <td><strong>Độ khó vận hành</strong></td>
                <td>Dễ nhất (<code>Plug-and-play</code> — cắm là chạy).</td>
                <td>Vừa phải (Dễ làm quen nhưng can thiệp sâu được).</td>
                <td>Rất khó (Cảnh báo: Không dùng cho người mới hay xài hằng ngày).</td>
                <td>Khó (Đòi hỏi kiến thức quản trị hệ thống chuyên sâu).</td>
              </tr>
              <tr>
                <td><strong>Chi phí &amp; Chu kỳ phát hành</strong></td>
                <td>Miễn phí <code>100%</code>; cập nhật rất thận trọng để ưu tiên ổn định.</td>
                <td>Miễn phí <code>100%</code>; cập nhật định kỳ <code>6 tháng/lần</code> + bản <code>LTS</code> (hỗ trợ <code>5–12 năm</code>).</td>
                <td>Miễn phí <code>100%</code>; phát triển dựa trên nền tảng <code>Debian Testing</code>.</td>
                <td>Trả phí thuê bao (<code>Subscription</code>) để nhận hỗ trợ chuyên gia <code>24/7</code>.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3 id="linux-1-2-takeaway">4. Đúc kết Cơ học &amp; Đánh đổi (Trade-off)</h3>
        <ul>
          <li><strong>Bản chất cơ học:</strong> Việc chọn <code>Distro</code> thực chất là sự đánh đổi giữa <strong>Sự tiện lợi đóng gói sẵn</strong> (<code>Linux Mint</code> cài sẵn mọi thứ văn phòng, <code>Kali</code> cài sẵn đồ nghề bảo mật), <strong>Cam kết bảo hành thương mại <code>24/7</code></strong> (<code>RHEL</code> thu phí thuê bao), và <strong>Tính cân bằng cho phát triển phần mềm</strong> (<code>Ubuntu</code> tối giản phần thừa, có bản <code>LTS</code> ổn định kèm chu kỳ <code>6 tháng</code> cập nhật công nghệ mới). Đó là lý do <code>Ubuntu</code> được chọn làm môi trường chuẩn để vận hành hệ thống trong học phần này.</li>
          <li><strong>Sự đánh đổi dẫn sang Trạm 1.3:</strong> Bây giờ máy chủ <code>Ubuntu</code> đã bật lên, tệp <code>app.log</code> đã nằm trên đĩa cứng. Bạn mở màn hình đen lên và gõ lệnh <code>grep ERROR app.log</code>. <em>Nhưng tại sao dòng chữ bạn gõ không chạy thẳng xuống ổ cứng để tìm chữ <code>ERROR</code>, mà phải đi qua tới <code>6</code> trạm kiểm soát trung gian trong "Căn bếp Linux"?</em></li>
        </ul>

        <hr />

        <h2 id="linux-1-3" tabindex="-1">TRẠM 1.3: GIẢI PHẪU "CĂN BẾP LINUX" — HÀNH TRÌNH 7 BƯỚC CỦA LỆNH grep ERROR app.log</h2>
        <p><em>(Tương ứng Mục <code>01/ Architecture of Linux OS</code> &amp; <code>03/ Command Line Basics</code> trong Slide <code>01-linux-fundamentals.pdf</code> + Sách <em>TLPI</em> Ch. 2–3, tr. 21–68 &amp; <em>OSTEP</em> Ch. 4–6: Process API <code>fork/exec/wait</code> &amp; Limited Direct Execution, tr. 25–62)</em></p>

        <h3 id="linux-1-3-analogy">1. Bối cảnh &amp; Ẩn dụ đời thực: Kỷ luật thép trong "Căn bếp Linux"</h3>
        <p>Hãy bước vào <strong>"Căn bếp Linux"</strong> (hoặc "Tòa cao ốc 3 tầng") từ bản vẽ kiến trúc cơ học:</p>
        <ul>
          <li>Bạn là thực khách đứng ở <strong>Quầy giao tiếp</strong> (<code>Terminal</code>), viết phiếu gọi món đưa cho <strong>Người nhận việc</strong> (<code>Shell</code> / <code>Bash</code>).</li>
          <li>Người nhận việc tra cứu cuốn <strong>Công thức nấu ăn</strong> (<code>Program</code> đang nằm im trên kệ sách đĩa cứng) để cử một <strong>Người đầu bếp thực thụ</strong> (<code>Process</code>) xắn tay vào làm việc.</li>
          <li>Nhưng trong căn bếp này có một kỷ luật thép (cơ chế <em>Limited Direct Execution</em> chia tách <code>User Space — Ring 3</code> và <code>Kernel Space — Ring 0</code> trên phần cứng CPU): Đầu bếp (<code>Process</code>) <strong>tuyệt đối không được tự ý</strong> mở tủ lấy <strong>Sổ ghi chép</strong> (<code>File</code>), bật <strong>Bếp lửa</strong> (<code>CPU</code>), chiếm <strong>Bàn sơ chế</strong> (<code>RAM</code>) hay gọi điện ra ngoài (<code>Network</code>). Mọi yêu cầu đụng vào tài nguyên đều phải điền vào <strong>Phiếu đăng ký</strong> (<code>System Call</code>) để trình lên vị <strong>Bếp trưởng kiêm Quản lý kho tối cao</strong> (<code>Linux Kernel</code>) xét duyệt quyền hạn!</li>
        </ul>

        <h3 id="linux-1-3-pain">2. Nỗi đau (Pain Point) từ trạm trước</h3>
        <p>Nhiều người mới học nhìn vào màn hình đen gõ <code>grep ERROR app.log</code> rồi thấy kết quả hiện ra ngay lập tức thì lầm tưởng <code>Terminal</code>, <code>Shell</code>, <code>Program</code>, <code>Process</code> và <code>Kernel</code> là một khối duy nhất. Khi lệnh bị lỗi <em>"Permission denied"</em> (Không đủ quyền đọc tệp) hoặc <em>"Command not found"</em> (Không tìm thấy lệnh), họ không biết lỗi nằm ở khâu nào: Do người nhận việc (<code>Shell</code>) không tìm thấy công thức (<code>Program</code>), do đầu bếp (<code>Process</code>) xử lý sai, hay do quản lý kho (<code>Kernel</code>) chặn cửa không cho mở sổ (<code>File</code>)?</p>

        <h3 id="linux-1-3-visuals">3. Sơ đồ Giải phẫu Cơ chế &amp; Bảng Dữ liệu thật</h3>

        ${buildVisualBlock(
          "linux-1-3a",
          "Hình 1.3A — Giải phẫu Luồng chạy Cơ bản (Basic Flow) trong 'Căn bếp Linux' đối chiếu Kiến trúc 3 Tầng",
          d["1.3a"].ascii,
          d["1.3a"].mermaid,
          "Đối chiếu Kiến trúc 3 Tầng trên Slide (User Space Ring 3 vs. Kernel Space Ring 0) với luồng cơ học 7 bước trong 'Căn bếp Linux': [1] Terminal -> [2] Shell/Bash -> [3] Program (/bin/grep) -> [4] Process -> [5] System Call -> [6] Linux Kernel -> [7] Hardware Resources (File, CPU, RAM, Network)."
        )}

        ${buildVisualBlock(
          "linux-1-3b",
          "Hình 1.3B — Phân định Ranh giới Trách nhiệm giữa Linux Kernel và Process trong Chiến dịch grep ERROR app.log",
          d["1.3b"].ascii,
          d["1.3b"].mermaid,
          "Giải phẫu 6 bước thực thi lệnh grep ERROR app.log và ranh giới cốt tử ở Bước 5: Linux Kernel chỉ làm nhiệm vụ thủ kho mở tệp app.log và nạp khối byte lên RAM theo đúng quyền (Kernel không hề biết chữ ERROR là gì), còn việc dùng CPU dò từng dòng tìm chuỗi ERROR là trách nhiệm của Process grep."
        )}

        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Thực thể kỹ thuật</th>
                <th>Hình ảnh trong "Căn bếp"</th>
                <th>Trạng thái vật lý</th>
                <th>Vai trò chính xác khi chạy <code>grep ERROR app.log</code></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong><code>Terminal</code> / <code>CLI</code></strong></td>
                <td>Quầy giao tiếp &amp; Cuốn sổ gọi món.</td>
                <td>Giao diện văn bản hiển thị trên màn hình.</td>
                <td>Nhận dòng chữ <code>grep ERROR app.log</code> từ bàn phím chuyển cho <code>Shell</code> và in kết quả trả về.</td>
              </tr>
              <tr>
                <td><strong><code>Shell</code> (<code>Bash</code> / <code>zsh</code> / <code>sh</code>)</strong></td>
                <td>Người nhận việc / Thông dịch viên.</td>
                <td>Chương trình thông dịch (<code>Shell</code> là xe hơi nói chung; <code>Bash</code> là chiếc xe cụ thể thuộc dự án <code>GNU</code>).</td>
                <td>Đọc hiểu câu lệnh, kiểm tra cú pháp, xác định cần gọi chương trình <code>grep</code> với tham số <code>ERROR</code> và <code>app.log</code>.</td>
              </tr>
              <tr>
                <td><strong><code>Program</code></strong></td>
                <td>Công thức nấu ăn trong sách.</td>
                <td>File nhị phân (<code>0</code> và <code>1</code>, chuẩn <code>ELF</code> tại <code>/bin/grep</code>) nằm tĩnh trên ổ cứng, chưa chiếm <code>CPU</code>/<code>RAM</code>.</td>
                <td>Mô tả thuật toán tìm kiếm chuỗi ký tự của <code>grep</code>, nhưng chưa có người vào nhận việc để làm.</td>
              </tr>
              <tr>
                <td><strong><code>Process</code></strong></td>
                <td>Người đầu bếp đang nấu theo công thức.</td>
                <td>Thực thể động đang chạy trên <code>RAM</code> và được cấp lượt <code>CPU</code> (sinh ra qua cặp lệnh <code>fork() + execve()</code>).</td>
                <td>Trực tiếp nhận dữ liệu từ <code>Kernel</code> và thực hiện thuật toán so khớp tìm dòng chứa chữ <code>ERROR</code>.</td>
              </tr>
              <tr>
                <td><strong><code>System Call</code></strong></td>
                <td>Phiếu đăng ký xin dùng tài nguyên.</td>
                <td>Giao diện yêu cầu đặc quyền (<code>open()</code>, <code>read()</code>, <code>write()</code>) giữa <code>Process</code> và <code>Kernel</code>.</td>
                <td>Tờ đơn <code>Process</code> (<code>grep</code>) nộp lên để xin phép mở và đọc nội dung tệp <code>app.log</code>.</td>
              </tr>
              <tr>
                <td><strong><code>Linux Kernel</code></strong></td>
                <td>Bếp trưởng tối cao / Quản lý kho.</td>
                <td>Lõi hạt nhân chạy ở <code>Ring 0</code> kiểm soát <code>100%</code> phần cứng (<code>File</code>, <code>CPU</code>, <code>RAM</code>, <code>Network</code>).</td>
                <td>Kiểm tra đường dẫn <code>app.log</code>, xét duyệt quyền truy cập và đọc dữ liệu từ ổ cứng giao cho <code>Process</code>.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3 id="linux-1-3-takeaway">4. Đúc kết Cơ học &amp; Đánh đổi (Trade-off)</h3>
        <ul>
          <li><strong>Bản chất cơ học:</strong> Quy tắc vàng trong thiết kế của Linux là <strong>Sự phân tách quyền lực tuyệt đối</strong>. <code>Kernel</code> không hề biết chữ <code>ERROR</code> là gì — <code>Kernel</code> chỉ làm đúng nhiệm vụ của người thủ kho: kiểm tra quyền và trao dữ liệu tệp <code>app.log</code> cho <code>Process</code>; còn việc tìm chữ <code>ERROR</code> là công việc lao động trí óc của riêng <code>Process</code> (<code>grep</code>).</li>
          <li><strong>Sự đánh đổi &amp; Câu hỏi dẫn sang Chặng 2:</strong> Thiết kế qua trạm kiểm soát <code>System Call</code> giúp hệ thống đạt độ bảo mật tối đa, không một chương trình nào có thể tự ý phá hỏng máy chủ. Nhưng hãy nhìn kỹ vào khoảnh khắc <code>Process</code> (<code>grep</code>) cầm tờ phiếu <code>System Call</code> đứng trước mặt <code>Kernel</code>:
            <ol>
              <li>Một <code>Process</code> phải mang theo <strong>"Bộ hồ sơ căn cước" gồm 5 thông tin gì</strong> trên người để <code>Kernel</code> biết nó là ai, của người dùng nào, đang đứng ở đâu mà xét duyệt?</li>
              <li>Tại sao trong Linux, từ cuốn sổ <code>app.log</code>, cái ổ cứng <code>/dev/sda</code>, cho đến chính anh đầu bếp <code>Process</code> đang chạy đều bị biến thành <strong><code>File</code></strong> (<code>"Everything is a file"</code>), và chúng được sắp xếp như thế nào trên <strong>Cây thư mục <code>/</code> duy nhất</strong>?</li>
            </ol>
          </li>
        </ul>

        <section class="summary-section" id="linux-1-summary" tabindex="-1">
          <h2>TÓM TẮT BỎ TÚI CHẶNG 1 (MẠCH NHÂN – QUẢ &amp; CHECKLIST 5 CÂU HỎI BẢN CHẤT)</h2>
          <ol>
            <li><strong>Tại sao gọi chuẩn phải là <code>GNU/Linux</code>?</strong> Vì <code>Linux</code> (Linus Torvalds, <code>1991</code>) thực chất chỉ là cục máy hạt nhân (<code>Kernel</code>) điều khiển phần cứng; phải ghép với bộ khung công cụ người dùng của dự án <code>GNU</code> (Richard Stallman, <code>1983</code>: <code>Bash</code>, <code>Coreutils</code>, <code>GCC</code>, <code>glibc</code>) mới tạo thành hệ điều hành hoàn chỉnh.</li>
            <li><strong>Tại sao <code>GNU/Linux</code> thống trị tuyệt đối thế giới Server &amp; Cloud?</strong> Nhờ 6 trụ cột: (1) Mã nguồn mở miễn phí <code>$0</code> bản quyền cho cả <code>1.000</code> máy chủ; (2) Đa người dùng (<code>50 dev</code> SSH cùng lúc) &amp; Đa nhiệm bền bỉ quanh năm; (3) Bảo mật phân quyền <code>user</code> thường vs. <code>root</code>; (4) Kiểm soát hạt mịn ép sát tới <code>10% CPU</code> &amp; <code>1 GB RAM</code>; (5) Nhẹ và khả chuyển mọi phần cứng; (6) Hệ sinh thái gói phần mềm chuẩn hóa.</li>
            <li><strong>Giữa rừng <code>Distro</code>, tại sao chọn <code>Ubuntu</code>?</strong> <code>Linux Mint</code> tối ưu cho dân văn phòng chuyển từ Windows; <code>Kali Linux</code> là hộp đồ nghề chuyên biệt cho PenTest; <code>RHEL</code> là xe bọc thép thu phí thuê bao <code>24/7</code> cho ngân hàng; còn <code>Ubuntu</code> (nhánh <code>Debian</code>, gói <code>apt/.deb</code>) cân bằng hoàn hảo giữa độ ổn định (<code>LTS 5–12 năm</code>) và chu cập nhật công nghệ mới (<code>6 tháng/lần</code>) cho Data/Cloud/AI.</li>
            <li><strong>Phân biệt <code>Shell</code> vs. <code>Bash</code> và <code>Program</code> vs. <code>Process</code> như thế nào?</strong> <code>Shell</code> là khái niệm trình thông dịch nói chung ("xe hơi"), còn <code>Bash</code> là chương trình Shell cụ thể thuộc dự án GNU ("xe Mec/BMW"). <code>Program</code> là tệp nhị phân tĩnh nằm im trên đĩa cứng (<code>/bin/grep</code> — công thức nấu ăn), còn <code>Process</code> là thực thể sống đang chiếm <code>RAM</code> và <code>CPU</code> để thực thi công thức đó (người đầu bếp).</li>
            <li><strong>Ai thực sự tìm chữ <code>ERROR</code> trong <code>grep ERROR app.log</code> — <code>Kernel</code> hay <code>Process</code>?</strong> <code>Linux Kernel</code> hoàn toàn không biết chữ <code>ERROR</code> là gì! Khi nhận phiếu <code>System Call</code> (<code>open</code>, <code>read</code>), <code>Kernel</code> chỉ kiểm tra đường dẫn và quyền hạn rồi đọc khối byte của <code>app.log</code> từ đĩa cứng nạp lên <code>RAM</code>; còn việc dùng <code>CPU</code> dò từng dòng để lọc ra chữ <code>ERROR</code> là trách nhiệm của <code>Process</code> (<code>grep</code>).</li>
          </ol>
          <p style="margin-top:14px;"><strong>Bước tiếp theo:</strong> Chuyển sang <a href="#topic=F01&stage=2" onclick="selectStorageStage(2);return false;">Chặng 2: Giải phẫu Căn cước Process, Triết lý "Everything is a file" &amp; Cây thư mục / ➔</a></p>
        </section>
      </div>
    `;
  }

  function renderLinuxChang2() {
    const d = HUB_DATA.linux_diagrams;
    return `
      <div class="prose">
        <p>Ở <strong>Chặng 1</strong>, lệnh <code>grep ERROR /var/log/app.log</code> đã được <code>Shell (Bash)</code> đánh thức từ tệp nhị phân tĩnh <code>/bin/grep</code> trên ổ cứng thành một <code>Process</code> sống động trên <code>RAM/CPU</code> và trình tờ phiếu <code>System Call</code> lên <code>Linux Kernel</code>. Bước sang <strong>Chặng 2 (Trạm 2.1 ➔ 2.4)</strong>, chúng ta giải phẫu câu hỏi: <em>Giữa hàng trăm Process của 50 người dùng cùng chạy đồng thời, dựa vào "chứng minh thư" nào mà Kernel quyết định cho phép hay từ chối mở tệp <code>/var/log/app.log</code>? Tại sao trong mắt Linux mọi thứ từ văn bản, thư mục, ổ cứng đến CPU đều là File nằm trên một cây thư mục gốc <code>/</code> duy nhất, và bộ lệnh CLI nào giúp kỹ sư tác chiến trên cây thư mục đó?</em></p>

        ${buildVisualBlock(
          "linux-2-map",
          "Hình 2.0 — Bản đồ Kiến trúc Chặng 2: Căn cước Process (task_struct), Inode/VFS & Cây Thư mục Gốc /",
          d["0.2"].ascii,
          d["0.2"].mermaid,
          "Tổng quan 4 trạm của Chặng 2 trên Bản đồ Cơ học Linux: [2.1] Hồ sơ căn cước Process & rwx -> [2.2] Everything is a File & Inode -> [2.3] Cây thư mục hợp nhất / -> [2.4] Bộ công cụ CLI điều hướng & săn log."
        )}

        <hr />

        <h2 id="linux-2-1" tabindex="-1">TRẠM 2.1: GIẢI PHẪU HỒ SƠ CĂN CƯỚC CỦA MỘT PROCESS (PID, USER/GROUP, WORKING DIRECTORY, ENVIRONMENT, OPEN FILES)</h2>
        <p><em>(Tương ứng Mục <code>01/ Introduction to GNU/Linux</code> &amp; <code>03/ Command Line Basics — Shell &amp; Permissions</code> trong Slide <code>01-linux-fundamentals.pdf</code> tr. 26, 28 + Sách <em>The Linux Programming Interface</em>, Ch. 6: Processes, Ch. 8–9: Users, Groups &amp; Process Credentials, tr. 113–184)</em></p>

        <h3 id="linux-2-1-analogy">1. Bối cảnh &amp; Ẩn dụ đời thực: Thẻ căn cước của "Người đầu bếp"</h3>
        <p>Hãy quay lại <strong>"Căn bếp Linux"</strong> ở khoảnh khắc anh đầu bếp <code>Process (grep)</code> cầm tờ phiếu <code>System Call (open)</code> đứng trước quầy của vị Bếp trưởng <code>Linux Kernel</code> để xin mở cuốn sổ <code>/var/log/app.log</code>. Trong một nhà hàng có <code>50</code> đầu bếp cùng làm việc một lúc, Bếp trưởng không bao giờ giao chìa khóa kho cho một người vô danh. Mỗi <code>Process</code> ngay từ giây phút chào đời qua cặp lệnh <code>fork() + execve()</code> đều bị <code>Kernel</code> gắn chặt một <strong>"Bộ hồ sơ căn cước" (<code>task_struct</code>) gồm 5 thuộc tính bất di bất dịch</strong> đeo trước ngực.</p>

        <h3 id="linux-2-1-pain">2. Nỗi đau (Pain Point) từ trạm trước</h3>
        <p>Khi bạn gõ một dòng lệnh ngắn gọn <code>grep ERROR app.log</code> vào Terminal, có 3 câu hỏi sống còn mà nếu không hiểu cơ chế căn cước của <code>Process</code>, kỹ sư sẽ hoàn toàn mù mờ khi hệ thống báo lỗi:</p>
        <ul>
          <li><strong>(1) Làm sao Shell tìm thấy công cụ <code>grep</code>?</strong> Bạn chỉ gõ chữ <code>grep</code> chứ không hề gõ đường dẫn đầy đủ <code>/bin/grep</code>. Tại sao <code>Shell</code> biết phải tìm ở đâu, còn khi bạn tự viết một công cụ riêng thì gõ tên lại bị báo lỗi <em>"Command not found"</em>?</li>
          <li><strong>(2) Làm sao Process hiểu đường dẫn ngắn <code>app.log</code>?</strong> Trên máy chủ có hàng chục tệp tên là <code>app.log</code> ở các thư mục khác nhau; dựa vào đâu mà tiến trình <code>grep</code> biết chính xác bạn đang nói tới tệp nào?</li>
          <li><strong>(3) Tại sao người này đọc được <code>app.log</code> còn người kia bị chặn?</strong> Khi gặp lỗi <em>"Permission denied"</em>, làm sao đọc vị chính xác bức tường phân quyền 10 ký tự <code>-rw-r-----</code> của Linux để xử lý tận gốc thay vì gõ bừa <code>chmod 777</code> gây thủng bảo mật?</li>
        </ul>

        <h3 id="linux-2-1-visuals">3. Sơ đồ Giải phẫu Cơ chế &amp; Bảng Dữ liệu thật</h3>

        ${buildVisualBlock(
          "linux-2-1a",
          "Hình 2.1A — Quy trình 3 Bước của Shell (Slide 26) & Giải phẫu 5 Thuộc tính Căn cước trong Hồ sơ Process (task_struct)",
          d["2.1a"].ascii,
          d["2.1a"].mermaid,
          "Quy trình 3 bước của Shell trên Slide 26 (1. Parse & Expand -> 2. Search $PATH -> 3. Translate to System Calls fork/execve) và 5 thuộc tính căn cước gắn chặt vào mỗi Process đang chạy: PID/PPID, User/Group (UID/GID), Working Directory (cwd), Environment ($PATH), và Open Files (File Descriptors 0, 1, 2, 3)."
        )}

        ${buildVisualBlock(
          "linux-2-1b",
          "Hình 2.1B — Giải mã Chuỗi 10 Ký tự Phân quyền ls -l (Slide 28) & Phép chiếu Quyền hạn của Linux Kernel",
          d["2.1b"].ascii,
          d["2.1b"].mermaid,
          "Giải phẫu kết quả lệnh ls -lh /var/log/app.log (-rw-r----- 1 root adm 1.5G) và thuật toán 3 bước của Linux Kernel khi đối chiếu UID/GID trên căn cước Process với bộ 3 cụm quyền User (rw-), Group (r--) và Others (---)."
        )}

        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Thuộc tính Căn cước Process</th>
                <th>Hình ảnh trong "Căn bếp"</th>
                <th>Bản chất Kỹ thuật trong <code>Linux Kernel</code></th>
                <th>Vai trò trực tiếp khi chạy <code>grep ERROR app.log</code> &amp; Lệnh kiểm tra</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>1. <code>PID</code> &amp; <code>PPID</code></strong><br><em>(Process ID)</em></td>
                <td>Mã số thẻ nhân viên &amp; Mã số người quản lý trực tiếp.</td>
                <td>Số nguyên duy nhất định danh tiến trình đang sống trên RAM (<code>PID 1</code> luôn là <code>systemd</code>; <code>PPID</code> là PID của tiến trình cha <code>Bash</code> đã <code>fork()</code> ra nó).</td>
                <td>Giúp <code>Kernel</code> quản lý vòng đời, cấp phát <code>CPU/RAM</code> hoặc tiêu diệt đúng tiến trình bị treo (<code>ps aux | grep grep</code>, <code>kill -9 &lt;PID&gt;</code>).</td>
              </tr>
              <tr>
                <td><strong>2. <code>User / Group</code></strong><br><em>(<code>UID</code> &amp; <code>GID</code>)</em></td>
                <td>Họ tên chủ nhân &amp; Phòng ban trực thuộc.</td>
                <td>Định danh số của người dùng chạy lệnh (<code>root</code> luôn có <code>UID = 0</code>; người dùng thường <code>UID &gt;= 1000</code>) và các nhóm quyền (<code>adm</code>, <code>sudo</code>, <code>docker</code>).</td>
                <td><code>Kernel</code> đem <code>UID/GID</code> của <code>grep</code> so với quyền <code>rwx</code> trên tệp <code>/var/log/app.log</code> để quyết định mở kho hay trả về lỗi <code>EACCES (Permission denied)</code>. Kiểm tra bằng <code>id</code> hoặc <code>whoami</code>.</td>
              </tr>
              <tr>
                <td><strong>3. <code>Working Directory</code></strong><br><em>(<code>cwd</code>)</em></td>
                <td>Vị trí bàn bếp nơi người đầu bếp đang đứng.</td>
                <td>Con trỏ thư mục hiện tại của tiến trình (kế thừa từ <code>Shell</code> lúc gõ lệnh, lưu tại <code>/proc/&lt;PID&gt;/cwd</code>).</td>
                <td>Gốc tọa độ để giải mã mọi <strong>đường dẫn tương đối</strong>: nếu <code>cwd = /var/log</code>, gõ <code>app.log</code> sẽ tự động được hiểu là <code>/var/log/app.log</code>. Kiểm tra bằng <code>pwd</code>.</td>
              </tr>
              <tr>
                <td><strong>4. <code>Environment</code></strong><br><em>(<code>$PATH</code>, <code>$HOME</code>)</em></td>
                <td>Cuốn sổ tay địa chỉ mang theo bên người.</td>
                <td>Danh sách các cặp <code>KEY=VALUE</code> mà tiến trình con kế thừa từ tiến trình cha (quan trọng nhất là biến <code>$PATH=/usr/local/bin:/usr/bin:/bin</code>).</td>
                <td>Nhờ <code>$PATH</code> chứa <code>/bin</code>, bạn chỉ cần gõ <code>grep</code> mà không phải gõ <code>/bin/grep</code> (Bước <code>2. SEARCH PATH</code> trên Slide 26). Kiểm tra bằng <code>echo $PATH</code>, <code>which grep</code>.</td>
              </tr>
              <tr>
                <td><strong>5. <code>Open Files</code></strong><br><em>(Bảng <code>FD Table</code>)</em></td>
                <td>Danh sách các cuốn sổ &amp; đường ống đang cầm trên tay.</td>
                <td>Bảng chỉ mục các tệp/luồng mà tiến trình đang mở (mặc định mở sẵn <code>0 = stdin</code>, <code>1 = stdout</code>, <code>2 = stderr</code>; tệp <code>app.log</code> mở thêm sẽ nhận <code>FD = 3</code>).</td>
                <td>Cầu nối trực tiếp để <code>grep</code> đọc từng khối byte từ <code>FD 3 (app.log)</code> và đẩy kết quả ra <code>FD 1 (stdout)</code> hoặc đẩy lỗi ra <code>FD 2 (stderr)</code>. Kiểm tra bằng <code>ls -l /proc/&lt;PID&gt;/fd</code>.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3 id="linux-2-1-takeaway">4. Đúc kết Cơ học &amp; Đánh đổi (Trade-off)</h3>
        <ul>
          <li><strong>Bản chất cơ học:</strong> Một <code>Process</code> không bao giờ tồn tại lơ lửng; nó luôn mang theo 5 thuộc tính căn cước (<code>PID</code>, <code>UID/GID</code>, <code>Working Directory</code>, <code>Environment</code>, <code>Open Files</code>) kế thừa từ tiến trình cha (<code>Bash</code>). Khi <code>grep</code> xin mở <code>app.log</code>, <code>Kernel</code> đối chiếu tuần tự <code>UID ➔ GID ➔ Others</code> với 9 bit quyền <code>rwx</code> (<code>r=4, w=2, x=1</code>) trên tệp: khớp ở cấp nào là chốt ngay ở cấp đó.</li>
          <li><strong>Sự đánh đổi dẫn sang Trạm 2.2:</strong> Cơ chế kiểm tra căn cước <code>UID/GID</code> đối chiếu với quyền <code>rwx</code> của <code>File</code> chặt chẽ và đơn giản đến mức các nhà thiết kế UNIX/Linux đã nảy ra một ý tưởng táo bạo: <em>Thay vì thiết kế thêm hàng chục cơ chế bảo mật và giao diện lập trình khác nhau cho ổ đĩa cứng, cổng USB, card mạng hay vùng nhớ tiến trình, tại sao không biến TẤT CẢ mọi thứ trong máy tính thành <code>File</code>?</em></li>
        </ul>

        <hr />

        <h2 id="linux-2-2" tabindex="-1">TRẠM 2.2: TRIẾT LÝ "EVERYTHING IS A FILE" (REGULAR FILE, DIRECTORY, DEVICE /dev/sda, PROCESS /proc/1234) &amp; CƠ HỌC INODE</h2>
        <p><em>(Tương ứng Mục <code>01/ The Linux File System Hierarchy — "Everything is a file"</code> trong Slide <code>01-linux-fundamentals.pdf</code> tr. 19, 31–37 + Sách <em>TLPI</em> Ch. 4, 14–15, 18 &amp; <em>OSTEP</em> Ch. 39–40: Files, Directories &amp; Inodes, tr. 467–502)</em></p>

        <h3 id="linux-2-2-analogy">1. Bối cảnh &amp; Ẩn dụ đời thực: Chuẩn "Ổ cắm điện 2 chấu" toàn hệ thống</h3>
        <p>Hãy tưởng tượng nếu trong nhà bạn, quạt máy đòi ổ cắm 2 lỗ tròn, tủ lạnh đòi ổ cắm 3 chấu dẹt, còn đèn bàn lại bắt nối dây đồng trực tiếp vào cầu dao tổng — bạn sẽ phát điên vì mỗi thiết bị đòi một kiểu đấu nối riêng. Triết lý cốt lõi nhất làm nên vẻ đẹp vĩnh cửu của UNIX và GNU/Linux chính là <strong><code>"Everything is a file"</code> (Mọi thứ đều là File)</strong>: từ tệp nhật ký <code>app.log</code>, thư mục <code>/var/log</code>, ổ đĩa cứng vật lý <code>/dev/sda</code>, thiết bị USB <code>/dev/usb0</code> cho đến chính tiến trình đang chạy trên RAM <code>/proc/1234</code> đều được ngụy trang thành một chuẩn "ổ cắm" duy nhất mang tên <strong><code>File</code></strong> (luồng byte đọc/ghi tuần tự).</p>

        <h3 id="linux-2-2-pain">2. Nỗi đau (Pain Point) từ trạm trước</h3>
        <p>Nếu không có triết lý <code>"Everything is a file"</code>, người kỹ sư sẽ vấp phải 2 nỗi thống khổ lớn:</p>
        <ul>
          <li><strong>(1) Phân mảnh công cụ:</strong> Bạn sẽ phải dùng một phần mềm riêng để đọc văn bản, một phần mềm khác để xem dung lượng <code>RAM/CPU</code>, và một bộ API hoàn toàn khác để đọc dữ liệu thô từ ổ cứng <code>SSD</code>.</li>
          <li><strong>(2) Hiểu sai bản chất của Thư mục (<code>Directory</code>), Đổi tên (<code>mv</code>) và Xóa tệp (<code>rm</code>):</strong> Nhiều người tưởng "Thư mục" là cái hộp vật lý nhốt tệp bên trong, nên không hiểu tại sao đổi tên hay di chuyển một tệp <code>app.log</code> nặng <code>50 GB</code> bằng lệnh <code>mv</code> lại hoàn tất trong <code>0,001 giây</code>, hay tại sao lệnh <code>rm</code> trên Linux lại xóa vĩnh viễn không có Thùng rác (<code>Recycle Bin</code>).</li>
        </ul>

        <h3 id="linux-2-2-visuals">3. Sơ đồ Giải phẫu Cơ chế &amp; Bảng Dữ liệu thật</h3>

        ${buildVisualBlock(
          "linux-2-2a",
          "Hình 2.2A — Triết lý 'Everything is a file' (Slide 19): Tầng VFS biến 4 Thực thể thành Giao diện Đọc/Ghi Đồng nhất",
          d["2.2a"].ascii,
          d["2.2a"].mermaid,
          "Bốn nhóm thực thể trên Slide 19 (Regular files, Directories, Device interfaces /dev/sda & /dev/usb0, Processes /proc/1234) đi qua tầng Virtual File System (VFS) của Kernel để dùng chung một bộ System Call (open/read/write/close) và dùng chung một bộ lệnh CLI (cat, grep, cp, echo)."
        )}

        ${buildVisualBlock(
          "linux-2-2b",
          "Hình 2.2B — Giải phẫu 'Fun Fact' Slide 19 (Thư mục chỉ là File chứa Tên -> Inode) & Cơ học Đằng sau cp, mv, rm",
          d["2.2b"].ascii,
          d["2.2b"].mermaid,
          "Giải thích cơ học cho 'Fun fact: A directory is just a file containing the names of other files' (Slide 19): Thư mục chỉ là bảng ánh xạ Tên hiển thị -> Số Inode. Nhờ đó lệnh mv cùng ổ đĩa chỉ sửa tên trong bảng (0 byte copy), còn lệnh rm tháo liên kết (unlink) khỏi bảng thư mục khiến tệp biến mất vĩnh viễn không qua Recycle Bin."
        )}

        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Phân loại File trong Linux (Slide 19)</th>
                <th>Ký hiệu <code>ls -l</code> &amp; Ví dụ thực tế</th>
                <th>Bản chất Vật lý Bên dưới (<code>Inode</code> / <code>VFS</code>)</th>
                <th>Ứng dụng Thực chiến với Bộ lệnh Đồng nhất (<code>cat</code>, <code>grep</code>, <code>cp</code>)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>1. Tệp thông thường</strong><br>(<code>Regular Files</code>)</td>
                <td>Ký tự đầu: <code>-</code><br>VD: <code>/var/log/app.log</code>, <code>document.txt</code>, <code>image.png</code>, <code>script.sh</code></td>
                <td>Chứa chuỗi byte dữ liệu thực sự (văn bản ASCII/UTF-8, ảnh PNG, mã máy nhị phân ELF) nằm trên các khối (<code>Data Blocks</code>) của ổ cứng SSD/HDD.</td>
                <td>Dùng <code>grep ERROR /var/log/app.log</code> để lọc dòng lỗi, <code>cat</code>/<code>head</code>/<code>tail</code> để xem nội dung, <code>cp</code> để sao lưu.</td>
              </tr>
              <tr>
                <td><strong>2. Thư mục</strong><br>(<code>Directories</code>)</td>
                <td>Ký tự đầu: <code>d</code><br>VD: <code>/var/log</code>, <code>/home/fsds</code>, <code>/etc</code></td>
                <td><strong>Fun Fact (Slide 19):</strong> Thư mục thực chất chỉ là một <em>tệp đặc biệt</em> chứa bảng danh bạ ánh xạ <code>Tên tệp (Filename) ➔ Mã số Inode</code> (metadata thật của tệp nằm ở <code>Inode</code>).</td>
                <td>Đổi tên tệp <code>100 GB</code> bằng <code>mv app.log old.log</code> chỉ sửa 1 dòng chữ trong tệp thư mục nên mất <code>&lt; 1 ms</code>; xóa bằng <code>rm</code> là gỡ dòng ánh xạ (<code>unlink</code>).</td>
              </tr>
              <tr>
                <td><strong>3. Giao diện Thiết bị</strong><br>(<code>Device Interfaces</code>)</td>
                <td>Ký tự đầu: <code>b</code> (Block) / <code>c</code> (Char)<br>VD: <code>/dev/sda</code> (ổ cứng), <code>/dev/usb0</code> (USB), <code>/dev/null</code> (hố đen)</td>
                <td>Không chiếm dung lượng dữ liệu trên đĩa; là "cổng đại diện" nối thẳng vào trình điều khiển phần cứng (<code>Device Driver</code>) bên trong <code>Kernel</code>.</td>
                <td>Sao lưu nguyên ổ cứng bằng <code>cp /dev/sda1 disk.img</code>, hoặc vứt bỏ toàn bộ thông báo rác vào "hố đen" bằng <code>grep ERROR app.log 2&gt; /dev/null</code>.</td>
              </tr>
              <tr>
                <td><strong>4. Hồ sơ Tiến trình &amp; Hệ thống</strong><br>(<code>Processes</code>)</td>
                <td>Nằm trong <code>/proc</code><br>VD: <code>/proc/1234</code>, <code>/proc/meminfo</code>, <code>/proc/cpuinfo</code></td>
                <td>Tệp ảo (<code>Virtual Files</code>) sinh trực tiếp từ cấu trúc dữ liệu trên <code>RAM</code> của <code>Kernel</code> ngay lúc bạn đọc (chiếm <code>0 byte</code> ổ cứng).</td>
                <td>Không cần cài phần mềm theo dõi: chỉ cần gõ <code>cat /proc/meminfo</code>, <code>cat /proc/cpuinfo</code> hoặc <code>cat /proc/uptime</code> là đọc ngay thông số máy chủ!</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3 id="linux-2-2-takeaway">4. Đúc kết Cơ học &amp; Đánh đổi (Trade-off)</h3>
        <ul>
          <li><strong>Bản chất cơ học:</strong> Triết lý <code>"Everything is a file"</code> kết hợp với cấu trúc <code>Directory ➔ Inode ➔ Data Blocks</code> giúp Linux biến mọi tài nguyên phức tạp thành các dòng chảy byte đơn giản. Bạn chỉ cần học một bộ công cụ duy nhất (<code>cat</code>, <code>grep</code>, <code>echo</code>, <code>cp</code>) là điều khiển được cả tệp log, tiến trình lẫn thiết bị phần cứng.</li>
          <li><strong>Sự đánh đổi dẫn sang Trạm 2.3:</strong> Khi cả triệu thực thể từ chương trình hệ thống, tệp cấu hình, thiết bị phần cứng, tiến trình trên RAM cho tới nhật ký <code>app.log</code> đều biến thành <code>File</code>, nếu vứt chung vào một đống thì hệ thống sẽ hỗn loạn. <em>Linux đã quy hoạch "Bản đồ kho hàng" (Cây thư mục <code>/</code>) thành các phân khu chức năng như thế nào, và tại sao thiết kế 1 gốc <code>/</code> duy nhất lại ưu việt hơn hẳn kiểu chia ổ đĩa <code>C:\\</code>, <code>D:\\</code> của Windows?</em></li>
        </ul>

        <hr />

        <h2 id="linux-2-3" tabindex="-1">TRẠM 2.3: BẢN ĐỒ KHO HÀNG — CÂY THƯ MỤC DUY NHẤT / (/bin, /sbin, /usr, /etc, /home, /root, /var/log, /tmp, /proc) &amp; ĐỐI CHIẾU WINDOWS</h2>
        <p><em>(Tương ứng Mục <code>01/ The Linux File System Hierarchy — System, User &amp; Temporary Folders</code> trong Slide <code>01-linux-fundamentals.pdf</code> tr. 20–22, 29–30 + Sách <em>TLPI</em> Ch. 12: The <code>/proc</code> File System, tr. 223–232; Ch. 18: Directories and Links, tr. 339–374)</em></p>

        <h3 id="linux-2-3-analogy">1. Bối cảnh &amp; Ẩn dụ đời thực: "Đại siêu thị 1 Cửa chính <code>/</code>" vs. "Khu chợ nhiều Ki-ốt <code>C:\\</code>, <code>D:\\</code>"</h3>
        <p>Trên Windows, mỗi khi bạn cắm thêm một ổ cứng hay một chiếc USB, hệ thống lại đẻ ra một gốc cây mới (<code>C:\\</code>, <code>D:\\</code>, <code>E:\\</code>) giống như các ki-ốt tách biệt ngoài chợ. Ngược lại, Linux quy hoạch toàn bộ hệ thống như một <strong>Đại siêu thị chỉ có duy nhất một Cửa chính là thư mục gốc <code>/</code> (<code>Root Folder</code>)</strong>. Bất kỳ ổ cứng vật lý mới nào lắp thêm vào máy chủ đều được gắn (<code>mount</code>) thành một gian hàng con nằm bên dưới mái nhà chung <code>/</code> này.</p>

        <h3 id="linux-2-3-pain">2. Nỗi đau (Pain Point) từ trạm trước</h3>
        <p>Hãy hình dung ứng dụng của bạn đang ghi nhật ký vào đường dẫn <code>D:\\Logs\\app.log</code> trên Windows. Sáu tháng sau, ổ cứng <code>D:\\</code> bị đầy; quản trị viên lắp thêm ổ cứng mới <code>E:\\</code> và chuyển thư mục log sang <code>E:\\Logs\\app.log</code>. Ngay lập tức, hàng chục kịch bản quét lỗi và ứng dụng đang trỏ cố định vào chữ <code>D:\\</code> bị gãy vụn! Hơn nữa, nếu một kỹ sư mới đăng nhập vào máy chủ Linux mà không nắm được quy hoạch chuẩn của cây thư mục <code>/</code>, họ sẽ không biết công cụ <code>grep</code> cất ở kệ nào, tệp cấu hình <code>SSH</code> nằm ở đâu, và tại sao thư mục <code>/proc</code> báo dung lượng khả dụng nhưng không chiếm một byte ổ cứng nào.</p>

        <h3 id="linux-2-3-visuals">3. Sơ đồ Giải phẫu Cơ chế &amp; Bảng Dữ liệu thật</h3>

        ${buildVisualBlock(
          "linux-2-3a",
          "Hình 2.3A — Bản đồ Cây Thư mục Hợp nhất / (Slide 20–22): Phân khu User Folders, System Folders & Temporary/Variable Folders",
          d["2.3a"].ascii,
          d["2.3a"].mermaid,
          "Cấu trúc cây thư mục Linux bắt đầu từ gốc / (Slide 20–22) chia làm 3 phân khu rõ rệt: (1) Khu nhà ở User (/home/fsds, /root); (2) Khu Hệ thống (/bin, /sbin, /usr/bin, /usr/local, /etc, và /proc ảo 0 MB đĩa); (3) Khu Tạm & Biến đổi liên tục (/tmp tự xóa khi reboot, và /var/log nơi chứa tệp app.log)."
        )}

        ${buildVisualBlock(
          "linux-2-3b",
          "Hình 2.3B — Đối chiếu Kiến trúc Đa gốc Windows (C:\\, D:\\) vs. Cây Hợp nhất Linux (/) & Đường dẫn Tuyệt đối vs. Tương đối",
          d["2.3b"].ascii,
          d["2.3b"].mermaid,
          "Sự khác biệt cơ học giữa mô hình chia ổ đĩa vật lý C:\\, D:\\ của Windows với cơ chế gắn kết (Mount Point) vào cây thư mục / duy nhất của Linux, cùng nguyên tắc phân biệt Đường dẫn Tuyệt đối (bắt đầu bằng /) và Đường dẫn Tương đối (tính từ Working Directory hiện tại)."
        )}

        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Nhóm &amp; Thư mục trên Cây <code>/</code></th>
                <th>Ý nghĩa &amp; Vai trò trong "Kho hàng Linux" (Slide 20–22)</th>
                <th>Tệp / Lệnh Tiêu biểu Thực tế</th>
                <th>Đối chiếu với <code>Windows</code> &amp; Lưu ý Vận hành</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong><code>/bin</code></strong><br><em>(Essential User Binaries)</em></td>
                <td>Kệ chứa các công cụ nhị phân thiết yếu nhất cho mọi người dùng; bắt buộc phải có để khởi động (<code>boot</code>) và cứu hộ hệ thống.</td>
                <td><code>/bin/ls</code>, <code>/bin/cp</code>, <code>/bin/mv</code>, <code>/bin/rm</code>, <code>/bin/cat</code>, <strong><code>/bin/grep</code></strong>, <code>/bin/bash</code></td>
                <td>Tương đương các lệnh lõi trong <code>C:\\Windows\\System32</code>. Nơi cất giữ "công thức" của nhân vật chính <code>grep</code>!</td>
              </tr>
              <tr>
                <td><strong><code>/sbin</code></strong><br><em>(System Binaries)</em></td>
                <td>Kệ chứa các lệnh quản trị hệ thống nguy hiểm; mặc định chỉ quản trị viên tối cao (<code>root</code>) mới được phép chạy.</td>
                <td><code>/sbin/reboot</code>, <code>/sbin/shutdown</code>, <code>/sbin/fdisk</code>, <code>/sbin/iptables</code></td>
                <td>Tách biệt khỏi <code>/bin</code> để ngăn người dùng thường vô tình tắt máy chủ hoặc format nhầm ổ cứng.</td>
              </tr>
              <tr>
                <td><strong><code>/usr</code></strong><br><em>(User Programs &amp; Data)</em></td>
                <td>Kho phần mềm và thư viện dùng chung cho toàn bộ người dùng trên máy chủ.</td>
                <td>• <code>/usr/bin</code>: <code>python</code>, <code>git</code>, <code>gcc</code>, <code>ssh</code><br>• <code>/usr/local/bin</code>: Phần mềm do dev tự biên dịch/cài thêm</td>
                <td>Tương đương <code>C:\\Program Files</code> trên Windows. Trên Ubuntu đời mới, <code>/bin</code> được nối tắt (<code>symlink</code>) vào <code>/usr/bin</code>.</td>
              </tr>
              <tr>
                <td><strong><code>/etc</code></strong><br><em>(Configuration Files)</em></td>
                <td>Phòng chứa toàn bộ "sổ tay cấu hình" dạng văn bản của hệ điều hành và các dịch vụ máy chủ.</td>
                <td>• <code>/etc/passwd</code> (Danh sách tài khoản)<br>• <code>/etc/hosts</code> (Cấu hình tên miền cục bộ)<br>• <code>/etc/ssh/sshd_config</code> (Cấu hình SSH)</td>
                <td>Thay thế cho <code>Windows Registry</code> phức tạp: trên Linux, mọi cấu hình hệ thống đều là tệp văn bản thuần túy đọc/sửa được bằng <code>vim</code>/<code>nano</code>!</td>
              </tr>
              <tr>
                <td><strong><code>/proc</code></strong><br><em>(Process &amp; System Info)</em></td>
                <td><strong>Cửa kính ảo (Virtual Filesystem)</strong> do <code>Kernel</code> tạo trực tiếp trên <code>RAM</code> để phơi bày trạng thái thời gian thực của <code>Process</code> và phần cứng.</td>
                <td>• <code>/proc/meminfo</code> (Dung lượng RAM)<br>• <code>/proc/cpuinfo</code> (Thông số CPU)<br>• <code>/proc/uptime</code> &amp; <code>/proc/1234/</code></td>
                <td><strong>Đặc tính sống còn:</strong> Chiếm đúng <strong><code>0 MB</code> trên ổ đĩa cứng</strong>! Khi tắt nguồn máy chủ, toàn bộ <code>/proc</code> biến mất và được <code>Kernel</code> dựng lại khi bật máy.</td>
              </tr>
              <tr>
                <td><strong><code>/home</code></strong> &amp; <strong><code>/root</code></strong><br><em>(User &amp; Admin Homes)</em></td>
                <td>• <code>/home</code>: Khu căn hộ riêng của từng người dùng thường.<br>• <code>/root</code>: Phủ riêng của quản trị viên tối cao <code>root</code>.</td>
                <td>• <code>/home/fsds</code>, <code>/home/student1</code>, <code>/home/developer</code><br>• <code>/root</code> (Nằm tách hẳn khỏi <code>/home</code>)</td>
                <td><code>/home</code> giống <code>C:\\Users</code>. <code>/root</code> được đặt ngay dưới <code>/</code> để nếu ổ đĩa chứa <code>/home</code> bị hỏng, <code>root</code> vẫn đăng nhập vào cứu máy được.</td>
              </tr>
              <tr>
                <td><strong><code>/tmp</code></strong><br><em>(Temporary Files)</em></td>
                <td>Bàn nháp công cộng: bất kỳ người dùng hay chương trình nào cũng được phép tạo tệp tạm tại đây.</td>
                <td>Tệp tải dở của trình duyệt, socket tạm, tệp nháp khi chạy <code>crontab -e</code> (<code>/tmp/crontab.SpK7AW</code>)</td>
                <td>Tương đương <code>C:\\Temp</code>. <strong>Cảnh báo:</strong> Dữ liệu trong <code>/tmp</code> sẽ bị <strong>xóa sạch tự động mỗi khi khởi động lại máy (Reboot)</strong>!</td>
              </tr>
              <tr>
                <td><strong><code>/var</code></strong><br><em>(Variable Data)</em></td>
                <td>Kho chứa dữ liệu <strong>phình to và biến đổi liên tục</strong> trong suốt quá trình máy chủ vận hành 24/7.</td>
                <td>• <strong><code>/var/log</code></strong>: Nhật ký hệ thống &amp; <strong><code>app.log</code></strong><br>• <code>/var/www</code>: Mã nguồn Web (Nginx/Apache)<br>• <code>/var/lib</code>: Dữ liệu Database (PostgreSQL/Docker)</td>
                <td>Đây chính là "quê hương" của tệp mục tiêu <code>/var/log/app.log</code>. Khi ổ cứng máy chủ báo đầy <code>100%</code>, thủ phạm số 1 luôn nằm ở <code>/var/log</code>!</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3 id="linux-2-3-takeaway">4. Đúc kết Cơ học &amp; Đánh đổi (Trade-off)</h3>
        <ul>
          <li><strong>Bản chất cơ học:</strong> Việc quy hoạch toàn bộ hệ thống dưới một gốc <code>/</code> duy nhất cho phép Linux tách rời hoàn toàn <strong>Đường dẫn logic trong code</strong> khỏi <strong>Ổ đĩa vật lý bên dưới</strong>. Nếu thư mục <code>/var/log</code> bị tệp <code>app.log</code> làm đầy, quản trị viên chỉ cần cắm thêm một ổ cứng <code>NVMe 10 TB</code> mới và gắn (<code>mount</code>) nó vào đúng nhánh <code>/var/log</code> — mọi kịch bản đang gọi <code>/var/log/app.log</code> vẫn chạy mượt mà không phải sửa một dòng code nào!</li>
          <li><strong>Sự đánh đổi dẫn sang Trạm 2.4:</strong> Đã nắm trọn bản đồ kho hàng <code>/</code> trong tay, nhưng khi đăng nhập vào máy chủ qua <code>SSH</code>, trước mặt bạn chỉ có con trỏ nhấp nháy trên màn hình đen. <em>Làm sao di chuyển thần tốc giữa các thư mục, tạo/sao chép/đổi tên/xóa tệp an toàn, và soi đúng những dòng lỗi mới nhất trong tệp <code>/var/log/app.log</code> nặng hàng Gigabyte mà không làm treo máy chủ?</em></li>
        </ul>

        <hr />

        <h2 id="linux-2-4" tabindex="-1">TRẠM 2.4: BỘ CÔNG CỤ TÁC CHIẾN TRÊN CÂY THƯ MỤC — ĐIỀU HƯỚNG (pwd/ls/cd), THAO TÁC (cp/mv/rm) &amp; SĂN LOG (head/tail -f/find/du)</h2>
        <p><em>(Tương ứng Mục <code>03/ Command Line Basics — Navigate, Manipulate, View &amp; Search Files</code> trong Slide <code>01-linux-fundamentals.pdf</code> tr. 27–44 + Sách <em>The Linux Programming Interface</em>, Ch. 18)</em></p>

        <h3 id="linux-2-4-analogy">1. Bối cảnh &amp; Ẩn dụ đời thực: Bộ đồ nghề tác chiến trong đêm</h3>
        <p>Nếu cây thư mục <code>/</code> là một tòa kho khổng lồ không bật đèn (vì trên Server không có giao diện chuột <code>GUI</code>), thì bộ lệnh <strong><code>Command Line Basics</code></strong> chính là chiếc la bàn định vị (<code>pwd</code>, <code>ls</code>, <code>cd</code>), đôi găng tay bốc xếp hàng hóa (<code>touch</code>, <code>mkdir</code>, <code>cp</code>, <code>mv</code>, <code>rm</code>) và chiếc đèn pin chiếu điểm (<code>head</code>, <code>tail -f</code>, <code>find</code>, <code>du</code>) giúp kỹ sư thao tác chính xác tới từng tệp log trong tích tắc.</p>

        <h3 id="linux-2-4-pain">2. Nỗi đau (Pain Point) từ trạm trước</h3>
        <p>Trong thực tế vận hành máy chủ sản xuất (<code>Production Server</code>), kỹ sư mới thường mắc 3 sai lầm chí mạng khi thao tác với tệp trên dòng lệnh:</p>
        <ul>
          <li><strong>(1) Quên kiểm tra vị trí đứng trước khi xóa:</strong> Chạy lệnh xóa đệ quy <code>rm -rf</code> khi đang đứng nhầm thư mục. Vì trên Linux CLI <strong>không hề có Thùng rác (<code>Recycle Bin</code>)</strong>, một cú gõ <code>rm -rf /</code> hoặc <code>rm -rf *</code> sẽ xóa sổ toàn bộ dữ liệu ngay lập tức không thể cứu vãn!</li>
          <li><strong>(2) Dùng <code>cat</code> mở tệp log khổng lồ:</strong> Khi tệp <code>/var/log/app.log</code> đã phình lên <code>5 GB</code>, nếu gõ <code>cat /var/log/app.log</code>, hệ thống sẽ cố gắng đổ cả trăm triệu dòng chữ ra màn hình Terminal, làm nghẽn băng thông <code>SSH</code> và treo cứng phiên làm việc.</li>
          <li><strong>(3) Máy chủ báo hết ổ cứng (<code>Disk Full 100%</code>) lúc nửa đêm:</strong> Giữa hàng vạn thư mục trên cây <code>/</code>, nếu chỉ đi gõ <code>ls</code> từng thư mục thì mất cả tiếng đồng hồ vẫn không tìm ra tệp <code>.log</code> nào đang ngốn hết ổ cứng.</li>
        </ul>

        <h3 id="linux-2-4-visuals">3. Sơ đồ Giải phẫu Cơ chế &amp; Bảng Dữ liệu thật</h3>

        ${buildVisualBlock(
          "linux-2-4a",
          "Hình 2.4A — Bản đồ Tác chiến Nhóm Lệnh Điều hướng (pwd, ls, cd — Slide 28–30) & Nhóm Thao tác File (touch, mkdir, cp, mv, rm — Slide 31–37)",
          d["2.4a"].ascii,
          d["2.4a"].mermaid,
          "Tổng hợp cơ học 2 nhóm lệnh nền tảng trên Slide 28–37: Nhóm Điều hướng (pwd định vị, ls -lh/-a/-t quan sát, cd ~/../- di chuyển) và Nhóm Thao tác (touch tạo file rỗng, mkdir -p tạo cây thư mục, cp -r sao chép, mv đổi tên/di chuyển, và rm -r xóa vĩnh viễn)."
        )}

        ${buildVisualBlock(
          "linux-2-4b",
          "Hình 2.4B — Chiến thuật Soi File Log Lớn (head vs. cat vs. tail -f — Slide 38–40) & Bộ Tứ Săn Lùng (du, find, sed, man — Slide 41–44)",
          d["2.4b"].ascii,
          d["2.4b"].mermaid,
          "Chiến thuật đọc tệp /var/log/app.log theo đúng mục tiêu: head -n 20 lấy 20 dòng đầu, cat chỉ dùng khi ghép/đọc file nhỏ, tail -f theo dõi dòng lỗi mới bắn ra theo thời gian thực (Real-time), kết hợp du -sh * và find -size +1G để truy lùng tệp ngốn ổ đĩa."
        )}

        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Nhóm Tác vụ (Slide 27)</th>
                <th>Lệnh &amp; Cú pháp Chuẩn trên Slide</th>
                <th>Cơ chế Hoạt động &amp; Các Cờ (<code>Flags</code>) Quan trọng</th>
                <th>Kinh nghiệm Xương máu khi Vận hành <code>/var/log/app.log</code></th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>1. Điều hướng cây thư mục</strong><br>(<code>Navigate</code> — Slide 28–30)</td>
                <td>• <code>pwd</code><br>• <code>ls -lh</code>, <code>ls -a</code>, <code>ls -t</code><br>• <code>cd ~</code>, <code>cd ..</code>, <code>cd -</code>, <code>cd /</code></td>
                <td>• <code>pwd</code>: In đường dẫn tuyệt đối đang đứng.<br>• <code>ls -l</code> (chi tiết), <code>-h</code> (đơn vị <code>K/M/G</code>), <code>-a</code> (hiện file ẩn <code>.bashrc</code>), <code>-t</code> (xếp theo thời gian mới nhất).<br>• <code>cd ..</code> (lên cha), <code>cd -</code> (quay lại thư mục vừa đứng trước đó).</td>
                <td>Luôn gõ <code>ls -lht /var/log</code> để thấy ngay tệp log nào vừa mới bị ghi đè ở dòng đầu tiên kèm dung lượng thực tế (<code>MB/GB</code>).</td>
              </tr>
              <tr>
                <td><strong>2. Tạo &amp; Sao chép</strong><br>(<code>Create &amp; Copy</code> — Slide 31–34)</td>
                <td>• <code>touch folder1/newfile.txt</code><br>• <code>mkdir -p project/src/components/</code><br>• <code>cp file.txt backup.txt</code><br>• <code>cp -r folder2 folder1/folder1.3</code></td>
                <td>• <code>touch</code>: Tạo tệp rỗng mới (hoặc cập nhật <code>timestamp</code> nếu tệp đã tồn tại).<br>• <code>mkdir -p</code>: Tự động tạo luôn các thư mục cha nếu chưa có (không có <code>-p</code> sẽ báo lỗi).<br>• <code>cp -r</code>: Sao chép đệ quy toàn bộ thư mục và các tệp con bên trong.</td>
                <td>Trước khi sửa tệp cấu hình <code>/etc/ssh/sshd_config</code> hay cắt gọt <code>app.log</code>, luôn chạy <code>cp app.log app.log.bak</code> để có đường lùi.</td>
              </tr>
              <tr>
                <td><strong>3. Di chuyển, Đổi tên &amp; Xóa</strong><br>(<code>Move &amp; Remove</code> — Slide 35–37)</td>
                <td>• <code>mv old.txt new.txt</code> (Đổi tên)<br>• <code>mv file.txt /path/dest/</code> (Chuyển)<br>• <code>rm file.txt</code><br>• <code>rm -r folder4</code></td>
                <td>• <code>mv</code> có 2 công dụng: Cùng thư mục = <strong>Đổi tên (<code>RENAME</code>)</strong>; Khác thư mục = <strong>Di chuyển (<code>MOVE</code>)</strong>.<br>• <code>rm</code>: Xóa tệp; <code>rm -r</code>: Xóa cả thư mục và toàn bộ nội dung bên trong.</td>
                <td><strong>CẢNH BÁO ĐỎ (Slide 37):</strong> <code>rm</code> xóa vĩnh viễn không có <code>Recycle Bin</code>! Tuyệt đối cấm chạy <code>rm -rf /</code> (xóa sạch toàn bộ hệ điều hành).</td>
              </tr>
              <tr>
                <td><strong>4. Xem &amp; Theo dõi Log</strong><br>(<code>View Files</code> — Slide 38–40)</td>
                <td>• <code>cat file1.txt &gt; new.txt</code><br>• <code>head -n 20 file3.txt</code><br>• <code>tail -n 20 file3.txt</code><br>• <strong><code>tail -f log.txt</code></strong></td>
                <td>• <code>cat</code>: Đọc toàn bộ tệp hoặc nối nhiều tệp (<code>cat f1 f2 &gt; merge.txt</code>).<br>• <code>head</code> / <code>tail</code>: Mặc định lấy <code>10</code> dòng đầu / cuối (dùng <code>-n 20</code> để lấy <code>20</code> dòng).<br>• <code>tail -f</code>: Giữ luồng mở để xem dòng mới ghi thêm theo <strong>thời gian thực (<code>REAL-TIME</code>)</strong>.</td>
                <td>Không bao giờ dùng <code>cat</code> cho tệp log hàng GB! Hãy dùng <code>tail -n 100 /var/log/app.log</code> hoặc <code>tail -f /var/log/app.log</code> để bắt sống lỗi vừa nổ ra.</td>
              </tr>
              <tr>
                <td><strong>5. Săn lùng &amp; Tra cứu</strong><br>(<code>Search &amp; Manual</code> — Slide 41–44)</td>
                <td>• <code>find / -type f -size +1G</code><br>• <code>du -sh *</code><br>• <code>sed 's/unix/linux/g' file.txt</code><br>• <code>man ls</code> / <code>clear</code></td>
                <td>• <code>find . -name "*.log" -size +1G</code>: Truy tìm mọi tệp <code>.log</code> nặng trên <code>1 GB</code>.<br>• <code>du -sh *</code>: Tóm tắt tổng dung lượng từng thư mục con hiện tại.<br>• <code>sed 's/A/B/g'</code>: Thay thế toàn bộ chuỗi <code>A</code> thành <code>B</code>.<br>• <code>man &lt;lệnh&gt;</code>: Mở sách hướng dẫn chính hãng tích hợp sẵn (bấm <code>q</code> để thoát).</td>
                <td>Khi ổ đĩa báo đầy <code>100%</code>: Chạy ngay cặp bài trùng <code>du -sh /var/log/*</code> và <code>find /var/log -name "*.log" -size +1G</code> để tóm gọn thủ phạm trong 3 giây!</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3 id="linux-2-4-takeaway">4. Đúc kết Cơ học &amp; Đánh đổi (Trade-off)</h3>
        <ul>
          <li><strong>Bản chất cơ học:</strong> Mỗi công cụ dòng lệnh trên Linux (<code>ls</code>, <code>head</code>, <code>tail</code>, <code>grep</code>, <code>find</code>, <code>du</code>, <code>sed</code>, <code>wc</code>) đều được thiết kế theo triết lý UNIX: <strong>"Mỗi chương trình chỉ làm duy nhất 1 việc và làm thật xuất sắc" (<em>Do one thing and do it well</em> — Slide 45)</strong>.</li>
          <li><strong>Sự đánh đổi &amp; Câu hỏi dẫn sang Chặng 3:</strong> Giả sử bạn đã dùng <code>grep ERROR /var/log/app.log</code> để lọc ra được <code>50.000</code> dòng lỗi, nhưng bây giờ sếp yêu cầu: <em>"Hãy cắt lấy cột tên dịch vụ bị lỗi, sắp xếp theo thứ tự A–Z, đếm xem lỗi nào xuất hiện nhiều nhất và ghi báo cáo ra tệp, đồng thời nếu có lỗi đọc tệp thì tách riêng ra chỗ khác!"</em> Một mình lệnh <code>grep</code> không thể làm hết ngần ấy việc. Làm thế nào để các <code>Process</code> độc lập chuyền tay nhau luồng dữ liệu ngay trên <code>RAM</code> qua 3 cổng <code>stdin (0)</code>, <code>stdout (1)</code>, <code>stderr (2)</code> và đường ống <code>Pipe (|)</code> mà không làm bẩn kết quả của nhau? Đó chính là nội dung của <strong>Chặng 3</strong>!</li>
        </ul>

        <section class="summary-section" id="linux-2-summary" tabindex="-1">
          <h2>TÓM TẮT BỎ TÚI CHẶNG 2 (MẠCH NHÂN – QUẢ &amp; CHECKLIST 5 CÂU HỎI BẢN CHẤT)</h2>
          <ol>
            <li><strong>5 thuộc tính trên "chứng minh thư" của một <code>Process</code> là gì và dùng để làm gì?</strong> <code>PID</code> (định danh tiến trình), <code>User/Group (UID/GID)</code> (xét duyệt quyền chạm vào tệp <code>rwx</code>), <code>Working Directory (cwd)</code> (gốc tọa độ giải mã đường dẫn tương đối), <code>Environment ($PATH)</code> (danh bạ giúp <code>Shell</code> tìm thấy <code>/bin/grep</code> khi chỉ gõ <code>grep</code>), và <code>Open Files (FD 0, 1, 2...)</code>.</li>
            <li><strong>Triết lý <code>"Everything is a file"</code> (Slide 19) mang lại sức mạnh cơ học gì?</strong> Nhờ tầng <code>Virtual File System (VFS)</code>, cả tệp văn bản (<code>app.log</code>), thư mục (<code>/var/log</code>), thiết bị phần cứng (<code>/dev/sda</code>) lẫn thông tin tiến trình trên RAM (<code>/proc/1234</code>) đều dùng chung một giao diện đọc/ghi byte và thao tác được bằng cùng một bộ lệnh (<code>cat</code>, <code>grep</code>, <code>cp</code>, <code>echo</code>).</li>
            <li><strong>Tại sao lệnh <code>mv</code> đổi tên tệp <code>100 GB</code> lại mất chưa tới <code>1 ms</code>, và tại sao <code>rm</code> xóa không khôi phục được?</strong> Vì thư mục thực chất chỉ là một tệp đặc biệt chứa bảng ánh xạ <code>Tên tệp ➔ Số Inode</code> (Slide 19). Đổi tên bằng <code>mv</code> chỉ sửa dòng chữ trong bảng thư mục (không chạm vào <code>100 GB</code> dữ liệu trên đĩa), còn <code>rm</code> tháo liên kết (<code>unlink</code>) khỏi bảng thư mục ngay lập tức mà không đi qua <code>Recycle Bin</code>.</li>
            <li><strong>Tại sao thư mục <code>/proc</code> chiếm <code>0 MB</code> ổ cứng, và tại sao cây thư mục <code>/</code> của Linux ưu việt hơn <code>C:\\</code>, <code>D:\\</code> của Windows?</strong> <code>/proc</code> là hệ thống tệp ảo do <code>Kernel</code> sinh trực tiếp trên <code>RAM</code> (như <code>/proc/meminfo</code>, <code>/proc/cpuinfo</code>). Cây thư mục hợp nhất <code>/</code> cho phép gắn (<code>mount</code>) ổ đĩa mới vào bất kỳ nhánh nào (như <code>/var/log</code>) mà không làm đứt gãy đường dẫn <code>/var/log/app.log</code> trong code.</li>
            <li><strong>Khi tệp <code>/var/log/app.log</code> phình lên <code>5 GB</code> làm đầy ổ đĩa, bộ lệnh tác chiến chuẩn là gì?</strong> Tuyệt đối không dùng <code>cat</code>; dùng <code>du -sh /var/log/*</code> và <code>find /var/log -name "*.log" -size +1G</code> để định vị tệp khổng lồ, dùng <code>head -n 20</code> / <code>tail -n 20</code> để cắt đầu/đuôi, và dùng <code>tail -f /var/log/app.log</code> để theo dõi dòng lỗi mới theo thời gian thực (<code>Real-time</code>).</li>
          </ol>
          <p style="margin-top:14px;"><strong>Bước tiếp theo:</strong> Chuyển sang <a href="#topic=F01&stage=3" onclick="selectStorageStage(3);return false;">Chặng 3: Giao tiếp Đa tiến trình (IPC), Ba Cổng 0/1/2 &amp; Đường ống Pipe ➔</a></p>
        </section>
      </div>
    `;
  }

  function renderLinuxChang3() {
    const d = HUB_DATA.linux_diagrams;
    return `
      <div class="prose">
        <p>Ở <strong>Chặng 2</strong>, tiến trình <code>grep</code> đã xuất trình căn cước hợp lệ để mở tệp <code>/var/log/app.log</code> trên cây thư mục <code>/</code> và lọc ra hàng nghìn dòng chứa chữ <code>ERROR</code>. Bước sang <strong>Chặng 3 (Trạm 3.1 ➔ 3.2)</strong>, chúng ta giải quyết bài toán phối hợp dây chuyền giữa nhiều tiến trình: <em>Làm thế nào để truyền ngay luồng kết quả của <code>grep</code> sang cho tiến trình kế tiếp xử lý ngay trên bộ nhớ RAM thông qua 3 cổng tiêu chuẩn (<code>stdin: 0</code>, <code>stdout: 1</code>, <code>stderr: 2</code>) và đường ống <code>Pipe (|)</code>, đồng thời điều hướng dòng chảy (<code>&gt;&gt;</code> và <code>2&gt;&amp;1</code>) để chặn đứng "bẫy mù lỗi" khi hệ thống chạy ngầm lúc nửa đêm?</em></p>

        ${buildVisualBlock(
          "linux-3-map",
          "Hình 3.0 — Vị trí của Chặng 3 trên Bản đồ Cơ học Linux (Ba Cổng 0/1/2, Đường ống Pipe & Điều hướng I/O)",
          d["0.2"].ascii,
          d["0.2"].mermaid,
          "Khung tham chiếu Chặng 3 trên Bản đồ Cơ học Linux: Cơ chế 3 cổng tiêu chuẩn stdin (0), stdout (1), stderr (2), đường ống Pipe trong bộ đệm RAM của Kernel và các toán tử điều hướng luồng (>, >>, 2>, 2>&1)."
        )}

        <h2 id="linux-3-1" tabindex="-1">TRẠM 3.1: BA CỔNG TIÊU CHUẨN (0, 1, 2) &amp; ĐƯỜNG ỐNG PIPE TRONG KERNEL</h2>

        <h3>1. Bối cảnh &amp; Ẩn dụ đời thực</h3>
        <p>Hãy hình dung mỗi anh đầu bếp <code>Process</code> (Tiến trình đang chạy) khi đứng vào dây chuyền chế biến trong "Căn bếp Linux" đều được thiết kế sẵn đúng <strong>3 cửa giao nhận hàng độc lập</strong> (trong bảng <code>File Descriptor Table</code> của tiến trình — Sách <em>The Linux Programming Interface</em>, Ch. 4 &amp; <em>CS:APP</em>, Ch. 10):</p>
        <ul>
          <li><strong>1 cửa nhập nguyên liệu đầu vào</strong> (<code>stdin</code> — <em>Standard Input</em>, mang số hiệu <code>0</code>).</li>
          <li><strong>1 cửa xuất món ăn đạt chuẩn ra ngoài</strong> (<code>stdout</code> — <em>Standard Output</em>, mang số hiệu <code>1</code>).</li>
          <li><strong>1 cửa thoát hiểm chuyên dùng để báo cáo sự cố/hỏng hóc</strong> (<code>stderr</code> — <em>Standard Error</em>, mang số hiệu <code>2</code>).</li>
        </ul>
        <p>Khi cần kết hợp nhiều đầu bếp làm việc nối tiếp nhau, người điều phối <code>Shell</code> (Trình thông dịch) sẽ lắp một đường ống dẫn kín (<code>Pipe</code> — ký hiệu <code>|</code>) nối thẳng từ cửa xuất thành phẩm (<code>stdout: 1</code>) của anh đứng trước sang cửa nhập nguyên liệu (<code>stdin: 0</code>) của anh đứng sau.</p>

        <h3>2. Nỗi đau (Pain Point) từ trạm trước</h3>
        <p>Ở Chặng 2, anh đầu bếp <code>grep</code> đã lọc ra được hàng nghìn dòng chứa chữ <code>ERROR</code> từ file <code>/var/log/app.log</code>. Nhưng trong thực tế, một <code>Process</code> đơn lẻ chỉ làm tốt đúng phần việc riêng của nó. Nếu bạn muốn đem kết quả của <code>grep</code> chuyển sang cho một <code>Process</code> thứ hai (như <code>wc -l</code> để đếm tổng số dòng lỗi hoặc <code>sort | uniq -c</code> để thống kê tần suất) mà phải ghi tạm ra ổ cứng rồi đọc lại thì rất rườm rà và tốn <code>Disk I/O</code>. Nguy hiểm hơn: Nếu trong lúc đang lọc dữ liệu mà <code>Process</code> thứ nhất gặp lỗi (ví dụ: đụng phải một file bị khóa quyền đọc báo <em>Permission denied</em>), dòng chữ thông báo lỗi đó nếu đi chung đường với kết quả bình thường sẽ làm "bẩn" nguyên liệu đầu vào của <code>Process</code> thứ hai!</p>

        <h3>3. Sơ đồ Giải phẫu Cơ chế &amp; Bảng Dữ liệu thật</h3>

        <h4>Sơ đồ 3.1A: Giải phẫu 3 Cổng Tiêu chuẩn (stdin, stdout, stderr) của một Process</h4>
        ${buildVisualBlock(
          "linux-3-1a",
          "Sơ đồ 3.1A — Cấu trúc 3 Cổng Giao tiếp Mặc định của Mọi Process (stdin: 0, stdout: 1, stderr: 2)",
          d["3.1a"].ascii,
          d["3.1a"].mermaid,
          "Mọi Process đang chạy đều nhận dữ liệu qua Cổng 0 (stdin), đẩy kết quả bình thường qua Cổng 1 (stdout) và xả thông báo lỗi qua Cổng 2 (stderr) theo một đường riêng biệt, không bao giờ trộn lẫn vào Cổng 1."
        )}

        <h4>Sơ đồ 3.1B: Cơ chế Phối hợp Đa tiến trình qua Đường ống Pipe giữa Shell và Kernel</h4>
        ${buildVisualBlock(
          "linux-3-1b",
          "Sơ đồ 3.1B — Phân vai Cơ học khi Nối Nhiều Process: Shell Đấu nối Cổng — Kernel Giữ Đường Pipe trên RAM",
          d["3.1b"].ascii,
          d["3.1b"].mermaid,
          "Shell đóng vai trò thợ lắp ống nối cổng stdout (1) của Process 1 vào cổng stdin (0) của Process 2; Linux Kernel giữ đường ống Pipe (bộ đệm 64 KB trên RAM) truyền từng byte dữ liệu, trong khi stderr (2) đi đường riêng."
        )}

        <h4>Bảng 3.1: Đặt lên bàn cân 3 Cổng Tiêu chuẩn &amp; Phân vai Trách nhiệm trong Hệ thống</h4>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Tên Cổng</th>
                <th>Số hiệu (<code>File Descriptor</code>)</th>
                <th>Nhiệm vụ Cơ học</th>
                <th>Vai trò của <code>Process</code>, <code>Shell</code> và <code>Kernel</code> khi phối hợp</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong><code>stdin</code></strong><br><em>(Standard Input)</em></td>
                <td><strong><code>0</code></strong></td>
                <td>Nhận dữ liệu đầu vào để xử lý.</td>
                <td><strong><code>Process</code></strong>: Chỉ tập trung đọc dữ liệu từ cổng <code>0</code> và làm việc riêng của nó, không cần biết dữ liệu đến từ bàn phím, từ file hay từ <code>Process</code> khác.</td>
              </tr>
              <tr>
                <td><strong><code>stdout</code></strong><br><em>(Standard Output)</em></td>
                <td><strong><code>1</code></strong></td>
                <td>Gửi kết quả xử lý bình thường ra ngoài.</td>
                <td><strong><code>Shell</code></strong>: Đóng vai trò thợ lắp ống, nối cổng <code>stdout (1)</code> của <code>Process</code> trước vào cổng <code>stdin (0)</code> của <code>Process</code> sau.<br><br><strong><code>Kernel</code></strong>: Giữ đường ống <code>Pipe</code> trên bộ nhớ <code>RAM</code> (mặc định <code>64 KB</code> ring buffer — <em>TLPI</em> Ch. 44) để truyền dòng <code>byte</code> giữa hai tiến trình mà không chạm ổ cứng.</td>
              </tr>
              <tr>
                <td><strong><code>stderr</code></strong><br><em>(Standard Error)</em></td>
                <td><strong><code>2</code></strong></td>
                <td>Gửi các thông báo lỗi phát sinh ra ngoài.</td>
                <td><strong><code>stderr</code></strong>: Đi theo một đường riêng biệt (không bị đẩy tự động vào ống <code>Pipe |</code>) để các dòng chữ báo lỗi không bị trộn lẫn vào kết quả dữ liệu sạch ở cổng <code>stdout (1)</code>.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3>4. Đúc kết Cơ học &amp; Đánh đổi (Trade-off)</h3>
        <ul>
          <li><strong>Bản chất cơ học:</strong> Sự ưu việt của Linux nằm ở chỗ: Mỗi <code>Process</code> hoàn toàn "mù" về sự tồn tại của các <code>Process</code> khác — nó chỉ biết hút dữ liệu từ cổng <code>0</code> (<code>stdin</code>), đẩy kết quả ra cổng <code>1</code> (<code>stdout</code>) và xả lỗi ra cổng <code>2</code> (<code>stderr</code>). Việc đấu nối dây chuyền là việc của <code>Shell</code>, còn việc giữ đường ống <code>Pipe</code> truyền từng <code>byte</code> dữ liệu an toàn trên <code>RAM</code> là việc của <code>Kernel</code>.</li>
          <li><strong>Sự đánh đổi dẫn sang Trạm 3.2:</strong> Khi bạn ngồi trực tiếp trước màn hình <code>Terminal</code>, cả cổng <code>1</code> (<code>stdout</code>) và cổng <code>2</code> (<code>stderr</code>) đều in chữ lên màn hình cho mắt bạn nhìn thấy. Nhưng chuyện gì xảy ra khi tập lệnh của bạn chạy ngầm vào lúc nửa đêm (không hề có màn hình <code>Terminal</code> nào mở sẵn): Các dòng kết quả và dòng báo lỗi đỏ lòm ở cổng <code>1</code> và cổng <code>2</code> sẽ bị ném đi đâu?</li>
        </ul>

        <h2 id="linux-3-2" tabindex="-1">TRẠM 3.2: ĐIỀU HƯỚNG DÒNG CHẢY (&gt;&gt; VÀ 2&gt;&amp;1) — CHẶN ĐỨNG "BẪY MÙ LỖI" KHI CHẠY NGẦM</h2>

        <h3>1. Bối cảnh &amp; Ẩn dụ đời thực</h3>
        <p>Khi bạn trực tiếp đứng ở quầy giao tiếp (<code>Terminal</code>), nhân viên bếp làm xong món ăn (<code>stdout: 1</code>) hay làm cháy chảo báo động (<code>stderr: 2</code>) đều hô to lên ngay trước mặt bạn. Nhưng khi bạn giao việc cho hệ thống tự chạy ngầm lúc <code>3:00</code> sáng trong lúc bạn đang ngủ, không có ai đứng ở quầy giao tiếp cả. Nếu bạn không lắp sẵn một <strong>ống dẫn phụ để gom cả biên bản làm việc (<code>1</code>) lẫn biên bản sự cố (<code>2</code>) ghi nối đuôi vào một cuốn sổ nhật ký</strong>, mọi thông báo lỗi sẽ bị ném thẳng vào sọt rác vô hình!</p>

        <h3>2. Nỗi đau (Pain Point) từ trạm trước</h3>
        <p>Rất nhiều người mới học gặp tình huống: Chạy thử lệnh bằng tay trên màn hình <code>Terminal</code> thì thấy lỗi đỏ lòm để sửa ngay, nhưng khi cài cho máy tự chạy ngầm thì chương trình chết im lặng. Vì tiến trình chạy ngầm không có màn hình hiển thị, mọi thông báo lỗi bắn ra từ cổng <code>stderr (2)</code> đều biến mất không dấu vết, khiến kỹ sư sáng hôm sau mở máy lên không tài nào biết được đêm qua hệ thống thất bại vì lý do gì.</p>

        <h3>3. Sơ đồ Giải phẫu Cơ chế &amp; Bảng Dữ liệu thật</h3>

        <h4>Sơ đồ 3.2A: Giải phẫu Cơ học Cú pháp Điều hướng <code>&gt;&gt; /var/log/backup.log 2&gt;&amp;1</code></h4>
        ${buildVisualBlock(
          "linux-3-2a",
          "Sơ đồ 3.2A — So sánh Trạng thái Dòng chảy: Chạy Ngầm Mặc định (Mù Lỗi) vs. Điều hướng Thu gom Log (2>&1)",
          d["3.2a"].ascii,
          d["3.2a"].mermaid,
          "Khi chạy ngầm không điều hướng, cả stdout (1) lẫn stderr (2) đều mất dấu vết vì không có màn hình Terminal; khi thêm >> /var/log/backup.log 2>&1, cổng 1 ghi nối đuôi vào file log và cổng 2 được bẻ chập chung vào cổng 1."
        )}

        <h4>Sơ đồ 3.2B: Ma trận Toán tử Điều hướng I/O (<code>&gt;</code>, <code>&gt;&gt;</code>, <code>&lt;</code>, <code>&lt;&lt; EOF</code>, <code>2&gt;</code>, <code>2&gt;&amp;1</code> — Slide 55 &amp; TLPI Ch. 5.5)</h4>
        ${buildVisualBlock(
          "linux-3-2b",
          "Sơ đồ 3.2B — Toàn cảnh Các Toán tử Điều hướng I/O trên Linux & Cạm bẫy Thứ tự Gộp Cổng 2>&1",
          d["3.2b"].ascii,
          d["3.2b"].mermaid,
          "Tổng hợp 6 toán tử điều hướng từ Slide 55 (>, >>, <, << EOF, 2>, 2>&1) và cơ chế lời gọi hệ thống dup2(): Tại sao bắt buộc phải viết >> app.log 2>&1 theo thứ tự từ trái sang phải."
        )}

        <h4>Bảng 3.2: Giải mã Từng Mảnh ghép Cơ học trong Lệnh Điều hướng &amp; Hệ thống Toán tử I/O</h4>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Thành phần Cú pháp</th>
                <th>Ý nghĩa Cơ học trong Hệ thống</th>
                <th>Tác dụng Thực tế khi Vận hành</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong><code>&gt; /var/log/backup.log</code></strong><br><em>(Overwrite Output — Slide 55)</em></td>
                <td>Hướng cổng kết quả bình thường (<code>stdout: 1</code>) ghi <strong>đè mới từ đầu</strong> vào file <code>/var/log/backup.log</code> (cờ <code>O_TRUNC</code>).</td>
                <td>Chỉ dùng khi muốn tạo báo cáo mới tinh mỗi lần chạy; <strong>cẩn thận</strong> vì nó sẽ xóa sạch toàn bộ lịch sử log của các ngày trước!</td>
              </tr>
              <tr>
                <td><strong><code>&gt;&gt; /var/log/backup.log</code></strong><br><em>(Append Output — Slide 55)</em></td>
                <td>Hướng cổng kết quả bình thường (<code>stdout: 1</code>) ghi <strong>nối đuôi</strong> vào cuối file <code>/var/log/backup.log</code> (cờ <code>O_APPEND</code>).</td>
                <td>Giữ nguyên lịch sử cũ trong file, các dòng kết quả mới của đêm nay sẽ được viết tiếp xuống dưới cùng theo trình tự thời gian.</td>
              </tr>
              <tr>
                <td><strong><code>2&gt;&amp;1</code></strong><br><em>(Merge Error to Output — <code>dup2(1, 2)</code>)</em></td>
                <td>Bẻ cổng báo lỗi số <code>2</code> (<code>stderr</code>) nhập chung vào <strong>đúng chỗ mà cổng số <code>1</code> (<code>&amp;1</code>) đang trỏ tới</strong> tại thời điểm đó.</td>
                <td>Đảm bảo mọi thông báo lỗi phát sinh cũng chảy vào file <code>/var/log/backup.log</code>. <em>Lưu ý sống còn:</em> Phải viết <code>&gt;&gt; file 2&gt;&amp;1</code> (nếu viết ngược <code>2&gt;&amp;1 &gt;&gt; file</code>, cổng 2 sẽ trỏ vào màn hình cũ trước khi cổng 1 rẽ vào file!).</td>
              </tr>
              <tr>
                <td><strong><code>&lt; input.txt</code></strong> &amp; <strong><code>&lt;&lt; EOF</code></strong><br><em>(Input &amp; Here-Document — Slide 55)</em></td>
                <td>Bơm nội dung từ một file có sẵn (<code>&lt;</code>) hoặc một khối văn bản nhiều dòng ngay trong kịch bản (<code>&lt;&lt; EOF ... EOF</code>) vào cổng <code>stdin (0)</code>.</td>
                <td>Giúp tự động cấp dữ liệu đầu vào cho chương trình mà không cần con người ngồi gõ bàn phím trực tiếp.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3>4. Đúc kết Cơ học &amp; Đánh đổi (Trade-off)</h3>
        <ul>
          <li><strong>Bản chất cơ học:</strong> Ký hiệu <code>&amp;1</code> trong cụm <code>2&gt;&amp;1</code> có nghĩa là <em>"địa chỉ hiện tại của cổng số 1"</em> (thực thi qua lời gọi hệ thống <code>dup2()</code> trong Kernel — <em>TLPI</em>, Ch. 5.5). Nhờ bẻ cổng <code>2</code> chập vào cổng <code>1</code> sau khi cổng <code>1</code> đã nối vào file nhật ký, không một dòng báo lỗi nào có thể lọt ra ngoài khi hệ thống chạy ngầm.</li>
          <li><strong>Sự đánh đổi dẫn sang Chặng 4:</strong> Đến đây, bạn đã nắm vững cách điều khiển một <code>Process</code> đơn lẻ (Chặng 2) và cách ghép nối nhiều <code>Process</code> phối hợp với nhau cũng như thu gom nhật ký lỗi (Chặng 3). Nhưng chẳng lẽ đêm nào bạn cũng phải thức dậy lúc <code>2:00</code> sáng để tự tay gõ chuỗi lệnh này? Làm sao để biến toàn bộ quy trình thành một dây chuyền tự động hóa chạy <code>24/7</code>? Chúng ta bước vào Chặng 4!</li>
        </ul>

        <section class="summary-section" id="linux-3-summary" tabindex="-1">
          <h2>TÓM TẮT BỎ TÚI CHẶNG 3</h2>
          <p><strong>Mạch nhân – quả xuyên suốt Chặng 3:</strong></p>
          <ul>
            <li><strong>[Trạm 3.1]</strong> Mỗi <code>Process</code> chỉ làm tốt một việc riêng và có 3 cổng giao tiếp độc lập (<code>stdin: 0</code>, <code>stdout: 1</code>, <code>stderr: 2</code>) ➔ Để ghép nhiều lệnh làm việc nối tiếp nhau mà không phải ghi file tạm ra ổ cứng, <code>Shell</code> đấu nối cổng <code>1</code> của lệnh trước sang cổng <code>0</code> của lệnh sau, còn <code>Kernel</code> giữ đường ống <code>Pipe</code> truyền từng <code>byte</code> dữ liệu trên bộ nhớ <code>RAM</code> (trong khi cổng <code>stderr: 2</code> đi đường riêng để không làm bẩn dữ liệu) ➔</li>
            <li><strong>[Trạm 3.2]</strong> Khi lệnh chạy ngầm không có màn hình <code>Terminal</code>, để không bị "mù lỗi", kỹ sư dùng <code>&gt;&gt;</code> để ghi nối đuôi cổng <code>stdout (1)</code> vào file log và dùng <code>2&gt;&amp;1</code> để gộp luôn cổng <code>stderr (2)</code> vào cùng file log đó.</li>
          </ul>
          <p><strong>Checklist tự kiểm tra (3 Câu hỏi Bản chất trước khi sang Chặng 4):</strong></p>
          <ol>
            <li>Khi nối hai lệnh bằng đường ống <code>Pipe (|)</code>, tại sao cổng <code>stderr (2)</code> của tiến trình thứ nhất phải đi đường riêng mà không chảy chung vào cổng <code>stdout (1)</code> sang tiến trình thứ hai?</li>
            <li>Trong quá trình phối hợp đa tiến trình, <code>Process</code>, <code>Shell</code> và <code>Kernel</code> phân chia công việc lắp ống và truyền dữ liệu cho nhau như thế nào?</li>
            <li>Trong cú pháp <code>&gt;&gt; /var/log/backup.log 2&gt;&amp;1</code>, ký hiệu <code>&gt;&gt;</code> và cụm <code>2&gt;&amp;1</code> lần lượt tác động lên những cổng nào và tại sao không được đảo ngược thứ tự của chúng?</li>
          </ol>
          <p style="margin-top:14px;"><strong>Bước tiếp theo:</strong> Chuyển sang <a href="#topic=F01&stage=4" onclick="selectStorageStage(4);return false;">Chặng 4: Biến các Lệnh Đã Hiểu Việc thành Dây chuyền Chạy Tự động 24/7 (Bash Script, GCC/Makefile &amp; Cronjob) ➔</a></p>
        </section>
      </div>
    `;
  }

  function renderLinuxChang4() {
    const d = HUB_DATA.linux_diagrams;
    return `
      <div class="prose">
        <p>Ở <strong>Chặng 3</strong>, chúng ta đã biết cách đấu nối các tiến trình bằng đường ống <code>Pipe (|)</code> và thu gom toàn bộ luồng kết quả lẫn luồng lỗi bằng <code>&gt;&gt; /var/log/backup.log 2&gt;&amp;1</code>. Bước vào <strong>Chặng 4 (Trạm 4.1 ➔ 4.3)</strong> — chặng cuối cùng khép lại học phần <strong>F01 · Linux Fundamentals</strong> — trước khi đi vào từng công cụ, hãy nhìn bức tranh tổng thể: Để hệ thống tự vận hành mà không cần con người ngồi gõ lệnh, Linux phối hợp nhịp nhàng một <strong>bộ ba công cụ tự động hóa</strong>, mỗi công cụ trả lời đúng một câu hỏi cơ học:</p>

        <h4>Sơ đồ 4.0: Phối hợp Nhịp nhàng giữa Bộ ba Công cụ Tự động hóa trong Linux</h4>
        ${buildVisualBlock(
          "linux-4-0",
          "Sơ đồ 4.0 — Dây chuyền Tự động hóa 24/7: Phân vai Rõ ràng giữa 3 Công cụ (Shell Script, Make & Cronjob)",
          d["4.0"].ascii,
          d["4.0"].mermaid,
          "Bộ ba tự động hóa trong Linux: [1] Shell Script (.sh) định nghĩa 'Làm những bước nào?', [2] Make (Makefile) kiểm tra 'File nào vừa sửa, có cần biên dịch lại không?', và [3] Cronjob (crond) quyết định 'Khi nào bắt đầu kích hoạt?'."
        )}

        <h2 id="linux-4-1" tabindex="-1">TRẠM 4.1: BASH SCRIPTING — "TỜ GIẤY DÁN TỦ LẠNH" ĐỊNH NGHĨA LÀM BƯỚC NÀO, RA SAO</h2>

        <h3>1. Bối cảnh &amp; Ẩn dụ đời thực</h3>
        <p>Người mới học thường bối rối giữa 3 khái niệm: <code>Shell</code>, <code>Bash</code> và <code>Bash Scripting</code>. Hãy dùng một ẩn dụ cực kỳ đời thường (đối chiếu <em>Slide 46–51</em> của bài giảng <code>01-linux-fundamentals.pdf</code>):</p>
        <ul>
          <li><strong><code>Shell</code></strong> giống như khái niệm <strong>"Xe hơi" nói chung</strong> — là chương trình thông dịch lệnh nằm giữa con người và <code>Kernel</code> (có nhiều hãng khác nhau như <code>sh</code>, <code>bash</code>, <code>zsh</code>, <code>fish</code>).</li>
          <li><strong><code>Bash</code></strong> (<em>Bourne-Again SHell</em>) giống như một dòng xe cụ thể rất phổ biến (ví dụ: <strong>"Xe Mec / BMW"</strong>) — là loại <code>Shell</code> mặc định trên hầu hết các bản phân phối Linux thuộc dự án <code>GNU</code>.</li>
          <li><strong><code>Bash Scripting</code></strong> giống như <strong>"Tờ giấy dán trên tủ lạnh"</strong> ghi sẵn danh sách công việc từ bước 1 đến bước 10. Thay vì bạn phải đứng đọc từng câu lệnh cho đầu bếp làm, bạn viết tất cả vào một file văn bản có đuôi <code>.sh</code> để <code>Bash</code> tự đọc từ trên xuống dưới và làm một mạch!</li>
        </ul>

        <h3>2. Nỗi đau (Pain Point) từ trạm trước</h3>
        <p>Ở Chặng 2 và Chặng 3, nếu mỗi lần cần sao lưu dữ liệu và lọc nhật ký mà bạn phải tự tay gõ hàng chục lệnh trên <code>Terminal</code>, bạn sẽ rất dễ gõ sót bước, gõ nhầm tên thư mục, và không thể tự động kiểm tra điều kiện (ví dụ: <em>"Nếu có file báo cáo thì mới nén, nếu không có thì báo lỗi"</em>) hay lặp lại công việc qua hàng loạt máy chủ.</p>

        <h3>3. Sơ đồ Giải phẫu Cơ chế &amp; Bảng Dữ liệu thật</h3>

        <h4>Sơ đồ 4.1A: Sơ đồ Phân cấp giữa Shell, Bash và Bash Scripting</h4>
        ${buildVisualBlock(
          "linux-4-1a",
          "Sơ đồ 4.1A — Từ Trình Thông dịch Lệnh (Shell / Bash) đến Kịch bản Tự động (Bash Script .sh)",
          d["4.1a"].ascii,
          d["4.1a"].mermaid,
          "Phân cấp 3 tầng từ khái niệm chung Shell (sh, bash, zsh, fish) xuống Bash (Bourne-Again SHell mặc định của GNU) và kịch bản Bash Script (.sh) tích hợp Shebang #!/bin/bash, biến, nhánh điều kiện if/else, vòng lặp for và quyền thực thi chmod +x."
        )}

        <h4>Sơ đồ 4.1B: Trình Soạn thảo CLI (Nano vs. Vim) &amp; Cú pháp Bash Thực chiến (Slide 48–63)</h4>
        ${buildVisualBlock(
          "linux-4-1b",
          "Sơ đồ 4.1B — Soạn thảo Kịch bản trên Terminal (Nano vs. Vim) & Các Cấu trúc Bash Cốt lõi (Slide 48–63)",
          d["4.1b"].ascii,
          d["4.1b"].mermaid,
          "Đối chiếu hai trình soạn thảo dòng lệnh Nano (^O lưu, ^X thoát) và Vim (3 chế độ Normal, Insert 'i', Command ':wq' / ':q!'), cùng cạm bẫy so sánh chuỗi [[ 10 > 9 ]] vs số học (( 10 > 9 )), mảng (Arrays) và hàm (Functions)."
        )}

        <h4>Khối lệnh Thực tế: Kịch bản Mẫu <code>backup.sh</code> Tích hợp Đủ 5 Thành phần Cốt lõi</h4>
        <pre><code>#!/bin/bash
# 1. Dòng chỉ dẫn trình thông dịch (Shebang): Báo cho hệ thống dùng /bin/bash để chạy file này

# 2. Khai báo biến (Variables): Lưu ý KHÔNG có khoảng trắng quanh dấu "="
TEN="Nam"
THU_MUC="/home/nam/tailieu"
FILE="baocao.csv"

echo "Xin chào \$TEN! Đang kiểm tra thư mục \$THU_MUC..."

# 3. Nhánh điều kiện (if / else): Kiểm tra xem file có tồn tại hay không (-f)
if [ -f "\$FILE" ]; then
    echo "Tìm thấy file \$FILE! Bắt đầu sao lưu..."
else
    echo "CẢNH BÁO: Không tìm thấy file \$FILE!"
fi

# 4. Vòng lặp (for loop): Tự động lặp qua danh sách nhiều máy chủ
for SERVER in server1 server2 server3; do
    echo "Đang đồng bộ dữ liệu lên máy chủ: \$SERVER"
done</code></pre>
        <p>Để chạy kịch bản trên như một chương trình thực thụ (Cách 2 trên <em>Slide 51</em>), kỹ sư chỉ cần thực hiện 2 lệnh (hoặc gọi trực tiếp <code>bash backup.sh</code> theo Cách 1):</p>
        <pre><code>chmod +x backup.sh   # Bước 5: Cấp quyền thực thi (Execute) cho file kịch bản
./backup.sh          # Kích hoạt chạy kịch bản ngay tại thư mục hiện tại</code></pre>

        <h4>Bảng 4.1A: Giải phẫu Cơ học 5 Thành phần Cốt lõi của một File Bash Script (<code>.sh</code>)</h4>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Thành phần trong Script</th>
                <th>Cú pháp Thực tế</th>
                <th>Vai trò Cơ học</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>1. <code>Shebang</code></strong><br><em>(Chỉ dẫn trình thông dịch — Slide 47)</em></td>
                <td><code>#!/bin/bash</code> <em>(luôn đặt ở dòng đầu tiên)</em></td>
                <td>Chỉ định rõ cho <code>Linux Kernel</code> (hàm <code>execve()</code> — <em>TLPI</em> Ch. 27) phải gọi đúng chương trình <code>/bin/bash</code> ra để đọc và thực thi các dòng lệnh bên dưới.</td>
              </tr>
              <tr>
                <td><strong>2. Biến (<code>Variables</code>)</strong><br><em>(Slide 52–54)</em></td>
                <td>Gán: <code>TEN="Nam"</code><br>Gọi ra: <code>\$TEN</code> | Nhập từ bàn phím: <code>read TEN</code></td>
                <td>Lưu trữ tên người dùng, đường dẫn thư mục hoặc tên file vào bộ nhớ để tái sử dụng nhiều lần. <em>(Lưu ý sống còn: Tuyệt đối không đặt khoảng trắng quanh dấu <code>=</code> khi gán biến; dùng <code>export</code> nếu muốn truyền biến sang tiến trình con!).</em></td>
              </tr>
              <tr>
                <td><strong>3. Điều kiện (<code>if / elif / else</code>)</strong><br><em>(Slide 57)</em></td>
                <td><code>if [ -f "\$FILE" ]; then ... else ... fi</code></td>
                <td>Giúp kịch bản biết tự ra quyết định rẽ nhánh (ví dụ: kiểm tra file có tồn tại <code>-f</code> hay thư mục có tồn tại <code>-d</code> trước khi xử lý).</td>
              </tr>
              <tr>
                <td><strong>4. Vòng lặp (<code>for / while</code>)</strong><br><em>(Slide 58–59)</em></td>
                <td><code>for SERVER in server1 server2 server3; do ... done</code><br>hoặc <code>for i in {1..5}; do ... done</code></td>
                <td>Tự động lặp đi lặp lại cùng một thao tác qua một danh sách nhiều phần tử (nhiều file, nhiều máy chủ) mà không phải viết lặp lại lệnh.</td>
              </tr>
              <tr>
                <td><strong>5. Cấp quyền &amp; Chạy</strong><br><em>(Slide 51)</em></td>
                <td><code>chmod +x backup.sh</code> rồi gõ <code>./backup.sh</code><br><em>(hoặc chạy trực tiếp: <code>bash backup.sh</code>)</em></td>
                <td>Biến một file văn bản bình thường thành một chương trình có quyền thực thi (<code>x</code>) độc lập trên hệ thống.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h4>Bảng 4.1B: Trình Soạn thảo CLI (<code>Nano</code> vs. <code>Vim</code>), Cạm bẫy So sánh Số học <code>(( ))</code>, Mảng &amp; Hàm Bash (Slide 48–63)</h4>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Chủ đề Thực chiến (Slide 48–63)</th>
                <th>Cú pháp / Thao tác Chuẩn</th>
                <th>Cơ chế &amp; Cạm bẫy Kỹ sư Cần Nhớ</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Trình soạn thảo <code>Nano</code> vs. <code>Vim</code></strong><br><em>(Slide 48–50)</em></td>
                <td><strong>Nano:</strong> <code>Ctrl+O</code> (Lưu), <code>Ctrl+X</code> (Thoát), <code>Ctrl+K</code> (Cắt), <code>Ctrl+U</code> (Dán).<br><strong>Vim:</strong> Bấm <code>i</code> vào <em>Insert Mode</em> ➔ bấm <code>ESC</code> về <em>Normal Mode</em> ➔ gõ <code>:wq</code> (Lưu &amp; thoát) hoặc <code>:q!</code> (Thoát hủy sửa).</td>
                <td>Trên máy chủ Linux (Server không có chuột), <code>Nano</code> giúp chỉnh sửa nhanh cho người mới, còn <code>Vim</code> cực mạnh khi xử lý file cấu hình lớn nhờ tách biệt chế độ di chuyển/xóa (<em>Normal Mode</em>: <code>dd</code> xóa dòng, <code>u</code> hoàn tác) và chế độ gõ chữ (<em>Insert Mode</em>).</td>
              </tr>
              <tr>
                <td><strong>Cạm bẫy So sánh Chuỗi vs. Số học</strong><br><em>(Slide 56)</em></td>
                <td>Sai (Chuỗi): <code>[[ 10 &gt; 9 ]]</code> ➔ <strong><code>False</code> (1)</strong><br>Đúng (Số): <code>(( 10 &gt; 9 ))</code> ➔ <strong><code>True</code> (0)</strong></td>
                <td>Bên trong cặp ngoặc vuông <code>[[ ... ]]</code>, dấu <code>&gt;</code> so sánh theo <strong>thứ tự bảng chữ cái ASCII (Lexicographical)</strong> nên ký tự đầu <code>'1'</code> của <code>"10"</code> nhỏ hơn <code>'9'</code>! Muốn tính toán hoặc so sánh số học trong Bash, bắt buộc dùng ngoặc kép <code>(( 10 &gt; 9 ))</code> hoặc cờ <code>-gt</code>, <code>-lt</code>, <code>-eq</code>.</td>
              </tr>
              <tr>
                <td><strong>Mảng (<code>Arrays</code>) trong Bash</strong><br><em>(Slide 60)</em></td>
                <td>Khai báo: <code>my_array=(10 2 300)</code><br>Đầu: <code>\${my_array[0]}</code> | Cuối: <code>\${my_array[-1]}</code><br>Độ dài: <code>\${#my_array[@]}</code></td>
                <td>Các phần tử trong mảng Bash phân tách nhau bằng <strong>khoảng trắng</strong> (không dùng dấu phẩy). Dùng <code>unset my_array[1]</code> để xóa phần tử tại vị trí số 1.</td>
              </tr>
              <tr>
                <td><strong>Hàm (<code>Functions</code>) &amp; Mã thoát <code>\$?</code></strong><br><em>(Slide 61–62)</em></td>
                <td>Đối số vào hàm: <code>\$1</code>, <code>\$2</code> | Biến cục bộ: <code>local</code><br>Bắt kết quả in ra: <code>kq=\$(ten_ham)</code><br>Kiểm tra mã thoát: <code>echo \$?</code></td>
                <td>Trong Linux, hàm dùng <code>return 0</code> để báo <strong>thành công (Success)</strong> và <code>1..255</code> để báo <strong>mã lỗi (Error Status)</strong> đọc qua biến <code>\$?</code>; còn muốn trả về chuỗi dữ liệu từ hàm thì dùng <code>echo</code> kết hợp <code>\$(...)</code> (Command Substitution).</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3>4. Đúc kết Cơ học &amp; Đánh đổi (Trade-off)</h3>
        <ul>
          <li><strong>Bản chất cơ học:</strong> <code>Bash Script</code> gom các lệnh rời rạc thành một quy trình khép kín có biến nhớ, có rẽ nhánh điều kiện và có vòng lặp tự động.</li>
          <li><strong>Sự đánh đổi dẫn sang Trạm 4.2:</strong> <code>Bash Script</code> là ngôn ngữ thông dịch (<em>Interpreted</em>) — mỗi lần chạy là <code>Bash</code> phải đọc từng dòng chữ rồi dịch ngay lúc đó nên tốc độ xử lý tính toán nặng rất chậm. Với các phần mềm đòi hỏi tốc độ cao viết bằng ngôn ngữ <code>C/C++</code> gồm hàng trăm file mã nguồn, làm sao để dịch chúng sang mã máy (<code>0</code> và <code>1</code>) và quản lý việc cập nhật mà không phải biên dịch lại từ đầu toàn bộ dự án mỗi khi chỉ sửa <code>1</code> dòng code?</li>
        </ul>

        <h2 id="linux-4-2" tabindex="-1">TRẠM 4.2: COMPILATION (GCC) &amp; MAKEFILE — LÒ LUYỆN MÃ MÁY &amp; NGƯỜI QUẢN ĐỐC XƯỞNG</h2>

        <h3>1. Bối cảnh &amp; Ẩn dụ đời thực</h3>
        <ul>
          <li><strong><code>Compilation</code> (Biên dịch với <code>GCC</code>):</strong> Giống như một <strong>lò luyện kim</strong>. Mã nguồn viết bằng ngôn ngữ <code>C</code> (<code>.c</code>) hay <code>C++</code> (<code>.cpp</code>) là bản thiết kế mà con người đọc hiểu được, nhưng <code>CPU</code> không hiểu. Trình biên dịch <code>gcc</code> / <code>g++</code> sẽ nung chảy bản thiết kế đó qua 4 công đoạn (<code>Pre-processor ➔ Compiler ➔ Assembler ➔ Linker</code>) để đúc thành một cỗ máy nguyên khối bằng mã máy nhị phân (<code>Binary Executable</code>) chạy với tốc độ tối đa (<em>Slide 64–67</em>).</li>
          <li><strong><code>Make</code> &amp; <code>Makefile</code>:</strong> Giống như <strong>người quản đốc phân xưởng thông minh</strong> (<em>Slide 68–71</em>). Khi dự án có <code>100</code> bản thiết kế (<code>.c</code>), nếu bạn chỉ vừa sửa lại đúng <code>1</code> bản thiết kế <code>main.c</code>, người quản đốc <code>make</code> sẽ nhìn vào đồng hồ thời gian (<code>Timestamp</code>) trên từng file để chỉ nung đúc lại đúng phần vừa sửa, tuyệt đối không đập đi làm lại cả <code>99</code> phần kia!</li>
        </ul>

        <h3>2. Nỗi đau (Pain Point) từ trạm trước</h3>
        <p>Khi xây dựng một phần mềm lớn từ nhiều file mã nguồn (<code>main.c</code>, <code>ham_phu.c</code>...), nếu biên dịch thủ công bằng tay với lệnh <code>gcc</code>, bạn vừa phải gõ những câu lệnh dài lê thê, vừa phải chờ máy biên dịch lại từ đầu toàn bộ <code>100</code> file dù bạn chỉ sửa đúng một dấu chấm phẩy trong <code>1</code> file duy nhất — cực kỳ lãng phí thời gian và tài nguyên máy tính.</p>

        <h3>3. Sơ đồ Giải phẫu Cơ chế &amp; Bảng Dữ liệu thật</h3>

        <h4>Sơ đồ 4.2A: Dây chuyền Biên dịch Mã nguồn C sang Mã máy của GCC (Slide 64–67)</h4>
        ${buildVisualBlock(
          "linux-4-2a",
          "Sơ đồ 4.2A — Quá trình Biên dịch 4 Bước của GCC (.c ➔ .i ➔ .s ➔ .o ➔ Binary ELF 64-bit)",
          d["4.2a"].ascii,
          d["4.2a"].mermaid,
          "Trình biên dịch GCC đưa mã nguồn C (.c) qua 4 giai đoạn: Pre-processor (.i) ➔ Compiler (.s Assembly) ➔ Assembler (.o Object file) ➔ Linker ghép các file .o cùng thư viện thành chương trình thực thi nhị phân ELF 64-bit."
        )}

        <h4>Sơ đồ 4.2B: Cơ chế Quyết định Thông minh của Make dựa trên Makefile (Slide 68–71)</h4>
        ${buildVisualBlock(
          "linux-4-2b",
          "Sơ đồ 4.2B — Cách Quản đốc Make Kiểm tra Thời gian Sửa đổi (Timestamp mtime) & Nhãn .PHONY",
          d["4.2b"].ascii,
          d["4.2b"].mermaid,
          "Công cụ Make đọc Makefile theo cấu trúc Target : Prerequisites và dòng lệnh Recipe thụt đầu dòng bằng phím [TAB], đối chiếu Timestamp (mtime) để chỉ dịch lại file .c vừa sửa và bỏ qua các file .o còn mới."
        )}

        <h4>Khối lệnh Thực tế: Cấu trúc một File <code>Makefile</code> Chuẩn mực (Kèm Luật Phím <code>[TAB]</code> &amp; Nhãn <code>.PHONY</code>)</h4>
        <pre><code># Khai báo biến trình biên dịch và cờ tối ưu (Slide 71)
CC = gcc
CFLAGS = -Wall -O2

# Khai báo các nhãn tác vụ không phải tên file thật trên ổ đĩa (.PHONY — Slide 71)
.PHONY: all clean

all: ung_dung

# CẤU TRÚC QUY TẮC: Đích_cần_tạo (Target) : Các_file_nguyên_liệu (Prerequisites)
# [!] LƯU Ý SỐNG CÒN: Dòng lệnh thực thi (Recipe) bên dưới BẮT BUỘC phải thụt lề bằng phím [TAB] (không dùng dấu cách Space!)

ung_dung: main.o ham_phu.o
	\$(CC) \$(CFLAGS) main.o ham_phu.o -o ung_dung

main.o: main.c
	\$(CC) \$(CFLAGS) -c main.c -o main.o

ham_phu.o: ham_phu.c
	\$(CC) \$(CFLAGS) -c ham_phu.c -o ham_phu.o

# Tác vụ dọn dẹp nhanh toàn bộ file tạm sau khi biên dịch
clean:
	rm -f *.o ung_dung</code></pre>

        <h4>Bảng 4.2: Đối chiếu Cơ học giữa Biên dịch Thủ công (<code>gcc</code>) và Quản lý Tự động (<code>make</code>)</h4>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Tiêu chí Đối chiếu</th>
                <th>Biên dịch Thủ công bằng <code>gcc</code> (<em>Slide 65–67</em>)</th>
                <th>Quản lý Biên dịch bằng <code>make</code> &amp; <code>Makefile</code> (<em>Slide 68–71</em>)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Câu lệnh kích hoạt</strong></td>
                <td>Phải gõ tay toàn bộ: <code>gcc main.c ham_phu.c -o ung_dung</code> (và kiểm tra bằng <code>file ung_dung</code> ➔ <code>ELF 64-bit LSB shared object</code>).</td>
                <td>Chỉ cần gõ đúng một từ ngắn gọn: <code>make</code> (hoặc <code>make clean</code> khi muốn dọn rác).</td>
              </tr>
              <tr>
                <td><strong>Cơ chế khi sửa <code>1</code> file nhỏ</strong></td>
                <td>Biên dịch lại từ đầu tất cả các file mã nguồn trong dự án.</td>
                <td>Tự động so sánh thời gian sửa file (<code>mtime Timestamp</code>): Chỉ biên dịch lại đúng file vừa bị sửa đổi.</td>
              </tr>
              <tr>
                <td><strong>Quy tắc cú pháp bắt buộc</strong></td>
                <td>Truyền đúng cờ <code>-c</code> (tạo file đối tượng <code>.o</code>) và cờ <code>-o</code> (đặt tên file đầu ra).</td>
                <td>Dòng lệnh thực thi (<code>Recipe</code>) bên dưới dòng <code>Target: Prerequisites</code> <strong>bắt buộc phải thụt đầu dòng bằng phím <code>[TAB]</code></strong>; dùng <code>.PHONY</code> cho các nhãn hành động như <code>all</code>, <code>clean</code>, <code>build</code>, <code>test</code>.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3>4. Đúc kết Cơ học &amp; Đánh đổi (Trade-off)</h3>
        <ul>
          <li><strong>Bản chất cơ học:</strong> <code>GCC</code> biến mã nguồn con người viết thành mã máy tốc độ cao, còn <code>Make</code> dùng mốc thời gian (<code>Timestamp</code>) của từng file để đảm bảo hệ thống không bao giờ làm lại những bước biên dịch dư thừa.</li>
          <li><strong>Sự đánh đổi dẫn sang Trạm 4.3:</strong> Bây giờ bạn đã có kịch bản <code>backup.sh</code> (biết làm những bước nào) và <code>Makefile</code> (biết lắp ráp chương trình thông minh). Nhưng cả hai công cụ này đều nằm im trên ổ đĩa cho đến khi có ai đó gõ lệnh kích hoạt. Làm sao để đúng <code>2:00</code> sáng mỗi ngày, hệ thống tự động bấm nút chạy mà bạn vẫn ngủ ngon?</li>
        </ul>

        <h2 id="linux-4-3" tabindex="-1">TRẠM 4.3: HỆ THỐNG CRONJOB — TRỰC BAN 24/7 ("KHI NÀO BẮT ĐẦU CHẠY?") &amp; 3 CẠM BẪY KINH ĐIỂN</h2>

        <h3>1. Bối cảnh &amp; Ẩn dụ đời thực</h3>
        <p>Để hẹn giờ tự động trên Linux, bạn sẽ gặp 4 khái niệm có chữ "Cron" rất dễ bị gọi lẫn lộn. Hãy phân biệt chúng thật rạch ròi qua hình ảnh <strong>Hệ thống Trực ban Tòa nhà</strong> (<em>Slide 72–74</em> &amp; <em>TLPI</em> Ch. 37):</p>
        <ul>
          <li><strong><code>Cron</code></strong>: Là tên gọi chung của <strong>toàn bộ hệ thống/cơ chế hẹn giờ tự động</strong> trong Linux.</li>
          <li><strong><code>Crontab</code></strong> (<em>Cron Table</em>): Là <strong>cuốn sổ lịch trình (bảng thời gian biểu)</strong> ghi danh sách giờ nào làm việc gì (gõ <code>crontab -e</code> để mở sổ ra sửa, <code>crontab -l</code> để xem sổ, <code>crontab -r</code> để xóa sổ).</li>
          <li><strong><code>Cronjob</code></strong>: Là <strong>từng dòng công việc cụ thể</strong> được ghi bên trong cuốn sổ <code>Crontab</code> đó.</li>
          <li><strong><code>Crond</code></strong> (<em>Cron Daemon</em>): Là <strong>anh bảo vệ chạy ngầm 24/7</strong>, cứ đúng mỗi <strong><code>60 giây</code> (1 phút)</strong> lại thức dậy một lần, cầm đồng hồ đối chiếu với cuốn sổ <code>Crontab</code>: Hễ thấy dòng <code>Cronjob</code> nào khớp với giờ hiện tại là lập tức bấm nút kích hoạt!</li>
        </ul>

        <h3>2. Nỗi đau (Pain Point) từ trạm trước</h3>
        <p>Đây là "cơn ác mộng" kinh điển nhất của mọi kỹ sư vận hành Linux: Lúc chiều ngồi gõ lệnh chạy thử kịch bản <code>./backup.sh</code> trên màn hình <code>Terminal</code> thì chạy mượt mà 100%, nhưng tối hôm đó cài vào <code>Crontab</code> để hẹn <code>2:00</code> sáng tự chạy thì sáng hôm sau mở ra thấy <strong>không có bất kỳ bản sao lưu nào được tạo ra, cũng chẳng có một dòng báo lỗi nào</strong>! Tại sao một lệnh chạy tay thì sống mà đưa vào <code>Cronjob</code> lại chết im lặng?</p>

        <h3>3. Sơ đồ Giải phẫu Cơ chế &amp; Bảng Dữ liệu thật</h3>

        <h4>Sơ đồ 4.3A: Giải phẫu 5 Trường Thời gian của Crontab (Từ Nhỏ đến Lớn — Slide 73–74)</h4>
        ${buildVisualBlock(
          "linux-4-3a",
          "Sơ đồ 4.3A — Công thức Đọc 5 Dấu sao (* * * * *) trong Crontab: Từ Đơn vị Nhỏ đến Đơn vị Lớn",
          d["4.3a"].ascii,
          d["4.3a"].mermaid,
          "Giải phẫu 4 khái niệm Cron/Crontab/Cronjob/Crond và 5 trường thời gian của Crontab sắp xếp từ đơn vị nhỏ đến lớn: Phút (0-59) ➔ Giờ (0-23) ➔ Ngày trong tháng (1-31) ➔ Tháng (1-12) ➔ Thứ trong tuần (0-6 hoặc 0-7, Chủ Nhật = 0 hoặc 7), cùng 4 ký tự *, ,, -, /."
        )}

        <h4>Sơ đồ 4.3B: Vòng lặp Quét 60 Giây của Crond, 3 Cạm bẫy Kinh điển &amp; 2 Giới hạn Cốt tử (Slide 72–76)</h4>
        ${buildVisualBlock(
          "linux-4-3b",
          "Sơ đồ 4.3B — Cơ chế Quét Mỗi 60 Giây của Crond, 3 Cạm bẫy 'Chết Im Lặng' & Giải pháp Bọc Lỗi (Slide 72–76)",
          d["4.3b"].ascii,
          d["4.3b"].mermaid,
          "Mỗi 60 giây tiến trình ngầm crond quét bảng Crontab; để không chết im lặng, kỹ sư phải vượt qua 3 cạm bẫy (đường dẫn tuyệt đối, thu gom log 2>&1, đúng sổ user vs root) và 2 giới hạn cốt tử của Cron (không tự retry khi lỗi mạng, mất lịch khi máy tắt nguồn)."
        )}

        <h4>Bảng 4.3A: Bộ 6 Ví dụ Lập lịch Crontab Thực chiến Điển hình Nhất (Slide 73–74)</h4>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Biểu thức 5 Trường (<code>Phút Giờ Ngày Tháng Thứ</code>)</th>
                <th>Ý nghĩa Thời gian Thực thi</th>
                <th>Giải thích Cơ học theo Ký tự Điều khiển</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong><code>* * * * *</code></strong></td>
                <td>Chạy <strong>mỗi phút một lần</strong> (<code>Every minute</code>).</td>
                <td>Cả 5 trường đều là dấu <code>*</code> (khớp với mọi phút, mọi giờ, mọi ngày).</td>
              </tr>
              <tr>
                <td><strong><code>*/5 * * * *</code></strong></td>
                <td>Chạy <strong>mỗi 5 phút một lần</strong> (<code>00, 05, 10, 15...</code>).</td>
                <td>Ký tự bước nhảy <code>*/5</code> ở trường Phút chia chu kỳ 60 phút thành các nhịp 5 phút.</td>
              </tr>
              <tr>
                <td><strong><code>0 2 * * *</code></strong></td>
                <td>Chạy vào đúng <strong><code>02:00</code> sáng hàng ngày</strong>.</td>
                <td>Trường Phút = <code>0</code>, trường Giờ = <code>2</code>; 3 trường Ngày/Tháng/Thứ đều là <code>*</code>.</td>
              </tr>
              <tr>
                <td><strong><code>30 8 * * 1</code></strong></td>
                <td>Chạy vào <strong><code>08:30</code> sáng mỗi Thứ Hai hàng tuần</strong>.</td>
                <td>Phút = <code>30</code>, Giờ = <code>8</code>, Thứ trong tuần = <code>1</code> (Thứ Hai; lưu ý Chủ Nhật là <code>0</code> hoặc <code>7</code>).</td>
              </tr>
              <tr>
                <td><strong><code>0 9-17 * * *</code></strong></td>
                <td>Chạy <strong>đầu mỗi giờ trong khung giờ hành chính</strong> (từ <code>09:00</code> đến <code>17:00</code>).</td>
                <td>Dấu gạch ngang <code>9-17</code> ở trường Giờ chỉ định một khoảng liên tục từ 9 giờ đến 17 giờ.</td>
              </tr>
              <tr>
                <td><strong><code>0 0 1 * *</code></strong></td>
                <td>Chạy vào <strong><code>00:00</code> nửa đêm ngày Mùng 1 đầu mỗi tháng</strong>.</td>
                <td>Phút = <code>0</code>, Giờ = <code>0</code>, Ngày trong tháng = <code>1</code> (dùng cho báo cáo/dọn dẹp định kỳ hàng tháng).</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h4>Khối lệnh Thực tế: Quy trình 3 Bước Thiết lập một Cronjob Tự động Chạy Ngầm Hoàn chỉnh</h4>
        <p><strong>Bước 1:</strong> Viết nội dung kịch bản sao lưu vào đường dẫn tuyệt đối <code>/home/nam/backup.sh</code> (lưu ý dùng đường dẫn tuyệt đối cho mọi file/thư mục bên trong):</p>
        <pre><code>#!/bin/bash
# Đóng gói và nén toàn bộ thư mục tài liệu kèm nhãn ngày tháng năm (YYYY-MM-DD)
/bin/tar -czf /backup/tailieu_\$(/bin/date +%F).tar.gz /home/nam/tailieu</code></pre>
        <p><strong>Bước 2:</strong> Cấp quyền thực thi (<code>Execute</code>) cho file kịch bản:</p>
        <pre><code>chmod +x /home/nam/backup.sh</code></pre>
        <p><strong>Bước 3:</strong> Mở sổ lịch trình bằng lệnh <code>crontab -e</code> và thêm dòng hẹn giờ chạy lúc <code>2:00</code> sáng mỗi ngày (kết hợp thu gom toàn bộ nhật ký và lỗi từ Chặng 3):</p>
        <pre><code>0 2 * * * /home/nam/backup.sh &gt;&gt; /var/log/backup.log 2&gt;&amp;1</code></pre>

        <h4>Bảng 4.3B: 3 Cạm bẫy Kinh điển &amp; 2 Giới hạn Cốt tử của CronJob (Kèm Giải pháp từ Slide 75–76)</h4>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Cạm bẫy / Giới hạn Cốt tử</th>
                <th>Cơ chế Gốc Gây Lỗi (Root Cause)</th>
                <th>Giải pháp Thực chiến Chuẩn Công nghiệp</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Cạm bẫy 1: Quên Đường dẫn Tuyệt đối (<code>Absolute Path</code>)</strong></td>
                <td>Khi bạn mở <code>Terminal</code>, biến môi trường <code>\$PATH</code> chứa rất nhiều thư mục và bạn đang đứng sẵn ở thư mục làm việc. Nhưng khi <code>crond</code> chạy ngầm, nó khởi tạo một môi trường cực kỳ tối giản (<code>\$PATH=/usr/bin:/bin</code> và đứng ở <code>\$HOME</code>), nên gõ <code>backup.sh</code> hay <code>python3</code> trống không sẽ bị báo <em>"command not found"</em> ngay!</td>
                <td>Luôn viết <strong>đường dẫn tuyệt đối bắt đầu từ gốc <code>/</code></strong> cho cả chương trình lẫn file kịch bản (ví dụ: <code>/usr/bin/python3 /home/nam/script.py</code> hoặc khai báo <code>PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin</code> ở đầu <code>Crontab</code>).</td>
              </tr>
              <tr>
                <td><strong>Cạm bẫy 2: Quên Thu gom Log &amp; Lỗi (<code>2&gt;&amp;1</code>)</strong></td>
                <td>Tiến trình do <code>crond</code> đẻ ra lúc nửa đêm không gắn với bất kỳ màn hình <code>Terminal</code> nào. Nếu thiếu điều hướng, mọi dòng báo lỗi bắn ra từ cổng <code>stderr (2)</code> đều biến mất vô hình.</td>
                <td>Luôn gắn đuôi <code>&gt;&gt; /var/log/ten_file.log 2&gt;&amp;1</code> vào cuối dòng <code>Cronjob</code> để gom cả kết quả (<code>1</code>) lẫn báo lỗi (<code>2</code>) vào sổ nhật ký.</td>
              </tr>
              <tr>
                <td><strong>Cạm bẫy 3: Đặt Nhầm Sổ <code>Crontab</code> (User vs. Root)</strong></td>
                <td>Mỗi tài khoản trên Linux có một cuốn sổ <code>Crontab</code> riêng biệt! Gõ <code>crontab -e</code> là ghi vào sổ của <code>nam</code> (chạy với quyền hạn hẹp của <code>nam</code>); còn gõ <code>sudo crontab -e</code> là ghi vào sổ của <code>root</code>.</td>
                <td>Nếu kịch bản cần quyền quản trị (như ghi vào <code>/var/log</code> hoặc khởi động lại dịch vụ hệ thống), phải đặt trong <code>sudo crontab -e</code> (hoặc <code>/etc/crontab</code>), tránh đặt nhầm vào sổ của user thường gây lỗi <em>Permission denied</em>.</td>
              </tr>
              <tr>
                <td><strong>Giới hạn 4: Không Tự Thử Lại Khi Lỗi (<code>No Auto-Retry</code> — Slide 75)</strong></td>
                <td><code>Cron</code> chỉ biết kích hoạt lệnh đúng giờ hẹn. Nếu đúng <code>02:00</code> sáng mạng bị rớt 5 giây làm lệnh tải dữ liệu thất bại, <code>Cron</code> <strong>không bao giờ tự động chạy lại</strong> mà bỏ qua luôn đến tận ngày hôm sau!</td>
                <td>Bọc vòng lặp tự động thử lại (<code>Retry Loop</code>) ngay bên trong kịch bản <code>Bash Script</code> (<em>Slide 75</em>):<br><code>for ((i=1; i&lt;=3; i++)); do /home/nam/backup.sh &amp;&amp; exit 0; sleep 60; done</code> (thử tối đa 3 lần, mỗi lần cách nhau 60 giây).</td>
              </tr>
              <tr>
                <td><strong>Giới hạn 5: Mất Lịch Khi Máy Tắt Nguồn (<code>Missed Jobs</code> — Slide 75–76)</strong></td>
                <td>Nếu máy tính/server bị tắt nguồn hoặc bảo trì đúng vào lúc <code>02:00</code> sáng, khi bật máy lại lúc <code>08:00</code> sáng, <code>crond</code> sẽ <strong>bỏ qua luôn công việc đã lỡ</strong> chứ không chạy bù!</td>
                <td>Trên máy cá nhân hay tắt mở hoặc hệ thống Production hiện đại, sử dụng <strong><code>Anacron</code></strong> hoặc <strong><code>systemd Timers</code></strong> (<em>Slide 76</em>) — hỗ trợ tự động chạy bù các lịch bị lỡ khi bật máy (<code>Persistent=true</code>), kiểm tra điều kiện mạng sẵn sàng rồi mới chạy, và ghi log tập trung qua <code>journald</code>.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3>4. Đúc kết Cơ học &amp; Đánh đổi (Trade-off)</h3>
        <ul>
          <li><strong>Bản chất cơ học:</strong> Hệ thống <code>Cronjob</code> hoàn thiện mảnh ghép cuối cùng của dây chuyền tự động hóa: Tiến trình ngầm <code>crond</code> thức dậy mỗi <code>60 giây</code>, đọc 5 trường thời gian trong sổ <code>Crontab</code>, rồi tự động gọi kịch bản <code>Bash Script</code> (và <code>Make</code>) chạy ngầm cùng bộ thu gom nhật ký <code>&gt;&gt; ... 2&gt;&amp;1</code>.</li>
          <li><strong>Khép lại toàn bộ hành trình 4 Chặng:</strong> Từ một câu hỏi khởi đầu ở Chặng 1 (<em>"Khi bạn gõ một dòng lệnh, chuyện gì thực sự diễn ra bên dưới nắp máy?"</em>), giờ đây bạn đã nắm trọn vẹn đường đi cơ học của hệ điều hành Linux từ lõi <code>Kernel</code> ra tới dây chuyền tự động hóa <code>24/7</code>!</li>
        </ul>

        <section class="summary-section" id="linux-4-summary" tabindex="-1">
          <h2>TÓM TẮT BỎ TÚI CHẶNG 4 &amp; KHÉP KÍN HÀNH TRÌNH LINUX FUNDAMENTALS</h2>
          <p><strong>Mạch nhân – quả khép kín toàn bộ hành trình (Chặng 1 ➔ Chặng 4):</strong></p>
          <ul>
            <li><strong>[Chặng 1]</strong> Bạn hiểu cấu trúc "Căn bếp Linux" (<code>Kernel</code>, <code>Shell</code>, <code>Process</code>), phân biệt vì sao tác vụ nặng cần <code>CLI</code> thay vì <code>GUI</code>, và giải mã được từng thành phần trên dòng nhắc lệnh <code>nam@ubuntu:~$</code> ➔</li>
            <li><strong>[Chặng 2]</strong> Khi <code>Process</code> (như <code>grep</code>) đi làm việc, nó mang theo hồ sơ căn cước 5 thông tin để mở các <code>File</code> (vốn là nhãn tên trong <code>Directory</code> trỏ vào số căn cước <code>Inode</code>) nằm trên cây thư mục duy nhất bắt đầu từ gốc <code>/</code> ➔</li>
            <li><strong>[Chặng 3]</strong> Khi một <code>Process</code> không đủ sức làm hết mọi việc, <code>Shell</code> nối cổng <code>stdout (1)</code> của anh trước vào cổng <code>stdin (0)</code> của anh sau qua đường ống <code>Pipe</code> trong <code>Kernel</code>, đồng thời dùng <code>&gt;&gt;</code> và <code>2&gt;&amp;1</code> để gom sạch cả kết quả lẫn báo lỗi (<code>stderr: 2</code>) vào file nhật ký ➔</li>
            <li><strong>[Chặng 4]</strong> Toàn bộ chuỗi lệnh được đóng gói vào kịch bản <code>Bash Script (.sh)</code> (<strong>Làm những bước nào?</strong>), kết hợp với <code>GCC &amp; Makefile</code> (<strong>File nào vừa sửa cần biên dịch lại?</strong>) và giao cho bảo vệ <code>crond</code> canh sổ <code>Crontab</code> kích hoạt định kỳ (<strong>Khi nào bắt đầu chạy?</strong>).</li>
          </ul>
          <p><strong>Checklist tự kiểm tra cuối khóa (5 Câu hỏi Bản chất để làm chủ Linux Fundamentals):</strong></p>
          <ol>
            <li>Khi cần tự động hóa một hệ thống trên Linux, 3 công cụ <code>Bash Script</code>, <code>Make (Makefile)</code> và <code>Cronjob (crond)</code> phân chia nhau trả lời 3 câu hỏi cơ học nào?</li>
            <li>Hãy phân biệt rõ 3 khái niệm: <code>Shell</code>, <code>Bash</code> và <code>Bash Scripting</code>. Dòng chữ <code>#!/bin/bash</code> ở đầu file kịch bản dùng để báo điều gì cho hệ thống, và tại sao so sánh số học trong Bash phải dùng <code>(( 10 &gt; 9 ))</code> thay vì <code>[[ 10 &gt; 9 ]]</code>?</li>
            <li>Trong file <code>Makefile</code>, công cụ <code>make</code> dựa vào thông số nào của các file để biết có cần phải gọi <code>gcc</code> biên dịch lại hay không, và dòng lệnh bên dưới phải thụt đầu dòng bằng phím gì?</li>
            <li>Hãy giải thích thứ tự từ nhỏ đến lớn của 5 dấu sao <code>* * * * *</code> trong <code>Crontab</code> và phân biệt rõ 4 khái niệm: <code>Cron</code>, <code>Crontab</code>, <code>Cronjob</code>, <code>Crond</code>.</li>
            <li>Nếu một kịch bản chạy bằng tay trên <code>Terminal</code> thì thành công nhưng đưa vào <code>Crontab</code> chạy lúc nửa đêm lại thất bại im lặng, bạn sẽ kiểm tra ngay 3 cạm bẫy nào đầu tiên và xử lý ra sao nếu cần tự động thử lại (<code>Retry</code>) khi mạng chập chờn?</li>
          </ol>
          <p style="margin-top:14px;"><a href="#topic=F01&stage=1" onclick="selectStorageStage(1);return false;">Quay lại Chặng 1 (Trạm 0.0 — Bản đồ Tư duy Toàn Học phần F01 · Linux Fundamentals) ➔</a></p>
        </section>
      </div>
    `;
  }

  function renderLinuxTopic() {
    const totalStages = LINUX_STAGES.length;
    const currentStage = LINUX_STAGES.find(s => s.id === activeStorageStage) || LINUX_STAGES[0];
    const prevId = activeStorageStage > 1 ? activeStorageStage - 1 : null;
    const nextId = activeStorageStage < totalStages ? activeStorageStage + 1 : null;
    const padNum = n => String(n).padStart(2, "0");

    const stageRows = LINUX_STAGES.map(st => `
      <button type="button" class="stage-dir-item ${st.id === activeStorageStage ? 'active' : ''}" onclick="selectStorageStage(${st.id})">
        <span class="stage-dir-code">Chặng ${padNum(st.id)}</span>
        <span>${escapeHtml(st.title.replace(/^Chặng \d+:\s*/, ""))}</span>
        <span class="stage-dir-meta">${st.id <= 4 ? 'Đã có bài' : 'Khung Trạm'}</span>
      </button>
    `).join("");

    let bodyHtml = "";
    if (activeStorageStage === 1) {
      bodyHtml = renderLinuxChang1();
    } else if (activeStorageStage === 2) {
      bodyHtml = renderLinuxChang2();
    } else if (activeStorageStage === 3) {
      bodyHtml = renderLinuxChang3();
    } else if (activeStorageStage === 4) {
      bodyHtml = renderLinuxChang4();
    } else {
      bodyHtml = renderLinuxChang1();
    }

    return `
      <header class="lesson-header">
        <div class="lesson-meta">
          <span>I. Engineering Foundation · F01 · Linux Fundamentals</span>
          <a href="course-slides/01-linux-fundamentals.pdf" target="_blank" rel="noopener">Slide gốc: 01-linux-fundamentals.pdf (78 trang)</a>
        </div>
        <h1 class="lesson-title">Fundamentals of Engineering — Linux &amp; Bash Scripting</h1>
        <p class="lesson-lead">Mô hình cơ học "Căn bếp Linux" qua hành trình của chiến dịch săn lùng dòng nhật ký lỗi <code>grep ERROR /var/log/app.log</code>: Từ kiến trúc Kernel/Shell/Process, triết lý "Everything is a file" trên cây thư mục <code>/</code>, giao tiếp đa tiến trình qua 3 cổng <code>0/1/2</code> &amp; <code>Pipe</code>, đến dây chuyền tự động hóa 24/7 với <code>Bash Script</code>, <code>GCC/Makefile</code> và <code>Cronjob</code>.</p>
        <div aria-label="Điều hướng chặng kiến thức">
          <div class="stage-bar">
            <div class="stage-bar-current">
              <span class="stage-bar-idx">Chặng ${padNum(currentStage.id)} / ${padNum(totalStages)}</span>
              <span class="stage-bar-title">${escapeHtml(currentStage.title.replace(/^Chặng \d+:\s*/, ""))}</span>
            </div>
            <div class="stage-bar-actions">
              <button type="button" class="ui-btn" ${prevId ? `onclick="selectStorageStage(${prevId})"` : 'disabled style="opacity:0.4;cursor:default;"'}>Trước</button>
              <button type="button" class="ui-btn" ${nextId ? `onclick="selectStorageStage(${nextId})"` : 'disabled style="opacity:0.4;cursor:default;"'}>Tiếp</button>
              <button type="button" class="ui-btn" id="stageDirectoryToggleBtn" aria-expanded="false" aria-controls="stageDirectoryPanel" onclick="toggleStageDirectory()">Danh sách chặng (${padNum(totalStages)})</button>
            </div>
          </div>
          <div class="stage-directory" id="stageDirectoryPanel" role="region" aria-label="Danh mục toàn bộ các chặng">
            ${stageRows}
          </div>
        </div>
      </header>
      ${bodyHtml}
    `;
  }

  function renderStorageTopic() {
    const totalStages = STORAGE_STAGES.length;
    const currentStage = STORAGE_STAGES.find(s => s.id === activeStorageStage) || STORAGE_STAGES[0];
    const prevId = activeStorageStage > 1 ? activeStorageStage - 1 : null;
    const nextId = activeStorageStage < totalStages ? activeStorageStage + 1 : null;
    const padNum = n => String(n).padStart(2, "0");

    const stageRows = STORAGE_STAGES.map(st => `
      <button type="button" class="stage-dir-item ${st.id === activeStorageStage ? 'active' : ''}" onclick="selectStorageStage(${st.id})">
        <span class="stage-dir-code">Chặng ${padNum(st.id)}</span>
        <span>${escapeHtml(st.title.replace(/^Chặng \d+:\s*/, ""))}</span>
        <span class="stage-dir-meta">${(st.id >= 1 && st.id <= 7) ? 'Đã có bài' : 'Chờ cập nhật'}</span>
      </button>
    `).join("");

    let bodyHtml = "";
    if (activeStorageStage === 1) {
      bodyHtml = renderStorageChang1();
    } else if (activeStorageStage === 2) {
      bodyHtml = renderStorageChang2();
    } else if (activeStorageStage === 3) {
      bodyHtml = renderStorageChang3();
    } else if (activeStorageStage === 4) {
      bodyHtml = renderStorageChang4();
    } else if (activeStorageStage === 5) {
      bodyHtml = renderStorageChang5();
    } else if (activeStorageStage === 6) {
      bodyHtml = renderStorageChang6();
    } else if (activeStorageStage === 7) {
      bodyHtml = renderStorageChang7();
    } else {
      bodyHtml = renderStorageChang1();
    }

    return `
      <header class="lesson-header">
        <div class="lesson-meta">
          <span>II. Data Engineering · D02 · Storage Layer</span>
          <a href="course-slides/08-storage-layer.pdf" target="_blank" rel="noopener">Slide gốc: 08-storage-layer.pdf (59 trang)</a>
        </div>
        <h1 class="lesson-title">Data Engineering — Storage Layer</h1>
        <p class="lesson-lead">Từ giới hạn vật lý của CPU Cache, RAM, SSD/HDD, Cloud Object Storage cho đến định dạng tuần tự hóa (Avro, Parquet, Arrow), kiến trúc Data Lakehouse (Delta Lake, Apache Iceberg, Apache Hudi) và Medallion Multi-hop.</p>
        <div aria-label="Điều hướng chặng kiến thức">
          <div class="stage-bar">
            <div class="stage-bar-current">
              <span class="stage-bar-idx">Chặng ${padNum(currentStage.id)} / ${padNum(totalStages)}</span>
              <span class="stage-bar-title">${escapeHtml(currentStage.title.replace(/^Chặng \d+:\s*/, ""))}</span>
            </div>
            <div class="stage-bar-actions">
              <button type="button" class="ui-btn" ${prevId ? `onclick="selectStorageStage(${prevId})"` : 'disabled style="opacity:0.4;cursor:default;"'}>Trước</button>
              <button type="button" class="ui-btn" ${nextId ? `onclick="selectStorageStage(${nextId})"` : 'disabled style="opacity:0.4;cursor:default;"'}>Tiếp</button>
              <button type="button" class="ui-btn" id="stageDirectoryToggleBtn" aria-expanded="false" aria-controls="stageDirectoryPanel" onclick="toggleStageDirectory()">Danh sách chặng (${padNum(totalStages)})</button>
            </div>
          </div>
          <div class="stage-directory" id="stageDirectoryPanel" role="region" aria-label="Danh mục toàn bộ các chặng">
            ${stageRows}
          </div>
        </div>
      </header>
      ${bodyHtml}
    `;
  }

  function renderPendingTopic(item, groupTitle) {
    const tocRows = (item.slideToc || []).map((section, idx) => `
      <tr>
        <td style="width:90px;color:var(--muted);">Mục 0${idx + 1}</td>
        <td><strong>${escapeHtml(section)}</strong></td>
      </tr>
    `).join("");

    const slideAction = item.slide
      ? `<a href="course-slides/${escapeHtml(item.slide)}" target="_blank" rel="noopener">Slide gốc: ${escapeHtml(item.slide)} (${item.pages} trang)</a>`
      : "";

    return `
      <header class="lesson-header">
        <div class="lesson-meta">
          <span>${escapeHtml(groupTitle)} · ${escapeHtml(item.code)}</span>
          ${slideAction}
        </div>
        <h1 class="lesson-title">${escapeHtml(item.title)}</h1>
        <p class="lesson-lead">Đề cương chi tiết học phần ${escapeHtml(item.code)} trích xuất từ ${item.slide ? `tài liệu Slide <code>course-slides/${escapeHtml(item.slide)}</code>` : `đề cương <code>FSDS-EDAI-DSAI-syllabus.md</code>`}.</p>
      </header>
      <div class="prose">
        <h2>Mục lục Học phần</h2>
        <div class="table-wrap">
          <table class="clean-table">
            <thead>
              <tr>
                <th>Thứ tự</th>
                <th>Chủ đề / Chương mục</th>
              </tr>
            </thead>
            <tbody>
              ${tocRows}
            </tbody>
          </table>
        </div>

        <h2>Thông số Đề cương</h2>
        <div class="table-wrap">
          <table class="clean-table">
            <tbody>
              <tr>
                <th style="width:180px;">Modules trọng tâm</th>
                <td>${escapeHtml(item.modules || "")}</td>
              </tr>
              <tr>
                <th>Bài thực hành (Lab)</th>
                <td>${escapeHtml(item.lab || "")}</td>
              </tr>
              <tr>
                <th>Tech Stack</th>
                <td><code>${escapeHtml(item.stack || "")}</code></td>
              </tr>
              ${item.slide ? `
              <tr>
                <th>Tài liệu Slide</th>
                <td><a href="course-slides/${escapeHtml(item.slide)}" target="_blank" rel="noopener"><code>course-slides/${escapeHtml(item.slide)}</code> (${item.pages} trang)</a></td>
              </tr>` : ""}
            </tbody>
          </table>
        </div>
        <p>Học phần này chưa có bài viết chi tiết. Xem bài đã xuất bản tại <a href="#topic=F01&stage=1" onclick="selectTopic('F01');return false;">F01 · Linux Fundamentals (Chặng 1 – Chặng 4)</a> hoặc <a href="#topic=D02&stage=1" onclick="selectTopic('D02');return false;">D02 · Storage Layer (Chặng 1 – Chặng 7)</a>.</p>
      </div>
    `;
  }

  /* ==========================================================================
     TOPBAR BREADCRUMB & SIDEBAR RAIL (OUTLINE + COLLAPSIBLE TRACK ACCORDIONS)
     ========================================================================== */
  function updateTopbarBreadcrumb() {
    const { group, item } = findTopicContext(activeTopic);
    const ol = document.getElementById("topbarBreadcrumbs");
    if (!ol) return;

    let stageCrumb = "";
    let stationCrumb = "";
    const topicStages = getTopicStages(activeTopic);
    if (topicStages.length > 0) {
      const st = topicStages.find(s => s.id === activeStorageStage) || topicStages[0];
      stageCrumb = `
        <li class="crumb-sep">/</li>
        <li class="crumb-item"><span class="crumb-current">Chặng ${st.id}: ${escapeHtml(st.shortTitle)}</span></li>
      `;
      const activeStations = getTopicStations(activeTopic, activeStorageStage);
      if (activeStations.length > 0) {
        const station = activeStations.find(s => s.id === activeStationId) || activeStations[0];
        const label = station.code === "Kết" ? "Tóm tắt" : (station.code === "Khung" ? "Bản đồ Khung" : `Trạm ${station.code}`);
        stationCrumb = `
          <li class="crumb-sep hide-mobile">/</li>
          <li class="crumb-item hide-mobile"><span id="topbarStationText">${escapeHtml(label)}</span></li>
        `;
      }
    }

    ol.innerHTML = `
      <li class="crumb-item crumb-track"><span>${escapeHtml(group.shortTitle)}</span></li>
      <li class="crumb-sep crumb-sep-track">/</li>
      <li class="crumb-item"><span class="${topicStages.length > 0 ? 'crumb-topic' : 'crumb-current'}">${escapeHtml(item.code)} · ${escapeHtml(item.title)}</span></li>
      ${stageCrumb}
      ${stationCrumb}
    `;
  }

  function renderSyllabus() {
    const rail = document.getElementById("syllabusRail");
    if (!rail) return;

    let outlineHtml = "";
    const activeStations = getTopicStations(activeTopic, activeStorageStage);
    if (activeStations.length > 0) {
      outlineHtml = `
        <section class="rail-outline-section" aria-label="Mục lục trên trang">
          <div class="rail-section-heading">
            <span>Mục lục ${activeTopic} · Chặng ${activeStorageStage}</span>
            <span id="railProgressPct">0%</span>
          </div>
          <ul class="rail-outline-list" id="railOutlineList">
            ${activeStations.map(st => `
              <li>
                <a href="#${st.id}" class="rail-outline-link" data-station-id="${st.id}" ${st.id === activeStationId ? 'aria-current="location"' : ''} onclick="jumpToStation('${st.id}');return false;">
                  <span class="rail-outline-code">${escapeHtml(st.code)}</span>
                  <span>${escapeHtml(st.title)}</span>
                </a>
              </li>
            `).join("")}
          </ul>
        </section>
      `;
    }

    const tracksHtml = SYLLABUS_GROUPS.map(group => {
      const isExpanded = expandedTracks.has(group.id);
      const itemsHtml = group.items.map(item => {
        const isActive = item.code === activeTopic;
        return `
          <button type="button" class="rail-item" ${isActive ? 'aria-current="page"' : ''} onclick="selectTopic('${item.code}')">
            <span class="rail-code">${escapeHtml(item.code)}</span>
            <span class="rail-item-title">${escapeHtml(item.title)}</span>
            <span class="rail-item-note">${escapeHtml(item.contentNote || (item.hasContent ? 'Đã có bài' : ''))}</span>
          </button>
        `;
      }).join("");

      return `
        <section class="track-group" id="card-${group.id}" data-expanded="${isExpanded ? 'true' : 'false'}">
          <button type="button" class="track-trigger" aria-expanded="${isExpanded ? 'true' : 'false'}" aria-controls="panel-${group.id}" onclick="toggleTrack('${group.id}')">
            <span>${escapeHtml(group.shortTitle)}</span>
            <span class="track-indicator" id="ind-${group.id}">${isExpanded ? '−' : '+'}</span>
          </button>
          <div class="track-panel-wrap" id="panel-${group.id}" ${isExpanded ? '' : 'inert'}>
            <div class="track-panel-inner">
              <div class="track-items">
                ${itemsHtml}
              </div>
            </div>
          </div>
        </section>
      `;
    }).join("");

    rail.innerHTML = `
      <div class="rail-top-bar">
        <div class="rail-brand-title">FSDS · EDAI · DSAI</div>
        <button type="button" class="rail-search-btn" onclick="openSearchModal()">
          <span>Tìm học phần, trạm...</span>
          <kbd class="shortcut-key">⌘K</kbd>
        </button>
      </div>

      ${outlineHtml}

      <div class="rail-section-heading"><span>Chương trình (26 Học phần)</span></div>
      <div class="track-list">
        ${tracksHtml}
      </div>
    `;
  }

  function toggleTrack(trackId) {
    if (expandedTracks.has(trackId)) {
      expandedTracks.delete(trackId);
    } else {
      expandedTracks.add(trackId);
    }
    const card = document.getElementById("card-" + trackId);
    const panel = document.getElementById("panel-" + trackId);
    const ind = document.getElementById("ind-" + trackId);
    const btn = card ? card.querySelector(".track-trigger") : null;
    const isExp = expandedTracks.has(trackId);
    if (card) card.dataset.expanded = isExp ? "true" : "false";
    if (btn) btn.setAttribute("aria-expanded", isExp ? "true" : "false");
    if (ind) ind.textContent = isExp ? "−" : "+";
    if (panel) {
      if (isExp) panel.removeAttribute("inert");
      else panel.setAttribute("inert", "");
    }
  }

  function jumpToStation(stationId) {
    activeStationId = stationId;
    document.body.classList.remove("mobile-rail-open");
    const target = document.getElementById(stationId);
    if (target) {
      target.scrollIntoView({ behavior: "smooth", block: "start" });
      target.focus({ preventScroll: true });
    }
    highlightActiveStation(stationId);
    history.replaceState(null, "", `#topic=${activeTopic}&stage=${activeStorageStage}&section=${stationId}`);
  }

  function highlightActiveStation(stationId) {
    activeStationId = stationId;
    document.querySelectorAll("#railOutlineList .rail-outline-link").forEach(a => {
      if (a.getAttribute("data-station-id") === stationId) {
        a.setAttribute("aria-current", "location");
      } else {
        a.removeAttribute("aria-current");
      }
    });
    const textEl = document.getElementById("topbarStationText");
    if (textEl) {
      const activeStations = getTopicStations(activeTopic, activeStorageStage);
      const st = activeStations.find(s => s.id === stationId);
      if (st) {
        textEl.textContent = st.code === "Kết" ? "Tóm tắt" : (st.code === "Khung" ? "Bản đồ Khung" : ("Trạm " + st.code));
      }
    }
  }

  function setupScrollSpy() {
    if (scrollObserver) {
      scrollObserver.disconnect();
      scrollObserver = null;
    }
    const activeStations = getTopicStations(activeTopic, activeStorageStage);
    if (!activeStations.length) return;

    const headings = activeStations
      .map(s => document.getElementById(s.id))
      .filter(Boolean);
    if (!headings.length) return;

    scrollObserver = new IntersectionObserver((entries) => {
      const visible = entries
        .filter(e => e.isIntersecting)
        .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (visible.length > 0) {
        highlightActiveStation(visible[0].target.id);
      }
    }, {
      rootMargin: "-64px 0px -68% 0px",
      threshold: [0, 1]
    });

    headings.forEach(h => scrollObserver.observe(h));
  }

  /* ==========================================================================
     MERMAID LIFECYCLE & CAMERA MOUNTING (RACE-SAFE)
     ========================================================================== */
  function initMermaidConfig() {
    if (!window.mermaid) return;
    const isLight = document.documentElement.classList.contains("light");
    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: "loose",
      theme: "base",
      themeVariables: {
        background: isLight ? "#FAF9F5" : "#181716",
        primaryColor: isLight ? "#EBE7DD" : "#252321",
        primaryTextColor: isLight ? "#181716" : "#ECEAE2",
        primaryBorderColor: isLight ? "#C96442" : "#D97757",
        lineColor: isLight ? "#68645B" : "#9A968C",
        secondaryColor: isLight ? "#F4F1EA" : "#1E1D1B",
        tertiaryColor: isLight ? "#EBE7DD" : "#252321",
        fontFamily: '"SFMono-Regular", "SF Mono", ui-monospace, Menlo, monospace',
        fontSize: "13.5px"
      }
    });
  }

  async function ensureMermaidRendered(safeId, expectedGen = mermaidRenderGeneration) {
    if (!window.mermaid) return;
    const item = window.__diagrams?.[safeId];
    if (!item) return;
    const vp = document.getElementById("mviewport-" + safeId);
    const tr = document.getElementById("mtransform-" + safeId);
    const lbl = document.getElementById("mzoom-label-" + safeId);
    if (!vp || !tr) return;

    const isLight = document.documentElement.classList.contains("light");
    const themeKey = isLight ? "light" : "dark";
    if (tr.getAttribute("data-rendered-theme") === themeKey && activeInlineCameras.has(safeId)) {
      requestAnimationFrame(() => {
        const cam = activeInlineCameras.get(safeId);
        if (cam) cam.fitToViewport();
      });
      return;
    }

    initMermaidConfig();
    const uid = "mgraph_" + safeId + "_" + (++mermaidUniqueCounter);
    try {
      const { svg } = await window.mermaid.render(uid, item.mermaid);
      if (expectedGen !== mermaidRenderGeneration || !tr.isConnected) return;

      const prevCam = activeInlineCameras.get(safeId);
      if (prevCam) {
        prevCam.dispose();
        activeInlineCameras.delete(safeId);
      }

      tr.innerHTML = svg;
      tr.setAttribute("data-rendered-theme", themeKey);
      const cam = createMermaidCamera(vp, tr, lbl);
      activeInlineCameras.set(safeId, cam);
    } catch (e) {
      console.warn("Mermaid render warning:", e);
    }
  }

  async function reRenderVisibleMermaidDiagrams() {
    if (!window.mermaid) return;
    const gen = ++mermaidRenderGeneration;
    document.querySelectorAll(".mermaid-transform").forEach(n => n.removeAttribute("data-rendered-theme"));
    const visibleCards = document.querySelectorAll('.visual-card[data-mode="mermaid"]');
    for (const card of visibleCards) {
      if (gen !== mermaidRenderGeneration) return;
      const safeId = card.id.replace(/^vcard-/, "");
      await ensureMermaidRendered(safeId, gen);
    }
    if (document.getElementById("expandModal").classList.contains("open") && currentExpandMode === "mermaid") {
      await renderExpandModalContent();
    }
  }

  /* ==========================================================================
     INTERACTIVE GLOSSARY SCANNER & FROSTED-GLASS POPOVER CONTROLLER
     ========================================================================== */
  const GLOSSARY_DB = (HUB_DATA && HUB_DATA.glossary && HUB_DATA.glossary.entries) ? HUB_DATA.glossary.entries : {};
  const GLOSSARY_LOOKUP = (HUB_DATA && HUB_DATA.glossary && HUB_DATA.glossary.lookup) ? HUB_DATA.glossary.lookup : {};
  let activeGlossaryAnchor = null;
  let activeGlossaryTermId = null;
  let glossaryPinned = false;
  let glossaryOpenTimer = null;
  let glossaryCloseTimer = null;

  function normalizeGlossaryKey(str) {
    if (!str) return "";
    let s = String(str).normalize("NFC").trim().replace(/\s+/g, " ");
    s = s.replace(/^[\s:;.,!?()\[\]"\x27“”‘’—–\-•▸]+|[\s:;.,!?()\[\]"\x27“”‘’—–\-]+$/g, "");
    return s.toLowerCase();
  }

  function resolveGlossaryTermId(rawText) {
    const k = normalizeGlossaryKey(rawText);
    if (!k || k.length < 2) return null;
    if (GLOSSARY_LOOKUP[k]) return GLOSSARY_LOOKUP[k];
    const noColon = normalizeGlossaryKey(k.replace(/:$/, ""));
    if (GLOSSARY_LOOKUP[noColon]) return GLOSSARY_LOOKUP[noColon];
    return null;
  }

  function bindGlossaryTerms(container) {
    if (!container) return;
    const candidates = container.querySelectorAll(".prose strong, .prose code, .callout strong, .callout code, .data-table td strong, .data-table td code, .lesson-lead strong, .lesson-lead code");
    candidates.forEach((el) => {
      if (el.closest("pre, .ascii-diagram, .mermaid-viewer, .pic-viewer, .visual-header, .stage-bar, .stage-dir-grid, a, button, h1, h2, h3, h4")) {
        return;
      }
      if (el.querySelector(".glossary-term")) return;
      const text = (el.textContent || "").trim();
      const termId = resolveGlossaryTermId(text);
      if (!termId || !GLOSSARY_DB[termId]) return;
      el.classList.add("glossary-term");
      el.setAttribute("data-term-id", termId);
      el.setAttribute("data-term-raw", text.slice(0, 64));
      if (!el.hasAttribute("tabindex")) {
        el.setAttribute("tabindex", "0");
      }
      el.setAttribute("role", "button");
      el.setAttribute("aria-haspopup", "dialog");
    });
  }

  function positionGlossaryPopover() {
    const pop = document.getElementById("glossaryPopover");
    if (!pop || !activeGlossaryAnchor || !pop.classList.contains("open")) return;
    const vw = document.documentElement.clientWidth || window.innerWidth;
    const vh = document.documentElement.clientHeight || window.innerHeight;
    if (vw <= 680) {
      pop.style.left = "";
      pop.style.top = "";
      return;
    }
    const rect = activeGlossaryAnchor.getBoundingClientRect();
    if (rect.width === 0 && rect.height === 0) return;

    const margin = 14;
    const topSafe = 54;
    const gap = 10;
    const popW = pop.offsetWidth || Math.min(440, vw - 28);
    const popH = pop.offsetHeight || 320;

    let left = rect.left + (rect.width / 2) - (popW / 2);
    left = Math.max(margin, Math.min(left, vw - popW - margin));

    let top = rect.bottom + gap;
    if (top + popH > vh - margin && rect.top - gap - popH >= topSafe) {
      top = rect.top - gap - popH;
    } else if (top + popH > vh - margin) {
      top = Math.max(topSafe, vh - popH - margin);
    }
    top = Math.max(topSafe, Math.min(top, Math.max(topSafe, vh - popH - margin)));

    pop.style.left = Math.round(left) + "px";
    pop.style.top = Math.round(top) + "px";
  }

  function renderGlossaryPopoverContent(termId, matchedText) {
    const entry = GLOSSARY_DB[termId];
    if (!entry) return false;
    document.getElementById("glossaryPopCat").textContent = entry.category || "TECHNICAL TERM";
    const matchEl = document.getElementById("glossaryPopMatch");
    const cleanMatch = (matchedText || entry.name || "").trim();
    matchEl.textContent = cleanMatch.length > 34 ? cleanMatch.slice(0, 32) + "…" : cleanMatch;
    document.getElementById("glossaryPopTitle").textContent = entry.name || termId;
    document.getElementById("glossaryPopIntuition").textContent = entry.intuition || "";
    document.getElementById("glossaryPopMechanism").textContent = entry.mechanism || "";

    const ex = entry.example || {};
    document.getElementById("glossaryPopCode").textContent = ex.code || "";
    document.getElementById("glossaryPopNote").textContent = ex.note || "";

    const relWrap = document.getElementById("glossaryPopRelatedWrap");
    const relBox = document.getElementById("glossaryPopRelated");
    const related = Array.isArray(entry.related) ? entry.related : [];
    if (related.length > 0) {
      relWrap.style.display = "";
      relBox.innerHTML = related.map((relName) => {
        const relId = resolveGlossaryTermId(relName);
        if (relId && GLOSSARY_DB[relId]) {
          return `<button type="button" class="glossary-pop-chip" data-jump-term="${escapeHtml(relId)}" data-jump-label="${escapeHtml(relName)}">${escapeHtml(relName)}</button>`;
        }
        return `<span class="glossary-pop-chip" style="cursor:default;opacity:0.8;">${escapeHtml(relName)}</span>`;
      }).join("");
    } else {
      relWrap.style.display = "none";
      relBox.innerHTML = "";
    }

    const pinStateEl = document.getElementById("glossaryPopPinState");
    if (glossaryPinned) {
      pinStateEl.textContent = "Đã ghim cố định";
      pinStateEl.classList.add("is-pinned");
    } else {
      pinStateEl.textContent = "Click để ghim";
      pinStateEl.classList.remove("is-pinned");
    }
    return true;
  }

  function openGlossaryPopover(anchorEl, termId, pin = false, matchedOverride = null) {
    if (!anchorEl || !termId || !GLOSSARY_DB[termId]) return;
    clearTimeout(glossaryOpenTimer);
    clearTimeout(glossaryCloseTimer);

    if (activeGlossaryAnchor && activeGlossaryAnchor !== anchorEl) {
      activeGlossaryAnchor.classList.remove("glossary-active", "glossary-pinned");
    }
    activeGlossaryAnchor = anchorEl;
    activeGlossaryTermId = termId;
    glossaryPinned = Boolean(pin);

    anchorEl.classList.add("glossary-active");
    anchorEl.classList.toggle("glossary-pinned", glossaryPinned);

    const matchedText = matchedOverride || anchorEl.getAttribute("data-term-raw") || anchorEl.textContent || "";
    renderGlossaryPopoverContent(termId, matchedText);

    const pop = document.getElementById("glossaryPopover");
    pop.classList.add("open");
    pop.classList.toggle("pinned", glossaryPinned);
    pop.setAttribute("aria-hidden", "false");
    positionGlossaryPopover();
    requestAnimationFrame(positionGlossaryPopover);
  }

  function closeGlossaryPopover(force = false) {
    if (glossaryPinned && !force) return;
    clearTimeout(glossaryOpenTimer);
    clearTimeout(glossaryCloseTimer);
    const pop = document.getElementById("glossaryPopover");
    if (pop) {
      pop.classList.remove("open", "pinned");
      pop.setAttribute("aria-hidden", "true");
    }
    if (activeGlossaryAnchor) {
      activeGlossaryAnchor.classList.remove("glossary-active", "glossary-pinned");
    }
    activeGlossaryAnchor = null;
    activeGlossaryTermId = null;
    glossaryPinned = false;
  }

  function initGlossarySystem() {
    const container = document.getElementById("articleContainer");
    const pop = document.getElementById("glossaryPopover");
    const closeBtn = document.getElementById("glossaryPopCloseBtn");
    if (!container || !pop) return;

    container.addEventListener("mouseover", (e) => {
      if (glossaryPinned) return;
      const termEl = e.target.closest(".glossary-term");
      if (!termEl) return;
      clearTimeout(glossaryCloseTimer);
      const termId = termEl.getAttribute("data-term-id");
      if (!termId) return;
      if (activeGlossaryAnchor === termEl && pop.classList.contains("open")) return;
      clearTimeout(glossaryOpenTimer);
      glossaryOpenTimer = setTimeout(() => {
        openGlossaryPopover(termEl, termId, false);
      }, 110);
    });

    container.addEventListener("mouseout", (e) => {
      if (glossaryPinned) return;
      const termEl = e.target.closest(".glossary-term");
      if (!termEl) return;
      const rel = e.relatedTarget;
      if (rel && (termEl.contains(rel) || pop.contains(rel))) return;
      clearTimeout(glossaryOpenTimer);
      clearTimeout(glossaryCloseTimer);
      glossaryCloseTimer = setTimeout(() => {
        closeGlossaryPopover(false);
      }, 190);
    });

    container.addEventListener("click", (e) => {
      const termEl = e.target.closest(".glossary-term");
      if (!termEl) return;
      e.stopPropagation();
      const termId = termEl.getAttribute("data-term-id");
      if (!termId) return;
      if (activeGlossaryAnchor === termEl && glossaryPinned && pop.classList.contains("open")) {
        closeGlossaryPopover(true);
      } else {
        openGlossaryPopover(termEl, termId, true);
      }
    });

    container.addEventListener("keydown", (e) => {
      const termEl = e.target.closest(".glossary-term");
      if (!termEl) return;
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        e.stopPropagation();
        const termId = termEl.getAttribute("data-term-id");
        if (termId) openGlossaryPopover(termEl, termId, true);
      }
    });

    pop.addEventListener("mouseenter", () => {
      clearTimeout(glossaryCloseTimer);
    });

    pop.addEventListener("mouseleave", (e) => {
      if (glossaryPinned) return;
      const rel = e.relatedTarget;
      if (rel && activeGlossaryAnchor && activeGlossaryAnchor.contains(rel)) return;
      clearTimeout(glossaryCloseTimer);
      glossaryCloseTimer = setTimeout(() => {
        closeGlossaryPopover(false);
      }, 180);
    });

    pop.addEventListener("click", (e) => {
      e.stopPropagation();
      const chip = e.target.closest("[data-jump-term]");
      if (chip && activeGlossaryAnchor) {
        const nextId = chip.getAttribute("data-jump-term");
        const nextLbl = chip.getAttribute("data-jump-label") || nextId;
        if (nextId && GLOSSARY_DB[nextId]) {
          openGlossaryPopover(activeGlossaryAnchor, nextId, true, nextLbl);
        }
      }
    });

    if (closeBtn) {
      closeBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        closeGlossaryPopover(true);
      });
    }

    document.addEventListener("click", (e) => {
      if (!pop.classList.contains("open")) return;
      if (pop.contains(e.target)) return;
      if (e.target.closest && e.target.closest(".glossary-term")) return;
      closeGlossaryPopover(true);
    });

    window.addEventListener("scroll", () => {
      if (pop.classList.contains("open")) {
        positionGlossaryPopover();
      }
    }, { passive: true });

    window.addEventListener("resize", () => {
      if (pop.classList.contains("open")) {
        positionGlossaryPopover();
      }
    });
  }

  /* ==========================================================================
     MAIN CONTROLLER & NAVIGATION
     ========================================================================== */
  function renderMain(preserveScroll = false) {
    closeGlossaryPopover(true);
    disposeAllInlineCameras();
    mermaidRenderGeneration++;
    window.__diagrams = {};
    syncGlobalVisualButtons();
    const container = document.getElementById("articleContainer");
    if (activeTopic === "D02") {
      container.innerHTML = renderStorageTopic();
    } else if (activeTopic === "F01") {
      container.innerHTML = renderLinuxTopic();
    } else {
      const { group, item } = findTopicContext(activeTopic);
      container.innerHTML = renderPendingTopic(item, group.title);
    }
    bindGlossaryTerms(container);
    updateTopbarBreadcrumb();
    if (!preserveScroll) {
      window.scrollTo(0, 0);
    }
    setupScrollSpy();
    updateReadingProgress();
    if (defaultVisualMode === "mermaid") {
      reRenderVisibleMermaidDiagrams();
    } else if (defaultVisualMode === "pic") {
      document.querySelectorAll('.visual-card[data-mode="pic"]').forEach(card => {
        const safeId = card.id.replace(/^vcard-/, "");
        ensurePictureRendered(safeId);
      });
    }
  }

  function selectTopic(code, stageId = null, sectionId = null) {
    const { group } = findTopicContext(code);
    expandedTracks.add(group.id);
    const topicChanged = (activeTopic !== code);
    activeTopic = code;
    if (stageId !== null) {
      activeStorageStage = stageId;
    } else if (topicChanged) {
      activeStorageStage = 1;
    }
    const stages = getTopicStages(activeTopic);
    if (stages.length > 0 && !stages.some(s => s.id === activeStorageStage)) {
      activeStorageStage = stages[0].id;
    }
    const stations = getTopicStations(activeTopic, activeStorageStage);
    if (sectionId !== null) {
      activeStationId = sectionId;
    } else if (stations.length > 0) {
      activeStationId = stations[0].id;
    }
    document.body.classList.remove("mobile-rail-open");
    renderSyllabus();
    renderMain(Boolean(sectionId));
    if (sectionId) {
      setTimeout(() => jumpToStation(sectionId), 30);
    } else {
      history.replaceState(null, "", `#topic=${activeTopic}&stage=${activeStorageStage}`);
    }
  }

  function selectStorageStage(stageId) {
    activeStorageStage = stageId;
    const stations = getTopicStations(activeTopic, stageId);
    if (stations.length > 0) {
      activeStationId = stations[0].id;
    }
    document.body.classList.remove("mobile-rail-open");
    renderSyllabus();
    renderMain();
    history.replaceState(null, "", `#topic=${activeTopic}&stage=${activeStorageStage}`);
  }

  /* ==========================================================================
     COMMAND PALETTE SEARCH (⌘K / /)
     ========================================================================== */
  let cmdSelectedIndex = 0;
  let currentCmdMatches = [];

  function buildSearchCatalog() {
    const entries = [];
    for (const st of LINUX_CHANG1_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "I. Engineering Foundation / F01 · Linux Fundamentals / Chặng 1",
        topic: "F01",
        stage: 1,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} linux gnu kernel open source distro ubuntu rhel kali mint terminal shell bash program process system call hardware grep app.log`)
      });
    }
    for (const st of LINUX_CHANG2_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "I. Engineering Foundation / F01 · Linux Fundamentals / Chặng 2",
        topic: "F01",
        stage: 2,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} process pid uid gid user group working directory environment path open files everything is a file inode vfs root directory /bin /sbin /usr /etc /var/log /tmp /proc`)
      });
    }
    for (const st of LINUX_CHANG3_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "I. Engineering Foundation / F01 · Linux Fundamentals / Chặng 3",
        topic: "F01",
        stage: 3,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} ipc interprocess communication stdin stdout stderr file descriptor 0 1 2 pipe redirection dup2 2>&1`)
      });
    }
    for (const st of LINUX_CHANG4_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "I. Engineering Foundation / F01 · Linux Fundamentals / Chặng 4",
        topic: "F01",
        stage: 4,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} shell bash scripting shebang chmod compilation gcc object file linker makefile target prerequisites recipe tab cron crond crontab cronjob`)
      });
    }
    for (const stg of LINUX_STAGES) {
      entries.push({
        kind: "Lộ trình Chặng",
        title: `F01 · ${stg.title}`,
        sub: "I. Engineering Foundation / Linux Fundamentals",
        topic: "F01",
        stage: stg.id,
        section: null,
        keywords: normalizeSearch(`F01 linux bash ${stg.title}`)
      });
    }
    for (const st of STORAGE_CHANG1_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "II. Data Engineering / D02 · Storage Layer / Chặng 1",
        topic: "D02",
        stage: 1,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} storage ram ssd hdd iops oltp olap spill to disk`)
      });
    }
    for (const st of STORAGE_CHANG2_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "II. Data Engineering / D02 · Storage Layer / Chặng 2",
        topic: "D02",
        stage: 2,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} file block object s3 ebs parquet avro orc arrow dremel snappy zstd gzip bzip2 splittable zero copy`)
      });
    }
    for (const st of STORAGE_CHANG3_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "II. Data Engineering / D02 · Storage Layer / Chặng 3",
        topic: "D02",
        stage: 3,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} hdfs namenode datanode replication erasure coding rack topology data local redis memcached rocksdb lsm kafka cdc append only replay data warehouse acid oltp olap colossus snowflake micro partition`)
      });
    }
    for (const st of STORAGE_CHANG4_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "II. Data Engineering / D02 · Storage Layer / Chặng 4",
        topic: "D02",
        stage: 4,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} conceptual logical physical inmon 3nf kimball star snowflake obt olap cube data vault hub link satellite fact dimension grain additive surrogate key scd type 1 type 2 type 3 bus matrix conformed dimensions`)
      });
    }
    for (const st of STORAGE_CHANG5_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "II. Data Engineering / D02 · Storage Layer / Chặng 5",
        topic: "D02",
        stage: 5,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} data lake data swamp schema on read schema on write elt etl dark data worn worm zombie writes partial files hive table format schema drift gdpr eventual consistency strong consistency object versioning data catalog lineage observability zoning raw cleansed curated data contracts schema registry backward forward full single source of truth`)
      });
    }
    for (const st of STORAGE_CHANG6_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "II. Data Engineering / D02 · Storage Layer / Chặng 6",
        topic: "D02",
        stage: 6,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} data lakehouse open table formats delta lake apache iceberg apache hudi delta log checkpoint manifest list manifest file cas timeline file groups record level index bloom filter bucket index uniform xtable acid mvcc occ nbcc time travel change data feed cdf schema enforcement schema evolution column id copy on write cow merge on read mor positional delete equality delete compaction bin packing small file problem hidden partitioning partition evolution z ordering liquid clustering hilbert curve deletion vectors roaring bitmap vacuum expire snapshots gdpr`)
      });
    }
    for (const st of STORAGE_CHANG7_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "II. Data Engineering / D02 · Storage Layer / Chặng 7",
        topic: "D02",
        stage: 7,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} multi hop medallion architecture bronze silver gold infancy teenage maturity quality gating permissive _corrupt _debug quarantine deduplication 3nf scd2 star schema obt streaming medallion mergeSchema check constraints dlt expect write audit publish wap undercurrents unity catalog openlineage lineage single source of truth 40 buckets row level security column masking gdpr finops hot warm cold glacier ephemeral compute bottom up blueprint`)
      });
    }
    for (const stg of STORAGE_STAGES) {
      entries.push({
        kind: (stg.id >= 1 && stg.id <= 7) ? "Chặng bài đọc" : "Lộ trình Chặng",
        title: `D02 · ${stg.title}`,
        sub: "II. Data Engineering / Storage Layer",
        topic: "D02",
        stage: stg.id,
        section: null,
        keywords: normalizeSearch(`D02 storage ${stg.title}`)
      });
    }
    for (const g of SYLLABUS_GROUPS) {
      for (const it of g.items) {
        entries.push({
          kind: it.hasContent ? "Học phần" : "Đề cương Slide",
          title: `${it.code} · ${it.title}`,
          sub: `${g.shortTitle} · ${it.stack || ""}`,
          topic: it.code,
          stage: 1,
          section: null,
          keywords: normalizeSearch(`${it.code} ${it.title} ${it.modules || ""} ${it.stack || ""} ${(it.slideToc || []).join(" ")}`)
        });
      }
    }
    return entries;
  }

  const SEARCH_CATALOG = buildSearchCatalog();

  function openSearchModal() {
    const modal = document.getElementById("searchModal");
    const input = document.getElementById("cmdSearchInput");
    modal.classList.add("open");
    input.value = "";
    cmdSelectedIndex = 0;
    renderSearchResults("");
    setTimeout(() => input.focus(), 20);
  }

  function closeSearchModal() {
    document.getElementById("searchModal").classList.remove("open");
  }

  function renderSearchResults(query) {
    const q = normalizeSearch(query);
    currentCmdMatches = SEARCH_CATALOG.filter(item => !q || item.keywords.includes(q)).slice(0, 14);
    if (cmdSelectedIndex >= currentCmdMatches.length) cmdSelectedIndex = 0;

    const list = document.getElementById("cmdResultsList");
    if (!currentCmdMatches.length) {
      list.innerHTML = `<li style="padding:14px;color:var(--muted);font-size:12.5px;">Không tìm thấy kết quả khớp với "${escapeHtml(query)}".</li>`;
      return;
    }

    list.innerHTML = currentCmdMatches.map((m, idx) => `
      <li>
        <button type="button" class="cmd-item ${idx === cmdSelectedIndex ? 'selected' : ''}" onclick="executeSearchResult(${idx})">
          <span class="cmd-item-left">
            <strong>${escapeHtml(m.title)}</strong>
            <span class="cmd-item-sub">${escapeHtml(m.sub)}</span>
          </span>
          <span class="cmd-item-kind">${escapeHtml(m.kind)}</span>
        </button>
      </li>
    `).join("");
  }

  function executeSearchResult(idx) {
    const match = currentCmdMatches[idx];
    if (!match) return;
    closeSearchModal();
    selectTopic(match.topic, match.stage, match.section);
  }

  document.getElementById("cmdSearchInput").addEventListener("input", (e) => {
    cmdSelectedIndex = 0;
    renderSearchResults(e.target.value);
  });

  document.getElementById("cmdSearchInput").addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      if (currentCmdMatches.length) {
        cmdSelectedIndex = (cmdSelectedIndex + 1) % currentCmdMatches.length;
        renderSearchResults(e.target.value);
      }
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      if (currentCmdMatches.length) {
        cmdSelectedIndex = (cmdSelectedIndex - 1 + currentCmdMatches.length) % currentCmdMatches.length;
        renderSearchResults(e.target.value);
      }
    } else if (e.key === "Enter") {
      e.preventDefault();
      executeSearchResult(cmdSelectedIndex);
    }
  });

  /* ==========================================================================
     SIDEBAR, THEME & KEYBOARD SHORTCUTS
     ========================================================================== */
  function toggleSidebar() {
    const btn = document.getElementById("railToggleBtn");
    const rail = document.getElementById("syllabusRail");
    if (window.innerWidth <= 900) {
      const open = document.body.classList.toggle("mobile-rail-open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      rail.removeAttribute("inert");
    } else {
      const collapsed = document.body.classList.toggle("rail-collapsed");
      btn.setAttribute("aria-expanded", collapsed ? "false" : "true");
      if (collapsed) rail.setAttribute("inert", "");
      else rail.removeAttribute("inert");
    }
  }

  document.getElementById("railToggleBtn").addEventListener("click", toggleSidebar);
  document.getElementById("searchTriggerBtn").addEventListener("click", openSearchModal);
  document.getElementById("searchModal").addEventListener("click", closeSearchModal);
  document.getElementById("expandModal").addEventListener("click", closeExpandModal);
  document.getElementById("expandCloseBtn").addEventListener("click", closeExpandModal);

  function applyTheme(mode) {
    const isLight = (mode === "light");
    document.documentElement.classList.toggle("light", isLight);
    document.documentElement.classList.toggle("dark", !isLight);
    document.getElementById("themeToggleLabel").textContent = isLight ? "Giao diện: Sáng" : "Giao diện: Tối";
    localStorage.setItem("fsds-theme", isLight ? "light" : "dark");
    reRenderVisibleMermaidDiagrams();
  }

  document.getElementById("themeToggleBtn").addEventListener("click", () => {
    const isLight = document.documentElement.classList.contains("light");
    applyTheme(isLight ? "dark" : "light");
  });

  document.addEventListener("click", () => closeAllVisualMenus());

  document.addEventListener("keydown", (e) => {
    if (e.isComposing) return;
    const tag = (e.target && e.target.tagName) ? e.target.tagName.toLowerCase() : "";
    const isTyping = tag === "input" || tag === "textarea" || (e.target && e.target.isContentEditable);

    if (e.key === "Escape") {
      closeAllVisualMenus();
      if (document.getElementById("glossaryPopover").classList.contains("open")) {
        closeGlossaryPopover(true);
        return;
      }
      if (document.getElementById("searchModal").classList.contains("open")) {
        closeSearchModal();
        return;
      }
      if (document.getElementById("expandModal").classList.contains("open")) {
        closeExpandModal();
        return;
      }
    }

    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      openSearchModal();
      return;
    }

    if (!isTyping && e.key === "/") {
      e.preventDefault();
      openSearchModal();
      return;
    }

    if (!isTyping && (e.key === "[" || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "b"))) {
      e.preventDefault();
      toggleSidebar();
    }
  });

  function updateReadingProgress() {
    const doc = document.documentElement;
    const max = Math.max(1, doc.scrollHeight - window.innerHeight);
    const pct = Math.min(100, Math.max(0, Math.round((window.scrollY / max) * 100)));
    document.getElementById("progressBar").style.width = pct + "%";
    const railPct = document.getElementById("railProgressPct");
    if (railPct) railPct.textContent = pct + "%";
  }

  window.addEventListener("scroll", updateReadingProgress, { passive: true });
  window.addEventListener("resize", () => {
    if (window.innerWidth <= 900) {
      document.getElementById("syllabusRail").removeAttribute("inert");
    } else if (document.body.classList.contains("rail-collapsed")) {
      document.getElementById("syllabusRail").setAttribute("inert", "");
    }
  });

  const savedTheme = localStorage.getItem("fsds-theme") || "dark";
  applyTheme(savedTheme);

  const hashParams = new URLSearchParams(window.location.hash.replace(/^#/, ""));
  if (hashParams.get("topic")) activeTopic = hashParams.get("topic");
  if (hashParams.get("stage")) activeStorageStage = Number(hashParams.get("stage")) || 1;
  if (hashParams.get("section")) activeStationId = hashParams.get("section");

  initGlossarySystem();
  renderSyllabus();
  renderMain(Boolean(hashParams.get("section")));
  if (hashParams.get("section")) {
    setTimeout(() => jumpToStation(hashParams.get("section")), 50);
  }
  </script>
  <script type="module">
    import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
    window.mermaid = mermaid;
    initMermaidConfig();
    reRenderVisibleMermaidDiagrams();
  </script>
</body>
</html>
"""


def main():
    storage_ascii = build_storage_ascii_diagrams()

    storage_mermaid = {
        "0.1": """flowchart LR
    S1["CHẶNG 1–2: Vật lý & Định dạng Tệp<br/>• Đơn #8888 trên RAM (100 ns) -> SSD (100 µs)<br/>• OLTP Row (Avro) -> OLAP Columnar (Parquet)<br/>• In-Memory Zero-Copy Apache Arrow"]
    S2["CHẶNG 3–4: Hạ tầng Phân tán & Data Modeling<br/>• HDFS (x3) / Streaming Kafka CDC Append-only<br/>• Data Warehouse + Kimball Star Schema / SCD2<br/>• Đụng trần 3 giới hạn: Phi cấu trúc, Giá & Đóng kín"]
    S3["CHẶNG 5–6: Từ Data Lake/Swamp lên Lakehouse<br/>• S3/GCS ($0.02/GB) -> Data Swamp (3 Tooling Gaps)<br/>• Open Table Formats: Delta Lake / Iceberg / Hudi<br/>• ACID, Time Travel, COW/MOR, Compaction, Z-Order"]
    S4["CHẶNG 7: Multi-Hop Medallion & Governance<br/>• Tinh chế: Bronze (Raw) -> Silver (3NF) -> Gold (Star/OBT)<br/>• Undercurrents: Unity Catalog, Lineage, RLS/Masking<br/>• Cloud FinOps: Tiering Hot/Warm/Cold (1/17 giá)"]
    S1 --> S2 --> S3 --> S4""",

        "1.1": """flowchart TD
    subgraph CPU_RAM ["Tầng Vi xử lý & Bộ nhớ Khả biến (Volatile)"]
        L1["L1 / L2 / L3 CPU Cache<br/>Độ trễ: ~1–10 ns | Băng thông: ~1 TB/s | On-die"]
        RAM["RAM (DDR5 / DRAM)<br/>Độ trễ: ~100 ns (0.1 µs) | Băng thông: ~100 GB/s | ~$10/GB"]
    end
    subgraph LOCAL_DISK ["Tầng Mạng LAN & Đĩa Cục bộ (Nonvolatile)"]
        NET["Mạng nội bộ 1 Gbps (~10 µs)<br/>Memcached LAN packet"]
        SSD["NVMe SSD / Flash (~100 µs | ~4 GB/s | ~$0.20/GB)<br/>RocksDB Read & PostgreSQL INSERT (~1 ms)"]
        HDD["Đĩa từ cơ học HDD (~4–10 ms | 200–300 MB/s | ~$0.03/GB)<br/>Giới hạn vật lý: ~100 IOPS (Seek)"]
    end
    subgraph CLOUD_TIER ["Tầng Lưu trữ Đám mây & Lưu trữ Lạnh (Durability 11 Nines)"]
        OBJ["Cloud Object Storage - S3 / ADLS / GCS<br/>Độ trễ: ~100 ms | Băng thông song song: ~3 GB/s* | ~$0.02/GB/tháng"]
        ARC["Cloud Archival - Glacier / Tape<br/>Độ trễ phục hồi: ~12 giờ | Giá: ~$0.004/GB/tháng (rẻ bằng 1/17)"]
    end
    L1 -->|"Chậm hơn ~10–100x"| RAM
    RAM -->|"Qua mạng LAN"| NET
    NET -->|"Chậm hơn RAM ~1.000x"| SSD
    SSD -->|"Chậm hơn SSD ~40–100x"| HDD
    HDD -->|"Đọc song song qua WAN"| OBJ
    OBJ -->|"Hạ tầng lưu trữ lạnh"| ARC""",

        "1.2": """flowchart TD
    IN["Dữ liệu 10 triệu đơn hàng đẩy vào RAM<br/>của Node tính toán Apache Spark"] --> CHECK{"Kiểm tra dung lượng<br/>RAM khả dụng?"}
    CHECK -->|"Đủ dung lượng RAM"| FAST["Xử lý In-Memory tốc độ ~100 ns (~100 GB/s)<br/>Hoàn tất cực nhanh"]
    CHECK -->|"Vượt quá RAM (JOIN / GROUP BY quá lớn)"| SPILL["SPILL-TO-DISK<br/>Tràn bộ nhớ xuống đĩa cứng cục bộ SSD / HDD"]
    SPILL --> PENALTY["Hệ quả kỹ thuật:<br/>1. Tốc độ rơi tự do: 100 ns -> 100 µs (SSD, chậm 1.000x) hoặc 4–10 ms (HDD, chậm 100.000x)<br/>2. Tốn CPU tuần tự hóa (Serialize) xuống đĩa rồi đọc ngược lên"]""",

        "1.3": """flowchart LR
    subgraph SEEK ["1. RANDOM SEEK (Truy xuất ngẫu nhiên từng dòng)"]
        direction TB
        S1["Đơn #12"] -->|"Di chuyển đầu đọc<br/>Seek 4–10 ms"| S2["Đơn #8888"]
        S2 -->|"Di chuyển đầu đọc<br/>Seek 4–10 ms"| S1
        S_NOTE["Nghẽn cổ chai:<br/>Bị bóp nghẹt bởi giới hạn ~100 IOPS"]
    end
    subgraph SCAN ["2. SEQUENTIAL SCAN (Quét tuần tự liền mạch)"]
        direction TB
        C1["Đơn #8886"] --> C2["Đơn #8887"] --> C3["Đơn #8888 ..."]
        C_NOTE["Tối ưu hóa:<br/>Định vị 1 lần, đọc trượt 200–300 MB/s<br/>Tận dụng tối đa Maximum Bandwidth"]
    end""",

        "1.4": """flowchart LR
    HOT["HOT TIER (Lưu trữ Nóng)<br/>• Phần cứng: RAM / SSD<br/>• Giá: $0.20 – $10 / GB<br/>• Độ trễ: 100 ns – 100 µs<br/>• Đơn #8888 vừa đặt / đệm EMR HDFS"]
    WARM["WARM TIER (Lưu trữ Ấm)<br/>• Phần cứng: Cloud Object (S3/GCS)<br/>• Giá: ~$0.02 / GB / tháng<br/>• Độ trễ: ~100 ms<br/>• Lịch sử đơn hàng chạy báo cáo tuần"]
    COLD["COLD / ARCHIVAL (Lưu trữ Lạnh)<br/>• Phần cứng: Glacier / Tape<br/>• Giá: ~$0.004 / GB / tháng<br/>• Độ trễ: ~12 giờ chờ<br/>• Hóa đơn 3–10 năm kiểm toán pháp lý"]
    HOT -->|"Giảm nhiệt độ dữ liệu"| WARM -->|"Lưu trữ dài hạn"| COLD""",

        "1.5": """flowchart LR
    subgraph OLTP ["HỆ THỐNG NGUỒN (SOURCE SYSTEM - OLTP)"]
        T1["Máy POS / App Bán Hàng / PostgreSQL"]
        T2["• Mục tiêu: Ghi nhận giao dịch Đơn #8888<br/>• Thao tác: INSERT / UPDATE / đọc vài dòng<br/>• Độ trễ yêu cầu: Cực thấp (~1 ms insert)<br/>• Định dạng: Lưu theo DÒNG (Row-oriented)<br/>• Mô hình: Chuẩn hóa (Normalized) nhiều bảng<br/>• Phần cứng: NVMe SSD / Block Storage"]
        T1 --- T2
    end
    subgraph OLAP ["HỆ THỐNG LƯU TRỮ PHÂN TÍCH (STORAGE SYSTEM - OLAP)"]
        A1["Data Warehouse / Data Lake / Lakehouse"]
        A2["• Mục tiêu: Quét 10 triệu đơn tính tổng doanh số<br/>• Thao tác: Quét tuần tự (Sequential Scan) lớn<br/>• Định dạng: Lưu theo CỘT (Columnar) & nén cao<br/>• Mô hình: Phi chuẩn hóa (Denormalized) giảm JOIN<br/>• Phần cứng: Cloud Object Storage + Cụm phân tán"]
        A1 --- A2
    end
    OLTP -->|"Tách biệt hệ thống<br/>(Ingestion / CDC / ETL)"| OLAP""",

        "2.1": """flowchart LR
    subgraph FILE ["1. FILE STORAGE (NAS / ext4 / NTFS)"]
        F1["/ (Root Directory)"] --> F2["KinhDoanh / 2026 / DonHang.csv"]
        F2 --- F3["• Duyệt con trỏ (pointer) qua từng cấp thư mục<br/>• Khóa nút thư mục mẹ & nghẽn inode khi > 10 triệu tệp"]
    end
    subgraph BLOCK ["2. BLOCK STORAGE (SAN / AWS EBS)"]
        B1["Tệp Dữ Liệu Lớn"] --> B2["[Block 1: 512KB] + [Block 2: 512KB] + [Block 3: 512KB]"]
        B2 --- B3["• Mỗi Block có Unique ID riêng, không có cây thư mục<br/>• Độ trễ < 1 ms (tới 256.000 IOPS) cho OLTP DB & VM"]
    end
    subgraph OBJECT ["3. OBJECT STORAGE (S3 / ADLS / GCS)"]
        O1["Bucket phẳng: ashley-data-lake"] --> O2["Object: ID (orders/8888.parquet)<br/>+ Metadata tùy biến + Data nhị phân bất biến"]
        O2 --- O3["• HTTP REST API, đọc/ghi luồng song song ~3 GB/s<br/>• Giá ~$0.02/GB/tháng, tách rời Compute & Storage"]
    end""",

        "2.2a": """flowchart TD
    TBL["BẢNG LOGIC (OrderID | Province | Amount)<br/>Row 1: 8886 | HaNoi | 5M<br/>Row 2: 8887 | DaNang | 12M<br/>Row 3: 8888 | BinhDuong | 15M"]
    subgraph ROW ["1. ROW-ORIENTED (CSV, JSONL, Apache Avro)"]
        R1["[8886 | HaNoi | 5M] -> [8887 | DaNang | 12M] -> [8888 | BinhDuong | 15M]"]
        R2["[+] Đọc/ghi trọn vẹn 1 bản ghi, tối ưu cho Kafka / CDC (Sync Marker 16-byte)<br/>[x] Tính tổng 1 cột vẫn phải quét qua toàn bộ các cột không liên quan"]
        R1 --- R2
    end
    subgraph COL ["2. COLUMN-ORIENTED (Apache Parquet, Apache ORC)"]
        C1["Row Group 1:<br/>• Cột OrderID: [8886, 8887, 8888]<br/>• Cột Province: [HaNoi, DaNang, BinhDuong]<br/>• Cột Amount: [5M, 12M, 15M]"]
        C2["[+] Cắt tỉa cột (Column Pruning) giảm 80–95% I/O<br/>[+] Cùng kiểu dữ liệu nằm sát nhau -> Nén RLE / Dictionary / Delta cực cao"]
        C1 --- C2
    end
    TBL -->|"Tuần tự hóa theo hàng"| ROW
    TBL -->|"Xoay trục theo cột trong Row Group"| COL""",

        "2.2b": """flowchart TD
    H["1. HEADER: Ký hiệu ma thuật 4-byte 'PAR1'"]
    subgraph RG1 ["2. ROW GROUP 1 (Phân đoạn hàng 1: 128 MB – 1 GB)"]
        RG1_C1["Column Chunk [OrderID]<br/>Page Header -> Data Page 1 -> Data Page 2"]
        RG1_C2["Column Chunk [Province]<br/>Dictionary Page -> Data Page 1 (RLE)"]
        RG1_C3["Column Chunk [Amount]<br/>Data Page 1 -> Data Page 2"]
    end
    subgraph RG2 ["3. ROW GROUP 2 (Nơi chứa Đơn hàng #8888)"]
        RG2_C1["Column Chunk [OrderID]<br/>Min: 5001 | Max: 9999"]
        RG2_C2["Column Chunk [Amount]<br/>Data Page 1 ..."]
    end
    F["4. FOOTER METADATA (Động cơ truy vấn đọc ĐẦU TIÊN qua HTTP Range Request)<br/>• Schema bảng & Google Dremel (Definition / Repetition Levels)<br/>• Thống kê Min / Max / Null Count từng Column Chunk (Data Skipping)<br/>• Con trỏ Byte Offset từng Row Group & Column Chunk + Độ dài Footer + 'PAR1'"]
    H --> RG1 --> RG2 --> F
    F -.->|"1. Đọc Footer trước để lọc Row Group & chọn Cột"| RG2""",

        "2.3": """flowchart LR
    subgraph LEGACY ["1. TRƯỚC KHI CÓ APACHE ARROW"]
        L1["Vùng nhớ Apache Spark (JVM)"] -->|"CPU Serialize"| L2["Bộ đệm Byte trung gian"]
        L2 -->|"CPU Deserialize & Copy"| L3["Vùng nhớ Python / Pandas / C++"]
        L4["Nghẽn cổ chai: Tốn 70–80% thời gian CPU chỉ để dịch qua lại trên cùng thanh RAM"]
        L3 --- L4
    end
    subgraph ARROW ["2. KHI DÙNG APACHE ARROW (ZERO-COPY IN-MEMORY)"]
        A_MEM["BỐ CỤC BỘ NHỚ CỘT CHUẨN HÓA APACHE ARROW TRÊN RAM<br/>• OrderID: [8886, 8887, 8888] | Amount: [5M, 12M, 15M]<br/>• Hỗ trợ Shredding cho JSON lồng nhau & ánh xạ Virtual Memory từ đĩa"]
        A_JVM["Apache Spark (JVM)"] -->|"Đọc trực tiếp qua con trỏ (Zero-copy)"| A_MEM
        A_PY["Python / Pandas / Polars / ML"] -->|"Đọc trực tiếp qua con trỏ (Zero-copy)"| A_MEM
    end""",

        "2.4": """flowchart TD
    subgraph BAD ["1. NON-SPLITTABLE: Nén khối đơn Gzip nguyên tệp (orders.csv.gz - 100 GB)"]
        B_FILE["Luồng mã hóa liền mạch từ Byte đầu đến Byte cuối (Không có mốc cắt giữa tệp)"]
        B_N1["Máy chủ 1: Phải tự đọc tuần tự từ đầu đến hết 100 GB"] --> B_FILE
        B_IDLE["Máy chủ 2 ... 100: Ngồi chờ không vì không biết điểm bắt đầu giải nén"]
    end
    subgraph GOOD ["2. SPLITTABLE: Container Formats (Parquet Row Groups / Avro 16-byte Sync Markers)"]
        G1["Khối 1 (Row Group 1)<br/>Nén Snappy / ZSTD độc lập"]
        G2["Khối 2 (Row Group 2)<br/>Nén Snappy / ZSTD độc lập"]
        G3["Khối 3 (Row Group 3)<br/>Nén Snappy / ZSTD độc lập"]
        M1["Máy chủ 1"] -->|"Đọc & giải nén song song"| G1
        M2["Máy chủ 2"] -->|"Đọc & giải nén song song"| G2
        M3["Máy chủ 3"] -->|"Đọc & giải nén song song"| G3
    end""",

        "3.1": """flowchart TD
    NN["NAMENODE (Quản lý Metadata trên RAM + EditLog / FsImage)<br/>• Sổ danh bạ: 'orders.log (1 GB) = 8 Blocks x 128 MB'<br/>• Block 1 (#8888) -> [DataNode 1 (Rack 1), DataNode 2 (Rack 2), DataNode 4 (Rack 2)]<br/>• Nhận Heartbeat & Blockreport định kỳ"]
    subgraph CLUSTER ["TẦNG DATANODES (Đặt chung Compute & Storage + Nhân bản x3 / Erasure Coding RS 6,3)"]
        DN1["DataNode 1 (Rack 1)<br/>• [Block 1] Bản gốc<br/>• Chạy Task Map tại chỗ"]
        DN2["DataNode 2 (Rack 2)<br/>• [Block 1] Bản sao 2<br/>• [Block 2] Bản gốc"]
        DN4["DataNode 4 (Rack 2)<br/>• [Block 1] Bản sao 3<br/>• [Block 5] Bản sao"]
        DN1 -->|"Đường ống nhân bản 2"| DN2 -->|"Đường ống nhân bản 3"| DN4
    end
    NN -->|"Chỉ huy phân bổ & Tự chữa lành (Self-healing khi hệ số < 3)"| CLUSTER""",

        "3.2": """flowchart TD
    CORE["Switch Tổng Trung Tâm (Core Switch)<br/>(3) OFF-RACK: Băng qua liên tủ mạng -> Băng thông thấp nhất, dễ nghẽn cổ chai"]
    subgraph RACK1 ["TỦ MẠNG 1 (RACK 1) — Top-of-Rack Switch 1"]
        NA["Máy chủ A (Node A)<br/>• Đang chạy Task tính toán<br/>• Có sẵn [Block #8888] (Bản sao 1)<br/>-> (1) DATA-LOCAL: Nhanh nhất, không tốn mạng"]
        NB["Máy chủ B (Node B)<br/>• Lưu [Block #8888] khi Node A bận<br/>-> (2) RACK-LOCAL: Chỉ qua Switch nội bộ tủ 1"]
    end
    subgraph RACK2 ["TỦ MẠNG 2 (RACK 2) — Top-of-Rack Switch 2"]
        NC["Máy chủ C (Node C)<br/>• Lưu [Block #8888] (Bản sao 2)"]
        ND["Máy chủ D (Node D)<br/>• Lưu [Block #8888] (Bản sao 3)"]
    end
    CORE <--> RACK1
    CORE <--> RACK2""",

        "3.3": """flowchart LR
    OLTP["DB Giao dịch OLTP<br/>(Đơn hàng #8888)"] -->|"Luồng sự kiện CDC<br/>(INSERT / UPDATE)"| KAFKA
    subgraph KAFKA ["APACHE KAFKA TOPIC: 'orders_events' (Append-only Log)"]
        O0["Offset 0<br/>[Đơn #8886]"] --> O1["Offset 1<br/>[Đơn #8887]"] --> O2["Offset 2<br/>[Đơn #8888]"] --> O3["Offset 3<br/>[Sửa Đ/C #8888]"]
        NOTE["• Ghi nối đuôi tuần tự (Sequential I/O) + Nén LZ4/Snappy<br/>• Tiered Storage xuống S3 & tua lại lịch sử (Replay)"]
    end
    KAFKA -->|"Consumer 1 (Real-time)"| FLINK["Apache Flink / Kafka Streams<br/>Tính doanh thu tức thời + Lưu state trên RocksDB"]
    KAFKA -->|"Consumer 2 (Stream-to-Batch)"| DW["Kinesis Firehose / BigQuery Streaming Buffer<br/>Nạp vào Kho phân tích / Lakehouse"]""",

        "3.4": """flowchart TD
    subgraph SRC ["1. NGUỒN DỮ LIỆU ĐẦU VÀO"]
        OP["Operational Data<br/>(DB Bán hàng OLTP)"]
        EX["External Data<br/>(CRM, ERP đối tác)"]
    end
    ETL["2. Quy trình ETL / ELT<br/>Làm sạch, chuẩn hóa & kiểm định lược đồ nghiêm ngặt (Schema-on-Write)"]
    DW["3. DATA WAREHOUSE (Snowflake / BigQuery / Redshift / Teradata)<br/>• Chỉ lưu dữ liệu CÓ CẤU TRÚC (Structured Data) & Đảm bảo giao dịch ACID<br/>• Động cơ lưu trữ dạng cột (Columnar) + Micro-partitioning (50–500 MB) + Query Result Cache<br/>• Hybrid Object Storage (BigQuery Colossus / S3 Select) & Zero-Copy Cloning"]
    BI["4a. Khai thác: BI Tools & Reports<br/>Truy vấn SQL phân tích tốc độ cao"]
    LIM["4b. 3 Hạn chế lịch sử:<br/>1. Bó tay trước dữ liệu phi cấu trúc (Ảnh/Video/Audio)<br/>2. Chi phí đắt đỏ ở quy mô Petabyte<br/>3. Động cơ đóng kín, khó chia sẻ trực tiếp cho AI/ML"]
    OP & EX --> ETL --> DW
    DW --> BI
    DW -.->|"Lực đẩy tiến hóa sang Data Lake / Lakehouse"| LIM""",

        "4.1": """flowchart LR
    subgraph C ["1. CONCEPTUAL MODEL (Mô hình Khái niệm)"]
        C1["Giao tiếp với Business / Chủ nhà<br/>Xác định thực thể & mối quan hệ:<br/>[Khách hàng] --mua--> [Đơn hàng] --gồm--> [Sản phẩm]"]
    end
    subgraph L ["2. LOGICAL MODEL (Mô hình Logic)"]
        L1["Bản thiết kế chi tiết độc lập CSDL:<br/>Bảng Fact_Sales<br/>• Ma_Don (PK / Degenerate Dim)<br/>• Ma_Khach_Hang (FK), Ma_San_Pham (FK)<br/>• So_Luong, So_Tien"]
    end
    subgraph P ["3. PHYSICAL MODEL (Mô hình Vật lý)"]
        P1["Triển khai trên CSDL thực tế (Snowflake/BigQuery):<br/>CREATE TABLE fact_sales (<br/>  ma_don BIGINT, so_luong INT, so_tien DECIMAL(18,2)<br/>) PARTITION BY (nam_thang) CLUSTER BY (ma_khach_hang)"]
    end
    C -->|"Kimball 4-Step:<br/>Process -> Grain -> Dim -> Fact"| L -->|"Chọn kiểu dữ liệu,<br/>Partition, Cluster, Index"| P""",

        "4.2": """flowchart TD
    subgraph INMON ["1. BILL INMON (Top-Down 3NF)"]
        I_SRC["Nguồn dữ liệu toàn Công ty"] --> I_EDW["Enterprise Data Warehouse (EDW)<br/>• Chuẩn hóa 3NF, tránh trùng lặp<br/>• Subject-oriented, Integrated,<br/>  Nonvolatile, Time-variant"]
        I_EDW --> I_M1["Data Mart: Sales"] & I_M2["Data Mart: Mkt"] & I_M3["Data Mart: Purch"]
    end
    subgraph KIMBALL ["2. RALPH KIMBALL (Bottom-Up Dimensional)"]
        K_SRC["Nguồn dữ liệu theo Quy trình Nghiệp vụ"] --> K_DW["Data Warehouse Trung tâm<br/>• Phi chuẩn hóa (Denormalized)<br/>• Thiết kế thẳng Fact & Conformed Dimensions<br/>  theo Star Schema"]
        K_DW --> K_BI["Phục vụ báo cáo BI cực nhanh"]
    end
    subgraph DV ["3. DAN LINSTEDT (Data Vault — Insert-Only)"]
        DV_H1["Hub 1 (HashKey + BusinessKey)"] --> DV_L["Link (Quan hệ N-N)"]
        DV_H2["Hub 2 (HashKey + BusinessKey)"] --> DV_L
        DV_S1["Satellite 1 (Thuộc tính + LoadDate)"] --> DV_H1
        DV_S2["Satellite 2 (Lịch sử Đ/C + LoadDate)"] --> DV_H2
    end""",

        "4.3": """flowchart LR
    subgraph DIM ["NGỮ CẢNH ĐỊNH TÍNH — DIMENSION TABLES (Rộng & Ngắn)"]
        D1["• Dim_Customer: Nguyễn Văn A (Bình Dương)<br/>• Dim_Store: Chi nhánh Bình Dương<br/>• Dim_Product: Nội thất Sofa<br/>• Dim_Date: Ngày 15/10/2026 (Smart Key: 20261015)<br/>-> Dùng để Lọc (WHERE) & Gom nhóm (GROUP BY)"]
    end
    subgraph FACT ["SỰ KIỆN ĐỊNH LƯỢNG — FACT_SALES (Hẹp & Rất dài)"]
        F1["• Ma_Don (Degenerate Dim): 8888<br/>• Khóa ngoại FK: Customer_SK, Store_SK, Date_SK<br/>• So_Luong: 1 (Additive Fact)<br/>• So_Tien: 5.000.000 VNĐ (Additive Fact)<br/>-> Bất biến (Append-only) tại 1 Grain nguyên tử cố định"]
    end
    DIM -->|"Nối qua khóa Surrogate PK / FK"| FACT""",

        "4.4": """flowchart TD
    subgraph STAR ["1. STAR SCHEMA (Lược đồ Hình sao — 1 Cấp JOIN)"]
        S_CUST["Dim_Customer"] & S_STORE["Dim_Store"] & S_PROD["Dim_Product"] & S_DATE["Dim_Date"] -->|"1 JOIN"| S_FACT["FACT_SALES"]
    end
    subgraph SNOW ["2. SNOWFLAKE SCHEMA (Hình bông tuyết — Nhiều Cấp JOIN)"]
        SN_CITY["Sub-Dim_City"] -->|"JOIN 2"| SN_STORE["Dim_Store"]
        SN_BRAND["Sub-Dim_Brand"] -->|"JOIN 2"| SN_PROD["Dim_Product"]
        SN_STORE & SN_PROD -->|"JOIN 1"| SN_FACT["FACT_SALES"]
    end
    subgraph OBT ["3. OBT — ONE BIG TABLE (Bảng phẳng — 0 JOIN)"]
        OBT_TBL["Bảng phẳng OBT_SALES:<br/>[Ma_Don: 8888 | Ten_Khach | Ten_Cua_Hang | Ten_San_Pham | So_Luong: 1 | So_Tien: 5M]<br/>-> Loại bỏ hoàn toàn JOIN, tối ưu quét trên Cloud Columnar Engine"]
    end""",

        "4.5": """flowchart LR
    subgraph DIMS ["CONFORMED DIMENSIONS (Chiều đồng nhất dùng chung toàn Công ty)"]
        CD_DATE["Dim_Date"]
        CD_PROD["Dim_Product"]
        CD_CUST["Dim_Customer<br/>(SCD Type 2: SK 101 -> SK 205)"]
        CD_STORE["Dim_Store"]
    end
    subgraph FACTS ["QUY TRÌNH NGHIỆP VỤ (BUSINESS PROCESSES / FACT TABLES)"]
        F_SALES["1. Bán lẻ (Fact_Retail_Sales)<br/>Nơi chứa Đơn hàng #8888"]
        F_INV["2. Quản lý Tồn kho (Fact_Inventory)"]
        F_PROC["3. Mua hàng NCC (Fact_Procurement)"]
    end
    CD_DATE & CD_PROD & CD_STORE --> F_SALES & F_INV & F_PROC
    CD_CUST --> F_SALES""",

        "5.1": """flowchart TD
    subgraph DW_FLOW ["1. DATA WAREHOUSE TRUYỀN THỐNG (Schema-on-Write & ETL)"]
        direction LR
        DW_SRC["Nguồn dữ liệu (Đơn #8888)"] -->|"TRANSFORM kiểm duyệt gắt gao:<br/>Định nghĩa đúng cột trước;<br/>JSON thêm 1 trường lạ -> GÃY PIPELINE"| DW_DST["DATA WAREHOUSE<br/>• Chỉ chứa bảng có cấu trúc sạch<br/>• Mất dữ liệu thô gốc, đĩa đắt đỏ"]
    end
    subgraph DL_FLOW ["2. DATA LAKE THẾ HỆ MỚI (Schema-on-Read & ELT)"]
        direction LR
        DL_SRC["Mọi định dạng của Đơn #8888<br/>(Structured + Textual + Analog/IoT)"] -->|"LOAD THẲNG (ELT):<br/>Đổ nguyên bản JSON, Parquet, Ảnh, Video<br/>lên S3/ADLS/GCS giá ~$0.02/GB/tháng"| DL_DST["DATA LAKE (Cloud Object Storage)<br/>• Lúc đọc ra phân tích mới áp Schema<br/>• Rủi ro: Dễ thoái hóa nếu thiếu quản trị"]
    end""",

        "5.2a": """flowchart LR
    subgraph LAKE ["DATA LAKE BAN ĐẦU (Ngăn nắp — Kỳ vọng WORM)"]
        L_DIR["• /sales/orders/8888.parquet<br/>• /logs/clickstream/click_8888.json<br/>• /images/contracts/contract_8888.jpg<br/>-> Phân vùng rõ ràng, tin cậy"]
    end
    subgraph SWAMP ["DATA SWAMP SAU 6 THÁNG (Hỗn loạn — Hội chứng WORN)"]
        S_DIR["• /tmp_test_8888/ & /data_final_final_v2/<br/>• /dump_2026_unnamed/8888_part1.json (Lỗi UTF)<br/>• /dump_2026_unnamed/3.parquet (Tệp ghi dở dang)<br/>• /dump_2026_unnamed/3_v2.parquet (Nhân đôi số!)<br/>-> Không ai biết tệp nào đúng, không ai dám dùng"]
    end
    LAKE -->|"Thoái hóa sau 6 tháng<br/>thiếu Catalog & Lifecycle"| SWAMP""",

        "5.2b": """flowchart TD
    JOB["Job Apache Spark đang ghi Đơn #8888 xuống S3"]
    JOB -->|"1. Đứt mạng ở giây thứ 5"| ZOMBIE["Sinh ra tệp ghi dở '3.parquet' (50% dữ liệu)"]
    JOB -->|"2. Tự động Retry chạy lại thành công 100%"| VALID["Sinh ra tệp hoàn chỉnh '3_v2.parquet' (100% dữ liệu)"]
    ZOMBIE & VALID --> DIR["Cùng nằm trong thư mục phân vùng S3<br/>(Apache Hive Table Format quản lý cấp độ thư mục)"]
    DIR --> DUP["HẬU QUẢ TRUY VẤN SQL:<br/>Động cơ quét TẤT CẢ tệp trong thư mục ('3.parquet' + '3_v2.parquet')<br/>-> Doanh thu Đơn #8888 bị TÍNH GẤP ĐÔI (Duplicate counts)!"]""",

        "5.3": """flowchart TD
    SWAMP["DATA SWAMP (ĐẦM LẦY DỮ LIỆU)"]
    G1["1. LỖ HỔNG GIAO DỊCH & CÔNG CỤ (ACID / Mutability)<br/>• Không có ACID: Job ETL đụng độ truy vấn đọc<br/>• Bất biến (Immutable): Không thể Upsert / Xóa lẻ GDPR<br/>• Không chặn được Schema Drift lúc nạp"]
    G2["2. THIẾU DATA CATALOG & METADATA MGMT<br/>• Không biết bảng nào ở đâu, ý nghĩa cột là gì<br/>• Thiếu người sở hữu rõ ràng (Ownership / Steward)<br/>• Tạo ra Dark Data / WORN & rủi ro rò rỉ dữ liệu"]
    G3["3. THIẾU DATA LINEAGE & OBSERVABILITY<br/>• Không truy vết được dữ liệu sinh ra từ nguồn nào,<br/>  qua bước biến đổi nào mà bị sai lệch / NULL<br/>• Thiếu 5 trụ cột giám sát & Quality Checks tự động"]
    SWAMP --> G1 & G2 & G3""",

        "5.4a": """flowchart LR
    SRC["Nguồn dữ liệu<br/>(Đơn hàng #8888)"] --> RAW["1. RAW ZONE (Vùng Dữ liệu Thô)<br/>• Giữ nguyên bản Đơn #8888 lúc mới nạp<br/>• Phục vụ đối chiếu & chạy lại lịch sử"]
    RAW -->|"Đường ống kiểm duyệt<br/>ETL / ELT 1"| CLEAN["2. CLEANSED ZONE (Vùng Đã Làm Sạch)<br/>• Lọc bỏ file rác, chuẩn hóa kiểu dữ liệu<br/>• Khử trùng lặp (Deduplicate)"]
    CLEAN -->|"Đường ống kiểm duyệt<br/>ETL / ELT 2"| CUR["3. CURATED ZONE (Vùng Tinh Chế)<br/>• Chuẩn hóa mô hình chiều / tổng hợp<br/>• Sẵn sàng cho BI & Machine Learning"]""",

        "5.4b": """flowchart TD
    subgraph CONTRACT ["1. QUẢN LÝ LƯỢC ĐỒ: DATA CONTRACTS + SCHEMA REGISTRY"]
        direction LR
        P_BAD["Không có Schema Mgmt:<br/>Producer tự ý đổi tên cột -> Kafka -> DIY -> GÃY PIPELINE!"]
        P_GOOD["Có Data Contract & Schema Registry (BACKWARD / FORWARD / FULL):<br/>Producer (#8888) -> Kafka -> Schema Registry kiểm tra tương thích -> Consumer an toàn"]
    end
    subgraph SSOT ["2. NGUỒN SỰ THẬT DUY NHẤT (SINGLE SOURCE OF TRUTH)"]
        direction LR
        S_BAD["Sai lầm (Divergent Truths):<br/>Xuất bảng Đơn hàng ra 40 Cloud Storage Buckets cho 40 phòng ban<br/>-> Ác mộng thu hồi quyền, chạy lại 40 nơi & tốn phí mạng Ingress/Egress"]
        S_GOOD["Giải pháp (Single Source of Truth):<br/>Duy trì DUY NHẤT 1 bảng nền tảng chuẩn xác tại trung tâm;<br/>mọi phòng ban truy cập chung qua phân quyền hạt mịn"]
    end""",

        "1.2b": """flowchart LR
    subgraph VOL ["1. BỘ NHỚ KHẢ BIẾN (VOLATILE: CPU Cache & RAM)"]
        V1["L1/L2/L3 Cache (~1–10 ns) & DDR5 RAM (~100 ns)"]
        V2["[x] Cúp điện -> Mất sạch Đơn #8888 trong 0 giây<br/>[+] Siêu nhanh nhưng đắt (~$10/GB)"]
        V1 --- V2
    end
    subgraph NONVOL ["2. LƯU TRỮ BẤT BIẾN + WAL (NON-VOLATILE: SSD / HDD / S3)"]
        N1["1. Ghi nối đuôi vào Write-Ahead Log (WAL) trên NVMe SSD (~1 ms)"]
        N2["2. Đồng bộ xuống Data Files & Cloud Object Storage (11 Nines Durability)"]
        N3["[+] Cúp điện vẫn khôi phục nguyên vẹn 100% Đơn hàng #8888"]
        N1 --> N2 --- N3
    end
    VOL -->|"Bắt buộc flush xuống đĩa<br/>trước khi báo thành công"| NONVOL""",

        "1.3b": """flowchart LR
    subgraph HDD_MECH ["1. ĐĨA TỪ CƠ HỌC HDD (Mechanical Platter)"]
        H1["Cánh tay cơ học phải chờ đĩa quay (Seek Time: 4–10 ms)"]
        H2["Giới hạn vật lý: ~100 IOPS | Băng thông tuần tự: 200–300 MB/s"]
        H1 --- H2
    end
    subgraph SSD_FLASH ["2. CHIP BÁN DẪN NVMe SSD (NAND Flash Cells)"]
        S1["Đọc điện tử trực tiếp (~100 µs), song song hàng chục nghìn IOPS"]
        S2["Giới hạn vật lý: Không ghi đè tại chỗ; phải xóa cả Erase Block (256KB–4MB)<br/>-> Gây Write Amplification & hao mòn tuổi thọ chip nhớ"]
        S1 --- S2
    end""",

        "2.1b": """flowchart TD
    subgraph COUPLED ["1. KIẾN TRÚC GẮN KẾT CỨNG (HDFS / On-Premise)"]
        C_NODES["Node 1 (CPU+RAM+Disk) & Node 2 (CPU+RAM+Disk) & Node 3 (CPU+RAM+Disk)"]
        C_PAIN["[x] Hết ổ cứng phải mua kèm CPU/RAM đắt đỏ<br/>[x] Không thể tắt cụm máy tính lúc nửa đêm vì tắt là mất dữ liệu!"]
        C_NODES --- C_PAIN
    end
    subgraph DECOUPLED ["2. KIẾN TRÚC TÁCH RỜI COMPUTE & STORAGE (Cloud Object Storage)"]
        D_COMP["Tầng Compute (Spark / Trino / Snowflake)<br/>Bật/tắt đàn hồi theo giây, trả tiền theo phút chạy"]
        D_STOR["Tầng Cloud Object Storage (AWS S3 / GCS / ADLS)<br/>Lưu trữ độc lập giá rẻ ~$0.02/GB/tháng, băng thông song song ~3 GB/s"]
        D_COMP <-->|"Đọc/ghi song song qua HTTP REST"| D_STOR
    end""",

        "2.4b": """flowchart LR
    subgraph RLE ["1. RUN-LENGTH ENCODING (RLE)"]
        R_IN["Cột Khu_Vực đã sắp xếp:<br/>[Bình Dương, Bình Dương, ..., Bình Dương (x5.000)]"]
        R_OUT["Nén thành cặp duy nhất:<br/>(Giá trị: 'Bình Dương', Số lần lặp: 5.000)"]
        R_IN --> R_OUT
    end
    subgraph DICT ["2. DICTIONARY + BIT-PACKING"]
        D_IN["Chuỗi văn bản dài lặp lại (20 bytes/dòng)"]
        D_OUT["Sổ từ điển: {0: 'Bình Dương', 1: 'Hà Nội'}<br/>Dữ liệu cột thay bằng mảng số nguyên 1-bit: [0, 0, 1, 0]"]
        D_IN --> D_OUT
    end
    subgraph DELTA ["3. DELTA ENCODING"]
        DL_IN["Chuỗi Mã đơn / Timestamp tăng dần:<br/>[8886, 8887, 8888, 8889]"]
        DL_OUT["Lưu số gốc + khoảng chênh lệch siêu nhỏ:<br/>[Gốc: 8886 | Delta: +1, +1, +1]"]
        DL_IN --> DL_OUT
    end""",

        "3.2b": """flowchart LR
    subgraph REDIS ["1. REDIS (In-Memory Data Structures)"]
        R1["Lưu trên RAM (~100 ns) | Hỗ trợ String, Hash, List, Set, Sorted Set"]
        R2["Có RDB Snapshot + AOF Log | Dùng cho Leaderboard, Session, Giỏ hàng #8888"]
        R1 --- R2
    end
    subgraph MEM ["2. MEMCACHED (Pure Key-Value Cache)"]
        M1["Lưu thuần Key-Value trên RAM (Đa luồng Multi-threaded cực nhẹ)"]
        M2["Không lưu xuống đĩa | Dùng làm bộ đệm trang HTML / kết quả truy vấn tĩnh"]
        M1 --- M2
    end
    subgraph ROCKS ["3. ROCKSDB (Embedded LSM-Tree Engine)"]
        K1["Ghi nối đuôi vào MemTable (RAM) + WAL -> Flush xuống SSTables trên NVMe SSD"]
        K2["Dùng làm State Store cục bộ cho Apache Flink / Kafka Streams (lưu trạng thái hàng tỷ đơn)"]
        K1 --- K2
    end""",

        "3.5": """flowchart TD
    Q["Câu lệnh SQL: SELECT SUM(so_tien) FROM fact_sales WHERE ngay = '2026-10-15'"]
    CACHE{"1. Kiểm tra Query Result Cache<br/>(Khớp 100% câu lệnh & bảng chưa đổi?)"}
    CACHE -->|"Cache Hit (~10 ms)"| HIT["Trả kết quả tức thì — Tốn 0 CPU Compute!"]
    CACHE -->|"Cache Miss"| PRUNE["2. Micro-partition Pruning qua Metadata Min/Max<br/>Bỏ qua 99% các Micro-partitions (50–500 MB) không chứa ngày 15/10"]
    PRUNE --> SCAN["3. Quét cột (Columnar Scan) đúng 1 Micro-partition chứa Đơn #8888<br/>Kết hợp Zero-Copy Cloning khi cần tạo môi trường Test tốn $0 lưu trữ"]
    Q --> CACHE""",

        "4.3b": """flowchart LR
    subgraph ADD ["1. ADDITIVE FACTS (Cộng được trên MỌI chiều)"]
        A1["Ví dụ: So_Tien (15.000.000đ), So_Luong (3 món) của Đơn #8888"]
        A2["[+] Dùng hàm SUM() tự do theo Ngày, Tháng, Cửa hàng, Sản phẩm, Khách hàng"]
        A1 --- A2
    end
    subgraph SEMI ["2. SEMI-ADDITIVE FACTS (Số dư tại 1 thời điểm)"]
        S1["Ví dụ: Ton_Kho_Cuoi_Ngay (50 chiếc ghế Sofa), So_Du_Tai_Khoan"]
        S2["[+] Cộng được theo Cửa hàng / Kho | [x] CẤM dùng SUM() cộng dồn qua chiều Thời gian!"]
        S1 --- S2
    end
    subgraph NON ["3. NON-ADDITIVE FACTS (Tỷ lệ / Đơn giá / Nhiệt độ)"]
        N1["Ví dụ: Ty_Le_Chiet_Khau (10%), Don_Gia_Trung_Binh, Bien_Loi_Nhuan (%)"]
        N2["[x] CẤM cộng trực tiếp trên mọi chiều! Phải lưu Tử số & Mẫu số để chia lại khi gộp"]
        N1 --- N2
    end""",

        "4.5a": """flowchart TD
    EVENT["Sự kiện thực tế: Khách hàng Nguyễn Văn A (Đơn #8888)<br/>chuyển nhà từ 'Hà Nội' vào 'Bình Dương' ngày 15/10/2026"]
    subgraph SCD1 ["SCD TYPE 1 (Overwrite — Ghi đè xóa dấu vết)"]
        T1["Ghi đè trực tiếp cột Tinh_Thanh = 'Bình Dương' tại dòng SK 101<br/>[x] Mất lịch sử: Đơn hàng cũ năm 2025 ở Hà Nội bị tính nhầm cho Bình Dương!"]
    end
    subgraph SCD2 ["SCD TYPE 2 (Add New Row — Chuẩn vàng Kimball)"]
        T2["• Dòng cũ (SK 101): Hà Nội | Eff: 2024-01-01 -> Exp: 2026-10-14 | Current = False<br/>• Dòng mới (SK 205): Bình Dương | Eff: 2026-10-15 -> Exp: 9999-12-31 | Current = True<br/>[+] Bảo toàn 100% lịch sử doanh thu theo đúng thời điểm phát sinh"]
    end
    subgraph SCD3 ["SCD TYPE 3 (Add New Column — Lưu đúng 1 lần đổi gần nhất)"]
        T3["Thêm cột Tinh_Thanh_Cu = 'Hà Nội' cạnh cột Tinh_Thanh_Hien_Tai = 'Bình Dương'<br/>[x] Nếu khách chuyển nhà lần thứ 3 sẽ mất lịch sử lần 1"]
    end
    EVENT --> SCD1 & SCD2 & SCD3""",

        "5.2c": """flowchart LR
    subgraph HIVE ["1. APACHE HIVE TABLE FORMAT (Quản lý cấp độ Thư mục)"]
        H1["Hive Metastore chỉ lưu đường dẫn thư mục: s3://lake/orders/month=2026-10/"]
        H2["Khi đọc phải gọi lệnh LIST (ls) toàn bộ thư mục S3:<br/>[x] Rất chậm khi có hàng vạn tệp | [x] Đọc nhầm cả tệp rác '3.parquet' ghi dở!"]
        H1 --> H2
    end
    subgraph S3_TRAP ["2. BẪY BẤT BIẾN (IMMUTABILITY) & XÓA LẺ GDPR TRÊN S3"]
        S1["Muốn xóa/sửa 1 dòng Đơn #8888 trong 10.000 tệp Parquet (1 TB)?"]
        S2["[x] Không thể sửa tại chỗ 1 byte trên S3!<br/>Phải đọc và viết lại nguyên tệp hàng trăm MB mà không có khóa giao dịch ACID"]
        S1 --> S2
    end""",

        "5.3b": """flowchart LR
    PILLARS["5 TRỤ CỘT QUAN SÁT DỮ LIỆU TỰ ĐỘNG (DATA OBSERVABILITY)"]
    P1["1. Freshness (Độ tươi mới):<br/>Bảng Đơn hàng có được nạp đúng 07:00 sáng nay không?"]
    P2["2. Volume (Khối lượng):<br/>Số dòng nạp hôm nay (50.000 đơn) có tụt bất thường về 0 hay tăng vọt gấp đôi?"]
    P3["3. Schema (Cấu trúc):<br/>Có cột nào vừa bị đổi tên, xóa bỏ hay đổi kiểu dữ liệu ngoài ý muốn?"]
    P4["4. Distribution (Phân phối giá trị):<br/>Tỷ lệ NULL của cột So_Tien hay phạm vi giá trị có lệch khỏi ngưỡng lịch sử?"]
    P5["5. Lineage (Phả hệ):<br/>Khi bảng báo cáo lỗi, upstream job nào là thủ phạm gốc và dashboard nào bị ảnh hưởng?"]
    PILLARS --> P1 & P2 & P3 & P4 & P5""",

        "6.1a": """flowchart TD
    subgraph GEN1 ["1. DATA WAREHOUSE (Thế hệ 1)"]
        W1["[+] Giao dịch ACID, Schema chuẩn, BI nhanh"]
        W2["[x] Đắt đỏ, đóng kín, mù dữ liệu phi cấu trúc"]
        W1 --- W2
    end
    subgraph GEN2 ["2. DATA LAKE 1.0 (Thế hệ 2)"]
        L1["[+] Lưu mọi định dạng trên S3 giá rẻ ~$0.02/GB"]
        L2["[x] Không có ACID -> Thoái hóa thành Data Swamp"]
        L1 --- L2
    end
    subgraph GEN3 ["3. DATA LAKEHOUSE (Thế hệ 3 — CIDR 2021)"]
        LH_APPS["Tầng Ứng dụng Hợp nhất: BI & SQL Analytics + Data Science + Machine Learning & Streaming"]
        LH_META["LỚP GIAO DỊCH & SIÊU DỮ LIỆU (Delta Lake / Apache Iceberg / Apache Hudi)<br/>ACID Transactions | Time Travel | Schema Enforcement & Evolution | Caching & Indexing"]
        LH_STOR["Tầng Lưu trữ Mở (Cloud Object Storage: S3 / ADLS / GCS) + Định dạng Mở (Apache Parquet)"]
        LH_APPS --> LH_META --> LH_STOR
    end
    GEN1 & GEN2 -->|"Hợp nhất tinh hoa cả 2 thế giới"| GEN3""",

        "6.1b": """flowchart LR
    subgraph TWO_TIER ["1. KIẾN TRÚC 2 TẦNG CŨ (Two-Tier: Lake + Warehouse)"]
        T_SRC["Nguồn dữ liệu"] --> T_LAKE["Data Lake (S3)"] -->|"Reverse/Copy ETL<br/>phức tạp & trễ"| T_DW["Data Warehouse Độc quyền"]
        T_NOTE["[x] Nhân bản dữ liệu 2–3 lần | [x] Lệch pha số liệu giữa AI và BI"]
        T_DW --- T_NOTE
    end
    subgraph LH_FAST ["2. KIẾN TRÚC LAKEHOUSE 1 TẦNG + 3 VŨ KHÍ TĂNG TỐC BI (CIDR 2021)"]
        F1["(1) Hot Caching trên RAM/NVMe SSD"]
        F2["(2) Auxiliary Data (Min/Max/Bloom) & Gom cụm Z-Order/Hilbert"]
        F3["(3) Vectorized Execution (SIMD + Apache Arrow)"]
        F_RES["Đọc trực tiếp từ 1 nguồn Parquet duy nhất trên S3 với tốc độ ngang ngửa Data Warehouse!"]
        F1 & F2 & F3 --> F_RES
    end""",

        "6.2a": """flowchart TD
    subgraph LOG ["THƯ MỤC NHẬT KÝ GIAO DỊCH: _delta_log/ (Nguồn sự thật duy nhất)"]
        V0["000000.json (Version 0 — INSERT Đơn #8888 = 15M):<br/>• protocol + metaData<br/>• add: part-A.parquet (min=8000, max=8888)"]
        V1["000001.json (Version 1 — UPDATE Đơn #8888 = 14M):<br/>• remove: part-A.parquet (Xóa logic)<br/>• add: part-B.parquet (Bản ghi mới 14M)"]
        CP["000010.checkpoint.parquet + _last_checkpoint:<br/>Gộp trạng thái sau mỗi 10 commits để đọc nhanh mà không cần duyệt JSON cũ"]
        V0 --> V1 --> CP
    end
    subgraph DATA ["THƯ MỤC DỮ LIỆU S3 (orders/)"]
        FA["part-A.parquet (15M)<br/>Giữ lại cho Time Travel v0"]
        FB["part-B.parquet (14M)<br/>Hợp lệ tại Version hiện tại"]
        FZ["part-Z.parquet (Tệp rác ghi dở)<br/>Không có trong _delta_log -> Bị bỏ qua 100%!"]
    end
    V0 -.->|"Trỏ tới khi đọc v0"| FA
    V1 -->|"Trỏ tới khi đọc bản mới nhất"| FB""",

        "6.2b": """flowchart TD
    CAT["1. ICEBERG CATALOG (REST / Glue / Polaris / Nessie)<br/>Cập nhật con trỏ nguyên tử CAS: v1.metadata.json -> v2.metadata.json"]
    META["2. METADATA FILE (v2.metadata.json)<br/>Lưu Table UUID, Schema (field-id), Partition Specs & danh sách Snapshots (s1, s2)"]
    MLIST["3. MANIFEST LIST (snap-s2.avro)<br/>Danh sách các Manifest Files + Phạm vi phân vùng (Cắt tỉa Cấp 1 — Partition Pruning)"]
    MFILE["4. MANIFEST FILE (manifest-02.avro)<br/>Danh sách Data Files + Thống kê cột Min/Max/Null (Cắt tỉa Cấp 2 — File Skipping)"]
    DATA["5. DATA FILES TRÊN S3<br/>part-001.parquet (Chứa Đơn #8888 = 14M) + Delete Files (nếu dùng MOR)"]
    CAT --> META --> MLIST --> MFILE --> DATA""",

        "6.2c": """flowchart TD
    subgraph TIMELINE ["1. HUDI TIMELINE (.hoodie/ — Quản lý trạng thái giao dịch 3 bước)"]
        TL[".requested (Yêu cầu) -> .inflight (Đang ghi) -> .commit (COW) / .deltacommit (MOR)"]
    end
    subgraph INDEX ["2. HUDI INDEXING ENGINE (Định vị siêu tốc File Group chứa Đơn #8888)"]
        IDX["Record-Level Index (RLI) | Bloom Filter Index | Bucket Hashing Index<br/>-> Tra cứu 'order_id = 8888' nằm ở File Group nào mà không cần quét toàn bảng!"]
    end
    subgraph FG ["3. HUDI FILE GROUP (fg_id_01) & FILE SLICES"]
        BASE["Base File cột: fg_01_v1.parquet (Chứa Đơn #8888 gốc = 15M)"]
        LOG["Delta Log Files dòng: .fg_01.log.1_avro (Bản ghi cập nhật #8888 = 14M)"]
        BASE --- LOG
    end
    TIMELINE & INDEX --> FG""",

        "6.2d": """flowchart TD
    PARQ["TẦNG DỮ LIỆU VẬT LÝ DUY NHẤT TRÊN S3:<br/>orders_8888.parquet (Không nhân bản tệp dữ liệu!)"]
    UNI["BỘ DỊCH SIÊU DỮ LIỆU ĐA CHIỀU:<br/>Delta UniForm / Apache XTable / Hudi Pluggable Format"]
    M_DELTA["Metadata Delta Lake<br/>(_delta_log/*.json)"]
    M_ICE["Metadata Apache Iceberg<br/>(metadata/*.json + *.avro)"]
    M_HUDI["Metadata Apache Hudi<br/>(.hoodie/ timeline)"]
    PARQ --> UNI
    UNI --> M_DELTA & M_ICE & M_HUDI
    M_DELTA -->|"Đọc tự nhiên"| E1["Databricks / Spark"]
    M_ICE -->|"Đọc tự nhiên"| E2["Snowflake / Trino / BigQuery"]
    M_HUDI -->|"Đọc tự nhiên"| E3["Apache Flink / Presto"]""",

        "6.3": """flowchart LR
    subgraph MVCC ["1. MVCC (Snapshot Isolation — Đọc & Ghi)"]
        M1["Luồng Đọc (Giám đốc BI) đọc Snapshot v1 (part-A.parquet)<br/>trong khi Luồng Ghi đang tạo Snapshot v2 (part-B.parquet)"]
        M2["[+] Readers NEVER block Writers & Writers NEVER block Readers!"]
        M1 --- M2
    end
    subgraph OCC ["2. OCC (Optimistic Concurrency — Ghi & Ghi)"]
        O1["Writer 1 & Writer 2 cùng xuất phát từ v1;<br/>Writer 1 thắng v2 -> Writer 2 kiểm tra xung đột cấp độ tệp (File-Level Conflict)"]
        O2["[+] Khác Partition/Tệp -> Cho phép lên v3 | [x] Trùng tệp #8888 -> Báo lỗi / Retry"]
        O1 --- O2
    end
    subgraph NBCC ["3. NBCC (Non-Blocking Concurrency — Hudi MOR)"]
        N1["Nhiều luồng Streaming (Kafka/Flink) cùng ghi nối đuôi vào các Delta Log (.log.avro)<br/>và sắp thứ tự theo TrueTime commit timestamp mà không bao giờ hủy giao dịch"]
    end""",

        "6.3b": """flowchart TD
    subgraph TT ["1. TIME TRAVEL & CHANGE DATA FEED (CDF)"]
        S0["Snapshot v0 (14:00)<br/>Đơn #8888 = 15M"] -->|"UPDATE #8888 = 14M"| S1["Snapshot v1 (14:05)<br/>Đơn #8888 = 14M"]
        S1 -->|"RESTORE TO v0"| S2["Snapshot v2<br/>Khôi phục tức thời về 15M"]
        S1 -.->|"CDF: table_changes(0, 1)"| CDF["Xuất dòng biến động:<br/>update_preimage (15M) + update_postimage (14M)<br/>cho pipeline Silver -> Gold"]
    end
    subgraph COLID ["2. SCHEMA EVOLUTION BẰNG MÃ CỘT BẤT BIẾN (COLUMN ID / FIELD ID)"]
        C_OLD["Tệp Parquet cũ lưu theo ID:<br/>[field-id=1: 8888 | field-id=2: 15M]"]
        C_META["Lệnh RENAME COLUMN total_cost TO order_amount:<br/>Chỉ sửa nhãn của field-id=2 trong JSON Metadata (Tốn 1 ms, viết lại 0 byte Parquet!)"]
        C_OLD --> C_META
    end""",

        "6.4": """flowchart LR
    subgraph COW ["1. COPY-ON-WRITE (COW — Tối ưu Đọc OLAP/BI)"]
        C1["Tệp gốc file_01.parquet (100 MB, 100.000 dòng, #8888 = 15M)"]
        C2["Khi UPDATE #8888 = 14M:<br/>Viết lại TOÀN BỘ tệp mới file_02.parquet (100 MB) chứa 99.999 dòng cũ + 1 dòng mới"]
        C3["[+] Đọc cực nhanh (Quét thẳng 1 tệp) | [x] Ghi chậm, khuếch đại ghi WAF >> 1"]
        C1 --> C2 --- C3
    end
    subgraph MOR ["2. MERGE-ON-READ (MOR — Tối ưu Ghi Streaming/CDC)"]
        M1["Giữ nguyên Base File file_01.parquet (100 MB)"]
        M2["Khi UPDATE #8888 = 14M:<br/>Chỉ ghi nối đuôi 1 KB vào Delta Log (.avro) hoặc Positional/Equality Delete File"]
        M3["[+] Ghi tức thì (WAF ≈ 1) | [x] Khi đọc RT phải trộn Base + Log (hoặc đọc RO bỏ qua Log)"]
        M1 --> M2 --- M3
    end""",

        "6.5a": """flowchart LR
    subgraph HIVE_P ["1. HIVE PARTITIONING CŨ (Bẫy Quét Toàn Bảng)"]
        HP1["Phân vùng theo cột phái sinh nam_thang = '2026-10'"]
        HP2["User lọc: WHERE ngay_gio_mua >= '2026-10-15' (Quên thêm AND nam_thang = '2026-10')<br/>-> [x] Hive không hiểu mối liên hệ, quét mù toàn bộ 10 năm dữ liệu!"]
        HP1 --> HP2
    end
    subgraph ICE_P ["2. ICEBERG HIDDEN PARTITIONING & PARTITION EVOLUTION"]
        IP1["Lưu hàm biến đổi month(ngay_gio_mua) trong Partition Spec ID 0 của Metadata:<br/>-> [+] User chỉ lọc ngay_gio_mua, Iceberg tự động cắt tỉa đúng phân vùng tháng 10!"]
        IP2["Partition Evolution (Đổi sang chia theo Ngày — Spec ID 1):<br/>-> [+] Chỉ cập nhật Metadata trong 1 giây, giữ nguyên các tệp Parquet cũ!"]
        IP1 --> IP2
    end""",

        "6.5b": """flowchart LR
    subgraph BEFORE ["1. TRƯỚC KHI GOM CỤM (Dữ liệu phân tán ngẫu nhiên)"]
        B1["File 1: Tỉnh [An Giang .. Yên Bái] | Mã đơn [1001 .. 9990]"]
        B2["File 2: Tỉnh [An Giang .. Vĩnh Phúc] | Mã đơn [1005 .. 9999]"]
        B_RES["[x] Tìm Đơn #8888 ở Bình Dương phải ĐỌC CẢ 2 FILE vì khoảng Min/Max chồng lấn!"]
        B1 & B2 --> B_RES
    end
    subgraph AFTER ["2. SAU KHI CHẠY Z-ORDERING / LIQUID CLUSTERING (Hilbert Curve)"]
        A1["File 1: Tỉnh [An Giang .. Bình Dương] | Mã đơn [8000 .. 8999] -> ĐỌC FILE 1"]
        A2["File 2: Tỉnh [Đà Nẵng .. Yên Bái] | Mã đơn [1000 .. 7999] -> BỎ QUA NGAY (SKIP)!"]
        A_RES["[+] Thu hẹp khoảng [Min, Max] đa chiều & gom cụm tăng trưởng (Liquid Clustering)"]
        A1 & A2 --> A_RES
    end""",

        "6.5c": """flowchart TD
    subgraph COMP ["1. COMPACTION / BIN-PACKING (OPTIMIZE)"]
        CP1["43.200 tệp Parquet nhỏ li ti (500 KB/tệp) từ luồng Streaming"] -->|"Lệnh OPTIMIZE / rewrite_data_files"| CP2["Gộp thành các tệp Parquet chuẩn 128 MB – 1 GB<br/>Trị dứt điểm Small File Problem"]
    end
    subgraph DV ["2. DELETION VECTORS (Xóa mềm Roaring Bitmap)"]
        DV1["Xóa/sửa Đơn #8888 trong tệp 512 MB"] -->|"Không viết lại tệp Parquet"| DV2["Ghi tệp Roaring Bitmap siêu nhỏ đánh dấu 'Dòng 4512 đã xóa'<br/>Ghi xong trong vài ms; gộp vật lý sau khi chạy OPTIMIZE / REORG PURGE"]
    end
    subgraph VAC ["3. VACUUM / SNAPSHOT EXPIRATION & TUÂN THỦ GDPR"]
        VC1["Dọn vĩnh viễn các tệp Parquet lịch sử đã quá hạn lưu giữ (Mặc định >= 168 giờ = 7 ngày)"]
        VC2["Quy trình 3 bước xóa GDPR: (1) DELETE -> (2) REORG PURGE / OPTIMIZE -> (3) VACUUM"]
        VC1 --- VC2
    end""",

        "7.1a": """flowchart LR
    SRC1["Nguồn Batch (Files / DB)"] & SRC2["Nguồn Stream (Kafka / Debezium CDC)"] --> B
    subgraph B ["1. BRONZE LAYER (Infancy — Raw Zone)"]
        B1["• Ghi Append-only & Immutable<br/>• Biến đổi tối thiểu, hứng lỗi vào _corrupt / _debug<br/>• [+] Chốt chặn Audit & Replay!"]
    end
    subgraph S ["2. SILVER LAYER (Teenage — Cleaned & Conformed)"]
        S1["• Lọc bỏ _corrupt, khử trùng (Dedup)<br/>• Cưỡng chế Schema, chuẩn hóa kiểu<br/>• Enterprise View (~3NF / Data Vault / SCD2)"]
    end
    subgraph G ["3. GOLD LAYER (Maturity — Curated & Business-Ready)"]
        G1["• Tính sẵn KPI & quy tắc nghiệp vụ<br/>• Phi chuẩn hóa Star Schema / OBT (0 JOIN)<br/>• Thiết kế chuyên biệt cho từng bài toán"]
    end
    B -->|"Cổng kiểm soát 1<br/>(Quality Gate 1)"| S -->|"Cổng kiểm soát 2<br/>(Quality Gate 2)"| G
    G --> OUT1["BI / Executive Reports"] & OUT2["AI / Machine Learning Apps"]""",

        "7.1b": """flowchart LR
    subgraph ONE_HOP ["1. ĐƯỜNG ỐNG 1-HOP TRỰC TIẾP (Nguồn -> Thẳng BI)"]
        OH1["[x] Gãy vụn tức thì: 1 dòng JSON lỗi (#8889) làm sập cả báo cáo CEO"]
        OH2["[x] Không có điểm quay lui (No Fallback): Đổi công thức KPI phải chọc lại vào DB OLTP đang chạy thật"]
        OH3["[x] Trùng lặp công sức: 5 phòng ban tự viết lại cùng 1 logic làm sạch"]
        OH1 --- OH2 --- OH3
    end
    subgraph THREE_HOP ["2. KIẾN TRÚC 3-TIERED MEDALLION (Có Chốt chặn Fallback)"]
        TH1["[+] Tầng Bronze làm mỏ neo bất biến: Khi cần sửa lỗi chỉ việc Replay từ Bronze -> Silver, bảo vệ 100% DB OLTP"]
        TH2["[+] Tầng Silver tái sử dụng toàn công ty: Làm sạch & khử trùng Đơn #8888 đúng 1 lần cho mọi đội nhóm"]
        TH3["[+] Tầng Gold linh hoạt: Có thể nối Gold -> Gold tạo sản phẩm mới"]
        TH1 --> TH2 --> TH3
    end""",

        "7.2a": """flowchart TD
    IN["Luồng Kafka / CDC đổ về:<br/>Đơn #8888 (Hợp lệ: 15M) + Đơn #8889 (Lỗi JSON: 'ERROR_TIMEOUT')"]
    PERM["Spark Permissive Passthrough:<br/>option('mode', 'PERMISSIVE').option('columnNameOfCorruptRecord', '_corrupt')"]
    BRONZE["Bảng 'bronze.sales_transactions_raw' (Không làm gãy pipeline giữa đêm!):<br/>• #8888: raw_amount='15,000,000 VND' | _corrupt = NULL<br/>• #8889: raw_amount='ERROR_TIMEOUT' | _corrupt = '{raw_err_payload}'"]
    CLEAN["Bảng 'silver.orders_cleaned'<br/>[+] Bỏ cột _corrupt + Dedup + Ép kiểu DECIMAL(15000000.00)"]
    QUAR["Bảng cách ly 'quarantine.corrupt_orders'<br/>[!] Bắn cảnh báo cho kỹ sư sửa lỗi & Replay lại sau"]
    IN --> PERM --> BRONZE
    BRONZE -->|"Cổng lọc 1: WHERE _corrupt IS NULL"| CLEAN
    BRONZE -->|"Cổng cách ly: WHERE _corrupt IS NOT NULL"| QUAR""",

        "7.2b": """flowchart TD
    B["1. TẦNG BRONZE: bronze.sales_transactions_raw (Append-only / MOR)<br/>• id='8888' | cust='  nguyen van a ' | amt='15,000,000 VND' | ts=14:00:01 | _corrupt=NULL<br/>• id='8888' | cust='  nguyen van a ' | amt='15,000,000 VND' | ts=14:00:02 | _corrupt=NULL (Trùng)<br/>• id='8889' | cust=NULL | amt='ERROR_TIMEOUT' | ts=14:00:05 | _corrupt='{raw_err}'"]
    S["2. TẦNG SILVER: silver.orders_cleaned (Enterprise View ~3NF / SCD Type 2)<br/>• order_id=8888 | customer_sk=501 | store_sk=12 | net_amount=15000000.00 | ts=2026-10-15 14:00:01"]
    G["3. TẦNG GOLD: gold.obt_customer_sales_analytics (Phi chuẩn hóa OBT — 0 JOIN cho BI!)<br/>• order_id=8888 | Nguyễn Văn A | Bình Dương | Showroom Bình Dương 1 | 15000000.00 | VIP_GOLD"]
    B -->|"Lọc _corrupt IS NULL, Dedup #8888, Ép kiểu DECIMAL, Đối khớp SK (~3NF)"| S
    S -->|"Áp quy tắc hạng VIP_GOLD, Phi chuẩn hóa Star Schema / OBT (COW + Z-Ordering)"| G""",

        "7.2c": """flowchart LR
    subgraph GATE1 ["1. KHÓA LƯỢC ĐỒ (SCHEMA GATE)"]
        G1_A["Tắt trộn tự động: mergeSchema = false<br/>Cấm ghi đè bừa bãi: overwriteSchema = false"]
        G1_B["[+] Ngăn cột rác từ tầng Bronze vô tình tràn sang làm bẩn bảng Silver"]
        G1_A --- G1_B
    end
    subgraph GATE2 ["2. RÀNG BUỘC CẤP BẢNG (CHECK CONSTRAINTS)"]
        G2_A["ALTER TABLE silver.orders ADD CONSTRAINT valid_amount CHECK (net_amount > 0)"]
        G2_B["[+] Vi phạm sẽ ném lỗi DeltaInvariantViolationException và chặn ghi tức thì"]
        G2_A --- G2_B
    end
    subgraph GATE3 ["3. DLT EXPECTATIONS & ICEBERG WAP"]
        G3_A["@dlt.expect (Cảnh báo) | @dlt.expect_or_drop (Lọc bỏ) | @dlt.expect_or_fail (Dừng)"]
        G3_B["Iceberg Write-Audit-Publish (WAP): Ghi vào nhánh 'audit', kiểm định Pass 100% mới nối sang 'main'"]
        G3_A --- G3_B
    end""",

        "7.3a": """flowchart TD
    subgraph MED ["LUỒNG TINH CHẾ DỮ LIỆU NGANG (MULTI-HOP MEDALLION PIPELINE)"]
        B["1. BRONZE LAYER (Raw)"] --> S["2. SILVER LAYER (~3NF / SCD2)"] --> G["3. GOLD LAYER (Star / OBT)"]
    end
    subgraph UNDER ["BA DÒNG CHẢY NGẦM QUẢN TRỊ & VẬN HÀNH XUYÊN SUỐT (THE UNDERCURRENTS)"]
        U1["1. Data Catalog & Lineage: Unity Catalog / Glue / Nessie (catalog.schema.table) + OpenLineage (Dataset-Job-Run)"]
        U2["2. Security & Compliance: Least Privilege (DCL GRANT/REVOKE), Row Filter, Column Masking & Xóa GDPR 3 bước"]
        U3["3. Cloud FinOps & Lifecycle: Hot ($0.023/GB) -> Warm ($0.0125/GB) -> Cold/Glacier ($0.004/GB, 1/17 giá) + Vacuum + Ephemeral Compute"]
        U1 --- U2 --- U3
    end
    UNDER -->|"Nâng đỡ & kiểm soát xuyên suốt cả 3 tầng"| MED""",

        "7.3b": """flowchart LR
    subgraph ANTI ["1. PHẢN MẪU: EXPORT BẢNG RA 40 BUCKETS RIÊNG LẺ"]
        A1["Chép các phân vùng của bảng Đơn hàng ra 40 Buckets / Prefixes S3 cho 40 đội nhóm"]
        A2["[x] Ác mộng phân quyền IAM rời rạc ở 40 nơi<br/>[x] Khi Reprocess Đơn #8888 phải tính lại 40 lần & tốn phí mạng 2 chiều (Ingress/Egress)!"]
        A1 --> A2
    end
    subgraph SSOT ["2. CHUẨN MỰC: SINGLE SOURCE OF TRUTH + CATALOG"]
        S1["Giữ 1 bảng vật lý duy nhất trên S3 dưới định danh 3 cấp: prod.gold.customer_sales"]
        S2["[+] Cấp quyền tại chỗ bằng SQL DCL hoặc Delta Sharing (Zero-copy)<br/>[+] Reprocess Đơn #8888 đúng 1 lần, cả 40 đội nhóm thấy ngay mà tốn $0 phí mạng dư thừa!"]
        S1 --> S2
    end""",

        "7.3c": """flowchart TD
    BASE["BẢNG GỐC DUY NHẤT TRÊN S3: prod.gold.customer_sales<br/>• Dòng 1: order_id=8888 | Nguyễn Văn A | phone=0909-123-456 | Bình Dương | 15.000.000đ<br/>• Dòng 2: order_id=9999 | Trần Thị B | phone=0918-888-999 | TP.HCM | 20.000.000đ"]
    RLS["1. Giám đốc Chi nhánh Bình Dương (ROW-LEVEL SECURITY / ROW FILTER)<br/>[+] Chỉ thấy dòng có province = 'Bình Dương' (Đơn #8888), ẩn hoàn toàn Đơn #9999"]
    MASK["2. Chuyên viên Phân tích Data Analyst (COLUMN-LEVEL MASKING)<br/>[+] Thấy cả 2 đơn #8888 và #9999, nhưng cột PII phone_number tự động hiện 'xxxx-xxx-456'"]
    BASE --> RLS & MASK""",

        "7.3d": """flowchart LR
    subgraph HOT ["1. TẦNG NÓNG (HOT TIER)"]
        H1["Bảng Gold & Silver đang truy vấn BI/ML hàng ngày<br/>S3 Standard / GCS Standard + Cache NVMe SSD/RAM<br/>Chi phí: ~$0.020 – $0.023/GB/tháng"]
    end
    subgraph WARM ["2. TẦNG ẤM (WARM TIER)"]
        W1["Bảng Silver / Bronze ít truy cập sau 30–90 ngày<br/>S3 Standard-IA / GCS Nearline / Cool Blob<br/>Chi phí: ~$0.010 – $0.0125/GB/tháng (Giữ >= 30 ngày)"]
    end
    subgraph COLD ["3. TẦNG LẠNH (COLD / ARCHIVAL)"]
        C1["Bảng Bronze quá hạn 6–12 tháng (giữ để Audit/Replay)<br/>S3 Glacier Instant / Deep Archive / GCS Archive<br/>Chi phí: ~$0.004 – $0.001/GB/tháng (Rẻ bằng 1/6 đến 1/17 giá!)"]
    end
    HOT -->|"Sau 30–90 ngày"| WARM -->|"Sau 180–365 ngày"| COLD""",

        "7.4": """flowchart BT
    L1["TẦNG 1: PHYSICAL HARDWARE & STORAGE MODELS (Chặng 1, 2 & 3)<br/>CPU Cache (1 ns) -> RAM (100 ns, Spill) -> SSD (100 us) -> HDD (4-10 ms) | File vs Block vs Object (S3 ~100 ms) & HDFS (x3)"]
    L2["TẦNG 2: FILE FORMATS, IN-MEMORY & COMPRESSION PRIMITIVES (Chặng 2)<br/>Row (CSV, JSON, Avro + Sync Markers) vs Columnar (Parquet Footer/RowGroup, ORC) | Apache Arrow (Zero-copy) | Snappy, ZSTD"]
    L3["TẦNG 3: OPEN TABLE FORMATS — BỘ NÃO GIAO DỊCH LAKEHOUSE (Chặng 5 & 6)<br/>Delta Lake (_delta_log) | Apache Iceberg (3-layer Metadata) | Apache Hudi (Timeline + Index) | ACID, MVCC/OCC, COW/MOR, Z-Order, Vacuum"]
    L4["TẦNG 4: COMPUTE & STREAMING ENGINES — TÁCH RỜI STORAGE (Chặng 3 & 6)<br/>Batch & MPP: Spark, Trino, Snowflake, BigQuery, Fabric | Streaming & Cache: Debezium CDC -> Kafka -> Flink (RocksDB / Redis)"]
    L5["TẦNG 5: DATA ORGANIZATION & MODELING — MEDALLION & KIMBALL (Chặng 4 & 7)<br/>Bronze (Raw Append-only/Replay + _corrupt) -> Silver (Cleaned ~3NF/SCD2) -> Gold (Star Schema / OBT, Surrogate Key, Bus Matrix)"]
    L6["TẦNG 6: CONSUMPTION & GOVERNANCE UNDERCURRENTS (Chặng 4 & 7)<br/>Phục vụ: Power BI, Tableau, SQL, Data Science, AI/ML | Quản trị ngầm: Unity Catalog, OpenLineage, Row/Col Security, GDPR, FinOps"]
    L1 --> L2 --> L3 --> L4 --> L5 --> L6""",
    }

    linux_ascii = build_linux_ascii_diagrams()
    linux_mermaid = {
        "0.1": """flowchart LR
    subgraph S12 ["1–2. TỪ TĨNH SANG ĐỘNG & VƯỢT RANH GIỚI KERNEL"]
        B1["[BƯỚC 1 — CHẶNG 1] Từ Tĩnh sang Động:<br/>• Gõ lệnh tĩnh trên Terminal (Quầy lễ tân)<br/>• Shell (Bash) đánh thức Program (/bin/grep)<br/>• Nạp lên RAM/CPU thành Process đang chạy"]
        B2["[BƯỚC 2 — CHẶNG 2] Va chạm Ranh giới Bảo mật:<br/>• Process trình phiếu System Call (open/read)<br/>• Linux Kernel xét 5 thuộc tính căn cước:<br/>  PID, UID/GID, Working Dir, Env, Open Files<br/>• Mở kho /var/log/app.log trên cây thư mục /"]
        B1 --> B2
    end
    subgraph S34 ["3–4. NỐI ỐNG PIPE (IPC) & TỰ ĐỘNG HÓA 24/7"]
        B3["[BƯỚC 3 — CHẶNG 3] Phối hợp Dây chuyền IPC:<br/>• Một mình grep không xuể -> nối ống Pipe (|)<br/>• Qua 3 cổng: stdin(0), stdout(1), stderr(2)<br/>• Tách riêng luồng lỗi (2>&1), không bẩn kết quả"]
        B4["[BƯỚC 4 — CHẶNG 4] Tự động hóa Công nghiệp:<br/>• Bash Script (.sh): Định nghĩa làm bước nào<br/>• GCC & Makefile: Xét timestamp có làm lại?<br/>• Cronjob (crond): Quét mỗi 60s chạy 03:00 sáng"]
        B3 --> B4
    end
    S12 -->|"Luồng dữ liệu & tự động hóa"| S34""",

        "0.2": """flowchart TD
    subgraph C1 ["[CHẶNG 1] KHỞI NGUỒN & LUỒNG CHẠY 1 LỆNH (grep ERROR /var/log/app.log)"]
        T1["[1] TERMINAL (Quầy giao tiếp): Nhận phím & in kết quả"] --> T2["[2] SHELL / BASH (Người nhận việc): Phân tách lệnh"]
        T2 --> T3["[3] PROGRAM (Công thức đĩa): File nhị phân /bin/grep"] --> T4["[4] PROCESS (Đầu bếp chạy trên RAM & CPU)"]
    end
    subgraph C2 ["[CHẶNG 2] HỒ SƠ CĂN CƯỚC PROCESS & KHO HÀNG /"]
        P_ID["HỒ SƠ CĂN CƯỚC PROCESS:<br/>• PID & User/Group (UID/GID: root / me)<br/>• Working Dir (cwd) + Environment ($PATH)<br/>• Open Files (Bảng File Descriptors 0, 1, 2)"]
        FS["BẢN ĐỒ KHO HÀNG (UNIFIED FILESYSTEM /):<br/>• /bin, /sbin, /usr (Program) | /home, /root, /etc (Cấu hình)<br/>• /var/log, /tmp (Kho log & Bàn tạm) | /proc (0 MB Disk trên RAM)"]
        P_ID --> FS
    end
    T4 --> P_ID
    SYSCALL["[5] SYSTEM CALL (Phiếu xin cấp phát tài nguyên: open, read, write, fork, execve, pipe, dup2...)"]
    KERNEL["[6] LINUX KERNEL (Bếp trưởng tối cao / Quản lý kho)<br/>Kiểm tra đường dẫn + Quyền (UID/GID) + Cấp phát 4 trụ cột phần cứng:<br/>1. FILE ('Everything is a file') | 2. CPU (Scheduling) | 3. RAM (Memory & Pipe 64KB) | 4. NETWORK (Socket)"]
    T4 & FS --> SYSCALL --> KERNEL
    subgraph C3 ["[CHẶNG 3] PHỐI HỢP ĐA TIẾN TRÌNH (IPC & I/O)"]
        IPC["Ba cổng chuẩn: stdin(0), stdout(1), stderr(2)<br/>[Process 1: stdout(1)] --(Đường ống Pipe trong Kernel RAM)--> [stdin(0): Process 2]<br/>Tách riêng luồng lỗi stderr(2) & điều hướng (>, >>, 2>&1)"]
    end
    subgraph C4 ["[CHẶNG 4] ĐÓNG GÓI & TỰ ĐỘNG HÓA 24/7"]
        AUTO["Tam giác Tự động hóa:<br/>[1] BASH SCRIPT (.sh): Định nghĩa 'Làm những bước nào'<br/>[2] GCC & MAKEFILE: Dịch .c -> .o -> binary; xét timestamp 'Có cần làm lại?'<br/>[3] CRONJOB (crond): Thức dậy mỗi 60s, xét lịch (* * * * *) 'Khi nào kích hoạt'"]
    end
    KERNEL --> C3 --> C4""",

        "1.1a": """flowchart TD
    GNU["1. DỰ ÁN GNU (Richard Stallman, 1983 - 'Khung sườn xe')<br/>• [+] Bash: Màn hình dòng lệnh (CLI Shell)<br/>• [+] Coreutils: Bộ lệnh ls, cp, mv, rm, grep...<br/>• [+] GCC & GDB: Dịch code C/C++ -> 0/1 & soi lỗi<br/>• [+] glibc: Thư viện hàm C bọc System Call<br/>• [!] NỖI ĐAU: Khuyết mất quả tim hạt nhân (Kernel)!"]
    KERN["2. HẠT NHÂN LINUX (Linus Torvalds, 1991 - 'Cục máy')<br/>• [+] CPU Scheduler: Chia lượt xử lý tiến trình<br/>• [+] Memory Mgmt: Cấp phát & cách ly vùng RAM<br/>• [+] VFS & File System: Quản lý kho tệp (ext4/xfs)<br/>• [+] Device Control: Điều khiển đĩa, phím, mạng<br/>• [!] NỖI ĐAU: Không có công cụ để con người bấm!"]
    OS["3. HỆ ĐIỀU HÀNH HOÀN CHỈNH: GNU/LINUX (Kế thừa UNIX 1969 & POSIX / GPLv2)<br/>• Người dùng gõ lệnh 'grep ERROR app.log' qua bộ công cụ GNU (Bash + /bin/grep + glibc)<br/>• Hạt nhân Linux Kernel điều khiển ổ cứng & CPU đọc tệp trả kết quả an toàn tuyệt đối"]
    GNU & KERN -->|"Ghép Khung sườn GNU + Cục máy Linux"| OS""",

        "1.1b": """flowchart TD
    ROOT["TẠI SAO HẠ TẦNG SERVER, CLOUD & SIÊU MÁY TÍNH CHỌN GNU/LINUX? (6 TRỤ CỘT)"]
    P1["1. OPEN SOURCE ($0 LICENSE)<br/>• Mã nguồn mở GPLv2 công khai<br/>• $0 phí bản quyền cho 1.000 server<br/>• Hàng triệu chuyên gia cùng vá lỗi"]
    P2["2. MULTI-USER & MULTI-TASK<br/>• 50 dev SSH vào chung 1 server<br/>• Chạy 24/7 quanh năm không Reboot<br/>• Không giẫm chân vùng nhớ"]
    P3["3. SECURITY & STABILITY<br/>• Khóa quyền User thường vs. root<br/>• Ranh giới cứng User (Ring 3) vs. Kernel (Ring 0)<br/>• Miễn nhiễm phần lớn mã độc"]
    P4["4. GRANULAR RESOURCE CTRL<br/>• Kiểm soát tới từng milimet (cgroups)<br/>• Ép sát giới hạn ứng dụng chỉ dùng<br/>  tối đa 10% CPU và 1 GB RAM"]
    P5["5. PORTABILITY (KHẢ CHUYỂN)<br/>• Tách rời GUI, cực kỳ nhẹ<br/>• Chạy từ Router Wifi, Android tới<br/>  100% siêu máy tính TOP500 & Cloud"]
    P6["6. COMMUNITY & ECOSYSTEM<br/>• Kho gói chuẩn hóa (apt, dnf, Docker)<br/>• Nền tảng gốc của hệ sinh thái<br/>  Data & AI/ML (Spark, Kafka, K8s)"]
    ROOT --> P1 & P2 & P3 & P4 & P5 & P6""",

        "1.2a": """flowchart TD
    CORE["LÕI CỐT LÕI: GNU TOOLS + LINUX KERNEL"]
    DEB["1. NHÁNH DEBIAN (Nền tảng 'Nồi đồng cối đá')<br/>• Chạy 10 năm bền bỉ không sập<br/>• Trình quản lý gói: dpkg / apt (.deb)"]
    ENT["2. NHÁNH DOANH NGHIỆP (Fedora / RHEL)<br/>• 'Xe bọc thép' cho Ngân hàng, Viễn thông<br/>• Trình quản lý gói: rpm / dnf (.rpm)<br/>• Thuê bao hỗ trợ chuyên gia 24/7"]
    ARCH["3. NHÁNH TỰ LẮP RÁP (Arch Linux)<br/>• Quản lý gói: pacman (Rolling-release)<br/>• Tự gõ lệnh lắp từng con ốc vít từ số 0"]
    subgraph DEB_FAM ["BA BẢN PHÂN PHỐI PHÁI SINH PHỔ BIẾN TỪ NỀN DEBIAN"]
        U["[1] UBUNTU ('Xe máy quốc dân IT')<br/>Cập nhật 6 tháng/lần + bản LTS (5–12 năm) cho Cloud, Data & AI/ML"]
        M["[2] LINUX MINT ('Ngôi nhà ấm áp')<br/>Giao diện Cinnamon giống Windows 7/10, cài sẵn LibreOffice, VLC, Codecs"]
        K["[3] KALI LINUX ('Hộp đồ nghề Hacker')<br/>Cài sẵn hàng trăm công cụ PenTest (Wireshark, Nmap)"]
    end
    CORE --> DEB & ENT & ARCH
    DEB --> DEB_FAM""",

        "1.2b": """flowchart LR
    subgraph LAYERS ["1. CẤU TRÚC 4 LỚP BÊN TRONG MỘT DISTRO"]
        L4["[Lớp 4] Giao diện & Ứng dụng:<br/>Desktop GUI (GNOME, Cinnamon) hoặc Server thuần SSH CLI"]
        L3["[Lớp 3] Trình quản lý gói (Package Manager):<br/>Tự động tải & giải quyết phụ thuộc (apt/.deb vs. dnf/.rpm)"]
        L2["[Lớp 2] Hệ thống Khởi động & Bộ công cụ GNU:<br/>systemd (PID 1) + glibc + Bash + Coreutils (grep, ls, cp)"]
        L1["[Lớp 1] Hạt nhân Linux Kernel (vmlinuz) + Device Drivers"]
        L4 --> L3 --> L2 --> L1
    end
    subgraph TRADE ["2. BA ĐÁNH ĐỔI KHI CHỌN DISTRO VẬN HÀNH app.log"]
        T1["• Tiện lợi đóng gói sẵn:<br/>Mint (cài sẵn Office/VLC) vs. Kali (PenTest) vs. Arch (tự lắp)"]
        T2["• Bảo hành thương mại 24/7:<br/>RHEL (Thu phí Subscription) vs. Cộng đồng mở miễn phí"]
        T3["• Chuẩn cân bằng cho Kỹ sư Data/AI:<br/>Ubuntu LTS (Miễn phí 100%, nhân gọn nhẹ, kho gói Cloud/AI lớn nhất)"]
        T1 --> T2 --> T3
    end
    LAYERS -->|"Định hình hương vị Distro"| TRADE""",

        "1.3a": """flowchart TD
    subgraph USER ["TẦNG 3 & 2: USER SPACE (Ring 3 — Bị cấm chạm thẳng phần cứng)"]
        S1["[1] TERMINAL (Quầy giao tiếp): Nhận gõ 'grep ERROR app.log' & hiển thị kết quả"]
        S2["[2] SHELL / BASH (Người nhận việc): Phân tách lệnh 'grep', mẫu 'ERROR', file 'app.log'<br/>(Phân cấp: Shell nói chung -> Bash thuộc GNU -> Bash Script tự động)"]
        S3["[3] PROGRAM (Công thức tĩnh trên đĩa): File nhị phân /bin/grep"]
        S4["[4] PROCESS (Người đầu bếp đang chạy trên RAM & CPU): Sinh ra qua fork() + execve()"]
        S1 --> S2 --> S3 --> S4
    end
    S5["[5] SYSTEM CALL (Phiếu đăng ký xin tài nguyên: open, read, write)"]
    subgraph KERN ["TẦNG 1: KERNEL SPACE (Ring 0 — Bếp trưởng tối cao)"]
        S6["[6] LINUX KERNEL (Quản lý kho & Tài nguyên tối cao):<br/>Kiểm tra đường dẫn 'app.log' + Xét duyệt quyền đọc + Cấp phát phần cứng"]
    end
    subgraph HW ["[7] PHẦN CỨNG VẬT LÝ (HARDWARE RESOURCES)"]
        H_FILE["FILE (Sổ ghi chép: app.log)"]
        H_CPU["CPU (Não thực hiện phép tính)"]
        H_RAM["RAM (Bộ nhớ tạm giữ mọi thứ)"]
        H_NET["NETWORK (Kênh trao đổi máy khác)"]
    end
    S4 --> S5 --> S6 --> H_FILE & H_CPU & H_RAM & H_NET""",

        "1.3b": """flowchart LR
    subgraph STEP14 ["1. ĐÁNH THỨC PROCESS & TRÌNH PHIẾU SYSCALL (BƯỚC 1–4)"]
        B1["[Bước 1] Gõ lệnh tại Terminal: $ grep ERROR app.log"]
        B2["[Bước 2] Shell (Bash) phân tích cú pháp:<br/>Lệnh: grep | Chuỗi tìm: ERROR | File: app.log"]
        B3["[Bước 3] Khởi tạo Process từ Program (/bin/grep):<br/>[!] NỖI ĐAU: Process không có quyền tự thò tay xuống ổ cứng!"]
        B4["[Bước 4] Gửi phiếu System Call (open, read) xuống Kernel"]
        B1 --> B2 --> B3 --> B4
    end
    subgraph STEP56 ["2. PHÂN ĐỊNH RANH GIỚI KERNEL VS. PROCESS (BƯỚC 5–6)"]
        B5K["[Bước 5a — TRÁCH NHIỆM CỦA KERNEL]:<br/>Kiểm tra đường dẫn + quyền đọc, mở kho lấy khối dữ liệu từ app.log đưa lên RAM.<br/>(Kernel KHÔNG HỀ BIẾT chữ 'ERROR' là gì!)"]
        B5P["[Bước 5b — TRÁCH NHIỆM CỦA PROCESS]:<br/>Bản thân tiến trình grep dùng CPU tự dò từng dòng trên RAM để lọc dòng có chữ 'ERROR'"]
        B6["[Bước 6] Đẩy kết quả khớp về lại màn hình Terminal cho bạn!"]
        B5K --> B5P --> B6
    end
    STEP14 --> STEP56""",

        "2.1a": """flowchart LR
    subgraph SHELL ["1. QUY TRÌNH 3 BƯỚC CỦA SHELL (SLIDE 26)"]
        S1["[Bước 1] PARSE & EXPAND:<br/>Tách lệnh 'grep', mẫu 'ERROR', file 'app.log'<br/>Khai triển ký tự đại diện (*.log, ~, $VAR)"]
        S2["[Bước 2] SEARCH $PATH:<br/>Tra danh bạ $PATH=/usr/local/bin:/usr/bin:/bin<br/>==> Định vị trúng tệp thực thi: /bin/grep"]
        S3["[Bước 3] TRANSLATE TO SYSTEM CALLS:<br/>Gọi fork() nhân bản + execve('/bin/grep',...)<br/>để khai sinh Process mới trên RAM"]
        S1 --> S2 --> S3
    end
    subgraph IDCARD ["2. HỒ SƠ CĂN CƯỚC 5 THUỘC TÍNH CỦA PROCESS (task_struct)"]
        P1["[1] PID & PPID (Thẻ định danh):<br/>PID = 4821 (duy nhất) | PPID = 2105 (Bash)"]
        P2["[2] User & Group (UID / GID):<br/>UID = 1000 (fsds) | GID = 1000, 4 (adm)<br/>(root luôn có UID = 0 tối cao)"]
        P3["[3] Working Directory (cwd):<br/>cwd = /var/log (Gốc giải mã đường dẫn tương đối)"]
        P4["[4] Environment ($PATH, $HOME):<br/>Kế thừa biến môi trường từ cha Bash"]
        P5["[5] Open Files (Bảng FD Table):<br/>0=stdin | 1=stdout | 2=stderr | 3=/var/log/app.log"]
        P1 --> P2 --> P3 --> P4 --> P5
    end
    SHELL -->|"Khai sinh & Cấp căn cước"| IDCARD""",

        "2.1b": """flowchart LR
    subgraph LSL ["1. GIẢI PHẪU CHUỖI 10 KÝ TỰ PHÂN QUYỀN (SLIDE 28)"]
        CMD["$ ls -lh /var/log/app.log<br/>-rw-r----- 1 root adm 1.5G Oct 16 12:00 app.log"]
        T0["Ký tự 1 [-]: Loại File<br/>'-' = Regular File | 'd' = Directory"]
        U3["Ký tự 2-4 [rw-]: USER (Owner = root)<br/>r(4)+w(2)+0 = 6 (Đọc + Ghi)"]
        G3["Ký tự 5-7 [r--]: GROUP (Group = adm)<br/>r(4)+0+0 = 4 (Chỉ Đọc)"]
        O3["Ký tự 8-10 [---]: OTHERS (Người lạ)<br/>0+0+0 = 0 (Cấm toàn bộ)"]
        CMD --> T0 & U3 & G3 & O3
    end
    subgraph CHECK ["2. THUẬT TOÁN XÉT DUYỆT QUYỀN CỦA LINUX KERNEL"]
        C1["[Cổng 1] UID của Process == Owner (root)?<br/>Nếu khớp ==> Áp dụng quyền USER (rw-)"]
        C2["[Cổng 2] GID của Process thuộc nhóm (adm)?<br/>Nếu khớp ==> Áp dụng quyền GROUP (r--)"]
        C3["[Cổng 3] Rơi vào OTHERS (---):<br/>Chặn đứng & trả lỗi EACCES (Permission denied)!"]
        C1 -->|"Không khớp"| C2 -->|"Không khớp"| C3
    end
    LSL --> CHECK""",

        "2.2a": """flowchart TD
    PHIL["TRIẾT LÝ CỐT LÕI: 'EVERYTHING IS A FILE' (SLIDE 19)<br/>Mọi tài nguyên đều quy về giao diện luồng byte qua tầng VFS của Kernel:<br/>open() -> read() -> write() -> close()"]
    F1["1. REGULAR FILES (-)<br/>• /var/log/app.log<br/>• document.txt, script.sh<br/>• Chứa byte dữ liệu trên SSD"]
    F2["2. DIRECTORIES (d)<br/>• /var/log, /home/fsds<br/>• FUN FACT (Slide 19):<br/>  Chỉ là File chứa bảng ánh xạ<br/>  Tên file -> Số Inode!"]
    F3["3. DEVICE INTERFACES (b/c)<br/>• /dev/sda (Ổ đĩa cứng)<br/>• /dev/usb0, /dev/null<br/>• Cổng nối thẳng vào Driver"]
    F4["4. PROCESSES (/proc)<br/>• /proc/1234/status<br/>• /proc/meminfo, /proc/cpuinfo<br/>• File ảo trực tiếp trên RAM"]
    UNIF["SỨC MẠNH ĐỒNG NHẤT:<br/>Cùng 1 bộ lệnh (cat, grep, cp, echo) điều khiển được cả File log, Thiết bị lẫn Tiến trình!"]
    PHIL --> F1 & F2 & F3 & F4
    F1 & F2 & F3 & F4 --> UNIF""",

        "2.2b": """flowchart LR
    subgraph INODE ["1. BẢN CHẤT THƯ MỤC & INODE (SLIDE 19 FUN FACT)"]
        DIR["Tệp Thư mục (/var/log):<br/>Chỉ là bảng danh bạ 2 cột:<br/>• 'app.log'  --> Inode #94021<br/>• 'auth.log' --> Inode #94088"]
        INO["Inode #94021 (Siêu dữ liệu):<br/>• Owner: root:adm | Mode: 0640<br/>• Size: 1.5 GB | Links: 1<br/>• Con trỏ tới các khối đĩa SSD"]
        BLK["Data Blocks trên SSD:<br/>[2026-10-16 ERROR Db timeout...]<br/>(Chứa nội dung thực sự)"]
        DIR -->|"Trỏ số Inode"| INO -->|"Trỏ khối vật lý"| BLK
    end
    subgraph OPS ["2. CƠ HỌC ĐẰNG SAU LỆNH cp, mv VÀ rm (SLIDE 34–37)"]
        OP_CP["• Lệnh cp a.log b.log:<br/>  Tạo Inode mới + Chép toàn bộ Data Blocks"]
        OP_MV["• Lệnh mv old.log new.log (Cùng ổ đĩa):<br/>  Chỉ đổi chữ trong bảng Directory (0 byte copy, < 1 ms!)"]
        OP_RM["• Lệnh rm app.log (XÓA VĨNH VIỄN):<br/>  Gỡ dòng ánh xạ (unlink) + giải phóng Inode/Blocks.<br/>  [!] KHÔNG CÓ RECYCLE BIN! Cấm tuyệt đối: rm -rf /"]
        OP_CP --> OP_MV --> OP_RM
    end
    INODE --> OPS""",

        "2.3a": """flowchart TD
    ROOT["GỐC DUY NHẤT: / (Root Directory — Slide 20–22)"]
    subgraph USER_GRP ["1. KHU NHÀ Ở NGƯỜI DÙNG (USER FOLDERS — Slide 20)"]
        U_HOME["/home : Căn hộ riêng từng User<br/>(/home/fsds, /home/student1, /home/developer)"]
        U_ROOT["/root : Phủ riêng của Quản trị viên tối cao (root)<br/>(Tách biệt hoàn toàn khỏi /home)"]
    end
    subgraph SYS_GRP ["2. KHU HỆ THỐNG & CẤU HÌNH (SYSTEM FOLDERS — Slide 21)"]
        S_BIN["/bin & /sbin : Lệnh thiết yếu (/bin/grep, /bin/ls)<br/>& Lệnh quản trị hệ thống (/sbin/reboot)"]
        S_USR["/usr : Phần mềm dùng chung<br/>(/usr/bin/python, /usr/local)"]
        S_ETC["/etc : Sổ tay cấu hình văn bản<br/>(/etc/passwd, /etc/hosts, /etc/ssh)"]
        S_PROC["/proc : File ảo trên RAM (0 MB ổ đĩa!)<br/>(/proc/meminfo, /proc/cpuinfo, /proc/uptime)"]
    end
    subgraph VAR_GRP ["3. KHU TẠM & BIẾN ĐỔI LIÊN TỤC (TEMP & VARIABLE — Slide 22)"]
        V_TMP["/tmp : Bàn nháp tạm thời<br/>([!] Tự động xóa sạch khi Reboot!)"]
        V_VAR["/var : Dữ liệu phình to liên tục 24/7<br/>• /var/log/app.log (MỤC TIÊU SĂN LỖI!)<br/>• /var/www (Web) | /var/lib (Database)"]
    end
    ROOT --> USER_GRP & SYS_GRP & VAR_GRP""",

        "2.3b": """flowchart LR
    subgraph WIN ["1. KIẾN TRÚC WINDOWS: NHIỀU GỐC THEO Ổ ĐĨA VẬT LÝ"]
        W1["Ổ cứng 1 -> Gốc C:\\<br/>(C:\\Windows, C:\\Users)"]
        W2["Ổ cứng 2 -> Gốc D:\\<br/>(D:\\Logs\\app.log)"]
        W3["[!] NỖI ĐAU: Khi ổ D:\\ đầy, đổi sang E:\\Logs\\app.log<br/>làm gãy toàn bộ đường dẫn cứng trong code!"]
        W1 --> W2 --> W3
    end
    subgraph LNX ["2. KIẾN TRÚC LINUX: MỘT CÂY HỢP NHẤT DUY NHẤT (/)"]
        L1["Mọi ổ đĩa đều gắn (mount) vào các nhánh dưới gốc /:<br/>• SSD 1 gắn vào /<br/>• SSD 2 (10 TB) gắn thẳng vào /var/log"]
        L2["Đường dẫn Tuyệt đối (Absolute Path — Slide 30):<br/>Luôn bắt đầu từ gốc '/' ==> /var/log/app.log"]
        L3["Đường dẫn Tương đối (Relative Path — Slide 30):<br/>Tính từ Working Directory hiện tại (cwd) ==> app.log, ../etc"]
        L1 --> L2 --> L3
    end
    WIN -->|"Tiến hóa sang"| LNX""",

        "2.4a": """flowchart LR
    subgraph NAV ["1. NHÓM ĐIỀU HƯỚNG & QUAN SÁT (SLIDE 28–30)"]
        N1["• pwd : In đường dẫn tuyệt đối đang đứng"]
        N2["• ls  : Liệt kê thư mục<br/>  -l (chi tiết quyền/chủ) | -h (đơn vị K/M/G)<br/>  -a (hiện file ẩn .bashrc) | -t (xếp theo thời gian)"]
        N3["• cd  : Di chuyển vị trí đứng<br/>  cd ~ (về Home) | cd .. (lên cha) | cd - (quay lại chỗ cũ)"]
        N1 --> N2 --> N3
    end
    subgraph MANIP ["2. NHÓM TẠO, SAO CHÉP, DI CHUYỂN & XÓA (SLIDE 31–37)"]
        M1["• touch f.txt     : Tạo file rỗng mới / cập nhật timestamp<br/>• mkdir -p a/b/c  : Tạo liền chuỗi thư mục cha-con"]
        M2["• cp a.txt b.txt  : Sao chép file (dùng 'cp -r' cho thư mục)<br/>• mv old new      : Cùng thư mục = RENAME | Khác thư mục = MOVE"]
        M3["• rm file / rm -r : Xóa vĩnh viễn KHÔNG QUA RECYCLE BIN!<br/>  [!] CẤM TUYỆT ĐỐI: rm -rf /"]
        M1 --> M2 --> M3
    end
    NAV -->|"Định vị trúng đích rồi mới"| MANIP""",

        "2.4b": """flowchart LR
    subgraph VIEW ["1. CHIẾN THUẬT SOI FILE LOG KHỔNG LỒ (SLIDE 38–40)"]
        V1["• head -n 20 app.log :<br/>  Chỉ đọc 20 dòng ĐẦU TIÊN (mặc định 10 dòng)"]
        V2["• cat f1.txt f2.txt > merged.txt :<br/>  Đọc toàn bộ / ghép file ([!] Cấm dùng cat cho file hàng GB!)"]
        V3["• tail -n 20 app.log & tail -f app.log :<br/>  Đọc 20 dòng CUỐI hoặc canh dòng lỗi mới REAL-TIME (-f)"]
        V1 --> V2 --> V3
    end
    subgraph HUNT ["2. BỘ TỨ SĂN LÙNG DUNG LƯỢNG, BIẾN ĐỔI & CỨU HỘ (SLIDE 41–44)"]
        H1["• du -sh /var/log/* :<br/>  Đo tổng dung lượng từng thư mục để khoanh vùng ổ đĩa đầy"]
        H2["• find /var/log -name '*.log' -size +1G :<br/>  Truy lùng chính xác file .log nào nặng trên 1 GB"]
        H3["• sed 's/unix/linux/g' f.txt : Tìm & thay thế văn bản tự động<br/>• man <lệnh> : Mở cẩm nang tra cứu tại chỗ (bấm q để thoát)"]
        H1 --> H2 --> H3
    end
    VIEW --> HUNT""",

        "3.1a": """flowchart LR
    subgraph IN ["1. NGUỒN ĐẦU VÀO: stdin (FD 0)"]
        I1["• Bàn phím (Keyboard)<br/>• File dữ liệu (< file)<br/>• Đường ống Pipe (|)<br/>==> Đi vào Cổng 0 (stdin)"]
    end
    subgraph PROC ["2. PROCESS ĐANG CHẠY (VD: grep ERROR)"]
        P1["Bảng File Descriptor (FD Table):<br/>• [Cổng 0] stdin  (Nhập nguyên liệu)<br/>• [Cổng 1] stdout (Xuất kết quả sạch)<br/>• [Cổng 2] stderr (Báo cáo sự cố)"]
    end
    subgraph OUT ["3. HAI ĐẦU RA TÁCH BIỆT: FD 1 & FD 2"]
        O1["[Cổng 1] stdout (FD 1):<br/>Kết quả bình thường ra Màn hình / Pipe / File"]
        O2["[Cổng 2] stderr (FD 2):<br/>Thông báo lỗi đi đường riêng!<br/>Không bao giờ trộn lẫn vào Cổng 1"]
    end
    I1 -->|"stdin (0)"| P1
    P1 -->|"stdout (1)"| O1
    P1 -->|"stderr (2)"| O2""",

        "3.1b": """flowchart LR
    subgraph P1 ["1. PROCESS 1 (Ví dụ: grep ERROR)"]
        P1_IO["• Hút dữ liệu từ [stdin: 0]<br/>• Đẩy kết quả sạch ra [stdout: 1]"]
        P1_ERR["• Nếu gặp lỗi (Permission denied):<br/>  Xả qua [stderr: 2] đi đường riêng!"]
    end
    subgraph PIPE ["2. TRONG LÕI LINUX KERNEL (BỘ ĐỆM RAM)"]
        K_PIPE["• SHELL (Thợ lắp ống):<br/>  Nối cổng stdout (1) P1 -> stdin (0) P2<br/>• KERNEL (Giữ ống Pipe 64 KB trên RAM):<br/>  Truyền dòng byte trực tiếp, 0 Disk I/O!"]
    end
    subgraph P2 ["3. PROCESS 2 (Xử lý tiếp: wc -l)"]
        P2_IO["• Hút dòng byte sạch từ Pipe qua [stdin: 0]<br/>• Không bị làm bẩn bởi lỗi của Process 1<br/>• Xuất kết quả cuối ra [stdout: 1]"]
    end
    P1_IO -->|"stdout (1)"| K_PIPE -->|"stdin (0)"| P2_IO""",

        "3.2a": """flowchart LR
    subgraph DEFAULT ["[X] TRẠNG THÁI 1: CHẠY NGẦM MẶC ĐỊNH (BẪY MÙ LỖI)"]
        D1["$ /home/nam/tu_dong_backup.sh (lúc 03:00 sáng)"]
        D2["• [stdout: 1] Kết quả bình thường -> Không có Terminal -> MẤT DẤU VẾT!<br/>• [stderr: 2] Báo lỗi đỏ lòm -> Không có Terminal -> MẤT DẤU VẾT!"]
        D3["==> Sáng hôm sau kỹ sư mở máy: Sao lưu thất bại nhưng MÙ TỊT nguyên nhân!"]
        D1 --> D2 --> D3
    end
    subgraph REDIR ["[V] TRẠNG THÁI 2: ĐIỀU HƯỚNG THU GOM LOG (>> backup.log 2>&1)"]
        R1["$ /home/nam/tu_dong_backup.sh >> /var/log/backup.log 2>&1"]
        R2["• Bước 1 (>> /var/log/backup.log):<br/>  Hướng cổng [stdout: 1] ghi nối đuôi vào cuối file log"]
        R3["• Bước 2 (2>&1 — gọi dup2(1, 2)):<br/>  Bẻ cổng báo lỗi [stderr: 2] chập chung vào đúng đường ống của [&1]"]
        R4["==> Cả kết quả (1) lẫn báo lỗi (2) đều nằm gọn trong /var/log/backup.log!"]
        R1 --> R2 --> R3 --> R4
    end
    DEFAULT -->|"Khắc phục bằng"| REDIR""",

        "3.2b": """flowchart LR
    subgraph IO_OPS ["1. ĐIỀU HƯỚNG ĐẦU RA & ĐẦU VÀO (SLIDE 55)"]
        O1["• > file  : Ghi đè từ đầu (Xóa trắng lịch sử cũ - O_TRUNC)<br/>• >> file : Ghi nối đuôi vào cuối file (Giữ lịch sử cũ - O_APPEND)"]
        O2["• < file  : Đọc đầu vào từ file bơm vào stdin (0)<br/>• << EOF  : Here-Document bơm khối văn bản nhiều dòng vào stdin (0)"]
        O1 --> O2
    end
    subgraph ERR_OPS ["2. ĐIỀU HƯỚNG LỖI & CẠM BẪY THỨ TỰ 2>&1 (TLPI CH. 5.5)"]
        E1["• 2> error.log : Tách riêng cổng lỗi stderr (2) vào file lỗi riêng<br/>• 2>&1         : Chập cổng 2 vào đích hiện tại của cổng 1"]
        E2["[!] CẠM BẪY THỨ TỰ:<br/>• ĐÚNG: >> app.log 2>&1 (Cổng 1 vào file trước, cổng 2 theo cổng 1 vào file)<br/>• SAI : 2>&1 >> app.log (Cổng 2 trỏ màn hình cũ, rồi cổng 1 mới rẽ vào file!)"]
        E1 --> E2
    end
    IO_OPS --> ERR_OPS""",

        "4.0": """flowchart LR
    subgraph S1 ["[1] SHELL SCRIPT (.sh)"]
        B1["• Đóng gói chuỗi lệnh rời rạc vào 1 kịch bản<br/>• Trả lời câu hỏi cơ học:<br/>  'CẦN LÀM NHỮNG BƯỚC NÀO?'<br/>• Tự kiểm tra if/else & lặp qua các server"]
    end
    subgraph S2 ["[2] MAKE (Makefile)"]
        B2["• Đối chiếu thời gian sửa file (Timestamp mtime)<br/>• Trả lời câu hỏi cơ học:<br/>  'FILE NÀO VỪA SỬA, CÓ CẦN BIÊN DỊCH LẠI KHÔNG?'<br/>• Tránh biên dịch thừa 99 file không đổi"]
    end
    subgraph S3 ["[3] CRONJOB (crond)"]
        B3["• Tiến trình ngầm crond canh đồng hồ 24/7<br/>• Trả lời câu hỏi cơ học:<br/>  'KHI NÀO BẮT ĐẦU KÍCH HOẠT?'<br/>• Đúng 02:00 sáng tự động gọi Script & Make"]
    end
    S1 -->|"Kết hợp với"| S2 -->|"Hẹn giờ tự chạy bằng"| S3""",

        "4.1a": """flowchart LR
    subgraph HIER ["1. PHÂN CẤP: SHELL --> BASH --> BASH SCRIPT (.sh)"]
        H1["[Cấp 1] SHELL ('Xe hơi nói chung' — Slide 46):<br/>Trình thông dịch lệnh giữa Người & Kernel (sh, bash, zsh, fish)"]
        H2["[Cấp 2] BASH ('Xe Mec / BMW' — Bourne-Again SHell):<br/>Loại Shell mặc định phổ biến nhất thuộc dự án GNU"]
        H3["[Cấp 3] BASH SCRIPTING ('Tờ giấy dán tủ lạnh'):<br/>File kịch bản .sh ghi sẵn bước 1..10 để Bash đọc & làm một mạch!"]
        H1 --> H2 --> H3
    end
    subgraph ANAT ["2. GIẢI PHẪU KỊCH BẢN MẪU backup.sh (SLIDE 51–58)"]
        A1["• Dòng 1 (Shebang): #!/bin/bash (Gọi /bin/bash thực thi)<br/>• Biến (Variables): TEN='Nam' (Không có khoảng trắng quanh dấu =)"]
        A2["• Nhánh điều kiện : if [ -f \"$FILE\" ]; then ... else ... fi<br/>• Vòng lặp tự động: for SERVER in server1 server2 server3; do ... done"]
        A3["• 2 Cách kích hoạt chạy (Slide 51):<br/>  - Cách 1: $ bash backup.sh<br/>  - Cách 2: $ chmod +x backup.sh && ./backup.sh"]
        A1 --> A2 --> A3
    end
    HIER --> ANAT""",

        "4.1b": """flowchart LR
    subgraph EDIT ["1. TRÌNH SOẠN THẢO CLI: NANO VS. VIM (SLIDE 48–50)"]
        ED1["• NANO (Đơn giản, hiện phím tắt ở đáy màn hình):<br/>  Ctrl+O (^O): Lưu file | Ctrl+X (^X): Thoát<br/>  Ctrl+K (^K): Cắt dòng | Ctrl+U (^U): Dán dòng"]
        ED2["• VIM (Mạnh mẽ, chia 3 chế độ):<br/>  Normal Mode (mặc định: dd xóa dòng, u hoàn tác)<br/>  --> Bấm 'i' vào Insert Mode (gõ code)<br/>  --> Bấm 'ESC' về Normal --> Gõ ':wq' (Lưu) hoặc ':q!' (Hủy)"]
        ED1 --> ED2
    end
    subgraph SYNTAX ["2. SỐ HỌC (( )), MẢNG & HÀM BASH (SLIDE 56–63)"]
        SY1["[!] Cạm bẫy so sánh chuỗi vs số (Slide 56):<br/>• [[ 10 > 9 ]] --> FALSE! (So thứ tự chữ cái ASCII: '1' < '9')<br/>• (( 10 > 9 )) --> TRUE!  (So sánh số học chuẩn xác)"]
        SY2["• Mảng (Arrays — Slide 60): my_array=(10 2 300)<br/>  Đầu: ${my_array[0]} | Cuối: ${my_array[-1]} | Độ dài: ${#my_array[@]}"]
        SY3["• Hàm & Mã thoát (Slide 61–62):<br/>  Đối số $1, $2 | Biến local | Mã thoát $? (0 = Thành công)"]
        SY1 --> SY2 --> SY3
    end
    EDIT --> SYNTAX""",

        "4.2a": """flowchart LR
    subgraph FOUR ["1. BỐN GIAI ĐOẠN BIÊN DỊCH CỦA GCC (SLIDE 65–67)"]
        G1["Mã nguồn C/C++ (chao.c / demo2.cpp):<br/>Con người đọc hiểu (#include, int main)"]
        G2["[Bước 1] Pre-processor (.c --> .i): Bung #include, xóa comment<br/>[Bước 2] Compiler (.i --> .s): Dịch sang hợp ngữ Assembly<br/>[Bước 3] Assembler (.s --> .o): Đúc file mã máy trung gian (Object file)"]
        G1 --> G2
    end
    subgraph LINK ["2. LINKER & FILE THỰC THI ELF 64-BIT (SLIDE 66)"]
        L1["[Bước 4] Linker (Ghép các file .o + Thư viện chuẩn libc):<br/>$ gcc chao.c -o chuong_trinh_chao"]
        L2["Kiểm tra định dạng bằng lệnh file (Slide 66):<br/>$ file chuong_trinh_chao<br/>--> ELF 64-bit LSB shared object, x86-64"]
        L3["Chạy trực tiếp trên CPU với tốc độ tối đa:<br/>$ ./chuong_trinh_chao"]
        L1 --> L2 --> L3
    end
    FOUR --> LINK""",

        "4.2b": """flowchart LR
    subgraph RULE ["1. CẤU TRÚC MAKEFILE & LUẬT THÉP PHÍM [TAB] (SLIDE 69)"]
        R1["Cấu trúc quy tắc:<br/>target: prerequisites<br/>[TAB]recipe"]
        R2["Ví dụ thực tế:<br/>ung_dung: main.o ham_phu.o<br/>[TAB]gcc main.o ham_phu.o -o ung_dung"]
        R3["[!] LUẬT THÉP: Dòng lệnh Recipe BẮT BUỘC thụt đầu dòng<br/>bằng phím [TAB] (dùng Space sẽ báo lỗi 'missing separator'!)"]
        R1 --> R2 --> R3
    end
    subgraph MTIME ["2. SO SÁNH TIMESTAMP (mtime) & NHÃN .PHONY (SLIDE 70–71)"]
        M1["Cơ chế đối chiếu đồng hồ (mtime) của Make:<br/>• main.c (10:05) > main.o (09:00) --> BIÊN DỊCH LẠI main.o!<br/>• ham_phu.c (08:00) < ham_phu.o (09:00) --> BỎ QUA (Không dịch thừa)!"]
        M2["Khai báo nhãn tác vụ .PHONY (Slide 71):<br/>.PHONY: all clean build test run deploy<br/>Giúp lệnh 'make clean' (rm -f *.o ung_dung) luôn chạy chuẩn xác"]
        M1 --> M2
    end
    RULE --> MTIME""",

        "4.3a": """flowchart LR
    subgraph CONCEPTS ["1. BỐN KHÁI NIỆM: CRON, CRONTAB, CRONJOB, CROND"]
        C1["• Cron    : Toàn bộ hệ thống hẹn giờ tự động trên Linux<br/>• Crontab : Cuốn sổ lịch trình (crontab -e sửa | -l xem | -r xóa)"]
        C2["• Cronjob : Từng dòng công việc cụ thể hẹn giờ trong sổ<br/>• Crond   : Anh bảo vệ chạy ngầm 24/7, thức dậy đúng mỗi 60 giây!"]
        C1 --> C2
    end
    subgraph STARS ["2. NĂM DẤU SAO (* * * * *) TỪ NHỎ ĐẾN LỚN (SLIDE 73–74)"]
        S1["Cú pháp: [Phút] [Giờ] [Ngày] [Tháng] [Thứ] <Lệnh><br/>• Trường 1: Phút (0 - 59)  | Trường 2: Giờ (0 - 23)<br/>• Trường 3: Ngày (1 - 31)  | Trường 4: Tháng (1 - 12)<br/>• Trường 5: Thứ  (0 - 6 hoặc 0 - 7, Chủ Nhật = 0 hoặc 7)"]
        S2["4 Ký tự điều khiển (Slide 73):<br/>* (Mọi giá trị) | , (Danh sách: 1,3,5) | - (Khoảng: 9-17) | / (Bước nhảy: */5)"]
        S1 --> S2
    end
    CONCEPTS --> STARS""",

        "4.3b": """flowchart LR
    subgraph TRAPS ["1. CHU KỲ CROND 60 GIÂY & 3 CẠM BẪY KINH ĐIỂN"]
        T1["Mỗi 60 giây crond quét sổ Crontab --> Khớp giờ --> Kích hoạt!"]
        T2["3 Cạm bẫy làm Cronjob 'chết im lặng' lúc 02:00 sáng:<br/>1. Quên đường dẫn tuyệt đối (/usr/bin/python3, /home/nam/backup.sh)<br/>2. Quên thu gom log & lỗi (>> /var/log/backup.log 2>&1)<br/>3. Đặt nhầm sổ Crontab (crontab -e của User vs sudo crontab -e của Root)"]
        T1 --> T2
    end
    subgraph LIMITS ["2. HAI GIỚI HẠN CỐT TỬ CỦA CRONJOB & GIẢI PHÁP (SLIDE 75–76)"]
        L1["[Giới hạn 1] No Auto-Retry (Lỗi mạng không tự chạy lại — Slide 75):<br/>--> Giải pháp: Bọc vòng lặp Retry 3 lần trong Bash Script<br/>    (for ((i=1; i<=3; i++)); do ./backup.sh && exit 0; sleep 60; done)"]
        L2["[Giới hạn 2] Missed Jobs khi máy tắt nguồn (Slide 75–76):<br/>--> Giải pháp: Dùng Anacron hoặc systemd Timers<br/>    (tự động chạy bù khi bật máy, tích hợp journald & kiểm tra mạng)"]
        L1 --> L2
    end
    TRAPS --> LIMITS""",
    }

    import html as html_lib
    import re
    import textwrap

    visuals_dir = ROOT / "assets" / "visuals"
    visuals_dir.mkdir(parents=True, exist_ok=True)

    def strip_html_tags(text: str) -> str:
        cleaned = re.sub(r"<br\s*/?>", " · ", text or "", flags=re.IGNORECASE)
        cleaned = re.sub(r"<[^>]+>", "", cleaned)
        return html_lib.unescape(cleaned).strip()

    def build_style2_svg_infographic(
        safe_id: str,
        title_txt: str,
        diag_key: str,
        mermaid_code: str,
        ascii_code: str,
        caption_txt: str,
        tmpl: str,
    ) -> str:
        palettes = [
            ("#06b6d4", "#0e2936", "#67e8f9"),  # Cyan
            ("#10b981", "#0d2b24", "#6ee7b7"),  # Emerald
            ("#f59e0b", "#2e210d", "#fcd34d"),  # Amber
            ("#f43f5e", "#31131e", "#fda4af"),  # Coral
            ("#a855f7", "#241435", "#d8b4fe"),  # Purple
        ]
        subgraphs = []
        current_sg = None
        for raw_line in (mermaid_code or "").splitlines():
            line = raw_line.strip()
            sg_match = re.match(r'^subgraph\s+[A-Za-z0-9_]+\s*\["([^"]+)"\]', line)
            if sg_match:
                current_sg = {"title": strip_html_tags(sg_match.group(1)), "nodes": []}
                subgraphs.append(current_sg)
                continue
            if line == "end":
                current_sg = None
                continue
            for node_match in re.finditer(r'[A-Za-z0-9_]+\s*\[(?:"([^"]+)"|([^\]]+))\]', line):
                raw_lbl = node_match.group(1) or node_match.group(2) or ""
                parts = [
                    strip_html_tags(p)
                    for p in re.split(r"<br\s*/?>", raw_lbl, flags=re.IGNORECASE)
                    if strip_html_tags(p)
                ]
                if not parts:
                    continue
                if current_sg is None:
                    current_sg = {"title": f"ARCHITECTURAL STAGE · {diag_key}", "nodes": []}
                    subgraphs.append(current_sg)
                current_sg["nodes"].append(parts[:4])

        if not subgraphs:
            subgraphs = [{"title": strip_html_tags(title_txt), "nodes": [[strip_html_tags(caption_txt)[:110]]]}]

        sg_list = subgraphs[:4]
        num_sg = len(sg_list)
        total_w = 1504
        gap = 24
        col_w = int((total_w - gap * (num_sg - 1)) / max(1, num_sg))

        # Extract quantitative metrics & key tokens from Mermaid + Caption for the Telemetry Strip
        combined_text = strip_html_tags(f"{title_txt} {mermaid_code} {caption_txt}")
        metric_matches = re.findall(
            r"(?:#8888|\b\d+(?:\.\d+)?\s*(?:ns|ms|s|KB|MB|GB|TB|PB|%|x|B|rows|cols|days|mins)\b|ACID|MVCC|OCC|COW|MOR|Parquet|Arrow|Iceberg|Delta|Hudi|SCD\s*Type\s*\d|3NF|Star\s*Schema|Inode|PID|Pipe|VFS)",
            combined_text,
            flags=re.IGNORECASE,
        )
        unique_metrics = []
        for m_tok in metric_matches:
            norm_m = re.sub(r"\s+", " ", m_tok.strip())
            if norm_m.upper() not in [u.upper() for u in unique_metrics]:
                unique_metrics.append(norm_m)
        if not unique_metrics:
            unique_metrics = ["Order #8888", f"Diagram {diag_key}", "Zero-Loss Architecture", "Style #2 Blueprint"]
        unique_metrics = unique_metrics[:6]

        svg_parts = [
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900">',
            "<defs>",
            '  <pattern id="bpgrid" width="32" height="32" patternUnits="userSpaceOnUse">',
            '    <path d="M 32 0 L 0 0 0 32" fill="none" stroke="#1e293b" stroke-width="0.9"/>',
            "  </pattern>",
            '  <linearGradient id="bggrad" x1="0" y1="0" x2="1" y2="1">',
            '    <stop offset="0%" stop-color="#0b1017"/>',
            '    <stop offset="55%" stop-color="#0f1722"/>',
            '    <stop offset="100%" stop-color="#0b131c"/>',
            "  </linearGradient>",
            '  <marker id="arrow-cyan" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
            '    <path d="M 0 1 L 9 5 L 0 9 z" fill="#06b6d4"/>',
            "  </marker>",
            "</defs>",
            '<rect width="1600" height="900" fill="url(#bggrad)"/>',
            '<rect width="1600" height="900" fill="url(#bpgrid)" opacity="0.75"/>',
            '<rect x="28" y="24" width="1544" height="852" rx="16" fill="none" stroke="#1e293b" stroke-width="2"/>',
            # Top Header Banner with Isometric Cube Emblem
            '<rect x="48" y="40" width="1504" height="92" rx="14" fill="#131c27" stroke="#06b6d4" stroke-width="1.6"/>',
            '<polygon points="92,58 118,72 118,100 92,114 66,100 66,72" fill="#0e2936" stroke="#06b6d4" stroke-width="1.8"/>',
            '<polyline points="66,72 92,86 118,72" fill="none" stroke="#67e8f9" stroke-width="1.4"/>',
            '<line x1="92" y1="86" x2="92" y2="114" stroke="#67e8f9" stroke-width="1.4"/>',
            f'<rect x="138" y="54" width="246" height="24" rx="6" fill="#0e2936" stroke="#06b6d4" stroke-width="1"/>',
            f'<text x="261" y="71" fill="#67e8f9" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11.5" font-weight="700" text-anchor="middle">STYLE #2 · {html_lib.escape(tmpl)}</text>',
            f'<text x="400" y="71" fill="#94a3b8" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" font-weight="700">VISUAL ASSET: {html_lib.escape(safe_id.upper())} · STATION {html_lib.escape(diag_key)}</text>',
            f'<text x="138" y="109" fill="#f8fafc" font-family="system-ui, -apple-system, sans-serif" font-size="21.5" font-weight="700">{html_lib.escape(strip_html_tags(title_txt)[:96])}</text>',
        ]

        # Full-Width Isometric Architectural Columns
        for idx, sg in enumerate(sg_list):
            stroke_c, fill_c, text_c = palettes[idx % len(palettes)]
            x0 = 48 + idx * (col_w + gap)
            y0 = 152
            box_h = 532
            # 3D Isometric shadow offset
            svg_parts.append(
                f'<rect x="{x0 + 5}" y="{y0 + 6}" width="{col_w}" height="{box_h}" rx="14" fill="#070b10" opacity="0.65"/>'
            )
            svg_parts.append(
                f'<rect x="{x0}" y="{y0}" width="{col_w}" height="{box_h}" rx="14" fill="#111923" stroke="{stroke_c}" stroke-width="2"/>'
            )
            svg_parts.append(
                f'<rect x="{x0}" y="{y0}" width="{col_w}" height="48" rx="14" fill="{fill_c}" stroke="{stroke_c}" stroke-width="1.5"/>'
            )
            # Stage Number Badge inside Column Header
            svg_parts.append(
                f'<circle cx="{x0 + 26}" cy="{y0 + 24}" r="13" fill="#0b1017" stroke="{stroke_c}" stroke-width="1.5"/>'
            )
            svg_parts.append(
                f'<text x="{x0 + 26}" y="{y0 + 29}" fill="{text_c}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" font-weight="700" text-anchor="middle">{idx + 1}</text>'
            )
            sg_title_short = sg["title"][: max(22, int((col_w - 60) / 8.2))]
            svg_parts.append(
                f'<text x="{x0 + 48}" y="{y0 + 29}" fill="{text_c}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="13" font-weight="700">{html_lib.escape(sg_title_short)}</text>'
            )

            nodes = sg["nodes"][:4]
            if not nodes:
                nodes = [["Architectural Component"]]
            ny = y0 + 66
            avail_h = box_h - 82
            nh = min(124, int((avail_h - 16 * (len(nodes) - 1)) / max(1, len(nodes))))
            for n_idx, node_lines in enumerate(nodes):
                svg_parts.append(
                    f'<rect x="{x0 + 16}" y="{ny}" width="{col_w - 32}" height="{nh}" rx="10" fill="#162230" stroke="{stroke_c}" stroke-opacity="0.65" stroke-width="1.4"/>'
                )
                svg_parts.append(
                    f'<rect x="{x0 + 16}" y="{ny}" width="6" height="{nh}" rx="3" fill="{stroke_c}"/>'
                )
                wrap_w = max(24, int((col_w - 64) / 7.5))
                rendered_lines = []
                for nl in node_lines:
                    rendered_lines.extend(textwrap.wrap(nl, width=wrap_w)[:2])
                rendered_lines = rendered_lines[:4]
                for l_idx, l_txt in enumerate(rendered_lines):
                    ly = ny + 26 + l_idx * 22
                    fw = "700" if l_idx == 0 else "400"
                    fc = "#f8fafc" if l_idx == 0 else "#cbd5e1"
                    svg_parts.append(
                        f'<text x="{x0 + 34}" y="{ly}" fill="{fc}" font-family="system-ui, -apple-system, sans-serif" font-size="13.5" font-weight="{fw}">{html_lib.escape(l_txt)}</text>'
                    )
                if n_idx < len(nodes) - 1:
                    mid_x = x0 + col_w // 2
                    svg_parts.append(
                        f'<line x1="{mid_x}" y1="{ny + nh}" x2="{mid_x}" y2="{ny + nh + 14}" stroke="{stroke_c}" stroke-width="2"/>'
                    )
                ny += nh + 16

            # Horizontal glowing flow connector between columns
            if idx < num_sg - 1:
                ax1 = x0 + col_w + 2
                ax2 = x0 + col_w + gap - 4
                ay = y0 + box_h // 2
                svg_parts.append(
                    f'<line x1="{ax1}" y1="{ay}" x2="{ax2}" y2="{ay}" stroke="#06b6d4" stroke-width="2.5" marker-end="url(#arrow-cyan)"/>'
                )

        # Quantitative Telemetry & Key Entities Strip (y = 702..758)
        svg_parts.append(
            '<rect x="48" y="702" width="1504" height="58" rx="10" fill="#0f1824" stroke="#334155" stroke-width="1.4"/>'
        )
        svg_parts.append(
            '<text x="68" y="736" fill="#fcd34d" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" font-weight="700">KEY METRICS &amp; INVARIANTS:</text>'
        )
        bx = 290
        for m_idx, m_val in enumerate(unique_metrics):
            stroke_c, fill_c, text_c = palettes[m_idx % len(palettes)]
            bw = max(130, min(215, len(m_val) * 9 + 34))
            if bx + bw > 1536:
                break
            svg_parts.append(
                f'<rect x="{bx}" y="714" width="{bw}" height="34" rx="8" fill="{fill_c}" stroke="{stroke_c}" stroke-width="1.2"/>'
            )
            svg_parts.append(
                f'<text x="{bx + bw // 2}" y="736" fill="{text_c}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12.5" font-weight="700" text-anchor="middle">{html_lib.escape(m_val)}</text>'
            )
            bx += bw + 14

        # Bottom Takeaway / Caption Footer (y = 774..856)
        clean_cap = strip_html_tags(caption_txt)
        cap_lines = textwrap.wrap(clean_cap, width=142)[:2] or [strip_html_tags(title_txt)]
        svg_parts.append(
            '<rect x="48" y="774" width="1504" height="82" rx="12" fill="#131c27" stroke="#10b981" stroke-width="1.5"/>'
        )
        svg_parts.append(
            '<text x="68" y="800" fill="#6ee7b7" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11.5" font-weight="700">CAUSAL MECHANISM &amp; ARCHITECTURAL TAKEAWAY:</text>'
        )
        for c_idx, c_line in enumerate(cap_lines):
            svg_parts.append(
                f'<text x="68" y="{824 + c_idx * 21}" fill="#e2e8f0" font-family="system-ui, -apple-system, sans-serif" font-size="13.5">{html_lib.escape(c_line)}</text>'
            )

        svg_parts.append("</svg>")
        return "\n".join(svg_parts)

    call_pattern = re.compile(
        r'buildVisualBlock\(\s*"((?:[^"\\]|\\.)*)"\s*,\s*"((?:[^"\\]|\\.)*)"\s*,\s*d\["([^"]+)"\]\.ascii\s*,\s*d\["([^"]+)"\]\.mermaid\s*,\s*"((?:[^"\\]|\\.)*)"\s*\)',
        re.DOTALL,
    )

    spine_ids = {
        "linux-0-1",
        "linux-0-2",
        "linux-2-map",
        "linux-2-summary",
        "linux-3-map",
        "linux-4-0",
        "storage-0-1",
    }

    visual_assets = {}
    for m in call_pattern.finditer(HTML_TEMPLATE):
        raw_id, title_txt, diag_key, _, caption_txt = m.groups()
        safe_id = re.sub(r"[^a-zA-Z0-9_-]", "_", raw_id)
        is_linux = safe_id.startswith("linux")
        role = "spine" if safe_id in spine_ids else "diagram"

        story_kw = re.search(
            r"(bếp|kitchen|bẫy|trap|case|sự cố|đánh đổi|vs\.|so sánh|silent|ngầm|cạm bẫy|nỗi đau|swamp|đầm lầy)",
            f"{title_txt} {caption_txt}",
            re.IGNORECASE,
        )
        tmpl = "PROMPT-STORY-ANALOGY" if story_kw else "PROMPT-ARCH-DIAGRAM"

        jpg_candidate = visuals_dir / f"{safe_id}.jpg"
        if safe_id == "storage-0-1":
            preview_src = "assets/visuals/storage-0-map.jpg"
            status = "ready"
            badge_lbl = f"READY · {tmpl}"
        elif jpg_candidate.exists():
            preview_src = f"assets/visuals/{safe_id}.jpg"
            status = "ready"
            badge_lbl = f"READY · {tmpl}"
        else:
            m_code = linux_mermaid.get(diag_key, "") if is_linux else storage_mermaid.get(diag_key, "")
            a_code = (
                linux_ascii.get(diag_key, {}).get("ascii", "")
                if is_linux
                else storage_ascii.get(diag_key, {}).get("ascii", "")
            )
            svg_content = build_style2_svg_infographic(
                safe_id, title_txt, diag_key, m_code, a_code, caption_txt, tmpl
            )
            svg_path = visuals_dir / f"{safe_id}.svg"
            svg_path.write_text(svg_content, encoding="utf-8")
            preview_src = f"assets/visuals/{safe_id}.svg"
            status = "ready"
            badge_lbl = f"READY · {tmpl}"

        if tmpl == "PROMPT-STORY-ANALOGY":
            prompt_str = (
                f"[PROMPT-STORY-ANALOGY]\n"
                f"Generate a vivid, engaging, high-resolution 16:9 widescreen dark-slate storytelling illustration "
                f"(#0f1419 background with warm Amber #f59e0b, Cyan #06b6d4, Emerald #10b981, and Coral #f43f5e highlights).\n"
                f"TITLE: \"{title_txt}\"\n"
                f"SCENARIO & CAUSAL STORY: {strip_html_tags(caption_txt)}\n"
                f"STYLE: Style #2 Isometric Storytelling Infographic — map every visual metaphor 1:1 to exact technical entities, "
                f"ports, commands, and quantitative Before/After metrics."
            )
        else:
            prompt_str = (
                f"[PROMPT-ARCH-DIAGRAM]\n"
                f"Generate a clean, high-resolution 16:9 widescreen technical infographic / architecture diagram "
                f"on a deep dark-slate engineering blueprint background (#0f1419) with crisp Cyan (#06b6d4), Emerald (#10b981), "
                f"Amber (#f59e0b), and Coral (#f43f5e) accents.\n"
                f"TITLE: \"{title_txt}\"\n"
                f"ARCHITECTURE & MECHANICS: {strip_html_tags(caption_txt)}\n"
                f"STYLE: Style #2 Dark-Slate Engineering Blueprint — crisp vector-like schematic/isometric blocks, "
                f"exact English technical labels, ports, commands, and zero visual clutter."
            )

        visual_assets[safe_id] = {
            "id": safe_id,
            "diagramKey": diag_key,
            "src": preview_src,
            "previewSrc": preview_src,
            "status": status,
            "role": role,
            "template": tmpl,
            "badgeLabel": badge_lbl,
            "alt": title_txt,
            "prompt": prompt_str,
        }

    from glossary_scanner import scan_build_hub
    glossary_payload = scan_build_hub(ROOT / "scripts" / "build_hub.py")

    data_out = {
        "storage_diagrams": {
            k: {
                "kind": storage_ascii[k]["kind"],
                "ascii": storage_ascii[k]["ascii"],
                "mermaid": storage_mermaid[k],
            }
            for k in storage_ascii
        },
        "linux_diagrams": {
            k: {
                "kind": linux_ascii[k]["kind"],
                "ascii": linux_ascii[k]["ascii"],
                "mermaid": linux_mermaid[k],
            }
            for k in linux_ascii
        },
        "visual_assets": visual_assets,
        "glossary": {
            "entries": glossary_payload["entries"],
            "lookup": glossary_payload["lookup"],
            "stats": glossary_payload["stats"],
        },
    }

    content_dir = ROOT / "content"
    content_dir.mkdir(parents=True, exist_ok=True)
    (content_dir / "lessons-data.json").write_text(
        json.dumps(data_out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (content_dir / "glossary-data.json").write_text(
        json.dumps(glossary_payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    html = (
        HTML_TEMPLATE
        .replace("__FONT_FACES__", extract_font_faces())
        .replace("__HUB_DATA_JSON__", json.dumps(data_out, ensure_ascii=False))
    )
    (ROOT / "fsds-learning-hub.html").write_text(html, encoding="utf-8")
    unique_srcs = len({v["previewSrc"] for v in visual_assets.values()})
    g_stats = glossary_payload["stats"]
    print(
        f"Built fsds-learning-hub.html ({len(html):,} bytes), content/lessons-data.json, "
        f"{len(visual_assets)} visual_assets ({unique_srcs} unique images), and "
        f"glossary ({g_stats['total_canonical_entries']} canonical entries, {g_stats['total_lookup_keys']} lookup keys, "
        f"{g_stats['unclassified_count']} unclassified) successfully."
    )


if __name__ == "__main__":
    main()

