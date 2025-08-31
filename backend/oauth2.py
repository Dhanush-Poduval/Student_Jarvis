from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,SecurityScopes
from . import token

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def get_current_user( security_scopes: SecurityScopes,token1:str=Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    return token.verify_token(token1,credentials_exception)