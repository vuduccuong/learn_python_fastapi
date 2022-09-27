#  author = "Vũ Đức Cường"
#  date = 9/23/22, 9:09 PM
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(255))
    priority = Column(Integer, default="")
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="todos")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255))
    username = Column(String(50))
    first_name = Column(String(100))
    last_name = Column(String(100))
    hash_password = Column(String(255))
    is_active = Column(Boolean, default=True)

    todos = relationship("Todo", back_populates="owner")
