#!/usr/bin/env python3
"""
Durdraw (.dur JSON & .ans ANSI) Loader & Exporter for the Headless Monodraw+Durdraw Engine.
Maps Durdraw 16/256-color indices to the 8 semantic CDS roles:
  border, shadow, header, flow, ok, warn, danger, muted
"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

VALID_ROLES = {"border", "shadow", "header", "flow", "ok", "warn", "danger", "muted"}

# Standard Durdraw ANSI 16/256 foreground color code -> semantic role mapping
ANSI_FG_TO_ROLE: Dict[int, str] = {
    6: "border",    # Cyan
    14: "flow",     # Bright Cyan
    38: "border",   # 256-color Sky Cyan
    45: "flow",     # 256-color Electric Cyan
    8: "shadow",    # Dark Gray
    240: "shadow",  # 256-color Slate Shadow
    3: "header",    # Yellow/Amber
    11: "header",   # Bright Yellow/Amber
    214: "header",  # 256-color Warm Amber
    2: "ok",        # Green
    10: "ok",       # Bright Green
    42: "ok",       # 256-color Emerald
    208: "warn",    # 256-color Orange
    1: "danger",    # Red
    9: "danger",    # Bright Red
    196: "danger",  # 256-color Coral/Crimson
    7: "muted",     # Light Gray
    245: "muted",   # 256-color Muted Gray
}

ROLE_TO_ANSI_FG: Dict[str, int] = {
    "border": 38,
    "shadow": 240,
    "header": 214,
    "flow": 45,
    "ok": 42,
    "warn": 208,
    "danger": 196,
    "muted": 245,
}


def load_dur_overlay(dur_path: Path) -> Dict[Tuple[int, int], str]:
    """
    Read a Durdraw `.dur` JSON file and extract a non-destructive `(row, col) -> role` color map
    from the first frame's `colorMap` (or explicit `roleMap`).
    """
    if not dur_path.exists():
        return {}
    raw = json.loads(dur_path.read_text(encoding="utf-8"))
    overlay: Dict[Tuple[int, int], str] = {}

    # Support explicit roleMap format: {"roleMap": {"r,c": "border", ...}}
    if "roleMap" in raw and isinstance(raw["roleMap"], dict):
        for k, role in raw["roleMap"].items():
            if role in VALID_ROLES and "," in k:
                r_s, c_s = k.split(",", 1)
                overlay[(int(r_s), int(c_s))] = role

    # Support standard Durdraw Movie JSON format: {"DurMovie": {"frames": [{"colorMap": [[[fg, bg], ...]]]}}
    movie = raw.get("DurMovie") or raw
    frames = movie.get("frames") or []
    if frames and isinstance(frames[0], dict):
        cmap = frames[0].get("colorMap") or []
        for r_idx, row in enumerate(cmap):
            if not isinstance(row, list):
                continue
            for c_idx, cell in enumerate(row):
                if isinstance(cell, (list, tuple)) and len(cell) >= 1:
                    fg = cell[0]
                    if isinstance(fg, int) and fg in ANSI_FG_TO_ROLE:
                        overlay[(r_idx, c_idx)] = ANSI_FG_TO_ROLE[fg]
                elif isinstance(cell, str) and cell in VALID_ROLES:
                    overlay[(r_idx, c_idx)] = cell

    return overlay


def export_dur_json(
    raw_ascii: str,
    role_grid: List[List[Optional[str]]],
    name: str = "diagram",
) -> dict:
    """
    Export a verified ASCII diagram + its semantic role grid to a Durdraw-compatible `.dur` JSON object.
    """
    lines = raw_ascii.splitlines()
    height = len(lines)
    width = max((len(l) for l in lines), default=0)
    char_map: List[List[str]] = []
    color_map: List[List[List[int]]] = []

    for r_idx, line in enumerate(lines):
        padded = line.ljust(width)
        char_map.append(list(padded))
        c_row: List[List[int]] = []
        r_roles = role_grid[r_idx] if r_idx < len(role_grid) else []
        for c_idx in range(width):
            role = r_roles[c_idx] if c_idx < len(r_roles) else None
            fg = ROLE_TO_ANSI_FG.get(role or "", 7)
            c_row.append([fg, 0])
        color_map.append(c_row)

    return {
        "DurMovie": {
            "version": 1,
            "name": name,
            "sizeX": width,
            "sizeY": height,
            "colorMode": "256",
            "encoding": "utf-8",
            "frames": [
                {
                    "delay": 0.25,
                    "charMap": char_map,
                    "colorMap": color_map,
                }
            ],
        }
    }
