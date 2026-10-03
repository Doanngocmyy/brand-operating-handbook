---
title: Vị trí, RACI & phân quyền
badges: internal, onboarding
---

# Vị trí, trách nhiệm và phân quyền

Mỗi việc có **đúng một vị trí chủ trì**. Vị trí được thiết kế để tách được: giai đoạn đầu 1 người kiêm nhiều mã, khi tuyển thêm thì giao nguyên mã đó cho người mới, kèm đúng phần dữ liệu cần dùng. Trang bắt đầu cho từng vị trí: [Find by role](tim-theo-vai-tro.html).

<div class="legend"><span><span class="r ceo">P0 CEO</span></span><span><span class="r ops">P1 OPS</span></span><span><span class="r src">P2 SRC</span></span><span><span class="r log">P3 LOG</span></span><span><span class="r cx">P4 CX</span></span><span><span class="r mkt">P5 MKT</span></span><span><span class="r fin">P6 FIN</span></span></div>

## 1. Bảy vị trí {#positions}

<div class="cards">
<div class="c" style="--rc:#1d1d1f"><span class="k">P0 · CEO</span><h4>Chủ doanh nghiệp</h4><p>Chiến lược, giá, ngân sách, duyệt NCC mới, bồi thường &gt; A$150, pháp lý.</p><p><b>KPI:</b> lãi ròng · chargeback</p></div>
<div class="c" style="--rc:#6b5a45"><span class="k">P1 · OPS</span><h4>Điều phối (Control tower)</h4><p>Rà SLA 09:00 hằng ngày, leo thang, duyệt lô, duyệt A$51–150, sửa SOP.</p><p><b>KPI:</b> % giao trong khung</p></div>
<div class="c" style="--rc:#2e7d4f"><span class="k">P2 · SRC</span><h4>Mua hàng &amp; QC</h4><p>Hỏi tồn, lập PO, theo dõi xưởng, QC kho gom, claim NCC. Tiếng Trung.</p><p><b>KPI:</b> % PO ≤ 24h · % lỗi QC</p></div>
<div class="c" style="--rc:#0f7c80"><span class="k">P3 · LOG</span><h4>Logistics &amp; Hải quan</h4><p>Cắt lô, chứng từ, forwarder, broker, hãng giao, thu hồi hàng.</p><p><b>KPI:</b> lead time lô · % lô bị giữ</p></div>
<div class="c" style="--rc:#2f6fb0"><span class="k">P4 · CX</span><h4>Chăm sóc khách</h4><p>Kiểm đơn, xác nhận, cập nhật 7 ngày, mở và đóng case, đề xuất bồi thường.</p><p><b>KPI:</b> phản hồi đầu · % case đóng ≤ 7d</p></div>
<div class="c" style="--rc:#b5562b"><span class="k">P5 · MKT</span><h4>Marketing &amp; Listing</h4><p>Trang sản phẩm từ spec đã duyệt, quảng cáo, nội dung, review thật.</p><p><b>KPI:</b> MER · CTR</p></div>
<div class="c" style="--rc:#7a4fa3"><span class="k">P6 · FIN</span><h4>Tài chính</h4><p>Trả NCC, trả cước/thuế, thực hiện hoàn tiền, xử lý dispute, đối soát.</p><p><b>KPI:</b> lãi thực/đơn · hoàn đúng hạn</p></div>
</div>

## 2. Ai làm gì theo giai đoạn (RACI) {#raci}

R = làm · A = chịu trách nhiệm cuối · C = được hỏi · I = được báo. Mỗi dòng chỉ có **một A**.

| Giai đoạn | P0 CEO | P1 OPS | P2 SRC | P3 LOG | P4 CX | P5 MKT | P6 FIN |
|---|---|---|---|---|---|---|---|
| **SOP-A · Đơn chuẩn** | | | | | | | |
| S1 Nhận & xác nhận đơn | – | I | – | – | **A/R** | – | – |
| S2 Đặt NCC + thanh toán NCC | – | I | **A/R** | – | I | – | R |
| S3 Theo dõi xưởng gửi | – | C | **A/R** | – | I | – | – |
| S4 Kho gom · QC | – | I | **A/R** | C | I | – | – |
| S5 Cắt lô · chứng từ · trả cước | – | C | C | **A/R** | – | – | R |
| S6 Thông quan | – | I | – | **A/R** | I | – | C |
| S7 Giao chặng cuối | – | I | – | **A/R** | C | – | – |
| S8 Sau giao · đóng đơn | – | **A** | – | R | R | I | R |
| Cập nhật 7 ngày cho khách | – | I | C | C | **A/R** | – | – |
| **SOP-B · Hậu mãi** | | | | | | | |
| B1–B2 Mở case, thu bằng chứng | – | I | – | – | **A/R** | – | – |
| B3 Duyệt ≤ A$50 | – | I | – | – | **A/R** | – | I |
| B3 Duyệt A$51–150 | I | **A** | C | C | R | – | I |
| B3 Duyệt > A$150 · hoàn 100% | **A** | R | C | C | R | – | I |
| B5 Gửi bù · đổi mới · thu hồi | – | I | **A/R** | R | I | – | – |
| B5 Thực hiện hoàn tiền | – | I | – | – | I | – | **A/R** |
| B6 Claim NCC / hãng giao | – | I | **A/R** | R | – | – | I |
| D Chargeback | I | **A** | – | C | R | – | R |
| **Nền tảng** | | | | | | | |
| Chọn mã hàng, duyệt NCC mới | **A** | C | R | C | – | C | – |
| Đăng / sửa trang sản phẩm | I | C | C | – | – | **A/R** | – |
| Ngân sách quảng cáo tuần | **A** | I | – | – | – | R | C |
| Sửa SOP, chính sách | **A** | R | C | C | C | C | C |

