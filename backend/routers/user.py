from fastapi import FastAPI,APIRouter,Depends
from .. import models,schemas,database
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

app=FastAPI()

router=APIRouter(
    tags=['User']
)

@router.post('/user')
def create_user(signup:schemas.Signup , db:Session=Depends(database.get_db)):
    new_user=models.User(name=signup.name , email=signup.email , password=signup.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/allusers',response_model=List[schemas.Show_User])
def get_allusers(db:Session=Depends(database.get_db)):
    users=db.query(models.User).all()
    return users