"""Tiny swimlane (Visio-style) SVG generator for the handbook.

Each diagram = lanes (rows, one per position) x stages (columns, groups of sub-columns).
Nodes sit on a (lane, col) grid. Edges are orthogonal. Output is plain SVG that
inherits the site colours through CSS variables (with light fallbacks for standalone use).

Usage:  python tools/swimlane.py      -> writes assets/sop/*.svg
"""
from html import escape
from pathlib import Path

HDR_W, STAGE_H, COL_W, LANE_H = 118, 50, 134, 92
NODE_W, NODE_H = 116, 50
FS = 10.5

ROLE = {  # code: (label, sublabel, colour)
    "KH":  ("Khách hàng", "Customer", "#8e8e93"),
    "CX":  ("P4 · CX", "Chăm sóc KH", "#2f6fb0"),
    "OPS": ("P1 · OPS", "Điều phối", "#6b5a45"),
    "SRC": ("P2 · SRC", "Mua hàng & QC", "#2e7d4f"),
    "LOG": ("P3 · LOG", "Logistics & HQ", "#0f7c80"),
    "FIN": ("P6 · FIN", "Tài chính", "#7a4fa3"),
    "CEO": ("P0 · CEO", "Duyệt cấp cao", "#1d1d1f"),
    "EXT": ("Đối tác", "NCC · kho · hãng", "#a1a1a6"),
    "BANK": ("Ngân hàng", "Cổng thanh toán", "#a1a1a6"),
    # end-to-end supply chain: internal + every external stakeholder on its own lane
    "MKT": ("P5 · MKT", "Marketing & listing", "#b5562b"),
    "WEB": ("Shopify · cổng TT", "Hệ thống bán hàng", "#8e8e93"),
    "SUP": ("NCC / xưởng TQ", "Taobao · 1688", "#a1a1a6"),
    "WH":  ("Kho gom TQ", "Consolidation WH", "#a1a1a6"),
    "FWD": ("Forwarder", "Hãng tàu · HQ xuất TQ", "#a1a1a6"),
    "BRK": ("Đại lý HQ Úc", "Customs broker", "#a1a1a6"),
    "GOV": ("ABF · DAFF", "Hải quan · kiểm dịch Úc", "#a1a1a6"),
    "TPL": ("Kho CFS / 3PL Úc", "Dỡ hàng · lưu tạm", "#a1a1a6"),
    "LMC": ("Hãng giao Úc", "Giao 2 người · lắp", "#a1a1a6"),
}
EXTERNAL = {"KH", "EXT", "BANK", "WEB", "SUP", "WH", "FWD", "BRK", "GOV", "TPL", "LMC"}

CSS = """
.sw{font-family:Inter,-apple-system,"Segoe UI",sans-serif}
.sw .bg{fill:var(--panel,#fff)}
.sw .lane{fill:var(--panel,#fff);stroke:var(--line,#e5e5e7)}
.sw .lane.alt{fill:var(--bg,#fbfbfa)}
.sw .hdr{fill:var(--accent-soft,#f3efe9);stroke:var(--line,#e5e5e7)}
.sw .stg{fill:var(--accent-soft,#f3efe9);stroke:var(--line,#e5e5e7)}
.sw .sep{stroke:var(--line,#e5e5e7);stroke-dasharray:3 4}
.sw .t{fill:var(--ink,#1d1d1f);font-size:%(fs)spx}
.sw .tb{fill:var(--ink,#1d1d1f);font-size:12px;font-weight:650}
.sw .tm{fill:var(--muted,#6e6e73);font-size:10px}
.sw .ts{fill:var(--accent,#6b5a45);font-size:10px;font-weight:600}
.sw .n{fill:var(--panel,#fff);stroke-width:1.4}
.sw .n.ext{stroke-dasharray:4 3}
.sw .n.cust{fill:var(--bg,#fbfbfa)}
.sw .n.term{fill:var(--accent-soft,#f3efe9)}
.sw .e{fill:none;stroke:var(--ink,#1d1d1f);stroke-width:1.2;opacity:.75}
.sw .e.info{stroke-dasharray:4 3;opacity:.55}
.sw .ah{fill:var(--ink,#1d1d1f);opacity:.75}
.sw .lbl{fill:var(--muted,#6e6e73);font-size:9.5px;font-weight:600}
.sw .lblbg{fill:var(--panel,#fff);opacity:.92}
.sw .tag{fill:var(--ink,#1d1d1f)}
.sw .tagt{fill:var(--bg,#fff);font-size:9.5px;font-weight:700}
.sw .x{fill:#fdecea;stroke:#c0392b;stroke-width:1}
.sw .xt{fill:#a5281b;font-size:9.5px;font-weight:600}
.sw .band{fill:none;stroke-width:1.2;stroke-dasharray:6 4;opacity:.8}
.sw .bandt{font-size:9.5px;font-weight:600}
@media (prefers-color-scheme:dark){.sw .x{fill:#3a1f1c}.sw .xt{fill:#f5a097}}
""" % {"fs": FS}


