"""Flat design profile: solid colours, simple shapes, zero gradients. Run: python scripts/gen_flat.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, icon, pic, linked, write_readme
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, EXPERIENCE, WINS, short

F = "flat"
HEAD = "'Segoe UI Black', 'Arial Black', 'Helvetica Neue', Arial, sans-serif"
BODY = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
THEMES = {"light": dict(bg="#FFF6EA", ink="#2D3047", soft="#6B6F86", card="#FFFFFF", coral="#FF6B6B", teal="#1ABC9C", sun="#F7C948", blue="#3D7BF7", navy="#2D3047"),
          "dark": dict(bg="#1E2235", ink="#F4F1EA", soft="#A7ABC2", card="#2A2F48", coral="#FF6B6B", teal="#1ABC9C", sun="#F7C948", blue="#5B8FFF", navy="#13162A")}
PAL = ["coral", "teal", "sun", "blue"]

for th, t in THEMES.items():
    # hero: words left, flat illustration right
    c = Canvas(F, t, 1200, 560)
    c.add(f'<rect width="1200" height="560" fill="{t["bg"]}"/>')
    c.add(f'<circle cx="900" cy="290" r="230" fill="{t["sun"]}" opacity=".9"/>',
          f'<path d="M640 470h520v90H640z" fill="{t["teal"]}"/>')
    # transformer
    c.add(f'<g><rect x="760" y="250" width="150" height="160" fill="{t["navy"]}"/>'
          + "".join(f'<rect x="{915 + i * 13}" y="268" width="8" height="124" fill="{t["blue"]}"/>' for i in range(4))
          + "".join(f'<rect x="{782 + i * 44}" y="{200 if i != 1 else 186}" width="18" height="{50 if i != 1 else 64}" fill="{t["card"]}"/>'
                    f'<rect x="{776 + i * 44}" y="{196 if i != 1 else 182}" width="30" height="10" fill="{t["coral"]}"/>' for i in range(3))
          + f'<path class="bolt" d="M845 290l-26 50h24l-12 46 40-60h-26l14-36z" fill="{t["sun"]}"/></g>')
    # laptop with typing code
    c.add(f'<rect x="980" y="330" width="170" height="110" rx="6" fill="{t["navy"]}"/><rect x="992" y="342" width="146" height="86" fill="{t["card"]}"/>'
          f'<path d="M960 440h210l-14 16H974z" fill="{t["ink"]}"/>'
          + "".join(f'<rect class="code" style="animation-delay:{i * .35:.2f}s" x="1002" y="{354 + i * 14}" width="{[90, 60, 110, 70, 50][i]}" height="6" rx="3" '
                    f'fill="{t[PAL[i % 4]]}"/>' for i in range(5)))
    # truck
    c.add(f'<g class="truck">{icon("dispatch", 650, 400, 110, t["coral"], t["blue"], t["navy"])}</g>')
    c.text(70, 150, "HELLO, I'M", 22, t["coral"], HEAD, extra='letter-spacing="4"')
    c.text(66, 230, "Krishna", 92, t["ink"], HEAD, extra='letter-spacing="-3"')
    c.text(66, 316, "Raju S.", 92, t["ink"], HEAD, extra='letter-spacing="-3"')
    c.para(70, 372, "I make factories run on software. Electrical engineer by degree, automator by reflex.", 22, 520, fill=t["soft"], font=BODY)
    c.add(f'<rect x="70" y="440" width="230" height="58" rx="29" fill="{t["coral"]}"/>')
    c.text(185, 477, "Let's build →", 21, "#FFFFFF", HEAD, anchor="middle")
    c.add(f'<rect x="316" y="440" width="200" height="58" rx="29" fill="none" stroke="{t["ink"]}" stroke-width="3"/>')
    c.text(416, 477, "9 apps live", 21, t["ink"], HEAD, anchor="middle")
    c.css.append(".bolt{animation:z 1.6s steps(2) infinite}@keyframes z{50%{opacity:.25}}"
                 ".code{animation:ty 2.4s ease-out infinite;transform-box:fill-box}@keyframes ty{0%{transform:scaleX(0)}40%,100%{transform:scaleX(1)}}"
                 ".truck{animation:tr 1.2s ease-in-out infinite}@keyframes tr{50%{transform:translateY(-3px)}}")
    c.save(f"hero-{th}.svg", f"Hello, I'm {NAME}. I make factories run on software.")

    # stats as flat circles
    c = Canvas(F, t, 1200, 300)
    c.add(f'<rect width="1200" height="300" fill="{t["bg"]}"/>')
    for i, (v, l) in enumerate([("9", "apps in production"), ("128", "tests on dispatch"), ("30s", "was 30 minutes"), ("#7", "of 1500+ colleges")]):
        x = 150 + i * 300
        c.add(f'<circle cx="{x}" cy="120" r="88" fill="{t[PAL[i]]}"/><circle cx="{x + 10}" cy="130" r="88" fill="none" stroke="{t["ink"]}" stroke-width="3" opacity=".15"/>')
        c.text(x, 140, v, 54, "#FFFFFF" if i != 2 else t["navy"], HEAD, anchor="middle")
        c.text(x, 250, l, 19, t["ink"], BODY, 600, "middle")
    c.save(f"stats-{th}.svg", "9 apps in production; 128 tests on dispatch; 30 seconds that used to be 30 minutes; rank 7 of 1500+ colleges")

    # project grid: 10 flat tiles
    c = Canvas(F, t, 1200, 700)
    c.add(f'<rect width="1200" height="700" fill="{t["bg"]}"/>')
    c.text(600, 64, "Things I shipped", 40, t["ink"], HEAD, anchor="middle")
    c.text(600, 98, "flat design, zero fluff. like my code reviews.", 18, t["soft"], BODY, anchor="middle")
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        x, y = 40 + (i % 5) * 228, 130 + (i // 5) * 280
        col = t[PAL[i % 4]]
        c.add(f'<rect x="{x}" y="{y}" width="212" height="262" rx="18" fill="{t["card"]}"/><rect x="{x}" y="{y}" width="212" height="110" rx="18" fill="{col}"/>'
              f'<rect x="{x}" y="{y + 80}" width="212" height="30" fill="{col}"/>')
        c.add(icon(slug, x + 66, y + 15, 80, t["card"], t["navy"], t["ink"] if th == "light" else t["navy"]))
        c.text(x + 16, y + 142, short(name), 18, t["ink"], HEAD)
        c.text(x + 16, y + 164, status.lower(), 13, col if th == "dark" else t["soft"], BODY, 700, extra='letter-spacing="1"')
        c.para(x + 16, y + 192, hook, 14, 184, fill=t["soft"], font=BODY)
    c.save(f"projects-{th}.svg", "Projects: " + "; ".join(f"{p[1]}: {p[4]}" for p in PROJECTS))

    # career as flat stepping stones
    c = Canvas(F, t, 1200, 380)
    c.add(f'<rect width="1200" height="380" fill="{t["bg"]}"/>')
    c.text(600, 60, "The route so far", 36, t["ink"], HEAD, anchor="middle")
    for i, (org, role, when, where, what, win) in enumerate(reversed(EXPERIENCE)):
        x, h = 60 + i * 226, 70 + i * 34
        c.add(f'<rect x="{x}" y="{340 - h}" width="200" height="{h}" fill="{t[PAL[i % 4]]}"/>')
        c.text(x + 100, 330 - h - 76, when, 14, t["soft"], BODY, 700, "middle")
        c.para(x + 100, 330 - h - 50, org, 17, 190, fill=t["ink"], font=HEAD, anchor="middle")
    c.add(f'<circle class="hop" cx="{60 + 4 * 226 + 100}" cy="120" r="14" fill="{t["coral"]}"/>')
    c.css.append(".hop{animation:hop 1s ease-in-out infinite}@keyframes hop{50%{transform:translateY(-14px)}}")
    c.save(f"route-{th}.svg", "Career: " + "; ".join(f"{e[2]} {e[0]}" for e in reversed(EXPERIENCE)))

    # footer
    c = Canvas(F, t, 1200, 260)
    c.add(f'<rect width="1200" height="260" fill="{t["navy"]}"/><circle cx="1100" cy="40" r="140" fill="{t["coral"]}"/><circle cx="90" cy="250" r="110" fill="{t["teal"]}"/>')
    c.text(600, 110, "Got a manual process?", 40, "#FFFFFF", HEAD, anchor="middle")
    c.text(600, 160, "Flatten it. Send it to me.", 26, t["sun"], HEAD, anchor="middle")
    c.text(600, 208, EMAIL, 20, "#FFFFFF", BODY, 600, "middle")
    c.save(f"footer-{th}.svg", f"Got a manual process? Flatten it. Send it to me. {EMAIL}")

links = " · ".join(f"[{p[1]}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Flat design: solid colours, simple shapes, no gradients. Light and dark versions follow your GitHub theme. Built by scripts/gen_flat.py -->

<p align="center">{pic(F, "hero", f"Hello, I'm {NAME}. I make factories run on software.")}</p>

<p align="center">
  <a href="mailto:{EMAIL}"><img src="https://img.shields.io/badge/Email-FF6B6B?style=flat-square&logo=gmail&logoColor=white" alt="Email"/></a>
  <a href="{LINKEDIN}"><img src="https://img.shields.io/badge/LinkedIn-3D7BF7?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
  <a href="https://krishna-ittl.github.io/Candidate-Screener/"><img src="https://img.shields.io/badge/Try_Job_Lens-1ABC9C?style=flat-square&logo=githubpages&logoColor=white" alt="Job Lens"/></a>
</p>

<p align="center">{pic(F, "stats", "9 apps in production; 128 tests on dispatch; 30 seconds that used to be 30 minutes; rank 7 of 1500+")}</p>
<p align="center">{pic(F, "projects", "Things I shipped")}</p>
<p align="center"><sub>open: {links}</sub></p>
<p align="center">{pic(F, "route", "The route so far")}</p>
<p align="center">{pic(F, "footer", f"Got a manual process? Send it to me. {EMAIL}")}</p>
""")
print("ok")
