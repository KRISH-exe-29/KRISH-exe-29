"""Editorial profile in numbered chapters: 01 About, 02 Recognition, 03 Selected work, 04 Toolkit, 05 Commit log, 06 Career, 07 Connect.
Copper on dark, like the windings inside a transformer. Run: python scripts/gen_chapters.py"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, icon, linked, write_readme, SANS, MONO, SERIF
from profile_data import NAME, EMAIL, LINKEDIN, CITY, DEGREE, COLLEGE, CGPA, GRAD, LANGUAGES, QUOTE, EXPERIENCE, PROJECTS, WINS, CERTS, SKILLS

F = "chapters"
T = dict(bg="#14100D", card="#1E1814", line="#3A2E25", ink="#F4EADF", soft="#B3A595", cu="#D9894A", rose="#E8B49A", deep="#7A3E1D")
PORTFOLIO = "https://krish-exe-29.github.io/KRISH_Portfolio/"
FEATURED = ["dispatch", "job-lens", "test-planner", "hardware"]
W = 1200


def canvas(h):
    c = Canvas(F, T, W, h)
    c.add(f'<rect width="{W}" height="{h}" rx="24" fill="{T["bg"]}"/>')
    return c


def chapter(c, n, title, y=74):
    c.text(48, y, f"{n:02d}", 18, T["cu"], MONO, 700)
    c.text(92, y, title, 40, T["ink"], SERIF)
    c.add(f'<line x1="48" x2="{W - 48}" y1="{y + 24}" y2="{y + 24}" stroke="{T["line"]}"/>')


def pill(c, x, y, label, fill, ink, size=13):
    w = 22 + len(label) * size * .62
    c.add(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{size * 2.1:.0f}" rx="{size * 1.05:.0f}" fill="{fill}"/>')
    c.text(x + w / 2, y + size * 1.45, label, size, ink, MONO, 600, "middle")
    return x + w + 8


def wave(x0, x1, y, amp, period, phase, step=8):
    return "M" + " L".join(f"{x},{y + amp * math.sin(2 * math.pi * (x - x0) / period + phase):.1f}" for x in range(x0, x1 + 1, step))


def img(name, alt, width="100%"):
    return f'<img src="./assets/{F}/{name}.svg" width="{width}" alt="{alt}"/>'


def badge(label, logo, url, text=""):
    msg = f"{label}-{text}" if text else label
    return (f'<a href="{url}"><img src="https://img.shields.io/badge/{msg}-7A3E1D?style=for-the-badge&labelColor=14100D'
            f'&logoColor=F4EADF&logo={logo}" alt="{label.replace("_", " ")}"/></a>')


# ── hero ──
c = canvas(520)
for i, col in enumerate((T["cu"], T["rose"], T["deep"])):
    c.add(f'<path class="w" d="{wave(0, W, 440, 34, 300, i * 2 * math.pi / 3)}" fill="none" stroke="{col}" stroke-width="2.5" opacity=".85"/>')
c.css.append(".w{stroke-dasharray:14 10;animation:flow 6s linear infinite}@keyframes flow{to{stroke-dashoffset:-240}}"
             ".in{animation:up .9s cubic-bezier(.2,0,0,1) both}@keyframes up{from{opacity:0;transform:translateY(16px)}}")
c.text(64, 96, "ELECTRICAL ENGINEER  ·  SHIPS SOFTWARE  ·  " + CITY.upper(), 15, T["cu"], MONO, 700, extra='letter-spacing="2"')
c.text(60, 200, NAME, 92, T["ink"], SERIF, extra='class="in"')
c.para(64, 256, "Nine apps running on a transformer factory floor. One patent filed. A habit of turning 30-minute chores into 30-second taps.",
       21, 640, fill=T["soft"])
for i, (big, small) in enumerate([("9", "apps in production"), ("128", "tests guarding dispatch"), ("30 min → 30 s", "hardware paperwork")]):
    y = 120 + i * 92
    c.text(820, y + 26, big, 34, T["rose"], SERIF, extra=f'class="in" style="animation-delay:{.2 + i * .15}s"')
    c.text(820, y + 52, small, 14, T["soft"], MONO)
    c.add(f'<line x1="820" x2="1136" y1="{y + 70}" y2="{y + 70}" stroke="{T["line"]}"/>')
c.save("hero.svg", f"{NAME}: electrical engineer who ships software. Nine apps in production, 128 tests guarding dispatch, 30 minutes of paperwork cut to 30 seconds.")

# ── 01 about ──
c = canvas(400)
chapter(c, 1, "About")
c.para(48, 150, "I test 161 kV transformers by day and write the software the plant runs on by night. Dispatch, testing, quality and "
       "hardware paperwork used to live in spreadsheets and phone calls. Now they are buttons.", 22, 640, fill=T["ink"], font=SERIF)
c.text(48, 330, f"“{QUOTE}”", 15, T["soft"], SERIF, extra='font-style="italic"')
c.add(f'<rect x="780" y="128" width="372" height="232" rx="18" fill="{T["card"]}" stroke="{T["line"]}"/>')
c.text(808, 164, "RIGHT NOW", 13, T["cu"], MONO, 700, extra='letter-spacing="2"')
for i, s in enumerate(["Associate Engineer, Indo Tech", "Leading OT-IT: sensors → cloud", "Growing an AI agent, v12",
                       f"{DEGREE}, CGPA {CGPA}", " · ".join(LANGUAGES)]):
    c.add(f'<circle cx="814" cy="{196 + i * 34}" r="4" fill="{T["rose"] if i < 3 else T["line"]}"/>')
    c.text(830, 201 + i * 34, s, 16, T["ink"] if i < 3 else T["soft"], SANS)
c.save("about.svg", "01 About: tests 161 kV transformers by day, writes the plant's software by night. Right now: Associate Engineer at Indo Tech, leading OT-IT integration, growing an AI agent.")

# ── 02 recognition ──
c = canvas(330)
chapter(c, 2, "Recognition")
for i, (when, title, where) in enumerate(WINS):
    x = 48 + i * 280
    c.add(f'<rect x="{x}" y="128" width="264" height="168" rx="18" fill="{T["card"]}" stroke="{T["line"]}"/>')
    c.text(x + 24, 160, when.upper(), 12, T["cu"], MONO, 700, extra='letter-spacing="1.5"')
    c.text(x + 24, 204, title, 24, T["rose"], SERIF)
    c.para(x + 24, 240, where, 14, 220, fill=T["soft"])
c.save("recognition.svg", "02 Recognition: " + "; ".join(f"{t}, {w} ({d})" for d, t, w in WINS))

# ── 03 selected work ──
c = canvas(110)
chapter(c, 3, "Selected work", 64)
c.save("title-work.svg", "03 Selected work")
by_slug = {p[0]: p for p in PROJECTS}
for slug in FEATURED:
    _, name, status, url, hook, impact, stack = by_slug[slug]
    c = canvas(250)
    c.add(f'<circle cx="140" cy="125" r="76" fill="{T["card"]}" stroke="{T["line"]}"/>' + icon(slug, 92, 77, 96, T["cu"], T["rose"], T["deep"]))
    c.text(260, 92, name, 36, T["ink"], SERIF)
    pill(c, 262, 110, status, T["deep"], T["ink"])
    c.text(262, 172, hook, 20, T["rose"], SANS)
    c.text(262, 206, f"{impact}   ·   {stack}", 15, T["soft"], MONO)
    c.save(f"project-{slug}.svg", f"{name} ({status.lower()}): {hook} {impact}. {stack}.")
rest = [p for p in PROJECTS if p[0] not in FEATURED]
c = canvas(110 + (len(rest) + 1) // 2 * 64)
c.text(48, 56, "ALSO SHIPPED", 13, T["cu"], MONO, 700, extra='letter-spacing="2"')
for i, (slug, name, status, url, hook, *_ ) in enumerate(rest):
    x, y = 48 + (i % 2) * 560, 90 + (i // 2) * 64
    c.add(icon(slug, x, y, 40, T["cu"], T["rose"], T["deep"]))
    c.text(x + 56, y + 18, name, 18, T["ink"], SERIF)
    c.text(x + 56, y + 40, hook, 14, T["soft"], SANS)
c.save("also-shipped.svg", "Also shipped: " + "; ".join(f"{p[1]}: {p[4]}" for p in rest))

# ── 04 toolkit ──
rows = max(len(v) for v in SKILLS.values())
c = canvas(170 + rows * 42)
chapter(c, 4, "Toolkit")
for i, (group, items) in enumerate(SKILLS.items()):
    x = 48 + i * 280
    c.text(x, 150, group.upper(), 14, T["cu"], MONO, 700, extra='letter-spacing="2"')
    c.add(f'<line x1="{x + 6}" x2="{x + 6}" y1="170" y2="{150 + len(items) * 42}" stroke="{T["line"]}" stroke-dasharray="2 5"/>')
    for j, s in enumerate(items):
        y = 186 + j * 42
        c.add(f'<circle cx="{x + 6}" cy="{y - 5}" r="5" fill="{T["rose"] if j == 0 else T["deep"]}"/>')
        c.text(x + 24, y, s, 16, T["ink"], SANS)
c.save("toolkit.svg", "04 Toolkit: " + "; ".join(f"{g}: {', '.join(v)}" for g, v in SKILLS.items()))

# ── 05 commit log / 06 career / 07 connect titles ──
for n, title, name in [(5, "Commit log", "title-commits"), (7, "Connect", "title-connect")]:
    c = canvas(110)
    chapter(c, n, title, 64)
    c.save(f"{name}.svg", f"{n:02d} {title}")

c = canvas(170 + len(EXPERIENCE) * 76 + 70)
chapter(c, 6, "Career")
for i, (org, role, when, where, what, win) in enumerate(EXPERIENCE):
    y = 160 + i * 76
    c.text(48, y, when, 14, T["cu"], MONO, 700)
    c.text(220, y, org, 22, T["ink"], SERIF)
    c.text(W - 48, y, where, 14, T["soft"], MONO, anchor="end")
    c.text(220, y + 28, f"{role}. {win}.", 15, T["soft"], SANS)
y = 170 + len(EXPERIENCE) * 76
c.text(48, y, "CERTIFIED", 13, T["cu"], MONO, 700, extra='letter-spacing="2"')
c.text(220, y, f"{COLLEGE}, {GRAD}  ·  " + "  ·  ".join(CERTS[:3]), 14, T["soft"], SANS)
c.save("career.svg", "06 Career: " + "; ".join(f"{e[0]}, {e[1]}, {e[2]}" for e in EXPERIENCE) + ". Certified: " + ", ".join(CERTS))

# ── signature ──
c = canvas(220)
c.text(W / 2, 112, "Krishna", 72, T["rose"], SERIF, anchor="middle", extra='font-style="italic"')
c.add(f'<path class="sig" d="M430 136 Q600 160 770 128" fill="none" stroke="{T["cu"]}" stroke-width="3" stroke-linecap="round"/>')
c.css.append(".sig{stroke-dasharray:360;animation:sig 2.4s ease-out both}@keyframes sig{from{stroke-dashoffset:360}}")
c.text(W / 2, 184, "Send it over. I'll turn it into a button.", 16, T["soft"], MONO, anchor="middle")
c.save("signature.svg", "Krishna. Send it over. I'll turn it into a button.")


def buttons(url):
    if "github.com" in url:
        return badge("Repository", "github", url)
    return badge("Live_demo", "vercel" if "vercel.app" in url else "githubpages", url)


cards = "\n\n".join(
    f'<p align="center">{linked(by_slug[s][3], img(f"project-{s}", by_slug[s][1] + ": " + by_slug[s][4]))}</p>\n'
    f'<p align="center">{buttons(by_slug[s][3])}</p>' for s in FEATURED)
stats = ("https://github-readme-stats.vercel.app/api?username=KRISH-exe-29&show_icons=true&hide_rank=true&hide_border=true&border_radius=16"
         "&bg_color=14100D&title_color=E8B49A&text_color=B3A595&icon_color=D9894A&custom_title=GitHub%20at%20a%20glance")
contact = "\n  ".join([badge("Email", "gmail", f"mailto:{EMAIL}", "krishnarajus2004"), badge("LinkedIn", "linkedin", LINKEDIN),
                      badge("Portfolio", "githubpages", PORTFOLIO), badge("Job_Lens", "githubpages", "https://krishna-ittl.github.io/Candidate-Screener/")])
write_readme(f"""
<!-- Editorial profile in numbered chapters. Built by scripts/gen_chapters.py: edit scripts/profile_data.py, then rerun. -->

