---
title: SOP chuỗi cung ứng end-to-end
badges: daily, onboarding, internal
---

# SOP chuỗi cung ứng end-to-end {#supply-chain}

Một trang cho toàn bộ chuỗi: **chuẩn bị sản phẩm → bán → mua → vận chuyển → giao → hậu mãi**. Mỗi bước có đúng một người làm chính, có người duyệt khi cần, có bên ngoài tham gia và có bằng chứng trước khi chuyển bước. Chi tiết từng đơn vẫn nằm ở [SOP-A](sop-a-don-chuan.html) và [SOP-B](sop-b-hau-mai.html); trang này nối chúng với phần trước bán và với từng đối tác bên ngoài.

<div class="legend"><span><b>R</b> làm chính</span><span><b>A</b> duyệt / chịu trách nhiệm cuối</span><span><b>C</b> tham gia, cung cấp đầu vào</span><span><b>I</b> được báo</span><span>┄▭ đối tác ngoài</span><span><span class="s">30</span> trạng thái tracker</span><span><span class="flag">đỏ</span> lối thoát ngoại lệ</span></div>

## 1. Bản đồ tổng: ai làm gì ở từng giai đoạn {#map}

Hàng ngang là bên liên quan (nội bộ ở trên, đối tác ngoài ở dưới đường kẻ đậm). Cột là 12 giai đoạn. Mũi tên nối người làm chính, cho thấy "quả bóng" đi qua ai.

{{SVG:map}}

## 2. Danh bạ bên liên quan {#stakeholders}

| Bên liên quan | Là ai | Giao cho chuỗi cái gì | Người nội bộ giữ quan hệ | Bằng chứng nhận lại |
|---|---|---|---|---|
| Khách hàng (KH) | Người mua tại Úc | Đơn, địa chỉ, ngày nhận, ký POD, ảnh khi có lỗi | <span class="r cx">CX</span> | Email xác nhận, POD, ảnh case |
| Shopify · cổng thanh toán | Hệ thống bán và thu tiền | Đơn đã thu tiền, email tự động, cảnh báo gian lận, tranh chấp | <span class="r ops">OPS</span> · <span class="r fin">FIN</span> | Mã đơn, trạng thái thanh toán |
| NCC / xưởng TQ | Shop Taobao · 1688 | Bản vẽ W×D×H, vật liệu, số kiện, sản xuất, đóng gói, nhãn brand | <span class="r src">SRC</span> | Xác nhận bằng chữ, ảnh kiện, vận đơn nội địa |
| Kho gom TQ | Kho consolidation | Nhận, đếm, cân, chụp; gia cố, dán shipping mark, pallet ISPM-15 | <span class="r src">SRC</span> (QC) · <span class="r log">LOG</span> (xuất) | Phiếu nhập kho, ảnh, số CBM/kg |
| Forwarder · hãng tàu | Đại lý vận tải biển | Báo giá, booking, khai hải quan xuất TQ, container, B/L | <span class="r log">LOG</span> | Booking, B/L, lịch tàu |
| Đại lý hải quan Úc | Licensed customs broker | Mã HS, khai báo nhập khẩu, tính thuế/GST, hồ sơ kiểm dịch | <span class="r log">LOG</span> | Bản khai, hóa đơn thuế, lệnh giải phóng |
| ABF · DAFF | Hải quan và kiểm dịch Úc | Đánh giá hồ sơ, yêu cầu xử lý/kiểm hóa, giải phóng hàng | <span class="r log">LOG</span> (qua broker) | Lệnh giải phóng, biên bản kiểm hóa nếu có |
| Kho CFS / 3PL Úc | Kho dỡ container, lưu tạm | Dỡ hàng, đếm kiện theo PL, chụp hư hỏng, giao cho hãng | <span class="r log">LOG</span> | Phiếu nhận, ảnh tình trạng |
| Hãng giao Úc | Giao 2 người, lắp đặt | Hẹn ngày, quét, giao đủ kiện, lắp (nếu mua), POD | <span class="r log">LOG</span> · <span class="r cx">CX</span> | Lượt quét, ảnh POD |

