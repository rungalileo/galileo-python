import builtins
from typing import Optional, Union, overload

from galileo.base import BaseClientModel
from galileo.projects import Projects
from galileo.resources.api.log_stream import (
    create_log_stream_v2_projects_project_id_log_streams_post,
    get_log_stream_v2_projects_project_id_log_streams_log_stream_id_get,
    list_log_streams_v2_projects_project_id_log_streams_get,
)
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.log_stream_create_request import LogStreamCreateRequest
from galileo.resources.models.log_stream_response import LogStreamResponse


class LogStream(LogStreamResponse):
    def __init__(self, log_stream: Union[None, LogStreamResponse] = None):
        if log_stream is not None:
            super().__init__(
                created_at=log_stream.created_at,
                id=log_stream.id,
                name=log_stream.name,
                project_id=log_stream.project_id,
                updated_at=log_stream.updated_at,
                created_by=log_stream.created_by,
            )
            self.additional_properties = log_stream.additional_properties.copy()
            return


class LogStreams(BaseClientModel):
    @overload
    def list(self, *, project_id: str) -> list[LogStream]: ...

    @overload
    def list(self, *, project_name: str) -> builtins.list[LogStream]: ...

    def list(self, *, project_id: Optional[str] = None, project_name: Optional[str] = None) -> builtins.list[LogStream]:
        """
        Lists all log streams. Exactly one of `project_id` or `project_name` must be provided.

        Parameters
        ----------
        project_id : Optional[str]
            The ID of the project to list log streams for.
        project_name : Optional[str]
            The name of the project to list log streams for.

        Returns
        -------
        list[LogStream]
            A list of log streams.

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        if (project_id is None) == (project_name is None):
            raise ValueError("Exactly one of 'project_id' or 'project_name' must be provided")

        if project_id:
            log_streams = list_log_streams_v2_projects_project_id_log_streams_get.sync(
                client=self.client, project_id=project_id
            )
        else:
            project = Projects(client=self.client).get(name=project_name)
            if not project:
                raise ValueError(f"Project {project_name} not found")
            log_streams = list_log_streams_v2_projects_project_id_log_streams_get.sync(
                client=self.client, project_id=project.id
            )
        return [LogStream(log_stream=log_stream) for log_stream in log_streams] if log_streams else []

    @overload
    def get(
        self, *, id: str, project_id: Optional[str] = None, project_name: Optional[str] = None
    ) -> Optional[LogStream]: ...
    @overload
    def get(
        self, *, name: str, project_id: Optional[str] = None, project_name: Optional[str] = None
    ) -> Optional[LogStream]: ...
    def get(
        self,
        *,
        id: Optional[str] = None,
        name: Optional[str] = None,
        project_id: Optional[str] = None,
        project_name: Optional[str] = None,
    ) -> Optional[LogStream]:
        """
        Retrieves a log stream by id or name.
        Exactly one of `id` or `name` must be provided.
        Exactly one of `project_id` or `project_name` must be provided.

        Parameters
        ----------
        id : str
            The id of the log stream.
        name : str
            The name of the log stream.
        Returns
        -------
        LogStream
            The log stream.

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

        if (project_id is None) == (project_name is None):
            raise ValueError("Exactly one of 'project_id' or 'project_name' must be provided")

        if not project_id:
            project = Projects(client=self.client).get(name=project_name)
            if not project:
                raise ValueError(f"Project {project_name} not found")
            project_id = project.id

        if id:
            log_stream_response = get_log_stream_v2_projects_project_id_log_streams_log_stream_id_get.sync(
                project_id=project_id, log_stream_id=id, client=self.client
            )
            if not log_stream_response:
                return None
            log_stream = LogStream(log_stream=log_stream_response)

        elif name:
            log_streams = self.list(project_id=project_id)

            if not log_streams or len(log_streams) == 0:
                return None

            log_stream = log_streams[0]

        return log_stream

    @overload
    def create(self, name: str, *, project_id: Optional[str] = None) -> LogStream: ...
    @overload
    def create(self, name: str, *, project_name: str) -> LogStream: ...

    def create(self, name: str, *, project_id: Optional[str] = None, project_name: Optional[str] = None) -> LogStream:
        """
        Creates a new log stream. Exactly one of `project_id` or `project_name` must be provided.

        Parameters
        ----------
        name : str
            The name of the log stream.
        project_id : Optional[str], optional
            The ID of the project to create the log stream in, by default None
        project_name : Optional[str], optional
            The name of the project to create the log stream in, by default None

        Returns
        -------
        LogStream
            The created log stream.

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """

        if (project_id is None) == (project_name is None):
            raise ValueError("Exactly one of 'project_id' or 'project_name' must be provided")

        if not project_id:
            project = Projects(client=self.client).get(name=project_name)
            if not project:
                raise ValueError(f"Project {project_name} not found")
            project_id = project.id

        body = LogStreamCreateRequest(name=name)
        response = create_log_stream_v2_projects_project_id_log_streams_post.sync(
            project_id=project_id, client=self.client, body=body
        )

        if isinstance(response, HTTPValidationError):
            raise response

        if not response:
            raise ValueError("Unable to create log stream")

        return LogStream(log_stream=response)


#
# Convenience methods
#


def get_log_stream(
    *, name: Optional[str] = None, project_id: Optional[str] = None, project_name: Optional[str] = None
) -> Optional[LogStream]:
    """
    Retrieves a log stream by name. Exactly one of `project_id` or `project_name` must be provided.

    Parameters
    ----------
    name : str
        The name of the log stream.
    project_id : str
        The id of the project.
    project_name : str
        The name of the project.

    Returns
    -------
    LogStream
        The log stream.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return LogStreams().get(name=name, project_id=project_id, project_name=project_name)


def list_log_streams(*, project_id: Optional[str] = None, project_name: Optional[str] = None) -> list[LogStream]:
    """
    Lists all log streams. Exactly one of `project_id` or `project_name` must be provided.

    Parameters
    ----------
    project_id : str
        The id of the project.
    project_name : str
        The name of the project.

    Returns
    -------
    list[LogStream]
        A list of projects.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return LogStreams().list(project_id=project_id, project_name=project_name)


def create_log_stream(name: str, project_id: Optional[str] = None, project_name: Optional[str] = None) -> LogStream:
    """
    Creates a new log stream. Exactly one of `project_id` or `project_name` must be provided.

    Parameters
    ----------
    name : str
        The name of the log stream.

    Returns
    -------
    LogStream
        The created project.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return LogStreams().create(name=name, project_id=project_id, project_name=project_name)
