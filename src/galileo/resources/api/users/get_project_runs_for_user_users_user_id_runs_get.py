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
from ...models.project_db import ProjectDB
from ...models.project_type import ProjectType
from ...types import UNSET, Response, Unset


def _get_kwargs(user_id: str, *, project_type: None | ProjectType | Unset = UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_project_type: None | str | Unset
    if isinstance(project_type, Unset):
        json_project_type = UNSET
    elif isinstance(project_type, ProjectType):
        json_project_type = project_type.value
    else:
        json_project_type = project_type
    params["project_type"] = json_project_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/users/{user_id}/runs".format(user_id=user_id),
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | list[ProjectDB]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ProjectDB.from_dict(response_200_item_data)

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


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[HTTPValidationError | list[ProjectDB]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str, *, client: ApiClient, project_type: None | ProjectType | Unset = UNSET
) -> Response[HTTPValidationError | list[ProjectDB]]:
    """Get Project Runs For User

     Get all user created runs across all projects they can access.

    This returns a filtered list of projects with only runs created by this user.

    Args:
        user_id (str):
        project_type (None | ProjectType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ProjectDB]]
    """

    kwargs = _get_kwargs(user_id=user_id, project_type=project_type)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    user_id: str, *, client: ApiClient, project_type: None | ProjectType | Unset = UNSET
) -> Optional[HTTPValidationError | list[ProjectDB]]:
    """Get Project Runs For User

     Get all user created runs across all projects they can access.

    This returns a filtered list of projects with only runs created by this user.

    Args:
        user_id (str):
        project_type (None | ProjectType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ProjectDB]
    """

    return sync_detailed(user_id=user_id, client=client, project_type=project_type).parsed


async def asyncio_detailed(
    user_id: str, *, client: ApiClient, project_type: None | ProjectType | Unset = UNSET
) -> Response[HTTPValidationError | list[ProjectDB]]:
    """Get Project Runs For User

     Get all user created runs across all projects they can access.

    This returns a filtered list of projects with only runs created by this user.

    Args:
        user_id (str):
        project_type (None | ProjectType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ProjectDB]]
    """

    kwargs = _get_kwargs(user_id=user_id, project_type=project_type)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str, *, client: ApiClient, project_type: None | ProjectType | Unset = UNSET
) -> Optional[HTTPValidationError | list[ProjectDB]]:
    """Get Project Runs For User

     Get all user created runs across all projects they can access.

    This returns a filtered list of projects with only runs created by this user.

    Args:
        user_id (str):
        project_type (None | ProjectType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ProjectDB]
    """

    return (await asyncio_detailed(user_id=user_id, client=client, project_type=project_type)).parsed
