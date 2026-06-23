#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Per-page content for North Shore Garage Doors. Run to (re)build all pages.
  python3 scripts/content.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_pages import (service_page, area_page, head, header, footer, cta_band,
                         page_hero, ld, breadcrumb_ld, faq_ld, write, BASE, PHONE, TEL, SMS, PHONE_SVG)

# ============================ SERVICE PAGES ============================

service_page(
  "spring-repair.html",
  "Garage Door Spring Repair West Vancouver | Same-Day Torsion Springs",
  "Broken garage door spring in West Vancouver? Same-day torsion &amp; extension spring replacement with free cables on pairs and a free safety inspection. Upfront flat-rate pricing.",
  "Garage Door Spring Repair in West Vancouver",
  "A snapped spring is the #1 reason a garage door stops working — and the most common same-day call we run across the North Shore. Here's exactly what we replace, why, and what it costs.",
  [("p","If your door suddenly won't lift, you heard a loud bang from the garage, or the opener strains and gives up, you've almost certainly broken a torsion spring. The spring — not the opener — does the heavy lifting, so when it goes, the door becomes a 150–250&nbsp;lb dead weight. Please don't force it."),
   ("h2","Torsion vs. extension springs"),
   ("p","Most West Vancouver homes use <b>torsion springs</b> mounted on a steel shaft above the door — they're safer, quieter and longer-lived. Older or lighter doors may use <b>extension springs</b> running along the tracks. We replace both, but we'll often recommend converting to torsion for a smoother, more durable system."),
   ("h2","Why we replace springs in pairs"),
   ("p","If you have two springs and one breaks, the second is the same age and usually within months of failing too. Replacing both at once means one service call instead of two, a balanced door, and longer life overall. That's why our two-spring option includes <b>brand-new lift cables free</b> — the cables wear alongside the springs."),
   ("h2","High-cycle springs &amp; our coastal climate"),
   ("p","A standard spring is rated around 10,000 cycles (~7 years of normal use). On the North Shore, salt air and damp accelerate corrosion, so for busy households or homes near the water we recommend <b>high-cycle springs</b> — 20,000–30,000 cycles — often the last spring you'll ever buy."),
   ("ul",["Free safety inspection with every spring job","Free cables on both two-spring options","Oil-tempered, corrosion-resistant springs stocked on every truck","Same-day replacement in most cases","Workmanship warranty on parts &amp; labour"]),
   ("h2","Why you shouldn't DIY a spring"),
   ("p","Torsion springs hold enormous stored energy. A slip with the winding bars can cause serious injury. This is the one repair every manufacturer says to leave to a trained technician — and it's routine work for us.")],
  [("Can I still open my door with a broken spring?","Please don't. The door is extremely heavy without a working spring and can fall. Disconnect the opener (red cord) and call us — forcing it can damage the opener, tracks and panels."),
   ("How long does spring replacement take?","Most replacements take 45–90 minutes on site, and we carry the common sizes on the truck, so it's usually a same-day, one-visit fix."),
   ("How much does a garage door spring cost in West Vancouver?","Our single-spring replacement is a flat upfront rate; two springs with free cables and two high-cycle springs are priced higher for the added parts and lifespan. Tap “Show pricing” in the footer to see exact numbers — no hidden fees."),
   ("Should I replace one spring or both?","If you have two springs, we strongly recommend replacing both. They wear at the same rate, and doing both keeps the door balanced and saves a second call.")],
  [("Garage door repair","garage-door-repair.html"),("Cables &amp; rollers","cable-roller-repair.html"),("Maintenance tune-up","maintenance-tune-up.html"),("Openers","opener-installation.html")],
  img="assets/img/service-spring-960.webp",
  price_html=(
    '<h2>Spring pricing — clear and upfront</h2>'
    '<div class="price-card" style="max-width:520px;margin-top:8px">'
    '<div class="price-row"><span class="pr-label">Single torsion spring</span><span class="price-tag" data-px="$739">Upfront flat rate</span></div>'
    '<div class="price-row"><span class="pr-label">Two springs + free cables</span><span class="price-tag" data-px="$851">Best value</span></div>'
    '<div class="price-row"><span class="pr-label">Two high-cycle springs (cables free)</span><span class="price-tag" data-px="$1,274">Longest life</span></div>'
    '<p class="price-hint">Prices hidden by default — reveal them with “Show pricing” in the footer.</p></div>'))

