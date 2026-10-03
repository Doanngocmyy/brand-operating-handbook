"""Build the static handbook site (docs/) from content/*.md + site_map.py.

Usage:  python build.py
Requires: pip install markdown
- Navigation, role/task routes, lifecycle map, SOP control panels, source-of-truth and launch-blocker
  callouts come from site_map.py (one place to edit).
- Placeholders that must sit on their own line in a page:
    {{SVG:a}} {{PANEL:sop-a}} {{ROLE_CARDS}} {{TASK_CARDS}} {{LIFECYCLE}} {{RHYTHM}} {{ROLE_GUIDES}}
    {{TASK_ROUTES}} {{CASE_ROUTER}} {{SOT:order,case}} {{SOT_TABLE}} {{BLOCKER:gst}} {{BLOCKERS}} {{BLOCKER_STRIP}}
  Inline: {{BLK:gst}} (launch-blocker pill), {{BRAND}}, {{REPO}}.
- Old page URLs get redirect stubs so existing links keep working.
"""
import html
import json
import re
from pathlib import Path

import markdown

import site_map as SM

ROOT = Path(__file__).parent
CFG = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
OUT = ROOT / "docs"
OUT.mkdir(exist_ok=True)
E = html.escape
REPO = CFG["repo"]
RAW = f"https://github.com/{REPO}/raw/main/"
LINKS = {
    "TRACKER": RAW + "templates/SOP-Tracker.xlsx",
    "DOCS": RAW + "templates/Mau_chung_tu_NCC.xlsx",
    "SHEET": CFG.get("sot_sheet_url") or RAW + "templates/SOP-Tracker.xlsx",
    "COST": "cong-cu-bieu-mau.html#source-of-truth",
}


def url(u):
    """Resolve a routing link: tokens, repo templates, or page#anchor."""
    if u in LINKS:
        return LINKS[u]
    if u.startswith("templates/"):
        return RAW + u
    return u


def role(code):
    return f'<span class="r {SM.ROLE_COLOURS.get(code, "")}">{E(code)}</span>'


def roles(text):
    """'SRC → OPS' -> chips, keeps the arrow / extra words."""
    return re.sub(r"\b(CX|SRC|LOG|OPS|MKT|FIN|CEO)\b", lambda m: role(m.group(1)), E(text))


# ----------------------------------------------------------------------------- components
def c_svg(name):
    svg = (ROOT / "assets" / "sop" / f"{name}.svg").read_text(encoding="utf-8").replace("\n\n", "\n")
    return (f'<div class="swim" tabindex="0" role="region" aria-label="Swimlane, kéo ngang để xem hết">{svg}</div>\n'
            f'<p class="swim-cap">Kéo ngang để xem hết · <a href="sop/{name}.svg" target="_blank" rel="noopener">Mở bản lớn / in ↗</a></p>')


def c_panel(key):
    rows = "".join(
        f'<div class="pr"><dt>{E(k)}</dt><dd>{v.replace("{TRACKER}", LINKS["TRACKER"]).replace("{DOCS}", LINKS["DOCS"])}</dd></div>'
        for k, v in SM.PANELS[key])
    return f'<section class="panel" id="control-panel" aria-label="SOP control panel"><h2 class="panel-h">SOP control panel</h2><dl>{rows}</dl></section>'


def c_role_cards():
    cards = []
    for r in SM.ROLES:
        cards.append(
            f'<a class="card role-card" href="tim-theo-vai-tro.html#{r["code"].lower()}">'
            f'<span class="rc-top">{role(r["code"])}<span class="rc-p">{E(r["p"])}</span></span>'
            f'<strong>{E(r["name"])}</strong><span class="muted">{E(r["vn"])}</span>'
            f'<span class="rc-go">Bắt đầu ở đây →</span></a>')
    return f'<div class="grid roles">{"".join(cards)}</div>'


