from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Signup(BaseModel):
    name:str
    email:str
    password:str
class Show_User(BaseModel):
    name:str
    email:str
    class Config():
        orm_mode=True
    
class Login(BaseModel):
    name:str
    email:str
    password:str
class Check_Login(BaseModel):
    email:str
    password:str
    class Config():
        orm_mode=True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str]=None

class DocumentBase(BaseModel):
    filename:str
    file_path:str
class DocumentCreate(DocumentBase):
    user_id:int
class DocumentOut(DocumentBase):
    id:int
    user_id:int
    uploaded_at:datetime
    class Config:
        orm_mode=True