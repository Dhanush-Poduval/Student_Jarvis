from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from .. import models,schemas,database,token
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from passlib.context import CryptContext

app=FastAPI()

router=APIRouter(
    tags=['User']
)

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
hashedPassword=""
@router.post('/user')
def create_user(signup:schemas.Signup , db:Session=Depends(database.get_db)):
    global hashedPassword
    hashedPassword=pwd_context.hash(signup.password)
    new_user=models.User(name=signup.name , email=signup.email , password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/allusers',response_model=List[schemas.Show_User])
def get_allusers(db:Session=Depends(database.get_db)):
    users=db.query(models.User).all()
    return users

@router.get('/users/{id}',response_model=schemas.Show_User)
def get_user(id , db:Session=Depends(database.get_db)):
   user=db.query(models.User).filter(models.User.id==id).first()
   return user

@router.post('/login')
def login(user:schemas.Check_Login, db:Session=Depends(database.get_db)):
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Email not found")
    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Wrong Password")
    
    
    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return{"Access token":access_token,"token type":"bearer"}



