from datetime import timedelta,timezone,datetime
from jose import JWTError,jwt
from dotenv import load_dotenv
from . import schemas
import os
load_dotenv()
SECRET_KEY = os.getenv("my_secret_key")
ALGORITHM = os.getenv("my_algo")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token1:str,credentials_exception):
    try:
        payload = jwt.decode(token1, SECRET_KEY, algorithms=[ALGORITHM])
        email:str=payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data=schemas.TokenData(username=email)
        return token_data
    except JWTError:
         raise credentials_exception
    
       