class Diagram:
    def __init__(self, name, title, lanes, stages):
        self.name, self.title, self.lanes = name, title, lanes
        self.stages = stages  # list of (code, label, sla, n_subcols)
        self.ncols = sum(s[3] for s in stages)
        self.nodes, self.edges, self.bands, self.exits = {}, [], [], []
        self.W = HDR_W + self.ncols * COL_W + 8
        self.H = STAGE_H + len(lanes) * LANE_H + 8

    # grid helpers
    def cx(self, col):
        return HDR_W + col * COL_W + COL_W / 2

    def cy(self, lane, dy=0):
        return STAGE_H + self.lanes.index(lane) * LANE_H + LANE_H / 2 + dy

    def node(self, nid, lane, col, text, kind="task", tag=None, dy=0, w=NODE_W):
        self.nodes[nid] = dict(lane=lane, col=col, text=text, kind=kind, tag=tag,
                               x=self.cx(col), y=self.cy(lane, dy), w=w,
                               h=NODE_H if kind != "dec" else 58)
        return nid

    def edge(self, a, b, label=None, info=False, route="auto", sa=None, sb=None):
        self.edges.append(dict(a=a, b=b, label=label, info=info, route=route, sa=sa, sb=sb))

    def exit(self, nid, text, side="below"):
        self.exits.append((nid, text, side))

    def band(self, lane, c0, c1, text, dy=34):
        self.bands.append((lane, c0, c1, text, dy))

    # geometry
    def anchor(self, n, side):
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        return {"r": (x + w / 2, y), "l": (x - w / 2, y), "t": (x, y - h / 2), "b": (x, y + h / 2)}[side]

    def path(self, e):
        a, b = self.nodes[e["a"]], self.nodes[e["b"]]
        r = e["route"]
        if r == "auto":
            if a["lane"] == b["lane"]:
                r = "h" if b["col"] > a["col"] else "hb"
            elif abs(a["col"] - b["col"]) < 1e-6:
                r = "v"
            else:
                r = "hv" if b["col"] > a["col"] else "vh"
        if r == "h":
            p1, p2 = self.anchor(a, e["sa"] or "r"), self.anchor(b, e["sb"] or "l")
            pts = [p1, p2] if abs(p1[1] - p2[1]) < 1 else [p1, ((p1[0] + p2[0]) / 2, p1[1]), ((p1[0] + p2[0]) / 2, p2[1]), p2]
        elif r == "v":
            down = b["y"] > a["y"]
            p1 = self.anchor(a, e["sa"] or ("b" if down else "t"))
            p2 = self.anchor(b, e["sb"] or ("t" if down else "b"))
            pts = [p1, p2] if abs(p1[0] - p2[0]) < 1 else [p1, (p1[0], (p1[1] + p2[1]) / 2), (p2[0], (p1[1] + p2[1]) / 2), p2]
        elif r == "hv":  # right out of a, elbow just before b's column, into b's side
            p1 = self.anchor(a, e["sa"] or "r")
            if e["sb"] in ("t", "b"):
                p2 = self.anchor(b, e["sb"])
                pts = [p1, (p2[0], p1[1]), p2]
            else:
                p2 = self.anchor(b, "l")
                mx = p2[0] - 9
                pts = [p1, (mx, p1[1]), (mx, p2[1]), p2]
        elif r == "vh":  # vertical out of a, then horizontal into b
            down = b["y"] > a["y"]
            p1 = self.anchor(a, e["sa"] or ("b" if down else "t"))
            p2 = self.anchor(b, e["sb"] or ("l" if b["x"] > a["x"] else "r"))
            pts = [p1, (p1[0], p2[1]), p2]
        elif r == "rr":  # out of a's right, up/down in the column gap, into b's right
            p1, p2 = self.anchor(a, "r"), self.anchor(b, "r")
            mx = max(p1[0], p2[0]) + 9
            pts = [p1, (mx, p1[1]), (mx, p2[1]), p2]
        elif r == "hb":  # backward in same lane: under the nodes
            p1, p2 = self.anchor(a, "b"), self.anchor(b, "b")
            yy = p1[1] + 14
            pts = [p1, (p1[0], yy), (p2[0], yy), p2]
        return pts

    def render(self):
        o = [f'<svg class="sw" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.W:.0f} {self.H:.0f}" '
             f'width="{self.W:.0f}" height="{self.H:.0f}" role="img" aria-label="{escape(self.title)}">',
             f'<title>{escape(self.title)}</title><style>{CSS}</style>',
             '<defs><marker id="ah-%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
             '<path class="ah" d="M0,0 L10,5 L0,10 z"/></marker></defs>' % self.name,
             f'<rect class="bg" x="0" y="0" width="{self.W:.0f}" height="{self.H:.0f}" rx="12"/>']
        # stage header
        x = HDR_W
        o.append(f'<rect class="hdr" x="0" y="0" width="{HDR_W}" height="{STAGE_H}"/>')
        o.append(f'<text class="tm" x="12" y="22">Vị trí ↓</text><text class="tm" x="12" y="38">Giai đoạn →</text>')
        for code, label, sla, n in self.stages:
            w = n * COL_W
            o.append(f'<rect class="stg" x="{x}" y="0" width="{w}" height="{STAGE_H}"/>')
            o.append(f'<text class="tb" x="{x + 10}" y="21"><tspan class="ts">{escape(code)}</tspan>  {escape(label)}</text>')
            o.append(f'<text class="tm" x="{x + 10}" y="38">⏱ {escape(sla)}</text>')
            x += w
        # lanes
        for i, ln in enumerate(self.lanes):
            y = STAGE_H + i * LANE_H
            lab, sub, col = ROLE[ln]
            o.append(f'<rect class="lane{" alt" if i % 2 else ""}" x="0" y="{y}" width="{self.W - 8}" height="{LANE_H}"/>')
            o.append(f'<rect x="0" y="{y}" width="5" height="{LANE_H}" fill="{col}"/>')
            o.append(f'<text class="tb" x="14" y="{y + LANE_H / 2 - 3}">{escape(lab)}</text>')
            o.append(f'<text class="tm" x="14" y="{y + LANE_H / 2 + 12}">{escape(sub)}</text>')
        # stage separators
        x = HDR_W
        for _, _, _, n in self.stages[:-1]:
            x += n * COL_W
            o.append(f'<line class="sep" x1="{x}" y1="{STAGE_H}" x2="{x}" y2="{STAGE_H + len(self.lanes) * LANE_H}"/>')
        # bands (continuous activities)
        for lane, c0, c1, text, dy in self.bands:
            col = ROLE[lane][2]
            y = self.cy(lane, dy)
            x0, x1 = HDR_W + c0 * COL_W + 6, HDR_W + (c1 + 1) * COL_W - 6
            o.append(f'<line class="band" stroke="{col}" x1="{x0}" y1="{y}" x2="{x1}" y2="{y}"/>')
            o.append(f'<text class="bandt" fill="{col}" x="{x0 + 4}" y="{y - 4}">↻ {escape(text)}</text>')
        # edges
        for e in self.edges:
            pts = self.path(e)
            d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
            o.append(f'<path class="e{" info" if e["info"] else ""}" d="{d}" marker-end="url(#ah-{self.name})"/>')
            if e["label"]:
                (x1, y1), (x2, y2) = pts[0], pts[1]
                lx, ly = (x1 + x2) / 2, (y1 + y2) / 2
                if abs(y1 - y2) < 1:
                    ly -= 5
                else:
                    lx += 4
                tw = len(e["label"]) * 5.4 + 6
                anchor = "middle" if abs(y1 - y2) < 1 else "start"
                bx = lx - tw / 2 if anchor == "middle" else lx - 2
                o.append(f'<rect class="lblbg" x="{bx:.1f}" y="{ly - 9:.1f}" width="{tw:.1f}" height="12" rx="3"/>')
                o.append(f'<text class="lbl" x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}">{escape(e["label"])}</text>')
        # nodes
        for nid, n in self.nodes.items():
            col = ROLE[n["lane"]][2]
            x, y, w, h = n["x"], n["y"], n["w"], n["h"]
            k = n["kind"]
            if k == "dec":
                o.append(f'<path class="n" stroke="{col}" d="M{x},{y - h / 2} L{x + w / 2},{y} L{x},{y + h / 2} L{x - w / 2},{y} z"/>')
            elif k in ("start", "end", "term"):
                o.append(f'<rect class="n term" stroke="{col}" x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="{h / 2}"/>')
            else:
                cls = {"ext": "n ext", "cust": "n cust"}.get(k, "n")
                o.append(f'<rect class="{cls}" stroke="{col}" x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="8"/>')
                if k == "task":
                    o.append(f'<rect x="{x - w / 2}" y="{y - h / 2 + 8}" width="3" height="{h - 16}" fill="{col}"/>')
            lines = n["text"].split("\n")
            fs = FS if k != "dec" else 10
            y0 = y - (len(lines) - 1) * (fs + 2) / 2 + fs / 2 - 1
            for j, ln in enumerate(lines):
                weight = ' font-weight="600"' if j == 0 and k != "dec" else ""
                o.append(f'<text class="t" x="{x}" y="{y0 + j * (fs + 2):.1f}" text-anchor="middle" font-size="{fs}"{weight}>{escape(ln)}</text>')
            if n["tag"]:
                tw = len(n["tag"]) * 6 + 10
                tx, ty = x + w / 2 - tw + 6, y - h / 2 - 7
                o.append(f'<rect class="tag" x="{tx}" y="{ty}" width="{tw}" height="14" rx="7"/>')
                o.append(f'<text class="tagt" x="{tx + tw / 2}" y="{ty + 10.5}" text-anchor="middle">{escape(n["tag"])}</text>')
        # exception exits
        for nid, text, side in self.exits:
            n = self.nodes[nid]
            tw = len(text) * 5.3 + 14
            if side == "below":
                tx, ty = n["x"] - tw / 2, n["y"] + n["h"] / 2 + 4
            else:  # above
                tx, ty = n["x"] - tw / 2, n["y"] - n["h"] / 2 - 25
            o.append(f'<rect class="x" x="{tx:.1f}" y="{ty:.1f}" width="{tw:.1f}" height="14" rx="7"/>')
            o.append(f'<text class="xt" x="{tx + tw / 2:.1f}" y="{ty + 10.5:.1f}" text-anchor="middle">{escape(text)}</text>')
        o.append("</svg>")
        return "\n".join(o)


