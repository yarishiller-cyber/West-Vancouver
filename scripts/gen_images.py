#!/usr/bin/env python3
"""Generate website imagery with Gemini 2.5 Flash Image ("nano banana").

Usage:
  python3 scripts/gen_images.py <name>          # generate a single image by key
  python3 scripts/gen_images.py --all           # generate everything missing
  python3 scripts/gen_images.py --all --force    # regenerate everything
"""
import base64
import io
import json
import os
import sys
import time
import urllib.request
import urllib.error
from PIL import Image

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MODEL = "gemini-2.5-flash-image"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "img")

# Shared style guidance appended to every prompt for a cohesive, premium look.
STYLE = (
    " Ultra-realistic professional photograph, shot on a full-frame DSLR, 35mm, "
    "natural soft lighting, high dynamic range, crisp sharp focus, true-to-life colors, "
    "editorial real-estate photography quality, no text, no watermarks, no logos, no people's faces distorted."
)

PROMPTS = {
    # ---- Heroes ----
    "hero-home": (
        "A stunning luxury West Coast modern home in West Vancouver, British Columbia at golden hour. "
        "A wide double two-car garage with a contemporary flush dark charcoal aluminum garage door with "
        "frosted glass accent panels. Cedar wood soffits, stone and glass facade, lush green landscaping, "
        "ocean and forested North Shore mountains softly in the background. Clean modern driveway. "
        "Warm inviting exterior lights just turning on. 16:9 cinematic wide shot." + STYLE
    ),
    "hero-carriage": (
        "A beautiful Craftsman-style home in West Vancouver with two warm wood-grain carriage-house garage "
        "doors with black decorative hardware and small top window panes. Manicured front garden, blue sky, "
        "tall evergreen trees. Bright clean daytime real-estate photo. 16:9 wide." + STYLE
    ),
    # ---- Family / trust ----
    "family-team": (
        "A friendly family-owned garage door service team of three technicians in clean plain solid navy-blue "
        "polo shirts with absolutely no text, no embroidery and no logo on the shirts, standing confidently in "
        "a residential driveway in front of an open garage, smiling, arms relaxed. A father and two adult sons "
        "vibe, approachable and trustworthy. Bright daylight, North Shore residential street. Group portrait. "
        "4:3." + STYLE
    ),
    "service-van": (
        "A clean white branded service van parked in a residential West Vancouver driveway next to a modern "
        "garage, ladders and equipment, professional local contractor look, blank white panel on the van side "
        "(no text or logo). Bright morning light. 4:3." + STYLE
    ),
    # ---- Services ----
    "service-repair": (
        "A professional garage door technician in a navy uniform kneeling and repairing the bottom bracket and "
        "track of a residential garage door, using a power drill, focused and careful. Inside a tidy suburban "
        "garage, natural light from open door. Close documentary shot. 4:3." + STYLE
    ),
    "service-spring": (
        "Extreme close-up of a hand using a winding bar to adjust a black torsion spring on a steel shaft above "
        "a residential garage door, mechanical detail, depth of field background blur. 4:3." + STYLE
    ),
    "service-opener": (
        "A technician installing a modern white garage door opener motor unit mounted to a garage ceiling, "
        "belt-drive rail visible, looking up, clean residential garage interior. 4:3." + STYLE
    ),
    "service-install": (
        "Two technicians installing a brand-new modern sectional garage door panel into the track of a "
        "residential garage, teamwork, bright daylight from the open doorway. 4:3." + STYLE
    ),
    "service-maintenance": (
        "A technician lubricating and inspecting the rollers and hinges of a residential garage door with a "
        "clipboard tune-up checklist nearby, careful maintenance work, clean garage. 4:3." + STYLE
    ),
    "service-cable": (
        "Close-up of a technician's gloved hands re-threading a steel lift cable onto the drum and roller of a "
        "residential garage door track, mechanical detail. 4:3." + STYLE
    ),
    # ---- Strata ----
    "strata": (
        "A handsome row of modern West Coast townhomes / strata complex in West Vancouver, each with its own "
        "matching contemporary garage door, cedar and dark-panel facades, tidy shared driveway and landscaping, "
        "blue sky. Wide architectural shot. 16:9." + STYLE
    ),
    # ---- Door styles ----
    "door-modern": (
        "Product-style architectural photo of a single contemporary full-view garage door: black aluminum "
        "frame with large frosted glass panels on a modern home facade, clean and minimal. 1:1 square." + STYLE
    ),
    "door-carriage": (
        "Product-style photo of a single warm wood-grain carriage-house garage door with black strap hinges and "
        "handles and a row of small top windows, on a craftsman home facade. 1:1 square." + STYLE
    ),
    "door-traditional": (
        "Product-style photo of a single classic white steel raised-panel garage door with a row of decorative "
        "top windows on a traditional home facade. 1:1 square." + STYLE
    ),
    "door-flush": (
        "Product-style photo of a single sleek dark charcoal flush-panel modern garage door, no windows, smooth "
        "matte finish, on a minimalist concrete and cedar home facade. 1:1 square." + STYLE
    ),
    # ---- Openers (generic realistic product shots, no brand text) ----
    "opener-belt": (
        "Clean product photo of a premium white residential garage door opener motor head unit with a small "
        "integrated camera lens and dual LED side lights, belt-drive, on a soft light-grey studio gradient "
        "background. No text or logos. 1:1 square." + STYLE
    ),
    "opener-wallmount": (
        "Clean product photo of a compact white wall-mount / jackshaft residential garage door opener unit that "
        "mounts beside the door on the wall, on a soft light-grey studio gradient background. No text or logos. "
        "1:1 square." + STYLE
    ),
    "opener-chain": (
        "Clean product photo of a sturdy grey-and-black residential chain-drive garage door opener motor head "
        "unit on a soft light-grey studio gradient background. No text or logos. 1:1 square." + STYLE
    ),
    # ---- Springs (product close-ups) ----
    "spring-standard": (
        "Clean product photo of a single real garage-door TORSION spring: a long horizontal cylindrical tube of "
        "tightly wound black steel wire with the coils packed closely together touching each other, threaded onto "
        "a metal torsion shaft with a black cast-iron winding cone fitting at the end. Horizontal orientation, "
        "soft light-grey studio gradient background. Photorealistic hardware. No text. 1:1 square." + STYLE
    ),
    "spring-highcycle": (
        "Clean product photo of a single heavy-duty oil-tempered garage-door TORSION spring: a long horizontal "
        "cylindrical coil of tightly wound galvanized zinc-grey steel wire, coils tightly packed together, on a "
        "steel torsion shaft with a winding cone at the end. Horizontal orientation, soft light-grey studio "
        "gradient background. Photorealistic. No text. 1:1 square." + STYLE
    ),
    "spring-premium": (
        "Clean product photo of two premium heavy-duty garage-door TORSION springs mounted side by side on a "
        "single long steel torsion shaft above where a garage door would be: each is a long cylindrical coil of "
        "tightly wound black powder-coated steel wire with red cast winding cones in the centre. Horizontal "
        "orientation, soft light-grey studio gradient background. Photorealistic. No text. 1:1 square." + STYLE
    ),
    # ---- CTA / texture ----
    "cta-bg": (
        "A moody twilight photo of a beautiful West Vancouver modern home with a warmly lit garage and driveway, "
        "deep blue dusk sky, cinematic, slightly dark so white text reads on top. 16:9 wide." + STYLE
    ),
    # ---- Gallery (before/after & finished installs) ----
    "gallery-1": (
        "A finished installation of an elegant dark modern garage door on a West Vancouver luxury home, "
        "twilight, warm lights. 4:3." + STYLE
    ),
    "gallery-2": (
        "A finished installation of double white carriage-house garage doors on a large family home with a "
        "circular driveway. Daytime. 4:3." + STYLE
    ),
    "gallery-3": (
        "A finished installation of a full-view aluminum and glass modern garage door on a contemporary "
        "concrete home. Daytime. 4:3." + STYLE
    ),
    "gallery-4": (
        "A finished installation of warm cedar wood-look garage doors on a West Coast contemporary home "
        "surrounded by evergreens. 4:3." + STYLE
    ),
}


