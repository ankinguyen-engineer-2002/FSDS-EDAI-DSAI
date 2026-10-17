#!/usr/bin/env python3
"""
Headless Monodraw + Durdraw Non-Destructive Color Brush Engine (`painter.py`).
Paints verified ASCII/Unicode box-drawing diagrams with semantic `<span class="ac-{role}">`
overlays while guaranteeing 100% character-for-character parity (`textContent === raw_ascii`).
"""
import html
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .dur_loader import load_dur_overlay

BOX_BORDER_CHARS = set("┌┐└┘├┤┬┴┼─│═║╔╗╚╝╠╣╦╩╬╭╮╰╯+")
SHADOW_CHARS = set("░▒▓█")
ARROW_CHARS = set("▲▼◄►")

# Regex patterns painted in priority order (lower priority first, higher priority overrides)
SPAN_PATTERNS: List[Tuple[re.Pattern, str]] = [
    # Comments at end of line (# ...)
    (re.compile(r"(?<=\s)#\s[^\│║\n]+$"), "muted"),
    # Bracketed headers, stage/step badges, numbered pills
    (re.compile(r"\[(?:CHẶNG|TRẠM|BƯỚC|TẦNG|STAGE|STEP|STATION|PHASE|LAYER|NODE|POD|VM|HOST|KERNEL|DISK|RAM|CPU|WAL|MVCC|ACID|CAP|BASE|BRONZE|SILVER|GOLD)[^\]]*\]", re.IGNORECASE), "header"),
    (re.compile(r"\([1-9]\)|\[[1-9]\]|\b(?:CHẶNG|TRẠM|BƯỚC)\s+\d+(?:\.\d+)?\b"), "header"),
    # Success / active / fast path tokens
    (re.compile(r"\b(?:OK|PASS|READY|ACTIVE|COMMIT|COMMITTED|ACID|HIT|CACHE HIT|ZERO-COPY|ONLINE|HEALTHY|RUNNING|SYNC|IMMUTABLE)\b"), "ok"),
    # Warning / lock / transaction / copy-on-write tokens
    (re.compile(r"\b(?:WARN|WAIT|WAITING|LOCK|LOCKED|RETRY|CACHE MISS|MISS|WAL|MVCC|COW|MOR|DIRTY|THROTTLE|PENDING|ASYNC)\b"), "warn"),
    # Danger / failure / crash / OOM / bottleneck tokens
    (re.compile(r"\b(?:ERROR|ERR|FAIL|FAILED|OOM|OOM KILLER|SIGKILL|DEADLOCK|CRASH|SPOF|DROP|CONFLICT|ABORT|ROLLBACK|CORRUPT|BOTTLENECK)\b"), "danger"),
    # Data flow connectors & directional arrows
    (re.compile(r"(?:◄──+►|──+►|◄──+|==+>|──+>|<-+|--+>|◄═+►|═+►|◄═+)"), "flow"),
]


def add_monodraw_shadow(box_lines: List[str], shadow_char: str = "░") -> List[str]:
    """
    Monodraw 1-Click 3D Shadow generator: appends a 1-cell right shadow starting on row 1
    and a bottom shadow row offset by 1 column using `shadow_char` (`░`, `▒`, or `▓`).
    """
    if not box_lines:
        return []
    ch = shadow_char[0] if shadow_char else "░"
    width = max(len(l) for l in box_lines)
    out: List[str] = []
    for idx, line in enumerate(box_lines):
        padded = line.ljust(width)
        if idx == 0:
            out.append(padded)
        else:
            out.append(padded + ch)
    out.append(" " + (ch * width))
    return out


def classify_line_roles(
    line: str,
    row_idx: int = 0,
    dur_overlay: Optional[Dict[Tuple[int, int], str]] = None,
) -> List[Optional[str]]:
    """
    Return a per-character list of semantic role names for `line` without modifying any character.
    """
    n = len(line)
    roles: List[Optional[str]] = [None] * n

    # 1. Apply regex span patterns on text tokens
    for rx, role in SPAN_PATTERNS:
        for m in rx.finditer(line):
            for i in range(m.start(), m.end()):
                roles[i] = role

    # 2. Apply single-character geometric roles (borders, shadows, arrows Always win over text regex)
    for i, ch in enumerate(line):
        if ch in SHADOW_CHARS:
            roles[i] = "shadow"
        elif ch in ARROW_CHARS:
            roles[i] = "flow"
        elif ch in BOX_BORDER_CHARS:
            # Keep flow role if part of a flow arrow already matched
            if roles[i] != "flow":
                roles[i] = "border"

    # 3. Apply explicit Durdraw `.dur` cell overlay if provided (highest priority)
    if dur_overlay:
        for i in range(n):
            ov = dur_overlay.get((row_idx, i))
            if ov:
                roles[i] = ov

    return roles


def strip_html_tags_unescape(html_str: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", html_str))


def paint_ascii_html(
    raw_ascii: str,
    dur_overlay: Optional[Dict[Tuple[int, int], str]] = None,
    dur_path: Optional[Path] = None,
) -> Tuple[str, int, List[List[Optional[str]]]]:
    """
    Non-destructively paint `raw_ascii` into semantic HTML `<span class="ac-{role}">` runs.
    Returns `(painted_html, max_cols, role_grid)`.
    Raises `AssertionError` if `strip_html_tags_unescape(painted_html) != raw_ascii`.
    """
    if dur_overlay is None and dur_path is not None and dur_path.exists():
        dur_overlay = load_dur_overlay(dur_path)

    lines = raw_ascii.split("\n")
    max_cols = max((len(l) for l in lines), default=0)
    painted_lines: List[str] = []
    role_grid: List[List[Optional[str]]] = []

    for r_idx, line in enumerate(lines):
        roles = classify_line_roles(line, r_idx, dur_overlay)
        role_grid.append(roles)
        if not line:
            painted_lines.append("")
            continue

        # Merge contiguous characters sharing the same role into minimal <span> runs
        runs: List[str] = []
        cur_role = roles[0]
        cur_chars: List[str] = [line[0]]
        for ch, r in zip(line[1:], roles[1:]):
            if r == cur_role:
                cur_chars.append(ch)
            else:
                escaped = html.escape("".join(cur_chars))
                runs.append(f'<span class="ac-{cur_role}">{escaped}</span>' if cur_role else escaped)
                cur_role = r
                cur_chars = [ch]
        escaped = html.escape("".join(cur_chars))
        runs.append(f'<span class="ac-{cur_role}">{escaped}</span>' if cur_role else escaped)
        painted_lines.append("".join(runs))

    painted_html = "\n".join(painted_lines)
    recovered = strip_html_tags_unescape(painted_html)
    if recovered != raw_ascii:
        raise AssertionError("Durdraw Painter invariant violated: painted HTML textContent != raw_ascii")
    return painted_html, max_cols, role_grid
