#!/usr/bin/env python3
"""
catalog_export.py  v2 - Full export of a Shopify storefront catalogue (products, variants,
specs, collections, images) + completeness check + "standardisation" screening.

Purpose: export a Shopify store catalogue you own or are authorised to use, as INTERNAL REFERENCE,
then cross-check against Taobao/1688 suppliers. Before re-using anything publicly:
  * Rewrite titles/descriptions (no old brand names / copied marketing copy).
  * Verify material claims with the supplier (old listings contain wrong claims).
  * Do NOT use compare_at_price as a "was" price (ACCC was/now rules).
  * Confirm image rights (many images originate from suppliers).

Typical run (data first, then images for a shortlist):
  python catalog_export.py --store https://your-store.example --out export_store --images none
  python catalog_export.py --from-json export_store/raw_products.json --out export_store \
         --handles shortlist.txt --images variant
  python catalog_export.py --from-json export_store/raw_products.json --out export_store --images all

Outputs (in --out): raw_products.json, products.csv, variants.csv, images.csv, collections.csv,
sku_master_draft.csv, completeness_report.txt, catalogue_review.xlsx (if openpyxl installed), images/...

Requires: Python 3.9+, pip install requests   (optional: pip install openpyxl)
"""
import argparse, csv, html, json, os, random, re, sys, time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    sys.exit("Please install requests:  pip install requests")

UA = {"User-Agent": "Mozilla/5.0 (catalog-export; internal reference)"}
PAGE_LIMIT = 250
SESSION = requests.Session()
SESSION.headers.update(UA)


# ============================================================================ HTTP helpers
def get(url, *, as_json=False, tries=4, timeout=30, method="GET"):
    for attempt in range(tries):
        try:
            r = SESSION.request(method, url, timeout=timeout)
            if r.status_code == 429:
                time.sleep(5 * (attempt + 1)); continue
            if r.status_code == 404:
                return None
            r.raise_for_status()
            return r.json() if as_json else r
        except requests.RequestException:
            if attempt == tries - 1:
                raise
            time.sleep(3 * (attempt + 1))
    return None


def paged_products(base_url, sleep):
    out, page = [], 1
    while True:
        j = get(f"{base_url}?limit={PAGE_LIMIT}&page={page}", as_json=True) or {}
        batch = j.get("products", [])
        if not batch:
            break
        out.extend(batch)
        page += 1
        time.sleep(sleep)
    return out


def fetch_all_products(store, sleep, max_products=0):
    products = []
    page = 1
    while True:
        j = get(f"{store}/products.json?limit={PAGE_LIMIT}&page={page}", as_json=True) or {}
        batch = j.get("products", [])
        if not batch:
            break
        products.extend(batch)
        print(f"  products page {page}: +{len(batch)} (total {len(products)})")
        if max_products and len(products) >= max_products:
            return products[:max_products]
        page += 1
        time.sleep(sleep)
    return products


def sitemap_product_handles(store):
    """All product URLs listed in the sitemap (used to prove completeness)."""
    handles = set()
    root = get(f"{store}/sitemap.xml")
    if root is None:
        return handles
    for loc in re.findall(r"<loc>([^<]+)</loc>", root.text):
        loc = html.unescape(loc)
        if "sitemap_products" not in loc:
            continue
        sm = get(loc)
        if sm is None:
            continue
        for u in re.findall(r"<loc>([^<]+)</loc>", sm.text):
            m = re.search(r"/products/([^/?#<]+)", html.unescape(u))
            if m:
                handles.add(m.group(1))
    return handles


