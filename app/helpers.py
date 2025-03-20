from models import Todo
from typing import List, Optional
from fastapi import HTTPException


def find_todo_index(todos: List[Todo], todo_id: int) -> int:
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            return index
    raise HTTPException(status_code=404, detail="Todo not found")


def find_todo(todos: List[Todo], todo_id: int) -> Optional[Todo]:
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")