# Aspect ratio + final max width (px) per image category.
def aspect_for(name):
    if name.startswith(("hero", "cta", "strata")):
        return "16:9", 1600
    if name.startswith(("door", "opener", "spring")):
        return "1:1", 900
    return "4:3", 1200


def compress(png_bytes, out_path, max_w):
    im = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    if im.width > max_w:
        h = round(im.height * max_w / im.width)
        im = im.resize((max_w, h), Image.LANCZOS)
    im.save(out_path, "JPEG", quality=82, optimize=True, progressive=True)
    return os.path.getsize(out_path)


def generate(name, prompt, force=False):
    out_path = os.path.join(OUT_DIR, f"{name}.jpg")
    if os.path.exists(out_path) and not force:
        print(f"  skip {name} (exists)")
        return True
    aspect, max_w = aspect_for(name)
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"],
                             "imageConfig": {"aspectRatio": aspect}},
    }).encode()
    for attempt in range(4):
        try:
            req = urllib.request.Request(ENDPOINT, data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r)
            parts = data["candidates"][0]["content"]["parts"]
            for p in parts:
                inline = p.get("inlineData") or p.get("inline_data")
                if inline and inline.get("data"):
                    img = base64.b64decode(inline["data"])
                    size = compress(img, out_path, max_w)
                    print(f"  OK   {name} ({aspect}) -> {size//1024} KB")
                    return True
            print(f"  WARN {name}: no image in response: {json.dumps(data)[:300]}")
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:300]
            print(f"  ERR  {name} HTTP {e.code}: {msg}")
            if e.code in (429, 500, 503):
                time.sleep(2 ** attempt * 2)
                continue
            return False
        except Exception as e:
            print(f"  ERR  {name}: {e}")
            time.sleep(2 ** attempt * 2)
    return False


def main():
    if not API_KEY:
        print("ERROR: set GEMINI_API_KEY env var")
        sys.exit(1)
    os.makedirs(OUT_DIR, exist_ok=True)
    args = sys.argv[1:]
    force = "--force" in args
    args = [a for a in args if a != "--force"]
    if args and args[0] == "--all":
        keys = list(PROMPTS.keys())
    elif args:
        keys = args
    else:
        print(__doc__)
        sys.exit(0)
    ok = 0
    for k in keys:
        if k not in PROMPTS:
            print(f"  unknown key: {k}")
            continue
        if generate(k, PROMPTS[k], force=force):
            ok += 1
        time.sleep(1)
    print(f"\nDone: {ok}/{len(keys)} succeeded")


if __name__ == "__main__":
    main()
