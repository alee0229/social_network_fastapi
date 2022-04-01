from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr  
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password:str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


#Inheritance PostBase : TITLE, CONTENT, and PUBLISHED
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

#CONVERTS THE DATA TO A DICT SO THE CREATE POST CAN READ IT
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]= None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)