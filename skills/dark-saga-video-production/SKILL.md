---
name: "dark-saga-video-production"
description: "Produce the Who's A Good Boy intense dark horror-comedy saga episodes and viral one-offs: character bible, intensity direction, generation specs, logo-bug burn, caption formula, and file conventions. Trigger when creating saga videos, viral pet videos, or continuing the DARK TURN storyline."
---

# Dark Saga Video Production

## Purpose
Produce original photoreal 9:16 videos for "Who's A Good Boy Pet Accessories & Toys" in the intense dark horror-comedy style: Dread Lock the Dog and Sir Whiskers the Cat run a vengeful night crew stalking pet owners who never shopped at the store. Menacing-but-absurd, never graphic. Every video is a store commercial with the product as plot device.

## Workflow
1. **Read the story state** — `~/workspace/content_videos/character-series/STATE.md` for the next episode numbers and the running storyline. Never reuse an episode number; never contradict established plot.
2. **Pick real products** — verify each product page loads at `whosagoodboypets.myshopify.com` with available variants. Use `~/workspace/content_videos/product_links.csv` for keyword→URL mapping. Never invent products, prices, or claims. Don't repeat products from the last 2 days (check recent `manifest.csv` files).
3. **Write the shot prompt** — one paragraph per video: photoreal (explicitly NOT cartoon), vertical 9:16, ~10s, hook in the first 1–2 seconds, character descriptions verbatim from `references/character-bible.md`, intensity beats from the Intensity Checklist below, no on-screen text. The product appears as plot device (calling card, bait, enforcement gear) — never a pitch.
4. **Generate** via `media.generate_video`. If a scene misfires on character likeness, regenerate with the bible description pasted verbatim rather than editing around it.
5. **Burn the logo bug** — `~/workspace/content_videos/assets/logo-bug.png` into the bottom of each video:
   `ffmpeg -i INPUT.mp4 -i ~/workspace/content_videos/assets/logo-bug.png -filter_complex "overlay=W-w-24:H-h-24" -c:a copy OUTPUT.mp4`
6. **Write captions** per `references/caption-formula.md`.
7. **Save** to `~/workspace/instagram-daily-five/<YYYY-MM-DD>/`: the mp4s + `captions.txt` + `manifest.csv` (columns: `filename,kind,episode_number,product_name,product_url`).
8. **Update STATE.md** with new episodes (number, premise, product featured).

## Intensity Checklist (the DARK TURN)
Oppressive dread, rain-slicked night streets, flickering lights, unblinking stares directly into the lens, slow menacing push-ins, extreme close-ups, hard cuts to black. Horror-trailer pacing. Comedy comes from absurdity of menace (a cat running a shakedown), never from gore.

## Output Contract
- 720×1280 mp4, ~10s, logo bug burned in, no on-screen text.
- Caption carries: hook, dark comedic voice, individual product URL with UTM (`utm_source`, `utm_medium`, `utm_campaign`), forced-choice verdict-bait CTA, end tagline.
- Recurring lines: "Reward your good boy with Who's A Good Boy Pet Accessories & Toys... or else." End tagline: "Who's A Good Boy Pet Accessories & Toys — before your pet goes bad."

## Operating Rules
1. Original characters and stories only — never depict real movie characters, never clone real actors' voices, never copy anyone's footage/audio.
2. Menacing-but-absurd, NEVER graphic: no blood, no gore, no real violence, no genuine threats toward real people.
3. Product is the plot device, never the pitch. Saga episodes end on a genuine cliffhanger teasing the next part ("PART N TOMORROW").
4. $0 spend on distribution unless the owner explicitly approves a budget.
