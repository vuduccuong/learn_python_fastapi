from typing import Optional

from fastapi import FastAPI, Request, status, responses
from starlette.responses import JSONResponse

from exceptions.custom_exception_1 import CustomExceptionOne
from models.base.response import IResponseModelBase

app = FastAPI()


@app.exception_handler(CustomExceptionOne)
async def custom_exception_handler(request: Request, exception: CustomExceptionOne):
    """
    Custom exception
    :param request: http request
    :param exception:
    :return: Json response
    """
    print(request)
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content=dict(message=f"Ha ha ha {exception.custom_field}"),
    )


@app.get("/", response_model=IResponseModelBase[dict])
async def root(field: Optional[str] = None):
    """

    :param field:
    :return:
    """
    if field and field != "home":
        raise CustomExceptionOne(custom_field=field)

    res = dict(
        message="Hello",
        hi=1234,
    )
    return IResponseModelBase(data=res)


@app.get("/login")
async def login():
    return dict(status=200, message="Login Page")


@app.get("/posts")
async def posts():
    return dict(message="Post Page")
