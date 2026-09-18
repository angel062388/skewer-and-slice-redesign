# Skewer &amp; Slice — session notes

**Date:** 2026-09-18 · **Org:** Magister Digital AI · **Client:** Skewer &amp; Slice
**Folder:** `Magister Digital AI/Skewer and Slice/`

---

## Where things stand

Redesign mockup is **built and verified locally**. Five pages, committed to a
local git repo (`95003ee`). **Not yet pushed — no GitHub remote exists.**

---

## Verified facts (pulled from skewerandslice.com this session)

| Item | Value |
|---|---|
| Phone | (719) 368-6548 |
| Email | info@skewerandslice.com |
| Address | 6970 Mesa Ridge Pkwy, Unit #130, Fountain, CO 80817 |
| Hours | Daily 11AM – 9PM |
| Taglines | "Built over open flame. No compromise." / "Forged in fire. Made to order." / logo: "Forged in Fire, Served with Honor" |
| Nav | Home · Menu · About · Contact (already uses "Contact") |
| Menu | 9 categories, full item list captured — **no prices published anywhere** |
| Reviews | Only one attributable review on site (Melanie V., Google Local Guide) |
| Flame | YouTube embed, video ID `94UkyRfa4rs` — not a self-hosted file |

WordPress REST API (`/wp-json/wp/v2/media`) is **open**, which is how the full
media library was enumerated. Useful for future asset pulls.

---

## Decisions made

- **Hero food**: used the real photos (`sns-pepperoni-pizza`, `sns-k8-shami-teka-gyro-combo-v2`)
  rather than cropping the existing hero collage. Both are round objects, so
  they rotate convincingly; the collage panels are rectangular torn-edge art
  that would rotate awkwardly. Background removed with a flood-fill script
  (Pillow) — **no rembg, ImageMagick or ffmpeg on this machine**.
- **Flame**: rebuilt as ember still + canvas particles + glow. The YouTube
  embed cannot be re-hosted or timed to 5.5s, and there is no ffmpeg to encode
  a video locally. This uses the client's own licensed asset.
- **Animation timing**: BBQ at 350ms, pizza at 1150ms (800ms stagger), matching
  the client's "bbq first then pizza" instruction. Verified via the Web
  Animations API, not by eye.
- **Prices and reviews**: none invented. Two review slots carry visible
  `data-placeholder` markers so nothing fake can ship by accident.

---

## Bugs found on the LIVE site (worth telling the client)

1. **`/order/` is an empty page.** Every "Order Online" button leads nowhere.
   Biggest conversion problem on the site.
2. **Contact page map points to the London Eye, UK** instead of Fountain, CO.

---

## Client guidelines captured this session

- Home page with a visible Home nav link ✅ done
- "Contact", not "Contact Us" ✅ done
- No cursive fonts, especially in reviews ✅ done
- Order Online prominent, one button colour throughout, label exactly
  "Order Online", reachable while scrolling, Get Directions secondary,
  contrast over intrusive popup ✅ done
- Clean the ordering catalog; test mobile ordering, cart, pickup scheduling,
  checkout; verify completed-order attribution ⛔ **cannot be done** — there is
  no ordering platform connected to test against. Blocked until a provider is
  chosen and connected.

---

## Next steps

1. **Create the GitHub repo** — `gh` is installed (v2.98.0) but not logged in:
   ```
   gh auth login
   gh repo create skewer-and-slice-redesign --public --source=. --remote=origin --push
   ```
   Prior Magister repos live under `betchy1511-arch` (origin) and `angel062388`.
2. Get prices, two real Google reviews, and the About story from the client.
3. Choose an online ordering provider, embed it in `order.html`, then run the
   catalog/cart/checkout tests and set up completed-order (not click) tracking.
4. Wire the contact form to an inbox.

---

## Repo layout

```
Skewer and Slice/
├─ README.md
├─ SESSION-NOTES.md
├─ mockup/            index, menu, about, contact, order + assets/
└─ scratch/           build_pages.py, qc.py   (candidates/ gitignored)
```

Run `python scratch/qc.py` after any edit — it checks links, assets and every
client design rule above. Last run: 11 passed, 0 failures.
