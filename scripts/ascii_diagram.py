#!/usr/bin/env python3
"""
Strict Unicode/ASCII Diagram Builder & Multi-Layer Geometry Verifier.
Workflow: PLAN -> BUILD -> GEOMETRY VERIFY -> BROWSER PIXEL-GRID VERIFY.

Guarantees:
1. NFC Normalization on all input/output strings.
2. Strict Single-Cell Character Policy: rejects tabs, control chars, zero-width chars,
   variation selectors, and variable-width emojis anywhere in a diagram.
3. Strict Padding Contract: `pad_right` and `pad_center` raise `ValueError` immediately
   if `display_width(text) > width` (never silently overflows a column or shifts a border).
4. Diagram-Kind Geometry Verifiers:
   - `boxes`: verifies every `┌─...─┐`, `│...│`, `└─...─┘` shares identical start/end display columns.
   - `pyramid`: verifies apex `▲` at `C`, left `/` at `C - k`, right `\\` at `C + k`, base `└...┘`
     at `(C - K, C + K)`, constant vertical table divider `│`/`┼` column, and constant callout `◄──` column.
5. Built-in Regression Self-Test (`--self-test`) proving negative fixtures are caught.
"""
import argparse
import re
import sys
import unicodedata
from typing import Dict, List, Optional, Tuple


FORBIDDEN_CODEPOINTS = {
    0x200B,  # ZERO WIDTH SPACE
    0x200C,  # ZERO WIDTH NON-JOINER
    0x200D,  # ZERO WIDTH JOINER
    0xFEFF,  # ZERO WIDTH NO-BREAK SPACE
    0xFE0E,  # VARIATION SELECTOR-15
    0xFE0F,  # VARIATION SELECTOR-16
}

ALLOWED_GEOMETRIC_SYMBOLS = set(
    "┌┐└┘├┤┬┴┼─│═║╔╗╚╝╠╣╦╩╬╭╮╰╯░▒▓█▲▼◄►•"
)


def nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def is_forbidden_char(ch: str) -> Optional[str]:
    cp = ord(ch)
    if ch == "\t":
        return "Tab character '\\t' is forbidden in diagrams"
    if cp < 0x20 and ch not in ("\n", "\r"):
        return f"Control character U+{cp:04X} is forbidden"
    if cp in FORBIDDEN_CODEPOINTS:
        return f"Zero-width / variation selector U+{cp:04X} is forbidden"
    if cp >= 0x1F000:
        return f"Variable-width emoji '{ch}' (U+{cp:04X}) is forbidden"
    if 0x2600 <= cp <= 0x27BF and ch not in ALLOWED_GEOMETRIC_SYMBOLS:
        return f"Dingbat/symbol '{ch}' (U+{cp:04X}) is forbidden"
    return None


def char_width(ch: str) -> int:
    if unicodedata.combining(ch):
        return 0
    eaw = unicodedata.east_asian_width(ch)
    if eaw in ("W", "F"):
        return 2
    return 1


def validate_text_cells(text: str, context: str = "text") -> str:
    norm = nfc(text)
    for ch in norm:
        reason = is_forbidden_char(ch)
        if reason:
            raise ValueError(f"[{context}] {reason} in {text!r}")
        if char_width(ch) != 1:
            raise ValueError(
                f"[{context}] Non-single-cell character '{ch}' (U+{ord(ch):04X}, width={char_width(ch)}) in {text!r}"
            )
    return norm


def display_width(text: str) -> int:
    norm = nfc(text)
    return sum(char_width(ch) for ch in norm)


def pad_right(
    text: str,
    width: int,
    fill: str = " ",
    strict: bool = True,
    context: str = "pad_right",
) -> str:
    if not isinstance(width, int) or width < 0:
        raise ValueError(f"[{context}] width must be a non-negative int, got {width!r}")
    fill = validate_text_cells(fill, f"{context}.fill")
    if display_width(fill) != 1:
        raise ValueError(f"[{context}] fill must be exactly 1 cell wide, got {fill!r}")
    norm = validate_text_cells(text, context)
    w = display_width(norm)
    if w > width:
        if strict:
            raise ValueError(
                f"[{context}] Overflow: required={w} cells, available={width} cells, value={norm!r}"
            )
        return norm
    out = norm + (fill * (width - w))
    assert display_width(out) == width
    return out


