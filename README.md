# North Shore Garage Doors — Website

A fast, mobile-first, SEO-optimized marketing website for a family-owned garage
door company serving **West Vancouver, North Vancouver and the North Shore** of
British Columbia. Residential and strata/townhome focus.

- **Instant live preview (no setup):** https://raw.githack.com/yarishiller-cyber/West-Vancouver/main/index.html
  (serves the public repo with correct content-types; relative assets resolve).
- **Production (GitHub Pages):** needs a one-time toggle — see "Publishing" below.
- **Intended domain:** https://www.northshoregaragedoors.ca/
- **Phone:** (778) 800-0769 · **Email:** info@NorthShoreGarageDoors.ca

## Tech
- Static **HTML / CSS / JS** — no build step.
- Imagery generated with Google **Gemini 2.5 Flash Image ("nano banana")**.

## Files
```
index.html              # full single-page site
privacy-policy.html     # PIPEDA/PIPA-aligned privacy policy
terms.html              # terms of service
assets/css/style.css    # design system + components
assets/js/script.js     # nav, FAQ, opener toggle, scroll reveal, form
assets/img/             # generated imagery + favicon
scripts/gen_images.py   # image-generation pipeline
robots.txt              # allows search engines + AI crawlers
sitemap.xml             # XML sitemap with image entries
llms.txt                # AI-assistant discoverability summary
site.webmanifest        # PWA manifest
.github/workflows/pages.yml  # auto-deploy to GitHub Pages on push to main
```

## SEO / discoverability
- Descriptive `<title>`, meta description, keywords, robots, geo meta tags.
- Open Graph + Twitter Card tags with absolute image URLs.
- Rich **JSON-LD `@graph`**: Organization, LocalBusiness/HomeAndConstructionBusiness
  (geo, opening hours, areaServed, services, aggregateRating + reviews), WebSite,
  BreadcrumbList, and FAQPage (eligible for FAQ rich results).
- `robots.txt` explicitly allows AI crawlers (GPTBot, ClaudeBot, PerplexityBot,
  Google-Extended, etc.) plus an `llms.txt` summary so AI assistants can find and
  cite the business.
- `sitemap.xml` referenced from `robots.txt`.

## Run locally
```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## Publishing
**One-time setup** (the automation token can't flip this for you): in the repo,
go to **Settings → Pages → Build and deployment → Source** and choose either:
- **"GitHub Actions"** (recommended) — then every push to `main` runs
  `.github/workflows/pages.yml` and deploys. Live URL:
  `https://yarishiller-cyber.github.io/West-Vancouver/`.
- **"Deploy from a branch" → `main` → `/ (root)`** — publishes the static files
  directly, no workflow needed.

Until then, use the instant **raw.githack** preview URL above to view the site.

### Point the custom domain (www.northshoregaragedoors.ca)
1. At your DNS provider for `northshoregaragedoors.ca`, add:
   - `CNAME` record: `www` → `<owner>.github.io`
   - Apex (`@`) `A` records to GitHub Pages: `185.199.108.153`, `185.199.109.153`,
     `185.199.110.153`, `185.199.111.153` (and the AAAA equivalents).
2. In the repo: **Settings → Pages → Custom domain**, enter
   `www.northshoregaragedoors.ca`, save, and enable "Enforce HTTPS".
   (This recreates the `CNAME` file in the repo.)

## Before going fully live
1. Replace the family-team / review copy with real names/photos as available.
2. Connect the contact form to a backend (Formspree / Netlify Forms) — it
   currently validates and falls back to a `mailto:` link.
3. Add real Google Business Profile + social URLs (footer + `sameAs` in JSON-LD).

## Regenerating images
```bash
export GEMINI_API_KEY="your-key"
python3 scripts/gen_images.py --all          # only missing
python3 scripts/gen_images.py hero-home --force
```
