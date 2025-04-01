# Contributing to PyMCPfy

Thank you for your interest in contributing to PyMCPfy! This guide will help you get started with the development environment.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- virtualenv or venv (recommended)

### Setting Up the Development Environment

1. Clone the repository:
```bash
git clone https://github.com/nimeshkverma/pymcpfy.git
cd pymcpfy
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. Install development dependencies:
```bash
# Install all dependencies (including optional ones)
pip install -r requirements.txt

# For minimal installation (core only)
pip install -e ".[dev]"

# For specific framework support
pip install -e ".[django]"  # For Django
pip install -e ".[flask]"   # For Flask
pip install -e ".[fastapi]" # For FastAPI

# For all frameworks
pip install -e ".[all]"
```

## Development Workflow

1. Create a new branch for your feature/bugfix:
```bash
git checkout -b feature-name
```

2. Format your code:
```bash
# Format Python code
black .

# Sort imports
isort .
```

3. Run linting:
```bash
# Run flake8
flake8 .

# Run type checking
mypy .
```

4. Run tests:
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=pymcpfy

# Run specific test file
pytest tests/test_file.py
```

5. Build documentation:
```bash
cd docs
make html
```

## Project Structure

```
pymcpfy/
├── docs/              # Documentation
├── examples/          # Example applications
│   ├── django_example/
│   ├── flask_example/
│   └── fastapi_example/
├── pymcpfy/          # Main package
│   ├── core/         # Core functionality
│   ├── django/       # Django integration
│   ├── flask/        # Flask integration
│   └── fastapi/      # FastAPI integration
└── tests/            # Test suite
```

## Coding Standards

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all public functions/classes
- Include tests for new features
- Keep functions focused and modular
- Add comments for complex logic

## Pull Request Process

1. Update documentation for any new features
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md if applicable
5. Submit a pull request with a clear description of changes

## Getting Help

- Open an issue for bugs or feature requests
- Join our community discussions
- Check existing documentation and issues

## License

By contributing to PyMCPfy, you agree that your contributions will be licensed under its MIT license.
