#!/usr/bin/env python3
"""
normalize_catalog.py - Turn raw_products.json (from catalog_export.py) into a CLEAN product database:
  * 2-level category taxonomy (7 main categories + sub-categories), product codes
  * standardisation tier A/B/C with reasons (standard items first)
  * one colour standard (raw colour -> standard colour + family + material/finish)
  * one size standard (W x D x H in cm), one option-name standard (Color / Size / Material / Variant)
  * variant SKUs, image download into a clean folder tree

Usage
  python normalize_catalog.py --raw export_store/raw_products.json --out clean_db
  python normalize_catalog.py --raw export_store/raw_products.json --out clean_db --download-images A      # tier A only
  python normalize_catalog.py --raw ... --out clean_db --download-images AB --images-per-colour 6

Image tree:  clean_db/images/<Tier>/<MainCategory>/<SubCategory>/<PRODUCT_CODE>_<slug>/<ColourStd>/<NN>.jpg
Requires: Python 3.9+, requests (for images), openpyxl (for the review workbook)
"""
import argparse, csv, html, json, os, re, sys, time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

# =============================================================================== TAXONOMY
# (main category, code) -> [(sub category, code, regex on product_type/title)]
TAXONOMY = [
    ("Living Room", "LIV", [
        ("TV Units", "TVU", r"\btv\b|media console|entertainment unit|tv unit|tv stand|tv cabinet|floating console"),
        ("Coffee Tables", "COF", r"coffee table"),
        ("Side Tables", "SID", r"side table|end table|accent table|c[\s-]?table"),
        ("Sofas", "SOF", r"sofa|couch|sectional|chaise|loveseat"),
        ("Armchairs & Lounge Chairs", "ARM", r"armchair|lounge chair|accent chair|recliner|velvet chair|rattan.*chair|wooden chair"),
    ]),
    ("Dining & Kitchen", "DIN", [
        ("Dining Tables", "DTB", r"dining table|dining set|extendable table|round table|oval table"),
        ("Dining Chairs", "DCH", r"dining chair"),
        ("Bar Stools & Bar Tables", "BAR", r"bar stool|counter stool|bar table|bar chair"),
        ("Sideboards & Buffets", "SBD", r"sideboard|buffet|credenza|tea cabinet|tea station"),
        ("Wine & Display Cabinets", "WIN", r"wine|display cabinet|glass cabinet|curio"),
        ("Kitchen Islands", "KIS", r"kitchen island|\bisland\b"),
    ]),
    ("Bedroom", "BED", [
        ("Bed Frames", "BFR", r"bed\s?frame|bedframe|platform bed|\bbed\b|bunk|loft bed|daybed|sofa bed|bedroom set"),
        ("Bedside Tables", "BST", r"bedside|nightstand|night stand"),
        ("Chests & Dressers", "DRS", r"chest of drawers|drawer|dresser|tallboy|lowboy"),
        ("Wardrobes", "WRD", r"wardrobe|armoire|closet"),
    ]),
    ("Entryway & Storage", "STO", [
        ("Shoe Cabinets", "SHO", r"shoe"),
        ("Console & Hallway Tables", "CON", r"console table|hallway table|entryway table|entry table|console$"),
        ("Bookshelves & Shelving", "SHE", r"bookshelf|bookcase|shelf|shelving|display shelf|ladder"),
        ("Storage Cabinets", "CAB", r"storage cabinet|cabinet|cupboard|storage"),
        ("Benches", "BEN", r"bench|ottoman|pouf"),
    ]),
    ("Home Office", "OFF", [
        ("Desks", "DSK", r"desk|study table|writing table|computer table"),
        ("Office Chairs", "OCH", r"office chair|desk chair"),
    ]),
    ("Bathroom", "BTH", [
        ("Bathroom Vanities", "VAN", r"vanity|basin|sink"),
        ("Bathroom Cabinets", "BCB", r"bathroom cabinet|mirror cabinet"),
    ]),
    ("Decor & Lighting", "DEC", [
        ("Mirrors", "MIR", r"mirror"),
        ("Lighting", "LGT", r"lamp|light|pendant|chandelier"),
        ("Rugs", "RUG", r"\brug\b|carpet"),
        ("Wall Panels & Decor", "WAL", r"feature wall|wall panel|decor|art|vase"),
    ]),
    ("Outdoor", "OUT", [
        ("Outdoor Furniture", "ODF", r"outdoor|patio|garden"),
    ]),
]
NON_PRODUCT_RE = re.compile(r"add[\s-]?charge|extra charge|shipping fee|shipwill|deposit|top[\s-]?up|price difference|"
                            r"payment link|upgrade fee|insurance|gift card|test product|^design$", re.I)

