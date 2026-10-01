# my-pet-store-ad-ops

Ad operations repo for **Who's A Good Boy Pet Accessories & Toys**
(`whosagoodboypets.myshopify.com`). Everything needed to run paid social and
host the supporting pages — no build step, no dependencies.

## Structure

```
my-pet-store-ad-ops/
├── .github/workflows/
│   ├── feed.yml              # Regenerates catalog.xml every 12h
│   ├── daily-report.yml      # Daily ad report → reports/YYYY-MM-DD.md
│   └── stock-check.yml       # Inventory guardrail every 6h
├── generate_feed.py              # Builds Meta/Google Ads XML catalog from products.json
├── catalog.xml                   # Generated feed (committed by the workflow)
├── scripts/
│   ├── daily_report.py           # Shopify + Meta/TikTok → Markdown report
│   └── stock_check.py            # Low-stock guardrail for featured buy links
├── reports/                      # Daily reports (generated)
├── docs/
│   └── automation-setup.md       # Setup guide for all four systems
├── creatives/
│   ├── image-prompts.md          # Midjourney/Flux photo prompts
│   ├── video-scripts.md          # TikTok & Reels ad scripts (Hook/Problem/CTA)
│   └── prompt_generator.md       # Winning-hook expansion framework
├── landing-pages/
│   ├── index.html                # Ultra-fast GitHub Pages landing page
│   └── featured.json             # Guardrail-managed featured buy links
├── tools/
│   └── utm_builder.html          # UTM link generator (open in any browser)
└── README.md
```

## Setup

1. **Push to GitHub.** Create a repo, push this folder.
2. **Enable Pages:** Settings → Pages → Deploy from branch → `/ (root)`.
   - Feed: `https://<you>.github.io/<repo>/catalog.xml`
   - Landing page: `https://<you>.github.io/<repo>/landing-pages/`
   - UTM builder: `https://<you>.github.io/<repo>/tools/utm_builder.html`
3. **Meta / Google catalog:** add the `catalog.xml` URL as a scheduled-fetch
   data source in Meta Commerce Manager / Google Merchant Center. The workflow
   refreshes it every 12 hours (00:00 and 12:00 UTC).
4. **Pixels:** paste your real Meta + TikTok Pixel IDs into `landing-pages/index.html`
   and `quiz-widget/index.html` where marked.

## Conventions

- UTM every outbound link: `utm_source` / `utm_medium` / `utm_campaign`
  (use `tools/utm_builder.html` to generate them).
- Only real promos in copy: `GOODBOY20` = 20% off, ends Oct 8, 2026.
  Never invent discounts, reviews, ratings, or customer counts.
- Prices and product names come from the live store — re-verify before each campaign.

## Local runs

```bash
python3 generate_feed.py   # writes catalog.xml in the repo root
```
