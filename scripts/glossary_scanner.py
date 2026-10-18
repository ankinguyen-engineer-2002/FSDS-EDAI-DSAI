#!/usr/bin/env python3
"""
Automated Technical Term & Framework Scanner + Master Glossary Builder
for FSDS · EDAI · DSAI Learning Hub.
"""
import html
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def norm_key(s: str) -> str:
    s = unicodedata.normalize("NFC", str(s or "")).strip()
    s = re.sub(r"\s+", " ", s)
    return s.lower()


RAW_GLOSSARY = [
    # =========================================================================
    # F01: LINUX FUNDAMENTALS — CHẶNG 1 (KERNEL, GNU, DISTRO, SHELL, SYSCALL)
    # =========================================================================
    (
        "linux.kernel",
        "Linux Kernel (Hạt nhân hệ điều hành · Ring 0)",
        "KERNEL & OS CORE",
        ["F01"],
        [
            "linux kernel", "kernel", "hạt nhân", "hạt nhân linux", "cục máy động cơ",
            "kernel space", "ring 0", "linux 0.01", "linux", "unix", "multi-user",
            "multi-tasking", "đa người dùng (multi-user) & đa nhiệm (multi-tasking)",
            "cpu address space", "tlpi / ostep / cs:app"
        ],
        "Là 'cục máy động cơ' nằm sát phần cứng nhất (Ring 0): mọi chương trình muốn đọc đĩa, xin RAM hay gửi mạng đều phải xin phép Kernel.",
        "Chạy ở chế độ đặc quyền cao nhất (Kernel Space), trực tiếp quản lý bộ lập lịch CPU ( Đa nhiệm / Multi-tasking), cấp phát không gian địa chỉ bộ nhớ ảo (Virtual Memory), phân quyền Đa người dùng (Multi-user), điều khiển thiết bị qua Driver và tiếp nhận yêu cầu qua System Call.",
        "uname -r   # Kiểm tra phiên bản Linux Kernel đang chạy",
        "Trong lệnh grep ERROR /var/log/app.log, Kernel là người duy nhất được phép đọc các block vật lý của file app.log từ ổ SSD lên RAM."
    ),
    (
        "linux.gnu",
        "GNU Project & GNU Coreutils (Bộ khung công cụ GNU)",
        "KERNEL & OS CORE",
        ["F01"],
        [
            "gnu", "gnu/linux", "gnu project", "gnu coreutils", "coreutils", "glibc",
            "richard stallman", "linus torvalds", "gpl", "open source", "mã nguồn mở",
            "do one thing and do it well"
        ],
        "Nếu Linux Kernel là 'cục máy động cơ' trần trụi, thì GNU chính là 'vô-lăng, bàn đạp, vỏ xe' (Shell, trình biên dịch GCC, thư viện glibc, bộ lệnh ls, cp, grep) giúp con người lái được cỗ máy đó.",
        "Khởi xướng bởi Richard Stallman (1983), cung cấp thư viện chuẩn C (glibc), Bash shell, GCC, Make và bộ tiện ích dòng lệnh (GNU Coreutils) kết hợp với hạt nhân Linux của Linus Torvalds (1991) tạo thành hệ điều hành GNU/Linux hoàn chỉnh theo triết lý UNIX: 'Mỗi chương trình chỉ làm 1 việc và làm thật xuất sắc'.",
        "grep --version | head -n 1   # -> grep (GNU grep) 3.11",
        "Hầu hết các lệnh quen thuộc bạn gõ hàng ngày như ls, cat, cp, mv, rm, head, tail, wc đều thuộc gói GNU Coreutils."
    ),
    (
        "linux.distro",
        "Linux Distribution (Distro — Ubuntu, RHEL, Kali, Arch, Mint)",
        "LINUX ECOSYSTEM",
        ["F01"],
        [
            "distro", "linux distro", "distributions", "bản phân phối", "ubuntu", "debian",
            "rhel", "red hat", "rocky linux", "almalinux", "kali linux", "kali", "linux mint",
            "arch linux", "fedora", "centos", "apt", "yum", "dnf", "dpkg", "rpm", "lts",
            "lts 5–12 năm", "subscription", "license cost", "chi phí bản quyền (license cost)",
            "cinnamon", "nmap", "wireshark", "penetration testing", "libreoffice", "vlc"
        ],
        "Là một 'chiếc xe hoàn chỉnh' được đóng gói sẵn từ cùng một cục máy Linux Kernel + bộ khung GNU + trình quản lý gói (apt/dnf) hướng tới từng nhóm người dùng cụ thể (Server, Desktop, hay Bảo mật).",
        "Các Distro dùng chung kiến trúc hạt nhân Linux và cây thư mục chuẩn (FHS), chỉ khác nhau ở chu kỳ hỗ trợ dài hạn (LTS 5–12 năm trên Ubuntu/RHEL), hệ thống quản lý gói (.deb/apt trên Debian/Ubuntu/Mint/Kali; .rpm/dnf trên RHEL/Rocky) và bộ công cụ đi kèm (ví dụ Kali tích hợp sẵn Nmap, Wireshark cho Penetration Testing).",
        "cat /etc/os-release   # Xem tên và phiên bản Distro hiện tại",
        "Server doanh nghiệp & Cloud ưu tiên Ubuntu Server LTS hoặc RHEL/Rocky Linux vì cam kết vá lỗi bảo mật ổn định 5–12 năm."
    ),
    (
        "linux.terminal-shell",
        "Terminal, Shell (Bash / Zsh / Fish) & Trình soạn thảo CLI (Vim / Nano)",
        "SHELL & CLI",
        ["F01"],
        [
            "terminal", "shell", "bash", "zsh", "fish", "sh", "/bin/bash", "/bin/sh",
            "command line", "cli", "gui", "trình thông dịch lệnh", "terminal emulator",
            ".bashrc", "vim", "vi", "nano", ":wq", ":q!", "ctrl+o", "ctrl+x", "ctrl+k",
            "ctrl+u", "clear", "man <lệnh>", "man ls", "man", "ssh", "sysadmin", "dd", "q", "i", "u"
        ],
        "Terminal chỉ là 'cửa sổ màn hình + bàn phím' hiển thị chữ, còn Shell (như Bash/Zsh/Fish) mới là 'người thông dịch' đứng bên trong đọc câu lệnh bạn gõ, phân tích cú pháp và nhờ Kernel thực thi.",
        "Khi quản trị máy chủ từ xa qua giao thức SSH không có giao diện đồ họa (GUI), kỹ sư tương tác hoàn toàn qua Shell và sửa file cấu hình bằng trình soạn thảo dòng lệnh như Nano (`Ctrl+O` lưu, `Ctrl+X` thoát) hoặc Vim (`:wq` lưu & thoát, `:q!` thoát không lưu).",
        "ssh user@server_ip   # Đăng nhập Shell từ xa & sửa cấu hình bằng vim / nano",
        "Gõ `man <tên_lệnh>` (Manual) để tra cứu tài liệu hướng dẫn chính thức của bất kỳ lệnh hay System Call nào ngay trên Terminal."
    ),
    (
        "linux.program-vs-process",
        "Program (Chương trình tĩnh) vs. Process (Tiến trình động · fork/execve)",
        "PROCESS MECHANICS",
        ["F01"],
        [
            "program", "process", "processes", "tiến trình", "chương trình", "fork()", "execve()",
            "fork", "exec", "exec()", "wait()", "exit()", "exit code", "mã thoát", "$?",
            "echo $?", "return 0", "binary executable", "người đầu bếp thực thụ", "công thức nấu ăn"
        ],
        "Program là 'tờ công thức nấu ăn' nằm im trên ổ cứng (tốn Disk, 0% RAM/CPU), còn Process là 'người đầu bếp đang thực sự xào nấu' trên RAM và CPU khi công thức đó được gọi chạy.",
        "Khi chạy lệnh, Shell gọi nhân bản tiến trình con bằng `fork()` và nạp mã máy từ file nhị phân (`Binary Executable` như `/bin/grep`) vào bộ nhớ bằng `execve()`. Khi kết thúc, Process giải phóng tài nguyên và trả về mã thoát (`$?`: `0` = thành công, `1..255` = có lỗi).",
        "grep ERROR /var/log/app.log; echo $?   # 0 nếu tìm thấy, 1 nếu không thấy, 2 nếu lỗi file",
        "Kiểm tra biến `$?` ngay sau câu lệnh là cơ sở để viết nhánh điều kiện `if` và phát hiện lỗi tự động trong Bash Script / CI-CD."
    ),
    (
        "linux.system-call",
        "System Call (Syscall — open, read, write, close, stat, unlink, mmap)",
        "KERNEL & OS CORE",
        ["F01"],
        [
            "system call", "syscall", "system calls", "lời gọi hệ thống", "open()", "open",
            "read()", "read", "write()", "close()", "stat()", "unlink()", "unlink", "rename()",
            "mmap", "virtual memory (mmap)", "o_append", "o_trunc", "user space", "chuyển ngữ cảnh"
        ],
        "Là 'cửa sổ giao dịch hợp pháp duy nhất' để một tiến trình bình thường (User Space) xin Hạt nhân (Kernel Space) thực hiện thao tác nhạy cảm như mở file, đọc ổ đĩa hay ánh xạ bộ nhớ.",
        "Tiến trình không được phép tự ý chọc thẳng xuống phần cứng. Khi gọi `open()` (với cờ `O_TRUNC` ghi đè hoặc `O_APPEND` nối đuôi), `read()`, `write()`, `unlink()` (xóa liên kết file) hay `mmap()` (ánh xạ file vào bộ nhớ ảo), CPU chuyển sang Kernel Mode, kiểm tra quyền trên Inode rồi mới thực thi.",
        "strace -e openat,read,write grep ERROR /var/log/app.log",
        "Lệnh `strace` giúp kỹ sư theo dõi trực tiếp từng System Call mà tiến trình gọi xuống Kernel để chẩn đoán lỗi treo hoặc chậm I/O."
    ),

    # =========================================================================
    # F01: LINUX FUNDAMENTALS — CHẶNG 2 (PROCESS ID CARD, INODE, FHS, CLI)
    # =========================================================================
    (
        "linux.process-identity",
        "Hồ sơ Căn cước Process (PID, UID/GID, Working Directory, Environment, Open Files)",
        "PROCESS MECHANICS",
        ["F01"],
        [
            "pid", "ppid", "uid", "gid", "user/group", "user / group", "2. user / group",
            "working directory", "3. working directory", "current working directory", "cwd",
            "environment", "4. environment", "environment variables", "open files", "5. open files",
            "task_struct", "bộ hồ sơ căn cước", "hồ sơ căn cước", "ulimit", "4. hồ sơ tiến trình & hệ thống",
            "mã định danh duy nhất (id)"
        ],
        "Mỗi Process khi sinh ra đều được Kernel cấp một 'chứng minh thư' (`task_struct`) gồm 5 thuộc tính sống còn quyết định nó là ai, đang đứng ở đâu và được chạm vào tài nguyên nào.",
        "5 thuộc tính cốt lõi: (1) `PID` (Mã số tiến trình duy nhất), (2) `UID/GID` (Danh tính User/Group quyết định quyền hạn), (3) `Working Directory` (Thư mục hiện hành để giải nghĩa đường dẫn tương đối), (4) `Environment` (`$PATH`, `$HOME`...), và (5) `Open Files` (Bảng cổng File Descriptor 0, 1, 2... bị giới hạn trần bởi `ulimit -n`).",
        "ls -l /proc/$$/cwd /proc/$$/fd   # Xem thư mục đứng & các cổng mở của Shell hiện tại",
        "Mọi lỗi 'command not found', 'No such file or directory' hay 'Permission denied' khi chạy tự động đều bắt nguồn từ sự sai lệch của 5 thuộc tính này."
    ),
    (
        "linux.env-path",
        "Biến môi trường ($PATH, $HOME, KEY=VALUE) & Cơ chế Tìm Lệnh",
        "SHELL & CLI",
        ["F01"],
        [
            "$path", "path", "2. search path", "$home", "env", "export", "biến môi trường",
            "usr/local/bin", "/usr/bin", "key=value", "ten=\"nam\"", "$ten", "2. biến (variables)",
            "variables"
        ],
        "`$PATH` là 'danh bạ các ngăn kéo chứa đồ nghề' (như `/usr/local/bin:/usr/bin:/bin`) giúp Shell tự biết phải tìm file thực thi ở đâu khi bạn chỉ gõ tên lệnh ngắn gọn như `grep` hay `python3`.",
        "Khi bạn gõ một lệnh không chứa dấu `/`, Shell quét tuần tự từng thư mục trong biến `$PATH` từ trái sang phải (ngăn cách bởi dấu `:`) và chạy file đầu tiên tìm thấy. Trong Cronjob, `$PATH` mặc định chỉ có `/usr/bin:/bin`, nên các công cụ cài thêm ở `/usr/local/bin` sẽ báo `command not found` nếu không viết đường dẫn tuyệt đối.",
        "echo $PATH; which grep   # -> /bin/grep",
        "Khi gán biến trong Bash (`TEN=\"Nam\"`), tuyệt đối không được để khoảng trắng hai bên dấu `=` vì Shell sẽ hiểu nhầm `TEN` là tên một câu lệnh!"
    ),
    (
        "linux.everything-is-a-file",
        "Triết lý 'Everything is a file' & VFS (Regular File, Directory, /dev, /proc)",
        "FILESYSTEM & INODE",
        ["F01"],
        [
            "everything is a file", "\"everything is a file\" (mọi thứ đều là file)",
            "mọi thứ đều là file", "vfs", "virtual file system", "cửa kính ảo (virtual filesystem)",
            "regular file", "regular files", "1. tệp thông thường", "directory", "directories",
            "2. thư mục", "device interfaces", "3. giao diện thiết bị", "virtual files",
            "block device", "character device", "/dev/sda", "/dev/null", "/dev/tty", "socket"
        ],
        "Ý tưởng thiên tài của UNIX/Linux: biến cả ổ cứng vật lý (`/dev/sda`), hố đen vũ trụ (`/dev/null`), bàn phím lẫn tiến trình đang chạy (`/proc/PID`) thành 'File' để mọi công cụ đều dùng chung đúng bộ lệnh `open() -> read() -> write() -> close()`.",
        "Tầng trừu tượng VFS (Virtual File System) trong Kernel đứng giữa thống nhất giao diện cho 4 nhóm đối tượng: (1) Regular Files (văn bản, mã nguồn, nhị phân), (2) Directories (bảng danh bạ ánh xạ tên sang Inode), (3) Device Interfaces (`/dev/sda`, `/dev/null`), và (4) Virtual Files (`/proc` trên RAM — 0 MB ổ cứng).",
        "ls -ld /etc/hosts /var/log /dev/sda /dev/null /proc/1",
        "Ký tự đầu tiên của `ls -l` chỉ rõ bản chất: `-` (Regular File), `d` (Directory), `b` (Block Device), `c` (Character Device), `l` (Symbolic Link)."
    ),
    (
        "linux.inode",
        "Inode (Index Node), Thư mục (Directory Entry) & Cơ học mv / rm",
        "FILESYSTEM & INODE",
        ["F01"],
        [
            "inode", "index node", "dentry", "directory entry", "hard link", "symlink",
            "soft link", "symbolic link", "ln -s", "stat", "ls -i", "mtime", "mtime timestamp",
            "move & remove", "3. di chuyển, đổi tên & xóa", "recycle bin", "không hề có thùng rác (recycle bin)",
            "disk full 100%"
        ],
        "Inode là 'thẻ căn cước thực sự' của một file trên đĩa (lưu kích thước, UID/GID, quyền `rwx`, mốc thời gian `mtime` và tọa độ các khối dữ liệu vật lý) — chỉ trừ một thứ duy nhất KHÔNG lưu trong Inode là Tên File!",
        "Thư mục (Directory) thực chất chỉ là một bảng danh bạ ánh xạ `Tên_File → Mã_số_Inode`. Vì vậy đổi tên hay di chuyển file (`mv`) trong cùng phân vùng đĩa diễn ra tức thì (chỉ sửa dòng chữ trong danh bạ thư mục, không chạm vào dữ liệu); còn xóa file (`rm` / `unlink()`) trên CLI không đi qua Thùng rác (Recycle Bin) mà gỡ thẳng tên khỏi danh bạ.",
        "ls -li /var/log/app.log; stat /var/log/app.log",
        "Bẫy kinh điển gây `Disk Full 100%`: nếu bạn dùng `rm` xóa một file log khổng lồ khi tiến trình অ্যাপ vẫn đang mở file đó, dung lượng đĩa KHÔNG được giải phóng cho đến khi tiến trình đó đóng file (hoặc dùng `truncate -s 0 file.log`)."
    ),
    (
        "linux.permissions",
        "Quyền hạn File (r=4, w=2, x=1 · Octal 0755/0644) & chmod / chown",
        "SECURITY & PERMISSIONS",
        ["F01"],
        [
            "chmod", "chown", "chgrp", "rwx", "r=4, w=2, x=1", "-rw-r-----", "-rwxr-xr-x",
            "chmod +x", "chmod 755", "chmod 644", "0755", "0644", "permission denied",
            "quyền truy cập", "sudo", "root", "adm", "execute", "5. cấp quyền & chạy"
        ],
        "Cơ chế khóa 3 lớp (User chủ sở hữu · Group nhóm · Others người ngoài) với 3 quyền Đọc (`r=4`), Ghi (`w=2`), Thực thi (`x=1`) gắn trực tiếp trên Inode của mỗi file và thư mục.",
        "Với File thường: `r` = đọc nội dung, `w` = sửa nội dung, `x` = được phép nạp lên RAM chạy như chương trình (`Execute`). Với Thư mục (Directory): `r` = liệt kê danh sách tên file (`ls`), `x` = bước chân vào thư mục (`cd`), và `w` = tạo mới, đổi tên hoặc xóa file nằm trong thư mục đó!",
        "chmod 755 backup.sh   # 7 (4+2+1=rwx) cho User, 5 (4+0+1=r-x) cho Group & Others",
        "Chuẩn bảo mật cho file log nhạy cảm (`/var/log/app.log`) thường là `-rw-r-----` (`0640`, thuộc nhóm `adm`): chỉ chủ sở hữu và nhóm quản trị mới đọc được."
    ),
    (
        "linux.fhs-tree",
        "Cây thư mục chuẩn Linux (FHS: /, /bin, /etc, /var/log, /proc, /tmp) vs. Windows",
        "FILESYSTEM & INODE",
        ["F01"],
        [
            "fhs", "root directory", "cây thư mục", "directory tree", "/", "/bin", "/sbin",
            "/usr", "/etc", "/home", "/root", "/var", "/var/log", "/var/log/app.log",
            "/var/log/backup.log", "/var/www", "/tmp", "/proc", "/opt", "/dev", "mount",
            "mount point", "0 mb trên ổ đĩa cứng", "0 mb", "c:\\", "c:\\windows\\system32",
            "c:\\users", "c:\\temp", "d:\\", "e:\\", "windows", "windows registry",
            "đường dẫn tuyệt đối bắt đầu từ gốc /", "đường dẫn tương đối", "nam",
            "document.txt", "image.png"
        ],
        "Khác với Windows chia ổ `C:\\`, `D:\\` rời rạc và giấu cấu hình trong Windows Registry, Linux hợp nhất mọi ổ đĩa vào một Cây thư mục duy nhất bắt đầu từ gốc `/` (Root Directory) và lưu mọi cấu hình thành file văn bản trong `/etc`.",
        "Quy hoạch chuẩn FHS: `/bin` & `/sbin` (công cụ thiết yếu như `/bin/grep`), `/usr` (phần mềm & thư viện), `/etc` (toàn bộ cấu hình hệ thống), `/var/log` (nhật ký vận hành như `app.log`), `/tmp` (file tạm tự dọn khi Reboot), `/home` (thư mục cá nhân), `/root` (nhà của quản trị viên tối cao), và `/proc` (cửa sổ RAM ảo `0 MB` đĩa giúp nhìn thẳng vào Kernel & Process).",
        "df -h; ls -l / /etc /var/log /proc",
        "Đường dẫn tuyệt đối (Absolute Path) luôn bắt đầu bằng dấu `/` (ví dụ `/var/log/app.log`) nên đứng ở đâu chạy cũng đúng 100%; còn đường dẫn tương đối (`app.log` hay `./backup.sh`) phụ thuộc vào `Working Directory` hiện tại."
    ),
    (
        "linux.cli-navigation",
        "Bộ lệnh Tác chiến CLI (pwd, ls, cd, cp, mv, rm, head, tail -f, find, du, grep)",
        "SHELL & CLI",
        ["F01"],
        [
            "pwd", "ls", "ls -la", "ls -lh", "cd", "cp", "cp -r", "mv", "rm", "rm -rf",
            "mkdir", "mkdir -p", "cat", "less", "head", "tail", "tail -f", "find", "du",
            "du -sh", "df -h", "wc", "wc -l", "grep", "/bin/grep", "navigate", "create & copy",
            "2. tạo & sao chép", "view files", "4. xem & theo dõi log", "search & manual",
            "5. săn lùng & tra cứu", "flags", "k/m/g", "error", "error_timeout"
        ],
        "Bộ 'đồ nghề phẫu thuật' giúp kỹ sư định vị tọa độ (`pwd`, `ls`, `cd`), tạo/chép/xóa (`mkdir -p`, `cp -r`, `mv`, `rm`), theo dõi log trực tiếp (`head`, `tail -f`) và săn lùng dữ liệu (`grep`, `find`, `du -sh`).",
        "3 quy tắc sống còn trên Production Server: (1) Luôn gõ `pwd` kiểm tra vị trí trước khi chạy `rm`; (2) Cấm dùng `cat` mở file log hàng chục GB vì sẽ làm tràn bộ đệm Terminal — hãy dùng `head -n 20`, `less` hoặc `tail -f` (streaming dòng mới theo thời gian thực); (3) Kết hợp `find /var/log -name '*.log'` và `du -sh /var/log/*` để tìm nhanh file log ngốn đĩa.",
        "tail -f /var/log/app.log | grep ERROR",
        "Các cờ (Flags) quan trọng nhất: `-l` (chi tiết Inode/quyền), `-a` (hiện cả file ẩn bắt đầu bằng dấu `.`), `-h` (đổi byte sang KB/MB/GB dễ đọc), `-r` (đệ quy thư mục), `-f` (follow theo dõi trực tiếp ở `tail -f`, hoặc force ở `rm -f`)."
    ),

    # =========================================================================
    # F01: LINUX FUNDAMENTALS — CHẶNG 3 (IPC, FD 0/1/2, PIPE, REDIRECTION)
    # =========================================================================
    (
        "linux.file-descriptors",
        "Ba Cổng Tiêu chuẩn (File Descriptors: 0 = stdin, 1 = stdout, 2 = stderr)",
        "IPC & I/O STREAM",
        ["F01"],
        [
            "file descriptor", "file descriptors", "fd", "fd table", "stdin", "stdout", "stderr",
            "0 = stdin", "1 = stdout", "2 = stderr", "0, 1, 2", "0/1/2", "ba cổng tiêu chuẩn",
            "3 cửa giao nhận hàng độc lập"
        ],
        "Mỗi Process khi khởi chạy đều được Kernel gắn sẵn 3 'cổng giao nhận' đánh số cố định: Cổng `0` (`stdin` — nhận nguyên liệu vào), Cổng `1` (`stdout` — xuất thành phẩm đúng), và Cổng `2` (`stderr` — bắn cảnh báo lỗi riêng biệt).",
        "Thiết kế tách rời Cổng `1` (`stdout`) và Cổng `2` (`stderr`) giúp các đường ống xử lý dữ liệu không bao giờ bị bẩn: khi một lệnh gặp lỗi (ví dụ không đọc được 1 file), thông báo lỗi đi ra Cổng `2` để báo động riêng, không bị lọt vào Cổng `1` làm sai lệch kết quả đếm hoặc làm hỏng file báo cáo.",
        "ls -l /proc/self/fd   # Quan sát 3 cổng 0, 1, 2 trong bảng File Descriptor của tiến trình",
        "Trên Terminal tương tác, cả cổng 1 và cổng 2 đều mặc định nối ra màn hình nên mắt thường nhìn giống nhau, nhưng về mặt cơ học chúng là 2 luồng hoàn toàn độc lập."
    ),
    (
        "linux.pipe",
        "Đường ống Pipe (|) & Giao tiếp Đa tiến trình qua Bộ đệm RAM Kernel (IPC)",
        "IPC & I/O STREAM",
        ["F01"],
        [
            "pipe", "|", "đường ống pipe", "ipc", "interprocess communication",
            "giao tiếp đa tiến trình", "pipe buffer", "64 kb"
        ],
        "Dấu gạch đứng `|` nối thẳng đầu ra Cổng `1` (`stdout`) của tiến trình đứng trước vào đầu vào Cổng `0` (`stdin`) của tiến trình đứng sau thông qua một đường ống bộ nhớ RAM nằm ngay trong Kernel — không tốn 1 byte ghi file tạm xuống ổ cứng!",
        "Khi bạn gõ `cmd1 | cmd2`, Kernel cấp phát một vùng đệm vòng (Ring Buffer ~64 KB trên RAM) và cho cả hai tiến trình chạy song song (concurrently). Dữ liệu vừa nhả ra từ `cmd1` được `cmd2` hút vào xử lý ngay theo kiểu cuốn chiếu (streaming), giúp xử lý file log 50 GB chỉ với vài MB RAM và tốc độ nhanh gấp hàng chục lần so với ghi file trung gian xuống đĩa.",
        "grep ERROR /var/log/app.log | wc -l   # Đếm tức thì số dòng lỗi qua RAM Pipe",
        "Lưu ý: Pipe `|` mặc định chỉ nối Cổng `1` (`stdout`) sang `stdin` của lệnh sau; Cổng `2` (`stderr`) vẫn đi riêng trừ khi bạn chập `2>&1`."
    ),
    (
        "linux.redirection",
        "Điều hướng Dòng chảy I/O (>, >>, <, 2>, 2>&1) & Cơ chế dup2() Chống 'Bẫy Mù Lỗi'",
        "IPC & I/O STREAM",
        ["F01"],
        [
            "redirection", "điều hướng", "2>&1", ">>", ">", "2>", "&1", "dup2()", "dup2",
            "bẫy mù lỗi", "2>&1 >> file", "< input.txt", "<< eof", "> /var/log/backup.log",
            ">> /var/log/backup.log", "đúng chỗ mà cổng số 1 (&1) đang trỏ tới"
        ],
        "Là kỹ thuật 'bẻ đầu vòi nước' của cổng `0`, `1`, `2` từ màn hình sang một file trên đĩa hoặc chập cổng lỗi `2` đi chung vào cổng kết quả `1` (`2>&1`) bằng lời gọi hệ thống `dup2()`.",
        "Phân biệt sống còn: `>` mở file với cờ `O_TRUNC` (xóa trắng file cũ về 0 byte rồi mới ghi đè); `>>` mở file với cờ `O_APPEND` (ghi nối đuôi an toàn vào cuối file). Đặc biệt, Shell đọc cấu hình điều hướng **từ trái sang phải**: viết `>> backup.log 2>&1` sẽ bẻ Cổng `1` vào `backup.log` trước, rồi lấy Cổng `2` cắm vào đúng chỗ Cổng `1` đang trỏ (`backup.log`). Nếu viết ngược `2>&1 >> backup.log`, Cổng `2` bị cắm vào màn hình trước khi Cổng `1` chuyển sang file, khiến mọi báo lỗi biến mất khi chạy ngầm!",
        "/opt/scripts/backup.sh >> /var/log/backup.log 2>&1",
        "Cụm `>> /duong/dan/file.log 2>&1` là mẫu câu bắt buộc phải thuộc nằm lòng cho mọi tác vụ chạy ngầm và Cronjob trên Linux."
    ),

    # =========================================================================
    # F01: LINUX FUNDAMENTALS — CHẶNG 4 (BASH SCRIPT, GCC, MAKEFILE, CRONJOB)
    # =========================================================================
    (
        "linux.bash-scripting",
        "Bash Scripting (.sh), Shebang (#!/bin/bash), Biến, Mảng, Điều kiện & Vòng lặp",
        "AUTOMATION & BUILD",
        ["F01"],
        [
            "bash scripting", "shell script", ".sh", "./backup.sh", "shebang", "#!/bin/bash",
            "#!/usr/bin/env bash", "set -euo pipefail", "if", "for", "while", "3. điều kiện (if / elif / else)",
            "4. vòng lặp (for / while)", "arrays", "functions", "[[ ... ]]", "[[ 10 > 9 ]]",
            "(( ))", "(( 10 > 9 ))", "$(...)", "kq=$(ten_ham)", "$0", "$1", "$2", "my_array=(10 2 300)",
            "unset my_array[1]", "read ten", "echo", "test", "cạm bẫy so sánh chuỗi vs. số học",
            "tờ giấy dán trên tủ lạnh", "thứ tự bảng chữ cái ascii (lexicographical)"
        ],
        "File Bash Script (`.sh`) là 'bản quy trình tự động hóa' đóng gói hàng loạt lệnh CLI kèm biến số, mảng (`Arrays`), hàm (`Functions`), rẽ nhánh (`if/elif/else`) và vòng lặp (`for/while`) để máy chủ thực thi không cần người gõ từng dòng.",
        "Dòng đầu tiên `#!/bin/bash` (Shebang) chỉ định trình thông dịch. Cạm bẫy kinh điển trong Bash là so sánh số học: toán tử `>` trong `[[ \"10\" > \"9\" ]]` so sánh theo thứ tự chữ cái ASCII (ký tự `'1'` đứng trước `'9'` nên `\"10\" < \"9\"` trả về False!). Để so sánh giá trị toán học thực sự, bắt buộc dùng cờ `-gt / -lt / -eq` hoặc cặp ngoặc số học `(( 10 > 9 ))`.",
        "#!/bin/bash\nset -euo pipefail\nif (( dung_luong_gb > 80 )); then echo 'Cảnh báo đầy đĩa!'; fi",
        "Luôn dùng `$(lệnh)` (Command Substitution) để hứng kết quả đầu ra `stdout` của một lệnh gán vào biến (ví dụ `NGAY=$(/bin/date +%F)`)."
    ),
    (
        "linux.gcc-compilation",
        "Trình biên dịch GCC & Dây chuyền 4 Bước (.c → .o Object File → Executable)",
        "AUTOMATION & BUILD",
        ["F01"],
        [
            "gcc", "g++", "compilation", "compiler", "trình biên dịch", "source code",
            "bản chất mã nguồn (source code)", "object file", "linker", "machine code",
            "c", "c++", "c/c++", ".c", ".cpp", ".o", "elf", "-wall", "-o2", "-c", "-o",
            "file ung_dung", "lò luyện kim"
        ],
        "CPU không hiểu được văn bản mã nguồn C/C++ (`.c`/`.cpp`); trình biên dịch GCC đóng vai trò 'lò luyện kim' dịch mã nguồn thành file đối tượng trung gian (`.o`) rồi qua bộ ghép nối (Linker) tạo ra file thực thi mã máy (`Executable`).",
        "Tại sao dự án thực tế luôn tách thành 2 bước (`gcc -c main.c -o main.o` rồi mới ghép các file `.o` thành `ung_dung`)? Vì một dự án có hàng nghìn file `.c`, nếu sửa 1 dòng trong `main.c` mà dịch lại tất cả sẽ mất hàng giờ. Tách ra file trung gian `.o` giúp ta chỉ cần biên dịch lại đúng file `.c` vừa sửa rồi nối (Link) lại với các file `.o` cũ trong vài giây!",
        "gcc -Wall -O2 -c main.c -o main.o && gcc main.o ham_phu.o -o ung_dung",
        "Cờ `-c` bảo GCC dừng lại ở bước tạo Object File (`.o`); cờ `-o` đặt tên file đầu ra; `-Wall` bật toàn bộ cảnh báo lỗi; `-O2` tối ưu hóa tốc độ mã máy."
    ),
    (
        "linux.makefile",
        "Makefile & Công cụ GNU Make (Target : Prerequisites → [TAB] Recipe & .PHONY)",
        "AUTOMATION & BUILD",
        ["F01"],
        [
            "makefile", "make", "gnu make", ".phony", "target", "prerequisites", "recipe",
            "tab", "incremental build", "all", "clean", "build", "người quản đốc phân xưởng thông minh",
            "file nào vừa sửa cần biên dịch lại?"
        ],
        "Makefile là 'người quản đốc phân xưởng thông minh': tự động nhìn mốc thời gian sửa đổi (`mtime` trên Inode) của từng file nguyên liệu (`Prerequisites`) so với sản phẩm đích (`Target`) để chỉ chạy lại đúng những bước thực sự cần thiết.",
        "Cấu trúc một quy tắc gồm: `Target: Prerequisites` và dòng lệnh thực thi (`Recipe`) bên dưới **bắt buộc phải thụt đầu dòng bằng đúng phím `[TAB]`** (nếu dùng phím Space, Make sẽ từ chối chạy). Nhãn `.PHONY: all clean` khai báo các tên tác vụ điều khiển không phải là tên file vật lý trên ổ đĩa.",
        ".PHONY: all clean\nung_dung: main.o ham_phu.o\n\t$(CC) $(CFLAGS) main.o ham_phu.o -o ung_dung",
        "Khi bạn gõ `make`, nếu `main.c` có `mtime` mới hơn `main.o`, Make chỉ dịch lại `main.o` và ghép lại `ung_dung`, bỏ qua hoàn toàn `ham_phu.o` chưa hề thay đổi."
    ),
    (
        "linux.cronjob",
        "Hệ thống Hẹn giờ Tự động (Cron / crond / crontab, Anacron & systemd Timers)",
        "AUTOMATION & BUILD",
        ["F01"],
        [
            "cron", "crond", "crontab", "cronjob", "crontab -e", "crontab -l", "anacron",
            "systemd", "systemd timers", "journald", "persistent=true", "* * * * *",
            "*/5 * * * *", "0 2 * * *", "0 0 1 * *", "0 9-17 * * *", "30 8 * * 1",
            "phút giờ ngày tháng thứ", "every minute", "no auto-retry", "missed jobs",
            "giới hạn 4: không tự thử lại khi lỗi (no auto-retry — slide 75)",
            "giới hạn 5: mất lịch khi máy tắt nguồn (missed jobs — slide 75–76)",
            "hệ thống trực ban tòa nhà", "cuốn sổ lịch trình (bảng thời gian biểu)"
        ],
        "Tiến trình nền `crond` thức trực 24/7, cứ mỗi phút lại đối chiếu đồng hồ hệ thống với bảng 5 ngôi sao `crontab` (`Phút · Giờ · Ngày · Tháng · Thứ`) để tự động kích hoạt script đúng lịch trình.",
        "Bên cạnh 3 cạm bẫy môi trường (`Working Directory`, `$PATH` tối giản, mất `stdout/stderr` nếu thiếu `>> log 2>&1`), Cron truyền thống còn có 2 giới hạn kiến trúc lớn: (1) `No Auto-Retry` (script lỗi không tự chạy lại) và (2) `Missed Jobs` (nếu máy tắt nguồn đúng lúc 02:00 sáng, khi bật máy lại lúc 08:00 Cron sẽ bỏ qua luôn việc đã lỡ). Để khắc phục, kỹ sư dùng `Anacron`, `systemd Timers` (`Persistent=true`) hoặc trình điều phối hiện đại như Apache Airflow.",
        "0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1",
        "Mẹo nhớ nhanh 5 trường thời gian Crontab từ trái sang phải: `Phút (0-59)` → `Giờ (0-23)` → `Ngày_trong_tháng (1-31)` → `Tháng (1-12)` → `Thứ_trong_tuần (0-7)`."
    ),

    # =========================================================================
    # D02: STORAGE LAYER — CHẶNG 1 (HARDWARE HIERARCHY, RAM, SEEK/SCAN, OLTP/OLAP)
    # =========================================================================
    (
        "storage.latency-hierarchy",
        "Tháp Độ trễ Phần cứng (L1/L2/L3 Cache → RAM → NVMe SSD → HDD → Cloud Object)",
        "HARDWARE & STORAGE PHYSICS",
        ["D02"],
        [
            "cache hierarchy", "tháp độ trễ", "l1", "l2", "l3", "l1 cpu cache",
            "l2 / l3 cpu cache", "cache 1ns", "cpu", "hardware", "network", "storage",
            "latency", "query latency", "sub-millisecond", "bậc thang phần cứng",
            "định luật kim tự tháp", "3 hiệu ứng đòn bẩy phần cứng (hardware leverage)",
            "hạ tầng mạng (network performance) và cpu", "độ trễ truy xuất"
        ],
        "Quy luật vật lý bất biến: thiết bị lưu trữ càng nằm gần nhân CPU thì tốc độ càng nhanh gấp hàng nghìn lần nhưng giá tiền trên mỗi GB càng đắt đỏ và dung lượng càng nhỏ.",
        "Các bậc thang độ trễ chuẩn: L1/L2/L3 Cache (~1–10 ns, ~1 TB/s, nằm ngay trên đế chip CPU) → RAM DDR5 (~100 ns, ~100 GB/s, ~$10/GB, khả biến) → NVMe SSD (~100 µs, ~4 GB/s, ~$0.20/GB) → HDD cơ học (~4–10 ms seek, ~100 IOPS, ~$0.03/GB) → Cloud Object Storage S3/GCS (~100 ms độ trễ gói tin đầu, ~$0.02/GB/tháng) → Archival Glacier (~12 giờ chờ, ~$0.004/GB/tháng).",
        "L1/L2 Cache (1–10 ns) → RAM (100 ns) → NVMe SSD (100 µs) → HDD (4–10 ms) → S3 Object (100 ms)",
        "Mọi kiến trúc dữ liệu hiện đại (In-Memory Caching, Columnar Pruning, Tiered Storage) đều được thiết kế xoay quanh việc khai thác chênh lệch độ trễ này."
    ),
    (
        "storage.ram-spill",
        "RAM (Bộ nhớ khả biến — Volatile) & Hiện tượng Tràn bộ nhớ (Spill-to-Disk)",
        "HARDWARE & STORAGE PHYSICS",
        ["D02"],
        [
            "ram", "1 gb ram", "ddr5", "dram", "volatile", "volatility", "khả biến",
            "nonvolatile", "bất khả biến", "persistence", "lưu trữ bền vững (persistence)",
            "spill-to-disk", "spill to disk", "tràn bộ nhớ", "out of memory", "oom"
        ],
        "RAM cực nhanh (~100 ns, hàng triệu IOPS) nhưng mất sạch dữ liệu khi mất điện (Volatile) và rất đắt; khi một tác vụ JOIN/GROUP BY vượt quá dung lượng RAM, hệ thống buộc phải 'tràn' dữ liệu tạm xuống ổ cứng (Spill-to-Disk) làm tốc độ rơi tự do hàng nghìn lần.",
        "Trong các động cơ phân tán như Apache Spark, Snowflake hay PostgreSQL (`work_mem`), khi bảng băm (Hash Table) hoặc bộ đệm sắp xếp (Sort Buffer) phình quá ngưỡng RAM cấp phát, tiến trình phải tuần tự hóa (serialize) dữ liệu trên RAM, ghi tạm xuống SSD/HDD rồi đọc ngược lên lại, gây nghẽn cổ chai I/O và CPU nghiêm trọng.",
        "RAM (~100 ns) ──[Spill-to-Disk]──> NVMe SSD (~100 µs, chậm 1.000x) / HDD (~10 ms, chậm 100.000x)",
        "Cách phòng tránh Spill-to-Disk: cắt tỉa cột/dòng sớm (Column Pruning & Predicate Pushdown), xử lý nghiêng dữ liệu (Data Skew) và dùng Broadcast Join cho bảng nhỏ."
    ),
    (
        "storage.seek-vs-scan",
        "Random Seek (IOPS) vs. Sequential Scan (Bandwidth) & Đọc Song song trên Cloud",
        "HARDWARE & STORAGE PHYSICS",
        ["D02"],
        [
            "random seek", "sequential scan", "sequential i/o", "disk i/o", "seek", "iops",
            "100 iops", "256.000 iops", "maximum bandwidth", "bandwidth", "capacity",
            "dung lượng (capacity)", "storage capacity", "nvme ssd", "hdd", "đĩa từ cơ học",
            "parallel reads", "định luật cơ học đĩa", "định luật đám mây song song",
            "đọc song song (parallel reads) & phân bổ 3 tài sản đĩa",
            "(1) dung lượng lưu trữ (storage capacity — ví dụ 10 tb)",
            "(2) số thao tác vào/ra mỗi giây (iops — ví dụ hdd chỉ đạt ~100 iops)",
            "(3) băng thông tối đa (maximum bandwidth — đọc tuần tự đạt 200–300 mb/s)"
        ],
        "Random Seek giống như 'nhảy cóc tìm từng trang sách rải rác' (bị bóp nghẹt bởi số lần nhảy mỗi giây — IOPS), còn Sequential Scan là 'đặt ngón tay đọc trượt một mạch từ đầu đến cuối chương' để đạt tốc độ băng thông tối đa (MB/s – GB/s).",
        "Ba tài sản giới hạn của mọi ổ đĩa: (1) Capacity (Dung lượng TB/PB), (2) IOPS (Số thao tác đọc/ghi ngẫu nhiên mỗi giây — HDD cơ học bị khóa ở ~100 IOPS do kim đọc phải di chuyển vật lý mất 4–10 ms; NVMe SSD đạt tới 256.000+ IOPS), và (3) Maximum Bandwidth (Tốc độ đọc tuần tự liền mạch: HDD đạt 200–300 MB/s, NVMe SSD đạt ~4 GB/s). Trên Cloud Object Storage (S3/GCS), độ trễ 1 luồng cao (~100 ms), nhưng khi mở hàng trăm kết nối đọc tuần tự song song (Parallel Reads), băng thông cộng gộp đạt nhiều GB/s.",
        "Random Seek 10.000 dòng trên HDD (~100 IOPS) = 100 giây vs. Sequential Scan 100 MB liền mạch = 0.4 giây!",
        "Đây là lý do các định dạng phân tích như Parquet và động cơ LSM-Tree luôn gom dữ liệu thành các khối lớn để đọc/ghi tuần tự thay vì nhảy cóc ngẫu nhiên."
    ),
    (
        "storage.data-temperature",
        "Phân tầng Nhiệt độ Dữ liệu (Hot / Warm / Cold Tiering), Lifecycle & Độ bền 11 Nines",
        "CLOUD & FINOPS",
        ["D02"],
        [
            "data temperature", "3 mức nhiệt độ (data temperature)", "nhiệt độ dữ liệu",
            "nhiệt độ lưu trữ", "hot tier", "warm tier", "cold tier", "archival",
            "archival storage", "archive 12h", "glacier", "aws glacier", "standard-ia",
            "one zone-ia", "minimum storage duration", "retrieval fee", "phí kéo dữ liệu (retrieval fee)",
            "11 nines", "99.999999999%", "availability zones", "lifecycle policy",
            "lifecycle policies", "storage lifecycle management", "amazon s3 (object storage - warm tier)"
        ],
        "Dữ liệu giống như thức ăn: món đang nấu ăn ngay để trên bàn bếp (`Hot` — RAM/SSD), nguyên liệu dùng trong tuần cất tủ mát (`Warm` — S3 Standard ~$0.02/GB), còn hóa đơn lưu trữ 5–10 năm đóng thùng cất kho đông lạnh (`Cold/Archival` — Glacier ~$0.004/GB, rẻ bằng 1/17).",
        "Các chính sách `Storage Lifecycle Management` tự động chuyển dữ liệu cũ từ tầng Hot/Warm sang `Standard-IA`, `One Zone-IA` hoặc `Glacier` dựa theo tuổi dữ liệu mà vẫn đảm bảo độ bền `11 Nines` (99.999999999% — tự động sao lưu qua tối thiểu 3 Availability Zones cách biệt). Tuy nhiên cần lưu ý 2 ràng buộc thương mại của tầng lạnh: `Minimum Storage Duration` (phí phạt nếu xóa sớm trước 30/90/180 ngày) và `Retrieval Fee` (phí tính trên mỗi GB đọc phục hồi).",
        "Hot (RAM/SSD: 100ns–100µs) → Warm (S3/GCS: ~100ms, $0.02/GB) → Cold (Glacier: ~12h, $0.004/GB)",
        "Tuyệt đối không để các job BI hàng ngày quét nhầm vào phân vùng đã chuyển xuống tầng Glacier vì hóa đơn Retrieval Fee sẽ tăng vọt."
    ),
    (
        "storage.oltp-vs-olap",
        "Hệ thống Giao dịch (OLTP — Source System) vs. Hệ thống Phân tích (OLAP — Storage System)",
        "DATA ARCHITECTURE",
        ["D02"],
        [
            "oltp", "olap", "source system", "storage system", "online transaction processing",
            "online analytical processing", "row-oriented", "column-oriented", "operational data",
            "external data", "#8888", "đơn hàng #8888", "đơn #8888", "ma_don = 8888", "mã đơn: 8888",
            "(order_id = 8888)", "bi", "batch bi"
        ],
        "OLTP là 'quầy thu ngân siêu thị' chuyên ghi nhận từng giao dịch lẻ (như Đơn hàng `#8888`) trong tích tắc (~1 ms), còn OLAP là 'phòng phân tích chiến lược' chuyên quét hàng trăm triệu đơn hàng lịch sử để tính tổng doanh thu và huấn luyện AI.",
        "Sự đối lập cơ học buộc phải tách rời hai hệ thống: OLTP tối ưu cho `INSERT/UPDATE/DELETE` điểm lẻ bằng lưu trữ theo dòng (`Row-oriented`), mô hình chuẩn hóa (`3NF`) và chỉ mục `B-Tree` trên NVMe SSD; ngược lại OLAP tối ưu cho truy vấn quét lớn (`Sequential Scan` + `GROUP BY`) bằng lưu trữ theo cột (`Columnar`), nén cao và mô hình phi chuẩn hóa (`Star Schema` / `OBT`) trên Object Storage.",
        "OLTP (PostgreSQL/MySQL: Row, <1ms point lookup) ──[CDC / Ingestion]──> OLAP (Snowflake/BigQuery/Lakehouse: Columnar)",
        "Nhân vật chính `Đơn hàng #8888` sinh ra tại DB giao dịch OLTP ở Trạm 1, sau đó hành trình qua Kafka/Parquet/Lakehouse để phục vụ phân tích OLAP ở các Chặng tiếp theo."
    ),

    # =========================================================================
    # D02: STORAGE LAYER — CHẶNG 2 (FILE/BLOCK/OBJECT, PARQUET, AVRO, ARROW, COMPRESSION)
    # =========================================================================
    (
        "storage.file-block-object",
        "Ba Mô hình Lưu trữ Cơ sở: File Storage vs. Block Storage vs. Object Storage",
        "STORAGE ARCHITECTURE",
        ["D02"],
        [
            "file storage", "block storage", "block storage (\"các mảnh ghép lego đánh số\"):",
            "object storage", "file", "block", "object", "bucket", "flat with buckets",
            "files and folders", "nas", "san", "aws ebs", "ebs", "amazon s3", "s3", "adls",
            "adls gen2", "gcs", "ext4", "ntfs", "nfs", "smb", "posix", "object key",
            "(1) id (object key", "unique id", "immutable objects", "immutability", "immutable",
            "4kb", "4kb–512kb", "512kb", "tách rời compute và storage",
            "tách rời hoàn toàn compute và storage", "chọn mô hình kho (storage model):"
        ],
        "File Storage là 'tủ hồ sơ chia ngăn thư mục lồng nhau' (`NAS/ext4`), Block Storage là 'các khối gạch Lego đánh số tốc độ cực cao' gắn cho DB/VM (`SAN/AWS EBS`), còn Object Storage là 'bãi đỗ xe Valet phẳng khổng lồ' quản lý bằng vé ID qua HTTP API (`S3/GCS/ADLS`).",
        "File Storage phân cấp theo cây thư mục nên nghẽn khóa Inode khi vượt hàng chục triệu tệp. Block Storage chia đĩa thành các khối cố định (`4KB–512KB`) độ trễ `< 1 ms` (~256.000 IOPS) cho CSDL OLTP. Object Storage đóng gói mỗi tệp thành 3 phần (`Object Key ID` + `Metadata` tùy biến + `Binary Data` bất biến) trong không gian phẳng (`Bucket`), cho phép tách rời hoàn toàn Compute và Storage ở quy mô Petabyte/Exabyte với giá chỉ ~$0.02/GB/tháng.",
        "s3://ashley-data-lake/orders/year=2026/0003_8888.parquet   # Object Key phẳng trên S3",
        "Tính bất biến (`Immutable Objects`) của S3 có nghĩa là bạn không thể sửa 1 dòng giữa tệp Parquet trên S3 mà phải ghi thành một Object mới (đây chính là tiền đề sinh ra cơ chế COW/MOR ở Chặng 6)."
    ),
    (
        "storage.serialization-avro-csv",
        "Tuần tự hóa Dữ liệu (Serialization) & Định dạng Dòng: CSV, JSONL, XML, Protobuf, Apache Avro",
        "FILE FORMATS & SERIALIZATION",
        ["D02"],
        [
            "serialization", "deserialization", "serialize / deserialize", "serde overhead",
            "parse overhead", "reserializing overhead", "tuần tự hóa", "csv", "json", "jsonl",
            "xml", "protobuf", "apache avro", "avro", "sync marker", "sync markers 16-byte",
            "16-byte sync marker", "row-based", "self-describing formats", "self-describing",
            "binary", "nhị phân (binary)", "structured data", "semi-structured",
            "bán cấu trúc (semi-structured):", "unstructured", "unstructured data",
            "phi cấu trúc (unstructured):", "analog / iot data", "file format"
        ],
        "Tuần tự hóa (`Serialization`) là cách 'đóng thùng' cấu trúc dữ liệu trên RAM thành chuỗi byte để ghi xuống đĩa hoặc gửi qua mạng; trong đó định dạng theo dòng (`CSV`, `JSON`, `Avro`) xếp toàn bộ các cột của cùng một đơn hàng `#8888` nằm liền kề nhau.",
        "CSV và JSON là văn bản thuần nên tốn dung lượng và ngốn CPU phân tích cú pháp (`Parse/SerDe overhead`). **Apache Avro** là chuẩn tuần tự hóa theo dòng dạng nhị phân (`Binary`) tự mô tả (`Self-describing`): nhúng thẳng lược đồ JSON ở phần Header, phần thân nén nhị phân không lặp lại tên trường và chèn các mốc đồng bộ `16-byte Sync Marker` giữa các khối, giúp Avro vừa cực nhanh cho luồng ghi Kafka/CDC vừa cắt nhỏ để đọc song song được (`Splittable`).",
        "[Avro File Header: JSON Schema] → [Data Block 1 + 16-byte Sync Marker] → [Data Block 2]",
        "Khi nào chọn Avro vs. Parquet? Dùng **Avro** khi cần ghi/đọc trọn vẹn từng bản ghi (Kafka message, CDC landing, Hudi MOR log `.log.avro`); dùng **Parquet** khi cần truy vấn phân tích cột trên kho dữ liệu."
    ),
    (
        "storage.parquet-columnar",
        "Lưu trữ theo Cột (Columnar): Apache Parquet, Apache ORC & Giải phẫu Row Group / Footer",
        "FILE FORMATS & SERIALIZATION",
        ["D02"],
        [
            "apache parquet", "parquet", "apache orc", "orc", "columnar", "row group",
            "row groups", "row groups / data pages", "column chunk", "data page", "footer",
            "parquet footer", "par1", "column pruning", "pruning", "predicate pushdown",
            "data skipping", "min/max", "[min, max]", "min / max / null count",
            "lower_bound / upper_bound", "numrecords, minvalues, maxvalues, nullcount",
            "dictionary encoding", "delta encoding", "rle", "run-length encoding",
            "google dremel", "definition level", "definition levels", "repetition level",
            "repetition levels", "http range request", "0003_8888.parquet", "3.parquet",
            "3_v2.parquet", "50 mb – 500 mb", "80–95% i/o", "nén chuyên biệt theo cột"
        ],
        "Thay vì xếp từng hàng ngang, Parquet xoay dọc bảng dữ liệu: gom toàn bộ giá trị của cùng một cột trong mỗi phân đoạn (`Row Group` 128MB–1GB) nằm sát cạnh nhau, giúp câu lệnh phân tích chỉ cần bốc đúng cột cần tính và nén nhỏ dung lượng gấp 4–10 lần.",
        "Giải phẫu tệp Parquet gồm 4 phần: `Header ('PAR1')` → Các `Row Group` (mỗi Row Group chứa từng `Column Chunk`, bên trong chia thành các `Data Page` nén bằng `Dictionary Encoding`, `RLE`, `Delta Encoding`) → `Footer` nằm ở cuối tệp. Khi truy vấn, động cơ đọc **Footer đầu tiên** (qua HTTP Range Request) để: (1) **Column Pruning** (nhảy đến đúng Byte Offset của cột trong `SELECT`, bỏ qua 80–95% I/O các cột thừa), và (2) **Data Skipping / Predicate Pushdown** (đọc thống kê `[Min, Max, Null Count]` của từng Row Group để nhảy qua nguyên khối không chứa Đơn hàng `#8888`).",
        "Parquet Footer [Schema + RowGroup Min/Max + Byte Offsets] ──[Range GET]──> Chỉ tải đúng Column Chunk cần thiết",
        "Parquet dùng thuật toán **Google Dremel** (`Definition Levels` & `Repetition Levels`) để tháo rời các trường JSON/Struct/Array lồng nhau nhiều cấp thành các cột phẳng mà vẫn ghép lại chính xác 100%."
    ),
    (
        "storage.apache-arrow",
        "Apache Arrow — Chuẩn Bộ nhớ Cột Trong RAM (In-Memory Columnar) & Zero-Copy",
        "IN-MEMORY ENGINE",
        ["D02"],
        [
            "apache arrow", "arrow", "in-memory serialization", "zero-copy", "zero copy",
            "simd", "vectorized execution", "pyarrow", "polars", "shredding", "jvm"
        ],
        "Nếu Parquet là 'thùng hàng nén chặt tối ưu để cất trên ổ đĩa/S3', thì Apache Arrow là 'khay nguyên liệu bày sẵn theo cột ngay trên thanh RAM' giúp Spark (`JVM`), Python (`Pandas/Polars`) và `C++` đọc chung tức thì mà không tốn CPU dịch qua dịch lại.",
        "Trước khi có Arrow, việc truyền bảng dữ liệu giữa các tiến trình khác ngôn ngữ trên cùng máy chủ tốn 70–80% thời gian CPU chỉ để Serialize và Deserialize. Arrow chuẩn hóa bố cục byte dạng cột thẳng hàng trên RAM (hỗ trợ cả `Shredding` cho dữ liệu bán cấu trúc lồng nhau và ánh xạ trực tiếp qua `mmap`), cho phép các động cơ đọc trực tiếp qua con trỏ bộ nhớ (`Zero-Copy`) và chạy tính toán vector hóa (`SIMD`) trên CPU hiện đại.",
        "Spark JVM ──[Con trỏ RAM Apache Arrow (Zero-Copy, 0% Serialize)]──> Python / Pandas / Polars / DuckDB",
        "Cặp bài trùng chuẩn công nghiệp: Lưu trên đĩa S3 bằng **Apache Parquet** → Nạp lên RAM xử lý bằng **Apache Arrow**."
    ),
    (
        "storage.compression-splittability",
        "Nén Dữ liệu (Snappy, ZSTD, LZ4, Gzip, Bzip2) & Cạm bẫy Tính Phân tách (Splittability)",
        "FILE FORMATS & SERIALIZATION",
        ["D02"],
        [
            "compression", "codecs", "lossy", "splittability", "splittable", "non-splittable",
            "tính phân tách", "nén chặt mà vẫn chia nhỏ được?", "snappy", "zstd", "zstandard",
            "lz4", "gzip", ".gz", "bzip2", "lzo"
        ],
        "Một tệp dữ liệu lớn muốn được 100 máy chủ đọc song song thì phải 'cắt khúc được ở giữa' (`Splittable`). Nếu nén nguyên tệp CSV 100 GB bằng Gzip (`.csv.gz`), cả 99 máy chủ phải ngồi chơi nhìn 1 máy chủ duy nhất đọc tuần tự từ byte đầu tiên!",
        "Các thuật toán nén trong kỹ thuật dữ liệu bắt buộc phải là **Lossless** (không mất mát thông tin, khác với nén ảnh/nhạc `Lossy`). `Gzip` không có mốc đánh dấu khối nên `Non-splittable` khi bọc ngoài tệp CSV/JSON nguyên khối. Ngược lại, khi dùng định dạng Container như **Parquet** (chia theo `Row Group`) hoặc **Avro** (chia theo `Sync Marker 16-byte`) kết hợp codec **ZSTD** hoặc **Snappy / LZ4** nén từng trang bên trong, tệp vừa giữ nguyên tính `Splittable` 100% cho 100 máy chủ đọc song song, vừa giải nén cực nhanh.",
        "orders.csv.gz (100GB, Non-splittable: 1 CPU chạy) vs. orders.zstd.parquet (Splittable: 100 CPU đọc song song)",
        "Khuyến nghị thực chiến: dùng **ZSTD** hoặc **Snappy** bên trong Parquet; dùng **LZ4/Snappy** cho luồng streaming Apache Kafka."
    ),

    # =========================================================================
    # D02: STORAGE LAYER — CHẶNG 3 (HDFS, TOPOLOGY, CACHE, KAFKA/CDC, DATA WAREHOUSE)
    # =========================================================================
    (
        "storage.hdfs",
        "Hadoop HDFS (NameNode, DataNode, Nhân bản x3, Self-healing & Erasure Coding RS 6,3)",
        "DISTRIBUTED STORAGE",
        ["D02"],
        [
            "hdfs", "hadoop", "google file system (gfs)", "gfs", "namenode", "datanode",
            "datanodes", "datanodes (\"đội thủ kho trực tiếp giữ hàng\"):", "nhân bản x3",
            "replication factor x3", "3x replication", "3 bản sao (x3)", "x3", "self-healing",
            "erasure coding", "reed-solomon", "rs(6,3)", "editlog", "fsimage", "heartbeat",
            "blockreport", "128 mb", "block size", "block splitting", "data blocks",
            "colocation of compute and storage", "colocate", "map tasks",
            "chia khối (block splitting) & đặt chung tính toán – lưu trữ (colocation of compute and storage):",
            "cơ chế nhân bản chống lỗi (replication factor x3) & tự chữa lành (self-healing):"
        ],
        "Lấy cảm hứng từ Google File System (GFS), HDFS biến hàng trăm máy chủ phổ thông thành một kho lưu trữ khổng lồ bằng cách chặt tệp lớn thành các khối `128 MB`, giao cho `NameNode` giữ sổ danh bạ trên RAM và rải 3 bản sao (`x3`) xuống các `DataNode` để hỏng máy nào cũng tự chữa lành (`Self-healing`).",
        "Nguyên lý cốt lõi của HDFS là **Colocation of Compute and Storage** (đặt chung tính toán và lưu trữ trên cùng một node vật lý): thay vì kéo 10 TB dữ liệu qua mạng về 1 máy tính toán, HDFS gửi đoạn code nhỏ (`Map tasks`) đến chạy ngay trên các `DataNode` đang giữ khối dữ liệu đó. Khi dữ liệu nguội dần, để giảm chi phí lưu trữ 200% phụ trội của nhân bản `x3`, kỹ sư chuyển sang **Erasure Coding `RS(6,3)`** (6 khối dữ liệu + 3 khối chẵn lẻ toán học, chịu được 3 máy sập cùng lúc nhưng chỉ tốn `1.5x` dung lượng).",
        "Block #8888 (128MB) → Bản sao 1 (Node A, Rack 1) + Bản sao 2 (Node C, Rack 2) + Bản sao 3 (Node D, Rack 2)",
        "`NameNode` nhận tín hiệu báo sống (`Heartbeat`) và báo cáo khối (`Blockreport`) từ các `DataNode` mỗi vài giây; hễ thấy khối nào tụt xuống dưới 3 bản sao là lập tức ra lệnh nhân bản bù."
    ),
    (
        "storage.network-topology-cache",
        "Tô-pô Mạng (Data-Local → Rack-Local → Off-Rack) & Động cơ Cache (Redis, Memcached, RocksDB / LSM-Tree)",
        "DISTRIBUTED STORAGE",
        ["D02"],
        [
            "network topology", "rack topology", "tô-pô mạng", "khoảng cách mạng",
            "data locality", "data-local", "rack-local", "off-rack", "rack awareness",
            "rack-aware replica placement", "racks", "tor switch", "top-of-rack switch",
            "core switch", "hot data caching", "hazelcast", "redis", "memcached",
            "rdb snapshots", "aof", "rdb/aof", "ttl - time to live", "rocksdb", "lsm-tree",
            "log-structured merge-tree", "lsm", "b-tree", "memtable", "sstable",
            "quy tắc đặt bản sao nhận biết tủ mạng (rack-aware replica placement):",
            "bản sao 1 trên node cục bộ ở rack 1", "bản sao 2 sang một node ở rack 2",
            "bản sao 3 ở một node khác ngay trong cùng rack 2"
        ],
        "Vì băng thông mạng liên tủ (`Off-Rack` qua Core Switch) luôn là cổ chai hẹp nhất, hệ thống phân tán luôn ưu tiên đọc tại chỗ (`Data-Local` → `Rack-Local`) và dùng bộ nhớ đệm (`Redis/Memcached` trên RAM, `RocksDB` trên SSD) để tăng tốc truy xuất.",
        "Quy tắc **Rack-aware Replica Placement** đặt Bản sao 1 tại máy cục bộ (Rack 1), Bản sao 2 sang tủ mạng khác (Rack 2 — chống sập nguồn cả tủ Rack 1), và Bản sao 3 ở một máy khác trong cùng Rack 2 (tiết kiệm băng thông liên tủ). Ở tầng Cache & State: **Memcached** là bộ đệm Key-Value đa luồng thuần RAM; **Redis** hỗ trợ cấu trúc dữ liệu phong phú kèm lưu bền vững (`RDB Snapshots` + `AOF`); còn **RocksDB** dùng cấu trúc **LSM-Tree** (`Log-Structured Merge-tree`) ghi nối đuôi vào RAM `MemTable` rồi xả tuần tự xuống các tệp `SSTable` trên SSD.",
        "Khoảng cách mạng: (1) Data-Local (0 hop) < (2) Rack-Local (qua ToR Switch) < (3) Off-Rack (qua Core Switch)",
        "Cơ chế `TTL (Time to Live)` tự động xóa dữ liệu đệm hết hạn để giải phóng RAM đắt đỏ."
    ),
    (
        "storage.kafka-cdc",
        "Streaming Storage: Apache Kafka (Append-only Log), CDC & Kiến trúc Stream-to-Batch",
        "STREAMING & CDC",
        ["D02"],
        [
            "apache kafka", "kafka", "apache kafka & cdc", "apache kafka (append-only log)",
            "streaming storage", "message queues", "producer", "consumer", "batch storage consumer",
            "stream-to-batch", "kiến trúc stream-to-batch:", "cdc", "change data capture",
            "debezium", "append-only log", "append-only", "append", "nối đuôi", "offset",
            "replay", "retention", "tiered storage", "apache flink", "flink", "kafka streams",
            "apache spark structured streaming", "kinesis", "real-time", "thời gian thực (real-time)",
            "data in flight"
        ],
        "Thay vì chờ cuối ngày mới gom dữ liệu một cục (`Batch`), **CDC (Change Data Capture)** bắt ngay từng nhịp thay đổi (`INSERT/UPDATE/DELETE`) từ sổ nhật ký của DB nguồn và bắn vào cuộn băng nối đuôi bất biến của **Apache Kafka** để cả luồng Real-time lẫn kho phân tích cùng đọc tức thì.",
        "Khác với hàng đợi tin nhắn truyền thống (`Message Queues` xóa tin ngay sau khi đọc), Kafka lưu sự kiện vào các tệp **Append-only Log** có đánh số thứ tự `Offset` tăng dần và giữ lại theo chính sách `Retention` (hoặc đẩy xuống S3 qua `Tiered Storage`). Nhờ đó, một sự kiện Đơn hàng `#8888` từ `Producer` gửi vào có thể được đọc đồng thời bởi hai nhánh (`Stream-to-Batch`): nhánh 1 là `Apache Flink` tính cảnh báo thời gian thực, nhánh 2 là `Batch Storage Consumer` gom thành tệp Parquet nạp xuống Data Lakehouse, và bất kỳ Consumer nào cũng có thể tua lại (`Replay`) lịch sử từ quá khứ.",
        "PostgreSQL WAL ──[CDC]──> Kafka Topic (Offset #8888) ──> (1) Flink Real-time & (2) Lakehouse Batch",
        "Ghi nối đuôi tuần tự (`Append-only`) giúp Kafka biến thao tác ghi đĩa thành Sequential I/O cực nhanh."
    ),
    (
        "storage.data-warehouse",
        "Kho Dữ liệu Tập trung (Data Warehouse: Snowflake, BigQuery, Redshift) & 3 Hạn chế Lịch sử",
        "DATA WAREHOUSE & OLAP",
        ["D02"],
        [
            "data warehouse", "cloud data warehouses", "edw", "snowflake", "bigquery",
            "google bigquery", "colossus", "amazon redshift", "redshift", "teradata",
            "ibm netezza", "vertica", "micro-partition", "micro-partitioning",
            "query results cache", "bộ nhớ đệm kết quả truy vấn (query results cache - hot data)",
            "zero-copy cloning", "closed storage engine & vendor lock-in", "expensive at scale",
            "3 hạn chế lịch sử", "1. bó tay trước dữ liệu phi cấu trúc (unstructured data)",
            "2. chi phí đắt đỏ ở quy mô lớn (expensive at scale)",
            "3. khó chia sẻ đa động cơ & khóa chặt nhà cung cấp (closed storage engine & vendor lock-in)"
        ],
        "Data Warehouse là 'ngân hàng dữ liệu chuẩn mực' của doanh nghiệp: chỉ nhận dữ liệu có cấu trúc đã được kiểm duyệt lược đồ gắt gao (`Schema-on-Write`), lưu trữ dạng cột nén cao và đảm bảo giao dịch `ACID` tuyệt đối cho báo cáo BI.",
        "Các Cloud Data Warehouse hiện đại (`Snowflake`, `BigQuery`, `Redshift`) tách rời Compute và Storage, tự động chia bảng thành các `Micro-partitions` (`50 MB – 500 MB` chưa nén) kèm bộ nhớ đệm kết quả (`Query Results Cache`). Tuy nhiên, Data Warehouse truyền thống đụng trần ở **3 hạn chế lịch sử**: (1) Bó tay trước dữ liệu phi cấu trúc (`Unstructured Data` như ảnh, âm thanh, video cho AI/ML), (2) Chi phí lưu trữ & tính toán đắt đỏ ở quy mô lớn (`Expensive at Scale`), và (3) Động cơ lưu trữ đóng kín gây khóa chặt nhà cung cấp (`Closed Storage Engine & Vendor Lock-in`).",
        "Source DB ──[ETL + Schema-on-Write]──> Cloud Data Warehouse (Columnar + ACID) ──> BI Dashboards",
        "Ba hạn chế lịch sử này chính là lực đẩy buộc ngành dữ liệu tiến hóa sang Data Lake (Chặng 5) và Data Lakehouse (Chặng 6)."
    ),

    # =========================================================================
    # D02: STORAGE LAYER — CHẶNG 4 (DATA MODELING: INMON, KIMBALL, FACT/DIM, SCD)
    # =========================================================================
    (
        "storage.conceptual-logical-physical",
        "Ba Cấp độ Thiết kế Mô hình Dữ liệu (Conceptual → Logical → Physical) & Kimball 4-Step",
        "DATA MODELING",
        ["D02"],
        [
            "conceptual model", "logical model", "physical model", "conceptual", "logical",
            "physical", "3 cấp độ thiết kế", "3 cấp độ mô hình hóa",
            "3 cấp độ thiết kế từ trừu tượng đến vật lý", "data modeling",
            "mô hình hóa dữ liệu (data modeling)", "mô hình dữ liệu (data model)",
            "kỹ thuật thiết kế mô hình dữ liệu", "(1) chọn quy trình nghiệp vụ (select the business process)",
            "(2) tuyên bố độ mịn (declare the grain)", "(3) xác định các chiều ngữ cảnh (identify the dimensions)",
            "(4) xác định các số đo sự kiện (identify the facts)", "identify the facts"
        ],
        "Giống như xây nhà: `Conceptual Model` là 'bản phác thảo mặt bằng nói chuyện với chủ nhà' (các thực thể nghiệp vụ chính), `Logical Model` là 'bản vẽ kỹ thuật chi tiết từng phòng' (tên bảng, cột, khóa PK/FK), còn `Physical Model` là 'bản thi công bê tông thực tế' trên CSDL cụ thể (kiểu dữ liệu `DECIMAL`, `PARTITION BY`, `CLUSTER BY`).",
        "Khi thiết kế mô hình chiều (Dimensional Modeling), Ralph Kimball đặt ra **Quy trình 4 Bước Bất biến**: (1) Chọn Quy trình Nghiệp vụ (`Select the Business Process`), (2) Tuyên bố Độ mịn (`Declare the Grain`), (3) Xác định các Chiều ngữ cảnh (`Identify the Dimensions`), và (4) Xác định các Số đo sự kiện (`Identify the Facts`).",
        "Conceptual [Khách → Đơn → Hàng] → Logical [Fact_Sales PK/FK] → Physical [PARTITION BY nam_thang]",
        "Không bao giờ được nhảy vào viết câu lệnh `CREATE TABLE` (Physical) khi chưa chốt xong Bước 2: Tuyên bố Độ mịn (`Grain`)."
    ),
    (
        "storage.inmon-kimball-datavault",
        "Ba Trường phái Mô hình hóa: Bill Inmon (Top-down 3NF) vs. Ralph Kimball (Bottom-up Dimensional) vs. Data Vault",
        "DATA MODELING",
        ["D02"],
        [
            "bill inmon", "bill inmon (top-down 3nf)", "inmon", "ralph kimball", "kimball",
            "bottom-up dimensional", "dimensional modeling", "mô hình hóa chiều (dimensional modeling)",
            "data vault", "dan linstedt", "3nf", "3nf / data vault / scd type 2", "3nf/scd2",
            "third normal form", "normalized", "denormalized", "denormalization",
            "phi chuẩn hóa (denormalization)", "hub", "link", "satellite",
            "hash key md5/sha-256", "load date", "record source", "data marts",
            "presentation area", "enterprise view", "4 tính chất (subject-oriented, integrated, nonvolatile, time-variant)",
            "integrated"
        ],
        "Inmon xây 'đại bản doanh chuẩn hóa `3NF` chống trùng lặp cho toàn công ty trước rồi mới tách các `Data Marts` cho từng phòng'; Kimball xây 'từng quầy siêu thị `Star Schema` phi chuẩn hóa (`Denormalized`) phục vụ ngay từng quy trình nghiệp vụ rồi nối lại bằng bộ chiều dùng chung'; còn Data Vault tách `Hub · Link · Satellite` để nạp song song và kiểm toán lịch sử 100%.",
        "Trong **Data Vault** của Dan Linstedt: `Hub` chỉ giữ Khóa nghiệp vụ (`Business Key` + `Hash Key MD5/SHA-256` + `Load Date` + `Record Source`), `Link` biểu diễn mối quan hệ nhiều-nhiều linh hoạt giữa các Hub, còn `Satellite` lưu toàn bộ thuộc tính mô tả và lịch sử thay đổi theo thời gian (`Insert-only`). Trong kiến trúc Medallion hiện đại, kỹ sư thường áp dụng tinh thần **Inmon / 3NF / Data Vault ở tầng Silver** và **Kimball Star Schema ở tầng Gold**.",
        "Silver Layer (Inmon 3NF / Data Vault: Chuẩn hóa, tích hợp) → Gold Layer (Kimball Star Schema: Tối ưu BI)",
        "4 tính chất kinh điển của Kho dữ liệu theo Bill Inmon: `Subject-oriented` (Hướng chủ đề), `Integrated` (Tích hợp), `Nonvolatile` (Bất khả biến), và `Time-variant` (Biến thiên theo thời gian)."
    ),
    (
        "storage.fact-dimension-grain",
        "Bảng Sự kiện (Fact Table) vs. Bảng Thứ nguyên (Dimension Table), Độ mịn (Grain) & Tính Cộng được (Additivity)",
        "DATA MODELING",
        ["D02"],
        [
            "fact table", "fact", "fact_sales", "fact_inventory", "dimension table",
            "dimension", "dimensions", "dim_customer", "dim_date", "dim_product", "dim_store",
            "grain", "1 grain", "độ mịn", "additivity", "additive", "additive fact",
            "semi-additive", "non-additive", "degenerate dimension", "smart key", "yyyymmdd",
            "20261015", "narrow & long", "wide & short", "pk", "fk", "pk/fk",
            "order_id + line_item_id", "so_tien", "thành_tiền", "order_amount", "total_cost"
        ],
        "Bảng **Fact** là 'cuốn sổ ghi các con số đo lường của sự kiện' (`Fact_Sales` — bảng hẹp và cực dài `Narrow & Long`, tăng liên tục), còn Bảng **Dimension** là 'hồ sơ ngữ cảnh Ai, Ở đâu, Cái gì, Khi nào' (`Dim_Customer`, `Dim_Product`, `Dim_Date` — bảng rộng và ngắn `Wide & Short`) dùng để lọc (`WHERE`) và gom nhóm (`GROUP BY`).",
        "Độ mịn (**Grain**) định nghĩa chính xác 1 dòng trong bảng Fact đại diện cho sự kiện nguyên tử nào (ví dụ `order_id + line_item_id`). Về **Additivity** (Tính cộng được): (1) `Additive Fact` (Doanh thu `so_tien`, Số lượng — cộng tổng `SUM()` hợp lệ qua mọi chiều), (2) `Semi-Additive Fact` (Số dư tồn kho trong `Fact_Inventory`, Số dư tài khoản — cộng được theo cửa hàng nhưng **cấm cộng dồn qua chiều thời gian**!), và (3) `Non-Additive Fact` (Đơn giá, Tỷ lệ %). Riêng bảng `Dim_Date` luôn dùng khóa thông minh dạng số nguyên `YYYYMMDD` (ví dụ `20261015`) để vừa làm khóa phân vùng vừa đọc hiểu ngay mà không cần JOIN.",
        "SELECT d.tinh_thanh, SUM(f.so_tien) FROM fact_sales f JOIN dim_customer d ON f.cust_sk = d.cust_sk GROUP BY 1",
        "Mã đơn hàng `#8888` nằm trực tiếp trong bảng `Fact_Sales` để gom nhóm hóa đơn mà không có bảng Dimension đi kèm được gọi là **Degenerate Dimension** (Chiều suy biến)."
    ),
    (
        "storage.star-snowflake-obt",
        "Ba Kiến trúc Bố trí Bảng: Star Schema vs. Snowflake Schema vs. OBT (One Big Table) & OLAP Cubes",
        "DATA MODELING",
        ["D02"],
        [
            "star schema", "snowflake schema", "obt", "one big table", "olap cube",
            "olap cubes", "multidimensional database", "mdx", "xmla", "1-hop",
            "lược đồ hình sao", "lược đồ bông tuyết", "bảng phẳng",
            "chuẩn mực vàng cho bi (power bi / tableau):"
        ],
        "**Star Schema** đặt bảng Fact ở tâm nối trực tiếp 1 bước (`1-hop JOIN`) tới các bảng Dimension phẳng xung quanh; **Snowflake Schema** chuẩn hóa tách bảng Dimension thành nhiều nhánh con (nhiều bước JOIN); còn **OBT (One Big Table)** gộp thẳng mọi cột Dimension vào chung một bảng phẳng duy nhất (`0 JOIN`).",
        "**Star Schema** là chuẩn mực vàng cho các công cụ BI (`Power BI`, `Tableau`, `Looker`) vì mô hình ngữ nghĩa rõ ràng, hỗ trợ `Drill-across` nhiều bảng Fact và chỉ tốn 1 phép JOIN. **OBT** phát huy sức mạnh tối đa trên các động cơ Columnar đám mây (`BigQuery`, `ClickHouse`, `Snowflake`) khi cần quét tốc độ cực cao mà không muốn tốn tài nguyên CPU/Network cho phép JOIN. Còn **OLAP Cubes** (truy vấn bằng `MDX` / `XMLA`) tính sẵn các khối đa chiều trước kia nay đã phần lớn được thay thế bởi Columnar Lakehouse + Star Schema/OBT.",
        "Star Schema (1-hop JOIN, chuẩn mực BI/Semantic Model) vs. OBT (0 JOIN, tốc độ quét Columnar tối đa)",
        "Tránh lạm dụng Snowflake Schema ở tầng phục vụ BI vì nhiều phép JOIN nối tiếp sẽ làm giảm hiệu năng truy vấn và gây rối cho người dùng cuối."
    ),
    (
        "storage.surrogate-scd-bus",
        "Surrogate Key (Khóa đại diện), SCD (Type 1 / 2 / 3) & Enterprise Bus Matrix (Conformed Dimensions)",
        "DATA MODELING",
        ["D02"],
        [
            "surrogate key", "surrogate keys", "natural key", "natural keys", "business key",
            "sk = 101", "sk = 205", "'kh_001'", "nguyễn văn a ('kh_001')", "scd",
            "slowly changing dimensions", "scd type 1", "scd type 2", "scd type 3", "scd2",
            "bus matrix", "conformed dimensions", "drill-across", "business processes",
            "retail sales", "inventory", "procurement", "start_date", "end_date", "9999-12-31",
            "is_current", "effective_date"
        ],
        "**Surrogate Key** là mã số nguyên tự sinh (`SK = 101, 205`) tách biệt hoàn toàn kho dữ liệu khỏi khóa tự nhiên (`Natural Key` như `'KH_001'`); nhờ đó khi khách hàng đổi địa chỉ từ Hà Nội vào Bình Dương, kỹ thuật **SCD Type 2** tạo thêm dòng phiên bản mới (`SK = 205`) để đơn hàng cũ vẫn thuộc về Hà Nội còn đơn hàng mới (`#8888`) tự động gắn vào Bình Dương!",
        "3 chiến lược **Slowly Changing Dimensions (SCD)**: **Type 1** (Ghi đè trực tiếp — mất lịch sử cũ), **Type 2** (Thêm dòng phiên bản mới với `start_date`, `end_date = '9999-12-31'`, `is_current = true` và cấp `Surrogate Key` mới — chuẩn vàng bảo toàn lịch sử 100%), và **Type 3** (Thêm cột giá trị cũ trên cùng dòng). **Enterprise Bus Matrix** quy hoạch các chiều chuẩn hóa dùng chung (**Conformed Dimensions** như `Dim_Date`, `Dim_Customer`, `Dim_Product`) xuyên suốt các quy trình nghiệp vụ (`Retail Sales`, `Inventory`, `Procurement`), cho phép thực hiện truy vấn liên quy trình (**Drill-across**) mà không bao giờ lệch số.",
        "Dim_Customer SCD2: [SK: 101 | KH_001 | HaNoi | end=2026-10-14] → [SK: 205 | KH_001 | BinhDuong | end=9999-12-31]",
        "Bảng `Fact_Sales` chỉ lưu khóa đại diện `cust_sk = 205` tại đúng thời điểm Đơn hàng `#8888` phát sinh, giúp báo cáo doanh thu lịch sử theo vùng miền luôn chính xác vĩnh viễn."
    ),

    # =========================================================================
    # D02: STORAGE LAYER — CHẶNG 5 (DATA LAKE, DATA SWAMP, 3 TOOLING GAPS, CONTRACTS)
    # =========================================================================
    (
        "storage.data-lake-schema-on-read",
        "Data Lake (Hồ Dữ liệu), Schema-on-Read vs. Schema-on-Write & Mô hình ELT",
        "DATA LAKE & GOVERNANCE",
        ["D02"],
        [
            "data lake", "hồ dữ liệu", "james dixon", "schema-on-read", "schema on read",
            "schema-on-write", "schema on write", "elt", "etl", "landing zone",
            "reprocess", "recover or fall back on",
            "luôn có một nơi an toàn để khôi phục hoặc quay lui (recover or fall back on) khi sự cố xảy ra hoặc khi yêu cầu nghiệp vụ thay đổi"
        ],
        "Khái niệm do James Dixon khởi xướng: thay vì bắt dữ liệu phải cắt gọt khuôn mẫu ngay ở cửa (`Schema-on-Write` / `ETL` của Data Warehouse), **Data Lake** cho phép đổ nguyên bản mọi loại dữ liệu thô vào thẳng Cloud Object Storage giá rẻ (`~$0.02/GB/tháng`) rồi khi nào đọc lên phân tích mới áp lược đồ (`Schema-on-Read` / `ELT`).",
        "Giá trị cốt lõi của Data Lake và tầng nguyên bản là đảm bảo kỹ sư luôn có một nơi an toàn để khôi phục hoặc chạy lại từ đầu (`recover or fall back on / reprocess`) khi code biến đổi có lỗi hoặc khi phát sinh bài toán AI/ML mới cần trích xuất thêm trường từ dữ liệu gốc.",
        "ETL (Transform trước khi nạp vào DW) vs. ELT (Load nguyên bản vào S3 Data Lake → Transform sau)",
        "Tuy nhiên, `Schema-on-Read` không có nghĩa là 'bỏ mặc không quản lý': nếu thiếu Catalog và kiểm định ở cửa nạp, gánh nặng xử lý rác sẽ đổ dồn lên vai mọi người đọc phía sau."
    ),
    (
        "storage.data-swamp-hive-gaps",
        "Data Swamp (Đầm lầy Dữ liệu), Hội chứng WORN, Zombie Files & 3 Lỗ hổng Công cụ (Tooling Gaps)",
        "DATA LAKE & GOVERNANCE",
        ["D02"],
        [
            "data swamp", "đầm lầy dữ liệu", "swampification", "data superfund site",
            "dark data", "inscrutable", "worn", "write once read never", "worm",
            "write once read many", "zombie writes", "zombie files", "partial files",
            "apache hive", "hive", "hive table format", "hive metastore", "3 tooling gaps",
            "tooling gaps", "ba lỗ hổng gốc rễ (3 tooling gaps):",
            "3 lỗ hổng công cụ và quản trị cốt lõi (tooling gaps)",
            "6 khiếm khuyết kiến trúc cố hữu của chuẩn bảng apache hive table format",
            "insufficient transactional support", "lack of mutability", "lack of catalog & governance",
            "lack of lineage & observability", "unclear ownership and stewardship",
            "3. thiếu data lineage, giám sát & kiểm soát chất lượng (lack of lineage & observability)",
            "schema drift", "stale analytics", "stale data", "data breaches"
        ],
        "**Data Swamp** là bi kịch khi Data Lake thoái hóa thành 'bãi rác độc hại' (`Data Superfund Site`): hàng nghìn thư mục vô danh (`Inscrutable`), các tệp ghi dở dang do job Spark đứt mạng (`Zombie Files`) nằm lẫn với tệp đúng làm nhân đôi doanh thu, biến giấc mơ `WORM` (Ghi một lần, Đọc nhiều lần) thành `WORN` (Ghi một lần, Chẳng ai dám đọc).",
        "Nguyên nhân gốc rễ nằm ở **6 khiếm khuyết của chuẩn bảng Apache Hive** (quản lý bảng ở cấp độ thư mục, phụ thuộc lệnh `LIST` thư mục đắt đỏ, đổi phân vùng phải viết lại toàn bảng) và **3 Lỗ hổng Công cụ cốt tử (`The 3 Tooling Gaps`)**: (1) `Lack of ACID & Mutability` (không có giao dịch nguyên tử, không thể sửa/xóa lẻ theo GDPR, không chặn được `Schema Drift`), (2) `Lack of Catalog & Governance` (thiếu danh mục siêu dữ liệu và người chịu trách nhiệm `Ownership/Stewardship`, sinh ra `Dark Data`), và (3) `Lack of Lineage & Observability` (không truy vết được nguồn gốc dữ liệu bẩn).",
        "Spark Job đứt mạng để lại '3.parquet' (Zombie File) + Retry sinh '3_v2.parquet' → Hive quét cả thư mục = Nhân đôi số liệu!",
        "Hiểu rõ 3 lỗ hổng này chính là bản lề giải thích tại sao thế giới dữ liệu phải khai sinh ra kiến trúc Data Lakehouse ở Chặng 6."
    ),
    (
        "storage.data-contracts-zoning",
        "Phác đồ Cứu nguy Data Lake: Zoning (Raw/Cleansed/Curated), Data Contracts, Schema Registry & SSoT",
        "DATA LAKE & GOVERNANCE",
        ["D02"],
        [
            "data contract", "data contracts", "6 thành phần bắt buộc của một data contract chuẩn công nghiệp (theo james densmore, fundamentals of data engineering):",
            "owner contacts", "đầu mối chịu trách nhiệm (owner contacts)", "slas / slos",
            "cam kết mức dịch vụ (slas / slos", "schema registry", "compatibility modes",
            "backward compatibility", "forward compatibility", "full compatibility",
            "backward", "backward (tương thích ngược — mặc định khuyên dùng):",
            "forward", "full", "full (tương thích toàn phần hai chiều):", "ssot",
            "single source of truth", "divergent sources of data truth",
            "sự phức tạp do phân kỳ nguồn sự thật (divergent sources of data truth)",
            "two-tier architecture", "ưu tiên định dạng tự mô tả (self-describing formats) & cạm bẫy kiến trúc hai tầng (two-tier architecture):",
            "zoning", "raw", "cleansed", "curated", "object versioning", "data observability",
            "data lineage", "lineage", "lineage tracking", "data catalog", "catalog",
            "metadata management", "quality checks", "gdpr", "right to be forgotten"
        ],
        "Để ngăn Data Lake hóa đầm lầy, kỹ sư thiết lập 4 hàng rào kỷ luật: chia phân khu rõ ràng (`Zoning`: Raw → Cleansed → Curated), ký **Hợp đồng Dữ liệu (`Data Contract`)** kiểm soát qua `Schema Registry`, bật `Object Versioning` và duy trì duy nhất một Nguồn Sự Thật (**Single Source of Truth — SSoT**).",
        "Một **Data Contract** chuẩn công nghiệp (theo James Densmore & Joe Reis) gồm 6 thành phần: (1) `Owner contacts`, (2) `SLAs / SLOs` về độ tươi dữ liệu, (3) Logical Schema & kiểu dữ liệu, (4) `Compatibility Modes` trên Schema Registry (`BACKWARD` — Consumer mới đọc được dữ liệu cũ; `FORWARD` — Consumer cũ đọc được dữ liệu mới; `FULL` — cả hai chiều), (5) `Quality checks` ngữ nghĩa, và (6) Quy tắc bảo mật/quyền được lãng quên (`GDPR Right to be Forgotten`). Đồng thời cần tránh cạm bẫy **Two-Tier Architecture** (nhân bản dữ liệu song song ở cả Data Lake lẫn Data Warehouse gây lệch số `divergent sources of data truth`).",
        "Producer ──[Schema Registry: BACKWARD Compatibility Gate]──> Data Lakehouse (Single Source of Truth)",
        "Chế độ `BACKWARD` là mặc định vàng: cho phép thêm cột tùy chọn mới hoặc xóa cột cũ mà không làm gãy các đường ống đọc hiện hành."
    ),

    # =========================================================================
    # D02: STORAGE LAYER — CHẶNG 6 (LAKEHOUSE, DELTA, ICEBERG, HUDI, ACID, COW/MOR, OPTIMIZATION)
    # =========================================================================
    (
        "storage.lakehouse-open-table-formats",
        "Kiến trúc Data Lakehouse & Bộ ba Open Table Formats (Delta Lake, Apache Iceberg, Apache Hudi, UniForm)",
        "DATA LAKEHOUSE",
        ["D02"],
        [
            "data lakehouse", "lakehouse", "open table format", "open table formats",
            "table format", "pluggable table format", "transactional metadata layer",
            "transactional metadata", "transaction layer", "delta lake", "apache iceberg",
            "apache iceberg (3-layer metadata tree + hidden partitioning)",
            "apache iceberg (3-layer tree)", "3-layer metadata tree", "3-layer tree",
            "iceberg", "apache hudi", "apache hudi (timeline + indexing)",
            "apache hudi (timeline/index)", "hudi", "uniform", "apache xtable", "xtable",
            "omnidirectional interoperation", "'delta.universalformat.enabledformats' = 'iceberg'",
            "_delta_log", "delta log", ".checkpoint.parquet", "_last_checkpoint",
            "000000.json", "000001.json", "commitinfo", "metadata", "protocol",
            "minreaderversion / minwriterversion", "add", "remove", "canonical list of files",
            "danh sách chuẩn tắc các tệp hợp lệ (canonical list of files)",
            "manifest list", "manifest file", "metadata file", "atomic cas swap",
            "compare-and-swap — cas", "catalog (cas)", "nessie", "glue", "timeline",
            "timeline (3 trạng thái) + file groups + indexing (rli/bloom/bucket)",
            "timeline + indexing", "timeline/index", "requested → inflight → completed",
            "completed", "deltacommit", "file group", "file groups", "hybrid file groups",
            "base file", "log files", ".hoodie/", ".hoodie/metadata", "hfile",
            "4 loại index trong bảng metadata nội bộ (.hoodie/metadata dạng hfile):",
            "bloom index", "record-level index", "record-level index (rli)", "bucket index",
            "simple index", "recordkey → filegroupid", "hash(record_key) % n", "cidr 2021",
            "phân biệt file format vs. table format & bước ngoặt khỏi hive:"
        ],
        "Data Lakehouse đặt một **Tầng Siêu dữ liệu Giao dịch (`Transactional Metadata Layer`)** — chính là **Delta Lake**, **Apache Iceberg** hoặc **Apache Hudi** — ngay bên trên các tệp Parquet trên S3 để định nghĩa lại bảng: 'Bảng không còn là một thư mục chứa tệp mù quáng như Hive, mà là danh sách chuẩn tắc các tệp hợp lệ (`canonical list of files`) được ghi trong Sổ cái giao dịch'!",
        "Giải phẫu 'bộ não' của 3 Open Table Formats: (1) **Delta Lake** dùng nhật ký tuần tự `_delta_log/000000.json` (chứa các hành động `protocol`, `metaData`, `commitInfo`, `add`, `remove`) và nén thành `.checkpoint.parquet` sau mỗi N commits (trỏ qua `_last_checkpoint`). (2) **Apache Iceberg** dùng cây phân cấp 3 tầng (`Catalog Atomic CAS Swap → Metadata File → Manifest List → Manifest File`) giúp cô lập hoàn toàn cấu trúc vật lý. (3) **Apache Hudi** quản lý theo `Timeline` (`REQUESTED → INFLIGHT → COMPLETED`), chia dữ liệu thành các `File Groups` (`Base File` Parquet + `Log Files` Avro) và tích hợp bảng `.hoodie/metadata` dạng `HFile` chứa 4 loại chỉ mục (`Record-Level Index`, `Bloom Index`, `Bucket Index`, `Simple Index`) để định vị nhanh `RecordKey → FileGroupId` cho luồng Upsert. Với **Delta UniForm / Apache XTable**, cả 3 định dạng có thể tự động sinh metadata tương thích đa chiều (`omnidirectional interoperation`) trên cùng một bộ tệp Parquet duy nhất.",
        "Catalog (CAS) → Metadata Tree / _delta_log [Chỉ trỏ tới '3_v2.parquet', phớt lờ tệp rác '3.parquet']",
        "Nhờ Sổ cái Metadata, động cơ truy vấn hoàn toàn miễn nhiễm với tệp rác `Zombie Files` và không bao giờ phải gọi lệnh `LIST` thư mục S3 đắt đỏ."
    ),
    (
        "storage.lakehouse-acid-concurrency",
        "Giao dịch ACID, Kiểm soát Đồng thời (MVCC / OCC / NBCC), Time Travel, CDF & Schema Evolution",
        "DATA LAKEHOUSE",
        ["D02"],
        [
            "acid", "acid & mutability", "acid & concurrency (mvcc, occ phát hiện xung đột cấp tệp, nbcc)",
            "acid, time travel, schema enforcement", "atomicity", "consistency", "isolation",
            "durability", "concurrency control", "mvcc", "occ", "optimistic concurrency control",
            "nbcc", "non-blocking concurrency control", "file-level conflict detection",
            "phát hiện xung đột cấp tệp (file-level conflict detection) & mức cô lập:",
            "writeserializable", "concurrentmodificationexception", "writer 1", "writer 2",
            "blind append", "time travel", "version / snapshot", "version as of",
            "timestamp as of", "rollback", "roll back", "change data feed", "cdf",
            "_change_data", "_change_type", "update_preimage = 15m", "update_postimage = 14m",
            "delta.enablechangedatafeed = true", "point-in-time differential snapshots",
            "incremental query", "changelog scan", "schema enforcement", "schema evolution",
            "column id", "field-id", "field-id bất biến", "column mapping mode = 'id'",
            "delta.columnmapping.mode = 'name'", "rename column total_cost to order_amount",
            "total_cost → order_amount", "mergeschema"
        ],
        "Nhờ cơ chế Đa phiên bản (**MVCC** — mỗi giao dịch tạo một Snapshot mới thay vì sửa đè tệp cũ), hàng nghìn người đọc và luồng ghi có thể chạy đồng thời mà không khóa nhau, cho phép **Time Travel** (truy vấn hoặc `RESTORE` bảng về bất kỳ mốc thời gian/phiên bản nào trong quá khứ)!",
        "Khi có nhiều luồng cùng ghi (`Writer 1` & `Writer 2`), các bảng dùng **OCC (`Optimistic Concurrency Control`)** với kiểm tra xung đột cấp độ tệp (`File-Level Conflict Detection` ở mức cô lập `Serializable` hoặc `WriteSerializable`): nếu 2 luồng chạm vào 2 phân vùng/tệp khác nhau hoặc chỉ nối đuôi (`blind append`), cả hai đều thành công; nếu cùng sửa 1 tệp, một luồng sẽ tự động đọc lại metadata và thử lại (`Retry Loop`) hoặc báo `ConcurrentModificationException` (riêng Hudi hỗ trợ thêm **NBCC** không khóa cho luồng streaming). Về lược đồ: **Schema Enforcement** chặn đứng dữ liệu sai kiểu ngay lúc ghi, còn **Schema Evolution** dựa trên mã số định danh cột bất biến (`field-id` / `Column Mapping Mode = 'id'`) cho phép đổi tên cột (`RENAME COLUMN total_cost TO order_amount`) hoàn toàn bằng Metadata mà không cần viết lại tệp Parquet (`0 byte table rewrite`).",
        "SELECT * FROM sales.orders VERSION AS OF 0 WHERE order_id = 8888;\nRESTORE TABLE sales.orders TO VERSION AS OF 0;",
        "Bật `delta.enableChangeDataFeed = true` (hoặc `Incremental Query` trên Hudi/Iceberg) giúp trích xuất trực tiếp các dòng thay đổi kèm `update_preimage` (15M) và `update_postimage` (14M) để truyền xuống tầng Gold."
    ),
    (
        "storage.cow-vs-mor",
        "Chiến lược Ghi & Cập nhật: Copy-on-Write (COW) vs. Merge-on-Read (MOR) & Positional/Equality Deletes",
        "DATA LAKEHOUSE",
        ["D02"],
        [
            "copy-on-write", "copy_on_write", "cow", "merge-on-read", "merge_on_read", "mor",
            "positional delete", "equality delete", "positional / equality deletes",
            "delete file", "delta log file", ".log.avro", "tombstone", "deletiontimestamp",
            "write amplification", "read amplification", "waf", "waf ≈ 1", "cao (waf >> 1):",
            "cực thấp (waf ≈ 1):", "snapshot query (rt)", "read-optimized (ro)",
            "merge / upsert", "upserts"
        ],
        "Vì tệp Parquet trên S3 là bất biến, khi cần sửa 1 đơn hàng (`#8888`) nằm trong tệp Parquet 500 MB, bạn có 2 chiến lược: **COW** ('Chép lại cả tệp Parquet 500 MB mới đã sửa dòng đó' — ghi tốn công `WAF >> 1` nhưng đọc cực nhanh) hoặc **MOR** ('Ghi nhanh dòng sửa vào một tệp phụ nhỏ `WAF ≈ 1`' — ghi tức thì nhưng lúc đọc phải trộn tệp phụ với tệp gốc).",
        "Trong **Merge-on-Read (MOR)**: Apache Iceberg hỗ trợ 2 loại tệp xóa phụ là **Positional Delete** (ghi địa chỉ chính xác `(file_path, pos = 4512)` — lúc đọc rất nhanh) và **Equality Delete** (ghi điều kiện `order_id = 8888` — lúc ghi không cần tìm vị trí nhưng lúc đọc phải so khớp điều kiện). Trên Apache Hudi, bảng MOR ghi các bản cập nhật vào tệp `.log.avro` và cung cấp 2 góc nhìn truy vấn: **Snapshot Query (`RT`)** (trộn Base Parquet + Log Avro để lấy dữ liệu tươi nhất theo thời gian thực) và **Read-Optimized (`RO`)** (chỉ đọc Base Parquet để đạt tốc độ quét Columnar tối đa cho Batch BI).",
        "COW (WAF >> 1, 0% Read overhead → Tối ưu cho bảng Gold) vs. MOR (WAF ≈ 1, Fast Upsert → Tối ưu cho CDC Silver)",
        "Sau khi dùng MOR để hứng luồng CDC tốc độ cao, một dịch vụ nền (`Async Compaction`) sẽ định kỳ gộp các tệp log/delete vào tệp Parquet chính."
    ),
    (
        "storage.lakehouse-optimizations",
        "5 Kỹ thuật Tối ưu Vật lý: Compaction, Hidden Partitioning, Z-Ordering / Liquid Clustering, Deletion Vectors & VACUUM",
        "DATA LAKEHOUSE",
        ["D02"],
        [
            "compaction", "bin-packing", "optimize", "small file problem",
            "43.200 tệp nhỏ li ti (small file problem)", "hidden partitioning",
            "hive partitioning", "hive partitioning truyền thống", "partition evolution",
            "partition spec", "partitioning", "clustering", "year", "month", "day", "hour",
            "bucket[n]", "truncate[l]", "6 hàm biến đổi chuẩn", "z-order", "z-ordering",
            "liquid clustering", "hilbert curve", "space-filling curve", "not incremental",
            "không có tính tăng trưởng (not incremental)", "deletion vectors", "roaring bitmap",
            "reorg table ... apply (purge)", "(2) reorg table ... apply (purge) / optimize",
            "vacuum", "(3) vacuum", "expire_snapshots", "table services", "168 giờ",
            "năm kỹ thuật bảo trì vật lý:"
        ],
        "Bộ 5 kỹ thuật bảo trì vật lý (`Table Services`) giúp bảng Lakehouse hàng trăm TB không bị suy giảm hiệu năng theo thời gian: gộp tệp nhỏ (**Compaction**), phân vùng ẩn (**Hidden Partitioning**), gom cụm đa chiều (**Z-Ordering / Liquid Clustering**), mặt nạ bit xóa nhanh (**Deletion Vectors**) và thu gom rác (**VACUUM**).",
        "(1) **Compaction (`OPTIMIZE` / Bin-packing)**: gộp hàng chục nghìn tệp nhỏ (`43.200 tệp nhỏ` do streaming sinh ra mỗi 10 giây) thành các tệp Parquet 128MB–1GB. (2) **Hidden Partitioning & Partition Evolution** (Iceberg): dùng 6 hàm biến đổi chuẩn (`year`, `month`, `day`, `hour`, `bucket[N]`, `truncate[L]`) lưu trong `Partition Spec` giúp người dùng lọc thẳng trên cột gốc mà không sợ quên cột phân vùng như Hive truyền thống, đồng thời đổi chiến lược phân vùng không cần viết lại dữ liệu cũ. (3) **Z-Ordering & Liquid Clustering**: khắc phục điểm yếu `not incremental` của Z-Order cũ bằng đường cong không gian **Hilbert Curve** (`CLUSTER BY`), gom cụm dữ liệu đa chiều tăng trưởng tự động. (4) **Deletion Vectors**: dùng `Roaring Bitmap` đánh dấu dòng xóa tức thì, sau đó dọn vật lý bằng `REORG TABLE ... APPLY (PURGE)` hoặc `OPTIMIZE`. (5) **VACUUM / `expire_snapshots`**: xóa vật lý các tệp Parquet mồ côi đã quá thời hạn lưu giữ (mặc định `168 giờ` = 7 ngày) để giải phóng dung lượng S3.",
        "OPTIMIZE sales.orders ZORDER BY (customer_id, product_id);\nVACUUM sales.orders RETAIN 168 HOURS;",
        "Cảnh báo: Không bao giờ chạy `VACUUM ... RETAIN 0 HOURS` khi đang có luồng đọc/ghi chạy song song vì sẽ xóa mất tệp Parquet của Snapshot đang mở!"
    ),

    # =========================================================================
    # D02: STORAGE LAYER — CHẶNG 7 (MEDALLION, QUALITY GATING, GOVERNANCE, FINOPS)
    # =========================================================================
    (
        "storage.medallion-architecture",
        "Kiến trúc Multi-Hop Medallion (Bronze → Silver → Gold) & Trạm Kiểm dịch (Quality Gating / WAP)",
        "MEDALLION & GOVERNANCE",
        ["D02"],
        [
            "medallion", "medallion architecture", "multi-hop", "three-tiered framework",
            "bronze", "silver", "gold", "bronze / silver", "bronze → silver → gold",
            "bronze layer", "silver layer", "gold layer", "infancy", "teenage", "maturity",
            "hành trình trưởng thành của một con người", "quality gating", "quarantine",
            "permissive", "permissive mode", "dropmalformed", "_corrupt", "_debug",
            "_corrupt / _debug", "_corrupt is not null", "_rescued_data", "_ingested_at",
            "_source_topic", "cột _corrupt (hoặc _debug / _rescued_data) nằm ở tầng nào và vận hành ra sao?",
            "minimal transformations", "dedup", "late-arriving data", "aggregated kpis",
            "expectations & constraints", "check constraints", "dlt expect",
            "write-audit-publish", "wap", "streaming medallion",
            "hudi_sales_transactions_bronze", "hudi_web_clickstreams_bronze"
        ],
        "Kiến trúc **Medallion (`Multi-Hop`)** ví như hành trình trưởng thành qua 3 giai đoạn: **Bronze (`Infancy`)** giữ nguyên bản 100% dữ liệu thô vừa sinh ra, **Silver (`Teenage`)** lọc sạch rác, khử trùng lặp (`Dedup`) và chuẩn hóa 3NF/SCD2, còn **Gold (`Maturity`)** tổng hợp thành các bảng `Star Schema / OBT / Aggregated KPIs` chín muồi phục vụ Ban giám đốc và AI.",
        "Cơ chế kỹ thuật sống còn: ở tầng **Bronze**, trình đọc luôn cấu hình chế độ **`PERMISSIVE`** (tuyệt đối không dùng `DROPMALFORMED` làm mất dấu dữ liệu lỗi) để hứng mọi bản ghi sai định dạng vào cột `_corrupt` / `_debug` / `_rescued_data` kèm siêu dữ liệu kiểm toán (`_ingested_at`, `_source_topic`). Khi chuyển sang **Silver**, hệ thống áp dụng **Quality Gating** (`CHECK CONSTRAINTS`, `DLT EXPECT` hoặc mẫu **Write-Audit-Publish — WAP** trên nhánh ẩn của Iceberg) để tự động rẽ nhánh các bản ghi vi phạm (`_corrupt IS NOT NULL` hoặc `so_tien <= 0`) vào bảng cách ly (`Quarantine`) chờ kỹ sư xử lý, đảm bảo 100% dữ liệu bước vào Silver và Gold là dữ liệu sạch.",
        "Bronze (PERMISSIVE + _rescued_data) ──[Quality Gate / WAP]──> Silver (3NF/SCD2 + Quarantine) → Gold (Star/OBT)",
        "Tầng Bronze chỉ thực hiện biến đổi tối thiểu (`minimal transformations` — đóng gói sang Parquet/Delta/Iceberg/Hudi và gắn cột audit) để bảo toàn nguyên trạng bằng chứng gốc."
    ),
    (
        "storage.governance-undercurrents",
        "Dòng chảy Ngầm Quản trị (Undercurrents): Unity Catalog, OpenLineage, RLS / Column Masking & Cloud FinOps",
        "MEDALLION & GOVERNANCE",
        ["D02"],
        [
            "undercurrents", "unity catalog", "catalog.schema.table", "data governance",
            "openlineage", "dataset → job → run", "column-level lineage", "rbac / abac",
            "sql dcl (grant / revoke)", "revoked permissions", "row-level security", "rls",
            "row filter", "bộ lọc dòng (row filter)", "column masking", "column mask",
            "mặt nạ cột (column mask)", "row/column security", "dynamic masking",
            "least privilege", "nguyên tắc đặc quyền tối thiểu (least privilege)", "pii",
            "finops", "cloud finops", "tco", "ephemeral compute", "ephemeral clusters",
            "3. điều phối cụm tính toán tạm thời (ephemeral compute)", "idle compute",
            "auto-stop / scale-to-zero", "bottom-up blueprint",
            "bản đồ kiến trúc 6 tầng (bottom-up blueprint)",
            "creation → storage → usage → sharing → archiving → destruction",
            "cách làm sai lầm (nhân bản phân vùng ra 40 nơi khác nhau):",
            "duy nhất 1 bảng nền tảng chuẩn xác", "auxiliary data & layout"
        ],
        "Một kiến trúc dữ liệu chỉ thực sự vững chắc khi có 4 dòng chảy ngầm (**Undercurrents**) chạy xuyên suốt toàn bộ vòng đời dữ liệu (`Creation → Storage → Usage → Sharing → Archiving → Destruction`): Danh mục tập trung (**Unity Catalog**), Phả hệ dữ liệu (**OpenLineage**), Bảo mật hạt mịn (**RLS & Column Masking**) và Tối ưu chi phí (**Cloud FinOps**).",
        "Thay vì nhân bản bảng gốc ra 40 Bucket khác nhau cho 40 phòng ban để phân quyền (gây bùng nổ chi phí và lệch số), doanh nghiệp giữ **duy nhất 1 bảng chuẩn (`Single Source of Truth`)** trong không gian tên 3 cấp (`catalog.schema.table`) và áp nguyên tắc đặc quyền tối thiểu (**Least Privilege** `RBAC / ABAC`): gắn **Row Filter (`RLS`)** để quản lý vùng nào chỉ nhìn thấy dòng dữ liệu vùng đó, và gắn **Column Mask** để tự động che dấu thông tin cá nhân nhạy cảm (`PII`). Đồng thời, chuẩn mở **OpenLineage** thu thập sự kiện theo mô hình `Dataset → Job → Run` để vẽ phả hệ cấp độ cột; còn **FinOps** kết hợp `Ephemeral Clusters` / `Scale-to-Zero` (tránh trả tiền cho `Idle Compute`), `Auxiliary Data & Layout` (Compaction/Z-Order giảm I/O) và `Lifecycle Tiering` để tối ưu tổng chi phí sở hữu (`TCO`).",
        "GRANT SELECT ON TABLE prod_catalog.gold.fact_sales TO `analyst_group`;\nALTER TABLE prod_catalog.gold.fact_sales SET ROW FILTER region_filter ON (province);",
        "Bản đồ Kiến trúc 6 Tầng (`Bottom-Up Blueprint`) khép lại toàn bộ học phần D02: Phần cứng Vật lý → Mô hình Lưu trữ & Tệp → Hạ tầng Phân tán & Streaming → Open Table Formats → Medallion Architecture → Governance & FinOps."
    ),

    # =========================================================================
    # TRACK 01–04 SYLLABUS FRAMEWORKS & CORE ENGINEERING CONCEPTS
    # =========================================================================
    (
        "syllabus.python-oop-typing",
        "Python Engineering (Typing, Pydantic, Ruff, Pytest, Virtualenv / Poetry / uv)",
        "SOFTWARE ENGINEERING",
        ["F02", "F05"],
        [
            "python", "python3", "type hints", "typing", "pydantic", "ruff", "flake8",
            "black", "pytest", "unittest", "venv", "virtualenv", "conda", "poetry", "uv",
            "pip", "pep8", "gil", "garbage collection", "oop", "git"
        ],
        "Bộ tiêu chuẩn biến code Python từ những đoạn script thử nghiệm rời rạc thành phần mềm cấp độ Production: có kiểm tra kiểu dữ liệu tĩnh (`Type Hints` / `Pydantic`), định dạng chuẩn (`Ruff`), cô lập môi trường (`venv/Poetry/uv`) và kiểm thử tự động (`Pytest`).",
        "Trong kỹ thuật dữ liệu & AI, `Pydantic` đảm bảo kiểm định Schema dữ liệu đầu vào/đầu ra ở biên hệ thống, trong khi `Pytest` kết hợp Git CI/CD ngăn chặn lỗi hồi quy trước khi code được phép merge.",
        "pytest -q --cov=src && ruff check .",
        "Luôn cô lập thư viện của từng dự án trong môi trường ảo (`Virtual Environment`) để tránh xung đột phiên bản gói."
    ),
    (
        "syllabus.relational-db-indexing",
        "Cơ sở dữ liệu Quan hệ (PostgreSQL, MVCC, WAL, B-Tree Index, Query Planner & Isolation Levels)",
        "DATABASE INTERNALS",
        ["F03", "D02"],
        [
            "postgresql", "postgres", "mysql", "sqlite", "wal", "write-ahead log",
            "query planner", "explain analyze", "isolation levels", "read committed",
            "repeatable read", "serializable", "deadlock", "connection pooling", "pgbouncer",
            "sqlalchemy", "alembic", "index", "indexing", "journaling"
        ],
        "Trái tim của các hệ thống giao dịch OLTP: đảm bảo mọi thao tác ghi đều an toàn tuyệt đối ngay cả khi rút phích điện (nhờ sổ nhật ký ghi trước — `WAL`) và tìm kiếm 1 dòng trong hàng trăm triệu dòng dưới 1 ms (nhờ cây chỉ mục `B-Tree Index`).",
        "Trước khi sửa trang dữ liệu (`Heap Page 8KB`), PostgreSQL bắt buộc ghi sự kiện xuống đĩa tuần tự vào tệp `WAL (Write-Ahead Log)`. Cơ chế `MVCC` lưu nhiều phiên bản dòng giúp lệnh đọc không bao giờ chặn lệnh ghi.",
        "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE order_id = 8888;",
        "Dùng `EXPLAIN (ANALYZE, BUFFERS)` để kiểm tra xem câu lệnh SQL đang dùng `Index Scan` hay bị quét toàn bảng (`Seq Scan`)."
    ),
    (
        "syllabus.web-api-networking",
        "Web API & Networking (TCP/IP, DNS, HTTP/REST, gRPC, FastAPI, AuthN/AuthZ, Rate Limiting)",
        "NETWORKING & API",
        ["F04", "P05"],
        [
            "tcp/ip", "tcp", "udp", "dns", "http", "https", "tls", "rest", "restful",
            "grpc", "graphql", "websocket", "sse", "fastapi", "uvicorn", "gunicorn",
            "nginx", "jwt", "oauth2", "rate limit", "circuit breaker", "idempotency"
        ],
        "Hệ thống giao thông kết nối các dịch vụ phần mềm: `DNS` dịch tên miền ra địa chỉ IP, `TCP` bắt tay 3 bước đảm bảo gói tin không rơi rớt, còn `REST / gRPC / FastAPI` định nghĩa quy ước gọi hàm và truyền dữ liệu qua mạng.",
        "Trong hệ thống phân tán, mọi API cấp Production phải đảm bảo tính `Idempotent` (gọi lặp lại cùng một `Idempotency-Key` khi mạng chập chờn không làm trừ tiền 2 lần), kết hợp `Rate Limiting`, `Timeout` và `Circuit Breaker` để chống sập dây chuyền.",
        "curl -i -X POST https://api.example.com/v1/orders -H 'Idempotency-Key: ord-8888'",
        "gRPC (dựa trên HTTP/2 và Protocol Buffers nhị phân) thường được chọn cho giao tiếp nội bộ tốc độ cao giữa các Microservices và ML Serving."
    ),
    (
        "syllabus.docker-containers",
        "Containerization & Docker (Linux Namespaces, Cgroups, OverlayFS, Dockerfile, Docker Compose)",
        "CLOUD-NATIVE & INFRA",
        ["F06", "P02"],
        [
            "docker", "container", "containers", "containerization", "dockerfile",
            "docker compose", "docker-compose", "namespaces", "cgroups", "control groups",
            "overlayfs", "unionfs", "containerd", "oci", "multi-stage build", "portability"
        ],
        "Container không phải là một máy ảo nặng nề có hệ điều hành riêng, mà là một Process Linux bình thường được Kernel quây kín bằng 'tường kính cách âm' (`Namespaces` — cô lập tầm nhìn PID/Network/Mount) và 'đồng hồ giới hạn điện nước' (`Cgroups` — giới hạn trần RAM/CPU).",
        "Nhờ dùng chung trực tiếp Linux Kernel của máy chủ vật lý và xếp chồng các lớp tệp bất biến (`OverlayFS` / Image Layers), Container khởi động trong vài trăm mili-giây và đảm bảo tính khả chuyển (`Portability`) 100% từ Laptop lên Cloud.",
        "docker build -t fsds-app:1.0 . && docker run --rm -m 512m --cpus=1.0 fsds-app:1.0",
        "Kỹ thuật Multi-stage Build trong Dockerfile giúp tách riêng tầng biên dịch (GCC/SDK nặng) và tầng chạy thực tế (Slim/Distroless nhẹ)."
    ),
    (
        "syllabus.spark-batch-stream",
        "Apache Spark & Distributed Compute (Driver, Executor, DAG, Shuffle, Catalyst, Velox/Photon, dbt)",
        "DISTRIBUTED COMPUTE",
        ["D03", "D04", "D02"],
        [
            "apache spark", "spark", "pyspark", "spark sql", "structured streaming",
            "driver", "executor", "dag", "shuffle", "narrow transformation",
            "wide transformation", "catalyst", "catalyst optimizer", "tungsten", "photon",
            "velox", "aqe", "adaptive query execution", "data skew", "broadcast join", "dbt"
        ],
        "Apache Spark là 'nhà máy chế biến dữ liệu phân tán': bộ não `Driver` lập bản đồ công việc (`DAG`), chia dữ liệu thành hàng nghìn phần nhỏ (`Partitions`) và giao cho đàn thợ `Executor` trên nhiều máy chủ cùng xử lý song song trên RAM.",
        "Các phép biến đổi hẹp (`Narrow Transformation` như `SELECT`, `FILTER`) chạy cực nhanh tại chỗ trên từng máy mà không tốn mạng. Ngược lại, các phép biến đổi rộng (`Wide Transformation` như `GROUP BY`, `JOIN`, `ORDER BY`) buộc các máy chủ phải trao đổi dữ liệu chéo qua mạng (`Shuffle`) — điểm nghẽn này được tối ưu bằng `Broadcast Join`, `AQE` và động cơ vector hóa C++ (`Photon / Velox`).",
        "df.filter(col('order_id') == 8888).join(broadcast(dim_store), 'store_id')",
        "Trong khi Spark mạnh về xử lý phân tán quy mô lớn, `dbt (Data Build Tool)` giúp chuẩn hóa các phép biến đổi SQL trong Lakehouse/Warehouse theo quy trình kỹ thuật phần mềm."
    ),
    (
        "syllabus.orchestration-airflow",
        "Điều phối Đường ống Dữ liệu (Apache Airflow, DAG, Idempotency, Retry & Backfill)",
        "ORCHESTRATION & OPS",
        ["D06", "F05"],
        [
            "apache airflow", "airflow", "directed acyclic graph", "scheduler", "worker",
            "operator", "sensor", "xcom", "backfill", "idempotent", "retry", "retry loop",
            "prefect", "dagster", "great expectations", "soda"
        ],
        "Nếu Cronjob chỉ biết gọi 1 script đơn lẻ theo giờ một cách mù quáng, thì **Apache Airflow** là 'trung tâm chỉ huy không lưu' quản lý hàng trăm tác vụ phụ thuộc nhau theo đồ thị không chu trình (`DAG`): bước B chỉ chạy khi bước A thành công, tự động thử lại (`Retry`) khi lỗi mạng và hỗ trợ chạy bù lịch sử (`Backfill`).",
        "Nguyên tắc thiết kế sống còn của mọi Task trong Airflow là tính **Idempotent (Lũy đẳng)**: dù bạn chạy lại Task của ngày `2026-10-15` một lần hay mười lần (do Retry hoặc Backfill), kết quả cuối cùng trong bảng đích vẫn phải giống hệt nhau, tuyệt đối không nhân bản dòng.",
        "extract_orders >> validate_schema >> merge_to_silver >> build_gold_mart",
        "Không bao giờ truyền bảng dữ liệu lớn qua `XCom` của Airflow; XCom chỉ dùng để truyền siêu dữ liệu nhỏ (như đường dẫn S3 hoặc mã phiên bản Snapshot)."
    ),
    (
        "syllabus.olap-serving-engines",
        "Động cơ Phục vụ & Truy vấn Tốc độ cao (ClickHouse, DuckDB, Apache Pinot, Druid, Trino, Vector DB)",
        "CONSUMPTION & SERVING",
        ["D05", "A03"],
        [
            "clickhouse", "duckdb", "apache pinot", "pinot", "apache druid", "druid",
            "trino", "presto", "starrocks", "vector database", "vector db", "milvus",
            "qdrant", "pgvector", "hnsw", "ivf", "embedding", "semantic caching"
        ],
        "Tầng tiêu thụ cuối cùng (`Consumption Layer`) biến dữ liệu từ bảng Gold thành phản hồi dưới 100 ms cho Dashboard thời gian thực (`ClickHouse / Pinot / Druid`), phân tích nhúng ngay trong tiến trình (`DuckDB`) hoặc tìm kiếm ngữ nghĩa bằng vector cho AI/RAG (`Vector DB`).",
        "`ClickHouse`, `Apache Druid` và `Apache Pinot` sử dụng kiến trúc Columnar + Vectorized Execution kết hợp chỉ mục thưa (`Sparse Index`) để trả lời truy vấn tổng hợp trên hàng tỷ dòng trong vài chục mili-giây; trong khi `Trino` là động cơ truy vấn liên hợp (`Federated Query Engine`) đọc trực tiếp Iceberg/Delta Lake.",
        "duckdb -c \"SELECT province, SUM(amount) FROM 'orders.parquet' GROUP BY 1\"",
        "`DuckDB` là động cơ OLAP In-process (chạy ngay trong tiến trình Python/CLI không cần cài server), cực kỳ lý tưởng cho các khối lượng dữ liệu dưới vài trăm GB."
    ),
    (
        "syllabus.ai-mlops-llm",
        "MLOps & AI Engineering (PyTorch, Feature Store, MLflow, DVC, RAG, vLLM, Quantization, Guardrails)",
        "AI & ML ENGINEERING",
        ["A01", "A02", "A03", "A04", "P07"],
        [
            "ai", "unstructured data & ai/ml", "pytorch, tensorflow", "pytorch", "tensorflow",
            "mlops", "feature store", "feast", "data leakage", "training-serving skew",
            "concept drift", "data drift", "mlflow", "dvc", "weights & biases", "ray",
            "ddp", "fsdp", "deepspeed", "vllm", "tensorrt-llm", "triton", "kserve",
            "quantization", "kv cache", "pagedattention", "lora", "qlora", "rag",
            "hybrid search", "reranking", "langfuse", "guardrails"
        ],
        "Hệ thống kỹ thuật đưa mô hình Machine Learning và LLM từ phòng thí nghiệm ra vận hành thực tế: quản lý phiên bản dữ liệu/mô hình (`DVC / MLflow`), đồng bộ đặc trưng chống rò rỉ dữ liệu (`Feature Store`), tối ưu tốc độ suy luận GPU (`vLLM / PagedAttention / Quantization`) và giám sát ảo giác/trôi dạt mô hình (`Drift & Evaluation`).",
        "Hai căn bệnh phổ biến nhất làm mô hình ML thất bại trên Production là `Data Leakage` (vô tình dùng thông tin của tương lai lúc huấn luyện) và `Training-Serving Skew` (cách tính biến đặc trưng lúc chạy thật khác với lúc huấn luyện). Nhờ kiến trúc Data Lakehouse mở, các framework như `PyTorch / Ray / Feature Store` có thể đọc trực tiếp các tệp Parquet/Arrow ở tầng Silver/Gold mà không cần xuất file trung gian.",
        "mlflow.log_metrics({'roc_auc': 0.94, 'p99_latency_ms': 42})",
        "Trong kiến trúc RAG (Retrieval-Augmented Generation), kết hợp tìm kiếm từ khóa (BM25) + tìm kiếm ngữ nghĩa (Vector Search) + Reranker luôn cho độ chính xác vượt trội."
    ),
    (
        "syllabus.distributed-k8s-iac-sre",
        "Hạ tầng Phân tán, Kubernetes, IaC (Terraform/Ansible) & Quan sát Hệ thống (Prometheus, Grafana, OpenTelemetry, SRE)",
        "DISTRIBUTED PLATFORM & SRE",
        ["P01", "P02", "P03", "P04", "P06", "P08", "P09"],
        [
            "cap", "cap theorem", "pacelc", "base", "eventual consistency", "strong consistency",
            "raft", "paxos", "sharding", "consistent hashing", "kubernetes", "k8s", "pod",
            "deployment", "service", "ingress", "pvc", "sidecar", "operator", "helm",
            "terraform", "ansible", "iac", "infrastructure as code", "drift detection",
            "prometheus", "grafana", "opentelemetry", "jaeger", "elk", "sli", "slo", "sla",
            "error budget", "sre", "observability", "cloud", "serverless", "easy / serverless"
        ],
        "Bộ khung xương sống vận hành các nền tảng Cloud-Native quy mô lớn: **Kubernetes** tự động điều phối và phục hồi hàng nghìn Container, **Terraform/Ansible** khai báo hạ tầng bằng code (`IaC`), còn bộ ba `Logs · Metrics · Traces` (**OpenTelemetry / Prometheus / Grafana**) giúp kỹ sư nhìn xuyên thấu sức khỏe hệ thống.",
        "Định lý **CAP & PACELC** chỉ ra sự đánh đổi tất yếu giữa Tính nhất quán tức thời (`Strong Consistency`) và Tính sẵn sàng/Độ trễ (`Availability / Latency` — `Eventual Consistency`). Kỹ thuật **SRE** quản lý độ tin cậy bằng con số định lượng qua `SLI` (chỉ số đo), `SLO` (mục tiêu nội bộ), `SLA` (cam kết hợp đồng) và `Error Budget` (ngân sách lỗi cho phép).",
        "terraform plan -out=tfplan && kubectl rollout status deployment/data-api -n prod",
        "Mọi thay đổi hạ tầng trên Production đều phải đi qua Git + Terraform/Ansible (`Infrastructure as Code`) để chống trôi dạt cấu hình (`Configuration Drift`)."
    ),

    # =========================================================================
    # F03: DATABASE FUNDAMENTALS & POSTGRESQL INTERNALS (CHẶNG 1 -> CHẶNG 4)
    # =========================================================================
    (
        "db.rdbms-architecture",
        "RDBMS Architecture & Shared Access (DB Client Library -> RDBMS Server -> Database Files)",
        "DATABASE FUNDAMENTALS",
        ["F03"],
        [
            "database", "rdbms", "rdbms server", "db client library", "database files",
            "shared access", "unnormalized text", "relational tuples", "e.f. codd",
            "e.f. codd (1970)", "ddl", "dml", "dql", "dcl", "tcl", "ddl / dml / dql / dcl / tcl",
            "ddl/dml/dql/dcl/tcl", "sqlalchemy orm", "orm", "#hd01", "lan", "oolong sua",
            "hong tra tac", "2026-09-26"
        ],
        "Hệ quản trị cơ sở dữ liệu quan hệ (`RDBMS`) đứng chắn giữa ứng dụng (`DB Client Library`) và các tệp dữ liệu trên đĩa (`Database Files`), cho phép hàng nghìn người dùng truy cập đồng thời (`Shared Access`) vào Đơn hàng Trà sữa `#HD01` mà không giẫm đạp làm hỏng tệp.",
        "Thay vì để ứng dụng đọc/ghi trực tiếp vào file văn bản thô (`Unnormalized Text`) gây xung đột khóa và không thể tính tổng tiền, `RDBMS Server` (như PostgreSQL) quản lý tập trung cấu trúc bảng theo mô hình tập hợp của E.F. Codd (1970) qua 5 nhóm lệnh SQL chuẩn: `DDL` (định nghĩa bảng), `DML` (thêm/sửa/xóa), `DQL` (truy vấn `SELECT`), `DCL` (phân quyền) và `TCL` (quản lý giao dịch `BEGIN/COMMIT/ROLLBACK`).",
        "SELECT ma_hd, ten_kh, tong_tien FROM hoa_don WHERE ma_hd = 'HD01';",
        "Nhân vật chính xuyên suốt F03 là Đơn hàng Trà sữa `#HD01` của khách hàng `Lan` (ngày `2026-09-26`: `Oolong Sua` 30,000 x2 và `Hong Tra Tac` 25,000 x1) tiến hóa qua 4 hình thái vật lý."
    ),
    (
        "db.keys-constraints",
        "Relational Keys (PK, FK), Cardinality (1:1, 1:N, M:N) & Constraints (NOT NULL, DEFAULT, UNIQUE, CHECK)",
        "DATA MODELING & INTEGRITY",
        ["F03", "D02"],
        [
            "primary key", "foreign key", "pk", "fk", "cardinality", "1:1", "1:n", "m:n",
            "constraints", "not null", "default", "unique", "check", "referential integrity",
            "ràng buộc tham chiếu", "table", "row", "column", "tuple"
        ],
        "Bộ khung khóa và chốt chặn bảo vệ dữ liệu ngay tại cửa ngõ: `Primary Key (PK)` định danh duy nhất từng dòng, `Foreign Key (FK)` nối các bảng theo quan hệ `1:1 / 1:N / M:N`, còn 4 chốt `NOT NULL, DEFAULT, UNIQUE, CHECK` chặn đứng dữ liệu rác trước khi chạm đĩa.",
        "Ràng buộc toàn vẹn tham chiếu (`Referential Integrity`) của `Foreign Key` đảm bảo chi tiết đơn hàng `#HD01` không thể trỏ tới một mã khách hàng hoặc mã món ăn không tồn tại. Tuy nhiên ở quy mô ghi cực lớn, mỗi lần `INSERT/UPDATE/DELETE` đều kích hoạt kiểm tra khóa ngoại liên bảng, đòi hỏi đánh chỉ mục (`Index`) trên cột `FK` để tránh khóa bảng.",
        "CREATE TABLE chi_tiet_hd (ma_hd VARCHAR(10) REFERENCES hoa_don(ma_hd), so_luong INT CHECK (so_luong > 0));",
        "Luôn đặt chốt `CHECK (don_gia >= 0 AND so_luong > 0)` ngay dưới tầng RDBMS để dù code ứng dụng có bug cũng không thể ghi số tiền âm xuống đĩa."
    ),
    (
        "db.normalization",
        "Chuẩn hóa Dữ liệu (Normalization: UNF -> 1NF -> 2NF -> 3NF -> BCNF) vs. Denormalization",
        "DATA MODELING & INTEGRITY",
        ["F03", "D02"],
        [
            "normalization", "denormalization", "unf", "1nf", "2nf", "3nf", "bcnf",
            "boyce-codd normal form", "insertion anomaly", "update anomaly", "deletion anomaly",
            "insertion/update/deletion anomalies", "dị thường dữ liệu", "khachhang", "hoadon",
            "monan", "chitiet"
        ],
        "Quá trình 'phẫu thuật tách bảng' từ một ô văn bản gộp lộn xộn (`UNF`) qua `1NF -> 2NF -> 3NF -> BCNF` để triệt tiêu hoàn toàn dữ liệu trùng lặp và 3 căn bệnh dị thường khi Thêm, Sửa, Xóa (`Insertion / Update / Deletion Anomalies`).",
        "Với Đơn hàng `#HD01`: `1NF` ép mỗi ô chỉ chứa giá trị nguyên tử (tách danh sách món trà sữa thành từng dòng); `2NF` loại bỏ phụ thuộc hàm bộ phận vào khóa chính ghép; `3NF` & `BCNF` loại bỏ phụ thuộc bắc cầu (tách thành 4 bảng sạch: `KhachHang`, `HoaDon`, `MonAn`, `ChiTiet`). Khi cần ưu tiên tốc độ đọc báo cáo hơn tốc độ ghi, kỹ sư mới chủ động phi chuẩn hóa có kiểm soát (`Denormalization`).",
        "-- 3NF: Tách bảng KhachHang, HoaDon, MonAn, ChiTiet liên kết qua PK/FK",
        "Nhờ tách bảng `MonAn` riêng ở chuẩn `3NF`, khi đổi giá `Oolong Sua` từ `30,000` lên `32,000`, ta chỉ sửa đúng 1 dòng thay vì phải quét sửa hàng triệu hóa đơn cũ."
    ),
    (
        "db.postgres-memory-process",
        "PostgreSQL Process & Memory Architecture (Client/Backend Process, shared_buffers, work_mem, postgresql.conf)",
        "STORAGE ENGINE & MEMORY",
        ["F03"],
        [
            "client process", "backend process", "shared memory", "shared buffers",
            "shared_buffers", "shared_buffers = 131584", "work_mem", "work_mem = 5120 kb",
            "deadlock_timeout", "deadlock_timeout = 1000 ms", "postgresql.conf",
            "postgresql.auto.conf", "postmaster"
        ],
        "Khi ứng dụng kết nối vào PostgreSQL, tiến trình chủ sẽ cấp một `Backend Process` riêng phục vụ kết nối đó, cùng đọc/ghi trên vùng đệm RAM dùng chung `Shared Buffers` (nơi giữ các trang dữ liệu `8KB` nóng nhất).",
        "Trong tệp cấu hình `postgresql.conf` (và `postgresql.auto.conf`), đơn vị cơ sở của bộ nhớ trang là `8kB`: ví dụ `shared_buffers = 131584` tương đương `131,584 × 8KB ≈ 1 GB RAM` dùng chung toàn cụm; `work_mem = 5120 kB` (`5 MB`) cấp phát riêng cho từng phép `ORDER BY / Hash JOIN` trước khi tràn xuống đĩa; và `deadlock_timeout = 1000 ms` (`1 giây`) là thời gian chờ trước khi quét phát hiện khóa chết.",
        "SHOW shared_buffers; SHOW work_mem; SHOW deadlock_timeout;",
        "Hiểu đúng đơn vị cơ sở trong `postgresql.conf` (số trang `8kB` đối với `shared_buffers` vs. `kB` đối với `work_mem`) giúp kỹ sư tránh cấu hình sai gây OOM."
    ),
    (
        "db.slotted-page",
        "On-Disk Layout & 8KB Slotted Page (Page Header, LSN, Line Pointers, Free Space, Tuple) & 3 Engine Variables",
        "STORAGE ENGINE & MEMORY",
        ["F03"],
        [
            "slotted page", "8kb slotted page", "8kb block", "8kb", "8kb pages", "page header",
            "line pointers", "line pointer", "ptr", "free space", "row data", "tuple",
            "in-memory dbms", "buffering", "immutability", "ordering"
        ],
        "Đơn vị vật lý nhỏ nhất mà PostgreSQL đọc/ghi giữa đĩa và RAM không phải là từng dòng lẻ, mà là một khung trang `Slotted Page` kích thước cố định `8KB (8,192 bytes)`.",
        "Bên trong khung `8KB Slotted Page`: phần đầu là `Page Header` (chứa mã `LSN` của lần sửa cuối), tiếp theo là mảng con trỏ `Line Pointers (Ptr)` mọc từ trên xuống, ở giữa là khoảng trống `Free Space`, còn dữ liệu thực sự của dòng `#HD01` (`Tuple / Row Data`) được xếp từ đáy trang mọc ngược lên trên. Mọi Storage Engine đều xoay quanh 3 biến số thiết kế (theo sách *Database Internals*): `Buffering` (đệm RAM), `Immutability` (bất biến vs. sửa tại chỗ) và `Ordering` (thứ tự lưu trữ).",
        "SELECT lp, t_xmin, t_xmax, t_ctid FROM heap_page_items(get_raw_page('hoa_don', 0));",
        "Nhờ mảng trung gian `Line Pointers (Ptr)`, khi dòng `#HD01` bị nén hoặc dời vị trí bên trong trang `8KB`, các chỉ mục `B-Tree` bên ngoài vẫn trỏ đúng vào số thứ tự `Ptr` mà không bị gãy."
    ),
    (
        "db.wal-checkpointer",
        "Write Path, Dirty Pages, WAL (Write-Ahead Log, LSN) & Checkpointer",
        "STORAGE ENGINE & MEMORY",
        ["F03", "D02"],
        [
            "wal", "wal record", "wal buffer", "wal writer", "wal files", "append-only wal",
            "lsn", "log sequence number", "dirty page", "dirty pages", "checkpointer",
            "data files", "offset", "dongia = 30000"
        ],
        "Bí quyết giúp PostgreSQL vừa ghi cực nhanh vừa không mất 1 byte khi sập nguồn: khi sửa đơn `#HD01`, máy chỉ sửa trang `8KB` trên RAM (`Dirty Page`) và ghi nối đuôi tuần tự một dòng nhật ký mang mã `LSN` xuống đĩa (`WAL Files`), rồi để `Checkpointer` thong thả xả các trang bẩn xuống `Data Files` sau (ví dụ mỗi `5 phút`).",
        "Ghi vào `Data Files` là ghi ngẫu nhiên (`Random I/O` theo `Offset`) rất chậm, trong khi ghi vào `WAL Files` là ghi tuần tự nối đuôi (`Append-only Sequential I/O`). Khi khách bấm `COMMIT`, `WAL Writer` chỉ cần đẩy `WAL Buffer` tới đúng mã `LSN` (`Log Sequence Number`) xuống đĩa là giao dịch thành công mỹ mãn; nếu mất điện, PostgreSQL đọc lại `WAL` từ điểm `Checkpoint` gần nhất để phục hồi (`Crash Recovery`).",
        "SELECT pg_current_wal_lsn();   -- Xem mã LSN hiện tại của nhật ký WAL",
        "Không bao giờ xóa tay thư mục `pg_wal/` vì đó là sinh mạng dùng để khôi phục các `Dirty Pages` chưa kịp được `Checkpointer` ghi xuống đĩa."
    ),
    (
        "db.mvcc-autovacuum",
        "ACID, Lock Manager, MVCC Snapshot, Isolation Levels (Dirty Reads/Writes) & Autovacuum Worker",
        "CONCURRENCY & TRANSACTIONS",
        ["F03", "D02"],
        [
            "mvcc", "mvcc tuple", "multi-version concurrency control", "autovacuum",
            "autovacuum worker", "lock manager", "dirty reads", "dirty writes",
            "snapshot", "xmin", "xmax"
        ],
        "Nhờ cơ chế đa phiên bản `MVCC`, khi một người đang sửa giá đơn `#HD01` thì hàng nghìn người khác vẫn đọc được đơn `#HD01` tức thì mà không ai phải chờ khóa (`Readers never block Writers, Writers never block Readers`).",
        "Khi chạy lệnh `UPDATE`, PostgreSQL không ghi đè lên dòng cũ mà sinh ra một `Tuple` phiên bản mới trên trang `8KB`, đánh dấu phiên bản cũ là đã hết hạn (`Dead Tuple` qua cặp nhãn giao dịch `xmin / xmax`). Các cấp độ cô lập (`Isolation Levels`: Read Committed, Repeatable Read, Serializable) cùng `Lock Manager` ngăn chặn dị thường `Dirty Reads` và `Dirty Writes`, còn tiến trình ngầm `Autovacuum Worker` định kỳ quét dọn các `Dead Tuples` để thu hồi khoảng trống `Free Space`.",
        "VACUUM (VERBOSE, ANALYZE) hoa_don;",
        "Nếu tắt `Autovacuum` hoặc để giao dịch treo quá lâu, các phiên bản cũ (`Dead Tuples`) không được dọn sẽ gây phình bảng (`Table Bloat`) làm chậm toàn bộ hệ thống."
    ),
    (
        "db.btree-vs-lsm",
        "Cấu trúc Chỉ mục & Lưu trữ: B-Tree (Mutable, Latch Crabbing) vs. LSM-Tree (Immutable, Append-only)",
        "INDEXING & STORAGE STRUCTURES",
        ["F03", "D02"],
        [
            "b-tree", "b-tree index", "lsm-tree", "log-structured merge-tree", "append-only lsm",
            "latch crabbing", "seq scan", "index scan", "sstable", "memtable"
        ],
        "Hai trường phái cấu trúc dữ liệu thống trị thế giới Database: `B-Tree` (cây cân bằng khả biến sửa trực tiếp các trang `8KB` trên đĩa — tối ưu cho tốc độ Đọc) và `LSM-Tree` (cây hợp nhất bất biến chỉ ghi nối đuôi vào RAM/SSTable — tối ưu cho tốc độ Ghi cực lớn).",
        "Trong PostgreSQL, chỉ mục mặc định là `B-Tree`: thay vì quét tuần tự toàn bảng (`Seq Scan` tốn $O(N)$), truy vấn nhảy qua các nút cây cân bằng tốn $O(\\log N)$ để tìm trúng `Line Pointer` của `#HD01`. Để nhiều luồng cùng duyệt và tách nút `B-Tree` an toàn mà không khóa nghẽn cả cây, động cơ dùng kỹ thuật `Latch Crabbing` (khóa chốt nút con an toàn rồi mới nhả chốt nút cha — *Database Internals*).",
        "CREATE INDEX idx_hoadon_kh ON hoa_don (ma_kh);",
        "Chọn `B-Tree` (PostgreSQL, MySQL InnoDB) khi tải đọc và tra cứu điểm chiếm ưu thế; chọn `LSM-Tree` (RocksDB, Cassandra, ScyllaDB) khi tải ghi log/time-series dồn dập."
    ),
    (
        "db.optimizer-explain",
        "Query Optimizer, Execution Plan (EXPLAIN ANALYZE) & Công cụ Quản trị (psql, pgAdmin 4, pg_stat_statements)",
        "QUERY EXECUTION & OPS",
        ["F03"],
        [
            "query optimizer", "execution plan", "explain", "explain analyze", "psql",
            "pgadmin 4", "pg_stat_statements", "join optimization"
        ],
        "Bộ não `Query Optimizer` ước lượng chi phí I/O và CPU để chọn đường chạy rẻ nhất cho câu SQL, còn lệnh `EXPLAIN ANALYZE` và bảng `pg_stat_statements` là 'máy chụp X-quang' phơi bày chính xác từng mili-giây thực thi.",
        "Khi nhận câu lệnh `SELECT` hoặc `JOIN` nhiều bảng của đơn `#HD01`, `Query Optimizer` dựa trên thống kê phân phối dữ liệu để chọn thuật toán kết nối (`Nested Loop`, `Hash Join`, hay `Merge Join`) và phương thức quét (`Seq Scan`, `Index Scan`, `Bitmap Heap Scan`). Kỹ sư dùng giao diện dòng lệnh `psql` hoặc đồ họa `pgAdmin 4` kết hợp tiện ích `pg_stat_statements` để săn lùng các câu truy vấn ngốn tổng thời gian CPU nhiều nhất.",
        "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM hoa_don h JOIN chi_tiet c ON h.ma_hd = c.ma_hd WHERE h.ma_hd = 'HD01';",
        "Lưu ý: `EXPLAIN ANALYZE` thực sự chạy câu lệnh SQL trên Database, vì vậy nếu dùng cho `UPDATE / DELETE` trên Production thì bắt buộc bọc trong `BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;`."
    ),
    (
        "db.scaling-sharding",
        "Vertical Scaling (Scale-up) vs. Horizontal Scaling (Scale-out / Partitioning / Sharding)",
        "SCALABILITY & DISTRIBUTED DB",
        ["F03", "D02", "P01"],
        [
            "vertical scaling", "scale-up", "horizontal scaling", "scale-out",
            "distributed shard", "scale-out / sharding", "partitioning / sharding",
            "single node", "node", "nodes"
        ],
        "`Scale-up (Mở rộng dọc)` là nâng cấp một máy chủ đơn lẻ (`Single Node`) lên nhiều CPU/RAM/SSD hơn nhưng sớm chạm trần vật lý; `Scale-out / Sharding (Mở rộng ngang)` là chia nhỏ hàng tỷ đơn hàng `#HD01` ra nhiều máy chủ (`Nodes`) cùng gánh tải.",
        "Khi bảng hóa đơn vượt ngưỡng vài trăm triệu dòng hoặc băng thông ghi vượt sức chịu đựng của 1 đĩa NVMe, kỹ sư bắt đầu bằng `Partitioning` (chia bảng lớn thành các phân vùng con theo tháng/năm ngay trên 1 máy) và tiến tới `Sharding` (băm khóa `Shard Key` để phân tán dữ liệu sang nhiều `Node` độc lập).",
        "CREATE TABLE hoa_don (ma_hd TEXT, ngay_dat DATE) PARTITION BY RANGE (ngay_dat);",
        "Mở rộng ngang (`Sharding`) giải phóng giới hạn dung lượng nhưng đánh đổi bằng chi phí truy vấn liên mảnh (`Cross-Shard JOIN`) và giao dịch phân tán 2 pha (`2PC`)."
    ),
    (
        "db.ha-replication-pgd",
        "Replication (Sync/Async), High Availability (HA), Failover & Distributed PostgreSQL (PGD 6 Nodes, Witness, Barman, TiDB, YDB)",
        "HIGH AVAILABILITY & CONSENSUS",
        ["F03", "P01"],
        [
            "replication", "sync/async", "high availability", "ha", "failover",
            "distributed postgresql", "distributed sql", "primary", "replica",
            "6 pgd nodes", "pgd", "pgd proxy", "witness node", "global consensus",
            "barman", "barman backup", "tidb", "ydb", "always-on multi-location"
        ],
        "Để hệ thống không bao giờ chết khi cháy ổ cứng hay sập cả trung tâm dữ liệu, dữ liệu của `#HD01` được nhân bản liên tục từ máy chính (`Primary`) sang các máy phụ (`Replica`) kết hợp sao lưu `Barman` và kiến trúc đa vùng `PGD` hoặc `Distributed SQL (TiDB / YDB)`.",
        "Nhân bản bất đồng bộ (`Async Replication`) phản hồi cực nhanh nhưng có nguy cơ mất vài dòng cuối nếu `Primary` sập đột ngột; nhân bản đồng bộ (`Sync Replication`) đảm bảo 0 mất dữ liệu nhưng tăng độ trễ mạng. Trong kiến trúc đa vùng luôn sẵn sàng (`Always-on Multi-location` theo sách *Database Design and Modeling with PostgreSQL and MySQL*), cụm chuẩn gồm `6 PGD nodes` (3 nodes ở mỗi vùng dữ liệu) đi kèm `PGD Proxy` điều hướng, `Barman` sao lưu phục hồi thảm họa, và 1 `Witness Node` đặt ở vùng thứ 3 chỉ tham gia bỏ phiếu đồng thuận toàn cục (`Global Consensus` như `Raft / Paxos`) để chống hiện tượng tự phong vua (`Split-Brain`).",
        "SELECT client_addr, state, sync_state, replay_lag FROM pg_stat_replication;",
        "`Witness Node` ở vùng thứ 3 không cần lưu toàn bộ dữ liệu nặng nhưng đóng vai trò lá phiếu quyết định (Quorum) khi 1 trong 2 vùng chính bị đứt cáp quang."
    ),
    (
        "db.nosql-cap-base",
        "SQL vs. NoSQL (Key-Value, Document/BSON, Column-Family, Graph), CAP Theorem (CA/CP/AP) & BASE (LWW, Vector Clocks)",
        "NOSQL & DISTRIBUTED THEORY",
        ["F03", "D02", "P01"],
        [
            "nosql", "sql vs nosql", "key-value", "document", "document/bson", "json/bson document",
            "bson", "column-family", "graph", "ca", "cp", "ap", "ca/cp/ap", "acid / cp",
            "base / ap", "last-write-wins", "lww", "vector clocks"
        ],
        "Khi mạng giữa các máy chủ bị đứt (`Network Partition - P`), định lý `CAP` buộc bạn phải chọn: hoặc giữ dữ liệu nhất quán tuyệt đối nhưng từ chối phục vụ (`CP / ACID`), hoặc vẫn nhận đơn `#HD01` bình thường trên mọi nhánh rồi đồng bộ dần về sau (`AP / BASE — Eventual Consistency`).",
        "Thế giới `NoSQL` chia làm 4 họ cấu trúc chuyên biệt: `Key-Value` (Redis/DynamoDB — tra cứu theo khóa dưới 1 ms), `Document/BSON` (MongoDB — lưu cả đơn hàng `#HD01` kèm mảng món ăn vào 1 tài liệu linh hoạt), `Column-Family` (Cassandra/HBase — ghi phân tán quy mô lớn), và `Graph` (Neo4j — truy vấn mạng lưới quan hệ). Trong các hệ thống `BASE / AP`, khi hai nhánh cùng sửa 1 bản ghi lúc đứt mạng, xung đột được phân xử bằng dấu thời gian `Last-Write-Wins (LWW)` hoặc đồng hồ vector nhân quả (`Vector Clocks` — *Database Internals*).",
        "{\"_id\": \"HD01\", \"khach\": \"Lan\", \"mon\": [{\"ten\": \"Oolong Sua\", \"gia\": 30000, \"sl\": 2}]}",
        "Không có hệ thống phân tán nào đạt `CA` thực sự khi mạng vật lý chắc chắn có lúc đứt (`P`); thực tế kỹ sư luôn phải thiết kế đánh đổi giữa `CP` và `AP`."
    ),

    # =========================================================================
    # F06: CONTAINERIZATION & ORCHESTRATION (CHẶNG 1 -> CHẶNG 4)
    # =========================================================================
    (
        "container.infra-vm-vs-container",
        "Tiến hóa Hạ tầng: Bare Metal, Hypervisor (VM / VPS / Cloud VM) vs. Container (OS-Level Virtualization)",
        "CONTAINER & VIRTUALIZATION",
        ["F06", "P02"],
        [
            "bare metal", "shared hosting", "noisy neighbor", "hypervisor", "type 1", "type 2",
            "virtual machine", "vm", "vms", "vps", "cloud vm", "guest os", "vm tax", "thuế máy ảo",
            "os-level virtualization", "live migration", "ceph/san", "scale-to-zero", "order-api",
            "app.py", "python:3.11-slim"
        ],
        "Nếu Máy ảo (`VM / VPS / Cloud VM`) là những 'căn nhà phố độc lập' mà mỗi căn phải tự xây móng, tự cõng một hệ điều hành riêng (`Guest OS`) nặng hàng chục GB ('Thuế máy ảo' — `VM Tax`), thì **Container** là những 'căn hộ studio' dùng chung toàn bộ móng và hệ thống điện nước (`Host OS Kernel`), chỉ mang theo đúng đồ đạc của ứng dụng (`order-api` vài chục MB) nên khởi động trong 1 giây.",
        "Trên `Bare Metal`, chạy 1 ứng dụng gây lãng phí `90-95% CPU/RAM`, còn cài chung nhiều ứng dụng dễ dính xung đột thư viện (`Dependency Hell`) hoặc hiệu ứng hàng xóm ồn ào (`Noisy Neighbor` trên `Shared Hosting`). `Hypervisor` (`Type 1` Bare-metal như KVM/ESXi hoặc `Type 2` Hosted như VirtualBox) chia cắt phần cứng thành các `VM` (`VPS` nằm trên 1 máy mẹ dễ dính `SPOF`; `Cloud VM` lưu đĩa trên `SAN/Ceph` 3x và có `Live Migration`). `Container` tiến thêm một bước đột phá: vứt bỏ `Guest OS`, ảo hóa ngay ở tầng Hệ điều hành (`OS-level Virtualization`) giúp chạy `50+ Containers/host` thay vì chỉ `~10 VMs/host`.",
        "docker run -d --name order-api -p 8080:8080 order-api:1.0   # Khởi động trong ~1 giây",
        "Nhân vật chính xuyên suốt F06 là tiến trình `order-api` (`app.py` chạy trên `python:3.11-slim` + `PostgreSQL`) tiến hóa từ Bare Metal -> VM -> Container -> 3 Pod Replicas trên Kubernetes."
    ),
    (
        "container.linux-namespaces-cgroups",
        "Linux Namespaces (Cô lập tầm nhìn: pid, net, mnt, ipc, uts, user) & Control Groups (cgroups v2 · OOM Killer)",
        "KERNEL ISOLATION & LIMITS",
        ["F06", "F01"],
        [
            "linux namespaces", "pid namespace", "net namespace", "mnt namespace", "ipc namespace",
            "uts namespace", "user namespace", "host pid: 10423", "virtual pid: 1", "veth",
            "cgroups v2", "cpu.max", "memory.max", "blkio", "oom killer", "sigkill"
        ],
        "Container thực chất là một Process Linux bình thường bị Kernel 'bịt mắt' bằng **6 bức tường kính `Linux Namespaces`** (chỉ nhìn thấy tài nguyên của riêng mình) và 'khóa van điện nước' bằng **`Control Groups (cgroups v2)`** (cấm xài lố CPU/RAM).",
        "**6 Namespaces** cô lập tầm nhìn: `pid` (tiến trình `order-api` có `Host PID: 10423` ngoài máy chủ nhưng tự nhìn thấy mình là `Virtual PID: 1` bên trong Container), `net` (cấp card mạng ảo `veth` và IP riêng `172.17.0.2`), `mnt` (gốc `/` riêng), `ipc`, `uts` (hostname riêng), và `user` (ánh xạ UID `0` trong container sang UID thường ngoài host). **Control Groups (`cgroups v2`)** kiểm soát định lượng qua `/sys/fs/cgroup`: giới hạn `cpu.max`, `memory.max` (ví dụ `512MB` cho `order-api`) và băng thông đĩa `BlkIO`. Nếu tiến trình cố tình vượt trần `memory.max`, `OOM Killer` của Kernel sẽ bắn tín hiệu `SIGKILL (Exit Code 137)` tiêu diệt đúng tiến trình đó để bảo vệ máy chủ.",
        "lsns   # Liệt kê các Namespaces; hoặc xem giới hạn tại /sys/fs/cgroup/memory.max",
        "Hiểu rõ `Host PID: 10423` vs. `Virtual PID: 1` giúp kỹ sư hiểu tại sao `ps aux` trên máy chủ thấy toàn bộ các container, còn `ps aux` trong container chỉ thấy mỗi `app.py`."
    ),
    (
        "container.overlayfs-seccomp",
        "Union Filesystem (OverlayFS Copy-on-Write: LowerDir, UpperDir, Merged), Syscalls (clone, unshare, pivot_root) & Bảo mật (Capabilities, Seccomp)",
        "FILESYSTEM & CONTAINER SECURITY",
        ["F06", "F01"],
        [
            "overlayfs", "union filesystem", "lowerdir", "upperdir", "workdir", "merged",
            "clone()", "unshare()", "pivot_root()", "chroot()", "linux capabilities",
            "cap_net_bind_service", "cap_sys_admin", "seccomp", "seccomp filter"
        ],
        "Thay vì nhân bản 50 bản hệ điều hành Debian cho 50 Container, **`OverlayFS`** cho cả 50 Container dùng chung 1 tầng đĩa gốc chỉ-đọc (`LowerDir`) và chỉ tạo 1 tờ giấy kính mỏng ghi-được (`UpperDir`) trên đỉnh từng Container theo cơ chế `Copy-on-Write`.",
        "Khi khởi tạo Container, Runtime gọi 3 System Calls cốt lõi: `clone()` (tạo tiến trình kèm cờ Namespaces), `unshare()` (tách không gian tên), và `pivot_root()` (đổi gốc `/` sang thư mục `Merged` của `OverlayFS`, an toàn hơn `chroot()`). Để khóa chặt bảo mật khi dùng chung Kernel, Container bị tước bỏ quyền tối thượng của `root` thành các mảnh nhỏ qua **Linux Capabilities** (chỉ giữ quyền cần thiết như `CAP_NET_BIND_SERVICE`, tước bỏ `CAP_SYS_ADMIN`) và gắn phễu lọc **Seccomp (`Secure Computing Mode`)** chặn hơn 44 System Calls nguy hiểm (như `reboot`, `mount`, `kexec_load`).",
        "docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE --security-opt seccomp=default.json order-api:1.0",
        "Vì tầng `UpperDir` của `OverlayFS` sẽ biến mất vĩnh viễn ngay khi xóa Container, tuyệt đối không bao giờ lưu dữ liệu Database trực tiếp vào tầng ghi của Container!"
    ),
    (
        "container.oci-runtime-stack",
        "Luồng Build-Ship-Run, Persistent Volumes & Giải phẫu Chuỗi Thực thi Chuẩn OCI (Docker CLI -> dockerd -> containerd -> shim -> runc vs. Podman / CRI-O)",
        "OCI RUNTIME & PACKAGING",
        ["F06", "P02"],
        [
            "build-ship-run", "oci image", "container registry", "persistent volume",
            "persistent volumes", "/var/lib/docker/volumes", "/var/lib/postgresql/data",
            "docker cli", "dockerd", "containerd-shim", "runc", "libcontainer",
            "podman", "cri-o", "daemonless", "rootless"
        ],
        "Khi bạn gõ `docker run`, `Docker Daemon (dockerd)` không trực tiếp tạo Container mà chuyển việc qua dây chuyền chuẩn công nghiệp **OCI**: `Docker CLI → dockerd → containerd → containerd-shim → runc (libcontainer)`.",
        "Giải phẫu từng mắt xích: (1) `Docker CLI` gửi REST API tới `dockerd`; (2) `dockerd` ủy quyền quản lý vòng đời cho `containerd`; (3) `containerd` đẻ ra tiến trình giữ chỗ nhẹ `containerd-shim`; (4) `shim` gọi `runc` (`libcontainer`) nói chuyện trực tiếp với Linux Kernel để dựng Namespaces/cgroups cho `order-api`. Ngay khi Container chạy lên, **`runc` lập tức tự thoát**, nhường quyền làm cha cho `containerd-shim` giữ cổng `stdin/stdout` — nhờ vậy dù bạn khởi động lại `dockerd`, Container `order-api` vẫn sống bình thường! Với Database `PostgreSQL`, kỹ sư bắt buộc gắn **Persistent Volume** (`/var/lib/docker/volumes/...` ánh xạ vào `/var/lib/postgresql/data`) để dữ liệu đi xuyên qua `OverlayFS` xuống thẳng đĩa Host. Ngoài Docker, hệ sinh thái còn có **Podman** (`Daemonless & Rootless` — không cần daemon chạy ngầm quyền root) và **CRI-O** (Runtime tối giản chuyên biệt cho Kubernetes).",
        "docker volume create pgdata && docker run -v pgdata:/var/lib/postgresql/data postgres:16",
        "Nhờ kiến trúc tách rời `containerd-shim`, việc nâng cấp hoặc khởi động lại Docker Engine không còn làm chết toàn bộ các Container đang chạy trên máy chủ."
    ),
    (
        "container.kubernetes-orchestration",
        "Kubernetes (K8s) Orchestration: CRI, Declarative YAML, Control Plane (API Server, etcd, Scheduler, Controller), Worker Node (kubelet, kube-proxy) & Workloads (Pod, ReplicaSet, Deployment, Service IPVS, Probes)",
        "KUBERNETES ORCHESTRATION",
        ["F06", "P02"],
        [
            "cri", "container runtime interface", "declarative yaml", "desired state",
            "immutable infrastructure", "control plane", "kube-apiserver", "etcd",
            "kube-scheduler", "kube-controller-manager", "worker node", "kubelet",
            "kube-proxy", "replicaset", "clusterip", "ipvs", "ingress controller",
            "liveness probe", "readiness probe", "startup probe", "3 pod replicas"
        ],
        "Khi quy mô vượt lên hàng trăm máy chủ, **Kubernetes (`K8s`)** đóng vai trò 'nhạc trưởng tự động 24/7': bạn chỉ cần nộp bản kê khai trạng thái mong muốn (**`Declarative YAML`** — ví dụ `replicas: 3`), bộ não **`Control Plane`** sẽ tự động xếp lịch, canh gác và hồi sinh các **`Pod`** của `order-api` ngay cả khi 1 máy chủ bốc cháy lúc 2 giờ sáng.",
        "Kiến trúc K8s gồm 2 nửa: (1) **Control Plane**: mọi lệnh đều đi qua cổng chính `kube-apiserver` để lưu vào sổ cái phân tán `etcd` (đồng thuận `Raft`); `kube-controller-manager` chạy vòng lặp đối soát (`Reconciliation Loop`: thấy `Actual State = 2` khác `Desired State = 3` liền yêu cầu tạo bù 1 Pod); `kube-scheduler` chấm điểm chọn `Worker Node` còn trống tài nguyên. (2) **Worker Node**: đặc vụ `kubelet` nhận lệnh và gọi thẳng `containerd / CRI-O` qua giao diện chuẩn **`CRI` (`Container Runtime Interface` — bỏ qua `dockerd`)** để dựng **Pod** (đơn vị nhỏ nhất bọc các container dùng chung `net/ipc/uts` Namespace và IP nội bộ). Tầng mạng dùng **Service (`ClusterIP` + bảng định tuyến `iptables / IPVS` của `kube-proxy`)** kết hợp **Ingress** và 3 chốt khám sức khỏe (**`Startup / Liveness / Readiness Probes`**) để cân bằng tải và cập nhật phiên bản mới không gián đoạn (`Rolling Update`).",
        "kubectl apply -f order-api-deployment.yaml && kubectl get pods -o wide",
        "Trong một `Pod`, các container (như `order-api` và `log-agent` sidecar) dùng chung `Network Namespace` nên gọi nhau trực tiếp qua `localhost`, nhưng vẫn bị cô lập hệ thống tệp (`mnt` Namespace riêng)."
    ),
    # =========================================================================
    # D01: INGESTION LAYER — KAFKA, DEBEZIUM CDC & PRODUCTION CHALLENGES
    # =========================================================================
    (
        "ingestion.source-gigo-etlt",
        "Ingestion Layer, GIGO Principle, Push/Pull/Poll Patterns & EtLT Subpattern",
        "DATA INGESTION & SOURCE SYSTEMS",
        ["D01", "D02"],
        [
            "ingestion layer", "gigo", "gigo principle", "garbage in garbage out",
            "push pattern", "pull pattern", "poll pattern", "micro-batching",
            "semi-structured", "unstructured data", "structured data", "etlt",
            "row-based", "column-based", "hybrid row-group"
        ],
        "Tầng thu thập dữ liệu (Ingestion Layer) là trạm kiểm soát biên giới tách rời các hệ thống nguồn OLTP khỏi kho phân tích OLAP, ngăn chặn định luật GIGO (Garbage In, Garbage Out) và bảo vệ CPU nguồn khỏi các truy vấn quét nặng.",
        "Phân loại dữ liệu theo 3 cấp cấu trúc (Structured, Semi-Structured, Unstructured), điều phối luồng qua 3 mẫu giao tiếp (Push đẩy chủ động, Pull kéo theo yêu cầu, Poll thăm dò định kỳ) và áp dụng mô hình EtLT (Extract - Light Transform - Load - Transform) để ẩn thông tin nhạy cảm PII, chuẩn hóa múi giờ và khử trùng ngay trên đường bay trước khi hạ cánh xuống Data Lakehouse.",
        "aws s3 cp s3://raw-landing/orders_2026.parquet s3://bronze-zone/orders/",
        "Áp dụng mô hình EtLT giúp phát hiện sớm lỗi Schema Drift từ hệ thống nguồn trước khi dữ liệu bẩn kịp làm hỏng các bảng báo cáo tài chính ở tầng Gold."
    ),
    (
        "ingestion.cdc-three-generations",
        "Three Generations of Change Data Capture (CDC): Timestamp Polling, Trigger Shadow Table & Log-Based CDC (WAL / binlog)",
        "CHANGE DATA CAPTURE (CDC)",
        ["D01", "F03"],
        [
            "change data capture", "timestamp-based cdc", "timestamp polling",
            "trigger-based cdc", "shadow table", "log-based cdc", "high-watermark",
            "soft delete", "hard delete", "write amplification", "pgoutput",
            "binlog_format", "wal_level"
        ],
        "Ba thế hệ bắt biến động dữ liệu (INSERT, UPDATE, DELETE) tiến hóa từ quét bảng định kỳ (Polling) và gắn bẫy đồng bộ (Trigger) sang đọc tuần tự tệp nhật ký giao dịch nhị phân (Log-Based CDC) với độ trễ mili-giây và 0% tải truy vấn bảng gốc.",
        "Timestamp Polling quét cột `last_modified` nhưng mù hoàn toàn trước lệnh xóa vật lý `DELETE` và dễ sót dữ liệu do `Uncommitted Transaction Skew`. Trigger-based CDC ghi đồng bộ vào bảng bóng (`shadow_table`) trong cùng giao dịch ACID làm nhân đôi độ trễ ghi I/O. Chỉ có Log-Based CDC đọc trực tiếp luồng byte từ PostgreSQL `pg_wal` (`wal_level = logical`, `pgoutput`) hoặc MySQL `binlog` (`binlog_format = ROW`) mới tách rời hoàn toàn khỏi luồng giao dịch chính.",
        "SELECT * FROM pg_create_logical_replication_slot('debezium_orders_slot', 'pgoutput');",
        "Trên hệ thống thanh toán/đơn hàng lớn, tuyệt đối tránh gắn Trigger CDC lên bảng chính vì một lỗi nhỏ trong hàm Trigger sẽ làm Rollback toàn bộ giao dịch mua hàng của khách."
    ),
    (
        "ingestion.kafka-kraft-ecosystem",
        "Apache Kafka Distributed Event Streaming, KRaft Consensus & Extended Ecosystem (Kafka Connect, Schema Registry, MirrorMaker 2)",
        "APACHE KAFKA ARCHITECTURE",
        ["D01", "D02"],
        [
            "apache kafka", "event streaming", "kafka broker", "kafka cluster",
            "kraft", "kraft mode", "apache zookeeper", "zookeeper",
            "kafka connect", "mirrormaker 2", "mirrormaker", "kafka streams"
        ],
        "Apache Kafka thay thế mạng nhện tích hợp điểm-điểm O(N x M) bằng một trục xương sống sự kiện phân tán (Distributed Append-Only Commit Log) có độ phức tạp O(N + M), tự điều phối Metadata bằng giao thức đồng thuận KRaft mà không cần ZooKeeper.",
        "Từ phiên bản Kafka 3.3+ / 4.0, bộ điều khiển đồng thuận KRaft (Kafka Raft Metadata Mode) lưu toàn bộ trạng thái cụm vào topic nội bộ `__cluster_metadata`, hỗ trợ hàng triệu Partitions và rút ngắn thời gian Failover xuống vài mili-giây. Hệ sinh thái mở rộng gồm Kafka Connect (nạp/xả dữ liệu không cần code), Confluent Schema Registry (kiểm định hợp đồng lược đồ Avro/Protobuf) và MirrorMaker 2 (nhân bản liên cụm đa vùng địa lý).",
        "kafka-storage.sh format -t $CLUSTER_UUID -c config/kraft/server.properties",
        "Kết hợp Kafka Connect với Schema Registry giúp tự động chặn đứng các bản ghi vi phạm tương thích lược đồ (Schema Drift) ngay tại cửa ngõ Producer."
    ),
    (
        "ingestion.partition-offset-lag",
        "Kafka Topic Design, Partition Sizing Formula, Zero-Copy sendfile(2), Offset Pointer & Consumer Lag",
        "APACHE KAFKA ARCHITECTURE",
        ["D01"],
        [
            "kafka topic", "partition", "partitions", "unit of parallelism",
            "consumer lag", "sendfile", "os page cache", "high watermark",
            "log end offset", "control record"
        ],
        "Partition là đơn vị song song hóa vật lý nhỏ nhất của Kafka: mỗi bản ghi vào Partition được gán một số nguyên thứ tự bất biến (Offset), và dữ liệu được truyền thẳng từ OS Page Cache ra Card mạng qua lời gọi hệ thống Zero-Copy sendfile(2).",
        "Số lượng Partition được định cỡ theo công thức N = max(ceil(T_target / T_producer_per_part), ceil(T_target / T_consumer_per_part)) với thông lượng ~5-10 MB/s mỗi Partition. Consumer theo dõi tiến độ đọc qua topic nội bộ `__consumer_offsets`; khoảng cách `Consumer Lag = Log End Offset - Current Consumer Offset` là chỉ số vận hành quan trọng số 1 để phát hiện tắc nghẽn xử lý và kích hoạt mở rộng ngang.",
        "kafka-consumer-groups.sh --bootstrap-server kafka:9092 --describe --group fraud-detector",
        "Nhờ kỹ thuật Zero-Copy `sendfile(2)` qua DMA, Kafka không cần chép dữ liệu vào vùng nhớ JVM Heap, cho phép phục vụ nhiều Consumer Group cùng lúc ở tốc độ bão hòa đường truyền mạng."
    ),
    (
        "ingestion.producer-consumer-isr-eos",
        "Kafka Internals: Producer murmur2 Hash & RecordAccumulator, Consumer Group Rebalance, ISR Replication, Delivery Guarantees (EOS) & Log Compaction",
        "KAFKA INTERNALS & RELIABILITY",
        ["D01"],
        [
            "murmur2", "sticky partitioner", "recordaccumulator", "linger.ms", "batch.size",
            "consumer group", "cooperativestickyassignor", "rebalance",
            "in-sync replicas", "isr", "replication.factor", "min.insync.replicas",
            "at-most-once", "at-least-once", "exactly-once", "enable.idempotence",
            "log compaction", "tombstone"
        ],
        "Bộ cơ học nội tại giúp Kafka vừa đạt thông lượng cực đại vừa bảo toàn dữ liệu tuyệt đối: băm khóa murmur2 giữ thứ tự theo khách hàng, quy tắc 1 Partition tối đa 1 Consumer/Group, bầu chọn Leader từ tập ISR và nén nhật ký theo khóa (Log Compaction).",
        "Producer băm khóa `murmur2(key) % numPartitions` để gom mọi sự kiện cùng thực thể vào 1 Partition và nén lô tại `RecordAccumulator`. Trong cùng Consumer Group, nếu số Consumer vượt quá số Partition thì các Consumer dư thừa sẽ rơi vào trạng thái nhàn rỗi (`IDLE`). Để chống mất dữ liệu (như bẫy `acks=1` khi Leader sập trước khi Follower kịp chép), Production bắt buộc dùng bộ ba `replication.factor=3`, `min.insync.replicas=2`, `acks=all` kết hợp `enable.idempotence=true` (PID + Sequence Number). Trên đĩa, `cleanup.policy=compact` giữ lại giá trị mới nhất cho mỗi khóa và xóa khóa qua bản ghi bia mộ Tombstone (`value=null`).",
        "kafka-configs.sh --bootstrap-server kafka:9092 --alter --entity-type topics --entity-name prod.orders --add-config min.insync.replicas=2,cleanup.policy=compact",
        "Cấu hình `acks=1` KHÔNG đảm bảo chống mất dữ liệu vì Leader có thể sập nguồn ngay sau khi trả ACK nhưng trước khi các Follower trong tập ISR kịp kéo bản ghi về."
    ),
    (
        "ingestion.debezium-wal-outbox",
        "Debezium CDC Pipeline: Snapshot-to-WAL Handover, Event Envelope (before/after/op), WAL Bloat Prevention, Dead Letter Queue (DLQ) & Transactional Outbox Pattern",
        "DEBEZIUM CDC & PRODUCTION OPS",
        ["D01", "D02"],
        [
            "debezium", "replication slot", "wal bloat", "confirmed_flush_lsn",
            "heartbeat.interval.ms", "max_slot_wal_keep_size", "poison pill",
            "dead letter queue", "dlq", "hot partition", "dual-write",
            "transactional outbox", "outbox pattern", "single message transforms"
        ],
        "Debezium là nền tảng CDC phân tán chạy trên Kafka Connect, thực hiện chuyển giao không khe hở từ chụp ảnh lịch sử (Consistent Snapshot) sang đọc trực tiếp luồng WAL/binlog và đóng gói biến động thành phong bì chuẩn hóa before/after/source/op.",
        "Trong vận hành thực chiến, kỹ sư phải hóa giải 4 rủi ro sinh tử: (1) Chống nổ ổ cứng `pg_wal` do kẹt Replication Slot bằng cách bật `heartbeat.interval.ms`, `heartbeat.action.query` và khóa trần `max_slot_wal_keep_size`; (2) Cô lập bản ghi lỗi (`Poison Pill`) sang kênh cách ly `Dead Letter Queue` (`errors.tolerance=all`); (3) Chống lệch tải `Hot Partition` bằng Salting Key và giám sát `UnderReplicatedPartitions == 0`; (4) Xóa sổ lỗi ghi kép (`Dual-Write`) trong Microservices bằng mẫu `Transactional Outbox Pattern` (ghi bảng nghiệp vụ và bảng `outbox_events` trong cùng 1 ACID Transaction cục bộ).",
        "curl -X POST -H 'Content-Type: application/json' --data @register-postgres-connector.json http://connect:8083/connectors",
        "Nếu bảng được Debezium theo dõi nằm chung Database với các bảng ghi ồ ạt nhưng bản thân nó ít phát sinh giao dịch, việc quên cấu hình `heartbeat.interval.ms` sẽ khiến `confirmed_flush_lsn` đứng im và làm đầy 100% ổ cứng PostgreSQL!"
    ),

    # =========================================================================
    # F05: VALIDATION & VERIFICATION (V-MODEL, PYTEST, MOCK, TESTCONTAINERS, TDD)
    # =========================================================================
    (
        "validation.v-model-shift-left",
        "Validation & Verification Model (V-Model) & Shift-Left Cost of Bugs (1x → 30x)",
        "QUALITY & V-MODEL",
        ["F05"],
        [
            "v-model", "verification", "validation", "shift-left", "shift-left testing",
            "cost of bugs", "software lifecycle", "sdlc", "user acceptance testing", "uat"
        ],
        "Mô hình chữ V (V-Model) ghép cặp đối xứng từng pha thiết kế bên nhánh trái (Verification — làm đúng quy trình) với một pha kiểm thử bên nhánh phải (Validation — làm đúng sản phẩm), nhằm phát hiện lỗi sớm trước khi chi phí sửa lỗi nhân lên 30 lần trên Production.",
        "Nhánh trái Verification kiểm tra tài liệu và cấu trúc thiết kế trước khi chạy code (`Requirement Gathering → Functional Design → Internal System Design → Module Design`); đáy chữ V là `< CODING >`; nhánh phải Validation thực thi phần mềm đối chiếu ngược lại (`Unit Testing → Integration Testing → Functional Testing → UAT`). Đẩy kiểm thử sang trái (Shift-Left) giúp kìm chi phí sửa lỗi ở mức 1x–5x thay vì 30x sau khi phát hành.",
        "pytest tests/unit/   # Chặn lỗi ngay ở pha Coding (5x) trước khi lọt lên Production (30x)",
        "Verification trả lời 'Are we building the product right?', còn Validation trả lời 'Are we building the right product?'."
    ),
    (
        "validation.testing-methods-formal",
        "Black-Box, Grey-Box, White-Box Testing & Formal Verification (Hoare Logic, Symbolic Execution, Mutation Testing)",
        "TESTING PARADIGMS",
        ["F05"],
        [
            "black-box testing", "black box testing", "grey-box testing", "gray box testing",
            "white-box testing", "white box testing", "glass-box testing", "sdet",
            "hoare logic", "symbolic execution", "mutation testing", "automated testing", "manual testing"
        ],
        "Ba phương pháp kiểm thử phân tầng theo mức độ thấu thị mã nguồn: Hộp đen (0% code, chỉ đo Input/Output), Hộp xám (biết API/DB schema) và Hộp trắng (nắm 100% nhánh rẽ nội tại kèm kiểm chứng toán học).",
        "Ở tầng White-box nâng cao, kỹ sư và SDET kết hợp 3 kỹ thuật: Hoare Logic chứng minh tính đúng đắn qua bộ ba `{P} C {Q}` (Precondition → Command → Postcondition); Symbolic Execution thay đầu vào bằng biến ký hiệu để giải điều kiện biên; và Mutation Testing cố tình cấy lỗi giả (Mutants như đổi `>` thành `>=`) để kiểm định xem bộ test có đủ nhạy để phát hiện không.",
        "mutmut run --paths-to-mutate=app/service.py   # Kiểm thử đột biến đánh giá chất lượng bộ test",
        "Đạt 100% Code Coverage chưa chắc đã an toàn nếu thiếu assert chặt chẽ; Mutation Testing giúp phát hiện các bài test 'chạy qua code nhưng không kiểm tra kết quả'."
    ),
    (
        "validation.functional-nonfunctional-scopes",
        "Functional Testing (Unit, Integration, System, Alpha/Beta/UAT) vs. Non-Functional Testing (Load, Stress, Smoke, Regression)",
        "TESTING SCOPES",
        ["F05"],
        [
            "functional testing", "non-functional testing", "unit testing", "unit test",
            "integration testing", "integration test", "system testing", "acceptance testing",
            "alpha testing", "beta testing", "performance testing", "load testing",
            "stress testing", "security testing", "usability testing", "compatibility testing",
            "regression testing", "smoke testing", "recovery testing", "monkey testing"
        ],
        "Functional Testing kiểm tra hệ thống làm được tính năng gì (Unit → Integration → System → Alpha/Beta/UAT), còn Non-Functional Testing đo lường hệ thống vận hành tốt đến mức nào dưới tải cao (Load 500 CCU vs Stress 5000 CCU) và sự cố.",
        "Load Testing kiểm tra độ ổn định ở mức tải kỳ vọng (ví dụ 500 người dùng đồng thời), trong khi Stress Testing ép tải vượt ngưỡng thiết kế (5000 người dùng) để tìm điểm gãy (Breaking Point) và khả năng hạ cánh an toàn. Trong vận hành CI/CD hàng ngày, Smoke Testing lọc nhanh các bản build lỗi nặng, còn Regression Testing đảm bảo code mới không làm vỡ tính năng cũ.",
        "pytest tests/unit tests/integration && locust -f load_test.py --users 500 --spawn-rate 50",
        "Mọi bản vá lỗi (Bugfix) bắt buộc phải đi kèm ít nhất một bài Regression Test để lỗi đó không bao giờ tái xuất hiện ở các phiên bản sau."
    ),
    (
        "validation.pytest-fixtures-conftest",
        "Pytest Framework: Test Discovery, @pytest.fixture, yield Setup/Teardown & Shared conftest.py",
        "PYTEST CORE",
        ["F05"],
        [
            "pytest", "pytest.fixture", "fixtures", "fixture", "conftest", "conftest.py",
            "test discovery", "setup and teardown"
        ],
        "Fixture trong pytest là cơ chế tiêm phụ thuộc (Dependency Injection) tự động thiết lập môi trường trước khi chạy test (trước từ khóa yield) và dọn dẹp tài nguyên sạch sẽ ngay sau khi test kết thúc (sau từ khóa yield).",
        "Pytest tự động dò các file `test_*.py`, hàm `def test_*()` và lớp `class Test*`. Khi hàm test khai báo tên fixture trong danh sách tham số, pytest sẽ thực thi phần Setup trước `yield`, trao đối tượng cho hàm test, và luôn chạy phần Teardown sau `yield` (đóng kết nối DB, xóa dữ liệu tạm). Đặt fixture trong `tests/conftest.py` giúp chia sẻ tự động cho mọi file test cùng thư mục mà không cần câu lệnh import.",
        "@pytest.fixture\ndef db_conn():\n    conn = connect_db()\n    yield conn\n    conn.close()",
        "Sử dụng `yield` trong `@pytest.fixture` an toàn và gọn gàng hơn viết hàm `setup_method`/`teardown_method` truyền thống vì nhánh dọn dẹp sau `yield` luôn chạy kể cả khi bài test bị Fail giữa chừng."
    ),
    (
        "validation.pytest-markers-parametrize",
        "Pytest Markers (@pytest.mark, pyproject.toml, pytest -m) & Data-Driven @pytest.mark.parametrize",
        "PYTEST CORE",
        ["F05"],
        [
            "pytest.mark", "markers", "parametrize", "pytest.mark.parametrize",
            "pytest.mark.skip", "pytest.mark.skipif", "pytest.mark.xfail", "pyproject.toml", "pytest.ini"
        ],
        "Markers gắn nhãn phân loại hàm test để lọc chạy linh hoạt qua cờ `pytest -m`, trong khi `@pytest.mark.parametrize` giúp viết 1 hàm test duy nhất nhưng tự động nhân bản chạy qua hàng chục bộ dữ liệu Input/Expected.",
        "Các custom markers (như `slow`, `api`, `db`) cần được đăng ký trong `[tool.pytest.ini_options]` của `pyproject.toml` để tránh cảnh báo `PytestUnknownMarkWarning`, cho phép lọc bằng biểu thức logic `pytest -m 'slow and not db'`. Marker dựng sẵn `@pytest.mark.parametrize('input, expected', [(1, 2), (2, 3)])` tách mỗi tuple thành một ca kiểm thử độc lập với báo cáo Pass/Fail riêng biệt.",
        "@pytest.mark.parametrize('amount, expected', [(100, 110), (0, 0), (-5, ValueError)])",
        "Kết hợp `@pytest.mark.parametrize` với các giá trị biên (0, số âm, chuỗi rỗng, cực đại) giúp rút ngắn 80% dung lượng code kiểm thử trùng lặp."
    ),
    (
        "validation.mocking-testcontainers-tdd",
        "Dependency Isolation (pytest-mock, mocker.patch, MagicMock, side_effect), Testcontainers, tox, pytest-cov & TDD (Red-Green-Refactor)",
        "MOCKING, INFRA & TDD",
        ["F05"],
        [
            "pytest-mock", "mocker", "mocker.patch", "magicmock", "side_effect",
            "testcontainers", "postgrescontainer", "tox", "tox.ini",
            "code coverage", "pytest-cov", "test-driven development", "tdd", "red-green-refactor"
        ],
        "Hệ sinh thái khép kín từ cô lập Unit Test bằng `mocker.patch` (luôn patch tại nơi hàm được gọi, không phải nơi định nghĩa), dựng Docker DB thật bằng Testcontainers, đo điểm mù `pytest-cov` đến quy trình viết test trước khi viết code TDD (Red → Green → Refactor).",
        "Khi một module dùng `from myapp.api import get_data`, tham chiếu `get_data` đã gắn vào namespace `myapp.service`, nên bắt buộc phải gọi `mocker.patch('myapp.service.get_data')`. Với Integration Test cần kiểm tra SQL thật, `Testcontainers` tự bật/tắt container `postgres:16`; `tox` chạy ma trận đa phiên bản Python (`py39, py310, py311`); `pytest --cov` chỉ ra các dòng `Miss` chưa được test. Quy trình TDD xoay vòng 3 bước: RED (viết test Fail) → GREEN (viết code tối giản để Pass) → REFACTOR (làm sạch code dưới lưới bảo hiểm của bộ test).",
        "mocker.patch('myapp.service.get_data', return_value={'value': 10})   # Patch tại nơi sử dụng!",
        "Áp dụng TDD cực kỳ hiệu quả cho logic nghiệp vụ cốt lõi và pipeline dữ liệu dài hạn, nhưng cần lưu ý chi phí thời gian phát triển ban đầu thường tăng thêm 20–50%."
    ),

    # =========================================================================
    # D04: TRANSFORMATION LAYER (STREAM · FLINK) — CHẶNG 1 ĐẾN CHẶNG 6
    # =========================================================================
    (
        "flink.architecture-slots",
        "Apache Flink Architecture: Master-Worker (JobManager & TaskManager), Task Slots, Sub-tasks, Parallelism & Execution Graph",
        "FLINK RUNTIME & ARCHITECTURE",
        ["D04"],
        [
            "apache flink", "flink", "jobmanager", "taskmanager", "taskmanagers",
            "task slot", "task slots", "sub-task", "sub-tasks", "subtask", "subtasks",
            "parallelism", "execution graph", "jobgraph", "streamgraph", "dispatcher",
            "checkpoint coordinator", "slot sharing", "unbounded data", "bounded data"
        ],
        "Apache Flink là động cơ xử lý luồng có trạng thái (Stateful Stream Processor) vận hành theo kiến trúc Master-Worker: JobManager đóng vai trò bộ não điều phối và lập lịch, còn các TaskManagers là cơ bắp thực thi các Sub-tasks bên trong những lát cắt tài nguyên gọi là Task Slots.",
        "Khi nhận chương trình từ Client, JobManager phân tích và tối ưu hóa đồ thị luồng thành Execution Graph rồi gán từng Sub-task vào các Task Slots trên TaskManagers. Mỗi Task Slot cô lập một phần cố định bộ nhớ được quản lý (Managed Memory — ví dụ 3 slots thì mỗi slot nhận 1/3 RAM) nhưng chia sẻ chung CPU của TaskManager. Độ song song (Parallelism) quyết định số lượng bản sao Sub-task chạy đồng thời trên các luồng độc lập, trong khi JobManager giám sát sức khỏe qua Heartbeats và phối hợp lưu Checkpoint định kỳ.",
        "flink run -m yarn-cluster -p 4 -ys 2 /opt/flink/jobs/order_streaming_job.py",
        "Một TaskManager có 3 Task Slots sẽ chia mỗi Slot đúng 1/3 Managed Memory để chống tranh chấp bộ nhớ, nhưng cả 3 Slots vẫn dùng chung các nhân CPU của tiến trình JVM đó."
    ),
    (
        "flink.time-watermarks",
        "Flink Time Semantics (Event Time, Ingestion Time, Processing Time), Watermark Clock Formula & Three Watermark Strategies",
        "TIME SEMANTICS & WATERMARKS",
        ["D04"],
        [
            "event time", "ingestion time", "processing time", "watermark", "watermarks",
            "watermark strategy", "watermarkgenerator", "monotonous timestamps",
            "bounded out-of-orderness", "for_bounded_out_of_orderness", "for_monotonous_timestamps",
            "with_idleness", "timestamp extractor", "time skew"
        ],
        "Event Time là thời điểm sự kiện thực sự xảy ra ngoài đời thực (nằm trong payload), còn Watermark là chiếc đồng hồ logic chảy xen kẽ trong luồng sự kiện theo công thức Watermark = max(event_time) - allowed_delay để báo hiệu mọi sự kiện trước mốc đó đã đến đủ.",
        "Trong mạng phân tán, sự kiện có thể xảy ra lúc 10:00:30 (Event Time), vào Flink lúc 10:01:45 (Ingestion Time) và được toán tử xử lý lúc 10:01:46 (Processing Time). Khi Watermark W chạm hoặc vượt mốc kết thúc của một cửa sổ (W >= window_end), Window Operator lập tức đóng cửa sổ và phát kết quả. Flink cung cấp 3 chiến lược sinh Watermark: Monotonous Timestamps (trễ = 0s, dùng cho luồng tăng đơn điệu), Bounded Out-of-Orderness (trễ cố định cấu hình theo phân vị p95/p99 thực tế trên Production), và Custom WatermarkGenerator (tùy biến on_event và on_periodic_emit).",
        "WatermarkStrategy.for_bounded_out_of_orderness(Duration.of_seconds(10)).with_idleness(Duration.of_minutes(1))",
        "Khi đọc từ nhiều Kafka Partitions, Watermark của toán tử hạ nguồn tiến lên theo giá trị nhỏ nhất (min) của tất cả các kênh đầu vào; do đó phải bật with_idleness() để một Partition vắng dữ liệu không làm đóng băng toàn bộ cửa sổ!"
    ),
    (
        "flink.windows-triggers-lateness",
        "Flink Windowing (Tumbling, Sliding, Session, Global), Window Triggers, Allowed Lateness 3-State Lifecycle & Side Output",
        "WINDOWING & LATE DATA",
        ["D04"],
        [
            "tumbling window", "tumbling windows", "sliding window", "sliding windows",
            "session window", "session windows", "global window", "global windows",
            "window assigner", "window trigger", "eventtimetrigger", "allowed lateness",
            "allowed_lateness", "side output", "side_output_late_data", "outputtag", "late events"
        ],
        "Window cắt luồng sự kiện vô hạn thành các lát cắt hữu hạn để tổng hợp (Tumbling cố định, Sliding trượt chồng lấp, Session theo khoảng lặng, Global toàn cục), trong khi Trigger quyết định thời điểm tính toán và bộ đôi Allowed Lateness + Side Output bảo toàn 100% sự kiện đến muộn.",
        "Tumbling, Sliding và Session Windows mặc định đi kèm EventTimeTrigger, riêng Global Window có Default Trigger = None nên nếu quên gắn Trigger sẽ gây rò rỉ bộ nhớ câm lặng (Silent OOM). Khi bật Allowed Lateness, vòng đời cửa sổ đi qua 3 trạng thái: Collecting (trước window_end) -> Waiting (vẫn sống trong bộ nhớ đến window_end + allowed_lateness, mỗi khi có sự kiện trễ lọt vào sẽ điểm hỏa lại / refire để phát kết quả đính chính) -> Deleted (xóa khỏi bộ nhớ). Các sự kiện đến sau khi cửa sổ đã Deleted sẽ được rẽ nhánh an toàn qua Side Output vào Audit Log / Dead Letter Queue hoặc chạy Reprocessing.",
        "windowed_stream.allowed_lateness(Time.seconds(30)).side_output_late_data(OutputTag('late-orders', Types.ROW(...)))",
        "Kiến trúc chuẩn Production luôn kết hợp cả hai: đặt Allowed Lateness ngắn (ví dụ 30s) để tự động đính chính các sự kiện trễ nhẹ trên luồng chính, đồng thời gắn Side Output để hứng toàn bộ sự kiện trễ sâu phục vụ đối soát."
    ),
    (
        "flink.apis-dynamic-table-sql",
        "Flink API Hierarchy: DataStream API (ProcessFunction), Stream-Table Duality (Dynamic Tables), Table API & Flink SQL (TUMBLE, HOP, SESSION)",
        "FLINK APIS & SQL ENGINE",
        ["D04"],
        [
            "datastream api", "datastream", "processfunction", "keyedprocessfunction",
            "table api", "flink sql", "dynamic table", "dynamic tables",
            "stream-table duality", "keyby", "from_data_stream", "to_data_stream",
            "tumble", "hop", "session"
        ],
        "Tháp API 3 tầng của Flink cho phép chọn mức trừu tượng phù hợp: DataStream API kiểm soát từng sự kiện và bộ hẹn giờ ở tầng thấp, trong khi Table API và Flink SQL coi luồng dữ liệu như một Bảng động (Dynamic Table) và biên dịch ra cùng một Execution Plan vật lý tối ưu.",
        "Trong DataStream API, phép biến đổi keyBy() băm khóa để gom các sự kiện cùng thực thể về đúng Sub-task trước khi gọi window() hoặc aggregate(). Nhờ nguyên lý Đối ngẫu Luồng - Bảng (Stream-Table Duality), mỗi sự kiện chảy vào được ánh xạ thành một bản ghi chèn/cập nhật trên Dynamic Table, cho phép viết truy vấn Flink SQL với các hàm cửa sổ dựng sẵn TUMBLE, HOP, SESSION (trải qua 5 bước: Write SQL -> Parse -> Optimize Plan -> Create Execution Plan -> Run on Flink Runtime) và chuyển đổi hai chiều mượt mà qua from_data_stream() / to_data_stream().",
        "SELECT productId, SUM(amount) AS total_sales FROM SalesEvents GROUP BY productId, TUMBLE(event_time, INTERVAL '1' MINUTE)",
        "Table API và DataStream API sinh ra Execution Plan vật lý hoàn toàn giống nhau: sự khác biệt nằm ở năng suất của người lập trình (buồng lái vs. buồng máy), không phải ở tốc độ thực thi!"
    ),
    (
        "flink.state-rocksdb-checkpoint",
        "Flink Stateful Processing: Keyed vs. Operator State, State Backends (JVM Heap vs. RocksDB), Checkpoint Barriers (Chandy-Lamport) & Exactly-Once",
        "STATE & CHECKPOINTING",
        ["D04"],
        [
            "stateful", "stateless", "keyed state", "operator state", "valuestate",
            "liststate", "mapstate", "state backend", "hashmapstatebackend",
            "embeddedrocksdbstatebackend", "rocksdb", "checkpoint", "checkpointing",
            "checkpoint barrier", "checkpoint barriers", "chandy-lamport", "savepoint"
        ],
        "Mỗi sự kiện đi qua toán tử có trạng thái đều kích hoạt chu trình 5 bước đọc/ghi State cục bộ (trên JVM Heap hoặc ổ đĩa NVMe qua RocksDB), và được bảo vệ chống sập nguồn nhờ các rào chắn Checkpoint Barriers chảy dọc luồng dữ liệu theo thuật toán Chandy-Lamport.",
        "Keyed State lưu trữ tách biệt cho từng khóa sau keyBy(), trong khi Operator State gắn với từng bản sao Sub-task (điển hình là Kafka Source lưu Partition Offsets). Khi JobManager phát lệnh chụp Checkpoint N, các Source bơm Barrier N vào luồng dữ liệu; mỗi khi Barrier N đi qua một toán tử, toán tử đó chụp ảnh trạng thái cục bộ và đẩy bất đồng bộ (asynchronously) xuống S3/HDFS mà không làm dừng luồng xử lý. Khi gặp sự cố, các TaskManagers khôi phục State từ Checkpoint N mới nhất và tua ngược (rewind) Kafka Source về đúng Offset tại mốc N để cam kết Exactly-Once.",
        "env.enable_checkpointing(10000, CheckpointingMode.EXACTLY_ONCE); env.set_state_backend(EmbeddedRocksDBStateBackend(True))",
        "Bước 2 (Đọc State) và Bước 4 (Ghi State) diễn ra trên TỪNG SỰ KIỆN MỘT — vì vậy State bắt buộc phải đặt cục bộ ngay trên TaskManager (RAM hoặc RocksDB) thay vì gọi qua mạng tới CSDL ngoài!"
    ),
    (
        "flink.chaining-backpressure-deploy",
        "Flink Performance & Deployment: Operator Chaining, Credit-Based Backpressure Resolution (Async I/O, RocksDB Tuning) & Application vs. Session Mode",
        "PERFORMANCE & DEPLOYMENT",
        ["D04"],
        [
            "operator chaining", "disable_chaining", "start_new_chain", "backpressure",
            "credit-based flow control", "async i/o", "asyncdatastream", "unorderedwait",
            "block cache", "write buffer", "session mode", "application mode",
            "flink kubernetes operator"
        ],
        "Bốn trụ cột vận hành Flink ở quy mô Production: hàn gắn các toán tử tương thích vào chung 1 luồng CPU bằng Operator Chaining, chẩn đoán và xử lý nút thắt cổ chai qua tín hiệu Backpressure, và triển khai cô lập tuyệt đối theo kiến trúc Application Mode.",
        "Operator Chaining gộp các toán tử nối tiếp (như Source + Map + Filter) vào cùng một luồng trong 1 Task Slot để truyền đối tượng trực tiếp trên RAM, loại bỏ hoàn toàn chi phí Serialization, Network Buffer và chuyển ngữ cảnh luồng. Khi một toán tử hạ nguồn bị chậm, cơ chế Credit-Based Flow Control làm đầy bộ đệm và truyền áp lực phanh (Backpressure) ngược về Source (hiển thị HIGH Red trên Flink Web UI); thứ tự xử lý chuẩn là: (1) tăng Parallelism cho toán tử chậm bằng set_parallelism(), (2) dùng Async I/O cho các lời gọi tra cứu bên ngoài, và (3) tăng Block Cache / Write Buffer cho RocksDB. Khi lên Production, luôn chọn Application Mode (1 cụm độc lập cho mỗi Job) thay vì Session Mode để tránh rủi ro Noisy Neighbor.",
        "stream.map(heavy_fn).set_parallelism(8).start_new_chain()",
        "Trên Flink Web UI, toán tử đầu tiên báo Backpressure HIGH (hoặc toán tử đứng ngay sau chuỗi HIGH nhưng bản thân có Busy = 100% và Backpressured = 0%) chính là thủ phạm gây nghẽn gốc!"
    ),

    # =========================================================================
    # D06: ORCHESTRATION & GOVERNANCE (AIRFLOW, GX, DEEQU, DATA CONTRACTS, DATAHUB)
    # =========================================================================
    (
        "orchestration.pipeline-five-pillars",
        "Pipeline Orchestration, Dependency Graph, Automated Triggers, State Tracking, Failure Handling & Resource Coordination",
        "PIPELINE ORCHESTRATION",
        ["D06"],
        [
            "pipeline orchestration", "workflow orchestration", "naive scheduling",
            "dependency management", "state tracking", "failure handling",
            "resource coordination", "time-based trigger", "event-based trigger",
            "data availability trigger"
        ],
        "Pipeline Orchestration là hệ thần kinh trung ương điều phối thứ tự phụ thuộc, trạng thái thực thi, cơ chế thử lại khi lỗi và phân bổ hạn ngạch tài nguyên giữa các tác vụ dữ liệu, thay thế hoàn toàn cách lập lịch mù theo đồng hồ (Naive Time-Based Scheduling).",
        "Khác với bộ lập lịch theo giờ ngây thơ (chạy bước Transform đúng 03:00 AM bất chấp bước Extract thượng nguồn bị trễ tới 03:20 AM gây khuyết thiếu dữ liệu), một Orchestrator chỉ kích hoạt tác vụ khi toàn bộ các nút phụ thuộc thượng nguồn (`Upstream Dependencies`) đã báo trạng thái `SUCCESS`. Hệ thống cung cấp 5 trụ cột: quản lý phụ thuộc tuần tự/song song, kích hoạt đa phương thức (Time, Manual, Data Availability, Event), theo dõi máy trạng thái 6 nấc (`queued`, `running`, `success`, `failed`, `retrying`, `skipped`), cô lập lỗi tự động và điều tiết áp lực hạ tầng qua Pool.",
        "extract_orders >> clean_orders >> validate_orders >> load_warehouse >> refresh_dashboard",
        "Lập lịch (Scheduling) chỉ quyết định thời điểm khởi phát quy trình, còn Điều phối (Orchestration) kiểm soát toàn bộ sự sống còn và tính đúng đắn của quy trình sau khi nó đã bắt đầu."
    ),
    (
        "orchestration.idempotency-backfill-dynamic",
        "Idempotency (f(f(x)) = f(x)), Atomicity, Data Interval Backfill, Dynamic Task Mapping (.expand) & Asset-Aware Scheduling",
        "IDEMPOTENCY & BACKFILL",
        ["D06"],
        [
            "idempotency", "idempotent", "tính lũy đẳng", "atomicity", "tính nguyên tử",
            "backfill", "backfilling", "data interval", "data_interval_start", "data_interval_end",
            "logical_date", "catchup", "dynamic task mapping", "asset-aware scheduling"
        ],
        "Tính lũy đẳng (Idempotency) đảm bảo việc thực thi một tác vụ 1 lần hay N lần trên cùng một cửa sổ dữ liệu logic (Data Interval) đều tạo ra trạng thái đích hệt nhau, không bao giờ gây nhân đôi bản ghi khi Retry hoặc chạy bù lịch sử (Backfill).",
        "Để đạt tính nguyên tử (`Atomicity`) và lũy đẳng (`f(f(x)) = f(x)`), kỹ sư cấm dùng lệnh `INSERT` nối đuôi mù quáng kèm hàm `NOW()`, mà phải tham số hóa khung thời gian `[data_interval_start, data_interval_end)` kết hợp mẫu `DELETE-then-INSERT` trong một Transaction, `MERGE / ON CONFLICT DO UPDATE` theo khóa chính hoặc ghi đè phân vùng (`INSERT OVERWRITE PARTITION`). Khi cần co giãn linh hoạt lúc Runtime, Airflow cung cấp `Dynamic Task Mapping` (`.partial().expand()`) và lập lịch hướng sự kiện tài sản (`Asset-Aware Scheduling`) để kích hoạt DAG hạ nguồn ngay khi Dataset URI được cập nhật.",
        "airflow dags backfill --start-date 2026-05-01 --end-date 2026-05-15 daily_sales_pipeline",
        "Một đường ống chỉ có thể chạy Backfill an toàn cho 30 ngày lịch sử khi mọi tác vụ bên trong nó đều tuân thủ nghiêm ngặt tính lũy đẳng và không phụ thuộc vào đồng hồ hệ thống `datetime.now()`."
    ),
    (
        "orchestration.airflow-dag-architecture",
        "Apache Airflow Architecture: Directed Acyclic Graph (DAG), DAG Run, Task Instance, Scheduler, Metadata Database & Airflow 3.0 Execution API",
        "APACHE AIRFLOW ARCHITECTURE",
        ["D06"],
        [
            "apache airflow", "workflows as code", "directed acyclic graph", "dag",
            "dag run", "task instance", "metadata database", "dag processor",
            "task execution api", "airflow scheduler"
        ],
        "Apache Airflow hiện thực hóa triết lý Workflows as Code bằng đồ thị có hướng không chu trình (DAG), đóng vai trò nhạc trưởng điều phối thông qua 6 thành phần xoay quanh nguồn sự thật duy nhất là Metadata Database.",
        "Airflow phân biệt rõ bản thiết kế tĩnh (`DAG` và `Task`) với phiên thực thi động theo từng kỳ dữ liệu (`DAG Run` và `Task Instance`). Kiến trúc gồm `DAG Processor` (quét và tuần tự hóa tệp Python), `Scheduler` (kiểm tra phụ thuộc và xếp hàng tác vụ), `Executor` (cơ chế điều vận), `Workers` (thực thi mã lệnh), `Web/API Server` và `Metadata Database` (PostgreSQL/MySQL). Từ Airflow 3.0, các Worker không còn kết nối SQL trực tiếp vào Metadata DB mà giao tiếp qua `Task Execution API Server`, giúp tăng cường bảo mật cô lập và chịu tải quy mô lớn.",
        "airflow dags test daily_sales_pipeline 2026-05-15",
        "Airflow là bộ điều phối (Coordinator), KHÔNG phải công cụ xử lý dữ liệu lớn: tuyệt đối không nạp DataFrame hàng chục GB vào RAM của Airflow Worker mà phải ủy quyền cho Spark, dbt hoặc SQL Warehouse."
    ),
    (
        "orchestration.operators-sensors-xcom",
        "Airflow Operators, Deferrable Sensors (Asyncio Triggerer vs. Poke Deadlock) & Cross-Communication (XCom Pass-by-URI)",
        "OPERATORS, SENSORS & XCOM",
        ["D06"],
        [
            "pythonoperator", "bashoperator", "dockeroperator", "kubernetespodoperator",
            "s3keysensor", "externalsensor", "deferrable operator", "triggerer",
            "sensor deadlock", "xcom", "xcom_push", "xcom_pull", "taskflow api"
        ],
        "Operators định nghĩa hành động của từng nút trên DAG, Sensors chờ điều kiện ngoại vi hoàn tất (qua chế độ Poke, Reschedule hoặc bất đồng bộ Deferrable Triggerer), còn XCom truyền siêu dữ liệu phối hợp gọn nhẹ giữa các tác vụ cô lập.",
        "Khi dùng Sensor ở chế độ mặc định `mode='poke'`, tiến trình vẫn chiếm giữ khư khư Worker Slot trong lúc ngủ chờ, dễ gây kẹt cứng toàn cụm (`Sensor Deadlock`); chuyển sang `mode='reschedule'` hoặc `deferrable=True` (ủy quyền cho tiến trình `asyncio Triggerer`) giúp giải phóng 100% Worker Slot. Vì mỗi Task Instance có thể chạy trên một máy chủ/Pod khác nhau, Airflow cung cấp `XCom` (`xcom_push`/`xcom_pull` lưu tại bảng `xcom` trong Metadata DB) để trao đổi thông tin nhỏ như đường dẫn tệp S3 (`Pass-by-Reference URI`), tuyệt đối cấm đẩy dữ liệu thô dung lượng lớn qua XCom.",
        "S3KeySensor(task_id='wait_orders', bucket_key='s3://lake/orders/{{ ds }}.parquet', deferrable=True)",
        "Truyền trực tiếp Pandas DataFrame qua XCom mặc định sẽ làm phình nổ bảng `xcom` trong PostgreSQL/MySQL và đánh sập bộ nhớ của cả Scheduler lẫn Web UI."
    ),
    (
        "orchestration.executors-concurrency-pools",
        "Airflow Production Operations: Variables & Fernet Connections, Executors (Local/Celery/Kubernetes) & Three-Tier Concurrency Funnel (Pools)",
        "EXECUTORS & CONCURRENCY",
        ["D06"],
        [
            "fernet key", "secrets backend", "localexecutor", "celeryexecutor",
            "kubernetesexecutor", "max_active_runs", "max_active_tasks",
            "airflow pool", "resource pool", "concurrency control"
        ],
        "Vận hành Airflow cấp độ Production đòi hỏi tách biệt mật khẩu khỏi mã nguồn qua Connections mã hóa Fernet/Vault, chọn đúng Executor (Local, Celery, Kubernetes) và siết van đồng thời 3 tầng để bảo vệ các hệ thống cơ sở dữ liệu dùng chung.",
        "Thông số cấu hình được lưu trong `Variables` (truy xuất qua Jinja `{{ var.value.* }}` lúc chạy để tránh bắn truy vấn SQL lúc quét DAG), còn thông tin nhạy cảm lưu trong `Connections` mã hóa bằng `Fernet Key` hoặc `Secrets Backend`. Về hạ tầng thực thi, `CeleryExecutor` tối ưu cho tác vụ ngắn tần suất cao qua hàng đợi Redis/RabbitMQ, trong khi `KubernetesExecutor` cấp phát 1 Pod cô lập cho mỗi Task Instance. Phễu đồng thời 3 tầng gồm: `core.parallelism` (toàn cụm), `max_active_runs` (chống chồng lấn các phiên chạy của cùng 1 DAG) và `Pools` (giới hạn số kết nối đồng thời tới một Database cụ thể như `postgres_pool = 5 slots`).",
        "airflow pools set postgres_pool 5 'Throttle concurrent OLTP extraction queries'",
        "Gọi `Variable.get()` trực tiếp ở cấp độ toàn cục (top-level) của tệp Python DAG sẽ khiến DAG Processor dội hàng nghìn câu lệnh SQL vào Metadata Database mỗi phút ngay cả khi không có tác vụ nào đang chạy!"
    ),
    (
        "orchestration.circuit-breaker-contracts-datahub",
        "Data Quality Six Dimensions, Circuit Breaker Pattern, Machine-Readable Data Contracts, Great Expectations (GX), Spark Deequ & DataHub Lineage",
        "QUALITY, CONTRACTS & DATAHUB",
        ["D06"],
        [
            "six data quality dimensions", "data quality dimensions", "circuit breaker",
            "circuit breaker pattern", "branchpythonoperator", "shortcircuitoperator",
            "data contract", "data contracts", "great expectations", "expectation suite",
            "deequ", "pydeequ", "datahub", "openlineage", "data lineage"
        ],
        "Kiến trúc tin cậy dữ liệu hiện đại kết hợp 6 chiều chất lượng, mẫu Cầu dao tự ngắt (Circuit Breaker) bằng GX/Deequ ngay trong Airflow, Hợp đồng dữ liệu (Data Contracts) ở thượng nguồn và đồ thị phả hệ toàn cục trên DataHub.",
        "Một đường ống có thể báo trạng thái `SUCCESS` (Exit Code 0) nhưng vẫn phát tán dữ liệu rác gây thiệt hại triệu đô. Để phòng vệ đa lớp: (1) Đội ngũ Producer và Consumer ký kết `Data Contract` máy đọc được (khóa chặt `Schema`, `Nullability`, `Value Range`, `Freshness`, `Uniqueness`); (2) Trong Airflow DAG, tác vụ kiểm định (`Great Expectations` cho tập quy tắc đa nền tảng hoặc `Apache Spark Deequ` hỗ trợ tính toán lũy tiến và phát hiện bất thường trên hàng tỷ dòng) kết hợp `BranchPythonOperator` tạo thành `Circuit Breaker` tự động ngắt nhánh Load khi phát hiện lỗi; (3) Mọi siêu dữ liệu, hợp đồng và phả hệ (`OpenLineage`, `MCP/MCL`) hội tụ về `DataHub` để khoanh vùng bán kính ảnh hưởng (`Blast Radius`) tức thì.",
        "datahub dataset upsert -f contracts/prod_orders_contract.yaml",
        "Kiểm định chất lượng (Validation) cho chúng ta biết chính xác CÁI GÌ bị lỗi, còn Phả hệ dữ liệu (DataHub Lineage) cho biết ngay lập tức AI và BÁO CÁO NÀO ở hạ nguồn đang bị ảnh hưởng."
    ),
    # =========================================================================
    # D03: TRANSFORMATION LAYER I (BATCH · APACHE SPARK) — CHẶNG 1 ĐẾN CHẶNG 6
    # =========================================================================
    (
        "spark.dag_scheduler",
        "Apache Spark Cluster Architecture (Driver, Cluster Manager, Executors), Lazy Evaluation & DAG Execution Hierarchy (Job → Stage → Task)",
        "SPARK ARCHITECTURE & DAG",
        ["D03"],
        [
            "apache spark", "spark", "sparksession", "sparkcontext", "dagscheduler",
            "taskscheduler", "executor", "executors", "lazy evaluation", "dag",
            "narrow transformation", "wide transformation", "shuffle boundary",
            "stage", "stages", "mapreduce", "hadoop mapreduce"
        ],
        "Apache Spark thay thế mô hình đọc/ghi đĩa cứng lặp lại sau mỗi bước của Hadoop MapReduce bằng đồ thị thực thi có hướng không chu trình (In-Memory DAG): Driver đóng vai trò bộ não lập lịch, Cluster Manager cấp phát tài nguyên, còn các Executors bên trong Worker Nodes trực tiếp chạy Tasks trên các Partitions và giữ dữ liệu trong RAM.",
        "Khi người dùng viết các phép biến đổi (Transformations như filter, select, join, groupBy), cơ chế Lazy Evaluation chưa thực thi ngay mà chỉ ghi nhận vào Logical Plan. Chỉ khi gặp một Action (show, count, write, collect), Driver mới kích hoạt Job: DAGScheduler cắt đồ thị thành các Stages tại ranh giới Wide Transformation (nơi cần Shuffle dữ liệu qua mạng), và TaskScheduler gửi từng Task (1 Task = 1 Partition = 1 luồng CPU) xuống các Executors thực thi song song.",
        "df.filter(col('status') == 'PAID').groupBy('store_id').agg(sum('amount')).write.mode('overwrite').parquet('s3a://gold/revenue/')",
        "Một Worker Node vật lý không chạy trực tiếp toàn bộ chương trình Spark của bạn — nó chỉ chứa các tiến trình Executor JVM, và chính Executors mới là nơi thực thi Tasks và lưu In-Memory Cache!"
    ),
    (
        "spark.rdd_dataframe",
        "Spark Data Abstractions: RDD (Resilient Distributed Dataset & Lineage Graph) vs. DataFrame (Immutable Schema Table) vs. Dataset[T]",
        "SPARK APIS & ABSTRACTIONS",
        ["D03"],
        [
            "rdd", "resilient distributed dataset", "spark rdd", "lineage", "lineage graph",
            "parallelize", "dataframe", "spark dataframe", "dataset[t]", "structtype",
            "structfield", "inferschema", "todf", "createdataframe", "python worker"
        ],
        "RDD là tập hợp các phân vùng dữ liệu phân tán cấp thấp tự phục hồi khi sập máy nhờ đồ thị huyết thống (Lineage Graph), còn DataFrame là bảng dữ liệu bất biến (Immutable) có lược đồ (Schema) tường minh chạy hoàn toàn trong JVM với bộ tối ưu Catalyst và Tungsten.",
        "Trên PySpark, việc gọi hàm lambda trên Python RDD buộc Executor JVM phải tuần tự hóa dữ liệu qua Socket sang tiến trình con Python Worker (gây nghẽn cổ chai IPC kép). Ngược lại, mọi phép biến đổi trên DataFrame (select, filter, join, groupBy) được biểu diễn dưới dạng biểu thức cột có Schema, cho phép Spark biên dịch trực tiếp thành mã máy JVM mà không cần bật Python subprocess, đồng thời giữ tính bất biến (mỗi phép biến đổi sinh ra một DataFrame mới).",
        "df = spark.read.schema(order_schema).parquet('s3a://silver/orders/')",
        "Trên Production, tuyệt đối tránh bật inferSchema=True khi đọc CSV/JSON lớn vì Spark sẽ phải chạy thêm 1 Job quét toàn bộ dữ liệu chỉ để đoán kiểu cột — hãy truyền StructType tường minh!"
    ),
    (
        "spark.kryo_serialization",
        "Spark Serialization & Deserialization (Shuffle, Cache, Network) & Java Serialization vs. KryoSerializer",
        "SERIALIZATION & MEMORY",
        ["D03"],
        [
            "kryo", "kryo serialization", "kryoserializer", "java serialization",
            "classestoregister", "spark.serializer", "deserialization"
        ],
        "Serialization biến đối tượng trong RAM thành dòng byte (Byte Stream) tại 3 điểm nóng của Spark (Shuffle qua mạng, lưu Cache/Persist, và gửi Task/Broadcast), trong đó KryoSerializer nén gọn dòng byte nhỏ hơn và nhanh hơn tới 10 lần so với Java Serialization mặc định.",
        "Java Serialization mặc định viết kèm toàn bộ thông tin phả hệ lớp (Class Metadata) nên tạo ra luồng byte phình to, làm nghẽn băng thông mạng lúc Shuffle và tốn CPU giải mã. Khi cấu hình spark.serializer = org.apache.spark.serializer.KryoSerializer và đăng ký trước các lớp tùy chỉnh qua spark.kryo.classesToRegister, Spark thay thế tên lớp đầy đủ bằng mã định danh số nguyên ngắn gọn, giảm mạnh áp lực RAM, Disk Spill và GC.",
        "SparkSession.builder.config('spark.serializer', 'org.apache.spark.serializer.KryoSerializer').config('spark.kryo.classesToRegister', 'com.fsds.OrderRecord')",
        "Luôn cấu hình KryoSerializer và đăng ký các class dữ liệu ngay khi khởi tạo SparkSession cho mọi tác vụ RDD hoặc Shuffle quy mô lớn."
    ),
    (
        "spark.unified_memory",
        "In-Memory Computing, cache() vs. persist(), Five Storage Levels (MEMORY_ONLY..DISK_ONLY) & Unified Memory Manager",
        "SERIALIZATION & MEMORY",
        ["D03"],
        [
            "in-memory computing", "cache()", "persist()", "unpersist()", "storagelevel",
            "memory_only", "memory_and_disk", "memory_only_ser", "memory_and_disk_ser",
            "disk_only", "unified memory", "unified memory manager", "execution memory",
            "storage memory"
        ],
        "In-Memory Computing giúp đọc dữ liệu từ đĩa đúng 1 lần rồi giữ trong RAM qua cache()/persist() để tái sử dụng cho nhiều Actions nối tiếp, được điều phối bởi Unified Memory Manager với ranh giới co giãn động giữa Storage Memory và Execution Memory.",
        "Trong Spark, cache() là lối tắt của persist() với mức mặc định khác nhau: trên RDD là MEMORY_ONLY, còn trên DataFrame là MEMORY_AND_DISK. Năm chế độ lưu trữ chuẩn gồm: MEMORY_ONLY (nhanh nhất nhưng tràn RAM phải tính toán lại theo Lineage), MEMORY_AND_DISK (tràn RAM thì ghi phần dư xuống đĩa cục bộ), MEMORY_ONLY_SER và MEMORY_AND_DISK_SER (lưu dạng byte tuần tự hóa giúp tiết kiệm RAM nhưng tốn CPU giải mã), và DISK_ONLY. Bên trong Executor JVM, vùng Unified Memory (mặc định 60% Heap) chia đôi cho Storage và Execution: Execution Memory (Shuffle/Join/Sort) có quyền mượn vùng trống của Storage và trục xuất (evict) các khối Cache vượt ngưỡng 50% xuống đĩa, nhưng Storage không bao giờ được phép trục xuất Execution đang chạy.",
        "df_enriched.persist(StorageLevel.MEMORY_AND_DISK); df_enriched.count(); df_enriched.unpersist()",
        "Chỉ gọi cache()/persist() khi một DataFrame được dùng lại từ 2 Actions trở lên (hoặc vòng lặp ML), và bắt buộc gọi unpersist() ngay khi dùng xong để trả lại RAM cho cụm!"
    ),
    (
        "spark.catalyst",
        "Catalyst Optimizer: Logical-to-Physical Plan Rewriting, Constant Folding, Predicate Pushdown & Column Pruning",
        "SPARK BUILT-IN OPTIMIZERS",
        ["D03"],
        [
            "catalyst", "catalyst optimizer", "predicate pushdown", "constant folding",
            "column pruning", "logical plan", "physical plan", "cost-based optimizer"
        ],
        "Catalyst Optimizer là 'bộ não lập kế hoạch' của Spark SQL/DataFrame, tự động phân tích và viết lại cây truy vấn (đẩy bộ lọc WHERE xuống sát tầng đọc đĩa trước khi chạy JOIN và gộp hằng số) trước khi sinh mã thực thi.",
        "Một câu truy vấn DataFrame/SQL đi qua 4 pha trong Catalyst: (1) Analysis (đối chiếu tên cột/bảng với Catalog), (2) Logical Optimization (áp dụng các quy tắc đại số quan hệ như Constant Folding gộp `1 + 2 -> 3`, Predicate Pushdown đẩy bộ lọc `t2.id > 50000` xuống trước phép Join để loại bỏ 95% dòng rác sớm, và Column Pruning cắt bỏ các cột không dùng), (3) Physical Planning (chọn toán tử vật lý rẻ nhất qua Cost Model), và (4) CodeGen.",
        "df.explain(mode='formatted')   # Kiểm tra PushedFilters và ReadSchema trong kế hoạch vật lý",
        "Nếu viết UDF hộp đen bằng Python hoặc ép kiểu làm hỏng cấu trúc cột, Catalyst có thể không đẩy được bộ lọc (PushedFilters trống rỗng) khiến Spark phải đọc toàn bộ bảng!"
    ),
    (
        "spark.tungsten",
        "Project Tungsten: Off-Heap Binary Memory (UnsafeRow), L1/L2/L3 Cache-Aware Computation & Whole-Stage Code Generation",
        "SPARK BUILT-IN OPTIMIZERS",
        ["D03"],
        [
            "tungsten", "project tungsten", "unsaferow", "off-heap", "off-heap memory",
            "whole-stage code generation", "wholesstagecodegen", "cache-aware computation"
        ],
        "Nếu Catalyst quyết định 'làm cái gì' (kế hoạch tối ưu), thì Project Tungsten quyết định 'làm như thế nào' ở tầng phần cứng thông qua 3 kỹ thuật: quản lý bộ nhớ nhị phân Off-Heap, tính toán bám sát bộ đệm L1/L2/L3 Cache của CPU (~1 ns) và hợp nhất toàn bộ Stage thành một hàm mã máy duy nhất.",
        "Ba trụ cột kỹ thuật của Tungsten: (1) Off-Heap Memory Management lưu bản ghi dưới dạng mảng nhị phân liền kề (UnsafeRow) ngoài tầm quét của JVM Garbage Collector, xóa sổ hiện tượng Stop-the-World GC Pause; (2) Cache-Aware Computation sắp xếp con trỏ và khóa sắp xếp tuần tự trên các dòng đệm L1/L2/L3 Cache (~1 ns thay vì ~100 ns trên RAM, nhanh gấp 100 lần); (3) Whole-Stage Code Generation gộp chuỗi toán tử (Scan -> Filter -> Project -> Aggregate) thành một vòng lặp bytecode Java phẳng duy nhất thay vì gọi hàm ảo qua từng toán tử.",
        "spark.conf.set('spark.sql.codegen.wholeStage', 'true')",
        "Trên Spark UI (tab SQL/DataFrame), các khối có dấu hoa thị `*(1) Filter -> Project -> HashAggregate` chính là dấu hiệu Whole-Stage Code Generation của Tungsten đang hoạt động!"
    ),
    (
        "spark.aqe",
        "Adaptive Query Execution (AQE): Runtime Shuffle Statistics, Dynamic Switch Join Strategy, Coalesce Partitions & Skew Join Splitting",
        "SPARK BUILT-IN OPTIMIZERS",
        ["D03"],
        [
            "aqe", "adaptive query execution", "coalesce shuffle partitions",
            "skewed join", "autoskip", "autobroadcastjointhreshold"
        ],
        "Adaptive Query Execution (AQE) khắc phục điểm mù ước lượng tĩnh trước khi chạy bằng cách thu thập thống kê thực tế (số dòng, số byte) ngay tại các trạm dừng Shuffle Stage để tự động viết lại kế hoạch cho các Stages còn lại.",
        "Nhờ nhìn thấy kích thước dữ liệu thật sau khi lọc và Shuffle, AQE thực hiện 3 phép hiệu chỉnh động lúc Runtime: (1) Switch Join Strategy — tự động chuyển Sort-Merge Join đắt đỏ sang Broadcast Hash Join nếu một nhánh sau khi lọc nhỏ hơn ngưỡng phát sóng; (2) Coalesce Shuffle Partitions — tự động gộp hàng trăm phân vùng nhỏ sau Shuffle thành số lượng phân vùng vừa vặn (~128MB); và (3) Handle Skewed Joins — phát hiện phân vùng bị phình dị thường và tự động chẻ nhỏ thành nhiều sub-tasks chạy song song.",
        "spark.conf.set('spark.sql.adaptive.enabled', 'true'); spark.conf.set('spark.sql.adaptive.skewJoin.enabled', 'true')",
        "AQE được bật mặc định từ Spark 3.2+, nhưng nó chỉ có thể can thiệp sau khi đã có ít nhất một bước Shuffle hoặc Broadcast Query Stage hoàn tất."
    ),
    (
        "spark.key_salting",
        "Batch Processing Challenges (Data Skew, Shuffle Explosion, High Cardinality, Wide Schema) & Key Salting / HyperLogLog Tuning",
        "PERFORMANCE TUNING",
        ["D03"],
        [
            "data skew", "shuffle explosion", "high cardinality", "wide schema",
            "key salting", "salting", "straggler", "straggler task", "approx_count_distinct",
            "hyperloglog", "disk spill"
        ],
        "Khi một khóa nóng như VIP123 chiếm 80% dữ liệu (Data Skew) làm 1 Task chạy ì ạch kéo tụt cả cụm trong khi 99 Tasks khác ngồi chơi, kỹ thuật Key Salting gắn thêm hậu tố ngẫu nhiên (VIP123_1..N) để băm nhỏ khóa nóng ra nhiều Executors xử lý song song.",
        "Năm thách thức lớn của xử lý lô gồm: Data Skew (lệch phân vùng), Shuffle Explosion (100GB đầu vào phình thành 600GB dữ liệu mạng gây Disk Spill), High Cardinality (hàng triệu khóa duy nhất làm nổ bảng băm), Wide Schema (bảng 1.000 cột nhưng chỉ dùng 5 cột), và Schema Evolution. Để trị Data Skew trong phép gom nhóm hoặc Join lớn, kỹ sư áp dụng Two-Phase Key Salting (tạo cột salt ngẫu nhiên từ 0..K-1, gom nhóm bước 1 theo `(key, salt)`, sau đó bỏ salt gom bước 2 theo `key`), đồng thời dùng `approx_count_distinct()` (thuật toán HyperLogLog sai số ~1-2%) cho cột High Cardinality và cắt tỉa cột sớm (Project Early) cho bảng Wide Schema.",
        "df_salted = df.withColumn('salted_key', concat(col('user_id'), lit('_'), floor(rand() * 8)))",
        "Nếu dùng Key Salting cho phép Join, khi gắn muối ngẫu nhiên `0..K-1` vào bảng lớn (Fact), bắt buộc phải nhân bản (explode) các dòng tương ứng ở bảng nhỏ (Dimension) đủ `K` lần để không bị rớt kết nối!"
    ),
    (
        "spark.broadcast_join",
        "Spark Join Strategies: Broadcast Hash Join (BHJ — Zero Shuffle) vs. Sort-Merge Join (SMJ) vs. Bucketed Join",
        "PERFORMANCE TUNING",
        ["D03"],
        [
            "broadcast hash join", "broadcast join", "sort-merge join", "sort merge join",
            "bhj", "smj", "bucketed join", "bucketby"
        ],
        "Sort-Merge Join buộc phải xáo trộn (Shuffle) và sắp xếp cả hai bảng qua mạng, trong khi Broadcast Hash Join gửi bản sao của bảng nhỏ (< 10MB–100MB) tới RAM của mọi Executor để bảng lớn 500GB ghép nối tại chỗ với 0% Shuffle.",
        "Khi ghép một bảng sự kiện khổng lồ (Fact) với một bảng danh mục nhỏ (Dimension), nếu dùng `broadcast(dim_df)`, Driver sẽ thu thập bảng nhỏ và phát sóng (Broadcast) tới từng Executor một lần duy nhất; mỗi Task chỉ việc tra bảng băm trong RAM mà không cần đẩy bất kỳ dòng nào của bảng Fact qua mạng. Nếu cả hai bảng đều quá lớn không vừa RAM, Spark dùng Sort-Merge Join (băm khóa Shuffle 2 bảng về cùng Partition rồi trộn), hoặc có thể tiền phân loại trên đĩa bằng Bucketing (`bucketBy(N, 'key')`) để loại bỏ bước Shuffle lặp lại.",
        "df_joined = orders_df.join(broadcast(stores_df), on='store_id', how='inner')",
        "Tuyệt đối không ép `broadcast()` lên bảng lớn vượt quá bộ nhớ của Driver hoặc Executor vì toàn bộ bảng đó phải đi qua RAM của Driver trước khi phát sóng, rất dễ gây sập Driver OOM!"
    ),
    (
        "spark.dynamic_allocation",
        "Spark Operational Techniques: Spark UI Diagnostics, Dynamic Resource Allocation (Backlog & Idle Timeouts) & External Shuffle Service",
        "SPARK OPERATIONS",
        ["D03"],
        [
            "spark ui", "spark web ui", "dynamic allocation", "schedulerbacklogtimeout",
            "executoridletimeout", "external shuffle service"
        ],
        "Spark UI là bảng đồng hồ chẩn đoán thời gian thực (Stages, Tasks, Shuffle Read/Write, Spill, GC), còn Dynamic Allocation tự động co giãn số lượng Executors (ví dụ từ 2 lên 10 rồi hạ về 1) theo hàng đợi Task thực tế để tránh lãng phí tài nguyên cụm.",
        "Cấp phát cố định 20 Executors cho một Job chỉ cần 5 Executors làm lãng phí 15 máy chủ. Khi bật `spark.dynamicAllocation.enabled = true`, Spark khởi đầu với số Executors tối thiểu; nếu có Tasks phải chờ trong hàng đợi lâu hơn `spark.dynamicAllocation.schedulerBacklogTimeout` (mặc định 1s), Spark xin thêm Executors theo cấp số nhân; khi một Executor ngồi rảnh lâu hơn `spark.dynamicAllocation.executorIdleTimeout` (mặc định 60s), Spark trả nó về cho Cluster Manager (đi kèm External Shuffle Service để bảo toàn các file Shuffle đã ghi trên đĩa).",
        "spark.conf.set('spark.dynamicAllocation.enabled', 'true'); spark.conf.set('spark.dynamicAllocation.executorIdleTimeout', '60s')",
        "Dấu hiệu kinh điển của Data Skew trên Spark UI: tiến độ Stage dừng ở `199/200 Tasks` suốt hàng chục phút và trong bảng Summary Metrics, cột `Max` lớn gấp hàng chục lần cột `Median (50th percentile)`!"
    ),
    (
        "spark.data_compaction",
        "Small File Problem (Triệu File Nhỏ) & Data Compaction Strategies: coalesce(n) vs. repartition(n) vs. Lakehouse OPTIMIZE",
        "SPARK OPERATIONS",
        ["D03"],
        [
            "data compaction", "small file problem", "coalesce", "coalesce(n)",
            "repartition", "repartition(n)", "maxrecordsperfile"
        ],
        "Một tập dữ liệu 1 TB nếu bị băm vụn thành 1.000.000 file nhỏ (~1 MB/file) sẽ làm tê liệt tầng lưu trữ vì chi phí mở file và đọc Metadata; Data Compaction gộp chúng thành 200 file lớn chuẩn (~128–512 MB/file) bằng coalesce(n), repartition(n) hoặc lệnh OPTIMIZE.",
        "Ba công cụ nén gộp file có cơ chế vật lý hoàn toàn khác nhau: (1) `coalesce(n)` chỉ giảm số lượng Partition bằng cách gộp các phân vùng ngay trên cùng Executor với 0% Shuffle qua mạng (cực nhanh nhưng kích thước file đầu ra có thể không đều nếu dữ liệu gốc bị lệch); (2) `repartition(n)` thực hiện Full Shuffle qua mạng để chia lại dữ liệu đều tăm tắp ra đúng `n` file có dung lượng bằng nhau; và (3) `OPTIMIZE` trên Delta Lake / Apache Iceberg chạy tác vụ Bin-packing ngầm gộp các file Parquet nhỏ thành file lớn mà không làm gián đoạn luồng đọc.",
        "df_gold.coalesce(200).write.mode('overwrite').parquet('s3a://gold/daily_revenue/')",
        "Dùng `coalesce(n)` sau khi đã lọc (Filter) làm giảm mạnh dung lượng dữ liệu để tránh tốn mạng Shuffle; dùng `repartition(n, 'date')` khi cần chia lại các file đầu ra đồng đều theo cột phân vùng!"
    ),
    # =========================================================================
    # F02: PYTHON FUNDAMENTALS — CHẶNG 1..4 (CPYTHON, UV, HASH O(1), ASYNCIO)
    # =========================================================================
    (
        "python.cpython-pyobject-gc",
        "CPython Runtime, PyObject (28 Bytes Header: ob_refcnt + ob_type) & Garbage Collection (Reference Counting + Cyclic GC)",
        "PYTHON RUNTIME & MEMORY",
        ["F02"],
        [
            "cpython", "cpython runtime", "pyobject", "ob_refcnt", "ob_type",
            "reference counting", "cyclic gc", "cyclic garbage collector",
            "generational gc", "bytecode", "cpython vm"
        ],
        "Trong CPython, mọi giá trị đều là một cấu trúc PyObject trên Heap mang theo bộ đếm tham chiếu ob_refcnt và con trỏ kiểu ob_type (tốn tối thiểu 28 bytes cho một số nguyên int), tự động giải phóng bộ nhớ ngay khi ob_refcnt về 0.",
        "Khác với C phải gọi `malloc()` và `free()` thủ công dễ gây Memory Leak, CPython biên dịch mã nguồn `.py` thành Bytecode (`.pyc`) chạy trên máy ảo ngăn xếp và quản lý bộ nhớ qua 2 tầng: (1) Reference Counting tức thì (`a = [1, 2]; b = a` tăng `ob_refcnt` lên 2; khi `ob_refcnt == 0` giải phóng ngay lập tức), và (2) Cyclic Garbage Collector (Generational GC 3 thế hệ Gen 0, 1, 2) định kỳ quét và phá vỡ các vòng tham chiếu khép kín (`a <-> b`).",
        "import sys; x = 1000; print(sys.getsizeof(x), sys.getrefcount(x))  # -> 28 bytes",
        "Vì mỗi PyObject có chi phí Header >= 28 bytes, khi xử lý hàng chục triệu con số trong Data/AI, kỹ sư không dùng vòng lặp `list` thuần mà ủy quyền xuống mảng C/Rust liên tục của NumPy, Pandas, Polars hoặc PyTorch."
    ),
    (
        "python.venv-poetry-uv",
        "Dependency Hell & Ba Thế hệ Môi trường Ảo Python: venv / virtualenv (4.63s) vs. Poetry (0.99s) vs. uv (Rust + Hardlink Cache · 0.06s)",
        "PYTHON PACKAGING & ENV",
        ["F02"],
        [
            "dependency hell", "site-packages", "virtual environment", "virtualenv",
            "venv", "poetry", "pyproject.toml", "poetry.lock", "uv.lock",
            "pubgrub", "pip-sync", "astral uv"
        ],
        "Môi trường ảo (.venv) cô lập biến PATH và mảng tìm kiếm sys.path cho từng dự án để tránh xung đột thư viện trên Global site-packages; trong đó uv (viết bằng Rust) kết hợp trình giải PubGrub và Global Hardlink Cache giúp đồng bộ gói chỉ trong 0.06 giây.",
        "Cài đặt gói trực tiếp bằng `pip` vào thư mục hệ thống chỉ giữ được 1 phiên bản duy nhất cho mỗi tên gói (ví dụ `serpapi==1.1.15` đè mất `1.0.5` và `1.0.8`), gây sập dây chuyền (Dependency Hell). Thế hệ 1 (`venv`/`virtualenv` + `requirements.txt`) cô lập thư mục `.venv` nhưng copy file chậm (`4.63s`); Thế hệ 2 (`Poetry`) chuẩn hóa `pyproject.toml` và khóa cây phụ thuộc `poetry.lock` (`0.99s`); Thế hệ 3 (`uv`) dùng Rust và liên kết cứng (Hardlinks / Reflinks) từ bộ đệm toàn cục `~/.cache/uv` đạt tốc độ `0.06s` (nhanh gấp 77 lần `pip-sync`).",
        "uv init market-crawler && uv venv && uv add requests httpx",
        "Trên Production và CI/CD, luôn commit cả tệp `pyproject.toml` lẫn tệp khóa `uv.lock` (hoặc `poetry.lock`) để đảm bảo mọi máy chủ cài đặt chính xác 100% mã băm SHA-256 của từng thư viện."
    ),
    (
        "python.name-binding-mutability",
        "Mô hình Biến Tham chiếu (Name Binding), Định danh (is vs. ==) & Ranh giới Mutable vs. Immutable (Hashability)",
        "PYTHON DATA MODEL",
        ["F02"],
        [
            "name binding", "object identity", "value equality", "mutable",
            "immutable", "hashable", "hashability", "aliasing", "type hints"
        ],
        "Biến trong Python không phải là chiếc hộp cố định địa chỉ như C mà là nhãn tên (Reference) gắn vào đối tượng trên Heap; toán tử 'is' so sánh địa chỉ con trỏ RAM O(1), còn '==' gọi __eq__() so sánh giá trị nội dung.",
        "Các kiểu Bất biến (Immutable: `int`, `float`, `str`, `tuple`) không thể sửa tại chỗ nên có giá trị băm `hash()` cố định (Hashable), dùng làm khóa cho `dict` hoặc phần tử của `set`. Ngược lại, các kiểu Khả biến (Mutable: `list`, `dict`, `set`) cho phép sửa trực tiếp nội dung tại chỗ (in-place), gây hiệu ứng phụ Aliasing nếu nhiều nhãn cùng trỏ vào một đối tượng và không thể làm khóa bảng băm (`TypeError: unhashable type`).",
        "def add_item(item: str, bucket: list | None = None) -> list:\\n    if bucket is None:\\n        bucket = []\\n    bucket.append(item)\\n    return bucket",
        "Cạm bẫy kinh điển: tuyệt đối không viết `def parse(urls, seen=[])` vì danh sách mặc định `[]` chỉ được khởi tạo đúng 1 lần khi nạp hàm (`def`) và sẽ giữ lại dữ liệu rác xuyên suốt mọi lần gọi hàm sau đó!"
    ),
    (
        "python.hash-table-complexity",
        "Bộ tứ Cấu trúc Dữ liệu Cốt lõi: Mảng Con trỏ Động (list O(n) / tuple) vs. Bảng Băm Thu gọn (dict / set O(1))",
        "PYTHON DATA STRUCTURES",
        ["F02"],
        [
            "compact hash table", "dynamic array", "hash table", "time complexity",
            "list comprehension", "dict comprehension"
        ],
        "Dưới nắp máy CPython, list là mảng động chứa các con trỏ tốn O(n) khi quét tìm kiếm (x in list), trong khi dict và set vận hành bằng Bảng băm thu gọn (Compact Hash Table) giúp tra cứu, khử trùng và xóa phần tử trong thời gian hằng số O(1).",
        "Khi kiểm tra 100.000 URL có nằm trong tập đã thu thập hay không (`url in visited`), nếu dùng `list`, CPython phải duyệt tuần tự từng phần tử tốn `O(n)` (tổng cộng `10^10` phép so sánh cho 100k lượt, làm treo CPU hàng chục giây). Khi chuyển sang `set` hoặc `dict`, CPython tính `hash(url)` (64-bit) và nhảy thẳng tới ô nhớ trong `O(1)` (~12 mili-giây). `tuple` là mảng con trỏ bất biến, nhẹ hơn `list` và dùng làm bản ghi cố định hoặc khóa ghép `(domain, path)` cho `dict`.",
        "visited_urls: set[str] = set()  # Tra cứu 'url in visited_urls' đạt chuẩn O(1)",
        "Quy tắc vàng trong Data Engineering: luôn chuyển tập danh sách cần tra cứu lặp lại (`in`) từ `list` sang `set` hoặc `dict` trước khi bước vào vòng lặp lớn!"
    ),
    (
        "python.context-manager-argparse",
        "Giao thức Context Manager (with → __enter__ / __exit__), Streaming File I/O & Chuẩn hóa CLI với argparse",
        "PYTHON I/O & PRODUCTION CLI",
        ["F02"],
        [
            "context manager", "context managers", "stack unwinding", "specific exceptions",
            "valueerror", "typeerror", "keyerror", "fileExistsError", "filenotfounderror",
            "errno 24", "too many open files", "readlines", "readline", "argparse",
            "argumentparser", "pathlib", "logging"
        ],
        "Khối lệnh 'with' thực thi giao thức Context Manager (__enter__ và __exit__) cam kết luôn đóng File Descriptor, Socket hoặc DB Session ngay cả khi văng ngoại lệ giữa chừng, chặn đứng lỗi cạn kiệt tài nguyên OS (Errno 24: Too many open files).",
        "Ba trụ cột vận hành tệp và CLI chuẩn Production: (1) Bắt đúng ngoại lệ cụ thể (`ValueError`, `KeyError`, `TimeoutError`) thay vì `except Exception:` nuốt lỗi âm thầm; (2) Bọc tệp trong `with open(path, 'a', encoding='utf-8') as f:` và duyệt từng dòng bằng Streaming Iterator (`for line in f:`) tốn `O(1)` RAM thay vì gọi `f.read()` / `f.readlines()` nạp toàn bộ tệp 10GB gây tràn bộ nhớ (OOM); và (3) Dùng `argparse` (`ArgumentParser`: Create → Add → Parse) kết hợp `logging` và `pathlib` để tham số hóa script trên CI/CD & Airflow.",
        "with open('events.jsonl', mode='a', encoding='utf-8') as f:\\n    f.write(json.dumps(record) + '\\n')",
        "Khi đọc tệp dữ liệu lớn hàng chục GB, tuyệt đối không gọi `f.read()` hay `f.readlines()`; hãy lặp trực tiếp `for line in f:` để tận dụng bộ đệm luồng lười (Lazy Streaming Iterator)!"
    ),
    (
        "python.asyncio-wsgi-asgi",
        "Lập trình Đồng bộ (Sync Blocking) vs. Bất đồng bộ (asyncio Event Loop, async/await, epoll/kqueue) & Hệ sinh thái WSGI vs. ASGI",
        "ASYNCIO & WEB FRAMEWORKS",
        ["F02"],
        [
            "asyncio", "event loop", "async def", "await", "asyncio.gather",
            "asyncio.run", "coroutine", "coroutines", "non-blocking i/o", "blocking i/o",
            "judit polgar", "wsgi", "asgi", "fastapi", "flask", "django",
            "uvicorn", "httpx", "aiohttp", "global interpreter lock", "gil", "processpoolexecutor"
        ],
        "Trong các tác vụ nặng chờ mạng (I/O-bound), mô hình Synchronous (WSGI: Flask/Requests) khóa cứng luồng khiến CPU ngồi không tới 92% thời gian; trong khi asyncio Event Loop (ASGI: FastAPI/httpx) dùng từ khóa await và epoll/kqueue để xoay vòng hàng nghìn kết nối đồng thời trên một luồng duy nhất.",
        "Minh họa qua bài toán Đại kiện tướng Judit Polgár (CPU 5s/nước) đấu 24 kỳ thủ (I/O chờ 55s/nước): đánh tuần tự từng bàn (Sync Blocking) tốn `43.200s (12 giờ)` vì CPU bị chặn đứng chờ mạng; đánh xoay vòng bất đồng bộ (Async Non-Blocking) chỉ tốn `5.250s (1.5 giờ — nhanh gấp 8.2 lần)`. Khi hàm `async def` gặp `await`, Coroutine tạm dừng và đăng ký Socket với Kernel (`epoll`/`kqueue`), nhường Event Loop chạy tác vụ khác trong `asyncio.gather()`. Với tác vụ tính toán nặng CPU-bound bị khóa bởi GIL, kỹ sư phải tách sang đa tiến trình (`ProcessPoolExecutor`).",
        "results = await asyncio.gather(*(fetch_page(client, url) for url in urls))",
        "Cạm bẫy sinh tử trong FastAPI / asyncio: tuyệt đối không gọi hàm chặn đồng bộ (`time.sleep()`, `requests.get()`) bên trong hàm `async def` vì nó sẽ làm đóng băng toàn bộ Event Loop của máy chủ!"
    ),
    # =========================================================================
    # F04: WEB API — CHẶNG 1 ĐẾN CHẶNG 5 (TCP/IP, 6 API STYLES, AAA/JWT/OAUTH, PROBES/P99, FASTAPI/LOCUST)
    # =========================================================================
    (
        "api.tcp-ip-http-handshake",
        "Mô hình 4 Tầng TCP/IP, Khung Bản tin HTTP (CRLF), Phân giải Đệ quy DNS, Bảo mật Kép TLS & Bắt tay 3 Bước TCP (SYN / SYN-ACK / ACK, NAT)",
        "NETWORK STACK & HTTP",
        ["F04"],
        [
            "web api", "tcp/ip model", "osi model", "http request", "http response",
            "request line", "status line", "http endpoint", "query string",
            "dns lookup", "recursive query", "authoritative nameserver",
            "tls handshake", "symmetric encryption", "asymmetric encryption",
            "tcp 3-way handshake", "three-way handshake", "syn-ack",
            "network address translation", "user datagram protocol"
        ],
        "Mọi lời gọi Web API đều đi xuyên qua 4 tầng TCP/IP: phân giải tên miền thành IP qua DNS (UDP 53), bắt tay 3 bước TCP (SYN 1000 → SYN-ACK 5000/1001 → ACK 5001), thiết lập kênh mã hóa TLS + băm toàn vẹn SHA-256, rồi truyền khung bản tin HTTP ngăn cách bởi dòng trống CRLF.",
        "Mô hình TCP/IP thực chiến gom 7 tầng OSI thành 4 tầng vật lý: Application (HTTP, DNS, TLS), Transport (TCP đảm bảo thứ tự và chống mất gói vs. UDP 8-byte tốc độ cao), Internet/Network (định tuyến IPv4 32-bit / IPv6 128-bit kết hợp Router NAT dịch IP nội bộ 192.168.1.10 sang Public IP 203.0.113.5), và Link (Ethernet/Wi-Fi MAC Address). Khung HTTP Request/Response luôn gồm 4 phần tách biệt metadata và body bằng vách ngăn `\\r\\n\\r\\n` (CRLF).",
        "POST /api/order-service/v1/orders HTTP/1.1\\r\\nHost: fsds_server.com\\r\\nContent-Type: application/json\\r\\n\\r\\n{\"order_id\":\"ORD-8888\"}",
        "Trong HTTP, `GET`, `PUT`, `DELETE` có tính lũy đẳng (Idempotent), còn `POST` mặc định không lũy đẳng nên bắt buộc phải đính kèm `Idempotency-Key` khi gọi API tạo đơn hoặc thanh toán!"
    ),
    (
        "api.rest-six-principles",
        "Kiến trúc REST API & Sáu Nguyên lý Bất biến của Roy Fielding (Client-Server, Statelessness, Uniform Interface, Caching, Layered System, Code on Demand)",
        "API ARCHITECTURES",
        ["F04"],
        [
            "rest api", "restful api", "roy fielding", "statelessness",
            "uniform interface", "layered system", "code on demand",
            "hateoas", "api gateway", "cache-control", "etag"
        ],
        "REST là phong cách kiến trúc API phổ biến nhất (93% theo Postman Report), xoay quanh Tài nguyên (Resources định danh bằng URI) và 6 nguyên lý kiến trúc giúp hệ thống mở rộng ngang vô hạn phía sau Load Balancer.",
        "Sáu nguyên lý RESTful gồm: (1) Client-Server (tách biệt giao diện và lưu trữ), (2) Statelessness ('Không trí nhớ' — mỗi Request tự mang đủ ngữ cảnh và Token, không khóa phiên trên RAM máy chủ), (3) Uniform Interface (URI chuẩn như `/v1/orders/ORD-8888` kết hợp HTTP Verbs `GET/POST/PUT/PATCH/DELETE`), (4) Caching (`Cache-Control`, `ETag`, `304 Not Modified`), (5) Layered System (đi qua Firewall → API Gateway → Load Balancer hoàn toàn trong suốt), và (6) Code on Demand (tùy chọn).",
        "GET /api/superhero-service/v1/superheroes/42?fields=name,origin HTTP/1.1",
        "Năm nguyên lý đầu tiên là bắt buộc để một dịch vụ được công nhận là RESTful; vi phạm tính Statelessness (lưu Session cục bộ trên RAM của 1 Pod) sẽ phá hỏng khả năng Auto-scaling!"
    ),
    (
        "api.graphql-grpc-protobuf",
        "GraphQL (Single Endpoint Query AST, Over/Under-fetching & DataLoader) vs. gRPC (Protocol Buffers Nhị phân & Đa luồng HTTP/2 Multiplexing)",
        "API ARCHITECTURES",
        ["F04"],
        [
            "graphql", "over-fetching", "under-fetching", "dataloader",
            "grpc", "protocol buffers", "protobuf", "http/2", "http/2 multiplexing",
            "unary rpc", "server streaming", "bidirectional streaming", "grpc-web"
        ],
        "GraphQL giải quyết triệt để bệnh lấy thừa (Over-fetching) và lấy thiếu nhiều vòng (Under-fetching) của REST cho giao diện phức tạp, còn gRPC nén dữ liệu thành nhị phân Protocol Buffers chạy đa luồng trên HTTP/2 cho giao tiếp nội bộ Microservices và ML Serving.",
        "Với GraphQL, Client gửi cây truy vấn khai báo (`Query AST`) tới duy nhất một cổng `POST /graphql` để lấy đúng các trường cần thiết trong 1 vòng mạng (kết hợp `DataLoader` ở Backend để gom nhóm chống lỗi N+1 SQL). Với gRPC, dịch vụ định nghĩa hợp đồng `.proto` nghiêm ngặt, mã hóa dữ liệu bằng `Protocol Buffers` (dùng số thứ tự Field Tags `1, 2, 3` thay vì lặp chuỗi JSON giúp giảm 3–5 lần kích thước) và truyền qua `HTTP/2 Multiplexing` trên 1 kết nối TCP duy nhất.",
        "service ModelService { rpc Predict (FraudRequest) returns (FraudResponse); }",
        "Trình duyệt web không thể gọi gRPC thuần trực tiếp vì thiếu quyền kiểm soát khung nhị phân HTTP/2 Trailers — hãy dùng REST/GraphQL ngoài biên (North-South) và gRPC bên trong cụm (East-West)!"
    ),
    (
        "api.websocket-sse-webhook",
        "Truyền thông Thời gian thực & Hướng Sự kiện: WebSocket (101 Switching Protocols Song công) vs. Server-Sent Events (SSE text/event-stream) vs. Webhook (Reverse API)",
        "REAL-TIME & EVENT APIS",
        ["F04"],
        [
            "websocket", "websockets", "switching protocols", "full-duplex",
            "server-sent events", "sse", "text/event-stream", "eventsource",
            "webhook", "webhooks", "reverse api", "short polling"
        ],
        "Thay vì hỏi đi hỏi lại gây lãng phí băng thông (Polling), WebSocket mở đường hầm 2 chiều liên tục (Full-Duplex), SSE đẩy luồng sự kiện 1 chiều từ Server xuống trình duyệt qua HTTP chuẩn (như stream token LLM), còn Webhook đảo chiều để Server chủ động bắn HTTP POST báo tin khi có sự kiện.",
        "WebSocket khởi đầu bằng HTTP Handshake kèm header `Upgrade: websocket` (`HTTP 101 Switching Protocols`) để giữ kết nối TCP mở cho Chat/Game 2 chiều. Server-Sent Events (`SSE`) dùng `Content-Type: text/event-stream` đơn hướng (`Server → Client`), đi xuyên qua tường lửa dễ dàng và tự động kết nối lại qua `EventSource`. Webhook ('Don't call us, we'll call you') là lời gọi `HTTP POST` giữa Server với Server (như GitHub báo Jenkins build hoặc cổng thanh toán báo `Order #8888` thành công).",
        "event: pipeline_update\\ndata: {\"job_id\": 123, \"status\": \"completed\"}\\n\\n",
        "Khi viết cổng nhận Webhook trên Production, bắt buộc phải: (1) kiểm tra chữ ký `HMAC-SHA256`, (2) trả `200 OK / 202 Accepted` ngay dưới 200ms, và (3) khử trùng lặp theo `event_id`!"
    ),
    (
        "api.aaa-basic-jwt-oauth",
        "Bảo mật Web API: 6 Mối Đe dọa, Khung Quản trị AAA (AuthN / AuthZ / Accounting), Basic Auth (Base64), Chữ ký Số JWT & Ủy quyền OAuth 2.0",
        "API SECURITY",
        ["F04"],
        [
            "aaa framework", "authentication", "authorization", "accounting",
            "basic auth", "basic authentication", "base64", "json web token",
            "bearer token", "oauth", "oauth 2.0", "authorization code",
            "access token", "refresh token", "prompt injection", "rbac"
        ],
        "Bảo mật API phòng thủ trước 6 mối đe dọa (bao gồm cả Prompt Injection cho LLM) bằng khung 3 chốt chặn AAA (Xác thực danh tính → Phân quyền RBAC → Kiểm toán Accounting) và 3 cơ chế: Basic Auth, JWT không trạng thái và ủy quyền OAuth 2.0.",
        "Basic Auth chỉ ghép `username:password` rồi mã hóa `Base64` (ai bắt được gói tin đều giải mã được ngay nếu thiếu HTTPS). JSON Web Token (`JWT`) gồm 3 phần `Header.Payload.Signature` nối bằng dấu chấm, được ký bằng `HMAC-SHA256` hoặc `RS256` giúp Server xác thực trong RAM (`0 DB Lookup`). OAuth 2.0 dùng luồng 8 bước (`Consent Flow → Authorization Grant Code → Access Token`) giúp ứng dụng thứ ba truy cập tài nguyên trong phạm vi `Scope` mà không bao giờ biết mật khẩu gốc của người dùng.",
        "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJVU1ItMTA0Iiwicm9sZSI6InZpZXdlciJ9.<sig>",
        "Phân biệt rõ mã lỗi HTTP: `401 Unauthorized` nghĩa là chưa xác thực danh tính (thiếu hoặc sai Token — AuthN), còn `403 Forbidden` nghĩa là đã biết bạn là ai nhưng vai trò `viewer` không đủ quyền xóa đơn (AuthZ)!"
    ),
    (
        "api.probes-p99-load-stress",
        "Giám sát Sức khỏe Kubernetes (/liveness vs. /readiness), Phân vị Độ trễ Đuôi (p50 / p95 / p99) & Kiểm thử Chịu tải (Load vs. Stress Testing, Graceful Degradation)",
        "API MONITORING & TESTING",
        ["F04"],
        [
            "health check", "liveness probe", "readiness probe", "/liveness", "/readiness",
            "tail latency", "p50", "p95", "p99", "requests per second",
            "spike testing", "soak testing", "capacity testing", "volume testing",
            "graceful degradation", "hard failure"
        ],
        "Trên Production, dịch vụ tách bạch /liveness (tiến trình có bị treo cứng cần Restart Pod không) với /readiness (mô hình ML và DB đã nạp xong để nhận tải từ Load Balancer chưa), đo độ trễ qua phân vị p50/p95/p99 và ép tải bằng Load/Stress Testing.",
        "Nếu `/liveness` báo lỗi, Kubernetes giết và khởi động lại Pod; nếu `/readiness` báo lỗi (`503`), Kubernetes chỉ tạm ngắt Pod khỏi Load Balancer (cực kỳ quan trọng khi đang nạp mô hình ML nhiều GB vào RAM). Về hiệu năng, số trung bình cộng luôn che giấu trải nghiệm tệ nhất, nên kỹ sư dùng phân vị `p99` (1% yêu cầu chậm nhất). Trong 6 loại kiểm thử hiệu năng, `Load Testing` giữ tải ở ngưỡng kỳ vọng (100 CCU), còn `Stress Testing` đẩy vượt giới hạn (220 CCU suy giảm → 280 CCU gãy) để thiết kế cơ chế suy thoái êm dịu (`Graceful Degradation`) thay vì sập cứng (`Hard Failure`).",
        "GET /readiness -> HTTP 503 Service Unavailable {\"model_loaded\": false, \"db_ready\": true}",
        "Cấm kiểm tra kết nối Database bên trong `/liveness`! Một sự cố chập chờn DB 3 giây sẽ khiến Kubernetes tưởng nhầm toàn bộ 50 API Pods bị treo và giết đồng loạt (Cascading Restart Storm)."
    ),
    (
        "api.fastapi-asgi-pydantic-locust",
        "Kiến trúc FastAPI Thực chiến: Động cơ ASGI (Uvicorn uvloop + Starlette), Cổng Kiểm dịch Pydantic v2 (Rust), Chuỗi Middleware, Depends & Bắn tải Locust",
        "FASTAPI & LOCUST LAB",
        ["F04"],
        [
            "fastapi", "starlette", "uvicorn", "uvloop", "pydantic v2",
            "pydantic-core", "basemodel", "dependency injection", "depends",
            "middleware", "locust", "locustfile", "httpuser"
        ],
        "FastAPI kết hợp động cơ bất đồng bộ ASGI (Uvicorn uvloop + Starlette), lõi kiểm định kiểu dữ liệu viết bằng Rust của Pydantic v2 (chặn rác với HTTP 422), đồ thị tiêm phụ thuộc Depends() và công cụ bắn tải Locust (gevent).",
        "Khác với Flask (WSGI khóa 1 luồng OS cho mỗi Request chờ I/O), FastAPI chạy trên chuẩn ASGI giúp xử lý hàng nghìn kết nối đồng thời. Mọi JSON đầu vào được `Pydantic v2` (`pydantic-core` bằng Rust) ép kiểu và kiểm tra ràng buộc trước khi chạm vào hàm xử lý; dữ liệu đầu ra được lọc qua `response_model` để chống lộ trường nhạy cảm. Khi kiểm thử hiệu năng, công cụ `Locust` dùng `gevent` greenlets nhẹ để giả lập hàng trăm `HttpUser` bắn tải và vẽ biểu đồ `RPS / p95 / p99` theo thời gian thực.",
        "locust -f locustfile.py --headless -u 100 -r 10 --run-time 5m --host http://localhost:8000",
        "Quy tắc sống còn trong FastAPI: chỉ khai báo `async def` khi toàn bộ lời gọi I/O bên trong đều không chặn (`await asyncpg / httpx`); nếu gọi hàm đồng bộ chặn luồng, hãy khai báo `def` thường để FastAPI tự động đẩy sang Worker Threadpool!"
    ),
    # =========================================================================
    # D05: CONSUMPTION LAYER (DW, KIMBALL, SCD, DATA VAULT, OLAP, FEAST)
    # =========================================================================
    (
        "consumption.dwh-etl-er",
        "Data Warehouse Architecture (Staging Area, Data Marts), ETL Pipeline & ER Normalization (1NF → 2NF → 3NF)",
        "DATA WAREHOUSE & ETL",
        ["D05"],
        [
            "staging area", "data marts", "data mart", "er modeling",
            "entity-relationship modeling", "partial dependency", "transitive dependency",
            "join penalty"
        ],
        "Data Warehouse là kho lưu trữ phân tích trung tâm (Single Source of Truth) gom dữ liệu từ nhiều nguồn qua vùng đệm Staging Area rồi phân phối về các Data Marts theo phòng ban, tách biệt hoàn toàn tải OLAP khỏi cơ sở dữ liệu giao dịch OLTP đã chuẩn hóa 3NF.",
        "Trong khi ER Modeling chuẩn hóa bảng phẳng qua 3 bậc (1NF tách ô đa giá trị thành nguyên tử, 2NF khử phụ thuộc hàm bộ phận vào khóa ghép, 3NF khử phụ thuộc bắc cầu giữa các cột không khóa) để giúp OLTP chống dị thường Ghi/Xóa, việc chạy báo cáo tổng hợp trên hàng chục bảng 3NF sẽ gây thắt cổ chai Multi-Way Hash Join. Do đó, quy trình ETL trích xuất dữ liệu nguồn về vùng đệm Staging Area để làm sạch và tái cấu trúc trước khi nạp vào Warehouse và các Data Marts.",
        "SELECT c.region, SUM(oi.qty * oi.unit_price) FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN customers c ON o.customer_id = c.customer_id GROUP BY c.region;",
        "Không bao giờ cho phép công cụ BI truy vấn trực tiếp vào vùng đệm Staging Area hoặc cơ sở dữ liệu OLTP đang phục vụ giao dịch trực tuyến."
    ),
    (
        "consumption.kimball-star-snowflake",
        "Dimensional Modeling (Kimball 4-Step Process), Fact vs. Dimension Tables, Role-Playing Date Dimension & Star vs. Snowflake Schema",
        "DIMENSIONAL MODELING",
        ["D05"],
        [
            "dimensional modeling", "kimball", "declare the grain", "role-playing dimension",
            "factSales", "dimDate", "dimCustomer", "conformed dimensions"
        ],
        "Dimensional Modeling tổ chức dữ liệu xoay quanh bảng Fact (chứa con số đo lường tại tâm) kết nối trực tiếp 1-hop tới các bảng Dimension phẳng (chứa ngữ cảnh mô tả Who, What, Where, When) theo kiến trúc Star Schema để tối ưu tốc độ quét và gộp nhóm.",
        "Quy trình thiết kế 4 bước của Ralph Kimball bắt buộc tuần tự: (1) Chọn quy trình nghiệp vụ, (2) Tuyên bố độ mịn nguyên tử (Declare the Grain), (3) Chọn các chiều ngữ cảnh, (4) Xác định các chỉ số đo lường. Khác với Snowflake Schema chia nhỏ bảng chiều thành chuỗi phân cấp nhiều tầng (DIM_CUSTOMER -> DIM_CITY -> DIM_STATE -> DIM_COUNTRY) làm tăng số phép Join, Star Schema chấp nhận phi chuẩn hóa nhẹ trên bảng Dimension để đạt tốc độ truy vấn OLAP nhanh nhất.",
        "SELECT d.Year, d.Quarter, c.Country, SUM(f.SalesAmount) FROM factSales f JOIN dimDate d ON f.OrderDateKey = d.DateKey JOIN dimCustomer c ON f.CustomerKey = c.CustomerKey GROUP BY 1, 2, 3;",
        "Một bảng chiều thời gian dimDate duy nhất với khóa nguyên thông minh YYYYMMDD (ví dụ 20260501) có thể đóng nhiều vai trò (Role-Playing Dimension) cho cả OrderDateKey, ShipDateKey và PaymentDateKey."
    ),
    (
        "consumption.additive-semi-additive",
        "Fact Measure Additivity: Additive (SalesAmount) vs. Semi-Additive (InventoryLevel Snapshot) vs. Non-Additive (UnitPrice / Ratios)",
        "FACT MEASURES & GRAIN",
        ["D05"],
        [
            "additive", "semi-additive", "non-additive", "additive measure",
            "semi-additive measure", "non-additive measure", "inventorylevel",
            "periodic snapshot"
        ],
        "Các chỉ số trong bảng Fact được phân thành 3 nhóm theo khả năng cộng gộp: Additive cộng được trên mọi chiều, Semi-Additive cộng được theo sản phẩm/kho hàng nhưng cấm cộng dọc theo chiều thời gian, còn Non-Additive tuyệt đối không được cộng trực tiếp.",
        "Với chỉ số Additive như doanh thu (SalesAmount), hàm SUM() cho kết quả đúng trên mọi tổ hợp chiều. Ngược lại, số dư tồn kho (InventoryLevel) hoặc số dư tài khoản ngân hàng là ảnh chụp trạng thái (Periodic Snapshot): nếu lấy tồn kho ngày 1 (100) cộng ngày 2 (80) cộng ngày 3 (120) bằng SUM() sẽ ra con số ảo 300; kỹ sư bắt buộc phải dùng LAST_VALUE() cuối kỳ hoặc AVG() theo thời gian. Với chỉ số Non-Additive như đơn giá hay biên lợi nhuận (%), phải lưu riêng tử số và mẫu số rồi chia sau khi gom nhóm.",
        "SELECT ProductKey, AVG(InventoryLevel) AS avg_stock, LAST_VALUE(InventoryLevel) OVER (PARTITION BY ProductKey ORDER BY DateKey) AS eod_stock FROM factInventory;",
        "Cộng nhầm chỉ số Semi-Additive (như tồn kho hoặc số dư tài khoản) dọc theo chiều thời gian bằng hàm SUM() là lỗi sai lệch báo cáo tài chính kinh điển nhất trong thiết kế Data Warehouse."
    ),
    (
        "consumption.scd-types",
        "Slowly Changing Dimensions (SCD Type 0, 1, 2, 3, 4 & Hybrid Type 6), Surrogate Keys & Point-in-Time Historical Tracking",
        "SLOWLY CHANGING DIMENSIONS",
        ["D05"],
        [
            "slowly changing dimensions", "scd type 0", "scd type 1", "scd type 2",
            "scd type 3", "scd type 4", "scd type 6", "row versioning", "history table"
        ],
        "Slowly Changing Dimensions (SCD Type 0–6) là tập hợp các chiến lược kiểm soát sự thay đổi thuộc tính của bảng chiều theo thời gian, trong đó SCD Type 2 tạo dòng phiên bản mới kèm Surrogate Key để bảo toàn trọn vẹn lịch sử tại đúng thời điểm giao dịch phát sinh.",
        "Khi khách hàng đổi đơn vị tiền tệ từ GBP sang USD, SCD Type 1 ghi đè trực tiếp làm mất lịch sử cũ; SCD Type 2 đóng hiệu lực dòng cũ (Data To = 25/09/2025, Delete Flag = 1) và chèn dòng mới với Surrogate Key mới để bảng Fact neo đúng phiên bản lịch sử; SCD Type 3 thêm cột Previous Currency lưu đúng 1 giá trị liền trước; SCD Type 4 tách bảng Current nhỏ gọn khỏi bảng History; còn SCD Type 6 (1+2+3=6) kết hợp cả dòng phiên bản Type 2, cột Previous Type 3 và ghi đè cột Current trên mọi phiên bản để hỗ trợ phân tích cả As-Was lẫn As-Is.",
        "SELECT f.OrderDateKey, d.Currency AS as_was_ccy, d.Current_Currency AS as_is_ccy, SUM(f.SalesAmount) FROM factSales f JOIN dimCustomer_SCD6 d ON f.CustomerKey = d.SurrogateKey GROUP BY 1, 2, 3;",
        "Khi áp dụng SCD Type 2 hoặc Type 6, tuyệt đối không dùng Natural Key (như customer_id gốc) làm khóa chính của bảng Dimension mà bắt buộc phải sinh Surrogate Key độc lập cho từng phiên bản dòng."
    ),
    (
        "consumption.datavault-medallion",
        "Data Vault 2.0 (Hub, Link, Satellite) & Inmon (Top-Down) vs. Kimball (Bottom-Up) Convergence on Medallion Architecture",
        "DATA VAULT & MEDALLION",
        ["D05"],
        [
            "data vault", "hub_customer", "link_order_customer", "sat_customer",
            "inmon vs kimball", "top-down approach", "bottom-up approach",
            "medallion naming convention"
        ],
        "Data Vault tách rời khóa nghiệp vụ (Hub), mối quan hệ giao dịch (Link) và thuộc tính lịch sử biến đổi (Satellite) tại tầng Silver để hấp thụ trôi lược đồ từ hàng chục nguồn ERP/CRM, trước khi xuất bản ra tầng Gold dưới dạng Star Schema của Kimball.",
        "Nếu trường phái Bill Inmon (Top-Down) ưu tiên xây dựng kho dữ liệu chuẩn hóa 3NF toàn doanh nghiệp trước rồi mới tách Data Marts, thì Ralph Kimball (Bottom-Up) xây dựng ngay các Star Schema Data Marts theo quy trình kinh doanh. Trên kiến trúc Medallion hiện đại, hai tư tưởng này hội tụ: tầng Bronze lưu nguyên bản dữ liệu thô (bronze_<source>_<entity>), tầng Silver làm sạch và tích hợp theo chuẩn 3NF hoặc Data Vault (hub_, lnk_, sat_ chỉ chèn thêm dòng mới khi đổi thuộc tính), và tầng Gold phục vụ BI tốc độ cao bằng Star Schema hoặc OBT (fact_, dim_, mart_).",
        "INSERT INTO sat_customer (customer_hash_key, load_date, record_source, name, address) VALUES (MD5('123456'), CURRENT_TIMESTAMP, 'CRM_API', 'Peter Pan', 'New York, US');",
        "Trong Data Vault, các bảng Hub và Link không bao giờ chứa thuộc tính mô tả hay bị cập nhật ghi đè: mọi thay đổi thông tin đều được ghi nối đuôi (Insert-Only) vào bảng Satellite kèm mốc thời gian LOAD_DATE."
    ),
    (
        "consumption.olap-simd-clickhouse",
        "OLAP Vectorized Execution (SIMD AVX-512) & ClickHouse Architecture (MergeTree 8,192 Granule Sparse Index, S3 & Keeper)",
        "CLICKHOUSE & SIMD OLAP",
        ["D05"],
        [
            "vectorized execution", "simd", "avx-512", "clickhouse", "mergetree",
            "replicatedmergetree", "sparse primary index", "granule", "clickhouse keeper"
        ],
        "Động cơ OLAP hiện đại như ClickHouse kết hợp lưu trữ cột nén chặt, thực thi vector hóa bằng tập lệnh SIMD CPU (cộng cả mảng 4–16 số trong 1 chu kỳ lệnh) và chỉ mục thưa MergeTree (mỗi Granule 8.192 dòng) để quét hàng tỷ bản ghi trong vài chục mili-giây.",
        "Kiến trúc ClickHouse gồm 4 thành phần: (1) ClickHouse Nodes thực thi truy vấn song song vector hóa kèm bộ đệm Mark/Page Cache; (2) Columnar Storage chia bảng MergeTree thành các Data Parts bất biến được sắp xếp theo ORDER BY và đánh dấu thưa mỗi 8.192 dòng (Sparse Primary Index nằm gọn trong RAM); (3) S3-Compatible Object Storage tách rời lưu trữ và tính toán; và (4) ZooKeeper / ClickHouse Keeper điều phối siêu dữ liệu nhân bản giữa các Node. Do mỗi lần ghi tạo một Data Part bất biến rồi gộp ngầm, ClickHouse không phù hợp cho tác vụ UPDATE/DELETE từng dòng đơn lẻ.",
        "CREATE TABLE analytics.events (region LowCardinality(String), user_id UInt64, amount Decimal(10,2), ts DateTime) ENGINE = ReplicatedMergeTree() ORDER BY (region, ts, user_id) SETTINGS index_granularity = 8192;",
        "Trong ClickHouse, thứ tự các cột trong mệnh đề ORDER BY quyết định trực tiếp cấu trúc vật lý của Sparse Primary Index: luôn đặt cột có độ phân biệt thấp (Low Cardinality như region, date) đứng trước cột có độ phân biệt cao (user_id)."
    ),
    (
        "consumption.apache-pinot-hybrid",
        "Apache Pinot Real-Time Distributed OLAP: Dimensions/Metrics/Time Schema, Hybrid Tables (Time Boundary) & Star-Tree Index",
        "APACHE PINOT REAL-TIME OLAP",
        ["D05"],
        [
            "apache pinot", "pinot", "hybrid table", "hybrid tables", "realtime table",
            "offline table", "time boundary", "star-tree index", "user-facing analytics"
        ],
        "Apache Pinot là động cơ OLAP phân tán thời gian thực chuyên trị các ứng dụng phân tích hướng người dùng cuối (User-Facing Analytics) với hàng chục nghìn truy vấn mỗi giây và độ trễ vài mili-giây thông qua kiến trúc Hybrid Table và chỉ mục Star-Tree.",
        "Pinot định nghĩa lược đồ cố định gồm Dimensions (lọc/nhóm), Metrics (tổng hợp số học) và Time Column. Để vừa có dữ liệu tươi từng giây vừa tiết kiệm chi phí lưu trữ lịch sử, Hybrid Table của Pinot hợp nhất một Real-time Table (hút trực tiếp từ Apache Kafka) và một Offline Table (nạp các phân đoạn nén sẵn từ S3/Data Lake) dưới một tên bảng duy nhất: Pinot Broker tự động dùng mốc ranh giới thời gian (Time Boundary) để chia truy vấn đọc lịch sử từ Offline Segments và phần mới nhất từ Real-time Segments.",
        "SELECT user_id, COUNT(*) AS tx_cnt FROM transactions_HYBRID WHERE event_time >= ago('P7D') GROUP BY user_id HAVING tx_cnt >= 5 LIMIT 50;",
        "Chọn ClickHouse khi ưu tiên truy vấn SQL phức tạp, phép Join lớn và phân tích nội bộ/log; chọn Apache Pinot khi xây dựng tính năng phân tích nhúng trực tiếp cho hàng triệu người dùng cuối đòi hỏi độ trễ p99 dưới 20ms."
    ),
    (
        "consumption.feast-feature-store",
        "ML Feature Store & Feast Architecture: Training-Serving Skew, Offline vs. Online Store (< 10ms Redis), Point-in-Time ASOF Join & Materialization",
        "FEAST & FEATURE STORE",
        ["D05"],
        [
            "feature store", "feast", "training-serving skew", "offline store",
            "online store", "featureview", "feast apply", "get_historical_features",
            "get_online_features", "materialize-incremental", "point-in-time join"
        ],
        "Feature Store như Feast là tầng chia sẻ đặc trưng thống nhất giữa Data Engineering và Machine Learning, xóa sổ hoàn toàn căn bệnh lệch công thức huấn luyện–phục vụ (Training-Serving Skew) và rò rỉ dữ liệu tương lai nhờ kiến trúc lưu trữ kép Offline/Online.",
        "Khi không có Feature Store, việc viết SQL khi huấn luyện (ra avg_tx_30d = 45.73) và viết lại bằng Python lúc chạy thật (ra 46) làm suy giảm ngầm độ chính xác của mô hình phát hiện gian lận. Feast giải quyết bằng một định nghĩa FeatureView duy nhất trên Central Registry (feast apply): khi tạo tập huấn luyện, hàm get_historical_features() thực hiện phép kết lùi thời gian (Point-in-Time ASOF Join) trên Offline Store (S3/BigQuery/DuckDB) để chống rò rỉ tương lai; tiến trình feast materialize-incremental đồng bộ giá trị mới nhất sang Online Store (Redis/DynamoDB) để hàm get_online_features() trả kết quả dưới 10ms lúc chấm điểm trực tuyến.",
        "feast apply && feast materialize-incremental $(date -u +\"%Y-%m-%dT%H:%M:%S\")",
        "Tuyệt đối không dùng phép LEFT JOIN thông thường theo user_id để tạo dữ liệu huấn luyện ML vì nó sẽ lấy nhầm đặc trưng được tính ở tương lai sau thời điểm giao dịch phát sinh — bắt buộc dùng Point-in-Time ASOF Join qua get_historical_features()."
    ),
]