# product_type -> forced sub-category code (cleans store inconsistencies like "Shoe Cabinets")
PTYPE_MAP = {
    "tv console": "TVU", "tv consoles": "TVU", "sofa": "SOF", "sofa beds": "BFR", "dining table": "DTB",
    "dining tables": "DTB", "dining set": "DTB", "bedframe": "BFR", "bed frames": "BFR", "sideboard": "SBD",
    "shoe cabinet": "SHO", "shoe cabinets": "SHO", "coffee table": "COF", "coffee tables": "COF",
    "chest of drawers": "DRS", "dining chair": "DCH", "dining chairs": "DCH", "wardrobe": "WRD",
    "bathroom vanity sink": "VAN", "vanity": "VAN", "bathroom cabinet": "BCB", "kitchen island": "KIS",
    "bookshelf": "SHE", "display shelf": "SHE", "shelf": "SHE", "console tables": "CON", "console table": "CON",
    "storage cabinet": "CAB", "cabinet": "CAB", "bedside table": "BST", "bench": "BEN",
    "outdoor furniture": "ODF", "wine cabinet": "WIN", "display cabinet": "WIN", "bar stool": "BAR",
    "bar table": "BAR", "stool": "BAR", "mirror": "MIR", "desk": "DSK", "lounge chair": "ARM",
    "lamp": "LGT", "side table": "SID", "side tables": "SID", "rug": "RUG",
}
SUB = {sc: (main, mc, sname) for main, mc, subs in TAXONOMY for sname, sc, _ in subs}


def classify(p):
    title = p.get("title", "") or ""
    pt = (p.get("product_type") or "").strip().lower()
    if NON_PRODUCT_RE.search(title) or NON_PRODUCT_RE.search(pt):
        return ("Excluded – Not a product", "XXX", "Fees & Payment Links", "FEE")
    if pt in PTYPE_MAP:
        sc = PTYPE_MAP[pt]
        # a few store types are too broad: refine from the title
        if sc in ("CAB", "SHE", "BAR"):
            for main, mc, subs in TAXONOMY:
                for sname, sc2, rx in subs:
                    if sc2 in ("SHO", "WIN", "SBD", "BST", "BCB", "TVU") and re.search(rx, title, re.I):
                        sc = sc2; break
        main, mc, sname = SUB[sc]
        return (main, mc, sname, sc)
    for main, mc, subs in TAXONOMY:          # fall back to title keywords (order matters)
        for sname, sc, rx in subs:
            if re.search(rx, title, re.I):
                return (main, mc, sname, sc)
    return ("Unclassified", "UNC", "Unclassified", "UNC")


