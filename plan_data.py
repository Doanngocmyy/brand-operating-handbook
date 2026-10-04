"""Strategy & roadmap data layer: reads plan/*.csv, validates it, renders SVG / HTML / Mermaid.

plan/ is the single source of truth for the roadmap (Gantt), objectives and KPI targets.
- build.py uses the render_* functions for the {{PLAN:...}}, {{OKR:...}}, {{KPI_DICT}}, {{YEAR_SUMMARY}} blocks.
- tools/build_plan.py validates the data and regenerates plan/README.md (Mermaid Gantt for GitHub).
Only targets and plans live here. Actual results stay in the private Google Sheet (public repo).
No third-party dependencies.
"""
import csv
import html
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).parent
PLAN = ROOT / "plan"
E = html.escape

ROLE_COLOURS = {"CX": "cx", "SRC": "src", "LOG": "log", "OPS": "ops", "MKT": "mkt", "FIN": "fin", "CEO": "ceo"}
# workstream -> (fill, stroke) as CSS variables with light-mode fallbacks (inline SVG follows the site theme)
WS_STYLE = {
    "Nền tảng": ("var(--accent-soft,#f3efe9)", "var(--accent,#6b5a45)"),
    "Sản phẩm & NCC": ("var(--green-soft,#e6f4ea)", "var(--green,#1e6b3a)"),
    "Web & nội dung": ("var(--violet-soft,#f1ebf8)", "var(--violet,#5f3b86)"),
    "Bán & tăng trưởng": ("var(--amber-soft,#fff4dc)", "var(--amber,#8a5a00)"),
    "Logistics & kho": ("var(--blue-soft,#e8f0f9)", "var(--blue,#1f5a94)"),
    "Quản trị & dữ liệu": ("var(--code,#f5f5f4)", "var(--muted,#62626a)"),
    "Mở rộng": ("var(--red-soft,#fdecea)", "var(--red,#b42318)"),
}
STATUS_VN = {"done": "Xong", "in_progress": "Đang làm", "planned": "Kế hoạch"}
LEVEL_VN = {"north_star": "North Star", "outcome": "Kết quả", "driver": "Đòn bẩy", "guardrail": "Rào chắn"}
INK, MUTED, LINE, PANEL = "var(--ink,#1d1d1f)", "var(--muted,#62626a)", "var(--line,#e5e5e7)", "var(--panel,#ffffff)"


# ----------------------------------------------------------------------------- loading
def _rows(name):
    with open(PLAN / name, encoding="utf-8", newline="") as f:
        return [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]


def _d(s):
    return date.fromisoformat(s)


def load():
    tasks = _rows("roadmap.csv")
    for t in tasks:
        t["s"], t["e"] = _d(t["start"]), _d(t["end"])
        t["deps"] = [x for x in t["depends_on"].split(";") if x]
    kpis = {r["kpi_id"]: r for r in _rows("kpi_dictionary.csv")}
    targets = _rows("kpi_targets.csv")
    for r in targets:
        r["value"] = float(r["target"])
    orders = [(r["month"], int(r["orders_target"]), r["note"]) for r in _rows("orders_plan.csv")]
    assume = {r["key"]: r["value"] for r in _rows("assumptions.csv")}
    objectives = _rows("objectives.csv")
    return dict(tasks=tasks, kpis=kpis, targets=targets, orders=orders, assume=assume, objectives=objectives)


# ----------------------------------------------------------------------------- derived numbers
def quarter_end_month(period):
    """'2027-Q2' -> '2027-06'; '2026-11' -> '2026-11'."""
    if "-Q" in period:
        y, q = period.split("-Q")
        return f"{y}-{int(q) * 3:02d}"
    return period


def north_star_plan(data):
    """Deliveries within promise per month = in_window_rate x orders placed `lag` months earlier."""
    lag = int(data["assume"]["delivery_lag_months"])
    rate = float(data["assume"]["in_window_rate"])
    o = [n for _, n, _ in data["orders"]]
    return {m: int(rate * (o[i - lag] if i >= lag else 0) + 0.5) for i, (m, _, _) in enumerate(data["orders"])}


