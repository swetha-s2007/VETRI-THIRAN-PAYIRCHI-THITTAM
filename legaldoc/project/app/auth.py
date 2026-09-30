import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime,timedelta,timezone
import jwt
from passlib.context import CryptContext
from fastapi import Depends,HTTPException,Request,status
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
SECRET_KEY=os.getenv('SECRET_KEY','dev-only-change-me')
pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
def hash_password(password): return pwd_context.hash(password)
def verify_password(password,password_hash): return pwd_context.verify(password,password_hash)
def create_token(user_id,expires_minutes=1440):
    return jwt.encode({'sub':str(user_id),'exp':datetime.now(timezone.utc)+timedelta(minutes=expires_minutes)},SECRET_KEY,algorithm='HS256')
def get_current_user(request:Request,db:Session=Depends(get_db)):
    token=request.cookies.get('access_token')
    if not token:
        auth=request.headers.get('Authorization','')
        if auth.startswith('Bearer '): token=auth[7:]
    if not token: raise HTTPException(status_code=401,detail='Login required')
    try: user_id=int(jwt.decode(token,SECRET_KEY,algorithms=['HS256'])['sub'])
    except Exception: raise HTTPException(status_code=401,detail='Invalid or expired token')
    user=db.get(User,user_id)
    if not user: raise HTTPException(status_code=401,detail='User not found')
    return user
