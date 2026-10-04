"""Navigation + routing data for the handbook (single source for cards, maps, panels and callouts).

Everything here is a ROUTING layer: short labels + deep links into the SOP/standard pages.
The procedures themselves live in content/*.md. If a rule changes, change it in the page first,
then update the summary here.
"""

# ----------------------------------------------------------------------------- navigation
SECTIONS = [
    ("start", "Start here"),
    ("run", "Run the business"),
    ("std", "Standards"),
    ("mgmt", "Management"),
]

# slug: page file stem in docs/ ; old: previous URL (a redirect stub is generated)
PAGES = [
    # slug,                     section, nav label,                              source md,                   old slug
    ("index",                   "start", "Operating Map",                        "index.md",                  None),
    ("tim-theo-vai-tro",        "start", "Find by role",                         "tim-theo-vai-tro.md",       None),
    ("tim-theo-su-kien",        "start", "Find by task / event",                 "tim-theo-su-kien.md",       None),
    ("chuoi-cung-ung",          "run",   "Supply Chain SOP (end-to-end)",        "chuoi-cung-ung.md",         None),
    ("sop-a-don-chuan",         "run",   "Standard Order (SOP-A)",               "sop-a-don-chuan.md",        "07-van-hanh-don-hang"),
    ("sop-b-hau-mai",           "run",   "Exceptions & Cases (SOP-B)",           "sop-b-hau-mai.md",          "08-cskh"),
    ("kpi-sla-nhip",            "run",   "KPI, SLA & Rhythm",                    "kpi-sla-nhip.md",           "11-kpi-nhip-van-hanh"),
    ("chuan-san-pham",          "std",   "Product & SKU Standard",               "chuan-san-pham.md",         "04-san-pham-chuan-hoa"),
    ("nha-cung-cap-qc",         "std",   "Supplier & QC Standard",               "nha-cung-cap-qc.md",        "05-nha-cung-cap"),
    ("dong-goi-chung-tu",       "std",   "Packaging, Labels & Import Docs",      "dong-goi-chung-tu.md",      "06-dong-goi-nhan-chung-tu"),
    ("thuong-hieu-marketing",   "std",   "Brand & Marketing Rules",              "thuong-hieu-marketing.md",  "10-marketing"),
    ("chinh-sach-khach-hang",   "std",   "Customer-facing Policy",               "chinh-sach-khach-hang.md",  "09-chinh-sach"),
    ("vai-tro-quyen-han",       "mgmt",  "Roles, Authority & Access",            "vai-tro-quyen-han.md",      "03-to-chuc-vai-tro"),
    ("mo-hinh-kinh-doanh",      "mgmt",  "Business Model & Unit Economics",      "mo-hinh-kinh-doanh.md",     "02-mo-hinh-kinh-doanh"),
    ("chien-luoc-ke-hoach",     "mgmt",  "Strategy, OKR & Roadmap",              "chien-luoc-ke-hoach.md",    None),
    ("lo-trinh-90-ngay",        "mgmt",  "90-Day Launch Plan",                   "lo-trinh-90-ngay.md",       "12-lo-trinh-90-ngay"),
    ("cong-cu-bieu-mau",        "mgmt",  "Tools & Templates",                    "cong-cu-bieu-mau.md",       "13-cong-cu-mau"),
    # low-priority "About" pages: linked under the sidebar, not in the main hierarchy
    ("nguyen-tac",              "about", "Operating principles",                 "nguyen-tac.md",             "01-nguyen-tac"),
    ("thu-founder",             "about", "Founder note",                         "thu-founder.md",            None),
]

BADGES = {
    "daily": ("Daily use", "b-daily"),
    "onboarding": ("Onboarding", "b-onb"),
    "internal": ("Internal", "b-int"),
    "customer": ("Customer-facing", "b-cust"),
    "blocker": ("Launch blocker", "b-block"),
    "signoff": ("Legal / customs sign-off required", "b-sign"),
}

# ----------------------------------------------------------------------------- roles
ROLE_COLOURS = {"CX": "cx", "SRC": "src", "LOG": "log", "OPS": "ops", "MKT": "mkt", "FIN": "fin", "CEO": "ceo"}

A = "sop-a-don-chuan.html"
B = "sop-b-hau-mai.html"
K = "kpi-sla-nhip.html"
R = "vai-tro-quyen-han.html"
T = "cong-cu-bieu-mau.html"
TRACKER = "SHEET"                              # live Google Sheet (falls back to the Excel template)
DOCS_XLSX = "templates/Mau_chung_tu_NCC.xlsx"

