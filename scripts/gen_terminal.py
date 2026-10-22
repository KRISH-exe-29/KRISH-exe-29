"""
Terminal-style profile art for the `terminal` design: an animated contribution
heatmap and a streak/numbers card, both built from the real public contribution
calendar. Rerun to refresh the numbers:

    python scripts/gen_terminal.py

Writes data.json, heatmap.svg and stats.svg into assets/terminal/. Stdlib only.
GitHub runs CSS/SMIL inside <img> SVGs but never JS, so all motion is CSS/SMIL.
"""
import datetime
import json
import os
import re
import urllib.request

USER = "KRISH-exe-29"
PROMPT = "krish@github"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "terminal")

FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
BG, BG2, TILE, FRAME = "#0d1117", "#111722", "#161b22", "#30363d"
MUTED, INK, ACCENT, GREEN, BAR, GOLD = "#7d8590", "#e6edf3", "#22d3ee", "#39d353", "#26a641", "#f2cc60"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]


# ---- data ------------------------------------------------------------------
def fetch_days():
    req = urllib.request.Request(f"https://github.com/users/{USER}/contributions",
                                 headers={"User-Agent": "profile-readme"})
    html = urllib.request.urlopen(req, timeout=30).read().decode()
    tips = dict(re.findall(r'<tool-tip[^>]*\bfor="([^"]+)"[^>]*>([^<]*)</tool-tip>', html))
    days = []
    for td in re.findall(r'<td[^>]*ContributionCalendar-day[^>]*>', html):
        date = re.search(r'data-date="([^"]+)"', td)
        cid = re.search(r'\bid="([^"]+)"', td)
        if not date:
            continue
        m = re.match(r"(\d+)", tips.get(cid.group(1) if cid else "", ""))
        days.append({"date": date.group(1), "count": int(m.group(1)) if m else 0})
    if not days:
        raise SystemExit("no calendar cells found -- GitHub markup may have changed")
    return sorted(days, key=lambda d: d["date"])


def streaks(days):
    longest = run = 0
    l_span = (None, None)
    for i, d in enumerate(days):
        run = run + 1 if d["count"] else 0
        if run > longest:
            longest, l_span = run, (days[i - run + 1]["date"], d["date"])
    i = len(days) - 1 - (days[-1]["count"] == 0)  # today isn't over yet
    end = i
    while i >= 0 and days[i]["count"]:
        i -= 1
    cur = end - i
    c_span = (days[i + 1]["date"], days[end]["date"]) if cur else (None, None)
    return (cur, *c_span), (longest, *l_span)


def build(days):
    total = sum(d["count"] for d in days)
    active = sum(1 for d in days if d["count"])
    cur, lng = streaks(days)
    monthly = {}
    for d in days:
        monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["count"]
    return {
        "total": total, "active": active, "avg": round(total / active, 1) if active else 0,
        "current": cur, "longest": lng, "best": max(days, key=lambda d: d["count"]),
        "monthly": sorted(monthly.items())[-12:], "days": days,
    }


# ---- shared chrome ---------------------------------------------------------
def window(w, h, title):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">',
        f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG2}"/>'
        f'<stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
        f'<rect width="{w}" height="{h}" rx="12" fill="url(#bg)"/>',
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" fill="none" stroke="{FRAME}"/>',
        f'<line x1="0" y1="30" x2="{w}" y2="30" stroke="{FRAME}"/>',
    ]
    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{20 + i*16}" cy="15" r="5" fill="{dot}"/>')
    parts.append(f'<text x="{w/2}" y="19" fill="{MUTED}" font-size="12" text-anchor="middle">{PROMPT}: {title}</text>')
    return parts


def short(d):
    d = datetime.date.fromisoformat(d)
    return f"{d:%b} {d.day}"


# ---- heatmap ---------------------------------------------------------------
def level(n):
    return next(i for i, cap in enumerate([0, 5, 15, 30, 50, 10**9]) if n <= cap)


