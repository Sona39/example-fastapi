from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from .. import schemas, models, oauth2, database
from ..oauth2 import get_current_user



router = APIRouter(
    prefix="/votes",
    tags=['Vote']
)


@router.post("/{id}")
def vote(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(id == models.Post.id)
    vote_query = db.query(models.Vote).filter(current_user.id == models.Vote.user_id, id == models.Vote.post_id)
    found_vote = vote_query.first()

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if found_vote:
        db.delete(found_vote)   
        db.commit()
        return {"message": "Successfully deleted the vote"}
    
    else:
        new_vote = models.Vote(post_id = id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added the vote"}    




# @router.post("/", status_code=status.HTTP_201_CREATED)
# def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
#          current_user: int = Depends(oauth2.get_current_user)):
#     # Check if the post exists
#     post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")

#     # Check if the user has already voted on the post
#     found_vote = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, 
#                                                models.Vote.user_id == current_user.id).first()
#     if vote.dir == 1:
#         # If the user hasn't voted, add the vote
#         if not found_vote:
#             new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
#             db.add(new_vote)
#             db.commit()
#             return {"message": "Successfully added vote"}
#         else:
#             # If the user has already voted, raise a conflict
#             raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
#                                 detail=f"User {current_user.id} has already voted on post {vote.post_id}")
#     else:
#         # If the user hasn't voted, raise a not found error
#         if not found_vote:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
#         # If the user has voted, delete the vote
#         db.delete(found_vote)
#         db.commit()
#         return {"message": "Successfully deleted vote"}
