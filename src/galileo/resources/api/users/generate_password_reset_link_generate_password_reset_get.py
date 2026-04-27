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
from ...models.password_reset_response import PasswordResetResponse
from ...types import UNSET, Response


def _get_kwargs(*, user_email: str) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["user_email"] = user_email

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/generate_password_reset",
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | PasswordResetResponse:
    if response.status_code == 200:
        response_200 = PasswordResetResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | PasswordResetResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(*, client: ApiClient, user_email: str) -> Response[HTTPValidationError | PasswordResetResponse]:
    """Generate Password Reset Link

    Args:
        user_email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PasswordResetResponse]
    """

    kwargs = _get_kwargs(user_email=user_email)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(*, client: ApiClient, user_email: str) -> Optional[HTTPValidationError | PasswordResetResponse]:
    """Generate Password Reset Link

    Args:
        user_email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PasswordResetResponse
    """

    return sync_detailed(client=client, user_email=user_email).parsed


async def asyncio_detailed(
    *, client: ApiClient, user_email: str
) -> Response[HTTPValidationError | PasswordResetResponse]:
    """Generate Password Reset Link

    Args:
        user_email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PasswordResetResponse]
    """

    kwargs = _get_kwargs(user_email=user_email)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(*, client: ApiClient, user_email: str) -> Optional[HTTPValidationError | PasswordResetResponse]:
    """Generate Password Reset Link

    Args:
        user_email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PasswordResetResponse
    """

    return (await asyncio_detailed(client=client, user_email=user_email)).parsed
