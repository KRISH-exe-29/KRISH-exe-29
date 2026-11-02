"""Immersive / visual storytelling profile: six cinematic chapters with animated scenes, and an interactive map of the
journey (GitHub renders ```geojson blocks as maps). Run: python scripts/gen_story.py"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short

F = "story"
SERIF = "Georgia, 'Iowan Old Style', 'Times New Roman', serif"
SANS = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
THEMES = {"dark": dict(sky="#0B1026", ground="#141A2E", ink="#F1EEE6", soft="#9AA3BF", acc="#FFB84D", line="#2A3352"),
          "light": dict(sky="#FDF3E3", ground="#EADBC4", ink="#1E1B16", soft="#6E6556", acc="#D9480F", line="#D8C8AE")}
CHAPTERS = [
    ("I", "2023 · Chennai", "The railway", "It started on the railways. I inspected electrical systems and filled in a lot of paper. That is when I started counting the minutes.", "train"),
    ("II", "2024 · Mettur", "The power plant", "At a thermal power plant I saw megawatts up close. Enormous machines. Tiny clipboards. Something did not add up.", "plant"),
    ("III", "2024 · Chennai", "The first deploy", "Then I wrote production code for the first time. Project Phantom shipped. The terminal turned green and something clicked.", "code"),
    ("IV", "Feb 2025 · IIT Bombay", "The stage", "Rank #7 of 1500+ colleges at the National Entrepreneurship Challenge, runner-up at Fish Tank. And a patent filed that summer.", "trophy"),
    ("V", "Jun 2025 · Bengaluru", "Thirty seconds", "At Bühler, MCC paperwork took thirty minutes. I wrote a tool over a few evenings. It took thirty seconds.", "clock"),
    ("VI", "2026 · Kanchipuram", "The plant runs on it", "Now I test transformers and write the software the plant runs on. Nine apps. Every shift. To be continued.", "factory"),
]


def scene(kind, t):
    a, ink, soft = t["acc"], t["ink"], t["soft"]
    if kind == "train":
        cars = "".join(f'<rect x="{i * 130}" y="250" width="120" height="60" rx="8" fill="{soft}"/><circle cx="{i * 130 + 28}" cy="314" r="10" fill="{ink}"/><circle cx="{i * 130 + 92}" cy="314" r="10" fill="{ink}"/>'
                       + "".join(f'<rect x="{i * 130 + 12 + k * 26}" y="262" width="18" height="18" fill="{a}"/>' for k in range(4)) for i in range(4))
        return f'<line x1="0" x2="760" y1="326" y2="326" stroke="{ink}" stroke-width="4"/><g class="move">{cars}</g>'
    if kind == "plant":
        return (f'<path d="M80 330 Q110 180 140 120 L220 120 Q250 180 280 330Z" fill="{soft}"/><path d="M320 330 Q350 200 380 150 L440 150 Q470 200 500 330Z" fill="{soft}"/>'
                + "".join(f'<circle class="puff" style="animation-delay:{k * .7}s" cx="{180 + (k % 2) * 230}" cy="{100 - k * 6}" r="{22 + k * 4}" fill="{ink}" opacity=".18"/>' for k in range(4))
                + f'<g class="spin" style="transform-origin:640px 230px"><path d="M640 230 L640 140 M640 230 L718 275 M640 230 L562 275" stroke="{a}" stroke-width="10" stroke-linecap="round"/></g>'
                  f'<line x1="640" x2="640" y1="230" y2="330" stroke="{ink}" stroke-width="6"/>')
    if kind == "code":
        lines = "".join(f'<rect class="type" style="animation-delay:{k * .35:.2f}s" x="{150 + (k % 3) * 20}" y="{150 + k * 26}" width="{[260, 180, 300, 220, 140, 250][k]}" height="10" rx="5" fill="{[a, soft, ink, soft, a, ink][k]}"/>' for k in range(6))
        return (f'<rect x="120" y="110" width="520" height="230" rx="14" fill="none" stroke="{ink}" stroke-width="4"/>{lines}'
                f'<rect class="ok" x="470" y="300" width="150" height="28" rx="14" fill="#2BB673"/><text class="ok" x="545" y="320" font-family="{SANS}" font-size="15" font-weight="700" fill="#fff" text-anchor="middle">✓ deployed</text>')
    if kind == "trophy":
        return (f'<path d="M300 120 h160 v60 a80 80 0 0 1 -160 0z" fill="{a}"/><rect x="360" y="260" width="40" height="40" fill="{a}"/><rect x="320" y="300" width="120" height="24" fill="{ink}"/>'
                f'<path d="M300 140 h-40 a40 40 0 0 0 40 60 M460 140 h40 a40 40 0 0 1 -40 60" fill="none" stroke="{a}" stroke-width="8"/>'
                f'<text x="380" y="200" font-family="{SERIF}" font-size="40" font-weight="700" fill="{t["sky"]}" text-anchor="middle">7</text>'
                + "".join(f'<path class="spark" style="animation-delay:{k * .4}s;transform-origin:{x}px {y}px" d="M{x},{y - 14} l4,10 10,4 -10,4 -4,10 -4,-10 -10,-4 10,-4z" fill="{a}"/>' for k, (x, y) in enumerate([(240, 110), (540, 150), (520, 280)])))
    if kind == "clock":
        return (f'<circle cx="380" cy="220" r="110" fill="none" stroke="{ink}" stroke-width="8"/>'
                + "".join(f'<line x1="{380 + 92 * math.cos(math.radians(k * 30)):.0f}" y1="{220 + 92 * math.sin(math.radians(k * 30)):.0f}" x2="{380 + 104 * math.cos(math.radians(k * 30)):.0f}" y2="{220 + 104 * math.sin(math.radians(k * 30)):.0f}" stroke="{ink}" stroke-width="4"/>' for k in range(12))
                + f'<g class="fast" style="transform-origin:380px 220px"><line x1="380" y1="220" x2="380" y2="134" stroke="{a}" stroke-width="7" stroke-linecap="round"/></g>'
                  f'<line x1="380" y1="220" x2="440" y2="220" stroke="{ink}" stroke-width="7" stroke-linecap="round"/><circle cx="380" cy="220" r="10" fill="{a}"/>'
                  f'<text x="560" y="180" font-family="{SERIF}" font-size="36" fill="{soft}" text-decoration="line-through">30 min</text>'
                  f'<text x="560" y="240" font-family="{SERIF}" font-size="44" font-weight="700" fill="{a}">30 s</text>')
    # factory
    wins = "".join(f'<rect class="win" style="animation-delay:{(k * 37 % 20) / 10:.1f}s" x="{140 + (k % 8) * 56}" y="{200 + (k // 8) * 44}" width="30" height="24" fill="{a}"/>' for k in range(16))
    return (f'<path d="M110 330 V180 L190 140 V180 L270 140 V180 L350 140 V180 L430 140 V180 L560 120 V330Z" fill="{soft}"/>{wins}'
            f'<rect x="600" y="160" width="40" height="170" fill="{soft}"/><g class="truck"><rect x="640" y="290" width="70" height="36" fill="{ink}"/><rect x="710" y="300" width="30" height="26" fill="{ink}"/></g>')


CSS = (".move{animation:mv 5s linear infinite}@keyframes mv{from{transform:translateX(-560px)}to{transform:translateX(780px)}}"
       ".puff{animation:pf 3s ease-out infinite}@keyframes pf{to{transform:translateY(-50px) scale(1.6);opacity:0}}"
       ".spin{animation:sp 3s linear infinite}@keyframes sp{to{transform:rotate(360deg)}}"
       ".type{transform-box:fill-box;transform-origin:left;animation:ty 4s ease-out infinite}@keyframes ty{0%{transform:scaleX(0)}30%,100%{transform:scaleX(1)}}"
       ".ok{animation:ok 4s steps(1) infinite}@keyframes ok{0%,55%{opacity:0}56%,100%{opacity:1}}"
       ".spark{animation:sk 1.4s ease-in-out infinite}@keyframes sk{50%{transform:scale(.3)}}"
       ".fast{animation:sp .8s linear infinite}"
       ".win{animation:wn 2s steps(1) infinite}@keyframes wn{50%{opacity:.25}}"
       ".truck{animation:tk 4s linear infinite}@keyframes tk{from{transform:translateX(0)}to{transform:translateX(460px)}}")

for th, t in THEMES.items():
    for i, (num, when, title, text, kind) in enumerate(CHAPTERS):
        c = Canvas(F, t, 1200, 440)
        c.add(f'<rect width="1200" height="440" fill="{t["sky"]}"/><rect y="330" width="1200" height="110" fill="{t["ground"]}"/>')
        c.add(f'<g transform="translate({20 if i % 2 == 0 else 420} 0)">{scene(kind, t)}</g>')
        tx = 820 if i % 2 == 0 else 60
        c.add(f'<rect x="{tx - 20}" y="70" width="380" height="255" fill="{t["sky"]}" opacity=".88"/>')
        c.text(tx, 110, f"CHAPTER {num}", 14, t["acc"], SANS, 700, extra='letter-spacing="4"')
        c.text(tx, 136, when, 14, t["soft"], SANS, 600)
        c.text(tx, 182, title, 34, t["ink"], SERIF, 700)
        c.para(tx, 222, text, 17, 340, lh=1.5, fill=t["ink"], font=SERIF)
        c.add('<rect width="1200" height="36" fill="#000"/><rect y="404" width="1200" height="36" fill="#000"/>')
        c.css.append(CSS)
        c.save(f"ch{i + 1}-{th}.svg", f"Chapter {num}, {when}: {title}. {text}")

stops = [("Southern Railway", "Chennai", 80.2707, 13.0827, "2023 · where it started"), ("Mettur Thermal Power Plant", "Mettur", 77.8000, 11.7863, "2024 · megawatts up close"),
         ("Inovate Technologies", "Chennai", 80.2209, 13.0569, "2024 · first production deploy"), ("IIT Bombay · NEC & E-Summit", "Mumbai", 72.9133, 19.1334, "Feb 2025 · rank #7, runner-up"),
         ("Bühler India", "Bengaluru", 77.5946, 12.9716, "Jun 2025 · 30 min → 30 s"), ("Indo Tech Transformers", "Kanchipuram", 79.7036, 12.8342, "2026 · the plant runs on it")]
geo = {"type": "FeatureCollection", "features":
       [{"type": "Feature", "properties": {"name": "The journey", "stroke": "#D9480F", "stroke-width": 3},
         "geometry": {"type": "LineString", "coordinates": [[lon, lat] for _, _, lon, lat, _ in stops]}}]
       + [{"type": "Feature", "properties": {"name": n, "city": city, "chapter": note, "marker-color": "#D9480F"},
           "geometry": {"type": "Point", "coordinates": [lon, lat]}} for n, city, lon, lat, note in stops]}
chapters = "\n\n".join(f'<p align="center">{pic(F, f"ch{i + 1}", f"Chapter {c[0]}: {c[2]}")}</p>' for i, c in enumerate(CHAPTERS))
links = " · ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Immersive / visual storytelling: six animated chapters and an interactive journey map (GeoJSON). Night and day follow your GitHub theme. Built by scripts/gen_story.py -->

<h1 align="center">The engineer who counted minutes</h1>
<p align="center"><i>a true story in six chapters · by {NAME}</i></p>

{chapters}

### 🗺️ Follow the route

Pan and zoom: every pin is a chapter.

```geojson
{json.dumps(geo, indent=1, ensure_ascii=False)}
```

### Epilogue

The apps in chapter VI, for the curious: {links}

<p align="center"><b>Chapter VII is unwritten.</b> Maybe you're in it: <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}">LinkedIn</a></p>
""")
print("ok")
