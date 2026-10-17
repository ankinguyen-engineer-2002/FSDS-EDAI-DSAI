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
        "container.infra-vm-vs-container": "#/F06/1/container-1-1",
        "container.linux-namespaces-cgroups": "#/F06/2/container-2-1",
        "container.overlayfs-seccomp": "#/F06/2/container-2-3",
        "container.oci-runtime-stack": "#/F06/3/container-3-2",
        "container.kubernetes-orchestration": "#/F06/4/container-4-2",
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
    if prefix == "db":
        return "#/F03/1"
    if prefix == "container":
        return "#/F06/1"
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
    "container.infra-vm-vs-container": "Hardware Virtualization (VM) vs. OS Containers",
    "container.linux-namespaces-cgroups": "Linux Namespaces & Control Groups (cgroups v2)",
    "container.overlayfs-seccomp": "OverlayFS Union Mount & Seccomp / Capabilities",
    "container.oci-runtime-stack": "OCI Runtime Stack (containerd → shim → runc)",
    "container.kubernetes-orchestration": "Kubernetes Control Plane & Worker Architecture",
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



