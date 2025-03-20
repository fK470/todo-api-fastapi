from typing import Optional
from sqlalchemy import Column, Integer, Text, Boolean
from database import Base, ENGINE

from pydantic import BaseModel


class TodoTable(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    done = Column(Boolean, default=False)


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class Todo(TodoCreate):
    id: int
    done: bool = False


# def main():
#     Base.metadata.create_all(bind=ENGINE)


# if __name__ == "__main__":
#     main()
