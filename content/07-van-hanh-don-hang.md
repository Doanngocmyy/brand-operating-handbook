---
title: SOP-A · Đơn chuẩn
order: 7
---

# SOP-A · Đơn chuẩn (normal case)

Một đơn đi qua **8 giai đoạn, 10 trạng thái**. Đơn chuẩn không cần CEO. Mọi lệch chuẩn thoát sang [SOP-B](08-cskh.html) bằng mã case.

<div class="flow">
<div class="st"><b>S1 · ≤ 4h LV</b><span class="n">Nhận đơn</span><span class="r cx">CX</span><small>→ <span class="s">20</span> đã xác nhận</small></div>
<div class="st"><b>S2 · ≤ 24h</b><span class="n">Đặt NCC</span><span class="r src">SRC</span> <span class="r fin">FIN</span><small>→ <span class="s">30</span> đã đặt</small></div>
<div class="st"><b>S3 · ≤ hẹn +2d</b><span class="n">SX &amp; gửi</span><span class="r src">SRC</span><small>→ <span class="s">40</span> NCC đã gửi</small></div>
<div class="st"><b>S4 · ≤ 2d</b><span class="n">Kho gom · QC</span><span class="r src">SRC</span><small>→ <span class="s">50</span> QC đạt</small></div>
<div class="st"><b>S5 · 1 ngày/tuần</b><span class="n">Xuất lô</span><span class="r log">LOG</span> <span class="r ops">OPS</span><small>→ <span class="s">60</span> đã xuất</small></div>
<div class="st"><b>S6 · báo ≤ 24h</b><span class="n">Thông quan</span><span class="r log">LOG</span><small>→ <span class="s">70</span> thông quan</small></div>
<div class="st"><b>S7 · hãng hẹn</b><span class="n">Giao cuối</span><span class="r log">LOG</span><small>→ <span class="s">80</span> → <span class="s">90</span></small></div>
<div class="st"><b>S8 · D+3 · D+14</b><span class="n">Sau giao · đóng</span><span class="r cx">CX</span> <span class="r fin">FIN</span><small>→ <span class="s">99</span> đóng</small></div>
</div>

## 1. Swimlane

<div class="legend"><span>▭ việc nội bộ</span><span>◇ quyết định</span><span>⬭ bắt đầu / kết thúc</span><span>┄▭ đối tác ngoài</span><span>── luồng việc</span><span>┄┄ thông báo</span><span><span class="s">30</span> trạng thái đặt ra</span><span><span class="flag">đỏ</span> lối thoát ngoại lệ</span></div>

{{SVG:a}}

## 2. Cổng qua từng giai đoạn

Chỉ chuyển trạng thái khi **có bằng chứng** ở cột cuối. Không có bằng chứng = chưa xong.

| Giai đoạn | Chủ trì | Việc chính | SLA | Cổng qua (bằng chứng) | → |
|---|---|---|---|---|---|
| S1 Nhận đơn | <span class="r cx">CX</span> | Kiểm địa chỉ giao được, SĐT, dấu hiệu gian lận. Email xác nhận với khung ETA thật | ≤ 4h làm việc | Email xác nhận đã gửi · dòng tracker có ETA min/max | <span class="s">20</span> |
| S2 Đặt NCC | <span class="r src">SRC</span> | Hỏi tồn + ngày xuất. PO đúng mã màu/size, 1 NCC/đơn. Gửi yêu cầu đóng gói | ≤ 24h sau thanh toán | Mã PO + ngày hẹn xuất · FIN đã thanh toán qua sàn | <span class="s">30</span> |
| S3 SX & gửi | <span class="r src">SRC</span> | Nhận ảnh/video đóng kiện X/Y, duyệt, nhận vận đơn nội địa | ≤ ngày hẹn +2d | Ảnh kiện đã duyệt · vận đơn nội địa | <span class="s">40</span> |
| S4 Kho gom · QC | <span class="r src">SRC</span> | Đếm kiện, QC màu, kích thước (±5 mm), phụ kiện, ISPM-15. Lỗi: trả NCC tại TQ | ≤ 2d sau nhập kho | Ảnh QC của đơn · checklist QC đạt | <span class="s">50</span> |
| S5 Xuất lô | <span class="r log">LOG</span> | Cắt lô 1 ngày cố định/tuần. CI, PL, ISPM, ChAFTA, BMSB. OPS duyệt chứng từ khớp hàng | theo lịch tuần | **Lượt quét thật** của hãng vận chuyển | <span class="s">60</span> |
| S6 Thông quan | <span class="r log">LOG</span> | Theo dõi cảng, broker khai báo, nộp thuế/GST. Bị giữ: báo khách ≤ 24h | báo ≤ 24h | Tracking báo tới cảng/hải quan | <span class="s">70</span> |
| S7 Giao cuối | <span class="r log">LOG</span> | Bàn giao hãng nội địa, hãng hẹn ngày, giao đủ kiện X/Y | theo hẹn | Hãng nhận hàng → POD/ảnh giao | <span class="s">80</span>→<span class="s">90</span> |
| S8 Sau giao | <span class="r cx">CX</span> <span class="r fin">FIN</span> | D+3 hướng dẫn lắp + mời review (mọi khách). FIN đối soát landed cost | D+3 · D+14 | D+14 không case · chi phí đủ | <span class="s">99</span> |

