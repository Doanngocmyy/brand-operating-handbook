# Operating Handbook — DTC furniture brand (AU · SG)

Sổ tay vận hành cho một brand nội thất bán trực tiếp (DTC) tại Úc và Singapore, team vận hành ở Việt Nam, hàng sản xuất tại Trung Quốc. Viết từ góc nhìn Founder/CEO, dùng để đào tạo và điều hành team.

**Đọc bản web:** GitHub Pages của repo này (thư mục `docs/`).

## Nội dung

| # | Trang | Cho ai |
|---|---|---|
| 00 | Thư của Founder | Cả team |
| 01 | Nguyên tắc cốt lõi & lằn ranh đỏ | Cả team |
| 02 | Mô hình kinh doanh & quy tắc giá | Quản lý |
| 03 | Tổ chức, vai trò, quyền duyệt | Cả team |
| 04 | Chuẩn hóa sản phẩm (danh mục, hạng, màu, dung sai) | Mua hàng, Listing |
| 05 | Nhà cung cấp: chọn, đối chiếu, chấm điểm | Mua hàng & QC |
| 06 | Đóng gói, nhãn, chứng từ hải quan | Mua hàng & QC |
| 07 | Vận hành đơn hàng (trạng thái, SLA) | Vận hành |
| 08 | Chăm sóc khách hàng, bảng bồi thường, mẫu tin | CSKH |
| 09 | Chính sách giao hàng, đổi trả (bản tiếng Anh cho web) | CSKH, Quản lý |
| 10 | Marketing & mạng xã hội | Marketing |
| 11 | KPI & nhịp vận hành | Cả team |
| 12 | Lộ trình 90 ngày | Quản lý |
| 13 | Công cụ & biểu mẫu | Cả team |

## Cấu trúc repo

```
content/     Markdown của từng trang (sửa ở đây)
assets/      CSS
docs/        Website đã build (GitHub Pages)
templates/   Biểu mẫu: chứng từ NCC (xlsx), sheet theo dõi đơn (csv)
tools/       Script Python chuẩn hóa dữ liệu sản phẩm
site.json    Tên brand, repo — đổi một lần là đổi toàn bộ
build.py     Tạo lại docs/ từ content/
```

```bash
pip install markdown
python build.py
```

## Quy tắc bảo mật (repo công khai)

- Không commit dữ liệu khách hàng, đơn hàng, thông tin NCC, file Excel gốc, mật khẩu, token.
- Chỉ đưa lên số liệu đã tổng hợp và quy trình.
- `.gitignore` chặn `*.xlsx`, `*.csv` ngoài thư mục `templates/`, và các thư mục dữ liệu.

*Các nội dung pháp lý là hướng dẫn vận hành, không phải tư vấn pháp lý.*
