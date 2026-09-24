# Python Fundamentals

Nguồn cho bài F02 trong `fsds-learning-hub.html`. Neo: `python -m pipeline ingest orders.csv`. Mỗi cảnh một trace. Phần chữ dưới đây là diễn giải và thuật ngữ đang gắn trong HTML.

## Mạch học vĩ mô → micro

Bài đi từ một chương trình hoàn chỉnh xuống các cơ chế nhỏ hơn:

1. **Project chạy bằng gì?** Virtual environment, dependency contract và lockfile giữ đúng interpreter/package boundary.
2. **Chương trình là gì?** Shell tạo process; interpreter đọc source và dựng bytecode.
3. **Dữ liệu ở đâu?** Tên chỉ tới object trong namespace; gán, sửa và copy là ba việc khác nhau.
4. **Lỗi đi thế nào?** Frame, call stack và traceback cho thấy lỗi phát sinh ở đâu và quay về đâu.
5. **Qua ranh giới ra sao?** File, socket và database chỉ nhận byte theo schema, không nhận object đang sống trong RAM.
6. **Chạy nhanh hơn bằng cách nào?** Tách CPU task khỏi IO task; async chồng thời gian chờ, còn thread/process là lựa chọn thực thi khác nhau.

Các thuật ngữ sâu như AST, GIL, ASGI hay Arrow chỉ xuất hiện sau khi đường chạy lớn đã rõ. Mục tiêu là hiểu Python đang giữ quyền chạy ở đâu, dữ liệu đang nằm ở đâu và phép đo nào đủ để kết luận.

## 00 · boundary — Chạy đúng code bằng đúng môi trường

Virtual environment tạo ranh giới interpreter và site-packages theo project; nó không phải container. `pyproject.toml` là dependency contract, resolver dựng graph, và lockfile (nếu workflow dùng lock) giữ lựa chọn cụ thể để sync ổn định hơn. `activate` chỉ thay PATH của shell hiện tại; cron/CI nên gọi interpreter rõ ràng. Không commit `.venv`; commit declaration, lockfile phù hợp, test và hướng dẫn chạy.

Thuật ngữ: `virtual environment`, `pyproject.toml`, `resolver`, `lockfile`, `site-packages`, `reproducibility`.

## 01 · sequence — Nhấn Enter, file .py chưa chạy ngay

Dòng lệnh không phải code Python. Shell tách argv: tên chương trình, cờ -m, tên module, file dữ liệu. Hệ điều hành tạo process, nạp interpreter, gắn environment, cwd, stdin, stdout và stderr. File .py là source. Python đọc chữ đó, dựng AST, rồi biên dịch thành bytecode nằm trong code object. Code object là kế hoạch tĩnh, chưa phải một lần chạy. Runtime mở xong, import system mới tìm module vì -m, tạo module namespace và chạy code ở cấp module. Nếu chạy như chương trình, module mang tên __main__ và entry point gọi main. Việc nặng lúc import xảy ra trước main. Cùng một file có thể chạy ở terminal nhưng lỗi trong cron nếu PATH, quyền hoặc cwd khác.

Thuật ngữ: `shell`, `argv`, `process`, `environment`, `cwd`, `interpreter`, `source`, `AST`, `bytecode`, `code object`, `import`, `__main__`, `entry point`.

## 02 · layers — File đứng trên, ba chân đứng dưới

pipeline.py là source, chữ người đọc. CPython là máy ảo: nó dựng AST, dịch thành bytecode, rồi interpreter đọc bytecode. Máy ảo nằm trong một process của hệ điều hành, và kernel xếp lịch process đó. Ba chân là ba tài nguyên của cùng process. CPU là chỗ interpreter đang bận với bytecode: đó là CPU task ở cảnh thời gian phía sau. RAM là chỗ object, frame và namespace nằm. I/O là file orders.csv và socket: máy ảo chờ kernel đọc hoặc ghi, khoảng chờ đó là IO task. Async chồng các khoảng chờ trên một thread. GIL, ở cảnh khóa, chỉ xếp hàng khi có thread đang giữ bytecode trên chân CPU. Lời gọi chờ của thư viện C ở chân I/O thì nhả khóa, thread khác vẫn tính được.

Thuật ngữ: `CPython`, `interpreter`, `bytecode`, `process`, `CPU`, `RAM`, `I/O`, `CPU task`, `IO task`.

## 03 · binding — Hai nhãn, một danh sách

