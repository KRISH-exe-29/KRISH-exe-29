"""Generates the SVG assets for this profile README.

Edit the text below (taglines, stats, projects, milestones), then run:  python scripts/gen_assets.py
"""
import math, os
from xml.sax.saxutils import escape as esc

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(os.path.join(OUT, "cards"), exist_ok=True)

INK, CARD, LINE, TEXT, MUTED = "#0A0A12", "#12121C", "#26263A", "#EDEDF5", "#9A9AB0"
VIOLET, PINK, PEACH, TEAL, SKY = "#A78BFA", "#F472B6", "#FDBA74", "#2DD4BF", "#60A5FA"
SANS = "'Segoe UI', Inter, -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
REDUCE = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
GRAD = f"""<linearGradient id="g" x1="0" x2="1" y1="0" y2="0">
  <stop offset="0" stop-color="{VIOLET}"/><stop offset=".55" stop-color="{PINK}"/><stop offset="1" stop-color="{PEACH}"/>
</linearGradient>"""


def write(name, w, h, body, title):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
           f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>{body}</svg>\n')
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def sine(x0, x1, y, amp, period, phase, step=6):
    pts = [f"{x:.0f},{y + amp * math.sin(2 * math.pi * (x - x0) / period + phase):.1f}"
           for x in range(x0, x1 + 1, step)]
    return "M" + " L".join(pts)


def three_phase(x0, x1, y, amp, period, width=2.5, op=.9):
    """Three sine waves 120 degrees apart: the shape of the power a transformer factory ships."""
    out = []
    for i, c in enumerate((VIOLET, PINK, TEAL)):
        out.append(f'<path class="wave w{i}" d="{sine(x0, x1, y, amp, period, i * 2 * math.pi / 3)}" '
                   f'fill="none" stroke="{c}" stroke-width="{width}" stroke-linecap="round" opacity="{op}"/>')
    return "".join(out)


# ─────────────────────────── HERO ───────────────────────────
W, H = 1200, 470
taglines = [
    "Spreadsheets in. Apps out.",
    "30 minutes of manual entry → under 30 seconds.",
    "Patent holder  ·  IIT Bombay NEC #7  ·  9 apps shipped",
]
tag_svg = "".join(
    f'<text class="tag t{i}" x="72" y="352" font-family="{MONO}" font-size="21" fill="{TEXT}">'
    f'<tspan fill="{TEAL}">❯ </tspan>{esc(t)}</text>' for i, t in enumerate(taglines))
hero = f"""<defs>{GRAD}
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="70"/></filter>
<pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#fff" opacity=".09"/></pattern>
<clipPath id="clip"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{INK}" stop-opacity="1"/><stop offset=".45" stop-color="{INK}" stop-opacity=".2"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></linearGradient>
</defs>
<style>
.blob{{transform-box:fill-box;transform-origin:center;animation:drift 18s ease-in-out infinite alternate}}
.b2{{animation-duration:23s;animation-delay:-6s}} .b3{{animation-duration:27s;animation-delay:-12s}}
@keyframes drift{{0%{{transform:translate(0,0) scale(1)}}50%{{transform:translate(-60px,40px) scale(1.15)}}100%{{transform:translate(50px,-30px) scale(.9)}}}}
.wave{{stroke-dasharray:14 10;animation:flow 2.4s linear infinite}}
.w1{{animation-duration:2.9s}} .w2{{animation-duration:3.4s}}
@keyframes flow{{to{{stroke-dashoffset:-48}}}}
.tag{{opacity:0;animation:cycle 12s infinite}} .t0{{opacity:1}} .t1{{animation-delay:4s}} .t2{{animation-delay:8s}}
@keyframes cycle{{0%{{opacity:0;transform:translateY(8px)}}4%,30%{{opacity:1;transform:none}}34%,100%{{opacity:0;transform:translateY(-8px)}}}}
.pulse{{animation:pulse 2s ease-in-out infinite}}
@keyframes pulse{{50%{{opacity:.25}}}}
.caret{{animation:pulse 1s steps(1) infinite}}
{REDUCE}
</style>
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="{INK}"/>
  <g filter="url(#blur)">
    <circle class="blob" cx="930" cy="120" r="210" fill="{VIOLET}" opacity=".55"/>
    <circle class="blob b2" cx="1090" cy="330" r="170" fill="{PINK}" opacity=".45"/>
    <circle class="blob b3" cx="760" cy="400" r="150" fill="{TEAL}" opacity=".35"/>
  </g>
  <rect width="{W}" height="{H}" fill="url(#dots)"/>
  <rect width="{W}" height="{H}" fill="url(#fade)"/>
  <g transform="translate(0,0)">{three_phase(0, W, 418, 22, 300, 2.2, .8)}</g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="27.5" fill="none" stroke="#fff" stroke-opacity=".08"/>

<g>
  <text x="72" y="92" font-family="{MONO}" font-size="18" fill="{MUTED}">~/krish.exe <tspan fill="{VIOLET}">$</tspan> whoami<tspan class="caret" fill="{TEXT}"> ▍</tspan></text>
</g>
<g>
  <text x="68" y="182" font-family="{SANS}" font-size="88" font-weight="800" letter-spacing="-2.5" fill="{TEXT}">Krishna Raju</text>
</g>
<g>
  <text x="72" y="236" font-family="{SANS}" font-size="34" font-weight="700" fill="url(#g)">Electrical engineer. Software builder.</text>
  <text x="72" y="282" font-family="{SANS}" font-size="22" fill="{MUTED}">I build the software a transformer factory runs on, every shift.</text>
</g>
<g>{tag_svg}</g>

<g transform="translate(838,52)">
  <rect width="292" height="40" rx="20" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".12"/>
  <circle class="pulse" cx="22" cy="20" r="5" fill="{TEAL}"/>
  <text x="38" y="26" font-family="{SANS}" font-size="16" fill="{TEXT}">Digitalisation · Indo Tech Transformers</text>
</g>"""
write("hero.svg", W, H, hero, "Krishna Raju: electrical engineer and software builder. I build the software a transformer factory runs on.")

