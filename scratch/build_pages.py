# -*- coding: utf-8 -*-
"""Generate about.html, contact.html and order.html from one shared shell."""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mockup")

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/logo.webp" type="image/webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<header class="header">
  <div class="wrap header__bar">
    <a class="header__logo" href="index.html">
      <img src="assets/logo.webp" alt="Skewer &amp; Slice">
      <span>Skewer &amp; Slice<small>Kabob &amp; Pizza</small></span>
    </a>
    <nav class="nav" id="nav" aria-label="Main">
      <a href="index.html"{a_home}>Home</a>
      <a href="menu.html"{a_menu}>Menu</a>
      <a href="about.html"{a_about}>About</a>
      <a href="contact.html"{a_contact}>Contact</a>
    </nav>
    <div class="header__actions">
      <a class="header__tel" href="tel:+17193686548">(719) 368-6548</a>
      <a class="btn btn-order btn-sm" href="order.html">Order Online</a>
    </div>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<main id="main">
  <section class="pagehead">
    <div class="embers">
      <div class="embers__still"></div>
      <canvas class="embers__canvas" aria-hidden="true"></canvas>
      <div class="embers__glow"></div>
      <div class="embers__scrim"></div>
    </div>
    <div class="wrap pagehead__inner">
      <p class="crumb"><a href="index.html">Home</a> &middot; {crumb}</p>
      <h1>{h1}</h1>
      <p>{lede}</p>
      <div class="hero__actions" style="margin-top:26px">
        <a class="btn btn-order btn-lg" href="order.html">Order Online</a>
        <a class="btn btn-ghost btn-lg" href="menu.html">See Our Menu</a>
      </div>
    </div>
  </section>
'''

FOOT = '''</main>

<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <div class="footer__logo"><img src="assets/logo.webp" alt="Skewer &amp; Slice"></div>
        <p style="color:var(--muted);max-width:290px">Afghan kabob and wood-fired pizza, served in Fountain, Colorado.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="menu.html">Menu</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Menu</h4>
        <ul>
          <li><a href="menu.html#kabobs">Kabobs</a></li>
          <li><a href="menu.html#pizza">Pizza</a></li>
          <li><a href="menu.html#wraps">Wraps</a></li>
          <li><a href="menu.html#desserts">Desserts</a></li>
        </ul>
      </div>
      <div>
        <h4>Visit</h4>
        <ul>
          <li>6970 Mesa Ridge Pkwy, Unit #130<br>Fountain, CO 80817</li>
          <li><a href="tel:+17193686548">(719) 368-6548</a></li>
          <li>Daily &middot; 11AM &ndash; 9PM</li>
        </ul>
        <a class="btn btn-order btn-sm" style="margin-top:16px" href="order.html">Order Online</a>
      </div>
    </div>
    <div class="footer__bottom">
      <span>&copy; <span data-year>2026</span> Skewer &amp; Slice. All rights reserved.</span>
      <span>6970 Mesa Ridge Pkwy, Unit #130, Fountain, CO 80817</span>
    </div>
  </div>
</footer>

<div class="orderbar" id="orderbar">
  <div class="orderbar__txt"><b>Open Daily 11AM &ndash; 9PM</b>Pickup on Mesa Ridge Pkwy</div>
  <a class="btn btn-order btn-sm" href="order.html">Order Online</a>
  <a class="btn btn-ghost btn-sm" href="https://maps.google.com/?q=6970+Mesa+Ridge+Pkwy+Unit+130,+Fountain,+CO+80817" target="_blank" rel="noopener">Directions</a>
</div>

