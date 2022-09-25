#  author = "Vũ Đức Cường"
#  date = 9/23/22, 9:14 PM
from typing import Optional

from fastapi import FastAPI

from TodoApp.routers import auth, todo
from TodoApp.company import company_api

app = FastAPI()
app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(
    company_api.router,
    prefix="/companies",
    tags=["Company"],
)
