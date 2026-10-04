# Operating Handbook - DTC furniture brand (AU → SG)

Hệ điều hành vận hành cho một brand nội thất bán trực tiếp (DTC) tại Úc và Singapore: team ở Việt Nam, hàng sản xuất tại Trung Quốc. Website mở ở **Operating Map**: chọn theo vị trí, theo việc đang xảy ra, hoặc theo giai đoạn đơn S1–S8.

**Bản web:** GitHub Pages của repo này (thư mục `docs/`).

## Cấu trúc thông tin

| Nhóm | Trang |
|---|---|
| Start here | Operating Map · Find by role · Find by task / event |
| Run the business | Standard Order (SOP-A) · Exceptions & Cases (SOP-B) · KPI, SLA & Rhythm |
| Standards | Product & SKU · Supplier & QC · Packaging, Labels & Import Docs · Brand & Marketing Rules · Customer-facing Policy |
| Management | Roles, Authority & Access · Business Model & Unit Economics · Strategy, OKR & Roadmap · 90-Day Launch Plan · Tools & Templates |
| About | Operating principles · Founder note |

## Cấu trúc repo

```
content/      Markdown của từng trang (sửa nội dung ở đây)
plan/         Roadmap (Gantt), OKR, KPI targets dạng CSV: nguồn dữ liệu của trang Strategy, OKR & Roadmap
plan_data.py  Đọc + kiểm tra plan/*.csv, vẽ Gantt/biểu đồ SVG, bảng OKR
site_map.py   Menu, thẻ vị trí/sự kiện, bản đồ S1–S8, control panel SOP, source of truth, launch blockers
assets/       CSS + swimlane SVG (assets/sop, tạo bởi tools/swimlane.py)
docs/         Website đã build (GitHub Pages) + trang chuyển hướng từ URL cũ
templates/    Biểu mẫu: SOP-Tracker.xlsx (Excel), SOT-Google-Sheet.xlsx (bản cho Google Sheets), chứng từ NCC
tools/        swimlane.py · build_tracker.py · build_sot_sheet.py · check_links.py · script dữ liệu sản phẩm
site.json     Tên brand, repo, link Google Sheet - đổi một lần là đổi toàn bộ
build.py      Tạo lại docs/ từ content/ + site_map.py
```

```bash
pip install markdown
python tools/build_plan.py   # kiểm tra plan/*.csv, tạo plan/README.md
python build.py
python tools/check_links.py   # phải báo 0 broken
```

## Quy tắc bảo mật (repo công khai)

- Không commit dữ liệu khách hàng, đơn hàng, thông tin NCC, chi phí thực, file Excel gốc, mật khẩu, token.
- Chỉ đưa lên số liệu đã tổng hợp và quy trình. Trang có nhãn **Internal** là logic nội bộ: cân nhắc trước khi chia sẻ link.
- `.gitignore` chặn `*.xlsx`, `*.csv` ngoài thư mục `templates/`, và các thư mục dữ liệu.

*Các nội dung pháp lý là hướng dẫn vận hành, không phải tư vấn pháp lý.*
