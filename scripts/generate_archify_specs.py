#!/usr/bin/env python3
"""Generate the 26 additional Archify specs for the first three FSDS lessons.

The 9 existing delivered specs remain hand-authored source of truth. This generator
owns only the additional L/P/D catalog entries listed in GENERATED.
"""
from pathlib import Path
import json

OUT = Path(__file__).resolve().parents[1] / "archify" / "specs"
OUT.mkdir(parents=True, exist_ok=True)


def cards(remember, evidence):
    return [
        {"dot": "cyan", "title": "Cơ chế cần giữ", "items": remember},
        {"dot": "orange", "title": "Bằng chứng để kiểm tra", "items": evidence},
    ]


def write(name, spec):
    spec["meta"].setdefault("output", f"{name}.html")
    spec["meta"].setdefault("quality_profile", "showcase")
    path = OUT / f"{name}.json"
    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
    return path


def architecture(name, title, subtitle, nodes, edges, *, views, card_data, boundaries=None):
    components=[]
    for n in nodes:
        item={"id":n[0],"type":n[1],"label":n[2],"sublabel":n[3],"pos":[n[4],n[5]],"size":[n[6],n[7]]}
        if len(n)>8 and n[8]: item["tag"]=n[8]
        components.append(item)
    connections=[]
    for i,e in enumerate(edges):
        item={"id":e[0] or f"edge-{i+1}","from":e[1],"to":e[2],"label":e[3]}
        if len(e)>4 and e[4]: item["variant"]=e[4]
        item["labelDy"] = -58
        connections.append(item)
    spec={
        "schema_version":1,"diagram_type":"architecture",
        "meta":{"title":title,"subtitle":subtitle,"viewBox":[1220,680],"visual_preset":"editorial","views":views},
        "components":components,"connections":connections,"cards":cards(*card_data)
    }
    if boundaries: spec["boundaries"]=boundaries
    return write(name,spec)


def workflow(name,title,subtitle,lanes,nodes,edges,*,views,card_data,main_path=None):
    ns=[]
    for n in nodes:
        item={"id":n[0],"lane":n[1],"col":n[2],"type":n[3],"label":n[4],"sublabel":n[5],"width":142}
        if len(n)>6 and n[6]: item["tag"]=n[6]
        ns.append(item)
    buckets = {}
    for item in ns:
        buckets.setdefault((item["lane"], item["col"]), []).append(item)
    for group in buckets.values():
        if len(group) > 1:
            spacing = 82
            start = -spacing * (len(group) - 1) / 2
            for index, item in enumerate(group):
                item["yOffset"] = start + spacing * index
    es=[]
    for i,e in enumerate(edges):
        item={"id":e[0] or f"edge-{i+1}","from":e[1],"to":e[2],"variant":e[4] if len(e)>4 and e[4] else "default"}
        if e[3]: item["label"]=e[3]
        if len(e)>5 and e[5]: item["role"]=e[5]
        es.append(item)
    spec={
        "schema_version":2,"diagram_type":"workflow",
        "meta":{"title":title,"subtitle":subtitle,"animation":"trace","visual_preset":"signal-flow","views":views},
        "lanes":[{"id":x[0],"label":x[1],**({"variant":x[2]} if len(x)>2 and x[2] else {})} for x in lanes],
        "nodes":ns,"edges":es,"cards":cards(*card_data)
    }
    if main_path: spec["mainPath"]=main_path
    return write(name,spec)


def sequence(name,title,subtitle,participants,messages,*,views,card_data):
    ms=[]
    y=190
    activations=[]
    for i,m in enumerate(messages):
        item={"id":m[0] or f"message-{i+1}","from":m[1],"to":m[2],"y":y,"label":m[3],"variant":m[4] if len(m)>4 and m[4] else "default"}
        if len(m)>5 and m[5]: item["note"]=m[5]
        ms.append(item); y += 88
    for pid in [p[0] for p in participants[1:-1]]:
        relevant=[m["y"] for m in ms if m["from"]==pid or m["to"]==pid]
        if relevant: activations.append({"participant":pid,"from":min(relevant)-12,"to":max(relevant)+38,"type":"backend"})
    return write(name,{
        "schema_version":1,"diagram_type":"sequence",
        "meta":{"title":title,"subtitle":subtitle,"viewBox":[1000,max(760,y+120)],"animation":"trace","visual_preset":"signal-flow","column_fit":"spread","views":views},
        "participants":[{"id":p[0],"type":p[1],"label":p[2],"sublabel":p[3]} for p in participants],
        "segments":[{"from":170,"to":y-45,"label":"đường chạy quan sát được"}],
        "messages":ms,"activations":activations,"cards":cards(*card_data)
    })


def dataflow(name,title,subtitle,stages,nodes,flows,*,views,card_data):
    ns=[]
    for n in nodes:
        item={"id":n[0],"type":n[1],"label":n[2],"sublabel":n[3],"stage":n[4],"row":n[5]}
        ns.append(item)
    fs=[]
    for i,f in enumerate(flows):
        fs.append({"id":f[0] or f"flow-{i+1}","from":f[1],"to":f[2],"label":f[3],"classification":f[4],"variant":f[5] if len(f)>5 and f[5] else "emphasis","route":"straight"})
    return write(name,{
        "schema_version":1,"diagram_type":"dataflow",
        "meta":{"title":title,"subtitle":subtitle,"viewBox":[1080,720],"animation":"trace","visual_preset":"signal-flow","views":views},
        "stages":[{"label":s} for s in stages],"nodes":ns,"flows":fs,"cards":cards(*card_data)
    })


def lifecycle(name,title,subtitle,lanes,states,transitions,*,views,card_data):
    ss=[]
    for s in states:
        item={"id":s[0],"type":s[1],"label":s[2],"sublabel":s[3],"lane":s[4],"col":s[5],"step":str(s[6]).zfill(2),"tag":s[7]}
        ss.append(item)
    ts=[]
    for i,t in enumerate(transitions):
        ts.append({"id":t[0] or f"transition-{i+1}","from":t[1],"to":t[2],"label":t[3],"variant":t[4] if len(t)>4 and t[4] else "emphasis"})
    return write(name,{
        "schema_version":1,"diagram_type":"lifecycle",
        "meta":{"title":title,"subtitle":subtitle,"viewBox":[1030,680],"animation":"trace","views":views},
        "lanes":[{"id":x[0],"label":x[1]} for x in lanes],"states":ss,"transitions":ts,"cards":cards(*card_data)
    })


def v(id,label,focus,note): return {"id":id,"label":label,"focus":focus,"note":note}

