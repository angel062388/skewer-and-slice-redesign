# Skewer &amp; Slice — website redesign

Static redesign mockup for **skewerandslice.com** (Afghan kabob &amp; wood-fired
pizza, Fountain, Colorado). Built as plain HTML/CSS/JS so it can be previewed
from any static host and handed to a developer without a build step.

**Client:** Skewer &amp; Slice · **Org:** Magister Digital AI

---

## Preview

**Live:** <https://angel062388.github.io/skewer-and-slice-redesign/>

Locally:

```bash
cd mockup && python -m http.server 8787
```

Then open <http://localhost:8787/index.html>.

---

## Pages

| File | Purpose |
|---|---|
| `mockup/index.html` | Home — intro, hero, menu browser, reviews, visit, order band |
| `mockup/menu.html` | Full menu, grouped exactly as the live site groups it |
| `mockup/about.html` | About |
| `mockup/contact.html` | Contact (correct Fountain CO map) |
| `mockup/order.html` | Order Online landing + provider embed slot |

---

## What was built to brief

**Intro (~5.5s, once per browser session)**
- Ember/flame field, logo at centre, tagline, and **Order Online** +
  **See Our Menu** at the bottom.
- Auto-exits, has a Skip control, a progress bar, and honours
  `prefers-reduced-motion`.

**Hero**
- Copy left, animated food right.
- The **BBQ plate flies in first at 350ms**, the **pizza follows at 1150ms** —
  an 800ms stagger. Both rotate-and-settle, then float gently.
- Modelled on the `pizza-flight-in` pattern from the Brooklyn Pizza reference.

**Menu browser** (replaces the live site's square "Browse our menu" boxes)
- All nine categories as rounded chips: Appetizers, Kabobs, Wraps, Specials,
  Pizza, Dessert, Sides, Ice Cream, Drinks — plus All.
- Filters in place; every card carries the same **Order Online** button.

**Scrolling ribbon**
- Restaurant's own wording only, with a **Pause motion** control.

---

## Design rules honoured

- **No sharp edges** — every box uses a `--r-*` radius token; buttons and chips
  are full pills. The only `border-radius:0` corners are edges flush to the
  viewport (skip link, mobile nav).
- **One CTA colour** — `--peach` (`#FFB177`, pastel orange) is reserved for
  **Order Online** and used nowhere else. Secondary actions (See Our Menu,
  Get Directions) are deliberately lower-contrast ghost buttons.
- **Ordering always reachable** — Order Online sits in the sticky header, and a
  sticky bottom bar appears once the hero scrolls away. It is a bar, not a
  popup: it never covers content and never interrupts.
- **Home** is a visible nav link on all five pages.
- **Contact**, never "Contact Us".
- **No cursive fonts** — display face is Oswald, body is Inter. Review text is
  explicitly pinned to the body face with `font-style:normal`.

---

## The flame

The live site's flame is a **YouTube embed** (`94UkyRfa4rs`), which cannot be
re-hosted or timed precisely. Instead the background is built from three layers:

1. `assets/embers.jpg` — the client's own licensed ember still, slowly drifting
2. a `<canvas>` ember particle system (`app.js`)
3. a flickering warm glow

No new licensing, no video encoding, and the intro timing is exact. It pauses
when off-screen or when the tab is hidden, and renders a still frame under
`prefers-reduced-motion`. Swapping in a real video later means replacing one
layer.

---

## Verification

```bash
python scratch/qc.py
```

Checks internal links, missing assets, dead anchors, and each client design
rule above. Last run: **11 passed, 0 failures**.

Also verified in-browser: all 5 pages return 200 with zero broken images, and
there is no horizontal scroll at 375px.

---

## Known gaps — these need client input, nothing has been invented

| Gap | Detail |
|---|---|
| **Prices** | The live site publishes none, so none are shown. |
| **Reviews** | One real Google review (Melanie V.) is used verbatim. Two slots are marked `data-placeholder` and must be filled with real reviews before launch. |
| **About story** | The live site publishes no family history or origin. |
| **Ordering** | No provider is connected — see below. |
| **Contact form** | Not wired to an inbox. |

## Bugs found on the live site

1. **`/order/` is an empty page.** Every "Order Online" button on the live site
   leads nowhere. This is the single biggest conversion problem.
2. **The Contact page map points to the London Eye**, London, UK — not
   6970 Mesa Ridge Pkwy. Corrected throughout this redesign.

## Added later the same day (2026-09-18)

- **Hero choreography (rebuilt in app.js):** each dish enters from the left, stops at the
  exact centre of the screen at 1.5x for a beat, then travels to its spot on the right.
  Strictly one after the other: BBQ plate, then pizza. Driven by the Web Animations API
  because "the centre" has to be measured per screen. Waits for the intro to leave, so
  first-time visitors actually see it. Fail-safe: if anything throws, the dishes appear
  in place.
- **Headline:** orange underline under "Open-Flame Kabob"; "Wood-Fired Pizza" warms from
  white to orange. Both trigger with the dishes.
- **Bigger:** dishes ~22% larger (403 / 461 px at 1440 wide), header logo 66 px.
- **Menu browser:** one representative card per category, nine under "All", each with
  Order Online and an "All ..." link into the full menu group. Far shorter page.
- **"One Kitchen, Two Fires":** ember field behind it, plus Order Online / See Our Menu.
- **Order band:** the restaurant's own YouTube fire clip (`94UkyRfa4rs`, titled
  "flame bg"), muted and looping, mounted only when the band is near the viewport,
  sized to cover. Embers stay underneath as the fallback (reduced motion, blocked
  embeds, slow connections). Nothing was downloaded; no new licence.

Verified by DOM and animation-API checks (exact centre, sequence, sizes, filters,
layer order, mobile overflow, console). The video mount is gated on
IntersectionObserver, which the automation pane does not deliver, so it was proven by
mounting the same iframe by hand (loads, covers). **Eyeball check:** scroll to the band on
the live page; the flames should fade in within about two seconds.
- **Small stamps under the dishes (v2):** two classic round stamps, about 110 px wide,
  in one warm ink colour: thick outer ring, thin inner ring, curved text top and bottom,
  bold word with stars in the middle (per the client's reference). "Built Over / Open
  Flame / No Compromise" beneath the BBQ plate and "Served With / Honor / Forged In
  Fire" beneath the pizza. Each slams down the moment its own dish lands. The first
  version (large, tilted band box) was removed after review; this one was seen
  rendered before it shipped.
