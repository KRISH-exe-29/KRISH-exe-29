"""Turns a profile photo into a pixel-art grid for the arcade player card.

Needs Pillow (pip install pillow). Run:  python scripts/pixels.py <photo>  then  python scripts/gen_retro.py
Writes assets/retro/pixels.txt: one row per line, a digit 0-9 per pixel (brightness), '.' outside the person.
The background cut is tuned for a photo against green foliage or bright sky; HEAD is the face box.
"""
import colorsys, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

COLS = 34
HEAD = (60, 20, 170, 165)  # face box in the 230px working image; gets its own contrast stretch
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "retro", "pixels.txt")

im = Image.open(sys.argv[1]).convert("RGB").resize((230, 230), Image.LANCZOS)
W, H = im.size
mask = Image.new("L", (W, H))
px, m = im.load(), mask.load()
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        _, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        m[x, y] = 0 if (g > r + 6 and g >= b - 4) or (v > .72 and s < .22) else 255
mask = mask.filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
ImageDraw.floodfill(mask, (W // 2, H - 2), 128)
mask = mask.point(lambda v: 255 if v == 128 else 0)
ImageDraw.floodfill(mask, (0, 0), 64)
mask = mask.point(lambda v: 0 if v == 64 else 255).filter(ImageFilter.MedianFilter(7))

gray = im.convert("L")
g = ImageOps.equalize(gray, mask=mask)
g.paste(ImageOps.equalize(gray.crop(HEAD), mask=mask.crop(HEAD)), HEAD[:2], mask.crop(HEAD))
g = g.filter(ImageFilter.UnsharpMask(3, 160, 1)).point(lambda v: int(255 * (v / 255) ** 1.3))
g, mask = g.resize((COLS, COLS), Image.LANCZOS), mask.resize((COLS, COLS), Image.LANCZOS)
rows = ["".join("." if mask.getpixel((x, y)) < 110 else str(min(9, g.getpixel((x, y)) * 10 // 256))
                for x in range(COLS)) for y in range(COLS)]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(rows))
print("wrote", OUT)