# =============================================================================== COLOUR STANDARD
# Ordered rules: first match wins. (regex on lower-cased token, standard name, family, 3-letter code)
COLOUR_RULES = [
    (r"custom|customi[sz]e|as picture|other colou?r|contact|specify|in notes", "Custom (exclude)", "Custom", "CUS"),
    (r"^\s*\d{2,3}([\s-]+\d{2})*[\s-]*$|^\s*\d{2}\s+[a-z]", "Supplier code (unnamed)", "Coded", "COD"),
    (r"pandora|marble|terrazzo|calacatta|travertine|bulgari|italic|latin|\bjad\b|pattern|grain", "Stone Pattern", "Pattern", "STN"),
    (r"multi\s*-?colou?r|rainbow", "Multicolour", "Colour", "MLT"),
    (r"white\s*wash|white\s*oak|light\s*oak|bleach", "White Oak", "Wood", "WOK"),
    (r"black\s*(oak|wood|elm|ash)|ebony|charcoal\s*wood", "Black Oak", "Wood", "BOK"),
    (r"dark\s*walnut|black\s*walnut|espresso|dark\s*(wood|brown\s*wood|oak)|wenge|chocolate\s*wood", "Dark Walnut", "Wood", "DWL"),
    (r"walnut", "Walnut", "Wood", "WAL"),
    (r"cherry|red(dish)?\s*brown|mahogany|rosewood|sienna", "Cherry", "Wood", "CHR"),
    (r"warm\s*brown|honey|teak|golden\s*(oak|pine)|birch\s*brown|brown\s*(oak|ash|elm|wood|tulipwood)|chestnut|rubber\s*wood|camphor|acacia", "Warm Brown", "Wood", "WBR"),
    (r"natural|\boak\b|oak\s*(wood|colou?r)|light\s*wood|maple|marple|\bash\b|beech|pine|birch|original|log|wood\s*colou?r|raw\s*wood|tulipwood|bamboo|rattan|^wood$", "Natural Oak", "Wood", "NOK"),
    (r"black|ebony|jet|onyx|matt\s*black|matte\s*black|\bcoal\b", "Black", "Neutral", "BLK"),
    (r"off[\s-]?white|ivory|cream|vanilla|milk|eggshell|azel\s*white|warm\s*white", "Cream", "Neutral", "CRM"),
    (r"white|snow|glossy\s*white", "White", "Neutral", "WHT"),
    (r"light\s*gr[ae]y|silver\s*gr[ae]y|pale\s*gr[ae]y", "Light Grey", "Neutral", "LGR"),
    (r"dark\s*gr[ae]y|space\s*gr[ae]y|charcoal|graphite|slate|anthracite|smoky|smoke", "Dark Grey", "Neutral", "DGR"),
    (r"gr[ae]y", "Grey", "Neutral", "GRY"),
    (r"beige|begie|khaki|sand|linen|nude|taupe|oat|camel|stone|mushroom|latte|almond", "Beige", "Neutral", "BEG"),
    (r"coffee|brown|mocha|caramel|tan|cognac|chocolate", "Brown", "Neutral", "BRN"),
    (r"green|olive|sage|forest|emerald|moss", "Green", "Colour", "GRN"),
    (r"blue|bule|navy|ocean|teal", "Blue", "Colour", "BLU"),
    (r"pink|rose(?!\s*gold)|blush", "Pink", "Colour", "PNK"),
    (r"orange|terracotta|rust|burnt|squash", "Orange", "Colour", "ORG"),
    (r"yellow|mustard", "Yellow", "Colour", "YEL"),
    (r"red|burgundy|wine", "Red", "Colour", "RED"),
    (r"purple|lilac|lavender", "Purple", "Colour", "PUR"),
    (r"gold|brass|champagne|bronze|rose\s*gold|copper", "Gold", "Metal", "GLD"),
    (r"silver|chrome|stainless", "Silver", "Metal", "SLV"),
        (r"transparent|clear|glass", "Clear", "Neutral", "CLR"),
]
MATERIAL_WORDS = [
    (r"pu\s*leather|faux\s*leather|vegan\s*leather", "PU Leather"), (r"(?<!pu )(?<!faux )(?<!vegan )leather", "Leather"),
    (r"boucl", "Boucle"), (r"suede", "Suede"), (r"velvet", "Velvet"), (r"fabric|linen|cotton|fleece|teddy", "Fabric"), (r"laminate", "Laminate"),
    (r"sintered\s*stone|rock\s*plate|slate", "Sintered Stone"), (r"marble", "Marble"), (r"glass", "Glass"),
    (r"glossy|gloss", "Gloss"), (r"matte|matt\b", "Matte"), (r"antique", "Antique"), (r"smooth", "Smooth"),
    (r"cerused", "Cerused"), (r"rattan", "Rattan"),
]
CORE_PALETTE = {"Natural Oak", "Walnut", "Dark Walnut", "Black", "White", "Cream", "Beige", "Grey", "Light Grey", "Dark Grey"}


def is_core(colour_std):
    return bool(colour_std) and all(c.strip() in CORE_PALETTE for c in colour_std.split("/"))


SPLIT_RE = re.compile(r"\s*(?:&|\+|/|\band\b|\bwith\b|,)\s*", re.I)
_colour_cache = {}


def std_one(token):
    t = token.lower().strip()
    for rx, name, fam, code in COLOUR_RULES:
        if re.search(rx, t):
            return name, fam, code
    return None


def standardise_colour(raw):
    """raw 'Walnut & Black PU Leather' -> ('Walnut / Black', 'Two-tone', 'WAL-BLK', 'PU Leather', needs_review)"""
    if raw in _colour_cache:
        return _colour_cache[raw]
    r = (raw or "").strip()
    mats = [m for rx, m in MATERIAL_WORDS if re.search(rx, r, re.I)]
    base = r
    for rx, _ in MATERIAL_WORDS:
        base = re.sub(rx, " ", base, flags=re.I)
    base = re.sub(r"\b(colou?r|finish|full|wood|frame|top|base|smooth)\b", lambda m: m.group(0) if re.fullmatch(r"wood", m.group(0), re.I) else " ", base, flags=re.I)
    parts = [x for x in SPLIT_RE.split(base) if x.strip()]
    stds = []
    for part in parts or [r]:
        s = std_one(part) or std_one(r)
        if s and s not in stds:
            stds.append(s)
    if not r:
        res = ("", "", "", "", False)
    elif not stds:
        res = ("UNMAPPED", "Unmapped", "UNM", " ".join(mats), True)
    elif any(s[1] == "Custom" for s in stds):
        res = ("Custom (exclude)", "Custom", "CUS", " ".join(mats), False)
    elif len(stds) == 1:
        res = (stds[0][0], stds[0][1], stds[0][2], " ".join(mats), stds[0][1] == "Coded")
    else:
        stds = sorted(stds[:2], key=lambda s: (s[1] != "Wood", s[1] == "Metal", s[0]))
        coded = any(s[1] in ("Coded",) for s in stds)
        res = (f"{stds[0][0]} / {stds[1][0]}", "Two-tone", f"{stds[0][2]}-{stds[1][2]}", " ".join(mats), coded)
    _colour_cache[raw] = res
    return res


