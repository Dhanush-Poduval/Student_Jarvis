from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Signup(BaseModel):
    name:str
    email:str
    password:str
class Show_User(BaseModel):
    id:int
    name:str
    email:str
    class Config():
        orm_mode=True
class User(BaseModel):
    name:str
    email:str
    password:str
    
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


class TokenData(BaseModel): #jwt
    username: Optional[str]=None

class DocumentBase(BaseModel):
    filename:str
    filepath:str
    document_text:str
    id:int
    user_id:int
class Document(BaseModel):
    filename:str
    id:int
    document_text:str
    class Config():
        orm_mode=True