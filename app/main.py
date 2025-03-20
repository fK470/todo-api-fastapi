from typing import List
from starlette.middleware.cors import CORSMiddleware
from models import TodoTable, Todo, TodoCreate

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from database import get_db


app = FastAPI()

# CORSを回避するために設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Store ---
# todos = []
# next_todo_id = 1


# @app.post("/todo", response_model=Todo, status_code=201)
# async def create_todo(todo_create: TodoCreate):
#     global next_todo_id
#     todo = Todo(id=next_todo_id, **todo_create.model_dump())
#     next_todo_id += 1
#     todos.append(todo)
#     return todo
@app.post("/todo", response_model=Todo, status_code=201)
async def create_todo(todo_create: TodoCreate, db: Session = Depends(get_db)):
    todo = TodoTable(**todo_create.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@app.get("/todos", response_model=List[Todo])
async def read_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoTable).all()
    return todos


@app.get("/todo/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoTable).filter(TodoTable.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# @app.patch("/todo/{todo_id}", response_model=Todo)
# async def update_todo(todo_id: int, todo_update: TodoCreate):
#     index = find_todo_index(todos, todo_id)

#     existing_todo = todos[index]
#     updated_todo = Todo(
#         id=todo_id,
#         **todo_update.model_dump(),
#         done=existing_todo.done
#     )
#     todos[index] = updated_todo
#     return updated_todo
@app.patch("/todo/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoCreate, db: Session = Depends(get_db)):
    try:
        todo = db.query(TodoTable).filter(TodoTable.id == todo_id).first()
        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        for key, value in todo_update.model_dump().items():
            setattr(todo, key, value)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    finally:
        db.refresh(todo)
        return todo


# @app.delete("/todo/{todo_id}")
# async def delete_todo(todo_id: int):
#     index = find_todo_index(todos, todo_id)
#     del todos[index]
#     return {"ok": True}
@app.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoTable).filter(TodoTable.id == todo_id).first()
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"ok": True}
