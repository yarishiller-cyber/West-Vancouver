#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OPTIONAL higher-fidelity route: render the garage-door "explode" as a real
interpolated clip with Google **Veo 3.1 first-last-frame**, then convert it into
the same scrubable WebP frame sequence the hero canvas already uses.

Pipeline:
  1. keyframes  — uses scratch/door-00.png (assembled) as FIRST frame and
                  scratch/door-08.png (exploded) as LAST frame. (Swap in
                  photoreal Nano Banana frames for a photographic version.)
  2. Veo 3.1    — POST :predictLongRunning with image + lastFrame, poll, download MP4.
  3. ffmpeg     — extract ~33 frames -> assets/anim/door-NN.webp (drop-in for the scrubber).

Notes:
  * Veo is a paid model (~$0.15-0.40/sec) and must be enabled on the key/project.
    If it isn't, this exits cleanly and the illustration sequence (gen_explode_frames.py)
    remains the shipped hero — no harm done.
  * Model id + param names move fast; override with VEO_MODEL if needed and check
    https://ai.google.dev/gemini-api/docs/video .

  GEMINI_API_KEY=... python3 scripts/gen_veo_explode.py
"""
import base64, json, os, sys, time, urllib.request, urllib.error
from PIL import Image
import imageio_ffmpeg

KEY = os.environ.get("GEMINI_API_KEY", "").strip()
ROOT = os.path.join(os.path.dirname(__file__), "..")
SCRATCH = os.path.join(ROOT, "scratch")
ANIM = os.path.join(ROOT, "assets", "anim")
FIRST = os.path.join(SCRATCH, "door-00.png")
LAST  = os.path.join(SCRATCH, "door-08.png")
API = "https://generativelanguage.googleapis.com/v1beta"
# candidate model ids (first that exists wins)
MODELS = [os.environ.get("VEO_MODEL", ""), "veo-3.1-generate-preview",
          "veo-3.1-fast-generate-preview", "veo-3.0-generate-001"]
PROMPT = ("A residential garage door system smoothly disassembling into an exploded "
          "technical view: panels, torsion spring, tracks, rollers and the ceiling "
          "opener gently separating apart, fixed camera, clean white background, "
          "navy and gold colour scheme.")

def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()

def b64_169(path):
    """Pad a square keyframe onto a 16:9 white canvas (Veo requires 16:9 or 9:16)."""
    import io
    im = Image.open(path).convert("RGB")
    W = max(im.width, int(im.height * 16 / 9)); H = int(W * 9 / 16)
    canvas = Image.new("RGB", (W, H), "white")
    canvas.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
    buf = io.BytesIO(); canvas.save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()

def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
    return json.load(urllib.request.urlopen(req, timeout=120))

def get(url):
    req = urllib.request.Request(url, headers={"x-goog-api-key": KEY})
    return json.load(urllib.request.urlopen(req, timeout=120))

def start(model):
    body = {"instances": [{"prompt": PROMPT,
              "image": {"bytesBase64Encoded": b64_169(FIRST), "mimeType": "image/png"},
              "lastFrame": {"bytesBase64Encoded": b64_169(LAST), "mimeType": "image/png"}}],
            "parameters": {"aspectRatio": "16:9", "durationSeconds": 6}}
    return post(f"{API}/models/{model}:predictLongRunning", body)

def main():
    if not KEY:
        sys.exit("set GEMINI_API_KEY")
    if not (os.path.exists(FIRST) and os.path.exists(LAST)):
        sys.exit("need scratch/door-00.png and door-08.png (run gen_explode_frames.py first)")

    op = None
    for m in [x for x in MODELS if x]:
        try:
            print("trying model:", m)
            op = start(m); print("  started:", op.get("name")); break
        except urllib.error.HTTPError as e:
            print(f"  {m}: HTTP {e.code} {e.read().decode()[:160]}")
        except Exception as e:
            print(f"  {m}: {e}")
    if not op or "name" not in op:
        sys.exit("Veo not available on this key — keeping the illustration sequence. (No charge.)")

    name = op["name"]
    for _ in range(60):
        time.sleep(10)
        st = get(f"{API}/{name}")
        if st.get("done"):
            print("  done."); break
        print("  …rendering")
    else:
        sys.exit("timed out waiting for Veo")

    # locate the returned video (uri or inline bytes — shape varies by version)
    resp = json.dumps(st)
    mp4 = os.path.join(SCRATCH, "explode-veo.mp4")
    vids = st.get("response", {}).get("generatedVideos") or st.get("response", {}).get("videos") or []
    wrote = False
    for v in vids:
        uri = (v.get("video") or {}).get("uri") or v.get("uri")
        data = (v.get("video") or {}).get("bytesBase64Encoded") or v.get("bytesBase64Encoded")
        if uri:
            req = urllib.request.Request(uri, headers={"x-goog-api-key": KEY})
            open(mp4, "wb").write(urllib.request.urlopen(req, timeout=300).read()); wrote = True; break
        if data:
            open(mp4, "wb").write(base64.b64decode(data)); wrote = True; break
    if not wrote:
        sys.exit("couldn't find video in response: " + resp[:300])
    print("  saved", mp4)

    # extract -> webp frames (drop-in for the scrubber)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    os.makedirs(os.path.join(SCRATCH, "veo"), exist_ok=True)
    os.system(f'"{ff}" -y -i "{mp4}" -vf "fps=24,scale=1280:720" "{os.path.join(SCRATCH,"veo","v_%03d.png")}" 2>/dev/null')
    import glob
    fs = sorted(glob.glob(os.path.join(SCRATCH, "veo", "v_*.png")))
    for old in glob.glob(os.path.join(ANIM, "door-*.webp")): os.remove(old)
    for i, f in enumerate(fs):
        Image.open(f).convert("RGB").save(os.path.join(ANIM, f"door-{i:02d}.webp"), "WEBP", quality=80, method=6)
    print(f"  wrote {len(fs)} webp frames -> assets/anim/  (set data-frames=\"{len(fs)}\" in index.html)")

if __name__ == "__main__":
    main()