# ---------------------------------------------------------------- SOP-A: normal order
def sop_a():
    d = Diagram("a", "SOP-A Đơn chuẩn: từ thanh toán tới đóng đơn",
                ["KH", "CX", "OPS", "SRC", "LOG", "EXT", "FIN"],
                [("S1", "Nhận đơn", "≤ 4h làm việc", 2), ("S2", "Đặt NCC", "≤ 24h sau thanh toán", 2),
                 ("S3", "SX & gửi", "≤ ngày hẹn +2d", 1), ("S4", "Kho gom · QC", "≤ 2d sau nhập", 2),
                 ("S5", "Xuất lô", "1 ngày cố định/tuần", 2), ("S6", "Thông quan", "báo giữ ≤ 24h", 1),
                 ("S7", "Giao cuối", "hãng hẹn ngày", 1), ("S8", "Sau giao · đóng", "D+3 · D+14", 2)])
    N, E = d.node, d.edge
    N("k0", "KH", 0, "Đặt hàng\n& thanh toán", "start")
    N("a1", "CX", 0, "A1 Kiểm đơn\nđịa chỉ · SĐT\nrủi ro gian lận", tag="10")
    N("a1d", "CX", 1, "Hợp lệ?", "dec", tag="20")
    N("k1", "KH", 1, "Nhận xác nhận\n+ khung ETA thật", "cust")
    N("a2", "SRC", 2, "A2 Hỏi tồn kho\n+ ngày xuất cụ thể\nchính → dự phòng")
    N("a3", "SRC", 3, "A3 Lập PO\nđúng mã màu/size\n+ yêu cầu đóng gói", tag="30")
    N("x3", "EXT", 3, "NCC nhận PO\nxác nhận ngày xuất", "ext")
    N("f3", "FIN", 3, "Thanh toán NCC\nqua sàn (escrow)")
    N("x4", "EXT", 4, "NCC sản xuất\nảnh/video\nđóng kiện X/Y", "ext")
    N("a4", "SRC", 4, "A4 Duyệt ảnh kiện\nnhận vận đơn\nnội địa", tag="40")
    N("o4", "OPS", 4, "Leo thang trễ\n+2d nhắc · +5d OPS\n+7d đổi NCC")
    N("x5", "EXT", 5, "Kho gom nhận\nđếm kiện X/Y", "ext")
    N("a5", "SRC", 5, "A5 QC kho gom\nkiện · màu · KT\nphụ kiện · ISPM")
    N("a5d", "SRC", 6, "QC đạt?", "dec", tag="50")
    N("c6", "CX", 6, "Gửi ảnh QC\ncho khách")
    N("k6", "KH", 6, "Nhận ảnh QC\ncủa chính đơn", "cust")
    N("a6", "LOG", 7, "A6 Cắt lô tuần\nCI · PL · ISPM\nChAFTA · BMSB")
    N("o7", "OPS", 7, "Duyệt lô\nchứng từ khớp\nhàng thật")
    N("x8", "EXT", 7, "Forwarder\nnhận hàng\nquét lần đầu", "ext")
    N("f7", "FIN", 7, "Trả cước\nthuế · GST lô")
    N("a7d", "LOG", 8, "Có lượt\nquét thật?", "dec", tag="60")
    N("c8", "CX", 8, "Fulfilled\n+ gửi tracking")
    N("k8", "KH", 8, "Nhận tracking", "cust")
    N("a8", "LOG", 9, "A8 Theo dõi cảng\nhải quan · kiểm dịch", tag="70")
    N("x9", "EXT", 9, "Broker khai báo\nnộp thuế/GST", "ext")
    N("a9", "LOG", 10, "A9 Bàn giao\nhãng giao nội địa", tag="80")
    N("x10", "EXT", 10, "Hãng giao hẹn\nngày · đủ kiện", "ext")
    N("k10", "KH", 10, "Nhận hàng\nđếm kiện · ký POD", "cust")
    N("a10", "LOG", 11, "A10 Xác nhận POD\nảnh giao hàng", tag="90")
    N("c11", "CX", 11, "D+3 Hướng dẫn lắp\n+ mời review\n(mời mọi khách)")
    N("k11", "KH", 11, "Có vấn đề?", "dec")
    N("f12", "FIN", 12, "Đối soát\nlanded cost thực\nvs giá sàn")
    N("o12", "OPS", 12, "D+14 không case\nĐÓNG ĐƠN", "end", tag="99")

    E("k0", "a1"); E("a1", "a1d"); E("a1d", "k1", "Đạt", info=True)
    E("a1d", "a2", "Đạt"); E("a2", "a3"); E("a3", "x3", "PO"); E("x3", "f3")
    E("f3", "x4", route="hv", sb="b"); E("x4", "a4", "ảnh", info=True); E("a4", "o4", "trễ hẹn", info=True)
    E("x4", "x5"); E("x5", "a5", "nhập kho"); E("a5", "a5d")
    E("a5d", "c6", "Đạt", info=True); E("c6", "k6", info=True)
    E("a5d", "a6", "Đạt"); E("a6", "o7"); E("a6", "x8", "giao hàng")
    E("x8", "f7", info=True); E("x8", "a7d", route="hv", sb="b")
    E("a7d", "c8", "Có"); E("c8", "k8", info=True)
    E("a7d", "a8"); E("a8", "x9"); E("a8", "a9"); E("a9", "x10"); E("x10", "k10", info=True, route="rr")
    E("a9", "a10"); E("a10", "c11"); E("c11", "k11", info=True)
    E("a10", "f12", route="vh"); E("f12", "o12")
    d.exit("a1d", "Không → C1 hủy / hỏi lại")
    d.exit("a2", "Hết hàng cả 2 NCC → C2")
    d.exit("a5d", "Không → trả NCC tại TQ")
    d.exit("a7d", "Chưa quét = KHÔNG gửi tracking", "above")
    d.exit("a8", "Bị giữ → báo KH ≤ 24h")
    d.exit("k11", "Có → SOP-B", "above")
    d.band("CX", 2, 10, "Cập nhật chủ động mỗi 7 ngày · trạng thái thật · trễ thì báo trước ≥ 7 ngày", dy=40)
    d.band("OPS", 0, 3, "Control tower 09:00 hằng ngày: rà cảnh báo SLA trong tracker", dy=38)
    return d