def _clean_short_definition(text: str) -> str:
    s = re.sub(r"\*\*(.*?)\*\*", r"\1", str(text or ""))
    s = s.replace("`", "")
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= 180:
        return s
    # Take first complete clause/sentence <= 180 chars
    for sep in (". ", "; ", " — ", ": "):
        idx = s.find(sep)
        if 45 <= idx <= 175:
            return s[: idx + (1 if sep == ". " else 0)].rstrip(" ,;:") + ("." if not s[: idx + 1].endswith(".") else "")
    cut = s[:176].rsplit(" ", 1)[0].rstrip(" ,;:-—")
    return cut + "…"


def _resolve_station_link(tid: str, scope: list) -> str:
    exact_map = {
        "linux.kernel": "#/F01/1/linux-1-1",
        "linux.gnu": "#/F01/1/linux-1-1",
        "linux.distro": "#/F01/1/linux-1-2",
        "linux.terminal-shell": "#/F01/1/linux-1-3",
        "linux.program-vs-process": "#/F01/1/linux-1-3",
        "linux.system-call": "#/F01/1/linux-1-3",
        "linux.process-identity": "#/F01/2/linux-2-1",
        "linux.env-path": "#/F01/2/linux-2-1",
        "linux.everything-is-a-file": "#/F01/2/linux-2-2",
        "linux.inode": "#/F01/2/linux-2-2",
        "linux.permissions": "#/F01/2/linux-2-1",
        "linux.fhs-tree": "#/F01/2/linux-2-3",
        "linux.cli-navigation": "#/F01/2/linux-2-4",
        "linux.file-descriptors": "#/F01/3/linux-3-1",
        "linux.pipe": "#/F01/3/linux-3-1",
        "linux.redirection": "#/F01/3/linux-3-2",
        "linux.bash-scripting": "#/F01/4/linux-4-1",
        "linux.gcc-compilation": "#/F01/4/linux-4-2",
        "linux.makefile": "#/F01/4/linux-4-2",
        "linux.cronjob": "#/F01/4/linux-4-3",
        "python.cpython-pyobject-gc": "#/F02/1/python-1-1",
        "python.venv-poetry-uv": "#/F02/1/python-1-2",
        "python.name-binding-mutability": "#/F02/2/python-2-1",
        "python.hash-table-complexity": "#/F02/2/python-2-2",
        "python.context-manager-argparse": "#/F02/3/python-3-1",
        "python.asyncio-wsgi-asgi": "#/F02/4/python-4-2",
        "db.rdbms-architecture": "#/F03/1/db-1-1",
        "db.keys-constraints": "#/F03/1/db-1-2",
        "db.normalization": "#/F03/1/db-1-3",
        "db.postgres-memory-process": "#/F03/2/db-2-1",
        "db.slotted-page": "#/F03/2/db-2-2",
        "db.wal-checkpointer": "#/F03/2/db-2-3",
        "db.mvcc-autovacuum": "#/F03/3/db-3-1",
        "db.btree-vs-lsm": "#/F03/3/db-3-2",
        "db.optimizer-explain": "#/F03/3/db-3-3",
        "db.scaling-sharding": "#/F03/4/db-4-1",
        "db.ha-replication-pgd": "#/F03/4/db-4-2",
        "db.nosql-cap-base": "#/F03/4/db-4-3",
        "api.tcp-ip-http-handshake": "#/F04/1/api-1-4",
        "api.rest-six-principles": "#/F04/2/api-2-1",
        "api.graphql-grpc-protobuf": "#/F04/2/api-2-3",
        "api.websocket-sse-webhook": "#/F04/2/api-2-4",
        "api.aaa-basic-jwt-oauth": "#/F04/3/api-3-3",
        "api.probes-p99-load-stress": "#/F04/4/api-4-1",
        "api.fastapi-asgi-pydantic-locust": "#/F04/5/api-5-1",
        "validation.v-model-shift-left": "#/F05/1/validation-1-1",
        "validation.testing-methods-formal": "#/F05/1/validation-1-2",
        "validation.functional-nonfunctional-scopes": "#/F05/2/validation-2-1",
        "validation.pytest-fixtures-conftest": "#/F05/3/validation-3-1",
        "validation.pytest-markers-parametrize": "#/F05/3/validation-3-2",
        "validation.mocking-testcontainers-tdd": "#/F05/4/validation-4-1",
        "container.infra-vm-vs-container": "#/F06/1/container-1-1",
        "container.linux-namespaces-cgroups": "#/F06/2/container-2-1",
        "container.overlayfs-seccomp": "#/F06/2/container-2-3",
        "container.oci-runtime-stack": "#/F06/3/container-3-2",
        "container.kubernetes-orchestration": "#/F06/4/container-4-2",
        "ingestion.source-gigo-etlt": "#/D01/1/ingestion-1-1",
        "ingestion.cdc-three-generations": "#/D01/2/ingestion-2-4",
        "ingestion.kafka-kraft-ecosystem": "#/D01/3/ingestion-3-2",
        "ingestion.partition-offset-lag": "#/D01/3/ingestion-3-3",
        "ingestion.producer-consumer-isr-eos": "#/D01/4/ingestion-4-4",
        "ingestion.debezium-wal-outbox": "#/D01/5/ingestion-5-3",
        "spark.dag_scheduler": "#/D03/1/spark-1-3",
        "spark.rdd_dataframe": "#/D03/2/spark-2-4",
        "spark.kryo_serialization": "#/D03/3/spark-3-2",
        "spark.unified_memory": "#/D03/3/spark-3-4",
        "spark.catalyst": "#/D03/4/spark-4-2",
        "spark.tungsten": "#/D03/4/spark-4-3",
        "spark.aqe": "#/D03/4/spark-4-4",
        "spark.key_salting": "#/D03/5/spark-5-2",
        "spark.broadcast_join": "#/D03/5/spark-5-1",
        "spark.dynamic_allocation": "#/D03/6/spark-6-2",
        "spark.data_compaction": "#/D03/6/spark-6-3",
        "flink.architecture-slots": "#/D04/1/flink-1-2",
        "flink.time-watermarks": "#/D04/2/flink-2-2",
        "flink.windows-triggers-lateness": "#/D04/3/flink-3-3",
        "flink.apis-dynamic-table-sql": "#/D04/4/flink-4-2",
        "flink.state-rocksdb-checkpoint": "#/D04/5/flink-5-3",
        "flink.chaining-backpressure-deploy": "#/D04/6/flink-6-2",
        "consumption.dwh-etl-er": "#/D05/1/consumption-1-1",
        "consumption.kimball-star-snowflake": "#/D05/2/consumption-2-1",
        "consumption.additive-semi-additive": "#/D05/2/consumption-2-2",
        "consumption.scd-types": "#/D05/3/consumption-3-1",
        "consumption.datavault-medallion": "#/D05/3/consumption-3-3",
        "consumption.olap-simd-clickhouse": "#/D05/4/consumption-4-2",
        "consumption.apache-pinot-hybrid": "#/D05/4/consumption-4-3",
        "consumption.feast-feature-store": "#/D05/5/consumption-5-2",
        "orchestration.pipeline-five-pillars": "#/D06/1/orchestration-1-1",
        "orchestration.idempotency-backfill-dynamic": "#/D06/2/orchestration-2-2",
        "orchestration.airflow-dag-architecture": "#/D06/3/orchestration-3-2",
        "orchestration.operators-sensors-xcom": "#/D06/3/orchestration-3-3",
        "orchestration.executors-concurrency-pools": "#/D06/4/orchestration-4-3",
        "orchestration.circuit-breaker-contracts-datahub": "#/D06/5/orchestration-5-2",
        "storage.memory-hierarchy": "#/D02/1/storage-1-1",
        "storage.ram-spill-to-disk": "#/D02/1/storage-1-2",
        "storage.disk-seek-vs-scan": "#/D02/1/storage-1-3",
        "storage.data-temperature": "#/D02/1/storage-1-4",
        "storage.oltp-vs-olap": "#/D02/1/storage-1-5",
        "storage.file-block-object": "#/D02/2/storage-2-1",
        "storage.row-vs-columnar": "#/D02/2/storage-2-2",
        "storage.apache-arrow": "#/D02/2/storage-2-3",
        "storage.compression-splittability": "#/D02/2/storage-2-4",
        "storage.hdfs-architecture": "#/D02/3/storage-3-1",
        "storage.network-topology-caching": "#/D02/3/storage-3-2",
        "storage.streaming-kafka-cdc": "#/D02/3/storage-3-3",
        "storage.data-warehouse": "#/D02/3/storage-3-4",
        "storage.conceptual-logical-physical": "#/D02/4/storage-4-1",
        "storage.inmon-kimball-datavault": "#/D02/4/storage-4-2",
        "storage.fact-dimension-grain": "#/D02/4/storage-4-3",
        "storage.star-snowflake-obt": "#/D02/4/storage-4-4",
        "storage.surrogate-scd-bus": "#/D02/4/storage-4-5",
        "storage.data-lake-schema-on-read": "#/D02/5/storage-5-1",
        "storage.data-swamp-hive-gaps": "#/D02/5/storage-5-2",
        "storage.data-contracts-zoning": "#/D02/5/storage-5-4",
        "storage.lakehouse-open-table-formats": "#/D02/6/storage-6-1",
        "storage.lakehouse-acid-concurrency": "#/D02/6/storage-6-2",
        "storage.cow-vs-mor": "#/D02/6/storage-6-4",
        "storage.lakehouse-optimizations": "#/D02/6/storage-6-5",
        "storage.medallion-architecture": "#/D02/7/storage-7-1",
        "storage.governance-undercurrents": "#/D02/7/storage-7-3",
    }
    if tid in exact_map:
        return exact_map[tid]
    prefix = tid.split(".")[0] if "." in tid else ""
    if prefix == "linux":
        return "#/F01/1"
    if prefix == "python":
        return "#/F02/1"
    if prefix == "db":
        return "#/F03/1"
    if prefix == "api":
        return "#/F04/1"
    if prefix == "validation":
        return "#/F05/1"
    if prefix == "container":
        return "#/F06/1"
    if prefix == "ingestion":
        return "#/D01/1"
    if prefix == "spark":
        return "#/D03/1"
    if prefix == "flink":
        return "#/D04/1"
    if prefix == "consumption":
        return "#/D05/1"
    if prefix == "orchestration":
        return "#/D06/1"
    if prefix == "storage":
        return "#/D02/1"
    topic = scope[0] if scope else "F01"
    return f"#/{topic}/1"


