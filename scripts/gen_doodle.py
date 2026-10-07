"""Hand-drawn / doodle profile: an engineering notebook by day, a chalkboard by night. Wobbly strokes that draw themselves.
Run: python scripts/gen_doodle.py"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, wrap
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short

F = "doodle"
HAND = "'Segoe Print', 'Bradley Hand', 'Chalkboard SE', 'Comic Sans MS', 'Comic Neue', cursive"
THEMES = {"light": dict(paper="#FFFDF5", grid="#CFE0F5", margin="#F2A3A3", ink="#1F2A44", red="#D62839", hl="#FFE66D", note=["#FFF3A3", "#FFD6E0", "#C9F2D9", "#CDE4FF"], chalk=0),
          "dark": dict(paper="#1F2B26", grid="#2A3832", margin="#3A4A42", ink="#EDEDE4", red="#FF8FA3", hl="#F5D76E", note=["#2C3A34", "#2C3A34", "#2C3A34", "#2C3A34"], chalk=1)}


class Pen:
    def __init__(self, seed):
        self.r = random.Random(seed)

    def line(self, x1, y1, x2, y2, j=2.5):
        """A slightly wobbly stroke, drawn twice like a real pen."""
        out = []
        for _ in range(2):
            mx, my = (x1 + x2) / 2 + self.r.uniform(-j, j) * 2, (y1 + y2) / 2 + self.r.uniform(-j, j) * 2
            out.append(f"M{x1 + self.r.uniform(-j, j):.1f},{y1 + self.r.uniform(-j, j):.1f} Q{mx:.1f},{my:.1f} {x2 + self.r.uniform(-j, j):.1f},{y2 + self.r.uniform(-j, j):.1f}")
        return " ".join(out)

    def box(self, x, y, w, h):
        return " ".join([self.line(x, y, x + w, y), self.line(x + w, y, x + w, y + h), self.line(x + w, y + h, x, y + h), self.line(x, y + h, x, y)])

    def circle(self, cx, cy, r):
        pts = [(cx + (r + self.r.uniform(-3, 3)) * math.cos(a), cy + (r + self.r.uniform(-3, 3)) * math.sin(a)) for a in [i * math.pi / 8 for i in range(18)]]
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def page(c, t, w, h):
    c.defs.append('<filter id="chalk"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="2.5"/></filter>')
    c.add(f'<rect width="{w}" height="{h}" fill="{t["paper"]}"/>')
    if not t["chalk"]:
        c.add("".join(f'<line x1="0" x2="{w}" y1="{y}" y2="{y}" stroke="{t["grid"]}"/>' for y in range(30, h, 30))
              + "".join(f'<line x1="{x}" x2="{x}" y1="0" y2="{h}" stroke="{t["grid"]}" opacity=".5"/>' for x in range(30, w, 30))
              + f'<line x1="90" x2="90" y1="0" y2="{h}" stroke="{t["margin"]}" stroke-width="2"/>')
    else:
        c.add(f'<rect x="10" y="10" width="{w - 20}" height="{h - 20}" fill="none" stroke="#5B4636" stroke-width="16"/>')


def stroke(d, col, w=3, delay=0, cls="draw"):
    return f'<path class="{cls}" style="animation-delay:{delay:.1f}s" d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


DRAW = ".draw{stroke-dasharray:1400;animation:dw 2.6s ease-out both}@keyframes dw{from{stroke-dashoffset:1400}}"

for th, t in THEMES.items():
    pen = Pen(11)
    ink = t["ink"]
    flt = ' filter="url(#chalk)"' if t["chalk"] else ""
    c = Canvas(F, t, 1200, 800)
    page(c, t, 1200, 800)
    c.add(f"<g{flt}>")
    c.add(f'<rect x="120" y="64" width="560" height="44" fill="{t["hl"]}" opacity="{.6 if not t["chalk"] else .25}" transform="rotate(-1 400 86)"/>')
    c.text(130, 100, NAME, 52, ink, HAND, 700)
    c.add(stroke(pen.line(130, 118, 660, 112) + " " + pen.line(140, 126, 600, 124), t["red"], 3))
    c.text(130, 170, "electrical engineer (who codes too)", 26, ink, HAND)
    c.add(stroke(pen.line(640, 160, 720, 140), t["red"], 3, .5), stroke(pen.line(720, 140, 706, 152) + " " + pen.line(720, 140, 704, 136), t["red"], 3, .6))
    c.text(730, 146, "that's me!", 22, t["red"], HAND, 700)
    # the flow: transformer → laptop → truck
    tx, ty = 160, 300
    c.add(stroke(pen.box(tx, ty, 120, 130), ink, 3, .8))
    for i in range(3):
        c.add(stroke(pen.line(tx + 20 + i * 40, ty, tx + 20 + i * 40, ty - 40), ink, 3, 1 + i * .1), stroke(pen.circle(tx + 20 + i * 40, ty - 46, 7), ink, 2.5, 1.2))
    for i in range(4):
        c.add(stroke(pen.line(tx + 132 + i * 10, ty + 20, tx + 132 + i * 10, ty + 110), ink, 2.5, 1.3))
    c.add(stroke(f"M{tx + 70},{ty + 30} L{tx + 50},{ty + 70} L{tx + 72},{ty + 70} L{tx + 56},{ty + 110}", t["hl"] if t["chalk"] else t["red"], 4, 1.4))
    c.text(tx + 20, ty + 170, "test it", 24, ink, HAND, 700)
    c.add(stroke(pen.line(330, 360, 450, 360) + " " + pen.line(450, 360, 432, 348) + " " + pen.line(450, 360, 434, 374), ink, 3, 1.8))
    lx, ly = 480, 300
    c.add(stroke(pen.box(lx, ly, 170, 110), ink, 3, 2), stroke(pen.line(lx - 20, ly + 125, lx + 190, ly + 125), ink, 3, 2.2))
    for i, wdt in enumerate([110, 70, 130, 90]):
        c.add(stroke(pen.line(lx + 16, ly + 22 + i * 22, lx + 16 + wdt, ly + 22 + i * 22), t["red"] if i == 1 else ink, 2.5, 2.3 + i * .1))
    c.text(lx + 10, ty + 170, "automate it", 24, ink, HAND, 700)
    c.add(stroke(pen.line(690, 360, 810, 360) + " " + pen.line(810, 360, 792, 348) + " " + pen.line(810, 360, 794, 374), ink, 3, 2.7))
    kx, ky = 840, 320
    c.add(stroke(pen.box(kx, ky, 150, 80) + " " + pen.box(kx + 150, ky + 26, 60, 54), ink, 3, 3), stroke(pen.circle(kx + 36, ky + 92, 14) + " " + pen.circle(kx + 170, ky + 92, 14), ink, 3, 3.2))
    c.text(kx + 10, ty + 170, "ship it!", 24, ink, HAND, 700)
    # notes and numbers
    c.add(stroke(pen.circle(220, 610, 62), t["red"], 3, 3.4))
    c.text(220, 625, "9", 52, ink, HAND, 700, "middle")
    c.text(150, 710, "apps in production", 22, ink, HAND)
    c.text(400, 590, "30 min", 40, ink, HAND, 700)
    c.add(stroke(pen.line(395, 578, 530, 578), t["red"], 4, 3.6))
    c.text(400, 650, "→ 30 seconds (!!!)", 36, t["red"], HAND, 700)
    c.text(400, 700, "at Bühler. still proud.", 20, ink, HAND)
    c.text(780, 590, "• 128 tests on dispatch", 24, ink, HAND)
    c.text(780, 630, "• patent filed (street lights", 24, ink, HAND)
    c.text(800, 662, "that follow cars, yes really)", 24, ink, HAND)
    c.text(780, 702, "• NEC #7 of 1500+ colleges", 24, ink, HAND)
    if not t["chalk"]:
        c.add(f'<circle cx="1080" cy="150" r="60" fill="none" stroke="#B5835A" stroke-width="6" opacity=".35"/><circle cx="1086" cy="156" r="54" fill="none" stroke="#B5835A" stroke-width="2" opacity=".25"/>')
        c.text(1080, 240, "(chai stain)", 16, "#B5835A", HAND, anchor="middle")
    else:
        c.text(1080, 150, "☕", 54, ink, HAND, anchor="middle")
    c.add("</g>")
    c.css.append(DRAW)
    c.save(f"notebook-{th}.svg", f"Notebook page: {NAME}, electrical engineer who codes too. Test it, automate it, ship it. 9 apps in production; 30 minutes became 30 seconds; 128 tests; patent filed; NEC rank 7.")

    # sticky notes of projects
    c = Canvas(F, t, 1200, 720)
    page(c, t, 1200, 720)
    c.add(f"<g{flt}>")
    c.text(130, 80, "things I built (& still maintain):", 36, ink, HAND, 700)
    c.add(stroke(pen.line(130, 96, 700, 92), t["red"], 3))
    rnd = random.Random(4)
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        x, y = 120 + (i % 5) * 210, 130 + (i // 5) * 290
        rot = rnd.uniform(-5, 5)
        c.add(f'<g transform="rotate({rot:.1f} {x + 90} {y + 120})"><rect x="{x}" y="{y}" width="185" height="240" fill="{t["note"][i % 4]}" '
              f'{"" if t["chalk"] else "style=" + chr(34) + "filter:drop-shadow(2px 4px 3px rgba(0,0,0,.18))" + chr(34)}/>')
        if t["chalk"]:
            c.add(stroke(pen.box(x, y, 185, 240), ink, 2, 0, "x"))
        c.add(f'<rect x="{x + 60}" y="{y - 12}" width="64" height="22" fill="{t["hl"]}" opacity=".55"/>')
        c.text(x + 14, y + 44, short(name), 22 if len(short(name)) < 13 else 18, ink, HAND, 700)
        for j, l in enumerate(wrap(hook, 16, 160, .5)[:4]):
            c.text(x + 14, y + 82 + j * 24, l, 16, ink, HAND)
        c.text(x + 14, y + 216, ("✓ " if status in ("PRODUCTION", "LIVE", "IN USE") else "~ ") + status.lower(), 16, t["red"], HAND, 700)
        c.add("</g>")
    c.text(130, 700, f"p.s. email me → {EMAIL}", 24, t["red"], HAND, 700)
    c.add("</g>")
    c.save(f"notes-{th}.svg", "Sticky notes of things I built: " + "; ".join(f"{p[1]}, {p[4]}" for p in PROJECTS))

links = " · ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Hand-drawn: an engineering notebook in light mode, a chalkboard in dark mode. Built by scripts/gen_doodle.py -->

<p align="center">{pic(F, "notebook", f"Notebook page for {NAME}: test it, automate it, ship it")}</p>
<p align="center">{pic(F, "notes", "Sticky notes of things I built")}</p>
<p align="center">✏️ {links}</p>
<p align="center"><sub><a href="mailto:{EMAIL}">email</a> · <a href="{LINKEDIN}">linkedin</a> · drawn with code, not a pen</sub></p>
""")
print("ok")