# ---------------------------------------------------------------- SOP-B1: case handling
def sop_b1():
    d = Diagram("b1", "SOP-B1 Xử lý case hậu mãi: tiếp nhận tới đóng case",
                ["KH", "CX", "OPS", "CEO", "SRC", "FIN", "EXT"],
                [("B1", "Tiếp nhận", "phản hồi ≤ 4h LV", 1), ("B2", "Bằng chứng", "KH gửi ≤ 7 ngày", 1),
                 ("B3", "Duyệt theo mức", "≤ 24h sau đủ chứng cứ", 2), ("B4", "Đề xuất", "KH chọn", 1),
                 ("B5", "Thực thi", "gửi bù ≤ 5d · hoàn ≤ 7d LV", 2), ("B6", "Truy đòi", "claim ≤ 48h", 1),
                 ("B7", "Đóng · học", "review thứ Sáu", 1)])
    N, E = d.node, d.edge
    N("k0", "KH", 0, "Báo vấn đề\nemail · form · chat", "start")
    N("b1", "CX", 0, "B1 Mở case\ngán mã C1–C8\nliên kết mã đơn", tag="OPEN")
    N("b2", "CX", 1, "B2 Xin bằng chứng\nnhãn kiện · ảnh lỗi\nảnh toàn món")
    N("k1", "KH", 1, "Gửi ảnh/video", "cust")
    N("b3", "CX", 2, "Mức\nđền bù?", "dec")
    N("b3a", "CX", 3, "≤ A$50\nCX tự duyệt", "term")
    N("o3", "OPS", 3, "A$51–150\nOPS duyệt", "term")
    N("e3", "CEO", 3, "> A$150 · 100%\nCEO duyệt", "term")
    N("b4", "CX", 4, "B4 Đề xuất\nR1 sửa · R2 gửi bù\nR3 đổi · R4 hoàn")
    N("k4", "KH", 4, "Đồng ý?", "dec")
    N("b5", "CX", 5, "B5 Kích hoạt\nthực thi · ghi case")
    N("s5", "SRC", 5, "Gửi bù / đổi mới\nhoặc đặt thu hồi\n(→ SOP-B2)")
    N("f6", "FIN", 6, "Hoàn tiền\nđúng số đã duyệt\ncổng gốc")
    N("s7", "SRC", 7, "B6 Claim NCC\n/ hãng giao\n/ bảo hiểm")
    N("x7", "EXT", 7, "Bồi hoàn\nhoặc gửi bù", "ext")
    N("c8", "CX", 8, "B7 Đóng case\nmã nguyên nhân gốc", "end", tag="CLOSED")
    N("o8", "OPS", 8, "Review tuần\nlỗi lặp 2 lần/tháng\n→ tắt mã / NCC")
    N("f8", "FIN", 8, "Sổ ngoại lệ\nchi phí − thu hồi")

    E("k0", "b1"); E("b1", "b2"); E("b2", "k1", info=True); E("k1", "b3", route="hv", sb="t")
    E("b3", "b3a", "≤50"); E("b3", "o3", "51–150", route="vh"); E("b3", "e3", ">150", route="vh")
    E("b3a", "b4"); E("o3", "b4", route="hv"); E("e3", "b4", route="hv")
    E("b4", "k4", info=True); E("k4", "b5", "Đồng ý", route="hv")
    E("b5", "s5", "R1–R3"); E("b5", "f6", "R4", route="hv", sb="t")
    E("s5", "s7"); E("s7", "x7"); E("s7", "f8", route="hv", sb="t")
    E("b5", "c8", "xong"); E("c8", "o8")
    d.exit("k4", "Không → OPS gọi điện", "above")
    d.exit("b1", "Nhắc chargeback → gọi ≤ 24h")
    return d


