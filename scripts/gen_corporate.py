"""Corporate / enterprise profile: an annual report. Cover, KPI board, before/after chart, and native Mermaid + tables.
Run: python scripts/gen_corporate.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, SANS, SERIF
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, CGPA, COLLEGE, short

F = "corporate"
THEMES = {"light": dict(bg="#FFFFFF", ink="#0B1F3A", soft="#5B6B82", line="#D9E1EC", navy="#0B2A5B", blue="#1F6FEB", teal="#0E9F8E", gold="#C9A227", card="#F5F8FC"),
          "dark": dict(bg="#0B1220", ink="#E8EEF7", soft="#93A3BA", line="#1E2A40", navy="#0F2547", blue="#4C8DFF", teal="#2BC4B0", gold="#E2BE4A", card="#111B2E")}

for th, t in THEMES.items():
    # cover
    c = Canvas(F, t, 1200, 560)
    c.add(f'<rect width="1200" height="560" fill="{t["navy"]}"/>',
          f'<path d="M760 0h440v560H560z" fill="{t["blue"]}" opacity=".55"/><path d="M960 0h240v560H860z" fill="{t["teal"]}" opacity=".6"/>',
          f'<rect x="60" y="60" width="8" height="120" fill="{t["gold"]}"/>')
    c.text(90, 90, "KRS HOLDINGS (A SUBSIDIARY OF ONE PERSON)", 14, "#C9D6EA", SANS, 700, extra='letter-spacing="3"')
    c.text(90, 150, "Annual Report", 64, "#FFFFFF", SERIF, 400)
    c.text(90, 200, "FY 2026", 40, t["gold"], SERIF, 400)
    c.text(90, 300, "Delivering operational excellence", 30, "#FFFFFF", SANS, 300)
    c.text(90, 340, "through relentless automation.", 30, "#FFFFFF", SANS, 300)
    c.text(90, 400, "Also: synergising Ohm's Law and Git since 2004.", 18, "#C9D6EA", SANS, 400, extra='font-style="italic"')
    c.text(90, 500, f"Prepared by {NAME} · Chief Everything Officer", 15, "#C9D6EA", SANS, 600, extra='letter-spacing="1"')
    c.add(f'<g class="up"><path d="M820 420 L900 360 L960 380 L1060 260 L1120 220" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<path d="M1092 214 L1124 218 L1114 248" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/></g>')
    c.css.append(".up path{stroke-dasharray:500;animation:dr 2.4s ease-out both}@keyframes dr{from{stroke-dashoffset:500}}")
    c.save(f"cover-{th}.svg", f"Annual Report FY 2026 by {NAME}, Chief Everything Officer: delivering operational excellence through relentless automation.")

    # KPI board
    c = Canvas(F, t, 1200, 600)
    c.add(f'<rect width="1200" height="600" fill="{t["bg"]}"/>')
    c.text(60, 64, "Financial highlights", 34, t["ink"], SERIF)
    c.text(60, 94, "Key performance indicators, fiscal year 2026. Unaudited, but extremely confident.", 15, t["soft"], SANS)
    kpis = [("Apps in production", "9", "▲ +9 since 2025", t["teal"]), ("Automated tests", "128", "▲ dispatch coverage", t["teal"]),
            ("Manual minutes per task", "0.5", "▼ from 30 (Bühler)", t["teal"]), ("National rank (NEC)", "#7", "of 1500+ colleges", t["gold"])]
    for i, (k, v, d, col) in enumerate(kpis):
        x = 60 + i * 276
        c.add(f'<rect x="{x}" y="120" width="260" height="140" rx="6" fill="{t["card"]}" stroke="{t["line"]}"/><rect x="{x}" y="120" width="4" height="140" fill="{col}"/>')
        c.text(x + 22, 152, k, 14, t["soft"], SANS, 600)
        c.text(x + 22, 208, v, 46, t["ink"], SANS, 700)
        c.text(x + 22, 240, d, 14, col, SANS, 700)
    # before/after chart
    c.add(f'<rect x="60" y="290" width="700" height="280" rx="6" fill="{t["card"]}" stroke="{t["line"]}"/>')
    c.text(84, 324, "Minutes per task, before vs after automation", 16, t["ink"], SANS, 700)
    rows = [("MCC documentation (Bühler)", 30, .5), ("Hardware list → BOM", 25, 1), ("Pending-point follow-ups", 20, 0), ("Test scheduling (per unit)", 15, 1)]
    for i, (lab, b, a) in enumerate(rows):
        y = 360 + i * 52
        c.text(84, y + 14, lab, 13, t["soft"], SANS, 600)
        c.add(f'<rect class="bb" style="animation-delay:{i * .15:.2f}s" x="330" y="{y}" width="{b * 12}" height="16" fill="{t["line"]}"/>'
              f'<rect class="bb" style="animation-delay:{.6 + i * .15:.2f}s" x="330" y="{y + 20}" width="{max(a * 12, 3)}" height="16" fill="{t["blue"]}"/>')
        c.text(330 + b * 12 + 8, y + 13, f"{b} min", 12, t["soft"], SANS)
        c.text(330 + max(a * 12, 3) + 8, y + 33, "auto" if a == 0 else f"{a:g} min", 12, t["blue"], SANS, 700)
    c.text(84, 562, "Sources: internship and plant records. Follow-ups and scheduling are estimates.", 11, t["soft"], SANS, extra='font-style="italic"')
    # donut of where the time goes
    import math
    c.add(f'<rect x="780" y="290" width="360" height="280" rx="6" fill="{t["card"]}" stroke="{t["line"]}"/>')
    c.text(804, 324, "Skills portfolio allocation", 16, t["ink"], SANS, 700)
    parts = [("Power engineering", 35, t["navy"] if th == "light" else t["blue"]), ("Software", 40, t["teal"]), ("IoT / embedded", 15, t["gold"]), ("Chai", 10, t["soft"])]
    a0, cx, cy, r = -90, 900, 450, 70
    for lab, pct, col in parts:
        a1 = a0 + pct * 3.6
        x1, y1 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x2, y2 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        c.add(f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 {1 if pct > 50 else 0} 1 {x2:.1f},{y2:.1f}" fill="none" stroke="{col}" stroke-width="26"/>')
        a0 = a1
    for i, (lab, pct, col) in enumerate(parts):
        c.add(f'<rect x="1000" y="{392 + i * 30}" width="12" height="12" fill="{col}"/>')
        c.text(1020, 403 + i * 30, f"{lab} {pct}%", 12, t["ink"], SANS, 600)
    c.css.append(".bb{transform-box:fill-box;transform-origin:left;animation:bx 1s ease-out backwards}@keyframes bx{from{transform:scaleX(0)}}")
    c.save(f"kpis-{th}.svg", "Highlights: 9 apps in production; 128 automated tests; manual minutes per task down from 30 to 0.5; national rank 7 of 1500+.")

rows = "\n".join(f"| {f'[{short(p[1])}]({p[3]})' if p[3] else short(p[1])} | {p[2].title()} | {p[4]} | {p[5]} |" for p in PROJECTS)
write_readme(f"""
<!-- Corporate / enterprise: an annual report. Images follow your GitHub theme; tables and the Mermaid chart are native GitHub. Built by scripts/gen_corporate.py -->

