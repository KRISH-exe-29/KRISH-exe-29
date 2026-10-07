"""Skeuomorphic control-panel SVGs for the profile README: day (light) and night (dark) shifts.

Run:  python scripts/gen_panel.py   (facts live in scripts/profile_data.py)
"""
import math, os, sys
from xml.sax.saxutils import escape as esc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from profile_data import NAME, EMAIL, CITY, CGPA, PROJECTS, EXPERIENCE, WINS, CERTS, SKILLS

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "panel")
os.makedirs(OUT, exist_ok=True)
DIN = "Bahnschrift, 'DIN Alternate', 'D-DIN', 'Roboto Condensed', 'Arial Narrow', Arial, sans-serif"
TYPE = "'Courier New', Courier, 'Nimbus Mono PS', monospace"
BOLD = "'Arial Black', 'Helvetica Neue', Arial, sans-serif"
THEMES = {
    "light": dict(steel=("#E4E7EB", "#C9CED5"), edge="#8E959E", ink="#2A2F36", hi="#FFFFFF", plate=("#F4F5F6", "#C7CBD0"),
                  face="#FBFAF6", glow=0, wall="#B9BFC7", paper="#FFFDF6"),
    "dark": dict(steel=("#3A4048", "#23272D"), edge="#0E1013", ink="#E9ECEF", hi="#000000", plate=("#59606A", "#353A41"),
                 face="#FFF1CF", glow=1, wall="#15181C", paper="#E9E2CC"),
}
LED = {"PRODUCTION": "#39FF6A", "LIVE": "#39FF6A", "IN USE": "#FFB020", "SHIPPED": "#FFB020", "NEW": "#3FA9FF",
       "PATENT FILED": "#FF4FD8", "BUILT": "#B8C2CC"}
REDUCE = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


