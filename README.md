# PyMCPfy

[![PyPI version](https://badge.fury.io/py/pymcpfy.svg)](https://badge.fury.io/py/pymcpfy)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A Python library to easily expose web framework APIs via the Model Context Protocol (MCP).

## Overview

PyMCPfy simplifies the process of exposing your Django, Flask, and FastAPI endpoints through MCP, enabling seamless integration with AI models and applications. Built on top of FastMCP, it provides a high-level, framework-specific interface while maintaining the power and flexibility of the underlying MCP implementation.

## Features

- 🚀 Easy integration with Django, Flask, and FastAPI
- 🎯 Simple decorators for Resources, Tools, and Prompts
- 🔒 Secure MCP server management
- 🛠️ Framework-specific utilities and helpers
- 📚 Comprehensive documentation
- ✨ Type hints and modern Python features

## Installation

```bash
pip install pymcpfy
```

## Quick Start

### Django

```python
from pymcpfy.django import mcpfy_resource, mcpfy_tool

@mcpfy_resource
def get_user(request, user_id: int):
    user = User.objects.get(id=user_id)
    return {"id": user.id, "name": user.name}

@mcpfy_tool
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

### Flask

```python
from pymcpfy.flask import mcpfy_resource, mcpfy_tool

@app.route("/user/<int:user_id>")
@mcpfy_resource
def get_user(user_id: int):
    user = User.query.get(user_id)
    return {"id": user.id, "name": user.name}

@mcpfy_tool
def create_user(name: str, email: str) -> dict:
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return {"id": user.id, "name": user.name}
```

### FastAPI

```python
from pymcpfy.fastapi import mcpfy_resource, mcpfy_tool

@app.get("/user/{user_id}")
@mcpfy_resource
async def get_user(user_id: int):
    user = await User.get(id=user_id)
    return {"id": user.id, "name": user.name}

@mcpfy_tool
async def create_user(name: str, email: str) -> dict:
    user = await User.create(name=name, email=email)
    return {"id": user.id, "name": user.name}
```

## Documentation

For detailed documentation, visit our [documentation site](https://pymcpfy.readthedocs.io/).

## Contributing

We welcome contributions! Please see our [Contributing Guide](docs/contributing.md) for details.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support and Community

- 📫 [GitHub Issues](https://github.com/yourusername/pymcpfy/issues)
- 💬 [Discord Community](https://discord.gg/pymcpfy)
- 📧 Email: support@pymcpfy.org
