"""
Project class for the Galileo Future API.

This module provides an object-centric interface for managing Galileo projects,
offering a more intuitive alternative to the service-based functions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from galileo.projects import Project as LegacyProject
from galileo.projects import create_project as service_create_project
from galileo.projects import get_project as service_get_project
from galileo.projects import list_projects as service_list_projects

if TYPE_CHECKING:
    from galileo.__future__.log_stream import LogStream


class Project:
    """
    Object-centric interface for Galileo projects.

    This class provides an intuitive way to work with Galileo projects,
    encapsulating project management operations and providing seamless
    integration with log stream management.

    Attributes:
        created_at (datetime.datetime): When the project was created.
        created_by (str): The user who created the project.
        id (str): The unique project identifier.
        updated_at (datetime.datetime): When the project was last updated.
        bookmark (Union[Unset, bool]): Whether the project is bookmarked.
        name (Union[None, Unset, str]): The project name.
        permissions (Union[Unset, list]): Project permissions.
        type (Union[None, ProjectType, Unset]): The project type.

    Examples:
        # Create a new project
        project = Project(name="My AI Project")

        # Get an existing project
        project = Project.get(name="My AI Project")

        # List all projects
        projects = Project.list()

        # Create a log stream for the project
        log_stream = project.create_log_stream(name="Production Logs")

        # List log streams for the project
        log_streams = project.list_log_streams()
    """

    def __init__(self, name: str | None = None, *, _legacy_project: LegacyProject | None = None) -> None:
        """
        Initialize a Project instance.

        When called with a name, this creates a new project. To get an existing
        project, use Project.get() instead.

        Args:
            name (Optional[str]): The name of the project to create.
            _legacy_project (Optional[LegacyProject]): Internal parameter for
                wrapping existing project instances.
        """
        if _legacy_project is not None:
            # Initialize from existing legacy project
            self._legacy_project = _legacy_project
            self.created_at = _legacy_project.created_at
            self.created_by = _legacy_project.created_by
            self.id = _legacy_project.id
            self.updated_at = _legacy_project.updated_at
            self.bookmark = _legacy_project.bookmark
            self.name = _legacy_project.name
            self.permissions = _legacy_project.permissions
            self.type = _legacy_project.type
        elif name is not None:
            # Create a new project
            self._legacy_project = service_create_project(name=name)
            self.created_at = self._legacy_project.created_at
            self.created_by = self._legacy_project.created_by
            self.id = self._legacy_project.id
            self.updated_at = self._legacy_project.updated_at
            self.bookmark = self._legacy_project.bookmark
            self.name = self._legacy_project.name
            self.permissions = self._legacy_project.permissions
            self.type = self._legacy_project.type
        else:
            raise ValueError(
                "Either 'name' must be provided to create a project, or use Project.get() to retrieve an existing project"
            )

    @classmethod
    def get(cls, *, id: str | None = None, name: str | None = None) -> Project | None:
        """
        Get an existing project by ID or name.

        Args:
            id (Optional[str]): The project ID.
            name (Optional[str]): The project name.

        Returns:
            Optional[Project]: The project if found, None otherwise.

        Raises:
            ValueError: If neither or both id and name are provided.

        Examples:
            # Get by name
            project = Project.get(name="My AI Project")

            # Get by ID
            project = Project.get(id="project-123")
        """
        legacy_project = service_get_project(id=id, name=name)
        if legacy_project is None:
            return None
        return cls(_legacy_project=legacy_project)

    @classmethod
    def list(cls) -> list[Project]:
        """
        List all available projects.

        Returns:
            List[Project]: A list of all projects.

        Examples:
            projects = Project.list()
            for project in projects:
                print(f"Project: {project.name} (ID: {project.id})")
        """
        legacy_projects = service_list_projects()
        return [cls(_legacy_project=legacy_project) for legacy_project in legacy_projects]

    def create_log_stream(self, name: str) -> LogStream:
        """
        Create a new log stream for this project.

        Args:
            name (str): The name of the log stream to create.

        Returns:
            LogStream: The created log stream.

        Examples:
            project = Project.get(name="My AI Project")
            log_stream = project.create_log_stream(name="Production Logs")
        """
        # Import here to avoid circular imports
        from galileo.__future__.log_stream import LogStream
        from galileo.log_streams import create_log_stream as service_create_log_stream

        legacy_log_stream = service_create_log_stream(name=name, project_id=self.id)
        return LogStream(_legacy_log_stream=legacy_log_stream)

    def list_log_streams(self) -> list[LogStream]:  # type: ignore[valid-type]
        """
        List all log streams for this project.

        Returns:
            List[LogStream]: A list of log streams belonging to this project.

        Examples:
            project = Project.get(name="My AI Project")
            log_streams = project.list_log_streams()
            for stream in log_streams:
                print(f"Log Stream: {stream.name} (ID: {stream.id})")
        """
        # Import here to avoid circular imports
        from galileo.__future__.log_stream import LogStream
        from galileo.log_streams import list_log_streams as service_list_log_streams

        legacy_log_streams = service_list_log_streams(project_id=self.id)
        return [LogStream(_legacy_log_stream=legacy_stream) for legacy_stream in legacy_log_streams]

    def __str__(self) -> str:
        """String representation of the project."""
        return f"Project(name='{self.name}', id='{self.id}')"

    def __repr__(self) -> str:
        """Detailed string representation of the project."""
        return f"Project(name='{self.name}', id='{self.id}', created_at='{self.created_at}')"
