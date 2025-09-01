from .database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Text
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import relationship

IST=timezone(timedelta(hours=5,minutes=30))


class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String , unique=True)
    password=Column(String,nullable=False)
    chat_sessions=relationship("ChatSessions",back_populates="user")

class ChatSessions(Base):
    __tablename__="chat_sessions"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("user.id"))
    title=Column(String,nullable=False)
    user=relationship("User",back_populates="chat_sessions")
    messages=relationship("ChatHistory",back_populates="session",cascade="all, delete")
    documents=relationship("Documents",back_populates="session",cascade="all, delete")
    summary=relationship("Summary",back_populates="session",cascade="all, delete")
    audio_files=relationship("Audio",back_populates="session",cascade="all, delete")



class Documents(Base):
    __tablename__="documents"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("user.id"))
    filename=Column(String)
    session_id=Column(Integer,ForeignKey("chat_sessions.id"))
    file_path=Column(String)
    document_text=Column(String)
    uploaded_at=Column(DateTime(timezone=True),default=lambda:datetime.now(IST))
    session = relationship("ChatSessions", back_populates="documents")

class Summary(Base):
    __tablename__="summary"
    id=Column(Integer,primary_key=True,index=True)
    document_id=Column(Integer,ForeignKey("documents.id"))
    summary_text=Column(Text)
    session_id=Column(Integer,ForeignKey("chat_sessions.id"))
    session = relationship("ChatSessions", back_populates="summary")

class Flashcards(Base):
    __tablename__="flashcard"
    id=Column(Integer, primary_key=True,index=True)
    summary_id=Column(ForeignKey("summary.id"))
    point =Column(Integer)
    answer=Column(String)
    session_id=Column(Integer,ForeignKey("chat_sessions.id"))


class Audio(Base):
    __tablename__="audio"
    id=Column(Integer,primary_key=True,index=True)
    flashcard_id=Column(Integer,ForeignKey("flashcard.id"))
    audio_path=Column(String)
    session_id=Column(Integer,ForeignKey("chat_sessions.id"))
    session = relationship("ChatSessions", back_populates="audio_files")

    

class ChatHistory(Base):
    __tablename__="chat_history"
    id=Column(Integer,primary_key=True,index=True)
    session_id=Column(Integer,ForeignKey("chat_sessions.id"))
    question=Column(Text,nullable=False)
    answer=Column(Text,nullable=False)
    
    session=relationship("ChatSessions",back_populates="messages")
    