# ── Linux ────────────────────────────────────────────────────────────────────
sequence("linux-command-execution-sequence","cat không tự đọc đĩa","Từ phím bấm tới byte trên terminal",
 [("user","external","Bạn","ý định"),("terminal","external","Terminal","nhận ký tự"),("shell","backend","Bash","parse argv + PATH"),("process","backend","cat process","file descriptors"),("kernel","backend","Kernel","permission + syscall"),("fs","database","Filesystem","inode + bytes"),("output","external","Terminal output","stdout / stderr")],
 [("type","user","terminal","gõ cat /etc/os-release","emphasis"),("line","terminal","shell","giao command line","default"),("parse","shell","process","exec /usr/bin/cat","emphasis"),("open","process","kernel","open(path)","default"),("read","kernel","fs","đọc inode + block","emphasis"),("bytes","fs","process","trả byte","return"),("stdout","process","output","write stdout","return"),("deny","kernel","output","EACCES → stderr","security","Nhánh lỗi kết thúc với exit status khác 0.")],
 views=[v("happy","Đường thành công",["user","terminal","shell","process","kernel","fs","output"],"Theo dữ liệu từ command tới stdout."),v("failure","Permission failure",["process","kernel","output"],"Dừng tại kernel khi identity không có quyền.")],
 card_data=(["Shell parse; process thực thi; kernel kiểm soát tài nguyên","stdout và stderr là hai hợp đồng khác nhau"],["strace cho thấy open/read/write","exit status và stderr chứng minh lỗi"]))

workflow("linux-path-permission-workflow","Path và permission được kiểm tra ở đâu","cwd tạo path; identity quyết định quyền",
 [("resolve","Resolve path"),("authorize","Kernel authorization"),("outcome","Observed outcome")],
 [("cwd","resolve",0,"external","cwd","/home/student","điểm xuất phát"),("relative","resolve",1,"frontend","report.log","relative path","cwd + name"),("absolute","resolve",2,"frontend","Absolute path","/home/student/report.log","canonical intent"),("identity","authorize",1,"security","uid / gid","owner · group · other","subject"),("mode","authorize",2,"security","r w x bits","permission matrix","object"),("check","authorize",3,"backend","Kernel check","path walk + access","decision"),("ok","outcome",4,"database","File opened","fd returned","read allowed"),("deny","outcome",4,"security","EACCES","stderr + exit != 0","denied")],
 [("resolve-rel","cwd","relative","join","default"),("normalize","relative","absolute","resolve","emphasis"),("who","identity","check","subject","security"),("what","mode","check","mode bits","security"),("allow","check","ok","allowed","emphasis"),("reject","check","deny","denied","security","error")],
 main_path=["cwd","relative","absolute"],
 views=[v("path","Path resolution",["cwd","relative","absolute"],"Relative path chỉ có nghĩa khi biết cwd."),v("permission","Permission decision",["identity","mode","check","ok","deny"],"Kernel đối chiếu subject với mode bits.")],
 card_data=(["Absolute path bắt đầu từ /; relative path bắt đầu từ cwd","x trên directory cho phép traverse, không đồng nghĩa đọc nội dung file"],["pwd + realpath xác nhận vị trí","id + ls -ld từng directory xác nhận quyền"]))

architecture("linux-syscall-layer-architecture","System call là ranh giới","User space xin; kernel quyết định và điều phối",
 [("app","backend","User process","cat / python / nginx",70,260,170,72,"user space"),("libc","backend","libc / runtime","wrapper + ABI",300,260,170,72,"boundary prep"),("syscall","security","System-call gate","open · read · write",530,260,180,72,"privilege switch"),("kernel","backend","Kernel core","policy + ownership",770,260,170,72,"kernel space"),("sched","cloud","Scheduler","CPU time",1010,100,150,64,"resource"),("memory","cloud","VM subsystem","address space",1010,235,150,64,"resource"),("vfs","database","VFS + driver","file / device / net",1010,370,150,64,"resource")],
 [("call","app","libc","function call","default"),("trap","libc","syscall","syscall instruction","emphasis"),("dispatch","syscall","kernel","validate + dispatch","security"),("cpu","kernel","sched","schedule","default"),("ram","kernel","memory","map pages","default"),("io","kernel","vfs","I/O request","emphasis")],
 views=[v("boundary","Privilege boundary",["app","libc","syscall","kernel"],"Không gọi trực tiếp driver từ user space."),v("resources","Kernel resources",["kernel","sched","memory","vfs"],"Kernel biến request thành CPU, memory hoặc I/O work.")],
 card_data=(["Library call có thể ở user space; system call đổi quyền thực thi","Kernel giữ isolation và ownership của tài nguyên"],["strace đo syscall thật","/proc và perf cho biết CPU/memory/I/O"]),
 boundaries=[{"kind":"region","label":"User space","wraps":["app","libc"],"pad":26},{"kind":"region","label":"Kernel space","wraps":["syscall","kernel","sched","memory","vfs"],"pad":26}])

workflow("linux-script-contract-workflow","Một script đáng tin có hợp đồng","Validate trước; chạy có kiểm soát; kết thúc có bằng chứng",
 [("entry","Entry contract"),("work","Controlled execution"),("result","Outcome")],
 [("shebang","entry",0,"frontend","Shebang","chọn interpreter","entry"),("strict","entry",1,"security","Strict mode","set -Eeuo pipefail","guard"),("input","entry",2,"security","Input readable?","path + permission","decision"),("pipeline","work",3,"backend","Run pipeline","quote + streams","work"),("temp","work",4,"database","Write safely","temp → atomic move","artifact"),("success","result",5,"backend","Exit 0","output + log","success"),("failure","result",5,"security","Exit non-zero","stderr + cleanup","failure")],
 [("a","shebang","strict","start","default"),("b","strict","input","validate","security"),("c","input","pipeline","yes","emphasis"),("d","pipeline","temp","produce","emphasis"),("e","temp","success","commit","emphasis"),("f","input","failure","no","security","error"),("g","pipeline","failure","command failed","security","error")],
 main_path=["shebang","strict","input","pipeline","temp","success"],
 views=[v("contract","Happy path",["shebang","strict","input","pipeline","temp","success"],"Đi từ interpreter tới output atomically."),v("failure","Failure contract",["strict","input","pipeline","failure"],"Lỗi phải dừng đúng chỗ và để lại evidence.")],
 card_data=(["Quote biến; validate input; giữ stdout sạch","Strict mode là guardrail, không thay thế error design"],["shellcheck kiểm tra syntax patterns","exit code + stderr + output checksum kiểm tra run"]))

dataflow("linux-compilation-dataflow","Source trở thành executable qua bốn artifact","Mỗi tool đổi representation và tạo loại lỗi riêng",
 ["Source","Preprocess","Compile","Assemble","Link"],
 [("c","frontend","hello.c","C source",0,0,"text"),("i","messagebus","hello.i","expanded source",1,0,"artifact"),("s","messagebus","hello.s","assembly",2,0,"artifact"),("o","database","hello.o","object code",3,0,"artifact"),("bin","backend","hello","executable",4,0,"artifact")],
 [("cpp","c","i","cpp","include + macro","emphasis"),("cc","i","s","compiler","syntax + type","emphasis"),("as","s","o","assembler","machine code","emphasis"),("ld","o","bin","linker","symbols + libraries","emphasis")],
 views=[v("artifacts","Artifact chain",["c","i","s","o","bin"],"Theo representation thay đổi sau mỗi tool."),v("errors","Failure boundary",["c","i","s","o","bin"],"Tên artifact cho biết lỗi thuộc stage nào.")],
 card_data=(["Compiler không trực tiếp tạo mọi executable trong một bước","Object file chưa chạy được cho tới khi linker giải quyết symbol"],["gcc -E/-S/-c dừng ở từng stage","file + nm + ldd kiểm tra artifact"]))

