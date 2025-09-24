from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from galileo.__future__.base import BusinessObjectMixin, SyncState
from galileo.__future__.exceptions import APIError, ValidationError
from galileo.__future__.log_stream import LogStream
from galileo.log_streams import LogStreams
from galileo.projects import Projects

logger = logging.getLogger(__name__)


class Project(BusinessObjectMixin):
    """
    Object-centric interface for Galileo projects.

    This class provides an intuitive way to work with Galileo projects,
    encapsulating project management operations and providing seamless
    integration with log stream management.

    Attributes
    ----------
        created_at (datetime.datetime): When the project was created.
        created_by (str): The user who created the project.
        id (str): The unique project identifier.
        updated_at (datetime.datetime): When the project was last updated.
        bookmark (Union[Unset, bool]): Whether the project is bookmarked.
        name (Union[None, Unset, str]): The project name.
        permissions (Union[Unset, list]): Project permissions.
        type (Union[None, ProjectType, Unset]): The project type.

    Examples
    --------
        # Create a new project locally, then persist
        project = Project(name="My AI Project").create()

        # Get an existing project
        project = Project.get(name="My AI Project")

        # List all projects
        projects = Project.list()

        # Create a log stream for the project
        log_stream = project.create_log_stream(name="Production Logs")

        # List log streams for the project
        log_streams = project.list_log_streams()
    """

    # Type annotations for instance attributes
    id: str | None
    name: str | None
    created_at: datetime | None
    created_by: str | None
    updated_at: datetime | None
    bookmark: bool | None
    permissions: list[Any] | None
    type: Any | None

    def __init__(self, name: str | None = None) -> None:
        """
        Initialize a Project instance locally.

        Creates a local project object that exists only in memory until .create()
        is called to persist it to the API.

        Args:
            name (Optional[str]): The name of the project to create.

        Raises
        ------
            ValidationError: If name is not provided.
        """
        super().__init__()
        if name is None:
            raise ValidationError(
                "'name' must be provided to create a project. Use Project.get() to retrieve an existing project."
            )

        # Initialize attributes locally
        self.name = name
        self.id = None
        self.created_at = None
        self.created_by = None
        self.updated_at = None
        self.bookmark = None
        self.permissions = None
        self.type = None

        # Set initial state
        self._set_state(SyncState.LOCAL_ONLY)

    def create(self) -> Project:
        """
        Persist this project to the API.

        Returns
        -------
            Project: This project instance with updated attributes from the API.

        Raises
        ------
            Exception: If the API call fails.

        Examples
        --------
            project = Project(name="My AI Project").create()
            assert project.is_synced()
        """
        if self.name is None:
            raise ValueError("Project name is not set. Cannot create project without a name.")
        try:
            logger.info(f"Project.create: name='{self.name}' - started")
            projects_service = Projects()
            created_project = projects_service.create(name=self.name)

            # Update attributes from response
            self.created_at = created_project.created_at
            self.created_by = created_project.created_by
            self.id = created_project.id
            self.updated_at = created_project.updated_at
            self.bookmark = created_project.bookmark
            self.name = created_project.name
            self.permissions = created_project.permissions
            self.type = created_project.type

            # Set state to synced
            self._set_state(SyncState.SYNCED)
            logger.info(f"Project.create: id='{self.id}' - completed")
            return self
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Project.create: name='{self.name}' - failed: {e}")
            raise

    @classmethod
    def get(cls, *, id: str | None = None, name: str | None = None) -> Project | None:
        """
        Get an existing project by ID or name.

        Args:
            id (Optional[str]): The project ID.
            name (Optional[str]): The project name.

        Returns
        -------
            Optional[Project]: The project if found, None otherwise.

        Raises
        ------
            ValidationError: If neither or both id and name are provided.

        Examples
        --------
            # Get by name
            project = Project.get(name="My AI Project")

            # Get by ID
            project = Project.get(id="project-123")
        """
        try:
            projects_service = Projects()
            retrieved_project = projects_service.get(id=id, name=name)
            if retrieved_project is None:
                return None

            # Create a new instance and populate its attributes
            instance = cls.__new__(cls)
            # Initialize mixin state
            BusinessObjectMixin.__init__(instance)
            instance.created_at = retrieved_project.created_at
            instance.created_by = retrieved_project.created_by
            instance.id = retrieved_project.id
            instance.updated_at = retrieved_project.updated_at
            instance.bookmark = retrieved_project.bookmark
            instance.name = retrieved_project.name
            instance.permissions = retrieved_project.permissions
            instance.type = retrieved_project.type
            # Set state to synced since we just retrieved from API
            instance._set_state(SyncState.SYNCED)
            return instance
        except Exception as e:
            logger.error("Project.get: id='%s' name='%s' - failed: %s", id, name, str(e))
            raise APIError("Failed to retrieve project: %s", original_error=e) from e

    @classmethod
    def list(cls) -> list[Project]:
        """
        List all available projects.

        Returns
        -------
            List[Project]: A list of all projects.

        Examples
        --------
            projects = Project.list()
            for project in projects:
                # Process each project
                pass
        """
        projects_service = Projects()
        retrieved_projects = projects_service.list()

        result = []
        for retrieved_project in retrieved_projects:
            instance = cls.__new__(cls)
            # Initialize mixin state
            BusinessObjectMixin.__init__(instance)
            instance.created_at = retrieved_project.created_at
            instance.created_by = retrieved_project.created_by
            instance.id = retrieved_project.id
            instance.updated_at = retrieved_project.updated_at
            instance.bookmark = retrieved_project.bookmark
            instance.name = retrieved_project.name
            instance.permissions = retrieved_project.permissions
            instance.type = retrieved_project.type
            # Set state to synced since we just retrieved from API
            instance._set_state(SyncState.SYNCED)
            result.append(instance)

        return result

    def create_log_stream(self, name: str) -> LogStream:
        """
        Create a new log stream for this project.

        Args:
            name (str): The name of the log stream to create.

        Returns
        -------
            LogStream: The created log stream.

        Examples
        --------
            project = Project.get(name="My AI Project")
            log_stream = project.create_log_stream(name="Production Logs")
        """
        if self.id is None:
            raise ValueError("Project ID is not set. Cannot create log stream for a local-only project.")
        logger.info(f"LogStream.create: name='{name}' project_id='{self.id}' - started")
        log_streams_service = LogStreams()
        created_log_stream = log_streams_service.create(name=name, project_id=self.id)
        logger.info(f"LogStream.create: id='{created_log_stream.id}' - completed")

        # Create a new LogStream instance and populate its attributes
        instance = LogStream.__new__(LogStream)
        instance.created_at = created_log_stream.created_at
        instance.created_by = created_log_stream.created_by
        instance.id = created_log_stream.id
        instance.name = created_log_stream.name
        instance.project_id = created_log_stream.project_id
        instance.updated_at = created_log_stream.updated_at
        instance.additional_properties = created_log_stream.additional_properties
        return instance

    def list_log_streams(self) -> list[LogStream]:  # type: ignore[valid-type]
        """
        List all log streams for this project.

        Returns
        -------
            List[LogStream]: A list of log streams belonging to this project.

        Examples
        --------
            project = Project.get(name="My AI Project")
            log_streams = project.list_log_streams()
            for stream in log_streams:
                # Process each log stream
                pass
        """
        if self.id is None:
            raise ValueError("Project ID is not set. Cannot list log streams for a local-only project.")
        log_streams_service = LogStreams()
        retrieved_log_streams = log_streams_service.list(project_id=self.id)

        result = []
        for retrieved_log_stream in retrieved_log_streams:
            instance = LogStream.__new__(LogStream)
            instance.created_at = retrieved_log_stream.created_at
            instance.created_by = retrieved_log_stream.created_by
            instance.id = retrieved_log_stream.id
            instance.name = retrieved_log_stream.name
            instance.project_id = retrieved_log_stream.project_id
            instance.updated_at = retrieved_log_stream.updated_at
            instance.additional_properties = retrieved_log_stream.additional_properties
            result.append(instance)

        return result

    def refresh(self) -> None:
        """
        Refresh this project's state from the API.

        Updates all attributes with the latest values from the remote API
        and sets the state to SYNCED.

        Raises
        ------
            Exception: If the API call fails or the project no longer exists.

        Examples
        --------
            project.refresh()
            assert project.is_synced()
        """
        if self.id is None:
            raise ValueError("Project ID is not set. Cannot refresh a local-only project.")
        try:
            logger.debug(f"Project.refresh: id='{self.id}' - started")
            projects_service = Projects()
            retrieved_project = projects_service.get(id=self.id)

            if retrieved_project is None:
                raise ValueError(f"Project with id '{self.id}' no longer exists")

            # Update all attributes from response
            self.created_at = retrieved_project.created_at
            self.created_by = retrieved_project.created_by
            self.id = retrieved_project.id
            self.updated_at = retrieved_project.updated_at
            self.bookmark = retrieved_project.bookmark
            self.name = retrieved_project.name
            self.permissions = retrieved_project.permissions
            self.type = retrieved_project.type

            # Set state to synced
            self._set_state(SyncState.SYNCED)
            logger.debug(f"Project.refresh: id='{self.id}' - completed")
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Project.refresh: id='{self.id}' - failed: {e}")
            raise

    def save(self) -> Project:
        """
        Save changes to this project.

        This method is a placeholder for future functionality to update
        project properties.

        Returns
        -------
            Project: This project instance.

        Raises
        ------
            NotImplementedError: This functionality is not yet implemented.
        """
        raise NotImplementedError(
            "Project updates are not yet implemented. Use specific methods to modify project state."
        )

    def __str__(self) -> str:
        """String representation of the project."""
        return f"Project(name='{self.name}', id='{self.id}')"

    def __repr__(self) -> str:
        """Detailed string representation of the project."""
        return f"Project(name='{self.name}', id='{self.id}', created_at='{self.created_at}')"
