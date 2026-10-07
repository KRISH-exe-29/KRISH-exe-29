"""Scroll-driven / scrollytelling profile: one tall page where current flows down a power line as you scroll,
Generation → Transmission → Transformation → Distribution → Load. Run: python scripts/gen_scrolly.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, SANS, MONO
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, COLLEGE, CGPA, short

F = "scrolly"
SERIF = "Georgia, 'Times New Roman', serif"
THEMES = {"dark": dict(bg="#06080F", ink="#EEF2FA", soft="#7F8AA3", wire="#28324A", live="#FFD34E", acc="#4CC9F0", hot="#FF6B6B"),
          "light": dict(bg="#FBFAF6", ink="#16181D", soft="#6B7180", wire="#D9DCE3", live="#E8A200", acc="#0077B6", hot="#D62839")}
SECTIONS = [
    ("GENERATION", "2004 – 2022", "Born in Chennai. Ohm's Law before algebra, probably.", [("2022", f"{COLLEGE}", f"B.E. Electrical & Electronics begins · CGPA {CGPA}")]),
    ("TRANSMISSION", "2023 – 2024", "Carrying the current through real industry.", [("2023", "Southern Railway", "electrical documentation, inspection"),
                                                                                       ("2024", "Mettur Thermal Power Plant", "megawatts up close"),
                                                                                       ("2024", "Inovate Technologies", "first production deploy")]),
    ("TRANSFORMATION", "2025", "Where the voltage steps up.", [("Feb", "NEC #7 of 1500+ · IIT Bombay", "plus runner-up at Fish Tank"),
                                                                 ("Jun", "Bühler India", "30 minutes of paperwork → 30 seconds"),
                                                                 ("Aug", "Patent filed", "street lights that follow the car")]),
    ("DISTRIBUTION", "2026 →", "Indo Tech Transformers. The current reaches every department.", []),
    ("LOAD", "now", "The factory floor runs on it.", []),
]

for th, t in THEMES.items():
    H = 3300
    c = Canvas(F, t, 1200, H)
    c.add(f'<rect width="1200" height="{H}" fill="{t["bg"]}"/>')
    c.text(600, 90, "SCROLL SLOWLY. THE CURRENT IS FLOWING.", 16, t["soft"], MONO, 700, "middle", 'letter-spacing="3"')
    c.text(600, 160, NAME, 60, t["ink"], SANS, 800, "middle", 'letter-spacing="-2"')
    c.text(600, 200, "a life story, wired as a power grid", 20, t["soft"], SERIF, anchor="middle", extra='font-style="italic"')
    # generator symbol
    c.add(f'<circle cx="600" cy="300" r="56" fill="none" stroke="{t["live"]}" stroke-width="5"/>'
          f'<path d="M560 300 q20 -34 40 0 t40 0" fill="none" stroke="{t["live"]}" stroke-width="5"/>')
    spine = [(600, 356)]
    y = 420
    nodes = []
    for si, (name, when, line, events) in enumerate(SECTIONS):
        nodes.append(("section", y, name, when, line))
        y += 150
        for ei, ev in enumerate(events):
            nodes.append(("event", y, ei, *ev))
            y += 150
        if name == "TRANSFORMATION":
            nodes.append(("transformer", y))
            y += 200
        if name == "DISTRIBUTION":
            nodes.append(("branches", y))
            y += 440
        y += 40
    end = y
    # spine wire + flowing current
    c.add(f'<line x1="600" x2="600" y1="356" y2="{end}" stroke="{t["wire"]}" stroke-width="10" stroke-linecap="round"/>'
          f'<line class="flow" x1="600" x2="600" y1="356" y2="{end}" stroke="{t["live"]}" stroke-width="4" stroke-dasharray="6 26" stroke-linecap="round"/>')
    for kind, ny, *rest in nodes:
        if kind == "section":
            name, when, line = rest
            c.add(f'<rect x="420" y="{ny - 34}" width="360" height="92" rx="12" fill="{t["bg"]}" stroke="{t["live"]}" stroke-width="2"/>')
            c.text(600, ny, name, 26, t["live"], MONO, 700, "middle", 'letter-spacing="6"')
            c.text(600, ny + 24, when, 14, t["soft"], MONO, anchor="middle")
            c.text(600, ny + 92, line, 19, t["ink"], SERIF, anchor="middle", extra='font-style="italic"')
        elif kind == "event":
            ei, yr, title, note = rest
            side = -1 if ei % 2 == 0 else 1
            x2 = 600 + side * 120
            c.add(f'<line x1="600" x2="{x2}" y1="{ny}" y2="{ny}" stroke="{t["wire"]}" stroke-width="6"/>'
                  f'<line class="flow" x1="600" x2="{x2}" y1="{ny}" y2="{ny}" stroke="{t["acc"]}" stroke-width="3" stroke-dasharray="4 14"/>'
                  f'<circle cx="{x2}" cy="{ny}" r="12" fill="{t["acc"]}"/>')
            anchor = "end" if side < 0 else "start"
            tx = x2 + side * 26
            c.text(tx, ny - 14, yr, 15, t["acc"], MONO, 700, anchor)
            c.text(tx, ny + 12, title, 24, t["ink"], SANS, 700, anchor)
            c.text(tx, ny + 38, note, 16, t["soft"], SANS, 400, anchor)
        elif kind == "transformer":
            cy = ny + 70
            coil = lambda x, d: f"M{x},{cy - 60}" + "".join(f" q{d * 22},7.5 0,15" for _ in range(8))
            c.add(f'<rect x="560" y="{cy - 80}" width="80" height="160" fill="{t["bg"]}"/>'
                  f'<path d="{coil(570, -1)}" fill="none" stroke="{t["live"]}" stroke-width="4"/><path d="{coil(630, 1)}" fill="none" stroke="{t["hot"]}" stroke-width="4"/>'
                  f'<line x1="595" x2="595" y1="{cy - 66}" y2="{cy + 66}" stroke="{t["ink"]}" stroke-width="3"/><line x1="605" x2="605" y1="{cy - 66}" y2="{cy + 66}" stroke="{t["ink"]}" stroke-width="3"/>')
            c.text(500, cy - 6, "engineer", 18, t["live"], MONO, 700, "end")
            c.text(500, cy + 18, "primary", 13, t["soft"], MONO, anchor="end")
            c.text(700, cy - 6, "builder", 18, t["hot"], MONO, 700)
            c.text(700, cy + 18, "secondary, stepped up", 13, t["soft"], MONO)
        elif kind == "branches":
            top = ny
            boxes = []
            for k, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
                col, row = k % 5, k // 5
                bx, by = 140 + col * 230, top + 160 + row * 190
                c.add(f'<path d="M600,{top} C600,{top + 60} {bx},{by - 100} {bx},{by - 30}" fill="none" stroke="{t["wire"]}" stroke-width="4"/>'
                      f'<path class="flow" d="M600,{top} C600,{top + 60} {bx},{by - 100} {bx},{by - 30}" fill="none" stroke="{t["acc"]}" stroke-width="2.5" stroke-dasharray="4 14"/>')
                boxes.append((bx, by, name, impact, status))
            for bx, by, name, impact, status in boxes:  # boxes after all wires, so wires pass behind them
                c.add(f'<rect x="{bx - 98}" y="{by - 30}" width="196" height="96" rx="12" fill="{t["bg"]}" stroke="{t["acc"]}" stroke-width="2"/>')
                c.text(bx, by + 2, short(name), 17, t["ink"], SANS, 700, "middle")
                c.text(bx, by + 26, impact.split(" · ")[0], 13, t["soft"], SANS, anchor="middle")
                c.text(bx, by + 50, status.lower(), 12, t["acc"], MONO, 700, "middle")
    # load: the factory lights up
    fy = end - 10
    c.add(f'<path d="M260 {fy + 260} V{fy + 120} L360 {fy + 70} V{fy + 120} L460 {fy + 70} V{fy + 120} L560 {fy + 70} V{fy + 120} L660 {fy + 70} V{fy + 120} L760 {fy + 70} V{fy + 120} L940 {fy + 60} V{fy + 260}Z" '
          f'fill="{t["wire"]}"/>' + "".join(f'<rect class="lit" style="animation-delay:{.15 * k:.2f}s" x="{290 + (k % 10) * 62}" y="{fy + 140 + (k // 10) * 50}" width="36" height="28" fill="{t["live"]}"/>' for k in range(20)))
    c.text(600, fy + 330, "THE PLANT RUNS ON IT.", 44, t["ink"], SANS, 800, "middle", 'letter-spacing="-1"')
    c.text(600, fy + 372, "nine apps · every shift · keep the current flowing → " + EMAIL, 17, t["soft"], MONO, anchor="middle")
    c.h = fy + 420
    c.parts[0] = f'<rect width="1200" height="{c.h}" fill="{t["bg"]}"/>'
    c.css.append(".flow{animation:fl 1.2s linear infinite}@keyframes fl{to{stroke-dashoffset:-32}}"
                 ".lit{animation:lt 3s ease-in-out infinite}@keyframes lt{0%,20%{opacity:.15}40%,100%{opacity:1}}")
    c.save(f"grid-{th}.svg", f"{NAME}: a life story wired as a power grid. Generation: born in Chennai, B.E. at {COLLEGE}. Transmission: Southern Railway, Mettur, Inovate. "
                             "Transformation: NEC rank 7, Bühler 30 minutes to 30 seconds, patent filed. Distribution: ten projects at Indo Tech Transformers. Load: the plant runs on it.")

links = " · ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Scroll-driven / scrollytelling: one tall page; scrolling follows the current from generation to load. Built by scripts/gen_scrolly.py -->

<p align="center">{pic(F, "grid", f"{NAME}: a life story wired as a power grid")}</p>

<p align="center"><sub>end of line · {links}<br/><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}">linkedin</a></sub></p>
""")
print("ok")
