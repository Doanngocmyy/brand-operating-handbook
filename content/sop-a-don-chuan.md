---
title: SOP-A · Đơn chuẩn
badges: daily, internal
order: 7
---

# SOP-A · Đơn chuẩn (normal case) {#sop-a}

Một đơn đi qua **8 giai đoạn, 10 trạng thái**. Đơn chuẩn không cần CEO. Mọi lệch chuẩn thoát sang [SOP-B](sop-b-hau-mai.html) bằng mã case.

{{PANEL:sop-a}}

{{SOT:order,supplier,shipment,promise}}

<div class="flow" id="flow">
<a class="st" href="#s1"><b>S1 · ≤ 4h LV</b><span class="n">Nhận đơn</span><span class="r cx">CX</span><small>→ <span class="s">20</span> đã xác nhận</small></a>
<a class="st" href="#s2"><b>S2 · ≤ 24h</b><span class="n">Đặt NCC</span><span class="r src">SRC</span> <span class="r fin">FIN</span><small>→ <span class="s">30</span> đã đặt</small></a>
<a class="st" href="#s3"><b>S3 · ≤ hẹn +2d</b><span class="n">SX &amp; gửi</span><span class="r src">SRC</span><small>→ <span class="s">40</span> NCC đã gửi</small></a>
<a class="st" href="#s4"><b>S4 · ≤ 2d</b><span class="n">Kho gom · QC</span><span class="r src">SRC</span><small>→ <span class="s">50</span> QC đạt</small></a>
<a class="st" href="#s5"><b>S5 · 1 ngày/tuần</b><span class="n">Xuất lô</span><span class="r log">LOG</span> <span class="r ops">OPS</span><small>→ <span class="s">60</span> đã xuất</small></a>
<a class="st" href="#s6"><b>S6 · báo ≤ 24h</b><span class="n">Thông quan</span><span class="r log">LOG</span><small>→ <span class="s">70</span> thông quan</small></a>
<a class="st" href="#s7"><b>S7 · hãng hẹn</b><span class="n">Giao cuối</span><span class="r log">LOG</span><small>→ <span class="s">80</span> → <span class="s">90</span></small></a>
<a class="st" href="#s8"><b>S8 · D+3 · D+14</b><span class="n">Sau giao · đóng</span><span class="r cx">CX</span> <span class="r fin">FIN</span><small>→ <span class="s">99</span> đóng</small></a>
</div>

## 1. Swimlane {#swimlane}

<div class="legend"><span>▭ việc nội bộ</span><span>◇ quyết định</span><span>⬭ bắt đầu / kết thúc</span><span>┄▭ đối tác ngoài</span><span>── luồng việc</span><span>┄┄ thông báo</span><span><span class="s">30</span> trạng thái đặt ra</span><span><span class="flag">đỏ</span> lối thoát ngoại lệ</span></div>

{{SVG:a}}

## 2. Cổng qua từng giai đoạn {#gates}

Chỉ chuyển trạng thái khi **có bằng chứng** ở cột cuối. Không có bằng chứng = chưa xong.

| Giai đoạn | Chủ trì | Việc chính | SLA | Cổng qua (bằng chứng) | → |
|---|---|---|---|---|---|
| <span class="anchor" id="s1"></span>**S1 Nhận đơn** | <span class="r cx">CX</span> | Kiểm địa chỉ giao được, SĐT, dấu hiệu gian lận. Email xác nhận với khung ETA thật | ≤ 4h làm việc | Email xác nhận đã gửi · dòng tracker có ETA min/max | <span class="s">20</span> |
| <span class="anchor" id="s2"></span>**S2 Đặt NCC** | <span class="r src">SRC</span> | Hỏi tồn + ngày xuất. PO đúng mã màu/size, 1 NCC/đơn. Gửi yêu cầu đóng gói | ≤ 24h sau thanh toán | Mã PO + ngày hẹn xuất · FIN đã thanh toán qua sàn | <span class="s">30</span> |
| <span class="anchor" id="s3"></span>**S3 SX & gửi** | <span class="r src">SRC</span> | Nhận ảnh/video đóng kiện X/Y, duyệt, nhận vận đơn nội địa | ≤ ngày hẹn +2d | Ảnh kiện đã duyệt · vận đơn nội địa | <span class="s">40</span> |
| <span class="anchor" id="s4"></span>**S4 Kho gom · QC** | <span class="r src">SRC</span> | Đếm kiện, QC màu, kích thước (±5 mm), phụ kiện, ISPM-15. Lỗi: trả NCC tại TQ | ≤ 2d sau nhập kho | Ảnh QC của đơn · checklist QC đạt | <span class="s">50</span> |
| <span class="anchor" id="s5"></span>**S5 Xuất lô** | <span class="r log">LOG</span> | Cắt lô 1 ngày cố định/tuần. CI, PL, ISPM, ChAFTA, BMSB. OPS duyệt chứng từ khớp hàng | theo lịch tuần | **Lượt quét thật** của hãng vận chuyển | <span class="s">60</span> |
| <span class="anchor" id="s6"></span>**S6 Thông quan** | <span class="r log">LOG</span> | Theo dõi cảng, broker khai báo, nộp thuế/GST. Bị giữ: báo khách ≤ 24h | báo ≤ 24h | Tracking báo tới cảng/hải quan | <span class="s">70</span> |
| <span class="anchor" id="s7"></span>**S7 Giao cuối** | <span class="r log">LOG</span> | Bàn giao hãng nội địa, hãng hẹn ngày, giao đủ kiện X/Y | theo hẹn | Hãng nhận hàng → POD/ảnh giao | <span class="s">80</span>→<span class="s">90</span> |
| <span class="anchor" id="s8"></span>**S8 Sau giao** | <span class="r cx">CX</span> <span class="r fin">FIN</span> | D+3 hướng dẫn lắp + mời review (mọi khách). FIN đối soát landed cost | D+3 · D+14 | D+14 không case · chi phí đủ | <span class="s">99</span> |

