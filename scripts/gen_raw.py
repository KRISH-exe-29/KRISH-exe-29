"""Raw brutalist profile: default fonts, default link blue, hard rules, cropped type, almost no styling on purpose.
Run: python scripts/gen_raw.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, EXPERIENCE, WINS, CERTS, COLLEGE, CGPA, short

F = "raw"
TIMES = "'Times New Roman', Times, serif"
COUR = "'Courier New', Courier, monospace"
THEMES = {"light": dict(bg="#FFFFFF", ink="#000000", link="#0000EE", visited="#551A8B", red="#FF0000"),
          "dark": dict(bg="#000000", ink="#FFFFFF", link="#5C8DFF", visited="#B98CFF", red="#FF3B3B")}

for th, t in THEMES.items():
    c = Canvas(F, t, 1200, 700)
    c.add(f'<rect width="1200" height="700" fill="{t["bg"]}"/>')
    c.text(-40, 330, "KRISHNA", 330, t["ink"], TIMES, 700, extra='letter-spacing="-12"')
    c.text(600, 692, "RAJU S", 190, "none", TIMES, 700, extra=f'stroke="{t["ink"]}" stroke-width="2" letter-spacing="-8"')
    c.add(f'<rect x="0" y="372" width="1200" height="6" fill="{t["ink"]}"/><rect x="0" y="384" width="760" height="2" fill="{t["ink"]}"/>')
    c.text(10, 420, "this page has no design system. it has a deadline.", 28, t["ink"], COUR)
    c.text(10, 460, "electrical engineer / writes software / ships it / goes home", 22, t["ink"], COUR)
    c.text(10, 520, "[ 9 apps in production ]  [ 128 tests ]  [ patent filed ]", 22, t["link"], TIMES, extra='text-decoration="underline"')
    c.text(10, 556, "[ NEC #7 of 1500+ ]  [ 30 min → 30 s ]", 22, t["visited"], TIMES, extra='text-decoration="underline"')
    c.add(f'<g class="blink"><text x="10" y="640" font-family="{TIMES}" font-size="20" font-weight="700" fill="{t["red"]}">UNDER CONSTRUCTION: PERMANENTLY. THAT IS THE POINT.</text></g>')
    c.add(f'<rect x="1080" y="20" width="100" height="100" fill="none" stroke="{t["ink"]}" stroke-width="2"/><line x1="1080" y1="20" x2="1180" y2="120" stroke="{t["ink"]}" stroke-width="2"/>'
          f'<line x1="1180" y1="20" x2="1080" y2="120" stroke="{t["ink"]}" stroke-width="2"/>')
    c.text(1130, 140, "img.jpg (missing)", 12, t["ink"], TIMES, anchor="middle")
    c.css.append(".blink{animation:b 1s steps(1) infinite}@keyframes b{50%{opacity:0}}")
    c.save(f"banner-{th}.svg", f"{NAME}. This page has no design system, it has a deadline. Electrical engineer, writes software, ships it, goes home.")

rows = "\n".join(f"| {i:02d} | {f'[{p[1]}]({p[3]})' if p[3] else p[1]} | {p[2]} | {p[4]} | `{p[6]}` |" for i, p in enumerate(PROJECTS, 1))
jobs = "\n".join(f"{e[2]:<16} {e[0].upper():<28} {e[1]}" for e in EXPERIENCE)
write_readme(f"""
<!-- Raw brutalism: default fonts, default blue links, hard rules, no polish. Built by scripts/gen_raw.py -->

{pic(F, "banner", f"{NAME}: this page has no design system, it has a deadline.")}

# KRISHNA RAJU S

**ELECTRICAL ENGINEER.** WRITES SOFTWARE. SHIPS IT. GOES HOME.

~~beautiful landing page~~ → working software on a factory floor.

***

## WHAT I MADE

| # | THING | STATE | WHAT IT DOES | MADE OF |
|---|---|---|---|---|
{rows}

***

## WHERE I WORKED

```
{jobs}
```

***

## PROOF

{chr(10).join(f"- **{a.upper()}**: {b} ({w})" for w, a, b in WINS)}
- **DEGREE**: B.E. ELECTRICAL & ELECTRONICS, {COLLEGE.upper()}, CGPA {CGPA}
- **CERTS**: {" / ".join(CERTS)}

***

## RULES I WORK BY

1. IF A HUMAN DOES IT TWICE A DAY, A SCRIPT DOES IT FROM NOW ON.
2. SHIP IT. THEN IMPROVE IT.
3. TESTS OR IT DIDN'T HAPPEN. (DISPATCH HAS 128.)
4. FLUENT IN OHM'S LAW AND GIT. NO OTHER LANGUAGE REQUIRED.

***

<kbd>EMAIL</kbd> {EMAIL} &nbsp; <kbd>LINKEDIN</kbd> [{LINKEDIN.replace("https://", "")}]({LINKEDIN})

<sub>NO TEMPLATES. NO GRADIENTS. NO REGRETS. LAST UPDATED: WHEN SOMETHING SHIPPED.</sub>
""")
print("ok")