def c_task_cards():
    out = []
    for t in SM.TASKS:
        label, href = t["go"]
        red = " is-red" if t.get("red") else ""
        out.append(
            f'<a class="card task-card{red}" href="{url(href)}">'
            f'<span class="tk-ic" aria-hidden="true">{E(t["icon"])}</span>'
            f'<span class="tk-body"><strong>{E(t["title"])}</strong>'
            f'<span class="tk-meta">{roles(t["owner"])} · {E(t["sla"])}</span>'
            f'<span class="tk-go">{E(label)} →</span></span></a>')
    return f'<div class="grid tasks">{"".join(out)}</div><p class="more"><a href="tim-theo-su-kien.html">Xem bảng định tuyến đầy đủ: bằng chứng, tracker, biểu mẫu →</a></p>'


def c_lifecycle():
    items = []
    for i, s in enumerate(SM.STAGES):
        exc = "".join(
            f'<a class="exc" href="{url(h)}"><span aria-hidden="true">↳</span> {E(t)} <b>{E(c)}</b></a>' for t, c, h in s["exc"])
        own = " ".join(role(o) for o in s["owner"])
        items.append(
            f'<li class="stage"><a class="st-link" href="sop-a-don-chuan.html#{s["code"].lower()}" aria-label="{s["code"]} {E(s["en"])}: mở SOP-A">'
            f'<span class="st-code">{s["code"]}</span><span class="st-name">{E(s["name"])}</span>'
            f'<span class="st-en">{E(s["en"])}</span>'
            f'<span class="st-own">{own}</span>'
            f'<span class="st-row"><i>SLA</i>{E(s["sla"])}</span>'
            f'<span class="st-row"><i>Cổng</i>{E(s["gate"])}</span>'
            f'<span class="st-row"><i>Khách</i>{E(s["cust"])}</span>'
            f'<span class="st-status">→ <span class="s">{E(s["status"])}</span></span></a>'
            f'<div class="st-exc">{exc}</div></li>')
    legend = ('<p class="lc-legend"><span class="s">30</span> trạng thái sau khi qua cổng · '
              '<span class="exc-k">↳ đỏ</span> lối thoát ngoại lệ → SOP-B · bấm vào một giai đoạn để mở đúng bước</p>')
    return f'<div class="lifecycle" role="region" aria-label="Order lifecycle S1–S8"><ol>{"".join(items)}</ol></div>{legend}'


def c_rhythm():
    rows = "".join(
        f'<a class="rh" href="{url(h)}"><span class="rh-t">{E(t)}</span><span class="rh-b"><strong>{E(a)}</strong>'
        f'<span class="muted">{E(b)}</span></span></a>' for t, a, b, h in SM.RHYTHM)
    links = (f'<p class="rh-links"><a href="{LINKS["SHEET"]}">Dashboard / tracker</a> · <a href="kpi-sla-nhip.html#flags">Cờ SLA</a> · '
             f'<a href="kpi-sla-nhip.html#weekly-report">Mẫu báo cáo tuần</a> · <a href="kpi-sla-nhip.html#checklist">Checklist theo vị trí</a></p>')
    return f'<div class="rhythm">{rows}</div>{links}'


def _links(items):
    return "".join(f'<li><a href="{url(h)}">{E(t)}</a></li>' for t, h in items)


def c_role_guides():
    nav = " ".join(f'<a class="chip-link" href="#{r["code"].lower()}">{role(r["code"])} {E(r["name"])}</a>' for r in SM.ROLES)
    out = [f'<nav class="jump" aria-label="Chọn vị trí">{nav}</nav>']
    for r in SM.ROLES:
        out.append(
            f'<section class="guide" id="{r["code"].lower()}">'
            f'<header class="g-head">{role(r["code"])}<h2>{E(r["name"])} <span class="muted">· {E(r["p"])} {E(r["vn"])}</span></h2></header>'
            f'<p class="g-purpose">{E(r["purpose"])}</p>'
            f'<div class="g-grid">'
            f'<div class="g-box"><h3>Mở mỗi ngày</h3><ul>{_links(r["daily_open"])}</ul></div>'
            f'<div class="g-box"><h3>Nhịp / checklist</h3><ul>{"".join(f"<li>{E(c)}</li>" for c in r["checklist"])}</ul></div>'
            f'<div class="g-box"><h3>Giai đoạn phụ trách</h3><ul>{_links(r["stages"])}</ul></div>'
            f'<div class="g-box"><h3>Đọc một lần khi nhận việc</h3><ul>{_links(r["onboarding"])}</ul></div>'
            f'<div class="g-box"><h3>Mức duyệt · leo thang</h3><p>{E(r["limit"])}</p></div>'
            f'<div class="g-box"><h3>Tracker · công cụ · biểu mẫu</h3><ul>{_links(r["tools"])}</ul></div>'
            f'</div>'
            f'<div class="g-never"><h3>Không bao giờ</h3><ul>{"".join(f"<li>{E(n)}</li>" for n in r["never"])}</ul></div>'
            f'<p class="g-src">Nguồn: <a href="vai-tro-quyen-han.html#raci">RACI</a> · <a href="kpi-sla-nhip.html#checklist">Checklist hằng ngày</a> · <a href="#top">↑ Lên đầu</a></p>'
            f'</section>')
    return "\n".join(out)


