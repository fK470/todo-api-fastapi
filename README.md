# Todo API with FastAPI and MySQL

This project is a RESTful API for managing a todo list, built with FastAPI and MySQL. It provides endpoints for creating, reading, updating, toggling, and deleting todo items.

## Features

- **CRUD ToDos:** ToDo app.
- **Code Quality:** Uses `ruff` for linting and code quality checks.

## Technologies Used

- **FastAPI:** Python framework
- **MySQL:** RDBMS
- **SQLAlchemy:** ORM
- **Pydantic:** Type annotations and Data validation
- **Docker:** Managed by Docker for easy deployment
- **Uvicorn:** ASGI server
- **pytest:** Testing framework
- **ruff:** Linter and formatter

## Getting Started

### Prerequisites

-   Docker
-   Python 3.9+
-   pip

### Usage

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd todo-api-fast-api
    ```

2.  **Build and run the Docker containers:**

    ```bash
    docker-compose up --build
    ```

#### Running locally (optional)

1. **Create a virtual environment**
    ```bash
    python3 -m venv venv
    ```

2. **Activate the virtual environment**
    ```bash
    source venv/bin/activate
    ```

3. **Install Python dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the dev API server**
    ```bash
    uvicorn app.main:app --reload
    ```

### API Endpoints

-   **POST /todos:** Create a new todo.
    -   Request Body:
        ```json
        {
            "title": "My Todo",
            "description": "Todo description"
        }
        ```
    -   Response:
        ```json
        {
            "id": 1,
            "title": "My Todo",
            "description": "Todo description",
            "done": false
        }
        ```

-   **GET /todos:** Get all todos.
    -   Response:
        ```json
        [
            {
                "id": 1,
                "title": "My Todo",
                "description": "Todo description",
                "done": false
            },
            {
                "id": 2,
                "title": "Another Todo",
                "description": null,
                "done": true
            }
        ]
        ```

-   **GET /todos/{todo_id}:** Get a specific todo.
    -   Response:
        ```json
        {
            "id": 1,
            "title": "My Todo",
            "description": "Todo description",
            "done": false
        }
        ```

-   **PATCH /todos/{todo_id}:** Update a todo.
    -   Request Body:
        ```json
        {
            "title": "Updated Todo",
            "description": "Updated description"
        }
        ```
    -   Response:
        ```json
        {
            "id": 1,
            "title": "Updated Todo",
            "description": "Updated description",
            "done": false
        }
        ```

-   **PATCH /todos/{todo_id}/toggle:** Toggle a todo's `done` status.
    -   Request Body:
        ```json
        {
            "done": true
        }
        ```
    -   Response:
        ```json
        {
            "id": 1,
            "title": "My Todo",
            "description": "Todo description",
            "done": true
        }
        ```

-   **DELETE /todos/{todo_id}:** Delete a todo.
    -   Response:
        ```json
        {
            "ok": true
        }
        ```

### Running Tests

To run the tests, use `pytest`:

```bash
pytest
```