def pad_center(
    text: str,
    width: int,
    fill: str = " ",
    strict: bool = True,
    context: str = "pad_center",
) -> str:
    if not isinstance(width, int) or width < 0:
        raise ValueError(f"[{context}] width must be a non-negative int, got {width!r}")
    fill = validate_text_cells(fill, f"{context}.fill")
    if display_width(fill) != 1:
        raise ValueError(f"[{context}] fill must be exactly 1 cell wide, got {fill!r}")
    norm = validate_text_cells(text, context)
    w = display_width(norm)
    if w > width:
        if strict:
            raise ValueError(
                f"[{context}] Overflow: required={w} cells, available={width} cells, value={norm!r}"
            )
        return norm
    total = width - w
    left = total // 2
    right = total - left
    out = (fill * left) + norm + (fill * right)
    assert display_width(out) == width
    return out


def make_box(
    lines: List[str],
    inner_width: Optional[int] = None,
    header: Optional[str] = None,
    context: str = "make_box",
) -> List[str]:
    """
    Create a strictly aligned Unicode box around `lines`.
    If `inner_width` is specified, any line exceeding `inner_width` raises `ValueError`.
    """
    norm_lines = [validate_text_cells(line, f"{context}.line[{i}]") for i, line in enumerate(lines)]
    computed_w = max((display_width(line) for line in norm_lines), default=0)
    norm_header = validate_text_cells(header, f"{context}.header") if header else None

    if inner_width is not None:
        if computed_w > inner_width:
            offending = next(l for l in norm_lines if display_width(l) > inner_width)
            raise ValueError(
                f"[{context}] Line overflow: required={display_width(offending)} cells, "
                f"inner_width={inner_width}, value={offending!r}"
            )
        w = inner_width
    else:
        w = computed_w
        if norm_header:
            w = max(w, display_width(norm_header))

    out: List[str] = []
    if norm_header:
        header_box_w = w + 4
        if display_width("  " + norm_header) > header_box_w:
            raise ValueError(
                f"[{context}] Header overflow: required={display_width(norm_header) + 2} cells, "
                f"box_width={header_box_w}, header={norm_header!r}"
            )
        out.append(pad_right("  " + norm_header, header_box_w, context=f"{context}.header_pad"))
    out.append("┌─" + ("─" * w) + "─┐")
    for idx, line in enumerate(norm_lines):
        out.append("│ " + pad_right(line, w, context=f"{context}.row[{idx}]") + " │")
    out.append("└─" + ("─" * w) + "─┘")
    return out


def join_horizontal(
    blocks: List[List[str]],
    gaps: List[str],
    connector_rows: Optional[Dict[int, List[str]]] = None,
    context: str = "join_horizontal",
) -> List[str]:
    """
    Join multiple vertical blocks side-by-side with strict gap width validation.
    Every custom connector row in `connector_rows` must match the exact cell widths of `gaps`.
    """
    if len(gaps) != len(blocks) - 1:
        raise ValueError(f"[{context}] Expected {len(blocks) - 1} gaps, got {len(gaps)}")

    gap_widths = [display_width(validate_text_cells(g, f"{context}.gap[{i}]")) for i, g in enumerate(gaps)]
    connector_rows = connector_rows or {}
    for r_idx, r_gaps in connector_rows.items():
        if len(r_gaps) != len(gaps):
            raise ValueError(f"[{context}] Row {r_idx} connector count mismatch")
        for g_idx, g_str in enumerate(r_gaps):
            gw = display_width(validate_text_cells(g_str, f"{context}.connector[{r_idx}][{g_idx}]"))
            if gw != gap_widths[g_idx]:
                raise ValueError(
                    f"[{context}] Connector width mismatch at row {r_idx}, gap {g_idx}: "
                    f"expected {gap_widths[g_idx]} cells ({gaps[g_idx]!r}), got {gw} cells ({g_str!r})"
                )

    block_widths = [max(display_width(validate_text_cells(line, context)) for line in b) for b in blocks]
    max_rows = max(len(b) for b in blocks)
    out: List[str] = []
    for r in range(max_rows):
        row_parts: List[str] = []
        row_gaps = connector_rows.get(r, gaps)
        for i, b in enumerate(blocks):
            cell = b[r] if r < len(b) else ""
            if i < len(blocks) - 1:
                row_parts.append(pad_right(cell, block_widths[i], context=f"{context}.r{r}b{i}"))
                row_parts.append(row_gaps[i])
            else:
                row_parts.append(cell.rstrip())
        out.append("".join(row_parts).rstrip())
    return out


