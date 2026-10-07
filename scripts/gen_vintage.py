"""Retro / vintage profile: a 1950s magazine advertisement, a product catalogue and a clip-and-mail coupon.
Run: python scripts/gen_vintage.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, icon, pic, write_readme, wrap
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short

F = "vintage"
SLAB = "'Rockwell', 'Rockwell Extra Bold', 'Courier New', serif"
SCRIPT = "'Brush Script MT', 'Lucida Handwriting', cursive"
SERIF = "'Century Schoolbook', 'Georgia', serif"
THEMES = {"light": dict(paper="#F4E9D2", ink="#2B1D14", red="#C8402E", teal="#2E7D7A", mustard="#E0A526", soft="#7A6650"),
          "dark": dict(paper="#2A2018", ink="#F4E9D2", red="#E8634F", teal="#57B3AE", mustard="#F0BE4A", soft="#BFAE92")}


def burst(cx, cy, r1, r2, n=18):
    pts = " ".join(f"{cx + (r1 if i % 2 else r2) * math.cos(math.pi * i / n):.1f},{cy + (r1 if i % 2 else r2) * math.sin(math.pi * i / n):.1f}" for i in range(2 * n))
    return pts


def texture(c, t, w, h):
    c.defs.append('<filter id="age"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="3" seed="9"/>'
                  '<feColorMatrix values="0 0 0 0 .3  0 0 0 0 .2  0 0 0 0 .1  0 0 0 .12 0"/><feComposite in2="SourceAlpha" operator="in"/></filter>'
                  f'<pattern id="dots" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="1.6" fill="{t["red"]}" opacity=".35"/></pattern>')
    c.add(f'<rect width="{w}" height="{h}" fill="{t["paper"]}"/><rect width="{w}" height="{h}" fill="#000" filter="url(#age)"/>')


for th, t in THEMES.items():
    c = Canvas(F, t, 1200, 900)
    texture(c, t, 1200, 900)
    c.add(f'<rect x="24" y="24" width="1152" height="852" fill="none" stroke="{t["ink"]}" stroke-width="4"/><rect x="34" y="34" width="1132" height="832" fill="none" stroke="{t["ink"]}" stroke-width="1.5"/>')
    c.text(600, 96, "AMAZING!", 30, t["red"], SLAB, 700, "middle", 'letter-spacing="10"')
    c.text(600, 170, "The KRISHNA", 76, t["ink"], SLAB, 700, "middle")
    c.text(600, 236, "Automatic Paperwork Eliminator", 50, t["ink"], SCRIPT, 400, "middle")
    c.add(f'<rect x="120" y="262" width="960" height="6" fill="{t["red"]}"/><rect x="120" y="274" width="960" height="2" fill="{t["red"]}"/>')
    # product illustration: a transformer with radiating lines
    c.add(f'<rect x="120" y="310" width="440" height="440" fill="url(#dots)"/>')
    c.add("".join(f'<line class="ray" style="animation-delay:{i * .1:.1f}s" x1="340" y1="530" x2="{340 + 230 * math.cos(math.radians(i * 20)):.0f}" y2="{530 + 230 * math.sin(math.radians(i * 20)):.0f}" stroke="{t["mustard"]}" stroke-width="5"/>' for i in range(18)))
    c.add(f'<rect x="260" y="470" width="160" height="170" rx="8" fill="{t["teal"]}" stroke="{t["ink"]}" stroke-width="4"/>'
          + "".join(f'<rect x="{428 + i * 14}" y="490" width="9" height="130" fill="{t["teal"]}" stroke="{t["ink"]}" stroke-width="2"/>' for i in range(3))
          + "".join(f'<rect x="{282 + i * 48}" y="{422 if i != 1 else 408}" width="20" height="{48 if i != 1 else 62}" fill="{t["paper"]}" stroke="{t["ink"]}" stroke-width="3"/>' for i in range(3))
          + f'<path d="M335 520l-22 42h20l-10 38 34-50h-22l12-30z" fill="{t["mustard"]}" stroke="{t["ink"]}" stroke-width="2"/>')
    c.add(f'<g class="spin" style="transform-origin:470px 360px"><polygon points="{burst(470, 360, 70, 92)}" fill="{t["red"]}"/></g>')
    c.text(470, 352, "98%", 34, t["paper"], SLAB, 700, "middle")
    c.text(470, 380, "LESS WAITING", 13, t["paper"], SLAB, 700, "middle")
    # copy column
    y = 340
    for line, size, col, font in [("Is paperwork eating", 34, t["ink"], SLAB), ("your afternoon?", 34, t["ink"], SLAB), ("", 10, t["ink"], SERIF)]:
        c.text(620, y, line, size, col, font, 700)
        y += size + 10
    body = ("Modern engineers agree: thirty minutes of manual entry is thirty minutes too many. "
            "The KRISHNA, invented in Chennai and tested on a real transformer plant, turns that chore into thirty seconds. "
            "Dispatch, testing, hiring and attendance, all automated.")
    y = c.para(620, y, body, 19, 520, fill=t["ink"], font=SERIF)
    feats = ["✓ Nine models now in production", "✓ 128 tests guard every shipment", "✓ Patent filed (street lights that follow cars!)", "✓ Ranked #7 of 1500+ colleges"]
    for i, f in enumerate(feats):
        c.text(620, y + 24 + i * 32, f, 20, t["teal"], SLAB, 700)
    c.text(620, y + 170, "Ask your plant manager today!", 30, t["red"], SCRIPT, 400)
    c.text(600, 850, "A FINE PRODUCT OF KRS ELECTRIC WORKS · CHENNAI, INDIA · EST. 2004", 14, t["soft"], SLAB, 700, "middle", 'letter-spacing="2"')
    c.css.append(".spin{animation:sp 20s linear infinite}@keyframes sp{to{transform:rotate(360deg)}}"
                 ".ray{animation:ry 2s ease-in-out infinite}@keyframes ry{50%{opacity:.3}}")
    c.save(f"ad-{th}.svg", f"Vintage ad: Amazing! The KRISHNA Automatic Paperwork Eliminator. 98% less waiting. Nine models in production, 128 tests, patent filed, ranked 7 of 1500+. Ask your plant manager today!")

    # catalogue
    c = Canvas(F, t, 1200, 760)
    texture(c, t, 1200, 760)
    c.text(600, 80, "The 2026 Catalogue", 44, t["ink"], SCRIPT, 400, "middle")
    c.text(600, 112, "TEN FINE PRODUCTS · EACH ONE GUARANTEED TO SAVE YOU TIME", 14, t["soft"], SLAB, 700, "middle", 'letter-spacing="2"')
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        x, y = 50 + (i % 5) * 222, 140 + (i // 5) * 300
        c.add(f'<rect x="{x}" y="{y}" width="208" height="280" fill="none" stroke="{t["ink"]}" stroke-width="2"/><rect x="{x + 6}" y="{y + 6}" width="196" height="268" fill="none" stroke="{t["ink"]}" stroke-width=".8"/>')
        c.add(f'<circle cx="{x + 104}" cy="{y + 70}" r="44" fill="{[t["teal"], t["red"], t["mustard"]][i % 3]}" opacity=".9"/>' + icon(slug, x + 74, y + 40, 60, t["paper"], t["ink"], t["ink"]))
        c.text(x + 104, y + 146, f"No. {i + 1}", 13, t["soft"], SLAB, 700, "middle")
        nm = wrap(short(name), 18, 190, .55)
        for j, l in enumerate(nm[:2]):
            c.text(x + 104, y + 170 + j * 22, l, 18, t["ink"], SLAB, 700, "middle")
        hy = y + 176 + len(nm[:2]) * 22
        for j, l in enumerate(wrap(hook, 13, 186, .5)[:3]):
            c.text(x + 104, hy + j * 17, l, 13, t["ink"], SERIF, anchor="middle", extra='font-style="italic"')
        c.text(x + 104, y + 264, "₹0 · satisfaction guaranteed" if url else "by appointment only", 11, t["red"], SLAB, 700, "middle")
    c.save(f"catalogue-{th}.svg", "Catalogue of ten products: " + "; ".join(f"No. {i + 1} {p[1]}, {p[4]}" for i, p in enumerate(PROJECTS)))

    # coupon
    c = Canvas(F, t, 1200, 320)
    texture(c, t, 1200, 320)
    c.add(f'<rect x="60" y="40" width="1080" height="240" fill="none" stroke="{t["ink"]}" stroke-width="3" stroke-dasharray="14 8"/>')
    c.text(70, 36, "✂", 28, t["ink"], SERIF)
    c.text(600, 100, "CLIP & MAIL TODAY", 34, t["red"], SLAB, 700, "middle", 'letter-spacing="4"')
    c.text(600, 140, "Yes! Please send one engineer to delete my most boring process.", 20, t["ink"], SERIF, anchor="middle", extra='font-style="italic"')
    c.text(200, 196, "NAME ______________________", 18, t["ink"], SLAB, 700)
    c.text(660, 196, "PROCESS ____________________", 18, t["ink"], SLAB, 700)
    c.text(600, 252, f"Mail to: {EMAIL}", 22, t["teal"], SLAB, 700, "middle")
    c.save(f"coupon-{th}.svg", f"Clip and mail today: please send one engineer to delete my most boring process. Mail to {EMAIL}")

links = " · ".join(f"[No. {i + 1} {short(p[1])}]({p[3]})" for i, p in enumerate(PROJECTS) if p[3])
write_readme(f"""
<!-- Retro / vintage: a 1950s magazine ad on aged paper. Daylight print and an after-dark edition follow your GitHub theme. Built by scripts/gen_vintage.py -->

<p align="center">{pic(F, "ad", "Vintage advertisement for the KRISHNA Automatic Paperwork Eliminator")}</p>
<p align="center">{pic(F, "catalogue", "The catalogue of ten products")}</p>
<p align="center"><sub>{links}</sub></p>
<p align="center"><a href="mailto:{EMAIL}">{pic(F, "coupon", "Clip and mail coupon")}</a></p>
<p align="center"><sub><a href="{LINKEDIN}">also available by telegram (LinkedIn)</a></sub></p>
""")
print("ok")
