from __future__ import annotations

from typing import Optional

from database import Base
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, Text


class TodoTable(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    done = Column(Boolean, default=False)


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class Todo(TodoCreate):
    id: int
    done: bool = False


class TodoToggle(BaseModel):
    done: bool

    class Config:
        from_attributes = True


class TodoUpdate(BaseModel):
    title: Optional[str] = None

    class Config:
        from_attributes = True
