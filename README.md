# PyMCPfy: MCP-fy Your Python Web APIs

[![PyPI version](https://badge.fury.io/py/pymcpfy.svg)](https://badge.fury.io/py/pymcpfy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/pymcpfy.svg)](https://pypi.org/project/pymcpfy/)

PyMCPfy is a Python library that enables developers to easily expose their existing web framework APIs (Django, Flask, and FastAPI) via the Model Context Protocol (MCP). It handles the complexities of MCP integration while providing a simple and consistent developer experience.

## Quick Start

1. Install PyMCPfy with your preferred framework:

```bash
# For Django
pip install "pymcpfy[django]"

# For Flask
pip install "pymcpfy[flask]"

# For FastAPI
pip install "pymcpfy[fastapi]"
```

2. Expose your API endpoints via MCP:

```python
# Django example
from pymcpfy.django import mcpfy

@mcpfy()
def get_user(request, user_id: int):
    user = User.objects.get(id=user_id)
    return JsonResponse({"name": user.name, "email": user.email})

# Flask example
from pymcpfy.flask import mcpfy

@app.route("/user/<int:user_id>")
@mcpfy()
def get_user(user_id: int):
    user = User.query.get(user_id)
    return jsonify({"name": user.name, "email": user.email})

# FastAPI example
from pymcpfy.fastapi import mcpfy

@app.get("/user/{user_id}")
@mcpfy()
async def get_user(user_id: int):
    user = await User.get(id=user_id)
    return {"name": user.name, "email": user.email}
```

3. Start your MCP server:

```bash
# Django
python manage.py runmcp

# Flask/FastAPI
python app.py --mcp
```

## Features

- Framework-agnostic core with specific integrations for Django, Flask, and FastAPI
- Automatic MCP schema generation from your existing API endpoints
- Support for WebSocket and HTTP transports
- Simple configuration via YAML or programmatic setup
- Comprehensive documentation and examples

## Documentation

Visit our [documentation](https://pymcpfy.readthedocs.io/) for:
- Detailed installation and setup instructions
- Framework-specific guides
- Configuration options
- API reference
- Examples and tutorials

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
