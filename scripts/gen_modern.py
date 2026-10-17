"""Modern / contemporary product-launch profile: big type, spotlight beam, a live dashboard mock, feature grid, changelog.
Run: python scripts/gen_modern.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, icon, pic, write_readme, SANS, MONO
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short

F = "modern"
THEMES = {"dark": dict(bg="#08090A", ink="#F7F8F8", soft="#8A8F98", line="#23252A", card="#0F1011", beam="#5E6AD2", hi="#B4BCFF", g2="#E2E4FF"),
          "light": dict(bg="#FFFFFF", ink="#0A0A0B", soft="#6B6F76", line="#E6E8EB", card="#FAFAFB", beam="#5E6AD2", hi="#3C46B8", g2="#0A0A0B")}

for th, t in THEMES.items():
    c = Canvas(F, t, 1200, 980)
    c.defs.append(f'<radialGradient id="beam" cx=".5" cy="0" r=".7"><stop offset="0" stop-color="{t["beam"]}" stop-opacity="{.55 if th == "dark" else .25}"/>'
                  f'<stop offset="1" stop-color="{t["beam"]}" stop-opacity="0"/></radialGradient>'
                  f'<linearGradient id="head" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["g2"]}"/><stop offset="1" stop-color="{t["hi"]}"/></linearGradient>'
                  f'<pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" stroke="{t["line"]}"/></pattern>'
                  f'<linearGradient id="fadeg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["bg"]}" stop-opacity="0"/><stop offset=".7" stop-color="{t["bg"]}"/></linearGradient>'
                  f'<filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="24" stdDeviation="30" flood-color="#000" flood-opacity="{.6 if th == "dark" else .12}"/></filter>')
    c.add(f'<rect width="1200" height="980" fill="{t["bg"]}"/><rect width="1200" height="620" fill="url(#grid)"/><rect width="1200" height="620" fill="url(#fadeg)"/>',
          f'<ellipse class="beam" cx="600" cy="0" rx="700" ry="520" fill="url(#beam)"/>')
    # nav
    c.text(60, 52, "◆ krishna", 18, t["ink"], SANS, 600)
    for i, n in enumerate(["Work", "Career", "Changelog", "Contact"]):
        c.text(760 + i * 100, 52, n, 15, t["soft"], SANS, 500)
    # pill + headline
    c.add(f'<rect x="440" y="104" width="320" height="34" rx="17" fill="{t["card"]}" stroke="{t["line"]}"/>')
    c.text(600, 126, "✦ New: KioskSentinel shipped  →", 14, t["soft"], SANS, 500, "middle")
    c.text(600, 230, "Software for the", 82, "url(#head)", SANS, 700, "middle", 'letter-spacing="-3.5"')
    c.text(600, 318, "factory floor.", 82, "url(#head)", SANS, 700, "middle", 'letter-spacing="-3.5"')
    c.text(600, 372, "Krishna Raju S is an electrical engineer who ships the tools a transformer plant runs on.", 20, t["soft"], SANS, 400, "middle")
    c.text(600, 400, "Dispatch, testing, hiring, attendance. Built, tested, in production.", 20, t["soft"], SANS, 400, "middle")
    c.add(f'<rect x="462" y="430" width="140" height="44" rx="10" fill="{t["ink"]}"/><rect x="614" y="430" width="124" height="44" rx="10" fill="{t["card"]}" stroke="{t["line"]}"/>')
    c.text(532, 458, "Get in touch", 15, t["bg"], SANS, 600, "middle")
    c.text(676, 458, "See work ↓", 15, t["ink"], SANS, 500, "middle")
    # product mock: dispatch dashboard
    x0, y0 = 150, 520
    c.add(f'<g filter="url(#sh)"><rect x="{x0}" y="{y0}" width="900" height="430" rx="14" fill="{t["card"]}" stroke="{t["line"]}"/></g>')
    c.add("".join(f'<circle cx="{x0 + 24 + i * 18}" cy="{y0 + 22}" r="5" fill="{t["line"]}"/>' for i in range(3)))
    c.add(f'<line x1="{x0}" x2="{x0 + 900}" y1="{y0 + 44}" y2="{y0 + 44}" stroke="{t["line"]}"/>')
    c.text(x0 + 450, y0 + 27, "dispatch dashboard  ·  mock-up with illustrative numbers", 12, t["soft"], MONO, anchor="middle")
    c.add(f'<rect x="{x0}" y="{y0 + 44}" width="170" height="386" fill="{t["bg"]}" opacity=".5"/>')
    for i, n in enumerate(["Dashboard", "Work orders", "Packing", "Loading", "Vehicles", "Calendar", "System health"]):
        if i == 0:
            c.add(f'<rect x="{x0 + 10}" y="{y0 + 62}" width="150" height="30" rx="6" fill="{t["line"]}"/>')
        c.text(x0 + 24, y0 + 82 + i * 40, n, 13, t["ink"] if i == 0 else t["soft"], SANS, 500)
    kp = [("Work orders", "142"), ("Packed", "1,288"), ("Dispatched", "97%"), ("Escalations", "0")]
    for i, (k, v) in enumerate(kp):
        kx = x0 + 190 + i * 176
        c.add(f'<rect x="{kx}" y="{y0 + 64}" width="164" height="84" rx="10" fill="{t["bg"]}" stroke="{t["line"]}"/>')
        c.text(kx + 14, y0 + 90, k, 12, t["soft"], SANS, 500)
        c.text(kx + 14, y0 + 128, v, 28, t["ink"], SANS, 600)
    c.add(f'<rect x="{x0 + 190}" y="{y0 + 164}" width="692" height="248" rx="10" fill="{t["bg"]}" stroke="{t["line"]}"/>')
    c.text(x0 + 206, y0 + 190, "Dispatches per week", 13, t["ink"], SANS, 600)
    for i, v in enumerate([.42, .55, .5, .68, .61, .74, .7, .82, .78, .9, .86, .95]):
        bx = x0 + 214 + i * 55
        h = 170 * v
        c.add(f'<rect class="bar" style="animation-delay:{.3 + i * .06:.2f}s" x="{bx}" y="{y0 + 392 - h:.0f}" width="34" height="{h:.0f}" rx="4" '
              f'fill="{t["beam"]}" opacity="{.45 + v * .55:.2f}"/>')
    
    c.css.append(".bar{transform-box:fill-box;transform-origin:bottom;animation:gr 1s cubic-bezier(.2,.8,.2,1) backwards}@keyframes gr{from{transform:scaleY(0)}}"
                 ".beam{animation:bm 6s ease-in-out infinite alternate}@keyframes bm{to{opacity:.6;transform:translateX(30px)}}")
    c.save(f"hero-{th}.svg", f"Software for the factory floor. {NAME} ships the tools a transformer plant runs on: dispatch, testing, hiring, attendance.")

    # features grid
    c = Canvas(F, t, 1200, 720)
    c.add(f'<rect width="1200" height="720" fill="{t["bg"]}"/>')
    c.text(60, 70, "Built for real shifts.", 44, t["ink"], SANS, 700, extra='letter-spacing="-1.5"')
    c.text(60, 106, "Not demo day. Ten things in the wild, each solving one stubborn problem.", 18, t["soft"], SANS)
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        x, y = 60 + (i % 5) * 220, 150 + (i // 5) * 280
        c.add(f'<rect x="{x}" y="{y}" width="204" height="256" rx="14" fill="{t["card"]}" stroke="{t["line"]}"/>'
              f'<rect x="{x + 18}" y="{y + 18}" width="44" height="44" rx="10" fill="{t["bg"]}" stroke="{t["line"]}"/>'
              + icon(slug, x + 26, y + 26, 28, t["ink"], t["beam"], t["soft"]))
        c.text(x + 18, y + 96, short(name), 17, t["ink"], SANS, 600)
        c.text(x + 18, y + 118, status.lower(), 12, t["hi"], MONO)
        c.para(x + 18, y + 148, hook, 14, 172, fill=t["soft"], font=SANS)
        c.text(x + 18, y + 234, impact.split(" · ")[0], 12, t["ink"], MONO)
    c.save(f"features-{th}.svg", "Projects: " + "; ".join(f"{p[1]}: {p[4]}" for p in PROJECTS))

    # changelog
    log = [("v2026.10", "KioskSentinel", "Attendance kiosks that survive power cuts and pranksters."),
           ("v2026.09", "Dispatch · Live", "Calendar, email escalations, server-down alerts. 128 tests."),
           ("v2026.03", "Fastener standard", "Pitched to the CEO. Approved for rollout."),
           ("v2025.08", "Patent filed", "Street lights that follow the car. 60% less energy."),
           ("v2025.06", "HWE tool @ Bühler", "30 minutes of MCC paperwork, now 30 seconds."),
           ("v2025.02", "NEC #7", "Ranked 7th of 1500+ colleges, IIT Bombay.")]
    c = Canvas(F, t, 1200, 560)
    c.add(f'<rect width="1200" height="560" fill="{t["bg"]}"/>')
    c.text(60, 70, "Changelog", 44, t["ink"], SANS, 700, extra='letter-spacing="-1.5"')
    c.add(f'<line x1="246" x2="246" y1="110" y2="530" stroke="{t["line"]}" stroke-width="2"/>')
    for i, (v, title, note) in enumerate(log):
        y = 130 + i * 70
        c.text(60, y + 14, v, 14, t["soft"], MONO)
        c.add(f'<circle cx="246" cy="{y + 9}" r="6" fill="{t["beam"] if i == 0 else t["bg"]}" stroke="{t["beam"]}" stroke-width="2"/>')
        c.text(276, y + 15, title, 19, t["ink"], SANS, 600)
        c.text(276, y + 40, note, 16, t["soft"], SANS)
    c.save(f"changelog-{th}.svg", "Changelog: " + "; ".join(f"{a} {b}: {n}" for a, b, n in log))

links = " · ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Modern / contemporary launch page. Light and dark follow your GitHub theme. Built by scripts/gen_modern.py -->

<p align="center">{pic(F, "hero", f"Software for the factory floor. {NAME} ships the tools a transformer plant runs on.")}</p>

<p align="center">
  <a href="mailto:{EMAIL}"><img src="https://img.shields.io/badge/Get_in_touch-0A0A0B?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
  <a href="{LINKEDIN}"><img src="https://img.shields.io/badge/LinkedIn-5E6AD2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
  <a href="https://krishna-ittl.github.io/Candidate-Screener/"><img src="https://img.shields.io/badge/Live_demo-F7F8F8?style=for-the-badge&logo=githubpages&logoColor=0A0A0B" alt="Job Lens live demo"/></a>
</p>

<p align="center">{pic(F, "features", "Built for real shifts: ten projects")}</p>
<p align="center"><sub>{links}</sub></p>
<p align="center">{pic(F, "changelog", "Changelog")}</p>

<p align="center"><sub>Electrical by degree · software by choice · {EMAIL}</sub></p>
""")
print("ok")
