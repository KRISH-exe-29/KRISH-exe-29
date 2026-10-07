"""Futuristic profile: a holographic mission HUD. Rotating rings, a radar of projects, a scanned hologram, a mission log.
Run: python scripts/gen_future.py [photo]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, photo_grid, wrap
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, EXPERIENCE, WINS, short

F = "future"
SCI = "'Orbitron', 'Eurostile', 'Bahnschrift', 'Segoe UI', sans-serif"
MONO = "'JetBrains Mono', Consolas, monospace"
THEMES = {"dark": dict(bg="#020814", holo="#5CE1FF", hot="#FF8A3D", ink="#D8F6FF", soft="#4C7A95", faint="#0B2236", glow=1),
          "light": dict(bg="#F2F7FB", holo="#0077B6", hot="#E85D04", ink="#0B2540", soft="#5C7A90", faint="#D3E4F0", glow=0)}
photo = photo_grid(F, 52, sys.argv[1] if len(sys.argv) > 1 else None)


def arc(cx, cy, r, a0, a1):
    p = lambda a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
    (x0, y0), (x1, y1) = p(a0), p(a1)
    return f"M{x0:.1f},{y0:.1f} A{r},{r} 0 {1 if a1 - a0 > 180 else 0} 1 {x1:.1f},{y1:.1f}"


for th, t in THEMES.items():
    glow = (f'<filter id="gl" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            if t["glow"] else '<filter id="gl"><feOffset/></filter>')
    c = Canvas(F, t, 1200, 700)
    c.defs.append(glow + f'<radialGradient id="rad" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{t["holo"]}" stop-opacity=".18"/><stop offset="1" stop-color="{t["holo"]}" stop-opacity="0"/></radialGradient>'
                  f'<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["holo"]}" stop-opacity="0"/><stop offset="1" stop-color="{t["holo"]}" stop-opacity=".45"/></linearGradient>')
    c.add(f'<rect width="1200" height="700" fill="{t["bg"]}"/>')
    c.add("".join(f'<line x1="{x}" x2="{x}" y1="0" y2="700" stroke="{t["faint"]}"/>' for x in range(0, 1200, 40)))
    c.add("".join(f'<line x1="0" x2="1200" y1="{y}" y2="{y}" stroke="{t["faint"]}"/>' for y in range(0, 700, 40)))
    # hologram portrait in rings
    cx, cy = 300, 360
    c.add(f'<circle cx="{cx}" cy="{cy}" r="260" fill="url(#rad)"/>')
    for k, (r, a0, a1, dur, w) in enumerate([(250, 0, 300, 30, 2), (226, 20, 140, 18, 6), (226, 200, 320, 18, 6), (204, 0, 360, 60, 1)]):
        c.add(f'<g class="rot" style="animation-duration:{dur}s;animation-direction:{"reverse" if k % 2 else "normal"};transform-origin:{cx}px {cy}px">'
              f'<path d="{arc(cx, cy, r, a0, a1)}" fill="none" stroke="{t["holo"]}" stroke-width="{w}" stroke-dasharray="{"4 6" if k == 3 else "none"}" filter="url(#gl)"/></g>')
    for a in range(0, 360, 10):
        x1, y1 = cx + 262 * math.cos(math.radians(a)), cy + 262 * math.sin(math.radians(a))
        x2, y2 = cx + (272 if a % 30 == 0 else 267) * math.cos(math.radians(a)), cy + (272 if a % 30 == 0 else 267) * math.sin(math.radians(a))
        c.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{t["holo"]}" stroke-width="1.5"/>')
    cell = 7
    ox, oy = cx - 26 * cell, cy - 26 * cell
    dots = []
    for r, row in enumerate(photo):
        for q, ch in enumerate(row):
            if ch != ".":
                v = int(ch) / 9 if t["glow"] else (9 - int(ch)) / 9
                if v > .12:
                    dots.append(f'<circle cx="{ox + q * cell:.0f}" cy="{oy + r * cell:.0f}" r="{1 + 2.2 * v:.1f}" opacity="{.3 + .7 * v:.2f}"/>')
    c.add(f'<clipPath id="pc"><circle cx="{cx}" cy="{cy}" r="200"/></clipPath><g clip-path="url(#pc)" fill="{t["holo"]}" class="flick">{"".join(dots)}</g>')
    c.add(f'<rect class="scan" x="{cx - 200}" y="{cy - 200}" width="400" height="4" fill="{t["hot"]}" opacity=".8" filter="url(#gl)"/>')
    c.text(cx, 680, "HOLO-ID · SUBJECT VERIFIED", 13, t["soft"], SCI, 700, "middle", 'letter-spacing="3"')
    # right side readouts
    c.text(620, 90, "MISSION HUD // 2026", 16, t["hot"], SCI, 700, extra='letter-spacing="4"')
    c.text(620, 150, "KRISHNA RAJU S", 50, t["ink"], SCI, 700, extra='letter-spacing="3" filter="url(#gl)"')
    c.text(620, 188, "ELECTRICAL ENGINEER  ·  SOFTWARE ARCHITECT OF THE SHOP FLOOR", 14, t["holo"], SCI, 600, extra='letter-spacing="2"')
    stats = [("APPS DEPLOYED", 9, 12), ("TEST COVERAGE · DISPATCH", 128, 150), ("TIME SAVED / TASK", 98, 100), ("NEC PERCENTILE", 99.5, 100)]
    for i, (lab, v, mx) in enumerate(stats):
        y = 250 + i * 70
        c.text(620, y, lab, 13, t["soft"], SCI, 700, extra='letter-spacing="2"')
        c.text(1160, y, f"{v:g}{'%' if mx == 100 else ''}", 22, t["ink"], MONO, 700, "end", 'filter="url(#gl)"')
        c.add(f'<rect x="620" y="{y + 14}" width="540" height="6" fill="{t["faint"]}"/>'
              f'<rect class="fill" style="animation-delay:{.3 + i * .2:.1f}s" x="620" y="{y + 14}" width="{540 * v / mx:.0f}" height="6" fill="{t["holo"]}" filter="url(#gl)"/>')
        c.add("".join(f'<rect x="{620 + k * 27}" y="{y + 14}" width="2" height="6" fill="{t["bg"]}"/>' for k in range(1, 20)))
    c.text(620, 560, "STATUS: ONLINE · LOCATION: CHENNAI, EARTH · FUEL: CHAI", 13, t["holo"], MONO, extra='filter="url(#gl)"')
    c.text(620, 590, "NEXT OBJECTIVE: LIVE JOB STATUS FOR EVERY SHOP-FLOOR BAY", 13, t["hot"], MONO)
    c.css.append(".rot{animation:rt linear infinite}@keyframes rt{to{transform:rotate(360deg)}}"
                 f".scan{{animation:sc 3.5s ease-in-out infinite}}@keyframes sc{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(396px)}}}}"
                 ".flick{animation:fk 4s steps(1) infinite}@keyframes fk{0%,96%{opacity:1}97%{opacity:.4}98%{opacity:1}99%{opacity:.6}}"
                 ".fill{transform-box:fill-box;transform-origin:left;animation:fl 1.4s cubic-bezier(.2,.8,.2,1) backwards}@keyframes fl{from{transform:scaleX(0)}}")
    c.save(f"hud-{th}.svg", f"Mission HUD: hologram of {NAME}, electrical engineer and software architect of the shop floor. 9 apps deployed, 128 tests on dispatch, 98% time saved per task.")

    # radar of projects + mission log
    c = Canvas(F, t, 1200, 620)
    c.defs.append(glow + f'<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["holo"]}" stop-opacity="0"/><stop offset="1" stop-color="{t["holo"]}" stop-opacity=".5"/></linearGradient>')
    c.add(f'<rect width="1200" height="620" fill="{t["bg"]}"/>')
    rx, ry, R = 310, 310, 260
    for k in range(1, 5):
        c.add(f'<circle cx="{rx}" cy="{ry}" r="{R * k / 4}" fill="none" stroke="{t["holo"]}" stroke-opacity=".35"/>')
    c.add(f'<line x1="{rx - R}" x2="{rx + R}" y1="{ry}" y2="{ry}" stroke="{t["holo"]}" stroke-opacity=".3"/><line x1="{rx}" x2="{rx}" y1="{ry - R}" y2="{ry + R}" stroke="{t["holo"]}" stroke-opacity=".3"/>')
    c.add(f'<g class="sw" style="transform-origin:{rx}px {ry}px"><path d="M{rx},{ry} L{rx + R},{ry} A{R},{R} 0 0 0 {rx + R * math.cos(math.radians(-40)):.1f},{ry + R * math.sin(math.radians(-40)):.1f} Z" fill="url(#sweep)"/></g>')
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        a = i * 36 - 90
        d = R * (.35 + .55 * ((i * 7) % 10) / 10)
        bx, by = rx + d * math.cos(math.radians(a)), ry + d * math.sin(math.radians(a))
        col = t["hot"] if status in ("PRODUCTION", "LIVE") else t["holo"]
        c.add(f'<circle class="blip" style="animation-delay:{((a + 90) % 360) / 360 * 4:.2f}s" cx="{bx:.0f}" cy="{by:.0f}" r="7" fill="{col}" filter="url(#gl)"/>')
        c.text(bx + 12, by + 4, short(name).upper(), 11, t["ink"], SCI, 700, extra='letter-spacing="1"')
    c.text(640, 70, "MISSION LOG", 22, t["hot"], SCI, 700, extra='letter-spacing="4"')
    log = [(e[2], e[0], e[5]) for e in EXPERIENCE] + [(w, a, b) for w, a, b in WINS[:2]]
    for i, (when, what, note) in enumerate(log[:7]):
        y = 120 + i * 66
        c.add(f'<rect x="640" y="{y - 22}" width="520" height="54" fill="{t["faint"]}" opacity=".6"/><rect x="640" y="{y - 22}" width="3" height="54" fill="{t["holo"]}"/>')
        c.text(656, y, f"[{when}]", 12, t["soft"], MONO)
        c.text(656, y + 22, what.upper(), 15, t["ink"], SCI, 700, extra='letter-spacing="1"')
        nl = wrap(note, 12, 250, .6)
        c.text(1148, y + 22, nl[0] + ("…" if len(nl) > 1 else ""), 12, t["holo"], MONO, anchor="end")
    c.css.append(".sw{animation:rt 4s linear infinite}@keyframes rt{to{transform:rotate(360deg)}}"
                 ".blip{animation:bp 4s linear infinite}@keyframes bp{0%{opacity:1}30%{opacity:.25}100%{opacity:.25}}")
    c.save(f"radar-{th}.svg", "Radar of 10 projects and a mission log: " + "; ".join(f"{a} {b}" for a, b, _ in log[:7]))

links = " · ".join(f"[{short(p[1]).upper()}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Futuristic holographic HUD: deep-space dark mode, clean-lab light mode. Built by scripts/gen_future.py -->

<p align="center">{pic(F, "hud", f"Mission HUD for {NAME}")}</p>
<p align="center">{pic(F, "radar", "Radar of projects and mission log")}</p>
<p align="center"><sub>LOCK ON: {links}</sub></p>
<p align="center"><sub>OPEN CHANNEL → <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}">LINKEDIN</a></sub></p>
""")
print("ok")