ROLES = [
    dict(
        code="CX", p="P4", name="Customer Experience", vn="Chăm sóc khách",
        purpose="Kiểm đơn, xác nhận, cập nhật 7 ngày, mở và đóng case, đề xuất bồi thường.",
        daily_open=[("Tracker · tab DON: cờ “Sắp vượt ETA”, “Vượt ETA”, “>7d chưa cập nhật KH”", f"{K}#flags"),
                    ("Tracker · tab CASE: case chưa phản hồi, case mở > 7 ngày", f"{K}#flags"),
                    ("Hộp thư chung (khách Úc trước)", f"{K}#checklist")],
        onboarding=[("Customer-facing Policy", "chinh-sach-khach-hang.html"), ("SOP-A · S1 và S8", f"{A}#s1"),
                    ("SOP-B toàn bộ", B), ("Lằn ranh đỏ", "nguyen-tac.html#red-lines")],
        checklist=["07:00 Hộp thư, khách Úc trước", "09:00 Họp control tower",
                   "Sáng: kiểm + xác nhận đơn mới (S1)", "Chiều: cập nhật 7 ngày, case mới",
                   "Cuối ngày: không case nào > 24h chưa trả lời"],
        stages=[("S1 Nhận & xác nhận đơn · A/R", f"{A}#s1"), ("Cập nhật 7 ngày cho khách · A/R", f"{A}#continuous"),
                ("S8 Sau giao · R", f"{A}#s8"), ("B1–B2 Mở case, bằng chứng · A/R", f"{B}#b1"),
                ("B3 Duyệt ≤ A$50 · A/R", f"{B}#approval")],
        limit="Tự duyệt đền bù ≤ A$50. A$51–150 → OPS. > A$150 hoặc hoàn 100% → CEO. Khách nhắc chargeback → gọi ≤ 24h, OPS chịu trách nhiệm cuối.",
        tools=[("Tracker DON: cột 20 Xác nhận, “Cập nhật KH gần nhất”", TRACKER), ("Tracker CASE", TRACKER),
               ("Mẫu tin nhắn tiếng Anh", f"{B}#templates"), ("FAQ dán web", f"{B}#faq")],
        never=["Gửi tracking hoặc bấm Fulfilled khi chưa có lượt quét thật.",
               "Đưa lý do trễ không có bằng chứng cho đúng đơn đó.",
               "Bồi thường ngoài bảng hoặc vượt mức duyệt của mình.",
               "Ghi tên, email, SĐT, địa chỉ khách vào tracker.",
               "Gửi “đang chuyển nhân viên” khi không có ai trực."],
    ),
    dict(
        code="SRC", p="P2", name="Sourcing & Quality Control", vn="Mua hàng & QC",
        purpose="Hỏi tồn, lập PO, theo dõi xưởng, QC kho gom, claim NCC. Tiếng Trung.",
        daily_open=[("Tracker · DON: cờ “Chưa đặt NCC >24h”, “NCC quá hẹn >2d”", f"{K}#flags"),
                    ("Tin nhắn NCC qua đêm", f"{K}#checklist")],
        onboarding=[("Product & SKU Standard", "chuan-san-pham.html"), ("Supplier & QC Standard", "nha-cung-cap-qc.html"),
                    ("Packaging, Labels & Import Docs", "dong-goi-chung-tu.html"), ("SOP-A · S2–S4", f"{A}#s2")],
        checklist=["07:00 Tin nhắn NCC qua đêm", "09:00 Họp control tower", "Sáng: đặt PO mọi đơn trạng thái 20 (S2)",
                   "Chiều: duyệt ảnh kiện, QC, claim NCC", "Cuối ngày: tracker đủ ngày + bằng chứng"],
        stages=[("S2 Đặt NCC · A/R", f"{A}#s2"), ("S3 Theo dõi xưởng · A/R", f"{A}#s3"), ("S4 Kho gom · QC · A/R", f"{A}#s4"),
                ("B5 Gửi bù · đổi mới · thu hồi · A/R", f"{B}#solutions"), ("B6 Claim NCC / hãng giao · A/R", f"{B}#root-cause")],
        limit="Không duyệt NCC mới (CEO duyệt), không chi tiền (FIN chi). NCC trễ: +2d nhắc · +5d báo OPS · +7d đổi NCC.",
        tools=[("Tracker DON: cột 30–50", TRACKER), ("Mẫu chứng từ + QC checklist NCC", DOCS_XLSX),
               ("Mẫu tin nhắn NCC (tiếng Trung)", "nha-cung-cap-qc.html#supplier-message"),
               ("Checklist hồ sơ NCC", "nha-cung-cap-qc.html#doc-checklist")],
        never=["Trộn 2 NCC trong một đơn.",
               "Chuyển trạng thái QC đạt khi chưa có ảnh QC của đúng đơn.",
               "Nhận hay ghi thông tin cá nhân của khách: làm việc bằng mã đơn + SKU.",
               "Chấp nhận bao bì gỗ nguyên khối không có dấu ISPM-15."],
    ),
    dict(
        code="LOG", p="P3", name="Logistics & Customs", vn="Logistics & Hải quan",
        purpose="Cắt lô, chứng từ, forwarder, broker, hãng giao, thu hồi hàng.",
        daily_open=[("Tracking các lô đang chạy", f"{K}#checklist"), ("Tracker · DON: đơn ở trạng thái 50–80", f"{A}#statuses")],
        onboarding=[("Packaging, Labels & Import Docs", "dong-goi-chung-tu.html"), ("SOP-A · S5–S7", f"{A}#s5"),
                    ("SOP-B · B2 Trả hàng & thu hồi", f"{B}#b2")],
        checklist=["07:00 Tracking lô đang chạy", "09:00 Họp control tower", "Sáng: chứng từ lô tuần (S5)",
                   "Chiều: hải quan, hãng giao, thu hồi", "Cuối ngày: tracker đủ ngày + bằng chứng"],
        stages=[("S5 Cắt lô · chứng từ · A/R", f"{A}#s5"), ("S6 Thông quan · A/R", f"{A}#s6"), ("S7 Giao chặng cuối · A/R", f"{A}#s7"),
                ("R5 Thu hồi hàng", f"{B}#b2")],
        limit="OPS duyệt lô và chứng từ trước khi xuất. Hàng bị giữ: báo ngay để khách được báo ≤ 24h.",
        tools=[("Tracker DON: cột 60–90", TRACKER), ("Bộ chứng từ lô hàng", "dong-goi-chung-tu.html#documents"),
               ("Mẫu CI · PL · shipping mark", DOCS_XLSX)],
        never=["Chuyển trạng thái 60 khi chưa có lượt quét thật.",
               "Khai mô tả, chất liệu, giá trị khác hàng thật.",
               "Gửi hàng lỗi về Trung Quốc thay vì thu hồi tại nước khách."],
    ),
    dict(
        code="OPS", p="P1", name="Operations / Control Tower", vn="Điều phối",
        purpose="Rà SLA 09:00 hằng ngày, leo thang, duyệt lô, duyệt A$51–150, sửa SOP.",
        daily_open=[("Dashboard: biểu đồ “Cờ SLA đang bật”", f"{K}#dashboard"), ("Mọi cột ⚑ trong DON và CASE", f"{K}#flags")],
        onboarding=[("Roles, Authority & Access", R), ("SOP-A", A), ("SOP-B", B), ("KPI, SLA & Rhythm", K)],
        checklist=["09:00 Chủ trì control tower, giao từng cờ cho một người", "Sáng: duyệt leo thang, duyệt A$51–150",
                   "Chiều: kiểm ngẫu nhiên 2 đơn, tin nhắn có khớp trạng thái không",
                   "Thứ Sáu 16:00: báo cáo tuần → CEO", "Ngày 01: rà khung ETA, rà lằn ranh đỏ, chấm điểm NCC"],
        stages=[("S8 Đóng đơn · A", f"{A}#s8"), ("S5 Duyệt lô · C", f"{A}#s5"), ("B3 Duyệt A$51–150 · A", f"{B}#approval"),
                ("Chargeback · A", f"{B}#b3"), ("Review nguyên nhân gốc thứ Sáu", f"{B}#root-cause")],
        limit="Duyệt A$51–150. Trên A$150 hoặc hoàn 100%, NCC mới, sửa chính sách → CEO.",
        tools=[("Dashboard + tab DON/CASE", TRACKER), ("Mẫu báo cáo tuần", f"{K}#weekly-report"),
               ("Bảng chấm điểm NCC", "nha-cung-cap-qc.html#scorecard")],
        never=["Duyệt vượt mức của mình (> A$150 hoặc hoàn 100%).",
               "Để một cờ đỏ qua họp 09:00 mà không có tên người xử lý trong ngày.",
               "Giữ khung ETA khi 10% đơn chậm nhất đã vượt khung."],
    ),
    dict(
        code="MKT", p="P5", name="Marketing & Listings", vn="Marketing & Listing",
        purpose="Trang sản phẩm từ spec đã duyệt, quảng cáo, nội dung, review thật.",
        daily_open=[("Số quảng cáo hôm qua: CTR, CPC, thêm giỏ, MER", f"{K}#checklist"), ("Bình luận và hộp thư mạng xã hội", f"{K}#checklist")],
        onboarding=[("Brand & Marketing Rules", "thuong-hieu-marketing.html"), ("Lằn ranh đỏ", "nguyen-tac.html#red-lines"),
                    ("7 tiêu chí đăng bán", "chuan-san-pham.html#listing-criteria")],
        checklist=["Đọc số quảng cáo hôm qua: CTR, CPC, thêm giỏ, MER",
                   "Trả lời bình luận trong ngày (không xóa bình luận tiêu cực có thật)",
                   "Đăng bài theo lịch, qua checklist 5 câu"],
        stages=[("Đăng / sửa trang sản phẩm · A/R", "chuan-san-pham.html#listing-criteria"),
                ("Ngân sách quảng cáo tuần · R (CEO duyệt)", "thuong-hieu-marketing.html#budget")],
        limit="Ngân sách quảng cáo do CEO duyệt. Tổng quảng cáo ≤ 25% doanh thu; chỉ tăng khi MER ≥ 4.",
        tools=[("Master SKU (thông số đã duyệt)", T + "#source-of-truth"), ("Duyệt trước khi đăng: 5 câu", "thuong-hieu-marketing.html#content-approval")],
        never=["Viết điều không chứng minh được: “solid wood”, “fast shipping”, “no mark-up”…",
               "Giá gạch Was/Now không có lịch sử giá thật, khan hiếm giả.",
               "Mua review, follower; ẩn bình luận tiêu cực có thật.",
               "Đăng nội dung creator có trả phí mà không ghi #ad / Paid partnership."],
    ),
    dict(
        code="FIN", p="P6", name="Finance", vn="Tài chính",
        purpose="Trả NCC, trả cước/thuế, thực hiện hoàn tiền, xử lý dispute, đối soát.",
        daily_open=[("Case đã duyệt chờ hoàn tiền (CASE: Ngày hoàn tiền trống)", f"{B}#refund-steps"),
                    ("Dispute mới từ cổng thanh toán", f"{B}#b3")],
        onboarding=[("Roles · tách quyền", f"{R}#separation"), ("SOP-B · Hoàn tiền 5 bước", f"{B}#refund-steps"),
                    ("Business Model · quy tắc giá", "mo-hinh-kinh-doanh.html#pricing")],
        checklist=["Thanh toán NCC qua sàn khi có PO (S2)", "Hoàn tiền đúng số đã duyệt, phương thức gốc",
                   "Thứ Sáu: đối soát chi phí thực từng đơn đã đóng"],
        stages=[("S2 Thanh toán NCC · R", f"{A}#s2"), ("S5 Trả cước · thuế lô · R", f"{A}#s5"),
                ("B5 Thực hiện hoàn tiền · A/R", f"{B}#refund-steps"), ("Chargeback · hồ sơ · R", f"{B}#b3"),
                ("S8 Đối soát landed cost · R", f"{A}#s8")],
        limit="Chỉ chi khi có người duyệt đúng mức trong case. Thiếu người duyệt → trả lại CX.",
        tools=[("File chi phí FIN (hạn chế quyền)", T + "#source-of-truth"), ("Tracker CASE: ngày hoàn, số thu hồi", TRACKER)],
        never=["Hoàn tiền khi chưa có người duyệt đúng mức.",
               "Hoàn qua chuyển khoản ngoài phương thức thanh toán gốc.",
               "Chia sẻ file chi phí, giá mua NCC cho CX hoặc MKT."],
    ),
    dict(
        code="CEO", p="P0", name="Decisions & approvals", vn="Duyệt cấp cao",
        purpose="Chiến lược, giá, ngân sách, duyệt NCC mới, bồi thường > A$150, pháp lý.",
        daily_open=[("Case chờ duyệt > A$150 / hoàn 100%", f"{B}#approval")],
        onboarding=[("Business Model & Unit Economics", "mo-hinh-kinh-doanh.html"), ("90-Day Launch Plan", "lo-trinh-90-ngay.html"),
                    ("Roles, Authority & Access", R)],
        checklist=["Duyệt case > A$150 / hoàn 100% trong 24h", "Thứ Sáu: đọc báo cáo tuần, quyết việc được nêu",
                   "Rà các bước một người kiêm cả đề xuất – duyệt – chi"],
        stages=[("B3 Duyệt > A$150 · hoàn 100% · A", f"{B}#approval"), ("Chọn mã, duyệt NCC mới · A", f"{R}#raci"),
                ("Ngân sách quảng cáo · A", "thuong-hieu-marketing.html#budget"), ("Sửa SOP, chính sách · A", f"{R}#raci")],
        limit="Cấp duyệt cuối. Các quyết định mở trước khi ra mắt nằm ở Launch blockers.",
        tools=[("Báo cáo tuần", f"{K}#weekly-report"), ("Việc cần CEO chốt", "lo-trinh-90-ngay.html#ceo-decisions"),
               ("Launch blockers", "lo-trinh-90-ngay.html#blockers")],
        never=["Duyệt lời hứa với khách vượt dữ liệu thật (Hứa ≤ Làm được ≤ Chứng minh được).",
               "Bỏ qua bước rà khi một người kiêm cả đề xuất, duyệt và chi tiền."],
    ),
]

