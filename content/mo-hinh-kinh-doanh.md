---
title: Mô hình kinh doanh
badges: internal
---

# Mô hình kinh doanh

{{BRAND}} bán nội thất cho khách tại Úc (trước), Singapore (sau), New Zealand (khi đủ điều kiện). Team vận hành ở Việt Nam. Hàng đặt từ xưởng ở Trung Quốc, gom về kho, đi biển, giao chặng cuối tại nước khách. Giai đoạn đầu không giữ tồn kho.

{{SOT:cost}}

## Dòng hàng và dòng tiền {#flows}

```text
Khách đặt trên website Shopify ──tiền──▶ Cổng thanh toán ──rút gộp──▶ Tài khoản công ty
        │
        ▼ (≤ 24 giờ)
Team đặt hàng xưởng (Taobao/1688/xưởng trực tiếp) ──▶ Xưởng sản xuất 3–14 ngày
        │
        ▼ (2–7 ngày)
Kho gom tại TQ: nhận, QC, chụp ảnh   ← điểm trả hàng rẻ nhất và cuối cùng
        │  cắt lô cố định 1 lần/tuần
        ▼
Đường biển 20–31 ngày + thông quan, kiểm dịch
        │
        ▼
Giao chặng cuối 3–7 ngày làm việc ──▶ Khách nhận (+ lắp đặt nếu có)
```

## Số liệu tham khảo từ mô hình cũ (cùng sản phẩm) {#reference}

Số liệu tổng hợp từ khoảng 1.850 đơn trong 4 tháng (05–09/2026). Đơn vị tiền theo sổ sách cũ (SGD). Chỉ dùng để định hướng, không dùng để quảng cáo.

| Chỉ số | Giá trị | Ý nghĩa cho {{BRAND}} |
|---|---|---|
| Thị trường | Úc 85% đơn, Singapore 15% | Úc là thị trường chính |
| Giá trị đơn trung bình | khoảng 1.000; Úc: trung vị khoảng 900, 50% đơn nằm trong 640–1.280 | Khách sẵn sàng trả khoảng A$600–1.500 cho một món |
| Biên lãi gộp (sau giá hàng + cước quốc tế) | khoảng 39% (tháng tốt nhất 41%) | Mặt bằng giá đã được thị trường chấp nhận |
| Biên lãi gộp theo nhóm | Tủ giày khoảng 49%, bàn trà 42%, kệ TV 41%, giường 26% | Ưu tiên kệ TV, bàn trà, tủ giày, buffet. Chưa bán giường |
| Cước giao về Úc | khoảng 76% giá hàng (Singapore khoảng 18%) | Cước là khoản cần đàm phán nhiều nhất |
| Thời gian giao thực tế, Úc | trung vị 8,7 tuần, 90% đơn ≤ 11,6 tuần | Công bố **8–12 tuần**, không hứa ngắn hơn |
| Thời gian giao thực tế, Singapore | trung vị 5,4 tuần, 90% đơn ≤ 7,1 tuần | Công bố **5–8 tuần** |
| Lãi ròng ước tính | khoảng 6–7% doanh thu | Quảng cáo, hoàn hủy, bồi thường và chargeback ăn mất phần lớn lãi gộp |

## Vì sao mô hình cũ mất lãi và {{BRAND}} làm khác thế nào {#differences}

| Mô hình cũ | {{BRAND}} |
|---|---|
| Hứa 3,5–6 tuần, thực tế 8–12 tuần | Công bố khung thời gian từ dữ liệu thật, cập nhật đơn mỗi 7 ngày |
| Gửi tracking trước khi hàng thật sự đi | Chỉ gửi tracking sau khi hãng vận chuyển đã quét kiện |
| Bot hứa chuyển cho nhân viên, không ai trả lời | Có người thật trả lời trong 24 giờ, đo hằng tuần |
| Một trang bán nhiều món, khách chọn nhầm | Mỗi trang một món, bán theo bộ thì có mã "Set" riêng |
| Bồi thường tùy người trực | Bảng bồi thường cố định |
| Mô tả chất liệu theo tiêu đề shop | Theo bản vẽ và xác nhận của NCC, có hàng mẫu |
| Hàng ngấm nước, thiếu ốc, không có hướng dẫn tiếng Anh | Tiêu chuẩn đóng gói, túi phụ kiện đánh mã, hướng dẫn PDF tiếng Anh |

## Quy tắc giá {#pricing}

- **Lãi ròng mục tiêu ≥ 30% giá bán**, tính sau: giá hàng, cước, phí cổng thanh toán, phí Shopify, quảng cáo, dự phòng hoàn tiền, dự phòng tỉ giá.
- Với quảng cáo khoảng 20% doanh thu, giá bán phải khoảng **3 lần (giá hàng + cước)** mới đạt 30%. Ba đòn bẩy để hạ hệ số này về 2,0–2,5 lần:
    1. Giảm quảng cáo về khoảng 12% nhờ creator và nội dung tự nhiên.
    2. Giảm hoàn hủy về khoảng 3% nhờ QC ở kho TQ và mô tả đúng.
    3. Đàm phán cước theo lô.
- Mã hàng không đạt ngưỡng lãi ở giá thị trường thì **không đăng bán**.
- Giá niêm yết nói rõ đã gồm hay chưa gồm GST và thuế nhập khẩu. {{BLK:gst}}

## Giai đoạn 2: kho tại Úc {#phase-2}

Khi đạt **30–40 đơn Úc/tháng ổn định trong 2 tháng** và có **ít nhất 3 mã bán đều**, chuyển sang mô hình: gom container mỗi tuần → kho 3PL tại Úc → giao 2–7 ngày cho mã bán chạy. Điều kiện đi kèm: có bên nhập khẩu tại Úc, đại lý hải quan, xử lý GST và thuế ở biên giới, hợp đồng 3PL.
