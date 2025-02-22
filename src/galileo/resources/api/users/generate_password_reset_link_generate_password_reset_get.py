from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.password_reset_response import PasswordResetResponse
from ...types import UNSET, Response


def _get_kwargs(*, user_email: str) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["user_email"] = user_email

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "get", "url": "/generate_password_reset", "params": params}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PasswordResetResponse]]:
    if response.status_code == 200:
        response_200 = PasswordResetResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, PasswordResetResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, user_email: str
) -> Response[Union[HTTPValidationError, PasswordResetResponse]]:
    """Generate Password Reset Link

    Args:
        user_email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PasswordResetResponse]]
    """

    kwargs = _get_kwargs(user_email=user_email)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient, user_email: str
) -> Optional[Union[HTTPValidationError, PasswordResetResponse]]:
    """Generate Password Reset Link

    Args:
        user_email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PasswordResetResponse]
    """

    return sync_detailed(client=client, user_email=user_email).parsed


async def asyncio_detailed(
    *, client: AuthenticatedClient, user_email: str
) -> Response[Union[HTTPValidationError, PasswordResetResponse]]:
    """Generate Password Reset Link

    Args:
        user_email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PasswordResetResponse]]
    """

    kwargs = _get_kwargs(user_email=user_email)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, user_email: str
) -> Optional[Union[HTTPValidationError, PasswordResetResponse]]:
    """Generate Password Reset Link

    Args:
        user_email (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PasswordResetResponse]
    """

    return (await asyncio_detailed(client=client, user_email=user_email)).parsed
