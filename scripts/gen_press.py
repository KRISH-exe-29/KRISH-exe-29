"""Editorial / newspaper SVGs for the profile README: the morning (light) and night (dark) editions.

Run:  python scripts/gen_press.py   (facts in scripts/profile_data.py, press photo from scripts/halftone.py)
"""
import os, sys
from xml.sax.saxutils import escape as esc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from profile_data import (NAME, EMAIL, CITY, COLLEGE, DEGREE, CGPA, GRAD, LANGUAGES, QUOTE,
                          EXPERIENCE, PROJECTS, WINS, CERTS)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "press")
BLACKLETTER = "'Old English Text MT', 'UnifrakturMaguntia', 'Engravers Old English', 'Times New Roman', serif"
DISPLAY = "'Playfair Display', Didot, 'Bodoni 72', 'Bodoni MT', 'Times New Roman', Georgia, serif"
BODY = "Georgia, 'Times New Roman', Times, serif"
LABEL = "'Franklin Gothic Medium', 'Arial Narrow', 'Helvetica Neue', Arial, sans-serif"
THEMES = {"light": dict(paper="#F3EEE3", ink="#1A1A1A", soft="#4A4640", rule="#1A1A1A", red="#B3261E", edition="LATE CITY EDITION"),
          "dark": dict(paper="#15130F", ink="#EDE6D6", soft="#B9B1A1", rule="#EDE6D6", red="#F0644F", edition="NIGHT EDITION")}
REDUCE = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def wrap(text, size, width, factor=.5):
    per = max(8, int(width / (size * factor)))
    lines, line = [], ""
    for w in text.split():
        if len(line) + len(w) + 1 > per and line:
            lines.append(line); line = w
        else:
            line = f"{line} {w}".strip()
    return lines + [line] if line else lines


class Page:
    def __init__(self, t, w, h):
        self.t, self.w, self.h, self.b = t, w, h, []

    def add(self, s):
        self.b.append(s)

    def text(self, x, y, s, size, font=BODY, fill=None, weight=400, anchor="start", style="", extra=""):
        self.add(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill or self.t["ink"]}" '
                 f'text-anchor="{anchor}" {f"font-style={chr(34)}{style}{chr(34)}" if style else ""} {extra}>{esc(s)}</text>')

    def para(self, x, y, s, size, width, lh=1.42, **kw):
        lines = wrap(s, size, width)
        for i, l in enumerate(lines):
            self.text(x, y + i * size * lh, l, size, **kw)
        return y + len(lines) * size * lh

    def rule(self, x1, x2, y, w=1.2):
        self.add(f'<line x1="{x1}" x2="{x2}" y1="{y}" y2="{y}" stroke="{self.t["rule"]}" stroke-width="{w}"/>')

    def vrule(self, x, y1, y2, w=1):
        self.add(f'<line x1="{x}" x2="{x}" y1="{y1}" y2="{y2}" stroke="{self.t["rule"]}" stroke-width="{w}" opacity=".6"/>')

    def kicker(self, x, y, s, color=None):
        self.text(x, y, s.upper(), 13, LABEL, color or self.t["red"], 700, extra='letter-spacing="2.5"')

    def save(self, name, title, style=""):
        t, w, h = self.t, self.w, self.h
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">'
               f'<title>{esc(title)}</title><defs><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/>'
               f'<feColorMatrix values="0 0 0 0 .5  0 0 0 0 .45  0 0 0 0 .4  0 0 0 .07 0"/><feComposite in2="SourceAlpha" operator="in"/></filter></defs>'
               f'<style>{style}{REDUCE}</style>'
               f'<rect width="{w}" height="{h}" fill="{t["paper"]}"/><rect width="{w}" height="{h}" fill="#000" filter="url(#grain)"/>'
               f'{"".join(self.b)}</svg>\n')
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(svg)


dots = open(os.path.join(OUT, "halftone.txt"), encoding="utf-8").read().split("\n")

