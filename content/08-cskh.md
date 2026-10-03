---
title: SOP-B · Hậu mãi & hoàn tiền
order: 8
---

# SOP-B · Hậu mãi: đổi trả, hoàn tiền, khiếu nại

Mọi lệch chuẩn thành **một case** có mã loại, mức duyệt, giải pháp chuẩn và nguyên nhân gốc. Không bồi thường theo cảm tính.

<div class="flow">
<div class="st"><b>B1–B2 · ≤ 4h LV</b><span class="n">Mở case · bằng chứng</span><span class="r cx">CX</span></div>
<div class="st"><b>B3 · ≤ 24h</b><span class="n">Duyệt theo mức</span><span class="r cx">CX</span> <span class="r ops">OPS</span> <span class="r ceo">CEO</span></div>
<div class="st"><b>B4–B5 · ≤ 5–7d</b><span class="n">Đề xuất · thực thi</span><span class="r src">SRC</span> <span class="r log">LOG</span> <span class="r fin">FIN</span></div>
<div class="st"><b>B6–B7 · ≤ 48h · thứ Sáu</b><span class="n">Truy đòi · đóng · học</span><span class="r src">SRC</span> <span class="r ops">OPS</span></div>
</div>

## 1. Tám loại case

| Mã | Loại | Dấu hiệu | Giải pháp chuẩn | Duyệt | Luồng |
|---|---|---|---|---|---|
| **C1** | Hủy đơn | Khách hủy · đơn không hợp lệ · hết hàng | Trước khi đặt NCC (≤ 48h): hoàn 100%. Sau đó: phí hủy đã công bố, trừ khi brand trễ hoặc lỗi | CX | B1 → R5 |
| **C2** | Trễ hạn | Còn 14 ngày tới ETA max chưa xuất · quá ETA max | Báo trước ≥ 7 ngày, 3 lựa chọn: chờ + tín dụng 5% (tối đa A$100) · đổi mã · hủy hoàn 100% | CX | B1 |
| **C3** | Hư hỏng khi nhận | Trầy, mẻ, vỡ, ẩm | Trầy nhẹ: bộ sửa + 10% · hỏng bộ phận: gửi bộ phận hoặc ≤ A$150 · hỏng nặng: đổi hoặc hoàn 100% (khách chọn) | theo mức | B1 · B2 |
| **C4** | Thiếu kiện / phụ kiện | Thiếu ốc, thiếu kiện X/Y, thiếu hướng dẫn | PDF ngay · phụ kiện gửi nhanh ≤ 5 ngày LV · thiếu kiện: truy hãng giao rồi gửi bù | CX · OPS | B1 |
| **C5** | Sai hàng / khác mô tả | Sai mã, sai size, màu khác rõ, chất liệu khác trang | Đổi đúng hoặc hoàn 100%. Brand thu hồi, **không bắt khách gửi về TQ** | theo mức | B1 · B2 |
| **C6** | Đổi ý | Còn mới, chưa lắp, nguyên hộp, ≤ 14 ngày từ khi giao | Khách trả cước về điểm nhận tại Úc · hoàn ≤ 7 ngày LV sau khi nhận | CX | B2 |
| **C7** | Tranh chấp thanh toán | Ngân hàng / cổng báo dispute · khách nhắc chargeback | Gọi ≤ 24h, đưa lựa chọn đúng bảng · nộp hồ sơ trước hạn | OPS | B3 |
| **C8** | Bảo hành | Lỗi phát sinh khi dùng (bản lề, ray, sơn bong) | Sửa · thay bộ phận · đổi · hoàn theo luật tiêu dùng (AU: ACL; SG: 6 tháng Lemon Law) | theo mức | B1 |

## 2. Mức duyệt và mã giải pháp