<script src="assets/app.js"></script>
</body>
</html>
'''

CUR = ' aria-current="page"'

MAP_IFRAME = ('<iframe title="Map to Skewer &amp; Slice, 6970 Mesa Ridge Parkway, Fountain, Colorado" '
              'src="https://maps.google.com/maps?q=6970%20Mesa%20Ridge%20Pkwy%20Unit%20130%2C%20Fountain%2C%20CO%2080817'
              '&amp;t=m&amp;z=15&amp;output=embed&amp;iwloc=near" '
              'loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>')

DIRECTIONS = ('https://maps.google.com/?q=6970+Mesa+Ridge+Pkwy+Unit+130,+Fountain,+CO+80817')


def build(fn, title, desc, crumb, h1, lede, body, active):
    keys = {'a_home': '', 'a_menu': '', 'a_about': '', 'a_contact': ''}
    keys['a_' + active] = CUR
    html = HEAD.format(title=title, desc=desc, crumb=crumb, h1=h1, lede=lede, **keys) + body + FOOT
    path = os.path.join(OUT, fn)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', fn, len(html), 'bytes')


# ---------------------------------------------------------------- ABOUT
about_body = '''
  <section class="section">
    <div class="wrap">
      <div class="split" style="align-items:center">
        <div class="split__panel reveal">
          <img src="assets/k6-chopan-kabob.jpg" alt="Chopan lamb chop kabob over seasoned rice">
          <div class="split__copy">
            <h3>Two Fires</h3>
            <p>An open flame for the skewers, a wood oven for the pies.</p>
          </div>
        </div>
        <div class="reveal">
          <p class="eyebrow">Built Over Open Flame. No Compromise.</p>
          <h2 style="font-size:clamp(30px,4vw,46px);margin-bottom:18px">Forged In Fire. Made To Order.</h2>
          <p style="color:var(--muted)">
            Whether you are stopping in for a quick bite or sitting down for a full meal,
            every dish is crafted with precision, heat and purpose.
          </p>
          <p style="color:var(--muted)">
            Kabob plates come off the flame with seasoned rice, chickpeas, salad and
            homemade nan. Pizzas come out of the wood oven, including a chicken shawarma
            pie you will not find anywhere else in Fountain.
          </p>
          <div class="hero__actions" style="margin-top:24px">
            <a class="btn btn-order" href="order.html">Order Online</a>
            <a class="btn btn-ghost" href="menu.html">See Our Menu</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap">
      <div class="notice reveal">
        <b>Our story needs your words.</b> The current website does not publish the family
        background, how long the restaurant has been open, or what the &ldquo;Served with
        Honor&rdquo; line refers to. Nothing has been invented here. Send those details and
        this becomes the strongest page on the site.
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head center reveal">
        <p class="eyebrow">Find Us</p>
        <h2>Visit The Grill</h2>
      </div>
      <div class="visit">
        <div class="info-card reveal">
          <dl>
            <div class="info-row"><dt>Address</dt><dd>6970 Mesa Ridge Pkwy, Unit #130<br>Fountain, CO 80817</dd></div>
            <div class="info-row"><dt>Hours</dt><dd>Daily &middot; 11:00AM &ndash; 9:00PM</dd></div>
            <div class="info-row"><dt>Phone</dt><dd><a href="tel:+17193686548">(719) 368-6548</a></dd></div>
            <div class="info-row"><dt>Email</dt><dd><a href="mailto:info@skewerandslice.com">info@skewerandslice.com</a></dd></div>
          </dl>
          <div class="hero__actions" style="margin-top:26px">
            <a class="btn btn-order" href="order.html">Order Online</a>
            <a class="btn btn-ghost" href="DIRECTIONS_URL" target="_blank" rel="noopener">Get Directions</a>
          </div>
        </div>
        <div class="map reveal">MAP_IFRAME</div>
      </div>
    </div>
  </section>
'''

# ---------------------------------------------------------------- CONTACT
contact_body = '''
  <section class="section">
    <div class="wrap">
      <div class="visit">
        <div class="info-card reveal">
          <p class="eyebrow">Get In Touch</p>
          <h2 style="font-size:clamp(26px,3.2vw,36px);margin-bottom:20px">Reach Out</h2>
          <dl>
            <div class="info-row"><dt>Phone</dt><dd><a href="tel:+17193686548">(719) 368-6548</a></dd></div>
            <div class="info-row"><dt>Email</dt><dd><a href="mailto:info@skewerandslice.com">info@skewerandslice.com</a></dd></div>
            <div class="info-row"><dt>Address</dt><dd>6970 Mesa Ridge Pkwy, Unit #130<br>Fountain, CO 80817</dd></div>
            <div class="info-row"><dt>Hours</dt><dd>Daily &middot; 11:00AM &ndash; 9:00PM</dd></div>
          </dl>
          <div class="hero__actions" style="margin-top:26px">
            <a class="btn btn-order" href="order.html">Order Online</a>
            <a class="btn btn-ghost" href="DIRECTIONS_URL" target="_blank" rel="noopener">Get Directions</a>
          </div>
        </div>

        <div class="info-card reveal">
          <p class="eyebrow">Send A Message</p>
          <h2 style="font-size:clamp(26px,3.2vw,36px);margin-bottom:8px">Ask Us Anything</h2>
          <p style="color:var(--muted)">
            Got a question, an idea, or feedback? Fill this out and send it our way.
          </p>
          <form action="#" method="post" novalidate>
            <div class="field"><label for="cname">Full Name</label><input id="cname" name="name" type="text" autocomplete="name" required></div>
            <div class="field"><label for="cemail">Email</label><input id="cemail" name="email" type="email" autocomplete="email" required></div>
            <div class="field"><label for="cphone">Phone No.</label><input id="cphone" name="phone" type="tel" autocomplete="tel"></div>
            <div class="field"><label for="csubject">Subject</label><input id="csubject" name="subject" type="text"></div>
            <div class="field"><label for="cmsg">Message</label><textarea id="cmsg" name="message" required></textarea></div>
            <button class="btn btn-ghost btn-block" type="submit">Send Message</button>
          </form>
          <p style="color:var(--muted-2);font-size:14px;margin-top:14px">
            This form is not wired to an inbox yet. It needs connecting before launch.
          </p>
        </div>
      </div>

      <div class="map reveal" style="margin-top:26px">MAP_IFRAME</div>
    </div>
  </section>
