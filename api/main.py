from fastapi import FastAPI
from .routers import auth ,users ,post
from . import models
from .database import engine


models.Base.metadata.create_all(bind=engine)



app=FastAPI()

@app.get("/",tags=['Root'])
def root():
    return{"message":""}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(post.router)