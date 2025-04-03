"""
Example Django views using PyMCPfy decorators.
"""
from django.contrib.auth.models import User
from django.http import JsonResponse

from pymcpfy.django import mcpfy_resource, mcpfy_tool, mcpfy_prompt

@mcpfy_resource(uri="/user/{user_id}")
def get_user(request, user_id: int):
    """Get user details by ID."""
    try:
        user = User.objects.get(id=user_id)
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

@mcpfy_tool()
def create_user(username: str, email: str, password: str) -> dict:
    """Create a new user.
    
    Args:
        username: The user's username
        email: The user's email address
        password: The user's password
    
    Returns:
        dict: The created user's details
    """
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
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
