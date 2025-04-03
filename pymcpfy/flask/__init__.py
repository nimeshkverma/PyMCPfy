"""
PyMCPfy Flask integration module.
"""
from functools import wraps
from typing import Any, Callable, Optional, Type, TypeVar

from flask import Flask, jsonify, request

from ..core import MCPfyBase

T = TypeVar("T", bound=Callable[..., Any])

class FlaskMCPfy:
    """Flask integration for PyMCPfy."""
    
    def __init__(self):
        self._mcp_base = MCPfyBase()
    
    def init_app(self, app: Flask) -> None:
        """Initialize Flask app with MCP integration.
        
        Args:
            app: Flask application instance
        """
        self._mcp_base.init_app(app)
        
        # Register MCP endpoints
        @app.route("/_mcp/health")
        def health_check():
            return jsonify({"status": "healthy"})

    def resource(self, *mcp_args, **mcp_kwargs) -> Callable[[T], T]:
        """Decorator to mark a Flask route as an MCP resource.
        
        This decorator should be placed AFTER the Flask route decorator.
        Example:
            @app.route("/user/<int:user_id>")
            @mcpfy_resource()
            def get_user(user_id: int):
                ...
        """
        def decorator(view_func: T) -> T:
            # First wrap with MCP resource
            mcp_wrapped = self._mcp_base.resource(*mcp_args, **mcp_kwargs)(view_func)
            
            @wraps(view_func)
            def wrapped_view(**view_kwargs):
                # Pass route parameters directly to the view function
                result = view_func(**view_kwargs)
                if isinstance(result, (dict, list)):
                    return jsonify(result)
                return result
            
            # Copy MCP metadata to the wrapped view
            for attr in dir(mcp_wrapped):
                if attr.startswith('_mcp_'):
                    setattr(wrapped_view, attr, getattr(mcp_wrapped, attr))
            
            # Preserve Flask route info
            wrapped_view.__name__ = view_func.__name__
            return wrapped_view
        return decorator

    def tool(self, *args, **kwargs) -> Callable[[T], T]:
        """Decorator to mark a function as an MCP tool."""
        def decorator(func: T) -> T:
            return self._mcp_base.tool(*args, **kwargs)(func)
        return decorator

    def prompt(self, *args, **kwargs) -> Callable[[T], T]:
        """Decorator to mark a function as an MCP prompt."""
        def decorator(func: T) -> T:
            return self._mcp_base.prompt(*args, **kwargs)(func)
        return decorator

# Create a singleton instance
_flask_mcpfy = FlaskMCPfy()

# Expose decorators at module level
mcpfy_resource = _flask_mcpfy.resource
mcpfy_tool = _flask_mcpfy.tool
mcpfy_prompt = _flask_mcpfy.prompt

# Expose the instance for advanced usage
flask_mcpfy = _flask_mcpfy

__all__ = [
    "FlaskMCPfy",
    "mcpfy_resource",
    "mcpfy_tool",
    "mcpfy_prompt",
    "flask_mcpfy",
]