# ----------------------------------------------------------------------------- tasks / events
TASKS = [
    dict(icon="①", title="Đơn mới vừa được thanh toán", en="A new order was paid",
         go=("SOP-A · S1 Nhận đơn", f"{A}#s1"), owner="CX", sla="≤ 4h làm việc",
         evidence="Email xác nhận + khung ETA đã gửi", tracker="DON · cột 20 Xác nhận",
         more=[("Mẫu email xác nhận", f"{B}#tpl-confirm")]),
    dict(icon="②", title="Cần đặt hàng NCC", en="Place an order with a supplier",
         go=("SOP-A · S2 Đặt NCC", f"{A}#s2"), owner="SRC", sla="≤ 24h sau thanh toán",
         evidence="Mã PO + ngày hẹn xuất · FIN đã thanh toán qua sàn", tracker="DON · cột 30, Hẹn NCC gửi",
         more=[("Mẫu tin nhắn NCC", "nha-cung-cap-qc.html#supplier-message"), ("Mẫu chứng từ NCC", DOCS_XLSX)]),
    dict(icon="!", title="NCC trễ hẹn hoặc QC trượt", en="Supplier late or QC failed", red=True,
         go=("SOP-A · Lối thoát S3 / S4", f"{A}#ex-s3"), owner="SRC → OPS", sla="+2d nhắc · +5d OPS · +7d đổi NCC",
         evidence="Ảnh QC / tin nhắn NCC", tracker="DON · cờ NCC quá hẹn",
         more=[("QC trượt", f"{A}#ex-s4"), ("Case C2 Trễ hạn", f"{B}#c2")]),
    dict(icon="③", title="Chuẩn bị lô hàng / chứng từ hải quan", en="Preparing a shipment / customs docs",
         go=("SOP-A · S5 Xuất lô", f"{A}#s5"), owner="LOG", sla="1 ngày cố định/tuần",
         evidence="Lượt quét thật của hãng vận chuyển", tracker="DON · cột 60",
         more=[("Bộ chứng từ", "dong-goi-chung-tu.html#documents"), ("Mẫu CI · PL", DOCS_XLSX)]),
    dict(icon="!", title="Đơn sắp tới hoặc đã quá ETA", en="Order approaching or past ETA", red=True,
         go=("SOP-B · C2 Trễ hạn", f"{B}#c2"), owner="CX", sla="Báo trước ≥ 7 ngày",
         evidence="Tin báo trễ có 3 lựa chọn", tracker="DON · cờ Sắp vượt / Vượt ETA",
         more=[("Mẫu báo trễ", f"{B}#tpl-delay"), ("Lối thoát ETA", f"{A}#ex-eta")]),
    dict(icon="!", title="Khách báo hỏng, thiếu, sai hàng hoặc muốn hoàn", en="Damage, missing, wrong item, refund", red=True,
         go=("SOP-B · Chọn loại case", f"{B}#cases"), owner="CX", sla="Phản hồi ≤ 4h LV",
         evidence="Nhãn kiện · ảnh lỗi · ảnh toàn món", tracker="CASE · một dòng/case",
         more=[("Mẫu nhận hàng hỏng", f"{B}#tpl-damaged"), ("Trả hàng & hoàn tiền", f"{B}#b2")]),
    dict(icon="!", title="Có tranh chấp thanh toán / chargeback", en="A chargeback has started", red=True,
         go=("SOP-B · B3 Chargeback", f"{B}#b3"), owner="OPS (CX gọi)", sla="Gọi khách ≤ 24h",
         evidence="Hồ sơ: ETA đã hứa, tracking, POD, trao đổi", tracker="CASE · loại C7",
         more=[("Case C7", f"{B}#c7")]),
    dict(icon="④", title="Ra mắt SKU hoặc sửa trang sản phẩm", en="Launching a SKU / changing a listing",
         go=("7 tiêu chí đăng bán", "chuan-san-pham.html#listing-criteria"), owner="MKT", sla="Trước khi đăng",
         evidence="Master SKU đã chốt + duyệt 5 câu", tracker="Master SKU",
         more=[("Duyệt 5 câu", "thuong-hieu-marketing.html#content-approval"), ("Đối chiếu NCC", "nha-cung-cap-qc.html#matching")]),
    dict(icon="⑤", title="Chủ trì control tower 09:00", en="Reviewing the 09:00 Control Tower",
         go=("Cờ SLA & cách xử lý", f"{K}#flags"), owner="OPS", sla="15 phút, hằng ngày",
         evidence="Mỗi cờ có tên người xử lý trong ngày", tracker="Dashboard",
         more=[("Dashboard", f"{K}#dashboard"), ("Nhịp vận hành", f"{K}#rhythm")]),
    dict(icon="⑥", title="Làm báo cáo tuần thứ Sáu", en="Preparing the Friday weekly report",
         go=("Mẫu báo cáo tuần", f"{K}#weekly-report"), owner="OPS → CEO", sla="Thứ Sáu 16:00",
         evidence="Ảnh Dashboard + case theo nguyên nhân", tracker="Dashboard · CASE",
         more=[("Mã nguyên nhân gốc", f"{B}#root-cause"), ("Bảng chấm điểm NCC", "nha-cung-cap-qc.html#scorecard")]),
]

