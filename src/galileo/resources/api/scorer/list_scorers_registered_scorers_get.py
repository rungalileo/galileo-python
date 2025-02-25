from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_registered_scorers_response import ListRegisteredScorersResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(*, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["starting_token"] = starting_token

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "get", "url": "/registered-scorers", "params": params}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ListRegisteredScorersResponse]]:
    if response.status_code == 200:
        response_200 = ListRegisteredScorersResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ListRegisteredScorersResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> Response[Union[HTTPValidationError, ListRegisteredScorersResponse]]:
    """List Scorers

    Args:
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListRegisteredScorersResponse]]
    """

    kwargs = _get_kwargs(starting_token=starting_token, limit=limit)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> Optional[Union[HTTPValidationError, ListRegisteredScorersResponse]]:
    """List Scorers

    Args:
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListRegisteredScorersResponse]
    """

    return sync_detailed(client=client, starting_token=starting_token, limit=limit).parsed


async def asyncio_detailed(
    *, client: AuthenticatedClient, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> Response[Union[HTTPValidationError, ListRegisteredScorersResponse]]:
    """List Scorers

    Args:
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListRegisteredScorersResponse]]
    """

    kwargs = _get_kwargs(starting_token=starting_token, limit=limit)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> Optional[Union[HTTPValidationError, ListRegisteredScorersResponse]]:
    """List Scorers

    Args:
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListRegisteredScorersResponse]
    """

    return (await asyncio_detailed(client=client, starting_token=starting_token, limit=limit)).parsed
