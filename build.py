"""Build the static handbook site (docs/) from content/*.md.

Usage:  python build.py
Requires: pip install markdown
Brand name and repo live in site.json ({{BRAND}} and {{REPO}} placeholders in content).
"""
import json, re, html
from pathlib import Path
import markdown

ROOT = Path(__file__).parent
CFG = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
OUT = ROOT / "docs"
OUT.mkdir(exist_ok=True)


def parse(path):
    raw = path.read_text(encoding="utf-8")
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
        raw = raw[m.end():]
    raw = raw.replace("{{BRAND}}", CFG["brand"]).replace("{{REPO}}", CFG["repo"])
    return meta, raw


def render_md(text):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc"],
                           extension_configs={"toc": {"permalink": False}})
    out = md.convert(text)
    out = out.replace("<li>[ ] ", '<li class="task"><span class="box"></span>')
    out = out.replace("<li>[x] ", '<li class="task done"><span class="box"></span>')
    out = re.sub(r"<li>\s*<p>\[ \] ", '<li class="task"><p><span class="box"></span>', out)
    out = out.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
    return out


pages = []
for p in sorted((ROOT / "content").glob("*.md")):
    meta, body = parse(p)
    slug = "index" if p.stem.startswith("00") else p.stem
    pages.append({"slug": slug, "title": meta.get("title", p.stem), "order": int(meta.get("order", 99)), "body": body})
pages.sort(key=lambda x: x["order"])

CSS = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
(OUT / "style.css").write_text(CSS, encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")

TEMPLATE = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · {brand} {site_title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css"></head>
<body>
<header class="top"><a class="brand" href="index.html">{brand}</a><span class="sub">{site_title}</span>
<button class="menu" onclick="document.body.classList.toggle('nav-open')" aria-label="Menu">Menu</button></header>
<div class="wrap">
<nav class="side">{nav}<p class="meta">Cập nhật {updated}<br><a href="https://github.com/{repo}">Mã nguồn trên GitHub</a></p></nav>
<main><article>{body}</article>
<div class="pager">{prev}{next}</div>
<footer>{brand} · {tagline}</footer></main></div>
</body></html>"""

for i, pg in enumerate(pages):
    nav = "".join(
        f'<a class="{"on" if q["slug"] == pg["slug"] else ""}" href="{q["slug"]}.html"><span>{q["order"]:02d}</span>{html.escape(q["title"])}</a>'
        for q in pages)
    prev = f'<a class="prev" href="{pages[i-1]["slug"]}.html">← {html.escape(pages[i-1]["title"])}</a>' if i > 0 else "<span></span>"
    nxt = f'<a class="next" href="{pages[i+1]["slug"]}.html">{html.escape(pages[i+1]["title"])} →</a>' if i < len(pages) - 1 else "<span></span>"
    doc = TEMPLATE.format(title=html.escape(pg["title"]), brand=html.escape(CFG["brand"]), site_title=html.escape(CFG["title"]),
                          nav=nav, body=render_md(pg["body"]), prev=prev, next=nxt, updated=CFG["updated"],
                          repo=CFG["repo"], tagline=html.escape(CFG["tagline"]))
    (OUT / f'{pg["slug"]}.html').write_text(doc, encoding="utf-8")
print(f"Built {len(pages)} pages into {OUT}")