## 3. Tách quyền: người đề xuất ≠ người duyệt ≠ người chi tiền {#separation}

| Dòng tiền | Đề xuất | Duyệt | Chi |
|---|---|---|---|
| Trả NCC | <span class="r src">SRC</span> | <span class="r ops">OPS</span> (đơn thường) · <span class="r ceo">CEO</span> (NCC mới) | <span class="r fin">FIN</span> |
| Bồi thường, hoàn tiền | <span class="r cx">CX</span> | theo mức: <span class="r cx">CX</span> ≤ 50 · <span class="r ops">OPS</span> 51–150 · <span class="r ceo">CEO</span> &gt; 150 | <span class="r fin">FIN</span> |
| Cước, thuế lô | <span class="r log">LOG</span> | <span class="r ops">OPS</span> | <span class="r fin">FIN</span> |
| Quảng cáo | <span class="r mkt">MKT</span> | <span class="r ceo">CEO</span> | thẻ công ty |

Một người kiêm cả ba bước (giai đoạn 1 người) thì ghi lý do vào case và CEO rà lại mỗi thứ Sáu.

## 4. Dữ liệu cần biết (giữ bí mật mô hình) {#data-access}

● dùng đầy đủ · ◐ chỉ xem phần cần · – không có quyền. **Mã đơn** là khóa nối giữa các vị trí; không ai cần thấy toàn bộ.

| Dữ liệu | CEO | OPS | SRC | LOG | CX | MKT | FIN |
|---|---|---|---|---|---|---|---|
| Tên, email, SĐT khách | ● | ◐ | – | – | ● | – | ◐ |
| Địa chỉ giao | ● | ◐ | – | ◐ chặng cuối | ● | – | – |
| Danh tính NCC, link, chat NCC | ● | ◐ | ● | – | – | – | ◐ |
| Giá mua NCC | ● | ◐ | ● | – | – | – | ● |
| Forwarder, broker, giá cước | ● | ◐ | – | ● | – | – | ● |
| Landed cost, biên lãi | ● | ◐ | – | – | – | – | ● |
| Trạng thái đơn, ETA | ● | ● | ● | ● | ● | ◐ tổng | ● |
| Chi quảng cáo, ROAS | ● | ◐ | – | – | – | ● | ● |
| Hoàn tiền, cổng thanh toán | ● | ◐ | – | – | ◐ trạng thái | – | ● |

**Cách thực hiện:**

- Shopify: tài khoản nhân viên theo vị trí, chỉ bật quyền cần (CX: Orders, Customers; MKT: Products; không ai ngoài CEO/FIN vào Payments).
- Tracker: mỗi vị trí một tab hoặc một bản xem lọc. Tab NCC và tab chi phí không chia sẻ cho CX, MKT.
- SRC làm việc với NCC bằng **mã đơn + SKU**, không có tên hay địa chỉ khách. Nhãn giao chặng cuối do LOG in tại nước khách.
- Mỗi người một tài khoản, xác thực 2 lớp, ít nhất 2 quản trị viên cho Shopify và Meta. Nghỉ việc: thu hồi quyền trong ngày.

## 5. Kiêm nhiệm theo quy mô {#staffing}

| Quy mô | Người 1 | Người 2 | Người 3 | Người 4 |
|---|---|---|---|---|
| Khởi đầu (1 người) | P0 · P1 · P2 · P3 · P4 · P5 · P6 | | | |
| ~ 5 đơn/ngày (2 người) | P0 · P1 · P5 · P6 | **P4 CX** + P3 | | |
| ~ 15 đơn/ngày (3 người) | P0 · P5 · P6 | P1 OPS + P3 LOG | **P2 SRC** (tiếng Trung) | |
| ~ 30 đơn/ngày (4+ người) | P0 · P5 | P1 OPS | P2 SRC | P4 CX · P3 tách khi cần · P6 kế toán thuê ngoài |

Thứ tự tuyển: **CX trước** (tốn giờ nhất, rủi ro chargeback cao nhất), sau đó SRC. Người mới nhận đúng trang SOP và đúng tab dữ liệu của vị trí mình.
