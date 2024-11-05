from fastapi import APIRouter,status,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas import UserCreate ,token
from ..database import get_db
from ..utils import  comparehash
from sqlalchemy.orm import Session
from .. import models,oauth2


router=APIRouter(
    
    tags=["Authentication"]
)

@router.post('/login',response_model=token)
def login(user_credentials:UserCreate,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={"message":"invalid user credentials"})
    if  not comparehash(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={"message":"invalid user credentials"})
    else:
        access_token=oauth2.create_access_token(data={"user_id":user.id,"email":user.email})
        return {"Access_Token":access_token,
                "Token_Type":"Bearer"
                }
