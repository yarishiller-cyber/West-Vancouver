#!/usr/bin/env python3
"""Convert assets/img/*.jpg|png to responsive WebP (full, -960, -480).

No cwebp needed — uses Pillow. Keeps originals. Skips images that already
have an up-to-date .webp unless --force is passed.

Usage:
  python3 scripts/to_webp.py            # convert all jpg/png in assets/img
  python3 scripts/to_webp.py --force
"""
import os, sys, glob
from PIL import Image

IMG_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
WIDTHS = [480, 960]          # responsive variants; full size always emitted
Q = 82

def convert(path, force=False):
    base, _ = os.path.splitext(path)
    name = os.path.basename(base)
    im = Image.open(path).convert("RGB")
    w, h = im.size
    outputs = []
    # full
    full = base + ".webp"
    if force or not os.path.exists(full):
        im.save(full, "WEBP", quality=Q, method=6)
        outputs.append(full)
    # responsive (only downscale, never upscale)
    for tw in WIDTHS:
        if tw >= w:
            continue
        th = round(h * tw / w)
        variant = f"{base}-{tw}.webp"
        if force or not os.path.exists(variant):
            im.resize((tw, th), Image.LANCZOS).save(variant, "WEBP", quality=Q, method=6)
            outputs.append(variant)
    return outputs

def main():
    force = "--force" in sys.argv
    files = sorted(glob.glob(os.path.join(IMG_DIR, "*.jpg")) +
                   glob.glob(os.path.join(IMG_DIR, "*.png")))
    total = 0
    for f in files:
        outs = convert(f, force=force)
        for o in outs:
            kb = os.path.getsize(o) // 1024
            print(f"  {os.path.basename(o):<34} {kb} KB")
            total += 1
    print(f"\nDone: wrote {total} webp files")

if __name__ == "__main__":
    main()