<a href="{PORTFOLIO}">{img("hero", f"{NAME}: electrical engineer who ships software. Nine apps in production.")}</a>

<p align="center">
  {contact}
</p>

{img("about", "01 About: tests 161 kV transformers by day, writes the plant's software by night.")}

{img("recognition", "02 Recognition: Rank 7 of 1500+ at IIT Bombay NEC, Fish Tank runner-up, patent filed, national finalist.")}

{img("title-work", "03 Selected work")}

{cards}

{img("also-shipped", "Also shipped: KioskSentinel, Street Lighting, RTCC Tracker, Industrial Data, HWE Tool, Flood Alerts.")}

{img("toolkit", "04 Toolkit: power, code, things and AI.")}

{img("title-commits", "05 Commit log")}

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/KRISH-exe-29/KRISH-exe-29/output/snake-dark.svg"/>
  <img alt="Snake eating my contribution graph" src="https://raw.githubusercontent.com/KRISH-exe-29/KRISH-exe-29/output/snake.svg"/>
</picture>

<p align="center"><img width="400" src="{stats}" alt="GitHub at a glance"/></p>

{img("career", "06 Career: Indo Tech Transformers, Bühler India, Inovate Technologies, Mettur Thermal Power Plant, Southern Railway.")}

{img("title-connect", "07 Connect")}

<p align="center">
  {contact}
</p>

<a href="{PORTFOLIO}">{img("signature", "Krishna. Send it over. I'll turn it into a button.")}</a>
""")
print("ok")
