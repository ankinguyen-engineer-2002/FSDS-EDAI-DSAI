# Linux Fundamentals

Nguồn cho bài F01 trong `fsds-learning-hub.html`. Neo: `cat /etc/os-release`, pipe, `daily.sh`, `make`, cron `30 3 * * *`. Mỗi cảnh một trace. Phần chữ dưới đây là diễn giải và thuật ngữ đang gắn trong HTML.

## Mạch học vĩ mô → micro

Đừng bắt đầu bằng việc thuộc lệnh. Hãy đi theo năm câu hỏi:

1. **Mình muốn làm gì?** Terminal và shell biến ý định thành command.
2. **Máy thực hiện ở đâu?** Process đi qua user space, system call và kernel.
3. **Các việc nối với nhau thế nào?** stdin, stdout, stderr, pipe và exit status tạo thành flow.
4. **Làm lại thế nào cho đúng?** Script, Make và dependency graph tránh chạy thừa hoặc chạy sai.
5. **Chạy tự động ra sao?** Cron chỉ là cái hẹn giờ; log, lock, retry và cảnh báo mới làm job đáng tin.

Kết thúc bài, người mới không cần nhớ mọi option. Chỉ cần nhìn một command và chỉ ra được: ai đọc dòng lệnh, process nào đang chạy, kernel đang cung cấp tài nguyên gì, dữ liệu đi qua cửa nào và bằng chứng nào cho biết lệnh thành công.

## 01 · sequence — Gõ cat và chữ hiện ra

Dòng bạn gõ mới chỉ là chữ. Terminal giữ ký tự và vẽ kết quả. Bash mới là shell: nó tách tên chương trình với đối số thành argv, xử lý quote và biến, rồi tìm cat trong PATH, thường ra /usr/bin/cat. cat thuộc coreutils. Nó gọi thư viện glibc, và glibc mới thực hiện system call. Kernel nhận fork để nhân process, exec để nạp chương trình, rồi open và read để kiểm tra path cùng permission và trả byte. Mỗi process có bảng file descriptor: stdin là 0, stdout là 1, stderr là 2. cat ghi nội dung vào stdout. Lỗi đi stderr.

Thuật ngữ: `terminal`, `shell`, `PATH`, `argv`, `coreutils`, `glibc`, `fork / exec`, `file descriptor`, `system call`.

## 02 · sequence — Cùng lệnh, nhưng bị từ chối

Cùng một đường tới kernel. Lần này open thất bại vì user của process không có quyền đọc file, nên không có byte nội dung nào đi stdout. Kernel trả lỗi EACCES. cat ghi câu từ chối ra stderr và thoát với exit status khác 0. Path tuyệt đối bắt đầu bằng /. Path tương đối tính từ cwd, thư mục hiện tại, xem bằng pwd và đổi bằng cd. ls -l cho thấy owner, group và ba bộ quyền r, w, x. chmod đổi quyền đó. chmod 777 mở hết cho mọi người, không phải cách sửa mặc định.

Thuật ngữ: `absolute path`, `relative path`, `cwd`, `permission`, `chmod`, `EACCES`, `stderr`, `exit status`.

## 03 · layers — Lệnh đi xuống, rồi tách ba chân

Cột này đi theo lệnh cat /etc/os-release. Ý định của bạn ở trên cùng. User process gồm terminal, Bash và cat, sống ở user space, cùng coreutils và GCC. glibc là thư viện chúng gọi trước khi xuống. System call là cửa: open, read, fork, exec. Kernel nhận việc, kiểm tra permission, giữ process và PID. Dưới kernel là ba chân dùng cùng lúc. CPU là chỗ scheduler cho process chạy. RAM giữ address space, vùng nhớ riêng, nơi buffer và bảng file descriptor nằm. I/O là đĩa: driver trong kernel đọc byte. Ba chân là ba tài nguyên của cùng một kernel. Init system và boot loader thuộc lúc máy khởi động. Lệnh đang chạy thì đi từ process xuống kernel, rồi dùng đúng chân. Cùng tầng user space, các lệnh chỉ là cách hỏi một việc: đang ở đâu dùng pwd, cd, ls, find; đổi file dùng cp, mv, rm; đọc dùng cat, less, head, tail hoặc man; đổi quyền dùng chmod; xem và dừng process dùng ps, top, kill.

Thuật ngữ: `user space`, `user process`, `glibc`, `kernel`, `system call`, `CPU`, `RAM`, `I/O`, `scheduler`, `address space`, `PID`, `driver`, `pwd · cd · ls · find`, `cp · mv · rm`, `man`.

## 04 · pipe — Ba chương trình, một dòng chữ

Unix không bắt cat biết grep là ai. Mỗi process đọc stdin, số 0, và ghi stdout, số 1. Pipe nối stdout của lệnh trước vào stdin của lệnh sau. stderr, số 2, vẫn là kênh chẩn đoán và không tự chui vào ống. Redirect như > hoặc 2> đổi điểm đến của một cửa mà lệnh kia không cần biết.

Thuật ngữ: `stdin`, `stdout`, `stderr`, `pipe`, `redirect`.