# ─────────────────────────── STATS ───────────────────────────
stats = [("9", "apps shipped", "to real users on a factory floor"),
         ("128", "automated tests", "guarding the dispatch system"),
         ("#7", "nationally", "IIT Bombay NEC, 1500+ colleges"),
         ("1", "patent", "smart street-light fault detection")]
tw, gap = 282, 24
tiles = []
for i, (num, label, sub) in enumerate(stats):
    x = i * (tw + gap)
    tiles.append(f"""<g transform="translate({x},0)">
  <rect x=".5" y=".5" width="{tw - 1}" height="179" rx="22" fill="{CARD}" stroke="{LINE}"/>
  <text x="28" y="86" font-family="{SANS}" font-size="62" font-weight="800" letter-spacing="-2" fill="url(#g)">{esc(num)}</text>
  <text x="28" y="122" font-family="{SANS}" font-size="20" font-weight="600" fill="{TEXT}">{esc(label)}</text>
  <text x="28" y="150" font-family="{SANS}" font-size="16" fill="{MUTED}">{esc(sub)}</text>
</g>""")
write("stats.svg", 1200, 180, f"""<defs>{GRAD}</defs>
{''.join(tiles)}""",
      "9 apps shipped, 128 automated tests, rank 7 nationally at IIT Bombay NEC, 1 patent")

