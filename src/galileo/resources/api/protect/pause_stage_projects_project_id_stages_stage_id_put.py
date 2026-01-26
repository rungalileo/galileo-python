from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo.exceptions import (
    AuthenticationError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from galileo.utils.headers_data import get_sdk_header
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.http_validation_error import HTTPValidationError
from ...models.stage_db import StageDB
from ...types import UNSET, Response, Unset


def _get_kwargs(project_id: str, stage_id: str, *, pause: Union[Unset, bool] = False) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["pause"] = pause

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.PUT,
        "return_raw_response": True,
        "path": f"/projects/{project_id}/stages/{stage_id}",
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Union[HTTPValidationError, StageDB]:
    if response.status_code == 200:
        return StageDB.from_dict(response.json())

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

    # Handle common HTTP errors with actionable messages
    if response.status_code == 400:
        raise BadRequestError(response.status_code, response.content)
    if response.status_code == 401:
        raise AuthenticationError(response.status_code, response.content)
    if response.status_code == 403:
        raise ForbiddenError(response.status_code, response.content)
    if response.status_code == 404:
        raise NotFoundError(response.status_code, response.content)
    if response.status_code == 409:
        raise ConflictError(response.status_code, response.content)
    if response.status_code == 429:
        raise RateLimitError(response.status_code, response.content)
    if response.status_code >= 500:
        raise ServerError(response.status_code, response.content)
    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[Union[HTTPValidationError, StageDB]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, stage_id: str, *, client: ApiClient, pause: Union[Unset, bool] = False
) -> Response[Union[HTTPValidationError, StageDB]]:
    """Pause Stage.

    Args:
        project_id (str):
        stage_id (str):
        pause (Union[Unset, bool]):  Default: False.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, StageDB]]
    """
    kwargs = _get_kwargs(project_id=project_id, stage_id=stage_id, pause=pause)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, stage_id: str, *, client: ApiClient, pause: Union[Unset, bool] = False
) -> Optional[Union[HTTPValidationError, StageDB]]:
    """Pause Stage.

    Args:
        project_id (str):
        stage_id (str):
        pause (Union[Unset, bool]):  Default: False.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, StageDB]
    """
    return sync_detailed(project_id=project_id, stage_id=stage_id, client=client, pause=pause).parsed


async def asyncio_detailed(
    project_id: str, stage_id: str, *, client: ApiClient, pause: Union[Unset, bool] = False
) -> Response[Union[HTTPValidationError, StageDB]]:
    """Pause Stage.

    Args:
        project_id (str):
        stage_id (str):
        pause (Union[Unset, bool]):  Default: False.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, StageDB]]
    """
    kwargs = _get_kwargs(project_id=project_id, stage_id=stage_id, pause=pause)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, stage_id: str, *, client: ApiClient, pause: Union[Unset, bool] = False
) -> Optional[Union[HTTPValidationError, StageDB]]:
    """Pause Stage.

    Args:
        project_id (str):
        stage_id (str):
        pause (Union[Unset, bool]):  Default: False.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, StageDB]
    """
    return (await asyncio_detailed(project_id=project_id, stage_id=stage_id, client=client, pause=pause)).parsed
