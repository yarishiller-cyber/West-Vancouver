#!/usr/bin/env python3
"""Generate the scroll "explode" frame sequence for the hero animation.

Technique: start from an assembled garage-door-system render, then chain
image-to-image edits (Gemini 2.5 Flash Image / "nano banana"), each step
nudging every component a little further apart along the same isometric axis.
Small incremental edits preserve subject/colour/camera consistency while the
cumulative separation becomes dramatic — a sequence we can scrub on scroll.

Output: assets/anim/door-00.webp ... door-NN.webp (+ raw PNGs in scratch/).
Run once; commit the webp frames. Re-run with --force to regenerate.

  GEMINI_API_KEY=... python3 scripts/gen_explode_frames.py [--frames 8] [--force]
"""
import base64, json, os, sys, time, urllib.request, urllib.error
from PIL import Image

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
MODEL = "gemini-2.5-flash-image"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
ROOT = os.path.join(os.path.dirname(__file__), "..")
SCRATCH = os.path.join(ROOT, "scratch")
ANIM = os.path.join(ROOT, "assets", "anim")

ASSEMBLED = (
    "Clean modern 3D technical illustration of a complete residential sectional garage "
    "door SYSTEM, three-quarter isometric view, fully ASSEMBLED. Show door panels, a "
    "horizontal torsion spring on a steel shaft at the top, cable drums, vertical and "
    "horizontal tracks, rollers, hinges, bottom bracket, and a ceiling-mounted belt-drive "
    "opener with rail. Studio product render, soft realistic lighting, subtle shadows, deep "
    "navy and warm gold accent color scheme on a pure flat white background. No text, no "
    "labels, no people. Centered, generous margins. Square composition."
)
STEP = (
    "Take this exact garage door system illustration and move every component a little "
    "further apart along the same diagonal isometric axis: add a bit more separation between "
    "the door panels, the torsion spring and shaft, the tracks, the rollers, the hinges, the "
    "cable drums, the bottom brackets and the ceiling opener, as if it is gently "
    "disassembling in mid-air. Keep the EXACT same camera angle, identical part shapes and "
    "navy + gold colours, identical soft studio lighting, identical pure flat white "
    "background, identical overall scale and centered composition. Only the spacing increases "
    "slightly. No text, no labels, no people."
)

def call(prompt, ref_png=None):
    parts = [{"text": prompt}]
    if ref_png:
        b64 = base64.b64encode(open(ref_png, "rb").read()).decode()
        parts.append({"inlineData": {"mimeType": "image/png", "data": b64}})
    body = json.dumps({"contents": [{"parts": parts}],
                       "generationConfig": {"responseModalities": ["IMAGE"],
                                            "imageConfig": {"aspectRatio": "1:1"}}}).encode()
    for attempt in range(6):
        try:
            req = urllib.request.Request(URL, data=body, headers={
                "Content-Type": "application/json", "x-goog-api-key": API_KEY})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r)
            for p in data["candidates"][0]["content"]["parts"]:
                inline = p.get("inlineData") or p.get("inline_data")
                if inline and inline.get("data"):
                    return base64.b64decode(inline["data"])
            print("   no image:", json.dumps(data)[:200])
        except Exception as e:
            print(f"   retry {attempt}: {e}")
        time.sleep(2 ** attempt * 2)
    raise SystemExit("generation failed")

def save_webp(png_path, webp_path, size=720):
    im = Image.open(png_path).convert("RGB")
    if im.width > size:
        im = im.resize((size, round(im.height * size / im.width)), Image.LANCZOS)
    im.save(webp_path, "WEBP", quality=80, method=6)

def main():
    if not API_KEY:
        raise SystemExit("set GEMINI_API_KEY")
    frames = 8
    if "--frames" in sys.argv:
        frames = int(sys.argv[sys.argv.index("--frames") + 1])
    force = "--force" in sys.argv
    os.makedirs(SCRATCH, exist_ok=True)
    os.makedirs(ANIM, exist_ok=True)

    base = os.path.join(SCRATCH, "door-00.png")
    if force or not os.path.exists(base):
        print("frame 00 (assembled)")
        open(base, "wb").write(call(ASSEMBLED))
    save_webp(base, os.path.join(ANIM, "door-00.webp"))

    prev = base
    for i in range(1, frames + 1):
        png = os.path.join(SCRATCH, f"door-{i:02d}.png")
        if force or not os.path.exists(png):
            print(f"frame {i:02d} (explode step)")
            open(png, "wb").write(call(STEP, ref_png=prev))
        save_webp(png, os.path.join(ANIM, f"door-{i:02d}.webp"))
        prev = png
    print(f"done: {frames+1} frames -> assets/anim/")

if __name__ == "__main__":
    main()
