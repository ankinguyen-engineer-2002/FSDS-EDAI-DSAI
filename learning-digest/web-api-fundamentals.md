# F04 · Web API Fundamentals — learning digest

_Cập nhật: 2026-09-24_

Digest này là bản ghi biên tập cho bài F04. Nội dung hiển thị trong hub nằm tại `content/beginner-guides.json`, `content/lesson-mechanisms.json` và `content/term-examples.json`; digest giải thích nguồn nào được dùng, phần nào được giữ/bỏ và mental model cuối cùng.

## 1. Vị trí trong toàn khóa

F04 đứng sau Linux, Python và Database:

```text
Linux cho process, file, network và evidence hệ thống
→ Python cho runtime, object, async và ASGI
→ Database cho shared truth, transaction và query
→ Web API biến các năng lực đó thành một boundary mà client khác có thể gọi
→ Validation & Verification sẽ kiểm chứng contract và failure model của API
→ Container/Kubernetes sẽ đóng gói, route và vận hành API
```

Năng lực đích theo syllabus:

- hiểu các API architecture styles và trade-off;
- hiểu authentication/authorization;
- dùng FastAPI với validation/type enforcement, middleware và health check;
- đọc performance metrics và thực hiện load/stress testing;
- triển khai một API có contract, failure behavior và evidence rõ.

## 2. Source map

### Slide chính

`course-slides/04-web-api.pdf` — 87 trang, PDF dạng ảnh, đã render và OCR toàn bộ.

Các cụm nội dung:

| Trang | Nội dung | Quyết định biên tập |
|---:|---|---|
| 4–8 | API, protocol, OSI/TCP-IP overview | Giữ boundary và layered reasoning; bỏ việc học thuộc đủ layer vì không phục vụ trực tiếp flow F04. |
| 9–23 | HTTP request/response, methods, headers, body, status | Giữ như contract trên dây; sửa cách diễn đạt method/status thành semantics chứ không chỉ CRUD mapping. |
| 24–35 | TLS, DNS, TCP/UDP, IP/link, network flow | Cô đọng thành một request journey: DNS → transport → TLS → HTTP/application. Không biến bài API thành bài networking đầy đủ. |
| 37–61 | API architecture overview; REST, gRPC, WebSocket, SSE, Webhook; trang 38 còn đặt GraphQL, RPC và AMQP trong bản đồ rộng hơn | Tách hai câu hỏi: **contract gọi gì** (REST/SOAP/GraphQL/gRPC) và **dữ liệu chảy thế nào** (request-response/WebSocket/SSE/webhook/polling). Không dùng bảng popularity làm knowledge core. |
| 63–76 | AAA, Basic Auth, JWT, OAuth | Giữ authenticate → authorize → audit; sửa các đơn giản hóa nguy hiểm về JWT “không cần database” và OAuth “là authentication”. |
| 78–85 | Health checks, metrics, load/stress testing | Giữ liveness/readiness, RPS, error rate, percentile, load test; bổ sung deadline/retry/idempotency vì thiếu chúng thì failure model không hoàn chỉnh. |

### Sách trong `library/`

1. **Computer Networking: A Top-Down Approach — Kurose & Ross**
   - Ch. 1: delay, loss, throughput và protocol layering.
   - Ch. 2.2: HTTP overview, connection behavior, message format, cookies/cache.
   - Ch. 2.4: DNS service và resolution.
   - Ch. 3: transport services, TCP/UDP, timeout/reliability.
   - Dùng để giữ đường đi request đúng lớp và tránh gọi mọi lỗi mạng là “API error”.

2. **Beej’s Guide to Network Programming — Brian Hall**
   - Socket/stream/datagram, port và địa chỉ.
   - Dùng để kiểm tra trực giác: HTTP application không tự vận chuyển byte; nó dựa lên networking stack/socket.

3. **Designing Data-Intensive Applications — Martin Kleppmann**
   - Ch. 4, “Dataflow Through Services: REST and RPC”.
   - REST là design philosophy chứ không phải protocol; RPC từ xa có timeout, lost response và partial failure; schema/compatibility quan trọng khi API tiến hóa.
   - Dùng để sửa ảo giác “remote call giống local function call”.

