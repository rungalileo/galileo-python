from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.gen_ai_project_settings import GenAIProjectSettings
from ...models.http_validation_error import HTTPValidationError
from ...models.project_settings_db import ProjectSettingsDB
from ...types import Response


def _get_kwargs(project_id: str, *, body: GenAIProjectSettings) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": "put", "url": f"/projects/{project_id}/settings"}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ProjectSettingsDB]]:
    if response.status_code == 200:
        response_200 = ProjectSettingsDB.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, ProjectSettingsDB]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, *, client: AuthenticatedClient, body: GenAIProjectSettings
) -> Response[Union[HTTPValidationError, ProjectSettingsDB]]:
    """Update Project Settings

    Args:
        project_id (str):
        body (GenAIProjectSettings):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ProjectSettingsDB]]
    """

    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, *, client: AuthenticatedClient, body: GenAIProjectSettings
) -> Optional[Union[HTTPValidationError, ProjectSettingsDB]]:
    """Update Project Settings

    Args:
        project_id (str):
        body (GenAIProjectSettings):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ProjectSettingsDB]
    """

    return sync_detailed(project_id=project_id, client=client, body=body).parsed


async def asyncio_detailed(
    project_id: str, *, client: AuthenticatedClient, body: GenAIProjectSettings
) -> Response[Union[HTTPValidationError, ProjectSettingsDB]]:
    """Update Project Settings

    Args:
        project_id (str):
        body (GenAIProjectSettings):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ProjectSettingsDB]]
    """

    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, *, client: AuthenticatedClient, body: GenAIProjectSettings
) -> Optional[Union[HTTPValidationError, ProjectSettingsDB]]:
    """Update Project Settings

    Args:
        project_id (str):
        body (GenAIProjectSettings):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ProjectSettingsDB]
    """

    return (await asyncio_detailed(project_id=project_id, client=client, body=body)).parsed