def fetch_product_js(store, handle):
    """Single product via /products/<handle>.js (fallback for products missing from products.json)."""
    j = get(f"{store}/products/{handle}.js", as_json=True)
    if not j:
        return None
    # normalise .js shape (prices in cents, images as URLs) to products.json shape
    imgs = [{"id": i + 1, "position": i + 1, "src": ("https:" + u if u.startswith("//") else u),
             "variant_ids": [], "width": None, "height": None, "alt": ""} for i, u in enumerate(j.get("images", []))]
    variants = []
    for v in j.get("variants", []):
        fi = v.get("featured_image")
        variants.append({"id": v["id"], "title": v.get("title"), "option1": v.get("option1"),
                         "option2": v.get("option2"), "option3": v.get("option3"),
                         "price": f'{(v.get("price") or 0)/100:.2f}',
                         "compare_at_price": f'{v["compare_at_price"]/100:.2f}' if v.get("compare_at_price") else None,
                         "available": v.get("available"), "grams": v.get("weight"), "sku": v.get("sku"),
                         "featured_image": ({"id": fi.get("id"), "position": fi.get("position"), "src": fi.get("src")} if fi else None)})
    return {"id": j["id"], "title": j["title"], "handle": j["handle"], "body_html": j.get("description", ""),
            "vendor": j.get("vendor"), "product_type": j.get("type"), "tags": j.get("tags", []),
            "created_at": j.get("created_at"), "published_at": j.get("published_at"),
            "options": [{"name": o["name"], "position": o.get("position"), "values": o.get("values", [])}
                        for o in j.get("options", [])],
            "variants": variants, "images": imgs, "_source": "products.js"}


# ============================================================================ parsing
TAG_RE = re.compile(r"<[^>]+>")
EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF☀-➿️‍]")
_N = r"[LWHD]?\s*(\d{2,4}(?:\.\d)?)\s*(?:cm|mm)?\s*[LWHD]?"
DIM_RE = re.compile(_N + r"\s*[*x×X]\s*" + _N + r"(?:\s*[*x×X]\s*" + _N + r")?\s*(cm|mm)?", re.I)
WIDTH_ONLY_RE = re.compile(r"(\d{2,4}(?:\.\d)?)\s*(cm|mm)\b", re.I)


def parse_dims(value):
    """'L140 x W70 x H75' / '120L x 40W x 50H cm' / '160 cm' -> (L, W, H) in cm (None if absent)."""
    v = str(value or "")
    m = DIM_RE.search(v)
    if m:
        unit = (m.group(4) or ("mm" if re.search(r"\bmm\b", v, re.I) else "cm")).lower()
        nums = [float(x) for x in m.groups()[:3] if x]
        if unit == "mm":
            nums = [n / 10 for n in nums]
        nums += [None] * (3 - len(nums))
        return tuple(nums)
    m = WIDTH_ONLY_RE.search(v)
    if m:
        n = float(m.group(1)) / (10 if m.group(2).lower() == "mm" else 1)
        return (n, None, None)
    return (None, None, None)
MATERIAL_RE = re.compile(r"(?:MATERIALS?|Material)\s*[:\-]?\s*([^\n]{2,160})", re.I)
BOILERPLATE_RE = re.compile(r"(for more information or custom designs[^\n]*|feel free to chat with us[^\n]*|"
                            r"elevate your space[^\n]*)", re.I)

CATS = [("TV Console", r"\btv\b|media console|entertainment unit|tv unit|tv stand"),
        ("Shoe Cabinet", r"shoe"), ("Coffee Table", r"coffee table"),
        ("Bedside Table", r"bedside|nightstand"), ("Side Table", r"side table|end table"),
        ("Console Table", r"console table|hallway table|entryway table"),
        ("Dining Table", r"dining table"), ("Dining Chair", r"dining chair"),
        ("Chair / Stool", r"chair|stool|armchair"), ("Bed Frame", r"bed frame|bedframe|\bbed\b|bunk"),
        ("Sofa", r"sofa|couch|lounge|sectional|chaise"), ("Sideboard / Buffet", r"sideboard|buffet|credenza"),
        ("Bookshelf / Shelf", r"shelf|bookcase|bookshelf|display|shelving"), ("Wardrobe", r"wardrobe|armoire"),
        ("Chest of Drawers", r"drawer|dresser|chest"), ("Desk", r"desk"), ("Kitchen Island", r"island"),
        ("Bathroom Vanity", r"vanity"), ("Storage Cabinet", r"cabinet|cupboard|storage"),
        ("Lighting", r"lamp|light|pendant"), ("Mirror", r"mirror"), ("Rug", r"\brug\b|carpet"),
        ("Feature Wall", r"feature wall|wall panel"), ("Outdoor", r"outdoor")]

