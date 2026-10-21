"""AI / generative profile: a seeded flow field, a neural net that fires from inputs to shipped projects,
a latent-space map of the work, and a prompt that types itself. Run: python scripts/gen_generative.py"""
import hashlib, math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, SANS, MONO
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short
from xml.sax.saxutils import escape as esc

F = "generative"
SEED = int(hashlib.sha256(b"KRISH-exe-29").hexdigest()[:8], 16)
THEMES = {"dark": dict(bg="#06070C", ink="#ECEBFF", soft="#8C8AB3", a="#7C5CFF", b="#00D1FF", c="#FF5CA8", d="#FFC857", faint="#14162A"),
          "light": dict(bg="#FBFAFF", ink="#16142B", soft="#6E6A93", a="#6741D9", b="#0B8FD6", c="#D6336C", d="#E29A00", faint="#ECEAF8")}


def noise(x, y, s):
    """Cheap smooth pseudo-noise from layered sines; deterministic per seed."""
    r = random.Random(s)
    k = [(r.uniform(.002, .006), r.uniform(.002, .006), r.uniform(0, 6.28)) for _ in range(4)]
    return sum(math.sin(x * a + y * b + p) for a, b, p in k) / 4


for th, t in THEMES.items():
    rnd = random.Random(SEED)
    # 1. flow field portrait-banner
    c = Canvas(F, t, 1200, 560)
    c.add(f'<rect width="1200" height="560" fill="{t["bg"]}"/>')
    cols = [t["a"], t["b"], t["c"], t["d"]]
    paths = []
    for i in range(260):
        x, y = rnd.uniform(0, 1200), rnd.uniform(0, 560)
        pts = []
        for _ in range(60):
            ang = noise(x, y, SEED) * math.pi * 2
            x, y = x + 4 * math.cos(ang), y + 4 * math.sin(ang)
            pts.append(f"{x:.0f},{y:.0f}")
        col = cols[int((x / 1200) * 4) % 4]
        paths.append(f'<path class="fl" style="animation-delay:-{rnd.uniform(0, 8):.1f}s" d="M{" L".join(pts)}" fill="none" stroke="{col}" stroke-width="{rnd.uniform(.6, 2.2):.1f}" '
                     f'stroke-opacity="{rnd.uniform(.25, .8):.2f}" stroke-linecap="round"/>')
    c.add("".join(paths))
    c.add(f'<rect x="60" y="170" width="640" height="220" rx="16" fill="{t["bg"]}" fill-opacity=".82" stroke="{t["faint"]}"/>')
    c.text(90, 230, "seed: KRISH-exe-29", 15, t["soft"], MONO)
    c.text(88, 296, NAME, 56, t["ink"], SANS, 800, extra='letter-spacing="-2"')
    c.text(90, 344, "a generated profile. no two engineers render the same.", 18, t["soft"], SANS)
    c.css.append(".fl{stroke-dasharray:240;animation:fl 8s linear infinite}@keyframes fl{to{stroke-dashoffset:-480}}")
    c.save(f"field-{th}.svg", f"A flow field generated from the seed KRISH-exe-29 behind the name {NAME}: a generated profile, no two engineers render the same.")

    # 2. neural network
    c = Canvas(F, t, 1200, 600)
    c.add(f'<rect width="1200" height="600" fill="{t["bg"]}"/>')
    c.text(60, 60, "model.forward(krishna)", 22, t["ink"], MONO, 700)
    inputs = ["Ohm's Law", "Chai", "Curiosity", "Git", "Shop floor"]
    hidden = [6, 6]
    outs = [short(p[1]) for p in PROJECTS[:8]]
    layers = [inputs, [None] * hidden[0], [None] * hidden[1], outs]
    xs = [180, 450, 720, 990]
    pos = []
    for li, layer in enumerate(layers):
        n = len(layer)
        pos.append([(xs[li], 110 + (440 / (n - 1 if n > 1 else 1)) * k) for k in range(n)])
    edges = []
    for li in range(3):
        for i, a in enumerate(pos[li]):
            for j, b in enumerate(pos[li + 1]):
                w = rnd.random()
                if w < .55:
                    continue
                edges.append(f'<line class="syn" style="animation-delay:{li * .6 + rnd.uniform(0, .6):.2f}s" x1="{a[0]}" y1="{a[1]:.0f}" x2="{b[0]}" y2="{b[1]:.0f}" '
                             f'stroke="{cols[(i + j) % 4]}" stroke-width="{.6 + 2 * (w - .55):.1f}" stroke-opacity=".55"/>')
    c.add("".join(edges))
    for li, layer in enumerate(layers):
        for k, (x, y) in enumerate(pos[li]):
            c.add(f'<circle class="neu" style="animation-delay:{li * .6:.1f}s" cx="{x}" cy="{y:.0f}" r="{11 if li in (0, 3) else 8}" fill="{t["bg"]}" stroke="{cols[k % 4]}" stroke-width="3"/>')
            if li == 0:
                c.text(x - 22, y + 5, layer[k], 15, t["ink"], SANS, 600, "end")
            if li == 3:
                c.text(x + 22, y + 5, layer[k], 15, t["ink"], SANS, 600)
    c.text(990, 590, "output layer: shipped software", 13, t["soft"], MONO, anchor="middle")
    c.css.append(".syn{animation:sy 2.4s ease-in-out infinite}@keyframes sy{0%,100%{stroke-opacity:.15}40%{stroke-opacity:.9}}"
                 ".neu{animation:nu 2.4s ease-in-out infinite}@keyframes nu{40%{stroke-width:6}}")
    c.save(f"network-{th}.svg", "A neural network: inputs Ohm's Law, chai, curiosity, Git and the shop floor fire through two hidden layers into shipped projects.")

    # 3. latent space + prompt
    c = Canvas(F, t, 1200, 620)
    c.add(f'<rect width="1200" height="620" fill="{t["bg"]}"/><rect x="40" y="40" width="620" height="540" rx="16" fill="none" stroke="{t["faint"]}" stroke-width="2"/>')
    c.text(60, 76, "latent space · t-SNE of the work (hand-placed, vibes-accurate)", 14, t["soft"], MONO)
    clusters = {"factory ops": (230, 230, t["a"]), "people & HR": (500, 200, t["c"]), "hardware & IoT": (230, 450, t["d"]), "testing & data": (480, 440, t["b"])}
    member = {"dispatch": "factory ops", "rtcc": "factory ops", "kiosk-sentinel": "people & HR", "job-lens": "people & HR", "street-light": "hardware & IoT",
              "flood": "hardware & IoT", "hardware": "hardware & IoT", "test-planner": "testing & data", "industrial-data": "testing & data", "hwe-tool": "factory ops"}
    for name, (cx, cy, col) in clusters.items():
        c.add(f'<circle cx="{cx}" cy="{cy}" r="96" fill="{col}" opacity=".08"/>')
        c.text(cx, cy - 104, name, 13, col, MONO, 700, "middle")
        for _ in range(40):
            a, r = rnd.uniform(0, 6.28), abs(rnd.gauss(0, 34))
            c.add(f'<circle cx="{cx + r * math.cos(a):.0f}" cy="{cy + r * math.sin(a):.0f}" r="2" fill="{col}" opacity=".35"/>')
    for slug, name, *_ in PROJECTS:
        cl = member[slug]
        cx, cy, col = clusters[cl]
        mates = [p[0] for p in PROJECTS if member[p[0]] == cl]
        a = -math.pi / 2 + 2 * math.pi * mates.index(slug) / len(mates)  # spread cluster-mates evenly so labels never collide
        x, y = cx + 52 * math.cos(a) - 20, cy + 52 * math.sin(a)
        c.add(f'<circle class="pt" cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{col}"/>')
        c.text(x + 10, y + 4, short(name), 12, t["ink"], SANS, 700)
    # prompt box typing
    c.add(f'<rect x="700" y="40" width="460" height="540" rx="16" fill="{t["faint"]}"/>')
    c.text(724, 78, "prompt", 13, t["soft"], MONO)
    prompt = ["/imagine an electrical engineer", "who deletes busywork for a", "transformer factory, ships 9 apps,", "files a patent, and still has", "time for chai. --style shipped"]
    for i, l in enumerate(prompt):
        c.add(f'<g class="ty" style="animation-delay:{.3 + i * .5:.1f}s"><text x="724" y="{116 + i * 26}" font-family="{MONO}" font-size="15" fill="{t["ink"]}">{esc(l)}</text></g>')
    c.add(f'<line x1="724" x2="1136" y1="262" y2="262" stroke="{t["soft"]}" stroke-opacity=".4"/>')
    c.text(724, 296, "output", 13, t["soft"], MONO)
    outl = [("name", NAME), ("role", "electrical engineer · builder"), ("shipped", "9 apps in production"), ("tests", "128 on dispatch"),
            ("best trick", "30 min → 30 s"), ("rank", "#7 of 1500+ (NEC)"), ("tokens/s", "fast. chai-powered."), ("contact", EMAIL)]
    for i, (k, v) in enumerate(outl):
        c.add(f'<g class="ty" style="animation-delay:{3 + i * .25:.2f}s">'
              f'<text x="724" y="{330 + i * 30}" font-family="{MONO}" font-size="14" fill="{t["soft"]}">{esc(k)}:</text>'
              f'<text x="850" y="{330 + i * 30}" font-family="{MONO}" font-size="14" font-weight="700" fill="{cols[i % 4]}">{esc(v)}</text></g>')
    c.css.append(".ty{animation:ty .3s steps(1) backwards}@keyframes ty{from{opacity:0}}"
                 ".pt{animation:pt 2s ease-in-out infinite}@keyframes pt{50%{opacity:.5}}")
    c.save(f"latent-{th}.svg", "Latent space of the work in four clusters: factory ops, people and HR, hardware and IoT, testing and data. A prompt imagines an electrical engineer who deletes busywork; the output lists name, role, 9 apps shipped, 128 tests, 30 minutes to 30 seconds.")

links = " · ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- AI / generative: art seeded from the username, a firing neural net, a latent-space map and a self-typing prompt. Light and dark follow your GitHub theme. Built by scripts/gen_generative.py -->

<p align="center">{pic(F, "field", f"Generated flow field for {NAME}")}</p>
<p align="center">{pic(F, "network", "Neural network from inputs to shipped projects")}</p>
<p align="center">{pic(F, "latent", "Latent space of the work and a self-typing prompt")}</p>

```text
> sampling 10 projects at temperature 0 (deterministic, like the tests)
```

<p align="center">{links}</p>
<p align="center"><sub>seed = sha256("KRISH-exe-29") · <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}">linkedin</a></sub></p>
""")
print("ok")