workflow("linux-make-dependency-workflow","Make đọc dependency graph, không đoán command","Timestamp làm bẩn node rồi lan xuống target",
 [("source","Sources"),("build","Derived artifacts"),("decision","Incremental decision")],
 [("c","source",0,"frontend","main.c","source changed","dirty"),("h","source",0,"frontend","common.h","header changed","dirty"),("maino","build",1,"database","main.o","depends on .c + .h","target"),("utilo","build",1,"database","util.o","depends on util.c + .h","target"),("binary","build",2,"backend","app","links objects","target"),("compare","decision",3,"security","Timestamp check","prerequisite newer?","decision"),("skip","decision",4,"external","Up to date","skip recipe","clean"),("rebuild","decision",4,"backend","Run recipe","rebuild downstream","dirty")],
 [("a","c","maino","compile","emphasis"),("b","h","maino","invalidate","default"),("c2","h","utilo","invalidate","default"),("d","maino","binary","link","emphasis"),("e","utilo","binary","link","emphasis"),("f","binary","compare","inspect graph","default"),("g","compare","skip","no","default"),("h2","compare","rebuild","yes","emphasis")],
 main_path=["c","maino","binary","compare","rebuild"],
 views=[v("graph","Dependency graph",["c","h","maino","utilo","binary"],"Đổi header có thể làm bẩn nhiều object."),v("decision","Incremental decision",["binary","compare","skip","rebuild"],"Make chỉ chạy recipe khi target thiếu hoặc cũ.")],
 card_data=(["Dependency quyết định thứ tự; recipe quyết định cách build","Một source change chỉ invalidate downstream targets liên quan"],["make -n cho biết recipe sẽ chạy","touch source rồi quan sát target timestamps"]))

architecture("linux-synthesis-architecture","Linux: sáu câu hỏi để không học vẹt","Một command được định vị bằng parser, state, resource và evidence",
 [("root","backend","Một command","ý định đang chạy",500,270,210,78,"root"),("parse","frontend","Ai parse?","terminal ≠ shell",80,90,180,68,"language"),("place","cloud","State ở đâu?","cwd · env · process",80,430,180,68,"context"),("resource","cloud","Tài nguyên nào?","CPU · RAM · I/O",930,90,180,68,"kernel"),("stream","messagebus","Kênh nào?","stdin · stdout · stderr",930,430,180,68,"contract"),("repeat","database","Làm lại thế nào?","script · Make",180,540,180,68,"automation"),("schedule","security","Ai đánh thức?","cron · timer",850,540,180,68,"operation")],
 [("p","parse","root","argv + syntax","emphasis"),("s","place","root","context","default"),("r","root","resource","syscall","emphasis"),("st","root","stream","file descriptors","default"),("re","root","repeat","dependency","default"),("sc","root","schedule","trigger","security")],
 views=[v("command","Command anatomy",["parse","root","place","resource","stream"],"Đọc một command bằng parser, context, resource và stream."),v("automation","Repeat safely",["root","repeat","schedule"],"Tách build/repeat khỏi scheduled trigger.")],
 card_data=(["Luôn hỏi ai parse, state ở đâu, kernel giữ gì","Automation tốt giữ exit status, log và idempotency"],["which/env/pwd/ps định vị context","strace + logs xác nhận đường chạy"]))

# ── Python ───────────────────────────────────────────────────────────────────
architecture("python-project-boundary-architecture","Project Python chạy đúng nhờ một ranh giới rõ","Declaration → resolve → lock → environment → explicit interpreter",
 [("repo","frontend","Project repo","source + tests",60,260,170,72,"versioned"),("pyproject","messagebus","pyproject.toml","dependency contract",280,150,180,72,"declare"),("lock","database","Lockfile","chosen versions",280,370,180,72,"reproduce"),("resolver","backend","Resolver","solve graph",540,260,170,72,"decision"),("venv","cloud","Virtual environment","interpreter + site-packages",780,260,190,72,"boundary"),("run","backend","Explicit python",".venv/bin/python",1030,150,160,72,"runtime"),("ci","external","CI / cron","same command",1030,370,160,72,"automation")],
 [("decl","repo","pyproject","declare deps","default"),("pin","repo","lock","commit choices","default"),("solve1","pyproject","resolver","constraints","emphasis"),("solve2","lock","resolver","exact set","emphasis"),("sync","resolver","venv","install graph","emphasis"),("local","venv","run","execute","emphasis"),("auto","venv","ci","explicit path","default")],
 views=[v("contract","Dependency contract",["repo","pyproject","lock","resolver"],"Declaration nói cần gì; lock ghi lựa chọn cụ thể."),v("runtime","Runtime boundary",["resolver","venv","run","ci"],"activate chỉ đổi PATH; interpreter path mới là bằng chứng.")],
 card_data=(["venv không phải container; nó cô lập interpreter và packages","Không commit .venv; commit declaration + lock phù hợp"],["python -c import sys; print(sys.executable)","pip/uv sync + test trên CI xác nhận reproducibility"]))

sequence("python-startup-sequence","File .py chưa chạy ngay khi nhấn Enter","Shell tạo process; interpreter mới compile và execute",
 [("user","external","Bạn","command"),("shell","backend","Shell","argv + env + cwd"),("os","cloud","OS","process image"),("python","backend","Python","interpreter startup"),("import","messagebus","Import system","module lookup"),("module","database","Module","namespace + __name__"),("main","backend","main()","application entry")],
 [("cmd","user","shell","python -m pipeline ...","emphasis"),("spawn","shell","os","exec interpreter","default"),("load","os","python","process + stdio","emphasis"),("compile","python","import","source → AST → bytecode","default"),("lookup","import","module","find + load pipeline","emphasis"),("namespace","module","main","create namespace","default"),("entry","main","user","run application","return")],
 views=[v("startup","Startup path",["user","shell","os","python"],"Process và interpreter tồn tại trước application code."),v("module","Module execution",["python","import","module","main"],"Import tạo namespace rồi mới đi vào entry point.")],
 card_data=(["Source → AST → bytecode tạo code object trước frame chạy","Side effect ở import xảy ra trước main"],["sys.executable + os.getcwd() kiểm tra context","python -X importtime cho evidence import"]))

architecture("python-name-binding-architecture","Tên không chứa object; namespace giữ đường trỏ","Assignment, alias, mutation và copy là bốn quan hệ khác nhau",
 [("ns","backend","Local namespace","records · backup",70,260,190,76,"name table"),("records","frontend","name: records","binding",330,150,170,68,"label"),("backup","frontend","name: backup","alias",330,370,170,68,"label"),("list","database","List object","mutable identity",590,260,190,76,"heap object"),("item1","messagebus","Item object A","record 1",860,130,170,64,"element"),("item2","messagebus","Item object B","record 2",860,260,170,64,"element"),("copy","database","Shallow copy","new outer list",860,420,170,68,"copy boundary")],
 [("nr","ns","records","lookup","default"),("nb","ns","backup","lookup","default"),("rlist","records","list","bind","emphasis"),("blist","backup","list","same identity","emphasis"),("e1","list","item1","contains ref","default"),("e2","list","item2","contains ref","default"),("cp","list","copy","copy outer shell","security")],
 views=[v("alias","Alias",["ns","records","backup","list"],"Hai name có thể trỏ cùng một mutable object."),v("copy","Shallow copy",["list","item1","item2","copy"],"Outer list mới nhưng phần tử vẫn có thể dùng chung.")],
 card_data=(["= bind name; append mutates object; is kiểm tra identity","Shallow copy không tự clone graph bên trong"],["id() chỉ dùng như evidence cục bộ","Test mutation ở nested item để phát hiện shared reference"]))

