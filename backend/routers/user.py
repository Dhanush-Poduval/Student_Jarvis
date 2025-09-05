from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from .. import models,schemas,database,token
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
app=FastAPI()

router=APIRouter(
    tags=['User']
)

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

@router.post('/user')
def create_user(signup:schemas.Signup , db:Session=Depends(database.get_db)):
    hashedPassword=""
    hashedPassword=pwd_context.hash(signup.password)
    new_user=models.User(name=signup.name , email=signup.email , password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token=token.create_access_token(
        data={"sub":new_user.email}
    )
    return{"access_token":access_token,"token_type":"bearer"}
@router.get('/allusers',response_model=List[schemas.Show_User])
def get_allusers(db:Session=Depends(database.get_db)):
    users=db.query(models.User).all()
    return users

@router.get('/users/{id}',response_model=schemas.Show_User)
def get_user(id , db:Session=Depends(database.get_db)):
   user=db.query(models.User).filter(models.User.id==id).first()
   return user

@router.post('/login')
def login(user:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)):
    
    db_user = db.query(models.User).filter(models.User.email == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Email not found")
    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Wrong Password")
    
    
    access_token = token.create_access_token(
        data={"sub": user.username}
    )
    print(access_token)
    return{"access_token":access_token,"token_type":"bearer"}



