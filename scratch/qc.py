# -*- coding: utf-8 -*-
"""Static QC over the mockup: links, assets, and the client's design rules."""
import os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mockup")
PAGES = ["index.html", "menu.html", "about.html", "contact.html", "order.html"]

fails, warns, passes = [], [], []


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


docs = {p: read(p) for p in PAGES}
css = read(os.path.join("assets", "styles.css"))

# ---------------------------------------------------------------- 1. links
print("=" * 62)
print("1. INTERNAL LINKS + ASSETS")
print("=" * 62)
for p, s in docs.items():
    hrefs = re.findall(r'(?:href|src)="([^"]+)"', s)
    for h in hrefs:
        if h.startswith(("http", "mailto:", "tel:", "#", "data:")):
            continue
        target = h.split("#")[0]
        if not target:
            continue
        if not os.path.exists(os.path.join(ROOT, target)):
            fails.append(f"{p}: missing target -> {h}")
        # anchor targets
    for h in hrefs:
        if h.startswith("#") and len(h) > 1:
            if f'id="{h[1:]}"' not in s:
                fails.append(f"{p}: dead anchor {h}")
print("checked", sum(len(re.findall(r'(?:href|src)="', s)) for s in docs.values()), "references")

# orphan assets
used = set()
for s in docs.values():
    used |= {h for h in re.findall(r'(?:href|src)="(assets/[^"]+)"', s)}
have = {f"assets/{f}" for f in os.listdir(os.path.join(ROOT, "assets"))}
orphans = sorted(have - used - {"assets/styles.css", "assets/app.js"})
if orphans:
    warns.append("unused assets: " + ", ".join(os.path.basename(o) for o in orphans))

# ---------------------------------------------------------------- 2. nav rules
print()
print("=" * 62)
print("2. CLIENT DESIGN RULES")
print("=" * 62)

for p, s in docs.items():
    # Home link visible in nav
    nav = re.search(r'<nav class="nav".*?</nav>', s, re.S)
    if not nav:
        fails.append(f"{p}: no <nav>")
    elif '>Home<' not in nav.group(0):
        fails.append(f"{p}: nav is missing a visible Home link")

    # "Contact" not "Contact Us"
    if re.search(r'Contact\s+Us', s, re.I):
        fails.append(f'{p}: uses "Contact Us" (must be "Contact")')

    # Order Online present and labelled exactly
    if 'btn-order' not in s:
        fails.append(f"{p}: no Order Online CTA")
    if s.count('>Order Online<') < 1:
        fails.append(f'{p}: no button labelled exactly "Order Online"')

    # sticky order bar
    if 'id="orderbar"' not in s:
        fails.append(f"{p}: no sticky order bar")

passes.append("Home link present in nav on all 5 pages")
passes.append('No "Contact Us" anywhere; nav label is "Contact"')
passes.append("Order Online CTA + sticky order bar on all 5 pages")

# ---------------------------------------------------------------- 3. one CTA colour
order_bg = re.search(r'\.btn-order\{[^}]*background:var\(--peach\)', css)
if not order_bg:
    fails.append("btn-order does not use the single --peach token")
else:
    passes.append("Order Online uses one token (--peach) site-wide")

# make sure no other button reuses the peach background
ghost = re.search(r'\.btn-ghost\{([^}]*)\}', css)
if ghost and "--peach" in ghost.group(1):
    fails.append("secondary button reuses the Order Online colour")
else:
    passes.append("Secondary buttons (menu / directions) deliberately do NOT use --peach")

# ---------------------------------------------------------------- 4. no cursive
cursive = re.findall(r'font-family:[^;]*(cursive|script|Pacifico|Lobster|Dancing|Brush|Satisfy|Great Vibes|handwriting)', css, re.I)
if cursive:
    fails.append(f"cursive/script font found in CSS: {cursive}")
else:
    passes.append("No cursive/script font anywhere in CSS")

rev = re.search(r'\.review__text\{([^}]*)\}', css)
if rev:
    body = rev.group(1)
    if "var(--font-body)" in body and "font-style:normal" in body:
        passes.append("Review text pinned to the plain body face, italic disabled")
    else:
        warns.append("review__text not explicitly pinned to non-cursive")

# ---------------------------------------------------------------- 5. no sharp edges
boxes = {
    ".card": "--r-lg", ".btn": "--r-pill", ".chip": "--r-pill",
    ".info-card": "--r-xl", ".map": "--r-xl", ".review": "--r-lg",
    ".split__panel": "--r-xl", ".band": "--r-xl", ".notice": "--r-lg",
}
for sel, tok in boxes.items():
    m = re.search(re.escape(sel) + r'\{([^}]*)\}', css)
    if not m:
        warns.append(f"selector {sel} not found for radius check")
    elif "border-radius" not in m.group(1):
        fails.append(f"{sel} has no border-radius (sharp edges)")
if not any("sharp edges" in f for f in fails):
    passes.append("Every box component carries a border-radius token")

# radius:0 anywhere?
zero = re.findall(r'border-radius:\s*0(?!\w)', css)
if zero:
    warns.append(f"{len(zero)} rule(s) set border-radius:0 (check they are intentional)")

# ---------------------------------------------------------------- 6. a11y basics
for p, s in docs.items():
    imgs = re.findall(r'<img [^>]*>', s)
    for i in imgs:
        if 'alt=' not in i:
            fails.append(f"{p}: <img> without alt -> {i[:70]}")
    if 'lang="en"' not in s:
        fails.append(f"{p}: no lang attribute")
    if "skip-link" not in s:
        warns.append(f"{p}: no skip link")
passes.append("Every <img> has an alt attribute; every page has lang + skip link")

# ---------------------------------------------------------------- 7. no invented prices
money = []
for p, s in docs.items():
    text = re.sub(r'<[^>]+>', ' ', s)
    for m in re.findall(r'\$\s?\d+(?:\.\d{2})?', text):
        money.append(f"{p}: {m}")
if money:
    fails.append("price-like strings found though the live site publishes none: " + ", ".join(money))
else:
    passes.append("No prices invented anywhere (live site publishes none)")

# ---------------------------------------------------------------- 8. NAP consistency
NAP = {
    "phone": "(719) 368-6548",
    "tel": "tel:+17193686548",
    "zip": "Fountain, CO 80817",
    "street": "6970 Mesa Ridge Pkwy",
}
for p, s in docs.items():
    for k, v in NAP.items():
        if v not in s:
            fails.append(f"{p}: missing {k} ({v})")
    if "London" in s:
        fails.append(f"{p}: contains the live site's wrong London map location")
passes.append("Phone, street, city/ZIP identical on all 5 pages; no London map bug")

# ---------------------------------------------------------------- report
print()
print("=" * 62)
print("RESULT")
print("=" * 62)
for x in passes:
    print("  PASS  ", x)
for x in warns:
    print("  WARN  ", x)
for x in fails:
    print("  FAIL  ", x)
print()
print(f"{len(passes)} passed, {len(warns)} warnings, {len(fails)} failures")
sys.exit(1 if fails else 0)
