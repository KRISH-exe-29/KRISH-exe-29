"""Dark-UI profile as a code editor: explorer, krishna.ts typing itself out, and a terminal running every project's tests.
Dark Modern for dark mode, Light Modern for light mode. Run: python scripts/gen_ide.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, SANS, MONO
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, CGPA, short
from xml.sax.saxutils import escape as esc

F = "ide"
THEMES = {
    "dark": dict(bg="#1F1F1F", side="#181818", bar="#181818", line="#2B2B2B", ink="#CCCCCC", soft="#8B8B8B", sel="#37373D", status="#0078D4", tab="#1F1F1F",
                 kw="#569CD6", st="#CE9178", pr="#9CDCFE", nu="#B5CEA8", cm="#6A9955", fn="#DCDCAA", ty="#4EC9B0", pu="#CCCCCC", ok="#73C991", term="#181818"),
    "light": dict(bg="#FFFFFF", side="#F8F8F8", bar="#F8F8F8", line="#E5E5E5", ink="#3B3B3B", soft="#868686", sel="#E4E6F1", status="#005FB8", tab="#FFFFFF",
                  kw="#0000FF", st="#A31515", pr="#001080", nu="#098658", cm="#008000", fn="#795E26", ty="#267F99", pu="#3B3B3B", ok="#388A34", term="#F8F8F8"),
}
CODE = [
    [("cm", "// krishna.ts: the only file that matters")],
    [("kw", "import"), ("pu", " { "), ("pr", "chai"), ("pu", " } "), ("kw", "from"), ("st", ' "./fuel"'), ("pu", ";")],
    [],
    [("kw", "export const "), ("pr", "krishna"), ("pu", ": "), ("ty", "Engineer"), ("pu", " = {")],
    [("pr", "  name"), ("pu", ": "), ("st", f'"{NAME}"'), ("pu", ",")],
    [("pr", "  base"), ("pu", ": "), ("st", '"Chennai, India"'), ("pu", ",")],
    [("pr", "  role"), ("pu", ": ["), ("st", '"Electrical Engineer"'), ("pu", ", "), ("st", '"Software Builder"'), ("pu", "],")],
    [("pr", "  degree"), ("pu", ": { "), ("pr", "college"), ("pu", ": "), ("st", '"St. Joseph\'s"'), ("pu", ", "), ("pr", "cgpa"), ("pu", ": "), ("nu", CGPA), ("pu", " },")],
    [("pr", "  shipped"), ("pu", ": "), ("nu", "9"), ("pu", ",           "), ("cm", "// apps in production")],
    [("pr", "  tests"), ("pu", ": "), ("nu", "128"), ("pu", ",           "), ("cm", "// guarding dispatch")],
    [("pr", "  patent"), ("pu", ": "), ("st", '"filed"'), ("pu", ",       "), ("cm", "// street lights that follow cars")],
    [("pr", "  nec"), ("pu", ": { "), ("pr", "rank"), ("pu", ": "), ("nu", "7"), ("pu", ", "), ("pr", "of"), ("pu", ": "), ("nu", "1500"), ("pu", " },")],
    [("pr", "  speaks"), ("pu", ": ["), ("st", '"ta"'), ("pu", ", "), ("st", '"en"'), ("pu", ", "), ("st", '"kn"'), ("pu", ", "), ("st", '"hi"'), ("pu", "],")],
    [("pr", "  fluentIn"), ("pu", ": ["), ("st", '"Ohm\'s Law"'), ("pu", ", "), ("st", '"Git"'), ("pu", "],")],
    [("pu", "};")],
    [],
    [("kw", "export function "), ("fn", "automate"), ("pu", "("), ("pr", "task"), ("pu", ": "), ("ty", "Task"), ("pu", "): "), ("ty", "Task"), ("pu", " {")],
    [("kw", "  if"), ("pu", " ("), ("pr", "task"), ("pu", "."), ("pr", "minutes"), ("pu", " > "), ("nu", "1"), ("pu", ") "), ("kw", "return "), ("fn", "rewrite"),
     ("pu", "("), ("pr", "task"), ("pu", ", { "), ("pr", "minutes"), ("pu", ": "), ("nu", "0.5"), ("pu", " });")],
    [("kw", "  return "), ("pr", "task"), ("pu", "; "), ("cm", "// already fast. leave it alone.")],
    [("pu", "}")],
]
EXT = {"Python": ".py", "Java": ".java", "C": ".c", "IoT": ".ino", "TypeScript": ".ts", "React": ".tsx"}

for th, t in THEMES.items():
    c = Canvas(F, t, 1200, 860)
    c.add(f'<rect width="1200" height="860" rx="12" fill="{t["bg"]}"/>')
    # title bar
    c.add(f'<rect width="1200" height="36" rx="12" fill="{t["bar"]}"/><rect y="24" width="1200" height="12" fill="{t["bar"]}"/>',
          "".join(f'<circle cx="{20 + i * 20}" cy="18" r="6" fill="{col}"/>' for i, col in enumerate(["#FF5F57", "#FEBC2E", "#28C840"])))
    c.add(f'<rect x="420" y="7" width="360" height="22" rx="6" fill="{t["bg"]}" stroke="{t["line"]}"/>')
    c.text(600, 23, "⌕  KRISH-exe-29", 12, t["soft"], SANS, anchor="middle")
    # activity bar + explorer
    c.add(f'<rect y="36" width="48" height="800" fill="{t["side"]}"/>')
    for i, g in enumerate(["⧉", "⌕", "⑂", "▷", "⊞"]):
        c.text(24, 74 + i * 48, g, 20, t["ink"] if i == 0 else t["soft"], SANS, anchor="middle")
    c.add(f'<rect x="48" y="36" width="250" height="800" fill="{t["side"]}"/><line x1="298" x2="298" y1="36" y2="836" stroke="{t["line"]}"/>')
    c.text(66, 62, "EXPLORER", 11, t["soft"], SANS, 600, extra='letter-spacing="1"')
    tree = [("⌄ KRISH-EXE-29", 0, True), ("⌄ src", 1, False), ("krishna.ts", 2, "sel"), ("fuel.ts", 2, False), ("⌄ projects", 1, False)]
    for slug, name, status, url, hook, impact, stack in PROJECTS:
        tree.append((slug + EXT.get(stack.split(" · ")[0], ".ts"), 2, status))
    tree += [("⌄ career", 1, False), ("railway → indo-tech.md", 2, False), ("README.md", 1, False)]
    for i, (name, depth, flag) in enumerate(tree):
        y = 88 + i * 24
        if flag == "sel":
            c.add(f'<rect x="48" y="{y - 16}" width="250" height="22" fill="{t["sel"]}"/>')
        dot = ""
        if isinstance(flag, str) and flag not in ("sel",):
            dot = {"PRODUCTION": t["ok"], "LIVE": t["ok"], "NEW": t["kw"]}.get(flag, "")
        c.text(62 + depth * 14, y, name, 13, t["ink"] if depth != 1 or name.startswith("README") else t["ink"], SANS, 600 if depth == 0 else 400)
        if dot:
            c.add(f'<circle cx="284" cy="{y - 4}" r="4" fill="{dot}"/>')
    # tabs
    c.add(f'<rect x="298" y="36" width="902" height="36" fill="{t["side"]}"/><rect x="298" y="36" width="150" height="36" fill="{t["tab"]}"/>'
          f'<rect x="298" y="36" width="150" height="2" fill="{t["status"]}"/>')
    c.text(316, 59, "TS  krishna.ts", 13, t["ink"], SANS)
    c.text(470, 59, "{ }  projects.json", 13, t["soft"], SANS)
    c.text(620, 59, "M↓  career.md", 13, t["soft"], SANS)
    c.text(316, 90, "src  ›  krishna.ts  ›  krishna", 12, t["soft"], SANS)
    # code with per-line typing reveal
    for i, toks in enumerate(CODE):
        y = 122 + i * 21
        c.text(330, y, str(i + 1), 13, t["soft"], MONO, anchor="end")
        if not toks:
            continue
        spans = "".join(f'<tspan fill="{t[k]}">{esc(s)}</tspan>' for k, s in toks)
        c.add(f'<g class="ln" style="animation-delay:{.2 + i * .14:.2f}s"><text x="350" y="{y}" font-family="{MONO}" font-size="14" xml:space="preserve">{spans}</text></g>')
    c.add(f'<rect class="cur" x="350" y="{122 + len(CODE) * 21 - 15}" width="8" height="18" fill="{t["ink"]}"/>')
    # minimap
    c.add(f'<rect x="1120" y="72" width="80" height="460" fill="{t["bg"]}"/>')
    for i, toks in enumerate(CODE):
        x = 1128
        for k, s in toks:
            w = len(s) * 1.6
            c.add(f'<rect x="{x:.0f}" y="{80 + i * 5}" width="{w:.0f}" height="2.5" fill="{t[k]}" opacity=".6"/>')
            x += w
    # terminal
    c.add(f'<rect x="298" y="540" width="902" height="296" fill="{t["term"]}"/><line x1="298" x2="1200" y1="540" y2="540" stroke="{t["line"]}"/>')
    for i, tab in enumerate(["PROBLEMS", "OUTPUT", "TERMINAL", "PORTS"]):
        c.text(320 + i * 100, 564, tab, 11, t["ink"] if tab == "TERMINAL" else t["soft"], SANS, 600)
    c.add(f'<rect x="520" y="570" width="66" height="2" fill="{t["status"]}"/>')
    c.text(320, 598, "krishna@indotech ~/KRISH-exe-29 $ npm test", 13, t["ink"], MONO)
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        y = 622 + i * 19
        c.add(f'<g class="ln" style="animation-delay:{3.3 + i * .22:.2f}s">'
              f'<text x="320" y="{y}" font-family="{MONO}" font-size="12.5" xml:space="preserve"><tspan fill="#FFFFFF" style="paint-order:stroke" stroke="{t["ok"]}" stroke-width="10"> PASS </tspan>'
              f'<tspan fill="{t["ink"]}">  {esc(slug + "/"):<18}</tspan><tspan fill="{t["soft"]}">{esc(impact)}</tspan></text></g>')
    c.add(f'<g class="ln" style="animation-delay:{3.3 + 10 * .22 + .2:.2f}s">'
          f'<text x="320" y="{622 + 10 * 19 + 4}" font-family="{MONO}" font-size="13" font-weight="700" fill="{t["ok"]}">Suites: 10 passed · Spreadsheets harmed: 0 · Chai remaining: 100%</text></g>')
    # status bar
    c.add(f'<rect y="836" width="1200" height="24" rx="0" fill="{t["status"]}"/>')
    c.text(12, 853, "⑂ main  ✓ 0 problems", 12, "#FFFFFF", SANS)
    c.text(1188, 853, "Ln 20, Col 2   UTF-8   TypeScript   ☕ chai: full   ⚡ shipping", 12, "#FFFFFF", SANS, anchor="end")
    c.css.append(".ln{animation:ln .25s steps(1) backwards}@keyframes ln{from{opacity:0}}"
                 ".cur{animation:cb 1s steps(1) infinite}@keyframes cb{50%{opacity:0}}")
    c.save(f"editor-{th}.svg", f"Code editor: krishna.ts describes {NAME}: electrical engineer and software builder in Chennai, 9 apps shipped, 128 tests, patent filed, "
                               f"NEC rank 7 of 1500, fluent in Ohm's Law and Git. The terminal shows all 10 project suites passing.")

links = " · ".join(f"[`{p[0]}`]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Dark-mode UI as a code editor (Dark Modern), with a Light Modern twin for light mode. Built by scripts/gen_ide.py -->

<p align="center">{pic(F, "editor", f"krishna.ts in a code editor, with every project's tests passing")}</p>

```bash
$ git clone https://github.com/KRISH-exe-29 && cd krishna
$ npm run hire   # → {EMAIL}
```

**Open a project:** {links}

<sub>⑂ main · ✓ 0 problems · [linkedin]({LINKEDIN}) · [email](mailto:{EMAIL})</sub>
""")
print("ok")
