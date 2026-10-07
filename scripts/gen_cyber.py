"""Cyberpunk profile: chamfered HUD frames, glitch type, a netrunner ID, a breach-protocol grid and projects as quickhacks.
Run: python scripts/gen_cyber.py [photo]"""
import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, photo_grid
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short

F = "cyber"
COND = "'Rajdhani', 'Bahnschrift', 'Arial Narrow', 'Roboto Condensed', Arial, sans-serif"
MONO = "'Share Tech Mono', 'Consolas', 'Courier New', monospace"
JP = "'Yu Gothic', 'MS Gothic', 'Noto Sans JP', sans-serif"
THEMES = {"dark": dict(bg="#07070D", panel="#0E0E1A", y="#FCEE0A", c="#00F0FF", r="#FF003C", ink="#E8F7FF", soft="#6E7B91"),
          "light": dict(bg="#FCEE0A", panel="#FFF8A8", y="#0A0A0A", c="#007A8A", r="#D1002F", ink="#0A0A0A", soft="#5A5A2A")}
photo = photo_grid(F, 48, sys.argv[1] if len(sys.argv) > 1 else None)


def chamfer(x, y, w, h, k=18):
    return f"M{x + k},{y} H{x + w} V{y + h - k} L{x + w - k},{y + h} H{x} V{y + k} Z"


