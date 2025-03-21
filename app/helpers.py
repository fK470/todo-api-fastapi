from __future__ import annotations

from typing import Optional

from fastapi import HTTPException
from models import Todo


def find_todo_index(todos: list[Todo], todo_id: int) -> int:
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            return index
    raise HTTPException(status_code=404, detail="Todo not found")


def find_todo(todos: list[Todo], todo_id: int) -> Optional(Todo):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")
