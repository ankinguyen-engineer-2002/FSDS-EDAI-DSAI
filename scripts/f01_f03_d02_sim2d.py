#!/usr/bin/env python3
"""
2D Animated SVG Simulators (Claude Academy CDS Theme-Aware `--sim-*`)
for F01 (Linux Fundamentals), F03 (Database Fundamentals), and D02 (Storage Layer).
"""

LINUX_SIM2D_JS = r"""
  /* ==========================================================================
     INTERACTIVE 2D SIMULATOR FOR F01 (LINUX FUNDAMENTALS)
     ========================================================================== */
  const LINUX2D_SLIDES = [
    {
      chapter: "Chặng 1 · Kernel Ring 0 & System Call",
      analogy: "Cửa Sổ Giao Dịch Hợp Pháp Duy Nhất",
      title: "Kiến Trúc 3 Tầng GNU/Linux: Từ Lệnh Gõ Trên Bash (Ring 3) Qua System Call Xuống Linux Kernel (Ring 0)",
      leadTitle: "Chiến dịch grep ERROR /var/log/app.log đi qua ranh giới bảo mật phần cứng",
      leadStory: "Khi kỹ sư gõ lệnh grep ERROR /var/log/app.log, tiến trình grep chạy ở User Space (Ring 3) bị phần cứng CPU cấm chạm trực tiếp vào ổ SSD. Nó bắt buộc phải gọi System Call (openat, read, write) để chuyển ngữ cảnh xuống Linux Kernel (Ring 0).",
      keypoints: [
        "1. Bash Shell (fork + execve): Shell nhân bản tiến trình con bằng fork() và nạp mã máy /bin/grep lên RAM bằng execve().",
        "2. Ranh giới Ring 3 ↔ Ring 0: Mọi truy cập File, RAM, Network đều phải đi qua cổng kiểm soát quyền hạn của System Call.",
        "3. Page Cache & VFS: Kernel kiểm tra quyền trên Inode, đọc khối dữ liệu từ SSD lên Page Cache rồi trả về cho bộ đệm của grep."
      ],
      verdict: "Chuẩn vận hành Production: Dùng strace -e openat,read,write để bắt mạch chính xác từng System Call khi tiến trình bị treo I/O.",
      simMode: "syscall_ring"
    },
    {
      chapter: "Chặng 2 · Hồ Sơ Process & Cây Thư Mục /",
      analogy: "Chứng Minh Thư 5 Thuộc Tính & Cửa Sổ RAM /proc",
      title: "Giải Phẫu Hồ Sơ Căn Cước Process (task_struct) & Cây Thư Mục Hợp Nhất FHS (/etc, /var/log, /proc)",
      leadTitle: "Tại sao lệnh chạy tay trên SSH thì mượt nhưng đưa vào tự động lại báo lỗi?",
      leadStory: "Mỗi Process trong Kernel được cấp một cấu trúc task_struct gồm 5 thuộc tính sống còn: PID, UID/GID, Working Directory (cwd), Environment ($PATH) và bảng Open Files (FD 0, 1, 2...). Toàn bộ thông số này được Kernel phơi bày trực tiếp dưới dạng file ảo trong /proc/<PID> tốn 0 MB ổ cứng.",
      keypoints: [
        "1. Năm thuộc tính task_struct: Sai lệch CWD hoặc thiếu /usr/local/bin trong $PATH là thủ phạm số 1 gây lỗi No such file / command not found.",
        "2. Cây thư mục FHS duy nhất bắt đầu từ /: /etc chứa cấu hình văn bản, /var/log chứa nhật ký vận hành, /bin & /usr/bin chứa công cụ thực thi.",
        "3. Hệ thống file ảo /proc (procfs): Đọc /proc/cpuinfo, /proc/meminfo hay /proc/PID/fd là đọc thẳng vào cấu trúc dữ liệu trên RAM của Kernel."
      ],
      verdict: "Quy tắc bất biến: Luôn kiểm tra ls -l /proc/$$/fd và echo $PATH khi chẩn đoán sự cố môi trường thực thi trên Linux Server.",
      simMode: "process_id_fhs"
    },
    {
      chapter: "Chặng 2 · Inode, Quyền rwx & Bẫy Disk Full",
      analogy: "Danh Bạ Thư Mục vs. Thẻ Căn Cước Inode",
      title: "Giải Phẫu Inode, Cơ Học mv / rm (unlink) & Cạm Bẫy Kinh Điển Disk Full 100% Khi Xóa File Đang Mở",
      leadTitle: "Tại sao vừa chạy rm /var/log/app.log nặng 50 GB mà df -h vẫn báo đầy đĩa 100%?",
      leadStory: "Trên Linux, Inode lưu toàn bộ siêu dữ liệu (kích thước, quyền rwx, tọa độ khối đĩa) NGOẠI TRỪ tên file! Thư mục chỉ là bảng danh bạ nối Tên_File → Số_Inode. Lệnh rm chỉ xóa dòng tên trong danh bạ (unlink), còn các khối đĩa chỉ được giải phóng khi Link Count = 0 VÀ Open FD Count = 0.",
      keypoints: [
        "1. Đổi tên/di chuyển mv cùng ổ đĩa là O(1): Chỉ cập nhật con trỏ tên trong Directory Entry, không chép lại bất kỳ byte dữ liệu nào.",
        "2. Bẫy xóa file log đang mở (Orphaned Inode): Nếu tiến trình app vẫn đang mở app.log (FD Count > 0), chạy rm không giải phóng 1 byte đĩa nào!",
        "3. Phác đồ giải cứu không cần khởi động lại app: Dùng truncate -s 0 /var/log/app.log (hoặc :> /var/log/app.log) để cắt dung lượng về 0 ngay trên Inode."
      ],
      verdict: "Tuyệt đối không dùng rm xóa thẳng file log đang được ghi bởi tiến trình sống — hãy dùng truncate -s 0 hoặc logrotate copytruncate.",
      simMode: "inode_unlink"
    },
    {
      chapter: "Chặng 3 · IPC 3 Cổng 0/1/2 & Kernel Pipe",
      analogy: "Đường Ống Nước Trên RAM 64 KB & Bẻ Khớp dup2()",
      title: "Giao Tiếp Đa Tiến Trình (IPC): Ba Cổng stdin(0) / stdout(1) / stderr(2), Kernel Pipe (|) & Điều Hướng 2>&1",
      leadTitle: "Ghép chuỗi grep ERROR app.log | awk | sort mà không tốn 1 byte ghi tạm xuống ổ đĩa",
      leadStory: "Mọi tiến trình sinh ra đều có sẵn 3 cổng tiêu chuẩn: 0 (stdin), 1 (stdout) và 2 (stderr). Khi nối bằng ký tự Pipe (|), Kernel cấp một bộ đệm vòng (Ring Buffer 64 KB) ngay trên RAM để luồng byte từ cổng 1 của tiến trình trước chảy thẳng sang cổng 0 của tiến trình sau.",
      keypoints: [
        "1. Tách bạch stdout(1) và stderr(2): Thông báo lỗi đi qua cổng 2 để không làm bẩn dữ liệu đầu vào của tiến trình đứng sau dấu Pipe.",
        "2. Bộ đệm Kernel Pipe 64 KB: Hai tiến trình chạy đồng thời (concurrenly); nếu bộ đệm đầy, Kernel tự động tạm dừng (block) bên ghi chờ bên đọc.",
        "3. Điều hướng bằng dup2(): Cú pháp > out.log 2>&1 bẻ cả cổng 1 và cổng 2 cùng trỏ vào file nhật ký để không bỏ sót lỗi khi chạy ngầm."
      ],
      verdict: "Thứ tự chuẩn POSIX: Luôn viết > file.log 2>&1 (mở file cho cổng 1 trước, rồi mới chép cổng 1 sang cổng 2).",
      simMode: "fd_pipe_ipc"
    },
    {
      chapter: "Chặng 4 · GCC 4 Pha & Makefile Incremental",
      analogy: "Quản Đốc Công Trường So Sánh Nhãn Thời Gian mtime",
      title: "Dây Chuyền Biên Dịch GCC (.c → .i → .s → .o → Binary) & Cơ Học Makefile Chỉ Dịch Lại File Vừa Sửa",
      leadTitle: "Làm sao biên dịch dự án 500 file C trong 0.8 giây thay vì chờ 15 phút mỗi lần sửa 1 dòng?",
      leadStory: "Trình biên dịch GCC biến mã nguồn C thành file thực thi qua 4 bước (Preprocessing, Compilation, Assembly, Linking). Công cụ GNU Make đọc đồ thị phụ thuộc trong Makefile và so sánh nhãn thời gian mtime trên Inode giữa Target và Prerequisites để chỉ biên dịch lại đúng nhánh vừa thay đổi.",
      keypoints: [
        "1. Tách rời Compile (-c ra file .o) và Link: Giúp tái sử dụng các file đối tượng (.o) không bị thay đổi mã nguồn.",
        "2. Thuật toán so sánh mtime của Make: Nếu mtime(prerequisite) > mtime(target) hoặc target chưa tồn tại, Make mới kích hoạt dòng lệnh Recipe.",
        "3. Luật cứng của Makefile: Dòng lệnh Recipe bên dưới Target bắt buộc phải thụt đầu dòng bằng đúng ký tự phím TAB (ASCII 0x09)."
      ],
      verdict: "Tự động hóa build: Kết hợp Makefile cho cả C/C++ lẫn các đường ống dữ liệu có phụ thuộc tệp đầu vào/đầu ra.",
      simMode: "gcc_makefile"
    },
    {
      chapter: "Chặng 4 · Bash Script & Cronjob 24/7",
      analogy: "Đồng Hồ Báo Thức Hạt Nhân Quét Mỗi 60 Giây",
      title: "Tự Động Hóa Vận Hành 24/7 Với Bash Script (Shebang, Exit Code $?) & Tiến Trình Ngầm Cron Daemon (crond)",
      leadTitle: "Hóa giải 3 cạm bẫy kinh điển khiến Cronjob chạy lúc 03:00 sáng chết câm lặng",
      leadStory: "Tiến trình nền crond thức dậy mỗi 60 giây để kiểm tra bảng hẹn giờ crontab (Phút Giờ Ngày Tháng Thứ). Vì crond khởi chạy script trong một môi trường tối giản (không có biến môi trường cá nhân, đứng ở /home/user, không có màn hình Terminal), 90% lỗi tự động hóa đến từ 3 cạm bẫy môi trường.",
      keypoints: [
        "1. Bẫy #1 — Quên Shebang & Quyền thực thi: Luôn mở đầu script bằng #!/bin/bash và cấp quyền chmod +x (hoặc 0755).",
        "2. Bẫy #2 — Đường dẫn tương đối & $PATH hẹp: Trong script và crontab bắt buộc dùng đường dẫn tuyệt đối (/var/log/app.log, /usr/bin/python3).",
        "3. Bẫy #3 — Nuốt lỗi câm lặng: Luôn kiểm tra mã thoát $? (0 = OK, != 0 = Lỗi) và gom toàn bộ đầu ra vào >> /var/log/cron_backup.log 2>&1."
      ],
      verdict: "Chuẩn Production: Mọi Cronjob phải ghi log đầy đủ kèm timestamp, kiểm tra mã thoát $? và dùng đường dẫn tuyệt đối 100%.",
      simMode: "cron_automation"
    }
  ];

  let lnx2dCurrentSlide = 0;
  const lnx2dState = {
    ringMode: "syscall_trap",
    fhsMode: "task_struct",
    inodeMode: "rm_open_trap",
    pipeMode: "pipe_ram",
    makeMode: "incremental_mtime",
    cronMode: "prod_hardened"
  };

  function buildLinux2DSimulatorHtml() {
    return `
      <div class="infra2d-wrap" id="lnx2dWidgetRoot">
        <div class="infra2d-header">
          <div class="infra2d-brand">
            <div class="infra2d-brand-icon">2D</div>
            <div>
              <div class="infra2d-brand-badges">
                <span class="infra2d-tag">Cắt Lớp Hạt Nhân &amp; Tiến Trình Linux 2D</span>
                <span class="infra2d-chapter" id="lnx2dChapterBadge">Chặng 1 · Kernel Ring 0 &amp; System Call</span>
              </div>
              <h4 class="infra2d-title-bar">Phòng Thí Nghiệm Tương Tác F01: Hành Trình Lệnh grep ERROR /var/log/app.log Từ Shell Xuống Kernel</h4>
            </div>
          </div>
          <div class="infra2d-dots" id="lnx2dDots"></div>
          <button type="button" class="infra2d-btn" onclick="toggleLinux2DSummaryModal()">Bảng Tóm Tắt Thông Số</button>
        </div>

        <div id="lnx2dSummaryDrawer" style="display:none;padding:14px 16px;background:var(--sim-canvas);border-bottom:1px solid var(--sim-border);">
          <div style="padding:10px 12px;border-radius:8px;background:var(--sim-flow-soft);border:1px solid color-mix(in oklab, var(--sim-flow) 35%, transparent);font-size:12.5px;color:var(--sim-flow);margin-bottom:10px;">
            <strong>Chuẩn kiến trúc F01 (Linux Fundamentals):</strong> Hiểu rõ ranh giới <strong>User Space (Ring 3) ↔ Kernel Space (Ring 0)</strong>, quản trị <strong>Inode / File Descriptors (0, 1, 2)</strong> và đóng gói dây chuyền tự động hóa <strong>Bash + Make + Cronjob</strong> chống lỗi câm lặng.
          </div>
          <div class="table-wrap" style="margin:0;">
            <table class="clean-table">
              <thead>
                <tr>
                  <th>Tầng Cắt Lớp</th>
                  <th>Cơ Chế Cốt Lõi</th>
                  <th>Lệnh &amp; Cấu Hình Chuẩn Production</th>
                  <th>Cạm Bẫy Sinh Tử Cần Tránh</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>1. Kernel &amp; Process</strong></td>
                  <td><code>fork() → execve() → Syscall</code></td>
                  <td><code>strace -f</code>, <code>ls -l /proc/$$/fd</code></td>
                  <td>Thiếu <code>/usr/local/bin</code> trong <code>$PATH</code> khi chạy tự động</td>
                </tr>
                <tr>
                  <td><strong>2. Inode &amp; VFS</strong></td>
                  <td><code>Directory Entry → Inode → Blocks</code></td>
                  <td><code>stat app.log</code>, <code>truncate -s 0 app.log</code></td>
                  <td>Chạy <code>rm</code> trên file log đang mở gây <code>Disk Full 100%</code></td>
                </tr>
                <tr>
                  <td><strong>3. IPC &amp; Pipe</strong></td>
                  <td><code>stdin(0) / stdout(1) / stderr(2)</code></td>
                  <td><code>cmd1 | cmd2 &gt; out.log 2&gt;&amp;1</code></td>
                  <td>Quên gom <code>stderr(2)</code> làm mất dấu vết lỗi lúc nửa đêm</td>
                </tr>
                <tr>
                  <td><strong>4. Build &amp; Cron</strong></td>
                  <td><code>Makefile mtime</code> + <code>crond 60s</code></td>
                  <td><code>#!/bin/bash</code>, <code>chmod 755</code>, <code>echo $?</code></td>
                  <td>Dùng Space thay vì <code>TAB</code> trong Makefile hoặc dùng đường dẫn tương đối</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="infra2d-grid">
          <div class="infra2d-col-left">
            <div>
              <div class="infra2d-pills">
                <span class="infra2d-pill-num" id="lnx2dSlideNumPill">SLIDE 1 / 6</span>
                <span class="infra2d-pill-analogy" id="lnx2dAnalogyPill">Lát Cắt Hạt Nhân</span>
              </div>
              <h3 class="infra2d-slide-h3" id="lnx2dSlideTitle"></h3>
              <div class="infra2d-story-box">
                <div class="infra2d-avatar" title="Tiến trình grep ERROR /var/log/app.log">LNX</div>
                <div>
                  <span class="infra2d-story-title" id="lnx2dLeadTitle"></span>
                  <p class="infra2d-story-text" id="lnx2dLeadStory"></p>
                </div>
              </div>
              <div class="infra2d-keypoints" id="lnx2dKeypoints"></div>
            </div>
            <div class="infra2d-verdict" id="lnx2dVerdictBox"></div>
          </div>

          <div class="infra2d-col-right">
            <div>
              <div class="infra2d-sim-top">
                <div class="infra2d-sim-live">
                  <span class="infra2d-sim-dot"></span>
                  <span>Sơ Đồ Cắt Lớp Linux Kernel &amp; Luồng Byte Chuyển Động (Animated SVG)</span>
                </div>
                <span class="infra2d-sim-hint">Bấm các nút kịch bản bên dưới để đổi cơ chế!</span>
              </div>
              <div class="infra2d-stage" id="lnx2dSimStage" style="padding:10px;"></div>
            </div>
            <div>
              <div class="infra2d-status" id="lnx2dSimStatusText">Sẵn sàng mô phỏng.</div>
              <div class="infra2d-controls" id="lnx2dSimControls"></div>
            </div>
          </div>
        </div>

        <div class="infra2d-footer">
          <button type="button" class="infra2d-btn" id="lnx2dBtnPrev" onclick="changeLinux2DSlide(-1)">← Mô Phỏng Trước</button>
          <div class="infra2d-progress-wrap">
            <div class="infra2d-progress-track">
              <div class="infra2d-progress-fill" id="lnx2dProgressFill" style="width:16.6%;"></div>
            </div>
            <span class="infra2d-progress-label" id="lnx2dProgressLabel">Mô phỏng 1 / 6</span>
          </div>
          <button type="button" class="infra2d-btn infra2d-btn-primary" id="lnx2dBtnNext" onclick="changeLinux2DSlide(1)">Mô Phỏng Tiếp Theo →</button>
        </div>
      </div>
    `;
  }

  function toggleLinux2DSummaryModal() {
    const el = document.getElementById("lnx2dSummaryDrawer");
    if (el) el.style.display = el.style.display === "none" ? "block" : "none";
  }

  function changeLinux2DSlide(delta) {
    lnx2dCurrentSlide = (lnx2dCurrentSlide + delta + LINUX2D_SLIDES.length) % LINUX2D_SLIDES.length;
    renderLinux2DSlide();
  }

  function jumpLinux2DSlide(idx) {
    lnx2dCurrentSlide = idx;
    renderLinux2DSlide();
  }

  function renderLinux2DSlide() {
    const s = LINUX2D_SLIDES[lnx2dCurrentSlide];
    if (!s) return;
    const chEl = document.getElementById("lnx2dChapterBadge");
    if (!chEl) return;
    chEl.textContent = s.chapter;
    document.getElementById("lnx2dSlideNumPill").textContent = `SLIDE ${lnx2dCurrentSlide + 1} / ${LINUX2D_SLIDES.length}`;
    document.getElementById("lnx2dAnalogyPill").textContent = s.analogy;
    document.getElementById("lnx2dSlideTitle").textContent = s.title;
    document.getElementById("lnx2dLeadTitle").textContent = s.leadTitle;
    document.getElementById("lnx2dLeadStory").textContent = s.leadStory;
    document.getElementById("lnx2dKeypoints").innerHTML = s.keypoints
      .map(kp => `<div class="infra2d-kp"><span class="infra2d-kp-dot"></span><span>${escapeHtml(kp)}</span></div>`)
      .join("");
    document.getElementById("lnx2dVerdictBox").innerHTML = `<strong>Chốt nguyên lý:</strong> ${escapeHtml(s.verdict)}`;
    document.getElementById("lnx2dDots").innerHTML = LINUX2D_SLIDES.map(
      (_, i) => `<button type="button" class="infra2d-dot ${i === lnx2dCurrentSlide ? 'active' : ''}" onclick="jumpLinux2DSlide(${i})" title="Slide ${i + 1}">${i + 1}</button>`
    ).join("");
    const pct = (((lnx2dCurrentSlide + 1) / LINUX2D_SLIDES.length) * 100).toFixed(1);
    document.getElementById("lnx2dProgressFill").style.width = `${pct}%`;
    document.getElementById("lnx2dProgressLabel").textContent = `Mô phỏng ${lnx2dCurrentSlide + 1} / ${LINUX2D_SLIDES.length}`;
    renderLinux2DInteractiveStage(s.simMode);
  }

  function renderLinux2DInteractiveStage(mode) {
    const stage = document.getElementById("lnx2dSimStage");
    const status = document.getElementById("lnx2dSimStatusText");
    const ctrls = document.getElementById("lnx2dSimControls");
    if (!stage || !status || !ctrls) return;

    if (mode === "syscall_ring") {
      const m = lnx2dState.ringMode;
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="24" y="22" width="512" height="58" rx="7" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="36" y="42" fill="var(--sim-flow)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">TẦNG 1 · USER SPACE (RING 3 — KHÔNG ĐẶC QUYỀN)</text>
          <text x="36" y="62" fill="var(--sim-ink)" font-size="9.2" font-family="var(--cds-font-mono)">${m === 'user_shell' ? 'Terminal → Bash Shell phân tích cú pháp: grep ERROR /var/log/app.log' : (m === 'fork_execve' ? 'Bash gọi fork() đẻ PID 4812 → gọi execve("/bin/grep") nạp mã máy lên RAM' : 'Process grep (PID 4812) gọi glibc read(fd=3, buf, 4096) → Lệnh CPU syscall')}</text>

          <rect x="24" y="92" width="512" height="62" rx="7" fill="var(--sim-flow-soft)" stroke="var(--sim-clay)" stroke-width="1.6"/>
          <text x="36" y="112" fill="var(--sim-clay)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">TẦNG 2 · LINUX KERNEL SPACE (RING 0 — ĐẶC QUYỀN TUYỆT ĐỐI)</text>
          <text x="36" y="132" fill="var(--sim-ink)" font-size="9.2" font-family="var(--cds-font-mono)">${m === 'user_shell' ? 'TTY Driver nhận phím gõ từ cổng SSH và chuyển cho tiến trình Bash' : (m === 'fork_execve' ? 'Scheduler cấp phát task_struct mới (PID 4812) & bảng trang bộ nhớ ảo (mm_struct)' : 'VFS kiểm tra quyền r-- trên Inode #9102 → Đọc Page Cache → Copy ra User Buffer')}</text>

          <rect x="24" y="166" width="512" height="56" rx="7" fill="var(--sim-card-alt)" stroke="var(--sim-ok)" stroke-width="1.5"/>
          <text x="36" y="186" fill="var(--sim-ok)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">TẦNG 3 · HARDWARE (CPU CORES · RAM PAGE CACHE · NVMe SSD)</text>
          <text x="36" y="206" fill="var(--sim-ink)" font-size="9.2" font-family="var(--cds-font-mono)">Khối đĩa vật lý /dev/nvme0n1 chứa nội dung tệp /var/log/app.log (DMA lên RAM)</text>

          <circle r="5" fill="var(--sim-clay)">
            <animate attributeName="cy" values="52;122;192;122;52" dur="2.6s" repeatCount="indefinite"/>
            <animate attributeName="cx" values="490;490;490;510;510" dur="2.6s" repeatCount="indefinite"/>
          </circle>
        </svg>
      `;
      status.textContent = m === "user_shell"
        ? "Bước 1 (Terminal & Shell): Người dùng gõ lệnh trên Terminal; Bash Shell đọc chuỗi văn bản và chuẩn bị khởi chạy chương trình."
        : (m === "fork_execve"
          ? "Bước 2 (Program → Process): Bash gọi fork() tạo tiến trình con và execve() nạp file nhị phân /bin/grep từ đĩa lên RAM."
          : "Bước 3 (System Call Ring 3 → Ring 0): Tiến trình grep gọi openat() và read() nhờ Kernel đọc các block của /var/log/app.log.");
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${m === 'user_shell' ? 'infra2d-btn-cyan' : ''}" onclick="lnx2dState.ringMode='user_shell';renderLinux2DInteractiveStage('syscall_ring')">1. Terminal &amp; Bash Shell</button>
        <button type="button" class="infra2d-btn ${m === 'fork_execve' ? 'infra2d-btn-amber' : ''}" onclick="lnx2dState.ringMode='fork_execve';renderLinux2DInteractiveStage('syscall_ring')">2. fork() + execve() Tạo Process</button>
        <button type="button" class="infra2d-btn ${m === 'syscall_trap' ? 'infra2d-btn-emerald' : ''}" onclick="lnx2dState.ringMode='syscall_trap';renderLinux2DInteractiveStage('syscall_ring')">3. System Call (Ring 3 ↔ Ring 0)</button>
      `;
    } else if (mode === "process_id_fhs") {
      const m = lnx2dState.fhsMode;
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="22" y="24" width="250" height="196" rx="8" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="34" y="46" fill="var(--sim-flow)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">HỒ SƠ PROCESS (task_struct)</text>
          <text x="34" y="70" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">1. PID / PPID : 4812 / 2104 (bash)</text>
          <text x="34" y="92" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">2. UID / GID  : 1000 (nam) / adm</text>
          <text x="34" y="114" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">3. Working Dir: /var/log</text>
          <text x="34" y="136" fill="${m === 'path_trap' ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">4. $PATH      : ${m === 'path_trap' ? '/usr/bin:/bin (Thiếu!)' : '/usr/local/bin:/usr/bin'}</text>
          <text x="34" y="158" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">5. Open Files : FD 0, 1, 2, 3(app.log)</text>
          <text x="34" y="188" fill="var(--sim-muted)" font-size="8.5" font-family="var(--cds-font-mono)">→ Phơi bày tại /proc/4812/* (0 MB đĩa)</text>

          <rect x="288" y="24" width="250" height="196" rx="8" fill="var(--sim-card-alt)" stroke="var(--sim-ok)" stroke-width="1.5"/>
          <text x="300" y="46" fill="var(--sim-ok)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">CÂY THƯ MỤC CHUẨN FHS (/)</text>
          <text x="300" y="70" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">├── /bin/grep       (Binary thực thi)</text>
          <text x="300" y="92" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">├── /etc/crontab    (Cấu hình văn bản)</text>
          <text x="300" y="114" fill="var(--sim-clay)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">├── /var/log/app.log (Nhật ký hệ thống)</text>
          <text x="300" y="136" fill="var(--sim-flow)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">├── /proc/4812/fd   (Cửa sổ RAM ảo)</text>
          <text x="300" y="158" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">└── /dev/null       (Hố đen thiết bị)</text>
          <text x="300" y="188" fill="var(--sim-ok)" font-size="8.5" font-weight="700" font-family="var(--cds-font-mono)">Triết lý: "Everything is a file"</text>
        </svg>
      `;
      status.textContent = m === "task_struct"
        ? "Hồ sơ căn cước 5 thuộc tính (task_struct): Quyết định quyền hạn và ngữ cảnh của mọi tiến trình đang chạy."
        : (m === "fhs_tree"
          ? "Cây thư mục hợp nhất FHS (/): Hợp nhất mọi ổ đĩa vật lý và hệ thống file ảo /proc vào một gốc / duy nhất."
          : "Bẫy môi trường $PATH: Khi thiếu /usr/local/bin trong $PATH, Shell báo command not found dù công cụ đã cài trên máy!");
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${m === 'task_struct' ? 'infra2d-btn-cyan' : ''}" onclick="lnx2dState.fhsMode='task_struct';renderLinux2DInteractiveStage('process_id_fhs')">1. Hồ Sơ 5 Thuộc Tính Process</button>
        <button type="button" class="infra2d-btn ${m === 'fhs_tree' ? 'infra2d-btn-emerald' : ''}" onclick="lnx2dState.fhsMode='fhs_tree';renderLinux2DInteractiveStage('process_id_fhs')">2. Cây Thư Mục / &amp; /proc (0 MB)</button>
        <button type="button" class="infra2d-btn ${m === 'path_trap' ? 'infra2d-btn-danger' : ''}" onclick="lnx2dState.fhsMode='path_trap';renderLinux2DInteractiveStage('process_id_fhs')">3. Giả Lập Lỗi Thiếu $PATH</button>
      `;
    } else if (mode === "inode_unlink") {
      const m = lnx2dState.inodeMode;
      const isTrap = m === "rm_open_trap";
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="22" y="30" width="155" height="140" rx="7" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="32" y="52" fill="var(--sim-flow)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">1. DIRECTORY (/var/log)</text>
          <text x="32" y="78" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">${isTrap ? '(Đã xóa tên app.log)' : 'Tên: "app.log"'}</text>
          <text x="32" y="100" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">Trỏ tới → Inode #9102</text>
          <text x="32" y="130" fill="var(--sim-muted)" font-size="8.5" font-family="var(--cds-font-mono)">${m === 'inode_mv' ? 'mv chỉ đổi tên ở đây!' : (isTrap ? 'unlink() gỡ Dentry' : 'Giữ nguyên Dentry')}</text>

          <rect x="202" y="30" width="160" height="140" rx="7" fill="${isTrap ? 'var(--sim-warn-soft)' : 'var(--sim-card)'}" stroke="${isTrap ? 'var(--sim-danger)' : 'var(--sim-clay)'}" stroke-width="1.6"/>
          <text x="212" y="52" fill="${isTrap ? 'var(--sim-danger)' : 'var(--sim-clay)'}" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">2. INODE #9102</text>
          <text x="212" y="76" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">Size: ${m === 'truncate_rescue' ? '0 Bytes (Đã cắt!)' : '50 GB'}</text>
          <text x="212" y="96" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">Link Count: ${isTrap ? '0 (Đã rm)' : '1'}</text>
          <text x="212" y="116" fill="${isTrap ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">Open FD Count: 1 (app)</text>
          <text x="212" y="140" fill="var(--sim-ink)" font-size="8.5" font-family="var(--cds-font-mono)">Quyền: -rw-r----- (0640)</text>

          <rect x="386" y="30" width="152" height="140" rx="7" fill="var(--sim-card-alt)" stroke="${isTrap ? 'var(--sim-danger)' : 'var(--sim-ok)'}" stroke-width="1.5"/>
          <text x="396" y="52" fill="${isTrap ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">3. KHỐI ĐĨA VẬT LÝ</text>
          <text x="396" y="80" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">${isTrap ? '50 GB VẪN BỊ GIỮ!' : (m === 'truncate_rescue' ? 'Đã giải phóng 50 GB!' : 'Đang lưu các block')}</text>
          <text x="396" y="104" fill="${isTrap ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">${isTrap ? 'df -h: 100% FULL!' : 'df -h: 18% Khỏe mạnh'}</text>

          <rect x="22" y="186" width="516" height="36" rx="6" fill="var(--sim-card-alt)" stroke="var(--sim-border)"/>
          <text x="34" y="208" fill="var(--sim-ink)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">${isTrap ? 'Bẫy kinh điển: rm xóa tên file nhưng Open FD Count = 1 nên Kernel KHÔNG giải phóng 50 GB đĩa!' : (m === 'truncate_rescue' ? 'Giải cứu chuẩn: truncate -s 0 /var/log/app.log xả sạch 50 GB khối đĩa ngay lập tức!' : 'Lệnh mv trong cùng phân vùng đĩa chỉ sửa bảng danh bạ Thư mục (tức thì O(1)).')}</text>
        </svg>
      `;
      status.textContent = isTrap
        ? "Cảnh báo Disk Full 100%: Chạy rm trên file log đang được tiến trình mở khiến file biến mất khỏi ls nhưng vẫn ngốn trọn 50 GB ổ cứng!"
        : (m === "truncate_rescue"
          ? "Phác đồ chuẩn: Dùng truncate -s 0 /var/log/app.log để thu hồi 50 GB dung lượng đĩa tức thì mà không cần tắt tiến trình."
          : "Cơ học Inode: Thư mục chỉ lưu ánh xạ Tên → Số Inode, giúp thao tác đổi tên/di chuyển mv hoàn tất tức thì.");
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${m === 'inode_mv' ? 'infra2d-btn-cyan' : ''}" onclick="lnx2dState.inodeMode='inode_mv';renderLinux2DInteractiveStage('inode_unlink')">1. Cấu Trúc Dentry → Inode (mv O(1))</button>
        <button type="button" class="infra2d-btn ${isTrap ? 'infra2d-btn-danger' : ''}" onclick="lnx2dState.inodeMode='rm_open_trap';renderLinux2DInteractiveStage('inode_unlink')">2. Bẫy rm File Đang Mở (Disk Full 100%)</button>
        <button type="button" class="infra2d-btn ${m === 'truncate_rescue' ? 'infra2d-btn-emerald' : ''}" onclick="lnx2dState.inodeMode='truncate_rescue';renderLinux2DInteractiveStage('inode_unlink')">3. Giải Cứu Bằng truncate -s 0</button>
      `;
    } else if (mode === "fd_pipe_ipc") {
      const m = lnx2dState.pipeMode;
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="24" y="42" width="150" height="120" rx="7" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="34" y="64" fill="var(--sim-flow)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">PROCESS 1 (grep)</text>
          <text x="34" y="88" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">FD 0 (stdin) : app.log</text>
          <text x="34" y="110" fill="var(--sim-ok)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">FD 1 (stdout): Dòng khớp</text>
          <text x="34" y="132" fill="var(--sim-danger)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">FD 2 (stderr): Lỗi quyền</text>

          <rect x="204" y="42" width="152" height="120" rx="7" fill="var(--sim-flow-soft)" stroke="var(--sim-clay)" stroke-width="1.6"/>
          <text x="214" y="64" fill="var(--sim-clay)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">${m === 'redirect_dup2' ? 'BẢNG FD SAU dup2()' : 'KERNEL PIPE (64 KB)'}</text>
          <text x="214" y="92" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">${m === 'redirect_dup2' ? 'FD 1 ──┐ Cùng trỏ vào' : 'Ring Buffer trên RAM'}</text>
          <text x="214" y="114" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">${m === 'redirect_dup2' ? 'FD 2 ──┴► report.txt' : '0 MB ghi tạm xuống đĩa!'}</text>
          <text x="214" y="138" fill="var(--sim-ok)" font-size="8.5" font-weight="700" font-family="var(--cds-font-mono)">${m === 'stderr_leak' ? 'FD 2 rẽ riêng ra màn hình' : 'Truyền luồng byte tức thì'}</text>

          <rect x="384" y="42" width="152" height="120" rx="7" fill="var(--sim-card-alt)" stroke="var(--sim-ok)" stroke-width="1.5"/>
          <text x="394" y="64" fill="var(--sim-ok)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">${m === 'redirect_dup2' ? 'FILE ĐÍCH (report.txt)' : 'PROCESS 2 (wc -l)'}</text>
          <text x="394" y="92" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">${m === 'redirect_dup2' ? 'Lưu trọn cả kết quả' : 'FD 0 (stdin) ← Pipe'}</text>
          <text x="394" y="114" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">${m === 'redirect_dup2' ? 'lẫn thông báo lỗi!' : 'Đếm số dòng ERROR'}</text>

          <circle r="4.5" fill="var(--sim-flow)">
            <animate attributeName="cx" values="174;280;384" dur="1.8s" repeatCount="indefinite"/>
            <animate attributeName="cy" values="102;102;102" dur="1.8s" repeatCount="indefinite"/>
          </circle>
        </svg>
      `;
      status.textContent = m === "pipe_ram"
        ? "Đường ống Kernel Pipe (|): Nối cổng stdout(1) của grep sang stdin(0) của wc -l qua bộ đệm RAM 64 KB trong Kernel."
        : (m === "stderr_leak"
          ? "Tách luồng lỗi stderr(2): Lỗi Permission denied đi ra cổng 2 riêng biệt để không làm sai lệch bộ đếm của wc -l."
          : "Hợp lưu bằng dup2() (> report.txt 2>&1): Bẻ cả cổng 1 và cổng 2 cùng ghi vào tệp nhật ký đích.");
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${m === 'pipe_ram' ? 'infra2d-btn-emerald' : ''}" onclick="lnx2dState.pipeMode='pipe_ram';renderLinux2DInteractiveStage('fd_pipe_ipc')">1. Kernel Pipe Bộ Đệm RAM 64KB</button>
        <button type="button" class="infra2d-btn ${m === 'stderr_leak' ? 'infra2d-btn-amber' : ''}" onclick="lnx2dState.pipeMode='stderr_leak';renderLinux2DInteractiveStage('fd_pipe_ipc')">2. Tách Luồng Lỗi stderr(2)</button>
        <button type="button" class="infra2d-btn ${m === 'redirect_dup2' ? 'infra2d-btn-cyan' : ''}" onclick="lnx2dState.pipeMode='redirect_dup2';renderLinux2DInteractiveStage('fd_pipe_ipc')">3. Hợp Lưu &gt; report.txt 2&gt;&amp;1</button>
      `;
    } else if (mode === "gcc_makefile") {
      const m = lnx2dState.makeMode;
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="24" y="36" width="155" height="130" rx="7" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="34" y="58" fill="var(--sim-flow)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">MÃ NGUỒN (.c / .h)</text>
          <text x="34" y="84" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">main.c   (mtime 10:00)</text>
          <text x="34" y="106" fill="var(--sim-clay)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">parser.c (mtime 10:05!)</text>
          <text x="34" y="128" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">utils.c  (mtime 10:00)</text>

          <rect x="202" y="36" width="156" height="130" rx="7" fill="var(--sim-flow-soft)" stroke="${m === 'tab_trap' ? 'var(--sim-danger)' : 'var(--sim-clay)'}" stroke-width="1.6"/>
          <text x="212" y="58" fill="${m === 'tab_trap' ? 'var(--sim-danger)' : 'var(--sim-clay)'}" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">GNU MAKE &amp; GCC -c</text>
          <text x="212" y="84" fill="var(--sim-ok)" font-size="9" font-family="var(--cds-font-mono)">${m === 'full_build' ? 'Dịch lại main.o' : 'Giữ nguyên main.o'}</text>
          <text x="212" y="106" fill="${m === 'tab_trap' ? 'var(--sim-danger)' : 'var(--sim-clay)'}" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">${m === 'tab_trap' ? 'LỖI: missing separator!' : 'Dịch lại parser.o!'}</text>
          <text x="212" y="128" fill="var(--sim-ok)" font-size="9" font-family="var(--cds-font-mono)">${m === 'full_build' ? 'Dịch lại utils.o' : 'Giữ nguyên utils.o'}</text>

          <rect x="382" y="36" width="154" height="130" rx="7" fill="var(--sim-card-alt)" stroke="var(--sim-ok)" stroke-width="1.5"/>
          <text x="392" y="58" fill="var(--sim-ok)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">LINKER (ELF BINARY)</text>
          <text x="392" y="88" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">Gộp *.o → log_analyzer</text>
          <text x="392" y="112" fill="var(--sim-ok)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">Thời gian: ${m === 'full_build' ? '14.2 giây' : (m === 'tab_trap' ? 'Dừng khẩn cấp!' : '0.4 giây (Incremental)')}</text>
        </svg>
      `;
      status.textContent = m === "incremental_mtime"
        ? "Incremental Build với Makefile: Chỉ file parser.c có mtime mới hơn parser.o mới bị GCC dịch lại, tiết kiệm 95% thời gian."
        : (m === "full_build"
          ? "Full Build (4 pha GCC): Preprocessing (.i) → Compilation (.s) → Assembly (.o) → Linking tạo file nhị phân ELF."
          : "Lỗi kinh điển trong Makefile: Dùng 4 dấu cách thay vì ký tự phím TAB ở dòng Recipe gây lỗi 'Makefile:4: *** missing separator. Stop.'");
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${m === 'incremental_mtime' ? 'infra2d-btn-emerald' : ''}" onclick="lnx2dState.makeMode='incremental_mtime';renderLinux2DInteractiveStage('gcc_makefile')">1. Incremental Build (So Sánh mtime)</button>
        <button type="button" class="infra2d-btn ${m === 'full_build' ? 'infra2d-btn-cyan' : ''}" onclick="lnx2dState.makeMode='full_build';renderLinux2DInteractiveStage('gcc_makefile')">2. GCC 4 Pha Full Build</button>
        <button type="button" class="infra2d-btn ${m === 'tab_trap' ? 'infra2d-btn-danger' : ''}" onclick="lnx2dState.makeMode='tab_trap';renderLinux2DInteractiveStage('gcc_makefile')">3. Bẫy Phím TAB Trong Makefile</button>
      `;
    } else {
      const m = lnx2dState.cronMode;
      const isTrap = m === "cron_3_traps";
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="24" y="34" width="156" height="142" rx="7" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="34" y="56" fill="var(--sim-flow)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">CRON DAEMON (crond)</text>
          <text x="34" y="82" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">Thức dậy mỗi 60 giây</text>
          <text x="34" y="104" fill="var(--sim-clay)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">Lịch: 0 3 * * *</text>
          <text x="34" y="126" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">(03:00 sáng mỗi ngày)</text>

          <rect x="202" y="34" width="164" height="142" rx="7" fill="${isTrap ? 'var(--sim-warn-soft)' : 'var(--sim-card)'}" stroke="${isTrap ? 'var(--sim-danger)' : 'var(--sim-ok)'}" stroke-width="1.6"/>
          <text x="212" y="56" fill="${isTrap ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">SCRIPT (backup.sh)</text>
          <text x="212" y="82" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">${isTrap ? '1. Quên chmod +x' : '1. #!/bin/bash + 0755'}</text>
          <text x="212" y="104" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">${isTrap ? '2. Dùng ./app.log (Sai!)' : '2. /var/log/app.log'}</text>
          <text x="212" y="126" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">${isTrap ? '3. Không ghi log 2>&1' : '3. Kiểm tra if [ $? -eq 0 ]'}</text>

          <rect x="388" y="34" width="148" height="142" rx="7" fill="var(--sim-card-alt)" stroke="${isTrap ? 'var(--sim-danger)' : 'var(--sim-ok)'}" stroke-width="1.5"/>
          <text x="398" y="56" fill="${isTrap ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">KẾT QUẢ LÚC 03:00</text>
          <text x="398" y="86" fill="${isTrap ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">${isTrap ? 'CHẾT CÂM LẶNG!' : 'EXIT CODE $? = 0 [OK]'}</text>
          <text x="398" y="110" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">${isTrap ? 'Không có bản backup' : 'Đã lưu backup.log'}</text>
        </svg>
      `;
      status.textContent = isTrap
        ? "3 Cạm bẫy Cronjob: Thiếu quyền thực thi chmod +x, viết đường dẫn tương đối ./app.log và quên điều hướng >> backup.log 2>&1."
        : "Chuẩn Production 24/7: Khai báo #!/bin/bash, cấp quyền 0755, dùng đường dẫn tuyệt đối 100% và kiểm tra mã thoát $?";
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${m === 'prod_hardened' ? 'infra2d-btn-emerald' : ''}" onclick="lnx2dState.cronMode='prod_hardened';renderLinux2DInteractiveStage('cron_automation')">1. Cronjob Chuẩn Production (03:00 AM)</button>
        <button type="button" class="infra2d-btn ${isTrap ? 'infra2d-btn-danger' : ''}" onclick="lnx2dState.cronMode='cron_3_traps';renderLinux2DInteractiveStage('cron_automation')">2. Giả Lập 3 Bẫy Chết Câm Lặng</button>
      `;
    }
  }
"""

