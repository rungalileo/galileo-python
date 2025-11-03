from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

from galileo.__future__.shared.base import StateManagementMixin, SyncState
from galileo.__future__.shared.exceptions import APIError, ValidationError
from galileo.projects import Projects

if TYPE_CHECKING:
    from galileo.__future__.dataset import Dataset
    from galileo.__future__.experiment import Experiment
    from galileo.__future__.log_stream import LogStream
    from galileo.__future__.prompt import Prompt

logger = logging.getLogger(__name__)


class Project(StateManagementMixin):
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

        # Access related resources via properties
        for log_stream in project.logstreams:
            print(log_stream.name)

        for experiment in project.experiments:
            print(experiment.name)

        for dataset in project.datasets:
            print(dataset.name)

        for prompt in project.prompts:
            print(prompt.name)

        # Or use the explicit list methods
        datasets = project.list_datasets()
        prompts = project.list_prompts()

        # Delete a project (WARNING: cannot be undone!)
        old_project = Project.get(name="Old Project")
        old_project.delete()
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

    def __str__(self) -> str:
        """String representation of the project."""
        return f"Project(name='{self.name}', id='{self.id}')"

    def __repr__(self) -> str:
        """Detailed string representation of the project."""
        return f"Project(name='{self.name}', id='{self.id}', created_at='{self.created_at}')"

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

    @classmethod
    def _create_empty(cls) -> Project:
        """Internal constructor bypassing __init__ for API hydration."""
        instance = cls.__new__(cls)
        super(Project, instance).__init__()
        return instance

    @classmethod
    def _from_api_response(cls, retrieved_project: Any) -> Project:
        """
        Factory method to create a Project instance from an API response.

        Args:
            retrieved_project: The project data retrieved from the API.

        Returns
        -------
            Project: A new Project instance populated with the API data.
        """
        instance = cls._create_empty()
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

            return cls._from_api_response(retrieved_project)
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

        return [cls._from_api_response(retrieved_project) for retrieved_project in retrieved_projects]

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

        # Use the LogStream pattern to avoid duplication
        return LogStream(name=name, project_id=self.id).create()

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

        # Use the LogStream pattern to avoid duplication
        return LogStream.list(project_id=self.id)

    def list_experiments(self) -> list[Experiment]:  # type: ignore[valid-type]
        """
        List all experiments for this project.

        Returns
        -------
            List[Experiment]: A list of experiments belonging to this project.

        Examples
        --------
            project = Project.get(name="My AI Project")
            experiments = project.list_experiments()
            for exp in experiments:
                # Process each experiment
                pass
        """
        if self.id is None:
            raise ValueError("Project ID is not set. Cannot list experiments for a local-only project.")

        # Use the Experiment pattern to avoid duplication
        return Experiment.list(project_id=self.id)

    def list_datasets(self) -> list[Dataset]:  # type: ignore[valid-type]
        """
        List all datasets used in this project.

        Returns
        -------
            List[Dataset]: A list of datasets used in this project.

        Examples
        --------
            project = Project.get(name="My AI Project")
            datasets = project.list_datasets()
            for dataset in datasets:
                # Process each dataset
                pass
        """
        if self.id is None:
            raise ValueError("Project ID is not set. Cannot list datasets for a local-only project.")

        # Use the Dataset pattern to avoid duplication
        return Dataset.list(project_id=self.id)

    def list_prompts(self) -> list[Prompt]:  # type: ignore[valid-type]
        """
        List all prompts used in this project.

        Returns
        -------
            List[Prompt]: A list of prompts used in this project.

        Examples
        --------
            project = Project.get(name="My AI Project")
            prompts = project.list_prompts()
            for prompt in prompts:
                # Process each prompt
                pass
        """
        if self.id is None:
            raise ValueError("Project ID is not set. Cannot list prompts for a local-only project.")

        # Use the Prompt pattern to avoid duplication
        return Prompt.list(project_id=self.id)

    @property
    def logstreams(self) -> list[LogStream]:  # type: ignore[valid-type]
        """
        Property to access log streams for this project.

        This is a read-only property that returns the current list of log streams.
        To create new log streams, use create_log_stream().

        Returns
        -------
            List[LogStream]: A list of log streams belonging to this project.

        Examples
        --------
            project = Project.get(name="My AI Project")
            for stream in project.logstreams:
                print(stream.name)
        """
        return self.list_log_streams()

    @property
    def experiments(self) -> list[Experiment]:  # type: ignore[valid-type]
        """
        Property to access experiments for this project.

        This is a read-only property that returns the current list of experiments.

        Returns
        -------
            List[Experiment]: A list of experiments belonging to this project.

        Examples
        --------
            project = Project.get(name="My AI Project")
            for exp in project.experiments:
                print(exp.name)
        """
        return self.list_experiments()

    @property
    def datasets(self) -> list[Dataset]:  # type: ignore[valid-type]
        """
        Property to access datasets used in this project.

        This is a read-only property that returns the datasets associated with this project.

        Returns
        -------
            List[Dataset]: A list of datasets used in this project.

        Examples
        --------
            project = Project.get(name="My AI Project")
            for dataset in project.datasets:
                print(dataset.name)
        """
        return self.list_datasets()

    @property
    def prompts(self) -> list[Prompt]:  # type: ignore[valid-type]
        """
        Property to access prompts used in this project.

        This is a read-only property that returns the prompts associated with this project.

        Returns
        -------
            List[Prompt]: A list of prompts used in this project.

        Examples
        --------
            project = Project.get(name="My AI Project")
            for prompt in project.prompts:
                print(prompt.name)
        """
        return self.list_prompts()

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

    def delete(self) -> None:
        """
        Delete this project.

        This is a destructive operation that permanently removes the project
        and all associated data (experiments, log streams, datasets, traces, etc.)
        from the API.

        WARNING: This operation cannot be undone!

        After successful deletion, the object state is set to DELETED. The local
        object still exists in memory but no longer represents a remote resource.

        Raises
        ------
            ValueError: If the project ID is not set.
            Exception: If the API call fails.

        Examples
        --------
            # Delete a project
            project = Project.get(name="Old Project")
            project.delete()
            assert project.is_deleted()

            # After deletion, the project no longer exists remotely
            # The local object is marked as DELETED
            print(project.sync_state)  # SyncState.DELETED
        """
        if self.id is None:
            raise ValueError("Project ID is not set. Cannot delete a local-only project.")

        try:
            logger.info(f"Project.delete: name='{self.name}' id='{self.id}' - started")
            projects_service = Projects()
            projects_service.delete_project(id=self.id)
            # Set state to deleted after successful deletion
            self._set_state(SyncState.DELETED)
            logger.info(f"Project.delete: name='{self.name}' id='{self.id}' - completed")
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Project.delete: name='{self.name}' id='{self.id}' - failed: {e}")
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


# Import at end to avoid circular import (log_stream.py imports Project)
from galileo.__future__.dataset import Dataset  # noqa: E402
from galileo.__future__.experiment import Experiment  # noqa: E402
from galileo.__future__.log_stream import LogStream  # noqa: E402
from galileo.__future__.prompt import Prompt  # noqa: E402