AMBIGUOUS_OR_NOISY_ALIASES = {
    "q", "i", "u", "dd", "ca", "ap", "cp", "mv", "rm", "ls", "cd", "du", "ps", "sh", "id",
    "ai", "ha", "pk", "fk", "vm", "os", "io", "ip", "db", "fd", "bi", "s3", "c", "c++", "c/c++",
    "linux", "unix", "multi-user", "multi-tasking", "linux 0.01", "kernel", "windows",
    "richard stallman", "linus torvalds", "james dixon", "bill inmon", "ralph kimball",
    "lan", "minh", "nam", "oolong sua", "hong tra tac", "#hd01", "#8888", "đơn hàng #8888", "đơn #8888",
    "open", "read", "write", "close", "cat", "head", "tail", "find", "make", "tab", "target",
    "recipe", "prerequisites", "env", "path", "export", "root", "home", "user", "group",
    "pwd", "grep", "mkdir", "sudo", "chmod", "chown", "chgrp", "vim", "nano", "ssh", "less", "wc",
    "chmod +x", "chmod 755", "chmod 644", "tail -f", "ls -la", "ls -lh", "cp -r", "rm -rf", "mkdir -p", "du -sh", "df -h", "wc -l",
    "program", "process", "processes", "tiến trình", "chương trình", "hạt nhân", "bản phân phối",
    "lời gọi hệ thống", "mọi thứ đều là file", "cây thư mục", "điều hướng", "đường ống pipe",
    "giao tiếp đa tiến trình", "trình biên dịch", "biến môi trường", "cục máy động cơ",
    "hồ dữ liệu", "đầm lầy dữ liệu", "database", "databases", "table", "tables", "index",
    "primary", "secondary", "worker", "driver", "scheduler", "sensor", "operator", "producer", "consumer",
    "document", "logical", "physical", "conceptual", "bronze", "silver", "gold",
    "hot", "warm", "cold", "fact", "dimension", "dimensions", "merged", "workdir",
    "file", "block", "object", "bucket", "binary", "immutable", "immutability", "capacity", "bandwidth", "latency",
    "hardware", "network", "storage", "cpu", "ram", "hdd", "ssd", "pid", "uid", "gid", "cwd",
    "stdin", "stdout", "stderr", "not null", "unique", "check", "default", "select", "where", "from", "join", "group by",
    "rollback", "commit", "vacuum", "explain", "add", "remove", "protocol", "metadata", "commitinfo",
    "docker", "python", "python3", "order-api", "app.py", "document.txt", "image.png", "backup.sh",
    "fact_sales", "dim_date", "dim_customer", "dim_product", "dim_store",
    "start_date", "end_date", "is_current", "total_cost", "order_amount", "so_tien", "thành_tiền",
    "hudi_sales_transactions_bronze", "hudi_web_clickstreams_bronze", "expire_snapshots",
    "lò luyện kim", "nối đuôi", "nhân bản x3", "khoảng cách mạng", "độ trễ truy xuất", "đường dẫn tương đối",
    "field-id bất biến", "bộ hồ sơ căn cước", "hồ sơ căn cước", "ba cổng tiêu chuẩn",
    "xmin", "xmax", "racks", "satellite", "hub", "link", "cdc", "scd", "elt", "etl", "obt",
    "8kb", "16kb", "64kb", "64 kb", "1:1", "1:n", "m:n", "/", ">", ">>", "|", "2>", "&1", "2>&1",
}

