"""Organic / natural profile: a tree that grows from electrical roots; career branches, project leaves, fireflies at night.
Run: python scripts/gen_organic.py"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, EXPERIENCE, COLLEGE, CGPA, short

F = "organic"
SERIF = "Georgia, 'Iowan Old Style', 'Palatino Linotype', serif"
SANS = "'Avenir Next', 'Segoe UI', 'Helvetica Neue', sans-serif"
THEMES = {"light": dict(bg="#F5EFE3", blob="#E6DCC8", ink="#2F3A2C", soft="#6E7A62", bark="#6B4E37", leaf=["#8FA98F", "#6F8F5E", "#A9BF8E", "#C66B3D"], soil="#D9C7A8", glow="#E6B655", night=0),
          "dark": dict(bg="#101716", blob="#18221F", ink="#E6EFE3", soft="#9DB09A", bark="#8A6A50", leaf=["#4F7A5A", "#7FB685", "#5E9C6B", "#E08A5E"], soil="#1E2622", glow="#FFE87A", night=1)}
LEAF = "M0,0 C 18,-22 52,-22 74,0 C 52,22 18,22 0,0 Z"

for th, t in THEMES.items():
    rnd = random.Random(25)
    c = Canvas(F, t, 1200, 1140)
    c.add(f'<rect width="1200" height="1140" fill="{t["bg"]}"/>')
    c.add(f'<path d="M-40,160 C120,40 300,120 360,40 S560,-20 640,60 S900,160 1240,40 V-10 H-40Z" fill="{t["blob"]}"/>'
          f'<path d="M-40,1150 C200,1070 380,1120 520,1070 S860,1020 1240,1090 V1150Z" fill="{t["soil"]}"/>')
    c.text(60, 80, "Rooted in electrical.", 34, t["ink"], SERIF, 400, extra='font-style="italic"')
    c.text(60, 122, "Growing into software.", 34, t["ink"], SERIF, 700, extra='font-style="italic"')
    c.text(1140, 80, NAME, 22, t["soft"], SANS, 600, "end", 'letter-spacing="2"')
    # roots
    for i in range(7):
        a = -70 + i * 23
        x2, y2 = 600 + 180 * math.sin(math.radians(a)), 1060 + 50 * abs(math.cos(math.radians(a)))
        c.add(f'<path class="grow" d="M600,1020 Q{600 + 90 * math.sin(math.radians(a)):.0f},{1050:.0f} {x2:.0f},{y2:.0f}" stroke="{t["bark"]}" stroke-width="{6 - abs(i - 3)}" fill="none" stroke-linecap="round"/>')
    c.text(600, 1128, f"roots: B.E. Electrical & Electronics · {COLLEGE} · CGPA {CGPA}", 15, t["ink"], SANS, 600, "middle")
    # trunk
    c.add(f'<path class="grow" d="M590,1020 C575,900 615,800 596,700 C580,620 610,560 600,500" stroke="{t["bark"]}" stroke-width="26" fill="none" stroke-linecap="round"/>')
    # career branches, oldest at the bottom
    stops = list(reversed(EXPERIENCE))
    for i, (org, role, when, where, what, win) in enumerate(stops):
        y = 960 - i * 92
        side = -1 if i % 2 == 0 else 1
        ex, ey = 600 + side * 210, y - 60
        c.add(f'<path class="grow" style="animation-delay:{.6 + i * .3:.1f}s" d="M600,{y} C{600 + side * 120},{y - 10} {600 + side * 200},{y - 70} {ex},{ey}" '
              f'stroke="{t["bark"]}" stroke-width="{10 - i}" fill="none" stroke-linecap="round"/>')
        for k in range(3):
            lx, ly = ex + side * (k * 14 - 10), ey - 10 + k * 8
            c.add(f'<path d="{LEAF}" fill="{t["leaf"][k % 3]}" transform="translate({lx:.0f} {ly:.0f}) rotate({-30 + side * 20 + k * 25}) scale(.6)"/>')
        anchor = "end" if side < 0 else "start"
        tx = ex + side * 40
        c.text(tx, ey - 4, when, 13, t["soft"], SANS, 700, anchor)
        c.text(tx, ey + 18, org, 18, t["ink"], SERIF, 700, anchor)
        c.text(tx, ey + 38, win, 12, t["soft"], SANS, 400, anchor)
    # canopy of project leaves
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        a = math.radians(-168 + i * (156 / 9))
        lx, ly = 600 + 470 * math.cos(a), 500 + 300 * math.sin(a)
        col = t["leaf"][3] if status in ("PRODUCTION", "LIVE") else t["leaf"][i % 3]
        rot = math.degrees(a) + 90
        c.add(f'<g class="sway" style="animation-delay:-{i * .4:.1f}s;transform-origin:{lx:.0f}px {ly:.0f}px">'
              f'<path d="{LEAF}" fill="{col}" transform="translate({lx - 40:.0f} {ly:.0f}) scale(1.1)"/></g>')
        c.add(f'<path d="M600,500 Q{(600 + lx) / 2:.0f},{ly + 60:.0f} {lx:.0f},{ly:.0f}" stroke="{t["bark"]}" stroke-width="2" fill="none" opacity=".5"/>')
        ox, oy = 600 + 470 * 1.13 * math.cos(a), 500 + 300 * 1.2 * math.sin(a)
        anc = "end" if math.cos(a) < -.3 else "start" if math.cos(a) > .3 else "middle"
        half = len(short(name)) * 8
        ox = min(ox, 1160 - half) if anc == "start" else max(ox, 40 + half) if anc == "end" else ox
        c.text(ox, oy + 5, short(name), 14, t["ink"], SANS, 700, anc)
    c.text(600, 420, "ten leaves, all still growing", 15, t["soft"], SERIF, 400, "middle", 'font-style="italic"')
    # fireflies by night, drifting pollen by day
    for i in range(22):
        x, y = rnd.uniform(40, 1160), rnd.uniform(200, 1000)
        c.add(f'<circle class="fly" style="animation-delay:-{rnd.uniform(0, 5):.1f}s;animation-duration:{rnd.uniform(4, 8):.1f}s" cx="{x:.0f}" cy="{y:.0f}" r="{3 if t["night"] else 2.5}" '
              f'fill="{t["glow"]}" opacity=".8"/>')
    c.css.append(".grow{stroke-dasharray:1100;animation:gr 3s ease-out both}@keyframes gr{from{stroke-dashoffset:1100}}"
                 ".sway{animation:sw 5s ease-in-out infinite}@keyframes sw{50%{transform:rotate(8deg)}}"
                 ".fly{animation:fy 6s ease-in-out infinite}@keyframes fy{0%,100%{transform:translate(0,0);opacity:.2}50%{transform:translate(18px,-26px);opacity:1}}")
    c.save(f"tree-{th}.svg", f"A tree for {NAME}: roots in electrical and electronics engineering, branches for each career stage from Southern Railway to Indo Tech Transformers, and ten project leaves.")

links = " · ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Organic / natural: a growing tree in daylight, fireflies by night, following your GitHub theme. Built by scripts/gen_organic.py -->

<p align="center">{pic(F, "tree", f"A tree for {NAME}: rooted in electrical, growing into software")}</p>

<p align="center"><i>Planted in Chennai, 2004. Watered with chai. Pruned by tests.</i></p>

<p align="center">🌱 {links}</p>

<p align="center"><sub>say hello: <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}">linkedin</a></sub></p>
""")
print("ok")
