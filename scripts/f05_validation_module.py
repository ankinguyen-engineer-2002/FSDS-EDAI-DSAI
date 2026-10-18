#!/usr/bin/env python3
"""
F05 · Validation & Verification — Colored ASCII Diagrams & 2D Interactive Simulator Module.
"""
from ascii_diagram import (
    display_width,
    join_horizontal,
    make_box as _raw_make_box,
    pad_center,
    verify_diagram,
)


def build_validation_ascii_diagrams() -> dict:
    def wrap_line(line: str, limit: int) -> list[str]:
        if display_width(line) <= limit:
            return [line]
        if any(c in line for c in "┐┘") or line.rstrip().endswith("│"):
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
    INNER_FULL = 132     # box width = 136
    INNER_HALF = 62      # box width = 66 -> 66 + 4 + 66 = 136
    INNER_THIRD = 38     # box width = 42 -> 42 + 4 + 42 + 4 + 42 = 134

    diagrams = {}

    # -------------------------------------------------------------------------
    # 0.1: Mental Map 4 Chặng — Hành trình Kiểm định checkout_order("ORD-8888")
    # -------------------------------------------------------------------------
    s01_c1 = make_box([
        "[CHẶNG 1: V-MODEL, SHIFT-LEFT & 3 PHƯƠNG PHÁP (TRẠM 1.1 -> 1.2)]",
        "├── Verification (Right Process) vs Validation (Right Product)",
        "├── V-Model đối xứng 4 tầng & Quy luật Chi phí Lỗi: 1x -> 30x",
        "├── Phân loại: Manual vs Automated | Black / Grey / White-box",
        "└── Hình thức: Hoare Logic {P}C{Q}, Symbolic Exec & Mutation",
    ], inner_width=INNER_HALF)
    s01_c2 = make_box([
        "[CHẶNG 2: PHẠM VI FUNCTIONAL & NON-FUNCTIONAL (TRẠM 2.1 -> 2.2)]",
        "├── Functional (Làm gì?) : Unit -> Integration -> System -> UAT",
        "├── Ba pha nghiệm thu    : Alpha (Nội bộ) -> Beta -> UAT (Client)",
        "├── Performance Testing  : Load (500 CCU) vs Stress (5000 CCU)",
        "└── Lưới chắn vận hành   : Smoke, Regression, Security, Recovery",
    ], inner_width=INNER_HALF)
    row_01_top = join_horizontal([s01_c1, s01_c2], ["    "], {3: [" ──►"]})

    s01_c3 = make_box([
        "[CHẶNG 3: THỰC CHIẾN FRAMEWORK PYTEST CỐT LÕI (TRẠM 3.1 -> 3.2)]",
        "├── Tự động dò tìm : test_*.py, def test_*(), class Test*",
        "├── @pytest.fixture: Tiêm phụ thuộc + yield (Setup / Teardown)",
        "├── conftest.py    : Chia sẻ Fixture toàn thư mục không cần import",
        "└── Phân luồng     : Markers (pytest -m) & @pytest.mark.parametrize",
    ], inner_width=INNER_HALF)
    s01_c4 = make_box([
        "[CHẶNG 4: MOCKING, TESTCONTAINERS, TOX & TDD (TRẠM 4.1 -> 4.2)]",
        "├── pytest-mock    : mocker.patch (Patch nơi gọi!) & MagicMock",
        "├── Testcontainers : Khởi chạy Docker PostgreSQL 16 thật tự hủy",
        "├── Đa môi trường  : tox (py39/310/311) & pytest-cov (Miss 6%)",
        "└── Quy trình TDD  : Vòng lặp 3 pha RED -> GREEN -> REFACTOR",
    ], inner_width=INNER_HALF)
    row_01_bot = join_horizontal([s01_c3, s01_c4], ["    "], {3: [" ──►"]})

    diagrams["0.1"] = {
        "ascii": "\n".join(
            banner("BẢN ĐỒ TƯ DUY 4 CHẶNG F05: HÀNH TRÌNH KIỂM ĐỊNH HÀM CHECKOUT_ORDER('ORD-8888')",
                   "(Từ Mô hình V-Model & Chi phí Shift-Left 1x->30x đến Tự động hóa pytest, Mocking, Testcontainers & TDD)")
            + [""]
            + row_01_top
            + v_arrow("Chuyển hóa từ Lý thuyết Phân loại Kiểm thử sang Dây chuyền Tự động hóa bằng Code (pytest)")
            + row_01_bot
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 1.1: V-Model & Chi phí sửa lỗi Shift-Left (1x -> 30x)
    # -------------------------------------------------------------------------
    s11_left = make_box([
        "[NHÁNH TRÁI: VERIFICATION PHASES (THE PROCESS CHECK)]",
        "• Câu hỏi gốc: 'Are we building the product RIGHT?'",
        "• Kiểm tra tài liệu & kiến trúc TRƯỚC khi chạy code:",
        "  [1] Requirement Gathering  (Đặc tả nghiệp vụ #8888)",
        "  [2] Functional Design      (Đặc tả luồng thanh toán)",
        "  [3] Internal System Design (Kiến trúc API <-> DB)",
        "  [4] Module Design          (Thuật toán checkout_order)",
    ], inner_width=INNER_HALF)
    s11_right = make_box([
        "[NHÁNH PHẢI: VALIDATION PHASES (THE RESULT CHECK)]",
        "• Câu hỏi gốc: 'Are we building the RIGHT product?'",
        "• Thực thi phần mềm thực tế đối chiếu ngược với nhánh trái:",
        "  <-> [4'] Unit Acceptance Testing (UAT - Khách nghiệm thu)",
        "  <-> [3'] Functional Testing      (Kiểm tra tính năng)",
        "  <-> [2'] Integration Testing     (Ghép nối API + DB)",
        "  <-> [1'] Unit Testing            (Kiểm thử hàm cô lập)",
    ], inner_width=INNER_HALF)
    row_11_top = join_horizontal([s11_left, s11_right], ["    "], {4: [" ◄─►"]})

    s11_cost = make_box([
        "[ĐÁY CHỮ V < CODING > & QUY LUẬT NHÂN 30 LẦN CHI PHÍ SỬA LỖI THEO THỜI GIAN PHÁT HIỆN (SHIFT-LEFT)]",
        "├── [Pha 1: Requirements / Architecture] : Chi phí sửa =  1x  │ [+] Sửa ngay trên tài liệu thiết kế trong 5 phút",
        "├── [Pha 2: Coding (Unit Testing)]       : Chi phí sửa =  5x  │ [+] Developer tự bắt lỗi bằng pytest ngay trên máy trạm",
        "├── [Pha 3: Integration Testing]         : Chi phí sửa = 10x  │ [!] Lệch hợp đồng giao tiếp giữa order-api và PostgreSQL",
        "├── [Pha 4: System / Acceptance (UAT)]   : Chi phí sửa = 15x  │ [!] Khách hàng phát hiện sai nghiệp vụ khi chạy thử",
        "└── [Pha 5: Production / Post-release]   : Chi phí sửa = 30x  │ [x] Trừ tiền đúp đơn #8888 -> Rollback, đền bù, mất uy tín!",
    ], inner_width=INNER_FULL)

    diagrams["1.1"] = {
        "ascii": "\n".join(
            banner("MÔ HÌNH CHỮ V (V-MODEL) & ĐƯỜNG CONG CHI PHÍ SỬA LỖI SHIFT-LEFT (1x -> 30x)")
            + [""]
            + row_11_top
            + v_arrow("Hội tụ tại Đáy chữ V: < CODING > (Code Verification & Validation)")
            + s11_cost
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 1.2: Black-box, Grey-box, White-box & Formal Verification
    # -------------------------------------------------------------------------
    s12_b1 = make_box([
        "[1. BLACK-BOX TESTING]",
        "• Tri thức code: 0% (Mù code)",
        "• Trọng tâm: Giao diện / API ngoài",
        "• Cách test: Bơm Input JSON #8888",
        "  -> So khớp Output HTTP 200 OK",
        "• Thực hiện: Tester / End-user",
        "• [!] Sót nhánh lỗi ẩn trong code",
    ], inner_width=INNER_THIRD)
    s12_b2 = make_box([
        "[2. GREY-BOX TESTING]",
        "• Tri thức code: Một phần (Partial)",
        "• Trọng tâm: Kiến trúc, DB Schema,",
        "  OpenAPI Contract & Data Flow",
        "• Cách test: Gọi API + kiểm tra dòng",
        "  ghi thật trong bảng orders DB",
        "• Thực hiện: Tester / Developer",
    ], inner_width=INNER_THIRD)
    s12_b3 = make_box([
        "[3. WHITE-BOX (GLASS-BOX)]",
        "• Tri thức code: 100% Source Code",
        "• Trọng tâm: Nhánh rẽ if/else, vòng",
        "  lặp, tối ưu hóa & Code Coverage",
        "• Cách test: Soi từng đường đi nội",
        "  tại của hàm checkout_order()",
        "• Thực hiện: Developer / SDET",
    ], inner_width=INNER_THIRD)
    row_12_top = join_horizontal([s12_b1, s12_b2, s12_b3], ["    ", "    "], {3: [" ──►", " ──►"]})

    s12_formal = make_box([
        "[BA KỸ THUẬT KIỂM CHỨNG HÌNH THỨC & ĐÁNH GIÁ CHẤT LƯỢNG BỘ TEST TRONG TẦNG WHITE-BOX (SYLLABUS CORE)]",
        "├── [A] Hoare Logic {P} C {Q} : Chứng minh toán học: Nếu thỏa Tiền điều kiện P {amount > 0} trước khi chạy lệnh C, luôn đạt Hậu điều kiện Q",
        "├── [B] Symbolic Execution    : Thay số cụ thể bằng biến ký hiệu (amount = alpha) để giải hệ phương trình tìm điều kiện biên làm sập hàm",
        "└── [C] Mutation Testing      : Cố tình cấy lỗi giả (đổi '>' thành '>=') tạo Mutant -> Nếu pytest báo FAIL (Killed) = Bộ test chất lượng cao!",
    ], inner_width=INNER_FULL)

    diagrams["1.2"] = {
        "ascii": "\n".join(
            banner("BA PHƯƠNG PHÁP KIỂM THỬ (BLACK / GREY / WHITE-BOX) & KIỂM CHỨNG HÌNH THỨC")
            + [""]
            + row_12_top
            + v_arrow("Đi sâu vào nội tạng mã nguồn (White-Box): Từ đo độ phủ dòng lệnh đến Chứng minh & Đột biến")
            + s12_formal
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 2.1: Functional Testing — 4 Cấp độ (Unit -> Integration -> System -> Acceptance)
    # -------------------------------------------------------------------------
    s21_top1 = make_box([
        "[CẤP 1: UNIT TESTING (CODE LEVEL)]",
        "├── Phạm vi  : 1 hàm / 1 class cô lập hoàn toàn",
        "├── Ví dụ    : Kiểm tra hàm add(2, 3) == 5 hoặc",
        "│              calculate_fee(450000) == 4500",
        "└── Đặc tính : Chạy cực nhanh (ms), số lượng nhiều nhất",
    ], inner_width=INNER_HALF)
    s21_top2 = make_box([
        "[CẤP 2: INTEGRATION TESTING (MODULE LEVEL)]",
        "├── Phạm vi  : Ghép nối 2+ modules / dịch vụ phụ thuộc",
        "├── Ví dụ    : Hàm Login đọc đúng bảng User DB; hoặc",
        "│              checkout_order() ghi đúng vào PostgreSQL",
        "└── Đặc tính : Bắt lỗi lệch kiểu dữ liệu & hợp đồng giao tiếp",
    ], inner_width=INNER_HALF)
    row_21_top = join_horizontal([s21_top1, s21_top2], ["    "], {2: [" ──►"]})

    s21_bot1 = make_box([
        "[CẤP 3: SYSTEM TESTING (END-TO-END NON-PROD)]",
        "├── Phạm vi  : Toàn bộ hệ thống ghép hoàn chỉnh trên Staging",
        "├── Ví dụ    : Luồng mua hàng E2E: Đăng nhập -> Tìm kiếm ->",
        "│              Đặt đơn #8888 -> Thanh toán -> Trang xác nhận",
        "└── Đặc tính : Xác nhận mọi mảnh ghép vận hành trơn tru",
    ], inner_width=INNER_HALF)
    s21_bot2 = make_box([
        "[CẤP 4: ACCEPTANCE TESTING (3 PHA NGHIỆM THU)]",
        "├── Phase 1 (Alpha) : Nhân viên nội bộ công ty kiểm thử sớm",
        "├── Phase 2 (Beta)  : Nhóm khách hàng thật dùng thử ngoài đời",
        "├── Phase 3 (UAT)   : Khách hàng nghiệm thu ký duyệt Release",
        "└── Đặc tính        : Chốt chặn cuối trước khi giao sản phẩm",
    ], inner_width=INNER_HALF)
    row_21_bot = join_horizontal([s21_bot1, s21_bot2], ["    "], {2: [" ──►"]})

    diagrams["2.1"] = {
        "ascii": "\n".join(
            banner("DÂY CHUYỀN 4 CẤP ĐỘ FUNCTIONAL TESTING: TỪ UNIT ĐẾN NGHIỆM THU ALPHA / BETA / UAT")
            + [""]
            + row_21_top
            + v_arrow("Mở rộng phạm vi từ Từng Module sang Toàn Hệ thống (End-to-End) & Nghiệm thu Người dùng")
            + row_21_bot
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 2.2: Non-Functional Testing — Load (500 CCU) vs Stress (5000 CCU) & Smoke/Regression
    # -------------------------------------------------------------------------
    s22_load = make_box([
        "[A. LOAD TESTING (KIỂM THỬ TẢI ĐỊNH MỨC)]",
        "├── Mức tải bơm vào : 500 Users truy cập đồng thời (Expected Load)",
        "├── Câu hỏi cốt lõi : Hệ thống có giữ được tốc độ phản hồi < 50ms",
        "│                     khi chạy ở mức tải thiết kế hàng ngày không?",
        "└── Kết quả kỳ vọng : [+] 0% lỗi, độ trễ ổn định, không nghẽn cổ chai",
    ], inner_width=INNER_HALF)
    s22_stress = make_box([
        "[B. STRESS TESTING (KIỂM THỬ CỰC HẠN / ĐIỂM GÃY)]",
        "├── Mức tải bơm vào : 5,000 Users dồn dập (Vượt xa giới hạn chuẩn)",
        "├── Câu hỏi cốt lõi : Hệ thống gãy ở ngưỡng nào (Breaking Point)?",
        "│                     Khi sập có Graceful Degradation hay mất data?",
        "└── Kết quả kỳ vọng : [!] Biết rõ trần chịu tải & tự phục hồi an toàn",
    ], inner_width=INNER_HALF)
    row_22_top = join_horizontal([s22_load, s22_stress], ["    "], {2: [" ──►"]})

    s22_ops = make_box([
        "[BẢY LỚP KIỂM THỬ PHI CHỨC NĂNG & VẬN HÀNH BẢO VỆ HỆ THỐNG (SLIDE 34-37)]",
        "├── [1. Security Testing]      : Kiểm tra mã hóa mật khẩu, phân quyền truy cập, chống đánh cắp dữ liệu & tấn công đăng nhập giả",
        "├── [2. Usability & Compat]    : Dễ điều hướng (Usability) + Chạy đồng nhất trên Android/iOS, Chrome/Firefox/Safari, Win/macOS",
        "├── [3. Smoke Testing]         : Bài kiểm tra sơ bộ cực nhanh xem các chức năng cơ bản nhất của bản build mới có chạy được không",
        "├── [4. Regression Testing]    : Chạy lại bộ test tự động sau mỗi lần sửa code để chắc chắn tính năng mới không làm vỡ tính năng cũ",
        "└── [5. Recovery & Monkey]     : Recovery (khả năng tự hồi phục sau crash/mất điện) | Monkey/Ad-hoc (bấm ngẫu nhiên không kịch bản)",
    ], inner_width=INNER_FULL)

    diagrams["2.2"] = {
        "ascii": "\n".join(
            banner("NON-FUNCTIONAL TESTING: LOAD (500 CCU) vs. STRESS (5000 CCU) & LƯỚI CHẮN VẬN HÀNH")
            + [""]
            + row_22_top
            + v_arrow("Kết hợp Đo kiểm Hiệu năng với Bảo mật, Tương thích & Kiểm thử Hồi quy Hàng ngày")
            + s22_ops
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 3.1: Pytest Discovery, @pytest.fixture (yield Setup/Teardown) & conftest.py
    # -------------------------------------------------------------------------
    s31_left = make_box([
        "[VÒNG ĐỜI @pytest.fixture VỚI TỪ KHÓA YIELD (SLIDE 42-43)]",
        "  @pytest.fixture",
        "  def resource():",
        "      # [Bước 1 - SETUP] Chạy TRƯỚC hàm test",
        "      r = {'name': 'database connection'}",
        "      yield r   # ---> [Bước 2] Trao 'r' cho test_ checkout(resource)",
        "      # [Bước 4 - TEARDOWN] Tự động chạy SAU khi test kết thúc!",
        "      print('Tearing down resource')",
    ], inner_width=INNER_HALF)
    s31_right = make_box([
        "[CHIA SẺ FIXTURE TỰ ĐỘNG QUA CONFTEST.PY (SLIDE 44)]",
        "  tests/",
        "  ├── conftest.py      # Chứa @pytest.fixture def shared_data()",
        "  ├── test_one.py      # Dùng thẳng shared_data() KHÔNG cần import!",
        "  └── test_two.py      # Dùng thẳng shared_data() KHÔNG cần import!",
        "",
        "  [+] pytest tự động dò conftest.py và cấp phát Fixture cho",
        "      mọi tệp test_*.py trong cùng thư mục và thư mục con.",
    ], inner_width=INNER_HALF)
    row_31 = join_horizontal([s31_left, s31_right], ["    "], {3: [" ──►"]})

    s31_disc = make_box([
        "[QUY TẮC TỰ ĐỘNG DÒ TÌM (TEST DISCOVERY) CỦA PYTEST (SLIDE 40-41)]",
        "├── Quét tệp tin : Tự động tìm các tệp có tiền tố 'test_*.py' hoặc hậu tố '*_test.py' trong thư mục dự án",
        "├── Quét hàm/lớp : Tự động chạy mọi hàm 'def test_*()' và các phương thức 'def test_*(self)' nằm trong lớp 'class Test*:'",
        "└── Báo cáo lỗi  : Nội soi biểu thức 'assert add(2, 3) == 5' để in chính xác giá trị thực tế làm bài test thất bại",
    ], inner_width=INNER_FULL)

    diagrams["3.1"] = {
        "ascii": "\n".join(
            banner("CƠ CHẾ PYTEST FIXTURE (YIELD SETUP / TEARDOWN), CONFTEST.PY & TEST DISCOVERY")
            + [""]
            + row_31
            + v_arrow("Kết hợp Tiêm phụ thuộc (Fixture Injection) với Quy ước Tự động Dò tìm")
            + s31_disc
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 3.2: Pytest Markers (-m, pyproject.toml) & @pytest.mark.parametrize
    # -------------------------------------------------------------------------
    s32_mark = make_box([
        "[A. PHÂN LUỒNG BẰNG MARKERS & PYPROJECT.TOML (SLIDE 45-49)]",
        "• Khai báo trong pyproject.toml (chống PytestUnknownMarkWarning):",
        "  [tool.pytest.ini_options]",
        "  markers = ['api: API tests', 'db: DB tests', 'slow: Slow tests']",
        "• Lọc thực thi bằng biểu thức logic trên CLI:",
        "  $ pytest -m 'api or db'        # Chạy nhóm API hoặc DB",
        "  $ pytest -m 'slow and not db'  # Chạy test chậm nhưng bỏ qua DB",
        "• Built-in: @pytest.mark.skip | skipif | xfail | parametrize",
    ], inner_width=INNER_HALF)
    s32_param = make_box([
        "[B. NHÂN BẢN KỊCH BẢN VỚI @pytest.mark.parametrize (SLIDE 50-51)]",
        "  @pytest.mark.parametrize('input, expected', [",
        "      (1, 2),   # ---> Ca chạy 1: test_add_one[1-2] PASSED",
        "      (2, 3),   # ---> Ca chạy 2: test_add_one[2-3] PASSED",
        "      (3, 4),   # ---> Ca chạy 3: test_add_one[3-4] PASSED",
        "  ])",
        "  def test_add_one(input, expected):",
        "      assert add_one(input) == expected",
    ], inner_width=INNER_HALF)
    row_32 = join_horizontal([s32_mark, s32_param], ["    "], {3: [" ──►"]})

    diagrams["3.2"] = {
        "ascii": "\n".join(
            banner("PHÂN LUỒNG KIỂM THỬ VỚI PYTEST MARKERS (-M) & NHÂN BẢN KỊCH BẢN PARAMETRIZE")
            + [""]
            + row_32
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 4.1: Giải phẫu Bẫy mocker.patch (Patch Where Used, Not Where Defined) & MagicMock
    # -------------------------------------------------------------------------
    s41_wrong = make_box([
        "[SAI LẦM KINH ĐIỂN: PATCH TẠI NƠI ĐỊNH NGHĨA (SLIDE 56)]",
        "• File myapp/service.py viết: from myapp.api import get_data",
        "  -> Không gian tên myapp.service đã giữ con trỏ tới hàm gốc!",
        "• Bài test gọi sai địa chỉ:",
        "  mocker.patch('myapp.api.get_data', return_value={'value': 10})",
        "• Hậu quả: process_data() vẫn gọi hàm gốc myapp.api cũ (trả về 5)",
        "  => [x] ASSERT RESULT == 20 FAILED! (Mock bị vô hiệu hóa)",
    ], inner_width=INNER_HALF)
    s41_right = make_box([
        "[CHUẨN XÁC: PATCH TẠI NƠI HÀM ĐƯỢC SỬ DỤNG (SLIDE 55-56)]",
        "• Quy tắc vàng: 'Patch where it is USED, not where DEFINED!'",
        "• Bài test chặn đúng tham chiếu trong myapp.service:",
        "  mocker.patch('myapp.service.get_data', return_value={'value': 10})",
        "• Kết quả: process_data() nhận{'value': 10} -> nhân 2 = 20",
        "  => [+] ASSERT RESULT == 20 PASSED! (Cô lập hoàn toàn API thật)",
        "• Kiểm chứng lời gọi: assert_called_once_with('Hello')",
    ], inner_width=INNER_HALF)
    row_41_top = join_horizontal([s41_wrong, s41_right], ["    "], {3: [" ──►"]})

    s41_magic = make_box([
        "[MÔ PHỎNG KỊCH BẢN THỰC TẾ LIÊN TIẾP VỚI MOCKER.MAGICMOCK & SIDE_EFFECT (SLIDE 57-59)]",
        "├── Tạo đối tượng giả đa năng : mock_api = mocker.MagicMock(side_effect=[{'name': 'Hung'}, Exception('API Error')])",
        "├── Lần gọi thứ 1 (Thành công): get_user_name(mock_api) -> trả về 'Hung' (kiểm tra luồng xử lý bình thường)",
        "└── Lần gọi thứ 2 (Ném ngoại lệ): with pytest.raises(Exception): get_user_name(mock_api) (kiểm tra luồng bắt lỗi / Retry)",
    ], inner_width=INNER_FULL)

    diagrams["4.1"] = {
        "ascii": "\n".join(
            banner("QUY TẮC VÀNG MOCKER.PATCH (PATCH WHERE USED) & MÔ PHỎNG LỖI VỚI MAGICMOCK")
            + [""]
            + row_41_top
            + v_arrow("Kết hợp Đánh tráo Hàm (mocker.patch) với Đối tượng Giả Thông minh (MagicMock side_effect)")
            + s41_magic
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 4.2: Testcontainers, tox, pytest-cov & Vòng lặp 3 pha TDD (Red-Green-Refactor)
    # -------------------------------------------------------------------------
    s42_b1 = make_box([
        "[1. TESTCONTAINERS (DOCKER DB)]",
        "• Vấn đề: Mock không bắt được lỗi",
        "  sai cú pháp SQL PostgreSQL thật",
        "• Cơ chế: Tự bật container Docker",
        "  with PostgresContainer('postgres:16')",
        "• Chạy xong khối with -> Tự hủy",
        "  container sạch sẽ 100%",
    ], inner_width=INNER_THIRD)
    s42_b2 = make_box([
        "[2. TOX & PYTEST-COV (COVERAGE)]",
        "• tox.ini: Tự tạo virtualenv & test",
        "  trên py39, py310, py311 + PyTorch",
        "• pytest --cov=myproj tests/:",
        "  Đo tỷ lệ dòng code đã được test",
        "• Cột Miss (6%): Chỉ điểm các dòng",
        "  Blind Spots chưa từng chạy qua!",
    ], inner_width=INNER_THIRD)
    s42_b3 = make_box([
        "[3. CHU TRÌNH TDD (3 PHA LẶP)]",
        "• Bước 1 [RED]     : Viết bài test",
        "  trước -> Chạy thấy FAIL",
        "• Bước 2 [GREEN]   : Viết code tối",
        "  giản nhất chỉ để test PASS",
        "• Bước 3 [REFACTOR]: Làm sạch & tối",
        "  ưu code dưới lưới bảo vệ xanh",
    ], inner_width=INNER_THIRD)
    row_42_top = join_horizontal([s42_b1, s42_b2, s42_b3], ["    ", "    "], {3: [" ──►", " ──►"]})

    s42_tradeoff = make_box([
        "[ĐÁNH ĐỔI KIẾN TRÚC CỦA TEST-DRIVEN DEVELOPMENT (TDD) — KHI NÀO DÙNG & KHI NÀO TRÁNH? (SLIDE 68)]",
        "├── [+] Lợi ích cốt lõi : Kiến trúc tách rời (Decoupled), Tài liệu sống (Living Docs), Tự tin tuyệt đối khi Refactor code",
        "├── [!] Chi phí đánh đổi: Thời gian phát triển ban đầu tăng thêm 20-50%; phải cập nhật cả code lẫn test khi đổi yêu cầu",
        "└── [>] Chỉ định thực tế: DÙNG cho Core Business Logic / AI Modules dài hạn; TRÁNH khi Rapid Prototyping hoặc CRUD đơn giản",
    ], inner_width=INNER_FULL)

    diagrams["4.2"] = {
        "ascii": "\n".join(
            banner("HỆ SINH THÁI TESTCONTAINERS + TOX + PYTEST-COV & CHU TRÌNH 3 PHA TDD")
            + [""]
            + row_42_top
            + v_arrow("Đánh đổi Kỹ thuật khi Áp dụng TDD trong Dự án Thực tế (Slide 68)")
            + s42_tradeoff
        ),
        "kind": "boxes",
    }

    for k, meta in diagrams.items():
        errs = verify_diagram(meta["ascii"], f"VAL-{k}", kind=meta["kind"])
        if errs:
            raise SystemExit(f"ASCII verification failed for VAL-{k} ({meta['kind']}): {errs}")
    return diagrams


VALIDATION_SIM2D_JS = """
  /* ==========================================================================
     CLAUDE / ANTHROPIC-STYLE 2D INTERACTIVE LAB FOR F05 (VALIDATION & PYTEST)
     ========================================================================== */
  const VAL2D_SLIDES = [
    {
      id: 1,
      chapter: "Chặng 1 · V-Model & Shift-Left",
      analogy: "Đường Cong Chi Phí Lỗi (1x → 30x)",
      title: "Mô Hình Chữ V (V-Model) & Quy Luật Nhân 30 Lần Chi Phí Sửa Lỗi",
      leadTitle: "Phát hiện lỗi ở Thiết kế tốn 1x — Để lọt lên Production tốn 30x",
      leadStory: "Mỗi pha thiết kế bên nhánh trái (Verification — làm đúng quy trình) phải được đối xứng với một pha kiểm thử bên nhánh phải (Validation — làm đúng sản phẩm). Hãy bấm chọn thời điểm phát hiện lỗi trên hàm checkout_order('ORD-8888') để quan sát chi phí khắc phục!",
      keypoints: [
        { b: "VER", t: "Verification (Nhánh Trái): Are we building the product right?", d: "Kiểm tra tài liệu đặc tả và cấu trúc thiết kế trước khi chạy code (Requirements → Functional → System → Module Design)." },
        { b: "VAL", t: "Validation (Nhánh Phải): Are we building the right product?", d: "Thực thi phần mềm thực tế để xác minh kết quả khớp nhu cầu người dùng (Unit → Integration → Functional → UAT)." },
        { b: "30x", t: "Shift-Left Testing: Đẩy kiểm thử về sớm nhất có thể", d: "Chi phí sửa lỗi tăng từ 1x (Requirements) → 5x (Coding) → 10x (Integration) → 15x (UAT) → 30x (Production)." }
      ],
      verdict: "Nguyên lý cốt lõi: Đừng đợi viết xong toàn bộ hệ thống mới kiểm thử — bắt lỗi ngay tại bàn thiết kế (1x) và Unit Test (5x).",
      simMode: "vmodel"
    },
    {
      id: 2,
      chapter: "Chặng 1 · Phương Pháp & Đột Biến",
      analogy: "Độ Xuyên Thấu Mã Nguồn & Mutant",
      title: "Black-Box vs. Grey-Box vs. White-Box & Kiểm Thử Đột Biến (Mutation)",
      leadTitle: "Từ hộp đen mù code đến giải phẫu nhánh rẽ & cấy lỗi giả Mutant",
      leadStory: "Thử chuyển đổi 3 góc nhìn kiểm thử trên hàm checkout_order() và kích hoạt Mutation Testing (đổi điều kiện > 0 thành >= 0) để xem bộ test của bạn có đủ nhạy để bắt lỗi biên không!",
      keypoints: [
        { b: "BLK", t: "Black-Box Testing (0% Code Knowledge)", d: "Chỉ bơm Input JSON và đo Output ngoài giao diện/API; không biết cấu trúc hàm bên trong." },
        { b: "GRY", t: "Grey-Box Testing (Partial Knowledge)", d: "Nắm tài liệu kiến trúc và bảng DB PostgreSQL để kiểm tra luồng dữ liệu tại ranh giới giao tiếp." },
        { b: "WHT", t: "White-Box, Hoare Logic {P}C{Q} & Mutation Testing", d: "Soi 100% nhánh rẽ nội tại và cố tình cấy lỗi giả (Mutant) để kiểm tra độ sắc bén của câu lệnh assert." }
      ],
      verdict: "100% Code Coverage vẫn có thể lọt lỗi nếu thiếu assert biên; Mutation Testing là thuốc thử cho chính bộ test của bạn.",
      simMode: "boxmethods"
    },
    {
      id: 3,
      chapter: "Chặng 2 · Phạm Vi Phi Chức Năng",
      analogy: "Định Mức 500 CCU vs Cực Hạn 5000 CCU",
      title: "Performance Testing: Load Testing (500 CCU) vs. Stress Testing (5000 CCU)",
      leadTitle: "Hệ thống chạy đúng với 1 người dùng nhưng có sống sót giờ Flash Sale?",
      leadStory: "Functional Testing xác nhận hàm thanh toán tính đúng tiền, còn Non-Functional Testing đo lường tốc độ và độ ổn định khi hàng nghìn người cùng bấm thanh toán.",
      keypoints: [
        { b: "LOAD", t: "Load Testing (Kiểm thử tải kỳ vọng — 500 Users)", d: "Đo độ trễ và thông lượng dưới mức tải bình thường/đỉnh dự kiến để đảm bảo không bị chậm." },
        { b: "STRS", t: "Stress Testing (Kiểm thử cực hạn — 5000 Users)", d: "Đẩy tải vượt xa giới hạn thiết kế để tìm điểm gãy (Breaking Point) và kiểm tra khả năng hạ cánh an toàn." },
        { b: "OPS", t: "Smoke Testing & Regression Testing hàng ngày", d: "Smoke Test lọc nhanh bản build hỏng; Regression Test đảm bảo code mới không làm vỡ tính năng cũ." }
      ],
      verdict: "Luôn chạy Smoke & Regression Test trong CI/CD mỗi ngày, và chạy Load/Stress Test trước mỗi đợt mở bán lớn.",
      simMode: "loadstress"
    },
    {
      id: 4,
      chapter: "Chặng 3 · Pytest Fixtures & Parametrize",
      analogy: "Tiêm Phụ Thuộc & Dọn Dẹp Tự Động",
      title: "Vòng Đời @pytest.fixture (yield Setup / Teardown) & conftest.py",
      leadTitle: "Mở kết nối trước yield — Tự động đóng kết nối sau yield dù Test Pass hay Fail",
      leadStory: "Quan sát cách pytest tự động phát hiện fixture trong conftest.py, chạy phần Setup trước từ khóa yield, bơm dữ liệu vào hàm test và luôn quay lại chạy phần Teardown sau yield.",
      keypoints: [
        { b: "YLD", t: "Cơ chế 2 nửa của từ khóa yield trong @pytest.fixture", d: "Code trước yield chạy trước bài test (Setup); code sau yield chạy ngay sau khi bài test kết thúc (Teardown)." },
        { b: "CNF", t: "Tệp đặc biệt tests/conftest.py", d: "Chia sẻ fixtures tự động cho mọi tệp test_*.py trong cùng thư mục mà không cần câu lệnh import." },
        { b: "PRM", t: "@pytest.mark.parametrize('input, expected', [...])", d: "Viết 1 hàm kiểm thử duy nhất nhưng tự động nhân bản chạy qua nhiều bộ tuple dữ liệu." }
      ],
      verdict: "Dùng yield trong fixture giúp triệt tiêu hoàn toàn nguy cơ rò rỉ kết nối Database khi bài test bị văng lỗi giữa chừng.",
      simMode: "fixtures"
    },
    {
      id: 5,
      chapter: "Chặng 4 · Quy Tắc Vàng Mocking",
      analogy: "Patch Where Used, Not Where Defined",
      title: "Giải Phẫu Bẫy mocker.patch() & Mô Phỏng Lỗi Với MagicMock(side_effect)",
      leadTitle: "Tại sao patch('myapp.api.get_data') thất bại khi service đã import hàm đó?",
      leadStory: "Khi myapp/service.py chạy lệnh 'from myapp.api import get_data', nó tạo một tham chiếu cục bộ ngay trong myapp.service. Bấm đổi địa chỉ patch bên dưới để xem con trỏ bộ nhớ đi về đâu!",
      keypoints: [
        { b: "ERR", t: "Sai lầm kinh điển: Patch tại nơi định nghĩa (myapp.api.get_data)", d: "Hàm process_data() trong myapp.service vẫn gọi qua tham chiếu cũ đã import từ trước → Mock hoàn toàn vô tác dụng!" },
        { b: "GOLD", t: "Quy tắc vàng: Patch tại nơi sử dụng (myapp.service.get_data)", d: "Đánh tráo trực tiếp tham chiếu nằm trong không gian tên myapp.service nơi hàm thực sự được gọi." },
        { b: "SIDE", t: "MagicMock(side_effect=[...]) mô phỏng chuỗi kịch bản", d: "Lần gọi 1 trả về dữ liệu thành công, lần gọi 2 ném Exception('API Error') để kiểm thử pytest.raises." }
      ],
      verdict: "Quy tắc bất di bất dịch của Python Mocking: Luôn mocker.patch() tại module ĐANG SỬ DỤNG hàm đó!",
      simMode: "mockpatch"
    },
    {
      id: 6,
      chapter: "Chặng 4 · Testcontainers, Coverage & TDD",
      analogy: "Vòng Lặp Red → Green → Refactor",
      title: "Testcontainers (PostgreSQL 16), Độ Phủ pytest-cov & Chu Trình 3 Pha TDD",
      leadTitle: "Viết bài test Fail trước (Red) → Viết code tối giản để Pass (Green) → Làm sạch (Refactor)",
      leadStory: "Bấm chuyển qua 3 pha của TDD kết hợp kiểm tra điểm mù Code Coverage (Miss 6% → 0%) và container PostgreSQL thật.",
      keypoints: [
        { b: "RED", t: "Pha 1 — RED: Viết bài test nhỏ cho tính năng chưa tồn tại", d: "Chạy pytest để xác nhận bài test Fail đúng lý do kỳ vọng trước khi viết bất kỳ dòng code nghiệp vụ nào." },
        { b: "GRN", t: "Pha 2 — GREEN: Viết lượng code đơn giản nhất để test Pass", d: "Chưa cần tối ưu hóa sớm; mục tiêu duy nhất là làm thanh trạng thái chuyển sang màu Xanh." },
        { b: "REF", t: "Pha 3 — REFACTOR + Testcontainers & pytest-cov", d: "Tối ưu cấu trúc code, kiểm tra SQL thật trên Docker PostgresContainer('postgres:16') và xóa điểm mù Miss." }
      ],
      verdict: "TDD tốn thêm 20–50% thời gian ban đầu nhưng đền đáp bằng kiến trúc module hóa sạch sẽ và sự tự tin tuyệt đối khi Refactor.",
      simMode: "tdd"
    }
  ];

  let val2dCurrentSlide = 0;
  let val2dState = {
    vPhase: "prod",
    boxMode: "white",
    mutantKilled: true,
    loadMode: "load500",
    fixOutcome: "pass",
    patchTarget: "correct",
    tddStep: "green"
  };

  function buildValidation2DSimulatorHtml() {
    return `
      <div class="infra2d-wrap" id="val2dWidgetRoot">
        <div class="infra2d-header">
          <div class="infra2d-brand">
            <div class="infra2d-brand-icon">2D</div>
            <div>
              <div class="infra2d-brand-badges">
                <span class="infra2d-tag">Mô Phỏng Kiểm Định &amp; Pytest Thực Chiến 2D</span>
                <span class="infra2d-chapter" id="val2dChapterBadge">Chặng 1 · V-Model &amp; Shift-Left</span>
              </div>
              <h4 class="infra2d-title-bar">Phòng Thí Nghiệm Tương Tác F05: Kiểm Định Hàm checkout_order(&#39;ORD-8888&#39;)</h4>
            </div>
          </div>
          <div class="infra2d-dots" id="val2dDots"></div>
          <button type="button" class="infra2d-btn" onclick="toggleValidation2DSummaryModal()">Bảng Tóm Tắt Cốt Lõi</button>
        </div>

        <div id="val2dSummaryDrawer" style="display:none;padding:14px 16px;background:var(--sim-canvas);border-bottom:1px solid var(--sim-border);">
          <div style="padding:10px 12px;border-radius:8px;background:var(--sim-flow-soft);border:1px solid color-mix(in oklab, var(--sim-flow) 35%, transparent);font-size:12.5px;color:var(--sim-flow);margin-bottom:10px;">
            <strong>Chuẩn cốt lõi F05 (Validation &amp; Verification):</strong> Đẩy kiểm thử sang trái (<strong>Shift-Left 1x–5x</strong>), tự động hóa bằng <strong>pytest</strong> (<code>@pytest.fixture</code> với <code>yield</code>, <code>conftest.py</code>, <code>@pytest.mark.parametrize</code>), cô lập phụ thuộc đúng chuẩn <code>mocker.patch(&#39;module_where_used.func&#39;)</code> + <code>Testcontainers</code> và áp dụng vòng lặp <strong>TDD (Red → Green → Refactor)</strong>.
          </div>
        </div>

        <div class="infra2d-grid">
          <div class="infra2d-col-left">
            <div>
              <div class="infra2d-pills">
                <span class="infra2d-pill-num" id="val2dSlideNumPill">SLIDE 1 / 6</span>
                <span class="infra2d-pill-analogy" id="val2dAnalogyPill">Cắt Lớp Kiểm Định</span>
              </div>
              <h3 class="infra2d-slide-h3" id="val2dSlideTitle"></h3>
              <div class="infra2d-story-box">
                <div class="infra2d-avatar" title="checkout_order('ORD-8888')">F05</div>
                <div>
                  <span class="infra2d-story-title" id="val2dLeadTitle"></span>
                  <p class="infra2d-story-text" id="val2dLeadStory"></p>
                </div>
              </div>
              <div class="infra2d-keypoints" id="val2dKeypoints"></div>
            </div>
            <div class="infra2d-verdict" id="val2dVerdictBox"></div>
          </div>

          <div class="infra2d-col-right">
            <div>
              <div class="infra2d-sim-top">
                <div class="infra2d-sim-live">
                  <span class="infra2d-sim-dot"></span>
                  <span>Sơ Đồ Cắt Lớp &amp; Luồng Kiểm Thử Chuyển Động (Animated SVG)</span>
                </div>
                <span class="infra2d-sim-hint">Bấm các nút kịch bản bên dưới để đổi trạng thái!</span>
              </div>
              <div class="infra2d-stage" id="val2dSimStage" style="padding:10px;"></div>
            </div>
            <div>
              <div class="infra2d-status" id="val2dSimStatusText">Sẵn sàng mô phỏng.</div>
              <div class="infra2d-controls" id="val2dSimControls"></div>
            </div>
          </div>
        </div>

        <div class="infra2d-footer">
          <button type="button" class="infra2d-btn" id="val2dBtnPrev" onclick="changeValidation2DSlide(-1)">← Mô Phỏng Trước</button>
          <div class="infra2d-progress-wrap">
            <div class="infra2d-progress-track">
              <div class="infra2d-progress-fill" id="val2dProgressFill" style="width:16.6%;"></div>
            </div>
            <span style="font-size:11px;color:var(--sim-muted);">Chọn 1 trong 6 lát cắt cốt lõi (1–6) hoặc bấm nút điều khiển kịch bản</span>
          </div>
          <button type="button" class="infra2d-btn infra2d-btn-primary" id="val2dBtnNext" onclick="changeValidation2DSlide(1)">Mô Phỏng Tiếp Theo →</button>
        </div>
      </div>
    `;
  }

  function toggleValidation2DSummaryModal() {
    const d = document.getElementById("val2dSummaryDrawer");
    if (!d) return;
    d.style.display = (d.style.display === "none" || !d.style.display) ? "block" : "none";
  }

  function changeValidation2DSlide(delta) {
    const next = val2dCurrentSlide + delta;
    if (next < 0 || next >= VAL2D_SLIDES.length) return;
    val2dCurrentSlide = next;
    renderValidation2DSlide();
  }

  function jumpValidation2DSlide(idx) {
    if (idx < 0 || idx >= VAL2D_SLIDES.length) return;
    val2dCurrentSlide = idx;
    renderValidation2DSlide();
  }

  function renderValidation2DSlide() {
    const root = document.getElementById("val2dWidgetRoot");
    if (!root) return;
    const slide = VAL2D_SLIDES[val2dCurrentSlide] || VAL2D_SLIDES[0];

    document.getElementById("val2dChapterBadge").textContent = slide.chapter;
    document.getElementById("val2dSlideNumPill").textContent = `SLIDE ${slide.id} / ${VAL2D_SLIDES.length}`;
    document.getElementById("val2dAnalogyPill").textContent = slide.analogy;
    document.getElementById("val2dSlideTitle").textContent = slide.title;
    document.getElementById("val2dLeadTitle").textContent = slide.leadTitle;
    document.getElementById("val2dLeadStory").textContent = slide.leadStory;

    const kpEl = document.getElementById("val2dKeypoints");
    kpEl.innerHTML = slide.keypoints.map(kp => `
      <div class="infra2d-kp-item">
        <div class="infra2d-kp-badge">${escapeHtml(kp.b)}</div>
        <div>
          <span class="infra2d-kp-title">${escapeHtml(kp.t)}</span>
          <p class="infra2d-kp-desc">${escapeHtml(kp.d)}</p>
        </div>
      </div>
    `).join("");

    document.getElementById("val2dVerdictBox").textContent = slide.verdict;

    const dotsEl = document.getElementById("val2dDots");
    dotsEl.innerHTML = VAL2D_SLIDES.map((s, idx) => `
      <button type="button" class="infra2d-dot-btn ${idx === val2dCurrentSlide ? 'active' : ''}" onclick="jumpValidation2DSlide(${idx})">${s.id}</button>
    `).join("");

    const prevBtn = document.getElementById("val2dBtnPrev");
    const nextBtn = document.getElementById("val2dBtnNext");
    if (prevBtn) prevBtn.disabled = (val2dCurrentSlide === 0);
    if (nextBtn) nextBtn.disabled = (val2dCurrentSlide === VAL2D_SLIDES.length - 1);

    const fillEl = document.getElementById("val2dProgressFill");
    if (fillEl) fillEl.style.width = `${((val2dCurrentSlide + 1) / VAL2D_SLIDES.length) * 100}%`;

    renderValidation2DInteractiveStage(slide.simMode);
  }

  function renderValidation2DInteractiveStage(mode) {
    const stage = document.getElementById("val2dSimStage");
    const status = document.getElementById("val2dSimStatusText");
    const ctrls = document.getElementById("val2dSimControls");
    if (!stage || !status || !ctrls) return;

    if (mode === "vmodel") {
      const p = val2dState.vPhase;
      const costMap = {
        req: { mult: "1x", col: "var(--sim-ok)", soft: "var(--sim-ok-soft)", lbl: "Requirements / Architecture" },
        code: { mult: "5x", col: "var(--sim-ok)", soft: "var(--sim-ok-soft)", lbl: "Coding & Unit Test" },
        integ: { mult: "10x", col: "var(--sim-warn)", soft: "var(--sim-warn-soft)", lbl: "Integration Testing" },
        uat: { mult: "15x", col: "var(--sim-warn)", soft: "var(--sim-warn-soft)", lbl: "System / UAT Testing" },
        prod: { mult: "30x", col: "var(--sim-danger)", soft: "var(--sim-danger-soft)", lbl: "Production Post-Release" }
      };
      const cur = costMap[p] || costMap.prod;

      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 240" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="12" y="10" width="536" height="220" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="24" y="28" fill="var(--sim-muted)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">V-MODEL SYMMETRY &amp; SHIFT-LEFT BUG COST MULTIPLIER (SLIDE 05-09)</text>

          <!-- V-Shape Path -->
          <path d="M 55 52 L 205 182 L 355 52" stroke="var(--sim-border)" stroke-width="3" fill="none"/>
          <circle r="5.5" fill="${cur.col}">
            <animateMotion dur="2.2s" repeatCount="indefinite" path="M 55 52 L 205 182 L 355 52"/>
          </circle>

          <!-- Left Verification Nodes -->
          <rect x="24" y="42" width="128" height="26" rx="5" fill="${p==='req'?'var(--sim-ok-soft)':'var(--sim-card)'}" stroke="${p==='req'?'var(--sim-ok)':'var(--sim-border)'}" stroke-width="1.5"/>
          <text x="32" y="59" fill="var(--sim-ink)" font-size="9.5" font-weight="700">1. Requirements</text>

          <rect x="52" y="82" width="128" height="26" rx="5" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="60" y="99" fill="var(--sim-ink)" font-size="9.5" font-weight="700">2. System Design</text>

          <rect x="82" y="122" width="128" height="26" rx="5" fill="${p==='code'?'var(--sim-ok-soft)':'var(--sim-card)'}" stroke="${p==='code'?'var(--sim-ok)':'var(--sim-border)'}" stroke-width="1.5"/>
          <text x="90" y="139" fill="var(--sim-ink)" font-size="9.5" font-weight="700">3. Module Design</text>

          <!-- Pivot Coding -->
          <rect x="148" y="168" width="114" height="28" rx="6" fill="var(--sim-flow-soft)" stroke="var(--sim-flow)" stroke-width="1.8"/>
          <text x="164" y="186" fill="var(--sim-flow)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">&lt; CODING &gt;</text>

          <!-- Right Validation Nodes -->
          <rect x="218" y="122" width="124" height="26" rx="5" fill="${p==='code'?'var(--sim-ok-soft)':'var(--sim-card)'}" stroke="${p==='code'?'var(--sim-ok)':'var(--sim-border)'}" stroke-width="1.5"/>
          <text x="226" y="139" fill="var(--sim-ink)" font-size="9.5" font-weight="700">Unit Testing (5x)</text>

          <rect x="246" y="82" width="124" height="26" rx="5" fill="${p==='integ'?'var(--sim-warn-soft)':'var(--sim-card)'}" stroke="${p==='integ'?'var(--sim-warn)':'var(--sim-border)'}" stroke-width="1.5"/>
          <text x="254" y="99" fill="var(--sim-ink)" font-size="9.5" font-weight="700">Integration (10x)</text>

          <rect x="272" y="42" width="124" height="26" rx="5" fill="${p==='uat'?'var(--sim-warn-soft)':'var(--sim-card)'}" stroke="${p==='uat'?'var(--sim-warn)':'var(--sim-border)'}" stroke-width="1.5"/>
          <text x="280" y="59" fill="var(--sim-ink)" font-size="9.5" font-weight="700">UAT / System (15x)</text>

          <!-- Right Cost Bar Chart -->
          <rect x="412" y="38" width="124" height="178" rx="7" fill="var(--sim-card)" stroke="${cur.col}" stroke-width="1.8"/>
          <text x="422" y="56" fill="var(--sim-ink)" font-size="10" font-weight="800">CHI PHÍ SỬA LỖI</text>
          <text x="422" y="92" fill="${cur.col}" font-size="28" font-weight="800" font-family="var(--cds-font-mono)">${cur.mult}</text>
          <text x="422" y="114" fill="var(--sim-sub)" font-size="9.5">${cur.lbl}</text>
          <rect x="422" y="130" width="16" height="70" rx="2" fill="var(--sim-border-muted)"/><rect x="422" y="196" width="16" height="4" rx="1" fill="var(--sim-ok)"/>
          <rect x="444" y="130" width="16" height="70" rx="2" fill="var(--sim-border-muted)"/><rect x="444" y="186" width="16" height="14" rx="1" fill="var(--sim-ok)"/>
          <rect x="466" y="130" width="16" height="70" rx="2" fill="var(--sim-border-muted)"/><rect x="466" y="174" width="16" height="26" rx="1" fill="var(--sim-warn)"/>
          <rect x="488" y="130" width="16" height="70" rx="2" fill="var(--sim-border-muted)"/><rect x="488" y="160" width="16" height="40" rx="1" fill="var(--sim-warn)"/>
          <rect x="510" y="130" width="16" height="70" rx="2" fill="var(--sim-border-muted)"/><rect x="510" y="130" width="16" height="70" rx="1" fill="var(--sim-danger)"/>
        </svg>
      `;
      status.innerHTML = `<strong style="color:${cur.col};">[Pha phát hiện: ${cur.lbl} — Chi phí ${cur.mult}]:</strong> ${p === 'prod' ? 'Lỗi lọt lên Production khiến đơn #8888 bị trừ tiền 2 lần: tốn chi phí khẩn cấp gấp 30 lần so với bắt lỗi từ giai đoạn Thiết kế!' : 'Nhờ Shift-Left Testing, lỗi được chặn đứng sớm ngay trong nội bộ với chi phí khắc phục cực thấp.'}`;
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${p==='req'?'infra2d-btn-emerald':''}" onclick="val2dState.vPhase='req';renderValidation2DInteractiveStage('vmodel')">1. Requirements (1x)</button>
        <button type="button" class="infra2d-btn ${p==='code'?'infra2d-btn-emerald':''}" onclick="val2dState.vPhase='code';renderValidation2DInteractiveStage('vmodel')">2. Coding / Unit (5x)</button>
        <button type="button" class="infra2d-btn ${p==='integ'?'infra2d-btn-amber':''}" onclick="val2dState.vPhase='integ';renderValidation2DInteractiveStage('vmodel')">3. Integration (10x)</button>
        <button type="button" class="infra2d-btn ${p==='uat'?'infra2d-btn-amber':''}" onclick="val2dState.vPhase='uat';renderValidation2DInteractiveStage('vmodel')">4. System / UAT (15x)</button>
        <button type="button" class="infra2d-btn ${p==='prod'?'infra2d-btn-danger':''}" onclick="val2dState.vPhase='prod';renderValidation2DInteractiveStage('vmodel')">5. Production (30x)</button>
      `;
    } else if (mode === "boxmethods") {
      const bm = val2dState.boxMode;
      const mut = val2dState.mutantKilled;
      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 240" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="12" y="10" width="536" height="220" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="24" y="28" fill="var(--sim-muted)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">GÓC NHÌN KIỂM THỬ: ${bm.toUpperCase()}-BOX &amp; MUTATION TESTING</text>

          <!-- Input -->
          <rect x="24" y="92" width="104" height="58" rx="6" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="34" y="114" fill="var(--sim-ink)" font-size="10.5" font-weight="700">Input Data</text>
          <text x="34" y="132" fill="var(--sim-flow)" font-size="9.5" font-family="var(--cds-font-mono)">amount=450000</text>

          <!-- Center Box (Black / Grey / White) -->
          <rect x="164" y="46" width="232" height="154" rx="8" fill="${bm==='black'?'var(--sim-ink)':(bm==='grey'?'var(--sim-card-alt)':'var(--sim-card)')}" stroke="${bm==='white'?'var(--sim-ok)':'var(--sim-border)'}" stroke-width="2"/>
          <text x="178" y="68" fill="${bm==='black'?'var(--sim-canvas)':'var(--sim-ink)'}" font-size="11" font-weight="800">${bm==='black'?'[BLACK-BOX: 0% CODE VISIBILITY]':(bm==='grey'?'[GREY-BOX: API CONTRACT + DB SCHEMA]':'[WHITE-BOX: 100% AST &amp; HOARE LOGIC]')}</text>
          ${bm === 'black' ? `
            <text x="178" y="112" fill="var(--sim-canvas)" font-size="10" font-family="var(--cds-font-mono)">??? (Hộp đen đóng kín)</text>
            <text x="178" y="132" fill="var(--sim-canvas)" font-size="9.5">Chỉ biết đầu vào &amp; đầu ra UI/API</text>
          ` : (bm === 'grey' ? `
            <text x="178" y="102" fill="var(--sim-sub)" font-size="10" font-family="var(--cds-font-mono)">POST /v1/orders/checkout</text>
            <text x="178" y="124" fill="var(--sim-flow)" font-size="10" font-family="var(--cds-font-mono)">TABLE orders (id, status, total)</text>
            <text x="178" y="146" fill="var(--sim-muted)" font-size="9.5">Kiểm tra giao diện &amp; dòng DB</text>
          ` : `
            <text x="178" y="96" fill="var(--sim-flow)" font-size="9.5" font-family="var(--cds-font-mono)">{P: amount &gt; 0} // Precondition</text>
            <text x="178" y="116" fill="${mut?'var(--sim-ok)':'var(--sim-danger)'}" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">if amount ${mut?'&gt; 0':'&gt;= 0 (Mutant!)'}:</text>
            <text x="178" y="136" fill="var(--sim-ink)" font-size="9.5" font-family="var(--cds-font-mono)">  charge(450000)</text>
            <text x="178" y="156" fill="var(--sim-ok)" font-size="9.5" font-family="var(--cds-font-mono)">{Q: balance_deducted == True}</text>
          `)}

          <!-- Output -->
          <rect x="432" y="92" width="104" height="58" rx="6" fill="var(--sim-card)" stroke="${mut?'var(--sim-ok)':'var(--sim-danger)'}" stroke-width="1.5"/>
          <text x="442" y="114" fill="var(--sim-ink)" font-size="10.5" font-weight="700">Output Check</text>
          <text x="442" y="132" fill="${mut?'var(--sim-ok)':'var(--sim-danger)'}" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">${mut?'[+] PASS / KILLED':'[x] SURVIVED!'}</text>

          <path d="M 128 121 L 164 121" stroke="var(--sim-flow)" stroke-width="2.2"/>
          <path d="M 396 121 L 432 121" stroke="${mut?'var(--sim-ok)':'var(--sim-danger)'}" stroke-width="2.2"/>
        </svg>
      `;
      status.innerHTML = `<strong style="color:var(--sim-flow);">[Phương pháp: ${bm.toUpperCase()}-BOX]:</strong> ${bm==='black'?'Kiểm thử viên tương tác bên ngoài mà không nhìn thấy mã nguồn.':(bm==='grey'?'Kết hợp tài liệu thiết kế và truy vấn bảng PostgreSQL để kiểm tra luồng dữ liệu.':'Nắm trọn 100% nhánh rẽ nội tại, chứng minh Hoare Logic {P}C{Q} và dùng Mutation Testing để diệt lỗi biên!')}`;
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${bm==='black'?'infra2d-btn-primary':''}" onclick="val2dState.boxMode='black';renderValidation2DInteractiveStage('boxmethods')">1. Black-Box (0% Code)</button>
        <button type="button" class="infra2d-btn ${bm==='grey'?'infra2d-btn-amber':''}" onclick="val2dState.boxMode='grey';renderValidation2DInteractiveStage('boxmethods')">2. Grey-Box (API + DB)</button>
        <button type="button" class="infra2d-btn ${bm==='white'?'infra2d-btn-emerald':''}" onclick="val2dState.boxMode='white';renderValidation2DInteractiveStage('boxmethods')">3. White-Box (100% Code)</button>
        <button type="button" class="infra2d-btn ${!mut?'infra2d-btn-danger':''}" onclick="val2dState.boxMode='white';val2dState.mutantKilled=!val2dState.mutantKilled;renderValidation2DInteractiveStage('boxmethods')">Đảo trạng thái Mutant (&gt; vs &gt;=)</button>
      `;
    } else if (mode === "loadstress") {
      const isStress = val2dState.loadMode === "stress5000";
      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 240" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="12" y="10" width="536" height="220" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="24" y="28" fill="var(--sim-muted)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">PERFORMANCE TESTING: ${isStress ? 'STRESS TESTING (5,000 CCU - VƯỢT NGƯỠNG)' : 'LOAD TESTING (500 CCU - TẢI KỲ VỌNG)'}</text>

          <rect x="28" y="64" width="144" height="116" rx="8" fill="var(--sim-card)" stroke="${isStress?'var(--sim-danger)':'var(--sim-ok)'}" stroke-width="1.8"/>
          <text x="40" y="88" fill="var(--sim-ink)" font-size="11" font-weight="800">${isStress ? '5,000 Concurrent' : '500 Concurrent'}</text>
          <text x="40" y="106" fill="var(--sim-sub)" font-size="9.5">Request 1..N dồn dập</text>
          <text x="40" y="132" fill="${isStress?'var(--sim-danger)':'var(--sim-ok)'}" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">${isStress ? 'Bơm vượt trần 10x!' : 'Mức tải định mức'}</text>

          <rect x="228" y="64" width="144" height="116" rx="8" fill="${isStress?'var(--sim-danger-soft)':'var(--sim-ok-soft)'}" stroke="${isStress?'var(--sim-danger)':'var(--sim-ok)'}" stroke-width="2"/>
          <text x="244" y="92" fill="var(--sim-ink)" font-size="12" font-weight="800">Our ML / Order App</text>
          <text x="244" y="116" fill="${isStress?'var(--sim-danger)':'var(--sim-ok)'}" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">${isStress ? 'CPU: 100% (Breaking!)' : 'CPU: 42% (Stable)'}</text>
          <text x="244" y="138" fill="var(--sim-sub)" font-size="9.5" font-family="var(--cds-font-mono)">${isStress ? 'p99: Timeout / 503' : 'p99: 18 ms'}</text>

          <rect x="408" y="64" width="124" height="116" rx="8" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="420" y="88" fill="var(--sim-ink)" font-size="10.5" font-weight="700">Mục tiêu Kiểm định</text>
          <text x="420" y="112" fill="var(--sim-sub)" font-size="9.5">${isStress ? 'Tìm điểm gãy &amp;' : 'Đảm bảo tốc độ'}</text>
          <text x="420" y="128" fill="var(--sim-sub)" font-size="9.5">${isStress ? 'Graceful Crash' : 'không suy thoái'}</text>

          <path d="M 172 122 L 228 122" stroke="${isStress?'var(--sim-danger)':'var(--sim-ok)'}" stroke-width="3" stroke-dasharray="5 4"/>
          <circle r="5.5" fill="${isStress?'var(--sim-danger)':'var(--sim-ok)'}">
            <animateMotion dur="${isStress?'0.5s':'1.3s'}" repeatCount="indefinite" path="M 172 122 L 228 122"/>
          </circle>
        </svg>
      `;
      status.innerHTML = isStress
        ? `<strong style="color:var(--sim-danger);">[Stress Testing — 5,000 Users]:</strong> Đẩy hệ thống vượt xa giới hạn bình thường để xác định chính xác ngưỡng gãy (Breaking Point) và đảm bảo máy chủ hạ cánh an toàn (Graceful Degradation) thay vì hỏng dữ liệu.`
        : `<strong style="color:var(--sim-ok);">[Load Testing — 500 Users]:</strong> Kiểm tra ứng dụng dưới mức tải kỳ vọng (Expected Normal Load) — xác nhận 500 người dùng cùng lúc không làm chậm tốc độ phản hồi (p99 = 18ms).`;
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${!isStress?'infra2d-btn-emerald':''}" onclick="val2dState.loadMode='load500';renderValidation2DInteractiveStage('loadstress')">1. Load Testing (500 Users — Kỳ vọng)</button>
        <button type="button" class="infra2d-btn ${isStress?'infra2d-btn-danger':''}" onclick="val2dState.loadMode='stress5000';renderValidation2DInteractiveStage('loadstress')">2. Stress Testing (5,000 Users — Tìm điểm gãy)</button>
      `;
    } else if (mode === "fixtures") {
      const isPass = val2dState.fixOutcome === "pass";
      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 240" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="12" y="10" width="536" height="220" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="24" y="28" fill="var(--sim-muted)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">VÒNG ĐỜI @PYTEST.FIXTURE VỚI YIELD &amp; CONFTEST.PY (SLIDE 42-44)</text>

          <rect x="24" y="56" width="150" height="128" rx="7" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.6"/>
          <text x="34" y="76" fill="var(--sim-flow)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">1. BEFORE YIELD (SETUP)</text>
          <text x="34" y="98" fill="var(--sim-ink)" font-size="9.5" font-family="var(--cds-font-mono)">@pytest.fixture</text>
          <text x="34" y="114" fill="var(--sim-ink)" font-size="9.5" font-family="var(--cds-font-mono)">def resource():</text>
          <text x="34" y="132" fill="var(--sim-ok)" font-size="9.5" font-family="var(--cds-font-mono)">  r = connect_db()</text>
          <text x="34" y="150" fill="var(--sim-flow)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">  yield r</text>

          <rect x="205" y="56" width="150" height="128" rx="7" fill="${isPass?'var(--sim-ok-soft)':'var(--sim-danger-soft)'}" stroke="${isPass?'var(--sim-ok)':'var(--sim-danger)'}" stroke-width="1.8"/>
          <text x="215" y="76" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">2. TEST EXECUTES</text>
          <text x="215" y="102" fill="var(--sim-ink)" font-size="9.5" font-family="var(--cds-font-mono)">def test_sum(resource):</text>
          <text x="215" y="122" fill="${isPass?'var(--sim-ok)':'var(--sim-danger)'}" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">  ${isPass ? 'assert sum == 15 [PASS]' : 'assert sum == 99 [FAIL]'}</text>
          <text x="215" y="148" fill="var(--sim-muted)" font-size="9">Tự động nhận từ conftest.py</text>

          <rect x="386" y="56" width="150" height="128" rx="7" fill="var(--sim-ok-soft)" stroke="var(--sim-ok)" stroke-width="1.8"/>
          <text x="396" y="76" fill="var(--sim-ok)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">3. AFTER YIELD (CLEANUP)</text>
          <text x="396" y="104" fill="var(--sim-ink)" font-size="9.5" font-family="var(--cds-font-mono)">  r.close()</text>
          <text x="396" y="124" fill="var(--sim-ok)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">[+] LUÔN CHẠY 100%!</text>
          <text x="396" y="146" fill="var(--sim-sub)" font-size="9">Dọn dẹp kể cả khi Test Fail</text>

          <path d="M 174 120 L 205 120 M 355 120 L 386 120" stroke="var(--sim-flow)" stroke-width="2.2"/>
          <circle r="5" fill="var(--sim-ok)"><animateMotion dur="1.8s" repeatCount="indefinite" path="M 100 120 L 280 120 L 460 120"/></circle>
        </svg>
      `;
      status.innerHTML = `<strong style="color:var(--sim-ok);">[Fixture Lifecycle — ${isPass ? 'Test PASSED' : 'Test FAILED'}]:</strong> Ngay cả khi hàm kiểm thử bị ${isPass ? 'Pass' : 'văng AssertionError giữa chừng'}, pytest vẫn quay trở lại điểm neo <code>yield</code> để thực thi đoạn code Teardown phía sau, đảm bảo không rò rỉ kết nối Database!`;
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${isPass?'infra2d-btn-emerald':''}" onclick="val2dState.fixOutcome='pass';renderValidation2DInteractiveStage('fixtures')">1. Chạy Test PASS (Setup → Test → Teardown)</button>
        <button type="button" class="infra2d-btn ${!isPass?'infra2d-btn-danger':''}" onclick="val2dState.fixOutcome='fail';renderValidation2DInteractiveStage('fixtures')">2. Giả lập Test FAIL (Teardown sau yield vẫn chạy!)</button>
      `;
    } else if (mode === "mockpatch") {
      const ok = val2dState.patchTarget === "correct";
      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 240" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="12" y="10" width="536" height="220" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="24" y="28" fill="var(--sim-muted)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">QUY TẮC VÀNG MOCKER.PATCH: PATCH WHERE USED vs. WHERE DEFINED (SLIDE 55-56)</text>

          <!-- myapp/api.py -->
          <rect x="24" y="52" width="168" height="72" rx="7" fill="var(--sim-card)" stroke="${!ok?'var(--sim-danger)':'var(--sim-border)'}" stroke-width="1.6"/>
          <text x="34" y="72" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">myapp/api.py (Defined)</text>
          <text x="34" y="90" fill="var(--sim-sub)" font-size="9.5" font-family="var(--cds-font-mono)">def get_data(): return 5</text>
          <text x="34" y="108" fill="${!ok?'var(--sim-danger)':'var(--sim-muted)'}" font-size="9" font-family="var(--cds-font-mono)">${!ok?'[x] Patch nhầm vào đây!':'Nơi định nghĩa gốc'}</text>

          <!-- myapp/service.py -->
          <rect x="24" y="142" width="230" height="72" rx="7" fill="var(--sim-card)" stroke="${ok?'var(--sim-ok)':'var(--sim-danger)'}" stroke-width="1.8"/>
          <text x="34" y="162" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">myapp/service.py (Where Used!)</text>
          <text x="34" y="180" fill="var(--sim-flow)" font-size="9.5" font-family="var(--cds-font-mono)">from myapp.api import get_data</text>
          <text x="34" y="198" fill="${ok?'var(--sim-ok)':'var(--sim-danger)'}" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">${ok?'[+] Đã chặn thành Mock = 10':'[!] Vẫn trỏ về hàm thật = 5!'}</text>

          <!-- Result Box -->
          <rect x="304" y="84" width="228" height="104" rx="8" fill="${ok?'var(--sim-ok-soft)':'var(--sim-danger-soft)'}" stroke="${ok?'var(--sim-ok)':'var(--sim-danger)'}" stroke-width="2"/>
          <text x="318" y="108" fill="var(--sim-ink)" font-size="11" font-weight="800" font-family="var(--cds-font-mono)">process_data() = data * 2</text>
          <text x="318" y="134" fill="${ok?'var(--sim-ok)':'var(--sim-danger)'}" font-size="12" font-weight="800" font-family="var(--cds-font-mono)">${ok ? 'Result = 20 == 20 [PASS]' : 'Result = 10 != 20 [FAIL]'}</text>
          <text x="318" y="158" fill="var(--sim-sub)" font-size="9.5" font-family="var(--cds-font-mono)">${ok ? "mocker.patch('myapp.service.get_data')" : "mocker.patch('myapp.api.get_data')"}</text>

          <path d="M 254 178 L 304 136" stroke="${ok?'var(--sim-ok)':'var(--sim-danger)'}" stroke-width="2.4"/>
        </svg>
      `;
      status.innerHTML = ok
        ? `<strong style="color:var(--sim-ok);">[ĐÚNG CHUẨN — Patch Where Used]:</strong> <code>mocker.patch('myapp.service.get_data', return_value={'value': 10})</code> thay thế đúng tham chiếu bên trong <code>myapp.service</code> — hàm <code>process_data()</code> trả về 20 (PASS).`
        : `<strong style="color:var(--sim-danger);">[SAI LẦM PHỔ BIẾN NHẤT — Patch Where Defined]:</strong> Vì <code>myapp/service.py</code> đã chạy <code>from myapp.api import get_data</code>, việc patch vào <code>myapp.api.get_data</code> không ảnh hưởng tới tham chiếu cục bộ trong <code>myapp.service</code>!`;
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${ok?'infra2d-btn-emerald':''}" onclick="val2dState.patchTarget='correct';renderValidation2DInteractiveStage('mockpatch')">1. Patch ĐÚNG: mocker.patch('myapp.service.get_data')</button>
        <button type="button" class="infra2d-btn ${!ok?'infra2d-btn-danger':''}" onclick="val2dState.patchTarget='wrong';renderValidation2DInteractiveStage('mockpatch')">2. Patch SAI: mocker.patch('myapp.api.get_data')</button>
      `;
    } else {
      const st = val2dState.tddStep;
      const isRed = st === "red";
      const isGreen = st === "green";
      const isRef = st === "refactor";
      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 240" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="12" y="10" width="536" height="220" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="24" y="28" fill="var(--sim-muted)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">CHU TRÌNH TDD (RED → GREEN → REFACTOR) &amp; CODE COVERAGE (SLIDE 64-68)</text>

          <rect x="24" y="62" width="152" height="122" rx="8" fill="${isRed?'var(--sim-danger-soft)':'var(--sim-card)'}" stroke="${isRed?'var(--sim-danger)':'var(--sim-border)'}" stroke-width="2"/>
          <text x="36" y="86" fill="var(--sim-danger)" font-size="11" font-weight="800" font-family="var(--cds-font-mono)">1. RED (WRITE TEST)</text>
          <text x="36" y="108" fill="var(--sim-ink)" font-size="9.5">Viết bài test trước khi</text>
          <text x="36" y="124" fill="var(--sim-ink)" font-size="9.5">viết code thực tế</text>
          <text x="36" y="152" fill="var(--sim-danger)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">[x] Test Fails!</text>

          <rect x="204" y="62" width="152" height="122" rx="8" fill="${isGreen?'var(--sim-ok-soft)':'var(--sim-card)'}" stroke="${isGreen?'var(--sim-ok)':'var(--sim-border)'}" stroke-width="2"/>
          <text x="216" y="86" fill="var(--sim-ok)" font-size="11" font-weight="800" font-family="var(--cds-font-mono)">2. GREEN (MIN CODE)</text>
          <text x="216" y="108" fill="var(--sim-ink)" font-size="9.5">Viết code đơn giản nhất</text>
          <text x="216" y="124" fill="var(--sim-ink)" font-size="9.5">để vượt qua bài test</text>
          <text x="216" y="152" fill="var(--sim-ok)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">[+] All Tests Pass!</text>

          <rect x="384" y="62" width="152" height="122" rx="8" fill="${isRef?'var(--sim-flow-soft)':'var(--sim-card)'}" stroke="${isRef?'var(--sim-flow)':'var(--sim-border)'}" stroke-width="2"/>
          <text x="396" y="86" fill="var(--sim-flow)" font-size="11" font-weight="800" font-family="var(--cds-font-mono)">3. REFACTOR (CLEAN)</text>
          <text x="396" y="108" fill="var(--sim-ink)" font-size="9.5">Tối ưu &amp; làm sạch code</text>
          <text x="396" y="124" fill="var(--sim-ink)" font-size="9.5">dưới lưới bảo hiểm test</text>
          <text x="396" y="152" fill="var(--sim-flow)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">Coverage: 94% (Miss 6%)</text>

          <path d="M 176 122 L 204 122 M 356 122 L 384 122" stroke="var(--sim-flow)" stroke-width="2.2"/>
        </svg>
      `;
      status.innerHTML = isRed
        ? `<strong style="color:var(--sim-danger);">[Bước 1 — RED]:</strong> Viết bài kiểm thử cho một tính năng nhỏ chưa được lập trình. Chạy <code>pytest</code> và quan sát bài test Fail đúng như dự kiến.`
        : (isGreen
          ? `<strong style="color:var(--sim-ok);">[Bước 2 — GREEN]:</strong> Viết lượng code tối giản nhất có thể chỉ để làm bài test chuyển sang màu Xanh (Pass), không tối ưu hóa sớm.`
          : `<strong style="color:var(--sim-flow);">[Bước 3 — REFACTOR &amp; Coverage]:</strong> Làm sạch cấu trúc code, chạy <code>Testcontainers</code> + <code>tox</code> + <code>pytest --cov=myproj</code> trong khi bộ test đảm bảo không làm vỡ bất kỳ tính năng nào.`);
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${isRed?'infra2d-btn-danger':''}" onclick="val2dState.tddStep='red';renderValidation2DInteractiveStage('tdd')">1. Pha RED (Viết Test Fail)</button>
        <button type="button" class="infra2d-btn ${isGreen?'infra2d-btn-emerald':''}" onclick="val2dState.tddStep='green';renderValidation2DInteractiveStage('tdd')">2. Pha GREEN (Viết Code Tối Giản)</button>
        <button type="button" class="infra2d-btn ${isRef?'infra2d-btn-primary':''}" onclick="val2dState.tddStep='refactor';renderValidation2DInteractiveStage('tdd')">3. Pha REFACTOR (+ Coverage 94%)</button>
      `;
    }
  }
"""
