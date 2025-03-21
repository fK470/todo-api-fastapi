import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

todos = []


def setup_function() -> None:
    todos.clear()


@pytest.fixture
def sample_data() -> TestClient:
    return client.post("/todos", json={"title": "Test Todo", "description": "Test Description"})


def test_create_todo(sample_data: TestClient) -> None:
    response = sample_data
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert data["id"] == 1
    assert not data["done"]

    assert len(todos) == 1


def test_read_todos() -> None:
    client.post("/todos", json={"title": "Todo 1", "description": "Description 1"})
    client.post("/todos", json={"title": "Todo 2", "description": "Description 2"})

    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Todo 1"
    assert data[1]["title"] == "Todo 2"


def test_read_todo(sample_data: TestClient) -> None:
    response_create = sample_data
    todo_id = response_create.json()["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert data["id"] == todo_id


def test_read_todo_not_found() -> None:
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_update_todo(sample_data: TestClient) -> None:
    response_create = sample_data
    todo_id = response_create.json()["id"]

    response = client.patch(
        f"/todos/{todo_id}",
        json={"title": "Updated Todo", "description": "Updated Description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Todo"
    assert data["description"] == "Updated Description"
    assert data["id"] == todo_id
    assert not data["done"]


def test_update_todo_not_found() -> None:
    response = client.patch("/todo/999", json={"title": "Updated Todo", "description": "Updated Description"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(sample_data: TestClient) -> None:
    response_create = sample_data
    todo_id = response_create.json()["id"]

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert len(todos) == 0


def test_delete_todo_not_found() -> None:
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
