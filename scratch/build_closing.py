# -*- coding: utf-8 -*-
"""Replace the home page order band with the winning mockup's "Made To Order" band.

Adapted from the "Skewer & Slice Version 3" artifact: same layout, side images,
eyebrow, slanted two-tone title, streak and copy -- with OUR buttons retained.
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MOCK = os.path.join(ROOT, "mockup")


def rw(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def wr(path, s):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(s)


# ------------------------------------------------------------------ index.html
p = os.path.join(MOCK, "index.html")
s = rw(p)
nl = "\r\n" if "\r\n" in s else "\n"
m = s.index('  <!-- ====================== ORDER BAND ====================== -->')
sec_start = s.index('<section class="section">', m)
sec_end = s.index('</section>', s.index('class="band reveal"', sec_start)) + len('</section>')

SECTION = [
    '  <!-- ====================== MADE TO ORDER ======================',
    '       Closing band from the winning "Version 3" mockup: cheese-pull',
    '       pizza left, flame-grilled skewers right, slanted two-tone title.',
    '       Our own buttons retained. The two side images came with that',
    '       mockup and have no confirmed licence (see README).',
    '       ============================================================ -->',
    '  <section class="section closing-fire" id="made-to-order" aria-labelledby="closing-title">',
    '    <div class="fire-art" aria-hidden="true">',
    '      <img class="fire-pizza" src="assets/closing-pizza.webp" alt="" width="356" height="941" loading="lazy" decoding="async">',
    '      <img class="fire-skewers" src="assets/closing-skewers.webp" alt="" width="459" height="941" loading="lazy" decoding="async">',
    '    </div>',
    '    <svg class="fire-defs" width="0" height="0" aria-hidden="true" focusable="false">',
    '      <filter id="brush-rough" x="-5%" y="-10%" width="110%" height="120%">',
    '        <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="7" result="n"/>',
    '        <feDisplacementMap in="SourceGraphic" in2="n" scale="4" xChannelSelector="R" yChannelSelector="G"/>',
    '      </filter>',
    '    </svg>',
    '    <div class="wrap reveal">',
    '      <p class="fire-eyebrow">Forged In Fire</p>',
    '      <h2 id="closing-title" class="fire-title"><span class="fire-made">Made To</span> <span class="fire-order">Order</span></h2>',
    '      <svg class="fire-streak" viewBox="0 0 400 24" preserveAspectRatio="none" aria-hidden="true" focusable="false">',
    '        <defs><linearGradient id="streak-grad" x1="0" x2="1"><stop offset="0" stop-color="#FFB177" stop-opacity="0"/><stop offset=".25" stop-color="#FFB177"/><stop offset="1" stop-color="#E4541B"/></linearGradient></defs>',
    '        <path d="M2 18 C 90 10, 220 6, 398 2 L 396 9 C 250 11, 120 16, 30 22 Z" fill="url(#streak-grad)"/>',
    '      </svg>',
    '      <p class="fire-copy">Whether you&rsquo;re stopping in for a quick bite or sitting down for a full meal, every dish is crafted with precision, heat and purpose.</p>',
    '      <div class="band__actions">',
    '        <a class="btn btn-order btn-lg" href="order.html">Order Online</a>',
    '        <a class="btn btn-ghost btn-lg" href="menu.html">See Our Menu</a>',
    '        <a class="btn btn-ghost btn-lg" href="https://maps.google.com/?q=6970+Mesa+Ridge+Pkwy+Unit+130,+Fountain,+CO+80817" target="_blank" rel="noopener">Get Directions</a>',
    '      </div>',
    '    </div>',
    '  </section>',
]
s = s[:m] + nl.join(SECTION) + s[sec_end:]
wr(p, s)
print("closing-fire sections:", s.count('closing-fire'),
      "| old band left:", s.count('class="band reveal"'),
      "| firevideo left:", s.count('class="firevideo"'))

# ------------------------------------------------------------------ styles.css
c = os.path.join(MOCK, "assets", "styles.css")
css = rw(c)
cnl = "\r\n" if "\r\n" in css else "\n"
BLOCK = """/* --------------------------------------------------------------------------
   Made To Order -- closing band from the winning "Version 3" mockup.
   Cheese-pull pizza left, flame-grilled skewers right, slanted two-tone
   title with a brush texture and an orange streak. Our buttons, unchanged.
   -------------------------------------------------------------------------- */