def year_totals(data):
    aov = float(data["assume"]["aov_aud"])
    out = {}
    for m, n, _ in data["orders"]:
        y = m[:4]
        out.setdefault(y, {"orders": 0, "revenue": 0.0})
        out[y]["orders"] += n
        out[y]["revenue"] += n * aov
    return out


def quarter_totals(data):
    aov = float(data["assume"]["aov_aud"])
    out = {}
    for m, n, _ in data["orders"]:
        y, mm = m.split("-")
        key = f"{y}-Q{(int(mm) - 1) // 3 + 1}"
        out.setdefault(key, [0, 0.0])
        out[key][0] += n
        out[key][1] += n * aov
    return out


# ----------------------------------------------------------------------------- validation
def validate(data):
    """Return a list of human-readable problems (empty = clean)."""
    errs = []
    ids = {t["id"] for t in data["tasks"]}
    by_id = {x["id"]: x for x in data["tasks"]}
    for t in data["tasks"]:
        if t["e"] < t["s"]:
            errs.append(f"{t['id']}: end before start")
        if t["type"] == "milestone" and t["s"] != t["e"]:
            errs.append(f"{t['id']}: milestone must have start == end")
        if t["workstream"] not in WS_STYLE:
            errs.append(f"{t['id']}: unknown workstream '{t['workstream']}'")
        if t["status"] not in STATUS_VN:
            errs.append(f"{t['id']}: unknown status '{t['status']}'")
        if t["owner"] not in ROLE_COLOURS:
            errs.append(f"{t['id']}: unknown owner role '{t['owner']}'")
        for d in t["deps"]:
            if d not in ids:
                errs.append(f"{t['id']}: depends on unknown task {d}")
            elif by_id[d]["type"] == "milestone" and by_id[d]["e"] > t["s"]:
                errs.append(f"{t['id']}: starts {t['s']} before gate {d} on {by_id[d]['e']}")
            elif by_id[d]["s"] > t["s"]:
                errs.append(f"{t['id']}: starts {t['s']} before dependency {d} starts {by_id[d]['s']}")
        for cond in filter(None, t["gate"].split(";")):
            k = cond.split(">")[0].split("<")[0].split("=")[0]
            if k not in data["kpis"]:
                errs.append(f"{t['id']}: gate uses unknown KPI {k}")
    periods = {o["period"] for o in data["objectives"]}
    months = {m for m, _, _ in data["orders"]}
    for r in data["targets"]:
        if r["kpi_id"] not in data["kpis"]:
            errs.append(f"targets: unknown KPI {r['kpi_id']} in {r['period']}")
        if r["period"] not in periods:
            errs.append(f"targets: period {r['period']} has no objective")
    orders = {m: n for m, n, _ in data["orders"]}
    ns = north_star_plan(data)
    for r in data["targets"]:
        m = quarter_end_month(r["period"])
        if m not in months:
            errs.append(f"targets: {r['period']} outside orders_plan months")
            continue
        if r["kpi_id"] == "K01" and int(r["value"]) != orders[m]:
            errs.append(f"K01 {r['period']} = {r['value']:g} but orders_plan {m} = {orders[m]}")
        if r["kpi_id"] == "NS1" and int(r["value"]) != ns[m]:
            errs.append(f"NS1 {r['period']} = {r['value']:g} but derived plan for {m} = {ns[m]}")
    return errs


# ----------------------------------------------------------------------------- formatting helpers
def fmt_target(kpi, v):
    unit = kpi["unit"]
    num = f"{v:,.0f}" if unit == "A$" else (f"{v:g}".replace(".", ","))
    sign = "≥" if kpi["direction"] == ">=" else "≤"
    if unit == "A$":
        return f"{sign} A${num}"
    sep = "" if unit == "%" else " "
    return f"{sign} {num}{sep}{unit}"


