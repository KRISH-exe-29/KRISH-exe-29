"""Turns a profile photo into ASCII portraits: one for light backgrounds, one (inverted) for dark.

Needs Pillow (pip install pillow). Run:  python scripts/portrait.py <photo>  then  python scripts/gen_ascii.py
The background cut is tuned for a photo against green foliage or bright sky; HEAD is the face box.
"""
import colorsys, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

COLS, GAMMA = 120, 1.5
CHAR_W, LINE_H = 6.6, 12.0  # glyph aspect the rows are sized for
HEAD = (60, 20, 170, 165)   # face box in the 230px working image; gets its own contrast stretch
RAMP = "@%#*+=-:. "         # dark → light
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "ascii")

im = Image.open(sys.argv[1]).convert("RGB").resize((230, 230), Image.LANCZOS)
W, H = im.size

# 1. mask: drop green-dominant (foliage) and bright low-saturation (sky) pixels
mask = Image.new("L", (W, H))
px, m = im.load(), mask.load()
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        _, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        m[x, y] = 0 if (g > r + 6 and g >= b - 4) or (v > .72 and s < .22) else 255
mask = mask.filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
ImageDraw.floodfill(mask, (W // 2, H - 2), 128)          # keep the blob touching the bottom-centre (the body)
mask = mask.point(lambda v: 255 if v == 128 else 0)
ImageDraw.floodfill(mask, (0, 0), 64)                    # fill holes inside the body
mask = mask.point(lambda v: 0 if v == 64 else 255).filter(ImageFilter.MedianFilter(7))

# 2. tone: equalise inside the mask, then the head on its own, sharpen, darken midtones
gray = im.convert("L")
g = ImageOps.equalize(gray, mask=mask)
g.paste(ImageOps.equalize(gray.crop(HEAD), mask=mask.crop(HEAD)), HEAD[:2], mask.crop(HEAD))
g = g.filter(ImageFilter.UnsharpMask(3, 220, 1)).point(lambda v: int(255 * (v / 255) ** GAMMA))

# 3. characters; light text on a dark page needs the ramp reversed, or the portrait prints as a negative
rows = round(COLS * H / W * CHAR_W / LINE_H)
g, mask = g.resize((COLS, rows), Image.LANCZOS), mask.resize((COLS, rows), Image.LANCZOS)
os.makedirs(OUT, exist_ok=True)
for theme, ramp in (("light", RAMP), ("dark", RAMP[-2::-1] + " ")):
    lines = ["".join(" " if mask.getpixel((x, y)) < 110 else ramp[min(len(ramp) - 2, g.getpixel((x, y)) * (len(ramp) - 1) // 255)]
                     for x in range(COLS)).rstrip() for y in range(rows)]
    while lines and not lines[0].strip():
        lines.pop(0)
    path = os.path.join(OUT, f"portrait-{theme}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"wrote {len(lines)} lines to {path}")
