---
title: Công cụ & biểu mẫu
order: 13
---

# Công cụ và biểu mẫu

## Biểu mẫu (tải về dùng ngay)

| File | Dùng để | Ai dùng |
|---|---|---|
| [SOP-Tracker.xlsx](https://github.com/{{REPO}}/raw/main/templates/SOP-Tracker.xlsx) | Theo dõi đơn (SOP-A) và case hậu mãi (SOP-B): trạng thái tự tính, cờ SLA, dashboard KPI. Không có dữ liệu cá nhân khách | Cả team, họp 09:00 |
| Swimlane: [SOP-A](sop/a.svg) · [B1 case](sop/b1.svg) · [B2 trả hàng](sop/b2.svg) · [B3 chargeback](sop/b3.svg) | Bản lớn để in, dán tường, đào tạo người mới | Cả team |
| [Mau_chung_tu_NCC.xlsx](https://github.com/{{REPO}}/raw/main/templates/Mau_chung_tu_NCC.xlsx) | Commercial invoice, packing list, shipping mark, nhãn sản phẩm, hướng dẫn lắp, QC checklist. Song ngữ Anh–Trung cho NCC | Mua hàng & QC, NCC |
| [order-tracker-template.csv](https://github.com/{{REPO}}/blob/main/templates/order-tracker-template.csv) | Bản cũ có cột chi phí thực từng đơn. Dùng làm file chi phí riêng của FIN (không chia sẻ cho CX, MKT) | FIN |
| [status-list.csv](https://github.com/{{REPO}}/blob/main/templates/status-list.csv) | Danh sách trạng thái đơn và điều kiện chuyển | Cả team |

Cách dùng bộ chứng từ NCC:

1. Gửi file cho NCC kèm đơn đặt hàng (PO) và mã SKU của {{BRAND}}.
2. NCC điền ô vàng, gửi lại kèm ảnh và video đóng kiện **trước khi xuất hàng**.
3. Mua hàng & QC duyệt trong 24 giờ. Sau đó NCC mới dán nhãn và giao cho forwarder.
4. Lưu toàn bộ theo số container.

## Công cụ dữ liệu sản phẩm (Python)

| Script | Làm gì |
|---|---|
| [tools/catalog_export.py](https://github.com/{{REPO}}/blob/main/tools/catalog_export.py) | Xuất toàn bộ sản phẩm, biến thể, ảnh từ một Shopify store **bạn sở hữu hoặc được phép dùng** (dữ liệu công khai `/products.json`), kiểm tra đủ theo sitemap |
| [tools/normalize_catalog.py](https://github.com/{{REPO}}/blob/main/tools/normalize_catalog.py) | Chuẩn hóa: 8 nhóm chính, hạng A/B/C, màu chuẩn, kích thước W × D × H (cm), mã sản phẩm và SKU mới, thư mục ảnh theo hạng/nhóm/mã/màu |

```bash
pip install requests openpyxl pandas
python tools/catalog_export.py --store https://your-store.example --out export_store --images none
python tools/normalize_catalog.py --raw export_store/raw_products.json --out clean_db --store-url https://your-store.example
# tải ảnh hạng A, tối đa 8 ảnh mỗi màu:
python tools/normalize_catalog.py --raw export_store/raw_products.json --out clean_db --download-images A
```

Kết quả: `01_categories.csv`, `02_products.csv`, `03_variants.csv`, `04_colour_map.csv`, `05_images.csv`, `clean_catalogue_review.xlsx`.

**Quy tắc dữ liệu:**

- Dữ liệu sản phẩm, file Excel gốc, dữ liệu đơn và NCC **không commit** lên repo này (repo công khai). `.gitignore` đã chặn.
- Thông số đăng web lấy từ NCC đã đối chiếu, không lấy nguyên từ store cũ.
- Viết lại tên và mô tả theo giọng {{BRAND}}. Không dùng giá gạch cũ.

## Sửa sổ tay này

Mỗi trang là một file Markdown trong thư mục `content/`. Sửa file rồi chạy `python build.py` để tạo lại website trong `docs/`. Tên thương hiệu nằm ở `site.json`, đổi một lần là đổi toàn bộ.

| Muốn sửa | Sửa ở | Rồi chạy |
|---|---|---|
| Swimlane (ô, mũi tên, SLA) | `tools/swimlane.py` | `python tools/swimlane.py` → `python build.py` |
| Tracker Excel | `tools/build_tracker.py` | `python tools/build_tracker.py` |
| Chữ trên trang | `content/*.md` (`{{SVG:a}}` = chèn swimlane) | `python build.py` |