# ---------------------------------------------------------------- SOP-B2: returns & refund
def sop_b2():
    d = Diagram("b2", "SOP-B2 Trả hàng, thu hồi và hoàn tiền",
                ["KH", "CX", "OPS", "LOG", "EXT", "FIN"],
                [("R1", "Yêu cầu", "phản hồi ≤ 24h", 1), ("R2", "Điều kiện", "≤ 24h", 2),
                 ("R3", "Thu hồi", "brand trả phí nếu lỗi", 1), ("R4", "Nhận · kiểm", "≤ 2d sau nhận", 1),
                 ("R5", "Hoàn tiền", "≤ 7 ngày LV", 1), ("R6", "Hàng về", "≤ 14 ngày", 1)])
    N, E = d.node, d.edge
    N("k0", "KH", 0, "Yêu cầu\ntrả / đổi hàng", "start")
    N("r1", "CX", 0, "R1 Kiểm case\nmã C3–C6\nngày giao")
    N("r2", "CX", 1, "Lỗi do\nbrand?", "dec")
    N("r2b", "CX", 2, "Đổi ý\nhợp lệ?", "dec")
    N("l2", "LOG", 2, "Đặt hãng thu hồi\nbrand trả phí\nKHÔNG gửi về TQ")
    N("f2", "FIN", 2, "Lỗi: hoàn / đổi\nKHÔNG chờ thu hồi")
    N("k3", "KH", 3, "Tự gửi về\nđiểm nhận AU\n(KH trả cước)", "cust")
    N("x3", "EXT", 3, "Hãng / 3PL AU\nlấy hàng\nchụp tình trạng", "ext")
    N("l4", "LOG", 4, "R4 Kiểm hàng về\nđủ kiện · tình trạng", tag="RTN")
    N("f5", "FIN", 5, "R5 Hoàn tiền\nđúng số đã duyệt\nphương thức gốc")
    N("k5", "KH", 5, "Nhận email\nhoàn tiền", "cust")
    N("o6", "OPS", 6, "Bán lại\nđược?", "dec")
    N("l6", "LOG", 6, "Nhập kho AU\nB-grade / outlet\nhoặc thanh lý")

    E("k0", "r1"); E("r1", "r2"); E("r2", "r2b", "Không")
    E("r2", "l2", "Có", route="vh"); E("r2", "f2", route="vh")
    E("l2", "x3", route="vh"); E("r2b", "k3", "Hợp lệ")
    E("k3", "x3"); E("x3", "l4", route="hv", sb="b"); E("l4", "f5", route="vh")
    E("f5", "k5", info=True); E("l4", "o6"); E("o6", "l6")
    d.exit("r2b", "≤ 14d · chưa lắp · nguyên hộp", "above")
    d.exit("r2b", "Không → từ chối, nêu rõ quyền ACL")
    d.exit("l4", "Hư do KH → trừ theo chính sách", "above")
    return d


# ---------------------------------------------------------------- SOP-B3: chargeback
def sop_b3():
    d = Diagram("b3", "SOP-B3 Tranh chấp thanh toán (chargeback)",
                ["KH", "BANK", "CX", "OPS", "FIN"],
                [("D1", "Cảnh báo", "trong ngày", 1), ("D2", "Liên hệ", "gọi ≤ 24h", 1),
                 ("D3", "Quyết định", "≤ 48h", 2), ("D4", "Hồ sơ", "trước hạn cổng −3d", 1),
                 ("D5", "Kết quả · học", "khi có phán quyết", 2)])
    N, E = d.node, d.edge
    N("k0", "KH", 0, "Mở tranh chấp\nvới ngân hàng", "start")
    N("g0", "BANK", 0, "Cổng TT báo\ndispute + hạn nộp", "ext")
    N("f0", "FIN", 0, "Ghi dispute\nliên kết mã đơn", tag="DSP")
    N("c1", "CX", 1, "Gọi KH ≤ 24h\nlựa chọn đúng\nbảng bồi thường")
    N("c2", "CX", 2, "KH rút\ntranh chấp?", "dec")
    N("o2", "OPS", 2, "Lỗi thuộc\nbrand?", "dec")
    N("f2", "FIN", 2, "Chấp nhận dispute\nhoàn tiền")
    N("f3", "FIN", 3, "Thực hiện\ngiải pháp\nđã thỏa thuận")
    N("f4", "FIN", 4, "Nộp hồ sơ\nETA đã hứa · tracking\nPOD · trao đổi")
    N("g5", "BANK", 5, "Phán quyết", "ext")
    N("o6", "OPS", 6, "Root cause\n→ sửa SOP", "end")

    E("k0", "g0"); E("g0", "f0"); E("f0", "c1", route="hv", sb="b")
    E("c1", "c2"); E("c2", "o2", "Không"); E("o2", "f2", "Có")
    E("c2", "f3", "Có", route="hv", sb="t"); E("o2", "f4", "Không", route="hv", sb="t")
    E("f4", "g5", route="hv", sb="b"); E("g5", "o6", route="hv", sb="t")
    d.exit("c1", "Không gọi được → email + SMS", "above")
    return d



# ================================================================= END-TO-END SUPPLY CHAIN (E0–E3)
def e0():
    d = Diagram("e0", "E0 Chuẩn bị sản phẩm: từ chọn mẫu tới mở bán",
                ["CEO", "MKT", "SRC", "SUP", "LOG", "FWD", "BRK", "FIN"],
                [("P1", "Chọn mẫu", "theo Top 100", 1), ("P2", "Đối chiếu NCC", "5 mẫu/ngày", 2),
                 ("P3", "Mẫu thật", "HERO: 7–14 ngày", 2), ("P4", "Giá về tới Úc", "trước khi đăng", 2),
                 ("P5", "Đăng bán", "DRAFT → ACTIVE", 2)])
    N, E = d.node, d.edge
    N("c0", "CEO", 0, "Duyệt danh sách\nmẫu mở bán\n(HERO / CORE)", "start")
    N("m0", "MKT", 0, "Đề xuất mẫu\ntừ Top 100\n+ nhu cầu thật")
    N("s1", "SRC", 1, "Tìm 2 NCC/mẫu\nbằng ảnh\nưu tiên NCC đã chấm")
    N("u1", "SUP", 1, "Báo bản vẽ W×D×H\nvật liệu · số kiện\nthời gian SX", "ext")
    N("s2", "SRC", 2, "Khớp ±2 cm?\nmàu đúng mã?", "dec")
    N("s3", "SRC", 3, "Đặt mẫu thật\n(HERO)\n+ yêu cầu đóng gói")
    N("u3", "SUP", 3, "Gửi mẫu\nảnh/video\nđóng kiện", "ext")
    N("s4", "SRC", 4, "Đo · chụp màu\ngolden sample\nghi Master SKU", tag="VERIFIED")
    N("l5", "LOG", 5, "Xin báo giá\ncước theo CBM\n+ phí kho gom")
    N("w5", "FWD", 5, "Báo giá LCL\nlịch tàu\nthời gian chạy", "ext")
    N("b5", "BRK", 5, "Xác nhận mã HS\nthuế · GST · kiểm dịch\ngỗ / bao bì", "ext")
    N("f6", "FIN", 6, "Tính landed cost\ngiá bán AUD\nbiên ròng ≥ 30%")
    N("c6", "CEO", 6, "Duyệt giá?", "dec")
    N("m7", "MKT", 7, "Viết listing EN\ntừ Master SKU\nảnh được phép dùng")
    N("m8", "MKT", 8, "Duyệt 5 câu\n+ bật bán", "end", tag="ACTIVE")
    E("m0", "c0", info=True, route="v"); E("c0", "s1", route="hv", sb="t")
    E("s1", "u1", "hỏi spec"); E("u1", "s2", route="hv", sb="b"); E("s1", "s2")
    E("s2", "s3", "Khớp"); E("s3", "u3"); E("u3", "s4", route="hv", sb="b"); E("s3", "s4")
    E("s4", "l5", route="hv", sb="t"); E("l5", "w5"); E("w5", "b5", info=True, route="v")
    E("b5", "f6", route="hv", sb="t")
    E("f6", "c6", route="v"); E("c6", "m7", "Duyệt", route="hv", sb="t"); E("m7", "m8")
    d.exit("s2", "Lệch > 2 cm → mẫu khác / NCC khác")
    d.exit("s4", "Mẫu trượt → đổi NCC", "above")
    d.exit("c6", "Biên < 30% → bỏ mẫu / đổi NCC")
    d.band("SRC", 5, 8, "Master SKU là nguồn duy nhất cho listing, nhãn, chứng từ", dy=38)
    return d


