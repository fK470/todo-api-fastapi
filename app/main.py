from typing import List

from fastapi import FastAPI
from .models import Todo, TodoCreate

from .helpers import find_todo, find_todo_index

app = FastAPI()

# --- Data Store ---
todos = []
next_todo_id = 1


@app.post("/todo", response_model=Todo, status_code=201)
async def create_todo(todo_create: TodoCreate):
    global next_todo_id
    todo = Todo(id=next_todo_id, **todo_create.model_dump())
    next_todo_id += 1
    todos.append(todo)
    return todo


@app.get("/todos", response_model=List[Todo])
async def read_todos():
    return todos


@app.get("/todo/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int):
    return find_todo(todos, todo_id)


@app.patch("/todo/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoCreate):
    index = find_todo_index(todos, todo_id)

    existing_todo = todos[index]
    updated_todo = Todo(
        id=todo_id,
        **todo_update.model_dump(),
        done=existing_todo.done
    )
    todos[index] = updated_todo
    return updated_todo


@app.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int):
    index = find_todo_index(todos, todo_id)
    del todos[index]
    return {"ok": True}
