"""Minimal, theme-matched SVGs: an animated ASCII portrait and an ASCII dancer.

Run:  python scripts/gen_ascii.py   (portraits from assets/ascii/portrait-<theme>.txt, made by scripts/portrait.py)
Backgrounds match GitHub's own page colours, so each image melts into the page in either theme.
"""
import os, random
from xml.sax.saxutils import escape as esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "ascii")
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
THEMES = {"light": dict(bg="#FFFFFF", ink="#1F2328", muted="#656D76", accent="#FF5A1F"),
          "dark": dict(bg="#0D1117", ink="#E6EDF3", muted="#8D96A0", accent="#FF8A5B")}
GLYPHS = "01#%&*+=-:<>/\\{}[]$@?"
REDUCE = "@media (prefers-reduced-motion: reduce){.f{animation:none!important;opacity:0}.still{opacity:1}*{animation:none!important}}"


def frames_css(windows, total):
    """windows: {frame_id: [(start_s, end_s), ...]} -> keyframes that show each frame only inside its windows."""
    css = [f".f{{opacity:0;animation-duration:{total}s;animation-iteration-count:infinite;animation-timing-function:step-end}}"]
    for fid, wins in windows.items():
        steps = ["0%{opacity:0}"] + [f"{100 * s / total:.3f}%{{opacity:1}}{100 * e / total:.3f}%{{opacity:0}}" for s, e in wins]
        css.append(f"#{fid}{{animation-name:k{fid}}}@keyframes k{fid}{{{''.join(steps)}}}")
    return "".join(css)


def rows_svg(lines, x, y, cw, lh):
    return "".join(f'<text x="{x}" y="{y + i * lh:.1f}" textLength="{len(l) * cw:.1f}" lengthAdjust="spacingAndGlyphs" '
                   f'xml:space="preserve">{esc(l)}</text>' for i, l in enumerate(lines) if l.strip())


def decode(art, lock, rng, p):
    return ["".join(c if c == " " or lock[y][x] < p else rng.choice(GLYPHS) for x, c in enumerate(line)) for y, line in enumerate(art)]


def glitch(art, rng, bands):
    out = list(art)
    for _ in range(bands):
        y0 = rng.randrange(len(art) - 4)
        for y in range(y0, y0 + rng.randint(1, 4)):
            s = rng.choice([-1, 1]) * rng.randint(2, 7)
            line = (" " * 8 + art[y] + " " * 8)[8 - s:]
            out[y] = "".join(rng.choice(GLYPHS) if c != " " and rng.random() < .3 else c for c in line)
    return out


# timeline (seconds): decode in, hold, two glitches, hold, dissolve out
DEC = [.12, .25, .38, .5, .62, .74, .86, .95]
win = {f"d{i}": [(i * .12, (i + 1) * .12)] for i in range(8)}
win["still"] = [(.96, 6.0), (6.12, 6.5), (6.74, 9.2)]
win.update({"g0": [(6.0, 6.12)], "g1": [(6.5, 6.62)], "g2": [(6.62, 6.74)]})
for j, i in enumerate([7, 5, 3, 1, 0]):  # dissolve back out through the decode frames
    win[f"d{i}"].append((9.2 + j * .16, 9.36 + j * .16))
TOTAL = 10.0

CW, LH, PX, PY = 4.3, 8.2, 40, 52
for theme, t in THEMES.items():
    art = open(os.path.join(OUT, f"portrait-{theme}.txt"), encoding="utf-8").read().split("\n")
    rng = random.Random(29)
    lock = [[rng.random() for _ in line] for line in art]  # when each character "locks in" during the decode
    seq = ([(f"d{i}", decode(art, lock, rng, p)) for i, p in enumerate(DEC)] + [("still", art)]
           + [(f"g{i}", glitch(art, rng, 4 + i)) for i in range(3)])
    groups = "".join(f'<g id="{fid}" class="f{" still" if fid == "still" else ""}">{rows_svg(lines, PX, PY, CW, LH)}</g>' for fid, lines in seq)
    status = ["shipping KioskSentinel", "deleting another spreadsheet", "mapping the shop floor, bay by bay"]
    st = "".join(f'<text class="s s{i}" x="620" y="452" font-family="{MONO}" font-size="17" fill="{t["muted"]}">'
                 f'<tspan fill="{t["accent"]}">now ›</tspan> {esc(s)}</text>' for i, s in enumerate(status))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="540" viewBox="0 0 1200 540" role="img" aria-label="Animated ASCII portrait of Krishna Raju S. I write the software a transformer factory runs on.">
