import datetime
import os
from typing import Optional, Union

import httpx

from galileo.config import GalileoPythonConfig
from galileo.resources.api.projects import (
    create_project_projects_post,
    delete_project_projects_project_id_delete,
    get_all_projects_projects_all_get,
    get_project_projects_project_id_get,
    get_projects_projects_get,
)
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.permission import Permission
from galileo.resources.models.project_create import ProjectCreate
from galileo.resources.models.project_create_response import ProjectCreateResponse
from galileo.resources.models.project_db import ProjectDB
from galileo.resources.models.project_db_thin import ProjectDBThin
from galileo.resources.models.project_type import ProjectType
from galileo.resources.types import UNSET, Unset
from galileo.utils.catch_log import DecorateAllMethods
from galileo.utils.exceptions import APIException
from galileo.utils.logging import get_logger

_logger = get_logger(__name__)


class ProjectsAPIException(APIException):
    pass


class Project:
    """
    Represents a project in the Galileo platform.

    Projects are containers for logs, traces, and other data in Galileo. All logs are stored
    within a project, and users can create and manage projects to organize their LLM usage data.

    Attributes:
        created_at (datetime.datetime): The timestamp when the project was created.
        created_by (str): The identifier of the user who created the project.
        id (str): The unique identifier of the project.
        updated_at (datetime.datetime): The timestamp when the project was last updated.
        bookmark (Union[Unset, bool]): Whether the project is bookmarked. Defaults to False.
        name (Union[None, Unset, str]): The name of the project.
        permissions (Union[Unset, list["Permission"]]): The permissions associated with the project.
        type (Union[None, ProjectType, Unset]): The type of the project, typically GEN_AI.

    Examples:
         from galileo.projects import get_project, create_project, list_projects, delete_project

         # Create a new project
         project = create_project(name="My AI Project")

         # Get a project by name
         project = get_project(name="My AI Project")

         # Get a project by ID
         project = get_project(id="8aed99a3-c678-49a3-80e8-2bf914eda7a5")

         # List all projects
         projects = list_projects()
         for project in projects:
             print(f"Project: {project.name} (ID: {project.id})")

         # Delete a project by ID
         success = delete_project(id="8aed99a3-c678-49a3-80e8-2bf914eda7a5")

         # Delete a project by name
         success = delete_project(name="My AI Project")
    """

    created_at: datetime.datetime
    created_by: str
    id: str
    updated_at: datetime.datetime
    bookmark: Union[Unset, bool] = False
    name: Union[None, Unset, str] = UNSET
    permissions: Union[Unset, list["Permission"]] = UNSET
    type: Union[None, ProjectType, Unset] = UNSET

    def __init__(self, project: Union[None, ProjectDBThin, ProjectDB, ProjectCreateResponse] = None) -> None:
        """
        Initialize a Project instance.

        Args:
            project (Union[None, ProjectDBThin, ProjectDB, ProjectCreateResponse], optional):
                The project data to initialize from. If None, creates an empty project instance.
                Defaults to None.
        """
        if project is None:
            return

        self.created_at = project.created_at
        self.created_by = project.created_by
        self.id = project.id
        self.updated_at = project.updated_at
        self.name = project.name
        self.type = project.type_

        if isinstance(project, (ProjectDBThin, ProjectDB)):
            self.bookmark = project.bookmark
            self.permissions = project.permissions