def role_chip(code):
    return f'<span class="r {ROLE_COLOURS.get(code, "")}">{E(code)}</span>'


def _months(start, end):
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        yield date(y, m, 1)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


# ----------------------------------------------------------------------------- SVG: Gantt
def render_gantt_svg(data):
    tasks = data["tasks"]
    t0 = min(t["s"] for t in tasks).replace(day=1)
    last = max(t["e"] for t in tasks)
    t1 = (last.replace(day=28) + timedelta(days=4)).replace(day=1)  # first day of the month after
    label_w, chart_w, row_h, head_h = 300, 900, 24, 46
    days = (t1 - t0).days
    x = lambda d: label_w + (d - t0).days / days * chart_w  # noqa: E731

    rows, ws_seen = [], []
    for t in tasks:
        if t["workstream"] not in ws_seen:
            ws_seen.append(t["workstream"])
            rows.append(("ws", t["workstream"]))
        rows.append(("task", t))
    height = head_h + len(rows) * row_h + 34
    width = label_w + chart_w + 16
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
         f'font-family="Inter,system-ui,sans-serif" font-size="12" role="img" aria-label="Gantt roadmap Q4/2026 – 2027">',
         f'<rect x="0" y="0" width="{width}" height="{height}" style="fill:{PANEL}"/>']
    # quarter bands + month grid
    for i, m in enumerate(_months(t0, t1 - timedelta(days=1))):
        nxt = (m.replace(day=28) + timedelta(days=4)).replace(day=1)
        q = (m.month - 1) // 3
        if q % 2 == 0:
            o.append(f'<rect x="{x(m):.1f}" y="{head_h - 18}" width="{x(nxt) - x(m):.1f}" height="{height - head_h - 16}" '
                     f'style="fill:var(--code,#f5f5f4);opacity:.6"/>')
        o.append(f'<line x1="{x(m):.1f}" y1="{head_h - 18}" x2="{x(m):.1f}" y2="{height - 34}" style="stroke:{LINE}"/>')
        o.append(f'<text x="{(x(m) + x(nxt)) / 2:.1f}" y="{head_h - 4}" text-anchor="middle" style="fill:{MUTED}">T{m.month}</text>')
        if m.month in (1, 4, 7, 10) or i == 0:
            o.append(f'<text x="{x(m) + 3:.1f}" y="{head_h - 24}" style="fill:{INK};font-weight:600">Q{q + 1}/{m.year}</text>')
    # rows
    y = head_h
    for kind, item in rows:
        if kind == "ws":
            fill, stroke = WS_STYLE[item]
            o.append(f'<rect x="8" y="{y + 6}" width="10" height="10" rx="2" style="fill:{fill};stroke:{stroke}"/>')
            o.append(f'<text x="24" y="{y + 15}" style="fill:{INK};font-weight:700;font-size:12.5px">{E(item)}</text>')
            o.append(f'<line x1="8" y1="{y + row_h - 1}" x2="{width - 8}" y2="{y + row_h - 1}" style="stroke:{LINE}"/>')
        else:
            t = item
            fill, stroke = WS_STYLE[t["workstream"]]
            label = f'{t["id"]} · {t["task"]}'
            if len(label) > 40:
                label = label[:39] + "…"
            o.append(f'<text x="24" y="{y + 15}" style="fill:{INK}"><title>{E(t["task"])} ({E(t["owner"])}, '
                     f'{t["s"]:%d/%m/%Y} – {t["e"]:%d/%m/%Y}, {STATUS_VN[t["status"]]})</title>{E(label)}</text>')
            o.append(f'<text x="{label_w - 8}" y="{y + 15}" text-anchor="end" style="fill:{MUTED};font-size:11px">{E(t["owner"])}</text>')
            if t["type"] == "milestone":
                cx, cy = x(t["s"]), y + row_h / 2
                o.append(f'<path d="M{cx:.1f} {cy - 7:.1f} L{cx + 7:.1f} {cy:.1f} L{cx:.1f} {cy + 7:.1f} L{cx - 7:.1f} {cy:.1f} Z" '
                         f'style="fill:{stroke}"><title>{E(t["task"])} · {t["s"]:%d/%m/%Y}</title></path>')
            else:
                x0, x1 = x(t["s"]), x(t["e"] + timedelta(days=1))
                solid = t["status"] in ("done", "in_progress")
                style = f"fill:{stroke if solid else fill};stroke:{stroke}"
                o.append(f'<rect x="{x0:.1f}" y="{y + 5}" width="{max(x1 - x0, 3):.1f}" height="{row_h - 10}" rx="4" style="{style}">'
                         f'<title>{E(t["task"])} · {t["s"]:%d/%m} – {t["e"]:%d/%m/%Y} · {STATUS_VN[t["status"]]}</title></rect>')
        y += row_h
    # as-of line
    asof = _d(data["assume"]["as_of"])
    if t0 <= asof <= t1:
        ax = x(asof)
        o.append(f'<line x1="{ax:.1f}" y1="{head_h - 18}" x2="{ax:.1f}" y2="{height - 34}" style="stroke:var(--red,#b42318);stroke-width:1.5;stroke-dasharray:4 3"/>')
        o.append(f'<text x="{ax + 4:.1f}" y="{height - 38}" style="fill:var(--red,#b42318);font-size:11px">Lập kế hoạch {asof:%d/%m/%Y}</text>')
    # legend
    ly = height - 14
    o.append(f'<rect x="24" y="{ly - 9}" width="22" height="10" rx="3" style="fill:{MUTED}"/><text x="52" y="{ly}" style="fill:{MUTED};font-size:11px">Đang làm / xong</text>')
    o.append(f'<rect x="160" y="{ly - 9}" width="22" height="10" rx="3" style="fill:var(--code,#f5f5f4);stroke:{MUTED}"/><text x="188" y="{ly}" style="fill:{MUTED};font-size:11px">Kế hoạch</text>')
    o.append(f'<path d="M270 {ly - 9} L276 {ly - 4} L270 {ly + 1} L264 {ly - 4} Z" style="fill:{MUTED}"/><text x="284" y="{ly}" style="fill:{MUTED};font-size:11px">Cổng quyết định (milestone)</text>')
    o.append("</svg>")
    return "\n".join(o)


