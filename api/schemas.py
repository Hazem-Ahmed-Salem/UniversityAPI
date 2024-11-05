from pydantic import BaseModel ,EmailStr
from datetime import datetime
from typing import Optional

class postBase(BaseModel):
    title: str
    content: str
    published: bool =True

class postCreate(postBase):
    pass

class UserReponse(BaseModel):
    id:int
    email:EmailStr
    #created_at:datetime

    class config:
        orm_mode=True

class PostResponse(postBase):
    id:int
    user:UserReponse
    user_id:int
    created_at: datetime
    
    
    class config:
        orm_mode=True

class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserLogin(BaseModel):
    email:EmailStr
    password:str
    class config:
        orm_mode=True

class token(BaseModel):
    Access_Token:str
    Token_Type:str

class token_data(BaseModel):
    id:int
    email:EmailStr 

class vote_post(BaseModel):
    post_id:int
    vote_dir:int    
