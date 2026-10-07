"""Illustrative profile: an isometric illustration of the factory campus, one building per project, trucks on the road.
Day and night versions. Run: python scripts/gen_isometric.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, SANS
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short

F = "isometric"
THEMES = {"light": dict(bg="#EAF4F4", ground="#CDE5D2", road="#8C93A3", ink="#1F2937", soft="#5B6575", win="#BFE3FF", lamp="#FFB703", night=0,
                        walls=[("#F4A261", "#E76F51"), ("#90BE6D", "#6A994E"), ("#8ECAE6", "#219EBC"), ("#CDB4DB", "#9D79BC"), ("#FFD166", "#E9B44C")]),
          "dark": dict(bg="#0B1020", ground="#16233A", road="#2A3550", ink="#E7ECF5", soft="#8C97AD", win="#FFD166", lamp="#FFD166", night=1,
                       walls=[("#7A4A3A", "#5C3428"), ("#3F5E3A", "#2E472B"), ("#2D5A73", "#1F4256"), ("#57466B", "#433553"), ("#7A6A33", "#5E5126")])}
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))
OX, OY, U = 600, 340, 30


def iso(x, y, z=0):
    return OX + (x - y) * C30 * U, OY + (x + y) * S30 * U - z * U


def pts(*p):
    return " ".join(f"{a:.1f},{b:.1f}" for a, b in p)


def building(x, y, w, d, h, col, t, lit):
    top, side = col
    A, B, Cc, D = iso(x, y, h), iso(x + w, y, h), iso(x + w, y + d, h), iso(x, y + d, h)
    out = [f'<polygon points="{pts(iso(x, y + d), iso(x + w, y + d), Cc, D)}" fill="{side}"/>',
           f'<polygon points="{pts(iso(x + w, y), iso(x + w, y + d), Cc, B)}" fill="{top}"/>',
           f'<polygon points="{pts(A, B, Cc, D)}" fill="{top}" opacity=".85"/>']
    for k in range(int(w)):
        for lvl in range(int(h)):
            wx, wy = iso(x + k + .3, y + d, lvl + .7)
            on = lit and (k + lvl) % 2 == 0
            out.append(f'<polygon points="{pts((wx, wy), (wx + 12, wy + 7), (wx + 12, wy - 7), (wx, wy - 14))}" fill="{t["win"]}" opacity="{1 if on or not t["night"] else .25}" '
                       f'{"class=" + chr(34) + "blink" + chr(34) if on and t["night"] else ""}/>')
    return "".join(out)


LOTS = [(-8, -1, 2, 2, 2), (-4.5, -1, 2, 2, 3), (-1, -1, 2, 2, 2), (2.5, -1, 2, 2, 4), (6, -1, 2, 2, 2),
        (-8, 4.4, 2, 2, 3), (-4.5, 4.4, 2, 2, 2), (-1, 4.4, 2, 2, 2), (2.5, 4.4, 2, 2, 3), (6, 4.4, 2, 2, 2)]

for th, t in THEMES.items():
    c = Canvas(F, t, 1200, 760)
    c.add(f'<rect width="1200" height="760" fill="{t["bg"]}"/>')
    c.add(f'<polygon points="{pts(iso(-9, -3), iso(10, -3), iso(10, 8), iso(-9, 8))}" fill="{t["ground"]}"/>')
    c.add(f'<polygon points="{pts(iso(-9, 1.6), iso(10, 1.6), iso(10, 3.2), iso(-9, 3.2))}" fill="{t["road"]}"/>')
    c.add("".join(f'<polygon points="{pts(iso(x, 2.35), iso(x + .6, 2.35), iso(x + .6, 2.45), iso(x, 2.45))}" fill="#FFFFFF" opacity=".7"/>' for x in range(-9, 10)))
    order = sorted(range(len(PROJECTS)), key=lambda i: LOTS[i][0] + LOTS[i][1])
    labels = []
    for i in order:
        slug, name, status, url, hook, impact, stack = PROJECTS[i]
        x, y, w, d, h = LOTS[i]
        lit = status in ("PRODUCTION", "LIVE", "IN USE", "NEW")
        c.add(building(x, y, w, d, h, t["walls"][i % 5], t, lit))
        sx, sy = iso(x + w / 2, y + d / 2, h)
        labels.append((sx, sy, 34 + (i % 2) * 30, short(name), status in ("PRODUCTION", "LIVE")))
    for sx, sy, lift, label, live in labels:  # signs go on top of every building, staggered so neighbours never collide
        c.add(f'<line x1="{sx:.0f}" y1="{sy:.0f}" x2="{sx:.0f}" y2="{sy - lift:.0f}" stroke="{t["ink"]}" stroke-width="1.5"/>'
              f'<rect x="{sx - 62:.0f}" y="{sy - lift - 24:.0f}" width="124" height="26" rx="6" fill="{t["bg"]}" stroke="{t["ink"]}" stroke-width="1.2"/>')
        c.text(sx, sy - lift - 6, label, 12, t["ink"], SANS, 700, "middle")
        if live:
            c.add(f'<circle class="beacon" cx="{sx + 70:.0f}" cy="{sy - lift - 11:.0f}" r="5" fill="#2BB673"/>')
    # smoke from the testing building, trucks on the road
    bx, by = iso(3.5, 0, 4)
    c.add("".join(f'<circle class="smoke" style="animation-delay:{k * .8}s" cx="{bx:.0f}" cy="{by - 10:.0f}" r="{10 + k * 3}" fill="{t["soft"]}" opacity=".35"/>' for k in range(3)))
    for k in range(2):
        tx, ty = iso(-9, 2.0 + k * .8)
        dx, dy = iso(10, 2.0 + k * .8)
        c.add(f'<g class="drive" style="animation-delay:-{k * 4}s;--dx:{dx - tx:.0f}px;--dy:{dy - ty:.0f}px">'
              f'<polygon points="{pts((tx, ty), (tx + 30, ty + 17), (tx + 30, ty + 3), (tx, ty - 14))}" fill="#E85D04"/>'
              f'<polygon points="{pts((tx + 30, ty + 17), (tx + 42, ty + 10), (tx + 42, ty - 4), (tx + 30, ty + 3))}" fill="#F48C06"/></g>')
    c.text(40, 60, NAME, 36, t["ink"], SANS, 800, extra='letter-spacing="-1"')
    c.text(40, 92, "The campus I keep building. One building per project.", 17, t["soft"], SANS)
    c.text(40, 730, "● green beacon = live or in production", 13, t["soft"], SANS)
    c.text(1160, 730, "illustrated in code, not in Figma", 13, t["soft"], SANS, anchor="end")
    c.css.append(".blink{animation:bk 3s steps(1) infinite}@keyframes bk{50%{opacity:.4}}"
                 ".beacon{animation:bc 1.4s ease-in-out infinite}@keyframes bc{50%{opacity:.2}}"
                 ".smoke{animation:sm 3s ease-out infinite}@keyframes sm{to{transform:translate(20px,-60px) scale(1.8);opacity:0}}"
                 ".drive{animation:dv 8s linear infinite}@keyframes dv{to{transform:translate(var(--dx),var(--dy))}}")
    c.save(f"campus-{th}.svg", f"Isometric campus for {NAME}: one building per project with signs, beacons on live ones, smoke from the test lab and dispatch trucks on the road.")

links = " · ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Illustrative: an isometric campus, one building per project. Daylight and lit-up night follow your GitHub theme. Built by scripts/gen_isometric.py -->

<p align="center">{pic(F, "campus", f"Isometric campus for {NAME}")}</p>

**Visit a building:** {links}

<sub>Every building is a project, every lit window a shift it runs. Directions: <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}">linkedin</a></sub>
""")
print("ok")
