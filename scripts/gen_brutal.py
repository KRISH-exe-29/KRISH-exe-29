"""Neo-brutalist panels for the profile README, in light and dark variants.

Run:  python scripts/gen_brutal.py   (content lives in scripts/profile_data.py)
"""
import os, sys
from xml.sax.saxutils import escape as esc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from profile_data import NAME, EMAIL, STATS, PROJECTS, MILESTONES, TOOLS

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "brutal")
os.makedirs(OUT, exist_ok=True)
HEAVY = "'Arial Black', 'Archivo Black', Impact, 'Helvetica Neue', Arial, sans-serif"
MONO = "'Courier New', ui-monospace, Menlo, Consolas, monospace"
BLACK = "#111111"
YELLOW, PINK, BLUE, GREEN, ORANGE, PURPLE = "#FFD93D", "#FF6B9D", "#4D96FF", "#6BCB77", "#FF8C42", "#B983FF"
LOUD = [YELLOW, PINK, BLUE, GREEN, ORANGE, PURPLE]
THEMES = {"light": dict(bg="#FFF8E7", ink=BLACK, grid="#11111114"),
          "dark": dict(bg="#121212", ink="#F4F1E8", grid="#F4F1E812")}
REDUCE = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


class Poster:
    def __init__(self, t, w, h):
        self.t, self.w, self.h, self.body = t, w, h, []

    def box(self, x, y, w, h, fill, shadow=8, border=4):
        ink = self.t["ink"]
        self.body.append(f'<rect x="{x + shadow}" y="{y + shadow}" width="{w}" height="{h}" fill="{ink}"/>'
                         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{ink}" stroke-width="{border}"/>')

    def text(self, x, y, s, size, fill=None, font=HEAVY, anchor="start", weight=900, extra=""):
        self.body.append(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
                         f'fill="{fill or self.t["ink"]}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')

    def sticker(self, cx, cy, label, fill, rot, size=22, cls="wob"):
        w, h = len(label) * size * .78 + 36, size * 2.3
        # rotation lives on the outer group: a CSS animation would replace a transform attribute on the same element
        self.body.append(f'<g transform="rotate({rot} {cx} {cy})"><g class="{cls}" style="transform-origin:{cx}px {cy}px">')
        self.box(cx - w / 2, cy - h / 2, w, h, fill, 6, 4)
        self.text(cx, cy + size * .36, label, size, BLACK, anchor="middle")
        self.body.append("</g></g>")

    def save(self, name, title, style=""):
        t, w, h = self.t, self.w, self.h
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
               f'aria-label="{esc(title)}"><title>{esc(title)}</title><defs>'
               f'<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{t["grid"]}" stroke-width="2"/></pattern></defs>'
               f'<style>.wob{{animation:wob 3.2s ease-in-out infinite}}@keyframes wob{{50%{{transform:rotate(4deg) scale(1.05)}}}}{style}{REDUCE}</style>'
               f'<rect width="{w}" height="{h}" fill="{t["bg"]}"/><rect width="{w}" height="{h}" fill="url(#grid)"/>'
               f'{"".join(self.body)}<rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="none" stroke="{t["ink"]}" stroke-width="4"/></svg>\n')
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(svg)


