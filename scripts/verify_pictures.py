#!/usr/bin/env python3
"""
Automated Picture QA & Multimodal OCR Verifier for FSDS Learning Hub (scripts/verify_pictures.py):
Enforces 4 strict quality gates on every visual asset (comparable to scripts/ascii_diagram.py for ASCII):
1. Gate 1 (1-to-1 Uniqueness & SHA-256 Content Hash):
   - Every visual block in content/lessons-data.json must map to a unique file AND a unique SHA-256 byte hash
     (prevents copying the same image file under two different names).
2. Gate 2 (Widescreen Geometry & Anti-ASCII-Clone Policy):
   - Every .jpg must be widescreen (~16:9, width >= 1200px).
   - Every .svg must be a genuine visual infographic (1600x900) and is FORBIDDEN from dumping raw ASCII
     box-drawing characters (┌ ┐ └ ┘ ═ ║) or truncated text matrices.
3. Gate 3 (macOS Vision OCR Audit — Border Clipping, Meta-Prompt Leaks, Duplicate Headers & Typos):
   - Runs Apple Vision Framework (VNRecognizeTextRequest) across all .jpg assets in a single fast batch.
   - Rejects any image with text clipped at canvas borders.
   - Rejects any image that leaks prompt meta-instructions ("LEFT PANEL", "RIGHT CARD", "Neon Theme",
     "Alert Box", "ENGINEERING TITLE", "TOP TIER", etc.).
   - Rejects any image that duplicates long section headers at both top and bottom.
   - Rejects any image containing AI spelling hallucinations or broken syntax (e.g., 4 stars "* * * *" on a 5-star Crontab diagram).
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SWIFT_OCR_SCRIPT = r"""
import Foundation
import Vision
import AppKit

struct TextBox: Codable {
    let text: String
    let confidence: Float
    let minX: Double
    let minY: Double
    let maxX: Double
    let maxY: Double
}

struct ImageReport: Codable {
    let path: String
    let width: Int
    let height: Int
    let boxes: [TextBox]
}

let paths = Array(CommandLine.arguments.dropFirst())
var reports: [ImageReport] = []

for path in paths {
    let url = URL(fileURLWithPath: path)
    guard let img = NSImage(contentsOf: url),
          let cgImg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        continue
    }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    let handler = VNImageRequestHandler(cgImage: cgImg, options: [:])
    try? handler.perform([req])
    var boxes: [TextBox] = []
    for obs in req.results ?? [] {
        if let top = obs.topCandidates(1).first {
            let b = obs.boundingBox
            boxes.append(TextBox(
                text: top.string,
                confidence: top.confidence,
                minX: Double(b.minX),
                minY: Double(b.minY),
                maxX: Double(b.maxX),
                maxY: Double(b.maxY)
            ))
        }
    }
    reports.append(ImageReport(path: path, width: cgImg.width, height: cgImg.height, boxes: boxes))
}

