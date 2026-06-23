#!/usr/bin/env python3
"""Generate the brand hero imagery (garage door + branded van + technician) per
_shared/playbooks/BRAND-IMAGERY.md, in desktop (landscape) + mobile (portrait),
plus a 1200x630 OG image. Outputs optimized WebP straight into assets/img.

  GEMINI_API_KEY=... python3 scripts/gen_brand.py [--force]
"""
import base64, json, os, sys, time, urllib.request
from PIL import Image

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MODEL = "gemini-2.5-flash-image"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
ROOT = os.path.join(os.path.dirname(__file__), "..")
IMG = os.path.join(ROOT, "assets", "img")
SCRATCH = os.path.join(ROOT, "scratch")

REALISM = (
    " Candid documentary photograph, shot on Canon EOS R6, 35mm f/1.8 lens, ISO 400, shot on "
    "Kodak Portra 400 film with natural film grain. Overcast Pacific-Northwest daylight, soft "
    "natural light, realistic shadows, natural colour grading. True-to-life textures, slight "
    "sensor noise, natural depth of field, slightly imperfect amateur framing. "
    "Negative: no plastic or waxy skin, no over-smoothing, no CGI or 3D-render look, no cartoon, "
    "no warped hands or extra fingers, no unnatural symmetry, no text artifacts, no "
    "over-saturation, no HDR glow, not a stock photo."
)
SCENE = (
    "A real residential West Vancouver driveway on the North Shore with cedar-and-glass West "
    "Coast modern homes and tall evergreens. An open double sectional garage door (dark charcoal "
    "with frosted glass accents). A navy-blue service van with a tasteful gold pinstripe and the "
    "small email 'info@westvangaragedoors.ca' on the side panel (no phone number) parked in the "
    "driveway. A friendly male garage-door technician in a clean navy-blue work uniform holding a "
    "cordless drill, mid-job by the door."
)

JOBS = {
    "hero-brand":     (SCENE + " Wide landscape composition with the door, van and technician all visible." + REALISM, "16:9", 1600),
    "hero-brand-portrait": (SCENE + " Vertical portrait composition framed for a phone screen, technician prominent in foreground, van and open garage door behind." + REALISM, "3:4", 1000),
}

def call(prompt, aspect, ref=None):
    parts = [{"text": prompt}]
    if ref:
        b64 = base64.b64encode(open(ref, "rb").read()).decode()
        parts.append({"inlineData": {"mimeType": "image/png", "data": b64}})
    body = json.dumps({"contents": [{"parts": parts}],
                       "generationConfig": {"responseModalities": ["IMAGE"],
                                            "imageConfig": {"aspectRatio": aspect}}}).encode()
    for a in range(6):
        try:
            req = urllib.request.Request(URL, data=body, headers={
                "Content-Type": "application/json", "x-goog-api-key": API_KEY})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r)
            for p in data["candidates"][0]["content"]["parts"]:
                inline = p.get("inlineData") or p.get("inline_data")
                if inline and inline.get("data"):
                    return base64.b64decode(inline["data"])
        except Exception as e:
            print("  retry", a, e)
        time.sleep(2 ** a * 2)
    raise SystemExit("gen failed")

def emit_webp(png, base, widths, q=82):
    im = Image.open(png).convert("RGB"); w, h = im.size
    im.save(os.path.join(IMG, base + ".webp"), "WEBP", quality=q, method=6)
    for tw in widths:
        if tw < w:
            im.resize((tw, round(h*tw/w)), Image.LANCZOS).save(
                os.path.join(IMG, f"{base}-{tw}.webp"), "WEBP", quality=q, method=6)

def main():
    force = "--force" in sys.argv
    os.makedirs(SCRATCH, exist_ok=True)
    ref = None
    for name, (prompt, aspect, _) in JOBS.items():
        png = os.path.join(SCRATCH, name + ".png")
        if force or not os.path.exists(png):
            print("generating", name)
            open(png, "wb").write(call(prompt, aspect, ref=ref))
        ref = ref or png  # use first (desktop) hero as style anchor for the portrait
        widths = [960, 480] if "portrait" not in name else [640, 360]
        emit_webp(png, name, widths)
    # OG image 1200x630 cropped from the desktop hero
    src = Image.open(os.path.join(SCRATCH, "hero-brand.png")).convert("RGB")
    tw, th = 1200, 630
    scale = max(tw/src.width, th/src.height)
    rs = src.resize((round(src.width*scale), round(src.height*scale)), Image.LANCZOS)
    left = (rs.width-tw)//2; top = (rs.height-th)//2
    os.makedirs(os.path.join(IMG, "..", "og"), exist_ok=True)
    rs.crop((left, top, left+tw, top+th)).save(os.path.join(IMG, "..", "og", "home.jpg"),
                                               "JPEG", quality=84, optimize=True)
    print("done -> hero-brand[-portrait].webp + og/home.jpg")

if __name__ == "__main__":
    main()
