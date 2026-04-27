from http import HTTPStatus
from typing import Any, Optional

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
from ...models.run_db import RunDB
from ...types import UNSET, Response, Unset


def _get_kwargs(project_id: str, *, run_name: None | str | Unset = UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_run_name: None | str | Unset
    if isinstance(run_name, Unset):
        json_run_name = UNSET
    else:
        json_run_name = run_name
    params["run_name"] = json_run_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/projects/{project_id}/runs".format(project_id=project_id),
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | list[RunDB]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RunDB.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

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


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[HTTPValidationError | list[RunDB]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, *, client: ApiClient, run_name: None | str | Unset = UNSET
) -> Response[HTTPValidationError | list[RunDB]]:
    """Get Project Runs

     Gets all runs for a project.

    If a run_name is provided, gets the run with that name, or []

    Args:
        project_id (str):
        run_name (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[RunDB]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_name=run_name)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, *, client: ApiClient, run_name: None | str | Unset = UNSET
) -> Optional[HTTPValidationError | list[RunDB]]:
    """Get Project Runs

     Gets all runs for a project.

    If a run_name is provided, gets the run with that name, or []

    Args:
        project_id (str):
        run_name (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[RunDB]
    """

    return sync_detailed(project_id=project_id, client=client, run_name=run_name).parsed


async def asyncio_detailed(
    project_id: str, *, client: ApiClient, run_name: None | str | Unset = UNSET
) -> Response[HTTPValidationError | list[RunDB]]:
    """Get Project Runs

     Gets all runs for a project.

    If a run_name is provided, gets the run with that name, or []

    Args:
        project_id (str):
        run_name (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[RunDB]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_name=run_name)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, *, client: ApiClient, run_name: None | str | Unset = UNSET
) -> Optional[HTTPValidationError | list[RunDB]]:
    """Get Project Runs

     Gets all runs for a project.

    If a run_name is provided, gets the run with that name, or []

    Args:
        project_id (str):
        run_name (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[RunDB]
    """

    return (await asyncio_detailed(project_id=project_id, client=client, run_name=run_name)).parsed
