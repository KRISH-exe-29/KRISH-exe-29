"""Art Deco profile: gold on black, sunburst fans, stepped symmetric frames, a shimmering gold sweep.
Run: python scripts/gen_deco.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, WINS, EXPERIENCE, short

F = "deco"
DECO = "'Broadway', 'Poiret One', 'Didot', 'Bodoni MT', 'Futura', 'Century Gothic', serif"
CAPS = "'Futura', 'Century Gothic', 'Josefin Sans', 'Trebuchet MS', sans-serif"
THEMES = {"dark": dict(bg="#0C0B09", panel="#14120E", gold1="#F6E27A", gold2="#B8862B", ink="#F3E9CF", soft="#9C8E6E"),
          "light": dict(bg="#F6F0E1", panel="#FFFBF1", gold1="#C9A13A", gold2="#7A5612", ink="#1A1610", soft="#6E5F42")}


def golds(c, t):
    c.defs.append(f'<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["gold1"]}"/><stop offset=".5" stop-color="{t["gold2"]}"/><stop offset="1" stop-color="{t["gold1"]}"/></linearGradient>'
                  '<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0"><stop offset=".4" stop-color="#FFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFF" stop-opacity=".55"/><stop offset=".6" stop-color="#FFF" stop-opacity="0"/></linearGradient>')
    c.css.append(".shine{animation:sh 5s ease-in-out infinite}@keyframes sh{0%{transform:translateX(-1300px)}60%,100%{transform:translateX(1300px)}}")


def stepped(x, y, w, h, s=14):
    """Stepped Art Deco frame outline."""
    return (f"M{x + 2 * s},{y} H{x + w - 2 * s} V{y + s} H{x + w - s} V{y + 2 * s} H{x + w} V{y + h - 2 * s} H{x + w - s} V{y + h - s} H{x + w - 2 * s} V{y + h} "
            f"H{x + 2 * s} V{y + h - s} H{x + s} V{y + h - 2 * s} H{x} V{y + 2 * s} H{x + s} V{y + s} H{x + 2 * s} Z")


def fan(cx, cy, r, n, a0=180, a1=360):
    out = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + r * math.cos(a):.1f}" y2="{cy + r * math.sin(a):.1f}" stroke="url(#gold)" stroke-width="2"/>')
    return "".join(out)


for th, t in THEMES.items():
    # marquee
    c = Canvas(F, t, 1200, 680)
    golds(c, t)
    c.add(f'<rect width="1200" height="680" fill="{t["bg"]}"/>', fan(600, 420, 520, 36))
    for r in (150, 190, 230):
        c.add(f'<path d="M{600 - r},420 A{r},{r} 0 0 1 {600 + r},420" fill="none" stroke="url(#gold)" stroke-width="{3 if r == 150 else 1.5}"/>')
    c.add(f'<path d="{stepped(140, 300, 920, 340, 18)}" fill="{t["panel"]}" stroke="url(#gold)" stroke-width="4"/>'
          f'<path d="{stepped(156, 316, 888, 308, 14)}" fill="none" stroke="url(#gold)" stroke-width="1.5"/>')
    c.text(600, 370, "THE", 22, t["soft"], CAPS, 700, "middle", 'letter-spacing="14"')
    c.text(600, 452, "KRISHNA RAJU S", 72, "url(#gold)", DECO, 700, "middle", 'letter-spacing="8"')
    c.text(600, 500, "ELECTRIC COMPANY", 26, t["ink"], CAPS, 700, "middle", 'letter-spacing="16"')
    c.add(f'<path d="M380 530 H560 M640 530 H820" stroke="url(#gold)" stroke-width="2"/><path d="M600 518 l12 12 -12 12 -12 -12z" fill="url(#gold)"/>')
    c.text(600, 580, "ENGINEERING · SOFTWARE · AUTOMATION", 16, t["soft"], CAPS, 700, "middle", 'letter-spacing="6"')
    c.text(600, 610, "EST. MMIV · CHENNAI", 14, t["soft"], CAPS, 700, "middle", 'letter-spacing="8"')
    c.add('<clipPath id="mq"><rect width="1200" height="680"/></clipPath><g clip-path="url(#mq)"><rect class="shine" x="0" y="0" width="1200" height="680" fill="url(#shine)" opacity=".5"/></g>')
    c.save(f"marquee-{th}.svg", f"The {NAME} Electric Company. Engineering, software, automation. Established 2004, Chennai.")

    # exhibits: projects in stepped frames
    c = Canvas(F, t, 1200, 780)
    golds(c, t)
    c.add(f'<rect width="1200" height="780" fill="{t["bg"]}"/>')
    c.text(600, 70, "THE EXHIBITS", 34, "url(#gold)", DECO, 700, "middle", 'letter-spacing="12"')
    c.add(f'<path d="M420 92 H780" stroke="url(#gold)" stroke-width="2"/>')
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        x, y = 50 + (i % 5) * 222, 120 + (i // 5) * 320
        c.add(f'<path d="{stepped(x, y, 206, 300, 10)}" fill="{t["panel"]}" stroke="url(#gold)" stroke-width="2"/>')
        c.add(f'<g opacity=".9">{fan(x + 103, y + 110, 70, 12)}</g><circle cx="{x + 103}" cy="{y + 110}" r="22" fill="url(#gold)"/>')
        c.text(x + 103, y + 116, ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"][i], 15, t["bg"], DECO, 700, "middle")
        nm = short(name).upper()
        c.text(x + 103, y + 166, nm, 15 if len(nm) < 15 else 12, t["ink"], CAPS, 700, "middle", 'letter-spacing="2"')
        c.add(f'<path d="M{x + 60} {y + 180} H{x + 146}" stroke="url(#gold)"/>')
        words, lines, line = hook.split(), [], ""
        for wd in words:
            if len(line + wd) > 24:
                lines.append(line.strip()); line = ""
            line += wd + " "
        lines.append(line.strip())
        for j, l in enumerate(lines[:3]):
            c.text(x + 103, y + 204 + j * 18, l, 13, t["soft"], CAPS, anchor="middle")
        c.text(x + 103, y + 278, status, 11, "url(#gold)", CAPS, 700, "middle", 'letter-spacing="3"')
    c.save(f"exhibits-{th}.svg", "The exhibits: " + "; ".join(f"{p[1]}, {p[4]}" for p in PROJECTS))

    # honours
    c = Canvas(F, t, 1200, 470)
    golds(c, t)
    c.add(f'<rect width="1200" height="470" fill="{t["bg"]}"/><path d="{stepped(40, 30, 1120, 410, 20)}" fill="{t["panel"]}" stroke="url(#gold)" stroke-width="3"/>')
    c.text(600, 96, "HONOURS & ENGAGEMENTS", 28, "url(#gold)", DECO, 700, "middle", 'letter-spacing="10"')
    rows = [(w, a, b) for w, a, b in WINS] + [(e[2], e[0], e[1]) for e in EXPERIENCE[:2]]
    for i, (when, title, where) in enumerate(rows):
        y = 150 + i * 46
        c.text(110, y, when.upper(), 14, t["soft"], CAPS, 700, extra='letter-spacing="2"')
        c.text(290, y, title.upper(), 18, t["ink"], CAPS, 700, extra='letter-spacing="2"')
        c.text(1090, y, where, 14, t["soft"], CAPS, anchor="end")
        c.add(f'<path d="M110 {y + 14} H1090" stroke="url(#gold)" stroke-width=".8" opacity=".6"/>')
    c.text(600, 420, f"CORRESPONDENCE · {EMAIL.upper()}", 14, "url(#gold)", CAPS, 700, "middle", 'letter-spacing="4"')
    c.save(f"honours-{th}.svg", "Honours and engagements: " + "; ".join(f"{a}, {b}, {w}" for w, a, b in rows))

links = " · ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Art Deco: gold on black (dark) and gold on ivory (light), following your GitHub theme. Built by scripts/gen_deco.py -->

<p align="center">{pic(F, "marquee", f"The {NAME} Electric Company")}</p>
<p align="center">{pic(F, "exhibits", "The exhibits")}</p>
<p align="center"><sub>✦ {links} ✦</sub></p>
<p align="center">{pic(F, "honours", "Honours and engagements")}</p>
<p align="center"><sub><a href="mailto:{EMAIL}">correspondence</a> · <a href="{LINKEDIN}">calling card</a></sub></p>
""")
print("ok")