def c_task_routes():
    rows = []
    for t in SM.TASKS:
        label, href = t["go"]
        more = " · ".join(f'<a href="{url(h)}">{E(x)}</a>' for x, h in t["more"])
        red = ' class="is-red"' if t.get("red") else ""
        rows.append(
            f'<tr{red}><th scope="row">{E(t["title"])}<span class="muted en">{E(t["en"])}</span></th>'
            f'<td><a class="go" href="{url(href)}">{E(label)} →</a></td><td>{roles(t["owner"])}</td><td>{E(t["sla"])}</td>'
            f'<td>{E(t["evidence"])}</td><td>{E(t["tracker"])}</td><td>{more}</td></tr>')
    return ('<div class="tbl routes"><table><thead><tr><th>Việc đang xảy ra</th><th>Mở ngay</th><th>Chủ</th><th>SLA</th>'
            '<th>Bằng chứng</th><th>Tracker</th><th>Liên quan</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>")


def c_case_router():
    out = []
    for code, name, sign, flow, anchor in SM.CASES:
        out.append(
            f'<div class="card case-card"><a class="cc-main" href="#{code.lower()}"><span class="cc-code">{code}</span>'
            f'<strong>{E(name)}</strong><span class="muted">{E(sign)}</span></a>'
            f'<a class="cc-flow" href="#{anchor}">Luồng {E(flow)} →</a></div>')
    return f'<div class="grid cases">{"".join(out)}</div>'


def c_sot(keys):
    items = []
    for k in keys.split(","):
        info, system, link = SM.SOT[k.strip()]
        items.append(f'<li><span class="sot-i">{E(info)}</span><a href="{url(link)}">{E(system)}</a></li>')
    return (f'<aside class="sot" aria-label="Source of truth"><span class="sot-h">Source of truth</span>'
            f'<ul>{"".join(items)}</ul></aside>')


def c_sot_table():
    rows = "".join(f'<tr><td>{E(i)}</td><td><a href="{url(l)}">{E(s)}</a></td></tr>' for i, s, l in SM.SOT.values())
    return f'<div class="tbl"><table><thead><tr><th>Thông tin</th><th>Bản ghi gốc (source of truth)</th></tr></thead><tbody>{rows}</tbody></table></div>'


def c_blocker(key):
    t, d, owner, href = SM.BLOCKERS[key]
    return (f'<aside class="blocker" id="blk-{key}" role="note"><span class="badge b-block">Launch blocker</span>'
            f'<strong>{E(t)}</strong><p>{E(d)} Chủ: {roles(owner)} · <a href="lo-trinh-90-ngay.html#blk-{key}">Theo dõi trong Launch blockers →</a></p></aside>')


def c_blockers():
    rows = "".join(
        f'<tr id="blk-{k}"><td><span class="badge b-block">Mở</span></td><td><strong>{E(t)}</strong><br><span class="muted">{E(d)}</span></td>'
        f'<td>{roles(o)}</td><td><a href="{h}">Xem →</a></td></tr>' for k, (t, d, o, h) in SM.BLOCKERS.items())
    return f'<div class="tbl blockers"><table><thead><tr><th>Trạng thái</th><th>Việc chưa xong</th><th>Chủ</th><th>Nơi ảnh hưởng</th></tr></thead><tbody>{rows}</tbody></table></div>'


def c_blocker_strip():
    items = " · ".join(f'<a href="lo-trinh-90-ngay.html#blk-{k}">{E(t)}</a>' for k, (t, *_r) in SM.BLOCKERS.items())
    return (f'<aside class="strip" role="note"><span class="badge b-block">{len(SM.BLOCKERS)} launch blockers</span>'
            f'<span>{items}</span></aside>')


def c_blk_inline(m):
    k = m.group(1)
    return f'<a class="blk" href="lo-trinh-90-ngay.html#blk-{k}" title="Launch blocker: {E(SM.BLOCKERS[k][0])}">⚠ {E(SM.BLOCKERS[k][0])}</a>'


BLOCK = {
    "ROLE_CARDS": c_role_cards, "TASK_CARDS": c_task_cards, "LIFECYCLE": c_lifecycle, "RHYTHM": c_rhythm,
    "ROLE_GUIDES": c_role_guides, "TASK_ROUTES": c_task_routes, "CASE_ROUTER": c_case_router,
    "SOT_TABLE": c_sot_table, "BLOCKERS": c_blockers, "BLOCKER_STRIP": c_blocker_strip,
}
BLOCK_ARG = {"SVG": c_svg, "PANEL": c_panel, "SOT": c_sot, "BLOCKER": c_blocker}


def expand(raw):
    raw = raw.replace("{{BRAND}}", CFG["brand"]).replace("{{REPO}}", REPO)
    raw = re.sub(r"\{\{BLK:(\w+)\}\}", c_blk_inline, raw)
    raw = re.sub(r"^\{\{(\w+)\}\}$", lambda m: "\n" + BLOCK[m.group(1)]() + "\n", raw, flags=re.M)
    raw = re.sub(r"^\{\{(\w+):([\w,-]+)\}\}$", lambda m: "\n" + BLOCK_ARG[m.group(1)](m.group(2)) + "\n", raw, flags=re.M)
    return raw


# ----------------------------------------------------------------------------- pages
def parse(path):
    raw = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
        raw = raw[m.end():]
    return meta, raw


def render_md(text):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "attr_list"])
    out = md.convert(text)
    out = out.replace("<li>[ ] ", '<li class="task"><span class="box"></span>')
    out = out.replace("<li>[x] ", '<li class="task done"><span class="box"></span>')
    out = re.sub(r"<li>\s*<p>\[ \] ", '<li class="task"><p><span class="box"></span>', out)
    out = re.sub(r"<table>", '<div class="tbl"><table>', out)
    out = out.replace("</table>", "</table></div>").replace("</table></div></div>", "</table></div>")
    return out