| Giá trị đền bù | Duyệt | Thời hạn |
|---|---|---|
| ≤ A$50 | <span class="r cx">CX</span> tự duyệt | ngay |
| A$51–150 | <span class="r ops">OPS</span> | ≤ 4h làm việc |
| > A$150 hoặc hoàn 100% | <span class="r ceo">CEO</span> | ≤ 24h |

| Mã | Giải pháp | Ai thực thi | SLA |
|---|---|---|---|
| R1 | Sửa: bộ sửa, hướng dẫn, kỹ thuật viên | <span class="r src">SRC</span> / <span class="r log">LOG</span> | gửi ≤ 5 ngày LV |
| R2 | Gửi bù bộ phận, phụ kiện, kiện thiếu | <span class="r src">SRC</span> | gửi ≤ 5 ngày LV |
| R3 | Đổi sản phẩm mới | <span class="r src">SRC</span> → SOP-A từ S2 | ETA mới báo khách |
| R4 | Hoàn tiền (một phần / toàn bộ / tín dụng) | <span class="r fin">FIN</span> | ≤ 7 ngày LV sau duyệt |
| R5 | Thu hồi hàng | <span class="r log">LOG</span> | đặt lịch ≤ 2 ngày LV |

## 3. Swimlane B1 · Xử lý case

{{SVG:b1}}

## 4. Swimlane B2 · Trả hàng, thu hồi, hoàn tiền

{{SVG:b2}}

**Hoàn tiền: 5 bước của FIN**

1. Đọc số tiền đã duyệt và người duyệt trong case. Không có người duyệt đúng mức thì trả lại CX.
2. Hoàn trên Shopify về **phương thức thanh toán gốc** (không chuyển khoản ngoài). Ghi rõ dòng hàng, phí ship.
3. Kiểm cổng thanh toán đã nhận lệnh (Shopify Payments, PayPal, Afterpay…).
4. CX gửi email xác nhận số tiền và thời gian ngân hàng xử lý.
5. Ghi vào tracker: ngày hoàn, số tiền, mã giải pháp. Đơn chuyển <span class="s">95</span> nếu hoàn toàn bộ.

## 5. Swimlane B3 · Chargeback

{{SVG:b3}}

**Hồ sơ nộp cổng thanh toán:** trang sản phẩm lúc mua (ảnh chụp), email xác nhận có khung ETA, tracking và POD, toàn bộ trao đổi với khách, các lựa chọn đã đưa ra. Chỉ nộp khi brand không có lỗi; brand sai thì chấp nhận và hoàn.

## 6. Đóng case: mã nguyên nhân gốc

Mỗi case đóng phải có **một** mã. Thứ Sáu OPS đếm theo mã; cùng mã trên cùng SKU/NCC 2 lần/tháng thì tạm ngừng SKU hoặc NCC đó.

| Mã | Nguyên nhân | Chủ sửa | Thu hồi chi phí từ |
|---|---|---|---|
| RC-NCC | Lỗi sản xuất, sai thông số | <span class="r src">SRC</span> | NCC |
| RC-PACK | Đóng gói không đạt chuẩn | <span class="r src">SRC</span> | NCC |
| RC-QC | QC kho gom bỏ sót | <span class="r src">SRC</span> | – |
| RC-FWD | Forwarder, cảng, hải quan | <span class="r log">LOG</span> | forwarder / bảo hiểm |
| RC-LAST | Hãng giao chặng cuối | <span class="r log">LOG</span> | hãng giao |
| RC-LIST | Trang sản phẩm sai, gây hiểu nhầm | <span class="r mkt">MKT</span> | – |
| RC-CX | Hứa sai, trả lời chậm, báo trễ muộn | <span class="r cx">CX</span> | – |
| RC-CUST | Khách đổi ý, chọn nhầm | – | – |

## 7. Cam kết phản hồi

