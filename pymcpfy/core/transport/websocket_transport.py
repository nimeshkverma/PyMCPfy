"""WebSocket transport implementation for FastMCP."""

import asyncio
import json
from typing import Any, Dict, Optional
import websockets
from websockets.server import WebSocketServerProtocol
from fastmcp import FastMCP, Context

class WebSocketTransport:
    """WebSocket transport for FastMCP communication."""
    def __init__(
        self,
        mcp: FastMCP,
        host: str = "localhost",
        port: int = 8765,
        ping_interval: int = 20,
        ping_timeout: int = 20
    ):
        self.mcp = mcp
        self.host = host
        self.port = port
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self._server: Optional[websockets.WebSocketServer] = None

    async def start(self):
        """Start the WebSocket server."""
        self._server = await websockets.serve(
            self._handle_connection,
            self.host,
            self.port,
            ping_interval=self.ping_interval,
            ping_timeout=self.ping_timeout
        )
        print(f"FastMCP WebSocket server running at ws://{self.host}:{self.port}")

    async def stop(self):
        """Stop the WebSocket server."""
        if self._server:
            self._server.close()
            await self._server.wait_closed()

    async def _handle_connection(self, websocket: WebSocketServerProtocol, path: str):
        """Handle incoming WebSocket connections."""
        try:
            async for message in websocket:
                try:
                    request = json.loads(message)
                    response = await self._handle_request(request, websocket)
                    await websocket.send(json.dumps(response))
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        "error": "Invalid JSON",
                        "status": 400
                    }))
                except Exception as e:
                    await websocket.send(json.dumps({
                        "error": str(e),
                        "status": 500
                    }))
        except websockets.exceptions.ConnectionClosed:
            pass

    async def _handle_request(
        self,
        request: Dict[str, Any],
        websocket: WebSocketServerProtocol
    ) -> Dict[str, Any]:
        """Handle incoming MCP request."""
        request_type = request.get("type")
        if not request_type:
            return {"error": "Missing request type", "status": 400}

        try:
            if request_type == "resource":
                return await self._handle_resource_request(request, websocket)
            elif request_type == "tool":
                return await self._handle_tool_request(request, websocket)
            elif request_type == "prompt":
                return await self._handle_prompt_request(request, websocket)
            elif request_type == "schema":
                return await self._handle_schema_request(request, websocket)
            else:
                return {"error": f"Unknown request type: {request_type}", "status": 400}
        except Exception as e:
            return {"error": str(e), "status": 500}

    async def _handle_resource_request(
        self,
        request: Dict[str, Any],
        websocket: WebSocketServerProtocol
    ) -> Dict[str, Any]:
        """Handle resource request."""
        path = request.get("path")
        if not path:
            return {"error": "Missing resource path", "status": 400}

        try:
            result = await self.mcp.get_resource(path, request.get("parameters", {}))
            return {"data": result, "status": 200}
        except Exception as e:
            return {"error": str(e), "status": 500}

    async def _handle_tool_request(
        self,
        request: Dict[str, Any],
        websocket: WebSocketServerProtocol
    ) -> Dict[str, Any]:
        """Handle tool request."""
        name = request.get("name")
        if not name:
            return {"error": "Missing tool name", "status": 400}

        try:
            ctx = Context(
                request_id=request.get("request_id", ""),
                metadata=request.get("metadata", {}),
                transport="websocket"
            )
            result = await self.mcp.call_tool(
                name,
                ctx,
                request.get("parameters", {})
            )
            return {"data": result, "status": 200}
        except Exception as e:
            return {"error": str(e), "status": 500}

    async def _handle_prompt_request(
        self,
        request: Dict[str, Any],
        websocket: WebSocketServerProtocol
    ) -> Dict[str, Any]:
        """Handle prompt request."""
        name = request.get("name")
        if not name:
            return {"error": "Missing prompt name", "status": 400}

        try:
            result = await self.mcp.get_prompt(
                name,
                request.get("parameters", {})
            )
            return {"data": result, "status": 200}
        except Exception as e:
            return {"error": str(e), "status": 500}

    async def _handle_schema_request(
        self,
        request: Dict[str, Any],
        websocket: WebSocketServerProtocol
    ) -> Dict[str, Any]:
        """Handle schema request."""
        try:
            schema = self.mcp.get_schema()
            return {"data": schema, "status": 200}
        except Exception as e:
            return {"error": str(e), "status": 500}
