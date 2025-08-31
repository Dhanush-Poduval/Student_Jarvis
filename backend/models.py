from .database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime
from datetime import datetime, timezone, timedelta

IST=timezone(timedelta(hours=5,minutes=30))


class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String , unique=True)
    password=Column(String,nullable=False)


class Documents(Base):
    __tablename__="documents"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("user.id"))
    filename=Column(String)
    file_path=Column(String)
    uploaded_at=Column(DateTime(timezone=True),default=lambda:datetime.now(IST))

class Summary(Base):
    __tablename__="summary"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("document.id"))
    
