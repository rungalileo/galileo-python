from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.group_member_create import GroupMemberCreate
from ...models.group_member_db import GroupMemberDB
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(group_id: str, *, body: list["GroupMemberCreate"]) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": "post", "url": f"/groups/{group_id}/members"}

    _body = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _body.append(body_item)

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["GroupMemberDB"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GroupMemberDB.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[HTTPValidationError, list["GroupMemberDB"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: str, *, client: AuthenticatedClient, body: list["GroupMemberCreate"]
) -> Response[Union[HTTPValidationError, list["GroupMemberDB"]]]:
    """Add User To Group

    Args:
        group_id (str):
        body (list['GroupMemberCreate']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['GroupMemberDB']]]
    """

    kwargs = _get_kwargs(group_id=group_id, body=body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    group_id: str, *, client: AuthenticatedClient, body: list["GroupMemberCreate"]
) -> Optional[Union[HTTPValidationError, list["GroupMemberDB"]]]:
    """Add User To Group

    Args:
        group_id (str):
        body (list['GroupMemberCreate']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['GroupMemberDB']]
    """

    return sync_detailed(group_id=group_id, client=client, body=body).parsed


async def asyncio_detailed(
    group_id: str, *, client: AuthenticatedClient, body: list["GroupMemberCreate"]
) -> Response[Union[HTTPValidationError, list["GroupMemberDB"]]]:
    """Add User To Group

    Args:
        group_id (str):
        body (list['GroupMemberCreate']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['GroupMemberDB']]]
    """

    kwargs = _get_kwargs(group_id=group_id, body=body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: str, *, client: AuthenticatedClient, body: list["GroupMemberCreate"]
) -> Optional[Union[HTTPValidationError, list["GroupMemberDB"]]]:
    """Add User To Group

    Args:
        group_id (str):
        body (list['GroupMemberCreate']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['GroupMemberDB']]
    """

    return (await asyncio_detailed(group_id=group_id, client=client, body=body)).parsed
