#!/usr/bin/env python3
"""Static multi-page site generator for North Shore Garage Doors.

Builds index.html + a dedicated page for every nav/hamburger item, all sharing
one header / mobile drawer / footer so navigation stays consistent.
Run:  python3 scripts/build_site.py
"""
import os, json, datetime

ROOT = os.path.join(os.path.dirname(__file__), "..")
PHONE_DISPLAY = "(778) 800-0769"
TEL = "+17788000769"
EMAIL_DISPLAY = "info@NorthShoreGarageDoors.ca"
EMAIL = "info@northshoregaragedoors.ca"
SITE = "https://www.northshoregaragedoors.ca"
TODAY = datetime.date.today().isoformat()

# ---- nav model: (label, file, key) ----
NAV_MAIN = [
    ("Services", "services.html", "services"),
    ("Garage Doors", "garage-doors.html", "doors"),
    ("Openers", "openers.html", "openers"),
    ("Springs", "springs.html", "springs"),
    ("Strata", "strata.html", "strata"),
    ("About", "about.html", "about"),
    ("Reviews", "reviews.html", "reviews"),
]
NAV_MOBILE = [
    ("Services", "services.html", "services"),
    ("Garage Doors", "garage-doors.html", "doors"),
    ("Garage Door Openers", "openers.html", "openers"),
    ("Spring Replacement", "springs.html", "springs"),
    ("Strata &amp; Townhomes", "strata.html", "strata"),
    ("About Us", "about.html", "about"),
    ("Service Areas", "service-areas.html", "areas"),
    ("Reviews", "reviews.html", "reviews"),
    ("FAQ", "faq.html", "faq"),
]

# ---- inline SVG snippets ----
CHK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M20 6 9 17l-5-5"/></svg>'
ARR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M5 12h14M13 5l7 7-7 7"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92Z"/></svg>'
PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0Z"/><circle cx="12" cy="10" r="3"/></svg>'
SHIELD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2 4 5v6c0 5 3.4 8.6 8 10 4.6-1.4 8-5 8-10V5l-8-3Z"/></svg>'

LOGO = ('<svg class="logo-mark" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<rect x="2" y="2" width="44" height="44" rx="11" fill="#0b2545"/>'
        '<path d="M9 22 24 11l15 11v15a1 1 0 0 1-1 1H10a1 1 0 0 1-1-1V22Z" fill="#13315c"/>'
        '<path d="M9 22 24 11l15 11" stroke="#e0a64e" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
        '<rect x="14" y="24" width="20" height="14" rx="1.5" fill="#fff"/>'
        '<path d="M14 28h20M14 32h20M14 36h20M20 24v14M28 24v14" stroke="#cdd9ea" stroke-width="1.2"/>'
        '<rect x="14" y="24" width="20" height="14" rx="1.5" stroke="#e0a64e" stroke-width="1.6"/></svg>')


def li_check(text):
    return f'<li>{CHK} {text}</li>'


