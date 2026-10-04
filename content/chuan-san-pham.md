---
title: Chuẩn hóa sản phẩm
badges: onboarding
---

# Chuẩn hóa sản phẩm

Một mã hàng chỉ được bán khi đạt đủ 7 tiêu chí bên dưới. Mục tiêu: khách nhận đúng món mình thấy, đúng kích thước, đúng màu, lắp được.

{{SOT:sku,listing}}

## Mã sản phẩm và SKU {#catalogue}

| Mã | Ví dụ | Quy tắc |
|---|---|---|
| Mã mẫu | `TVU0001` | Loại hàng (3 chữ) + số mẫu trong loại (4 số). Cấp một lần, không đổi, không tái sử dụng. |
| SKU | `TVU0001-V001` | Mã mẫu + số cấu hình bán. Một SKU = một cấu hình cụ thể. |
| Vị trí kho (sau này) | `AU01-A-01-03` | Kho, khu, kệ, tầng. Không nằm trong SKU. |

Ý nghĩa của SKU (màu thân, màu chân/khung, W × D × H, cấu hình, vật liệu) nằm trong bảng **master SKU**, không nằm trong mã. Nhãn và phiếu soạn hàng in cả SKU lẫn mô tả, ví dụ `TVU0001-V001 · TV Unit · Walnut body / Black legs · W180 × D40 × H50 cm · CARTON 1 OF 3`.

**Khi nào cấp SKU mới:** đổi màu, đổi kích thước quá 2 cm, đổi vật liệu, thêm hoặc bớt bộ phận (LED, ngăn kéo, chân…). **Giữ nguyên SKU** khi đổi NCC, đổi tên hiển thị màu hoặc đổi giá. SKU ngừng bán chuyển sang `ARCHIVED`, không cấp lại cho sản phẩm khác.

**Mã đã cấp được khóa** trong file đăng ký mã (lưu nội bộ, không đưa lên repo công khai): chạy lại công cụ chuẩn hóa không đánh số lại.

### Loại hàng: mỗi mẫu có đúng một loại chính {#types}

Khi một chiếc tủ có thể thuộc nhiều loại, chọn loại **đầu tiên khớp** theo thứ tự: **TVU** kệ TV (thấp, H ≤ 70, để TV) → **VAN / BCB** phòng tắm (có chậu hoặc chịu ẩm) → **WIN** tủ trưng bày (cửa kính là chính) → **SHO** tủ giày (ngăn nghiêng/lật) → **SBD** tủ buffet (H ≤ 100, W ≥ 120) → **CAB** tủ đựng đồ còn lại.

| Phòng (collection) | Loại hàng (mã) |
|---|---|
| Living | TV Units (TVU) · Coffee Tables (COF) · Side Tables (SID) · Sofas (SOF) · Armchairs (ARM) |
| Dining | Dining Tables (DTB) · Dining Chairs (DCH) · Bar Tables (BRT) · Bar Stools (BSL) · Sideboards (SBD) · Display Cabinets (WIN) · Kitchen Islands (KIS) |
| Bedroom | Bed Frames (BFR) · Bedside Tables (BST) · Chests of Drawers (DRS) · Wardrobes (WRD) |
| Entryway & Storage | Shoe Cabinets (SHO) · Console Tables (CON) · Bookshelves (BKS) · Storage Cabinets (CAB) · Benches (BEN) |
| Office | Desks (DSK) · Office Chairs (OCH) |
| Bathroom | Vanities (VAN) · Bathroom Cabinets (BCB) |
| Decor | Mirrors (MIR) · Lighting (LGT) · Rugs (RUG) · Wall Panels (WPN) |

Phòng là **collection**, không phải loại: ghế dài, bàn console, kệ sách có thể nằm ở nhiều collection. Đồ ngoài trời ghi theo loại thật (bàn, ghế, sofa) kèm thuộc tính `outdoor`. Mã loại không đổi sau khi đã cấp cho mẫu; muốn tách nhóm thì chỉ cập nhật danh mục mã.

## Phân hạng: hàng chuẩn đi trước {#grading}

Mỗi mã bắt đầu với 100 điểm và bị trừ điểm theo từng "ngoại lệ".

| Hạng | Điều kiện | Xử lý |
|---|---|---|
| **A – Chuẩn** | Từ 80 điểm, không có ngoại lệ lớn | Đối chiếu NCC, chọn 40–60 mã để ra mắt |
| **B – Cần xem** | Dưới 80 điểm. Bị trừ vì: dễ vỡ (đá, kính, gương) −25 · lắp tường hoặc cần thợ −15 · option lạ −15 · màu chưa đặt tên −15 · trên 18 biến thể −10 · giá chênh trên 3 lần −10 · không đọc được size −10 · ngoài nhóm ra mắt −10 | Chỉ bán khi đã có giải pháp đóng gói và hướng dẫn lắp |
| **C – Loại** | Làm theo yêu cầu, size đặc biệt, giường theo chuẩn nệm, sofa nhiều cấu hình hoặc chọn vải, trên 36 biến thể, không có ảnh | Không bán giai đoạn đầu. Sau này có thể chuẩn hóa lại, ví dụ chỉ bán 1 cấu hình |

