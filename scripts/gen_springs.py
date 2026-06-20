#!/usr/bin/env python3
"""Regenerate the 3 garage-door torsion spring product images, conditioned on a
real reference photo so they look like genuine garage door springs."""
import base64, io, json, os, time, urllib.request
from PIL import Image

KEY=os.environ["GEMINI_API_KEY"]
EP=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={KEY}"
OUT=os.path.join(os.path.dirname(__file__),"..","assets","img")
REF=open("/tmp/spring_ref.jpg","rb").read()
REF_B64=base64.b64encode(REF).decode()

STYLE=(" Match the EXACT style of the reference photo: a long cylindrical garage door TORSION spring made of "
       "tightly-wound CLOSED black steel coils packed closely together (coils touching, forming a dense ribbed "
       "black tube), with a cast-metal winding cone fitting and set screws at the end. Professional studio product "
       "photograph, centered, horizontal, on a clean smooth light-grey seamless studio gradient background, soft "
       "shadow, sharp focus, photorealistic. No text, no watermark, no logo, no packaging, no hands, no camera icons.")

PROMPTS={
 "spring-standard": "Create a product photo of a SINGLE garage door torsion spring with a bare zinc-grey cast winding cone."+STYLE,
 "spring-highcycle": "Create a product photo of a SINGLE premium garage door torsion spring with a bright RED cast winding cone at the end."+STYLE,
 "spring-premium": "Create a product photo of a PAIR of two matching garage door torsion springs side by side, one with a RED cast winding cone and one with a grey cone, like the reference."+STYLE,
}

def gen(name,prompt):
    body=json.dumps({"contents":[{"parts":[{"text":prompt},{"inline_data":{"mime_type":"image/jpeg","data":REF_B64}}]}],
                     "generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"1:1"}}}).encode()
    for attempt in range(4):
        try:
            req=urllib.request.Request(EP,data=body,headers={"Content-Type":"application/json"})
            d=json.load(urllib.request.urlopen(req,timeout=120))
            for p in d["candidates"][0]["content"]["parts"]:
                inl=p.get("inlineData") or p.get("inline_data")
                if inl and inl.get("data"):
                    img=Image.open(io.BytesIO(base64.b64decode(inl["data"]))).convert("RGB")
                    if img.width>900:
                        img=img.resize((900,round(img.height*900/img.width)),Image.LANCZOS)
                    out=os.path.join(OUT,name+".jpg")
                    img.save(out,"JPEG",quality=84,optimize=True,progressive=True)
                    print("OK",name,os.path.getsize(out)//1024,"KB"); return True
            print("WARN",name,"no image"); 
        except Exception as e:
            print("ERR",name,e); time.sleep(2**attempt*2)
    return False

for n,p in PROMPTS.items():
    gen(n,p); time.sleep(1)
