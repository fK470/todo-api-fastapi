from typing import Optional

from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None


class Todo(TodoCreate):
    id: int
    done: bool = False