for th, t in THEMES.items():
    rnd = random.Random(2077)
    # ID card
    c = Canvas(F, t, 1200, 620)
    c.add(f'<rect width="1200" height="620" fill="{t["bg"]}"/>')
    c.add("".join(f'<line x1="0" x2="1200" y1="{y}" y2="{y}" stroke="{t["c"]}" stroke-opacity=".05"/>' for y in range(0, 620, 4)))
    c.add(f'<path d="{chamfer(30, 30, 1140, 560, 28)}" fill="{t["panel"]}" stroke="{t["y"]}" stroke-width="2"/>')
    c.add(f'<rect x="30" y="30" width="300" height="34" fill="{t["y"]}"/>')
    c.text(44, 54, "NETRUNNER ID // VERIFIED", 18, t["bg"], COND, 700, extra='letter-spacing="2"')
    c.text(1150, 56, "クリシュナ・ラジュ", 20, t["r"], JP, 700, "end")
    # portrait with scanline glitch slices
    px0, py0, cell = 60, 96, 9
    c.add(f'<path d="{chamfer(50, 86, 450, 460, 20)}" fill="{t["bg"]}" stroke="{t["c"]}" stroke-width="1.5"/>')
    rects = []
    for r, row in enumerate(photo):
        for q, ch in enumerate(row):
            if ch != "." and (int(ch) > 1 if th == "dark" else int(ch) < 8):
                v = int(ch)
                op = v / 9 if th == "dark" else (9 - v) / 9
                rects.append(f'<rect x="{px0 + 14 + q * cell}" y="{py0 + r * cell}" width="{cell - 2}" height="{cell - 2}" opacity="{op:.2f}"/>')
    c.add(f'<g fill="{t["c"]}">{"".join(rects)}</g>')
    for i in range(3):
        y = 160 + i * 120
        c.add(f'<rect class="slice s{i}" x="60" y="{y}" width="430" height="{10 + i * 6}" fill="{t["r"]}" opacity=".55"/>')
    # glitch name
    for dx, col, cls in [(-3, t["c"], "ga"), (3, t["r"], "gb"), (0, t["ink"], "")]:
        c.text(540 + dx, 150, "KRISHNA RAJU S", 64, col, COND, 700, extra=f'class="{cls}" letter-spacing="2"')
    fields = [("HANDLE", "KRISH-exe-29"), ("CLASS", "Techie · Electrical & Electronics"), ("AFFILIATION", "Indo Tech Transformers · Digitalisation"),
              ("STREET CRED", "#7 of 1500+ · NEC, IIT Bombay"), ("CYBERWARE", "Chai Engine Mk.II · Ohm/Git dual core"),
              ("RECORD", "1 patent filed · 9 apps in production"), ("BOUNTY", "none. clean record.")]
    for i, (k, v) in enumerate(fields):
        y = 210 + i * 46
        c.text(540, y, k, 15, t["y"], COND, 700, extra='letter-spacing="3"')
        c.text(700, y, v, 20, t["ink"], MONO)
        c.add(f'<line x1="540" x2="1140" y1="{y + 14}" y2="{y + 14}" stroke="{t["c"]}" stroke-opacity=".25"/>')
    bars = "".join(f'<rect x="{540 + i * 7}" y="540" width="{rnd.choice([2, 3, 5])}" height="36" fill="{t["ink"]}"/>' for i in range(60))
    c.add(bars)
    c.text(980, 566, "SN 2004-KRS-0007", 16, t["soft"], MONO)
    c.css.append(".ga{animation:ga 3s steps(1) infinite}.gb{animation:gb 3s steps(1) infinite}"
                 "@keyframes ga{0%,92%{transform:none}93%{transform:translate(-8px,2px)}96%{transform:translate(5px,-2px)}}"
                 "@keyframes gb{0%,92%{transform:none}94%{transform:translate(9px,-3px)}97%{transform:translate(-4px,2px)}}"
                 ".slice{opacity:0;animation:sl 2.6s steps(1) infinite}.s1{animation-delay:.9s}.s2{animation-delay:1.7s}"
                 "@keyframes sl{0%,85%{opacity:0;transform:none}86%{opacity:.6;transform:translateX(18px)}90%{opacity:.4;transform:translateX(-12px)}94%{opacity:0}}")
    c.save(f"id-{th}.svg", f"Netrunner ID for {NAME}: class Techie, affiliation Indo Tech Transformers, street cred rank 7 of 1500+, record 1 patent filed and 9 apps in production, bounty none.")

    # breach protocol + quickhacks
    c = Canvas(F, t, 1200, 680)
    c.add(f'<rect width="1200" height="680" fill="{t["bg"]}"/>')
    c.add(f'<path d="{chamfer(30, 30, 520, 620, 24)}" fill="{t["panel"]}" stroke="{t["c"]}" stroke-width="2"/>')
    c.text(54, 74, "BREACH PROTOCOL", 28, t["y"], COND, 700, extra='letter-spacing="3"')
    c.text(54, 100, "BUFFER: AUTOMATE → TEST → SHIP", 14, t["soft"], MONO)
    codes = ["1C", "55", "BD", "E9", "7A", "FF"]
    grid = [[rnd.choice(codes) for _ in range(6)] for _ in range(6)]
    path = [(0, 0), (3, 0), (3, 4), (1, 4), (1, 2), (5, 2)]
    for j, (col, row) in enumerate(path):
        grid[row][col] = ["E9", "1C", "55", "BD", "7A", "FF"][j]
    for row in range(6):
        for col in range(6):
            x, y = 84 + col * 72, 150 + row * 72
            c.text(x, y, grid[row][col], 26, t["ink"], MONO, 700, "middle")
    for j, (col, row) in enumerate(path):
        x, y = 84 + col * 72, 150 + row * 72
        c.add(f'<rect class="hit" style="animation-delay:{j * .5:.1f}s" x="{x - 28}" y="{y - 32}" width="56" height="44" fill="none" stroke="{t["y"]}" stroke-width="3"/>')
    c.text(54, 620, "▶ DAEMONS UPLOADED: 10/10", 18, t["c"], COND, 700, extra='letter-spacing="2"')
    c.add(f'<path d="{chamfer(580, 30, 590, 620, 24)}" fill="{t["panel"]}" stroke="{t["y"]}" stroke-width="2"/>')
    c.text(604, 74, "QUICKHACKS // SHIPPED", 28, t["y"], COND, 700, extra='letter-spacing="3"')
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        y = 120 + i * 52
        c.add(f'<rect x="604" y="{y - 22}" width="542" height="44" fill="{t["bg"]}" opacity=".6"/><rect x="604" y="{y - 22}" width="4" height="44" fill="{t["r"] if status in ("PRODUCTION", "LIVE") else t["c"]}"/>')
        c.text(620, y - 2, short(name).upper(), 18, t["ink"], COND, 700, extra='letter-spacing="1"')
        c.text(620, y + 16, impact, 12, t["soft"], MONO)
        c.text(1132, y + 6, f"RAM {2 + i % 5}", 14, t["y"], MONO, 700, "end")
    c.css.append(".hit{opacity:0;animation:ht 4s steps(1) infinite}@keyframes ht{0%{opacity:0}2%,100%{opacity:1}}")
    c.save(f"breach-{th}.svg", "Breach protocol grid with the buffer automate, test, ship; and quickhacks shipped: " + "; ".join(f"{p[1]}, {p[5]}" for p in PROJECTS))

    # jack in
    c = Canvas(F, t, 1200, 240)
    c.add(f'<rect width="1200" height="240" fill="{t["bg"]}"/><path d="{chamfer(30, 20, 1140, 200, 26)}" fill="{t["y"]}"/>')
    c.text(70, 110, "JACK IN →", 64, t["bg"], COND, 700, extra='letter-spacing="4"')
    c.text(70, 170, EMAIL.upper(), 26, t["bg"], MONO, 700)
    c.text(1130, 110, "NO CORPO TEMPLATES.", 22, t["bg"], COND, 700, "end", 'letter-spacing="3"')
    c.text(1130, 145, "ONLY CUSTOM CHROME.", 22, t["bg"], COND, 700, "end", 'letter-spacing="3"')
    c.save(f"jackin-{th}.svg", f"Jack in: {EMAIL}")

links = " · ".join(f"[{short(p[1]).upper()}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Cyberpunk HUD: midnight neon in dark mode, the yellow menu look in light mode. Built by scripts/gen_cyber.py -->

<p align="center">{pic(F, "id", f"Netrunner ID for {NAME}")}</p>
<p align="center">{pic(F, "breach", "Breach protocol and quickhacks")}</p>
<p align="center"><code>{links}</code></p>
<p align="center"><a href="mailto:{EMAIL}">{pic(F, "jackin", f"Jack in: {EMAIL}")}</a></p>
<p align="center"><sub><a href="{LINKEDIN}">LINKEDIN // UPLINK</a></sub></p>
""")
print("ok")
