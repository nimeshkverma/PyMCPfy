"""
Django management command to run the server with MCP Inspector support.
"""
from django.core.management.base import BaseCommand
from django.core.management.commands.runserver import Command as RunserverCommand

from mcp.server.fastmcp import FastMCP
from ...views import get_user, create_user, generate_welcome_message

class Command(RunserverCommand):
    help = "Run the development server with MCP Inspector support"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--mcp",
            action="store_true",
            help="Run with MCP Inspector",
        )

    def handle(self, *args, **options):
        if options.get("mcp"):
            # Create MCP server
            mcp = FastMCP(
                "Django Example",
                description="Example Django application using PyMCPfy decorators",
                dependencies=["django"]
            )

            # Register MCP resources, tools, and prompts
            mcp.resource(uri="/user/{user_id}", name="get_user")(get_user)
            mcp.tool(name="create_user")(create_user)
            mcp.prompt(name="generate_welcome_message")(generate_welcome_message)

            # Run MCP server
            mcp.run()
        else:
            # Run regular Django server
            super().handle(*args, **options)