# ----------------------------------------------------------------------------- lifecycle S1–S8
STAGES = [
    dict(code="S1", name="Đơn mới", en="New order", owner=["CX"], sla="≤ 4h LV", status="20",
         gate="Email xác nhận · ETA min/max", cust="Email xác nhận + khung ETA",
         exc=[("Không hợp lệ / không giao được", "C1", f"{A}#ex-s1")]),
    dict(code="S2", name="Đặt NCC", en="Supplier order", owner=["SRC", "FIN"], sla="≤ 24h", status="30",
         gate="Mã PO + ngày xuất · đã thanh toán sàn", cust="Cập nhật 7 ngày: đang sản xuất",
         exc=[("NCC hết hàng", "C1·C2", f"{A}#ex-s2")]),
    dict(code="S3", name="SX & gửi", en="Production & dispatch", owner=["SRC"], sla="≤ hẹn +2d", status="40",
         gate="Ảnh kiện duyệt · vận đơn nội địa", cust="Cập nhật 7 ngày",
         exc=[("NCC trễ", "C2", f"{A}#ex-s3")]),
    dict(code="S4", name="Kho gom · QC", en="Consolidation & QC", owner=["SRC"], sla="≤ 2d sau nhập", status="50",
         gate="Ảnh QC · checklist đạt", cust="Ảnh QC của chính đơn",
         exc=[("QC trượt", "C2", f"{A}#ex-s4")]),
    dict(code="S5", name="Xuất lô", en="Export batch", owner=["LOG", "OPS"], sla="1 ngày/tuần", status="60",
         gate="Lượt quét thật của hãng", cust="Fulfilled + email tracking",
         exc=[("Rủi ro ETA (≤ 14d chưa xuất)", "C2", f"{A}#ex-eta")]),
    dict(code="S6", name="Thông quan", en="Customs", owner=["LOG"], sla="báo giữ ≤ 24h", status="70",
         gate="Tracking tới cảng / hải quan", cust="Cập nhật 7 ngày · bị giữ báo ≤ 24h",
         exc=[("Bị giữ hải quan", "C2", f"{A}#ex-s6")]),
    dict(code="S7", name="Giao cuối", en="Last-mile delivery", owner=["LOG"], sla="hãng hẹn ngày", status="80→90",
         gate="Hãng nhận hàng → POD", cust="Hãng giao hẹn ngày",
         exc=[("Quá ETA max", "C2", f"{A}#ex-late")]),
    dict(code="S8", name="Sau giao · đóng", en="Post-delivery & close", owner=["CX", "FIN"], sla="D+3 · D+14", status="99",
         gate="D+14 không case · chi phí đủ", cust="D+3 hướng dẫn lắp + mời review",
         exc=[("Khách khiếu nại", "C3–C8", f"{A}#ex-s8")]),
]

