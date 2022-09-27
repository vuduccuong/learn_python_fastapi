#  author = "Vũ Đức Cường"
#  date = 9/27/22, 8:18 AM
from fastapi import HTTPException
from starlette import status


def token_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrent username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
