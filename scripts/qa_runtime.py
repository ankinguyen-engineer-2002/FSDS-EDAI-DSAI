#!/usr/bin/env python3
"""Runtime DOM & Visual QA verifier for FSDS Learning Hub using headless Playwright."""
from __future__ import annotations

import argparse
import glob
import http.server
import json
import os
import socket
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TOPIC_STAGES: list[tuple[str, int]] = (
    [("F01", s) for s in range(1, 5)]
    + [("F03", s) for s in range(1, 5)]
    + [("F06", s) for s in range(1, 5)]
    + [("D02", s) for s in range(1, 8)]
)

VIEWPORTS = [
    ("desktop", 1440, 900),
    ("tablet", 768, 1024),
    ("mobile", 390, 844),
]


def _find_chromium_executable() -> str | None:
    cache_dir = Path.home() / "Library" / "Caches" / "ms-playwright"
    patterns = [
        str(cache_dir / "chromium_headless_shell-*" / "chrome-headless-shell-mac-*" / "chrome-headless-shell"),
        str(cache_dir / "chromium-*" / "chrome-mac" / "Chromium.app" / "Contents" / "MacOS" / "Chromium"),
    ]
    candidates: list[str] = []
    for pat in patterns:
        candidates.extend(glob.glob(pat))
    candidates = [c for c in sorted(candidates, reverse=True) if os.access(c, os.X_OK)]
    return candidates[0] if candidates else None


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format: str, *args) -> None:
        pass


def _ensure_server(port: int = 8765) -> tuple[str, http.server.ThreadingHTTPServer | None]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if sock.connect_ex(("127.0.0.1", port)) == 0:
            return f"http://127.0.0.1:{port}/index.html", None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _QuietHandler)
    actual_port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return f"http://127.0.0.1:{actual_port}/index.html", server