.closing-fire{
  position:relative; overflow:hidden; isolation:isolate; text-align:center;
  padding:64px 0 72px;
  background:radial-gradient(60% 55% at 50% 108%, rgba(228,84,27,.30), transparent 70%), #0A0706;
  border-top:1px solid var(--line);
}
.closing-fire .fire-art{ position:absolute; inset:0; z-index:-1; pointer-events:none; }
.closing-fire .fire-art img{
  position:absolute; top:0; height:100%; max-width:none; object-fit:cover;
  width:clamp(180px, calc((100% - 640px) / 2 + 90px), 460px);
}
.closing-fire .fire-pizza{
  left:0; object-position:40% center;
  -webkit-mask-image:linear-gradient(to right, #000 50%, transparent 100%);
          mask-image:linear-gradient(to right, #000 50%, transparent 100%);
}
.closing-fire .fire-skewers{
  right:0; object-position:60% center;
  -webkit-mask-image:linear-gradient(to left, #000 50%, transparent 100%);
          mask-image:linear-gradient(to left, #000 50%, transparent 100%);
}
.closing-fire .fire-art::after{
  content:""; position:absolute; inset:0;
  background:radial-gradient(34% 70% at 50% 50%, rgba(10,7,6,.92), rgba(10,7,6,.55) 70%, rgba(10,7,6,0) 100%);
}
.closing-fire .fire-defs{ position:absolute; width:0; height:0; overflow:hidden; }
.closing-fire .wrap{ position:relative; max-width:700px; }
.closing-fire .wrap::before{                 /* dark backing so the words stay legible over the food */
  content:""; position:absolute; inset:-48px -72px; z-index:-1; pointer-events:none;
  background:radial-gradient(closest-side, rgba(10,7,6,.88), rgba(10,7,6,.7) 65%, rgba(10,7,6,0));
}
.closing-fire .fire-eyebrow{
  display:inline-flex; align-items:center; gap:16px; margin:0 0 10px; padding-left:.42em;
  font-family:var(--font-display); font-weight:500; text-transform:uppercase;
  font-size:17px; letter-spacing:.42em; color:var(--cream);
  text-shadow:0 2px 10px rgba(0,0,0,.8);
}
.closing-fire .fire-eyebrow::before, .closing-fire .fire-eyebrow::after{
  content:""; width:46px; height:7px;
  background:linear-gradient(90deg, rgba(255,177,119,0), #FFB177 45%, #E4541B);
  clip-path:polygon(0 55%, 100% 0, 88% 100%);
}
.closing-fire .fire-eyebrow::after{ transform:scaleX(-1); }
.fire-title{
  display:flex; flex-direction:column; align-items:center;
  font-weight:700; line-height:.9; letter-spacing:.005em;
  transform:rotate(-4deg) skewX(-9deg);
  filter:url(#brush-rough) drop-shadow(0 6px 18px rgba(0,0,0,.75));
}
.fire-title .fire-made{
  font-size:clamp(38px,4.8vw,66px); margin-left:-.6em; color:#FF9A4A;
  background:linear-gradient(100deg, #FFB177 0%, #FF7A18 55%, #E4541B 100%);
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
}
.fire-title .fire-order{ font-size:clamp(64px,8.2vw,112px); margin-left:.5em; color:var(--cream); }
.fire-streak{ display:block; width:min(350px,66%); height:16px; margin:2px auto 0; transform:translateX(10%) rotate(-4deg); }
.closing-fire .fire-copy{ color:#E9E4DE; text-shadow:0 2px 12px rgba(0,0,0,.85); margin:16px auto 0; max-width:560px; }
.closing-fire .band__actions{ margin-top:26px; }
.closing-fire .btn-ghost{ background:rgba(10,7,6,.82); }
.closing-fire .btn-ghost:hover{ background:rgba(30,24,20,.9); }
@media (max-width:700px){
  .closing-fire{ padding:52px 0 60px; }
  .closing-fire .fire-art img{ width:58vw; height:62%; opacity:.75; }
  .closing-fire .fire-pizza{
    top:0; object-position:50% 30%;
    -webkit-mask-image:radial-gradient(90% 90% at 0 0, #000 35%, transparent 100%);
            mask-image:radial-gradient(90% 90% at 0 0, #000 35%, transparent 100%);
  }
  .closing-fire .fire-skewers{
    top:auto; bottom:0; object-position:50% 60%;
    -webkit-mask-image:radial-gradient(90% 90% at 100% 100%, #000 35%, transparent 100%);
            mask-image:radial-gradient(90% 90% at 100% 100%, #000 35%, transparent 100%);
  }
  .closing-fire .fire-art::after{ background:radial-gradient(80% 60% at 50% 50%, rgba(10,7,6,.9), rgba(10,7,6,.55) 80%, rgba(10,7,6,.25) 100%); }
  .closing-fire .fire-eyebrow{ font-size:14px; letter-spacing:.32em; padding-left:.32em; gap:10px; }
  .closing-fire .fire-eyebrow::before, .closing-fire .fire-eyebrow::after{ width:30px; }
}

""".replace("\n", cnl)
marker = "/* --------------------------------------------------------------------------" + cnl + "   Footer"
assert marker in css, "footer marker not found in styles.css"
if ".closing-fire{" not in css:
    css = css.replace(marker, BLOCK + marker, 1)
    wr(c, css)
print("css block present:", ".closing-fire{" in rw(c))

# ------------------------------------------------------------------ notes
with open(os.path.join(ROOT, "README.md"), "a", encoding="utf-8") as f:
    f.write("""
## Added 2026-09-24 -- the design won

- **"Made To Order" closing band** rebuilt from the winning "Skewer & Slice Version 3"
  mockup (claude.ai/artifact/1eJg5fS6LBVRjsxYcruWmp): cheese-pull pizza strip on the
  left, flame-grilled skewers on the right, eyebrow "Forged In Fire" with flame dashes,
  slanted two-tone title with a brush texture and an orange streak, our own buttons.
  The previous ember/YouTube band on the home page is gone.
- **Wording:** the mockup's eyebrow read "Forge in Fire"; the client's real motto is
  "Forged in Fire", so that is what ships.
- **Licence caveat carried over from the mockup:** the two side images
  (`assets/closing-pizza.webp`, `assets/closing-skewers.webp`) came with that mockup,
  look AI-generated or stock, are not the restaurant's dishes, and have no known
  licence. Confirm or replace before launch.
""")
with open(os.path.join(ROOT, "SESSION-NOTES.md"), "a", encoding="utf-8") as f:
    f.write("\n## 2026-09-24\n\nDesign won. Closing band replaced with the Version 3 mockup's "
            "'Made To Order' band (our buttons kept). Side images from the mockup: licence "
            "unconfirmed. Eyebrow uses 'Forged In Fire' (client's motto), not the mockup's "
            "'Forge in Fire'.\n")
print("README + notes updated")