service_page(
  "garage-door-repair.html",
  "Garage Door Repair West Vancouver | Same-Day &amp; Emergency",
  "Fast, honest garage door repair across West Vancouver &amp; the North Shore — off-track doors, broken cables, noisy operation, dented panels, dead openers and sensors. Same-day &amp; emergency.",
  "Garage Door Repair in West Vancouver",
  "Door off its tracks? Won't open or close? Grinding like a freight train? We diagnose it in plain language, quote it upfront, and fix most problems on the first visit.",
  [("p","A garage door is the largest moving part of your home, and when it fails it's rarely convenient — you're blocked in, or you can't lock up. We run same-day and emergency repairs across West Vancouver, from Ambleside to Horseshoe Bay, with a stocked truck so most jobs are done in one visit."),
   ("h2","What we repair"),
   ("ul",["<b>Off-track doors</b> — rollers jumped the track after an impact or cable failure","<b>Broken cables</b> — frayed or snapped lift cables (often alongside a spring)","<b>Broken springs</b> — our most common same-day call","<b>Noisy, grinding operation</b> — worn rollers, dry hinges, loose hardware","<b>Dented or sagging panels</b> — repaired, or a single section replaced","<b>Doors that won't open/close</b> — opener faults, safety sensors, logic boards","<b>Misaligned safety sensors</b> — the #1 reason a door reverses"]),
   ("h2","Our honest diagnostic"),
   ("p","We start by testing the door's balance, springs, cables, rollers, tracks and opener, then explain what's actually wrong and what's optional. You get a clear, all-in price <b>before</b> we start — no vague “service call” fee that balloons on your driveway, and no upselling a new door when a $200 repair will do."),
   ("h2","Built for the West Coast"),
   ("p","North Shore weather is hard on hardware — driving rain, salt air near the water, and big temperature swings up toward Cypress. We use corrosion-resistant parts and lubricants rated for damp coastal conditions so the fix lasts.")],
  [("Do you offer emergency garage door repair?","Yes. We keep same-day slots for urgent issues like a door stuck open (a security risk) or a car trapped inside, across West Vancouver and the North Shore."),
   ("How much does a garage door repair cost?","It depends on the part — a roller or sensor realignment is modest; spring or cable work is priced upfront. You always approve a written, all-in quote before we begin. Tap “Show pricing” in the footer for our common rates."),
   ("Can you fix my door, or do I need a new one?","Most doors are very repairable. We'll only recommend replacement if the cost of repairs approaches the value of a new door, or the panels are structurally damaged — and we'll tell you honestly."),
   ("My door reverses before it closes — why?","Usually the photo-eye safety sensors near the floor are misaligned or dirty. It's a quick fix, and something we check on every visit.")],
  [("Spring repair","spring-repair.html"),("Cables &amp; rollers","cable-roller-repair.html"),("Opener repair","opener-installation.html"),("Tune-up","maintenance-tune-up.html")],
  img="assets/img/service-repair-960.webp")

