"""
`profile.sh --live` design: a terminal banner with a 1-bit dithered portrait and
a SYSTEM.INFO panel, a self-rated skill radar, a language radar from my public
repos, and an at-a-glance stats card. Each comes in dark and light so the README
follows the viewer's GitHub theme. Facts come from profile_data.py; rerun after
editing it, or to refresh the numbers:

    python scripts/gen_live.py

Writes into assets/live/. Needs Pillow for the portrait; everything else is stdlib.
"""
import datetime
import json
import math
import os
import re
import urllib.request

from PIL import Image

import profile_data as P

USER = "KRISH-exe-29"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "live")
MONO = "ui-monospace,SFMono-Regular,Consolas,monospace"
SANS = "ui-sans-serif,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"

THEMES = {
    "dark": dict(bg="#0A101F", win="#0D1628", panel="#101B30", line="#25344C", muted="#8291A8", ink="#DDE7F5",
                 cyan="#22D3EE", ok="#10B981", accent="#aa9bef", grid="#30363d", spoke="#21262d", card="#0d1117",
                 title="#e6edf3", label="#c9d1d9", sub="#8b949e", stroke="#3fb950", dot="#7ee787"),
    "light": dict(bg="#EEF2F8", win="#FFFFFF", panel="#F6F8FB", line="#D0D7E2", muted="#5B6B82", ink="#1B2433",
                  cyan="#0891B2", ok="#059669", accent="#7c6cd6", grid="#d0d7de", spoke="#e1e4e8", card="#ffffff",
                  title="#1f2328", label="#24292f", sub="#57606a", stroke="#1a7f37", dot="#2da44e"),
}

# self-rated 0-100; edit freely
SKILL_RADAR = [("Power Testing", 86), ("Industrial Automation", 78), ("Full-Stack Web", 85), ("Python Tooling", 84),
               ("Databases", 78), ("Embedded / IoT", 72), ("AI Integration", 80)]

