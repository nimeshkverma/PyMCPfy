# PyMCPfy: MCP-fy Your Python Web APIs

[![PyPI version](https://badge.fury.io/py/pymcpfy.svg)](https://badge.fury.io/py/pymcpfy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/pymcpfy.svg)](https://pypi.org/project/pymcpfy/)

PyMCPfy is a Python library that enables developers to easily expose their existing web framework APIs (Django, Flask, and FastAPI) via the Model Context Protocol (MCP). It handles the complexities of MCP integration while providing a simple and consistent developer experience.

## Features

- 🔌 **Framework Agnostic Core**: Built on a solid foundation that works with any Python web framework
- 🎯 **Framework-Specific Integrations**: First-class support for Django, Flask, and FastAPI
- 🚀 **Easy Integration**: Simple decorators to expose existing APIs via MCP
- 📊 **Automatic Schema Generation**: Automatically generates MCP schemas from your Python types and docstrings
- 🔄 **Multiple Transport Protocols**: Support for WebSocket and HTTP transports
- ⚙️ **Flexible Configuration**: Configure via YAML, environment variables, or programmatically
- 🔒 **Security First**: Built-in support for authentication and authorization
- 📚 **Comprehensive Documentation**: Detailed guides and examples for all features
- **FastMCP Integration**: Built on FastMCP for robust MCP support
- **JWT Authentication**: Support for JSON Web Tokens
- **WebSocket Support**: Support for WebSocket transport protocol
- **Comprehensive Examples**: Examples for FastAPI, Flask, and Django

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

2. Create a configuration file (pymcpfy_config.yaml):

```yaml
transport:
  type: websocket  # or 'http'
  host: localhost
  port: 8765
backend_url: http://localhost:8000
debug: true
cors_origins:
  - http://localhost:3000
```

3. Expose your API endpoints via MCP:

```python
# Django example
from pymcpfy.django import mcpfy

@mcpfy()
def get_user(request, user_id: int):
    """Get user details by ID.
    
    :param user_id: The ID of the user to retrieve
    :return: User details including name and email
    """
    user = User.objects.get(id=user_id)
    return JsonResponse({"name": user.name, "email": user.email})

# Flask example
from pymcpfy.flask import mcpfy

@app.route("/user/<int:user_id>")
@mcpfy()
def get_user(user_id: int):
    """Get user details by ID."""
    user = User.query.get(user_id)
    return jsonify({"name": user.name, "email": user.email})

# FastAPI example
from pymcpfy.fastapi import mcpfy

@app.get("/user/{user_id}")
@mcpfy()
async def get_user(user_id: int):
    """Get user details by ID."""
    user = await User.get(id=user_id)
    return {"name": user.name, "email": user.email}
```

4. Start your MCP server:

```bash
# Django
python manage.py runmcp

# Flask/FastAPI
python app.py --mcp
```

## FastMCP Features Used

1. **Resources**: Expose static and dynamic data to LLMs
   ```python
   @mcp.resource("users://{user_id}/profile")
   def get_user_profile(user_id: str) -> dict:
       """Get user profile data."""
   ```

2. **Tools**: Define actions that LLMs can take
   ```python
   @mcp.tool()
   async def create_message(ctx: Context, content: str) -> dict:
       """Create a new message."""
   ```

3. **Prompts**: Provide helpful templates for LLMs
   ```python
   @mcp.prompt()
   def help_chat() -> str:
       """Help prompt for chat commands."""
   ```

4. **Context**: Log and track operations
   ```python
   ctx.log.info("Creating new message")
   ```

5. **Dependencies**: Specify required packages
   ```python
   mcp = FastMCP("API", dependencies=["fastapi", "sqlalchemy"])
   ```

## Documentation

Visit our [documentation](docs/index.md) for:

- [Getting Started Guide](docs/getting_started.md)
- Framework Integration Guides:
  - [Django Integration](docs/django_integration.md)
  - [Flask Integration](docs/flask_integration.md)
  - [FastAPI Integration](docs/fastapi_integration.md)
- [Configuration Guide](docs/configuration.md)
- [API Reference](docs/api_reference.md)
- [Examples](examples/)

## Examples

Find complete example applications in the [examples](examples/) directory:

- [Django Example](examples/django_example/): User management API with MCP integration
- [Flask Example](examples/flask_example/): Todo list API with MCP integration
- [FastAPI Example](examples/fastapi_example/): Real-time chat API with MCP integration

## Contributing

We welcome contributions! Here's how you can help:

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/nimeshkverma/pymcpfy.git
cd pymcpfy
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Run tests:
```bash
pytest tests/
```

### Development Guidelines

1. **Code Style**:
   - Follow PEP 8 guidelines
   - Use type hints
   - Write docstrings for all public functions/classes
   - Run `black` and `isort` before committing

2. **Testing**:
   - Write unit tests for new features
   - Ensure all tests pass before submitting PR
   - Maintain or improve code coverage

3. **Documentation**:
   - Update relevant documentation
   - Include docstrings with examples
   - Add new features to README if applicable

4. **Pull Requests**:
   - Create feature branches from `main`
   - Include tests and documentation
   - Keep changes focused and atomic
   - Follow the PR template

### Release Process

1. Update version in `setup.py` and `__init__.py`
2. Update CHANGELOG.md
3. Create release notes
4. Tag release in git
5. Build and upload to PyPI

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- Created and maintained by [Nimesh Kiran Verma](https://github.com/nimeshkverma)
- Built on the [Model Context Protocol](https://modelcontextprotocol.io)
- Inspired by the need for standardized AI-API interactions
