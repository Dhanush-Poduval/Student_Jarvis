from datetime import timedelta,timezone,datetime
from jose import JWTError,jwt
from dotenv import load_dotenv
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