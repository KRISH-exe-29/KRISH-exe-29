"""3D profile: a power-transformer mesh, shipped as a rotatable STL viewer (GitHub renders ```stl blocks) and as a
spinning wireframe SVG, plus isometric 3D stat blocks. Run: python scripts/gen_3d.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, SANS, MONO
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short

F = "3d"
THEMES = {"dark": dict(bg="#07090F", ink="#E6EDF7", soft="#7C8BA1", edge="#58A6FF", hot="#F78166", grid="#161B22", top="#2F81F7", left="#1F4E99", right="#173A73"),
          "light": dict(bg="#F6F8FA", ink="#1F2328", soft="#59636E", edge="#0969DA", hot="#CF222E", grid="#E1E6EB", top="#54AEFF", left="#218BFF", right="#0969DA")}


# ── a tiny mesh kit: boxes and cylinders as triangles, plus their visible edges ──
def box(x0, y0, z0, dx, dy, dz):
    v = [(x0 + a * dx, y0 + b * dy, z0 + c * dz) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
    faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    tris = [(v[a], v[b], v[c]) for f in faces for a, b, c in ((f[0], f[1], f[2]), (f[0], f[2], f[3]))]
    edges = [(v[a], v[b]) for a, b in [(0, 1), (1, 3), (3, 2), (2, 0), (4, 5), (5, 7), (7, 6), (6, 4), (0, 4), (1, 5), (2, 6), (3, 7)]]
    return tris, edges


def cylinder(cx, cy, z0, r, h, n=10, axis="z"):
    def p(a, z):
        u, w = r * math.cos(a), r * math.sin(a)
        return (cx + u, cy + w, z) if axis == "z" else (z, cy + u, cx + w)  # axis x: z is the x coordinate
    ring0 = [p(2 * math.pi * i / n, z0) for i in range(n)]
    ring1 = [p(2 * math.pi * i / n, z0 + h) for i in range(n)]
    c0 = (cx, cy, z0) if axis == "z" else (z0, cy, cx)
    c1 = (cx, cy, z0 + h) if axis == "z" else (z0 + h, cy, cx)
    tris, edges = [], []
    for i in range(n):
        j = (i + 1) % n
        tris += [(ring0[i], ring0[j], ring1[j]), (ring0[i], ring1[j], ring1[i]), (c0, ring0[j], ring0[i]), (c1, ring1[i], ring1[j])]
        edges += [(ring0[i], ring0[j]), (ring1[i], ring1[j])] + ([(ring0[i], ring1[i])] if i % 2 == 0 else [])
    return tris, edges


parts = [box(-45, -25, 0, 90, 50, 70), box(-50, -30, -6, 100, 60, 6)]
for i in range(6):
    parts += [box(-40 + i * 15, 25, 6, 4, 14, 58), box(-40 + i * 15, -39, 6, 4, 14, 58)]
for i, x in enumerate((-25, 0, 25)):
    parts += [cylinder(x, 8, 70, 4.5, 34), cylinder(x, 8, 104, 7, 4)]
    parts += [cylinder(x, -12, 70, 3, 16)]
parts += [box(-36, 18, 70, 4, 4, 40), box(32, 18, 70, 4, 4, 40), cylinder(118, 20, -45, 10, 90, 12, axis="x")]
TRIS = [t for p in parts for t in p[0]]
EDGES = [e for p in parts for e in p[1]]


def stl():
    out = ["solid transformer"]
    for a, b, c in TRIS:
        u = [b[k] - a[k] for k in range(3)]
        v = [c[k] - a[k] for k in range(3)]
        n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
        ln = math.sqrt(sum(x * x for x in n)) or 1
        out.append(f"facet normal {n[0] / ln:.2f} {n[1] / ln:.2f} {n[2] / ln:.2f}\nouter loop\n"
                   + "".join(f"vertex {p[0]:.1f} {p[1]:.1f} {p[2]:.1f}\n" for p in (a, b, c)) + "endloop\nendfacet")
    out.append("endsolid transformer")
    return "\n".join(out)


def project(p, yaw, pitch=-.42, s=2.3, cx=840, cy=350):
    x, y, z = p
    x, y = x * math.cos(yaw) - y * math.sin(yaw), x * math.sin(yaw) + y * math.cos(yaw)
    y, z = y * math.cos(pitch) - (z - 50) * math.sin(pitch), y * math.sin(pitch) + (z - 50) * math.cos(pitch)
    return cx + x * s, cy - z * s


for th, t in THEMES.items():
    c = Canvas(F, t, 1200, 640)
    c.add(f'<rect width="1200" height="640" fill="{t["bg"]}"/>')
    c.add("".join(f'<line x1="{x}" x2="{x}" y1="420" y2="640" stroke="{t["grid"]}"/>' for x in range(0, 1201, 60)) +
          "".join(f'<line x1="0" x2="1200" y1="{y}" y2="{y}" stroke="{t["grid"]}"/>' for y in range(420, 641, 30)))
    N = 24
    for f in range(N):
        yaw = 2 * math.pi * f / N
        d = " ".join(f"M{project(a, yaw)[0]:.0f},{project(a, yaw)[1]:.0f}L{project(b, yaw)[0]:.0f},{project(b, yaw)[1]:.0f}" for a, b in EDGES)
        c.add(f'<path class="fr f{f}" d="{d}" fill="none" stroke="{t["edge"]}" stroke-width="1.4" stroke-linejoin="round"/>')
    c.css.append(f".fr{{opacity:0;animation:fr {N * .15:.2f}s steps(1) infinite}}" + "".join(f".f{f}{{animation-delay:{f * .15:.2f}s}}" for f in range(N))
                 + f"@keyframes fr{{0%{{opacity:1}}{100 / N:.3f}%,100%{{opacity:0}}}}")
    c.text(60, 80, "KRISHNA RAJU S", 44, t["ink"], SANS, 700, extra='letter-spacing="-1"')
    c.text(60, 114, "Electrical engineer. Thinks in three phases", 18, t["soft"], SANS)
    c.text(60, 140, "and three dimensions.", 18, t["soft"], SANS)
    c.text(60, 560, f"MESH: {len(TRIS)} triangles · power transformer, tank + fins + bushings + conservator", 13, t["soft"], MONO)
    c.text(60, 584, "drag the real one below ↓  (GitHub renders it in 3D)", 13, t["hot"], MONO, 700)
    c.save(f"wireframe-{th}.svg", f"A rotating wireframe power transformer for {NAME}, electrical engineer who thinks in three phases and three dimensions.")

    # isometric stat blocks
    c = Canvas(F, t, 1200, 460)
    c.add(f'<rect width="1200" height="460" fill="{t["bg"]}"/>')
    stats = [("9", "apps live", 9), ("128", "tests", 12.8), ("30s", "was 30 min", 3), ("#7", "of 1500+", 7)]
    for i, (v, lab, h) in enumerate(stats):
        ox, oy, s = 180 + i * 280, 380, 26
        H = h * 16
        top = f"{ox},{oy - H - s} {ox + 2 * s},{oy - H} {ox},{oy - H + s} {ox - 2 * s},{oy - H}"
        left = f"{ox - 2 * s},{oy - H} {ox},{oy - H + s} {ox},{oy + s} {ox - 2 * s},{oy}"
        right = f"{ox + 2 * s},{oy - H} {ox},{oy - H + s} {ox},{oy + s} {ox + 2 * s},{oy}"
        c.add(f'<g class="rise" style="animation-delay:{i * .2:.1f}s;transform-origin:{ox}px {oy + s}px"><polygon points="{left}" fill="{t["left"]}"/><polygon points="{right}" fill="{t["right"]}"/><polygon points="{top}" fill="{t["top"]}"/></g>')
        c.text(ox, oy - H - s - 22, v, 40, t["ink"], SANS, 800, "middle")
        c.text(ox, oy + s + 40, lab, 16, t["soft"], SANS, 600, "middle")
    c.css.append(".rise{animation:rs 1.4s cubic-bezier(.2,.8,.2,1) backwards}@keyframes rs{from{transform:scaleY(0)}}")
    c.save(f"blocks-{th}.svg", "Isometric stat blocks: 9 apps live, 128 tests, 30 seconds that was 30 minutes, rank 7 of 1500+.")

links = " · ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- 3D: a power-transformer mesh as a spinning wireframe (light/dark) and as a real STL that GitHub renders in an interactive viewer. Built by scripts/gen_3d.py -->

<p align="center">{pic(F, "wireframe", f"Rotating wireframe transformer for {NAME}")}</p>

### 🧊 Spin it yourself

Drag to rotate, scroll to zoom. A {len(TRIS)}-triangle power transformer (tank, radiator fins, HV and LV bushings, conservator), generated in Python, because the person who wrote this tests real ones.

```stl
{stl()}
```

<p align="center">{pic(F, "blocks", "Isometric stat blocks")}</p>

<p align="center">{links}</p>
<p align="center"><sub><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}">linkedin</a></sub></p>
""")
print("ok", len(TRIS))