def e1():
    d = Diagram("e1", "E1 Đơn hàng → đặt NCC → sản xuất → kho gom QC (S1–S4)",
                ["KH", "WEB", "CX", "SRC", "FIN", "SUP", "WH", "OPS"],
                [("S1", "Nhận đơn", "≤ 4h làm việc", 3), ("S2", "Đặt NCC", "≤ 24h sau thanh toán", 3),
                 ("S3", "SX & gửi", "≤ ngày hẹn +2d", 2), ("S4", "Kho gom · QC", "≤ 2d sau nhập", 3)])
    N, E = d.node, d.edge
    N("k0", "KH", 0, "Đặt hàng\n& thanh toán", "start")
    N("w0", "WEB", 0, "Thu tiền\ntạo đơn · chống\ngian lận tự động", "ext", tag="10")
    N("c1", "CX", 1, "Kiểm đơn: địa chỉ\nđường vào · SĐT\nmã · rủi ro")
    N("c2", "CX", 2, "Hợp lệ?", "dec", tag="20")
    N("k2", "KH", 2, "Email xác nhận\n+ khung ETA thật", "cust")
    N("s3", "SRC", 3, "Hỏi tồn + ngày\nxuất: NCC chính\n→ dự phòng")
    N("s4", "SRC", 4, "Lập PO: đúng mã\n+ shipping mark\n+ file nhãn")
    N("f4", "FIN", 4, "Thanh toán NCC\nqua sàn")
    N("u5", "SUP", 5, "Xác nhận PO\nngày xuất cụ thể", "ext", tag="30")
    N("u6", "SUP", 6, "Sản xuất\nđóng kiện X/Y\ndán nhãn brand", "ext")
    N("s6", "SRC", 6, "Duyệt ảnh kiện\n+ vận đơn\nnội địa", tag="40")
    N("u7", "SUP", 7, "Gửi chuyển phát\nnội địa\ntới kho gom", "ext")
    N("h8", "WH", 8, "Nhận hàng\nđếm kiện · cân\nchụp ngoại quan", "ext")
    N("s8", "SRC", 8, "QC: kích thước\nmàu · phụ kiện\nđóng gói · ISPM")
    N("s9", "SRC", 9, "QC đạt?", "dec", tag="50")
    N("h10", "WH", 10, "Gia cố · dán\nshipping mark\nđóng pallet ISPM-15", "ext")
    N("c10", "CX", 10, "Gửi ảnh QC\ncủa chính đơn")
    N("k10", "KH", 10, "Nhận ảnh QC", "cust")
    E("k0", "w0", route="v"); E("w0", "c1", route="hv", sb="b"); E("c1", "c2"); E("c2", "k2", "Đạt", info=True, route="v")
    E("c2", "s3", "Đạt", route="hv", sb="t"); E("s3", "s4"); E("s4", "f4", route="v"); E("f4", "u5", route="hv", sb="t")
    E("u5", "u6"); E("u6", "s6", "ảnh", info=True, route="v"); E("u6", "u7"); E("u7", "h8", route="hv", sb="t")
    E("h8", "s8", "báo nhập", route="v"); E("s8", "s9"); E("s9", "h10", "Đạt", route="hv", sb="t")
    E("s9", "c10", info=True, route="hv", sb="b"); E("c10", "k10", info=True, route="v")
    d.exit("c2", "Không → C1 hủy / hỏi lại")
    d.exit("s3", "Hết hàng cả 2 NCC → C2", "above")
    d.exit("s6", "Trễ: +2d nhắc · +5d OPS · +7d đổi NCC")
    d.exit("s9", "Trượt → NCC làm lại / đổi", "above")
    d.band("OPS", 0, 10, "Control tower 09:00: rà cờ SLA (chưa đặt NCC > 24h, NCC quá hẹn > 2d, QC tồn > 2d)", dy=0)
    d.band("CX", 3, 9, "Cập nhật khách mỗi 7 ngày bằng trạng thái thật", dy=38)
    return d


def e2():
    d = Diagram("e2", "E2 Xuất khẩu TQ → vận tải biển → thông quan Úc (S5–S6)",
                ["OPS", "LOG", "FWD", "WH", "BRK", "GOV", "FIN", "CX"],
                [("S5", "Cắt lô · chứng từ", "1 ngày cố định/tuần", 3), ("S5", "Xuất khẩu TQ", "theo lịch tàu", 2),
                 ("S6", "Trên biển", "theo B/L", 1), ("S6", "Thông quan Úc", "báo giữ ≤ 24h", 3)])
    N, E = d.node, d.edge
    N("l0", "LOG", 0, "Cắt lô tuần\nđơn QC đạt\ntính CBM · kg", "start")
    N("l1", "LOG", 1, "Lập CI · PL\npacking declaration\nISPM-15 · C/O ChAFTA")
    N("o2", "OPS", 2, "Duyệt lô\nchứng từ khớp\nhàng thật", "dec")
    N("w3", "FWD", 3, "Booking\nlấy hàng\ntại kho gom", "ext")
    N("h3", "WH", 3, "Bàn giao\nđủ kiện\ntheo PL", "ext")
    N("w4", "FWD", 4, "Khai HQ xuất TQ\nđóng container\nphát hành B/L", "ext", tag="60")
    N("l5", "LOG", 5, "Cập nhật ETA lô\nvào tracker\ngửi bộ chứng từ")
    N("c5", "CX", 5, "Báo khách: đã\nxuất + tracking\n(chỉ khi có quét thật)")
    N("b6", "BRK", 6, "Khai báo nhập\nkhẩu (FID) trước\nkhi tàu cập cảng", "ext")
    N("g7", "GOV", 7, "Đánh giá hồ sơ\nkiểm dịch gỗ\nbao bì · kiểm hóa?", "ext")
    N("f7", "FIN", 7, "Nộp thuế · GST\nphí cảng · phí\nkiểm dịch")
    N("g8", "GOV", 8, "Thông quan?", "dec", tag="70")
    N("l8", "LOG", 8, "Nhận lệnh giải\nphóng · đặt kho\nCFS dỡ hàng", "end")
    E("l0", "l1"); E("l1", "o2", route="hv", sb="b"); E("o2", "w3", "Duyệt", route="hv", sb="t")
    E("w3", "h3", route="v"); E("w3", "w4"); E("w4", "l5", route="hv", sb="b"); E("l5", "c5", info=True, route="v")
    E("l5", "b6", route="hv", sb="t"); E("b6", "g7", route="hv", sb="t"); E("b6", "f7", route="hv", sb="t", info=True)
    E("g7", "g8"); E("g8", "l8", "Có", route="hv", sb="b")
    d.exit("o2", "Không khớp → sửa chứng từ")
    d.exit("g8", "Bị giữ → báo KH ≤ 24h")
    d.exit("w4", "Chậm tàu → cập nhật ETA ngay")
    d.band("LOG", 5, 8, "Theo dõi tàu · cảng; mọi thay đổi ETA ghi tracker trong ngày", dy=38)
    return d


