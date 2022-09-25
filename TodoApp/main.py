#  author = "Vũ Đức Cường"
#  date = 9/23/22, 9:14 PM
from typing import Optional

from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from TodoApp import models
from TodoApp.ViewModels.todo import TodoViewModel
from TodoApp.auth import get_current_user, get_user_exception
from TodoApp.database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    except Exception as ex:
        print(ex)
    finally:
        db.close()


@app.get("/todos")
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


@app.get("/todos/user")
async def get_all_by_user(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    if not user:
        raise get_user_exception()

    return (
        db.query(models.Todo).filter(models.Todo.owner_id == user.get("user_id")).all()
    )


@app.get("/todos/{todo_id}")
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


@app.post("/todos")
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


@app.put("/todos/{todo_id}")
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


@app.delete("/todos/{todo_id}")
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