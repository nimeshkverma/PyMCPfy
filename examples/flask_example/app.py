"""
Flask Example: Todo List API with FastMCP Integration
"""

from datetime import datetime
from typing import List, Optional
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from dataclasses import dataclass
from fastmcp import FastMCP, Context
from pydantic import BaseModel

# Initialize Flask and FastMCP apps
app = Flask(__name__)
mcp = FastMCP("Todo API", dependencies=["flask", "flask-sqlalchemy", "flask-jwt-extended"])

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change in production

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models
@dataclass
class User(db.Model):
    id: int
    username: str
    email: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)

@dataclass
class Todo(db.Model):
    id: int
    title: str
    description: str
    done: bool
    due_date: datetime
    created_at: datetime

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    done = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Resources
@mcp.resource("schema://todos")
def get_todo_schema() -> str:
    """Get the database schema for todos."""
    return """
    Todo:
        id: integer (primary key)
        title: string (required)
        description: text (optional)
        done: boolean (default: false)
        due_date: datetime (optional)
        created_at: datetime (auto)
        user_id: integer (foreign key)
    """

@mcp.resource("users://{user_id}/todos")
def get_user_todos(user_id: int) -> List[dict]:
    """Get todos for a specific user.
    
    :param user_id: User ID to lookup
    :return: List of todos
    """
    todos = Todo.query.filter_by(user_id=user_id).all()
    return [todo.__dict__ for todo in todos]

# Tools
@mcp.tool()
def login(ctx: Context, username: str, password: str) -> dict:
    """Login to get access token.
    
    :param username: User's username
    :param password: User's password
    :return: Access token
    """
    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:  # Use proper password hashing in production
        ctx.log.error(f"Failed login attempt for user {username}")
        return {"error": "Invalid credentials"}, 401
    
    ctx.log.info(f"Successful login for user {username}")
    access_token = create_access_token(identity=username)
    return {"access_token": access_token}

@mcp.tool()
def get_todos(ctx: Context, token: str) -> List[dict]:
    """Get all todos for the current user.
    
    :param token: JWT token
    :return: List of todos
    """
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        ctx.log.info(f"Fetching todos for user {username}")
        return [todo.__dict__ for todo in user.todos]
    except Exception as e:
        ctx.log.error(f"Error fetching todos: {str(e)}")
        return {"error": str(e)}, 401

@mcp.tool()
def create_todo(
    ctx: Context,
    token: str,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None
) -> dict:
    """Create a new todo.
    
    :param token: JWT token
    :param title: Todo title
    :param description: Todo description (optional)
    :param due_date: Due date (optional, format: YYYY-MM-DD)
    :return: Created todo
    """
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        
        todo = Todo(
            title=title,
            description=description,
            due_date=datetime.fromisoformat(due_date) if due_date else None,
            user_id=user.id
        )
        
        db.session.add(todo)
        db.session.commit()
        
        ctx.log.info(f"Created new todo '{title}' for user {username}")
        return todo.__dict__
    except Exception as e:
        ctx.log.error(f"Error creating todo: {str(e)}")
        return {"error": str(e)}, 400

@mcp.tool()
def update_todo(
    ctx: Context,
    token: str,
    todo_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    done: Optional[bool] = None,
    due_date: Optional[str] = None
) -> dict:
    """Update a todo.
    
    :param token: JWT token
    :param todo_id: ID of the todo to update
    :param title: New title (optional)
    :param description: New description (optional)
    :param done: New done status (optional)
    :param due_date: New due date (optional, format: YYYY-MM-DD)
    :return: Updated todo
    """
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()
        
        if not todo:
            return {"error": "Todo not found"}, 404
        
        if title:
            todo.title = title
        if description:
            todo.description = description
        if done is not None:
            todo.done = done
        if due_date:
            todo.due_date = datetime.fromisoformat(due_date)
        
        db.session.commit()
        ctx.log.info(f"Updated todo {todo_id} for user {username}")
        return todo.__dict__
    except Exception as e:
        ctx.log.error(f"Error updating todo: {str(e)}")
        return {"error": str(e)}, 400

@mcp.tool()
def delete_todo(ctx: Context, token: str, todo_id: int) -> dict:
    """Delete a todo.
    
    :param token: JWT token
    :param todo_id: ID of the todo to delete
    :return: Success message
    """
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()
        
        if not todo:
            return {"error": "Todo not found"}, 404
        
        db.session.delete(todo)
        db.session.commit()
        
        ctx.log.info(f"Deleted todo {todo_id} for user {username}")
        return {"message": "Todo deleted"}
    except Exception as e:
        ctx.log.error(f"Error deleting todo: {str(e)}")
        return {"error": str(e)}, 400

# Prompts
@mcp.prompt()
def help_todos() -> str:
    """Help prompt for todo commands."""
    return """
    Available commands:
    1. Login: Use the login tool with your username and password
    2. Get Todos: Use get_todos tool to view your todos
    3. Create Todo: Use create_todo tool to create a new todo
    4. Update Todo: Use update_todo tool to modify a todo
    5. Delete Todo: Use delete_todo tool to remove a todo
    6. View Schema: Check schema://todos resource
    7. View User's Todos: Check users://{user_id}/todos resource
    """

@mcp.prompt()
def todo_guidelines() -> str:
    """Guidelines for creating todos."""
    return """
    When creating or updating a todo:
    1. Title should be clear and concise
    2. Description should provide necessary details
    3. Due dates should be in YYYY-MM-DD format
    4. Mark todos as done when completed
    """

# Create database tables
with app.app_context():
    db.create_all()
    
    # Create demo user if not exists
    if not User.query.filter_by(username="demo").first():
        demo_user = User(
            username="demo",
            email="demo@example.com",
            password="demo123"  # Use proper password hashing in production
        )
        db.session.add(demo_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
