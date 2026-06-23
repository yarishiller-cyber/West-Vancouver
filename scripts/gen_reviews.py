import base64,json,os,time,urllib.request
from PIL import Image
KEY=os.environ["GEMINI_API_KEY"]; MODEL="gemini-2.5-flash-image"
URL=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
IMG=os.path.join(os.path.dirname(__file__),"..","assets","img","reviews"); os.makedirs(IMG,exist_ok=True)
R=(" Candid amateur smartphone headshot of an ordinary real person (not a model), at home, "
   "natural window light, slight imperfect framing, true-to-life skin texture with visible pores, "
   "Kodak Portra 400 grain. Negative: no waxy skin, no CGI, no over-smoothing, no HDR glow, not a stock photo.")
PEOPLE={
 "rv-1":"a 40-year-old white Canadian woman with shoulder-length blond hair, warm friendly smile"+R,
 "rv-2":"a 55-year-old white Canadian man, short grey hair, glasses, professional, slight smile"+R,
 "rv-3":"a 45-year-old white Canadian woman, brown hair, casual, genuine smile"+R,
 "rv-4":"a 60-year-old white Canadian man, balding, weathered friendly face"+R,
 "rv-5":"a 38-year-old white Canadian woman, dark hair in a ponytail, cheerful"+R,
 "rv-6":"a 50-year-old East-Asian Canadian man, short black hair, kind smile"+R,
}
def call(p):
  body=json.dumps({"contents":[{"parts":[{"text":p}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"1:1"}}}).encode()
  for a in range(6):
    try:
      req=urllib.request.Request(URL,data=body,headers={"Content-Type":"application/json","x-goog-api-key":KEY})
      d=json.load(urllib.request.urlopen(req,timeout=120))
      for part in d["candidates"][0]["content"]["parts"]:
        inl=part.get("inlineData") or part.get("inline_data")
        if inl and inl.get("data"): return base64.b64decode(inl["data"])
    except Exception as e: print("retry",a,e)
    time.sleep(2**a*2)
  return None
for k,p in PEOPLE.items():
  png=call(p)
  if png:
    open(os.path.join(IMG,k+".png"),"wb").write(png)
    im=Image.open(os.path.join(IMG,k+".png")).convert("RGB").resize((256,256),Image.LANCZOS)
    im.save(os.path.join(IMG,k+".webp"),"WEBP",quality=82,method=6)
    print("ok",k)
  else: print("FAIL",k)