# ============================ shared chrome ============================
def head(title, desc, canonical, extra_schema=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#0b2545">
<meta name="geo.region" content="CA-BC">
<meta name="geo.placename" content="West Vancouver, North Vancouver, British Columbia">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="North Shore Garage Doors">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="en_CA">
<meta property="og:image" content="{SITE}/assets/img/hero-home.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/assets/img/hero-home.jpg">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/favicon.svg">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
{extra_schema}
</head>
<body>'''


def topbar():
    return f'''
<div class="topbar">
  <div class="container">
    <div class="topbar-areas"><span>★ Family-owned &amp; locally operated across the North Shore</span></div>
    <div><span class="dot">●</span> Same-day service &amp; emergency repairs — <a href="tel:{TEL}">{PHONE_DISPLAY}</a></div>
  </div>
</div>'''


def header(active):
    parts = []
    for lbl, f, k in NAV_MAIN:
        cls = ' class="is-active" aria-current="page"' if k == active else ''
        parts.append(f'<a href="{f}"{cls}>{lbl}</a>')
    links = "".join(parts)
    return f'''
<header class="header" id="header">
  <div class="container">
    <a href="index.html" class="brand" aria-label="North Shore Garage Doors home">
      {LOGO}
      <span class="brand-text"><b>North Shore</b><span>Garage Doors</span></span>
    </a>
    <nav class="nav" aria-label="Primary">{links}</nav>
    <div class="header-cta">
      <div class="header-phone"><small>Call for service</small><b>{PHONE_DISPLAY}</b></div>
      <a href="contact.html" class="btn btn-primary">Free Quote</a>
      <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>'''


def mobile_nav(active):
    links = "".join(
        f'<a class="mn-link{" is-active" if k==active else ""}" href="{f}">{lbl}</a>'
        for lbl, f, k in NAV_MOBILE)
    return f'''
<div class="overlay" id="overlay"></div>
<aside class="mobile-nav" id="mobileNav" aria-label="Mobile menu">
  <div class="mn-head">
    <b style="font-family:var(--disp);color:#fff">Menu</b>
    <button class="mn-close" id="mnClose" aria-label="Close menu">×</button>
  </div>
  {links}
  <div class="mn-cta">
    <a href="tel:{TEL}" class="btn btn-call btn-block">Call {PHONE_DISPLAY}</a>
    <a href="contact.html" class="btn btn-primary btn-block">Get a Free Quote</a>
  </div>
</aside>'''


def page_hero(eyebrow, h1, intro, crumb, show_cta=True, hero=None):
    cta = (f'<div class="hero-actions"><a href="tel:{TEL}" class="btn btn-gold btn-lg magnetic">{PHONE} Call {PHONE_DISPLAY}</a>'
           f'<a href="contact.html" class="btn btn-glass btn-lg">Get a Free Quote</a></div>') if show_cta else ""
    bg = (f'<div class="ph-bg"><picture><source media="(max-width:760px)" srcset="assets/img/{hero}-hero-mobile.jpg">'
          f'<img src="assets/img/{hero}-hero.jpg" alt="" fetchpriority="high"></picture></div>') if hero else ""
    return f'''
<section class="page-hero">
  {bg}
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span class="sep">›</span><span>{crumb}</span></nav>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p>{intro}</p>
    {cta}
  </div>
</section>'''


def cta_band():
    return f'''
<section class="cta-band">
  <div class="cta-bg"><img src="assets/img/cta-bg.jpg" alt=""></div>
  <div class="container">
    <span class="eyebrow center" style="color:var(--gold);justify-content:center">Ready when you are</span>
    <h2>Let's Get Your Garage Door Working Again</h2>
    <p>Same-day appointments are often available. Call now or request your free, no-obligation quote.</p>
    <div class="cta-actions">
      <a href="tel:{TEL}" class="btn btn-gold btn-lg magnetic">{PHONE} Call {PHONE_DISPLAY}</a>
      <a href="contact.html" class="btn btn-glass btn-lg">Request a Free Quote</a>
    </div>
  </div>
</section>'''


def trust_promise(bg=""):
    cards = [
        (SHIELD, "Workmanship Warranty", "Every repair and installation is backed by our warranty on parts and labour, plus the manufacturer's coverage on doors, openers and springs."),
        ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg>', "Flexible Financing", "Spread the cost of a beautiful new door or opener with simple financing options — just ask and we'll walk you through it."),
        ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.6 11.5 12 20l-7-7a4 4 0 0 1 5.7-5.7l1.3 1.3 1.3-1.3a4 4 0 0 1 5.7 5.7Z"/></svg>', "Honest, Upfront Pricing", "You approve a clear, all-in quote before any work begins. No hidden fees, no pressure, no surprises — ever."),
    ]
    grid = '<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr))">' + "".join(
        f'<div class="promise reveal"><span class="p-ico">{ic}</span><h3>{t}</h3><p>{d}</p></div>' for ic, t, d in cards) + '</div>'
    return section("Peace of mind", "Done right — and backed up.",
                   "Quality work you can trust, fair prices, and real guarantees behind every job.", grid, bg=bg)


def footer():
    return f'''
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col footer-about">
        <a href="index.html" class="brand" aria-label="North Shore Garage Doors">{LOGO}
          <span class="brand-text"><b>North Shore</b><span style="color:var(--gold)">Garage Doors</span></span></a>
        <p class="footer-about">Family-owned garage door repair, installation and strata service across West Vancouver, North Vancouver and the North Shore. Quality work, honest prices, friendly faces.</p>
        <div class="footer-social">
          <a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12Z"/></svg></a>
          <a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg></a>
        </div>
      </div>
      <div class="footer-col"><h4>Services</h4><ul>
        <li><a href="services.html">Garage Door Repair</a></li>
        <li><a href="springs.html">Spring Replacement</a></li>
        <li><a href="openers.html">Openers &amp; Smart Control</a></li>
        <li><a href="garage-doors.html">New Door Installation</a></li>
        <li><a href="services.html">Cables &amp; Rollers</a></li>
        <li><a href="strata.html">Strata &amp; Townhomes</a></li>
      </ul></div>
      <div class="footer-col"><h4>Company</h4><ul>
        <li><a href="about.html">About Us</a></li>
        <li><a href="service-areas.html">Service Areas</a></li>
        <li><a href="reviews.html">Reviews</a></li>
        <li><a href="faq.html">FAQ</a></li>
        <li><a href="contact.html">Contact</a></li>
        <li><a href="privacy-policy.html">Privacy Policy</a></li>
      </ul></div>
      <div class="footer-col"><h4>Contact</h4><ul class="footer-contact">
        <li>{PHONE} <a href="tel:{TEL}">{PHONE_DISPLAY}</a></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/></svg> <a href="mailto:{EMAIL}">{EMAIL_DISPLAY}</a></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg> Mon–Fri 7–7 · Sat–Sun 8–6</li>
        <li>{SHIELD} Licensed, insured &amp; WorkSafeBC</li>
      </ul></div>
    </div>
    <div class="footer-bottom"><div class="container">
      <span>© <span id="year">2026</span> North Shore Garage Doors. All rights reserved. Proudly serving West &amp; North Vancouver and the North Shore.</span>
      <span class="fb-links"><button class="price-toggle" id="priceToggle" aria-pressed="false">Show prices</button><a href="privacy-policy.html">Privacy Policy</a><a href="terms.html">Terms</a><a href="sitemap.xml">Sitemap</a><a href="contact.html">Contact</a></span>
    </div></div>
  </div>
</footer>'''


def chrome_end():
    return f'''
<div class="quotebar" id="quoteBar">
  <div class="container">
    <div class="qb-text"><b>Garage door trouble?</b> <span>Same-day service across the North Shore.</span></div>
    <div class="qb-cta">
      <a href="tel:{TEL}" class="btn btn-call">{PHONE} Call {PHONE_DISPLAY}</a>
      <a href="contact.html" class="btn btn-gold magnetic">Free Quote</a>
      <button class="qb-close" id="quoteBarClose" aria-label="Dismiss">×</button>
    </div>
  </div>
</div>
<div class="mobile-bar">
  <a href="tel:{TEL}" class="btn btn-call">{PHONE} Call Now</a>
  <a href="contact.html" class="btn btn-primary">Free Quote</a>
</div>
<button class="to-top" id="toTop" aria-label="Back to top"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="m18 15-6-6-6 6"/></svg></button>
<script src="assets/js/script.js"></script>
</body>
</html>'''


def assemble(active, head_html, body_html):
    return head_html + header(active) + mobile_nav(active) + "<main>" + body_html + "</main>" + cta_band() + footer() + chrome_end()


# ============================ content blocks ============================
def trust_strip():
    items = [
        (SHIELD, "Licensed &amp; Insured", "WorkSafeBC covered"),
        ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M2 12h4M18 12h4M5 5l3 3M16 16l3 3M19 5l-3 3M8 16l-3 3"/></svg>', "Same-Day Service", "7 days a week"),
        ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m12 2 2.4 7.4H22l-6 4.4 2.3 7.2L12 16.7 5.7 21l2.3-7.2-6-4.4h7.6L12 2Z"/></svg>', "4.9★ Rated", "237+ reviews"),
        ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9 12 3l9 6v11a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9Z"/><path d="M9 21v-6h6v6"/></svg>', "Family-Owned", "Local to the North Shore"),
        ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 1 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78Z"/></svg>', "Workmanship Warranty", "Parts &amp; labour"),
    ]
    cells = "".join(f'<div class="trust-item"><span class="ti-ico">{ic}</span><span>{t}<small>{s}</small></span></div>' for ic, t, s in items)
    return f'<div class="trust-strip"><div class="container">{cells}</div></div>'


SERVICES = [
    ("service-repair.jpg", "Garage Door Repair", "Off-track doors, broken cables, noisy operation, dented panels and doors that won't open or close — diagnosed and fixed fast.", "services.html", "Book a repair"),
    ("service-spring.jpg", "Spring Replacement", "Broken torsion or extension spring? It's our most common call. We carry high-cycle springs on every truck for a same-day fix.", "springs.html", "See spring options"),
    ("service-opener.jpg", "Openers &amp; Smart Control", "Authorized LiftMaster® dealer. Quiet belt-drive, wall-mount and Wi-Fi openers supplied, installed and repaired — with myQ® app control.", "openers.html", "Explore openers"),
    ("service-install.jpg", "New Door Installation", "Modern, carriage, full-view glass and insulated steel doors built for the West Coast climate. Expert measure, supply and install.", "garage-doors.html", "Browse door styles"),
    ("service-cable.jpg", "Cables, Rollers &amp; Tracks", "Frayed cables, worn nylon rollers, bent tracks and loose hardware — replaced with quality parts so your door glides quietly again.", "contact.html", "Get it fixed"),
    ("service-maintenance.jpg", "Tune-Ups &amp; Maintenance", "A 25-point safety inspection: balance, lubrication, alignment and sensor testing to prevent breakdowns and extend your door's life.", "contact.html", "Book a tune-up"),
]
SERVICE_ICONS = [
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.1 2.1-2.1-.6-.6-2.1 2.1-2.1Z"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7c4-4 12-4 16 0M5 11c3.5-3 10.5-3 14 0M6 15c3-2.5 9-2.5 12 0M8 19c2-1.5 6-1.5 8 0"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="8" width="18" height="9" rx="2"/><path d="M7 8V6a5 5 0 0 1 10 0v2M12 12v2"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9 12 3l9 6v11a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9Z"/><path d="M3 9h18M8 22V13h8v9M8 17h8"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="6" cy="6" r="3"/><circle cx="18" cy="18" r="3"/><path d="M6 9v6a3 3 0 0 0 3 3h6"/></svg>',
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.1 2.1-2.1-.6-.6-2.1 2.1-2.1Z"/></svg>',
]


def services_grid():
    cards = ""
    for i, (img, title, body, link, cta) in enumerate(SERVICES):
        cards += f'''
      <article class="service-card reveal">
        <div class="sc-img"><img src="assets/img/{img}" alt="{title} on the North Shore" loading="lazy"><span class="sc-ico">{SERVICE_ICONS[i]}</span></div>
        <div class="sc-body"><h3>{title}</h3><p>{body}</p><a class="sc-link" href="{link}">{cta} {ARR}</a></div>
      </article>'''
    return f'<div class="grid services-grid">{cards}</div>'


def steps_section():
    steps = [
        ("Call or Book Online", "Tell us what's happening. We'll book a visit that fits your day — often same-day."),
        ("Free Diagnosis &amp; Quote", "We inspect, explain the issue in plain language and give you an upfront, all-in price."),
        ("We Fix It Right", "Most repairs are completed on the spot with quality parts stocked on our trucks."),
        ("Enjoy the Warranty", "Drive away happy, backed by our workmanship warranty on parts and labour."),
    ]
    cells = "".join(f'<div class="step reveal"><div class="step-num">{i+1}</div><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(steps))
    return f'''
<section class="section bg-cloud">
  <div class="container">
    <div class="center" style="margin-bottom:46px"><span class="eyebrow">Simple &amp; stress-free</span>
      <h2 class="section-title">Getting Your Garage Door Fixed Is Easy</h2>
      <p class="section-intro">No pushy sales, no guesswork. Just a friendly local team and a clear path from problem to solved.</p></div>
    <div class="grid steps">{cells}</div>
  </div>
</section>'''


DOORS = [
    ("door-modern.jpg", "Modern Full-View", "Aluminum &amp; glass"),
    ("door-carriage.jpg", "Carriage House", "Timeless wood-grain charm"),
    ("door-traditional.jpg", "Traditional Steel", "Classic raised-panel"),
    ("door-flush.jpg", "Contemporary Flush", "Clean, minimal lines"),
]


def doors_grid():
    cards = "".join(
        f'<a href="contact.html" class="door-card reveal"><div class="dc-img"><img src="assets/img/{img}" alt="{t} garage door" loading="lazy"></div><div class="dc-cap"><b>{t}</b><span>{s}</span></div></a>'
        for img, t, s in DOORS)
    return f'<div class="grid doors-grid">{cards}</div>'


def opener_card(featured, badge, model, name, feats, btn_dark=True):
    badge_html = f'<span class="opener-badge">{badge}</span>' if featured else (f'<span class="opener-tag">{badge}</span>' if badge else "")
    img = "opener-belt.jpg"
    if "Wall" in name:
        img = "opener-wallmount.jpg"
    elif "Chain" in name:
        img = "opener-chain.jpg"
    lis = "".join(f'<li>{CHK} {f}</li>' for f in feats)
    btn = "btn-primary" if featured else ("btn-dark" if btn_dark else "btn-dark")
    return f'''<article class="opener-card{" featured" if featured else ""}">
        <div class="oc-img">{badge_html}<img src="assets/img/{img}" alt="LiftMaster {model} opener"></div>
        <div class="oc-body"><span class="oc-model">LiftMaster {model}</span><h3>{name}</h3><ul>{lis}</ul>
        <a href="contact.html" class="btn {btn} btn-block">Get This Opener</a></div></article>'''


def openers_block():
    top = (
        opener_card(True, "Most Popular", "84505R", "Secure View™ Belt Drive",
                    ["Ultra-quiet belt drive — great for rooms above the garage", "Built-in 140° HD camera &amp; two-way talk", "Wi-Fi + myQ® app, dual LED lighting"]) +
        opener_card(False, "Best Value", "8160W", "Ultra-Quiet Belt Drive",
                    ["Smooth, quiet DC belt-drive operation", "Wi-Fi &amp; myQ® smartphone control built in", "Reliable everyday performance, excellent price"]) +
        opener_card(False, "Space Saver", "8500W", "Elite Wall-Mount",
                    ["Mounts beside the door — frees your ceiling", "Perfect for tall, cathedral or heavy doors", "Battery backup, auto-lock &amp; Wi-Fi included"])
    )
    more = (
        opener_card(False, "", "8165W", "Durable Chain Drive",
                    ["Rugged ¾-HP chain-drive strength", "Dependable workhorse for detached garages", "Wi-Fi &amp; myQ® compatible"]) +
        opener_card(False, "", "8365-267", "Contractor Chain Drive",
                    ["Proven, budget-friendly ½-HP opener", "Simple, reliable daily operation", "Wi-Fi enabled with myQ® control"]) +
        opener_card(False, "", "8550WLB", "Battery-Backup Belt Drive",
                    ["Keeps working through power outages", "Quiet DC belt drive with soft start/stop", "Integrated battery, Wi-Fi &amp; myQ®"]) +
        opener_card(False, "", "87802", "Secure View™ with Camera",
                    ["Belt drive with integrated HD camera", "Watch &amp; talk from anywhere in the myQ® app", "Corner-to-corner LED lighting"])
    )
    return f'''
    <div class="grid opener-grid">{top}</div>
    <div class="grid opener-grid opener-more" id="openerMore">{more}</div>
    <div class="opener-toggle-wrap">
      <button class="btn btn-ghost btn-lg" id="openerToggle" aria-expanded="false" aria-controls="openerMore">
        <span class="ot-text">Show all 7 openers</span>
        <svg class="ot-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" style="transition:transform .25s"><path d="m6 9 6 6 6-6"/></svg>
      </button>
    </div>'''


GIFT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M5 12v9h14v-9M12 8S11 3 8 3a2.5 2.5 0 0 0 0 5h4Zm0 0s1-5 4-5a2.5 2.5 0 0 1 0 5h-4Z"/></svg>'

def spring_card(popular, name, img, price, sub, feats, free_cables=False, extras=None, btn="Choose this option"):
    pop = '<span class="spring-pop">Most Popular</span>' if popular else ""
    lis = "".join(f'<li>{CHK} {f}</li>' for f in feats)
    btncls = "btn-primary" if popular else "btn-ghost"
    fc = f'<div class="free-cables">{CHK} FREE cable replacement included</div>' if free_cables else ""
    ex = ""
    if extras:
        ex = '<ul class="sp-extras">' + "".join(f'<li>{GIFT} {e}</li>' for e in extras) + '</ul>'
    price_html = f'<div class="sp-price price-tag"><span>from</span><b>${price}</b></div>'
    return f'''<article class="spring-card{" popular" if popular else ""} reveal">{pop}
      <div class="sp-img"><img src="assets/img/{img}" alt="{name}"></div>
      <div class="sp-body"><h3>{name}</h3>{price_html}<div class="sp-life">{sub}</div>
      {fc}{ex}
      <ul>{lis}</ul>
      <a href="contact.html" class="btn {btncls} btn-block">{btn}</a></div></article>'''


def springs_block():
    cards = (
        spring_card(False, "Single Spring", "spring-single.jpg", "730", "For single-spring garage doors",
                    ["One broken torsion spring replaced", "High-cycle steel for a long, quiet life",
                     "Same-day replacement on most doors", "Backed by our workmanship warranty"],
                    free_cables=False, extras=None, btn="Book single spring") +
        spring_card(True, "Two Springs", "spring-double.jpg", "849", "Both springs replaced — our best value",
                    ["For standard two-spring doors", "We replace both so they wear evenly and last longer",
                     "Same-day replacement on most doors", "Backed by our workmanship warranty"],
                    free_cables=True,
                    extras=["15% off your springs when you refer a friend",
                            "15% off a new opener or garage door install"],
                    btn="Choose two springs") +
        spring_card(False, "Premium — 2 Extra-Long-Life Springs", "spring-premium.jpg", "1300",
                    "Our longest-lasting, heaviest-duty springs",
                    ["Two premium extra-high-cycle springs (red-sleeved)", "Built for busy households and coastal salt air",
                     "The last springs you'll likely ever need", "Backed by our workmanship warranty"],
                    free_cables=True, extras=None, btn="Choose premium")
    )
    return (f'<div class="grid spring-grid">{cards}</div>'
            '<p class="center price-hint">🔒 Prices are tucked away by default — tap <b>"Show prices"</b> at the very bottom of the page to reveal them.</p>'
            '<p class="center" style="margin-top:10px;color:var(--slate);font-size:.92rem">⚠️ Garage door springs are under extreme tension. Please leave replacement to our trained technicians — never attempt it yourself.</p>')


AREAS = ["West Vancouver", "British Properties", "Ambleside", "Dundarave", "Caulfeild", "Horseshoe Bay",
         "Lions Bay", "Bowen Island", "North Vancouver", "Lynn Valley", "Deep Cove", "Capilano"]


def areas_list():
    return '<ul class="areas-list">' + "".join(f'<li>{PIN} {a}</li>' for a in AREAS) + '</ul>'


REVIEWS = [
    ("SM", "Sarah M.", "Dundarave", "Our spring snapped on a Sunday morning and they were here within two hours. Friendly, tidy, and the price was exactly what they quoted. Couldn't ask for more."),
    ("DK", "David K.", "Strata Manager", "As a property manager I rely on them for several strata buildings. Always responsive, professional, and their invoicing makes my job easy. Highly recommend."),
    ("JL", "Jennifer L.", "British Properties", "They installed a gorgeous new modern door and a quiet LiftMaster opener. The transformation to our home's curb appeal is incredible. True professionals."),
    ("RP", "Robert P.", "Ambleside", "Honest and knowledgeable. They could have sold me a whole new door but instead fixed the cables and tuned everything up for a fraction of the cost."),
    ("AC", "Amanda C.", "Caulfeild", "From the first phone call to the finished job, everything was smooth. You can tell it's a family business that genuinely cares. Our go-to from now on."),
    ("MT", "Michael T.", "Horseshoe Bay", "Quiet, fast, and respectful of our home. The new belt-drive opener with the app is fantastic. Wish we'd called them years ago."),
    ("PN", "Priya N.", "North Vancouver", "Booked online in the evening, fixed by lunch the next day. They replaced both springs and the cables and explained exactly why. No upsell, no nonsense."),
    ("GC", "Strata Council", "Lynn Valley", "Our parkade gate failed on a long weekend and they had it secured within the hour. Their maintenance plan has saved our building several emergency call-outs since."),
]


def reviews_grid(n=6):
    cards = ""
    for av, name, where, text in REVIEWS[:n]:
        cards += f'''<article class="review reveal"><div class="stars">★★★★★</div><p>"{text}"</p>
        <div class="rv-author"><span class="rv-avatar">{av}</span><div><b>{name}</b><small>{where}</small></div><span class="rv-where">Google</span></div></article>'''
    return f'<div class="grid reviews-grid">{cards}</div>'


FAQS = [
    ("Do you offer same-day garage door repair?", "Yes. Most repairs — including broken springs, cables and openers — are completed the same day. Our trucks are stocked with the most common parts so we can fix it on the first visit whenever possible."),
    ("My spring broke — can I still use my door?", "Please don't. A door with a broken spring is extremely heavy and can fall unexpectedly. Avoid forcing it open, and give us a call — spring replacement is our most common same-day service."),
    ("Do you work with strata corporations and property managers?", "Absolutely — it's a big part of what we do. We provide scheduled maintenance, priority response, matching doors and hardware across units, and clear documentation, quotes and consolidated invoicing for councils and managers."),
    ("Which garage door opener brand do you install?", "We're an authorized LiftMaster® dealer and install their full residential lineup — quiet belt-drive, durable chain-drive and space-saving wall-mount models, all with Wi-Fi and myQ® smartphone control. We also repair most existing opener brands."),
    ("How long does a new garage door installation take?", "Most single or double-door installations are completed in a few hours. We'll remove your old door, install the new one, set up the opener and walk you through everything before we leave."),
    ("How much does garage door repair cost?", "It depends on the part and the work involved, but we always give you a clear, all-in price before we start — no hidden fees or surprise charges. Many common repairs are surprisingly affordable."),
    ("Do you charge for a quote?", "Quotes for new doors and installations are free. For repairs we diagnose the issue on-site and give you an upfront price before any work begins, so you're always in control."),
    ("Is your work guaranteed?", "Yes. All of our work is backed by a workmanship warranty on parts and labour, plus the manufacturer's warranty on doors, openers and springs. We stand behind every job."),
    ("Should I replace one spring or both?", "If your door uses two springs and one breaks, we usually recommend replacing both — the second is the same age and typically fails soon after. Our two-spring and premium options also include free cable replacement, since cables wear at the same time."),
    ("Do you offer financing?", "Yes — for larger jobs like a new door or opener, we offer simple financing options to spread the cost. Just ask when you book and we'll walk you through it."),
]


def faq_accordion(faqs):
    items = ""
    for q, a in faqs:
        items += f'''<div class="faq-item"><button class="faq-q">{q} <span class="faq-icon"><svg viewBox="0 0 24 24" width="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg></span></button><div class="faq-a"><p>{a}</p></div></div>'''
    return f'<div class="faq">{items}</div>'


def contact_block():
    return f'''
  <div class="contact-grid">
    <div class="contact-info reveal">
      <h3>Talk to a real local person</h3>
      <p style="color:var(--slate)">No call centres, no runaround. Reach the family directly:</p>
      <ul class="contact-list">
        <li><span class="ci-ico">{PHONE}</span><div><small>Phone</small><b><a href="tel:{TEL}">{PHONE_DISPLAY}</a></b></div></li>
        <li><span class="ci-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/></svg></span><div><small>Email</small><b><a href="mailto:{EMAIL}">{EMAIL_DISPLAY}</a></b></div></li>
        <li><span class="ci-ico">{PIN}</span><div><small>Service area</small><b>West Vancouver &amp; the North Shore</b></div></li>
      </ul>
      <div class="hours-card"><h4>Hours</h4>
        <div class="hrow"><span>Monday – Friday</span><b>7:00 AM – 7:00 PM</b></div>
        <div class="hrow"><span>Saturday – Sunday</span><b>8:00 AM – 6:00 PM</b></div>
        <div class="emergency-tag"><svg viewBox="0 0 24 24" width="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8Z"/></svg> Emergency service available</div>
      </div>
    </div>
    <div class="form-card reveal">
      <h3>Send us a message</h3>
      <p>Fill out the form below for your free, no-obligation quote.</p>
      <form id="quoteForm" action="https://formsubmit.co/{EMAIL}" method="POST" novalidate>
        <input type="hidden" name="_subject" value="New quote request — North Shore Garage Doors website">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" id="f-company" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
        <div class="form-row two">
          <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" type="text" placeholder="Your name" required></div>
          <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" placeholder="(778) 000-0000" required></div>
        </div>
        <div class="form-row two">
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" placeholder="you@email.com"></div>
          <div class="field"><label for="f-service">Service needed</label>
            <select id="f-service" name="service"><option value="">Select a service…</option>
              <option>Garage door repair</option><option>Spring replacement</option><option>Opener repair or installation</option>
              <option>New door installation</option><option>Cable / roller / track repair</option><option>Maintenance &amp; tune-up</option>
              <option>Strata / townhome service</option><option>Something else</option></select></div>
        </div>
        <div class="form-row"><div class="field"><label for="f-msg">How can we help?</label><textarea id="f-msg" name="message" placeholder="Tell us a bit about your garage door…"></textarea></div></div>
        <button type="submit" class="btn btn-primary btn-block btn-lg">Get My Free Quote</button>
        <p class="form-note">Or call us directly at <a href="tel:{TEL}" style="color:var(--steel);font-weight:700">{PHONE_DISPLAY}</a> — we'd love to help.</p>
      </form>
      <div class="form-success" id="formSuccess">✅ Thanks! Your request has been received. We'll call you back shortly — for urgent issues, please call {PHONE_DISPLAY}.</div>
    </div>
  </div>'''


def section(eyebrow, title, intro, inner, bg="", center=True):
    head_html = ""
    if title:
        ttl = f'<h2 class="section-title">{title}</h2>' if title else ""
        intro_html = f'<p class="section-intro">{intro}</p>' if intro else ""
        eb = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
        wrap = ' class="center" style="margin-bottom:46px"' if center else ' style="margin-bottom:30px"'
        head_html = f'<div{wrap}>{eb}{ttl}{intro_html}</div>'
    cls = "section" + (" bg-cloud" if bg == "cloud" else "")
    return f'<section class="{cls}"><div class="container">{head_html}{inner}</div></section>'


def before_after(bg=""):
    slides = [
        ("ba1", "Modern", "After — a brand-new modern charcoal garage door installed by North Shore Garage Doors", "Before — a worn, faded, dated beige garage door"),
        ("ba2", "Carriage", "After — a new wood-grain carriage-house garage door with windows", "Before — an old, plain, faded white garage door"),
    ]
    tabs = '<div class="ba-tabs" role="tablist">' + "".join(
        f'<button class="ba-tab{" is-on" if i == 0 else ""}" data-ba="{i}" role="tab" aria-selected="{"true" if i == 0 else "false"}">{label}</button>'
        for i, (key, label, aa, bb) in enumerate(slides)) + '</div>'
    stage = ""
    for i, (key, label, aa, bb) in enumerate(slides):
        hid = "" if i == 0 else " hidden"
        stage += f'''<div class="ba-compare" data-slide="{i}"{hid} aria-label="Before and after — {label}">
        <img class="ba-img ba-base" src="assets/img/{key}-after.jpg" alt="{aa}">
        <img class="ba-img ba-top" src="assets/img/{key}-before.jpg" alt="{bb}">
        <span class="ba-tag ba-tag-b">Before</span><span class="ba-tag ba-tag-a">After</span>
        <div class="ba-handle" role="slider" aria-label="Drag to compare before and after" tabindex="0" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">
          <span class="knob"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="m9 7-5 5 5 5M15 7l5 5-5 5"/></svg></span>
        </div></div>'''
    inner = (tabs + f'<div class="ba-stage reveal">{stage}</div>'
             + '<div class="center" style="margin-top:30px"><a href="contact.html" class="btn btn-gold btn-lg magnetic">Transform my garage</a></div>')
    return section("See the difference", "The same garage, transformed.",
                   "Pick a style, then drag the slider — watch a tired old door become a stunning new one. Real North Shore transformations.",
                   inner, bg=bg)


# ============================ schema helpers ============================
def breadcrumb_schema(name, url):
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": url}]}
    return '<script type="application/ld+json">' + json.dumps(data) + '</script>'


def service_schema(name, desc, url):
    data = {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc,
            "serviceType": name, "url": url, "areaServed": [{"@type": "City", "name": a} for a in ["West Vancouver", "North Vancouver"]],
            "provider": {"@type": "LocalBusiness", "name": "North Shore Garage Doors", "telephone": TEL, "email": EMAIL,
                         "areaServed": "North Shore, BC", "url": SITE + "/"}}
    return '<script type="application/ld+json">' + json.dumps(data) + '</script>'


def faq_schema(faqs):
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    return '<script type="application/ld+json">' + json.dumps(data) + '</script>'


HOME_SCHEMA = '<script type="application/ld+json">' + json.dumps({
    "@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": SITE + "/#organization", "name": "North Shore Garage Doors", "url": SITE + "/",
         "logo": SITE + "/assets/img/favicon.svg", "image": SITE + "/assets/img/hero-home.jpg", "email": EMAIL, "telephone": TEL, "sameAs": []},
        {"@type": ["LocalBusiness", "HomeAndConstructionBusiness", "GeneralContractor"], "@id": SITE + "/#business",
         "name": "North Shore Garage Doors", "url": SITE + "/", "image": SITE + "/assets/img/hero-home.jpg",
         "logo": SITE + "/assets/img/favicon.svg", "telephone": TEL, "email": EMAIL, "priceRange": "$$",
         "currenciesAccepted": "CAD", "paymentAccepted": "Cash, Credit Card, Debit, e-Transfer",
         "description": "Family-owned garage door repair, spring and opener replacement, and new door installation serving West Vancouver, North Vancouver and the entire North Shore.",
         "address": {"@type": "PostalAddress", "addressLocality": "West Vancouver", "addressRegion": "BC", "addressCountry": "CA"},
         "geo": {"@type": "GeoCoordinates", "latitude": 49.3286, "longitude": -123.1606},
         "areaServed": [{"@type": "City", "name": a} for a in AREAS],
         "openingHoursSpecification": [
             {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:00", "closes": "19:00"},
             {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday", "Sunday"], "opens": "08:00", "closes": "18:00"}],
         "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "237", "bestRating": "5", "worstRating": "1"}},
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "North Shore Garage Doors",
         "publisher": {"@id": SITE + "/#organization"}, "inLanguage": "en-CA"}]}) + '</script>'


# ============================ pages ============================
def build():
    pages = {}

    # ---------- HOME ----------
    hero = f'''
<section class="hero">
  <div class="hero-bg"><picture>
    <source media="(max-width:760px)" srcset="assets/img/hero-mobile.jpg">
    <img src="assets/img/hero-home.jpg" alt="Modern North Shore home with a new garage door" fetchpriority="high"></picture></div>
  <div class="blob b1"></div><div class="blob b2"></div>
  <div class="container"><div class="hero-content">
    <span class="pill"><b>★ 4.9</b> &nbsp;237+ five-star North Shore reviews</span>
    <h1>Garage doors,<br>done <span class="hl">beautifully.</span></h1>
    <p class="lead">Family-owned specialists for West &amp; North Vancouver. From broken springs to brand-new doors, we get your garage working — often the same day, always done right.</p>
    <div class="hero-actions">
      <a href="tel:{TEL}" class="btn btn-gold btn-lg magnetic">{PHONE} Call {PHONE_DISPLAY}</a>
      <a href="contact.html" class="btn btn-glass btn-lg">Get a free quote</a>
    </div>
    <div class="hero-trust">
      <div class="gcard"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m12 2 2.4 7.4H22l-6 4.4 2.3 7.2L12 16.7 5.7 21l2.3-7.2-6-4.4h7.6L12 2Z"/></svg></span><div><b>4.9★ rating</b><small>237+ reviews</small></div></div>
      <div class="gcard"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg></span><div><b>Same-day</b><small>service, 7 days</small></div></div>
      <div class="gcard"><span class="ic">{SHIELD}</span><div><b>Licensed</b><small>&amp; insured</small></div></div>
    </div>
    <div class="marquee"><div class="track">
      <span>Licensed &amp; Insured</span><span>LiftMaster® Dealer</span><span>Same-Day Service</span><span>Family-Owned</span><span>WorkSafeBC</span><span>Strata Experts</span>
      <span>Licensed &amp; Insured</span><span>LiftMaster® Dealer</span><span>Same-Day Service</span><span>Family-Owned</span><span>WorkSafeBC</span><span>Strata Experts</span>
    </div></div>
  </div></div>
  <div class="scroll-cue" aria-hidden="true"><span></span></div>
</section>'''
    statband = ('<section class="statband"><div class="container">'
                '<div class="sb reveal"><b class="count" data-count="4.9" data-decimals="1" data-suffix="★">4.9★</b><span>Average rating</span></div>'
                '<div class="sb reveal"><b class="count" data-count="237" data-suffix="+">237+</b><span>Five-star reviews</span></div>'
                '<div class="sb reveal"><b class="count" data-count="10" data-suffix="k+">10k+</b><span>Doors serviced</span></div>'
                '<div class="sb reveal"><b class="count" data-count="15" data-suffix="+">15+</b><span>Years on the North Shore</span></div>'
                '</div></section>')
    bento = f'''<div class="bento">
      <a href="services.html" class="tile t-wide t-tall reveal"><img src="assets/img/service-repair.jpg" alt="Garage door repair"><span class="arrow">{ARR}</span><div class="t-in"><h3>Garage Door Repair</h3><p>Off-track doors, cables, noisy operation &amp; doors that won't open — fixed fast.</p></div></a>
      <a href="springs.html" class="tile reveal"><img src="assets/img/spring-highcycle.jpg" alt="Spring replacement"><span class="arrow">{ARR}</span><div class="t-in"><h3>Springs</h3></div></a>
      <a href="openers.html" class="tile reveal"><img src="assets/img/service-opener.jpg" alt="Opener installation"><span class="arrow">{ARR}</span><div class="t-in"><h3>Openers</h3></div></a>
      <div class="tile solid reveal"><span class="eyebrow">LiftMaster®</span><h3>Smart &amp; quiet by default.</h3><p>Wi-Fi + myQ® app control on every opener we install.</p></div>
      <a href="garage-doors.html" class="tile t-wide reveal"><img src="assets/img/door-modern.jpg" alt="New garage doors"><span class="arrow">{ARR}</span><div class="t-in"><h3>Brand-new doors</h3><p>Modern, carriage, full-view glass &amp; insulated steel.</p></div></a>
    </div>'''
    why = f'''<section class="section bg-cloud"><div class="container"><div class="about-grid">
      <div class="pframe reveal"><img class="parallax" src="assets/img/strata.jpg" alt="North Shore townhomes with matching garage doors"></div>
      <div class="reveal">
        <span class="eyebrow">Why North Shore</span>
        <h2 class="section-title">A door is a third of your home's curb appeal. We treat it that way.</h2>
        <p style="color:var(--slate);font-size:1.05rem;margin-bottom:6px">No call-centre scripts, no commissioned salespeople — just a family that takes pride in doing the job properly the first time.</p>
        <div class="feature-list">
          <div class="feature"><span class="f-ico">{CHK}</span><div><h4>Same-day &amp; emergency</h4><p>Stocked local trucks mean we're there fast when it counts.</p></div></div>
          <div class="feature"><span class="f-ico">{CHK}</span><div><h4>Upfront pricing</h4><p>You approve a clear, all-in quote before any work begins.</p></div></div>
          <div class="feature"><span class="f-ico">{CHK}</span><div><h4>Strata specialists</h4><p>Trusted by councils &amp; property managers across the North Shore.</p></div></div>
        </div>
        <a href="about.html" class="btn btn-gold btn-lg magnetic" style="margin-top:24px">Meet the team</a>
      </div>
    </div></div></section>'''
    area_marquee = ('<section class="areas-marquee"><div class="marquee"><div class="track">'
                    + "".join(f'<span>{a}</span>' for a in AREAS) + "".join(f'<span>{a}</span>' for a in AREAS)
                    + '</div></div></section>')
    home_body = (hero + statband
                 + section("What we do", "Everything your garage door needs — in one local team.",
                           "From a snapped spring to a showpiece new door, we handle it all across the North Shore.", services_grid())
                 + why
                 + before_after(bg="cloud")
                 + steps_section()
                 + trust_promise()
                 + section("Loved by the North Shore", "4.9★ From 237+ Happy Neighbours",
                           "Real reviews from West Vancouver homeowners and strata communities.",
                           reviews_grid(3) + '<div class="center" style="margin-top:34px"><a href="reviews.html" class="btn btn-ghost btn-lg">Read more reviews</a></div>')
                 + area_marquee
                 + section("Get in touch", "Request Your Free Quote",
                           "Tell us what's going on and we'll get right back to you — usually within the hour during business hours.", contact_block(), bg="cloud"))
    pages["index.html"] = assemble("", head(
        "North Shore Garage Doors | Repair, Springs &amp; Openers | West &amp; North Vancouver",
        "North Shore Garage Doors — family-owned garage door repair, broken spring & opener replacement, LiftMaster openers, new door installation and strata service across West Vancouver, North Vancouver & the North Shore. Same-day service. Call (778) 800-0769.",
        SITE + "/", HOME_SCHEMA), home_body)

    # ---------- SERVICES ----------
    body = (page_hero("Residential garage door services", "Complete Garage Door Services on the North Shore",
                      "From a snapped spring on a Sunday morning to a brand-new custom door, one trusted local team handles it all — for homes and strata communities across West Vancouver and North Vancouver.", "Services", hero="services")
            + section("", "", "", services_grid())
            + steps_section())
    pages["services.html"] = assemble("services", head(
        "Garage Door Services | Repair, Springs, Openers &amp; Install | North Shore",
        "Full residential garage door services on the North Shore: same-day repair, spring & cable replacement, opener install, new doors and maintenance. West & North Vancouver. Call (778) 800-0769.",
        SITE + "/services.html",
        breadcrumb_schema("Services", SITE + "/services.html") + service_schema("Garage Door Services", "Residential garage door repair, spring replacement, opener installation and new door installation.", SITE + "/services.html")), body)

    # ---------- GARAGE DOORS ----------
    doors_detail = '''
    <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:24px;margin-top:10px">
      <div class="service-card reveal"><div class="sc-body"><h3>Modern Full-View</h3><p>Slim aluminum frames with frosted or clear glass for a bright, contemporary West Coast look. A standout on minimalist and architectural homes.</p></div></div>
      <div class="service-card reveal"><div class="sc-body"><h3>Carriage House</h3><p>Warm wood-grain textures with decorative hardware and optional windows — timeless charm with modern overhead convenience and insulation.</p></div></div>
      <div class="service-card reveal"><div class="sc-body"><h3>Traditional Steel</h3><p>Classic raised-panel steel doors in a wide range of colours. Durable, low-maintenance and the most popular choice for family homes.</p></div></div>
      <div class="service-card reveal"><div class="sc-body"><h3>Contemporary Flush</h3><p>Smooth, clean flush panels in bold or muted tones for a sleek, understated finish that complements modern architecture.</p></div></div>
    </div>'''
    body = (page_hero("New garage doors", "A New Garage Door That Lifts Your Whole Home",
                      "Your garage door is up to a third of your home's curb appeal — and your largest moving part. We help you choose the perfect style, colour and insulation, then install it flawlessly with quality hardware built for the West Coast climate.", "Garage Doors", hero="garage-doors")
            + section("Styles we install", "Find Your Style", "Insulated steel, aluminum &amp; glass, wood-look carriage and contemporary flush — measured, supplied and professionally installed.", doors_grid())
            + before_after(bg="cloud")
            + section("", "Built for the West Coast", "", doors_detail))
    pages["garage-doors.html"] = assemble("doors", head(
        "New Garage Doors &amp; Installation | Modern, Carriage, Steel | North Shore",
        "New garage door installation on the North Shore — modern aluminum & glass, carriage house, traditional steel and contemporary flush doors, expertly measured and installed in West & North Vancouver.",
        SITE + "/garage-doors.html",
        breadcrumb_schema("Garage Doors", SITE + "/garage-doors.html") + service_schema("Garage Door Installation", "New residential garage door supply and installation in modern, carriage, steel and full-view glass styles.", SITE + "/garage-doors.html")), body)

    # ---------- OPENERS ----------
    body = (page_hero("LiftMaster® Authorized Dealer", "Garage Door Openers, Done Right",
                      "We install and service the full LiftMaster® residential lineup. Start with our three most popular picks — or open the full collection to compare all seven models, every one with Wi-Fi and myQ® smartphone control.", "Garage Door Openers", hero="openers")
            + section("", "", "", openers_block())
            + section("Opener repairs too", "Opener Acting Up?", "We also repair most existing opener brands — noisy operation, broken gears, dead remotes, faulty safety sensors and Wi-Fi setup.",
                      '<div class="center"><a href="contact.html" class="btn btn-primary btn-lg">Book an Opener Repair</a></div>', bg="cloud"))
    pages["openers.html"] = assemble("openers", head(
        "LiftMaster Garage Door Openers | Install &amp; Repair | North Shore",
        "Authorized LiftMaster dealer on the North Shore. Belt-drive, chain-drive and wall-mount openers with Wi-Fi & myQ — supplied, installed and repaired in West & North Vancouver. Call (778) 800-0769.",
        SITE + "/openers.html",
        breadcrumb_schema("Garage Door Openers", SITE + "/openers.html") + service_schema("Garage Door Opener Installation & Repair", "LiftMaster garage door opener supply, installation and repair — belt-drive, chain-drive and wall-mount models.", SITE + "/openers.html")), body)

    # ---------- SPRINGS ----------
    why_both = f'''
<section class="section"><div class="container"><div class="about-grid">
  <div class="about-media reveal"><img src="assets/img/spring-double.jpg" alt="A matched pair of garage door torsion springs"></div>
  <div class="reveal">
    <span class="eyebrow">Honest advice</span>
    <h2 class="section-title">Why we usually suggest replacing both springs.</h2>
    <p style="color:var(--slate);font-size:1.05rem;margin-bottom:6px">If your door runs on two springs and one snaps, the other is almost always the same age and close behind. Replacing just one often means a second call-out — and a second service fee — within months.</p>
    <div class="feature-list">
      <div class="feature"><span class="f-ico">{CHK}</span><div><h4>Even balance, longer life</h4><p>Matched new springs share the load evenly, so your door runs smoother and both last longer.</p></div></div>
      <div class="feature"><span class="f-ico">{CHK}</span><div><h4>Fewer surprise breakdowns</h4><p>No getting caught out a few weeks later when the second tired spring finally lets go.</p></div></div>
      <div class="feature"><span class="f-ico">{CHK}</span><div><h4>Free cables included</h4><p>Lift cables wear alongside springs — so our two-spring and premium options replace them at no extra charge.</p></div></div>
    </div>
    <a href="contact.html" class="btn btn-primary btn-lg magnetic" style="margin-top:24px">Book my spring repair</a>
  </div>
</div></div></section>'''
    body = (page_hero("Spring replacement", "Broken Garage Door Spring? We'll Fix It Today",
                      "A broken spring is the #1 reason a garage door stops working — and it's our most common same-day call. Choose a single spring, two springs, or our premium extra-long-life set. Two-spring and premium repairs include free cable replacement.", "Spring Replacement", hero="springs")
            + section("Choose your fix", "Three honest spring options.",
                      "Single spring, two springs, or our longest-lasting premium set — installed the same day on most doors, every one backed by our workmanship warranty.", springs_block())
            + why_both
            + section("Stay safe", "Please don't DIY a spring.", "Garage door springs store enormous tension and can cause serious injury if they release unexpectedly. Our trained technicians carry the right springs and proper tools on every truck — call us and we'll handle it safely.",
                      f'<div class="center"><a href="tel:{TEL}" class="btn btn-call btn-lg">{PHONE} Call {PHONE_DISPLAY}</a></div>', bg="cloud"))
    pages["springs.html"] = assemble("springs", head(
        "Garage Door Spring Replacement | Same-Day | North Shore",
        "Broken garage door spring? Same-day torsion spring replacement on the North Shore — single, two-spring (free cables) and premium extra-long-life options. West & North Vancouver. Call (778) 800-0769.",
        SITE + "/springs.html",
        breadcrumb_schema("Spring Replacement", SITE + "/springs.html") + service_schema("Garage Door Spring Replacement", "Same-day torsion spring replacement — single spring, two springs with free cables, and premium extra-long-life options.", SITE + "/springs.html")), body)

    # ---------- STRATA ----------
    pm_cards = [
        ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3 8-8"/><path d="M21 12a9 9 0 1 1-6.2-8.5"/></svg>',
         "Scheduled multi-point inspections", "Every door, opener, spring, cable, roller and safety sensor checked on a set schedule — so worn parts get flagged early."),
        ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.1 2.1-2.1-.6-.6-2.1 2.1-2.1Z"/></svg>',
         "Tune-up on every visit", "Lubrication, balancing, hardware tightening and safety-reverse testing keep doors quiet, smooth and code-compliant."),
        ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 3v4a1 1 0 0 0 1 1h4"/><path d="M5 3h9l5 5v11a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Z"/><path d="M9 13h6M9 17h4"/></svg>',
         "Documented condition reports", "Written reports with photos for your files, council updates and depreciation reports — no guesswork at the AGM."),
        ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v6l4 2"/><circle cx="12" cy="14" r="8"/></svg>',
         "Fewer surprise call-outs", "Catching small issues early means fewer 11pm emergencies, more predictable budgets and happier residents."),
    ]
    pm_grid = ('<div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,250px),1fr))">'
               + "".join(f'<div class="promise reveal"><span class="p-ico">{ic}</span><h3>{t}</h3><p>{d}</p></div>' for ic, t, d in pm_cards)
               + '</div>')
    intro = f'''
<section class="section"><div class="container"><div class="strata-grid">
  <div class="reveal">
    <span class="eyebrow">For strata councils &amp; property managers</span>
    <h2 class="section-title">Garage doors, handled — so they never land on your desk at the worst time.</h2>
    <p style="color:var(--slate);font-size:1.06rem;margin-bottom:6px">A jammed parkade gate or a resident locked out by a snapped spring always seems to happen at 11pm on a long weekend. We make sure it rarely does — and when something does go wrong, you have one accountable, licensed team who already knows your buildings.</p>
    <ul class="strata-feats" style="margin-top:22px">
      <li>{CHK} One point of contact for every door, gate &amp; opener</li>
      <li>{CHK} Consolidated quotes, POs &amp; invoicing</li>
      <li>{CHK} Licensed, insured &amp; WorkSafeBC — COI on file</li>
      <li>{CHK} Documentation for council &amp; depreciation reports</li>
    </ul>
    <a href="contact.html" class="btn btn-primary btn-lg magnetic" style="margin-top:8px">Request a strata proposal</a>
  </div>
  <div class="strata-img reveal"><img src="assets/img/strata.jpg" alt="North Shore strata townhomes with matching garage doors"></div>
</div></div></section>'''
    pm = section("Preventive maintenance program", "Catch the problem on a Tuesday — not at 11pm Sunday.",
                 "Our strata maintenance program is built to find worn springs, frayed cables, tired openers and failing safety sensors before they strand a resident or trigger an after-hours emergency.",
                 pm_grid, bg="cloud")
    emergency = f'''
<section class="section strata"><div class="container"><div class="strata-grid">
  <div class="reveal">
    <span class="eyebrow">True 24/7 emergency response</span>
    <h2>Doors break at the worst times. We answer anyway.</h2>
    <p>When a resident is blocked out of the parkade or a door won't secure overnight, you can reach a real person — any hour, any day, including long weekends. Contracted buildings get priority dispatch, and our trucks carry the most common parts for a first-visit fix.</p>
    <ul class="strata-feats">
      <li>{CHK} 24/7 emergency line &amp; priority dispatch</li>
      <li>{CHK} Fast response so residents aren't stranded</li>
      <li>{CHK} Common springs, cables &amp; opener parts stocked</li>
      <li>{CHK} Evenings, weekends &amp; long weekends covered</li>
    </ul>
    <a href="tel:{TEL}" class="btn btn-gold btn-lg magnetic" style="margin-top:6px">{PHONE} Call our 24/7 line</a>
  </div>
  <div class="strata-img reveal"><img src="assets/img/strata-hero.jpg" alt="Torsion springs and garage door hardware serviced for a North Shore strata"></div>
</div></div></section>'''
    why = section("Why managers choose us", "Less hassle for you. Fewer complaints from residents.", "",
                  '<div class="feature-list" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:24px">'
                  + "".join(f'<div class="feature"><span class="f-ico">{CHK}</span><div><h4>{t}</h4><p>{d}</p></div></div>' for t, d in [
                      ("Single point of contact", "One number for every building — no chasing three different vendors."),
                      ("Council-friendly quotes", "Clear, itemized pricing your council can approve without surprises."),
                      ("Multi-building experience", "Parkade gates, common-area doors and individual townhome doors alike."),
                      ("Matching doors &amp; hardware", "Consistent doors, springs and openers across units for a uniform look."),
                      ("Fully insured &amp; documented", "COI on file, WorkSafeBC, and a paper trail for every visit."),
                      ("Reliable, on-time crews", "Local, stocked trucks mean we show up when we say we will."),
                  ]) + '</div>')
    body = (page_hero("Strata &amp; townhome communities", "The Garage Door Partner Strata Managers Rely On",
                      "Preventive maintenance, fast documented repairs and genuine 24/7 emergency response for strata and townhome communities across West Vancouver and the North Shore.", "Strata &amp; Townhomes", hero="strata")
            + intro + pm + emergency + why)
    pages["strata.html"] = assemble("strata", head(
        "Strata Garage Door Maintenance &amp; 24/7 Service | North Shore",
        "Preventive maintenance, documented repairs and true 24/7 emergency response for North Shore strata & townhome communities. One point of contact, council-friendly quotes, fully insured. West & North Vancouver.",
        SITE + "/strata.html",
        breadcrumb_schema("Strata & Townhomes", SITE + "/strata.html") + service_schema("Strata & Townhome Garage Door Service", "Multi-unit garage door maintenance, repair and installation for strata corporations and property managers.", SITE + "/strata.html")), body)

    # ---------- ABOUT ----------
    about_inner = f'''
  <div class="about-grid">
    <div class="about-media reveal"><img src="assets/img/family-team.jpg" alt="The family-owned North Shore Garage Doors team">
      <div class="about-badge"><span class="ab-num">15+</span><small>Years serving<br>the North Shore</small></div></div>
    <div class="reveal">
      <p style="color:var(--slate);font-size:1.05rem;margin-bottom:6px">North Shore Garage Doors started with a simple idea: treat every customer's home like our own. As a family-owned and operated business, we don't have call-centre scripts or commissioned salespeople — just neighbours who take pride in doing the job properly the first time.</p>
      <div class="feature-list">
        <div class="feature"><span class="f-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg></span><div><h4>You'll always deal with the family</h4><p>The same trusted faces from your first call to the final test of your door.</p></div></div>
        <div class="feature"><span class="f-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></span><div><h4>Honest, upfront pricing</h4><p>You approve a clear, all-in quote before any work begins. No surprises, ever.</p></div></div>
        <div class="feature"><span class="f-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8Z"/></svg></span><div><h4>Fast, local response</h4><p>Based right here on the North Shore, so we're at your door quickly when it counts.</p></div></div>
      </div>
      <div class="stats"><div class="stat"><b class="count" data-count="4.9" data-decimals="1" data-suffix="★">4.9★</b><span>Average rating</span></div><div class="stat"><b class="count" data-count="10" data-suffix="k+">10k+</b><span>Doors serviced</span></div><div class="stat"><b>Same-Day</b><span>Most repairs</span></div></div>
    </div>
  </div>'''
    body = (page_hero("Our family, your neighbours", "Built on Family Values &amp; Honest Work",
                      "We're a family-owned and operated garage door company that treats every customer's home like our own — honest pricing, quality workmanship and friendly local faces.", "About Us", hero="about")
            + f'<section class="section"><div class="container">{about_inner}</div></section>'
            + section("Where we work", "Proudly Serving the North Shore", "From West Vancouver to Deep Cove, our stocked local trucks mean help is never far away.",
                      areas_list() + f'<div class="center" style="margin-top:30px"><a href="service-areas.html" class="btn btn-ghost btn-lg">See all service areas</a></div>', bg="cloud"))
    pages["about.html"] = assemble("about", head(
        "About Us | Family-Owned Garage Door Company | North Shore",
        "North Shore Garage Doors is a family-owned, locally operated garage door company serving West Vancouver, North Vancouver and the North Shore with honest pricing and quality workmanship.",
        SITE + "/about.html", breadcrumb_schema("About Us", SITE + "/about.html")), body)

    # ---------- SERVICE AREAS ----------
    body = (page_hero("Where we work", "Proudly Serving West Vancouver &amp; the North Shore",
                      "If you're on the North Shore, we've got you covered. Our trucks are stocked and local, so same-day help is never far away.", "Service Areas", hero="service-areas")
            + section("Where we work", "One local team for the whole North Shore.",
                      "From the British Properties to Horseshoe Bay, Lynn Valley to Deep Cove, and across to Bowen Island, our stocked local trucks mean fast, same-day garage door service — for single-family homes, townhomes and strata parkades alike.",
                      areas_list())
            + section("Not sure if we cover you?", "Just ask.", "If your community is on or near the North Shore, give us a call — we very likely serve your street.",
                      f'<div class="center"><a href="tel:{TEL}" class="btn btn-call btn-lg">{PHONE} Call {PHONE_DISPLAY}</a></div>', bg="cloud"))
    pages["service-areas.html"] = assemble("areas", head(
        "Service Areas | West &amp; North Vancouver, North Shore | Garage Doors",
        "North Shore Garage Doors serves West Vancouver, North Vancouver, British Properties, Ambleside, Dundarave, Caulfeild, Horseshoe Bay, Lions Bay, Bowen Island and more. Same-day garage door service.",
        SITE + "/service-areas.html", breadcrumb_schema("Service Areas", SITE + "/service-areas.html")), body)

    # ---------- REVIEWS ----------
    rating_band = ('<section class="statband"><div class="container">'
                   '<div class="sb reveal"><b class="count" data-count="4.9" data-decimals="1" data-suffix="★">4.9★</b><span>Average rating</span></div>'
                   '<div class="sb reveal"><b class="count" data-count="237" data-suffix="+">237+</b><span>Verified reviews</span></div>'
                   '<div class="sb reveal"><b class="count" data-count="98" data-suffix="%">98%</b><span>Would recommend</span></div>'
                   '<div class="sb reveal"><b class="count" data-count="15" data-suffix="+">15+</b><span>Years on the North Shore</span></div>'
                   '</div></section>')
    body = (page_hero("Loved by the North Shore", "4.9★ From 237+ Happy Neighbours",
                      "Real reviews from West Vancouver homeowners and strata communities who trust us with their garage doors.", "Reviews", hero="reviews")
            + rating_band
            + section("", "", "", reviews_grid(8))
            + section("Had a great experience?", "We'd love your review.",
                      "A quick review helps your North Shore neighbours find a garage door team they can trust.",
                      '<div class="center"><a href="contact.html" class="btn btn-primary btn-lg magnetic">Leave us a review</a></div>', bg="cloud"))
    pages["reviews.html"] = assemble("reviews", head(
        "Reviews | 4.9★ Garage Door Service | North Shore",
        "Read reviews of North Shore Garage Doors — 4.9 stars from 237+ West Vancouver and North Vancouver homeowners and strata communities. Honest, fast, family-owned garage door service.",
        SITE + "/reviews.html", breadcrumb_schema("Reviews", SITE + "/reviews.html")), body)

    # ---------- FAQ ----------
    body = (page_hero("Good to know", "Frequently Asked Questions",
                      "Answers to the questions North Shore homeowners ask us most about garage door repair, springs, openers and new doors.", "FAQ", hero="faq")
            + section("", "", "", faq_accordion(FAQS)))
    pages["faq.html"] = assemble("faq", head(
        "Garage Door FAQ | North Shore Garage Doors",
        "Garage door FAQs: same-day repair, broken springs, opener brands, installation time, pricing and warranty — answered by North Shore Garage Doors serving West & North Vancouver.",
        SITE + "/faq.html", breadcrumb_schema("FAQ", SITE + "/faq.html") + faq_schema(FAQS)), body)

    # ---------- CONTACT ----------
    body = (page_hero("Get in touch", "Request Your Free Quote",
                      "Tell us what's going on and we'll get right back to you — usually within the hour during business hours. For urgent issues, call us any time.", "Contact", show_cta=False, hero="contact")
            + section("", "", "", contact_block()))
    pages["contact.html"] = assemble("", head(
        "Contact &amp; Free Quote | North Shore Garage Doors | (778) 800-0769",
        "Contact North Shore Garage Doors for a free, no-obligation garage door quote. Call (778) 800-0769 or send a message. Serving West Vancouver, North Vancouver & the North Shore.",
        SITE + "/contact.html", breadcrumb_schema("Contact", SITE + "/contact.html")), body)

    # ---------- LEGAL PAGES ----------
    legal_css = ('<style>.legal{max-width:820px;margin:0 auto;padding:48px 20px}'
                 '.legal h2{font-size:1.3rem;margin:34px 0 12px;color:var(--navy)}'
                 '.legal h3{font-size:1.05rem;margin:22px 0 8px;color:var(--navy-2)}'
                 '.legal p,.legal li{color:var(--slate);margin-bottom:12px;font-size:1rem}'
                 '.legal ul{padding-left:22px;list-style:disc;margin-bottom:14px}'
                 '.legal a{color:var(--steel);font-weight:600;overflow-wrap:anywhere}'
                 '.legal .updated{color:var(--muted);font-size:.9rem}</style>')

    privacy_main = '''<main class="legal">
  <p class="updated">Last updated: ''' + "June 20, 2026" + '''</p>
  <p>North Shore Garage Doors ("we," "us," or "our") respects your privacy and is committed to protecting the personal information you share with us. This Privacy Policy explains what information we collect, how we use it, and the choices you have. We handle personal information in accordance with Canada's <em>Personal Information Protection and Electronic Documents Act</em> (PIPEDA) and British Columbia's <em>Personal Information Protection Act</em> (PIPA).</p>
  <h2>1. Information We Collect</h2>
  <p>We only collect information that helps us provide our garage door services. This may include:</p>
  <ul><li><strong>Contact details you provide</strong> — your name, phone number, email address, service address and any message you send through our quote form, by phone or by email.</li>
  <li><strong>Service information</strong> — details about your garage door issue or project that you choose to share with us.</li>
  <li><strong>Website usage data</strong> — basic technical information such as your browser type, device, approximate location and the pages you visit, collected automatically to keep the site secure and improve it.</li></ul>
  <h2>2. How We Use Your Information</h2>
  <p>We use your personal information to:</p>
  <ul><li>Respond to your enquiries and provide quotes;</li><li>Schedule, perform and follow up on garage door services;</li>
  <li>Send appointment confirmations, invoices and service-related communication;</li><li>Improve our website, services and customer experience;</li>
  <li>Meet our legal, accounting and regulatory obligations.</li></ul>
  <p>We will never sell your personal information.</p>
  <h2>3. Consent</h2>
  <p>By contacting us or submitting our quote form, you consent to the collection and use of your information for the purposes described above. You may withdraw your consent at any time by contacting us, subject to legal or contractual restrictions.</p>
  <h2>4. Sharing Your Information</h2>
  <p>We do not sell, rent or trade your personal information. We may share it only with trusted service providers who help us operate our business (for example, website hosting, email, scheduling or payment processing), and only to the extent necessary. These providers are required to safeguard your information. We may also disclose information where required by law.</p>
  <h2>5. Cookies &amp; Analytics</h2>
  <p>Our website may use cookies and similar technologies to remember your preferences and understand how visitors use the site. You can control or disable cookies through your browser settings. If we use analytics tools, they collect aggregate, non-identifying usage data.</p>
  <h2>6. Data Retention</h2>
  <p>We keep your personal information only as long as necessary to fulfil the purposes described in this policy and to meet legal and business requirements, after which it is securely deleted or anonymized.</p>
  <h2>7. Security</h2>
  <p>We use reasonable physical, organizational and technical safeguards to protect your personal information against loss, theft and unauthorized access. No method of transmission over the internet is completely secure, but we work to protect your information at all times.</p>
  <h2>8. Your Rights</h2>
  <p>You have the right to access the personal information we hold about you, to request corrections, and to ask that we delete it where appropriate. To make a request, please contact us using the details below.</p>
  <h2>9. Children's Privacy</h2>
  <p>Our services and website are intended for adults. We do not knowingly collect personal information from children.</p>
  <h2>10. Changes to This Policy</h2>
  <p>We may update this Privacy Policy from time to time. The "Last updated" date above reflects the most recent revision. Please review it periodically.</p>
  <h2>11. Contact Us</h2>
  <p>If you have questions about this Privacy Policy or how we handle your information, please contact us:</p>
  <ul><li><strong>North Shore Garage Doors</strong></li><li>Phone: <a href="tel:''' + TEL + '''">''' + PHONE_DISPLAY + '''</a></li>
  <li>Email: <a href="mailto:''' + EMAIL + '''">''' + EMAIL_DISPLAY + '''</a></li><li>Service area: West Vancouver &amp; the North Shore, British Columbia</li></ul>
</main>'''

    terms_main = '''<main class="legal">
  <p class="updated">Last updated: June 20, 2026</p>
  <p>These Terms of Service ("Terms") govern your use of the North Shore Garage Doors website and the services we provide. By using our website or engaging our services, you agree to these Terms.</p>
  <h2>1. Our Services</h2>
  <p>North Shore Garage Doors provides residential and strata garage door repair, spring and cable replacement, opener installation and repair, new door installation, and maintenance across West Vancouver, North Vancouver and the North Shore of British Columbia.</p>
  <h2>2. Quotes &amp; Pricing</h2>
  <p>Quotes are provided in good faith based on the information available at the time and may be adjusted if the scope of work changes or additional issues are discovered. We will always discuss and obtain your approval before performing additional work.</p>
  <h2>3. Workmanship &amp; Warranty</h2>
  <p>Our work is backed by a workmanship warranty on parts and labour, in addition to any applicable manufacturer warranties on doors, openers and springs. Warranty terms are provided with your invoice and exclude damage caused by misuse, accidents, or unauthorized modifications.</p>
  <h2>4. Safety Notice</h2>
  <p>Garage door springs and related components are under extreme tension and can cause serious injury. Repairs and adjustments should be carried out only by trained technicians. We are not responsible for injury or damage resulting from self-performed repairs.</p>
  <h2>5. Payment</h2>
  <p>Payment is due upon completion of work unless otherwise agreed in writing. We accept cash, credit card, debit and e-transfer.</p>
  <h2>6. Website Use</h2>
  <p>The content on this website is provided for general information only. While we strive to keep it accurate and up to date, we make no warranties about its completeness or accuracy. Product model availability, specifications and pricing may change without notice.</p>
  <h2>7. Intellectual Property</h2>
  <p>All content on this website, including text, graphics and images, is the property of North Shore Garage Doors unless otherwise stated, and may not be reproduced without permission. Brand names such as LiftMaster® and myQ® are the property of their respective owners.</p>
  <h2>8. Limitation of Liability</h2>
  <p>To the fullest extent permitted by law, North Shore Garage Doors shall not be liable for any indirect, incidental or consequential damages arising from the use of our website or services, beyond the amount paid for the services in question.</p>
  <h2>9. Changes to These Terms</h2>
  <p>We may update these Terms from time to time. The "Last updated" date reflects the most recent revision. Continued use of our website or services constitutes acceptance of the updated Terms.</p>
  <h2>10. Contact Us</h2>
  <ul><li><strong>North Shore Garage Doors</strong></li><li>Phone: <a href="tel:''' + TEL + '''">''' + PHONE_DISPLAY + '''</a></li>
  <li>Email: <a href="mailto:''' + EMAIL + '''">''' + EMAIL_DISPLAY + '''</a></li><li>Service area: West Vancouver &amp; the North Shore, British Columbia</li></ul>
</main>'''

    def legal_page(title, desc, canonical, crumb, h1, intro, main_html, schema):
        h = head(title, desc, canonical, legal_css + schema)
        return (h + header("") + mobile_nav("")
                + page_hero("Legal", h1, intro, crumb, show_cta=False)
                + main_html + footer() + chrome_end())

    pages["privacy-policy.html"] = legal_page(
        "Privacy Policy | North Shore Garage Doors",
        "Privacy Policy for North Shore Garage Doors — how we collect, use and protect your personal information, in line with Canada's PIPEDA and BC's PIPA.",
        SITE + "/privacy-policy.html", "Privacy Policy", "Privacy Policy",
        "How we collect, use and protect your personal information.", privacy_main,
        breadcrumb_schema("Privacy Policy", SITE + "/privacy-policy.html"))
    pages["terms.html"] = legal_page(
        "Terms of Service | North Shore Garage Doors",
        "Terms of Service for North Shore Garage Doors — the terms that apply to our website and garage door services across West Vancouver and the North Shore.",
        SITE + "/terms.html", "Terms", "Terms of Service",
        "The terms that apply to our website and services.", terms_main,
        breadcrumb_schema("Terms", SITE + "/terms.html"))

    # write files
    for fn, html in pages.items():
        with open(os.path.join(ROOT, fn), "w") as f:
            f.write(html)
        print("wrote", fn, f"({len(html)//1024} KB)")
    return list(pages.keys())


if __name__ == "__main__":
    build()