## 3. Trạng thái đơn {#statuses}

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

## 4. Lối thoát ngoại lệ {#exits}

Mỗi lối thoát đọc theo một công thức: **Dấu hiệu → Mã case → Chủ → Hạn báo khách → Cần duyệt → Bước tiếp**.

| Điểm | Dấu hiệu | Case | Chủ | Hạn báo khách | Cần duyệt | Bước tiếp |
|---|---|---|---|---|---|---|
| <span class="anchor" id="ex-s1"></span>**S1** | Địa chỉ không giao được, nghi gian lận | **C1** | <span class="r cx">CX</span> | Hỏi lại ≤ 24h; không trả lời thì hủy | Hoàn tiền theo [mức duyệt](sop-b-hau-mai.html#approval) | [C1 Hủy đơn](sop-b-hau-mai.html#c1) → [hoàn tiền](sop-b-hau-mai.html#refund-steps) |
| <span class="anchor" id="ex-s2"></span>**S2** | Cả 2 NCC hết hàng | **C1 · C2** | <span class="r src">SRC</span> phát hiện · <span class="r cx">CX</span> báo | ≤ 24h: đổi mã hoặc hủy hoàn 100% | Hoàn 100% → <span class="r ceo">CEO</span> | [C1](sop-b-hau-mai.html#c1) · [C2](sop-b-hau-mai.html#c2) |
| <span class="anchor" id="ex-s3"></span>**S3** | NCC trễ hẹn | **C2** nếu chạm ETA | <span class="r src">SRC</span> → <span class="r ops">OPS</span> | +5d: báo khách | +7d đổi NCC: <span class="r ops">OPS</span> | +2d nhắc · +5d báo OPS · +7d đổi NCC → [S2 với NCC dự phòng](#s2) |
| <span class="anchor" id="ex-s4"></span>**S4** | QC trượt | **C2** nếu lùi ETA | <span class="r src">SRC</span> | Nếu lùi ETA: báo trước ≥ 7 ngày | Không (trả NCC tại TQ) | Trả NCC, làm lại → [S4](#s4) · [C2](sop-b-hau-mai.html#c2) |
| <span class="anchor" id="ex-s6"></span>**S6** | Bị giữ hải quan, kiểm dịch | **C2** | <span class="r log">LOG</span> phát hiện · <span class="r cx">CX</span> báo | ≤ 24h, lý do thật, ngày mới | Bồi thường theo [mức duyệt](sop-b-hau-mai.html#approval) | [C2 Trễ hạn](sop-b-hau-mai.html#c2) · [mẫu báo trễ](sop-b-hau-mai.html#tpl-delay) |
| <span class="anchor" id="ex-eta"></span>**Mọi lúc** | Còn ≤ 14 ngày tới ETA max mà chưa <span class="s">60</span> | **C2** | <span class="r cx">CX</span> | Báo trước ≥ 7 ngày, đưa 3 lựa chọn | Tín dụng theo [mức duyệt](sop-b-hau-mai.html#approval) | [C2](sop-b-hau-mai.html#c2) · cờ [Sắp vượt ETA](kpi-sla-nhip.html#flags) |
| <span class="anchor" id="ex-late"></span>**S7** | Quá ETA max, chưa giao | **C2** | <span class="r cx">CX</span> | Trong ngày cờ bật (họp 09:00) | Tín dụng 5% hoặc hủy hoàn 100% theo [mức duyệt](sop-b-hau-mai.html#approval) | [C2](sop-b-hau-mai.html#c2) · cờ [Vượt ETA](kpi-sla-nhip.html#flags) |
| <span class="anchor" id="ex-s8"></span>**S8** | Khách báo vấn đề | **C3–C8** | <span class="r cx">CX</span> | Phản hồi ≤ 4h LV (hỏng/sai), ≤ 24h kênh khác | Theo [mức duyệt](sop-b-hau-mai.html#approval) | [Chọn loại case](sop-b-hau-mai.html#cases) |

## 5. Ba việc chạy liên tục {#continuous}

| Việc | Ai | Nhịp |
|---|---|---|
| Control tower: rà mọi cờ SLA trong tracker | <span class="r ops">OPS</span> | 09:00 hằng ngày |
| Cập nhật chủ động cho khách, kể cả "tuần này chưa có gì mới" | <span class="r cx">CX</span> | mỗi 7 ngày/đơn, tới khi giao |
| Ghi bằng chứng vào tracker (mã PO, ảnh, vận đơn, POD) | Chủ trì từng giai đoạn | ngay khi có |

Tracker, cờ cảnh báo và KPI: [KPI & tracking](kpi-sla-nhip.html).