# ----------------------------------------------------------------------------- SOP-B case router
CASES = [
    ("C1", "Hủy đơn", "Khách hủy · đơn không hợp lệ · hết hàng", "B1 → R5", "b1"),
    ("C2", "Trễ hạn", "≤ 14 ngày tới ETA max chưa xuất · quá ETA", "B1", "b1"),
    ("C3", "Hư hỏng khi nhận", "Trầy, mẻ, vỡ, ẩm", "B1 · B2", "b1"),
    ("C4", "Thiếu kiện / phụ kiện", "Thiếu ốc, kiện X/Y, hướng dẫn", "B1", "b1"),
    ("C5", "Sai hàng / khác mô tả", "Sai mã, size, màu, chất liệu", "B1 · B2", "b1"),
    ("C6", "Đổi ý", "≤ 14 ngày, chưa lắp, nguyên hộp", "B2", "b2"),
    ("C7", "Chargeback", "Ngân hàng / cổng báo dispute", "B3", "b3"),
    ("C8", "Bảo hành", "Lỗi phát sinh khi dùng", "B1", "b1"),
]

# ----------------------------------------------------------------------------- SOP control panels
PANELS = {
    "sop-a": [
        ("Dùng khi", "Đơn đã thanh toán trên Shopify, mã hàng đạt chuẩn đăng bán, giao AU/SG."),
        ("Không dùng khi", "Hủy, trễ ETA, hỏng/thiếu/sai, đổi ý, chargeback → <a href='sop-b-hau-mai.html#cases'>SOP-B</a>. Mã chưa đạt <a href='chuan-san-pham.html#listing-criteria'>7 tiêu chí</a> → không bán."),
        ("Chủ quy trình", "<span class='r ops'>OPS</span> (control tower, đóng đơn). Chủ từng giai đoạn: xem <a href='#gates'>cổng qua</a>."),
        ("Duyệt / leo thang", "Đơn chuẩn không cần CEO. NCC trễ +5d → OPS. OPS duyệt lô (S5). Bồi thường theo <a href='sop-b-hau-mai.html#approval'>mức duyệt</a>."),
        ("SLA", "S1 ≤ 4h LV · S2 ≤ 24h · S3 ≤ hẹn +2d · S4 ≤ 2d · S5 1 ngày/tuần · S6 báo giữ ≤ 24h · khách được cập nhật mỗi 7 ngày."),
        ("Đầu vào", "Đơn đã thanh toán · thông số Master SKU · NCC chính + dự phòng · khung ETA theo thị trường."),
        ("Bằng chứng trước khi đổi trạng thái", "Email xác nhận · PO · ảnh kiện + vận đơn · ảnh QC · lượt quét thật · POD."),
        ("Cập nhật tracker", "Tab DON: nhập ngày ở cột 20 → 99 ngay khi có bằng chứng; ghi “Cập nhật KH gần nhất”."),
        ("Biểu mẫu", "<a href='{TRACKER}'>SOP-Tracker.xlsx</a> · <a href='{DOCS}'>Mẫu chứng từ NCC</a> · <a href='sop-b-hau-mai.html#templates'>Mẫu tin nhắn khách</a> · <a href='nha-cung-cap-qc.html#supplier-message'>Mẫu tin NCC</a>"),
        ("Ngoại lệ / bước tiếp", "<a href='#exits'>Lối thoát ngoại lệ</a> → <a href='sop-b-hau-mai.html#cases'>SOP-B C1–C8</a> · cờ SLA ở <a href='kpi-sla-nhip.html#flags'>KPI & SLA</a>."),
    ],
    "sop-b": [
        ("Dùng khi", "Khách báo vấn đề, cờ ETA bật, khách hủy hoặc đổi ý, có dispute thanh toán."),
        ("Không dùng khi", "Đơn đang chạy bình thường → <a href='sop-a-don-chuan.html'>SOP-A</a>. Câu hỏi chung → <a href='#faq'>FAQ</a>. Đổi chính sách → CEO."),
        ("Chủ quy trình", "<span class='r cx'>CX</span> mở và đóng case. <span class='r ops'>OPS</span> review nguyên nhân gốc thứ Sáu."),
        ("Duyệt / leo thang", "≤ A$50 <span class='r cx'>CX</span> · A$51–150 <span class='r ops'>OPS</span> · > A$150 hoặc hoàn 100% <span class='r ceo'>CEO</span> · chargeback <span class='r ops'>OPS</span>."),
        ("SLA", "Phản hồi ≤ 4h LV (hỏng/sai), ≤ 24h kênh khác · quyết định ≤ 24h sau đủ chứng cứ · gửi bù ≤ 5 ngày LV · hoàn ≤ 7 ngày LV · claim ≤ 48h · chargeback gọi ≤ 24h."),
        ("Đầu vào", "Mã đơn · loại case · bằng chứng của khách (nhãn kiện, ảnh lỗi, ảnh toàn món)."),
        ("Bằng chứng trước khi đổi trạng thái", "Bằng chứng khách · người duyệt đúng mức · xác nhận cổng thanh toán đã nhận lệnh hoàn · mã nguyên nhân gốc khi đóng."),
        ("Cập nhật tracker", "Tab CASE: một dòng/case; đóng case phải có mã RC."),
        ("Biểu mẫu", "<a href='#templates'>Mẫu tin nhắn tiếng Anh</a> · <a href='{TRACKER}'>SOP-Tracker.xlsx (CASE)</a> · <a href='#refund-steps'>Hoàn tiền 5 bước</a>"),
        ("Ngoại lệ / bước tiếp", "R3 đổi mới → <a href='sop-a-don-chuan.html#s2'>SOP-A từ S2</a> · lỗi lặp → <a href='#root-cause'>tắt SKU/NCC</a> · <a href='kpi-sla-nhip.html#weekly-report'>báo cáo tuần</a>."),
    ],
}

