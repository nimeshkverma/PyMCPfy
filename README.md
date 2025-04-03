# PyMCPfy

[![PyPI version](https://badge.fury.io/py/pymcpfy.svg)](https://badge.fury.io/py/pymcpfy)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A Python library that seamlessly integrates web frameworks with the Model Context Protocol (MCP), enabling AI-powered interactions with your web applications.

## Overview

PyMCPfy bridges the gap between web frameworks and AI models by exposing your APIs through the Model Context Protocol. Built on top of FastMCP, it provides framework-specific integrations for Django, Flask, and FastAPI, making it easy to expose your web application's functionality to AI models while maintaining clean, idiomatic code.

## Features

- 🚀 **Framework Integration**: Native support for Django, Flask, and FastAPI
- 🎯 **MCP Decorators**: Simple decorators to expose:
  - Resources: Web endpoints and views
  - Tools: Function-based operations
  - Prompts: AI-specific text generation helpers
- 🔒 **Secure**: Built-in security features and best practices
- 🛠️ **Developer Tools**: MCP Inspector integration for testing and debugging
- 📚 **Type Safety**: Full type hints and modern Python features
- ⚡ **Performance**: Optimized for both sync and async operations

## Installation

```bash
pip install pymcpfy
```

## Quick Start

### Flask Integration

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pymcpfy.flask import mcpfy_resource, mcpfy_tool, mcpfy_prompt

app = Flask(__name__)
db = SQLAlchemy(app)

# Resource: Expose REST endpoints
@app.route("/user/<int:user_id>")
@mcpfy_resource(uri="/user/{user_id}")
def get_user(user_id: int):
    """Get user details by ID."""
    user = User.query.get_or_404(user_id)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }

# Tool: Expose functions for AI operations
@mcpfy_tool()
def create_user(username: str, email: str) -> dict:
    """Create a new user.
    
    Args:
        username: The user's username
        email: The user's email address
    
    Returns:
        dict: The created user's details
    """
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }

# Prompt: AI-specific text generation
@mcpfy_prompt()
def generate_welcome_message(user_data: dict) -> str:
    """Generate a personalized welcome message.
    
    Args:
        user_data: User information dictionary
            - username: The user's username
            - email: The user's email
    
    Returns:
        str: Personalized welcome message
    """
    return f"Welcome {user_data['username']}! Your account has been created."
def create_user(name: str, email: str) -> dict:
    """Create a new user.
    
    Args:
        name: The user's full name
        email: The user's email address
    
    Returns:
        dict: The created user's details
    """
    user = User.objects.create(name=name, email=email)
    return {"id": user.id, "name": user.name}
```

### Django Integration

```python
from django.contrib.auth.models import User
from django.http import JsonResponse
from pymcpfy.django import mcpfy_resource, mcpfy_tool, mcpfy_prompt

# Resource: Expose Django views
@mcpfy_resource(uri="/user/{user_id}")
def get_user(request, user_id: int):
    """Get user details by ID."""
    try:
        user = User.objects.get(id=user_id)
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

# Tool: Expose model operations
@mcpfy_tool()
def create_user(username: str, email: str, password: str) -> dict:
    """Create a new user."""
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
```

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from pymcpfy.fastapi import mcpfy_resource, mcpfy_tool, mcpfy_prompt

app = FastAPI()

# Resource: Expose FastAPI endpoints
@app.get("/user/{user_id}")
@mcpfy_resource(uri="/user/{user_id}")
async def get_user(user_id: int, db: Session):
    """Get user details by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }

# Tool: Expose async operations
@mcpfy_tool()
async def create_user(username: str, email: str) -> dict:
    """Create a new user."""
    user = User(username=username, email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
```

## Testing with MCP Inspector

PyMCPfy includes built-in support for the MCP Inspector, allowing you to test and debug your MCP integrations interactively.

### Prerequisites

1. Install FastMCP:
```bash
pip install fastmcp
```

### Running Examples with MCP Inspector

1. **Flask Example**:
```bash
# Navigate to the Flask example directory
cd examples/flask_example

# Run with MCP Inspector
python app.py --mcp
```

2. **Django Example**:
```bash
# Navigate to the Django example directory
cd examples/django_example

# Run with MCP Inspector
python manage.py runserver --mcp
```

3. **FastAPI Example**:
```bash
# Navigate to the FastAPI example directory
cd examples/fastapi_example

# Run with MCP Inspector
python app.py --mcp
```

The MCP Inspector provides:
- Interactive testing of resources, tools, and prompts
- Real-time logs and error messages
- Performance monitoring
- Environment variable management
- Request/response inspection
## Documentation

For detailed documentation, visit our [documentation site](https://pymcpfy.readthedocs.io/).

## Contributing

We welcome contributions to PyMCPfy! Here's how you can help:

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pymcpfy.git
cd pymcpfy
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=pymcpfy

# Run specific test file
pytest tests/test_flask.py
```

### Code Style

We use:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

Run all checks:
```bash
# Format code
black .
isort .

# Check code
flake8 .
mypy .
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and style checks
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Documentation

- Add docstrings to all public functions and classes
- Update README.md for significant changes
- Add example code when appropriate
- Include type hints

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support and Community

- 📫 [GitHub Issues](https://github.com/yourusername/pymcpfy/issues)
- 💬 [Discord Community](https://discord.gg/pymcpfy)
- 📧 Email: support@pymcpfy.org