let encoder = JSONEncoder()
if let data = try? encoder.encode(reports), let str = String(data: data, encoding: .utf8) {
    print(str)
}
"""

FORBIDDEN_META_PHRASES = [
    "LEFT PANEL",
    "RIGHT PANEL",
    "LEFT CARD",
    "CENTER CARD",
    "RIGHT CARD",
    "TOP TIER",
    "BOTTOM TIER",
    "ENGINEERING TITLE",
    "ENGINEERING BADGES",
    "TECHNICAL BADGES",
    "SYSTEM TELEMETRY",
    "NEON THEME",
    "ALERT BOX",
    "CORAL RED NEON",
    "EMERALD GREEN NEON",
    "CYAN NEON",
    "AMBER & SLATE",
    "VERIFIED SCHEMATIC MATRIX",
]

FORBIDDEN_TYPO_TOKENS = {
    "scrst",
    "owk",
    "refrent",
    "usrlb",
    "adnp",
    "annx",
    "roat",
    "vnin",
    "woot",
    "owrer",
    "finons",
    "tiike",
    "cliam",
    "operatus",
    "bypassng",
    "iirits",
    "sttdout",
    "corneten",
    "tiee",
    "mmory",
    "dicmension",
    "eriticat",
    "nomomeatuactualization",
    "robato",
    "stdl",
}


def run_batch_ocr(jpg_paths: list[Path]) -> dict[str, dict]:
    if not jpg_paths:
        return {}
    cmd = ["swift", "-e", SWIFT_OCR_SCRIPT] + [str(p) for p in jpg_paths]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Swift Vision OCR failed:\n{proc.stderr}")
    raw = proc.stdout.strip()
    if not raw:
        return {}
    items = json.loads(raw)
    return {item["path"]: item for item in items}


def verify_all_pictures(verbose: bool = True) -> list[str]:
    errors: list[str] = []
    data_path = ROOT / "content" / "lessons-data.json"
    if not data_path.exists():
        return ["Missing content/lessons-data.json"]

    data = json.loads(data_path.read_text(encoding="utf-8"))
    visual_assets = data.get("visual_assets", {})
    if len(visual_assets) < 85:
        errors.append(f"Expected >= 85 visual_assets, found {len(visual_assets)}")

    # 1. Check file existence, path uniqueness, and SHA-256 content uniqueness
    seen_paths: dict[str, str] = {}
    seen_hashes: dict[str, str] = {}
    jpg_files: list[Path] = []
    svg_files: list[Path] = []

    # Include top-level spine mindmap files as well
    all_checked_items = [(vid, meta.get("previewSrc", "")) for vid, meta in visual_assets.items()]
    if "assets/visuals/linux-0-map.jpg" not in [src for _, src in all_checked_items]:
        all_checked_items.append(("__spine_linux_0_map__", "assets/visuals/linux-0-map.jpg"))

    for vid, rel_src in all_checked_items:
        if not rel_src:
            errors.append(f"[{vid}] Empty previewSrc")
            continue
        abs_path = ROOT / rel_src
        if not abs_path.exists():
            errors.append(f"[{vid}] Missing file on disk: {rel_src}")
            continue
        if rel_src in seen_paths and vid != "__spine_linux_0_map__":
            errors.append(f"[{vid}] Duplicate previewSrc path '{rel_src}' (already used by {seen_paths[rel_src]})")
        seen_paths[rel_src] = vid

        file_bytes = abs_path.read_bytes()
        sha = hashlib.sha256(file_bytes).hexdigest()
        if sha in seen_hashes:
            errors.append(
                f"[{vid}] Identical SHA-256 image content between '{rel_src}' and '{seen_hashes[sha]}' (byte-for-byte clone!)"
            )
        else:
            seen_hashes[sha] = f"{vid} ({rel_src})"

        if rel_src.endswith(".jpg"):
            jpg_files.append(abs_path)
        elif rel_src.endswith(".svg"):
            svg_files.append(abs_path)

    # 2. Audit SVG files: forbid ASCII box-drawing dumps and truncated schematic matrices
    forbidden_svg_chars = set("┌┐└┘├┤┬┴┼═║╔╗╚╝╠╣╦╩╬")
    for svg_p in svg_files:
        txt = svg_p.read_text(encoding="utf-8")
        if 'viewBox="0 0 1600 900"' not in txt:
            errors.append(f"[{svg_p.name}] SVG missing standard 16:9 viewBox='0 0 1600 900'")
        if any(c in txt for c in forbidden_svg_chars) or "VERIFIED SCHEMATIC MATRIX" in txt:
            errors.append(
                f"[{svg_p.name}] SVG contains raw ASCII box-drawing dump instead of creative visual components"
            )

    # 3. Audit JPG files via macOS Vision OCR
    unique_jpgs = sorted(set(jpg_files))
    ocr_map = run_batch_ocr(unique_jpgs)

    for jpg_p in unique_jpgs:
        rep = ocr_map.get(str(jpg_p))
        if not rep:
            errors.append(f"[{jpg_p.name}] Failed to decode image for OCR")
            continue

        w, h = rep["width"], rep["height"]
        ratio = w / max(1, h)
        if w < 1200 or not (1.68 <= ratio <= 1.85):
            errors.append(f"[{jpg_p.name}] Invalid dimensions {w}x{h} (ratio {ratio:.2f}, expected 16:9 widescreen)")

        boxes = rep.get("boxes", [])
        full_text_upper = " | ".join(b["text"].upper() for b in boxes)

        # 3A. Forbidden Meta-Prompt phrases printed onto image
        for meta_phrase in FORBIDDEN_META_PHRASES:
            if meta_phrase in full_text_upper:
                errors.append(f"[{jpg_p.name}] Leaked meta-prompt label in image: {meta_phrase!r}")

        # 3B. Check for known AI typo tokens & repeated-word glitches
        for b in boxes:
            raw_line = b["text"]
            words = re.findall(r"[A-Za-z]+", raw_line)
            for word in words:
                wl = word.lower()
                if wl in FORBIDDEN_TYPO_TOKENS:
                    errors.append(f"[{jpg_p.name}] Typo / gibberish token detected via OCR: {word!r} in {raw_line!r}")
            # Detect immediate repeated words like "massive massive" or "pointer pointer"
            dup_m = re.search(r"\b([A-Za-z]{4,})\s+\1\b", raw_line, re.IGNORECASE)
            if dup_m:
                errors.append(f"[{jpg_p.name}] Repeated word glitch detected: {dup_m.group(0)!r} in {raw_line!r}")

            # 3C. Border clipping check (text touching extreme outer 0.3% edge)
            if len(raw_line.strip()) >= 4 and b["confidence"] >= 0.5:
                if b["minX"] < 0.003 or b["maxX"] > 0.997 or b["minY"] < 0.003 or b["maxY"] > 0.997:
                    errors.append(
                        f"[{jpg_p.name}] Text clipped at canvas edge ({b['minX']:.3f}, {b['minY']:.3f}, {b['maxX']:.3f}, {b['maxY']:.3f}): {raw_line!r}"
                    )

        # 3D. Duplicate multi-word section headers at top & bottom of the same image
        norm_headers: dict[str, list[float]] = {}
        for b in boxes:
            cleaned = re.sub(r"\s+", " ", b["text"].strip().upper())
            if len(cleaned) >= 18 and any(ch.isalpha() for ch in cleaned):
                norm_headers.setdefault(cleaned, []).append(b["minY"])
        for hdr, ys in norm_headers.items():
            if len(ys) >= 2 and (max(ys) - min(ys)) > 0.22:
                errors.append(f"[{jpg_p.name}] Duplicate header rendered at top and bottom of image: {hdr!r}")

        # 3E. Specific domain invariant checks
        if jpg_p.name in ("linux-4-3a.jpg", "linux-4-4a.jpg"):
            if "(* * * *)" in full_text_upper or "(* * * * )" in full_text_upper:
                errors.append(f"[{jpg_p.name}] Crontab 5-star title rendered with only 4 stars '(* * * *)'")

    if verbose:
        if errors:
            print(f"FAIL: verify_pictures.py found {len(errors)} visual quality issue(s):")
            for e in errors:
                print("  -", e)
        else:
            print(
                f"PASS: verify_pictures.py verified {len(unique_jpgs)} Style #2 JPGs (OCR + Geometry + Uniqueness) "
                f"and {len(svg_files)} bespoke SVGs with 0 errors."
            )
    return errors


if __name__ == "__main__":
    errs = verify_all_pictures(verbose=True)
    if errs:
        sys.exit(1)
