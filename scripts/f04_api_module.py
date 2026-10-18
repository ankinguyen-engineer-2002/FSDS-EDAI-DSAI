#!/usr/bin/env python3
import sys
from pathlib import Path

from ascii_diagram import (
    make_box as _raw_make_box,
    join_horizontal,
    pad_center,
    display_width,
    verify_diagram,
    verify_character_policy,
)


def build_api_ascii_diagrams() -> dict:
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
    INNER_FULL = W - 4    # 132 -> box width 136
    INNER_HALF = 62       # box width 66 -> 66 + 4 + 66 = 136
    INNER_THIRD = 38      # box width 42 -> 42 + 4 + 42 + 4 + 42 = 134

    diagrams = {}

    # -------------------------------------------------------------------------
    # 0.1: Mental Map 5 Chặng — Hành trình Gói tin Order #8888 qua Web API
    # -------------------------------------------------------------------------
    s01_c1 = make_box([
        "[CHẶNG 1: GIAO THỨC WEB & 4 TẦNG MẠNG TCP/IP (TRẠM 1.1 -> 1.4)]",
        "├── Tầng Ứng dụng : HTTP Request/Response, 6 phần Endpoint, DNS, TLS",
        "├── Tầng Giao vận : TCP 3-Way Handshake (ISN 1000/5000) vs UDP",
        "├── Tầng Mạng/Link: IPv4 (32-bit) / IPv6 (128-bit), MAC & Router NAT",
        "└── Luồng 10 bước : 192.168.1.10 -> NAT 203.0.113.5 -> 142.250.190.78",
    ], inner_width=INNER_HALF)
    s01_c2 = make_box([
        "[CHẶNG 2: SÁU PHONG CÁCH KIẾN TRÚC API (TRẠM 2.1 -> 2.5)]",
        "├── Request-Reply : REST (93%, 6 nguyên lý) | GraphQL (33%, Query AST)",
        "├── Nhị phân nội bộ: gRPC (14%, HTTP/2 Multiplexing + Protobuf .proto)",
        "├── Luồng Real-time: WebSocket (35%, 101 Upgrade) | SSE (12%, 1 chiều)",
        "└── Hướng sự kiện : Webhook (50%, Reverse HTTP POST + HMAC-SHA256)",
    ], inner_width=INNER_HALF)
    row_01_top = join_horizontal([s01_c1, s01_c2], ["    "], {3: [" ──►"]})

    s01_c3 = make_box([
        "[CHẶNG 3: BẢO MẬT WEB API — AAA, BASIC AUTH, JWT & OAUTH 2.0]",
        "├── 6 Mối đe dọa  : Unauthorized, Broken Auth, Exposure, Prompt Inj.",
        "├── Khung 3 chữ A : Authentication -> Authorization (RBAC) -> Accounting",
        "├── Basic vs JWT  : Base64(user:pass) vs Header.Payload.Signature (0 DB)",
        "└── OAuth 2.0     : Ủy quyền 8 bước qua Consent Flow & Access Token",
    ], inner_width=INNER_HALF)
    s01_c4 = make_box([
        "[CHẶNG 4: HEALTH PROBES, CHỈ SỐ p95/p99 & KIỂM THỬ CHỊU TẢI]",
        "├── K8s Probes    : /liveness (Restart Pod) vs /readiness (Ngắt LB)",
        "├── 6 Metrics     : Response Time, Error Rate, RPS, Uptime, p50/p95/p99",
        "├── 6 Bài Test    : Load (100 users), Stress (220->280), Spike, Soak...",
        "└── Phản ứng sập  : Graceful Degradation (800ms) vs Hard Failure (500)",
    ], inner_width=INNER_HALF)
    row_01_mid = join_horizontal([s01_c3, s01_c4], ["    "], {3: [" ──►"]})

    s01_c5 = make_box([
        "[CHẶNG 5: KIẾN TRÚC FASTAPI THỰC CHIẾN — ĐỘNG CƠ ASGI, PYDANTIC V2, MIDDLEWARE & LOCUST (TRẠM 5.1 -> 5.3)]",
        "├── Động cơ ASGI  : Uvicorn (uvloop + httptools) -> Starlette -> FastAPI (Phân tách rạch ròi async def vs def)",
        "├── Cổng kiểm dịch: Pydantic v2 (pydantic-core Rust) ép kiểu đầu vào (HTTP 422), lọc dữ liệu đầu ra (response_model)",
        "└── Kiểm thử tải  : Middleware Accounting + Depends(verify_jwt) + Kịch bản bắn tải Locust (gevent HttpUser 100-300 RPS)",
    ], inner_width=INNER_FULL)

    diagrams["0.1"] = {
        "ascii": "\n".join(
            banner("BẢN ĐỒ TƯ DUY 5 CHẶNG F04: HÀNH TRÌNH GÓI TIN ORDER #8888 QUA KIẾN TRÚC WEB API")
            + [""]
            + row_01_top
            + v_arrow("Đã có kết nối mạng và chọn đúng phong cách giao tiếp -> Bước vào Chặng 3 & 4 bảo mật và đo kiểm")
            + row_01_mid
            + v_arrow("Hiện thực hóa toàn bộ kiến trúc, bảo mật và healthcheck bằng mã nguồn FastAPI & Locust tại Chặng 5")
            + s01_c5
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 1.1: API vs Web API & OSI (7 Layers) <-> TCP/IP (4 Layers)
    # -------------------------------------------------------------------------
    s11_left = make_box([
        "[LOCAL API (GIAO DIỆN GỌI HÀM TRONG CÙNG TIẾN TRÌNH RAM)]",
        "├── Cơ chế gọi   : Nhảy con trỏ lệnh CPU (Stack Frame Call)",
        "├── Độ trễ vật lý: ~1 - 5 ns (Không qua Card mạng NIC)",
        "├── Rủi ro đứt   : Gần bằng 0 (Chung không gian địa chỉ ảo)",
        "└── Ví dụ thực tế: Gọi hàm math.sqrt() hoặc module nội bộ",
    ], inner_width=INNER_HALF)
    s11_right = make_box([
        "[WEB API (GIAO DIỆN TRUYỀN THÔNG QUA MẠNG INTERNET / LAN)]",
        "├── Cơ chế gọi   : Tuần tự hóa byte -> Socket Kernel -> Router",
        "├── Độ trễ vật lý: ~10 - 150 ms (Gấp ~10,000,000 lần Local API)",
        "├── Rủi ro đứt   : Rớt gói tin, nghẽn hàng đợi, tấn công MitM",
        "└── Ví dụ thực tế: App gọi POST /api/order-service/v1/orders",
    ], inner_width=INNER_HALF)
    row_11_top = join_horizontal([s11_left, s11_right], ["    "], {2: [" vs "]})

    s11_stack = make_box([
        "[ĐỐI CHIẾU MÔ HÌNH THAM CHIẾU OSI (7 TẦNG) <-> MÔ HÌNH THỰC CHIẾN INTERNET TCP/IP (4 TẦNG) & ĐÓNG GÓI PDU]",
        "├── Tầng 7, 6, 5 (Application + Presentation + Session) <===> [1. APPLICATION LAYER] : HTTP, TLS, DNS       | PDU: Message (Payload JSON #8888)",
        "├── Tầng 4       (Transport Layer)                      <===> [2. TRANSPORT LAYER]   : TCP (Port 443), UDP  | PDU: Segment (+20B TCP Header)",
        "├── Tầng 3       (Network Layer)                        <===> [3. INTERNET / NETWORK]: IP (IPv4 / IPv6)     | PDU: Packet  (+20B IPv4 Header)",
        "└── Tầng 2, 1    (Data Link + Physical Layer)           <===> [4. LINK LAYER]        : Ethernet, Wi-Fi, MAC | PDU: Frame   (+14B MAC + 4B FCS)",
    ], inner_width=INNER_FULL)

    diagrams["1.1"] = {
        "ascii": "\n".join(
            banner("ĐỐI CHIẾU LOCAL API VS. WEB API & ĐÓNG GÓI DỮ LIỆU QUA MÔ HÌNH OSI (7 TẦNG) <-> TCP/IP (4 TẦNG)")
            + [""]
            + row_11_top
            + v_arrow("Mỗi lệnh gọi Web API của Order #8888 phải đi qua 4 lớp bọc phong bì (Encapsulation) của ngăn xếp TCP/IP")
            + s11_stack
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 1.2: Anatomy of HTTP Request & HTTP Response (4 Components & CRLF)
    # -------------------------------------------------------------------------
    s12_req = make_box([
        "[CHIỀU ĐI: HTTP REQUEST MESSAGE (CLIENT -> SERVER)]",
        "1. Request Line  : POST /api/order-service/v1/orders HTTP/1.1",
        "                   [Method: POST] [Path: /.../orders] [Ver: 1.1]",
        "2. Request Header: Host: api.fsds.vn",
        "                   User-Agent: Mozilla/5.0 (MobileApp/2.4)",
        "                   Accept: application/json",
        "                   Authorization: Bearer eyJhbGciOiJIUzI1Ni...",
        "                   Content-Type: application/json",
        "                   Content-Length: 62",
        "3. Blank Line    : \\r\\n\\r\\n (Vách ngăn CRLF kết thúc Header)",
        "4. Request Body  : {\"order_id\":\"ORD-8888\",\"amount\":450000}",
    ], inner_width=INNER_HALF)
    s12_res = make_box([
        "[CHIỀU VỀ: HTTP RESPONSE MESSAGE (SERVER -> CLIENT)]",
        "1. Status Line   : HTTP/1.1 201 Created",
        "                   [Ver: HTTP/1.1] [Code: 201] [Phrase: Created]",
        "2. Response Hdr  : Date: Sun, 18 Oct 2026 08:30:00 GMT",
        "                   Server: uvicorn-fastapi/0.115",
        "                   ETag: \"ord-8888-v1\"",
        "                   Cache-Control: no-store",
        "                   Content-Type: application/json",
        "                   Content-Length: 54",
        "3. Blank Line    : \\r\\n\\r\\n (Vách ngăn CRLF bắt đầu dữ liệu)",
        "4. Response Body : {\"status\":\"created\",\"id\":\"ORD-8888\"}",
    ], inner_width=INNER_HALF)
    row_12 = join_horizontal([s12_req, s12_res], ["    "], {5: [" ──►"]})

    diagrams["1.2"] = {
        "ascii": "\n".join(
            banner("GIẢI PHẪU KHUNG BẢN TIN HTTP REQUEST & HTTP RESPONSE (4 THÀNH PHẦN BẮT BUỘC & VÁCH NGĂN CRLF)")
            + [""]
            + row_12
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 1.3: Anatomy of 6-Segment URL Endpoint & HTTP Methods + Status Codes
    # -------------------------------------------------------------------------
    s13_url = make_box([
        "[GIẢI PHẪU 6 PHÂN ĐOẠN CỦA MỘT HTTP ENDPOINT TRÊN BỘ ĐỊNH TUYẾN (ROUTER ANATOMY — SLIDE 18-19)]",
        "URL mẫu: http://example.com /api/superhero-service /v1 /superheroes /{id} ?fields=name,origin",
        "├── [1. Host]         : http://example.com         -> Địa chỉ tên miền hoặc IP nơi máy chủ API cư trú",
        "├── [2. Service]      : /api/superhero-service     -> Định danh microservice đích đằng sau API Gateway",
        "├── [3. API Version]  : /v1                        -> Khóa hợp đồng tương thích ngược khi nâng cấp API",
        "├── [4. Resource Type]: /superheroes (hoặc /orders)-> Danh từ số nhiều chỉ tập hợp thực thể dữ liệu",
        "├── [5. Resource ID]  : /{id} (VD: /42, /ORD-8888) -> Tham số đường dẫn (Path Param) trỏ đúng 1 bản ghi",
        "└── [6. Query String] : ?fields=name,origin        -> Cặp khóa-giá trị lọc (Filter), phân trang, sắp xếp",
    ], inner_width=INNER_FULL)

    s13_methods = make_box([
        "[5 ĐỘNG TỪ HTTP METHODS (SLIDE 13 & 20)]",
        "├── GET    : Đọc tài nguyên (Safe=Có, Idempotent=Có)",
        "├── POST   : Tạo mới bản ghi (Safe=Không, Idempotent=Không!)",
        "├── PUT    : Ghi đè toàn bộ (Safe=Không, Idempotent=Có)",
        "├── PATCH  : Cập nhật một phần (Safe=Không, Idempotent=Tùy)",
        "└── DELETE : Xóa bản ghi đích (Safe=Không, Idempotent=Có)",
    ], inner_width=INNER_HALF)
    s13_codes = make_box([
        "[5 DẢI MÃ TRẠNG THÁI HTTP STATUS CODES (SLIDE 23)]",
        "├── 1xx Informational: 100 Continue, 101 Switching Protocols",
        "├── 2xx Success      : 200 OK, 201 Created, 204 No Content",
        "├── 3xx Redirection  : 301 Moved, 304 Not Modified (Cache Hit)",
        "├── 4xx Client Error : 400 Bad, 401 Unauth, 403, 404, 422, 429",
        "└── 5xx Server Error : 500 Internal Error, 502, 503, 504 Timeout",
    ], inner_width=INNER_HALF)
    row_13_bot = join_horizontal([s13_methods, s13_codes], ["    "], {3: [" +  "]})

    diagrams["1.3"] = {
        "ascii": "\n".join(
            banner("GIẢI PHẪU 6 PHÂN ĐOẠN URL ENDPOINT & MA TRẬN TỔ HỢP HTTP METHODS + STATUS CODES")
            + [""]
            + s13_url
            + v_arrow("Endpoint chỉ là Địa chỉ Đích (Target); kết hợp với Động từ (HTTP Method) mới tạo thành Mệnh lệnh Hoàn chỉnh")
            + row_13_bot
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 1.4: DNS Recursive Lookup & TLS Encryption + SHA-256 Integrity
    # -------------------------------------------------------------------------
    s14_dns = make_box([
        "[1. PHÂN GIẢI TÊN MIỀN DNS: DANH BẠ SỐ INTERNET (SLIDE 25)]",
        "├── Bước A (Cache Search — < 1ms):",
        "│   Kiểm tra tuần tự: Browser Cache -> OS Cache -> Router Cache",
        "└── Bước B (Recursive Query khi Cache Miss — 15-80ms):",
        "    Resolver hỏi đệ quy qua 3 tầng máy chủ phân cấp:",
        "    [1. Root Server (.)] -> [2. TLD (.com)] -> [3. Authoritative]",
        "    => Trả về địa chỉ IP máy chủ: fsds_server.com = 142.250.190.78",
    ], inner_width=INNER_HALF)
    s14_tls = make_box([
        "[2. BẢO MẬT KÊNH TRUYỀN TLS: BIẾN HTTP -> HTTPS (SLIDE 24)]",
        "├── Khóa Bất đối xứng (Asymmetric: Public/Private Key):",
        "│   Dùng lúc bắt tay TLS để xác thực chứng chỉ & trao đổi khóa",
        "├── Khóa Đối xứng (Symmetric: Session Key AES-256-GCM):",
        "│   Mã hóa toàn bộ Payload Order #8888 thành Ciphertext tốc độ cao",
        "└── Toàn vẹn dữ liệu (Integrity: Hàm băm SHA-256 / HMAC):",
        "    Tạo vân tay số mỗi gói tin; kẻ tấn công MitM sửa 1 bit -> Hủy!",
    ], inner_width=INNER_HALF)
    row_14 = join_horizontal([s14_dns, s14_tls], ["    "], {3: [" ──►"]})

    diagrams["1.4"] = {
        "ascii": "\n".join(
            banner("BỘ ĐÔI BẢO HỘ TẦNG ỨNG DỤNG: PHÂN GIẢI ĐỆ QUY DNS & MÃ HÓA TOÀN VẸN TLS (HTTPS)")
            + [""]
            + row_14
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 1.5: TCP 3-Way Handshake (ISN 1000 / 5000) & TCP vs UDP
    # -------------------------------------------------------------------------
    s15_tcp = make_box([
        "[GIẢI PHẪU MÁY TRẠNG THÁI BẮT TAY 3 BƯỚC TCP (3-WAY HANDSHAKE — SLIDE 28-30)]",
        "  CLIENT (192.168.1.10)                                                   SERVER (142.250.190.78:443)",
        "  Trạng thái: CLOSED                                                      Trạng thái: LISTEN",
        "       │                                                                       │",
        "       ├── 1. Gửi gói [SYN]     : Flags=SYN, Seq=1000 (Client ISN) ───────────►│ (Chuyển sang SYN_RECEIVED)",
        "       │   (Chuyển sang SYN_SENT)                                              │",
        "       │◄── 2. Đáp trả [SYN-ACK]: Flags=SYN,ACK | Seq=5000 | Ack=1001 (ISN+1) ─┤",
        "       │                                                                       │",
        "       ├── 3. Xác nhận [ACK]    : Flags=ACK | Seq=1001 | Ack=5001 (Srv ISN+1) ►│",
        "  Trạng thái: ESTABLISHED  <====== [Bắt đầu truyền HTTP Request #8888] ======> Trạng thái: ESTABLISHED",
    ], inner_width=INNER_FULL)

    s15_c1 = make_box([
        "[TCP (TRANSMISSION CONTROL PROTOCOL — SLIDE 27)]",
        "├── Hướng kết nối (Connection-Oriented): Bắt buộc bắt tay 3 bước",
        "├── Đảm bảo giao nhận (Guaranteed)     : Tự động gửi lại khi rớt gói",
        "├── Bảo toàn thứ tự (Ordered Data)     : Sắp xếp đúng theo số Seq",
        "└── Ứng dụng: Web API (REST, gRPC, GraphQL), Database, Email",
    ], inner_width=INNER_HALF)
    s15_c2 = make_box([
        "[UDP (USER DATAGRAM PROTOCOL — SLIDE 31)]",
        "├── Phi kết nối (Connectionless)  : Bắn gói tin ngay (0 RTT Handshake)",
        "├── Giao nhận nỗ lực (Best-Effort): Rớt gói là mất luôn, không chờ ACK",
        "├── Không giữ thứ tự (No Ordering): Gói sau có thể tới trước gói đầu",
        "└── Ứng dụng: Live Video Streaming, VoIP, Gaming, DNS (UDP 53)",
    ], inner_width=INNER_HALF)
    row_15_bot = join_horizontal([s15_c1, s15_c2], ["    "], {2: [" vs "]})

    diagrams["1.5"] = {
        "ascii": "\n".join(
            banner("MÁY TRẠNG THÁI TCP 3-WAY HANDSHAKE (SEQ 1000 / 5000) & ĐỐI CHIẾU CƠ HỌC TCP VS. UDP")
            + [""]
            + s15_tcp
            + [""]
            + row_15_bot
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 1.6: End-to-End 10-Step Network Flow (LAN Switch, Router NAT, DNS, Server)
    # -------------------------------------------------------------------------
    s16_lan = make_box([
        "[MẠNG NỘI BỘ LAN (PRIVATE NETWORK — ETHERNET/MAC)]",
        "├── Client 1: IP 192.168.1.10 (Gửi GET fsds_server.com/users)",
        "├── Client 2: IP 192.168.1.11 (Cùng nhánh LAN, không nhận nhầm)",
        "├── Switch  : Chuyển mạch khung Ethernet theo địa chỉ vật lý MAC",
        "└── Router / Gateway (Biên giới LAN <-> WAN):",
        "    • Cổng LAN Private IP : 192.168.1.1",
        "    • Cổng WAN Public IP  : 203.0.113.5 (Chạy bảng dịch địa chỉ NAT)",
    ], inner_width=INNER_HALF)
    s16_wan = make_box([
        "[MẠNG DIỆN RỘNG WAN / INTERNET (ISP FIBER ROUTING)]",
        "├── Bước 1-3: Client 1 -> Switch -> Router NAT đổi IP nguồn thành",
        "│             203.0.113.5 rồi đẩy ra đường cáp quang ISP",
        "├── Bước 4-5: DNS Server (8.8.8.8) nhận truy vấn và trả về",
        "│             địa chỉ IP đích của fsds_server.com = 142.250.190.78",
        "├── Bước 6-7: Thiết lập kết nối tới FSDS Server (142.250.190.78),",
        "│             xử lý yêu cầu và gửi gói tin HTTP Response quay về",
        "└── Bước 8-10: Router tra bảng NAT -> Switch -> Giao đúng Client 1!",
    ], inner_width=INNER_HALF)
    row_16 = join_horizontal([s16_lan, s16_wan], ["    "], {3: [" ◄─►"]})

    diagrams["1.6"] = {
        "ascii": "\n".join(
            banner("TRUY VẾT 10 BƯỚC GÓI TIN THỰC TẾ QUA LAN SWITCH, ROUTER NAT (203.0.113.5), DNS (8.8.8.8) & FSDS SERVER")
            + [""]
            + row_16
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 2.1: Postman 2025 API Adoption & 4-Step REST Communication Cycle
    # -------------------------------------------------------------------------
    s21_left = make_box([
        "[TỶ LỆ ÁP DỤNG KIẾN TRÚC API (POSTMAN 2025 REPORT — SLIDE 38)]",
        "├── 1. REST          : ████████████████████████████ 93% (Mặc định)",
        "├── 2. Webhooks      : ███████████████              50% (Sự kiện)",
        "├── 3. WebSockets    : ██████████                   35% (2 chiều)",
        "├── 4. GraphQL       : █████████                    33% (Linh hoạt)",
        "├── 5. SOAP          : ███████                      25% (Legacy)",
        "├── 6. gRPC          : ████                         14% (Nhị phân)",
        "└── 7. SSE / MQTT    : ███                          12% / 8%",
    ], inner_width=INNER_HALF)
    s21_right = make_box([
        "[CHU TRÌNH 4 BƯỚC GIAO TIẾP REST API CHUẨN (SLIDE 40)]",
        "├── Bước 1 (TCP Handshake) : Thiết lập kết nối TCP 3 bước ổn định",
        "├── Bước 2 (HTTP Request)  : Client gửi động từ HTTP (POST/GET) kèm",
        "│                            Payload JSON của Order #8888",
        "├── Bước 3 (Server Logic)  : Máy chủ chạy nghiệp vụ, truy vấn CSDL",
        "│                            PostgreSQL hoặc gọi microservice khác",
        "└── Bước 4 (HTTP Response) : Trả về Status Code (200/201) + JSON",
    ], inner_width=INNER_HALF)
    row_21 = join_horizontal([s21_left, s21_right], ["    "], {3: [" ──►"]})

    diagrams["2.1"] = {
        "ascii": "\n".join(
            banner("TOÀN CẢNH HỆ SINH THÁI KIẾN TRÚC API (POSTMAN REPORT) & CHU TRÌNH 4 BƯỚC GIAO TIẾP REST")
            + [""]
            + row_21
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 2.2: The 6 Principles of REST API (Slide 41-48)
    # -------------------------------------------------------------------------
    s22_1 = make_box([
        "[1. CLIENT-SERVER SEPARATION]",
        "├── Client lo UI / trải nghiệm",
        "├── Server lo Storage / Security",
        "└── Tiến hóa độc lập không phụ thuộc",
    ], inner_width=INNER_THIRD)
    s22_2 = make_box([
        "[2. STATELESS (KHÔNG TRẠNG THÁI)]",
        "├── Server không nhớ lịch sử Client",
        "├── Mỗi Request mang đủ Token/Param",
        "└── Bất kỳ node nào sau LB đều xử lý",
    ], inner_width=INNER_THIRD)
    s22_3 = make_box([
        "[3. UNIFORM INTERFACE (ĐỒNG NHẤT)]",
        "├── Định danh tài nguyên bằng URI",
        "├── Thao tác qua động từ GET/POST...",
        "└── Bản tin tự mô tả (JSON) + Links",
    ], inner_width=INNER_THIRD)
    row_22_top = join_horizontal([s22_1, s22_2, s22_3], ["    ", "    "])

    s22_4 = make_box([
        "[4. CACHING (TĂNG TỐC PHẢN HỒI)]",
        "├── Khai báo Cache-Control / ETag",
        "├── Tái sử dụng kết quả tại Edge/Client",
        "└── Giảm tải truy vấn lặp vào DB",
    ], inner_width=INNER_THIRD)
    s22_5 = make_box([
        "[5. LAYERED SYSTEM (ĐA TẦNG)]",
        "├── Client chỉ thấy 1 điểm cuối duy nhất",
        "├── Đi ngầm qua Firewall -> API Gateway",
        "└── Gắn thêm Auth/Log không sửa Client",
    ], inner_width=INNER_THIRD)
    s22_6 = make_box([
        "[6. CODE ON DEMAND (TÙY CHỌN)]",
        "├── Server trả về mã thực thi (JS)",
        "├── VD: Script vẽ biểu đồ / tiền xử lý",
        "└── Nguyên lý duy nhất không bắt buộc",
    ], inner_width=INNER_THIRD)
    row_22_bot = join_horizontal([s22_4, s22_5, s22_6], ["    ", "    "])

    diagrams["2.2"] = {
        "ascii": "\n".join(
            banner("GIẢI PHẪU 6 NGUYÊN LÝ KIẾN TRÚC RESTFUL API (5 NGUYÊN LÝ BẮT BUỘC + 1 TÙY CHỌN — SLIDE 41-48)")
            + [""]
            + row_22_top
            + [""]
            + row_22_bot
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 2.3: REST (Over-fetching & Under-fetching) vs GraphQL (Single Round-Trip)
    # -------------------------------------------------------------------------
    s23_rest = make_box([
        "[ĐIỂM NGHẼN CỦA REST API TRÊN MÀN HÌNH PHỨC TẠP (SLIDE 49)]",
        "├── 1. Over-fetching (Lấy thừa dữ liệu):",
        "│   GET /v1/orders/ORD-8888 trả về 60 cột (45 KB JSON) trong khi",
        "│   màn hình Mobile chỉ cần 3 trường: order_id, amount, status",
        "└── 2. Under-fetching (Lấy thiếu -> N+1 vòng mạng):",
        "    Phải gọi tiếp GET /v1/users/USR-104 rồi GET /v1/shipments",
        "    => Tốn 3-4 vòng khứ hồi WAN (4 x 60ms = 240ms độ trễ)",
    ], inner_width=INNER_HALF)
    s23_gql = make_box([
        "[CƠ CHẾ ĐỒ THỊ GRAPHQL: CLIENT CHỈ ĐỊNH CHÍNH XÁC DỮ LIỆU (SLIDE 37)]",
        "├── Điểm cuối duy nhất : POST /graphql kèm cây truy vấn Query AST",
        "├── Truy vấn đúng trường: query { order(id:\"8888\") { amount user { name } } }",
        "├── Kết quả trả về     : Đúng 2 trường cần thiết trong 1 vòng mạng!",
        "└── Đánh đổi kỹ thuật  : Mất khả năng Cache URL tự động trên CDN;",
        "    cần gắn DataLoader ở Backend để gom truy vấn SQL chống lỗi N+1",
    ], inner_width=INNER_HALF)
    row_23 = join_horizontal([s23_rest, s23_gql], ["    "], {3: [" ──►"]})

    diagrams["2.3"] = {
        "ascii": "\n".join(
            banner("ĐỐI CHIẾU CƠ HỌC REST (OVER/UNDER-FETCHING) VS. GRAPHQL (TRUY VẤN ĐỒ THỊ 1 VÒNG MẠNG)")
            + [""]
            + row_23
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 2.4: gRPC & Protocol Buffers over HTTP/2 Multiplexing (Slide 50-52)
    # -------------------------------------------------------------------------
    s24_proto = make_box([
        "[1. HỢP ĐỒNG NGHIÊM NGẶT .PROTO & MÃ HÓA NHỊ PHÂN PROTOBUF]",
        "├── Định nghĩa hàm từ xa (Slide 51):",
        "│   service ModelService { rpc Predict (Input) returns (Output); }",
        "├── Gọi hàm tự nhiên trong Python:",
        "│   result = model_service.Predict(input_data)",
        "└── Mã hóa nhị phân Protocol Buffers:",
        "    Thay tên khóa chuỗi lặp lại bằng thẻ số (Field Tag 1, 2, 3) +",
        "    Varint -> Nhỏ hơn JSON 3-5 lần, giải mã nhanh hơn 5-10 lần!",
    ], inner_width=INNER_HALF)
    s24_http2 = make_box([
        "[2. ĐA LUỒNG TRÊN HTTP/2 & ĐÁNH ĐỔI KIẾN TRÚC (SLIDE 50, 52)]",
        "├── HTTP/2 Binary Framing & Multiplexing:",
        "│   Ghép hàng trăm lệnh gọi RPC song song trên 1 kết nối TCP duy nhất,",
        "│   nén Header bằng HPACK và hỗ trợ Streaming 2 chiều",
        "├── Ưu điểm cốt lõi : Độ trễ sub-millisecond giữa các Microservices",
        "└── Hạn chế (Cons)  : Trình duyệt Web không gọi trực tiếp được gRPC",
        "    (vì thiếu API kiểm soát khung nhị phân HTTP/2), cần gRPC-Web Proxy",
    ], inner_width=INNER_HALF)
    row_24 = join_horizontal([s24_proto, s24_http2], ["    "], {3: [" ──►"]})

    diagrams["2.4"] = {
        "ascii": "\n".join(
            banner("GIẢI PHẪU KIẾN TRÚC gRPC: HỢP ĐỒNG .PROTO, MÃ HÓA NHỊ PHÂN PROTOBUF & ĐA LUỒNG HTTP/2")
            + [""]
            + row_24
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 2.5: WebSocket (Full-Duplex 101 Upgrade) vs SSE (Unidirectional Stream)
    # -------------------------------------------------------------------------
    s25_ws = make_box([
        "[WEBSOCKET: SONG CÔNG TOÀN PHẦN 2 CHIỀU (SLIDE 53-57)]",
        "├── Bước 1: Client gửi HTTP GET kèm Header: Connection: Upgrade",
        "├── Bước 2: Server trả mã HTTP/1.1 101 Switching Protocols",
        "├── Bước 3: Cả Client và Server bắn khung tin 2 chiều tức thì",
        "├── Bước 4: Giữ kết nối TCP mở liên tục đến khi một bên đóng",
        "└── Đánh đổi: Khó mở rộng ngang (Stateful connections), cần",
        "    quản lý kết nối bền vững và tự viết logic kết nối lại",
    ], inner_width=INNER_HALF)
    s25_sse = make_box([
        "[SERVER-SENT EVENTS (SSE): ĐẨY LUỒNG 1 CHIỀU (SLIDE 58-59)]",
        "├── Bước 1: Client mở kết nối chuẩn HTTP (Accept: text/event-stream)",
        "├── Bước 2: Server giữ kết nối mở (Content-Type: text/event-stream)",
        "├── Bước 3: Server đẩy liên tục chuỗi sự kiện văn bản (Server -> Client):",
        "│           event: pipeline_update",
        "│           data: Job Spark ID 123 completed.",
        "└── Ưu thế: Đi xuyên Firewall dễ dàng, trình duyệt tự động kết nối",
        "    lại (Auto-reconnect) -> Chuẩn vàng cho Dashboard & LLM Streaming!",
    ], inner_width=INNER_HALF)
    row_25 = join_horizontal([s25_ws, s25_sse], ["    "], {3: [" vs "]})

    diagrams["2.5"] = {
        "ascii": "\n".join(
            banner("ĐỐI CHIẾU TRUYỀN THÔNG THỜI GIAN THỰC: WEBSOCKET (SONG CÔNG 2 CHIỀU) VS. SSE (LUỒNG ĐƠN HƯỚNG)")
            + [""]
            + row_25
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 2.6: Webhook Event-Driven Callback & 6-Architecture Decision Tree
    # -------------------------------------------------------------------------
    s26_wh = make_box([
        "[CƠ CHẾ ĐẢO CHIỀU ĐIỀU KHIỂN WEBHOOK: GIAO TIẾP SERVER-TO-SERVER HƯỚNG SỰ KIỆN (SLIDE 60-61)]",
        "  [Developer / Khách hàng] ──(1. Push code / Thanh toán #8888)──► [GitHub / Cổng Thanh Toán Stripe]",
        "                                                                           │",
        "       ┌──(2. Phát sinh sự kiện -> Tự động bắn HTTP POST Callback kèm chữ ký HMAC-SHA256)──┘",
        "       ▼",
        "  [Máy chủ Jenkins CI/CD hoặc order-api] ──(3. Xác thực chữ ký -> Trả 200 OK -> Thực thi Build/Cập nhật đơn)",
    ], inner_width=INNER_FULL)

    s26_tree = make_box([
        "[MA TRẬN QUYẾT ĐỊNH CHỌN PHONG CÁCH KIẾN TRÚC API TRÊN PRODUCTION (SLIDE 37-61)]",
        "├── Giao tiếp CRUD chuẩn cho đối tác bên ngoài, dễ cache & debug?   ──► Chọn [REST API] (JSON over HTTP)",
        "├── Giao diện Mobile/Web phức tạp cần lấy đúng trường trong 1 lượt? ──► Chọn [GraphQL]  (POST /graphql + DataLoader)",
        "├── Gọi hàm nội bộ giữa các Microservices cần độ trễ cực thấp?      ──► Chọn [gRPC]     (Protobuf + HTTP/2)",
        "├── Ứng dụng Chat / Game / Cộng tác cần trao đổi 2 chiều liên tục?  ──► Chọn [WebSocket](101 Switching Protocols)",
        "├── Bảng giám sát Live / Streaming từng token LLM (Server->Client)? ──► Chọn [SSE]      (text/event-stream)",
        "└── Thông báo sự kiện bất đồng bộ giữa 2 hệ thống (Server->Server)? ──► Chọn [Webhook]  (HTTP POST Callback)",
    ], inner_width=INNER_FULL)

    diagrams["2.6"] = {
        "ascii": "\n".join(
            banner("KIẾN TRÚC HƯỚNG SỰ KIỆN WEBHOOK (SERVER-TO-SERVER) & CÂY QUYẾT ĐỊNH 6 PHONG CÁCH API")
            + [""]
            + s26_wh
            + v_arrow("Tổng hợp quy tắc chọn lựa giữa 6 phong cách kiến trúc theo đúng bài toán kỹ thuật")
            + s26_tree
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 3.1: 6 API Security Threats & AAA Framework (Authentication, Authorization, Accounting)
    # -------------------------------------------------------------------------
    s31_threats = make_box([
        "[6 MỐI ĐE DỌA BẢO MẬT API TRÊN INTERNET (SLIDE 63)]",
        "├── 1. Unauthorized access  : Gọi trái phép vào API không có quyền",
        "├── 2. Broken authentication: Xác thực danh tính yếu, dễ giả mạo",
        "├── 3. Data exposure        : Trả dư các trường nhạy cảm (PII/Hash)",
        "├── 4. Injection attacks    : Tiêm mã độc SQL/Command vào tham số",
        "├── 5. Rate abuse (DDoS)    : Bắn phá hàng vạn RPS gây sập/đội phí",
        "└── 6. Prompt injection     : Tiêm lệnh đánh cắp điều khiển LLM API",
    ], inner_width=INNER_HALF)
    s31_aaa = make_box([
        "[KHUNG PHÒNG THỦ 3 CHỮ A: AAA FRAMEWORK (SLIDE 64-67)]",
        "├── 1. Authentication (Who are you? — Bạn là ai?):",
        "│      Xác minh danh tính bằng Username/Password + Mã MFA gửi điện thoại",
        "├── 2. Authorization  (What are you allowed to do? — Được làm gì?):",
        "│      Kiểm tra vai trò (VD: role='viewer' được Read, cấm Delete/Edit)",
        "└── 3. Accounting     (What did you actually do? — Đã làm những gì?):",
        "       Ghi nhật ký kiểm toán: 'Bob đăng nhập 10:00, tải 20MB, thoát 10:30'",
    ], inner_width=INNER_HALF)
    row_31 = join_horizontal([s31_threats, s31_aaa], ["    "], {3: [" ──►"]})

    diagrams["3.1"] = {
        "ascii": "\n".join(
            banner("BỨC TRANH 6 MỐI ĐE DỌA BẢO MẬT WEB API & KHUNG QUẢN TRỊ TRUY CẬP 3 LỚP AAA")
            + [""]
            + row_31
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 3.2: Basic Authentication (Base64 Encoding) & Plaintext Vulnerability
    # -------------------------------------------------------------------------
    s32_flow = make_box([
        "[CƠ CHẾ HOẠT ĐỘNG CỦA HTTP BASIC AUTHENTICATION (SLIDE 68-70)]",
        "  [1. Ghép thông tin gốc]       [2. Mã hóa Base64 (Không phải Encryption!)]     [3. Đính kèm vào mọi HTTP Request]",
        "   username:password     ───►    dXNlcm5hbWU6cGFzc3dvcmQ=                  ───►  GET /api/orders HTTP/1.1",
        "                                                                                 Host: api.example.com",
        "                                                                                 Authorization: Basic dXNlcm5hbWU6...",
    ], inner_width=INNER_FULL)

    s32_warn = make_box([
        "[CẢNH BÁO BẢO MẬT CỐT LÕI: BASE64 CHỈ LÀ BIỂU DIỄN KÝ TỰ, KHÔNG PHẢI MÃ HÓA MẬT MÃ (SLIDE 68 & 70)]",
        "├── Tử huyệt vật lý : Bất kỳ ai bắt được gói tin đều giải mã ngược (base64 -d) trong 1 bước để đọc mật khẩu gốc!",
        "├── Điều kiện bắt buộc: Chỉ được phép dùng Basic Auth bên trên đường hầm HTTPS (TLS) đã mã hóa toàn bộ gói tin.",
        "└── Phạm vi sử dụng : Chỉ phù hợp cho Script nội bộ hoặc công cụ ít rủi ro; CẤM dùng cho Public API (phải dùng JWT/OAuth).",
    ], inner_width=INNER_FULL)

    diagrams["3.2"] = {
        "ascii": "\n".join(
            banner("GIẢI PHẪU LUỒNG BASIC AUTHENTICATION (BASE64) & TỬ HUYỆT LỘ MẬT KHẨU KHI THIẾU TLS")
            + [""]
            + s32_flow
            + v_arrow("Máy chủ nhận Request -> Giải mã chuỗi Base64 -> Đối chiếu Username/Password trên từng Request một")
            + s32_warn
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 3.3: JWT (Header.Payload.Signature) & Stateless Verification
    # -------------------------------------------------------------------------
    s33_parts = make_box([
        "[GIẢI PHẪU 3 THÀNH PHẦN CỦA CHUỖI JSON WEB TOKEN (JWT — SLIDE 72 & 74)]",
        "Chuỗi Token: eyJhbGciOiJIUzI1NiJ9 . eyJ1c2VySWQiOiIxMjMiLCJyb2xlIjoidmlld2VyIn0 . SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
        "├── [1. HEADER (Base64URL)]  : {\"typ\": \"JWT\", \"alg\": \"HS256\"} -> Khai báo thuật toán ký số HMAC-SHA256",
        "├── [2. PAYLOAD (Base64URL)] : {\"iss\": \"https://jaypmedia.com\", \"sub\": \"user_id123\", \"exp\": 1644768000}",
        "└── [3. SIGNATURE (Chữ ký)]  : HMAC-SHA256(base64url(Header) + \".\" + base64url(Payload), secret_salt)",
    ], inner_width=INNER_FULL)

    s33_left = make_box([
        "[ƯU THẾ ĐỘT PHÁ: XÁC THỰC STATELESS 0 DB LOOKUP (SLIDE 73)]",
        "├── Client đăng nhập 1 lần -> Nhận JWT -> Gửi kèm Header:",
        "│   Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...",
        "├── Server chỉ cần tính lại chữ ký HMAC-SHA256 trên RAM (~0.02ms)",
        "└── Không cần tra cứu Database hay lưu Session trên bộ nhớ máy chủ!",
    ], inner_width=INNER_HALF)
    s33_right = make_box([
        "[ĐÁNH ĐỔI THỰC CHIẾN: BÀI TOÁN THU HỒI TOKEN (SLIDE 76)]",
        "├── Kẻ tấn công sửa Payload (viewer -> admin) -> Lệch chữ ký -> Chặn!",
        "├── Nhưng nếu lộ nguyên chuỗi JWT: Server không thể hủy trước hạn exp",
        "│   nếu không dựng thêm bộ nhớ đệm danh sách đen (Redis Blocklist)",
        "└── Giải pháp: Đặt hạn Access Token ngắn (15p) + Refresh Token",
    ], inner_width=INNER_HALF)
    row_33_bot = join_horizontal([s33_left, s33_right], ["    "], {2: [" vs "]})

    diagrams["3.3"] = {
        "ascii": "\n".join(
            banner("GIẢI PHẪU CẤU TRÚC 3 PHẦN JWT (HEADER.PAYLOAD.SIGNATURE) & XÁC THỰC KHÔNG TRẠNG THÁI")
            + [""]
            + s33_parts
            + [""]
            + row_33_bot
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 3.4: OAuth 2.0 8-Step Delegated Authorization Flow (Slide 75-76)
    # -------------------------------------------------------------------------
    s34_flow = make_box([
        "[LUỒNG ỦY QUYỀN 8 BƯỚC OAUTH 2.0 — CẤP QUYỀN TRUY CẬP KHÔNG CẦN CHIA SẺ MẬT KHẨU GỐC (SLIDE 75)]",
        "  [CLIENT APP (Bob)]                       [CONSENT / AUTH SERVER]                      [RESOURCE OWNER (User)]",
        "          │                                           │                                            │",
        "          ├── 1. Request authorization grant ────────►├── 2. Show requested scopes (Consent UI) ──►│",
        "          │◄─ 4. Grant code with scopes ──────────────┤◄─ 3. Approved scopes (Chấp thuận quyền) ───┤",
        "          │                                           │",
        "          ├── 5. Exchange grant code for token ──────►│ [AUTH SERVER xác minh Grant Code]",
        "          │◄─ 6. Trả về Access Token ─────────────────┤",
        "          │",
        "          ├── 7. Request with Access Token ──────────► [RESOURCE SERVER (order-api)]",
        "          │◄─ 8. Trả về dữ liệu Resource (#8888) ────┤",
    ], inner_width=INNER_FULL)

    s34_comp = make_box([
        "[QUY TẮC VÀNG CHỌN CƠ CHẾ XÁC THỰC (RULE OF THUMB — SLIDE 76)]",
        "├── 1. Basic Auth: Gửi user:pass (Base64) mỗi request -> Chỉ dùng cho Script nội bộ / Tool đơn giản có HTTPS",
        "├── 2. JWT Token : Ký số Stateless không cần tra DB   -> Chuẩn mực cho hệ thống Microservices & Stateless APIs",
        "└── 3. OAuth 2.0 : Ủy quyền qua bên thứ ba (Scopes)   -> Bắt buộc khi tích hợp Đăng nhập Google/GitHub hoặc cấp quyền đối tác",
    ], inner_width=INNER_FULL)

    diagrams["3.4"] = {
        "ascii": "\n".join(
            banner("LUỒNG ỦY QUYỀN 8 BƯỚC OAUTH 2.0 (CONSENT FLOW) & ĐỐI CHIẾU BASIC AUTH VS. JWT VS. OAUTH")
            + [""]
            + s34_flow
            + [""]
            + s34_comp
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 4.1: Health Check Endpoints (/liveness vs /readiness on Kubernetes)
    # -------------------------------------------------------------------------
    s41_live = make_box([
        "[1. GET /liveness — TIẾN TRÌNH CÒN SỐNG HAY ĐÃ TREO CỨNG? (SLIDE 79)]",
        "├── Phản hồi chuẩn : HTTP 200 -> {\"status\": \"alive\"}",
        "├── Khi thất bại   : Kubernetes GIẾT VÀ KHỞI ĐỘNG LẠI (Restart) Container!",
        "├── Nguyên tắc vàng: Chỉ báo lỗi /liveness khi tiến trình bị Deadlock",
        "│                    hoặc hỏng nội tại không thể tự phục hồi.",
        "└── CẤM TUYỆT ĐỐI  : Cấm kiểm tra kết nối Database trong /liveness!",
        "    (Nếu DB chập chờn 3s, K8s sẽ khởi động lại đồng loạt toàn bộ Pod!)",
    ], inner_width=INNER_HALF)
    s41_ready = make_box([
        "[2. GET /readiness — DỊCH VỤ ĐÃ SẴN SÀNG NHẬN LƯU LƯỢNG CHƯA? (SLIDE 79)]",
        "├── Phản hồi chuẩn : HTTP 200 -> {\"status\": \"ready\"}",
        "├── Khi thất bại   : K8s RÚT POD KHỎI LOAD BALANCER (Không Restart Pod!)",
        "├── Khi nào báo bận: Đang khởi động, đang chờ kết nối Database,",
        "│                    hoặc đang nạp mô hình AI/ML nặng vào bộ nhớ RAM/GPU.",
        "└── Vai trò trong ML: Bảo vệ Pod không nhận request dự báo khi trọng số",
        "    mô hình (Model Weights) chưa được nạp xong hoàn toàn vào bộ nhớ!",
    ], inner_width=INNER_HALF)
    row_41 = join_horizontal([s41_live, s41_ready], ["    "], {3: [" vs "]})

    diagrams["4.1"] = {
        "ascii": "\n".join(
            banner("GIẢI PHẪU HEALTH CHECK ENDPOINTS TRÊN KUBERNETES: PHÂN TÁCH SINH TỬ /LIVENESS VS. /READINESS")
            + [""]
            + row_41
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 4.2: 6 Key Performance Metrics & Tail Latency Distribution (p50/p95/p99)
    # -------------------------------------------------------------------------
    s42_metrics = make_box([
        "[6 CHỈ SỐ ĐO LƯỜNG HIỆU NĂNG API CỐT LÕI (SLIDE 80)]",
        "├── 1. Response Time : Thời gian phản hồi tính bằng ms",
        "├── 2. Error Rate (%) : Tỷ lệ phần trăm request thất bại (4xx/5xx)",
        "├── 3. Traffic Level : Lưu lượng truy cập mỗi giây (RPS)",
        "├── 4. Uptime        : Thời gian hệ thống hoạt động liên tục",
        "├── 5. Availability  : Phần trăm sẵn sàng (99.9% = nghỉ tối đa 8.76h/năm)",
        "└── 6. Latency (p50 / p95 / p99): Phân phối xác suất thời gian phản hồi",
    ], inner_width=INNER_HALF)
    s42_pct = make_box([
        "[TẠI SAO PHẢI ĐO PHÂN VỊ ĐỘ TRỄ p50 / p95 / p99? (SLIDE 80)]",
        "├── Bẫy Trung bình cộng: 99 request mất 10ms + 1 request kẹt khóa 5000ms",
        "│   -> Trung bình = 59.9ms (Che giấu hoàn toàn trải nghiệm tệ nhất!)",
        "├── Phân vị p50 (Median): 50% tổng số request nhanh hơn ngưỡng này (10ms)",
        "├── Phân vị p95         : 95% tổng số request nhanh hơn ngưỡng này (45ms)",
        "└── Phân vị p99 (Tail)  : 99% request nhanh hơn ngưỡng này; bắt trọn 1%",
        "    request chậm nhất (5000ms) nơi khách hàng VIP đang thanh toán!",
    ], inner_width=INNER_HALF)
    row_42 = join_horizontal([s42_metrics, s42_pct], ["    "], {3: [" ──►"]})

    diagrams["4.2"] = {
        "ascii": "\n".join(
            banner("HỆ THỐNG 6 CHỈ SỐ HIỆU NĂNG API & TOÁN HỌC PHÂN VỊ ĐỘ TRỄ ĐUÔI DÀI (p50 / p95 / p99)")
            + [""]
            + row_42
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 4.3: Load Testing Trapezoid Profile & 6 Types of Performance Testing
    # -------------------------------------------------------------------------
    s43_load = make_box([
        "[ĐỒ THỊ HÌNH THANG CỦA BÀI KIỂM THỬ TẢI CHUẨN (LOAD TESTING — SLIDE 82-83)]",
        "  Users ▲",
        "    100 │                   [═══════════════════════════════]  <-- Peak Load (Giữ 100 Users đồng thời)",
        "     80 │                  /                                 \\",
        "     40 │                 /    Đo: Response Time, RPS,        \\",
        "      0 └────────────────/________Error Rate & DB Slow_________\\────────► Thời gian (Phút)",
        "        0m (Ramp up tăng dần) 9m      (Hold giữ tải đỉnh)     15m (Ramp down) 18m",
    ], inner_width=INNER_FULL)

    s43_types = make_box([
        "[BẢN ĐỒ 6 LOẠI KIỂM THỬ HIỆU NĂNG HỆ THỐNG (6 TYPES OF PERFORMANCE TESTING — SLIDE 81)]",
        "├── 1. Load Testing    : Kiểm tra hệ thống dưới mức tải bình thường và tải đỉnh dự kiến (VD: 100 concurrent users)",
        "├── 2. Stress Testing  : Chủ động đẩy tải vượt ngưỡng tối đa để tìm điểm gãy vỡ (Breaking Point) và khả năng tự hồi phục",
        "├── 3. Spike Testing   : Đột ngột tăng vọt và giảm sốc lưu lượng trong vài giây (VD: Mở bán Flash Sale 0h00)",
        "├── 4. Soak Testing    : Duy trì tải liên tục nhiều giờ/ngày để bắt lỗi rò rỉ bộ nhớ (Memory Leak) hoặc cạn Connection Pool",
        "├── 5. Capacity Testing: Xác định trần số lượng người dùng tối đa mà hệ thống vẫn đạt cam kết SLA (p99 < 200ms)",
        "└── 6. Volume Testing  : Kiểm tra tốc độ truy vấn khi bảng dữ liệu phình to hàng trăm triệu dòng (Large Data Volume)",
    ], inner_width=INNER_FULL)

    diagrams["4.3"] = {
        "ascii": "\n".join(
            banner("ĐỒ THỊ HÌNH THANG LOAD TESTING (100 USERS) & BẢN ĐỒ 6 LOẠI KIỂM THỬ HIỆU NĂNG")
            + [""]
            + s43_load
            + [""]
            + s43_types
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 4.4: Stress Testing Breaking Point & Graceful Degradation vs Hard Failure
    # -------------------------------------------------------------------------
    s44_stress = make_box([
        "[ĐƯỜNG CONG BẺ GÃY HỆ THỐNG TRONG STRESS TESTING (SLIDE 84)]",
        "├── Mốc 0 -> 6 phút  (0 -> 100 Users)  : Vùng Normal — Hệ thống chạy êm ở ngưỡng tải thiết kế (Latency ~100ms)",
        "├── Mốc 6 -> 11 phút (100 -> 220 Users): Vùng Degrading — Bắt đầu chạm trần DB Pool; tại 220 Users độ trễ tăng vọt",
        "└── Mốc 11 -> 18 phút (280+ Users)     : Vùng Failing — Tại 280 Users (phút 14), API chạm Điểm Gãy (Breaking Point)!",
    ], inner_width=INNER_FULL)

    s44_grace = make_box([
        "[SUY THOÁI ÊM DỊU (GRACEFUL DEGRADATION — SLIDE 85)]",
        "├── Hiện tượng: Khi vượt tải, độ trễ tăng từ 100ms lên 800ms",
        "│               nhưng API vẫn tiếp tục trả kết quả thành công.",
        "├── Cơ chế bảo vệ: Giới hạn hàng đợi (Bounded Queue), cắt bớt",
        "│               tác vụ phụ, trả mã 429 Too Many Requests có kiểm soát.",
        "└── Hồi phục   : Tự động trở lại 100ms ngay khi tải giảm xuống.",
    ], inner_width=INNER_HALF)
    s44_hard = make_box([
        "[SẬP CỨNG TOÀN CỤC (HARD FAILURE — SLIDE 85)]",
        "├── Hiện tượng: Vừa chạm 150 Users là văng lỗi HTTP 500 hàng loạt",
        "│               hoặc sập chết tiến trình máy chủ (OOM / Crash).",
        "├── Nguyên nhân : Không giới hạn Connection Pool, tràn bộ nhớ RAM,",
        "│               hoặc khóa chết luồng sự kiện (Event Loop Deadlock).",
        "└── Hậu quả   : Hệ thống tê liệt hoàn toàn dù lưu lượng đã giảm!",
    ], inner_width=INNER_HALF)
    row_44_bot = join_horizontal([s44_grace, s44_hard], ["    "], {2: [" vs "]})

    diagrams["4.4"] = {
        "ascii": "\n".join(
            banner("GIẢI PHẪU ĐƯỜNG CONG STRESS TESTING (220 -> 280 USERS) & GRACEFUL DEGRADATION VS. HARD FAILURE")
            + [""]
            + s44_stress
            + [""]
            + row_44_bot
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 5.1: WSGI (Flask Synchronous Blocking) vs ASGI (FastAPI Uvicorn uvloop)
    # -------------------------------------------------------------------------
    s51_wsgi = make_box([
        "[KIẾN TRÚC ĐỒNG BỘ WSGI (FLASK / GUNICORN THREAD-PER-REQUEST)]",
        "├── Cơ chế xử lý : 1 Request chiếm cứng 1 luồng hệ điều hành (OS Thread)",
        "├── Điểm nghẽn I/O: Khi chờ PostgreSQL (50ms) + Cổng thanh toán (120ms),",
        "│                   luồng bị khóa cứng (Blocked) không nhận việc mới!",
        "└── Hệ lụy tải cao: Hết sạch Pool 32 luồng ở ~188 RPS dù CPU rảnh 90%",
    ], inner_width=INNER_HALF)
    s51_asgi = make_box([
        "[KIẾN TRÚC BẤT ĐỒNG BỘ 4 TẦNG ASGI (UVICORN + STARLETTE + FASTAPI)]",
        "├── 1. Uvicorn   : Máy chủ ASGI chạy vòng lặp Cython uvloop + httptools",
        "├── 2. Starlette : Định tuyến tốc độ cao, WebSocket, SSE & Middleware",
        "├── 3. FastAPI   : Dependency Injection (Depends) + OpenAPI 3.1 tự động",
        "└── 4. Pydantic 2: Nhân kiểm định kiểu viết bằng Rust (pydantic-core)",
    ], inner_width=INNER_HALF)
    row_51_top = join_horizontal([s51_wsgi, s51_asgi], ["    "], {2: [" ──►"]})

    s51_trap = make_box([
        "[QUY TẮC SỐNG CÒN TRONG FASTAPI: PHÂN TÁCH RẠCH RÒI HÀM BẤT ĐỒNG BỘ (async def) VÀ HÀM ĐỒNG BỘ (def)]",
        "├── Khi khai báo async def endpoint(): Chạy TRỰC TIẾP trên luồng chính Event Loop (Single-threaded uvloop).",
        "│   -> BẮT BUỘC dùng thư viện I/O bất đồng bộ có await (asyncpg, httpx.AsyncClient). Nếu gọi nhầm time.sleep()",
        "│      hoặc requests.get() đồng bộ bên trong async def, TOÀN BỘ EVENT LOOP SẼ ĐÓNG BĂNG (1000 user cùng treo)!",
        "└── Khi khai báo def endpoint() thường: FastAPI tự động đẩy hàm sang AnyIO Worker Threadpool (40 luồng phụ)",
        "    để chạy an toàn các thư viện đồng bộ cũ (psycopg2, boto3) mà không làm nghẽn vòng lặp sự kiện chính!",
    ], inner_width=INNER_FULL)

    diagrams["5.1"] = {
        "ascii": "\n".join(
            banner("ĐỐI CHIẾU KIẾN TRÚC WSGI (FLASK) VS. ASGI (FASTAPI UVLOOP) & CẠM BẪY CHẶN EVENT LOOP")
            + [""]
            + row_51_top
            + v_arrow("Hiểu cơ chế điều phối luồng của ASGI để tránh lỗi làm treo cứng máy chủ FastAPI trên Production")
            + s51_trap
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 5.2: FastAPI Middleware Pipeline, Pydantic v2 Gate & Dependency Injection
    # -------------------------------------------------------------------------
    s52_pipe = make_box([
        "[ĐƯỜNG ỐNG XỬ LÝ REQUEST ĐA LỚP TRONG FASTAPI (MIDDLEWARE -> DEPENDS -> PYDANTIC V2 -> HANDLER)]",
        "  [HTTP Request #8888] ──► [1. Middleware (CORS, Rate-Limit, Accounting Timer)]",
        "                                  │",
        "                                  ▼",
        "                           [2. Dependency Injection: Depends(verify_jwt) & Depends(get_db)]",
        "                                  │  (Nếu sai chữ ký JWT -> Trả ngay HTTP 401/403)",
        "                                  ▼",
        "                           [3. Cổng kiểm dịch Pydantic v2 (Rust pydantic-core Validation)]",
        "                                  │  (Nếu sai kiểu dữ liệu / amount <= 0 -> Trả ngay HTTP 422)",
        "                                  ▼",
        "                           [4. Route Handler xử lý nghiệp vụ -> Lọc trường nhạy cảm qua response_model]",
    ], inner_width=INNER_FULL)

    diagrams["5.2"] = {
        "ascii": "\n".join(
            banner("ĐƯỜNG ỐNG MIDDLEWARE, ĐỒ THỊ DEPENDENCY INJECTION (DEPENDS) & CỔNG KIỂM DỊCH PYDANTIC V2")
            + [""]
            + s52_pipe
        ),
        "kind": "boxes",
    }

    # -------------------------------------------------------------------------
    # 5.3: End-to-End FastAPI Multi-Architecture Service & Locust Load Testing Lab
    # -------------------------------------------------------------------------
    s53_locust = make_box([
        "[CỤM BẮN TẢI LOCUST (GEVENT GREENLETS)]",
        "├── Khởi tạo: 100 -> 300 HttpUser ảo",
        "├── @task(3): GET /v1/orders/ORD-8888",
        "├── @task(1): POST /v1/orders (Bearer JWT)",
        "└── Thu thập: RPS, p50, p95, p99, Error%",
    ], inner_width=INNER_HALF)
    s53_fastapi = make_box([
        "[TỔ HỢP DỊCH VỤ FASTAPI ĐA KIẾN TRÚC (ORDER-API)]",
        "├── 1. REST Endpoint  : POST /v1/orders (Pydantic v2 + JWT)",
        "├── 2. SSE Streaming  : GET /v1/orders/{id}/stream (Event)",
        "├── 3. Webhook Sink   : POST /webhooks/payment (HMAC-SHA256)",
        "└── 4. Health Probes  : GET /liveness & GET /readiness (ML)",
    ], inner_width=INNER_HALF)
    row_53 = join_horizontal([s53_locust, s53_fastapi], ["    "], {2: [" ──►"]})

    diagrams["5.3"] = {
        "ascii": "\n".join(
            banner("PHÒNG THÍ NGHIỆM KHÉP KÍN: CỤM BẮN TẢI LOCUST ĐO KIỂM DỊCH VỤ FASTAPI ĐA KIẾN TRÚC")
            + [""]
            + row_53
        ),
        "kind": "boxes",
    }

    for k, meta in diagrams.items():
        c_errs = verify_character_policy(meta["ascii"], f"API-{k}")
        if c_errs:
            raise SystemExit(f"ASCII character policy failed for API-{k}: {c_errs}")
        errs = verify_diagram(meta["ascii"], f"API-{k}", kind=meta["kind"])
        if errs:
            raise SystemExit(f"ASCII verification failed for API-{k} ({meta['kind']}): {errs}")
    return diagrams


API_SIM2D_JS = r"""
  /* ==========================================================================
     F04 · WEB API 2D INTERACTIVE SIMULATOR (CLAUDE ACADEMY CDS THEME)
     ========================================================================== */
  const API2D_SLIDES = [
    {
      id: 1,
      chapter: "Chặng 1 · Ngăn Xếp Mạng 4 Tầng TCP/IP & NAT",
      analogy: "4 Lớp Phong Bì, Bắt Tay 3 Bước & Bảng Dịch NAT",
      title: "Hành Trình Gói Tin Order #8888 Qua DNS, TCP 3-Way Handshake, TLS & Router NAT",
      leadTitle: "Tại sao một lệnh gọi POST /v1/orders mất 45ms trong khi gọi hàm Python nội bộ chỉ mất 2ns?",
      leadStory: "Khi ứng dụng tại Client (192.168.1.10) gửi Order #8888 tới máy chủ (142.250.190.78:443), gói tin phải phân giải tên miền qua DNS (8.8.8.8), dịch địa chỉ IP nội bộ sang IP công cộng (203.0.113.5) tại Router NAT, hoàn tất bắt tay 3 bước TCP (SYN Seq=1000 → SYN-ACK Seq=5000, Ack=1001 → ACK=5001) và thỏa thuận khóa phiên TLS trước khi byte JSON đầu tiên rời card mạng.",
      keypoints: [
        { b: "1", t: "Đóng Gói 4 Tầng TCP/IP (PDU Encapsulation)", d: "Application (HTTP Message + TLS + DNS) → Transport (TCP Segment +20B) → Network (IP Packet +20B) → Link (Ethernet Frame +18B MAC)." },
        { b: "2", t: "Bắt Tay 3 Bước TCP (Connection-Oriented)", d: "Đồng bộ số thứ tự gói tin (ISN 1000 & 5000) để chuyển trạng thái từ CLOSED → SYN_SENT → SYN_RECEIVED → ESTABLISHED, cam kết không mất gói." },
        { b: "3", t: "Router NAT & Phân Giải Đệ Quy DNS", d: "Router ánh xạ 192.168.1.10 sang Public IP 203.0.113.5 trong bảng NAT để khi máy chủ trả HTTP 201 Created, gói tin quay về đúng Client 1." }
      ],
      verdict: "Web API đánh đổi độ trễ mạng (RTT) và chi phí bắt tay TCP/TLS để đổi lấy sự tách biệt hoàn toàn giữa giao diện Client và tài nguyên máy chủ.",
      simMode: "netstack"
    },
    {
      id: 2,
      chapter: "Chặng 2 · Đối Chiếu REST vs. GraphQL vs. gRPC",
      analogy: "Thực Đơn Cố Định vs. Tự Chọn Món vs. Đường Ống Nhị Phân",
      title: "Ba Kiến Trúc Request–Response: Khi Nào Dùng REST (93%), GraphQL (33%) Hay gRPC (14%)?",
      leadTitle: "Làm sao khắc phục lỗi lấy thừa dữ liệu (Over-fetching) của REST và tăng tốc 10x giao tiếp nội bộ?",
      leadStory: "REST API thống trị 93% hệ thống nhờ tính đơn giản và tận dụng trọn vẹn HTTP Caching, nhưng dễ gây Over-fetching (trả về 45KB JSON khi Mobile chỉ cần 3 trường) hoặc Under-fetching (4 vòng mạng liên tiếp). GraphQL gom truy vấn vào 1 vòng mạng duy nhất qua Query AST, còn gRPC nén nhị phân Protobuf chạy đa luồng trên HTTP/2 cho các Microservices nội bộ.",
      keypoints: [
        { b: "1", t: "REST API (JSON over HTTP — 6 Nguyên Lý)", d: "Stateless, Uniform Interface (URI + HTTP Verbs GET/POST/PUT/DELETE) và Cacheable (ETag / 304). Chuẩn mực cho Public API." },
        { b: "2", t: "GraphQL (Client-Specified Query AST)", d: "Client gửi truy vấn đồ thị tới POST /graphql để lấy đúng các trường lồng nhau trong 1 RTT, kết hợp DataLoader chống lỗi N+1 SQL." },
        { b: "3", t: "gRPC & Protocol Buffers (HTTP/2 Binary)", d: "Định nghĩa hợp đồng .proto (rpc Predict), mã hóa thành thẻ số nhị phân nhỏ hơn JSON 3–5 lần, ghép kênh đa luồng không nghẽn." }
      ],
      verdict: "Chọn REST cho cổng Public API cần Cache/CDN, GraphQL cho ứng dụng Frontend đa thiết bị, và gRPC cho giao tiếp Microservices / ML Serving nội bộ.",
      simMode: "reqres"
    },
    {
      id: 3,
      chapter: "Chặng 2 · WebSocket vs. SSE vs. Webhook",
      analogy: "Bộ Đàm 2 Chiều vs. Loa Phát Thanh 1 Chiều vs. Chuông Báo Tự Động",
      title: "Ba Kiến Trúc Thời Gian Thực & Hướng Sự Kiện: Xóa Bỏ Vòng Lặp Hỏi Thăm (Polling) Lãng Phí",
      leadTitle: "Tại sao SSE là chuẩn vàng cho LLM Token Streaming còn Webhook thống trị tích hợp Server-to-Server?",
      leadStory: "Nếu Client hỏi thăm (Polling) mỗi giây để kiểm tra trạng thái Order #8888, 99% băng thông bị đốt vào HTTP Header rỗng. WebSocket nâng cấp kết nối (HTTP 101) thành đường ống 2 chiều liên tục; Server-Sent Events (SSE) đẩy luồng văn bản 1 chiều qua HTTP chuẩn kèm tự động kết nối lại; còn Webhook đảo chiều để Server tự bắn HTTP POST sang hệ thống đối tác ngay khi sự kiện nổ ra.",
      keypoints: [
        { b: "1", t: "WebSocket (Full-Duplex 101 Switching Protocols)", d: "Nâng cấp từ HTTP/1.1 lên kênh TCP song công bền vững, cho phép cả Client và Server bắn tin nhắn 2 chiều tức thì (Chat, Game)." },
        { b: "2", t: "Server-Sent Events (SSE — text/event-stream)", d: "Luồng đẩy đơn hướng Server → Client trên HTTP chuẩn, đi xuyên Firewall dễ dàng và tích hợp sẵn Auto-Reconnect (Dashboard, LLM)." },
        { b: "3", t: "Webhook (Event-Driven Server-to-Server Callback)", d: "GitHub hoặc cổng thanh toán chủ động gọi HTTP POST tới URL đăng ký sẵn kèm chữ ký HMAC-SHA256 khi có sự kiện mới." }
      ],
      verdict: "Chỉ dùng WebSocket khi thực sự cần đối thoại 2 chiều liên tục; ưu tiên SSE cho luồng cập nhật 1 chiều về trình duyệt và Webhook cho thông báo liên máy chủ.",
      simMode: "realtime"
    },
    {
      id: 4,
      chapter: "Chặng 3 · Bảo Mật AAA, Basic Auth, JWT & OAuth 2.0",
      analogy: "Thẻ Căn Cước Tự Chứa Chữ Ký Số & Ủy Quyền Không Lộ Mật Khẩu",
      title: "Giải Phẫu Khung Phòng Thủ AAA, Bẫy Base64 Basic Auth, Chữ Ký JWT & Luồng 8 Bước OAuth 2.0",
      leadTitle: "Làm sao xác thực hàng vạn RPS mà không cần chọc vào Database kiểm tra Session trên mỗi Request?",
      leadStory: "Basic Auth ghép username:password rồi mã hóa Base64 — kẻ nghe lén giải mã ngược trong 1 bước nếu thiếu HTTPS! JWT giải quyết triệt để bằng chuỗi 3 phần Header.Payload.Signature ký bằng HMAC-SHA256 giúp máy chủ xác thực trên RAM trong 0.02ms (0 DB Lookup). Khi cần cấp quyền cho ứng dụng thứ ba mà không lộ mật khẩu gốc, OAuth 2.0 thực thi luồng 8 bước qua Authorization Server.",
      keypoints: [
        { b: "1", t: "Khung AAA (Authentication → Authorization → Accounting)", d: "Xác minh danh tính (MFA) → Kiểm tra quyền hạn theo vai trò (RBAC: viewer cấm DELETE) → Ghi nhật ký kiểm toán chống chối bỏ." },
        { b: "2", t: "JWT (Header.Payload.Signature — Stateless)", d: "Chứa sẵn user_id, role, exp. Nếu kẻ gian sửa role='viewer' thành 'admin', chữ ký HMAC-SHA256 lệch ngay lập tức (HTTP 401)." },
        { b: "3", t: "OAuth 2.0 (8-Step Delegated Authorization)", d: "Tách bạch Resource Owner, Client, Auth Server và Resource Server; trao đổi Authorization Code + PKCE lấy Access Token giới hạn theo Scopes." }
      ],
      verdict: "Dùng Basic Auth (trên nền HTTPS) cho script nội bộ, JWT hạn ngắn (15 phút) + Refresh Token cho Stateless API, và OAuth 2.0 cho đăng nhập liên kết / đối tác.",
      simMode: "security"
    },
    {
      id: 5,
      chapter: "Chặng 4 · Probes (/liveness, /readiness) & Load / Stress Testing",
      analogy: "Nhịp Tim Sống Còn vs. Đèn Báo Sẵn Sàng & Điểm Gãy Chịu Tải",
      title: "Phân Tách Sinh Tử /liveness Với /readiness Trên Kubernetes & Đường Cong Suy Thoái Êm Dịu",
      leadTitle: "Tại sao kiểm tra kết nối Database bên trong /liveness lại gây ra bão khởi động lại toàn cụm?",
      leadStory: "Trên Kubernetes, nếu /liveness thất bại, Kubelet lập tức giết và khởi động lại Container; nếu /readiness thất bại, Pod chỉ tạm thời được rút khỏi Load Balancer để nạp xong mô hình ML 2.4GB hoặc chờ DB hồi phục. Khi bắn tải Stress Testing vượt ngưỡng 100 lên 220 và 280 Users, một API tốt phải suy thoái êm dịu (100ms → 800ms) thay vì sập cứng HTTP 500.",
      keypoints: [
        { b: "1", t: "/liveness (Chống Treo) vs. /readiness (Chờ Sẵn Sàng)", d: "Cấm kiểm tra DB trong /liveness! Phải đặt kiểm tra DB Pool và cờ nạp Model ML trong /readiness để bảo vệ Pod lúc khởi động." },
        { b: "2", t: "Phân Vị Độ Trễ Đuôi Dài (p50 / p95 / p99)", d: "Trung bình cộng che giấu thảm họa: 99 request 10ms + 1 request 5000ms có trung bình 59.9ms nhưng p99 vọt lên 5000ms." },
        { b: "3", t: "Load Testing (100 Users) vs. Stress Testing (280 Users)", d: "Load Testing giữ tải ở mức kỳ vọng; Stress Testing ép qua ngưỡng 220 Users (Degrading) tới 280 Users (Failing) để kiểm tra khả năng tự hồi phục." }
      ],
      verdict: "Luôn tách riêng 2 đầu đo /liveness và /readiness, giám sát chặt p99 thay vì trung bình cộng, và thiết kế hàng đợi giới hạn để đạt Graceful Degradation.",
      simMode: "resilience"
    },
    {
      id: 6,
      chapter: "Chặng 5 · Động Cơ FastAPI ASGI, Pydantic v2 & Locust",
      analogy: "Vòng Lặp Sự Kiện Đơn Luồng uvloop & Cổng Kiểm Dịch Rust",
      title: "Giải Phẫu Ngăn Xếp FastAPI 4 Tầng (Uvicorn → Starlette → FastAPI → Pydantic v2) & Bẫy async def",
      leadTitle: "Tại sao viết nhầm 1 lệnh đồng bộ bên trong hàm async def lại làm đóng băng 1.000 người dùng cùng lúc?",
      leadStory: "Khác với Flask (WSGI khóa cứng 1 luồng OS cho mỗi request đang chờ I/O), FastAPI chạy trên vòng lặp sự kiện bất đồng bộ Uvicorn (uvloop) kết hợp nhân kiểm định Pydantic v2 viết bằng Rust. Tuy nhiên, nếu lập trình viên gọi hàm chặn đồng bộ (time.sleep, requests.get) bên trong async def, luồng Event Loop duy nhất bị khóa cứng làm p99 nổ tung!",
      keypoints: [
        { b: "1", t: "Phân Tách Rạch Ròi async def vs. def Thường", d: "Dùng async def cho thư viện có await (asyncpg, httpx); dùng def thường cho thư viện đồng bộ để FastAPI đẩy sang AnyIO Worker Threadpool (40 luồng)." },
        { b: "2", t: "Pydantic v2 (HTTP 422) & Dependency Injection", d: "Chặn dữ liệu bẩn ngay tại cổng với tốc độ Rust (pydantic-core), lọc trường nhạy cảm qua response_model và tái sử dụng xác thực qua Depends()." },
        { b: "3", t: "Đo Kiểm Tự Động Bằng Locust (gevent HttpUser)", d: "Mô phỏng hàng trăm người dùng đồng thời bằng greenlets nhẹ để đo chính xác RPS, p50, p95, p99 trước khi đưa lên Production." }
      ],
      verdict: "Sức mạnh của FastAPI nằm ở sự kết hợp giữa vòng lặp bất đồng bộ uvloop không bị chặn, kiểm định kiểu chặt chẽ bằng Pydantic v2 và kiểm thử tải Locust định kỳ.",
      simMode: "fastapi"
    }
  ];

  let api2dCurrentSlide = 0;
  const api2dState = {
    netMode: "handshake",
    archMode: "rest",
    rtMode: "sse",
    secMode: "jwt",
    resMode: "readiness",
    fapiMode: "asgi_clean"
  };

  function buildApi2DSimulatorHtml() {
    return `
      <div class="infra2d-wrap" id="api2dWidgetRoot">
        <div class="infra2d-header">
          <div class="infra2d-brand">
            <div class="infra2d-brand-icon">2D</div>
            <div>
              <div class="infra2d-brand-badges">
                <span class="infra2d-tag">Cắt Lớp Kiến Trúc &amp; Giao Thức Web API 2D</span>
                <span class="infra2d-chapter" id="api2dChapterBadge">Chặng 1 · Ngăn Xếp Mạng 4 Tầng TCP/IP &amp; NAT</span>
              </div>
              <h4 class="infra2d-title-bar">Phòng Thí Nghiệm Tương Tác F04: Hành Trình Gói Tin Order #8888 Qua 6 Kiến Trúc API &amp; Động Cơ FastAPI</h4>
            </div>
          </div>
          <div class="infra2d-dots" id="api2dDots"></div>
          <button type="button" class="infra2d-btn" onclick="toggleApi2DSummaryModal()">Bảng Tóm Tắt Thông Số</button>
        </div>

        <div id="api2dSummaryDrawer" style="display:none;padding:14px 16px;background:var(--sim-canvas);border-bottom:1px solid var(--sim-border);">
          <div style="padding:10px 12px;border-radius:8px;background:var(--sim-flow-soft);border:1px solid color-mix(in oklab, var(--sim-flow) 35%, transparent);font-size:12.5px;color:var(--sim-flow);margin-bottom:10px;">
            <strong>Chuẩn kiến trúc F04 (Web API Engineering):</strong> Nắm vững ngăn xếp <strong>TCP/IP 4 tầng</strong>, lựa chọn chính xác giữa <strong>6 phong cách kiến trúc (REST, GraphQL, gRPC, WebSocket, SSE, Webhook)</strong>, bảo vệ bằng <strong>AAA + JWT/OAuth 2.0</strong>, tách biệt <strong>/liveness vs. /readiness</strong> và vận hành trên <strong>FastAPI ASGI + Pydantic v2</strong>.
          </div>
          <div class="table-wrap" style="margin:0;">
            <table class="clean-table">
              <thead>
                <tr>
                  <th>Lớp Kiến Trúc</th>
                  <th>Cơ Chế Cốt Lõi</th>
                  <th>Thông Số &amp; Quy Chuẩn Thực Chiến</th>
                  <th>Cạm Bẫy Sinh Tử Cần Tránh</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>1. TCP/IP &amp; HTTP</strong></td>
                  <td><code>DNS → TCP 3-Way → TLS → HTTP</code></td>
                  <td><code>SYN(1000) → SYN-ACK(5000,1001) → ACK(5001)</code></td>
                  <td>Gọi lại <code>POST</code> không có <code>Idempotency-Key</code> gây nhân đôi đơn hàng</td>
                </tr>
                <tr>
                  <td><strong>2. 6 Kiến Trúc API</strong></td>
                  <td><code>REST / GraphQL / gRPC / WS / SSE / Webhook</code></td>
                  <td>REST 93%, Webhook 50%, WS 35%, GraphQL 33%, gRPC 14%</td>
                  <td>Dùng Polling thay vì SSE/Webhook hoặc gọi gRPC trực tiếp từ Browser</td>
                </tr>
                <tr>
                  <td><strong>3. Bảo Mật API</strong></td>
                  <td><code>AAA + Basic Auth / JWT / OAuth 2.0</code></td>
                  <td><code>Header.Payload.Signature</code> (HMAC-SHA256, <code>0 DB Lookup</code>)</td>
                  <td>Dùng Basic Auth qua HTTP thường hoặc đặt hạn JWT quá dài không thể thu hồi</td>
                </tr>
                <tr>
                  <td><strong>4. Probes &amp; FastAPI</strong></td>
                  <td><code>/liveness</code>, <code>/readiness</code>, <code>uvloop + Pydantic v2</code></td>
                  <td><code>p99 &lt; 200ms</code>, Graceful Degradation, tách <code>async def</code> vs <code>def</code></td>
                  <td>Kiểm tra DB trong <code>/liveness</code> hoặc gọi hàm đồng bộ chặn trong <code>async def</code></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="infra2d-grid">
          <div class="infra2d-col-left">
            <div>
              <div class="infra2d-pills">
                <span class="infra2d-pill-num" id="api2dSlideNumPill">SLIDE 1 / 6</span>
                <span class="infra2d-pill-analogy" id="api2dAnalogyPill">Lát Cắt Kiến Trúc</span>
              </div>
              <h3 class="infra2d-slide-h3" id="api2dSlideTitle"></h3>
              <div class="infra2d-story-box">
                <div class="infra2d-avatar" title="Dịch vụ order-api (#8888)">API</div>
                <div>
                  <span class="infra2d-story-title" id="api2dLeadTitle"></span>
                  <p class="infra2d-story-text" id="api2dLeadStory"></p>
                </div>
              </div>
              <div class="infra2d-keypoints" id="api2dKeypoints"></div>
            </div>
            <div class="infra2d-verdict" id="api2dVerdictBox"></div>
          </div>

          <div class="infra2d-col-right">
            <div>
              <div class="infra2d-sim-top">
                <div class="infra2d-sim-live">
                  <span class="infra2d-sim-dot"></span>
                  <span>Sơ Đồ Cắt Lớp Kiến Trúc API &amp; Luồng Gói Tin Chuyển Động (Animated SVG)</span>
                </div>
                <span class="infra2d-sim-hint">Bấm các nút kịch bản bên dưới để đối chiếu cơ chế!</span>
              </div>
              <div class="infra2d-stage" id="api2dSimStage" style="padding:10px;"></div>
            </div>
            <div>
              <div class="infra2d-status" id="api2dSimStatusText">Sẵn sàng mô phỏng.</div>
              <div class="infra2d-controls" id="api2dSimControls"></div>
            </div>
          </div>
        </div>

        <div class="infra2d-footer">
          <button type="button" class="infra2d-btn" id="api2dBtnPrev" onclick="changeApi2DSlide(-1)">← Mô Phỏng Trước</button>
          <div class="infra2d-progress-wrap">
            <div class="infra2d-progress-track">
              <div class="infra2d-progress-fill" id="api2dProgressFill" style="width:16.6%;"></div>
            </div>
            <span style="font-size:11px;color:var(--sim-muted);">Chọn 1 trong 6 lát cắt kiến trúc Web API (1–6) hoặc bấm nút điều khiển để so sánh trực tiếp</span>
          </div>
          <button type="button" class="infra2d-btn infra2d-btn-primary" id="api2dBtnNext" onclick="changeApi2DSlide(1)">Mô Phỏng Tiếp Theo →</button>
        </div>
      </div>
    `;
  }

  function toggleApi2DSummaryModal() {
    const d = document.getElementById("api2dSummaryDrawer");
    if (!d) return;
    d.style.display = (d.style.display === "none" || !d.style.display) ? "block" : "none";
  }

  function changeApi2DSlide(delta) {
    const next = api2dCurrentSlide + delta;
    if (next < 0 || next >= API2D_SLIDES.length) return;
    api2dCurrentSlide = next;
    renderApi2DSlide();
  }

  function jumpApi2DSlide(idx) {
    if (idx < 0 || idx >= API2D_SLIDES.length) return;
    api2dCurrentSlide = idx;
    renderApi2DSlide();
  }

  function renderApi2DSlide() {
    const root = document.getElementById("api2dWidgetRoot");
    if (!root) return;
    const slide = API2D_SLIDES[api2dCurrentSlide] || API2D_SLIDES[0];

    document.getElementById("api2dChapterBadge").textContent = slide.chapter;
    document.getElementById("api2dSlideNumPill").textContent = `SLIDE ${slide.id} / ${API2D_SLIDES.length}`;
    document.getElementById("api2dAnalogyPill").textContent = slide.analogy;
    document.getElementById("api2dSlideTitle").textContent = slide.title;
    document.getElementById("api2dLeadTitle").textContent = slide.leadTitle;
    document.getElementById("api2dLeadStory").textContent = slide.leadStory;

    const kpEl = document.getElementById("api2dKeypoints");
    kpEl.innerHTML = slide.keypoints.map(kp => `
      <div class="infra2d-kp-item">
        <div class="infra2d-kp-badge">${escapeHtml(kp.b)}</div>
        <div>
          <span class="infra2d-kp-title">${escapeHtml(kp.t)}</span>
          <p class="infra2d-kp-desc">${escapeHtml(kp.d)}</p>
        </div>
      </div>
    `).join("");

    document.getElementById("api2dVerdictBox").textContent = slide.verdict;

    const dotsEl = document.getElementById("api2dDots");
    dotsEl.innerHTML = API2D_SLIDES.map((s, idx) => `
      <button type="button" class="infra2d-dot-btn ${idx === api2dCurrentSlide ? 'active' : ''}" onclick="jumpApi2DSlide(${idx})">${s.id}</button>
    `).join("");

    const prevBtn = document.getElementById("api2dBtnPrev");
    const nextBtn = document.getElementById("api2dBtnNext");
    if (prevBtn) prevBtn.disabled = (api2dCurrentSlide === 0);
    if (nextBtn) nextBtn.disabled = (api2dCurrentSlide === API2D_SLIDES.length - 1);

    const fillEl = document.getElementById("api2dProgressFill");
    if (fillEl) fillEl.style.width = `${((api2dCurrentSlide + 1) / API2D_SLIDES.length) * 100}%`;

    renderApi2DInteractiveStage(slide.simMode);
  }

  function renderApi2DInteractiveStage(mode) {
    const stage = document.getElementById("api2dSimStage");
    const status = document.getElementById("api2dSimStatusText");
    const ctrls = document.getElementById("api2dSimControls");
    if (!stage || !status || !ctrls) return;

    if (mode === "netstack") {
      const m = api2dState.netMode; // 'handshake' | 'nat_dns' | 'udp_fast'
      const isHs = (m === "handshake");
      const isNat = (m === "nat_dns");
      const isUdp = (m === "udp_fast");

      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 250" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="12" y="14" width="155" height="222" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="22" y="32" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">1. CLIENT LAN (192.168.1.10)</text>
          <rect x="22" y="42" width="135" height="44" rx="6" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.2"/>
          <text x="30" y="58" fill="var(--sim-ink)" font-size="9.5" font-weight="700">L7: HTTP + TLS + DNS</text>
          <text x="30" y="74" fill="var(--sim-flow)" font-size="8.5" font-family="var(--cds-font-mono)">POST /v1/orders (#8888)</text>
          <rect x="22" y="94" width="135" height="44" rx="6" fill="var(--sim-card)" stroke="${isUdp ? 'var(--sim-warn)' : 'var(--sim-ok)'}" stroke-width="1.4"/>
          <text x="30" y="110" fill="var(--sim-ink)" font-size="9.5" font-weight="700">L4: ${isUdp ? 'UDP (Best-Effort)' : 'TCP (Guaranteed)'}</text>
          <text x="30" y="126" fill="${isUdp ? 'var(--sim-warn)' : 'var(--sim-ok)'}" font-size="8.5" font-family="var(--cds-font-mono)">${isUdp ? '0-RTT (Không bắt tay)' : 'SYN Seq=1000 → ACK=5001'}</text>
          <rect x="22" y="146" width="135" height="76" rx="6" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.2"/>
          <text x="30" y="164" fill="var(--sim-ink)" font-size="9.5" font-weight="700">L3 IP &amp; L2 Ethernet</text>
          <text x="30" y="181" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">Src IP: 192.168.1.10</text>
          <text x="30" y="197" fill="var(--sim-muted)" font-size="8.5" font-family="var(--cds-font-mono)">Switch MAC Forwarding</text>
          <text x="30" y="213" fill="var(--sim-ok)" font-size="8.5" font-family="var(--cds-font-mono)">State: ${isUdp ? 'STATELESS' : 'ESTABLISHED'}</text>

          <rect x="195" y="14" width="165" height="222" rx="8" fill="var(--sim-canvas)" stroke="${isNat ? 'var(--sim-clay)' : 'var(--sim-border)'}" stroke-width="1.5"/>
          <text x="205" y="32" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">2. ROUTER NAT &amp; DNS</text>
          <rect x="205" y="42" width="145" height="78" rx="6" fill="var(--sim-card)" stroke="var(--sim-clay)" stroke-width="1.4"/>
          <text x="213" y="59" fill="var(--sim-ink)" font-size="9.5" font-weight="700">Router Gateway (NAT)</text>
          <text x="213" y="76" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">LAN: 192.168.1.1</text>
          <text x="213" y="92" fill="var(--sim-clay)" font-size="8.5" font-weight="700" font-family="var(--cds-font-mono)">WAN: 203.0.113.5</text>
          <text x="213" y="108" fill="var(--sim-ok)" font-size="8.3" font-family="var(--cds-font-mono)">Bảng NAT định tuyến về Client 1</text>
          <rect x="205" y="132" width="145" height="90" rx="6" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.3"/>
          <text x="213" y="150" fill="var(--sim-ink)" font-size="9.5" font-weight="700">DNS Server (8.8.8.8)</text>
          <text x="213" y="167" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">Root (.) → TLD (.com)</text>
          <text x="213" y="183" fill="var(--sim-flow)" font-size="8.5" font-family="var(--cds-font-mono)">→ Authoritative NS</text>
          <text x="213" y="201" fill="var(--sim-ok)" font-size="8.5" font-weight="700" font-family="var(--cds-font-mono)">IP = 142.250.190.78</text>

          <rect x="388" y="14" width="160" height="222" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-ok)" stroke-width="1.6"/>
          <text x="398" y="32" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">3. FSDS SERVER (:443)</text>
          <rect x="398" y="42" width="140" height="82" rx="6" fill="var(--sim-ok-soft)" stroke="var(--sim-ok)" stroke-width="1.4"/>
          <text x="406" y="60" fill="var(--sim-ink)" font-size="9.5" font-weight="700">IP: 142.250.190.78</text>
          <text x="406" y="77" fill="var(--sim-ok)" font-size="8.5" font-family="var(--cds-font-mono)">${isHs ? 'SYN-ACK: Seq=5000, Ack=1001' : 'TLS AES-256 + SHA-256'}</text>
          <text x="406" y="94" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">Router: /v1/orders</text>
          <text x="406" y="111" fill="var(--sim-ok)" font-size="8.5" font-weight="700" font-family="var(--cds-font-mono)">HTTP/1.1 201 Created</text>
          <rect x="398" y="136" width="140" height="86" rx="6" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.2"/>
          <text x="406" y="154" fill="var(--sim-ink)" font-size="9.5" font-weight="700">Bảo Toàn Toàn Vẹn TLS</text>
          <text x="406" y="171" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">Asymmetric: Trao đổi khóa</text>
          <text x="406" y="187" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">Symmetric: Mã hóa Payload</text>
          <text x="406" y="204" fill="var(--sim-flow)" font-size="8.5" font-family="var(--cds-font-mono)">SHA-256: Chống sửa 1 bit</text>

          <path d="M 167 110 L 205 82" stroke="var(--sim-flow)" stroke-width="2.2" class="ing2d-flow-active"/>
          <circle r="4.5" fill="var(--sim-flow)"><animateMotion dur="1.0s" repeatCount="indefinite" path="M 167 110 L 205 82"/></circle>
          <path d="M 350 82 L 398 82" stroke="var(--sim-ok)" stroke-width="2.4" class="ing2d-flow-active"/>
          <circle r="5" fill="var(--sim-ok)"><animateMotion dur="1.1s" repeatCount="indefinite" path="M 350 82 L 398 82"/></circle>
        </svg>
        <div class="ing2d-metrics-strip">
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Giao Thức L4</span><span class="ing2d-metric-val">${isUdp ? 'UDP (Best-Effort)' : 'TCP 3-Way Handshake'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Số Thứ Tự TCP</span><span class="ing2d-metric-val">${isUdp ? 'Không có Seq/Ack' : 'ISN 1000 ↔ 5000'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Dịch Địa Chỉ NAT</span><span class="ing2d-metric-val">192.168.1.10 → 203.0.113.5</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Bảo Mật L7</span><span class="ing2d-metric-val" style="color:var(--sim-ok)">TLS + SHA-256</span></div>
        </div>
      `;

      if (isHs) {
        status.innerHTML = `<strong style="color:var(--sim-ok);">[1. Máy trạng thái Bắt tay 3 bước TCP (Slide 28–30)]:</strong> Client gửi <code>SYN (Seq=1000)</code> chuyển sang <code>SYN_SENT</code>; Server đáp trả <code>SYN-ACK (Seq=5000, Ack=1001)</code> chuyển sang <code>SYN_RECEIVED</code>; Client chốt <code>ACK (Ack=5001)</code> đưa cả hai vào trạng thái <code>ESTABLISHED</code> trước khi truyền <code>Order #8888</code>.`;
      } else if (isNat) {
        status.innerHTML = `<strong style="color:var(--sim-flow);">[2. Luồng 10 bước qua Switch, Router NAT &amp; DNS (Slide 35)]:</strong> Router đổi IP nguồn nội bộ <code>192.168.1.10</code> thành IP công cộng <code>203.0.113.5</code> (NAT), hỏi <code>DNS 8.8.8.8</code> để tìm ra <code>142.250.190.78</code>, và dùng bảng NAT để giao gói tin phản hồi về đúng <code>Client 1</code>!`;
      } else {
        status.innerHTML = `<strong style="color:var(--sim-warn);">[3. Đối chiếu UDP Phi kết nối (Slide 31)]:</strong> UDP bắn dữ liệu đi ngay mà không tốn 1 vòng bắt tay 3 bước, nhưng nếu rớt gói tin trên đường cáp quang, gói tin mất vĩnh viễn và không đảm bảo thứ tự (chỉ hợp với Video Streaming/VoIP, không hợp cho giao dịch <code>Order #8888</code>).`;
      }

      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${isHs ? 'infra2d-btn-emerald' : ''}" onclick="api2dState.netMode='handshake';renderApi2DInteractiveStage('netstack')">1. TCP 3-Way Handshake (Seq 1000/5000) + TLS</button>
        <button type="button" class="infra2d-btn ${isNat ? 'infra2d-btn-cyan' : ''}" onclick="api2dState.netMode='nat_dns';renderApi2DInteractiveStage('netstack')">2. Luồng 10 Bước: LAN Switch → Router NAT → DNS</button>
        <button type="button" class="infra2d-btn ${isUdp ? 'infra2d-btn-amber' : ''}" onclick="api2dState.netMode='udp_fast';renderApi2DInteractiveStage('netstack')">3. Đối chiếu UDP (Connectionless / Best-Effort)</button>
      `;
    } else if (mode === "reqres") {
      const m = api2dState.archMode; // 'rest' | 'graphql' | 'grpc'
      const isRest = (m === "rest");
      const isGql = (m === "graphql");
      const isGrpc = (m === "grpc");

      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 250" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="16" width="150" height="218" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="24" y="36" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">1. API CLIENT</text>
          <rect x="24" y="48" width="130" height="76" rx="6" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.4"/>
          <text x="32" y="66" fill="var(--sim-ink)" font-size="9.5" font-weight="700">${isGrpc ? 'Internal Microservice' : 'Mobile / Web App'}</text>
          <text x="32" y="84" fill="var(--sim-flow)" font-size="8.5" font-family="var(--cds-font-mono)">${isRest ? 'GET /v1/orders/8888' : (isGql ? 'POST /graphql (AST)' : 'model_service.Predict()')}</text>
          <text x="32" y="102" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">${isRest ? '3 vòng gọi liên tiếp' : 'Đúng 1 vòng gọi mạng'}</text>
          <rect x="24" y="136" width="130" height="82" rx="6" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.2"/>
          <text x="32" y="155" fill="var(--sim-ink)" font-size="9.5" font-weight="700">Đặc tính Client</text>
          <text x="32" y="173" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">${isGrpc ? 'Cần gRPC-Web cho Browser' : 'Hỗ trợ mọi trình duyệt'}</text>
          <text x="32" y="191" fill="var(--sim-ok)" font-size="8.5" font-family="var(--cds-font-mono)">${isRest ? 'Tận dụng HTTP Cache/ETag' : (isGql ? 'Chống Over-fetching 100%' : 'Nhị phân Protobuf siêu gọn')}</text>

          <rect x="196" y="16" width="168" height="218" rx="8" fill="var(--sim-canvas)" stroke="${isGrpc ? 'var(--sim-ok)' : 'var(--sim-flow)'}" stroke-width="1.6"/>
          <text x="206" y="36" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">2. KÊNH TRUYỀN &amp; PAYLOAD</text>
          <rect x="206" y="48" width="148" height="82" rx="6" fill="var(--sim-card)" stroke="var(--sim-clay)" stroke-width="1.4"/>
          <text x="214" y="66" fill="var(--sim-ink)" font-size="9.5" font-weight="700">${isGrpc ? 'HTTP/2 Binary Framing' : 'HTTP/1.1 hoặc HTTP/2 Text'}</text>
          <text x="214" y="84" fill="var(--sim-clay)" font-size="8.5" font-family="var(--cds-font-mono)">${isGrpc ? 'Protocol Buffers (.proto)' : 'Định dạng văn bản JSON'}</text>
          <text x="214" y="102" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">Kích thước: ${isRest ? '45.2 KB (Dư 57 cột)' : (isGql ? '0.18 KB (Đúng 3 cột)' : '0.06 KB (Binary Tags)')}</text>
          <rect x="206" y="140" width="148" height="78" rx="6" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.2"/>
          <text x="214" y="158" fill="var(--sim-ink)" font-size="9.5" font-weight="700">Đánh Đổi Kỹ Thuật</text>
          <text x="214" y="176" fill="${isRest ? 'var(--sim-warn)' : 'var(--sim-sub)'}" font-size="8.5" font-family="var(--cds-font-mono)">${isRest ? 'Over/Under-fetching' : (isGql ? 'Khó Cache CDN trên POST' : 'Không đọc trực tiếp bằng mắt')}</text>
          <text x="214" y="194" fill="var(--sim-ok)" font-size="8.5" font-family="var(--cds-font-mono)">Tỷ lệ dùng: ${isRest ? '93% (Postman)' : (isGql ? '33% (Postman)' : '14% (Postman)')}</text>

          <rect x="396" y="16" width="150" height="218" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-ok)" stroke-width="1.5"/>
          <text x="406" y="36" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">3. BACKEND SERVER</text>
          <rect x="406" y="48" width="130" height="170" rx="6" fill="var(--sim-ok-soft)" stroke="var(--sim-ok)" stroke-width="1.4"/>
          <text x="414" y="68" fill="var(--sim-ink)" font-size="9.5" font-weight="700">${isRest ? 'REST Resource Router' : (isGql ? 'GraphQL Schema + DataLoader' : 'gRPC Stub ModelService')}</text>
          <text x="414" y="88" fill="var(--sim-ok)" font-size="8.5" font-family="var(--cds-font-mono)">${isRest ? 'Stateless + Layered' : (isGql ? 'Resolve đúng trường yêu cầu' : 'rpc Predict(Input)→Output')}</text>
          <text x="414" y="108" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">CPU Parse: ${isGrpc ? '0.08 ms (Zero-overhead)' : '1.40 ms (UTF-8 JSON)'}</text>
          <text x="414" y="128" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">Tổng RTT: ${isRest ? '180 ms (3 calls)' : (isGql ? '60 ms (1 call)' : '1.2 ms (Internal LAN)')}</text>

          <path d="M 164 86 L 206 86" stroke="var(--sim-flow)" stroke-width="2.4" class="ing2d-flow-active"/>
          <circle r="4.8" fill="var(--sim-flow)"><animateMotion dur="0.9s" repeatCount="indefinite" path="M 164 86 L 206 86"/></circle>
          <path d="M 354 86 L 406 86" stroke="var(--sim-ok)" stroke-width="2.4" class="ing2d-flow-active"/>
          <circle r="4.8" fill="var(--sim-ok)"><animateMotion dur="0.9s" repeatCount="indefinite" path="M 354 86 L 406 86"/></circle>
        </svg>
        <div class="ing2d-metrics-strip">
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Kiến Trúc</span><span class="ing2d-metric-val">${isRest ? 'REST API (93%)' : (isGql ? 'GraphQL (33%)' : 'gRPC (14%)')}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Định Dạng</span><span class="ing2d-metric-val">${isGrpc ? 'Binary Protobuf' : 'Text JSON'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Kích Thước Gói</span><span class="ing2d-metric-val">${isRest ? '45.2 KB (Over-fetch)' : (isGql ? '0.18 KB (Exact)' : '0.06 KB (Binary)')}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Độ Trễ Toàn Trình</span><span class="ing2d-metric-val" style="color:var(--sim-ok)">${isRest ? '180 ms (3 RTT)' : (isGql ? '60 ms (1 RTT)' : '1.2 ms (HTTP/2)')}</span></div>
        </div>
      `;

      if (isRest) {
        status.innerHTML = `<strong style="color:var(--sim-flow);">[1. REST API — Chuẩn mực cho Public API (Slide 39–49)]:</strong> Dựa trên 6 nguyên lý (Client-Server, Stateless, Uniform Interface, Caching, Layered, Code on Demand). Rất dễ hiểu và tận dụng tốt HTTP Caching, nhưng dễ bị <strong>Over-fetching</strong> (trả dư trường) hoặc <strong>Under-fetching</strong> (nhiều vòng gọi mạng).`;
      } else if (isGql) {
        status.innerHTML = `<strong style="color:var(--sim-clay);">[2. GraphQL — Truy vấn Linh hoạt từ Client (Slide 37, 49)]:</strong> Client chỉ định chính xác những trường cần lấy trong 1 lần gọi <code>POST /graphql</code> duy nhất, xóa sổ hoàn toàn Over-fetching và Under-fetching cho giao diện Mobile/Dashboard phức tạp.`;
      } else {
        status.innerHTML = `<strong style="color:var(--sim-ok);">[3. gRPC &amp; Protocol Buffers — Tốc độ Nhị phân Nội bộ (Slide 50–52)]:</strong> Thay vì gửi văn bản JSON nặng nề, gRPC đóng gói nhị phân theo hợp đồng <code>.proto</code> và truyền đa luồng trên <code>HTTP/2</code>, giúp <code>order-api</code> gọi hàm <code>model_service.Predict(input_data)</code> với độ trễ chỉ ~1.2ms!`;
      }

      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${isRest ? 'infra2d-btn-cyan' : ''}" onclick="api2dState.archMode='rest';renderApi2DInteractiveStage('reqres')">1. REST API (JSON, 6 Nguyên lý, Over/Under-fetching)</button>
        <button type="button" class="infra2d-btn ${isGql ? 'infra2d-btn-amber' : ''}" onclick="api2dState.archMode='graphql';renderApi2DInteractiveStage('reqres')">2. GraphQL (Truy vấn đúng trường trong 1 RTT)</button>
        <button type="button" class="infra2d-btn ${isGrpc ? 'infra2d-btn-emerald' : ''}" onclick="api2dState.archMode='grpc';renderApi2DInteractiveStage('reqres')">3. gRPC (Protobuf Binary + HTTP/2 Multiplexing)</button>
      `;
    } else if (mode === "realtime") {
      const m = api2dState.rtMode; // 'websocket' | 'sse' | 'webhook'
      const isWs = (m === "websocket");
      const isSse = (m === "sse");
      const isWh = (m === "webhook");

      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 250" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="16" width="160" height="218" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="24" y="36" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">1. ${isWh ? 'RECEIVER SERVER' : 'BROWSER / CLIENT APP'}</text>
          <rect x="24" y="48" width="140" height="82" rx="6" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.3"/>
          <text x="32" y="66" fill="var(--sim-ink)" font-size="9.5" font-weight="700">${isWs ? 'WebSocket Client (Bob)' : (isSse ? 'Dashboard / LLM UI' : 'Jenkins / order-api')}</text>
          <text x="32" y="84" fill="var(--sim-flow)" font-size="8.5" font-family="var(--cds-font-mono)">${isWs ? 'Connection: Upgrade' : (isSse ? 'EventSource (/stream)' : 'Mở cổng POST /webhook')}</text>
          <text x="32" y="102" fill="var(--sim-ok)" font-size="8.5" font-family="var(--cds-font-mono)">${isWs ? 'Gửi & Nhận 2 chiều tức thì' : (isSse ? 'Auto-reconnect tự động!' : 'Không cần Polling (0% rác)')}</text>
          <rect x="24" y="140" width="140" height="78" rx="6" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.2"/>
          <text x="32" y="158" fill="var(--sim-ink)" font-size="9.5" font-weight="700">Trạng Thái Kết Nối</text>
          <text x="32" y="176" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">${isWh ? 'Chỉ mở khi có sự kiện' : 'Persistent Long-Lived'}</text>
          <text x="32" y="194" fill="var(--sim-muted)" font-size="8.5" font-family="var(--cds-font-mono)">${isWs ? 'Cần Sticky LB / Redis PubSub' : 'Thân thiện Proxy & Firewall'}</text>

          <rect x="200" y="16" width="160" height="218" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-clay)" stroke-width="1.5"/>
          <text x="210" y="36" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">2. GIAO THỨC TRUYỀN</text>
          <rect x="210" y="48" width="140" height="170" rx="6" fill="var(--sim-card)" stroke="var(--sim-clay)" stroke-width="1.4"/>
          <text x="218" y="68" fill="var(--sim-ink)" font-size="9.5" font-weight="700">${isWs ? 'HTTP 101 Switching' : (isSse ? 'HTTP text/event-stream' : 'Reverse HTTP POST')}</text>
          <text x="218" y="88" fill="var(--sim-clay)" font-size="8.5" font-family="var(--cds-font-mono)">Hướng: ${isWs ? 'Song công (Client ↔ Server)' : 'Đơn hướng (Server → Đích)'}</text>
          <text x="218" y="108" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">${isWs ? 'Frame nhị phân/text 2-14B' : (isSse ? 'event: pipeline_update' : 'X-Hub-Signature-256')}</text>
          <text x="218" y="128" fill="var(--sim-ok)" font-size="8.5" font-family="var(--cds-font-mono)">${isWs ? 'Độ trễ ~1-2ms hai chiều' : (isSse ? 'data: Job Spark 123 done' : 'Idempotency + Retry Backoff')}</text>

          <rect x="386" y="16" width="160" height="218" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-ok)" stroke-width="1.5"/>
          <text x="396" y="36" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">3. EVENT PRODUCER SERVER</text>
          <rect x="396" y="48" width="140" height="170" rx="6" fill="var(--sim-ok-soft)" stroke="var(--sim-ok)" stroke-width="1.4"/>
          <text x="404" y="68" fill="var(--sim-ink)" font-size="9.5" font-weight="700">${isWh ? 'GitHub / Stripe Server' : 'Streaming Server'}</text>
          <text x="404" y="88" fill="var(--sim-ok)" font-size="8.5" font-family="var(--cds-font-mono)">${isWs ? 'Đẩy & Nhận khung tin' : (isSse ? 'Đẩy luồng sự kiện liên tục' : 'Phát hiện sự kiện Push/Pay')}</text>
          <text x="404" y="108" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">Ứng dụng: ${isWs ? 'Chat, Game, Collaborative' : (isSse ? 'Live Logs, LLM Streaming' : 'CI/CD Build, Payment Sync')}</text>

          <path d="M 386 95 L 174 95" stroke="var(--sim-ok)" stroke-width="2.4" class="ing2d-flow-active"/>
          <circle r="5" fill="var(--sim-ok)"><animateMotion dur="1.0s" repeatCount="indefinite" path="M 386 95 L 174 95"/></circle>
          ${isWs ? `
            <path d="M 174 125 L 386 125" stroke="var(--sim-flow)" stroke-width="2.4" class="ing2d-flow-active"/>
            <circle r="5" fill="var(--sim-flow)"><animateMotion dur="1.0s" repeatCount="indefinite" path="M 174 125 L 386 125"/></circle>
          ` : ""}
        </svg>
        <div class="ing2d-metrics-strip">
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Cơ Chế</span><span class="ing2d-metric-val">${isWs ? 'WebSocket (35%)' : (isSse ? 'SSE (12%)' : 'Webhook (50%)')}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Chiều Dữ Liệu</span><span class="ing2d-metric-val">${isWs ? '2 Chiều (Full-Duplex)' : '1 Chiều (Server Push)'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Đối Tượng Nhận</span><span class="ing2d-metric-val">${isWh ? 'Server / Microservice' : 'Browser / Mobile App'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Tự Kết Nối Lại</span><span class="ing2d-metric-val" style="color:var(--sim-ok)">${isSse ? 'Tích hợp sẵn (Browser)' : (isWs ? 'Tự lập trình thêm' : 'Sender Retry Backoff')}</span></div>
        </div>
      `;

      if (isWs) {
        status.innerHTML = `<strong style="color:var(--sim-flow);">[1. WebSocket — Song công 2 chiều liên tục (Slide 53–57)]:</strong> Khởi đầu bằng <code>Connection: Upgrade</code> và phản hồi <code>101 Switching Protocols</code>. Cả Client và Server đều có thể bắn tin nhắn bất kỳ lúc nào, nhưng đòi hỏi quản lý kết nối Stateful phức tạp khi mở rộng cụm.`;
      } else if (isSse) {
        status.innerHTML = `<strong style="color:var(--sim-ok);">[2. Server-Sent Events (SSE) — Đẩy 1 chiều nhẹ nhàng qua HTTP (Slide 58–59)]:</strong> Dùng chuẩn <code>Content-Type: text/event-stream</code> để đẩy thông báo, trạng thái pipeline (<code>Job Spark ID 123 completed</code>) hoặc từng token LLM về trình duyệt kèm cơ chế tự động kết nối lại khi rớt mạng!`;
      } else {
        status.innerHTML = `<strong style="color:var(--sim-clay);">[3. Webhook — Giao tiếp Hướng sự kiện Server-to-Server (Slide 60–61)]:</strong> Khác với WebSocket/SSE đẩy về trình duyệt đang mở, Webhook cho phép một hệ thống (như GitHub khi có <code>git push</code> hoặc cổng thanh toán) tự động bắn <code>HTTP POST</code> sang máy chủ Jenkins / <code>order-api</code>!`;
      }

      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${isWs ? 'infra2d-btn-cyan' : ''}" onclick="api2dState.rtMode='websocket';renderApi2DInteractiveStage('realtime')">1. WebSocket (101 Switching · 2 Chiều)</button>
        <button type="button" class="infra2d-btn ${isSse ? 'infra2d-btn-emerald' : ''}" onclick="api2dState.rtMode='sse';renderApi2DInteractiveStage('realtime')">2. Server-Sent Events (SSE · 1 Chiều + Auto-Reconnect)</button>
        <button type="button" class="infra2d-btn ${isWh ? 'infra2d-btn-amber' : ''}" onclick="api2dState.rtMode='webhook';renderApi2DInteractiveStage('realtime')">3. Webhook (Server-to-Server Callback)</button>
      `;
    } else if (mode === "security") {
      const m = api2dState.secMode; // 'basic' | 'jwt' | 'oauth'
      const isBasic = (m === "basic");
      const isJwt = (m === "jwt");
      const isOauth = (m === "oauth");

      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 250" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="16" width="160" height="218" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="24" y="36" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">1. CLIENT CREDENTIAL</text>
          <rect x="24" y="48" width="140" height="170" rx="6" fill="var(--sim-card)" stroke="${isBasic ? 'var(--sim-warn)' : 'var(--sim-flow)'}" stroke-width="1.4"/>
          <text x="32" y="68" fill="var(--sim-ink)" font-size="9.5" font-weight="700">${isBasic ? 'Basic Auth (Base64)' : (isJwt ? 'JWT Bearer Token' : 'OAuth 2.0 Client App')}</text>
          <text x="32" y="88" fill="var(--sim-flow)" font-size="8.3" font-family="var(--cds-font-mono)">${isBasic ? 'dXNlcm5hbWU6cGFzc3dvcmQ=' : (isJwt ? 'Header.Payload.Signature' : '1. Xin Authorization Code')}</text>
          <text x="32" y="108" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">${isBasic ? 'Gửi user:pass mỗi request!' : (isJwt ? 'Đăng nhập 1 lần, giữ Token' : 'Không hề biết mật khẩu User!')}</text>
          <text x="32" y="128" fill="${isBasic ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="8.5" font-weight="700" font-family="var(--cds-font-mono)">${isBasic ? '[!] Base64 KHÔNG PHẢI mã hóa' : '✓ Không truyền mật khẩu lặp lại'}</text>

          <rect x="198" y="16" width="164" height="218" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-clay)" stroke-width="1.5"/>
          <text x="208" y="36" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">2. XÁC MINH &amp; ỦY QUYỀN</text>
          <rect x="208" y="48" width="144" height="170" rx="6" fill="var(--sim-card)" stroke="var(--sim-clay)" stroke-width="1.4"/>
          <text x="216" y="68" fill="var(--sim-ink)" font-size="9.5" font-weight="700">${isBasic ? 'Decode Base64 + Tra DB' : (isJwt ? 'Kiểm tra Chữ ký HMAC-SHA256' : 'Consent Flow (8 Bước)')}</text>
          <text x="216" y="88" fill="var(--sim-clay)" font-size="8.5" font-family="var(--cds-font-mono)">${isBasic ? 'Tốn I/O tra bảng users' : (isJwt ? '0 DB Lookup (100% trên RAM)' : 'User duyệt Scopes trên Auth Srv')}</text>
          <text x="216" y="108" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">${isBasic ? 'Bắt buộc chạy trên HTTPS' : (isJwt ? 'Sửa 1 bit Payload → Lệch chữ ký' : 'Đổi Grant Code → Access Token')}</text>
          <text x="216" y="128" fill="var(--sim-ok)" font-size="8.5" font-family="var(--cds-font-mono)">AAA: AuthN → AuthZ → Audit</text>

          <rect x="386" y="16" width="160" height="218" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-ok)" stroke-width="1.5"/>
          <text x="396" y="36" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">3. RESOURCE SERVER</text>
          <rect x="396" y="48" width="140" height="170" rx="6" fill="var(--sim-ok-soft)" stroke="var(--sim-ok)" stroke-width="1.4"/>
          <text x="404" y="68" fill="var(--sim-ink)" font-size="9.5" font-weight="700">order-api (/v1/orders)</text>
          <text x="404" y="88" fill="var(--sim-ok)" font-size="8.5" font-family="var(--cds-font-mono)">RBAC: role = "viewer"</text>
          <text x="404" y="108" fill="var(--sim-ok)" font-size="8.5" font-family="var(--cds-font-mono)">✓ GET /orders → 200 OK</text>
          <text x="404" y="128" fill="var(--sim-danger)" font-size="8.5" font-family="var(--cds-font-mono)">✗ DELETE /orders → 403 Deny</text>
          <text x="404" y="148" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">Accounting: Ghi Audit Log</text>

          <path d="M 174 96 L 208 96" stroke="var(--sim-flow)" stroke-width="2.4" class="ing2d-flow-active"/>
          <circle r="4.8" fill="var(--sim-flow)"><animateMotion dur="0.9s" repeatCount="indefinite" path="M 174 96 L 208 96"/></circle>
          <path d="M 352 96 L 396 96" stroke="var(--sim-ok)" stroke-width="2.4" class="ing2d-flow-active"/>
          <circle r="4.8" fill="var(--sim-ok)"><animateMotion dur="0.9s" repeatCount="indefinite" path="M 352 96 L 396 96"/></circle>
        </svg>
        <div class="ing2d-metrics-strip">
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Phương Thức</span><span class="ing2d-metric-val">${isBasic ? 'Basic Auth (Base64)' : (isJwt ? 'JWT (Signed Token)' : 'OAuth 2.0 (Delegated)')}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Tra Cứu DB / Req</span><span class="ing2d-metric-val">${isJwt ? '0 lần (Stateless RAM)' : '1 lần / Introspection'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Điểm Mạnh Nhất</span><span class="ing2d-metric-val">${isBasic ? 'Cực kỳ đơn giản' : (isJwt ? 'Mở rộng ngang dễ dàng' : 'Ủy quyền không lộ Pass')}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Điểm Yếu Cần Lưu Ý</span><span class="ing2d-metric-val" style="color:var(--sim-warn)">${isBasic ? 'Gửi Pass mỗi Request' : (isJwt ? 'Cần Blocklist để hủy sớm' : 'Luồng 8 bước phức tạp')}</span></div>
        </div>
      `;

      if (isBasic) {
        status.innerHTML = `<strong style="color:var(--sim-warn);">[1. Basic Authentication (Slide 68–70)]:</strong> Đóng gói <code>username:password</code> bằng Base64 trong mỗi Request. Vì Base64 giải mã ngược tức thì, Basic Auth bắt buộc phải đi trên <code>HTTPS (TLS)</code> và chỉ nên dùng cho script/công cụ nội bộ.`;
      } else if (isJwt) {
        status.innerHTML = `<strong style="color:var(--sim-ok);">[2. JSON Web Token — JWT Stateless (Slide 71–74)]:</strong> Gồm 3 phần <code>Header.Payload.Signature</code> ngăn cách bởi dấu chấm. Máy chủ chỉ cần kiểm tra chữ ký <code>HMAC-SHA256</code> bằng khóa bí mật mà không cần chạm vào Database hay lưu Session!`;
      } else {
        status.innerHTML = `<strong style="color:var(--sim-flow);">[3. OAuth 2.0 — Ủy quyền 8 bước qua Consent Flow (Slide 75–76)]:</strong> Cho phép người dùng (Resource Owner) cấp quyền giới hạn theo <code>Scopes</code> cho ứng dụng thứ ba (Client) thông qua <code>Authorization Server</code> mà không bao giờ phải tiết lộ mật khẩu gốc.`;
      }

      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${isBasic ? 'infra2d-btn-amber' : ''}" onclick="api2dState.secMode='basic';renderApi2DInteractiveStage('security')">1. Basic Auth (Base64 username:password)</button>
        <button type="button" class="infra2d-btn ${isJwt ? 'infra2d-btn-emerald' : ''}" onclick="api2dState.secMode='jwt';renderApi2DInteractiveStage('security')">2. JWT (Header.Payload.Signature · 0 DB Lookup)</button>
        <button type="button" class="infra2d-btn ${isOauth ? 'infra2d-btn-cyan' : ''}" onclick="api2dState.secMode='oauth';renderApi2DInteractiveStage('security')">3. OAuth 2.0 (Luồng Ủy Quyền 8 Bước)</button>
      `;
    } else if (mode === "resilience") {
      const m = api2dState.resMode; // 'readiness' | 'graceful' | 'hard_fail'
      const isRdy = (m === "readiness");
      const isGrc = (m === "graceful");
      const isHrd = (m === "hard_fail");

      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 250" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="16" width="165" height="218" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="24" y="36" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">1. K8S &amp; TRAFFIC LOAD</text>
          <rect x="24" y="48" width="145" height="170" rx="6" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.3"/>
          <text x="32" y="68" fill="var(--sim-ink)" font-size="9.5" font-weight="700">${isRdy ? 'Khởi động Pod ML Mới' : (isGrc ? 'Stress Test: 220 Users' : 'Stress Test: 280 Users')}</text>
          <text x="32" y="88" fill="var(--sim-flow)" font-size="8.5" font-family="var(--cds-font-mono)">GET /liveness → ${isHrd ? '500 FAIL!' : '200 ALIVE'}</text>
          <text x="32" y="108" fill="${isRdy ? 'var(--sim-warn)' : 'var(--sim-ok)'}" font-size="8.5" font-family="var(--cds-font-mono)">GET /readiness → ${isRdy ? '503 LOADING' : '200 READY'}</text>
          <text x="32" y="128" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">Tải kỳ vọng: 100 Users</text>
          <text x="32" y="148" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">Tải hiện tại: ${isRdy ? '0 RPS (Chờ)' : (isGrc ? '220 Users (Degrading)' : '280 Users (Breaking!)')}</text>

          <rect x="202" y="16" width="165" height="218" rx="8" fill="var(--sim-canvas)" stroke="${isHrd ? 'var(--sim-danger)' : 'var(--sim-ok)'}" stroke-width="1.6"/>
          <text x="212" y="36" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">2. HÀNH ĐỘNG ĐIỀU PHỐI</text>
          <rect x="212" y="48" width="145" height="170" rx="6" fill="${isHrd ? 'var(--sim-danger-soft)' : 'var(--sim-card)'}" stroke="${isHrd ? 'var(--sim-danger)' : 'var(--sim-clay)'}" stroke-width="1.4"/>
          <text x="220" y="68" fill="var(--sim-ink)" font-size="9.5" font-weight="700">${isRdy ? 'Rút Pod khỏi Load Balancer' : (isGrc ? 'Suy thoái Êm dịu (Graceful)' : 'Sập Cứng (Hard Failure!)')}</text>
          <text x="220" y="88" fill="${isHrd ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="8.5" font-family="var(--cds-font-mono)">${isRdy ? 'KHÔNG Restart Container!' : (isGrc ? 'Chậm lại: 100ms → 800ms' : 'Văng lỗi HTTP 500 hàng loạt!')}</text>
          <text x="220" y="108" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">${isRdy ? 'Chờ nạp xong Model 2.4GB' : (isGrc ? 'Vẫn trả kết quả thành công' : 'CrashLoopBackOff toàn cụm')}</text>

          <rect x="390" y="16" width="156" height="218" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="400" y="36" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">3. CHỈ SỐ P50 / P95 / P99</text>
          <rect x="400" y="48" width="136" height="170" rx="6" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.3"/>
          <text x="408" y="68" fill="var(--sim-ink)" font-size="9.5" font-weight="700">Phân Bố Độ Trễ</text>
          <text x="408" y="88" fill="var(--sim-ok)" font-size="8.5" font-family="var(--cds-font-mono)">p50: ${isRdy ? '18 ms' : (isGrc ? '240 ms' : 'Timeout')}</text>
          <text x="408" y="108" fill="var(--sim-warn)" font-size="8.5" font-family="var(--cds-font-mono)">p95: ${isRdy ? '42 ms' : (isGrc ? '610 ms' : 'HTTP 500')}</text>
          <text x="408" y="128" fill="${isHrd ? 'var(--sim-danger)' : 'var(--sim-clay)'}" font-size="8.5" font-weight="700" font-family="var(--cds-font-mono)">p99: ${isRdy ? '85 ms' : (isGrc ? '800 ms' : '5000+ ms (Sập)')}</text>
          <text x="408" y="148" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">Error Rate: ${isHrd ? '64.5%' : '0.0%'}</text>

          <path d="M 179 96 L 212 96" stroke="${isHrd ? 'var(--sim-danger)' : 'var(--sim-ok)'}" stroke-width="2.4" class="ing2d-flow-active"/>
          <path d="M 357 96 L 400 96" stroke="${isHrd ? 'var(--sim-danger)' : 'var(--sim-flow)'}" stroke-width="2.4" class="ing2d-flow-active"/>
        </svg>
        <div class="ing2d-metrics-strip">
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">/liveness Probe</span><span class="ing2d-metric-val">${isHrd ? '500 (Restart Storm!)' : '200 OK (Alive)'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">/readiness Probe</span><span class="ing2d-metric-val">${isRdy ? '503 (Đang nạp Model)' : '200 OK (Ready)'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Độ Trễ p99</span><span class="ing2d-metric-val">${isRdy ? '85 ms' : (isGrc ? '800 ms (Graceful)' : 'Timeout / Crash')}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Trạng Thái Hệ Thống</span><span class="ing2d-metric-val" style="color:${isHrd ? 'var(--sim-danger)' : 'var(--sim-ok)'}">${isHrd ? 'Hard Failure (Sập cứng)' : 'An toàn & Tự hồi phục'}</span></div>
        </div>
      `;

      if (isRdy) {
        status.innerHTML = `<strong style="color:var(--sim-ok);">[1. Chuẩn Kubernetes cho Hệ thống AI/ML (Slide 79)]:</strong> Khi Pod đang nạp mô hình gian lận 2.4GB vào RAM, <code>/liveness</code> trả <code>200</code> (để K8s không giết Pod) trong khi <code>/readiness</code> trả <code>503</code> (để Load Balancer tạm ngưng gửi request cho tới khi nạp xong 100%).`;
      } else if (isGrc) {
        status.innerHTML = `<strong style="color:var(--sim-flow);">[2. Suy thoái Êm dịu — Graceful Degradation (Slide 84–85)]:</strong> Khi Stress Testing đẩy tải vượt ngưỡng 100 lên 220 Users, độ trễ tăng từ <code>100ms</code> lên <code>800ms</code> nhưng hệ thống vẫn phản hồi ổn định và tự động hồi phục ngay khi tải hạ xuống.`;
      } else {
        status.innerHTML = `<strong style="color:var(--sim-danger);">[3. Thảm họa Sập cứng — Hard Failure (Slide 79 &amp; 85)]:</strong> Đặt kiểm tra DB trong <code>/liveness</code> kèm không giới hạn Connection Pool khiến ngay khi chạm ngưỡng quá tải, các Pod vừa trả lỗi <code>HTTP 500</code> vừa bị K8s khởi động lại dây chuyền!`;
      }

      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${isRdy ? 'infra2d-btn-emerald' : ''}" onclick="api2dState.resMode='readiness';renderApi2DInteractiveStage('resilience')">1. Chuẩn K8s: /readiness Chờ Nạp Model ML</button>
        <button type="button" class="infra2d-btn ${isGrc ? 'infra2d-btn-cyan' : ''}" onclick="api2dState.resMode='graceful';renderApi2DInteractiveStage('resilience')">2. Stress Test: Graceful Degradation (100ms → 800ms)</button>
        <button type="button" class="infra2d-btn ${isHrd ? 'infra2d-btn-danger' : ''}" onclick="api2dState.resMode='hard_fail';renderApi2DInteractiveStage('resilience')">3. Lỗi Thiết Kế: Hard Failure &amp; Restart Storm</button>
      `;
    } else {
      const m = api2dState.fapiMode; // 'asgi_clean' | 'event_block' | 'wsgi_sync'
      const isClean = (m === "asgi_clean");
      const isBlock = (m === "event_block");
      const isWsgi = (m === "wsgi_sync");

      stage.innerHTML = `
        <svg class="ing2d-svg-stage" viewBox="0 0 560 250" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="14" y="16" width="160" height="218" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="24" y="36" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">1. LOCUST TRAFFIC</text>
          <rect x="24" y="48" width="140" height="170" rx="6" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.3"/>
          <text x="32" y="68" fill="var(--sim-ink)" font-size="9.5" font-weight="700">Locust (gevent Users)</text>
          <text x="32" y="88" fill="var(--sim-flow)" font-size="8.5" font-family="var(--cds-font-mono)">300 Concurrent Users</text>
          <text x="32" y="108" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">Middleware: Accounting</text>
          <text x="32" y="128" fill="var(--sim-ok)" font-size="8.5" font-family="var(--cds-font-mono)">Pydantic v2 (Rust Gate)</text>
          <text x="32" y="148" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">Depends(verify_jwt)</text>

          <rect x="198" y="16" width="168" height="218" rx="8" fill="var(--sim-canvas)" stroke="${isBlock ? 'var(--sim-danger)' : 'var(--sim-ok)'}" stroke-width="1.6"/>
          <text x="208" y="36" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">2. ĐỘNG CƠ THỰC THI</text>
          <rect x="208" y="48" width="148" height="170" rx="6" fill="${isBlock ? 'var(--sim-danger-soft)' : 'var(--sim-card)'}" stroke="${isBlock ? 'var(--sim-danger)' : 'var(--sim-clay)'}" stroke-width="1.4"/>
          <text x="216" y="68" fill="var(--sim-ink)" font-size="9.5" font-weight="700">${isWsgi ? 'WSGI (Flask 32 Threads)' : 'ASGI (Uvicorn uvloop)'}</text>
          <text x="216" y="88" fill="${isBlock ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="8.5" font-family="var(--cds-font-mono)">${isClean ? 'async def + await asyncpg' : (isBlock ? '[!] time.sleep trong async def' : '1 Request khóa 1 OS Thread')}</text>
          <text x="216" y="108" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">${isClean ? 'Event Loop rảnh chuyển ngữ cảnh' : (isBlock ? 'ĐÓNG BĂNG TOÀN BỘ LOOP!' : 'Cạn kiệt 32 luồng chờ I/O')}</text>

          <rect x="390" y="16" width="156" height="218" rx="8" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-width="1.5"/>
          <text x="400" y="36" fill="var(--sim-ink)" font-size="10" font-weight="800" font-family="var(--cds-font-mono)">3. KẾT QUẢ ĐO KIỂM</text>
          <rect x="400" y="48" width="136" height="170" rx="6" fill="var(--sim-card)" stroke="var(--sim-border)" stroke-width="1.3"/>
          <text x="408" y="68" fill="var(--sim-ink)" font-size="9.5" font-weight="700">Thông Lượng &amp; Độ Trễ</text>
          <text x="408" y="88" fill="${isClean ? 'var(--sim-ok)' : 'var(--sim-danger)'}" font-size="8.8" font-weight="700" font-family="var(--cds-font-mono)">RPS: ${isClean ? '2,450 req/s' : (isWsgi ? '188 req/s' : '12 req/s (Kẹt!)')}</text>
          <text x="408" y="108" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">p50: ${isClean ? '14 ms' : (isWsgi ? '165 ms' : '4,200 ms')}</text>
          <text x="408" y="128" fill="var(--sim-sub)" font-size="8.5" font-family="var(--cds-font-mono)">p99: ${isClean ? '38 ms' : (isWsgi ? '890 ms' : '15,000 ms')}</text>

          <path d="M 174 96 L 208 96" stroke="var(--sim-flow)" stroke-width="2.4" class="ing2d-flow-active"/>
          <path d="M 356 96 L 400 96" stroke="${isClean ? 'var(--sim-ok)' : 'var(--sim-danger)'}" stroke-width="2.4" class="ing2d-flow-active"/>
        </svg>
        <div class="ing2d-metrics-strip">
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Kiến Trúc Máy Chủ</span><span class="ing2d-metric-val">${isWsgi ? 'WSGI (Synchronous)' : 'ASGI (Uvicorn uvloop)'}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Cổng Kiểm Dịch</span><span class="ing2d-metric-val">Pydantic v2 (Rust Core)</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Thông Lượng (RPS)</span><span class="ing2d-metric-val">${isClean ? '2,450 RPS' : (isWsgi ? '188 RPS' : '12 RPS (Treo)')}</span></div>
          <div class="ing2d-metric-chip"><span class="ing2d-metric-label">Độ Trễ Đuôi p99</span><span class="ing2d-metric-val" style="color:${isClean ? 'var(--sim-ok)' : 'var(--sim-danger)'}">${isClean ? '38 ms (Tối ưu)' : (isWsgi ? '890 ms' : '15,000 ms!')}</span></div>
        </div>
      `;

      if (isClean) {
        status.innerHTML = `<strong style="color:var(--sim-ok);">[1. Chuẩn FastAPI ASGI Bất đồng bộ (Slide 86 &amp; Chặng 5)]:</strong> Kết hợp vòng lặp sự kiện <code>uvloop</code> với trình điều khiển bất đồng bộ <code>asyncpg</code> / <code>httpx.AsyncClient</code> và cổng kiểm dịch <code>Pydantic v2</code> viết bằng Rust giúp xử lý hơn <code>2,450 RPS</code> với <code>p99 = 38ms</code>!`;
      } else if (isBlock) {
        status.innerHTML = `<strong style="color:var(--sim-danger);">[2. Cạm bẫy Đóng băng Event Loop (Blocking Call in async def)]:</strong> Gọi hàm đồng bộ (<code>time.sleep()</code> hoặc <code>requests.get()</code>) bên trong hàm <code>async def</code> làm khóa cứng luồng Event Loop đơn duy nhất của Uvicorn — toàn bộ 300 người dùng phải xếp hàng chờ tuần tự!`;
      } else {
        status.innerHTML = `<strong style="color:var(--sim-warn);">[3. Giới hạn của WSGI Đồng bộ (Flask / Gunicorn)]:</strong> Mỗi request đang chờ Database hoặc mạng đều chiếm giữ cứng 1 luồng hệ điều hành (OS Thread), làm cạn sạch bể 32 luồng ở ngưỡng <code>~188 RPS</code> dù CPU vẫn rảnh rỗi.`;
      }

      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${isClean ? 'infra2d-btn-emerald' : ''}" onclick="api2dState.fapiMode='asgi_clean';renderApi2DInteractiveStage('fastapi')">1. Chuẩn ASGI: async def + await (2,450 RPS)</button>
        <button type="button" class="infra2d-btn ${isBlock ? 'infra2d-btn-danger' : ''}" onclick="api2dState.fapiMode='event_block';renderApi2DInteractiveStage('fastapi')">2. Bẫy Thực Chiến: Gọi Hàm Đồng Bộ Trong async def</button>
        <button type="button" class="infra2d-btn ${isWsgi ? 'infra2d-btn-amber' : ''}" onclick="api2dState.fapiMode='wsgi_sync';renderApi2DInteractiveStage('fastapi')">3. Đối Chiếu WSGI Đồng Bộ (Flask Thread-Blocking)</button>
      `;
    }
  }
"""
