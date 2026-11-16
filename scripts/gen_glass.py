"""Liquid-glass panels for the profile README, in light and dark variants.

Run:  python scripts/gen_glass.py   (content lives in scripts/profile_data.py)
Each panel refracts its own moving wallpaper: a displaced, blurred copy of the backdrop is
clipped to the glass shape, then tinted and given a specular rim.
"""
import os, sys
from xml.sax.saxutils import escape as esc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from profile_data import NAME, EMAIL, LINKEDIN, STATS, PROJECTS, MILESTONES, TOOLS

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "glass")
os.makedirs(OUT, exist_ok=True)
FONT = "'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI Variable Display', 'Segoe UI', Inter, system-ui, sans-serif"
MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, monospace"
THEMES = {
    "light": dict(base="#E9F0FF", blobs=["#7CC6FE", "#FF9EC7", "#FFD27A", "#A79BFF"], blob_op=.85, ink="#0B1020",
                  soft="#3A4358", tint="#FFFFFF", tint_op=.42, rim=.95, shadow="#3B4A7A", accent="#3B5BFF"),
    "dark": dict(base="#05070F", blobs=["#3A5BFF", "#D946EF", "#14B8A6", "#F59E0B"], blob_op=.5, ink="#F5F7FF",
                 soft="#C9D0E4", tint="#0A0E1C", tint_op=.5, rim=.45, shadow="#000000", accent="#8FA5FF"),
}
REDUCE = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


class Panel:
    def __init__(self, t, w, h, seed=0):
        self.t, self.w, self.h, self.seed, self.body, self.n = t, w, h, seed, [], 0

    def defs(self):
        t, w, h, s = self.t, self.w, self.h, self.seed
        spots = [(.18, .25), (.82, .2), (.7, .85), (.25, .9)]
        blobs = "".join(
            f'<circle class="b b{i}" cx="{w * spots[(i + s) % 4][0]:.0f}" cy="{h * spots[(i + s) % 4][1]:.0f}" '
            f'r="{max(w, h) * .32:.0f}" fill="{c}" opacity="{t["blob_op"]}"/>' for i, c in enumerate(t["blobs"]))
        return f"""<clipPath id="all"><rect width="{w}" height="{h}" rx="36"/></clipPath>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="{max(w, h) * .07:.0f}"/></filter>
<filter id="refract" x="-10%" y="-10%" width="120%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency=".006 .01" numOctaves="2" seed="{s + 3}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="70" xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feGaussianBlur in="d" stdDeviation="10"/>
</filter>
<filter id="lift" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="18" stdDeviation="20" flood-color="{t['shadow']}" flood-opacity=".22"/></filter>
<linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="{t['rim']}"/>
  <stop offset=".45" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-color="#fff" stop-opacity="{t['rim'] * .6:.2f}"/></linearGradient>
<linearGradient id="spec" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="ink" x1="0" x2="1"><stop offset="0" stop-color="{t['ink']}"/><stop offset="1" stop-color="{t['accent']}"/></linearGradient>
<g id="wall"><rect width="{w}" height="{h}" fill="{t['base']}"/><g filter="url(#soft)">{blobs}</g></g>"""

    def glass(self, x, y, w, h, rx=28, tint=None, lift=True):
        """A liquid-glass shape: refracted wallpaper + tint + specular top + rim."""
        self.n += 1
        t, cid = self.t, f"g{self.n}"
        op = t["tint_op"] if tint is None else tint
        self.body.append(f"""<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>
<g {'filter="url(#lift)"' if lift else ''}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{t['base']}"/></g>
<g clip-path="url(#{cid})"><use href="#wall" filter="url(#refract)"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{t['tint']}" opacity="{op}"/>
  <rect x="{x}" y="{y}" width="{w}" height="{min(h * .45, 90):.0f}" fill="url(#spec)" opacity=".5"/></g>
<rect x="{x + .75}" y="{y + .75}" width="{w - 1.5}" height="{h - 1.5}" rx="{rx}" fill="none" stroke="url(#rim)" stroke-width="1.5"/>""")

    def text(self, x, y, s, size, fill=None, weight=400, anchor="start", font=FONT, extra=""):
        self.body.append(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
                         f'fill="{fill or self.t["ink"]}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')

    def capsule(self, x, y, label, size=16, weight=600):
        w = 32 + len(label) * size * .56
        self.glass(x, y, w, size * 2.4, size * 1.2, lift=False)
        self.text(x + w / 2, y + size * 1.55, label, size, weight=weight, anchor="middle")
        return w

    def save(self, name, title, style=""):
        w, h = self.w, self.h
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" '
               f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
               f'<defs>{self.defs()}</defs><style>'
               '.b{transform-box:fill-box;transform-origin:center;animation:drift 16s ease-in-out infinite alternate}'
               '.b1{animation-duration:21s;animation-delay:-5s}.b2{animation-duration:25s;animation-delay:-9s}.b3{animation-duration:19s;animation-delay:-13s}'
               '@keyframes drift{0%{transform:translate(0,0) scale(1)}50%{transform:translate(-8%,6%) scale(1.12)}100%{transform:translate(7%,-5%) scale(.92)}}'
               f'{style}{REDUCE}</style>'
               f'<g clip-path="url(#all)"><use href="#wall"/>{"".join(self.body)}</g></svg>\n')
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(svg)


