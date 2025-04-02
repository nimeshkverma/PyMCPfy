"""
Example Flask application using PyMCPfy decorators.
"""
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from pymcpfy.flask import mcpfy_resource, mcpfy_tool, mcpfy_prompt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route("/user/<int:user_id>")
@mcpfy_resource
def get_user(user_id: int):
    """Get user details by ID."""
    user = User.query.get_or_404(user_id)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

@mcpfy_tool
def create_user(username: str, email: str) -> dict:
    """Create a new user.
    
    Args:
        username: The user's username
        email: The user's email address
    
    Returns:
        dict: The created user's details
    """
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

@mcpfy_prompt
def generate_welcome_message(user_data: dict) -> str:
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
    db.create_all()
    app.run(debug=True)
