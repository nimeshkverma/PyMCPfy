"""
PyMCPfy Django integration module.
"""
from functools import wraps
from typing import Any, Callable, Optional, Type, TypeVar

from django.apps import AppConfig
from django.conf import settings
from django.http import HttpRequest, JsonResponse

from ..core import MCPfyBase

T = TypeVar("T", bound=Callable[..., Any])

class DjangoMCPfy:
    """Django integration for PyMCPfy."""
    
    def __init__(self):
        self._mcp_base = MCPfyBase()
    """Django integration for PyMCPfy."""
    
    def init_app(self, app: AppConfig) -> None:
        """Initialize Django app with MCP integration.
        
        Args:
            app: Django AppConfig instance
        """
        self._mcp_base.init_app(app)
        # Add MCP middleware if not present
        if "pymcpfy.django.middleware.MCPfyMiddleware" not in settings.MIDDLEWARE:
            settings.MIDDLEWARE.append("pymcpfy.django.middleware.MCPfyMiddleware")

    def resource(self, *args, **kwargs) -> Callable[[T], T]:
        """Decorator to mark a Django view as an MCP resource."""
        def decorator(view_func: T) -> T:
            # First wrap with MCP resource
            mcp_args = args
            mcp_kwargs = kwargs
            mcp_wrapped = self._mcp_base.resource(*mcp_args, **mcp_kwargs)(view_func)
            
            @wraps(view_func)
            def wrapped_view(request: HttpRequest, *view_args, **view_kwargs) -> JsonResponse:
                # Pass route parameters to the view function
                result = view_func(request, *view_args, **view_kwargs)
                if isinstance(result, (dict, list)):
                    return JsonResponse(result, safe=False)
                return result
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
_django_mcpfy = DjangoMCPfy()

# Expose decorators at module level
mcpfy_resource = _django_mcpfy.resource
mcpfy_tool = _django_mcpfy.tool
mcpfy_prompt = _django_mcpfy.prompt

# Expose the instance for advanced usage
django_mcpfy = _django_mcpfy

__all__ = [
    "DjangoMCPfy",
    "mcpfy_resource",
    "mcpfy_tool",
    "mcpfy_prompt",
    "django_mcpfy",
]
