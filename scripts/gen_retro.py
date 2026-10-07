"""Retro-futurist (80s synthwave arcade) SVGs for the profile README: sunrise (light) and midnight (dark).

Run:  python scripts/gen_retro.py   (facts in scripts/profile_data.py, pixel portrait from scripts/pixels.py)
"""
import os, sys
from xml.sax.saxutils import escape as esc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from profile_data import NAME, EMAIL, CITY, CGPA, LANGUAGES, EXPERIENCE, PROJECTS, WINS, CERTS

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "retro")
CHROME = "'Arial Black', 'Helvetica Neue', Impact, Arial, sans-serif"
SCRIPT = "'Brush Script MT', 'Segoe Script', 'Lucida Handwriting', cursive"
PIXEL = "'Press Start 2P', 'Courier New', Courier, monospace"
THEMES = {
    "dark": dict(sky=["#07011A", "#1B0549", "#5B0F8A", "#F72585"], floor="#090018", grid="#F72585", neon="#4CC9F0", pink="#FF4FD8",
                 sun=["#FFE45E", "#FF7B54", "#F72585"], text="#F8F0FF", soft="#B9A6E0", hill="#12043A", panel="#120531", glow=1,
                 chrome=["#E9F6FF", "#7EC8FF", "#2A1B5C", "#FFB2E6", "#FFFFFF"], pix=["#1B0549", "#3A0CA3", "#7209B7", "#B5179E", "#F72585", "#FF6FB5", "#FF9E7A", "#FFC46B", "#FFE45E", "#FFF6C2"]),
    "light": dict(sky=["#FFF1E6", "#FFD6E8", "#FFB5C8", "#FF9A8B"], floor="#FDF0FF", grid="#C77DFF", neon="#3A86FF", pink="#E0218A",
                  sun=["#FFD166", "#FF8FAB", "#F15BB5"], text="#2E1A47", soft="#6B4E8F", hill="#E9C8FF", panel="#FFF7FB", glow=0,
                  chrome=["#2E1A47", "#5A3E9B", "#F7F0FF", "#C77DFF", "#2E1A47"], pix=["#3A0CA3", "#4E1DB3", "#6A2EC2", "#8A3FD1", "#B14FD8", "#D65DB1", "#F77F93", "#FF9E7A", "#FFC46B", "#FFE8A8"]),
}
REDUCE = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def defs(t):
    sky = "".join(f'<stop offset="{i / 3:.2f}" stop-color="{c}"/>' for i, c in enumerate(t["sky"]))
    sun = "".join(f'<stop offset="{i / 2:.2f}" stop-color="{c}"/>' for i, c in enumerate(t["sun"]))
    ch = t["chrome"]
    return f"""<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{sky}</linearGradient>
<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">{sun}</linearGradient>
<linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ch[0]}"/><stop offset=".48" stop-color="{ch[1]}"/>
  <stop offset=".5" stop-color="{ch[2]}"/><stop offset=".75" stop-color="{ch[3]}"/><stop offset="1" stop-color="{ch[4]}"/></linearGradient>
<filter id="neon" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="{4 if t['glow'] else 1.5}" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity="{.18 if t['glow'] else .05}"/></pattern>"""


def svg(t, w, h, body, title, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">'
            f'<title>{esc(title)}</title><defs>{defs(t)}<clipPath id="frame"><rect width="{w}" height="{h}" rx="20"/></clipPath></defs>'
            f'<style>.blink{{animation:bl 1s steps(1) infinite}}@keyframes bl{{50%{{opacity:0}}}}{style}{REDUCE}</style>'
            f'<g clip-path="url(#frame)">{body}<rect width="{w}" height="{h}" fill="url(#scan)"/></g></svg>\n')


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