4. **Cloud Native Patterns — Cornelia Davis**
   - Stateless application/scale-out; retries và retry storms; circuit breaker/API gateway.
   - Dùng để nối stateless với scale-out và thêm guardrail cho retry.

5. **Site Reliability Engineering — Google**
   - Latency/deadlines, overload behavior, load tests, health checking.
   - Dùng để phân biệt process health với service readiness và nhấn mạnh tail latency thay vì chỉ trung bình.

### Tài liệu chính thức để kiểm chứng

- FastAPI documentation: request body/schema validation, middleware, dependencies, OpenAPI và async/ASGI behavior.
- RFC 9110: HTTP semantics, safe/idempotent methods và status semantics.
- W3C SOAP 1.2 Primer và WSDL references: Envelope/Header/Body/Fault, operation contract và message binding.
- GraphQL specification/official learning docs: schema, selection set, validation, execution và resolver behavior.
- MDN HTTP/WebSocket/EventSource references: message anatomy, HTTP Upgrade và browser-facing realtime APIs.
- gRPC official concepts: `.proto`, generated stub, protobuf, unary/server-streaming/client-streaming/bidirectional streaming.
- GitHub Webhooks documentation: event delivery, signature verification, redelivery và callback behavior.
- Kubernetes probes documentation: liveness, readiness và startup probes.

## 3. Cơn đau nguyên bản

Không có API boundary, ba client sẽ phải biết:

- code nội bộ nằm ở đâu;
- database dùng bảng/cột nào;
- credential nào mở được dữ liệu;
- cách riêng để gọi, xử lý lỗi và theo dõi từng hệ thống.

Một thay đổi database có thể làm hỏng mọi client. Một client bị lộ credential có thể đi vòng qua business rule. Khi lỗi, không ai biết request chưa tìm được server, bị TLS chặn, sai schema, thiếu quyền hay chết ở database.

Điểm nghẽn vật lý là **không thể cho vô số client tự phối hợp trực tiếp với nội bộ luôn thay đổi của server**. Cần một quầy duy nhất có mẫu phiếu và biên nhận chung.

## 4. Living metaphor duy nhất

Thế giới dùng xuyên bài: **nhà hàng có một quầy nhận món cho website, app điện thoại và đối tác giao hàng**.

| Đồ vật / hành động | Khái niệm | Vai trò thật |
|---|---|---|
| Khách gửi phiếu | Client | Khởi tạo request. |
| Nhà hàng | Server | Giữ năng lực xử lý và state phía sau. |
| Mẫu phiếu | API contract/schema | Quy định request/response hợp lệ. |
| Danh bạ + địa chỉ | DNS + IP | Tìm đích mạng. |
| Xe/tuyến giao hàng | Transport | Chuyển byte. |
| Túi niêm phong + kiểm bảng hiệu | TLS | Mã hóa và xác thực server. |
| Phiếu/biên nhận | HTTP request/response | Chứa ý định và kết quả. |
| Ô nhận món | Endpoint/router | Chuyển request tới đúng handler. |
| Nhân viên soát phiếu | Validation/dependency/middleware | Chặn input sai và áp logic chung. |
| Bếp | Handler/business logic | Quyết định nghiệp vụ. |
| Sổ kho | Database | Giữ shared truth. |
| Dấu trên biên nhận | Status code | Phân loại kết quả. |
| Camera + đồng hồ ca | Logs/traces/metrics | Bằng chứng vận hành. |

Giới hạn ẩn dụ: mạng không phải một xe duy nhất; protocol được bọc theo lớp. Token không phải vé vào mọi phòng. Retry không phải “gọi lại đến khi được”.

## 5. Knowledge spine đã chốt

