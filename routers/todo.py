#  author = "Vũ Đức Cường"
#  date = 9/25/22, 5:21 PM
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette import status

import models
from ViewModels.todo import TodoViewModel
from database import SessionLocal, engine
from exceptions.user import get_user_exception
from routers.auth import get_current_user


models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/todos",
    tags=["Todo"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
    },
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    except Exception as ex:
        print(ex)
    finally:
        db.close()


@router.get("/test")
async def test(request: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return templates.TemplateResponse(
        name="home.html",
        context={
            "request": request,
            "todos": todos,
        },
    )


@router.get("/")
async def root(
    title: Optional[str] = None,
    owner_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Todo)
    if title:
        query = query.filter(models.Todo.title.contains(title))
    if owner_id:
        query = query.filter(models.Todo.owner_id == owner_id)

    return query.all()


@router.get("/user")
async def get_all_by_user(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    if not user:
        raise get_user_exception()

    return (
        db.query(models.Todo).filter(models.Todo.owner_id == user.get("user_id")).all()
    )


@router.get("/{todo_id}")
async def get_single(
    todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    if not user:
        raise get_user_exception()

    try:
        todo = (
            db.query(models.Todo)
            .filter(models.Todo.id == todo_id)
            .filter(models.Todo.owner_id == user.get("user_id"))
            .first()
        )
        if todo is not None:
            return {
                "status": status.HTTP_200_OK,
                "data": todo,
            }
    except Exception as ex:
        print(ex)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found!")


@router.post("/")
async def create(
    todo: TodoViewModel,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user:
        raise get_user_exception()

    try:
        todo_entity = models.Todo()
        todo_entity.title = todo.title
        todo_entity.description = todo.description
        todo_entity.priority = todo.priority
        todo_entity.complete = todo.complete
        todo_entity.owner_id = user.get("user_id")

        db.add(todo_entity)
        db.commit()
    except Exception as e:
        print(e)
        raise e

    return {"success": True}


@router.put("/{todo_id}")
async def update(
    todo_id: int,
    todo: TodoViewModel,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    todo_db = (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id)
        .filter(models.Todo.owner_id == user.get("user_id"))
        .first()
    )
    if todo_db is not None:
        todo_db.title = todo.title
        todo_db.description = todo.description
        todo_db.priority = todo.priority
        todo_db.complete = todo.complete

        db.add(todo_db)
        db.commit()

        return {
            "status": status.HTTP_200_OK,
            "data": todo,
        }

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found!")


@router.delete("/{todo_id}")
async def delete(
    todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    todo = (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id)
        .filter(models.Todo.owner_id == user.get("user_id)"))
        .first()
    )
    db.delete(todo)
    db.commit()

    return {
        "status": status.HTTP_204_NO_CONTENT,
    }
