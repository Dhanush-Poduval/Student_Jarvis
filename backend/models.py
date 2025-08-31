from .database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Text
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
    document_text=Column(String)
    uploaded_at=Column(DateTime(timezone=True),default=lambda:datetime.now(IST))

class Summary(Base):
    __tablename__="summary"
    id=Column(Integer,primary_key=True,index=True)
    document_id=Column(Integer,ForeignKey("documents.id"))
    summary_text=Column(Text)

class Flashcards(Base):
    __tablename__="flashcard"
    id=Column(Integer, primary_key=True,index=True)
    summary_id=Column(ForeignKey("summary.id"))
    point =Column(Integer)
    answer=Column(String)

class Audio(Base):
    __tablename__="audio"
    id=Column(Integer,primary_key=True,index=True)
    flashcard_id=Column(Integer,ForeignKey("flashcard.id"))
    audio_path=Column(String)
    