Nội bộ: <span class="r ceo">CEO</span> duyệt cấp cao · <span class="r ops">OPS</span> điều phối · <span class="r src">SRC</span> mua hàng & QC · <span class="r log">LOG</span> logistics & hải quan · <span class="r cx">CX</span> chăm sóc khách · <span class="r mkt">MKT</span> marketing & listing · <span class="r fin">FIN</span> tài chính. Chi tiết quyền hạn: [Roles, Authority & Access](vai-tro-quyen-han.html).

## 3. E0 · Chuẩn bị sản phẩm (trước khi bán) {#e0}

Một mẫu chỉ được bật bán khi đi hết E0. Trạng thái SKU: `DRAFT → VERIFIED → ACTIVE`.

{{SVG:e0}}

| Bước | Việc | R | A | C / I | Đầu ra / bằng chứng | Hạn |
|---|---|---|---|---|---|---|
| P1.1 | Đề xuất mẫu từ Top 100 theo nhu cầu thật | <span class="r mkt">MKT</span> | <span class="r ceo">CEO</span> | | Danh sách HERO / CORE | Đầu tuần |
| P2.1 | Tìm 2 NCC mỗi mẫu bằng ảnh, ưu tiên NCC đã chấm điểm | <span class="r src">SRC</span> | | NCC | Source_Map: shop, Item ID | 5 mẫu/ngày |
| P2.2 | Hỏi và nhận bản vẽ W×D×H, vật liệu, số kiện, thời gian SX | <span class="r src">SRC</span> | | NCC | Xác nhận bằng chữ của NCC | ≤ 48h |
| P2.3 | So với Master SKU: lệch ≤ 2 cm, màu đúng mã | <span class="r src">SRC</span> | | | Kết quả đối chiếu | Cùng ngày |
| P3.1 | Đặt mẫu thật (HERO), đo, chụp màu, ghi golden sample | <span class="r src">SRC</span> | <span class="r ops">OPS</span> | NCC | Ảnh đo, ảnh màu → `VERIFIED` | 7–14 ngày |
| P4.1 | Báo giá cước theo CBM, phí kho gom, lịch tàu | <span class="r log">LOG</span> | | Forwarder | Báo giá có hiệu lực | Mỗi quý |
| P4.2 | Xác nhận mã HS, thuế, GST, yêu cầu kiểm dịch gỗ / bao bì | <span class="r log">LOG</span> | | Đại lý HQ Úc | Email xác nhận mã HS | Trước lô đầu |
| P4.3 | Tính landed cost và giá bán AUD, biên ròng ≥ 30% | <span class="r fin">FIN</span> | <span class="r ceo">CEO</span> | LOG | Bảng giá đã duyệt | Trước khi đăng |
| P5.1 | Viết listing EN từ Master SKU, ảnh được phép dùng | <span class="r mkt">MKT</span> | | SRC | Listing nháp | 5/ngày |
| P5.2 | Duyệt 5 câu và bật bán | <span class="r mkt">MKT</span> | <span class="r ceo">CEO</span> | | SKU → `ACTIVE` | |

## 4. E1 · Đơn hàng → đặt NCC → sản xuất → kho gom QC (S1–S4) {#e1}

{{SVG:e1}}

