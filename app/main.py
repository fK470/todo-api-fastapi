from typing import Annotated

from database import get_db
from fastapi import Depends, FastAPI, HTTPException
from models import Todo, TodoCreate, TodoTable, TodoToggle, TodoUpdate
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/todos", status_code=201)
async def create_todo(todo_create: TodoCreate, db: Annotated[Session, Depends(get_db)]) -> Todo:
    todo = TodoTable(**todo_create.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.get("/todos")
async def read_todos(db: Annotated[Session, Depends(get_db)]) -> list[Todo]:
    todos = db.query(TodoTable).all()
    return todos


@app.get("/todos/{todo_id}")
async def read_todo(todo_id: int, db: Annotated[Session, Depends(get_db)]) -> Todo:
    todo = db.query(TodoTable).filter(TodoTable.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.patch("/todos/{todo_id}")
async def update_todo(todo_id: int, todo_update: TodoUpdate, db: Annotated[Session, Depends(get_db)]) -> Todo:
    try:
        todo = db.query(TodoTable).filter(TodoTable.id == todo_id).first()
        if todo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        for key, value in todo_update.model_dump(exclude_unset=True).items():
            setattr(todo, key, value)
        db.commit()
        db.refresh(todo)
        return todo
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@app.patch("/todos/{todo_id}/toggle")
async def toggle_todo(todo_id: int, todo_toggle: TodoToggle, db: Annotated[Session, Depends(get_db)]) -> Todo:
    try:
        todo = db.query(TodoTable).filter(TodoTable.id == todo_id).first()
        if todo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        todo.done = todo_toggle.done
        db.commit()
        db.refresh(todo)
        return todo
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Annotated[Session, Depends(get_db)]) -> dict[str, bool]:
    todo = db.query(TodoTable).filter(TodoTable.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"ok": True}
