from fastapi import APIRouter,status,Depends,HTTPException,Response
from ..schemas import vote_post
from typing import List,Optional
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,oauth2

router=APIRouter(
    prefix="vote",
    tags="vote"
)


router.post()