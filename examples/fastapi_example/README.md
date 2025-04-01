# FastAPI Chat Example

This example demonstrates how to build a real-time chat application using FastAPI and FastMCP.

## Features

- Real-time chat using WebSocket
- JWT authentication
- FastMCP integration for MCP functionality
- Resource definitions for user profiles
- Tool definitions for chat operations
- Helpful prompts for chat commands

## Installation

```bash
pip install -r requirements.txt
```

## Running the Example

```bash
python app.py
```

## FastMCP Usage

### Resources

```python
@mcp.resource("users://{username}/profile")
def get_user_profile(username: str) -> dict:
    """Get a user's profile data."""
    return {
        "username": user["username"],
        "full_name": user["full_name"]
    }
```

### Tools

```python
@mcp.tool()
async def create_message(ctx: Context, content: str, token: str) -> Message:
    """Create a new message."""
    message = Message(
        id=len(messages),
        content=content,
        sender=username,
        timestamp=datetime.now()
    )
    ctx.log.info(f"New message from {username}: {content}")
    return message
```

### Prompts

```python
@mcp.prompt()
def help_chat() -> str:
    """Help prompt for chat commands."""
    return """
    Available commands:
    1. Login: Use the login tool
    2. Get Messages: Use get_messages tool
    3. Send Message: Use create_message tool
    4. View Active Users: Check users://active
    5. View User Profile: Check users://{username}/profile
    """
```

## API Endpoints

- `POST /token`: Get JWT token
- `GET /messages`: Get chat messages
- `POST /messages`: Create new message
- `WebSocket /ws`: Real-time chat connection

## Testing

1. Get a token:
```bash
curl -X POST http://localhost:8000/token -d '{"username":"user1","password":"pass1"}'
```

2. Get messages:
```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/messages
```

3. Create message:
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" http://localhost:8000/messages -d '{"content":"Hello!"}'
```

## WebSocket Chat

Connect to the WebSocket endpoint for real-time chat:

```python
import websockets
import asyncio

async def chat():
    async with websockets.connect("ws://localhost:8000/ws") as ws:
        # Send message
        await ws.send("Hello, everyone!")
        
        # Receive messages
        while True:
            message = await ws.recv()
            print(f"Received: {message}")

asyncio.run(chat())
