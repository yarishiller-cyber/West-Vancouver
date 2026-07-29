#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate all inner pages (services, service areas, partner, thank-you, 404)
for North Shore Garage Doors from a shared shell + per-page content.

No build step at runtime — this just emits plain static .html files that match
index.html's header/footer/scripts. Re-run any time content changes.

  python3 scripts/build_pages.py

FLEET §0: every public URL is extensionless directory-style (/page/), assets are
root-absolute (/assets/...), and .htaccess maps /page/ -> page.html.
"""
import os, html
ROOT = os.path.join(os.path.dirname(__file__), "..")
PHONE = "(778) 800-0769"; TEL = "+17788000769"
SMS = "sms:+17788000769?&body=Hi%2C%20I'd%20like%20a%20garage%20door%20quote."
BASE = "https://www.northshoregaragedoors.ca"
DATE_MODIFIED = "2026-07-29"
FRESHNESS = "Updated July 2026"
OG_ALT = "North Shore Garage Doors — West Vancouver & the North Shore"

def page_url(slug):
    """Clean extensionless URL path for a flat .html slug (FLEET §0)."""
    if slug in ("", "index.html"):
        return "/"
    if "#" in slug:  # e.g. "index.html#contact" -> "/#contact"
        base, frag = slug.split("#", 1)
        return page_url(base) + "#" + frag
    if slug.endswith(".html"):
        return "/" + slug[:-5] + "/"
    return "/" + slug

def u(slug):
    return page_url(slug)

NAV = [("garage-door-repair.html","Repair"),("spring-repair.html","Springs"),
       ("opener-installation.html","Openers"),("new-garage-doors.html","New Doors"),
       ("strata-townhomes.html","Strata"),("service-areas.html","Areas"),
       ("index.html#reviews","Reviews")]

LOGO = ('<svg class="logo-mark" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
 '<rect x="2" y="2" width="44" height="44" rx="11" fill="#0b2545"/>'
 '<path d="M9 22 24 11l15 11v15a1 1 0 0 1-1 1H10a1 1 0 0 1-1-1V22Z" fill="#13315c"/>'
 '<path d="M9 22 24 11l15 11" stroke="#e0a64e" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
 '<rect x="14" y="24" width="20" height="14" rx="1.5" fill="#fff"/>'
 '<path d="M14 28h20M14 32h20M14 36h20M20 24v14M28 24v14" stroke="#cdd9ea" stroke-width="1.2"/>'
 '<rect x="14" y="24" width="20" height="14" rx="1.5" stroke="#e0a64e" stroke-width="1.6"/></svg>')
PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20 6 9 17l-5-5"/></svg>'

SPECULATION = ('<script type="speculationrules">{"prerender":[{"where":{"and":[{"href_matches":"/*"},'
 '{"not":{"href_matches":"/*.php"}},{"not":{"href_matches":"/thank-you*"}},'
 '{"not":{"href_matches":"/partner-thank-you*"}}]},"eagerness":"moderate"}]}</script>')

def head(title, desc, slug, ogimg=None, extra_ld="", noindex=False, hero_img=None):
    url = BASE + page_url(slug)
    # Per-page OG card if one exists; JPG-only guard (chat apps ignore webp).
    if ogimg is None:
        cand = "home" if slug == "index.html" else slug[:-5]
        ogimg = "og/%s.jpg" % cand if os.path.exists(os.path.join(ROOT, "og", cand + ".jpg")) else "og/home.jpg"
    if not ogimg.lower().endswith((".jpg", ".jpeg")):
        ogimg = "og/home.jpg"
    robots = '<meta name="robots" content="noindex, follow">\n' if noindex else ''
    canonical = '' if noindex else f'<link rel="canonical" href="{url}">\n'
    ogurl = '' if noindex else f'<meta property="og:url" content="{url}">\n'
    preload = f'<link rel="preload" as="image" href="/{hero_img}" fetchpriority="high">\n' if hero_img else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0b2545">
{robots}{canonical}<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="North Shore Garage Doors">
<meta property="og:locale" content="en_CA">
{ogurl}<meta property="og:image" content="{BASE}/{ogimg}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{OG_ALT}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}/{ogimg}">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon-48.png" sizes="48x48" type="image/png">
<link rel="icon" href="/assets/img/favicon-96.png" sizes="96x96" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css">
{preload}{extra_ld}
</head>
<body>'''

def header():
    nav = "".join(f'<a href="{u(h)}">{t}</a>' for h,t in NAV)
    drawer = "".join(f'<a class="mn-link" href="{u(h)}">{t}</a>' for h,t in [
        ("garage-door-repair.html","Garage Door Repair"),("spring-repair.html","Spring Replacement"),
        ("opener-installation.html","Openers &amp; Smart Control"),("new-garage-doors.html","New Door Installation"),
        ("cable-roller-repair.html","Cables, Rollers &amp; Tracks"),("maintenance-tune-up.html","Tune-Ups &amp; Maintenance"),
        ("strata-townhomes.html","Strata &amp; Townhomes"),("service-areas.html","Service Areas"),
        ("index.html#reviews","Reviews"),("become-a-partner.html","Become a Partner")])
    return f'''
<header class="header" id="header">
  <div class="container">
    <a href="/" class="brand" aria-label="North Shore Garage Doors home">{LOGO}
      <span class="brand-text"><b>North Shore</b><span>Garage Doors</span></span></a>
    <nav class="nav" aria-label="Primary">{nav}</nav>
    <div class="header-cta">
      <div class="header-phone"><small>Call for service</small><b>{PHONE}</b></div>
      <a href="/#contact" class="btn btn-primary">Free Quote</a>
      <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="overlay" id="overlay"></div>
<aside class="mobile-nav" id="mobileNav" aria-label="Mobile menu">
  <div class="mn-head"><b style="font-family:var(--font-head);color:var(--navy)">Menu</b>
    <button class="mn-close" id="mnClose" aria-label="Close menu">×</button></div>
  {drawer}
  <div class="mn-cta">
    <a href="tel:{TEL}" class="btn btn-call btn-block">Call {PHONE}</a>
    <a href="{SMS}" class="btn btn-text btn-block">Text Us</a>
    <a href="/#contact" class="btn btn-primary btn-block">Get a Free Quote</a>
  </div>
</aside>
<main id="top">'''

def page_hero(h1, sub, crumbs, img="assets/img/hero-brand-960.webp"):
    cr = ' &rsaquo; '.join(crumbs)
    return f'''
<section class="page-hero">
  <div class="hero-bg"><img src="/{img}" alt="" width="1600" height="900" fetchpriority="high"></div>
  <div class="container">
    <div class="breadcrumbs">{cr}</div>
    <h1>{h1}</h1>
    <p>{sub}</p>
    <div class="hero-actions">
      <a href="tel:{TEL}" class="btn btn-call btn-lg" data-hover-lift>{PHONE_SVG} Call {PHONE}</a>
      <a href="{SMS}" class="btn btn-outline-light btn-lg" data-hover-lift>Text Us</a>
    </div>
  </div>
</section>'''

def cta_band(title="Let's Get Your Garage Door Working Again",
             text="Same-day appointments are often available. Call now or request your free, no-obligation quote."):
    return f'''
<section class="cta-band">
  <div class="cta-bg"><img src="/assets/img/cta-bg.webp" alt="" loading="lazy" width="1600" height="900"></div>
  <div class="container">
    <span class="eyebrow center" style="color:var(--gold);justify-content:center">Ready when you are</span>
    <h2>{title}</h2><p>{text}</p>
    <div class="cta-actions">
      <a href="tel:{TEL}" class="btn btn-call btn-lg" data-hover-lift>{PHONE_SVG} Call {PHONE}</a>
      <a href="{SMS}" class="btn btn-outline-light btn-lg" data-hover-lift>Text Us</a>
    </div>
  </div>
</section>'''

def footer():
    return f'''
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col footer-about">
        <a href="/" class="brand" aria-label="North Shore Garage Doors">{LOGO}
          <span class="brand-text"><b>North Shore</b><span style="color:var(--gold)">Garage Doors</span></span></a>
        <p class="footer-about">Family-owned garage door repair, installation and strata service across West Vancouver and the North Shore. Quality work, honest prices, friendly faces.</p>
      </div>
      <div class="footer-col"><h4>Services</h4><ul>
        <li><a href="/garage-door-repair/">Garage Door Repair</a></li>
        <li><a href="/spring-repair/">Spring Replacement</a></li>
        <li><a href="/opener-installation/">Openers &amp; Smart Control</a></li>
        <li><a href="/new-garage-doors/">New Door Installation</a></li>
        <li><a href="/cable-roller-repair/">Cables &amp; Rollers</a></li>
        <li><a href="/maintenance-tune-up/">Tune-Ups &amp; Maintenance</a></li>
        <li><a href="/strata-townhomes/">Strata &amp; Townhomes</a></li></ul></div>
      <div class="footer-col"><h4>Service Areas</h4><ul>
        <li><a href="/">West Vancouver</a></li>
        <li><a href="/british-properties/">British Properties</a></li>
        <li><a href="/ambleside-dundarave/">Ambleside &amp; Dundarave</a></li>
        <li><a href="/horseshoe-bay/">Horseshoe Bay &amp; Caulfeild</a></li>
        <li><a href="/lions-bay-bowen-island/">Lions Bay &amp; Bowen Island</a></li>
        <li><a href="/north-vancouver/">North Vancouver</a></li></ul></div>
      <div class="footer-col"><h4>Contact</h4><ul class="footer-contact">
        <li>{PHONE_SVG} <a href="tel:{TEL}">{PHONE}</a></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/></svg> <a href="mailto:info@northshoregaragedoors.ca">info@northshoregaragedoors.ca</a></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg> Mon–Fri 7–7 · Sat–Sun 8–6</li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2 4 5v6c0 5 3.4 8.6 8 10 4.6-1.4 8-5 8-10V5l-8-3Z"/></svg> Licensed (business licence), insured &amp; WorkSafeBC</li></ul>
        <p style="margin-top:14px"><a href="/become-a-partner/" style="color:var(--gold);font-weight:700">Become a Partner →</a></p></div>
    </div>
    <div class="footer-bottom"><div class="container">
      <span>© <span id="year">2026</span> North Shore Garage Doors. All rights reserved.</span>
      <span class="fb-links">
        <button type="button" id="pricing-toggle" aria-pressed="false">Show pricing</button>
        <a href="/become-a-partner/">Partners</a><a href="/#reviews">Reviews</a><a href="/#contact">Contact</a>
      </span></div></div>
  </div>
</footer>
<div class="mobile-bar">
  <a href="tel:{TEL}" class="btn btn-call"><svg viewBox="0 0 24 24" width="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/></svg> Call Now</a>
  <a href="{SMS}" class="btn btn-text"><svg viewBox="0 0 24 24" width="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2Z"/></svg> Text Us</a>
</div>
<button class="to-top" id="toTop" aria-label="Back to top"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="m18 15-6-6-6 6"/></svg></button>
{SPECULATION}
<script src="/assets/js/script.js"></script>
<script type="module">
  import {{ animate, inView, scroll, stagger }} from "https://cdn.jsdelivr.net/npm/motion@latest/+esm";
  window.__motion = {{ animate, inView, scroll, stagger }};
  import("/assets/js/motion.js").then(m => m.initMotion());
</script>
</body>
</html>'''

def ld(*objs):
    import json
    graph = {"@context":"https://schema.org","@graph":list(objs)}
    return '<script type="application/ld+json">\n' + json.dumps(graph, indent=0) + '\n</script>'

def breadcrumb_ld(items):
    return {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":BASE+page_url(s)} for i,(n,s) in enumerate(items)]}

def offer(name, price=None, min_price=None):
    ps = {"@type":"PriceSpecification","priceCurrency":"CAD"}
    if price is not None: ps["price"] = price
    if min_price is not None: ps["minPrice"] = min_price
    return {"@type":"Offer","name":name,"priceSpecification":ps}

def service_ld(name, desc, slug, area="West Vancouver", offers=None):
    if isinstance(area, str):
        area_obj = {"@type":"City","name":area}
    else:
        area_obj = [{"@type":"City","name":a} for a in area]
    d = {"@type":"Service","name":name,"description":desc,"serviceType":name,
         "areaServed":area_obj,
         "provider":{"@id":BASE+"/#business"},
         "url":BASE+page_url(slug)}
    if offers: d["offers"] = offers
    return d

def webpage_ld(title, slug):
    url = BASE + page_url(slug)
    return {"@type":"WebPage","@id":url+"#webpage","url":url,"name":title,
            "dateModified":DATE_MODIFIED,"isPartOf":{"@id":BASE+"/#website"}}

def faq_ld(faqs):
    return {"@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}

def render_prose(sections):
    out=[]
    for sec in sections:
        kind=sec[0]
        if kind=="h2": out.append(f"<h2>{sec[1]}</h2>")
        elif kind=="h3": out.append(f"<h3>{sec[1]}</h3>")
        elif kind=="p": out.append(f"<p>{sec[1]}</p>")
        elif kind=="ul": out.append("<ul>"+"".join(f"<li>{x}</li>" for x in sec[1])+"</ul>")
    return "\n".join(out)

def faq_block(faqs):
    items="".join(
        f'<div class="faq-item"><button class="faq-q" aria-expanded="false">{q} '
        f'<span class="faq-icon"><svg viewBox="0 0 24 24" width="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg></span></button>'
        f'<div class="faq-a"><p>{a}</p></div></div>' for q,a in faqs)
    return f'<section class="section"><div class="container"><div class="center" style="margin-bottom:30px"><span class="eyebrow" data-reveal>Good to know</span><h2 class="section-title" data-reveal>Frequently Asked Questions</h2></div><div class="faq">{items}</div></div></section>'

def side_card(title, body, related):
    rl="".join(f'<a href="{u(s)}">{t}</a>' for t,s in related)
    return (f'<aside class="side-card"><h3>{title}</h3><p style="color:var(--slate);font-size:.95rem">{body}</p>'
            f'<a href="tel:{TEL}" class="btn btn-call btn-block" data-hover-lift>{PHONE_SVG} Call {PHONE}</a>'
            f'<a href="/#contact" class="btn btn-ghost btn-block" style="margin-top:10px">Request a Free Quote</a>'
            f'<div class="related-links">{rl}</div></aside>')

def write(slug, content):
    with open(os.path.join(ROOT, slug), "w") as f:
        f.write(content)
    print("wrote", slug)

# -------------------------------------------------------------------- SERVICE PAGES
def service_page(slug, title, desc, h1, sub, sections, faqs, related, freshness=FRESHNESS,
                 img="assets/img/hero-brand-960.webp", price_html="", offers=None):
    crumbs=["<a href='/'>Home</a>", h1]
    extra = ld(service_ld(h1.replace(" in West Vancouver",""), desc, slug, offers=offers),
               breadcrumb_ld([("Home","index.html"),(h1, slug)]),
               webpage_ld(title, slug),
               faq_ld(faqs))
    body = head(title, desc, slug, extra_ld=extra, hero_img=img) + header()
    body += page_hero(h1, sub, crumbs, img=img)
    body += f'''
<section class="section"><div class="container"><div class="two-col">
  <div class="prose">
    <p class="freshness"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg> {freshness}</p>
    {render_prose(sections)}
    {price_html}
  </div>
  {side_card("Need it fixed today?","Most repairs are same-day. Call or text the family directly — no call centres.",related)}
</div></div></section>'''
    body += faq_block(faqs) + cta_band() + footer()
    write(slug, body)

# -------------------------------------------------------------------- AREA PAGES
def area_page(slug, title, desc, h1, sub, sections, faqs, related,
              img="assets/img/hero-brand-960.webp", area="West Vancouver"):
    crumbs=["<a href='/'>Home</a>","<a href='/service-areas/'>Service Areas</a>", h1]
    extra = ld(service_ld("Garage Door Repair & Installation", desc, slug, area=area),
               breadcrumb_ld([("Home","index.html"),("Service Areas","service-areas.html"),(h1, slug)]),
               webpage_ld(title, slug),
               faq_ld(faqs))
    body = head(title, desc, slug, extra_ld=extra, hero_img=img) + header()
    body += page_hero(h1, sub, crumbs, img=img)
    body += f'''
<section class="section"><div class="container"><div class="two-col">
  <div class="prose">
    <p class="freshness"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg> {FRESHNESS}</p>
    {render_prose(sections)}
  </div>
  {side_card("Local & fast","Our trucks are stocked and on the North Shore daily, so help is never far away.",related)}
</div></div></section>'''
    body += faq_block(faqs) + cta_band() + footer()
    write(slug, body)

print("build_pages module loaded")
