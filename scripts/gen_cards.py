"""Card-based profile: a collectible trading-card set. One holo card per project plus a legendary card of me.
Cards carry their own colours, so a single version works on light and dark pages. Run: python scripts/gen_cards.py [photo]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, icon, pic, write_readme, photo_grid, wrap
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short

F = "cards"
FONT = "'Gill Sans', 'Gill Sans MT', 'Trebuchet MS', 'Segoe UI', Arial, sans-serif"
TYPES = {"Electric": ("#F7D02C", "#FFF3B0", "⚡"), "Steel": ("#9DB7C9", "#E3EEF5", "⚙"), "Psychic": ("#C77DFF", "#F0DDFF", "◉"),
         "Shadow": ("#6C7A89", "#DCE3EA", "◆"), "Fighting": ("#F08A4B", "#FFE1CC", "✊"), "Grass": ("#6BCB77", "#DDF7E0", "✿"), "Water": ("#4D96FF", "#DCEBFF", "≈")}
# slug: type, hp, (attack, cost, dmg), (attack, cost, dmg), weakness, flavour
DECK = {
    "dispatch": ("Steel", 128, ("Gate Pass", 1, 50), ("Auto-Escalate", 2, 128), "Phone calls", "Moves transformers out the gate without a single phone call."),
    "job-lens": ("Psychic", 100, ("Rubric Scan", 1, 40), ("Shortlist", 2, 100), "Bias", "Reads every resume. Remembers the best ones."),
    "kiosk-sentinel": ("Shadow", 180, ("Lock Screen", 1, 30), ("Power-Cut Recovery", 2, 120), "None found", "Logs you out at the moment you paused. Not a second later."),
    "test-planner": ("Electric", 90, ("Schedule", 1, 40), ("IEC 60076 Combo", 3, 90), "Delays", "Forty tests, many units, one plan."),
    "hardware": ("Steel", 60, ("PDF Parse", 1, 30), ("Weighted BOM", 2, 60), "Scanned PDFs", "Finishes before the Excel window opens."),
    "street-light": ("Electric", 160, ("Light Bubble", 1, 60), ("GPS Fault Alert", 2, 100), "Daylight", "Follows the car. Saves 60% of the energy. Patent filed."),
    "rtcc": ("Fighting", 48, ("Follow-Up", 1, 48), ("Escalate", 2, 96), "Out-of-office", "Sends the reminder you forgot to send. Every 48 hours."),
    "industrial-data": ("Grass", 90, ("QR Capture", 1, 40), ("3D Render", 2, 80), "Paper forms", "Every test reading, tagged and traceable."),
    "hwe-tool": ("Electric", 30, ("Feeder Classify", 1, 30), ("I/O Budget", 2, 60), "Manual calcs", "30 minutes of MCC paperwork. Thirty seconds."),
    "flood": ("Water", 90, ("Rising Alert", 1, 50), ("Outage Shield", 2, 90), "Silence", "Cuts outage risk by 90%."),
}
photo = photo_grid(F, 40, sys.argv[1] if len(sys.argv) > 1 else None)
W, H = 420, 588


def frame(c, ty_col, holo=False):
    c.defs.append('<linearGradient id="holo" x1="0" y1="0" x2="1" y2="1"><stop offset=".3" stop-color="#fff" stop-opacity="0"/>'
                  '<stop offset=".45" stop-color="#7DF9FF" stop-opacity=".28"/><stop offset=".5" stop-color="#FF7DF0" stop-opacity=".32"/>'
                  '<stop offset=".55" stop-color="#FFF27D" stop-opacity=".28"/><stop offset=".7" stop-color="#fff" stop-opacity="0"/></linearGradient>'
                  '<linearGradient id="rainbow" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF5F6D"/><stop offset=".25" stop-color="#FFC371"/>'
                  '<stop offset=".5" stop-color="#47E891"/><stop offset=".75" stop-color="#4D96FF"/><stop offset="1" stop-color="#C77DFF"/></linearGradient>'
                  '<filter id="sh"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-opacity=".35"/></filter>'
                  f'<clipPath id="card"><rect x="10" y="10" width="{W - 20}" height="{H - 20}" rx="20"/></clipPath>')
    c.add(f'<rect x="10" y="10" width="{W - 20}" height="{H - 20}" rx="20" fill="{"url(#rainbow)" if holo else "#F5C842"}" filter="url(#sh)"/>'
          f'<rect x="24" y="24" width="{W - 48}" height="{H - 48}" rx="12" fill="{ty_col}"/>')


def shimmer(c):
    c.add(f'<g clip-path="url(#card)"><rect class="holo" x="-420" y="0" width="{W * 2}" height="{H}" fill="url(#holo)"/></g>')
    c.css.append(".holo{animation:ho 3.6s ease-in-out infinite}@keyframes ho{0%{transform:translateX(0)}60%,100%{transform:translateX(840px)}}")


for n, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS, 1):
    ty, hp, a1, a2, weak, flav = DECK[slug]
    col, light, sym = TYPES[ty]
    c = Canvas(F, {}, W, H)
    frame(c, col)
    c.text(38, 54, "BASIC", 11, "#333", FONT, 700, extra='letter-spacing="1.5"')
    c.text(38, 82, short(name), 25, "#111", FONT, 700)
    c.text(W - 72, 80, f"HP {hp}", 18, "#C0262D", FONT, 700, "end")
    c.add(f'<circle cx="{W - 50}" cy="74" r="14" fill="{light}" stroke="#333" stroke-width="1.5"/>')
    c.text(W - 50, 80, sym, 15, "#333", FONT, 700, "middle")
    # art window
    c.add(f'<rect x="38" y="96" width="{W - 76}" height="200" fill="{light}" stroke="#B8962E" stroke-width="5"/>'
          f'<circle cx="{W / 2}" cy="196" r="78" fill="{col}" opacity=".45"/>' + icon(slug, W / 2 - 62, 134, 124, "#FFFFFF", "#222", col))
    c.add("".join(f'<path class="spark" style="animation-delay:{i * .5}s" d="M{x},{y} l4,10 10,4 -10,4 -4,10 -4,-10 -10,-4 10,-4z" fill="#FFF"/>'
                  for i, (x, y) in enumerate([(80, 120), (330, 140), (300, 260)])))
    c.add(f'<rect x="58" y="300" width="{W - 116}" height="22" fill="#E8D48A" stroke="#B8962E"/>')
    c.text(W / 2, 316, f"{ty}-type shop-floor build · {status.title()}", 11, "#333", FONT, 600, "middle", 'font-style="italic"')
    for i, (an, cost, dmg) in enumerate([a1, a2]):
        y = 362 + i * 68
        c.text(38, y, "●" * cost, 16, "#333", FONT)
        c.text(38 + cost * 14 + 10, y, an, 20, "#111", FONT, 700)
        c.text(W - 38, y, str(dmg), 22, "#111", FONT, 700, "end")
        detail = hook if i == 0 else impact
        c.text(38, y + 22, detail[:52], 12, "#333", FONT)
        c.add(f'<line x1="38" x2="{W - 38}" y1="{y + 38}" y2="{y + 38}" stroke="#333" stroke-opacity=".25"/>')
    c.text(38, 506, f"weakness: {weak}", 12, "#333", FONT, 600)
    c.text(W - 38, 506, f"resistance: manual work −30", 12, "#333", FONT, 600, "end")
    c.text(38, 530, flav, 11, "#333", FONT, extra='font-style="italic"')
    c.text(38, 552, f"KRS {n:02d}/10 · {stack}", 10, "#333", FONT)
    c.text(W - 38, 552, "★" if status in ("PRODUCTION", "LIVE", "PATENT FILED") else "◆", 14, "#111", FONT, 700, "end")
    c.css.append(".spark{transform-box:fill-box;transform-origin:center;animation:sp 1.5s ease-in-out infinite}@keyframes sp{50%{transform:scale(.3);opacity:.2}}")
    if status in ("PRODUCTION", "LIVE", "PATENT FILED"):
        shimmer(c)
    c.save(f"card-{slug}.svg", f"Trading card {n:02d}/10: {name}, {ty} type, HP {hp}. Attacks: {a1[0]} {a1[2]} ({hook}); {a2[0]} {a2[2]} ({impact}). {flav}")

# the legendary card
c = Canvas(F, {}, W, H)
frame(c, "#20123A", holo=True)
c.text(38, 54, "LEGENDARY · ENGINEER", 11, "#FFD86B", FONT, 700, extra='letter-spacing="1.5"')
c.text(38, 82, NAME, 25, "#FFFFFF", FONT, 700)
c.text(W - 38, 80, "HP 2004", 18, "#FF7DF0", FONT, 700, "end")
c.add(f'<rect x="38" y="96" width="{W - 76}" height="220" fill="#0D0720" stroke="url(#rainbow)" stroke-width="5"/>')
cell = 5.2
for r, row in enumerate(photo):
    for q, ch in enumerate(row):
        if ch != "." and int(ch) > 0:
            c.add(f'<rect x="{W / 2 - 20 * cell + q * cell:.1f}" y="{104 + r * cell:.1f}" width="{cell - .6:.1f}" height="{cell - .6:.1f}" '
                  f'fill="{["#2B1055", "#3E1A78", "#5B2A9E", "#7B3FC4", "#A04FD8", "#C86BE0", "#F08AD8", "#FFB0C8", "#FFD8A8", "#FFF2C8"][int(ch)]}"/>')
c.add(f'<rect x="58" y="322" width="{W - 116}" height="22" fill="#FFD86B" opacity=".9"/>')
c.text(W / 2, 338, "Electric / Code dual type · Chennai, 2004", 11, "#20123A", FONT, 700, "middle", 'font-style="italic"')
c.text(38, 380, "Ability: Chai Engine", 15, "#FF7DF0", FONT, 700)
c.text(38, 398, "Never runs out of energy between shifts.", 12, "#E8DFFF", FONT)
for i, (an, dmg, d) in enumerate([("30-Second Strike", 30, "Turns any 30-minute chore into 30 seconds."),
                                  ("Ohm's Law × Git", 9000, "Fluent in both. Damage cannot be resisted.")]):
    y = 434 + i * 50
    c.text(38, y, an, 19, "#FFFFFF", FONT, 700)
    c.text(W - 38, y, str(dmg), 21, "#FFD86B", FONT, 700, "end")
    c.text(38, y + 20, d, 12, "#E8DFFF", FONT)
c.text(38, 530, "Patent filed · NEC #7 of 1500+ · 9 apps in production", 11, "#FFD86B", FONT, 600)
c.text(38, 552, "KRS 00/10 · secret rare", 10, "#E8DFFF", FONT)
c.text(W - 38, 552, "★★★", 14, "#FFD86B", FONT, 700, "end")
shimmer(c)
c.save("card-legend.svg", f"Legendary card: {NAME}, Electric/Code dual type, HP 2004. Ability Chai Engine. Attacks: 30-Second Strike, Ohm's Law times Git 9000.")

cards = []
for p in PROJECTS:
    img = pic(F, f"card-{p[0]}", f"Trading card: {p[1]}", "32%", themed=False)
    cards.append(f'<a href="{p[3]}">{img}</a>' if p[3] else img)
rows = "\n".join("<p align=\"center\">\n  " + "\n  ".join(cards[i:i + 3]) + "\n</p>" for i in range(0, 10, 3))
write_readme(f"""
<!-- Card-based design as a trading-card set. Each card is self-coloured, so it reads on light and dark GitHub themes. Built by scripts/gen_cards.py -->

<h1 align="center">KRISH · the trading card game</h1>
<p align="center"><i>11 cards. 1 legendary. 0 spreadsheets in the deck.</i></p>

<p align="center">{pic(F, "card-legend", f"Legendary card: {NAME}", "40%", themed=False)}</p>

<p align="center">
  <a href="mailto:{EMAIL}"><img src="https://img.shields.io/badge/Trade_with_me-F5C842?style=for-the-badge&logo=gmail&logoColor=111111" alt="Email"/></a>
  <a href="{LINKEDIN}"><img src="https://img.shields.io/badge/LinkedIn-20123A?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
</p>

### The set

{rows}

<details>
<summary><b>📖 How to play</b></summary>

1. Pick a card. Holo cards (✦ shimmer) are in production or live right now.
2. Click it. Cards with a link open the real project; locked ones are company-internal or hardware.
3. Every attack is a real feature. Every HP is a real number from the project, give or take some game balance.
4. The legendary card cannot be collected. It can only be hired: **{EMAIL}**

</details>
""")
print("ok")
