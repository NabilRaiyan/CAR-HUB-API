from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# mysql database url
URL_DATABASE = 'mysql+pymysql://root:Qwerty123key###a@localhost:3306/BlogApplication'
# creating engine
engine = create_engine(URL_DATABASE)

# creating db session and local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()