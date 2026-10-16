"""Memphis design profile: squiggles, zigzags, confetti shapes, bold blocks and playful type.
Run: python scripts/gen_memphis.py"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, icon, pic, write_readme, wrap
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, EXPERIENCE, short

F = "memphis"
FUN = "'Arial Black', 'Futura', 'Century Gothic', 'Trebuchet MS', sans-serif"
BODY = "'Century Gothic', 'Futura', 'Trebuchet MS', sans-serif"
THEMES = {"light": dict(bg="#FFF7E6", ink="#1B1B1B", pink="#FF6FB5", yellow="#FFD23F", teal="#3BCEAC", blue="#3A86FF", purple="#8338EC", red="#EF476F"),
          "dark": dict(bg="#1B1430", ink="#FFF7E6", pink="#FF6FB5", yellow="#FFD23F", teal="#3BCEAC", blue="#5B9BFF", purple="#A06BFF", red="#FF5C85")}
COLS = ["pink", "yellow", "teal", "blue", "purple", "red"]


def squiggle(x, y, w, amp=10, n=6):
    return "M" + " ".join(f"{x + w * i / n:.0f},{y + (amp if i % 2 else -amp)}" if i else f"{x},{y}" for i in range(n + 1)).replace(" ", " Q", 0)


def wavy(x, y, w, amp=10, seg=30):
    d = f"M{x},{y}"
    for i in range(int(w / seg)):
        d += f" q{seg / 2},{-amp if i % 2 else amp} {seg},0"
    return d


def confetti(c, t, w, h, n, seed):
    rnd = random.Random(seed)
    for i in range(n):
        x, y, col = rnd.uniform(0, w), rnd.uniform(0, h), t[rnd.choice(COLS)]
        kind, rot = rnd.randrange(5), rnd.uniform(0, 360)
        cls = f'class="fl" style="animation-delay:-{rnd.uniform(0, 6):.1f}s;transform-origin:{x:.0f}px {y:.0f}px"'
        if kind == 0:
            shape = f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(5, 12):.0f}" fill="{col}"/>'
        elif kind == 1:
            shape = f'<path d="M{x:.0f},{y - 12:.0f} l12,20 h-24z" fill="none" stroke="{col}" stroke-width="4" transform="rotate({rot:.0f} {x:.0f} {y:.0f})"/>'
        elif kind == 2:
            shape = f'<path d="{wavy(x, y, 60, 8, 15)}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" transform="rotate({rot:.0f} {x:.0f} {y:.0f})"/>'
        elif kind == 3:
            shape = f'<rect x="{x:.0f}" y="{y:.0f}" width="14" height="14" fill="{col}" transform="rotate({rot:.0f} {x:.0f} {y:.0f})"/>'
        else:
            shape = f'<path d="M{x - 10:.0f},{y:.0f} h20 M{x:.0f},{y - 10:.0f} v20" stroke="{col}" stroke-width="4"/>'
        c.add(f'<g {cls}>{shape}</g>')
    c.css.append(".fl{animation:fl 6s ease-in-out infinite}@keyframes fl{50%{transform:translateY(-8px) rotate(14deg)}}")


for th, t in THEMES.items():
    c = Canvas(F, t, 1200, 620)
    c.defs.append(f'<pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="2.5" fill="{t["ink"]}"/></pattern>'
                  f'<pattern id="stripe" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="7" height="14" fill="{t["ink"]}"/></pattern>')
    c.add(f'<rect width="1200" height="620" fill="{t["bg"]}"/>')
    c.add(f'<circle cx="980" cy="170" r="150" fill="{t["yellow"]}"/><rect x="900" y="250" width="240" height="240" fill="url(#dots)" opacity=".8"/>'
          f'<path d="M760 560 l90 -160 90 160z" fill="{t["teal"]}"/><rect x="60" y="430" width="300" height="120" fill="url(#stripe)"/>'
          f'<rect x="1040" y="420" width="120" height="120" fill="{t["pink"]}" transform="rotate(15 1100 480)"/>')
    confetti(c, t, 1200, 620, 26, 7)
    c.add(f'<path d="{wavy(60, 120, 420, 16, 30)}" fill="none" stroke="{t["purple"]}" stroke-width="7" stroke-linecap="round"/>')
    c.text(60, 230, "TOTALLY", 92, t["ink"], FUN, 900, extra=f'style="paint-order:stroke" stroke="{t["pink"]}" stroke-width="10" letter-spacing="-2"')
    c.text(60, 330, "RADICAL", 92, t["ink"], FUN, 900, extra=f'style="paint-order:stroke" stroke="{t["teal"]}" stroke-width="10" letter-spacing="-2"')
    c.text(60, 410, "ENGINEER.", 64, t["blue"], FUN, 900, extra='letter-spacing="-1"')
    c.add(f'<rect x="400" y="460" width="420" height="80" fill="{t["red"]}" transform="rotate(-3 610 500)"/>')
    c.text(610, 512, NAME.upper(), 34, "#FFFFFF", FUN, 900, "middle", 'transform="rotate(-3 610 500)"')
    c.text(980, 160, "9", 120, t["ink"], FUN, 900, "middle")
    c.text(980, 210, "APPS LIVE!", 24, t["ink"], FUN, 900, "middle")
    c.save(f"hero-{th}.svg", f"Totally radical engineer: {NAME}. 9 apps live.")

    # projects as playful tiles
    c = Canvas(F, t, 1200, 820)
    c.defs.append(f'<pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="2.5" fill="{t["ink"]}"/></pattern>')
    c.add(f'<rect width="1200" height="820" fill="{t["bg"]}"/>')
    confetti(c, t, 1200, 820, 18, 11)
    c.text(600, 80, "STUFF I MADE (AND YES, IT WORKS)", 40, t["ink"], FUN, 900, "middle", f'style="paint-order:stroke" stroke="{t["yellow"]}" stroke-width="8"')
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        x, y = 50 + (i % 5) * 224, 130 + (i // 5) * 330
        col = t[COLS[i % 6]]
        shape = i % 3
        c.add(f'<rect x="{x + 10}" y="{y + 10}" width="200" height="290" fill="url(#dots)" opacity=".6"/>'
              f'<rect x="{x}" y="{y}" width="200" height="290" fill="{t["bg"]}" stroke="{t["ink"]}" stroke-width="4"/>')
        if shape == 0:
            c.add(f'<circle cx="{x + 100}" cy="{y + 86}" r="60" fill="{col}"/>')
        elif shape == 1:
            c.add(f'<path d="M{x + 100},{y + 20} l64,116 h-128z" fill="{col}"/>')
        else:
            c.add(f'<rect x="{x + 44}" y="{y + 30}" width="112" height="112" fill="{col}" transform="rotate(12 {x + 100} {y + 86})"/>')
        c.add(icon(slug, x + 66, y + 54, 68, "#FFFFFF", t["ink"] if th == "light" else "#1B1B1B", col))
        c.text(x + 100, y + 180, short(name).upper(), 16 if len(short(name)) < 15 else 13, t["ink"], FUN, 900, "middle")
        for j, l in enumerate(wrap(hook, 13, 176, .55)[:3]):
            c.text(x + 100, y + 206 + j * 18, l, 13, t["ink"], BODY, anchor="middle")
        c.add(f'<path d="{wavy(x + 30, y + 268, 140, 5, 14)}" fill="none" stroke="{col}" stroke-width="4"/>')
    c.save(f"projects-{th}.svg", "Stuff I made: " + "; ".join(f"{p[1]}, {p[4]}" for p in PROJECTS))

    # say hi banner
    c = Canvas(F, t, 1200, 300)
    c.add(f'<rect width="1200" height="300" fill="{t["purple"]}"/>')
    confetti(c, t, 1200, 300, 16, 3)
    c.add(f'<rect x="200" y="70" width="800" height="160" fill="{t["yellow"]}" stroke="{t["ink"]}" stroke-width="5" transform="rotate(-2 600 150)"/>')
    c.text(600, 150, "LET'S MAKE SOMETHING RAD!", 44, "#1B1B1B", FUN, 900, "middle", 'transform="rotate(-2 600 150)"')
    c.text(600, 198, EMAIL, 24, "#1B1B1B", BODY, 700, "middle", 'transform="rotate(-2 600 150)"')
    c.save(f"sayhi-{th}.svg", f"Let's make something rad: {EMAIL}")

links = " ~ ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Memphis design: squiggles, confetti and loud geometry. Cream daytime and grape-night versions follow your GitHub theme. Built by scripts/gen_memphis.py -->

<p align="center">{pic(F, "hero", f"Totally radical engineer: {NAME}")}</p>
<p align="center">{pic(F, "projects", "Stuff I made")}</p>
<p align="center"><b>{links}</b></p>
<p align="center"><a href="mailto:{EMAIL}">{pic(F, "sayhi", "Let's make something rad")}</a></p>
<p align="center"><sub>〰 <a href="{LINKEDIN}">linkedin</a> 〰</sub></p>
""")
print("ok")
