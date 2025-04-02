"""
PyMCPfy core module providing base functionality for MCP integration.
"""
from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union

from mcp.server.fastmcp import Context, FastMCP

T = TypeVar("T", bound=Callable[..., Any])

class MCPfyBase:
    """Base class for PyMCPfy framework integrations."""
    
    def __init__(self, app: Any = None, **kwargs):
        """Initialize MCPfyBase.
        
        Args:
            app: The framework application instance
            **kwargs: Additional configuration options
        """
        self.app = app
        self.mcp_server = FastMCP(**kwargs)
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app: Any) -> None:
        """Initialize the framework application with MCP integration.
        
        Args:
            app: The framework application instance
        """
        self.app = app
        # Framework-specific initialization will be implemented by subclasses
        
    def resource(self, *args, **kwargs) -> Callable[[T], T]:
        """Decorator to mark a function as an MCP resource."""
        def decorator(func: T) -> T:
            return self.mcp_server.resource(*args, **kwargs)(func)
        return decorator
    
    def tool(self, *args, **kwargs) -> Callable[[T], T]:
        """Decorator to mark a function as an MCP tool."""
        def decorator(func: T) -> T:
            return self.mcp_server.tool(*args, **kwargs)(func)
        return decorator
    
    def prompt(self, *args, **kwargs) -> Callable[[T], T]:
        """Decorator to mark a function as an MCP prompt."""
        def decorator(func: T) -> T:
            return self.mcp_server.prompt(*args, **kwargs)(func)
        return decorator