NON_PRODUCT_RE = re.compile(r"add[\s-]?charge|extra charge|shipping fee|deposit|top[\s-]?up|price difference|"
                            r"payment link|custom order|upgrade fee|insurance|gift card|test product", re.I)
MADE_TO_ORDER_RE = re.compile(r"made[\s-]?to[\s-]?order|custom(?:i[sz]ed|i[sz]able)?\s+(size|sizing|dimension|length|width|colour|color|order)|"
                              r"bespoke|tailor[\s-]?made|personali[sz]ed|定制|please (?:contact|chat) us for (?:custom|size)", re.I)
FRAGILE_RE = re.compile(r"marble|sintered stone|slate|glass|mirror|ceramic|travertine|terrazzo|rock ?plate|stone top", re.I)
INSTALL_RE = re.compile(r"wall installation|wall[\s-]?mount|professional install|installation required|requires? install", re.I)
ASSEMBLY_RE = re.compile(r"assembly required|self[\s-]?assembl|easy assembl|requires? assembl", re.I)
FULLY_ASSEMBLED_RE = re.compile(r"fully assembled|no assembly", re.I)
SOLID_CLAIM_RE = re.compile(r"solid\s+(oak|wood|timber|walnut|ash|pine|rubber ?wood|teak|acacia|eucalyptus|beech)", re.I)
SERVICE_OPTION_RE = re.compile(r"install|assembl|white glove|room of choice|delivery|service", re.I)
CUSTOM_OPTION_RE = re.compile(r"custom|bespoke|other size|special size|定制", re.I)


