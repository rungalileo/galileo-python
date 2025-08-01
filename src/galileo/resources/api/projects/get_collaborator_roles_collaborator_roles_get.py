from http import HTTPStatus
from typing import Any, Optional

import httpx

from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.collaborator_role_info import CollaboratorRoleInfo
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": RequestMethod.GET, "return_raw_response": True, "path": "/collaborator_roles"}

    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Optional[list["CollaboratorRoleInfo"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = CollaboratorRoleInfo.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[list["CollaboratorRoleInfo"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(*, client: ApiClient) -> Response[list["CollaboratorRoleInfo"]]:
    """Get Collaborator Roles

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['CollaboratorRoleInfo']]
    """

    kwargs = _get_kwargs()

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(*, client: ApiClient) -> Optional[list["CollaboratorRoleInfo"]]:
    """Get Collaborator Roles

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CollaboratorRoleInfo']
    """

    return sync_detailed(client=client).parsed


async def asyncio_detailed(*, client: ApiClient) -> Response[list["CollaboratorRoleInfo"]]:
    """Get Collaborator Roles

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['CollaboratorRoleInfo']]
    """

    kwargs = _get_kwargs()

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(*, client: ApiClient) -> Optional[list["CollaboratorRoleInfo"]]:
    """Get Collaborator Roles

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['CollaboratorRoleInfo']
    """

    return (await asyncio_detailed(client=client)).parsed
