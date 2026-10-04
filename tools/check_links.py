"""Check every internal link and #anchor in docs/ resolves. Usage: python tools/check_links.py"""
import re, sys
from html.parser import HTMLParser
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"


class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids, self.links = set(), []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        if tag == "a" and a.get("href"): self.links.append(a["href"])


pages = {}
for f in DOCS.glob("*.html"):
    p = P(); p.feed(f.read_text(encoding="utf-8")); pages[f.name] = p
for sub in ("sop", "plan"):
    for f in (DOCS / sub).glob("*.svg"):
        pages[f"{sub}/" + f.name] = P()
bad = 0
for name, p in sorted(pages.items()):
    for h in p.links:
        if re.match(r"^(https?:|mailto:)", h):
            continue
        page, _, frag = h.partition("#")
        target = page or name
        if target not in pages:
            print(f"{name}: missing page {h}"); bad += 1; continue
        if frag and frag != "top" and frag not in pages[target].ids:
            print(f"{name}: missing anchor {h}"); bad += 1
print(f"checked {sum(len(p.links) for p in pages.values())} links on {len(pages)} files, {bad} broken")
sys.exit(1 if bad else 0)
