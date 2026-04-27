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
from ...models.api_key_delete_response import ApiKeyDeleteResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(api_key_id: str) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.DELETE,
        "return_raw_response": True,
        "path": "/v2/users/api_keys/{api_key_id}".format(api_key_id=api_key_id),
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> ApiKeyDeleteResponse | HTTPValidationError:
    if response.status_code == 200:
        response_200 = ApiKeyDeleteResponse.from_dict(response.json())

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
) -> Response[ApiKeyDeleteResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(api_key_id: str, *, client: ApiClient) -> Response[ApiKeyDeleteResponse | HTTPValidationError]:
    """Delete Api Key

    Args:
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyDeleteResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(api_key_id=api_key_id)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(api_key_id: str, *, client: ApiClient) -> Optional[ApiKeyDeleteResponse | HTTPValidationError]:
    """Delete Api Key

    Args:
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyDeleteResponse | HTTPValidationError
    """

    return sync_detailed(api_key_id=api_key_id, client=client).parsed


async def asyncio_detailed(
    api_key_id: str, *, client: ApiClient
) -> Response[ApiKeyDeleteResponse | HTTPValidationError]:
    """Delete Api Key

    Args:
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiKeyDeleteResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(api_key_id=api_key_id)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(api_key_id: str, *, client: ApiClient) -> Optional[ApiKeyDeleteResponse | HTTPValidationError]:
    """Delete Api Key

    Args:
        api_key_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiKeyDeleteResponse | HTTPValidationError
    """

    return (await asyncio_detailed(api_key_id=api_key_id, client=client)).parsed
