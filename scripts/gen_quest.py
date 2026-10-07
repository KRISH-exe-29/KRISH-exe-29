"""Interactive / motion-first profile: KRISH QUEST, a choose-your-own-adventure played with GitHub's clickable
<details> blocks, under a kinetic animated title. Run: python scripts/gen_quest.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Canvas, pic, write_readme
from profile_data import NAME, EMAIL, LINKEDIN, PROJECTS, short

F = "quest"
PIX = "'Press Start 2P', 'Courier New', monospace"
BOLD = "'Arial Black', 'Segoe UI Black', Impact, sans-serif"
THEMES = {"dark": dict(bg="#0D0B1E", ink="#FFFFFF", a="#FFCF3F", b="#3FD0FF", c="#FF4F8B", soft="#8E8AB8"),
          "light": dict(bg="#FFF8E7", ink="#1D1A33", a="#E89B00", b="#0077B6", c="#D6336C", soft="#6E6A8E")}

for th, t in THEMES.items():
    c = Canvas(F, t, 1200, 520)
    c.add(f'<rect width="1200" height="520" fill="{t["bg"]}"/>')
    # star field
    import random
    r = random.Random(3)
    c.add("".join(f'<circle class="tw" style="animation-delay:-{r.uniform(0, 3):.1f}s" cx="{r.uniform(0, 1200):.0f}" cy="{r.uniform(0, 520):.0f}" r="{r.choice([1, 1.5, 2])}" fill="{t["soft"]}"/>' for _ in range(70)))
    word = "KRISH QUEST"
    x = 600 - len(word) * 44
    for i, ch in enumerate(word):
        if ch != " ":
            col = [t["a"], t["b"], t["c"]][i % 3]
            c.add(f'<g class="drop" style="animation-delay:{i * .09:.2f}s"><text x="{x + i * 88}" y="230" font-family="{BOLD}" font-size="120" fill="{col}" '
                  f'style="paint-order:stroke" stroke="{t["ink"]}" stroke-width="6" text-anchor="middle">{ch}</text></g>')
    c.text(600, 300, "A CHOOSE-YOUR-OWN-ADVENTURE IN ONE README", 18, t["ink"], PIX, 700, "middle", 'letter-spacing="2"')
    # a bolt sword slash
    c.add(f'<path class="slash" d="M240 380 L520 330 L680 360 L960 300" fill="none" stroke="{t["a"]}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')
    c.add(f'<g class="blink">' + "" + f'<text x="600" y="450" font-family="{PIX}" font-size="22" fill="{t["c"]}" text-anchor="middle">▼ CLICK A PATH BELOW ▼</text></g>')
    c.text(600, 500, f"hero: {NAME} · class: electrical engineer · weapon: automation", 13, t["soft"], PIX, anchor="middle")
    c.css.append(".drop{animation:dp .9s cubic-bezier(.3,1.6,.5,1) backwards}@keyframes dp{from{transform:translateY(-300px);opacity:0}}"
                 ".slash{stroke-dasharray:800;animation:sl 2.8s ease-in-out infinite}@keyframes sl{0%{stroke-dashoffset:800}40%,70%{stroke-dashoffset:0}100%{stroke-dashoffset:-800}}"
                 ".blink{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}"
                 ".tw{animation:tw 3s ease-in-out infinite}@keyframes tw{50%{opacity:.2}}")
    c.save(f"title-{th}.svg", f"KRISH QUEST: a choose-your-own-adventure in one README. Hero {NAME}, class electrical engineer, weapon automation.")

proj = {p[0]: p for p in PROJECTS}


def item(slug):
    s, name, status, url, hook, impact, stack = proj[slug]
    link = f" → [open]({url})" if url else " (company-internal)"
    return f"**{name}** · {hook} {impact}.{link}"


write_readme(f"""
<!-- Interactive / motion-first: an animated title and a playable choose-your-own-adventure made from nested <details>. Built by scripts/gen_quest.py -->

<p align="center">{pic(F, "title", "KRISH QUEST")}</p>

> 🏭 **You wake up on a factory floor.** A mountain of spreadsheets blocks the exit. Somewhere, a printer is jammed. It is 4:55 PM.
>
> **What do you do?** *(click to choose)*

<details>
<summary>⚔️ <b>Path A</b>: find the electrical engineer who "does computers"</summary>

> You find **{NAME}** testing a transformer. They look up. *"Spreadsheets? Give me an evening."*
>
> **HP** ∞ · **Weapon** automation · **Armour** 128 tests · **Fuel** chai

<details>
<summary>🗡️ <b>A1</b>: "Show me something you built."</summary>

> Three scrolls appear. Pick one.

<details><summary>📜 The scroll of <b>Dispatch</b></summary>

> {item("dispatch")}

</details>
<details><summary>📜 The scroll of <b>Job Lens</b></summary>

> {item("job-lens")}

</details>
<details><summary>📜 The scroll of <b>KioskSentinel</b></summary>

> {item("kiosk-sentinel")}

</details>
</details>

<details>
<summary>🧠 <b>A2</b>: "I'll test you first." (pop quiz)</summary>

> **Q1.** At Bühler, MCC paperwork took 30 minutes. After the tool?
> <details><summary>reveal</summary>30 seconds. ⚡ +100 XP</details>
>
> **Q2.** How many automated tests guard the dispatch system?
> <details><summary>reveal</summary>128. 🛡️ +100 XP</details>
>
> **Q3.** Where did they rank at IIT Bombay's National Entrepreneurship Challenge?
> <details><summary>reveal</summary>#7 of 1500+ colleges. 🏆 +100 XP</details>
>
> **Q4.** What does the patented street light do?
> <details><summary>reveal</summary>It forms a light bubble that follows the car, saving 60% energy, and reports faults over GPS. 💡 +100 XP · <b>Quiz cleared!</b></details>

</details>
</details>

<details>
<summary>📋 <b>Path B</b>: copy the spreadsheets by hand</summary>

> It is 9:40 PM. You are on row 4,812. The printer is still jammed.
>
> 💀 **BAD ENDING.** Scroll up and choose again.

</details>

<details>
<summary>🤝 <b>Path C</b>: skip the quest and hire the engineer</summary>

> The spreadsheets dissolve. The printer un-jams itself. Somewhere, a dispatch truck leaves on time.
>
> 🏆 **TRUE ENDING UNLOCKED.** Claim it: **[{EMAIL}](mailto:{EMAIL})** · [LinkedIn]({LINKEDIN})

</details>

<details>
<summary>🎒 Inventory</summary>

| Item | Effect |
|:--|:--|
{chr(10).join(f"| {short(p[1])} | {p[5]} |" for p in PROJECTS)}

</details>

<sub>Saves automatically. Difficulty: real factory floor.</sub>
""")
print("ok")
