"""Generates the clay-style SVG panels for this profile README.

Edit the text below, then run:  python scripts/gen_clay.py
The ASCII portrait is read from assets/clay/portrait.txt (made by scripts/portrait.py).
Every panel carries its own backdrop, so the page looks the same in light and dark mode.
"""
import os
from xml.sax.saxutils import escape as esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "clay")

INK, SOFT, PLUM, SHADOW = "#2B2140", "#6B5F80", "#7C5CD6", "#6E56A8"
BOARD_A, BOARD_B = "#F1EAFB", "#FBEFEA"
PEACH, MINT, LILAC, BUTTER, SKY, PINK = "#FFCBAE", "#BDEBD6", "#D9CBFA", "#FFE7A6", "#C4DEF8", "#FAC6D8"
FONT = "ui-rounded, 'SF Pro Rounded', 'Segoe UI Variable Display', 'Segoe UI', Nunito, system-ui, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
REDUCE = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

DEFS = f"""<linearGradient id="board" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BOARD_A}"/><stop offset="1" stop-color="{BOARD_B}"/></linearGradient>
<filter id="clay" x="-15%" y="-15%" width="135%" height="145%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="7" result="b"/>
  <feOffset in="b" dx="-6" dy="-8" result="up"/>
  <feComposite in="SourceAlpha" in2="up" operator="arithmetic" k2="1" k3="-1" result="rimBR"/>
  <feFlood flood-color="{SHADOW}" flood-opacity=".28"/><feComposite in2="rimBR" operator="in" result="shade"/>
  <feOffset in="b" dx="6" dy="8" result="down"/>
  <feComposite in="SourceAlpha" in2="down" operator="arithmetic" k2="1" k3="-1" result="rimTL"/>
  <feFlood flood-color="#fff" flood-opacity=".85"/><feComposite in2="rimTL" operator="in" result="light"/>
  <feGaussianBlur in="SourceAlpha" stdDeviation="11"/><feOffset dx="9" dy="14" result="ds"/>
  <feFlood flood-color="{SHADOW}" flood-opacity=".26"/><feComposite in2="ds" operator="in" result="drop"/>
  <feMerge><feMergeNode in="drop"/><feMergeNode in="SourceGraphic"/><feMergeNode in="shade"/><feMergeNode in="light"/></feMerge>
</filter>"""


