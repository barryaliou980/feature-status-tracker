#!/usr/bin/env python3
"""Generate assets/demo.gif — animated walkthrough of the FEATURES.md table lifecycle.

Usage: python3 assets/generate-demo.py   (requires Pillow, run from repo root)
"""
from PIL import Image, ImageDraw, ImageFont

SCALE = 2  # render at 2x then downscale for crisp text
W, H = 780, 235
FONT_SIZE = 13

BG = "#11111b"
PANEL = "#1e1e2e"
BORDER = "#45475a"
TEXT = "#cdd6f4"
DIM = "#7f849c"
ACCENT = "#cba6f7"

STATUS_COLORS = {
    "todo": "#f9e2af",
    "clarified": "#89b4fa",
    "in progress": "#fab387",
    "done": "#a6e3a1",
}

FEATURES = ["Multi-account OAuth ", "Dashboard PDF export"]

def load_font(size):
    for path in ("/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Monaco.ttf"):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()

FONT = load_font(FONT_SIZE * SCALE)
FONT_BOLD = load_font(FONT_SIZE * SCALE)

def row_line(feature, status, branch, pr):
    return f"| {feature} | {status:<11} | {branch:<29} | {pr:<3} |"

HEADER = f"| {'Feature':<20} | {'Status':<11} | {'Branch':<29} | {'PR':<3} |"
SEP = f"|{'-'*22}|{'-'*13}|{'-'*31}|{'-'*5}|"

def make_frame(rows, claude_line, claude_color=ACCENT):
    img = Image.new("RGB", (W * SCALE, H * SCALE), BG)
    d = ImageDraw.Draw(img)
    pad = 20 * SCALE

    # window chrome
    d.rounded_rectangle([pad // 2, pad // 2, W * SCALE - pad // 2, H * SCALE - pad // 2],
                        radius=10 * SCALE, fill=PANEL, outline=BORDER, width=SCALE)
    for i, c in enumerate(("#f38ba8", "#f9e2af", "#a6e3a1")):
        d.ellipse([pad + i * 22 * SCALE, pad, pad + i * 22 * SCALE + 12 * SCALE, pad + 12 * SCALE], fill=c)
    d.text((W * SCALE // 2 - 40 * SCALE, pad - 2 * SCALE), "FEATURES.md", font=FONT, fill=DIM)

    y = pad + 34 * SCALE
    line_h = int(FONT_SIZE * SCALE * 1.75)

    def put(text, color=TEXT, x=pad):
        nonlocal y
        d.text((x, y), text, font=FONT, fill=color)
        y += line_h

    put(HEADER, DIM)
    put(SEP, BORDER)
    for feature, status, branch, pr in rows:
        line = row_line(feature, status, branch, pr)
        put(line)
        # overdraw the status word in its color
        prefix = f"| {feature} | "
        x_status = pad + d.textlength(prefix, font=FONT)
        d.text((x_status, y - line_h), status, font=FONT, fill=STATUS_COLORS[status])

    y += line_h // 2
    d.line([pad, y, W * SCALE - pad, y], fill=BORDER, width=SCALE)
    y += line_h // 2
    put(claude_line, claude_color)
    return img.resize((W, H), Image.LANCZOS)

frames = [
    make_frame(
        [(FEATURES[0], "todo", "", ""), (FEATURES[1], "todo", "", "")],
        "❯ Phase 1 — clarifying 1/2: Multi-account OAuth (scope? edge cases? done when?)",
    ),
    make_frame(
        [(FEATURES[0], "clarified", "", ""), (FEATURES[1], "clarified", "", "")],
        "✔ All features clarified — waiting for your explicit GO before any code",
        "#89b4fa",
    ),
    make_frame(
        [(FEATURES[0], "in progress", "feature/multi-account-oauth", ""), (FEATURES[1], "clarified", "", "")],
        "⚙ Phase 3 — branch created · TDD red-green-refactor · self code review",
        "#fab387",
    ),
    make_frame(
        [(FEATURES[0], "done", "feature/multi-account-oauth", "#42"), (FEATURES[1], "in progress", "feature/dashboard-pdf-export", "")],
        "⚙ PR #42 opened (never auto-merged) → moving to next feature on its own",
        "#fab387",
    ),
    make_frame(
        [(FEATURES[0], "done", "feature/multi-account-oauth", "#42"), (FEATURES[1], "done", "feature/dashboard-pdf-export", "#43")],
        "✔ Final report: 2/2 done · 2 PRs open, awaiting your review · 0 blocked",
        "#a6e3a1",
    ),
]

frames[0].save(
    "assets/demo.gif",
    save_all=True,
    append_images=frames[1:],
    duration=[2200, 2200, 2200, 2400, 4000],
    loop=0,
)
print("wrote assets/demo.gif")
