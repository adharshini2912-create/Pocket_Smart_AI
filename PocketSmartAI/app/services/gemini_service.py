import json
from .fallbacks import home_fallback,party_fallback,jewelry_fallback
from .marketplaces import search_url
from ..config import settings
try:
    from google import genai
    from google.genai import types
except Exception:
    genai=None; types=None
def _client(): return genai.Client(api_key=settings.gemini_api_key) if settings.gemini_api_key and genai else None
def _prompt(planner,data,image=False):
    return f'''You are PocketSmart AI, a budget planning assistant. Planner: {planner}. User data: {json.dumps(data,ensure_ascii=False)}. {"An outfit image is attached. Analyze visible colors/style only." if image else ""}\nReturn ONLY valid JSON with keys allocation, recommendations, tips. allocation is a list of category/amount_inr objects. recommendations is a list of category/title/estimated_price_inr/platform/search_query/reason objects. Use only Amazon, Flipkart, IKEA, Swiggy, Zomato or OYO as platform values. Stay within budget. Use INR. Give 4-8 practical recommendations. Never claim a price is live or verified. Do not invent URLs; provide search_query only. For images, do not identify the person.'''
def _normalize(o):
    if not isinstance(o,dict) or not all(isinstance(o.get(k),list) for k in ('allocation','recommendations','tips')): raise ValueError('Invalid AI schema')
    for r in o['recommendations']:
        r['search_url']=search_url(r.get('platform','Amazon'),str(r.get('search_query',''))); r.pop('search_query',None)
    return o
def generate(planner,data,image_bytes=None,mime=None):
    fallback={'home':home_fallback,'party':party_fallback,'jewelry':jewelry_fallback}[planner](type('Obj',(),data)()); client=_client()
    if not client: fallback['source']='fallback'; return fallback
    try:
        contents=[_prompt(planner,data,bool(image_bytes))]
        if image_bytes: contents.append(types.Part.from_bytes(data=image_bytes,mime_type=mime or 'image/jpeg'))
        r=client.models.generate_content(model=settings.gemini_model,contents=contents); raw=(r.text or '').strip()
        if raw.startswith('```'): raw=raw.split('```',2)[1]; raw=raw[4:] if raw.lstrip().startswith('json') else raw
        out=_normalize(json.loads(raw)); out['source']='gemini'; return out
    except Exception as e:
        fallback['source']='fallback'; fallback['ai_error']=type(e).__name__; return fallback
