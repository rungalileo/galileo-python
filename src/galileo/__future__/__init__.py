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

Example Usage:
    from galileo.__future__ import Project, Prompt, Message, MessageRole

    # Create or get a project
    project = Project(name="My AI Project")
    project = Project.get(name="My AI Project")

    # List all projects
    projects = Project.list()

    # Create and manage log streams through the project
    log_stream = project.create_log_stream(name="Production Logs")
    log_streams = project.list_log_streams()

    # Create and manage prompts
    prompt = Prompt(
        name="ml-expert-v1",
        messages=[
            Message(role=MessageRole.system, content="You are an expert in ML."),
            Message(role=MessageRole.user, content="{{input}}"),
        ],
    )

    # Create and manage datasets
    dataset = Dataset(
        name="ml-knowledge-evaluation_3",
        content=[
            {"input": "What is machine learning?", "output": "Machine learning ..."},
            {"input": "How does deep learning work?", "output": "Deep learning uses ..."}
        ]
    )
"""

from galileo.__future__.dataset import Dataset
from galileo.__future__.log_stream import LogStream
from galileo.__future__.project import Project
from galileo.__future__.prompt import Prompt
from galileo.schema.message import Message
from galileo_core.schemas.logging.llm import MessageRole

__all__ = ["Project", "LogStream", "Prompt", "Message", "MessageRole", "Dataset"]