def write(name, w, h, body, title, style=""):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
           f'aria-label="{esc(title)}"><title>{esc(title)}</title><defs>{DEFS}</defs>'
           f'<style>{style}{REDUCE}</style>'
           f'<rect width="{w}" height="{h}" rx="34" fill="url(#board)"/>{body}</svg>\n')
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def blob(x, y, w, h, fill, rx=28):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" filter="url(#clay)"/>'


def text(x, y, s, size, fill=INK, weight=400, anchor="start", font=FONT, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')


def pill(x, y, label, fill, size=16):
    w = 30 + len(label) * size * .56
    return blob(x, y, w, 40, fill, 20) + text(x + w / 2, y + 26, label, size, INK, 600, "middle"), w


def title_row(y, kicker, heading):
    return text(48, y, kicker, 15, PLUM, 700, extra='letter-spacing="2"') + text(48, y + 40, heading, 34, INK, 800)


# ─────────────────────────── HERO: ASCII portrait + intro ───────────────────────────
art = open(os.path.join(OUT, "portrait.txt"), encoding="utf-8").read().split("\n")
CW, LH = 4.6, 8.7
PX, PY = 318 - 58 * CW, 606 - (len(art) - 1) * LH  # centred, bust cropped by the frame bottom
rows = "".join(
    f'<text x="{PX}" y="{PY + i * LH:.1f}" textLength="{len(line) * CW:.1f}" lengthAdjust="spacingAndGlyphs" '
    f'xml:space="preserve">{esc(line)}</text>'
    for i, line in enumerate(art) if line.strip())
currently = ["deleting another spreadsheet", "teaching kiosks to survive power cuts", "shipping before the chai gets cold"]
cur = "".join(
    f'<text class="cur c{i}" x="676" y="540" font-family="{MONO}" font-size="18" fill="{INK}">'
    f'<tspan fill="{PLUM}" font-weight="700">currently:</tspan> {esc(c)}</text>' for i, c in enumerate(currently))
p1, w1 = pill(642, 438, "⚡ EEE engineer", PEACH)
p2, w2 = pill(642 + w1 + 14, 438, "📜 Patent holder", MINT)
p3, _ = pill(642 + w1 + w2 + 28, 438, "🏆 NEC rank #7", BUTTER)
hero = f"""
{blob(40, 40, 556, 560, LILAC, 40)}
<clipPath id="frame"><rect x="40" y="40" width="556" height="560" rx="40"/></clipPath>
<g clip-path="url(#frame)">
  <linearGradient id="ink" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{INK}"/><stop offset="1" stop-color="{PLUM}"/></linearGradient>
  <g font-family="{MONO}" font-size="8.3" fill="url(#ink)">{rows}</g>
  <rect class="scan" x="40" y="0" width="556" height="70" fill="#fff" opacity=".35"/>
</g>
{blob(642, 52, 236, 42, "#FFFFFF", 21)}
{text(760, 80, "👋  hey, I'm Krishna", 18, INK, 700, "middle")}
{text(640, 172, "Krishna Raju S", 66, INK, 800, extra='letter-spacing="-1.5"')}
{text(642, 230, "Electrical engineer by degree.", 31, INK, 700)}
{text(642, 272, "Software engineer by audacity.", 31, PLUM, 800)}
{text(642, 326, "I turn 30-minute chores into 30-second clicks.", 20, SOFT)}
{text(642, 356, "Nine of my apps run Indo Tech Transformers' shop floor,", 20, SOFT)}
{text(642, 386, "every shift. The spreadsheets never saw it coming.", 20, SOFT)}
{p1}{p2}{p3}
{cur}
<rect class="caret" x="642" y="527" width="10" height="17" rx="3" fill="{PLUM}"/>"""
write("hero.svg", 1200, 640, hero,
      "ASCII portrait of Krishna Raju S. Electrical engineer by degree, software engineer by audacity. "
      "I turn 30-minute chores into 30-second clicks. Nine of my apps run Indo Tech Transformers' shop floor.",
      """.scan{animation:scan 5s ease-in-out infinite}@keyframes scan{0%{transform:translateY(0)}100%{transform:translateY(640px)}}
.cur{opacity:0;animation:cyc 12s infinite}.c0{opacity:1}.c1{animation-delay:4s}.c2{animation-delay:8s}
@keyframes cyc{0%{opacity:0}4%,30%{opacity:1}34%,100%{opacity:0}}
.caret{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}""")

# ─────────────────────────── RECEIPTS ───────────────────────────
receipts = [("9", "apps in production", PEACH), ("128", "tests guarding dispatch", MINT),
            ("30m→30s", "a BOM chore, automated", SKY), ("#7", "of 1500+ colleges, IIT B NEC", PINK)]
tw = (1200 - 96 - 3 * 24) / 4
tiles = "".join(
    blob(48 + i * (tw + 24), 118, tw, 150, c, 30)
    + text(48 + i * (tw + 24) + 26, 190, n, 46 if len(n) < 5 else 38, INK, 800)
    + text(48 + i * (tw + 24) + 26, 236, l, 17, SOFT, 600)
    for i, (n, l, c) in enumerate(receipts))
write("receipts.svg", 1200, 310, title_row(58, "NUMBERS DON'T FLIRT. THEY JUST FLEX.", "The receipts 🧾") + tiles,
      "The receipts: 9 apps in production, 128 tests guarding dispatch, a 30-minute BOM chore automated to 30 seconds, rank 7 of 1500+ colleges at IIT Bombay NEC")

# ─────────────────────────── PROJECT CARDS ───────────────────────────
STATUS = {"IN PRODUCTION": MINT, "LIVE DEMO": PINK, "IN USE": MINT, "NEW": SKY, "BUILT": LILAC, "IN DESIGN": BUTTER}
cards = [
    ("dispatch", "🚚", "Dispatch Management", PEACH, "IN PRODUCTION",
     ["Work order to gate pass, zero phone calls.", "Runs dispatch on the shop floor every shift."], "React 19 · Supabase · PL/pgSQL"),
    ("job-lens", "🔍", "Job Lens", LILAC, "LIVE DEMO",
     ["100 resumes in. A ranked shortlist out.", "Rubric-scored, ATS-checked, works offline."], "TypeScript · Transformers.js · OCR"),
    ("kiosk-sentinel", "🔐", "KioskSentinel", MINT, "NEW",
     ["Attendance that survives power cuts", "and pranksters. Offline-first, 3 shifts."], "Java 21 · SQLite · PostgreSQL"),
    ("test-planner", "🧪", "Transformer Test Planner", SKY, "LIVE DEMO",
     ["Every IEC 60076 test, planned for every unit.", "Live status board, one-click Excel."], "TypeScript · Next.js · Vercel"),
    ("rtcc", "🧰", "RTCC & M.Box Tracker", BUTTER, "IN USE",
     ["Chases pending points so nobody has to.", "Polite follow-up emails every 48 hours."], "React · Express · node-cron"),
    ("fasteners", "🔩", "Fasteners Automation", PINK, "IN USE",
     ["A 30-minute job, now 30 seconds.", "Hardware PDF in, weighted BOM out."], "Python · Pandas · PyQt5"),
]
for slug, icon, name, color, status, desc, stack in cards:
    sp, _ = pill(0, 0, status, STATUS[status], 13)
    body = f"""{blob(24, 24, 552, 292, color, 34)}
{blob(52, 52, 64, 64, "#FFFFFF", 22)}{text(84, 95, icon, 30, INK, 400, "middle")}
{text(134, 80, name, 26, INK, 800)}
<g transform="translate(134,92)">{sp}</g>
{text(52, 176, desc[0], 20, INK, 600)}{text(52, 206, desc[1], 20, SOFT)}
<rect x="52" y="236" width="496" height="52" rx="18" fill="#fff" opacity=".55"/>
{text(72, 268, stack, 16, INK, 600, font=MONO)}"""
    write(f"card-{slug}.svg", 600, 340, body, f"{name}: {' '.join(desc)}")

minis = [("epms", "📅", "EPMS", "Gantt-powered project HQ", LILAC),
         ("industrial-data", "📡", "Industrial Data", "QR capture + a 3D model", SKY),
         ("dmat", "🧠", "dMAT Practice", "A whole exam in 1 HTML file", MINT),
         ("shop-floor", "🏭", "Shop Floor Status", "In design: live bay status", BUTTER)]
for slug, icon, name, line, color in minis:
    write(f"mini-{slug}.svg", 300, 190, f"""{blob(18, 18, 264, 154, color, 28)}
{text(46, 76, icon, 30)}{text(46, 116, name, 24, INK, 800)}{text(46, 146, line, 17, SOFT, 600)}""", f"{name}: {line}")

# ─────────────────────────── TROPHY SHELF ───────────────────────────
trophies = [("2024", "National finalist", "Technical symposium", PEACH),
            ("2025", "Patent holder", "Smart street-light faults", MINT),
            ("2025", "Rank #7 of 1500+", "IIT Bombay NEC", BUTTER),
            ("2025", "Runner-up", "Fish Tank, E-Summit", PINK),
            ("2026", "9 apps shipped", "Indo Tech Transformers", SKY)]
tw = (1200 - 96 - 4 * 20) / 5
shelf = "".join(
    blob(48 + i * (tw + 20), 128, tw, 170, c, 30)
    + blob(48 + i * (tw + 20) + 20, 146, 70, 32, "#FFFFFF", 16)
    + text(48 + i * (tw + 20) + 55, 168, y, 15, PLUM, 800, "middle", MONO)
    + text(48 + i * (tw + 20) + 20, 230, t, 19, INK, 800)
    + text(48 + i * (tw + 20) + 20, 262, s, 15, SOFT, 600)
    for i, (y, t, s, c) in enumerate(trophies))
write("trophies.svg", 1200, 340, title_row(58, "BRAGGING, BUT WITH DATES", "Trophy shelf 🏆")
      + f'<rect x="48" y="304" width="1104" height="12" rx="6" fill="{LILAC}" filter="url(#clay)"/>' + shelf,
      "Trophy shelf: 2024 national finalist; 2025 patent holder, rank 7 of 1500+ colleges at IIT Bombay NEC, runner-up at IIT Bombay E-Summit Fish Tank; 2026 nine apps shipped at Indo Tech Transformers")

# ─────────────────────────── TOOLBOX ───────────────────────────
groups = [("On the factory floor", PEACH, ["IEC 60076 testing", "MCC panels", "Protection relays", "OLTC", "ESP8266 · IoT", "Proteus"]),
          ("In the code", LILAC, ["TypeScript", "React", "Next.js", "Python", "Java", "Node · Express", "Supabase", "PostgreSQL", "Three.js"]),
          ("With AI", MINT, ["Claude", "OpenAI", "LangChain", "LangGraph", "Transformers.js", "Tesseract OCR"])]
gw = (1200 - 96 - 2 * 24) / 3
tool = ""
for i, (head, color, items) in enumerate(groups):
    gx = 48 + i * (gw + 24)
    tool += blob(gx, 118, gw, 250, color, 32) + text(gx + 26, 162, head, 21, INK, 800)
    cx, cy = gx + 24, 184
    for it in items:
        w = 26 + len(it) * 8.6
        if cx + w > gx + gw - 20:
            cx, cy = gx + 24, cy + 46
        tool += f'<rect x="{cx}" y="{cy}" width="{w:.0f}" height="34" rx="17" fill="#fff" opacity=".7"/>' + text(cx + w / 2, cy + 23, it, 15, INK, 600, "middle")
        cx += w + 8
write("toolbox.svg", 1200, 410, title_row(58, "WHAT I BRING TO THE FIGHT", "Toolbox 🧰") + tool,
      "Toolbox. Factory floor: IEC 60076 testing, MCC panels, protection relays, OLTC, ESP8266, Proteus. Code: TypeScript, React, Next.js, Python, Java, Node, Express, Supabase, PostgreSQL, Three.js. AI: Claude, OpenAI, LangChain, LangGraph, Transformers.js, Tesseract OCR.")

# ─────────────────────────── FOOTER ───────────────────────────
write("footer.svg", 1200, 300, f"""{blob(48, 40, 1104, 220, LILAC, 40)}
{text(600, 112, "You bring the boring process.", 26, SOFT, 600, "middle")}
{text(600, 166, "I'll bring the button.", 50, INK, 800, "middle", extra='letter-spacing="-1"')}
{blob(372, 192, 456, 44, "#FFFFFF", 22)}
{text(600, 220, "krishnarajus2004@gmail.com", 18, PLUM, 700, "middle", MONO)}""",
      "You bring the boring process. I'll bring the button. krishnarajus2004@gmail.com")
print("ok")
