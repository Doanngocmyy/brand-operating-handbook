# Tools

| Script | Purpose |
|---|---|
| `catalog_export.py` | Export products, variants and images from a Shopify store you own or are authorised to use (public `/products.json`, sitemap completeness check, polite rate limits). |
| `normalize_catalog.py` | Normalise the export into a clean database: 8 main categories, A/B/C standardisation tiers, one colour standard, W × D × H in cm, new product codes and SKUs, image folders by tier/category/code/colour. |

```bash
pip install requests openpyxl pandas
python catalog_export.py --store https://your-store.example --out export_store --images none
python normalize_catalog.py --raw export_store/raw_products.json --out clean_db --store-url https://your-store.example
```

Output data stays local (it is git-ignored). Do not commit exported data to this public repository.
