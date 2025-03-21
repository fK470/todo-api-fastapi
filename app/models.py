from __future__ import annotations

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
    description: str | None = None

    class Config:
        orm_mode = True


class Todo(TodoCreate):
    id: int
    done: bool = False


class TodoToggle(BaseModel):
    done: bool

    class Config:
        orm_mode = True


class TodoUpdate(BaseModel):
    title: str | None = None

    class Config:
        orm_mode = True
