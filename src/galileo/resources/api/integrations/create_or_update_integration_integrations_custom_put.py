from http import HTTPStatus
from typing import Any, Optional, Union

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
from ...models.custom_integration_create import CustomIntegrationCreate
from ...models.http_validation_error import HTTPValidationError
from ...models.integration_db import IntegrationDB
from ...types import Response


def _get_kwargs(*, body: CustomIntegrationCreate) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": RequestMethod.PUT, "return_raw_response": True, "path": "/integrations/custom"}

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Union[HTTPValidationError, IntegrationDB]:
    if response.status_code == 200:
        return IntegrationDB.from_dict(response.json())

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, IntegrationDB]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, body: CustomIntegrationCreate
) -> Response[Union[HTTPValidationError, IntegrationDB]]:
    """Create Or Update Integration.

    Args:
        body (CustomIntegrationCreate): Schema for creating custom integrations.

            Inherits api_key field validation from CustomConfig:
            - api_key_header and api_key_value are required when authentication_type is api_key

            Token field is only used for oauth2 authentication (contains OAuth2 client credentials).
            For api_key auth, the api_key_value field is used instead.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, IntegrationDB]]
    """
    kwargs = _get_kwargs(body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(*, client: ApiClient, body: CustomIntegrationCreate) -> Optional[Union[HTTPValidationError, IntegrationDB]]:
    """Create Or Update Integration.

    Args:
        body (CustomIntegrationCreate): Schema for creating custom integrations.

            Inherits api_key field validation from CustomConfig:
            - api_key_header and api_key_value are required when authentication_type is api_key

            Token field is only used for oauth2 authentication (contains OAuth2 client credentials).
            For api_key auth, the api_key_value field is used instead.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, IntegrationDB]
    """
    return sync_detailed(client=client, body=body).parsed


async def asyncio_detailed(
    *, client: ApiClient, body: CustomIntegrationCreate
) -> Response[Union[HTTPValidationError, IntegrationDB]]:
    """Create Or Update Integration.

    Args:
        body (CustomIntegrationCreate): Schema for creating custom integrations.

            Inherits api_key field validation from CustomConfig:
            - api_key_header and api_key_value are required when authentication_type is api_key

            Token field is only used for oauth2 authentication (contains OAuth2 client credentials).
            For api_key auth, the api_key_value field is used instead.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, IntegrationDB]]
    """
    kwargs = _get_kwargs(body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, body: CustomIntegrationCreate
) -> Optional[Union[HTTPValidationError, IntegrationDB]]:
    """Create Or Update Integration.

    Args:
        body (CustomIntegrationCreate): Schema for creating custom integrations.

            Inherits api_key field validation from CustomConfig:
            - api_key_header and api_key_value are required when authentication_type is api_key

            Token field is only used for oauth2 authentication (contains OAuth2 client credentials).
            For api_key auth, the api_key_value field is used instead.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, IntegrationDB]
    """
    return (await asyncio_detailed(client=client, body=body)).parsed