| Bước | Việc | R | A | C / I | Đầu ra / bằng chứng | SLA | Trạng thái |
|---|---|---|---|---|---|---|---|
| S1.1 | Khách đặt và thanh toán; Shopify tạo đơn, chống gian lận | Shopify | | KH | Đơn đã thu tiền | Tức thì | <span class="s">10</span> |
| S1.2 | Kiểm đơn: địa chỉ giao được, đường vào nhà, SĐT, mã, dấu hiệu rủi ro | <span class="r cx">CX</span> | | | Kết quả kiểm | ≤ 4h LV | |
| S1.3 | Gửi email xác nhận kèm khung ETA thật | <span class="r cx">CX</span> | | KH (I) | Email đã gửi | ≤ 4h LV | <span class="s">20</span> |
| S2.1 | Hỏi tồn và ngày xuất: NCC chính, rồi dự phòng | <span class="r src">SRC</span> | | NCC | Ngày xuất cụ thể | ≤ 24h | |
| S2.2 | Lập PO đúng mã, kèm shipping mark và file nhãn brand | <span class="r src">SRC</span> | | NCC | Mã PO | ≤ 24h | |
| S2.3 | Thanh toán NCC qua sàn | <span class="r fin">FIN</span> | | SRC (I) | Chứng từ thanh toán | ≤ 24h | <span class="s">30</span> |
| S3.1 | NCC sản xuất, đóng kiện X/Y, dán nhãn, gửi ảnh/video | NCC | | SRC | Ảnh kiện | Ngày hẹn | |
| S3.2 | Duyệt ảnh kiện, nhận vận đơn nội địa | <span class="r src">SRC</span> | <span class="r ops">OPS</span> (trễ) | NCC | Vận đơn | ≤ hẹn +2d | <span class="s">40</span> |
| S4.1 | Kho gom nhận, đếm kiện, cân, chụp ngoại quan | Kho gom | | SRC (I) | Phiếu nhập | Khi hàng tới | |
| S4.2 | QC theo checklist: kích thước ±5 mm, màu, phụ kiện, đóng gói, ISPM-15 | <span class="r src">SRC</span> | | Kho gom | Checklist + ảnh QC | ≤ 2d sau nhập | <span class="s">50</span> |
| S4.3 | Gia cố, dán shipping mark, đóng pallet ISPM-15 | Kho gom | | SRC | Ảnh pallet | Trước ngày cắt lô | |
| S4.4 | Gửi ảnh QC của chính đơn cho khách | <span class="r cx">CX</span> | | KH (I) | Email kèm ảnh | ≤ 1d sau QC | |

## 5. E2 · Xuất khẩu TQ → biển → thông quan Úc (S5–S6) {#e2}

{{SVG:e2}}

| Bước | Việc | R | A | C / I | Đầu ra / bằng chứng | SLA | Trạng thái |
|---|---|---|---|---|---|---|---|
| S5.1 | Cắt lô tuần: chọn đơn đã QC đạt, tính CBM/kg | <span class="r log">LOG</span> | | Kho gom | Danh sách lô | 1 ngày cố định/tuần | |
| S5.2 | Lập CI, PL, packing declaration, chứng nhận ISPM-15, C/O ChAFTA | <span class="r log">LOG</span> | | Kho gom · Forwarder | Bộ chứng từ | Trước booking | |
| S5.3 | Duyệt lô: chứng từ khớp hàng thật | <span class="r log">LOG</span> | <span class="r ops">OPS</span> | | Lô đã duyệt | Cùng ngày | |
| S5.4 | Booking, lấy hàng tại kho gom, khai hải quan xuất TQ, phát hành B/L | Forwarder | | LOG | B/L, lượt quét đầu | Theo lịch tàu | <span class="s">60</span> |
| S5.5 | Cập nhật ETA lô vào tracker; báo khách đã xuất kèm tracking (chỉ khi có quét thật) | <span class="r log">LOG</span> | | CX · KH (I) | ETA trong tracker | Trong ngày | |
| S6.1 | Khai báo nhập khẩu trước khi tàu cập cảng (lô > A$1.000 cần tờ khai đầy đủ) | Đại lý HQ Úc | | LOG | Bản khai | Trước khi cập cảng | |
| S6.2 | ABF/DAFF đánh giá hồ sơ, yêu cầu xử lý hoặc kiểm hóa nếu cần | ABF · DAFF | | Broker · LOG | Kết quả đánh giá | Theo cơ quan | |
| S6.3 | Nộp thuế, GST, phí cảng, phí kiểm dịch | <span class="r fin">FIN</span> | | Broker | Biên lai | Trước giải phóng | |
| S6.4 | Nhận lệnh giải phóng, đặt kho CFS dỡ hàng | <span class="r log">LOG</span> | | Broker · Kho Úc | Lệnh giải phóng | ≤ 24h | <span class="s">70</span> |

