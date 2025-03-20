import pytest
from fastapi.testclient import TestClient
from .main import app, todos

client = TestClient(app)


def setup_function():
    todos.clear()
    print("Reset data")


@pytest.fixture
def sample_data():
    return client.post(
        "/todo", json={"title": "Test Todo", "description": "Test Description"}
    )


def test_create_todo(sample_data):
    response = sample_data
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert data["id"] == 1
    assert data["done"] == False

    assert len(todos) == 1


def test_read_todos():
    client.post(
        "/todo", json={"title": "Todo 1", "description": "Description 1"}
    )
    client.post(
        "/todo", json={"title": "Todo 2", "description": "Description 2"}
    )

    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Todo 1"
    assert data[1]["title"] == "Todo 2"


def test_read_todo(sample_data):
    response_create = sample_data
    todo_id = response_create.json()["id"]

    response = client.get(f"/todo/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert data["id"] == todo_id


def test_read_todo_not_found():
    response = client.get("/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_update_todo(sample_data):
    response_create = sample_data
    todo_id = response_create.json()["id"]

    response = client.patch(
        f"/todo/{todo_id}",
        json={"title": "Updated Todo", "description": "Updated Description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Todo"
    assert data["description"] == "Updated Description"
    assert data["id"] == todo_id
    assert data["done"] == False


def test_update_todo_not_found():
    response = client.patch(
        "/todo/999", json={"title": "Updated Todo", "description": "Updated Description"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(sample_data):
    response_create = sample_data
    todo_id = response_create.json()["id"]

    response = client.delete(f"/todo/{todo_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert len(todos) == 0


def test_delete_todo_not_found():
    response = client.delete("/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
