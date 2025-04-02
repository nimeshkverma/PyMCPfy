# Contributing to PyMCPfy

We love your input! We want to make contributing to PyMCPfy as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Setting Up Your Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pymcpfy.git
   cd pymcpfy
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Running Tests

We use pytest for our test suite. To run tests:

```bash
pytest
```

For coverage report:

```bash
pytest --cov=pymcpfy
```

## Code Style

We use several tools to maintain code quality:

- Black for code formatting
- isort for import sorting
- Flake8 for style guide enforcement
- MyPy for type checking

You can run all style checks with:

```bash
black .
isort .
flake8
mypy pymcpfy
```

## Documentation

We use Markdown for documentation. Please update the relevant documentation when you make changes:

- Update README.md if you change user-facing functionality
- Update docstrings for any modified functions/classes
- Add examples for new features

## Pull Request Process

1. Update the README.md with details of changes to the interface
2. Update the docs/ with any necessary changes
3. The PR may be merged once you have the sign-off of at least one other developer

## Any contributions you make will be under the Apache License 2.0

In short, when you submit code changes, your submissions are understood to be under the same [Apache License 2.0](http://choosealicense.com/licenses/apache-2.0/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker]

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yourusername/pymcpfy/issues/new).

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## License

By contributing, you agree that your contributions will be licensed under its Apache License 2.0.
