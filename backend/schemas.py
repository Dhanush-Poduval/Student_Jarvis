from pydantic import BaseModel
from typing import Optional

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
