"""Glass + 3D profile: a translucent glass cube turning in true orthographic 3D (labels mapped onto its faces),
floating glass orbs and frosted panels over a vivid backdrop. Run: python scripts/gen_glass3d.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, SANS
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short
from xml.sax.saxutils import escape as esc

F = "glass3d"
THEMES = {"dark": dict(bg1="#0B0630", bg2="#3A0CA3", bg3="#F72585", ink="#FFFFFF", soft="#D9D2FF", face="#B9A8FF", rim="#FFFFFF"),
          "light": dict(bg1="#FDE2F3", bg2="#C8E7FF", bg3="#FFD6A5", ink="#1B1340", soft="#4B3F7A", face="#7B61FF", rim="#FFFFFF")}
LABELS = ["ELECTRICAL", "SOFTWARE", "AUTOMATION", "IoT"]
V = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
FACES = [((0, 2, 3, 1), "x-"), ((4, 5, 7, 6), "x+"), ((0, 1, 5, 4), "y-"), ((2, 6, 7, 3), "y+"), ((0, 4, 6, 2), "z-"), ((1, 3, 7, 5), "z+")]
SIDE_LABEL = {"y-": 0, "x+": 1, "y+": 2, "x-": 3, "z+": None}


def rot(p, yaw, tilt=.5):
    x, y, z = p
    x, y = x * math.cos(yaw) - y * math.sin(yaw), x * math.sin(yaw) + y * math.cos(yaw)
    y, z = y * math.cos(tilt) - z * math.sin(tilt), y * math.sin(tilt) + z * math.cos(tilt)
    return x, y, z


def backdrop(c, t, w, h):
    c.defs.append(f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg1"]}"/><stop offset=".55" stop-color="{t["bg2"]}"/><stop offset="1" stop-color="{t["bg3"]}"/></linearGradient>'
                  f'<radialGradient id="orb" cx=".35" cy=".3" r=".7"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".95"/><stop offset=".35" stop-color="#FFFFFF" stop-opacity=".25"/>'
                  f'<stop offset="1" stop-color="{t["face"]}" stop-opacity=".35"/></radialGradient>'
                  '<filter id="soft"><feGaussianBlur stdDeviation="40"/></filter>')
    c.add(f'<rect width="{w}" height="{h}" fill="url(#bg)"/>',
          f'<circle cx="{w * .2:.0f}" cy="{h * .8:.0f}" r="{h * .35:.0f}" fill="{t["bg3"]}" opacity=".5" filter="url(#soft)"/>',
          f'<circle cx="{w * .85:.0f}" cy="{h * .15:.0f}" r="{h * .3:.0f}" fill="{t["bg2"]}" opacity=".6" filter="url(#soft)"/>')


def orb(c, x, y, r, delay):
    c.add(f'<g class="bob" style="animation-delay:-{delay}s"><circle cx="{x}" cy="{y}" r="{r}" fill="url(#orb)" stroke="#FFFFFF" stroke-opacity=".6"/>'
          f'<ellipse cx="{x - r * .3:.0f}" cy="{y - r * .4:.0f}" rx="{r * .35:.0f}" ry="{r * .18:.0f}" fill="#FFFFFF" opacity=".8"/></g>')


for th, t in THEMES.items():
    c = Canvas(F, t, 1200, 640)
    backdrop(c, t, 1200, 640)
    # glass cube, 30 frames
    N, S, CX, CY = 48, 120, 860, 330
    for f in range(N):
        yaw = 2 * math.pi * f / N  # one full turn per loop
        pts = [rot(v, yaw) for v in V]
        faces = []
        for idx, key in FACES:
            q = [pts[i] for i in idx]
            depth = sum(p[1] for p in q) / 4
            e1 = [q[1][k] - q[0][k] for k in range(3)]
            e2 = [q[3][k] - q[0][k] for k in range(3)]
            normal_y = e1[2] * e2[0] - e1[0] * e2[2]
            faces.append((depth, q, key, normal_y))
        g = []
        for depth, q, key, ny in sorted(faces, key=lambda x: -x[0]):
            front = depth < 0
            poly = " ".join(f"{CX + p[0] * S:.1f},{CY - p[2] * S:.1f}" for p in q)
            g.append(f'<polygon points="{poly}" fill="{t["face"]}" fill-opacity="{.32 if front else .1}" stroke="{t["rim"]}" stroke-opacity="{.85 if front else .3}" stroke-width="2"/>')
            li = SIDE_LABEL.get(key)
            if front and key != "z-":
                P = [(CX + p[0] * S, CY - p[2] * S, p[2]) for p in q]
                if key != "z+":  # side face: anchor at the top-left corner so text stays upright
                    top = sorted(P, key=lambda p: -p[2])[:2]
                    tl, tr = sorted(top, key=lambda p: p[0])
                    bl = min(sorted(P, key=lambda p: p[2])[:2], key=lambda p: abs(p[0] - tl[0]))
                    p0, ex, ey = tl, (tr[0] - tl[0], tr[1] - tl[1]), (bl[0] - tl[0], bl[1] - tl[1])
                else:
                    best = None  # top face: pick the corner and edge order that reads most upright, never mirrored
                    for k in range(4):
                        for d in (1, -1):
                            a0, a1, a3 = P[k], P[(k + d) % 4], P[(k - d) % 4]
                            ex_, ey_ = (a1[0] - a0[0], a1[1] - a0[1]), (a3[0] - a0[0], a3[1] - a0[1])
                            if ex_[0] * ey_[1] - ex_[1] * ey_[0] > 0:
                                score = ex_[0] + ey_[1]
                                if best is None or score > best[0]:
                                    best = (score, a0, ex_, ey_)
                    _, p0, ex, ey = best
                lab = "KRS" if li is None else LABELS[li]
                g.append(f'<text transform="matrix({ex[0] / 200:.4f} {ex[1] / 200:.4f} {ey[0] / 200:.4f} {ey[1] / 200:.4f} {p0[0]:.1f} {p0[1]:.1f})" '
                         f'x="100" y="112" font-family="{SANS}" font-size="{30 if li is not None else 54}" font-weight="800" fill="{t["ink"]}" text-anchor="middle" opacity=".92">{lab}</text>')
        c.add(f'<g class="fr f{f}">{"".join(g)}</g>')
    c.css.append(f".fr{{opacity:0;animation:fr {N * .12:.2f}s steps(1) infinite}}" + "".join(f".f{f}{{animation-delay:{f * .12:.2f}s}}" for f in range(N))
                 + f"@keyframes fr{{0%{{opacity:1}}{100 / N:.3f}%,100%{{opacity:0}}}}"
                 + ".bob{animation:bob 6s ease-in-out infinite}@keyframes bob{50%{transform:translateY(-18px)}}")
    orb(c, 640, 140, 38, 0)
    orb(c, 1110, 520, 52, 2)
    orb(c, 700, 560, 24, 4)
    # frosted panel
    c.add(f'<rect x="50" y="130" width="520" height="380" rx="30" fill="#FFFFFF" fill-opacity=".14" stroke="#FFFFFF" stroke-opacity=".55" stroke-width="1.5"/>'
          f'<rect x="50" y="130" width="520" height="90" rx="30" fill="#FFFFFF" fill-opacity=".12"/>')
    c.text(86, 214, "Krishna", 64, t["ink"], SANS, 800, extra='letter-spacing="-2"')
    c.text(86, 286, "Raju S.", 64, t["ink"], SANS, 800, extra='letter-spacing="-2"')
    c.para(88, 340, "Four faces, one engineer. Electrical by training, software by habit, automation by reflex, IoT for fun.", 19, 450, fill=t["soft"], font=SANS)
    c.text(88, 470, "9 apps live · patent filed · NEC #7", 17, t["ink"], SANS, 700)
    c.save(f"cube-{th}.svg", f"A turning glass cube with faces ELECTRICAL, SOFTWARE, AUTOMATION and IoT, beside a frosted panel: {NAME}, four faces, one engineer.")

    # projects on glass tiles with tiny 3D blocks
    c = Canvas(F, t, 1200, 700)
    backdrop(c, t, 1200, 700)
    c.text(600, 70, "Ten things, rendered in production", 34, t["ink"], SANS, 800, "middle", 'letter-spacing="-1"')
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        x, y = 50 + (i % 5) * 224, 110 + (i // 5) * 290
        c.add(f'<rect x="{x}" y="{y}" width="204" height="268" rx="24" fill="#FFFFFF" fill-opacity=".14" stroke="#FFFFFF" stroke-opacity=".55"/>')
        bx, by, s = x + 102, y + 80, 26
        hgt = 20 + (len(hook) % 5) * 8
        c.add(f'<g class="bob" style="animation-delay:-{i * .6:.1f}s">'
              f'<polygon points="{bx},{by - hgt - s} {bx + 2 * s},{by - hgt} {bx},{by - hgt + s} {bx - 2 * s},{by - hgt}" fill="#FFFFFF" fill-opacity=".55" stroke="#FFF"/>'
              f'<polygon points="{bx - 2 * s},{by - hgt} {bx},{by - hgt + s} {bx},{by + s} {bx - 2 * s},{by}" fill="{t["face"]}" fill-opacity=".45" stroke="#FFF" stroke-opacity=".7"/>'
              f'<polygon points="{bx + 2 * s},{by - hgt} {bx},{by - hgt + s} {bx},{by + s} {bx + 2 * s},{by}" fill="{t["face"]}" fill-opacity=".25" stroke="#FFF" stroke-opacity=".7"/></g>')
        c.text(x + 102, y + 160, short(name), 18, t["ink"], SANS, 800, "middle")
        c.text(x + 102, y + 182, status.lower(), 12, t["soft"], SANS, 700, "middle")
        words, lines, line = hook.split(), [], ""
        for wd in words:
            if len(line + wd) > 24:
                lines.append(line.strip()); line = ""
            line += wd + " "
        lines.append(line.strip())
        for j, l in enumerate(lines[:2]):
            c.text(x + 102, y + 210 + j * 19, l, 13, t["ink"], SANS, anchor="middle")
    c.css.append(".bob{animation:bob 5s ease-in-out infinite}@keyframes bob{50%{transform:translateY(-8px)}}")
    c.save(f"tiles-{th}.svg", "Ten projects on glass tiles: " + "; ".join(f"{p[1]}, {p[4]}" for p in PROJECTS))

links = " · ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Glass + 3D: a glass cube turning in true 3D, glass orbs and frosted panels. Night and day backdrops follow your GitHub theme. Built by scripts/gen_glass3d.py -->

<p align="center">{pic(F, "cube", f"Glass cube: four faces, one engineer. {NAME}")}</p>
<p align="center">{pic(F, "tiles", "Ten projects on glass tiles")}</p>
<p align="center">{links}</p>
<p align="center"><sub><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}">linkedin</a></sub></p>
""")
print("ok")