# =============================================================================== OPTIONS & SIZE
def option_role(name):
    n = (name or "").strip().lower().rstrip(" :")
    if re.search(r"colou?rs?|finish|base colou?r|frame colou?r|colou?r & material", n):
        return "Color"
    if re.search(r"^sizes?$|dimension|height|length|width|table thickness", n):
        return "Size"
    if re.search(r"material|wood|fabric|table top|top$|frame$|mirror", n):
        return "Material"
    if n == "title":
        return "Single"
    return "Variant"           # configuration / design / type / other / option ... (non-standard)


_N = r"(?<![A-WYZa-wyz])([LWHD])?\s*(\d{1,4}(?:\.\d+)?)\s*(?:cm|mm)?\s*([LWHD](?![a-wyz]))?"
DIM_RE = re.compile(_N + r"\s*[*x×X]\s*" + _N + r"(?:\s*[*x×X]\s*" + _N + r")?\s*(cm|mm|m\b)?", re.I)
FLAT_SUBS = {"MIR", "WAL"}          # wall items: 2 untagged values = W x H
SINGLE_RE = re.compile(r"(?<![A-Za-z])([LWHD])?\s*(\d{2,4}(?:\.\d+)?)\s*(cm|mm)\b\s*([LWHD](?![a-wyz]))?", re.I)
BED_RE = re.compile(r"\b(single|double|queen|king|bed)\b", re.I)


def _to_cm(vals, unit, text):
    nums = [x for x in vals if x is not None]
    if unit == "mm":
        return [x / 10 if x is not None else None for x in vals]
    # unit missing/cm but values look like mm (e.g. "1200L x 600W x 680H")
    if not re.search(r"cm", text, re.I) and nums and max(nums) > 400:
        return [x / 10 if x is not None else None for x in vals]
    return vals


def _best_match(v):
    """Pick the dimension group with most numbers (skips e.g. '(3x2)' drawer layouts)."""
    best = None
    for m in DIM_RE.finditer(v):
        g = m.groups()
        n = sum(1 for i in range(3) if g[i * 3 + 1])
        tagged = sum(1 for i in range(3) if g[i * 3] or g[i * 3 + 2])
        key = (n, tagged)
        if best is None or key > best[0]:
            best = (key, m)
    return best[1] if best else None


def parse_size(value, sub=None):
    """Return (W, D, H) in cm.
    Store convention L x W x H  ->  W(idth) x D(epth) x H(eight).
    Letter tags (prefix 'L120' or suffix '120L') are honoured: L->W, W->D if L present else W, D->D, H->H.
    Untagged values: positional (W, D, H). Units: cm/mm anywhere in string; >400 without 'cm' => mm."""
    v = str(value or "")
    m = _best_match(v)
    if m:
        g = m.groups()
        items = []
        for i in range(3):
            pre, num, suf = g[i * 3], g[i * 3 + 1], g[i * 3 + 2]
            if num is None:
                continue
            tag = (pre or suf or "").upper() or None
            items.append((tag, float(num)))
        unit = (g[9] or ("mm" if re.search(r"\d\s*mm\b", v, re.I) else "cm")).lower()
        tags = [t for t, _ in items]
        W = D = H = None
        if any(tags):
            has_l = "L" in tags
            pos = 0
            for t, x in items:
                if t == "L":
                    W = x
                elif t == "W":
                    if has_l:
                        D = x
                    else:
                        W = x
                elif t == "D":
                    D = x
                elif t == "H":
                    H = x
                else:  # untagged among tagged -> fill first free slot
                    if W is None:
                        W = x
                    elif D is None:
                        D = x
                    else:
                        H = x
        else:
            xs = [x for _, x in items]
            W = xs[0]
            D = xs[1] if len(xs) > 1 else None
            H = xs[2] if len(xs) > 2 else None
            if sub in FLAT_SUBS and len(xs) == 2:
                D, H = None, xs[1]
        if unit == "m":
            return tuple(x * 100 if x is not None else None for x in (W, D, H))
        W, D, H = _to_cm([W, D, H], unit, v)
        return (W, D, H)
    m = SINGLE_RE.search(v)
    if m:
        tag = (m.group(1) or m.group(4) or "").upper()
        x = float(m.group(2)) / (10 if m.group(3).lower() == "mm" else 1)
        if tag == "H":
            return (None, None, x)
        if tag == "D":
            return (None, x, None)
        return (x, None, None)
    m = re.search(r"(?<![A-Za-z0-9])(?:(D|Ø|Dia\.?)\s?(\d{2,3})|(\d{2,3})\s?(L|W)\b|(L|W)\s?(\d{2,3}))(?![\d.])", v)
    if m:   # "D80" (round: diameter) / "70L" / "W120" without unit
        if m.group(1):
            x = float(m.group(2)); return (x, x, None)
        x = float(m.group(3) or m.group(6)); return (x, None, None)
    return (None, None, None)


