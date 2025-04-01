"""
FastAPI Example: Real-time Chat API with FastMCP Integration
"""

from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastmcp import FastMCP, Context, Image
import jwt
import uvicorn

# Initialize FastAPI and FastMCP apps
app = FastAPI(title="Chat API")
mcp = FastMCP("Chat API", dependencies=["fastapi", "python-jose[cryptography]"])

# Security
SECRET_KEY = "your-secret-key"  # In production, use environment variable
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In-memory storage (use a proper database in production)
messages = []
active_connections: List[WebSocket] = []
users = {
    "demo": {
        "username": "demo",
        "password": "demo123",  # In production, use hashed passwords
        "full_name": "Demo User"
    }
}

# Models
class Message(BaseModel):
    id: int
    content: str
    sender: str
    timestamp: datetime

class User(BaseModel):
    username: str
    full_name: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Resources
@mcp.resource("users://{username}/profile")
def get_user_profile(username: str) -> dict:
    """Get a user's profile data.
    
    :param username: Username to lookup
    :return: User profile data
    """
    user = users.get(username)
    if not user:
        return {"error": "User not found"}
    return {
        "username": user["username"],
        "full_name": user["full_name"]
    }

@mcp.resource("users://active")
def get_active_users() -> List[str]:
    """Get list of currently active users.
    
    :return: List of usernames
    """
    return [conn.username for conn in active_connections if hasattr(conn, 'username')]

# Tools
@mcp.tool()
async def login(ctx: Context, username: str, password: str) -> dict:
    """Login to get access token.
    
    :param username: User's username
    :param password: User's password
    :return: Access token and type
    """
    user = users.get(username)
    if not user or password != user["password"]:
        ctx.log.error(f"Failed login attempt for user {username}")
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    ctx.log.info(f"Successful login for user {username}")
    token = jwt.encode(
        {"sub": username},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": token, "token_type": "bearer"}

@mcp.tool()
async def get_messages(ctx: Context, limit: Optional[int] = 50) -> List[Message]:
    """Get chat messages.
    
    :param limit: Maximum number of messages to return
    :return: List of messages
    """
    ctx.log.info(f"Fetching {limit} messages")
    return messages[-limit:]

@mcp.tool()
async def create_message(ctx: Context, content: str, token: str) -> Message:
    """Create a new message.
    
    :param content: Message content
    :param token: JWT token
    :return: Created message
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username or username not in users:
            raise HTTPException(status_code=401)
    except jwt.JWTError:
        raise HTTPException(status_code=401)

    message = Message(
        id=len(messages),
        content=content,
        sender=username,
        timestamp=datetime.now()
    )
    messages.append(message)
    
    ctx.log.info(f"New message from {username}: {content}")
    
    # Broadcast to WebSocket clients
    await manager.broadcast(
        f"{username}: {content}"
    )
    
    return message

# Prompts
@mcp.prompt()
def help_chat() -> str:
    """Help prompt for chat commands."""
    return """
    Available commands:
    1. Login: Use the login tool with your username and password
    2. Get Messages: Use get_messages tool to view chat history
    3. Send Message: Use create_message tool to send a new message
    4. View Active Users: Check users://active resource
    5. View User Profile: Check users://{username}/profile resource
    """

@mcp.prompt()
def message_guidelines() -> str:
    """Guidelines for creating messages."""
    return """
    When creating a message, please follow these guidelines:
    1. Keep messages concise and clear
    2. Be respectful to other users
    3. Don't share sensitive information
    4. Use appropriate language
    """

# WebSocket Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# API Endpoints
@app.post("/token")
@mcp.tool()
async def login_endpoint(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """Login to get access token.
    
    :param form_data: Username and password
    :return: Access token and type
    """
    return await login(None, form_data.username, form_data.password)

@app.get("/messages")
@mcp.tool()
async def get_messages_endpoint(limit: Optional[int] = 50) -> List[Message]:
    """Get chat messages.
    
    :param limit: Maximum number of messages to return
    :return: List of messages
    """
    return await get_messages(None, limit)

@app.post("/messages")
@mcp.tool()
async def create_message_endpoint(content: str, token: str) -> Message:
    """Create a new message.
    
    :param content: Message content
    :param token: JWT token
    :return: Created message
    """
    return await create_message(None, content, token)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(
                f"Message: {data}"
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("Client disconnected")

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