service_page(
  "opener-installation.html",
  "Garage Door Opener Installation West Vancouver | LiftMaster Dealer",
  "Authorized LiftMaster® dealer in West Vancouver. Quiet belt-drive, chain-drive and wall-mount openers installed and repaired — Wi-Fi + myQ, battery backup. Upfront installed pricing.",
  "Garage Door Openers in West Vancouver",
  "We install and service the full LiftMaster® residential lineup — quiet belt drives, rugged chain drives and space-saving wall-mounts, all with Wi-Fi and the myQ® app.",
  [("p","Whether your old opener finally died or you want app control, battery backup and a quieter motor, we're an authorized LiftMaster® dealer and install their complete residential range. We also repair most existing opener brands — sometimes a $150 logic board or gear kit saves a full replacement."),
   ("h2","Which drive is right for you?"),
   ("ul",["<b>Belt drive</b> — the quietest option; ideal when there's a bedroom or office above the garage (common in West Van's three-storey homes)","<b>Chain drive</b> — rugged and economical; perfect for detached garages and shops","<b>Wall-mount (jackshaft)</b> — mounts beside the door to free your ceiling; great for tall cathedral doors and built-in storage"]),
   ("h2","Smart features worth having"),
   ("ul",["<b>myQ® app</b> — open, close and check your door from anywhere; get alerts if it's left open","<b>Battery backup</b> — keep working through North Shore power outages (and it's required by code on new installs in many cases)","<b>Built-in camera &amp; 2-way talk</b> — see deliveries and visitors","<b>Wi-Fi + smart-home</b> — works with the home automation you already use"]),
   ("h2","The full LiftMaster lineup we install"),
   ("p","From the dependable 2220L chain drive up to the 6690L Secure View belt drive with a 360° camera and the 98022 wall-mount with battery backup — seven models in total. Every install includes haul-away of the old unit, new safety sensors, and a walkthrough of the app."),
   ("h2","Installed, upfront pricing"),
   ("p","Every opener price on this site is <b>installed</b>, not just the box — programmed, tested and tidied up. Reveal the per-model numbers with the footer toggle.")],
  [("Are you really a LiftMaster dealer?","Yes — we're an authorized LiftMaster® dealer, so you get genuine units, full manufacturer warranty and trained installation, not a big-box self-install kit."),
   ("Can you repair my existing opener?","Often, yes. Worn gears, broken belts, dead logic boards and faulty sensors are all repairable. We'll quote the repair vs. replacement honestly so you can choose."),
   ("How long does opener installation take?","A straightforward replacement is typically 2–3 hours, including removing the old unit, mounting the new one, new sensors, programming remotes and the myQ app."),
   ("Do new openers work in a power outage?","Models with battery backup do — they'll run for a number of cycles on the internal battery. We recommend it on the North Shore, where winter storms cause outages.")],
  [("New garage doors","new-garage-doors.html"),("Garage door repair","garage-door-repair.html"),("Spring repair","spring-repair.html"),("Maintenance","maintenance-tune-up.html")],
  img="assets/img/service-opener-960.webp",
  price_html=(
    '<h2>Installed opener pricing</h2>'
    '<div class="price-card" style="max-width:560px;margin-top:8px">'
    '<div class="price-row"><span class="pr-label">2220L — chain drive</span><span class="price-tag" data-px="$1,311 installed">Installed</span></div>'
    '<div class="price-row"><span class="pr-label">6580L — ultra-quiet belt</span><span class="price-tag" data-px="$1,448 installed">Installed</span></div>'
    '<div class="price-row"><span class="pr-label">6690L — belt + 360° camera</span><span class="price-tag" data-px="$1,523 installed">Installed</span></div>'
    '<div class="price-row"><span class="pr-label">98022 — wall-mount + battery</span><span class="price-tag" data-px="$2,155 installed">Installed</span></div>'
    '<p class="price-hint">All seven models priced individually — reveal with “Show pricing”.</p></div>'))

service_page(
  "new-garage-doors.html",
  "New Garage Doors West Vancouver | Modern, Carriage &amp; Glass Install",
  "New garage door installation in West Vancouver — modern full-view glass, carriage house, traditional steel and flush-panel doors, insulated for the West Coast. Expert measure, supply &amp; install.",
  "New Garage Door Installation in West Vancouver",
  "Your garage door is up to a third of your home's street view. We help you choose the right style, colour and insulation for the West Coast, then install it flawlessly.",
  [("p","From Dundarave character homes to glass-and-cedar new builds in the British Properties, the right garage door transforms a façade. We measure, supply and install doors that suit West Vancouver architecture and stand up to coastal weather — and we handle the old-door removal and disposal."),
   ("h2","Door styles we install"),
   ("ul",["<b>Modern full-view</b> — aluminum frame with frosted or clear glass; the signature West Coast contemporary look","<b>Carriage house</b> — warm wood-grain with decorative hardware; perfect for traditional and craftsman homes","<b>Traditional raised-panel steel</b> — timeless, durable and the best value","<b>Contemporary flush</b> — clean, minimal, no lines; pairs with concrete-and-cedar builds"]),
   ("h2","Insulation matters on the North Shore"),
   ("p","Many West Van garages sit under living space or double as gyms and studios. An insulated door (polyurethane core, higher R-value) keeps that space comfortable, cuts noise from rain and wind, and adds rigidity so the door lasts longer. We'll match the R-value to how you use the space."),
   ("h2","How the process works"),
   ("ul",["Free in-home measure &amp; design consult","Clear, written quote with styles and colours","Order &amp; schedule (most doors arrive in 2–4 weeks)","Professional one-day installation + opener setup","Walkthrough, balance test and warranty"]),
   ("h2","Transparent pricing"),
   ("p","New doors start at a clear, published price and scale with size, glass, insulation and design. No mystery quotes — reveal our starting prices with the footer toggle.")],
  [("How much is a new garage door installed?","Pricing scales with size, material, glass and insulation. Our entry, mid and premium tiers are published — tap “Show pricing” in the footer. Every quote is all-in, including removal of the old door."),
   ("How long until my new door is installed?","Most doors arrive within 2–4 weeks of ordering; installation itself is usually completed in a single day, including the opener."),
   ("Which door is best for a home above the water?","Near the ocean we recommend corrosion-resistant hardware and finishes, and often an insulated aluminum/glass or coated-steel door. We'll advise based on your exposure."),
   ("Do you install the opener too?","Yes — we can supply and install a matching LiftMaster® opener with your new door, or reuse a compatible existing unit.")],
  [("Openers","opener-installation.html"),("Strata &amp; townhomes","strata-townhomes.html"),("Garage door repair","garage-door-repair.html"),("Maintenance","maintenance-tune-up.html")],
  img="assets/img/service-install-960.webp",
  price_html=(
    '<h2>New door starting prices</h2>'
    '<div class="price-card" style="max-width:520px;margin-top:8px">'
    '<div class="price-row"><span class="pr-label">Entry — insulated steel, from</span><span class="price-tag" data-px="$3,647">From</span></div>'
    '<div class="price-row"><span class="pr-label">Mid — designer styles, from</span><span class="price-tag" data-px="$4,558">From</span></div>'
    '<div class="price-row"><span class="pr-label">Premium — full-view glass, from</span><span class="price-tag" data-px="$7,268">From</span></div>'
    '<p class="price-hint">Supplied + installed, old door hauled away. Reveal with “Show pricing”.</p></div>'))

