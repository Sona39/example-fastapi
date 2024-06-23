from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content:  str
    published: bool = True


class CreatePost(PostBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime
    class Config:
        orm_mode = True

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str 
    first_name: str
    last_name: str


class UserLogin(BaseModel):
     email: EmailStr
     password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
    first_name: str
    last_name: str
    user_email: str

# class Vote(BaseModel):
#         post_id: int
#         dir: conint(le=1)  # type: ignore


class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    class Config:
        from_attributes = True


class UserUpdateResponse(BaseModel):
    id: int
    email: EmailStr 
    first_name: str
    last_name: str   
    created_at: datetime
    access_token: str
    class Config:
        from_attributes = True

class VoteResponse(BaseModel):
    message: str
    likes: int

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None



class VoteResponse(BaseModel):
    message: str
    likes: int

class VoteStatusResponse(BaseModel):
    liked: bool
    likes: int

class VoteUser(BaseModel):
    postid: int