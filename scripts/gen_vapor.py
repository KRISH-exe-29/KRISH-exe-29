"""Vaporwave profile: pink-teal haze, palm silhouettes, a 3D grid, Windows-95 dialogs, a pixel portrait in a .bmp window.
Run: python scripts/gen_vapor.py [photo]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme, photo_grid
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short

F = "vapor"
W95 = "'MS Sans Serif', 'Microsoft Sans Serif', Tahoma, 'Segoe UI', sans-serif"
SERIF = "'Times New Roman', Times, serif"
JP = "'Yu Gothic', 'Hiragino Kaku Gothic Pro', 'MS Gothic', 'Noto Sans JP', sans-serif"
THEMES = {"light": dict(sky1="#FFD3F0", sky2="#B8F3FF", sun1="#FFF59D", sun2="#FF71CE", grid="#B967FF", floor="#FBE6FF", ink="#3D1A5B", palm="#7A3FB0"),
          "dark": dict(sky1="#1A0B3B", sky2="#FF71CE", sun1="#FFFB96", sun2="#FF2E97", grid="#01CDFE", floor="#120428", ink="#FFFFFF", palm="#0B0420")}
photo = photo_grid(F, 40, sys.argv[1] if len(sys.argv) > 1 else None)


def win(c, x, y, w, h, title, active=True):
    """A Windows-95 window frame with title bar and controls."""
    c.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#C0C0C0"/>'
          f'<path d="M{x},{y + h} V{y} H{x + w}" stroke="#FFFFFF" stroke-width="2" fill="none"/><path d="M{x},{y + h} H{x + w} V{y}" stroke="#000" stroke-width="2" fill="none"/>'
          f'<rect x="{x + 4}" y="{y + 4}" width="{w - 8}" height="24" fill="{"#000080" if active else "#808080"}"/>')
    c.text(x + 12, y + 21, title, 14, "#FFFFFF", W95, 700)
    for i, g in enumerate(["×", "□", "_"]):
        bx = x + w - 26 - i * 22
        c.add(f'<rect x="{bx}" y="{y + 7}" width="18" height="16" fill="#C0C0C0" stroke="#000" stroke-width="1"/>')
        c.text(bx + 9, y + 20, g, 13, "#000", W95, 700, "middle")


def palm(x, y, s, col):
    fronds = "".join(f'<path d="M{x},{y} q{dx * s * .5},{-40 * s} {dx * s},{dy * s}" stroke="{col}" stroke-width="{7 * s:.1f}" fill="none" stroke-linecap="round"/>'
                     for dx, dy in [(-90, -10), (-70, 20), (90, -10), (70, 25), (-40, -60), (40, -60)])
    return f'<path d="M{x - 6 * s},{y + 230 * s} q{14 * s},{-120 * s} {6 * s},{-230 * s}" stroke="{col}" stroke-width="{12 * s:.1f}" fill="none"/>{fronds}'


for th, t in THEMES.items():
    c = Canvas(F, t, 1200, 760)
    c.defs.append(f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["sky1"]}"/><stop offset="1" stop-color="{t["sky2"]}"/></linearGradient>'
                  f'<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["sun1"]}"/><stop offset="1" stop-color="{t["sun2"]}"/></linearGradient>')
    c.add('<rect width="1200" height="460" fill="url(#sky)"/>', '<circle cx="600" cy="400" r="190" fill="url(#sun)"/>')
    c.add('<clipPath id="sunc"><circle cx="600" cy="400" r="190"/></clipPath><g clip-path="url(#sunc)">'
          + "".join(f'<rect x="380" y="{400 - 110 + i * 26}" width="440" height="{4 + i * 3}" fill="{t["sky2"]}"/>' for i in range(6)) + "</g>")
    c.add(f'<rect y="440" width="1200" height="320" fill="{t["floor"]}"/>')
    c.add(f'<g stroke="{t["grid"]}" stroke-width="2" opacity=".8">' + "".join(f'<line x1="600" y1="440" x2="{600 + k * 160}" y2="760"/>' for k in range(-10, 11))
          + "".join(f'<line class="row" x1="0" x2="1200" y1="{440 + 320 * (i / 8) ** 2:.0f}" y2="{440 + 320 * (i / 8) ** 2:.0f}" style="--d:{320 * (((i + 1) / 8) ** 2 - (i / 8) ** 2):.0f}px"/>' for i in range(8)) + "</g>")
    c.add(palm(110, 300, 1, t["palm"]), palm(1090, 320, .9, t["palm"]), palm(200, 360, .6, t["palm"]))
    c.text(600, 120, "ＫＲＩＳＨＮＡ", 86, t["ink"], SERIF, 700, "middle", f'letter-spacing="6" style="paint-order:stroke" stroke="{t["sun2"]}" stroke-width="3"')
    c.text(600, 170, "エンジニア · 電気 · ソフトウェア", 26, t["ink"], JP, 700, "middle")
    # bmp window with pixel portrait
    win(c, 70, 470, 330, 270, "krishna.bmp - Paint")
    c.add('<rect x="80" y="504" width="310" height="226" fill="#FFFFFF"/>')
    cell = 5.5
    for r, row in enumerate(photo):
        for q, ch in enumerate(row):
            if ch != ".":
                v = int(ch)
                col = ["#2B0B4F", "#4B1380", "#6E1FA8", "#9230C2", "#B544CC", "#D85BD1", "#F279C9", "#FF9AC4", "#FFC1D6", "#FFE7EE"][v]
                c.add(f'<rect x="{125 + q * cell:.1f}" y="{506 + r * cell:.1f}" width="{cell:.1f}" height="{cell:.1f}" fill="{col}"/>')
    # error dialog
    win(c, 760, 500, 380, 180, "Error")
    c.add('<circle cx="808" cy="572" r="22" fill="#FF0000"/><path d="M798 562l20 20M818 562l-20 20" stroke="#FFF" stroke-width="5"/>')
    c.text(846, 562, "Too much manual work detected.", 15, "#000", W95)
    c.text(846, 586, "Automate it now?", 15, "#000", W95)
    for i, lab in enumerate(["Automate", "Automate"]):
        bx = 820 + i * 130
        c.add(f'<rect x="{bx}" y="626" width="110" height="32" fill="#C0C0C0"/><path d="M{bx},{658} V626 H{bx + 110}" stroke="#FFF" stroke-width="2" fill="none"/>'
              f'<path d="M{bx},{658} H{bx + 110} V626" stroke="#000" stroke-width="2" fill="none"/>')
        c.text(bx + 55, 648, lab, 14, "#000", W95, 700 if i == 0 else 400, "middle")
    c.css.append(".row{animation:rw 1.8s linear infinite}@keyframes rw{to{transform:translateY(var(--d))}}")
    c.save(f"scene-{th}.svg", f"Vaporwave scene: KRISHNA in wide letters, Japanese text for engineer, electrical, software; a pixel portrait in a Paint window, and an error: too much manual work detected, automate it now? Automate or Automate.")

    # program manager: projects as desktop icons + start bar
    c = Canvas(F, t, 1200, 520)
    c.add('<rect width="1200" height="520" fill="#008080"/>')
    win(c, 30, 24, 1140, 430, "Program Manager · C:\\KRISHNA\\SHIPPED", True)
    c.add('<rect x="40" y="58" width="1120" height="386" fill="#FFFFFF"/>')
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        x, y = 70 + (i % 5) * 220, 80 + (i // 5) * 180
        exe = slug.upper().replace("-", "_")[:8] + ".EXE"
        c.add(f'<rect x="{x + 60}" y="{y}" width="64" height="64" fill="{["#FF71CE", "#01CDFE", "#05FFA1", "#B967FF", "#FFFB96"][i % 5]}" stroke="#000" stroke-width="2"/>'
              f'<rect x="{x + 66}" y="{y + 6}" width="52" height="10" fill="#000080"/>')
        c.text(x + 92, y + 48, "⚡" if i % 2 else "▣", 22, "#000", W95, anchor="middle")
        c.text(x + 92, y + 88, exe, 13, "#000", W95, 700, "middle")
        c.text(x + 92, y + 108, short(name), 12, "#000", W95, anchor="middle")
        c.text(x + 92, y + 126, hook[:28] + ("…" if len(hook) > 28 else ""), 11, "#404040", W95, anchor="middle")
    c.add('<rect y="476" width="1200" height="44" fill="#C0C0C0"/><path d="M0 477H1200" stroke="#FFF" stroke-width="2"/>'
          '<rect x="6" y="482" width="90" height="32" fill="#C0C0C0"/><path d="M6 514V482H96" stroke="#FFF" stroke-width="2" fill="none"/><path d="M6 514H96V482" stroke="#000" stroke-width="2" fill="none"/>'
          '<rect x="1060" y="482" width="134" height="32" fill="none" stroke="#808080"/>')
    c.text(51, 504, "⊞ Start", 15, "#000", W95, 700, "middle")
    c.text(1127, 504, "2:00 AM", 14, "#000", W95, anchor="middle")
    c.text(120, 504, "▶ shipping_kiosk_sentinel.exe", 13, "#000", W95)
    c.save(f"desktop-{th}.svg", "Program Manager window listing shipped projects as .EXE icons: " + "; ".join(p[1] for p in PROJECTS))

links = " · ".join(f"[{short(p[1]).upper()}.EXE]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Vaporwave: Windows 95, palms, a sunset grid. Daytime pastel and midnight neon follow your GitHub theme. Built by scripts/gen_vapor.py -->

<p align="center">{pic(F, "scene", "Vaporwave scene with a pixel portrait and an error dialog")}</p>

<p align="center"><b>Ｗ Ｅ Ｌ Ｃ Ｏ Ｍ Ｅ　Ｔ Ｏ　Ｔ Ｈ Ｅ　Ｆ Ａ Ｃ Ｔ Ｏ Ｒ Ｙ</b><br/>
<sub>electrical engineer · software builder · chennai, 2004 → forever</sub></p>

<p align="center">{pic(F, "desktop", "Program Manager with shipped projects")}</p>
<p align="center">{links}</p>

<p align="center"><a href="mailto:{EMAIL}">ｅｍａｉｌ</a> · <a href="{LINKEDIN}">ｌｉｎｋｅｄｉｎ</a></p>
""")
print("ok")