# ─────────────────────────── PROJECT CARDS ───────────────────────────
CW, CH = 580, 300
STATUS = {"PRODUCTION": TEAL, "LIVE DEMO": PINK, "IN USE": TEAL, "BUILT": VIOLET, "NEW": SKY, "IN DESIGN": PEACH}
projects = [
    ("dispatch", "🚚", "Dispatch Management", VIOLET, "PRODUCTION",
     ["Work order → packing → loading → gate pass.", "Runs dispatch on the shop floor, every shift."],
     ["5 roles", "128 tests", "auto escalations"], "React 19 · Supabase · PL/pgSQL · Edge Functions"),
    ("job-lens", "🔍", "Job Lens", PINK, "LIVE DEMO",
     ["Every resume read. The best ones on top.", "Rubric scoring, ATS checks, HR pipeline."],
     ["offline AI", "OCR for scans", "Excel reports"], "TypeScript · React 19 · Transformers.js · Tesseract"),
    ("kiosk-sentinel", "🔐", "KioskSentinel", TEAL, "NEW",
     ["Lock-screen time & attendance for kiosk PCs.", "Survives power cuts. Syncs every 2 minutes."],
     ["3-shift dashboard", "offline-first", "locked down"], "Java 21 · SQLite · PostgreSQL · PowerShell"),
    ("test-planner", "🧪", "Transformer Test Planner", SKY, "LIVE DEMO",
     ["Plans every IEC 60076 test across units.", "Scheduler, live status board, Excel export."],
     ["40 tests", "multi-unit", "1-click Excel"], "TypeScript · Next.js · Vercel"),
    ("rtcc", "🧰", "RTCC & M.Box Tracker", PEACH, "IN USE",
     ["Inspection → testing → clearance, tracked.", "Chases pending points so nobody has to."],
     ["48h auto emails", "role-based", "no-code settings"], "React · Express · node-cron · Supabase"),
    ("industrial-data", "📡", "Industrial Data System", VIOLET, "BUILT",
     ["QR-tagged data capture for transformer tests.", "Multi-department portal with a 3D model."],
     ["QR codes", "OTP admin login", "Three.js"], "React · Express · Three.js · Netlify"),
    ("epms", "📅", "EPMS Project HQ", PINK, "BUILT",
     ["Projects, milestones, budgets, daily reports.", "Interactive Gantt behind a black-hole login."],
     ["Gantt", "5 roles", "budget & billing"], "TypeScript · React 19 · Supabase · Framer Motion"),
    ("fasteners", "🔩", "Fasteners Automation", TEAL, "IN USE",
     ["Drop a hardware PDF, get a weighted BOM.", "A 30-minute job now takes under 30 seconds."],
     ["30 min → <30 s", "Excel + PDF", "auto rounding"], "Python · Pandas · PyQt5 · VBA"),
    ("dmat", "🧠", "dMAT Master Practice", SKY, "LIVE DEMO",
     ["A complete exam simulator in one HTML file.", "Timed mocks, per-question timing, analytics."],
     ["990 checks", "works offline", "1 file"], "HTML · CSS · JavaScript"),
    ("shop-floor", "🏭", "Shop Floor Job Status", PEACH, "IN DESIGN",
     ["Live job status for every bay on the floor.", "Cycle-time norms meet worker efficiency."],
     ["phase 1", "cycle-time norms", "efficiency"], "Requirements · Flowcharts · Norms"),
]
for slug, icon, name, accent, status, desc, chips, stack in projects:
    sc = STATUS[status]
    chip_svg, cx = [], 32
    for c in chips:
        w = 24 + len(c) * 9.2
        chip_svg.append(f'<rect x="{cx}" y="196" width="{w:.0f}" height="32" rx="16" fill="{accent}" fill-opacity=".12" stroke="{accent}" stroke-opacity=".35"/>'
                        f'<text x="{cx + w / 2:.0f}" y="217" text-anchor="middle" font-family="{SANS}" font-size="16" fill="{TEXT}">{esc(c)}</text>')
        cx += w + 10
    body = f"""<defs>
<radialGradient id="glow" cx="1" cy="0" r="1"><stop offset="0" stop-color="{accent}" stop-opacity=".28"/><stop offset=".6" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{accent}" stop-opacity="0"/><stop offset=".5" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient>
<clipPath id="c"><rect width="{CW}" height="{CH}" rx="22"/></clipPath>
</defs>
<style>.shine{{animation:shine 6s ease-in-out infinite}}@keyframes shine{{0%,100%{{transform:translateX(-{CW}px)}}50%{{transform:translateX({CW}px)}}}}
.dot{{animation:p 2s ease-in-out infinite}}@keyframes p{{50%{{opacity:.3}}}}{REDUCE}</style>
<g clip-path="url(#c)">
  <rect width="{CW}" height="{CH}" fill="{CARD}"/>
  <rect width="{CW}" height="{CH}" fill="url(#glow)"/>
  <rect class="shine" width="{CW}" height="2" fill="url(#edge)"/>
</g>
<rect x=".5" y=".5" width="{CW - 1}" height="{CH - 1}" rx="21.5" fill="none" stroke="{LINE}"/>
<rect x="32" y="30" width="56" height="56" rx="16" fill="{accent}" fill-opacity=".14" stroke="{accent}" stroke-opacity=".4"/>
<text x="60" y="68" text-anchor="middle" font-size="28">{icon}</text>
<text x="106" y="60" font-family="{SANS}" font-size="27" font-weight="700" fill="{TEXT}">{esc(name)}</text>
<circle class="dot" cx="110" cy="80" r="4" fill="{sc}"/>
<text x="121" y="85" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="1" fill="{sc}">{esc(status)}</text>
<text font-family="{SANS}" font-size="19" fill="{MUTED}"><tspan x="32" y="128">{esc(desc[0])}</tspan><tspan x="32" y="156">{esc(desc[1])}</tspan></text>
{''.join(chip_svg)}
<line x1="32" x2="{CW - 32}" y1="250" y2="250" stroke="{LINE}"/>
<text x="32" y="278" font-family="{MONO}" font-size="15" fill="{accent}">{esc(stack)}</text>"""
    write(f"cards/{slug}.svg", CW, CH, body, f"{name}: {' '.join(desc)}")

