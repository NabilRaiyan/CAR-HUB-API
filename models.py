from sqlalchemy import Boolean, Column, Integer, String
from database import Base

# User schema
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)


class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(50))
    image_url = Column(String(150))
    user_id = Column(Integer)
    
    