sequence("python-exception-unwinding-sequence","Exception đi ngược call stack cho tới handler","Traceback là bằng chứng của quá trình gỡ frame",
 [("main","external","main frame","caller"),("load","backend","load_orders","frame"),("parse","backend","parse_row","frame"),("codec","messagebus","json.loads","library frame"),("handler","security","except handler","recovery"),("log","database","Log / traceback","evidence")],
 [("a","main","load","load file","emphasis"),("b","load","parse","parse row 42","default"),("c","parse","codec","decode bytes","default"),("d","codec","parse","raise JSONDecodeError","security"),("e","parse","load","no handler → unwind","security"),("f","load","handler","matching except","emphasis"),("g","handler","log","record traceback + context","return")],
 views=[v("call","Call stack",["main","load","parse","codec"],"Mỗi call tạo frame với locals và instruction pointer."),v("unwind","Exception unwind",["codec","parse","load","handler","log"],"Frame không bắt lỗi bị gỡ theo chiều ngược.")],
 card_data=(["Exception không tự biến mất; nó tìm handler theo stack","with/finally giữ cleanup ngay cả khi unwind"],["Traceback cho file, line và call chain","Log input identity nhưng tránh lộ secret"]))

dataflow("python-serialization-dataflow","Object chỉ đi qua boundary sau khi thành byte","Encode, transport, parse và validate là bốn trách nhiệm",
 ["Live object","Encode","Transport","Parse","Validated value"],
 [("object","database","Python object","dict / datetime",0,0,"RAM identity"),("encode","backend","Encoder","JSON / CSV / Arrow",1,0,"schema choice"),("bytes","messagebus","Byte buffer","UTF-8 / binary",2,0,"portable payload"),("parse","backend","Parser","bytes → fields",3,0,"syntax"),("valid","database","Validated model","types + invariant",4,0,"trusted state")],
 [("a","object","encode","serialize","representation","emphasis"),("b","encode","bytes","emit bytes","wire format","emphasis"),("c","bytes","parse","read payload","I/O boundary","emphasis"),("d","parse","valid","validate","schema + invariant","emphasis")],
 views=[v("outbound","Outbound",["object","encode","bytes"],"Identity trong RAM không đi qua file/socket."),v("inbound","Inbound",["bytes","parse","valid"],"Parse đúng syntax chưa đồng nghĩa dữ liệu hợp lệ.")],
 card_data=(["Serialization chọn representation; schema giữ meaning","pickle tiện nhưng không phải boundary tin cậy cho input lạ"],["Round-trip test kiểm tra encode/decode","Schema validation + checksum kiểm tra payload"]))

workflow("python-sync-async-workflow","Sync và async khác ở cách dùng thời gian chờ","Cùng I/O, nhưng ownership của thread khác nhau",
 [("sync","Synchronous path"),("async","Async event loop"),("evidence","Measurement")],
 [("srun","sync",0,"backend","Run task A","owns thread","running"),("swait","sync",1,"security","Blocking I/O","thread waits","idle"),("snext","sync",2,"backend","Run task B","starts later","serialized"),("arun","async",0,"backend","Run task A","until await","running"),("await","async",1,"messagebus","await I/O","register + yield","cooperative"),("other","async",2,"backend","Run task B","same thread","interleaved"),("resume","async",3,"backend","Resume A","I/O ready","continuation"),("metric","evidence",4,"database","Timeline evidence","latency + throughput","measure")],
 [("s1","srun","swait","call I/O","default"),("s2","swait","snext","returns","default"),("a1","arun","await","yield","emphasis"),("a2","await","other","loop schedules","emphasis"),("a3","other","resume","readiness event","emphasis"),("m1","snext","metric","compare","default"),("m2","resume","metric","compare","default")],
 main_path=["arun","await","other","resume","metric"],
 views=[v("sync","Blocking path",["srun","swait","snext","metric"],"Thread không làm task khác trong khoảng blocking call."),v("async","Async path",["arun","await","other","resume","metric"],"Task yield ở await để loop chạy việc khác.")],
 card_data=(["Async tối ưu wait-heavy concurrency, không biến CPU work thành parallel","Blocking library trong async handler có thể chặn cả loop"],["Timeline + p95 latency tốt hơn cảm giác","Profile CPU riêng với event-loop lag"]))

workflow("python-gil-decision-workflow","Chọn thread, async hay process từ bottleneck","Đầu tiên hỏi đang tính hay đang chờ",
 [("question","Workload question"),("choice","Execution choice"),("proof","Evidence")],
 [("work","question",0,"external","Đoạn này làm gì?","CPU work hay I/O wait","start"),("wait","question",1,"messagebus","Phần lớn chờ","socket · disk · DB","I/O-bound"),("cpu","question",1,"cloud","Phần lớn tính","Python bytecode","CPU-bound"),("async","choice",2,"backend","asyncio","many waits · one loop","cooperative"),("threads","choice",2,"backend","Threads","blocking libraries","shared memory"),("process","choice",2,"backend","Processes","parallel CPU","separate memory"),("measure","proof",3,"database","Benchmark + profile","throughput · CPU · latency","evidence")],
 [("a","work","wait","I/O-bound","default"),("b","work","cpu","CPU-bound","default"),("c","wait","async","async-compatible","emphasis"),("d","wait","threads","blocking API","emphasis"),("e","cpu","process","parallelism","emphasis"),("f","async","measure","verify","default"),("g","threads","measure","verify","default"),("h","process","measure","verify","default")],
 main_path=["work","wait","async","measure"],
 views=[v("io","I/O choices",["work","wait","async","threads","measure"],"Async và thread đều có thể che thời gian chờ theo cách khác nhau."),v("cpu","CPU choice",["work","cpu","process","measure"],"Process tách interpreter state để dùng nhiều core cho Python CPU work.")],
 card_data=(["GIL là property của build/runtime CPython, không phải định nghĩa của Python","Free-threaded build vẫn cần ecosystem compatibility"],["py-spy/cProfile xác nhận CPU hotspot","Load test xác nhận throughput và tail latency"]))

