#!/usr/bin/env python3
"""scripts/stock_check.py — Inventory guardrail for featured ad products.

Checks Shopify inventory for the products listed in
landing-pages/featured.json. If a featured product's total inventory falls
below LOW_STOCK_THRESHOLD (default 5) and its configured fallback is
in stock, the buy link in featured.json is swapped to the fallback.
If the featured product recovers, the link swaps back automatically.

The GitHub Actions workflow commits featured.json when it changes, and the
landing page applies it to every [data-featured] buy link on load.

Env vars:
  SHOPIFY_STORE_DOMAIN   e.g. whosagoodboypets.myshopify.com
  SHOPIFY_ADMIN_TOKEN    Admin API token (custom app, read_products scope)

Standard library only.
"""

import json
import os
import sys
import urllib.request

LOW_STOCK_THRESHOLD = 5
FEATURED_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "landing-pages",
    "featured.json",
)


def get_json(url, headers, timeout=30):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def inventory_for_handle(domain, token, handle):
    """Total inventory across all variants of a product handle. None on error."""
    url = f"https://{domain}/admin/api/2024-01/products.json?handle={handle}&fields=variants"
    try:
        data = get_json(url, {"X-Shopify-Access-Token": token})
    except Exception as exc:
        print(f"  ! API error for '{handle}': {exc}", file=sys.stderr)
        return None
    products = data.get("products", [])
    if not products:
        print(f"  ! handle '{handle}' not found in Shopify", file=sys.stderr)
        return None
    total = 0
    for v in products[0].get("variants", []):
        try:
            total += int(v.get("inventory_quantity") or 0)
        except (TypeError, ValueError):
            pass
    return total


def main():
    domain = os.environ.get("SHOPIFY_STORE_DOMAIN")
    token = os.environ.get("SHOPIFY_ADMIN_TOKEN")
    if not (domain and token):
        print("SHOPIFY_STORE_DOMAIN / SHOPIFY_ADMIN_TOKEN not set — nothing checked.",
              file=sys.stderr)
        return 0

    with open(FEATURED_PATH, encoding="utf-8") as f:
        featured = json.load(f)

    changed = []
    for slot, cfg in featured.items():
        stock = inventory_for_handle(domain, token, cfg["handle"])
        fb_stock = inventory_for_handle(domain, token, cfg["fallback_handle"])
        print(f"[{slot}] {cfg['handle']}: {stock} in stock | "
              f"fallback {cfg['fallback_handle']}: {fb_stock} in stock")
        if stock is None:
            continue  # API error — never swap on unknown state

        if stock < LOW_STOCK_THRESHOLD:
            if fb_stock is not None and fb_stock >= LOW_STOCK_THRESHOLD:
                if cfg["url"] != cfg["fallback_url"]:
                    cfg["url"] = cfg["fallback_url"]
                    changed.append(f"{slot}: swapped to fallback ({cfg['fallback_handle']})")
            else:
                print(f"  ! {slot}: LOW STOCK and fallback also low — needs attention")
        else:
            if cfg["url"] != cfg["primary_url"]:
                cfg["url"] = cfg["primary_url"]
                changed.append(f"{slot}: recovered, swapped back to primary")

    if changed:
        with open(FEATURED_PATH, "w", encoding="utf-8") as f:
            json.dump(featured, f, indent=2)
            f.write("\n")
        print("CHANGED:")
        for c in changed:
            print("  -", c)
    else:
        print("No changes needed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
