from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_token_response import GetTokenResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(*, organization_id: Union[None, Unset, str] = UNSET) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_organization_id: Union[None, Unset, str]
    if isinstance(organization_id, Unset):
        json_organization_id = UNSET
    else:
        json_organization_id = organization_id
    params["organization_id"] = json_organization_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "get", "url": "/v2/token", "params": params}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetTokenResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GetTokenResponse.from_dict(response.json())

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
) -> Response[Union[GetTokenResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, organization_id: Union[None, Unset, str] = UNSET
) -> Response[Union[GetTokenResponse, HTTPValidationError]]:
    """Get Token

    Args:
        organization_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetTokenResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(organization_id=organization_id)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient, organization_id: Union[None, Unset, str] = UNSET
) -> Optional[Union[GetTokenResponse, HTTPValidationError]]:
    """Get Token

    Args:
        organization_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetTokenResponse, HTTPValidationError]
    """

    return sync_detailed(client=client, organization_id=organization_id).parsed


async def asyncio_detailed(
    *, client: AuthenticatedClient, organization_id: Union[None, Unset, str] = UNSET
) -> Response[Union[GetTokenResponse, HTTPValidationError]]:
    """Get Token

    Args:
        organization_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetTokenResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(organization_id=organization_id)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, organization_id: Union[None, Unset, str] = UNSET
) -> Optional[Union[GetTokenResponse, HTTPValidationError]]:
    """Get Token

    Args:
        organization_id (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetTokenResponse, HTTPValidationError]
    """

    return (await asyncio_detailed(client=client, organization_id=organization_id)).parsed
