from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_user_response import GetUserResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": "/users/all"}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[list["GetUserResponse"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetUserResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["GetUserResponse"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(*, client: AuthenticatedClient) -> Response[list["GetUserResponse"]]:
    r"""List All Users

     List all users in the system.

    This endpoint is optimized to count project and runs for each user. This endpoint must be placed
    before
    `/users/{user_id}` so that \"all\" is not interpreted as a UUID4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['GetUserResponse']]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(*, client: AuthenticatedClient) -> Optional[list["GetUserResponse"]]:
    r"""List All Users

     List all users in the system.

    This endpoint is optimized to count project and runs for each user. This endpoint must be placed
    before
    `/users/{user_id}` so that \"all\" is not interpreted as a UUID4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['GetUserResponse']
    """

    return sync_detailed(client=client).parsed


async def asyncio_detailed(*, client: AuthenticatedClient) -> Response[list["GetUserResponse"]]:
    r"""List All Users

     List all users in the system.

    This endpoint is optimized to count project and runs for each user. This endpoint must be placed
    before
    `/users/{user_id}` so that \"all\" is not interpreted as a UUID4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['GetUserResponse']]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(*, client: AuthenticatedClient) -> Optional[list["GetUserResponse"]]:
    r"""List All Users

     List all users in the system.

    This endpoint is optimized to count project and runs for each user. This endpoint must be placed
    before
    `/users/{user_id}` so that \"all\" is not interpreted as a UUID4.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['GetUserResponse']
    """

    return (await asyncio_detailed(client=client)).parsed