def e3():
    d = Diagram("e3", "E3 Kho Úc → giao chặng cuối → sau giao → đóng đơn (S7–S8)",
                ["KH", "WEB", "CX", "LOG", "TPL", "LMC", "FIN", "OPS"],
                [("S7", "Dỡ hàng · phân bổ", "≤ 2d sau giải phóng", 2), ("S7", "Giao chặng cuối", "hãng hẹn ngày", 3),
                 ("S8", "Sau giao", "D+3", 2), ("S8", "Đóng đơn", "D+14", 2)])
    N, E = d.node, d.edge
    N("t0", "TPL", 0, "Dỡ container\nđếm kiện theo PL\nchụp hư hỏng", "start")
    N("l1", "LOG", 1, "Phân bổ đơn\ncho hãng giao\ntheo khu vực")
    N("m2", "LMC", 2, "Nhận hàng\nquét lần đầu\nhẹn ngày với KH", "ext")
    N("w2", "WEB", 2, "Fulfilled\n+ email tracking", "ext", tag="80")
    N("k2", "KH", 2, "Chọn ngày\nnhận hàng", "cust")
    N("m3", "LMC", 3, "Giao 2 người\nđủ kiện X/Y\nlắp (nếu mua)", "ext")
    N("k3", "KH", 3, "Kiểm kiện\nký POD", "cust")
    N("l4", "LOG", 4, "Xác nhận POD\nảnh giao hàng", tag="90")
    N("c5", "CX", 5, "D+3 hướng dẫn\nlắp + mời review\n(mọi khách)")
    N("k5", "KH", 5, "Có vấn đề?", "dec")
    N("f7", "FIN", 7, "Đối soát landed\ncost thực từng\nđơn vs giá sàn")
    N("o8", "OPS", 8, "D+14 không case\nĐÓNG ĐƠN", "end", tag="99")
    E("t0", "l1", route="hv", sb="b"); E("l1", "m2", route="hv", sb="t"); E("m2", "w2", "quét thật", route="hv", sb="b")
    E("w2", "k2", info=True, route="v"); E("m2", "m3"); E("m3", "k3", info=True, route="hv", sb="b")
    E("m3", "l4", "POD", route="hv", sb="b"); E("l4", "c5", route="hv", sb="b"); E("c5", "k5", info=True, route="hv", sb="b")
    E("l4", "f7", route="hv", sb="t"); E("f7", "o8")
    d.exit("t0", "Kiện hỏng → chụp, claim, gửi bù")
    d.exit("m3", "Thiếu kiện / hỏng → SOP-B")
    d.exit("k5", "Có → SOP-B (C3–C8)")
    d.band("CX", 0, 4, "Khách nhận tracking chỉ sau lượt quét thật của hãng giao", dy=38)
    return d


# ================================================================= OPERATING MAP (macro swimlane)
MAP_LANES = ["KH", "WEB", "CEO", "MKT", "CX", "OPS", "SRC", "LOG", "FIN",
             "SUP", "WH", "FWD", "BRK", "GOV", "TPL", "LMC"]
MAP_STAGES = [  # code, title, phase
    ("P1", "Chọn mẫu", "Chuẩn bị"), ("P2", "NCC & mẫu", "Chuẩn bị"), ("P3", "Giá & đăng bán", "Chuẩn bị"),
    ("S1", "Nhận đơn", "Bán"), ("S2", "Đặt NCC", "Mua"), ("S3", "SX & gửi", "Mua"), ("S4", "Kho gom · QC", "Mua"),
    ("S5", "Xuất lô", "Vận chuyển"), ("S6", "Biển · thông quan", "Vận chuyển"), ("S7", "Giao cuối", "Giao"),
    ("S8", "Sau giao · đóng", "Giao"), ("B", "Hậu mãi", "Hậu mãi")]
# (lane, stage index, text, kind) kind: R = làm chính (responsible), A = duyệt (accountable), C = tham gia/được hỏi, I = được báo
MAP_CELLS = [
    ("MKT", 0, "Đề xuất mẫu", "R"), ("CEO", 0, "Duyệt danh sách", "A"),
    ("SRC", 1, "Tìm 2 NCC · đặt mẫu", "R"), ("SUP", 1, "Báo spec · gửi mẫu", "C"),
    ("LOG", 2, "Báo giá cước · HS", "C"), ("FWD", 2, "Báo giá LCL", "C"), ("BRK", 2, "Mã HS · thuế", "C"),
    ("FIN", 2, "Landed cost · giá", "R"), ("CEO", 2, "Duyệt giá", "A"), ("MKT", 2, "Listing · bật bán", "R"),
    ("KH", 3, "Đặt & trả tiền", "C"), ("WEB", 3, "Thu tiền · tạo đơn", "C"), ("CX", 3, "Kiểm & xác nhận", "R"),
    ("SRC", 4, "Lập PO", "R"), ("FIN", 4, "Trả NCC qua sàn", "R"), ("SUP", 4, "Xác nhận ngày xuất", "C"),
    ("SUP", 5, "SX · đóng kiện", "C"), ("SRC", 5, "Duyệt ảnh kiện", "R"),
    ("WH", 6, "Nhận · đếm kiện", "C"), ("SRC", 6, "QC đạt/trượt", "R"), ("CX", 6, "Gửi ảnh QC", "I"),
    ("LOG", 7, "Cắt lô · chứng từ", "R"), ("OPS", 7, "Duyệt lô", "A"), ("WH", 7, "Gia cố · pallet", "C"),
    ("FWD", 7, "Booking · HQ xuất", "C"),
    ("BRK", 8, "Khai nhập khẩu", "C"), ("GOV", 8, "Kiểm dịch · thông quan", "C"), ("FIN", 8, "Thuế · GST", "R"),
    ("LOG", 8, "Theo dõi · ETA", "R"),
    ("TPL", 9, "Dỡ hàng · kiểm kiện", "C"), ("LMC", 9, "Hẹn · giao · POD", "C"), ("LOG", 9, "Phân bổ · POD", "R"),
    ("KH", 9, "Nhận · ký POD", "C"),
    ("CX", 10, "D+3 hướng dẫn · review", "R"), ("FIN", 10, "Đối soát chi phí", "R"), ("OPS", 10, "D+14 đóng đơn", "A"),
    ("CX", 11, "Mở · đóng case", "R"), ("OPS", 11, "Duyệt A$51–150", "A"), ("CEO", 11, "> A$150 · 100%", "A"),
    ("FIN", 11, "Hoàn tiền", "R"), ("SRC", 11, "Claim NCC", "R"),
]
MAP_FLOW = [("CEO", 0), ("SRC", 1), ("FIN", 2), ("MKT", 2), ("CX", 3), ("SRC", 4), ("SRC", 5), ("SRC", 6),
            ("LOG", 7), ("LOG", 8), ("LOG", 9), ("CX", 10)]


