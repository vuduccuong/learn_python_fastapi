#  author = "Vũ Đức Cường"
#  date = 9/23/22, 9:14 PM
from fastapi import FastAPI

from routers import auth, todo

app = FastAPI()
app.include_router(auth.router)
app.include_router(todo.router)
