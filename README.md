# North Shore Garage Doors — Website

Fast, mobile-first, conversion-focused 15-page microsite for a family-owned garage
door company serving **West Vancouver & the North Shore** (residential + strata).

## Tech
- **Static HTML / CSS / vanilla JS** — no build step. Deploys to Hostinger via Git.
- One JS dependency: **Motion** (CDN `+esm`) for scroll reveals. Everything else is vanilla.
- All imagery generated with Google **Gemini 2.5 Flash Image ("nano banana")**, optimized to WebP.

## Signature feature
A **scroll-driven "exploded view"** of a garage door (`assets/anim/door-00…08.webp`) scrubbed
on a `<canvas>` as you scroll the pinned "anatomy" section — assembles/disassembles with scroll.
Reduced-motion users get a static end-frame. See `assets/js/script.js` (`#anatomyStage`).

## Structure
```
index.html                 # home hub (hero, anatomy scroll-explode, services, pricing, springs,
                           #   openers, strata, about, areas, gallery, reviews, partner, FAQ, contact)
garage-door-repair.html spring-repair.html opener-installation.html new-garage-doors.html
cable-roller-repair.html maintenance-tune-up.html strata-townhomes.html      # 7 service pages
north-vancouver.html british-properties.html ambleside-dundarave.html
horseshoe-bay.html lions-bay-bowen-island.html                              # 5 area pages
become-a-partner.html thank-you.html 404.html
assets/css/style.css  assets/js/script.js  assets/js/motion.js
assets/img/  assets/anim/  og/home.jpg
robots.txt sitemap.xml site.webmanifest .htaccess site-config.json
scripts/   # image + page generators (NOT served; blocked by .htaccess)
```

## Build / regenerate
```bash
pip install Pillow                                   # (cwebp/ffmpeg not needed)
python3 scripts/to_webp.py                           # jpg/png -> responsive webp
GEMINI_API_KEY=... python3 scripts/gen_brand.py      # brand hero (desktop+mobile) + OG
GEMINI_API_KEY=... python3 scripts/gen_explode_frames.py   # the scroll-explode keyframes
pip install imageio-ffmpeg                            # bundled ffmpeg (no system install)
# densify keyframes for a buttery scrub:
ffmpeg -framerate 7 -i scratch/door-%02d.png \
  -vf "minterpolate=fps=32:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,scale=720:720" scratch/dense/d_%03d.png
GEMINI_API_KEY=... python3 scripts/gen_veo_explode.py   # OPTIONAL photoreal Veo 3.1 route (paid)
python3 scripts/content.py && python3 scripts/extra_pages.py   # (re)build all inner pages
```

The shipped hero uses 33 motion-interpolated WebP frames (`assets/anim/door-00…32.webp`, ~440 KB),
scrubbed with lerp smoothing + an LCP poster. `scripts/gen_veo_explode.py` is the optional
higher-fidelity Veo route — set `data-frames` in `index.html` to match the new frame count.

## Run locally
```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## Before go-live
1. **Replace placeholder phone** `(778) 800-0769` / `+17788000769` with the real local 604/778
   number (find/replace across all `*.html` and `assets/js/script.js`).
2. Wire forms to a backend (SMTP relay / Supabase / Formspree). They currently validate and
   fall back to `mailto:`. Partner + quote forms post to `info@northshoregaragedoors.ca`.
3. Add real Google Business Profile + social URLs (footer placeholders `#`).
4. Confirm canonical host in `.htaccess` (currently non-www → www).
