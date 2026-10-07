"""Aesthetic / art-driven profile: a museum exhibition. Each project becomes an abstract composition, framed and labelled.
Run: python scripts/gen_gallery.py"""
import hashlib, math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, wrap
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short

F = "gallery"
MUSEUM = "'Futura', 'Century Gothic', 'Gill Sans', 'Segoe UI', sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"
THEMES = {"light": dict(wall="#F1EEE8", floor="#C9BFAF", ink="#1E1E1E", soft="#6E6A62", frame="#1E1E1E", mat="#FAF8F4", light=0),
          "dark": dict(wall="#17181B", floor="#0E0E10", ink="#ECE8E1", soft="#8D8880", frame="#B8A27A", mat="#F4F1EA", light=1)}
PAL = ["#E63946", "#F4A261", "#2A9D8F", "#264653", "#E9C46A", "#1D3557", "#111111"]


def composition(x, y, w, h, key, big=False):
    """A deterministic Bauhaus/Kandinsky-style composition seeded by the project name."""
    r = random.Random(int(hashlib.md5(key.encode()).hexdigest()[:8], 16))
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#F4F1EA"/>']
    for _ in range(3 if not big else 5):
        cx, cy, rr = x + r.uniform(.2, .8) * w, y + r.uniform(.2, .8) * h, r.uniform(.12, .3) * min(w, h)
        out.append(f'<circle class="{"spin" if big else ""}" style="transform-origin:{cx:.0f}px {cy:.0f}px" cx="{cx:.0f}" cy="{cy:.0f}" r="{rr:.0f}" fill="{r.choice(PAL)}" opacity="{r.uniform(.75, .95):.2f}"/>')
    for _ in range(2 if not big else 4):
        x1, y1 = x + r.uniform(0, 1) * w, y + r.uniform(0, 1) * h
        out.append(f'<polygon points="{x1:.0f},{y1:.0f} {x1 + r.uniform(-.3, .3) * w:.0f},{y1 + r.uniform(.1, .3) * h:.0f} {x1 + r.uniform(.1, .3) * w:.0f},{y1 + r.uniform(-.2, .2) * h:.0f}" '
                   f'fill="{r.choice(PAL)}" opacity=".9"/>')
    for _ in range(4 if not big else 8):
        x1, y1 = x + r.uniform(0, 1) * w, y + r.uniform(0, 1) * h
        a = r.uniform(0, math.pi)
        L = r.uniform(.2, .6) * w
        out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x1 + L * math.cos(a):.0f}" y2="{y1 + L * math.sin(a):.0f}" stroke="#111" stroke-width="{r.uniform(1, 4):.1f}"/>')
    out.append(f'<rect x="{x + r.uniform(.1, .7) * w:.0f}" y="{y + r.uniform(.1, .7) * h:.0f}" width="{.18 * w:.0f}" height="{.08 * h:.0f}" fill="{r.choice(PAL)}"/>')
    return f'<clipPath id="cp{key[:6]}{w}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#cp{key[:6]}{w})">{"".join(out)}</g>'


