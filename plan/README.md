# Plan data – Roadmap, OKR & KPI targets

Thư mục này là **nguồn dữ liệu duy nhất** cho trang *Strategy, OKR & Roadmap* của handbook.
File này được tạo tự động bởi `tools/build_plan.py`: đừng sửa tay, hãy sửa CSV.

| File | Nội dung |
|---|---|
| `roadmap.csv` | Việc và cổng quyết định: workstream, chủ (role), ngày bắt đầu/kết thúc, trạng thái, phụ thuộc, điều kiện cổng |
| `objectives.csv` | Mục tiêu (Objective) cho từng tháng Q4/2026 và từng quý 2027 |
| `kpi_dictionary.csv` | Định nghĩa KPI: loại (North Star / kết quả / đòn bẩy / rào chắn), đơn vị, chiều, cách gộp, chủ, nguồn đo |
| `kpi_targets.csv` | Mục tiêu KPI theo kỳ (định dạng dài: kỳ × KPI × mục tiêu) |
| `orders_plan.csv` | Kế hoạch đơn hàng theo tháng: K01 và North Star được kiểm tra khớp với file này |
| `assumptions.csv` | Giả định: AOV, độ trễ giao, tỉ lệ giao trong khung, ngày lập kế hoạch |

**Chỉ có kế hoạch và mục tiêu.** Số thực tế (doanh thu, chi phí, đơn hàng) nằm trong Google Sheet nội bộ, không commit vào repo công khai này.

## Gantt

```mermaid
gantt
    title Roadmap Q4/2026 – 2027
    dateFormat YYYY-MM-DD
    axisFormat %m/%y
    todayMarker off
    section Nền tảng
    F1 Tên miền, handle 4 kênh, email hỗ trợ (CEO) :active, F1, 2026-10-05, 2026-10-18
    F2 Shopify, Pixel/CAPI, TikTok pixel (MKT) :F2, 2026-10-05, 2026-10-25
    F3 Tracker / Source of truth chạy thật (OPS) :active, F3, 2026-10-05, 2026-10-18
    F4 Chốt bên bán hàng + GST (blocker) (CEO) :F4, 2026-10-12, 2026-11-15
    section Sản phẩm & NCC
    P1 Đối chiếu 60 mã hạng A (SRC) :P1, 2026-10-19, 2026-11-08
    P2 Hàng mẫu – đo, chụp, thử lắp (SRC) :P2, 2026-10-26, 2026-11-15
    P3 NCC ký bộ chứng từ (SRC) :P3, 2026-11-02, 2026-11-15
    P4 Chốt forwarder + đại lý hải quan Úc (LOG) :P4, 2026-10-19, 2026-11-15
    G2 Cổng – ≥ 20 mã đạt 7 tiêu chí :milestone, G2, 2026-11-15, 0d
    section Web & nội dung
    W1 Đăng 20–30 mã chuẩn lên web (MKT) :W1, 2026-11-16, 2026-12-06
    W2 Luật sư Úc rà chính sách (CEO) :W2, 2026-11-16, 2026-12-13
    W3 Kho nội dung 4 trụ + lịch TikTok/FB (MKT) :W3, 2026-10-19, 2026-12-13
    W4 Ký 3–5 creator Úc (MKT) :W4, 2026-11-23, 2026-12-13
    G3 Cổng – web + chính sách đã duyệt :milestone, G3, 2026-12-13, 0d
    section Bán & tăng trưởng
    D1 Bán thử – TikTok → Meta, đo MER (MKT) :D1, 2026-12-14, 2027-01-03
    G4 Cổng – MER ≥ 4 trong 2 tuần :milestone, G4, 2027-01-03, 0d
    D2 Mở rộng quảng cáo theo MER (MKT) :D2, 2027-01-04, 2027-03-31
    D3 Tìm mã thắng + creator/UGC luân phiên (MKT) :D3, 2027-04-01, 2027-06-30
    D4 Bán "giao nhanh từ kho Úc" trên Shopify (MKT) :D4, 2027-08-16, 2027-09-30
    D5 Cao điểm Black Friday / Giáng sinh (MKT) :D5, 2027-11-01, 2027-12-31
    section Logistics & kho
    L1 Lô LCL đầu tiên (gom tuần) (LOG) :L1, 2026-12-21, 2027-01-24
    L2 Giao đơn đầu tiên tới khách Úc (LOG) :L2, 2027-02-01, 2027-03-31
    L3 Chọn 3PL Úc, báo giá, hợp đồng (LOG) :L3, 2027-05-01, 2027-06-30
    G5 Cổng kho Úc – 30–40 đơn/tháng × 2 tháng + ≥ 3 mã thắng :milestone, G5, 2027-06-30, 0d
    L4 Nhập lô đầu vào 3PL (5–10 mã thắng) (LOG) :L4, 2027-07-01, 2027-08-15
    section Quản trị & dữ liệu
    O1 Rà khung ETA theo dữ liệu thật (OPS) :O1, 2027-03-01, 2027-03-15
    O2 Thêm / loại mã theo lãi thực (FIN) :O2, 2027-03-01, 2027-03-31
    O3 Theo dõi tồn – sell-through, vòng quay (FIN) :O3, 2027-08-16, 2027-12-31
    O4 Kế hoạch 2028 (CEO) :O4, 2027-12-01, 2027-12-20
    section Mở rộng
    S1 Cổng nhãn hiệu – quyết nộp đơn IP Australia :milestone, S1, 2027-06-30, 0d
    S2 Nộp nhãn hiệu (nhóm 20 + 35) (CEO) :S2, 2027-07-01, 2027-07-31
    S3 Amazon AU (FBM từ 3PL) – chỉ mã có tồn (OPS) :S3, 2027-10-01, 2027-11-15
    S4 Đánh giá NZ / Singapore (CEO) :S4, 2027-10-01, 2027-12-15
```

## Tổng theo năm (kế hoạch)

| Năm | Tổng đơn | Đơn/tháng cuối năm | Giao trong khung (NS1) | Doanh thu ước tính |
|---|---|---|---|---|
| 2026 | 8 | 8 | 0 | A$7,200 |
| 2027 | 570 | 110 | 333 | A$513,000 |

## Cập nhật

```bash
python tools/build_plan.py   # kiểm tra dữ liệu + tạo lại file này và SVG
python build.py              # build lại website
python tools/check_links.py  # phải báo 0 broken
```
