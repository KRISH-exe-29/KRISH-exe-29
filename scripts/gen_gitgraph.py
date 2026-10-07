"""Experimental profile: the whole life story laid out as a git commit graph. Career paths are branches that merge
into main, projects are feature branches, achievements are tags, HEAD points at hire-me. Run: python scripts/gen_gitgraph.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, SANS, MONO
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short

F = "gitgraph"
THEMES = {"dark": dict(bg="#0D1117", ink="#E6EDF3", soft="#7D8590", line="#21262D", lanes=["#F78166", "#3FB950", "#58A6FF", "#D2A8FF", "#E3B341", "#39C5CF"], tag="#E3B341"),
          "light": dict(bg="#FFFFFF", ink="#1F2328", soft="#656D76", line="#D0D7DE", lanes=["#CF222E", "#1A7F37", "#0969DA", "#8250DF", "#9A6700", "#1B7C83"], tag="#9A6700")}
# (lane, kind, hash, message, tag) — lane 0 is main; kind: c = commit, b = branch off main, m = merge into main
LOG = [
    (0, "c", "a1b2004", "init: born in Chennai", "v2004"),
    (0, "c", "e3e2022", f"feat: start B.E. Electrical & Electronics", None),
    (1, "b", "5r2023a", "railway: electrical documentation + inspection", None),
    (1, "c", "5r2023b", "railway: notice how much is still on paper", None),
    (0, "m", "m2023rr", "merge branch 'railway'", None),
    (2, "b", "p2024mt", "power-plant: megawatts up close at Mettur", None),
    (3, "b", "w2024ph", "web: ship Project Phantom (first production deploy)", None),
    (2, "c", "p2024ok", "power-plant: big machines, small clipboards", None),
    (0, "m", "m2024pp", "merge branch 'power-plant'", None),
    (0, "m", "m2024wb", "merge branch 'web'", None),
    (0, "c", "n2025rk", "feat: rank #7 of 1500+ at NEC, IIT Bombay", "v2025.02"),
    (4, "b", "b2025hw", "automation: MCC feeder classification tool at Bühler", None),
    (4, "c", "b2025fx", "perf: 30 minutes of paperwork → 30 seconds", None),
    (0, "m", "m2025au", "merge branch 'automation'", None),
    (0, "c", "pt2025s", "feat: patent filed, street lights that follow the car", "v2025.08"),
    (5, "b", "it2026a", "indotech: IEC 60076 testing, then software", None),
    (5, "c", "it2026b", "feat(dispatch): 5 roles, 128 tests, live", None),
    (5, "c", "it2026c", "feat(job-lens): rank 100 resumes offline", None),
    (5, "c", "it2026d", "feat(kiosk-sentinel): survive power cuts", None),
    (0, "m", "m2026it", "merge branch 'indotech' (9 apps in production)", "v2026"),
    (0, "c", "HEAD000", "HEAD → main · next: your project?", "hire-me"),
]
LANE_NAMES = ["main", "railway", "power-plant", "web", "automation", "indotech"]

for th, t in THEMES.items():
    rowh, x0, lw = 44, 70, 40
    H = 160 + len(LOG) * rowh + 40
    c = Canvas(F, t, 1200, H)
    c.add(f'<rect width="1200" height="{H}" fill="{t["bg"]}"/>')
    c.text(40, 54, "$ git log --graph --all --author=\"Krishna Raju S\"", 18, t["ink"], MONO, 700)
    c.text(40, 84, "every life event is a commit. every career path is a branch. everything merges into main.", 14, t["soft"], MONO)
    for i, n in enumerate(LANE_NAMES):
        c.add(f'<circle cx="{x0 + i * lw}" cy="122" r="5" fill="{t["lanes"][i]}"/>')
        c.text(x0 + i * lw, 110, n, 10, t["lanes"][i], MONO, 700, "middle", f'transform="rotate(-35 {x0 + i * lw} 110)"')
    y0 = 160
    # lane lines: each branch lives from its first commit to its merge
    spans = {}
    for i, (lane, kind, *_r) in enumerate(LOG):
        spans.setdefault(lane, [i, i])[1] = i
    for lane, (a, b) in spans.items():
        if lane == 0:
            c.add(f'<line x1="{x0}" x2="{x0}" y1="{y0}" y2="{y0 + (len(LOG) - 1) * rowh}" stroke="{t["lanes"][0]}" stroke-width="3"/>')
            continue
        merge = next(i for i in range(b + 1, len(LOG)) if LOG[i][1] == "m" and f"'{LANE_NAMES[lane]}'" in LOG[i][3])
        xa = x0 + lane * lw
        c.add(f'<path d="M{x0},{y0 + (a - 1) * rowh} C{x0},{y0 + a * rowh - 20} {xa},{y0 + (a - 1) * rowh + 20} {xa},{y0 + a * rowh}" fill="none" stroke="{t["lanes"][lane]}" stroke-width="3"/>'
              f'<line x1="{xa}" x2="{xa}" y1="{y0 + a * rowh}" y2="{y0 + b * rowh}" stroke="{t["lanes"][lane]}" stroke-width="3"/>'
              f'<path d="M{xa},{y0 + b * rowh} C{xa},{y0 + merge * rowh - 20} {x0},{y0 + b * rowh + 20} {x0},{y0 + merge * rowh}" fill="none" stroke="{t["lanes"][lane]}" stroke-width="3"/>')
    for i, (lane, kind, h, msg, tag) in enumerate(LOG):
        y = y0 + i * rowh
        x = x0 + lane * lw
        col = t["lanes"][lane]
        c.add(f'<g class="cm" style="animation-delay:{i * .18:.2f}s">')
        if kind == "m":
            c.add(f'<circle cx="{x}" cy="{y}" r="9" fill="{t["bg"]}" stroke="{col}" stroke-width="3"/>')
        else:
            c.add(f'<circle cx="{x}" cy="{y}" r="{9 if h == "HEAD000" else 7}" fill="{col}"/>')
        tx = 330
        c.text(tx, y + 5, h[:7], 14, t["tag"] if h == "HEAD000" else t["soft"], MONO, 700 if h == "HEAD000" else 400)
        mx = tx + 84
        if tag:
            w = len(tag) * 8.6 + 18
            c.add(f'<rect x="{mx}" y="{y - 12}" width="{w:.0f}" height="22" rx="11" fill="none" stroke="{t["tag"]}" stroke-width="1.5"/>')
            c.text(mx + w / 2, y + 4, tag, 12, t["tag"], MONO, 700, "middle")
            mx += w + 10
        c.text(mx, y + 5, msg, 15, t["ink"], MONO, 700 if kind == "m" or h == "HEAD000" else 400)
        c.add("</g>")
    c.add(f'<rect class="cur" x="330" y="{y0 + len(LOG) * rowh - 14}" width="9" height="18" fill="{t["ink"]}"/>')
    c.css.append(".cm{animation:cm .3s ease-out backwards}@keyframes cm{from{opacity:0;transform:translateX(-10px)}}"
                 ".cur{animation:cb 1s steps(1) infinite}@keyframes cb{50%{opacity:0}}")
    c.save(f"graph-{th}.svg", "Git graph of a life: " + "; ".join(f"{m}" for _, _, _, m, _ in LOG))

oneline = "\n".join(f"{'| ' * l}* {h[:7]} {('(tag: ' + tg + ') ') if tg else ''}{m}" for l, k, h, m, tg in reversed(LOG))
branches = "\n".join(f"  {('* ' if p[2] in ('PRODUCTION', 'LIVE') else '  ')}feature/{p[0]:<18} {p[4]}" for p in PROJECTS)
links = " · ".join(f"[`feature/{p[0]}`]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Experimental: the profile as a git commit graph. Light and dark follow your GitHub theme. Built by scripts/gen_gitgraph.py -->

<p align="center">{pic(F, "graph", f"A git graph of {NAME}'s life")}</p>

```console
$ git branch --list 'feature/*'
{branches}
```

```console
$ git log --oneline --decorate
{oneline}
```

```console
$ git checkout -b your-project
fatal: needs one more contributor. try: {EMAIL}
```

**Checkout a feature:** {links}

<sub>[linkedin]({LINKEDIN}) · no history was rewritten in the making of this README</sub>
""")
print("ok")
