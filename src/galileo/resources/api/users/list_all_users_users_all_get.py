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
from ...models.get_user_response import GetUserResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": RequestMethod.GET, "return_raw_response": True, "path": "/users/all"}

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> list[GetUserResponse]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetUserResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

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


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[list[GetUserResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(*, client: ApiClient) -> Response[list[GetUserResponse]]:
    r"""List All Users

     List all users in the system.

    This endpoint is optimized to count project and runs for each user. This endpoint must be placed
    before
    `/users/{user_id}` so that \"all\" is not interpreted as a UUID4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[GetUserResponse]]
    """

    kwargs = _get_kwargs()

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(*, client: ApiClient) -> Optional[list[GetUserResponse]]:
    r"""List All Users

     List all users in the system.

    This endpoint is optimized to count project and runs for each user. This endpoint must be placed
    before
    `/users/{user_id}` so that \"all\" is not interpreted as a UUID4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[GetUserResponse]
    """

    return sync_detailed(client=client).parsed


async def asyncio_detailed(*, client: ApiClient) -> Response[list[GetUserResponse]]:
    r"""List All Users

     List all users in the system.

    This endpoint is optimized to count project and runs for each user. This endpoint must be placed
    before
    `/users/{user_id}` so that \"all\" is not interpreted as a UUID4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[GetUserResponse]]
    """

    kwargs = _get_kwargs()

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(*, client: ApiClient) -> Optional[list[GetUserResponse]]:
    r"""List All Users

     List all users in the system.

    This endpoint is optimized to count project and runs for each user. This endpoint must be placed
    before
    `/users/{user_id}` so that \"all\" is not interpreted as a UUID4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[GetUserResponse]
    """

    return (await asyncio_detailed(client=client)).parsed
