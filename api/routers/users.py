from fastapi import APIRouter,status,Depends,HTTPException
from ..schemas import UserCreate ,UserReponse
from ..database import get_db
from ..utils import hashing , comparehash
from sqlalchemy.orm import Session
from .. import models


router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

######### Creates a new user #########
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=UserReponse)
def Create_User(user:UserCreate,db:Session=Depends(get_db)):
    user.password=hashing(user.password)
    new_user=models.User(**user.model_dump())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as error:
        print("Error",error)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"message":"something wrong happened"})
    return new_user

######### Authentication a new user #########
