#!/usr/bin/env python3
"""generate_feed.py — Build a Meta/Google Ads XML product catalog feed.

Fetches product data from the store's public products.json endpoint,
loops through ALL products and variants, extracts title, price, image URL,
availability status, and product link (with UTMs), and writes a valid
Meta Catalog / Google Merchant XML feed to catalog.xml.

Standard library only — no pip dependencies needed.
"""

import html
import json
import re
import sys
import urllib.request

STORE_DOMAIN = "whosagoodboypets.myshopify.com"
BASE_URL = f"https://{STORE_DOMAIN}"
BRAND = "Who's A Good Boy Pet Accessories & Toys"
CURRENCY = "USD"
TIMEOUT = 30
PAGE_LIMIT = 250

# UTM tracking appended to every product link in the feed.
# If you run separate Meta and Google feeds, change utm_source per feed
# (e.g. utm_source=meta_catalog vs utm_source=google_shopping).
FEED_UTM = "utm_source=product_catalog&utm_medium=feed&utm_campaign=ad_ops"


def fetch_products():
    """Fetch all products from the public products.json endpoint (paginated)."""
    products = []
    page = 1
    while True:
        url = f"{BASE_URL}/products.json?limit={PAGE_LIMIT}&page={page}"
        req = urllib.request.Request(url, headers={"User-Agent": "WAGB-FeedBot/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                data = json.load(resp)
        except Exception as exc:  # network / HTTP errors
            print(f"ERROR fetching {url}: {exc}", file=sys.stderr)
            sys.exit(1)
        batch = data.get("products", [])
        if not batch:
            break
        products.extend(batch)
        page += 1
    return products


def strip_html(value):
    text = re.sub(r"<[^>]+>", " ", value or "")
    return html.unescape(re.sub(r"\s+", " ", text)).strip()


def esc(text):
    return html.escape(text or "", quote=True)


def variant_image(product, variant):
    """Best image for a variant: its own image, else the product's featured image."""
    vid = variant.get("id")
    for img in product.get("images", []):
        if vid in (img.get("variant_ids") or []):
            return img.get("src", "")
    return (product.get("image") or {}).get("src", "")


def variant_title(product, variant):
    title = product.get("title", "")
    vt = (variant.get("title") or "").strip()
    if vt and vt.lower() != "default title":
        title += " - " + vt
    return title


def build_feed(products):
    """Build the RSS 2.0 + Google Merchant namespace XML, one item per variant."""
    items = []
    for p in products:
        handle = p.get("handle", "")
        desc = strip_html(p.get("body_html", ""))[:5000] or p.get("title", "")
        vendor = p.get("vendor") or BRAND
        for v in p.get("variants", []):
            price = float(v.get("price") or 0)
            available = "in_stock" if v.get("available") else "out_of_stock"
            image = variant_image(p, v)
            link = f"{BASE_URL}/products/{handle}?variant={v['id']}&{FEED_UTM}"
            items.append(
                "    <item>\n"
                f"      <g:id>{v['id']}</g:id>\n"
                f"      <g:item_group_id>{p['id']}</g:item_group_id>\n"
                f"      <g:title>{esc(variant_title(p, v))}</g:title>\n"
                f"      <g:description>{esc(desc)}</g:description>\n"
                f"      <g:link>{esc(link)}</g:link>\n"
                + (f"      <g:image_link>{esc(image)}</g:image_link>\n" if image else "")
                + f"      <g:price>{price:.2f} {CURRENCY}</g:price>\n"
                f"      <g:availability>{available}</g:availability>\n"
                f"      <g:brand>{esc(vendor)}</g:brand>\n"
                "      <g:condition>new</g:condition>\n"
                "    </item>"
            )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">\n'
        "  <channel>\n"
        f"    <title>{esc(BRAND)}</title>\n"
        f"    <link>{BASE_URL}</link>\n"
        f"    <description>{esc('Product catalog feed for ' + BRAND)}</description>\n"
        + "\n".join(items)
        + "\n  </channel>\n</rss>\n"
    )


def main():
    products = fetch_products()
    if not products:
        print("No products fetched; catalog.xml not written.", file=sys.stderr)
        sys.exit(1)
    feed = build_feed(products)
    with open("catalog.xml", "w", encoding="utf-8") as f:
        f.write(feed)
    n_items = feed.count("<item>")
    print(f"Wrote catalog.xml: {len(products)} products, {n_items} variant items.")


if __name__ == "__main__":
    main()