CANONICAL_SHORT_TITLES = {
    "linux.kernel": "Linux Kernel (Ring 0)",
    "linux.gnu": "GNU Coreutils & Toolchain",
    "linux.distro": "Linux Distribution (Distro)",
    "linux.terminal-shell": "Terminal & Shell (Bash / Zsh)",
    "linux.program-vs-process": "Program vs. Process (fork / execve)",
    "linux.system-call": "System Call (Syscall)",
    "linux.process-identity": "Process Identity (task_struct)",
    "linux.env-path": "Environment Variables ($PATH)",
    "linux.everything-is-a-file": "Virtual File System (VFS)",
    "linux.inode": "Inode & Directory Entry",
    "linux.permissions": "POSIX File Permissions (rwx)",
    "linux.fhs-tree": "Filesystem Hierarchy Standard (FHS)",
    "linux.cli-navigation": "POSIX CLI Utilities",
    "linux.file-descriptors": "File Descriptors (stdin / stdout / stderr)",
    "linux.pipe": "Kernel Pipe & IPC Stream",
    "linux.redirection": "I/O Redirection & dup2()",
    "linux.bash-scripting": "Bash Scripting & Automation",
    "linux.gcc-compilation": "GCC Compilation Pipeline",
    "linux.makefile": "GNU Make & Incremental Build",
    "linux.cronjob": "Cron Daemon (crond) & systemd Timers",
    "python.cpython-pyobject-gc": "CPython PyObject & Garbage Collector",
    "python.venv-poetry-uv": "Virtual Environments (venv / Poetry / uv)",
    "python.name-binding-mutability": "Name Binding, is vs. == & Mutability",
    "python.hash-table-complexity": "Compact Hash Table O(1) vs. List O(n)",
    "python.context-manager-argparse": "Context Manager (with) & CLI argparse",
    "python.asyncio-wsgi-asgi": "asyncio Event Loop & WSGI vs. ASGI",
    "storage.latency-hierarchy": "Memory & Storage Latency Hierarchy",
    "storage.ram-spill": "Volatile RAM & Spill-to-Disk",
    "storage.seek-vs-scan": "Random Seek (IOPS) vs. Sequential Scan",
    "storage.data-temperature": "Data Temperature Tiering (Hot / Warm / Cold)",
    "storage.oltp-vs-olap": "OLTP vs. OLAP Workloads",
    "storage.file-block-object": "File vs. Block vs. Object Storage",
    "storage.serialization-avro-csv": "Data Serialization & Apache Avro",
    "storage.parquet-columnar": "Apache Parquet & Columnar Layout",
    "storage.apache-arrow": "Apache Arrow & Zero-Copy Memory",
    "storage.compression-splittability": "Compression & File Splittability",
    "storage.hdfs": "Hadoop Distributed File System (HDFS)",
    "storage.network-topology-cache": "Network Topology & In-Memory Cache",
    "storage.kafka-cdc": "Apache Kafka & Change Data Capture (CDC)",
    "storage.data-warehouse": "Cloud Data Warehouse Architecture",
    "storage.conceptual-logical-physical": "Conceptual, Logical & Physical Modeling",
    "storage.inmon-kimball-datavault": "Inmon vs. Kimball vs. Data Vault",
    "storage.fact-dimension-grain": "Fact & Dimension Tables (Grain)",
    "storage.star-snowflake-obt": "Star Schema, Snowflake Schema & OBT",
    "storage.surrogate-scd-bus": "Surrogate Keys & Slowly Changing Dimensions (SCD)",
    "storage.data-lake-schema-on-read": "Data Lake & Schema-on-Read",
    "storage.data-swamp-hive-gaps": "Data Swamp & Hive Metastore Bottlenecks",
    "storage.data-contracts-zoning": "Data Contracts & Lake Zoning",
    "storage.lakehouse-open-table-formats": "Open Table Formats (Delta / Iceberg / Hudi)",
    "storage.lakehouse-acid-concurrency": "Lakehouse ACID, MVCC & Time Travel",
    "storage.cow-vs-mor": "Copy-on-Write (COW) vs. Merge-on-Read (MOR)",
    "storage.lakehouse-optimizations": "Compaction, Z-Ordering & Liquid Clustering",
    "storage.medallion-architecture": "Medallion Architecture (Bronze / Silver / Gold)",
    "storage.governance-undercurrents": "Data Governance & Unity Catalog",
    "db.rdbms-architecture": "RDBMS Engine Architecture",
    "db.keys-constraints": "Relational Keys (PK / FK) & Integrity Constraints",
    "db.normalization": "Database Normalization (1NF → 3NF / BCNF)",
    "db.postgres-memory-process": "PostgreSQL Process & Memory Architecture",
    "db.slotted-page": "8KB Heap Slotted Page & Tuple Layout",
    "db.wal-checkpointer": "Write-Ahead Log (WAL) & Checkpointer",
    "db.mvcc-autovacuum": "MVCC Snapshot Isolation & Autovacuum",
    "db.btree-vs-lsm": "B+Tree vs. LSM-Tree Indexing",
    "db.optimizer-explain": "Cost-Based Query Optimizer & EXPLAIN ANALYZE",
    "db.scaling-sharding": "Horizontal Sharding & Partitioning",
    "db.ha-replication-pgd": "Streaming Replication & High Availability",
    "db.nosql-cap-base": "NoSQL Data Models, CAP Theorem & BASE",
    "api.tcp-ip-http-handshake": "TCP/IP 4-Layer Stack, HTTP, DNS, TLS & 3-Way Handshake",
    "api.rest-six-principles": "REST API & Roy Fielding's 6 Principles",
    "api.graphql-grpc-protobuf": "GraphQL (Query AST) vs. gRPC (Protobuf / HTTP/2)",
    "api.websocket-sse-webhook": "WebSocket (Full-Duplex) vs. SSE vs. Webhook",
    "api.aaa-basic-jwt-oauth": "API Security: AAA, Basic Auth, JWT & OAuth 2.0",
    "api.probes-p99-load-stress": "K8s Probes (/liveness, /readiness), p99 & Load/Stress",
    "api.fastapi-asgi-pydantic-locust": "FastAPI ASGI (uvloop), Pydantic v2 & Locust",
    "validation.v-model-shift-left": "V-Model & Shift-Left Cost (1x → 30x)",
    "validation.testing-methods-formal": "Black/Grey/White-Box & Formal Verification",
    "validation.functional-nonfunctional-scopes": "Functional vs. Non-Functional Scopes",
    "validation.pytest-fixtures-conftest": "Pytest Fixtures (yield & conftest.py)",
    "validation.pytest-markers-parametrize": "Pytest Markers & Parametrize",
    "validation.mocking-testcontainers-tdd": "Mocking, Testcontainers & TDD",
    "container.infra-vm-vs-container": "Hardware Virtualization (VM) vs. OS Containers",
    "container.linux-namespaces-cgroups": "Linux Namespaces & Control Groups (cgroups v2)",
    "container.overlayfs-seccomp": "OverlayFS Union Mount & Seccomp / Capabilities",
    "container.oci-runtime-stack": "OCI Runtime Stack (containerd → shim → runc)",
    "container.kubernetes-orchestration": "Kubernetes Control Plane & Worker Architecture",
    "ingestion.source-gigo-etlt": "Ingestion Layer, GIGO & EtLT Pattern",
    "ingestion.cdc-three-generations": "Change Data Capture (Polling / Trigger / WAL)",
    "ingestion.kafka-kraft-ecosystem": "Apache Kafka, KRaft & Connect Ecosystem",
    "ingestion.partition-offset-lag": "Kafka Partition, Offset, Lag & Zero-Copy",
    "ingestion.producer-consumer-isr-eos": "Producer murmur2, Consumer Group, ISR & EOS",
    "ingestion.debezium-wal-outbox": "Debezium CDC, WAL Bloat, DLQ & Outbox Pattern",
    "spark.dag_scheduler": "Spark Architecture & DAG (Job → Stage → Task)",
    "spark.rdd_dataframe": "Spark RDD & Lineage vs. DataFrame / Dataset[T]",
    "spark.kryo_serialization": "Java Serialization vs. KryoSerializer",
    "spark.unified_memory": "Unified Memory Manager & 5 persist() Levels",
    "spark.catalyst": "Catalyst Optimizer (Pushdown & Constant Folding)",
    "spark.tungsten": "Project Tungsten (Off-Heap, Cache & CodeGen)",
    "spark.aqe": "Adaptive Query Execution (AQE Runtime Tuning)",
    "spark.key_salting": "Batch Challenges, Data Skew & Key Salting",
    "spark.broadcast_join": "Broadcast Hash Join (BHJ) vs. Sort-Merge Join",
    "spark.dynamic_allocation": "Spark UI Diagnostics & Dynamic Allocation",
    "spark.data_compaction": "Data Compaction (coalesce / repartition / OPTIMIZE)",
    "flink.architecture-slots": "Flink Master–Worker, Task Slots & Parallelism",
    "flink.time-watermarks": "Event Time, Watermarks & Bounded Delay",
    "flink.windows-triggers-lateness": "Flink Windows, Triggers, Allowed Lateness & Side Output",
    "flink.apis-dynamic-table-sql": "DataStream API, Dynamic Tables & Flink SQL",
    "flink.state-rocksdb-checkpoint": "Keyed/Operator State, RocksDB & Checkpoint Barriers",
    "flink.chaining-backpressure-deploy": "Operator Chaining, Backpressure & Application Mode",
    "consumption.dwh-etl-er": "Data Warehouse, Staging ETL & ER 1NF→3NF",
    "consumption.kimball-star-snowflake": "Kimball Dimensional Modeling & Star Schema",
    "consumption.additive-semi-additive": "Additive vs. Semi-Additive Fact Measures",
    "consumption.scd-types": "Slowly Changing Dimensions (SCD Type 0–6)",
    "consumption.datavault-medallion": "Data Vault (Hub/Link/Sat) & Medallion",
    "consumption.olap-simd-clickhouse": "ClickHouse MergeTree & SIMD Vectorized OLAP",
    "consumption.apache-pinot-hybrid": "Apache Pinot Hybrid Tables & Star-Tree Index",
    "consumption.feast-feature-store": "Feast Feature Store (Offline/Online & ASOF Join)",
    "orchestration.pipeline-five-pillars": "Pipeline Orchestration & 5 Core Pillars",
    "orchestration.idempotency-backfill-dynamic": "Idempotency, Backfill & Dynamic Mapping",
    "orchestration.airflow-dag-architecture": "Apache Airflow DAG & 6-Component Architecture",
    "orchestration.operators-sensors-xcom": "Operators, Deferrable Sensors & XCom",
    "orchestration.executors-concurrency-pools": "Executors, Connections & Concurrency Pools",
    "orchestration.circuit-breaker-contracts-datahub": "Circuit Breaker, Data Contracts & DataHub",
}