for theme, t in THEMES.items():
    ink = t["ink"]
    # ── hero poster ──
    p = Poster(t, 1200, 660)
    p.body.append(f'<rect x="0" y="0" width="1200" height="52" fill="{ink}"/>')
    p.text(28, 34, "KRISH.EXE  ■  PORTFOLIO  ■  VOL. 2026", 18, t["bg"], MONO, weight=700)
    p.text(1172, 34, "NO TEMPLATES WERE HARMED", 18, t["bg"], MONO, "end", 700)
    p.box(40, 92, 640, 54, YELLOW, 6)
    p.text(58, 131, f"{NAME.upper()}  //  EEE ENGINEER", 26, BLACK)
    p.text(36, 262, "I AUTOMATE.", 102, extra='letter-spacing="-4"')
    p.text(36, 380, "YOU GO HOME", 102, extra='letter-spacing="-4"')
    p.box(40, 424, 520, 138, PINK, 10)
    p.text(58, 528, "EARLY.", 118, BLACK, extra='letter-spacing="-4"')
    p.text(600, 470, "Electrical engineer at Indo Tech Transformers.", 20, font=MONO, weight=700)
    p.text(600, 500, "I write the software the shop floor runs on:", 20, font=MONO, weight=700)
    p.text(600, 530, "dispatch, testing, hiring, attendance.", 20, font=MONO, weight=700)
    p.text(600, 572, "Your spreadsheet's worst nightmare.", 20, font=MONO, weight=700, extra='text-decoration="underline"')
    p.sticker(1045, 180, "PATENT HOLDER", GREEN, -10, 19)
    p.sticker(1040, 280, "NEC #7 / 1500+", BLUE, 7, 19)
    p.sticker(1050, 380, "9 APPS LIVE", ORANGE, -5, 22)
    p.save(f"hero-{theme}.svg", f"{NAME}, EEE engineer. I automate. You go home early. Electrical engineer at Indo Tech Transformers writing the software the shop floor runs on.")

    # ── crossing ticker tapes ──
    p = Poster(t, 1200, 210)
    tape1 = "  ★  ".join(["9 APPS IN PRODUCTION", "128 TESTS", "1 PATENT", "RANK #7 OF 1500+", "30 MIN → 30 SEC", "ZERO SPREADSHEETS SPARED"]) + "  ★  "
    tape2 = "  ✦  ".join(["NO-CODE? NO.", "ALL CODE.", "SHIPPED, NOT SIDE-PROJECTED", "RUNS EVERY SHIFT", "BUILT ON THE FACTORY FLOOR"]) + "  ✦  "
    for i, (txt, fill, rot, y, cls) in enumerate([(tape1, YELLOW, -3, 70, "l"), (tape2, PINK, 2.5, 140, "r")]):
        p.body.append(f'<g transform="rotate({rot} 600 {y})"><rect x="-60" y="{y - 30}" width="1320" height="60" fill="{fill}" stroke="{ink}" stroke-width="4"/>'
                      f'<g class="{cls}"><text x="0" y="{y + 11}" font-family="{HEAVY}" font-size="28" font-weight="900" fill="{BLACK}" xml:space="preserve">{esc(txt * 6)}</text></g></g>')
    p.save(f"ticker-{theme}.svg", tape1 + tape2,
           ".l{animation:l 30s linear infinite}.r{animation:r 30s linear infinite}"
           "@keyframes l{to{transform:translateX(-1400px)}}@keyframes r{from{transform:translateX(-1400px)}to{transform:none}}")

    # ── receipts ──
    p = Poster(t, 1200, 300)
    p.text(40, 80, "THE RECEIPTS", 56, extra='letter-spacing="-2"')
    p.text(1160, 80, "(NOT VIBES. NUMBERS.)", 20, font=MONO, anchor="end", weight=700)
    bw = (1200 - 80 - 3 * 28) / 4
    for i, (v, lab) in enumerate(STATS):
        x = 40 + i * (bw + 28)
        p.box(x, 112, bw, 150, LOUD[i], 10)
        p.text(x + 22, 196, v, 64 if len(v) < 5 else 40, BLACK, extra='letter-spacing="-2"')
        p.text(x + 22, 238, lab.upper(), 15, BLACK, MONO, weight=700)
    p.save(f"receipts-{theme}.svg", "The receipts: " + "; ".join(f"{v} {l}" for v, l in STATS))

    # ── project tickets ──
    for i, (slug, icon, name, status, url, hook, detail, stack) in enumerate(PROJECTS):
        p = Poster(t, 600, 330)
        c = LOUD[i % len(LOUD)]
        p.box(24, 24, 544, 274, c, 10)
        p.text(44, 104, f"{i + 1:02d}", 76, "none", extra=f'stroke="{BLACK}" stroke-width="3" letter-spacing="-3"')
        p.text(180, 70, name.upper() if len(name) < 20 else name.upper().replace("TRANSFORMER ", ""), 24, BLACK)
        p.body.append(f'<g transform="rotate(-3 470 98)">')
        sw = len(status) * 11 + 26
        p.box(548 - sw, 82, sw, 34, "#FFFFFF", 4, 3)
        p.text(548 - sw / 2, 105, status, 15, BLACK, MONO, "middle", 700)
        p.body.append("</g>")
        p.text(180, 104, icon, 30)
        p.text(44, 168, hook, 18, BLACK, MONO, weight=700)
        p.text(44, 198, detail, 16, BLACK, MONO, weight=400)
        p.body.append(f'<rect x="24" y="236" width="544" height="62" fill="{BLACK}"/>')
        p.text(44, 274, "> " + stack, 17, c, MONO, weight=700)
        p.text(548, 274, "OPEN ↗" if url else "PRIVATE", 15, "#FFFFFF", MONO, "end", 700)
        p.save(f"card-{slug}-{theme}.svg", f"{i + 1:02d} {name} ({status}): {hook} {detail}")

    # ── hall of flex ──
    p = Poster(t, 1200, 420)
    p.text(40, 80, "HALL OF FLEX", 56, extra='letter-spacing="-2"')
    p.sticker(1040, 62, "CERTIFIED", YELLOW, 6, 20)
    p.box(40, 112, 1120, 268, t["bg"], 10)
    for j, (yr, title, det) in enumerate(MILESTONES):
        y = 112 + j * 53.6
        if j:
            p.body.append(f'<line x1="40" x2="1160" y1="{y}" y2="{y}" stroke="{ink}" stroke-width="3"/>')
        p.body.append(f'<rect x="40" y="{y}" width="130" height="53.6" fill="{LOUD[j]}" stroke="{ink}" stroke-width="3"/>')
        p.text(105, y + 36, yr, 22, BLACK, MONO, "middle", 700)
        p.text(196, y + 37, title.upper(), 24)
        p.text(1136, y + 36, det, 19, font=MONO, anchor="end", weight=700)
    p.save(f"flex-{theme}.svg", "Hall of flex: " + "; ".join(f"{y} {a}, {b}" for y, a, b in MILESTONES))

    # ── weapons of choice ──
    p = Poster(t, 1200, 380)
    p.text(40, 80, "WEAPONS OF CHOICE", 56, extra='letter-spacing="-2"')
    y, k = 116, 0
    for group, items in TOOLS.items():
        p.text(40, y + 34, group.upper() + ":", 18, font=MONO, weight=700)
        x = 240
        for it in items:
            w = len(it) * 9.2 + 26
            p.box(x, y, w, 46, LOUD[k % len(LOUD)], 5, 3)
            p.text(x + w / 2, y + 30, it.upper(), 15, BLACK, MONO, "middle", 700)
            x, k = x + w + 12, k + 1
        y += 82
    p.save(f"weapons-{theme}.svg", "; ".join(f"{g}: {', '.join(v)}" for g, v in TOOLS.items()))

    # ── footer ──
    p = Poster(t, 1200, 330)
    p.text(600, 108, "HIRE ME.", 84, anchor="middle", extra='letter-spacing="-3"')
    p.text(600, 168, "OR DON'T. THE SCRIPTS RUN ANYWAY.", 30, anchor="middle")
    p.box(300, 206, 600, 64, YELLOW, 8)
    p.text(600, 248, EMAIL + " ", 24, BLACK, MONO, "middle", 700)
    p.body.append(f'<rect class="cur" x="866" y="226" width="14" height="28" fill="{BLACK}"/>')
    p.save(f"footer-{theme}.svg", f"Hire me. Or don't. The scripts run anyway. {EMAIL}",
           ".cur{animation:b 1s steps(1) infinite}@keyframes b{50%{opacity:0}}")
print("ok")
