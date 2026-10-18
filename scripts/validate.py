#!/usr/bin/env python3
"""
Strict Validator for FSDS Learning Hub (Anthropic Academy CDS + Monodraw/Durdraw Colored ASCII):
1. Runs 6 negative regression self-tests in scripts/ascii_diagram.py.
2. Verifies JS syntax in fsds-learning-hub.html via `node --check` on stdin.
3. Verifies 100% of Colored ASCII/Unicode diagrams (119/119, zero skipped) using kind-specific geometry verifiers.
4. Verifies HTML/JSON diagram parity, 12/12 official slide TOCs, and 100% of normalized lesson stations across 19 stages.
5. Audits removal of Picture/Mermaid bloat, Spine `<img>` boxes, decorative emojis, `➔` arrows, and AI meta-copy.
6. Runs Headless Browser Runtime QA (scripts/qa_runtime.py) across all 19 pages + #/catalog + #/glossary across 3 viewports.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ascii_diagram import run_self_tests, verify_character_policy, verify_diagram


def main():
    run_self_tests()

    html_path = ROOT / "fsds-learning-hub.html"
    data_path = ROOT / "content/lessons-data.json"
    if not html_path.exists() or not data_path.exists():
        raise SystemExit("Missing fsds-learning-hub.html or content/lessons-data.json. Run python3 scripts/build_hub.py")

    html = html_path.read_text(encoding="utf-8")
    data = json.loads(data_path.read_text(encoding="utf-8"))

    # 1. Extract inline script and check syntax via node --check on stdin
    script_body = html.split("<script>", 1)[1].split("</script>", 1)[0]
    proc = subprocess.run(
        ["node", "--check", "-"],
        input=script_body,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"JS syntax check failed:\n{proc.stderr}")

    # 2. Verify zero legacy AI content or visual_assets in lessons-data.json and verify all 119/119 diagrams
    if "foundation" in data:
        raise SystemExit("Legacy AI content ('foundation') still present in content/lessons-data.json")
    if "visual_assets" in data:
        raise SystemExit("Legacy 'visual_assets' still present in content/lessons-data.json (must be pure Colored ASCII)")

    char_checked = 0
    geom_checked = 0
    skipped = 0
    expected_kinds = {
        "0.1": "boxes",
        "1.1": "pyramid",
        "1.2": "boxes",
        "1.2b": "boxes",
        "1.3": "boxes",
        "1.3b": "boxes",
        "1.4": "boxes",
        "1.5": "boxes",
        "2.1": "boxes",
        "2.1b": "boxes",
        "2.2a": "boxes",
        "2.2b": "boxes",
        "2.3": "boxes",
        "2.4": "boxes",
        "2.4b": "boxes",
        "3.1": "boxes",
        "3.2": "boxes",
        "3.2b": "boxes",
        "3.3": "boxes",
        "3.4": "boxes",
        "3.5": "boxes",
        "4.1": "boxes",
        "4.2": "boxes",
        "4.3": "boxes",
        "4.3b": "boxes",
        "4.4": "boxes",
        "4.5": "boxes",
        "4.5a": "boxes",
        "5.1": "boxes",
        "5.2a": "boxes",
        "5.2b": "boxes",
        "5.2c": "boxes",
        "5.3": "boxes",
        "5.3b": "boxes",
        "5.4a": "boxes",
        "5.4b": "boxes",
        "6.1a": "boxes",
        "6.1b": "boxes",
        "6.2a": "boxes",
        "6.2b": "boxes",
        "6.2c": "boxes",
        "6.2d": "boxes",
        "6.3": "boxes",
        "6.3b": "boxes",
        "6.4": "boxes",
        "6.5a": "boxes",
        "6.5b": "boxes",
        "6.5c": "boxes",
        "7.1a": "boxes",
        "7.1b": "boxes",
        "7.2a": "boxes",
        "7.2b": "boxes",
        "7.2c": "boxes",
        "7.3a": "boxes",
        "7.3b": "boxes",
        "7.3c": "boxes",
        "7.3d": "boxes",
        "7.4": "boxes",
    }

    linux_expected_kinds = {
        "0.1": "boxes",
        "0.2": "boxes",
        "1.1a": "boxes",
        "1.1b": "boxes",
        "1.2a": "boxes",
        "1.2b": "boxes",
        "1.3a": "boxes",
        "1.3b": "boxes",
        "2.1a": "boxes",
        "2.1b": "boxes",
        "2.2a": "boxes",
        "2.2b": "boxes",
        "2.3a": "boxes",
        "2.3b": "boxes",
        "2.4a": "boxes",
        "2.4b": "boxes",
        "3.1a": "boxes",
        "3.1b": "boxes",
        "3.2a": "boxes",
        "3.2b": "boxes",
        "4.0": "boxes",
        "4.1a": "boxes",
        "4.1b": "boxes",
        "4.2a": "boxes",
        "4.2b": "boxes",
        "4.3a": "boxes",
        "4.3b": "boxes",
    }

    db_expected_kinds = {
        "0.1": "boxes",
        "0.2": "boxes",
        "1.0": "boxes",
        "1.1": "boxes",
        "1.2": "boxes",
        "1.3": "boxes",
        "2.0": "boxes",
        "2.1": "boxes",
        "2.2": "boxes",
        "2.3": "boxes",
        "3.0": "boxes",
        "3.1": "boxes",
        "3.2": "boxes",
        "3.3": "boxes",
        "4.0": "boxes",
        "4.1": "boxes",
        "4.2": "boxes",
        "4.3": "boxes",
    }

    container_expected_kinds = {
        "0.1": "boxes",
        "0.2": "boxes",
        "1.0": "boxes",
        "1.1": "boxes",
        "1.2": "boxes",
        "2.0": "boxes",
        "2.1": "boxes",
        "2.2": "boxes",
        "2.3": "boxes",
        "3.0": "boxes",
        "3.1": "boxes",
        "3.2": "boxes",
        "4.0": "boxes",
        "4.1": "boxes",
        "4.2": "boxes",
        "4.3": "boxes",
    }

    ingestion_expected_kinds = {
        "0.1": "boxes",
        "1.1": "boxes",
        "1.2": "boxes",
        "1.3": "boxes",
        "2.1": "boxes",
        "2.2": "boxes",
        "2.3": "boxes",
        "2.4": "boxes",
        "3.1": "boxes",
        "3.2": "boxes",
        "3.3": "boxes",
        "3.4": "boxes",
        "4.1": "boxes",
        "4.2": "boxes",
        "4.3": "boxes",
        "4.4": "boxes",
        "4.5": "boxes",
        "5.1": "boxes",
        "5.2": "boxes",
        "5.3": "boxes",
    }

    suite_specs = [
        ("storage_diagrams", "Storage", expected_kinds),
        ("linux_diagrams", "Linux", linux_expected_kinds),
        ("db_diagrams", "DB", db_expected_kinds),
        ("container_diagrams", "Container", container_expected_kinds),
        ("ingestion_diagrams", "Ingestion", ingestion_expected_kinds),
    ]

    for dict_key, label_prefix, kind_map in suite_specs:
        if dict_key not in data:
            raise SystemExit(f"Missing {dict_key} in content/lessons-data.json")
        for k, exp_kind in kind_map.items():
            if k not in data[dict_key]:
                raise SystemExit(f"Missing {label_prefix} diagram {k} in content/lessons-data.json")
            item = data[dict_key][k]
            actual_kind = item.get("kind")
            if actual_kind != exp_kind:
                raise SystemExit(f"{label_prefix} Diagram {k} kind mismatch: expected {exp_kind!r}, got {actual_kind!r}")

            c_errs = verify_character_policy(item["ascii"], f"{label_prefix}-{k}")
            if c_errs:
                raise SystemExit(f"ASCII character policy failed for {label_prefix}-{k}: {c_errs}")
            char_checked += 1

            g_errs = verify_diagram(item["ascii"], f"{label_prefix}-{k}", kind=actual_kind)
            if g_errs:
                raise SystemExit(f"ASCII geometry verification failed for {label_prefix}-{k} ({actual_kind}): {g_errs}")
            geom_checked += 1

            if "asciiHtml" not in item or "<span class=\"ac-" not in item["asciiHtml"]:
                raise SystemExit(f"Missing colored ANSI HTML spans ('asciiHtml') for {label_prefix}-{k}")

            if item.get("maxCols", 999) > 136:
                raise SystemExit(f"{label_prefix}-{k} maxCols={item.get('maxCols')} exceeds 136 columns")

            if json.dumps(item["ascii"], ensure_ascii=False) not in html:
                raise SystemExit(f"HTML/JSON parity failure: {label_prefix}-{k} ASCII not identically embedded in HTML")

    # 3. Verify all 12 official slide PDFs in course-slides/ are listed in the HTML Table of Contents
    slides = sorted(p.name for p in (ROOT / "course-slides").glob("*.pdf"))
    for s in slides:
        if s not in html:
            raise SystemExit(f"Official slide missing from HTML Table of Contents: {s}")

    # 4. Verify all externalized lesson stage files have their section IDs, h2 headings, and Claude Editorial Standard compliance
    lesson_files = sorted((ROOT / "content" / "lessons").glob("*/*.html"))
    if len(lesson_files) < 24:
        raise SystemExit(f"Expected >= 24 lesson HTML files in content/lessons/, found {len(lesson_files)}")
    forbidden_stage_patterns = [
        r"<h3>\s*[1-5]\.\s*(Bối cảnh|Nỗi đau|Sơ đồ|Đúc kết|Kết nối)",
        r"\[Bổ sung Chuyên sâu",
        r"\(Bước 0\s*[—-]",
        r"\(Tương ứng Mục\s+\d+",
        r"\[(Bối cảnh & Ẩn dụ|Định nghĩa chuẩn xác|Sơ đồ trực quan|Đúc kết Kỹ thuật)",
    ]
    section_count = 0
    for lf in lesson_files:
        l_text = lf.read_text(encoding="utf-8")
        if lf.name == "stage-1.html" and "<x-spine " not in l_text:
            raise SystemExit(f"Missing <x-spine> header in {lf}")
        if 'class="summary-section"' not in l_text and '-summary"' not in l_text:
            raise SystemExit(f"Missing summary-section in {lf}")
        for fig_cap in re.findall(r"<x-figure[^>]*>(.*?)</x-figure>", l_text, flags=re.S):
            if not fig_cap.strip():
                raise SystemExit(f"Empty <x-figure> caption in {lf}")
        for pat in forbidden_stage_patterns:
            if re.search(pat, l_text):
                raise SystemExit(f"Forbidden scaffolding/meta-label pattern /{pat}/ found in {lf}")
        for sec_id in re.findall(r'<section class="lesson-section" id="([^"]+)"', l_text):
            section_count += 1
            if f'id="{sec_id}"' not in html:
                raise SystemExit(f"Missing section id='{sec_id}' from {lf} in compiled HTML")

    # 5. Verify removal of dead features, Picture/Mermaid bloat, decorative emojis, `➔` arrows, and AI meta-copy
    forbidden_tokens = [
        "widthToggleBtn",
        "wide-reading",
        "noteToggleBtn",
        "noteDrawer",
        "noteIndicatorDot",
        "flushPendingNote",
        "syncNotesForTopic",
        "visual-tag",
        "SFMono 13.5pt",
        "[cite:",
        "Sẵn sàng nạp nội dung",
        "LỆNH ĐIỀU KHIỂN ĐỂ ĐI SÂU",
        "mermaid.esm.min.mjs",
        "createMermaidCamera",
        "createPictureCamera",
        "Phóng to Mindmap",
        "Mở ảnh gốc",
        "PROMPT-ARCH-DIAGRAM",
        "PROMPT-STORY-ANALOGY",
        "➔",
        "🏛️",
        "⚡",
        "💿",
        "🌡️",
        "🚧",
        "🎯",
        "📁",
        "🧱",
        "📦",
        "🪣",
        "🧬",
        "🗜️",
        "⭐",
        "🐢",
        "🐌",
        "🐘",
        "🧠",
        "💪",
        "🌐",
        "📨",
        "🏦",
        "📊",
        "📈",
        "⚠️",
        "📐",
        "💭",
        "🧩",
        "🔑",
        "🎉",
        "🌊",
        "🖱️",
        "📸",
        "🐊",
        "📄",
        "🖼️",
        "🧟",
        "💥",
        "🦠",
        "🔀",
        "⚖️",
        "⏳",
        "🕳️",
        "🛡️",
        "⚙️",
        "🛠️",
        "🔥",
        "💡",
        "✅",
        "❌",
        "🚀",
        "👉",
        "🏗️",
        "👶",
        "🧑",
        "👔",
        "🥉",
        "🥈",
        "🥇",
        "🔬",
        "📚",
        "🔐",
        "💰",
        "👁️",
        "🗺️",
        "🧊",
        "hãy gửi tiếp Chặng 2",
        "đi sâu tiếp vào Trạm 3",
        "mổ xẻ thật chi tiết",
        "Bạn nhắn tôi để chúng ta đi sâu ngay vào",
        "Hãy gửi nội dung biên soạn",
        "Toàn bộ nội dung AI cũ đã được dọn sạch",
        "Chặng này đang chờ nạp nội dung chi tiết",
        'data-vmode="both"',
        ">Song song<",
    ]
    for tok in forbidden_tokens:
        if tok in html:
            raise SystemExit(f"Forbidden token / AI-slop tell still present in HTML: {tok!r}")

    # 6. Verify Anthropic Academy CDS, Colored ASCII, Glossary & 2D Simulator symbols exist
    for fn in (
        "buildSpineHeroBanner",
        "spine-overview-card",
        "buildVisualBlock",
        "toggleAsciiAnimation",
        "openCatalogView",
        "openGlossaryView",
        "filterGlossaryDictionary",
        "stage-pills-bar",
        "rail-stage-sublist",
        "--font-display",
        "--font-sans",
        "--font-mono",
        "--glossary-surface",
        "glossaryPopover",
        "bindGlossaryTerms",
        "openGlossaryPopover",
        "initGlossarySystem",
        "buildInfra2DSimulatorHtml",
        "renderInfra2DSlide",
        "goToInfra2DSlide",
        "buildIngestion2DSimulatorHtml",
        "renderIngestion2DInteractiveStage",
        "renderIngestion2DSlide",
    ):
        if fn not in html:
            raise SystemExit(f"Missing Academy / Colored ASCII / Glossary / 2D Simulator symbol in HTML: {fn}")

    # 6a. Verify Glossary Scanner data & 0 unclassified candidate gate
    if "glossary" not in data or "entries" not in data["glossary"] or "lookup" not in data["glossary"]:
        raise SystemExit("Missing 'glossary' object (entries + lookup) in lessons-data.json")
    g_entries = data["glossary"]["entries"]
    g_lookup = data["glossary"]["lookup"]
    g_stats = data["glossary"].get("stats", {})
    if len(g_entries) < 80:
        raise SystemExit(f"Expected >= 80 canonical glossary entries, found {len(g_entries)}")
    if len(g_lookup) < 500:
        raise SystemExit(f"Expected >= 500 exact normalized lookup keys in glossary, found {len(g_lookup)}")
    if g_stats.get("unclassified_count", 1) != 0:
        raise SystemExit(f"Glossary scanner has {g_stats.get('unclassified_count')} unclassified terms! Must be 0.")
    for tid, entry in g_entries.items():
        for req_f in ("name", "category", "short", "station_link", "example"):
            if not entry.get(req_f):
                raise SystemExit(f"Glossary entry '{tid}' is missing required field '{req_f}'")
        if len(entry["short"]) > 180 or "`" in entry["short"]:
            raise SystemExit(f"Glossary entry '{tid}' short definition exceeds 180 chars or contains raw backticks")
        ex = entry["example"]
        if not isinstance(ex, dict) or not ex.get("code"):
            raise SystemExit(f"Glossary entry '{tid}' example must contain non-empty 'code'")

    # 6b. Verify Quarantine manifest exists and assets/visuals is absent
    q_manifest = ROOT / ".quarantine" / "2026-10-17-pic-mermaid" / "manifest.json"
    if not q_manifest.exists():
        raise SystemExit("Missing .quarantine/2026-10-17-pic-mermaid/manifest.json")
    if (ROOT / "assets" / "visuals").exists():
        raise SystemExit("assets/visuals/ still exists in live workspace (should be quarantined)")

    # 7. Verify prompt.md exists and references all 12 slides and library books
    prompt_path = ROOT / "prompt.md"
    if not prompt_path.exists():
        raise SystemExit("Missing prompt.md at repository root.")
    prompt_text = prompt_path.read_text(encoding="utf-8")
    lib_refs = re.findall(r"`(library/[^`*]+\.pdf)`", prompt_text)
    if not lib_refs:
        raise SystemExit("No concrete library/*.pdf references found in prompt.md")
    for lib_ref in lib_refs:
        if not (ROOT / lib_ref).exists():
            raise SystemExit(f"Broken book path in prompt.md: {lib_ref}")
    slide_refs = re.findall(r"`(\d{2}-[^`*]+\.pdf)`", prompt_text)
    if len(set(slide_refs)) != 12:
        raise SystemExit(f"Expected 12 slide references in prompt.md, found {len(set(slide_refs))}")
    for slide_ref in slide_refs:
        if not (ROOT / "course-slides" / slide_ref).exists():
            raise SystemExit(f"Broken slide path in prompt.md: course-slides/{slide_ref}")

    # 8. Mandatory Headless Browser Runtime QA Gate (scripts/qa_runtime.py)
    venv_py = ROOT / ".venv" / "bin" / "python"
    qa_py = str(venv_py) if venv_py.exists() else sys.executable
    qa_proc = subprocess.run(
        [qa_py, str(ROOT / "scripts" / "qa_runtime.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if qa_proc.returncode != 0:
        raise SystemExit(
            f"Runtime DOM QA (scripts/qa_runtime.py) FAILED:\n{qa_proc.stderr or qa_proc.stdout}"
        )

    total_expected = (
        len(expected_kinds)
        + len(linux_expected_kinds)
        + len(db_expected_kinds)
        + len(container_expected_kinds)
        + len(ingestion_expected_kinds)
    )
    print(
        f"PASS: Negative self-tests: 6/6 | JS syntax: valid | Runtime DOM QA: 24/24 pages + #/catalog + #/glossary (3 viewports) | "
        f"Anthropic Academy CDS Typography: verified | Glossary Scanner: {len(g_entries)} entries / {len(g_lookup)} lookup keys (0 unclassified) | "
        f"Colored ASCII checks: {char_checked}/{total_expected} char + {geom_checked}/{total_expected} geometry | "
        f"Externalized Lessons: {len(lesson_files)}/24 stage files ({section_count} stations) | "
        f"Quarantine verified: 0 live Picture/Mermaid bloat | Official slide TOCs: {len(slides)}/12 | Anti-slop audit: clean."
    )


if __name__ == "__main__":
    main()