'''

# ---------------------------------------------------------------- ORDER
order_body = '''
  <section class="section">
    <div class="wrap">

      <div class="notice reveal" style="margin-bottom:38px">
        <b>No ordering system is connected yet.</b> On the live site,
        <span style="color:var(--cream)">skewerandslice.com/order/</span> is an empty page, so
        every &ldquo;Order Online&rdquo; button currently leads nowhere. The panel below is where
        the ordering provider gets embedded. Until that is connected, phone orders are the only
        route that actually works.
      </div>

      <div class="visit">
        <div class="info-card reveal">
          <p class="eyebrow">Order For Pickup</p>
          <h2 style="font-size:clamp(26px,3.2vw,36px);margin-bottom:14px">Call It In</h2>
          <p style="color:var(--muted)">
            Orders are taken by phone during opening hours. Tell us what you want off the
            flame and we will have it ready.
          </p>
          <dl>
            <div class="info-row"><dt>Phone</dt><dd><a href="tel:+17193686548">(719) 368-6548</a></dd></div>
            <div class="info-row"><dt>Pickup</dt><dd>6970 Mesa Ridge Pkwy, Unit #130<br>Fountain, CO 80817</dd></div>
            <div class="info-row"><dt>Hours</dt><dd>Daily &middot; 11:00AM &ndash; 9:00PM</dd></div>
          </dl>
          <div class="hero__actions" style="margin-top:24px">
            <a class="btn btn-order btn-lg" href="tel:+17193686548">Call To Order</a>
            <a class="btn btn-ghost" href="menu.html">See Our Menu</a>
          </div>
        </div>

        <div class="info-card reveal" style="display:flex;flex-direction:column;justify-content:center;text-align:center">
          <p class="eyebrow" style="text-align:center">Online Ordering</p>
          <h2 style="font-size:clamp(24px,3vw,32px);margin-bottom:14px">Provider Embed Slot</h2>
          <p style="color:var(--muted)">
            Once a provider is chosen, its catalog, cart, pickup scheduling and checkout drop
            in here. Every &ldquo;Order Online&rdquo; button on the site already points at this
            page, so nothing else needs rewiring.
          </p>
          <div style="border:2px dashed var(--line);border-radius:var(--r-lg);padding:38px 20px;margin-top:18px;color:var(--muted-2)">
            Ordering widget goes here
          </div>
        </div>
      </div>

    </div>
  </section>
'''


def fix(s):
    return s.replace('MAP_IFRAME', MAP_IFRAME).replace('DIRECTIONS_URL', DIRECTIONS)


build('about.html',
      'About | Skewer &amp; Slice &mdash; Kabob &amp; Pizza, Fountain CO',
      'Built over open flame, no compromise. Afghan kabob and wood-fired pizza in Fountain, Colorado.',
      'About', 'About Us',
      'Built over open flame. No compromise.', fix(about_body), 'about')

build('contact.html',
      'Contact | Skewer &amp; Slice &mdash; Fountain, CO',
      'Call (719) 368-6548 or visit Skewer and Slice at 6970 Mesa Ridge Pkwy, Fountain, CO. Open daily 11AM to 9PM.',
      'Contact', 'Contact',
      'Open daily, 11AM to 9PM, on Mesa Ridge Parkway.', fix(contact_body), 'contact')

build('order.html',
      'Order Online | Skewer &amp; Slice &mdash; Fountain, CO',
      'Order kabob plates and wood-fired pizza from Skewer and Slice in Fountain, Colorado. Open daily 11AM to 9PM.',
      'Order', 'Order Online',
      'Kabob plates and wood-fired pizza, ready for pickup on Mesa Ridge Parkway.', fix(order_body), 'home')

print('done')
