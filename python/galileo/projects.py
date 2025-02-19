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


from galileo.resources.types import Unset

from galileo.resources.models.http_validation_error import HTTPValidationError

from galileo.base import BaseClientModel


class Project(ProjectDBThin):
    def __init__(self, project_db: ProjectDBThin):
        self.project_db = project_db

    def __getattr__(self, attr):
        """
        Delegate attribute access to the underlying ProjectDB instance.
        """
        return getattr(self.project_db, attr)


class Projects(BaseClientModel):
    def list(self, limit: Union[Unset, int] = 100) -> list[Project]:
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
        projects: list["ProjectDBThin"] = get_all_projects_projects_all_get.sync(
            client=self.client, type_=ProjectType.GEN_AI
        )
        return [Project(project_db=project) for project in projects] if projects else []

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
            project = Project(project_db=project_response)

        elif name:
            projects_response = get_projects_projects_get.sync(
                client=self.client, project_name=name, type_=ProjectType.GEN_AI
            )

            if not projects_response or len(projects_response.projects) == 0:
                return None

            project = Project(project_db=projects_response.projects[0])

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

        body = ProjectCreate(name=name, type_=ProjectType.GEN_AI)
        response = create_project_projects_post.sync(client=self.client, body=body)

        if isinstance(response, HTTPValidationError):
            raise response

        if not response:
            raise ValueError("Unable to create project")

        return Project(project_db=response)


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