architecture("python-synthesis-architecture","Python: theo một lần chạy bằng ba câu hỏi","Ai giữ quyền chạy, dữ liệu ở đâu, evidence nào đủ",
 [("root","backend","Một lần chạy Python","python -m pipeline",500,270,220,80,"root"),("project","frontend","Project boundary","env + dependencies",70,90,185,70,"before run"),("runtime","cloud","Runtime","process + interpreter",70,430,185,70,"execution"),("objects","database","Objects","namespace + identity",930,90,185,70,"memory"),("errors","security","Errors","frame + traceback",930,430,185,70,"control flow"),("boundary","messagebus","Byte boundary","file · socket · DB",170,550,185,70,"I/O"),("time","backend","Time model","sync · async · process",850,550,185,70,"scheduling")],
 [("a","project","root","select interpreter","emphasis"),("b","runtime","root","execute bytecode","default"),("c","root","objects","bind names","default"),("d","root","errors","unwind","security"),("e","root","boundary","serialize","emphasis"),("f","root","time","schedule","default")],
 views=[v("run","One run",["project","runtime","root","objects","errors"],"Định vị project, process, object và failure."),v("system","External work",["root","boundary","time"],"I/O boundary và time model quyết định concurrency.")],
 card_data=(["Không bắt đầu từ syntax; bắt đầu từ boundary và execution","Mọi tối ưu phải gắn với CPU, memory hoặc wait evidence"],["sys.executable/cwd xác nhận runtime","traceback/profile/metrics xác nhận behavior"]))

# ── Database / PostgreSQL ────────────────────────────────────────────────────
architecture("database-responsibility-architecture","Database giữ shared truth cho nhiều actor","State, invariant, concurrency và recovery là bốn trách nhiệm",
 [("clients","external","Nhiều client","app · analyst · job",60,260,180,72,"concurrent intent"),("protocol","messagebus","Protocol / driver","request + transaction",300,260,180,72,"boundary"),("database","backend","Database engine","serialize shared truth",550,260,190,76,"authority"),("state","database","Durable state","relations + pages",840,90,180,68,"where"),("rules","security","Invariant","keys + constraints",840,210,180,68,"validity"),("concurrency","cloud","Concurrency control","visibility + locks",840,330,180,68,"coordination"),("recovery","cloud","Recovery","log + backup",840,450,180,68,"survival")],
 [("intent","clients","protocol","query + params","default"),("request","protocol","database","transactional request","emphasis"),("persist","database","state","store facts","emphasis"),("validate","database","rules","enforce","security"),("coordinate","database","concurrency","isolate actors","default"),("survive","database","recovery","restore truth","default")],
 views=[v("contract","Database contract",["clients","protocol","database","state","rules"],"Database không chỉ chứa file; nó giữ shared truth và invariant."),v("multiuser","Many actors",["clients","database","concurrency","recovery"],"Concurrency và recovery làm state dùng được trong thực tế.")],
 card_data=(["Table là representation; trách nhiệm cốt lõi là shared truth","Constraint gần dữ liệu bảo vệ mọi writer"],["Transaction tests kiểm tra invariant","Restore drill chứng minh durability"]))

architecture("database-relational-model-architecture","Relational model nối fact, key và invariant","Từ business statement tới relation có nghĩa",
 [("fact","external","Business fact","order belongs to customer",60,260,190,72,"meaning"),("customer","database","Customer relation","customer_id PK",340,120,190,72,"entity"),("order","database","Order relation","order_id PK",340,330,190,72,"entity"),("fk","security","Foreign key","orders.customer_id",640,260,190,72,"invariant"),("join","backend","Relational join","PK ↔ FK",920,150,180,68,"query"),("access","cloud","Access pattern","lookup · range · aggregate",920,370,180,68,"workload")],
 [("model1","fact","customer","identify actor","default"),("model2","fact","order","identify event","default"),("ref1","customer","fk","referenced key","security"),("ref2","order","fk","referencing key","security"),("query","fk","join","combine facts","emphasis"),("use","join","access","serve question","default")],
 views=[v("model","Facts to relations",["fact","customer","order","fk"],"Key và constraint giữ identity và relationship."),v("query","Use the model",["customer","order","fk","join","access"],"Access pattern đến sau semantic model, nhưng ảnh hưởng physical design.")],
 card_data=(["Primary key định danh fact; foreign key giữ relationship","Normalization giảm anomaly, không phải chia bảng vô hạn"],["Constraint violation test kiểm tra invariant","EXPLAIN kiểm tra physical access path"]))

workflow("database-normalization-workflow","Normalization sửa anomaly bằng cách tách fact","Một nguồn sự thật cho mỗi loại fact",
 [("wide","Wide table"),("anomaly","Observed anomaly"),("normalized","Separated facts")],
 [("table","wide",0,"database","orders_wide","customer + order repeated","mixed facts"),("update","anomaly",1,"security","Update anomaly","one customer · many rows","inconsistent"),("insert","anomaly",1,"security","Insert anomaly","need order to store customer","coupled"),("delete","anomaly",1,"security","Delete anomaly","last order deletes customer","data loss"),("customer","normalized",2,"database","customers","one row per customer","fact A"),("orders","normalized",2,"database","orders","one row per order","fact B"),("fk","normalized",3,"security","Foreign key","explicit relationship","invariant")],
 [("a","table","update","repeated value","security"),("b","table","insert","coupled fact","security"),("c","table","delete","accidental loss","security"),("d","update","customer","separate customer","emphasis"),("e","insert","orders","separate order","emphasis"),("f","customer","fk","referenced","default"),("g","orders","fk","references","default")],
 main_path=["table","update","customer","fk"],
 views=[v("anomalies","Three anomalies",["table","update","insert","delete"],"Mixed facts create update, insert and delete anomalies."),v("split","Normalized design",["customer","orders","fk"],"Relations tách fact nhưng vẫn nối bằng constraint.")],
 card_data=(["Tách theo functional dependency, không theo cảm giác","Denormalize chỉ khi workload + evidence biện minh"],["Test duplicate/update/delete cases","Constraint + migration test bảo vệ model"]))

workflow("postgresql-planner-workflow","Planner chọn access path bằng estimate và cost","Index chỉ là một ứng viên, không phải mệnh lệnh",
 [("input","Query inputs"),("estimate","Planner reasoning"),("choice","Candidate plans"),("proof","Runtime evidence")],
 [("sql","input",0,"external","SQL + predicate","WHERE status = ...","intent"),("stats","input",0,"database","Statistics","histogram · ndistinct","evidence"),("selectivity","estimate",1,"backend","Selectivity","estimated rows","assumption"),("cost","estimate",2,"backend","Cost model","I/O + CPU","compare"),("seq","choice",3,"database","Seq Scan","read many pages","candidate"),("index","choice",3,"database","Index Scan","random lookup","candidate"),("bitmap","choice",3,"database","Bitmap Scan","batch heap pages","candidate"),("actual","proof",4,"security","EXPLAIN ANALYZE","estimate vs actual","measurement")],
 [("a","sql","selectivity","predicate","default"),("b","stats","selectivity","distribution","emphasis"),("c","selectivity","cost","row estimate","emphasis"),("d","cost","seq","candidate cost","default"),("e","cost","index","candidate cost","default"),("f","cost","bitmap","candidate cost","default"),("g","seq","actual","chosen plan","emphasis"),("h","index","actual","chosen plan","emphasis"),("i","bitmap","actual","chosen plan","emphasis")],
 main_path=["sql","selectivity","cost","index","actual"],
 views=[v("estimate","Estimate path",["sql","stats","selectivity","cost"],"Planner dự đoán cardinality trước khi chạy."),v("choice","Plan choice",["cost","seq","index","bitmap","actual"],"Actual evidence cho biết estimate nào sai.")],
 card_data=(["Có index không đồng nghĩa planner phải dùng index","Sai cardinality thường kéo theo sai join/access path"],["EXPLAIN (ANALYZE, BUFFERS) so estimate và actual","ANALYZE cập nhật statistics trước khi kết luận"]))