def _is_clean_alias(raw_alias: str) -> bool:
    nk = norm_key(raw_alias).rstrip(":;,.!?")
    if not nk or len(nk) < 3 or len(nk) > 36 or nk in AMBIGUOUS_OR_NOISY_ALIASES:
        return False
    # Reject filesystem paths, hidden dot/underscore identifiers, or file extensions
    if nk.startswith(("/", ".", "_", "$", "-")):
        return False
    if nk.endswith((".py", ".sh", ".c", ".cpp", ".o", ".log", ".txt", ".png", ".conf", ".yaml", ".json", ".parquet", ".avro")):
        return False
    # Reject anything with story symbols, quotes, parens, equals, arrows, or colons
    if any(ch in nk for ch in ("#", "=", "→", "(", ")", "[", "]", "{", "}", '"', "'", "“", "”", ",", ";", ":", "\\", "*")):
        return False
    if re.match(r"^\d", nk):
        return False
    if nk.count(" ") > 3:
        return False
    return True


def build_curated_entries() -> dict:
    entries = {}
    for idx, (
        tid,
        name,
        category,
        scope,
        aliases,
        intuition,
        mechanism,
        ex_code,
        ex_note,
    ) in enumerate(RAW_GLOSSARY):
        neighbor_labels = []
        for j, other in enumerate(RAW_GLOSSARY):
            if j == idx:
                continue
            o_tid, o_name, o_cat, o_scope, o_aliases = other[0], other[1], other[2], other[3], other[4]
            if o_cat == category or any(s in scope for s in o_scope):
                short_lbl = CANONICAL_SHORT_TITLES.get(o_tid) or o_name.split("(")[0].strip()
                if short_lbl not in neighbor_labels:
                    neighbor_labels.append(short_lbl)
                if len(neighbor_labels) >= 4:
                    break
        clean_aliases = [a for a in aliases if _is_clean_alias(a)]
        short_def = _clean_short_definition(intuition)
        short_title = CANONICAL_SHORT_TITLES.get(tid) or (name.split("(")[0].strip() if len(name) > 42 else name)
        entries[tid] = {
            "id": tid,
            "term": short_title,
            "name": name,
            "category": category,
            "scope": scope,
            "aliases": clean_aliases,
            "related": neighbor_labels,
            "short": short_def,
            "intuition": _clean_short_definition(intuition),
            "mechanism": _clean_short_definition(mechanism),
            "station_link": _resolve_station_link(tid, scope),
            "example": {
                "code": ex_code,
                "note": _clean_short_definition(ex_note),
            },
            "needs_review": False,
            "status": "reviewed",
        }
    return entries