service_page(
  "cable-roller-repair.html",
  "Garage Door Cable &amp; Roller Repair West Vancouver | Off-Track Doors",
  "Frayed cables, worn rollers, bent tracks and off-track garage doors repaired across West Vancouver &amp; the North Shore. Quiet, smooth operation restored — same-day in most cases.",
  "Cable, Roller &amp; Track Repair in West Vancouver",
  "The small parts that make a big noise. Frayed cables, worn nylon rollers and bent tracks throw a door off balance — and off its tracks. We set it right.",
  [("p","If your door has gone crooked, jumped its track, or sounds like it's grinding gravel, the culprit is usually the hardware: cables, rollers, hinges, bearings or the tracks themselves. These wear faster on the North Shore thanks to damp, salt air and heavy daily use."),
   ("h2","What we replace"),
   ("ul",["<b>Lift cables</b> — frayed, rusted or snapped (often paired with spring work)","<b>Nylon rollers</b> — the single best upgrade for a quiet door","<b>Bent or misaligned tracks</b> — straightened or replaced","<b>Worn hinges &amp; bearings</b> — eliminate squeaks and binding","<b>Cable drums</b> — re-seated and balanced after an off-track event"]),
   ("h2","Off-track doors"),
   ("p","A door comes off its track after an impact, a snapped cable, or a roller that finally gave out. <b>Don't run the opener</b> — it can bend panels and tracks. We carefully re-seat the door, find the root cause, and replace whatever failed so it doesn't happen again."),
   ("h2","Quiet, smooth, balanced"),
   ("p","After hardware work we re-balance the door, lubricate every moving part with a coastal-rated product, and test the opener's force settings — so it glides instead of grinds.")],
  [("Why is my garage door so noisy?","Usually worn steel rollers and dry hinges. Swapping to nylon rollers and proper lubrication makes most doors dramatically quieter — a popular, affordable fix."),
   ("My door is crooked / off its track — what should I do?","Stop using the opener and call us. Running it can cause expensive panel and track damage. We'll re-seat the door and fix the underlying cause, usually same-day."),
   ("How long do garage door cables last?","Typically 8–12 years, less in damp coastal conditions. We recommend replacing cables together with springs since they wear at a similar rate."),
   ("Do you carry parts on the truck?","Yes — cables, rollers, hinges and common track hardware are stocked, so most cable and roller jobs are completed in a single visit.")],
  [("Spring repair","spring-repair.html"),("Garage door repair","garage-door-repair.html"),("Maintenance tune-up","maintenance-tune-up.html"),("Openers","opener-installation.html")],
  img="assets/img/service-cable-960.webp")

