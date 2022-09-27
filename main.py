#  author = "Vũ Đức Cường"
#  date = 9/23/22, 9:14 PM
from typing import Optional

from fastapi import FastAPI


from company import company_api

from routers import auth, todo

app = FastAPI()
app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(
    company_api.router,
    prefix="/companies",
    tags=["Company"],
)
