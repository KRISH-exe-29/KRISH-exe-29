"""Parallax profile: a looping landscape where each layer moves at its own speed, and project cards floating at
different depths. Day and night versions. Run: python scripts/gen_parallax.py"""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, SANS
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short

F = "parallax"
THEMES = {"light": dict(sky1="#8EC5FF", sky2="#FFE3C2", sun="#FFD166", far="#A9B8D6", mid="#7F93BA", near="#4B5D86", road="#2E3A59", win="#FFE8A3", ink="#1B2238", card="#FFFFFF", night=0),
          "dark": dict(sky1="#070B1E", sky2="#2B1B4A", sun="#F4F1DE", far="#1E2546", mid="#283160", near="#121733", road="#0A0D1F", win="#FFD166", ink="#F1F3FF", card="#151A36", night=1)}
W = 1200


def strip(content_fn, speed, cls):
    """Two copies side by side, translated by one width per loop: seamless, at this layer's own speed."""
    return f'<g class="{cls}" style="animation-duration:{speed}s">{content_fn(0)}{content_fn(W)}</g>'


for th, t in THEMES.items():
    rnd = random.Random(7)
    c = Canvas(F, t, W, 600)
    c.defs.append(f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["sky1"]}"/><stop offset="1" stop-color="{t["sky2"]}"/></linearGradient>')
    c.add(f'<rect width="{W}" height="600" fill="url(#sky)"/>')
    if t["night"]:
        c.add("".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, 300):.0f}" r="{rnd.choice([1, 1.5])}" fill="#FFF" opacity="{rnd.uniform(.4, 1):.2f}"/>' for _ in range(90)))
    c.add(f'<circle cx="930" cy="150" r="56" fill="{t["sun"]}"/>')
    clouds = [(rnd.uniform(0, W), rnd.uniform(60, 220), rnd.uniform(.6, 1.3)) for _ in range(5)]
    c.add(strip(lambda o: "".join(f'<g opacity="{.25 if t["night"] else .9}" fill="#FFFFFF"><ellipse cx="{x + o:.0f}" cy="{y:.0f}" rx="{60 * s:.0f}" ry="{18 * s:.0f}"/>'
                                   f'<ellipse cx="{x + o + 30 * s:.0f}" cy="{y - 12 * s:.0f}" rx="{34 * s:.0f}" ry="{18 * s:.0f}"/></g>' for x, y, s in clouds), 120, "pan"))
    far = lambda o: f'<path d="M{o},420 ' + " ".join(f"L{o + x},{340 + 50 * math.sin(x / 90) + 30 * math.sin(x / 37):.0f}" for x in range(0, W + 1, 40)) + f' L{o + W},600 L{o},600Z" fill="{t["far"]}"/>'
    c.add(strip(far, 90, "pan"))
    def mid(o):
        out = f'<path d="M{o},470 ' + " ".join(f"L{o + x},{420 + 25 * math.sin(x / 140):.0f}" for x in range(0, W + 1, 40)) + f' L{o + W},600 L{o},600Z" fill="{t["mid"]}"/>'
        for k in range(4):
            px = o + 150 + k * 300
            out += (f'<path d="M{px - 18},450 L{px},330 L{px + 18},450 M{px - 30},360 H{px + 30} M{px - 22},390 H{px + 22}" stroke="{t["near"]}" stroke-width="3" fill="none"/>'
                    f'<path d="M{px - 30},360 Q{px + 120},392 {px + 270},360" stroke="{t["near"]}" stroke-width="1.5" fill="none"/>')
        return out
    c.add(strip(mid, 50, "pan"))
    def near(o):
        out = ""
        x = o
        for k in range(14):
            w, h = 60 + (k * 37) % 50, 70 + (k * 53) % 90
            out += f'<rect x="{x}" y="{520 - h}" width="{w}" height="{h}" fill="{t["near"]}"/>'
            for wy in range(520 - h + 12, 510, 18):
                for wx in range(x + 8, x + w - 8, 16):
                    if (wx * 7 + wy * 3) % 5 < (3 if t["night"] else 1):
                        out += f'<rect x="{wx}" y="{wy}" width="7" height="8" fill="{t["win"]}"/>'
            x += w + 26
        return out
    c.add(strip(near, 30, "pan"))
    def road(o):
        out = f'<rect x="{o}" y="520" width="{W}" height="80" fill="{t["road"]}"/>' + "".join(f'<rect x="{o + k * 80}" y="556" width="40" height="5" fill="{t["win"]}" opacity=".7"/>' for k in range(15))
        for k in range(2):
            tx = o + 200 + k * 600
            out += (f'<rect x="{tx}" y="508" width="90" height="34" rx="3" fill="#E85D04"/><rect x="{tx + 90}" y="516" width="34" height="26" rx="3" fill="#F48C06"/>'
                    f'<circle cx="{tx + 20}" cy="546" r="8" fill="#111"/><circle cx="{tx + 104}" cy="546" r="8" fill="#111"/>'
                    f'<text x="{tx + 45}" y="530" font-family="{SANS}" font-size="11" font-weight="700" fill="#FFF" text-anchor="middle">DISPATCH</text>')
        return out
    c.add(strip(road, 12, "pan"))
    c.add(f'<rect x="60" y="60" width="560" height="200" rx="20" fill="{t["card"]}" opacity=".86"/>')
    c.text(90, 128, NAME, 50, t["ink"], SANS, 800, extra='letter-spacing="-1.5"')
    c.text(92, 172, "Electrical engineer. Software builder.", 22, t["ink"], SANS, 500)
    c.text(92, 214, "Everything here moves at its own speed. Except the deadlines.", 16, t["ink"], SANS, extra='opacity=".7"')
    c.css.append(f".pan{{animation:pan linear infinite}}@keyframes pan{{to{{transform:translateX(-{W}px)}}}}")
    c.save(f"landscape-{th}.svg", f"Parallax landscape for {NAME}: clouds, mountains, power pylons, a city skyline and dispatch trucks each moving at a different speed.")

    # depth cards
    c = Canvas(F, t, W, 720)
    c.defs.append(f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["sky1"]}"/><stop offset="1" stop-color="{t["sky2"]}"/></linearGradient>'
                  + "".join(f'<filter id="d{k}"><feGaussianBlur stdDeviation="{k * .5}"/></filter>' for k in range(3)))
    c.add(f'<rect width="{W}" height="720" fill="url(#sky)"/>')
    c.text(W / 2, 64, "Ten projects at three depths", 32, t["ink"], SANS, 800, "middle")
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        depth = [2, 0, 1, 0, 2, 1, 0, 2, 1, 0][i]
        sc = [1, .86, .72][depth]
        x, y = 40 + (i % 5) * 228, 110 + (i // 5) * 300 + depth * 24
        w, h = 210 * sc, 250 * sc
        x += (210 - w) / 2
        c.add(f'<g class="fl" style="animation-duration:{4 + depth * 2}s;animation-delay:-{i * .7:.1f}s" opacity="{[1, .85, .7][depth]}" filter="url(#d{depth})">'
              f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="18" fill="{t["card"]}" style="filter:drop-shadow(0 {14 - depth * 4}px {16 - depth * 4}px rgba(0,0,0,.25))"/>')
        c.text(x + w / 2, y + h * .32, short(name), 20 * sc, t["ink"], SANS, 800, "middle")
        c.text(x + w / 2, y + h * .44, status.lower(), 13 * sc, "#E85D04", SANS, 700, "middle")
        words, lines, line = hook.split(), [], ""
        for wd in words:
            if len(line + wd) > 22:
                lines.append(line.strip()); line = ""
            line += wd + " "
        lines.append(line.strip())
        for j, l in enumerate(lines[:3]):
            c.text(x + w / 2, y + h * .6 + j * 20 * sc, l, 14 * sc, t["ink"], SANS, anchor="middle", extra='opacity=".8"')
        c.add("</g>")
    c.css.append(".fl{animation:fl ease-in-out infinite}@keyframes fl{50%{transform:translateY(-14px)}}")
    c.save(f"depth-{th}.svg", "Ten projects floating at three depths: " + "; ".join(f"{p[1]}, {p[4]}" for p in PROJECTS))

links = " · ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Parallax: layered landscape moving at five speeds and cards floating at three depths. Day and night follow your GitHub theme. Built by scripts/gen_parallax.py -->

<p align="center">{pic(F, "landscape", f"Parallax landscape for {NAME}")}</p>
<p align="center">{pic(F, "depth", "Ten projects at three depths")}</p>
<p align="center">{links}</p>
<p align="center"><sub><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}">linkedin</a></sub></p>
""")
print("ok")