<p align="center">{pic(F, "cover", f"Annual Report FY 2026 by {NAME}")}</p>

<p align="center">
  <a href="mailto:{EMAIL}"><img src="https://img.shields.io/badge/Investor_relations-0B2A5B?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
  <a href="{LINKEDIN}"><img src="https://img.shields.io/badge/LinkedIn-1F6FEB?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
  <a href="https://krishna-ittl.github.io/Candidate-Screener/"><img src="https://img.shields.io/badge/Product_demo-0E9F8E?style=for-the-badge&logo=githubpages&logoColor=white" alt="Job Lens demo"/></a>
</p>

## 1. Letter to stakeholders

> Dear stakeholders,
>
> This year we moved from testing transformers to writing the software the plant runs on. Dispatch, testing, hiring and attendance are now digital, nine applications are in production, and a 30-minute documentation task now completes in 30 seconds. We remain committed to deleting boring work at scale.
>
> **{NAME}**, Chief Everything Officer

## 2. Highlights

<p align="center">{pic(F, "kpis", "KPI board")}</p>

## 3. Product portfolio

| Product | Status | Value proposition | Impact |
|:--|:--|:--|:--|
{rows}

## 4. Corporate history

```mermaid
gantt
    title Career timeline
    dateFormat YYYY-MM
    axisFormat %Y
    section Industry
    Southern Railway, electrical intern      :done, 2023-01, 1M
    Mettur Thermal Power Plant               :done, 2024-06, 2M
    Bühler India, automation HWE             :done, 2025-06, 1M
    Indo Tech Transformers                   :active, 2026-01, 10M
    section Software
    Inovate Technologies, full stack intern  :done, 2024-03, 3M
    section Recognition
    NEC rank 7 and E-Summit runner-up        :milestone, 2025-02, 0d
    Patent filed                             :milestone, 2025-08, 0d
```

## 5. Governance

| Board member | Role |
|:--|:--|
| Krishna Raju S | Chairman, CEO, CTO, intern |
| Chai | Independent director, never absent |
| {COLLEGE} | Founding investor (B.E. EEE, CGPA {CGPA}) |

## 6. Risk factors

- The company may automate the boring parts of your job. Shareholders have described this as a feature.
- Exposure to legacy spreadsheets remains high across the industry. Management considers this the growth market.
- Key-person risk: one engineer. Mitigated by documentation and 128 tests.

<sub>Forward-looking statements: more apps. Contact investor relations at {EMAIL}.</sub>
""")
print("ok")
