#  author = "Vũ Đức Cường"
#  date = 9/23/22, 9:14 PM
from fastapi import FastAPI

from routers import auth, todo
from starlette.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(todo.router)
