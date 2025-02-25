from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.project_db_thin import ProjectDBThin
from ...models.project_type import ProjectType
from ...types import UNSET, Response, Unset


def _get_kwargs(*, type_: Union[None, ProjectType, Unset] = UNSET) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_type_: Union[None, Unset, str]
    if isinstance(type_, Unset):
        json_type_ = UNSET
    elif isinstance(type_, ProjectType):
        json_type_ = type_.value
    else:
        json_type_ = type_
    params["type"] = json_type_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "get", "url": "/projects/all", "params": params}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["ProjectDBThin"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ProjectDBThin.from_dict(response_200_item_data)

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
) -> Response[Union[HTTPValidationError, list["ProjectDBThin"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, type_: Union[None, ProjectType, Unset] = UNSET
) -> Response[Union[HTTPValidationError, list["ProjectDBThin"]]]:
    """Get All Projects

     Gets all public projects and all private projects that the user has access to.

    For Enterprise SaaS Clusters, this will return all projects in the cluster.

    DEPRECATED in favor of `get_projects_paginated`.

    Args:
        type_ (Union[None, ProjectType, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['ProjectDBThin']]]
    """

    kwargs = _get_kwargs(type_=type_)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient, type_: Union[None, ProjectType, Unset] = UNSET
) -> Optional[Union[HTTPValidationError, list["ProjectDBThin"]]]:
    """Get All Projects

     Gets all public projects and all private projects that the user has access to.

    For Enterprise SaaS Clusters, this will return all projects in the cluster.

    DEPRECATED in favor of `get_projects_paginated`.

    Args:
        type_ (Union[None, ProjectType, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['ProjectDBThin']]
    """

    return sync_detailed(client=client, type_=type_).parsed


async def asyncio_detailed(
    *, client: AuthenticatedClient, type_: Union[None, ProjectType, Unset] = UNSET
) -> Response[Union[HTTPValidationError, list["ProjectDBThin"]]]:
    """Get All Projects

     Gets all public projects and all private projects that the user has access to.

    For Enterprise SaaS Clusters, this will return all projects in the cluster.

    DEPRECATED in favor of `get_projects_paginated`.

    Args:
        type_ (Union[None, ProjectType, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['ProjectDBThin']]]
    """

    kwargs = _get_kwargs(type_=type_)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, type_: Union[None, ProjectType, Unset] = UNSET
) -> Optional[Union[HTTPValidationError, list["ProjectDBThin"]]]:
    """Get All Projects

     Gets all public projects and all private projects that the user has access to.

    For Enterprise SaaS Clusters, this will return all projects in the cluster.

    DEPRECATED in favor of `get_projects_paginated`.

    Args:
        type_ (Union[None, ProjectType, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['ProjectDBThin']]
    """

    return (await asyncio_detailed(client=client, type_=type_)).parsed