## 05 · sequence — Script kiểm tra rồi mới chạy

Script là file chữ. Shebang, dòng #!/usr/bin/env bash, chọn Bash để đọc nó. set -Eeuo pipefail bắt lỗi phải dừng, biến chưa khai báo là lỗi, và một lệnh hỏng trong pipe không bị nuốt. Giá trị đưa vào lệnh cần được quote để khỏi vỡ thành nhiều đối số. File không đọc được thì ghi stderr và exit 1. Pipeline phía sau không chạy. Exit status là hợp đồng với người gọi, kể cả cron.

Thuật ngữ: `shebang`, `set -euo pipefail`, `quote`, `exit status`.

## 06 · dag — Make chỉ làm phần đã cũ

Make không tự dịch C. Target đứng trước dấu hai chấm, dependency đứng sau. Recipe là lệnh chạy khi target thiếu hoặc cũ hơn dependency, và trong Makefile dòng recipe bắt đầu bằng tab. Sửa hello.c thì hello.o cũ, gcc -c chạy. hello phụ thuộc hello.o nên bước link chạy sau. Phần còn mới thì nghỉ. Trên đường từ source tới file chạy: preprocessor mở #include và macro thành .i, compiler dịch C thành assembly .s, assembler tạo object file .o, linker ghép .o với thư viện thành executable. Lỗi compile nằm lúc dịch source. Lỗi link nằm lúc ghép object.

Thuật ngữ: `target`, `dependency`, `recipe`, `preprocessor`, `compiler`, `assembler`, `linker`.

## 07 · sequence — Cron bấm cò, không chữa lỗi

Cron là daemon so năm ô trong crontab: phút, giờ, ngày trong tháng, tháng, thứ. 30 3 * * * là 03:30 mỗi ngày. Đúng giờ nó mở một shell với environment rất mỏng, nên PATH và cwd có thể khác terminal bạn đang ngồi. Lệnh trong crontab nên dùng absolute path và tự ghi log, ví dụ gắn stdout và stderr vào một file bằng >> và 2>&1. Cron không retry, không backfill, không chống overlap. Job nên idempotent, có lock nếu không được chạy chồng, và tự cảnh báo. Việc có dependency nhiều bước, cần retry hoặc theo dõi SLA, thuộc orchestrator như systemd timer hoặc Airflow, không thuộc cron.

Thuật ngữ: `crontab`, `cron expression`, `daemon`, `environment`, `absolute path`, `idempotent`, `lock`, `backfill`, `orchestrator`.

## 08 · mindmap — Linux của bài này

Bài này đi theo một lệnh thật, rồi nhìn lại các tên cần giữ. Gốc là Linux. Nhánh là các chỗ trên cùng đường chạy đó: ai hiểu lệnh, nền dưới lệnh, kernel giữ gì, cách ghép việc, cách làm lại đúng phần, và cái gì xảy ra khi hẹn giờ.

Thuật ngữ: `terminal`, `shell`, `PATH`, `fork / exec`, `stdout / stderr`, `absolute path`, `cwd`, `permission`, `chmod`, `ps / kill`, `exit status`, `scheduler`, `address space`, `PID`, `system call`, `driver`, `stdin / stdout / stderr`, `pipe`, `shebang`, `set -euo pipefail`, `target`, `dependency`, `recipe`, `link`, `cron expression`, `environment`, `idempotent`, `backfill`.

## Coverage map và nguồn kiểm chứng

| Cảnh trong hub | Ý chính được chứng minh | Nguồn nội bộ / đối chiếu |
|---|---|---|
| 01–02 | shell, argv, fork/exec, file descriptor, permission, stderr và exit status | `course-slides/01-linux-fundamentals.pdf`; `man 1 cat`, `man 2 open`, `man 2 read`, `man 7 pipe` |
| 03 | user space, kernel, process, CPU/RAM/I/O, VFS và driver | `course-slides/01-linux-fundamentals.pdf`; `man 7 user_namespaces`; `man 5 proc` |
| 04–05 | pipe/redirect, shebang, `set -Eeuo pipefail`, quote và exit contract | `course-slides/01-linux-fundamentals.pdf`; Bash Reference Manual §3.2–3.7 |
| 06 | dependency graph, incremental build, preprocess/compile/assemble/link | `course-slides/01-linux-fundamentals.pdf`; GNU Make manual §2; GCC manual “Overall Options” |
| 07 | cron fields, môi trường mỏng, log, idempotency và giới hạn retry/overlap | `course-slides/01-linux-fundamentals.pdf`; `man 5 crontab`; `man 8 cron` |
| 08 | bản đồ tổng hợp từ command đến kernel và scheduler | Các cảnh 01–07; `LEARNING-DESIGN-METHOD.md` |

### Ghi chú biên tập

- Sơ đồ sequence tách terminal, shell, process và kernel để không gộp “gõ lệnh” với “chạy chương trình”.
- Pipe giữ `stderr` là kênh riêng; đây là điểm thường bị bỏ qua trong slide nhập môn.
- Cron được mô tả là trigger, không phải workflow engine: retry, backfill, lock và cảnh báo phải do job/orchestrator đảm nhiệm.
