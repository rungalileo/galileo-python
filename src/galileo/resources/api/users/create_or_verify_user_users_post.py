from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_user_response import CreateUserResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.user_create import UserCreate
from ...types import UNSET, Response, Unset


def _get_kwargs(*, body: UserCreate, signup_token: Union[None, Unset, str] = UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_signup_token: Union[None, Unset, str]
    if isinstance(signup_token, Unset):
        json_signup_token = UNSET
    else:
        json_signup_token = signup_token
    params["signup_token"] = json_signup_token

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "post", "url": "/users", "params": params}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateUserResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = CreateUserResponse.from_dict(response.json())

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
) -> Response[Union[CreateUserResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: Union[AuthenticatedClient, Client], body: UserCreate, signup_token: Union[None, Unset, str] = UNSET
) -> Response[Union[CreateUserResponse, HTTPValidationError]]:
    """Create Or Verify User

     Create a new user with an email and password.

    If no admin exists (first user), the user will be created as an admin.

    Otherwise:
    - User record was already created when the admin invited the user
    - We should verify the user's email

    Args:
        signup_token (Union[None, Unset, str]):
        body (UserCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateUserResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(body=body, signup_token=signup_token)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: Union[AuthenticatedClient, Client], body: UserCreate, signup_token: Union[None, Unset, str] = UNSET
) -> Optional[Union[CreateUserResponse, HTTPValidationError]]:
    """Create Or Verify User

     Create a new user with an email and password.

    If no admin exists (first user), the user will be created as an admin.

    Otherwise:
    - User record was already created when the admin invited the user
    - We should verify the user's email

    Args:
        signup_token (Union[None, Unset, str]):
        body (UserCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateUserResponse, HTTPValidationError]
    """

    return sync_detailed(client=client, body=body, signup_token=signup_token).parsed


async def asyncio_detailed(
    *, client: Union[AuthenticatedClient, Client], body: UserCreate, signup_token: Union[None, Unset, str] = UNSET
) -> Response[Union[CreateUserResponse, HTTPValidationError]]:
    """Create Or Verify User

     Create a new user with an email and password.

    If no admin exists (first user), the user will be created as an admin.

    Otherwise:
    - User record was already created when the admin invited the user
    - We should verify the user's email

    Args:
        signup_token (Union[None, Unset, str]):
        body (UserCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateUserResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(body=body, signup_token=signup_token)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: Union[AuthenticatedClient, Client], body: UserCreate, signup_token: Union[None, Unset, str] = UNSET
) -> Optional[Union[CreateUserResponse, HTTPValidationError]]:
    """Create Or Verify User

     Create a new user with an email and password.

    If no admin exists (first user), the user will be created as an admin.

    Otherwise:
    - User record was already created when the admin invited the user
    - We should verify the user's email

    Args:
        signup_token (Union[None, Unset, str]):
        body (UserCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateUserResponse, HTTPValidationError]
    """

    return (await asyncio_detailed(client=client, body=body, signup_token=signup_token)).parsed