def framed(c, t, x, y, w, h, key, big=False):
    fw = 14 if big else 9
    if t["light"]:
        c.add(f'<ellipse cx="{x + w / 2}" cy="{y - 30}" rx="{w * .7:.0f}" ry="{h * .9:.0f}" fill="url(#spot)"/>')
    c.add(f'<rect x="{x - fw}" y="{y - fw}" width="{w + 2 * fw}" height="{h + 2 * fw}" fill="{t["frame"]}" style="filter:drop-shadow(0 10px 14px rgba(0,0,0,.35))"/>'
          f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{t["mat"]}"/>')
    pad = 18 if big else 12
    c.add(composition(x + pad, y + pad, w - 2 * pad, h - 2 * pad, key, big))


for th, t in THEMES.items():
    spot = ('<radialGradient id="spot" cx=".5" cy=".3" r=".6"><stop offset="0" stop-color="#FFF4D6" stop-opacity=".22"/><stop offset="1" stop-color="#FFF4D6" stop-opacity="0"/></radialGradient>')
    c = Canvas(F, t, 1200, 720)
    c.defs.append(spot)
    c.add(f'<rect width="1200" height="720" fill="{t["wall"]}"/><rect y="640" width="1200" height="80" fill="{t["floor"]}"/>')
    c.text(60, 80, "KRISHNA RAJU S", 40, t["ink"], MUSEUM, 700, extra='letter-spacing="6"')
    c.text(60, 116, "SELECTED WORKS, 2023–2026", 16, t["soft"], MUSEUM, 400, extra='letter-spacing="5"')
    c.text(60, 146, "Gallery 1 · Engineering as an art form", 15, t["soft"], SERIF, extra='font-style="italic"')
    framed(c, t, 140, 200, 420, 380, "Composition No. 9", True)
    # placard
    c.add(f'<rect x="640" y="300" width="400" height="230" fill="{t["mat"]}" stroke="{t["soft"]}" stroke-opacity=".4"/>')
    c.text(664, 340, NAME, 18, "#1E1E1E", MUSEUM, 700)
    c.text(664, 362, "b. 2004, Chennai", 14, "#55524C", SERIF)
    c.text(664, 400, "Composition No. 9 (Nine Apps)", 18, "#1E1E1E", SERIF, 700, extra='font-style="italic"')
    c.text(664, 422, "2026", 14, "#55524C", SERIF)
    for i, l in enumerate(wrap("React, Python, Java and 128 tests on a working factory floor. On permanent loan to Indo Tech Transformers.", 14, 350, .5)):
        c.text(664, 452 + i * 20, l, 14, "#55524C", SERIF)
    c.text(664, 516, "Patent filed · NEC #7 of 1500+", 12, "#8A857C", MUSEUM, 700, extra='letter-spacing="1.5"')
    c.add(f'<rect x="1080" y="560" width="60" height="80" fill="none" stroke="{t["soft"]}" stroke-opacity=".5"/><line x1="1080" x2="1140" y1="600" y2="600" stroke="{t["soft"]}" stroke-opacity=".5"/>')
    c.text(1110, 594, "EXIT", 10, t["soft"], MUSEUM, 700, "middle", 'letter-spacing="2"')
    c.css.append(".spin{animation:sp 30s linear infinite}@keyframes sp{to{transform:rotate(360deg)}}")
    c.save(f"hall-{th}.svg", f"Museum hall: {NAME}, selected works 2023 to 2026. Featured: Composition No. 9 (Nine Apps), 2026, on permanent loan to Indo Tech Transformers.")

    # salon hang of the ten works
    c = Canvas(F, t, 1200, 860)
    c.defs.append(spot)
    c.add(f'<rect width="1200" height="860" fill="{t["wall"]}"/><rect y="800" width="1200" height="60" fill="{t["floor"]}"/>')
    c.text(600, 60, "GALLERY 2 · THE PERMANENT COLLECTION", 18, t["ink"], MUSEUM, 700, "middle", 'letter-spacing="5"')
    sizes = [(200, 240), (240, 180), (180, 180), (220, 260), (200, 200), (240, 200), (180, 240), (220, 180), (200, 220), (220, 200)]
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        w, h = sizes[i]
        x = 60 + (i % 5) * 224 + (204 - w) / 2 + 10
        y = 110 + (i // 5) * 360 + (260 - h) / 2
        framed(c, t, x, y, w * .85, h * .85, name)
        px, py = 60 + (i % 5) * 224 + 10, 110 + (i // 5) * 360 + 270
        c.add(f'<rect x="{px}" y="{py}" width="200" height="66" fill="{t["mat"]}"/>')
        c.text(px + 10, py + 22, short(name), 14, "#1E1E1E", SERIF, 700, extra='font-style="italic"')
        c.text(px + 10, py + 40, f"{stack.split(' · ')[0]} · {status.lower()}", 11, "#55524C", MUSEUM)
        c.text(px + 10, py + 56, hook[:34] + ("…" if len(hook) > 34 else ""), 10, "#8A857C", SERIF)
    c.save(f"salon-{th}.svg", "The permanent collection: " + "; ".join(f"{p[1]}, {p[4]}" for p in PROJECTS))

links = " · ".join(f"[*{short(p[1])}*]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Aesthetic / art-driven: a museum exhibition of the work. Daylight gallery and after-hours spotlights follow your GitHub theme. Built by scripts/gen_gallery.py -->

<p align="center">{pic(F, "hall", f"Museum hall: {NAME}, selected works")}</p>
<p align="center">{pic(F, "salon", "The permanent collection")}</p>

> *"Every composition here was generated from the name of a project. The shapes are art. The software underneath is not: it runs on a factory floor every shift."*
> — exhibition notes

<p align="center">{links}</p>
<p align="center"><sub>Private viewings: <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}">linkedin</a></sub></p>
""")
print("ok")
