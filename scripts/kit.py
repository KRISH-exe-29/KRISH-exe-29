"""Tiny SVG toolkit shared by the profile generators: one canvas class, text helpers, light/dark output."""
import os
from xml.sax.saxutils import escape as esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REDUCE = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SERIF = "Georgia, 'Times New Roman', Times, serif"


def wrap(text, size, width, factor=.52):
    """Greedy word wrap using an average glyph width of factor * size."""
    per = max(6, int(width / (size * factor)))
    lines, line = [], ""
    for w in str(text).split():
        if line and len(line) + len(w) + 1 > per:
            lines.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    return lines + [line] if line else lines


class Canvas:
    def __init__(self, folder, t, w, h):
        self.folder, self.t, self.w, self.h, self.parts, self.defs, self.css = folder, t, w, h, [], [], []

    def add(self, *s):
        self.parts.extend(s)
        return self

    def text(self, x, y, s, size, fill=None, font=SANS, weight=400, anchor="start", extra=""):
        self.parts.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
                          f'fill="{fill or self.t.get("ink", "#111")}" text-anchor="{anchor}" {extra}>{esc(str(s))}</text>')
        return self

    def para(self, x, y, s, size, width, lh=1.45, factor=.52, **kw):
        """Wrapped text; returns the y after the last line."""
        lines = wrap(s, size, width, factor)
        for i, l in enumerate(lines):
            self.text(x, y + i * size * lh, l, size, **kw)
        return y + len(lines) * size * lh

    def save(self, name, title, bg=None, rx=0):
        os.makedirs(os.path.join(ROOT, "assets", self.folder), exist_ok=True)
        back = f'<rect width="{self.w}" height="{self.h}" rx="{rx}" fill="{bg}"/>' if bg else ""
        clip = f'<clipPath id="kitclip"><rect width="{self.w}" height="{self.h}" rx="{rx}"/></clipPath>' if rx else ""
        body = "".join(self.parts)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
               f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title><defs>{clip}{"".join(self.defs)}</defs>'
               f'<style>{"".join(self.css)}{REDUCE}</style>'
               + (f'<g clip-path="url(#kitclip)">{back}{body}</g>' if rx else back + body) + "</svg>\n")
        with open(os.path.join(ROOT, "assets", self.folder, name), "w", encoding="utf-8") as f:
            f.write(svg)


def pic(folder, name, alt, width="100%", themed=True):
    """Markdown/HTML for an image that follows the viewer's GitHub theme."""
    if not themed:
        return f'<img src="./assets/{folder}/{name}.svg" width="{width}" alt="{esc(alt)}"/>'
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/{folder}/{name}-dark.svg"/>'
            f'<img src="./assets/{folder}/{name}-light.svg" width="{width}" alt="{esc(alt)}"/></picture>')


def linked(url, html):
    return f'<a href="{url}">{html}</a>' if url else html


def write_readme(text):
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(text.strip() + "\n")


