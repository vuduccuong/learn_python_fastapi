#  author = "Vũ Đức Cường"
#  date = 9/25/22, 12:46 PM
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from requests import Session
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status
from jose import jwt, JWTError
from datetime import datetime, timedelta

from TodoApp import models
from TodoApp.ViewModels.todo import CreateUserViewModel
from TodoApp.database import engine, SessionLocal


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "Thasdjal;sfhjkwh3lkasjlk;asdkjasdkjh"
ALGORITHM = "HS256"

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    except Exception as ex:
        print(ex)
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def get_user_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def token_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrent username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise get_user_exception()
    if not verify_password(password, user.hash_password):
        raise token_exception()

    return user


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(user: models.User, exprires_delta: Optional[timedelta] = None):
    expire = datetime.utcnow() + timedelta(minutes=15)
    if exprires_delta:
        expire = datetime.utcnow() + exprires_delta

    encode = {"sub": user.username, "id": user.id, "exp": expire}

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if not all([username, user_id]):
            raise get_user_exception()

        return dict(
            username=username,
            user_id=user_id,
        )
    except JWTError:
        raise token_exception()


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_new_user(
    create_user: CreateUserViewModel, db: Session = Depends(get_db)
):
    user_entity = models.User()
    user_entity.username = create_user.username
    user_entity.email = create_user.email
    user_entity.first_name = create_user.first_name
    user_entity.last_name = create_user.last_name
    user_entity.hash_password = get_password_hash(create_user.password)

    db.add(user_entity)
    db.commit()

    return user_entity


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db=db,
    )
    if not user:
        raise get_user_exception()

    return {"jwt_token": create_access_token(user=user)}
