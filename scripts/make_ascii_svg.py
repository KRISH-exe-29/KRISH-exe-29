"""
Turn assets/terminal/portrait.jpg into a monochrome ASCII portrait SVG that
"types" itself in row by row like a terminal, then holds. One-off; rerun only
when the photo changes:

    python scripts/make_ascii_svg.py

The photo's green foliage is keyed out to blank so only the subject prints.
Canvas is 840x880, same as stats.svg, so the two sit side by side evenly.
"""
import html
import os

from PIL import Image, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "assets", "terminal", "portrait.jpg")
OUT = os.path.join(HERE, "..", "assets", "terminal", "ascii.svg")

COLS, ROWS = 180, 96                  # ~1:1.875 char cells -> square art
CELL_W, CELL_H = 800 / COLS, 800 / ROWS
RAMP = " .`:-=+*cs#%@"                # bright(sparse) -> dark(dense)
GAMMA, WHITE_FLOOR = 1.18, 0.80
GREEN_KEY = 12                        # g must beat r and b by this to count as foliage; tune per photo
PAD, TITLEBAR_H = 20, 30
BG, BG2, FRAME, MUTED, INK = "#0d1117", "#111722", "#30363d", "#7d8590", "#c9d1d9"
ROW_DUR = 5.8 / ROWS                  # whole portrait prints in ~6s

im = Image.open(SRC).convert("RGB")
im = im.crop((112, 40, 912, 840))     # square on head + shoulders of the 1024x1536 photo
im = im.resize((COLS, ROWS), Image.LANCZOS)
gray = ImageEnhance.Contrast(im.convert("L")).enhance(1.15)
rgb, px = im.load(), gray.load()

rows = []
for y in range(ROWS):
    line = ""
    for x in range(COLS):
        r, g, b = rgb[x, y]
        lum = (px[x, y] / 255) ** GAMMA
        if (g > r + GREEN_KEY and g > b + GREEN_KEY) or lum >= WHITE_FLOOR:
            line += " "
        else:
            line += RAMP[min(len(RAMP) - 1, int((1 - lum) * (len(RAMP) - 1) + 0.5))]
    rows.append(line)

W, H = 840, 880
art_top = TITLEBAR_H + 7
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG2}"/>'
    f'<stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="15" r="5" fill="{dot}"/>')
parts.append(f'<text x="{W/2}" y="19" fill="{MUTED}" font-size="12" text-anchor="middle">krish@github: ~$ ./portrait.sh</text>')

for ry, line in enumerate(rows):
    row_y = art_top + ry * CELL_H
    d = ry * ROW_DUR
    parts.append(
        f'<clipPath id="r{ry}"><rect x="{PAD}" y="{row_y:.1f}" height="{CELL_H:.2f}" width="0">'
        f'<animate attributeName="width" from="0" to="800" begin="{d:.3f}s" dur="{ROW_DUR:.3f}s" fill="freeze"/></rect></clipPath>'
        f'<g clip-path="url(#r{ry})"><text xml:space="preserve" x="{PAD}" y="{row_y + CELL_H*0.74:.1f}" fill="{INK}" '
        f'font-size="{CELL_H*0.86:.1f}" textLength="800" lengthAdjust="spacing">{html.escape(line)}</text></g>'
        f'<rect y="{row_y+1:.1f}" width="{CELL_W:.2f}" height="{CELL_H-2:.2f}" fill="{INK}" opacity="0">'
        f'<animate attributeName="x" from="{PAD}" to="{PAD+800}" begin="{d:.3f}s" dur="{ROW_DUR:.3f}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.85" begin="{d:.3f}s"/><set attributeName="opacity" to="0" begin="{d+ROW_DUR:.3f}s"/></rect>'
    )

sl = art_top + ROWS * CELL_H + 7
parts.append(f'<line x1="0" y1="{sl:.1f}" x2="{W}" y2="{sl:.1f}" stroke="{FRAME}"/>')
parts.append(f'<text x="{PAD}" y="{sl+19:.1f}" fill="{MUTED}" font-size="13">krish@github:~$ whoami '
             f'<tspan fill="{INK}">Krishna Raju S</tspan></text>')
cx = PAD + len("krish@github:~$ whoami Krishna Raju S ") * 13 * 0.6
parts.append(f'<rect x="{cx:.1f}" y="{sl+7:.1f}" width="8" height="14" fill="{INK}">'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/></rect>')
parts.append("</svg>")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("".join(parts))
print("wrote", OUT)
