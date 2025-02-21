from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_signup_link_response import CreateSignupLinkResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(*, user_email: str, send_email: Union[Unset, bool] = True) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["user_email"] = user_email

    params["send_email"] = send_email

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "post", "url": "/signup_link", "params": params}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateSignupLinkResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = CreateSignupLinkResponse.from_dict(response.json())

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
) -> Response[Union[CreateSignupLinkResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, user_email: str, send_email: Union[Unset, bool] = True
) -> Response[Union[CreateSignupLinkResponse, HTTPValidationError]]:
    """Generate Signup Link

     Generate a signup link for a new user.

    This endpoint is used by admins in the console Command Center.
    We create an unverified user entry and send a signup email to the new user.

    The user is then verified via one of the following endpoints:
    - POST /users
    - POST /users/social

    Args:
        user_email (str):
        send_email (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateSignupLinkResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(user_email=user_email, send_email=send_email)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient, user_email: str, send_email: Union[Unset, bool] = True
) -> Optional[Union[CreateSignupLinkResponse, HTTPValidationError]]:
    """Generate Signup Link

     Generate a signup link for a new user.

    This endpoint is used by admins in the console Command Center.
    We create an unverified user entry and send a signup email to the new user.

    The user is then verified via one of the following endpoints:
    - POST /users
    - POST /users/social

    Args:
        user_email (str):
        send_email (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateSignupLinkResponse, HTTPValidationError]
    """

    return sync_detailed(client=client, user_email=user_email, send_email=send_email).parsed


async def asyncio_detailed(
    *, client: AuthenticatedClient, user_email: str, send_email: Union[Unset, bool] = True
) -> Response[Union[CreateSignupLinkResponse, HTTPValidationError]]:
    """Generate Signup Link

     Generate a signup link for a new user.

    This endpoint is used by admins in the console Command Center.
    We create an unverified user entry and send a signup email to the new user.

    The user is then verified via one of the following endpoints:
    - POST /users
    - POST /users/social

    Args:
        user_email (str):
        send_email (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateSignupLinkResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(user_email=user_email, send_email=send_email)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, user_email: str, send_email: Union[Unset, bool] = True
) -> Optional[Union[CreateSignupLinkResponse, HTTPValidationError]]:
    """Generate Signup Link

     Generate a signup link for a new user.

    This endpoint is used by admins in the console Command Center.
    We create an unverified user entry and send a signup email to the new user.

    The user is then verified via one of the following endpoints:
    - POST /users
    - POST /users/social

    Args:
        user_email (str):
        send_email (Union[Unset, bool]):  Default: True.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateSignupLinkResponse, HTTPValidationError]
    """

    return (await asyncio_detailed(client=client, user_email=user_email, send_email=send_email)).parsed
