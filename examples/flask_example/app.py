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
@mcpfy_resource(uri="/user/{user_id}")
def get_user(user_id: int):
    """Get user details by ID."""
    user = User.query.get_or_404(user_id)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }

@mcpfy_tool()
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

@mcpfy_prompt()
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

def create_mcp_server():
    """Create MCP server for testing with MCP Inspector."""
    from mcp.server.fastmcp import FastMCP
    
    # Create MCP server with a descriptive name
    mcp = FastMCP(
        "Flask Example",
        description="Example Flask application using PyMCPfy decorators",
        dependencies=["flask", "flask-sqlalchemy"]
    )
    
    # Register MCP resources, tools, and prompts
    mcp.resource(uri="/user/{user_id}", name="get_user")(get_user)
    mcp.tool(name="create_user")(create_user)
    mcp.prompt(name="generate_welcome_message")(generate_welcome_message)
    
    return mcp

if __name__ == "__main__":
    import sys
    
    # Initialize database
    db.create_all()
    
    # Check if we should run in MCP Inspector mode
    if len(sys.argv) > 1 and sys.argv[1] == "--mcp":
        # Create and run MCP server
        mcp = create_mcp_server()
        mcp.run()
    else:
        # Run regular Flask server
        app.run(debug=True)
