---
title: KPI & tracking
order: 11
---

# KPI, cờ cảnh báo và nhịp vận hành

Mỗi giai đoạn trong SOP có **1 KPI, 1 chủ, 1 cột trong tracker**. Tracker tự tính trạng thái và bật cờ, người chỉ nhập ngày khi có bằng chứng.

**Công cụ:** [SOP-Tracker.xlsx](https://github.com/{{REPO}}/raw/main/templates/SOP-Tracker.xlsx) · 5 tab: Hướng dẫn · Dashboard · DON (đơn) · CASE (hậu mãi) · DS (danh mục). Không có cột dữ liệu cá nhân của khách; mã đơn là khóa nối.

## 1. Cây KPI theo giai đoạn

| Giai đoạn | KPI | Cách đo (cột tracker) | Mục tiêu | Chủ |
|---|---|---|---|---|
| S1 Nhận đơn | Xác nhận đúng hạn | Ngày `20 Xác nhận` − `Ngày thanh toán` | 100% trong ngày | <span class="r cx">CX</span> |
| S2 Đặt NCC | Đặt NCC ≤ 24h | `S1–S2 TT→Đặt NCC` ≤ 1 | ≥ 95% | <span class="r src">SRC</span> |
| S3 SX & gửi | NCC gửi đúng hẹn | `40 NCC gửi` ≤ `Hẹn NCC gửi` + 2 | ≥ 90% | <span class="r src">SRC</span> |
| S4 QC | Lỗi lọt QC | Case RC-QC ÷ đơn đã giao | ≤ 1% | <span class="r src">SRC</span> |
| S5 Xuất lô | Fulfilled đúng luật | Đơn `60` có lượt quét thật (kiểm 10 đơn/tuần) | 100% | <span class="r log">LOG</span> |
| S6–S7 | Lead time biển + giao | `S6–S7 Xuất→Giao` trung bình | theo dõi, rà khung mỗi tháng | <span class="r log">LOG</span> |
| Toàn đơn | **Giao trong khung đã hứa** | `Giao trong khung` = Có | ≥ 90% | <span class="r ops">OPS</span> |
| Toàn đơn | Cập nhật khách đều | Cờ `>7d chưa cập nhật KH` | 0 | <span class="r cx">CX</span> |
| Hậu mãi | Phản hồi đầu | `Giờ phản hồi` trung vị | ≤ 4h LV (tối đa 24h) | <span class="r cx">CX</span> |
| Hậu mãi | Tỉ lệ case | Số case ÷ số đơn | ≤ 3% | <span class="r ops">OPS</span> |
| Hậu mãi | Chargeback | Case C7 ÷ số đơn | ≤ 0,5% | <span class="r ops">OPS</span> |
| Hậu mãi | Duyệt đúng cấp | Cờ `Duyệt sai cấp` | 0 | <span class="r ops">OPS</span> |
| Tài chính | Lãi thực/đơn | Landed cost thực (file chi phí riêng) | ≥ 30% | <span class="r fin">FIN</span> |
| Tăng trưởng | MER | Doanh thu ÷ chi quảng cáo | ≥ 4 | <span class="r mkt">MKT</span> |

## 2. Cờ SLA (tự bật trong tracker)

| Cờ | Bật khi | Ai xử lý | Hành động |
|---|---|---|---|
| <span class="flag">Chưa đặt NCC &gt;24h</span> | Đã thanh toán > 1 ngày, chưa có PO | <span class="r src">SRC</span> | Đặt ngay hoặc chuyển NCC dự phòng |
| <span class="flag">NCC quá hẹn &gt;2d</span> | Quá hẹn gửi 2 ngày, chưa có vận đơn | <span class="r src">SRC</span> → <span class="r ops">OPS</span> | +2d nhắc · +5d OPS + báo khách · +7d đổi NCC |
| <span class="flag amber">Sắp vượt ETA</span> | Còn ≤ 14 ngày tới ETA max, chưa xuất | <span class="r cx">CX</span> | Mở case C2, báo khách trước ≥ 7 ngày |
| <span class="flag">Vượt ETA</span> | Quá ETA max, chưa giao | <span class="r cx">CX</span> | Đề nghị tín dụng 5% hoặc hủy hoàn 100% |
| <span class="flag amber">&gt;7d chưa cập nhật KH</span> | Lần liên hệ gần nhất > 7 ngày | <span class="r cx">CX</span> | Gửi cập nhật tuần, ghi ngày |
| <span class="flag">Case phản hồi &gt;24h</span> | Chưa có người thật trả lời sau 24h | <span class="r cx">CX</span> | Trả lời ngay, lên đầu họp 09:00 |
| <span class="flag amber">Case mở &gt;7 ngày</span> | Case chưa đóng sau 7 ngày | <span class="r ops">OPS</span> | Gọi khách, chốt giải pháp |
| <span class="flag">Duyệt sai cấp</span> | Người duyệt thấp hơn mức cần | <span class="r ops">OPS</span> | Rà lại, ghi lý do |

## 3. Dashboard (tab DASHBOARD)

| Khối | Câu hỏi nó trả lời | Dùng ở đâu |
|---|---|---|
| 8 ô KPI | Hôm nay mình đứng ở đâu so với mục tiêu? | Họp 09:00 |
| Đơn theo trạng thái | Đơn đang dồn ở giai đoạn nào? | Họp 09:00 |
| Cờ SLA đang bật | Việc gì phải xử lý **ngay hôm nay**? | Họp 09:00 |
| Lead time theo giai đoạn | Giai đoạn nào chậm nhất, khung ETA còn đúng không? | Báo cáo tuần · rà khung tháng |
| Case theo loại | Khách đang gặp vấn đề gì nhiều nhất? | Báo cáo tuần |
| Nguyên nhân gốc | Lỗi do ai, sửa quy trình nào, đòi tiền ai? | Báo cáo tuần |

## 4. Nhịp vận hành

| Nhịp | Khi nào | Ai | Đầu vào → Đầu ra |
|---|---|---|---|
| Control tower | 09:00 hằng ngày, 15 phút | <span class="r ops">OPS</span> + mọi vị trí | Dashboard, cờ đỏ → mỗi cờ có tên người xử lý trong ngày |
| Báo cáo tuần | Thứ Sáu 16:00 | <span class="r ops">OPS</span> → <span class="r ceo">CEO</span> | Dashboard + case theo nguyên nhân → SKU/NCC tắt, sửa SOP |
| Đối soát | Thứ Sáu | <span class="r fin">FIN</span> | Chi phí thực từng đơn đã đóng → lãi thực, mã cần tăng giá |
| Rà khung ETA | Ngày 01 hằng tháng | <span class="r ops">OPS</span> | Lead time thực → nếu 10% đơn chậm nhất vượt khung thì nới khung |
| Rà lằn ranh đỏ | Ngày 01 hằng tháng | <span class="r ops">OPS</span> + <span class="r mkt">MKT</span> | Web, quảng cáo, email theo [Nguyên tắc](01-nguyen-tac.html) |

## 5. Checklist hằng ngày theo vị trí

| Giờ (VN) | <span class="r cx">CX</span> | <span class="r src">SRC</span> | <span class="r log">LOG</span> | <span class="r ops">OPS</span> |
|---|---|---|---|---|
| 07:00 | Hộp thư, khách Úc trước | Tin nhắn NCC qua đêm | Tracking lô đang chạy | – |
| 09:00 | Họp control tower | Họp control tower | Họp control tower | **Chủ trì**, giao cờ |
| Sáng | Kiểm + xác nhận đơn mới (S1) | Đặt PO mọi đơn `20` (S2) | Chứng từ lô tuần (S5) | Duyệt leo thang, duyệt A$51–150 |
| Chiều | Cập nhật 7 ngày, case mới | Duyệt ảnh kiện, QC, claim NCC | Hải quan, hãng giao, thu hồi | Kiểm ngẫu nhiên 2 đơn: tin nhắn khớp trạng thái? |
| Cuối ngày | Không case nào > 24h chưa trả lời | Tracker đủ ngày + bằng chứng | Tracker đủ ngày + bằng chứng | – |

## 6. Mẫu báo cáo tuần

```text
Tuần: __/__ – __/__                       (dán ảnh DASHBOARD)
1. Đơn: mới __ · đã giao __ · giao trong khung __% · đang có cờ đỏ __
2. Giai đoạn chậm nhất: ____ (lead time __ ngày, mục tiêu __)
3. Case: mới __ · đóng __ · mở > 7 ngày __ · chi phí ròng A$__
4. Top nguyên nhân gốc: ____ → sửa gì, ai sửa, hạn
5. SKU / NCC đề xuất tắt hoặc tăng giá:
6. Quảng cáo: chi __ · doanh thu __ · MER __
7. Việc cần CEO quyết:
```
