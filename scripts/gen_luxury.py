"""Luxury / premium profile: ivory and noir, hairline gold, thin serif capitals, a watch dial of skills, the collection.
Run: python scripts/gen_luxury.py [photo]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, photo_grid
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, CGPA, short

F = "luxury"
DIDOT = "'Didot', 'Bodoni 72', 'Bodoni MT', 'Playfair Display', 'Times New Roman', serif"
THIN = "'Helvetica Neue', 'Segoe UI Light', 'Segoe UI', Arial, sans-serif"
THEMES = {"light": dict(bg="#F7F3EC", ink="#141210", soft="#8A8175", gold="#B08D57", line="#D9CFBF"),
          "dark": dict(bg="#0E0D0C", ink="#F2ECE2", soft="#8F8679", gold="#C9A66B", line="#2E2A25")}
photo = photo_grid(F, 60, sys.argv[1] if len(sys.argv) > 1 else None)

for th, t in THEMES.items():
    # maison hero
    c = Canvas(F, t, 1200, 720)
    c.add(f'<rect width="1200" height="720" fill="{t["bg"]}"/>')
    c.text(600, 70, "MAISON · KRS", 13, t["soft"], THIN, 300, "middle", 'letter-spacing="6"')
    c.add(f'<line x1="540" x2="660" y1="88" y2="88" stroke="{t["gold"]}" stroke-width=".8"/>')
    cx, cy = 600, 300
    c.add(f'<circle cx="{cx}" cy="{cy}" r="170" fill="none" stroke="{t["gold"]}" stroke-width=".8"/><circle cx="{cx}" cy="{cy}" r="160" fill="none" stroke="{t["gold"]}" stroke-width="2"/>')
    cell = 5
    dots = []
    for r, row in enumerate(photo):
        for q, ch in enumerate(row):
            if ch != ".":
                v = (9 - int(ch)) / 9 if th == "light" else int(ch) / 9
                if v > .1:
                    dots.append(f'<circle cx="{cx - 30 * cell + q * cell:.1f}" cy="{cy - 30 * cell + 8 + r * cell:.1f}" r="{cell * .48 * v ** .7:.2f}"/>')
    c.add(f'<clipPath id="ring"><circle cx="{cx}" cy="{cy}" r="156"/></clipPath><g clip-path="url(#ring)" fill="{t["ink"]}">{"".join(dots)}</g>')
    c.add(f'<g class="hand" style="transform-origin:{cx}px {cy}px"><circle cx="{cx}" cy="{cy - 165}" r="3" fill="{t["gold"]}"/></g>')
    c.text(600, 540, "KRISHNA RAJU S", 54, t["ink"], DIDOT, 400, "middle", 'letter-spacing="12"')
    c.text(600, 586, "Haute Ingénierie", 24, t["gold"], DIDOT, 400, "middle", 'font-style="italic"')
    c.text(600, 640, "PRECISION ENGINEERING, HANDCRAFTED IN CHENNAI SINCE 2004", 12, t["soft"], THIN, 300, "middle", 'letter-spacing="5"')
    c.css.append(".hand{animation:hd 60s linear infinite}@keyframes hd{to{transform:rotate(360deg)}}")
    c.save(f"maison-{th}.svg", f"Maison KRS. {NAME}, Haute Ingénierie: precision engineering, handcrafted in Chennai since 2004.")

    # the movement: a watch dial whose complications are skills
    c = Canvas(F, t, 1200, 640)
    c.add(f'<rect width="1200" height="640" fill="{t["bg"]}"/>')
    cx, cy, R = 330, 320, 250
    c.add(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{t["gold"]}" stroke-width="1.5"/><circle cx="{cx}" cy="{cy}" r="{R - 14}" fill="none" stroke="{t["line"]}"/>')
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = R - 14 - (16 if i % 5 == 0 else 7)
        c.add(f'<line x1="{cx + (R - 14) * math.cos(a):.1f}" y1="{cy + (R - 14) * math.sin(a):.1f}" x2="{cx + r1 * math.cos(a):.1f}" y2="{cy + r1 * math.sin(a):.1f}" '
              f'stroke="{t["ink"]}" stroke-width="{1.6 if i % 5 == 0 else .6}"/>')
    subs = [(cx, cy - 110, "POWER", .92), (cx - 110, cy + 30, "CODE", .9), (cx + 110, cy + 30, "IoT", .8)]
    for sx, sy, lab, v in subs:
        c.add(f'<circle cx="{sx}" cy="{sy}" r="58" fill="none" stroke="{t["line"]}"/>'
              f'<path d="M{sx},{sy} L{sx + 46 * math.sin(v * 2 * math.pi):.1f},{sy - 46 * math.cos(v * 2 * math.pi):.1f}" stroke="{t["gold"]}" stroke-width="1.6"/>'
              f'<circle cx="{sx}" cy="{sy}" r="3" fill="{t["gold"]}"/>')
        c.text(sx, sy + 34, lab, 10, t["soft"], THIN, 400, "middle", 'letter-spacing="3"')
    c.add(f'<rect x="{cx - 26}" y="{cy + 130}" width="52" height="28" fill="none" stroke="{t["gold"]}"/>')
    c.text(cx, cy + 150, CGPA, 14, t["ink"], DIDOT, 400, "middle")
    c.text(cx, cy + 180, "CGPA", 9, t["soft"], THIN, 400, "middle", 'letter-spacing="3"')
    c.add(f'<g class="sec" style="transform-origin:{cx}px {cy}px"><line x1="{cx}" y1="{cy + 30}" x2="{cx}" y2="{cy - R + 40}" stroke="{t["gold"]}" stroke-width="1.2"/></g>'
          f'<circle cx="{cx}" cy="{cy}" r="6" fill="{t["gold"]}"/>')
    c.text(680, 120, "The Movement", 40, t["ink"], DIDOT, 400, extra='font-style="italic"')
    specs = [("Calibre", "Electrical & Electronics, B.E."), ("Complications", "Power · Code · IoT"), ("Jewels", "9 apps in production"),
             ("Power reserve", "Chai, indefinitely"), ("Accuracy", "30 minutes → 30 seconds"), ("Certification", "Patent filed, 2025"), ("Provenance", "St. Joseph's · Chennai")]
    for i, (k, v) in enumerate(specs):
        y = 190 + i * 56
        c.text(680, y, k.upper(), 11, t["soft"], THIN, 400, extra='letter-spacing="4"')
        c.text(680, y + 26, v, 22, t["ink"], DIDOT, 400)
        c.add(f'<line x1="680" x2="1140" y1="{y + 38}" y2="{y + 38}" stroke="{t["line"]}"/>')
    c.css.append(".sec{animation:sc 60s steps(60) infinite}@keyframes sc{to{transform:rotate(360deg)}}")
    c.save(f"movement-{th}.svg", "The movement: calibre electrical and electronics; complications power, code, IoT; 9 apps in production; accuracy 30 minutes to 30 seconds; patent filed.")

    # the collection
    c = Canvas(F, t, 1200, 760)
    c.add(f'<rect width="1200" height="760" fill="{t["bg"]}"/>')
    c.text(600, 80, "The Collection", 44, t["ink"], DIDOT, 400, "middle", 'font-style="italic"')
    c.text(600, 112, "TEN PIECES · EACH MADE TO MEASURE", 11, t["soft"], THIN, 400, "middle", 'letter-spacing="5"')
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        col, row = i % 2, i // 2
        x, y = 80 + col * 540, 160 + row * 116
        c.text(x, y + 10, f"N° {i + 1:02d}", 12, t["gold"], THIN, 400, extra='letter-spacing="3"')
        c.text(x + 80, y + 12, short(name), 26, t["ink"], DIDOT, 400)
        c.text(x + 80, y + 42, hook, 15, t["soft"], DIDOT, 400, extra='font-style="italic"')
        c.text(x + 80, y + 66, status.upper(), 10, t["gold"], THIN, 400, extra='letter-spacing="4"')
        c.add(f'<line x1="{x}" x2="{x + 480}" y1="{y + 88}" y2="{y + 88}" stroke="{t["line"]}"/>')
    c.save(f"collection-{th}.svg", "The collection: " + "; ".join(f"No. {i + 1} {p[1]}, {p[4]}" for i, p in enumerate(PROJECTS)))

    # private appointment
    c = Canvas(F, t, 1200, 260)
    c.add(f'<rect width="1200" height="260" fill="{t["ink"]}"/>')
    c.text(600, 100, "By private appointment", 34, t["bg"], DIDOT, 400, "middle", 'font-style="italic"')
    c.add(f'<line x1="540" x2="660" y1="128" y2="128" stroke="{t["gold"]}"/>')
    c.text(600, 176, EMAIL.upper(), 16, t["gold"], THIN, 400, "middle", 'letter-spacing="6"')
    c.save(f"appointment-{th}.svg", f"By private appointment: {EMAIL}")

links = " · ".join(f"[N° {i + 1:02d} {short(p[1])}]({p[3]})" for i, p in enumerate(PROJECTS) if p[3])
write_readme(f"""
<!-- Luxury / premium: Maison KRS. Ivory by day, noir by night, following your GitHub theme. Built by scripts/gen_luxury.py -->

<p align="center">{pic(F, "maison", f"Maison KRS: {NAME}, Haute Ingénierie")}</p>
<p align="center">{pic(F, "movement", "The movement: a watch dial of skills")}</p>
<p align="center">{pic(F, "collection", "The collection")}</p>
<p align="center"><sub>{links}</sub></p>
<p align="center"><a href="mailto:{EMAIL}">{pic(F, "appointment", "By private appointment")}</a></p>
<p align="center"><sub><a href="{LINKEDIN}">the atelier on LinkedIn</a></sub></p>
""")
print("ok")