class Projects(DecorateAllMethods):
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

    def list(self) -> list[Project]:
        """
        Lists all projects.

        Returns
        -------
        list[Project]
            A list of projects.

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        projects: list[ProjectDBThin] = get_all_projects_projects_all_get.sync(
            client=self.config.api_client, type_=ProjectType.GEN_AI
        )
        return [Project(project=project) for project in projects] if projects else []

    def get_with_env_fallbacks(self, *, id: Optional[str] = None, name: Optional[str] = None) -> Optional[Project]:
        """
        Retrieves a project by id or name.

        Either `id` or `name` must be provided, but not both. If neither is provided,
        the method will attempt to read from the environment variables `GALILEO_PROJECT_ID`
        and `GALILEO_PROJECT`. If both environment variables are set, a ValueError is raised.

        Parameters
        ----------
        id : str
            The id of the project.
        name : str
            The name of the project.
        Returns
        -------
        Project
            The project.

        Raises
        ------
        ValueError
            If neither or both `id` and `name` are provided.
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        id = id or (None if name else os.getenv("GALILEO_PROJECT_ID")) or None
        name = name or (None if id else os.getenv("GALILEO_PROJECT")) or None

        return self.get(id=id, name=name)

    def get(self, *, id: Optional[str] = None, name: Optional[str] = None) -> Optional[Project]:
        """
        Retrieves a project by id or name (exactly one of `id` or `name` must be provided).

        Parameters
        ----------
        id : str
            The id of the project.
        name : str
            The name of the project.
        Returns
        -------
        Project
            The project.

        Raises
        ------
        ValueError
            If neither or both `id` and `name` are provided.
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        name = name.strip() if name else None
        id = id.strip() if id else None

        # Check we have one and only one of project name or Id.
        if (not name and not id) or (name and id):
            raise ValueError("Exactly one of 'id' or 'name' must be provided.")

        project: Optional[Project] = None

        if id:
            detailed_response = get_project_projects_project_id_get.sync_detailed(
                project_id=id, client=self.config.api_client
            )
            if detailed_response.status_code != httpx.codes.OK:
                raise ProjectsAPIException(detailed_response.content)

            project_response = detailed_response.parsed
            if not project_response:
                return None
            project = Project(project=project_response)

        elif name:
            detailed_response = get_projects_projects_get.sync_detailed(
                client=self.config.api_client, project_name=name, type_=ProjectType.GEN_AI
            )

            if detailed_response.status_code != httpx.codes.OK:
                raise ProjectsAPIException(detailed_response.content)

            projects_response = detailed_response.parsed

            if not projects_response or len(projects_response) == 0:
                return None

            project = Project(project=projects_response[0])

        return project

    def create(self, name: str) -> Project:
        """
        Creates a new project.

        Parameters
        ----------
        name : str
            The name of the project.

        Returns
        -------
        Project
            The created project.

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        body = ProjectCreate(name=name, type_=ProjectType.GEN_AI, create_example_templates=False, created_by=None)

        detailed_response = create_project_projects_post.sync_detailed(client=self.config.api_client, body=body)

        if detailed_response.status_code != httpx.codes.OK:
            raise ProjectsAPIException(detailed_response.content)

        response = detailed_response.parsed

        if isinstance(response, HTTPValidationError):
            _logger.error(response)
            raise response

        if not response:
            raise ValueError(f"Unable to create project: {name}")

        return Project(project=response)

    def _delete_project(self, project_id: Optional[str] = None, project_name: Optional[str] = None) -> bool:
        """Internal method to handle project deletion logic."""
        # First, get the project to verify it exists and is a gen_ai project
        if project_id:
            project = self.get(id=project_id)
            identifier = project_id
        elif project_name:
            project = self.get(name=project_name)
            identifier = project_name
        else:
            raise ValueError("Either project_id or project_name must be provided")

        if not project:
            raise ProjectsAPIException(f"Project '{identifier}' not found")

        if project.type != ProjectType.GEN_AI:
            raise ProjectsAPIException(
                f"Project '{project.name}' (ID: {project.id}) is not a gen_ai project (type: {project.type}). Only gen_ai projects can be deleted through this SDK."
            )

        # Now delete using the project ID
        detailed_response = delete_project_projects_project_id_delete.sync_detailed(
            project_id=project.id, client=self.client
        )

        if detailed_response.status_code != httpx.codes.OK:
            raise ProjectsAPIException(str(detailed_response.content))

        response = detailed_response.parsed

        if isinstance(response, HTTPValidationError):
            _logger.error(response)
            raise ProjectsAPIException(str(response))

        return response is not None


#
# Convenience methods
#


def get_project(*, id: Optional[str] = None, name: Optional[str] = None) -> Optional[Project]:
    """
    Retrieves a project by id or name (exactly one of `id` or `name` must be provided).

    Parameters
    ----------
    id : str
        The id of the project.
    name : str
        The name of the project.
    with_content : bool
        Whether to return the content of the project. Default is False.

    Returns
    -------
    Project
        The project.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return Projects().get(id=id, name=name)


def list_projects() -> list[Project]:
    """
    Lists all projects.

    Parameters
    ----------
    limit : Union[Unset, int]
        The maximum number of projects to return. Default is 100.

    Returns
    -------
    list[Project]
        A list of projects.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return Projects().list()


def create_project(name: str) -> Project:
    """
    Creates a new project.

    Parameters
    ----------
    name : str
        The name of the project.
    type_ : ProjectType
        The type of the project.

    Returns
    -------
    Project
        The created project.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return Projects().create(name=name)


def delete_project(*, id: Optional[str] = None, name: Optional[str] = None) -> bool:
    """
    Deletes a gen_ai project by ID or name (exactly one of `id` or `name` must be provided).

    Parameters
    ----------
    id : str, optional
        The ID of the project to delete.
    name : str, optional
        The name of the project to delete.

    Returns
    -------
    bool
        True if the project was successfully deleted, False otherwise.

    Raises
    ------
    ValueError
        If neither or both `id` and `name` are provided.
    ProjectsAPIException
        If the server returns an error response or if the project is not a gen_ai project.
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    Examples
    --------
    >>> delete_project(id="8aed99a3-c678-49a3-80e8-2bf914eda7a5")
    >>> delete_project(name="my-project")
    """
    if (id is None) == (name is None):  # Both None or both not None
        raise ValueError("Exactly one of 'id' or 'name' must be provided")

    if id:
        return Projects()._delete_project(project_id=id)
    else:
        return Projects()._delete_project(project_name=name)
