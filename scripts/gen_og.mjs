// gen_og.mjs — generate branded 1200x630 Open Graph cards, one per page.
// Uses the globally-installed Playwright + pre-installed Chromium (no network needed
// for images; fonts fall back to a system stack if Google Fonts can't load).
//   node scripts/gen_og.mjs
import { createRequire } from 'module';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
import { readFileSync, existsSync, mkdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const IMG = (f) => 'file://' + resolve(ROOT, 'assets/img', f);

const PAGES = [
  ['home',                 'Garage Door Repair &amp; Installation', 'West Vancouver &amp; the North Shore',       'hero-brand.webp'],
  ['garage-door-repair',   'Garage Door Repair',                    'Same-day repair across the North Shore',      'service-repair.webp'],
  ['spring-repair',        'Spring Replacement',                    'Torsion &amp; extension springs — same day',  'service-spring.webp'],
  ['opener-installation',  'Openers &amp; Smart Control',           'LiftMaster® authorized dealer',               'service-opener.webp'],
  ['new-garage-doors',     'New Garage Doors',                      'Modern, carriage, full-view glass &amp; steel','door-modern.webp'],
  ['cable-roller-repair',  'Cables, Rollers &amp; Tracks',          'Quiet, smooth-gliding doors again',           'service-cable.webp'],
  ['maintenance-tune-up',  'Tune-Ups &amp; Maintenance',            '25-point garage door safety inspection',      'service-maintenance.webp'],
  ['strata-townhomes',     'Strata &amp; Townhome Service',         'Multi-unit, documented, on schedule',         'strata.webp'],
  ['service-areas',        'Service Areas',                         'Across West Vancouver &amp; the North Shore', 'gallery-2.webp'],
  ['north-vancouver',      'North Vancouver',                       'Lynn Valley · Deep Cove · Lonsdale',          'gallery-3.webp'],
  ['british-properties',   'British Properties',                    'Estate doors &amp; hillside driveways',       'gallery-2.webp'],
  ['ambleside-dundarave',  'Ambleside &amp; Dundarave',             'Seawall character homes, salt-air wear',      'gallery-1.webp'],
  ['horseshoe-bay',        'Horseshoe Bay &amp; Caulfeild',         'Seaside doors — Eagle Harbour &amp; West Bay','gallery-4.webp'],
  ['lions-bay-bowen-island','Lions Bay &amp; Bowen Island',         'Sea-to-Sky &amp; ferry-scheduled visits',     'hero-carriage.webp'],
  ['become-a-partner',     'Become a Partner',                      'For strata councils &amp; property managers', 'family-team.webp'],
];

const LOGO = `<svg width="60" height="60" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="2" y="2" width="44" height="44" rx="11" fill="#0b2545"/><path d="M9 22 24 11l15 11v15a1 1 0 0 1-1 1H10a1 1 0 0 1-1-1V22Z" fill="#13315c"/><path d="M9 22 24 11l15 11" stroke="#e0a64e" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><rect x="14" y="24" width="20" height="14" rx="1.5" fill="#fff"/><path d="M14 28h20M14 32h20M14 36h20M20 24v14M28 24v14" stroke="#cdd9ea" stroke-width="1.2"/><rect x="14" y="24" width="20" height="14" rx="1.5" stroke="#e0a64e" stroke-width="1.6"/></svg>`;

const card = (title, sub, bg) => `<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
*{margin:0;box-sizing:border-box}
html,body{width:1200px;height:630px}
.card{position:relative;width:1200px;height:630px;overflow:hidden;background:#0b2545;font-family:'Inter',system-ui,'Segoe UI',sans-serif}
.bg{position:absolute;inset:0;background:url('${bg}') center/cover no-repeat;opacity:.32}
.grad{position:absolute;inset:0;background:linear-gradient(105deg,#0b2545 32%,rgba(11,37,69,.86) 55%,rgba(19,49,92,.55) 100%)}
.edge{position:absolute;left:0;top:0;bottom:0;width:14px;background:#e0a64e}
.wrap{position:absolute;inset:0;padding:64px 72px;display:flex;flex-direction:column;justify-content:space-between}
.brand{display:flex;align-items:center;gap:16px}
.brand b{font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;color:#fff;font-size:26px;letter-spacing:.2px;line-height:1}
.brand span{color:#e0a64e;font-weight:700;font-size:16px;display:block;margin-top:3px;letter-spacing:.4px}
.mid{max-width:820px}
.eyebrow{color:#e0a64e;font-weight:600;font-size:20px;letter-spacing:2px;text-transform:uppercase;margin-bottom:14px}
h1{font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;color:#fff;font-size:66px;line-height:1.04;letter-spacing:-1px}
.sub{color:#cdd9ea;font-size:27px;margin-top:18px;font-weight:400}
.foot{display:flex;align-items:center;gap:22px}
.chip{display:flex;align-items:center;gap:12px;background:#e0a64e;color:#0b2545;font-weight:800;font-size:26px;padding:15px 28px;border-radius:999px;font-family:'Plus Jakarta Sans',sans-serif}
.badges{color:#9fb3cc;font-size:19px;font-weight:600;letter-spacing:.3px}
.dot{color:#e0a64e}
</style></head><body>
<div class="card">
  <div class="bg"></div><div class="grad"></div><div class="edge"></div>
  <div class="wrap">
    <div class="brand">${LOGO}<div><b>North Shore</b><span>GARAGE DOORS</span></div></div>
    <div class="mid">
      <div class="eyebrow">West Vancouver · North Shore</div>
      <h1>${title}</h1>
      <div class="sub">${sub}</div>
    </div>
    <div class="foot">
      <div class="chip">📞 (778) 800-0769</div>
      <div class="badges">Licensed <span class="dot">·</span> Insured <span class="dot">·</span> WorkSafeBC <span class="dot">·</span> Same-Day</div>
    </div>
  </div>
</div></body></html>`;

const outDir = resolve(ROOT, 'og');
if (!existsSync(outDir)) mkdirSync(outDir);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
let n = 0;
for (const [slug, title, sub, bgFile] of PAGES) {
  const bg = existsSync(resolve(ROOT, 'assets/img', bgFile)) ? IMG(bgFile) : '';
  await page.setContent(card(title, sub, bg), { waitUntil: 'load' });
  try { await page.evaluate(() => document.fonts.ready); } catch {}
  await page.waitForTimeout(350);
  await page.screenshot({ path: resolve(outDir, `${slug}.jpg`), type: 'jpeg', quality: 82 });
  n++; console.log(`✓ og/${slug}.jpg`);
}
await browser.close();
console.log(`Done — ${n} OG cards.`);