Hàng bị giữ hoặc kiểm hóa: LOG báo CX để khách được báo trong 24 giờ, kèm ETA mới. Yêu cầu kiểm dịch cụ thể (gỗ, bao bì, xử lý theo mùa) do đại lý hải quan xác nhận cho từng lô; không tự suy đoán.

## 6. E3 · Kho Úc → giao chặng cuối → đóng đơn (S7–S8) {#e3}

{{SVG:e3}}

| Bước | Việc | R | A | C / I | Đầu ra / bằng chứng | SLA | Trạng thái |
|---|---|---|---|---|---|---|---|
| S7.1 | Dỡ container, đếm kiện theo PL, chụp hư hỏng | Kho Úc | | LOG | Phiếu nhận + ảnh | ≤ 2d sau giải phóng | |
| S7.2 | Phân bổ đơn cho hãng giao theo khu vực | <span class="r log">LOG</span> | | Hãng giao | Danh sách giao | Cùng ngày | |
| S7.3 | Hãng nhận hàng, quét lần đầu, hẹn ngày với khách | Hãng giao | | KH · CX (I) | Lượt quét thật | Theo hãng | |
| S7.4 | Shopify chuyển Fulfilled và gửi tracking (chỉ sau lượt quét thật) | <span class="r cx">CX</span> | | KH (I) | Email tracking | Trong ngày | <span class="s">80</span> |
| S7.5 | Giao 2 người, đủ kiện X/Y, lắp nếu khách mua; khách ký POD | Hãng giao | | KH | Ảnh POD | Ngày hẹn | |
| S7.6 | Xác nhận POD trong tracker | <span class="r log">LOG</span> | | | POD | ≤ 1d | <span class="s">90</span> |
| S8.1 | D+3: hướng dẫn lắp, mời review (mọi khách) | <span class="r cx">CX</span> | | KH | Email | D+3 | |
| S8.2 | Đối soát landed cost thực từng đơn với giá sàn | <span class="r fin">FIN</span> | | | File chi phí | Thứ Sáu | |
| S8.3 | D+14 không có case: đóng đơn | <span class="r ops">OPS</span> | <span class="r ops">OPS</span> | | Đơn đóng | D+14 | <span class="s">99</span> |

## 7. Hậu mãi và ngoại lệ {#exceptions}

Mọi lệch chuẩn ở bất kỳ bước nào thoát sang [SOP-B](sop-b-hau-mai.html#cases) bằng mã case C1–C8: hủy, trễ, hỏng, thiếu kiện, sai hàng, đổi ý, chargeback, bảo hành. Mức duyệt bồi thường: ≤ A$50 <span class="r cx">CX</span> · A$51–150 <span class="r ops">OPS</span> · > A$150 hoặc hoàn 100% <span class="r ceo">CEO</span>. Hàng lỗi xử lý tại Úc, không gửi về Trung Quốc.

## 8. Điểm bàn giao quan trọng {#handoffs}

| Bàn giao | Từ → tới | Điều kiện để nhận | Nếu thiếu |
|---|---|---|---|
| Mẫu sang bán | SRC → MKT | SKU `VERIFIED`, giá đã duyệt | Không viết listing |
| Đơn sang mua | CX → SRC | Đơn trạng thái 20 | SRC không đặt PO |
| Hàng sang kho gom | NCC → Kho gom | Đủ kiện X/Y, có nhãn | Kho báo SRC trong ngày |
| QC sang xuất lô | SRC → LOG | Trạng thái 50, ảnh QC | Không đưa vào lô |
| Lô sang forwarder | LOG → Forwarder | OPS đã duyệt chứng từ | Không booking |
| Thông quan sang giao | Broker → LOG → Kho Úc | Lệnh giải phóng | Báo khách ≤ 24h |
| Giao sang sau bán | Hãng giao → LOG → CX | Ảnh POD | Không chuyển 90 |
