#!/usr/bin/env python3
"""Generate vertical (mobile) hero images, conditioned on the existing desktop
hero so the two formats match. Output: <name>-mobile.jpg (9:16)."""
import base64,io,json,os,time,urllib.request
from PIL import Image
KEY=os.environ["GEMINI_API_KEY"]
EP=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={KEY}"
OUT=os.path.join(os.path.dirname(__file__),"..","assets","img")

def gen(ref_name,out_name,prompt,aspect="9:16",w=900):
    ref=open(os.path.join(OUT,ref_name),"rb").read()
    parts=[{"text":prompt},{"inline_data":{"mime_type":"image/jpeg","data":base64.b64encode(ref).decode()}}]
    body=json.dumps({"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":aspect}}}).encode()
    for a in range(4):
        try:
            r=urllib.request.Request(EP,data=body,headers={"Content-Type":"application/json"})
            d=json.load(urllib.request.urlopen(r,timeout=120))
            for p in d["candidates"][0]["content"]["parts"]:
                inl=p.get("inlineData") or p.get("inline_data")
                if inl and inl.get("data"):
                    im=Image.open(io.BytesIO(base64.b64decode(inl["data"]))).convert("RGB")
                    if im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
                    pth=os.path.join(OUT,out_name); im.save(pth,"JPEG",quality=84,optimize=True,progressive=True)
                    print("OK",out_name,im.size,os.path.getsize(pth)//1024,"KB");return True
            print("no image")
        except Exception as e: print("err",e);time.sleep(2**a*2)
    return False

gen("hero-home.jpg","hero-mobile.jpg",
    "Recompose this exact same luxury West Vancouver home and its modern garage door into a TALL VERTICAL 9:16 PORTRAIT photograph designed as a mobile phone hero background. Keep the same house, the same dark modern garage door, the same golden-hour lighting, ocean and North Shore mountains. Compose vertically: the beautiful garage door prominent in the lower two-thirds, with the home's roofline, tall evergreens, sky and mountains filling the upper third. Cinematic, photorealistic, crisp. 9:16.")
