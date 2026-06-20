# West Vancouver Garage Doors — Website

A fast, mobile-first, conversion-focused marketing website for a family-owned
garage door company serving West Vancouver and the North Shore. Residential and
strata/townhome focus.

## Tech
- Static **HTML / CSS / JS** — no build step, hosts anywhere (GitHub Pages, Netlify, Vercel, S3…).
- All imagery is original, generated with Google's **Gemini 2.5 Flash Image ("nano banana")**.

## Structure
```
index.html              # full single-page site
assets/css/style.css    # design system + components
assets/js/script.js     # nav, FAQ, opener toggle, scroll reveal, form
assets/img/             # generated imagery + favicon
scripts/gen_images.py   # image-generation pipeline (re-run to regenerate art)
robots.txt / sitemap.xml
```

## Run locally
```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Sections
Hero · Trust badges · Services · How it works (buyer journey) · Garage door
styles · LiftMaster openers (top 3 + full 7) · Spring options (3 tiers) ·
Strata & townhomes · About / family story · Service areas · Gallery · Reviews ·
CTA · FAQ · Contact form · Sticky mobile call bar.

## To do before going live
1. Replace placeholder phone **(604) 555-0199** and email **info@westvangaragedoors.ca**
   with real contact details (find/replace across `index.html`, `script.js`).
2. Connect the contact form to a backend (Formspree / Netlify Forms) — it
   currently validates and falls back to a `mailto:` link.
3. Add real Google review/business links and social URLs in the footer.
4. Regenerate imagery any time with: `GEMINI_API_KEY=... python3 scripts/gen_images.py --all --force`

## Regenerating images
```bash
export GEMINI_API_KEY="your-key"
python3 scripts/gen_images.py --all          # only missing
python3 scripts/gen_images.py hero-home --force
```
