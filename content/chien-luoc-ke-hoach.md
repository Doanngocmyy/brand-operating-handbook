---
title: Strategy, OKR & Roadmap
badges: internal
---

# Chiến lược, OKR & Roadmap

Trang này là lớp **chiến lược** của handbook: vì sao {{BRAND}} tồn tại, đo thành công bằng gì, và đi theo lộ trình nào từ Q4/2026 đến hết 2027. Việc chi tiết từng tuần của 90 ngày đầu nằm ở [90-Day Launch Plan](lo-trinh-90-ngay.html).

Mọi con số và mốc thời gian trên trang này được dựng từ dữ liệu trong [plan/*.csv](https://github.com/{{REPO}}/tree/main/plan) và được kiểm tra tự động khi build. Đây là **kế hoạch và mục tiêu**, không phải kết quả thực tế.

## Tầm nhìn, sứ mệnh, lợi thế cốt lõi {#vision}

| | |
|---|---|
| **Tầm nhìn** (Vision) | Trở thành thương hiệu nội thất bán trực tiếp đáng tin nhất cho các gia đình ở Úc và New Zealand: khách luôn biết chính xác hàng của mình đang ở đâu và khi nào tới. |
| **Sứ mệnh** (Mission) | Đưa nội thất tối giản, bền, giá hợp lý từ xưởng tới tận nhà khách qua một chuỗi cung ứng do chính đội ngũ điều phối từ đầu tới cuối, với thời gian giao trung thực và người thật chăm sóc sau bán. |
| **Lợi thế cốt lõi** | Năng lực vận hành chuỗi cung ứng end-to-end: chọn NCC và QC tại kho gom, gom lô LCL theo lịch tàu, chứng từ và hải quan, theo dõi từng lô, giao chặng cuối. Tên thương hiệu có thể bị sao chép, còn cách vận hành này thì khó sao chép hơn nhiều. |
| **Định vị** | "Quiet, honest furniture": ít mã, mã nào cũng chuẩn hoá, mô tả đúng, khung giao lấy từ dữ liệu thật. |

Khi nói với khách, dùng cách diễn đạt *"we manage every step from sourcing to your door"*. Không viết "own factory" hay "own warehouse" khi chưa có, theo [Nguyên tắc](nguyen-tac.html).

## North Star và cây KPI {#north-star}

**North Star: số đơn được giao trong khung thời gian đã hứa mỗi tháng (NS1).** Chỉ số này chỉ tăng khi cả hai cùng tăng: nhu cầu (có đơn) và độ tin cậy (giao đúng lời hứa). Bán nhiều mà giao trễ thì NS1 không tăng.

```text
NS1  Đơn giao trong khung / tháng
 ├─ Kết quả     K01 đơn đã thanh toán · K02 doanh thu · K03 lãi thực/đơn · K04 MER
 ├─ Đòn bẩy     danh mục (K14, K05, K06) · nội dung (K07) · chuyển đổi (K08) · mã thắng (K09) · tồn Úc (K10, K11)
 └─ Rào chắn    G01 giao trong khung % · G02 phản hồi · G03 case · G04 chargeback · G05 huỷ/hoàn · G06–G07 Amazon
```

Quy tắc đọc: đòn bẩy là thứ team tác động trực tiếp hằng tuần. Rào chắn là lằn ranh: vượt ngưỡng thì **dừng mở rộng** dù chỉ số kết quả đang đẹp.

{{KPI_DICT}}

## Roadmap Q4/2026 – 2027 {#gantt}

Bảy luồng việc. Cổng (hình thoi) là điểm dừng để quyết định bằng dữ liệu: chưa qua cổng thì không làm bước sau.

{{PLAN:gantt}}

## Kế hoạch đơn hàng và North Star {#orders}

Cột là số đơn đã thanh toán theo kế hoạch. Đường xanh là North Star suy ra từ giả định: đơn đặt ở tháng *m* được giao ở tháng *m + 2* (trung vị 8–9 tuần), với 90% giao trong khung. Từ Q3/2027, phần hàng có sẵn ở kho Úc sẽ giao nhanh hơn, nên North Star thực tế có thể cao hơn đường này.

{{PLAN:orders}}

{{YEAR_SUMMARY}}

## Q4/2026 theo tháng {#q4-2026}

Mục tiêu năm 2026: **sẵn sàng bán một cách trung thực.** Hết tháng 12 phải có web và chính sách đã duyệt, 0 launch blocker, và dữ liệu nhu cầu thật từ đợt bán thử.

{{OKR:2026-10}}

{{OKR:2026-11}}

{{OKR:2026-12}}

## 2027 theo quý {#y2027}

Mục tiêu năm 2027: **từ dropship minh bạch sang có hàng sẵn tại Úc cho mã thắng, rồi mở Amazon AU**, trong khi luôn giữ ≥ 90% đơn giao trong khung đã hứa.

{{OKR:2027-Q1}}

{{OKR:2027-Q2}}

{{OKR:2027-Q3}}

{{OKR:2027-Q4}}

## Cổng quyết định {#gates}

| Cổng | Điều kiện (đo bằng dữ liệu) | Quyết định khi đạt | Dự kiến |
|---|---|---|---|
| Mở rộng quảng cáo | MER ≥ 4 trong 2 tuần liên tiếp, G05 ≤ 5% | Tăng ngân sách theo bậc, mỗi bậc giữ 1 tuần | 01/2027 |
| Kho tại Úc (3PL) | 30–40 đơn Úc/tháng ổn định 2 tháng **và** ≥ 3 mã thắng | Nhập lô LCL đầu cho 5–10 mã thắng vào 3PL | 06/2027 |
| Nộp nhãn hiệu tại Úc | Qua cổng kho Úc, hoặc chuẩn bị chi quảng cáo lớn, hoặc trước khi lên Amazon | Nộp IP Australia nhóm 20 (nội thất) + 35 (bán lẻ online) | 07/2027 |
| Amazon AU | Có tồn tại Úc; tự đo được Late Shipment < 4%, Valid Tracking > 95%, huỷ < 2,5% | Mở FBM từ kho 3PL, chỉ mã có sẵn | 10/2027 |
| NZ / Singapore | G01 ≥ 90% trong 3 tháng liên tiếp, lãi thực ≥ 30% | Lập kế hoạch thị trường thứ hai cho 2028 | Q4/2027 |

Trước khi qua cổng nhãn hiệu: giữ tên miền và handle, lưu bằng chứng ngày bắt đầu dùng tên. Đây là hướng dẫn vận hành, không phải tư vấn pháp lý.

## Cập nhật kế hoạch {#update}

| Nhịp | Ai | Việc |
|---|---|---|
| Thứ Sáu hằng tuần | <span class="r ops">OPS</span> | Cập nhật cột `status` trong `plan/roadmap.csv` |
| Ngày 01 hằng tháng | <span class="r ceo">CEO</span> + <span class="r ops">OPS</span> | So kết quả thực (Google Sheet) với mục tiêu tháng/quý; chỉnh `kpi_targets.csv`, `orders_plan.csv` nếu cần |
| Cuối quý | <span class="r ceo">CEO</span> | Chấm OKR quý, chốt Objective quý sau trong `objectives.csv` |

```bash
python tools/build_plan.py   # kiểm tra dữ liệu, tạo plan/README.md (Gantt Mermaid) + SVG
python build.py              # build lại website
python tools/check_links.py  # phải báo 0 broken
```

Repo này công khai: **chỉ commit kế hoạch và mục tiêu**. Số thực tế (doanh thu, chi phí, đơn hàng) chỉ nằm trong Google Sheet nội bộ.
