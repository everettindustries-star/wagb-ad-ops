# Automation Setup Guide

Covers all four systems: daily reporting, quiz webhook, inventory guardrail,
hook framework. Do the steps once; the workflows run themselves after.

## 0. Secrets (used by every workflow)

In your GitHub repo: **Settings → Secrets and variables → Actions → New repository secret.**

| Secret | Where to get it | Used by |
|---|---|---|
| `SHOPIFY_STORE_DOMAIN` | Your domain: `whosagoodboypets.myshopify.com` | daily report, guardrail |
| `SHOPIFY_ADMIN_TOKEN` | Shopify admin → Settings → Apps and sales channels → Develop apps → create app → Admin API access token. Scopes: `read_products`, `read_inventory`, `read_orders` | daily report, guardrail |
| `META_AD_ACCOUNT_ID` | Meta Ads Manager → account settings (numeric, no `act_`) | daily report |
| `META_ACCESS_TOKEN` | Meta App → Marketing API, or a system-user token with `ads_read` | daily report |
| `TIKTOK_ADVERTISER_ID` | TikTok Ads Manager → account info | daily report |
| `TIKTOK_ACCESS_TOKEN` | TikTok Marketing API app with advertiser authorization | daily report |

Never commit tokens to the repo. The scripts read them only from the environment.

## 1. Daily reporting (`scripts/daily_report.py`)

- Workflow: `.github/workflows/daily-report.yml` — runs daily at 12:00 UTC,
  writes `reports/YYYY-MM-DD.md` (yesterday's complete data), commits it.
- Manual run: Actions tab → "Daily Ad Report" → Run workflow.
- Local test (no secrets needed — sources just show "not configured"):
  `python3 scripts/daily_report.py`
- Report shows: total spend, orders, revenue, blended ROAS, per-channel
  spend/impressions/clicks/conversion value/ROAS.

## 2. Quiz webhook (`quiz-widget/index.html`)

The standalone quiz file (kept outside this repo per the repo tree) now has:

- `WEBHOOK_URL` constant at the top of the script — paste your Zapier
  "Catch Hook" URL or Klaviyo webhook URL there. Default is a placeholder.
- An optional email field on the result card ("Email me my match").
- On submit it POSTs JSON (fire-and-forget, never blocks the result):
  ```json
  {
    "event": "QuizCompleted",
    "pet_type": "dog", "trait": "chewer", "size": "Medium (25–60 lbs)",
    "email": "shopper@example.com",
    "product": "Durable Training Bite Stick Dog Toy",
    "value": 20.99, "currency": "USD",
    "timestamp": "2026-09-30T22:30:00Z"
  }
  ```
- The Meta Pixel `QuizCompleted` event still fires as before.

**Zapier:** create a Zap → Webhooks by Zapier → Catch Hook → copy the URL
into `WEBHOOK_URL` → add a Klaviyo/Sheets/Email step.
**Klaviyo:** use a Zapier step, or point `WEBHOOK_URL` at a Klaviyo-compatible
endpoint and map the fields.

## 3. Inventory guardrail (`scripts/stock_check.py`)

- Config: `landing-pages/featured.json` — each slot has a primary product
  handle + URL and a fallback handle + URL.
- Workflow: `.github/workflows/stock-check.yml` — runs every 6 hours.
  If a featured product's total inventory drops below **5** and the fallback
  is in stock, the buy link swaps to the fallback and the change is committed.
  When the product recovers, it swaps back automatically.
- The landing page applies `featured.json` to every `[data-featured]` link on
  load (see the "Featured Ad Picks" section in `landing-pages/index.html`).
- Every swap is a git commit, so it's fully auditable. If both primary and
  fallback are low, nothing swaps and the run logs "needs attention".
- Local test (no secrets): `python3 scripts/stock_check.py` → exits 0,
  prints "not set — nothing checked".

## 4. Hook framework (`creatives/prompt_generator.md`)

- No setup. Fill in `[PRODUCT]`/`[PRICE]` with real values, generate one
  creative per framework (10 total), tag links with `tools/utm_builder.html`,
  run them, keep the winner, repeat.
- Compliance checklist at the bottom of the file is mandatory for every
  variation — no invented stats, reviews, or discounts.