service_page(
  "maintenance-tune-up.html",
  "Garage Door Maintenance &amp; Tune-Up West Vancouver | 25-Point Service",
  "Prevent breakdowns with a 25-point garage door tune-up in West Vancouver — balance, lubrication, sensor alignment and coastal rust prevention. Single homes &amp; strata programs.",
  "Garage Door Tune-Ups &amp; Maintenance in West Vancouver",
  "The cheapest repair is the one you prevent. A yearly tune-up keeps your door quiet, safe and reliable — and catches a $30 part before it becomes a $700 emergency.",
  [("p","Garage doors are easy to ignore until they fail at the worst moment. A simple annual service extends the life of springs, cables and the opener, keeps the door quiet, and — most importantly — keeps the safety systems working. It's also the best defence against North Shore damp and salt-air corrosion."),
   ("h2","Our 25-point tune-up"),
   ("ul",["Test and adjust door <b>balance</b> (the key to spring &amp; opener life)","Lubricate springs, rollers, hinges and bearings with coastal-rated product","Inspect cables and drums for fraying and rust","Check and tighten all hardware and brackets","Align and test the photo-eye <b>safety sensors</b>","Test auto-reverse force settings (a critical safety check)","Inspect rollers and tracks for wear and alignment","Check weather-seal and bottom astragal","Full opener health check + remote/myQ test"]),
   ("h2","Why it pays off here"),
   ("p","Salt air and heavy rain accelerate rust on cables and springs; big luxury doors put more load on every part. A tune-up spots corrosion and wear early, so you replace one worn roller on your schedule instead of a snapped cable on a Sunday."),
   ("h2","Strata &amp; multi-unit programs"),
   ("p","We run scheduled maintenance programs for strata corporations and townhome complexes across West Vancouver — consistent service across every unit, documented reports for council, and priority response when something does go wrong.")],
  [("How often should I service my garage door?","Once a year for most homes; twice a year for heavy-use doors, homes near the ocean, or large/heavy luxury doors. Strata programs are typically annual per unit."),
   ("What does a tune-up cost?","It's a flat, affordable rate per door, with multi-door and strata discounts. Call or text for current pricing — it's a fraction of an emergency repair."),
   ("Will a tune-up make my door quieter?","Almost always. Lubrication, balance adjustment and tightening hardware remove most of the rattles and grinding — and we'll flag worn rollers if a swap would help."),
   ("Do you service strata and townhome complexes?","Yes — scheduled multi-unit maintenance with consolidated invoicing and council-ready reports is a core part of what we do.")],
  [("Strata &amp; townhomes","strata-townhomes.html"),("Spring repair","spring-repair.html"),("Cables &amp; rollers","cable-roller-repair.html"),("Garage door repair","garage-door-repair.html")],
  img="assets/img/service-maintenance-960.webp")

# strata as a service page
service_page(
  "strata-townhomes.html",
  "Strata &amp; Townhome Garage Door Service West Vancouver | Property Managers",
  "Garage door service for strata corporations, property managers and townhome complexes across West Vancouver &amp; the North Shore — scheduled maintenance, matching doors, consolidated invoicing.",
  "Strata &amp; Townhome Garage Door Service",
  "A garage door partner your strata council and property managers can actually rely on — from a single unit to an entire complex, fully documented.",
  [("p","Managing garage doors across a townhome complex or strata building is a headache when every unit needs a different contractor and every invoice looks different. We're the single, dependable point of contact for garage doors across West Vancouver and the North Shore — responsive, professional and easy to administrate."),
   ("h2","Built for councils &amp; property managers"),
   ("ul",["Scheduled multi-unit <b>maintenance programs</b> with documented reports","Priority emergency response for residents","<b>Matching doors &amp; hardware</b> across units for a consistent look","Clear quotes, purchase orders and <b>consolidated invoicing</b>","Licensed (business licence), insured &amp; WorkSafeBC-covered","Detailed records for depreciation reports and council minutes"]),
   ("h2","From one unit to the whole complex"),
   ("p","Need a single resident's spring fixed today, or a phased replacement of 40 aging doors across a complex? We scale to either — with a quote your council can approve and a schedule that minimizes disruption to residents."),
   ("h2","Why managers choose us"),
   ("p","No call-centre runaround, no surprise charges, and paperwork that makes your job easier. We treat every building like it's our own, and we keep the same crew on your property so they know its quirks.")],
  [("Do you offer scheduled maintenance contracts?","Yes — annual or semi-annual programs per unit, with documented inspection reports for council records and depreciation planning."),
   ("Can you match existing doors across a complex?","In most cases, yes. We'll source doors and hardware to match the existing look, or propose a coordinated upgrade if models are discontinued."),
   ("How do you handle invoicing for stratas?","We provide clear quotes and POs and can consolidate invoicing across multiple units or work orders to simplify your bookkeeping."),
   ("Do you respond to resident emergencies?","Yes — strata clients get priority same-day response for urgent issues like a door stuck open or a resident blocked in.")],
  [("Maintenance programs","maintenance-tune-up.html"),("New garage doors","new-garage-doors.html"),("Openers","opener-installation.html"),("Become a partner","become-a-partner.html")],
  img="assets/img/strata-960.webp")