## Chuẩn màu: một tên duy nhất cho mỗi màu {#colour}

Mọi tên màu của NCC ("胡桃色", "walnut", "black walnut", "dark wood"…) đều quy về **một** tên chuẩn có mã 3 chữ. Chất liệu và bề mặt (PU Leather, Boucle, Velvet, Sintered Stone, Marble, Glass, Gloss, Matte…) ghi ở cột riêng, không lẫn vào tên màu.

| Họ màu | Tên chuẩn (mã) | Gom từ |
|---|---|---|
| Gỗ | Natural Oak (NOK) | natural, oak, wood, maple, ash, pine, original, log |
| Gỗ | White Oak (WOK) | white oak, light oak, white wash |
| Gỗ | Warm Brown (WBR) | honey, teak, golden pine, brown oak |
| Gỗ | Walnut (WAL) | walnut |
| Gỗ | Dark Walnut (DWL) | black walnut, dark wood, espresso |
| Gỗ | Black Oak (BOK) · Cherry (CHR) | black oak · cherry |
| Trung tính | White (WHT) · Cream (CRM) · Beige (BEG) · Light Grey (LGR) · Grey (GRY) · Dark Grey (DGR) · Black (BLK) · Brown (BRN) · Clear (CLR) | ivory/off-white → Cream; khaki/sand/linen → Beige; slate/smoky → Dark Grey |
| Màu | Green · Blue · Pink · Orange · Yellow · Red · Purple · Multicolour | |
| Kim loại | Gold (GLD) · Silver (SLV) | brass, champagne, bronze → Gold |
| Đặc biệt | Stone Pattern (STN) | các vân đá đặt tên riêng |

**Hai tông màu** ghi theo thứ tự cố định: màu thân/mặt chính trước, màu chân/khung/viền sau, ví dụ `Walnut / Black`, `White / Gold`. Trong master SKU lưu thành hai cột `body_colour` và `accent_colour`.

**Core palette của {{BRAND}}** (ưu tiên cho phong cách tối giản): Natural Oak · Walnut · Dark Walnut · Black · White · Cream · Beige · Grey · Light Grey · Dark Grey. Màu ngoài core chỉ thêm khi bán chạy.

## Kích thước và dung sai {#dimensions}

Mọi kích thước ghi theo chuẩn Úc **W × D × H, đơn vị cm**: W = ngang/dài mặt trước, D = sâu, H = cao. Bàn tròn ghi đường kính ở W. Nguồn duy nhất là bản vẽ của NCC đã được kiểm bằng hàng mẫu.

| Việc | Dung sai | Vượt thì sao |
|---|---|---|
| Ghép mẫu với listing NCC | ±2 cm mỗi chiều | Coi là mẫu khác |
| Kích thước đăng web | Theo bản vẽ, ghi "±1 cm" | Không làm tròn tùy ý |
| QC trước khi xuất | Đạt ≤ ±5 mm · cảnh báo 5–10 mm · loại > 10 mm | NCC làm lại hoặc đổi |

Sai số 5–10 cm **không chấp nhận được**. Tiêu chuẩn đồ gỗ Trung Quốc GB/T 3324 cho phép ±5 mm. Luật Úc yêu cầu hàng phải đúng mô tả. Khách mua kệ TV hay tủ áo để vừa hốc tường.

Cần chặt hơn với: giường (vừa nệm chuẩn Úc, Queen 153 × 203 cm), mặt đá hoặc kính lắp theo lỗ, tủ treo tường. Hàng bọc nệm (sofa, ghế) cho phép ±2 cm và ghi rõ trên web.

## 7 tiêu chí để một mã được đăng bán {#listing-criteria}

- [ ] Kích thước cố định, tối đa 3 size mỗi mẫu. Không nhận size riêng.
- [ ] Màu nằm trong bảng chuẩn, có ảnh thật ban ngày hoặc mẫu màu từ NCC.
- [ ] Chất liệu ghi đúng từng bộ phận (gỗ tự nhiên / veneer / MDF / ván dăm, lớp phủ).
- [ ] Mỗi trang bán một món. Bán theo bộ thì có mã "Set" riêng, ghi rõ bộ gồm những gì.
- [ ] Có hướng dẫn lắp tiếng Anh (PDF + danh sách phụ kiện). Lắp trên 45 phút thì ghi rõ trên web.
- [ ] Đóng gói đạt chuẩn ([mục Đóng gói](dong-goi-chung-tu.html)), biết trước số kiện, kích thước và cân nặng từng kiện.
- [ ] Tủ áo, kệ sách, buffet cao từ 686 mm và mọi kệ TV có nhãn cảnh báo đổ ngã kèm bộ neo tường.