def photo_grid(folder, cols, photo=None):
    """Brightness grid of the profile photo: rows of digits 0 (dark) to 9 (light), '.' outside the person.

    Pass the photo once (needs Pillow) to build assets/<folder>/photo-<cols>.txt; later runs just read that file.
    The background cut is tuned for a photo against green foliage or bright sky.
    """
    path = os.path.join(ROOT, "assets", folder, f"photo-{cols}.txt")
    if photo and os.path.exists(photo):
        import colorsys
        from PIL import Image, ImageDraw, ImageFilter, ImageOps
        im = Image.open(photo).convert("RGB").resize((230, 230), Image.LANCZOS)
        mask = Image.new("L", im.size)
        px, m = im.load(), mask.load()
        for y in range(230):
            for x in range(230):
                r, g, b = px[x, y]
                _, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                m[x, y] = 0 if (g > r + 6 and g >= b - 4) or (v > .72 and s < .22) else 255
        mask = mask.filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
        ImageDraw.floodfill(mask, (115, 228), 128)
        mask = mask.point(lambda v: 255 if v == 128 else 0)
        ImageDraw.floodfill(mask, (0, 0), 64)
        mask = mask.point(lambda v: 0 if v == 64 else 255).filter(ImageFilter.MedianFilter(7))
        head = (60, 20, 170, 165)  # face box: gets its own contrast stretch
        gray = im.convert("L")
        g = ImageOps.equalize(gray, mask=mask)
        g.paste(ImageOps.equalize(gray.crop(head), mask=mask.crop(head)), head[:2], mask.crop(head))
        g = g.filter(ImageFilter.UnsharpMask(3, 160, 1)).point(lambda v: int(255 * (v / 255) ** 1.3))
        g, mask = g.resize((cols, cols), Image.LANCZOS), mask.resize((cols, cols), Image.LANCZOS)
        rows = ["".join("." if mask.getpixel((x, y)) < 110 else str(min(9, g.getpixel((x, y)) * 10 // 256)) for x in range(cols))
                for y in range(cols)]
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(rows))
    return open(path, encoding="utf-8").read().split("\n")


def icon(slug, x, y, s, a, b, c):
    """Flat icon for a project in a 100x100 box at (x, y), scaled by s/100. a = main, b = accent, c = detail colour."""
    k = s / 100
    shapes = {
        "dispatch": f'<rect x="6" y="34" width="56" height="36" rx="4" fill="{a}"/><path d="M62 44h18l12 14v12H62z" fill="{b}"/>'
                    f'<rect x="68" y="48" width="12" height="9" fill="{c}"/><circle cx="24" cy="74" r="9" fill="{c}"/><circle cx="76" cy="74" r="9" fill="{c}"/>',
        "job-lens": f'<rect x="14" y="10" width="46" height="60" rx="5" fill="{a}"/><rect x="22" y="22" width="30" height="5" fill="{c}"/>'
                    f'<rect x="22" y="33" width="22" height="5" fill="{c}"/><circle cx="60" cy="60" r="20" fill="none" stroke="{b}" stroke-width="9"/>'
                    f'<path d="M74 74l16 16" stroke="{b}" stroke-width="10" stroke-linecap="round"/>',
        "kiosk-sentinel": f'<rect x="10" y="12" width="80" height="54" rx="6" fill="{a}"/><rect x="40" y="66" width="20" height="14" fill="{c}"/>'
                          f'<rect x="26" y="80" width="48" height="8" rx="4" fill="{c}"/><rect x="38" y="36" width="24" height="20" rx="3" fill="{b}"/>'
                          f'<path d="M43 36v-6a7 7 0 0 1 14 0v6" fill="none" stroke="{b}" stroke-width="5"/>',
        "test-planner": f'<path d="M38 10h24v26l22 42a6 6 0 0 1-5 9H21a6 6 0 0 1-5-9l22-42z" fill="{a}"/><path d="M27 62h46l9 17H18z" fill="{b}"/>'
                        f'<rect x="34" y="6" width="32" height="8" rx="3" fill="{c}"/>',
        "hardware": f'<path d="M50 8l36 21v42L50 92 14 71V29z" fill="{a}"/><circle cx="50" cy="50" r="17" fill="{c}"/><circle cx="50" cy="50" r="9" fill="{b}"/>',
        "street-light": f'<rect x="44" y="30" width="7" height="62" fill="{c}"/><path d="M47 30q0-18 26-18h4" fill="none" stroke="{c}" stroke-width="7"/>'
                        f'<path d="M64 12h26l-5 10H69z" fill="{a}"/><path d="M66 24l-12 40h48l-12-40z" fill="{b}" opacity=".55"/>',
        "rtcc": f'<rect x="14" y="8" width="72" height="84" rx="6" fill="{a}"/><circle cx="36" cy="34" r="11" fill="{c}"/><circle cx="64" cy="34" r="11" fill="{c}"/>'
                f'<path d="M36 34l6-6M64 34l-3-8" stroke="{b}" stroke-width="3"/><rect x="26" y="58" width="48" height="8" rx="3" fill="{b}"/><rect x="26" y="72" width="30" height="8" rx="3" fill="{c}"/>',
        "industrial-data": f'<rect x="10" y="10" width="80" height="80" rx="6" fill="{a}"/>'
                           + "".join(f'<rect x="{18 + (i % 3) * 22}" y="{18 + (i // 3) * 22}" width="18" height="18" fill="{b if i in (0, 2, 6) else c}"/>' for i in range(9) if i != 4),
        "hwe-tool": "".join(f'<rect x="44" y="6" width="12" height="20" rx="3" fill="{a}" transform="rotate({r} 50 50)"/>' for r in range(0, 360, 45))
                    + f'<circle cx="50" cy="50" r="30" fill="{a}"/><circle cx="50" cy="50" r="13" fill="{c}"/><path d="M44 50h12M50 44v12" stroke="{b}" stroke-width="4"/>',
        "flood": f'<path d="M50 8c14 20 24 32 24 46a24 24 0 0 1-48 0c0-14 10-26 24-46z" fill="{a}"/>'
                 f'<path d="M6 80q11-10 22 0t22 0 22 0 22 0" fill="none" stroke="{b}" stroke-width="7"/><path d="M6 92q11-10 22 0t22 0 22 0 22 0" fill="none" stroke="{c}" stroke-width="6"/>',
    }
    return f'<g transform="translate({x} {y}) scale({k:.3f})">{shapes[slug]}</g>'
