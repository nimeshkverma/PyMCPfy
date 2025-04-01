"""User views."""

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from fastmcp import FastMCP, Context
from .serializers import UserSerializer

# Initialize FastMCP
mcp = FastMCP("User API")

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """Allow unauthenticated access to register."""
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    @mcp.tool()
    def create(self, request: object, ctx: Context):
        """
        Create a new user with profile.
        
        :param username: Username for the new user
        :param email: Email address
        :param password: Password
        :param first_name: First name (optional)
        :param last_name: Last name (optional)
        :param profile: Profile data (optional)
            - bio: User bio
            - location: User location
            - birth_date: Birth date (YYYY-MM-DD)
            - avatar: Avatar URL
        :return: Created user data
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        ctx.log.info(f"Created new user: {user.username}")
        return Response(self.get_serializer(user).data)

    @mcp.tool()
    def list(self, request: object, ctx: Context):
        """
        List all users.
        
        :return: List of users
        """
        ctx.log.info("Listing all users")
        return super().list(request)

    @mcp.tool()
    def retrieve(self, request: object, ctx: Context, pk: int = None):
        """
        Get a specific user by ID.
        
        :param pk: User ID
        :return: User data
        """
        ctx.log.info(f"Retrieving user {pk}")
        return super().retrieve(request, pk=pk)

    @mcp.tool()
    def update(self, request: object, ctx: Context, pk: int = None):
        """
        Update a user.
        
        :param pk: User ID
        :param username: New username (optional)
        :param email: New email (optional)
        :param password: New password (optional)
        :param first_name: New first name (optional)
        :param last_name: New last name (optional)
        :param profile: Profile data (optional)
            - bio: User bio
            - location: User location
            - birth_date: Birth date (YYYY-MM-DD)
            - avatar: Avatar URL
        :return: Updated user data
        """
        ctx.log.info(f"Updating user {pk}")
        return super().update(request, pk=pk)

    @mcp.tool()
    def destroy(self, request: object, ctx: Context, pk: int = None):
        """
        Delete a user.
        
        :param pk: User ID to delete
        :return: Success message
        """
        ctx.log.info(f"Deleting user {pk}")
        return super().destroy(request, pk=pk)

    @action(detail=True, methods=['get'])
    @mcp.tool()
    def profile(self, request: object, ctx: Context, pk: int = None):
        """
        Get user's profile.
        
        :param pk: User ID
        :return: User profile data
        """
        user = self.get_object()
        ctx.log.info(f"Retrieving profile for user {user.username}")
        serializer = self.get_serializer(user)
        return Response(serializer.data.get('profile', {}))