class Panel:
    def __init__(self, t, w, h):
        self.t, self.w, self.h, self.b = t, w, h, []

    def add(self, s):
        self.b.append(s)

    def steel(self, x, y, w, h, rx=14, colors=None):
        c = colors or self.t["steel"]
        gid = f"st{len(self.b)}"
        self.add(f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c[0]}"/><stop offset="1" stop-color="{c[1]}"/></linearGradient>'
                 f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{gid})" filter="url(#lift)"/>'
                 f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#fff" filter="url(#brush)"/>'
                 f'<rect x="{x + 1}" y="{y + 1}" width="{w - 2}" height="{h - 2}" rx="{rx}" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="1.5"/>'
                 f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="{self.t["edge"]}" stroke-width="1.5"/>')

    def screw(self, x, y, r=9, rot=30):
        self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#screw)" stroke="{self.t["edge"]}" stroke-width="1"/>'
                 f'<line x1="{x - r * .6}" x2="{x + r * .6}" y1="{y}" y2="{y}" stroke="#4A4F57" stroke-width="2.2" stroke-linecap="round" transform="rotate({rot} {x} {y})"/>')

    def screws(self, x, y, w, h, inset=22):
        for i, (sx, sy) in enumerate([(x + inset, y + inset), (x + w - inset, y + inset), (x + inset, y + h - inset), (x + w - inset, y + h - inset)]):
            self.screw(sx, sy, rot=20 + i * 37)

    def engrave(self, x, y, s, size, weight=700, anchor="start", font=DIN, fill=None, spacing=1):
        ink = fill or self.t["ink"]
        lit = ' filter="url(#backlit)"' if self.t["glow"] and fill is None else ""
        self.add(f'<text x="{x}" y="{y + 1.2}" font-family="{font}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
                 f'letter-spacing="{spacing}" fill="{self.t["hi"]}" opacity=".6">{esc(s)}</text>'
                 f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
                 f'letter-spacing="{spacing}" fill="{ink}"{lit}>{esc(s)}</text>')

    def led(self, x, y, color, r=8, blink=None):
        cls = f' class="{blink}"' if blink else ""
        self.add(f'<circle cx="{x}" cy="{y}" r="{r + 3}" fill="#1A1C20"/>'
                 f'<g{cls}><circle cx="{x}" cy="{y}" r="{r * (2.6 if self.t["glow"] else 1.8)}" fill="{color}" opacity=".35" filter="url(#bloom)"/>'
                 f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>'
                 f'<circle cx="{x - r * .35}" cy="{y - r * .35}" r="{r * .35}" fill="#fff" opacity=".7"/></g>')

    def dymo(self, x, y, s, tape="#111111", size=17):
        w = len(s) * size * .88 + 28
        self.add(f'<g transform="rotate(-.6 {x} {y})"><rect x="{x}" y="{y}" width="{w:.0f}" height="{size * 1.9:.0f}" rx="3" fill="{tape}" filter="url(#lift)"/>'
                 f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{size * 1.9:.0f}" rx="3" fill="#fff" opacity=".06" filter="url(#brush)"/>'
                 f'<text x="{x + 14}" y="{y + size * 1.32:.0f}" font-family="{BOLD}" font-size="{size}" letter-spacing="1.5" fill="#F6F6F6" '
                 f'filter="url(#emboss)">{esc(s.upper())}</text></g>')
        return w

    def save(self, name, title, style=""):
        t, w, h = self.t, self.w, self.h
        defs = f"""<filter id="brush" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency=".003 .85" numOctaves="2" seed="7"/>
  <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .22 -.04"/>
  <feComposite in2="SourceAlpha" operator="in"/></filter>
<filter id="lift" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#000" flood-opacity="{.5 if t['glow'] else .28}"/></filter>
<filter id="bloom" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="backlit" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur in="SourceGraphic" stdDeviation="3" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="emboss"><feOffset dy="1"/><feGaussianBlur stdDeviation=".3"/></filter>
<radialGradient id="screw" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#FDFDFD"/><stop offset=".6" stop-color="#A9AFB7"/><stop offset="1" stop-color="#6D737B"/></radialGradient>
<linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".45" stop-color="#9AA1AA"/><stop offset=".55" stop-color="#6B727B"/><stop offset="1" stop-color="#E3E6EA"/></linearGradient>
<linearGradient id="hazard" x1="0" y1="0" x2="1" y2="0"></linearGradient>
<pattern id="stripes" width="34" height="34" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="17" height="34" fill="#FFC400"/><rect x="17" width="17" height="34" fill="#151515"/></pattern>"""
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">'
               f'<title>{esc(title)}</title><defs>{defs}</defs>'
               f'<style>.blink{{animation:bl 1.4s steps(1) infinite}}.blink2{{animation:bl 2.3s steps(1) infinite .6s}}'
               f'@keyframes bl{{50%{{opacity:.15}}}}{style}{REDUCE}</style>'
               f'<rect width="{w}" height="{h}" rx="22" fill="{t["wall"]}"/>{"".join(self.b)}</svg>\n')
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(svg)