def _idx_to_col(s: str, char_idx: int) -> int:
    return display_width(s[:char_idx]) + 1


def _col_positions(s: str, target_chars: str) -> List[int]:
    cols = []
    col = 1
    for ch in s:
        if ch in target_chars:
            cols.append(col)
        col += char_width(ch)
    return cols


def verify_character_policy(text: str, name: str) -> List[str]:
    errors: List[str] = []
    lines = text.splitlines()
    if not lines:
        return [f"[{name}] Diagram is empty."]
    for idx, line in enumerate(lines, 1):
        if line != nfc(line):
            errors.append(f"[{name}] Line {idx}: Not NFC normalized.")
        if line.endswith(" "):
            errors.append(f"[{name}] Line {idx}: Trailing whitespace detected.")
        for ch in line:
            reason = is_forbidden_char(ch)
            if reason:
                errors.append(f"[{name}] Line {idx}: {reason}.")
            elif char_width(ch) != 1:
                errors.append(
                    f"[{name}] Line {idx}: Character '{ch}' (U+{ord(ch):04X}) has display width {char_width(ch)} != 1."
                )
    return errors


def verify_box_diagram(text: str, name: str = "diagram") -> List[str]:
    errors: List[str] = []
    lines = text.splitlines()
    active_boxes: List[Tuple[int, int, int]] = []
    total_boxes_verified = 0

    # 1. Verify Unicode boxes (┌..┐ / │..│ / └..┘) and merge/split connectors
    for idx, line in enumerate(lines, 1):
        # First check if any active Unicode box is closed by vertical arrows ▼ at (b_start, b_end) (split connector)
        arrows_down = set(_col_positions(line, "▼v"))
        for b_start, b_end, b_line in list(active_boxes):
            if b_start in arrows_down and b_end in arrows_down:
                active_boxes.remove((b_start, b_end, b_line))
                total_boxes_verified += 1

        for m in re.finditer(r"┌[─┬┴┼▲▼]+┐", line):
            s_col = _idx_to_col(line, m.start())
            e_col = _idx_to_col(line, m.end() - 1)
            active_boxes.append((s_col, e_col, idx))

        for m in re.finditer(r"└[─┴┬┼▲▼]+┘", line):
            cs = _idx_to_col(line, m.start())
            ce = _idx_to_col(line, m.end() - 1)
            matched = [b for b in active_boxes if b[0] == cs and b[1] == ce]
            if not matched:
                # Check if this is a 2-into-1 merge connector (e.g. └───┬───┘ or └───┼───┘ with │ above)
                if idx >= 2 and any(ch in m.group(0) for ch in "┬┼▲▼"):
                    prev_pipes = set(_col_positions(lines[idx - 2], "│├┤┼▲▼"))
                    if cs in prev_pipes and ce in prev_pipes:
                        total_boxes_verified += 1
                        continue
                errors.append(
                    f"[{name}] Line {idx}: Bottom border └..┘ at cols ({cs}, {ce}) does not match any open top border ┌..┐ {[(b[0], b[1]) for b in active_boxes]}."
                )
            else:
                active_boxes.remove(matched[0])
                total_boxes_verified += 1

        pipes = set(_col_positions(line, "│├┤┼"))
        for b_start, b_end, b_line in list(active_boxes):
            if b_line == idx:
                continue
            if b_start not in pipes or b_end not in pipes:
                errors.append(
                    f"[{name}] Line {idx}: Open box from line {b_line} expects '│' at cols ({b_start}, {b_end}), found pipes at {sorted(pipes)}."
                )

    for b_start, b_end, b_line in active_boxes:
        errors.append(f"[{name}] Unclosed box opened at line {b_line} cols ({b_start}, {b_end}).")

    # 2. Verify Classic ASCII boxes (+---+ / |...| / +---+) and split connectors
    for idx, line in enumerate(lines):
        for m in re.finditer(r"\+[-+|]{2,}\+", line):
            s_col = _idx_to_col(line, m.start())
            e_col = _idx_to_col(line, m.end() - 1)
            if idx + 1 >= len(lines):
                continue
            next_pipes = set(_col_positions(lines[idx + 1], "|"))
            if s_col in next_pipes and e_col in next_pipes:
                closed = False
                for k in range(idx + 1, len(lines)):
                    k_line = lines[k]
                    closed_here = False
                    for m2 in re.finditer(r"\+[-+|]{2,}\+", k_line):
                        cs = _idx_to_col(k_line, m2.start())
                        ce = _idx_to_col(k_line, m2.end() - 1)
                        if cs <= s_col and ce >= e_col and (cs == s_col or ce == e_col):
                            closed_here = True
                            break
                    if closed_here:
                        closed = True
                        total_boxes_verified += 1
                        break
                    k_arrows = set(_col_positions(k_line, "v▼"))
                    if s_col in k_arrows and e_col in k_arrows:
                        closed = True
                        total_boxes_verified += 1
                        break
                    k_pipes = set(_col_positions(k_line, "|+"))
                    if s_col not in k_pipes or e_col not in k_pipes:
                        errors.append(
                            f"[{name}] Line {k+1}: Open ASCII box from line {idx+1} cols ({s_col}, {e_col}) expects '|' at cols ({s_col}, {e_col}), found pipes at {sorted(k_pipes)}."
                        )
                        closed = True
                        break
                if not closed:
                    errors.append(f"[{name}] Unclosed ASCII box opened at line {idx+1} cols ({s_col}, {b_end if 'b_end' in locals() else e_col}).")

    # 3. Also accept structured tree / flowchart / banner diagrams that use explicit connectors
    if total_boxes_verified == 0:
        has_flow_or_tree = any(
            tok in text
            for tok in ("──►", "──>", "-->", "==>", "├──", "└──", "|--", "+--", "═══", "===", "───", "---")
        )
        if not has_flow_or_tree:
            errors.append(f"[{name}] No rectangular boxes (┌..┐ / +..+) or structured flow connectors found for kind='boxes'.")

    return errors