sequence("postgresql-mvcc-sequence","MVCC quyết định ai nhìn thấy version nào","Visibility và lock conflict là hai cơ chế khác nhau",
 [("tx1","external","Transaction A","writer"),("backend1","backend","Backend A","snapshot + xid"),("heap","database","Heap page","tuple versions"),("backend2","backend","Backend B","reader snapshot"),("tx2","external","Transaction B","reader"),("lock","security","Lock manager","write conflict"),("wal","messagebus","WAL","durability")],
 [("begin1","tx1","backend1","BEGIN · snapshot S1","default"),("update","backend1","heap","create new tuple version","emphasis"),("record","backend1","wal","append WAL record","emphasis"),("begin2","tx2","backend2","SELECT · snapshot S2","default"),("read","backend2","heap","test xmin/xmax visibility","emphasis"),("visible","heap","backend2","return visible version","return"),("conflict","backend1","lock","second writer waits","security"),("commit","backend1","tx1","COMMIT after WAL flush","return")],
 views=[v("visibility","Reader visibility",["tx2","backend2","heap"],"Snapshot chọn version phù hợp mà không khóa mọi reader."),v("write","Writer coordination",["tx1","backend1","heap","lock","wal"],"Lock xử lý conflict; WAL xử lý durability.")],
 card_data=(["MVCC tạo version; snapshot quyết định visibility","Lock conflict không đồng nghĩa mọi read đều bị chặn"],["pg_locks + pg_stat_activity cho wait evidence","xmin/xmax lab giải thích version lifecycle"]))

architecture("postgresql-storage-architecture","Một row vật lý sống trong page và nhiều bản đồ","Heap, buffer, VM/FSM và WAL phục vụ mục tiêu khác nhau",
 [("executor","backend","Executor","tuple operation",60,260,170,72,"logical action"),("buffer","cloud","Shared buffers","cached 8 KB pages",300,260,180,72,"memory"),("heap","database","Heap page","line pointer + tuple",560,120,180,72,"data"),("index","database","Index page","key → TID",560,330,180,72,"access path"),("vm","messagebus","Visibility map","all-visible hints",840,80,180,68,"maintenance"),("fsm","messagebus","Free space map","space hints",840,230,180,68,"placement"),("wal","security","WAL files","redo evidence",300,480,180,68,"durability"),("disk","database","Persistent files","heap + index forks",1060,260,140,72,"storage")],
 [("page","executor","buffer","pin + modify","emphasis"),("h","buffer","heap","heap page","default"),("i","buffer","index","index page","default"),("v","heap","vm","visibility state","default"),("f","heap","fsm","free space","default"),("w","buffer","wal","write-ahead","security"),("persist1","heap","disk","data file","default"),("persist2","index","disk","index file","default")],
 views=[v("row","Tuple location",["executor","buffer","heap","index","disk"],"Logical row được chứa trong heap page; index trỏ TID."),v("maintenance","Maintenance metadata",["heap","vm","fsm","wal"],"VM/FSM hỗ trợ vacuum và placement; WAL bảo vệ redo.")],
 card_data=(["Shared buffers cache page, không phải toàn bộ database","WAL là redo log; heap/index vẫn là data files"],["pageinspect cho page anatomy","BUFFERS + pg_relation_size đo I/O và footprint"]))

lifecycle("postgresql-vacuum-lifecycle","VACUUM làm sạch version khi không snapshot nào còn cần","Dead tuple → reclaim space → freeze → statistics",
 [("main","Tuple lifecycle"),("maintenance","Background maintenance")],
 [("live","start","Live tuple","visible version","main",0,1,"current"),("superseded","active","Superseded","UPDATE creates successor","main",1,2,"old version"),("dead","waiting","Dead to all","global xmin passed","main",2,3,"reclaimable"),("scan","active","VACUUM scan","find dead tuples","maintenance",2,4,"worker"),("reclaim","success","Space reusable","FSM updated","maintenance",3,5,"reuse"),("freeze","active","Freeze old xmin","avoid wraparound","maintenance",3,6,"safety"),("stats","success","Stats refreshed","planner evidence","maintenance",4,7,"observe")],
 [("a","live","superseded","UPDATE / DELETE","default"),("b","superseded","dead","old snapshots finish","emphasis"),("c","dead","scan","eligible","emphasis"),("d","scan","reclaim","remove dead line items","emphasis"),("e","reclaim","freeze","maintenance pass","default"),("f","freeze","stats","report","default")],
 views=[v("tuple","Tuple death",["live","superseded","dead"],"Version chỉ dead khi không transaction nào còn nhìn thấy."),v("vacuum","Vacuum work",["dead","scan","reclaim","freeze","stats"],"VACUUM reclaim, freeze và cung cấp evidence cho planner.")],
 card_data=(["VACUUM không shrink file mặc định; nó làm space reusable","Long transaction giữ xmin và cản cleanup"],["n_dead_tup + autovacuum logs theo dõi bloat","age(datfrozenxid) theo dõi wraparound risk"]))

workflow("postgresql-index-family-workflow","Chọn index từ operator và data shape","Không có một index tốt cho mọi predicate",
 [("question","Access question"),("family","Index family"),("tradeoff","Operational cost")],
 [("predicate","question",0,"external","Predicate là gì?","equality · range · contains","operator"),("shape","question",0,"database","Data shape","ordered · array · spatial · huge","distribution"),("btree","family",1,"database","B-tree","equality + range + order","default"),("gin","family",1,"database","GIN","array · JSONB · text","inverted"),("gist","family",1,"database","GiST","spatial · similarity","framework"),("brin","family",1,"database","BRIN","huge correlated table","summary"),("cost","tradeoff",2,"security","Write + storage cost","maintenance overhead","tradeoff"),("plan","tradeoff",3,"backend","Planner choice","costed candidate","decision"),("evidence","tradeoff",4,"external","EXPLAIN evidence","actual workload","proof")],
 [("a","predicate","btree","equality/range","emphasis"),("b","predicate","gin","contains","emphasis"),("c","predicate","gist","distance","emphasis"),("d","shape","brin","correlated blocks","emphasis"),("e","btree","cost","maintain","default"),("f","gin","cost","maintain","default"),("g","gist","cost","maintain","default"),("h","brin","cost","maintain","default"),("i","cost","plan","candidate","default"),("j","plan","evidence","measure","emphasis")],
 main_path=["predicate","btree","cost","plan","evidence"],
 views=[v("operators","Operator fit",["predicate","shape","btree","gin","gist","brin"],"Index family phải hỗ trợ operator class cần dùng."),v("tradeoff","Cost and proof",["btree","gin","gist","brin","cost","plan","evidence"],"Đọc nhanh hơn đổi lấy write/storage/maintenance cost.")],
 card_data=(["Composite index còn phụ thuộc column order và predicate shape","Partial/covering index là workload decision"],["EXPLAIN ANALYZE + BUFFERS xác nhận benefit","Theo dõi write amplification và index size"]))

