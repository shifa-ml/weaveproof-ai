import hashlib, os, time
from typing import Optional
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
load_dotenv()
app=FastAPI(title="QR-to-Weave API",version="1.0.0")
origins=[x.strip() for x in os.getenv("CORS_ORIGINS","http://localhost:5173,http://127.0.0.1:5173").split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=False,allow_methods=["GET","POST","OPTIONS"],allow_headers=["Content-Type","Authorization"])
TTL=int(os.getenv("STORY_CACHE_TTL_SECONDS","86400")); TIMEOUT=float(os.getenv("STORY_TIMEOUT_SECONDS","7"))
cache={}; recent=[]
class Product(BaseModel):
 id:str=Field(max_length=80); name:str=Field(max_length=200); artisan:str=Field(max_length=200); location:str=Field(max_length=200); technique:str=Field(max_length=200); materials:str=Field(max_length=200); motif:str=""; status:str="incomplete"
class StoryRequest(BaseModel):
 product:Product; language:str=Field(default="en",pattern="^(en|as|hi)$"); fallback_story:str=Field(default="",max_length=5000)
class StoryResponse(BaseModel):
 story:str; cached:bool=False; source:str="fallback"
def fallback(req):
 if req.fallback_story.strip(): return req.fallback_story.strip()
 p=req.product; lang=req.language
 if lang=="as": return f"{p.name} সামগ্ৰীখন {p.materials} আৰু {p.technique} কৌশলৰ সৈতে উল্লেখ কৰা হৈছে। দিয়া উৎপত্তিস্থল হৈছে {p.location}। এই তথ্যসমূহ স্বতন্ত্ৰভাৱে পৰীক্ষা কৰা হোৱা নাই। প্ৰমাণিত সামগ্ৰী হিচাপে উপস্থাপন কৰাৰ আগতে শিল্পীৰ সৈতে তথ্য নিশ্চিত কৰক।"
 if lang=="hi": return f"{p.name} को {p.materials} से बना और {p.technique} तकनीक से तैयार बताया गया है। इसका बताया गया मूल स्थान {p.location} है। इन विवरणों का स्वतंत्र सत्यापन नहीं हुआ है। इसे प्रमाणित उत्पाद बताने से पहले कारीगर से जानकारी की पुष्टि करें।"
 return f"{p.name} is listed as a {p.materials} textile using {p.technique}, with the stated origin {p.location}. These details have not been independently verified by this story service. Confirm the information with the artisan before presenting it as an authenticated product."
def key(req):
 raw=req.product.model_dump_json()+req.language
 return hashlib.sha256(raw.encode()).hexdigest()
async def gemma(req)->Optional[str]:
 api=os.getenv("GOOGLE_API_KEY","").strip()
 if not api:return None
 model=os.getenv("GEMMA_MODEL","gemma-3-27b-it")
 p=req.product; language={"en":"English","as":"Assamese","hi":"Hindi"}[req.language]
 prompt=f"""Write a respectful 100-140 word handloom craft story in {language}. Use only the supplied facts. Do not invent awards, certifications, family history, dates, GI status, sustainability claims or personal details. If record status is not verified, say details have not been independently verified. Even if status is verified, do not claim this AI response proves physical textile authenticity.
Product: {p.name}; ID: {p.id}; artisan field: {p.artisan}; stated origin: {p.location}; material: {p.materials}; technique: {p.technique}; motif note: {p.motif}; record status: {p.status}. Return only story text."""
 url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
 async with httpx.AsyncClient(timeout=TIMEOUT) as client:
  r=await client.post(url,params={"key":api},json={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0.55,"maxOutputTokens":260}})
  if r.status_code==429:return None
  r.raise_for_status(); data=r.json()
 candidates=data.get("candidates") or []
 parts=(candidates[0].get("content") or {}).get("parts") or [] if candidates else []
 result="\n".join(x.get("text","") for x in parts).strip()
 return result[:5000] if result else None
@app.get("/api/health")
async def health():return {"ok":True,"provider_configured":bool(os.getenv("GOOGLE_API_KEY",""))}
@app.post("/api/story",response_model=StoryResponse)
async def story(req:StoryRequest):
 k=key(req); now=time.time()
 if k in cache and now-cache[k][0]<TTL:return StoryResponse(story=cache[k][1],cached=True,source="cache")
 global recent
 recent=[x for x in recent if now-x<60]
 if len(recent)>=8:return StoryResponse(story=fallback(req),source="fallback")
 recent.append(now)
 try:
  generated=await gemma(req)
  if generated:cache[k]=(time.time(),generated);return StoryResponse(story=generated,source="gemma")
 except Exception:
  pass
 return StoryResponse(story=fallback(req),source="fallback")
