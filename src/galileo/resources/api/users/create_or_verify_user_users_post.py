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
from ...models.system_user_db import SystemUserDB
from ...models.user_create import UserCreate
from ...types import UNSET, Response, Unset


def _get_kwargs(*, body: UserCreate, signup_token: None | str | Unset = UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_signup_token: None | str | Unset
    if isinstance(signup_token, Unset):
        json_signup_token = UNSET
    else:
        json_signup_token = signup_token
    params["signup_token"] = json_signup_token

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/users",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | SystemUserDB:
    if response.status_code == 200:
        response_200 = SystemUserDB.from_dict(response.json())

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


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[HTTPValidationError | SystemUserDB]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, body: UserCreate, signup_token: None | str | Unset = UNSET
) -> Response[HTTPValidationError | SystemUserDB]:
    """Create Or Verify User

     Create a new system user with an email and password.

    If no admin exists (first user), the user will be created as an admin.

    Otherwise:
    - User record was already created when the admin invited the user
    - We should verify the user's email

    Args:
        signup_token (None | str | Unset):
        body (UserCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SystemUserDB]
    """

    kwargs = _get_kwargs(body=body, signup_token=signup_token)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, body: UserCreate, signup_token: None | str | Unset = UNSET
) -> Optional[HTTPValidationError | SystemUserDB]:
    """Create Or Verify User

     Create a new system user with an email and password.

    If no admin exists (first user), the user will be created as an admin.

    Otherwise:
    - User record was already created when the admin invited the user
    - We should verify the user's email

    Args:
        signup_token (None | str | Unset):
        body (UserCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SystemUserDB
    """

    return sync_detailed(client=client, body=body, signup_token=signup_token).parsed


async def asyncio_detailed(
    *, client: ApiClient, body: UserCreate, signup_token: None | str | Unset = UNSET
) -> Response[HTTPValidationError | SystemUserDB]:
    """Create Or Verify User

     Create a new system user with an email and password.

    If no admin exists (first user), the user will be created as an admin.

    Otherwise:
    - User record was already created when the admin invited the user
    - We should verify the user's email

    Args:
        signup_token (None | str | Unset):
        body (UserCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SystemUserDB]
    """

    kwargs = _get_kwargs(body=body, signup_token=signup_token)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, body: UserCreate, signup_token: None | str | Unset = UNSET
) -> Optional[HTTPValidationError | SystemUserDB]:
    """Create Or Verify User

     Create a new system user with an email and password.

    If no admin exists (first user), the user will be created as an admin.

    Otherwise:
    - User record was already created when the admin invited the user
    - We should verify the user's email

    Args:
        signup_token (None | str | Unset):
        body (UserCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SystemUserDB
    """

    return (await asyncio_detailed(client=client, body=body, signup_token=signup_token)).parsed
