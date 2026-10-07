"""Swiss / International Typographic Style profile: strict grid, Helvetica, red/black, flush-left, numbered sections.
Run: python scripts/gen_swiss.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, EXPERIENCE, WINS, SKILLS, CITY, CGPA, short

F = "swiss"
HEL = "'Helvetica Neue', Helvetica, 'Arial Nova', Arial, sans-serif"
THEMES = {"light": dict(bg="#F2F0EB", ink="#111111", red="#E3120B", soft="#6A6A6A", grid="#11111112"),
          "dark": dict(bg="#111111", ink="#F2F0EB", red="#FF2A1F", soft="#9A9A9A", grid="#F2F0EB12")}
COL = 1200 / 12


def grid(c, t, h):
    c.add(f'<rect width="1200" height="{h}" fill="{t["bg"]}"/>' + "".join(f'<line x1="{i * COL}" x2="{i * COL}" y1="0" y2="{h}" stroke="{t["grid"]}"/>' for i in range(1, 12)))


for th, t in THEMES.items():
    # poster hero
    c = Canvas(F, t, 1200, 900)
    grid(c, t, 900)
    c.add(f'<circle class="sun" cx="{COL * 9}" cy="300" r="190" fill="{t["red"]}"/>')
    for i, w in enumerate(["Krishna", "Raju S."]):
        c.text(COL * .4, 250 + i * 170, w, 190, t["ink"], HEL, 700, extra='letter-spacing="-10"')
    c.add(f'<rect class="bar" x="{COL * .5}" y="500" width="{COL * 11}" height="10" fill="{t["ink"]}"/>')
    cols = [("01", "Discipline", ["Electrical &", "Electronics", "Engineering"]),
            ("02", "Practice", ["Software for", "the factory", "floor"]),
            ("03", "Location", [CITY.split(",")[0], "Kanchipuram", "India"]),
            ("04", "Output", ["9 apps", "128 tests", "1 patent filed"])]
    for i, (n, h, lines) in enumerate(cols):
        x = COL * (.5 + i * 3)
        c.text(x, 560, n, 16, t["red"], HEL, 700)
        c.text(x, 590, h, 16, t["soft"], HEL, 400)
        for j, l in enumerate(lines):
            c.text(x, 640 + j * 34, l, 28, t["ink"], HEL, 700, extra='letter-spacing="-.5"')
    c.text(1170, 880, "Profile — 2026 — Typeset in Helvetica — Grid: 12 columns", 13, t["soft"], HEL, anchor="end")
    c.add(f'<text transform="translate(1180 470) rotate(-90)" font-family="{HEL}" font-size="13" fill="{t["soft"]}" letter-spacing="4">ENGINEER · BUILDER · AUTOMATOR</text>')
    c.css.append(".sun{transform-box:fill-box;transform-origin:center;animation:s 1.2s cubic-bezier(.7,0,.2,1) both}@keyframes s{from{transform:scale(0)}}"
                 ".bar{transform-box:fill-box;transform-origin:left;animation:b 1.4s cubic-bezier(.7,0,.2,1) .3s both}@keyframes b{from{transform:scaleX(0)}}")
    c.save(f"poster-{th}.svg", f"{NAME}. Discipline: electrical and electronics engineering. Practice: software for the factory floor. Output: 9 apps, 128 tests, 1 patent filed.")

    # index of works: typographic table
    c = Canvas(F, t, 1200, 760)
    grid(c, t, 760)
    c.text(COL * .5, 90, "Index of works", 64, t["ink"], HEL, 700, extra='letter-spacing="-3"')
    c.text(COL * 11.5, 90, "10", 64, t["red"], HEL, 700, "end")
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        y = 160 + i * 58
        c.add(f'<line x1="{COL * .5}" x2="{COL * 11.5}" y1="{y - 34}" y2="{y - 34}" stroke="{t["ink"]}" stroke-width="{2 if i == 0 else 1}"/>')
        c.text(COL * .5, y, f"{i + 1:02d}", 18, t["red"], HEL, 700)
        c.text(COL * 1.5, y, short(name), 24, t["ink"], HEL, 700, extra='letter-spacing="-.5"')
        c.text(COL * 5, y, hook, 16, t["ink"], HEL)
        c.text(COL * 9, y, stack.split(" · ")[0], 16, t["soft"], HEL)
        c.text(COL * 11.5, y, status.title(), 16, t["red"] if status in ("PRODUCTION", "LIVE") else t["soft"], HEL, 700, "end")
    c.save(f"index-{th}.svg", "Index of works: " + "; ".join(f"{i + 1:02d} {p[1]}, {p[2].lower()}" for i, p in enumerate(PROJECTS)))

    # chronology + distinctions
    c = Canvas(F, t, 1200, 640)
    grid(c, t, 640)
    c.text(COL * .5, 90, "Chronology", 64, t["ink"], HEL, 700, extra='letter-spacing="-3"')
    for i, (org, role, when, where, what, win) in enumerate(EXPERIENCE):
        y = 150 + i * 70
        c.text(COL * .5, y, when.split()[-1] if "now" not in when else "Now", 30, t["red"] if i == 0 else t["ink"], HEL, 700)
        c.text(COL * 2.5, y - 8, org, 20, t["ink"], HEL, 700)
        c.text(COL * 2.5, y + 16, role, 15, t["soft"], HEL)
    c.add(f'<rect x="{COL * 7.5}" y="120" width="{COL * 4}" height="460" fill="{t["red"]}"/>')
    c.text(COL * 7.8, 170, "Distinctions", 30, "#FFFFFF", HEL, 700)
    for i, (when, title, where) in enumerate(WINS):
        y = 230 + i * 84
        c.text(COL * 7.8, y, title, 22, "#FFFFFF", HEL, 700)
        c.para(COL * 7.8, y + 24, f"{where}, {when}", 14, COL * 3.4, fill="#FFFFFF", font=HEL)
    c.text(COL * .5, 610, f"B.E. Electrical & Electronics, CGPA {CGPA}  ·  {EMAIL}", 15, t["soft"], HEL)
    c.save(f"chronology-{th}.svg", "Chronology: " + "; ".join(f"{e[2]} {e[0]}" for e in EXPERIENCE) + ". Distinctions: " + "; ".join(f"{a}, {b}" for _, a, b in WINS))

links = " — ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Swiss / International Typographic Style. Light and dark follow your GitHub theme. Built by scripts/gen_swiss.py -->

{pic(F, "poster", f"{NAME}: engineer, builder, automator")}

**01** [Email]({"mailto:" + EMAIL}) — **02** [LinkedIn]({LINKEDIN}) — **03** [Job Lens, live](https://krishna-ittl.github.io/Candidate-Screener/)

{pic(F, "index", "Index of works")}

{links}

{pic(F, "chronology", "Chronology and distinctions")}
""")
print("ok")
