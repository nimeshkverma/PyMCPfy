"""Core FastMCP integration for PyMCPfy."""

from typing import Any, Callable, Dict, List, Optional, Type, Union
from fastmcp import FastMCP, Context, Image
from pydantic import BaseModel, Field

class MCPResource:
    """Wrapper for resources exposed via FastMCP."""
    def __init__(
        self,
        func: Callable,
        path: str,
        description: Optional[str] = None,
        return_type: Optional[Type] = None,
        is_async: bool = False
    ):
        self.func = func
        self.path = path
        self.description = description or func.__doc__ or ""
        self.return_type = return_type
        self.is_async = is_async

    async def __call__(self, *args, **kwargs) -> Any:
        """Call the resource function."""
        if self.is_async:
            return await self.func(*args, **kwargs)
        return self.func(*args, **kwargs)

class MCPTool:
    """Wrapper for tools exposed via FastMCP."""
    def __init__(
        self,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
        parameter_types: Optional[Dict[str, Type]] = None,
        return_type: Optional[Type] = None,
        is_async: bool = False
    ):
        self.func = func
        self.name = name or func.__name__
        self.description = description or func.__doc__ or ""
        self.parameter_types = parameter_types
        self.return_type = return_type
        self.is_async = is_async

    async def __call__(self, ctx: Context, *args, **kwargs) -> Any:
        """Call the tool function with context."""
        if self.is_async:
            return await self.func(ctx, *args, **kwargs)
        return self.func(ctx, *args, **kwargs)

class MCPPrompt:
    """Wrapper for prompts exposed via FastMCP."""
    def __init__(
        self,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None
    ):
        self.func = func
        self.name = name or func.__name__
        self.description = description or func.__doc__ or ""

    def __call__(self, *args, **kwargs) -> str:
        """Call the prompt function."""
        return self.func(*args, **kwargs)

class MCPRegistry:
    """Registry for FastMCP components."""
    def __init__(self, app_name: str, dependencies: Optional[List[str]] = None):
        self.mcp = FastMCP(app_name, dependencies=dependencies)
        self.resources: Dict[str, MCPResource] = {}
        self.tools: Dict[str, MCPTool] = {}
        self.prompts: Dict[str, MCPPrompt] = {}

    def resource(self, path: str, **kwargs):
        """Decorator to register a resource."""
        def decorator(func):
            resource = MCPResource(func, path, **kwargs)
            self.resources[path] = resource
            self.mcp.resource(path)(func)
            return resource
        return decorator

    def tool(self, **kwargs):
        """Decorator to register a tool."""
        def decorator(func):
            tool = MCPTool(func, **kwargs)
            self.tools[tool.name] = tool
            self.mcp.tool()(func)
            return tool
        return decorator

    def prompt(self, **kwargs):
        """Decorator to register a prompt."""
        def decorator(func):
            prompt = MCPPrompt(func, **kwargs)
            self.prompts[prompt.name] = prompt
            self.mcp.prompt()(func)
            return prompt
        return decorator

    def get_resource(self, path: str) -> Optional[MCPResource]:
        """Get a registered resource by path."""
        return self.resources.get(path)

    def get_tool(self, name: str) -> Optional[MCPTool]:
        """Get a registered tool by name."""
        return self.tools.get(name)

    def get_prompt(self, name: str) -> Optional[MCPPrompt]:
        """Get a registered prompt by name."""
        return self.prompts.get(name)

    def get_schema(self) -> Dict[str, Any]:
        """Get schema for all registered components."""
        return {
            "resources": {
                path: {
                    "description": resource.description,
                    "return_type": str(resource.return_type),
                    "is_async": resource.is_async
                }
                for path, resource in self.resources.items()
            },
            "tools": {
                tool.name: {
                    "description": tool.description,
                    "parameters": tool.parameter_types,
                    "return_type": str(tool.return_type),
                    "is_async": tool.is_async
                }
                for tool in self.tools.values()
            },
            "prompts": {
                prompt.name: {
                    "description": prompt.description
                }
                for prompt in self.prompts.values()
            }
        }
