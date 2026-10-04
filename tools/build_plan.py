"""Validate plan/*.csv and regenerate the GitHub-readable roadmap (plan/README.md) + SVG charts.

Usage:  python tools/build_plan.py          (then: python build.py)
Fails (exit 1) when the data is inconsistent: unknown KPI/owner/workstream, dependency order,
K01 targets that do not match orders_plan.csv, NS1 targets that do not match the derived plan.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import plan_data as P  # noqa: E402

data = P.load()
errs = P.validate(data)
if errs:
    print("Plan data has problems:")
    for e in errs:
        print("  -", e)
    sys.exit(1)

out = P.ROOT / "assets" / "plan"
out.mkdir(parents=True, exist_ok=True)
(out / "gantt.svg").write_text(P.render_gantt_svg(data), encoding="utf-8")
(out / "orders.svg").write_text(P.render_orders_svg(data), encoding="utf-8")

yt = P.year_totals(data)
ns = P.north_star_plan(data)
lines = [
    "# Plan data – Roadmap, OKR & KPI targets",
    "",
    "Thư mục này là **nguồn dữ liệu duy nhất** cho trang *Strategy, OKR & Roadmap* của handbook.",
    "File này được tạo tự động bởi `tools/build_plan.py`: đừng sửa tay, hãy sửa CSV.",
    "",
    "| File | Nội dung |",
    "|---|---|",
    "| `roadmap.csv` | Việc và cổng quyết định: workstream, chủ (role), ngày bắt đầu/kết thúc, trạng thái, phụ thuộc, điều kiện cổng |",
    "| `objectives.csv` | Mục tiêu (Objective) cho từng tháng Q4/2026 và từng quý 2027 |",
    "| `kpi_dictionary.csv` | Định nghĩa KPI: loại (North Star / kết quả / đòn bẩy / rào chắn), đơn vị, chiều, cách gộp, chủ, nguồn đo |",
    "| `kpi_targets.csv` | Mục tiêu KPI theo kỳ (định dạng dài: kỳ × KPI × mục tiêu) |",
    "| `orders_plan.csv` | Kế hoạch đơn hàng theo tháng: K01 và North Star được kiểm tra khớp với file này |",
    "| `assumptions.csv` | Giả định: AOV, độ trễ giao, tỉ lệ giao trong khung, ngày lập kế hoạch |",
    "",
    "**Chỉ có kế hoạch và mục tiêu.** Số thực tế (doanh thu, chi phí, đơn hàng) nằm trong Google Sheet nội bộ, không commit vào repo công khai này.",
    "",
    "## Gantt",
    "",
    P.render_mermaid(data),
    "",
    "## Tổng theo năm (kế hoạch)",
    "",
    "| Năm | Tổng đơn | Đơn/tháng cuối năm | Giao trong khung (NS1) | Doanh thu ước tính |",
    "|---|---|---|---|---|",
]
orders = {m: n for m, n, _ in data["orders"]}
for y, v in yt.items():
    exit_m = max(m for m in orders if m.startswith(y))
    lines.append(f"| {y} | {v['orders']} | {orders[exit_m]} | {sum(n for m, n in ns.items() if m.startswith(y))} | A${v['revenue']:,.0f} |")
lines += ["", "## Cập nhật", "", "```bash", "python tools/build_plan.py   # kiểm tra dữ liệu + tạo lại file này và SVG",
          "python build.py              # build lại website", "python tools/check_links.py  # phải báo 0 broken", "```", ""]
(P.PLAN / "README.md").write_text("\n".join(lines), encoding="utf-8")
print(f"Plan OK: {len(data['tasks'])} tasks, {len(data['objectives'])} objectives, {len(data['targets'])} KPI targets")