def heatmap(data):
    days = data["days"]
    cell, step, pad, left, top = 12, 15, 22, 30, 50
    lead = (datetime.date.fromisoformat(days[0]["date"]).weekday() + 1) % 7  # sunday = row 0
    n_cols = (lead + len(days) + 6) // 7
    w = pad + left + n_cols * step + pad
    h = top + 7 * step + 88 + pad
    parts = window(w, h, "~/contributions --graph")
    parts.insert(1, '<style>.c{opacity:0;animation:cell .42s cubic-bezier(.2,.8,.2,1) both}'
                    '@keyframes cell{0%{opacity:0;transform:translateY(-6px)}100%{opacity:1;transform:none}}'
                    '@media (prefers-reduced-motion:reduce){.c{animation:none;opacity:1}}</style>')
    seen = set()
    for i, d in enumerate(days):
        col, row = divmod(lead + i, 7)
        date = datetime.date.fromisoformat(d["date"])
        if date.day <= 7 and (date.year, date.month) not in seen and row == 0:
            seen.add((date.year, date.month))
            parts.append(f'<text x="{pad + left + col*step}" y="44" fill="{MUTED}" font-size="10">{date:%b}</text>')
        n = d["count"]
        parts.append(f'<rect class="c" x="{pad + left + col*step}" y="{top + row*step}" width="{cell}" height="{cell}" '
                     f'rx="2.5" fill="{PALETTE[level(n)]}" style="animation-delay:{col*.018 + row*.045:.3f}s">'
                     f'<title>{d["date"]}: {n} contribution{"s" * (n != 1)}</title></rect>')
    for row, name in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        parts.append(f'<text x="{pad}" y="{top + row*step + 9.4:.1f}" fill="{MUTED}" font-size="9">{name}</text>')

    ly = top + 7 * step + 6
    lx = w - pad - (len(PALETTE) * cell + 34)
    parts.append(f'<text x="{lx - 6}" y="{ly + 9.6}" fill="{MUTED}" font-size="10" text-anchor="end">Less</text>')
    for i, color in enumerate(PALETTE):
        parts.append(f'<rect x="{lx + i*cell}" y="{ly}" width="11" height="11" rx="2.2" fill="{color}"/>')
    parts.append(f'<text x="{lx + len(PALETTE)*cell + 4}" y="{ly + 9.6}" fill="{MUTED}" font-size="10">More</text>')

    sy = ly + cell + 14
    parts.append(f'<line x1="0" y1="{sy}" x2="{w}" y2="{sy}" stroke="{FRAME}" stroke-opacity="0.6"/>')
    cur, lng, best = data["current"], data["longest"], data["best"]
    parts.append(f'<text x="{pad}" y="{sy + 24}" font-size="13" fill="{GREEN}"><tspan font-weight="700">{data["total"]:,}</tspan>'
                 f'<tspan fill="{MUTED}"> contributions in the last year</tspan></text>')
    parts.append(f'<text x="{w - pad}" y="{sy + 24}" font-size="12" fill="{MUTED}" text-anchor="end">'
                 f'{days[0]["date"]} &#8594; {days[-1]["date"]}</text>')
    parts.append(f'<text x="{pad}" y="{sy + 48}" font-size="13" fill="{MUTED}">current streak '
                 f'<tspan fill="{ACCENT}" font-weight="700">{cur[0]} days</tspan>   &#183;   longest '
                 f'<tspan fill="{ACCENT}" font-weight="700">{lng[0]} days</tspan></text>')
    parts.append(f'<text x="{w - pad}" y="{sy + 48}" font-size="12" fill="{MUTED}" text-anchor="end">best day '
                 f'<tspan fill="{GOLD}" font-weight="700">{best["count"]}</tspan> on {best["date"]}</text>')
    return "".join(parts + ["</svg>"])


