# CLAUDE.md — West Vancouver Garage Doors (site-specific)

> The METHOD lives in `_shared/CLAUDE.md` + `_shared/FLEET-STANDARDS.md` (read those first,
> every session). This file holds the SPECIFICS. Facts also in `site-config.json`.

## This site
- **Town:** West Vancouver, BC (+ the North Shore)
- **Coverage model:** `single-town` (West Van + adjacent North Shore areas as their own pages)
- **Domain:** westvangaragedoors.ca · canonical host **www** · deploys to Hostinger via Git
- **Email:** info@westvangaragedoors.ca
- **Phone:** (604) 555-0199 — **PLACEHOLDER**, replace with the real local number before go-live
- **Emphasis:** residential + strata/townhome
- **Primary keyword:** West Vancouver garage door repair
- **Voice/angle:** premium-coastal, family-owned, calm and trustworthy (NOT a funny-brand site)
- **Palette:** navy `#0b2545` / `#13315c`, steel `#1d4e89`, gold `#e0a64e`
- **Fonts:** Plus Jakarta Sans (headings) / Inter (body)
- **Layout variant:** layout-A — full-bleed brand hero + signature **scroll "exploded view"** anatomy section

## Pages (15, flat structure)
Home + 7 services (repair, spring, opener, new-doors, cable-roller, maintenance, strata) +
5 areas (north-vancouver, british-properties, ambleside-dundarave, horseshoe-bay,
lions-bay-bowen-island) + become-a-partner, thank-you, 404.

## Fleet-standard compliance notes
- Prices = canonical fleet table, hidden by default, revealed by the footer **Show pricing**
  toggle (`[data-px]`). Springs $739 / $851 / $1,274. Openers 2220L…98022 ($1,311…$2,155).
- **NO** Review/AggregateRating schema. Schema = HomeAndConstructionBusiness + WebSite +
  FAQPage (+ Service/Breadcrumb on inner pages).
- Compliance wording: "Licensed (business licence), insured & WorkSafeBC-covered" — garage-door
  is an UNREGULATED trade in BC; never imply a trade certificate.
- Floating Call + **Text** bar on every page; dual mobile/desktop hero via `<picture>`.

## Regenerate / build (no build step at runtime)
See README.md → "Build / regenerate". Image tooling uses Pillow (no cwebp/ffmpeg in env).
Inner pages are emitted by `scripts/build_pages.py` + `content.py` + `extra_pages.py`.

## When done
Update `_shared/LESSONS.md`, `_shared/sites-registry.md`, promote reusables, commit + push
both this repo and `_shared` to branch `claude/relaxed-fermi-oqp52j`.
