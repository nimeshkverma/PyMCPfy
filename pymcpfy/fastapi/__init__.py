"""
PyMCPfy FastAPI integration module.
"""
from functools import wraps
from typing import Any, Callable, Optional, Type, TypeVar

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from ..core import MCPfyBase

T = TypeVar("T", bound=Callable[..., Any])

class FastAPIMCPfy:
    """FastAPI integration for PyMCPfy."""
    
    def __init__(self):
        self._mcp_base = MCPfyBase()
    """FastAPI integration for PyMCPfy."""
    
    def init_app(self, app: FastAPI) -> None:
        """Initialize FastAPI app with MCP integration.
        
        Args:
            app: FastAPI application instance
        """
        self._mcp_base.init_app(app)
        
        # Register MCP endpoints
        @app.get("/_mcp/health")
        async def health_check():
            return {"status": "healthy"}

    def resource(self, *args, **kwargs) -> Callable[[T], T]:
        """Decorator to mark a FastAPI route as an MCP resource."""
        def decorator(route_func: T) -> T:
            # First wrap with MCP resource
            mcp_wrapped = self._mcp_base.resource(*args, **kwargs)(route_func)
            
            @wraps(route_func)
            async def wrapped_route(*route_args, **route_kwargs):
                # Pass route parameters to the route function
                result = await route_func(*route_args, **route_kwargs)
                if isinstance(result, (dict, list)):
                    return JSONResponse(content=result)
                return result
            
            # Preserve FastAPI route info
            wrapped_route.__signature__ = route_func.__signature__
            
            # Copy MCP metadata to the wrapped route
            for attr in dir(mcp_wrapped):
                if attr.startswith('_mcp_'):
                    setattr(wrapped_route, attr, getattr(mcp_wrapped, attr))
            
            return wrapped_route
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
_fastapi_mcpfy = FastAPIMCPfy()

# Expose decorators at module level
mcpfy_resource = _fastapi_mcpfy.resource
mcpfy_tool = _fastapi_mcpfy.tool
mcpfy_prompt = _fastapi_mcpfy.prompt

# Expose the instance for advanced usage
fastapi_mcpfy = _fastapi_mcpfy

__all__ = [
    "FastAPIMCPfy",
    "mcpfy_resource",
    "mcpfy_tool",
    "mcpfy_prompt",
    "fastapi_mcpfy",
]
