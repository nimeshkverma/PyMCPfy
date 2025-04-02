"""
PyMCPfy FastAPI integration module.
"""
from functools import wraps
from typing import Any, Callable, Optional, Type, TypeVar

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from ..core import MCPfyBase

T = TypeVar("T", bound=Callable[..., Any])

class FastAPIMCPfy(MCPfyBase):
    """FastAPI integration for PyMCPfy."""
    
    def init_app(self, app: FastAPI) -> None:
        """Initialize FastAPI app with MCP integration.
        
        Args:
            app: FastAPI application instance
        """
        super().init_app(app)
        
        # Register MCP endpoints
        @app.get("/_mcp/health")
        async def health_check():
            return {"status": "healthy"}

    def resource(self, *args, **kwargs) -> Callable[[T], T]:
        """Decorator to mark a FastAPI route as an MCP resource."""
        def decorator(route_func: T) -> T:
            @wraps(route_func)
            async def wrapped_route(*args, **kwargs):
                result = await route_func(*args, **kwargs)
                if isinstance(result, (dict, list)):
                    return JSONResponse(content=result)
                return result
            return super().resource(*args, **kwargs)(wrapped_route)
        return decorator

fastapi_mcpfy = FastAPIMCPfy()
mcpfy_resource = fastapi_mcpfy.resource
mcpfy_tool = fastapi_mcpfy.tool
mcpfy_prompt = fastapi_mcpfy.prompt