Gán trong Python thường không sao chép dữ liệu. Namespace ghi name binding: tên trỏ tới object. backup = records tạo alias, nhãn thứ hai trên cùng list. List là mutable, sửa được tại chỗ. append là mutation, nên cả hai tên đều thấy C. Gán backup sang một list mới là rebinding, tên trỏ sang object khác. Hai tên có cùng một vật hay không thì xem identity, toán tử is, không phải so giá trị bằng ==. copy.copy là shallow copy: vỏ mới, vật con bên trong vẫn dùng chung. CPython đếm reference. Hết đường trỏ thì object thường được thu hồi ngay. Hai object trỏ lẫn nhau thành vòng thì cyclic garbage collector mới nhặt. File và socket vẫn phải đóng rõ, không chờ bộ thu gom.

Thuật ngữ: `namespace`, `name binding`, `alias`, `object`, `mutable`, `mutation`, `rebinding`, `identity`, `shallow copy`, `reference counting`, `cyclic GC`.

## 04 · stack — parse lỗi, lỗi đi ngược lên

Mỗi lần gọi hàm, Python mở một frame. Frame giữ biến local, instruction pointer là chỗ đang chạy trong bytecode, và địa chỉ quay về. main gọi load thì frame load nằm trên frame main trong call stack. parse đang chạy là frame trên cùng. Raise tạo exception. Không có handler thì interpreter gỡ frame, gọi là unwinding, và đưa lỗi về frame đang chờ. Traceback là bản đồ chuỗi đó. finally và context manager, cú pháp with, vẫn chạy __exit__ để đóng file, lock, transaction trên cả đường thành công lẫn đường lỗi. Bắt exception ở nơi biết phải trả exit code hoặc HTTP status nào. Traceback cho biết lỗi đi đâu. cProfile cho biết thời gian nằm ở hàm nào. tracemalloc cho biết dòng nào đang cấp nhiều object Python.

Thuật ngữ: `frame`, `instruction pointer`, `call stack`, `exception`, `unwinding`, `traceback`, `handler`, `context manager`, `cProfile`, `tracemalloc`.

## 05 · boundary — Danh sách đi ra file

Trong process, code truyền reference tới object. Qua file, socket hoặc database, hai phía không dùng chung object. Serialization, còn gọi là encode, đổi value theo schema thành byte. CSV và JSON là chữ. Arrow là bộ nhớ cột, dùng khi muốn đỡ copy giữa Python và engine. Kernel chuyển byte qua buffer. Phía nhận decode rồi parse thành object mới và validate. Schema lệch, encode lặp, hoặc chunk quá nhỏ làm tăng số lần system call và dễ sai. Chunk quá lớn thì tốn memory và tăng latency. Contract của cửa gồm format, schema, và cách báo lỗi. Producer đổi contract âm thầm thì downstream sai.

Thuật ngữ: `serialization`, `JSON`, `CSV`, `Arrow`, `schema`, `buffer`, `decode / parse`, `validate`, `contract`.

## 06 · timeline — Việc tính và việc chờ

Khối đậm là CPU task, khối nhạt là IO task. Sync đứng trong khoảng chờ của A nên B chưa bắt đầu. Async vẫn một thread: await nhả thread khi A chờ, B tính một đoạn ngắn rồi cũng chờ. Hai khoảng IO chồng nhau. Các đoạn CPU không chồng. GIL chưa xuất hiện vì mới có một thread.

Thuật ngữ: `CPU task`, `IO task`, `synchronous`, `blocking I/O`, `await`, `event loop`.

## 07 · timeline — GIL chỉ khóa lúc đang tính

Hai thread, một process, CPython mặc định. Hai CPU task phải thay nhau cầm GIL, các khối tính không chồng. Một CPU task và một IO task: lời gọi chờ của thư viện C nhả GIL, nên thread đang tính chạy trong lúc thread kia chờ. Async không dùng GIL để xen kẽ. Hai CPU task Python chạy cùng lúc thật thì tách process.

Thuật ngữ: `GIL`, `bytecode`, `CPU task`, `IO task`, `thread`, `process`.

## 08 · sequence — Một request đi tới hàm của bạn