DATABASE_SIM2D_JS = r"""
  /* ==========================================================================
     INTERACTIVE 2D SIMULATOR FOR F03 (DATABASE FUNDAMENTALS)
     ========================================================================== */
  const DB2D_SLIDES = [
    {
      chapter: "Chặng 1 · RDBMS & Chuẩn Hóa 3NF",
      analogy: "Bốn Chốt Chặn Toàn Vẹn & Phẫu Thuật Tách Bảng",
      title: "Kiến Trúc 4 Tầng RDBMS & Chuẩn Hóa UNF → 1NF → 2NF → 3NF Cho Đơn Hàng Trà Sữa #HD01",
      leadTitle: "Tại sao lưu đơn hàng #HD01 vào 1 bảng gộp phẳng lại gây thảm họa dị thường dữ liệu?",
      leadStory: "Khi khách hàng Lan đặt đơn #HD01 (2 ly Oolong Sua 30k + 1 ly Hong Tra Tac 25k), nếu gộp chung vào 1 dòng văn bản (UNF), hệ thống sẽ mắc kẹt trong 3 dị thường (Thêm, Sửa, Xóa). Chuẩn hóa 3NF tách đơn hàng thành 4 bảng liên kết bằng Primary Key (PK) và Foreign Key (FK).",
      keypoints: [
        "1. 1NF (Nguyên tử hóa): Cấm lưu mảng/chuỗi gộp nhiều món trong 1 ô; mỗi giao điểm dòng–cột chỉ chứa đúng 1 giá trị đơn.",
        "2. 2NF & 3NF (Khử phụ thuộc bộ phận & bắc cầu): Tách thông tin Khách hàng và Món ăn ra bảng riêng để đổi giá 1 lần áp dụng toàn cục.",
        "3. Bốn ràng buộc toàn vẹn (Constraints): NOT NULL, UNIQUE, DEFAULT và CHECK (DonGia > 0) khóa chặt rác ngay tại cửa RDBMS."
      ],
      verdict: "Nguyên lý OLTP: Chuẩn hóa 3NF/BCNF để bảo vệ tính nhất quán khi ghi; chỉ phi chuẩn hóa (Denormalize) có kiểm soát khi tối ưu đọc.",
      simMode: "rdbms_3nf"
    },
    {
      chapter: "Chặng 2 · Giải Phẫu 8KB Slotted Page",
      analogy: "Mảng Con Trỏ Mọc Xuôi vs. Dữ Liệu Mọc Ngược",
      title: "Giải Phẫu Trang Vật Lý 8KB Heap Slotted Page Trong PostgreSQL (PageHeader, Line Pointers & HeapTuple)",
      leadTitle: "Đơn hàng #HD01 nằm như thế nào bên trong khối 8.192 Bytes trên RAM và ổ đĩa?",
      leadStory: "PostgreSQL không đọc/ghi từng dòng lẻ tẻ xuống ổ cứng mà quản lý theo từng trang 8KB (Slotted Page). Đầu trang chứa PageHeader (24B, lưu pd_lsn) và mảng con trỏ ItemIdData (4B/con trỏ) mọc từ trên xuống; dữ liệu dòng (HeapTuple) mọc từ đáy trang ngược lên trên, ở giữa là Free Space.",
      keypoints: [
        "1. Tại sao cần Line Pointer (ItemIdData) trung gian? Để khi dọn mảnh (Defragment) di chuyển Tuple trong trang, B-Tree Index bên ngoài vẫn giữ nguyên địa chỉ TID (Page, Slot)!",
        "2. Cấu trúc HeapTuple: Gồm Tuple Header (23B lưu xmin, xmax, t_ctid, Null Bitmap) đi kèm các byte dữ liệu thực tế của #HD01.",
        "3. Dây xích phiên bản t_ctid: Khi UPDATE #HD01, bản ghi cũ trỏ t_ctid sang vị trí bản ghi mới ngay trong trang (HOT Update) hoặc trang khác."
      ],
      verdict: "Thiết kế Slotted Page tách rời định danh logic (Slot Number) khỏi tọa độ byte vật lý (Offset), giúp B-Tree Index không bị vỡ khi dọn trang.",
      simMode: "slotted_page"
    },
    {
      chapter: "Chặng 2 · WAL Buffer, Dirty Page & Checkpointer",
      analogy: "Ghi Sổ Nhật Ký Tuần Tự Trước Khi Xếp Kệ Kho",
      title: "Đường Đua Bền Vững ACID: Nhật Ký Tuần Tự WAL (Write-Ahead Log) Khi COMMIT vs. Checkpointer Xả Dirty Pages",
      leadTitle: "Làm sao PostgreSQL đảm bảo không mất đơn #HD01 khi sập nguồn mà không bắt khách chờ ghi ngẫu nhiên 8KB?",
      leadStory: "Khi giao dịch #HD01 sửa trang 8KB trên Shared Buffers (RAM), trang đó trở thành Dirty Page. Khi gọi COMMIT, PostgreSQL chỉ cần ghi nối đuôi (Append-only) bản ghi biến động mang mã LSN xuống file WAL trên đĩa (~0.2ms), còn các Dirty Pages được tiến trình Checkpointer xả ngầm xuống Data Files định kỳ.",
      keypoints: [
        "1. Quy tắc Write-Ahead Logging: Bản ghi WAL mang mã LSN bắt buộc phải fsync xuống đĩa TRƯỚC khi lệnh COMMIT trả kết quả thành công.",
        "2. Tách rời Sequential I/O và Random I/O: Ghi WAL là ghi tuần tự siêu nhanh; Checkpointer gom hàng nghìn Dirty Pages xả 1 lượt sau mỗi 5 phút.",
        "3. Khôi phục sau thảm họa (Crash Recovery): Khi bật lại máy, PostgreSQL đọc WAL từ mốc REDO Point và phát lại (Replay) các trang có pd_lsn < WAL LSN."
      ],
      verdict: "WAL là trái tim của cả tính bền vững ACID (Durability), khôi phục sự cố (Crash Recovery) lẫn nhân bản Streaming Replication / CDC!",
      simMode: "wal_checkpoint"
    },
    {
      chapter: "Chặng 3 · MVCC Snapshot & Autovacuum",
      analogy: "Đọc Không Khóa Ghi & Đội Vệ Sinh Thu Hồi Xác Bản Ghi",
      title: "Cơ Học Đa Phiên Bản MVCC (xmin, xmax, Snapshot Isolation) & Tiến Trình Dọn Rác Ngầm Autovacuum",
      leadTitle: "Tại sao 1.000 khách xem menu không bị chặn khi thu ngân đang UPDATE đơn hàng #HD01?",
      leadStory: "Thay vì khóa cứng dòng dữ liệu khi sửa, PostgreSQL áp dụng MVCC: lệnh UPDATE không ghi đè bản ghi cũ mà đánh dấu xmax cho bản cũ (biến thành Dead Tuple khi commit) và chèn một Tuple mới với xmin = txid hiện tại. Mỗi câu lệnh SELECT chụp một bức ảnh Snapshot để chỉ nhìn thấy các phiên bản hợp lệ.",
      keypoints: [
        "1. Đọc không bao giờ chặn Ghi, Ghi không bao giờ chặn Đọc: Nhờ kiểm tra khoảng sống [xmin, xmax] đối chiếu với txid_current_snapshot().",
        "2. Cái giá của MVCC — Table Bloat: Các bản ghi cũ (Dead Tuples) vẫn nằm chiếm chỗ trong trang 8KB cho đến khi không còn giao dịch nào nhìn thấy chúng.",
        "3. Tiến trình Autovacuum Worker: Quét ngầm các trang 8KB để thu hồi vùng nhớ của Dead Tuples đưa vào Free Space Map (FSM) tái sử dụng."
      ],
      verdict: "Trên Production: Tuyệt đối không tắt Autovacuum và phải giám sát giao dịch treo lâu (Long-running transactions) vì chúng ngăn Autovacuum dọn Dead Tuples!",
      simMode: "mvcc_vacuum"
    },
    {
      chapter: "Chặng 3 · B+Tree vs. LSM-Tree & EXPLAIN",
      analogy: "Cây Chỉ Mục Khả Biến Đọc Nhanh vs. Nhật Ký Bất Biến Ghi Nhanh",
      title: "Đọ Sức Cấu Trúc Chỉ Mục: B+Tree (Tối Ưu Đọc) vs. LSM-Tree (Tối Ưu Ghi) & Phẫu Thuật EXPLAIN ANALYZE",
      leadTitle: " Biến truy vấn tìm đơn hàng từ Seq Scan 1.420 ms xuống Index Scan 0.08 ms",
      leadStory: "Khi bảng HoaDon cán mốc 50 triệu dòng, truy vấn không có chỉ mục buộc PostgreSQL phải quét tuần tự toàn bộ các trang 8KB (Seq Scan). Cây B+Tree giữ các khóa sắp xếp sẵn với chiều cao chỉ 3–4 tầng giúp nhảy thẳng tới đúng trang 8KB sau 3 lần đọc bộ nhớ.",
      keypoints: [
        "1. B+Tree (PostgreSQL, MySQL InnoDB): Cập nhật tại chỗ (In-place page split), lá nối nhau bằng danh sách liên kết kép cực kỳ tối ưu cho truy vấn khoảng (Range Scan).",
        "2. LSM-Tree (RocksDB, Cassandra): Ghi nối đuôi vào MemTable (RAM) rồi xả thành SSTable bất biến trên đĩa + Compaction ngầm — tối ưu cho tải ghi cực lớn.",
        "3. Đọc vị EXPLAIN (ANALYZE, BUFFERS): So sánh Estimated Rows vs. Actual Rows và kiểm tra Shared Hit (RAM) vs. Shared Read (Đĩa)."
      ],
      verdict: "Đánh đổi cốt lõi: B+Tree thắng về tốc độ Đọc ngẫu nhiên/khoảng; LSM-Tree thắng về thông lượng Ghi tuần tự và độ nén đĩa.",
      simMode: "btree_vs_lsm"
    },
    {
      chapter: "Chặng 4 · Sharding, 6 PGD Nodes & CAP/BASE",
      analogy: "Chia Để Trị & Lá Phiếu Trọng Tài Chống Split-Brain",
      title: "Mở Rộng Phân Tán: Horizontal Sharding, Cụm High Availability (Witness Node Quorum) & Định Lý CAP / BASE",
      leadTitle: "Khi 1 máy chủ PostgreSQL chạm trần vật lý và bài toán sống còn khi đứt cáp liên vùng",
      leadStory: "Khi dữ liệu vượt ngưỡng 1 máy chủ (Scale-up), kiến trúc buộc phải mở rộng ngang (Scale-out) qua Replication (tách đọc/ghi, dự phòng HA) và Sharding (băm khóa chia dữ liệu ra nhiều nút). Khi đứt cáp mạng (Network Partition — P), định lý CAP buộc hệ thống phải chọn giữa Nhất quán tuyệt đối (CP) hoặc Sẵn sàng phục vụ (AP).",
      keypoints: [
        "1. Sync vs. Async Replication: Nhân bản đồng bộ bảo toàn 0% mất dữ liệu (RPO = 0) nhưng tăng độ trễ COMMIT; bất đồng bộ nhanh nhưng có thể trễ Replication Lag.",
        "2. Chống não phân đôi (Split-Brain) bằng Witness Node: Đặt 3 nodes ở Region A, 3 nodes ở Region B và 1 Witness Node ở Region C để luôn có số lẻ bầu chọn Quorum.",
        "3. Định lý CAP & Mô hình BASE: Hệ thống tài chính chọn CP (khóa giao dịch nếu mất Quorum); giỏ hàng/mạng xã hội chọn AP (Eventual Consistency)."
      ],
      verdict: "Thiết kế cụm HA chuẩn: Luôn dùng tổng số nút bầu chọn lẻ (3, 5, hoặc 2 vùng + 1 Witness Node) để đạt đồng thuận Raft/Paxos.",
      simMode: "sharding_cap"
    }
  ];

  let db2dCurrentSlide = 0;
  const db2dState = {
    normMode: "norm_3nf",
    pageMode: "update_ctid",
    walMode: "commit_wal",
    mvccMode: "mvcc_snapshot",
    idxMode: "btree_index",
    capMode: "pgd_witness"
  };

  function buildDatabase2DSimulatorHtml() {
    return `
      <div class="infra2d-wrap" id="db2dWidgetRoot">
        <div class="infra2d-header">
          <div class="infra2d-brand">
            <div class="infra2d-brand-icon">2D</div>
            <div>
              <div class="infra2d-brand-badges">
                <span class="infra2d-tag">Cắt Lớp Động Cơ Lưu Trữ &amp; Phân Tán CSDL 2D</span>
                <span class="infra2d-chapter" id="db2dChapterBadge">Chặng 1 · RDBMS &amp; Chuẩn Hóa 3NF</span>
              </div>
              <h4 class="infra2d-title-bar">Phòng Thí Nghiệm Tương Tác F03: Hành Trình Đơn Hàng Trà Sữa #HD01 Trong Động Cơ PostgreSQL</h4>
            </div>
          </div>
          <div class="infra2d-dots" id="db2dDots"></div>
          <button type="button" class="infra2d-btn" onclick="toggleDatabase2DSummaryModal()">Bảng Tóm Tắt Thông Số</button>
        </div>

        <div id="db2dSummaryDrawer" style="display:none;padding:14px 16px;background:var(--sim-canvas);border-bottom:1px solid var(--sim-border);">
          <div style="padding:10px 12px;border-radius:8px;background:var(--sim-flow-soft);border:1px solid color-mix(in oklab, var(--sim-flow) 35%, transparent);font-size:12.5px;color:var(--sim-flow);margin-bottom:10px;">
            <strong>Chuẩn kiến trúc F03 (Database Internals):</strong> Thiết kế lược đồ <strong>3NF + Constraints</strong>, nắm vững cơ học <strong>8KB Slotted Page + Write-Ahead Log (WAL)</strong>, giám sát <strong>MVCC Autovacuum</strong> và tối ưu truy vấn bằng <strong>B+Tree + EXPLAIN ANALYZE</strong>.
          </div>
          <div class="table-wrap" style="margin:0;">
            <table class="clean-table">
              <thead>
                <tr>
                  <th>Tầng Cắt Lớp</th>
                  <th>Cơ Chế Cốt Lõi</th>
                  <th>Thông Số &amp; Lệnh Chuẩn Production</th>
                  <th>Rủi Ro Sinh Tử Cần Chặn</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>1. Schema &amp; 3NF</strong></td>
                  <td><code>UNF → 1NF → 2NF → 3NF</code> + <code>PK/FK</code></td>
                  <td><code>NOT NULL</code>, <code>UNIQUE</code>, <code>CHECK (price &gt; 0)</code></td>
                  <td>Lưu chuỗi gộp gây dị thường cập nhật và rác dữ liệu nguồn</td>
                </tr>
                <tr>
                  <td><strong>2. Storage Engine</strong></td>
                  <td><code>8KB Slotted Page</code> + <code>WAL LSN</code></td>
                  <td><code>shared_buffers = 25% RAM</code>, <code>wal_level = logical</code></td>
                  <td>Nhầm lẫn rằng <code>COMMIT</code> ghi thẳng xuống bảng Heap thay vì <code>WAL</code></td>
                </tr>
                <tr>
                  <td><strong>3. MVCC &amp; Index</strong></td>
                  <td><code>xmin/xmax Snapshot</code> + <code>B+Tree</code></td>
                  <td><code>EXPLAIN (ANALYZE, BUFFERS)</code>, <code>autovacuum = on</code></td>
                  <td>Giao dịch treo lâu chặn <code>Autovacuum</code> gây phình bảng <code>Table Bloat</code></td>
                </tr>
                <tr>
                  <td><strong>4. HA &amp; Distributed</strong></td>
                  <td><code>Sharding</code> + <code>Raft Quorum</code> + <code>CAP</code></td>
                  <td>Cụm đa vùng + <code>Witness Node</code> (Số phiếu lẻ)</td>
                  <td>Cụm 2 vùng chẵn không có Witness Node dẫn tới <code>Split-Brain</code></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="infra2d-grid">
          <div class="infra2d-col-left">
            <div>
              <div class="infra2d-pills">
                <span class="infra2d-pill-num" id="db2dSlideNumPill">SLIDE 1 / 6</span>
                <span class="infra2d-pill-analogy" id="db2dAnalogyPill">Lát Cắt CSDL</span>
              </div>
              <h3 class="infra2d-slide-h3" id="db2dSlideTitle"></h3>
              <div class="infra2d-story-box">
                <div class="infra2d-avatar" title="Đơn hàng Trà sữa #HD01">DB</div>
                <div>
                  <span class="infra2d-story-title" id="db2dLeadTitle"></span>
                  <p class="infra2d-story-text" id="db2dLeadStory"></p>
                </div>
              </div>
              <div class="infra2d-keypoints" id="db2dKeypoints"></div>
            </div>
            <div class="infra2d-verdict" id="db2dVerdictBox"></div>
          </div>

          <div class="infra2d-col-right">
            <div>
              <div class="infra2d-sim-top">
                <div class="infra2d-sim-live">
                  <span class="infra2d-sim-dot"></span>
                  <span>Sơ Đồ Cắt Lớp PostgreSQL Storage Engine &amp; MVCC (Animated SVG)</span>
                </div>
                <span class="infra2d-sim-hint">Bấm các nút kịch bản bên dưới để đổi cơ chế!</span>
              </div>
              <div class="infra2d-stage" id="db2dSimStage" style="padding:10px;"></div>
            </div>
            <div>
              <div class="infra2d-status" id="db2dSimStatusText">Sẵn sàng mô phỏng.</div>
              <div class="infra2d-controls" id="db2dSimControls"></div>
            </div>
          </div>
        </div>

        <div class="infra2d-footer">
          <button type="button" class="infra2d-btn" id="db2dBtnPrev" onclick="changeDatabase2DSlide(-1)">← Mô Phỏng Trước</button>
          <div class="infra2d-progress-wrap">
            <div class="infra2d-progress-track">
              <div class="infra2d-progress-fill" id="db2dProgressFill" style="width:16.6%;"></div>
            </div>
            <span class="infra2d-progress-label" id="db2dProgressLabel">Mô phỏng 1 / 6</span>
          </div>
          <button type="button" class="infra2d-btn infra2d-btn-primary" id="db2dBtnNext" onclick="changeDatabase2DSlide(1)">Mô Phỏng Tiếp Theo →</button>
        </div>
      </div>
    `;
  }

  function toggleDatabase2DSummaryModal() {
    const el = document.getElementById("db2dSummaryDrawer");
    if (el) el.style.display = el.style.display === "none" ? "block" : "none";
  }

  function changeDatabase2DSlide(delta) {
    db2dCurrentSlide = (db2dCurrentSlide + delta + DB2D_SLIDES.length) % DB2D_SLIDES.length;
    renderDatabase2DSlide();
  }

  function jumpDatabase2DSlide(idx) {
    db2dCurrentSlide = idx;
    renderDatabase2DSlide();
  }

  function renderDatabase2DSlide() {
    const s = DB2D_SLIDES[db2dCurrentSlide];
    if (!s) return;
    const chEl = document.getElementById("db2dChapterBadge");
    if (!chEl) return;
    chEl.textContent = s.chapter;
    document.getElementById("db2dSlideNumPill").textContent = `SLIDE ${db2dCurrentSlide + 1} / ${DB2D_SLIDES.length}`;
    document.getElementById("db2dAnalogyPill").textContent = s.analogy;
    document.getElementById("db2dSlideTitle").textContent = s.title;
    document.getElementById("db2dLeadTitle").textContent = s.leadTitle;
    document.getElementById("db2dLeadStory").textContent = s.leadStory;
    document.getElementById("db2dKeypoints").innerHTML = s.keypoints
      .map(kp => `<div class="infra2d-kp"><span class="infra2d-kp-dot"></span><span>${escapeHtml(kp)}</span></div>`)
      .join("");
    document.getElementById("db2dVerdictBox").innerHTML = `<strong>Chốt nguyên lý:</strong> ${escapeHtml(s.verdict)}`;
    document.getElementById("db2dDots").innerHTML = DB2D_SLIDES.map(
      (_, i) => `<button type="button" class="infra2d-dot ${i === db2dCurrentSlide ? 'active' : ''}" onclick="jumpDatabase2DSlide(${i})" title="Slide ${i + 1}">${i + 1}</button>`
    ).join("");
    const pct = (((db2dCurrentSlide + 1) / DB2D_SLIDES.length) * 100).toFixed(1);
    document.getElementById("db2dProgressFill").style.width = `${pct}%`;
    document.getElementById("db2dProgressLabel").textContent = `Mô phỏng ${db2dCurrentSlide + 1} / ${DB2D_SLIDES.length}`;
    renderDatabase2DInteractiveStage(s.simMode);
  }

  function renderDatabase2DInteractiveStage(mode) {
    const stage = document.getElementById("db2dSimStage");
    const status = document.getElementById("db2dSimStatusText");
    const ctrls = document.getElementById("db2dSimControls");
    if (!stage || !status || !ctrls) return;

    if (mode === "rdbms_3nf") {
      const m = db2dState.normMode;
      const isUnf = m === "unf_anomaly";
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          ${isUnf ? `
            <rect x="24" y="34" width="512" height="150" rx="8" fill="var(--sim-warn-soft)" stroke="var(--sim-danger)" stroke-width="1.6"/>
            <text x="36" y="58" fill="var(--sim-danger)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">BẢNG GỘP CHƯA CHUẨN HÓA (UNF — VI PHẠM 1NF/2NF/3NF)</text>
            <text x="36" y="84" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">MaHD="#HD01" | TenKH="Lan" | Mon="Oolong(30k,SL:2), HongTra(25k,SL:1)"</text>
            <text x="36" y="112" fill="var(--sim-danger)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">• Dị thường Sửa: Đổi giá Oolong phải quét sửa 100.000 dòng hóa đơn cũ!</text>
            <text x="36" y="134" fill="var(--sim-danger)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">• Dị thường Xóa: Xóa đơn #HD01 làm mất luôn thông tin khách hàng Lan!</text>
            <text x="36" y="156" fill="var(--sim-danger)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">• Dị thường Thêm: Không thể thêm món mới vào menu nếu chưa có người mua!</text>
          ` : `
            <rect x="22" y="28" width="248" height="74" rx="7" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.5"/>
            <text x="32" y="48" fill="var(--sim-flow)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">1. BẢNG KhachHang (PK: MaKH)</text>
            <text x="32" y="70" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">MaKH="KH01" | Ten="Lan" | SDT UNIQUE</text>

            <rect x="290" y="28" width="248" height="74" rx="7" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.5"/>
            <text x="300" y="48" fill="var(--sim-flow)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">2. BẢNG HoaDon (PK: MaHD, FK: MaKH)</text>
            <text x="300" y="70" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">MaHD="#HD01" | MaKH="KH01" | Ngay</text>

            <rect x="22" y="114" width="248" height="74" rx="7" fill="var(--sim-card-alt)" stroke="var(--sim-ok)" stroke-width="1.5"/>
            <text x="32" y="134" fill="var(--sim-ok)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">3. BẢNG MonAn (PK: MaMon)</text>
            <text x="32" y="156" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">M01="Oolong" CHECK(DonGia = 30000 &gt; 0)</text>

            <rect x="290" y="114" width="248" height="74" rx="7" fill="var(--sim-flow-soft)" stroke="var(--sim-clay)" stroke-width="1.6"/>
            <text x="300" y="134" fill="var(--sim-clay)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">4. BẢNG ChiTietHD (PK Kép: MaHD+MaMon)</text>
            <text x="300" y="156" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">(#HD01, M01, SL=2) + (#HD01, M02, SL=1)</text>
          `}
          <rect x="22" y="198" width="516" height="28" rx="6" fill="var(--sim-card-alt)" stroke="var(--sim-border)"/>
          <text x="34" y="216" fill="var(--sim-ink)" font-size="9.2" font-weight="700" font-family="var(--cds-font-mono)">${isUnf ? 'Cảnh báo: Vi phạm 1NF (cột gộp nhiều món) làm tê liệt khả năng truy vấn và gây sai lệch dữ liệu.' : 'Chuẩn 3NF + Constraints: Mọi thuộc tính không khóa chỉ phụ thuộc duy nhất vào Primary Key!'}</text>
        </svg>
      `;
      status.textContent = isUnf
        ? "Bảng UNF chưa chuẩn hóa: Gộp nhiều món vào 1 ô khiến việc cập nhật giá hoặc xóa đơn hàng gây mất mát thông tin."
        : "Chuẩn hóa 3NF hoàn chỉnh: Tách đơn #HD01 thành 4 bảng có PK/FK và khóa đầu vào bằng NOT NULL, UNIQUE, CHECK.";
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${!isUnf ? 'infra2d-btn-emerald' : ''}" onclick="db2dState.normMode='norm_3nf';renderDatabase2DInteractiveStage('rdbms_3nf')">1. Lược Đồ Chuẩn 3NF (4 Bảng PK/FK)</button>
        <button type="button" class="infra2d-btn ${isUnf ? 'infra2d-btn-danger' : ''}" onclick="db2dState.normMode='unf_anomaly';renderDatabase2DInteractiveStage('rdbms_3nf')">2. Giả Lập Bảng Phẳng UNF (3 Dị Thường)</button>
      `;
    } else if (mode === "slotted_page") {
      const m = db2dState.pageMode;
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="24" y="24" width="512" height="44" rx="6" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="36" y="44" fill="var(--sim-flow)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">ĐẦU TRANG 8KB: PageHeader (24B: pd_lsn=0/16B3748) + Line Pointers (Mọc Xuôi ↓)</text>
          <text x="36" y="60" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">[Slot 1 → Offset 8096]   [Slot 2 → Offset 7980]   ${m === 'update_ctid' ? '[Slot 3 (New) → Offset 7860]' : ''}</text>

          <rect x="24" y="78" width="512" height="58" rx="6" fill="var(--sim-canvas)" stroke="var(--sim-border)" stroke-dasharray="5 4"/>
          <text x="195" y="112" fill="var(--sim-muted)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">↕ FREE SPACE (pd_lower → pd_upper) ↕</text>

          <rect x="24" y="146" width="512" height="74" rx="6" fill="var(--sim-flow-soft)" stroke="var(--sim-clay)" stroke-width="1.6"/>
          <text x="36" y="168" fill="var(--sim-clay)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">ĐÁY TRANG 8KB: Dữ Liệu Dòng HeapTuple (Mọc Ngược Từ Dưới Lên ↑)</text>
          <text x="36" y="190" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">${m === 'insert_tuple' ? 'Tuple 1 (#HD01: xmin=501, xmax=0, t_ctid=(0,1), DonGia=30000)' : 'Tuple 1 (Cũ: xmin=501, xmax=509, t_ctid=(0,3)) ──► Tuple 3 (Mới: xmin=509, xmax=0, DonGia=32000)'}</text>
          <text x="36" y="208" fill="var(--sim-ok)" font-size="8.8" font-weight="700" font-family="var(--cds-font-mono)">B-Tree Index chỉ lưu TID = (Page 0, Slot 1) — không bao giờ sợ lệch khi dọn mảnh trang!</text>
        </svg>
      `;
      status.textContent = m === "insert_tuple"
        ? "Khi INSERT #HD01: Thêm 1 Line Pointer (4B) ở đầu trang và ghi HeapTuple vào đáy trang, thu hẹp khoảng Free Space ở giữa."
        : "Khi UPDATE #HD01: Không ghi đè tại chỗ! Bản cũ được gán xmax=509 và nối con trỏ t_ctid=(0,3) sang bản ghi mới ở Slot 3.";
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${m === 'insert_tuple' ? 'infra2d-btn-cyan' : ''}" onclick="db2dState.pageMode='insert_tuple';renderDatabase2DInteractiveStage('slotted_page')">1. INSERT #HD01 Vào Trang 8KB</button>
        <button type="button" class="infra2d-btn ${m === 'update_ctid' ? 'infra2d-btn-emerald' : ''}" onclick="db2dState.pageMode='update_ctid';renderDatabase2DInteractiveStage('slotted_page')">2. UPDATE #HD01 (Nối Dây Xích t_ctid)</button>
      `;
    } else if (mode === "wal_checkpoint") {
      const m = db2dState.walMode;
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="22" y="28" width="244" height="148" rx="7" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="32" y="50" fill="var(--sim-flow)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">RAM (SHARED BUFFERS + WAL BUFFER)</text>
          <text x="32" y="78" fill="var(--sim-clay)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">• Page #0 (#HD01) = DIRTY PAGE!</text>
          <text x="32" y="100" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">• WAL Buffer: LSN 0/16B3748</text>
          <text x="32" y="128" fill="var(--sim-muted)" font-size="8.5" font-family="var(--cds-font-mono)">RAM mất dữ liệu nếu đứt điện!</text>

          <rect x="294" y="28" width="244" height="70" rx="7" fill="var(--sim-flow-soft)" stroke="var(--sim-ok)" stroke-width="1.6"/>
          <text x="304" y="48" fill="var(--sim-ok)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">ĐĨA 1 · WAL FILES (pg_wal/)</text>
          <text x="304" y="68" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">Ghi tuần tự (Sequential fsync ~0.2ms)</text>
          <text x="304" y="86" fill="var(--sim-ok)" font-size="8.5" font-weight="700" font-family="var(--cds-font-mono)">→ Đảm bảo COMMIT thành công tức thì!</text>

          <rect x="294" y="108" width="244" height="68" rx="7" fill="var(--sim-card-alt)" stroke="var(--sim-clay)" stroke-width="1.5"/>
          <text x="304" y="128" fill="var(--sim-clay)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">ĐĨA 2 · DATA FILES (base/heap)</text>
          <text x="304" y="148" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">${m === 'commit_wal' ? 'Chưa cần ghi ngay lúc COMMIT!' : 'Checkpointer xả Dirty Pages mỗi 5p'}</text>

          <circle r="4.5" fill="var(--sim-ok)">
            <animate attributeName="cx" values="266;294" dur="1.1s" repeatCount="indefinite"/>
            <animate attributeName="cy" values="64;64" dur="1.1s" repeatCount="indefinite"/>
          </circle>
          <rect x="22" y="190" width="516" height="32" rx="6" fill="var(--sim-card-alt)" stroke="var(--sim-border)"/>
          <text x="34" y="210" fill="var(--sim-ink)" font-size="9.2" font-weight="700" font-family="var(--cds-font-mono)">${m === 'commit_wal' ? 'Lúc COMMIT: Chỉ ép fsync dòng WAL tuần tự xuống pg_wal, giúp giao dịch OLTP đạt độ trễ sub-millisecond.' : 'Khi sập nguồn: PostgreSQL đọc lại pg_wal từ REDO Point để tái tạo chính xác mọi Dirty Page chưa kịp xả!'}</text>
        </svg>
      `;
      status.textContent = m === "commit_wal"
        ? "Luồng COMMIT chuẩn: Ghi nối đuôi WAL Record xuống pg_wal trước, trả kết quả ngay cho khách hàng mà không chờ ghi Data Files."
        : "Checkpointer & Crash Recovery: Xả ngầm Dirty Pages định kỳ và tự động phát lại (Replay) WAL nếu máy chủ mất điện.";
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${m === 'commit_wal' ? 'infra2d-btn-emerald' : ''}" onclick="db2dState.walMode='commit_wal';renderDatabase2DInteractiveStage('wal_checkpoint')">1. Lúc COMMIT (Sequential WAL fsync)</button>
        <button type="button" class="infra2d-btn ${m === 'checkpoint_flush' ? 'infra2d-btn-cyan' : ''}" onclick="db2dState.walMode='checkpoint_flush';renderDatabase2DInteractiveStage('wal_checkpoint')">2. Checkpointer &amp; Phục Hồi Sập Nguồn</button>
      `;
    } else if (mode === "mvcc_vacuum") {
      const m = db2dState.mvccMode;
      const isBloat = m === "dead_tuple_bloat";
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="24" y="30" width="512" height="145" rx="8" fill="${isBloat ? 'var(--sim-warn-soft)' : 'var(--sim-card)'}" stroke="${isBloat ? 'var(--sim-danger)' : 'var(--sim-flow)'}" stroke-width="1.6"/>
          <text x="36" y="54" fill="${isBloat ? 'var(--sim-danger)' : 'var(--sim-flow)'}" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">${isBloat ? 'CẢNH BÁO TABLE BLOAT: TẮT AUTOVACUUM HOẶC GIAO DỊCH TREO!' : 'CƠ CHẾ ĐA PHIÊN BẢN MVCC & AUTOVACUUM WORKER'}</text>
          <text x="36" y="82" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">• Bản v1 (Cũ) : xmin=501, xmax=509 → ${isBloat ? 'DEAD TUPLE nằm lì chiếm chỗ!' : 'Đã được Autovacuum thu hồi vào FSM!'}</text>
          <text x="36" y="106" fill="var(--sim-ok)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">• Bản v2 (Mới): xmin=509, xmax=0   → LIVE TUPLE (Phục vụ đọc/ghi mới)</text>
          <text x="36" y="134" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">• Reader (txid=505): Nhìn thấy v1 qua Snapshot mà KHÔNG chặn Writer (txid=509)!</text>
          <rect x="24" y="188" width="512" height="34" rx="6" fill="var(--sim-card-alt)" stroke="var(--sim-border)"/>
          <text x="36" y="209" fill="var(--sim-ink)" font-size="9.2" font-weight="700" font-family="var(--cds-font-mono)">${isBloat ? 'Hậu quả: Bảng chỉ có 1 triệu dòng sống nhưng phình thành 10 triệu dòng xác chết, làm Seq Scan chậm gấp 10x!' : 'Quy tắc vàng: MVCC giúp Đọc–Ghi song song không khóa nhau, còn Autovacuum dọn dẹp Dead Tuples ngầm.'}</text>
        </svg>
      `;
      status.textContent = isBloat
        ? "Bệnh phình bảng (Table Bloat): Dead Tuples tích tụ làm giảm mật độ trang 8KB và ngốn bộ nhớ đệm Shared Buffers."
        : "MVCC + Autovacuum khỏe mạnh: Đọc và Ghi hoàn toàn không khóa nhau, vùng nhớ cũ được thu hồi liên tục.";
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${!isBloat ? 'infra2d-btn-emerald' : ''}" onclick="db2dState.mvccMode='mvcc_snapshot';renderDatabase2DInteractiveStage('mvcc_vacuum')">1. MVCC Snapshot + Autovacuum Dọn Rác</button>
        <button type="button" class="infra2d-btn ${isBloat ? 'infra2d-btn-danger' : ''}" onclick="db2dState.mvccMode='dead_tuple_bloat';renderDatabase2DInteractiveStage('mvcc_vacuum')">2. Giả Lập Phình Bảng (Dead Tuple Bloat)</button>
      `;
    } else if (mode === "btree_vs_lsm") {
      const m = db2dState.idxMode;
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="22" y="28" width="250" height="150" rx="7" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="32" y="50" fill="var(--sim-flow)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">B+TREE INDEX (POSTGRESQL)</text>
          <text x="32" y="76" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">Root Page → Internal → Leaf Pages</text>
          <text x="32" y="100" fill="var(--sim-ok)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">Độ trễ tìm #HD01: 0.08 ms (3 hops)</text>
          <text x="32" y="124" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">Lá nối danh sách liên kết kép</text>
          <text x="32" y="146" fill="var(--sim-muted)" font-size="8.5" font-family="var(--cds-font-mono)">Tối ưu: Đọc điểm &amp; Range Scan</text>

          <rect x="288" y="28" width="250" height="150" rx="7" fill="var(--sim-flow-soft)" stroke="var(--sim-clay)" stroke-width="1.6"/>
          <text x="298" y="50" fill="var(--sim-clay)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">LSM-TREE (ROCKSDB / CASSANDRA)</text>
          <text x="298" y="76" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">MemTable (RAM) → SSTables L0..L3</text>
          <text x="298" y="100" fill="var(--sim-clay)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">Ghi nối đuôi siêu tốc (Append-Only)</text>
          <text x="298" y="124" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">Dùng Bloom Filter + Compaction</text>
          <text x="298" y="146" fill="var(--sim-muted)" font-size="8.5" font-family="var(--cds-font-mono)">Tối ưu: Tải ghi sự kiện khổng lồ</text>

          <rect x="22" y="190" width="516" height="32" rx="6" fill="var(--sim-card-alt)" stroke="var(--sim-border)"/>
          <text x="34" y="210" fill="var(--sim-ink)" font-size="9.2" font-weight="700" font-family="var(--cds-font-mono)">${m === 'seq_scan_slow' ? 'Thiếu Index: EXPLAIN ANALYZE báo Seq Scan quét 50 triệu dòng mất 1.420 ms!' : 'Có B+Tree Index: EXPLAIN ANALYZE báo Index Scan (Shared Hit=3) chỉ mất 0.08 ms!'}</text>
        </svg>
      `;
      status.textContent = m === "btree_index"
        ? "B+Tree Index Scan: Chỉ đọc đúng 3 trang 8KB từ Root xuống Leaf để lấy TID của #HD01 trong 0.08 ms."
        : "Seq Scan khi thiếu Index: Phải đọc tuần tự hàng trăm nghìn trang 8KB từ đĩa để lọc ra 1 đơn hàng.";
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${m === 'btree_index' ? 'infra2d-btn-emerald' : ''}" onclick="db2dState.idxMode='btree_index';renderDatabase2DInteractiveStage('btree_vs_lsm')">1. B+Tree Index Scan (0.08 ms)</button>
        <button type="button" class="infra2d-btn ${m === 'seq_scan_slow' ? 'infra2d-btn-danger' : ''}" onclick="db2dState.idxMode='seq_scan_slow';renderDatabase2DInteractiveStage('btree_vs_lsm')">2. Giả Lập Seq Scan Không Index (1.420 ms)</button>
      `;
    } else {
      const m = db2dState.capMode;
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="22" y="32" width="155" height="140" rx="7" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="32" y="54" fill="var(--sim-flow)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">REGION A (3 NODES)</text>
          <text x="32" y="80" fill="var(--sim-ok)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">Leader + 2 Replicas</text>
          <text x="32" y="104" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">Nhận ghi #HD01</text>

          <rect x="202" y="32" width="156" height="140" rx="7" fill="var(--sim-flow-soft)" stroke="var(--sim-clay)" stroke-width="1.6"/>
          <text x="212" y="54" fill="var(--sim-clay)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">REGION C (WITNESS)</text>
          <text x="212" y="80" fill="var(--sim-ink)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">1 Witness Node</text>
          <text x="212" y="104" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">Giữ lá phiếu lẻ thứ 7</text>
          <text x="212" y="128" fill="var(--sim-ok)" font-size="8.5" font-weight="700" font-family="var(--cds-font-mono)">Chống Split-Brain 100%!</text>

          <rect x="382" y="32" width="156" height="140" rx="7" fill="var(--sim-card-alt)" stroke="var(--sim-ok)" stroke-width="1.5"/>
          <text x="392" y="54" fill="var(--sim-ok)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">REGION B (3 NODES)</text>
          <text x="392" y="80" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">3 Standby Replicas</text>
          <text x="392" y="104" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">Sẵn sàng Failover</text>
        </svg>
      `;
      status.textContent = m === "pgd_witness"
        ? "Kiến trúc High Availability đa vùng: 3 Nodes Region A + 3 Nodes Region B + 1 Witness Node ở Region C tạo tổng 7 phiếu bầu Quorum."
        : "Định lý CAP: Khi xảy ra phân vùng mạng (P), hệ thống CP khóa nhánh thiểu số để bảo vệ tiền tệ, còn AP ưu tiên phản hồi Eventual Consistency.";
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${m === 'pgd_witness' ? 'infra2d-btn-emerald' : ''}" onclick="db2dState.capMode='pgd_witness';renderDatabase2DInteractiveStage('sharding_cap')">1. Cụm Đa Vùng + Witness Node (Quorum)</button>
        <button type="button" class="infra2d-btn ${m === 'cap_tradeoff' ? 'infra2d-btn-cyan' : ''}" onclick="db2dState.capMode='cap_tradeoff';renderDatabase2DInteractiveStage('sharding_cap')">2. Đối Chiếu CP (ACID) vs. AP (BASE)</button>
      `;
    }
  }
"""