# ============================ AREA PAGES ============================

area_page(
  "north-vancouver.html",
  "Garage Door Repair North Vancouver | Springs, Openers &amp; New Doors",
  "Same-day garage door repair in North Vancouver — Lynn Valley, Deep Cove, Lonsdale, Edgemont &amp; Capilano. Springs, cables, openers and new doors. Licensed, insured &amp; local.",
  "Garage Door Repair in North Vancouver",
  "From Lower Lonsdale to Lynn Valley and Deep Cove, we're the North Shore's family-owned garage door team — often at your door the same day.",
  [("p","North Vancouver's mix of post-war bungalows, Lynn Valley family homes and new Lonsdale townhomes means we see every kind of garage door — and every kind of North Shore weather wearing them down. We cover all of North Van with a stocked truck for fast, one-visit repairs."),
   ("h2","Neighbourhoods we serve in North Van"),
   ("ul",["Lynn Valley &amp; Lynn Creek","Deep Cove &amp; Dollarton","Lonsdale (Lower &amp; Central) and the Shipyards","Edgemont Village &amp; Capilano","Grand Boulevard, Norgate, Pemberton Heights"]),
   ("h2","Common North Vancouver door problems"),
   ("p","The rainforest climate up toward Lynn Valley and Mount Seymour is brutal on hardware — we see rusted cables, swollen wood doors and seized rollers more here than almost anywhere. Cold snaps also stiffen grease and thicken oil in openers, causing winter no-starts. We use coastal-rated parts and lubricants built for exactly this."),
   ("h2","Springs, openers, cables &amp; new doors"),
   ("p","Everything we do in West Vancouver we do in North Van: same-day spring replacement, LiftMaster® opener installs, cable and roller repair, tune-ups, and full new-door installation — all at upfront, published prices.")],
  [("Do you really cover all of North Vancouver?","Yes — from Lower Lonsdale to Deep Cove and up into Lynn Valley and Seymour. Our trucks are on the North Shore daily, so same-day service is common."),
   ("How fast can you get to me in North Van?","For urgent issues we keep same-day slots. Call or text and we'll give you an honest arrival window."),
   ("Why do North Shore doors rust so fast?","Heavy rainfall and humidity, plus salt air near the inlet, corrode cables and springs faster than inland. Annual maintenance with corrosion-resistant parts is the fix."),
   ("Are your prices the same in North Vancouver?","Yes — the same upfront, published pricing applies across West and North Vancouver. Reveal it with the footer toggle.")],
  [("Spring repair","spring-repair.html"),("Garage door repair","garage-door-repair.html"),("Openers","opener-installation.html"),("West Vancouver","index.html")],
  img="assets/img/gallery-1-960.webp")

area_page(
  "british-properties.html",
  "Garage Door Service British Properties | Luxury Homes, West Vancouver",
  "Garage door repair &amp; installation in the British Properties, West Vancouver — large, heavy and custom doors, glass &amp; carriage styles, quiet belt-drive openers. Discreet, professional service.",
  "Garage Door Service in the British Properties",
  "Large estate doors, custom glass, and triple garages on steep driveways — the British Properties needs a garage door team that handles premium work discreetly and properly.",
  [("p","The British Properties and Chartwell are home to some of West Vancouver's largest and most distinctive houses — and their garage doors are correspondingly big, heavy and often custom. Oversized doors put extra load on springs, cables and openers, so the right parts and a properly balanced system matter even more here."),
   ("h2","What estate homes need"),
   ("ul",["<b>High-cycle springs</b> sized for heavy, oversized and triple doors","<b>Quiet belt-drive or wall-mount openers</b> for homes with rooms above the garage","Custom <b>full-view glass</b> and <b>carriage-style</b> doors to match architecture","Corrosion-resistant hardware for elevated, exposed lots","Discreet, scheduled, by-appointment service"]),
   ("h2","Steep driveways &amp; big doors"),
   ("p","Many Properties homes sit on steep, winding lots up toward Cypress, with multi-car garages. Heavier doors wear springs faster and demand stronger openers — we size every component to the actual door, not a one-size guess, so it runs smoothly for years."),
   ("h2","Repairs, replacements &amp; upgrades"),
   ("p","Whether it's an urgent spring on a Saturday or a coordinated upgrade of three custom doors, we deliver estate-grade work with upfront pricing and a workmanship warranty.")],
  [("Why do large doors break springs sooner?","More weight means more cycles of stress on the spring. We fit high-cycle springs rated for the actual door weight, which last far longer on big estate doors."),
   ("Can you match a custom or designer door?","Yes — we install full-view glass, carriage and custom-finish doors, and can match or coordinate with existing architecture."),
   ("Do you work by appointment for privacy?","Absolutely — we schedule discreet, by-appointment visits and keep the same crew on your property."),
   ("Which opener is best for a home with rooms above the garage?","A belt-drive or wall-mount (jackshaft) opener — both are very quiet, so noise and vibration don't carry into living space above.")],
  [("New garage doors","new-garage-doors.html"),("Spring repair","spring-repair.html"),("Openers","opener-installation.html"),("West Vancouver","index.html")],
  img="assets/img/gallery-2-960.webp")

