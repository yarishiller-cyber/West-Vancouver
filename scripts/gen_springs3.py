#!/usr/bin/env python3
"""Regenerate realistic GARAGE-DOOR TORSION SPRING images with nano banana.

Educated on real reference photos: garage-door torsion springs are LONG
cylindrical tubes of TIGHTLY-WOUND CLOSED black oil-tempered steel coils
(adjacent coils touch — NO gaps), with cast-iron winding cones and set
screws, color-coded by wire size. They are NOT automotive suspension coils.

Generates a consistent set, then writes uniquely-named, descriptive files.
Run:  GEMINI_API_KEY=... python3 scripts/gen_springs3.py
"""
import base64, io, json, os, time, urllib.request
from PIL import Image

KEY = os.environ["GEMINI_API_KEY"]
EP = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={KEY}"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")

# The non-negotiable reality of a garage-door torsion spring, fed to every prompt.
REALITY = (
    " IMPORTANT — this is a GARAGE-DOOR TORSION SPRING, not an automotive or suspension spring. "
    "It is a long cylindrical tube made of TIGHTLY-WOUND, CLOSED helical coils of thick black "
    "oil-tempered square steel wire, where adjacent coils TOUCH each other with NO gaps between "
    "them (a solid-looking dense black coil cylinder, roughly 50 cm long and 5 cm in diameter). "
    "Each end has a heavy CAST-IRON winding cone with two visible set screws and four winding-bar "
    "holes, and the spring slides onto a round steel torsion shaft through its center. "
    "Do NOT make an open, widely-spaced suspension coil. Coils must be packed solid and touching. "
    "Photorealistic professional product photography, sharp mechanical detail, clean smooth light-grey "
    "seamless studio background, soft realistic shadow, no text, no watermark, no logo, no hands."
)

def call(parts, aspect):
    body = json.dumps({
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}},
    }).encode()
    for a in range(4):
        try:
            req = urllib.request.Request(EP, data=body, headers={"Content-Type": "application/json"})
            d = json.load(urllib.request.urlopen(req, timeout=180))
            for p in d["candidates"][0]["content"]["parts"]:
                inl = p.get("inlineData") or p.get("inline_data")
                if inl and inl.get("data"):
                    return base64.b64decode(inl["data"])
        except Exception as e:
            print("  err:", e); time.sleep(2 ** a * 2)
    return None

def save(raw, name, w):
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    path = os.path.join(OUT, name + ".jpg")
    im.save(path, "JPEG", quality=86, optimize=True, progressive=True)
    print("  saved", name, os.path.getsize(path) // 1024, "KB")
    return raw

def gen(name, prompt, aspect="1:1", w=900, cond=None):
    print("gen", name)
    parts = [{"text": prompt + REALITY}]
    if cond:
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(cond).decode()}})
    raw = call(parts, aspect)
    if raw:
        return save(raw, name, w)
    print("  FAILED", name)
    return None

# 1) Single spring — generate first; reuse as a style anchor for the others.
anchor = gen(
    "garage-door-torsion-spring-single",
    "A single garage-door torsion spring lying horizontally, centered, with a bright RED cast-iron "
    "winding cone at one end and a black stationary cone at the other. The long black tightly-wound "
    "closed coil fills the frame. Studio product shot.",
)

# 2) A matched PAIR of two springs (the two-spring repair option).
gen(
    "garage-door-torsion-springs-pair",
    "Two matching garage-door torsion springs lying side by side horizontally, a left-wind and a "
    "right-wind spring as a matched pair. One has a RED cast winding cone, the other a BLACK cone. "
    "Both are long, dense, tightly-wound closed black coils. Studio product shot.",
    cond=anchor,
)

# 3) Premium extra-long-life springs — coils powder-coated bright RED.
gen(
    "garage-door-torsion-springs-premium-red-coated",
    "Two PREMIUM heavy-duty extra-long-life garage-door torsion springs side by side. The tightly-wound "
    "closed coils themselves are POWDER-COATED bright glossy RED along the full length (red-coated steel "
    "coil, not a stripe), with black cast-iron winding cones and set screws. The red coating clearly marks "
    "them as the premium upgrade. Studio product shot.",
    cond=anchor,
)

# 4) HERO — real springs mounted on the torsion shaft above a residential garage door.
hero = gen(
    "garage-door-torsion-springs-hero",
    "Cinematic close-up of two real black garage-door torsion springs mounted on a horizontal round steel "
    "torsion shaft on the header wall ABOVE a residential garage door, red winding cones at the center, "
    "cables and drums visible at the ends, warm soft daylight from a garage window, shallow depth of field. "
    "Keep the left third darker and calmer for text. The coils are tightly-wound and closed (touching).",
    aspect="16:9", w=1600,
)

# 4b) Vertical hero for mobile, recomposed from the desktop hero for consistency.
if hero:
    gen(
        "garage-door-torsion-springs-hero-mobile",
        "Recompose this exact scene into a TALL VERTICAL 9:16 portrait crop for a mobile banner: the same two "
        "mounted black torsion springs on the steel shaft above the garage door, same lighting and mood, "
        "well composed for portrait, subject in the upper-middle, calmer area low for text.",
        aspect="9:16", w=820, cond=hero,
    )

# 5) Mounted detail for the home 'Springs' category tile.
gen(
    "garage-door-torsion-spring-mounted-closeup",
    "Tight close-up of one black garage-door torsion spring with a red winding cone mounted on its steel "
    "shaft, a technician's winding bar inserted in a cone hole, crisp detail, soft workshop light. The coil "
    "is dense, tightly-wound and closed.",
    aspect="4:3", w=900,
)

print("SPRINGS DONE")