def run_qa(
    url: str,
    snapshot_dir: Path | None = None,
    baseline_dir: Path | None = None,
    check_backticks: bool = False,
) -> dict:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "ERROR: playwright is not installed in this Python interpreter.\n"
            "Run with `.venv/bin/python scripts/qa_runtime.py` or install via `.venv/bin/pip install playwright`.",
            file=sys.stderr,
        )
        sys.exit(2)

    if snapshot_dir:
        snapshot_dir.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    pages_report: dict[str, dict] = {}
    console_errors: list[str] = []

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
        except Exception:
            exe = _find_chromium_executable()
            if not exe:
                raise
            browser = p.chromium.launch(headless=True, executable_path=exe)

        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        page.on(
            "console",
            lambda msg: console_errors.append(f"[{msg.type}] {msg.text}")
            if msg.type == "error"
            else None,
        )
        page.on("pageerror", lambda exc: console_errors.append(f"[pageerror] {exc}"))

        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(300)

        for topic, stage in TOPIC_STAGES:
            key = f"{topic}-{stage}"
            page.set_viewport_size({"width": 1440, "height": 900})
            page.evaluate(f"selectTopic({json.dumps(topic)}, {stage})")
            page.wait_for_timeout(180)

            audit = page.evaluate(
                """() => {
                const mainEl = document.querySelector('#mainContent') || document.querySelector('main') || document.body;
                const imgs = Array.from(mainEl.querySelectorAll('img'));
                const txt = mainEl.innerText || '';
                const undefMatches = txt.match(/\\b(?:undefined|NaN)\\b/g) || [];
                const escapedMatches = txt.match(/<\\/?(?:code|strong|em|span|div)>|&(?:amp|lt|gt|quot);/g) || [];
                const backtickMatches = txt.match(/`/g) || [];
                const pipelineMatches = txt.match(/PROMPT-[A-Z0-9_-]+|STYLE\\s*#2|Style\\s*#2|READY\\s*·|Phóng to Mindmap|Mở ảnh gốc/g) || [];
                const arrowMatches = txt.match(/➔/g) || [];

                // Glossary density invariants:
                // 0 in .lesson-lead, max 5 per .lesson-section, max 1 per p/li/td
                const leadTerms = mainEl.querySelectorAll('.lesson-lead .glossary-term').length;
                let maxStationTerms = 0;
                mainEl.querySelectorAll('.lesson-section').forEach(sec => {
                  const c = sec.querySelectorAll('.glossary-term').length;
                  if (c > maxStationTerms) maxStationTerms = c;
                });

                // Check prose text without UI chrome/diagram pre blocks for baseline diffing
                const proseClone = mainEl.cloneNode(true);
                proseClone.querySelectorAll('.visual-bar, .stage-pills-bar, .lesson-stage-subtitle, .lesson-pager').forEach(el => el.remove());
                const cleanProseText = (proseClone.innerText || '').replace(/\\s+/g, ' ').trim();
                const figCount = mainEl.querySelectorAll('figure.visual-card').length;
                const preCount = mainEl.querySelectorAll('pre.ascii-diagram').length;
                const stagePills = mainEl.querySelectorAll('.stage-pills-bar .stage-pill-btn').length;
                const railStages = document.querySelectorAll('#syllabusRail .rail-stage-sublist .rail-stage-btn').length;

                return {
                  imgCount: imgs.length,
                  undefCount: undefMatches.length,
                  escapedMatches: escapedMatches.slice(0, 10),
                  escapedCount: escapedMatches.length,
                  backtickCount: backtickMatches.length,
                  pipelineMatches: pipelineMatches.slice(0, 10),
                  pipelineCount: pipelineMatches.length,
                  arrowCount: arrowMatches.length,
                  leadTerms,
                  maxStationTerms,
                  cleanProseText,
                  figCount,
                  preCount,
                  stagePills,
                  railStages,
                };
              }"""
            )

            overflow_by_vp: dict[str, dict[str, int]] = {}
            for vp_name, w, h in VIEWPORTS:
                page.set_viewport_size({"width": w, "height": h})
                page.wait_for_timeout(50)
                dims = page.evaluate(
                    "() => ({ scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth })"
                )
                overflow_by_vp[vp_name] = dims
                if dims["scrollWidth"] > dims["innerWidth"]:
                    failures.append(
                        f"{key} [{vp_name} {w}px]: horizontal overflow scrollWidth={dims['scrollWidth']} > innerWidth={dims['innerWidth']}"
                    )

            if audit["imgCount"] > 0:
                failures.append(f"{key}: expected 0 <img> tags in pure Colored-ASCII mode, found {audit['imgCount']}")
            if audit["undefCount"] > 0:
                failures.append(f"{key}: found {audit['undefCount']} 'undefined'/'NaN' in visible text")
            if audit["escapedCount"] > 0:
                failures.append(
                    f"{key}: found {audit['escapedCount']} raw HTML tags/entities {audit['escapedMatches']}"
                )
            if check_backticks and audit["backtickCount"] > 0:
                failures.append(f"{key}: found {audit['backtickCount']} raw backticks in visible text")
            if audit["pipelineCount"] > 0:
                failures.append(
                    f"{key}: found {audit['pipelineCount']} leaked pipeline strings {audit['pipelineMatches']}"
                )
            if audit["arrowCount"] > 0:
                failures.append(f"{key}: found {audit['arrowCount']} forbidden '➔' arrows in visible text")
            if audit["leadTerms"] > 0:
                failures.append(f"{key}: found {audit['leadTerms']} glossary terms inside .lesson-lead (expected 0)")
            if audit["maxStationTerms"] > 5:
                failures.append(f"{key}: found {audit['maxStationTerms']} glossary terms in a single station (max 5)")
            if audit["stagePills"] == 0:
                failures.append(f"{key}: missing .stage-pills-bar buttons")
            if audit["railStages"] == 0:
                failures.append(f"{key}: missing nested .rail-stage-sublist in left sidebar")

            if snapshot_dir:
                (snapshot_dir / f"{key}.txt").write_text(audit["cleanProseText"], encoding="utf-8")
                (snapshot_dir / f"{key}.meta.json").write_text(
                    json.dumps(
                        {"figCount": audit["figCount"], "preCount": audit["preCount"]},
                        ensure_ascii=False,
                        indent=2,
                    ),
                    encoding="utf-8",
                )
                page.set_viewport_size({"width": 1440, "height": 900})
                page.screenshot(path=str(snapshot_dir / f"{key}.png"), full_page=False)

            if baseline_dir:
                base_txt_path = baseline_dir / f"{key}.txt"
                if base_txt_path.exists():
                    base_txt = base_txt_path.read_text(encoding="utf-8")
                    if base_txt != audit["cleanProseText"]:
                        failures.append(
                            f"{key}: innerText mismatch vs baseline (len {len(audit['cleanProseText'])} vs {len(base_txt)})"
                        )

            pages_report[key] = {
                "imgCount": audit["imgCount"],
                "undefCount": audit["undefCount"],
                "escapedCount": audit["escapedCount"],
                "backtickCount": audit["backtickCount"],
                "pipelineCount": audit["pipelineCount"],
                "figCount": audit["figCount"],
                "preCount": audit["preCount"],
                "overflow": overflow_by_vp,
            }

        # Verify URL routing & browser history (history.back() / history.forward() / hashchange)
        page.evaluate("() => selectTopic('F03', 2)")
        page.wait_for_timeout(80)
        page.evaluate("() => selectTopic('D02', 3)")
        page.wait_for_timeout(80)
        page.evaluate("() => history.back()")
        page.wait_for_timeout(120)
        after_back = page.evaluate("() => ({ topic: activeTopic, stage: activeStorageStage, hash: window.location.hash })")
        if after_back["topic"] != "F03" or after_back["stage"] != 2:
            failures.append(f"Router history.back() failed: expected F03 stage 2, got {after_back}")
        page.evaluate("() => { window.location.hash = '#topic=F06&stage=2'; }")
        page.wait_for_timeout(120)
        after_hash = page.evaluate("() => ({ topic: activeTopic, stage: activeStorageStage })")
        if after_hash["topic"] != "F06" or after_hash["stage"] != 2:
            failures.append(f"Router legacy hashchange (#topic=F06&stage=2) failed: expected F06 stage 2, got {after_hash}")

        # Verify Phase 2 & 4 (TOC + Lesson Pager + Skip Link + Colored ASCII + Spine Overview Card)
        page.set_viewport_size({"width": 1440, "height": 900})
        page.evaluate("() => selectTopic('F01', 1)")
        page.wait_for_timeout(100)
        p2_audit = page.evaluate(
            """() => ({
                hasSkipLink: Boolean(document.querySelector('a.skip-link')),
                tocLinks: document.querySelectorAll('#pageTocPanel a.page-toc-link').length,
                tocCodeSpans: document.querySelectorAll('#pageTocPanel .page-toc-code').length,
                pagerCards: document.querySelectorAll('.lesson-pager .lesson-pager-card').length,
                spineCards: document.querySelectorAll('.spine-overview-card').length,
                colorSpans: document.querySelectorAll('pre.ascii-diagram span[class^="ac-"]').length,
                pulseSpans: document.querySelectorAll('.visual-card[data-flagship="true"] pre.ascii-diagram span.ac-flow').length
            })"""
        )
        if not p2_audit["hasSkipLink"]:
            failures.append("Phase 2 QA: missing a.skip-link")
        if p2_audit["tocLinks"] == 0:
            failures.append("Phase 2 QA: #pageTocPanel has 0 links on F01 stage 1")
        if p2_audit["tocCodeSpans"] > 0:
            failures.append("Phase 2 QA: #pageTocPanel still has old two-column .page-toc-code spans")
        if p2_audit["pagerCards"] == 0:
            failures.append("Phase 2 QA: missing .lesson-pager-card on F01 stage 1")
        if p2_audit["spineCards"] == 0:
            failures.append("Phase 5 QA: missing .spine-overview-card on F01 stage 1")
        if p2_audit["colorSpans"] == 0:
            failures.append("Phase 4 QA: pre.ascii-diagram has 0 semantic color spans (span.ac-*)")
        if p2_audit["pulseSpans"] == 0:
            failures.append("Phase 4 QA: flagship diagram on F01 stage 1 has 0 animated .ac-flow spans")

        # Verify Phase 3 Minimalist Glossary Popover & Escape focus restoration
        glossary_qa = page.evaluate(
            """() => {
                const term = document.querySelector('#articleContainer .glossary-term');
                if (!term) return { ok: false, reason: 'no .glossary-term found' };
                term.focus();
                term.click();
                const pop = document.getElementById('glossaryPopover');
                const isOpen = pop && pop.classList.contains('open');
                const rect = pop ? pop.getBoundingClientRect() : { width: 0, height: 0 };
                const intuitionText = document.getElementById('glossaryPopIntuition')?.textContent || '';
                const catText = document.getElementById('glossaryPopCategory')?.textContent || '';
                const hasBackticks = intuitionText.includes('`');
                document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
                const closedAfterEsc = pop && !pop.classList.contains('open');
                const focusRestored = (document.activeElement === term);
                return {
                    ok: isOpen && closedAfterEsc && focusRestored && !hasBackticks && Boolean(catText) && rect.width <= 760,
                    isOpen,
                    closedAfterEsc,
                    focusRestored,
                    hasBackticks,
                    catText,
                    width: Math.round(rect.width)
                };
            }"""
        )
        if not glossary_qa.get("ok"):
            failures.append(f"Phase 3 Glossary Popover QA failed: {glossary_qa}")

        # Verify Phase 4 prefers-reduced-motion disables ASCII flow pulse animation
        page.emulate_media(reduced_motion="reduce")
        page.wait_for_timeout(50)
        anim_name_reduced = page.evaluate(
            """() => {
                const el = document.querySelector('.visual-card[data-flagship="true"] pre.ascii-diagram span.ac-flow');
                return el ? window.getComputedStyle(el).animationName : 'none';
            }"""
        )
        if anim_name_reduced != "none":
            failures.append(f"Phase 4 a11y: prefers-reduced-motion did not disable .ac-flow animation (got {anim_name_reduced})")
        page.emulate_media(reduced_motion="no-preference")

        # Verify Catalog View (#/catalog)
        page.evaluate("() => openCatalogView()")
        page.wait_for_timeout(80)
        cat_cards = page.evaluate("() => document.querySelectorAll('.catalog-card').length")
        if cat_cards < 20:
            failures.append(f"Phase 2 Catalog QA: expected >= 20 .catalog-card items, got {cat_cards}")

        # Verify Glossary Dictionary View (#/glossary)
        page.evaluate("() => openGlossaryView()")
        page.wait_for_timeout(80)
        gdict_cards = page.evaluate("() => document.querySelectorAll('.glossary-dict-card').length")
        if gdict_cards < 70:
            failures.append(f"Phase 3 Glossary Dictionary QA: expected >= 70 .glossary-dict-card items, got {gdict_cards}")

        browser.close()

    non_404_console_errors = [
        e for e in console_errors if "Failed to load resource" not in e
    ]
    if non_404_console_errors:
        for err in non_404_console_errors[:10]:
            failures.append(f"console/page error: {err}")

    return {
        "passed": len(failures) == 0,
        "failureCount": len(failures),
        "failures": failures,
        "pages": pages_report,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Playwright runtime QA across all 19 FSDS Hub pages.")
    parser.add_argument("--url", default="", help="URL to test (starts local server if omitted)")
    parser.add_argument("--snapshot", default="", help="Directory to save innerText & screenshot baseline")
    parser.add_argument("--verify-baseline", default="", help="Directory to compare innerText against")
    parser.add_argument("--check-backticks", action="store_true", help="Fail if backticks appear in visible text")
    parser.add_argument("--json-out", default="", help="Write JSON report to file")
    args = parser.parse_args()

    url, server = (args.url, None) if args.url else _ensure_server(8765)
    try:
        report = run_qa(
            url=url,
            snapshot_dir=Path(args.snapshot) if args.snapshot else None,
            baseline_dir=Path(args.verify_baseline) if args.verify_baseline else None,
            check_backticks=args.check_backticks,
        )
    finally:
        if server:
            server.shutdown()

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if report["passed"]:
        print("QA_RUNTIME PASS: 19/19 pages + #/catalog + #/glossary verified across 3 viewports (0 failures).")
        sys.exit(0)
    else:
        print(f"QA_RUNTIME FAIL: {report['failureCount']} failure(s) detected:", file=sys.stderr)
        for f in report["failures"]:
            print(f"  - {f}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
