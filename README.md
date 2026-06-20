# North Shore Garage Doors — Website

A fast, mobile-first, SEO-optimized marketing website for a family-owned garage
door company serving **West Vancouver, North Vancouver and the North Shore** of
British Columbia. Residential and strata/townhome focus.

- **Live (GitHub Pages):** published automatically from `main` — see the Actions
  "Deploy site to GitHub Pages" run for the URL (e.g. `https://<owner>.github.io/<repo>/`).
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
Pushing to `main` triggers `.github/workflows/pages.yml`, which enables GitHub
Pages (first run) and deploys the site. The live URL appears in the workflow's
`github-pages` environment.

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