def txt(x, y, s, size, fill, font=PIXEL, anchor="start", weight=700, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{esc(s)}</text>')


def backdrop(t, w, h, horizon):
    """Sky, striped sun, pylons with sagging power lines, and a perspective grid that rolls toward you."""
    cx = w / 2
    out = [f'<rect width="{w}" height="{horizon}" fill="url(#sky)"/>',
           f'<circle cx="{cx}" cy="{horizon - 10}" r="{h * .3:.0f}" fill="{t["sun"][1]}" opacity=".45" filter="url(#soft)"/>',
           f'<mask id="cuts"><rect width="{w}" height="{h}" fill="#fff"/>'
           + "".join(f'<rect class="cut" style="animation-delay:-{i * .6:.1f}s" x="0" y="{horizon - 70 + i * 16}" width="{w}" height="{3 + i * 1.6:.1f}" fill="#000"/>' for i, _ in enumerate(range(5)))
           + "</mask>",
           f'<circle cx="{cx}" cy="{horizon - 4}" r="{h * .24:.0f}" fill="url(#sun)" mask="url(#cuts)"/>']
    # mountains
    pts = " ".join(f"{x},{horizon - (abs((x * 37) % 90 - 45) + 10) * (1.6 if (x // 120) % 2 else .9):.0f}" for x in range(0, w + 60, 60))
    out.append(f'<polygon points="0,{horizon} {pts} {w},{horizon}" fill="{t["hill"]}" opacity=".9"/>')
    # pylons + power lines
    tops = []
    for k, px in enumerate([70, 300, w - 300, w - 70]):
        s = .9 if k in (0, 3) else .6
        hgt = 150 * s
        top = horizon - hgt
        tops.append((px, top + 18 * s))
        out.append(f'<g stroke="{t["neon"]}" stroke-width="2" fill="none" opacity=".85" filter="url(#neon)">'
                   f'<path d="M{px - 26 * s},{horizon} L{px - 6 * s},{top} L{px + 6 * s},{top} L{px + 26 * s},{horizon} '
                   f'M{px - 20 * s},{horizon - hgt * .3} L{px + 20 * s},{horizon - hgt * .3} M{px - 13 * s},{horizon - hgt * .6} L{px + 13 * s},{horizon - hgt * .6} '
                   f'M{px - 34 * s},{top + 18 * s} L{px + 34 * s},{top + 18 * s} M{px - 22 * s},{horizon} L{px + 13 * s},{horizon - hgt * .6} M{px + 22 * s},{horizon} L{px - 13 * s},{horizon - hgt * .6}"/></g>')
    for (x1, y1), (x2, y2) in zip(tops, tops[1:]):
        if abs(x2 - x1) > w / 2:
            continue
        out.append(f'<path d="M{x1},{y1} Q{(x1 + x2) / 2},{max(y1, y2) + 26} {x2},{y2}" stroke="{t["neon"]}" stroke-width="1.5" fill="none" opacity=".7"/>')
    # floor grid
    out.append(f'<rect y="{horizon}" width="{w}" height="{h - horizon}" fill="{t["floor"]}"/>')
    g = [f'<line x1="{cx}" y1="{horizon}" x2="{cx + k * 140}" y2="{h}" />' for k in range(-12, 13)]
    ys = [horizon + (h - horizon) * (i / 9) ** 2.2 for i in range(10)]
    for i in range(9):
        g.append(f'<line class="row r{i}" x1="0" x2="{w}" y1="{ys[i]:.1f}" y2="{ys[i]:.1f}" style="--d:{ys[i + 1] - ys[i]:.1f}px"/>')
    out.append(f'<g stroke="{t["grid"]}" stroke-width="2" filter="url(#neon)" opacity=".85">{"".join(g)}</g>')
    out.append(f'<line x1="0" x2="{w}" y1="{horizon}" y2="{horizon}" stroke="{t["pink"]}" stroke-width="3" filter="url(#neon)"/>')
    return "".join(out)


BACK_CSS = (".row{animation:row 1.6s cubic-bezier(.55,0,1,.45) infinite}@keyframes row{to{transform:translateY(var(--d))}}"
            ".cut{animation:cut 3s linear infinite}@keyframes cut{from{transform:translateY(0)}to{transform:translateY(16px)}}")


def truck(t, x, y, s=1):
    """Neon flatbed carrying a power transformer: the dispatch system, on the road."""
    c = t["neon"]
    fins = "".join(f'<line x1="{x + 70 + i * 9}" y1="{y - 50}" x2="{x + 70 + i * 9}" y2="{y - 14}"/>' for i in range(6))
    return (f'<g transform="scale({s})" stroke-linejoin="round"><g fill="none" stroke="{c}" stroke-width="3" filter="url(#neon)">'
            f'<rect x="{x}" y="{y - 12}" width="190" height="12"/>'
            f'<path d="M{x + 190},{y} V{y - 42} H{x + 222} L{x + 244},{y - 22} V{y} Z"/><path d="M{x + 196},{y - 36} H{x + 220} L{x + 234},{y - 22} H{x + 196} Z"/>'
            f'<rect x="{x + 20}" y="{y - 64}" width="44" height="52"/>{fins}'
            f'<path d="M{x + 30},{y - 64} V{y - 82} M{x + 44},{y - 64} V{y - 86} M{x + 58},{y - 64} V{y - 82}"/>'
            f'<circle cx="{x + 34}" cy="{y + 6}" r="11"/><circle cx="{x + 150}" cy="{y + 6}" r="11"/><circle cx="{x + 222}" cy="{y + 6}" r="11"/></g>'
            f'<text x="{x + 120}" y="{y - 22}" font-family="{PIXEL}" font-size="10" fill="{t["pink"]}" text-anchor="middle">ITTL</text></g>')


pix = open(os.path.join(OUT, "pixels.txt"), encoding="utf-8").read().split("\n")

for theme, t in THEMES.items():
    W, H, HZ = 1200, 660, 400
    # ── hero ──
    body = backdrop(t, W, H, HZ)
    body += f'<g class="drive">{truck(t, -260, HZ + 70)}</g>'
    body += (f'<text x="600" y="190" text-anchor="middle" font-family="{CHROME}" font-size="104" font-style="italic" font-weight="900" '
             f'fill="url(#chrome)" stroke="{t["text"] if t["glow"] else "#FFFFFF"}" stroke-width="2" letter-spacing="-2">{esc(NAME.upper().replace(" S", ""))}</text>'
             f'<text x="770" y="262" text-anchor="middle" font-family="{SCRIPT}" font-size="76" fill="{t["pink"]}" filter="url(#neon)" '
             f'transform="rotate(-6 770 262)">Engineer</text>'
             + f'<rect x="290" y="306" width="620" height="36" rx="18" fill="{t["floor"]}" opacity=".78"/>'
             + txt(600, 331, "ELECTRICAL BY DEGREE  ★  SOFTWARE BY CHOICE", 20, t["text"], anchor="middle", extra='letter-spacing="3"')
             + txt(40, 46, "▶ PLAY", 18, t["text"]) + txt(1160, 46, "SP 00:20:26", 18, t["text"], anchor="end")
             + f'<g class="blink">{txt(600, 640, "PRESS START", 18, t["text"], anchor="middle", extra="letter-spacing=\"4\"")}</g>')
    save(f"hero-{theme}.svg", svg(t, W, H, body, f"{NAME}: electrical by degree, software by choice. A neon truck carries a transformer past power pylons.",
                                  BACK_CSS + ".drive{animation:drive 9s linear infinite}@keyframes drive{to{transform:translateX(1560px)}}"))

    # ── player card ──
    body = f'<rect width="1200" height="520" fill="{t["panel"]}"/><rect width="1200" height="520" fill="url(#sky)" opacity=".18"/>'
    body += txt(600, 58, "PLAYER 1  ·  CHARACTER SELECT", 24, t["pink"], anchor="middle", extra='letter-spacing="3" filter="url(#neon)"')
    px0, py0, cs = 70, 96, 11
    cells = "".join(f'<rect x="{px0 + x * cs}" y="{py0 + y * cs}" width="{cs}" height="{cs}" fill="{t["pix"][int(c)]}"/>'
                    for y, row in enumerate(pix) for x, c in enumerate(row) if c != ".")
    body += (f'<rect x="{px0 - 14}" y="{py0 - 14}" width="{34 * cs + 28}" height="{34 * cs + 28}" fill="none" stroke="{t["neon"]}" stroke-width="4" filter="url(#neon)"/>'
             f'<g class="bob">{cells}</g>')
    body += txt(px0 + 17 * cs, py0 + 34 * cs + 52, "KRS-2004", 16, t["text"], anchor="middle", extra='letter-spacing="3"')
    rx = 520
    info = [("CLASS", "Engineer-Mage"), ("LEVEL", "22"), ("HOME", CITY), ("GUILD", "Indo Tech · Digitalisation")]
    for i, (k, v) in enumerate(info):
        body += txt(rx, 118 + i * 34, k, 14, t["soft"]) + txt(rx + 120, 118 + i * 34, v, 16, t["text"])
    bars = [("VOLTAGE", .92, "#FFE45E"), ("CODE", .9, t["neon"]), ("AUTOMATION", .99, t["pink"]), ("HARDWARE", .82, "#7CFFB2"), ("CHAI", 1.0, "#FF9E7A")]
    for i, (k, v, c) in enumerate(bars):
        y = 270 + i * 34
        body += (txt(rx, y + 12, k, 14, t["soft"]) + f'<rect x="{rx + 170}" y="{y - 4}" width="440" height="18" fill="none" stroke="{t["text"]}" stroke-opacity=".5"/>'
                 + f'<rect class="fill" style="animation-delay:{.2 + i * .15:.2f}s" x="{rx + 172}" y="{y - 2}" width="{436 * v:.0f}" height="14" fill="{c}"/>'
                 + "".join(f'<line x1="{rx + 172 + j * 22}" x2="{rx + 172 + j * 22}" y1="{y - 2}" y2="{y + 12}" stroke="{t["panel"]}" stroke-width="3"/>' for j in range(1, 20)))
    body += txt(rx, 462, "SPECIAL MOVES:", 14, t["soft"]) + txt(rx + 190, 462, "30-MIN→30-SEC  ·  IEC 60076 COMBO  ·  PATENT STRIKE", 13, t["pink"])
    body += txt(rx, 494, "LANGUAGE PACKS:", 14, t["soft"]) + txt(rx + 190, 494, "  ".join(l.upper() for l in LANGUAGES), 13, t["text"])
    save(f"player-{theme}.svg", svg(t, 1200, 520, body,
         f"Player 1: pixel portrait of {NAME}. Class Engineer-Mage, level 22, home {CITY}, guild Indo Tech Digitalisation. "
         "Self-reported stats: voltage, code, automation, hardware, chai. Special moves: 30 minutes to 30 seconds, IEC 60076 combo, patent strike. Speaks " + ", ".join(LANGUAGES),
         ".bob{animation:bob 1.2s steps(2) infinite}@keyframes bob{50%{transform:translateY(-4px)}}"
         ".fill{animation:fill 1.2s steps(12) backwards}@keyframes fill{from{width:0}}"))

    # ── career stages ──
    body = f'<rect width="1200" height="430" fill="{t["panel"]}"/><rect width="1200" height="430" fill="url(#sky)" opacity=".18"/>'
    body += txt(600, 56, "CAREER MODE  ·  STAGE SELECT", 24, t["pink"], anchor="middle", extra='letter-spacing="3" filter="url(#neon)"')
    stages = list(reversed(EXPERIENCE))
    bosses = ["Paper-only docs", "Megawatt maze", "Blank repo", "30-min paperwork", "Spreadsheet empire"]
    for i, (org, role, when, where, what, win) in enumerate(stages):
        x = 40 + i * 228
        now = i == len(stages) - 1
        col = t["pink"] if now else t["neon"]
        body += (f'<rect x="{x}" y="96" width="210" height="300" rx="6" fill="{t["floor"]}" stroke="{col}" stroke-width="3" filter="url(#neon)"/>'
                 + txt(x + 105, 134, f"STAGE {i + 1}", 16, col, anchor="middle")
                 + txt(x + 105, 160, when.upper(), 11, t["soft"], anchor="middle"))
        words, lines, line = org.upper().split(), [], ""
        for wd in words:
            if len(line + wd) > 13:
                lines.append(line.strip()); line = ""
            line += wd + " "
        lines.append(line.strip())
        for j, l in enumerate(lines[:3]):
            body += txt(x + 105, 204 + j * 24, l, 15, t["text"], anchor="middle")
        body += txt(x + 105, 296, "BOSS:", 11, t["soft"], anchor="middle") + txt(x + 105, 318, bosses[i].upper(), 10, t["text"], anchor="middle")
        if now:
            body += f'<g class="blink">{txt(x + 105, 368, "▶ NOW PLAYING", 13, t["pink"], anchor="middle")}</g>'
        else:
            body += txt(x + 105, 368, "CLEAR ✓", 13, "#7CFFB2" if t["glow"] else "#13A35A", anchor="middle")
    save(f"stages-{theme}.svg", svg(t, 1200, 430, body, "Career mode: " + "; ".join(f"stage {i + 1}: {o}, {w}, boss {b}" for i, ((o, _, w, _, _, _), b) in enumerate(zip(stages, bosses)))))

    # ── cartridges ──
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        c1, c2 = [(t["neon"], t["pink"]), ("#FFE45E", t["pink"]), ("#7CFFB2", t["neon"]), (t["pink"], "#FFE45E")][i % 4]
        plastic = "#3B3552" if t["glow"] else "#D9D3E6"
        edge = "#1E1A2E" if t["glow"] else "#A79FBC"
        body = (f'<rect width="600" height="340" fill="{t["panel"]}"/>'
                f'<path d="M60,30 H540 a16,16 0 0 1 16,16 V300 H44 V46 a16,16 0 0 1 16,-16 Z" fill="{plastic}" stroke="{edge}" stroke-width="3"/>'
                + "".join(f'<rect x="{80 + k * 20}" y="304" width="12" height="18" fill="{edge}"/>' for k in range(23))
                + f'<rect x="76" y="50" width="448" height="210" rx="8" fill="{t["floor"]}"/>'
                f'<linearGradient id="lab" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}" stop-opacity=".35"/><stop offset="1" stop-color="{c2}" stop-opacity=".35"/></linearGradient>'
                f'<rect x="76" y="50" width="448" height="210" rx="8" fill="url(#lab)"/>'
                + txt(96, 84, f"No.{i + 1:02d}", 12, t["soft"]) + txt(504, 84, status, 12, c2, anchor="end")
                + f'<text x="96" y="136" font-family="{CHROME}" font-size="{30 if len(name) < 18 else 24}" font-style="italic" font-weight="900" fill="url(#chrome)" stroke="{edge}" stroke-width="1">{esc(name.upper())}</text>'
                + txt(96, 178, hook, 12, t["text"]) + txt(96, 204, impact, 12, c1 if t["glow"] else t["pink"])
                + txt(96, 242, stack.upper(), 11, t["soft"])
                + f'<rect x="76" y="270" width="448" height="22" rx="4" fill="{edge}"/>'
                + txt(300, 286, "▶ INSERT & PLAY" if url else "◆ COLLECTOR'S EDITION", 11, "#FFFFFF", anchor="middle"))
        save(f"card-{slug}-{theme}.svg", svg(t, 600, 340, body, f"Cartridge No.{i + 1:02d}: {name} ({status}). {hook} {impact}."))

    # ── high scores ──
    body = f'<rect width="1200" height="440" fill="{t["floor"]}"/><rect width="1200" height="440" fill="url(#sky)" opacity=".12"/>'
    body += txt(600, 70, "HIGH SCORES", 40, t["pink"], anchor="middle", extra='letter-spacing="6" filter="url(#neon)"')
    body += txt(150, 120, "RANK", 14, t["soft"]) + txt(330, 120, "SCORE", 14, t["soft"]) + txt(640, 120, "STAGE", 14, t["soft"]) + txt(1060, 120, "NAME", 14, t["soft"], anchor="end")
    scores = [("1ST", "#7 / 1500+", "NEC · IIT BOMBAY"), ("2ND", "RUNNER-UP", "FISH TANK · E-SUMMIT"), ("3RD", "PATENT FILED", "STREET LIGHTS · 2025"),
              ("4TH", "FINALIST", "TECH SYMPOSIUM · 2024"), ("5TH", f"CGPA {CGPA}", "ST. JOSEPH'S · 2026")]
    cols = ["#FFE45E", t["neon"], t["pink"], "#7CFFB2", t["text"]] if t["glow"] else ["#C9184A", "#3A86FF", "#E0218A", "#13A35A", t["text"]]
    for i, (r, s, st) in enumerate(scores):
        y = 166 + i * 42
        cls = ' class="blink"' if i == 0 else ""
        body += (f'<g{cls}>' + txt(150, y, r, 20, cols[i]) + txt(330, y, s, 20, cols[i]) + txt(640, y, st, 16, cols[i]) + txt(1060, y, "KRS", 20, cols[i], anchor="end") + "</g>")
    body += txt(600, 402, "POWER-UPS: " + "  ·  ".join(c.split(" · ")[0].upper() for c in CERTS), 11, t["soft"], anchor="middle")
    save(f"scores-{theme}.svg", svg(t, 1200, 440, body, "High scores: " + "; ".join(f"{r} {s}, {st}" for r, s, st in scores) + ". Power-ups: " + ", ".join(CERTS)))

    # ── footer ──
    body = backdrop(t, 1200, 360, 200)
    body += (f'<rect x="300" y="40" width="600" height="250" rx="12" fill="{t["floor"]}" opacity=".82" stroke="{t["pink"]}" stroke-width="3" filter="url(#neon)"/>'
             + f'<g class="blink">{txt(600, 112, "INSERT COIN TO HIRE", 30, t["pink"], anchor="middle", extra="letter-spacing=\"3\"")}</g>'
             + txt(600, 160, "1 COIN = 1 BORING PROCESS, DELETED", 15, t["text"], anchor="middle")
             + txt(600, 206, EMAIL, 18, t["neon"] if t["glow"] else t["text"], anchor="middle")
             + txt(600, 256, "GAME OVER?  NEVER.  CONTINUE ▶ 9", 14, t["soft"], anchor="middle"))
    save(f"coin-{theme}.svg", svg(t, 1200, 360, body, f"Insert coin to hire. One coin equals one boring process, deleted. {EMAIL}", BACK_CSS))
print("ok")
