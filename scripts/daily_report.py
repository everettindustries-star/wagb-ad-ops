#!/usr/bin/env python3
"""scripts/daily_report.py — Daily ad performance report.

Fetches yesterday's spend/impressions/clicks from Meta and TikTok Marketing
APIs, orders/revenue from Shopify, computes ROAS, and writes a Markdown
report to reports/YYYY-MM-DD.md.

All credentials come from environment variables (set as GitHub Secrets in
the workflow). Any source missing credentials is skipped with a note —
the report is still written.

Env vars:
  SHOPIFY_STORE_DOMAIN   e.g. whosagoodboypets.myshopify.com
  SHOPIFY_ADMIN_TOKEN    Admin API token (custom app, read_orders scope)
  META_AD_ACCOUNT_ID     numeric, without the act_ prefix
  META_ACCESS_TOKEN      Meta Marketing API token
  TIKTOK_ADVERTISER_ID   TikTok advertiser ID
  TIKTOK_ACCESS_TOKEN    TikTok Marketing API token

Standard library only.
"""

import datetime
import json
import os
import sys
import urllib.request

META_API_VERSION = "v22.0"  # bump if Meta deprecates this version
CURRENCY = "USD"


def get(url, headers=None, timeout=30):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def post(url, payload, headers=None, timeout=30):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers or {}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def shopify_orders(domain, token, day):
    """(order_count, revenue) for a UTC day, or None if unavailable."""
    if not (domain and token):
        return None
    start = day.strftime("%Y-%m-%dT00:00:00Z")
    end = (day + datetime.timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
    url = (
        f"https://{domain}/admin/api/2024-01/orders.json"
        f"?status=any&created_at_min={start}&created_at_max={end}&limit=250"
        f"&fields=total_price,cancelled_at"
    )
    try:
        data = get(url, {"X-Shopify-Access-Token": token})
    except Exception as exc:
        print(f"Shopify error: {exc}", file=sys.stderr)
        return None
    count, revenue = 0, 0.0
    for o in data.get("orders", []):
        if o.get("cancelled_at"):
            continue
        count += 1
        try:
            revenue += float(o.get("total_price") or 0)
        except (TypeError, ValueError):
            pass
    return count, revenue


def meta_ads(account_id, token, day):
    """(spend, impressions, clicks, conv_value) for a day, or None."""
    if not (account_id and token):
        return None
    ds = day.strftime("%Y-%m-%d")
    url = (
        f"https://graph.facebook.com/{META_API_VERSION}/act_{account_id}/insights"
        f"?fields=spend,impressions,clicks,actions"
        f"&time_range={{'since':'{ds}','until':'{ds}'}}"
        f"&access_token={token}"
    )
    try:
        data = get(url)
    except Exception as exc:
        print(f"Meta error: {exc}", file=sys.stderr)
        return None
    rows = data.get("data", [])
    if not rows:
        return 0.0, 0, 0, 0.0
    r = rows[0]
    conv_value = 0.0
    for a in r.get("actions", []):
        if a.get("action_type") == "omni_purchase":
            try:
                conv_value = float(a.get("value") or 0)
            except (TypeError, ValueError):
                pass
    try:
        spend = float(r.get("spend") or 0)
    except (TypeError, ValueError):
        spend = 0.0
    return spend, int(r.get("impressions") or 0), int(r.get("clicks") or 0), conv_value


def tiktok_ads(advertiser_id, token, day):
    """(spend, impressions, clicks) for a day, or None."""
    if not (advertiser_id and token):
        return None
    ds = day.strftime("%Y-%m-%d")
    payload = {
        "advertiser_id": advertiser_id,
        "report_type": "BASIC",
        "dimensions": ["stat_time_day"],
        "data_level": "AUCTION_ADVERTISER",
        "start_date": ds,
        "end_date": ds,
        "metrics": ["spend", "impressions", "clicks"],
    }
    try:
        data = post(
            "https://business-api.tiktok.com/open_api/v1.3/report/integrated/get/",
            payload,
            {"Access-Token": token, "Content-Type": "application/json"},
        )
    except Exception as exc:
        print(f"TikTok error: {exc}", file=sys.stderr)
        return None
    rows = (data.get("data") or {}).get("list", [])
    if not rows:
        return 0.0, 0, 0
    m = rows[0].get("metrics", {})
    try:
        spend = float(m.get("spend") or 0)
    except (TypeError, ValueError):
        spend = 0.0
    return spend, int(m.get("impressions") or 0), int(m.get("clicks") or 0)


def fmt_money(v):
    return f"${v:,.2f}"


def fmt_roas(revenue, spend):
    if spend and spend > 0:
        return f"{revenue / spend:.2f}x"
    return "n/a"


def main():
    day = datetime.date.today() - datetime.timedelta(days=1)  # yesterday, complete day
    env = os.environ

    shop = shopify_orders(env.get("SHOPIFY_STORE_DOMAIN"), env.get("SHOPIFY_ADMIN_TOKEN"), day)
    meta = meta_ads(env.get("META_AD_ACCOUNT_ID"), env.get("META_ACCESS_TOKEN"), day)
    ttok = tiktok_ads(env.get("TIKTOK_ADVERTISER_ID"), env.get("TIKTOK_ACCESS_TOKEN"), day)

    total_spend = (meta[0] if meta else 0) + (ttok[0] if ttok else 0)
    revenue = shop[1] if shop else 0
    lines = [
        f"# Daily Ad Report — {day.isoformat()}",
        "",
        f"_Generated {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total ad spend | {fmt_money(total_spend)} |",
        f"| Shopify orders | {shop[0] if shop else 'n/a'} |",
        f"| Shopify revenue | {fmt_money(revenue) if shop else 'n/a'} |",
        f"| Blended ROAS (revenue / ad spend) | {fmt_roas(revenue, total_spend)} |",
        "",
        "## By channel",
        "",
        "| Channel | Spend | Impressions | Clicks | Conv. value | ROAS |",
        "|---|---|---|---|---|---|",
    ]
    if meta:
        lines.append(
            f"| Meta | {fmt_money(meta[0])} | {meta[1]:,} | {meta[2]:,} | "
            f"{fmt_money(meta[3])} | {fmt_roas(meta[3], meta[0])} |"
        )
    else:
        lines.append("| Meta | not configured | — | — | — | — |")
    if ttok:
        lines.append(
            f"| TikTok | {fmt_money(ttok[0])} | {ttok[1]:,} | {ttok[2]:,} | "
            f"— | — |"
        )
    else:
        lines.append("| TikTok | not configured | — | — | — | — |")
    lines += [
        "",
        "## Notes",
        "",
        "- ROAS = conversion value / spend (Meta) or Shopify revenue / total ad spend (blended).",
        "- TikTok conversion value needs the TikTok Pixel + Events API wired; spend/impressions/clicks report regardless.",
        "- A source showing 'not configured' means its env credentials were missing — see docs/automation-setup.md.",
        "",
    ]

    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{day.isoformat()}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
