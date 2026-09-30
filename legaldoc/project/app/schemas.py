from typing import List
from pydantic import BaseModel,Field,EmailStr
class RegisterRequest(BaseModel):
    name:str=Field(min_length=2,max_length=100)
    email:EmailStr
    password:str=Field(min_length=6,max_length=128)
class LoginRequest(BaseModel):
    email:EmailStr
    password:str
class HomeRequest(BaseModel):
    budget:float=Field(gt=0,le=10000000)
    room_type:str=Field(min_length=2,max_length=50)
    style:str=Field(default='Modern',max_length=50)
    items:List[str]=Field(default_factory=list)
class PartyRequest(BaseModel):
    budget:float=Field(gt=0,le=10000000)
    guests:int=Field(gt=0,le=10000)
    event_type:str=Field(min_length=2,max_length=80)
    venue:str=Field(default='Flexible',max_length=120)
    city:str=Field(default='Chennai',max_length=80)
