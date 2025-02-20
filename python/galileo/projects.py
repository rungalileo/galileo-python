from typing import Union, Optional, overload

from galileo.resources.models.project_db import ProjectDB
from galileo.resources.models.project_db_thin import ProjectDBThin
from galileo.resources.models.project_type import ProjectType
from galileo.resources.models.project_create import ProjectCreate

from galileo.resources.api.projects import (
    get_project_projects_project_id_get,
    get_all_projects_projects_all_get,
    get_projects_projects_get,
    create_project_projects_post,
)

from galileo.resources.models.project_create_response import ProjectCreateResponse
from galileo.resources.models.permission import Permission
from galileo.resources.models.run_db import RunDB
from galileo.resources.models.run_db_thin import RunDBThin

from galileo.resources.types import Unset, UNSET

from galileo.resources.models.http_validation_error import HTTPValidationError

from galileo.base import BaseClientModel
import datetime


class Project:
    created_at: datetime.datetime
    created_by: str
    id: str
    updated_at: datetime.datetime
    bookmark: Union[Unset, bool] = False
    name: Union[None, Unset, str] = UNSET
    permissions: Union[Unset, list["Permission"]] = UNSET
    type: Union[None, ProjectType, Unset] = UNSET

    def __init__(
        self,
        project: Union[None, ProjectDBThin, ProjectDB, ProjectCreateResponse] = None,
    ) -> None:
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


class Projects(BaseClientModel):
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
        projects: list["ProjectDBThin"] = get_all_projects_projects_all_get.sync(
            client=self.client, type_=ProjectType.GEN_AI
        )
        return [Project(project=project) for project in projects] if projects else []

    @overload
    def get(self, *, id: str) -> Optional[Project]: ...
    @overload
    def get(self, *, name: str) -> Optional[Project]: ...
    def get(
        self,
        *,
        id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Optional[Project]:
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
        if (id is None) == (name is None):
            raise ValueError("Exactly one of 'id' or 'name' must be provided")

        if id:
            project_response = get_project_projects_project_id_get.sync(
                project_id=id,
                client=self.client,
            )
            if not project_response:
                return None
            project = Project(project=project_response)

        elif name:
            projects_response = get_projects_projects_get.sync(
                client=self.client, project_name=name, type_=ProjectType.GEN_AI
            )

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
        try:
            body = ProjectCreate(
                name=name,
                type_=ProjectType.GEN_AI,
                create_example_templates=False,
                created_by=None,
            )

            response = create_project_projects_post.sync(client=self.client, body=body)

            if isinstance(response, HTTPValidationError):
                print(response)
                raise response

            if not response:
                raise ValueError("Unable to create project")

            return Project(project=response)

        except Exception as e:
            raise e


#
# Convenience methods
#


def get_project(
    *, id: Optional[str] = None, name: Optional[str] = None
) -> Optional[Project]:
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
