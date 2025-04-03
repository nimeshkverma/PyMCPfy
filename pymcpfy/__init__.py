"""
PyMCPfy - A Python library to MCP-fy Web Framework APIs
"""

__version__ = "0.1.0"

from . import core
from . import django
from . import flask
from . import fastapi

__all__ = ["core", "django", "flask", "fastapi"]