def verify_pyramid_diagram(text: str, name: str = "pyramid") -> List[str]:
    """
    Strict mathematical geometry verifier for a pyramid latency table diagram:
    1. Finds apex `▲` at (apex_line, apex_col).
    2. Every subsequent row `step = 1, 2, ...` down to base `└─...─┘` must place:
       - Left slope `/` (or `└` on base row) at exact display column `apex_col - step`.
       - Right slope `\\` (or `┘` on base row) at exact display column `apex_col + step`.
    3. Every row from apex_line to base_line must place the table divider `│` or `┼`
       at the exact same column `divider_col`.
    4. Every callout arrow `◄──` must start at the exact same display column `callout_col`.
    """
    errors: List[str] = []
    lines = text.splitlines()
    apex_line: Optional[int] = None
    apex_col: Optional[int] = None

    for idx, line in enumerate(lines, 1):
        cols = _col_positions(line, "▲")
        if len(cols) == 1:
            apex_line = idx
            apex_col = cols[0]
            break

    if apex_line is None or apex_col is None:
        return [f"[{name}] Pyramid apex '▲' not found."]

    divider_cols: List[Tuple[int, int]] = []
    callout_cols: List[Tuple[int, int]] = []
    base_found = False

    for idx in range(apex_line, len(lines) + 1):
        line = lines[idx - 1]
        step = idx - apex_line

        # Check table divider column (first │ or ┼ before pyramid left edge)
        expected_left = apex_col - step
        expected_right = apex_col + step
        div_candidates = [c for c in _col_positions(line, "│┼") if c < expected_left]
        if not div_candidates:
            errors.append(f"[{name}] Line {idx}: Missing table divider '│' or '┼' before pyramid.")
        else:
            divider_cols.append((idx, div_candidates[0]))

        if step == 0:
            continue

        # Check if base row
        if "└" in line or "┘" in line:
            l_cols = _col_positions(line, "└")
            r_cols = _col_positions(line, "┘")
            if l_cols != [expected_left] or r_cols != [expected_right]:
                errors.append(
                    f"[{name}] Line {idx} (base): Expected (└, ┘) at cols ({expected_left}, {expected_right}), "
                    f"got ({l_cols}, {r_cols})."
                )
            base_found = True
        else:
            # Must have '/' at expected_left and '\' at expected_right
            slash_cols = _col_positions(line, "/")
            bslash_cols = _col_positions(line, "\\")
            if expected_left not in slash_cols:
                errors.append(
                    f"[{name}] Line {idx} (step={step}): Expected left slope '/' at col {expected_left}, "
                    f"found '/' at {slash_cols}."
                )
            if expected_right not in bslash_cols:
                errors.append(
                    f"[{name}] Line {idx} (step={step}): Expected right slope '\\\\' at col {expected_right}, "
                    f"found '\\\\' at {bslash_cols}."
                )

        if "◄" in line:
            c_cols = _col_positions(line, "◄")
            callout_cols.append((idx, c_cols[0]))

    if not base_found:
        errors.append(f"[{name}] Pyramid base '└─...─┘' not found.")

    if divider_cols:
        ref_div = divider_cols[0][1]
        for l_idx, d_col in divider_cols:
            if d_col != ref_div:
                errors.append(
                    f"[{name}] Line {l_idx}: Table divider at col {d_col} != expected col {ref_div}."
                )

    if callout_cols:
        ref_call = callout_cols[0][1]
        for l_idx, c_col in callout_cols:
            if c_col != ref_call:
                errors.append(
                    f"[{name}] Line {l_idx}: Callout '◄──' at col {c_col} != expected col {ref_call}."
                )

    return errors