def gauge(p, cx, cy, r, value, vmax, label, unit, ticks=6, fmt="{:.0f}"):
    t = p.t
    a0, a1 = -120, 120
    ang = a0 + (a1 - a0) * min(value / vmax, 1)
    p.add(f'<circle cx="{cx}" cy="{cy}" r="{r + 14}" fill="url(#chrome)" filter="url(#lift)"/>'
          f'<circle cx="{cx}" cy="{cy}" r="{r + 4}" fill="#1D2025"/>'
          f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t["face"]}"/>')
    if t["glow"]:
        p.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFB547" opacity=".18" filter="url(#bloom)"/>')
    # red zone + ticks + numbers
    def pt(a, rr):
        rad = math.radians(a - 90)
        return cx + rr * math.cos(rad), cy + rr * math.sin(rad)
    za, zb = pt(80, r - 10), pt(120, r - 10)
    p.add(f'<path d="M{za[0]:.1f},{za[1]:.1f} A{r - 10},{r - 10} 0 0 1 {zb[0]:.1f},{zb[1]:.1f}" fill="none" stroke="#E5383B" stroke-width="7"/>')
    for i in range(ticks * 5 + 1):
        a = a0 + (a1 - a0) * i / (ticks * 5)
        major = i % 5 == 0
        x1, y1 = pt(a, r - 4)
        x2, y2 = pt(a, r - (18 if major else 11))
        p.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#222" stroke-width="{2.2 if major else 1}"/>')
        if major:
            nx, ny = pt(a, r - 32)
            p.add(f'<text x="{nx:.1f}" y="{ny + 5:.1f}" text-anchor="middle" font-family="{DIN}" font-size="13" fill="#222">{vmax * i // (ticks * 5)}</text>')
    p.add(f'<text x="{cx}" y="{cy + r * .42:.0f}" text-anchor="middle" font-family="{DIN}" font-size="13" font-weight="700" letter-spacing="1.5" fill="#444">{esc(unit)}</text>'
          f'<text x="{cx}" y="{cy + r * .66:.0f}" text-anchor="middle" font-family="{DIN}" font-size="22" font-weight="700" fill="#111">{esc(fmt.format(value))}</text>')
    # needle: sweeps up on load, then hunts around the reading like a real movement
    p.add(f'<g class="sweep" style="--a:{ang:.1f}deg;transform-origin:{cx}px {cy}px;transform:rotate({ang:.1f}deg)">'
          f'<g class="hunt" style="transform-origin:{cx}px {cy}px">'
          f'<polygon points="{cx - 3},{cy + 18} {cx + 3},{cy + 18} {cx + 1},{cy - r + 14} {cx - 1},{cy - r + 14}" fill="#D62828"/></g></g>'
          f'<circle cx="{cx}" cy="{cy}" r="10" fill="url(#chrome)"/>'
          f'<path d="M{cx - r * .8:.0f},{cy - r * .25:.0f} A{r},{r} 0 0 1 {cx + r * .8:.0f},{cy - r * .25:.0f} Q{cx},{cy - r * .55:.0f} {cx - r * .8:.0f},{cy - r * .25:.0f}Z" fill="#fff" opacity=".22"/>')
    p.engrave(cx, cy + r + 46, label, 16, anchor="middle", spacing=2)


GAUGE_CSS = (".sweep{animation:sweep 2.2s cubic-bezier(.3,1.4,.5,1) both}@keyframes sweep{from{transform:rotate(-120deg)}to{transform:rotate(var(--a))}}"
             ".hunt{animation:hunt 3.1s ease-in-out infinite 2.2s}@keyframes hunt{25%{transform:rotate(1.6deg)}60%{transform:rotate(-1.2deg)}}")

for theme, t in THEMES.items():
    # ── hero: transformer rating plate ──
    p = Panel(t, 1200, 600)
    p.steel(20, 20, 1160, 560, 18)
    p.screws(20, 20, 1160, 560)
    p.steel(70, 62, 760, 476, 10, t["plate"])
    for rx, ry in [(92, 84), (808, 84), (92, 516), (808, 516)]:
        p.screw(rx, ry, 7, 0)
    p.engrave(450, 112, "KRISH.EXE  ·  POWER TRANSFORMER  ·  RATING PLATE", 17, anchor="middle", spacing=3)
    p.add(f'<line x1="110" x2="790" y1="128" y2="128" stroke="{t["ink"]}" stroke-opacity=".5" stroke-width="1.5"/>')
    p.engrave(450, 190, NAME.upper(), 54, 800, "middle", spacing=4)
    p.engrave(450, 226, "ELECTRICAL ENGINEER  ·  SOFTWARE BUILDER", 18, anchor="middle", spacing=3)
    rows = [("RATED OUTPUT", "10 builds shipped"), ("VECTOR GROUP", "Ohm's Law ⇄ Git"),
            ("COOLING", "ONAN (chai-assisted)"), ("FREQUENCY", "ships daily"),
            ("STANDARD", "IEC 60076 · tested"), ("INSULATION", "calm under load"),
            ("SERIAL NO.", "KRS-2004"), ("MFD.", CITY)]
    for i, (k, v) in enumerate(rows):
        col, row = i % 2, i // 2
        x, y = 112 + col * 350, 282 + row * 56
        p.add(f'<rect x="{x - 8}" y="{y - 24}" width="330" height="44" rx="4" fill="none" stroke="{t["ink"]}" stroke-opacity=".35"/>')
        p.engrave(x, y - 6, k, 11, 700, spacing=2)
        p.engrave(x, y + 13, v, 17, 700, spacing=.5)
    # status column
    p.steel(870, 62, 270, 476, 10)
    p.engrave(1005, 104, "STATUS", 16, anchor="middle", spacing=4)
    for i, (lab, col, bl) in enumerate([("POWER", "#39FF6A", None), ("SHIPPING", "#39FF6A", "blink"),
                                         ("COFFEE", "#FFB020", "blink2"), ("FAULTS", "#3A3F46", None)]):
        y = 156 + i * 64
        p.led(916, y, col, 9, bl)
        p.engrave(942, y + 6, lab, 18, spacing=2)
    p.add(f'<rect x="896" y="410" width="218" height="104" rx="8" fill="url(#stripes)" filter="url(#lift)"/>'
          f'<rect x="908" y="422" width="194" height="80" rx="4" fill="#FFC400"/>'
          f'<path d="M935 486 L955 446 L975 486 Z" fill="none" stroke="#151515" stroke-width="4" stroke-linejoin="round"/>'
          f'<text x="955" y="481" text-anchor="middle" font-family="{BOLD}" font-size="18" fill="#151515">!</text>'
          f'<text x="1040" y="458" text-anchor="middle" font-family="{BOLD}" font-size="15" fill="#151515">DANGER</text>'
          f'<text x="1040" y="480" text-anchor="middle" font-family="{BOLD}" font-size="12" fill="#151515">HIGH OUTPUT</text>')
    p.save(f"hero-{theme}.svg", f"Rating plate: {NAME}, electrical engineer and software builder. Rated output 10 builds shipped; vector group Ohm's Law to Git; cooling ONAN, chai-assisted; ships daily; IEC 60076 tested; made in {CITY}.")

    # ── meters ──
    p = Panel(t, 1200, 390)
    p.steel(20, 20, 1160, 350, 18)
    p.screws(20, 20, 1160, 350)
    for i, (v, mx, lab, unit, fmt) in enumerate([(9, 12, "APPS IN PRODUCTION", "APPS", "{:.0f}"), (128, 150, "TESTS GUARDING DISPATCH", "TESTS", "{:.0f}"),
                                                  (98, 100, "MANUAL TIME DELETED", "%", "{:.0f}%"), (8.38, 10, "CGPA", "/ 10", "{:.2f}")]):
        gauge(p, 165 + i * 290, 180, 104, v, mx, lab, unit, fmt=fmt)
    p.save(f"meters-{theme}.svg", f"Meters: 9 apps in production, 128 tests guarding dispatch, 98% of manual time deleted, CGPA {CGPA} of 10.", GAUGE_CSS)

    # ── project breaker modules ──
    for slug, name, status, url, hook, impact, stack in PROJECTS:
        p = Panel(t, 600, 300)
        p.steel(14, 14, 572, 272, 14)
        p.screws(14, 14, 572, 272, 18)
        led = LED[status]
        p.led(60, 66, led, 9, "blink" if status in ("PRODUCTION", "LIVE") else None)
        p.engrave(82, 72, status, 15, spacing=2.5)
        # toggle switch, thrown ON
        p.add(f'<rect x="488" y="44" width="56" height="86" rx="10" fill="#2B2F35" filter="url(#lift)"/>'
              f'<rect x="496" y="52" width="40" height="70" rx="7" fill="#15171A"/>'
              f'<g class="flip" style="transform-origin:516px 87px"><rect x="507" y="40" width="18" height="50" rx="9" fill="url(#chrome)"/></g>'
              f'<text x="516" y="146" text-anchor="middle" font-family="{DIN}" font-size="12" font-weight="700" fill="{t["ink"]}">ON</text>')
        p.engrave(44, 128, name.upper(), 26, 800, spacing=1.5)
        p.dymo(44, 152, hook, "#151515", 13)
        p.dymo(44, 198, impact, "#C1121F", 13)
        p.engrave(44, 266, stack, 15, 600, font=DIN, spacing=1)
        if url:
            p.engrave(556, 266, "OPEN ↗", 13, anchor="end", spacing=2)
        p.save(f"card-{slug}-{theme}.svg", f"{name} ({status}): {hook} {impact}. Built with {stack}.",
               ".flip{animation:flip 6s ease-in-out infinite}@keyframes flip{0%,88%,100%{transform:none}92%{transform:scaleY(-1)}96%{transform:none}}")

    # ── logbook clipboard ──
    p = Panel(t, 1200, 720)
    p.add(f'<rect x="150" y="30" width="900" height="670" rx="26" fill="#8B5A2B" filter="url(#lift)"/>'
          f'<rect x="150" y="30" width="900" height="670" rx="26" fill="#fff" opacity=".06" filter="url(#brush)"/>'
          f'<rect x="190" y="80" width="820" height="596" fill="{t["paper"]}" filter="url(#lift)"/>')
    for i in range(16):
        p.add(f'<line x1="190" x2="1010" y1="{150 + i * 33}" y2="{150 + i * 33}" stroke="#7FB2E5" stroke-opacity=".45"/>')
    p.add('<line x1="262" x2="262" y1="80" y2="676" stroke="#E5383B" stroke-opacity=".55" stroke-width="1.5"/>'
          '<rect x="480" y="16" width="240" height="78" rx="14" fill="url(#chrome)" filter="url(#lift)"/>'
          '<rect x="540" y="34" width="120" height="22" rx="11" fill="#5D646D"/>')
    p.add(f'<text x="290" y="128" font-family="{TYPE}" font-size="26" font-weight="700" fill="#1B1B1B" letter-spacing="3">SHIFT LOG · CAREER</text>')
    y = 180
    for org, role, when, where, what, win in EXPERIENCE:
        p.add(f'<text x="276" y="{y}" font-family="{TYPE}" font-size="19" font-weight="700" fill="#1B1B1B">{esc(org.upper())}</text>'
              f'<text x="990" y="{y}" text-anchor="end" font-family="{TYPE}" font-size="16" fill="#3A3A3A">{esc(when)} · {esc(where)}</text>'
              f'<text x="276" y="{y + 24}" font-family="{TYPE}" font-size="16" fill="#1F4E99">{esc(role)}</text>'
              f'<text x="276" y="{y + 48}" font-family="{TYPE}" font-size="15" fill="#333">{esc(what)}</text>'
              f'<text x="276" y="{y + 72}" font-family="{TYPE}" font-size="15" font-weight="700" fill="#0B6E4F">✔ {esc(win)}</text>')
        y += 99
    p.add(f'<g transform="rotate(-10 880 112)" opacity=".85"><rect x="790" y="82" width="190" height="56" rx="8" fill="none" stroke="#C1121F" stroke-width="5"/>'
          f'<text x="885" y="121" text-anchor="middle" font-family="{BOLD}" font-size="24" fill="#C1121F" letter-spacing="2">APPROVED</text></g>')
    p.save(f"logbook-{theme}.svg", "Shift log: " + "; ".join(f"{o}, {r}, {w}: {x}" for o, r, w, _, x, _ in EXPERIENCE))

    # ── wins as hanging inspection tags + cert stickers ──
    p = Panel(t, 1200, 470)
    p.steel(20, 20, 1160, 430, 18)
    p.screws(20, 20, 1160, 430)
    p.engrave(600, 74, "INSPECTION TAGS  ·  PASSED", 20, anchor="middle", spacing=4)
    p.add(f'<line x1="60" x2="1140" y1="110" y2="110" stroke="url(#chrome)" stroke-width="8" stroke-linecap="round"/>')
    for i, (when, title, where) in enumerate(WINS):
        x = 80 + i * 270
        rot = [-3, 2, -2, 3][i]
        words, lines, line = where.split(), [], ""
        for wd in words:
            if len(line + wd) > 24:
                lines.append(line.strip()); line = ""
            line += wd + " "
        lines.append(line.strip())
        p.add(f'<g class="sway" style="transform-origin:{x + 115}px 110px;animation-delay:-{i * .7:.1f}s"><g transform="rotate({rot} {x + 115} 110)">'
              f'<line x1="{x + 115}" y1="110" x2="{x + 115}" y2="150" stroke="#C9B37E" stroke-width="2"/>'
              f'<path d="M{x + 30},150 h170 l30,30 v190 h-230 v-190 z" fill="#E8D6A8" filter="url(#lift)"/>'
              f'<circle cx="{x + 115}" cy="170" r="9" fill="{t["steel"][1]}" stroke="#B89B5E" stroke-width="3"/>'
              f'<text x="{x + 115}" y="214" text-anchor="middle" font-family="{TYPE}" font-size="15" fill="#6B4E16">{esc(when)}</text>'
              f'<text x="{x + 115}" y="250" text-anchor="middle" font-family="{BOLD}" font-size="19" fill="#2A2112">{esc(title.upper())}</text>'
              + "".join(f'<text x="{x + 115}" y="{280 + j * 20}" text-anchor="middle" font-family="{TYPE}" font-size="13" fill="#4A3A1A">{esc(l)}</text>' for j, l in enumerate(lines[:3]))
              + f'<text x="{x + 115}" y="352" text-anchor="middle" font-family="{BOLD}" font-size="13" fill="#0B6E4F" letter-spacing="2">✔ PASSED</text></g></g>')
    p.save(f"tags-{theme}.svg", "Inspection tags: " + "; ".join(f"{w} {a}, {b}" for w, a, b in WINS),
           ".sway{animation:sway 4s ease-in-out infinite}@keyframes sway{50%{transform:rotate(2.5deg)}}")

    # ── skills on DIN-rail terminal blocks ──
    COLORS = {"Power": "#7A8591", "Code": "#2F6FD1", "Things": "#E07A1F", "AI": "#2BA84A"}
    p = Panel(t, 1200, 520)
    p.steel(20, 20, 1160, 480, 18)
    p.screws(20, 20, 1160, 480)
    y = 70
    for group, items in SKILLS.items():
        p.engrave(56, y + 48, group.upper(), 18, spacing=3)
        p.add(f'<rect x="170" y="{y + 22}" width="980" height="36" fill="url(#chrome)"/>'
              + "".join(f'<rect x="{180 + k * 40}" y="{y + 36}" width="22" height="8" rx="4" fill="#6B727B"/>' for k in range(24)))
        x = 178
        for it in items:
            w = max(len(it) * 7.6 + 18, 58)
            p.add(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="80" rx="4" fill="{COLORS[group]}" filter="url(#lift)"/>'
                  f'<rect x="{x}" y="{y}" width="{w:.0f}" height="80" rx="4" fill="#fff" opacity=".12" filter="url(#brush)"/>'
                  f'<circle cx="{x + w / 2:.0f}" cy="{y + 16}" r="7" fill="url(#screw)"/>'
                  f'<rect x="{x + 5}" y="{y + 30}" width="{w - 10:.0f}" height="22" rx="2" fill="#F7F7F2"/>'
                  f'<text x="{x + w / 2:.0f}" y="{y + 46}" text-anchor="middle" font-family="{DIN}" font-size="13" font-weight="700" fill="#151515">{esc(it)}</text>'
                  f'<circle cx="{x + w / 2:.0f}" cy="{y + 66}" r="7" fill="url(#screw)"/>')
            x += w + 4
        y += 108
    p.save(f"terminals-{theme}.svg", "Skills wired in: " + "; ".join(f"{g}: {', '.join(v)}" for g, v in SKILLS.items()))

    # ── footer: emergency stop that hires ──
    p = Panel(t, 1200, 400)
    p.add('<rect x="20" y="20" width="1160" height="360" rx="18" fill="url(#stripes)" filter="url(#lift)"/>')
    p.steel(60, 56, 1080, 288, 14)
    p.screws(60, 56, 1080, 288)
    p.add(f'<circle cx="300" cy="200" r="118" fill="#FFC400" filter="url(#lift)"/>'
          f'<circle cx="300" cy="200" r="104" fill="#E9B200"/>'
          f'<text font-family="{BOLD}" font-size="13" fill="#151515" letter-spacing="3"><textPath href="#ring" startOffset="50%" text-anchor="middle">PRESS TO HIRE  ·  PRESS TO HIRE  ·  PRESS TO HIRE</textPath></text>'
          f'<path id="ring" d="M300,200 m-92,0 a92,92 0 1,1 184,0 a92,92 0 1,1 -184,0" fill="none"/>'
          f'<g class="push" style="transform-origin:300px 200px"><circle cx="300" cy="208" r="74" fill="#7A0A12"/>'
          f'<circle cx="300" cy="200" r="74" fill="#D62828"/><circle cx="300" cy="200" r="74" fill="url(#chrome)" opacity=".18"/>'
          f'<ellipse cx="280" cy="172" rx="40" ry="20" fill="#fff" opacity=".35"/></g>')
    p.engrave(470, 170, "IN CASE OF BORING PROCESS:", 22, spacing=2)
    p.engrave(470, 226, "BREAK GLASS. CALL KRISHNA.", 40, 800, spacing=1)
    p.dymo(470, 254, EMAIL, "#151515", 17)
    p.save(f"estop-{theme}.svg", f"In case of boring process: break glass, call Krishna. {EMAIL}",
           ".push{animation:push 3s ease-in-out infinite}@keyframes push{0%,80%,100%{transform:none}86%{transform:scale(.94)}}")
print("ok")
