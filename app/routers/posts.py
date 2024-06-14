from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, schemas, oauth2
from app.database import get_db
from sqlalchemy import func



router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# GET ALL POSTS            
@router.get("/", response_model=List[schemas.PostOut]) # this enshures that all the posts only have the presaved parameters in the response body
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              skip: int = 0, limit: int = 10,  # Skip and limit querries for showing specific nuber of posts per request
              search: Optional[str] = ""):     # Search querry for searching though the post titles
    
 # --- grabs the posts based on the given criterias from the DB and stors in 'posts' variable ---
   posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
   results = results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
               .outerjoin(models.Vote, models.Vote.post_id == models.Post.id) \
               .group_by(models.Post.id) \
               .filter(models.Post.title.contains(search)).order_by(models.Post.id)\
               .limit(limit).offset(skip)
   return results



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)) :
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(posts)
    if not posts:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post_querry = db.query(models.Post).filter(models.Post.id==id)
    

    if post_querry.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} does not exist")
    
    if post_querry.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    
    post_querry.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_querry.first()




