#!/usr/bin/env python3
"""Generate before/after garage door pairs. 'After' is image-conditioned on the
'before' so the house/composition stays identical — only the door changes."""
import base64,io,json,os,time,urllib.request
from PIL import Image
KEY=os.environ["GEMINI_API_KEY"]
EP=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={KEY}"
OUT=os.path.join(os.path.dirname(__file__),"..","assets","img")
STYLE=" Ultra-realistic professional real-estate photograph, sharp focus, natural daylight, eye-level straight-on view of the garage. 16:9."

def call(parts,aspect="16:9"):
    body=json.dumps({"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":aspect}}}).encode()
    for a in range(4):
        try:
            r=urllib.request.Request(EP,data=body,headers={"Content-Type":"application/json"})
            d=json.load(urllib.request.urlopen(r,timeout=120))
            for p in d["candidates"][0]["content"]["parts"]:
                inl=p.get("inlineData") or p.get("inline_data")
                if inl and inl.get("data"): return base64.b64decode(inl["data"])
            print("no image"); 
        except Exception as e: print("err",e); time.sleep(2**a*2)
    return None

def save(raw,name,w=1600):
    im=Image.open(io.BytesIO(raw)).convert("RGB")
    if im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    p=os.path.join(OUT,name+".jpg"); im.save(p,"JPEG",quality=84,optimize=True,progressive=True)
    print("saved",name,os.path.getsize(p)//1024,"KB"); return raw

pairs=[
 ("ba1","A single-family West Coast home with a TIRED OLD garage door: a faded, dated, slightly dented beige/cream steel raised-panel garage door that looks worn and aged, on an older home with a concrete driveway."+STYLE,
       "Keep this exact same house, driveway, lighting and camera angle, but REPLACE ONLY the old garage door with a brand-new sleek modern dark charcoal aluminum garage door with frosted glass accent panels. Everything else stays identical."),
]
for key,bp,ap in pairs:
    print("before...",key)
    raw=call([{"text":bp}])
    if not raw: continue
    save(raw,key+"-before")
    print("after...",key)
    b64=base64.b64encode(raw).decode()
    raw2=call([{"text":ap},{"inline_data":{"mime_type":"image/jpeg","data":b64}}])
    if raw2: save(raw2,key+"-after")
    time.sleep(1)