# ----------------------------------------------------------------------------- SVG: orders plan + North Star
def render_orders_svg(data):
    rows = data["orders"]
    ns = north_star_plan(data)
    w, h, left, right, top, bottom = 1060, 300, 46, 16, 26, 44
    cw, ch = w - left - right, h - top - bottom
    vmax = max(n for _, n, _ in rows)
    vmax = int((vmax // 20 + 1) * 20)
    bw = cw / len(rows)
    y = lambda v: top + ch - v / vmax * ch  # noqa: E731
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="Inter,system-ui,sans-serif" '
         f'font-size="11.5" role="img" aria-label="Kế hoạch đơn hàng theo tháng và North Star">',
         f'<rect width="{w}" height="{h}" style="fill:{PANEL}"/>']
    for g in range(0, vmax + 1, 20):
        o.append(f'<line x1="{left}" x2="{w - right}" y1="{y(g):.1f}" y2="{y(g):.1f}" style="stroke:{LINE}"/>')
        o.append(f'<text x="{left - 6}" y="{y(g) + 4:.1f}" text-anchor="end" style="fill:{MUTED}">{g}</text>')
    pts = []
    for i, (m, n, note) in enumerate(rows):
        cx = left + bw * i + bw / 2
        o.append(f'<rect x="{cx - bw * 0.32:.1f}" y="{y(n):.1f}" width="{bw * 0.64:.1f}" height="{y(0) - y(n):.1f}" rx="3" '
                 f'style="fill:var(--accent-soft,#f3efe9);stroke:var(--accent,#6b5a45)"><title>{m}: {n} đơn kế hoạch{(" · " + E(note)) if note else ""}</title></rect>')
        if n:
            o.append(f'<text x="{cx:.1f}" y="{y(n) - 5:.1f}" text-anchor="middle" style="fill:{INK};font-weight:600">{n}</text>')
        yy, mm = m.split("-")
        o.append(f'<text x="{cx:.1f}" y="{h - bottom + 16}" text-anchor="middle" style="fill:{MUTED}">T{int(mm)}</text>')
        if mm == "01" or i == 0:
            o.append(f'<text x="{cx - bw / 2 + 2:.1f}" y="{h - bottom + 32}" style="fill:{INK};font-weight:600">{yy}</text>')
        pts.append((cx, y(ns[m]), m, ns[m]))
    o.append('<polyline fill="none" style="stroke:var(--green,#1e6b3a);stroke-width:2" points="'
             + " ".join(f"{px:.1f},{py:.1f}" for px, py, _, _ in pts) + '"/>')
    for px, py, m, v in pts:
        o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.5" style="fill:var(--green,#1e6b3a)"><title>{m}: North Star kế hoạch {v} đơn giao trong khung</title></circle>')
    o.append(f'<rect x="{left + 8}" y="6" width="14" height="10" rx="2" style="fill:var(--accent-soft,#f3efe9);stroke:var(--accent,#6b5a45)"/>'
             f'<text x="{left + 28}" y="15" style="fill:{MUTED}">Đơn đã thanh toán (K01, kế hoạch)</text>'
             f'<line x1="{left + 250}" x2="{left + 268}" y1="11" y2="11" style="stroke:var(--green,#1e6b3a);stroke-width:2"/>'
             f'<text x="{left + 274}" y="15" style="fill:{MUTED}">North Star: đơn giao trong khung (NS1, suy ra)</text>')
    o.append("</svg>")
    return "\n".join(o)


# ----------------------------------------------------------------------------- HTML blocks
def _tbl(head, body_rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    return f'<div class="tbl"><table data-plan><thead><tr>{th}</tr></thead><tbody>{"".join(body_rows)}</tbody></table></div>'


def render_okr(data, period):
    obj = next(o for o in data["objectives"] if o["period"] == period)
    rows = []
    order = {"north_star": 0, "outcome": 1, "driver": 2, "guardrail": 3}
    items = [r for r in data["targets"] if r["period"] == period]
    items.sort(key=lambda r: (order[data["kpis"][r["kpi_id"]]["level"]], r["kpi_id"]))
    for r in items:
        k = data["kpis"][r["kpi_id"]]
        rows.append(f'<tr><td><code>{E(r["kpi_id"])}</code></td><td>{E(k["name"])}</td><td><strong>{E(fmt_target(k, r["value"]))}</strong></td>'
                    f'<td>{E(LEVEL_VN[k["level"]])}</td><td>{role_chip(k["owner"])}</td></tr>')
    qt = quarter_totals(data)
    extra = ""
    if "-Q" in period and period in qt:
        n, rev = qt[period]
        extra = f'<p class="muted">Cả quý: {n} đơn kế hoạch · doanh thu ước tính A${rev:,.0f} (AOV giả định A${float(data["assume"]["aov_aud"]):,.0f}).</p>'
    tasks = [t for t in data["tasks"] if _in_period(t, period)]
    work = ", ".join(f'{E(t["id"])} {E(t["task"])}' for t in tasks if t["type"] == "task")
    gates = "; ".join(E(t["task"].removeprefix("Cổng: ").removeprefix("Cổng ")) for t in tasks if t["type"] == "milestone")
    lines = f'<p><strong>Việc chính:</strong> {work or "–"}</p>'
    if gates:
        lines += f'<p><strong>Cổng:</strong> {gates}</p>'
    return (f'<section class="guide okr" id="{period.lower()}"><header class="g-head"><span class="badge b-int">{E(period)}</span>'
            f'<h3>{E(obj["obj_id"])} · {E(obj["objective"])}</h3></header><p class="g-purpose">{E(obj["why"])}</p>'
            + _tbl(["KPI", "Chỉ số", "Mục tiêu", "Loại", "Chủ"], rows) + extra + lines + "</section>")


def _period_range(period):
    if "-Q" in period:
        y, q = period.split("-Q")
        s = date(int(y), (int(q) - 1) * 3 + 1, 1)
        months = 3
    else:
        y, m = period.split("-")
        s, months = date(int(y), int(m), 1), 1
    e = s
    for _ in range(months):
        e = (e.replace(day=28) + timedelta(days=4)).replace(day=1)
    return s, e - timedelta(days=1)


def _in_period(t, period):
    s, e = _period_range(period)
    return t["s"] <= e and t["e"] >= s


def render_kpi_dict(data):
    rows = []
    for k in sorted(data["kpis"].values(), key=lambda k: ({"north_star": 0, "outcome": 1, "driver": 2, "guardrail": 3}[k["level"]], k["kpi_id"])):
        agg = {"exit": "giá trị tháng cuối kỳ", "sum": "cộng dồn kỳ", "rate": "tỉ lệ trong kỳ"}[k["aggregation"]]
        rows.append(f'<tr><td><code>{E(k["kpi_id"])}</code></td><td>{E(LEVEL_VN[k["level"]])}</td><td>{E(k["name"])}</td>'
                    f'<td>{E(k["unit"])}</td><td>{E(agg)}</td><td>{role_chip(k["owner"])}</td>'
                    f'<td><a href="{E(k["page"])}">{E(k["source"])}</a></td></tr>')
    return _tbl(["ID", "Loại", "Chỉ số", "Đơn vị", "Cách gộp theo kỳ", "Chủ", "Nguồn đo"], rows)


def render_year_summary(data):
    yt = year_totals(data)
    ns = north_star_plan(data)
    rows = []
    for y, v in yt.items():
        ns_total = sum(n for m, n in ns.items() if m.startswith(y))
        exit_m = max(m for m, _, _ in data["orders"] if m.startswith(y))
        exit_orders = dict((m, n) for m, n, _ in data["orders"])[exit_m]
        rows.append(f'<tr><th scope="row">{y}</th><td>{v["orders"]}</td><td>{exit_orders}</td><td>{ns_total}</td>'
                    f'<td>A${v["revenue"]:,.0f}</td></tr>')
    return _tbl(["Năm", "Tổng đơn kế hoạch", "Đơn/tháng cuối năm", "Đơn giao trong khung (NS1, suy ra)", "Doanh thu ước tính"], rows)


# ----------------------------------------------------------------------------- Mermaid (GitHub view)
def render_mermaid(data):
    out = ["```mermaid", "gantt", "    title Roadmap Q4/2026 – 2027", "    dateFormat YYYY-MM-DD", "    axisFormat %m/%y",
           "    todayMarker off"]
    ws = None
    for t in data["tasks"]:
        if t["workstream"] != ws:
            ws = t["workstream"]
            out.append(f"    section {ws}")
        name = t["task"].replace(":", " –").replace("#", "").replace(";", ",")
        tags = []
        if t["status"] == "done":
            tags.append("done")
        elif t["status"] == "in_progress":
            tags.append("active")
        if t["type"] == "milestone":
            tags.append("milestone")
            out.append(f"    {t['id']} {name} :{', '.join(tags + [t['id']])}, {t['start']}, 0d")
        else:
            out.append(f"    {t['id']} {name} ({t['owner']}) :{', '.join(tags + [t['id']])}, {t['start']}, {t['end']}")
    out.append("```")
    return "\n".join(out)