area_page(
  "ambleside-dundarave.html",
  "Garage Door Repair Ambleside &amp; Dundarave | West Vancouver",
  "Local garage door repair &amp; installation in Ambleside and Dundarave, West Vancouver — character homes, laneway garages and modern builds. Same-day springs, openers &amp; new doors.",
  "Garage Door Service in Ambleside &amp; Dundarave",
  "From heritage character homes near Dundarave Pier to modern builds along Marine Drive, we keep Ambleside and Dundarave garages running smoothly.",
  [("p","Ambleside and Dundarave are the heart of West Vancouver — walkable villages, a mix of 1940s character homes, mid-century houses and sleek new builds, many with tucked-away or laneway garages. That variety means everything from original wood doors to the latest glass-and-aluminum, and we service all of them."),
   ("h2","What we see in these neighbourhoods"),
   ("ul",["Older <b>wood doors</b> that swell and stick in the wet season","Tight, lane-access garages that need careful track work","Heritage and character homes wanting <b>carriage-style</b> replacements","Modern Marine Drive builds wanting <b>full-view glass</b>","Salt-air corrosion on cables and springs near the seawall"]),
   ("h2","Close to the water = faster wear"),
   ("p","A block from the Dundarave or Ambleside seawall, salt air corrodes springs and cables noticeably faster. We fit corrosion-resistant hardware and recommend an annual tune-up to catch rust before it strands you."),
   ("h2","Everything, locally"),
   ("p","Same-day spring and cable repair, quiet LiftMaster® openers, tune-ups and full new-door installs — all with upfront, published pricing, minutes from your door.")],
  [("Do you service older character homes?","Yes — we're used to original wood doors and non-standard openings. We can repair what's there or fit a carriage-style replacement that suits a heritage façade."),
   ("My wood door sticks in winter — can you help?","Often, yes. Swelling, worn rollers and balance issues are all fixable; if the door is past its life we'll show you matching replacement options."),
   ("Can you work with tight laneway garages?","Definitely — we handle low-headroom and tight side-room track setups common in Ambleside and Dundarave lanes."),
   ("How quickly can you come?","We're local to West Van, so same-day service in Ambleside and Dundarave is common. Call or text for a window.")],
  [("Spring repair","spring-repair.html"),("New garage doors","new-garage-doors.html"),("Maintenance","maintenance-tune-up.html"),("West Vancouver","index.html")],
  img="assets/img/gallery-3-960.webp")

