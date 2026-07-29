#!/usr/bin/env python3
"""Downsize assets/img/icon-512.png (from gen_favicons.mjs) to the full favicon
set: icon-192, favicon-96, favicon-48, favicon-32 + a multi-size favicon.ico at
the web root (SERP favicon needs >=48px).
  node scripts/gen_favicons.mjs && python3 scripts/gen_favicons.py
"""
import os
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..")
IMG = os.path.join(ROOT, "assets", "img")
src = Image.open(os.path.join(IMG, "icon-512.png")).convert("RGBA")

for size, name in [(192, "icon-192.png"), (96, "favicon-96.png"),
                   (48, "favicon-48.png"), (32, "favicon-32.png")]:
    src.resize((size, size), Image.LANCZOS).save(os.path.join(IMG, name))
    print("wrote assets/img/" + name)

src.resize((48, 48), Image.LANCZOS).save(
    os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
print("wrote favicon.ico (16/32/48)")