## 3. Trạng thái đơn

| Mã | Trạng thái | Shopify | Khách được báo |
|---|---|---|---|
| <span class="s">10</span> | Mới (đã thanh toán) | Unfulfilled | – |
| <span class="s">20</span> | Đã xác nhận | Unfulfilled | Email xác nhận + khung ETA |
| <span class="s">30</span> | Đã đặt NCC | Unfulfilled | Cập nhật 7 ngày: "đang sản xuất" |
| <span class="s">40</span> | NCC đã gửi | Unfulfilled | Cập nhật 7 ngày |
| <span class="s">50</span> | QC đạt | Unfulfilled | Ảnh QC của chính đơn |
| <span class="s">60</span> | Đã xuất | **Fulfilled + tracking** | Email tracking |
| <span class="s">70</span> | Thông quan | Fulfilled | Cập nhật 7 ngày |
| <span class="s">80</span> | Đang giao | Fulfilled | Hãng giao hẹn ngày |
| <span class="s">90</span> | Đã giao | Fulfilled | Hướng dẫn lắp (D+3) |
| <span class="s">99</span> | Đóng | Archived | – |
| <span class="s">95</span> | Hủy / hoàn | Refunded | Email hoàn tiền |

> **Không bấm Fulfilled, không gửi tracking khi chưa có lượt quét thật.** Trạng thái trên Shopify, trong tracker và trong tin nhắn khách phải giống nhau.

## 4. Lối thoát ngoại lệ

| Điểm | Tình huống | Ai phát hiện | Xử lý | Sang |
|---|---|---|---|---|
| S1 | Địa chỉ không giao được, nghi gian lận | <span class="r cx">CX</span> | Hỏi lại trong 24h, không trả lời thì hủy | C1 |
| S2 | Cả 2 NCC hết hàng | <span class="r src">SRC</span> | Báo khách ≤ 24h: đổi mã hoặc hủy hoàn 100% | C1 · C2 |
| S3 | NCC trễ hẹn | <span class="r src">SRC</span> → <span class="r ops">OPS</span> | +2d nhắc · +5d báo OPS, báo khách · +7d đổi NCC | C2 nếu chạm ETA |
| S4 | QC trượt | <span class="r src">SRC</span> | Trả NCC tại TQ, làm lại; báo khách nếu lùi ETA | C2 |
| S6 | Bị giữ hải quan, kiểm dịch | <span class="r log">LOG</span> | Báo khách ≤ 24h, lý do thật, ngày mới | C2 |
| Mọi lúc | Còn 14 ngày tới ETA max mà chưa <span class="s">60</span> | Tracker | CX báo trước ≥ 7 ngày, đưa 3 lựa chọn | C2 |
| S8 | Khách báo vấn đề | <span class="r cx">CX</span> | Mở case | C3–C8 |

## 5. Ba việc chạy liên tục

| Việc | Ai | Nhịp |
|---|---|---|
| Control tower: rà mọi cờ SLA trong tracker | <span class="r ops">OPS</span> | 09:00 hằng ngày |
| Cập nhật chủ động cho khách, kể cả "tuần này chưa có gì mới" | <span class="r cx">CX</span> | mỗi 7 ngày/đơn, tới khi giao |
| Ghi bằng chứng vào tracker (mã PO, ảnh, vận đơn, POD) | Chủ trì từng giai đoạn | ngay khi có |

Tracker, cờ cảnh báo và KPI: [KPI & tracking](11-kpi-nhip-van-hanh.html).
