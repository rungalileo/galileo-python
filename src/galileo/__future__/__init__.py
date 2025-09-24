"""
Galileo Future API

This package provides the next-generation object-centric API for Galileo.
It offers an intuitive, object-oriented interface that simplifies common workflows
while maintaining full compatibility with the existing service-based functions.

Key Features:
- Object-centric design for better usability
- Simplified project and log stream management
- Backward-compatible with existing service functions
- Clean, intuitive method chaining and relationships

Example Usage:
    from galileo.__future__ import Project

    # Create or get a project
    project = Project(name="My AI Project")
    project = Project.get(name="My AI Project")

    # List all projects
    projects = Project.list()

    # Create and manage log streams through the project
    log_stream = project.create_log_stream(name="Production Logs")
    log_streams = project.list_log_streams()
"""

from galileo.__future__.log_stream import LogStream
from galileo.__future__.project import Project

__all__ = ["Project", "LogStream"]
