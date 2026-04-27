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
from ...models.list_log_stream_response import ListLogStreamResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str, *, include_counts: bool | Unset = False, starting_token: int | Unset = 0, limit: int | Unset = 100
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["include_counts"] = include_counts

    params["starting_token"] = starting_token

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/v2/projects/{project_id}/log_streams/paginated".format(project_id=project_id),
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | ListLogStreamResponse:
    if response.status_code == 200:
        response_200 = ListLogStreamResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ListLogStreamResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: ApiClient,
    include_counts: bool | Unset = False,
    starting_token: int | Unset = 0,
    limit: int | Unset = 100,
) -> Response[HTTPValidationError | ListLogStreamResponse]:
    """List Log Streams Paginated

     Retrieve all log streams for a project paginated.

    Args:
        project_id (str):
        include_counts (bool | Unset):  Default: False.
        starting_token (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListLogStreamResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id, include_counts=include_counts, starting_token=starting_token, limit=limit
    )

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: ApiClient,
    include_counts: bool | Unset = False,
    starting_token: int | Unset = 0,
    limit: int | Unset = 100,
) -> Optional[HTTPValidationError | ListLogStreamResponse]:
    """List Log Streams Paginated

     Retrieve all log streams for a project paginated.

    Args:
        project_id (str):
        include_counts (bool | Unset):  Default: False.
        starting_token (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListLogStreamResponse
    """

    return sync_detailed(
        project_id=project_id, client=client, include_counts=include_counts, starting_token=starting_token, limit=limit
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: ApiClient,
    include_counts: bool | Unset = False,
    starting_token: int | Unset = 0,
    limit: int | Unset = 100,
) -> Response[HTTPValidationError | ListLogStreamResponse]:
    """List Log Streams Paginated

     Retrieve all log streams for a project paginated.

    Args:
        project_id (str):
        include_counts (bool | Unset):  Default: False.
        starting_token (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListLogStreamResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id, include_counts=include_counts, starting_token=starting_token, limit=limit
    )

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: ApiClient,
    include_counts: bool | Unset = False,
    starting_token: int | Unset = 0,
    limit: int | Unset = 100,
) -> Optional[HTTPValidationError | ListLogStreamResponse]:
    """List Log Streams Paginated

     Retrieve all log streams for a project paginated.

    Args:
        project_id (str):
        include_counts (bool | Unset):  Default: False.
        starting_token (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListLogStreamResponse
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            include_counts=include_counts,
            starting_token=starting_token,
            limit=limit,
        )
    ).parsed