def verify_diagram(text: str, name: str = "diagram", kind: str = "boxes") -> List[str]:
    errors = verify_character_policy(text, name)
    if kind == "boxes":
        errors.extend(verify_box_diagram(text, name))
    elif kind == "pyramid":
        errors.extend(verify_pyramid_diagram(text, name))
    else:
        errors.append(f"[{name}] Unsupported diagram kind '{kind}'. Must be 'boxes' or 'pyramid'.")
    return errors


def run_self_tests() -> None:
    """
    Negative regression suite: proves that all 6 historical & structural failure modes
    are caught deterministically by the builder and verifier.
    """
    # 1. pad_center overflow ("L1" into width 1) must raise ValueError
    try:
        pad_center("L1", 1)
        raise AssertionError("Self-test 1 failed: pad_center('L1', 1) did not raise ValueError")
    except ValueError:
        pass

    # 2. Pyramid with right-edge vertical step (historical bug on L1/CPU) must fail verify_pyramid_diagram
    broken_pyramid = "\n".join([
        "   │      ▲",
        "   │     /L1\\",
        "   │    /CPU\\",
        "   │   └─────┘",
    ])
    errs = verify_diagram(broken_pyramid, "broken-pyr", kind="pyramid")
    if not any("Expected right slope" in e for e in errs):
        raise AssertionError(f"Self-test 2 failed: broken pyramid slope not caught: {errs}")

    # 3. Tab character in label must fail
    try:
        make_box(["Hello\tWorld"])
        raise AssertionError("Self-test 3 failed: tab character did not raise ValueError")
    except ValueError:
        pass

    # 4. Connector gap width mismatch in join_horizontal must fail
    b1 = make_box(["A"], inner_width=3)
    b2 = make_box(["B"], inner_width=3)
    try:
        join_horizontal([b1, b2], ["   "], {1: [" ──► "]})
        raise AssertionError("Self-test 4 failed: connector gap mismatch did not raise ValueError")
    except ValueError:
        pass

    # 5. Misaligned box border must fail verify_box_diagram
    broken_box = "┌────┐\n│ OK  │\n└────┘"
    errs_box = verify_diagram(broken_box, "broken-box", kind="boxes")
    if not errs_box:
        raise AssertionError("Self-test 5 failed: misaligned box border not caught")

    # 6. Unknown diagram kind must fail
    errs_kind = verify_diagram(broken_box, "unknown-kind", kind="unknown")
    if not any("Unsupported diagram kind" in e for e in errs_kind):
        raise AssertionError("Self-test 6 failed: unknown diagram kind not caught")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build & verify ASCII/Unicode diagrams")
    parser.add_argument("--self-test", action="store_true", help="Run negative regression self-tests")
    parser.add_argument("--kind", default="boxes", choices=["boxes", "pyramid"], help="Diagram geometry kind")
    parser.add_argument("files", nargs="*", help="Files to verify (or stdin)")
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        print("PASS: All 6 negative regression self-tests caught expected errors.")
        sys.exit(0)

    all_errors: List[str] = []
    if not args.files:
        data = sys.stdin.read()
        all_errors.extend(verify_diagram(data, "stdin", kind=args.kind))
    else:
        for fpath in args.files:
            with open(fpath, "r", encoding="utf-8") as f:
                all_errors.extend(verify_diagram(f.read(), fpath, kind=args.kind))

    if all_errors:
        for err in all_errors:
            print("ERROR:", err, file=sys.stderr)
        sys.exit(1)
    print(f"PASS: All ASCII/Unicode diagrams passed NFC, character policy, and '{args.kind}' geometry verification.")
