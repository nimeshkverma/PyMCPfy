"""
PyMCPfy Flask integration module.
"""
from functools import wraps
from typing import Any, Callable, Optional, Type, TypeVar

from flask import Flask, jsonify, request

from ..core import MCPfyBase

T = TypeVar("T", bound=Callable[..., Any])

class FlaskMCPfy(MCPfyBase):
    """Flask integration for PyMCPfy."""
    
    def init_app(self, app: Flask) -> None:
        """Initialize Flask app with MCP integration.
        
        Args:
            app: Flask application instance
        """
        super().init_app(app)
        
        # Register MCP endpoints
        @app.route("/_mcp/health")
        def health_check():
            return jsonify({"status": "healthy"})

    def resource(self, *args, **kwargs) -> Callable[[T], T]:
        """Decorator to mark a Flask route as an MCP resource."""
        def decorator(view_func: T) -> T:
            @wraps(view_func)
            def wrapped_view(*args, **kwargs):
                result = view_func(*args, **kwargs)
                if isinstance(result, (dict, list)):
                    return jsonify(result)
                return result
            return super().resource(*args, **kwargs)(wrapped_view)
        return decorator

flask_mcpfy = FlaskMCPfy()
mcpfy_resource = flask_mcpfy.resource
mcpfy_tool = flask_mcpfy.tool
mcpfy_prompt = flask_mcpfy.prompt
