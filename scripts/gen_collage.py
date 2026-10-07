"""Collage / zine profile: ransom-note letters, torn paper, tape, a halftone cut-out, stamps and ticket stubs.
Run: python scripts/gen_collage.py [photo]"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, photo_grid, wrap
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, WINS, short

F = "collage"
FONTS = ["'Arial Black', sans-serif", "Georgia, serif", "'Courier New', monospace", "Impact, sans-serif", "'Times New Roman', serif",
         "'Trebuchet MS', sans-serif", "'Brush Script MT', cursive", "Verdana, sans-serif"]
TYPE = "'Courier New', Courier, monospace"
THEMES = {"light": dict(bg="#EDE6DA", cork="#D9C9AE", ink="#151515", papers=["#FFFFFF", "#F7E27C", "#FF6B6B", "#7CC6FE", "#111111", "#FFB5C2", "#B5E48C"], tape="#F2E3B3"),
          "dark": dict(bg="#151311", cork="#2A231C", ink="#F3EEE5", papers=["#F3EEE5", "#F7E27C", "#FF6B6B", "#7CC6FE", "#2B2B2B", "#FFB5C2", "#B5E48C"], tape="#C9B98A")}
photo = photo_grid(F, 56, sys.argv[1] if len(sys.argv) > 1 else None)


def torn(x, y, w, h, rnd, step=14):
    """Rectangle with torn top and bottom edges."""
    top = " ".join(f"L{x + i:.0f},{y + rnd.uniform(-4, 4):.0f}" for i in range(0, int(w) + 1, step))
    bot = " ".join(f"L{x + w - i:.0f},{y + h + rnd.uniform(-4, 4):.0f}" for i in range(0, int(w) + 1, step))
    return f"M{x},{y} {top} L{x + w},{y + h} {bot} Z"


def ransom(c, t, text, x, y, size, rnd):
    """Each letter cut from a different magazine."""
    for ch in text:
        if ch == " ":
            x += size * .5
            continue
        f = rnd.choice(FONTS)
        bg = rnd.choice(t["papers"])
        fg = "#FFFFFF" if bg in ("#111111", "#2B2B2B", "#FF6B6B") else "#111111"
        s = size * rnd.uniform(.85, 1.15)
        w = s * .78
        rot = rnd.uniform(-8, 8)
        c.add(f'<g transform="rotate({rot:.1f} {x + w / 2:.0f} {y - s * .35:.0f})"><rect x="{x:.0f}" y="{y - s * .95:.0f}" width="{w:.0f}" height="{s * 1.15:.0f}" fill="{bg}" '
              f'style="filter:drop-shadow(1px 2px 1px rgba(0,0,0,.3))"/>'
              f'<text x="{x + w / 2:.0f}" y="{y:.0f}" font-family="{f}" font-size="{s * .85:.0f}" font-weight="700" fill="{fg}" text-anchor="middle">{ch}</text></g>')
        x += w + 6
    return x


def tape(c, t, x, y, w=90, rot=-8):
    c.add(f'<rect x="{x}" y="{y}" width="{w}" height="26" fill="{t["tape"]}" opacity=".8" transform="rotate({rot} {x + w / 2} {y + 13})"/>')


for th, t in THEMES.items():
    rnd = random.Random(29)
    c = Canvas(F, t, 1200, 860)
    c.defs.append('<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".7" numOctaves="3" seed="5"/><feColorMatrix values="0 0 0 0 .3 0 0 0 0 .25 0 0 0 0 .2 0 0 0 .18 0"/>'
                  '<feComposite in2="SourceAlpha" operator="in"/></filter>')
    c.add(f'<rect width="1200" height="860" fill="{t["cork"]}"/><rect width="1200" height="860" fill="#000" filter="url(#grain)"/>')
    # halftone cut-out photo on a torn page
    c.add(f'<path d="{torn(60, 120, 420, 520, rnd)}" fill="#F7F3EA" transform="rotate(-3 270 380)" style="filter:drop-shadow(3px 6px 4px rgba(0,0,0,.35))"/>')
    cell = 7
    dots = []
    for r, row in enumerate(photo):
        for q, ch in enumerate(row):
            if ch != "." and int(ch) < 9:
                dots.append(f'<circle cx="{75 + q * cell}" cy="{150 + r * cell}" r="{cell * .5 * ((9 - int(ch)) / 9) ** .7:.2f}"/>')
    c.add(f'<g transform="rotate(-3 270 380)" fill="#151515">{"".join(dots)}</g>')
    tape(c, t, 220, 104, 110, -6)
    c.add(f'<g transform="rotate(4 280 690)"><rect x="110" y="660" width="340" height="60" fill="#FFFFFF" style="filter:drop-shadow(2px 3px 2px rgba(0,0,0,.3))"/></g>')
    c.text(280, 698, "fig. 1: the engineer", 20, "#151515", TYPE, 700, "middle", 'transform="rotate(4 280 690)"')
    # ransom headline
    x = ransom(c, t, "KRISHNA", 540, 160, 70, rnd)
    ransom(c, t, "RAJU S", 560, 270, 70, rnd)
    # cut strips of copy
    strips = ["ELECTRICAL ENGINEER, SOFTWARE BUILDER", "9 APPS RUNNING ON A REAL FACTORY FLOOR", "30 MINUTES OF PAPERWORK → 30 SECONDS",
              "PATENT FILED: STREET LIGHTS THAT FOLLOW YOU"]
    for i, s in enumerate(strips):
        y = 340 + i * 62
        rot = rnd.uniform(-2.5, 2.5)
        bg = t["papers"][[0, 1, 3, 6][i]]
        c.add(f'<g transform="rotate({rot:.1f} 820 {y})"><path d="{torn(540, y - 30, 600, 44, rnd, 10)}" fill="{bg}" style="filter:drop-shadow(2px 3px 2px rgba(0,0,0,.3))"/>'
              f'<text x="556" y="{y}" font-family="{TYPE}" font-size="21" font-weight="700" fill="#151515">{s}</text></g>')
    # stamp + ticket
    c.add(f'<g transform="rotate(-12 650 700)"><circle cx="650" cy="700" r="78" fill="none" stroke="#C1121F" stroke-width="5"/>'
          f'<circle cx="650" cy="700" r="64" fill="none" stroke="#C1121F" stroke-width="2"/></g>')
    c.text(650, 694, "NEC #7", 26, "#C1121F", "'Arial Black', sans-serif", 700, "middle", 'transform="rotate(-12 650 700)"')
    c.text(650, 722, "OF 1500+", 15, "#C1121F", TYPE, 700, "middle", 'transform="rotate(-12 650 700)"')
    c.add(f'<g transform="rotate(5 960 720)"><rect x="800" y="650" width="330" height="140" fill="#F7E27C" style="filter:drop-shadow(2px 3px 2px rgba(0,0,0,.3))"/>'
          f'<line x1="1060" x2="1060" y1="650" y2="790" stroke="#151515" stroke-dasharray="6 5"/>'
          f'<text x="820" y="690" font-family="{TYPE}" font-size="15" font-weight="700" fill="#151515">ADMIT ONE</text>'
          f'<text x="820" y="730" font-family="\'Arial Black\', sans-serif" font-size="26" fill="#151515">HIRE KRISHNA</text>'
          f'<text x="820" y="764" font-family="{TYPE}" font-size="12" fill="#151515">{EMAIL}</text>'
          f'<text x="1095" y="728" font-family="{TYPE}" font-size="14" font-weight="700" fill="#151515" transform="rotate(-90 1095 720)" text-anchor="middle">№ 2004</text></g>')
    c.css.append(".wig{animation:wg 3s ease-in-out infinite}@keyframes wg{50%{transform:rotate(2deg)}}")
    c.save(f"zine-{th}.svg", f"Collage cover: ransom-note letters spelling KRISHNA RAJU S, a halftone photo cut-out, strips reading electrical engineer and software builder, 9 apps on a real factory floor, 30 minutes to 30 seconds, patent filed; an NEC rank 7 stamp and a ticket: admit one, hire Krishna.")

    # projects as pinned clippings
    c = Canvas(F, t, 1200, 760)
    c.defs.append('<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".7" numOctaves="3" seed="8"/><feColorMatrix values="0 0 0 0 .3 0 0 0 0 .25 0 0 0 0 .2 0 0 0 .18 0"/>'
                  '<feComposite in2="SourceAlpha" operator="in"/></filter>')
    c.add(f'<rect width="1200" height="760" fill="{t["cork"]}"/><rect width="1200" height="760" fill="#000" filter="url(#grain)"/>')
    ransom(c, t, "THE WORK", 60, 90, 54, rnd)
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        x, y = 50 + (i % 5) * 226, 140 + (i // 5) * 300
        rot = rnd.uniform(-4, 4)
        bg = t["papers"][[0, 1, 3, 6, 5][i % 5]]
        c.add(f'<g class="wig" style="animation-delay:-{i * .3:.1f}s;transform-origin:{x + 100}px {y}px"><g transform="rotate({rot:.1f} {x + 100} {y + 120})">'
              f'<path d="{torn(x, y, 200, 250, rnd, 12)}" fill="{bg}" style="filter:drop-shadow(2px 4px 3px rgba(0,0,0,.35))"/>'
              f'<circle cx="{x + 100}" cy="{y + 12}" r="8" fill="#C1121F"/><circle cx="{x + 98}" cy="{y + 10}" r="3" fill="#FFF" opacity=".7"/>'
              f'<text x="{x + 14}" y="{y + 56}" font-family="\'Arial Black\', sans-serif" font-size="{19 if len(short(name)) < 14 else 15}" fill="#151515">{short(name).upper()}</text>')
        for j, l in enumerate(wrap(hook, 15, 175, .58)[:4]):
            c.add(f'<text x="{x + 14}" y="{y + 92 + j * 22}" font-family="{TYPE}" font-size="15" fill="#151515">{l}</text>')
        c.add(f'<rect x="{x + 14}" y="{y + 206}" width="{len(status) * 9 + 16}" height="24" fill="#151515"/>'
              f'<text x="{x + 22}" y="{y + 223}" font-family="{TYPE}" font-size="13" font-weight="700" fill="#F7E27C">{status}</text></g></g>')
    c.css.append(".wig{animation:wg 4s ease-in-out infinite}@keyframes wg{50%{transform:rotate(1.5deg)}}")
    c.save(f"work-{th}.svg", "Pinned clippings of the work: " + "; ".join(f"{p[1]}, {p[4]}" for p in PROJECTS))

links = " ✂ ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Collage / zine: cut paper on cork by day, on a dark board by night, following your GitHub theme. Built by scripts/gen_collage.py -->

<p align="center">{pic(F, "zine", f"Collage cover for {NAME}")}</p>
<p align="center">{pic(F, "work", "Pinned clippings of the work")}</p>
<p align="center">{links}</p>
<p align="center"><sub>cut, taped and pinned in code · <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}">linkedin</a></sub></p>
""")
print("ok")
