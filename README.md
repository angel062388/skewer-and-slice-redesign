# Skewer &amp; Slice — website redesign

Static redesign mockup for **skewerandslice.com** (Afghan kabob &amp; wood-fired
pizza, Fountain, Colorado). Built as plain HTML/CSS/JS so it can be previewed
from any static host and handed to a developer without a build step.

**Client:** Skewer &amp; Slice · **Org:** Magister Digital AI

---

## Preview

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