for theme, t in THEMES.items():
    # ── front page ──
    p = Page(t, 1200, 1000)
    p.rule(40, 1160, 34, 1)
    p.text(40, 26, f"VOL. 22 · NO. 2004 · {CITY.upper()}", 13, LABEL, t["soft"], 700, extra='letter-spacing="2"')
    p.text(600, 26, "₹0 · FREE FOR RECRUITERS", 13, LABEL, t["soft"], 700, "middle", extra='letter-spacing="2"')
    p.text(1160, 26, t["edition"], 13, LABEL, t["red"], 700, "end", extra='letter-spacing="2"')
    p.text(600, 124, "The Krishna Chronicle", 70, BLACKLETTER, anchor="middle")
    # ears
    p.add(f'<rect x="40" y="56" width="160" height="86" fill="none" stroke="{t["rule"]}"/>')
    p.text(120, 78, "WEATHER", 12, LABEL, t["red"], 700, "middle", extra='letter-spacing="2"')
    p.text(120, 102, "100% chance", 13, BODY, anchor="middle", style="italic")
    p.text(120, 120, "of deploys. Excel", 13, BODY, anchor="middle", style="italic")
    p.text(120, 137, "clearing by noon.", 13, BODY, anchor="middle", style="italic")
    p.add(f'<rect x="1000" y="56" width="160" height="86" fill="none" stroke="{t["rule"]}"/>'
          f'<clipPath id="tick"><rect x="1002" y="84" width="156" height="56"/></clipPath>')
    p.text(1080, 78, "MARKETS", 12, LABEL, t["red"], 700, "middle", extra='letter-spacing="2"')
    tape = "$KRISH ▲ 9 apps   $TESTS ▲ 128   $TIME ▼ 98%   $CGPA 8.38   "
    p.add(f'<g clip-path="url(#tick)"><g class="tick"><text x="1002" y="118" font-family="{LABEL}" font-size="17" font-weight="700" fill="{t["ink"]}" xml:space="preserve">{esc(tape * 3)}</text></g></g>')
    p.rule(40, 1160, 160, 3)
    p.rule(40, 1160, 166, 1)
    # headline + deck
    p.text(600, 230, "LOCAL ENGINEER DELETES 30-MINUTE TASK;", 42, DISPLAY, weight=900, anchor="middle", extra='letter-spacing="-1"')
    p.text(600, 290, "FACTORY QUIETLY ASKS FOR MORE", 54, DISPLAY, weight=900, anchor="middle", extra='letter-spacing="-1"')
    p.text(600, 346, "Trained on transformers, fluent in Git, and “not done yet,” sources confirm.", 22, BODY, t["soft"], anchor="middle", style="italic")
    p.rule(40, 1160, 370, 1)
    # press photo: halftone that prints in, row by row
    ox, oy, cell = 52, 392, 7.6
    rows = []
    for y, row in enumerate(dots):
        cs = []
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            ink = int(ch) if theme == "light" else 9 - int(ch)  # light ink on a dark page prints the inverse
            if ink:
                cs.append(f'<circle cx="{ox + x * cell:.1f}" cy="{oy + y * cell:.1f}" r="{.42 * cell * (ink / 9) ** .6:.2f}"/>')
        rows.append(f'<g class="pr" style="animation-delay:{.4 + y * .03:.2f}s">{"".join(cs)}</g>')
    p.add(f'<rect x="40" y="382" width="510" height="510" fill="none" stroke="{t["rule"]}"/>'
          f'<g fill="{t["ink"]}">{"".join(rows)}</g>'
          f'<rect class="roller" x="40" y="382" width="510" height="6" fill="{t["red"]}" opacity=".7"/>')
    p.para(40, 916, "THE SUSPECT: Krishna Raju S, photographed moments before automating something. Chronicle staff.", 14, 510, font=BODY, style="italic", fill=t["soft"])
    # lead story in two columns
    p.kicker(580, 400, "Exclusive · Shop floor")
    p.text(580, 444, "Nine apps, one plant,", 34, DISPLAY, weight=800)
    p.text(580, 484, "zero spreadsheets spared", 34, DISPLAY, weight=800)
    p.text(580, 512, f"By the Chronicle desk · {CITY}", 13, LABEL, t["soft"], 700, extra='letter-spacing="1.5"')
    col1 = (f"KANCHIPURAM — Krishna arrived at Indo Tech Transformers to test them: ratio, vector group, SFRA, partial discharge, the full IEC 60076 drill. "
            f"Then Krishna noticed how much of the plant still ran on paper, phone calls and copy-paste. Witnesses report a long silence. "
            f"Months later, dispatch, testing, hiring and attendance run on Krishna's software.")
    col2 = (f"The habit is not new. As an intern at Bühler India, Krishna built a Python tool that turned thirty minutes of MCC paperwork into thirty seconds. "
            f"Before that: a patent filing for street lights that follow the car, a #7 national rank among 1500+ colleges at IIT Bombay, "
            f"and a {DEGREE} from {COLLEGE} (CGPA {CGPA}).")
    p.para(580, 548, col1, 15.5, 274)
    p.vrule(870, 532, 900)
    p.para(886, 548, col2, 15.5, 274)
    # pull quote
    p.rule(580, 1160, 924, 2)
    p.text(870, 960, "“Fluent in both Ohm's Law and Git commits.”", 24, DISPLAY, t["red"], 700, "middle", style="italic")
    p.text(870, 986, "— the subject, in their own words", 13, LABEL, t["soft"], 700, "middle", extra='letter-spacing="1.5"')
    p.save(f"front-{theme}.svg", f"The Krishna Chronicle. Local engineer deletes 30-minute task; factory quietly asks for more. {col1} {col2}",
           ".pr{animation:ink .5s ease-out backwards}@keyframes ink{from{opacity:0}}"
           ".roller{animation:roll 2.6s linear .4s backwards}@keyframes roll{from{transform:translateY(0);opacity:.7}to{transform:translateY(504px);opacity:.7}}"
           ".roller{transform:translateY(504px);opacity:0}"
           ".tick{animation:tk 16s linear infinite}@keyframes tk{to{transform:translateX(-" + f"{len(tape) * 9.3:.0f}" + "px)}}")

    # ── business section: career as articles ──
    HEADS = ["Testing engineer becomes the plant's software engineer; CEO signs off on fastener standard",
             "Intern's tool turns 30 minutes of paperwork into 30 seconds",
             "‘Project Phantom’ ships; first production deploy confirmed",
             "Student sees megawatts up close, takes very good notes",
             "Where it all started: the railways"]
    p = Page(t, 1200, 650)
    p.text(40, 64, "Business & Industry", 44, DISPLAY, weight=800)
    p.text(1160, 64, "SECTION B · CAREER", 13, LABEL, t["red"], 700, "end", extra='letter-spacing="2.5"')
    p.rule(40, 1160, 84, 3)
    p.rule(40, 1160, 90, 1)
    # lead article (first job) wide, then a 4-column row
    org, role, when, where, what, win = EXPERIENCE[0]
    p.kicker(40, 126, f"{org} · {when}")
    y = 126
    for l in wrap(HEADS[0], 36, 1080, .48):
        y += 44
        p.text(40, y, l, 36, DISPLAY, weight=800)
    p.text(40, y + 30, f"{role} · {where}", 14, LABEL, t["soft"], 700, extra='letter-spacing="1"')
    p.para(40, y + 62, f"{what} {win}. Dispatch, KioskSentinel, Job Lens and the test planner followed.", 17, 1100)
    p.rule(40, 1160, 330, 1)
    for i, (org, role, when, where, what, win) in enumerate(EXPERIENCE[1:]):
        x = 40 + i * 285
        if i:
            p.vrule(x - 12, 350, 630)
        p.kicker(x, 364, org)
        yy = 364
        for l in wrap(HEADS[i + 1], 22, 262, .5):
            yy += 28
            p.text(x, yy, l, 22, DISPLAY, weight=800)
        p.text(x, yy + 26, f"{when} · {where}", 12, LABEL, t["soft"], 700, extra='letter-spacing="1"')
        yy = p.para(x, yy + 54, f"{role}. {what}", 15, 262)
        p.para(x, yy + 8, f"▸ {win}", 14, 262, font=BODY, fill=t["red"], weight=700, style="italic")
    p.save(f"business-{theme}.svg", "Career: " + "; ".join(f"{o}, {r}, {w}: {x} {n}" for o, r, w, _, x, n in EXPERIENCE))

    # ── project clippings ──
    for i, (slug, name, status, url, hook, impact, stack) in enumerate(PROJECTS):
        p = Page(t, 600, 330)
        rot = [-1.4, 1.1, -.8, 1.5, -1.2, .9, -1.6, 1.2, -.7, 1.3][i]
        teeth = "".join(f"L{x},{(14 if (x // 12) % 2 else 20)}" for x in range(24, 577, 12))
        bteeth = "".join(f"L{x},{(312 if (x // 12) % 2 else 306)}" for x in range(576, 23, -12))
        clip_fill = "#FBF8F1" if theme == "light" else "#221F19"
        p.add(f'<g transform="rotate({rot} 300 165)"><path d="M24,20 {teeth} L576,306 {bteeth} Z" fill="{clip_fill}" stroke="{t["rule"]}" stroke-opacity=".25" '
              f'style="filter:drop-shadow(0 6px 8px rgba(0,0,0,.25))"/>'
              f'<rect x="250" y="4" width="100" height="26" fill="#E9D9A6" opacity=".75" transform="rotate(-3 300 17)"/>')
        p.kicker(48, 62, "Breaking" if status in ("PRODUCTION", "LIVE") else status.title())
        p.text(552, 62, f"No. {i + 1:02d}", 13, LABEL, t["soft"], 700, "end", extra='letter-spacing="2"')
        p.rule(48, 552, 74, 1)
        p.text(48, 118, name, 36 if len(name) < 20 else 30, DISPLAY, weight=900, extra='letter-spacing="-.5"')
        p.text(48, 158, hook, 19, BODY, style="italic")
        p.text(48, 198, impact, 17, BODY, weight=700)
        p.rule(48, 552, 236, .8)
        p.text(48, 266, f"Filed under: {stack}", 14, LABEL, t["soft"], 700, extra='letter-spacing="1"')
        if url:
            p.text(552, 266, "Read more →", 14, BODY, t["red"], 700, "end", style="italic")
        p.add("</g>")
        p.save(f"card-{slug}-{theme}.svg", f"No. {i + 1:02d}, {name} ({status}): {hook} {impact}.")

    # ── sports-style scoreboard + comic strip ──
    p = Page(t, 1200, 520)
    p.text(40, 64, "Scores & Standings", 44, DISPLAY, weight=800)
    p.text(1160, 64, "SECTION C · AWARDS", 13, LABEL, t["red"], 700, "end", extra='letter-spacing="2.5"')
    p.rule(40, 1160, 84, 3)
    p.rule(40, 1160, 90, 1)
    y = 132
    for when, title, where in WINS:
        p.text(40, y, where, 18, BODY)
        p.add(f'<line x1="{52 + len(where) * 9.2:.0f}" x2="{1036 - len(title) * 13.5:.0f}" y1="{y - 4}" y2="{y - 4}" stroke="{t["soft"]}" stroke-dasharray="1 6" stroke-width="2"/>')
        p.text(1050, y, title.upper(), 18, LABEL, t["red"] if "#7" in title else t["ink"], 700, "end", extra='letter-spacing="1.5"')
        p.text(1160, y, when, 15, LABEL, t["soft"], 700, "end")
        y += 38
    p.text(40, y + 6, "ALSO QUALIFIED: " + "  ·  ".join(CERTS), 13, LABEL, t["soft"], 700, extra='letter-spacing="1"')
    # comic: three panels
    cy = y + 34
    lines = [("BOSS: This report takes", "30 minutes. Every day."), ("KRISHNA: hmm.", "*types for one evening*"),
             ("BOSS: It takes 30 seconds now.", "What do I do with the rest?")]
    for k, (a, b) in enumerate(lines):
        x = 40 + k * 378
        p.add(f'<g class="pane" style="animation-delay:{.3 + k * .5:.1f}s"><rect x="{x}" y="{cy}" width="356" height="{500 - cy}" fill="none" stroke="{t["rule"]}" stroke-width="2"/>')
        fx = x + 70
        p.add(f'<g stroke="{t["ink"]}" stroke-width="3" fill="none" stroke-linecap="round">'
              f'<circle cx="{fx}" cy="{cy + 52}" r="13"/><line x1="{fx}" y1="{cy + 65}" x2="{fx}" y2="{cy + 100}"/>'
              f'<line x1="{fx}" y1="{cy + 76}" x2="{fx + (22 if k == 1 else -18)}" y2="{cy + (70 if k == 1 else 92)}"/>'
              f'<line x1="{fx}" y1="{cy + 76}" x2="{fx + 20}" y2="{cy + (70 if k == 1 else 92)}"/></g>')
        if k == 1:
            p.add(f'<rect x="{fx + 26}" y="{cy + 64}" width="60" height="38" rx="3" fill="none" stroke="{t["ink"]}" stroke-width="2.5"/>'
                  f'<text x="{fx + 56}" y="{cy + 89}" text-anchor="middle" font-family="monospace" font-size="14" fill="{t["red"]}">&gt;_</text>')
        p.add(f'<rect x="{x + 120}" y="{cy + 22}" width="224" height="62" rx="16" fill="{t["paper"]}" stroke="{t["ink"]}" stroke-width="2"/>')
        p.text(x + 132, cy + 48, a, 14, LABEL, weight=700)
        p.text(x + 132, cy + 70, b, 14, LABEL, weight=700)
        p.add("</g>")
    p.save(f"scores-{theme}.svg", "Scores: " + "; ".join(f"{b}: {a}, {w}" for w, a, b in WINS)
           + ". Comic: Boss: this report takes 30 minutes every day. Krishna types for one evening. Boss: it takes 30 seconds now, what do I do with the rest?",
           ".pane{animation:pane .6s ease-out backwards}@keyframes pane{from{opacity:0;transform:translateY(8px)}}")

    # ── classifieds ──
    ads = [("WANTED", "Boring, repetitive processes. Any size. Will automate. Ask for Krishna."),
           ("FOR HIRE", f"EEE engineer, fluent in Ohm's Law and Git. Speaks {', '.join(LANGUAGES[:-1])} and {LANGUAGES[-1]}."),
           ("LOST & FOUND", "Lost: 30 minutes of paperwork. Found: 30 seconds. Bühler India, Bengaluru."),
           ("EDUCATION", f"{DEGREE}, {COLLEGE}, Chennai. CGPA {CGPA}. Class of {GRAD}."),
           ("PUBLIC NOTICE", "Patent filed, Aug 2025. Street lights will now follow your car. Please do not panic."),
           ("SEEKING", "Hard problems on factory floors. Bonus points if someone said “it's always been done this way.”")]
    p = Page(t, 1200, 620)
    p.text(600, 70, "Classifieds", 52, BLACKLETTER, anchor="middle")
    p.rule(40, 1160, 92, 3)
    p.rule(40, 1160, 98, 1)
    for i, (head, body) in enumerate(ads):
        x, y = 40 + (i % 3) * 380, 124 + (i // 3) * 190
        p.add(f'<rect x="{x}" y="{y}" width="360" height="170" fill="none" stroke="{t["rule"]}" stroke-width="{2 if i == 0 else 1}"/>')
        p.text(x + 180, y + 36, head, 22, DISPLAY, t["red"] if i == 0 else t["ink"], 900, "middle", extra='letter-spacing="2"')
        p.para(x + 20, y + 70, body, 16, 320)
    p.add(f'<rect x="40" y="512" width="1120" height="76" fill="{t["ink"]}"/>')
    p.text(600, 546, "REPLY TO BOX 2004", 14, LABEL, t["paper"], 700, "middle", extra='letter-spacing="4"')
    p.text(600, 574, EMAIL, 22, BODY, t["paper"], 700, "middle")
    p.save(f"classifieds-{theme}.svg", "Classifieds: " + " ".join(f"{h}: {b}" for h, b in ads) + f" Reply to {EMAIL}")
print("ok")