def size_label(w, d, h):
    parts = [f"W{w:g}" if w else "", f"D{d:g}" if d else "", f"H{h:g}" if h else ""]
    parts = [p for p in parts if p]
    return (" × ".join(parts) + " cm") if parts else ""


# =============================================================================== SCREENING
FRAGILE_RE = re.compile(r"marble|sintered stone|slate|glass|mirror|ceramic|travertine|terrazzo|rock ?plate|stone top", re.I)
MTO_RE = re.compile(r"made[\s-]?to[\s-]?order|custom(?:i[sz]ed|i[sz]able)?\s+(size|sizing|dimension|length|width|colou?r|order)|"
                    r"bespoke|tailor[\s-]?made|personali[sz]ed|定制", re.I)
INSTALL_RE = re.compile(r"wall installation|wall[\s-]?mount|professional install|installation required|requires? install", re.I)
BOILER_RE = re.compile(r"(for more information or custom designs[^\n]*|feel free to chat with us[^\n]*|elevate your space[^\n]*)", re.I)


def html_to_text(s):
    s = re.sub(r"<\s*(br|/p|/li|/h\d|/div|/tr)\s*/?>", "\n", s or "", flags=re.I)
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    s = re.sub("[\U0001F000-\U0001FAFF☀-➿️‍]", "", s)
    return "\n".join(ln.strip() for ln in s.splitlines() if ln.strip())


def screen(p, cls, var_info, text_nb):
    """Return (tier, score, reasons). var_info: list of dicts with colour_family, roles."""
    if cls[3] == "FEE":
        return "C-EXCLUDE", 0, ["Not a product (fee/payment link)"]
    hard, soft, score = [], [], 100
    title = p.get("title", "")
    nvar = len(p.get("variants", []))
    roles = {o["role"] for o in var_info["options"]}
    prices = [float(v["price"]) for v in p.get("variants", []) if v.get("price")]
    if MTO_RE.search(title + "\n" + text_nb):
        hard.append("Made-to-order / custom")
    if var_info["has_custom_colour"] or var_info["has_custom_value"]:
        hard.append("Custom colour/size option")
    if cls[3] == "BFR":
        hard.append("Bed: size depends on mattress standard")
    if cls[3] == "SOF" and ("Variant" in roles or "Material" in roles or nvar > 8):
        hard.append("Sofa: configuration/fabric options")
    if nvar > 36:
        hard.append(f"Too many variants ({nvar})")
    if not p.get("images"):
        hard.append("No images")
    if cls[3] in ("UNC",):
        hard.append("Unclassified product")
    if "Variant" in roles:
        soft.append("Non-standard option (configuration/design/type)"); score -= 15
    if nvar > 18:
        soft.append(f"Many variants ({nvar})"); score -= 10
    if prices and min(prices) > 0 and max(prices) / min(prices) > 3:
        soft.append("Price range > 3x"); score -= 10
    if FRAGILE_RE.search(title + "\n" + text_nb):
        soft.append("Fragile (stone/glass/mirror)"); score -= 25
    if INSTALL_RE.search(text_nb):
        soft.append("Wall / professional installation"); score -= 15
    if var_info["unmapped_colour"]:
        soft.append("Colour unnamed/coded or unmapped"); score -= 15
    if var_info["size_parsed_ratio"] < 0.5:
        soft.append("Size not parsable"); score -= 10
    if cls[3] in ("SOF", "VAN", "ODF", "LGT", "RUG", "MIR", "WAL"):
        soft.append("Category outside launch focus"); score -= 10
    score = max(score, 0)
    tier = "C-EXCLUDE" if hard else ("A-STANDARD" if score >= 80 else "B-REVIEW")
    return tier, score, hard + soft