SECTION_NAME = dict(SM.SECTIONS)
SECTION_HOME = {"start": "index", "run": "sop-a-don-chuan", "std": "chuan-san-pham", "mgmt": "vai-tro-quyen-han"}
WIDE = {"index", "tim-theo-vai-tro", "tim-theo-su-kien"}

pages = []
for slug, section, nav, src, old in SM.PAGES:
    meta, body = parse(ROOT / "content" / src)
    pages.append(dict(slug=slug, section=section, nav=nav, old=old, title=meta.get("title", nav),
                      badges=[b.strip() for b in meta.get("badges", "").split(",") if b.strip()],
                      body=body))

CSS = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
(OUT / "style.css").write_text(CSS, encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")
(OUT / "sop").mkdir(exist_ok=True)
for f in (ROOT / "assets" / "sop").glob("*.svg"):
    (OUT / "sop" / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")


CUR = ' aria-current="page" class="on"'
CUR_A = ' aria-current="page"'
CUR_S = ' aria-current="true" class="on"'


def sidebar(cur):
    parts = []
    for key, name in SM.SECTIONS:
        links = "".join(
            f'<a href="{p["slug"]}.html"{CUR if p["slug"] == cur["slug"] else ""}>{E(p["nav"])}</a>'
            for p in pages if p["section"] == key)
        parts.append(f'<div class="nav-group"><p class="nav-h">{E(name)}</p>{links}</div>')
    about = " · ".join(f'<a href="{p["slug"]}.html"{CUR_A if p["slug"] == cur["slug"] else ""}>{E(p["nav"])}</a>'
                       for p in pages if p["section"] == "about")
    parts.append(f'<p class="meta">About: {about}<br>Cập nhật {E(CFG["updated"])} · <a href="https://github.com/{REPO}">GitHub</a></p>')
    return "".join(parts)


def topnav(cur):
    sec = cur["section"] if cur["section"] in SECTION_HOME else None
    return "".join(
        f'<a href="{SECTION_HOME[k]}.html"{CUR_S if k == sec else ""}>{E(n)}</a>'
        for k, n in SM.SECTIONS)


def header_bits(p):
    crumb = SECTION_NAME.get(p["section"], "About")
    badges = "".join(f'<span class="badge {SM.BADGES[b][1]}">{E(SM.BADGES[b][0])}</span>' for b in p["badges"])
    return crumb, (f'<div class="badges">{badges}</div>' if badges else "")


SCRIPT = """<script>
function openTarget(){var id=decodeURIComponent(location.hash.slice(1));if(!id)return;var el=document.getElementById(id);if(!el)return;var d=el.closest("details")||(el.tagName==="DETAILS"?el:null);if(d){d.open=true;}}
window.addEventListener("hashchange",openTarget);openTarget();
</script>"""

TEMPLATE = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · {brand} {site_title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css"></head>
<body class="{body_class}" id="top">
<a class="skip" href="#main">Bỏ qua tới nội dung</a>
<header class="top"><a class="brand" href="index.html">{brand}<span class="sub">Operating System</span></a>
<nav class="topnav" aria-label="Khu vực">{topnav}</nav>
<button class="menu" type="button" aria-expanded="false" aria-controls="side" onclick="var o=document.body.classList.toggle('nav-open');this.setAttribute('aria-expanded',o)">Menu</button></header>
<div class="wrap">
<nav class="side" id="side" aria-label="Mục lục">{nav}</nav>
<main id="main"><article><p class="crumb">{crumb}</p>{body}</article>
<div class="pager">{prev}{next}</div>
<footer>{brand} · {tagline}</footer></main></div>
{script}
</body></html>"""

ordered = [p for p in pages if p["section"] != "about"]
for p in pages:
    body = render_md(expand(p["body"]))
    crumb, badges = header_bits(p)
    body = re.sub(r"(</h1>)", r"\1" + badges.replace("\\", "\\\\"), body, count=1)
    seq = ordered if p in ordered else []
    i = seq.index(p) if seq else -1
    prev = f'<a class="prev" href="{seq[i-1]["slug"]}.html">← {E(seq[i-1]["nav"])}</a>' if seq and i > 0 else "<span></span>"
    nxt = f'<a class="next" href="{seq[i+1]["slug"]}.html">{E(seq[i+1]["nav"])} →</a>' if seq and i < len(seq) - 1 else "<span></span>"
    doc = TEMPLATE.format(title=E(p["nav"]), brand=E(CFG["brand"]), site_title=E(CFG["title"]), nav=sidebar(p),
                          topnav=topnav(p), crumb=E(crumb), body=body, prev=prev, next=nxt,
                          tagline=E(CFG["tagline"]), script=SCRIPT, body_class="wide" if p["slug"] in WIDE else "")
    (OUT / f'{p["slug"]}.html').write_text(doc, encoding="utf-8")
    if p["old"]:
        new = f'{p["slug"]}.html'
        (OUT / f'{p["old"]}.html').write_text(
            f'<!doctype html><meta charset="utf-8"><title>Đã chuyển</title><meta name="robots" content="noindex">'
            f'<meta http-equiv="refresh" content="0; url={new}"><link rel="canonical" href="{new}">'
            f'<script>location.replace("{new}"+location.hash)</script><a href="{new}">Trang đã chuyển tới {E(p["nav"])}</a>',
            encoding="utf-8")
print(f"Built {len(pages)} pages + {sum(1 for p in pages if p['old'])} redirects into {OUT}")