| Kênh / tình huống | Phản hồi đầu | Giải pháp |
|---|---|---|
| Email, form, Messenger, Instagram, WhatsApp | ≤ 24h (mục tiêu ≤ 4h LV) | ≤ 24h sau khi đủ thông tin |
| Hàng hỏng, sai hàng | ≤ 4h làm việc | ≤ 24h |
| Khách nhắc chargeback / cơ quan nhà nước | **gọi điện ≤ 24h** | ngay trong cuộc gọi |

Bot chỉ tra đơn bằng mã đơn; không tra được thì nói rõ khi nào người thật trả lời. Không gửi "đang chuyển nhân viên" khi không có ai trực.

## 8. Mẫu tin nhắn (tiếng Anh)

Chỉ gửi nội dung khớp trạng thái thật. Thay phần [ngoặc vuông].

<details><summary>Xác nhận đơn · trạng thái 20</summary>
<pre><code>Hi [First name], thank you for your order #[No].
Your [product] is made and packed by our partner workshop and shipped by sea.
Estimated delivery: [date A] – [date B]
1) Workshop prepares and packs your item
2) Quality check at our consolidation warehouse (we'll send you photos)
3) Sea freight and customs
4) Local delivery — the carrier will book a time with you
You can cancel for a full refund any time before production starts.
We send tracking as soon as the carrier has scanned your parcel.</code></pre>
</details>

<details><summary>Cập nhật mỗi 7 ngày</summary>
<pre><code>Hi [First name], your weekly update for order #[No]:
Current stage: [In production / Quality checked / On the ship / In customs / With local carrier]
What changed this week: [one honest line, or "No change this week"]
Estimated delivery: still [date A] – [date B]
Reply here any time — a team member answers within 24 hours.</code></pre>
</details>

<details><summary>Báo trễ · C2 (gửi trước ≥ 7 ngày)</summary>
<pre><code>Hi [First name], an honest update on order #[No]:
[The workshop has moved dispatch to DATE / The ship's departure moved to DATE].
New estimated delivery: [date A] – [date B]
Your options:
1) Keep your order, with a credit of [amount] for the delay
2) Switch to [alternative item]
3) Cancel for a full refund, processed within 2 business days
Just reply 1, 2 or 3.</code></pre>
</details>

<details><summary>Đã xuất hàng · trạng thái 60</summary>
<pre><code>Hi [First name], good news: order #[No] is on its way.
Tracking: [number] ([link])
Estimated delivery: [date A] – [date B]
Sea tracking can stay unchanged for several days while the ship is at sea — that's normal.
The local carrier will contact you to book a delivery time.
Please count the boxes ("Box X of Y") before signing.</code></pre>
</details>

<details><summary>Nhận hàng hỏng · C3</summary>
<pre><code>Hi [First name], we're sorry your [item] arrived damaged.
To fix this quickly, please send:
- a photo of the box label
- photos or a short video of the damage
- one photo of the whole item
We'll reply with a solution (replacement part, replacement item or refund) within 24 hours.
This doesn't affect your rights under Australian Consumer Law.</code></pre>
</details>

<details><summary>Đã hoàn tiền · R4</summary>
<pre><code>Hi [First name], we've refunded [amount] for order #[No] to your original payment method today.
Banks usually take [3–5] business days to show it. Case reference: [Case ID].
If anything else isn't right, just reply here.</code></pre>
</details>

## 9. Câu hỏi hay gặp (dán lên web)

| Câu hỏi | Trả lời ngắn |
|---|---|
| How long is delivery? | Australia 8–12 weeks, Singapore 5–8 weeks. Your window is shown at checkout. |
| When do I get tracking? | As soon as the carrier scans your parcel. Before that, we email you every 7 days. |
| Is it solid wood? | Each product page lists the exact material of each part (solid timber, veneer, MDF…). |
| Can I cancel? | Free before production starts. If we are late, you can cancel for a full refund. |
| Can I return it? | Faulty or not as described: we fix, replace or refund and collect it. Change of mind: within 14 days, unused and in original packaging. |
