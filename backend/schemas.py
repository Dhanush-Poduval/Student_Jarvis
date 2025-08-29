from pydantic import BaseModel


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
    password:str