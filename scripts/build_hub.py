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
    Embeds all WOFF2 fonts declared in assets/fonts/fonts.css (Anthropic Sans, Serif,
    Mono with 100% static Vietnamese glyphs, plus JetBrains Mono & Anthropicons) as Base64
    data URIs, alongside macOS Terminal.app SF Mono OpenType fonts. Inlining as data URIs
    guarantees identical rendering over both file:// and http:// with zero CORS errors
    and zero fallback to incomplete macOS system fonts.
    """
    import re

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
    local_woff2_css = ""
    fonts_css_path = ROOT / "assets" / "fonts" / "fonts.css"
    if fonts_css_path.exists():
        raw_css = fonts_css_path.read_text(encoding="utf-8").strip()

        def _inline_woff2(match: re.Match) -> str:
            rel_path = match.group(1)
            woff_path = ROOT / rel_path
            if woff_path.exists():
                b64_woff = base64.b64encode(woff_path.read_bytes()).decode("ascii")
                return f'url("data:font/woff2;base64,{b64_woff}")'
            return match.group(0)

        local_woff2_css = re.sub(r'url\(["\']?(assets/fonts/[^"\')]+)["\']?\)', _inline_woff2, raw_css) + "\n  "
    if rules:
        return local_woff2_css + "\n  ".join(rules)
    return local_woff2_css


def build_storage_ascii_diagrams() -> dict:
    diagrams = {
        '0.1': {"ascii": '====================================================================================================\n      HÀNH TRÌNH 7 CHẶNG CỦA ĐƠN HÀNG #8888 (15.000.000 VNĐ) XUYÊN SUỐT TẦNG LƯU TRỮ DỮ LIỆU\n====================================================================================================\n\n  [CHẶNG 1: PHẦN CỨNG & VẬT LÝ]          [CHẶNG 2: MÔ HÌNH & ĐỊNH DẠNG TỆP]     [CHẶNG 3: HỆ PHÂN TÁN & DWH]\n  ┌──────────────────────────────┐       ┌──────────────────────────────┐       ┌──────────────────────────┐\n  │ • CPU Cache (1ns) -> RAM     │       │ • File vs Block vs Object S3 │       │ • HDFS NameNode/DataNode │\n  │   (100ns, Memory Spill)      │ ────► │ • Row (CSV/Avro) vs Columnar │ ────► │   (3x Replication, Rack) │\n  │ • SSD (100us) vs HDD (4ms)   │       │   (Parquet Footer, Arrow)    │       │ • Kafka Append-only Log  │\n  │ • Random Seek vs Seq Scan    │       │ • Compression & Splittable   │       │ • Data Warehouse & 3 Nỗi │\n  └──────────────────────────────┘       └──────────────────────────────┘       └─────────────┬────────────┘\n                                                                                              │\n                                                                                              ▼\n  [CHẶNG 7: MEDALLION & GOVERNANCE]      [CHẶNG 6: DATA LAKEHOUSE (ACID)]       [CHẶNG 4 & 5: MODELING & LAKE]\n  ┌──────────────────────────────┐       ┌──────────────────────────────┐       ┌──────────────────────────┐\n  │ • Bronze (Raw) -> Silver     │       │ • Delta Lake (_delta_log),   │       │ • Inmon vs Kimball (Star │\n  │   (Cleaned) -> Gold (OBT/BI) │ ◄──── │   Iceberg (3-tier), Hudi     │ ◄──── │   Schema, Fact/Dim, SCD2)│\n  │ • Unity Catalog, Lineage,    │       │ • MVCC / OCC / NBCC, Time    │       │ • Data Lake (Schema-on-  │\n  │   RLS/Masking & Cloud FinOps │       │   Travel, COW vs MOR, Z-Order│       │   Read) -> Data Swamp!   │\n  └──────────────────────────────┘       └──────────────────────────────┘       └──────────────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '1.1': {"ascii": '                        THÁP ĐỘ TRỄ VẬT LÝ & CÁC TÁC VỤ THỰC TẾ\n           │                                            ▲\n           │                                           / \\\n  ~1 ns    │ L1 CPU Cache                             /L1 \\                    ◄── Đọc thanh ghi / chỉ lệnh CPU tức thời\n  ~10 ns   │ L2 / L3 CPU Cache                       / CPU \\                       Băng thông: ~1 TB/s | Giá: Cực đắt (On-die)\n───────────┼────────────────────────────────────────/───────\\──────────────────────────────────────────────────────────────\n  ~100 ns  │ RAM (DDR5 / DRAM)                     /RAM DDR5 \\                 ◄── Đọc từ bộ nhớ đệm Redis (Redis read)\n  (0.1 µs) │                                      / ~100 GB/s \\                    Hàng triệu IOPS | Giá: ~$10 / GB\n───────────┼─────────────────────────────────────/─────────────\\───────────────────────────────────────────────────────────\n  ~10 µs   │ Mạng nội bộ 1 Gbps                 / Network 1Gbps \\              ◄── Memcached gửi gói tin qua mạng LAN\n  ~100 µs  │ NVMe SSD (Flash)                  /  SSD (~4 GB/s)  \\             ◄── RocksDB read (~0.1 ms) | Giá: ~$0.20/GB\n  ~1 ms    │ Ghi CSDL giao dịch               /  Database Insert  \\            ◄── PostgreSQL thực hiện lệnh INSERT\n───────────┼─────────────────────────────────/─────────────────────\\───────────────────────────────────────────────────────\n  ~4–10 ms │ Đĩa từ cơ học (HDD)            /  HDD (~200-300 MB/s)  \\          ◄── Kim đĩa từ di chuyển tìm rãnh (Seek)\n           │ Giới hạn ~100 IOPS            /     Giá: ~$0.03/GB      \\\n───────────┼──────────────────────────────/───────────────────────────\\────────────────────────────────────────────────────\n  ~100 ms  │ Cloud Object & WAN          /   Object Storage (S3/GCS)   \\       ◄── Gói tin xuyên lục địa (CA -> NL -> CA)\n  ~10 s    │ Chu kỳ làm mới Grafana     /     ~3 GB/s* | ~$0.02/GB      \\          hoặc cuộc gọi Zoom quốc tế\n───────────┼───────────────────────────/─────────────────────────────────\\─────────────────────────────────────────────────\n  ~12 giờ  │ Lưu trữ lạnh (Archival)  /       Cloud Archival / Tape       \\    ◄── Phục hồi sao lưu dài hạn\n           │                         └─────────────────────────────────────┘       Giá: ~$0.004/GB/tháng (rẻ bằng ~1/17)', "kind": 'pyramid'},
        '1.2': {"ascii": '====================================================================================================\n  ┌─────────────────────────────────────────────────────────────────────┐\n  │    Dữ liệu 10 triệu đơn hàng đẩy vào RAM của Node tính toán Spark   │\n  └──────────────────┬──────────────────────────────────────────────────┘\n                     │\n                     ├──► [+] Đủ dung lượng RAM\n                     │        └──► Xử lý ở tốc độ ~100 ns (~100 GB/s) ──► Hoàn tất cực nhanh!\n                     │\n                     └──► [!] Vượt quá dung lượng RAM (Ví dụ: Phép JOIN hoặc GROUP BY quá lớn)\n                              │\n                              ▼\n                    ┌──────────────────────────────────────────────────────────────────────┐\n                    │ [!] SPILL-TO-DISK (Tràn bộ nhớ xuống đĩa cứng cục bộ SSD / HDD)      │\n                    │ • Tốc độ rơi tự do từ 100 ns xuống 100 µs (SSD) hoặc 4–10 ms (HDD)   │\n                    │ • Tốn thêm CPU để tuần tự hóa (Serialize) từ RAM xuống đĩa & đọc lại │\n                    └──────────────────────────────────────────────────────────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '1.2b': {"ascii": '==================================================================================================================================\n  1. KHÔNG GIAN ĐỊA CHỈ CPU & RAM             2. TỤ ĐIỆN DRAM & TÍNH KHẢ BIẾN             3. ĐỘNG CƠ IN-MEMORY & BỀN VỮNG\n┌────────────────────────────────────────┐  ┌────────────────────────────────────────┐  ┌────────────────────────────────────────┐\n│ • Ánh xạ thẳng vào không gian          │  │ • Lưu bit trong tụ điện DRAM siêu      │  │ • Dùng làm tầng Đệm Nóng (Cache):      │\n│   địa chỉ của CPU (Address Space)      │  │   nhỏ, cần nạp làm tươi liên tục       │  │   - Redis (Cấu trúc + RDB/AOF)         │\n│ • Chứa cả Mã lệnh (Code) lẫn           │  │ • Tính khả biến (Volatile):            │  │   - Memcached (Key-Value thuần)        │\n│   Dữ liệu (Data) đang xử lý            │  │   [Mất điện < 1 giây]                  │  │   - Hazelcast (In-Memory Grid)         │\n│   (Kiến trúc Von Neumann/Harvard)      │  │       └──> Bốc hơi 100% dữ liệu!       │  │ • Đơn #8888 bắt buộc phải đồng thời    │\n│ • Băng thông: ~100 GB/s (DDR5)         │  │ • Bắt buộc dùng ECC RAM trên máy       │  │   ghi xuống đĩa bền vững (SSD/S3)      │\n│   Độ trễ: ~100 ns (Nhanh 1.000x SSD)   │  │   chủ để chống lật bit (Bit rot)       │  │   để không mất đơn khi sập nguồn!      │\n└────────────────────────────────────────┘  └────────────────────────────────────────┘  └────────────────────────────────────────┘\n==================================================================================================================================', "kind": 'boxes'},
        '1.3': {"ascii": '==========================================================================================================\n  1. RANDOM SEEK (Truy xuất ngẫu nhiên từng dòng)         2. SEQUENTIAL SCAN (Quét tuần tự liền mạch)\n┌─────────────────────────────────────────────────┐     ┌────────────────────────────────────────────────┐\n│ Đầu đọc đĩa phải liên tục di chuyển tìm vị      │     │ Đầu đọc chỉ cần định vị 1 lần, sau đó đọc      │\n│ trí của từng đơn hàng nằm rải rác trên đĩa:     │     │ trượt một mạch qua các dữ liệu nằm liền kề:    │\n│                                                 │     │                                                │\n│  [Đơn #12] ──(Seek 4-10ms)──> [Đơn #8888]       │     │  [Đơn #8886] -> [Đơn #8887] -> [Đơn #8888]...  │\n│      ▲                             │            │     │  ══════════════════════════════════════════>   │\n│      └───────(Seek 4-10ms)─────────┘            │     │  Đạt tối đa băng thông vật lý: 200–300 MB/s    │\n│                                                 │     │                                                │\n│ [x] Bị bóp nghẹt bởi giới hạn ~100 IOPS!        │     │ [+] Tận dụng tối đa Maximum Bandwidth của đĩa! │\n└─────────────────────────────────────────────────┘     └────────────────────────────────────────────────┘\n==========================================================================================================', "kind": 'boxes'},
        '1.3b': {"ascii": '====================================================================================================================\n  BÍ MẬT 1: ĐỌC SONG SONG HÀNG NGHÌN Ổ ĐĨA (~3 GB/s)          BÍ MẬT 2: TẠI SAO ARCHIVAL CHUNG ĐĨA MÀ RẺ 1/17?\n┌──────────────────────────────────────────────────────┐    ┌──────────────────────────────────────────────────────┐\n│ • 1 ổ đĩa HDD đơn lẻ chỉ đọc được: ~200 MB/s         │    │ • Cùng chạy trên 1 cụm ổ đĩa vật lý (10 TB,          │\n│ • Cloud Object Storage băm nhỏ & rải tệp lớn         │    │   100 IOPS, 200 MB/s), nhưng tách gói bán:           │\n│   ra HÀNG NGHÌN Ổ ĐĨA trên khắp Data Center:         │    │   - Gói Standard (~$0.02/GB): Mua trọn IOPS          │\n│     [Ổ đĩa 1: 200 MB/s] ──┐                          │    │     & Băng thông để đọc tức thì (~100 ms).           │\n│     [Ổ đĩa 2: 200 MB/s] ──┼──> Đọc song song         │    │   - Gói Archival (~$0.004/GB — rẻ bằng 1/17):        │\n│     [... 1.000 ổ đĩa ] ──┘    đạt ~3 GB/s!           │    │     Chỉ mua phần Dung lượng (Capacity) dư thừa,      │\n│ • Điểm nghẽn chuyển từ Đĩa sang Mạng & CPU!          │    │     chờ ~12 giờ lúc đĩa rảnh IOPS mới lấy ra!        │\n└──────────────────────────────────────────────────────┘    └──────────────────────────────────────────────────────┘\n====================================================================================================================', "kind": 'boxes'},
        '1.4': {"ascii": '=====================================================================================================\n  [HOT TIER] Lưu trữ Nóng           [WARM TIER] Lưu trữ Ấm             [COLD / ARCHIVAL] Lưu trữ Lạnh\n┌───────────────────────────┐     ┌────────────────────────────┐     ┌──────────────────────────────┐\n│ • Phần cứng: RAM / SSD    │     │ • Phần cứng: Cloud Object  │     │ • Phần cứng: Glacier / Tape  │\n│ • Giá: $0.20 – $10 / GB   │     │ • Giá: ~$0.02 / GB / tháng │     │ • Giá: ~$0.004 / GB / tháng  │\n│ • Độ trễ: 100 ns – 100 µs │ ──> │ • Độ trễ: ~100 ms          │ ──> │ • Độ trễ: ~12 giờ chờ        │\n│ • Dữ liệu: Đơn #8888 vừa  │     │ • Dữ liệu: Lịch sử đơn     │     │ • Dữ liệu: Hóa đơn cũ từ     │\n│   đặt, đang xử lý nóng    │     │   hàng phục vụ chạy        │     │   3–10 năm trước cất giữ     │\n│   hoặc nạp đệm tính toán  │     │   báo cáo & pipeline tuần  │     │   để kiểm toán pháp lý       │\n└───────────────────────────┘     └────────────────────────────┘     └──────────────────────────────┘\n=====================================================================================================', "kind": 'boxes'},
        '1.5': {"ascii": '============================================================================================================\n  HỆ THỐNG NGUỒN (SOURCE SYSTEM - OLTP)                 HỆ THỐNG LƯU TRỮ PHÂN TÍCH (STORAGE SYSTEM - OLAP)\n┌──────────────────────────────────────────────┐      ┌────────────────────────────────────────────────────┐\n│ [*] Mục tiêu: Ghi nhận giao dịch Đơn #8888   │      │ [*] Mục tiêu: Quét 10 triệu đơn tính tổng doanh số │\n│ • Thao tác: INSERT / UPDATE / đọc vài dòng   │ ───> │ • Thao tác: Quét tuần tự (Sequential Scan) lớn     │\n│ • Độ trễ yêu cầu: Cực thấp (~1 ms insert)    │ Tách │ • Định dạng: Lưu theo CỘT (Columnar) để chỉ đọc    │\n│ • Định dạng: Lưu theo DÒNG (Row-oriented)    │ biệt │   cột cần tính toán và nén dung lượng cực cao      │\n│ • Mô hình: Chuẩn hóa (Normalized) nhiều bảng │      │ • Mô hình: Phi chuẩn hóa (Denormalized) giảm JOIN  │\n│ • Phần cứng: NVMe SSD / Block Storage        │      │ • Phần cứng: Cloud Object Storage + Cụm phân tán   │\n└──────────────────────────────────────────────┘      └────────────────────────────────────────────────────┘\n============================================================================================================', "kind": 'boxes'},
        '2.1': {"ascii": '====================================================================================================\n       ĐỐI CHIẾU 3 MÔ HÌNH LƯU TRỮ: FILE STORAGE (NAS) vs. BLOCK STORAGE (SAN) vs. OBJECT STORAGE\n====================================================================================================\n\n   1. FILE STORAGE (NAS / Local)      2. BLOCK STORAGE (SAN / EBS)       3. OBJECT STORAGE (S3 / ADLS / GCS)\n   [Cây thư mục phân cấp]             [Các khối byte kích thước cố định] [Không gian phẳng - Flat Namespace]\n\n            / (Root)                        [Tệp Dữ Liệu Lớn]              [+] Bucket: "ashley-data-lake"\n            ├── KinhDoanh                           │                      ┌───────────────────────────────┐\n            │   └── 2026                     ┌──────┼──────┐               │ [ID] "orders/8888.parquet"    │\n            │       └── DonHang.csv          ▼      ▼      ▼               ├───────────────────────────────┤\n            └── NhanSu                    [Blk 1][Blk 2][Blk 3]            │ [Meta] Tùy biến vô hạn:       │\n                                          (512KB)(512KB)(512KB)            │  • ChiNhanh: "BinhDuong"      │\n   • HĐH duyệt con trỏ (pointer) qua                                       │  • LoaiDon : "BanLe"          │\n     từng cấp thư mục từ gốc          • Mỗi Block có Unique ID riêng       ├───────────────────────────────┤\n   • Quá tải mục lục khi số lượng     • Độ trễ cực thấp (<1ms) cho DB      │ [Data] Chuỗi byte nhị phân    │\n     tệp vượt hàng chục triệu           nhưng đắt & khó mở rộng            │  bất biến (Immutable Object)  │\n                                                                           └───────────────────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '2.1b': {"ascii": '=============================================================================================================\n  1. BẤT BIẾN (IMMUTABILITY = LOCK-FREE)                 2. CONSISTENCY, VERSIONING & LIFECYCLE\n┌────────────────────────────────────────────────┐     ┌────────────────────────────────────────────────────┐\n│ • Không sửa tại chỗ, không ghi nối đuôi        │ ──> │ • Strong Read-After-Write Consistency:             │\n│   ──> Ghi 1 lần thành luồng byte BẤT BIẾN      │ ──> │   Đọc ngay sau khi PUT luôn thấy bản mới nhất      │\n│ • Lợi ích vàng: Bỏ hoàn toàn khóa tệp (Lock    │ ──> │ • Object Versioning (Key + Version ID):            │\n│   free) ──> Đọc/ghi luồng song song ~3 GB/s    │ ──> │   Lưu bản sao nguyên khối (Brute-force full        │\n│   & Tách rời Compute khỏi Storage!             │ ──> │   copy) ──> Ghi đè tệp 10 GB x 100 lần = 1 TB!     │\n│ • Hỗ trợ HTTP Range Request đọc riêng phần     │ ──> │ • Bắt buộc gắn Lifecycle Policy:                   │\n│   Footer của tệp Parquet mà không tải cả tệp   │ ──> │   Standard ($0.02) ──> IA ──> Glacier ($0.001)     │\n└────────────────────────────────────────────────┘     └────────────────────────────────────────────────────┘\n=============================================================================================================', "kind": 'boxes'},
        '2.2a': {"ascii": '====================================================================================================\n        ĐỐI CHIẾU CƠ HỌC BỐ TRÍ THEO HÀNG (ROW-ORIENTED) vs. THEO CỘT (COLUMN-ORIENTED)\n====================================================================================================\n\n                        BẢNG LOGIC (LOGICAL TABLE - ĐƠN HÀNG #8886..#8889)\n                    ┌────────┬──────────┬──────────┐\n                    │  col1  │   col2   │   col3   │ (Ví dụ: OrderID | Province | Amount)\n                    ├────────┼──────────┼──────────┤\n             row1   │   1    │    2     │    3     │ (Đơn #8886)\n             row2   │   4    │    5     │    6     │ (Đơn #8887)\n             row3   │   7    │    8     │    9     │ (Đơn #8888)\n             row4   │   10   │    11    │    12    │ (Đơn #8889)\n                    └────────┴──────────┴──────────┘\n\n  1. BỐ TRÍ THEO HÀNG (ROW-ORIENTED: CSV, SEQUENCEFILE, AVRO)\n  Lưu toàn bộ các cột của từng hàng nằm liền kề nhau trên đĩa:\n  ┌─────────────┬─────────────┬─────────────┬──────────────┐\n  │  1 | 2 | 3  │  4 | 5 | 6  │  7 | 8 | 9  │ 10 | 11 | 12 │\n  └─────────────┴─────────────┴─────────────┴──────────────┘\n       row 1         row 2         row 3         row 4\n\n  2. BỐ TRÍ THEO CỘT THEO PHÂN ĐOẠN (COLUMN-ORIENTED: PARQUET, ORC, RCFILE)\n  Chia bảng thành các cụm hàng (Row Splits / Row Groups), rồi gom từng cột nằm liền kề nhau:\n  ┌────────────────────────────────────────────────────────┬───────────────────────────────────────┐\n  │                 Row Group / Split 1                    │          Row Group / Split 2          │\n  ├──────────────────┬───────────────────┬─────────────────┼───────────────────┬───────────────────┤\n  │ col1: [ 1 | 4 ]  │  col2: [ 2 | 5 ]  │ col3: [ 3 | 6 ] │ col1: [ 7 | 10 ]  │ col2: [ 8 | 11 ]  │\n  └──────────────────┴───────────────────┴─────────────────┴───────────────────┴───────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '2.2b': {"ascii": '====================================================================================================\n  CẤU TRÚC VẬT LÝ BÊN TRONG TỆP APACHE PARQUET\n┌──────────────────────────────────────────────────────────────────────────────────────────┐\n│ [1] HEADER: Ký hiệu ma thuật 4-byte "PAR1" (Nhận diện định dạng tệp Parquet)             │\n│ ──────────────────────────────────────────────────────────────────────────────────────   │\n│ [2] ROW GROUP 1 (Phân đoạn hàng 1 — ví dụ 128 MB – 1 GB dữ liệu):                        │\n│     ├── Column Chunk [OrderID]  ──> [Page Header | Data Page 1] [Data Page 2] ...        │\n│     ├── Column Chunk [Province] ──> [Dictionary Page] [Data Page 1 (RLE/Bit-pack)]       │\n│     └── Column Chunk [Amount]   ──> [Data Page 1] [Data Page 2] ...                      │\n│ ──────────────────────────────────────────────────────────────────────────────────────   │\n│ [3] ROW GROUP 2 (Phân đoạn hàng 2 — nơi chứa Đơn hàng #8888):                            │\n│     ├── Column Chunk [OrderID]  ──> [Data Page 1 (Min: 5001, Max: 9999)] ...             │\n│     └── Column Chunk [Amount]   ──> [Data Page 1] ...                                    │\n│ ──────────────────────────────────────────────────────────────────────────────────────   │\n│ [4] FOOTER METADATA (Nằm ở ĐÁY tệp — Động cơ truy vấn luôn đọc phần này ĐẦU TIÊN!):      │\n│     • Schema của bảng, phiên bản & cấu trúc Dremel (Definition / Repetition Levels)      │\n│     • Thống kê từng Column Chunk: Min, Max, Null Count (Dùng để nhảy cóc Data Skipping)  │\n│     • Con trỏ vị trí byte (Byte Offset) bắt đầu của từng Row Group & Column Chunk        │\n│     • Kết thúc bằng độ dài Footer (4-byte) + Ký hiệu ma thuật 4-byte "PAR1"              │\n└──────────────────────────────────────────────────────────────────────────────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '2.3': {"ascii": '====================================================================================================\n          ĐỊNH DẠNG CỘT TRÊN BỘ NHỚ RAM: APACHE ARROW & CƠ CHẾ ĐỌC TRỰC TIẾP ZERO-COPY\n====================================================================================================\n\n  [x] TRƯỚC KHI CÓ APACHE ARROW (Tốn 70-80% CPU dịch và chép vùng nhớ trên RAM):\n  [Vùng nhớ Spark / JVM] ──(Serialize)──► [Byte trung gian] ──(Deserialize)──► [Vùng nhớ Python / C++]\n\n  [+] KHI DÙNG APACHE ARROW (Xử lý Zero-Copy trực tiếp trên RAM):\n  ┌─────────────────────────────────────────────────────────────────────────┐\n  │       VÙNG NHỚ CỘT CHUẨN HÓA APACHE ARROW TRÊN RAM (Dùng chung)         │\n  │  • Cột OrderID: [8886, 8887, 8888]  |  Cột Amount: [5M, 12M, 15M]       │\n  │  • Hỗ trợ kỹ thuật Shredding để tách phẳng dữ liệu lồng nhau trên RAM   │\n  └───────────────────▲─────────────────────────────────▲───────────────────┘\n                      │ Đọc trực tiếp (Zero-copy)       │ Đọc trực tiếp (Zero-copy)\n              [ Apache Spark ]                  [ Python / Pandas / ML ]\n====================================================================================================', "kind": 'boxes'},
        '2.4': {"ascii": '====================================================================================================\n      ĐỐI CHIẾU NÉN KHỐI ĐƠN (NON-SPLITTABLE GZIP) vs. ĐÓNG GÓI KHỐI NỘI BỘ (SPLITTABLE PARQUET)\n====================================================================================================\n\n  [x] THẢM HỌA: Nén khối đơn (Non-Splittable File - Ví dụ: "orders.csv.gz" nén bằng Gzip)\n  ┌─────────────────────────────────────────────────────────────────────────────────────┐\n  │ [Dữ liệu bị mã hóa nối đuôi nhau thành 1 khối duy nhất từ Byte đầu đến Byte cuối]   │\n  └────────▲────────────────────────────────────────────────────────────────────────────┘\n           │ Không một máy nào có thể nhảy vào giữa tệp để giải nén vì không biết mốc bắt đầu!\n     [Máy chủ 1] phải đọc tuần tự từ đầu đến hết 100 GB, trong khi [Máy chủ 2...100] ngồi chờ!\n\n  ───────────────────────────────────────────────────────────────────────────────────────────────────\n\n  [+] GIẢI PHÁP: Đóng gói khối nội bộ qua Container Formats (Parquet, Avro) -> SPLITTABLE!\n  ┌─────────────────────────┬─────────────────────────┬─────────────────────────┐\n  │ Khối 1 (Row Group 1)    │ Khối 2 (Row Group 2)    │ Khối 3 (Row Group 3)    │\n  │ [Nén Snappy/ZSTD độc lập│ [Nén Snappy/ZSTD độc lập│ [Nén Snappy/ZSTD độc lập│\n  │  hoặc có Sync Marker]   │  hoặc có Sync Marker]   │  hoặc có Sync Marker]   │\n  └────────────▲────────────┴────────────▲────────────┴────────────▲────────────┘\n               │                         │                         │\n         [Máy chủ 1]               [Máy chủ 2]               [Máy chủ 3]\n         (Đọc & giải nén           (Đọc & giải nén           (Đọc & giải nén\n          song song ngay!)          song song ngay!)          song song ngay!)\n====================================================================================================', "kind": 'boxes'},
        '2.4b': {"ascii": '================================================================================================================================\n  1. GIẢM DUNG LƯỢNG LƯU TRỮ                2. KHUẾCH ĐẠI TỐC ĐỘ QUÉT ĐĨA               3. KHUẾCH ĐẠI BĂNG THÔNG MẠNG\n┌──────────────────────────────────────┐  ┌────────────────────────────────────────┐  ┌────────────────────────────────────────┐\n│ • Bảng gốc chưa nén: 100 GB          │  │ • Đĩa HDD đọc vật lý: 200 MB/s         │  │ • Đường truyền mạng giữa máy ảo        │\n│ • Nén cột Parquet (4:1 đến 10:1):    │  │   (Đọc 100 GB thô mất 500 giây)        │  │   EC2 và S3 vật lý: 10 Gbps            │\n│   ──> Chỉ còn 10 GB – 25 GB          │  │ • Nén 4:1 (25 GB) ──> Đọc 125 giây     │  │ • Khi truyền dữ liệu nén tỷ lệ 10:1:   │\n│ • Giảm trực tiếp 75% – 90%           │  │   + CPU giải nén trên RAM (100 GB/s)   │  │   ──> Băng thông truyền tải dữ liệu    │\n│   hóa đơn lưu trữ hàng tháng!        │  │ • Băng thông quét logic tăng vọt:      │  │       hiệu dụng đạt 100 Gbps!          │\n└──────────────────────────────────────┘  │   200 MB/s ──> 800 MB/s (tới 2 GB/s)!  │  │ • Đổi vài chu kỳ CPU lấy 10x I/O!      │\n                                          └────────────────────────────────────────┘  └────────────────────────────────────────┘\n================================================================================================================================', "kind": 'boxes'},
        '3.1': {"ascii": '======================================================================================================\n  KIẾN TRÚC PHÂN TÁN, NHÂN BẢN (x3) & TỰ CHỮA LÀNH TRONG HADOOP HDFS\n┌────────────────────────────────────────────────────────────────────────────────────────────────────┐\n│ [1] NAMENODE (Tổng công trình sư quản lý Metadata trên RAM + EditLog / FsImage):                   │\n│     • Sổ danh bạ: "orders.log (1 GB) = 8 Blocks x 128 MB"                                          │\n│     • Block 1 (#8888) ──> Lưu tại [DataNode 1 (Rack 1), DataNode 2 (Rack 2), DataNode 4 (Rack 2)]  │\n│     • Block 2         ──> Lưu tại [DataNode 2 (Rack 2), DataNode 3 (Rack 1), DataNode 5 (Rack 3)]  │\n│     • Nhận Heartbeat & Blockreport định kỳ để giám sát sức khỏe toàn cụm                           │\n│ ──────────────────────────────────────────────────────────────────────────────────────             │\n│ [2] TẦNG DATANODES (Đội thủ kho giữ khối vật lý + Đặt chung Compute & Storage):                    │\n│   ┌───────────────────────┐        ┌─────────────────────────┐        ┌─────────────────────────┐  │\n│   │ DataNode 1 (Rack 1)   │        │ DataNode 2 (Rack 2)     │        │ DataNode 4 (Rack 2)     │  │\n│   │ • [Block 1] Bản gốc   │ ─────> │ • [Block 1] Bản sao 2   │ ─────> │ • [Block 1] Bản sao 3   │  │\n│   │ • Task Map tại chỗ    │        │ • [Block 2] Bản gốc     │        │ • [Block 5] Bản sao     │  │\n│   └───────────────────────┘        └─────────────────────────┘        └─────────────────────────┘  │\n│ ──────────────────────────────────────────────────────────────────────────────────────             │\n│ [+] Tự chữa lành (Self-Healing): Nếu DataNode 1 hỏng đĩa (hệ số < 3), NameNode lập tức             │\n│     chỉ huy DataNode 2 sao chép bù [Block 1] sang node khác để khôi phục đủ 3 bản sao!             │\n│ [+] Erasure Coding RS(6,3): 6 khối dữ liệu + 3 khối Parity -> Chỉ tốn 1.5x dung lượng (thay vì 3x) │\n└────────────────────────────────────────────────────────────────────────────────────────────────────┘\n======================================================================================================', "kind": 'boxes'},
        '3.2': {"ascii": '====================================================================================================\n                    MÔ HÌNH CÂY MẠNG & 3 CẤP ĐỘ KHOẢNG CÁCH DỮ LIỆU (DATA LOCALITY)\n====================================================================================================\n\n                         ┌─────────────────────────────────────────────┐\n                         │   Switch Tổng Trung Tâm (Core Switch)       │\n                         │   (3) OFF-RACK: Khác tủ mạng, băng thông    │\n                         │       thấp nhất, dễ nghẽn cổ chai mạng!     │\n                         └──────────────────────┬──────────────────────┘\n                        ┌───────────────────────┴───────────────────────┐\n                        ▼                                               ▼\n         ┌──────────────────────────────┐               ┌──────────────────────────────┐\n         │    Tủ mạng 1 (Rack 1)        │               │    Tủ mạng 2 (Rack 2)        │\n         │  [Switch Tủ 1 (ToR Switch)]  │               │  [Switch Tủ 2 (ToR Switch)]  │\n         │      ├── Máy chủ A:          │               │      └── Máy chủ C:          │\n         │      │   • Task tính toán    │               │          • Lưu [Block #8888] │\n         │      │   • Lưu [Block #8888] │               │            (Bản sao thứ 3)   │\n         │      │   --> (1) DATA-LOCAL! │               │          --> (3) OFF-RACK!   │\n         │      │     (Nhanh nhất - Đọc │               └──────────────────────────────┘\n         │      │      ngay trên máy!)  │\n         │      └── Máy chủ B:          │\n         │          • Lưu [Block #8888] │\n         │          --> (2) RACK-LOCAL! │\n         │            (Cùng tủ mạng)    │\n         └──────────────────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '3.2b': {"ascii": '==================================================================================================================================\n  1. REDIS (IN-MEMORY STRUCTURES)             2. MEMCACHED (PURE RAM CACHE)               3. ROCKSDB (EMBEDDED LSM-TREE)\n┌────────────────────────────────────────┐  ┌────────────────────────────────────────┐  ┌────────────────────────────────────────┐\n│ • Mô hình: Client-Server trên RAM      │  │ • Mô hình: Client-Server đa luồng      │  │ • Mô hình: Nhúng trực tiếp (Embedded   │\n│   (~100 ns access + mạng LAN)          │  │   siêu nhẹ (~10 µs gói tin LAN)        │  │   LSM-Tree) vào tiến trình tính toán   │\n│ • Đa cấu trúc: String, Hash, List,     │  │ • Cấu trúc: Key-Value đơn giản         │  │ • Luồng ghi/đọc (~100 µs NVMe SSD):    │\n│   Set, Sorted Set, Bitmap + TTL        │  │   (Chỉ lưu String / Integer)           │  │   [WAL + RAM MemTable] ──> [SSTables]  │\n│ • Bền vững: Có (Chụp RDB Snapshot      │  │ • Bền vững: KHÔNG (Thuần RAM,          │  │ • Bền vững: Có (Cây LSM trên SSD)      │\n│   & ghi nhật ký AOF mỗi ~2 giây)       │  │   mất điện là mất sạch 100%)           │  │ • Vai trò: Lưu trạng thái (State       │\n│ • Vai trò: Cache phân tán dùng chung   │  │ • Vai trò: Đệm kết quả DB & Web API    │  │   Backend) cho Apache Flink & Kafka    │\n└────────────────────────────────────────┘  └────────────────────────────────────────┘  └────────────────────────────────────────┘\n==================================================================================================================================', "kind": 'boxes'},
        '3.3': {"ascii": '======================================================================================================\n  CƠ CHẾ GHI NHẬT KÝ NỐI ĐUÔI (APPEND-ONLY LOG) & REPLAY CỦA APACHE KAFKA\n┌────────────────────────────────────────────────────────────────────────────────────────────────────┐\n│ [DB Giao dịch OLTP] ──(Sự kiện CDC: Thêm/Sửa Đơn #8888)──> APACHE KAFKA TOPIC: "orders_events"     │\n│     ┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐                  │\n│     │ Offset 0         │ Offset 1         │ Offset 2         │ Offset 3 (Mới)   │                  │\n│     │ [Đơn #8886]      │ [Đơn #8887]      │ [Đơn #8888]      │ [Sửa Đ/C #8888]  │                  │\n│     └──────────────────┴──────────────────┴──────────────────┴──────────────────┘                  │\n│                                                                        ▲                           │\n│     • Ghi tuần tự nối đuôi (Append-only Sequential I/O) + Nén LZ4/Snappy/ZSTD                      │\n│     • Tiered Storage: Tự động đẩy các đoạn Log cũ xuống Object Storage để lưu dài hạn              │\n│     • Cơ chế REPLAY: Cho phép tua lại Offset bất kỳ trong quá khứ để chạy lại dữ liệu              │\n│ ──────────────────────────────────────────────────────────────────────────────────────             │\n│ [KIẾN TRÚC STREAM-TO-BATCH: 1 Luồng Kafka nuôi đồng thời 2 nhánh Consumer độc lập]                 │\n│     ├──> [Consumer 1 - Real-time]: Apache Flink / Kafka Streams (Lưu state trên RocksDB)           │\n│     └──> [Consumer 2 - Batch/DW ]: Kinesis Firehose / BigQuery Streaming Buffer / Lakehouse        │\n└────────────────────────────────────────────────────────────────────────────────────────────────────┘\n======================================================================================================', "kind": 'boxes'},
        '3.4': {"ascii": '======================================================================================================\n  KIẾN TRÚC LUỒNG DỮ LIỆU TRONG DATA WAREHOUSE & 3 RÀO CẢN LỊCH SỬ\n┌────────────────────────────────────────────────────────────────────────────────────────────────────┐\n│ [1] NGUỒN DỮ LIỆU : [Operational Data (DB Bán hàng OLTP)]  +  [External Data (CRM, ERP)]           │\n│                                               │                                                    │\n│                                               ▼                                                    │\n│ [2] TẦNG ETL / ELT: Trích xuất, làm sạch và kiểm định cấu trúc chặt chẽ (Schema-on-Write)          │\n│                                               │                                                    │\n│                                               ▼                                                    │\n│ [3] KHO DỮ LIỆU TẬP TRUNG (DATA WAREHOUSE — Snowflake / BigQuery / Redshift / Teradata):           │\n│     • Chỉ lưu dữ liệu CÓ CẤU TRÚC (Structured Data) & Đảm bảo giao dịch ACID tuyệt đối             │\n│     • Động cơ lưu trữ dạng cột (Columnar) + Micro-partitioning (50–500 MB) + Query Cache           │\n│     • Hybrid Object Storage (BigQuery Colossus / S3 Select) & Zero-Copy Cloning (Shallow Copy)     │\n│                                               │                                                    │\n│                         ┌─────────────────────┴─────────────────────┐                              │\n│                         ▼                                           ▼                              │\n│         [4a] Khai thác: [BI Dashboards & Reports]   [4b] 3 Rào cản: Bó tay trước Ảnh/Video,        │\n│              (Truy vấn SQL phân tích cực nhanh)          Đắt đỏ ở quy mô PB & Đóng kín định dạng   │\n└────────────────────────────────────────────────────────────────────────────────────────────────────┘\n======================================================================================================', "kind": 'boxes'},
        '3.5': {"ascii": '==================================================================================================================================\n  1. BÓ TAY TRƯỚC UNSTRUCTURED DATA           2. ĐẮT ĐỎ Ở QUY MÔ PETABYTE                 3. ĐÓNG KÍN & VENDOR LOCK-IN\n┌────────────────────────────────────────┐  ┌────────────────────────────────────────┐  ┌────────────────────────────────────────┐\n│ • Đơn #8888 phát sinh thêm:            │  │ • Sau 5 năm, lịch sử đơn hàng &        │  │ • Định dạng lưu trữ bên dưới bị        │\n│   - Ảnh kiện hàng (contract.jpg)       │  │   log hành vi phình lên Petabyte       │  │   đóng kín độc quyền (Proprietary).    │\n│   - Video camera kho bãi               │  │   (Volume, Velocity, Variety).         │  │ • [x] Đội Data Science muốn dùng       │\n│   - Ghi âm tổng đài CSKH               │  │ • [x] Lưu trữ & mở rộng trên phần      │  │   Python / Spark / PyTorch đọc         │\n│ • [x] Data Warehouse chỉ hiểu bảng     │  │   cứng MPP / kho chuyên dụng đắt       │  │   trực tiếp tệp gốc để train ML        │\n│   có cấu trúc / JSON, bó tay trước     │  │   gấp hàng chục lần so với lưu tệp     │  │   phải tốn phí tuần tự hóa lại         │\n│   dữ liệu phi cấu trúc cho AI/DL!      │  │   thô trên Cloud Object Storage!       │  │   (Reserializing / Export ETL)!        │\n└────────────────────────────────────────┘  └────────────────────────────────────────┘  └────────────────────────────────────────┘\n==================================================================================================================================', "kind": 'boxes'},
        '4.1': {"ascii": '====================================================================================================\n        BA CẤP ĐỘ TRỪU TƯỢNG TRONG THIẾT KẾ DỮ LIỆU: CONCEPTUAL -> LOGICAL -> PHYSICAL MODEL\n====================================================================================================\n\n  1. CONCEPTUAL MODEL (Khái niệm)     2. LOGICAL MODEL (Logic)             3. PHYSICAL MODEL (Vật lý)\n  Giao tiếp với Business              Độc lập với phần mềm CSDL            Triển khai lên CSDL thực tế\n  ┌────────────┐     ┌────────────┐   ┌──────────────────────────────┐     ┌──────────────────────────────────┐\n  │ Khách hàng ├────►│  Đơn hàng  │   │ Bảng: Fact_Sales             │     │ CREATE TABLE fact_sales (        │\n  └────────────┘ mua └──────┬─────┘   │ • Ma_Don (PK)                │     │   ma_don BIGINT,                 │\n                            │ gồm     │ • Ma_Khach_Hang (FK)         │ ──► │   so_luong INT,                  │\n                            ▼         │ • Ma_San_Pham (FK)           │     │   so_tien DECIMAL(18,2)          │\n                     ┌────────────┐   │ • So_Luong, So_Tien          │     │ ) PARTITION BY (nam_thang)       │\n                     │  Sản phẩm  │   └──────────────────────────────┘     │   CLUSTER BY (ma_khach_hang);    │\n                     └────────────┘   Xác định bảng, cột, PK & FK          └──────────────────────────────────┘\n                                                                           Chọn kiểu dữ liệu, Partition, Index\n====================================================================================================', "kind": 'boxes'},
        '4.2': {"ascii": '====================================================================================================\n          BA TRƯỜNG PHÁI KIẾN TRÚC DATA WAREHOUSE: BILL INMON vs. RALPH KIMBALL vs. DATA VAULT\n====================================================================================================\n\n  1. BILL INMON (Top-Down)              2. RALPH KIMBALL (Bottom-Up)       3. DATA VAULT (Hybrid Audit)\n  ┌──────────────────────────┐           ┌──────────────────────────┐            ┌───────────┐    ┌───────────┐\n  │ Nguồn dữ liệu toàn Cty   │           │ Nguồn dữ liệu theo nghiệp│            │ Satellite1├───►│   Hub 1   │\n  └────────────┬─────────────┘           │ vụ (Bán hàng, Kho...)    │            └───────────┘    └─────┬─────┘\n               ▼                         └────────────┬─────────────┘                                   │\n  ┌──────────────────────────┐                        ▼                                                 ▼\n  │ Enterprise Data Warehouse│           ┌──────────────────────────┐                             ┌───────────┐\n  │ (Chuẩn hóa chặt 3NF toàn │           │ Data Warehouse trung tâm │                             │   Link    │\n  │  doanh nghiệp)           │           │ (Mô hình hóa trực tiếp   │                             └─────▲─────┘\n  └────────────┬─────────────┘           │  bằng Fact & Dimension   │                                   │\n       ┌───────┼───────┐                 │  theo Star Schema)       │            ┌───────────┐    ┌─────┴─────┐\n       ▼       ▼       ▼                 └────────────┬─────────────┘            │ Satellite2├───►│   Hub 2   │\n   [Mart 1] [Mart 2] [Mart 3]                         ▼                          └───────────┘    └───────────┘\n   (Sales)   (Mkt)   (Purch)                 [ Phục vụ BI ngay! ]                (Chỉ nạp Insert-only từ nguồn)\n====================================================================================================', "kind": 'boxes'},
        '4.3': {"ascii": '====================================================================================================\n                  PHÂN TÁCH ĐƠN HÀNG #8888 THÀNH BẢNG CHIỀU (DIMENSION) VÀ BẢNG SỰ KIỆN (FACT)\n====================================================================================================\n\n   [NGỮ CẢNH ĐỊNH TÍNH - DIMENSIONS]                 [SỰ KIỆN ĐỊNH LƯỢNG - FACT TABLE]\n   Trả lời: Ai? Cái gì? Ở đâu? Khi nào?              Trả lời: Bao nhiêu? (Tại 1 Grain cố định)\n  ┌──────────────────────────────────────┐          ┌──────────────────────────────────────────┐\n  │ • Khách hàng: Nguyễn Văn A           │          │ Bảng: FACT_SALES (Hẹp & Rất dài)         │\n  │ • Cửa hàng  : Chi nhánh Bình Dương   │ ───────► │  • Ma_Don  : 8888                        │\n  │ • Sản phẩm  : Nội thất               │Tham chiếu│  • So_Luong: 1                           │\n  │ • Thời gian : Ngày 15/10/2026        │ qua Khóa │  • So_Tien : 5.000.000 VNĐ               │\n  └──────────────────────────────────────┘ PK / FK  └──────────────────────────────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '4.3b': {"ascii": '==========================================================================================================================\n  PHÂN LOẠI SỐ ĐO (ADDITIVITY) & 3 KIỂU BẢNG FACT CHUẨN CỦA RALPH KIMBALL\n┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐\n│ [PHẦN A — 3 MỨC ĐỘ CỘNG GỘP SỐ ĐO (ADDITIVITY TRONG BẢNG FACT)]:                                                       │\n│   ┌───────────────────────────────────┬───────────────────────────────────────┬──────────────────────────────────────┐ │\n│   │ 1. ADDITIVE (Cộng mọi chiều)      │ 2. SEMI-ADDITIVE (Bán cộng)           │ 3. NON-ADDITIVE (Không cộng được)    │ │\n│   │ • Cộng (SUM) hợp lệ qua TẤT CẢ    │ • Cộng được theo Cửa hàng / Sản phẩm  │ • Tuyệt đối CẤM dùng hàm SUM()!      │ │\n│   │   các chiều (Thời gian, Khu vực)  │   nhưng CẤM CỘNG THEO THỜI GIAN!      │ • Phải cộng Tử số & Mẫu số trước     │ │\n│   │ • VD: So_Luong (1), So_Tien (5M)  │ • VD: Tồn kho cuối ngày, Số dư TK     │ • VD: Đơn giá, Tỷ lệ lãi gộp (%)     │ │\n│   └───────────────────────────────────┴───────────────────────────────────────┴──────────────────────────────────────┘ │\n│ ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── │\n│ [PHẦN B — 3 KIỂU BẢNG FACT CHUẨN THEO QUY TRÌNH NGHIỆP VỤ]:                                                            │\n│   • (1) Transaction Fact Table          : 1 dòng nguyên tử cho mỗi giao dịch phát sinh (VD: Đơn hàng #8888 lúc mua).   │\n│   • (2) Periodic Snapshot Fact Table    : Chụp trạng thái định kỳ theo mốc cố định (VD: Tồn kho cuối mỗi ngày/tháng).  │\n│   • (3) Accumulating Snapshot Fact Table: 1 dòng theo dõi trọn vòng đời đơn hàng, cập nhật dần các cột mốc thời gian:  │\n│         [Ngay_Dat_Hang] ──> [Ngay_Thanh_Toan] ──> [Ngay_Xuat_Kho] ──> [Ngay_Giao_Thanh_Cong].                          │\n└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘\n==========================================================================================================================', "kind": 'boxes'},
        '4.4': {"ascii": '====================================================================================================\n           BA KIẾN TRÚC BỐ TRÍ BẢNG: STAR SCHEMA vs. SNOWFLAKE SCHEMA vs. ONE BIG TABLE (OBT)\n====================================================================================================\n\n  1. STAR SCHEMA (Lược đồ Hình sao)                   2. SNOWFLAKE SCHEMA (Lược đồ Hình bông tuyết)\n  Các Dimension để ở dạng phi chuẩn hóa               Các bảng Dimension bị chuẩn hóa tách thành nhiều\n  (Denormalized) nối trực tiếp vào Fact               bảng nhánh con (Sub-dimension tables)\n\n            ┌────────────────────┐                           ┌──────────────┐      ┌──────────────┐\n            │     Dim_Store      │                           │ Sub-Dim_City │      │Sub-Dim_Brand │\n            └─────────┬──────────┘                           └──────┬───────┘      └──────┬───────┘\n                      │ (1 JOIN)                                    │ (JOIN 2)            │ (JOIN 2)\n  ┌──────────────┐    ▼    ┌──────────────┐                         ▼                     ▼\n  │ Dim_Customer ├──►FACT◄─┤ Dim_Product  │                  ┌──────────────┐      ┌──────────────┐\n  └──────────────┘    ▲    └──────────────┘                  │   Dim_Store  │      │ Dim_Product  │\n                      │ (1 JOIN)                             └──────┬───────┘      └──────┬───────┘\n            ┌─────────┴──────────┐                                  └──────────►FACT◄─────┘\n            │      Dim_Date      │                                            (JOIN 1)\n            └────────────────────┘\n\n  ───────────────────────────────────────────────────────────────────────────────────────────────────\n  3. OBT - ONE BIG TABLE (Bảng phẳng khổng lồ - 0 JOIN trên Cloud Columnar Engine!)\n  ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐\n  │ Bảng phẳng OBT_SALES: [Ma_Don: 8888 | Ten_Khach | Ten_Cua_Hang | Ten_San_Pham | So_Tien: 5M]    │\n  └─────────────────────────────────────────────────────────────────────────────────────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '4.5a': {"ascii": "==================================================================================================================================\n  1. SCD TYPE 1 (OVERWRITE)                 2. SCD TYPE 2 (ROW VERSIONING)                3. SCD TYPE 3 (COLUMN HISTORY)\n┌──────────────────────────────────────┐  ┌──────────────────────────────────────────┐  ┌────────────────────────────────────────┐\n│ • Cơ chế: Ghi đè trực tiếp tỉnh      │  │ • Cơ chế: Giữ dòng cũ & Thêm dòng        │  │ • Cơ chế: Giữ 1 dòng (SK = 101),       │\n│   mới lên dòng cũ (SK = 101):        │  │   mới với Surrogate Key mới:             │  │   mở thêm cột mới trên cùng dòng:      │\n│   [Bình Dương] ──> [TP.HCM]          │  │   - SK 101: Bình Dương (is_current=0)    │  │   - Tinh_Hien_Tai : 'TP.HCM'           │\n│ • Hệ quả với Đơn #8888 (5M):         │  │   - SK 205: TP.HCM     (is_current=1)    │  │   - Tinh_Truoc_Do : 'Bình Dương'       │\n│   [x] MẤT DẤU LỊCH SỬ! Doanh thu     │  │ • Hệ quả với Đơn #8888 (5M):             │  │ • Hệ quả với Đơn #8888 (5M):           │\n│   tháng 10 ở Bình Dương bị cộng      │  │   [+] CHUẨN VÀNG! Đơn #8888 nối SK 101   │  │   [!] So sánh nhanh cũ/mới, nhưng      │\n│   nhầm sang cho TP.HCM!              │  │   (Bình Dương); Đơn #9999 nối SK 205!    │  │   chỉ nhớ được 1 lần đổi gần nhất!     │\n└──────────────────────────────────────┘  └──────────────────────────────────────────┘  └────────────────────────────────────────┘\n==================================================================================================================================", "kind": 'boxes'},
        '4.5': {"ascii": '====================================================================================================\n                MA TRẬN TUYẾN DOANH NGHIỆP (ENTERPRISE DW BUS MATRIX & CONFORMED DIMENSIONS)\n====================================================================================================\n\n  ┌───────────────────────────────────────────────────┬──────────┬─────────────┬──────────────┬───────────┐\n  │ Quy trình Nghiệp vụ (Facts) \\ Chiều dùng chung    │ Dim_Date │ Dim_Product │ Dim_Customer │ Dim_Store │\n  ├───────────────────────────────────────────────────┼──────────┼─────────────┼──────────────┼───────────┤\n  │ 1. Bán lẻ (Retail Sales - nơi có Đơn hàng #8888)  │   [x]    │     [x]     │     [x]      │    [x]    │\n  ├───────────────────────────────────────────────────┼──────────┼─────────────┼──────────────┼───────────┤\n  │ 2. Quản lý Tồn kho (Inventory Snapshot)           │   [x]    │     [x]     │     [ ]      │    [x]    │\n  ├───────────────────────────────────────────────────┼──────────┼─────────────┼──────────────┼───────────┤\n  │ 3. Nhập hàng từ Nhà cung cấp (Procurement)        │   [x]    │     [x]     │     [ ]      │    [x]    │\n  ├───────────────────────────────────────────────────┼──────────┼─────────────┼──────────────┼───────────┤\n  │ 4. Chăm sóc Khách hàng & Bảo hành (CRM Support)   │   [x]    │     [x]     │     [x]      │    [ ]    │\n  └───────────────────────────────────────────────────┴──────────┴─────────────┴──────────────┴───────────┘\n  --> Các chiều dùng chung (Conformed Dimensions) giúp nối kết (Drill-across) nhiều Data Marts độc lập!\n====================================================================================================', "kind": 'boxes'},
        '5.1': {"ascii": '====================================================================================================\n      ĐỐI CHIẾU CƠ HỌC: DATA WAREHOUSE (SCHEMA-ON-WRITE & ETL) vs. DATA LAKE (SCHEMA-ON-READ & ELT)\n====================================================================================================\n\n  1. DATA WAREHOUSE TRUYỀN THỐNG (Schema-on-Write & ETL)\n  ┌──────────────┐     [!] TRANSFORM (Kiểm duyệt gắt gao)    ┌─────────────────────────┐\n  │ Nguồn dữ liệu├────► Phải định nghĩa đúng cột trước. ────►│ [DWH] DATA WAREHOUSE    │\n  │ (Đơn #8888)  │      Nếu JSON thêm 1 trường lạ -> BÁO LỖI,│ (Chỉ chứa bảng sạch,    │\n  └──────────────┘      GÃY TOÀN BỘ PIPELINE NGAY LẬP TỨC!   │  mất dữ liệu thô gốc)   │\n                                                             └─────────────────────────┘\n\n  2. DATA LAKE THẾ HỆ MỚI (Schema-on-Read & ELT)\n  ┌──────────────┐     [+] LOAD THẲNG (Không kiểm tra)       ┌─────────────────────────┐\n  │ Mọi định dạng├────► Cứ ném nguyên bản JSON, Parquet, ───►│ [LAKE] DATA LAKE (S3)   │\n  │ của Đơn #8888│      Ảnh, Video vào hồ với giá $0.02/GB!  │ Lúc nào cần ĐỌC ra phân │\n  └──────────────┘                                           │ tích mới áp Schema vào! │\n                                                             └─────────────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '5.2a': {"ascii": '====================================================================================================\n                  QUÁ TRÌNH THOÁI HÓA TỪ HỒ DỮ LIỆU (DATA LAKE) THÀNH ĐẦM LẦY (DATA SWAMP)\n====================================================================================================\n\n       [+] DATA LAKE BAN ĐẦU (Ngăn nắp)             [!] DATA SWAMP SAU 6 THÁNG (Hỗn loạn)\n     ┌───────────────────────────────────┐        ┌──────────────────────────────────────────┐\n     │ /sales/orders/                    │        │ /tmp_test_8888/                          │\n     │   └── 8888.parquet                │        │ /data_final_final_v2/                    │\n     │ /logs/clickstream/                │ ─────► │ /dump_2026_unnamed/                      │\n     │   └── click_8888.json             │ Thoái  │   ├── 8888_part1.json (Lỗi mã hóa UTF-8) │\n     │ /images/contracts/                │  hóa   │   ├── 3_zombie.parquet (Tệp ghi dở, rác) │\n     │   └── contract_8888.jpg           │        │   └── 3_v2.parquet (Bị nhân đôi số liệu!)│\n     └───────────────────────────────────┘        └──────────────────────────────────────────┘\n       Hồ nước trong lành, phân vùng rõ             Đầm lầy ô nhiễm: Không ai biết tệp nào\n       ràng, tin cậy                                đúng, không ai dám sử dụng!\n====================================================================================================', "kind": 'boxes'},
        '5.2b': {"ascii": "========================================================================================================================\n  CƠ CHẾ SINH TỆP GHI DỞ (ZOMBIE WRITES) & ĐIỂM MÙ CỦA APACHE HIVE TABLE FORMAT\n┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐\n│ [Job Spark đang ghi Đơn #8888 vào S3] ──(Đứt mạng ở giây thứ 5!)──> Sinh ra '3.parquet' (Ghi dở 50% — Zombie File)   │\n│                   │                                                                                                  │\n│        (Hệ thống tự động Retry chạy lại Job)                                                                         │\n│                   │                                                                                                  │\n│                   └─────────────────────(Chạy thành công 100%)────> Sinh ra '3_v2.parquet' (Đủ 100% dữ liệu)         │\n│ ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────   │\n│ [HẬU QUẢ KHI TRUY VẤN TRÊN ĐỊNH DẠNG BẢNG APACHE HIVE (Directory-level Tracking)]:                                   │\n│ • Bảng Hive định nghĩa dữ liệu bằng TOÀN BỘ TỆP NẰM TRONG THƯ MỤC (chứ không có danh sách tệp hợp lệ cụ thể).        │\n│ • Trên S3 không có lệnh đổi tên thư mục nguyên tử (Rename = COPY + DELETE O(N)), thiếu khóa giao dịch đa tệp.        │\n│ • Khi chạy SQL, động cơ quét TẤT CẢ tệp trong thư mục: đọc cả '3.parquet' lẫn '3_v2.parquet'                         │\n│   ──> Doanh thu Đơn #8888 bị TÍNH GẤP ĐÔI (Duplicate Counts / Wrong Answers)!                                        │\n└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘\n========================================================================================================================", "kind": 'boxes'},
        '5.2c': {"ascii": "==========================================================================================================================\n  6 KHIẾM KHUYẾT KIẾN TRÚC CỦA APACHE HIVE TABLE FORMAT TRÊN CLOUD OBJECT STORAGE\n┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐\n│   ┌────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────┐ │\n│   │ [1] QUẢN LÝ CẤP THƯ MỤC (DIRECTORY-LEVEL TRACKING)     │ [4] LIỆT KÊ TỆP ĐẮT ĐỎ & NGHẼN TIỀN TỐ (S3 LIST)        │ │\n│   │ • Định nghĩa bảng bằng toàn bộ tệp trong thư mục       │ • Phải gọi S3 LIST tuần tự qua hàng nghìn thư mục;      │ │\n│   │   ──> Đọc nhầm cả tệp ghi dở (3.parquet) làm nhân đôi! │   dễ bị bóp băng thông (Throttling) khi quá nhiều file. │ │\n│   ├────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┤ │\n│   │ [2] ĐỔI TÊN (RENAME) KHÔNG NGUYÊN TỬ TRÊN S3           │ [5] PHỤ THUỘC CỨNG CỘT PHÂN VÙNG (PARTITION COUPLING)   │ │\n│   │ • Trên S3 không có cây thư mục thật: lệnh Rename thực  │ • Lọc trên cột 'order_timestamp' mà quên thêm điều kiện │ │\n│   │   chất là chuỗi COPY + DELETE tốn O(N) theo byte!      │   lọc cột phân vùng 'year_month' ──> Quét toàn bộ bảng! │ │\n│   ├────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┤ │\n│   │ [3] THIẾU GIAO DỊCH ĐA PHÂN VÙNG (NO MULTI-PARTITION)  │ [6] THỐNG KÊ LỖI THỜI & GIỚI HẠN ĐƠN TỆP (SINGLE-OBJ)   │ │\n│   │ • Hive Metastore chỉ khóa từng phân vùng đơn lẻ; cập   │ • Lệnh ANALYZE TABLE quá chậm; Strong Consistency của   │ │\n│   │   nhật 12 tháng cùng lúc sẽ lộ trạng thái nửa cũ/mới!  │   S3 chỉ bảo vệ 1 tệp đơn lẻ, bó tay khi ghi 200 tệp!   │ │\n│   └────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────┘ │\n└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘\n==========================================================================================================================", "kind": 'boxes'},
        '5.3': {"ascii": '====================================================================================================\n                     3 LỖ HỔNG CỐT TỬ BIẾN DATA LAKE THÀNH DATA SWAMP (ĐẦM LẦY DỮ LIỆU)\n====================================================================================================\n\n             ┌──────────────────────────────────────────────────────────────┐\n             │               [!] DATA SWAMP (ĐẦM LẦY DỮ LIỆU)               │\n             └──────────────┬───────────────┬────────────────┬──────────────┘\n                            │               │                │\n         ┌──────────────────┘               │                └──────────────────┐\n         ▼                                  ▼                                   ▼\n  ┌──────────────────────────┐   ┌──────────────────────────┐   ┌──────────────────────────┐\n  │ 1. LỖ HỔNG GIAO DỊCH &   │   │ 2. THIẾU DATA CATALOG    │   │ 3. THIẾU DATA LINEAGE    │\n  │    CÔNG CỤ (ACID/Mutate) │   │    & METADATA MGMT       │   │    & OBSERVABILITY       │\n  ├──────────────────────────┤   ├──────────────────────────┤   ├──────────────────────────┤\n  │ • Không có ACID: Job ETL │   │ • Không biết bảng nào ở  │   │ • Không truy vết được dữ │\n  │   đụng độ truy vấn đọc   │   │   đâu, ý nghĩa cột là gì │   │   liệu sinh ra từ nguồn  │\n  │ • Bất biến (Immutable):  │   │ • Thiếu người sở hữu rõ  │   │   nào, qua bước biến đổi │\n  │   Không thể Upsert/Xóa lẻ│   │   ràng (Ownership)       │   │   nào mà bị sai lệch     │\n  │ • Không chặn Schema Drift│   │ • Tạo ra Dark Data/WORN  │   │ • Thiếu Quality Checks   │\n  └──────────────────────────┘   └──────────────────────────┘   └──────────────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '5.3b': {"ascii": '==============================================================================================================================\n  KIẾN TRÚC DATA CATALOG HIỆN ĐẠI (3 TẦNG)                      5 TRỤ CỘT GIÁM SÁT DỮ LIỆU (DATA OBSERVABILITY)\n┌──────────────────────────────────────────────────────────┐  ┌──────────────────────────────────────────────────────────────┐\n│ • Tầng 3 — Cổng Tra cứu & Cộng tác (Web Portal/Wiki):    │  │ • [1] Freshness (Độ tươi mới): Có trễ SLA 6 tiếng không?     │\n│   Tra cứu định nghĩa bảng, chỉ định Data Owner/Steward   │  │ • [2] Volume (Sản lượng)     : Có tụt dòng hoặc tăng gấp     │\n│                       ▲                                  │  │       đôi bất thường do tệp rác Zombie Writes không?         │\n│ • Tầng 2 — Quét & Suy luận Tự động (Auto-Scanning):      │  │ • [3] Schema (Cấu trúc)      : Có ai tự ý đổi tên cột        │\n│   Tự động khám phá Schema, gợi ý khóa JOIN & quét PII    │  │       (total_cost ──> order_amount) làm gãy ETL không?       │\n│                       ▲                                  │  │ • [4] Distribution (Phân phối): Tỷ lệ NULL / số âm có vọt?   │\n│ • Tầng 1 — Tích hợp API Ứng dụng (API Integration):      │  │ • [5] Lineage (Phả hệ Cột/Bảng): Truy vết Root Cause &       │\n│   Kết nối trực tiếp với Spark, Airflow, dbt, Lakehouse   │  │       khoanh vùng ảnh hưởng hạ nguồn (Blast Radius)!         │\n└──────────────────────────────────────────────────────────┘  └──────────────────────────────────────────────────────────────┘\n==============================================================================================================================', "kind": 'boxes'},
        '5.4a': {"ascii": '====================================================================================================\n                  QUY HOẠCH PHÂN VÙNG CÁCH LY TRONG DATA LAKE (DATA LAKE ZONING)\n====================================================================================================\n\n                ┌──────────────────────────┐     ┌──────────────────────────┐     ┌──────────────────────────┐\n                │ [1] RAW ZONE             │     │ [2] CLEANSED ZONE        │     │ [3] CURATED ZONE         │\n  [Nguồn] ────► │ (Vùng Dữ liệu Thô)       ├────►│ (Vùng Đã Làm Sạch)       ├────►│ (Vùng Tinh Chế)          │\n                ├──────────────────────────┤ ETL ├──────────────────────────┤ ELT ├──────────────────────────┤\n                │ • Giữ nguyên bản Đơn     │     │ • Lọc bỏ file rác, chuẩn │     │ • Chuẩn hóa mô hình kinh │\n                │   #8888 lúc mới nạp vào  │     │   hóa kiểu dữ liệu, khử  │     │   doanh, tổng hợp sẵn    │\n                │   hồ để Replay khi cần   │     │   trùng lặp (Dedup)      │     │   sàng cho BI & AI/ML    │\n                └──────────────────────────┘     └──────────────────────────┘     └──────────────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '5.4b': {"ascii": '====================================================================================================\n          KỶ LUẬT CHỐNG ĐẦM LẦY: HỢP ĐỒNG DỮ LIỆU (DATA CONTRACTS) & SCHEMA REGISTRY\n====================================================================================================\n\n  [x] KHÔNG CÓ QUẢN LÝ SCHEMA (Without Proper Schema Management):\n  ┌──────────┐  (Tự ý đổi Schema)  ┌──────────────┐       ┌─────────────────┐       ┌──────────────────────────┐\n  │ Producer ├───────────────────► │ Kafka Topics ├─────► │ DIY Schema Mgmt ├─────► │ [!] Gãy Pipeline & Mất!  │\n  └──────────┘                     └──────────────┘       └─────────────────┘       └──────────────────────────┘\n\n  [+] CÓ HỢP ĐỒNG DỮ LIỆU & SCHEMA REGISTRY (With Proper Schema Management):\n  ┌──────────┐  (Gửi sự kiện #8888)┌──────────────┐       ┌─────────────────┐       ┌──────────────────────────┐\n  │ Producer ├───────────────────► │ Kafka Topics ├─────► │ Schema Registry ├─────► │ [+] Consumer nhận an toàn│\n  └──────────┘                     └──────────────┘       └─────────────────┘       └──────────────────────────┘\n                                                           Kiểm tra & Đảm bảo\n                                                           tương thích Schema\n====================================================================================================', "kind": 'boxes'},
        '6.1a': {"ascii": '====================================================================================================\n               SƠ ĐỒ GIAO THOA KIẾN TRÚC DATA LAKEHOUSE (BÀI BÁO KINH ĐIỂN CIDR 2021)\n====================================================================================================\n\n       [1] DATA WAREHOUSE               [3] DATA LAKEHOUSE                 [2] DATA LAKE\n    ┌─────────────────────────┐      ┌──────────────────────────┐      ┌─────────────────────────┐\n    │ • Dữ liệu có cấu trúc   │      │ • Giao dịch ACID         │      │ • Dữ liệu thô & phi     │\n    │   (Structured data)     │      │   (Transactions)         │      │   cấu trúc (Raw/Unstr.) │\n    │ • Tổ chức nghiêm ngặt   │      │ • Cưỡng chế lược đồ      │      │ • Lược đồ linh hoạt     │\n    │   (Highly organized)    │ ───► │   (Schema enforcement)   │ ◄─── │   (Flexible schema)     │\n    │ • Tối ưu sẵn cho BI     │ Hợp  │ • Tách rời Lưu trữ &     │ Hợp  │ • Phục vụ Data Science  │\n    │   (Built for BI)        │ nhất │   Tính toán (Decoupled)  │ nhất │   & Machine Learning    │\n    │ • Truy vấn cực nhanh    │      │ • Đa dạng Workload       │      │ • Chi phí lưu trữ rẻ    │\n    │   (Fast queries)        │      │   (BI, SQL, Streaming,ML)│      │   (Low storage cost)    │\n    │ [x] Đắt đỏ ở quy mô lớn │      │ • Quản trị dữ liệu       │      │ • Dung lượng khổng lồ   │\n    │   (Expensive at scale)  │      │   (Data governance)      │      │ [x] Dễ hóa thành Đầm lầy│\n    └─────────────────────────┘      └──────────────────────────┘      └─────────────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '6.1b': {"ascii": "===============================================================================================================\n  KIẾN TRÚC 3 TẦNG CỦA HỆ THỐNG DATA LAKEHOUSE (DECOUPLED COMPUTE & STORAGE)\n┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐\n│ [TẦNG 1: ĐỘNG CƠ TRUY VẤN & TÍNH TOÁN (QUERY ENGINES / EPHEMERAL COMPUTE)]                                  │\n│   ┌──────────────────────────────┐  ┌──────────────────────────────┐  ┌──────────────────────────────┐      │\n│   │            Node A            │  │            Node B            │  │            Node C            │      │\n│   │  [SQL Exec / Vectorized]     │  │  [SQL Exec / Vectorized]     │  │  [SQL Exec / Vectorized]     │      │\n│   │  [(Local SSD / RAM Cache)]   │  │  [(Local SSD / RAM Cache)]   │  │  [(Local SSD / RAM Cache)]   │      │\n│   └──────────────────────────────┘  └──────────────────────────────┘  └──────────────────────────────┘      │\n│   • Đa động cơ (Apache Spark, Trino, Flink, Presto, DuckDB, BI, PyTorch) bật/tắt theo nhu cầu (Ephemeral)   │\n│ ────────────────────────────────────────────────────▲────────────────────────────────────────────────────   │\n│                                                     │ Hỏi Transaction Layer: 'Đọc những tệp hợp lệ nào?'    │\n│ ────────────────────────────────────────────────────┴────────────────────────────────────────────────────   │\n│ [TẦNG 2: TẦNG GIAO DỊCH & ĐỊNH DẠNG BẢNG (TRANSACTION LAYER — 'Trái tim của Data Lakehouse')]               │\n│   ┌──────────────────────────────┐  ┌──────────────────────────────┐  ┌──────────────────────────────┐      │\n│   │         Table Format         │  │        Table Services        │  │     Transaction Manager      │      │\n│   │  (Delta Lake/Iceberg/Hudi)   │  │ (Compaction/Z-Order/Vacuum)  │  │   (ACID / OCC / MVCC / NBCC) │      │\n│   └──────────────────────────────┘  └──────────────────────────────┘  └──────────────────────────────┘      │\n│   • Định nghĩa Bảng = Danh sách chuẩn tắc các tệp hợp lệ (Canonical List of Files) thay vì quét thư mục!    │\n│ ────────────────────────────────────────────────────▲────────────────────────────────────────────────────   │\n│                                                     │ Quản lý siêu dữ liệu trỏ xuống các tệp vật lý         │\n│ ────────────────────────────────────────────────────┴────────────────────────────────────────────────────   │\n│ [TẦNG 3: TẦNG LƯU TRỮ ĐÁM MÂY (CLOUD OBJECT STORAGE: AWS S3 / Azure ADLS Gen2 / Google Cloud Storage)]      │\n│   • [Data Files (File Format: Parquet / ORC / Avro)]  +  [Metadata / Log / Manifest / Delete Files]         │\n└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘\n===============================================================================================================", "kind": 'boxes'},
        '6.2a': {"ascii": "========================================================================================================================\n  CÁCH DELTA LAKE (_delta_log) CỨU ĐƠN HÀNG #8888 KHỎI TỆP GHI DỞ (ZOMBIE WRITES)\n┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐\n│ s3://bucket/orders_delta/ (Thư mục gốc của bảng Delta Lake)                                                          │\n│  ├── _delta_log/ (Cuốn sổ cái kế toán ghi nối đuôi tuần tự — Nguồn sự thật duy nhất của bảng)                        │\n│  │    ├── 000000.json  ──> Ghi nhận Version 0:                                                                       │\n│  │    │                    • protocol (minReader/Writer) + metaData (Schema bảng, Partition)                         │\n│  │    │                    • ADD 'part-01.parquet' (Đơn #8888: 15.000.000đ | stats Min/Max)                          │\n│  │    ├── 000001.json  ──> Ghi nhận Version 1 (Sau khi khách nhập mã giảm giá còn 14.000.000đ):                      │\n│  │    │                    • REMOVE 'part-01.parquet' (Đánh dấu Tombstone tệp cũ)                                    │\n│  │    │                    • ADD    'part-02.parquet' (Đơn #8888: 14.000.000đ | commitInfo)                          │\n│  │    ├── 000010.checkpoint.parquet  ──> Gộp trạng thái các tệp JSON trước đó thành Parquet để đọc siêu tốc          │\n│  │    └── _last_checkpoint           ──> Con trỏ chỉ định tệp Checkpoint mới nhất (tránh lệnh S3 LIST)               │\n│  │                                                                                                                   │\n│  ├── part-01.parquet            (Bản cũ — vẫn giữ trên S3 để phục vụ Time Travel về Version 0)                       │\n│  ├── part-02.parquet            (Bản hiện hành hợp lệ duy nhất ở Version 1)                                          │\n│  └── 3_zombie_partial.parquet   (Tệp do 1 job Spark đứt mạng ghi dở dang 50% rớt lại trong thư mục)                  │\n│ ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────   │\n│ [+] KẾT QUẢ KHI TRUY VẤN: Động cơ đọc '_delta_log' thấy ở Version 1 chỉ có 'part-02.parquet' là hợp lệ.              │\n│     Tệp rác '3_zombie_partial.parquet' chưa bao giờ được commit vào '_delta_log' nên TÀNG HÌNH 100%!                 │\n└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘\n========================================================================================================================", "kind": 'boxes'},
        '6.2b': {"ascii": '====================================================================================================================\n  CÂY SIÊU DỮ LIỆU 3 TẦNG CỦA APACHE ICEBERG (CATALOG -> METADATA -> MANIFEST LIST -> MANIFEST)\n┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐\n│                                ┌───────────────────────────────────────────────┐                                 │\n│                                │                ICEBERG CATALOG                │                                 │\n│                                │  • Giữ con trỏ nguyên tử (Atomic CAS Pointer) │                                 │\n│                                │    trỏ tới Metadata hiện tại: v2.metadata.json│                                 │\n│                                └───────────────────────┬───────────────────────┘                                 │\n│                                                        │                                                         │\n│                                                        ▼                                                         │\n│ TẦNG 1:                        ┌───────────────────────────────────────────────┐                                 │\n│ Metadata File                  │               v2.metadata.json                │                                 │\n│ (Cấu trúc & Snapshots)         │  • Lưu Table UUID, Schema (Column IDs)        │                                 │\n│                                │  • Lưu Partition Specs & Sort Orders          │                                 │\n│                                │  • Danh sách Snapshots: [s0, s1 (current)]    │                                 │\n│                                └───────────────────────┬───────────────────────┘                                 │\n│                                                        │ Trỏ tới Snapshot hiện tại (s1)                          │\n│                                                        ▼                                                         │\n│ TẦNG 2:                        ┌───────────────────────────────────────────────┐                                 │\n│ Manifest List                  │          snap-s1-manifest-list.avro           │                                 │\n│ (Mục lục của 1 Snapshot)       │  • Một dòng cho mỗi Manifest File             │                                 │\n│                                │  • Lưu khoảng Min/Max từng phân vùng giúp     │                                 │\n│                                │    cắt tỉa cả cụm Manifest ngay lập tức       │                                 │\n│                                └───────────┬───────────────────────┬───────────┘                                 │\n│                                            │                       │                                             │\n│                             ┌──────────────┘                       └──────────────┐                              │\n│                             ▼                                                     ▼                              │\n│ TẦNG 3:       ┌───────────────────────────────────────┐             ┌───────────────────────────────────────┐    │\n│ Manifest      │           manifest-01.avro            │             │           manifest-02.avro            │    │\n│ Files         │  • Danh sách Data/Delete Files        │             │  • Danh sách Data/Delete Files        │    │\n│ (Thống kê tệp)│  • Lưu Min/Max/Null Count từng cột    │             │    (Chứa tệp của Đơn hàng #8888)      │    │\n│               └───────────────────┬───────────────────┘             └───────────────────┬───────────────────┘    │\n│                                   │                                                     │                        │\n│                                   ▼                                                     ▼                        │\n│ DATA LAYER:    [0001.parquet] + [0002.parquet]                       [0003_8888.parquet] + [pos_delete.parquet]  │\n└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘\n====================================================================================================================', "kind": 'boxes'},
        '6.2c': {"ascii": '================================================================================================================================\n  1. HUDI TIMELINE (STATE MACHINE)        2. HỆ THỐNG CHỈ MỤC (INDEXING)            3. FILE GROUPS (BASE + LOG FILES)\n┌────────────────────────────────────┐  ┌──────────────────────────────────────┐  ┌────────────────────────────────────────────┐\n│ [1. HUDI TIMELINE (.hoodie/)]:     │  │ [2. INDEXING SUBSYSTEM]:             │  │ [3. FILE GROUPS & FILE SLICES (Hybrid)]:   │\n│ • Ghi nhận tuần tự mọi Instant     │  │ • Lưu trong bảng Metadata nội bộ     │  │ • Mỗi File Group có FileId cố định,        │\n│   theo máy trạng thái 3 bước:      │  │   (.hoodie/metadata dạng HFile)      │  │   chia thành các File Slice theo mốc giờ:  │\n│   [REQUESTED] ──> [INFLIGHT]       │  │ • Ánh xạ siêu tốc khóa bản ghi:      │  │   ┌────────────────────────────────────┐   │\n│               ──> [COMPLETED]      │  │   RecordKey (#8888) ──> FileGroup ID │  │   │ Base File (Parquet - Lưu theo Cột) │   │\n│ • Các hành động chính:             │  │ • Các loại Index thực chiến:         │  │   │  • Chứa Đơn #8888 gốc (15.000.000đ)│   │\n│   - commit (Bảng COW)              │  │   - Record-Level Index (RLI - O(1))  │  │   ├────────────────────────────────────┤   │\n│   - deltacommit (Bảng MOR)         │  │   - Bloom Index (Mặc định)           │  │   │ + Log Files (.log.avro - Theo Dòng)│   │\n│   - compaction / clustering        │  │   - Bucket Index (Băm trực tiếp)     │  │   │  • Bắt nhanh CDC: #8888 -> 14 triệu│   │\n│   - clean / rollback / savepoint   │  │   - Simple / HBase Index             │  │   └────────────────────────────────────┘   │\n└────────────────────────────────────┘  └──────────────────────────────────────┘  └────────────────────────────────────────────┘\n================================================================================================================================', "kind": 'boxes'},
        '6.2d': {"ascii": '============================================================================================================\n  KỶ NGUYÊN HỢP NHẤT ĐA ĐỊNH DẠNG: DELTA UNIFORM, APACHE XTABLE & PLUGGABLE FORMAT\n┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐\n│                       ┌───────────────────────────────────────────────────────────┐                      │\n│                       │   BỘ DỊCH SIÊU DỮ LIỆU ĐA CHIỀU (UNIFORM / APACHE XTABLE) │                      │\n│                       │   • Chuyển đổi qua lại con trỏ & thống kê ở tầng Metadata │                      │\n│                       └───────────┬─────────────────┬─────────────────┬───────────┘                      │\n│                                   │                 │                 │                                  │\n│                                   ▼                 ▼                 ▼                                  │\n│                         [ _delta_log JSON ]  [ Iceberg Tree ]  [ Hudi Timeline ]                         │\n│                         (Spark / Databricks) (Trino/Snowflake) (Flink / Presto)                          │\n│                                   │                 │                 │                                  │\n│                                   └─────────────────┼─────────────────┘                                  │\n│                                                     ▼                                                    │\n│                       ┌───────────────────────────────────────────────────────────┐                      │\n│                       │     CÙNG 1 BỘ TỆP VẬT LÝ DUY NHẤT: orders_8888.parquet    │                      │\n│                       │  [+] Không nhân bản dữ liệu Parquet, không tốn thêm phí S3│                      │\n│                       └───────────────────────────────────────────────────────────┘                      │\n└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘\n============================================================================================================', "kind": 'boxes'},
        '6.3': {"ascii": '====================================================================================================\n                  3 CƠ CHẾ KIỂM SOÁT ĐỒNG THỜI TRÊN DATA LAKEHOUSE (MVCC, OCC, NBCC)\n====================================================================================================\n\n  ┌────────────────────────────────────────────────────────────────────────────────────────────────┐\n  │ 1. MVCC (Multi-Version Concurrency Control - Cô lập Snapshot cho Người Đọc & Dịch vụ Bảng):    │\n  │    • Người Đọc (Giám đốc) đọc bản chụp [Snapshot v1].                                          │\n  │    • Người Ghi hoặc dịch vụ Compaction âm thầm tạo tệp mới cho [Snapshot v2] ở hậu trường.     │\n  │    --> Đọc và Ghi KHÔNG BAO GIỜ KHÓA NHAU (Non-blocking reads)!                                │\n  ├────────────────────────────────────────────────────────────────────────────────────────────────┤\n  │ 2. OCC (Optimistic Concurrency Control - Kiểm soát Lạc quan giữa 2 Người Ghi):                 │\n  │    • Writer 1 và Writer 2 cùng bắt đầu sửa từ [Snapshot v1].                                   │\n  │    • Writer 1 xong trước --> Ghi nhận thành công [Snapshot v2].                                │\n  │    • Writer 2 xong sau   --> Kiểm tra thấy bảng đã lên v2: Nếu không đụng cùng file thì cho    │\n  │      qua; nếu đụng độ (collision) thì báo lỗi hoặc thử lại để bảo toàn thứ tự tuần tự!         │\n  ├────────────────────────────────────────────────────────────────────────────────────────────────┤\n  │ 3. NBCC (Non-Blocking Concurrency Control - Không khóa cho Streaming tốc độ cao trong Hudi):   │\n  │    • Cho phép nhiều luồng ghi (multiple writers) và dịch vụ bảng cùng ghi vào các Log files    │\n  │      mà không làm hỏng hay bắt nhau phải chạy lại, tránh lãng phí tài nguyên CPU của OCC!      │\n  └────────────────────────────────────────────────────────────────────────────────────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '6.3b': {"ascii": "====================================================================================================================================\n  1. SCHEMA EVOLUTION QUA MÃ CỘT BẤT BIẾN (COLUMN ID)             2. LUỒNG THAY ĐỔI TĂNG TRƯỞNG (CHANGE DATA FEED)\n┌────────────────────────────────────────────────────────────┐  ┌──────────────────────────────────────────────────────────────────┐\n│ • [x] Bảng Parquet/Hive cũ (Ánh xạ theo Tên chữ):          │  │ • Khi bật Change Data Feed (CDF / Changelog Scan):               │\n│   Đổi tên 'total_cost' ──> 'order_amount' khiến tệp cũ     │  │   Mỗi lần Đơn #8888 sửa từ 15M ──> 14M ở Version 1,              │\n│   trả về toàn bộ NULL (hoặc dữ liệu cũ đội mồ sống dậy)!   │  │   Lakehouse tự động xuất luồng thay đổi kèm '_change_type':      │\n│ • [+] Iceberg & Delta Column Mapping (Ánh xạ theo ID):     │  │   - insert           : Bản ghi mới chèn                          │\n│   Gắn mã bất biến: order_id [ID=1], total_cost [ID=2].     │  │   - update_preimage  : Giá trị trước khi sửa (15.000.000đ)       │\n│   ──> Khi RENAME sang 'order_amount', chỉ sửa nhãn của     │  │   - update_postimage : Giá trị sau khi sửa   (14.000.000đ)       │\n│       [ID=2] trong Metadata mất 1 ms, KHÔNG VIẾT LẠI TỆP!  │  │   - delete           : Bản ghi bị xóa (phục vụ ETL Silver->Gold) │\n└────────────────────────────────────────────────────────────┘  └──────────────────────────────────────────────────────────────────┘\n====================================================================================================================================", "kind": 'boxes'},
        '6.4': {"ascii": '========================================================================================================================\n  ĐỐI CHIẾU CƠ HỌC COPY-ON-WRITE (COW) VS. MERGE-ON-READ (MOR) KHI SỬA ĐƠN HÀNG #8888\n┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐\n│ [CHIẾN LƯỢC 1: COPY-ON-WRITE (COW — Chép lại toàn bộ tệp Parquet khi ghi / sửa / xóa)]                               │\n│   ┌──────────────────────────────────────┐                          ┌──────────────────────────────────────┐         │\n│   │ file_01.parquet (100 MB - 100k dòng) │   Đọc 99.999 đơn cũ      │ file_02.parquet (100 MB - Tệp mới)   │         │\n│   │ • 99.999 đơn hàng khác               │ ── + Đơn #8888 (14M) ──> │ • 99.999 đơn hàng khác               │         │\n│   │ • Đơn #8888: 15.000.000đ             │   Viết lại nguyên 100 MB │ • Đơn #8888: 14.000.000đ             │         │\n│   └──────────────────────────────────────┘                          └──────────────────┬───────────────────┘         │\n│    (Đánh dấu Tombstone trong Metadata)                                                 ▲                             │\n│                                                                      [+] Lúc ĐỌC: Quét thẳng file_02 siêu tốc!       │\n│ ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════   │\n│ [CHIẾN LƯỢC 2: MERGE-ON-READ (MOR — Ghi nối đuôi vào Log / Delete File, Trộn lại khi đọc)]                           │\n│   ┌──────────────────────────────────────┐                          ┌──────────────────────────────────────┐         │\n│   │ Base File: file_01.parquet (100 MB)  │   KHÔNG viết lại 100 MB! │ Delta Log / Delete File (Chỉ ~1 KB)  │         │\n│   │ • Giữ nguyên bất biến trên S3,       │ ── Chỉ ghi 1 dòng sửa ──>│ • Hudi: log_01.avro (#8888 -> 14M)   │         │\n│   │   không đụng chạm tới 99.999 đơn cũ  │   bằng deltacommit       │ • Iceberg/Delta: Pos/Eq Delete Vector│         │\n│   └──────────────────┬───────────────────┘                          └──────────────────┬───────────────────┘         │\n│                      │                                                                 │                             │\n│                      └──────────────> [LÚC ĐỌC (Snapshot Query)]: Engine trộn (Merge) <┘                             │\n│                                       Base File (Cột) + Log/Delete File để trả về 14M!                               │\n└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘\n========================================================================================================================', "kind": 'boxes'},
        '6.5a': {"ascii": "========================================================================================================================\n  1. PARTITIONING TRUYỀN THỐNG (HIVE)                         2. HIDDEN PARTITIONING & EVOLUTION (ICEBERG)\n┌──────────────────────────────────────────┐                ┌──────────────────────────────────────────────────────────┐\n│ • Phải tạo thêm cột vật lý dẫn xuất      │ ──(Đột phá)──> │ • Hidden Partitioning: Iceberg lưu hàm biến đổi          │\n│   'nam_thang' = '2026-10' từ cột gốc     │ ──(Đột phá)──> │   month(ngay_gio_mua) hoặc bucket(16, id) ngay           │\n│   'ngay_gio_mua'.                        │ ──(Đột phá)──> │   trong Metadata (Partition Spec).                       │\n│ • Nếu người dùng viết câu lệnh SQL:      │ ──(Đột phá)──> │   ──> Người dùng chỉ cần lọc trên cột 'ngay_gio_mua'     │\n│   WHERE ngay_gio_mua >= '2026-10-15'     │ ──(Đột phá)──> │       tự nhiên, Engine tự động cắt tỉa đúng phân vùng!   │\n│   mà QUÊN thêm AND nam_thang='2026-10'   │ ──(Đột phá)──> │ • Partition Evolution (Tiến hóa phân vùng tại chỗ):      │\n│   ──> Quét toàn bộ bảng (Full Scan)!     │ ──(Đột phá)──> │   ──> Đổi từ month(ts) [Spec 0] sang day(ts) [Spec 1]    │\n│ • Muốn đổi từ chia theo Tháng sang       │ ──(Đột phá)──> │       chỉ bằng 1 lệnh cập nhật Metadata; dữ liệu cũ      │\n│   chia theo Ngày: Phải viết lại 100%     │ ──(Đột phá)──> │       giữ Spec 0, dữ liệu mới dùng Spec 1, KHÔNG CẦN     │\n│   tệp Parquet lịch sử!                   │ ──(Đột phá)──> │       VIẾT LẠI bất kỳ tệp Parquet lịch sử nào!           │\n└──────────────────────────────────────────┘                └──────────────────────────────────────────────────────────┘\n========================================================================================================================", "kind": 'boxes'},
        '6.5b': {"ascii": '====================================================================================================\n        GOM CỤM ĐA CHIỀU Z-ORDERING & LIQUID CLUSTERING (SPACE-FILLING CURVES: Z-CURVE / HILBERT)\n====================================================================================================\n\n  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐\n  │ [x] TRƯỚC KHI Z-ORDER (Dữ liệu rải ngẫu nhiên ở mọi tệp Parquet):                                │\n  │  • File 1: Customer_ID [min: 1, max: 9999]  |  Product_ID [min: 10, max: 500]                    │\n  │  • File 2: Customer_ID [min: 2, max: 9998]  |  Product_ID [min: 12, max: 499]                    │\n  │  --> Tìm Đơn #8888 (Customer 501, Product 25) phải đọc CẢ 2 FILE vì khoảng Min/Max chồng lấn!    │\n  ├──────────────────────────────────────────────────────────────────────────────────────────────────┤\n  │ [+] SAU KHI CHẠY Z-ORDER BY (Customer_ID, Product_ID) / LIQUID CLUSTERING:                       │\n  │  • File 1: Customer_ID [min: 1,    max: 1000] | Product_ID [min: 10,  max: 100] <-- Chứa #8888!  │\n  │  • File 2: Customer_ID [min: 1001, max: 9999] | Product_ID [min: 101, max: 500]                  │\n  │  --> Tìm Đơn #8888 chỉ đọc đúng FILE 1, bỏ qua ngay FILE 2 (Data Skipping tối đa trên đa chiều)! │\n  └──────────────────────────────────────────────────────────────────────────────────────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '6.5c': {"ascii": "================================================================================================================================\n  1. COMPACTION (OPTIMIZE)                  2. DELETION VECTORS (BITMAP)                3. VACUUM / EXPIRE SNAPSHOTS\n┌──────────────────────────────────────┐  ┌────────────────────────────────────────┐  ┌────────────────────────────────────────┐\n│ • Nỗi đau: Streaming xả 1 phút/file  │  │ • Bản chất: Khi DELETE/UPDATE #8888,   │  │ • Nỗi đau: Giữ các tệp Parquet cũ      │\n│   ──> 43.200 tệp nhỏ 500 KB/tháng    │  │   không viết lại ngay tệp 512 MB       │  │   cho Time Travel làm phình S3.        │\n│   gây nghẽn HTTP GET trên S3.        │  │   mà ghi 1 mảng Roaring Bitmap siêu    │  │ • Giải pháp (VACUUM RETAIN 168 HRS):   │\n│ • Giải pháp (OPTIMIZE / Bin-pack):   │  │   nhỏ đánh dấu: 'Dòng 4.512 đã xóa'.   │  │   Xóa vĩnh viễn các tệp đã quá hạn     │\n│   Gộp hàng nghìn tệp nhỏ thành       │  │ • Lợi ích: Xóa/Sửa tức thì như MOR;    │  │   lưu giữ (7 ngày) & tệp mồ côi,       │\n│   tệp Parquet chuẩn 128 MB – 1 GB.   │  │   hợp nhất vật lý sau khi OPTIMIZE.    │  │   thu hồi dung lượng S3 & chuẩn GDPR.  │\n└──────────────────────────────────────┘  └────────────────────────────────────────┘  └────────────────────────────────────────┘\n================================================================================================================================", "kind": 'boxes'},
        '7.1a': {"ascii": '====================================================================================================\n                KIẾN TRÚC MULTI-HOP MEDALLION & CỔNG KIỂM SOÁT CHẤT LƯỢNG (QUALITY GATES)\n====================================================================================================\n\n  [Nguồn Batch] ──┐      ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐      ┌──► [BI / Reports]\n                  ├─────►│ [1] BRONZE LAYER│ ───► │ [2] SILVER LAYER│ ───► │ [3] GOLD LAYER  │ ─────┤\n  [Nguồn Stream] ─┘      │   (Raw Data)    │ Cổng │ (Cleaned & 3NF) │ Cổng │ (Curated/Star)  │      └──► [AI / ML Apps]\n  (Kafka / CDC)          └─────────────────┘ lọc 1└─────────────────┘ lọc 2└─────────────────┘\n                         • Landing zone thô       • Lọc sạch, khử trùng    • Tổng hợp sẵn KPI\n                         • Không cần Schema       • Cưỡng chế Schema,      • Phi chuẩn hóa tối\n                           khắt khe, giữ lịch       tiến hóa Schema          ưu đọc (Ít JOIN)\n                           sử để Replay!            khi cần thiết            cho người dùng cuối\n====================================================================================================', "kind": 'boxes'},
        '7.1b': {"ascii": '============================================================================================================================\n  1. ĐƯỜNG ỐNG 1-HOP TRỰC TIẾP (NGUỒN     THẲNG BI)             2. KIẾN TRÚC 3-TIERED MEDALLION (CÓ ĐIỂM FALLBACK)\n┌──────────────────────────────────────────────────────────┐  ┌────────────────────────────────────────────────────────────┐\n│ • [x] Gãy vụn tức thì: Chỉ cần 1 gói tin JSON của        │  │ • [+] Tầng Bronze làm mỏ neo bất biến: Cất giữ trọn vẹn    │\n│       Đơn #8889 bị lỗi định dạng là sập cả báo cáo CEO   │  │       lịch sử thô trên S3; khi cần sửa lỗi chỉ việc        │\n│ • [x] Không có điểm quay lui (No Fallback): Khi công     │  │       Replay từ Bronze -> Silver mà không chạm DB OLTP!    │\n│       thức tính KPI đổi, phải chọc ngược vào DB OLTP     │  │ • [+] Tầng Silver tái sử dụng toàn công ty: Làm sạch &     │\n│       đang chạy thật để kéo lại dữ liệu (Gây nghẽn!)     │  │       khử trùng Đơn #8888 đúng 1 lần cho mọi đội nhóm      │\n│ • [x] Trùng lặp công sức: 5 phòng ban phải tự viết lại   │  │ • [+] Linh hoạt mở rộng: Có thể nối Gold -> Gold tạo sản   │\n│       cùng 1 đoạn code làm sạch & khử trùng từ đầu       │  │       phẩm mới (hoặc nạp thẳng nguồn đã sạch vào Gold)     │\n└──────────────────────────────────────────────────────────┘  └────────────────────────────────────────────────────────────┘\n============================================================================================================================', "kind": 'boxes'},
        '7.2a': {"ascii": "========================================================================================================================\n  CƠ CHẾ CỘT BẢO TOÀN LỖI (PERMISSIVE PASSTHROUGH: _corrupt / _debug) & CÁCH LY DỮ LIỆU BẨN\n┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐\n│   [Luồng Kafka / CDC] ──> Gồm Đơn #8888 (Hợp lệ: 15M) + Đơn #8889 (Lỗi JSON: 'ERROR_TIMEOUT')                        │\n│                                            │                                                                         │\n│                                            ▼                                                                         │\n│   [Spark Permissive Mode: option('mode','PERMISSIVE').option('columnNameOfCorruptRecord','_corrupt')]                │\n│   ──> Ghi toàn bộ vào bảng 'bronze.sales_transactions_raw' (KHÔNG LÀM GÃY PIPELINE GIỮA ĐÊM!)                        │\n│       • Đơn #8888: order_id='8888' | raw_amount='15,000,000 VND' | _corrupt = NULL                                   │\n│       • Đơn #8889: order_id='8889' | raw_amount='ERROR_TIMEOUT'  | _corrupt = '{raw_err_payload}'                    │\n│                                            │                                                                         │\n│             ┌──────────────────────────────┴──────────────────────────────┐                                          │\n│             │ Cổng lọc 1: WHERE _corrupt IS NULL                          │ Cổng cách ly: WHERE _corrupt IS NOT NULL │\n│             ▼ (Bỏ cột _corrupt + Dedup + Ép kiểu DECIMAL)                 ▼ (Đẩy sang bảng cách ly + Bắn cảnh báo)   │\n│   [+] Bảng 'silver.orders_cleaned' (Đơn #8888 sạch)         [!] Bảng 'quarantine.corrupt_orders' (Chờ sửa & Replay)  │\n└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘\n========================================================================================================================", "kind": 'boxes'},
        '7.2b': {"ascii": '====================================================================================================\n          HÀNH TRÌNH LỘT XÁC CỦA ĐƠN HÀNG #8888 QUA 3 BẢNG LAKEHOUSE (BRONZE -> SILVER -> GOLD)\n====================================================================================================\n\n  [1] TẦNG BRONZE: Bảng "bronze.sales_transactions_raw" (Append-only, giữ nguyên bản từ CDC Kafka)\n  ┌──────────┬────────────────────┬──────────────────┬────────────────┬──────────────────────┬────────────┐\n  │ order_id │ raw_cust_name      │ raw_amount       │ store_code     │ _ingested_at         │ _corrupt   │\n  ├──────────┼────────────────────┼──────────────────┼────────────────┼──────────────────────┼────────────┤\n  │ "8888"   │ "  nguyen van a "  │ "15,000,000 VND" │ "STR_BD_01"    │ 2026-10-15 14:00:01  │ NULL       │\n  │ "8888"   │ "  nguyen van a "  │ "15,000,000 VND" │ "STR_BD_01"    │ 2026-10-15 14:00:02  │ NULL(Trùng)│\n  │ "8889"   │ NULL               │ "ERROR_TIMEOUT"  │ "STR_BD_01"    │ 2026-10-15 14:00:05  │ "{raw_err}"│\n  └──────────┴────────────────────┴──────────────────┴────────────────┴──────────────────────┴────────────┘\n                                                      │\n         [+] Pipeline Bronze --> Silver: Lọc bỏ dòng _corrupt != NULL, Khử trùng (Dedup) mã 8888,\n             Chuẩn hóa chữ hoa & kiểu số DECIMAL, nối chuẩn hóa thực thể (~3NF / SCD Type 2)\n                                                      ▼\n  [2] TẦNG SILVER: Bảng "silver.orders_cleaned" (Góc nhìn Doanh nghiệp chuẩn hóa ~3NF)\n  ┌──────────┬─────────────┬────────────┬──────────────────┬──────────────────────┐\n  │ order_id │ customer_sk │ store_sk   │ net_amount (DEC) │ order_timestamp      │\n  ├──────────┼─────────────┼────────────┼──────────────────┼──────────────────────┤\n  │ 8888     │ 501         │ 12         │ 15000000.00      │ 2026-10-15 14:00:01  │\n  └──────────┴─────────────┴────────────┴──────────────────┴──────────────────────┘\n                                                      │\n         [+] Pipeline Silver --> Gold: Áp quy tắc kinh doanh, phi chuẩn hóa thành Star Schema\n             hoặc gộp phẳng thành OBT (One Big Table) / Tổng hợp KPI doanh thu theo Tỉnh\n                                                      ▼\n  [3] TẦNG GOLD: Bảng "gold.obt_customer_sales_analytics" (Phi chuẩn hóa OBT - 0 JOIN cho BI!)\n  ┌──────────┬────────────────┬──────────────┬───────────────────────┬──────────────────┬─────────────────┐\n  │ order_id │ customer_name  │ province     │ store_branch_name     │ revenue_vnd      │ customer_tier   │\n  ├──────────┼────────────────┼──────────────┼───────────────────────┼──────────────────┼─────────────────┤\n  │ 8888     │ Nguyễn Văn A   │ Bình Dương   │ Showroom Bình Dương 1 │ 15000000.00      │ VIP_GOLD        │\n  └──────────┴────────────────┴──────────────┴───────────────────────┴──────────────────┴─────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '7.2c': {"ascii": "==============================================================================================================================\n  1. KHÓA LƯỢC ĐỒ (SCHEMA GATE)             2. RÀNG BUỘC CHECK CONSTRAINTS            3. DLT EXPECTATIONS & ICEBERG WAP\n┌──────────────────────────────────────┐  ┌──────────────────────────────────────┐  ┌────────────────────────────────────────┐\n│ • Tắt trộn lược đồ tự động:          │  │ • Khai báo bất biến cấp bảng:        │  │ • @dlt.expect: Ghi log cảnh báo        │\n│   mergeSchema = false (Mặc định)     │  │   ALTER TABLE silver.orders          │  │ • @dlt.expect_or_drop: Lọc dòng bẩn    │\n│ • Cấm ghi đè lược đồ bừa bãi:        │  │   ADD CONSTRAINT valid_amount        │  │ • @dlt.expect_or_fail: Dừng pipeline   │\n│   overwriteSchema = false            │  │   CHECK (net_amount > 0)             │  │ • Iceberg WAP (Write-Audit-Publish):   │\n│ • [+] Ngăn cột rác từ tầng Bronze    │  │ • [+] Vi phạm sẽ chặn ghi tức thì:   │  │   Ghi vào nhánh 'audit', kiểm định     │\n│   vô tình tràn sang làm bẩn Silver!  │  │   DeltaInvariantViolationException   │  │   Pass 100% mới nối sang nhánh 'main'  │\n└──────────────────────────────────────┘  └──────────────────────────────────────┘  └────────────────────────────────────────┘\n==============================================================================================================================", "kind": 'boxes'},
        '7.3a': {"ascii": '====================================================================================================\n             KIẾN TRÚC MEDALLION ĐƯỢC NÂNG ĐỠ BỞI CÁC DÒNG CHẢY NGẦM (THE UNDERCURRENTS)\n====================================================================================================\n\n      ┌───────────────────┐          ┌───────────────────┐          ┌───────────────────┐\n      │ [1] BRONZE LAYER  │ ───────► │ [2] SILVER LAYER  │ ───────► │  [3] GOLD LAYER   │\n      └─────────▲─────────┘          └─────────▲─────────┘          └─────────▲─────────┘\n                │                              │                              │\n  ══════════════╪══════════════════════════════╪══════════════════════════════╪══════════════\n  [+] DÒNG CHẢY NGẦM QUẢN TRỊ & VẬN HÀNH XUYÊN SUỐT (THE UNDERCURRENTS):\n  ├── [1] Data Catalog & Lineage : Unity Catalog / Hive Metastore / AWS Glue / Project Nessie\n  ├── [2] Security & Compliance  : Row-Level Security, Column Masking, Least Privilege, GDPR\n  └── [3] Cloud FinOps & Lifecycle: Hot --> Warm --> Cold/Archival (1/17 giá), Vacuum, Ephemeral Compute\n====================================================================================================', "kind": 'boxes'},
        '7.3b': {"ascii": "==========================================================================================================================\n  1. PHẢN MẪU: EXPORT RA 40 BUCKETS RIÊNG LẺ                   2. CHUẨN MỰC: SINGLE SOURCE OF TRUTH + CATALOG\n┌─────────────────────────────────────────────────────────┐  ┌───────────────────────────────────────────────────────────┐\n│ • Xuất (Export) các phân vùng bảng Đơn hàng ra 40       │  │ • Duy trì 1 bảng vật lý duy nhất trên S3, quản trị        │\n│   Buckets / Prefixes S3 riêng cho 40 đội nhóm:          │  │   qua định danh 3 cấp 'prod.gold.customer_sales':         │\n│ • [x] Ác mộng phân quyền: Phải cấp & thu hồi quyền      │  │ • [+] Phân quyền tập trung tại 1 nơi bằng SQL DCL         │\n│       IAM rời rạc ở cả 40 nơi (Rất dễ lộ lọt dữ liệu)   │  │       hoặc chia sẻ zero-copy qua Delta Sharing            │\n│ • [x] Đốt tiền khi Reprocess: Khi Đơn #8888 cần sửa     │  │ • [+] Sửa lỗi 1 lần cho tất cả: Khi Reprocess Đơn         │\n│       lỗi, phải tính toán lại 40 lần & gánh phí băng    │  │       #8888 tại bảng gốc, cả 40 đội nhóm thấy ngay        │\n│       thông mạng 2 chiều (Ingress & Egress) đắt đỏ!     │  │       số liệu chuẩn mà tốn $0 phí chép mạng dư thừa!      │\n└─────────────────────────────────────────────────────────┘  └───────────────────────────────────────────────────────────┘\n==========================================================================================================================", "kind": 'boxes'},
        '7.3c': {"ascii": '====================================================================================================\n            PHÂN QUYỀN CHI TIẾT TRÊN CÙNG 1 BẢNG GOLD (ROW-LEVEL SECURITY & COLUMN MASKING)\n====================================================================================================\n\n  Bảng gốc "gold.customer_sales":\n  ┌──────────┬────────────────┬───────────────┬────────────┬─────────────┐\n  │ order_id │ customer_name  │ phone_number  │ province   │ revenue_vnd │\n  ├──────────┼────────────────┼───────────────┼────────────┼─────────────┤\n  │ 8888     │ Nguyễn Văn A   │ 0909-123-456  │ Bình Dương │ 15.000.000  │\n  │ 9999     │ Trần Thị B     │ 0918-888-999  │ TP.HCM     │ 20.000.000  │\n  └──────────┴────────────────┴───────────────┴────────────┴─────────────┘\n         │                                           │\n         ├──► [+] Giám đốc Chi nhánh Bình Dương      ├──► [+] Chuyên viên Phân tích (Data Analyst)\n         │    (Áp dụng ROW-LEVEL SECURITY:           │    (Áp dụng COLUMN MASKING:\n         │     Chỉ thấy dòng có province=Bình Dương) │     Ẩn danh hóa số điện thoại cá nhân)\n         ▼                                           ▼\n  [Chỉ thấy Đơn #8888, không thấy Đơn #9999]   [Thấy cả 2 đơn, nhưng SĐT hiện "xxxx-xxx-456"]\n====================================================================================================', "kind": 'boxes'},
        '7.3d': {"ascii": '====================================================================================================\n          3 TẦNG NHIỆT ĐỘ LƯU TRỮ & CHÍNH SÁCH CLOUD FINOPS (HOT -> WARM -> COLD / ARCHIVAL)\n====================================================================================================\n  ┌──────────────────────────────┐  ┌──────────────────────────────┐  ┌────────────────────────────┐\n  │ 1. TẦNG NÓNG (HOT TIER)      │  │ 2. TẦNG ẤM (WARM TIER)       │  │ 3. TẦNG LẠNH (COLD/ARCHIVE)│\n  ├──────────────────────────────┤  ├──────────────────────────────┤  ├────────────────────────────┤\n  │ • Dữ liệu: Bảng Gold & Silver│  │ • Dữ liệu: Silver / Bronze   │  │ • Dữ liệu: Bronze quá hạn  │\n  │   truy vấn BI/ML hàng ngày   ├─►│   ít đọc sau 30 - 90 ngày    ├─►│   6-12 tháng (Audit/Replay)│\n  │ • Hạ tầng: S3/GCS Standard   │  │ • Hạ tầng: S3 Standard-IA /  │  │ • Hạ tầng: S3 Glacier /    │\n  │   + Cache NVMe SSD / RAM     │  │   GCS Nearline / Cool Blob   │  │   Deep Archive / Tape      │\n  │ • Giá: ~$0.020 - $0.023 / GB │  │ • Giá: ~$0.010 - $0.0125/GB  │  │ • Giá: ~$0.004 - $0.001/GB │\n  │ • Độ trễ: ~100 us - vài ms   │  │ • Lưu ý: Giữ tối thiểu >=30d │  │ • [+] Rẻ bằng 1/6 - 1/17!  │\n  └──────────────────────────────┘  └──────────────────────────────┘  └────────────────────────────┘\n====================================================================================================', "kind": 'boxes'},
        '7.4': {"ascii": '========================================================================================================================\n  BẢN ĐỒ KIẾN TRÚC 6 TẦNG CỦA HỆ THỐNG LƯU TRỮ HIỆN ĐẠI (BOTTOM-UP BLUEPRINT: CHẶNG 1 -> CHẶNG 7)\n┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐\n│   [TẦNG 6] CONSUMPTION & GOVERNANCE UNDERCURRENTS (Chặng 4 & Chặng 7)                                                │\n│   • Phục vụ: Power BI, Tableau, SQL Analytics, Data Science, Machine Learning / AI Agents                            │\n│   • Quản trị ngầm: Unity Catalog / Glue / Nessie, OpenLineage, Row/Col Security, GDPR, FinOps                        │\n│   ────────────────────────────────────────────────────────────────────────────────────────────────────────────────   │\n│   [TẦNG 5] DATA ORGANIZATION & MODELING — MEDALLION & KIMBALL (Chặng 4 & Chặng 7)                                    │\n│   • Luồng Multi-hop: Bronze (Raw Append-only/Replay + _corrupt) ──> Silver (Cleaned ~3NF/SCD2) ──> Gold (Curated)    │\n│   • Kỹ thuật Kimball tại Gold: Fact vs. Dimension, Star Schema / OBT (0 JOIN), Surrogate Key, Bus Matrix             │\n│   ────────────────────────────────────────────────────────────────────────────────────────────────────────────────   │\n│   [TẦNG 4] COMPUTE & STREAMING ENGINES — TÁCH RỜI KHỎI STORAGE (Chặng 3 & Chặng 6)                                   │\n│   • Batch & Query MPP: Apache Spark, Trino, Presto, Snowflake, BigQuery, Microsoft Fabric (Ephemeral Compute)        │\n│   • Streaming & Cache: Debezium CDC ──> Apache Kafka ──> Apache Flink (RocksDB State Store / Redis Cache)            │\n│   ────────────────────────────────────────────────────────────────────────────────────────────────────────────────   │\n│   [TẦNG 3] OPEN TABLE FORMATS — BỘ NÃO GIAO DỊCH LAKEHOUSE (Chặng 5 & Chặng 6)                                       │\n│   • Động cơ: Delta Lake (_delta_log) | Apache Iceberg (3-layer Metadata Tree) | Apache Hudi (Timeline + Index)       │\n│   • Sức mạnh: ACID, MVCC/OCC/NBCC, Time Travel, Schema Evolution, COW vs. MOR, Z-Order/Hilbert, Deletion Vectors     │\n│   ────────────────────────────────────────────────────────────────────────────────────────────────────────────────   │\n│   [TẦNG 2] FILE FORMATS, IN-MEMORY & COMPRESSION PRIMITIVES (Chặng 2)                                                │\n│   • Trên đĩa: Row-oriented (CSV, JSON, Avro + Sync Markers) vs. Columnar (Parquet Footer/RowGroup, ORC)              │\n│   • Trên RAM: Apache Arrow (Zero-copy SIMD) | Nén: Snappy, LZ4, ZSTD, Gzip & Tính phân tách (Splittability)          │\n│   ────────────────────────────────────────────────────────────────────────────────────────────────────────────────   │\n│   [TẦNG 1] PHYSICAL HARDWARE & STORAGE MODELS — NỀN MÓNG VẬT LÝ (Chặng 1, Chặng 2 & Chặng 3)                         │\n│   • Phần cứng: CPU Cache (1 ns) ──> RAM (100 ns, Volatile, Spill-to-Disk) ──> NVMe SSD (100 us) ──> HDD (4-10 ms)    │\n│   • Mô hình: Random Seek vs. Sequential Scan | File vs. Block vs. Object Storage (S3/ADLS/GCS ~100 ms) & HDFS (x3)   │\n└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘\n========================================================================================================================', "kind": 'boxes'},
    }
    for k, meta in diagrams.items():
        errs = verify_diagram(meta["ascii"], f"Storage-{k}", kind=meta["kind"])
        if errs:
            raise SystemExit(f"ASCII verification failed for Storage-{k} ({meta['kind']}): {errs}")
    return diagrams


def build_linux_ascii_diagrams() -> dict:
    diagrams = {
        '0.1': {"ascii": '====================================================================================================\n      HỒ SƠ NHÂN VẬT CHÍNH: CHIẾN DỊCH SĂN LÙNG NHẬT KÝ LỖI "grep ERROR /var/log/app.log"\n====================================================================================================\n\n  [BƯỚC 1: TỪ TĨNH SANG ĐỘNG (TERMINAL -> SHELL -> PROGRAM -> PROCESS)]\n  ┌──────────────────────────────────────────────┐      ┌──────────────────────────────────────────────┐\n  │ • Bạn gõ chuỗi tĩnh:                         │      │ • Shell (Bash) tra $PATH tìm /bin/grep       │\n  │   $ grep ERROR /var/log/app.log              │ ───► │ • Đánh thức Program tĩnh trên Disk thành     │\n  │   tại Terminal (Quầy giao tiếp)              │      │   Process sống trên RAM & CPU (PID = 4321)   │\n  └──────────────────────────────────────────────┘      └──────────────────────┬───────────────────────┘\n                                                                               │\n                                                                               ▼\n  [BƯỚC 4: TỰ ĐỘNG HÓA CÔNG NGHIỆP (BASH + MAKE + CRON)] [BƯỚC 2: VA CHẠM RANH GIỚI BẢO MẬT KERNEL]\n  ┌──────────────────────────────────────────────┐      ┌──────────────────────────────────────────────┐\n  │ • Bash Script : Đóng gói các bước thực thi   │      │ • Process trình phiếu System Call open()     │\n  │ • Makefile    : Chỉ biên dịch lại (GCC) khi  │ ◄─── │   lên Linux Kernel (Bếp trưởng)              │\n  │   file mã nguồn mới hơn (Timestamp)          │      │ • Kernel xét duyệt 5 thuộc tính căn cước:    │\n  │ • Cronjob     : Tự động kích hoạt mỗi 60s    │      │   PID, UID/GID, Working Dir, Env, Open Files │\n  └──────────────────────────────────────────────┘      └──────────────────────┬───────────────────────┘\n                                                                               │\n                                                                               ▼\n                                                        [BƯỚC 3: PHỐI HỢP DÂY CHUYỀN QUA 3 CỔNG & PIPE]\n                                                        ┌──────────────────────────────────────────────┐\n                                                        │ • Nối ống Pipe (|) qua stdin(0), stdout(1)   │\n                                                        │ • Tách riêng dòng báo lỗi qua cổng stderr(2) │\n                                                        └──────────────────────────────────────────────┘\n====================================================================================================', "kind": "boxes"},
        '0.2': {"ascii": '====================================================================================================\n                  BẢN ĐỒ CƠ HỌC LINUX: MÔ HÌNH "CĂN BẾP" & DÂY CHUYỀN TỰ ĐỘNG HÓA\n====================================================================================================\n\n [CHẶNG 1: KHỞI NGUỒN & LUỒNG CHẠY 1 LỆNH]              [CHẶNG 2: CĂN CƯỚC PROCESS & CÂY THƯ MỤC]\n (Gõ: grep ERROR /var/log/app.log)                      (Hồ sơ Process mang theo khi xin tài nguyên)\n\n ┌───────────────────────────────────────┐              ┌──────────────────────────────────────────┐\n │ [1] TERMINAL (Quầy giao tiếp)         │              │ HỒ SƠ MỘT PROCESS ĐANG CHẠY:             │\n │  • Nhận chuỗi ký tự & trả kết quả     │              │  ├── PID        : Mã định danh tiến trình│\n └───────────────────┬───────────────────┘              │  ├── User/Group : Quyền của ai? (root/me)│\n                     ▼                                  │  ├── Working Dir: Đứng ở đâu trên cây / ?│\n ┌───────────────────────────────────────┐              │  ├── Environment: Biến môi trường ($PATH)│\n │ [2] SHELL / BASH (Người nhận việc)    │              │  └── Open Files : Đang mở kênh đọc/ghi gì│\n │  • Phân tách lệnh: gọi ai, tham số gì │              └────────────────────┬─────────────────────┘\n └───────────────────┬───────────────────┘                                   │\n                     ▼                                                       ▼\n ┌───────────────────────────────────────┐              ┌──────────────────────────────────────────┐\n │ [3] PROGRAM (Công thức trên đĩa)      │              │ BẢN ĐỒ KHO HÀNG (UNIFIED FILESYSTEM /):  │\n │  • File nhị phân /bin/grep nằm tĩnh   │              │  • /bin, /sbin, /usr : Kệ chứa Program   │\n └───────────────────┬───────────────────┘              │  • /home, /root      : Phòng riêng User  │\n                     ▼                                  │  • /etc              : Tủ bảng cấu hình  │\n ┌───────────────────────────────────────┐              │  • /var/log, /tmp    : Kho log & Bàn tạm │\n │ [4] PROCESS (Đầu bếp đang làm việc)   ├─────────────►│  • /proc (0 MB Disk) : Cửa kính ảo trên  │\n │  • Cấp phát RAM, xếp hàng đợi CPU     │              │    RAM soi thẳng nội tạng CPU/Process    │\n └───────────────────┬───────────────────┘              └────────────────────┬─────────────────────┘\n                     │                                                       │\n                     └───────────────────────────┬───────────────────────────┘\n                                                 ▼\n ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐\n │ [5] SYSTEM CALL (Phiếu xin cấp phát tài nguyên: open, read, write, fork...)                     │\n └───────────────────────────────────────────────┬─────────────────────────────────────────────────┘\n                                                 ▼\n ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐\n │ [6] LINUX KERNEL (Bếp trưởng tối cao / Quản lý kho)                                             │\n │  • Kiểm tra đường dẫn + Quyền hạn (User/Group) + Cấp phát phần cứng chi tiết                    │\n └─────────┬─────────────────────────┬───────────────────────────┬─────────────────────────┬───────┘\n           ▼                         ▼                           ▼                         ▼\n   [ FILE (Sổ ghi) ]         [ CPU (Não tính) ]         [ RAM (Nhớ tạm) ]        [ NETWORK (Mạng) ]\n  ("Everything is a          (Chia lịch thực thi)       (Giữ biến, vùng nhớ      (Trao đổi gói tin\n   file": /dev, /proc)                                   process & đường Pipe)    với máy chủ khác)\n           │                         │                           │                         │\n===========┴─────────────────────────┴───────────────────────────┴─────────────────────────┴========\n                                                 │\n                                                 ▼\n [CHẶNG 3: PHỐI HỢP ĐA TIẾN TRÌNH (IPC)]                [CHẶNG 4: ĐÓNG GÓI & TỰ ĐỘNG HÓA 24/7]\n (Nhiều đầu bếp chuyền tay qua 3 cổng)                  (Biến thao tác thủ công thành dây chuyền)\n\n                     ┌──► [stdout: 1] ──(Đường PIPE trong Kernel)──► [stdin: 0] ──► [Process 2]\n [stdin: 0] ──► [Process 1]                                                              │\n                     └──► [stderr: 2] ──(Tách luồng lỗi riêng, không làm bẩn kết quả)    │\n                                                                                         ▼\n ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐\n │ BỘ BA TỰ ĐỘNG HÓA:                                                                              │\n │  [1] BASH SCRIPT (.sh) : Kịch bản định nghĩa "Làm những bước nào, logic rẽ nhánh ra sao"        │\n │           │                                                                                     │\n │           ▼                                                                                     │\n │  [2] COMPILATION & MAKE: GCC dịch mã C (.c -> .o -> binary); Make xét timestamp "Có cần làm lại"│\n │           │                                                                                     │\n │           ▼                                                                                     │\n │  [3] CRONJOB (crond)   : Trực ban thức dậy mỗi 60 giây, xét lịch (* * * * *) "Khi nào kích hoạt"│\n └─────────────────────────────────────────────────────────────────────────────────────────────────┘', "kind": "boxes"},
        '1.1a': {"ascii": '==========================================================================================\n        DỰ ÁN GNU (Những năm 1980)                     HẠT NHÂN LINUX (Năm 1991)\n     (Richard Stallman - "Khung sườn xe")             (Linus Torvalds - "Cục máy")\n==========================================================================================\n ┌──────────────────────────────────────────┐     ┌──────────────────────────────────────┐\n │ [+] Bash     : Màn hình dòng lệnh (CLI)  │     │ [+] CPU Scheduler : Chia lượt xử lý  │\n │ [+] Coreutils: Bộ lệnh ls, cp, mv, rm... │     │ [+] Memory Mgmt   : Cấp phát vùng RAM│\n │ [+] GCC      : Dịch code C/C++ -> 0 và 1 │     │ [+] Device Control: Điều khiển ổ đĩa,│\n │ [+] glibc    : Thư viện hàm (printf,...) │     │                     chuột, bàn phím  │\n │ [+] Emacs/GDB: Soạn thảo & soi lỗi code  │     │                                      │\n │ [!] NỖI ĐAU  : Thiếu hạt nhân (Kernel)   │     │ [!] NỖI ĐAU: Không có công cụ để bấm │\n └────────────────────┬─────────────────────┘     └───────────────────┬──────────────────┘\n                      │                                               │\n                      └───────────────────────┬───────────────────────┘\n                                              ▼\n               ┌─────────────────────────────────────────────────────────────┐\n               │           HỆ ĐIỀU HÀNH HOÀN CHỈNH: GNU/LINUX                │\n               │  • Người dùng gõ lệnh "grep ERROR app.log" qua công cụ GNU  │\n               │  • Hạt nhân Linux điều khiển ổ cứng & CPU đọc trả kết quả   │\n               └─────────────────────────────────────────────────────────────┘', "kind": "boxes"},
        '1.1b': {"ascii": '                        ┌───────────────────────────────────────┐\n                        │   TẠI SAO SERVER CHỌN GNU/LINUX?      │\n                        └───────────────────┬───────────────────┘\n      ┌───────────────────────┬─────────────┴─────────────┬───────────────────────┐\n      ▼                       ▼                           ▼                       ▼\n┌───────────┐           ┌───────────┐               ┌───────────┐           ┌───────────┐\n│ OPEN SRC  │           │ MULTI-USER│               │ SECURITY  │           │ GRANULAR  │\n│  • $0 phí │           │  • 50 dev │               │  • Khóa   │           │  CONTROL  │\n│  bản quyền│           │  cùng vào │               │  quyền    │           │  • Ép sát │\n│  cho 1.000│           │  1 server │               │  user     │           │  tới 10%  │\n│  máy chủ  │           │ không đụng│               │  thường vs│           │  CPU &    │\n│           │           │  vùng nhớ │               │  root     │           │  1GB RAM  │\n└───────────┘           └───────────┘               └───────────┘           └───────────┘', "kind": "boxes"},
        '1.2a': {"ascii": '                         ┌─────────────────────────────────────┐\n                         │    LÕI CỐT LÕI: GNU + LINUX KERNEL  │\n                         └──────────────────┬──────────────────┘\n           ┌────────────────────────────────┼────────────────────────────────┐\n           ▼                                ▼                                ▼\n ┌───────────────────┐            ┌───────────────────┐            ┌───────────────────┐\n │ NHÁNH DEBIAN      │            │ NHÁNH DOANH NGHIỆP│            │ NHÁNH TỰ LẮP RÁP  │\n │ ("Nồi đồng cối đá"│            │ (Fedora / RHEL)   │            │ (Arch Linux)      │\n │  chạy 10 năm      │            │  • "Xe bọc thép"  │            │  • Tự gõ lệnh cài │\n │  không sập)       │            │  • Ngân hàng,     │            │    ráp từng con   │\n └─────────┬─────────┘            │    viễn thông     │            │    ốc từ số 0     │\n           │                      │  • Thuê bao hỗ trợ│            └───────────────────┘\n           │                      │    kỹ thuật 24/7  │\n           ▼                      └───────────────────┘\n ┌────────────────────────────────────────────────────┐\n │ 3 BẢN PHÂN PHỐI PHÁI SINH PHỔ BIẾN TỪ NỀN DEBIAN:  │\n ├────────────────────────────────────────────────────┤\n │ [1] UBUNTU     : "Xe máy quốc dân" cho IT, Cloud,  │\n │                  AI/ML (Cập nhật 6 tháng/lần + LTS)│\n │ [2] LINUX MINT : Giao diện Cinnamon giống hệt      │\n │                  Windows 7/10, cài sẵn VLC, Office │\n │ [3] Kali LINUX : Hộp đồ nghề PenTest/An ninh mạng  │\n │                  (Cài sẵn Wireshark, Nmap...)      │\n └────────────────────────────────────────────────────┘', "kind": "boxes"},
        '1.2b': {"ascii": '====================================================================================================\n      GIẢI PHẪU CẤU TRÚC 4 LỚP BÊN TRONG MỘT BẢN PHÂN PHỐI LINUX (LINUX DISTRIBUTION ANATOMY)\n====================================================================================================\n\n  ┌────────────────────────────────────────────────────────────────────────────────────────────────┐\n  │ [LỚP 4: TRÌNH QUẢN LÝ GÓI & KHO PHẦN MỀM — PACKAGE MANAGER]                                    │\n  │  • Debian/Ubuntu: apt / dpkg (.deb)  |  RHEL/Fedora: dnf / yum / rpm (.rpm)  |  Arch: pacman   │\n  │  • Tự động tải phần mềm từ Repository, kiểm tra chữ ký số và giải quyết phụ thuộc (Dependency) │\n  └───────────────────────────────────────────────┬────────────────────────────────────────────────┘\n                                                  ▼\n  ┌────────────────────────────────────────────────────────────────────────────────────────────────┐\n  │ [LỚP 3: GIAO DIỆN NGƯỜI DÙNG — CLI SHELL vs DESKTOP ENVIRONMENT (GUI)]                         │\n  │  • Máy chủ (Server/Cloud): Chỉ cài CLI (Bash/Zsh) qua SSH -> Tiết kiệm 100% RAM/GPU đồ họa     │\n  │  • Máy trạm (Workstation): Gắn thêm X11/Wayland + GNOME, KDE Plasma hoặc XFCE                  │\n  └───────────────────────────────────────────────┬────────────────────────────────────────────────┘\n                                                  ▼\n  ┌────────────────────────────────────────────────────────────────────────────────────────────────┐\n  │ [LỚP 2: BỘ CÔNG CỤ HỆ THỐNG GNU & KHỞI ĐỘNG — GNU USERLAND & INIT SYSTEM (PID 1)]              │\n  │  • Thư viện C chuẩn (glibc), GNU Coreutils (ls, cp, mv, grep, cat), Bash Shell, GCC, Make      │\n  │  • Tiến trình khởi tạo đầu tiên (systemd / init - PID 1) quản lý toàn bộ dịch vụ chạy ngầm     │\n  └───────────────────────────────────────────────┬────────────────────────────────────────────────┘\n                                                  ▼\n  ┌────────────────────────────────────────────────────────────────────────────────────────────────┐\n  │ [LỚP 1: HẠT NHÂN LINUX — LINUX KERNEL (vmlinuz + Kernel Modules)]                              │\n  │  • Trực tiếp điều khiển CPU Scheduler, Memory Manager, Virtual File System (VFS) & Device I/O  │\n  └────────────────────────────────────────────────────────────────────────────────────────────────┘\n====================================================================================================', "kind": "boxes"},
        '1.3a': {"ascii": '===================================================================================================\n     KIẾN TRÚC 3 TẦNG (SLIDE)              LUỒNG CƠ HỌC "CĂN BẾP LINUX" (EXCALIDRAW)\n===================================================================================================\n                                    [ Người dùng gõ: grep ERROR app.log ]\n                                                      │\n                                                      ▼\n ┌──────────────────────────────┐   ┌─────────────────────────────────────────────────────────────┐\n │ TẦNG 3 & 2:                  │   │ [1] TERMINAL (Quầy giao tiếp)                               │\n │ GIAO TIẾP & THÔNG DỊCH       │   │  • Tiếp nhận chuỗi ký tự gõ vào & hiển thị phản hồi         │\n │                              │   └─────────────────┬───────────────────────────────────────────┘\n │  • Phân biệt rõ:             │                     ▼\n │    Shell (Xe hơi nói chung)  │   ┌─────────────────────────────────────────────────────────────┐\n │      └──> Bash (Xe Mec/BMW   │   │ [2] SHELL / BASH (Người nhận việc & Thông dịch viên)        │\n │           thuộc dự án GNU)   │   │  • Đọc yêu cầu, hiểu: cần chạy "grep", tìm chữ "ERROR"      │\n │             └──> Bash Script │   │    bên trong file "app.log"                                 │\n │                  (Chạy tự    │   └─────────────────┬───────────────────────────────────────────┘\n │                   động)      │                     ▼\n └──────────────┬───────────────┘   ┌─────────────────────────────────────────────────────────────┐\n                │                   │ [3] PROGRAM (Công thức nấu ăn tĩnh)                         │\n                │                   │  • File mã máy "grep" có sẵn trên đĩa (chưa có ai làm)      │\n                ▼                   └─────────────────┬───────────────────────────────────────────┘\n ┌──────────────────────────────┐                     ▼\n │ TẦNG 3 (Thực thi):           │   ┌─────────────────────────────────────────────────────────────┐\n │ ỨNG DỤNG ĐANG CHẠY           │   │ [4] PROCESS (Người đầu bếp đang làm theo công thức)         │\n │ (Applications / Processes)   │   │  • "grep" được nạp lên thành 1 Process sống, cần tài nguyên │\n └──────────────┬───────────────┘   │    để đọc file "app.log"                                    │\n                │                   └─────────────────┬───────────────────────────────────────────┘\n                │                                     ▼\n                │                   ┌─────────────────────────────────────────────────────────────┐\n                │                   │ [5] SYSTEM CALL (Phiếu đăng ký xin dùng tài nguyên)         │\n                │                   │  • Process gửi phiếu yêu cầu Kernel cho đọc "app.log"       │\n                ▼                   └─────────────────┬───────────────────────────────────────────┘\n ┌──────────────────────────────┐                     ▼\n │ TẦNG 1:                      │   ┌─────────────────────────────────────────────────────────────┐\n │ BẾP TRƯỞNG TỐI CAO           │   │ [6] LINUX KERNEL (Người quản lý kho & Tài nguyên tối cao)   │\n │ (The Kernel)                 │   │  • Kiểm tra đường dẫn file "app.log" & kiểm tra quyền đọc   │\n │  • Nắm quyền sinh sát        │   │  • Quyết định cái gì được đáp ứng, cấp phát phần cứng       │\n └──────────────┬───────────────┘   └────┬────────────────┬───────────────────┬──────────────┬────┘\n                │                        │                │                   │              │\n                ▼                        ▼                ▼                   ▼              ▼\n ════════════════════════════════   ┌──────────┐    ┌───────────┐       ┌───────────┐  ┌──────────┐\n           PHẦN CỨNG                │   FILE   │    │    CPU    │       │    RAM    │  │ NETWORK  │\n      (Hardware Resources)          │ (Sổ ghi  │    │ (Não thực │       │ (Bộ nhớ   │  │ (Kênh    │\n                                    │  chép dữ │    │  hiện phép│       │  tạm mọi  │  │ trao đổi │\n                                    │  liệu)   │    │  tính)    │       │  thứ)     │  │ máy khác)│\n                                    └──────────┘    └───────────┘       └───────────┘  └──────────┘', "kind": "boxes"},
        '1.3b': {"ascii": '  [BƯỚC 1] Bạn gõ lệnh ở Terminal:\n           $ grep ERROR app.log\n                 │\n                 ▼\n  [BƯỚC 2] Shell (Bash) phân tích cú pháp:\n           • Lệnh cần gọi : grep\n           • Chuỗi cần tìm: ERROR\n           • File mục tiêu: app.log\n                 │\n                 ▼\n  [BƯỚC 3] Khởi tạo Process từ Program:\n           • Công thức "grep" biến thành một Process đang sống.\n           • [!] NỖI ĐAU: Process không có quyền tự thò tay xuống ổ cứng lấy "app.log".\n                 │\n                 ▼\n  [BƯỚC 4] Gửi phiếu System Call xuống Kernel:\n           • Process: "Thưa Kernel, cho tôi mở và đọc dữ liệu từ đường dẫn \'app.log\'!"\n           • Kernel : Kiểm tra đường dẫn "app.log" + Kiểm tra quyền đọc của Process.\n                 │\n                 ▼\n  [BƯỚC 5] Phân chia trách nhiệm xử lý (ĐIỂM CỐT TỬ CẦN NHỚ):\n           ┌────────────────────────────────────────────────────────────────────┐\n           │ • TRÁCH NHIỆM CỦA KERNEL : Mở kho, lấy khối dữ liệu từ "app.log"   │\n           │                            đưa lên RAM cho Process theo đúng quyền.│\n           │ • TRÁCH NHIỆM CỦA PROCESS: Bản thân "grep" dùng CPU tự dò từng dòng│\n           │                            để lọc ra dòng có chữ "ERROR".          │\n           └────────────────────────────────────────────────────────────────────┘\n                 │\n                 ▼\n  [BƯỚC 6] Kết quả khớp ("ERROR...") được đẩy ngược lại màn hình Terminal cho bạn!', "kind": "boxes"},
        '2.1a': {"ascii": '====================================================================================================\n     GIẢI PHẪU QUY TRÌNH 3 BƯỚC SHELL ĐÁNH THỨC PROCESS & 5 THUỘC TÍNH CĂN CƯỚC (TASK_STRUCT)\n====================================================================================================\n\n  [A. BA BƯỚC SHELL ĐÁNH THỨC PROCESS KHI GÕ: $ grep ERROR app.log]\n  ┌──────────────────────────────┐     ┌──────────────────────────────┐     ┌──────────────────────────┐\n  │ [1] PARSE & EXPAND           │     │ [2] SEARCH $PATH             │     │ [3] SYSCALLS fork+execve │\n  │  • Tách lệnh "grep", mẫu     │     │  • Quét biến môi trường:     │     │  • fork() nhân bản con   │\n  │    "ERROR", đối số "app.log" │ ──► │    /usr/local/bin:/usr/bin:  │ ──► │  • execve("/bin/grep")   │\n  │  • Bung ký tự đại diện (*.log│     │    /bin                      │     │    nạp mã máy lên RAM    │\n  │    -> app.log, auth.log)     │     │  • Định vị trúng: /bin/grep  │     │    biến thành Process!   │\n  └──────────────────────────────┘     └──────────────────────────────┘     └─────────────┬────────────┘\n                                                                                          │\n                                                                                          ▼\n  [B. HỒ SƠ 5 THUỘC TÍNH CĂN CƯỚC CỦA MỘT PROCESS ĐANG CHẠY (TRONG LINUX KERNEL)]         │\n  ┌───────────────────────────────────────────────────────────────────────────────────────┴────────┐\n  │  ├── [1] PID & PPID       : PID = 4321 (Mã định danh tiến trình con; Cha Bash PPID = 1024)     │\n  │  ├── [2] User / Group     : UID = 1000 (dev), GID = 4 (adm) -> Quyết định quyền mở file        │\n  │  ├── [3] Working Dir (cwd): /var/log -> Gốc tọa độ để giải mã đường dẫn tương đối "app.log"    │\n  │  ├── [4] Environment      : PATH=/usr/bin:/bin, HOME=/home/dev, LANG=en_US.UTF-8               │\n  │  └── [5] Open Files (FD)  : 0 (stdin), 1 (stdout), 2 (stderr) + FD 3 trỏ tới /var/log/app.log  │\n  └────────────────────────────────────────────────────────────────────────────────────────────────┘\n====================================================================================================', "kind": "boxes"},
        '2.1b': {"ascii": '====================================================================================================\n      GIẢI MÃ CHUỖI 10 KÝ TỰ PHÂN QUYỀN (ls -lh) & PHÉP CHIẾU QUYỀN HẠN TRONG LINUX KERNEL\n====================================================================================================\n\n  [1. GIẢI PHẪU KẾT QUẢ LỆNH: $ ls -lh /var/log/app.log]\n  ┌────────────────────────────────────────────────────────────────────────────────────────────────┐\n  │     -      rw-      r--      ---     1     root     adm     1.5G   Mar 23 08:00   app.log      │\n  │    [1]     [2]      [3]      [4]           [5]      [6]     [7]                     [8]        │\n  │     │       │        │        │             │        │       └── Dung lượng tệp (1.5 Gigabyte) │\n  │     │       │        │        │             │        └────────── Nhóm sở hữu (Group = adm)     │\n  │     │       │        │        │             └─────────────────── Chủ sở hữu (Owner = root)     │\n  │     │       │        │        └──── [4] Others (o): --- (Người lạ: Cấm Đọc, Cấm Ghi, Cấm Chạy) │\n  │     │       │        └───────────── [3] Group  (g): r-- (Nhóm adm: Chỉ được Đọc, Cấm sửa/xóa)  │\n  │     │       └────────────────────── [2] User   (u): rw- (Chủ root: Được Đọc + Ghi)             │\n  │     └────────────────────────────── [1] Loại File : "-" = File thường | "d" = Thư mục          │\n  └───────────────────────────────────────────────┬────────────────────────────────────────────────┘\n                                                  │\n                                                  ▼\n  [2. PHÉP CHIẾU QUYỀN HẠN KHI PROCESS grep (UID=dev, GID=adm) GỌI SYSCALL open("app.log")]\n  ┌───────────────────────────────────────────────┴────────────────────────────────────────────────┐\n  │  • Bước 1 (So khớp Owner): UID(dev) != Owner(root) ──► Bỏ qua cụm "rw-"                        │\n  │  • Bước 2 (So khớp Group): GID(adm) == Group(adm)  ──► Áp dụng cụm "r--" -> Có "r" -> MỞ KHO!  │\n  │  • Bước 3 (Nếu là Guest) : Rơi vào cụm Others "---" ──► Kernel chặn đứng: Permission denied!   │\n  └────────────────────────────────────────────────────────────────────────────────────────────────┘\n====================================================================================================', "kind": "boxes"},
        '2.2a': {"ascii": '====================================================================================================\n       TRIẾT LÝ "EVERYTHING IS A FILE" & TẦNG TRỪU TƯỢNG VIRTUAL FILE SYSTEM (VFS - SLIDE 19)\n====================================================================================================\n\n  [1. BỐN THỰC THỂ KHÁC BIỆT TRONG HỆ THỐNG]\n  ┌───────────────────────┐ ┌───────────────────────┐ ┌──────────────────────┐ ┌───────────────────┐\n  │ [A] REGULAR FILES (-) │ │ [B] DIRECTORIES (d)   │ │ [C] DEVICES (b / c)  │ │ [D] PROCESSES     │\n  │ • /var/log/app.log    │ │ • /var/log, /home     │ │ • /dev/sda (Ổ cứng)  │ │ • /proc/meminfo   │\n  │ • code.c, backup.sh   │ │ • Bảng ánh xạ Inode   │ │ • /dev/null, /dev/tty│ │ • /proc/4321/fd   │\n  └───────────┬───────────┘ └───────────┬───────────┘ └──────────┬───────────┘ └─────────┬─────────┘\n              │                         │                        │                       │\n              └─────────────────────────┴────────────┬───────────┴───────────────────────┘\n                                                     ▼\n  [2. TẦNG TRỪU TƯỢNG VIRTUAL FILE SYSTEM (VFS) TRONG LINUX KERNEL]\n  ┌────────────────────────────────────────────────────────────────────────────────────────────────┐\n  │ • Hợp nhất mọi thiết bị phần cứng, ổ đĩa và RAM dưới CÙNG MỘT GIAO DIỆN SYSTEM CALLS duy nhất: │\n  │                       open()  ───►  read() / write()  ───►  close()                            │\n  │ • Hệ quả thực chiến: Kỹ sư dùng chung 1 bộ công cụ (cat, grep, cp, echo) để đọc log trên đĩa   │\n  │   (grep ERROR app.log), soi nội tạng RAM/CPU (cat /proc/meminfo) và sao lưu ổ cứng (/dev/sda)! │\n  └────────────────────────────────────────────────────────────────────────────────────────────────┘\n====================================================================================================', "kind": "boxes"},
        '2.2b': {"ascii": '====================================================================================================\n      GIẢI PHẪU CƠ HỌC DIRECTORY & INODE (FUN FACT SLIDE 19: TẠI SAO mv NHANH CÒN rm MẤT VĨNH VIỄN?)\n====================================================================================================\n\n  [1. BẢN CHẤT THƯ MỤC (/var/log/) CHỈ LÀ BẢNG ÁNH XẠ TÊN FILE -> SỐ INODE]\n  ┌───────────────────────────────────────────┐          ┌─────────────────────────────────────────┐\n  │ THƯ MỤC: /var/log/ (Directory Table)      │          │ KHO METADATA: Inode #98102              │\n  │ ┌────────────────────┬──────────────────┐ │          │  • Quyền & Chủ : -rw-r----- (root:adm)  │\n  │ │ Tên hiển thị       │ Con trỏ Inode    │ │          │  • Kích thước  : 1.5 GB (Link count = 1)│\n  │ ├────────────────────┼──────────────────┤ │  Trỏ tới │  • Con trỏ dữ liệu vật lý trên SSD:     │\n  │ │ app.log            │ Inode #98102     │─┼─────────►│    ──► [Block #401] [Block #402] ...    │\n  │ │ syslog             │ Inode #98105     │ │          └─────────────────────────────────────────┘\n  │ └────────────────────┴──────────────────┘ │\n  └─────────────────────┬─────────────────────┘\n                        │\n                        ▼\n  [2. HỆ QUẢ VẬT LÝ KHI CHẠY LỆNH mv, cp VÀ rm TRÊN FILE 1.5 GB (SLIDE 31–37)]\n  ┌─────────────────────┴──────────────────────────────────────────────────────────────────────────┐\n  │ • Đổi tên / Di chuyển cùng ổ đĩa (mv app.log old.log):                                         │\n  │   Chỉ sửa chuỗi "app.log" -> "old.log" trong bảng thư mục, giữ nguyên Inode #98102 -> Tốn 0s!  │\n  │ • Sao chép (cp app.log backup.log):                                                            │\n  │   Cấp phát Inode mới #99200 và chép toàn bộ 1.5 GB dữ liệu sang các Block ổ cứng mới.          │\n  │ • Xóa vĩnh viễn (rm app.log):                                                                  │\n  │   Gỡ dòng "app.log" khỏi bảng (unlink) & trả Inode #98102 về trạng thái trống -> 0 Thùng rác!  │\n  └────────────────────────────────────────────────────────────────────────────────────────────────┘\n====================================================================================================', "kind": "boxes"},
        '2.3a': {"ascii": '====================================================================================================\n      BẢN ĐỒ KHO HÀNG: CÂY THƯ MỤC HỢP NHẤT LINUX (UNIFIED FILESYSTEM HIERARCHY / - SLIDE 20-22)\n====================================================================================================\n\n                                  ┌───────────────────────────┐\n                                  │  / (ROOT DIRECTORY - GỐC) │\n                                  └─────────────┬─────────────┘\n                  ┌─────────────────────────────┼─────────────────────────────┐\n                  ▼                             ▼                             ▼\n  ┌───────────────────────────────┐ ┌───────────────────────────┐ ┌────────────────────────────────┐\n  │ [1. KHU NHÀ Ở USER (SLIDE 22)]│ │ [2. KHU HỆ THỐNG (SL 21)] │ │ [3. KHU TẠM & BIẾN ĐỔI (SL 22)]│\n  ├───────────────────────────────┤ ├───────────────────────────┤ ├────────────────────────────────┤\n  │ ├── /home                     │ │ ├── /bin  (ls, cp, grep)  │ │ ├── /tmp (Bàn nháp tạm thời;   │\n  │ │    ├── /home/fsds (~)       │ │ ├── /sbin (reboot, fdisk) │ │ │         tự xóa khi Reboot)   │\n  │ │    └── /home/dev            │ │ ├── /usr  (/usr/bin: git, │ │ └── /var (Biến đổi liên tục)   │\n  │ └── /root                     │ │ │          python, gcc)   │ │      ├── /var/log (app.log!)   │\n  │      (Phủ riêng của Admin     │ │ ├── /etc  (Tủ cấu hình:   │ │      ├── /var/www (Web Server) │\n  │       root, tách khỏi /home)  │ │ │          passwd, hosts) │ │      └── /var/lib (PostgreSQL) │\n  │                               │ │ └── /proc (Ảo trên RAM =  │ │                                │\n  │                               │ │            0 MB ổ cứng!)  │ │                                │\n  └───────────────────────────────┘ └───────────────────────────┘ └────────────────────────────────┘\n====================================================================================================', "kind": "boxes"},
        '2.3b': {"ascii": '====================================================================================================\n     ĐỐI CHIẾU ĐA GỐC WINDOWS (C:\\, D:\\) vs. CÂY HỢP NHẤT LINUX (/) & TUYỆT ĐỐI vs. TƯƠNG ĐỐI\n====================================================================================================\n\n  [A. ĐA GỐC THEO Ổ ĐĨA CỦA WINDOWS]                   [B. MỘT GỐC DUY NHẤT (/) & MOUNT CỦA LINUX]\n  ┌────────────────────────────────────────────┐       ┌───────────────────────────────────────────┐\n  │ • Ổ cứng SSD 1 ──► C:\\Windows\\System32     │       │ • Ổ cứng SSD 1 ──(mount)──► /             │\n  │ • Ổ cứng SSD 2 ──► D:\\Logs\\app.log         │       │ • Ổ cứng SSD 2 ──(mount)──► /var/log      │\n  │ • [!] Nỗi đau: Thay ổ đĩa vật lý làm đổi   │       │ • [+] Ưu việt: Gắn ổ 10TB mới vào nhánh   │\n  │   chữ cái ổ đĩa -> Gãy toàn bộ đường dẫn!  │       │   /var/log mà code không phải sửa 1 dòng! │\n  └────────────────────────────────────────────┘       └───────────────────────────────────────────┘\n\n  [C. PHÂN ĐỊNH ĐƯỜNG DẪN TUYỆT ĐỐI (ABSOLUTE PATH) vs. ĐƯỜNG DẪN TƯƠNG ĐỐI (RELATIVE PATH)]\n  ┌────────────────────────────────────────────────────────────────────────────────────────────────┐\n  │ Giả sử Process đang đứng tại thư mục làm việc: pwd = /var                                      │\n  │  1. ĐƯỜNG DẪN TUYỆT ĐỐI (Bắt đầu bằng gốc "/"):                                                │\n  │     $ grep ERROR /var/log/app.log   ──► Đứng ở bất kỳ đâu (hay trong Cronjob) đều trúng 100%!  │\n  │  2. ĐƯỜNG DẪN TƯƠNG ĐỐI (Tính từ vị trí đang đứng hiện tại; "." = hiện tại, ".." = lên cha):   │\n  │     $ grep ERROR log/app.log        ──► Ngắn gọn khi gõ tay, nhưng chạy sai nếu đứng lệch chỗ! │\n  └────────────────────────────────────────────────────────────────────────────────────────────────┘\n====================================================================================================', "kind": "boxes"},
        '2.4a': {"ascii": '====================================================================================================\n        BỘ CÔNG CỤ ĐIỀU HƯỚNG (pwd, ls, cd) & THAO TÁC FILE TRÊN CÂY THƯ MỤC (SLIDE 27–37)\n====================================================================================================\n\n  [1. NHÓM ĐỊNH VỊ & QUAN SÁT (NAVIGATION)]            [2. NHÓM KHỞI TẠO & BIẾN ĐỔI (MANIPULATION)]\n  ┌────────────────────────────────────────────┐       ┌───────────────────────────────────────────┐\n  │ • pwd (Print Working Directory - Slide 30):│       │ • touch & mkdir (Slide 33–34):            │\n  │   In tọa độ đứng hiện tại (/var/log)       │       │   - touch a.log   : Tạo file rỗng mới     │\n  │ • ls (List Directory Contents - Slide 28): │       │   - mkdir -p a/b/c: Tạo liền cả cây cha   │\n  │   - ls -lh : Hiện quyền, chủ, size (1.5G)  │ ────► │ • cp (Copy - Slide 31–32):                │\n  │   - ls -a  : Hiện cả file ẩn (.bashrc)     │       │   - cp app.log bak.log | cp -r dir1 dir2  │\n  │   - ls -lt : Xếp file mới cập nhật lên đầu │       │ • mv (Move/Rename - Slide 35–36):         │\n  │ • cd (Change Directory - Slide 29):        │       │   - Cùng thư mục = Đổi tên (0s I/O)       │\n  │   - cd /var/log | cd ~ | cd .. | cd -      │       │ • rm (Remove - Slide 37): rm / rm -r      │\n  └────────────────────────────────────────────┘       └───────────────────────────────────────────┘\n====================================================================================================', "kind": "boxes"},
        '2.4b': {"ascii": '====================================================================================================\n         CHIẾN THUẬT SOI FILE NHẬT KÝ KHỔNG LỒ (app.log 5 GB) & BỘ TỨ SĂN LÙNG (SLIDE 38–44)\n====================================================================================================\n\n  [1. BA CÁCH ĐỌC FILE LOG 5 GB: head vs. cat vs. tail -f]\n  ┌─────────────────────────────────────────┐       ┌──────────────────────────────────────────────┐\n  │  FILE: /var/log/app.log (Nặng 5.0 GB)   │       │ [A] head -n 20 app.log (Slide 39):           │\n  │ ┌─────────────────────────────────────┐ │       │     Chỉ cắt 20 dòng ĐẦU TIÊN -> Siêu nhẹ!    │\n  │ │ Dòng 1..20 (Phần đầu file)          │─┼──────►│ [B] cat app.log (Slide 38):                  │\n  │ ├─────────────────────────────────────┤ │       │     [!] Đổ cả 5 GB ra màn hình -> Treo máy!  │\n  │ │ ... Hàng chục triệu dòng ở giữa ... │─┼──────►│ [C] tail -n 20 app.log & tail -f (Slide 40): │\n  │ ├─────────────────────────────────────┤ │       │     Cắt 20 dòng CUỐI & giữ luồng mở để       │\n  │ │ Dòng cuối (Log mới đang bắn ra...)  │─┼──────►│     canh dòng lỗi bắn ra theo thời gian thực!│\n  │ └─────────────────────────────────────┘ │       └──────────────────────────────────────────────┘\n  └─────────────────────────────────────────┘\n\n  [2. BỘ TỨ ĐẶC NHIỆM KHI KHO /var/log BÁO ĐẦY ĐĨA (SLIDE 41–44)]\n  ┌────────────────────────────────────────────────────────────────────────────────────────────────┐\n  │  • du -sh /var/log/*                      : Đo dung lượng từng thư mục, chỉ mặt kẻ ngốn GB     │\n  │  • find /var/log -name "*.log" -size +1G  : Truy lùng chính xác các file log vượt ngưỡng 1 GB  │\n  │  • grep "ERROR" app.log | sed "s/a/b/g"   : Lọc dòng khớp mẫu (grep) & thay thế chuỗi (sed)    │\n  │  • man grep / man find                    : Mở cuốn từ điển hướng dẫn chính chủ ngay tại chỗ   │\n  └────────────────────────────────────────────────────────────────────────────────────────────────┘\n====================================================================================================', "kind": "boxes"},
        '3.1a': {"ascii": '===================================================================================================\n                    CẤU TRÚC 3 CỔNG GIAO TIẾP MẶC ĐỊNH CỦA MỌI PROCESS\n===================================================================================================\n\n                                  ┌───────────────────────────┐\n                                  │     PROCESS ĐANG CHẠY     │\n                                  │   (Ví dụ: grep ERROR...)  │\n  [ Dữ liệu đầu vào ]             │                           │            [ Kết quả bình thường ]\n  (Bàn phím / File /  ───────────►│ [Cổng 0]         [Cổng 1] │───────────► (Màn hình Terminal /\n   Đường ống Pipe)     stdin (0)  │  stdin             stdout │ stdout (1)   Đường ống Pipe / File)\n                                  │                           │\n                                  │         [Cổng 2]          │\n                                  │          stderr           │\n                                  └─────────────┬─────────────┘\n                                                │ stderr (2)\n                                                ▼\n                                  [ Thông báo lỗi đi đường riêng ]\n                                  (Không bao giờ trộn lẫn vào Cổng 1)', "kind": "boxes"},
        '3.1b': {"ascii": '===================================================================================================\n      PHÂN VAI CƠ HỌC KHI NỐI NHIỀU PROCESS: SHELL ĐẤU NỐI CỔNG - KERNEL GIỮ ĐƯỜNG PIPE\n===================================================================================================\n\n  [ PROCESS 1 (Ví dụ: grep) ]         [ TRONG LÕI LINUX KERNEL ]         [ PROCESS 2 (Xử lý tiếp) ]\n  (Chỉ làm việc riêng của nó)         (Giữ đường Pipe truyền byte)       (Chỉ làm việc riêng của nó)\n ┌───────────────────────────┐       ┌──────────────────────────┐       ┌───────────────────────────┐\n │                           │       │  [Shell nối cổng 1 -> 0] │       │                           │\n │  [stdin: 0]   [stdout: 1] ├──────►│ ════════════════════════ ├──────►│ [stdin: 0]    [stdout: 1] ├──►\n │                           │       │   ĐƯỜNG ỐNG PIPE (BYTE)  │       │                           │\n │               [stderr: 2] │       └──────────────────────────┘       │               [stderr: 2] │\n └─────────────────────┬─────┘                                          └─────────────────────┬─────┘\n                       │                                                                      │\n                       ▼ (Đi đường riêng)                                                     ▼\n        [ Cửa báo lỗi độc lập: Không làm bẩn dòng byte đang chảy sang Process 2 ]', "kind": "boxes"},
        '3.2a': {"ascii": '===================================================================================================\n      SO SÁNH TRẠNG THÁI DÒNG CHẢY: CHẠY NGẦM MẶC ĐỊNH VS. ĐIỀU HƯỚNG THU GOM LOG (2>&1)\n===================================================================================================\n\n [TRƯỚC] Chạy ngầm không điều hướng:                [SAU] Có gắn ">> /var/log/backup.log 2>&1":\n (Lỗi bị ném vào hư không, không thể điều tra)      (Gom cả Cổng 1 và Cổng 2 ghi nối đuôi vào File)\n\n   ┌──────────────────────────┐                       ┌──────────────────────────┐\n   │  PROCESS CHẠY NGẦM       │                       │  PROCESS CHẠY NGẦM       │\n   │  (tu_dong_backup.sh)     │                       │  (tu_dong_backup.sh)     │\n   └─────┬──────────────┬─────┘                       └─────┬──────────────┬─────┘\n         │              │                                   │              │\n  Cổng 1 │       Cổng 2 │                            Cổng 1 │       Cổng 2 │\n (stdout)│      (stderr)│                           (stdout)│      (stderr)│\n         ▼              ▼                                   │              │\n   [x] Mất dấu    [x] Rơi vào "sọt rác"                     │   (2>&1: Bẻ Cổng 2 nhập chung vào Cổng 1)\n   (Không có      (Sáng hôm sau kỹ sư                       │◄─────────────┘\n    màn hình)      mù tịt nguyên nhân lỗi!)                 │\n                                                            ▼ (>>: Ghi nối đuôi vào cuối file)\n                                              ┌──────────────────────────────────────────┐\n                                              │ FILE NHẬT KÝ: /var/log/backup.log        │\n                                              │  [+] Lưu toàn bộ kết quả đúng (stdout)   │\n                                              │  [+] Lưu toàn bộ thông báo lỗi (stderr)  │\n                                              └──────────────────────────────────────────┘', "kind": "boxes"},
        '3.2b': {"ascii": '====================================================================================================\n          MA TRẬN 6 TOÁN TỬ ĐIỀU HƯỚNG LUỒNG VÀO/RA (I/O REDIRECTION OPERATORS - SLIDE 55)\n====================================================================================================\n\n  ┌──────────────────┬─────────────────────────────┬───────────────────────────────────────────────┐\n  │ Toán tử Cú pháp  │ Cổng File Descriptor (FD)   │ Cơ chế Vận hành Vật lý & Cảnh báo An toàn     │\n  ├──────────────────┼─────────────────────────────┼───────────────────────────────────────────────┤\n  │ command > file   │ Cổng 1 (stdout)             │ [!] GHI ĐÈ (Overwrite): Xóa trắng nội dung cũ │\n  │                  │                             │ của file trước khi đổ kết quả mới vào!        │\n  ├──────────────────┼─────────────────────────────┼───────────────────────────────────────────────┤\n  │ command >> file  │ Cổng 1 (stdout)             │ [+] GHI NỐI ĐUÔI (Append): Bảo toàn dữ liệu cũ│\n  │                  │                             │ và viết tiếp xuống dòng cuối cùng (Chuẩn Log) │\n  ├──────────────────┼─────────────────────────────┼───────────────────────────────────────────────┤\n  │ command < file   │ Cổng 0 (stdin)              │ Bơm nội dung từ file vào cổng đọc thay vì chờ │\n  │                  │                             │ người dùng gõ từng phím trên bàn phím         │\n  ├──────────────────┼─────────────────────────────┼───────────────────────────────────────────────┤\n  │ command << EOF   │ Cổng 0 (stdin - HereDoc)    │ Truyền trực tiếp một khối văn bản nhiều dòng  │\n  │                  │                             │ cho đến khi gặp từ khóa kết thúc EOF          │\n  ├──────────────────┼─────────────────────────────┼───────────────────────────────────────────────┤\n  │ command 2> file  │ Cổng 2 (stderr)             │ Chỉ bắt riêng các dòng thông báo lỗi chảy vào │\n  │                  │                             │ file nhật ký lỗi (VD: error.log)              │\n  ├──────────────────┼─────────────────────────────┼───────────────────────────────────────────────┤\n  │ >> file 2>&1     │ Gộp Cổng 2 (stderr) vào 1   │ Bẻ ống lỗi (2) chập chung vào ống chuẩn (1)   │\n  │                  │                             │ và thu gom tất cả nối đuôi vào 1 file duy nhất│\n  └──────────────────┴─────────────────────────────┴───────────────────────────────────────────────┘\n====================================================================================================', "kind": "boxes"},
        '4.0': {"ascii": '===================================================================================================\n          BỘ BA TỰ ĐỘNG HÓA TRONG SƠ ĐỒ TƯ DUY: PHÂN ĐỊNH RÕ 3 CÂU HỎI CỐT LÕI\n===================================================================================================\n  [1] SHELL SCRIPT (.sh) ──────► Trả lời câu hỏi: "Làm những bước nào, trình tự ra sao?"\n            │\n            ▼\n  [2] MAKE (Makefile)    ──────► Trả lời câu hỏi: "File nào vừa sửa? Có cần biên dịch lại không?"\n            │\n            ▼\n  [3] CRONJOB (crond)    ──────► Trả lời câu hỏi: "Khi nào bắt đầu kích hoạt (schedule) luồng đó?"\n===================================================================================================', "kind": "boxes"},
        '4.1a': {"ascii": '===================================================================================================\n          GIẢI PHẪU FILE KỊCH BẢN (backup.sh) & HAI BƯỚC BẮT BUỘC ĐỂ CHẠY TRÊN LINUX\n===================================================================================================\n\n ┌───────────────────────────────────────────────────────────────────────────────────────────────┐\n │ #!/bin/bash                              <── [A. DÒNG SHEBANG]: Luôn ở dòng số 1! Báo cho     │\n │                                              Linux dùng trình thông dịch /bin/bash để chạy.   │\n │                                                                                               │\n │ TEN="Nam"                                <── [B. KHAI BÁO BIẾN]: CẤM có dấu cách quanh dấu =  │\n │ THU_MUC="/home/nam/tailieu"                  Muốn lấy giá trị ra dùng thì gắn dấu $ ($TEN).   │\n │ FILE="baocao.csv"                                                                             │\n │                                                                                               │\n │ if [ -f "$FILE" ]; then                  <── [C. LOGIC RẼ NHÁNH (if/else)]:                   │\n │     echo "Tìm thấy file, xử lý..."           Cờ "-f" kiểm tra xem file có tồn tại hay không   │\n │ else                                         để tự ra quyết định theo hoàn cảnh thực tế.      │\n │     echo "Cảnh báo: File không tồn tại!"                                                      │\n │ fi                                                                                            │\n │                                                                                               │\n │ for SERVER in server1 server2 server3; do <── [D. VÒNG LẶP (for)]: Duyệt tự động qua danh     │\n │     echo "Đang kiểm tra $SERVER..."           sách nhiều máy chủ mà không cần viết lặp lệnh.  │\n │ done                                                                                          │\n └──────────────────────────────────────────────┬────────────────────────────────────────────────┘\n                                                │\n                  [!] NỖI ĐAU BẢO MẬT: File văn bản mới tạo bị Linux KHÓA quyền chạy mặc định!\n                                                │\n                                                ▼\n ┌───────────────────────────────────────────────────────────────────────────────────────────────┐\n │ BƯỚC 1 (Mở khóa quyền chạy):  $ chmod +x backup.sh   (Cấp quyền thực thi - Execute cho file)  │\n │ BƯỚC 2 (Kích hoạt tại chỗ) :  $ ./backup.sh          (./ nghĩa là chạy file ở thư mục hiện tại│\n └───────────────────────────────────────────────────────────────────────────────────────────────┘', "kind": "boxes"},
        '4.1b': {"ascii": '====================================================================================================\n        ĐỐI CHIẾU TRÌNH SOẠN THẢO CLI (NANO vs. VIM) & CẤU TRÚC BASH SCRIPT (SLIDE 48–63)\n====================================================================================================\n\n  [1. HAI TRÌNH SOẠN THẢO TRÊN TERMINAL (KHÔNG CẦN CHUỘT)]\n  ┌─────────────────────────────────────────────┐     ┌────────────────────────────────────────────┐\n  │ [A] NANO (Đơn giản, gõ trực tiếp - Slide 49)│     │ [B] VIM (Mạnh mẽ, 3 chế độ - Slide 50–51)  │\n  │  • Mở file là gõ chữ ngay lập tức           │     │  • Normal Mode (Mặc định): Di chuyển, xóa  │\n  │  • Phím tắt hiển thị sẵn ở đáy màn hình:    │     │       │ (Nhấn phím "i")     ▲ (Nhấn "Esc") │\n  │    - Ctrl + O -> Enter : Lưu file (WriteOut)│     │       ▼                     │              │\n  │    - Ctrl + X          : Thoát khỏi Nano    │     │  • Insert Mode: Nhập code   │              │\n  │    - Ctrl + W          : Tìm kiếm chuỗi     │     │  • Command Mode (Gõ ":wq" lưu, ":q!" thoát)│\n  └─────────────────────────────────────────────┘     └────────────────────────────────────────────┘\n\n  [2. KHUNG XƯƠNG SỐNG CỦA MỘT BASH SCRIPT CÔNG NGHIỆP (SLIDE 52–63)]\n  ┌────────────────────────────────────────────────────────────────────────────────────────────────┐\n  │  #!/bin/bash                                  <-- [1] Shebang chỉ định trình thông dịch Bash   │\n  │  LOG_FILE="/var/log/app.log"                  <-- [2] Khai báo biến (Cấm khoảng trắng quanh =) │\n  │  if [ -f "$LOG_FILE" ]; then                  <-- [3] Rẽ nhánh điều kiện kiểm tra file tồn tại │\n  │      for kw in ERROR CRITICAL; do             <-- [4] Vòng lặp quét qua danh sách từ khóa lỗi  │\n  │          grep "$kw" "$LOG_FILE" >> alert.log  <-- [5] Lọc & điều hướng nối đuôi vào alert.log  │\n  │      done                                                                                      │\n  │  fi                                                                                            │\n  └────────────────────────────────────────────────────────────────────────────────────────────────┘\n====================================================================================================', "kind": "boxes"},
        '4.2a': {"ascii": '===================================================================================================\n            HÀNH TRÌNH BIẾN ĐỔI TRẠNG THÁI TRONG LÒ LUYỆN GCC: $ gcc chao.c -o chuong_trinh_chao\n===================================================================================================\n\n  [ MÃ NGUỒN: chao.c ]        (Ngôn ngữ C bậc cao con người đọc hiểu: #include <stdio.h>, printf...)\n           │\n           ▼  (Bước 1: TIỀN XỬ LÝ - Preprocessing)\n  [ Gom thư viện & Macro ]    • Gom nội dung các thư viện #include, xử lý các macro định nghĩa sẵn\n           │\n           ▼  (Bước 2: BIÊN DỊCH SANG HỢP NGỮ - Compilation)\n  [ Mã hợp ngữ: Assembly ]    • Chuyển đổi logic C thành tập lệnh hợp ngữ sát với kiến trúc phần cứng\n           │\n           ▼  (Bước 3: RÁP MÃ NHỊ PHÂN - Assembler)\n  [ Object File: .o ]         • Dịch thành mã nhị phân 0 và 1 từng phần rời (ví dụ: main.o, ham_phu.o)\n           │\n           ▼  (Bước 4: LIÊN KẾT - Linker)\n  [ FILE THỰC THI HOÀN CHỈNH ] • Gắn kết các file .o và thư viện hệ thống thành "chuong_trinh_chao"\n                              • Chạy trực tiếp trên CPU bằng lệnh: ./chuong_trinh_chao', "kind": "boxes"},
        '4.2b': {"ascii": '===================================================================================================\n         CƠ CHẾ QUYẾT ĐỊNH "CÓ CẦN LÀM LẠI KHÔNG?" CỦA MAKE DỰA TRÊN TIMESTAMP (THỜI GIAN SỬA)\n===================================================================================================\n\n  [Dự án gồm 2 nhánh nguyên liệu]\n   ├── Nhánh 1: main.c (Giữ nguyên không sửa) ──► [Make kiểm tra Timestamp] ──► [+] BỎ QUA main.o!\n   │                                                                                (Tiết kiệm giờ)\n   └── Nhánh 2: ham_phu.c (Vừa sửa 1 dòng!)   ──► [Timestamp mới hơn ham_phu.o]\n                                                               │\n                                                               ▼\n                                                  [!] CHỈ BIÊN DỊCH LẠI ĐÚNG ham_phu.c -> ham_phu.o\n                                                               │\n                                                               ▼\n                                                  [+] Ghép main.o (cũ) + ham_phu.o (mới) -> ung_dung\n\n---------------------------------------------------------------------------------------------------\n                 GIẢI PHẪU CÚ PHÁP FILE "Makefile" (CẢNH BÁO LỖI PHÍM TAB KINH ĐIỂN!)\n---------------------------------------------------------------------------------------------------\n  ung_dung: main.o ham_phu.o               <── TARGET (Mục tiêu): Sản phẩm muốn tạo ra ("ung_dung")\n  [TAB]gcc main.o ham_phu.o -o ung_dung        PREREQUISITES (Phụ thuộc): Nguyên liệu (main.o, ham_phu.o)\n                                               RECIPE (Công thức): Lệnh chạy. BẮT BUỘC lùi đầu dòng\n  main.o: main.c                               bằng 1 PHÍM TAB (Dùng phím Space sẽ báo lỗi ngay!)\n  [TAB]gcc -c main.c', "kind": "boxes"},
        '4.3a': {"ascii": '===================================================================================================\n         CƠ CHẾ VẬN HÀNH CỦA HỆ THỐNG CRON & GIẢI MÃ 5 TRƯỜNG THỜI GIAN (TRÁI SANG PHẢI)\n===================================================================================================\n\n  ┌──────────────────────────────────────────────────┐\n  │ 1. CUỐN SỔ LỊCH HẸN: CRONTAB (Quản lý qua lệnh)  │\n  │  • crontab -e : Mở sổ thêm/sửa lịch (chọn nano)  │\n  │  • crontab -l : In xem danh sách lịch đang cài   │\n  │  • crontab -r : XÓA SẠCH cuốn sổ (Không hỏi lại!)│\n  └────────────────────────┬─────────────────────────┘\n                           │ (Đọc dữ liệu lịch)\n                           ▼\n  ┌──────────────────────────────────────────────────┐\n  │ 2. TRỰC BAN CHẠY NGẦM: CROND (Cron Daemon)       │\n  │  • Chu kỳ: Cứ mỗi 60 GIÂY thức dậy kiểm tra 1 lần│\n  └────────────────────────┬─────────────────────────┘\n                           │ (Khớp giờ -> Kích hoạt!)\n                           ▼\n  ┌───────────────────────────────────────────────────────────────────────────────────────────────┐\n  │ 3. GIẢI MÃ 1 DÒNG NHIỆM VỤ (CRONJOB): Đi từ đơn vị thời gian NHỎ NHẤT đến LỚN NHẤT            │\n  │                                                                                               │\n  │    *          *          *          *          *       /home/nam/tu_dong_backup.sh            │\n  │    │          │          │          │          │                                              │\n  │    │          │          │          │          └───► [5] THỨ TRONG TUẦN  (0 - 6) (0 = CN)     │\n  │    │          │          │          └──────────────► [4] THÁNG TRONG NĂM (1 - 12)             │\n  │    │          │          └─────────────────────────► [3] NGÀY TRONG THÁNG(1 - 31)             │\n  │    │          └────────────────────────────────────► [2] GIỜ TRONG NGÀY  (0 - 23)             │\n  │    └───────────────────────────────────────────────► [1] PHÚT TRONG GIỜ  (0 - 59)             │\n  ├───────────────────────────────────────────────────────────────────────────────────────────────┤\n  │ 4 KÝ TỰ ĐẠI DIỆN ĐẶC BIỆT:                                                                    │\n  │  [+] Dấu sao (*)      : "MỌI" (mỗi phút, mỗi giờ, mỗi ngày đều chạy)                          │\n  │  [+] Dấu phẩy (,)     : Liệt kê các mốc rời nhau (VD phút: "15,45" -> chạy ở phút 15 và 45)   │\n  │  [+] Dấu gạch ngang(-): Khoảng liên tục (VD giờ: "9-17" -> từ 9h sáng đến 5h chiều)           │\n  │  [+] Dấu gạch chéo (/): Bước nhảy chu kỳ (VD phút: "*/10" -> cứ cách 10 phút chạy 1 lần)      │\n  └───────────────────────────────────────────────────────────────────────────────────────────────┘', "kind": "boxes"},
        '4.3b': {"ascii": '===================================================================================================\n       TẠI SAO CHẠY TAY TRÊN TERMINAL THÌ MƯỢT, ĐƯA VÀO CRONTAB THÌ NẰM IM KHÔNG HOẠT ĐỘNG?\n===================================================================================================\n\n  [CẠM BẪY 1: QUÊN ĐƯỜNG DẪN TUYỆT ĐỐI]\n   • Nguyên nhân cơ học: Khi gõ ở Terminal, Shell nạp sẵn danh bạ $PATH nên gõ "python" là hiểu.\n                         Khi Crond chạy ngầm, môi trường tối giản KHÔNG biết "python" nằm ở đâu!\n   • [x] Viết SAI : 0 2 * * * python backup.py\n   • [+] Viết ĐÚNG: 0 2 * * * /usr/bin/python3 /home/nam/scripts/backup.py  (Đủ từ gốc / đầu tiên)\n  ─────────────────────────────────────────────────────────────────────────────────────────────────\n  [CẠM BẪY 2: TIẾN TRÌNH CHẠY NGẦM NÉM LỖI VÀO SỌT RÁC]\n   • Nguyên nhân cơ học: Cron chạy ngầm không có màn hình. Lệnh lỗi không in ra đâu được.\n   • [x] Viết SAI : 0 3 * * * /home/nam/tu_dong_backup.sh\n   • [+] Viết ĐÚNG: 0 3 * * * /home/nam/tu_dong_backup.sh >> /var/log/backup.log 2>&1\n  ─────────────────────────────────────────────────────────────────────────────────────────────────\n  [CẠM BẪY 3: NHẦM LẪN QUYỀN HẠN GIỮA USER THƯỜNG VÀ ROOT]\n   • Nguyên nhân cơ học: Mỗi user có 1 sổ crontab riêng. Sổ của "nam" chỉ làm được việc "nam" có\n                         quyền. Muốn khởi động lại nginx hay dọn /var hệ thống phải dùng sổ Root!\n   • [x] Viết SAI : $ crontab -e        (Đang ở quyền user thường nhưng chạy lệnh quản trị hệ thống)\n   • [+] Viết ĐÚNG: $ sudo crontab -e   (Mở cuốn sổ Crontab của quyền tối cao Root)', "kind": "boxes"},
    }
    for k, meta in diagrams.items():
        errs = verify_diagram(meta["ascii"], f"Linux-{k}", kind=meta["kind"])
        if errs:
            raise SystemExit(f"ASCII verification failed for Linux-{k} ({meta['kind']}): {errs}")
    return diagrams


def build_db_ascii_diagrams() -> dict:
    diagrams = {
        '0.1': {"ascii": '====================================================================================================\n      BỐN HÌNH THÁI VẬT LÝ CỦA NHÂN VẬT CHÍNH: ĐƠN HÀNG TRÀ SỮA #HD01 (KHÁCH HÀNG LAN)\n====================================================================================================\n\n  [BẢN ĐỒ TƯ DUY 1 DÒNG (ONE-LINE MENTAL MAP)]\n  [Dữ liệu thô hỗn độn] --(1. Chuẩn hóa & Ràng buộc)--> [Bảng quan hệ sạch (3NF)]\n       |\n       +--(2. Đóng gói Page 8KB + Ghi WAL/RAM)--> [Bền vững vật lý trên Disk]\n       |\n       +--(3. MVCC + B-Tree Index + EXPLAIN)----> [Đọc/Ghi đồng thời tốc độ ms]\n       |\n       +--(4. Replication + Sharding + CAP/BASE)-> [Hệ thống phân tán chịu lỗi quy mô lớn]\n\n  +-----------------------------------------------+      +-----------------------------------------------+\n  | [HÌNH THÁI 1] DÒNG CHỮ THÔ (UNNORMALIZED UNF) |      | [HÌNH THÁI 2] BẢN GHI QUAN HỆ SẠCH (3NF)      |\n  +-----------------------------------------------+      +-----------------------------------------------+\n  | • #HD01 | Lan | 2026-09-26 | Oolong Sua       |      | • Phân rã thành 4 bảng chuẩn 3NF:             |\n  |   (30,000, SL:2), Hong Tra Tac (25,000, SL:1) | ---> |   KhachHang, HoaDon, MonAn, ChiTietHoaDon     |\n  | • [!] Nỗi đau: Dị thường Thêm / Sửa / Xóa     |      | • Cắm 4 chốt chặn: NOT NULL, DEFAULT,         |\n  |   (Insert / Update / Delete Anomalies)        |      |   UNIQUE, CHECK + Khóa PK / FK                |\n  +-----------------------------------------------+      +-----------------------+-----------------------+\n                                                                                 |\n                                                                                 v\n  +-----------------------------------------------+      +-----------------------------------------------+\n  | [HÌNH THÁI 4] ĐA PHIÊN BẢN & PHÂN MẢNH (HA)   |      | [HÌNH THÁI 3] KHỐI BYTE RAM & ĐĨA (8KB PAGE)  |\n  +-----------------------------------------------+      +-----------------------------------------------+\n  | • Tách nhiều phiên bản MVCC (xmin/xmax) +     |      | • Nằm trong khung 8KB Slotted Page trên       |\n  |   Autovacuum Worker dọn rác Dead Tuples       | <--- |   Shared Buffers (~1GB RAM)                   |\n  | • Chỉ mục B-Tree O(log N) vs LSM-Tree         |      | • Ghi nhật ký tuần tự mang mã LSN vào WAL     |\n  | • Nhân bản 6 PGD Nodes + Witness + Sharding   |      |   trước khi Checkpointer xả xuống Data Files  |\n  +-----------------------------------------------+      +-----------------------------------------------+\n====================================================================================================', "kind": "boxes"},
        '0.2': {"ascii": '====================================================================================================\n                  HÀNH TRÌNH CỦA ĐƠN HÀNG #HD01 QUA HỆ THỐNG CƠ SỞ DỮ LIỆU\n====================================================================================================\n\n  [CHẶNG 1: DATABASE FUNDAMENTALS & DATA MODELING] (Nền móng cấu trúc & Toàn vẹn dữ liệu)\n  +------------------------------------------------------------------------------------------------+\n  | Trạm 1.1: What is a Database & RDBMS Architecture                                              |\n  |   File phẳng lộn xộn ---> [DB Client Library] ---> [RDBMS Server] ---> [Database Files]        |\n  |                                    |                                                           |\n  |                                    v                                                           |\n  | Trạm 1.2: Relational Model, Keys (PK, FK), Cardinality (1:1, 1:N, M:N) & Constraints           |\n  |   Định hình thực thể ---> Cắm chốt chặn: [NOT NULL] + [DEFAULT] + [UNIQUE] + [CHECK]           |\n  |                                    |                                                           |\n  |                                    v                                                           |\n  | Trạm 1.3: Normalization (UNF -> 1NF -> 2NF -> 3NF -> BCNF) vs Denormalization                  |\n  |   Phân rã bảng gộp #HD01 ---> Tách 4 bảng sạch (KhachHang, HoaDon, MonAn, ChiTiet)             |\n  +------------------------------------+-----------------------------------------------------------+\n                                       |\n         [Nỗi đau chuyển giao]: Bảng 3NF đã sạch trên thiết kế logic, nhưng làm sao lưu xuống đĩa\n         vật lý vừa không mất dữ liệu khi sập nguồn, vừa không bị chậm bởi tốc độ I/O của ổ cứng?\n                                       |\n                                       v\n  [CHẶNG 2: STORAGE ENGINE & MEMORY ARCHITECTURE] (Giải phẫu động cơ PostgreSQL & Bộ nhớ)\n  +------------------------------------------------------------------------------------------------+\n  | Trạm 2.1: PostgreSQL Process & Memory Architecture + Configuration (postgresql.conf)           |\n  |   [Client Process] ---> Sinh [Backend Process] ---> Cấp phát RAM (shared_buffers = 8kB pages)  |\n  |                                    |                                                           |\n  |                                    v                                                           |\n  | Trạm 2.2: On-Disk Layout & Slotted Page (8KB Block) vs In-Memory DBMS                          |\n  |   Gom dòng #HD01 vào khung 8KB: [Page Header (LSN) | Line Pointers (Ptr) ---> Free <--- Tuple] |\n  |                                    |                                                           |\n  |                                    v                                                           |\n  | Trạm 2.3: Write Path, Shared Buffers (Dirty Pages), WAL Buffer & Checkpointer                  |\n  |   Sửa RAM (Dirty Page) + Ghi tuần tự [WAL Buffer -> WAL Files] ---> [Checkpointer (5 phút)]    |\n  +------------------------------------+-----------------------------------------------------------+\n                                       |\n         [Nỗi đau chuyển giao]: Đĩa và RAM đã phối hợp nhịp nhàng cho 1 người dùng, nhưng khi\n         1,000 người cùng đọc/sửa #HD01 và bảng phình lên 100 triệu dòng thì kẹt khóa và quét chậm!\n                                       |\n                                       v\n  [CHẶNG 3: CONCURRENCY CONTROL & QUERY EXECUTION] (Vận hành đồng thời & Tối ưu truy vấn)\n  +------------------------------------------------------------------------------------------------+\n  | Trạm 3.1: ACID Transactions, Lock Manager, MVCC & Autovacuum Worker                            |\n  |   Đọc không chặn ghi (Snapshot) ---> Sinh Tuple mới khi UPDATE ---> [Autovacuum] dọn rác       |\n  |                                    |                                                           |\n  |                                    v                                                           |\n  | Trạm 3.2: Storage Structures (B-Tree vs LSM-Tree) & Indexing Strategies                        |\n  |   Bỏ quét tuần tự (Seq Scan) ---> Nhảy qua cây cân bằng [B-Tree Index] / [Append-only LSM]     |\n  |                                    |                                                           |\n  |                                    v                                                           |\n  | Trạm 3.3: Query Optimizer, Execution Plan (EXPLAIN ANALYZE) & Administration Tools             |\n  |   [psql / pgAdmin 4] -> Giải phẫu chi phí truy vấn qua [EXPLAIN ANALYZE] & [pg_stat_statements]|\n  +------------------------------------+-----------------------------------------------------------+\n                                       |\n         [Nỗi đau chuyển giao]: Một máy chủ PostgreSQL (Single Node) dù tối ưu kịch trần vẫn chạm\n         ngưỡng vật lý CPU/RAM/Disk và đối mặt nguy cơ đứt cáp mạng hoặc cháy ổ cứng!\n                                       |\n                                       v\n  [CHẶNG 4: SCALABILITY, HIGH AVAILABILITY & NOSQL TRADE-OFFS] (Mở rộng quy mô & Phân tán)\n  +------------------------------------------------------------------------------------------------+\n  | Trạm 4.1: Vertical Scaling (Scale-up) vs Horizontal Scaling (Scale-out / Sharding)             |\n  |   Nâng cấp 1 máy chủ to ---> Chia nhỏ dữ liệu #HD01 ra nhiều Node (Partitioning / Sharding)    |\n  |                                    |                                                           |\n  |                                    v                                                           |\n  | Trạm 4.2: Replication (Sync/Async), High Availability (HA) & Distributed PostgreSQL            |\n  |   Nhân bản [Primary -> Replica], cấu trúc đa vùng (PGD 6 Nodes, Witness Node, Barman Backup)   |\n  |                                    |                                                           |\n  |                                    v                                                           |\n  | Trạm 4.3: SQL vs NoSQL Data Models, CAP Theorem (CA/CP/AP) & BASE Transactions                 |\n  |   Đánh đổi khi đứt mạng (Partition): Chọn [ACID / CP] hay [BASE / AP] (Eventual Consistency)?  |\n  +------------------------------------------------------------------------------------------------+', "kind": "boxes"},
        '1.0': {"ascii": '====================================================================================================\n     CHẶNG 1 OVERVIEW: DATABASE FUNDAMENTALS & DATA MODELING (TỪ FILE PHẲNG ĐẾN BẢNG CHUẨN 3NF)\n====================================================================================================\n\n  [TRẠM 1.1: RDBMS ARCHITECTURE]       [TRẠM 1.2: KEYS & CONSTRAINTS]       [TRẠM 1.3: NORMALIZATION (3NF)]\n  +------------------------------+     +------------------------------+     +------------------------------+\n  | • Khắc phục File phẳng:      |     | • Mô hình quan hệ E.F. Codd: |     | • Khử dị thường dữ liệu      |\n  |   [DB Client] ---> [RDBMS]   |     |   Table, Row (Tuple), Column |     |   (Insert / Update / Delete):|\n  |   ---> [Database Files]      | --> | • Khóa PK & FK (Toàn vẹn     | --> |   UNF -> 1NF -> 2NF -> 3NF   |\n  | • Chia sẻ truy cập an toàn   |     |   tham chiếu Referential)    |     | • Tách đơn #HD01 thành 4 bảng|\n  |   cho đơn hàng #HD01         |     | • Cardinality: 1:1, 1:N, M:N |     |   sạch (Lossless Join)       |\n  | • 5 nhóm SQL: DDL, DML, DQL, |     | • 4 Chốt: NOT NULL, DEFAULT, |     | • Đối sánh Denormalization   |\n  |   DCL, TCL                   |     |   UNIQUE, CHECK              |     |   có kiểm soát cho OLAP      |\n  +--------------+---------------+     +--------------+---------------+     +--------------+---------------+\n                 |                                    |                                    |\n                 +------------------------------------+------------------------------------+\n                                                      |\n                                                      v\n  +------------------------------------------------------------------------------------------------+\n  | [ĐẦU RA CHẶNG 1]: Đơn hàng #HD01 được chuẩn hóa thành 4 bảng 3NF (KhachHang, HoaDon, MonAn,    |\n  | ChiTietHoaDon) bảo vệ nghiêm ngặt bởi PK/FK và 4 chốt chặn Constraints trước khi chạm đĩa!     |\n  +------------------------------------------------------------------------------------------------+\n====================================================================================================', "kind": "boxes"},
        '1.1': {"ascii": '====================================================================================================\n      GIẢI PHẪU KIẾN TRÚC RDBMS KHI TIẾP NHẬN ĐƠN HÀNG #HD01 (CLIENT/SERVER & MODULAR ENGINE)\n====================================================================================================\n\n  [ APPLICATION CLIENT ]  (Quầy thu ngân gửi câu lệnh: INSERT #HD01 / SELECT #HD01)\n            |\n            v  (Gửi gói tin qua mạng tới DBMS Instance)\n  +------------------------------------------------------------------------------------------------+\n  | 1. TRANSPORT SUBSYSTEM                                                                         |\n  |    +----------------------------------------+      +----------------------------------------+  |\n  |    | [+] Client Communication               | <--> | [+] Cluster Communication              |  |\n  |    |     (Tiếp nhận kết nối từ ứng dụng)    |      |     (Giao tiếp với các Node khác)      |  |\n  |    +-------------------+--------------------+      +-------------------+--------------------+  |\n  +------------------------|-----------------------------------------------|-----------------------+\n                           v                                               |\n  +------------------------------------------------------------------------|-----------------------+\n  | 2. QUERY PROCESSOR                                                     |                       |\n  |    +-------------------------------------------------------------------+------------------+    |\n  |    | [+] Query Parser: Phân tích cú pháp SQL, kiểm tra hợp lệ & quyền truy cập (Access)   |    |\n  |    +-----------------------------------+--------------------------------------------------+    |\n  |                                        v                                                       |\n  |    +--------------------------------------------------------------------------------------+    |\n  |    | [+] Query Optimizer: Loại bỏ phần dư thừa, dựa vào thống kê (Index Cardinality,      |    |\n  |    |     Data Placement) để lập cây phụ thuộc (Dependency Tree) có chi phí thấp nhất      |    |\n  |    +-----------------------------------+--------------------------------------------------+    |\n  +----------------------------------------|-------------------------------------------------------+\n                                           v\n  +------------------------------------------------------------------------------------------------+\n  | 3. EXECUTION ENGINE                                                                            |\n  |    +----------------------------------------+      +----------------------------------------+  |\n  |    | [+] Local Execution                    |      | [+] Remote Execution                   |  |\n  |    |    (Thực thi dữ liệu tại Node hiện tại)|      |     (Điều phối thực thi từ Node xa)    |  |\n  |    +-------------------+--------------------+      +----------------------------------------+  |\n  +------------------------|-----------------------------------------------------------------------+\n                           v\n  +------------------------------------------------------------------------------------------------+\n  | 4. STORAGE ENGINE (Trái tim quản lý bộ nhớ & đĩa vật lý của từng Node)                         |\n  |                                                                                                |\n  |    +----------------------------------------+      +----------------------------------------+  |\n  |    | [!] Transaction Manager                |      | [!] Lock Manager                       |  |\n  |    |     Lập lịch giao dịch, bảo toàn       |      |     Khóa đối tượng đang chạy, giữ      |  |\n  |    |     trạng thái nhất quán logic         |      |     toàn vẹn vật lý khi chạy đồng thời |  |\n  |    +----------------------------------------+      +----------------------------------------+  |\n  |    +----------------------------------------------------------------------------------------+  |\n  |    | [+] Access Methods (Storage Structures): Quản lý tổ chức dữ liệu trên đĩa              |  |\n  |    |     (Heap Files, B-Trees trang 33, LSM-Trees trang 130)                                |  |\n  |    +----------------------------------------------------------------------------------------+  |\n  |    +----------------------------------------+      +----------------------------------------+  |\n  |    | [+] Buffer Manager                     |      | [+] Recovery Manager                   |  |\n  |    |     Đệm các trang đĩa (Pages) trên RAM |      |     Duy trì nhật ký thao tác (Log) để  |  |\n  |    |     (Trang 81)                         |      |     khôi phục khi sập nguồn (Trang 88) |  |\n  |    +----------------------------------------+      +----------------------------------------+  |\n  +------------------------------------------------------------------------------------------------+', "kind": "boxes"},
        '1.2': {"ascii": '====================================================================================================\n     GIẢI PHẪU THỰC THỂ (ERD), Lực LƯỢNG QUAN HỆ (CARDINALITY) & 4 CHỐT CHẶN CONSTRAINTS (#HD01)\n====================================================================================================\n\n  [1. LỰC LƯỢNG QUAN HỆ (CARDINALITY)]\n  +------------------------------------------------------------------------------------------------+\n  | • 1:1 (One-to-One)  : [KhachHang] (1) ---------- (1) [TheThanhVien_VIP]  (1 khách 1 thẻ riêng) |\n  | • 1:N (One-to-Many) : [KhachHang] (1) ---------- (<) [HoaDon]            (Lan đặt nhiều đơn)   |\n  | • M:N (Many-to-Many): [HoaDon]   (>) --- [ChiTietHoaDon] --- (<) [MonAn] (Tách bảng trung gian)|\n  +------------------------------------------------------------------------------------------------+\n\n  [2. SƠ ĐỒ THỰC THỂ LIÊN KẾT (ERD) & CƠ CHẾ KHÓA (KEYS)]\n  +------------------------------+          +------------------------------------------------------+\n  | BANG_KHACHHANG (Relation)    |          | BANG_HOADON (Relation)                               |\n  +------------------------------+          +------------------------------------------------------+\n  | [PK] MaKH    : VARCHAR(10)   | (1)  (<) | [PK] MaHD    : VARCHAR(10)  --> Định danh duy nhất   |\n  |      TenKH   : VARCHAR(100)  +--------->| [FK] MaKH    : VARCHAR(10)  --> Tham chiếu KhachHang |\n  |      SoDT    : VARCHAR(15)   |          |      NgayDat : DATE         --> Tối ưu tính thời gian|\n  +------------------------------+          +--------------------------+---------------------------+\n                                                                       | (1)\n                                                                       |\n                                                                       v (<)\n  +------------------------------+          +------------------------------------------------------+\n  | BANG_MONAN (Relation)        |          | BANG_CHITIET_HOADON (Associative Table xử lý M:N)   |\n  +------------------------------+          +------------------------------------------------------+\n  | [PK] MaMon   : VARCHAR(10)   | (1)  (<) | [PK, FK1] MaHD    : VARCHAR(10) (Composite PK phần 1)|\n  |      TenMon  : VARCHAR(100)  +--------->| [PK, FK2] MaMon   : VARCHAR(10) (Composite PK phần 2)|\n  |      DonGia  : DECIMAL(10,2) |          |           SoLuong : INTEGER                          |\n  +------------------------------+          +------------------------------------------------------+\n\n  [3. PHỄU LỌC 4 CHỐT CHẶN RÀNG BUỘC (DATABASE CONSTRAINTS) KHI GHI DÒNG #HD01]\n  Dữ liệu vào ---> [1. NOT NULL & DEFAULT] ---> [2. UNIQUE] ---> [3. CHECK (Logic)] ---> [4. PK / FK]\n                    (Cấm rỗng, tự điền mặc định) (Cấm trùng lặp)  (DonGia > 0, SL > 0)    (Toàn vẹn tham chiếu)', "kind": "boxes"},
        '1.3': {"ascii": '====================================================================================================\n      HÀNH TRÌNH PHÂN RÃ ĐƠN HÀNG #HD01 TỪ UNF -> 1NF -> 2NF -> 3NF (LOSSLESS DECOMPOSITION)\n====================================================================================================\n\n  [BƯỚC 0: UNF (Unnormalized Form - Bảng gộp lộn xộn)]\n  +------+------------+------+-------+------------+------------------------------------+\n  | MaHD | NgayDat    | MaKH | TenKH | SoDienThoai| DanhSachMon                        |\n  +------+------------+------+-------+------------+------------------------------------+\n  | HD01 | 2026-09-26 | KH01 | Lan   | 0901xxxxxx | Oolong (30k, SL:2), HongTra (25k)  |\n  | HD02 | 2026-09-26 | KH02 | Minh  | 0987xxxxxx | Oolong (30k, SL:1)                 |\n  +------+------------+------+-------+------------+------------------------------------+\n     |\n     | [!] Nỗi đau UNF: Ô DanhSachMon chứa nhiều giá trị -> Không thể chạy SQL tính tổng/đếm món.\n     v\n  [BƯỚC 1: 1NF (First Normal Form - Nguyên tử hóa / Atomic Values)]\n  Quy tắc: Mỗi ô chứa đúng 1 giá trị đơn lẻ + Thiết lập Khóa chính ghép (Composite PK: MaHD + MaMon)\n  +------+-------+------------+------+-------+------------+--------------+--------+---------+\n  | MaHD | MaMon | NgayDat    | MaKH | TenKH | SoDT       | TenMon       | DonGia | SoLuong |\n  +------+-------+------------+------+-------+------------+--------------+--------+---------+\n  | HD01 | M01   | 2026-09-26 | KH01 | Lan   | 0901xxxxxx | Oolong Sua   |  30000 |       2 |\n  | HD01 | M02   | 2026-09-26 | KH01 | Lan   | 0901xxxxxx | Hong Tra Tac |  25000 |       1 |\n  | HD02 | M01   | 2026-09-26 | KH02 | Minh  | 0987xxxxxx | Oolong Sua   |  30000 |       1 |\n  +------+-------+------------+------+-------+------------+--------------+--------+---------+\n     |\n     | [!] Nỗi đau 1NF (Phụ thuộc một phần - Partial Dependency):\n     |     • TenMon, DonGia chỉ phụ thuộc vào MaMon (không cần MaHD).\n     |     • NgayDat, MaKH, TenKH, SoDT chỉ phụ thuộc vào MaHD (không cần MaMon).\n     |     • Chỉ có SoLuong phụ thuộc hoàn toàn vào cả cặp khóa ghép (MaHD + MaMon).\n     v\n  [BƯỚC 2: 2NF (Second Normal Form - Khử phụ thuộc một phần)] -> Tách làm 3 bảng:\n  +--------------------------------------------+   +-----------------------------------+\n  | BANG_HOADON (PK: MaHD)                     |   | BANG_MONAN (PK: MaMon)            |\n  | MaHD | NgayDat    | MaKH | TenKH | SoDT    |   | MaMon | TenMon       | DonGia     |\n  | HD01 | 2026-09-26 | KH01 | Lan   | 0901xxx |   | M01   | Oolong Sua   |  30000     |\n  | HD02 | 2026-09-26 | KH02 | Minh  | 0987xxx |   | M02   | Hong Tra Tac |  25000     |\n  +--------------------------------------------+   +-----------------------------------+\n                        \\                                 /\n                         v                               v\n               +---------------------------------------------------+\n               | BANG_CHITIET_HOADON (PK ghép: MaHD + MaMon)       |\n               | MaHD (FK) | MaMon (FK) | SoLuong                  |\n               | HD01      | M01        |       2                  |\n               | HD01      | M02        |       1                  |\n               | HD02      | M01        |       1                  |\n               +---------------------------------------------------+\n     |\n     | [!] Nỗi đau 2NF (Phụ thuộc bắc cầu - Transitive Dependency trong BANG_HOADON):\n     |     • MaHD ---> MaKH ---> (TenKH, SoDT). Cột không khóa (TenKH, SoDT) phụ thuộc vào\n     |       một cột không khóa khác (MaKH). Nếu Lan đổi SĐT, phải sửa mọi hóa đơn của Lan!\n     v\n  [BƯỚC 3: 3NF (Third Normal Form - Khử phụ thuộc bắc cầu hoàn toàn)] -> Tách BANG_KHACHHANG:\n  +-----------------------------------+          +-------------------------------------+\n  | BANG_KHACHHANG (PK: MaKH)         |          | BANG_HOADON (PK: MaHD, FK: MaKH)    |\n  | MaKH | TenKH | SoDT               | (1)  (<) | MaHD | NgayDat    | MaKH            |\n  | KH01 | Lan   | 0901xxxxxx         +--------->| HD01 | 2026-09-26 | KH01            |\n  | KH02 | Minh  | 0987xxxxxx         |          | HD02 | 2026-09-26 | KH02            |\n  +-----------------------------------+          +-------------------------------------+', "kind": "boxes"},
        '2.0': {"ascii": '====================================================================================================\n    CHẶNG 2 OVERVIEW: STORAGE ENGINE & MEMORY ARCHITECTURE (8KB SLOTTED PAGE, WAL & CHECKPOINTER)\n====================================================================================================\n\n  [TRẠM 2.1: PROCESS & MEMORY]         [TRẠM 2.2: 8KB SLOTTED PAGE]         [TRẠM 2.3: WAL & CHECKPOINTER]\n  +------------------------------+     +------------------------------+     +------------------------------+\n  | • [Client] ---> [Postmaster] |     | • Khung trang 8KB chuẩn:     |     | • Sửa RAM -> Dirty Page      |\n  |   ---> [Backend Process]     |     |   - Page Header (mã LSN)     |     | • Luồng nhanh (COMMIT):      |\n  | • RAM riêng: work_mem = 5MB  | --> |   - Line Pointers (mọc xuôi) | --> |   WAL Buffer -> WAL Writer   |\n  | • RAM chung: shared_buffers  |     |   - Free Space ở giữa        |     |   -> WAL Files tuần tự (LSN) |\n  |   = 131584 pages (~1GB RAM)  |     |   - Tuple #HD01 (mọc ngược)  |     | • Luồng ngầm (5 phút/lần):   |\n  | • deadlock_timeout = 1000 ms |     | • Row-Store vs Column-Store  |     |   Checkpointer xả Data Files |\n  +--------------+---------------+     +--------------+---------------+     +--------------+---------------+\n                 |                                    |                                    |\n                 +------------------------------------+------------------------------------+\n                                                      |\n                                                      v\n  +------------------------------------------------------------------------------------------------+\n  | [ĐẦU RA CHẶNG 2]: Biến thao tác ghi ngẫu nhiên đắt đỏ (Random I/O) thành ghi nhật ký tuần tự   |\n  | (Sequential WAL I/O), đảm bảo đơn #HD01 bền vững tuyệt đối ngay cả khi rút phích cắm điện!     |\n  +------------------------------------------------------------------------------------------------+\n====================================================================================================', "kind": "boxes"},
        '2.1': {"ascii": '====================================================================================================\n      KIẾN TRÚC TIẾN TRÌNH & PHÂN CẤP BỘ NHỚ 2 TẦNG TRONG POSTGRESQL (SHARED MEMORY vs DISK)\n====================================================================================================\n\n  [ CLIENT PROCESS ] (Ứng dụng đặt trà sữa gửi kết nối & truy vấn cho đơn #HD01)\n          ^\n          |  (Mỗi kết nối Client sinh ra 1 Backend Process riêng biệt để thực thi SQL)\n          v\n  [ BACKEND PROCESS ] ---------------------+\n          |                                |\n          | (1. Ghi lịch sử thay đổi)      | (2. Đọc/Sửa trang dữ liệu trên RAM)\n          v                                v\n  +------------------------------------------------------------------------------------------------+\n  | RAM: SHARED MEMORY (Vùng bộ nhớ dùng chung giữa các tiến trình - Truy cập tốc độ cao)          |\n  |                                                                                                |\n  |  +------------------------------------------------------------------------------------------+  |\n  |  | [+] WAL BUFFER (Bộ đệm nhật ký ghi trước: Lưu tạm các thay đổi trước khi đẩy xuống đĩa)  |  |\n  |  +---------------------------------------------+--------------------------------------------+  |\n  |                                                |                                               |\n  |  +---------------------------------------------+  +-----------------------------------------+  |\n  |  | [+] SHARED BUFFERS                          |  | [+] TEMP BUFFERS                        |  |\n  |  |     (Đệm các trang dữ liệu truy cập thường  |  |     (Bộ đệm tạm thời cho từng phiên)    |  |\n  |  |      xuyên -> Giảm mạnh thời gian đọc đĩa)  |  +-----------------------------------------+  |\n  |  +---------------------------------------------+  +-----------------------------------------+  |\n  |  | [+] CLOG BUFFERS (Commit Log)               |  | [+] OTHER BUFFERS                       |  |\n  |  |     (Lưu trạng thái Commit/Abort giao dịch) |  |     (Các vùng đệm kiểm soát nội bộ khác)|  |\n  |  +---------------------------------------------+  +-----------------------------------------+  |\n  +-----------------------+-----------------------------------+------------------------------------+\n                          |                                   |\n                          v                                   v\n               (Tiến trình nền: WAL Writer)      (Tiến trình nền: Writer and Checkpointer)\n                          |                                   |\n                          v                                   v\n  +------------------------------------------------+  +--------------------------------------------+\n  | DISK: WAL FILES                                |  | DISK: DATA FILES                           |\n  | (Lưu bền vững nhật ký tuần tự thông qua Commit)|  | (Lưu trữ dài hạn các bảng & chỉ mục)       |\n  +------------------------------------------------+  +--------------------------------------------+\n                                                              ^\n                                                              | (Dọn dẹp bản ghi rác định kỳ)\n                                                  [ Autovacuum Launcher ] ---> [ Autovacuum Worker ]', "kind": "boxes"},
        '2.2': {"ascii": "====================================================================================================\n      GIẢI PHẪU CẤU TRÚC SLOTTED PAGE (4-16 KB) & ĐỐI SÁNH ROW-ORIENTED vs COLUMN-ORIENTED\n====================================================================================================\n\n  [1. BÊN TRONG MỘT KHỐI PAGE CỐ ĐỊNH (4-16 KB) CHỨA ĐƠN HÀNG #HD01]\n  +------------------------------------------------------------------------------------------------+\n  | PAGE HEADER (Chứa mã LSN - Log Sequence Number, trạng thái trang, biên vùng trống)             |\n  +------------------------------------------------------------------------------------------------+\n  | Con trỏ dòng (Line Pointers / Offset Array): [Ptr 1] --> [Ptr 2] --> [Ptr 3] ...               |\n  |   |                                            |           |                                   |\n  |   | (Mảng con trỏ mọc xuôi từ trên xuống)      |           +------------------------+          |\n  +---|--------------------------------------------|------------------------------------|----------+\n  |   v                                            |                                    |          |\n  |                              < VÙNG TRỐNG TỰ DO (FREE SPACE) >                      |          |\n  |                                                ^                                    |          |\n  +------------------------------------------------|------------------------------------|----------+\n  | ... [Dữ liệu Dòng 3: MaHD='HD02', MaMon='M01', SoLuong=1]                           |          |\n  | ... [Dữ liệu Dòng 2: MaHD='HD01', MaMon='M02', TenMon='Hong Tra Tac', DonGia=25000] <----------+\n  | ... [Dữ liệu Dòng 1: ID=10, MaHD='HD01', Ten='Lan', Mon='Oolong', DonGia=30000] <---+          |\n  |     (Các bản ghi dữ liệu mọc ngược từ đáy trang đi lên)                                        |\n  +------------------------------------------------------------------------------------------------+\n\n  [2. CÁCH SẮP XẾP DỮ LIỆU TRÊN ĐĨA: ROW-ORIENTED LAYOUT vs COLUMN-ORIENTED LAYOUT]\n  • Row-Oriented (Lưu liền kề theo từng dòng - Tối ưu giao dịch OLTP đọc/ghi nguyên đơn #HD01):\n    [ HD01 | 2026-09-26 | Lan | 30000 ] [ HD01 | 2026-09-26 | Lan | 25000 ] [ HD02 | 2026-09-26 | Minh | 30000 ]\n\n  • Column-Oriented (Lưu liền kề theo từng cột - Tối ưu phân tích OLAP tính tổng cột DonGia):\n    Cột MaHD  : [ HD01 | HD01 | HD02 ]\n    Cột TenKH : [ Lan  | Lan  | Minh ]\n    Cột DonGia: [ 30000| 25000| 30000] ---> Nén dữ liệu (Compression) cực tốt & chỉ đọc đúng cột cần tính!", "kind": "boxes"},
        '2.3': {"ascii": '====================================================================================================\n      GIẢI PHẪU LUỒNG GHI KÉP (WRITE PATH): WAL BUFFER vs SHARED BUFFERS (DIRTY PAGE) CHO #HD01\n====================================================================================================\n\n                        [ CLIENT / BACKEND PROCESS ]\n                     (Chạy lệnh: UPDATE DonGia = 30000)\n                                     |\n              +----------------------+----------------------+\n              | (1a. Ghi nhật ký tuần tự)                   | (1b. Đọc & Sửa trực tiếp trên RAM)\n              |      Ghi mã LSN (Log Sequence Number)       |      Gọi Page lên RAM rồi sửa nhỏ\n              v                                             v\n  +------------------------------------------------------------------------------------------------+\n  | RAM: SHARED MEMORY (Shared Buffers / Page Cache)                                               |\n  |                                                                                                |\n  |  +-------------------------------------------+     +----------------------------------------+  |\n  |  | [!] WAL BUFFER                            |     | [!] SHARED BUFFERS                     |  |\n  |  | • Ghi tuần tự lịch sử sửa:                |     | • Nạp Page chứa #HD01 từ đĩa lên RAM   |  |\n  |  |   "LSN #905: Page X, Dòng 1, Cột DonGia   |     | • Sửa trực tiếp DonGia = 30000         |  |\n  |  |    đổi thành 30000"                       |     | • Page bị đánh dấu thành: DIRTY PAGE   |  |\n  |  | • Xả RAM ngay khi đẩy xuống đĩa           |     | • Giữ lại trên RAM thong thả, chưa vội |  |\n  |  +---------------------+---------------------+     +--------------------+-------------------+  |\n  +------------------------|------------------------------------------------|----------------------+\n                           |                                                |\n        [Commit bắt buộc]  | Tiến trình: WAL Writer      [Định kỳ 5 phút]   | Tiến trình: Checkpointer\n        (Auto-commit đẩy   | (Ghi tuần tự - Sequential   (Chờ gom hàng      | (Ghi ngẫu nhiên - Random\n         LSN xuống ngay)   v  Append vô Disk)             nghìn Dirty Page) v  Overwrite theo Offset)\n  +------------------------------------------------------------------------------------------------+\n  | DISK STORAGE                                                                                   |\n  |  +-------------------------------------------+     +----------------------------------------+  |\n  |  | [+] DISK: WAL FILES                       |     | [+] DISK: DATA FILES                   |  |\n  |  | • Cấu trúc Append-only (Chỉ ghi nối đuôi) |     | • Chứa các Page cố định 4-16 KB        |  |\n  |  | • Dùng để Crash Recovery (Khôi phục lại   |     |   (Dữ liệu bảng & Index)               |  |\n  |  |   dữ liệu nếu sập nguồn trước khi         |     | • Có đánh Offset cho từng Page nên     |  |\n  |  |   Checkpointer kịp xả Dirty Page)         |     |   Checkpointer biết tìm đúng chỗ ghi đè|  |\n  |  +-------------------------------------------+     +----------------------------------------+  |\n  +------------------------------------------------------------------------------------------------+', "kind": "boxes"},
        '3.0': {"ascii": '====================================================================================================\n     CHẶNG 3 OVERVIEW: CONCURRENCY CONTROL & QUERY EXECUTION (MVCC, B-TREE vs LSM-TREE & EXPLAIN)\n====================================================================================================\n\n  [TRẠM 3.1: ACID, MVCC & VACUUM]      [TRẠM 3.2: B-TREE vs LSM-TREE]       [TRẠM 3.3: OPTIMIZER & EXPLAIN]\n  +------------------------------+     +------------------------------+     +------------------------------+\n  | • 4 tính chất ACID & Khóa    |     | • Bỏ Seq Scan O(N) chậm chạp |     | • Query Optimizer lập cây    |\n  | • MVCC (xmin / xmax): Đọc    |     | • B-Tree Index (Mutable 8KB, |     |   Execution Plan tối ưu      |\n  |   không bao giờ chặn Ghi!    | --> |   tối ưu Đọc O(log N) kèm    | --> | • Giải phẫu chi phí thực tế  |\n  | • UPDATE #HD01 sinh Tuple mới|     |   kỹ thuật Latch Crabbing)   |     |   bằng lệnh EXPLAIN ANALYZE  |\n  | • Autovacuum Worker dọn ngầm |     | • LSM-Tree (Immutable Append |     | • Săn truy vấn chậm qua      |\n  |   Dead Tuples chống phình    |     |   MemTable + SSTable + Bloom)|     |   pg_stat_statements & psql  |\n  +--------------+---------------+     +--------------+---------------+     +--------------+---------------+\n                 |                                    |                                    |\n                 +------------------------------------+------------------------------------+\n                                                      |\n                                                      v\n  +------------------------------------------------------------------------------------------------+\n  | [ĐẦU RA CHẶNG 3]: Hàng nghìn giao dịch đọc/sửa đơn #HD01 chạy đồng thời không khóa cứng nhau,  |\n  | truy vấn xuyên 100 triệu dòng trong vài mili-giây nhờ chỉ mục B-Tree và bộ tối ưu hóa!         |\n  +------------------------------------------------------------------------------------------------+\n====================================================================================================', "kind": "boxes"},
        '3.1': {"ascii": '====================================================================================================\n      GIẢI PHẪU RANH GIỚI GIAO DỊCH (ACID), CƠ CHẾ MVCC & TIẾN TRÌNH DỌN RÁC AUTOVACUUM (#HD01)\n====================================================================================================\n\n  [1. MỤC TIÊU CUỐI CỦA TRANSACTION & CONCURRENCY]\n  [Nhiều Request cùng Đọc/Ghi] ---> [Dữ liệu vẫn đúng (Isolation/Consistency)]\n                               ---> [Commit an toàn (Durability)]\n                               ---> [Gặp lỗi vẫn Rollback / Recover sạch sẽ (Atomicity)]\n\n  [2. CƠ CHẾ MVCC (MULTI-VERSION CONCURRENCY CONTROL) KHI SỬA ĐƠN HÀNG #HD01 TRÊN CÙNG PAGE]\n  Thời gian   Giao dịch T1 (Thu ngân sửa giá #HD01)       Giao dịch T2 (Quản lý đọc đơn #HD01)\n  ---------   -------------------------------------       ------------------------------------\n    t1        BEGIN; (TxID = 100)                         BEGIN; (TxID = 101)\n    t2        UPDATE MonAn SET DonGia = 30000             SELECT DonGia FROM MonAn\n              WHERE MaMon = \'M01\';                        WHERE MaMon = \'M01\';\n                   |                                           |\n                   | (Không ghi đè dòng cũ! Sinh dòng mới)     | (Đọc bản chụp Snapshot ổn định!)\n                   v                                           v\n              +-------------------------------------------------------------------------------+\n              | BÊN TRONG DATA PAGE (Trên Shared Buffers):                                    |\n              | • Tuple Phiên bản 1 (Cũ) : [MaMon=\'M01\' | DonGia=25000 | Đánh dấu hết hạn]    | <-- T2 đọc (25000)\n              | • Tuple Phiên bản 2 (Mới): [MaMon=\'M01\' | DonGia=30000 | Tạo bởi TxID=100]    | <-- T1 ghi (30000)\n              +-------------------------------------------------------------------------------+\n    t3        COMMIT; (Cập nhật trạng thái vào CLOG)      Đọc xong không bị chặn (Readers don\'t block Writers!)\n    t4                                                    COMMIT;\n    t5        [!] Tuple Phiên bản 1 (25000) trở thành "Dòng chết" (Dead Tuple / Deletion Marker)\n                   |\n                   v\n              [ AUTOVACUUM LAUNCHER ] ---> Gọi [ AUTOVACUUM WORKER ] quét dọn Tuple Phiên bản 1,\n                                           chống phân mảnh (Defragmentation) & thu hồi Vùng trống!', "kind": "boxes"},
        '3.2': {"ascii": "====================================================================================================\n      GIẢI PHẪU 2 CẤU TRÚC LƯU TRỮ TRÊN ĐĨA: B-TREE (MUTABLE) vs LSM-TREE (IMMUTABLE APPEND-ONLY)\n====================================================================================================\n\n  [1. CẤU TRÚC B-TREE INDEX (Cây tìm kiếm nhiều nhánh trên đĩa - Mặc định trong PostgreSQL & MySQL)]\n                          +---------------------------------------+\n                          | [Root Page]  Khóa phân tách:          |\n                          |   < 'HD50'      |      >= 'HD50'      |\n                          +--------+--------+----------+----------+\n                                   |                   |\n                   +---------------+                   +---------------+\n                   v                                                   v\n     +-----------------------------------+               +-----------------------------------+\n     | [Internal Node]                   |               | [Internal Node]                   |\n     |  'HD01'..'HD25' | 'HD26'..'HD49'  |               |  'HD50'..'HD75' | 'HD76'..'HD99'  |\n     +--------+--------+-----------------+               +-----------------------------------+\n              |\n              v  (Chỉ tốn vài bước nhảy con trỏ trang đĩa để định vị chính xác!)\n     +-------------------------------------------------------+     +-------------------------+\n     | [Leaf Page (Trang lá)] (Có con trỏ ngang Blink-Tree)  | <-> | [Leaf Page kế tiếp]     |\n     | • Key: 'HD01' ---> Con trỏ: (Page #42, Slot Ptr #1)   |     | • Key: 'HD26' ...       |\n     | • Key: 'HD02' ---> Con trỏ: (Page #42, Slot Ptr #3)   |     +-------------------------+\n     +--------------------------+----------------------------+\n                                |\n                                +---> Nhảy thẳng tới [Data File: Page #42, Ptr #1] lấy đơn #HD01!\n\n  [2. CẤU TRÚC LSM-TREE (Log-Structured Merge-Tree - Dùng trong RocksDB / MyRocks, Cassandra)]\n  Luồng Ghi (#HD01) ---> [1. Memtable (Trên RAM, sắp thứ tự)] + [Ghi WAL trên Disk]\n                                   |\n                                   | (Khi Memtable đầy -> Xả tuần tự thành file bất biến trên Disk)\n                                   v\n                         [2. Level 0: Immutable SSTables (Các file bất biến không bao giờ sửa đè)]\n                                   |\n                                   | (Tiến trình Compaction ngầm: Gộp & sắp xếp lại + Xóa Tombstones)\n                                   v\n                         [3. Level 1 -> Level N: Các SSTables lớn hơn đã sắp xếp thứ tự khóa]", "kind": "boxes"},
        '3.3': {"ascii": '====================================================================================================\n      GIẢI PHẪU BỘ TỐI ƯU HÓA TRUY VẤN (QUERY OPTIMIZER) & MÔ HÌNH PHÂN QUYỀN (LEAST PRIVILEGE)\n====================================================================================================\n\n  [1. HÀNH TRÌNH TỐI ƯU HÓA CÂU LỆNH TRUY VẤN ĐƠN HÀNG #HD01]\n  Câu lệnh SQL: SELECT h.MaHD, k.TenKH, m.TenMon, ct.SoLuong * m.DonGia AS ThanhTien ...\n        |\n        v\n  +------------------------------------------------------------------------------------------------+\n  | BƯỚC 1: QUERY PARSER (Kiểm tra cú pháp SQL & Kiểm tra quyền truy cập RBAC/PoLP)                |\n  +-----------------------------------------------+------------------------------------------------+\n                                                  |\n                                                  v\n  +------------------------------------------------------------------------------------------------+\n  | BƯỚC 2: QUERY OPTIMIZER (Loại bỏ phần dư thừa & Đánh giá chi phí dựa trên Thống kê nội bộ)     |\n  |   • Index Cardinality (Độ phân biệt của khóa MaHD, MaKH)                                       |\n  |   • Approximate Intersection Size (Kích thước giao cắt ước lượng khi JOIN 4 bảng 3NF)          |\n  |   • Data Placement (Vị trí đặt dữ liệu và chi phí truyền tải)                                  |\n  |          |                                                                                     |\n  |          +---> Lập Cây phụ thuộc (Dependency Tree) & Chọn Phương thức truy cập (Access Method):|\n  |                [x] Phương án A: Full Table Scan (Đọc toàn bộ hàng trăm nghìn dòng) -> LOẠI!    |\n  |                [+] Phương án B: B-Tree Index Scan trên PK/FK + Nested Loop Join    -> CHỌN!    |\n  +-----------------------------------------------+------------------------------------------------+\n                                                  |\n                                                  v\n  [KIỂM TRA BẰNG LỆNH: EXPLAIN (PostgreSQL) / EXPLAIN PLAN (MySQL)] ---> Thực thi tại STORAGE ENGINE', "kind": "boxes"},
        '4.0': {"ascii": '====================================================================================================\n     CHẶNG 4 OVERVIEW: SCALABILITY, HIGH AVAILABILITY & NOSQL (SHARDING, 6 PGD NODES & ĐỊNH LÝ CAP)\n====================================================================================================\n\n  [TRẠM 4.1: SCALE-UP vs SHARDING]     [TRẠM 4.2: HA, PGD & CONSENSUS]      [TRẠM 4.3: NOSQL, CAP & BASE]\n  +------------------------------+     +------------------------------+     +------------------------------+\n  | • Vertical (Scale-up): Nâng  |     | • Replication: Sync (0 mất   |     | • 4 Họ NoSQL: Key-Value,     |\n  |   CPU/RAM/NVMe trên 1 máy    |     |   dữ liệu) vs Async (nhanh)  |     |   Document, Column, Graph    |\n  | • Horizontal (Sharding):     | --> | • Kiến trúc Always-on EDB:   | --> | • Định lý CAP khi đứt mạng:  |\n  |   Băm ngang đơn #HD01..#HD99 |     |   6 PGD Nodes (2 vùng) +     |     |   Đánh đổi CP (ACID) vs AP   |\n  |   ra nhiều Node độc lập      |     |   PGD Proxy + Barman + PEM   |     |   (BASE - Eventual Consist.) |\n  | • Thách thức Cross-Shard JOIN|     | • Witness Node tại Vùng thứ 3|     | • Kiến trúc lai: PostgreSQL  |\n  |   & giao dịch phân tán 2PC   |     |   giữ phiếu Global Consensus |     |   (3NF + JSONB) + Redis Cache|\n  +--------------+---------------+     +--------------+---------------+     +--------------+---------------+\n                 |                                    |                                    |\n                 +------------------------------------+------------------------------------+\n                                                      |\n                                                      v\n  +------------------------------------------------------------------------------------------------+\n  | [ĐẦU RA CHẶNG 4]: Hệ thống cơ sở dữ liệu vượt thoát giới hạn 1 máy chủ vật lý, tự động chuyển  |\n  | đổi dự phòng (Failover) đa vùng địa lý và kết hợp hài hòa chuẩn ACID với tốc độ NoSQL/Cache!   |\n  +------------------------------------------------------------------------------------------------+\n====================================================================================================', "kind": "boxes"},
        '4.1': {"ascii": '====================================================================================================\n      GIẢI PHẪU SCALE-UP vs SCALE-OUT (SHARDING) & CƠ CHẾ REPLICATION (SYNC vs ASYNC) CHO #HD01\n====================================================================================================\n\n  [1. VERTICAL SCALING (Scale-up)]               [2. HORIZONTAL SCALING (Scale-out / Sharding)]\n  +------------------------------------+         +-------------------------------------------------+\n  | Một Máy chủ Duy nhất (Single Node) |         | Cụm Phân tán nhiều Máy chủ (Database Cluster)   |\n  |  [CPU x4]  ---> Nâng lên [CPU x64] |         |  • Shard 1 (Node A): Giữ đơn #HD01 .. #HD33     |\n  |  [RAM 16G] ---> Nâng lên [RAM 512G]|         |  • Shard 2 (Node B): Giữ đơn #HD34 .. #HD66     |\n  |  [HDD]    ---> Thay bằng [NVMe SSD]|         |  • Shard 3 (Node C): Giữ đơn #HD67 .. #HD99     |\n  +------------------------------------+         +-------------------------------------------------+\n\n  [3. ĐỐI SÁNH LUỒNG NHÂN BẢN: SYNCHRONOUS REPLICATION vs ASYNCHRONOUS REPLICATION]\n\n  • SYNCHRONOUS REPLICATION (Nhân bản đồng bộ - Đảm bảo 0 mất dữ liệu nhưng tăng độ trễ Commit):\n    [Client] ---(1. Ghi #HD01)---> [Primary Node] =====(2. Truyền Log qua mạng)=====> [Replica Node]\n    [Client] <--(4. Báo OK!)------ [Primary Node] <====(3. Xác nhận đã ghi ACK)====== [Replica Node]\n\n  • ASYNCHRONOUS REPLICATION (Nhân bản bất đồng bộ - Phản hồi cực nhanh nhưng có rủi ro trễ dữ liệu):\n    [Client] ---(1. Ghi #HD01)---> [Primary Node]\n    [Client] <--(2. Báo OK ngay!)- [Primary Node] - - -(3. Sao chép ngầm sau đó)- - -> [Replica Node]', "kind": "boxes"},
        '4.2': {"ascii": '====================================================================================================\n      KIẾN TRÚC ALWAYS-ON MULTI-LOCATION TRONG ENTERPRISEDB (6 PGD NODES + WITNESS NODE + BARMAN)\n====================================================================================================\n\n                  +-------------------------------------------------------+\n                  | VÙNG ĐỊA LÝ 3 (THIRD REGION - TRỌNG TÀI PHÂN XỬ)      |\n                  |   [!] WITNESS NODE (Không lưu dữ liệu - Chỉ bỏ phiếu  |\n                  |       giữ Global Consensus & Distributed DDL khi      |\n                  |       1 trong 2 vùng chính gặp sự cố sập toàn vùng)   |\n                  +-----------+-------------------------------+-----------+\n                              ^                               ^\n                              | (Kết nối đồng thuận toàn cục) |\n                              v                               v\n  +-----------------------------------------------+       +-----------------------------------------------+\n  | VÙNG ĐỊA LÝ 1 (LOCATION A - ACTIVE)           |       | VÙNG ĐỊA LÝ 2 (LOCATION B - ACTIVE / DR)      |\n  | (Đối xứng cấu hình & phần cứng dự phòng)      |       | (Đối xứng cấu hình & phần cứng dự phòng)      |\n  |                                               |       |                                               |\n  |  [Application]                                |       |  [Application]                                |\n  |       |                                       |       |       |                                       |\n  |       v                                       |       |       v                                       |\n  |  +-----------------------------------------+  |       |  +-----------------------------------------+  |\n  |  | [PGD Proxy 1] [PGD Proxy 2] [PGD Proxy 3]| |       |  | [PGD Proxy 4] [PGD Proxy 5] [PGD Proxy 6]| |\n  |  +------+-------------+-------------+------+  |       |  +------+-------------+-------------+------+  |\n  |         |             |             |         |       |         |             |             |         |\n  |         v             v             v         |       |         v             v             v         |\n  |  +----------+   +----------+   +----------+   |       |  +----------+   +----------+   +----------+   |\n  |  |Data Node1|<->|Data Node2|<->|Data Node3|   | <===> |  |Data Node4|<->|Data Node5|<->|Data Node6|   |\n  |  +----+-----+   +----------+   +----+-----+   | (Mesh |  +----------+   +----------+   +----------+   |\n  |       ^                             ^         |  Repl)|                                               |\n  |       +-----------------------------+         |       |                                               |\n  |        (Nhân bản chéo đầy đủ giữa Node 1 & 3) |       |                                               |\n  +-----------------------+-----------------------+       +-----------------------+-----------------------+\n                          |                                                       |\n                          +---------------------------+---------------------------+\n                                                      |\n                                                      v\n  +-------------------------------------------------------------------------------------------------------+\n  | HỆ THỐNG HẬU CẦN QUẢN TRỊ & PHỤC HỒI THẢM HỌA (OFFSITE BACKUP & MONITORING)                           |\n  |  • [+] BARMAN : Sao lưu và phục hồi (Backup & Recovery) ngoại vi cho nhiều cụm PGD (Đảm bảo RTO)      |\n  |  • [+] PEM    : Công cụ giám sát (Monitoring) sức khỏe và hiệu năng tập trung cho toàn bộ các cụm PGD |\n  +-------------------------------------------------------------------------------------------------------+', "kind": "boxes"},
        '4.3': {"ascii": '====================================================================================================\n      GIẢI PHẪU 4 MÔ HÌNH NOSQL, TAM GIÁC ĐÁNH ĐỔI ĐỊNH LÝ CAP & KIẾN TRÚC LAI (POSTGRESQL + REDIS)\n====================================================================================================\n\n  [1. TAM GIÁC ĐỊNH LÝ CAP (ERIC BREWER) KHI XẢY RA ĐỨT MẠNG (NETWORK PARTITION)]\n                            [ C: CONSISTENCY ] (Mọi Node thấy cùng dữ liệu tại cùng thời điểm)\n                                 /      \\\n                                /        \\\n         (Hệ thống CA:         /          \\         (Hệ thống CP:\n          RDBMS đơn vùng,     /   KHÔNG    \\         Ưu tiên dữ liệu đúng tuyệt đối,\n          Tài chính/Đặt chỗ  /   THỂ ĐẠT    \\        chấp nhận từ chối phục vụ khi\n          không chịu lỗi    /   CẢ 3 CÙNG    \\       mất kết nối liên vùng)\n          phân mảnh mạng)  /       LÚC!       \\\n                          /                    \\\n      [ A: AVAILABILITY ] ---------------------- [ P: PARTITION TOLERANCE ]\n      (Mọi yêu cầu đều nhận                      (Hệ thống vẫn vận hành dù đứt\n       được phản hồi)                             liên lạc mạng giữa các Node)\n                                    ^\n                                    |\n                     (Hệ thống AP - Mô hình BASE:\n                      Ưu tiên luôn phản hồi khách hàng, chấp nhận trạng thái mềm\n                      Soft State & Nhất quán cuối cùng Eventual Consistency)\n\n  [2. BỐN MÔ HÌNH DỮ LIỆU NOSQL vs ĐẠI DIỆN TRONG SLIDE & SÁCH]\n  +------------------------+------------------------+------------------------+------------------------+\n  | 1. KEY-VALUE STORES    | 2. DOCUMENT STORES     | 3. COLUMN-FAMILY       | 4. GRAPH DATABASES     |\n  | • Cấu trúc: Key -> Val | • Cấu trúc: JSON/BSON  | • Cấu trúc: Họ cột rộng| • Cấu trúc: Node & Edge|\n  | • Đại diện: Redis,     |   lồng nhau (Nested)   | • Đại diện: Cassandra, | • Đại diện: Neo4j,     |\n  |   Memcache, DynamoDB   | • Đại diện: MongoDB,   |   Apache HBase,        |   OrientDB             |\n  | • Tối ưu: Caching #HD01|   CouchDB, RavenDB     |   Hypertable           | • Tối ưu: Mạng quan hệ |\n  +------------------------+------------------------+------------------------+------------------------+\n\n  [3. KIẾN TRÚC THỰC TẾ HIỆN ĐẠI: KẾT HỢP POSTGRESQL (MULTI-MODEL) + REDIS CACHE]\n  [Client Request #HD01] ---> [1. Kiểm tra REDIS / MEMCACHE (Key-Value Cache kết quả truy vấn)]\n                                       |\n                        (Cache Miss)   v\n  +------------------------------------------------------------------------------------------------+\n  | POSTGRESQL BACKEND (Nền tảng Quan hệ ACID + Tích hợp sẵn sức mạnh NoSQL trước cả khi có tên!)  |\n  |  • Bảng chuẩn 3NF : Lưu giao dịch cốt lõi của #HD01 (Đảm bảo ACID & Referential Integrity)     |\n  |  • Kiểu JSON/JSONB: Lưu cấu trúc tài liệu động (Document) tương tự MongoDB BSON                |\n  |  • Extension hstore: Lưu các cặp khóa-giá trị (Key-Value pairs)                                |\n  |  • Extension ltree : Lưu và truy vấn cấu trúc cây/đồ thị (Graphs)                              |\n  +------------------------------------------------------------------------------------------------+', "kind": "boxes"},
    }
    for k, meta in diagrams.items():
        errs = verify_diagram(meta["ascii"], f"DB-{k}", kind=meta["kind"])
        if errs:
            raise SystemExit(f"ASCII verification failed for DB-{k} ({meta['kind']}): {errs}")
    return diagrams


def build_container_ascii_diagrams() -> dict:
    diagrams = {
        '0.1': {"ascii": '+--------------------------------------------------------------------------------------------------+\n|                        HỒ SƠ NHÂN VẬT CHÍNH: DỊCH VỤ "order-api" (app.py)                        |\n+--------------------------------------------------------------------------------------------------+\n| • Xuất thân    : Ứng dụng xử lý đơn hàng viết bằng Python (app.py) + Database PostgreSQL         |\n| • Nỗi sợ lớn   : Xung đột thư viện (Dependency Hell), bị cướp RAM/CPU, mất dữ liệu khi tắt máy   |\n| • Hành trình   : Lạc lõng trên Bare Metal (chỉ dùng 5-10% CPU)                                   |\n|               -> Bị nhốt trong Máy ảo (chịu thuế VM Tax nặng hàng chục GB, boot mất hàng phút)   |\n|               -> Tiến hóa thành Container (Host PID: 10423 nhưng tự thấy mình là Virtual PID: 1) |\n|               -> Nhân bản thành 3 Pod Replicas bất tử trên cụm máy chủ Kubernetes (K8s)          |\n+--------------------------------------------------------------------------------------------------+\n\n  [BỐN HÌNH THÁI TIẾN HÓA CỦA TIẾN TRÌNH "order-api" (app.py + PostgreSQL)]\n  +------------------------------------------------+      +------------------------------------------------+\n  | [1] BARE METAL SERVER (Trước 1998)             |      | [2] VIRTUAL MACHINE - VM (Từ 1998-2000)        |\n  |  • Chạy độc tôn trên máy chủ trần              | ---> |  • Hypervisor cắt phần cứng vật lý             |\n  |  • [!] Lãng phí 90-95% CPU/RAM, sợ xung đột    |      |  • [!] Thuế VM Tax: Guest OS nặng hàng GB      |\n  +------------------------------------------------+      +-----------------------+------------------------+\n                                                                                  |\n                                                                                  v\n  +------------------------------------------------+      +------------------------------------------------+\n  | [4] KUBERNETES CLUSTER (3 Pod Replicas HA)     |      | [3] LINUX CONTAINER (OS-level Virtualization)  |\n  |  • kubelet --[gRPC CRI]--> containerd / CRI-O  | <--- |  • Dùng chung Host Kernel (Namespaces+cgroups) |\n  |  • Tự phục hồi (Self-healing) & Zero-downtime  |      |  • Host PID 10423 -> Virtual PID 1, boot 1 giây|\n  +------------------------------------------------+      +------------------------------------------------+', "kind": "boxes"},
        '0.2': {"ascii": '====================================================================================================\n                  BẢN ĐỒ TƯ DUY 4 CHẶNG: TỪ BARE METAL ĐẾN ĐẠI DƯƠNG KUBERNETES\n====================================================================================================\n  +------------------------------------------------------------------------------------------------+\n  | [CHẶNG 1: TIẾN HÓA HẠ TẦNG (THỜI KỲ 1 -> THỜI KỲ 2)]                                           |\n  |  • Trạm 1.1: Bare Metal (Lãng phí 90-95% CPU) -> Hypervisor VM (Thuế VM Tax: Guest OS nặng GB) |\n  |  • Trạm 1.2: Container Model (OS Virtualization) dùng chung Host Kernel, boot 1s, chạy 50+ Pods|\n  +-----------------------------------------------+------------------------------------------------+\n                                                  | [!] Dùng chung Kernel làm sao cô lập & giới hạn?\n                                                  v\n  +------------------------------------------------------------------------------------------------+\n  | [CHẶNG 2: GIẢI PHẪU HỌC TẦNG NHÂN LINUX (LINUX KERNEL FOUNDATIONS)]                            |\n  |  • Trạm 2.1: Linux Namespaces (Cô lập góc nhìn: pid 10423 -> PID 1, net, mnt, ipc, uts, user)  |\n  |  • Trạm 2.2: Control Groups cgroups v2 (Định mức phần cứng: 2 CPU, 512MB RAM, 100MB/s Disk I/O)|\n  |  • Trạm 2.3: OverlayFS (LowerDir RO + UpperDir RW) + Capabilities & Seccomp lọc System Calls   |\n  +-----------------------------------------------+------------------------------------------------+\n                                                  | [!] Gõ lệnh Kernel thủ công quá phức tạp!\n                                                  v\n  +------------------------------------------------------------------------------------------------+\n  | [CHẶNG 3: CHU TRÌNH BUILD-SHIP-RUN & ĐỘNG CƠ OCI RUNTIME]                                      |\n  |  • Trạm 3.1: Build (Dockerfile) -> Ship (OCI Registry) -> Run + Persistent Volume cho Database |\n  |  • Trạm 3.2: Chuỗi OCI: Docker CLI -> dockerd -> containerd -> shim -> runc + Podman Rootless  |\n  +-----------------------------------------------+------------------------------------------------+\n                                                  | [!] Mở rộng 100 máy chủ: Ai tự cứu & cân tải?\n                                                  v\n  +------------------------------------------------------------------------------------------------+\n  | [CHẶNG 4: THỜI KỲ 3 — ĐIỀU PHỐI PHÂN TÁN VỚI KUBERNETES (ORCHESTRATION)]                       |\n  |  • Trạm 4.1: Chuẩn CRI (kubelet -> containerd/CRI-O) & Triết lý Khai báo (Declarative YAML)    |\n  |  • Trạm 4.2: Control Plane (apiserver, etcd, Controller, Scheduler) & Worker Nodes (Luồng 9b)  |\n  |  • Trạm 4.3: ReplicaSet (3 Pods), Deployment (Rolling Update), Service IPVS & Ingress L7       |\n  +------------------------------------------------------------------------------------------------+\n====================================================================================================', "kind": "boxes"},
        '1.0': {"ascii": '====================================================================================================\n      CHẶNG 1 OVERVIEW: TIẾN HÓA HẠ TẦNG (BARE METAL -> HYPERVISOR VM/VPS/CLOUD VM -> CONTAINER)\n====================================================================================================\n\n  [TRẠM 1.1: BARE METAL & VM TAX]      [MÔ PHỎNG 2D: 6 BÀI TOÁN HẠ TẦNG]    [TRẠM 1.2: CONTAINER MODEL]\n  +------------------------------+     +------------------------------+     +------------------------------+\n  | • Bare Metal: Chỉ dùng 5-10% |     | • Shared Hosting: Ở ghép,    |     | • OS-level Virtualization:   |\n  |   CPU/RAM, sợ Dependency Hell|     |   chung IP, lỗi 503 hàng xóm |     |   Vứt bỏ hoàn toàn Guest OS, |\n  | • Hypervisor (Type 1 & 2):   | --> | • VPS (1 máy mẹ SPOF) vs     | --> |   dùng chung Host OS Kernel  |\n  |   Chia cắt phần cứng vật lý  |     |   Cloud VM (Ceph 3x + Live   |     | • Nhẹ vài MB, khởi động tính |\n  | • [!] Thuế VM Tax: Nuôi      |     |   Migration chống sập nguồn) |     |   bằng giây, mật độ vọt lên  |\n  |   Guest OS nặng hàng chục GB |     | • Serverless: Scale-to-Zero  |     |   50+ Containers/host (3-5x) |\n  +--------------+---------------+     +--------------+---------------+     +--------------+---------------+\n                 |                                    |                                    |\n                 +------------------------------------+------------------------------------+\n                                                      |\n                                                      v\n  +------------------------------------------------------------------------------------------------+\n  | [ĐẦU RA CHẶNG 1]: Xóa sổ hoàn toàn "Thuế máy ảo" (VM Tax) bằng cách dùng chung Host OS Kernel, |\n  | đưa tiến trình order-api (app.py) vào kỷ nguyên đóng gói siêu nhẹ và khởi chạy tức thì!        |\n  +------------------------------------------------------------------------------------------------+\n====================================================================================================', "kind": "boxes"},
        '1.1': {"ascii": '====================================================================================================\n      THỜI KỲ 1: TỪ SỰ LÃNG PHÍ BARE METAL (TRƯỚC 1998) ĐẾN GÁNH NẶNG "VM TAX" (TỪ 1998-2000)\n====================================================================================================\n\n  [A. KIẾN TRÚC BARE METAL ĐƠN LẺ]                 [B. KIẾN TRÚC VIRTUAL MACHINES (HYPERVISOR)]\n  +------------------------------------+           +--------------+ +--------------+ +--------------+\n  |      Ung dung duy nhat: app.py     |           |    VM 1      | |    VM 2      | |    VM 3      |\n  |    (Workload lot thom: 5-10% CPU)  |           | +----------+ | | +----------+ | | +----------+ |\n  |                                    |           | |  App A   | | | |  App B   | | | |  App C   | |\n  |   [!] Lang phi 90-95% tai nguyen   |           | +----------+ | | +----------+ | | +----------+ |\n  |   [x] Khong dam chay chung App B   |           | | Bins/Lib | | | | Bins/Lib | | | | Bins/Lib | |\n  |       vi so xung dot Dependency    |           | +----------+ | | +----------+ | | +----------+ |\n  +------------------------------------+           | |Guest OS 1| | | |Guest OS 2| | | |Guest OS 3| |\n                    |                              | |(Hang GB!)| | | |(Hang GB!)| | | |(Hang GB!)| |\n                    v                              | +----------+ | | +----------+ | | +----------+ |\n  +------------------------------------+           +--------------+ +--------------+ +--------------+\n  |      Host OS chuyen dung           |                  |                |                |\n  +------------------------------------+                  +----------------+----------------+\n                    |                                                      |\n                    v                                                      v\n  +------------------------------------+           +------------------------------------------------+\n  |  Bare Metal Server khong lo        |           |   Hypervisor (Hardware Virtualization)         |\n  |  (Dot dien nang & chiem tu Rack)   |           |   Chia cat CPU, RAM, Disk vat ly thanh VMs     |\n  +------------------------------------+           +------------------------------------------------+\n                                                                           |\n                                                                           v\n                                                   +------------------------------------------------+\n                                                   |   Shared Bare Metal Server                     |\n                                                   +------------------------------------------------+\n\n  --------------------------------------------------------------------------------------------------\n  [!] PHẪU THUẬT ĐƯỜNG ĐI CỦA LỆNH TRONG HYPERVISOR TYPE 1 vs. TYPE 2:\n  • Type 1 (Bare-metal Hypervisor - vd: VMware ESXi):\n    [App: order-api] --> [Guest OS Kernel] --> [Hypervisor] --> [CPU / Memory Vật lý]\n  • Type 2 (Hosted Hypervisor - vd: QEMU, VirtualBox, Parallels, VMware Fusion/Workstation):\n    [App: order-api] --> [Guest OS Kernel] --> [Hypervisor Program] --> [Host OS] --> [CPU / Memory]\n    => Chậm chạp vì mỗi lệnh chạm phần cứng phải đi vòng qua cả Guest OS lẫn Host OS!\n====================================================================================================', "kind": "boxes"},
        '1.2': {"ascii": '====================================================================================================\n     THỜI KỲ 2 (2010-2013): ĐỐI CHIẾU CƠ HỌC KIẾN TRÚC MÁY ẢO (VM) vs. KIẾN TRÚC CONTAINER\n====================================================================================================\n\n  [KIẾN TRÚC MÁY ẢO - HARDWARE VIRTUALIZATION]      [KIẾN TRÚC CONTAINER - OS VIRTUALIZATION]\n  +------------------------------------------+      +------------------------------------------+\n  |            Tầng Ứng dụng & Libs          |      |     Các Container siêu nhẹ (Độc lập)     |\n  |  +----------+  +----------+  +---------+ |      |  +----------+  +----------+  +---------+ |\n  |  |  App 1   |  |  App 2   |  |  App 3  | |      |  |  App 1   |  |  App 2   |  |App 3..50| |\n  |  | (app.py) |  | (db.sql) |  | (redis) | |      |  | (app.py) |  | (db.sql) |  | (redis) | |\n  |  +----+-----+  +----+-----+  +----+----+ |      |  +----+-----+  +----+-----+  +----+----+ |\n  |       |             |             |      |      |       |             |             |      |\n  |       v             v             v      |      |       v             v             v      |\n  |  +----------+  +----------+  +---------+ |      |  +----------+  +----------+  +---------+ |\n  |  |Bins/Libs1|  |Bins/Libs2|  |Bins/Lib3| |      |  |Bins/Libs1|  |Bins/Libs2|  |Bins/Lib3| |\n  |  +----+-----+  +----+-----+  +----+----+ |      |  +----+-----+  +----+-----+  +----+----+ |\n  +-------|-------------|-------------|------+      +-------|-------------|-------------|------+\n          |             |             |                     |             |             |\n          v             v             v                     +-------------+-------------+\n  +------------------------------------------+                            |\n  | [!] ĐIỂM NGHẼN: VM TAX (LÃNG PHÍ LỚN)    |                            v\n  |  +----------+  +----------+  +---------+ |      +------------------------------------------+\n  |  |Guest OS 1|  |Guest OS 2|  |Guest OS3| |      |  [+] Container Engine (Docker / runc)    |\n  |  |(Hàng GB) |  |(Hàng GB) |  |(Hàng GB)| |      |      (Điều phối tiến trình siêu nhẹ)     |\n  |  +----+-----+  +----+-----+  +----+----+ |      +---------------------+--------------------+\n  +-------|-------------|-------------|------+                            |\n          +-------------+-------------+                                   v\n                        |                           +------------------------------------------+\n                        v                           |  [+] Host OS (Shared Linux Kernel)       |\n  +------------------------------------------+      |      (Dùng chung 1 nhân HĐH đã boot sẵn) |\n  |     Hypervisor (Ảo hóa phần cứng)        |      +---------------------+--------------------+\n  +---------------------+--------------------+                            |\n                        |                                                 v\n                        v                           +------------------------------------------+\n  +------------------------------------------+      |     Physical Server (Phần cứng vật lý)   |\n  |     Physical Server (Phần cứng vật lý)   |      +------------------------------------------+\n  +------------------------------------------+\n   => KẾT QUẢ: Nặng hàng GB | Boot mất phút          => KẾT QUẢ: Nhẹ vài MB | Boot trong giây\n               Tối đa ~10 VMs / Server                           Chạy 50+ Containers / Server\n====================================================================================================', "kind": "boxes"},
        '2.0': {"ascii": '====================================================================================================\n     CHẶNG 2 OVERVIEW: GIẢI PHẪU HỌC TẦNG NHÂN LINUX (NAMESPACES, CGROUPS V2, OVERLAYFS & SECCOMP)\n====================================================================================================\n\n  [TRẠM 2.1: LINUX NAMESPACES]         [TRẠM 2.2: CONTROL GROUPS V2]        [TRẠM 2.3: OVERLAYFS & SECURITY]\n  +------------------------------+     +------------------------------+     +------------------------------+\n  | • Cô lập góc nhìn (Isolation)|     | • Định mức vật lý (Limits):  |     | • Syscalls: clone(CLONE_NEW*)|\n  |   qua 6 Namespaces:          |     |   cpu.max, memory.max, BlkIO |     |   unshare(), pivot_root()    |\n  |   pid, net, mnt, ipc, uts,   | --> | • Cont A (order-api): Khóa   | --> | • OverlayFS (Copy-on-Write): |\n  |   user                       |     |   tối đa 2 CPU, 512 MB RAM   |     |   LowerDir (RO) + UpperDir   |\n  | • Host PID 10423 & 10424 đều |     | • Cont B (Postgres): Khóa    |     |   (RW) -> Merged View (/app) |\n  |   thấy mình là Virtual PID 1 |     |   1 CPU, 1GB RAM, 100MB/s IO |     | • Capabilities & Seccomp     |\n  +--------------+---------------+     +--------------+---------------+     +--------------+---------------+\n                 |                                    |                                    |\n                 +------------------------------------+------------------------------------+\n                                                      |\n                                                      v\n  +------------------------------------------------------------------------------------------------+\n  | [ĐẦU RA CHẶNG 2]: Bản chất Container không phải là một máy ảo thu nhỏ, mà là một tiến trình    |\n  | Linux bình thường bị che mắt bởi 6 Namespaces, khóa định mức bởi cgroups v2 và xếp tầng CoW!   |\n  +------------------------------------------------------------------------------------------------+\n====================================================================================================', "kind": "boxes"},
        '2.1': {"ascii": '====================================================================================================\n      GIẢI PHẪU HỌC TẦNG NHÂN (PHẦN 1): LĂNG KÍNH ẢO ẢNH LINUX NAMESPACES TRÊN HOST KERNEL\n====================================================================================================\n\n  +----------------------------------------------------------------------------------------------+\n  |                     TẦNG TIẾN TRÌNH CÔ LẬP (CONTAINER INSTANCES RUNTIME)                     |\n  |                                                                                              |\n  |  +-------------------------------------------+  +-----------------------------------------+  |\n  |  |   CONTAINER A (Web Frontend Instance)     |  |  CONTAINER B (Database Backend Instance)|  |\n  |  |  +-------------------------------------+  |  |  +-----------------------------------+  |  |\n  |  |  | [>] Tiến trình Nginx / order-api    |  |  |  | [>] Tiến trình PostgreSQL         |  |  |\n  |  |  |     (Host PID thật: 10423)          |  |  |  |     (Host PID thật: 10424)        |  |  |\n  |  |  +------------------+------------------+  |  |  +-----------------+-----------------+  |  |\n  |  |                     | Tạo góc nhìn ảo     |  |                    | Tạo góc nhìn ảo    |  |\n  |  |                     v                     |  |                    v                    |  |\n  |  |  +-------------------------------------+  |  |  +-----------------------------------+  |  |\n  |  |  | [!] NAMESPACES: LĂNG KÍNH ẢO ẢNH    |  |  |  | [!] NAMESPACES: LĂNG KÍNH ẢO ẢNH  |  |  |\n  |  |  |  +-------------------------------+  |  |  |  |  +-----------------------------+  |  |  |\n  |  |  |  | • PID Namespace               |  |  |  |  |  | • PID Namespace             |  |  |  |\n  |  |  |  |   (Ảo ảnh: Virtual PID = 1)   |  |  |  |  |  |   (Ảo ảnh: Virtual PID = 1) |  |  |  |\n  |  |  |  +---------------+---------------+  |  |  |  |  +--------------+--------------+  |  |  |\n  |  |  |                  v                  |  |  |  |                 v                 |  |  |\n  |  |  |  +-------------------------------+  |  |  |  |  +-----------------------------+  |  |  |\n  |  |  |  | • Network Namespace           |  |  |  |  |  | • Network Namespace         |  |  |  |\n  |  |  |  |   (IP riêng: 172.17.0.2)      |  |  |  |  |  |   (IP riêng: 172.17.0.3)    |  |  |  |\n  |  |  |  +---------------+---------------+  |  |  |  |  +--------------+--------------+  |  |  |\n  |  |  |                  v                  |  |  |  |                 v                 |  |  |\n  |  |  |  +-------------------------------+  |  |  |  |  +-----------------------------+  |  |  |\n  |  |  |  | • Mount Namespace             |  |  |  |  |  | • Mount Namespace           |  |  |  |\n  |  |  |  |   (Rootfs riêng: /app)        |  |  |  |  |  |   (Rootfs riêng: /pgdata)   |  |  |  |\n  |  |  |  +-------------------------------+  |  |  |  |  +-----------------------------+  |  |  |\n  |  |  +------------------+------------------+  |  |  +-----------------+-----------------+  |  |\n  |  +---------------------|---------------------+  +--------------------|--------------------+  |\n  +------------------------|---------------------------------------------|-----------------------+\n                           | 1. Ủy quyền cô lập                          | 3. Ủy quyền cô lập\n                           +----------------------+----------------------+\n                                                  |\n                                                  v\n  +----------------------------------------------------------------------------------------------+\n  |                       [LINUX KERNEL CORE SPACE - SHARED HOST KERNEL]                         |\n  |       Quản lý bảng ánh xạ thật: Host PID 10423 <-> Cont A (PID 1) | 10424 <-> Cont B (PID 1) |\n  |               Cung cấp Syscalls: clone(2) với cờ CLONE_NEW*, unshare(2), pivot_root(2)       |\n  +----------------------------------------------------------------------------------------------+\n====================================================================================================', "kind": "boxes"},
        '2.2': {"ascii": '====================================================================================================\n      GIẢI PHẪU HỌC TẦNG NHÂN (PHẦN 2): VÒNG KIM CÔ CGROUPS KHÓA CỨNG TÀI NGUYÊN VẬT LÝ\n====================================================================================================\n\n  +----------------------------------------------+  +----------------------------------------------+\n  |   CONTAINER A: Web Frontend (PID: 10423)     |  |   CONTAINER B: Database Backend (PID: 10424) |\n  |  +----------------------------------------+  |  |  +----------------------------------------+  |\n  |  | [!] cgroups v2: VÒNG KIM CÔ ĐỊNH MỨC   |  |  |  | [!] cgroups v2: VÒNG KIM CÔ ĐỊNH MỨC   |  |\n  |  |                                        |  |  |  |                                        |  |\n  |  |  +----------------------------------+  |  |  |  |  +----------------------------------+  |  |\n  |  |  | • CPU Quota (cpu.max / CFS)      |  |  |  |  |  | • CPU Quota (cpu.max / CFS)      |  |  |\n  |  |  |   [Khóa cứng: Tối đa 2 Cores]    |  |  |  |  |  |   [Khóa cứng: Tối đa 1 Core]     |  |  |\n  |  |  +----------------+-----------------+  |  |  |  |  +----------------+-----------------+  |  |\n  |  |                   |                    |  |  |  |                   |                    |  |\n  |  |                   v                    |  |  |  |                   v                    |  |\n  |  |  +----------------------------------+  |  |  |  |  +----------------------------------+  |  |\n  |  |  | • Memory Limit (memory.max)      |  |  |  |  |  | • Memory Limit (memory.max)      |  |  |\n  |  |  |   [Khóa cứng: Tối đa 512 MB]     |  |  |  |  |  |   [Khóa cứng: Tối đa 1 GB]       |  |  |\n  |  |  +----------------+-----------------+  |  |  |  |  +----------------+-----------------+  |  |\n  |  |                   |                    |  |  |  |                   |                    |  |\n  |  |                   v                    |  |  |  |                   v                    |  |\n  |  |  +----------------------------------+  |  |  |  |  +----------------------------------+  |  |\n  |  |  | • BlkIO (Block I/O)              |  |  |  |  |  | • BlkIO (Block I/O)              |  |  |\n  |  |  |   [Đọc/Ghi tối đa: 100 MB/s]     |  |  |  |  |  |   [Giới hạn IOPS đĩa vật lý]     |  |  |\n  |  |  +----------------------------------+  |  |  |  |  +----------------------------------+  |  |\n  |  +-------------------+--------------------+  |  |  +-------------------+--------------------+  |\n  +----------------------|-----------------------+  +----------------------|-----------------------+\n                         | 2. Kiểm soát tài nguyên                         | 4. Kiểm soát tài nguyên\n                         +-----------------------+-------------------------+\n                                                 |\n                                                 v\n  +------------------------------------------------------------------------------------------------+\n  |                       [LINUX KERNEL CORE SPACE - BỘ ĐẾM & CẦU DAO CGROUPS]                     |\n  |                     (Điều phối trực tiếp xuống phần cứng Bare Metal bên dưới)                  |\n  +----------------------------------------------+-------------------------------------------------+\n                                                 |\n                                                 v\n  +------------------------------------------------------------------------------------------------+\n  |        [MÁY CHỦ VẬT LÝ DÙNG CHUNG (BARE METAL): Physical CPU Cores, RAM Pool, Disk I/O]        |\n  +------------------------------------------------------------------------------------------------+\n====================================================================================================', "kind": "boxes"},
        '2.3': {"ascii": '====================================================================================================\n      GIẢI PHẪU HỌC TẦNG NHÂN (PHẦN 3 & 4): CỔNG SYSCALLS, OVERLAYFS & SECURITY HARDENING\n====================================================================================================\n\n                  +--------------------------------------------------------------+\n                  |               [LINUX SYSCALLS GATEWAY]                       |\n                  |  clone(2) với cờ CLONE_NEW*, unshare(2), pivot_root(2)       |\n                  +---------------+------------------------------+---------------+\n                                  |                              |\n         3. Ánh xạ không gian     |                              | 4. Nạp bộ lọc an ninh\n            mount (mnt namespace) |                              |    khi khởi tạo tiến trình\n                                  v                              v\n  +-----------------------------------------------+  +---------------------------------------------+\n  |   [3. OVERLAYFS (UNION FILE SYSTEM)]          |  |  [4. SECURITY HARDENING (GIA CỐ AN NINH)]   |\n  |                                               |  |                                             |\n  |  +-----------------------------------------+  |  |  +---------------------------------------+  |\n  |  | [+] Merged View                         |  |  |  | [+] Linux Capabilities                |  |\n  |  |     Thư mục hợp nhất tiến trình         |  |  |  |     Chia nhỏ quyền root thành các     |  |\n  |  |     app.py nhìn thấy (vd: /app)         |  |  |  |     mảnh nhỏ; tước bỏ đặc quyền       |  |\n  |  +--------------------+--------------------+  |  |  |     root dư thừa (Least Privilege)    |  |\n  |                       |                       |  |  +-------------------+-------------------+  |\n  |                       v                       |  |                      |                      |\n  |  +-----------------------------------------+  |  |                      v                      |\n  |  | [+] UpperDir (Thin Writable Layer)      |  |  |  +---------------------------------------+  |\n  |  |     Lớp mỏng ghi nhận mọi thay đổi      |  |  |  | [+] Seccomp (Secure Computing Mode)   |  |\n  |  |     tạm thời của riêng Container        |  |  |  |     Bộ lọc tường lửa chặn đứng các    |  |\n  |  +--------------------+--------------------+  |  |  |     System Calls nguy hiểm xuống      |  |\n  |                       |                       |  |  |     Kernel (kết hợp AppArmor/SELinux) |  |\n  |                       v                       |  |  +---------------------------------------+  |\n  |  +-----------------------------------------+  |  +---------------------------------------------+\n  |  | [+] LowerDir (Read-Only Image Layers)   |  |\n  |  |     Các tầng Image bất biến xếp chồng   |  |  [CÂY KẾ THỪA ĐỒ THỊ DAG CỦA LOWERDIR (SÁCH)]\n  |  |     dùng chung cho hàng chục Container  |  |   Container A (Base OS: Debian)\n  |  +-----------------------------------------+  |     ├── Container B (+ Ruby v2.1.10)\n  +-----------------------------------------------+     │     ├── Container D (+ Rails v4.2.6)\n                                                        │     └── Container E (+ Rails v3.2.x)\n                                                        └── Container C (+ Golang v1.6)\n====================================================================================================', "kind": "boxes"},
        '3.0': {"ascii": '====================================================================================================\n       CHẶNG 3 OVERVIEW: CHU TRÌNH BUILD-SHIP-RUN, PERSISTENT VOLUMES & ĐỘNG CƠ OCI RUNTIME\n====================================================================================================\n\n  [TRẠM 3.1: BUILD-SHIP-RUN & VOLUME]               [TRẠM 3.2: ĐỘNG CƠ OCI RUNTIME & PODMAN]\n  +-------------------------------------------+     +----------------------------------------------+\n  | • [1. BUILD]: Dockerfile -> OCI Image (RO)|     | • Chuỗi gọi chuẩn công nghiệp:               |\n  | • [2. SHIP] : Push/Pull qua OCI Registry  |     |   Docker CLI --[REST]--> dockerd --[gRPC]--> |\n  | • [3. RUN]  : Khởi chạy Container đồng bộ | --> |   containerd --> containerd-shim --> runc    |\n  | • [VOLUME]  : Tách dữ liệu PostgreSQL ra  |     | • runc gọi Kernel tạo Container rồi TỰ THOÁT |\n  |   Persistent Volume (/var/lib/docker/...) |     |   (Daemonless container do shim giữ stdio)   |\n  |   để xóa Container không mất Database!    |     | • Nhánh rẽ Podman (Daemonless & Rootless)    |\n  +---------------------+---------------------+     +----------------------+-----------------------+\n                        |                                                  |\n                        +------------------------+-------------------------+\n                                                 |\n                                                 v\n  +------------------------------------------------------------------------------------------------+\n  | [ĐẦU RA CHẶNG 3]: Tự động hóa hoàn toàn việc đóng gói ứng dụng và chuẩn hóa động cơ thực thi   |\n  | theo chuẩn mở OCI (containerd + runc), sẵn sàng ghép nối trực tiếp vào bộ điều phối cụm K8s!   |\n  +------------------------------------------------------------------------------------------------+\n====================================================================================================', "kind": "boxes"},
        '3.1': {"ascii": '====================================================================================================\n      TẦNG 1 WORKFLOW VĨ MÔ: CHU TRÌNH BUILD - SHIP - RUN & CƠ CHẾ LƯU TRỮ BỀN VỮNG (VOLUME)\n====================================================================================================\n\n  [GÓC TRÁI: CẤU TRÚC DỰ ÁN & DOCKERFILE (SLIDE)]     [GÓC PHẢI: LUỒNG VĨ MÔ BUILD - SHIP - RUN]\n  project/                                            . . . . . . . . . . . . . . . . . . . . . . .\n  |-- app.py                                          .  +-------------------------------------+  .\n  +-- Dockerfile                                      .  | [1] Dockerfile (Multi-stage Build)  |  .\n                                                      .  +------------------+------------------+  .\n  +-----------------------------------------------+   .                     |                     .\n  | # Use official Python image                   |   .                     v                     .\n  | FROM python:3.11-slim                         |   .        +-------------------------+        .\n  |                                               |   .        |     docker build        |        .\n  | # Set working directory                       |   .        +------------+------------+        .\n  | WORKDIR /app                                  |   .                     |                     .\n  |                                               |   .                     v                     .\n  | # Copy files into container                   |   .  +-------------------------------------+  .\n  | COPY app.py .                                 |   .  | [2] OCI Image (Read-Only Layers)    |  .\n  |                                               |   .  +------------------+------------------+  .\n  | # Run the app                                 |   . . . . . . . . . . . | . . . . . . . . . . .\n  | CMD ["python", "app.py"]                      |                         |==> [BUILD]\n  +-----------------------------------------------+                         |    (Nơi chứa công thức\n                                                                            |     & gói bất biến)\n                                                                            | docker push\n                                                                            v\n                                                      . . . . . . . . . . . . . . . . . . . . . . .\n                                                      .  +-------------------------------------+  .\n                                                      .  | [3] Registry (Docker Hub / Harbor)  |  .\n                                                      .  +------------------+------------------+  .\n                                                      . . . . . . . . . . . | . . . . . . . . . . .\n                                                                            |==> [SHIP]\n                                                                            | docker pull\n                                                                            v\n  [GIẢI PHẪU 3 CƠ CHẾ LƯU TRỮ DỮ LIỆU CONTAINER]      . . . . . . . . . . . . . . . . . . . . . . .\n  +-----------------------------------------------+   .  +-------------------------------------+  .\n  | 1. Writable Layer (UpperDir mặc định):        |   .  | [4] docker run (CLI tiếp nhận lệnh) |  .\n  |    [x] Tạm bợ (Ephemeral) -> Xóa container    |   .  +------------------+------------------+  .\n  |        là MẤT SẠCH dữ liệu! (Dùng cho temp)   |   .                     |                     .\n  | 2. Bind Mounts:                               |   .                     v                     .\n  |    [!] Ánh xạ trực tiếp file/folder từ Host   |   .  +-------------------------------------+  .\n  |        filesystem vào Container.              |   .  | [5] Container (Sự sống của Image:   |  .\n  | 3. Docker Volumes (/var/lib/docker/volumes):  |   .  |     Tiến trình + Writable Layer)    |  .\n  |    [+] Phân vùng do Docker quản lý, ĐỘC LẬP   |   .  +------------------+------------------+  .\n  |        với vòng đời Container -> Chuẩn mực    |   . . . . . . . . . . . ^ . . . . . . . . . . .\n  |        bắt buộc khi chạy Database Stateful!   |                         |==> [RUN]\n  +-----------------------------------------------+                         | Gắn kết lưu trữ\n                                                                            | Stateful (2 chiều)\n                                                                            v\n                                                         +-------------------------------------+\n                                                         | [+] Volume / Mount                  |\n                                                         |     (Lưu trữ bền vững ngoài vòng    |\n                                                         |      đời Container - Chống mất DB!) |\n                                                         +-------------------------------------+\n====================================================================================================', "kind": "boxes"},
        '3.2': {"ascii": '====================================================================================================\n      TẦNG 2 OCI RUNTIME ENGINE: CHUỖI TIẾN TRÌNH ĐIỀU PHỐI & NHÁNH RẼ DAEMONLESS (PODMAN)\n====================================================================================================\n\n  [NHÁNH 1: KIẾN TRÚC CLIENT-DAEMON CỦA DOCKER]         [NHÁNH 2: KIẾN TRÚC DAEMONLESS CỦA PODMAN]\n  +-------------------------------------------+         +------------------------------------------+\n  | [>] Docker CLI (Đóng gói REST Payload)    |         | [>] Podman CLI / Buildah / Skopeo        |\n  |     (/usr/bin/docker)                     |         |     (Không cần Daemon chạy ngầm,         |\n  +---------------------+---------------------+         |      chạy an toàn ở chế độ Rootless!)    |\n                        |                               +--------------------+---------------------+\n                        | 1. Unix Socket / REST API                          |\n                        |    (/var/run/docker.sock)                          | Mô hình thay thế:\n                        v                                                    | Bỏ qua hoàn toàn\n  +-------------------------------------------+                              | Daemon trung tâm\n  | [!] dockerd (Docker Daemon - Chạy quyền   |                              | (Fork/Exec trực tiếp)\n  |     Root, quản lý Network, Storage & API) |                              |\n  |     (/usr/bin/dockerd)                    |                              |\n  +---------------------+---------------------+                              |\n                        |                                                    |\n                        | 2. gRPC Call (CRUD API)                            |\n                        v                                                    |\n  +-------------------------------------------+                              |\n  | [+] containerd (High-Level Runtime CNCF:  |                              |\n  |     Quản lý vòng đời & Unpack OCI Bundle) |                              |\n  |     (/usr/bin/containerd)                 |                              |\n  +---------------------+---------------------+                              |\n                        |                                                    |\n                        | 3. Khởi tạo tiến trình con (Fork)                  |\n                        v                                                    |\n  +-------------------------------------------+                              |\n  | [+] containerd-shim (Tiến trình đệm:      |                              |\n  |     Giữ mở STDIN/STDOUT, báo cáo Exit     |                              |\n  |     Code, bảo vệ Container khi tắt Daemon)|                              |\n  |     (/usr/bin/containerd-shim-runc-v2)    |                              |\n  +---------------------+---------------------+                              |\n                        |                                                    |\n                        | 4. Kích hoạt nhị phân OCI                          |\n                        +----------------------------------------------------+\n                        |\n                        v\n  +------------------------------------------------------------------------------------------------+\n  | [+] runc (Low-Level OCI Runtime - /usr/bin/runc):                                              |\n  |     Bọc thư viện libcontainer -> Gọi Linux Syscalls (clone, unshare, pivot_root) cấu hình      |\n  |     Namespaces + cgroups + OverlayFS + Seccomp -> Khởi chạy Container rồi LẬP TỨC TỰ THOÁT!    |\n  +---------------------------------------------+--------------------------------------------------+\n                                                | (Sau khi runc thoát, shim làm cha của Container)\n                                                v\n  +------------------------------------------------------------------------------------------------+\n  |         [RUNNING CONTAINER INSTANCE: order-api (app.py) chạy cô lập trên Linux Kernel]         |\n  +------------------------------------------------------------------------------------------------+\n====================================================================================================', "kind": "boxes"},
        '4.0': {"ascii": '====================================================================================================\n      CHẶNG 4 OVERVIEW: ĐIỀU PHỐI PHÂN TÁN VỚI KUBERNETES (CRI, CONTROL PLANE & 3 POD REPLICAS)\n====================================================================================================\n\n  [TRẠM 4.1: CRI & DECLARATIVE]        [TRẠM 4.2: CONTROL PLANE & NODES]    [TRẠM 4.3: POD, SERVICE & HA]\n  +------------------------------+     +------------------------------+     +------------------------------+\n  | • K8s >= 1.25 loại bỏ hẳn    |     | • Control Plane: API Server, |     | • Giải phẫu nguyên tử Pod:   |\n  |   dockerd/dockershim, gọi    |     |   etcd (Raft), Controller    |     |   Chung net/ipc/uts (gọi qua |\n  |   thẳng containerd qua CRI   | --> |   Manager, kube-scheduler    | --> |   localhost), riêng cgroups  |\n  | • Hạ tầng bất biến (Immutable|     | • Worker Fleet: kubelet,     |     | • Chuỗi điều phối: Ingress   |\n  |   Infrastructure) & khai báo |     |   CRI Runtime & kube-proxy   |     |   -> Service (IPVS) ->       |\n  |   trạng thái đích bằng YAML  |     | • Luồng 9 bước từ YAML -> Pod|     |   Deployment -> 3 Replicas   |\n  +--------------+---------------+     +--------------+---------------+     +--------------+---------------+\n                 |                                    |                                    |\n                 +------------------------------------+------------------------------------+\n                                                      |\n                                                      v\n  +------------------------------------------------------------------------------------------------+\n  | [ĐẦU RA CHẶNG 4]: Dịch vụ order-api tiến hóa thành 3 Pod Replicas bất tử trải trên cụm máy     |\n  | chủ Worker Nodes, tự động cân bằng tải (IPVS), tự phục hồi (Self-healing) & nâng cấp 0-downtime|\n  +------------------------------------------------------------------------------------------------+\n====================================================================================================', "kind": "boxes"},
        '4.1': {"ascii": '====================================================================================================\n      BƯỚC NGOẶT KIẾN TRÚC K8S: LOẠI BỎ DOCKER DAEMON (CHUẨN CRI) & TRIẾT LÝ BẤT BIẾN / KHAI BÁO\n====================================================================================================\n\n  [A. PHẪU THUẬT ĐƯỜNG GỌI RUNTIME TRÊN WORKER NODE (K8S >= 1.25)]\n  +----------------------------------------------------------------------------------------------+\n  |  • Kiến trúc cũ (Qua trung gian nặng nề):                                                    |\n  |    [kubelet] --(dockershim)--> [dockerd (Nặng, dư thừa)] --(gRPC)--> [containerd] --> [runc] |\n  |                                                                                              |\n  |  • Kiến trúc chuẩn CRI hiện đại (Cắt bỏ hoàn toàn dockerd!):                                 |\n  |    [kubelet] ======(Chuẩn mở CRI qua gRPC)======> [containerd / CRI-O] --> [shim] --> [runc] |\n  |    => Vẫn chạy 100% các OCI Images do Docker build ra, nhưng nhẹ, nhanh và ổn định hơn!      |\n  +----------------------------------------------------------------------------------------------+\n\n  [B. ĐỐI CHIẾU NÂNG CẤP PHẦN MỀM: KHẢ BIẾN (MUTABLE) vs. BẤT BIẾN (IMMUTABLE INFRASTRUCTURE)]\n  +----------------------------------------------+  +--------------------------------------------+\n  | [x] CÁCH CŨ: SỬA SỐNG TRỰC TIẾP (MUTABLE)    |  | [+] CHUẨN K8S: THAY THẾ TOÀN BỘ (IMMUTABLE)|\n  |                                              |  |                                            |\n  |   1. Kỹ sư login (SSH/exec) vào Container v1 |  |   1. Build một OCI Image v2 mới hoàn toàn  |\n  |   2. Chạy lệnh tải code mới đè lên file cũ   |  |   2. Push Image v2 lên Container Registry  |\n  |   3. Kill server cũ, bật server mới tại chỗ  |  |   3. K8s xóa hẳn Container v1 cũ           |\n  |   => [!] Lệch cấu hình, không thể Rollback!  |  |   4. K8s khởi tạo Container v2 mới tinh    |\n  +----------------------------------------------+  +--------------------------------------------+\n\n  [C. RANH GIỚI PHÂN TÁCH TRÁCH NHIỆM ("NOT MY MONKEY, NOT MY CIRCUS" LINE - SÁCH K8S)]\n      Đội ngũ Phát triển Ứng dụng (App Ops / Devs)  |  Chỉ tương tác qua YAML (Pods, Services)\n  ==================================================+=============================================\n                                    [ KUBERNETES ORCHESTRATION API ]  <-- Hợp đồng SLA rõ ràng\n  ==================================================+=============================================\n      Đội ngũ Hạ tầng Cụm (Cluster Ops / SREs)      |  Quản lý Servers, Linux Kernel, Network, Disk\n====================================================================================================', "kind": "boxes"},
        '4.2': {"ascii": '====================================================================================================\n      THỜI KỲ 3: GIẢI PHẪU LUỒNG 9 BƯỚC TỪ KHAI BÁO YAML ĐẾN CỤM WORKER FLEET (EXCALIDRAW)\n====================================================================================================\n\n  [1. KHAI BÁO (DECLARATIVE SPEC)]\n  +---------------------------------------------------------------------------------------------+\n  |  +-------------------+  1. Soạn thảo  +-------------------+  2. Áp dụng  +---------------+  |\n  |  |  DevOps Engineer  | ------------> |   YAML Manifest   | ------------> | kubectl Client|  |\n  |  | (Khai báo hạ tầng)|               | (Replicas: 3, v2) |               | (Công cụ CLI) |  |\n  |  +-------------------+               +-------------------+               +-------+-------+  |\n  +----------------------------------------------------------------------------------|----------+\n                                                                                     |\n                                                                3. Gửi REST Payload  |\n                                                                                     v\n  [2. BỘ NÃO TRUNG TÂM (CONTROL PLANE)]                                              |\n  +----------------------------------------------------------------------------------|----------+\n  |                                                                                  v          |\n  |                                      +-------------------------------------------+          |\n  |                                      | [+] kube-apiserver (Cửa ngõ REST API duy nhất)       |\n  |                                      +---+---------------+---------------+-------+          |\n  |                                          |               |               |                  |\n  |                     4. Ghi nhận          |   5. Đối soát |   6. Lập lịch | 7. Lệnh gRPC     |\n  |                        trạng thái        |      liên tục |      chọn máy |    triển khai    |\n  |                        v                 v               v               |    xuống Nodes   |\n  |  +-----------------------+  +-----------------------+  +--------------+  |                  |\n  |  | [+] etcd              |  | [+] Controller Manager|  | [+] kube-    |  |                  |\n  |  | (Lưu Desired State)   |  | (Hòa giải Actual vs.  |  |   scheduler  |  |                  |\n  |  +-----------------------+  |  Desired State)       |  | (Chọn Node)  |  |                  |\n  |                             +-----------------------+  +--------------+  |                  |\n  +--------------------------------------------------------------------------|------------------+\n                                                                             |\n         +-------------------------------------------------------------------+\n         | (7. Lệnh gRPC triển khai gửi tới các Quản đốc kubelet)\n         v\n  [3. CỤM THỰC THI (WORKER FLEET - ĐỘI QUÂN CƠ BẮP)]\n  +----------------------------------------------------------------------------------------------+\n  |  +----------------------------------------------------------------------------------------+  |\n  |  | [WORKER NODE 01 - MÁY CHỦ CHÍNH]                                                       |  |\n  |  |  +------------------+  8. Ra lệnh CRI  +------------------+  9. Khởi chạy  +---------+ |  |\n  |  |  | kubelet 01       | ---------------> | CRI containerd   | -------------> | Pods    | |  |\n  |  |  | (Quản đốc Node)  |                  | (Runtime)        |                | 01 & 02 | |  |\n  |  |  +------------------+                  +------------------+                | (App)   | |  |\n  |  |                                        +------------------+  Cân bằng tải  |         | |  |\n  |  |                                        | kube-proxy 01    | -------------> |         | |  |\n  |  |                                        | (Định tuyến IPVS)|       IP       +---------+ |  |\n  |  |                                        +------------------+                            |  |\n  |  +----------------------------------------------------------------------------------------+  |\n  |                                                                                              |\n  |  +----------------------------------------------------------------------------------------+  |\n  |  | [WORKER NODE 02 - MÁY CHỦ DỰ PHÒNG HA (HIGH AVAILABILITY)]                             |  |\n  |  |  +------------------+  8. Ra lệnh CRI  +------------------+  9. Khởi chạy  +---------+ |  |\n  |  |  | kubelet 02       | ---------------> | CRI containerd   | -------------> | Pod 03  | |  |\n  |  |  | (Quản đốc Node)  |                  | (Runtime)        |                | (Dự     | |  |\n  |  |  +------------------+                  +------------------+                |  phòng  | |  |\n  |  |                                        +------------------+  Cân bằng tải  |  HA)    | |  |\n  |  |                                        | kube-proxy 02    | -------------> |         | |  |\n  |  |                                        | (Định tuyến IPVS)|       IP       +---------+ |  |\n  |  |                                        +------------------+                            |  |\n  |  +----------------------------------------------------------------------------------------+  |\n  +----------------------------------------------------------------------------------------------+\n====================================================================================================', "kind": "boxes"},
        '4.3': {"ascii": '====================================================================================================\n      GIẢI PHẪU HẠT NHÂN CỦA NGUYÊN TỬ POD & CHUỖI ĐIỀU PHỐI DEPLOYMENT - SERVICE - INGRESS\n====================================================================================================\n\n  [A. GIẢI PHẪU CƠ HỌC BÊN TRONG 1 POD (MULTI-CONTAINER SIDECAR PATTERN - SÁCH K8S CH.5)]\n  +----------------------------------------------------------------------------------------------+\n  |  ĐƠN VỊ NGUYÊN TỬ POD (Cùng lập lịch trên 1 Worker Node - Chia sẻ chung IP: 10.244.1.15)     |\n  |                                                                                              |\n  |  +----------------------------------------------------------------------------------------+  |\n  |  | [+] KHÔNG GIAN DÙNG CHUNG (SHARED LINUX NAMESPACES):                                   |  |\n  |  |     • Shared Network Namespace (Chung địa chỉ IP, chung không gian Port -> gọi nhau    |  |\n  |  |       trực tiếp qua localhost!)                                                        |  |\n  |  |     • Shared UTS Namespace (Chung Hostname) & Shared IPC Namespace (Chung hàng đợi IPC)|  |\n  |  |                                                                                        |  |\n  |  |   +----------------------------------------+  +------------------------------------+   |  |\n  |  |   | CONTAINER 1: Web Serving (order-api)   |  | CONTAINER 2: Sidecar (Git Sync)    |   |  |\n  |  |   | • Port: 8080/TCP                       |  | • Chuyên đồng bộ file từ Git về    |   |  |\n  |  |   | • Mount Namespace riêng (Rootfs riêng) |  | • Mount Namespace riêng            |   |  |\n  |  |   | • [!] cgroup RIÊNG: RAM tối đa 512 MB  |  | • [!] cgroup RIÊNG: RAM 128 MB     |   |  |\n  |  |   |   (Bảo vệ: Nếu Git Sync bị Memory Leak,|  |   (Nếu tràn RAM, chỉ mình Git Sync |   |  |\n  |  |   |    order-api vẫn sống khỏe 100%!)      |  |    bị OOM Kill và khởi động lại!)  |   |  |\n  |  |   +-------------------+--------------------+  +-----------------+------------------+   |  |\n  |  |                       |                                         |                      |  |\n  |  |                       | Đọc dữ liệu                             | Ghi dữ liệu đồng bộ  |  |\n  |  |                       v                                         v                      |  |\n  |  |                 +-----------------------------------------------------+                |  |\n  |  |                 |       [+] Shared Volume (Shared Filesystem)         |                |  |\n  |  |                 |           (Ví dụ: /exports gắn từ NFS / PVC)        |                |  |\n  |  |                 +-----------------------------------------------------+                |  |\n  |  +----------------------------------------------------------------------------------------+  |\n  +----------------------------------------------------------------------------------------------+\n\n  [B. CHUỖI VŨ KHÍ VẬN HÀNH PHÂN TÁN: TỪ INTERNET ĐẾN POD REPLICAS]\n  [Internet Traffic (HTTPS)]\n              |\n              v\n  +-----------------------+     +----------------------------------------------------------------+\n  | [1] Ingress           |     | [3] Deployment (Quản lý phát hành Rolling Update v1 -> v2)     |\n  |     (Định tuyến Lớp 7 |     |  +----------------------------------------------------------+  |\n  |      HTTP/HTTPS)      |     |  | [4] ReplicaSet (Đảm bảo luôn duy trì đúng 3 bản sao)     |  |\n  +-----------+-----------+     |  +-------------+----------------------------+---------------+  |\n              |                 +----------------|----------------------------|------------------+\n              v                                  | Quản lý qua                | Quản lý qua\n  +-----------------------+                      | Label Selectors            | Label Selectors\n  | [2] Service           |                      v                            v\n  |     (Cấp IP ảo cố định| ===(IPVS)==> [Pod Replica 01: 10.244.1.15]  [Pod Replica 02: .1.16]\n  |      ClusterIP & DNS) | ===(IPVS)==> [Pod Replica 03: 10.244.2.08]  (Kèm Liveness/Readiness)\n  +-----------------------+\n====================================================================================================', "kind": "boxes"},
    }
    for k, meta in diagrams.items():
        errs = verify_diagram(meta["ascii"], f"CNT-{k}", kind=meta["kind"])
        if errs:
            raise SystemExit(f"ASCII verification failed for CNT-{k} ({meta['kind']}): {errs}")
    return diagrams


def build_ingestion_ascii_diagrams() -> dict:
    from ascii_diagram import make_box as _raw_make_box, display_width
    def wrap_line(line: str, limit: int) -> list[str]:
        if display_width(line) <= limit:
            return [line]
        if any(c in line for c in "┐┘") or line.rstrip().endswith("│") or "[Tables]   [BI Dashboard]" in line:
            return [line]
        import re as _re
        m = _re.match(r"^(\s*(?:[├└]──\s+|\│\s+|\•\s+)?)", line)
        prefix = m.group(1) if m else ""
        cont_indent = prefix.replace("├──", "│  ").replace("└──", "   ").replace("•", " ")
        if len(cont_indent) > 12:
            cont_indent = "  "
        words = line.split(" ")
        out = []
        cur = ""
        for w in words:
            cand = w if not cur else cur + " " + w
            if display_width(cand) <= limit:
                cur = cand
            else:
                if cur:
                    out.append(cur)
                cur = cont_indent + w
        if cur:
            out.append(cur)
        return out

    def make_box(lines, inner_width=None, header=None, context="make_box"):
        if inner_width:
            wrapped = []
            for l in lines:
                wrapped.extend(wrap_line(l, inner_width))
            lines = wrapped
        req_w = max((display_width(l) for l in lines), default=0)
        w = max(inner_width or 0, req_w)
        return _raw_make_box(lines, inner_width=w, header=header, context=context)

    def banner(title: str, subtitle: str = "", width: int = 136) -> list[str]:
        bar = "=" * width
        out = [bar, pad_center(title, width).rstrip()]
        if subtitle:
            out.append(pad_center(subtitle, width).rstrip())
        out.append(bar)
        return out

    def v_arrow(label: str = "", width: int = 136) -> list[str]:
        mid = width // 2
        if label:
            lbl = f"│  {label}"
            start = min(mid, max(2, width - display_width(lbl)))
            return [
                (" " * mid) + "│",
                (" " * start) + lbl,
                (" " * mid) + "▼",
            ]
        return [
            (" " * mid) + "│",
            (" " * mid) + "▼",
        ]
    W = 136
    INNER_FULL = W - 4   # 136
    INNER_HALF = 62      # box width = 68 -> 68 + 4 + 68 = 140
    INNER_THIRD = 38     # box width = 44 -> 44 + 4 + 44 + 4 + 44 = 140

    diagrams = {}

    # -------------------------------------------------------------------------
    # 0.1: Mental Map 5 Chặng — Cắt lớp Kiến trúc Toàn khóa D01
    # -------------------------------------------------------------------------
    s01_c1 = make_box([
        "[CHẶNG 1: SOURCE SYSTEMS & STORAGE LAYOUTS (TRẠM 1.1 -> 1.3)]",
        "├── Nguồn phát sinh : PostgreSQL OLTP (Order #8888, 450.000đ)",
        "├── Ràng buộc vật lý: Định luật GIGO, khóa dòng & quá tải CPU",
        "├── Phân loại & Mẫu : Structured/Semi/Unstructured | Push/Pull/Poll",
        "└── Bố cục lưu trữ  : Row (CSV) vs Column (ORC) vs Hybrid (Parquet)",
    ], inner_width=INNER_HALF)
    s01_c2 = make_box([
        "[CHẶNG 2: BA THẾ HỆ CHANGE DATA CAPTURE (TRẠM 2.1 -> 2.4)]",
        "├── Thế hệ 1 (Polling): Quét cột updated_at -> Mù lệnh Hard DELETE",
        "├── Thế hệ 2 (Trigger): Ghi đồng bộ shadow_table -> Nhân đôi I/O",
        "├── Thế hệ 3 (Log CDC): Đọc tuần tự tệp nhị phân pg_wal / binlog",
        "└── Kết quả cho #8888 : Bắt sự kiện tại LSN=0/16B3748 với <2% CPU",
    ], inner_width=INNER_HALF)
    row_01_top = join_horizontal([s01_c1, s01_c2], ["    "], {3: [" ──►"]})

    s01_c3 = make_box([
        "[CHẶNG 3: HỆ SINH THÁI & KIẾN TRÚC APACHE KAFKA (TRẠM 3.1 -> 3.4)]",
        "├── Phá vỡ mạng nhện điểm-điểm O(N x M) bằng Event Backbone O(N+M)",
        "├── Điều phối cụm : Từ Apache ZooKeeper sang KRaft Consensus (4.0)",
        "├── Hệ sinh thái  : Kafka Connect, Schema Registry, MirrorMaker 2",
        "└── Vật lý & Độ trễ: Định cỡ Partition, Zero-Copy sendfile(), Lag",
    ], inner_width=INNER_HALF)
    s01_c4 = make_box([
        "[CHẶNG 4: CƠ HỌC VẬN HÀNH & ĐỘ TIN CẬY KAFKA (TRẠM 4.1 -> 4.5)]",
        "├── Producer : Băm khóa murmur2(user_id) % P & RecordAccumulator",
        "├── Consumer : Quy tắc 1 Partition - 1 Consumer/Group & Rebalance",
        "├── Chịu lỗi : Leader/Follower Replicas, Tập hợp ISR & High Watermark",
        "└── Cam kết  : At-most / At-least / Exactly-Once (EOS) & Compaction",
    ], inner_width=INNER_HALF)
    row_01_mid = join_horizontal([s01_c3, s01_c4], ["    "], {3: [" ──►"]})

    s01_c5 = make_box([
        "[CHẶNG 5: ĐƯỜNG ỐNG DEBEZIUM CDC THỜI GIAN THỰC & VẬN HÀNH THỰC CHIẾN (TRẠM 5.1 -> 5.3)]",
        "├── [Lớp 1 - Capture] : Chuyển tiếp không khe hở Initial Consistent Snapshot (op='r') -> Streaming pgoutput WAL (op='c/u/d')",
        "├── [Lớp 2 - Routing] : Kafka Connect Distributed Workers + Schema Registry (Avro/Protobuf) + Single Message Transforms (SMT)",
        "├── [Lớp 3 - Sinks]   : Cấp dữ liệu đồng thời cho Data Lakehouse (D02 Bronze), Fraud Detection (<50ms), Redis Cache, Elastic",
        "└── [Lớp 4 - Defense] : Chống nổ đĩa WAL Bloat (Heartbeat/max_slot_wal_keep_size), Dead Letter Queue (DLQ) & Outbox Pattern",
    ], inner_width=INNER_FULL)

    diagrams["0.1"] = {
        "ascii": "\n".join(
            banner("BẢN ĐỒ TƯ DUY TOÀN KHÓA D01: HÀNH TRÌNH SỰ KIỆN ORDER #8888 QUA TẦNG INGESTION",
                   "(Từ Nhật ký Giao dịch PostgreSQL pg_wal [LSN=0/16B3748] -> Debezium CDC -> Cụm Apache Kafka -> Data Lakehouse)")
            + [""]
            + row_01_top
            + v_arrow("Bước chuyển 1: Đóng gói biến động từ tệp WAL thành dòng sự kiện phân tán (Event Stream)")
            + row_01_mid
            + v_arrow("Bước chuyển 2: Tự động hóa kết nối Đa Đích (Multi-Sink) & Phòng vệ Sự cố Sản xuất")
            + s01_c5
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 1.1: Cắt lớp 5 Tầng Kiến trúc Dữ liệu, Data Governance & Nút thắt GIGO
    # -------------------------------------------------------------------------
    s11_p1 = make_box([
        "[TẦNG 1: DATA SOURCES]",
        "• PostgreSQL OLTP (#8888)",
        "• REST APIs / Webhooks",
        "• CSV/JSON Files, Raw Logs",
        "• IoT Sensors / Third-party",
        "[!] Nhạy cảm CPU & I/O Lock!",
    ], inner_width=INNER_THIRD)
    s11_p2 = make_box([
        "[TẦNG 2: INGESTION & STAGING]",
        "• Hút dữ liệu thô (Batch/CDC)",
        "• Cách ly tải khỏi DB nguồn",
        "• Staging Area: Kiểm tra Schema",
        "  Validation & lọc rác GIGO",
        "[+] Chốt chặn biên giới #1",
    ], inner_width=INNER_THIRD)
    s11_p3 = make_box([
        "[TẦNG 3-5: WAREHOUSE -> MARTS]",
        "• Warehouse / Lakehouse (SSoT):",
        "  Raw + Summary + Metadata",
        "• Data Marts: Sales, Inventory,",
        "  Purchasing (Tối ưu theo miền)",
        "• Users: BI, Reporting, Mining",
    ], inner_width=INNER_THIRD)
    row_11_arch = join_horizontal([s11_p1, s11_p2, s11_p3], ["    ", "    "], {3: [" ──►", " ──►"]})

    s11_gov = make_box([
        "[LỚP NỀN CẮT NGANG TOÀN HỆ THỐNG: DATA GOVERNANCE LAYER (5 TRỤ CỘT QUẢN TRỊ - SLIDE 4)]",
        "├── [1] Data Quality        : Kiểm định tính chính xác (Accuracy), đầy đủ (Completeness) và nhất quán (Consistency)",
        "├── [2] Data Security       : Mã hóa kênh truyền (TLS/mTLS), ẩn danh hóa thông tin định danh cá nhân (PII Masking/Hashing)",
        "├── [3] Data Lineage        : Truy vết toàn bộ phả hệ nguồn gốc và biến đổi của Order #8888 từ bảng OLTP đến báo cáo BI",
        "├── [4] Metadata Management : Quản lý danh mục bảng, định nghĩa nghiệp vụ và hợp đồng lược đồ (Schema Contracts)",
        "└── [5] Access Control      : Phân quyền truy cập theo vai trò (RBAC) và nguyên tắc đặc quyền tối thiểu (PoLP)",
    ], inner_width=INNER_FULL)

    s11_gigo = make_box([
        "[CẮT LỚP RỦI RO TẠI NGUỒN: ĐỊNH LUẬT GIGO, QUÁ TẢI TÀI NGUỒN & TRÔI DẠT LƯỢC ĐỒ (SLIDE 7 + CHƯƠNG 7 JOE REIS)]",
        "• [x] GIGO Principle (Garbage In = Garbage Out): Dữ liệu nguồn bị khuyết (Null), trùng lặp hoặc sai múi giờ -> Phá hỏng toàn bộ ML/BI",
        "• [x] Resource Contention (Tranh chấp tài nguyên): Chạy SELECT quét bảng lớn trên DB nguồn làm vọt 100% CPU, treo giỏ hàng của khách",
        "• [!] Upstream Schema Drift (Trôi lược đồ): Đội Backend chạy ALTER TABLE đổi kiểu/xóa cột -> Cần Data Contract + Staging Quarantine",
    ], inner_width=INNER_FULL)

    diagrams["1.1"] = {
        "ascii": "\n".join(
            banner("CẮT LỚP KIẾN TRÚC 5 TẦNG DỮ LIỆU, DATA GOVERNANCE & ĐỊNH LUẬT GIGO (SLIDE 4-7)")
            + [""]
            + row_11_arch
            + v_arrow("Lớp quản trị Data Governance áp dụng xuyên suốt mọi tầng từ Source đến Users")
            + s11_gov
            + [""]
            + s11_gigo
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 1.2: Tam giác Cấu trúc Dữ liệu (Structured/Semi/Unstructured) & Push-Pull-Poll
    # -------------------------------------------------------------------------
    s12_t1 = make_box([
        "[A. STRUCTURED DATA (SLIDE 10)]",
        "• Bố cục bảng Hàng & Cột cố định",
        "  (PostgreSQL, MySQL, Oracle)",
        "• Kiểm tra Schema-on-Write",
        "• [+] Dễ dàng truy vấn SQL tức thì",
        "• [x] Kém linh hoạt khi đổi cấu trúc",
    ], inner_width=INNER_THIRD)
    s12_t2 = make_box([
        "[B. SEMI-STRUCTURED DATA]",
        "• Tổ chức phân cấp Key-Value/Tag",
        "  (JSON, XML, Avro, Log Events)",
        "• Kèm Metadata tự mô tả trong tệp",
        "• [+] Linh hoạt mở rộng trường mới",
        "• [!] Cần bước giải mã (Parsing)",
    ], inner_width=INNER_THIRD)
    s12_t3 = make_box([
        "[C. UNSTRUCTURED DATA]",
        "• Không có lược đồ định sẵn",
        "  (Ảnh, Video, Audio, PDF, Text)",
        "• Lưu trữ dạng File/Object (S3)",
        "• [+] Chiếm >80% dữ liệu doanh nghiệp",
        "• [x] Bắt buộc bóc tách (OCR/Vector)",
    ], inner_width=INNER_THIRD)
    row_12_types = join_horizontal([s12_t1, s12_t2, s12_t3], ["    ", "    "])

    s12_m1 = make_box([
        "[CƠ HỌC MẪU PUSH vs. PULL vs. POLL (CHƯƠNG 7 JOE REIS)]",
        "├── [1] PUSH : [Source App] ──(HTTP POST / SDK)──► [Collector]",
        "│       • Độ trễ mili-giây; rủi ro làm ngập đích (Cần Queue đệm)",
        "├── [2] PULL : [Source S3/FTP] ◄──(GET / Copy)──── [Ingestion Worker]",
        "│       • Đích chủ động nhịp độ đọc, không cần mở cổng Firewall nguồn",
        "└── [3] POLL : [Source DB] ◄──(SELECT định kỳ)──── [Scheduler Cron]",
        "        • Dò tìm thay đổi theo chu kỳ; quét rỗng gây lãng phí I/O",
    ], inner_width=INNER_HALF)
    s12_m2 = make_box([
        "[CƠ HỌC FILE INGESTION: BATCH vs. MICRO-BATCH (SLIDE 9)]",
        "├── [A] Scheduled Batch Ingestion (Theo lô hàng giờ / hàng ngày):",
        "│       • Hệ thống nguồn gom dữ liệu xuất thành tệp lớn (CSV/Parquet)",
        "│       • Job định kỳ đọc toàn bộ tệp nạp vào Data Lake / Warehouse",
        "└── [B] Micro-Batching (Lô nhỏ tần suất cao - Mỗi 1-5 phút):",
        "        • Chia thành các tệp nhỏ xử lý liên tục để giảm độ trễ",
        "        • [!] Cạm bẫy: Dễ gây bệnh 'Small Files Problem' trên S3/HDFS!",
    ], inner_width=INNER_HALF)
    row_12_modes = join_horizontal([s12_m1, s12_m2], ["    "])

    diagrams["1.2"] = {
        "ascii": "\n".join(
            banner("BA CẤP ĐỘ CẤU TRÚC DỮ LIỆU (SLIDE 9-10) & CƠ HỌC THU THẬP PUSH - PULL - POLL")
            + [""]
            + row_12_types
            + v_arrow("Ánh xạ sang chiến lược vận chuyển dữ liệu (Push / Pull / Poll) và nhịp độ xử lý (Batch / Micro-batch)")
            + row_12_modes
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 1.3: OLTP vs OLAP, Bố cục Lưu trữ (Row / Column / Hybrid), EtLT & Logs
    # -------------------------------------------------------------------------
    s13_oltp = make_box([
        "[LUỒNG HỆ THỐNG GIAO DỊCH: OLTP (SLIDE 15 & 18)]",
        "  [User/App] ──► [API Layer] ──► [OLTP DB (Orders/Users)]",
        "                                         │",
        "                                  [Transaction WAL]",
        "                                         │",
        "                                         ▼",
        "                                [CDC -> Kafka Layer]",
        "• Mục đích : Xử lý giao dịch thời gian thực (Đặt hàng #8888)",
        "• Thao tác : INSERT, UPDATE, DELETE (Độ trễ: Milliseconds)",
    ], inner_width=INNER_HALF)
    s13_olap = make_box([
        "[LUỒNG HỆ THỐNG PHÂN TÍCH: OLAP (SLIDE 16 & 18)]",
        "  [Source/Kafka] ──► [ETL/EtLT] ──► [Data Warehouse]",
        "                                          │",
        "                            ┌─────────────┼─────────────┐",
        "                            ▼             ▼             ▼",
        "                        [Tables]   [BI Dashboard]  [ML Models]",
        "• Mục đích : Phân tích dữ liệu lịch sử quy mô lớn (Insights)",
        "• Thao tác : SELECT tổng hợp phức tạp (Seconds - Hours)",
    ], inner_width=INNER_HALF)
    row_13_sys = join_horizontal([s13_oltp, s13_olap], ["    "], {3: [" ──►"]})

    s13_layouts = make_box([
        "[CẮT LỚP BỐ CỤC BYTE TRÊN ĐĨA: ROW-BASED vs. COLUMN-BASED vs. HYBRID ROW-GROUP (SLIDE 17)]",
        "├── [1] ROW-BASED (CSV, Postgres Heap)  : [a | 1 | 2020-01] ──► [b | 2 | 2020-02] ──► [c | 3 | 2020-03]",
        "│       └── Lưu liền kề từng dòng; tối ưu cho OLTP & mệnh đề WHERE (Predicate), nhưng phải đọc thừa toàn bộ cột khi tính tổng",
        "├── [2] COLUMN-BASED (ORC)              : [a | b | c (String)] ──► [1 | 2 | 3 (Int)] ──► [2020-01 | 2020-02 | 2020-03 (Date)]",
        "│       └── Lưu liền kề từng cột; tối ưu cho OLAP & mệnh đề SELECT (Projection), nén cực tốt nhưng tái tạo 1 dòng rất tốn kém",
        "└── [3] HYBRID ROW-GROUP (Parquet)      : Cắt ngang thành từng lô hàng (Row Group Size = 2), bên trong mỗi lô lưu theo cột:",
        "        └── Row Group 1: [a | b] [1 | 2] [2020-01 | 2020-02]   ||   Row Group 2 (Final): [c] [3] [2020-03]",
        "        └── [+] Kết hợp hoàn hảo: Vừa lọc bỏ cả cụm hàng qua Min/Max Statistics, vừa chỉ đọc đúng các cột được SELECT!",
    ], inner_width=INNER_FULL)

    s13_logs = make_box([
        "[THU THẬP NHẬT KÝ HỆ THỐNG (LOGS - SLIDE 19) & MÔ HÌNH BIẾN ĐỔI TRÊN ĐƯỜNG BAY EtLT (CHƯƠNG 3 DENSMORE)]",
        "• 3 Nguồn phát sinh Logs : [Docker Containers] + [Physical/Cloud Servers] + [IoT Devices & Gateways]",
        "• 6 Phân loại Logs       : System Logs | Application Logs | Error/Debug Logs | Audit Logs | Security Logs | Network Logs",
        "• Tiến hóa ETL/ELT/EtLT  : Extract ──► [t: Light Transform (Ẩn PII, Chuẩn hóa Múi giờ, Khử trùng)] ──► Load ──► Transform (DBT/Spark)",
    ], inner_width=INNER_FULL)

    diagrams["1.3"] = {
        "ascii": "\n".join(
            banner("GIẢI PHẪU OLTP vs. OLAP, BỐ CỤC ROW / COLUMN / HYBRID PARQUET & LOGS (SLIDE 15-19)")
            + [""]
            + row_13_sys
            + v_arrow("Sự khác biệt truy cập (Giao dịch theo dòng vs. Tổng hợp theo cột) quyết định cấu trúc lưu trữ vật lý")
            + s13_layouts
            + [""]
            + s13_logs
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 2.1: Toàn cảnh 3 Thế hệ CDC — Cắt lớp vị trí can thiệp trong DBMS
    # -------------------------------------------------------------------------
    s21_top = make_box([
        "[CẮT LỚP NỘI TẠNG HỆ QUẢN TRỊ CƠ SỞ DỮ LIỆU NGUỒN (POSTGRESQL / MYSQL) & 3 ĐIỂM ĐẶT ĐẦU DÒ CDC (SLIDE 11)]",
        "  [Ứng dụng Giao dịch] ──(INSERT / UPDATE / DELETE Order #8888)──► [1. SQL Query Parser & Executor]",
        "                                                                          │                     ▲",
        "                                                                          ▼                     └── (Điểm dò #1: TIMESTAMP POLLING",
        "                                                                   [2. Trigger Engine] ───────────►  Quét SELECT định kỳ gây tốn CPU)",
        "                                                                     │             │",
        "                                       (Ghi bảng chính)              │             └──► (Điểm dò #2: TRIGGER-BASED CDC",
        "                                             ▼                       ▼                  Ghi đồng bộ vào Shadow Table -> Chậm x2!)",
        "                                    [3. Heap Pages / B-Tree]   [4. Transaction Log (WAL / binlog)]",
        "                                                                          │",
        "                                                                          └──► (Điểm dò #3: LOG-BASED CDC / DEBEZIUM",
        "                                                                               Đọc luồng byte bất đồng bộ -> 0% tải SQL!)",
    ], inner_width=INNER_FULL)

    s21_g1 = make_box([
        "[1. TIMESTAMP-BASED POLLING]",
        "• Truy vấn: WHERE last_modified > T",
        "• [+] Dễ cài đặt bằng SQL thuần",
        "• [x] Mù lệnh xóa cứng (Hard DELETE)",
        "• [x] Gây tải quét bảng lên DB nguồn",
    ], inner_width=INNER_THIRD)
    s21_g2 = make_box([
        "[2. TRIGGER-BASED CDC]",
        "• Thực thi Trigger sau INSERT/UPD/DEL",
        "• [+] Bắt đủ mọi thao tác kể cả DELETE",
        "• [x] Ghi thêm vào audit_log làm tăng",
        "  gấp đôi độ trễ giao dịch chính!",
    ], inner_width=INNER_THIRD)
    s21_g3 = make_box([
        "[3. LOG-BASED CDC (CHUẨN HIỆN ĐẠI)]",
        "• Đọc trực tiếp từ WAL / binlog",
        "• [+] Không chạm vào bảng, 0% tải SQL",
        "• [+] Không cần sửa Schema bảng gốc",
        "• [!] Cần bộ giải mã nhị phân (Debezium)",
    ], inner_width=INNER_THIRD)
    row_21 = join_horizontal([s21_g1, s21_g2, s21_g3], ["    ", "    "], {2: [" ──►", " ──►"]})

    diagrams["2.1"] = {
        "ascii": "\n".join(
            banner("CẮT LỚP NỘI TẠNG DATABASE & BA PHƯƠNG PHÁP CHANGE DATA CAPTURE (SLIDE 11)")
            + [""]
            + s21_top
            + v_arrow("So sánh 3 phương pháp thu thập biến động dữ liệu đổ về Elasticsearch, Redis và Snowflake/Lakehouse")
            + row_21
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 2.2: Giải phẫu Timestamp-Based Polling CDC & 2 Lỗ hổng Cơ học
    # -------------------------------------------------------------------------
    s22_tbl = make_box([
        "[CẤU TRÚC BẢNG NGUỒN TRONG TIMESTAMP-BASED CDC: BẮT BUỘC THÊM CỘT last_modified & is_deleted (SLIDE 12)]",
        "┌─────────────┬──────────┬───────────────┬───────────────┬────────────────────────────┬──────────────────────────┐",
        "│ is_deleted  │ ID       │ First Name    │ Last Name     │ Email                      │ Last Modified (Watermark)│",
        "├─────────────┼──────────┼───────────────┼───────────────┼────────────────────────────┼──────────────────────────┤",
        "│ false       │ 1122     │ Michael       │ Jackson       │ Michael1122@gmail.com      │ 2022-10-31-T12:11:07     │",
        "│ true        │ 1122     │ George        │ Clooney       │ George.Clooney@gmail.com   │ 2023-10-13-T02:17:08     │",
        "└─────────────┴──────────┴───────────────┴───────────────┴────────────────────────────┴──────────────────────────┘",
    ], inner_width=INNER_FULL)

    s22_f1 = make_box([
        "[LỖ HỔNG 1: MÙ XÓA CỨNG (HARD DELETE BLINDNESS)]",
        "• Khi chạy lệnh vật lý: DELETE FROM users WHERE id = 1122;",
        "• Bản ghi bị xóa khỏi B-Tree & đánh dấu Dead Tuple trên trang đĩa.",
        "• Khi Job Polling chạy: SELECT * FROM users WHERE last_modified > T",
        "  ──► Không tìm thấy dòng 1122 (Vì dòng đó đã biến mất!).",
        "• [x] Hậu quả: Bắt buộc cấm lệnh DELETE vật lý, phải sửa toàn bộ",
        "  code ứng dụng sang Xóa mềm (UPDATE SET is_deleted = true).",
    ], inner_width=INNER_HALF)
    s22_f2 = make_box([
        "[LỖ HỔNG 2: TRANH CHẤP MỐC THỜI GIAN (WATERMARK RACE)]",
        "• T1 (12:00:01): Giao dịch A bắt đầu, gán last_modified = 12:00:01",
        "• T2 (12:00:03): Giao dịch B bắt đầu & COMMIT ngay (12:00:03)",
        "• T3 (12:00:04): Job Polling quét, nâng mốc Watermark = 12:00:03",
        "• T4 (12:00:05): Giao dịch A hoàn tất kiểm tra và COMMIT xuống đĩa!",
        "• [x] Hậu quả: Chu kỳ quét kế tiếp tìm last_modified > 12:00:03",
        "  ──► Bỏ sót vĩnh viễn Giao dịch A (do 12:00:01 < 12:00:03)!",
    ], inner_width=INNER_HALF)
    row_22 = join_horizontal([s22_f1, s22_f2], ["    "])

    diagrams["2.2"] = {
        "ascii": "\n".join(
            banner("GIẢI PHẪU TIMESTAMP-BASED POLLING CDC: SOFT DELETE & LỖ HỔNG WATERMARK (SLIDE 12)")
            + [""]
            + s22_tbl
            + v_arrow("Hai điểm mù vật lý khiến Timestamp Polling không thể dùng cho hệ thống tài chính/đơn hàng khắt khe")
            + row_22
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 2.3: Giải phẫu Trigger-Based CDC: Shadow Table & Nhân đôi I/O Giao dịch
    # -------------------------------------------------------------------------
    s23_flow = make_box([
        "[CẮT LỚP LUỒNG THỰC THI ĐỒNG BỘ CỦA TRIGGER-BASED CDC TRÊN MAIN SOURCE DATABASE (SLIDE 13)]",
        "  [Khách hàng bấm Thanh toán #8888] ──► BEGIN TRANSACTION;",
        "                                          ├── [Bước 1] Ghi vào Bảng Chính (Main Table: orders)",
        "                                          │            │",
        "                                          │            ▼ (Kích hoạt Trigger: AFTER INSERT OR UPDATE OR DELETE)",
        "                                          ├── [Bước 2] Ghi đồng bộ vào Bảng Bóng (Shadow Table / audit_log):",
        "                                          │            ┌────┬────────┬────────┬───────────┬───────────┐",
        "                                          │            │ ID │ Name   │ Amount │ Timestamp │ Operation │",
        "                                          │            ├────┼────────┼────────┼───────────┼───────────┤",
        "                                          │            │ 1  │ Vinnie │ 101    │ 12:10am   │ Insert    │",
        "                                          │            │ 2  │ Vinnie │ 127    │ 12:15am   │ Update    │",
        "                                          │            │ 3  │ Vinnie │ 142    │ 12:17am   │ Delete    │",
        "                                          │            └────┴────────┴────────┴───────────┴───────────┘",
        "                                          └── [Bước 3] COMMIT; (Chỉ thành công khi CẢ Bảng Chính và Bảng Bóng ghi xong!)",
    ], inner_width=INNER_FULL)

    s23_pros = make_box([
        "[ƯU ĐIỂM CỦA TRIGGER-BASED CDC]",
        "• [+] Bắt được toàn bộ 3 loại biến động: INSERT, UPDATE",
        "  và cả lệnh xóa vật lý DELETE (nhờ OLD.* trong Trigger).",
        "• [+] Được hỗ trợ sẵn trên hầu hết mọi RDBMS truyền thống.",
    ], inner_width=INNER_HALF)
    s23_cons = make_box([
        "[NHƯỢC ĐIỂM CHÍ MẠNG TRÊN MÔI TRƯỜNG PRODUCTION]",
        "• [x] Nhân đôi tải ghi (Write Amplification) ngay trên luồng",
        "  giao dịch của khách hàng -> Làm chậm trực tiếp API bán hàng!",
        "• [x] Cực kỳ khó bảo trì và gỡ lỗi khi có Cascading Triggers.",
    ], inner_width=INNER_HALF)
    row_23 = join_horizontal([s23_pros, s23_cons], ["    "])

    diagrams["2.3"] = {
        "ascii": "\n".join(
            banner("GIẢI PHẪU TRIGGER-BASED CDC: BẢNG BÓNG SHADOW TABLE & WRITE AMPLIFICATION (SLIDE 13)")
            + [""]
            + s23_flow
            + [""]
            + row_23
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 2.4: Giải phẫu Log-Based CDC: Đọc Bất đồng bộ từ Transaction Log
    # -------------------------------------------------------------------------
    s24_arch = make_box([
        "[KIẾN TRÚC TÁCH RỜI ĐỌC - GHI CỦA LOG-BASED CHANGE DATA CAPTURE (SLIDE 14)]",
        "",
        "  [Inserts] ──┐      ┌──────────────────┐     (Ghi tuần tự)     ┌─────────────────┐     (Đọc luồng byte)    ┌────────────────┐",
        "  [Updates] ──┼─────►│  Source Database │ ────────────────────► │ Transaction Log │ ──────────────────────► │   CDC Engine   │",
        "  [Deletes] ──┘      │ (PostgreSQL/MySQL│                       │  00101110 (WAL/ │  (Không chạm vào bảng,  │  (Debezium /   │",
        "                     │  Không Trigger!) │                       │  01100100 binlog│   không sửa Schema!)    │  Kafka Connect)│",
        "                     └──────────────────┘                       └─────────────────┘                         └───────┬────────┘",
        "                                                                                                                    │",
        "                                                                                                                    ▼",
        "                                                                                                        ┌────────────────────────┐",
        "                                                                                                        │ Store to Change Stream │",
        "                                                                                                        │ (Kafka Topic / Target) │",
        "                                                                                                        └────────────────────────┘",
    ], inner_width=INNER_FULL)

    s24_left = make_box([
        "[TẠI SAO LOG-BASED CDC LÀ TIÊU CHUẨN VÀNG?]",
        "• [+] Tác động tối thiểu (Minimal Impact): Chỉ đọc tuần tự",
        "  từ tệp Transaction Log có sẵn, không viết thêm bất cứ gì",
        "  vào Database nguồn -> 0% tranh chấp khóa trên bảng chính!",
        "• [+] Không xâm phạm Schema: Bắt đủ INSERT/UPDATE/DELETE mà",
        "  không cần thêm cột last_modified hay cờ is_deleted.",
    ], inner_width=INNER_HALF)
    s24_right = make_box([
        "[HAI THÁCH THỨC KỸ THUẬT CẦN VƯỢT QUA (SLIDE 14)]",
        "• [!] Định dạng nhị phân độc quyền theo từng hãng:",
        "  PostgreSQL dùng WAL (pgoutput LSN), MySQL dùng binlog (ROW),",
        "  Oracle dùng Redo Log -> Không có trình đọc chung đơn giản.",
        "• [!] Xử lý giao dịch bị hủy (Rolled-back Transactions):",
        "  CDC Engine phải đợi cờ COMMIT trong log trước khi phát sự kiện.",
    ], inner_width=INNER_HALF)
    row_24 = join_horizontal([s24_left, s24_right], ["    "])

    diagrams["2.4"] = {
        "ascii": "\n".join(
            banner("GIẢI PHẪU LOG-BASED CDC: ĐỌC TUẦN TỰ TRANSACTION LOG VỚI 0% TẢI BẢNG NGUỒN (SLIDE 14)")
            + [""]
            + s24_arch
            + [""]
            + row_24
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 3.1: Từ Mạng nhện O(N x M) đến Kiến trúc Cụm Apache Kafka (Slide 21-23)
    # -------------------------------------------------------------------------
    s31_spaghetti = make_box([
        "[TRƯỚC KAFKA: NỖI ĐAU TÍCH HỢP ĐIỂM - ĐIỂM (SLIDE 21)]",
        "  [E-Commerce Order DB] ──┬──► [Daily Analytics Exports]",
        "  [Payment Service    ] ──┼──► [Marketing Campaign Engine]",
        "  [User Clickstream   ] ──┼──► [Real-time Fraud Detection]",
        "  [Inventory Service  ] ──┴──► [Search & Redis Cache]",
        "• [x] Khi lưu lượng tăng, các truy vấn trích xuất làm chậm",
        "  trực tiếp giao dịch mua hàng sống (Live Transactions)!",
        "• [x] Vấn đề không nằm ở bản thân dữ liệu, mà nằm ở CÁCH",
        "  dữ liệu di chuyển hỗn loạn giữa các hệ thống (O(N x M)).",
    ], inner_width=INNER_HALF)
    s31_kafka = make_box([
        "[SAU KAFKA: KIẾN TRÚC PHÂN TÁN APACHE KAFKA (SLIDE 23)]",
        "                              ┌─────────────────────────────┐",
        "  [Producer 1..3] ──(Push)──► │ [KAFKA CLUSTER: 3 BROKERS]  │",
        "  (Nguồn đẩy dữ liệu)         │ • Broker 1: Topic A (P0, P1)│",
        "                              │ • Broker 2: Topic B (P0, P1)│",
        "  [Consumer 1..3] ◄──(Pull)── │ • Broker 3: Topic C (P0, P1)│",
        "  (Đích tự kéo khi sẵn sàng)  └─────────────────────────────┘",
        "• [+] Multiple Brokers: Nếu 1 máy chủ sập, các Broker còn lại",
        "  tiếp tục chạy bình thường -> Kafka không làm mất dữ liệu!",
    ], inner_width=INNER_HALF)
    row_31 = join_horizontal([s31_spaghetti, s31_kafka], ["    "], {4: [" ──►"]})

    diagrams["3.1"] = {
        "ascii": "\n".join(
            banner("TỪ MẠNG NHỆN ĐIỂM - ĐIỂM ĐẾN KIẾN TRÚC PHÂN TÁN APACHE KAFKA (SLIDE 21-23)")
            + [""]
            + row_31
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 3.2: Hệ sinh thái Kafka Mở rộng & Bước ngoặt Điều phối ZooKeeper -> KRaft
    # -------------------------------------------------------------------------
    s32_eco = make_box([
        "[CẮT LỚP LUỒNG DỮ LIỆU TRONG HỆ SINH THÁI KAFKA MỞ RỘNG (KAFKA EXTENDED API - SLIDE 25)]",
        "                                          ┌───────────────────────────┐",
        "                                          │   Kafka Streams / Flink   │ (Thư viện/Engine biến đổi luồng thời gian thực)",
        "                                          └─────────────▲─────────────┘",
        "                                                        │",
        "  [Source System] ──► [Kafka Connect Source] ──► [ KAFKA CLUSTER 1 ] ──► [Kafka Connect Sink] ──► [Target System]",
        "  (DB / App / Log)    (Nạp dữ liệu vào Kafka)    (Cụm chính lưu trữ) │   (Đẩy ra DB/Warehouse)    (Lakehouse / BI)",
        "                                                                     │",
        "                                                   [MirrorMaker 2] ◄─┘ (Sao chép liên cụm phục vụ Backup / Multi-Region)",
        "                                                          │",
        "                                                          ▼",
        "                                                 [ KAFKA CLUSTER 2 ] (Cụm thứ cấp dự phòng thảm họa / Disaster Recovery)",
    ], inner_width=INNER_FULL)

    s32_zk = make_box([
        "[ĐIỀU PHỐI THẾ HỆ CŨ: APACHE ZOOKEEPER (SLIDE 24)]",
        "• Dịch vụ điều phối bên ngoài dùng trong các bản Kafka cũ",
        "  để quản lý Metadata cụm và bầu chọn Broker Controller.",
        "• [x] Gánh nặng vận hành 2 hệ thống phân tán khác nhau.",
        "• [x] Cổ chai Metadata khi cụm vượt > 200.000 Partitions.",
    ], inner_width=INNER_HALF)
    s32_kraft = make_box([
        "[ĐIỀU PHỐI THẾ HỆ MỚI: KRAFT CONSENSUS (KAFKA 3.3+ / 4.0)]",
        "• Bộ điều phối đồng thuận Raft tích hợp sẵn bên trong Kafka",
        "  (Loại bỏ hoàn toàn sự phụ thuộc vào ZooKeeper từ bản 4.0!).",
        "• [+] Lưu Metadata dưới dạng Event Log (__cluster_metadata).",
        "• [+] Mở rộng hàng triệu Partitions, Failover trong vài ms.",
    ], inner_width=INNER_HALF)
    row_32 = join_horizontal([s32_zk, s32_kraft], ["    "], {2: [" ──►"]})

    diagrams["3.2"] = {
        "ascii": "\n".join(
            banner("HỆ SINH THÁI KAFKA MỞ RỘNG & BƯỚC NGOẶT ZOOKEEPER -> KRAFT (SLIDE 24-25)")
            + [""]
            + s32_eco
            + v_arrow("Tiến hóa tầng điều phối Metadata của Cụm Kafka (Cluster Coordination)")
            + row_32
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 3.3: Topic, Partition (Unit of Parallelism), Định cỡ & Zero-Copy
    # -------------------------------------------------------------------------
    s33_p1 = make_box([
        "[1. CHIẾN LƯỢC THIẾT KẾ TOPIC (SLIDE 28)]",
        "• Event-based : 1 Topic / loại sự kiện",
        "  (VD: user_created, order_paid)",
        "• Domain-based: 1 Topic / thực thể",
        "  nghiệp vụ (VD: orders, payments)",
        "• Env-based   : Tách biệt môi trường",
        "  (dev.orders, test.orders, prod.orders)",
    ], inner_width=INNER_THIRD)
    s33_p2 = make_box([
        "[2. PARTITION & SONG SONG HÓA (SLIDE 30-32)]",
        "• Single Queue: [M][M][M] -> 1 Reader chờ",
        "• Multi-Partition (Đọc song song):",
        "  ├── Partition 0 ──► Consumer A (Reader 0)",
        "  ├── Partition 1 ──► Consumer B (Reader 1)",
        "  └── Partition 2 ──► Consumer C (Reader 2)",
        "• Scale-out: Rải P0..P3 (M1), P4..P7 (M2)",
    ], inner_width=INNER_THIRD)
    s33_p3 = make_box([
        "[3. TOÁN HỌC ĐỊNH CỠ PARTITION (SLIDE 33)]",
        "• 1 Partition xử lý ~ 5 - 10 MB/s",
        "• Muốn 16 Consumers chạy song song",
        "  trong 1 Group -> Cần >= 16 Partitions!",
        "• Công thức định cỡ:",
        "  N = max(T_muc_tieu/T_p, T_muc_tieu/T_c)",
        "• [!] Quá nhiều Partition gây nặng Controller",
    ], inner_width=INNER_THIRD)
    row_33 = join_horizontal([s33_p1, s33_p2, s33_p3], ["    ", "    "])

    s33_zc = make_box([
        "[CẮT LỚP ĐƯỜNG TRUYỀN KERNEL ZERO-COPY sendfile(2): TẠI SAO KAFKA ĐẠT BĂNG THÔNG HÀNG GB/S? (CHƯƠNG 5 KAFKA GUIDE)]",
        "├── Luồng truyền thống (4 lần chép + 4 lần chuyển ngữ cảnh): [NVMe Disk] ──► [OS Page Cache] ──► [JVM Heap] ──► [Socket Buffer] ──► [NIC]",
        "└── Luồng Kafka Zero-Copy (syscall sendfile / DMA):          [NVMe Disk] ──► [OS Page Cache] ════════(Truyền thẳng DMA)══════════► [NIC]",
    ], inner_width=INNER_FULL)

    diagrams["3.3"] = {
        "ascii": "\n".join(
            banner("GIẢI PHẪU TOPIC, PARTITION (ĐƠN VỊ SONG SONG HÓA) & ZERO-COPY (SLIDE 27-33)")
            + [""]
            + row_33
            + [""]
            + s33_zc
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 3.4: Giải phẫu Con trỏ Offset, Control Records & Độ trễ Consumer Lag
    # -------------------------------------------------------------------------
    s34_tape = make_box([
        "[CẮT LỚP MẢNG NHẬT KÝ PARTITION 0 & KHOẢNG CÁCH TRỄ CONSUMER LAG (SLIDE 34)]",
        "",
        "   |<───────────── Dữ liệu đã đọc (Data Consumed) ─────────────>| |<────── Độ trễ (CONSUMER LAG = 3) ──────>| (Control)",
        "   ┌────────────┬────────────┬────────────┬────────────┬──────────┬────────────┬────────────┬────────────┬──────────┐",
        "   │  Offset 0  │  Offset 1  │  Offset 2  │  Offset 3  │ Offset 4 │  Offset 5  │  Offset 6  │  Offset 7  │ Offset 8 │",
        "   │   #8884    │   #8885    │   #8886    │   #8887    │  #8888   │   #8889    │   #8890    │  [COMMIT]  │ (Trống)  │",
        "   └────────────┴────────────┴────────────┴────────────┴────▲─────┴────────────┴────────────┴─────▲──────┴────▲─────┘",
        "                                                            │                                     │           │",
        "                                             [Consumer Position = Offset 4]            [Control Message]  [End Offset = 8]",
        "                                             (Lưu tại __consumer_offsets)              (Chốt Giao dịch)   (Vị trí mới nhất)",
    ], inner_width=INNER_FULL)

    s34_roles = make_box([
        "[CƠ CHẾ HOẠT ĐỘNG CỦA CON TRỎ OFFSET & CÔNG THỨC GIÁM SÁT CONSUMER LAG (SLIDE 34 + CHƯƠNG 4 & 10 KAFKA GUIDE)]",
        "├── [1] Định danh bất biến: Mỗi bản ghi vào Partition được gán 1 số nguyên tăng dần duy nhất (0, 1, 2, 3...) không bao giờ đổi",
        "├── [2] Ba công dụng cốt lõi: Theo dõi tiến độ đọc (Track progress) | Đọc tiếp sau khi sập (Resume) | Tua lại lịch sử (Reprocess)",
        "└── [3] Công thức Consumer Lag = End Offset - Current Consumer Offset: Chỉ số số 1 để phát hiện Consumer bị nghẽn và kích hoạt Scale-out!",
    ], inner_width=INNER_FULL)

    diagrams["3.4"] = {
        "ascii": "\n".join(
            banner("GIẢI PHẪU CON TRỎ OFFSET, CONTROL MESSAGES & ĐỘ TRỄ CONSUMER LAG (SLIDE 34)")
            + [""]
            + s34_tape
            + [""]
            + s34_roles
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 4.1: Producer Fundamentals — Keyed murmur2 Hash vs Keyless & RecordAccumulator
    # -------------------------------------------------------------------------
    s41_pipe = make_box([
        "[CẮT LỚP ĐƯỜNG ỐNG NỘI BỘ KAFKA PRODUCER CLIENT (CHƯƠNG 3 KAFKA: THE DEFINITIVE GUIDE)]",
        "  [ProducerRecord] ──► [1. Serializer (Avro/Schema ID)] ──► [2. Partitioner] ──► [3. RecordAccumulator (Deque Batch)] ──► [4. Sender Thread]",
        "  (Topic,Key,Val)      (Chuyển thành mảng Byte chuẩn)       (Tính mã Partition)   (Gom lô batch.size=64KB, linger.ms=10ms)  (Gửi tới Broker)",
    ], inner_width=INNER_FULL)

    s41_keyed = make_box([
        "[NHÁNH A: GỬI CÓ KHÓA (WITH KEY = 'USR-104' - SLIDE 35)]",
        "• Công thức băm: Partition = murmur2(key) % numPartitions",
        "• Mọi sự kiện của cùng Key 'USR-104' luôn vào CÙNG 1 Partition:",
        "  [Producer] ──(Key='USR-104': Đặt hàng #8888)──► [Partition 1]",
        "  [Producer] ──(Key='USR-104': Thanh toán    )──► [Partition 1]",
        "  [Producer] ──(Key='USR-104': Giao hàng     )──► [Partition 1]",
        "• [+] Bảo toàn thứ tự nhân quả 100% cho từng khách hàng/đơn hàng!",
    ], inner_width=INNER_HALF)
    s41_keyless = make_box([
        "[NHÁNH B: GỬI KHÔNG KHÓA (WITHOUT KEY = null - SLIDE 35)]",
        "• Thuật toán: Sticky Partitioner / Round-Robin phân bổ đều",
        "• Các bản ghi được rải sang tất cả các Partition để cân bằng tải:",
        "  [Producer] ──(Message A: Key=null)────────────► [Partition 0]",
        "  [Producer] ──(Message B: Key=null)────────────► [Partition 1]",
        "  [Producer] ──(Message C: Key=null)────────────► [Partition 2]",
        "• [+] Tối ưu thông lượng, nhưng mất thứ tự giữa các Message A, B, C!",
    ], inner_width=INNER_HALF)
    row_41 = join_horizontal([s41_keyed, s41_keyless], ["    "])

    diagrams["4.1"] = {
        "ascii": "\n".join(
            banner("PRODUCER FUNDAMENTALS: ĐƯỜNG ỐNG NỘI BỘ & CHIẾN LƯỢC CHỌN PARTITION (SLIDE 35)")
            + [""]
            + s41_pipe
            + v_arrow("Hai chế độ định tuyến Partition tại tầng Partitioner")
            + row_41
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 4.2: Consumer Groups, Parallelism, Idle Consumer & Cooperative Rebalance
    # -------------------------------------------------------------------------
    s42_left = make_box([
        "[QUY TẮC VÀNG TRONG CÙNG 1 CONSUMER GROUP (SLIDE 36)]",
        "  ┌─────────────────────┐      ┌────────────────────────┐",
        "  │ [  Topic: orders  ] │      │ [  Consumer Group 1  ] │",
        "  │ • Partition 0       ├─────►│ • Consumer 1 (Active)  │",
        "  │ • Partition 1       ├─────►│ • Consumer 2 (Active)  │",
        "  │ • Partition 2       ├─────►│ • Consumer 3 (Active)  │",
        "  └─────────────────────┘      │ • Consumer 4 [ IDLE! ] │",
        "                               └────────────────────────┘",
        "• Mỗi Partition chỉ được đọc bởi TỐI ĐA 1 Consumer trong Group!",
    ], inner_width=INNER_HALF)
    s42_right = make_box([
        "[PHÁT SÓNG ĐA NHÓM (FAN-OUT) & TÁI CÂN BẰNG (REBALANCE)]",
        "• Nhiều Consumer Group khác nhau cùng đọc 1 Topic độc lập:",
        "  ├── Group 1 (Fraud Detection): Đọc 100% sự kiện ở độ trễ <50ms",
        "  ├── Group 2 (Inventory Sync ): Đọc 100% sự kiện để trừ tồn kho",
        "  └── Group 3 (Lakehouse Sink ): Gom lô ghi Parquet xuống S3",
        "• Khi Consumer 3 sập hoặc xử lý lố max.poll.interval.ms:",
        "  ──► Group Coordinator chạy CooperativeStickyAssignor chuyển",
        "      riêng Partition 2 sang cho Consumer 1 mà không dừng cả cụm!",
    ], inner_width=INNER_HALF)
    row_42 = join_horizontal([s42_left, s42_right], ["    "])

    diagrams["4.2"] = {
        "ascii": "\n".join(
            banner("CONSUMER GROUPS: QUY TẮC ĐỘC QUYỀN PARTITION, FAN-OUT & REBALANCE (SLIDE 36)")
            + [""]
            + row_42
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 4.3: Replication & Fault Tolerance — Leader, Follower, ISR & Failover
    # -------------------------------------------------------------------------
    s43_norm = make_box([
        "[TRẠNG THÁI 1: HOẠT ĐỘNG BÌNH THƯỜNG (REPLICATION FACTOR = 3)]",
        "  • Broker 1: [Partition 0 - LEADER  ] ◄══ (Mọi Đọc/Ghi đi qua Leader)",
        "  • Broker 2: [Partition 0 - Follower] (Nằm trong tập ISR - Đã đồng bộ)",
        "  • Broker 3: [Partition 0 - Follower] (Nằm trong tập ISR - Đã đồng bộ)",
        "  • Broker 4: [Partition 2 - LEADER  ] (Phân bổ đều Leader qua các máy)",
    ], inner_width=INNER_HALF)
    s43_fail = make_box([
        "[TRẠNG THÁI 2: KHI BROKER 1 SẬP (AUTOMATIC LEADER ELECTION)]",
        "  • Broker 1: [x] SẬP NGUỒN / ĐỨT MẠNG (Mất toàn bộ Leader trên B1!)",
        "  • Broker 2: [+] TỰ ĐỘNG THĂNG CẤP LÀM LEADER MỚI CHO PARTITION 0!",
        "  • Broker 3: [Partition 0 - Follower] (Tiếp tục đồng bộ từ Broker 2)",
        "  • Kết quả : Hệ thống chạy liên tục với 0% mất mát dữ liệu (Slide 37)!",
    ], inner_width=INNER_HALF)
    row_43 = join_horizontal([s43_norm, s43_fail], ["    "], {2: [" ──►"]})

    s43_isr = make_box([
        "[CƠ HỌC TẬP HỢP ISR (IN-SYNC REPLICAS), HIGH WATERMARK & CẤU HÌNH BẤT BIẾN PRODUCTION (CHƯƠNG 6 KAFKA GUIDE)]",
        "├── [1] ISR (In-Sync Replicas)      : Tập các Replica bám sát Leader trong ngưỡng thời gian replica.lag.time.max.ms (Đủ tư cách lên ngôi)",
        "├── [2] High Watermark (HW)         : Offset cao nhất đã được chép thành công sang TOÀN BỘ các Replica trong ISR (Consumer chỉ thấy tới HW)",
        "└── [3] Cấu hình Chống Mất Dữ Liệu : replication.factor = 3  |  min.insync.replicas = 2  |  unclean.leader.election.enable = false",
    ], inner_width=INNER_FULL)

    diagrams["4.3"] = {
        "ascii": "\n".join(
            banner("REPLICATION & FAULT TOLERANCE: LEADER, FOLLOWER & BẦU CHỌN TỪ TẬP ISR (SLIDE 37)")
            + [""]
            + row_43
            + [""]
            + s43_isr
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 4.4: Kafka Message Delivery Guarantees (Slide 38-39)
    # -------------------------------------------------------------------------
    s44_m1 = make_box([
        "[1. AT-MOST-ONCE (TỐI ĐA 1 LẦN)]",
        "• Producer : acks = 0 (Bắn & quên)",
        "• Consumer : enable.auto.commit = true",
        "  (Commit Offset TRƯỚC khi xử lý)",
        "• Luồng    : Có thể mất bản ghi trên",
        "  đường truyền hoặc khi Consumer sập",
        "• Dùng cho : Telemetry/Log chấp nhận rơi",
    ], inner_width=INNER_THIRD)
    s44_m2 = make_box([
        "[2. AT-LEAST-ONCE (TỐI THIỂU 1 LẦN)]",
        "• Producer : acks = 1 hoặc acks = all",
        "• Consumer : enable.auto.commit = false",
        "  (Xử lý xong MỚI Commit Offset)",
        "• Luồng    : Nếu Consumer sập trước khi",
        "  Commit, khởi động lại sẽ ĐỌC LẠI",
        "  ──► Có thể sinh bản ghi TRÙNG LẶP!",
    ], inner_width=INNER_THIRD)
    s44_m3 = make_box([
        "[3. EXACTLY-ONCE (ĐÚNG 1 LẦN - EOS)]",
        "• Producer : acks = all &",
        "  enable.idempotence = true (PID + Seq)",
        "• Consumer : isolation.level =",
        "  read_committed + Transactional API",
        "• Luồng    : Giao nhận & xử lý đúng 1",
        "  lần duy nhất ngay cả khi sập mạng!",
    ], inner_width=INNER_THIRD)
    row_44 = join_horizontal([s44_m1, s44_m2, s44_m3], ["    ", "    "])

    s44_acks1 = make_box([
        "[PHẪU THUẬT CẢNH BÁO ĐÁY SLIDE 39: TẠI SAO CẤU HÌNH acks=1 KHÔNG ĐẢM BẢO CHỐNG MẤT DỮ LIỆU?]",
        "  [Bước 1] Producer gửi Order #8888 (acks=1) ──► [Broker 1 (Leader)] ghi vào đĩa cục bộ & lập tức trả ACK thành công cho Producer",
        "  [Bước 2] [x] Đúng khoảnh khắc đó, Broker 1 bị sập nguồn TRƯỚC KHI Broker 2 & Broker 3 (Followers) kịp kéo bản ghi #8888 về!",
        "  [Bước 3] Broker 2 được bầu làm Leader mới nhưng không có #8888 ──► Giao dịch #8888 bị MẤT VĨNH VIỄN dù Producer đã nhận báo OK!",
        "  [Chốt chặn]: Để đạt Zero Data Loss, bắt buộc phải đặt acks=all kết hợp min.insync.replicas=2 trên Broker!",
    ], inner_width=INNER_FULL)

    diagrams["4.4"] = {
        "ascii": "\n".join(
            banner("BA CẤP ĐỘ ĐẢM BẢO GIAO NHẬN & CẢNH BÁO MẤT DỮ LIỆU CỦA ACKS=1 (SLIDE 38-39)")
            + [""]
            + row_44
            + [""]
            + s44_acks1
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 4.5: Retention & Log Model trên Đĩa (Time, Size & Log Compaction)
    # -------------------------------------------------------------------------
    s45_left = make_box([
        "[1. XÓA THEO THỜI GIAN & DUNG LƯỢNG (SLIDE 40)]",
        "• Cấu trúc thư mục Partition trên đĩa (/orders-0/):",
        "  ├── 00000000000000000000.log (Closed - 8 ngày trước)",
        "  ├── 00000000000000541020.log (Closed - 3 ngày trước)",
        "  └── 00000000000000982100.log (Active Segment đang ghi)",
        "• Time-based (7 days) / Size-based (1 GB per partition):",
        "  ──► Chỉ việc gọi syscall unlink() xóa trọn tệp Segment cũ",
        "      với chi phí O(1), không gây phân mảnh đĩa cứng!",
    ], inner_width=INNER_HALF)
    s45_right = make_box([
        "[2. NÉN NHẬT KÝ THEO KHÓA (LOG COMPACTION - SLIDE 40)]",
        "• Chính sách: cleanup.policy = compact (Keep latest per key)",
        "• Trước khi nén (Vùng Dirty Tail đang ghi):",
        "  [Off 10: K=#8888, V=PENDING] -> [Off 11: K=#99, V=OK]",
        "  -> [Off 12: K=#8888, V=PAID] -> [Off 13: K=#8888, V=SHIPPED]",
        "• Sau khi Log Cleaner nén (Vùng Clean Head):",
        "  ──► Chỉ giữ lại: [Off 11: K=#99, V=OK] [Off 13: K=#8888, V=SHIPPED]",
        "• Xóa khóa: Bắn bản ghi bia mộ Tombstone [K=#8888, V=null]!",
    ], inner_width=INNER_HALF)
    row_45 = join_horizontal([s45_left, s45_right], ["    "])

    diagrams["4.5"] = {
        "ascii": "\n".join(
            banner("RETENTION & LOG MODEL: TIME/SIZE SEGMENT DELETION vs. LOG COMPACTION (SLIDE 40)")
            + [""]
            + row_45
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 5.1: Giải phẫu Debezium Log-Based CDC & Gói tin before/after/op
    # -------------------------------------------------------------------------
    s51_p1 = make_box([
        "[PHA 1: INITIAL CONSISTENT SNAPSHOT (KHỞI TẠO KHÔNG KHÓA BẢNG)]",
        "• [1] Mở giao dịch REPEATABLE READ, ghi nhận tọa độ LSN_0 = 0/16B3700",
        "• [2] Quét các dòng hiện có trong bảng orders, phát sự kiện op = 'r'",
        "• [3] Hoàn tất chụp ảnh mà không làm chặn các giao dịch ghi mới!",
    ], inner_width=INNER_HALF)
    s51_p2 = make_box([
        "[PHA 2: CONTINUOUS WAL STREAMING (CHUYỂN TIẾP KHÔNG KHE HỞ)]",
        "• [4] Móc vào khe nhân bản logic PostgreSQL (pgoutput Replication Slot)",
        "• [5] Đọc nối tiếp tệp WAL từ đúng vị trí LSN_0 = 0/16B3700 trở đi!",
        "• [6] Chuyển đổi mọi lệnh INSERT/UPDATE/DELETE thành sự kiện chuẩn.",
    ], inner_width=INNER_HALF)
    row_51 = join_horizontal([s51_p1, s51_p2], ["    "], {2: [" ──►"]})

    s51_env = make_box([
        "[CẮT LỚP PHONG BÌ SỰ KIỆN DEBEZIUM (DATABASE-AGNOSTIC EVENT ENVELOPE CHO ORDER #8888 - SLIDE 42)]",
        "  { \"op\": \"u\",                                   // Loại biến động: 'c' (INSERT), 'u' (UPDATE), 'd' (DELETE), 'r' (READ)",
        "    \"before\": { \"order_id\": \"ORD-8888\", \"user_id\": \"USR-104\", \"status\": \"PENDING\", \"amount\": 450000 }, // Trước khi sửa",
        "    \"after\" : { \"order_id\": \"ORD-8888\", \"user_id\": \"USR-104\", \"status\": \"PAID\",    \"amount\": 450000 }, // Sau khi sửa",
        "    \"source\": { \"connector\": \"postgresql\", \"db\": \"shop\", \"table\": \"orders\", \"lsn\": 23803720, \"ts_ms\": 1760785200000 } }",
    ], inner_width=INNER_FULL)

    diagrams["5.1"] = {
        "ascii": "\n".join(
            banner("GIẢI PHẪU DEBEZIUM CDC: SNAPSHOT -> WAL STREAMING & PHONG BÌ SỰ KIỆN (SLIDE 42)")
            + [""]
            + row_51
            + v_arrow("Biến đổi dòng byte nhị phân độc quyền của từng hãng DB thành cấu trúc JSON/Avro thống nhất")
            + s51_env
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 5.2: Đường ống End-to-End Debezium Sources & Sinks (Slide 43)
    # -------------------------------------------------------------------------
    s52_b1 = make_box([
        "1. Source Database",
        "• Postgres / MySQL",
        "• MongoDB / Oracle",
        "• SQLServer/Spanner",
    ], inner_width=19)
    s52_b2 = make_box([
        "2. Debezium Source",
        "• Đọc WAL / binlog",
        "• Gói before/after",
        "• Lưu tọa độ LSN",
    ], inner_width=19)
    s52_b3 = make_box([
        "3. Apache Kafka",
        "• Event Topic",
        "  prod.orders",
        "• Schema Registry",
    ], inner_width=17)
    s52_b4 = make_box([
        "4. Sink Connector",
        "• Kafka Connect",
        "• SMT Transform",
        "• Batch / Stream",
    ], inner_width=17)
    s52_b5 = make_box([
        "5. Multi-Sinks",
        "• Data Lakehouse",
        "• Elastic / Redis",
        "• Snowflake/Flink",
    ], inner_width=17)
    s52_inner_row = join_horizontal(
        [s52_b1, s52_b2, s52_b3, s52_b4, s52_b5],
        ["   ", "   ", "   ", "   "],
        {2: ["──►", "──►", "──►", "──►"]},
    )
    s52_pipe = make_box(
        ["[KIẾN TRÚC ĐƯỜNG ỐNG 4 CHẶNG: DEBEZIUM SOURCES AND SINKS (SLIDE 43)]", ""] + s52_inner_row,
        inner_width=INNER_FULL,
    )

    s52_internal = make_box([
        "[CẮT LỚP NỘI TẠI CỤM KAFKA CONNECT DISTRIBUTED CLUSTER (CHƯƠNG 7 KAFKA GUIDE)]",
        "├── [1] connect-offsets (Compacted Topic) : Lưu vị trí LSN / binlog file+pos để khi Connector khởi động lại đọc tiếp chính xác 100%",
        "├── [2] connect-configs & connect-status  : Đồng bộ cấu hình JSON và trạng thái sống còn của các Connector Tasks qua toàn bộ Workers",
        "└── [3] Single Message Transforms (SMTs)  : Biến đổi nhẹ trên đường bay (ExtractNewRecordState bóc phẳng after, MaskField ẩn số thẻ/SĐT)",
    ], inner_width=INNER_FULL)

    diagrams["5.2"] = {
        "ascii": "\n".join(
            banner("KIẾN TRÚC ĐƯỜNG ỐNG END-TO-END: SOURCE DB -> DEBEZIUM -> KAFKA -> SINKS (SLIDE 43)")
            + [""]
            + s52_pipe
            + [""]
            + s52_internal
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 5.3: Bốn Thách thức Vận hành Thực chiến (WAL Bloat, Schema Drift, Outbox)
    # -------------------------------------------------------------------------
    s53_c1 = make_box([
        "[1. NỔ ĐĨA DB NGUỒN DO KẸT REPLICATION SLOT (WAL BLOAT)]",
        "• Cơ chế gãy : Debezium chết HOẶC bảng orders ít ghi trong khi",
        "  bảng audit khác ghi liên tục -> Con trỏ confirmed_flush_lsn",
        "  bị đứng im -> PostgreSQL giữ lại toàn bộ tệp pg_wal gây sập DB!",
        "• Hóa giải   : Bật heartbeat.interval.ms + heartbeat.action.query",
        "  kết hợp khóa trần max_slot_wal_keep_size trong postgresql.conf!",
    ], inner_width=INNER_HALF)
    s53_c2 = make_box([
        "[2. TRÔI LƯỢC ĐỒ (SCHEMA DRIFT) & TIN NHẮN ĐỘC (POISON PILL)]",
        "• Cơ chế gãy : Nguồn đổi kiểu cột hoặc bắn bản ghi hỏng làm",
        "  Sink Connector văng ngoại lệ Deserialization và chết lặp lại!",
        "• Hóa giải   : Áp dụng Confluent Schema Registry (Kiểm tra tương",
        "  thích BACKWARD/FULL) + cấu hình errors.tolerance = all để tự",
        "  động đẩy bản ghi lỗi sang kênh cách ly Dead Letter Queue (DLQ).",
    ], inner_width=INNER_HALF)
    row_53_top = join_horizontal([s53_c1, s53_c2], ["    "])

    s53_c3 = make_box([
        "[3. LỆCH TẢI PHÂN VÙNG (HOT PARTITION) & GIÁM SÁT]",
        "• Cơ chế gãy : 1 khách hàng doanh nghiệp lớn chiếm 50% tổng",
        "  lượng đơn -> Băm cùng Key làm nghẽn cứng 1 Partition duy nhất!",
        "• Hóa giải   : Gắn hậu tố Salting Key (Key#1..N) và canh 3 chỉ số",
        "  vàng: UnderReplicatedPartitions=0, ActiveController=1, Lag.",
    ], inner_width=INNER_HALF)
    s53_c4 = make_box([
        "[4. BÀI TOÁN GHI KÉP (DUAL-WRITE) & OUTBOX PATTERN]",
        "• Cơ chế gãy : Microservice vừa COMMIT vào DB vừa gọi hàm",
        "  producer.send() -> Nếu sập giữa 2 lệnh sẽ gây lệch dữ liệu!",
        "• Hóa giải   : Ghi vào bảng orders VÀ bảng outbox_events trong",
        "  CÙNG 1 ACID Transaction local, rồi để Debezium đọc bảng Outbox!",
    ], inner_width=INNER_HALF)
    row_53_bot = join_horizontal([s53_c3, s53_c4], ["    "])

    diagrams["5.3"] = {
        "ascii": "\n".join(
            banner("BỐN THÁCH THỨC VẬN HÀNH THỰC CHIẾN & PHÁC ĐỒ HÓA GIẢI (PRODUCTION CHALLENGES)")
            + [""]
            + row_53_top
            + [""]
            + row_53_bot
        ),
        "kind": "boxes",
    }

    for k, meta in diagrams.items():
        errs = verify_diagram(meta["ascii"], f"ING-{k}", kind=meta["kind"])
        if errs:
            raise SystemExit(f"ASCII verification failed for ING-{k} ({meta['kind']}): {errs}")
    return diagrams


import html as _html_mod
import re as _re_mod

_LESSON_FUNC_SPECS = [
    ("renderStorageChang1", "D02", 1, "storage_diagrams"),
    ("renderStorageChang2", "D02", 2, "storage_diagrams"),
    ("renderStorageChang3", "D02", 3, "storage_diagrams"),
    ("renderStorageChang4", "D02", 4, "storage_diagrams"),
    ("renderStorageChang5", "D02", 5, "storage_diagrams"),
    ("renderStorageChang6", "D02", 6, "storage_diagrams"),
    ("renderStorageChang7", "D02", 7, "storage_diagrams"),
    ("renderLinuxChang1", "F01", 1, "linux_diagrams"),
    ("renderLinuxChang2", "F01", 2, "linux_diagrams"),
    ("renderLinuxChang3", "F01", 3, "linux_diagrams"),
    ("renderLinuxChang4", "F01", 4, "linux_diagrams"),
    ("renderDatabaseChang1", "F03", 1, "db_diagrams"),
    ("renderDatabaseChang2", "F03", 2, "db_diagrams"),
    ("renderDatabaseChang3", "F03", 3, "db_diagrams"),
    ("renderDatabaseChang4", "F03", 4, "db_diagrams"),
    ("renderContainerChang1", "F06", 1, "container_diagrams"),
    ("renderContainerChang2", "F06", 2, "container_diagrams"),
    ("renderContainerChang3", "F06", 3, "container_diagrams"),
    ("renderContainerChang4", "F06", 4, "container_diagrams"),
    ("renderIngestionChang1", "D01", 1, "ingestion_diagrams"),
    ("renderIngestionChang2", "D01", 2, "ingestion_diagrams"),
    ("renderIngestionChang3", "D01", 3, "ingestion_diagrams"),
    ("renderIngestionChang4", "D01", 4, "ingestion_diagrams"),
    ("renderIngestionChang5", "D01", 5, "ingestion_diagrams"),
]

_X_SPINE_RE = _re_mod.compile(
    r'<x-spine\s+id="([^"]*)"\s+badge="([^"]*)"\s+title="([^"]*)"\s+subtitle="([^"]*)"(?:\s+img="([^"]*)")?>(.*?)</x-spine>',
    _re_mod.DOTALL,
)
_X_FIGURE_RE = _re_mod.compile(
    r'<x-figure\s+id="([^"]*)"\s+key="([^"]*)"\s+title="([^"]*)">(.*?)</x-figure>',
    _re_mod.DOTALL,
)
_X_INFRA2D_RE = _re_mod.compile(r"<x-infra2d></x-infra2d>")
_X_INGESTION2D_RE = _re_mod.compile(r"<x-ingestion2d>\s*</x-ingestion2d>")


def _js_str_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _compile_lesson_html_to_js(html_content: str) -> str:
    out = html_content.rstrip("\n").replace("`", "\\`").replace("${", "\\${")

    def repl_x_spine(m):
        sid, badge, title, subtitle, _img, cap = m.groups()
        sid = _js_str_escape(_html_mod.unescape(sid))
        badge = _js_str_escape(_html_mod.unescape(badge))
        title = _js_str_escape(_html_mod.unescape(title))
        subtitle = _js_str_escape(_html_mod.unescape(subtitle))
        cap_raw = cap.replace("\\`", "`").replace("\\${", "${")
        cap_esc = _js_str_escape(cap_raw)
        return (
            "${buildSpineHeroBanner({\n"
            f'          id: "{sid}",\n'
            f'          badge: "{badge}",\n'
            f'          title: "{title}",\n'
            f'          subtitle: "{subtitle}",\n'
            f'          captionHtml: "{cap_esc}"\n'
            "        })}"
        )

    def repl_x_figure(m):
        vid, dkey, title, cap = m.groups()
        vid = _js_str_escape(_html_mod.unescape(vid))
        dkey = _html_mod.unescape(dkey)
        title = _js_str_escape(_html_mod.unescape(title))
        cap_raw = cap.replace("\\`", "`").replace("\\${", "${")
        cap_esc = _js_str_escape(cap_raw)
        return (
            "${buildVisualBlock(\n"
            f'          "{vid}",\n'
            f'          "{title}",\n'
            f'          d["{dkey}"].ascii,\n'
            f'          "{cap_esc}",\n'
            f'          d["{dkey}"].asciiHtml,\n'
            f'          d["{dkey}"].maxCols,\n'
            f'          d["{dkey}"].flagship\n'
            "        )}"
        )

    out = _X_SPINE_RE.sub(repl_x_spine, out)
    out = _X_FIGURE_RE.sub(repl_x_figure, out)
    out = _X_INFRA2D_RE.sub("${buildInfra2DSimulatorHtml()}", out)
    out = _X_INGESTION2D_RE.sub("${buildIngestion2DSimulatorHtml()}", out)
    return out


def compile_lesson_templates_js() -> str:
    lessons_dir = ROOT / "content" / "lessons"
    js_blocks = []
    for func_name, topic, stage, diag_prop in _LESSON_FUNC_SPECS:
        fpath = lessons_dir / topic / f"stage-{stage}.html"
        if not fpath.exists():
            raise FileNotFoundError(f"Missing extracted lesson template: {fpath}")
        raw_html = fpath.read_text(encoding="utf-8")
        compiled_body = _compile_lesson_html_to_js(raw_html)
        js_blocks.append(
            f"  function {func_name}() {{\n"
            f"    const d = HUB_DATA.{diag_prop};\n"
            f"    return `\n{compiled_body}\n    `;\n"
            f"  }}"
        )
    js_blocks.append(
        """  const LESSON_RENDERERS = {
    D02: {
      1: renderStorageChang1,
      2: renderStorageChang2,
      3: renderStorageChang3,
      4: renderStorageChang4,
      5: renderStorageChang5,
      6: renderStorageChang6,
      7: renderStorageChang7
    },
    F01: {
      1: renderLinuxChang1,
      2: renderLinuxChang2,
      3: renderLinuxChang3,
      4: renderLinuxChang4
    },
    F03: {
      1: renderDatabaseChang1,
      2: renderDatabaseChang2,
      3: renderDatabaseChang3,
      4: renderDatabaseChang4
    },
    F06: {
      1: renderContainerChang1,
      2: renderContainerChang2,
      3: renderContainerChang3,
      4: renderContainerChang4
    },
    D01: {
      1: renderIngestionChang1,
      2: renderIngestionChang2,
      3: renderIngestionChang3,
      4: renderIngestionChang4,
      5: renderIngestionChang5
    }
  };"""
    )
    return "\n\n".join(js_blocks)


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="vi" class="light" data-cds="" data-mode="light" data-density="comfortable" data-platform="web" data-font="anthropic">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>FSDS · EDAI · DSAI — Tài liệu Học tập Kỹ thuật</title>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 21 21'%3E%3Cpath fill='%23d97757' d='M12.313 1.5h3.112L21 16.5h-3.112l-1.15-3.175h-6.288L9.3 16.5H6.188l5.562-15h.563zm1.556 3.725-2.25 6.212h4.5l-2.25-6.212zM0 16.5 5.563 1.5h3.112L3.113 16.5H0z'/%3E%3C/svg%3E" />
  <style>
  __FONT_FACES__

  /* ==========================================================================
     1. CLAUDE ACADEMY DESIGN SYSTEM (CDS TOKENS · 21-STOP OKLAB SWATCHES)
     ========================================================================== */
  :root,
  html[data-cds] {
    --cds-font-sans: "anthropic-sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --cds-font-serif: "anthropic-serif", Georgia, Cambria, "Times New Roman", serif;
    --cds-font-mono: "anthropic-mono", "JetBrains Mono", "SFMono-Regular", ui-monospace, Menlo, monospace;
    --cds-font-display: var(--cds-font-serif);
    --cds-font-reading: var(--cds-font-sans);
    --cds-font-voice: var(--cds-font-serif);

    --font-display: var(--cds-font-serif);
    --font-sans: var(--cds-font-sans);
    --font-mono: var(--cds-font-mono);

    --cds-clay: #d97757;
    --cds-radius-xs: 4px;
    --cds-radius-sm: 6px;
    --cds-radius-md: 8px;
    --cds-radius-card: 12px;
    --cds-radius-pill: 9999px;

    --rail-width: 296px;
    --toc-width: 268px;
    --header-height: 56px;
    --page-gutter: clamp(20px, 3.8vw, 48px);
    --article-max: 58rem;
    --reading-measure: 47rem;
    --motion-duration: 210ms;
    --motion-ease: cubic-bezier(0.22, 1, 0.36, 1);
  }

  /* Light Mode (Claude Academy Warm Parchment #faf9f5 / Stone #f0eee6 / Sand #e8e6dc) */
  html.light,
  html[data-mode="light"] {
    color-scheme: light;
    --cds-surface-0: #faf9f5;
    --cds-surface-1: #f0eee6;
    --cds-surface-2: #e8e6dc;
    --cds-surface-card: #ffffff;
    --cds-page-bg: var(--cds-surface-0);
    --cds-text-primary: #141413;
    --cds-text-body: #252523;
    --cds-text-secondary: #3d3d3a;
    --cds-text-muted: #6c6a63;
    --cds-border-subtle: rgba(31, 30, 29, 0.10);
    --cds-border-default: rgba(31, 30, 29, 0.16);
    --cds-border-strong: rgba(31, 30, 29, 0.28);
    --cds-fill-ghost-hover: rgba(20, 20, 19, 0.06);
    --cds-fill-ghost-active: rgba(20, 20, 19, 0.10);
    --cds-fill-primary: #141413;
    --cds-text-on-primary: #faf9f5;

    --cds-shadow-card-ring: 0 0 0 1px rgba(31, 30, 29, 0.10), 0 1px 2px rgba(20, 20, 19, 0.03);
    --cds-shadow-hero-edge: inset 0 -1px 0 0 rgba(31, 30, 29, 0.11);
    --cds-shadow-popover: 0 12px 32px rgba(20, 20, 19, 0.14), 0 2px 6px rgba(20, 20, 19, 0.06), 0 0 0 1px rgba(20, 20, 19, 0.12);
    --cds-shadow-modal: 0 24px 64px rgba(20, 20, 19, 0.22), 0 4px 16px rgba(20, 20, 19, 0.08), 0 0 0 1px rgba(20, 20, 19, 0.15);

    --th-bg: #faf9f5;
    --th-surface: #f0eee6;
    --th-elevated: #ffffff;
    --th-border: #dad8ce;
    --th-border-subtle: #e8e6dc;

    --bg: var(--cds-surface-0);
    --surface: var(--cds-surface-1);
    --surface-subtle: var(--cds-surface-2);
    --surface-hover: rgba(20, 20, 19, 0.06);
    --ink: var(--cds-text-primary);
    --ink-bold: #141413;
    --ink-secondary: var(--cds-text-secondary);
    --muted: var(--cds-text-muted);
    --selection-bg: #ebe2d3;
    --line: var(--cds-border-subtle);
    --line-strong: var(--cds-border-default);
    --border-strong: var(--cds-border-strong);
    --accent: #b54e2e;
    --accent-strong: #963c20;
    --accent-interactive: #1f64bd;
    --accent-soft: rgba(217, 119, 87, 0.11);
    --code-inline-bg: rgba(20, 20, 19, 0.06);
    --code-block-bg: #f0eee6;

    --glossary-surface: #ffffff;
    --glossary-border: rgba(20, 20, 19, 0.14);
    --glossary-shadow: var(--cds-shadow-popover);
    --glossary-underline: rgba(108, 106, 99, 0.55);
    --glossary-badge-bg: rgba(217, 119, 87, 0.13);
    --glossary-badge-text: #963c20;

    /* Monodraw + Durdraw Semantic ANSI Palette (Light Mode — WCAG AA >= 4.5:1) */
    --ac-border: #0369a1;
    --ac-shadow: #94a3b8;
    --ac-header: #b54e2e;
    --ac-flow: #0284c7;
    --ac-ok: #047857;
    --ac-warn: #b45309;
    --ac-danger: #be123c;
    --ac-muted: #595650;

    /* Interactive 2D Simulator Palette (Claude Academy Warm Parchment — Light Mode) */
    --sim-bg: var(--cds-surface-1);
    --sim-header-bg: var(--cds-surface-2);
    --sim-canvas: #f6f4ec;
    --sim-card: #ffffff;
    --sim-card-alt: #eeeae0;
    --sim-border: #d5d1c6;
    --sim-border-muted: #b8b3a6;
    --sim-ink: var(--cds-text-primary);
    --sim-sub: var(--cds-text-body);
    --sim-muted: var(--cds-text-muted);
    --sim-clay: var(--accent);
    --sim-clay-soft: var(--accent-soft);
    --sim-clay-border: color-mix(in oklab, var(--cds-clay) 36%, transparent);
    --sim-flow: var(--ac-flow);
    --sim-flow-soft: color-mix(in oklab, var(--ac-flow) 12%, var(--sim-card));
    --sim-ok: var(--ac-ok);
    --sim-ok-soft: color-mix(in oklab, var(--ac-ok) 12%, var(--sim-card));
    --sim-warn: var(--ac-warn);
    --sim-warn-soft: color-mix(in oklab, var(--ac-warn) 14%, var(--sim-card));
    --sim-danger: var(--ac-danger);
    --sim-danger-soft: color-mix(in oklab, var(--ac-danger) 12%, var(--sim-card));
  }

  /* Dark Mode (Claude Academy Obsidian #141413) */
  html.dark,
  html[data-mode="dark"] {
    color-scheme: dark;
    --cds-surface-0: #141413;
    --cds-surface-1: #1f1e1b;
    --cds-surface-2: #2a2924;
    --cds-surface-card: #1f1e1b;
    --cds-page-bg: var(--cds-surface-0);
    --cds-text-primary: #faf9f5;
    --cds-text-body: #e8e6dc;
    --cds-text-secondary: #c2c0b6;
    --cds-text-muted: #9a988e;
    --cds-border-subtle: rgba(250, 249, 245, 0.10);
    --cds-border-default: rgba(250, 249, 245, 0.17);
    --cds-border-strong: rgba(250, 249, 245, 0.28);
    --cds-fill-ghost-hover: rgba(250, 249, 245, 0.065);
    --cds-fill-ghost-active: rgba(250, 249, 245, 0.11);
    --cds-fill-primary: #faf9f5;
    --cds-text-on-primary: #141413;

    --cds-shadow-card-ring: 0 0 0 1px rgba(250, 249, 245, 0.12), 0 1px 3px rgba(0, 0, 0, 0.35);
    --cds-shadow-hero-edge: inset 0 -1px 0 0 rgba(250, 249, 245, 0.13);
    --cds-shadow-popover: 0 14px 36px rgba(0, 0, 0, 0.55), 0 3px 8px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(250, 249, 245, 0.16);
    --cds-shadow-modal: 0 24px 64px rgba(0, 0, 0, 0.68), 0 4px 16px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(250, 249, 245, 0.18);

    --th-bg: #141413;
    --th-surface: #1f1e1b;
    --th-elevated: #282623;
    --th-border: #3d3b36;
    --th-border-subtle: #2e2c28;

    --bg: var(--cds-surface-0);
    --surface: var(--cds-surface-1);
    --surface-subtle: var(--cds-surface-2);
    --surface-hover: rgba(250, 249, 245, 0.075);
    --ink: var(--cds-text-primary);
    --ink-bold: #faf9f5;
    --ink-secondary: var(--cds-text-secondary);
    --muted: var(--cds-text-muted);
    --selection-bg: #38332c;
    --line: var(--cds-border-subtle);
    --line-strong: var(--cds-border-default);
    --border-strong: var(--cds-border-strong);
    --accent: #e38768;
    --accent-strong: #d97757;
    --accent-interactive: #5b9cf0;
    --accent-soft: rgba(217, 119, 87, 0.16);
    --code-inline-bg: rgba(250, 249, 245, 0.08);
    --code-block-bg: #181715;

    --glossary-surface: #1f1e1b;
    --glossary-border: rgba(250, 249, 245, 0.16);
    --glossary-shadow: var(--cds-shadow-popover);
    --glossary-underline: rgba(156, 153, 143, 0.58);
    --glossary-badge-bg: rgba(217, 119, 87, 0.16);
    --glossary-badge-text: #f39d7b;

    /* Monodraw + Durdraw Semantic ANSI Palette (Dark Mode) */
    --ac-border: #38bdf8;
    --ac-shadow: #475569;
    --ac-header: #f59e0b;
    --ac-flow: #22d3ee;
    --ac-ok: #34d399;
    --ac-warn: #fbbf24;
    --ac-danger: #fb7185;
    --ac-muted: #94a3b8;

    /* Interactive 2D Simulator Palette (Claude Academy Warm Obsidian — Dark Mode) */
    --sim-bg: var(--cds-surface-1);
    --sim-header-bg: var(--cds-surface-2);
    --sim-canvas: #161513;
    --sim-card: #211f1c;
    --sim-card-alt: #2a2824;
    --sim-border: #3d3a34;
    --sim-border-muted: #57534a;
    --sim-ink: var(--cds-text-primary);
    --sim-sub: var(--cds-text-body);
    --sim-muted: var(--cds-text-muted);
    --sim-clay: var(--accent);
    --sim-clay-soft: var(--accent-soft);
    --sim-clay-border: color-mix(in oklab, var(--cds-clay) 42%, transparent);
    --sim-flow: var(--ac-flow);
    --sim-flow-soft: color-mix(in oklab, var(--ac-flow) 16%, var(--sim-card));
    --sim-ok: var(--ac-ok);
    --sim-ok-soft: color-mix(in oklab, var(--ac-ok) 16%, var(--sim-card));
    --sim-warn: var(--ac-warn);
    --sim-warn-soft: color-mix(in oklab, var(--ac-warn) 17%, var(--sim-card));
    --sim-danger: var(--ac-danger);
    --sim-danger-soft: color-mix(in oklab, var(--ac-danger) 17%, var(--sim-card));
  }

  /* 6 Curated Editorial Accent Palettes (Default: Anthropic Clay #d97757) */
  html[data-accent="cobalt"] {
    --cds-clay: #3b6fd4;
    --accent: #2856b3;
    --accent-strong: #1d428f;
    --accent-soft: rgba(59, 111, 212, 0.12);
    --glossary-badge-bg: rgba(59, 111, 212, 0.13);
    --glossary-badge-text: #21499c;
  }
  html.dark[data-accent="cobalt"] {
    --cds-clay: #689bf5;
    --accent: #7daaf8;
    --accent-strong: #5389eb;
    --accent-soft: rgba(104, 155, 245, 0.17);
    --glossary-badge-bg: rgba(104, 155, 245, 0.18);
    --glossary-badge-text: #9ec0ff;
  }
  html[data-accent="sage"] {
    --cds-clay: #2f7d5b;
    --accent: #236648;
    --accent-strong: #194f37;
    --accent-soft: rgba(47, 125, 91, 0.12);
    --glossary-badge-bg: rgba(47, 125, 91, 0.13);
    --glossary-badge-text: #1c593e;
  }
  html.dark[data-accent="sage"] {
    --cds-clay: #56b389;
    --accent: #6ec49d;
    --accent-strong: #469e76;
    --accent-soft: rgba(86, 179, 137, 0.17);
    --glossary-badge-bg: rgba(86, 179, 137, 0.18);
    --glossary-badge-text: #8cdbb6;
  }
  html[data-accent="plum"] {
    --cds-clay: #7c52ab;
    --accent: #643c91;
    --accent-strong: #4d2b73;
    --accent-soft: rgba(124, 82, 171, 0.12);
    --glossary-badge-bg: rgba(124, 82, 171, 0.13);
    --glossary-badge-text: #563280;
  }
  html.dark[data-accent="plum"] {
    --cds-clay: #a982d9;
    --accent: #ba98e6;
    --accent-strong: #946bc7;
    --accent-soft: rgba(169, 130, 217, 0.17);
    --glossary-badge-bg: rgba(169, 130, 217, 0.18);
    --glossary-badge-text: #ceb3f2;
  }
  html[data-accent="ochre"] {
    --cds-clay: #b8781e;
    --accent: #945d10;
    --accent-strong: #754708;
    --accent-soft: rgba(184, 120, 30, 0.12);
    --glossary-badge-bg: rgba(184, 120, 30, 0.14);
    --glossary-badge-text: #804f0a;
  }
  html.dark[data-accent="ochre"] {
    --cds-clay: #e5a343;
    --accent: #f0b45b;
    --accent-strong: #d18d2c;
    --accent-soft: rgba(229, 163, 67, 0.17);
    --glossary-badge-bg: rgba(229, 163, 67, 0.18);
    --glossary-badge-text: #f7c983;
  }
  html[data-accent="crimson"] {
    --cds-clay: #b8424c;
    --accent: #962f38;
    --accent-strong: #782129;
    --accent-soft: rgba(184, 66, 76, 0.11);
    --glossary-badge-bg: rgba(184, 66, 76, 0.13);
    --glossary-badge-text: #852730;
  }
  html.dark[data-accent="crimson"] {
    --cds-clay: #e66c76;
    --accent: #f0848d;
    --accent-strong: #d15660;
    --accent-soft: rgba(230, 108, 118, 0.17);
    --glossary-badge-bg: rgba(230, 108, 118, 0.18);
    --glossary-badge-text: #f7a6ad;
  }

  /* 21-Stop OKLab Precomputed Swatches from academy.claude.com */
  .swatch-peach {
    --swatch-bg: #e09070;
    --swatch-fg: #6b2a14;
    --swatch-accent: #b84a24;
    --swatch-band: #ebd9ce;
    --swatch-0: #6b2a14;
  }
  .swatch-cactus {
    --swatch-bg: #7cb090;
    --swatch-fg: #1b422b;
    --swatch-accent: #2c6b45;
    --swatch-band: #d4e3d7;
    --swatch-0: #1b422b;
  }
  .swatch-heather {
    --swatch-bg: #9e8cb8;
    --swatch-fg: #32244b;
    --swatch-accent: #584182;
    --swatch-band: #dfdbe6;
    --swatch-0: #32244b;
  }
  .swatch-oat {
    --swatch-bg: #c9b79c;
    --swatch-fg: #443722;
    --swatch-accent: #785f37;
    --swatch-band: #e9e4d8;
    --swatch-0: #443722;
  }

  html.dark .swatch-peach,
  html[data-mode="dark"] .swatch-peach {
    --swatch-bg: #542818;
    --swatch-fg: #f5cbb8;
    --swatch-accent: #e0835e;
    --swatch-band: #281b16;
    --swatch-0: #f5cbb8;
  }
  html.dark .swatch-cactus,
  html[data-mode="dark"] .swatch-cactus {
    --swatch-bg: #1e3d2b;
    --swatch-fg: #bde0c9;
    --swatch-accent: #68ab81;
    --swatch-band: #17231c;
    --swatch-0: #bde0c9;
  }
  html.dark .swatch-heather,
  html[data-mode="dark"] .swatch-heather {
    --swatch-bg: #2e2440;
    --swatch-fg: #d9cee8;
    --swatch-accent: #9f8bc0;
    --swatch-band: #1d1924;
    --swatch-0: #d9cee8;
  }
  html.dark .swatch-oat,
  html[data-mode="dark"] .swatch-oat {
    --swatch-bg: #382f21;
    --swatch-fg: #e8decb;
    --swatch-accent: #bfa782;
    --swatch-band: #211e18;
    --swatch-0: #e8decb;
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
    background: var(--cds-surface-0);
    color: var(--cds-text-body);
    font-family: var(--cds-font-sans);
    font-size: 16.5px;
    line-height: 1.68;
    letter-spacing: -0.003em;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    font-synthesis: none;
  }

  button, input, select, textarea {
    font-family: var(--cds-font-sans);
    letter-spacing: -0.003em;
  }

  code, pre, kbd, samp {
    font-family: var(--cds-font-mono);
    letter-spacing: 0;
    font-variant-ligatures: none;
    font-feature-settings: "liga" 0, "calt" 0;
  }

  h1, h2 {
    font-family: var(--cds-font-serif);
    font-weight: 400;
    color: var(--cds-text-primary);
  }
  h3, h4 {
    font-family: var(--cds-font-sans);
    color: var(--cds-text-primary);
  }

  strong, b {
    font-weight: 600;
    color: var(--cds-text-primary);
  }

  a {
    color: var(--accent);
    text-decoration: underline;
    text-underline-offset: 3px;
  }
  a:hover {
    color: var(--cds-text-primary);
  }

  :where(button, a, input, summary, [tabindex]):focus-visible {
    outline: 2px solid var(--cds-clay);
    outline-offset: 2px;
  }

  .cds-icon {
    font-family: "Anthropicons-Variable", sans-serif;
    font-weight: 400;
    font-style: normal;
    line-height: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    user-select: none;
    flex-shrink: 0;
  }

  /* ==========================================================================
     2. CLAUDE ACADEMY GLOBAL HEADER (h-14 / 56px)
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
    background: var(--cds-clay);
    transition: width 0.12s linear;
  }

  .topbar {
    position: sticky;
    top: 0;
    z-index: 60;
    height: var(--header-height);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 0 20px;
    background: var(--cds-surface-0);
    border-bottom: 1px solid var(--cds-border-subtle);
    line-height: 1.25;
  }

  .topbar-context {
    display: flex;
    align-items: center;
    gap: 6px;
    min-width: 0;
  }

  .topbar-actions {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
  }

  .ui-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    height: 32px;
    padding: 0 10px;
    font-size: 13.5px;
    font-weight: 400;
    line-height: 1.2;
    color: var(--cds-text-secondary);
    background: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    cursor: pointer;
    text-decoration: none;
    white-space: nowrap;
    transition: background 0.14s ease, border-color 0.14s ease, color 0.14s ease, transform 0.12s ease;
  }
  .ui-btn:hover {
    background: var(--cds-fill-ghost-hover);
    color: var(--cds-text-primary);
  }
  .ui-btn:active {
    transform: scale(0.985);
  }
  .ui-btn[aria-expanded="true"],
  .ui-btn.active {
    background: var(--cds-fill-ghost-hover);
    color: var(--cds-text-primary);
    font-weight: 500;
  }

  .ui-btn-ghost {
    border-color: transparent;
    padding: 0 8px;
  }

  .search-pill-btn {
    height: 32px;
    border-radius: 8px;
    background: var(--cds-surface-1);
    box-shadow: var(--cds-shadow-card-ring);
    padding: 0 11px;
    gap: 8px;
    color: var(--cds-text-muted);
    font-size: 13px;
  }
  .search-pill-btn:hover {
    background: var(--cds-surface-2);
    color: var(--cds-text-primary);
  }

  kbd.shortcut-key {
    display: inline-block;
    padding: 1px 5px;
    font-family: var(--cds-font-mono);
    font-size: 10.5px;
    line-height: 1.2;
    color: var(--cds-text-muted);
    background: var(--cds-surface-0);
    border: 1px solid var(--cds-border-default);
    border-radius: 4px;
  }

  .rail-toggle-modern {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    height: 32px;
    padding: 0 11px;
    border-radius: 7px;
    border: 1px solid var(--cds-border-subtle);
    background: var(--cds-surface-1);
    color: var(--cds-text-primary);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.14s ease, border-color 0.14s ease;
  }
  .rail-toggle-modern:hover {
    background: var(--cds-surface-2);
    border-color: var(--cds-border-default);
  }
  .rail-toggle-svg {
    width: 15px;
    height: 15px;
    stroke: currentColor;
    fill: none;
    stroke-width: 1.65;
    flex-shrink: 0;
  }

  .academy-brand-btn {
    display: inline-flex;
    align-items: center;
    gap: 11px;
    color: var(--cds-text-primary);
    border: 0;
    background: transparent;
    border-radius: 8px;
    padding: 0 10px;
    height: 38px;
    cursor: pointer;
    transition: background 0.14s ease;
  }
  .academy-brand-btn:hover {
    background: var(--cds-fill-ghost-hover);
  }
  .academy-brand-mark {
    width: 28px;
    height: 28px;
    border-radius: 7px;
    background: var(--accent-dim);
    border: 1px solid var(--accent-border);
    color: var(--cds-clay);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    position: relative;
    flex-shrink: 0;
    transition: border-color 0.16s ease, background 0.16s ease;
  }
  .academy-brand-btn:hover .academy-brand-mark {
    border-color: var(--cds-clay);
  }
  .academy-brand-mark svg {
    width: 16px;
    height: 16px;
    display: block;
  }
  .academy-brand-wordmark {
    display: inline-flex;
    align-items: baseline;
    gap: 9px;
  }
  .academy-brand-main {
    font-family: var(--cds-font-sans);
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--cds-text-primary);
  }
  .academy-brand-sep {
    width: 1px;
    height: 14px;
    background: var(--cds-border-strong);
    align-self: center;
    flex-shrink: 0;
  }
  .academy-brand-sub {
    font-family: var(--cds-font-serif);
    font-weight: 400;
    font-size: 17.5px;
    letter-spacing: -0.01em;
    color: var(--cds-text-secondary);
  }

  /* Accent Swatch Picker & Bilingual Switcher */
  .accent-picker-wrap {
    position: relative;
    display: inline-flex;
    align-items: center;
  }
  .accent-trigger-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    height: 32px;
    padding: 0 10px;
    border-radius: 7px;
    border: 1px solid var(--cds-border-subtle);
    background: var(--cds-surface-1);
    color: var(--cds-text-primary);
    font-family: var(--cds-font-sans);
    font-size: 12.5px;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.14s ease, border-color 0.14s ease;
  }
  .accent-trigger-btn:hover {
    background: var(--cds-surface-2);
    border-color: var(--cds-border-default);
  }
  .accent-dot-live,
  .accent-trigger-dot {
    width: 11px;
    height: 11px;
    border-radius: 999px;
    background: var(--cds-clay);
    box-shadow: inset 0 0 0 1px rgba(20, 20, 19, 0.22);
    flex-shrink: 0;
  }
  .accent-popover {
    position: absolute;
    top: calc(100% + 8px);
    right: 0;
    z-index: 125;
    background: var(--cds-surface-0);
    border: 1px solid var(--cds-border-default);
    border-radius: 10px;
    box-shadow: var(--cds-shadow-popover);
    padding: 8px 10px;
    display: none;
    align-items: center;
    gap: 7px;
    white-space: nowrap;
  }
  .accent-popover.open {
    display: inline-flex;
  }
  .accent-swatch-opt,
  .accent-swatch-btn {
    width: 22px;
    height: 22px;
    border-radius: 999px;
    border: 2px solid transparent;
    cursor: pointer;
    padding: 0;
    flex-shrink: 0;
    transition: transform 0.14s ease, border-color 0.14s ease;
  }
  .accent-swatch-opt:hover,
  .accent-swatch-btn:hover {
    transform: scale(1.12);
  }
  .accent-swatch-opt.active,
  .accent-swatch-btn.active {
    border-color: var(--cds-text-primary);
    transform: scale(1.08);
  }

  .lang-switch-btn {
    font-family: var(--cds-font-sans);
    font-weight: 600;
    font-size: 11.5px;
    letter-spacing: 0.03em;
    padding: 0 5px;
    height: 32px;
    border-radius: 7px;
    border: 1px solid var(--cds-border-subtle);
    background: var(--cds-surface-1);
    color: var(--cds-text-muted);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 2px;
    transition: background 0.14s ease, border-color 0.14s ease;
  }
  .lang-switch-btn:hover {
    background: var(--cds-surface-2);
    border-color: var(--cds-border-default);
  }
  .lang-switch-btn.is-translating {
    opacity: 0.72;
    pointer-events: none;
  }
  .lang-opt {
    padding: 3px 6px;
    border-radius: 5px;
    line-height: 1;
    color: var(--cds-text-muted);
    transition: background 0.14s ease, color 0.14s ease;
  }
  .lang-opt.active {
    background: var(--cds-surface-0);
    color: var(--cds-clay);
    box-shadow: var(--cds-shadow-card-ring);
  }

  .topbar-divider {
    width: 1px;
    height: 16px;
    background: var(--cds-border-default);
    margin: 0 4px;
    flex-shrink: 0;
  }

  .topbar-nav-tabs {
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }

  .topbar-context-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    height: 28px;
    padding: 0 10px;
    border-radius: 999px;
    background: var(--cds-surface-1);
    box-shadow: var(--cds-shadow-card-ring);
    font-size: 12.5px;
    color: var(--cds-text-secondary);
    white-space: nowrap;
    max-width: 340px;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .topbar-context-pill strong {
    font-family: var(--cds-font-mono);
    font-size: 11px;
    font-weight: 500;
    color: var(--cds-clay);
  }

  /* ==========================================================================
     3. CLAUDE ACADEMY <HubShell> 3-COLUMN LAYOUT, LEFT SIDEBAR & RIGHT TOC
        (Unified Visual Grammar Across Left & Right Rails)
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
    background: var(--cds-surface-0);
    border-right: 1px solid var(--cds-border-subtle);
    height: calc(100vh - var(--header-height));
    overflow-y: auto;
    overscroll-behavior: contain;
    padding: 18px 14px 48px;
    line-height: 1.38;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .skip-link {
    position: fixed;
    top: -100px;
    left: 16px;
    z-index: 200;
    padding: 10px 16px;
    background: var(--cds-text-primary);
    color: var(--cds-surface-0);
    font-weight: 500;
    font-size: 13px;
    border-radius: 6px;
    text-decoration: none;
    transition: top 0.15s ease;
  }
  .skip-link:focus {
    top: 10px;
  }

  /* Unified Section Header for BOTH Left Rail & Right TOC (Sans 600 for clean Vietnamese diacritics) */
  .rail-section-heading,
  .page-toc-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 8px 4px;
    font-family: var(--cds-font-sans);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--cds-text-muted);
  }

  /* Right Sticky Column: Synchronized with Left Sidebar */
  .page-toc-slot {
    display: none;
    min-width: 0;
  }
  .page-toc {
    position: sticky;
    top: var(--header-height);
    height: calc(100vh - var(--header-height));
    overflow-y: auto;
    overscroll-behavior: contain;
    padding: 18px 16px 48px 14px;
    background: var(--cds-surface-0);
    border-left: 1px solid var(--cds-border-subtle);
    font-size: 13px;
    line-height: 1.4;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .page-toc-course-meta {
    display: flex;
    flex-direction: column;
    gap: 3px;
    padding: 9px 11px;
    border-radius: 8px;
    background: var(--cds-surface-1);
    border: 1px solid var(--cds-border-subtle);
  }
  .page-toc-course-kicker {
    font-family: var(--cds-font-sans);
    font-size: 10.5px;
    font-weight: 600;
    color: var(--cds-clay);
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }
  .page-toc-course-stage {
    font-size: 12.5px;
    font-weight: 500;
    color: var(--cds-text-primary);
    line-height: 1.35;
  }

  .page-toc-progress {
    height: 2px;
    width: 100%;
    background: var(--cds-border-subtle);
    border-radius: 999px;
    overflow: hidden;
    margin: -2px 0 4px;
  }
  .page-toc-progress-fill {
    height: 100%;
    width: 0%;
    background: var(--cds-clay);
    transition: width 0.16s ease-out;
  }

  .page-toc-list {
    list-style: none;
    margin: 0 0 0 6px;
    padding: 0;
    border-left: 1px solid var(--cds-border-default);
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .page-toc-link {
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-left: -1px;
    padding: 6px 10px 6px 11px;
    border-left: 2px solid transparent;
    border-radius: 0 6px 6px 0;
    color: var(--cds-text-secondary);
    text-decoration: none;
    font-size: 12.5px;
    line-height: 1.4;
    transition: color 0.16s var(--motion-ease), background 0.16s var(--motion-ease), border-color 0.16s var(--motion-ease);
  }
  .page-toc-link:hover {
    color: var(--cds-text-primary);
    background: var(--cds-fill-ghost-hover);
  }
  .page-toc-link[aria-current="location"] {
    color: var(--cds-text-primary);
    font-weight: 500;
    border-left-color: var(--cds-clay);
    background: var(--cds-surface-1);
  }
  .page-toc-code {
    font-family: var(--cds-font-mono);
    font-size: 10.5px;
    color: var(--cds-text-muted);
    font-variant-numeric: tabular-nums;
    flex-shrink: 0;
  }
  .page-toc-link[aria-current="location"] .page-toc-code {
    color: var(--cds-clay);
    font-weight: 500;
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
      transition: transform var(--motion-duration) var(--motion-ease), opacity 160ms ease;
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

  @media (min-width: 1280px) {
    .layout {
      grid-template-columns: var(--rail-width) minmax(0, 1fr) var(--toc-width);
    }
    body.rail-collapsed .layout {
      grid-template-columns: 0px minmax(0, 1fr) var(--toc-width);
    }
    body.catalog-mode .layout {
      grid-template-columns: var(--rail-width) minmax(0, 1fr);
    }
    body.catalog-mode.rail-collapsed .layout {
      grid-template-columns: 0px minmax(0, 1fr);
    }
    body:not(.catalog-mode) .page-toc-slot {
      display: block;
    }
  }

  /* Left Sidebar Curriculum Tree (Crisp Anthropic CDS Active States — Zero Curved Orange Left Bars, Zero Ellipsis Truncation) */
  .rail-nav-shortcuts {
    display: flex;
    flex-direction: column;
    gap: 3px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--cds-border-subtle);
  }
  .rail-shortcut-btn {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    min-height: 34px;
    padding: 6px 10px;
    border: 1px solid transparent;
    border-radius: 8px;
    background: transparent;
    color: var(--cds-text-secondary);
    font-size: 13px;
    font-weight: 400;
    text-align: left;
    cursor: pointer;
    transition: background 0.16s var(--motion-ease), color 0.16s var(--motion-ease), border-color 0.16s var(--motion-ease);
  }
  .rail-shortcut-btn:hover {
    background: var(--cds-fill-ghost-hover);
    color: var(--cds-text-primary);
  }
  .rail-shortcut-btn.active {
    background: var(--cds-surface-1);
    border-color: var(--cds-border-default);
    color: var(--cds-text-primary);
    font-weight: 500;
  }
  .rail-shortcut-badge {
    font-family: var(--cds-font-mono);
    font-size: 10.5px;
    color: var(--cds-text-muted);
    font-variant-numeric: tabular-nums;
  }
  .rail-shortcut-btn.active .rail-shortcut-badge {
    color: var(--cds-clay);
    font-weight: 500;
  }

  .track-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .track-group {
    padding-bottom: 2px;
  }
  .track-trigger {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    min-height: 32px;
    padding: 6px 8px;
    background: transparent;
    border: 0;
    border-radius: 7px;
    color: var(--cds-text-primary);
    font-size: 12.5px;
    font-weight: 600;
    letter-spacing: -0.005em;
    line-height: 1.3;
    text-align: left;
    cursor: pointer;
    transition: background 0.16s var(--motion-ease), color 0.16s var(--motion-ease);
  }
  .track-trigger:hover {
    background: var(--cds-fill-ghost-hover);
  }
  .track-indicator {
    color: var(--cds-text-muted);
    font-size: 13px;
    font-weight: 400;
    flex-shrink: 0;
    transition: transform 0.22s var(--motion-ease), color 0.16s var(--motion-ease);
  }
  .track-group[data-expanded="true"] .track-indicator {
    transform: rotate(180deg);
    color: var(--cds-text-primary);
  }
  .track-panel-wrap {
    display: grid;
    grid-template-rows: 0fr;
    transition: grid-template-rows 0.22s var(--motion-ease);
  }
  .track-group[data-expanded="true"] .track-panel-wrap {
    grid-template-rows: 1fr;
  }
  .track-panel-inner {
    min-height: 0;
    overflow: hidden;
  }
  .track-items {
    padding: 3px 0 6px;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .rail-item {
    display: grid;
    grid-template-columns: 32px minmax(0, 1fr) auto;
    align-items: baseline;
    gap: 6px;
    width: 100%;
    min-height: 32px;
    text-align: left;
    padding: 6px 9px;
    border: 1px solid transparent;
    border-radius: 7px;
    background: transparent;
    color: var(--cds-text-secondary);
    font-size: 13px;
    font-weight: 400;
    line-height: 1.36;
    cursor: pointer;
    transition: background 0.16s var(--motion-ease), color 0.16s var(--motion-ease), border-color 0.16s var(--motion-ease);
  }
  .rail-item:hover {
    background: var(--cds-fill-ghost-hover);
    color: var(--cds-text-primary);
  }
  .rail-item[aria-current="page"] {
    background: var(--cds-surface-1);
    border-color: var(--cds-border-default);
    color: var(--cds-text-primary);
    font-weight: 500;
  }
  .rail-code {
    font-family: var(--cds-font-mono);
    font-size: 11px;
    color: var(--cds-text-muted);
    font-variant-numeric: tabular-nums;
  }
  .rail-item[aria-current="page"] .rail-code {
    color: var(--cds-clay);
    font-weight: 500;
  }
  .rail-item-title {
    min-width: 0;
    white-space: normal;
    overflow-wrap: break-word;
    line-height: 1.34;
  }
  .rail-item-dot {
    width: 6px;
    height: 6px;
    border-radius: 999px;
    background: var(--cds-clay);
    opacity: 0.75;
    flex-shrink: 0;
    align-self: center;
  }
  .rail-item[aria-current="page"] .rail-item-dot {
    opacity: 1;
  }

  /* Nested Stage Subtree under Active Course in Left Sidebar (Mirrors Right TOC) */
  .rail-stage-sublist {
    list-style: none;
    margin: 3px 0 8px 15px;
    padding: 0;
    border-left: 1px solid var(--cds-border-default);
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .rail-stage-btn {
    display: flex;
    align-items: baseline;
    gap: 8px;
    width: calc(100% + 1px);
    margin-left: -1px;
    min-height: 28px;
    padding: 5px 9px 5px 11px;
    border: 0;
    border-left: 2px solid transparent;
    border-radius: 0 6px 6px 0;
    background: transparent;
    color: var(--cds-text-secondary);
    font-size: 12.5px;
    line-height: 1.36;
    text-align: left;
    cursor: pointer;
    transition: color 0.16s var(--motion-ease), background 0.16s var(--motion-ease), border-color 0.16s var(--motion-ease);
  }
  .rail-stage-btn:hover {
    color: var(--cds-text-primary);
    background: var(--cds-fill-ghost-hover);
  }
  .rail-stage-btn.active {
    color: var(--cds-text-primary);
    font-weight: 500;
    border-left-color: var(--cds-clay);
    background: var(--cds-surface-1);
  }
  .rail-stage-idx {
    font-family: var(--cds-font-mono);
    font-size: 10.5px;
    color: var(--cds-text-muted);
    font-variant-numeric: tabular-nums;
    flex-shrink: 0;
  }
  .rail-stage-btn.active .rail-stage-idx {
    color: var(--cds-clay);
    font-weight: 500;
  }

  /* ==========================================================================
     4. CLAUDE ACADEMY <ContentHero> SWATCH BANNER, STACKED ROADMAP & PROSE
     ========================================================================== */
  .main-view {
    min-width: 0;
    padding: 28px var(--page-gutter) 110px;
  }
  .article-wrap {
    width: 100%;
    max-width: var(--article-max);
    margin-inline: auto;
  }

  .lesson-header {
    position: relative;
    overflow: hidden;
    border-radius: 16px;
    background: color-mix(in oklab, var(--swatch-band, var(--cds-surface-1)) 46%, var(--cds-surface-1));
    box-shadow: var(--cds-shadow-card-ring), var(--cds-shadow-hero-edge);
    padding: clamp(22px, 3vw, 32px);
    margin: 0 auto 32px;
  }
  .lesson-hero-dots {
    position: absolute;
    inset: 0;
    pointer-events: none;
    background-image: radial-gradient(circle, color-mix(in oklab, var(--swatch-0, #141413) 24%, transparent) 1.25px, transparent 1.25px);
    background-size: 14px 14px;
    -webkit-mask-image: radial-gradient(ellipse 75% 78% at 76% 42%, #000 14%, transparent 70%);
    mask-image: radial-gradient(ellipse 75% 78% at 76% 42%, #000 14%, transparent 70%);
  }
  .lesson-header-grid {
    position: relative;
    z-index: 2;
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 24px;
    align-items: center;
  }
  @media (min-width: 960px) {
    .lesson-header-grid.has-artwork {
      grid-template-columns: minmax(0, 1fr) 196px;
    }
  }
  .lesson-hero-art {
    display: none;
    position: relative;
    width: 196px;
    height: 186px;
    align-items: center;
    justify-content: center;
    user-select: none;
    pointer-events: none;
  }
  @media (min-width: 960px) {
    .lesson-hero-art {
      display: flex;
    }
  }
  .cds-badge-seal {
    position: relative;
    width: 184px;
    height: 184px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    filter: drop-shadow(0 10px 24px rgba(20, 20, 19, 0.08));
  }
  .cds-badge-seal-svg {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
  }
  .cds-badge-seal-inner {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 22px 24px 18px;
    gap: 5px;
  }
  .cds-badge-seal-kicker {
    font-family: var(--cds-font-sans);
    font-size: 8.5px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #5e5d59;
    line-height: 1;
  }
  .cds-badge-seal-picto {
    width: 64px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .cds-badge-seal-picto svg {
    width: 100%;
    height: 100%;
  }
  .cds-badge-seal-title {
    font-family: var(--cds-font-serif);
    font-size: 11px;
    font-weight: 500;
    line-height: 1.22;
    color: #141413;
    max-width: 128px;
  }

  .lesson-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    line-height: 1.3;
    color: var(--cds-text-secondary);
    margin-bottom: 12px;
  }
  .cds-swatch-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: 6px;
    border: 1px solid color-mix(in oklab, var(--swatch-0, var(--cds-text-primary)) 26%, transparent);
    background: color-mix(in oklab, var(--swatch-0, var(--cds-text-primary)) 9%, transparent);
    color: var(--cds-text-primary);
    font-size: 12px;
    font-weight: 500;
    text-decoration: none;
    font-variant-numeric: tabular-nums;
  }
  a.cds-swatch-pill:hover {
    background: color-mix(in oklab, var(--swatch-0, var(--cds-text-primary)) 15%, transparent);
  }

  .lesson-title {
    font-family: var(--cds-font-serif);
    font-size: clamp(25px, 2.4vw, 33px);
    font-weight: 400;
    line-height: 1.16;
    letter-spacing: -0.02em;
    color: var(--cds-text-primary);
    margin: 0 0 8px;
  }
  .lesson-stage-subtitle {
    font-family: var(--cds-font-sans);
    font-size: clamp(15px, 1.25vw, 17px);
    font-weight: 500;
    line-height: 1.4;
    color: var(--swatch-fg, var(--cds-text-primary));
    margin: 0 0 10px;
  }
  .lesson-lead {
    font-family: var(--cds-font-sans);
    font-size: 15px;
    color: var(--cds-text-secondary);
    line-height: 1.58;
    margin: 0;
    max-width: 44rem;
  }

  /* Vertically Stacked Stages Roadmap (.stage-pills-bar) + Stage Objectives Grid */
  .lesson-roadmap-grid {
    position: relative;
    z-index: 2;
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 14px;
    margin-top: 20px;
    padding-top: 18px;
    border-top: 1px solid color-mix(in oklab, var(--swatch-0, var(--cds-text-primary)) 15%, transparent);
  }
  @media (min-width: 860px) {
    .lesson-roadmap-grid {
      grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);
      align-items: start;
    }
  }

  .stage-pills-bar {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: 5px;
    background: color-mix(in oklab, var(--cds-surface-0) 76%, transparent);
    border: 1px solid color-mix(in oklab, var(--swatch-0, var(--cds-text-primary)) 16%, transparent);
    border-radius: 12px;
    padding: 12px;
  }
  .stage-pills-label {
    font-family: var(--cds-font-sans);
    font-size: 10.5px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--cds-text-muted);
    padding: 0 4px 4px;
  }
  .stage-pill,
  .stage-pill-btn {
    appearance: none;
    display: grid;
    grid-template-columns: 68px minmax(0, 1fr) auto;
    align-items: center;
    gap: 8px;
    width: 100%;
    min-height: 34px;
    padding: 6px 10px;
    border-radius: 8px;
    border: 1px solid transparent;
    background: transparent;
    color: var(--cds-text-secondary);
    font-family: var(--cds-font-sans);
    font-size: 13px;
    font-weight: 400;
    line-height: 1.32;
    text-align: left;
    cursor: pointer;
    transition: background 0.16s var(--motion-ease), border-color 0.16s var(--motion-ease), color 0.16s var(--motion-ease);
  }
  .stage-pill:hover,
  .stage-pill-btn:hover {
    background: var(--cds-surface-0);
    color: var(--cds-text-primary);
  }
  .stage-pill.active,
  .stage-pill-btn.active {
    background: var(--cds-surface-0);
    border-color: color-mix(in oklab, var(--swatch-0, var(--cds-text-primary)) 26%, transparent);
    box-shadow: 0 1px 2px rgba(20, 20, 19, 0.05);
    color: var(--cds-text-primary);
    font-weight: 500;
  }
  .stage-pill-num {
    font-family: var(--cds-font-mono);
    font-size: 11px;
    font-weight: 500;
    font-variant-numeric: tabular-nums;
    color: var(--cds-text-muted);
    align-self: flex-start;
    padding-top: 1px;
  }
  .stage-pill-btn.active .stage-pill-num {
    color: var(--cds-clay);
  }
  .stage-pill-title {
    min-width: 0;
    line-height: 1.35;
  }
  .stage-pill-state {
    font-family: var(--cds-font-sans);
    font-size: 11px;
    color: var(--cds-text-muted);
    white-space: nowrap;
    align-self: flex-start;
    padding-top: 1px;
  }
  .stage-pill-btn.active .stage-pill-state {
    color: var(--cds-clay);
    font-weight: 600;
  }

  .lesson-objectives-card {
    display: flex;
    flex-direction: column;
    gap: 6px;
    background: color-mix(in oklab, var(--cds-surface-0) 76%, transparent);
    border: 1px solid color-mix(in oklab, var(--swatch-0, var(--cds-text-primary)) 16%, transparent);
    border-radius: 12px;
    padding: 12px 14px;
  }
  .lesson-objectives-title {
    font-family: var(--cds-font-sans);
    font-size: 10.5px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--cds-text-muted);
    margin-bottom: 2px;
  }
  .lesson-objectives-list {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  .lesson-objective-link {
    display: flex;
    align-items: baseline;
    gap: 8px;
    padding: 4px 6px;
    border-radius: 6px;
    font-size: 12.5px;
    line-height: 1.38;
    color: var(--cds-text-secondary);
    text-decoration: none;
    transition: background 0.14s ease, color 0.14s ease;
  }
  .lesson-objective-link:hover {
    background: var(--cds-surface-0);
    color: var(--cds-text-primary);
  }
  .lesson-objective-code {
    font-family: var(--cds-font-sans);
    font-size: 11px;
    font-weight: 600;
    color: var(--cds-clay);
    flex-shrink: 0;
  }

  /* Editorial Prose & Harmonious Anthropic Serif + Sans Pairing */
  .prose {
    display: block;
    width: 100%;
    font-family: var(--cds-font-sans);
    font-size: 16.5px;
    line-height: 1.68;
    letter-spacing: -0.003em;
    color: var(--cds-text-body);
  }
  .prose > p:first-child:has(+ h2),
  .prose > h2 + p:has(> em:only-child) {
    display: none;
  }
  .prose hr {
    border: 0;
    border-top: 1px solid var(--cds-border-subtle);
    margin: 36px auto;
    max-width: var(--reading-measure);
  }
  .prose :is(h2, h3, h4, .summary-section, .lesson-section)[id] {
    scroll-margin-block-start: calc(var(--header-height) + 22px);
  }
  .prose > :is(p, ul, ol, blockquote, h2, h3, h4, .callout, .summary-section),
  .lesson-section > :is(p, ul, ol, blockquote, h2, h3, h4, .callout, .summary-section) {
    max-width: var(--reading-measure);
    margin-inline: auto;
  }
  .prose h2 {
    font-family: var(--cds-font-serif);
    font-size: clamp(22px, 1.9vw, 26px);
    font-weight: 400;
    line-height: 1.24;
    letter-spacing: -0.018em;
    margin: 44px auto 14px;
    padding-top: 24px;
    border-top: 1px solid var(--cds-border-subtle);
    color: var(--cds-text-primary);
  }
  .prose > h2:first-of-type,
  .lesson-section:first-of-type > h2:first-child {
    margin-top: 4px;
    padding-top: 0;
    border-top: 0;
  }
  .prose h3 {
    font-family: var(--cds-font-sans);
    font-size: clamp(17.5px, 1.35vw, 19.5px);
    font-weight: 600;
    line-height: 1.35;
    letter-spacing: -0.012em;
    margin: 28px auto 10px;
    color: var(--cds-text-primary);
  }
  .prose h4 {
    font-family: var(--cds-font-sans);
    font-size: 16px;
    font-weight: 600;
    line-height: 1.42;
    margin: 20px auto 8px;
    color: var(--cds-text-primary);
  }
  .prose p {
    margin: 0 auto 15px;
  }
  .prose ul, .prose ol {
    margin: 0 auto 18px;
    padding-left: 22px;
  }
  .prose li {
    margin-bottom: 8px;
  }
  .prose li ul {
    margin-top: 6px;
  }

  /* Subtle Borderless Inline Code */
  .prose code,
  .lesson-lead code,
  .spine-overview-body code {
    font-family: var(--cds-font-mono);
    font-size: 0.85em;
    font-weight: 400;
    line-height: 1.35;
    padding: 0.12em 0.38em;
    background: var(--code-inline-bg);
    border: 0;
    border-radius: 4px;
    color: var(--cds-text-primary);
    overflow-wrap: anywhere;
    word-break: break-word;
  }
  .prose :is(h1, h2, h3, h4) code {
    font-size: 0.86em;
    padding: 0.08em 0.32em;
  }

  .prose pre:not(.ascii-diagram) {
    margin: 18px auto 24px;
    padding: 15px 18px;
    background: var(--cds-surface-1);
    box-shadow: var(--cds-shadow-card-ring);
    border: 0;
    border-radius: 10px;
    overflow-x: auto;
    max-width: var(--reading-measure);
    font-size: 13px;
    line-height: 1.55;
  }
  .prose pre:not(.ascii-diagram) code {
    padding: 0;
    background: transparent;
    border: 0;
    overflow-wrap: normal;
    word-break: normal;
    white-space: pre;
  }

  /* Centered Tables & Visual Blocks */
  .table-wrap {
    overflow-x: auto;
    max-width: var(--article-max);
    margin: 20px auto 28px;
    border-radius: var(--cds-radius-card);
    background: var(--cds-surface-1);
    box-shadow: var(--cds-shadow-card-ring);
  }
  table.clean-table {
    width: 100%;
    border-collapse: collapse;
    font-family: var(--cds-font-sans);
    font-size: 14px;
    line-height: 1.55;
  }
  table.clean-table th,
  table.clean-table td {
    padding: 11px 14px;
    text-align: left;
    vertical-align: top;
    border-bottom: 1px solid var(--cds-border-subtle);
  }
  table.clean-table th {
    background: var(--cds-surface-2);
    font-size: 12.5px;
    font-weight: 500;
    color: var(--cds-text-primary);
  }
  table.clean-table tr:last-child td {
    border-bottom: 0;
  }

  /* ==========================================================================
     5. CLAUDE ACADEMY "IN THIS LESSON" CARD & COLORED ASCII APP-WINDOW
     ========================================================================== */
  .spine-overview-card {
    max-width: var(--reading-measure);
    margin: 20px auto 28px;
    padding: 16px 20px;
    background: var(--cds-surface-1);
    border-radius: var(--cds-radius-card);
    box-shadow: var(--cds-shadow-card-ring);
    border: 1px solid var(--cds-border-default);
  }
  .spine-overview-head {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 8px;
  }
  .spine-overview-title-wrap {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
  }
  .spine-overview-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 2px 8px;
    border-radius: 5px;
    font-family: var(--cds-font-sans);
    font-size: 10.5px;
    font-weight: 600;
    background: var(--glossary-badge-bg);
    color: var(--glossary-badge-text);
  }
  .spine-overview-title {
    font-family: var(--cds-font-sans);
    font-size: 14px;
    font-weight: 600;
    color: var(--cds-text-primary);
  }
  .spine-overview-sub {
    font-size: 11.5px;
    color: var(--cds-text-muted);
  }
  .spine-overview-body {
    display: block;
    font-size: 14px;
    line-height: 1.58;
    color: var(--cds-text-secondary);
  }

  /* Colored-ASCII Visual Sandbox Card (Centered & Balanced) */
  .visual-card {
    container-type: inline-size;
    max-width: var(--article-max);
    margin: 24px auto 30px;
    border-radius: var(--cds-radius-card);
    background: var(--cds-surface-1);
    box-shadow: var(--cds-shadow-card-ring);
    border: 0;
    overflow: hidden;
  }
  .visual-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding: 9px 14px;
    background: var(--cds-surface-1);
    border-bottom: 1px solid var(--cds-border-subtle);
    line-height: 1.3;
  }
  .visual-bar-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: var(--cds-font-sans);
    font-size: 13px;
    font-weight: 500;
    color: var(--cds-text-primary);
    min-width: 0;
  }
  .visual-window-dots {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    flex-shrink: 0;
  }
  .visual-window-dots span {
    width: 7px;
    height: 7px;
    border-radius: 999px;
    background: var(--cds-border-strong);
  }
  .visual-controls {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
  }
  .visual-engine-tag {
    font-family: var(--cds-font-mono);
    font-size: 11px;
    color: var(--cds-text-muted);
    padding: 2px 7px;
    border-radius: 5px;
    background: var(--cds-surface-0);
    border: 1px solid var(--cds-border-subtle);
  }
  .visual-pane {
    display: flex;
    justify-content: center;
    background: var(--code-block-bg);
    overflow-x: auto;
  }

  pre.ascii-diagram {
    margin: 0 auto;
    padding: 18px 20px;
    background: var(--code-block-bg);
    border: 0;
    font-family: "JetBrains Mono", "anthropic-mono", "SFMono-Regular", ui-monospace, monospace;
    font-size: clamp(8.5px, calc(156cqi / var(--ascii-cols, 96)), 13.5px);
    font-weight: 400;
    font-style: normal;
    line-height: 1.34;
    letter-spacing: 0;
    font-variant-ligatures: none;
    font-feature-settings: "liga" 0, "calt" 0;
    color: var(--cds-text-primary);
    overflow-x: auto;
    white-space: pre;
    tab-size: 4;
  }
  body.rail-collapsed pre.ascii-diagram {
    font-size: clamp(9px, calc(156cqi / var(--ascii-cols, 96)), 14px);
  }
  pre.ascii-diagram .ac-border { color: var(--ac-border); }
  pre.ascii-diagram .ac-shadow { color: var(--ac-shadow); }
  pre.ascii-diagram .ac-header { color: var(--ac-header); }
  pre.ascii-diagram .ac-flow   { color: var(--ac-flow); }
  pre.ascii-diagram .ac-ok     { color: var(--ac-ok); }
  pre.ascii-diagram .ac-warn   { color: var(--ac-warn); }
  pre.ascii-diagram .ac-danger { color: var(--ac-danger); }
  pre.ascii-diagram .ac-muted  { color: var(--ac-muted); }

  @keyframes acFlowPulse {
    0%, 100% { opacity: 1; filter: brightness(1); }
    50% { opacity: 0.68; filter: brightness(1.38); }
  }
  body:not(.ascii-anim-paused) .visual-card[data-flagship="true"] pre.ascii-diagram .ac-flow {
    animation: acFlowPulse 1.8s steps(3, end) infinite;
  }
  @media (prefers-reduced-motion: reduce) {
    .visual-card[data-flagship="true"] pre.ascii-diagram .ac-flow {
      animation: none !important;
    }
  }

  .visual-caption {
    padding: 10px 16px;
    font-size: 13px;
    line-height: 1.5;
    color: var(--cds-text-secondary);
    border-top: 1px solid var(--cds-border-subtle);
    background: var(--cds-surface-1);
    text-align: center;
  }

  .summary-section {
    margin: 36px auto 24px;
    padding-top: 20px;
    border-top: 1px solid var(--cds-border-default);
  }
  .summary-section h2 {
    margin-top: 0;
    border-top: 0;
    padding-top: 0;
  }

  /* Lesson Pager & Course Catalog & Glossary Dictionary View */
  .lesson-pager {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
    max-width: var(--reading-measure);
    margin: 48px auto 16px;
    padding-top: 24px;
    border-top: 1px solid var(--cds-border-subtle);
  }
  .lesson-pager-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 6px;
    padding: 16px 18px;
    border-radius: var(--cds-radius-card);
    border: 0;
    background: var(--cds-surface-1);
    box-shadow: var(--cds-shadow-card-ring);
    color: var(--cds-text-primary);
    text-align: left;
    text-decoration: none;
    cursor: pointer;
    transition: background 0.16s var(--motion-ease), transform 0.16s var(--motion-ease);
  }
  .lesson-pager-card:hover {
    background: var(--cds-surface-2);
    transform: translateY(-1px);
  }
  .lesson-pager-card.is-next {
    text-align: right;
  }
  .lesson-pager-dir {
    font-family: var(--cds-font-mono);
    font-size: 11.5px;
    font-weight: 500;
    color: var(--cds-text-muted);
  }
  .lesson-pager-title {
    font-family: var(--cds-font-sans);
    font-size: 14.5px;
    font-weight: 500;
    color: var(--cds-text-primary);
    line-height: 1.38;
  }

  .catalog-hero {
    position: relative;
    overflow: hidden;
    border-radius: 16px;
    padding: clamp(24px, 3.2vw, 34px);
    margin-bottom: 32px;
    background: color-mix(in oklab, var(--swatch-band, var(--cds-surface-1)) 46%, var(--cds-surface-1));
    box-shadow: var(--cds-shadow-card-ring), var(--cds-shadow-hero-edge);
  }
  .catalog-kicker {
    display: inline-block;
    font-family: var(--cds-font-sans);
    font-size: 11.5px;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: var(--swatch-fg, var(--cds-clay));
    margin-bottom: 8px;
  }
  .catalog-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 18px;
    margin: 16px 0 36px;
  }
  .catalog-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 14px;
    padding: 20px;
    border-radius: 14px;
    border: 0;
    background: var(--cds-surface-1);
    box-shadow: var(--cds-shadow-card-ring);
    overflow: hidden;
    transition: background 0.16s var(--motion-ease), transform 0.16s var(--motion-ease), box-shadow 0.16s var(--motion-ease);
  }
  .catalog-card.has-thumb {
    padding: 0;
    gap: 0;
  }
  .catalog-card:hover {
    background: var(--cds-surface-2);
    transform: translateY(-2px);
  }
  .cds-content-thumb {
    position: relative;
    height: 136px;
    width: 100%;
    overflow: hidden;
    background-color: var(--swatch-band, var(--cds-surface-2));
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .cds-thumb-mask {
    position: absolute;
    inset: 0;
    pointer-events: none;
    background-color: color-mix(in oklab, var(--swatch-0, #141413) 32%, transparent);
    -webkit-mask-size: 200% auto;
    mask-size: 200% auto;
    -webkit-mask-position: center;
    mask-position: center;
    -webkit-mask-repeat: no-repeat;
    mask-repeat: no-repeat;
    opacity: 0.52;
  }
  .cds-thumb-stack {
    position: relative;
    z-index: 2;
    width: 128px;
    height: 94px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .cds-thumb-fan {
    position: absolute;
    width: 88px;
    height: 74px;
    border-radius: 10px;
    background: color-mix(in oklab, var(--swatch-band) 55%, var(--cds-surface-0, #faf9f5));
    border: 1px solid color-mix(in oklab, var(--swatch-0, #141413) 26%, transparent);
    transition: transform 0.26s var(--motion-ease);
  }
  .cds-thumb-fan.is-left {
    transform: translate(-10px, 5px) rotate(-5deg);
  }
  .cds-thumb-fan.is-right {
    transform: translate(10px, 5px) rotate(5deg);
  }
  .catalog-card:hover .cds-thumb-fan.is-left {
    transform: translate(-15px, 3px) rotate(-8deg);
  }
  .catalog-card:hover .cds-thumb-fan.is-right {
    transform: translate(15px, 3px) rotate(8deg);
  }
  .cds-thumb-front {
    position: relative;
    z-index: 3;
    width: 116px;
    height: 86px;
    border-radius: 11px;
    background: var(--cds-surface-0, #faf9f5);
    border: 1px solid color-mix(in oklab, var(--swatch-0, #141413) 28%, transparent);
    box-shadow: 0 6px 16px rgba(20, 20, 19, 0.08);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 8px 8px 6px;
    transition: transform 0.26s var(--motion-ease);
  }
  .catalog-card:hover .cds-thumb-front {
    transform: translateY(-2px);
  }
  .cds-thumb-picto {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .cds-thumb-picto svg {
    width: 100%;
    height: 100%;
  }
  .cds-thumb-meta {
    font-family: var(--cds-font-sans);
    font-size: 9px;
    font-weight: 500;
    color: var(--cds-text-secondary);
    white-space: nowrap;
  }
  .catalog-card-body {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex: 1;
    gap: 12px;
    padding: 16px 18px 18px;
  }
  .catalog-card-top {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
  }
  .catalog-code-pill {
    font-family: var(--cds-font-mono);
    font-size: 11px;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 6px;
    background: var(--cds-surface-0);
    color: var(--cds-text-primary);
    box-shadow: var(--cds-shadow-card-ring);
  }
  .catalog-status-pill {
    font-size: 11.5px;
    font-weight: 500;
    color: var(--cds-clay);
    white-space: nowrap;
  }
  .catalog-card h3 {
    margin: 8px 0 6px;
    font-family: var(--cds-font-serif);
    font-size: 18.5px;
    font-weight: 400;
    line-height: 1.26;
    letter-spacing: -0.015em;
    min-height: 2.52em;
    display: flex;
    align-items: flex-start;
    text-wrap: balance;
  }
  .catalog-syllabus-meta {
    display: flex;
    flex-direction: column;
    gap: 6px;
    font-size: 13px;
    line-height: 1.5;
    color: var(--cds-text-secondary);
    margin-top: 2px;
  }
  .catalog-syllabus-row {
    display: grid;
    grid-template-columns: 58px minmax(0, 1fr);
    align-items: baseline;
    gap: 8px;
  }
  .catalog-syllabus-tag {
    font-family: var(--cds-font-sans);
    font-size: 10.5px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--cds-text-muted);
    flex-shrink: 0;
  }
  .catalog-card-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding-top: 10px;
    border-top: 1px solid var(--cds-border-subtle);
    font-size: 12px;
    color: var(--cds-text-muted);
  }
  .catalog-card-footer code {
    font-family: var(--cds-font-mono);
    font-size: 11px;
    color: var(--cds-text-secondary);
    line-height: 1.4;
    white-space: normal;
    word-break: break-word;
  }
  .catalog-card-footer .ui-btn {
    flex-shrink: 0;
  }

  /* Glossary Dictionary View (#/glossary) */
  .glossary-ai-ask-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 16px;
    padding: 14px 18px;
    background: color-mix(in oklab, var(--accent-soft) 55%, var(--cds-surface-1));
    border: 1px solid color-mix(in oklab, var(--cds-clay) 28%, var(--cds-border-default));
    border-radius: var(--cds-radius-card);
  }
  .glossary-ai-ask-label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: var(--cds-font-sans);
    font-size: 13.5px;
    font-weight: 600;
    color: var(--cds-text-primary);
  }
  .glossary-ai-ask-form {
    display: flex;
    flex: 1 1 360px;
    align-items: center;
    gap: 8px;
  }
  .glossary-ai-ask-input {
    appearance: none;
    flex: 1;
    height: 36px;
    padding: 0 12px;
    border-radius: 8px;
    border: 1px solid var(--cds-border-default);
    background: var(--cds-surface-0);
    color: var(--cds-text-primary);
    font-family: var(--cds-font-sans);
    font-size: 13.5px;
    outline: none;
  }
  .glossary-ai-ask-input:focus {
    border-color: var(--cds-clay);
  }
  .glossary-dict-controls,
  .glossary-filter-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 24px;
    padding: 14px 16px;
    background: var(--cds-surface-1);
    box-shadow: var(--cds-shadow-card-ring);
    border-radius: var(--cds-radius-card);
  }
  .glossary-dict-search,
  .glossary-search-input {
    appearance: none;
    flex: 1 1 280px;
    height: 36px;
    padding: 0 12px;
    border-radius: 8px;
    border: 1px solid var(--cds-border-default);
    background: var(--cds-surface-0);
    color: var(--cds-text-primary);
    font-family: var(--cds-font-sans);
    font-size: 13.5px;
    outline: none;
  }
  .glossary-dict-search:focus,
  .glossary-search-input:focus {
    border-color: var(--cds-clay);
  }
  .glossary-filter-pills {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 6px;
  }
  .glossary-filter-pill {
    appearance: none;
    height: 30px;
    padding: 0 11px;
    border-radius: 8px;
    border: 1px solid var(--cds-border-subtle);
    background: var(--cds-surface-0);
    color: var(--cds-text-secondary);
    font-family: var(--cds-font-sans);
    font-size: 12.5px;
    font-weight: 400;
    cursor: pointer;
    transition: background 0.14s, color 0.14s;
  }
  .glossary-filter-pill:hover {
    background: var(--cds-fill-ghost-hover);
    color: var(--cds-text-primary);
  }
  .glossary-filter-pill.active {
    background: var(--cds-fill-primary);
    border-color: var(--cds-fill-primary);
    color: var(--cds-text-on-primary);
    font-weight: 500;
  }
  .glossary-dict-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 14px;
  }
  .glossary-dict-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 12px;
    padding: 18px 20px;
    border-radius: var(--cds-radius-card);
    background: var(--cds-surface-1);
    box-shadow: var(--cds-shadow-card-ring);
    cursor: pointer;
    transition: background 0.16s var(--motion-ease), transform 0.16s var(--motion-ease), box-shadow 0.16s var(--motion-ease);
  }
  .glossary-dict-card:hover {
    background: var(--cds-surface-2);
    transform: translateY(-2px);
    box-shadow: 0 0 0 1px var(--cds-clay), 0 8px 20px rgba(20, 20, 19, 0.06);
  }
  .glossary-dict-card-top {
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin-bottom: 6px;
  }
  .glossary-dict-name,
  .glossary-dict-card h3 {
    margin: 0;
    font-family: var(--cds-font-sans);
    font-size: 15.5px;
    font-weight: 600;
    line-height: 1.32;
    color: var(--cds-text-primary);
  }
  .glossary-dict-cat {
    align-self: flex-start;
    font-family: var(--cds-font-sans);
    font-size: 10.5px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--glossary-badge-text);
    background: var(--glossary-badge-bg);
    padding: 2px 7px;
    border-radius: 4px;
  }
  .glossary-dict-desc {
    margin: 0;
    font-size: 13.5px;
    line-height: 1.58;
    color: var(--cds-text-secondary);
  }
  .glossary-dict-code {
    margin: 0 0 10px;
    padding: 8px 10px;
    background: var(--cds-surface-0);
    border: 1px solid var(--cds-border-subtle);
    border-radius: 6px;
    font-family: "anthropic-mono", "anthropic-sans", ui-monospace, monospace;
    font-size: 11.5px;
    line-height: 1.45;
    color: var(--cds-text-primary);
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-word;
  }
  .glossary-dict-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding-top: 8px;
    border-top: 1px solid var(--cds-border-subtle);
    font-size: 11.5px;
    color: var(--cds-text-muted);
  }
  .glossary-dict-ai-cta {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-family: var(--cds-font-sans);
    font-size: 12px;
    font-weight: 600;
    color: var(--cds-clay);
  }

  /* ==========================================================================
     6. COMMAND PALETTE MODAL (⌘K) & FULLSCREEN DIAGRAM MODAL
     ========================================================================== */
  .modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(20, 20, 19, 0.55);
    backdrop-filter: blur(3px);
    -webkit-backdrop-filter: blur(3px);
    z-index: 110;
    display: none;
    align-items: flex-start;
    justify-content: center;
    padding: 8vh 16px 24px;
  }
  .modal-backdrop.open {
    display: flex;
  }

  .cmd-dialog {
    width: min(640px, 100%);
    background: var(--cds-surface-0);
    border-radius: var(--cds-radius-card);
    box-shadow: var(--cds-shadow-modal);
    overflow: hidden;
    line-height: 1.3;
  }
  .cmd-input-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 14px;
    border-bottom: 1px solid var(--cds-border-subtle);
    background: var(--cds-surface-0);
  }
  .cmd-input {
    flex: 1;
    border: 0;
    background: transparent;
    color: var(--cds-text-primary);
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
    border-radius: 8px;
    background: transparent;
    color: var(--cds-text-primary);
    font-size: 13px;
    text-align: left;
    cursor: pointer;
  }
  .cmd-item:hover,
  .cmd-item.selected {
    background: var(--cds-fill-ghost-hover);
  }
  .cmd-item-left {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
  }
  .cmd-item-sub {
    font-size: 11.5px;
    color: var(--cds-text-muted);
  }
  .cmd-item-kind {
    font-size: 11px;
    color: var(--cds-text-muted);
    flex-shrink: 0;
  }
  .cmd-footer {
    display: flex;
    justify-content: space-between;
    padding: 8px 14px;
    font-size: 11px;
    color: var(--cds-text-muted);
    background: var(--cds-surface-1);
    border-top: 1px solid var(--cds-border-subtle);
  }

  /* Fullscreen Diagram Expand Dialog */
  .expand-dialog {
    width: min(1760px, 96vw);
    height: 86vh;
    background: var(--cds-surface-0);
    border-radius: var(--cds-radius-card);
    box-shadow: var(--cds-shadow-modal);
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
    padding: 10px 16px;
    background: var(--cds-surface-1);
    border-bottom: 1px solid var(--cds-border-subtle);
    font-size: 13.5px;
    font-weight: 500;
  }
  .expand-body {
    flex: 1;
    min-height: 0;
    overflow: auto;
    background: var(--code-block-bg);
    display: flex;
    flex-direction: column;
  }
  .expand-body pre.ascii-diagram {
    font-size: 13.5px;
    line-height: 1.32;
    padding: 24px;
  }

  .toast {
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 9px 14px;
    background: var(--cds-surface-1);
    box-shadow: var(--cds-shadow-popover);
    border-radius: 8px;
    color: var(--cds-text-primary);
    font-size: 13px;
    line-height: 1.3;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.15s;
    z-index: 130;
  }
  .toast.show {
    opacity: 1;
  }

  /* ==========================================================================
     7. EDITORIAL GLOSSARY TRIGGER & CENTERED ANTHROPIC-STYLE AI MODAL
     ========================================================================== */
  .glossary-term {
    cursor: pointer;
    position: relative;
    border-bottom: 1px dotted var(--glossary-underline);
    padding-bottom: 0;
    transition: color 0.14s ease, background-color 0.14s ease, border-color 0.14s ease;
  }
  .glossary-term:hover,
  .glossary-term:focus-visible,
  .glossary-term.glossary-active,
  .glossary-term.glossary-pinned {
    color: var(--cds-text-primary);
    background-color: var(--accent-soft);
    border-bottom: 1px solid var(--cds-clay);
    border-radius: 3px;
    outline: none;
  }

  .glossary-modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(20, 20, 19, 0.48);
    backdrop-filter: blur(3px);
    -webkit-backdrop-filter: blur(3px);
    z-index: 142;
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transition: opacity 0.18s var(--motion-ease), visibility 0.18s;
  }
  .glossary-modal-backdrop.open {
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
  }

  .glossary-popover {
    position: fixed;
    top: 50% !important;
    left: 50% !important;
    width: min(640px, calc(100vw - 24px));
    max-height: min(82vh, 720px);
    overflow-y: auto;
    z-index: 145;
    background: var(--cds-surface-0);
    box-shadow: var(--cds-shadow-modal);
    border: 1px solid var(--cds-border-default);
    border-radius: 16px;
    padding: 20px 24px 18px;
    color: var(--cds-text-primary);
    font-family: var(--cds-font-sans);
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transform: translate(-50%, -48%) scale(0.97);
    transition: opacity 0.18s var(--motion-ease), transform 0.18s var(--motion-ease), visibility 0.18s;
  }
  .glossary-popover.open {
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
    transform: translate(-50%, -50%) scale(1);
  }
  .glossary-popover.pinned {
    box-shadow: 0 0 0 1px var(--cds-border-strong), var(--cds-shadow-modal);
  }
  .glossary-pop-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 10px;
  }
  .glossary-pop-meta-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 6px;
    margin-bottom: 6px;
  }
  .glossary-pop-meta {
    display: inline-block;
    font-family: var(--cds-font-sans);
    font-size: 10.5px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--glossary-badge-text);
    background: var(--glossary-badge-bg);
    padding: 2px 8px;
    border-radius: 4px;
  }
  .glossary-pop-cache-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-family: var(--cds-font-sans);
    font-size: 10.5px;
    font-weight: 500;
    padding: 2px 7px;
    border-radius: 4px;
    background: var(--cds-surface-2);
    color: var(--cds-text-secondary);
  }
  .glossary-pop-title {
    font-family: var(--cds-font-serif);
    font-size: 21px;
    font-weight: 400;
    line-height: 1.25;
    color: var(--cds-text-primary);
    margin: 0;
    letter-spacing: -0.015em;
  }
  .glossary-pop-close {
    appearance: none;
    border: 0;
    background: var(--cds-fill-ghost-hover);
    color: var(--cds-text-muted);
    width: 30px;
    height: 30px;
    border-radius: 8px;
    font-size: 12px;
    line-height: 1;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: background 0.12s, color 0.12s;
  }
  .glossary-pop-close:hover {
    background: var(--cds-fill-ghost-active);
    color: var(--cds-text-primary);
  }
  .glossary-pop-intuition {
    font-size: 14px;
    line-height: 1.62;
    color: var(--cds-text-body);
    margin: 0 0 10px;
  }
  .glossary-pop-code {
    display: block;
    font-family: "anthropic-mono", "anthropic-sans", ui-monospace, monospace;
    font-size: 12px;
    line-height: 1.5;
    color: var(--cds-text-primary);
    background: var(--cds-surface-1);
    border: 1px solid var(--cds-border-subtle);
    border-radius: 8px;
    padding: 9px 12px;
    white-space: pre-wrap;
    word-break: break-word;
    margin-bottom: 12px;
  }
  .glossary-ai-box {
    margin: 12px 0;
    padding: 14px 16px;
    border-radius: 12px;
    background: var(--cds-surface-1);
    border: 1px solid var(--cds-border-subtle);
  }
  .glossary-ai-box-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--cds-border-subtle);
  }
  .glossary-ai-box-title {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: var(--cds-font-sans);
    font-size: 12px;
    font-weight: 600;
    color: var(--cds-clay);
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }
  .glossary-ai-sections {
    display: flex;
    flex-direction: column;
    gap: 10px;
    font-size: 13.5px;
    line-height: 1.6;
    color: var(--cds-text-body);
  }
  .glossary-ai-sec {
    padding: 9px 12px;
    border-radius: 8px;
    background: var(--cds-surface-0);
    border: 1px solid var(--cds-border-subtle);
  }
  .glossary-ai-sec-label {
    display: block;
    font-family: var(--cds-font-sans);
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--cds-clay);
    margin-bottom: 4px;
  }
  .glossary-ai-sec pre {
    margin: 6px 0 2px;
    padding: 8px 10px;
    border-radius: 6px;
    background: var(--cds-surface-1);
    border: 1px solid var(--cds-border-subtle);
    font-family: "anthropic-mono", "anthropic-sans", ui-monospace, monospace;
    font-size: 11.5px;
    line-height: 1.48;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-word;
  }
  .glossary-ai-custom-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid var(--cds-border-subtle);
  }
  .glossary-ai-custom-input {
    appearance: none;
    flex: 1;
    height: 32px;
    padding: 0 10px;
    border-radius: 7px;
    border: 1px solid var(--cds-border-default);
    background: var(--cds-surface-0);
    color: var(--cds-text-primary);
    font-family: var(--cds-font-sans);
    font-size: 12.5px;
    outline: none;
  }
  .glossary-ai-custom-input:focus {
    border-color: var(--cds-clay);
  }
  .glossary-pop-foot {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding-top: 10px;
    border-top: 1px solid var(--cds-border-subtle);
    font-size: 12px;
    color: var(--cds-text-muted);
  }
  .glossary-pop-link {
    color: var(--accent);
    text-decoration: none;
    font-weight: 500;
  }
  .glossary-pop-link:hover {
    text-decoration: underline;
  }

  /* ==========================================================================
     8. RESPONSIVE MOBILE & TABLET BREAKPOINTS (390px / 768px)
     ========================================================================== */
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
      box-shadow: 12px 0 32px rgba(0, 0, 0, 0.35);
    }
    .rail {
      width: 100%;
      height: 100%;
    }
  }

  @media (max-width: 680px) {
    :root {
      --page-gutter: 14px;
      --header-height: 54px;
    }
    html, body {
      overflow-x: hidden;
      max-width: 100vw;
    }
    .topbar {
      padding: 0 8px;
      gap: 6px;
    }
    .topbar-context {
      gap: 6px;
      min-width: 0;
    }
    .topbar-actions {
      gap: 4px;
      flex-shrink: 0;
    }
    .academy-brand-sub,
    .academy-brand-sep {
      display: none;
    }
    .search-pill-btn {
      min-width: 0;
      padding: 0 9px;
    }
    .accent-trigger-btn {
      padding: 0 8px;
    }
    .search-pill-label {
      display: none;
    }
    #themeToggleLabel {
      display: none;
    }
    .main-view {
      padding: 16px var(--page-gutter) 96px;
    }
    .lesson-header {
      padding: 18px 16px;
      border-radius: 12px;
    }
    .lesson-title {
      font-size: clamp(22px, 6.2vw, 28px);
    }
    .lesson-lead {
      font-size: 14.5px;
    }
    .prose {
      font-size: 15.5px;
      line-height: 1.68;
    }
    .ui-btn,
    .stage-pill,
    .stage-pill-btn,
    .rail-item,
    .rail-stage-btn,
    .rail-shortcut-btn,
    .track-trigger {
      min-height: 44px;
    }
    .visual-card {
      margin: 16px 0 22px;
      border-radius: 10px;
      max-width: 100%;
    }
    .visual-bar {
      flex-direction: column;
      align-items: stretch;
      gap: 8px;
      padding: 8px 10px;
    }
    .visual-controls {
      width: 100%;
      justify-content: space-between;
    }
    .catalog-grid,
    .glossary-dict-grid {
      grid-template-columns: 1fr;
    }
    .glossary-ai-ask-form {
      flex-direction: column;
      align-items: stretch;
      flex: 1 1 100%;
      width: 100%;
    }
    .glossary-ai-ask-input {
      width: 100%;
      flex: none;
    }
    .lesson-pager {
      grid-template-columns: 1fr;
    }
    .lesson-pager-card.is-next {
      text-align: left;
    }
    pre.ascii-diagram {
      padding: 12px 10px;
      font-size: 11px;
      -webkit-overflow-scrolling: touch;
    }
    .modal-backdrop {
      padding: 0;
    }
    .expand-dialog {
      width: 100vw;
      height: 100dvh;
      max-height: 100dvh;
      border: 0;
      border-radius: 0;
    }
    .glossary-popover {
      top: 50% !important;
      left: 50% !important;
      width: calc(100vw - 20px) !important;
      max-height: 84dvh;
      border-radius: 16px;
      padding: 16px 16px 14px;
      transform: translate(-50%, -48%) scale(0.97);
    }
    .glossary-popover.open {
      transform: translate(-50%, -50%) scale(1);
    }
    .glossary-pop-close {
      width: 44px;
      height: 44px;
      font-size: 14px;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .layout, .rail, .track-panel-wrap {
      transition: none !important;
    }
  }

  /* ==========================================================================
     INTERACTIVE 2D INFRASTRUCTURE SIMULATOR (CHUYỆN TIỆM BÁNH CỦA MINH — 8 SLIDES)
     ========================================================================== */
  @keyframes infraFloatSlow {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-5px); }
  }
  @keyframes infraShakeBuilding {
    0%, 100% { transform: translateX(0); }
    20%, 60% { transform: translateX(-5px) rotate(-1deg); }
    40%, 80% { transform: translateX(5px) rotate(1deg); }
  }
  @keyframes infraPulseDanger {
    0%, 100% { box-shadow: 0 0 0 0 color-mix(in oklab, var(--sim-danger) 42%, transparent); }
    50% { box-shadow: 0 0 22px 6px color-mix(in oklab, var(--sim-danger) 20%, transparent); }
  }
  @keyframes infraPulseSuccess {
    0%, 100% { box-shadow: 0 0 0 0 color-mix(in oklab, var(--sim-ok) 40%, transparent); }
    50% { box-shadow: 0 0 20px 5px color-mix(in oklab, var(--sim-ok) 18%, transparent); }
  }
  @keyframes infraDataFlow {
    0% { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
  }
  .infra2d-wrap {
    margin: 22px 0 28px;
    border: 1px solid var(--cds-border-default);
    border-radius: var(--cds-radius-lg, 14px);
    background: var(--sim-bg);
    color: var(--sim-ink);
    font-family: var(--cds-font-sans);
    overflow: hidden;
    box-shadow: var(--cds-shadow-card-ring);
  }
  .infra2d-header {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding: 12px 16px;
    background: var(--sim-header-bg);
    border-bottom: 1px solid var(--sim-border);
  }
  .infra2d-brand {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .infra2d-brand-icon {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: var(--cds-clay);
    color: #faf9f5;
    font-weight: 800;
    font-size: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--cds-font-mono);
    flex-shrink: 0;
  }
  .infra2d-brand-badges {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 2px;
  }
  .infra2d-tag {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 2px 8px;
    border-radius: 999px;
    background: var(--sim-clay-soft);
    color: var(--sim-clay);
    border: 1px solid var(--sim-clay-border);
    font-family: var(--cds-font-mono);
  }
  .infra2d-chapter {
    font-size: 11.5px;
    font-weight: 700;
    color: var(--sim-warn);
    font-family: var(--cds-font-sans);
  }
  .infra2d-title-bar {
    font-family: var(--cds-font-serif);
    font-size: 15.5px;
    font-weight: 700;
    color: var(--sim-ink);
    margin: 0;
  }
  .infra2d-dots {
    display: flex;
    align-items: center;
    gap: 6px;
    overflow-x: auto;
    padding: 2px 0;
  }
  .infra2d-dot-btn {
    padding: 5px 10px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 700;
    font-family: var(--cds-font-sans);
    border: 1px solid var(--sim-border);
    background: var(--sim-card);
    color: var(--sim-muted);
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.15s ease;
  }
  .infra2d-dot-btn:hover {
    background: var(--sim-card-alt);
    color: var(--sim-ink);
  }
  .infra2d-dot-btn.active {
    background: var(--cds-clay);
    border-color: var(--accent-strong);
    color: #faf9f5;
    box-shadow: 0 3px 10px var(--sim-clay-soft);
  }
  .infra2d-grid {
    display: grid;
    grid-template-columns: 5fr 7fr;
    gap: 16px;
    padding: 16px;
  }
  .infra2d-col-left,
  .infra2d-col-right {
    background: var(--sim-card);
    border: 1px solid var(--sim-border);
    border-radius: 12px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .infra2d-pills {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 12px;
  }
  .infra2d-pill-num {
    font-size: 11px;
    font-weight: 800;
    padding: 3px 10px;
    border-radius: 999px;
    background: var(--sim-clay-soft);
    color: var(--sim-clay);
    border: 1px solid var(--sim-clay-border);
    font-family: var(--cds-font-mono);
  }
  .infra2d-pill-analogy {
    font-size: 11.5px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 999px;
    background: var(--sim-warn-soft);
    color: var(--sim-warn);
    border: 1px solid color-mix(in oklab, var(--sim-warn) 35%, transparent);
    font-family: var(--cds-font-sans);
  }
  .infra2d-slide-h3 {
    font-family: var(--cds-font-serif) !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    color: var(--sim-ink) !important;
    margin: 0 0 12px 0 !important;
    line-height: 1.35 !important;
  }
  .infra2d-story-box {
    background: var(--sim-canvas);
    border: 1px solid var(--sim-border);
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 12px;
    display: flex;
    gap: 10px;
    align-items: flex-start;
  }
  .infra2d-avatar {
    width: 36px;
    height: 36px;
    border-radius: 999px;
    background: var(--sim-clay-soft);
    border: 1px solid var(--sim-clay-border);
    color: var(--sim-clay);
    font-family: var(--cds-font-mono);
    font-size: 11px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .infra2d-story-title {
    font-size: 12.5px;
    font-weight: 700;
    color: var(--sim-clay);
    display: block;
    margin-bottom: 3px;
  }
  .infra2d-story-text {
    font-size: 13px;
    color: var(--sim-sub);
    font-style: italic;
    margin: 0 !important;
    line-height: 1.45;
  }
  .infra2d-keypoints {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 12px;
  }
  .infra2d-kp-item {
    padding: 10px 12px;
    border-radius: 10px;
    background: var(--sim-canvas);
    border: 1px solid var(--sim-border);
    display: flex;
    gap: 10px;
    align-items: flex-start;
  }
  .infra2d-kp-badge {
    width: 26px;
    height: 26px;
    border-radius: 6px;
    background: var(--sim-card);
    border: 1px solid var(--sim-border);
    color: var(--sim-clay);
    font-family: var(--cds-font-mono);
    font-size: 11px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 2px;
  }
  .infra2d-kp-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--sim-ink);
    margin: 0 0 2px 0;
    display: block;
  }
  .infra2d-kp-desc {
    font-size: 12.5px;
    color: var(--sim-sub);
    margin: 0 !important;
    line-height: 1.45;
  }
  .infra2d-verdict {
    padding: 10px 12px;
    border-radius: 10px;
    background: var(--sim-clay-soft);
    border: 1px solid var(--sim-clay-border);
    font-size: 12.5px;
    color: var(--sim-ink);
    line-height: 1.45;
  }
  .infra2d-sim-top {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding-bottom: 10px;
    margin-bottom: 12px;
    border-bottom: 1px solid var(--sim-border);
  }
  .infra2d-sim-live {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11.5px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--sim-muted);
    font-family: var(--cds-font-sans);
  }
  .infra2d-sim-dot {
    width: 9px;
    height: 9px;
    border-radius: 999px;
    background: var(--sim-ok);
    box-shadow: 0 0 8px var(--sim-ok);
  }
  .infra2d-sim-hint {
    font-size: 11.5px;
    color: var(--sim-flow);
    background: var(--sim-flow-soft);
    border: 1px solid color-mix(in oklab, var(--sim-flow) 32%, transparent);
    padding: 3px 10px;
    border-radius: 7px;
    font-weight: 600;
  }
  .infra2d-stage {
    min-height: 290px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: var(--sim-canvas);
    border: 1px solid var(--sim-border);
    padding: 14px;
    position: relative;
    overflow: hidden;
  }
  .infra2d-status {
    margin-top: 12px;
    padding: 10px 12px;
    border-radius: 10px;
    background: var(--sim-canvas);
    border: 1px solid var(--sim-border);
    font-size: 12.5px;
    color: var(--sim-ink);
    line-height: 1.45;
  }
  .infra2d-controls {
    margin-top: 10px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
  .infra2d-btn {
    padding: 8px 13px;
    border-radius: 9px;
    font-size: 12px;
    font-weight: 700;
    font-family: var(--cds-font-sans);
    cursor: pointer;
    border: 1px solid var(--sim-border);
    background: var(--sim-canvas);
    color: var(--sim-ink);
    transition: all 0.15s ease;
  }
  .infra2d-btn:hover {
    background: var(--sim-card-alt);
    color: var(--sim-ink);
  }
  .infra2d-btn-primary {
    background: var(--cds-clay);
    border-color: var(--accent-strong);
    color: #faf9f5;
  }
  .infra2d-btn-primary:hover {
    background: var(--accent-strong);
    color: #faf9f5;
  }
  .infra2d-btn-danger {
    background: var(--sim-danger);
    border-color: var(--sim-danger);
    color: #faf9f5;
  }
  .infra2d-btn-danger:hover {
    filter: brightness(1.08);
    color: #faf9f5;
  }
  .infra2d-btn-emerald {
    background: var(--sim-ok);
    border-color: var(--sim-ok);
    color: #faf9f5;
  }
  .infra2d-btn-emerald:hover {
    filter: brightness(1.08);
    color: #faf9f5;
  }
  .infra2d-btn-amber {
    background: var(--sim-warn);
    border-color: var(--sim-warn);
    color: #faf9f5;
  }
  .infra2d-btn-amber:hover {
    filter: brightness(1.08);
    color: #faf9f5;
  }
  .infra2d-btn-cyan {
    background: var(--sim-flow);
    border-color: var(--sim-flow);
    color: #faf9f5;
  }
  .infra2d-btn-cyan:hover {
    filter: brightness(1.08);
    color: #faf9f5;
  }
  .infra2d-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 12px 16px;
    background: var(--sim-header-bg);
    border-top: 1px solid var(--sim-border);
  }
  .infra2d-progress-wrap {
    flex: 1;
    max-width: 360px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }
  .infra2d-progress-track {
    width: 100%;
    height: 7px;
    background: var(--sim-card-alt);
    border-radius: 999px;
    overflow: hidden;
  }
  .infra2d-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--cds-clay), var(--sim-flow), var(--sim-ok));
    transition: width 0.25s ease;
  }
  @keyframes ingFlowDash {
    to { stroke-dashoffset: -24; }
  }
  @keyframes ingPulseNode {
    0%, 100% { filter: drop-shadow(0 0 3px color-mix(in oklab, var(--sim-flow) 35%, transparent)); }
    50% { filter: drop-shadow(0 0 9px color-mix(in oklab, var(--sim-flow) 85%, transparent)); }
  }
  .ing2d-flow-active {
    stroke-dasharray: 6 6;
    animation: ingFlowDash 0.85s linear infinite;
  }
  .ing2d-svg-stage {
    width: 100%;
    height: auto;
    max-height: 310px;
    display: block;
    border-radius: 8px;
    font-family: var(--cds-font-sans);
    background: radial-gradient(circle at 50% 25%, var(--sim-card) 0%, var(--sim-canvas) 100%);
    border: 1px solid var(--sim-border);
  }
  .ing2d-metrics-strip {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 6px;
    margin-top: 8px;
  }
  .ing2d-metric-chip {
    background: var(--sim-card);
    border: 1px solid var(--sim-border);
    border-radius: 7px;
    padding: 5px 8px;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .ing2d-metric-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--sim-muted);
    font-weight: 700;
    font-family: var(--cds-font-sans);
  }
  .ing2d-metric-val {
    font-size: 12px;
    font-weight: 800;
    color: var(--sim-ink);
    font-family: var(--cds-font-mono);
  }
  .infra2d-card-grid2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    width: 100%;
  }
  .infra2d-card-grid3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    width: 100%;
  }
  .infra2d-box {
    border: 1.5px solid var(--sim-border);
    background: var(--sim-card);
    color: var(--sim-ink);
    border-radius: 10px;
    padding: 10px;
    text-align: center;
    transition: all 0.2s ease;
  }
  .infra2d-float { animation: infraFloatSlow 3.2s ease-in-out infinite; }
  .infra2d-shake { animation: infraShakeBuilding 0.45s ease-in-out infinite; }
  .infra2d-glow-danger { animation: infraPulseDanger 1.5s infinite; border-color: var(--sim-danger) !important; }
  .infra2d-glow-success { animation: infraPulseSuccess 2s infinite; border-color: var(--sim-ok) !important; }
  .infra2d-pipe {
    height: 9px;
    width: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--sim-card-alt) 25%, var(--sim-flow) 50%, var(--sim-card-alt) 75%);
    background-size: 200% 100%;
    animation: infraDataFlow 1.8s linear infinite;
    margin: 8px 0;
  }
  @media (max-width: 900px) {
    .infra2d-grid {
      grid-template-columns: 1fr;
      padding: 10px;
      gap: 12px;
    }
    .infra2d-card-grid3 {
      grid-template-columns: 1fr;
    }
    .infra2d-progress-wrap {
      display: none;
    }
  }
  </style>
</head>
<body>
  <a href="#articleContainer" class="skip-link">Chuyển đến nội dung chính</a>
  <div class="progress-track"><div class="progress-bar" id="progressBar"></div></div>

  <header class="topbar">
    <div class="topbar-context">
      <button class="rail-toggle-modern" id="railToggleBtn" type="button" aria-label="Đóng hoặc mở mục lục (Phím [ hoặc ⌘B)" aria-controls="syllabusRail" aria-expanded="true" title="Đóng / mở thanh mục lục ([ hoặc ⌘B)">
        <svg class="rail-toggle-svg" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <rect x="1.75" y="2.25" width="12.5" height="11.5" rx="2.25"/>
          <line x1="6" y1="2.5" x2="6" y2="13.5"/>
        </svg>
        <span id="railToggleLabel">Mục lục</span>
      </button>
      <button class="academy-brand-btn" id="catalogNavBtn" type="button" onclick="openCatalogView()" title="FSDS Learning Academy — Xem toàn bộ Danh mục 26 Học phần">
        <span class="academy-brand-mark" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2.75L14.35 9.65L21.25 12L14.35 14.35L12 21.25L9.65 14.35L2.75 12L9.65 9.65L12 2.75Z" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"/>
            <circle cx="12" cy="12" r="2.25" fill="currentColor"/>
          </svg>
        </span>
        <span class="academy-brand-wordmark">
          <span class="academy-brand-main">FSDS</span>
          <span class="academy-brand-sep" aria-hidden="true"></span>
          <span class="academy-brand-sub" id="brandSubLabel">Academy</span>
        </span>
      </button>
      <span class="topbar-divider hide-mobile" aria-hidden="true"></span>
      <nav class="topbar-nav-tabs hide-mobile" aria-label="Điều hướng nền tảng">
        <button class="ui-btn" id="catalogTopBtn" type="button" onclick="openCatalogView()" title="Danh mục 26 Học phần">
          <span id="navCoursesLabel">Khóa học (26)</span>
        </button>
        <button class="ui-btn" id="glossaryNavBtn" type="button" onclick="openGlossaryView()" title="Mở Từ điển Kỹ thuật AI">
          <span id="navGlossaryLabel">Từ điển AI (74)</span>
        </button>
      </nav>
      <span class="topbar-context-pill hide-mobile" id="topbarContextPill"></span>
    </div>

    <div class="topbar-actions">
      <button class="ui-btn search-pill-btn" id="searchTriggerBtn" type="button" title="Tìm nhanh học phần, chặng, trạm hoặc thuật ngữ (⌘K hoặc /)">
        <span style="display:inline-flex;align-items:center;gap:6px;"><span class="cds-icon" aria-hidden="true">&#xE0D3;</span><span class="search-pill-label" id="searchBtnLabel">Tìm kiếm...</span></span>
        <kbd class="shortcut-key hide-mobile">⌘K</kbd>
      </button>

      <div class="accent-picker-wrap" id="accentPickerWrap">
        <button class="accent-trigger-btn" id="accentPickerBtn" type="button" onclick="toggleAccentPopover(event)" title="Chọn tông màu chủ đạo (6 bảng màu Editorial)">
          <span class="accent-dot-live" id="accentDotLive"></span>
          <span class="hide-mobile" id="accentBtnLabel">Màu</span>
        </button>
        <div class="accent-popover" id="accentPopover" role="menu" aria-label="Bảng chọn 6 tông màu chủ đạo">
          <button type="button" class="accent-swatch-opt active" data-accent="clay" onclick="applyAccentTheme('clay')" title="Anthropic Clay (Cam đất mặc định)" style="background:#d97757;"></button>
          <button type="button" class="accent-swatch-opt" data-accent="cobalt" onclick="applyAccentTheme('cobalt')" title="Cobalt Blue (Xanh lam kỹ thuật)" style="background:#2f6fed;"></button>
          <button type="button" class="accent-swatch-opt" data-accent="sage" onclick="applyAccentTheme('sage')" title="Sage Forest (Xanh lá tùng)" style="background:#2e7d5b;"></button>
          <button type="button" class="accent-swatch-opt" data-accent="plum" onclick="applyAccentTheme('plum')" title="Royal Plum (Tím mận)" style="background:#844fc1;"></button>
          <button type="button" class="accent-swatch-opt" data-accent="ochre" onclick="applyAccentTheme('ochre')" title="Amber Ochre (Vàng hổ phách)" style="background:#c57b1c;"></button>
          <button type="button" class="accent-swatch-opt" data-accent="crimson" onclick="applyAccentTheme('crimson')" title="Editorial Rose (Đỏ hồng ngọc)" style="background:#c93b5b;"></button>
        </div>
      </div>

      <button class="lang-switch-btn" id="langToggleBtn" type="button" onclick="toggleAppLanguage()" title="Chuyển đổi ngôn ngữ Tiếng Việt ↔ English (AI Auto-Translate + TTL Cache)">
        <span class="lang-opt active" id="langOptVi">VI</span>
        <span class="lang-opt" id="langOptEn">EN</span>
      </button>

      <button class="ui-btn" id="themeToggleBtn" type="button" title="Chuyển chế độ màu Sáng / Tối">
        <span class="cds-icon" id="themeToggleIcon" aria-hidden="true">&#xE0B0;</span>
        <span id="themeToggleLabel">Sáng</span>
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
    <aside class="page-toc-slot" id="pageTocSlot" aria-label="Mục lục trên trang">
      <div class="page-toc" id="pageTocPanel"></div>
    </aside>
  </div>

  <!-- Command Palette Modal (⌘K / /) -->
  <div class="modal-backdrop" id="searchModal" role="dialog" aria-modal="true" aria-label="Tìm kiếm học phần và trạm kiến thức">
    <div class="cmd-dialog" onclick="event.stopPropagation()">
      <div class="cmd-input-row">
        <input type="text" class="cmd-input" id="cmdSearchInput" placeholder="Tìm học phần (D02, F03...), trạm (MVCC, Slotted Page...) hoặc thuật ngữ..." autocomplete="off" />
        <kbd class="shortcut-key">ESC</kbd>
      </div>
      <ul class="cmd-results" id="cmdResultsList"></ul>
      <div class="cmd-footer">
        <span id="cmdFooterHint">↑↓ Di chuyển · Enter Chọn · Esc Đóng</span>
        <span id="cmdFooterStats">26 Học phần · 19 Chặng · 74 Thuật ngữ Kỹ thuật</span>
      </div>
    </div>
  </div>

  <!-- Fullscreen Diagram Expand Modal -->
  <div class="modal-backdrop" id="expandModal" role="dialog" aria-modal="true" aria-label="Phóng to sơ đồ">
    <div class="expand-dialog" onclick="event.stopPropagation()">
      <div class="expand-header">
        <span id="expandModalTitle">Sơ đồ chi tiết</span>
        <div style="display:flex;align-items:center;gap:8px;">
          <button class="ui-btn" id="expandCopyBtn" type="button">Sao chép ASCII</button>
          <button class="ui-btn" id="expandCloseBtn" type="button">Đóng (Esc)</button>
        </div>
      </div>
      <div class="expand-body" id="expandModalBody"></div>
    </div>
  </div>

  <!-- Centered Anthropic-Style AI Technical Glossary Modal -->
  <div class="glossary-modal-backdrop" id="glossaryModalBackdrop" onclick="closeGlossaryPopover(true)"></div>
  <div class="glossary-popover" id="glossaryPopover" role="dialog" aria-modal="true" aria-label="Giải nghĩa thuật ngữ kỹ thuật bằng AI" aria-hidden="true">
    <div class="glossary-pop-head">
      <div>
        <div class="glossary-pop-meta-row">
          <span class="glossary-pop-meta" id="glossaryPopCategory">THUẬT NGỮ KỸ THUẬT</span>
          <span class="glossary-pop-cache-badge" id="glossaryPopCacheBadge">◈ AI TTL Cache</span>
        </div>
        <h4 class="glossary-pop-title" id="glossaryPopTitle">Tên thuật ngữ</h4>
      </div>
      <button type="button" class="glossary-pop-close" id="glossaryPopCloseBtn" title="Đóng (Esc)" aria-label="Đóng bảng giải nghĩa">✕</button>
    </div>
    <p class="glossary-pop-intuition" id="glossaryPopIntuition"></p>
    <code class="glossary-pop-code" id="glossaryPopCode"></code>

    <div class="glossary-ai-box" id="glossaryAiBox">
      <div class="glossary-ai-box-head">
        <span class="glossary-ai-box-title" id="glossaryAiBoxTitle">✦ Giải thích chuyên sâu &amp; Ví dụ thực tế (Gemini AI)</span>
        <button type="button" class="ui-btn" id="glossaryAiRefreshBtn" style="height:24px;padding:0 8px;font-size:11px;" onclick="regenerateCurrentGlossaryAi()">↻ Tạo lại</button>
      </div>
      <div class="glossary-ai-sections" id="glossaryPopAiBody"></div>
      <div class="glossary-ai-custom-row">
        <input type="text" class="glossary-ai-custom-input" id="glossaryAiCustomInput" placeholder="Nhập bất kỳ thuật ngữ, công nghệ hoặc framework nào để AI giải thích..." onkeydown="if(event.key==='Enter'){event.preventDefault();askAiCustomTermFromModal();}" />
        <button type="button" class="ui-btn" style="height:32px;font-size:12px;" onclick="askAiCustomTermFromModal()">Hỏi AI ✦</button>
      </div>
    </div>

    <div class="glossary-pop-foot">
      <a class="glossary-pop-link" id="glossaryPopLink" href="#/F01/1">Xem tại trạm gốc →</a>
      <a class="glossary-pop-link" href="#/glossary" onclick="openGlossaryView();closeGlossaryPopover(true);return false;">Mở toàn bộ Từ điển AI (74) →</a>
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
          modules: "Kiến trúc GNU/Linux, Bash scripting, biên dịch với Makefile và lập lịch CronJob",
          lab: "Cài đặt Ubuntu và thực hành Linux CLI 101",
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
          modules: "Cấu trúc dữ liệu Python, môi trường ảo, xử lý ngoại lệ và lập trình bất đồng bộ (Async/Sync)",
          lab: "Xây dựng trình thu thập dữ liệu (Data Crawler) bằng Python",
          stack: "Python, venv, asyncio"
        },
        {
          code: "F03",
          title: "Database Fundamentals",
          slide: "03-database-fundamentals.pdf",
          pages: 70,
          hasContent: true,
          contentNote: "Chặng 1–4",
          slideToc: [
            "01/ Introduction to Databases",
            "02/ SQL vs NoSQL",
            "03/ SQL Command Groups (DDL, DML, DQL, DCL, TCL)",
            "04/ Cost & Performance Optimization Techniques"
          ],
          modules: "Thiết kế CSDL quan hệ & NoSQL, nhóm lệnh DDL, DML, DQL, DCL, TCL và tối ưu hóa truy vấn",
          lab: "Khởi tạo PostgreSQL và tối ưu hóa câu lệnh SQL thực tế",
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
          modules: "Kiến trúc REST, gRPC, GraphQL, xác thực JWT/OAuth, kiểm tra kiểu dữ liệu và đo kiểm tải FastAPI",
          lab: "Triển khai dịch vụ Web API đa kiến trúc và kiểm thử chịu tải",
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
          modules: "Mô hình V-Model, kiểm thử hộp đen/hộp trắng, Mutation Testing, Hoare Logic và quy trình TDD",
          lab: "Xây dựng bộ kiểm thử tự động toàn diện cho hệ thống API",
          stack: "pytest, unittest"
        },
        {
          code: "F06",
          title: "Containerization & Orchestration",
          slide: "06-containerization-and-orchestration.pdf",
          pages: 72,
          hasContent: true,
          contentNote: "Chặng 1–4",
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
          modules: "Ảo hóa cấp OS (Namespaces, cgroups), kiến trúc Docker/OCI, quản lý mạng, ổ đĩa và Docker Compose",
          lab: "Đóng gói API với Docker, dựng cụm dịch vụ bằng Compose và kiểm thử",
          stack: "Docker, Docker Compose, Kubernetes"
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
          hasContent: true,
          contentNote: "Chặng 1–5",
          slideToc: [
            "01/ Introduction & Data Architectures",
            "02/ Source Systems",
            "03/ The Kafka Ecosystem",
            "04/ Fundamentals of Kafka",
            "05/ Kafka's Challenges & Operations",
            "06/ Change Data Capture (CDC) & Debezium"
          ],
          modules: "Kiến trúc thu thập dữ liệu, hệ sinh thái Apache Kafka, vận hành cụm broker và đồng bộ CDC với Debezium",
          lab: "Xây dựng đường ống thu thập dữ liệu CDC thời gian thực",
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
          modules: "Lưu trữ phân tán, định dạng cột Parquet, mô hình hóa DWH, Open Lakehouse (Delta, Iceberg, Hudi) & Medallion",
          lab: "Triển khai kiến trúc Data Lakehouse hoàn chỉnh từ con số 0",
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
          modules: "Kiến trúc thực thi Apache Spark, RDD/DataFrame API, quản lý bộ nhớ, chống lệch dữ liệu và tối ưu hiệu năng",
          lab: "Viết tác vụ Spark Batch xử lý và kiểm định chất lượng dữ liệu",
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
          modules: "Ngữ nghĩa thời gian (Event/Processing Time), Watermark, cửa sổ trượt, quản lý State và chịu lỗi trên Flink",
          lab: "Xây dựng tác vụ xử lý luồng (Stream Processing) kiểm soát chất lượng dữ liệu",
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
          modules: "Mô hình chiều (Kimball, SCD, Data Vault), động cơ OLAP tốc độ cao (ClickHouse, Pinot) và Feature Store",
          lab: "Xây dựng Feature Store và đường ống cung cấp đặc trưng cho ML",
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
          modules: "Điều phối DAG với Apache Airflow, tính lũy đẳng (Idempotency), Backfill, hợp đồng dữ liệu và quản trị DataHub",
          lab: "Triển khai Airflow điều phối đa tầng kèm truy vết dòng chảy dữ liệu (Lineage)",
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
          modules: "Tích hợp toàn trình đường ống dữ liệu từ nguồn đến tầng phục vụ kèm kiểm thử và truy vết Lineage",
          lab: "Đồ án thực chiến tổng hợp Data Engineering (Mini Coursework)",
          stack: "FastAPI, PostgreSQL, Docker, Kafka, Delta Lake, Spark, Airflow"
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
          modules: "Xử lý ma trận với NumPy, phân tích bằng Pandas, trực quan hóa Matplotlib và nền tảng học sâu với PyTorch",
          lab: "Dự án Khoa học Dữ liệu toàn trình và ứng dụng nhận diện ký tự (OCR)",
          stack: "NumPy, Pandas, Matplotlib, PyTorch"
        },
        {
          code: "A02",
          title: "Introduction to LLM, RAG & Agent",
          slide: null,
          slideToc: ["01/ Transformer Architecture & LLM", "02/ Retrieval-Augmented Generation (RAG)", "03/ AI Agents & Guardrails"],
          modules: "Kiến trúc Transformer, mô hình ngôn ngữ lớn (LLM), hệ thống truy hồi tri thức (RAG), AI Agent và Guardrails",
          lab: "Tinh chỉnh LLM mã nguồn mở, xây dựng hệ thống RAG và tác tử tự hành (Agentic AI)",
          stack: "LLM Stack, Vector DB, Agent Framework"
        },
        {
          code: "A03",
          title: "Model Serving Design Patterns",
          slide: null,
          slideToc: ["01/ Model Serving Patterns", "02/ Model Loading Patterns", "03/ Asynchronous Task Queue ML System"],
          modules: "Các mẫu thiết kế phục vụ mô hình (Online, Batch, Streaming), cơ chế nạp trọng số và hàng đợi tác vụ bất đồng bộ",
          lab: "Xây dựng hệ thống suy luận ML phân tán qua hàng đợi RabbitMQ",
          stack: "LLM, RabbitMQ"
        },
        {
          code: "A04",
          title: "Dive into LLM Serving",
          slide: null,
          slideToc: ["01/ KV Cache Mechanics", "02/ LLM Serving Challenges & Throughput Optimization", "03/ High-Performance Engines (vLLM, TensorRT-LLM, SGLang)"],
          modules: "Cơ chế bộ nhớ KV Cache, PagedAttention, Continuous Batching và tối ưu hóa thông lượng suy luận LLM",
          lab: "Triển khai điểm cuối phục vụ LLM hiệu năng cao",
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
          modules: "Định lý CAP/PACELC, đồng thuận phân tán (Raft/Paxos), nhân bản, phân mảnh (Sharding) và tính nhất quán",
          lab: "Thiết kế hệ thống phân tán và mô phỏng kịch bản chịu lỗi mạng",
          stack: "Distributed Systems"
        },
        {
          code: "P02",
          title: "Kubernetes",
          slide: null,
          slideToc: ["01/ K8s Architecture & Core Workloads (Pod, Deployment, Service, Ingress, PV/PVC)", "02/ Sidecars, Init Containers & Operators", "03/ Deployment Strategies, Helm/Helmfile, Secrets & Resources"],
          modules: "Kiến trúc K8s, đối tượng Pod, Deployment, Service, Ingress, PV/PVC, mẫu Sidecar/Operator và quản lý gói bằng Helm",
          lab: "Xử lý tác vụ bất đồng bộ và triển khai hệ thống API trên cụm Kubernetes",
          stack: "Kubernetes, Helm, KServe, Vault"
        },
        {
          code: "P03",
          title: "Kubeflow & Distributed Training",
          slide: null,
          slideToc: ["01/ Kubeflow Architecture & Operators", "02/ Distributed Training & Distributed Storage", "03/ GPU Scheduling"],
          modules: "Kiến trúc Kubeflow Operator, huấn luyện phân tán đa nút, lưu trữ phân tán và lập lịch tài nguyên GPU",
          lab: "Triển khai Kubeflow và đường ống huấn luyện mô hình phân tán",
          stack: "Kubeflow"
        },
        {
          code: "P04",
          title: "Cloud Services (GCP / FinOps)",
          slide: null,
          slideToc: ["01/ Cloud Hierarchy & IAM", "02/ VPC Networking & Storage Lifecycle/Locality", "03/ GCP ML/Data Stack, IaaS/PaaS/SaaS & FinOps"],
          modules: "Phân quyền IAM, mạng ảo VPC, vòng đời lưu trữ đám mây, hệ sinh thái Data/ML trên GCP và tối ưu chi phí FinOps",
          lab: "Khởi tạo hạ tầng đám mây GCP bằng Terraform và tự động hóa triển khai với Ansible",
          stack: "GCP, NGINX"
        },
        {
          code: "P05",
          title: "Routing & Gateway",
          slide: null,
          slideToc: ["01/ Routing, Load Balancing & Service Discovery", "02/ Resiliency (Retry, Circuit Breaker, Fallback, Timeout)", "03/ AuthN/AuthZ, Rate Limits, Semantic Caching & Tracing"],
          modules: "Cân bằng tải, khám phá dịch vụ, mẫu chịu lỗi (Circuit Breaker, Retry), giới hạn lưu lượng và Semantic Caching",
          lab: "Thiết kế kịch bản định tuyến và áp dụng chính sách bảo vệ tại tầng API Gateway",
          stack: "API Gateway Stack"
        },
        {
          code: "P06",
          title: "Infrastructure as Code",
          slide: null,
          slideToc: ["01/ IaC Fundamentals", "02/ Terraform & Ansible Architecture, Commands & Best Practices", "03/ Hybrid Workflow & Drift Detection"],
          modules: "Nguyên lý Hạ tầng dưới dạng Mã (IaC), kiến trúc Terraform & Ansible, quy trình kết hợp và phát hiện sai lệch cấu hình",
          lab: "Cấp phát tự động và đồng bộ hóa trạng thái hạ tầng máy chủ",
          stack: "Terraform, Ansible"
        },
        {
          code: "P07",
          title: "Versioning & CI/CD",
          slide: null,
          slideToc: ["01/ Code, Data, Model & Experiment Versioning (Git/DVC/MLflow)", "02/ CI/CD & AIDE Pipelines", "03/ Jenkins, DVC & MLflow Architectures"],
          modules: "Quản lý phiên bản mã nguồn, dữ liệu và mô hình (Git, DVC, MLflow) cùng đường ống tích hợp liên tục CI/CD",
          lab: "Xây dựng đa đường ống CI/CD tự động hóa kiểm thử và phát hành mô hình",
          stack: "Jenkins, DVC, MLflow"
        },
        {
          code: "P08",
          title: "Observable Systems",
          slide: null,
          slideToc: ["01/ Logs, Metrics & Distributed Traces", "02/ Observable Architecture & Drift Detection", "03/ LLM & Agent Telemetry"],
          modules: "Ba trụ cột quan sát hệ thống (Logs, Metrics, Traces), phát hiện trôi dữ liệu (Data Drift) và giám sát tác tử LLM",
          lab: "Thiết lập hệ thống giám sát toàn diện với Prometheus, Grafana, Jaeger và Langfuse",
          stack: "OpenTelemetry, Evidently, Prometheus, Grafana, ELK, Jaeger, Langfuse"
        },
        {
          code: "P09",
          title: "Misc Problems & Final Coursework",
          slide: null,
          slideToc: ["01/ Security Best Practices & SRE", "02/ Repository Design & Service Mesh", "03/ Final Coursework (2 tháng): End-to-End Data/AI System"],
          modules: "Bảo mật hệ thống, nguyên lý SRE, thiết kế Monorepo/Polyrepo, Service Mesh và Đồ án Tốt nghiệp (2 tháng)",
          lab: "Xây dựng, triển khai và vận hành hệ thống Data & AI thực chiến quy mô sản xuất",
          stack: "Full Stack Data & AI"
        }
      ]
    }
  ];

  const LINUX_STAGES = [
    { id: 1, shortTitle: "Hạt nhân, Hệ sinh thái & Luồng chạy 1 lệnh", title: "Chặng 1: Hạt nhân, Hệ sinh thái GNU/Linux & Giải phẫu Luồng chạy 1 Lệnh (Trạm 1.1 → 1.3)" },
    { id: 2, shortTitle: "Giải phẫu Process, Triết lý File & Cây thư mục", title: "Chặng 2: Giải phẫu Căn cước Process, Triết lý 'Everything is a file', Cây thư mục / & Bộ lệnh CLI (Trạm 2.1 → 2.4)" },
    { id: 3, shortTitle: "Giao tiếp Đa tiến trình (IPC) & Điều hướng I/O", title: "Chặng 3: Giao tiếp Đa tiến trình (stdin/stdout/stderr), Đường ống Pipe & Điều hướng I/O (Trạm 3.1 → 3.2)" },
    { id: 4, shortTitle: "Dây chuyền Tự động hóa: Script, Make & Cron", title: "Chặng 4: Dây chuyền Tự động hóa 24/7 — Bash Scripting, GCC/Makefile & Cronjob (Trạm 4.1 → 4.3)" }
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
    { id: "storage-4-1", code: "4.1", title: "Conceptual → Logical → Physical", fullTitle: "Trạm 4.1: Ba Cấp độ Thiết kế Mô hình Dữ liệu (Conceptual → Logical → Physical)" },
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
    { id: "storage-5-4", code: "5.4", title: "Phác đồ Cứu nguy (Zoning, Contracts, SSoT)", fullTitle: "Trạm 5.4: Phác đồ Cứu nguy — Zoning (Raw → Cleansed → Curated), Data Contracts & Single Source of Truth" },
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
    { id: "storage-7-2", code: "7.2", title: "Giải phẫu 3 Tầng Bronze → Silver → Gold", fullTitle: "Trạm 7.2: Giải phẫu Chi tiết 3 Tầng Medallion qua Hành trình Đơn hàng #8888 (Bronze → Silver → Gold)" },
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

  const DB_STAGES = [
    { id: 1, shortTitle: "Fundamentals & Data Modeling (3NF)", title: "Chặng 1: Database Fundamentals & Data Modeling (Nền móng cấu trúc & Toàn vẹn dữ liệu)" },
    { id: 2, shortTitle: "Storage Engine & Memory (8KB Page & WAL)", title: "Chặng 2: Storage Engine & Memory Architecture (Giải phẫu động cơ PostgreSQL & Bộ nhớ)" },
    { id: 3, shortTitle: "Concurrency (MVCC) & Query Execution", title: "Chặng 3: Concurrency Control & Query Execution (Vận hành đồng thời & Tối ưu truy vấn)" },
    { id: 4, shortTitle: "Scalability, HA (PGD) & NoSQL (CAP/BASE)", title: "Chặng 4: Scalability, High Availability & NoSQL Trade-offs (Mở rộng quy mô & Phân tán)" }
  ];

  const DB_CHANG1_STATIONS = [
    { id: "db-0-map", code: "0.0", title: "Nhân vật chính #HD01 & Bản đồ 4 Chặng", fullTitle: "Trạm 0.0: Đơn hàng Trà sữa #HD01 của khách hàng Lan & Bản đồ Tư duy 4 Chặng — 12 Trạm" },
    { id: "db-1-1", code: "1.1", title: "What is a Database & DBMS Architecture", fullTitle: "Trạm 1.1: What is a Database & DBMS Architecture (Cơ sở dữ liệu & Giải phẫu Hệ quản trị)" },
    { id: "db-1-2", code: "1.2", title: "Relational Model, Keys (PK, FK) & Constraints", fullTitle: "Trạm 1.2: Relational Model, Keys (PK, FK), Cardinality & Constraints (Mô hình Quan hệ & Chốt chặn Ràng buộc)" },
    { id: "db-1-3", code: "1.3", title: "Normalization (UNF → 3NF → BCNF) vs Denormalization", fullTitle: "Trạm 1.3: Normalization (UNF → 1NF → 2NF → 3NF → BCNF) vs Denormalization (Chuẩn hóa & Phi chuẩn hóa)" },
    { id: "db-1-summary", code: "Kết", title: "Tóm tắt bỏ túi Chặng 1", fullTitle: "Tóm tắt bỏ túi Chặng 1 & Checklist Tự kiểm tra (Data Modeling & 3NF)" }
  ];

  const DB_CHANG2_STATIONS = [
    { id: "db-2-1", code: "2.1", title: "Client/Backend Process & Memory vs Disk DBMS", fullTitle: "Trạm 2.1: Client/Backend Process & Memory Versus Disk-Based DBMS (Tiến trình & Phân cấp Bộ nhớ 2 tầng)" },
    { id: "db-2-2", code: "2.2", title: "On-Disk Layout (Row vs Column) & Slotted Page", fullTitle: "Trạm 2.2: On-Disk Data Layout (Row vs Column) & Slotted Page (4-16 KB) (Cấu trúc Trang vật lý)" },
    { id: "db-2-3", code: "2.3", title: "Write Path, WAL Buffer, Dirty Pages & Checkpointer", fullTitle: "Trạm 2.3: Write Path, WAL Buffer, Dirty Pages & Checkpointer (Luồng Ghi Kép & Cơ chế Phục hồi)" },
    { id: "db-2-summary", code: "Kết", title: "Tóm tắt bỏ túi Chặng 2", fullTitle: "Tóm tắt bỏ túi Chặng 2 & Checklist Tự kiểm tra (Storage Engine & Memory)" }
  ];

  const DB_CHANG3_STATIONS = [
    { id: "db-3-1", code: "3.1", title: "ACID, Lock Manager, MVCC & Autovacuum Worker", fullTitle: "Trạm 3.1: ACID Transactions, Lock Manager, MVCC & Autovacuum Worker (Giao dịch & Kiểm soát Đồng thời Đa phiên bản)" },
    { id: "db-3-2", code: "3.2", title: "Storage Structures (B-Trees vs LSM-Trees) & Indexing", fullTitle: "Trạm 3.2: Storage Structures (B-Trees vs LSM-Trees) & Indexing Strategies (Cấu trúc Cây Chỉ mục & Đánh đổi Đọc/Ghi)" },
    { id: "db-3-3", code: "3.3", title: "Query Optimizer, EXPLAIN PLAN & Access Control (PoLP)", fullTitle: "Trạm 3.3: Query Optimizer, EXPLAIN PLAN, SQL Command Groups & Access Control (PoLP) (Tối ưu Truy vấn & Bảo mật Phân quyền)" },
    { id: "db-3-summary", code: "Kết", title: "Tóm tắt bỏ túi Chặng 3", fullTitle: "Tóm tắt bỏ túi Chặng 3 & Checklist Tự kiểm tra (MVCC, Indexing & EXPLAIN)" }
  ];

  const DB_CHANG4_STATIONS = [
    { id: "db-4-1", code: "4.1", title: "Scale-up vs Scale-out, Replication & Sharding", fullTitle: "Trạm 4.1: Vertical Scaling (Scale-up) vs Horizontal Scaling (Scale-out), Replication & Sharding (Mở rộng Hạ tầng & Nhân bản)" },
    { id: "db-4-2", code: "4.2", title: "Always-On Multi-Location HA (PGD) & Next-Gen DB", fullTitle: "Trạm 4.2: Always-On Multi-Location HA (EnterpriseDB PGD) & Next-Gen Databases (TiDB, YugabyteDB, ClickHouse)" },
    { id: "db-4-3", code: "4.3", title: "SQL vs NoSQL, CAP Theorem (CA/CP/AP) & BASE", fullTitle: "Trạm 4.3: SQL vs NoSQL Data Models, CAP Theorem (CA/CP/AP) & BASE vs ACID (Định lý CAP & Kiến trúc Lai)" },
    { id: "db-4-summary", code: "Kết", title: "Tóm tắt bỏ túi Chặng 4 (Khép kín F03)", fullTitle: "Tóm tắt bỏ túi Chặng 4 & Khép kín Toàn bộ Hành trình Database Fundamentals" }
  ];

  function getDbStations(stageId = activeStorageStage) {
    if (stageId === 1) return DB_CHANG1_STATIONS;
    if (stageId === 2) return DB_CHANG2_STATIONS;
    if (stageId === 3) return DB_CHANG3_STATIONS;
    if (stageId === 4) return DB_CHANG4_STATIONS;
    return [];
  }

  const CONTAINER_STAGES = [
    { id: 1, shortTitle: "Tiến hóa Hạ tầng (Bare Metal, VM, VPS, Cloud VM & Container)", title: "Chặng 1: Tiến hóa Hạ tầng (Thời kỳ 1 → Thời kỳ 2: Bare Metal, VM/VPS/Cloud VM, Container & Serverless)" },
    { id: 2, shortTitle: "Giải phẫu Tầng Nhân Linux (Namespaces, cgroups v2 & OverlayFS)", title: "Chặng 2: Giải phẫu Học Tầng Nhân Linux (Linux Kernel Foundations: Namespaces, cgroups v2, OverlayFS & Seccomp)" },
    { id: 3, shortTitle: "Chu trình Build-Ship-Run & Động cơ OCI Runtime", title: "Chặng 3: Chu trình Build-Ship-Run & Động cơ OCI Runtime (Dockerfile, Volumes, containerd, shim & runc)" },
    { id: 4, shortTitle: "Điều phối Phân tán với Kubernetes (CRI, Control Plane & Pods)", title: "Chặng 4: Thời kỳ 3 — Điều phối Phân tán với Kubernetes (CRI, Declarative YAML, Control Plane & 3 Pod Replicas)" }
  ];

  const CONTAINER_CHANG1_STATIONS = [
    { id: "container-0-map", code: "0.0", title: "Nhân vật chính order-api & Bản đồ 4 Chặng", fullTitle: "Trạm 0.0: Tiến trình dịch vụ order-api (app.py + PostgreSQL) & Bản đồ Tư duy 4 Chặng — 10 Trạm" },
    { id: "container-1-0-sim", code: "2D", title: "Mô phỏng 2D (8 Slide): Chuyện Tiệm Bánh Của Minh", fullTitle: "Trạm 1.0 (Mô phỏng 2D): Chuyện Tiệm Bánh Của Minh — Từ Máy Ảo (VM) Đến VPS, Cloud VM, Container & Serverless" },
    { id: "container-1-1", code: "1.1", title: "Bare Metal & VMs (Hypervisor Type 1/2 & VM Tax)", fullTitle: "Trạm 1.1: Bare Metal (Lãng phí 90–95% CPU) & Virtual Machines (Hypervisor Type 1 & Type 2, Guest OS, VM Tax)" },
    { id: "container-1-2", code: "1.2", title: "Container Model (OS-level Virtualization vs VMs)", fullTitle: "Trạm 1.2: Container Model (OS-level Virtualization, Shared Host OS Kernel, 50+ Containers/host)" },
    { id: "container-1-summary", code: "Kết", title: "Tóm tắt bỏ túi Chặng 1", fullTitle: "Tóm tắt bỏ túi Chặng 1 & Checklist Tự kiểm tra (Tiến hóa Hạ tầng)" }
  ];

  const CONTAINER_CHANG2_STATIONS = [
    { id: "container-2-1", code: "2.1", title: "Linux Namespaces (pid, net, mnt, ipc, uts, user)", fullTitle: "Trạm 2.1: Linux Namespaces — Lăng kính Ảo ảnh Cô lập Góc nhìn (Host PID 10423 → Virtual PID 1)" },
    { id: "container-2-2", code: "2.2", title: "Control Groups — cgroups v2 (cpu.max, memory.max, BlkIO)", fullTitle: "Trạm 2.2: Control Groups (cgroups v2) — Vòng Kim Cô Định mức Phần cứng (CPU, RAM & Disk I/O)" },
    { id: "container-2-3", code: "2.3", title: "OverlayFS (LowerDir/UpperDir) & Security (Capabilities/Seccomp)", fullTitle: "Trạm 2.3: OverlayFS & Security Hardening (Image Layers, Syscalls clone/unshare/pivot_root, Capabilities & Seccomp)" },
    { id: "container-2-summary", code: "Kết", title: "Tóm tắt bỏ túi Chặng 2", fullTitle: "Tóm tắt bỏ túi Chặng 2 & Checklist Tự kiểm tra (Linux Kernel Foundations)" }
  ];

  const CONTAINER_CHANG3_STATIONS = [
    { id: "container-3-1", code: "3.1", title: "Workflow Build - Ship - Run & Persistent Volumes", fullTitle: "Trạm 3.1: Workflow Vĩ mô Build - Ship - Run (Dockerfile, Multi-stage Build, OCI Image, Registry & Persistent Volumes)" },
    { id: "container-3-2", code: "3.2", title: "Động cơ OCI Runtime (dockerd → containerd → shim → runc)", fullTitle: "Trạm 3.2: Giải phẫu Động cơ OCI Runtime & Hệ sinh thái Công cụ (Docker vs Podman vs containerd vs CRI-O)" },
    { id: "container-3-summary", code: "Kết", title: "Tóm tắt bỏ túi Chặng 3", fullTitle: "Tóm tắt bỏ túi Chặng 3 & Checklist Tự kiểm tra (Build-Ship-Run & OCI Runtime)" }
  ];

  const CONTAINER_CHANG4_STATIONS = [
    { id: "container-4-1", code: "4.1", title: "Bước ngoặt CRI & Triết lý Khai báo (Declarative YAML)", fullTitle: "Trạm 4.1: Bước ngoặt Chuẩn CRI & Triết lý Khai báo (Immutable Infrastructure, Desired State & GitOps)" },
    { id: "container-4-2", code: "4.2", title: "Bộ não Control Plane & Cơ bắp Worker Nodes (Luồng 9 bước)", fullTitle: "Trạm 4.2: Giải phẫu Bộ não Control Plane (apiserver, etcd, Controller, Scheduler) & Worker Nodes (kubelet, Pod)" },
    { id: "container-4-3", code: "4.3", title: "Vũ khí Vận hành Phân tán (Deployment, Service IPVS, Ingress)", fullTitle: "Trạm 4.3: Vũ khí Vận hành Phân tán (ReplicaSet, Deployment, DaemonSet, Service ClusterIP/IPVS, Ingress & Probes)" },
    { id: "container-4-summary", code: "Kết", title: "Tóm tắt bỏ túi Chặng 4 (Khép kín F06)", fullTitle: "Tóm tắt bỏ túi Chặng 4 & Khép kín Toàn bộ Hành trình Containerization & Orchestration" }
  ];

  function getContainerStations(stageId = activeStorageStage) {
    if (stageId === 1) return CONTAINER_CHANG1_STATIONS;
    if (stageId === 2) return CONTAINER_CHANG2_STATIONS;
    if (stageId === 3) return CONTAINER_CHANG3_STATIONS;
    if (stageId === 4) return CONTAINER_CHANG4_STATIONS;
    return [];
  }

  const INGESTION_STAGES = [
    { id: 1, shortTitle: "Hệ thống Nguồn, GIGO, Push/Pull/Poll & Bố cục Lưu trữ", title: "Chặng 1: Bản Đồ Thu Thập Dữ Liệu & Giải Phẫu Hệ Thống Nguồn (Source Systems)" },
    { id: 2, shortTitle: "Ba Thế Hệ CDC (Timestamp Polling, Trigger & Log-Based WAL)", title: "Chặng 2: Ba Thế Hệ Change Data Capture — Từ Timestamp Polling, Trigger Đến Log-Based CDC" },
    { id: 3, shortTitle: "Hệ Sinh Thái Apache Kafka, KRaft, Partition & Zero-Copy", title: "Chặng 3: Hệ Sinh Thái Apache Kafka & Kiến Trúc Lưu Trữ Sự Kiện Phân Tán" },
    { id: 4, shortTitle: "Producer murmur2, Consumer Group, ISR, EOS & Log Compaction", title: "Chặng 4: Cơ Học Vận Hành Kafka — Producer, Consumer Group, Replication, Delivery Guarantees & Log Model" },
    { id: 5, shortTitle: "Đường Ống Debezium CDC & 4 Thách Thức Vận Hành Thực Chiến", title: "Chặng 5: Đường Ống CDC Thời Gian Thực Với Debezium & Giải Quyết Thách Thức Vận Hành Thực Chiến" }
  ];

  const INGESTION_CHANG1_STATIONS = [
    { id: "ingestion-0-map", code: "0.0", title: "Nhân vật chính Order #8888 & Bản đồ 5 Chặng", fullTitle: "Trạm 0.0: Nhân vật chính Order #8888 & Bản đồ Kiến trúc 5 Chặng Ingestion Layer" },
    { id: "ingestion-1-0-sim", code: "2D", title: "Mô phỏng 2D (6 Slide): Cắt lớp CDC, Kafka, ISR & WAL Bloat", fullTitle: "Trạm 1.0 (Mô phỏng 2D): Phòng Thí Nghiệm Dòng Chảy CDC, Kafka Partition, ISR Failover & WAL Bloat" },
    { id: "ingestion-1-1", code: "1.1", title: "Kiến trúc 5 Tầng Dữ liệu, Data Governance & Định luật GIGO", fullTitle: "Trạm 1.1: Kiến trúc 5 Tầng Dữ liệu, Lớp Quản trị Data Governance & Định luật GIGO tại Hệ thống Nguồn" },
    { id: "ingestion-1-2", code: "1.2", title: "File Ingestion, Structured/Semi/Unstructured & Push-Pull-Poll", fullTitle: "Trạm 1.2: Giải phẫu File Ingestion, Ba Cấp độ Cấu trúc Dữ liệu & Mô hình Push – Pull – Poll" },
    { id: "ingestion-1-3", code: "1.3", title: "OLTP vs OLAP, Bố cục Row/Column/Hybrid, EtLT & Thu thập Logs", fullTitle: "Trạm 1.3: Đối chiếu OLTP vs. OLAP, Bố cục Lưu trữ (Row / Column / Hybrid), Mô hình EtLT & Thu thập Logs" },
    { id: "ingestion-1-summary", code: "Kết", title: "Tóm tắt bỏ túi Chặng 1", fullTitle: "Tóm tắt bỏ túi Chặng 1 & Checklist 5 câu hỏi bản chất" }
  ];

  const INGESTION_CHANG2_STATIONS = [
    { id: "ingestion-2-1", code: "2.1", title: "Bài toán Đồng bộ Biến động (CDC) & Sự sụp đổ của Full-Table Dump", fullTitle: "Trạm 2.1: Bài toán Đồng bộ Biến động (CDC) & Sự Sụp đổ của Full-Table Dump Định kỳ" },
    { id: "ingestion-2-2", code: "2.2", title: "Timestamp-Based Polling CDC, High-Watermark & Bẫy Soft Delete", fullTitle: "Trạm 2.2: Timestamp-Based Polling CDC — Cửa sổ High-Watermark, Cạm bẫy Soft Delete & Chi phí Quét Bảng" },
    { id: "ingestion-2-3", code: "2.3", title: "Trigger-Based CDC, Bảng Bóng Shadow Table & Nhân đôi I/O", fullTitle: "Trạm 2.3: Trigger-Based CDC — Bảng Bóng (Shadow Table), Nhân đôi Ghi I/O & Ác mộng Cascading Triggers" },
    { id: "ingestion-2-4", code: "2.4", title: "Log-Based CDC (WAL / binlog) & Ma trận Đối chiếu 7 Chiều", fullTitle: "Trạm 2.4: Log-Based CDC — Đọc Tuần tự Nhật ký Nhị phân (WAL / binlog) & Đánh đổi Độ phức tạp Giải mã" },
    { id: "ingestion-2-summary", code: "Kết", title: "Tóm tắt bỏ túi Chặng 2", fullTitle: "Tóm tắt bỏ túi Chặng 2 & Checklist 5 câu hỏi bản chất" }
  ];

  const INGESTION_CHANG3_STATIONS = [
    { id: "ingestion-3-1", code: "3.1", title: "Mạng nhện Điểm – Điểm O(N×M) & Trục Sự kiện Apache Kafka", fullTitle: "Trạm 3.1: Nỗi đau Mạng nhện Điểm – Điểm O(N × M) & Sự ra đời của Nền tảng Event Streaming Apache Kafka" },
    { id: "ingestion-3-2", code: "3.2", title: "Điều phối Cụm (ZooKeeper → KRaft) & Hệ sinh thái Connect/MM2", fullTitle: "Trạm 3.2: Bộ máy Điều phối Cụm (ZooKeeper → KRaft Consensus) & Hệ sinh thái Mở rộng (Connect, Streams, MirrorMaker 2)" },
    { id: "ingestion-3-3", code: "3.3", title: "Thiết kế Topic, Toán học Định cỡ Partition & Zero-Copy sendfile(2)", fullTitle: "Trạm 3.3: Sáu Viên gạch Nền tảng, Chiến lược Thiết kế Topic & Toán học Định cỡ Partition (Unit of Parallelism)" },
    { id: "ingestion-3-4", code: "3.4", title: "Con trỏ Offset, Control Records & Độ trễ Consumer Lag", fullTitle: "Trạm 3.4: Giải phẫu Con trỏ Offset, Control Records & Bài toán Độ trễ Tiêu thụ (Consumer Lag)" },
    { id: "ingestion-3-summary", code: "Kết", title: "Tóm tắt bỏ túi Chặng 3", fullTitle: "Tóm tắt bỏ túi Chặng 3 & Checklist 5 câu hỏi bản chất" }
  ];

  const INGESTION_CHANG4_STATIONS = [
    { id: "ingestion-4-1", code: "4.1", title: "Producer Internals: Băm Khóa murmur2 vs Sticky & RecordAccumulator", fullTitle: "Trạm 4.1: Producer Internals — Chiến lược Chọn Partition (Keyed murmur2 Hash vs. Keyless Sticky) & Bộ đệm Gom lô" },
    { id: "ingestion-4-2", code: "4.2", title: "Consumer Groups: Quy tắc 1:1, Fan-out & Cooperative Rebalance", fullTitle: "Trạm 4.2: Consumer Groups — Quy tắc Độc quyền Partition, Đa Nhóm Fan-out & Tái cân bằng (Rebalance)" },
    { id: "ingestion-4-3", code: "4.3", title: "Replication Leader/Follower, Tập hợp ISR & Bầu chọn Tự động", fullTitle: "Trạm 4.3: Replication & Fault Tolerance — Leader/Follower Replicas, Tập hợp ISR & Bầu chọn Tự động khi Sập Broker" },
    { id: "ingestion-4-4", code: "4.4", title: "Ba Cấp độ Giao nhận (At-most/At-least/Exactly-once) & Bẫy acks=1", fullTitle: "Trạm 4.4: Ba Cấp Độ Đảm Bảo Giao Nhận (At-most-once, At-least-once, Exactly-once) & Cạm bẫy Mất Dữ liệu của acks=1" },
    { id: "ingestion-4-5", code: "4.5", title: "Log Segment trên Đĩa (.log/.index) & Nén Nhật ký Log Compaction", fullTitle: "Trạm 4.5: Mô hình Lưu trữ Log Segment trên Đĩa & Ba Chính sách Dọn dẹp (Time, Size & Log Compaction)" },
    { id: "ingestion-4-summary", code: "Kết", title: "Tóm tắt bỏ túi Chặng 4", fullTitle: "Tóm tắt bỏ túi Chặng 4 & Checklist 5 câu hỏi bản chất" }
  ];

  const INGESTION_CHANG5_STATIONS = [
    { id: "ingestion-5-1", code: "5.1", title: "Giải phẫu Debezium: Snapshot → WAL Streaming & Gói tin before/after/op", fullTitle: "Trạm 5.1: Giải phẫu Debezium Log-Based CDC — Chu trình Snapshot sang Streaming WAL & Cấu trúc Gói tin before/after/op" },
    { id: "ingestion-5-2", code: "5.2", title: "Đường ống End-to-End: Đa Nguồn → Debezium → Kafka Connect → Đa Đích", fullTitle: "Trạm 5.2: Kiến trúc Đường ống End-to-End — Từ Đa Hệ quản trị Nguồn qua Debezium & Kafka Connect Đến Đa Đích (Multi-Sink)" },
    { id: "ingestion-5-3", code: "5.3", title: "Bốn Sự cố Thực chiến: Nổ Đĩa WAL Bloat, Schema Drift, Hot Key & Outbox", fullTitle: "Trạm 5.3: Bốn Thách thức Vận hành Thực chiến (Kafka & Debezium Challenges) — WAL Bloat, Schema Drift, Hot Partition & Outbox Pattern" },
    { id: "ingestion-5-summary", code: "Kết", title: "Tóm tắt bỏ túi Chặng 5 (Khép kín D01)", fullTitle: "Tóm tắt bỏ túi Chặng 5 & Khép kín Toàn bộ Học phần D01 · Ingestion Layer" }
  ];

  function getIngestionStations(stageId = activeStorageStage) {
    if (stageId === 1) return INGESTION_CHANG1_STATIONS;
    if (stageId === 2) return INGESTION_CHANG2_STATIONS;
    if (stageId === 3) return INGESTION_CHANG3_STATIONS;
    if (stageId === 4) return INGESTION_CHANG4_STATIONS;
    if (stageId === 5) return INGESTION_CHANG5_STATIONS;
    return [];
  }

  function getTopicStages(topic = activeTopic) {
    if (topic === "F01") return LINUX_STAGES;
    if (topic === "F03") return DB_STAGES;
    if (topic === "F06") return CONTAINER_STAGES;
    if (topic === "D01") return INGESTION_STAGES;
    if (topic === "D02") return STORAGE_STAGES;
    return [];
  }

  function getTopicStations(topic = activeTopic, stageId = activeStorageStage) {
    if (topic === "F01") return getLinuxStations(stageId);
    if (topic === "F03") return getDbStations(stageId);
    if (topic === "F06") return getContainerStations(stageId);
    if (topic === "D01") return getIngestionStations(stageId);
    if (topic === "D02") return getStorageStations(stageId);
    return [];
  }

  const state = {
    topic: "F01",
    stage: 1,
    section: "linux-0-map"
  };
  let activeTopic = state.topic;
  let activeStorageStage = state.stage;
  let activeStationId = state.section;

  function syncStateVars(topic, stage, section) {
    if (topic !== undefined && topic !== null) {
      state.topic = topic;
      activeTopic = topic;
    }
    if (stage !== undefined && stage !== null) {
      state.stage = Number(stage) || 1;
      activeStorageStage = state.stage;
    }
    if (section !== undefined) {
      state.section = section;
      activeStationId = section;
    }
  }

  function formatRouteHash(topic = state.topic, stage = state.stage, section = null) {
    const cleanTopic = String(topic || "F01").trim();
    if (cleanTopic === "CATALOG") return "#/catalog";
    if (cleanTopic === "GLOSSARY") return "#/glossary";
    const cleanStage = Number(stage) || 1;
    if (section) {
      return `#/${cleanTopic}/${cleanStage}/${section}`;
    }
    return `#/${cleanTopic}/${cleanStage}`;
  }

  function parseRouteHash(rawHash = window.location.hash) {
    const h = String(rawHash || "").replace(/^#/, "").trim();
    if (!h) return { topic: null, stage: null, section: null };
    if (h === "/catalog" || h === "catalog") {
      return { topic: "CATALOG", stage: 1, section: null };
    }
    if (h === "/glossary" || h === "glossary") {
      return { topic: "GLOSSARY", stage: 1, section: null };
    }
    if (h.startsWith("/")) {
      const parts = h.slice(1).split("/").filter(Boolean);
      const t0 = parts[0] ? decodeURIComponent(parts[0]) : null;
      if (t0 && t0.toLowerCase() === "catalog") return { topic: "CATALOG", stage: 1, section: null };
      if (t0 && t0.toLowerCase() === "glossary") return { topic: "GLOSSARY", stage: 1, section: null };
      return {
        topic: t0,
        stage: parts[1] ? (Number(parts[1]) || 1) : null,
        section: parts[2] ? decodeURIComponent(parts[2]) : null
      };
    }
    if (h.includes("topic=") || h.includes("stage=") || h.includes("section=")) {
      const params = new URLSearchParams(h);
      return {
        topic: params.get("topic") || null,
        stage: params.get("stage") ? (Number(params.get("stage")) || 1) : null,
        section: params.get("section") || null
      };
    }
    return { topic: null, stage: null, section: h };
  }

  let expandedTracks = new Set(["track-1", "track-2"]);
  let scrollObserver = null;
  let currentExpandSafeId = null;
  let lastExpandTriggerEl = null;

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
    return { group: SYLLABUS_GROUPS[0], item: SYLLABUS_GROUPS[0].items[0] };
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
     ANTHROPIC ACADEMY COURSE OVERVIEW CALLOUT & COLORED ASCII SANDBOX BUILDER
     ========================================================================== */
  function buildSpineHeroBanner({ id, badge, title, subtitle, captionHtml }) {
    const safeId = String(id || "spine").replace(/[^a-zA-Z0-9_-]/g, "_");
    return `
      <aside class="spine-overview-card" id="spine-hero-${safeId}" aria-label="${escapeHtml(title)}">
        <div class="spine-overview-head">
          <div class="spine-overview-title-wrap">
            <span class="spine-overview-badge">${escapeHtml(badge || "Trong bài học này")}</span>
            <strong class="spine-overview-title">${escapeHtml(title)}</strong>
          </div>
          ${subtitle ? `<span class="spine-overview-sub hide-mobile">${escapeHtml(subtitle)}</span>` : ""}
        </div>
        <div class="spine-overview-body"><span class="cds-icon" style="color:var(--accent-clay);margin-right:4px;" aria-hidden="true">&#xE02A;</span>${captionHtml}</div>
      </aside>
    `;
  }

  function toggleAsciiAnimation() {
    const paused = document.body.classList.toggle("ascii-anim-paused");
    document.querySelectorAll(".ascii-anim-btn").forEach(b => {
      b.setAttribute("aria-pressed", paused ? "false" : "true");
      b.textContent = paused ? "Hiệu ứng: Tắt" : "Hiệu ứng: Bật";
    });
    showToast(paused ? "Đã tắt hiệu ứng dòng chảy ASCII" : "Đã bật hiệu ứng dòng chảy ASCII (Durdraw)");
  }

  function buildVisualBlock(id, title, asciiText, caption, asciiHtml = null, maxCols = null, isFlagship = false) {
    const safeId = id.replace(/[^a-zA-Z0-9_-]/g, "_");
    const cols = maxCols || Math.max(60, ...String(asciiText || "").split("\n").map(l => l.length));
    const renderedAscii = asciiHtml || escapeHtml(asciiText);

    window.__diagrams = window.__diagrams || {};
    window.__diagrams[safeId] = {
      ascii: asciiText,
      asciiHtml: renderedAscii,
      maxCols: cols,
      flagship: Boolean(isFlagship),
      title,
      caption: caption || ""
    };

    return `
      <figure class="visual-card" id="vcard-${safeId}"${isFlagship ? ' data-flagship="true"' : ""}>
        <div class="visual-bar">
          <div class="visual-bar-title">
            <span class="visual-window-dots" aria-hidden="true"><span></span><span></span><span></span></span>
            <span>${escapeHtml(title)}</span>
          </div>
          <div class="visual-controls">
            <button type="button" class="ui-btn" onclick="copyDiagram('${safeId}')">Sao chép</button>
            <button type="button" class="ui-btn" onclick="openExpandModal('${safeId}', this)">Phóng to</button>
          </div>
        </div>
        <div class="visual-pane pane-ascii" id="pane-ascii-${safeId}">
          <pre class="ascii-diagram" style="--ascii-cols: ${cols};" tabindex="0" aria-label="${escapeHtml(title)}">${renderedAscii}</pre>
        </div>
        ${caption ? `<figcaption class="visual-caption">${caption}</figcaption>` : ""}
      </figure>
    `;
  }

  function copyDiagram(safeId) {
    const item = window.__diagrams?.[safeId];
    if (!item) return;
    copyText(item.ascii, "sơ đồ ASCII");
  }

  function openExpandModal(safeId, triggerEl = null) {
    const item = window.__diagrams?.[safeId];
    if (!item) return;
    lastExpandTriggerEl = triggerEl || document.activeElement;
    currentExpandSafeId = safeId;

    const modal = document.getElementById("expandModal");
    document.getElementById("expandModalTitle").textContent = item.title;
    const copyBtn = document.getElementById("expandCopyBtn");
    if (copyBtn) {
      copyBtn.onclick = () => copyDiagram(safeId);
    }
    const body = document.getElementById("expandModalBody");
    body.innerHTML = `<pre class="ascii-diagram" style="--ascii-cols: ${item.maxCols || 96};" tabindex="0">${item.asciiHtml || escapeHtml(item.ascii)}</pre>`;
    modal.classList.add("open");
  }

  function closeExpandModal() {
    document.getElementById("expandModal").classList.remove("open");
    if (lastExpandTriggerEl && typeof lastExpandTriggerEl.focus === "function") {
      lastExpandTriggerEl.focus();
      lastExpandTriggerEl = null;
    }
  }

  /* ==========================================================================
     EXTRACTED LESSON RENDERERS (content/lessons/{D02,F01,F03,F06}/stage-{n}.html)
     ========================================================================== */
__LESSON_TEMPLATES_JS__

  /* ==========================================================================
     INTERACTIVE 2D SIMULATOR: CHUYỆN TIỆM BÁNH CỦA MINH (8 SLIDES)
     ========================================================================== */
  let infra2dCurrentSlide = 0;
  let infra2dState = {
    sliced: false,
    productMode: "none",
    noisyNeighbor: false,
    vpsNeighborOverload: false,
    vpsHardwareCrash: false,
    cloudNodeACrash: false,
    cloudScaled: false,
    dedicatedTurbo: false,
    dedicatedUpgrading: false,
    raceStarted: false,
    serverlessMode: "idle",
    selectedCase: 0
  };

  const INFRA2D_SLIDES = [
    {
      id: "vm-root",
      shortNav: "Gốc VM",
      chapter: "Gốc rễ khái niệm",
      analogy: "Ẩn dụ BĐS: Công nghệ cắt đất vs. Căn hộ bán ra",
      title: "1. Tại sao dễ nhầm? \"VM\" khác gì \"VPS\" và \"Cloud VM\"?",
      minhTitle: "Minh bối rối ngày đầu tìm hiểu:",
      minhStory: "“Em định mở web bán bánh ngọt mà người bảo thuê VPS, người bảo tạo VM, người lại khuyên lên Cloud VM. Rốt cuộc 3 thứ này là một hay khác nhau?”",
      keypoints: [
        { badge: "VM", title: "VM (Virtual Machine) là CÔNG NGHỆ", desc: "Là kỹ thuật dùng phần mềm (Hypervisor) cắt 1 máy chủ vật lý khổng lồ thành nhiều máy tính ảo nhỏ độc lập." },
        { badge: "SP", title: "VPS & Cloud VM là SẢN PHẨM THƯƠNG MẠI", desc: "Nhà cung cấp dùng công nghệ VM tạo sẵn máy ảo trên Internet rồi đóng gói bán cho bạn thuê theo tháng/giờ." },
        { badge: "VD", title: "Ví dụ dễ hiểu nhất", desc: "Giống như \"Động cơ đốt trong\" là công nghệ (VM), còn \"Xe máy Honda\" (VPS) hay \"Xe hơi\" (Cloud VM) là sản phẩm dùng động cơ đó!" }
      ],
      verdict: "<strong>Chốt ngắn gọn:</strong> Tạo máy ảo trên Laptop cá nhân = <strong>VM</strong>. Thuê máy ảo trên 1 máy chủ đơn lẻ = <strong>VPS</strong>. Thuê máy ảo trên cụm đám mây = <strong>Cloud VM</strong>."
    },
    {
      id: "shared-hosting",
      shortNav: "Hosting",
      chapter: "Chương 1: Khởi nghiệp 100k",
      analogy: "Ẩn dụ BĐS: Thuê 1 chiếc giường trong Ký túc xá",
      title: "2. Shared Hosting – \"Ở Ghép Ký Túc Xá Sinh Viên\"",
      minhTitle: "Minh mở web giới thiệu tiệm bánh:",
      minhStory: "“Mình mới bán bánh vốn ít, lại mù tịt Linux. Mình thuê Shared Hosting giá 50k/tháng, có sẵn bảng điều khiển cPanel chỉ việc thả code WordPress vào là chạy!”",
      keypoints: [
        { badge: "ALL", title: "Dùng chung mọi thứ", desc: "Hàng trăm website cùng nằm chung trong 1 phòng, dùng chung CPU, RAM và 1 đường ống nước (Băng thông/IP)." },
        { badge: "NO", title: "Không có chìa khóa phòng (Không có quyền Root)", desc: "Ban quản lý cài sẵn gì dùng nấy, Minh không được tự ý cài phần mềm lạ hay đập sửa tường." },
        { badge: "503", title: "Rủi ro: Hàng xóm ồn ào (Noisy Neighbor)", desc: "Nếu 1 web cùng phòng bị tấn công DDoS hoặc ngốn sạch RAM, web tiệm bánh của Minh cũng bị đơ theo!" }
      ],
      verdict: "<strong>Khi nào dùng?</strong> Web giới thiệu, blog nhỏ, mới học làm web, ngân sách siêu tiết kiệm."
    },
    {
      id: "vps",
      shortNav: "VPS",
      chapter: "Chương 2: Ra riêng tự chủ",
      analogy: "Ẩn dụ BĐS: Căn hộ khép kín trong 1 tòa chung cư",
      title: "3. VPS (Virtual Private Server) – \"Chung Cư Mini Riêng Biệt\"",
      minhTitle: "Khách mua bánh đông lên, Minh chuyển nhà:",
      minhStory: "“Chán cảnh hàng xóm làm tắc nước ở ký túc xá, mình thuê hẳn 1 căn VPS! Có tường ngăn riêng, đồng hồ điện nước riêng và chìa khóa tự do đập sửa.”",
      keypoints: [
        { badge: "ISO", title: "Tài nguyên cách ly + Toàn quyền Root", desc: "Minh được cam kết riêng 4 CPU, 8GB RAM. Hàng xóm bên cạnh có quá tải thì tiệm bánh của Minh vẫn chạy mượt." },
        { badge: "SU", title: "Tự do cài đặt mọi thứ", desc: "Minh toàn quyền chọn hệ điều hành Ubuntu/CentOS, cài Docker, cấu hình tường lửa theo ý thích." },
        { badge: "SPOF", title: "Điểm yếu chí mạng: Nằm trên 1 tòa nhà duy nhất!", desc: "Nếu máy chủ vật lý mẹ bị cháy ổ cứng hoặc hỏng nguồn, căn hộ VPS của Minh sẽ SẬP ngay lập tức." }
      ],
      verdict: "<strong>Khi nào dùng?</strong> Web vừa và nhỏ, môi trường Dev/Test, cần quyền Root với chi phí cố định hàng tháng."
    },
    {
      id: "cloud-vm",
      shortNav: "Cloud VM",
      chapter: "Chương 3: Lên mây bất tử",
      analogy: "Ẩn dụ BĐS: Căn hộ thông minh trong Siêu đô thị liên kết",
      title: "4. Cloud VM (Cloud Server) – \"Tự Dịch Chuyển Khi Có Sự Cố\"",
      minhTitle: "Sau vụ sập VPS ngày Valentine, Minh lên Cloud:",
      minhStory: "“Đúng lễ Valentine thì máy chủ vật lý của bên VPS cháy ổ cứng làm mình mất trăm đơn bánh! Mình chuyển sang Cloud VM để không bao giờ sợ hỏng phần cứng nữa.”",
      keypoints: [
        { badge: "SAN", title: "Khác VPS ở đâu? Ở hạ tầng cụm máy chủ!", desc: "VPS nằm trên 1 máy lẻ. Còn Cloud VM nằm trên hàng trăm máy chủ nối mạng với nhau + Hầm dữ liệu tách rời (sao lưu 3 bản Ceph/SAN)." },
        { badge: "HA", title: "Tự phục hồi (Failover / Live Migration)", desc: "Tòa nhà số 1 bị mất điện? Đám mây tự động bế căn hộ của Minh sang Tòa nhà số 2 trong tích tắc, web vẫn sống!" },
        { badge: "x10", title: "Co giãn linh hoạt (Auto-Scaling)", desc: "Dịp Trung Thu khách tăng gấp 10? Kéo thanh trượt tăng RAM/CPU hoặc nhân bản máy ảo trong vài giây, hết lễ thu nhỏ lại." }
      ],
      verdict: "<strong>Khi nào dùng?</strong> Web thương mại điện tử, hệ thống công ty, dự án cấm sập (Downtime = Mất tiền)."
    },
    {
      id: "dedicated",
      shortNav: "Dedicated",
      chapter: "Chương 4: Độc quyền phần cứng",
      analogy: "Ẩn dụ BĐS: Thuê đứt nguyên một căn Biệt thự mặt đất",
      title: "5. Dedicated Server (Bare Metal) – \"Nguyên Cỗ Máy Vật Lý\"",
      minhTitle: "Chuỗi bánh của Minh thành Tập đoàn lớn:",
      minhStory: "“Khi công ty xử lý hàng triệu giao dịch tài chính và AI nặng mỗi giây, mình thuê đứt nguyên một cỗ máy chủ vật lý thật trong Data Center, không chia sẻ với ai!”",
      keypoints: [
        { badge: "100%", title: "100% Hiệu năng trần (Không qua Hypervisor)", desc: "Không bị hao hụt 2-5% sức mạnh cho lớp phần mềm cắt máy ảo. Toàn bộ CPU và RAM vật lý thuộc về một mình bạn." },
        { badge: "SEC", title: "Bảo mật vật lý tuyệt đối", desc: "Phù hợp tiêu chuẩn ngân hàng, y tế hoặc game server cực lớn cấm nằm chung phần cứng với khách hàng khác." },
        { badge: "RAM", title: "Kém linh hoạt & Đắt đỏ", desc: "Muốn nâng cấp thêm RAM? Phải chờ kỹ thuật viên cầm tua-vít ra cắm thanh RAM thật vào bo mạch!" }
      ],
      verdict: "<strong>Khi nào dùng?</strong> Tập đoàn lớn, Big Data, AI, Ngân hàng cần hiệu năng vật lý tối đa."
    },
    {
      id: "container",
      shortNav: "Container",
      chapter: "Chương 5: Cách mạng đóng gói",
      analogy: "Ẩn dụ BĐS: Thùng Container lắp ghép tiêu chuẩn hóa",
      title: "6. Container (Docker) – \"Nhẹ Gấp Bội So Với Máy Ảo\"",
      minhTitle: "Đội kỹ sư của Minh tối ưu tốc độ:",
      minhStory: "“Mỗi lần bật thêm 1 máy ảo (VM) phải chờ 2 phút vì nó phải khởi động cả một Hệ điều hành riêng nặng hàng chục GB. Dùng Container (Docker), tiệm bánh khởi động chỉ mất 1 giây!”",
      keypoints: [
        { badge: "TAX", title: "Nỗi đau của VM: Cõng nhiều Hệ điều hành", desc: "Tạo 3 máy ảo là phải nuôi 3 bản Hệ điều hành (Guest OS) ngốn rất nhiều RAM (12GB) và ổ cứng." },
        { badge: "OCI", title: "Giải pháp Container: Dùng chung nhân HĐH", desc: "Container chỉ đóng gói đúng \"Code tiệm bánh + Thư viện cần thiết\" vào 1 chiếc hộp siêu nhẹ, dùng chung nền móng Host OS Kernel." },
        { badge: "1s", title: "Khởi động 1 giây & Chạy mọi nơi", desc: "Đặt thùng Container lên Laptop, VPS hay Cloud VM đều chạy giống hệt nhau, chấm dứt cảnh \"Máy em chạy được mà lên Server lại lỗi!\"" }
      ],
      verdict: "<strong>Thực tế:</strong> Ngày nay người ta thường thuê <strong>VPS / Cloud VM</strong> rồi cài <strong>Docker Container</strong> lên bên trong!"
    },
    {
      id: "serverless",
      shortNav: "Serverless",
      chapter: "Chương 6: Quên luôn máy chủ",
      analogy: "Ẩn dụ BĐS: Thuê dịch vụ bếp nướng bánh theo từng đơn",
      title: "7. PaaS & Serverless – \"Chỉ Đưa Công Thức, Không Lo Nhà Cửa\"",
      minhTitle: "Minh muốn rảnh tay 100% để sáng tạo bánh mới:",
      minhStory: "“Mình không muốn thức đêm canh máy chủ hay cập nhật bảo mật Linux nữa! Mình đẩy thẳng Code lên Serverless (Vercel / Cloud Run / Lambda), có khách mua hệ thống mới tính tiền!”",
      keypoints: [
        { badge: "GIT", title: "Chỉ cần giao Công thức bánh (Code)", desc: "Nhà cung cấp lo toàn bộ máy chủ bên dưới. Bạn không cần biết mặt mũi con server trông như thế nào." },
        { badge: "AUTO", title: "Co giãn từ 0 đến Hàng nghìn trong tích tắc", desc: "Có 1 khách bấm mua -> Bật 1 bếp nướng trong 0.2 giây (200ms) rồi tắt. Có 5.000 khách cùng lúc -> Tự nhân bản 5.000 bếp!" },
        { badge: "0VND", title: "Ban đêm không có khách = 0 Đồng (Scale-to-Zero)", desc: "Khác với VPS phải trả tiền cả khi nửa đêm không ai vào web, Serverless chỉ thu phí đúng số mili-giây code chạy." }
      ],
      verdict: "<strong>Khi nào dùng?</strong> Startup muốn ra mắt sản phẩm thần tốc, API, Web hiện đại không muốn thuê nhân sự quản trị mạng."
    },
    {
      id: "advisor",
      shortNav: "Tư vấn",
      chapter: "Tổng kết & Thực chiến",
      analogy: "La bàn chọn đúng hạ tầng trong 5 giây",
      title: "8. Câu Thần Chú Ghi Nhớ & Máy Tư Vấn Hạ Tầng",
      minhTitle: "Minh đúc kết bí kíp cho bạn:",
      minhStory: "“Đi từ tiệm bánh nhỏ đến chuỗi cửa hàng lớn, mình nhận ra không có hạ tầng nào tốt nhất cho mọi thứ, chỉ có hạ tầng phù hợp nhất với giai đoạn của bạn!”",
      keypoints: [
        { badge: "P1", title: "Thần chú phần 1: Công nghệ & Lưu trữ truyền thống", desc: "“VM là công nghệ chia máy. Hosting là ở ghép ký túc. VPS là chung cư đơn lẻ. Cloud VM là đô thị liên hoàn.”" },
        { badge: "P2", title: "Thần chú phần 2: Hạ tầng hiện đại", desc: "“Dedicated là biệt thự nguyên căn. Container là nhà hộp lắp ghép. Còn Serverless là thuê bếp nướng theo giờ!”" },
        { badge: "TRY", title: "Thử ngay Máy Tư Vấn bên phải", desc: "Hãy bấm chọn 1 trong 4 tình huống dự án thực tế ở khung bên phải để xem kiến trúc khuyên dùng!" }
      ],
      verdict: "<strong>Tổng kết:</strong> Bạn đã nắm vững toàn bộ bản đồ hạ tầng máy chủ từ gốc rễ kỹ thuật đến ứng dụng thực tế."
    }
  ];

  function goToInfra2DSlide(idx) {
    if (idx < 0 || idx >= INFRA2D_SLIDES.length) return;
    infra2dCurrentSlide = idx;
    infra2dState = {
      sliced: false,
      productMode: "none",
      noisyNeighbor: false,
      vpsNeighborOverload: false,
      vpsHardwareCrash: false,
      cloudNodeACrash: false,
      cloudScaled: false,
      dedicatedTurbo: false,
      dedicatedUpgrading: false,
      raceStarted: false,
      serverlessMode: "idle",
      selectedCase: 0
    };
    renderInfra2DSlide();
  }

  function changeInfra2DSlide(delta) {
    goToInfra2DSlide(infra2dCurrentSlide + delta);
  }

  function toggleInfra2DSummaryModal() {
    const panel = document.getElementById("infra2dSummaryDrawer");
    if (!panel) return;
    panel.style.display = panel.style.display === "none" ? "block" : "none";
  }

  function renderInfra2DSlide() {
    const root = document.getElementById("infra2dWidgetRoot");
    if (!root) return;
    const slide = INFRA2D_SLIDES[infra2dCurrentSlide] || INFRA2D_SLIDES[0];

    const dotsEl = document.getElementById("infra2dDots");
    if (dotsEl) {
      dotsEl.innerHTML = INFRA2D_SLIDES.map((s, idx) => `
        <button type="button" class="infra2d-dot-btn ${idx === infra2dCurrentSlide ? 'active' : ''}" onclick="goToInfra2DSlide(${idx})">
          ${idx + 1}. ${escapeHtml(s.shortNav)}
        </button>
      `).join("");
    }

    const chBadge = document.getElementById("infra2dChapterBadge");
    if (chBadge) chBadge.textContent = slide.chapter;
    const numPill = document.getElementById("infra2dSlideNumPill");
    if (numPill) numPill.textContent = `SLIDE ${infra2dCurrentSlide + 1} / ${INFRA2D_SLIDES.length}`;
    const anaPill = document.getElementById("infra2dAnalogyPill");
    if (anaPill) anaPill.textContent = slide.analogy;
    const titleEl = document.getElementById("infra2dSlideTitle");
    if (titleEl) titleEl.textContent = slide.title;
    const mTitle = document.getElementById("infra2dMinhTitle");
    if (mTitle) mTitle.textContent = slide.minhTitle;
    const mStory = document.getElementById("infra2dMinhStory");
    if (mStory) mStory.textContent = slide.minhStory;

    const kpEl = document.getElementById("infra2dKeypoints");
    if (kpEl) {
      kpEl.innerHTML = slide.keypoints.map(kp => `
        <div class="infra2d-kp-item">
          <div class="infra2d-kp-badge">${escapeHtml(kp.badge)}</div>
          <div>
            <div class="infra2d-kp-title">${escapeHtml(kp.title)}</div>
            <p class="infra2d-kp-desc">${escapeHtml(kp.desc)}</p>
          </div>
        </div>
      `).join("");
    }

    const vEl = document.getElementById("infra2dVerdictBox");
    if (vEl) vEl.innerHTML = slide.verdict;

    const prevBtn = document.getElementById("infra2dBtnPrev");
    if (prevBtn) prevBtn.disabled = (infra2dCurrentSlide === 0);
    const nextBtn = document.getElementById("infra2dBtnNext");
    if (nextBtn) {
      if (infra2dCurrentSlide === INFRA2D_SLIDES.length - 1) {
        nextBtn.textContent = "Xem Bảng Tổng Hợp →";
        nextBtn.onclick = () => toggleInfra2DSummaryModal();
      } else {
        nextBtn.textContent = "Slide Tiếp Theo →";
        nextBtn.onclick = () => changeInfra2DSlide(1);
      }
    }
    const progEl = document.getElementById("infra2dProgressFill");
    if (progEl) {
      progEl.style.width = `${((infra2dCurrentSlide + 1) / INFRA2D_SLIDES.length) * 100}%`;
    }

    renderInfra2DSimStage();
  }

  function renderInfra2DSimStage() {
    const stage = document.getElementById("infra2dSimStage");
    const controls = document.getElementById("infra2dSimControls");
    const statusText = document.getElementById("infra2dSimStatusText");
    if (!stage || !controls || !statusText) return;

    if (infra2dCurrentSlide === 0) {
      if (!infra2dState.sliced) {
        statusText.innerHTML = "<strong>[TRẠNG THÁI]:</strong> Đây là <strong>1 Máy chủ vật lý khổng lồ (64 CPU, 256GB RAM)</strong>. Hãy bấm nút cắt máy bằng Hypervisor!";
        stage.innerHTML = `
          <div class="infra2d-box infra2d-float" style="max-width:420px;width:100%;border-color:var(--sim-clay);padding:18px;">
            <div style="font-size:11px;font-weight:800;color:var(--sim-clay);letter-spacing:0.06em;">MÁY CHỦ VẬT LÝ NGUYÊN KHỐI (BARE METAL HOST)</div>
            <div style="font-size:18px;font-weight:800;color:var(--sim-ink);margin:8px 0 4px;">64 CPU • 256 GB RAM</div>
            <p style="font-size:12px;color:var(--sim-muted);margin:0 0 12px !important;">Quá to cho 1 tiệm bánh nhỏ! Nếu chỉ chạy 1 web sẽ lãng phí 95% sức mạnh.</p>
            <div style="padding:8px 10px;border-radius:8px;background:var(--sim-canvas);border:1px solid var(--sim-border);font-size:12px;color:var(--sim-warn);">
              [CHƯA ẢO HÓA] Chưa cài phần mềm <strong>Hypervisor</strong>
            </div>
          </div>
        `;
      } else {
        let badgeLabel = "CÔNG NGHỆ GỐC: MÁY ẢO (VIRTUAL MACHINE - VM)";
        let subNote = "<strong>[KẾT QUẢ]:</strong> Mỗi ô là 1 <strong>Virtual Machine (VM)</strong> có Hệ điều hành riêng, tưởng mình là máy thật!";
        let borderCol = "var(--sim-flow)";
        let tagName = "Máy Ảo VM";
        if (infra2dState.productMode === "vps") {
          badgeLabel = "SẢN PHẨM 2: ĐÓNG GÓI THÀNH \"VPS\" CHO THUÊ THEO THÁNG";
          subNote = "<strong>[VPS]:</strong> Nhà mạng gắn IP Internet vào từng chiếc VM trên cỗ máy đơn lẻ này rồi bán lẻ cho Minh thuê = <strong>VPS</strong>!";
          borderCol = "var(--sim-clay)";
          tagName = "Gói VPS";
        } else if (infra2dState.productMode === "cloud") {
          badgeLabel = "SẢN PHẨM 3: ĐÓNG GÓI THÀNH \"CLOUD VM\" TRÊN ĐÁM MÂY";
          subNote = "<strong>[CLOUD VM]:</strong> Vẫn là chiếc VM đó, nhưng đặt trên hệ thống hàng trăm máy chủ liên kết tự phục hồi = <strong>Cloud VM</strong>!";
          borderCol = "var(--sim-ok)";
          tagName = "Cloud VM";
        }
        statusText.innerHTML = subNote;
        stage.innerHTML = `
          <div style="width:100%;max-width:480px;">
            <div style="text-align:center;margin-bottom:8px;">
              <span class="infra2d-tag">${badgeLabel}</span>
            </div>
            <div class="infra2d-box" style="padding:12px;">
              <div class="infra2d-card-grid2" style="margin-bottom:10px;">
                ${[1, 2, 3, 4].map(n => `
                  <div class="infra2d-box" style="border-color:${borderCol};background:var(--sim-card);">
                    <div style="font-size:12.5px;font-weight:800;color:var(--sim-ink);">${tagName} #${n}</div>
                    <div style="font-size:11px;color:var(--sim-sub);margin:2px 0;">16 CPU • 64GB RAM</div>
                    <span style="display:inline-block;font-size:10.5px;padding:2px 6px;border-radius:4px;background:var(--sim-card-alt);color:var(--sim-ok);">HĐH Ubuntu Riêng</span>
                  </div>
                `).join("")}
              </div>
              <div style="padding:6px;border-radius:6px;background:linear-gradient(90deg,var(--sim-danger),var(--sim-warn),var(--sim-danger));color:#faf9f5;font-weight:800;font-size:11.5px;text-align:center;">
                LỚP CẮT ẢO HÓA HYPERVISOR (KVM / VMware ESXi)
              </div>
              <div style="margin-top:6px;font-size:11px;color:var(--sim-muted);text-align:center;">
                Phần cứng máy chủ vật lý bên dưới (64 CPU • 256 GB RAM)
              </div>
            </div>
          </div>
        `;
      }
      controls.innerHTML = `
        <button type="button" class="infra2d-btn ${!infra2dState.sliced ? 'infra2d-btn-primary' : ''}" onclick="infra2dState.sliced = !infra2dState.sliced; infra2dState.productMode = 'none'; renderInfra2DSimStage();">
          ${!infra2dState.sliced ? '1. Bấm cắt máy bằng Hypervisor (Tạo VM)' : 'Gộp lại máy vật lý'}
        </button>
        <button type="button" class="infra2d-btn" onclick="infra2dState.sliced = true; infra2dState.productMode = 'vps'; renderInfra2DSimStage();">
          2. Biến VM thành gói VPS
        </button>
        <button type="button" class="infra2d-btn" onclick="infra2dState.sliced = true; infra2dState.productMode = 'cloud'; renderInfra2DSimStage();">
          3. Biến VM thành Cloud VM
        </button>
      `;
    } else if (infra2dCurrentSlide === 1) {
      const noisy = infra2dState.noisyNeighbor;
      statusText.innerHTML = noisy
        ? "<strong>[HIỆU ỨNG HÀNG XÓM ỒN ÀO - NOISY NEIGHBOR]:</strong> Web hàng xóm số 2 bị tấn công DDoS hút cạn 95% ống nước CPU/RAM chung! Tiệm bánh của Minh bị vạ lây báo lỗi 503!"
        : "<strong>[TRẠNG THÁI BÌNH THƯỜNG]:</strong> 4 giường ký túc xá ôn hòa chia nhau ống nước CPU/RAM chung. Web của Minh chạy ổn với giá 50k/tháng.";
      stage.innerHTML = `
        <div style="width:100%;max-width:480px;">
          <div class="infra2d-box" style="margin-bottom:10px;text-align:left;">
            <div style="display:flex;justify-content:space-between;font-size:12px;font-weight:700;margin-bottom:6px;">
              <span style="color:var(--sim-flow);">Ống nước Tài nguyên Dùng chung (CPU &amp; RAM chung)</span>
              <span style="color:${noisy ? 'var(--sim-danger)' : 'var(--sim-ok)'};">${noisy ? '99% CẠN KIỆT!' : '35% Ổn định'}</span>
            </div>
            <div style="width:100%;height:12px;background:var(--sim-card-alt);border-radius:999px;overflow:hidden;display:flex;">
              <div style="height:100%;background:var(--sim-warn);width:${noisy ? '4%' : '15%'};transition:width 0.4s;"></div>
              <div style="height:100%;background:${noisy ? 'var(--sim-danger)' : 'var(--sim-flow)'};width:${noisy ? '95%' : '20%'};transition:width 0.4s;"></div>
            </div>
          </div>
          <div class="infra2d-box ${noisy ? 'infra2d-glow-danger' : ''}" style="padding:12px;">
            <div style="font-size:11.5px;font-weight:700;color:var(--sim-muted);margin-bottom:8px;">
              PHÒNG KÝ TÚC XÁ SHARED HOSTING (Không có vách ngăn tài nguyên)
            </div>
            <div class="infra2d-card-grid2">
              <div class="infra2d-box" style="border-color:${noisy ? 'var(--sim-danger)' : 'var(--sim-warn)'};background:${noisy ? 'var(--sim-danger-soft)' : 'var(--sim-warn-soft)'};">
                <div style="font-size:12px;font-weight:800;color:var(--sim-warn);">Giường 1: Tiệm Bánh Minh</div>
                <div style="font-size:11px;font-weight:700;margin-top:4px;color:${noisy ? 'var(--sim-danger)' : 'var(--sim-ok)'};">
                  ${noisy ? '[LỖI 503] Mất nước oan!' : '[ONLINE] Đang mở cửa (20 khách)'}
                </div>
              </div>
              <div class="infra2d-box ${noisy ? 'infra2d-shake' : ''}" style="border-color:${noisy ? 'var(--sim-danger)' : 'var(--sim-border)'};background:${noisy ? 'var(--sim-danger-soft)' : 'var(--sim-border)'};">
                <div style="font-size:12px;font-weight:800;color:var(--sim-ink);">Giường 2: Web Hàng Xóm</div>
                <div style="font-size:11px;font-weight:700;margin-top:4px;color:${noisy ? 'var(--sim-danger)' : 'var(--sim-muted)'};">
                  ${noisy ? '[DDoS] Hút cạn 95% RAM!' : '[ONLINE] Bình thường'}
                </div>
              </div>
              <div class="infra2d-box" style="padding:8px;">
                <div style="font-size:11.5px;font-weight:700;color:var(--sim-sub);">Giường 3: Blog Cá Nhân</div>
                <div style="font-size:10.5px;color:${noisy ? 'var(--sim-danger)' : 'var(--sim-muted)'};">${noisy ? '[503] Treo theo' : '[OK] Bình thường'}</div>
              </div>
              <div class="infra2d-box" style="padding:8px;">
                <div style="font-size:11.5px;font-weight:700;color:var(--sim-sub);">Giường 4: Web Áo Quần</div>
                <div style="font-size:10.5px;color:${noisy ? 'var(--sim-danger)' : 'var(--sim-muted)'};">${noisy ? '[503] Treo theo' : '[OK] Bình thường'}</div>
              </div>
            </div>
          </div>
        </div>
      `;
      controls.innerHTML = `
        <button type="button" class="infra2d-btn infra2d-btn-danger" onclick="infra2dState.noisyNeighbor = true; renderInfra2DSimStage();">
          1. Cho Hàng Xóm Mở Tiệc / Bị DDoS (Noisy Neighbor)
        </button>
        <button type="button" class="infra2d-btn" onclick="infra2dState.noisyNeighbor = false; renderInfra2DSimStage();">
          2. Khôi phục bình yên
        </button>
      `;
    } else if (infra2dCurrentSlide === 2) {
      const neighborHot = infra2dState.vpsNeighborOverload;
      const crashed = infra2dState.vpsHardwareCrash;
      if (crashed) {
        statusText.innerHTML = "<strong>[ĐIỂM YẾU CHÍ MẠNG CỦA VPS - SPOF]:</strong> Máy chủ vật lý mẹ bị cháy ổ cứng! Vì toàn bộ căn hộ VPS nằm trên 1 tòa nhà duy nhất nên Tiệm bánh của Minh SẬP NGAY LẬP TỨC!";
      } else if (neighborHot) {
        statusText.innerHTML = "<strong>[ƯU ĐIỂM CỦA VPS]:</strong> Nhờ tường gạch Hypervisor ngăn căn hộ riêng, hàng xóm có quá tải 100% CPU của họ thì căn hộ VPS của Minh vẫn chạy mượt (CPU: 25%)!";
      } else {
        statusText.innerHTML = "<strong>[CẤU TRÚC VPS]:</strong> Mỗi VPS là 1 căn hộ khép kín có đồng hồ CPU/RAM riêng và chìa khóa Root trên <strong>1 tòa nhà máy chủ vật lý đơn lẻ</strong>.";
      }
      stage.innerHTML = `
        <div style="width:100%;max-width:480px;">
          <div class="infra2d-box ${crashed ? 'infra2d-glow-danger infra2d-shake' : ''}" style="padding:14px;border-color:${crashed ? 'var(--sim-danger)' : 'var(--sim-clay)'};">
            <div style="display:flex;justify-content:space-between;font-size:11.5px;font-weight:700;margin-bottom:10px;">
              <span style="color:var(--sim-clay);">TÒA NHÀ MÁY CHỦ VẬT LÝ ĐƠN LẺ (Single Physical Server)</span>
              <span style="color:${crashed ? 'var(--sim-danger)' : 'var(--sim-ok)'};">${crashed ? '[SPOF: HỎNG PHẦN CỨNG]' : '[ONLINE]'}</span>
            </div>
            <div class="infra2d-card-grid2">
              <div class="infra2d-box" style="border-color:${crashed ? 'var(--sim-danger)' : 'var(--sim-ok)'};background:${crashed ? 'var(--sim-danger-soft)' : 'var(--sim-ok-soft)'};">
                <div style="font-size:12px;font-weight:800;color:var(--sim-ink);">Căn hộ VPS Của Minh [ROOT]</div>
                <div style="font-size:11px;color:var(--sim-sub);margin-top:2px;">Cam kết riêng: 4 CPU • 8GB RAM</div>
                <div style="margin-top:8px;padding:4px 6px;border-radius:6px;background:var(--sim-canvas);font-size:11px;font-weight:700;color:${crashed ? 'var(--sim-danger)' : 'var(--sim-ok)'};">
                  ${crashed ? '[OFFLINE] SẬP WEB (Mất móng nhà!)' : '[ONLINE] Chạy mượt (CPU: 25%)'}
                </div>
              </div>
              <div class="infra2d-box" style="border-color:${crashed ? 'var(--sim-danger)' : neighborHot ? 'var(--sim-warn)' : 'var(--sim-border-muted)'};background:${crashed ? 'var(--sim-danger-soft)' : neighborHot ? 'var(--sim-warn-soft)' : 'var(--sim-border)'};">
                <div style="font-size:12px;font-weight:800;color:var(--sim-ink);">Căn hộ VPS Hàng Xóm</div>
                <div style="font-size:11px;color:var(--sim-sub);margin-top:2px;">Cam kết riêng: 4 CPU • 8GB RAM</div>
                <div style="margin-top:8px;padding:4px 6px;border-radius:6px;background:var(--sim-canvas);font-size:11px;font-weight:700;color:${crashed ? 'var(--sim-danger)' : neighborHot ? 'var(--sim-warn)' : 'var(--sim-sub)'};">
                  ${crashed ? '[OFFLINE] SẬP WEB' : neighborHot ? '[100% CPU] Quá tải riêng họ!' : '[ONLINE] Bình thường (CPU: 30%)'}
                </div>
              </div>
            </div>
            <div style="margin-top:10px;padding:8px;border-radius:8px;border:1px solid ${crashed ? 'var(--sim-danger)' : 'var(--sim-border)'};background:${crashed ? 'var(--sim-danger)' : 'var(--sim-canvas)'};color:${crashed ? '#faf9f5' : 'var(--sim-sub)'};font-size:11.5px;font-weight:700;text-align:center;">
              ${crashed ? 'MÓNG TÒA NHÀ: CHÁY Ổ CỨNG VẬT LÝ / HỎNG NGUỒN!' : 'Móng tòa nhà: 1 Ổ cứng & Bo mạch vật lý duy nhất'}
            </div>
          </div>
        </div>
      `;
      controls.innerHTML = `
        <button type="button" class="infra2d-btn infra2d-btn-primary" onclick="infra2dState.vpsHardwareCrash = false; infra2dState.vpsNeighborOverload = true; renderInfra2DSimStage();">
          1. Thử cho Hàng xóm quá tải 100%
        </button>
        <button type="button" class="infra2d-btn infra2d-btn-danger" onclick="infra2dState.vpsHardwareCrash = true; renderInfra2DSimStage();">
          2. Thử làm cháy ổ cứng tòa nhà mẹ!
        </button>
        <button type="button" class="infra2d-btn" onclick="infra2dState.vpsHardwareCrash = false; infra2dState.vpsNeighborOverload = false; renderInfra2DSimStage();">
          Reset
        </button>
      `;
    } else if (infra2dCurrentSlide === 3) {
      const nodeAFailed = infra2dState.cloudNodeACrash;
      const scaled = infra2dState.cloudScaled;
      if (nodeAFailed) {
        statusText.innerHTML = "<strong>[PHÉP MÀU CLOUD VM - FAILOVER / LIVE MIGRATION]:</strong> Tòa nhà số 1 vừa mất điện, Đám mây lập tức dịch chuyển căn hộ của Minh sang Tòa nhà số 2! Dữ liệu dưới hầm Ceph/SAN 3 bản sao vẫn nguyên vẹn, web KHÔNG SẬP!";
      } else if (scaled) {
        statusText.innerHTML = "<strong>[CO GIÃN TỨC THÌ - AUTO-SCALING]:</strong> Đón bão khách Trung Thu, Cloud VM tự động nâng gấp đôi sức mạnh (16 CPU) và nhân bản thêm căn hộ phụ chỉ trong vài giây!";
      } else {
        statusText.innerHTML = "<strong>[KIẾN TRÚC ĐÁM MÂY]:</strong> Hàng trăm tòa nhà kết nối với nhau + Hầm dữ liệu phân tán độc lập (Cloud SAN / Ceph Storage sao lưu 3 bản).";
      }
      stage.innerHTML = `
        <div style="width:100%;max-width:520px;">
          <div class="infra2d-card-grid3">
            <div class="infra2d-box ${!nodeAFailed ? 'infra2d-glow-success' : ''}" style="border-color:${nodeAFailed ? 'var(--sim-danger)' : 'var(--sim-ok)'};opacity:${nodeAFailed ? '0.75' : '1'};">
              <div style="font-size:11px;font-weight:700;color:var(--sim-muted);">Tòa Nhà Cloud #1</div>
              <div style="font-size:12px;font-weight:800;margin:6px 0;color:${nodeAFailed ? 'var(--sim-danger)' : 'var(--sim-ok)'};">
                ${nodeAFailed ? '[MẤT ĐIỆN]' : 'Cloud VM Của Minh'}
              </div>
              <div style="font-size:10.5px;color:var(--sim-sub);">
                ${nodeAFailed ? 'Đã sơ tán sang #2 →' : scaled ? '16 CPU (Đã nâng!)' : '4 CPU • 8GB RAM'}
              </div>
            </div>
            <div class="infra2d-box ${nodeAFailed ? 'infra2d-glow-success' : ''}" style="border-color:${nodeAFailed ? 'var(--sim-ok)' : scaled ? 'var(--sim-flow)' : 'var(--sim-border)'};">
              <div style="font-size:11px;font-weight:700;color:var(--sim-muted);">Tòa Nhà Cloud #2</div>
              <div style="font-size:12px;font-weight:800;margin:6px 0;color:${nodeAFailed ? 'var(--sim-ok)' : scaled ? 'var(--sim-flow)' : 'var(--sim-muted)'};">
                ${nodeAFailed ? 'Minh đã bay sang đây!' : scaled ? 'Bản sao Auto-Scale' : 'Dự phòng sẵn sàng'}
              </div>
              <div style="font-size:10.5px;color:var(--sim-ok);">
                ${nodeAFailed ? '[HA] Web chạy 100%!' : scaled ? '[ACTIVE] Đón phụ 5.000 khách' : 'Chờ tiếp ứng'}
              </div>
            </div>
            <div class="infra2d-box" style="border-color:${scaled ? 'var(--sim-flow)' : 'var(--sim-border)'};">
              <div style="font-size:11px;font-weight:700;color:var(--sim-muted);">Tòa Nhà Cloud #3</div>
              <div style="font-size:12px;font-weight:800;margin:6px 0;color:${scaled ? 'var(--sim-flow)' : 'var(--sim-muted)'};">
                ${scaled ? 'Bản sao Auto-Scale' : 'Dự phòng sẵn sàng'}
              </div>
              <div style="font-size:10.5px;color:var(--sim-ok);">
                ${scaled ? '[ACTIVE] Đón phụ 5.000 khách' : 'Chờ tiếp ứng'}
              </div>
            </div>
          </div>
          <div class="infra2d-pipe"></div>
          <div class="infra2d-box" style="border-color:var(--sim-clay);background:var(--sim-clay-soft);display:flex;align-items:center;justify-content:space-between;gap:10px;text-align:left;">
            <div>
              <div style="font-size:12px;font-weight:800;color:var(--sim-clay);">Hầm Dữ Liệu Phân Tán Độc Lập (Cloud SAN / Ceph Storage)</div>
              <div style="font-size:11px;color:var(--sim-sub);">Dữ liệu bánh &amp; đơn hàng được nhân làm 3 bản an toàn tuyệt đối (Tòa #1 cháy cũng không mất file!)</div>
            </div>
            <span style="padding:4px 8px;border-radius:6px;background:var(--sim-ok-soft);color:var(--sim-ok);font-size:11px;font-weight:800;white-space:nowrap;">3 Bản Sao</span>
          </div>
        </div>
      `;
      controls.innerHTML = `
        <button type="button" class="infra2d-btn infra2d-btn-danger" onclick="infra2dState.cloudNodeACrash = true; infra2dState.cloudScaled = false; renderInfra2DSimStage();">
          1. Đánh sập Tòa nhà #1 (Xem tự chuyển nhà!)
        </button>
        <button type="button" class="infra2d-btn infra2d-btn-emerald" onclick="infra2dState.cloudScaled = true; infra2dState.cloudNodeACrash = false; renderInfra2DSimStage();">
          2. Bão khách Trung Thu (Auto-Scale x3)
        </button>
        <button type="button" class="infra2d-btn" onclick="infra2dState.cloudNodeACrash = false; infra2dState.cloudScaled = false; renderInfra2DSimStage();">
          Reset
        </button>
      `;
    } else if (infra2dCurrentSlide === 4) {
      const turbo = infra2dState.dedicatedTurbo;
      const upgrading = infra2dState.dedicatedUpgrading;
      if (upgrading) {
        statusText.innerHTML = "<strong>[NHƯỢC ĐIỂM VẬT LÝ]:</strong> Vì là máy thật nguyên chiếc nên khi muốn gắn thêm ổ cứng hay thanh RAM mới, kỹ thuật viên phải tắt máy và cầm tua-vít lắp bằng tay!";
      } else if (turbo) {
        statusText.innerHTML = "<strong>[100% SỨC MẠNH BARE METAL]:</strong> Không có lớp ảo hóa trung gian Hypervisor, Minh vắt kiệt toàn bộ 100% xung nhịp CPU vật lý để chạy dữ liệu lớn!";
      } else {
        statusText.innerHTML = "<strong>[BARE METAL / DEDICATED]:</strong> Nguyên một căn biệt thự máy chủ vật lý thuộc độc quyền của công ty Minh, không có bất kỳ hàng xóm nào.";
      }
      stage.innerHTML = `
        <div class="infra2d-box" style="max-width:440px;width:100%;border-color:var(--sim-warn);padding:16px;">
          <span class="infra2d-pill-analogy" style="display:inline-block;margin-bottom:8px;">BIỆT THỰ ĐỘC QUYỀN (BARE METAL SERVER)</span>
          <div style="font-size:16px;font-weight:800;color:var(--sim-ink);">Dedicated Server Của Tập Đoàn Minh</div>
          <p style="font-size:11.5px;color:var(--sim-sub);margin:4px 0 12px !important;">Không chia sẻ • Không lớp cắt Hypervisor • Bảo mật vật lý</p>
          <div style="background:var(--sim-canvas);border:1px solid var(--sim-border);border-radius:8px;padding:10px;text-align:left;font-size:12px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
              <span style="color:var(--sim-muted);">Hao hụt ảo hóa (Hypervisor Tax):</span>
              <span style="font-weight:700;color:var(--sim-ok);">0% (Chạy thẳng trên phần cứng)</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
              <span style="color:var(--sim-muted);">Hàng xóm dùng chung:</span>
              <span style="font-weight:700;color:var(--sim-ok);">0 người (Độc quyền 100%)</span>
            </div>
            <div style="display:flex;justify-content:space-between;">
              <span style="color:var(--sim-muted);">Trạng thái hiện tại:</span>
              <span style="font-weight:700;color:${upgrading ? 'var(--sim-warn)' : 'var(--sim-flow)'};">
                ${upgrading ? '[DOWNTIME] Tắt máy chờ lắp thêm thanh RAM thật...' : turbo ? '[MAX PERF] Full 100% Công Suất Vật Lý!' : '[READY] Sẵn sàng'}
              </span>
            </div>
          </div>
        </div>
      `;
      controls.innerHTML = `
        <button type="button" class="infra2d-btn infra2d-btn-amber" onclick="infra2dState.dedicatedTurbo = true; infra2dState.dedicatedUpgrading = false; renderInfra2DSimStage();">
          1. Chạy 100% Hiệu năng Bare Metal
        </button>
        <button type="button" class="infra2d-btn" onclick="infra2dState.dedicatedUpgrading = true; infra2dState.dedicatedTurbo = false; renderInfra2DSimStage();">
          2. Thử nâng cấp thêm RAM vật lý
        </button>
      `;
    } else if (infra2dCurrentSlide === 5) {
      const started = infra2dState.raceStarted;
      statusText.innerHTML = started
        ? "<strong>[KẾT QUẢ CUỘC ĐUA]:</strong> Container (Docker) khởi động xong trong <strong>1 giây</strong> và chỉ tốn <strong>0.6 GB RAM</strong> cho 6 tiệm bánh vì bỏ qua cục tạ \"Hệ điều hành riêng (Guest OS)\"!"
        : "<strong>[SO SÁNH TRỰC QUAN]:</strong> Hãy bấm nút <strong>\"Bấm Đua Khởi Động (VM vs. Container)\"</strong> để thấy vì sao Container nhẹ và nhanh gấp chục lần Máy ảo (VM)!";
      stage.innerHTML = `
        <div class="infra2d-card-grid2" style="max-width:520px;">
          <div class="infra2d-box" style="text-align:left;display:flex;flex-direction:column;justify-content:space-between;">
            <div>
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <span style="font-size:12px;font-weight:800;color:var(--sim-warn);">Cách Cũ: 3 Máy Ảo (VM)</span>
                <span style="font-size:10.5px;padding:2px 6px;border-radius:4px;background:var(--sim-danger-soft);color:var(--sim-danger);">${started ? '60 giây' : 'Nặng nề'}</span>
              </div>
              ${[1, 2, 3].map(i => `
                <div style="padding:6px 8px;border-radius:6px;background:var(--sim-canvas);border:1px solid var(--sim-border);margin-bottom:6px;font-size:11px;">
                  <div style="font-weight:700;color:var(--sim-ink);">App Bánh #${i}</div>
                  <div style="margin-top:3px;padding:2px 6px;border-radius:4px;background:var(--sim-danger-soft);color:var(--sim-danger);font-weight:600;">
                    Cõng HĐH Guest OS riêng (4GB RAM)
                  </div>
                </div>
              `).join("")}
            </div>
            <div style="padding-top:6px;border-top:1px solid var(--sim-border);font-size:11px;color:var(--sim-muted);text-align:center;">
              Ngốn mất <strong>12 GB RAM</strong> chỉ để nuôi 3 Hệ điều hành!
            </div>
          </div>
          <div class="infra2d-box ${started ? 'infra2d-glow-success' : ''}" style="border-color:var(--sim-flow);display:flex;flex-direction:column;justify-content:space-between;">
            <div>
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <span style="font-size:12px;font-weight:800;color:var(--sim-flow);">Hiện Đại: 6 Container</span>
                <span style="font-size:10.5px;padding:2px 6px;border-radius:4px;background:var(--sim-ok-soft);color:var(--sim-ok);font-weight:700;">${started ? '1 GIÂY XONG!' : 'Siêu nhẹ'}</span>
              </div>
              <div class="infra2d-card-grid2" style="gap:6px;">
                ${[1, 2, 3, 4, 5, 6].map(i => `
                  <div style="padding:6px;border-radius:6px;background:var(--sim-flow-soft);border:1px solid color-mix(in oklab, var(--sim-flow) 38%, transparent);">
                    <div style="font-size:11px;font-weight:700;color:var(--sim-ink);">Container #${i}</div>
                    <div style="font-size:10px;color:var(--sim-ok);">${started ? '[RUNNING] 1s!' : 'Chỉ 100MB'}</div>
                  </div>
                `).join("")}
              </div>
              <div style="margin-top:8px;padding:5px;border-radius:6px;background:var(--sim-flow-soft);border:1px solid color-mix(in oklab, var(--sim-flow) 38%, transparent);font-size:11px;font-weight:700;color:var(--sim-flow);">
                Docker Engine + Dùng chung 1 Nhân HĐH Máy Chủ
              </div>
            </div>
            <div style="padding-top:6px;border-top:1px solid var(--sim-border);font-size:11px;color:var(--sim-ok);font-weight:600;">
              Chạy gấp đôi số tiệm bánh mà chỉ tốn <strong>0.6 GB RAM</strong>!
            </div>
          </div>
        </div>
      `;
      controls.innerHTML = `
        <button type="button" class="infra2d-btn infra2d-btn-cyan" onclick="infra2dState.raceStarted = true; renderInfra2DSimStage();">
          1. Bấm Đua Khởi Động (VM vs. Container)
        </button>
        <button type="button" class="infra2d-btn" onclick="infra2dState.raceStarted = false; renderInfra2DSimStage();">
          Reset
        </button>
      `;
    } else if (infra2dCurrentSlide === 6) {
      const mode = infra2dState.serverlessMode;
      if (mode === "idle") {
        statusText.innerHTML = "<strong>[SCALE-TO-ZERO]:</strong> Trạng thái 0 Khách — Bếp Serverless tắt hoàn toàn. Minh tốn <strong>0 VNĐ</strong> (Trong khi thuê VPS vẫn bị trừ tiền đều đặn!).";
      } else if (mode === "one") {
        statusText.innerHTML = "<strong>[1 REQUEST]:</strong> Có 1 Khách đặt bánh — Hệ thống tự bật 1 đầu bếp Robot trong 0.2 giây (200ms), nướng xong giao bánh rồi tắt. Chỉ tốn <strong>2 đồng</strong>!";
      } else {
        statusText.innerHTML = "<strong>[FLASH SALE 1.000 KHÁCH]:</strong> Serverless lập tức triệu hồi 1.000 đầu bếp Robot chạy song song mà Minh không cần đụng tay vào bất kỳ máy chủ nào!";
      }
      stage.innerHTML = `
        <div class="infra2d-box ${mode === 'flash' ? 'infra2d-glow-success' : ''}" style="max-width:480px;width:100%;border-color:${mode === 'flash' ? 'var(--sim-warn)' : mode === 'one' ? 'var(--sim-ok)' : 'var(--sim-border)'};padding:14px;">
          <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--sim-border);padding-bottom:8px;margin-bottom:10px;font-size:11.5px;font-weight:700;">
            <span style="color:var(--sim-danger);">KHU BẾP SERVERLESS (AWS Lambda / Cloud Run / Vercel)</span>
            <span style="padding:3px 8px;border-radius:999px;background:var(--sim-ok-soft);color:var(--sim-ok);">
              Chi phí: ${mode === 'idle' ? '0 VNĐ / giờ' : mode === 'one' ? '2 VNĐ / đơn' : 'Tính đúng 1.000 đơn'}
            </span>
          </div>
          <div style="min-height:130px;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:8px;padding:12px;border-radius:8px;background:var(--sim-canvas);border:1px solid var(--sim-border);">
            ${mode === "idle" ? `
              <div style="color:var(--sim-muted);font-size:12px;">
                <div style="font-weight:800;color:var(--sim-sub);margin-bottom:4px;">[SCALE-TO-ZERO] Chỉ có bản Công thức bánh (Code) đang nằm chờ</div>
                <div>Không tốn 1 xu tiền thuê mặt bằng khi vắng khách!</div>
              </div>
            ` : mode === "one" ? `
              <div class="infra2d-box" style="border-color:var(--sim-ok);background:var(--sim-ok-soft);">
                <div style="font-size:12.5px;font-weight:800;color:var(--sim-ok);">Đầu Bếp Serverless #1</div>
                <div style="font-size:11px;color:var(--sim-sub);margin-top:4px;">Nướng xong trong 200ms → Tự biến mất!</div>
              </div>
            ` : `
              ${[1, 2, 3, 4, 5, 6, 7, 8].map(n => `
                <div style="padding:6px 10px;border-radius:8px;background:var(--sim-warn-soft);border:1px solid color-mix(in oklab, var(--sim-warn) 42%, transparent);font-size:11px;font-weight:700;color:var(--sim-warn);">
                  Bếp #${n} [ACTIVE]
                </div>
              `).join("")}
              <div style="width:100%;font-size:11.5px;font-weight:700;color:var(--sim-ok);margin-top:6px;">
                + Tự động nhân bản 1.000 hàm xử lý song song rồi tự giải tán về 0đ!
              </div>
            `}
          </div>
        </div>
      `;
      controls.innerHTML = `
        <button type="button" class="infra2d-btn ${mode === 'idle' ? 'infra2d-btn-primary' : ''}" onclick="infra2dState.serverlessMode = 'idle'; renderInfra2DSimStage();">
          1. Ban đêm 0 khách (0 VNĐ)
        </button>
        <button type="button" class="infra2d-btn infra2d-btn-emerald" onclick="infra2dState.serverlessMode = 'one'; renderInfra2DSimStage();">
          2. Có 1 khách bấm mua bánh
        </button>
        <button type="button" class="infra2d-btn infra2d-btn-amber" onclick="infra2dState.serverlessMode = 'flash'; renderInfra2DSimStage();">
          3. Bão Sale 1.000 khách cùng lúc!
        </button>
      `;
    } else {
      const scenarios = [
        {
          btn: "1. Làm Blog / Web giới thiệu nhỏ",
          pick: "Shared Hosting (hoặc PaaS tĩnh miễn phí)",
          badge: "[HOSTING / STATIC PAAS]",
          color: "var(--sim-flow)",
          why: "Ngân sách chỉ vài chục nghìn/tháng, không cần biết quản trị Linux, có sẵn cPanel để cài WordPress trong 5 phút.",
          avoid: "Chưa cần thuê Dedicated hay Cloud VM phức tạp gây lãng phí."
        },
        {
          btn: "2. Lập trình viên cần máy riêng giá rẻ",
          pick: "VPS + Cài Docker Container bên trong",
          badge: "[VPS + DOCKER ENGINE]",
          color: "var(--sim-clay)",
          why: "Chi phí cố định hàng tháng rất rẻ (100k - 300k), có toàn quyền Root để vọc Linux và chạy nhiều dự án nhỏ bằng Docker.",
          avoid: "Nhớ tự sao lưu dữ liệu (Backup) định kỳ đề phòng ổ cứng máy mẹ hỏng (SPOF)."
        },
        {
          btn: "3. Sàn TMĐT / Hệ thống công ty cấm sập",
          pick: "Cloud VM + Kubernetes (AWS / GCP / Viettel / VNG Cloud)",
          badge: "[CLOUD VM + K8S HA]",
          color: "var(--sim-ok)",
          why: "Tự động chuyển đổi dự phòng (Failover) khi lỗi phần cứng, dễ dàng nâng/hạ cấu hình theo mùa cao điểm mà không gián đoạn.",
          avoid: "Nhớ cài cảnh báo ngân sách (Billing Alert) để kiểm soát chi phí."
        },
        {
          btn: "4. Startup muốn ra mắt App thần tốc, ít người",
          pick: "PaaS / Serverless (Vercel, Cloud Run, Render)",
          badge: "[SERVERLESS SCALE-TO-ZERO]",
          color: "var(--sim-warn)",
          why: "Đội ngũ chỉ việc viết Code và đẩy lên Git. Không tốn tiền thuê kỹ sư trực máy chủ, vắng khách chi phí gần như bằng 0.",
          avoid: "Rất tuyệt vời cho giai đoạn tăng trưởng nhanh."
        }
      ];
      const cur = scenarios[infra2dState.selectedCase || 0];
      statusText.innerHTML = "<strong>[MÁY TƯ VẤN HẠ TẦNG]:</strong> Hãy bấm chọn 1 trong 4 bài toán thực tế bên dưới để xem lời khuyên thiết kế hạ tầng!";
      stage.innerHTML = `
        <div class="infra2d-box" style="max-width:480px;width:100%;border-color:${cur.color};padding:16px;">
          <div style="font-size:11.5px;font-weight:800;color:${cur.color};margin-bottom:4px;">${cur.badge} — GIẢI PHÁP KHUYÊN DÙNG</div>
          <div style="font-size:17px;font-weight:800;color:var(--sim-ink);margin-bottom:10px;">${cur.pick}</div>
          <div style="background:var(--sim-canvas);border:1px solid var(--sim-border);border-radius:8px;padding:12px;text-align:left;font-size:12px;">
            <p style="color:var(--sim-ok);margin:0 0 6px !important;"><strong>[TẠI SAO PHÙ HỢP]:</strong> ${cur.why}</p>
            <p style="color:var(--sim-warn);margin:0 !important;"><strong>[LƯU Ý THỰC CHIẾN]:</strong> ${cur.avoid}</p>
          </div>
        </div>
      `;
      controls.innerHTML = scenarios.map((sc, idx) => `
        <button type="button" class="infra2d-btn ${(infra2dState.selectedCase || 0) === idx ? 'infra2d-btn-primary' : ''}" onclick="infra2dState.selectedCase = ${idx}; renderInfra2DSimStage();">
          ${sc.btn}
        </button>
      `).join("");
    }
  }

  function buildInfra2DSimulatorHtml() {
    return `
      <div class="infra2d-wrap" id="infra2dWidgetRoot">
        <div class="infra2d-header">
          <div class="infra2d-brand">
            <div class="infra2d-brand-icon">2D</div>
            <div>
              <div class="infra2d-brand-badges">
                <span class="infra2d-tag">Storytelling 2D</span>
                <span class="infra2d-chapter" id="infra2dChapterBadge">Gốc rễ khái niệm</span>
              </div>
              <h4 class="infra2d-title-bar">Chuyện Tiệm Bánh Của Minh: Từ Máy Ảo Đến Đám Mây</h4>
            </div>
          </div>
          <div class="infra2d-dots" id="infra2dDots"></div>
          <button type="button" class="infra2d-btn" onclick="toggleInfra2DSummaryModal()">Bảng So Sánh Nhanh</button>
        </div>

        <div id="infra2dSummaryDrawer" style="display:none;padding:14px 16px;background:var(--sim-canvas);border-bottom:1px solid var(--sim-border);">
          <div style="padding:10px 12px;border-radius:8px;background:var(--sim-clay-soft);border:1px solid var(--sim-clay-border);font-size:12.5px;color:var(--sim-clay);margin-bottom:10px;">
            <strong>Quy tắc vàng:</strong> <strong>VM (Virtual Machine)</strong> là <em>công nghệ chia cắt máy tính bằng Hypervisor</em>. Còn <strong>VPS</strong> và <strong>Cloud VM</strong> là <em>gói sản phẩm thương mại</em> ứng dụng công nghệ VM đó để cho bạn thuê!
          </div>
          <div class="table-wrap" style="margin:0;">
            <table class="clean-table">
              <thead>
                <tr>
                  <th>Loại hình</th>
                  <th>Ẩn dụ Bất động sản</th>
                  <th>Điểm mạnh nhất</th>
                  <th>Rủi ro / Hạn chế</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Shared Hosting</strong></td>
                  <td>Giường ký túc xá ở ghép</td>
                  <td>Rẻ nhất (50k/tháng), có sẵn cPanel, không cần biết kỹ thuật Linux</td>
                  <td>Không có quyền Root; hàng xóm bị DDoS (Noisy Neighbor) là mình sập lỗi 503 theo</td>
                </tr>
                <tr>
                  <td><strong>VPS</strong></td>
                  <td>Căn hộ chung cư đơn lẻ</td>
                  <td>Toàn quyền Root, tài nguyên cam kết riêng (4 CPU, 8GB RAM), giá cố định</td>
                  <td>Nằm trên 1 máy vật lý mẹ duy nhất (SPOF): cháy ổ cứng máy mẹ là sập ngay</td>
                </tr>
                <tr>
                  <td><strong>Cloud VM</strong></td>
                  <td>Căn hộ thông minh liên kết</td>
                  <td>Tự chuyển nhà (Failover / Live Migration) + hầm Ceph/SAN 3 bản sao, Auto-Scaling</td>
                  <td>Chi phí tính theo mức dùng (Pay-as-you-go), cần cài Billing Alert tối ưu</td>
                </tr>
                <tr>
                  <td><strong>Dedicated Server</strong></td>
                  <td>Thuê nguyên căn biệt thự</td>
                  <td>100% sức mạnh phần cứng trần (0% Hypervisor Tax), bảo mật vật lý tuyệt đối</td>
                  <td>Đắt đỏ, nâng cấp phải tắt máy chờ kỹ thuật viên lắp thanh RAM bằng tay</td>
                </tr>
                <tr>
                  <td><strong>Container (Docker)</strong></td>
                  <td>Nhà hộp lắp ghép tiêu chuẩn</td>
                  <td>Khởi động 1 giây, cực nhẹ (6 containers = 0.6GB RAM) vì dùng chung Host OS Kernel</td>
                  <td>Cần học quy trình đóng gói Docker / điều phối Kubernetes</td>
                </tr>
                <tr>
                  <td><strong>Serverless / PaaS</strong></td>
                  <td>Thuê bếp nướng bánh theo lượt</td>
                  <td>Chỉ cần đưa Code, tự nhân bản 1.000 bếp (200ms/đơn), ban đêm 0 khách = 0 VNĐ</td>
                  <td>Phụ thuộc nền tảng của nhà cung cấp (Cloud Run / AWS Lambda / Vercel)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="infra2d-grid">
          <div class="infra2d-col-left">
            <div>
              <div class="infra2d-pills">
                <span class="infra2d-pill-num" id="infra2dSlideNumPill">SLIDE 1 / 8</span>
                <span class="infra2d-pill-analogy" id="infra2dAnalogyPill">Ẩn dụ Bất động sản</span>
              </div>
              <h3 class="infra2d-slide-h3" id="infra2dSlideTitle"></h3>
              <div class="infra2d-story-box">
                <div class="infra2d-avatar" title="Minh - Chủ tiệm bánh">MINH</div>
                <div>
                  <span class="infra2d-story-title" id="infra2dMinhTitle"></span>
                  <p class="infra2d-story-text" id="infra2dMinhStory"></p>
                </div>
              </div>
              <div class="infra2d-keypoints" id="infra2dKeypoints"></div>
            </div>
            <div class="infra2d-verdict" id="infra2dVerdictBox"></div>
          </div>

          <div class="infra2d-col-right">
            <div>
              <div class="infra2d-sim-top">
                <div class="infra2d-sim-live">
                  <span class="infra2d-sim-dot"></span>
                  <span>Mô Phỏng Tương Tác 2D</span>
                </div>
                <span class="infra2d-sim-hint">Hãy bấm các nút bên dưới để thử nghiệm!</span>
              </div>
              <div class="infra2d-stage" id="infra2dSimStage"></div>
            </div>
            <div>
              <div class="infra2d-status" id="infra2dSimStatusText">Sẵn sàng tương tác.</div>
              <div class="infra2d-controls" id="infra2dSimControls"></div>
            </div>
          </div>
        </div>

        <div class="infra2d-footer">
          <button type="button" class="infra2d-btn" id="infra2dBtnPrev" onclick="changeInfra2DSlide(-1)">← Slide Trước</button>
          <div class="infra2d-progress-wrap">
            <div class="infra2d-progress-track">
              <div class="infra2d-progress-fill" id="infra2dProgressFill" style="width:12.5%;"></div>
            </div>
            <span style="font-size:11px;color:var(--sim-muted);">Bấm chọn từng Slide (1–8) hoặc nút điều khiển bên phải để tương tác trực tiếp</span>
          </div>
          <button type="button" class="infra2d-btn infra2d-btn-primary" id="infra2dBtnNext" onclick="changeInfra2DSlide(1)">Slide Tiếp Theo →</button>
        </div>
      </div>
    `;
  }


  /* ==========================================================================
     CLAUDE / ANTHROPIC-STYLE 2D ANIMATED PACKET FLOW & ARCHITECTURAL LAB (D01)
     ========================================================================== */
  const ING2D_SLIDES = [
    {
      id: 1,
      chapter: "Chặng 2 · 3 Thế Hệ CDC",
      analogy: "Cắt Lớp 4 Tầng Nội Tạng PostgreSQL",
      title: "1. Phẫu Thuật 3 Thế Hệ CDC: Polling vs. Trigger vs. Log-Based WAL",
      leadTitle: "Đặt đầu dò ở tầng nào của Database để bắt Order #8888 mà không làm sập CPU?",
      leadStory: "Giao dịch #8888 (450.000đ) vừa đi qua 4 tầng nội tạng của PostgreSQL: (L1) SQL Parser/Executor → (L2) Trigger Engine → (L3) 8KB Heap Pages → (L4) Nhật ký nhị phân pg_wal. Hãy chuyển đổi giữa 3 thế hệ CDC và bấm nút [Thử lệnh Hard DELETE #8888] để quan sát đường đi của gói tin và tải phần cứng!",
      keypoints: [
        { b: "1", t: "Timestamp Polling (Đầu dò tại L1 — SQL Executor)", d: "Cứ 5 phút bắn SELECT WHERE last_modified > Watermark. Quét bảng gây vọt 78% CPU, trễ hàng phút và MÙ HOÀN TOÀN trước lệnh xóa vật lý Hard DELETE." },
        { b: "2", t: "Trigger-Based CDC (Đầu dò tại L2 — Trigger Engine)", d: "Chặn ngay trong giao dịch của khách để ghi thêm 1 bản vào shadow_table. Bắt được DELETE nhưng nhân đôi I/O và kéo độ trễ Checkout từ 12ms lên 26ms!" },
        { b: "3", t: "Log-Based CDC / Debezium (Đầu dò tại L4 — pg_wal)", d: "Đọc tuần tự luồng byte nhị phân tại LSN=0/16B3748 thông qua khe pgoutput. 0% tải truy vấn bảng chính, độ trễ < 15ms và bắt trọn cả Hard DELETE." }
      ],
      verdict: "Chốt thiết kế: Luôn ưu tiên Log-Based CDC (Debezium đọc WAL/binlog) cho các bảng giao dịch cốt lõi để tách rời 100% tải phân tích khỏi luồng OLTP.",
      simMode: "cdc"
    },
    {
      id: 2,
      chapter: "Chặng 4 · Producer Internals",
      analogy: "Cắt Lớp 4 Tầng Kafka Producer & Partitioner",
      title: "2. Đường Ống Producer: Băm Khóa murmur2(Key) vs. Chia Tải Keyless",
      leadTitle: "Làm sao giữ đúng thứ tự nhân quả: Đặt hàng (#1) → Thanh toán (#2) → Giao hàng (#3)?",
      leadStory: "Một đơn hàng #8888 của khách USR-104 phát sinh liên tiếp 3 sự kiện trạng thái. Bên trong Kafka Producer, bản ghi đi qua: [1. Avro Serializer] → [2. Partitioner] → [3. RecordAccumulator Batch 64KB] → [4. Sender Thread]. Hãy thử so sánh chế độ Có Khóa (With Key) và Không Khóa (Without Key)!",
      keypoints: [
        { b: "A", t: "With Key (key = 'USR-104' → murmur2(key) % 3 = Partition 1)", d: "Hàm băm tất định ép toàn bộ sự kiện của USR-104 đi vào duy nhất Partition 1 theo đúng thứ tự: Offset 10 (CREATED) → Offset 11 (PAID) → Offset 12 (SHIPPED)." },
        { b: "B", t: "Without Key (key = null → Sticky / Round-Robin P0, P1, P2)", d: "Các bản ghi được rải đều sang Partition 0, 1, 2 để cân bằng tải tối đa, nhưng Consumer đọc P2 có thể xử lý trạng thái SHIPPED trước cả khi P0 xử lý CREATED!" },
        { b: "C", t: "RecordAccumulator & Nén Lô (batch.size = 64KB, linger.ms = 10ms)", d: "Thay vì gửi lẻ từng gói qua mạng, Producer gom nhiều bản ghi cùng Partition vào bộ đệm RAM và nén LZ4/ZSTD trước khi đẩy sang Broker." }
      ],
      verdict: "Quy tắc định tuyến: Bắt buộc truyền khóa định danh thực thể (order_id hoặc user_id) khi nghiệp vụ đòi hỏi bảo toàn thứ tự trạng thái.",
      simMode: "producer"
    },
    {
      id: 3,
      chapter: "Chặng 4 · Consumer Group",
      analogy: "Cắt Lớp Ánh Xạ Partition ↔ Consumer & Fan-out",
      title: "3. Cơ Học Consumer Group: Quy Tắc Độc Quyền Partition & Trạng Thái IDLE",
      leadTitle: "Tại saoTopic có 3 Partitions mà tăng lên 4 Consumers thì máy thứ 4 lại ngồi chơi?",
      leadStory: "Trong cùng một Consumer Group, Kafka khóa cứng quy tắc: 1 Partition chỉ được gán cho TỐI ĐA 1 Consumer tại một thời điểm để tránh đọc trùng và giữ thứ tự. Hãy bấm tăng số lượng Consumer từ 1 → 4 hoặc giả lập sập Consumer 2 để xem Group Coordinator vẽ lại sơ đồ dây nối!",
      keypoints: [
        { b: "1:3", t: "1 Consumer đọc 3 Partitions (Nghẽn cổ chai)", d: "Một tiến trình phải kéo dữ liệu từ cả P0, P1, P2. Thông lượng chỉ đạt 10 MB/s, độ trễ Consumer Lag tăng vọt khi có Flash Sale." },
        { b: "3:3", t: "3 Consumers đọc 3 Partitions (Ánh xạ vàng 1:1)", d: "Mỗi Consumer độc quyền 1 Partition (C1←P0, C2←P1, C3←P2). Thông lượng nhân 3 (30 MB/s), Consumer Lag giảm về 0." },
        { b: "4:3", t: "4 Consumers trên 3 Partitions (Dư thừa → Consumer 4 IDLE!)", d: "Không được phép để 2 Consumer cùng đọc 1 Partition trong cùng Group! Do đó Consumer 4 hoàn toàn nhàn rỗi (IDLE), chỉ đứng chờ làm dự phòng." }
      ],
      verdict: "Định luật song song hóa: Số lượng Partition của Topic chính là trần song song tối đa (Max Parallelism) của một Consumer Group.",
      simMode: "consumer"
    },
    {
      id: 4,
      chapter: "Chặng 4 · Replication & EOS",
      analogy: "Cắt Lớp Cụm 3 Brokers, Tập Hợp ISR & High Watermark",
      title: "4. Chịu Lỗi Replication (RF=3), Tập Hợp ISR & Cạm Bẫy Mất Dữ Liệu acks=1",
      leadTitle: "Tại sao Slide 39 cảnh báo cấu hình acks=1 VẪN LÀM MẤT DỮ LIỆU khi Leader sập?",
      leadStory: "Topic prod.orders có replication.factor = 3: Broker 1 giữ bản chính (Leader), còn Broker 2 và Broker 3 giữ bản sao (Followers trong tập ISR). Hãy bắn thử Order #8888 rồi cho sập nguồn Broker 1 ở hai chế độ acks=1 và acks=all để tận mắt thấy sự khác biệt sinh tử!",
      keypoints: [
        { b: "ISR", t: "Leader & In-Sync Replicas (ISR = {B1, B2, B3})", d: "Mọi thao tác Đọc/Ghi của Client đi qua Leader (B1). Các Followers (B2, B3) liên tục gửi FetchRequest kéo dữ liệu mới về để bám sát High Watermark." },
        { b: "!", t: "Thảm kịch acks=1: Leader trả ACK xong rồi sập trước khi Follower kịp chép!", d: "Với acks=1, Broker 1 vừa ghi xong đĩa cục bộ đã báo OK cho Producer. Nếu B1 cháy nguồn đúng mili-giây đó, B2 lên làm Leader mới nhưng KHÔNG HỀ CÓ #8888 → Mất đơn!" },
        { b: "+", t: "Tam giác vàng: acks=all + min.insync.replicas=2 + idempotence=true", d: "Leader chỉ trả ACK khi ít nhất 2 bản sao trong ISR đã ghi bền vững. Kể cả Broker 1 nổ tung, Broker 2 lên ngôi vẫn giữ nguyên vẹn 100% đơn #8888." }
      ],
      verdict: "Chuẩn Production cho dữ liệu tài chính/CDC: replication.factor=3, min.insync.replicas=2, unclean.leader.election.enable=false và acks=all.",
      simMode: "replication"
    },
    {
      id: 5,
      chapter: "Chặng 4 · On-Disk Log Model",
      analogy: "Cắt Lớp Thư Mục /orders-0/ (.log, .index) & Log Cleaner",
      title: "5. Vật Lý Đĩa Cứng: Xóa Segment O(1) vs. Nén Nhật Ký Theo Khóa (Log Compaction)",
      leadTitle: "Kafka lưu trữ hàng Terabyte trên đĩa và tự động gộp lịch sử cập nhật của #8888 như thế nào?",
      leadStory: "Trên ổ cứng NVMe, mỗi Partition thực chất là một thư mục (orders-0/) được chia thành các tệp phân đoạn (Log Segments: .log, .index, .timeindex). Hãy thử kích hoạt tiến trình Log Cleaner (cleanup.policy=compact) và bắn bản ghi bia mộ Tombstone trên luồng cập nhật của Order #8888!",
      keypoints: [
        { b: "SEG", t: "Phân đoạn Tệp (.log + .index) & Xóa theo Thời gian/Dung lượng (7 days / 1GB)", d: "Thay vì xóa từng dòng gây phân mảnh đĩa, Kafka đóng tệp Segment cũ và gọi syscall unlink() xóa trọn file hết hạn trong O(1) mili-giây." },
        { b: "CMP", t: "Log Compaction (Dirty Tail → Clean Head theo Khóa)", d: "Đơn #8888 trải qua 3 lần sửa: Off 10 (PENDING) → Off 12 (PAID) → Off 13 (SHIPPED). Log Cleaner quét nền và chỉ giữ lại bản ghi mới nhất (Off 13: SHIPPED)!" },
        { b: "DEL", t: "Bản ghi Bia mộ Tombstone (key='ORD-8888', value=null)", d: "Để xóa hẳn một khóa khỏi Topic nén, Producer bắn một bản ghi có value=null (Tombstone) báo hiệu cho các Consumer và Log Cleaner thu hồi khóa." }
      ],
      verdict: "Chọn chính sách lưu trữ: Dùng cleanup.policy=delete (7 ngày) cho luồng sự kiện phân tích, và cleanup.policy=compact cho bảng trạng thái CDC / __consumer_offsets.",
      simMode: "compaction"
    },
    {
      id: 6,
      chapter: "Chặng 5 · Production Challenges",
      analogy: "Cắt Lớp Đường Ống End-to-End & 4 Chốt Chặn Sinh Tử",
      title: "6. Giải Cứu Sự Cố Thực Chiến: Nổ Đĩa WAL Bloat, DLQ & Transactional Outbox",
      leadTitle: "Tại sao cắm Debezium vào PostgreSQL mà quên cấu hình Heartbeat lại làm sập cứng Database nguồn?",
      leadStory: "Trong thực tế vận hành, đường ống Debezium → Kafka Connect đối mặt 4 tai nạn kinh điển: (1) Kẹt Replication Slot làm nổ ổ cứng pg_wal, (2) Tin nhắn độc Poison Pill làm chết Sink Connector, (3) Hot Partition Skew và (4) Dual-Write mất đồng bộ. Hãy bấm từng phác đồ để kích hoạt cơ chế phòng vệ!",
      keypoints: [
        { b: "WAL", t: "Phòng chống Nổ đĩa pg_wal (Replication Slot Bloat)", d: "Nếu bảng theo dõi ít phát sinh giao dịch hoặc Connector chết, con trỏ confirmed_flush_lsn đứng im khiến Postgres giữ lại toàn bộ WAL. Phải bật heartbeat.interval.ms + max_slot_wal_keep_size!" },
        { b: "DLQ", t: "Confluent Schema Registry & Kênh Cách Ly Dead Letter Queue (DLQ)", d: "Kiểm tra tương thích lược đồ (BACKWARD/FULL) tại cửa ngõ và cấu hình errors.tolerance=all để tự động đẩy bản ghi lỗi sang topic DLQ thay vì làm sập cả đường ống." },
        { b: "BOX", t: "Mẫu Transactional Outbox Pattern xóa sổ lỗi Ghi Kép (Dual-Write)", d: "Microservice ghi đồng thời vào bảng orders và bảng outbox_events trong CÙNG 1 ACID Transaction cục bộ, sau đó Debezium đọc bảng Outbox đẩy lên Kafka." }
      ],
      verdict: "Kỷ luật SRE: Không bao giờ đưa Debezium lên Production nếu chưa cài đặt cảnh báo dung lượng pg_wal, max_slot_wal_keep_size và kênh cách ly Dead Letter Queue.",
      simMode: "challenges"
    }
  ];

  let ing2dCurrentSlide = 0;
  let ing2dState = {
    cdcMode: "wal",
    cdcHardDelete: false,
    prodMode: "keyed",
    prodSeqStep: 3,
    consCount: 3,
    consCrash2: false,
    repScenario: "normal",
    compMode: "dirty",
    chalMode: "bloat"
  };

  function buildIngestion2DSimulatorHtml() {
    return `
      <div class="infra2d-wrap" id="ing2dWidgetRoot">
        <div class="infra2d-header">
          <div class="infra2d-brand">
            <div class="infra2d-brand-icon">2D</div>
            <div>
              <div class="infra2d-brand-badges">
                <span class="infra2d-tag">Cắt Lớp Kiến Trúc &amp; Luồng Gói Tin 2D</span>
                <span class="infra2d-chapter" id="ing2dChapterBadge">Chặng 2 · 3 Thế Hệ CDC</span>
              </div>
              <h4 class="infra2d-title-bar">Phòng Thí Nghiệm Tương Tác D01: Hành Trình Sự Kiện Order #8888 Qua Tầng Ingestion</h4>
            </div>
          </div>
          <div class="infra2d-dots" id="ing2dDots"></div>
          <button type="button" class="infra2d-btn" onclick="toggleIngestion2DSummaryModal()">Bảng Tóm Tắt Thông Số</button>
        </div>

        <div id="ing2dSummaryDrawer" style="display:none;padding:14px 16px;background:var(--sim-canvas);border-bottom:1px solid var(--sim-border);">
          <div style="padding:10px 12px;border-radius:8px;background:var(--sim-flow-soft);border:1px solid color-mix(in oklab, var(--sim-flow) 35%, transparent);font-size:12.5px;color:var(--sim-flow);margin-bottom:10px;">
            <strong>Chuẩn kiến trúc D01 (Ingestion Layer):</strong> Kết hợp <strong>Debezium Log-Based CDC</strong> (đọc tuần tự <code>pg_wal</code>/<code>binlog</code>) với trục sự kiện phân tán <strong>Apache Kafka (KRaft, RF=3, min.insync.replicas=2, acks=all)</strong> để đạt độ trễ mili-giây và 0% mất mát dữ liệu.
          </div>
          <div class="table-wrap" style="margin:0;">
            <table class="clean-table">
              <thead>
                <tr>
                  <th>Tầng Cắt Lớp</th>
                  <th>Cơ Chế Cốt Lõi</th>
                  <th>Thông Số Chuẩn Production</th>
                  <th>Rủi Ro Sinh Tử Cần Chặn</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>1. Source CDC</strong></td>
                  <td>Đọc nhật ký nhị phân <code>pg_wal</code> (<code>pgoutput</code>) / <code>binlog</code> (<code>ROW</code>)</td>
                  <td><code>wal_level = logical</code>, <code>heartbeat.interval.ms = 10000</code></td>
                  <td>Kẹt Replication Slot làm nổ ổ cứng DB nguồn (<code>WAL Bloat</code>)</td>
                </tr>
                <tr>
                  <td><strong>2. Kafka Producer</strong></td>
                  <td>Băm khóa <code>murmur2(key) % P</code> + Gom lô <code>RecordAccumulator</code></td>
                  <td><code>acks = all</code>, <code>enable.idempotence = true</code>, <code>linger.ms = 10</code></td>
                  <td>Mất thứ tự khi <code>key = null</code> hoặc lệch tải <code>Hot Partition</code></td>
                </tr>
                <tr>
                  <td><strong>3. Kafka Broker &amp; ISR</strong></td>
                  <td>Sao chép Leader → Followers trong tập <code>ISR</code> + Zero-Copy <code>sendfile(2)</code></td>
                  <td><code>replication.factor = 3</code>, <code>min.insync.replicas = 2</code></td>
                  <td>Đặt <code>acks = 1</code> làm mất bản ghi khi Leader sập trước khi đồng bộ</td>
                </tr>
                <tr>
                  <td><strong>4. Consumer &amp; Sink</strong></td>
                  <td>Mỗi Partition tối đa 1 Consumer/Group + <code>CooperativeStickyAssignor</code></td>
                  <td><code>enable.auto.commit = false</code>, <code>errors.tolerance = all</code> (+ DLQ)</td>
                  <td>Dư Consumer ngồi chơi (<code>IDLE</code>) hoặc chết lặp do <code>Poison Pill</code></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="infra2d-grid">
          <div class="infra2d-col-left">
            <div>
              <div class="infra2d-pills">
                <span class="infra2d-pill-num" id="ing2dSlideNumPill">SLIDE 1 / 6</span>
                <span class="infra2d-pill-analogy" id="ing2dAnalogyPill">Cắt Lớp Kiến Trúc</span>
              </div>
              <h3 class="infra2d-slide-h3" id="ing2dSlideTitle"></h3>
              <div class="infra2d-story-box">
                <div class="infra2d-avatar" title="Sự kiện Giao dịch Order #8888">#8888</div>
                <div>
                  <span class="infra2d-story-title" id="ing2dLeadTitle"></span>
                  <p class="infra2d-story-text" id="ing2dLeadStory"></p>
                </div>
              </div>
              <div class="infra2d-keypoints" id="ing2dKeypoints"></div>
            </div>
            <div class="infra2d-verdict" id="ing2dVerdictBox"></div>
          </div>

          <div class="infra2d-col-right">
            <div>
              <div class="infra2d-sim-top">
                <div class="infra2d-sim-live">
                  <span class="infra2d-sim-dot"></span>
                  <span>Sơ Đồ Cắt Lớp &amp; Luồng Gói Tin Chuyển Động (Animated SVG)</span>
                </div>
                <span class="infra2d-sim-hint">Bấm các nút kịch bản bên dưới để đổi luồng!</span>
              </div>
              <div class="infra2d-stage" id="ing2dSimStage" style="padding:10px;"></div>
            </div>
            <div>
              <div class="infra2d-status" id="ing2dSimStatusText">Sẵn sàng mô phỏng.</div>
              <div class="infra2d-controls" id="ing2dSimControls"></div>
            </div>
          </div>
        </div>

        <div class="infra2d-footer">
          <button type="button" class="infra2d-btn" id="ing2dBtnPrev" onclick="changeIngestion2DSlide(-1)">← Mô Phỏng Trước</button>
          <div class="infra2d-progress-wrap">
            <div class="infra2d-progress-track">
              <div class="infra2d-progress-fill" id="ing2dProgressFill" style="width:16.6%;"></div>
            </div>
            <span style="font-size:11px;color:var(--sim-muted);">Chọn 1 trong 6 lát cắt kiến trúc (1–6) hoặc kích hoạt kịch bản lỗi ở bảng điều khiển</span>
          </div>
          <button type="button" class="infra2d-btn infra2d-btn-primary" id="ing2dBtnNext" onclick="changeIngestion2DSlide(1)">Mô Phỏng Tiếp Theo →</button>
        </div>
      </div>
    `;
  }

  function toggleIngestion2DSummaryModal() {
    const d = document.getElementById("ing2dSummaryDrawer");
    if (!d) return;
    d.style.display = (d.style.display === "none" || !d.style.display) ? "block" : "none";
  }

  function changeIngestion2DSlide(delta) {
    const next = ing2dCurrentSlide + delta;
    if (next < 0 || next >= ING2D_SLIDES.length) return;
    ing2dCurrentSlide = next;
    renderIngestion2DSlide();
  }

  function jumpIngestion2DSlide(idx) {
    if (idx < 0 || idx >= ING2D_SLIDES.length) return;
    ing2dCurrentSlide = idx;
    renderIngestion2DSlide();
  }

  function renderIngestion2DSlide() {
    const root = document.getElementById("ing2dWidgetRoot");
    if (!root) return;
    const slide = ING2D_SLIDES[ing2dCurrentSlide] || ING2D_SLIDES[0];

    document.getElementById("ing2dChapterBadge").textContent = slide.chapter;
    document.getElementById("ing2dSlideNumPill").textContent = `SLIDE ${slide.id} / ${ING2D_SLIDES.length}`;
    document.getElementById("ing2dAnalogyPill").textContent = slide.analogy;
    document.getElementById("ing2dSlideTitle").textContent = slide.title;
    document.getElementById("ing2dLeadTitle").textContent = slide.leadTitle;
    document.getElementById("ing2dLeadStory").textContent = slide.leadStory;

    const kpEl = document.getElementById("ing2dKeypoints");
    kpEl.innerHTML = slide.keypoints.map(kp => `
      <div class="infra2d-kp-item">
        <div class="infra2d-kp-badge">${escapeHtml(kp.b)}</div>
        <div>
          <span class="infra2d-kp-title">${escapeHtml(kp.t)}</span>
          <p class="infra2d-kp-desc">${escapeHtml(kp.d)}</p>
        </div>
      </div>
    `).join("");

    document.getElementById("ing2dVerdictBox").textContent = slide.verdict;

    const dotsEl = document.getElementById("ing2dDots");
    dotsEl.innerHTML = ING2D_SLIDES.map((s, idx) => `
      <button type="button" class="infra2d-dot-btn ${idx === ing2dCurrentSlide ? 'active' : ''}" onclick="jumpIngestion2DSlide(${idx})">${s.id}</button>
    `).join("");

    const prevBtn = document.getElementById("ing2dBtnPrev");
    const nextBtn = document.getElementById("ing2dBtnNext");
    if (prevBtn) prevBtn.disabled = (ing2dCurrentSlide === 0);
    if (nextBtn) nextBtn.disabled = (ing2dCurrentSlide === ING2D_SLIDES.length - 1);

    const fillEl = document.getElementById("ing2dProgressFill");
    if (fillEl) fillEl.style.width = `${((ing2dCurrentSlide + 1) / ING2D_SLIDES.length) * 100}%`;

    renderIngestion2DInteractiveStage(slide.simMode);
  }

  function renderIngestion2DInteractiveStage(mode) {
    const stage = document.getElementById("ing2dSimStage");
    const status = document.getElementById("ing2dSimStatusText");
    const ctrls = document.getElementById("ing2dSimControls");
    if (!stage || !status || !ctrls) return;

    if (mode === "cdc") {
      const m = ing2dState.cdcMode;
      const isDel = ing2dState.cdcHardDelete;
      const cpuVal = m === "poll" ? "78% (Quét SeqScan)" : (m === "trig" ? "46% (Ghi kép x2)" : "2% (Đọc tuần tự WAL)");
      const latVal = m === "poll" ? "5 phút (Batch)" : (m === "trig" ? "26 ms (+14ms khóa)" : "12 ms (Real-time)");
      const delStatus = (m === "poll" && isDel) ? "MẤT DẤU (Blind!)" : (isDel ? "Bắt được op='d'" : "Bắt được op='c'/'u'");
      const schemaMod = m === "poll" ? "Phải thêm is_deleted" : (m === "trig" ? "Phải tạo shadow_table" : "0 sửa bảng gốc");

      const pollActive = m === "poll";
      const trigActive = m === "trig";
      const walActive = m === "wal";

      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 250" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <marker id="ingArrCyan" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><polygon points="0 0, 7 3.5, 0 7" fill="var(--sim-flow)"/></marker>
            <marker id="ingArrAmber" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><polygon points="0 0, 7 3.5, 0 7" fill="var(--sim-warn)"/></marker>
            <marker id="ingArrRose" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><polygon points="0 0, 7 3.5, 0 7" fill="var(--sim-danger)"/></marker>
            <marker id="ingArrEmerald" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><polygon points="0 0, 7 3.5, 0 7" fill="var(--sim-ok)"/></marker>
          </defs>

          <!-- Outer Source DBMS Cross-Section Frame -->
          <rect x="12" y="10" width="335" height="230" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="22" y="27" fill="var(--sim-muted)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">CẮT LỚP NỘI TẠNG POSTGRESQL (SOURCE OLTP)</text>

          <!-- Layer 1: SQL Query Parser & Executor -->
          <rect x="24" y="36" width="310" height="40" rx="6" fill="${pollActive ? 'var(--sim-danger-soft)' : 'var(--sim-card)'}" stroke="${pollActive ? 'var(--sim-danger)' : 'var(--sim-border)'}" stroke-width="1.5"/>
          <text x="34" y="53" fill="var(--sim-ink)" font-size="11" font-weight="700">[Tầng 1] SQL Parser &amp; Query Executor</text>
          <text x="34" y="68" fill="var(--sim-muted)" font-size="9.5" font-family="var(--cds-font-mono)">${isDel ? 'DELETE FROM orders WHERE id = 8888;' : 'INSERT / UPDATE orders (#8888, 450.000đ)'}</text>

          <!-- Layer 2: Trigger Engine -->
          <rect x="24" y="86" width="310" height="42" rx="6" fill="${trigActive ? 'var(--sim-warn-soft)' : 'var(--sim-card)'}" stroke="${trigActive ? 'var(--sim-warn)' : 'var(--sim-border)'}" stroke-width="1.5"/>
          <text x="34" y="103" fill="var(--sim-ink)" font-size="11" font-weight="700">[Tầng 2] Synchronous Trigger Engine</text>
          <text x="34" y="118" fill="${trigActive ? 'var(--sim-warn)' : 'var(--sim-muted)'}" font-size="9.5" font-family="var(--cds-font-mono)">${trigActive ? 'AFTER INS/UPD/DEL → Ghi thêm vào shadow_table (Chậm x2!)' : 'Không gắn Trigger (0ms Overhead)'}</text>

          <!-- Layer 3: 8KB Heap Pages & B-Tree -->
          <rect x="24" y="138" width="310" height="42" rx="6" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="34" y="155" fill="var(--sim-ink)" font-size="11" font-weight="700">[Tầng 3] 8KB Slotted Heap Pages &amp; B-Tree</text>
          <text x="34" y="170" fill="${isDel ? 'var(--sim-danger)' : 'var(--sim-muted)'}" font-size="9.5" font-family="var(--cds-font-mono)">${isDel ? 'Dòng #8888 đã bị xóa vật lý khỏi trang đĩa!' : 'Lưu dòng #8888 (last_modified = 12:00:05)'}</text>

          <!-- Layer 4: Append-Only Transaction Log (pg_wal) -->
          <rect x="24" y="190" width="310" height="42" rx="6" fill="${walActive ? 'var(--sim-ok-soft)' : 'var(--sim-card)'}" stroke="${walActive ? 'var(--sim-ok)' : 'var(--sim-border)'}" stroke-width="1.5"/>
          <text x="34" y="207" fill="var(--sim-ink)" font-size="11" font-weight="700">[Tầng 4] Transaction Log (pg_wal / binlog)</text>
          <text x="34" y="222" fill="var(--sim-ok)" font-size="9.5" font-family="var(--cds-font-mono)">LSN=0/16B3748 | op=${isDel ? "'d' (before=#8888)" : "'u' (before/after)"}</text>

          <!-- Right Side: CDC Collector & Kafka Topic -->
          <rect x="382" y="36" width="166" height="86" rx="8" fill="var(--sim-card)" stroke="${pollActive ? 'var(--sim-danger)' : (trigActive ? 'var(--sim-warn)' : 'var(--sim-ok)')}" stroke-width="1.8"/>
          <text x="394" y="56" fill="var(--sim-ink)" font-size="11" font-weight="800">${pollActive ? '1. Polling CronJob' : (trigActive ? '2. Shadow Table Reader' : '3. Debezium Engine')}</text>
          <text x="394" y="74" fill="var(--sim-sub)" font-size="9.5">${pollActive ? 'SELECT * WHERE updated > T' : (trigActive ? 'Đọc bảng orders_audit_log' : 'Đọc khe nhân bản pgoutput')}</text>
          <text x="394" y="92" fill="${(pollActive && isDel) ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">${(pollActive && isDel) ? '[x] 0 rows (Bỏ lỡ DELETE!)' : '[+] Bắt trọn sự kiện #8888'}</text>
          <text x="394" y="109" fill="var(--sim-muted)" font-size="9" font-family="var(--cds-font-mono)">CPU Nguồn: ${pollActive ? '78%' : (trigActive ? '46%' : '2%')}</text>

          <rect x="382" y="154" width="166" height="78" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="394" y="174" fill="var(--sim-flow)" font-size="10.5" font-weight="800" font-family="var(--cds-font-mono)">KAFKA TOPIC: prod.orders</text>
          <text x="394" y="193" fill="var(--sim-sub)" font-size="9.5" font-family="var(--cds-font-mono)">${(pollActive && isDel) ? '[!] Dữ liệu đích bị lệch!' : 'Offset 42: Key=ORD-8888'}</text>
          <text x="394" y="209" fill="var(--sim-muted)" font-size="9" font-family="var(--cds-font-mono)">${(pollActive && isDel) ? 'Đơn đã xóa vẫn còn ở Đích' : (isDel ? 'Payload: op="d", after=null' : 'Payload: op="u", amt=450000')}</text>

          <!-- Internal DB Write Flow (L1 -> L2 -> L3 -> L4) -->
          <path d="M 175 76 L 175 190" stroke="var(--sim-border-muted)" stroke-width="1.5" stroke-dasharray="3 3"/>

          <!-- Active CDC Probe Path + Animated Packet -->
          ${pollActive ? `
            <path id="cdcProbePath" d="M 334 56 L 382 56" stroke="var(--sim-danger)" stroke-width="2.5" class="ing2d-flow-active" marker-end="url(#ingArrRose)"/>
            <path d="M 334 158 C 360 158, 355 75, 382 75" stroke="var(--sim-danger)" stroke-width="1.8" stroke-dasharray="4 4"/>
            ${!isDel ? `
              <path id="cdcOutPath" d="M 465 122 L 465 154" stroke="var(--sim-danger)" stroke-width="2.2" class="ing2d-flow-active" marker-end="url(#ingArrRose)"/>
              <circle r="5" fill="var(--sim-danger)"><animateMotion dur="1.4s" repeatCount="indefinite" path="M 334 56 L 382 56 L 465 122 L 465 154"/></circle>
            ` : `
              <text x="405" y="143" fill="var(--sim-danger)" font-size="10" font-weight="800">✗ ĐỨT LUỒNG (MÙ DELETE)</text>
            `}
          ` : ""}

          ${trigActive ? `
            <path id="cdcProbePath" d="M 334 107 L 382 80" stroke="var(--sim-warn)" stroke-width="2.5" class="ing2d-flow-active" marker-end="url(#ingArrAmber)"/>
            <path id="cdcOutPath" d="M 465 122 L 465 154" stroke="var(--sim-warn)" stroke-width="2.2" class="ing2d-flow-active" marker-end="url(#ingArrAmber)"/>
            <circle r="5" fill="var(--sim-warn)"><animateMotion dur="1.5s" repeatCount="indefinite" path="M 334 107 L 382 80 L 465 122 L 465 154"/></circle>
          ` : ""}

          ${walActive ? `
            <path id="cdcProbePath" d="M 334 211 C 362 211, 354 82, 382 82" stroke="var(--sim-ok)" stroke-width="2.6" class="ing2d-flow-active" marker-end="url(#ingArrEmerald)"/>
            <path id="cdcOutPath" d="M 465 122 L 465 154" stroke="var(--sim-flow)" stroke-width="2.4" class="ing2d-flow-active" marker-end="url(#ingArrCyan)"/>
            <circle r="5.5" fill="var(--sim-ok)"><animateMotion dur="1.2s" repeatCount="indefinite" path="M 334 211 C 362 211, 354 82, 382 82 L 465 122 L 465 154"/></circle>
          ` : ""}
        </svg>
        <div class="ing2d-metrics-strip">
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Tải CPU Nguồn</span><span class="ing2d-metric-val" style="color:${pollActive ? 'var(--sim-danger)' : (trigActive ? 'var(--sim-warn)' : 'var(--sim-ok)')}">${cpuVal}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Độ Trễ Giao Dịch</span><span class="ing2d-metric-val">${latVal}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Trạng Thái DELETE</span><span class="ing2d-metric-val" style="color:${(pollActive && isDel) ? 'var(--sim-danger)' : 'var(--sim-ok)'}">${delStatus}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Xâm Phạm Schema</span><span class="ing2d-metric-val">${schemaMod}</span></div>
        </div>
      `;

      if (pollActive && isDel) {
        status.innerHTML = `<strong style="color:var(--sim-danger);">[CẢNH BÁO MẤT DỮ LIỆU]:</strong> Khi chạy lệnh vật lý <code>DELETE FROM orders WHERE id=8888</code>, bản ghi biến mất khỏi B-Tree/Heap. Truy vấn <code>SELECT WHERE last_modified &gt; T</code> trả về 0 dòng — kho dữ liệu đích giữ mãi đơn hàng ảo!`;
      } else if (pollActive) {
        status.innerHTML = `<strong style="color:var(--sim-danger);">[Thế hệ 1 — Timestamp Polling]:</strong> Đặt đầu dò tại Tầng 1 (SQL Executor). Cứ mỗi chu kỳ lại quét bảng làm CPU vọt lên 78% và có nguy cơ bỏ sót giao dịch treo (Uncommitted Transaction Skew).`;
      } else if (trigActive) {
        status.innerHTML = `<strong style="color:var(--sim-warn);">[Thế hệ 2 — Trigger-Based CDC]:</strong> Đặt đầu dò tại Tầng 2 (Trigger Engine). Bắt được cả lệnh <code>DELETE</code> nhờ biến <code>OLD.*</code>, nhưng bắt khách hàng chờ ghi xong cả Bảng Chính lẫn <code>shadow_table</code> (độ trễ tăng gấp đôi 12ms → 26ms).`;
      } else {
        status.innerHTML = `<strong style="color:var(--sim-ok);">[Thế hệ 3 — Log-Based CDC (Debezium)]:</strong> Đặt đầu dò tại Tầng 4 (<code>pg_wal</code> LSN=0/16B3748). Không chạm vào SQL Engine hay Bảng Chính, tiêu tốn chỉ ~2% CPU và bắt trọn vẹn mọi thao tác <code>INSERT/UPDATE/DELETE</code> theo thời gian thực!`;
      }

      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${pollActive ? 'infra2d-btn-danger' : ''}" onclick="ing2dState.cdcMode='poll';renderIngestion2DInteractiveStage('cdc')">1. Timestamp Polling (L1)</button>
        <button type="button" class="infra2d-btn ${trigActive ? 'infra2d-btn-amber' : ''}" onclick="ing2dState.cdcMode='trig';renderIngestion2DInteractiveStage('cdc')">2. Trigger Shadow Table (L2)</button>
        <button type="button" class="infra2d-btn ${walActive ? 'infra2d-btn-emerald' : ''}" onclick="ing2dState.cdcMode='wal';renderIngestion2DInteractiveStage('cdc')">3. Log-Based WAL / Debezium (L4)</button>
        <button type="button" class="infra2d-btn ${isDel ? 'infra2d-btn-primary' : ''}" onclick="ing2dState.cdcHardDelete=!ing2dState.cdcHardDelete;renderIngestion2DInteractiveStage('cdc')">${isDel ? 'Đang bật: Lệnh Hard DELETE #8888' : 'Thử thách: Bắn lệnh Hard DELETE #8888'}</button>
      `;
    } else if (mode === "producer") {
      const isKeyed = (ing2dState.prodMode === "keyed");
      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 250" fill="none" xmlns="http://www.w3.org/2000/svg">
          <!-- Producer Internal Pipeline (Left) -->
          <rect x="12" y="12" width="235" height="226" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="22" y="29" fill="var(--sim-muted)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">CẮT LỚP KAFKA PRODUCER CLIENT</text>

          <rect x="24" y="38" width="210" height="38" rx="6" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.3"/>
          <text x="32" y="54" fill="var(--sim-ink)" font-size="10.5" font-weight="700">[1] Avro Serializer (Schema ID)</text>
          <text x="32" y="68" fill="var(--sim-flow)" font-size="9" font-family="var(--cds-font-mono)">${isKeyed ? 'Key="USR-104" | #8888 (E1→E2→E3)' : 'Key=null | #8888 (E1→E2→E3)'}</text>

          <rect x="24" y="88" width="210" height="44" rx="6" fill="${isKeyed ? 'var(--sim-ok-soft)' : 'var(--sim-warn-soft)'}" stroke="${isKeyed ? 'var(--sim-ok)' : 'var(--sim-warn)'}" stroke-width="1.5"/>
          <text x="32" y="105" fill="var(--sim-ink)" font-size="10.5" font-weight="700">[2] Partitioner Router</text>
          <text x="32" y="121" fill="${isKeyed ? 'var(--sim-ok)' : 'var(--sim-warn)'}" font-size="9" font-family="var(--cds-font-mono)">${isKeyed ? 'murmur2("USR-104") % 3 == Partition 1' : 'Round-Robin / Sticky → Rải P0, P1, P2'}</text>

          <rect x="24" y="144" width="210" height="42" rx="6" fill="var(--sim-card)" stroke="var(--sim-clay)" stroke-width="1.3"/>
          <text x="32" y="160" fill="var(--sim-ink)" font-size="10.5" font-weight="700">[3] RecordAccumulator (RAM Batch)</text>
          <text x="32" y="175" fill="var(--sim-clay)" font-size="9" font-family="var(--cds-font-mono)">batch.size=64KB | linger.ms=10ms | LZ4</text>

          <rect x="24" y="196" width="210" height="32" rx="6" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.3"/>
          <text x="32" y="216" fill="var(--sim-sub)" font-size="10" font-weight="700">[4] Sender I/O Thread (Async Push)</text>

          <!-- Right Side: Kafka Topic Partitions 0, 1, 2 -->
          <rect x="305" y="12" width="243" height="226" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="315" y="29" fill="var(--sim-muted)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">TOPIC: prod.orders (3 PARTITIONS)</text>

          <!-- Partition 0 -->
          <rect x="317" y="40" width="218" height="54" rx="6" fill="var(--sim-card)" stroke="${!isKeyed ? 'var(--sim-warn)' : 'var(--sim-border)'}" stroke-width="1.5"/>
          <text x="327" y="57" fill="var(--sim-ink)" font-size="10.5" font-weight="700">Partition 0 (Broker 1)</text>
          <text x="327" y="76" fill="${!isKeyed ? 'var(--sim-warn)' : 'var(--sim-muted)'}" font-size="9.5" font-family="var(--cds-font-mono)">${!isKeyed ? '[Off 0: E1 CREATED #8888]' : '[Trống — Dành cho Key khác]'}</text>

          <!-- Partition 1 -->
          <rect x="317" y="106" width="218" height="58" rx="6" fill="${isKeyed ? 'var(--sim-ok-soft)' : 'var(--sim-card)'}" stroke="${isKeyed ? 'var(--sim-ok)' : 'var(--sim-warn)'}" stroke-width="1.8"/>
          <text x="327" y="123" fill="var(--sim-ink)" font-size="10.5" font-weight="700">Partition 1 (Broker 2)</text>
          <text x="327" y="141" fill="${isKeyed ? 'var(--sim-ok)' : 'var(--sim-warn)'}" font-size="9.2" font-family="var(--cds-font-mono)">${isKeyed ? '[Off 10: E1 CREATED] → [Off 11: E2 PAID]' : '[Off 0: E2 PAID #8888]'}</text>
          <text x="327" y="155" fill="${isKeyed ? 'var(--sim-ok)' : 'var(--sim-muted)'}" font-size="9.2" font-family="var(--cds-font-mono)">${isKeyed ? '→ [Off 12: E3 SHIPPED] (Đúng thứ tự 100%!)' : '(Chỉ nhận 1/3 sự kiện)'}</text>

          <!-- Partition 2 -->
          <rect x="317" y="176" width="218" height="52" rx="6" fill="var(--sim-card)" stroke="${!isKeyed ? 'var(--sim-warn)' : 'var(--sim-border)'}" stroke-width="1.5"/>
          <text x="327" y="193" fill="var(--sim-ink)" font-size="10.5" font-weight="700">Partition 2 (Broker 3)</text>
          <text x="327" y="212" fill="${!isKeyed ? 'var(--sim-danger)' : 'var(--sim-muted)'}" font-size="9.5" font-family="var(--cds-font-mono)">${!isKeyed ? '[Off 0: E3 SHIPPED] (Đọc trước cả E1!)' : '[Trống — Dành cho Key khác]'}</text>

          <!-- Animated Routing Wires -->
          ${isKeyed ? `
            <path d="M 234 110 C 275 110, 275 135, 317 135" stroke="var(--sim-ok)" stroke-width="2.8" class="ing2d-flow-active"/>
            <circle r="5.5" fill="var(--sim-ok)"><animateMotion dur="1.1s" repeatCount="indefinite" path="M 234 110 C 275 110, 275 135, 317 135"/></circle>
          ` : `
            <path d="M 234 110 C 270 110, 275 67, 317 67" stroke="var(--sim-warn)" stroke-width="2" class="ing2d-flow-active"/>
            <path d="M 234 110 C 270 110, 275 135, 317 135" stroke="var(--sim-warn)" stroke-width="2" class="ing2d-flow-active"/>
            <path d="M 234 110 C 270 110, 275 202, 317 202" stroke="var(--sim-danger)" stroke-width="2" class="ing2d-flow-active"/>
            <circle r="4.5" fill="var(--sim-warn)"><animateMotion dur="1.2s" repeatCount="indefinite" path="M 234 110 C 270 110, 275 67, 317 67"/></circle>
            <circle r="4.5" fill="var(--sim-flow)"><animateMotion dur="1.4s" repeatCount="indefinite" path="M 234 110 C 270 110, 275 135, 317 135"/></circle>
            <circle r="4.5" fill="var(--sim-danger)"><animateMotion dur="1.0s" repeatCount="indefinite" path="M 234 110 C 270 110, 275 202, 317 202"/></circle>
          `}
        </svg>
        <div class="ing2d-metrics-strip">
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Thuật Toán Chọn</span><span class="ing2d-metric-val">${isKeyed ? 'murmur2(key) % 3' : 'Sticky / Round-Robin'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Partition Đích</span><span class="ing2d-metric-val" style="color:${isKeyed ? 'var(--sim-ok)' : 'var(--sim-warn)'}">${isKeyed ? '100% vào Partition 1' : 'Rải đều P0, P1, P2'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Bảo Toàn Thứ Tự</span><span class="ing2d-metric-val" style="color:${isKeyed ? 'var(--sim-ok)' : 'var(--sim-danger)'}">${isKeyed ? 'Đảm bảo 100% (E1→E2→E3)' : 'MẤT THỨ TỰ (Race!)'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Nén Lô RAM</span><span class="ing2d-metric-val">64KB / LZ4</span></div>
        </div>
      `;

      status.innerHTML = isKeyed
        ? `<strong style="color:var(--sim-ok);">[Chế độ Có Khóa — With Key = "USR-104"]:</strong> Hàm băm <code>murmur2("USR-104") % 3</code> luôn trả về <code>Partition 1</code>. Cả 3 sự kiện <code>CREATED → PAID → SHIPPED</code> của đơn #8888 nằm nối đuôi nhau trên cùng một Partition, bảo toàn 100% thứ tự nhân quả!`
        : `<strong style="color:var(--sim-danger);">[Chế độ Không Khóa — Without Key = null]:</strong> Các sự kiện của đơn #8888 bị rải ra 3 Partition khác nhau (<code>P0</code>, <code>P1</code>, <code>P2</code>). Nếu Consumer đọc <code>P2</code> chạy nhanh hơn <code>P0</code>, hệ thống đích sẽ nhận lệnh <code>SHIPPED</code> trước cả khi đơn hàng được <code>CREATED</code>!`;

      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${isKeyed ? 'infra2d-btn-emerald' : ''}" onclick="ing2dState.prodMode='keyed';renderIngestion2DInteractiveStage('producer')">1. Có Khóa: key="USR-104" (murmur2 → P1)</button>
        <button type="button" class="infra2d-btn ${!isKeyed ? 'infra2d-btn-amber' : ''}" onclick="ing2dState.prodMode='keyless';renderIngestion2DInteractiveStage('producer')">2. Không Khóa: key=null (Rải đều P0, P1, P2)</button>
      `;
    } else if (mode === "consumer") {
      const cCount = ing2dState.consCount;
      // Map partitions P0, P1, P2 to consumers 1..cCount
      let pMap = [0, 0, 0];
      if (cCount === 1) pMap = [1, 1, 1];
      else if (cCount === 2) pMap = [1, 1, 2];
      else pMap = [1, 2, 3]; // for 3 or 4 consumers, C4 is IDLE!

      const pY = [62, 125, 188];
      const cY = cCount === 1 ? [125] : (cCount === 2 ? [90, 165] : (cCount === 3 ? [62, 125, 188] : [48, 98, 148, 198]));

      let wiresSvg = "";
      for (let p = 0; p < 3; p++) {
        const targetC = pMap[p] - 1;
        const y1 = pY[p];
        const y2 = cY[targetC];
        const pathStr = `M 212 ${y1} C 265 ${y1}, 275 ${y2}, 330 ${y2}`;
        wiresSvg += `
          <path d="${pathStr}" stroke="var(--sim-flow)" stroke-width="2.4" class="ing2d-flow-active"/>
          <circle r="4.8" fill="var(--sim-ok)"><animateMotion dur="${1.1 + p * 0.2}s" repeatCount="indefinite" path="${pathStr}"/></circle>
        `;
      }

      let consBoxesSvg = "";
      for (let c = 0; c < cCount; c++) {
        const isIdle = (c === 3);
        const cy = cY[c] - 20;
        const assignedParts = [];
        for (let p = 0; p < 3; p++) if (pMap[p] === c + 1) assignedParts.push(`P${p}`);
        consBoxesSvg += `
          <rect x="330" y="${cy}" width="212" height="40" rx="6" fill="${isIdle ? 'var(--sim-danger-soft)' : 'var(--sim-card)'}" stroke="${isIdle ? 'var(--sim-danger)' : 'var(--sim-ok)'}" stroke-width="1.6"/>
          <text x="340" y="${cy + 16}" fill="var(--sim-ink)" font-size="10.5" font-weight="700">Consumer ${c + 1} ${isIdle ? '[IDLE — NHÀN RỖI!]' : '[Active]'}</text>
          <text x="340" y="${cy + 31}" fill="${isIdle ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="9.2" font-family="var(--cds-font-mono)">${isIdle ? '0 Partition (Do P=3 < C=4!)' : 'Độc quyền đọc: ' + assignedParts.join(', ')}</text>
        `;
      }

      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 250" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="12" y="12" width="200" height="226" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="22" y="29" fill="var(--sim-muted)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">TOPIC: prod.orders (P=3)</text>

          <rect x="24" y="40" width="176" height="44" rx="6" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.4"/>
          <text x="34" y="58" fill="var(--sim-ink)" font-size="10.5" font-weight="700">Partition 0</text>
          <text x="34" y="74" fill="var(--sim-muted)" font-size="9" font-family="var(--cds-font-mono)">Off 0..42 (10 MB/s)</text>

          <rect x="24" y="103" width="176" height="44" rx="6" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.4"/>
          <text x="34" y="121" fill="var(--sim-ink)" font-size="10.5" font-weight="700">Partition 1 (#8888)</text>
          <text x="34" y="137" fill="var(--sim-flow)" font-size="9" font-family="var(--cds-font-mono)">Off 0..58 (10 MB/s)</text>

          <rect x="24" y="166" width="176" height="44" rx="6" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.4"/>
          <text x="34" y="184" fill="var(--sim-ink)" font-size="10.5" font-weight="700">Partition 2</text>
          <text x="34" y="200" fill="var(--sim-muted)" font-size="9" font-family="var(--cds-font-mono)">Off 0..39 (10 MB/s)</text>

          <rect x="318" y="12" width="230" height="226" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="328" y="29" fill="var(--sim-muted)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">CONSUMER GROUP: fraud-detector</text>

          ${wiresSvg}
          ${consBoxesSvg}
        </svg>
        <div class="ing2d-metrics-strip">
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Số Partition (P)</span><span class="ing2d-metric-val">3 Partitions</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Số Consumer (C)</span><span class="ing2d-metric-val">${cCount} Consumers</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Tổng Thông Lượng</span><span class="ing2d-metric-val" style="color:${cCount >= 3 ? 'var(--sim-ok)' : 'var(--sim-warn)'}">${Math.min(3, cCount) * 10} MB/s</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Consumer Dư Thừa</span><span class="ing2d-metric-val" style="color:${cCount > 3 ? 'var(--sim-danger)' : 'var(--sim-ok)'}">${cCount > 3 ? '1 IDLE (C4 ngồi chơi!)' : '0 IDLE (100% bận)'}</span></div>
        </div>
      `;

      if (cCount === 1) {
        status.innerHTML = `<strong style="color:var(--sim-warn);">[1 Consumer đọc cả 3 Partitions]:</strong> Một mình Consumer 1 phải gánh toàn bộ P0, P1, P2. Thông lượng bị kẹt ở mức 10 MB/s và <code>Consumer Lag</code> tăng nhanh.`;
      } else if (cCount === 2) {
        status.innerHTML = `<strong style="color:var(--sim-flow);">[2 Consumers chia tải lệch (2 + 1)]:</strong> Group Coordinator gán <code>P0, P1 → Consumer 1</code> và <code>P2 → Consumer 2</code>. Consumer 1 vẫn chịu tải gấp đôi Consumer 2.`;
      } else if (cCount === 3) {
        status.innerHTML = `<strong style="color:var(--sim-ok);">[3 Consumers — Điểm Cân Bằng Vàng 1:1]:</strong> Mỗi Partition được độc quyền bởi đúng 1 Consumer (<code>P0→C1, P1→C2, P2→C3</code>). Thông lượng đạt đỉnh 30 MB/s và <code>Consumer Lag = 0</code>!`;
      } else {
        status.innerHTML = `<strong style="color:var(--sim-danger);">[4 Consumers > 3 Partitions — Cảnh báo IDLE!]:</strong> Do quy tắc bất biến <em>"Trong cùng 1 Consumer Group, mỗi Partition chỉ được đọc bởi tối đa 1 Consumer"</em>, <strong>Consumer 4 không được cấp Partition nào và phải ngồi chơi (IDLE)</strong>! Muốn 4 Consumers cùng chạy, bắt buộc phải tăng số Partition của Topic lên &ge; 4.`;
      }

      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${cCount === 1 ? 'infra2d-btn-amber' : ''}" onclick="ing2dState.consCount=1;renderIngestion2DInteractiveStage('consumer')">1 Consumer (Quá tải)</button>
        <button type="button" class="infra2d-btn ${cCount === 2 ? 'infra2d-btn-cyan' : ''}" onclick="ing2dState.consCount=2;renderIngestion2DInteractiveStage('consumer')">2 Consumers (Lệch 2:1)</button>
        <button type="button" class="infra2d-btn ${cCount === 3 ? 'infra2d-btn-emerald' : ''}" onclick="ing2dState.consCount=3;renderIngestion2DInteractiveStage('consumer')">3 Consumers (Tối ưu 1:1)</button>
        <button type="button" class="infra2d-btn ${cCount === 4 ? 'infra2d-btn-danger' : ''}" onclick="ing2dState.consCount=4;renderIngestion2DInteractiveStage('consumer')">4 Consumers (C4 bị IDLE!)</button>
      `;
    } else if (mode === "replication") {
      const sc = ing2dState.repScenario; // 'normal' | 'acks1_crash' | 'acksall_crash'
      const isNormal = (sc === "normal");
      const isAcks1Crash = (sc === "acks1_crash");
      const isAcksAllCrash = (sc === "acksall_crash");

      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 250" fill="none" xmlns="http://www.w3.org/2000/svg">
          <!-- Producer Box -->
          <rect x="14" y="88" width="136" height="74" rx="8" fill="var(--sim-card)" stroke="${isAcks1Crash ? 'var(--sim-danger)' : 'var(--sim-flow)'}" stroke-width="1.6"/>
          <text x="24" y="108" fill="var(--sim-ink)" font-size="10.5" font-weight="800">Kafka Producer</text>
          <text x="24" y="125" fill="var(--sim-flow)" font-size="9.2" font-family="var(--cds-font-mono)">Order #8888 (Off 42)</text>
          <text x="24" y="142" fill="${isAcks1Crash ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="9.2" font-weight="700" font-family="var(--cds-font-mono)">acks = ${isAcks1Crash ? '1 (Nguy hiểm!)' : 'all (An toàn)'}</text>

          <!-- Kafka Cluster 3 Brokers -->
          <rect x="188" y="10" width="358" height="230" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="200" y="27" fill="var(--sim-muted)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">KAFKA CLUSTER (REPLICATION FACTOR = 3, MIN.INSYNC = 2)</text>

          <!-- Broker 1 -->
          <rect x="202" y="38" width="330" height="56" rx="6" fill="${isNormal ? 'var(--sim-ok-soft)' : 'var(--sim-danger-soft)'}" stroke="${isNormal ? 'var(--sim-ok)' : 'var(--sim-danger)'}" stroke-width="1.7"/>
          <text x="214" y="57" fill="var(--sim-ink)" font-size="11" font-weight="800">Broker 1 — ${isNormal ? 'LEADER REPLICA (Active)' : '✗ SẬP NGUỒN ĐỘT NGỘT (CRASHED!)'}</text>
          <text x="214" y="76" fill="${isNormal ? 'var(--sim-ok)' : 'var(--sim-danger)'}" font-size="9.5" font-family="var(--cds-font-mono)">${isNormal ? 'Log: [Off 40][Off 41][Off 42: #8888] (LEO=43)' : (isAcks1Crash ? 'Đã nhận #8888 & trả ACK=1 nhưng CHẾT trước khi B2/B3 kịp kéo!' : 'Sập sau khi B2 & B3 đã đồng bộ xong #8888!')}</text>

          <!-- Broker 2 -->
          <rect x="202" y="106" width="330" height="58" rx="6" fill="${!isNormal ? 'var(--sim-flow-soft)' : 'var(--sim-card)'}" stroke="${!isNormal ? 'var(--sim-flow)' : 'var(--sim-border)'}" stroke-width="1.7"/>
          <text x="214" y="125" fill="var(--sim-ink)" font-size="11" font-weight="800">Broker 2 — ${isNormal ? 'Follower Replica (Trong tập ISR)' : '★ TỰ ĐỘNG THĂNG CẤP LÀM LEADER MỚI!'}</text>
          <text x="214" y="144" fill="${isAcks1Crash ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="9.5" font-family="var(--cds-font-mono)">${isAcks1Crash ? 'Log: [Off 40][Off 41] → MẤT VĨNH VIỄN Off 42 (#8888)!' : 'Log: [Off 40][Off 41][Off 42: #8888] (Bảo toàn 100%!)'}</text>

          <!-- Broker 3 -->
          <rect x="202" y="176" width="330" height="52" rx="6" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="214" y="195" fill="var(--sim-ink)" font-size="11" font-weight="700">Broker 3 — Follower Replica (Trong tập ISR)</text>
          <text x="214" y="213" fill="${isAcks1Crash ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="9.5" font-family="var(--cds-font-mono)">${isAcks1Crash ? 'Log: [Off 40][Off 41] (Chưa kịp kéo Off 42)' : 'Log: [Off 40][Off 41][Off 42: #8888] (In-Sync)'}</text>

          ${isNormal ? `
            <path d="M 150 118 C 175 118, 175 66, 202 66" stroke="var(--sim-ok)" stroke-width="2.5" class="ing2d-flow-active"/>
            <path d="M 365 94 L 365 106" stroke="var(--sim-flow)" stroke-width="2" class="ing2d-flow-active"/>
            <path d="M 365 164 L 365 176" stroke="var(--sim-flow)" stroke-width="2" class="ing2d-flow-active"/>
            <circle r="5" fill="var(--sim-ok)"><animateMotion dur="1.1s" repeatCount="indefinite" path="M 150 118 C 175 118, 175 66, 202 66"/></circle>
          ` : `
            <path d="M 150 132 L 202 132" stroke="${isAcks1Crash ? 'var(--sim-danger)' : 'var(--sim-flow)'}" stroke-width="2.5" class="ing2d-flow-active"/>
            <circle r="5" fill="${isAcks1Crash ? 'var(--sim-danger)' : 'var(--sim-flow)'}"><animateMotion dur="1.1s" repeatCount="indefinite" path="M 150 132 L 202 132"/></circle>
          `}
        </svg>
        <div class="ing2d-metrics-strip">
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Leader Hiện Tại</span><span class="ing2d-metric-val">${isNormal ? 'Broker 1' : 'Broker 2 (Failover)'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Tập Hợp ISR</span><span class="ing2d-metric-val">${isNormal ? '{B1, B2, B3}' : '{B2, B3}'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Cấu Hình Producer</span><span class="ing2d-metric-val">${isAcks1Crash ? 'acks = 1' : 'acks = all'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Số Phận Đơn #8888</span><span class="ing2d-metric-val" style="color:${isAcks1Crash ? 'var(--sim-danger)' : 'var(--sim-ok)'}">${isAcks1Crash ? 'MẤT DỮ LIỆU (Data Loss!)' : 'An toàn tuyệt đối (0% Loss)'}</span></div>
        </div>
      `;

      if (isNormal) {
        status.innerHTML = `<strong style="color:var(--sim-ok);">[Trạng thái Bình thường — RF=3, ISR={B1, B2, B3}]:</strong> Producer ghi đơn #8888 vào <code>Broker 1 (Leader)</code>. Hai máy <code>Broker 2</code> và <code>Broker 3</code> liên tục kéo bản sao về để giữ trạng thái đồng bộ trong tập <code>ISR</code>.`;
      } else if (isAcks1Crash) {
        status.innerHTML = `<strong style="color:var(--sim-danger);">[Cạm bẫy Mất Dữ liệu của acks=1 (Slide 39)]:</strong> Producer nhận báo thành công ngay khi <code>Broker 1</code> vừa ghi xong đĩa cục bộ. Đúng tích tắc đó <code>Broker 1</code> cháy nguồn trước khi <code>Broker 2 &amp; 3</code> kịp chép #8888 về! Khi <code>Broker 2</code> lên làm Leader mới, đơn #8888 biến mất vĩnh viễn!`;
      } else {
        status.innerHTML = `<strong style="color:var(--sim-ok);">[Chốt chặn Bất tử: acks=all + min.insync.replicas=2]:</strong> <code>Broker 1</code> chỉ được phép trả ACK cho Producer sau khi các Follower trong <code>ISR</code> đã chép xong #8888. Khi <code>Broker 1</code> sập, <code>Broker 2</code> tự động thăng cấp làm Leader mới trong vài mili-giây với 0% mất mát dữ liệu!`;
      }

      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${isNormal ? 'infra2d-btn-emerald' : ''}" onclick="ing2dState.repScenario='normal';renderIngestion2DInteractiveStage('replication')">1. Bình thường (ISR = {B1, B2, B3})</button>
        <button type="button" class="infra2d-btn ${isAcks1Crash ? 'infra2d-btn-danger' : ''}" onclick="ing2dState.repScenario='acks1_crash';renderIngestion2DInteractiveStage('replication')">2. Sập Broker 1 với acks=1 (Mất đơn #8888!)</button>
        <button type="button" class="infra2d-btn ${isAcksAllCrash ? 'infra2d-btn-cyan' : ''}" onclick="ing2dState.repScenario='acksall_crash';renderIngestion2DInteractiveStage('replication')">3. Sập Broker 1 với acks=all + min.insync=2 (An toàn 100%)</button>
      `;
    } else if (mode === "compaction") {
      const cm = ing2dState.compMode; // 'dirty' | 'compacted' | 'tombstone'
      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 250" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="12" y="10" width="536" height="230" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="24" y="28" fill="var(--sim-muted)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">CẮT LỚP THƯ MỤC ĐĨA VẬT LÝ: /var/lib/kafka/data/prod.orders-1/ (SLIDE 40)</text>

          <!-- Top Row: Segment Files on Disk -->
          <rect x="24" y="38" width="160" height="46" rx="6" fill="var(--sim-card)" stroke="var(--sim-border-muted)" stroke-width="1.3"/>
          <text x="32" y="55" fill="var(--sim-sub)" font-size="10" font-weight="700">000000000000.log</text>
          <text x="32" y="71" fill="var(--sim-muted)" font-size="9" font-family="var(--cds-font-mono)">Closed Segment (&gt;7d → unlink O(1))</text>

          <rect x="198" y="38" width="164" height="46" rx="6" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.4"/>
          <text x="206" y="55" fill="var(--sim-ink)" font-size="10" font-weight="700">000000000010.log</text>
          <text x="206" y="71" fill="var(--sim-flow)" font-size="9" font-family="var(--cds-font-mono)">Clean Head + .index + .timeindex</text>

          <rect x="376" y="38" width="160" height="46" rx="6" fill="var(--sim-card)" stroke="var(--sim-ok)" stroke-width="1.4"/>
          <text x="384" y="55" fill="var(--sim-ink)" font-size="10" font-weight="700">000000000050.log</text>
          <text x="384" y="71" fill="var(--sim-ok)" font-size="9" font-family="var(--cds-font-mono)">Active Segment (Append-only)</text>

          <!-- Bottom Area: Log Compaction Cells -->
          <text x="24" y="108" fill="var(--sim-sub)" font-size="10.5" font-weight="700">Cơ chế Nén Nhật ký Theo Khóa (cleanup.policy = compact — Keep latest value per Key):</text>

          <!-- Offset 10 -->
          <rect x="24" y="120" width="118" height="92" rx="6" fill="${cm === 'dirty' ? 'var(--sim-card)' : 'var(--sim-danger-soft)'}" stroke="${cm === 'dirty' ? 'var(--sim-flow)' : 'var(--sim-border-muted)'}" stroke-dasharray="${cm === 'dirty' ? '0' : '4 4'}" stroke-width="1.5"/>
          <text x="32" y="139" fill="var(--sim-muted)" font-size="9.5" font-family="var(--cds-font-mono)">Offset 10</text>
          <text x="32" y="157" fill="var(--sim-ink)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">Key: ORD-8888</text>
          <text x="32" y="175" fill="var(--sim-sub)" font-size="9.5" font-family="var(--cds-font-mono)">status: PENDING</text>
          <text x="32" y="197" fill="${cm === 'dirty' ? 'var(--sim-warn)' : 'var(--sim-danger)'}" font-size="9" font-weight="700">${cm === 'dirty' ? 'Bản cũ #1' : '✗ Đã dọn (Superseded)'}</text>

          <!-- Offset 11 (Other order) -->
          <rect x="154" y="120" width="118" height="92" rx="6" fill="var(--sim-ok-soft)" stroke="var(--sim-ok)" stroke-width="1.6"/>
          <text x="162" y="139" fill="var(--sim-muted)" font-size="9.5" font-family="var(--cds-font-mono)">Offset 11</text>
          <text x="162" y="157" fill="var(--sim-ink)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">Key: ORD-9999</text>
          <text x="162" y="175" fill="var(--sim-ok)" font-size="9.5" font-family="var(--cds-font-mono)">status: PAID</text>
          <text x="162" y="197" fill="var(--sim-ok)" font-size="9" font-weight="700">✓ Giữ nguyên (Khóa khác)</text>

          <!-- Offset 12 -->
          <rect x="284" y="120" width="118" height="92" rx="6" fill="${cm === 'dirty' ? 'var(--sim-card)' : 'var(--sim-danger-soft)'}" stroke="${cm === 'dirty' ? 'var(--sim-flow)' : 'var(--sim-border-muted)'}" stroke-dasharray="${cm === 'dirty' ? '0' : '4 4'}" stroke-width="1.5"/>
          <text x="292" y="139" fill="var(--sim-muted)" font-size="9.5" font-family="var(--cds-font-mono)">Offset 12</text>
          <text x="292" y="157" fill="var(--sim-ink)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">Key: ORD-8888</text>
          <text x="292" y="175" fill="var(--sim-sub)" font-size="9.5" font-family="var(--cds-font-mono)">status: PAID</text>
          <text x="292" y="197" fill="${cm === 'dirty' ? 'var(--sim-warn)' : 'var(--sim-danger)'}" font-size="9" font-weight="700">${cm === 'dirty' ? 'Bản cũ #2' : '✗ Đã dọn (Superseded)'}</text>

          <!-- Offset 13 (Latest or Tombstone) -->
          <rect x="414" y="120" width="122" height="92" rx="6" fill="${cm === 'tombstone' ? 'var(--sim-danger-soft)' : 'var(--sim-flow-soft)'}" stroke="${cm === 'tombstone' ? 'var(--sim-danger)' : 'var(--sim-flow)'}" stroke-width="1.8"/>
          <text x="422" y="139" fill="var(--sim-muted)" font-size="9.5" font-family="var(--cds-font-mono)">${cm === 'tombstone' ? 'Offset 14 (Tombstone)' : 'Offset 13 (Mới nhất)'}</text>
          <text x="422" y="157" fill="var(--sim-ink)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">Key: ORD-8888</text>
          <text x="422" y="175" fill="${cm === 'tombstone' ? 'var(--sim-danger)' : 'var(--sim-flow)'}" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">${cm === 'tombstone' ? 'value: null' : 'status: SHIPPED'}</text>
          <text x="422" y="197" fill="${cm === 'tombstone' ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="9" font-weight="700">${cm === 'tombstone' ? '[DEL] Bia mộ xóa khóa!' : '★ Bản ghi giữ lại!'}</text>
        </svg>
        <div class="ing2d-metrics-strip">
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Time/Size Retention</span><span class="ing2d-metric-val">7 days / 1 GB</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Log Compaction</span><span class="ing2d-metric-val">${cm === 'dirty' ? 'Chưa chạy (4 bản ghi)' : (cm === 'compacted' ? 'Đã nén (Còn 2 bản ghi)' : 'Tombstone (Xóa #8888)')}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Trạng Thái #8888</span><span class="ing2d-metric-val" style="color:${cm === 'tombstone' ? 'var(--sim-danger)' : 'var(--sim-ok)'}">${cm === 'tombstone' ? 'value = null (Purge)' : 'SHIPPED (Off 13)'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Chi Phí Xóa Đĩa</span><span class="ing2d-metric-val">O(1) Sequential I/O</span></div>
        </div>
      `;

      if (cm === "dirty") {
        status.innerHTML = `<strong style="color:var(--sim-flow);">[1. Vùng Dirty Tail trước khi nén]:</strong> Mọi thay đổi của <code>ORD-8888</code> (<code>Off 10: PENDING</code>, <code>Off 12: PAID</code>, <code>Off 13: SHIPPED</code>) được ghi nối đuôi tuần tự vào tệp <code>.log</code> đang mở.`;
      } else if (cm === "compacted") {
        status.innerHTML = `<strong style="color:var(--sim-ok);">[2. Sau khi Log Cleaner thực thi Log Compaction]:</strong> Luồng nền của Broker quét gộp các Segment, tự động loại bỏ <code>Offset 10</code> và <code>Offset 12</code> đã lỗi thời, chỉ giữ lại trạng thái cuối cùng <code>Offset 13 (SHIPPED)</code> cho khóa <code>ORD-8888</code>!`;
      } else {
        status.innerHTML = `<strong style="color:var(--sim-danger);">[3. Bản ghi Bia mộ Tombstone (key="ORD-8888", value=null)]:</strong> Khi đơn hàng bị xóa vật lý, Debezium bắn một bản ghi có <code>value = null</code>. Các Consumer nhận tín hiệu xóa khỏi bảng đích, và sau thời gian <code>delete.retention.ms</code>, Log Cleaner thu hồi vĩnh viễn khóa <code>ORD-8888</code> khỏi đĩa!`;
      }

      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${cm === 'dirty' ? 'infra2d-btn-cyan' : ''}" onclick="ing2dState.compMode='dirty';renderIngestion2DInteractiveStage('compaction')">1. Trước khi nén (Dirty Tail: 4 Offsets)</button>
        <button type="button" class="infra2d-btn ${cm === 'compacted' ? 'infra2d-btn-emerald' : ''}" onclick="ing2dState.compMode='compacted';renderIngestion2DInteractiveStage('compaction')">2. Chạy Log Compaction (Giữ bản mới nhất)</button>
        <button type="button" class="infra2d-btn ${cm === 'tombstone' ? 'infra2d-btn-danger' : ''}" onclick="ing2dState.compMode='tombstone';renderIngestion2DInteractiveStage('compaction')">3. Bắn Tombstone (key=#8888, value=null)</button>
      `;
    } else {
      // Slide 6: Production Challenges
      const ch = ing2dState.chalMode; // 'bloat' | 'heartbeat' | 'dlq' | 'outbox'
      const isBloat = (ch === "bloat");
      const isHb = (ch === "heartbeat");
      const isDlq = (ch === "dlq");
      const isOutbox = (ch === "outbox");

      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 250" fill="none" xmlns="http://www.w3.org/2000/svg">
          <!-- Box 1: Source PostgreSQL + Outbox + WAL -->
          <rect x="12" y="14" width="175" height="222" rx="8" fill="var(--sim-canvas)" stroke="${isBloat ? 'var(--sim-danger)' : 'var(--sim-ok)'}" stroke-width="1.6"/>
          <text x="22" y="32" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">1. POSTGRESQL SOURCE</text>

          <rect x="22" y="42" width="155" height="52" rx="6" fill="var(--sim-card)" stroke="${isOutbox ? 'var(--sim-flow)' : 'var(--sim-border)'}" stroke-width="1.4"/>
          <text x="30" y="58" fill="var(--sim-ink)" font-size="10" font-weight="700">${isOutbox ? 'ACID: orders + outbox' : 'Bảng: shop.orders'}</text>
          <text x="30" y="74" fill="${isOutbox ? 'var(--sim-flow)' : 'var(--sim-muted)'}" font-size="8.8" font-family="var(--cds-font-mono)">${isOutbox ? 'Chống lỗi Dual-Write 100%' : 'Ghi giao dịch #8888'}</text>

          <rect x="22" y="106" width="155" height="62" rx="6" fill="${isBloat ? 'var(--sim-danger-soft)' : 'var(--sim-ok-soft)'}" stroke="${isBloat ? 'var(--sim-danger)' : 'var(--sim-ok)'}" stroke-width="1.6"/>
          <text x="30" y="123" fill="var(--sim-ink)" font-size="10" font-weight="700">pg_wal &amp; Replication Slot</text>
          <text x="30" y="140" fill="${isBloat ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">${isBloat ? '[!] DISK: 96% (WAL BLOAT!)' : '✓ DISK: 14% (Đã xả WAL)'}</text>
          <text x="30" y="156" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">${isBloat ? 'confirmed_flush_lsn ĐỨNG IM' : 'heartbeat.interval.ms=10s'}</text>

          <rect x="22" y="178" width="155" height="46" rx="6" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.2"/>
          <text x="30" y="195" fill="var(--sim-sub)" font-size="9.5" font-weight="700">Chốt trần an toàn DB:</text>
          <text x="30" y="211" fill="var(--sim-flow)" font-size="8.5" font-family="var(--cds-font-mono)">max_slot_wal_keep_size=10GB</text>

          <!-- Box 2: Debezium + Kafka + Schema Registry -->
          <rect x="208" y="14" width="160" height="222" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="218" y="32" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">2. DEBEZIUM &amp; KAFKA</text>

          <rect x="218" y="42" width="140" height="52" rx="6" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.3"/>
          <text x="226" y="58" fill="var(--sim-ink)" font-size="10" font-weight="700">Debezium Connector</text>
          <text x="226" y="74" fill="var(--sim-flow)" font-size="8.8" font-family="var(--cds-font-mono)">plugin.name = pgoutput</text>

          <rect x="218" y="106" width="140" height="58" rx="6" fill="var(--sim-card)" stroke="var(--sim-clay)" stroke-width="1.4"/>
          <text x="226" y="123" fill="var(--sim-ink)" font-size="10" font-weight="700">Schema Registry</text>
          <text x="226" y="140" fill="var(--sim-clay)" font-size="8.8" font-family="var(--cds-font-mono)">Avro BACKWARD / FULL</text>
          <text x="226" y="154" fill="var(--sim-muted)" font-size="8.5" font-family="var(--cds-font-mono)">Chặn Schema Drift từ gốc</text>

          <rect x="218" y="176" width="140" height="48" rx="6" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.2"/>
          <text x="226" y="194" fill="var(--sim-ink)" font-size="9.5" font-weight="700">Kafka Connect Offsets</text>
          <text x="226" y="210" fill="var(--sim-ok)" font-size="8.5" font-family="var(--cds-font-mono)">connect-offsets (Compact)</text>

          <!-- Box 3: Sink Connector + Lakehouse + DLQ -->
          <rect x="390" y="14" width="158" height="222" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="400" y="32" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">3. MULTI-SINK &amp; DLQ</text>

          <rect x="400" y="42" width="138" height="72" rx="6" fill="var(--sim-ok-soft)" stroke="var(--sim-ok)" stroke-width="1.5"/>
          <text x="408" y="60" fill="var(--sim-ink)" font-size="10" font-weight="700">Data Lakehouse (D02)</text>
          <text x="408" y="77" fill="var(--sim-ok)" font-size="8.8" font-family="var(--cds-font-mono)">+ Elastic + Redis + Flink</text>
          <text x="408" y="95" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">Nhận dòng sạch #8888</text>

          <rect x="400" y="132" width="138" height="92" rx="6" fill="${isDlq ? 'var(--sim-warn-soft)' : 'var(--sim-card)'}" stroke="${isDlq ? 'var(--sim-warn)' : 'var(--sim-border-muted)'}" stroke-width="1.6"/>
          <text x="408" y="151" fill="var(--sim-warn)" font-size="10" font-weight="800">Dead Letter Queue (DLQ)</text>
          <text x="408" y="168" fill="var(--sim-sub)" font-size="8.8" font-family="var(--cds-font-mono)">errors.tolerance = all</text>
          <text x="408" y="185" fill="${isDlq ? 'var(--sim-danger)' : 'var(--sim-muted)'}" font-size="8.8" font-family="var(--cds-font-mono)">${isDlq ? 'Đã cách ly 1 Poison Pill!' : 'Kênh cách ly bản ghi lỗi'}</text>
          <text x="408" y="203" fill="var(--sim-ok)" font-size="8.5" font-family="var(--cds-font-mono)">Đường ống chính KHÔNG SẬP</text>

          <!-- Animated Connectors -->
          ${!isBloat ? `
            <path d="M 177 135 L 218 68" stroke="var(--sim-ok)" stroke-width="2.4" class="ing2d-flow-active"/>
            <circle r="5" fill="var(--sim-ok)"><animateMotion dur="1.1s" repeatCount="indefinite" path="M 177 135 L 218 68"/></circle>
          ` : `
            <line x1="177" y1="135" x2="218" y2="68" stroke="var(--sim-danger)" stroke-width="2.2" stroke-dasharray="3 3"/>
          `}
          <path d="M 358 68 L 400 68" stroke="var(--sim-flow)" stroke-width="2.4" class="ing2d-flow-active"/>
          <circle r="4.8" fill="var(--sim-flow)"><animateMotion dur="1.0s" repeatCount="indefinite" path="M 358 68 L 400 68"/></circle>
          ${isDlq ? `
            <path d="M 358 135 L 400 175" stroke="var(--sim-warn)" stroke-width="2.4" class="ing2d-flow-active"/>
            <circle r="5" fill="var(--sim-warn)"><animateMotion dur="1.1s" repeatCount="indefinite" path="M 358 135 L 400 175"/></circle>
          ` : ""}
        </svg>
        <div class="ing2d-metrics-strip">
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Ổ Cứng pg_wal</span><span class="ing2d-metric-val" style="color:${isBloat ? 'var(--sim-danger)' : 'var(--sim-ok)'}">${isBloat ? '96% (Báo động đỏ!)' : '14% (An toàn)'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Heartbeat LSN</span><span class="ing2d-metric-val">${isBloat ? 'Tắt (Kẹt LSN)' : '10.000 ms (Active)'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Xử Lý Poison Pill</span><span class="ing2d-metric-val">${isDlq ? 'Cách ly vào DLQ' : 'Schema Registry + DLQ'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Tính Nguyên Tử</span><span class="ing2d-metric-val">${isOutbox ? 'Transactional Outbox' : 'Log-Based CDC'}</span></div>
        </div>
      `;

      if (isBloat) {
        status.innerHTML = `<strong style="color:var(--sim-danger);">[Sự cố #1 — Đầy ổ cứng PostgreSQL do kẹt Replication Slot (WAL Bloat)]:</strong> Khi Debezium ngắt kết nối hoặc bảng <code>orders</code> ít ghi trong khi các bảng khác ghi ồ ạt, con trỏ <code>confirmed_flush_lsn</code> không nhích lên được. PostgreSQL giữ lại toàn bộ tệp <code>pg_wal</code> làm đầy 96% ổ đĩa!`;
      } else if (isHb) {
        status.innerHTML = `<strong style="color:var(--sim-ok);">[Phác đồ Giải cứu WAL Bloat]:</strong> Bật <code>heartbeat.interval.ms = 10000</code> kèm <code>heartbeat.action.query</code> để Debezium chủ động đẩy con trỏ <code>confirmed_flush_lsn</code> định kỳ, đồng thời khóa trần <code>max_slot_wal_keep_size = 10GB</code> trong <code>postgresql.conf</code>!`;
      } else if (isDlq) {
        status.innerHTML = `<strong style="color:var(--sim-warn);">[Phác đồ Chống Tin Nhắn Độc (Poison Pill) &amp; Schema Drift]:</strong> Khi gặp một bản ghi hỏng định dạng, Kafka Connect Sink cấu hình <code>errors.tolerance = all</code> sẽ tự động bẻ lái bản ghi lỗi kèm Stacktrace vào kênh cách ly <strong>Dead Letter Queue (DLQ)</strong>, giúp luồng dữ liệu chính chạy xuyên suốt 24/7!`;
      } else {
        status.innerHTML = `<strong style="color:var(--sim-flow);">[Phác đồ Chống Ghi Kép (Dual-Write) bằng Transactional Outbox Pattern]:</strong> Thay vì vừa <code>COMMIT</code> vào DB vừa gọi <code>producer.send()</code> trên code dễ gây lệch trạng thái khi sập mạng, ứng dụng ghi đồng thời vào bảng <code>orders</code> và bảng <code>outbox_events</code> trong cùng 1 ACID Transaction cục bộ!`;
      }

      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${isBloat ? 'infra2d-btn-danger' : ''}" onclick="ing2dState.chalMode='bloat';renderIngestion2DInteractiveStage('challenges')">1. Sự cố: Kẹt Slot → Nổ đĩa pg_wal (96%)</button>
        <button type="button" class="infra2d-btn ${isHb ? 'infra2d-btn-emerald' : ''}" onclick="ing2dState.chalMode='heartbeat';renderIngestion2DInteractiveStage('challenges')">2. Giải cứu WAL: Heartbeat + max_slot_wal_keep_size</button>
        <button type="button" class="infra2d-btn ${isDlq ? 'infra2d-btn-amber' : ''}" onclick="ing2dState.chalMode='dlq';renderIngestion2DInteractiveStage('challenges')">3. Cô lập Poison Pill sang Dead Letter Queue (DLQ)</button>
        <button type="button" class="infra2d-btn ${isOutbox ? 'infra2d-btn-cyan' : ''}" onclick="ing2dState.chalMode='outbox';renderIngestion2DInteractiveStage('challenges')">4. Chống Dual-Write: Transactional Outbox</button>
      `;
    }
  }

  /* ==========================================================================
     UNIFIED TOPIC RENDERER (DECLARATIVE TOPIC_CONFIG FOR F01, F03, F06, D02)
     ========================================================================== */
  const PICTO_DB = (HUB_DATA && HUB_DATA.pictograms) ? HUB_DATA.pictograms : { sealViewBox: "0 0 947.805 952.224", sealPath: "", pictograms: {} };
  const MASK_DB = (HUB_DATA && HUB_DATA.masks) ? HUB_DATA.masks : {};

  function renderPictogramSvg(name, fallbackSvg = "") {
    const p = (PICTO_DB.pictograms && PICTO_DB.pictograms[name]) || null;
    if (!p) return fallbackSvg || "";
    const hlPaths = (p.highlight || []).map(d => `<path d="${d}" fill="var(--swatch-band, #ebc9b7)"/>`).join("");
    const lnPaths = (p.line || []).map(d => `<path d="${d}" fill="var(--swatch-fg, var(--cds-text-primary, currentColor))"/>`).join("");
    return `<svg viewBox="0 0 500 500" fill="none" aria-hidden="true">${hlPaths}${lnPaths}</svg>`;
  }

  function renderBadgeSealHtml(pictoName, sealTitle, fallbackSvg = "") {
    const pictoHtml = renderPictogramSvg(pictoName, fallbackSvg);
    const sealVb = PICTO_DB.sealViewBox || "0 0 947.805 952.224";
    const sealPath = PICTO_DB.sealPath || "";
    return `
      <div class="cds-badge-seal">
        ${sealPath ? `<svg class="cds-badge-seal-svg" viewBox="${sealVb}" fill="none" aria-hidden="true"><path d="${sealPath}" fill="var(--swatch-seal, #faf5f2)" stroke="color-mix(in oklab, var(--swatch-0, #141413) 42%, transparent)" stroke-width="5"/></svg>` : ""}
        <div class="cds-badge-seal-inner">
          <span class="cds-badge-seal-kicker">FSDS ACADEMY</span>
          <div class="cds-badge-seal-picto">${pictoHtml}</div>
          <span class="cds-badge-seal-title">${escapeHtml(sealTitle)}</span>
        </div>
      </div>
    `;
  }

  function renderContentThumbHtml(swatchCls, maskFile, pictoName, metaLabel, fallbackSvg = "") {
    const pictoHtml = renderPictogramSvg(pictoName, fallbackSvg);
    const maskUrl = (maskFile && MASK_DB[maskFile]) ? MASK_DB[maskFile] : (maskFile ? `assets/masks/${maskFile}` : "");
    const maskStyle = maskUrl
      ? `style="-webkit-mask-image:url('${maskUrl}');mask-image:url('${maskUrl}');"`
      : "";
    return `
      <div class="cds-content-thumb ${swatchCls}" aria-hidden="true">
        ${maskUrl ? `<div class="cds-thumb-mask" ${maskStyle}></div>` : ""}
        <div class="cds-thumb-stack">
          <div class="cds-thumb-fan is-left"></div>
          <div class="cds-thumb-fan is-right"></div>
          <div class="cds-thumb-front">
            <div class="cds-thumb-picto">${pictoHtml}</div>
            <span class="cds-thumb-meta">${escapeHtml(metaLabel)}</span>
          </div>
        </div>
      </div>
    `;
  }

  const TRACK_VISUAL_DEFAULTS = {
    "track-1": { swatchClass: "swatch-cactus", maskFile: "loops.svg", pictogram: "ObjectCodeTerminal" },
    "track-2": { swatchClass: "swatch-oat", maskFile: "strata.svg", pictogram: "ObjectClouds" },
    "track-3": { swatchClass: "swatch-sky", maskFile: "vines.svg", pictogram: "ObjectCompass" },
    "track-4": { swatchClass: "swatch-fig", maskFile: "snowflake.svg", pictogram: "ObjectBookApple" }
  };

  const TOPIC_CONFIG = {
    F01: {
      stages: LINUX_STAGES,
      swatchClass: "swatch-cactus",
      maskFile: "loops.svg",
      pictogram: "ObjectCodeTerminal",
      sealTitle: "F01 · Linux & Bash",
      heroSvg: `<svg viewBox="0 0 120 120" fill="none" aria-hidden="true"><rect x="14" y="22" width="92" height="76" rx="14" fill="var(--cds-color-swatch-base-primary)" fill-opacity="0.16" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="2.5"/><path d="M28 46L44 60L28 74M52 74H78" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="28" cy="33" r="3" fill="var(--cds-color-swatch-contrast-primary)"/><circle cx="38" cy="33" r="3" fill="var(--cds-color-swatch-contrast-primary)"/></svg>`,
      metaTrack: "I. Engineering Foundation · F01 · Linux Fundamentals",
      slideHref: "course-slides/01-linux-fundamentals.pdf",
      slideLabel: "Slide gốc: 01-linux-fundamentals.pdf (78 trang)",
      titleHtml: "Fundamentals of Engineering — Linux &amp; Bash Scripting",
      leadHtml: "Làm chủ kiến trúc GNU/Linux Kernel, quản lý tiến trình (Process &amp; Inode), điều hướng luồng I/O (<code>stdin/stdout/stderr</code>, Pipe) và tự động hóa vận hành với Bash Script, GNU Make và Cron.",
      stageStatus: (st) => st.id <= 4 ? "Đã xuất bản" : "Khung trạm"
    },
    F03: {
      stages: DB_STAGES,
      swatchClass: "swatch-peach",
      maskFile: "swoops.svg",
      pictogram: "NodeTree",
      sealTitle: "F03 · Database Internals",
      heroSvg: `<svg viewBox="0 0 120 120" fill="none" aria-hidden="true"><ellipse cx="60" cy="32" rx="38" ry="14" fill="var(--cds-color-swatch-base-primary)" fill-opacity="0.22" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="2.5"/><path d="M22 32V60C22 67.7 39 74 60 74C81 74 98 67.7 98 60V32" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="2.5"/><path d="M22 60V88C22 95.7 39 102 60 102C81 102 98 95.7 98 88V60" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="2.5"/><circle cx="60" cy="54" r="4" fill="var(--cds-color-swatch-contrast-primary)"/><circle cx="60" cy="82" r="4" fill="var(--cds-color-swatch-contrast-primary)"/></svg>`,
      metaTrack: "I. Engineering Foundation · F03 · Database Fundamentals",
      slideHref: "course-slides/03-database-fundamentals.pdf",
      slideLabel: "Slide gốc: 03-database-fundamentals.pdf (70 trang)",
      titleHtml: "Fundamentals of Engineering — Database Architecture &amp; PostgreSQL Internals",
      leadHtml: "Nắm vững thiết kế cơ sở dữ liệu chuẩn hóa (3NF/BCNF), kiến trúc lưu trữ nội tại của PostgreSQL (<code>8KB Slotted Page</code>, WAL, MVCC, B-Tree/LSM-Tree), tối ưu truy vấn <code>EXPLAIN ANALYZE</code> và phân tán dữ liệu (Replication, Sharding, CAP/BASE).",
      stageStatus: () => "Đã xuất bản"
    },
    F06: {
      stages: CONTAINER_STAGES,
      swatchClass: "swatch-heather",
      maskFile: "threads.svg",
      pictogram: "ObjectBricks",
      sealTitle: "F06 · Containers & K8s",
      heroSvg: `<svg viewBox="0 0 120 120" fill="none" aria-hidden="true"><rect x="18" y="26" width="36" height="30" rx="6" fill="var(--cds-color-swatch-base-primary)" fill-opacity="0.2" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="2.5"/><rect x="66" y="26" width="36" height="30" rx="6" fill="var(--cds-color-swatch-base-primary)" fill-opacity="0.2" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="2.5"/><rect x="18" y="66" width="84" height="28" rx="8" fill="var(--cds-color-swatch-base-primary)" fill-opacity="0.14" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="2.5"/><path d="M36 56V66M84 56V66" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="2.5" stroke-linecap="round"/></svg>`,
      metaTrack: "I. Engineering Foundation · F06 · Containerization &amp; Orchestration",
      slideHref: "course-slides/06-containerization-and-orchestration.pdf",
      slideLabel: "Slide gốc: 06-containerization-and-orchestration.pdf (72 trang)",
      titleHtml: "Fundamentals of Engineering — Containerization (Docker / OCI) &amp; Kubernetes Orchestration",
      leadHtml: "Hiểu bản chất ảo hóa cấp hệ điều hành (Linux Namespaces, <code>cgroups v2</code>, OverlayFS), kiến trúc động cơ OCI Runtime (<code>containerd</code>/<code>runc</code>), đóng gói ứng dụng với Docker Compose và điều phối cụm container trên Kubernetes.",
      stageStatus: () => "Đã xuất bản"
    },
    D01: {
      stages: INGESTION_STAGES,
      swatchClass: "swatch-fig",
      maskFile: "vines.svg",
      pictogram: "NodeTree",
      sealTitle: "D01 · Kafka & Debezium CDC",
      heroSvg: `<svg viewBox="0 0 120 120" fill="none" aria-hidden="true"><circle cx="30" cy="60" r="14" fill="var(--cds-color-swatch-base-primary)" fill-opacity="0.22" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="2.5"/><circle cx="90" cy="34" r="14" fill="var(--cds-color-swatch-base-primary)" fill-opacity="0.22" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="2.5"/><circle cx="90" cy="86" r="14" fill="var(--cds-color-swatch-base-primary)" fill-opacity="0.22" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="2.5"/><path d="M43 54L77 39M43 66L77 81M90 48V72" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="2.5" stroke-linecap="round"/></svg>`,
      metaTrack: "II. Data Engineering · D01 · Ingestion Layer",
      slideHref: "course-slides/07-ingestion-layer.pdf",
      slideLabel: "Slide gốc: 07-ingestion-layer.pdf (45 trang)",
      titleHtml: "Data Engineering — Ingestion Layer, Apache Kafka &amp; Real-Time Debezium CDC",
      leadHtml: "Làm chủ kiến trúc thu thập dữ liệu hiện đại: từ giải phẫu hệ thống nguồn (OLTP/OLAP, GIGO, Push/Pull/Poll, Row/Column/Hybrid Parquet), ba thế hệ Change Data Capture (Timestamp Polling, Trigger, Log-Based WAL/binlog), đến cơ học vận hành cụm <strong>Apache Kafka</strong> (KRaft, Partition Sizing, Zero-Copy, Producer <code>murmur2</code>, Consumer Group, <code>ISR</code>, <code>Exactly-once</code>, Log Compaction) và đường ống <strong>Debezium CDC</strong> thực chiến.",
      stageStatus: () => "Đã xuất bản"
    },
    D02: {
      stages: STORAGE_STAGES,
      swatchClass: "swatch-oat",
      maskFile: "strata.svg",
      pictogram: "ObjectClouds",
      sealTitle: "D02 · Storage & Lakehouse",
      heroSvg: `<svg viewBox="0 0 120 120" fill="none" aria-hidden="true"><path d="M60 18L102 38L60 58L18 38L60 18Z" fill="var(--cds-color-swatch-base-primary)" fill-opacity="0.22" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="2.5" stroke-linejoin="round"/><path d="M18 60L60 80L102 60" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M18 82L60 102L102 82" stroke="var(--cds-color-swatch-contrast-primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
      metaTrack: "II. Data Engineering · D02 · Storage Layer",
      slideHref: "course-slides/08-storage-layer.pdf",
      slideLabel: "Slide gốc: 08-storage-layer.pdf (59 trang)",
      titleHtml: "Data Engineering — Storage Layer &amp; Open Lakehouse Architecture",
      leadHtml: "Thiết kế tầng lưu trữ dữ liệu quy mô lớn: từ cơ học vật lý (RAM/SSD/Object Storage) và định dạng cột (Parquet, Arrow), mô hình hóa kho dữ liệu (Inmon, Kimball Star Schema, SCD), đến Open Data Lakehouse (Delta Lake, Iceberg, Hudi) và kiến trúc Medallion.",
      stageStatus: (st) => (st.id >= 1 && st.id <= 7) ? "Đã xuất bản" : "Chờ cập nhật"
    }
  };

  function renderTopic(topicCode = activeTopic) {
    const cfg = TOPIC_CONFIG[topicCode];
    if (!cfg) {
      const { group, item } = findTopicContext(topicCode);
      return renderPendingTopic(item, group.title);
    }
    const stages = cfg.stages;
    const totalStages = stages.length;
    const currentStage = stages.find(s => s.id === activeStorageStage) || stages[0];
    const padNum = n => String(n).padStart(2, "0");

    const stagePillsHtml = stages.map(st => {
      const isAct = st.id === activeStorageStage;
      const cleanShort = st.shortTitle || st.title.replace(/^Chặng \d+:\s*/, "");
      return `
        <button type="button" class="stage-pill-btn ${isAct ? 'active' : ''}" onclick="selectStorageStage(${st.id})" title="${escapeHtml(st.title)}">
          <span class="stage-pill-num">Chặng ${padNum(st.id)}</span>
          <span class="stage-pill-title">${escapeHtml(cleanShort)}</span>
          <span class="stage-pill-state">${isAct ? 'Đang học ●' : 'Mở →'}</span>
        </button>
      `;
    }).join("");

    const stations = getTopicStations(topicCode, activeStorageStage);
    const objectivesHtml = stations.map(st => {
      const codeLabel = (st.code === "Khung" || st.code === "Kết") ? st.code : `Trạm ${st.code}`;
      return `
        <li>
          <a href="#${st.id}" class="lesson-objective-link" onclick="jumpToStation('${st.id}');return false;">
            <span class="lesson-objective-code">${escapeHtml(codeLabel)}</span>
            <span>${escapeHtml(st.title)}</span>
          </a>
        </li>
      `;
    }).join("");

    const topicRenderers = LESSON_RENDERERS[topicCode] || {};
    const stageRenderer = topicRenderers[activeStorageStage] || topicRenderers[1];
    const bodyHtml = stageRenderer ? stageRenderer() : "";
    const stageCleanTitle = currentStage.title.replace(/^Chặng \d+:\s*/, "");
    const swatchCls = cfg.swatchClass || "swatch-oat";

    return `
      <header class="lesson-header ${swatchCls}">
        <div class="lesson-hero-dots" aria-hidden="true"></div>
        <div class="lesson-header-grid has-artwork">
          <div class="lesson-header-copy">
            <div class="lesson-meta">
              <span class="cds-swatch-pill">${cfg.metaTrack}</span>
              <a class="cds-swatch-pill" href="${cfg.slideHref}" target="_blank" rel="noopener">${cfg.slideLabel} ↗</a>
            </div>
            <h1 class="lesson-title">${cfg.titleHtml}</h1>
            <p class="lesson-stage-subtitle">Chặng ${padNum(currentStage.id)} / ${padNum(totalStages)} · ${escapeHtml(stageCleanTitle)}</p>
            <p class="lesson-lead">${cfg.leadHtml}</p>
          </div>
          <div class="lesson-hero-art" aria-hidden="true">
            ${renderBadgeSealHtml(cfg.pictogram, cfg.sealTitle || topicCode, cfg.heroSvg)}
          </div>
        </div>
        <div class="lesson-roadmap-grid">
          <nav class="stage-pills-bar" aria-label="Danh sách các chặng trong học phần (xếp chồng)">
            <span class="stage-pills-label">Lộ trình ${totalStages} chặng học (Xếp chồng)</span>
            ${stagePillsHtml}
          </nav>
          <div class="lesson-objectives-card">
            <span class="lesson-objectives-title">Trọng tâm Chặng ${padNum(currentStage.id)} (${stations.length} trạm kiến thức)</span>
            <ul class="lesson-objectives-list">
              ${objectivesHtml}
            </ul>
          </div>
        </div>
      </header>
      ${bodyHtml}
      ${renderLessonPager(topicCode, stages, activeStorageStage)}
    `;
  }

  function renderLessonPager(topicCode, stages, currentStageId) {
    const padNum = n => String(n).padStart(2, "0");
    const prevStage = stages.find(s => s.id === currentStageId - 1);
    const nextStage = stages.find(s => s.id === currentStageId + 1);
    const publishedOrder = ["F01", "F03", "F06", "D01", "D02"];
    const topicIdx = publishedOrder.indexOf(topicCode);

    let prevCardHtml = `<div></div>`;
    if (prevStage) {
      prevCardHtml = `
        <button type="button" class="lesson-pager-card is-prev" onclick="selectStorageStage(${prevStage.id})">
          <span class="lesson-pager-dir">← Chặng ${padNum(prevStage.id)}</span>
          <span class="lesson-pager-title">${escapeHtml(prevStage.title.replace(/^Chặng \d+:\s*/, ""))}</span>
        </button>
      `;
    } else if (topicIdx > 0) {
      const prevTopic = publishedOrder[topicIdx - 1];
      const prevCfg = TOPIC_CONFIG[prevTopic];
      const lastStg = prevCfg.stages[prevCfg.stages.length - 1];
      prevCardHtml = `
        <button type="button" class="lesson-pager-card is-prev" onclick="selectTopic('${prevTopic}', ${lastStg.id})">
          <span class="lesson-pager-dir">← Học phần ${prevTopic} · Chặng ${padNum(lastStg.id)}</span>
          <span class="lesson-pager-title">${escapeHtml(lastStg.title.replace(/^Chặng \d+:\s*/, ""))}</span>
        </button>
      `;
    }

    let nextCardHtml = `<div></div>`;
    if (nextStage) {
      nextCardHtml = `
        <button type="button" class="lesson-pager-card is-next" onclick="selectStorageStage(${nextStage.id})">
          <span class="lesson-pager-dir">Chặng ${padNum(nextStage.id)} →</span>
          <span class="lesson-pager-title">${escapeHtml(nextStage.title.replace(/^Chặng \d+:\s*/, ""))}</span>
        </button>
      `;
    } else if (topicIdx !== -1 && topicIdx < publishedOrder.length - 1) {
      const nextTopic = publishedOrder[topicIdx + 1];
      const nextCfg = TOPIC_CONFIG[nextTopic];
      const firstStg = nextCfg.stages[0];
      nextCardHtml = `
        <button type="button" class="lesson-pager-card is-next" onclick="selectTopic('${nextTopic}', 1)">
          <span class="lesson-pager-dir">Học phần tiếp: ${nextTopic} · Chặng 01 →</span>
          <span class="lesson-pager-title">${escapeHtml(firstStg.title.replace(/^Chặng \d+:\s*/, ""))}</span>
        </button>
      `;
    }

    return `<nav class="lesson-pager" aria-label="Điều hướng Chặng trước và tiếp theo">${prevCardHtml}${nextCardHtml}</nav>`;
  }

  function renderCatalogView() {
    const featuredCodes = ["F01", "F03", "F06", "D01", "D02"];
    const featuredCards = featuredCodes.map(code => {
      const cfg = TOPIC_CONFIG[code];
      const { group, item } = findTopicContext(code);
      const thumbHtml = renderContentThumbHtml(
        cfg.swatchClass,
        cfg.maskFile,
        cfg.pictogram,
        `${cfg.stages.length} Chặng • Certificate`,
        cfg.heroSvg
      );
      return `
        <article class="catalog-card published has-thumb">
          ${thumbHtml}
          <div class="catalog-card-body">
            <div>
              <div class="catalog-card-top">
                <span class="catalog-code-pill">${escapeHtml(code)} · ${escapeHtml(group.shortTitle)}</span>
                <span class="catalog-status-pill">${cfg.stages.length} Chặng hoàn chỉnh</span>
              </div>
              <h3><a href="#/${code}/1" onclick="selectTopic('${code}', 1);return false;" style="text-decoration:none;color:var(--ink-bold);">${escapeHtml(item.title)}</a></h3>
              <div class="catalog-syllabus-meta">
                <div class="catalog-syllabus-row"><span class="catalog-syllabus-tag">Học gì:</span><span>${escapeHtml(item.modules || "")}</span></div>
                <div class="catalog-syllabus-row"><span class="catalog-syllabus-tag">Lab:</span><span>${escapeHtml(item.lab || "")}</span></div>
              </div>
            </div>
            <div class="catalog-card-footer">
              <code>${escapeHtml(item.stack || "")}</code>
              <button type="button" class="ui-btn" onclick="selectTopic('${code}', 1)">Vào học →</button>
            </div>
          </div>
        </article>
      `;
    }).join("");

    const trackSections = SYLLABUS_GROUPS.map(group => {
      const tVis = TRACK_VISUAL_DEFAULTS[group.id] || TRACK_VISUAL_DEFAULTS["track-1"];
      const cards = group.items.map(it => {
        const cfg = TOPIC_CONFIG[it.code];
        const hasFull = Boolean(cfg);
        const swatchCls = cfg ? cfg.swatchClass : tVis.swatchClass;
        const maskFile = cfg ? cfg.maskFile : tVis.maskFile;
        const pictoName = cfg ? cfg.pictogram : tVis.pictogram;
        const metaLabel = cfg ? `${cfg.stages.length} Chặng • Certificate` : `${it.pages || 60} Slides • Đề cương`;
        const thumbHtml = renderContentThumbHtml(swatchCls, maskFile, pictoName, metaLabel, cfg ? cfg.heroSvg : "");
        return `
          <article class="catalog-card has-thumb ${hasFull ? 'published' : ''}">
            ${thumbHtml}
            <div class="catalog-card-body">
              <div>
                <div class="catalog-card-top">
                  <span class="catalog-code-pill">${escapeHtml(it.code)}</span>
                  <span class="catalog-status-pill">${escapeHtml(it.contentNote || (hasFull ? 'Đã xuất bản' : 'Đề cương Slide'))}</span>
                </div>
                <h3><a href="#/${it.code}/1" onclick="selectTopic('${it.code}', 1);return false;" style="text-decoration:none;color:var(--ink-bold);">${escapeHtml(it.title)}</a></h3>
                <div class="catalog-syllabus-meta">
                  <div class="catalog-syllabus-row"><span class="catalog-syllabus-tag">Học gì:</span><span>${escapeHtml(it.modules || "")}</span></div>
                  <div class="catalog-syllabus-row"><span class="catalog-syllabus-tag">Lab:</span><span>${escapeHtml(it.lab || "")}</span></div>
                </div>
              </div>
              <div class="catalog-card-footer">
                <code>${escapeHtml(it.stack || "")}</code>
                <button type="button" class="ui-btn" onclick="selectTopic('${it.code}', 1)">${hasFull ? 'Vào học →' : 'Xem đề cương'}</button>
              </div>
            </div>
          </article>
        `;
      }).join("");
      return `
        <section style="margin-bottom:36px;">
          <h2 style="font-family:var(--cds-font-serif);font-size:22px;font-weight:400;letter-spacing:-0.015em;margin:0 0 12px;color:var(--ink-bold);">${escapeHtml(group.title)}</h2>
          <div class="catalog-grid">${cards}</div>
        </section>
      `;
    }).join("");

    return `
      <header class="catalog-hero swatch-oat">
        <div class="lesson-hero-dots" aria-hidden="true"></div>
        <div class="lesson-header-grid has-artwork">
          <div>
            <span class="catalog-kicker">FSDS · EDAI · DSAI LEARNING ACADEMY</span>
            <h1 class="lesson-title">Danh mục 26 Học phần Kỹ thuật &amp; Hệ thống Dữ liệu</h1>
            <p class="lesson-lead" style="margin-bottom:0;">Chương trình đào tạo Full-Stack Data Science, Data Engineering &amp; AI Engineering gồm 4 Track chuyên sâu: nắm vững lý thuyết cốt lõi, thực hành Lab thực chiến và làm chủ hệ thống qua 119 sơ đồ kiến trúc Colored ASCII.</p>
          </div>
          <div class="lesson-hero-art" aria-hidden="true">
            ${renderBadgeSealHtml("ObjectCompass", "26 Học phần · 4 Tracks")}
          </div>
        </div>
      </header>
      <section style="margin-bottom:40px;">
        <h2 style="font-family:var(--cds-font-serif);font-size:22px;font-weight:400;letter-spacing:-0.015em;margin:0 0 12px;color:var(--ink-bold);">Học phần Đã Xuất bản Toàn diện (19 Chặng · 119 Sơ đồ Kiến trúc)</h2>
        <div class="catalog-grid">${featuredCards}</div>
      </section>
      ${trackSections}
    `;
  }

  function openCatalogView(pushHistory = true) {
    syncStateVars("CATALOG", 1, null);
    document.body.classList.add("catalog-mode");
    document.body.classList.remove("mobile-rail-open");
    renderSyllabus();
    renderMain(false);
    if (pushHistory && !isHandlingRouteEvent) {
      history.pushState({ topic: "CATALOG", stage: 1, section: null }, "", "#/catalog");
    }
  }

  let activeGlossaryFilter = "ALL";
  let activeGlossaryQuery = "";

  function renderGlossaryCardsList() {
    const entries = Object.values(GLOSSARY_DB);
    const q = normalizeSearch(activeGlossaryQuery);
    const filtered = entries.filter(e => {
      if (activeGlossaryFilter !== "ALL") {
        const link = e.station_link || "";
        if (!link.startsWith("#/" + activeGlossaryFilter + "/")) return false;
      }
      if (!q) return true;
      const hay = normalizeSearch(`${e.term || ""} ${e.name} ${e.category} ${e.short || ""} ${(e.aliases || []).join(" ")} ${(e.example && e.example.code) || ""}`);
      return hay.includes(q);
    });

    if (!filtered.length) {
      const rawQ = (activeGlossaryQuery || "").trim();
      return `
        <div style="grid-column:1/-1;padding:24px;border-radius:12px;background:var(--cds-surface-1);border:1px solid var(--cds-border-default);display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;">
          <div>
            <strong style="display:block;font-size:15px;margin-bottom:4px;color:var(--cds-text-primary);">Chưa có "${escapeHtml(rawQ)}" trong 74 thuật ngữ mặc định — Hãy để Gemini AI giải thích ngay!</strong>
            <span style="font-size:13px;color:var(--cds-text-secondary);">AI sẽ tự động phân tích bản chất cốt lõi, cơ chế hoạt động và tạo ví dụ thực tế (kèm lưu vào TTL Cache).</span>
          </div>
          <button type="button" class="ui-btn" style="background:var(--cds-clay);color:#fff;border-color:var(--cds-clay);" onclick="openCustomAiTermModal(${JSON.stringify(rawQ)})">✦ Giải thích "${escapeHtml(rawQ)}" bằng AI</button>
        </div>
      `;
    }

    return filtered.map(e => {
      const codeStr = (e.example && e.example.code) ? e.example.code : "";
      const displayTitle = e.term || e.name || e.id;
      return `
        <article class="glossary-dict-card" id="gdict-${escapeHtml(e.id)}" tabindex="0" role="button" aria-haspopup="dialog" onclick="openGlossaryPopoverFromDict(this, '${escapeHtml(e.id)}', event)">
          <div>
            <div class="glossary-dict-card-top">
              <h3 class="glossary-dict-name">${escapeHtml(displayTitle)}</h3>
              <span class="glossary-dict-cat">${escapeHtml(e.category || "Thuật ngữ")}</span>
            </div>
            <p class="glossary-dict-desc">${escapeHtml(e.short || e.intuition || "")}</p>
          </div>
          <div>
            ${codeStr ? `<pre class="glossary-dict-code">${escapeHtml(codeStr)}</pre>` : ""}
            <div class="glossary-dict-footer">
              <span>ID: <code>${escapeHtml(e.id)}</code></span>
              <span class="glossary-dict-ai-cta">✦ Giải thích AI &amp; Ví dụ thực tế →</span>
            </div>
          </div>
        </article>
      `;
    }).join("");
  }

  function filterGlossaryDictionary(courseFilter = null, queryStr = null) {
    if (courseFilter !== null) activeGlossaryFilter = courseFilter;
    if (queryStr !== null) activeGlossaryQuery = queryStr;
    document.querySelectorAll(".glossary-filter-pill").forEach(btn => {
      btn.classList.toggle("active", btn.getAttribute("data-filter") === activeGlossaryFilter);
    });
    const grid = document.getElementById("glossaryDictGrid");
    if (grid) {
      grid.innerHTML = renderGlossaryCardsList();
    }
  }

  function renderGlossaryView() {
    const totalCount = Object.keys(GLOSSARY_DB).length;
    const filters = [
      { id: "ALL", label: `Tất cả (${totalCount})` },
      { id: "F01", label: "F01 · Linux & Bash" },
      { id: "F03", label: "F03 · Database & PostgreSQL" },
      { id: "F06", label: "F06 · Docker & Kubernetes" },
      { id: "D02", label: "D02 · Storage & Lakehouse" }
    ];
    const filterBtns = filters.map(f => `
      <button type="button" class="glossary-filter-pill ${activeGlossaryFilter === f.id ? 'active' : ''}" data-filter="${f.id}" onclick="filterGlossaryDictionary('${f.id}', null)">${escapeHtml(f.label)}</button>
    `).join("");

    return `
      <header class="catalog-hero swatch-cactus">
        <div class="lesson-hero-dots" aria-hidden="true"></div>
        <div class="lesson-header-grid has-artwork">
          <div>
            <span class="catalog-kicker">AI-POWERED ENGINEERING GLOSSARY · TỪ ĐIỂN KỸ THUẬT THÔNG MINH</span>
            <h1 class="lesson-title">Từ điển Thuật ngữ Kỹ thuật &amp; Trợ lý Giải thích AI (${totalCount}+ Khái niệm)</h1>
            <p class="lesson-lead" style="margin-bottom:0;">Bấm vào bất kỳ thẻ thuật ngữ nào bên dưới — hoặc nhập bất kỳ thuật ngữ, công nghệ, framework nào vào ô AI — để mở Popup chuẩn Anthropic ở giữa màn hình với phân tích chuyên sâu từ định nghĩa dễ hiểu đến ví dụ thực tế (tự động lưu vào bộ nhớ đệm TTL Cache).</p>
          </div>
          <div class="lesson-hero-art" aria-hidden="true">
            ${renderBadgeSealHtml("ObjectBookApple", `${totalCount} Thuật ngữ · AI Cache`)}
          </div>
        </div>
      </header>
      <div class="glossary-ai-ask-bar">
        <div class="glossary-ai-ask-label">
          <span>✦ Giải thích bất kỳ Thuật ngữ / Framework nào bằng Gemini AI:</span>
        </div>
        <div class="glossary-ai-ask-form">
          <input type="text" class="glossary-ai-ask-input" id="glossaryCustomAskInput" placeholder="Nhập bất kỳ từ khóa, công nghệ, framework (VD: Apache Iceberg, vLLM, Raft, Zero-Copy, LangGraph...)" onkeydown="if(event.key==='Enter'){event.preventDefault();askAiFromDictionaryBar();}" />
          <button type="button" class="ui-btn" style="background:var(--cds-clay);color:#fff;border-color:var(--cds-clay);font-weight:500;" onclick="askAiFromDictionaryBar()">Giải thích bằng AI ✦</button>
        </div>
      </div>
      <div class="glossary-dict-controls">
        <input type="search" class="glossary-dict-search" placeholder="Lọc nhanh 74 thuật ngữ nền tảng hoặc gõ từ mới để hỏi AI..." value="${escapeHtml(activeGlossaryQuery)}" oninput="filterGlossaryDictionary(null, this.value)" aria-label="Tìm kiếm trong từ điển thuật ngữ" />
        <div class="glossary-filter-pills">${filterBtns}</div>
      </div>
      <div class="glossary-dict-grid" id="glossaryDictGrid">
        ${renderGlossaryCardsList()}
      </div>
    `;
  }

  function openGlossaryView(pushHistory = true) {
    syncStateVars("GLOSSARY", 1, null);
    document.body.classList.add("catalog-mode");
    document.body.classList.remove("mobile-rail-open");
    renderSyllabus();
    renderMain(false);
    if (pushHistory && !isHandlingRouteEvent) {
      history.pushState({ topic: "GLOSSARY", stage: 1, section: null }, "", "#/glossary");
    }
  }

  function renderLinuxTopic() { return renderTopic("F01"); }
  function renderDatabaseTopic() { return renderTopic("F03"); }
  function renderContainerTopic() { return renderTopic("F06"); }
  function renderStorageTopic() { return renderTopic("D02"); }

  function renderPendingTopic(item, groupTitle) {
    const tocRows = (item.slideToc || []).map((section, idx) => `
      <tr>
        <td style="width:90px;color:var(--muted);">Mục 0${idx + 1}</td>
        <td><strong>${escapeHtml(section)}</strong></td>
      </tr>
    `).join("");

    const slideAction = item.slide
      ? `<a class="cds-swatch-pill" href="course-slides/${escapeHtml(item.slide)}" target="_blank" rel="noopener">Slide gốc: ${escapeHtml(item.slide)} (${item.pages} trang) ↗</a>`
      : "";

    const { group } = findTopicContext(item.code);
    const tVis = TRACK_VISUAL_DEFAULTS[(group && group.id) || "track-1"] || TRACK_VISUAL_DEFAULTS["track-1"];

    return `
      <header class="lesson-header ${tVis.swatchClass}">
        <div class="lesson-hero-dots" aria-hidden="true"></div>
        <div class="lesson-header-grid has-artwork">
          <div class="lesson-header-copy">
            <div class="lesson-meta">
              <span class="cds-swatch-pill">${escapeHtml(groupTitle)} · ${escapeHtml(item.code)}</span>
              ${slideAction}
            </div>
            <h1 class="lesson-title">${escapeHtml(item.title)}</h1>
            <p class="lesson-lead" style="margin-bottom:0;"><strong>Học gì:</strong> ${escapeHtml(item.modules || "")} · <strong>Lab:</strong> ${escapeHtml(item.lab || "")}</p>
          </div>
          <div class="lesson-hero-art" aria-hidden="true">
            ${renderBadgeSealHtml(tVis.pictogram, `${item.code} · Đề cương`)}
          </div>
        </div>
      </header>
      <div class="prose">
        <h2>Mục lục học phần</h2>
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

        <h2>Thông số đề cương</h2>
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
        <p>Học phần này đang ở trạng thái đề cương. Xem các học phần đã xuất bản đầy đủ tại <a href="#/F01/1" onclick="selectTopic('F01');return false;">F01 · Linux Fundamentals</a>, <a href="#/F03/1" onclick="selectTopic('F03');return false;">F03 · Database Fundamentals</a>, <a href="#/F06/1" onclick="selectTopic('F06');return false;">F06 · Containerization &amp; Orchestration</a>, hoặc <a href="#/D02/1" onclick="selectTopic('D02');return false;">D02 · Storage Layer</a>.</p>
      </div>
    `;
  }

  /* ==========================================================================
     TOPBAR CONTEXT PILL & UNIFIED SIDEBAR RAILS (LEFT SYLLABUS & RIGHT TOC)
     ========================================================================== */
  function updateTopbarBreadcrumb() {
    const pill = document.getElementById("topbarContextPill");
    if (!pill) return;

    if (activeTopic === "CATALOG" || activeTopic === "GLOSSARY") {
      pill.style.display = "none";
      pill.innerHTML = "";
      return;
    }

    const { item } = findTopicContext(activeTopic);
    const topicStages = getTopicStages(activeTopic);
    pill.style.display = "inline-flex";
    if (topicStages.length > 0) {
      const padNum = n => String(n).padStart(2, "0");
      pill.innerHTML = `<strong>${escapeHtml(item.code)}</strong><span>${escapeHtml(item.title)} · Chặng ${padNum(activeStorageStage)}/${padNum(topicStages.length)}</span>`;
    } else {
      pill.innerHTML = `<strong>${escapeHtml(item.code)}</strong><span>${escapeHtml(item.title)}</span>`;
    }
  }

  function renderSyllabus() {
    const rail = document.getElementById("syllabusRail");
    if (!rail) return;

    const padNum = n => String(n).padStart(2, "0");
    const tracksHtml = SYLLABUS_GROUPS.map(group => {
      const isExpanded = expandedTracks.has(group.id);
      const itemsHtml = group.items.map(item => {
        const isActive = item.code === activeTopic;
        const stages = getTopicStages(item.code);
        let nestedStagesHtml = "";
        if (isActive && stages.length > 0) {
          nestedStagesHtml = `
            <div class="rail-stage-sublist" role="group" aria-label="Các chặng của ${escapeHtml(item.code)}">
              ${stages.map(st => `
                <button type="button" class="rail-stage-btn ${st.id === activeStorageStage ? 'active' : ''}" onclick="selectStorageStage(${st.id})">
                  <span class="rail-stage-idx">${padNum(st.id)}</span>
                  <span>${escapeHtml(st.shortTitle || st.title)}</span>
                </button>
              `).join("")}
            </div>
          `;
        }
        return `
          <div>
            <button type="button" class="rail-item" ${isActive ? 'aria-current="page"' : ''} onclick="selectTopic('${item.code}')" title="${escapeHtml(item.code)} · ${escapeHtml(item.title)}">
              <span class="rail-code">${escapeHtml(item.code)}</span>
              <span class="rail-item-title">${escapeHtml(item.title)}</span>
              ${item.hasContent ? `<span class="rail-item-dot" title="Đã xuất bản bài học chi tiết"></span>` : `<span></span>`}
            </button>
            ${nestedStagesHtml}
          </div>
        `;
      }).join("");

      return `
        <section class="track-group" id="card-${group.id}" data-expanded="${isExpanded ? 'true' : 'false'}">
          <button type="button" class="track-trigger" aria-expanded="${isExpanded ? 'true' : 'false'}" aria-controls="panel-${group.id}" onclick="toggleTrack('${group.id}')">
            <span>${escapeHtml(group.shortTitle)}</span>
            <span class="cds-icon track-indicator" id="ind-${group.id}" aria-hidden="true">&#xE027;</span>
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
      <div class="rail-nav-shortcuts">
        <button type="button" class="rail-shortcut-btn ${activeTopic === 'CATALOG' ? 'active' : ''}" onclick="openCatalogView()">
          <span>Danh mục khóa học</span>
          <span class="rail-shortcut-badge">26 học phần</span>
        </button>
        <button type="button" class="rail-shortcut-btn ${activeTopic === 'GLOSSARY' ? 'active' : ''}" onclick="openGlossaryView()">
          <span>Từ điển kỹ thuật AI</span>
          <span class="rail-shortcut-badge">74 thuật ngữ</span>
        </button>
      </div>

      <div class="rail-section-heading"><span>Lộ trình 4 Tracks</span><span>26</span></div>
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
    const btn = card ? card.querySelector(".track-trigger") : null;
    const isExp = expandedTracks.has(trackId);
    if (card) card.dataset.expanded = isExp ? "true" : "false";
    if (btn) btn.setAttribute("aria-expanded", isExp ? "true" : "false");
    if (panel) {
      if (isExp) panel.removeAttribute("inert");
      else panel.setAttribute("inert", "");
    }
  }

  let isHandlingRouteEvent = false;

  function jumpToStation(stationId, replaceHistory = true) {
    syncStateVars(activeTopic, activeStorageStage, stationId);
    document.body.classList.remove("mobile-rail-open");
    const target = document.getElementById(stationId);
    if (target) {
      target.scrollIntoView({ behavior: "smooth", block: "start" });
      target.focus({ preventScroll: true });
    }
    highlightActiveStation(stationId);
    if (replaceHistory && !isHandlingRouteEvent) {
      const nextHash = formatRouteHash(activeTopic, activeStorageStage, stationId);
      if (window.location.hash !== nextHash) {
        history.replaceState({ topic: activeTopic, stage: activeStorageStage, section: stationId }, "", nextHash);
      }
    }
  }

  function renderPageToc() {
    const panel = document.getElementById("pageTocPanel");
    if (!panel) return;
    if (activeTopic === "CATALOG" || activeTopic === "GLOSSARY") {
      panel.innerHTML = "";
      return;
    }
    const activeStations = getTopicStations(activeTopic, activeStorageStage);
    const stages = getTopicStages(activeTopic);
    const { item } = findTopicContext(activeTopic);
    const padNum = n => String(n).padStart(2, "0");

    let metaBoxHtml = "";
    if (stages && stages.length > 0) {
      const curStg = stages.find(s => s.id === activeStorageStage) || stages[0];
      const curClean = curStg.shortTitle || curStg.title.replace(/^Chặng \d+:\s*/, "");
      metaBoxHtml = `
        <div class="page-toc-course-meta">
          <span class="page-toc-course-kicker">${escapeHtml(item.code)} · CHẶNG ${padNum(curStg.id)} / ${padNum(stages.length)}</span>
          <span class="page-toc-course-stage">${escapeHtml(curClean)}</span>
        </div>
      `;
    }

    if (!activeStations.length) {
      panel.innerHTML = `
        ${metaBoxHtml}
        <div class="page-toc-header"><span>Trên trang này</span></div>
        <p style="color:var(--muted);font-size:12px;padding:0 8px;">Đề cương học phần ${escapeHtml(activeTopic)}.</p>
      `;
      return;
    }
    panel.innerHTML = `
      ${metaBoxHtml}
      <div class="page-toc-header">
        <span>Trên trang này</span>
        <span id="tocProgressPct">0%</span>
      </div>
      <div class="page-toc-progress" aria-hidden="true">
        <div class="page-toc-progress-fill" id="tocProgressBarFill"></div>
      </div>
      <ul class="page-toc-list" id="pageTocList">
        ${activeStations.map(st => {
          return `
            <li>
              <a href="#${st.id}" class="page-toc-link" data-station-id="${st.id}" ${st.id === activeStationId ? 'aria-current="location"' : ''} onclick="jumpToStation('${st.id}');return false;">
                <span>${escapeHtml(st.title)}</span>
              </a>
            </li>
          `;
        }).join("")}
      </ul>
    `;
  }

  function highlightActiveStation(stationId) {
    activeStationId = stationId;
    document.querySelectorAll("#pageTocList .page-toc-link").forEach(a => {
      if (a.getAttribute("data-station-id") === stationId) {
        a.setAttribute("aria-current", "location");
      } else {
        a.removeAttribute("aria-current");
      }
    });
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
     INTERACTIVE GLOSSARY SCANNER & CENTERED ANTHROPIC-STYLE AI MODAL
     ========================================================================== */
  const GLOSSARY_DB = (HUB_DATA && HUB_DATA.glossary && HUB_DATA.glossary.entries) ? HUB_DATA.glossary.entries : {};
  const GLOSSARY_LOOKUP = (HUB_DATA && HUB_DATA.glossary && HUB_DATA.glossary.lookup) ? HUB_DATA.glossary.lookup : {};
  let activeGlossaryAnchor = null;
  let activeGlossaryTermId = null;
  let activeCustomTermTitle = "";
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
    let currentStationId = null;
    const stationSeen = new Map();
    const stationCounts = new Map();
    const blockCounts = new WeakMap();
    const maxTermsPerStation = 5;

    const nodes = container.querySelectorAll(
      ".lesson-section[id], h2[id], .prose strong, .prose code, .callout strong, .callout code, .data-table td strong, .data-table td code, .clean-table td strong, .clean-table td code"
    );

    nodes.forEach((el) => {
      if (el.matches(".lesson-section[id], h2[id]")) {
        currentStationId = el.id || currentStationId;
        if (currentStationId && !stationSeen.has(currentStationId)) {
          stationSeen.set(currentStationId, new Set());
          stationCounts.set(currentStationId, 0);
        }
        return;
      }
      if (!currentStationId) return;

      const countInStation = stationCounts.get(currentStationId) || 0;
      if (countInStation >= maxTermsPerStation) return;

      if (el.closest("pre, .ascii-diagram, .visual-header, .visual-card, .spine-overview-card, .stage-pills-bar, .lesson-pager, .lesson-lead, .hero-card, a, button, h1, h2, h3, h4, th")) {
        return;
      }
      if (el.querySelector(".glossary-term")) return;
      const text = (el.textContent || "").trim();
      if (text.length < 2 || text.length > 44) return;
      const termId = resolveGlossaryTermId(text);
      if (!termId || !GLOSSARY_DB[termId]) return;

      const seenSet = stationSeen.get(currentStationId);
      if (seenSet.has(termId)) return;

      const blockEl = el.closest("p, li, td, .callout-body, .callout") || el.parentElement;
      const blockUsed = blockCounts.get(blockEl) || 0;
      if (blockUsed >= 1) return;

      seenSet.add(termId);
      stationCounts.set(currentStationId, countInStation + 1);
      blockCounts.set(blockEl, blockUsed + 1);

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
    // Centered modal uses CSS top: 50% !important; left: 50% !important; transform: translate(-50%, -50%)
  }

  function renderGlossaryPopoverContent(termId, rawText = "") {
    const entry = GLOSSARY_DB[termId];
    if (!entry) return false;
    const canonicalTitle = entry.term || entry.name || termId;
    activeCustomTermTitle = canonicalTitle;
    const catEl = document.getElementById("glossaryPopCategory");
    if (catEl) {
      const cleanRaw = (rawText || "").trim();
      const showRaw = cleanRaw && cleanRaw.toLowerCase() !== canonicalTitle.toLowerCase() && cleanRaw.length <= 36;
      catEl.textContent = showRaw ? `${entry.category || "Thuật ngữ"} · ${cleanRaw}` : (entry.category || "Thuật ngữ Kỹ thuật");
    }
    document.getElementById("glossaryPopTitle").textContent = canonicalTitle;
    document.getElementById("glossaryPopIntuition").textContent = entry.short || entry.intuition || "";

    const ex = entry.example || {};
    const codeEl = document.getElementById("glossaryPopCode");
    if (codeEl) {
      codeEl.textContent = ex.code || "";
      codeEl.style.display = ex.code ? "block" : "none";
    }

    const linkEl = document.getElementById("glossaryPopLink");
    if (linkEl) {
      linkEl.setAttribute("href", entry.station_link || "#/F01/1");
      linkEl.style.display = "inline";
    }

    populateAiGlossaryModalSections(canonicalTitle, entry.category || "Systems & Data Engineering", entry.short || "", ex.code || "", false);
    return true;
  }

  function openGlossaryPopover(anchorEl, termId, pin = true) {
    if (!anchorEl || !termId || !GLOSSARY_DB[termId]) return;
    clearTimeout(glossaryOpenTimer);
    clearTimeout(glossaryCloseTimer);

    if (activeGlossaryAnchor && activeGlossaryAnchor !== anchorEl) {
      activeGlossaryAnchor.classList.remove("glossary-active", "glossary-pinned");
    }
    activeGlossaryAnchor = anchorEl;
    activeGlossaryTermId = termId;
    glossaryPinned = true;

    anchorEl.classList.add("glossary-active", "glossary-pinned");

    const rawText = anchorEl.getAttribute("data-term-raw") || anchorEl.textContent || "";
    renderGlossaryPopoverContent(termId, rawText);

    const pop = document.getElementById("glossaryPopover");
    const backdrop = document.getElementById("glossaryModalBackdrop");
    if (backdrop) backdrop.classList.add("open");
    pop.classList.add("open", "pinned");
    pop.setAttribute("aria-hidden", "false");
  }

  function openGlossaryPopoverFromDict(cardEl, termId, ev) {
    if (ev) ev.stopPropagation();
    openGlossaryPopover(cardEl, termId, true);
  }

  function openCustomAiTermModal(customTerm) {
    const cleanTerm = String(customTerm || "").trim();
    if (!cleanTerm) return;
    const matchedId = resolveGlossaryTermId(cleanTerm);
    if (matchedId && GLOSSARY_DB[matchedId]) {
      const dummyAnchor = document.getElementById("glossaryCustomAskInput") || document.body;
      openGlossaryPopover(dummyAnchor, matchedId, true);
      return;
    }
    clearTimeout(glossaryOpenTimer);
    clearTimeout(glossaryCloseTimer);
    activeGlossaryAnchor = document.getElementById("glossaryCustomAskInput") || null;
    activeGlossaryTermId = "custom:" + normalizeGlossaryKey(cleanTerm);
    activeCustomTermTitle = cleanTerm;
    glossaryPinned = true;

    const catEl = document.getElementById("glossaryPopCategory");
    if (catEl) catEl.textContent = "AI KNOWLEDGE · THUẬT NGỮ / FRAMEWORK MỞ RỘNG";
    document.getElementById("glossaryPopTitle").textContent = cleanTerm;
    document.getElementById("glossaryPopIntuition").textContent = `Đang tổng hợp kiến thức cốt lõi và ví dụ thực tế cho "${cleanTerm}" bằng Gemini AI...`;
    const codeEl = document.getElementById("glossaryPopCode");
    if (codeEl) {
      codeEl.textContent = "";
      codeEl.style.display = "none";
    }
    const linkEl = document.getElementById("glossaryPopLink");
    if (linkEl) linkEl.style.display = "none";

    const pop = document.getElementById("glossaryPopover");
    const backdrop = document.getElementById("glossaryModalBackdrop");
    if (backdrop) backdrop.classList.add("open");
    pop.classList.add("open", "pinned");
    pop.setAttribute("aria-hidden", "false");

    populateAiGlossaryModalSections(cleanTerm, "Data, AI & Distributed Systems", "", "", false);
  }

  function askAiFromDictionaryBar() {
    const inp = document.getElementById("glossaryCustomAskInput");
    if (!inp || !inp.value.trim()) return;
    openCustomAiTermModal(inp.value.trim());
  }

  function askAiCustomTermFromModal() {
    const inp = document.getElementById("glossaryAiCustomInput");
    if (!inp || !inp.value.trim()) return;
    const val = inp.value.trim();
    inp.value = "";
    openCustomAiTermModal(val);
  }

  function regenerateCurrentGlossaryAi() {
    if (!activeCustomTermTitle) return;
    const entry = activeGlossaryTermId && GLOSSARY_DB[activeGlossaryTermId] ? GLOSSARY_DB[activeGlossaryTermId] : null;
    populateAiGlossaryModalSections(
      activeCustomTermTitle,
      entry ? (entry.category || "Systems Engineering") : "Data, AI & Distributed Systems",
      entry ? (entry.short || "") : "",
      (entry && entry.example && entry.example.code) ? entry.example.code : "",
      true
    );
  }

  function closeGlossaryPopover(force = false, restoreFocus = false) {
    if (glossaryPinned && !force) return;
    clearTimeout(glossaryOpenTimer);
    clearTimeout(glossaryCloseTimer);
    const pop = document.getElementById("glossaryPopover");
    const backdrop = document.getElementById("glossaryModalBackdrop");
    if (backdrop) backdrop.classList.remove("open");
    if (pop) {
      pop.classList.remove("open", "pinned");
      pop.setAttribute("aria-hidden", "true");
    }
    const anchorToRestore = activeGlossaryAnchor;
    if (activeGlossaryAnchor && activeGlossaryAnchor.classList) {
      activeGlossaryAnchor.classList.remove("glossary-active", "glossary-pinned");
    }
    activeGlossaryAnchor = null;
    activeGlossaryTermId = null;
    glossaryPinned = false;
    if (restoreFocus && anchorToRestore && typeof anchorToRestore.focus === "function") {
      anchorToRestore.focus();
    }
  }

  function initGlossarySystem() {
    const container = document.getElementById("articleContainer");
    const pop = document.getElementById("glossaryPopover");
    const closeBtn = document.getElementById("glossaryPopCloseBtn");
    if (!container || !pop) return;

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

    pop.addEventListener("click", (e) => {
      const link = e.target.closest(".glossary-pop-link");
      if (link) {
        closeGlossaryPopover(true);
        return;
      }
      e.stopPropagation();
    });

    if (closeBtn) {
      closeBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        closeGlossaryPopover(true, true);
      });
    }

    document.addEventListener("click", (e) => {
      if (!pop.classList.contains("open")) return;
      if (pop.contains(e.target)) return;
      if (e.target.closest && e.target.closest(".glossary-term, .glossary-dict-card")) return;
      closeGlossaryPopover(true);
    });
  }

  /* ==========================================================================
     MAIN CONTROLLER & NAVIGATION
     ========================================================================== */
  function renderMain(preserveScroll = false) {
    closeGlossaryPopover(true);
    window.__diagrams = {};
    const container = document.getElementById("articleContainer");
    const isFullWidthMode = (activeTopic === "CATALOG" || activeTopic === "GLOSSARY");
    document.body.classList.toggle("catalog-mode", isFullWidthMode);

    const catBtn = document.getElementById("catalogTopBtn");
    if (catBtn) catBtn.classList.toggle("active", activeTopic === "CATALOG");
    const glsBtn = document.getElementById("glossaryNavBtn");
    if (glsBtn) glsBtn.classList.toggle("active", activeTopic === "GLOSSARY");

    if (activeTopic === "CATALOG") {
      container.innerHTML = renderCatalogView();
    } else if (activeTopic === "GLOSSARY") {
      container.innerHTML = renderGlossaryView();
    } else if (TOPIC_CONFIG[activeTopic]) {
      container.innerHTML = renderTopic(activeTopic);
      if (activeTopic === "F06" && activeStorageStage === 1) {
        renderInfra2DSlide();
      }
      if (activeTopic === "D01" && activeStorageStage === 1) {
        renderIngestion2DSlide();
      }
      bindGlossaryTerms(container);
    } else {
      const { group, item } = findTopicContext(activeTopic);
      container.innerHTML = renderPendingTopic(item, group.title);
    }
    updateTopbarBreadcrumb();
    renderPageToc();
    if (!preserveScroll) {
      window.scrollTo(0, 0);
    }
    setupScrollSpy();
    updateReadingProgress();
    if (typeof currentAppLang !== "undefined" && currentAppLang === "en") {
      translateActiveViewToEnglish();
    }
  }

  function selectTopic(code, stageId = null, sectionId = null, pushHistory = true) {
    if (code === "CATALOG") {
      openCatalogView(pushHistory);
      return;
    }
    if (code === "GLOSSARY") {
      openGlossaryView(pushHistory);
      return;
    }
    const { group } = findTopicContext(code);
    expandedTracks.add(group.id);
    const topicChanged = (activeTopic !== code);
    let nextStage = activeStorageStage;
    if (stageId !== null && stageId !== undefined) {
      nextStage = Number(stageId) || 1;
    } else if (topicChanged) {
      nextStage = 1;
    }
    const stages = getTopicStages(code);
    if (stages.length > 0 && !stages.some(s => s.id === nextStage)) {
      nextStage = stages[0].id;
    }
    const stations = getTopicStations(code, nextStage);
    let nextSection = activeStationId;
    if (sectionId !== null && sectionId !== undefined) {
      nextSection = sectionId;
    } else if (stations.length > 0) {
      nextSection = stations[0].id;
    }
    syncStateVars(code, nextStage, nextSection);
    document.body.classList.remove("mobile-rail-open");
    renderSyllabus();
    renderMain(Boolean(sectionId));
    if (pushHistory && !isHandlingRouteEvent) {
      const nextHash = formatRouteHash(activeTopic, activeStorageStage, sectionId || null);
      if (window.location.hash !== nextHash) {
        history.pushState({ topic: activeTopic, stage: activeStorageStage, section: sectionId || null }, "", nextHash);
      }
    }
    if (sectionId) {
      setTimeout(() => jumpToStation(sectionId, false), 30);
    }
  }

  function selectStorageStage(stageId, pushHistory = true) {
    const nextStage = Number(stageId) || 1;
    const stations = getTopicStations(activeTopic, nextStage);
    const nextSection = stations.length > 0 ? stations[0].id : activeStationId;
    syncStateVars(activeTopic, nextStage, nextSection);
    document.body.classList.remove("mobile-rail-open");
    renderSyllabus();
    renderMain();
    if (pushHistory && !isHandlingRouteEvent) {
      const nextHash = formatRouteHash(activeTopic, activeStorageStage, null);
      if (window.location.hash !== nextHash) {
        history.pushState({ topic: activeTopic, stage: activeStorageStage, section: null }, "", nextHash);
      }
    }
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
    for (const st of DB_CHANG1_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "I. Engineering Foundation / F03 · Database Fundamentals / Chặng 1",
        topic: "F03",
        stage: 1,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} database rdbms sql pk fk primary key foreign key cardinality constraints not null unique check normalization unf 1nf 2nf 3nf bcnf denormalization hd01 lan`)
      });
    }
    for (const st of DB_CHANG2_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "I. Engineering Foundation / F03 · Database Fundamentals / Chặng 2",
        topic: "F03",
        stage: 2,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} postgresql storage engine memory architecture shared_buffers work_mem postgresql.conf slotted page 8kb lsn line pointer tuple wal buffer wal writer checkpointer dirty page`)
      });
    }
    for (const st of DB_CHANG3_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "I. Engineering Foundation / F03 · Database Fundamentals / Chặng 3",
        topic: "F03",
        stage: 3,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} acid lock manager mvcc snapshot isolation autovacuum b-tree lsm-tree latch crabbing index query optimizer explain analyze psql pgadmin pg_stat_statements`)
      });
    }
    for (const st of DB_CHANG4_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "I. Engineering Foundation / F03 · Database Fundamentals / Chặng 4",
        topic: "F03",
        stage: 4,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} scale-up scale-out partitioning sharding replication ha failover pgd witness node raft paxos barman tidb ydb nosql key-value document bson column-family graph cap base lww vector clocks`)
      });
    }
    for (const stg of DB_STAGES) {
      entries.push({
        kind: "Lộ trình Chặng",
        title: `F03 · ${stg.title}`,
        sub: "I. Engineering Foundation / Database Fundamentals",
        topic: "F03",
        stage: stg.id,
        section: null,
        keywords: normalizeSearch(`F03 database postgresql sql nosql ${stg.title}`)
      });
    }
    for (const st of CONTAINER_CHANG1_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "I. Engineering Foundation / F06 · Containerization & Orchestration / Chặng 1",
        topic: "F06",
        stage: 1,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} bare metal hypervisor vm vps cloud vm shared hosting noisy neighbor spof vm tax guest os container os-level virtualization serverless scale to zero order-api app.py tiem banh cua minh`)
      });
    }
    for (const st of CONTAINER_CHANG2_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "I. Engineering Foundation / F06 · Containerization & Orchestration / Chặng 2",
        topic: "F06",
        stage: 2,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} linux namespaces pid net mnt ipc uts user host pid 10423 virtual pid 1 control groups cgroups v2 cpu.max memory.max blkio oom killer overlayfs lowerdir upperdir merged copy-on-write clone unshare pivot_root linux capabilities seccomp`)
      });
    }
    for (const st of CONTAINER_CHANG3_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "I. Engineering Foundation / F06 · Containerization & Orchestration / Chặng 3",
        topic: "F06",
        stage: 3,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} build ship run dockerfile multi-stage build oci image container registry persistent volumes var lib docker volumes docker cli dockerd containerd containerd-shim runc libcontainer podman daemonless rootless cri-o`)
      });
    }
    for (const st of CONTAINER_CHANG4_STATIONS) {
      entries.push({
        kind: "Trạm kiến thức",
        title: st.fullTitle,
        sub: "I. Engineering Foundation / F06 · Containerization & Orchestration / Chặng 4",
        topic: "F06",
        stage: 4,
        section: st.id,
        keywords: normalizeSearch(`${st.code} ${st.fullTitle} kubernetes k8s orchestration cri container runtime interface declarative yaml desired state control plane kube-apiserver etcd kube-scheduler kube-controller-manager worker node kubelet kube-proxy pod replicaset deployment service clusterip ipvs ingress liveness readiness startup probes`)
      });
    }
    for (const stg of CONTAINER_STAGES) {
      entries.push({
        kind: "Lộ trình Chặng",
        title: `F06 · ${stg.title}`,
        sub: "I. Engineering Foundation / Containerization & Orchestration",
        topic: "F06",
        stage: stg.id,
        section: null,
        keywords: normalizeSearch(`F06 docker container kubernetes k8s podman containerd runc ${stg.title}`)
      });
    }
    const d01StationLists = [
      [1, INGESTION_CHANG1_STATIONS, "ingestion source system gigo governance structured semi-structured unstructured push pull poll oltp olap etlt row column hybrid parquet logs order 8888"],
      [2, INGESTION_CHANG2_STATIONS, "cdc change data capture full table dump timestamp polling watermark soft delete is_deleted trigger shadow table write amplification log-based wal pgoutput binlog lsn"],
      [3, INGESTION_CHANG3_STATIONS, "apache kafka event streaming broker topic partition offset consumer lag zookeeper kraft consensus kafka connect mirrormaker 2 schema registry zero-copy sendfile page cache"],
      [4, INGESTION_CHANG4_STATIONS, "kafka producer murmur2 sticky partitioner recordaccumulator batch.size linger.ms consumer group rebalance cooperativestickyassignor replication leader follower isr high watermark acks=0 acks=1 acks=all idempotence eos log compaction tombstone"],
      [5, INGESTION_CHANG5_STATIONS, "debezium snapshot wal streaming before after op envelope kafka connect sink smt replication slot wal bloat heartbeat.interval.ms max_slot_wal_keep_size poison pill dead letter queue dlq hot partition dual-write transactional outbox"]
    ];
    for (const [stgId, stList, kwExtra] of d01StationLists) {
      for (const st of stList) {
        entries.push({
          kind: "Trạm kiến thức",
          title: st.fullTitle,
          sub: `II. Data Engineering / D01 · Ingestion Layer / Chặng ${stgId}`,
          topic: "D01",
          stage: stgId,
          section: st.id,
          keywords: normalizeSearch(`${st.code} ${st.fullTitle} ${kwExtra}`)
        });
      }
    }
    for (const stg of INGESTION_STAGES) {
      entries.push({
        kind: "Chặng bài đọc",
        title: `D01 · ${stg.title}`,
        sub: "II. Data Engineering / Ingestion Layer",
        topic: "D01",
        stage: stg.id,
        section: null,
        keywords: normalizeSearch(`D01 ingestion kafka debezium cdc ${stg.title}`)
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
    for (const gEntry of Object.values(GLOSSARY_DB)) {
      const parsedLink = parseRouteHash(gEntry.station_link || "#/F01/1");
      entries.push({
        kind: "Thuật ngữ",
        title: gEntry.name,
        sub: `${gEntry.category || "Từ điển"} — ${gEntry.short || ""}`,
        topic: parsedLink.topic || "GLOSSARY",
        stage: parsedLink.stage || 1,
        section: parsedLink.section || null,
        keywords: normalizeSearch(`${gEntry.name} ${gEntry.category || ""} ${gEntry.short || ""} ${(gEntry.aliases || []).join(" ")}`)
      });
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

  /* ==========================================================================
     PERSISTENT AI TTL CACHE (Memory + localStorage + IndexedDB, 30-Day TTL)
     ========================================================================== */
  const FSDS_TTL_CACHE = (() => {
    const PREFIX = "fsds_ttl_v2_";
    const DEFAULT_TTL_MS = 30 * 24 * 60 * 60 * 1000;
    const mem = new Map();
    let dbPromise = null;
    let stats = { hits: 0, misses: 0 };

    function openDb() {
      if (dbPromise) return dbPromise;
      if (typeof indexedDB === "undefined") return Promise.resolve(null);
      dbPromise = new Promise((resolve) => {
        try {
          const req = indexedDB.open("fsds_ai_ttl_db", 1);
          req.onupgradeneeded = () => {
            const db = req.result;
            if (!db.objectStoreNames.contains("ttl_store")) {
              db.createObjectStore("ttl_store");
            }
          };
          req.onsuccess = () => resolve(req.result);
          req.onerror = () => resolve(null);
        } catch (_e) {
          resolve(null);
        }
      });
      return dbPromise;
    }

    function hashKey(raw) {
      let h1 = 0xdeadbeef ^ raw.length;
      let h2 = 0x41c6ce57 ^ raw.length;
      for (let i = 0, ch; i < raw.length; i++) {
        ch = raw.charCodeAt(i);
        h1 = Math.imul(h1 ^ ch, 2654435761);
        h2 = Math.imul(h2 ^ ch, 1597334677);
      }
      h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
      h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
      return PREFIX + (4294967296 * (2097151 & h2) + (h1 >>> 0)).toString(36);
    }

    function getSync(rawKey) {
      const k = hashKey(rawKey);
      const now = Date.now();
      if (mem.has(k)) {
        const item = mem.get(k);
        if (item && item.exp > now) {
          stats.hits++;
          return item.val;
        }
        mem.delete(k);
      }
      try {
        const raw = localStorage.getItem(k);
        if (raw) {
          const parsed = JSON.parse(raw);
          if (parsed && parsed.exp > now) {
            mem.set(k, parsed);
            stats.hits++;
            return parsed.val;
          }
          localStorage.removeItem(k);
        }
      } catch (_e) {}
      stats.misses++;
      return null;
    }

    async function getAsync(rawKey) {
      const syncVal = getSync(rawKey);
      if (syncVal !== null) return syncVal;
      const k = hashKey(rawKey);
      const now = Date.now();
      const db = await openDb();
      if (!db) return null;
      return new Promise((resolve) => {
        try {
          const tx = db.transaction("ttl_store", "readonly");
          const req = tx.objectStore("ttl_store").get(k);
          req.onsuccess = () => {
            const rec = req.result;
            if (rec && rec.exp > now) {
              mem.set(k, rec);
              try { localStorage.setItem(k, JSON.stringify(rec)); } catch (_e) {}
              stats.hits++;
              resolve(rec.val);
            } else {
              resolve(null);
            }
          };
          req.onerror = () => resolve(null);
        } catch (_e) {
          resolve(null);
        }
      });
    }

    function set(rawKey, val, ttlMs = DEFAULT_TTL_MS) {
      const k = hashKey(rawKey);
      const rec = { val, exp: Date.now() + ttlMs, ts: Date.now() };
      mem.set(k, rec);
      try {
        localStorage.setItem(k, JSON.stringify(rec));
      } catch (_e) {}
      openDb().then((db) => {
        if (!db) return;
        try {
          const tx = db.transaction("ttl_store", "readwrite");
          tx.objectStore("ttl_store").put(rec, k);
        } catch (_e) {}
      });
    }

    return { getSync, getAsync, set, stats, hashKey };
  })();
  window.FSDS_TTL_CACHE = FSDS_TTL_CACHE;

  /* ==========================================================================
     GOOGLE AI STUDIO CREDENTIAL VAULT & GEMINI 3.5 INTERACTIONS ENGINE
     ========================================================================== */
  function resolveAiCredential() {
    try {
      const custom = localStorage.getItem("fsds-custom-ai-key");
      if (custom && custom.trim()) return custom.trim();
    } catch (_e) {}
    const vault = (HUB_DATA && HUB_DATA.ai_vault) ? HUB_DATA.ai_vault : null;
    if (!vault || !Array.isArray(vault.d) || !Array.isArray(vault.m) || !vault.d.length) return "";
    const bytes = new Uint8Array(vault.d.length);
    for (let i = 0; i < vault.d.length; i++) {
      bytes[i] = (vault.d[i] ^ vault.m[i % vault.m.length]) & 0xff;
    }
    try {
      return new TextDecoder("utf-8").decode(bytes);
    } catch (_e) {
      return String.fromCharCode(...bytes);
    }
  }

  async function callGeminiAI(promptText) {
    const key = resolveAiCredential();
    if (!key) throw new Error("Missing AI credential");
    const vault = (HUB_DATA && HUB_DATA.ai_vault) || {};
    const endpoint = vault.endpoint || "https://generativelanguage.googleapis.com/v1/interactions";
    const model = vault.model || "models/gemini-3.5-flash-lite";

    const resp = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-goog-api-key": key
      },
      body: JSON.stringify({
        model,
        input: promptText,
        store: false,
        generation_config: {
          thinking_level: "minimal"
        }
      })
    });
    if (!resp.ok) {
      throw new Error(`Gemini HTTP ${resp.status}`);
    }
    const data = await resp.json();
    const steps = Array.isArray(data.steps) ? data.steps : [];
    for (let i = steps.length - 1; i >= 0; i--) {
      const st = steps[i];
      if (!st) continue;
      const contentArr = Array.isArray(st.content)
        ? st.content
        : (st.model_output && Array.isArray(st.model_output.content) ? st.model_output.content : []);
      for (const part of contentArr) {
        if (part && typeof part.text === "string" && part.text.trim()) {
          return part.text.trim();
        }
      }
    }
    throw new Error("Empty AI response");
  }

  function renderStructuredAiGlossaryHtml(sections, isEnglish = false) {
    const s1Label = isEnglish ? "1. Core Intuition (First-Principles)" : "1. Bản chất cốt lõi (Định nghĩa dễ hiểu)";
    const s2Label = isEnglish ? "2. Under-the-Hood Mechanics" : "2. Cơ chế hoạt động nội tại";
    const s3Label = isEnglish ? "3. Real-World Production Example" : "3. Ví dụ thực tế & Code minh họa";
    const s4Label = isEnglish ? "4. Production Trade-offs & Pitfalls" : "4. Cạm bẫy & Kinh nghiệm thực chiến";
    return `
      <div class="glossary-ai-sec">
        <span class="glossary-ai-sec-label">${s1Label}</span>
        <div>${escapeHtml(sections.intuition || "")}</div>
      </div>
      <div class="glossary-ai-sec">
        <span class="glossary-ai-sec-label">${s2Label}</span>
        <div>${escapeHtml(sections.mechanics || "")}</div>
      </div>
      <div class="glossary-ai-sec">
        <span class="glossary-ai-sec-label">${s3Label}</span>
        <div>${escapeHtml(sections.example || "")}</div>
        ${sections.code ? `<pre>${escapeHtml(sections.code)}</pre>` : ""}
      </div>
      <div class="glossary-ai-sec">
        <span class="glossary-ai-sec-label">${s4Label}</span>
        <div>${escapeHtml(sections.pitfalls || "")}</div>
      </div>
    `;
  }

  function buildFallbackStructuredGlossary(termTitle, category, shortDesc, codeSnippet, isEnglish = false) {
    if (isEnglish) {
      return {
        intuition: shortDesc || `${termTitle} is a foundational concept in ${category}, designed to guarantee predictable performance, reliability, and clean abstraction boundaries in modern data and AI systems.`,
        mechanics: `At runtime, ${termTitle} operates by isolating state transitions and minimizing unnecessary I/O or lock contention across execution layers.`,
        example: `In a production pipeline handling high-throughput traffic, engineers apply ${termTitle} to prevent bottlenecks and keep latency deterministic.`,
        code: codeSnippet || `# Production check for ${termTitle}\nexplain_system_metric("${termTitle}")`,
        pitfalls: `Avoid applying ${termTitle} blindly without measuring baseline workload characteristics (read/write ratio, payload size, and failure recovery SLA).`
      };
    }
    return {
      intuition: shortDesc || `${termTitle} là khái niệm/công nghệ trọng tâm trong mảng ${category}, giúp giải quyết bài toán hiệu năng, tính nhất quán và khả năng mở rộng của hệ thống thực tế.`,
      mechanics: `Về mặt cơ chế, ${termTitle} kiểm soát trực tiếp luồng dữ liệu/tài nguyên ở tầng hệ thống nhằm giảm thiểu chi phí I/O dư thừa, tránh tranh chấp khóa (lock contention) và đảm bảo tính tất định khi vận hành.`,
      example: `Trong hệ thống Production quy mô lớn (Data Pipeline / Distributed Backend), kỹ sư sử dụng ${termTitle} để xử lý tải cao mà không làm sập nút xử lý hoặc thất thoát dữ liệu.`,
      code: codeSnippet || `# Ví dụ kiểm tra / áp dụng ${termTitle} trong thực tế\n# Chạy lệnh hoặc cấu hình chuẩn Production`,
      pitfalls: `Luôn đo đạc đặc thù tải (tỷ lệ Đọc/Ghi, kích thước bản ghi, ngưỡng SLA) trước khi tinh chỉnh ${termTitle}; tránh lạm dụng theo thói quen gây phức tạp hóa vận hành.`
    };
  }

  async function populateAiGlossaryModalSections(termTitle, category, shortDesc, codeSnippet, forceRefresh = false) {
    const bodyEl = document.getElementById("glossaryPopAiBody");
    const badgeEl = document.getElementById("glossaryPopCacheBadge");
    if (!bodyEl) return;

    const lang = (typeof currentAppLang !== "undefined" && currentAppLang === "en") ? "en" : "vi";
    const cacheKey = `glossary_ai_v2:${lang}:${normalizeGlossaryKey(termTitle)}`;

    if (!forceRefresh) {
      const cached = FSDS_TTL_CACHE.getSync(cacheKey);
      if (cached && typeof cached === "object") {
        if (badgeEl) badgeEl.textContent = "◈ TTL Cache Hit · 0ms";
        if (cached.intuition && document.getElementById("glossaryPopIntuition")) {
          document.getElementById("glossaryPopIntuition").textContent = cached.intuition;
        }
        bodyEl.innerHTML = renderStructuredAiGlossaryHtml(cached, lang === "en");
        return;
      }
    }

    const fallbackObj = buildFallbackStructuredGlossary(termTitle, category, shortDesc, codeSnippet, lang === "en");
    bodyEl.innerHTML = renderStructuredAiGlossaryHtml(fallbackObj, lang === "en");
    if (badgeEl) badgeEl.textContent = "✦ Gemini AI đang phân tích...";

    const prompt = lang === "en"
      ? `You are a Principal Systems & Data/AI Architect at Anthropic Academy. Explain the technical term or framework "${termTitle}" (Category: ${category}).
Return ONLY a valid JSON object with 5 keys (no markdown fences, no extra text, never use backtick characters inside string values):
{
  "intuition": "Clear, vivid first-principles explanation in 2 sentences (with a concrete real-world analogy).",
  "mechanics": "How it works under the hood in 2-3 concise sentences (OS/memory/network/storage mechanics).",
  "example": "A concrete production scenario showing how engineers use it in real life (2 sentences).",
  "code": "A short, realistic 2-4 line CLI command, SQL query, or Python/config snippet illustrating it.",
  "pitfalls": "Key production pitfall or trade-off to watch out for (1-2 sentences)."
}`
      : `Bạn là Kiến trúc sư Hệ thống & Data/AI (Anthropic Academy). Hãy giải thích thuật ngữ hoặc công nghệ/framework "${termTitle}" (Nhóm: ${category}) thật sắc sảo, dễ hiểu cho cả người mới lẫn kỹ sư thực chiến.
Chỉ trả về DUY NHẤT 1 JSON object hợp lệ gồm 5 trường (không bọc markdown code block, tuyệt đối không dùng dấu backtick trong chuỗi văn bản):
{
  "intuition": "Định nghĩa bản chất cốt lõi cực kỳ dễ hiểu kèm 1 ví dụ ẩn dụ đời thực (2-3 câu).",
  "mechanics": "Cơ chế hoạt động nội tại bên dưới hệ thống/bộ nhớ/mạng/đĩa (2-3 câu ngắn gọn).",
  "example": "Tình huống ứng dụng thực tế trong hệ thống Production quy mô lớn (2 câu).",
  "code": "Đoạn code/lệnh CLI/SQL/cấu hình thực tế ngắn gọn (2-4 dòng) minh họa trực tiếp.",
  "pitfalls": "Cạm bẫy thực chiến hoặc đánh đổi (trade-off) quan trọng cần tránh (1-2 câu)."
}`;

    try {
      const rawText = await callGeminiAI(prompt);
      const jsonMatch = rawText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        const cleanObj = {
          intuition: String(parsed.intuition || fallbackObj.intuition).replace(/`/g, "'"),
          mechanics: String(parsed.mechanics || fallbackObj.mechanics).replace(/`/g, "'"),
          example: String(parsed.example || fallbackObj.example).replace(/`/g, "'"),
          code: String(parsed.code || fallbackObj.code).replace(/^```\w*\n?|\n?```$/g, ""),
          pitfalls: String(parsed.pitfalls || fallbackObj.pitfalls).replace(/`/g, "'")
        };
        FSDS_TTL_CACHE.set(cacheKey, cleanObj);
        if (activeCustomTermTitle === termTitle) {
          if (badgeEl) badgeEl.textContent = "✦ Gemini AI · Đã lưu TTL Cache";
          const intEl = document.getElementById("glossaryPopIntuition");
          if (intEl && (!shortDesc || activeGlossaryTermId?.startsWith("custom:"))) {
            intEl.textContent = cleanObj.intuition;
          }
          bodyEl.innerHTML = renderStructuredAiGlossaryHtml(cleanObj, lang === "en");
        }
        return;
      }
    } catch (_err) {
      // Fallback already rendered cleanly; cache fallback for session smoothness
    }
    if (activeCustomTermTitle === termTitle && badgeEl) {
      badgeEl.textContent = "◈ Local Core Cache";
    }
  }

  /* ==========================================================================
     6 ACCENT COLOR THEMES, DARK/LIGHT MODE & MOBILE DEV PREVIEW
     ========================================================================== */
  function toggleAccentPopover(ev) {
    if (ev) ev.stopPropagation();
    const pop = document.getElementById("accentPopover");
    if (pop) pop.classList.toggle("open");
  }

  function applyAccentTheme(accentName) {
    const validAccents = ["clay", "cobalt", "sage", "plum", "ochre", "crimson"];
    const chosen = validAccents.includes(accentName) ? accentName : "clay";
    document.documentElement.setAttribute("data-accent", chosen);
    document.querySelectorAll(".accent-swatch-opt").forEach(btn => {
      btn.classList.toggle("active", btn.getAttribute("data-accent") === chosen);
    });
    const pop = document.getElementById("accentPopover");
    if (pop) pop.classList.remove("open");
    try {
      localStorage.setItem("fsds-accent", chosen);
    } catch (_e) {}
  }

  document.addEventListener("click", (e) => {
    const wrap = document.getElementById("accentPickerWrap");
    const pop = document.getElementById("accentPopover");
    if (pop && pop.classList.contains("open") && wrap && !wrap.contains(e.target)) {
      pop.classList.remove("open");
    }
  });

  function applyTheme(mode) {
    const isLight = (mode === "light");
    document.documentElement.classList.toggle("light", isLight);
    document.documentElement.classList.toggle("dark", !isLight);
    document.documentElement.setAttribute("data-mode", isLight ? "light" : "dark");
    const isEn = (typeof currentAppLang !== "undefined" && currentAppLang === "en");
    document.getElementById("themeToggleLabel").textContent = isEn
      ? (isLight ? "Light" : "Dark")
      : (isLight ? "Sáng" : "Tối");
    const themeIcon = document.getElementById("themeToggleIcon");
    if (themeIcon) {
      themeIcon.textContent = isLight ? "\uE0B0" : "\uE0EE";
    }
    localStorage.setItem("fsds-theme", isLight ? "light" : "dark");
  }

  document.getElementById("themeToggleBtn").addEventListener("click", () => {
    const isLight = document.documentElement.classList.contains("light");
    applyTheme(isLight ? "dark" : "light");
  });

  /* ==========================================================================
     FULL BILINGUAL EN <-> VI AUTO-TRANSLATION ENGINE (GEMINI AI + TTL CACHE)
     ========================================================================== */
  let currentAppLang = localStorage.getItem("fsds-lang") || "vi";
  let activeTranslationToken = 0;

  function applyStaticUiChromeLanguage(lang) {
    const isEn = (lang === "en");
    document.documentElement.setAttribute("lang", isEn ? "en" : "vi");
    const viOpt = document.getElementById("langOptVi");
    const enOpt = document.getElementById("langOptEn");
    if (viOpt) viOpt.classList.toggle("active", !isEn);
    if (enOpt) enOpt.classList.toggle("active", isEn);

    const setTxt = (id, viText, enText) => {
      const el = document.getElementById(id);
      if (el) el.textContent = isEn ? enText : viText;
    };
    setTxt("railToggleLabel", "Mục lục", "Syllabus");
    setTxt("navCoursesLabel", "Khóa học (26)", "Courses (26)");
    setTxt("navGlossaryLabel", "Từ điển AI (74)", "AI Glossary (74)");
    setTxt("searchBtnLabel", "Tìm kiếm...", "Search...");
    setTxt("accentBtnLabel", "Màu", "Accent");
    setTxt("cmdFooterHint", "↑↓ Di chuyển · Enter Chọn · Esc Đóng", "↑↓ Navigate · Enter Select · Esc Close");
    setTxt("cmdFooterStats", "26 Học phần · 19 Chặng · 74 Thuật ngữ Kỹ thuật", "26 Courses · 19 Stages · 74 Technical Terms");
    setTxt("glossaryAiBoxTitle", "✦ Giải thích chuyên sâu & Ví dụ thực tế (Gemini AI)", "✦ Deep-Dive Explanation & Real-World Example (Gemini AI)");
    setTxt("glossaryAiRefreshBtn", "↻ Tạo lại", "↻ Regenerate");

    const cmdInput = document.getElementById("cmdSearchInput");
    if (cmdInput) {
      cmdInput.placeholder = isEn
        ? "Search courses (D02, F03...), stations (MVCC, Slotted Page...) or technical terms..."
        : "Tìm học phần (D02, F03...), trạm (MVCC, Slotted Page...) hoặc thuật ngữ...";
    }
    const isLight = document.documentElement.classList.contains("light");
    setTxt("themeToggleLabel", isLight ? "Sáng" : "Tối", isLight ? "Light" : "Dark");
  }

  async function translateActiveViewToEnglish() {
    if (currentAppLang !== "en") return;
    const myToken = ++activeTranslationToken;
    const rootNodes = [
      document.getElementById("articleContainer"),
      document.getElementById("syllabusRail"),
      document.getElementById("pageTocPanel")
    ].filter(Boolean);

    const selector = [
      "h1", "h2", "h3", "h4",
      ".lesson-lead", ".lesson-stage-subtitle",
      ".stage-pills-label", ".stage-pill-title", ".stage-pill-state",
      ".lesson-objectives-title", ".lesson-objective-link > span:last-child",
      ".spine-overview-badge", ".spine-overview-title", ".spine-overview-sub", ".spine-overview-body",
      ".prose p", ".prose li", ".callout-title", ".visual-caption",
      ".catalog-kicker", ".catalog-status-pill", ".catalog-syllabus-tag", ".catalog-syllabus-row > span:last-child",
      ".catalog-card-footer .ui-btn",
      ".glossary-dict-cat", ".glossary-dict-desc", ".glossary-dict-ai-cta",
      ".rail-shortcut-btn > span:first-child", ".rail-shortcut-badge", ".rail-section-heading > span:first-child",
      ".page-toc-header > span:first-child", ".page-toc-course-stage", ".page-toc-link > span"
    ].join(", ");

    const candidates = [];
    rootNodes.forEach(root => {
      root.querySelectorAll(selector).forEach(el => {
        if (el.closest("pre, .ascii-diagram, code")) return;
        if (el.querySelector("ul, ol, table, pre, .visual-card, .callout")) return;
        const txt = (el.textContent || "").trim();
        if (!txt || txt.length < 2) return;
        if (!el.hasAttribute("data-orig-vi-html")) {
          el.setAttribute("data-orig-vi-html", el.innerHTML);
        }
        const origHtml = el.getAttribute("data-orig-vi-html") || "";
        const cacheKey = "tr_en_v2:" + origHtml;
        const cached = FSDS_TTL_CACHE.getSync(cacheKey);
        if (cached) {
          el.innerHTML = cached;
        } else {
          candidates.push({ el, origHtml, cacheKey });
        }
      });
    });

    if (!candidates.length) return;

    const BATCH_SIZE = 18;
    for (let i = 0; i < candidates.length; i += BATCH_SIZE) {
      if (currentAppLang !== "en" || myToken !== activeTranslationToken) return;
      const batch = candidates.slice(i, i + BATCH_SIZE);
      const payload = batch.map((item, idx) => ({ id: idx, html: item.origHtml }));
      const prompt = `Translate the following Vietnamese technical education HTML snippets into crisp, natural, idiomatic English (Anthropic Academy style).
Preserve all HTML tags (<code>, <strong>, <em>, <span>, <a>) and attributes intact. Do NOT translate code identifiers or commands inside <code>.
Return ONLY a valid JSON array of objects [{"id": 0, "html": "..."}, ...] matching the input IDs:
${JSON.stringify(payload)}`;

      try {
        const respText = await callGeminiAI(prompt);
        const match = respText.match(/\[[\s\S]*\]/);
        if (match) {
          const arr = JSON.parse(match[0]);
          if (Array.isArray(arr)) {
            arr.forEach(entry => {
              const target = batch[entry.id];
              if (target && typeof entry.html === "string" && entry.html.trim()) {
                FSDS_TTL_CACHE.set(target.cacheKey, entry.html);
                if (currentAppLang === "en") {
                  target.el.innerHTML = entry.html;
                }
              }
            });
          }
        }
      } catch (_err) {
        break;
      }
    }
  }

  function restoreVietnameseView() {
    activeTranslationToken++;
    document.querySelectorAll("[data-orig-vi-html]").forEach(el => {
      el.innerHTML = el.getAttribute("data-orig-vi-html");
    });
  }

  function toggleAppLanguage() {
    currentAppLang = (currentAppLang === "vi") ? "en" : "vi";
    try {
      localStorage.setItem("fsds-lang", currentAppLang);
    } catch (_e) {}
    applyStaticUiChromeLanguage(currentAppLang);
    if (currentAppLang === "en") {
      showToast("Switching to English (AI Auto-Translate + TTL Cache)...");
      translateActiveViewToEnglish();
    } else {
      restoreVietnameseView();
      showToast("Đã chuyển về Tiếng Việt nguyên bản");
    }
    if (document.getElementById("glossaryPopover").classList.contains("open") && activeCustomTermTitle) {
      regenerateCurrentGlossaryAi();
    }
  }

  document.addEventListener("keydown", (e) => {
    if (e.isComposing) return;
    const tag = (e.target && e.target.tagName) ? e.target.tagName.toLowerCase() : "";
    const isTyping = tag === "input" || tag === "textarea" || (e.target && e.target.isContentEditable);

    if (e.key === "Escape") {
      if (document.getElementById("glossaryPopover").classList.contains("open")) {
        closeGlossaryPopover(true, true);
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
    const tocPct = document.getElementById("tocProgressPct");
    if (tocPct) tocPct.textContent = pct + "%";
    const tocFill = document.getElementById("tocProgressBarFill");
    if (tocFill) tocFill.style.width = pct + "%";
  }

  window.addEventListener("scroll", updateReadingProgress, { passive: true });
  window.addEventListener("resize", () => {
    if (window.innerWidth <= 900) {
      document.getElementById("syllabusRail").removeAttribute("inert");
    } else if (document.body.classList.contains("rail-collapsed")) {
      document.getElementById("syllabusRail").setAttribute("inert", "");
    }
  });

  const savedTheme = localStorage.getItem("fsds-theme") || "light";
  const savedAccent = localStorage.getItem("fsds-accent") || "clay";
  applyTheme(savedTheme);
  applyAccentTheme(savedAccent);
  applyStaticUiChromeLanguage(currentAppLang);

  function applyRouteFromUrl(eventState = null) {
    const parsed = parseRouteHash(window.location.hash);
    const nextTopic = (eventState && eventState.topic) || parsed.topic || activeTopic || "F01";
    const nextStage = (eventState && eventState.stage) || parsed.stage || (nextTopic !== activeTopic ? 1 : activeStorageStage) || 1;
    const nextSection = (eventState && eventState.section) || parsed.section || null;

    if (nextTopic === activeTopic && nextStage === activeStorageStage && nextSection && document.getElementById(nextSection)) {
      isHandlingRouteEvent = true;
      jumpToStation(nextSection, false);
      isHandlingRouteEvent = false;
      return;
    }

    isHandlingRouteEvent = true;
    selectTopic(nextTopic, nextStage, nextSection, false);
    isHandlingRouteEvent = false;
  }

  window.addEventListener("popstate", (e) => {
    applyRouteFromUrl(e.state || null);
  });

  window.addEventListener("hashchange", () => {
    applyRouteFromUrl(null);
  });

  const initRoute = parseRouteHash(window.location.hash);
  if (initRoute.topic) syncStateVars(initRoute.topic, initRoute.stage || 1, initRoute.section || activeStationId);
  else if (initRoute.stage) syncStateVars(activeTopic, initRoute.stage, initRoute.section || activeStationId);
  else if (initRoute.section) syncStateVars(activeTopic, activeStorageStage, initRoute.section);

  initGlossarySystem();
  renderSyllabus();
  renderMain(Boolean(initRoute.section));
  const initialCanonicalHash = formatRouteHash(activeTopic, activeStorageStage, initRoute.section || null);
  history.replaceState({ topic: activeTopic, stage: activeStorageStage, section: initRoute.section || null }, "", initialCanonicalHash);
  if (initRoute.section) {
    setTimeout(() => jumpToStation(initRoute.section, false), 50);
  }
  </script>
</body>
</html>
"""


def _load_obfuscated_ai_vault() -> dict:
    import os
    raw_key = os.environ.get("GEMINI_API_KEY", "").strip()
    env_file = ROOT / ".env.local"
    if not raw_key and env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                raw_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    mask = [73, 194, 41, 138, 211, 59, 92, 167]
    raw_bytes = raw_key.encode("utf-8") if raw_key else b""
    encoded = [(b ^ mask[i % len(mask)]) for i, b in enumerate(raw_bytes)]
    return {
        "m": mask,
        "d": encoded,
        "model": "models/gemini-3.5-flash-lite",
        "endpoint": "https://generativelanguage.googleapis.com/v1/interactions",
    }


def main():
    storage_ascii = build_storage_ascii_diagrams()
    linux_ascii = build_linux_ascii_diagrams()
    db_ascii = build_db_ascii_diagrams()
    container_ascii = build_container_ascii_diagrams()
    ingestion_ascii = build_ingestion_ascii_diagrams()

    compiled_html_template = HTML_TEMPLATE.replace("__LESSON_TEMPLATES_JS__", compile_lesson_templates_js())

    from glossary_scanner import scan_build_hub
    from ascii_engine import paint_ascii_html, export_dur_json, is_flagship_animated

    glossary_payload = scan_build_hub(ROOT / "scripts" / "build_hub.py")
    dur_dir = ROOT / "content" / "ascii-art"
    dur_dir.mkdir(parents=True, exist_ok=True)

    sample_dur_path = dur_dir / "linux-3.1a.dur"
    if not sample_dur_path.exists() and "3.1a" in linux_ascii:
        _, _, sample_roles = paint_ascii_html(linux_ascii["3.1a"]["ascii"])
        dur_obj = export_dur_json(linux_ascii["3.1a"]["ascii"], sample_roles, name="linux-3.1a")
        sample_dur_path.write_text(json.dumps(dur_obj, ensure_ascii=False, indent=2), encoding="utf-8")

    def _build_diag_map(ascii_dict, topic_prefix):
        out_map = {}
        for k in ascii_dict:
            raw_a = ascii_dict[k]["ascii"]
            dur_file = dur_dir / f"{topic_prefix}-{k}.dur"
            painted_html, max_cols, _ = paint_ascii_html(raw_a, dur_path=dur_file)
            out_map[k] = {
                "kind": ascii_dict[k]["kind"],
                "ascii": raw_a,
                "asciiHtml": painted_html,
                "maxCols": max_cols,
                "flagship": is_flagship_animated(topic_prefix, k),
            }
        return out_map

    picto_path = ROOT / "content" / "pictograms.json"
    pictograms_payload = (
        json.loads(picto_path.read_text(encoding="utf-8"))
        if picto_path.exists()
        else {"sealViewBox": "0 0 947.805 952.224", "sealPath": "", "pictograms": {}}
    )

    masks_payload = {}
    masks_dir = ROOT / "assets" / "masks"
    if masks_dir.exists():
        for svg_file in sorted(masks_dir.glob("*.svg")):
            b64_svg = base64.b64encode(svg_file.read_bytes()).decode("ascii")
            masks_payload[svg_file.stem] = f"data:image/svg+xml;base64,{b64_svg}"

    data_out = {
        "storage_diagrams": _build_diag_map(storage_ascii, "storage"),
        "linux_diagrams": _build_diag_map(linux_ascii, "linux"),
        "db_diagrams": _build_diag_map(db_ascii, "db"),
        "container_diagrams": _build_diag_map(container_ascii, "container"),
        "ingestion_diagrams": _build_diag_map(ingestion_ascii, "ingestion"),
        "pictograms": pictograms_payload,
        "masks": masks_payload,
        "ai_vault": _load_obfuscated_ai_vault(),
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
        compiled_html_template
        .replace("__FONT_FACES__", extract_font_faces())
        .replace("__HUB_DATA_JSON__", json.dumps(data_out, ensure_ascii=False))
    )
    (ROOT / "fsds-learning-hub.html").write_text(html, encoding="utf-8")
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    total_diags = sum(len(data_out[k]) for k in ("storage_diagrams", "linux_diagrams", "db_diagrams", "container_diagrams", "ingestion_diagrams"))
    g_stats = glossary_payload["stats"]
    print(
        f"Built fsds-learning-hub.html + index.html ({len(html):,} bytes), content/lessons-data.json, "
        f"{total_diags} colored ASCII diagrams, and "
        f"glossary ({g_stats['total_canonical_entries']} canonical entries, {g_stats['total_lookup_keys']} lookup keys, "
        f"{g_stats['unclassified_count']} unclassified) successfully."
    )


if __name__ == "__main__":
    main()

