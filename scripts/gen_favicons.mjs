// gen_favicons.mjs — rasterize assets/img/favicon.svg to a 512px PNG via the
// globally-installed Playwright Chromium (no network). Pillow then downsizes
// (scripts/gen_favicons.py) to 192/96/48/32 + favicon.ico.
//   node scripts/gen_favicons.mjs && python3 scripts/gen_favicons.py
import { createRequire } from 'module';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const svg = readFileSync(resolve(ROOT, 'assets/img/favicon.svg'), 'utf8');
const html = `<!doctype html><html><head><style>*{margin:0}html,body{width:512px;height:512px;background:transparent}svg{width:512px;height:512px;display:block}</style></head><body>${svg}</body></html>`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 512, height: 512 } });
await page.setContent(html, { waitUntil: 'load' });
await page.screenshot({ path: resolve(ROOT, 'assets/img/icon-512.png'), omitBackground: true });
await browser.close();
console.log('✓ assets/img/icon-512.png (512x512)');