for theme, t in THEMES.items():
    # ── hero ──
    p = Panel(t, 1200, 600, 0)
    p.glass(40, 28, 1120, 48, 24, lift=False)
    p.body.append("".join(f'<circle cx="{70 + i * 22}" cy="52" r="6.5" fill="{c}"/>' for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"])))
    p.text(600, 58, "krish.exe", 16, weight=600, anchor="middle")
    p.text(1136, 58, "● online · shipping", 15, t["soft"], 500, "end")
    p.glass(40, 104, 1120, 456, 40)
    p.text(84, 174, "HELLO, FACTORY FLOOR.", 16, t["accent"], 700, extra='letter-spacing="3"')
    p.text(80, 262, NAME, 86, weight=800, extra='letter-spacing="-3"')
    p.text(84, 322, "Engineered for the shop floor.", 36, "url(#ink)", 700, extra='letter-spacing="-.5"')
    p.text(84, 372, "Electrical engineer who ships software. Nine apps in production,", 20, t["soft"])
    p.text(84, 402, "one patent, and zero spreadsheets left behind.", 20, t["soft"])
    x = 84
    for lab in ["⚡ EEE engineer", "📜 Patent holder", "🏆 NEC #7 / 1500+"]:
        x += p.capsule(x, 448, lab) + 12
    # floating liquid drop with the headline number
    p.body.append('<g class="drop">')
    p.glass(860, 170, 230, 230, 115, tint=t["tint_op"] * .6)
    p.text(975, 300, "9", 96, "url(#ink)", 800, "middle", extra='letter-spacing="-4"')
    p.text(975, 340, "apps live", 18, t["soft"], 600, "middle")
    p.body.append("</g>")
    p.save(f"hero-{theme}.svg", f"{NAME}. Hello, factory floor. Engineered for the shop floor: electrical engineer who ships software, nine apps in production, one patent.",
           ".drop{animation:bob 6s ease-in-out infinite}@keyframes bob{50%{transform:translateY(-14px)}}")

    # ── stats ──
    p = Panel(t, 1200, 210, 1)
    cw = (1200 - 80 - 3 * 20) / 4
    for i, (v, lab) in enumerate(STATS):
        x = 40 + i * (cw + 20)
        p.glass(x, 30, cw, 150, 30)
        p.text(x + 28, 104, v, 50 if len(v) < 5 else 40, "url(#ink)", 800, extra='letter-spacing="-1.5"')
        p.text(x + 28, 146, lab, 17, t["soft"], 500)
    p.save(f"stats-{theme}.svg", "; ".join(f"{v} {l}" for v, l in STATS))

    # ── project cards ──
    for i, (slug, icon, name, status, url, hook, detail, stack) in enumerate(PROJECTS):
        big = i < 6
        w, h = (600, 300) if big else (300, 224)
        p = Panel(t, w, h, i)
        p.glass(18, 18, w - 36, h - 36, 30)
        if big:
            p.glass(46, 46, 60, 60, 18, lift=False)
            p.text(76, 87, icon, 30, anchor="middle")
            p.text(126, 74, name, 25, weight=700, extra='letter-spacing="-.3"')
            p.text(126, 100, status, 13, t["accent"], 700, font=MONO, extra='letter-spacing="1.5"')
            p.text(46, 160, hook, 21, weight=600)
            p.text(46, 192, detail, 17, t["soft"])
            p.text(46, 248, stack, 15, t["soft"], 500, font=MONO)
        else:
            p.text(42, 76, icon, 28)
            p.text(42, 116, name if len(name) < 17 else " ".join(name.split()[:2]), 21, weight=700)
            p.text(42, 140, status, 12, t["accent"], 700, font=MONO, extra='letter-spacing="1.5"')
            words, line, lines = hook.split(), "", []
            for wd in words:
                if len(line + wd) > 26:
                    lines.append(line.strip()); line = ""
                line += wd + " "
            lines.append(line.strip())
            for j, ln in enumerate(lines[:2]):
                p.text(42, 166 + j * 19, ln, 15, t["soft"])
        p.save(f"card-{slug}-{theme}.svg", f"{name}: {hook} {detail}")

    # ── milestones ──
    p = Panel(t, 1200, 290, 2)
    p.glass(30, 20, 1140, 250, 32)
    p.glass(60, 70, 1080, 26, 13, lift=False)
    for i, (yr, title, det) in enumerate(MILESTONES):
        x = 140 + i * 230
        p.glass(x - 22, 61, 44, 44, 22, tint=t["tint_op"] * 1.6, lift=False)
        p.body.append(f'<circle cx="{x}" cy="83" r="7" fill="{t["accent"]}"/>')
        p.text(x, 44, yr, 15, t["soft"], 600, "middle", MONO)
        p.text(x, 150, title, 20, weight=700, anchor="middle")
        p.text(x, 178, det, 15, t["soft"], anchor="middle")
    p.text(600, 248, "Every one of these started with someone saying “that's not possible.”", 18, t["soft"], 500, "middle", extra='font-style="italic"')
    p.save(f"milestones-{theme}.svg", "; ".join(f"{y} {a}, {b}" for y, a, b in MILESTONES))

    # ── dock ──
    p = Panel(t, 1200, 330, 3)
    p.glass(30, 18, 1140, 294, 32)
    y = 34
    for group, items in TOOLS.items():
        p.text(64, y + 38, group, 17, t["soft"], 700)
        widths = [24 + len(it) * 8.8 for it in items]
        total = sum(widths) + 10 * (len(items) - 1) + 32
        p.glass(220, y, total, 60, 30)
        x = 236
        for it, wd in zip(items, widths):
            p.glass(x, y + 10, wd, 40, 20, tint=t["tint_op"] * 1.4, lift=False)
            p.text(x + wd / 2, y + 36, it, 15, weight=600, anchor="middle")
            x += wd + 10
        y += 92
    p.save(f"dock-{theme}.svg", "; ".join(f"{g}: {', '.join(v)}" for g, v in TOOLS.items()))

    # ── footer ──
    p = Panel(t, 1200, 280, 1)
    p.glass(40, 30, 1120, 220, 40)
    p.text(600, 104, "Your next “quick manual step”", 28, t["soft"], 500, "middle")
    p.text(600, 160, "is my next app.", 52, "url(#ink)", 800, "middle", extra='letter-spacing="-1.5"')
    p.capsule(600 - (32 + len(EMAIL) * 9) / 2, 186, EMAIL, 16, 600)
    p.save(f"footer-{theme}.svg", f"Your next quick manual step is my next app. {EMAIL}")
print("ok")
