import os,json,re
from dotenv import load_dotenv
load_dotenv()
from google import genai
from google.genai import types
from .fallback import fallback_home,fallback_party,fallback_jewelry
API_KEY=os.getenv('GEMINI_API_KEY','').strip(); MODEL=os.getenv('GEMINI_MODEL','gemini-2.5-flash')
def client(): return genai.Client(api_key=API_KEY) if API_KEY else None
def extract_json(text):
    text=text.strip(); text=re.sub(r'^```(?:json)?\s*','',text); text=re.sub(r'\s*```$','',text); a,b=text.find('{'),text.rfind('}')
    if a<0 or b<0: raise ValueError('Gemini did not return JSON')
    return json.loads(text[a:b+1])
def prompt(planner,data):
    return f'''You are PocketSmart AI, a budget planning assistant. Return ONLY valid JSON, no markdown. Planner: {planner}. User input: {json.dumps(data)}. Rules: never exceed budget; use estimated prices, not guaranteed live prices; platform URLs are search links; give 3-6 useful items; allocation total must be <= budget. JSON: {json.dumps({'planner':planner,'budget':0,'summary':'','allocation':{},'recommendations':[{'name':'','category':'','estimated_price':0,'platform':'Amazon','url':'','reason':''}],'tips':[],'ai_generated':True})}'''
def run(planner,data,fallback,image=None,mime=None):
    if not API_KEY:return fallback
    try:
        c=client(); contents=[prompt(planner,data)]
        if image:
            contents += [types.Part.from_bytes(data=image,mime_type=mime or 'image/jpeg'),'Use the image only for outfit color/style coordination; do not identify the person.']
        r=c.models.generate_content(model=MODEL,contents=contents,config=types.GenerateContentConfig(temperature=.2))
        out=extract_json(r.text); out['planner']=planner; out['budget']=data['budget']; out['ai_generated']=True; return out
    except Exception:return fallback
def generate_home(d): return run('home',d,fallback_home(**d))
def generate_party(d): return run('party',d,fallback_party(**d))
def generate_jewelry(d,image=None,mime=None): return run('jewelry',d,fallback_jewelry(**d),image,mime)
