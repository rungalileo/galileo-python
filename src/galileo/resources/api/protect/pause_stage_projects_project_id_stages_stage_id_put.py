from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.stage_db import StageDB
from ...types import UNSET, Response, Unset


def _get_kwargs(project_id: str, stage_id: str, *, pause: Union[Unset, bool] = False) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["pause"] = pause

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "put", "url": f"/projects/{project_id}/stages/{stage_id}", "params": params}

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
    project_id: str, stage_id: str, *, client: AuthenticatedClient, pause: Union[Unset, bool] = False
) -> Response[Union[HTTPValidationError, StageDB]]:
    """Pause Stage

    Args:
        project_id (str):
        stage_id (str):
        pause (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StageDB]]
    """

    kwargs = _get_kwargs(project_id=project_id, stage_id=stage_id, pause=pause)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, stage_id: str, *, client: AuthenticatedClient, pause: Union[Unset, bool] = False
) -> Optional[Union[HTTPValidationError, StageDB]]:
    """Pause Stage

    Args:
        project_id (str):
        stage_id (str):
        pause (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StageDB]
    """

    return sync_detailed(project_id=project_id, stage_id=stage_id, client=client, pause=pause).parsed


async def asyncio_detailed(
    project_id: str, stage_id: str, *, client: AuthenticatedClient, pause: Union[Unset, bool] = False
) -> Response[Union[HTTPValidationError, StageDB]]:
    """Pause Stage

    Args:
        project_id (str):
        stage_id (str):
        pause (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StageDB]]
    """

    kwargs = _get_kwargs(project_id=project_id, stage_id=stage_id, pause=pause)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, stage_id: str, *, client: AuthenticatedClient, pause: Union[Unset, bool] = False
) -> Optional[Union[HTTPValidationError, StageDB]]:
    """Pause Stage

    Args:
        project_id (str):
        stage_id (str):
        pause (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StageDB]
    """

    return (await asyncio_detailed(project_id=project_id, stage_id=stage_id, client=client, pause=pause)).parsed
