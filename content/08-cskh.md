---
title: Chăm sóc khách hàng
order: 8
---

# Chăm sóc khách hàng (CSKH)

Khách mua nội thất khoảng A$1.000 và chờ 8–12 tuần. Điều họ sợ nhất là **không ai trả lời**. Khi không ai trả lời, khách quay sang ngân hàng (chargeback) và cơ quan bảo vệ người tiêu dùng.

## 1. Bài học từ hộp thư của mô hình cũ

Đọc khoảng 20 hội thoại gần nhất (đã bỏ thông tin cá nhân), các nhóm vấn đề:

| Nhóm vấn đề | Tần suất | Nguyên nhân gốc | {{BRAND}} xử lý ở đâu |
|---|---|---|---|
| Giao trễ, không có tracking | rất cao (~16/22) | Hứa 4–6 tuần, thực tế 2–4 tháng | Khung thời gian thật + cập nhật mỗi 7 ngày |
| Nhắn mà không có người trả lời, bot chạy vòng | cao (~12/22) | Bot không tra được đơn, không ai trực | Cam kết 24 giờ, bot chỉ tra đơn |
| Dọa chargeback, báo cơ quan bảo vệ người tiêu dùng | cao (~9/22) | Hai vấn đề trên kéo dài | Bảng bồi thường, gọi điện trong 24 giờ |
| Hàng hỏng (ẩm, trầy, mẻ, đèn LED hỏng) | vừa | Đóng gói và QC kém | Chuẩn đóng gói + QC ở kho gom |
| Sai hàng, sai size, màu khác ảnh | vừa | Không đối chiếu thông số, giao nhầm kiện | Đối chiếu NCC, nhãn kiện X/Y |
| Thiếu hướng dẫn lắp, thiếu phụ kiện | vừa | Không có hướng dẫn tiếng Anh | PDF tiếng Anh + túi phụ kiện đánh mã |
| Chọn nhầm biến thể khi đặt | thấp | Một trang bán nhiều món | Mỗi trang một món |

## 2. Cam kết phản hồi

| Kênh | Phản hồi đầu tiên | Giải pháp đề xuất |
|---|---|---|
| Email, form web, Messenger, Instagram, WhatsApp | ≤ 24 giờ (mục tiêu ≤ 4 giờ trong giờ làm việc) | ≤ 24 giờ sau khi có đủ thông tin |
| Khiếu nại hàng hỏng | ≤ 4 giờ làm việc | ≤ 24 giờ |
| Khách nhắc chargeback hoặc cơ quan nhà nước | Gọi điện trong 24 giờ | Ngay trong cuộc gọi, theo bảng bồi thường |

**Quy tắc cho bot và tin tự động:**

- Tin tự động nói đúng giờ làm việc và thời gian người thật sẽ trả lời.
- Bot chỉ tra đơn bằng mã đơn. Không tìm thấy thì xin email và báo người thật sẽ trả lời trong bao lâu.
- Không gửi câu "đang chuyển cho nhân viên" khi không có ai trực.
- Mọi hội thoại chờ quá 24 giờ hiện lên đầu danh sách ở buổi họp đứng.

## 3. Bảng bồi thường (dùng chung cho cả team)

| Tình huống | Xử lý chuẩn | Ai duyệt |
|---|---|---|
| Trễ quá khung thời gian đã hứa | Tín dụng 5% giá trị đơn (tối đa A$100), **hoặc** hủy và hoàn 100% nếu khách muốn | CSKH |
| Trầy nhẹ, sửa được | Gửi bộ sửa (sáp/kem) + hoàn 10% giá món | CSKH |
| Thiếu phụ kiện hoặc hướng dẫn | Gửi PDF ngay, gửi bù phụ kiện trong 5 ngày | CSKH |
| Hỏng một bộ phận | Gửi bộ phận thay hoặc hoàn tới A$150 | Ops Lead |
| Hỏng nặng, sai hàng, sai size, màu khác rõ rệt | Đổi mới hoặc hoàn 100% (khách chọn). {{BRAND}} thu hồi hàng, không bắt khách gửi về TQ | CEO nếu > A$150 |
| Khách dọa chargeback | Gọi điện trong 24 giờ, đưa lựa chọn đúng bảng này, ghi lại toàn bộ trao đổi | Ops Lead |

Mọi khoản bồi thường ghi vào sheet ngoại lệ: lý do, số tiền, người duyệt, nguyên nhân gốc. Cùng một mã lỗi 2 lần trong tháng thì tạm ngừng mã hoặc NCC đó.

## 4. Mẫu tin nhắn (tiếng Anh)

Chỉ gửi nội dung khớp trạng thái thật. Thay phần [ngoặc vuông].

**Xác nhận đơn**

```text
Hi [First name], thank you for your order #[No].

Your [product] is made and packed by our partner workshop and shipped
by sea, so it takes longer than local stock.

Estimated delivery: [date A] – [date B]

What happens next:
1) Workshop prepares and packs your item
2) Quality check at our consolidation warehouse (we'll send you photos)
3) Sea freight and customs
4) Local delivery — the carrier will book a time with you

You can cancel for a full refund any time before production starts.
We send tracking as soon as the carrier has scanned your parcel.
```

**Cập nhật mỗi 7 ngày**

```text
Hi [First name], your weekly update for order #[No]:

Current stage: [In production / Quality checked / On the ship / In customs / With local carrier]
What changed this week: [one honest line, or "No change this week"]
Estimated delivery: still [date A] – [date B]

Reply here any time — a team member answers within 24 hours.
```

**Báo trễ (gửi trước ít nhất 7 ngày)**

```text
Hi [First name], an honest update on order #[No]:
[The workshop has moved dispatch to DATE / The ship's departure moved to DATE].

New estimated delivery: [date A] – [date B]

Your options:
1) Keep your order, with a credit of [amount] for the delay
2) Switch to [alternative item]
3) Cancel for a full refund, processed within 2 business days

Just reply 1, 2 or 3.
```

**Đã xuất hàng**

```text
Hi [First name], good news: order #[No] is on its way.

Tracking: [number] ([link])
Estimated delivery: [date A] – [date B]

Sea tracking can stay unchanged for several days while the ship is
at sea — that's normal. The local carrier will contact you to book
a delivery time. Please count the boxes ("Box X of Y") before signing.
```

**Nhận hàng hỏng**

```text
Hi [First name], we're sorry your [item] arrived damaged.
To fix this quickly, please send:
- a photo of the box label
- photos or a short video of the damage
- one photo of the whole item

We'll reply with a solution (replacement part, replacement item or
refund) within 24 hours. This doesn't affect your rights under
Australian Consumer Law.
```

## 5. Câu hỏi hay gặp (FAQ để dán lên web)

| Câu hỏi | Trả lời ngắn |
|---|---|
| How long is delivery? | Australia 8–12 weeks, Singapore 5–8 weeks. Your window is shown at checkout. |
| Why does it take that long? | Each item is made to order and shipped by sea, then quality checked before it leaves. |
| When do I get tracking? | As soon as the carrier scans your parcel. Before that, we email you every 7 days. |
| Is it solid wood? | Each product page lists the exact material of each part (solid timber, veneer, MDF…). |
| Do I need to assemble it? | Each page shows "Assembled" or "Assembly ~X minutes". English instructions and a video are included. |
| Can I cancel? | Free before production starts. If we are late, you can cancel for a full refund. |
