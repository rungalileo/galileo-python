from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.user_password_reset_request import UserPasswordResetRequest
from ...models.user_password_reset_response import UserPasswordResetResponse
from ...types import UNSET, Response


def _get_kwargs(*, body: UserPasswordResetRequest, reset_token: str) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["reset_token"] = reset_token

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "post", "url": "/password_reset", "params": params}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, UserPasswordResetResponse]]:
    if response.status_code == 200:
        response_200 = UserPasswordResetResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, UserPasswordResetResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: Union[AuthenticatedClient, Client], body: UserPasswordResetRequest, reset_token: str
) -> Response[Union[HTTPValidationError, UserPasswordResetResponse]]:
    """Password Reset

     Reset a user's password.

    A password reset with a valid token should always verify the user. (See default of
    UserPasswordResetRequest.email_is_verified is True)

    Args:
        reset_token (str):
        body (UserPasswordResetRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UserPasswordResetResponse]]
    """

    kwargs = _get_kwargs(body=body, reset_token=reset_token)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: Union[AuthenticatedClient, Client], body: UserPasswordResetRequest, reset_token: str
) -> Optional[Union[HTTPValidationError, UserPasswordResetResponse]]:
    """Password Reset

     Reset a user's password.

    A password reset with a valid token should always verify the user. (See default of
    UserPasswordResetRequest.email_is_verified is True)

    Args:
        reset_token (str):
        body (UserPasswordResetRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UserPasswordResetResponse]
    """

    return sync_detailed(client=client, body=body, reset_token=reset_token).parsed


async def asyncio_detailed(
    *, client: Union[AuthenticatedClient, Client], body: UserPasswordResetRequest, reset_token: str
) -> Response[Union[HTTPValidationError, UserPasswordResetResponse]]:
    """Password Reset

     Reset a user's password.

    A password reset with a valid token should always verify the user. (See default of
    UserPasswordResetRequest.email_is_verified is True)

    Args:
        reset_token (str):
        body (UserPasswordResetRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UserPasswordResetResponse]]
    """

    kwargs = _get_kwargs(body=body, reset_token=reset_token)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: Union[AuthenticatedClient, Client], body: UserPasswordResetRequest, reset_token: str
) -> Optional[Union[HTTPValidationError, UserPasswordResetResponse]]:
    """Password Reset

     Reset a user's password.

    A password reset with a valid token should always verify the user. (See default of
    UserPasswordResetRequest.email_is_verified is True)

    Args:
        reset_token (str):
        body (UserPasswordResetRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UserPasswordResetResponse]
    """

    return (await asyncio_detailed(client=client, body=body, reset_token=reset_token)).parsed
