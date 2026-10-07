"""Typography-first profile: words are the only visuals. Kinetic statements, outline giants, rotating verbs.
Run: python scripts/gen_typography.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, MONO
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short

F = "type"
HEAVY = "'Arial Black', 'Helvetica Neue', Impact, Arial, sans-serif"
SERIF = "'Playfair Display', Didot, 'Bodoni MT', Georgia, serif"
THEMES = {"light": dict(bg="#FAFAF7", ink="#0D0D0D", acc="#FF3D00", soft="#9A9A92"), "dark": dict(bg="#0D0D0D", ink="#FAFAF7", acc="#FF5A1F", soft="#6A6A64")}

for th, t in THEMES.items():
    # 1. statement with rotating verb
    c = Canvas(F, t, 1200, 640)
    c.add(f'<rect width="1200" height="640" fill="{t["bg"]}"/>')
    c.text(40, 60, "KRISHNA RAJU S — A PROFILE SET IN TYPE", 14, t["soft"], MONO, extra='letter-spacing="3"')
    c.text(30, 220, "I", 190, t["ink"], HEAVY, 900)
    verbs = ["BUILD", "TEST", "SHIP", "DELETE"]
    c.add(f'<clipPath id="vb"><rect x="130" y="50" width="1060" height="200"/></clipPath><g clip-path="url(#vb)">')
    for i, v in enumerate(verbs):
        c.add(f'<g class="v v{i}"><text x="150" y="220" font-family="{HEAVY}" font-size="190" font-weight="900" fill="{t["acc"]}" letter-spacing="-8">{v}</text></g>')
    c.add("</g>")
    c.text(30, 400, "THINGS", 190, "none", HEAVY, 900, extra=f'stroke="{t["ink"]}" stroke-width="3" letter-spacing="-8"')
    c.text(30, 575, "FACTORIES RUN ON.", 98, t["ink"], HEAVY, 900, extra='letter-spacing="-5"')
    c.css.append(".v{opacity:0;animation:vv 8s infinite}.v0{opacity:1}.v1{animation-delay:2s}.v2{animation-delay:4s}.v3{animation-delay:6s}"
                 "@keyframes vv{0%{opacity:0;transform:translateY(200px)}5%,22%{opacity:1;transform:none}27%,100%{opacity:0;transform:translateY(-200px)}}")
    c.save(f"statement-{th}.svg", "I build, test, ship and delete things factories run on.")

    # 2. numbers as type
    c = Canvas(F, t, 1200, 700)
    c.add(f'<rect width="1200" height="700" fill="{t["bg"]}"/>')
    big = [("30", "minutes of paperwork"), ("→", ""), ("30", "seconds. Bühler, 2025.")]
    c.text(30, 250, "30", 220, t["ink"], HEAVY, 900, extra='letter-spacing="-14"')
    c.text(310, 160, "minutes of MCC", 28, t["soft"], SERIF, extra='font-style="italic"')
    c.text(310, 198, "paperwork, before.", 28, t["soft"], SERIF, extra='font-style="italic"')
    c.add(f'<g class="arrow"><text x="560" y="228" font-family="{HEAVY}" font-size="150" fill="{t["acc"]}">→</text></g>')
    c.text(1170, 250, "30s", 220, t["acc"], HEAVY, 900, "end", 'letter-spacing="-14"')
    c.add(f'<line x1="30" x2="1170" y1="300" y2="300" stroke="{t["ink"]}" stroke-width="4"/>')
    for i, (n, l) in enumerate([("9", "apps in production"), ("128", "tests guard dispatch"), ("#7", "of 1500+ colleges"), ("1", "patent filed")]):
        x = 30 + i * 290
        c.text(x, 520, n, 170 if len(n) < 3 else 130, t["ink"] if i % 2 else "none", HEAVY, 900,
               extra=f'letter-spacing="-8" {"" if i % 2 else f"stroke={chr(34)}{t["ink"]}{chr(34)} stroke-width={chr(34)}3{chr(34)}"}')
        c.text(x + 4, 572, l.upper(), 16, t["soft"], MONO, extra='letter-spacing="2"')
    c.text(30, 660, "Numbers do the talking. I just write the scripts that move them.", 26, t["ink"], SERIF, extra='font-style="italic"')
    c.css.append(".arrow{animation:ar 1.4s ease-in-out infinite}@keyframes ar{50%{transform:translateX(30px)}}")
    c.save(f"numbers-{th}.svg", "30 minutes of paperwork became 30 seconds. 9 apps in production, 128 tests, rank 7 of 1500+, 1 patent filed.")

    # 3. works as a typographic list
    c = Canvas(F, t, 1200, 860)
    c.add(f'<rect width="1200" height="860" fill="{t["bg"]}"/>')
    c.text(30, 70, "SELECTED WORKS", 16, t["soft"], MONO, extra='letter-spacing="3"')
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        y = 140 + i * 72
        nm = short(name).upper()
        live = status in ("PRODUCTION", "LIVE")
        c.text(30, y, nm, 60, t["ink"] if live else "none", HEAVY, 900,
               extra=f'letter-spacing="-3" {"" if live else f"stroke={chr(34)}{t["ink"]}{chr(34)} stroke-width={chr(34)}1.6{chr(34)}"}')
        c.text(1170, y - 30, f"{i + 1:02d}", 16, t["acc"], MONO, 700, "end")
        c.text(1170, y - 6, hook, 18, t["soft"], SERIF, anchor="end", extra='font-style="italic"')
    c.text(30, 845, "SOLID = IN PRODUCTION OR LIVE.   OUTLINE = SHIPPED, BUILT OR COMING.", 14, t["soft"], MONO, extra='letter-spacing="2"')
    c.save(f"works-{th}.svg", "Selected works: " + "; ".join(f"{p[1]}, {p[4]}" for p in PROJECTS))

    # 4. sign-off
    c = Canvas(F, t, 1200, 380)
    c.add(f'<rect width="1200" height="380" fill="{t["acc"]}"/>')
    c.text(30, 150, "SAY HI.", 150, "#FFFFFF", HEAVY, 900, extra='letter-spacing="-8"')
    c.text(30, 230, "I read every email. I automate the rest.", 32, "#FFFFFF", SERIF, extra='font-style="italic"')
    c.text(30, 330, EMAIL.upper(), 34, "#FFFFFF", MONO, 700)
    c.save(f"signoff-{th}.svg", f"Say hi. I read every email, I automate the rest. {EMAIL}")

links = " / ".join(f"[{short(p[1]).lower()}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Typography-first: type is the only visual. Light and dark follow your GitHub theme. Built by scripts/gen_typography.py -->

{pic(F, "statement", "I build, test, ship and delete things factories run on.")}

{pic(F, "numbers", "30 minutes of paperwork became 30 seconds.")}

{pic(F, "works", "Selected works")}

<p align="center"><code>{links}</code></p>

<a href="mailto:{EMAIL}">{pic(F, "signoff", "Say hi.")}</a>

<p align="center"><sub><a href="{LINKEDIN}">linkedin</a></sub></p>
""")
print("ok")
