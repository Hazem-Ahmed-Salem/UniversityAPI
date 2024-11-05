from fastapi import APIRouter,status,Depends,HTTPException,Response
from ..schemas import PostResponse,postCreate
from typing import List,Optional
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,oauth2



router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)
###### Gets all posts ######   it allows searching
@router.get("/",status_code=status.HTTP_302_FOUND,response_model=List[PostResponse])
def Get_Posts(search:Optional[str]="",limit:int=5,skip:int=0,db:Session=Depends(get_db),user=Depends(oauth2.get_current_user)):
    
    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"there is not post with title {search}")
    return posts

###### creates a post ######
@router.post("/",status_code=status.HTTP_302_FOUND,response_model=postCreate)
def create_Post(post:postCreate,db:Session=Depends(get_db),user=Depends(oauth2.get_current_user)):
    print(user.email)
    newpost=models.Post(**post.model_dump(),user_id=user.id)
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    return newpost    

###### Gets a post by id ######
@router.get("/{id}",status_code=status.HTTP_302_FOUND,response_model=PostResponse)
def Get_Post(id:int,db:Session=Depends(get_db),user=Depends(oauth2.get_current_user)):
    try:
        wanted=db.query(models.Post).filter(models.Post.id==id).first()
    except Exception as error:
        print("Error",error)
        return {"Error":error.__str__()}
    if wanted==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"mesaage":"post was not found"})

    else:
        return wanted
    
###### Deletes a post by id ######
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def Delete_Post(id:int,db:Session=Depends(get_db),user=Depends(oauth2.get_current_user)):
    Deleted_Post_query=db.query(models.Post).filter(models.Post.id==id)
    Deleted_Post=Deleted_Post_query.first()
    if not Deleted_Post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":"post was not found"})
    else:
        if Deleted_Post.user_id!=user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not Authorized to perform requested action")    
        
        # db.delete(Deleted_Post) you can use this to delete too
        Deleted_Post_query.delete(synchronize_session=False)
        db.commit()
            

 ###### Updates a post by id ######
@router.put("/{id}",response_model=PostResponse)
def Update_Post(id:int ,post:postCreate,response:Response,db:Session=Depends(get_db),user=Depends(oauth2.get_current_user)):
    try:
        post_q=db.query(models.Post).filter(models.Post.id==id)
    except Exception as error:
        response.status_code=status.HTTP_400_BAD_REQUEST
        print("Error",error)
        return {"Error":error.__str__()}
    
    if not post_q.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":"post was not found"})

    
    if post_q.first().user_id!=user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not Authorized to perform requested action")
    post_q.update(post.model_dump())
    db.commit()  
    return post_q.first()