# ---- stats card (same 840x880 canvas as the ascii portrait) ----------------
def stats(data):
    W, H, PAD, GAP, TILE_H, FRAMES = 840, 880, 20, 16, 150, 16
    tile_w = (W - PAD * 2 - GAP) / 2
    tiles_top = 54
    chart_top = tiles_top + 3 * TILE_H + 3 * GAP
    cur, lng, best = data["current"], data["longest"], data["best"]
    n = len(data["days"])
    span = lambda s: f"{short(s[1])} – {short(s[2])}" if s[0] else "—"
    tiles = [
        ("current streak", cur[0], " days", span(cur), GREEN),
        ("longest streak", lng[0], " days", span(lng), INK),
        ("contributions", data["total"], "", "in the last year", INK),
        ("active days", data["active"], f" / {n}", f'{data["active"] / n:.0%} of the year', INK),
        ("best day", best["count"], "", short(best["date"]), INK),
        ("avg / active day", data["avg"], "", "contributions", INK),
    ]
    parts = window(W, H, "~$ ./stats.sh")
    parts.insert(1, '<style>.t{opacity:0;animation:in .45s ease-out both}'
                    '@keyframes in{0%{opacity:0;transform:translateY(14px)}100%{opacity:1;transform:none}}'
                    '.b{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow .6s ease-out both}'
                    '@keyframes grow{to{transform:scaleY(1)}}'
                    '@media (prefers-reduced-motion:reduce){.t,.b{opacity:1!important;transform:none!important;animation:none!important}}</style>')
    for i, (label, value, suffix, caption, color) in enumerate(tiles):
        x = PAD + (i % 2) * (tile_w + GAP)
        y = tiles_top + (i // 2) * (TILE_H + GAP)
        start = i * 0.15
        parts.append(f'<g class="t" style="animation-delay:{start:.2f}s">'
                     f'<rect x="{x:.1f}" y="{y}" width="{tile_w:.1f}" height="{TILE_H}" rx="10" fill="{TILE}" stroke="{FRAME}"/>'
                     f'<text x="{x+24:.1f}" y="{y+40}" fill="{MUTED}" font-size="22">$ {label}</text>')
        # count-up: pre-rendered frames toggled with SMIL <set>, easing out into the real number
        for k in range(1, FRAMES + 1):
            v = value * (1 - (1 - k / FRAMES) ** 3)
            on = start + 0.27 + 1.2 * (k - 1) / FRAMES
            anim = f'<set attributeName="opacity" to="1" begin="{on:.3f}s"/>'
            if k < FRAMES:
                anim += f'<set attributeName="opacity" to="0" begin="{on + 1.2 / FRAMES:.3f}s"/>'
            num = f"{v:,.1f}" if isinstance(value, float) else f"{round(v):,}"
            parts.append(f'<text x="{x+24:.1f}" y="{y+100}" opacity="0" font-size="54" font-weight="700" fill="{color}">'
                         f'{num}<tspan font-size="24" font-weight="400" fill="{MUTED}">{suffix}</tspan>{anim}</text>')
        parts.append(f'<text x="{x+24:.1f}" y="{y+132}" fill="{MUTED}" font-size="20">{caption}</text></g>')

    monthly = data["monthly"]
    bar_start = 0.15 * 6 + 0.4
    chart_h = H - PAD - chart_top
    parts.append(f'<g class="t" style="animation-delay:{bar_start - 0.3:.2f}s">'
                 f'<rect x="{PAD}" y="{chart_top}" width="{W - 2*PAD}" height="{chart_h}" rx="10" fill="{TILE}" stroke="{FRAME}"/>'
                 f'<text x="{PAD+24}" y="{chart_top+40}" fill="{MUTED}" font-size="22">$ contributions / month</text></g>')
    top, bot = chart_top + 64, chart_top + chart_h - 40
    slot = (W - 2 * PAD - 48) / len(monthly)
    bw = slot * 0.62
    peak = max(t for _, t in monthly) or 1
    for i, (month, total) in enumerate(monthly):
        bh = max(2, (bot - top) * total / peak)
        bx = PAD + 24 + i * slot + (slot - bw) / 2
        delay = bar_start + i * 0.06
        parts.append(f'<rect class="b" x="{bx:.1f}" y="{bot - bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="3" '
                     f'fill="{GREEN if total == peak else BAR}" style="animation-delay:{delay:.2f}s"/>')
        parts.append(f'<text x="{bx + bw/2:.1f}" y="{bot + 28}" fill="{MUTED}" font-size="18" text-anchor="middle">'
                     f'{datetime.date.fromisoformat(month + "-01"):%b}'[:1] + '</text>')
        if total == peak:
            parts.append(f'<text class="t" style="animation-delay:{delay + 0.6:.2f}s" x="{bx + bw/2:.1f}" y="{bot - bh - 10:.1f}" '
                         f'fill="{INK}" font-size="18" text-anchor="middle">{peak:,}</text>')
    return "".join(parts + ["</svg>"])


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    data = build(fetch_days())
    assert data["current"][0] <= data["longest"][0] and data["total"] >= data["best"]["count"]
    for name, body in [("data.json", json.dumps(data, indent=1)), ("heatmap.svg", heatmap(data)), ("stats.svg", stats(data))]:
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(body)
    print(f'{data["total"]} contributions, streak {data["current"][0]}, longest {data["longest"][0]}')