# =============================================================================== MAIN
def slug(s, n=40):
    return (re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-") or "na")[:n]


STORE_URL = ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raw", required=True, help="raw_products.json from catalog_export.py")
    ap.add_argument("--collections", help="raw_collections.json (optional)")
    ap.add_argument("--out", default="clean_db")
    ap.add_argument("--download-images", default="", help="tiers to download, e.g. A or AB or ABC (empty = none)")
    ap.add_argument("--images-per-colour", type=int, default=8)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--store-url", default="", help="base URL of the source store, used for source_url column (optional)")
    a = ap.parse_args()
    global STORE_URL
    STORE_URL = a.store_url

    P = json.loads(Path(a.raw).read_text(encoding="utf-8"))
    cpath = Path(a.collections) if a.collections else Path(a.raw).with_name("raw_collections.json")
    colls = json.loads(cpath.read_text(encoding="utf-8")) if cpath.exists() else {}
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

    products, variants, images, colour_counter = [], [], [], Counter()
    colour_examples = defaultdict(set)
    for p in P:
        cls = classify(p)
        text = html_to_text(p.get("body_html", ""))
        text_nb = BOILER_RE.sub("", text)
        opts = []
        for i, o in enumerate(p.get("options", []) or []):
            opts.append({"pos": i + 1, "name": o["name"], "role": option_role(o["name"]), "values": o.get("values", [])})
        col_opt = next((o for o in opts if o["role"] == "Color"), None)
        size_opt = next((o for o in opts if o["role"] == "Size"), None)
        has_custom_value = any(re.search(r"custom|bespoke|other size|special size|定制", str(v), re.I)
                               for o in opts for v in o["values"])
        vrows = []
        for v in p.get("variants", []):
            vals = {o["role"]: v.get(f'option{o["pos"]}') for o in opts}
            raw_col = vals.get("Color") or ""
            c_std, c_fam, c_code, c_mat, c_rev = standardise_colour(raw_col) if raw_col else ("", "", "", "", False)
            if raw_col:
                colour_counter[raw_col] += 1
                colour_examples[raw_col].add(p["title"][:40])
            size_src = vals.get("Size") or next((x for x in vals.values() if x and any(parse_size(x, cls[3]))), "")
            w, d, h = parse_size(size_src, cls[3])
            size_chk = ""
            if size_src and re.search(r"\d\s*(cm|mm|[x×*])", str(size_src), re.I) and not any((w, d, h)):
                size_chk = "UNPARSED"
            elif any(x is not None and (x > 450 or x < 5) for x in (w, d, h)) and cls[3] != "RUG":
                size_chk = "CHECK_VALUE"
            vrows.append({"v": v, "vals": vals, "raw_col": raw_col, "c_std": c_std, "c_fam": c_fam, "c_code": c_code,
                          "c_mat": c_mat, "c_rev": c_rev, "size_raw": size_src, "w": w, "d": d, "h": h, "size_chk": size_chk})
        var_info = {"options": opts,
                    "has_custom_colour": any(r["c_fam"] == "Custom" for r in vrows),
                    "has_custom_value": has_custom_value,
                    "unmapped_colour": any(r["c_rev"] for r in vrows),
                    "size_parsed_ratio": (sum(1 for r in vrows if any((r["w"], r["d"], r["h"]))) / len(vrows)) if (size_opt and vrows) else 1.0}
        tier, score, reasons = screen(p, cls, var_info, text_nb)
        products.append({"p": p, "cls": cls, "tier": tier, "score": score, "reasons": reasons, "opts": opts,
                         "vrows": vrows, "text": text_nb})

    # product codes: ordered by tier -> main -> sub -> score (standard items first)
    order = {"A-STANDARD": 0, "B-REVIEW": 1, "C-EXCLUDE": 2}
    products.sort(key=lambda x: (order[x["tier"]], x["cls"][1], x["cls"][3], -x["score"], x["p"]["title"]))
    seq = Counter()
    prod_rows, var_rows, img_rows, downloads = [], [], [], []
    for x in products:
        p, cls = x["p"], x["cls"]
        seq[cls[3]] += 1
        code = f"{cls[1]}-{cls[3]}-{seq[cls[3]]:04d}"
        x["code"] = code
        colours_std = sorted({r["c_std"] for r in x["vrows"] if r["c_std"]})
        core_share = (sum(1 for r in x["vrows"] if r["c_std"] and is_core(r["c_std"])) / max(1, sum(1 for r in x["vrows"] if r["c_std"]))) if colours_std else 1
        widths = sorted({r["w"] for r in x["vrows"] if r["w"]})
        prices = [float(r["v"]["price"]) for r in x["vrows"] if r["v"].get("price")]
        prod_rows.append({
            "product_code": code, "tier": x["tier"], "standard_score": x["score"], "reasons": "; ".join(x["reasons"]),
            "main_category": cls[0], "sub_category": cls[2], "source_title": p.get("title", ""), "source_handle": p["handle"],
            "source_product_type": p.get("product_type") or "", "source_collections": " | ".join(colls.get(p["handle"], [])),
            "option_structure": " × ".join(f'{o["role"]}({o["name"].strip()})' for o in x["opts"]),
            "variant_count": len(x["vrows"]), "colours_std": " | ".join(colours_std),
            "core_palette_share": round(core_share, 2),
            "widths_cm": " | ".join(f"{w:g}" for w in widths),
            "price_min_AUD": min(prices) if prices else "", "price_max_AUD": max(prices) if prices else "",
            "image_count": len(p.get("images", [])), "description_clean": x["text"],
            "source_url": (STORE_URL.rstrip('/') + '/products/' + p["handle"]) if STORE_URL else p["handle"],
        })
        # variants
        for r in x["vrows"]:
            v = r["v"]
            other = " / ".join(str(val) for role, val in r["vals"].items() if role not in ("Color", "Size", "Single") and val)
            sku = "-".join(s for s in [code, r["c_code"] or "", f'{int(r["w"])}' if r["w"] else ""] if s)
            var_rows.append({
                "variant_sku": sku, "product_code": code, "tier": x["tier"], "main_category": cls[0], "sub_category": cls[2],
                "colour_raw": r["raw_col"], "colour_std": r["c_std"], "colour_family": r["c_fam"], "colour_code": r["c_code"],
                "material_finish": r["c_mat"], "core_palette": ("YES" if is_core(r["c_std"]) else ("NO" if r["c_std"] else "")),
                "size_raw": r["size_raw"], "W_cm": r["w"], "D_cm": r["d"], "H_cm": r["h"],
                "size_std": size_label(r["w"], r["d"], r["h"]), "size_check": r["size_chk"], "other_option": other,
                "price_AUD": v.get("price"), "source_variant_id": v.get("id"),
                "variant_image_src": (v.get("featured_image") or {}).get("src", ""),
            })
        # de-duplicate SKUs inside a product (e.g. same colour+width but other option differs)
        seen = Counter(r["variant_sku"] for r in var_rows if r["product_code"] == code)
        idx = Counter()
        for r in var_rows:
            if r["product_code"] == code and seen[r["variant_sku"]] > 1:
                idx[r["variant_sku"]] += 1
                r["variant_sku"] = f'{r["variant_sku"]}-{idx[r["variant_sku"]]}'
        # images: assign standard colour folder
        col_vals = {r["raw_col"]: r["c_std"] for r in x["vrows"] if r["raw_col"]}
        img_col = {}
        for r in x["vrows"]:
            fi = r["v"].get("featured_image")
            if fi and fi.get("id"):
                img_col.setdefault(fi["id"], r["c_std"])
        per_col = Counter()
        for im in p.get("images", []):
            c = img_col.get(im.get("id"), "")
            if not c:
                hay = re.sub(r"[_\-]+", " ", (os.path.basename(urlparse(im["src"]).path) + " " + (im.get("alt") or "")).lower())
                for raw, std in sorted(col_vals.items(), key=lambda kv: -len(kv[0])):
                    if raw.lower() in hay:
                        c = std; break
            folder = slug(c or "General", 30)
            per_col[folder] += 1
            ext = os.path.splitext(urlparse(im["src"]).path)[1] or ".jpg"
            rel = Path("images") / x["tier"] / slug(cls[0], 30) / slug(cls[2], 30) / f"{code}_{slug(p['title'], 30)}" / folder / f"{per_col[folder]:02d}{ext}"
            img_rows.append({"product_code": code, "tier": x["tier"], "colour_std": c or "General", "position": im.get("position"),
                             "src": im["src"], "local_path": str(rel)})
            if a.download_images and x["tier"][0] in a.download_images.upper() and per_col[folder] <= a.images_per_colour:
                downloads.append((im["src"], out / rel))

    # colour map table
    cmap = []
    for raw, n in colour_counter.most_common():
        s = standardise_colour(raw)
        cmap.append({"colour_raw": raw, "variants": n, "colour_std": s[0], "colour_family": s[1], "colour_code": s[2],
                     "core_palette": "YES" if is_core(s[0]) else "NO",
                     "material_finish": s[3], "needs_review": "YES" if s[4] else "", "example_products": " | ".join(sorted(colour_examples[raw])[:3])})

    # category table
    cat_rows = []
    cnt = defaultdict(Counter)
    for r in prod_rows:
        cnt[(r["main_category"], r["sub_category"])][r["tier"]] += 1
    for main, mc, subs in TAXONOMY + [("Excluded – Not a product", "XXX", [("Fees & Payment Links", "FEE", "")]),
                                      ("Unclassified", "UNC", [("Unclassified", "UNC", "")])]:
        for sname, sc, _ in subs:
            c = cnt.get((main, sname), Counter())
            if sum(c.values()) or main not in ("Unclassified",):
                cat_rows.append({"main_category": main, "main_code": mc, "sub_category": sname, "sub_code": sc,
                                 "products": sum(c.values()), "A-STANDARD": c["A-STANDARD"], "B-REVIEW": c["B-REVIEW"],
                                 "C-EXCLUDE": c["C-EXCLUDE"]})

    def write_csv(name, rows):
        keys = list(dict.fromkeys(k for r in rows for k in r))
        with open(out / name, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
        print(f"  {name}: {len(rows)} rows")

    write_csv("01_categories.csv", cat_rows)
    write_csv("02_products.csv", prod_rows)
    write_csv("03_variants.csv", var_rows)
    write_csv("04_colour_map.csv", cmap)
    write_csv("05_images.csv", img_rows)

    # review workbook
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment
        wb = Workbook()
        hdr = dict(font=Font(bold=True, color="FFFFFF", name="Arial", size=10), fill=PatternFill("solid", fgColor="1F3864"))
        tier_fill = {"A-STANDARD": "E2EFDA", "B-REVIEW": "FFF2CC", "C-EXCLUDE": "F8CBAD"}

        def sheet(title, rows, widths, first=False, tier_col=None):
            ws = wb.active if first else wb.create_sheet()
            ws.title = title
            keys = list(rows[0].keys())
            ws.append(keys)
            for c in ws[1]:
                c.font = hdr["font"]; c.fill = hdr["fill"]; c.alignment = Alignment(wrap_text=True, vertical="center")
            for r in rows:
                ws.append([r[k] for k in keys])
            if tier_col:
                ti = keys.index(tier_col) + 1
                for row in ws.iter_rows(min_row=2):
                    f = tier_fill.get(row[ti - 1].value)
                    if f:
                        row[ti - 1].fill = PatternFill("solid", fgColor=f)
            for i, w in enumerate(widths, 1):
                ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = w
            ws.freeze_panes = "B2"; ws.auto_filter.ref = ws.dimensions
            return ws

        sheet("Categories", cat_rows, [24, 8, 28, 8, 9, 11, 10, 10], first=True)
        prod_view = [{k: r[k] for k in ["product_code", "tier", "standard_score", "main_category", "sub_category", "source_title",
                                        "variant_count", "colours_std", "core_palette_share", "widths_cm", "price_min_AUD", "price_max_AUD",
                                        "option_structure", "reasons", "source_url"]} for r in prod_rows]
        sheet("Products", prod_view, [16, 12, 8, 18, 22, 40, 8, 30, 9, 22, 9, 9, 34, 50, 40], tier_col="tier")
        var_view = [{k: r[k] for k in ["variant_sku", "product_code", "tier", "sub_category", "colour_raw", "colour_std",
                                       "colour_family", "material_finish", "core_palette", "size_raw", "size_std", "size_check", "other_option", "price_AUD"]}
                    for r in var_rows]
        sheet("Variants", var_view, [26, 16, 12, 20, 24, 18, 12, 14, 9, 26, 24, 20, 9], tier_col="tier")
        sheet("Colour_Map", cmap, [30, 9, 22, 12, 10, 9, 16, 12, 60])
        g = wb.create_sheet("Colour_Standard")
        g.append(["colour_std", "family", "code", "rule (raw words that map here)"])
        for c in g[1]:
            c.font = hdr["font"]; c.fill = hdr["fill"]
        for rx, name, fam, code in COLOUR_RULES:
            g.append([name, fam, code, rx])
        g.column_dimensions["A"].width = 18; g.column_dimensions["D"].width = 90
        wb.save(out / "clean_catalogue_review.xlsx")
        print("  clean_catalogue_review.xlsx")
    except ImportError:
        print("  (openpyxl not installed: workbook skipped)")

    # images
    if downloads:
        import requests
        sess = requests.Session(); sess.headers["User-Agent"] = "Mozilla/5.0 (catalog-normalize; internal reference)"
        print(f"Downloading {len(downloads)} images ...")

        def dl(item):
            src, dest = item
            if dest.exists() and dest.stat().st_size > 0:
                return "skip"
            dest.parent.mkdir(parents=True, exist_ok=True)
            for k in range(3):
                try:
                    r = sess.get(src, timeout=60); r.raise_for_status(); dest.write_bytes(r.content); return "ok"
                except Exception:
                    time.sleep(2 * (k + 1))
            return "fail"

        with ThreadPoolExecutor(max_workers=max(1, min(a.workers, 8))) as ex:
            res = list(ex.map(dl, downloads))
        print(f"  images ok={res.count('ok')} skipped={res.count('skip')} failed={res.count('fail')}")

    t = Counter(r["tier"] for r in prod_rows)
    print(f"Products {len(prod_rows)} | A={t['A-STANDARD']} B={t['B-REVIEW']} C={t['C-EXCLUDE']} | variants {len(var_rows)} | "
          f"colour values {len(cmap)} (needs review: {sum(1 for c in cmap if c['needs_review'])})")


if __name__ == "__main__":
    main()
