"""Schema generator for FastMCP components."""

import inspect
from typing import Any, Callable, Dict, List, Optional, Type, get_type_hints
from pydantic import BaseModel, Field

class SchemaGenerator:
    """Generate FastMCP schema from Python functions."""

    @staticmethod
    def generate_resource_schema(func: Callable, path: str) -> Dict[str, Any]:
        """Generate schema for a resource."""
        type_hints = get_type_hints(func)
        return_type = type_hints.get("return", Any)

        schema = {
            "path": path,
            "description": func.__doc__ or "",
            "parameters": SchemaGenerator._get_path_parameters(path),
            "return_type": SchemaGenerator._get_type_schema(return_type),
            "is_async": inspect.iscoroutinefunction(func)
        }

        # Add parameter descriptions from docstring
        if func.__doc__:
            for param_name in schema["parameters"]:
                param_desc = SchemaGenerator._extract_param_description(func.__doc__, param_name)
                if param_desc:
                    schema["parameters"][param_name]["description"] = param_desc

        return schema

    @staticmethod
    def generate_tool_schema(func: Callable) -> Dict[str, Any]:
        """Generate schema for a tool."""
        signature = inspect.signature(func)
        type_hints = get_type_hints(func)

        # Skip context parameter
        params = {
            name: param
            for name, param in signature.parameters.items()
            if name != "ctx"
        }

        schema = {
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": {},
            "return_type": SchemaGenerator._get_type_schema(type_hints.get("return", Any)),
            "is_async": inspect.iscoroutinefunction(func)
        }

        # Process parameters
        for name, param in params.items():
            param_type = type_hints.get(name, Any)
            schema["parameters"][name] = SchemaGenerator._get_type_schema(param_type)

            # Add default value if present
            if param.default is not param.empty:
                schema["parameters"][name]["default"] = param.default

            # Add description from docstring
            if func.__doc__:
                param_desc = SchemaGenerator._extract_param_description(func.__doc__, name)
                if param_desc:
                    schema["parameters"][name]["description"] = param_desc

        return schema

    @staticmethod
    def generate_prompt_schema(func: Callable) -> Dict[str, Any]:
        """Generate schema for a prompt."""
        return {
            "name": func.__name__,
            "description": func.__doc__ or "",
            "return_type": {"type": "string"}
        }

    @staticmethod
    def _get_path_parameters(path: str) -> Dict[str, Dict[str, Any]]:
        """Extract parameters from a resource path."""
        params = {}
        parts = path.split("/")
        for part in parts:
            if part.startswith("{") and part.endswith("}"):
                param_name = part[1:-1]
                params[param_name] = {
                    "type": "string",
                    "description": f"Path parameter: {param_name}"
                }
        return params

    @staticmethod
    def _get_type_schema(type_hint: Type) -> Dict[str, Any]:
        """Convert Python type hint to FastMCP type schema."""
        if hasattr(type_hint, "__origin__"):  # Handle generic types
            origin = type_hint.__origin__
            if origin in (list, List):
                return {
                    "type": "array",
                    "items": SchemaGenerator._get_type_schema(type_hint.__args__[0])
                }
            elif origin in (dict, Dict):
                key_type = type_hint.__args__[0]
                value_type = type_hint.__args__[1]
                return {
                    "type": "object",
                    "additionalProperties": SchemaGenerator._get_type_schema(value_type)
                }
            elif origin == Optional:
                return {**SchemaGenerator._get_type_schema(type_hint.__args__[0]), "optional": True}
        elif issubclass(type_hint, BaseModel):
            return {
                "type": "object",
                "properties": {
                    field_name: SchemaGenerator._get_type_schema(field.annotation)
                    for field_name, field in type_hint.__fields__.items()
                }
            }
        elif type_hint == str:
            return {"type": "string"}
        elif type_hint == int:
            return {"type": "integer"}
        elif type_hint == float:
            return {"type": "number"}
        elif type_hint == bool:
            return {"type": "boolean"}
        elif type_hint == Any:
            return {"type": "any"}
        else:
            return {"type": "string", "format": type_hint.__name__}

    @staticmethod
    def _extract_param_description(docstring: str, param_name: str) -> Optional[str]:
        """Extract parameter description from docstring."""
        lines = docstring.split("\n")
        for i, line in enumerate(lines):
            if f":param {param_name}:" in line:
                return line.split(f":param {param_name}:")[1].strip()
        return None
