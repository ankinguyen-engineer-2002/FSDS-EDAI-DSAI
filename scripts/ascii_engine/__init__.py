"""
Headless Monodraw + Durdraw ASCII Color & Animation Engine for FSDS Academy.
"""
from .animation import FLAGSHIP_ANIMATED_DIAGRAMS, is_flagship_animated
from .dur_loader import export_dur_json, load_dur_overlay
from .painter import (
    add_monodraw_shadow,
    classify_line_roles,
    paint_ascii_html,
    strip_html_tags_unescape,
)

__all__ = [
    "FLAGSHIP_ANIMATED_DIAGRAMS",
    "is_flagship_animated",
    "export_dur_json",
    "load_dur_overlay",
    "add_monodraw_shadow",
    "classify_line_roles",
    "paint_ascii_html",
    "strip_html_tags_unescape",
]
