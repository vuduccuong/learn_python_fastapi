#  author = "Vũ Đức Cường"
#  date = 9/23/22, 8:58 PM
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "mysql+mysqldb://root:mysqlpw@host.docker.internal:49153/todo_db"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()
