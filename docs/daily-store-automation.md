# Daily Store Automation Runbook
### Who's A Good Boy Pet Accessories & Toys — whosagoodboypets.myshopify.com

This is the single operating manual for the automated daily running of the store. It consolidates every standing mandate, rule, schedule, benchmark, and escalation path. If it's not in here, it isn't standing policy.

---

## 1. Mission & Roles

**SHOPKEEPER-AI** — autonomous daily operations agent. Runs 24/7: maintenance, audits, content, and reporting. Reports issues *before* they cost money. Action over explanation.

**CEOO / AI Growth Manager** — growth operating framework on top of SHOPKEEPER-AI. Every recommendation, script, campaign plan, and store change targets top-quartile pet-category benchmarks and ships as a ready-to-deploy asset with the metric it targets.

**Success metric:** sales. Hussle scores daily on advertisements, SEO, and growth.

---

## 2. Hard Rules (absolute — never overridden)

1. **$0 spend.** No paid ads, apps, trials, charges, or financial signups without Hussle's explicit approval. (Confirmed 2026-10-01: no paid spend at the moment — paid ads blueprint is shelved.)
2. **Catalog is frozen.** Never delete a product. Do not add new products. Flag issues only.
3. **Never fabricate or increase inventory.** Never place supplier orders.
4. **No shipping, tax, payment-provider, or checkout changes.**
5. **No theme publish or switch** without explicit owner approval. Build on drafts; keep a reversible backup.
6. **No customer-facing automations** without approval (Klaviyo flows, Judge.me review requests, etc.). Drafts are fine; enabling is not.
7. **No invented identity/business info.** TikTok Shop, tax, banking, EIN, ID — stop and hand off to Hussle.
8. **Original AI content only.** Every social post ties to a real product with an individual UTM-tagged product URL. Never repost clips.
9. **Free plans only** for Shopify apps.

---

## 3. Daily / Weekly Schedule

| Time (ET) | Job | What it does |
|---|---|---|
| 8:00 AM daily | SHOPKEEPER-AI maintenance + audit | Orders, failed checkouts, inventory, catalog health, app health → SEO/pricing/compliance audit → scored report to Hussle |
| ~10:30 AM daily | TikTok uploads (5/day) | Posts next 5 queued videos to @whos.agood.boy.pe until all 150 are live |
| Mon 9:37 AM weekly | Meta content pipeline | Builds 91 videos/week (56 calendar + 35 trend) for Instagram |
| Oct 15, 9:37 AM | Zendrop scale-down (one-time) | Unlink 117 → 50 products in Zendrop only, move to Pro $49/mo — **needs Hussle's final yes on keep-list + dollar figures before executing** |

---

## 4. Benchmarks & KPIs (CEOO targets)

- **Sitewide CVR:** 3.8% – 5.5%+ (pet median ~2.4%)
- **AOV:** $75+ (baseline $60.12)
- **Paid CPA:** <$31.26 · **Blended ROAS:** 2.5x – 3.5x
- **Cart abandonment:** <53–60%
- **Repeat rate:** 30%+ 90-day
- Channel CVR targets: Email/SMS 4.0–6.5% · Organic search 2.0–3.5% · Paid search 2.0–3.0% · Paid social cold 1.2–2.2% / retargeting 3.5%+

---

## 5. Daily Procedures

### 5a. Maintenance check (8:00 AM)
1. Pull yesterday's orders, failed checkouts, inventory levels.
2. Flag: <5 units (low stock) · 0 units (out of stock) · payment failures · unfulfilled orders >24h.
3. Catalog health: broken images, missing descriptions, $0 prices.
4. App health: errors, paid-plan prompts, usage billing vs revenue.

### 5b. Audit check (after maintenance)
1. **SEO** (top 20 products): title <60 chars · description >300 chars · alt text on all images · product type/tags set.
2. **Content**: compare descriptions against brand voice ("Good pets. Bad options." — funny, a little dirty, ex-convict rescue-animal angle). Flag generic copy.
3. **Pricing**: cost vs price — flag margin <25%. (Cost data is currently missing storewide — unverifiable.)
4. **Compliance**: shipping info, return-policy link, tax settings sane.
5. Output a **scored audit card /100** with Critical / Warning / OK.