Client gửi byte HTTP qua socket. Uvicorn là ASGI server đứng trước FastAPI: nó đọc socket, giữ connection, rồi gọi ứng dụng với scope, receive và send. FastAPI không tự đọc socket. Lúc import, decorator như @app.post ghi hàm vào registry, chưa chạy nghiệp vụ. Khi request tới, router chọn route, dependency dựng những thứ hàm cần, rồi mới gọi handler. Hàm async def được await trên event loop. Hàm def thường có thể bị đưa sang thread pool. Nếu trong async def bạn gọi thư viện blocking, cả loop phải đợi. Handler trả kết quả, server encode thành HTTP response và ghi ra socket. Auth, log, CORS thường là middleware bọc ngoài route.

Thuật ngữ: `HTTP`, `socket`, `Uvicorn`, `ASGI`, `scope`, `decorator`, `route`, `dependency`, `handler`, `async def / def`, `middleware`.

## 09 · mindmap — Python của bài này

Ba câu để quay lại khi lạc: ai đang giữ quyền chạy, dữ liệu đang ở đâu, và bằng chứng nào cho biết đúng hay sai. Sáu nhánh là sáu chỗ phóng to của cùng lệnh python -m pipeline ingest orders.csv.

Thuật ngữ: `argv`, `cwd`, `interpreter`, `AST`, `bytecode`, `code object`, `__main__`, `name binding`, `alias`, `mutable`, `identity`, `reference counting`, `frame`, `traceback`, `context manager`, `cProfile`, `tracemalloc`, `serialization`, `schema`, `buffer`, `validate`, `CPU task`, `IO task`, `await`, `GIL`, `bytecode`, `thread`, `process`, `Uvicorn`, `ASGI`, `decorator`, `handler`, `middleware`.

## Archify visual labs được nhúng

Python hiện có **11/11 Archify visuals**: project boundary, runtime architecture, startup sequence, name-binding object graph, exception unwinding, serialization dataflow, sync/async comparison, concurrency lifecycle, GIL decision map, web request sequence và synthesis map.

Mỗi artifact đóng vai trò một “bàn thí nghiệm” cho đúng một câu hỏi cơ chế; prose không lặp lại toàn bộ quan hệ đã có trong diagram. Các visual có pan/zoom, guided views, theme, export và canonical Python/FastAPI marks khi phù hợp.

Source of truth là JSON trong `archify/specs/`; không sửa trực tiếp artifact đã deliver.

## Coverage map và nguồn kiểm chứng

| Cảnh trong hub | Ý chính được chứng minh | Nguồn nội bộ / đối chiếu |
|---|---|---|
| 01 | shell → process → interpreter → import → `__main__`, AST và code object | `course-slides/02-python-fundamentals.pdf`; Python docs: `__main__`, import system, `compile()` |
| 02 | CPython, bytecode, process, CPU/RAM/I/O và ranh giới runtime | `course-slides/02-python-fundamentals.pdf`; Python/C API glossary; `resource` và `sys` docs |
| 03–04 | name binding, mutation, identity, frame, exception unwinding và traceback | `course-slides/02-python-fundamentals.pdf`; Python Language Reference: execution model, exceptions, data model |
| 05 | serialization, schema, buffer, parse và validate qua file/socket/database | `course-slides/02-python-fundamentals.pdf`; `json`, `csv`, `pickle` docs; Apache Arrow format docs |
| 06 | sync/async, blocking I/O, `await`, event loop và giới hạn CPU | `course-slides/02-python-fundamentals.pdf`; `asyncio` docs §Coroutines and Tasks |
| 07 | GIL theo build/runtime, I/O release, free-threaded build và lựa chọn process | `course-slides/02-python-fundamentals.pdf`; Python docs: `threading`, `concurrent.futures`, free-threaded CPython notes |
| 08 | socket → ASGI server → router/dependency → handler → response | `course-slides/04-web-api.pdf`; ASGI spec; FastAPI/Uvicorn docs |
| 09 | bản đồ tổng hợp: ai giữ quyền chạy, dữ liệu ở đâu, bằng chứng nào | Các cảnh 01–08; `LEARNING-DESIGN-METHOD.md` |

### Ghi chú biên tập

- Cảnh GIL đã được sửa để nói rõ đây là hành vi của một số build CPython, không phải chân lý của ngôn ngữ Python; free-threaded build từ Python 3.13 là tùy chọn và hệ sinh thái extension phải tương thích.
- “CPU task” và “IO task” được tách thành hai trục: đoạn bytecode đang chạy và khoảng chờ bên ngoài. Điều này tránh đồng nhất async với parallelism.
- Cảnh web API giữ ranh giới: Uvicorn đọc socket và gọi ASGI app; FastAPI/router/dependency mới dựng handler context; handler mới thực hiện nghiệp vụ.
