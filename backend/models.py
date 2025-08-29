from .database import Base
from sqlalchemy import Column,Integer,String

class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String , unique=True)
    password_hasg=Column(String,nullable=False)