def operating_map():
    HW, SH, CW, LH = 150, 60, 132, 46
    W, H = HW + CW * len(MAP_STAGES) + 8, SH + LH * len(MAP_LANES) + 8
    cell = {(l, s): (t, k) for l, s, t, k in MAP_CELLS}
    cx = lambda s: HW + s * CW + CW / 2
    cy = lambda l: SH + MAP_LANES.index(l) * LH + LH / 2
    o = [f'<svg class="sw" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
         f'aria-label="Operating map: chuỗi cung ứng end-to-end">',
         f'<title>Operating map: ai làm gì ở từng giai đoạn chuỗi cung ứng</title><style>{CSS}'
         '.sw .mc{fill:var(--panel,#fff);stroke-width:1.3}.sw .mc.A{fill:var(--accent-soft,#f3efe9)}'
         '.sw .mc.C{stroke-dasharray:4 3}.sw .mc.I{stroke-dasharray:1 3}.sw .mt{fill:var(--ink,#1d1d1f);font-size:10px}'
         '.sw .mk{font-size:9px;font-weight:700}.sw .ph{fill:var(--muted,#6e6e73);font-size:9.5px;font-weight:700;letter-spacing:.06em}'
         '.sw .grp{fill:var(--muted,#6e6e73);font-size:9px;font-weight:700;letter-spacing:.08em}</style>',
         '<defs><marker id="ah-map" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
         '<path class="ah" d="M0,0 L10,5 L0,10 z"/></marker></defs>',
         f'<rect class="bg" x="0" y="0" width="{W}" height="{H}" rx="12"/>',
         f'<rect class="hdr" x="0" y="0" width="{HW}" height="{SH}"/>',
         f'<text class="tm" x="12" y="26">Bên liên quan ↓</text><text class="tm" x="12" y="42">Giai đoạn →</text>']
    for i, (code, title, phase) in enumerate(MAP_STAGES):
        x = HW + i * CW
        o.append(f'<rect class="stg" x="{x}" y="0" width="{CW}" height="{SH}"/>')
        o.append(f'<text class="ph" x="{x + 8}" y="16">{escape(phase.upper())}</text>')
        o.append(f'<text class="tb" x="{x + 8}" y="36"><tspan class="ts">{escape(code)}</tspan>  {escape(title)}</text>')
    for j, ln in enumerate(MAP_LANES):
        y = SH + j * LH
        lab, sub, col = ROLE[ln]
        o.append(f'<rect class="lane{" alt" if j % 2 else ""}" x="0" y="{y}" width="{W - 8}" height="{LH}"/>')
        o.append(f'<rect x="0" y="{y}" width="5" height="{LH}" fill="{col}"/>')
        o.append(f'<text class="tb" x="14" y="{y + LH / 2 - 2}" font-size="11">{escape(lab)}</text>')
        o.append(f'<text class="tm" x="14" y="{y + LH / 2 + 11}">{escape(sub)}</text>')
    # group labels: internal vs external
    first_ext = MAP_LANES.index("SUP")
    y = SH + first_ext * LH
    o.append(f'<line x1="0" y1="{y}" x2="{W - 8}" y2="{y}" stroke="currentColor" stroke-width="1.6" opacity=".35"/>')
    for i in range(1, len(MAP_STAGES)):
        x = HW + i * CW
        o.append(f'<line class="sep" x1="{x}" y1="{SH}" x2="{x}" y2="{H - 8}"/>')
    # flow arrows between responsible boxes
    pts = [(cx(s), cy(l)) for l, s in MAP_FLOW]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if abs(x1 - x2) < 1:
            a, b = (x1, y1 + (16 if y2 > y1 else -16)), (x2, y2 + (-16 if y2 > y1 else 16))
            d = f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}"
        else:
            sx, ex = x1 + 58, x2 - 58
            mx = (sx + ex) / 2
            d = f"M{sx:.1f},{y1:.1f} L{mx:.1f},{y1:.1f} L{mx:.1f},{y2:.1f} L{ex:.1f},{y2:.1f}"
        o.append(f'<path class="e" d="{d}" marker-end="url(#ah-map)" opacity=".5"/>')
    for (l, s), (t, k) in cell.items():
        col = ROLE[l][2]
        x, y = cx(s), cy(l)
        o.append(f'<rect class="mc {k}" stroke="{col}" x="{x - 58}" y="{y - 16}" width="116" height="32" rx="7"/>')
        o.append(f'<text class="mk" x="{x - 52}" y="{y - 4}" fill="{col}">{k}</text>')
        words, lines, cur = t.split(), [], ""
        for wd in words:
            if len(cur) + len(wd) + 1 > 19 and cur:
                lines.append(cur); cur = wd
            else:
                cur = (cur + " " + wd).strip()
        lines.append(cur)
        y0 = y - (len(lines) - 1) * 6 + 3.5
        for n, ln in enumerate(lines[:2]):
            o.append(f'<text class="mt" x="{x + 5}" y="{y0 + n * 12:.1f}" text-anchor="middle">{escape(ln)}</text>')
    o.append("</svg>")

    class _M:  # mimic Diagram interface for the writer below
        name, title = "map", "Operating map"
    m = _M(); m.W, m.H = W, H; m.render = lambda: "\n".join(o)
    return m


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "sop"
    out.mkdir(parents=True, exist_ok=True)
    for fn in (sop_a, sop_b1, sop_b2, sop_b3, e0, e1, e2, e3, operating_map):
        dg = fn()
        (out / f"{dg.name}.svg").write_text(dg.render(), encoding="utf-8")
        print("wrote", dg.name, f"{dg.W:.0f}x{dg.H:.0f}")
