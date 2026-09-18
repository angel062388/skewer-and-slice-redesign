# Skewer &amp; Slice — session notes

**Date:** 2026-09-18 · **Org:** Magister Digital AI · **Client:** Skewer &amp; Slice
**Folder:** `Magister Digital AI/Skewer and Slice/`

---

## Where things stand

Redesign mockup is **built, pushed, and live on GitHub Pages** (verified HTTP 200
on all five pages, 2026-09-18).

| | |
|---|---|
| **Repo** | https://github.com/angel062388/skewer-and-slice-redesign |
| **Live preview** | https://angel062388.github.io/skewer-and-slice-redesign/ (root redirects to `mockup/`) |
| **Account** | `angel062388` — the browser's default account at login time, **not** `betchy1511-arch` where the Magister Digital redesign lives. Fine functionally; move it later if the client wants one home for all repos. |
| **Pages source** | `main` branch, `/` root — same setup as the previous redesign |

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

1. ~~Create the GitHub repo~~ **Done.** `gh` is now logged in as `angel062388`
   (keyring). To publish future edits: `git add -A && git commit && git push` —
   Pages rebuilds in about 40s.
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

---

## Update - later on 2026-09-18

**Pushed:** hero choreography rebuilt (left -> centre at 1.5x -> right, one by one,
waits for the intro), headline underline + white-to-orange, dishes and logo bigger,
menu browser cut to one card per category (9 under All), ember field + two buttons on
the "One Kitchen, Two Fires" section, and the restaurant's own YouTube fire clip behind
the order band (lazy, muted, looping, embers as fallback).

**Decisions**
- Real video = the client's YouTube clip `94UkyRfa4rs` ("flame bg"), the same one the
  live site uses. Cannot be downloaded (YouTube terms, no ffmpeg here), so it is
  embedded via youtube-nocookie, only when the band is near the viewport.
- Hero animation moved from CSS keyframes to the Web Animations API: the "stop at the
  centre" distance differs per screen and must be measured at runtime.
- Nine unused menu images deleted after the browser was shortened.

**Verifying in the Claude desktop browser pane - lessons (cost real time today)**
- The pane tab is *hidden* during automation: requestAnimationFrame never fires,
  IntersectionObserver callbacks never fire, animation timelines freeze, and
  screenshots can time out or come back black.
- `scroll-behavior:smooth` overshoots to the page bottom there; set
  `documentElement.style.scrollBehavior='auto'` before measuring.
- Verify animations by pausing them and setting `currentTime` to a keyframe, then
  reading computed transforms / getBoundingClientRect. Chain steps with `finish()`.
- Anything gated on rAF/IO must be verified by exercising the same code manually.

**Still open (unchanged):** prices, two real reviews, About story, ordering provider,
contact form wiring. Account note: repo lives under `angel062388`.

**Stamps tried and removed (client call, 2026-09-18):** two red rubber stamps under the
hero dishes were pushed without a rendered look (the pane could not draw) and did not
suit the hero. Reverted in full. Lesson: no new visual element goes live unseen; if the
pane cannot render, ask the client to preview locally first.

**Stamps v2 (client asked again, with a reference):** small classic round stamps,
~110 px, one under each dish, land-triggered. Rendered look checked in the pane
before pushing this time.

**Later still:** stamps v3 (bigger, distressed), the client's steam clip as a section
with poster, and a 10-question FAQ with FAQPage schema. Temporary local receiver
(scratch/recv.py) used to save browser-captured frames to disk without routing the
data through the model; stop it after use. The pane cannot screenshot live video; swap
the poster in as a background to judge the section.
