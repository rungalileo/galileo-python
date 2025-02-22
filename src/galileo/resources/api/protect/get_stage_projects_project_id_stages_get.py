from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.stage_db import StageDB
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str, *, stage_name: Union[None, Unset, str] = UNSET, stage_id: Union[None, Unset, str] = UNSET
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_stage_name: Union[None, Unset, str]
    if isinstance(stage_name, Unset):
        json_stage_name = UNSET
    else:
        json_stage_name = stage_name
    params["stage_name"] = json_stage_name

    json_stage_id: Union[None, Unset, str]
    if isinstance(stage_id, Unset):
        json_stage_id = UNSET
    else:
        json_stage_id = stage_id
    params["stage_id"] = json_stage_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "get", "url": f"/projects/{project_id}/stages", "params": params}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, StageDB]]:
    if response.status_code == 200:
        response_200 = StageDB.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, StageDB]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    stage_name: Union[None, Unset, str] = UNSET,
    stage_id: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, StageDB]]:
    """Get Stage

    Args:
        project_id (str):
        stage_name (Union[None, Unset, str]):
        stage_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StageDB]]
    """

    kwargs = _get_kwargs(project_id=project_id, stage_name=stage_name, stage_id=stage_id)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    stage_name: Union[None, Unset, str] = UNSET,
    stage_id: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, StageDB]]:
    """Get Stage

    Args:
        project_id (str):
        stage_name (Union[None, Unset, str]):
        stage_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StageDB]
    """

    return sync_detailed(project_id=project_id, client=client, stage_name=stage_name, stage_id=stage_id).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    stage_name: Union[None, Unset, str] = UNSET,
    stage_id: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, StageDB]]:
    """Get Stage

    Args:
        project_id (str):
        stage_name (Union[None, Unset, str]):
        stage_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StageDB]]
    """

    kwargs = _get_kwargs(project_id=project_id, stage_name=stage_name, stage_id=stage_id)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    stage_name: Union[None, Unset, str] = UNSET,
    stage_id: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, StageDB]]:
    """Get Stage

    Args:
        project_id (str):
        stage_name (Union[None, Unset, str]):
        stage_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StageDB]
    """

    return (
        await asyncio_detailed(project_id=project_id, client=client, stage_name=stage_name, stage_id=stage_id)
    ).parsed
