from jose import JWTError ,jwt
from datetime import datetime ,timedelta
from . import schemas,database,models
from fastapi import Depends ,HTTPException ,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_min

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    print(to_encode)
    encodedJWT=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encodedJWT

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id: int=payload.get("user_id")
        email:str =payload.get("email")
        if not id:
            raise credentials_exception
        if not email:
            raise credentials_exception
        token_data=schemas.token_data(id=id,email=email)
    except JWTError:
        raise credentials_exception
    return token_data
    
    ## we should fitch the user from here and get the user data from the jwt token ##
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials",
                                        headers={"WWW-Authenticate":"Bearer"})
    user_data=verify_access_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id==user_data.id and models.User.email==user_data.email).first()
    return user