<title>Animated ASCII portrait of Krishna Raju S. I write the software a transformer factory runs on.</title>
<style>{frames_css(win, TOTAL)}
.s{{opacity:0;animation:cy 12s infinite}}.s0{{opacity:1}}.s1{{animation-delay:4s}}.s2{{animation-delay:8s}}
@keyframes cy{{0%{{opacity:0}}3%,31%{{opacity:1}}34%,100%{{opacity:0}}}}
.cur{{animation:bl 1s steps(1) infinite}}@keyframes bl{{50%{{opacity:0}}}}{REDUCE}</style>
<rect width="1200" height="540" fill="{t['bg']}"/>
<g font-family="{MONO}" font-size="8" fill="{t['ink']}">{groups}</g>
<text x="620" y="118" font-family="{MONO}" font-size="16" fill="{t['muted']}">~/krishna-raju-s</text>
<text font-family="{SANS}" font-size="50" font-weight="300" fill="{t['ink']}" letter-spacing="-1.5">
  <tspan x="616" y="196">I write the software</tspan><tspan x="616" y="256">a transformer factory</tspan><tspan x="616" y="316" font-weight="600" fill="{t['accent']}">runs on.</tspan></text>
<text x="620" y="372" font-family="{MONO}" font-size="16" fill="{t['muted']}">electrical engineer · indo tech transformers</text>
<line x1="620" x2="1150" y1="410" y2="410" stroke="{t['muted']}" stroke-opacity=".3"/>
{st}
<rect class="cur" x="1124" y="438" width="9" height="18" fill="{t['accent']}"/>
</svg>
"""
    with open(os.path.join(OUT, f"hero-{theme}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)

# ── ASCII dancer ──
POSES = {
    "up":    [r"\o/", r" | ", r"/ \ "],
    "left":  [r"_o/", r" | ", r"/ >"],
    "right": [r"\o_", r" | ", r"< \ "],
    "rest":  [r" o ", r"/|\ ", r"/ \ "],
    "flat":  [r"_o_", r" | ", r"/ \ "],
    "kick":  [r" o/", r"/| ", r" |\_"],
}
ORDER = ["up", "left", "up", "right", "rest", "flat", "kick", "flat"]
STEP = .22
for theme, t in THEMES.items():
    total = STEP * len(ORDER)
    dwin = {}
    for i, pose in enumerate(ORDER):
        dwin.setdefault(f"p{pose}", []).append((i * STEP, (i + 1) * STEP))
    groups = ""
    for pose, lines in POSES.items():
        rows = "".join(f'<text x="96" y="{78 + j * 40}" xml:space="preserve">{esc(l)}</text>' for j, l in enumerate(lines))
        groups += f'<g id="p{pose}" class="f{" still" if pose == "up" else ""}">{rows}</g>'
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="200" viewBox="0 0 1200 200" role="img" aria-label="An ASCII stick figure dancing: me when the deploy goes green.">
<title>An ASCII stick figure dancing: me when the deploy goes green.</title>
<style>{frames_css(dwin, round(total, 2))}{REDUCE}</style>
<rect width="1200" height="200" fill="{t['bg']}"/>
<g font-family="{MONO}" font-size="40" font-weight="700" fill="{t['ink']}">{groups}</g>
<line x1="78" x2="200" y1="176" y2="176" stroke="{t['muted']}" stroke-width="3" stroke-linecap="round"/>
<text x="300" y="98" font-family="{SANS}" font-size="38" font-weight="300" fill="{t['ink']}" letter-spacing="-1">me, every time a deploy goes <tspan font-weight="600" fill="{t['accent']}">green</tspan>.</text>
<text x="302" y="138" font-family="{MONO}" font-size="17" fill="{t['muted']}">// so, roughly every day.</text>
</svg>
"""
    with open(os.path.join(OUT, f"dancer-{theme}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
print("ok")