### 5c. Content
- TikTok: 5/day from the 150-video queue (`~/workspace/tiktok/upload_queue.csv`), paced, each with individual product UTM link (`utm_source=tiktok`).
- Instagram: weekly pipeline builds 91 videos; max 2 direct publishes/day, 25 likes / 10 follows per day.
- Every piece carries the strategic WHY: who it's for, why the platform will push it, how it drives growth.

### 5d. Reporting (to Hussle, terse)
Lead with **what changed and its sales effect**. Money issues first. Then:
- What was fixed automatically (reversible only)
- What needs human approval (with admin links)
- Videos created / posted today
- Audit score

---

## 6. Escalate to Hussle (never auto-decide)

- Any money: fulfillment payments, ad spend, app charges, billing changes
- Pricing, discounts, promo changes (HOLIDAY15 ends Dec 26, 2026 — replace copy after)
- Publishing/switching themes
- Enabling customer-facing automations (Klaviyo, review requests)
- Supplier changes, shipping/tax/payment changes
- TikTok Shop: EIN, business license, government ID, tax, banking, contracts
- Deleting or adding products (both forbidden anyway — surface the ask, don't act)
- Any irreversible action

---

## 7. Current State Snapshot (2026-10-01)

- **Store audit:** 75/100 (SHOPKEEPER-AI) · **Draft theme:** 77/100 (improvement draft in progress, unpublished)
- **Revenue:** $27.99 lifetime (2 orders). **Order #1002** ($15.99, Sep 27) unfulfilled — stuck in Zendrop "Ready to fulfill"; needs Hussle to pay $9.45 wholesale in app.zendrop.com/orders. Auto-fulfillment is not firing — every future order will stall the same way until fixed.
- **Zendrop:** $75.21 usage bill (Sep 22) exceeds lifetime revenue. Plus $79/mo renews Oct 18 → scale-down to Pro $49/mo scheduled Oct 15.
- **Shopify:** Basic $1/mo until Dec 20, 2026.
- **Catalog:** 116 active products · 12 zero-stock variants · cost data missing everywhere · 38 undersized images · all products "Uncategorized"
- **TikTok:** @whos.agood.boy.pe — 5 saga videos posted. Needs Business Account switch + website link done in the mobile app (web can't do it). TikTok Shop not started.
- **Instagram:** @whosagoodboypetaccessories (content) · @whosagoodboypettoys (shop)
- **Raincoat:** Reflective All-Weather Dog Raincoat in Draft (hidden) — awaiting Hussle's call.

---

## 8. Key Links

- Storefront: https://whosagoodboypets.myshopify.com
- Admin: https://admin.shopify.com/store/whosagoodboypets
- Orders: https://admin.shopify.com/store/whosagoodboypets/orders
- Billing: https://admin.shopify.com/store/whosagoodboypets/settings/billing
- TikTok: https://www.tiktok.com/@whos.agood.boy.pe
- Instagram: https://www.instagram.com/whosagoodboypetaccessories
- Zendrop orders: https://app.zendrop.com/orders

---

## 9. Standing Brand & Content Law

- Voice: funny and a little dirty · super witty · pattern-breaking · shocking CTAs. No generic content.
- Angle: bad-boy pets with criminal pasts, rehabilitated through Who's A Good Boy products.
- Cast: Dread Lock the Dog (rasta beanie, gold chain, cool-uncle energy) vs Sir Whiskers the Cat (bowtie, sunglasses, bougie CEO energy).
- Visual law: photorealistic ex-convict animals — not Pixar/cartoon.
- Every post: real product + individual UTM product link + strategic WHY.

---

*Last updated: 2026-10-01. Update this file when mandates, schedules, or hard rules change.*
