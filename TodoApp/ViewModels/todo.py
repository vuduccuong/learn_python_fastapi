#  author = "Vũ Đức Cường"
#  date = 9/23/22, 9:42 PM
from typing import Optional

from pydantic import BaseModel, Field


class TodoViewModel(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6)
    complete: bool


class CreateUserViewModel(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
