#!/usr/bin/env python3
import base64,io,json,os,time,urllib.request
from PIL import Image
KEY=os.environ["GEMINI_API_KEY"]
EP=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={KEY}"
OUT="assets/img"
REF=base64.b64encode(open("/tmp/spring_ref.jpg","rb").read()).decode()
STYLE=(" Match the EXACT realistic style of the reference photo of garage-door torsion springs: long cylindrical "
       "tubes of tightly-wound CLOSED black steel coils packed together (coils touching), with cast-metal winding "
       "cones and set screws. Professional studio product photo, horizontal, centered, on a clean smooth light-grey "
       "seamless studio gradient, soft shadow, photorealistic. No text, no watermark, no logo, no hands.")
def call(parts,aspect,w):
    body=json.dumps({"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":aspect}}}).encode()
    for a in range(4):
        try:
            r=urllib.request.Request(EP,data=body,headers={"Content-Type":"application/json"})
            d=json.load(urllib.request.urlopen(r,timeout=120))
            for p in d["candidates"][0]["content"]["parts"]:
                inl=p.get("inlineData") or p.get("inline_data")
                if inl and inl.get("data"):
                    return base64.b64decode(inl["data"])
        except Exception as e: print("err",e);time.sleep(2**a*2)
    return None
def save(raw,name,w):
    im=Image.open(io.BytesIO(raw)).convert("RGB")
    if im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    p=os.path.join(OUT,name+".jpg");im.save(p,"JPEG",quality=86,optimize=True,progressive=True)
    print("saved",name,os.path.getsize(p)//1024,"KB")
def ref_gen(name,prompt,aspect="1:1",w=900):
    raw=call([{"text":prompt+STYLE},{"inline_data":{"mime_type":"image/jpeg","data":REF}}],aspect,w)
    if raw: save(raw,name,w)
# product images
ref_gen("spring-single","Create a product photo of a SINGLE garage-door torsion spring with a bright RED cast winding cone at the end.")
ref_gen("spring-double","Create a product photo of a PAIR of two matching garage-door torsion springs side by side, one with a red cast winding cone and one with a black cone.")
ref_gen("spring-premium","Create a product photo of a PAIR of two PREMIUM heavy-duty garage-door torsion springs, each black coil WRAPPED in a bright RED protective sleeve/coating running along the length of the spring, with cast winding cones. The red sleeves clearly distinguish them as premium.")
# hero (real springs mounted) 16:9 + mobile 3:4
hp=("Create a cinematic close-up of two real black garage-door torsion springs mounted on a steel torsion shaft above a "
    "residential garage door, with red winding cones, crisp mechanical detail, soft daylight. Leave the left third darker "
    "and calmer for text overlay. Photorealistic, no text.")
raw=call([{"text":hp},{"inline_data":{"mime_type":"image/jpeg","data":REF}}],"16:9",1600)
if raw:
    save(raw,"springs-hero",1600)
    b64=base64.b64encode(raw).decode()
    mp=("Recompose this exact scene into a TALL VERTICAL 3:4 portrait crop for a mobile banner, same springs, shaft and "
        "mood, well composed for portrait. Photorealistic, no text.")
    raw2=call([{"text":mp},{"inline_data":{"mime_type":"image/jpeg","data":b64}}],"3:4",800)
    if raw2: save(raw2,"springs-hero-mobile",800)
print("SPRINGS DONE")