# ----------------------------------------------------------------------------- source of truth
SOT = {
    "order":    ("Trạng thái đơn, cờ SLA, ETA", "Source of Truth sheet · tab DON", "SHEET"),
    "case":     ("Case khách và người duyệt", "Source of Truth sheet · tab CASE", "SHEET"),
    "sku":      ("Thông số, kích thước, màu, chất liệu", "Source of Truth sheet · tab MASTER_SKU", "SHEET"),
    "supplier": ("Bằng chứng NCC, PO, ảnh QC", "Thư mục NCC / PO / QC trên Drive", "DOCS"),
    "shipment": ("Chứng từ lô hàng", "Thư mục lô hàng theo container", "DOCS"),
    "cost":     ("Landed cost thực, biên lãi", "File chi phí FIN · hạn chế quyền", "COST"),
    "promise":  ("Lời hứa với khách", "Customer-facing Policy + email xác nhận đơn", "chinh-sach-khach-hang.html"),
    "listing":  ("Nội dung trang sản phẩm", "Listing đã duyệt từ Master SKU", "chuan-san-pham.html#listing-criteria"),
}

# ----------------------------------------------------------------------------- launch blockers
BLOCKERS = {
    "gst": ("GST / thuế nhập khẩu", "Giá niêm yết đã gồm hay chưa gồm GST và thuế nhập khẩu: chờ chốt pháp nhân bán hàng và đăng ký GST.", "CEO", "lo-trinh-90-ngay.html#ceo-decisions"),
    "email": ("Email hỗ trợ", "Chưa có email hỗ trợ chính thức cho chính sách và website.", "CEO", "chinh-sach-khach-hang.html#customer-care"),
    "hours": ("Giờ chăm sóc khách", "Chưa chốt giờ làm việc (AEST) công bố cho khách.", "CEO · OPS", "chinh-sach-khach-hang.html#customer-care"),
    "legal": ("Luật sư Úc rà chính sách", "Chính sách giao hàng, đổi trả, hoàn tiền chưa được luật sư tại Úc (và Singapore) rà.", "CEO", "chinh-sach-khach-hang.html#legal-basis"),
    "broker": ("Đại lý hải quan Úc", "Chưa có đại lý hải quan xác nhận mã HS và điều kiện nhập khẩu cho từng mã trước lô đầu tiên.", "CEO · LOG", "dong-goi-chung-tu.html#au-rules"),
}

RHYTHM = [
    ("07:00", "Kiểm tra theo vị trí", "CX hộp thư · SRC tin NCC · LOG tracking lô", f"{K}#checklist"),
    ("09:00", "Control Tower", "15 phút. Mỗi cờ đỏ có tên người xử lý trong ngày", f"{K}#flags"),
    ("Trong ngày", "Đơn · NCC · logistics · khách", "S1 xác nhận · S2 PO · S5 chứng từ · cập nhật 7 ngày · case", f"{K}#checklist"),
    ("Thứ Sáu", "Đối soát · review case · báo cáo tuần", "FIN đối soát · OPS báo cáo → CEO", f"{K}#weekly-report"),
    ("Ngày 01", "Rà ETA · chính sách · lằn ranh đỏ", "Nới khung nếu 10% đơn chậm nhất vượt khung", f"{K}#rhythm"),
]
