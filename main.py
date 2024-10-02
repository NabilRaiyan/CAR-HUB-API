import string
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Annotated

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import pyshorteners



app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title: str
    content: str
    image_url: str
    user_id: int


class UserBase(BaseModel):
    username: str
    

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/posts/{title}", status_code=status.HTTP_200_OK)
async def get_post(post_title: str, db:db_dependency):
    post = db.query(models.Post).filter(models.Post.title == post_title).first()
    if post is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post is not found in the database")
    return post
    

@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    url_shortener = pyshorteners.Shortener()
    short_url = url_shortener.tinyurl.short(post.image_url)
    
    post_data = post.dict()
    post_data['image_url'] = short_url
    
    print("The Shortened URL is: " + short_url)
    db_post = models.Post(**post_data)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
        