# ─────────────────────────── MILESTONES ───────────────────────────
ms = [("2024", "National finalist", ["Competitive engineering", "technical symposium"]),
      ("2025", "Patent holder", ["Street lighting with", "automatic fault detection"]),
      ("2025", "Rank #7 nationally", ["IIT Bombay NEC,", "1500+ colleges"]),
      ("2025", "Runner-up", ["Fish Tank pitch,", "IIT Bombay E-Summit"]),
      ("2026", "9 apps shipped", ["Digitalisation team,", "Indo Tech Transformers"])]
nodes = []
for i, (yr, title, sub) in enumerate(ms):
    x = 120 + i * 240
    c = (VIOLET, PINK, PEACH, TEAL, SKY)[i]
    nodes.append(f"""<g>
  <text x="{x}" y="58" text-anchor="middle" font-family="{MONO}" font-size="17" fill="{MUTED}">{yr}</text>
  <circle cx="{x}" cy="100" r="15" fill="{c}" fill-opacity=".18"/><circle cx="{x}" cy="100" r="7" fill="{c}"/>
  <text x="{x}" y="154" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="700" fill="{TEXT}">{esc(title)}</text>
  <text text-anchor="middle" font-family="{SANS}" font-size="16" fill="{MUTED}"><tspan x="{x}" y="182">{esc(sub[0])}</tspan><tspan x="{x}" y="204">{esc(sub[1])}</tspan></text>
</g>""")
write("milestones.svg", 1200, 230, f"""<defs>{GRAD}</defs>
<line x1="120" x2="1080" y1="100" y2="100" stroke="{LINE}" stroke-width="3" stroke-linecap="round"/>
<line x1="120" x2="1080" y1="100" y2="100" stroke="url(#g)" stroke-width="3" stroke-linecap="round"/>
{''.join(nodes)}""", "Milestones: 2024 national finalist; 2025 patent holder, rank 7 at IIT Bombay NEC, runner-up at IIT Bombay E-Summit Fish Tank; 2026 nine apps shipped at Indo Tech Transformers")

# ─────────────────────────── DIVIDER ───────────────────────────
write("divider.svg", 1200, 40, f"""<defs>{GRAD}
<linearGradient id="m" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="k"><rect width="1200" height="40" fill="url(#m)"/></mask></defs>
<style>.wave{{stroke-dasharray:10 8;animation:flow 3s linear infinite}}@keyframes flow{{to{{stroke-dashoffset:-36}}}}{REDUCE}</style>
<g mask="url(#k)">{three_phase(200, 1000, 20, 7, 160, 1.6, .75)}</g>""", "")

# ─────────────────────────── FOOTER ───────────────────────────
write("footer.svg", 1200, 300, f"""<defs>{GRAD}
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
<clipPath id="clip"><rect width="1200" height="300" rx="28"/></clipPath></defs>
<style>.wave{{stroke-dasharray:14 10;animation:flow 2.6s linear infinite}}.w1{{animation-duration:3.1s}}.w2{{animation-duration:3.6s}}
@keyframes flow{{to{{stroke-dashoffset:-48}}}}{REDUCE}</style>
<g clip-path="url(#clip)">
  <rect width="1200" height="300" fill="{INK}"/>
  <g filter="url(#blur)"><circle cx="300" cy="300" r="180" fill="{VIOLET}" opacity=".4"/><circle cx="900" cy="300" r="180" fill="{PINK}" opacity=".35"/></g>
  {three_phase(0, 1200, 250, 18, 340, 2.2, .7)}
</g>
<rect x=".5" y=".5" width="1199" height="299" rx="27.5" fill="none" stroke="#fff" stroke-opacity=".08"/>
<text x="600" y="92" text-anchor="middle" font-family="{SANS}" font-size="26" fill="{MUTED}">Is your team still doing something by hand, every single day?</text>
<text x="600" y="150" text-anchor="middle" font-family="{SANS}" font-size="46" font-weight="800" letter-spacing="-1" fill="url(#g)">Let's make it run itself.</text>
<text x="600" y="196" text-anchor="middle" font-family="{MONO}" font-size="17" fill="{TEXT}" opacity=".8">krishnarajus2004@gmail.com  ·  linkedin.com/in/krishnarajus2004</text>""",
      "Is your team still doing something by hand every day? Let's make it run itself. krishnarajus2004@gmail.com")
print("ok")
