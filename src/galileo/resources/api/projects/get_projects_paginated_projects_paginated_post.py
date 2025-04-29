from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_projects_paginated_response import GetProjectsPaginatedResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.project_action import ProjectAction
from ...models.project_collection_params import ProjectCollectionParams
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ProjectCollectionParams,
    actions: Union[Unset, list[ProjectAction]] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_actions: Union[Unset, list[str]] = UNSET
    if not isinstance(actions, Unset):
        json_actions = []
        for actions_item_data in actions:
            actions_item = actions_item_data.value
            json_actions.append(actions_item)

    params["actions"] = json_actions

    params["starting_token"] = starting_token

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "post", "url": "/projects/paginated", "params": params}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetProjectsPaginatedResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GetProjectsPaginatedResponse.from_dict(response.json())

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
) -> Response[Union[GetProjectsPaginatedResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ProjectCollectionParams,
    actions: Union[Unset, list[ProjectAction]] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[GetProjectsPaginatedResponse, HTTPValidationError]]:
    """Get Projects Paginated

     Gets projects for a user with pagination.

    If provided, filters on project_name and project_type.

    Args:
        actions (Union[Unset, list[ProjectAction]]): Actions to include in the 'permissions'
            field.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (ProjectCollectionParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetProjectsPaginatedResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(body=body, actions=actions, starting_token=starting_token, limit=limit)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ProjectCollectionParams,
    actions: Union[Unset, list[ProjectAction]] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[GetProjectsPaginatedResponse, HTTPValidationError]]:
    """Get Projects Paginated

     Gets projects for a user with pagination.

    If provided, filters on project_name and project_type.

    Args:
        actions (Union[Unset, list[ProjectAction]]): Actions to include in the 'permissions'
            field.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (ProjectCollectionParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetProjectsPaginatedResponse, HTTPValidationError]
    """

    return sync_detailed(client=client, body=body, actions=actions, starting_token=starting_token, limit=limit).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ProjectCollectionParams,
    actions: Union[Unset, list[ProjectAction]] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[GetProjectsPaginatedResponse, HTTPValidationError]]:
    """Get Projects Paginated

     Gets projects for a user with pagination.

    If provided, filters on project_name and project_type.

    Args:
        actions (Union[Unset, list[ProjectAction]]): Actions to include in the 'permissions'
            field.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (ProjectCollectionParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetProjectsPaginatedResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(body=body, actions=actions, starting_token=starting_token, limit=limit)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ProjectCollectionParams,
    actions: Union[Unset, list[ProjectAction]] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[GetProjectsPaginatedResponse, HTTPValidationError]]:
    """Get Projects Paginated

     Gets projects for a user with pagination.

    If provided, filters on project_name and project_type.

    Args:
        actions (Union[Unset, list[ProjectAction]]): Actions to include in the 'permissions'
            field.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (ProjectCollectionParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetProjectsPaginatedResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(client=client, body=body, actions=actions, starting_token=starting_token, limit=limit)
    ).parsed
