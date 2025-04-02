import datetime
import logging
from typing import Optional, Union, overload

import httpx

from galileo.base import BaseClientModel
from galileo.resources.api.projects import (
    create_project_projects_post,
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

_logger = logging.getLogger(__name__)


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
         from galileo.projects import get_project, create_project, list_projects

         # Create a new project
         project = create_project(name="My AI Project")

         # Get a project by name
         project = get_project(name="My AI Project")

         # Get a project by ID
         project = get_project(id="project-id-123")

         # List all projects
         projects = list_projects()
         for project in projects:
             print(f"Project: {project.name} (ID: {project.id})")
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

        if isinstance(project, ProjectDBThin) or isinstance(project, ProjectDB):
            self.bookmark = project.bookmark
            self.permissions = project.permissions


class Projects(BaseClientModel, DecorateAllMethods):
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
            client=self.client, type_=ProjectType.GEN_AI
        )
        return [Project(project=project) for project in projects] if projects else []

    @overload
    def get(self, *, id: str) -> Optional[Project]: ...
    @overload
    def get(self, *, name: str) -> Optional[Project]: ...
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
        if (id is None) and (name is None):
            raise ValueError("Exactly one of 'id' or 'name' must be provided")

        if id:
            detailed_response = get_project_projects_project_id_get.sync_detailed(project_id=id, client=self.client)
            if detailed_response.status_code != httpx.codes.OK:
                raise ProjectsAPIException(detailed_response.content)

            project_response = detailed_response.parsed
            if not project_response:
                return None
            project = Project(project=project_response)

        elif name:
            detailed_response = get_projects_projects_get.sync_detailed(
                client=self.client, project_name=name, type_=ProjectType.GEN_AI
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

        detailed_response = create_project_projects_post.sync_detailed(client=self.client, body=body)

        if detailed_response.status_code != httpx.codes.OK:
            raise ProjectsAPIException(detailed_response.content)

        response = detailed_response.parsed

        if isinstance(response, HTTPValidationError):
            _logger.error(response)
            raise response

        if not response:
            raise ValueError(f"Unable to create project: {name}")

        return Project(project=response)


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
