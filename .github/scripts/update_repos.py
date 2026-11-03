"""Fill the <!-- REPOS:START --> ... <!-- REPOS:END --> block in README.md with my latest public repos.

Lives in .github/ because the daily design rotation replaces scripts/ on main every morning.
If today's design has no markers, the block goes before the README's last '---', or at the end.
Run `python .github/scripts/update_repos.py --selftest` to check the logic offline.
"""
import json
import os
import sys
import urllib.request

USER = os.environ.get("GH_USER", "KRISH-exe-29")
COUNT = 6
SKIP_DESC = ("Study copy", "Fork of")  # not my own work
START, END = "<!-- REPOS:START -->", "<!-- REPOS:END -->"


def fetch():
    req = urllib.request.Request(
        f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&sort=pushed",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-readme-bot"},
    )
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode())


def pick(repos):
    own = [r for r in repos
           if not r["fork"] and not r["archived"] and not r["private"]
           and r["name"].lower() != USER.lower()
           and r["description"] and not r["description"].startswith(SKIP_DESC)
           and "no code yet" not in r["description"].lower()]  # empty WIP repos
    return sorted(own, key=lambda r: r["pushed_at"], reverse=True)[:COUNT]


def cell(s):
    return s.replace("|", "\\|").replace("\n", " ").strip()


def render(repos):
    rows = [f"| [{cell(r['name'])}]({r['html_url']}) | {cell(r['description'])} | "
            f"{r['language'] or '—'} | {r['stargazers_count']} | {r['pushed_at'][:10]} |" for r in repos]
    # Dates, not "3 days ago": the block only changes when a repo does, so no empty daily commits.
    return "\n".join([
        START,
        "",
        "## Latest repos",
        "",
        "<sub>Updated automatically from GitHub by a workflow.</sub>",
        "",
        "| Repo | What it is | Language | ★ | Last push |",
        "|---|---|---|---|---|",
        *rows,
        "",
        END,
    ])


def inject(readme, block):
    if START in readme and END in readme:
        head, rest = readme.split(START, 1)
        return head + block + rest.split(END, 1)[1]
    cut = readme.rfind("\n---\n")
    if cut == -1:
        return readme.rstrip("\n") + "\n\n" + block + "\n"
    return readme[:cut] + "\n\n" + block + "\n" + readme[cut:]


def selftest():
    r = lambda name, **kw: {"name": name, "fork": False, "archived": False, "private": False,
                            "description": "d", "pushed_at": "2026-01-01T00:00:00Z", "language": "Python",
                            "stargazers_count": 0, "html_url": "u", **kw}
    got = pick([r("a"), r("b", fork=True), r(USER), r("c", description=None),
                r("d", description="Study copy of x"), r("f", description="WIP: no code yet."), r("e", pushed_at="2026-05-01T00:00:00Z")])
    assert [x["name"] for x in got] == ["e", "a"], got
    assert "a \\| b" in render([r("x", description="a | b")])
    b1, b2 = render([r("one")]), render([r("two")])
    once = inject("top\n\n---\n\nfooter\n", b1)
    assert once.index(START) < once.index("---") and once.endswith("footer\n")
    twice = inject(once, b2)
    assert "one" not in twice and twice.count(START) == 1 and twice.endswith("footer\n")
    assert inject("no rule", b1).endswith(END + "\n")
    print("selftest ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        sys.exit()
    path = sys.argv[1] if len(sys.argv) > 1 else "README.md"
    with open(path, encoding="utf-8") as f:
        old = f.read()
    new = inject(old, render(pick(fetch())))
    if new != old:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new)
    print("README updated" if new != old else "README already current")