area_page(
  "horseshoe-bay.html",
  "Garage Door Repair Horseshoe Bay &amp; Caulfeild | West Vancouver",
  "Garage door repair &amp; installation in Horseshoe Bay, Caulfeild, Eagle Harbour and West Bay — coastal-grade hardware against salt air. Same-day springs, openers &amp; new doors.",
  "Garage Door Service in Horseshoe Bay &amp; Caulfeild",
  "Right on the water by the ferry terminal, Horseshoe Bay, Caulfeild and Eagle Harbour are beautiful — and tough on garage door hardware. We come prepared.",
  [("p","The far west of West Vancouver — Horseshoe Bay, Caulfeild, Eagle Harbour and West Bay — sits directly on Howe Sound. The views are spectacular and the salt air is relentless, which makes corrosion-resistant parts and regular maintenance essential, not optional."),
   ("h2","Coastal conditions, coastal-grade parts"),
   ("ul",["Salt-air <b>corrosion</b> on springs, cables and fasteners — we fit galvanized/coated hardware","Damp that <b>swells wood doors</b> and seizes rollers","Steep, rocky driveways and detached garages","Exposed, windy lots that stress door seals and panels"]),
   ("h2","Same-day, even out here"),
   ("p","Being at the end of Marine Drive doesn't mean waiting days for service. We're on the West Van side daily and keep parts stocked, so springs, cables and openers are usually a same-day, one-visit fix in Horseshoe Bay and Caulfeild."),
   ("h2","Repairs, new doors &amp; prevention"),
   ("p","We handle urgent repairs, full new-door installation suited to a seaside setting, and — the smart move out here — annual maintenance that catches salt-air rust before it snaps a cable.")],
  [("Does salt air really damage garage doors?","Yes — noticeably. Springs and cables near the water can corrode years faster. Coastal-grade hardware and an annual tune-up dramatically extend their life."),
   ("Do you come all the way to Horseshoe Bay?","Yes — Horseshoe Bay, Caulfeild, Eagle Harbour and West Bay are part of our core West Vancouver service area, with same-day availability."),
   ("What door is best for a seaside home?","Corrosion-resistant aluminum/glass or coated-steel doors with stainless or galvanized hardware. We'll recommend based on how exposed your home is."),
   ("How often should a seaside door be serviced?","Twice a year is wise this close to the water, to stay ahead of salt-air corrosion on cables and springs.")],
  [("Spring repair","spring-repair.html"),("Maintenance tune-up","maintenance-tune-up.html"),("New garage doors","new-garage-doors.html"),("West Vancouver","index.html")],
  img="assets/img/gallery-4-960.webp")

area_page(
  "lions-bay-bowen-island.html",
  "Garage Door Repair Lions Bay &amp; Bowen Island | Sea-to-Sky",
  "Garage door repair &amp; installation for Lions Bay and Bowen Island — mountainside and island homes, coastal-grade hardware, scheduled visits. Springs, openers &amp; new doors.",
  "Garage Door Service in Lions Bay &amp; Bowen Island",
  "Mountainside Lions Bay and island-living Bowen are worth the trip — we plan our visits so even the far corners of the North Shore get proper garage door service.",
  [("p","Lions Bay clings to the Sea-to-Sky mountainside north of Horseshoe Bay, and Bowen Island is a short ferry away across Howe Sound. Both are gorgeous, both are exposed to coastal weather, and both deserve more than a contractor who won't make the trip. We schedule efficient visits so you get the same quality service as the rest of West Van."),
   ("h2","What these communities need"),
   ("ul",["<b>Coastal-grade, corrosion-resistant</b> springs, cables and hardware","Openers with <b>battery backup</b> for storm-season outages","Doors and seals built for wind and driving rain","Planned, scheduled visits (especially for Bowen ferry trips)","Detached-garage and steep-driveway expertise"]),
   ("h2","Planned visits, full service"),
   ("p","For Lions Bay and Bowen we coordinate appointments to make the trip count — bring the right parts the first time and, where possible, batch nearby jobs. You still get upfront pricing, quality parts and a workmanship warranty."),
   ("h2","Storm-ready openers"),
   ("p","Power outages are a fact of life on the exposed coast. We strongly recommend LiftMaster® openers with battery backup here, so a winter storm never traps your car in the garage.")],
  [("Do you really service Bowen Island?","Yes — we schedule Bowen visits around the ferry and aim to bring everything needed to finish in one trip. Call or text and we'll arrange a date."),
   ("Can you reach Lions Bay?","Yes — Lions Bay is on our Sea-to-Sky route just past Horseshoe Bay. We plan visits to keep it efficient for you."),
   ("Is service more expensive out here?","Our parts and labour prices are the same; for Bowen Island a scheduled trip simply means planning ahead rather than same-day. We'll be upfront about timing."),
   ("Why do you recommend battery backup here?","These exposed coastal communities lose power in winter storms. A battery-backup opener keeps your door working — and your car free — during outages.")],
  [("Openers","opener-installation.html"),("Spring repair","spring-repair.html"),("Maintenance","maintenance-tune-up.html"),("West Vancouver","index.html")],
  img="assets/img/hero-carriage.webp")

print("\nservice + area pages built")
