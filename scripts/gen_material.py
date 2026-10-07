"""Material Design 3 profile: tonal surfaces, elevation, chips, FAB with ripple, lists, stepper, snackbar.
Run: python scripts/gen_material.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, icon, pic, write_readme
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, EXPERIENCE, CGPA, short

F = "material"
ROBOTO = "Roboto, 'Google Sans', 'Segoe UI', Arial, sans-serif"
THEMES = {  # Material 3 tonal palette from seed #6750A4
    "light": dict(surf="#FEF7FF", cont="#F3EDF7", high="#ECE6F0", pri="#6750A4", onpri="#FFFFFF", pcont="#EADDFF", onpc="#21005D",
                  sec="#E8DEF8", tert="#7D5260", tcont="#FFD8E4", ink="#1D1B20", soft="#49454F", line="#CAC4D0", shadow=".18"),
    "dark": dict(surf="#141218", cont="#211F26", high="#2B2930", pri="#D0BCFF", onpri="#381E72", pcont="#4F378B", onpc="#EADDFF",
                 sec="#4A4458", tert="#EFB8C8", tcont="#633B48", ink="#E6E0E9", soft="#CAC4D0", line="#49454F", shadow=".5"),
}
STATUS_COL = {"PRODUCTION": "pcont", "LIVE": "pcont", "IN USE": "sec", "SHIPPED": "sec", "NEW": "tcont", "PATENT FILED": "tcont", "BUILT": "high"}


def elev(c, t, level=1):
    c.defs.append(f'<filter id="e{level}" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="{level}" stdDeviation="{level * 1.5}" '
                  f'flood-color="#000" flood-opacity="{t["shadow"]}"/></filter>')


for th, t in THEMES.items():
    # hero: app bar + profile card + FAB
    c = Canvas(F, t, 1200, 600)
    for lv in (1, 3, 6):
        elev(c, t, lv)
    c.add(f'<rect width="1200" height="600" fill="{t["surf"]}"/>')
    c.add(f'<rect width="1200" height="72" fill="{t["cont"]}"/>')
    c.add(f'<path d="M32 28h24M32 36h24M32 44h24" stroke="{t["ink"]}" stroke-width="3" stroke-linecap="round"/>')
    c.text(80, 44, "krishna.profile", 22, t["ink"], ROBOTO, 500)
    for i, ic in enumerate(["⌕", "⋮"]):
        c.text(1100 + i * 48, 46, ic, 26, t["ink"], ROBOTO, anchor="middle")
    c.text(48, 150, "Electrical engineer.", 56, t["ink"], ROBOTO, 400, extra='letter-spacing="-.5"')
    c.text(48, 216, "Builds the software", 56, t["ink"], ROBOTO, 400, extra='letter-spacing="-.5"')
    c.text(48, 282, "factories run on.", 56, t["pri"], ROBOTO, 500, extra='letter-spacing="-.5"')
    c.para(48, 330, "Nine apps in production at Indo Tech Transformers. One patent filed. A habit of turning 30-minute chores into 30-second taps.", 20, 600, fill=t["soft"], font=ROBOTO)
    x = 48
    for lab in ["⚡ EEE engineer", "📜 Patent filed", "🏆 NEC #7 / 1500+", "🎓 CGPA " + CGPA]:
        w = 30 + len(lab) * 9.2
        c.add(f'<rect x="{x}" y="420" width="{w:.0f}" height="36" rx="8" fill="none" stroke="{t["line"]}"/>')
        c.text(x + 14, 444, lab, 15, t["ink"], ROBOTO, 500)
        x += w + 10
    # profile card
    c.add(f'<rect x="760" y="110" width="380" height="380" rx="28" fill="{t["cont"]}" filter="url(#e1)"/>'
          f'<circle cx="950" cy="210" r="64" fill="{t["pcont"]}"/>')
    c.text(950, 232, "KR", 54, t["onpc"], ROBOTO, 500, "middle")
    c.text(950, 316, NAME, 26, t["ink"], ROBOTO, 500, "middle")
    c.text(950, 344, "Chennai · Indo Tech Transformers", 15, t["soft"], ROBOTO, anchor="middle")
    c.add(f'<rect x="800" y="372" width="300" height="6" rx="3" fill="{t["high"]}"/><rect class="prog" x="800" y="372" width="294" height="6" rx="3" fill="{t["pri"]}"/>')
    c.text(800, 404, "Manual time deleted", 13, t["soft"], ROBOTO)
    c.text(1100, 404, "98%", 13, t["pri"], ROBOTO, 700, "end")
    c.add(f'<rect x="800" y="424" width="140" height="44" rx="22" fill="{t["pri"]}"/><rect x="956" y="424" width="144" height="44" rx="22" fill="none" stroke="{t["line"]}"/>')
    c.text(870, 452, "Hire", 16, t["onpri"], ROBOTO, 500, "middle")
    c.text(1028, 452, "Projects", 16, t["pri"], ROBOTO, 500, "middle")
    # FAB with ripple
    c.add(f'<g filter="url(#e3)"><rect x="1064" y="508" width="96" height="64" rx="18" fill="{t["tcont"]}"/></g>'
          f'<clipPath id="fab"><rect x="1064" y="508" width="96" height="64" rx="18"/></clipPath>'
          f'<g clip-path="url(#fab)"><circle class="ripple" cx="1112" cy="540" r="60" fill="{t["tert"]}"/></g>')
    c.text(1112, 550, "✉", 28, t["ink"], ROBOTO, anchor="middle")
    c.css.append(".ripple{transform-box:fill-box;transform-origin:center;animation:rp 2.4s ease-out infinite}"
                 "@keyframes rp{0%{transform:scale(0);opacity:.45}70%,100%{transform:scale(1.2);opacity:0}}"
                 ".prog{animation:pg 2s cubic-bezier(.2,0,0,1) both}@keyframes pg{from{width:0}}")
    c.save(f"hero-{th}.svg", f"{NAME}: electrical engineer who builds the software factories run on. Nine apps in production, one patent filed.")

    # projects as a Material list
    c = Canvas(F, t, 1200, 860)
    elev(c, t, 1)
    c.add(f'<rect width="1200" height="860" fill="{t["surf"]}"/>')
    c.text(48, 64, "Projects", 32, t["ink"], ROBOTO, 400)
    c.text(1152, 64, "10 items", 14, t["soft"], ROBOTO, anchor="end")
    c.add(f'<rect x="32" y="88" width="1136" height="752" rx="24" fill="{t["cont"]}" filter="url(#e1)"/>')
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        y = 104 + i * 73
        if i:
            c.add(f'<line x1="120" x2="1150" y1="{y}" y2="{y}" stroke="{t["line"]}" opacity=".6"/>')
        c.add(f'<rect x="56" y="{y + 12}" width="48" height="48" rx="12" fill="{t["pcont"]}"/>' + icon(slug, 64, y + 20, 32, t["onpc"], t["pri"], t["pcont"]))
        c.text(124, y + 34, name, 18, t["ink"], ROBOTO, 500)
        c.text(124, y + 58, f"{hook}  ·  {stack}", 14, t["soft"], ROBOTO)
        lab = status.title()
        w = 24 + len(lab) * 8
        c.add(f'<rect x="{1080 - w:.0f}" y="{y + 20}" width="{w:.0f}" height="32" rx="8" fill="{t[STATUS_COL[status]]}"/>')
        c.text(1080 - w / 2, y + 41, lab, 13, t["ink"], ROBOTO, 500, "middle")
        c.text(1130, y + 44, "›" if url else "🔒", 22, t["soft"], ROBOTO, anchor="middle")
    c.save(f"projects-{th}.svg", "Projects: " + "; ".join(f"{p[1]} ({p[2].lower()}): {p[4]}" for p in PROJECTS))

    # career as a vertical stepper
    c = Canvas(F, t, 1200, 600)
    c.add(f'<rect width="1200" height="600" fill="{t["surf"]}"/>')
    c.text(48, 64, "Career", 32, t["ink"], ROBOTO, 400)
    for i, (org, role, when, where, what, win) in enumerate(EXPERIENCE):
        y = 112 + i * 98
        if i < len(EXPERIENCE) - 1:
            c.add(f'<line x1="76" x2="76" y1="{y + 22}" y2="{y + 98}" stroke="{t["line"]}" stroke-width="2"/>')
        cur = i == 0
        c.add(f'<circle cx="76" cy="{y}" r="16" fill="{t["pri"] if cur else t["pcont"]}"/>')
        c.text(76, y + 6, "●" if cur else "✓", 15, t["onpri"] if cur else t["onpc"], ROBOTO, 700, "middle")
        c.text(112, y + 6, f"{org}", 20, t["ink"], ROBOTO, 500)
        c.text(1152, y + 6, f"{when} · {where}", 14, t["soft"], ROBOTO, anchor="end")
        c.text(112, y + 32, f"{role}. {win}.", 15, t["soft"], ROBOTO)
    c.save(f"career-{th}.svg", "Career: " + "; ".join(f"{e[0]}, {e[1]}, {e[2]}" for e in EXPERIENCE))

    # bottom: nav bar + snackbar
    c = Canvas(F, t, 1200, 230)
    elev(c, t, 6)
    c.add(f'<rect width="1200" height="230" fill="{t["surf"]}"/>')
    c.add(f'<g class="snack"><rect x="300" y="24" width="600" height="56" rx="6" fill="{t["ink"]}" filter="url(#e6)"/></g>')
    c.text(324, 58, "Krishna is available for new problems.", 15, t["surf"], ROBOTO, extra='class="snack"')
    c.text(876, 58, "CONTACT", 15, "#D0BCFF" if th == "light" else "#6750A4", ROBOTO, 700, "end", extra='class="snack"')
    c.add(f'<rect y="120" width="1200" height="110" fill="{t["cont"]}"/>')
    for i, (ic, lab) in enumerate([("⌂", "Home"), ("▦", "Projects"), ("⚡", "Career"), ("✉", EMAIL)]):
        x = 150 + i * 300
        if i == 3:
            c.add(f'<rect x="{x - 32}" y="136" width="64" height="32" rx="16" fill="{t["sec"]}"/>')
        c.text(x, 160, ic, 20, t["ink"], ROBOTO, anchor="middle")
        c.text(x, 196, lab, 13, t["ink"], ROBOTO, 600 if i == 3 else 500, "middle")
    c.css.append(".snack{animation:sn .6s cubic-bezier(.2,0,0,1) 1s backwards}@keyframes sn{from{transform:translateY(40px);opacity:0}}")
    c.save(f"navbar-{th}.svg", f"Krishna is available for new problems. Contact {EMAIL}")

links = " · ".join(f"[{short(p[1])}]({p[3]})" for p in PROJECTS if p[3])
write_readme(f"""
<!-- Material Design 3: tonal surfaces, elevation and motion. Light and dark tonal schemes follow your GitHub theme. Built by scripts/gen_material.py -->

<p align="center">{pic(F, "hero", f"{NAME}: electrical engineer who builds the software factories run on.")}</p>

<p align="center">
  <a href="mailto:{EMAIL}"><img src="https://img.shields.io/badge/Email-6750A4?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
  <a href="{LINKEDIN}"><img src="https://img.shields.io/badge/LinkedIn-7D5260?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
  <a href="https://krishna-ittl.github.io/Candidate-Screener/"><img src="https://img.shields.io/badge/Open_Job_Lens-21005D?style=for-the-badge&logo=githubpages&logoColor=white" alt="Job Lens"/></a>
</p>

<p align="center">{pic(F, "projects", "Projects list")}</p>
<p align="center"><sub>tap to open: {links}</sub></p>
<p align="center">{pic(F, "career", "Career stepper")}</p>
<p align="center">{pic(F, "navbar", f"Krishna is available for new problems. {EMAIL}")}</p>
""")
print("ok")
