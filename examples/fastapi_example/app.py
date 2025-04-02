"""
Example FastAPI application using PyMCPfy decorators.
"""
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pymcpfy.fastapi import mcpfy_resource, mcpfy_tool, mcpfy_prompt

app = FastAPI()

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    username: str
    email: str

@app.get("/user/{user_id}")
@mcpfy_resource
async def get_user(user_id: int):
    """Get user details by ID."""
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

@mcpfy_tool
async def create_user(username: str, email: str) -> dict:
    """Create a new user.
    
    Args:
        username: The user's username
        email: The user's email address
    
    Returns:
        dict: The created user's details
    """
    db = SessionLocal()
    user = User(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

@mcpfy_prompt
async def generate_welcome_message(user_data: dict) -> str:
    """Generate a personalized welcome message for a user.
    
    Args:
        user_data: Dictionary containing user information
            - username: The user's username
            - email: The user's email
    
    Returns:
        str: A personalized welcome message
    """
    return f"Welcome {user_data['username']}! Your account has been created with email {user_data['email']}."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
