"""Neumorphism / soft UI profile: one monochrome surface, every control raised or pressed into it.
Run: python scripts/gen_soft.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, icon, pic, write_readme, SANS
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short

F = "soft"
THEMES = {"light": dict(bg="#E4E9F0", hi="#FFFFFF", lo="#A3B1C6", ink="#3D4A5C", soft="#7C8AA0", acc="#5B7CFA"),
          "dark": dict(bg="#272B33", hi="#343A45", lo="#16191E", ink="#D6DCE6", soft="#8792A3", acc="#7C95FF")}


def soft_defs(c, t):
    c.defs.append(f'<filter id="up" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="-8" dy="-8" stdDeviation="8" flood-color="{t["hi"]}"/>'
                  f'<feDropShadow dx="8" dy="8" stdDeviation="9" flood-color="{t["lo"]}"/></filter>'
                  f'<filter id="in" x="-10%" y="-10%" width="120%" height="120%"><feFlood flood-color="{t["lo"]}" result="d"/><feComposite in2="SourceAlpha" operator="out"/>'
                  f'<feGaussianBlur stdDeviation="5"/><feOffset dx="5" dy="5" result="s1"/><feFlood flood-color="{t["hi"]}"/><feComposite in2="SourceAlpha" operator="out"/>'
                  f'<feGaussianBlur stdDeviation="5"/><feOffset dx="-5" dy="-5" result="s2"/><feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="s1"/><feMergeNode in="s2"/></feMerge>'
                  f'<feComposite in2="SourceAlpha" operator="in"/></filter>')


def raised(c, t, x, y, w, h, rx):
    c.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{t["bg"]}" filter="url(#up)"/>')


def pressed(c, t, x, y, w, h, rx):
    c.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{t["bg"]}" filter="url(#in)"/>')


for th, t in THEMES.items():
    c = Canvas(F, t, 1200, 640)
    soft_defs(c, t)
    c.add(f'<rect width="1200" height="640" fill="{t["bg"]}"/>')
    # profile card
    raised(c, t, 60, 60, 520, 520, 40)
    c.add(f'<circle cx="170" cy="170" r="62" fill="{t["bg"]}" filter="url(#up)"/><circle cx="170" cy="170" r="48" fill="{t["bg"]}" filter="url(#in)"/>')
    c.text(170, 184, "KR", 38, t["acc"], SANS, 700, "middle")
    c.text(260, 160, NAME, 34, t["ink"], SANS, 700)
    c.text(260, 194, "Electrical engineer · software builder", 17, t["soft"], SANS)
    c.text(100, 290, "Soft on the eyes.", 30, t["ink"], SANS, 300)
    c.text(100, 330, "Hard on manual work.", 30, t["ink"], SANS, 700)
    for i, (lab, on) in enumerate([("Automation", True), ("Manual entry", False), ("Chai", True)]):
        y = 400 + i * 56
        c.text(100, y + 8, lab, 18, t["ink"], SANS, 500)
        pressed(c, t, 420, y - 16, 110, 44, 22)
        kx = 508 if on else 442
        c.add(f'<circle class="{"kn" if lab == "Automation" else ""}" cx="{kx}" cy="{y + 6}" r="16" fill="{t["acc"] if on else t["bg"]}" filter="url(#up)"/>')
    # knob + now playing
    raised(c, t, 640, 60, 500, 250, 40)
    cx, cy = 760, 185
    c.add(f'<circle cx="{cx}" cy="{cy}" r="78" fill="{t["bg"]}" filter="url(#in)"/><circle cx="{cx}" cy="{cy}" r="58" fill="{t["bg"]}" filter="url(#up)"/>')
    for a in range(-135, 136, 27):
        x1, y1 = cx + 90 * math.sin(math.radians(a)), cy - 90 * math.cos(math.radians(a))
        c.add(f'<circle cx="{x1:.0f}" cy="{y1:.0f}" r="3" fill="{t["acc"] if a <= 108 else t["soft"]}"/>')
    c.add(f'<g class="knob" style="transform-origin:{cx}px {cy}px"><circle cx="{cx}" cy="{cy - 40}" r="7" fill="{t["acc"]}"/></g>')
    c.text(880, 150, "OUTPUT", 14, t["soft"], SANS, 700, extra='letter-spacing="3"')
    c.text(880, 200, "9 apps", 44, t["ink"], SANS, 700)
    c.text(880, 236, "in production, turned up", 16, t["soft"], SANS)
    raised(c, t, 640, 340, 500, 240, 40)
    c.text(680, 392, "NOW SHIPPING", 13, t["soft"], SANS, 700, extra='letter-spacing="3"')
    c.text(680, 430, "KioskSentinel", 28, t["ink"], SANS, 700)
    c.text(680, 458, "attendance that survives power cuts", 15, t["soft"], SANS)
    pressed(c, t, 680, 488, 300, 12, 6)
    c.add(f'<rect class="bar" x="683" y="491" width="210" height="6" rx="3" fill="{t["acc"]}"/>')
    c.add(f'<circle cx="1040" cy="494" r="30" fill="{t["bg"]}" filter="url(#up)"/>')
    c.text(1040, 503, "▶", 24, t["acc"], SANS, 700, "middle")
    c.css.append(".knob{animation:kb 4s ease-in-out infinite alternate}@keyframes kb{from{transform:rotate(-120deg)}to{transform:rotate(108deg)}}"
                 ".bar{transform-box:fill-box;transform-origin:left;animation:br 6s linear infinite}@keyframes br{from{transform:scaleX(.1)}}")
    c.save(f"panel-{th}.svg", f"Soft UI panel for {NAME}: soft on the eyes, hard on manual work. Automation on, manual entry off, chai on. Output knob at 9 apps. Now shipping KioskSentinel.")

    # projects: raised tiles with pressed icon wells
    c = Canvas(F, t, 1200, 700)
    soft_defs(c, t)
    c.add(f'<rect width="1200" height="700" fill="{t["bg"]}"/>')
    c.text(60, 76, "Projects", 34, t["ink"], SANS, 700)
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        x, y = 60 + (i % 5) * 220, 120 + (i // 5) * 280
        raised(c, t, x, y, 190, 250, 30)
        c.add(f'<circle cx="{x + 95}" cy="{y + 72}" r="44" fill="{t["bg"]}" filter="url(#in)"/>' + icon(slug, x + 70, y + 47, 50, t["acc"], t["ink"], t["soft"]))
        c.text(x + 95, y + 148, short(name), 17, t["ink"], SANS, 700, "middle")
        c.text(x + 95, y + 172, status.lower(), 12, t["acc"], SANS, 700, "middle")
        words, lines, line = hook.split(), [], ""
        for w in words:
            if len(line + w) > 22:
                lines.append(line.strip()); line = ""
            line += w + " "
        lines.append(line.strip())
        for j, l in enumerate(lines[:2]):
            c.text(x + 95, y + 200 + j * 18, l, 13, t["soft"], SANS, anchor="middle")
    c.save(f"projects-{th}.svg", "Projects: " + "; ".join(f"{p[1]}, {p[4]}" for p in PROJECTS))

    # contact pill
    c = Canvas(F, t, 1200, 220)
    soft_defs(c, t)
    c.add(f'<rect width="1200" height="220" fill="{t["bg"]}"/>')
    raised(c, t, 300, 60, 600, 100, 50)
    pressed(c, t, 320, 76, 68, 68, 34)
    c.text(354, 120, "✉", 26, t["acc"], SANS, 700, "middle")
    c.text(410, 104, "Press gently to hire", 15, t["soft"], SANS)
    c.text(410, 132, EMAIL, 22, t["ink"], SANS, 700)
    c.save(f"contact-{th}.svg", f"Press gently to hire: {EMAIL}")

links = " · ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Neumorphism / soft UI: one surface, raised and pressed. Cloud-grey and graphite versions follow your GitHub theme. Built by scripts/gen_soft.py -->

<p align="center">{pic(F, "panel", f"Soft UI panel for {NAME}")}</p>
<p align="center">{pic(F, "projects", "Projects")}</p>
<p align="center"><sub>{links}</sub></p>
<p align="center"><a href="mailto:{EMAIL}">{pic(F, "contact", "Press gently to hire")}</a></p>
<p align="center"><sub><a href="{LINKEDIN}">linkedin</a></sub></p>
""")
print("ok")
