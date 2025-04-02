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

class DjangoMCPfy(MCPfyBase):
    """Django integration for PyMCPfy."""
    
    def init_app(self, app: AppConfig) -> None:
        """Initialize Django app with MCP integration.
        
        Args:
            app: Django AppConfig instance
        """
        super().init_app(app)
        # Add MCP middleware if not present
        if "pymcpfy.django.middleware.MCPfyMiddleware" not in settings.MIDDLEWARE:
            settings.MIDDLEWARE.append("pymcpfy.django.middleware.MCPfyMiddleware")

    def resource(self, *args, **kwargs) -> Callable[[T], T]:
        """Decorator to mark a Django view as an MCP resource."""
        def decorator(view_func: T) -> T:
            @wraps(view_func)
            def wrapped_view(request: HttpRequest, *args, **kwargs) -> JsonResponse:
                result = view_func(request, *args, **kwargs)
                if isinstance(result, (dict, list)):
                    return JsonResponse(result, safe=False)
                return result
            return super().resource(*args, **kwargs)(wrapped_view)
        return decorator

django_mcpfy = DjangoMCPfy()
mcpfy_resource = django_mcpfy.resource
mcpfy_tool = django_mcpfy.tool
mcpfy_prompt = django_mcpfy.prompt
