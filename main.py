import string
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Annotated

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import pyshorteners


# initiating FastAPI
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Post Base interface
class PostBase(BaseModel):
    title: str
    content: str
    image_url: str
    user_id: int


# User Base interface
class UserBase(BaseModel):
    username: str
    
# get db function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

# get post by title route
@app.get("/posts/{title}", status_code=status.HTTP_200_OK)
async def get_post(post_title: str, db:db_dependency):
    post = db.query(models.Post).filter(models.Post.title == post_title).first()
    if post is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post is not found in the database")
    return post
    
# creating user  
@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()


# creating post 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    # shortening url of image
    url_shortener = pyshorteners.Shortener()
    short_url = url_shortener.tinyurl.short(post.image_url)
    
    # initializing new short image url to our post object
    post_data = post.dict()
    post_data['image_url'] = short_url
    
    print("The Shortened URL is: " + short_url)
    
    # saving data to the db
    db_post = models.Post(**post_data)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
        