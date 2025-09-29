"""
Galileo Future API

This package provides the next-generation object-centric API for Galileo.
It offers an intuitive, object-oriented interface that simplifies common workflows
while maintaining full compatibility with the existing service-based functions.

Key Features:
- Object-centric design for better usability
- Simplified project, log stream, and prompt management
- Backward-compatible with existing service functions
- Clean, intuitive method chaining and relationships
- Comprehensive logging and error handling
- Consistent naming conventions and method patterns

Logging:
    The SDK uses structured logging that integrates with your application's logging.
    For interactive use (REPL, IPython, Jupyter), enable console logging:

        from galileo.__future__ import enable_console_logging
        enable_console_logging()  # Shows INFO level and above

Example Usage:
    from galileo.__future__ import Project, Prompt, Message, MessageRole

    # Configure the SDK
    Configuration.set_galileo_api_key("your-api-key")
    Configuration.set_console_url("https://app.galileo.ai")
    Configuration.connect()  # Validate configuration

    # Create or get a project
    project = Project(name="My AI Project")
    project = Project.get(name="My AI Project")

    # List all projects
    projects = Project.list()

    # Create and manage log streams through the project
    log_stream = project.create_log_stream(name="Production Logs")
    log_streams = project.list_log_streams()

    # Access related objects
    project = log_stream.project  # Get the parent project

    # Create and manage prompts
    prompt = Prompt(
        name="ml-expert-v1",
        messages=[
            Message(role=MessageRole.system, content="You are an expert in ML."),
            Message(role=MessageRole.user, content="{{input}}"),
        ],
    )

    # List and manage prompts
    prompts = Prompt.list(name_filter="ml-expert")
    new_version = prompt.create_version()

    # Create and manage datasets
    dataset = Dataset(
        name="ml-knowledge-evaluation_3",
        content=[
            {"input": "What is machine learning?", "output": "Machine learning ..."},
            {"input": "How does deep learning work?", "output": "Deep learning uses ..."}
        ]
    )

Error Handling:
    All methods raise specific exceptions for different error conditions:

        from galileo.__future__ import ConfigurationError, ValidationError

        try:
            Configuration.connect()
        except ConfigurationError as e:
            # Handle configuration issues
            pass
        except ValidationError as e:
            # Handle validation errors
            pass
"""

from galileo.__future__.configuration import Configuration
from galileo.__future__.dataset import Dataset
from galileo.__future__.exceptions import (
    APIError,
    ConfigurationError,
    GalileoFutureError,
    ResourceConflictError,
    ResourceNotFoundError,
    ValidationError,
)
from galileo.__future__.log_stream import LogStream
from galileo.__future__.project import Project
from galileo.__future__.prompt import Prompt
from galileo.schema.message import Message
from galileo_core.schemas.logging.llm import MessageRole

__all__ = [
    "APIError",
    "Configuration",
    "ConfigurationError",
    "Dataset",
    "GalileoFutureError",
    "LogStream",
    "Message",
    "MessageRole",
    "Project",
    "Prompt",
    "ResourceConflictError",
    "ResourceNotFoundError",
    "ValidationError",
    "disable_console_logging",
    "enable_console_logging",
]
