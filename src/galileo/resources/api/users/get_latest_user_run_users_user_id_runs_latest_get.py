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
from ...models.get_user_latest_runs_db import GetUserLatestRunsDB
from ...models.http_validation_error import HTTPValidationError
from ...models.project_type import ProjectType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_id: str,
    *,
    project_type: ProjectType | Unset = UNSET,
    starting_token: int | Unset = 0,
    limit: int | Unset = 100,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_project_type: str | Unset = UNSET
    if not isinstance(project_type, Unset):
        json_project_type = project_type.value

    params["project_type"] = json_project_type

    params["starting_token"] = starting_token

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/users/{user_id}/runs/latest".format(user_id=user_id),
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> GetUserLatestRunsDB | HTTPValidationError:
    if response.status_code == 200:
        response_200 = GetUserLatestRunsDB.from_dict(response.json())

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


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[GetUserLatestRunsDB | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    *,
    client: ApiClient,
    project_type: ProjectType | Unset = UNSET,
    starting_token: int | Unset = 0,
    limit: int | Unset = 100,
) -> Response[GetUserLatestRunsDB | HTTPValidationError]:
    """Get Latest User Run

     Gets the most recent run for a User, ordered by last updated.

    Args:
        user_id (str):
        project_type (ProjectType | Unset):
        starting_token (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetUserLatestRunsDB | HTTPValidationError]
    """

    kwargs = _get_kwargs(user_id=user_id, project_type=project_type, starting_token=starting_token, limit=limit)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: ApiClient,
    project_type: ProjectType | Unset = UNSET,
    starting_token: int | Unset = 0,
    limit: int | Unset = 100,
) -> Optional[GetUserLatestRunsDB | HTTPValidationError]:
    """Get Latest User Run

     Gets the most recent run for a User, ordered by last updated.

    Args:
        user_id (str):
        project_type (ProjectType | Unset):
        starting_token (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetUserLatestRunsDB | HTTPValidationError
    """

    return sync_detailed(
        user_id=user_id, client=client, project_type=project_type, starting_token=starting_token, limit=limit
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: ApiClient,
    project_type: ProjectType | Unset = UNSET,
    starting_token: int | Unset = 0,
    limit: int | Unset = 100,
) -> Response[GetUserLatestRunsDB | HTTPValidationError]:
    """Get Latest User Run

     Gets the most recent run for a User, ordered by last updated.

    Args:
        user_id (str):
        project_type (ProjectType | Unset):
        starting_token (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetUserLatestRunsDB | HTTPValidationError]
    """

    kwargs = _get_kwargs(user_id=user_id, project_type=project_type, starting_token=starting_token, limit=limit)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: ApiClient,
    project_type: ProjectType | Unset = UNSET,
    starting_token: int | Unset = 0,
    limit: int | Unset = 100,
) -> Optional[GetUserLatestRunsDB | HTTPValidationError]:
    """Get Latest User Run

     Gets the most recent run for a User, ordered by last updated.

    Args:
        user_id (str):
        project_type (ProjectType | Unset):
        starting_token (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetUserLatestRunsDB | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            user_id=user_id, client=client, project_type=project_type, starting_token=starting_token, limit=limit
        )
    ).parsed
