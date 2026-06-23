#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_pages import (head, header, footer, cta_band, page_hero, ld, breadcrumb_ld,
                         write, BASE, PHONE, TEL, SMS, PHONE_SVG, CHECK)

# ---------------- BECOME A PARTNER ----------------
extra = ld(breadcrumb_ld([("Home","index.html"),("Become a Partner","become-a-partner.html")]))
p = head("Become a Partner | North Shore Garage Doors",
         "Apply to receive overflow garage-door leads on the North Shore. For vetted, licensed and insured installers, handymen and property-services companies in West &amp; North Vancouver.",
         "become-a-partner.html", extra_ld=extra) + header()
p += page_hero("Become a Partner",
    "We get more calls than we can take. If you do quality garage-door or property work on the North Shore, partner with us for vetted overflow jobs in your area.",
    ["<a href='index.html'>Home</a>","Become a Partner"])
p += f'''
<section class="section"><div class="container"><div class="two-col">
  <div class="prose">
    <h2>Real overflow work, fairly shared</h2>
    <p>North Shore Garage Doors is busy — and some weeks we simply can't reach every customer as fast as we'd like. Rather than leave homeowners waiting, we pass genuine, ready-to-book jobs to trusted local partners. No buy-in, no lead-selling games — just real work in your service area when we're at capacity.</p>
    <h2>Who we partner with</h2>
    <ul>
      <li>Garage-door installers &amp; repair techs</li>
      <li>Handymen and general contractors</li>
      <li>Builders &amp; renovators needing door supply/install</li>
      <li>Property-services &amp; strata-maintenance companies</li>
    </ul>
    <h2>What we ask</h2>
    <ul>
      <li>Licensed (business licence), insured &amp; WorkSafeBC-covered</li>
      <li>Quality workmanship and honest, upfront pricing</li>
      <li>Responsiveness — these are real customers waiting</li>
    </ul>
    <h2>Apply below</h2>
    <p>Tell us about your company and where you work. We'll be in touch to set things up. Applications go straight to <a href="mailto:info@northshoregaragedoors.ca" style="color:var(--steel);font-weight:700">info@northshoregaragedoors.ca</a>.</p>
    <div class="form-card" style="margin-top:18px">
      <form data-quote data-subject="Partner application" data-to="info@northshoregaragedoors.ca" novalidate>
        <div class="form-row two">
          <div class="field"><label for="p-name">Your name</label><input id="p-name" name="name" type="text" placeholder="Full name" required></div>
          <div class="field"><label for="p-company">Company</label><input id="p-company" name="company" type="text" placeholder="Business name"></div>
        </div>
        <div class="form-row two">
          <div class="field"><label for="p-phone">Phone</label><input id="p-phone" name="phone" type="tel" placeholder="(604) 000-0000" required></div>
          <div class="field"><label for="p-email">Email</label><input id="p-email" name="email" type="email" placeholder="you@email.com"></div>
        </div>
        <div class="form-row two">
          <div class="field"><label for="p-trade">Trade / service</label><input id="p-trade" name="trade" type="text" placeholder="e.g. garage door installer, handyman"></div>
          <div class="field"><label for="p-area">Service area</label><input id="p-area" name="service_area" type="text" placeholder="e.g. North &amp; West Vancouver"></div>
        </div>
        <div class="form-row"><div class="field"><label for="p-notes">Capacity &amp; notes</label><textarea id="p-notes" name="notes" placeholder="How many jobs/week can you take? Licensing, insurance, WorkSafeBC #, experience…"></textarea></div></div>
        <button type="submit" class="btn btn-primary btn-block btn-lg">Submit Application</button>
        <p class="form-note">Prefer to talk? Call <a href="tel:{TEL}" style="color:var(--steel);font-weight:700">{PHONE}</a>.</p>
      </form>
      <div class="form-success" id="formSuccess">{CHECK} Thanks! Your application has been received — we'll be in touch about overflow work in your area.</div>
    </div>
  </div>
  <aside class="side-card"><h3>Why partner with us?</h3>
    <p style="color:var(--slate);font-size:.95rem">We're an established, well-reviewed West Vancouver brand sending you pre-qualified local customers — no platforms, no per-lead fees.</p>
    <a href="tel:{TEL}" class="btn btn-call btn-block">{PHONE_SVG} Call {PHONE}</a>
    <a href="{SMS}" class="btn btn-ghost btn-block" style="margin-top:10px">Text Us</a>
  </aside>
</div></div></section>'''
p += cta_band("Let's Send You Some Work","Apply above or call to talk it through — we'd rather a great local pro handle the overflow than make a customer wait.") + footer()
write("become-a-partner.html", p)

# ---------------- THANK YOU ----------------
t = head("Thank You | North Shore Garage Doors",
         "Thanks for getting in touch with North Shore Garage Doors. We'll be right back to you.",
         "thank-you.html") + header()
t += f'''
<section class="section" style="min-height:54vh;display:flex;align-items:center">
  <div class="container center" style="max-width:640px">
    <div style="width:78px;height:78px;border-radius:50%;background:var(--green);color:#fff;display:flex;align-items:center;justify-content:center;margin:0 auto 22px"><svg viewBox="0 0 24 24" width="40" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M20 6 9 17l-5-5"/></svg></div>
    <span class="eyebrow center" style="justify-content:center">Message received</span>
    <h1 class="section-title">Thank You — We'll Be in Touch Shortly</h1>
    <p class="section-intro" style="margin:0 auto 26px">Your request has reached the family. We usually reply within the hour during business hours. For anything urgent — a door stuck open or a car trapped inside — please call us right now.</p>
    <div class="cta-actions" style="justify-content:center">
      <a href="tel:{TEL}" class="btn btn-call btn-lg" data-hover-lift>{PHONE_SVG} Call {PHONE}</a>
      <a href="index.html" class="btn btn-ghost btn-lg">Back to Home</a>
    </div>
  </div>
</section>'''
t += footer()
write("thank-you.html", t)

# ---------------- 404 ----------------
e = head("Page Not Found | North Shore Garage Doors",
         "That page couldn't be found. Explore our garage door services across West Vancouver and the North Shore.",
         "404.html") + header()
e += f'''
<section class="section" style="min-height:54vh;display:flex;align-items:center">
  <div class="container center" style="max-width:640px">
    <span class="eyebrow center" style="justify-content:center">Error 404</span>
    <h1 class="section-title">That Door Wouldn't Open</h1>
    <p class="section-intro" style="margin:0 auto 26px">We couldn't find the page you were after — but we can definitely find your garage door problem. Try one of these:</p>
    <div class="related-links" style="justify-content:center">
      <a href="index.html">Home</a><a href="garage-door-repair.html">Repair</a><a href="spring-repair.html">Springs</a>
      <a href="opener-installation.html">Openers</a><a href="new-garage-doors.html">New Doors</a><a href="index.html#contact">Contact</a>
    </div>
    <div class="cta-actions" style="justify-content:center;margin-top:24px">
      <a href="tel:{TEL}" class="btn btn-call btn-lg" data-hover-lift>{PHONE_SVG} Call {PHONE}</a>
    </div>
  </div>
</section>'''
e += footer()
write("404.html", e)
print("extra pages built")