```text
1. API boundary: tại sao cần một hợp đồng chung?
2. HTTPS journey: request tới đúng nơi bằng cách nào?
3. HTTP message: hai phía diễn đạt ý định/kết quả ra sao?
4. REST + FastAPI: contract biến thành code chạy thế nào?
5. API styles: REST/SOAP/GraphQL/gRPC ký hợp đồng ra sao; polling/SSE/WebSocket/webhook chuyển cập nhật thế nào?
6. Trust path: ai gọi, được làm gì, đã làm gì?
7. Resilience: khi chậm/hỏng/quá tải thì dừng và hồi phục thế nào?
8. Synthesis: request đang mắc ở boundary nào và evidence nào chứng minh?
```

Đây là một causal chain. Không chương nào là “từ điển riêng”; mỗi thuật ngữ chỉ xuất hiện sau khi người học đã thấy việc nó giải quyết.

## 6. Những chỉnh sửa quan trọng so với slide

### JWT

Không dạy “JWT giúp server không cần database lookup”. Server có thể verify chữ ký cục bộ, nhưng authorization theo resource, revocation, consent, device/session state hoặc account status vẫn có thể cần server-side state. JWT payload thường chỉ encode, không mặc định mã hóa.

### OAuth 2.0

Dạy là framework ủy quyền để cấp access token. Nếu dùng cho đăng nhập, cần lớp identity phù hợp như OpenID Connect; không gọi OAuth đơn giản là “authentication mechanism”.

### Stateless

Không hiểu là “server không có state”. Nghĩa thực dụng ở đây: request không phụ thuộc memory phiên ngầm của request trước trên cùng instance. Business state vẫn nằm trong database/cache và authorization vẫn cần state hiện tại.

### REST

Không dạy REST như bảng `GET=read, POST=create`. Method có semantics rộng hơn CRUD; resource/representation, uniform interface và stateless interaction mới là lõi cần giữ.

### SOAP

Không gọi SOAP là “REST dùng XML”. SOAP là protocol/message model: WSDL mô tả operation và binding; Envelope bọc Header/Body; lỗi có Fault. Giữ điểm mạnh là contract/policy chặt và điểm đổi lại là verbosity/độ phức tạp.

### GraphQL

Không dạy “một endpoint nên chỉ có một backend call” hoặc “GraphQL tự nhanh”. Query chọn field ở client boundary; parser/validator/resolver graph vẫn có thể fan-out, tạo N+1 và cần authorization theo field/resource.

### RPC và gRPC

Không để generated stub che mất network. `.proto` + protobuf + HTTP/2 tạo typed call và streaming hiệu quả, nhưng deadline, lost response, partial failure và schema compatibility vẫn là trách nhiệm thật.

### WebSocket, SSE, polling và webhook

Không gom mọi thứ vào chữ “realtime”. Polling đánh đổi request thừa lấy đơn giản; SSE là event stream một chiều; WebSocket là connection hai chiều cần heartbeat/reconnect/state sync; webhook là HTTP callback có thể trễ, lặp hoặc đảo thứ tự nên phải verify, persist, ACK và deduplicate.

### Health check

Liveness trả lời process có cần restart không. Readiness trả lời instance có nên nhận traffic mới không. Database tạm chậm không nên mặc định làm liveness fail và gây restart loop.

### Retry

Retry là một load multiplier. Chỉ retry lỗi tạm thời, có deadline/budget, exponential backoff + jitter và semantics/idempotency phù hợp.

### Performance

Không dùng average latency làm bằng chứng chính. Giữ RPS/throughput, error rate và p50/p95/p99 để nhìn tail. Load test hỏi hệ thống có giữ mục tiêu ở traffic dự kiến; stress test tìm breaking point và cách hồi phục.

## 7. Chapter map và term inventory

