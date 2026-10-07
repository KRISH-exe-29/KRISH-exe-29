"""Y2K profile: a 2006 social page. Chrome bubble text, glossy aqua buttons, sparkles, a Top 8 of projects, an IM status window.
Run: python scripts/gen_y2k.py [photo]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, icon, pic, write_readme, photo_grid
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, CITY, LANGUAGES, short

F = "y2k"
VERD = "Verdana, Tahoma, 'Segoe UI', sans-serif"
TAHOMA = "Tahoma, Verdana, 'Segoe UI', sans-serif"
BUBBLE = "'Arial Rounded MT Bold', 'Comic Sans MS', 'Trebuchet MS', Arial, sans-serif"
THEMES = {"light": dict(page="#CFE8FF", box="#FFFFFF", head="#6BA4E8", ink="#1A2B4C", soft="#4D6A94", link="#0033CC", hot="#FF3399", glow="#9FE7FF"),
          "dark": dict(page="#0B0B2E", box="#151545", head="#3B2D8C", ink="#E9E6FF", soft="#A7A3E0", link="#7FD4FF", hot="#FF5AC8", glow="#5B3BFF")}
photo = photo_grid(F, 36, sys.argv[1] if len(sys.argv) > 1 else None)


def sparkles(c, pts):
    for i, (x, y, s) in enumerate(pts):
        c.add(f'<g class="sp" style="animation-delay:{i * .35:.2f}s;transform-origin:{x}px {y}px"><path d="M{x},{y - s} L{x + s * .25},{y - s * .25} L{x + s},{y} L{x + s * .25},{y + s * .25} '
              f'L{x},{y + s} L{x - s * .25},{y + s * .25} L{x - s},{y} L{x - s * .25},{y - s * .25}Z" fill="#FFFFFF"/></g>')


def box(c, t, x, y, w, h, title):
    c.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{t["box"]}" stroke="{t["head"]}" stroke-width="2"/>'
          f'<rect x="{x}" y="{y}" width="{w}" height="30" fill="url(#gloss)"/>')
    c.text(x + 10, y + 21, title, 14, "#FFFFFF", VERD, 700)


def gloss_defs(c, t):
    c.defs.append(f'<linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".7"/><stop offset=".5" stop-color="{t["head"]}"/><stop offset="1" stop-color="{t["head"]}"/></linearGradient>'
                  '<linearGradient id="aqua" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E8FBFF"/><stop offset=".48" stop-color="#7FD4FF"/><stop offset=".52" stop-color="#2E9BEA"/><stop offset="1" stop-color="#8FE3FF"/></linearGradient>'
                  '<linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".45" stop-color="#B9C6D6"/><stop offset=".5" stop-color="#5D6B80"/><stop offset=".8" stop-color="#DDE6F0"/><stop offset="1" stop-color="#FFFFFF"/></linearGradient>'
                  f'<filter id="glow"><feGaussianBlur stdDeviation="4" result="b"/><feFlood flood-color="{t["glow"]}"/><feComposite in2="b" operator="in"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    c.css.append(".sp{animation:sp 1.4s ease-in-out infinite}@keyframes sp{50%{transform:scale(.2) rotate(45deg);opacity:.3}}")


for th, t in THEMES.items():
    c = Canvas(F, t, 1200, 1040)
    gloss_defs(c, t)
    c.add(f'<rect width="1200" height="1040" fill="{t["page"]}"/>')
    # header bar
    c.add('<rect width="1200" height="64" fill="url(#gloss)"/>')
    c.text(24, 44, "KrishSpace", 30, "#FFFFFF", BUBBLE, 700, extra='filter="url(#glow)"')
    c.text(1176, 40, "Home | Browse | Search | Invite | Mail | Blog | Favorites | Forum | Groups", 13, "#FFFFFF", VERD, anchor="end")
    # name in chrome bubble text
    c.text(24, 130, f"{NAME}", 52, "url(#chrome)", BUBBLE, 900, extra=f'stroke="{t["ink"]}" stroke-width="1.5" filter="url(#glow)"')
    c.text(24, 162, "“I replace hours of work with scripts. Then pretend it was team effort ;)”", 15, t["soft"], VERD, extra='font-style="italic"')
    # left column: photo + details
    box(c, t, 24, 186, 380, 420, f"{NAME.split()[0]}'s Pic")
    cell = 8.6
    for r, row in enumerate(photo):
        for q, ch in enumerate(row):
            if ch != ".":
                v = int(ch)
                col = ["#1A1446", "#2B1F6B", "#3D2B8E", "#5A3BB0", "#7B4FD0", "#9E66E0", "#C487EC", "#E2A9F2", "#F5CDF7", "#FFF0FD"][v]
                c.add(f'<rect x="{60 + q * cell:.1f}" y="{226 + r * cell:.1f}" width="{cell:.1f}" height="{cell:.1f}" fill="{col}"/>')
    c.text(214, 556, "22 years old", 14, t["ink"], VERD, anchor="middle")
    c.text(214, 576, f"{CITY}", 14, t["ink"], VERD, anchor="middle")
    c.text(214, 596, "Last login: 5 minutes ago ✨", 12, t["soft"], VERD, anchor="middle")
    box(c, t, 24, 622, 380, 190, "Krishna's Details")
    det = [("Status:", "Shipping"), ("Here for:", "Boring processes"), ("Mood:", "⚡ electrified"), ("Speaks:", " · ".join(LANGUAGES)), ("Zodiac:", "Ohm ♉ Git")]
    for i, (k, v) in enumerate(det):
        c.text(40, 668 + i * 28, k, 13, t["soft"], VERD, 700)
        c.text(140, 668 + i * 28, v, 13, t["ink"], VERD)
    # now playing
    box(c, t, 24, 828, 380, 120, "♫ Now Playing")
    c.text(40, 882, "“Ohm's Law (Automation Remix)”", 14, t["ink"], VERD, 700)
    c.text(40, 904, "by DJ Thirty Seconds ft. Chai", 12, t["soft"], VERD)
    c.add('<rect x="40" y="918" width="300" height="10" rx="5" fill="#00000022"/><rect class="play" x="40" y="918" width="300" height="10" rx="5" fill="url(#aqua)"/>')
    # right column: blurb + top 8 + comments
    box(c, t, 424, 186, 752, 190, "Krishna's Blurbs")
    c.text(440, 232, "About me:", 15, t["hot"], VERD, 700)
    lines = ["EEE engineer @ Indo Tech Transformers (Kanchipuram!!). I test transformers",
             "& then write the software the whole plant runs on. 9 apps in production,",
             "128 tests, 1 patent filed (street lights that FOLLOW YOUR CAR omg).",
             "Ranked #7 out of 1500+ colleges @ IIT Bombay NEC. no big deal. ok it's a big deal."]
    for i, l in enumerate(lines):
        c.text(440, 260 + i * 24, l, 14, t["ink"], VERD)
    c.text(440, 362, "Who I'd like to meet: anyone with a spreadsheet they hate.", 14, t["link"], VERD, extra='text-decoration="underline"')
    box(c, t, 424, 392, 752, 400, "Krishna's Friend Space · Top 8")
    c.text(1160, 413, "Krishna has 10 projects", 12, "#FFFFFF", VERD, anchor="end")
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS[:8]):
        x, y = 444 + (i % 4) * 182, 440 + (i // 4) * 172
        c.add(f'<rect x="{x}" y="{y}" width="160" height="110" rx="6" fill="url(#aqua)" stroke="#FFFFFF" stroke-width="2"/>'
              + icon(slug, x + 45, y + 15, 70, "#FFFFFF", "#0B3D91", "#1F6FD1"))
        c.text(x + 80, y + 132, short(name), 14, t["link"], VERD, 700, "middle", 'text-decoration="underline"')
        c.text(x + 80, y + 150, "● online" if status in ("PRODUCTION", "LIVE") else "○ away", 11, "#2ECC40" if status in ("PRODUCTION", "LIVE") else t["soft"], VERD, anchor="middle")
    box(c, t, 424, 808, 752, 140, "Friends Comments")
    c.text(440, 856, "Chai says:", 13, t["hot"], VERD, 700)
    c.text(440, 878, "“we're out again. you used all of us on the dispatch release.”", 13, t["ink"], VERD)
    c.text(440, 912, "Past Krishna (2023) says:", 13, t["hot"], VERD, 700)
    c.text(440, 934, "“started on the railways. told you it would work out.”", 13, t["ink"], VERD)
    # aqua buttons + counter
    for i, lab in enumerate(["Add to Friends", "Send Message", "Hire Krishna"]):
        x = 24 + i * 250
        c.add(f'<rect x="{x}" y="970" width="230" height="44" rx="22" fill="url(#aqua)" stroke="#FFFFFF" stroke-width="2"/>'
              f'<rect x="{x + 10}" y="974" width="210" height="16" rx="8" fill="#FFFFFF" opacity=".55"/>')
        c.text(x + 115, 998, lab, 15, "#0B3D91", VERD, 700, "middle")
    c.add(f'<rect x="900" y="970" width="276" height="44" fill="#000"/>')
    c.text(1038, 998, "visitors: 0 0 4 2 0 0 4", 18, "#39FF14", "'Courier New', monospace", 700, "middle")
    sparkles(c, [(370, 110, 14), (700, 120, 10), (1150, 150, 16), (380, 260, 10), (1120, 420, 12), (390, 840, 12), (860, 990, 10)])
    c.css.append(".play{transform-box:fill-box;transform-origin:left;animation:pl 8s linear infinite}@keyframes pl{from{transform:scaleX(0)}}")
    c.save(f"page-{th}.svg", f"KrishSpace, a 2006-style social profile for {NAME}: about me, details, now playing, a Top 8 of projects, comments, and buttons to add, message or hire.")

links = " · ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Y2K: a 2006 social profile, glossy aqua and chrome. Light (sky) and dark (midnight) follow your GitHub theme. Built by scripts/gen_y2k.py -->

<p align="center">{pic(F, "page", f"KrishSpace profile for {NAME}")}</p>

<p align="center">
  <a href="mailto:{EMAIL}"><img src="https://img.shields.io/badge/✉_Send_Message-2E9BEA?style=for-the-badge" alt="Email"/></a>
  <a href="{LINKEDIN}"><img src="https://img.shields.io/badge/★_Add_to_Friends-FF3399?style=for-the-badge" alt="LinkedIn"/></a>
  <a href="https://krishna-ittl.github.io/Candidate-Screener/"><img src="https://img.shields.io/badge/♫_Play_Job_Lens-6BA4E8?style=for-the-badge" alt="Job Lens"/></a>
</p>

<p align="center"><b>~*~ Top 8, clickable ~*~</b><br/>{links}</p>

<p align="center"><sub>best viewed in any browser at 1024×768 ✨ sign my guestbook: {EMAIL}</sub></p>
""")
print("ok")
