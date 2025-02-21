from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.integration_name import IntegrationName
from ...types import Response


def _get_kwargs(name: IntegrationName) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "delete", "url": f"/integrations/{name}"}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = response.json()
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
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(name: IntegrationName, *, client: AuthenticatedClient) -> Response[Union[Any, HTTPValidationError]]:
    """Delete Integration

     Delete the integration created by this user.

    Args:
        name (IntegrationName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(name=name)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(name: IntegrationName, *, client: AuthenticatedClient) -> Optional[Union[Any, HTTPValidationError]]:
    """Delete Integration

     Delete the integration created by this user.

    Args:
        name (IntegrationName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(name=name, client=client).parsed


async def asyncio_detailed(
    name: IntegrationName, *, client: AuthenticatedClient
) -> Response[Union[Any, HTTPValidationError]]:
    """Delete Integration

     Delete the integration created by this user.

    Args:
        name (IntegrationName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(name=name)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(name: IntegrationName, *, client: AuthenticatedClient) -> Optional[Union[Any, HTTPValidationError]]:
    """Delete Integration

     Delete the integration created by this user.

    Args:
        name (IntegrationName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (await asyncio_detailed(name=name, client=client)).parsed