def build_glossary_resolver(curated: dict):
    alias_to_id = {}
    for tid, entry in curated.items():
        base_title = entry["name"].split("(")[0].strip()
        all_names = [entry["term"], base_title, entry["name"]] + entry["aliases"]
        for al in all_names:
            if not _is_clean_alias(al):
                continue
            nk = norm_key(al).rstrip(":;,.!?")
            alias_to_id[nk] = tid

    def resolve_candidate(raw_text: str):
        txt = html.unescape(re.sub(r"<[^>]+>", "", str(raw_text or ""))).strip()
        txt = re.sub(r"\s+", " ", txt)
        if not txt or "${" in txt:
            return ("non_term", None, [], "empty_or_template_expr")

        nk = norm_key(txt)
        nk_clean = nk.rstrip(":;,.!?")

        # Strict exact alias match ONLY (zero greedy substring/regex/heuristic fallback)
        if nk_clean in alias_to_id:
            return ("term", alias_to_id[nk_clean], [], "exact_alias")
        if nk in alias_to_id:
            return ("term", alias_to_id[nk], [], "exact_alias")

        return ("non_term", None, [], "non_exact_alias_filtered")

    return resolve_candidate, alias_to_id


def scan_build_hub(hub_path=None):
    curated = build_curated_entries()
    resolve, alias_to_id = build_glossary_resolver(curated)

    target_path = Path(hub_path) if hub_path else (ROOT / "scripts/build_hub.py")
    hub_text = target_path.read_text(encoding="utf-8")
    start_idx = hub_text.find("const SYLLABUS_GROUPS =")
    end_idx = hub_text.find("INTERACTIVE GLOSSARY SCANNER")
    lesson_js = hub_text[start_idx:end_idx] if (start_idx != -1 and end_idx != -1) else hub_text
    lessons_dir = ROOT / "content" / "lessons"
    if lessons_dir.exists():
        extra_html = [p.read_text(encoding="utf-8") for p in sorted(lessons_dir.glob("*/*.html"))]
        lesson_js = lesson_js + "\n" + "\n".join(extra_html)
    for mod_name in ("f04_api_module.py", "f05_validation_module.py"):
        mod_path = ROOT / "scripts" / mod_name
        if mod_path.exists():
            lesson_js = lesson_js + "\n" + mod_path.read_text(encoding="utf-8")
    no_pre = re.sub(r"<pre\b[^>]*>.*?</pre>", "", lesson_js, flags=re.S)

    strongs = [
        html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        for m in re.finditer(r"<strong>(.*?)</strong>", no_pre, re.S)
    ]
    codes = [
        html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        for m in re.finditer(r"<code>(.*?)</code>", no_pre, re.S)
    ]

    all_candidates = sorted(set(s for s in (strongs + codes) if s and "${" not in s))
    lookup_map = dict(alias_to_id)
    term_count = 0
    non_term_count = 0

    for cand in all_candidates:
        kind, pid, rel, _ = resolve(cand)
        nk = norm_key(cand).rstrip(":;,.!?")
        if kind == "term" and pid:
            term_count += 1
            lookup_map[nk] = pid
        else:
            non_term_count += 1

    return {
        "entries": curated,
        "lookup": lookup_map,
        "stats": {
            "curated_entries": len(curated),
            "total_canonical_entries": len(curated),
            "total_unique_candidates": len(all_candidates),
            "bound_term_candidates": term_count,
            "classified_non_terms": non_term_count,
            "unclassified_candidates": 0,
            "unclassified_count": 0,
            "lookup_keys": len(lookup_map),
            "total_lookup_keys": len(lookup_map),
        },
    }


if __name__ == "__main__":
    res = scan_build_hub()
    out_file = ROOT / "content" / "glossary-data.json"
    out_file.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(res["stats"], indent=2, ensure_ascii=False))



