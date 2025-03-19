from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# --- Data Store ---
# Using a list for an in-memory database is fine for a small example, but in production
# you'd likely use a real database.
todos = []
next_todo_id = 1  # Initialize the ID counter outside of the function.


# --- Models ---
class TodoCreate(BaseModel):
    """Model for creating a new Todo item."""

    title: str
    description: Optional[str] = None


class Todo(TodoCreate):
    """Model representing a Todo item."""

    id: int
    done: bool = False


# --- Helper Functions ---
def find_todo_index(todo_id: int) -> int:
    """Helper function to find the index of a Todo by its ID."""
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            return index
    return -1  # Return -1 if not found


def find_todo(todo_id: int) -> Optional[Todo]:
    """Helper function to find a Todo by its ID."""
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return None


# --- API Endpoints ---
@app.get("/api/v1/", tags=["Root"])
async def read_root():
    """Root endpoint to check if the API is working."""
    return {"message": "In-Memory TODO API is working!"}


@app.post("/api/v1/todos/", response_model=Todo, status_code=201, tags=["Todos"])
async def create_todo(todo_create: TodoCreate):
    """Create a new Todo item."""
    global next_todo_id  # Access the global variable
    todo = Todo(id=next_todo_id, **todo_create.dict())
    next_todo_id += 1  # Increment the counter
    todos.append(todo)
    return todo


@app.get("/api/v1/todos/", response_model=List[Todo], tags=["Todos"])
async def read_todos():
    """Get all Todo items."""
    return todos


@app.get("/api/v1/todos/{todo_id}", response_model=Todo, tags=["Todos"])
async def read_todo(todo_id: int):
    """Get a Todo item by ID."""
    todo = find_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/api/v1/todos/{todo_id}", response_model=Todo, tags=["Todos"])
async def update_todo(todo_id: int, todo_update: TodoCreate):
    """Update a Todo item by ID."""
    index = find_todo_index(todo_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Todo not found")

    existing_todo = todos[index]
    updated_todo = Todo(id=todo_id, **todo_update.dict(), done=existing_todo.done)
    todos[index] = updated_todo
    return updated_todo


@app.delete("/api/v1/todos/{todo_id}", tags=["Todos"])
async def delete_todo(todo_id: int):
    """Delete a Todo item by ID."""
    index = find_todo_index(todo_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[index]
    return {"ok": True}
