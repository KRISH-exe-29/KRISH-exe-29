"""Bento-grid profile: one keynote-style board of modular tiles, each a tiny live widget.
Run: python scripts/gen_bento.py [photo]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, icon, pic, write_readme, photo_grid, SANS, MONO
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, EXPERIENCE, LANGUAGES, short

F = "bento"
THEMES = {"light": dict(bg="#F5F5F7", tile="#FFFFFF", ink="#1D1D1F", soft="#6E6E73", line="#E5E5EA", blue="#0071E3", green="#28CD41", orange="#FF9F0A", pink="#FF375F", purple="#BF5AF2"),
          "dark": dict(bg="#000000", tile="#1C1C1E", ink="#F5F5F7", soft="#98989D", line="#2C2C2E", blue="#0A84FF", green="#30D158", orange="#FF9F0A", pink="#FF375F", purple="#BF5AF2")}
U, G, M = 270, 20, 25  # tile unit, gap, margin
photo = photo_grid(F, 44, sys.argv[1] if len(sys.argv) > 1 else None)


def tile(c, t, col, row, w=1, h=1, fill=None):
    x, y = M + col * (U + G), M + row * (U + G)
    W, H = w * U + (w - 1) * G, h * U + (h - 1) * G
    c.add(f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="28" fill="{fill or t["tile"]}"/>')
    return x, y, W, H


for th, t in THEMES.items():
    c = Canvas(F, t, 1200, 1475)
    c.add(f'<rect width="1200" height="1475" fill="{t["bg"]}"/>')
    # portrait 2x2
    x, y, W, H = tile(c, t, 0, 0, 2, 2)
    cell = 9.6
    ox, oy = x + (W - 44 * cell) / 2, y + 40
    dots = []
    for r, row in enumerate(photo):
        for q, ch in enumerate(row):
            if ch == ".":
                continue
            d = int(ch)
            op = (9 - d) / 9 if th == "light" else d / 9
            if op > .08:
                dots.append(f'<rect x="{ox + q * cell:.1f}" y="{oy + r * cell:.1f}" width="{cell - 1.6:.1f}" height="{cell - 1.6:.1f}" rx="2" opacity="{op:.2f}"/>')
    c.add(f'<g fill="{t["ink"]}">{"".join(dots)}</g>')
    c.add(f'<g fill="{t["tile"]}" opacity=".94"><rect x="{x}" y="{y + H - 120}" width="{W}" height="120" rx="28"/>'
          f'<rect x="{x}" y="{y + H - 120}" width="{W}" height="60"/></g>')
    c.text(x + 32, y + H - 66, NAME, 36, t["ink"], SANS, 700, extra='letter-spacing="-1"')
    c.text(x + 32, y + H - 32, "Electrical engineer who ships software.", 18, t["soft"], SANS)
    # 9 apps live
    x, y, W, H = tile(c, t, 2, 0)
    c.add(f'<circle class="pulse" cx="{x + 40}" cy="{y + 42}" r="8" fill="{t["green"]}"/>')
    c.text(x + 58, y + 48, "Live now", 16, t["green"], SANS, 600)
    c.text(x + 30, y + 190, "9", 130, t["ink"], SANS, 700, extra='letter-spacing="-6"')
    c.text(x + 30, y + 236, "apps in production", 18, t["soft"], SANS, 500)
    # now shipping with equaliser
    x, y, W, H = tile(c, t, 3, 0, fill=t["blue"])
    c.text(x + 28, y + 46, "NOW SHIPPING", 13, "#FFFFFF", SANS, 700, extra='letter-spacing="2" opacity=".8"')
    c.text(x + 28, y + 92, "KioskSentinel", 28, "#FFFFFF", SANS, 700)
    c.text(x + 28, y + 120, "attendance that survives", 15, "#FFFFFF", SANS, extra='opacity=".85"')
    c.text(x + 28, y + 140, "power cuts", 15, "#FFFFFF", SANS, extra='opacity=".85"')
    for i in range(9):
        c.add(f'<rect class="eq" style="animation-delay:-{i * .17:.2f}s;animation-duration:{.7 + (i % 3) * .2:.1f}s" x="{x + 28 + i * 24}" y="{y + 180}" width="14" height="60" rx="7" fill="#FFFFFF" opacity=".9"/>')
    # time saved clock
    x, y, W, H = tile(c, t, 2, 1)
    cx, cy = x + W / 2, y + 118
    c.add(f'<circle cx="{cx}" cy="{cy}" r="74" fill="none" stroke="{t["line"]}" stroke-width="10"/>'
          f'<circle cx="{cx}" cy="{cy}" r="74" fill="none" stroke="{t["orange"]}" stroke-width="10" stroke-linecap="round" stroke-dasharray="{2 * math.pi * 74 * .98:.0f} 999" transform="rotate(-90 {cx} {cy})" class="ring"/>'
          f'<line class="hand" x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 52}" stroke="{t["ink"]}" stroke-width="5" stroke-linecap="round" style="transform-origin:{cx}px {cy}px"/>'
          f'<circle cx="{cx}" cy="{cy}" r="6" fill="{t["ink"]}"/>')
    c.text(cx, y + 230, "30 min → 30 s", 22, t["ink"], SANS, 700, "middle")
    c.text(cx, y + 254, "98% of the chore, deleted", 14, t["soft"], SANS, anchor="middle")
    # patent
    x, y, W, H = tile(c, t, 3, 1)
    c.add(f'<g class="glow"><circle cx="{x + W / 2}" cy="{y + 96}" r="52" fill="{t["orange"]}" opacity=".25"/></g>'
          f'<path d="M{x + W / 2 - 24},{y + 108} a32,32 0 1 1 48,0 l-6,18 h-36z" fill="{t["orange"]}"/>'
          f'<rect x="{x + W / 2 - 16}" y="{y + 130}" width="32" height="12" rx="3" fill="{t["soft"]}"/>')
    c.text(x + W / 2, y + 196, "Patent filed", 22, t["ink"], SANS, 700, "middle")
    c.text(x + W / 2, y + 222, "street lights that", 14, t["soft"], SANS, anchor="middle")
    c.text(x + W / 2, y + 240, "follow the car", 14, t["soft"], SANS, anchor="middle")
    # projects marquee 4x1
    x, y, W, H = tile(c, t, 0, 2, 4, 1)
    c.text(x + 32, y + 50, "Shipped", 26, t["ink"], SANS, 700)
    c.text(x + W - 32, y + 50, "10 projects →", 16, t["soft"], SANS, anchor="end")
    c.add(f'<clipPath id="mq"><rect x="{x}" y="{y + 70}" width="{W}" height="190"/></clipPath><g clip-path="url(#mq)"><g class="mq">')
    for rep in range(2):
        for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
            px = x + 32 + (rep * len(PROJECTS) + i) * 236
            col = [t["blue"], t["green"], t["orange"], t["pink"], t["purple"]][i % 5]
            c.add(f'<rect x="{px}" y="{y + 84}" width="220" height="160" rx="20" fill="{t["bg"]}"/>'
                  f'<rect x="{px + 18}" y="{y + 100}" width="48" height="48" rx="12" fill="{col}"/>' + icon(slug, px + 26, y + 108, 32, "#FFFFFF", t["ink"], col))
            c.text(px + 18, y + 180, short(name), 18, t["ink"], SANS, 700)
            c.text(px + 18, y + 204, hook[:27] + ("…" if len(hook) > 27 else ""), 13, t["soft"], SANS)
            c.text(px + 18, y + 228, status.lower(), 12, col, MONO, 700)
    c.add("</g></g>")
    # journey 2x1
    x, y, W, H = tile(c, t, 0, 3, 2, 1)
    c.text(x + 32, y + 50, "The journey", 26, t["ink"], SANS, 700)
    stops = list(reversed(EXPERIENCE))
    for i, (org, role, when, where, what, win) in enumerate(stops):
        sx = x + 50 + i * 115
        if i:
            c.add(f'<line x1="{sx - 115}" x2="{sx}" y1="{y + 140}" y2="{y + 140}" stroke="{t["line"]}" stroke-width="4"/>')
        c.add(f'<circle cx="{sx}" cy="{y + 140}" r="{14 if i == 4 else 9}" fill="{t["blue"] if i == 4 else t["soft"]}"/>')
        c.text(sx, y + 106, when.split()[-1] if "now" not in when else "now", 13, t["soft"], SANS, 600, "middle")
        for j, wd in enumerate(org.split()[:2]):
            c.text(sx, y + 180 + j * 18, wd, 13, t["ink"], SANS, 600, "middle")
    c.add(f'<circle class="ping" cx="{x + 50 + 4 * 115}" cy="{y + 140}" r="14" fill="none" stroke="{t["blue"]}" stroke-width="3"/>')
    # stack cloud
    x, y, W, H = tile(c, t, 2, 3, fill=t["purple"])
    words = [("TypeScript", 22), ("Python", 26), ("React", 20), ("IEC 60076", 17), ("Java", 18), ("Supabase", 16), ("ESP8266", 15), ("LangGraph", 15)]
    for i, (wd, sz) in enumerate(words):
        c.text(x + 26 + (i % 2) * 118, y + 56 + (i // 2) * 52, wd, sz, "#FFFFFF", SANS, 700)
    # languages
    x, y, W, H = tile(c, t, 3, 3)
    c.text(x + 28, y + 50, "Speaks", 22, t["ink"], SANS, 700)
    for i, lg in enumerate(LANGUAGES):
        c.add(f'<rect x="{x + 28}" y="{y + 76 + i * 44}" width="{[200, 180, 120, 90][i]}" height="30" rx="15" fill="{[t["pink"], t["blue"], t["green"], t["orange"]][i]}" opacity=".18"/>')
        c.text(x + 44, y + 97 + i * 44, lg, 16, t["ink"], SANS, 600)
    # quote 2x1 + contact 2x1
    x, y, W, H = tile(c, t, 0, 4, 2, 1, fill=t["ink"])
    c.text(x + 32, y + 92, "“", 90, t["orange"], SANS, 700)
    c.text(x + 32, y + 140, "Fluent in both Ohm's Law", 32, t["tile"], SANS, 700)
    c.text(x + 32, y + 182, "and Git commits.”", 32, t["tile"], SANS, 700)
    c.text(x + 32, y + 228, "— me, on a good day", 15, t["soft"], SANS)
    x, y, W, H = tile(c, t, 2, 4, 2, 1, fill=t["green"])
    c.text(x + 32, y + 70, "Say hi.", 54, "#FFFFFF", SANS, 700, extra='letter-spacing="-2"')
    c.text(x + 32, y + 112, "Boring process? I want it.", 20, "#FFFFFF", SANS, 500)
    c.text(x + 32, y + 226, EMAIL, 20, "#FFFFFF", MONO, 700)
    c.add(f'<g class="arrow"><circle cx="{x + W - 70}" cy="{y + 80}" r="36" fill="#FFFFFF"/><path d="M{x + W - 84},{y + 94} l28,-28 M{x + W - 80},{y + 66} h24 v24" stroke="{t["green"]}" stroke-width="5" fill="none" stroke-linecap="round"/></g>')
    c.css.append(".pulse{animation:pu 1.6s ease-in-out infinite}@keyframes pu{50%{opacity:.3}}"
                 ".eq{transform-box:fill-box;transform-origin:bottom;animation:eq .8s ease-in-out infinite alternate}@keyframes eq{from{transform:scaleY(.2)}}"
                 ".hand{animation:hd 4s linear infinite}@keyframes hd{to{transform:rotate(360deg)}}"
                 ".ring{animation:rg 2s ease-out both}@keyframes rg{from{stroke-dasharray:0 999}}"
                 ".glow{animation:pu 2.4s ease-in-out infinite}"
                 ".mq{animation:mq 40s linear infinite}@keyframes mq{to{transform:translateX(-2360px)}}"
                 ".ping{transform-box:fill-box;transform-origin:center;animation:pg 2s ease-out infinite}@keyframes pg{to{transform:scale(2.4);opacity:0}}"
                 ".arrow{animation:ar 1.4s ease-in-out infinite}@keyframes ar{50%{transform:translate(4px,-4px)}}")
    c.save(f"board-{th}.svg", f"Bento board for {NAME}: 9 apps in production, now shipping KioskSentinel, 30 minutes to 30 seconds, patent filed, 10 projects, the journey from Southern Railway to Indo Tech Transformers, speaks {', '.join(LANGUAGES)}. {EMAIL}")

links = " · ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Bento grid: one board of modular tiles, light and dark following your GitHub theme. Built by scripts/gen_bento.py -->

<p align="center">{pic(F, "board", f"Bento board for {NAME}")}</p>

<p align="center">{links}<br/><a href="mailto:{EMAIL}">email</a> · <a href="{LINKEDIN}">linkedin</a></p>
""")
print("ok")
