import json
from fastapi import APIRouter,Depends,HTTPException,UploadFile,File,Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..database import get_db
from ..models import User,RecommendationHistory
from ..schemas import RegisterRequest,LoginRequest,HomeRequest,PartyRequest
from ..auth import hash_password,verify_password,create_token,get_current_user
from ..services.gemini_service import generate_home,generate_party,generate_jewelry
router=APIRouter(prefix='/api')
@router.get('/health')
def health(): return {'status':'ok','service':'PocketSmart AI'}
@router.post('/register')
def register(d:RegisterRequest,db:Session=Depends(get_db)):
    e=d.email.lower()
    if db.query(User).filter(User.email==e).first(): raise HTTPException(400,'Email is already registered')
    u=User(name=d.name.strip(),email=e,password_hash=hash_password(d.password)); db.add(u); db.commit(); db.refresh(u); return {'message':'Registration successful','user_id':u.id}
@router.post('/login')
def login(d:LoginRequest,db:Session=Depends(get_db)):
    u=db.query(User).filter(User.email==d.email.lower()).first()
    if not u or not verify_password(d.password,u.password_hash): raise HTTPException(401,'Invalid email or password')
    r=JSONResponse({'message':'Login successful','user':{'id':u.id,'name':u.name,'email':u.email}}); r.set_cookie('access_token',create_token(u.id),httponly=True,samesite='lax',max_age=86400); return r
@router.post('/logout')
def logout():
    r=JSONResponse({'message':'Logged out'}); r.delete_cookie('access_token'); return r
@router.get('/token')
def token(u=Depends(get_current_user)): return {'access_token':create_token(u.id),'token_type':'bearer'}
@router.get('/session-info')
def info(u=Depends(get_current_user)): return {'logged_in':True,'user_id':u.id,'name':u.name,'email':u.email}
@router.get('/session-data')
def data(u=Depends(get_current_user),db:Session=Depends(get_db)): return {'user_id':u.id,'recommendation_count':db.query(RecommendationHistory).filter_by(user_id=u.id).count()}
def save(db,u,p,b,req,res): db.add(RecommendationHistory(user_id=u.id,planner=p,budget=b,request_json=json.dumps(req),response_json=json.dumps(res))); db.commit()
@router.post('/generate-home')
def home(d:HomeRequest,u=Depends(get_current_user),db:Session=Depends(get_db)):
    r=generate_home(d.model_dump()); save(db,u,'home',d.budget,d.model_dump(),r); return r
@router.post('/generate-party')
def party(d:PartyRequest,u=Depends(get_current_user),db:Session=Depends(get_db)):
    r=generate_party(d.model_dump()); save(db,u,'party',d.budget,d.model_dump(),r); return r
@router.post('/generate-jewelry')
async def jewelry(budget:float=Form(...),occasion:str=Form(...),style:str=Form('Elegant'),outfit_description:str=Form(''),outfit_image:UploadFile|None=File(None),u=Depends(get_current_user),db:Session=Depends(get_db)):
    if budget<=0 or budget>10000000: raise HTTPException(422,'Invalid budget')
    img=None; mime=None
    if outfit_image and outfit_image.filename:
        if outfit_image.content_type not in {'image/jpeg','image/png','image/webp'}: raise HTTPException(400,'Only JPG, PNG or WEBP images are supported')
        img=await outfit_image.read()
        if len(img)>5*1024*1024: raise HTTPException(400,'Image must be 5 MB or smaller')
        mime=outfit_image.content_type
    d={'budget':budget,'occasion':occasion,'style':style,'outfit_description':outfit_description}; r=generate_jewelry(d,img,mime); save(db,u,'jewelry',budget,d,r); return r
@router.get('/history')
def history(u=Depends(get_current_user),db:Session=Depends(get_db)):
    rows=db.query(RecommendationHistory).filter_by(user_id=u.id).order_by(desc(RecommendationHistory.created_at)).limit(50).all()
    return [{'id':x.id,'planner':x.planner,'budget':x.budget,'request':json.loads(x.request_json),'response':json.loads(x.response_json),'created_at':x.created_at.isoformat()} for x in rows]
@router.get('/recommendations-details/{history_id}')
def details(history_id:int,u=Depends(get_current_user),db:Session=Depends(get_db)):
    x=db.query(RecommendationHistory).filter_by(id=history_id,user_id=u.id).first()
    if not x: raise HTTPException(404,'Recommendation not found')
    return {'id':x.id,'planner':x.planner,'request':json.loads(x.request_json),'response':json.loads(x.response_json),'created_at':x.created_at.isoformat()}