architecture("postgresql-production-architecture","PostgreSQL production là topology của state và evidence","Primary, standby, backup và observability có vai trò khác nhau",
 [("app","frontend","Application","requests + pool",50,260,170,72,"client"),("pool","messagebus","Connection pooler","session boundary",270,260,180,72,"capacity"),("primary","backend","Primary","commit + WAL",520,260,180,76,"authority"),("standby","backend","Standby","replay + reads",800,100,180,72,"availability"),("archive","database","WAL archive","continuous log",800,250,180,72,"recovery"),("backup","database","Base backup","restore seed",800,400,180,72,"recovery"),("observe","cloud","Observability","metrics · logs · traces",1040,260,150,72,"evidence"),("restore","security","Restore environment","PITR drill",1040,400,150,72,"proof")],
 [("conn","app","pool","connections","default"),("query","pool","primary","transactions","emphasis"),("rep","primary","standby","stream WAL","default"),("arch","primary","archive","archive WAL","emphasis"),("base","primary","backup","base backup","default"),("metrics","primary","observe","waits + rates","default"),("drill1","archive","restore","replay","security"),("drill2","backup","restore","restore base","security")],
 views=[v("availability","Serve and replicate",["app","pool","primary","standby","observe"],"Standby hỗ trợ availability/read scale nhưng có replication lag."),v("recovery","Backup and PITR",["primary","archive","backup","restore"],"Backup chỉ đáng tin khi restore drill thành công.")],
 card_data=(["Replica không thay backup; backup không tự chứng minh restore","Pooler bảo vệ connection capacity, không sửa query chậm"],["Lag/waits/throughput là evidence vận hành","RTO/RPO chỉ có nghĩa sau restore drill"]))

workflow("postgresql-evidence-workflow","Tuning bắt đầu bằng câu hỏi và kết thúc bằng đo lại","Không thay đổi production dựa trên dashboard trang trí",
 [("question","Question"),("collect","Collect evidence"),("diagnose","Mechanism"),("change","Controlled change"),("verify","Verify")],
 [("symptom","question",0,"external","Symptom cụ thể","slow query · lag · bloat","scope"),("plan","collect",1,"backend","Query plan","rows · loops · time","EXPLAIN"),("buffers","collect",1,"database","Buffers / I/O","hit · read · dirtied","storage"),("waits","collect",1,"messagebus","Wait events","CPU · lock · I/O","blocking"),("hypothesis","diagnose",2,"security","Mechanism hypothesis","estimate · lock · cache","causal"),("change","change",3,"backend","One change","index · query · config","controlled"),("compare","verify",4,"database","Before / after","same workload","evidence"),("rollback","verify",4,"security","Rollback","regression guard","safety")],
 [("a","symptom","plan","query evidence","default"),("b","symptom","buffers","I/O evidence","default"),("c","symptom","waits","wait evidence","default"),("d","plan","hypothesis","interpret","emphasis"),("e","buffers","hypothesis","interpret","emphasis"),("f","waits","hypothesis","interpret","emphasis"),("g","hypothesis","change","test one cause","emphasis"),("h","change","compare","measure","emphasis"),("i","compare","rollback","regressed","security","error")],
 main_path=["symptom","plan","hypothesis","change","compare"],
 views=[v("evidence","Evidence bundle",["symptom","plan","buffers","waits","hypothesis"],"Mỗi evidence trả lời một lớp khác nhau."),v("experiment","Controlled experiment",["hypothesis","change","compare","rollback"],"Một thay đổi, cùng workload, có rollback.")],
 card_data=(["Chart không có question/failure model chỉ là decoration","Estimate vs actual thường là đầu mối quan trọng"],["Lưu query, parameters và workload window","So p50/p95, buffers, waits và correctness sau change"]))

architecture("postgresql-synthesis-architecture","PostgreSQL: năm câu hỏi chẩn đoán","Where, visibility, path, durability và evidence nối thành một mental model",
 [("root","backend","Một database request","shared truth",500,270,220,80,"root"),("where","database","Dữ liệu ở đâu?","relation → page → disk",60,90,190,72,"storage"),("who","security","Ai nhìn thấy?","snapshot → MVCC → lock",60,430,190,72,"concurrency"),("path","backend","Đường nào được chọn?","stats → cost → plan",930,90,190,72,"execution"),("durable","cloud","Commit sống qua crash?","WAL → checkpoint → replay",930,430,190,72,"recovery"),("evidence","messagebus","Bằng chứng nào?","plan · waits · restore",170,550,190,72,"proof"),("operation","frontend","Ai vận hành?","pool · vacuum · backup",850,550,190,72,"ownership")],
 [("a","where","root","pages","default"),("b","who","root","visibility","security"),("c","root","path","planner","emphasis"),("d","root","durable","write-ahead","emphasis"),("e","root","evidence","measure","default"),("f","root","operation","operate","default")],
 views=[v("request","Request reasoning",["where","who","root","path"],"Theo query từ logical intent tới visible tuple và chosen plan."),v("production","Production proof",["root","durable","evidence","operation"],"Durability và operation phải được chứng minh bằng evidence.")],
 card_data=(["Logical model, physical pages và operational topology là ba lớp khác nhau","Mọi câu trả lời tốt đều chỉ ra mechanism + evidence"],["EXPLAIN/locks/pages cho runtime evidence","Backup restore drill cho recovery evidence"]))

GENERATED = {
    "linux-command-execution-sequence.json",
    "linux-path-permission-workflow.json",
    "linux-syscall-layer-architecture.json",
    "linux-script-contract-workflow.json",
    "linux-compilation-dataflow.json",
    "linux-make-dependency-workflow.json",
    "linux-synthesis-architecture.json",
    "python-project-boundary-architecture.json",
    "python-startup-sequence.json",
    "python-name-binding-architecture.json",
    "python-exception-unwinding-sequence.json",
    "python-serialization-dataflow.json",
    "python-sync-async-workflow.json",
    "python-gil-decision-workflow.json",
    "python-synthesis-architecture.json",
    "database-responsibility-architecture.json",
    "database-relational-model-architecture.json",
    "database-normalization-workflow.json",
    "postgresql-planner-workflow.json",
    "postgresql-mvcc-sequence.json",
    "postgresql-storage-architecture.json",
    "postgresql-vacuum-lifecycle.json",
    "postgresql-index-family-workflow.json",
    "postgresql-production-architecture.json",
    "postgresql-evidence-workflow.json",
    "postgresql-synthesis-architecture.json",
}

# Targeted geometry simplification for showcase composition.
# Keep the semantic nodes, but remove redundant branch edges that would merge
# into ambiguous corridors in the compact embedded viewer.
EDGE_REMOVALS = {
    "database-normalization-workflow.json": {"b", "c"},
    "python-gil-decision-workflow.json": {"d", "f"},
    "postgresql-planner-workflow.json": {"d", "f", "g", "i"},
    "postgresql-evidence-workflow.json": {"b", "c", "e", "f"},
    "postgresql-index-family-workflow.json": {"b", "c", "e", "f", "g"},
}
for filename, edge_ids in EDGE_REMOVALS.items():
    path = OUT / filename
    spec = json.loads(path.read_text())
    spec["edges"] = [edge for edge in spec["edges"] if edge.get("id") not in edge_ids]
    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")