| Chapter | Câu hỏi | Thuật ngữ lõi |
|---|---|---|
| boundary | Vì sao không chạm thẳng code/database? | API, client, server, API contract, endpoint |
| journey | Request tới application bằng đường nào? | DNS, IP address, transport connection, TLS, HTTPS |
| message | HTTP message mang gì? | request, method, target, header, body, status, idempotent method |
| contract | REST/FastAPI chia trách nhiệm thế nào? | REST, resource, stateless, schema, validation, OpenAPI, ASGI, middleware |
| styles | Contract gọi gì và cập nhật chảy thế nào? | REST, SOAP, WSDL, SOAP Envelope, GraphQL, resolver, RPC, gRPC, protobuf, stub, WebSocket, HTTP Upgrade, SSE, event stream, webhook, signature, polling |
| trust | Ai gọi, được làm gì, đã làm gì? | authentication, authorization, audit log, credential, access token, JWT, OAuth 2.0 |
| resilience | Khi chậm/hỏng/quá tải thì sao? | deadline, retry, backoff+jitter, idempotency key, probes, RPS, percentile, load test |
| recap | Chẩn đoán end-to-end bằng gì? | trace ID, observability |

Tổng: 8 chapter, 10 mechanism scene, 60 core term card.

## 8. Visual inventory — chỉ giữ visual cần thiết

| ID | File | Câu hỏi nhận thức | Vì sao prose chưa đủ |
|---|---|---|---|
| W01 | `web-api-boundary-architecture` | Client, API, business logic và database nằm ở đâu? | Người mới thường đồng nhất API với server/database; cần spatial boundary. |
| W02 | `https-request-journey-sequence` | Một request đi theo thứ tự nào trước/sau application? | Sequence giúp tách DNS/transport/TLS/HTTP và failure layer. |
| W03 | `http-message-contract-architecture` | Request/response gồm gì và mỗi phần trả lời câu nào? | Cần nhìn hai phong bì song song thay vì bullet list. |
| W04 | `fastapi-contract-sequence` | Contract được công bố và runtime thực thi ra sao? | Nối OpenAPI, ASGI, FastAPI, handler và DB theo thời gian. |
| W05A | `api-contract-styles-architecture` | REST/SOAP/GraphQL/gRPC khác ở thứ được gọi, contract và runtime nào? | Cần nhìn bốn đường WHAT → HOW hội tụ vào cùng service; prose riêng lẻ khó giữ quan hệ. |
| W05B | `api-interaction-styles-architecture` | Polling/WebSocket/SSE/Webhook khác ai chủ động, hướng và tuổi thọ connection nào? | So sánh direction/topology hiệu quả hơn các định nghĩa rời. |
| W06 | `api-trust-sequence` | Authenticate → authorize → act → audit diễn ra thế nào? | Security dễ bị dồn vào một chữ “token”; sequence tách các cửa. |
| W07 | `api-resilience-lifecycle` | Đường bình thường, retry và overload khác nhau ra sao? | Cần thấy failure branch và traffic control như ba đường riêng. |
| W08 | `web-api-synthesis-architecture` | Bảy câu hỏi chẩn đoán nối thành mental model nào? | Bản đồ cuối giúp người học kể lại và khoanh vùng lỗi. |

Không tạo visual riêng cho bảng status code, danh sách method, cấu trúc JWT hay bảng popularity vì chúng là reference/tra cứu, không phải cơ chế cần thêm một sơ đồ độc lập.

## 9. Stress test xuyên bài

Tình huống: database chậm 10 giây. Client timeout sau 2 giây và 1.000 client retry cùng lúc. Một số request POST đã tạo order nhưng response thất lạc, nên retry tạo order trùng. Readiness vẫn xanh vì process còn chạy; liveness bị cấu hình phụ thuộc database nên Kubernetes restart liên tục.

Cách hệ thống đúng hơn:

1. Deadline đi cùng request và được truyền xuống downstream.
2. Chỉ retry failure tạm thời, có retry budget, backoff và jitter.
3. POST dùng idempotency key để lần lặp nhận lại cùng outcome.
4. Readiness có thể tạm dừng traffic; liveness chỉ fail khi process không tiến triển.
5. Dashboard nhìn RPS, error rate, p95/p99, queue/saturation; trace ID nối client, API và database.

## 10. Golden takeaway

> Web API là quầy có hợp đồng: đưa một yêu cầu tới đúng nơi, kiểm tra nó, làm việc được phép, rồi trả kết quả và bằng chứng đủ rõ để cả người dùng lẫn người vận hành biết chuyện gì đã xảy ra.
