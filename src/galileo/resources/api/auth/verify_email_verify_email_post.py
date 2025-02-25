from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.email_verification_request import EmailVerificationRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.token import Token
from ...types import UNSET, Response


def _get_kwargs(*, body: EmailVerificationRequest, verification_token: str) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["verification_token"] = verification_token

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "post", "url": "/verify_email", "params": params}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, Token]]:
    if response.status_code == 200:
        response_200 = Token.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, Token]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: Union[AuthenticatedClient, Client], body: EmailVerificationRequest, verification_token: str
) -> Response[Union[HTTPValidationError, Token]]:
    """Verify Email

    Args:
        verification_token (str):
        body (EmailVerificationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Token]]
    """

    kwargs = _get_kwargs(body=body, verification_token=verification_token)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: Union[AuthenticatedClient, Client], body: EmailVerificationRequest, verification_token: str
) -> Optional[Union[HTTPValidationError, Token]]:
    """Verify Email

    Args:
        verification_token (str):
        body (EmailVerificationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Token]
    """

    return sync_detailed(client=client, body=body, verification_token=verification_token).parsed


async def asyncio_detailed(
    *, client: Union[AuthenticatedClient, Client], body: EmailVerificationRequest, verification_token: str
) -> Response[Union[HTTPValidationError, Token]]:
    """Verify Email

    Args:
        verification_token (str):
        body (EmailVerificationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Token]]
    """

    kwargs = _get_kwargs(body=body, verification_token=verification_token)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: Union[AuthenticatedClient, Client], body: EmailVerificationRequest, verification_token: str
) -> Optional[Union[HTTPValidationError, Token]]:
    """Verify Email

    Args:
        verification_token (str):
        body (EmailVerificationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Token]
    """

    return (await asyncio_detailed(client=client, body=body, verification_token=verification_token)).parsed
