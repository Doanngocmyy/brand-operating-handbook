---
title: Vận hành đơn hàng
order: 7
---

# Vận hành đơn hàng

Mỗi đơn đi qua 10 trạng thái. Trạng thái trên Shopify và trong sheet theo dõi phải **luôn khớp với thực tế**. Đây là quy tắc quan trọng nhất của bộ phận vận hành.

## 1. Trạng thái đơn

| Trạng thái | Trên Shopify | Điều kiện để chuyển sang | Báo khách |
|---|---|---|---|
| CHỜ MUA | Unfulfilled | Đã kiểm đơn và xác nhận với khách | Email xác nhận + khung thời gian giao |
| ĐÃ MUA | Unfulfilled | Có mã đơn đặt xưởng | – |
| XƯỞNG ĐÃ GỬI | Unfulfilled | Có vận đơn nội địa TQ | – |
| TẠI KHO GOM | Unfulfilled | Kho xác nhận nhập đủ kiện, QC đạt | "Đơn của bạn đã qua kiểm tra" + ảnh QC |
| ĐÃ XUẤT | Fulfilled + tracking | Có vận đơn quốc tế **và lượt quét đầu tiên** | Email tracking |
| THÔNG QUAN | Fulfilled | Tracking báo tới cảng hoặc hải quan | Cập nhật |
| ĐANG GIAO | Fulfilled | Đã giao cho hãng giao nội địa | Hãng giao hẹn ngày |
| ĐÃ GIAO | Fulfilled | Hãng giao xác nhận hoặc có ảnh giao | Hướng dẫn lắp + mời review sau 3 ngày |
| ĐÓNG | Archived | Không còn vấn đề, đủ chi phí | – |
| HỦY / HOÀN | Refunded | Đã hoàn tiền | Email hoàn tiền |

**Không bao giờ** bấm Fulfilled hay gửi tracking khi hàng chưa có lượt quét thật của hãng vận chuyển.

## 2. Các bước và thời hạn (SLA)

### B0. Trước khi bán: chuẩn listing

Mã hàng phải đạt 7 tiêu chí ở trang [Chuẩn hóa sản phẩm](04-san-pham-chuan-hoa.html), có 2 NCC, đạt ngưỡng lãi trong bảng tính giá, và khung thời gian giao đúng theo thị trường.

### B1. Nhận đơn — trong 4 giờ làm việc (CSKH & Listing)

1. Kiểm địa chỉ có giao được không (vùng xa, đảo), số điện thoại đủ chưa. Đơn giá trị cao bất thường hoặc tên/địa chỉ không khớp: hỏi lại trước khi mua.
2. Gửi email xác nhận: sản phẩm, khung thời gian giao thật, điều kiện hủy miễn phí.
3. Tạo dòng trong sheet theo dõi, trạng thái CHỜ MUA.

### B2. Đặt hàng xưởng — trong 24 giờ sau khi khách thanh toán (Mua hàng & QC)

1. Hỏi lại tồn kho và **ngày xuất cụ thể**. Không có hàng thì chuyển NCC dự phòng. Không có cả hai thì báo khách trong 24 giờ.
2. Đúng mã màu NCC, size, chất liệu. Không trộn 2 NCC trong một đơn (lệch màu).
3. Gửi ngay mẫu tin nhắn NCC ([trang Nhà cung cấp](05-nha-cung-cap.html)): đóng gói xuất khẩu, nhãn kiện X/Y, túi phụ kiện, ảnh trước khi gửi.
4. Thanh toán qua sàn để có bảo vệ người mua. NCC ngoài sàn chỉ khi có thỏa thuận rõ.
5. Ghi mã đơn xưởng, giá, NCC vào sheet. Trạng thái ĐÃ MUA.

### B3. Theo dõi xưởng gửi hàng — có vận đơn nội địa trong 72 giờ sau ngày hẹn

- Quá 2 ngày: nhắc NCC. Quá 5 ngày: báo Ops Lead, cân nhắc chuyển NCC dự phòng và báo khách. Quá 7 ngày: đổi NCC.

### B4. Nhận tại kho gom và QC — QC trong 2 ngày sau khi nhập kho

1. Kho xác nhận nhập kho và chụp ảnh, quay video: đủ số kiện, bao bì nguyên, nhãn X/Y, bao bì gỗ có dấu ISPM-15 (nếu có).
2. Hàng giá trị cao hoặc dễ hỏng: mở kiểm màu, kích thước, bề mặt.
3. Lỗi hoặc sai: **trả lại NCC ngay tại TQ**, trong thời hạn trả hàng của kho. Đây là điểm trả hàng rẻ nhất và cuối cùng.
4. Đủ kiện: trạng thái TẠI KHO GOM. Gửi khách ảnh QC.

### B5. Cắt lô và gửi quốc tế — 1 ngày cố định mỗi tuần

- Chứng từ đủ theo [trang Đóng gói & chứng từ](06-dong-goi-nhan-chung-tu.html). Mô tả hàng đúng, giá trị đúng.
- Có tracking quốc tế **và lượt quét đầu tiên** thì mới chuyển ĐÃ XUẤT và gửi tracking cho khách.

### B6. Thông quan và giao chặng cuối

- Bị giữ ở hải quan hoặc kiểm dịch: báo khách trong 24 giờ, nói lý do thật và ngày dự kiến mới.
- Hãng giao hẹn ngày với khách. Đơn nhiều kiện phải giao đủ số kiện.

### B7. Sau giao

- Sau 3 ngày: email hướng dẫn lắp và mời review. Mời mọi khách như nhau, không trả tiền đổi review tốt, không lọc review xấu.
- Có vấn đề: chuyển sang quy trình [CSKH](08-cskh.html).

## 3. Cập nhật chủ động cho khách

| Mốc | Nội dung | Kênh |
|---|---|---|
| Xác nhận đơn | Sản phẩm, khung thời gian, điều kiện hủy | Email |
| Mỗi 7 ngày khi chưa giao | Trạng thái thật hiện tại, kể cả khi chưa có gì mới | Email hoặc SMS |
| QC đạt | Ảnh QC của chính đơn đó | Email |
| Đã xuất | Tracking + giải thích tracking đường biển có thể đứng yên vài ngày | Email |
| Sắp trễ | Báo trước ít nhất 7 ngày: lý do thật, ngày mới, lựa chọn chờ, đổi hoặc hủy | Email + tin nhắn |
| Đã giao | Hướng dẫn lắp, cách liên hệ hỗ trợ | Email |

## 4. Cảnh báo tự động trong sheet theo dõi

| Cảnh báo | Điều kiện | Ai xử lý |
|---|---|---|
| Chưa đặt hàng | > 48 giờ sau thanh toán vẫn CHỜ MUA | Mua hàng & QC |
| Xưởng quá hẹn | Quá ngày hẹn gửi 2 ngày | Mua hàng & QC |
| Sắp vượt khung | Còn 14 ngày tới hạn cuối mà chưa ĐÃ XUẤT | Ops Lead + CSKH |
| Vượt khung | Quá hạn cuối đã hứa | CSKH chủ động đề nghị chờ có bồi thường hoặc hủy hoàn 100% |
| Khách chờ trả lời | Tin nhắn > 24 giờ chưa có người trả lời | CSKH |

Mẫu sheet theo dõi: [templates/order-tracker-template.csv](https://github.com/{{REPO}}/blob/main/templates/order-tracker-template.csv).
