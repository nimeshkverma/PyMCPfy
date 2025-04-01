# Flask Todo Example

This example demonstrates how to build a todo list application using Flask and FastMCP.

## Features

- SQLAlchemy database integration
- JWT authentication
- FastMCP integration for MCP functionality
- Resource definitions for todo schema
- Tool definitions for todo operations
- Helpful prompts for todo commands

## Installation

```bash
pip install -r ../../requirements.txt
```

## Running the Example

```bash
flask run
```

## FastMCP Usage

### Resources

```python
@mcp.resource("schema://todos")
def get_todo_schema() -> str:
    """Get the database schema for todos."""
    return """
    Todo:
        id: integer (primary key)
        title: string (required)
        description: text (optional)
        done: boolean (default: false)
        due_date: datetime (optional)
        created_at: datetime (auto)
        user_id: integer (foreign key)
    """
```

### Tools

```python
@mcp.tool()
def create_todo(
    ctx: Context,
    token: str,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None
) -> dict:
    """Create a new todo."""
    todo = Todo(
        title=title,
        description=description,
        due_date=datetime.fromisoformat(due_date) if due_date else None,
        user_id=user.id
    )
    ctx.log.info(f"Created new todo '{title}' for user {username}")
    return todo.__dict__
```

### Prompts

```python
@mcp.prompt()
def todo_guidelines() -> str:
    """Guidelines for creating todos."""
    return """
    When creating or updating a todo:
    1. Title should be clear and concise
    2. Description should provide necessary details
    3. Due dates should be in YYYY-MM-DD format
    4. Mark todos as done when completed
    """
```

## API Endpoints

- `POST /login`: Get JWT token
- `GET /todos`: Get user's todos
- `POST /todos`: Create new todo
- `PUT /todos/<id>`: Update todo
- `DELETE /todos/<id>`: Delete todo

## Testing

1. Get a token:
```bash
curl -X POST http://localhost:5000/login -d '{"username":"user1","password":"pass1"}'
```

2. Get todos:
```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/todos
```

3. Create todo:
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" http://localhost:5000/todos -d '{"title":"Test Todo","description":"Test Description"}'
```

4. Update todo:
```bash
curl -X PUT -H "Authorization: Bearer $TOKEN" http://localhost:5000/todos/1 -d '{"done":true}'
```

5. Delete todo:
```bash
curl -X DELETE -H "Authorization: Bearer $TOKEN" http://localhost:5000/todos/1
```