# Vacuum is clearest as one five-state lifecycle; freeze/statistics remain in cards.
path = OUT / "postgresql-vacuum-lifecycle.json"
spec = json.loads(path.read_text())
spec["lanes"] = [{"id": "main", "label": "Tuple → reusable space"}]
spec["states"] = [
    {"id":"live","type":"start","label":"Live tuple","sublabel":"visible version","lane":"main","col":0,"step":"01","tag":"current"},
    {"id":"superseded","type":"active","label":"Superseded","sublabel":"UPDATE creates successor","lane":"main","col":1,"step":"02","tag":"old version"},
    {"id":"dead","type":"waiting","label":"Dead to all","sublabel":"global xmin passed","lane":"main","col":2,"step":"03","tag":"reclaimable"},
    {"id":"scan","type":"active","label":"VACUUM scan","sublabel":"reclaim + freeze","lane":"main","col":3,"step":"04","tag":"maintenance","brand":"postgresql"},
    {"id":"reclaim","type":"success","label":"Space reusable","sublabel":"FSM + stats updated","lane":"main","col":4,"step":"05","tag":"evidence"},
]
spec["transitions"] = [
    {"id":"a","from":"live","to":"superseded","variant":"default"},
    {"id":"b","from":"superseded","to":"dead","variant":"emphasis"},
    {"id":"c","from":"dead","to":"scan","variant":"emphasis"},
    {"id":"d","from":"scan","to":"reclaim","variant":"emphasis"},
]
path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")

# Final semantic simplification: these overview maps carry relationship meaning
# in node titles, sublabels, guided views and cards. Repeating the same words on
# converging star edges creates visual noise, so those redundant labels are omitted.
LABELLESS_ARCHITECTURES = {
    "database-relational-model-architecture.json",
    "database-responsibility-architecture.json",
    "linux-synthesis-architecture.json",
    "linux-syscall-layer-architecture.json",
    "postgresql-production-architecture.json",
    "postgresql-storage-architecture.json",
    "postgresql-synthesis-architecture.json",
    "python-name-binding-architecture.json",
    "python-project-boundary-architecture.json",
    "python-synthesis-architecture.json",
}
for filename in LABELLESS_ARCHITECTURES:
    path = OUT / filename
    spec = json.loads(path.read_text())
    for edge in spec.get("connections", []):
        edge.pop("label", None)
        edge.pop("labelDy", None)
    if filename == "postgresql-production-architecture.json":
        spec["connections"] = [edge for edge in spec["connections"] if edge.get("id") != "metrics"]
    if filename == "postgresql-storage-architecture.json":
        spec["connections"] = [edge for edge in spec["connections"] if edge.get("id") not in {"persist1", "persist2"}]
    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")

# Removed optional branch edges must not remain in mainPath contracts.
for filename in ["python-gil-decision-workflow.json", "postgresql-index-family-workflow.json"]:
    path = OUT / filename
    spec = json.loads(path.read_text())
    spec.pop("mainPath", None)
    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")

# Guided view follows the simplified five-state vacuum lifecycle.
path = OUT / "postgresql-vacuum-lifecycle.json"
spec = json.loads(path.read_text())
spec["meta"]["views"][1]["focus"] = ["dead", "scan", "reclaim"]
path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")

# Apply vetted Archify marks. Python/PostgreSQL/FastAPI come from the bundled
# canonical catalogue. Linux/Tux is captured from the official kernel.org site,
# digest-pinned by Archify, and mirrored under archify/brand-assets for audit.
LINUX_BRAND = {
    "url": "https://www.kernel.org/",
    "sha256": "9bfb70bf96004ac694b4ed902e634d029df9cc3b0ca50ce06d0608d29afa6d37",
}
BRAND_ASSIGNMENTS = {
    "linux-command-architecture.json": {"kernel": LINUX_BRAND},
    "linux-command-execution-sequence.json": {"kernel": LINUX_BRAND},
    "linux-path-permission-workflow.json": {"check": LINUX_BRAND},
    "linux-synthesis-architecture.json": {"root": LINUX_BRAND},
    "linux-syscall-layer-architecture.json": {"kernel": LINUX_BRAND},
    "python-project-boundary-architecture.json": {"repo": "python", "venv": "python", "run": "python"},
    "python-startup-sequence.json": {"python": "python", "main": "python"},
    "python-name-binding-architecture.json": {"ns": "python"},
    "python-exception-unwinding-sequence.json": {"main": "python"},
    "python-serialization-dataflow.json": {"object": "python"},
    "python-sync-async-workflow.json": {"arun": "python", "async": "python"},
    "python-gil-decision-workflow.json": {"async": "python", "threads": "python", "process": "python"},
    "python-synthesis-architecture.json": {"root": "python", "runtime": "python"},
    "python-runtime-architecture.json": {"process": "python", "interpreter": "python"},
    "python-request-sequence.json": {"fastapi": "fastapi", "handler": "python"},
    "database-responsibility-architecture.json": {"database": "postgresql"},
    "database-relational-model-architecture.json": {"customer": "postgresql", "order": "postgresql"},
    "database-normalization-workflow.json": {"table": "postgresql", "customer": "postgresql", "orders": "postgresql"},
    "postgresql-planner-workflow.json": {"sql": "postgresql", "actual": "postgresql"},
    "postgresql-mvcc-sequence.json": {"backend1": "postgresql", "backend2": "postgresql"},
    "postgresql-storage-architecture.json": {"executor": "postgresql", "buffer": "postgresql"},
    "postgresql-vacuum-lifecycle.json": {"scan": "postgresql"},
    "postgresql-index-family-workflow.json": {"plan": "postgresql"},
    "postgresql-production-architecture.json": {"primary": "postgresql", "standby": "postgresql"},
    "postgresql-evidence-workflow.json": {"plan": "postgresql"},
    "postgresql-synthesis-architecture.json": {"root": "postgresql"},
    "postgresql-architecture.json": {"backend": "postgresql", "planner": "postgresql"},
    "postgresql-query-sequence.json": {"backend": "postgresql", "planner": "postgresql", "executor": "postgresql"},
    "postgresql-mvcc-durability-lifecycle.json": {"write": "postgresql", "commit": "postgresql"},
}
for filename, assignments in BRAND_ASSIGNMENTS.items():
    path = OUT / filename
    if not path.exists():
        continue
    spec = json.loads(path.read_text())
    collection = spec.get("components") or spec.get("participants") or spec.get("nodes") or spec.get("states") or []
    for item in collection:
        if item.get("id") in assignments:
            item["brand"] = assignments[item["id"]]
        if filename == "python-request-sequence.json" and item.get("id") == "handler":
            item["label"] = "Handler"
    path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")

print("Generated additional specs:")
for p in sorted(OUT.glob("*.json")):
    if p.name in GENERATED:
        print(" -", p.name)