def html_to_text(s):
    s = re.sub(r"<\s*(br|/p|/li|/h\d|/div|/tr)\s*/?>", "\n", s or "", flags=re.I)
    s = html.unescape(TAG_RE.sub("", s))
    s = EMOJI_RE.sub("", s)
    lines = [re.sub(r"[ \t ]+", " ", ln).strip() for ln in s.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def guess_category(title, ptype):
    for name, pat in CATS:
        if re.search(pat, title or "", re.I):
            return name
    return ptype or ""


def infer_color(im, color_vals):
    hay = (os.path.basename(urlparse(im.get("src", "")).path) + " " + (im.get("alt") or "")).lower()
    hay = re.sub(r"[_\-]+", " ", hay)
    for c in sorted([c for c in color_vals if c], key=len, reverse=True):
        if c.lower() in hay:
            return c
    return ""


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-") or "na"


def screen_product(p, text):
    """Standardisation screening: returns (score 0-100, flags list, eligible bool)."""
    flags = []
    title = p.get("title", "")
    text_nb = BOILERPLATE_RE.sub("", text)          # ignore store-wide boilerplate ("custom designs" etc.)
    opts = p.get("options", [])
    vals = [str(v) for o in opts for v in o.get("values", [])]
    nvar = len(p.get("variants", []))
    prices = [float(v["price"]) for v in p.get("variants", []) if v.get("price")]
    score = 100

    if NON_PRODUCT_RE.search(title) or (prices and max(prices) < 5):
        return 0, ["NOT_A_PRODUCT (fee/payment link)"], "C-EXCLUDE"
    if MADE_TO_ORDER_RE.search(title + "\n" + text_nb):
        flags.append("MADE_TO_ORDER/CUSTOM"); score -= 45
    if any(CUSTOM_OPTION_RE.search(v) for v in vals) or any(CUSTOM_OPTION_RE.search(o["name"]) for o in opts):
        flags.append("CUSTOM_OPTION_VALUE"); score -= 35
    if any(SERVICE_OPTION_RE.search(o["name"]) or any(SERVICE_OPTION_RE.search(v) for v in o.get("values", [])) for o in opts):
        flags.append("SERVICE_IN_VARIANTS (install/delivery)"); score -= 15
    if nvar > 36:
        flags.append(f"TOO_MANY_VARIANTS ({nvar})"); score -= 20
    elif nvar > 18:
        flags.append(f"MANY_VARIANTS ({nvar})"); score -= 10
    if prices and min(prices) > 0 and max(prices) / min(prices) > 3:
        flags.append("WIDE_PRICE_RANGE (>3x)"); score -= 10
    if FRAGILE_RE.search(title + "\n" + text_nb):
        flags.append("FRAGILE_MATERIAL (stone/glass)"); score -= 25
    if INSTALL_RE.search(text_nb):
        flags.append("WALL/PRO INSTALL"); score -= 15
    if re.search(r"bed|mattress", title, re.I):
        flags.append("BED_SIZE_DEPENDENT"); score -= 10
    if re.search(r"sofa|couch|sectional", title, re.I) and any(re.search(r"left|right|fabric|leather", v, re.I) for v in vals):
        flags.append("SOFA_CONFIG/FABRIC"); score -= 10
    if SOLID_CLAIM_RE.search(title + "\n" + text_nb):
        flags.append("CLAIM_SOLID_WOOD_VERIFY")        # verification flag, no score penalty
    if not p.get("images"):
        flags.append("NO_IMAGES"); score -= 20
    if not DIM_RE.search(text_nb) and not any(parse_dims(v)[0] for v in vals):
        flags.append("NO_DIMENSIONS_FOUND"); score -= 10
    if ASSEMBLY_RE.search(text_nb):
        flags.append("SELF_ASSEMBLY")
    elif FULLY_ASSEMBLED_RE.search(text_nb):
        flags.append("FULLY_ASSEMBLED")
    hard = {"MADE_TO_ORDER/CUSTOM", "CUSTOM_OPTION_VALUE", "BED_SIZE_DEPENDENT", "SOFA_CONFIG/FABRIC",
            "TOO_MANY_VARIANTS", "NO_IMAGES"}
    has_hard = bool(hard & {f.split(" ")[0] for f in flags})
    score = max(score, 0)
    tier = "C-EXCLUDE" if has_hard or score < 60 else ("A-STANDARD" if score >= 80 else "B-REVIEW")
    return score, flags, tier


# ============================================================================ main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--store", help="e.g. https://your-store.example")
    ap.add_argument("--from-json", help="re-use saved raw_products.json (skips catalogue fetch)")
    ap.add_argument("--out", default="export")
    ap.add_argument("--images", choices=["none", "variant", "all"], default="none")
    ap.add_argument("--handles", help="file: one product handle per line (shortlist)")
    ap.add_argument("--only-eligible", action="store_true", help="download images only for eligible (standardised) products")
    ap.add_argument("--max-products", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--sleep", type=float, default=0.8)
    ap.add_argument("--no-collections", action="store_true")
    ap.add_argument("--check-images", type=int, default=0, help="HEAD-check a random sample of N image URLs")
    a = ap.parse_args()

    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    report = []
    store = (a.store or "").rstrip("/")

    # ---------------- catalogue
    if a.from_json:
        products = json.loads(Path(a.from_json).read_text(encoding="utf-8"))
        coll_path = Path(a.from_json).with_name("raw_collections.json")
        coll_map = json.loads(coll_path.read_text(encoding="utf-8")) if coll_path.exists() else {}
    else:
        if not store:
            sys.exit("--store or --from-json is required")
        print(f"[1/4] Catalogue from {store}/products.json")
        products = fetch_all_products(store, a.sleep, a.max_products)
        report.append(f"products.json: {len(products)} products")

        if not a.max_products:
            print("[2/4] Completeness check vs sitemap")
            sm = sitemap_product_handles(store)
            got = {p["handle"] for p in products}
            missing = sorted(sm - got)
            report.append(f"sitemap product URLs: {len(sm)} | in products.json: {len(sm & got)} | missing: {len(missing)}")
            recovered = 0
            for h in missing:
                pj = fetch_product_js(store, h)
                if pj:
                    products.append(pj); recovered += 1
                time.sleep(a.sleep / 2)
            report.append(f"missing recovered via /products/<handle>.js: {recovered}")
            not_in_sitemap = len(got - sm)
            report.append(f"in products.json but not in sitemap: {not_in_sitemap}")

        coll_map = {}
        if not a.no_collections:
            print("[3/4] Collections → product mapping")
            cj = get(f"{store}/collections.json?limit=250", as_json=True) or {}
            cols = cj.get("collections", [])
            report.append(f"collections: {len(cols)}")
            for c in cols:
                for p in paged_products(f"{store}/collections/{c['handle']}/products.json", a.sleep / 2):
                    coll_map.setdefault(p["handle"], []).append(c["title"])
            (out / "raw_collections.json").write_text(json.dumps(coll_map, ensure_ascii=False), encoding="utf-8")
        (out / "raw_products.json").write_text(json.dumps(products, ensure_ascii=False), encoding="utf-8")

    # ---------------- filter
    if a.handles:
        keep = {ln.strip() for ln in Path(a.handles).read_text(encoding="utf-8").splitlines() if ln.strip()}
        products = [p for p in products if p["handle"] in keep]

    # ---------------- flatten
    print("[4/4] Building tables")
    prod_rows, var_rows, img_rows, sku_rows, coll_rows, downloads = [], [], [], [], [], []
    for p in products:
        handle = p["handle"]
        opts = p.get("options", []) or []
        opt_names = [o["name"] for o in opts]
        color_idx = next((i for i, n in enumerate(opt_names) if re.search(r"colou?r|finish", n, re.I)), None)
        color_vals = list(opts[color_idx].get("values", [])) if color_idx is not None else []
        text = html_to_text(p.get("body_html", ""))
        text_nb = BOILERPLATE_RE.sub("", text)
        all_vals = [str(v) for o in opts for v in o.get("values", [])]
        dims = sorted({"x".join(g for g in m.groups()[:3] if g) + (m.group(4) or "cm").lower() for m in DIM_RE.finditer(text_nb)} |
                      {v for v in all_vals if parse_dims(v)[0]})
        mat = MATERIAL_RE.search(text_nb)
        score, flags, tier = screen_product(p, text)
        eligible = tier != "C-EXCLUDE"
        prices = [float(v["price"]) for v in p.get("variants", []) if v.get("price")]
        cmp_prices = [float(v["compare_at_price"]) for v in p.get("variants", []) if v.get("compare_at_price")]
        cols = coll_map.get(handle, [])
        category = guess_category(p.get("title", ""), p.get("product_type") or "")
        prod_rows.append({
            "handle": handle, "title": p.get("title", ""), "category_guess": category,
            "product_type": p.get("product_type") or "", "collections": " | ".join(cols),
            "options": " || ".join(f'{o["name"]}: {", ".join(map(str, o.get("values", [])))}' for o in opts),
            "variant_count": len(p.get("variants", [])), "image_count": len(p.get("images", [])),
            "price_min": min(prices) if prices else "", "price_max": max(prices) if prices else "",
            "compare_at_max": max(cmp_prices) if cmp_prices else "",
            "standard_score": score, "tier": tier, "flags": "; ".join(flags),
            "dimensions_found": "; ".join(dims), "material_found": mat.group(1).strip() if mat else "",
            "created_at": p.get("created_at", ""), "url": f"{store}/products/{handle}" if store else "",
            "source": p.get("_source", "products.json"),
            "description_text": text, "description_no_boilerplate": text_nb,
        })
        for c in cols:
            coll_rows.append({"collection": c, "handle": handle})

        has_variant_map = any(im.get("variant_ids") for im in p.get("images", []))
        img_color = {}
        for v in p.get("variants", []):
            fi = v.get("featured_image")
            if fi and fi.get("id") is not None and color_idx is not None:
                img_color.setdefault(fi["id"], v.get(f"option{color_idx+1}"))
        imgs = p.get("images", [])
        for im in imgs:
            color = img_color.get(im.get("id"), "") or infer_color(im, color_vals)
            pos = im.get("position") or 99
            fname = os.path.basename(urlparse(im["src"]).path)
            local = Path("images") / handle / slug(color or "gallery") / f"{int(pos):03d}_{fname}"
            img_rows.append({"handle": handle, "image_id": im.get("id"), "position": pos, "color": color,
                             "src": im["src"], "local_path": str(local), "width": im.get("width"),
                             "height": im.get("height"), "variant_ids": " ".join(map(str, im.get("variant_ids", []) or []))})
            want = a.images == "all" or (a.images == "variant" and (
                im.get("variant_ids") or pos <= 3 or (not has_variant_map and (color or pos <= 15))))
            if a.only_eligible and not eligible:
                want = False
            if want:
                downloads.append((im["src"], out / local))

        for v in p.get("variants", []):
            vals = [v.get("option1"), v.get("option2"), v.get("option3")]
            color = vals[color_idx] if color_idx is not None else ""
            others = [str(x) for i, x in enumerate(vals) if x and i != color_idx]
            fi = v.get("featured_image") or {}
            img_local = ""
            if fi.get("src"):
                img_local = str(Path("images") / handle / slug(color or "gallery") /
                                f'{int(fi.get("position") or 0):03d}_{os.path.basename(urlparse(fi["src"]).path)}')
            elif color:
                m = next((r for r in img_rows if r["handle"] == handle and r["color"] == color), None)
                img_local = m["local_path"] if m else ""
            var_rows.append({"handle": handle, "variant_id": v.get("id"), "variant_title": v.get("title", ""),
                             "option1_name": opt_names[0] if len(opt_names) > 0 else "", "option1": vals[0],
                             "option2_name": opt_names[1] if len(opt_names) > 1 else "", "option2": vals[1],
                             "option3_name": opt_names[2] if len(opt_names) > 2 else "", "option3": vals[2],
                             "price": v.get("price"), "compare_at_price": v.get("compare_at_price"),
                             "available": v.get("available"), "grams": v.get("grams"),
                             "variant_image_src": fi.get("src", ""), "variant_image_local": img_local,
                             **dict(zip(["L_cm", "W_cm", "H_cm"], next((parse_dims(x) for x in vals if x and parse_dims(x)[0]), (None, None, None))))})
            sku_rows.append({
                "tier": tier, "new_sku": "", "new_title_EN (rewrite)": "",
                "source_handle": handle, "source_title": p.get("title", ""), "category": category,
                "color": color, "size_or_other": " / ".join(others),
                "anchor_price_AUD": v.get("price"), "source_compare_at (DO NOT USE as was-price)": v.get("compare_at_price") or "",
                "dimensions_found": "; ".join(dims), "material_claimed": prod_rows[-1]["material_found"],
                "material_verified_with_supplier": "", "taobao_match_shop": "", "taobao_match_item": "",
                "supplier_link_main": "", "supplier_link_backup": "", "cost_cny": "", "parcels": "", "cbm": "",
                "variant_image_local": img_local, "flags": "; ".join(flags),
                **dict(zip(["L_cm", "W_cm", "H_cm"], next((parse_dims(x) for x in vals if x and parse_dims(x)[0]), (None, None, None))))})

    def write_csv(name, rows):
        if not rows:
            return
        keys = list(dict.fromkeys(k for r in rows for k in r))
        with open(out / name, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
        print(f"  wrote {name} ({len(rows)} rows)")

    for name, rows in [("products.csv", prod_rows), ("variants.csv", var_rows), ("images.csv", img_rows),
                       ("collections.csv", coll_rows), ("sku_master_draft.csv", sku_rows)]:
        write_csv(name, rows)

    tiers = defaultdict(int)
    for r in prod_rows:
        tiers[r["tier"]] += 1
    flag_count = defaultdict(int)
    for r in prod_rows:
        for f in filter(None, r["flags"].split("; ")):
            flag_count[f.split(" (")[0]] += 1
    report += [f"products exported: {len(prod_rows)} | variants: {len(var_rows)} | images: {len(img_rows)}",
               "tiers: " + ", ".join(f"{k}={v}" for k, v in sorted(tiers.items())),
               "flags: " + ", ".join(f"{k}={v}" for k, v in sorted(flag_count.items(), key=lambda x: -x[1])),
               f"variants with a colour-linked image: {sum(1 for r in var_rows if r['variant_image_local'])} / {len(var_rows)}"]

    # ---------------- optional image URL check
    if a.check_images and img_rows:
        sample = random.sample(img_rows, min(a.check_images, len(img_rows)))
        ok, sizes = 0, []
        for r in sample:
            try:
                h = SESSION.head(r["src"], timeout=20, allow_redirects=True)
                if h.status_code == 200:
                    ok += 1
                    if h.headers.get("Content-Length"):
                        sizes.append(int(h.headers["Content-Length"]))
            except requests.RequestException:
                pass
        avg = sum(sizes) / len(sizes) if sizes else 0
        report.append(f"image URL check: {ok}/{len(sample)} reachable; avg size {avg/1024:.0f} KB; "
                      f"estimated total for all images ≈ {avg*len(img_rows)/1e9:.1f} GB")

    # ---------------- images
    if a.images != "none" and downloads:
        print(f"Downloading {len(downloads)} images (existing files skipped) ...")

        def dl(item):
            src, dest = item
            if dest.exists() and dest.stat().st_size > 0:
                return "skip"
            dest.parent.mkdir(parents=True, exist_ok=True)
            for attempt in range(3):
                try:
                    r = SESSION.get(src, timeout=60); r.raise_for_status()
                    dest.write_bytes(r.content); return "ok"
                except requests.RequestException:
                    time.sleep(2 * (attempt + 1))
            return "fail"

        with ThreadPoolExecutor(max_workers=max(1, min(a.workers, 8))) as ex:
            res = list(ex.map(dl, downloads))
        report.append(f"images downloaded: ok={res.count('ok')} skipped={res.count('skip')} failed={res.count('fail')}")

    (out / "completeness_report.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))

    # ---------------- review workbook
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill
        wb = Workbook(); ws = wb.active; ws.title = "Products"
        cols = ["tier", "standard_score", "handle", "title", "category_guess", "collections", "variant_count",
                "image_count", "price_min", "price_max", "flags", "dimensions_found", "material_found", "url"]
        ws.append(cols)
        for r in sorted(prod_rows, key=lambda r: (r["tier"], -r["standard_score"], r["category_guess"])):
            ws.append([r[c] for c in cols])
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="1F3864")
        ws.auto_filter.ref = ws.dimensions; ws.freeze_panes = "C2"
        for col, w in zip("ABCDEFGHIJKLMN", [9, 8, 30, 40, 18, 30, 8, 8, 9, 9, 50, 30, 30, 40]):
            ws.column_dimensions[col].width = w
        s = wb.create_sheet("Summary")
        for line in report:
            s.append([line])
        cat = defaultdict(lambda: defaultdict(int))
        for r in prod_rows:
            cat[r["category_guess"]]["total"] += 1
            cat[r["category_guess"]][r["tier"]] += 1
        s.append([]); s.append(["Category", "Products", "A-STANDARD", "B-REVIEW", "C-EXCLUDE"])
        for k, d in sorted(cat.items(), key=lambda x: -x[1]["total"]):
            s.append([k, d["total"], d["A-STANDARD"], d["B-REVIEW"], d["C-EXCLUDE"]])
        s.column_dimensions["A"].width = 90
        wb.save(out / "catalogue_review.xlsx"); print("  wrote catalogue_review.xlsx")
    except ImportError:
        pass
    print("Done.")


if __name__ == "__main__":
    main()