STORAGE_SIM2D_JS = r"""
  /* ==========================================================================
     INTERACTIVE 2D SIMULATOR FOR D02 (STORAGE LAYER & LAKEHOUSE)
     ========================================================================== */
  const STORAGE2D_SLIDES = [
    {
      chapter: "Chặng 1 · Tháp Độ Trễ & Spill-to-Disk",
      analogy: "Từ Bàn Làm Việc CPU 1ns Đến Kho Lạnh S3 100ms",
      title: "Tháp Độ Trễ Vật Lý (L1 Cache 1ns → RAM 100ns → NVMe 100µs → HDD 10ms → S3 100ms) & Phân Tầng Nhiệt Độ",
      leadTitle: "Tại sao tràn RAM phải Spill-to-Disk lại làm truy vấn Đơn hàng #8888 chậm đi gấp 1.000 lần?",
      leadStory: "Không có phần cứng nào vừa nhanh như CPU Cache (1 ns), vừa rẻ như Cloud Object Storage (S3 ~$0.023/GB/tháng), lại vừa bền vững khi mất điện. Kiến trúc lưu trữ bắt buộc phải phân tầng theo nhiệt độ dữ liệu (Hot / Warm / Cold) và ưu tiên đọc tuần tự (Sequential Scan) thay vì nhảy cóc ngẫu nhiên (Random Seek).",
      keypoints: [
        "1. Khoảng cách 100.000x: Đọc từ RAM mất ~100 ns, nhưng khi tràn bộ nhớ phải Spill-to-Disk xuống SSD/HDD hoặc S3 thì độ trễ vọt lên 100 µs – 100 ms.",
        "2. Random Seek vs. Sequential Scan: Đọc tuần tự liền mạch giúp tận dụng băng thông tối đa của cả ổ cứng lẫn mạng Cloud.",
        "3. Phân tầng Hot / Warm / Cold: Dữ liệu giao dịch nóng nằm trên NVMe/RAM; lịch sử phân tích nằm trên S3 Parquet; lưu trữ pháp lý đẩy xuống Glacier."
      ],
      verdict: "Mọi thiết kế định dạng tệp (Parquet) và bảng (Lakehouse) ở tầng trên đều sinh ra để bù đắp cho giới hạn độ trễ vật lý ở tầng dưới!",
      simMode: "latency_spill"
    },
    {
      chapter: "Chặng 2 · Parquet Columnar & Apache Arrow",
      analogy: "Xoay Trục Theo Cột & Nhảy Cóc Qua Row Group",
      title: "Giải Phẫu Định Dạng Cột Lai Apache Parquet (Row Group, Column Chunk, Footer Min/Max) & Apache Arrow Zero-Copy",
      leadTitle: "Tại sao đọc 3 cột trên bảng 100 cột bằng Parquet giảm 96% I/O so với CSV?",
      leadStory: "Định dạng theo dòng (CSV) bắt buộc đầu đọc phải lướt qua toàn bộ 100 cột của từng dòng. Ngược lại, Apache Parquet chia bảng thành các Row Groups (128MB), bên trong xếp dữ liệu cùng một cột nằm liền kề nhau thành Column Chunks kèm thống kê Min/Max trong Footer.",
      keypoints: [
        "1. Projection Pushdown (Column Pruning): Truy vấn SELECT store_id, amount chỉ đọc đúng 2 Column Chunks đó trên đĩa, bỏ qua 98 cột còn lại.",
        "2. Predicate Pushdown (Row Group Skipping): Nhờ đọc Min/Max trong Footer ở cuối file, động cơ bỏ qua nguyên các Row Groups không chứa Đơn hàng #8888.",
        "3. Apache Arrow trên RAM: Chuẩn hóa bộ nhớ cột trên RAM giúp truyền dữ liệu giữa JVM (Spark), C++ (DuckDB) và Python với 0% chi phí Serialization."
      ],
      verdict: "Bộ đôi chuẩn vàng của Data Engineering hiện đại: Lưu trữ trên đĩa bằng Apache Parquet (nén ZSTD/Snappy) + Xử lý trên RAM bằng Apache Arrow.",
      simMode: "parquet_arrow"
    },
    {
      chapter: "Chặng 3 · HDFS 3x vs. Cloud Object Storage",
      analogy: "Kho Khối Gắn Chặt Máy Chủ vs. Kho Đối Tượng Tách Rời",
      title: "Hạ Tầng Phân Tán: Hadoop HDFS (NameNode & 128MB Blocks Nhân Bản 3x) vs. Cloud Object Storage (S3 / MinIO)",
      leadTitle: "Bước chuyển mình lịch sử từ cụm HDFS gắn chặt Compute–Storage sang đám mây S3 tách rời",
      leadStory: "HDFS chia tệp lớn thành các khối 128 MB và nhân bản 3 lần (3x Replication) qua các Racks máy chủ vật lý để chịu lỗi. Tuy nhiên trên Cloud, việc phải thuê thêm CPU chỉ để mở rộng ổ cứng HDFS quá tốn kém — Cloud Object Storage (S3/GCS/ADLS/MinIO) tách rời hoàn toàn tầng Lưu trữ khỏi tầng Tính toán.",
      keypoints: [
        "1. HDFS Rack-Aware Replication (3x): 1 bản tại node cục bộ, 1 bản ở rack khác và 1 bản nữa cùng rack thứ hai để chống sập cả tủ mạng.",
        "2. Điểm nghẽn NameNode RAM: Mọi siêu dữ liệu file/block của HDFS đều nằm trong RAM của NameNode, nên hàng triệu file nhỏ sẽ làm nổ NameNode!",
        "3. Cloud Object Storage (S3/MinIO): Không gian tên phẳng truy cập qua HTTP REST API (PUT/GET), bất biến (Immutable Objects) và co giãn độc lập với Compute."
      ],
      verdict: "Đặc tính bất biến (không thể sửa 1 byte giữa file Parquet trên S3) chính là lý do phải sinh ra tầng siêu dữ liệu Open Table Formats ở Chặng 6!",
      simMode: "hdfs_object_dwh"
    },
    {
      chapter: "Chặng 4 · Kimball Star Schema & SCD Type 2",
      analogy: "Bảng Sự Kiện Trung Tâm & Vết Thời Gian Lịch Sử",
      title: "Mô Hình Hóa Chiều Kimball: Fact vs. Dimension (Grain), Star Schema vs. OBT & Theo Dõi Lịch Sử SCD Type 2",
      leadTitle: "Làm sao giữ đúng doanh thu lịch sử ở Bình Dương khi khách hàng Nguyễn Văn A chuyển nhà lên TP.HCM?",
      leadStory: "Trong kho dữ liệu phân tích, mô hình Kimball tổ chức dữ liệu thành bảng Fact (lưu số đo định lượng như đơn #8888 giá 15 triệu ở một độ mịn Grain cố định) bao quanh bởi các bảng Dimension (Ai, Ở đâu, Khi nào). Để không làm lệch lịch sử khi khách đổi địa chỉ, bảng Dimension phải dùng Surrogate Key kết hợp SCD Type 2.",
      keypoints: [
        "1. Khóa đại diện (Surrogate Key): Dùng số nguyên tự tăng (customer_sk) thay vì khóa tự nhiên (customer_id) để tách biệt kho phân tích khỏi hệ thống nguồn.",
        "2. Bi kịch SCD Type 1 (Ghi đè): Nếu đè địa chỉ mới 'TP.HCM' lên dòng cũ, toàn bộ doanh thu năm ngoái ở Bình Dương bị cộng nhầm sang TP.HCM!",
        "3. Cơ học SCD Type 2: Đóng dòng cũ (end_date = '2026-10-18', is_current = false) và chèn dòng mới với customer_sk mới cho giai đoạn ở TP.HCM."
      ],
      verdict: "Quy tắc bất biến khi thiết kế Fact Table: Phải tuyên bố rõ độ mịn (Grain) ngay từ dòng đầu tiên và không bao giờ trộn lẫn 2 Grain trong 1 bảng Fact.",
      simMode: "kimball_scd2"
    },
    {
      chapter: "Chặng 5 & 6 · Từ Data Swamp Lên Open Lakehouse",
      analogy: "Tầng Nhật Ký Nguyên Tử Gác Cổng Cho Parquet",
      title: "Hóa Giải Đầm Lầy Data Swamp Bằng Open Table Formats (Delta Lake _delta_log, Apache Iceberg & Apache Hudi)",
      leadTitle: "Chặn đứng thảm họa Zombie Parquet Files khi Job Spark sập ở 60% và bài toán xóa 1 dòng GDPR",
      leadStory: "Đổ thẳng file Parquet trần trụi lên S3 biến Data Lake thành Data Swamp: khi một Job ghi 100 files bị sập ở file thứ 60, 60 files rác (Zombie Files) nằm lại làm báo cáo nhân đôi doanh thu! Open Table Formats (Delta Lake, Iceberg, Hudi) đặt một tầng Transactional Metadata Log đứng gác cổng trước các file Parquet.",
      keypoints: [
        "1. Bảng Lakehouse = Transactional Metadata + Parquet Files: Người đọc không bao giờ quét mù thư mục S3 mà hỏi trực tiếp _delta_log hoặc Iceberg Snapshot.",
        "2. Giao dịch ACID & Time Travel: Nếu Job sập ở 60%, không có file JSON commit nào được ghi vào _delta_log nên người đọc hoàn toàn không nhìn thấy 60 files rác!",
        "3. Copy-on-Write (COW) vs. Merge-on-Read (MOR): COW viết lại file Parquet mới khi UPDATE/DELETE (tối ưu đọc); MOR ghi file chênh lệch/Deletion Vector (tối ưu ghi)."
      ],
      verdict: "Open Lakehouse kết hợp chi phí lưu trữ mở siêu rẻ của Data Lake (S3 + Parquet) với độ tin cậy ACID và quản trị lược đồ của Data Warehouse.",
      simMode: "swamp_to_lakehouse"
    },
    {
      chapter: "Chặng 7 · Kiến Trúc Medallion & Data Governance",
      analogy: "Dây Chuyền Tinh Luyện 3 Cấp & Trạm Cách Ly Quarantine",
      title: "Kiến Trúc Multi-Hop Medallion (Bronze → Silver → Gold), Trạm Quarantine, Z-Ordering & 4 Trụ Cột Governance",
      leadTitle: "Khép kín hành trình Đơn hàng #8888 từ sự kiện thô đến bảng KPI chuẩn quản trị",
      leadStory: "Thay vì biến đổi 1 bước từ nguồn bẩn ra thẳng báo cáo, kiến trúc Medallion tinh luyện dữ liệu lũy tiến qua 3 tầng: Bronze (giữ nguyên bản gốc Append-only để replay), Silver (làm sạch, khử trùng lặp, áp Schema Enforcement, đẩy dòng lỗi sang Quarantine) và Gold (mô hình Star Schema / OBT phục vụ BI & AI).",
      keypoints: [
        "1. Trạm kiểm dịch Quarantine: Các bản ghi vi phạm hợp đồng dữ liệu (Data Contract) được rẽ nhánh sang bảng Quarantine thay vì làm gãy đường ống.",
        "2. Tối ưu vật lý Lakehouse: Kết hợp Compaction (OPTIMIZE gộp file nhỏ) với Z-Ordering / Liquid Clustering để gom dữ liệu đa chiều và Vacuum dọn file cũ.",
        "3. Bốn dòng chảy ngầm (Governance Undercurrents): Unity Catalog / Iceberg Catalog, OpenLineage, bảo mật dòng/cột (RLS / Masking) và FinOps."
      ],
      verdict: "Tầng Bronze là bảo hiểm sống còn giúp tái tạo lại toàn bộ tầng Silver và Gold bất cứ khi nào logic nghiệp vụ thay đổi mà không cần quét lại DB nguồn.",
      simMode: "medallion_governance"
    }
  ];

  let stg2dCurrentSlide = 0;
  const stg2dState = {
    latMode: "ram_fast",
    pqMode: "parquet_pushdown",
    distMode: "s3_decoupled",
    modMode: "scd2_history",
    lhMode: "delta_iceberg_acid",
    medMode: "medallion_flow"
  };

  function buildStorage2DSimulatorHtml() {
    return `
      <div class="infra2d-wrap" id="stg2dWidgetRoot">
        <div class="infra2d-header">
          <div class="infra2d-brand">
            <div class="infra2d-brand-icon">2D</div>
            <div>
              <div class="infra2d-brand-badges">
                <span class="infra2d-tag">Cắt Lớp Lưu Trữ, Parquet &amp; Open Lakehouse 2D</span>
                <span class="infra2d-chapter" id="stg2dChapterBadge">Chặng 1 · Tháp Độ Trễ &amp; Spill-to-Disk</span>
              </div>
              <h4 class="infra2d-title-bar">Phòng Thí Nghiệm Tương Tác D02: Hành Trình Đơn Hàng #8888 Từ Phần Cứng Đến Open Data Lakehouse</h4>
            </div>
          </div>
          <div class="infra2d-dots" id="stg2dDots"></div>
          <button type="button" class="infra2d-btn" onclick="toggleStorage2DSummaryModal()">Bảng Tóm Tắt Thông Số</button>
        </div>

        <div id="stg2dSummaryDrawer" style="display:none;padding:14px 16px;background:var(--sim-canvas);border-bottom:1px solid var(--sim-border);">
          <div style="padding:10px 12px;border-radius:8px;background:var(--sim-flow-soft);border:1px solid color-mix(in oklab, var(--sim-flow) 35%, transparent);font-size:12.5px;color:var(--sim-flow);margin-bottom:10px;">
            <strong>Chuẩn kiến trúc D02 (Storage Layer &amp; Open Lakehouse):</strong> Lưu trữ định dạng cột <strong>Apache Parquet</strong> trên <strong>Cloud Object Storage (S3/MinIO)</strong>, quản trị giao dịch <strong>ACID / Time Travel</strong> bằng <strong>Delta Lake / Apache Iceberg</strong> và quy hoạch 3 tầng <strong>Medallion (Bronze → Silver → Gold)</strong>.
          </div>
          <div class="table-wrap" style="margin:0;">
            <table class="clean-table">
              <thead>
                <tr>
                  <th>Tầng Cắt Lớp</th>
                  <th>Cơ Chế Cốt Lõi</th>
                  <th>Chuẩn Thiết Kế Production</th>
                  <th>Rủi Ro Sinh Tử Cần Chặn</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>1. Phần Cứng &amp; File</strong></td>
                  <td><code>Parquet Columnar</code> + <code>Arrow RAM</code></td>
                  <td>Row Group <code>128MB–512MB</code>, nén <code>ZSTD / Snappy</code></td>
                  <td>Dùng CSV hoặc nén Gzip không cắt nhỏ được (Non-splittable)</td>
                </tr>
                <tr>
                  <td><strong>2. Data Modeling</strong></td>
                  <td><code>Kimball Star Schema</code> + <code>SCD Type 2</code></td>
                  <td>Khóa đại diện <code>Surrogate Key</code> + Grain tường minh</td>
                  <td>Dùng SCD Type 1 ghi đè làm sai lệch báo cáo doanh thu lịch sử</td>
                </tr>
                <tr>
                  <td><strong>3. Open Lakehouse</strong></td>
                  <td><code>_delta_log</code> / <code>Iceberg Metadata Tree</code></td>
                  <td><code>MERGE INTO</code>, <code>OPTIMIZE ZORDER BY</code>, <code>VACUUM</code></td>
                  <td>Ghi Parquet trần lên S3 sinh <code>Zombie Files</code> khi Job sập giữa chừng</td>
                </tr>
                <tr>
                  <td><strong>4. Medallion &amp; Gov</strong></td>
                  <td><code>Bronze → Silver (+Quarantine) → Gold</code></td>
                  <td><code>Data Contracts</code>, <code>Unity Catalog</code>, <code>RLS/Masking</code></td>
                  <td>Biến đổi 1-hop không có tầng Bronze khiến mất khả năng Replay lịch sử</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="infra2d-grid">
          <div class="infra2d-col-left">
            <div>
              <div class="infra2d-pills">
                <span class="infra2d-pill-num" id="stg2dSlideNumPill">SLIDE 1 / 6</span>
                <span class="infra2d-pill-analogy" id="stg2dAnalogyPill">Lát Cắt Lưu Trữ</span>
              </div>
              <h3 class="infra2d-slide-h3" id="stg2dSlideTitle"></h3>
              <div class="infra2d-story-box">
                <div class="infra2d-avatar" title="Đơn hàng #8888 (Sofa 15.000.000 VNĐ)">STG</div>
                <div>
                  <span class="infra2d-story-title" id="stg2dLeadTitle"></span>
                  <p class="infra2d-story-text" id="stg2dLeadStory"></p>
                </div>
              </div>
              <div class="infra2d-keypoints" id="stg2dKeypoints"></div>
            </div>
            <div class="infra2d-verdict" id="stg2dVerdictBox"></div>
          </div>

          <div class="infra2d-col-right">
            <div>
              <div class="infra2d-sim-top">
                <div class="infra2d-sim-live">
                  <span class="infra2d-sim-dot"></span>
                  <span>Sơ Đồ Cắt Lớp Parquet, Kimball SCD2 &amp; Open Lakehouse (Animated SVG)</span>
                </div>
                <span class="infra2d-sim-hint">Bấm các nút kịch bản bên dưới để đổi cơ chế!</span>
              </div>
              <div class="infra2d-stage" id="stg2dSimStage" style="padding:10px;"></div>
            </div>
            <div>
              <div class="infra2d-status" id="stg2dSimStatusText">Sẵn sàng mô phỏng.</div>
              <div class="infra2d-controls" id="stg2dSimControls"></div>
            </div>
          </div>
        </div>

        <div class="infra2d-footer">
          <button type="button" class="infra2d-btn" id="stg2dBtnPrev" onclick="changeStorage2DSlide(-1)">← Mô Phỏng Trước</button>
          <div class="infra2d-progress-wrap">
            <div class="infra2d-progress-track">
              <div class="infra2d-progress-fill" id="stg2dProgressFill" style="width:16.6%;"></div>
            </div>
            <span class="infra2d-progress-label" id="stg2dProgressLabel">Mô phỏng 1 / 6</span>
          </div>
          <button type="button" class="infra2d-btn infra2d-btn-primary" id="stg2dBtnNext" onclick="changeStorage2DSlide(1)">Mô Phỏng Tiếp Theo →</button>
        </div>
      </div>
    `;
  }

  function toggleStorage2DSummaryModal() {
    const el = document.getElementById("stg2dSummaryDrawer");
    if (el) el.style.display = el.style.display === "none" ? "block" : "none";
  }

  function changeStorage2DSlide(delta) {
    stg2dCurrentSlide = (stg2dCurrentSlide + delta + STORAGE2D_SLIDES.length) % STORAGE2D_SLIDES.length;
    renderStorage2DSlide();
  }

  function jumpStorage2DSlide(idx) {
    stg2dCurrentSlide = idx;
    renderStorage2DSlide();
  }

  function renderStorage2DSlide() {
    const s = STORAGE2D_SLIDES[stg2dCurrentSlide];
    if (!s) return;
    const chEl = document.getElementById("stg2dChapterBadge");
    if (!chEl) return;
    chEl.textContent = s.chapter;
    document.getElementById("stg2dSlideNumPill").textContent = `SLIDE ${stg2dCurrentSlide + 1} / ${STORAGE2D_SLIDES.length}`;
    document.getElementById("stg2dAnalogyPill").textContent = s.analogy;
    document.getElementById("stg2dSlideTitle").textContent = s.title;
    document.getElementById("stg2dLeadTitle").textContent = s.leadTitle;
    document.getElementById("stg2dLeadStory").textContent = s.leadStory;
    document.getElementById("stg2dKeypoints").innerHTML = s.keypoints
      .map(kp => `<div class="infra2d-kp"><span class="infra2d-kp-dot"></span><span>${escapeHtml(kp)}</span></div>`)
      .join("");
    document.getElementById("stg2dVerdictBox").innerHTML = `<strong>Chốt nguyên lý:</strong> ${escapeHtml(s.verdict)}`;
    document.getElementById("stg2dDots").innerHTML = STORAGE2D_SLIDES.map(
      (_, i) => `<button type="button" class="infra2d-dot ${i === stg2dCurrentSlide ? 'active' : ''}" onclick="jumpStorage2DSlide(${i})" title="Slide ${i + 1}">${i + 1}</button>`
    ).join("");
    const pct = (((stg2dCurrentSlide + 1) / STORAGE2D_SLIDES.length) * 100).toFixed(1);
    document.getElementById("stg2dProgressFill").style.width = `${pct}%`;
    document.getElementById("stg2dProgressLabel").textContent = `Mô phỏng ${stg2dCurrentSlide + 1} / ${STORAGE2D_SLIDES.length}`;
    renderStorage2DInteractiveStage(s.simMode);
  }

  function renderStorage2DInteractiveStage(mode) {
    const stage = document.getElementById("stg2dSimStage");
    const status = document.getElementById("stg2dSimStatusText");
    const ctrls = document.getElementById("stg2dSimControls");
    if (!stage || !status || !ctrls) return;

    if (mode === "latency_spill") {
      const m = stg2dState.latMode;
      const isSpill = m === "spill_thrash";
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="150" y="20" width="260" height="36" rx="6" fill="var(--sim-card)" stroke="var(--sim-ok)" stroke-width="1.5"/>
          <text x="165" y="42" fill="var(--sim-ok)" font-size="9.2" font-weight="700" font-family="var(--cds-font-mono)">HOT · CPU L1/L3 (~1ns) &amp; RAM (~100ns)</text>

          <rect x="95" y="66" width="370" height="40" rx="6" fill="${isSpill ? 'var(--sim-warn-soft)' : 'var(--sim-card)'}" stroke="${isSpill ? 'var(--sim-danger)' : 'var(--sim-flow)'}" stroke-width="1.5"/>
          <text x="112" y="90" fill="${isSpill ? 'var(--sim-danger)' : 'var(--sim-flow)'}" font-size="9.2" font-weight="700" font-family="var(--cds-font-mono)">WARM · Local NVMe SSD (~100 µs) ${isSpill ? '← SPILL-TO-DISK!' : ''}</text>

          <rect x="35" y="116" width="490" height="46" rx="6" fill="var(--sim-flow-soft)" stroke="var(--sim-clay)" stroke-width="1.6"/>
          <text x="52" y="143" fill="var(--sim-clay)" font-size="9.2" font-weight="700" font-family="var(--cds-font-mono)">COLD / LAKEHOUSE · Cloud Object Storage S3 / MinIO (~50–100 ms)</text>

          <rect x="35" y="174" width="490" height="44" rx="6" fill="var(--sim-card-alt)" stroke="var(--sim-border)"/>
          <text x="48" y="200" fill="var(--sim-ink)" font-size="9.2" font-weight="700" font-family="var(--cds-font-mono)">${isSpill ? 'Tràn bộ nhớ RAM buộc hệ thống ghi/đọc tạm xuống đĩa (Spill), làm tốc độ giảm 1.000x!' : 'Quy hoạch chuẩn: Xử lý nóng trên RAM/NVMe, lưu trữ lịch sử lâu dài trên S3 Parquet.'}</text>
        </svg>
      `;
      status.textContent = isSpill
        ? "Cảnh báo Spill-to-Disk: Khi tập dữ liệu vượt quá vùng nhớ RAM, CPU phải chờ I/O đĩa chậm gấp hàng nghìn lần."
        : "Tháp độ trễ vật lý: Kết hợp bộ nhớ tốc độ cao cho luồng nóng (Hot) và Object Storage giá rẻ cho luồng lạnh (Cold).";
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${!isSpill ? 'infra2d-btn-emerald' : ''}" onclick="stg2dState.latMode='ram_fast';renderStorage2DInteractiveStage('latency_spill')">1. Xử Lý Trong RAM &amp; Phân Tầng Nhiệt Độ</button>
        <button type="button" class="infra2d-btn ${isSpill ? 'infra2d-btn-danger' : ''}" onclick="stg2dState.latMode='spill_thrash';renderStorage2DInteractiveStage('latency_spill')">2. Giả Lập Tràn RAM (Spill-to-Disk)</button>
      `;
    } else if (mode === "parquet_arrow") {
      const m = stg2dState.pqMode;
      const isCsv = m === "csv_row_scan";
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          ${isCsv ? `
            <rect x="24" y="34" width="512" height="140" rx="8" fill="var(--sim-warn-soft)" stroke="var(--sim-danger)" stroke-width="1.6"/>
            <text x="36" y="58" fill="var(--sim-danger)" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">ĐỊNH DẠNG THEO DÒNG (ROW-ORIENTED CSV — QUÉT THỪA 96% DỮ LIỆU)</text>
            <text x="36" y="86" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">Row 1: [order_id | user_id | address_500B | note_800B | amount=15M | ... 95 cột khác]</text>
            <text x="36" y="112" fill="var(--sim-danger)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">→ Dù chỉ SELECT amount, đầu đọc vẫn phải lướt qua toàn bộ 100 cột của mọi dòng!</text>
          ` : `
            <rect x="24" y="28" width="330" height="148" rx="7" fill="var(--sim-card)" stroke="var(--sim-ok)" stroke-width="1.6"/>
            <text x="34" y="50" fill="var(--sim-ok)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">APACHE PARQUET (HYBRID COLUMNAR)</text>
            <text x="34" y="76" fill="var(--sim-ok)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">• Đọc đúng Column Chunk [amount] (Bỏ qua 98 cột!)</text>
            <text x="34" y="100" fill="var(--sim-flow)" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">• Footer Min/Max: Nhảy qua Row Group không khớp!</text>
            <text x="34" y="124" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">• Nén RLE + Dictionary + ZSTD cùng kiểu dữ liệu</text>

            <rect x="370" y="28" width="166" height="148" rx="7" fill="var(--sim-flow-soft)" stroke="var(--sim-clay)" stroke-width="1.5"/>
            <text x="380" y="50" fill="var(--sim-clay)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">APACHE ARROW (RAM)</text>
            <text x="380" y="78" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">Bộ đệm cột liền kề</text>
            <text x="380" y="100" fill="var(--sim-ok)" font-size="8.8" font-weight="700" font-family="var(--cds-font-mono)">Zero-Copy IPC</text>
            <text x="380" y="122" fill="var(--sim-ink)" font-size="8.5" font-family="var(--cds-font-mono)">Spark ↔ DuckDB ↔ Python</text>
          `}
          <rect x="24" y="188" width="512" height="34" rx="6" fill="var(--sim-card-alt)" stroke="var(--sim-border)"/>
          <text x="36" y="209" fill="var(--sim-ink)" font-size="9.2" font-weight="700" font-family="var(--cds-font-mono)">${isCsv ? 'CSV: Không có thống kê Min/Max, không cắt tỉa được cột, tốn 100% băng thông đọc đĩa.' : 'Parquet + Arrow: Cắt giảm 90–98% lượng byte đọc từ S3 và truyền thẳng vào CPU SIMD Vector.'}</text>
        </svg>
      `;
      status.textContent = isCsv
        ? "Đọc tệp CSV theo dòng: Phải đọc toàn bộ tệp từ đầu đến cuối và tốn CPU tách chuỗi theo dấu phẩy."
        : "Đọc tệp Parquet + Arrow: Kết hợp Column Pruning (cắt cột) và Predicate Pushdown (nhảy Row Group qua Footer Min/Max).";
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${!isCsv ? 'infra2d-btn-emerald' : ''}" onclick="stg2dState.pqMode='parquet_pushdown';renderStorage2DInteractiveStage('parquet_arrow')">1. Parquet Pushdown + Arrow Zero-Copy</button>
        <button type="button" class="infra2d-btn ${isCsv ? 'infra2d-btn-danger' : ''}" onclick="stg2dState.pqMode='csv_row_scan';renderStorage2DInteractiveStage('parquet_arrow')">2. Đối Chiếu Quét Toàn Bảng CSV</button>
      `;
    } else if (mode === "hdfs_object_dwh") {
      const m = stg2dState.distMode;
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="22" y="30" width="250" height="145" rx="7" fill="var(--sim-card)" stroke="var(--sim-flow)" stroke-width="1.5"/>
          <text x="32" y="52" fill="var(--sim-flow)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">HADOOP HDFS (GẮN CHẶT COMPUTE-STORAGE)</text>
          <text x="32" y="78" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">• NameNode giữ toàn bộ Metadata trên RAM</text>
          <text x="32" y="100" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">• DataNodes lưu Block 128MB nhân bản 3x</text>
          <text x="32" y="124" fill="var(--sim-danger)" font-size="8.8" font-weight="700" font-family="var(--cds-font-mono)">• Muốn thêm đĩa phải mua thêm cả máy chủ!</text>

          <rect x="288" y="30" width="250" height="145" rx="7" fill="var(--sim-flow-soft)" stroke="var(--sim-ok)" stroke-width="1.6"/>
          <text x="298" y="52" fill="var(--sim-ok)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">CLOUD OBJECT STORAGE (S3 / MINIO)</text>
          <text x="298" y="78" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">• Không gian phẳng Bucket + Key + Object</text>
          <text x="298" y="100" fill="var(--sim-ok)" font-size="8.8" font-weight="700" font-family="var(--cds-font-mono)">• Tách rời hoàn toàn Compute và Storage!</text>
          <text x="298" y="124" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">• Bất biến (Immutable PUT/GET qua HTTP)</text>
        </svg>
      `;
      status.textContent = m === "s3_decoupled"
        ? "Cloud Object Storage (S3/MinIO): Cho phép tắt cụm Spark/Trino khi không chạy truy vấn mà dữ liệu vẫn an toàn tuyệt đối."
        : "Hadoop HDFS truyền thống: Cắt file thành các khối 128 MB nhân bản 3x qua nhiều Rack, nhưng bị giới hạn bởi RAM của NameNode.";
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${m === 's3_decoupled' ? 'infra2d-btn-emerald' : ''}" onclick="stg2dState.distMode='s3_decoupled';renderStorage2DInteractiveStage('hdfs_object_dwh')">1. Cloud Object Storage (Tách Rời Compute)</button>
        <button type="button" class="infra2d-btn ${m === 'hdfs_3x_rack' ? 'infra2d-btn-cyan' : ''}" onclick="stg2dState.distMode='hdfs_3x_rack';renderStorage2DInteractiveStage('hdfs_object_dwh')">2. HDFS 128MB Blocks &amp; 3x Replication</button>
      `;
    } else if (mode === "kimball_scd2") {
      const m = stg2dState.modMode;
      const isScd1 = m === "scd1_overwrite";
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="24" y="28" width="512" height="150" rx="8" fill="${isScd1 ? 'var(--sim-warn-soft)' : 'var(--sim-card)'}" stroke="${isScd1 ? 'var(--sim-danger)' : 'var(--sim-ok)'}" stroke-width="1.6"/>
          <text x="36" y="52" fill="${isScd1 ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">${isScd1 ? 'SAI LẦM SCD TYPE 1: GHI ĐÈ ĐỊA CHỈ LÀM MẤT LỊCH SỬ BÌNH DƯƠNG!' : 'CHUẨN KIMBALL SCD TYPE 2: BẢO TOÀN 100% LỊCH SỬ THEO THỜI GIAN'}</text>
          <text x="36" y="80" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">${isScd1 ? 'dim_customer: [sk=101 | id=KH_A | city="TP.HCM" (Đã đè mất Bình Dương!)]' : 'Dòng 1 (Cũ): [sk=101 | id=KH_A | city="Bình Dương" | is_current=false | end=2026-10]'}</text>
          <text x="36" y="104" fill="var(--sim-ok)" font-size="8.8" font-weight="700" font-family="var(--cds-font-mono)">${isScd1 ? '' : 'Dòng 2 (Mới): [sk=205 | id=KH_A | city="TP.HCM"     | is_current=true  | end=9999-12]'}</text>
          <text x="36" y="134" fill="${isScd1 ? 'var(--sim-danger)' : 'var(--sim-flow)'}" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">${isScd1 ? '→ Đơn #8888 (15 triệu) đặt năm ngoái ở Bình Dương bị cộng nhầm sang TP.HCM!' : '→ Đơn #8888 nối với sk=101 (Bình Dương); đơn mới nối với sk=205 (TP.HCM)!'}</text>
        </svg>
      `;
      status.textContent = isScd1
        ? "Bi kịch SCD Type 1: Ghi đè thuộc tính trên bảng Dimension làm thay đổi toàn bộ báo cáo doanh thu quá khứ."
        : "Chuẩn SCD Type 2: Cấp Surrogate Key mới (sk=205) khi khách chuyển nhà, giúp Fact Table giữ nguyên sự thật lịch sử.";
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${!isScd1 ? 'infra2d-btn-emerald' : ''}" onclick="stg2dState.modMode='scd2_history';renderStorage2DInteractiveStage('kimball_scd2')">1. Kimball Star Schema + SCD Type 2</button>
        <button type="button" class="infra2d-btn ${isScd1 ? 'infra2d-btn-danger' : ''}" onclick="stg2dState.modMode='scd1_overwrite';renderStorage2DInteractiveStage('kimball_scd2')">2. Giả Lập Lỗi Ghi Đè SCD Type 1</button>
      `;
    } else if (mode === "swamp_to_lakehouse") {
      const m = stg2dState.lhMode;
      const isSwamp = m === "swamp_zombie";
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="24" y="30" width="512" height="148" rx="8" fill="${isSwamp ? 'var(--sim-warn-soft)' : 'var(--sim-card)'}" stroke="${isSwamp ? 'var(--sim-danger)' : 'var(--sim-ok)'}" stroke-width="1.6"/>
          <text x="36" y="54" fill="${isSwamp ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="10" font-weight="700" font-family="var(--cds-font-mono)">${isSwamp ? 'THẢM HỌA DATA SWAMP: JOB SẬP Ở 60% ĐỂ LẠI ZOMBIE PARQUET FILES!' : 'OPEN LAKEHOUSE (DELTA LAKE _delta_log / APACHE ICEBERG SNAPSHOT)'}</text>
          <text x="36" y="82" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">${isSwamp ? '• Không có Transaction Log: 60/100 file Parquet rác nằm lẫn với dữ liệu thật!' : '• Mọi thao tác đọc/ghi đi qua nhật ký nguyên tử 00001.json / Manifest List'}</text>
          <text x="36" y="106" fill="${isSwamp ? 'var(--sim-danger)' : 'var(--sim-ok)'}" font-size="9" font-weight="700" font-family="var(--cds-font-mono)">${isSwamp ? '• Engine đọc quét mù s3://bucket/*.parquet → Báo cáo sai lệch nghiêm trọng!' : '• Giao dịch ACID + Time Travel (VERSION AS OF): Chặn 100% Zombie Files!'}</text>
          <text x="36" y="132" fill="var(--sim-ink)" font-size="9" font-family="var(--cds-font-mono)">• Hỗ trợ UPDATE / DELETE / MERGE INTO trực tiếp trên S3 qua COW &amp; MOR</text>
        </svg>
      `;
      status.textContent = isSwamp
        ? "Bi kịch Data Swamp: Ghi trực tiếp các file Parquet rời rạc không có lớp siêu dữ liệu nguyên tử dẫn tới dữ liệu bẩn khi Job lỗi."
        : "Open Table Formats (Delta Lake / Iceberg / Hudi): Bọc tầng Transactional Metadata bên trên Parquet để mang ACID lên S3.";
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${!isSwamp ? 'infra2d-btn-emerald' : ''}" onclick="stg2dState.lhMode='delta_iceberg_acid';renderStorage2DInteractiveStage('swamp_to_lakehouse')">1. Open Lakehouse ACID (_delta_log / Iceberg)</button>
        <button type="button" class="infra2d-btn ${isSwamp ? 'infra2d-btn-danger' : ''}" onclick="stg2dState.lhMode='swamp_zombie';renderStorage2DInteractiveStage('swamp_to_lakehouse')">2. Giả Lập Data Swamp (Zombie Files)</button>
      `;
    } else {
      const m = stg2dState.medMode;
      stage.innerHTML = `
        <svg viewBox="0 0 560 245" style="width:100%;height:auto;display:block;">
          <rect x="10" y="10" width="540" height="225" rx="10" fill="var(--sim-canvas)" stroke="var(--sim-border)"/>
          <rect x="20" y="34" width="155" height="115" rx="7" fill="var(--sim-card)" stroke="var(--sim-clay)" stroke-width="1.5"/>
          <text x="30" y="56" fill="var(--sim-clay)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">1. BRONZE (RAW)</text>
          <text x="30" y="80" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">Append-Only CDC/JSON</text>
          <text x="30" y="102" fill="var(--sim-ok)" font-size="8.5" font-weight="700" font-family="var(--cds-font-mono)">Bảo hiểm Replay 100%</text>

          <rect x="202" y="34" width="156" height="115" rx="7" fill="var(--sim-flow-soft)" stroke="var(--sim-flow)" stroke-width="1.6"/>
          <text x="212" y="56" fill="var(--sim-flow)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">2. SILVER (CLEANED)</text>
          <text x="212" y="80" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">Khử trùng + SCD Type 2</text>
          <text x="212" y="102" fill="var(--sim-danger)" font-size="8.5" font-weight="700" font-family="var(--cds-font-mono)">Dòng bẩn → Quarantine!</text>

          <rect x="384" y="34" width="156" height="115" rx="7" fill="var(--sim-card-alt)" stroke="var(--sim-ok)" stroke-width="1.6"/>
          <text x="394" y="56" fill="var(--sim-ok)" font-size="9.5" font-weight="700" font-family="var(--cds-font-mono)">3. GOLD (CURATED)</text>
          <text x="394" y="80" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">Star Schema &amp; OBT</text>
          <text x="394" y="102" fill="var(--sim-ok)" font-size="8.5" font-weight="700" font-family="var(--cds-font-mono)">Z-Order + Liquid Cluster</text>

          <rect x="20" y="164" width="520" height="54" rx="7" fill="var(--sim-card)" stroke="var(--sim-border)"/>
          <text x="32" y="186" fill="var(--sim-flow)" font-size="9.2" font-weight="700" font-family="var(--cds-font-mono)">NỀN TẢNG QUẢN TRỊ XUYÊN SUỐT (DATA GOVERNANCE UNDERCURRENTS)</text>
          <text x="32" y="206" fill="var(--sim-ink)" font-size="8.8" font-family="var(--cds-font-mono)">Unity Catalog · Data Contracts · OpenLineage · Row-Level Security &amp; Column Masking · FinOps</text>

          <circle r="4.5" fill="var(--sim-ok)">
            <animate attributeName="cx" values="175;202;358;384" dur="2.2s" repeatCount="indefinite"/>
            <animate attributeName="cy" values="90;90;90;90" dur="2.2s" repeatCount="indefinite"/>
          </circle>
        </svg>
      `;
      status.textContent = m === "medallion_flow"
        ? "Kiến trúc Multi-Hop Medallion: Tinh luyện Đơn hàng #8888 qua 3 tầng Bronze → Silver → Gold với nền tảng Data Governance."
        : "Trạm cách ly Quarantine & Z-Ordering: Cô lập bản ghi vi phạm hợp đồng dữ liệu và tối ưu bố cục tệp đa chiều trên Gold.";
      ctrls.innerHTML = `
        <button type="button" class="infra2d-btn ${m === 'medallion_flow' ? 'infra2d-btn-emerald' : ''}" onclick="stg2dState.medMode='medallion_flow';renderStorage2DInteractiveStage('medallion_governance')">1. Luồng Medallion (Bronze → Silver → Gold)</button>
        <button type="button" class="infra2d-btn ${m === 'quarantine_gate' ? 'infra2d-btn-cyan' : ''}" onclick="stg2dState.medMode='quarantine_gate';renderStorage2DInteractiveStage('medallion_governance')">2. Trạm Quarantine &amp; Z-Ordering</button>
      `;
    }
  }
"""
