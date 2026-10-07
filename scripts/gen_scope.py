"""Monochromatic profile: one hue only. A phosphor-green oscilloscope (dark) and its chart-recorder printout (light).
Run: python scripts/gen_scope.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, wrap, MONO
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, EXPERIENCE, short

F = "scope"
THEMES = {"dark": dict(bg="#020A04", screen="#03140A", ink="#39FF88", dim="#1E8C4E", faint="#0C3A20", glow=1),
          "light": dict(bg="#F1F7F2", screen="#F7FBF8", ink="#0E5A2E", dim="#4F8F69", faint="#CFE5D6", glow=0)}


def path(fn, x0, w, y0, amp, n=240):
    return "M" + " L".join(f"{x0 + w * i / n:.1f},{y0 - amp * fn(i / n):.1f}" for i in range(n + 1))


def square(u, k):
    """Fourier partial sum of a square wave: k=1 is a pure sine, more terms sharpen it."""
    return sum(math.sin(2 * math.pi * 3 * u * (2 * j + 1)) / (2 * j + 1) for j in range(k)) * 4 / math.pi * .8


for th, t in THEMES.items():
    glow = (f'<filter id="ph" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="3" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>') if t["glow"] else '<filter id="ph"><feOffset/></filter>'
    # main scope screen
    c = Canvas(F, t, 1200, 640)
    c.defs.append(glow)
    c.add(f'<rect width="1200" height="640" rx="18" fill="{t["bg"]}"/><rect x="30" y="30" width="800" height="500" rx="10" fill="{t["screen"]}" stroke="{t["dim"]}" stroke-width="2"/>')
    for i in range(1, 10):
        c.add(f'<line x1="{30 + i * 80}" x2="{30 + i * 80}" y1="30" y2="530" stroke="{t["faint"]}" stroke-width="{2 if i == 5 else 1}"/>')
    for j in range(1, 8):
        c.add(f'<line x1="30" x2="830" y1="{30 + j * 62.5}" y2="{30 + j * 62.5}" stroke="{t["faint"]}" stroke-width="{2 if j == 4 else 1}"/>')
    # morphing trace: analog sine to digital square, frame by frame
    ks = [1, 2, 3, 5, 8, 14, 8, 5, 3, 2]
    for i, k in enumerate(ks):
        c.add(f'<path class="f f{i}" d="{path(lambda u: square(u, k), 30, 800, 280, 120)}" fill="none" stroke="{t["ink"]}" stroke-width="2.6" filter="url(#ph)"/>')
    steps = "".join(f".f{i}{{animation-delay:{i * .4:.1f}s}}" for i in range(len(ks)))
    c.css.append(f".f{{opacity:0;animation:fr {len(ks) * .4:.1f}s steps(1) infinite}}{steps}"
                 f"@keyframes fr{{0%{{opacity:1}}{100 / len(ks):.2f}%,100%{{opacity:0}}}}")
    c.text(46, 64, "CH1  ANALOG → DIGITAL", 15, t["ink"], MONO, 700, extra='filter="url(#ph)"')
    c.text(814, 64, "KRISHNA RAJU S", 15, t["ink"], MONO, 700, "end", 'filter="url(#ph)"')
    c.text(46, 516, "1 div = 1 career pivot      TRIG: curiosity ↑", 13, t["dim"], MONO)
    c.text(814, 516, "RUN", 13, t["ink"], MONO, 700, "end")
    # measurement panel
    c.add(f'<rect x="860" y="30" width="310" height="500" rx="10" fill="{t["screen"]}" stroke="{t["dim"]}" stroke-width="2"/>')
    c.text(880, 66, "MEASURE", 16, t["ink"], MONO, 700, extra='filter="url(#ph)"')
    meas = [("APPS", "9 live"), ("TESTS", "128 pass"), ("Δt TASK", "30m → 30s"), ("NEC RANK", "7 / 1500+"), ("PATENT", "filed"), ("CGPA", "8.38"), ("LANG", "ta en kn hi"), ("FUEL", "chai")]
    for i, (k, v) in enumerate(meas):
        y = 110 + i * 52
        c.add(f'<line x1="880" x2="1150" y1="{y + 16}" y2="{y + 16}" stroke="{t["faint"]}"/>')
        c.text(880, y, k, 13, t["dim"], MONO)
        c.text(1150, y, v, 17, t["ink"], MONO, 700, "end", 'filter="url(#ph)"')
    # knobs
    for i, lab in enumerate(["VOLTS/DIV", "TIME/DIV", "TRIGGER", "FOCUS"]):
        x = 100 + i * 200
        c.add(f'<circle cx="{x}" cy="585" r="24" fill="{t["screen"]}" stroke="{t["dim"]}" stroke-width="2"/>'
              f'<line x1="{x}" y1="585" x2="{x + 14 * math.cos(i + .5):.1f}" y2="{585 - 14 * math.sin(i + .5):.1f}" stroke="{t["ink"]}" stroke-width="3"/>')
        c.text(x + 36, 590, lab, 12, t["dim"], MONO)
    c.text(1150, 592, f"{EMAIL}", 13, t["ink"], MONO, 700, "end")
    c.save(f"scope-{th}.svg", f"Oscilloscope: a sine wave sharpens into a square wave, analog to digital. Measurements for {NAME}: 9 apps live, 128 tests, 30 minutes to 30 seconds, NEC rank 7 of 1500+, patent filed, CGPA 8.38.")

    # captured traces: one per project, plus Lissajous
    c = Canvas(F, t, 1200, 700)
    c.defs.append(glow)
    c.add(f'<rect width="1200" height="700" rx="18" fill="{t["bg"]}"/>')
    c.text(40, 54, "SAVED TRACES  ·  10 CAPTURES", 18, t["ink"], MONO, 700, extra='filter="url(#ph)"')
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        x, y = 40 + (i % 2) * 560, 84 + (i // 2) * 120
        c.add(f'<rect x="{x}" y="{y}" width="540" height="104" rx="8" fill="{t["screen"]}" stroke="{t["faint"]}" stroke-width="1.5"/>')
        f = (lambda u, i=i: math.sin(2 * math.pi * (u * (2 + i % 4)) + i) * (.4 + .6 * abs(math.sin(math.pi * u * (1 + i % 3)))))
        c.add(f'<path class="trace" style="animation-delay:{i * .3:.1f}s" d="{path(f, x + 300, 220, y + 56, 34, 120)}" fill="none" stroke="{t["ink"]}" stroke-width="2" filter="url(#ph)"/>')
        c.text(x + 16, y + 30, f"T{i + 1:02d}  {short(name).upper()}", 16, t["ink"], MONO, 700)
        first = wrap(hook, 13, 270, .6)
        c.text(x + 16, y + 56, first[0] + ("…" if len(first) > 1 else ""), 13, t["dim"], MONO)
        c.text(x + 16, y + 82, status.lower(), 12, t["ink"], MONO)
    c.css.append(".trace{stroke-dasharray:900;animation:tr 4s linear infinite}@keyframes tr{from{stroke-dashoffset:900}to{stroke-dashoffset:-900}}")
    c.save(f"traces-{th}.svg", "Saved traces: " + "; ".join(f"{p[1]}, {p[4]}" for p in PROJECTS))

    # lissajous + career frequency log
    c = Canvas(F, t, 1200, 420)
    c.defs.append(glow)
    c.add(f'<rect width="1200" height="420" rx="18" fill="{t["bg"]}"/><rect x="40" y="30" width="360" height="360" rx="10" fill="{t["screen"]}" stroke="{t["dim"]}" stroke-width="2"/>')
    for i, ph in enumerate([0, .4, .8, 1.2, 1.6, 2.0, 2.4, 2.8]):
        pts = " L".join(f"{220 + 150 * math.sin(3 * a + ph):.1f},{210 + 150 * math.sin(2 * a):.1f}" for a in [k * 2 * math.pi / 300 for k in range(301)])
        c.add(f'<path class="g g{i}" d="M{pts}" fill="none" stroke="{t["ink"]}" stroke-width="2" filter="url(#ph)"/>')
    c.css.append(".g{opacity:0;animation:fr 3.2s steps(1) infinite}" + "".join(f".g{i}{{animation-delay:{i * .4:.1f}s}}" for i in range(8))
                 + "@keyframes fr{0%{opacity:1}12.5%,100%{opacity:0}}")
    c.text(440, 70, "X: ELECTRICAL   Y: SOFTWARE   ratio 3:2, stable", 16, t["ink"], MONO, 700, extra='filter="url(#ph)"')
    for i, (org, role, when, where, what, win) in enumerate(EXPERIENCE):
        y = 120 + i * 54
        c.text(440, y, f"{when:<16}", 14, t["dim"], MONO)
        c.text(610, y, org.upper(), 16, t["ink"], MONO, 700)
        c.text(610, y + 22, win, 13, t["dim"], MONO)
    c.save(f"lissajous-{th}.svg", "Lissajous figure of electrical against software, and the career log: " + "; ".join(f"{e[2]} {e[0]}" for e in EXPERIENCE))

links = " · ".join(f"[{short(p[1]).lower()}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Monochromatic: one hue. Phosphor oscilloscope in dark mode, chart-recorder printout in light mode. Built by scripts/gen_scope.py -->

<p align="center">{pic(F, "scope", "Oscilloscope: analog to digital")}</p>
<p align="center">{pic(F, "traces", "Saved traces: ten projects")}</p>
<p align="center"><code>{links}</code></p>
<p align="center">{pic(F, "lissajous", "Lissajous figure and career log")}</p>
<p align="center"><sub><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}">linkedin</a></sub></p>
""")
print("ok")