INFO = [
    ("Subject", P.NAME),
    ("Role", "Associate Engineer · Digitalisation"),
    ("Origin", P.CITY),
    ("Plant", "Indo Tech Transformers"),
    ("Education", f"{P.DEGREE} · {P.GRAD}"),
    ("Status", "Testing by day · Shipping by night"),
    ("Core.Power", "IEC 60076 · SFRA · MCC panels"),
    ("Core.Lang", "TypeScript · Python · Java · C"),
    ("Core.Frontend", "React · Next.js · Three.js"),
    ("Core.Backend", "Node · Supabase · PostgreSQL"),
    ("Core.AI", "Claude · LangChain · Transformers.js"),
    ("Grid.Mail", P.EMAIL),
    ("Grid.LinkedIn", "/in/" + P.LINKEDIN.rstrip("/").rsplit("/", 1)[-1]),
    ("Grid.GitHub", USER),
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-readme"})
    return urllib.request.urlopen(req, timeout=30).read().decode()


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


# ---- data ------------------------------------------------------------------
def contributions():
    html = get(f"https://github.com/users/{USER}/contributions")
    tips = dict(re.findall(r'<tool-tip[^>]*\bfor="([^"]+)"[^>]*>([^<]*)</tool-tip>', html))
    days = []
    for td in re.findall(r'<td[^>]*ContributionCalendar-day[^>]*>', html):
        date, cid = re.search(r'data-date="([^"]+)"', td), re.search(r'\bid="([^"]+)"', td)
        m = re.match(r"(\d+)", tips.get(cid.group(1) if cid else "", ""))
        if date:
            days.append((date.group(1), int(m.group(1)) if m else 0))
    days.sort()
    counts = [c for _, c in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    i = len(counts) - 1 - (counts[-1] == 0)  # today isn't over yet
    current = 0
    while i >= 0 and counts[i]:
        current, i = current + 1, i - 1
    return sum(counts), current, longest


def github():
    user = json.loads(get(f"https://api.github.com/users/{USER}"))
    repos = json.loads(get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner"))
    langs = {}
    for r in repos:
        if r["language"] and not r["fork"]:
            langs[r["language"]] = langs.get(r["language"], 0) + 1
    total, current, longest = contributions()
    return {
        "stars": sum(r["stargazers_count"] for r in repos), "repos": user["public_repos"], "followers": user["followers"],
        "contributions": total, "current": current, "longest": longest,
        "langs": sorted(langs.items(), key=lambda kv: -kv[1])[:6],
    }


# ---- banner ----------------------------------------------------------------
def dither(invert):
    """1-bit portrait as horizontal pixel runs. Green foliage is keyed out to nothing."""
    im = Image.open(os.path.join(OUT, "portrait.jpg")).convert("RGB")
    im = im.crop((172, 20, 852, 791)).resize((300, 340), Image.LANCZOS)  # head + shoulders, 300x340
    gray = im.convert("L").point(lambda v: min(255, int(255 * (v / 255) ** 0.8)))
    bw = gray.convert("1").load()  # Floyd-Steinberg
    rgb = im.load()

    def on(x, y):
        r, g, b = rgb[x, y]
        foliage = g > r + 12 and g > b + 12
        sky = min(r, g, b) > 120 and b >= r - 20  # pale and cool; skin is warm
        return bool(bw[x, y]) != invert and not (foliage or sky)

    runs, pts = [], 0
    for y in range(340):
        x = 0
        while x < 300:
            if not on(x, y):
                x += 1
                continue
            start = x
            while x < 300 and on(x, y):
                x += 1
            runs.append(f"M{start} {y}h{x - start}")
            pts += x - start
    return "".join(runs), pts


def banner(t, theme):
    path, pts = dither(invert=theme == "light")  # light theme inks the dark pixels
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610" role="img">'
        f'<title>{esc(P.NAME)}: live system profile</title>',
        '<style>.row{opacity:0;animation:in .35s ease-out forwards}@keyframes in{to{opacity:1}}'
        '@media (prefers-reduced-motion:reduce){.row{animation:none;opacity:1}}</style>',
        f'<defs><clipPath id="scan"><rect x="49" y="124" width="390" height="0">'
        f'<animate attributeName="height" from="0" to="414" begin="0.2s" dur="2.6s" fill="freeze"/></rect></clipPath></defs>',
        f'<rect width="1180" height="610" rx="18" fill="{t["bg"]}"/>',
        f'<rect x="13" y="13" width="1154" height="584" rx="13" fill="{t["win"]}" stroke="{t["line"]}"/>',
        f'<path d="M13 62H1167" stroke="{t["line"]}"/>',
    ]
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        o.append(f'<circle cx="{38 + i*21}" cy="38" r="6" fill="{c}"/>')
    o.append(f'<text x="590" y="43" text-anchor="middle" fill="{t["muted"]}" font-family="{MONO}" font-size="13">profile.sh --live</text>')

    # left: VISUAL.MAP
    o += [
        f'<rect x="35" y="88" width="418" height="472" rx="6" fill="{t["panel"]}" stroke="{t["line"]}"/>',
        f'<path d="M35 124H453" stroke="{t["line"]}"/>',
        f'<text x="49" y="111" fill="{t["cyan"]}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="1.2">VISUAL.MAP</text>',
        f'<text x="438" y="111" text-anchor="end" fill="{t["muted"]}" font-family="{MONO}" font-size="11">300×340 / 1-BIT</text>',
        f'<path d="M49 141h12M49 141v12M439 141h-12M439 141v12M49 539h12M49 539v-12M439 539h-12M439 539v-12" fill="none" stroke="{t["cyan"]}" opacity=".55"/>',
        f'<g clip-path="url(#scan)"><path transform="translate(94 160)" d="{path}" stroke="{t["ink"]}" stroke-width="1" '
        f'shape-rendering="crispEdges" fill="none"/></g>',
        f'<text x="58" y="551" fill="{t["muted"]}" font-family="{MONO}" font-size="10">PTS {pts:,} · FLOYD-STEINBERG</text>',
    ]

    # right: SYSTEM.INFO
    o += [
        f'<rect x="475" y="88" width="670" height="472" rx="6" fill="{t["panel"]}" stroke="{t["line"]}"/>',
        f'<path d="M475 124H1145" stroke="{t["line"]}"/>',
        f'<text x="490" y="111" fill="{t["cyan"]}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="1.2">SYSTEM.INFO</text>',
        f'<circle cx="915" cy="107" r="4" fill="{t["ok"]}"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>',
        f'<text x="927" y="111" fill="{t["ok"]}" font-family="{MONO}" font-size="11" font-weight="700">LIVE</text>',
        f'<text x="1130" y="111" text-anchor="end" fill="{t["muted"]}" font-family="{MONO}" font-size="11">@{USER}</text>',
    ]
    for i, (k, v) in enumerate(INFO):
        y = 153 + i * 26
        kx = 491 + len(k) * 8.4 + 10
        vx = 1127 - len(v) * 8.4 - 10
        o.append(f'<g class="row" style="animation-delay:{0.4 + i*0.12:.2f}s">'
                 f'<text x="491" y="{y}" fill="{t["muted"]}" font-family="{MONO}" font-size="14">{esc(k)}</text>'
                 f'<path d="M{kx:.1f} {y-4}H{vx:.1f}" stroke="{t["line"]}" stroke-dasharray="1 4"/>'
                 f'<text x="1127" y="{y}" text-anchor="end" fill="{t["ink"]}" font-family="{MONO}" font-size="14">{esc(v)}</text></g>')
    o += [
        f'<path d="M490 530H1130" stroke="{t["line"]}"/>',
        f'<text x="491" y="548" fill="{t["ok"]}" font-family="{MONO}" font-size="11">● ALL SYSTEMS NOMINAL</text>',
        f'<text x="1128" y="548" text-anchor="end" fill="{t["muted"]}" font-family="{MONO}" font-size="11">UTC+5:30 · CHENNAI NODE</text>',
        "</svg>",
    ]
    return "".join(o)


# ---- radar -----------------------------------------------------------------
def radar(t, title, axes):
    n, R = len(axes), 212
    pt = lambda i, r: (r * math.sin(2 * math.pi * i / n), -r * math.cos(2 * math.pi * i / n))
    poly = lambda rs: " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(i, r) for i, r in enumerate(rs)))
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 746 526" width="746" height="526" role="img" '
         f'aria-label="{title}" font-family="{SANS}">',
         f'<text x="373" y="25" text-anchor="middle" font-size="15" font-weight="700" fill="{t["title"]}">{title}</text>',
         '<g transform="translate(373,289)">']
    for k, op in zip([1, .75, .5, .25], [.85, .72, .6, .47]):
        o.append(f'<polygon points="{poly([R*k]*n)}" fill="none" stroke="{t["grid"]}" opacity="{op}"/>')
    for i in range(n):
        x, y = pt(i, R)
        o.append(f'<line x1="0" y1="0" x2="{x:.1f}" y2="{y:.1f}" stroke="{t["spoke"]}"/>')
    vals = [R * v / 100 for _, v in axes]
    o.append('<g><animateTransform attributeName="transform" type="scale" values="0.04;1" dur="1.1s" calcMode="spline" '
             'keyTimes="0;1" keySplines="0.22 1 0.36 1" fill="freeze"/>'
             f'<polygon points="{poly(vals)}" fill="{t["accent"]}" fill-opacity="0.22" stroke="{t["stroke"]}" stroke-width="2.5" stroke-linejoin="round"/>')
    for i, r in enumerate(vals):
        x, y = pt(i, r)
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{t["dot"]}" stroke="{t["stroke"]}" stroke-width="1.2"/>')
    o.append("</g>")
    for i, (label, _) in enumerate(axes):
        x, y = pt(i, R + 25)
        anchor = "middle" if abs(x) < 1 else ("start" if x > 0 else "end")
        o.append(f'<text x="{x:.1f}" y="{y + 4:.1f}" text-anchor="{anchor}" font-size="13" font-weight="600" fill="{t["label"]}">{esc(label)}</text>')
    return "".join(o + ["</g></svg>"])


# ---- stats card ------------------------------------------------------------
def card(t, s):
    cells = [("Total stars", s["stars"]), ("Public repos", s["repos"]), ("Followers", s["followers"]),
             ("Contributions (1y)", s["contributions"]), ("Current streak", s["current"]), ("Longest streak", s["longest"])]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 159" width="480" height="159" role="img" '
         f'aria-label="{USER} GitHub statistics" font-family="{SANS}">',
         f'<rect x="0.5" y="0.5" width="479" height="158" rx="10" fill="{t["card"]}" stroke="{t["grid"]}"/>',
         f'<text x="22" y="36" font-size="15" font-weight="700" fill="{t["accent"]}">{USER}</text>',
         f'<text x="458" y="36" font-size="11" text-anchor="end" fill="{t["sub"]}">as of {datetime.date.today():%d %b %Y}</text>',
         f'<line x1="22" y1="48" x2="458" y2="48" stroke="{t["grid"]}"/>']
    for i, (label, v) in enumerate(cells):
        x, y = 22 + (i % 3) * 145.5, 74 + (i // 3) * 46
        o.append(f'<text x="{x:.0f}" y="{y}" font-size="23" font-weight="700" fill="{t["title"]}">{v:,}</text>'
                 f'<text x="{x:.0f}" y="{y+17}" font-size="10.5" fill="{t["sub"]}">{label}</text>')
    return "".join(o + ["</svg>"])


if __name__ == "__main__":
    s = github()
    assert s["current"] <= s["longest"] and len(s["langs"]) >= 3, s
    top = max(c for _, c in s["langs"])
    langs = [(name, round(100 * c / top)) for name, c in s["langs"]]
    for name, t in THEMES.items():
        for fn, body in [(f"banner-{name}.svg", banner(t, name)),
                         (f"radar-{name}.svg", radar(t, "Skill Radar", SKILL_RADAR)),
                         (f"radar-langs-{name}.svg", radar(t, "Repo Languages", langs)),
                         (f"card-stats-{name}.svg", card(t, s))]:
            with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
                f.write(body)
    print(json.dumps({k: v for k, v in s.items()}))
