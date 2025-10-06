from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.http_validation_error import HTTPValidationError
from ...models.project_db import ProjectDB
from ...models.project_type import ProjectType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, project_name: Union[None, Unset, str] = UNSET, type_: Union[None, ProjectType, Unset] = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_project_name: Union[None, Unset, str]
    json_project_name = UNSET if isinstance(project_name, Unset) else project_name
    params["project_name"] = json_project_name

    json_type_: Union[None, Unset, str]
    if isinstance(type_, Unset):
        json_type_ = UNSET
    elif isinstance(type_, ProjectType):
        json_type_ = type_.value
    else:
        json_type_ = type_
    params["type"] = json_type_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/projects",
        "params": params,
    }

    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["ProjectDB"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ProjectDB.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[Union[HTTPValidationError, list["ProjectDB"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, project_name: Union[None, Unset, str] = UNSET, type_: Union[None, ProjectType, Unset] = UNSET
) -> Response[Union[HTTPValidationError, list["ProjectDB"]]]:
    """Get Projects

     Gets projects for a user.

    If provided, filters on project_name and project_type.

    DEPRECATED in favor of `get_projects_paginated`.

    Args:
        project_name (Union[None, Unset, str]):
        type_ (Union[None, ProjectType, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['ProjectDB']]]
    """

    kwargs = _get_kwargs(project_name=project_name, type_=type_)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, project_name: Union[None, Unset, str] = UNSET, type_: Union[None, ProjectType, Unset] = UNSET
) -> Optional[Union[HTTPValidationError, list["ProjectDB"]]]:
    """Get Projects

     Gets projects for a user.

    If provided, filters on project_name and project_type.

    DEPRECATED in favor of `get_projects_paginated`.

    Args:
        project_name (Union[None, Unset, str]):
        type_ (Union[None, ProjectType, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['ProjectDB']]
    """

    return sync_detailed(client=client, project_name=project_name, type_=type_).parsed


async def asyncio_detailed(
    *, client: ApiClient, project_name: Union[None, Unset, str] = UNSET, type_: Union[None, ProjectType, Unset] = UNSET
) -> Response[Union[HTTPValidationError, list["ProjectDB"]]]:
    """Get Projects

     Gets projects for a user.

    If provided, filters on project_name and project_type.

    DEPRECATED in favor of `get_projects_paginated`.

    Args:
        project_name (Union[None, Unset, str]):
        type_ (Union[None, ProjectType, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['ProjectDB']]]
    """

    kwargs = _get_kwargs(project_name=project_name, type_=type_)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, project_name: Union[None, Unset, str] = UNSET, type_: Union[None, ProjectType, Unset] = UNSET
) -> Optional[Union[HTTPValidationError, list["ProjectDB"]]]:
    """Get Projects

     Gets projects for a user.

    If provided, filters on project_name and project_type.

    DEPRECATED in favor of `get_projects_paginated`.

    Args:
        project_name (Union[None, Unset, str]):
        type_ (Union[None, ProjectType, Unset]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['ProjectDB']]
    """

    return (await asyncio_detailed(client=client, project_name=project_name, type_=type_)).parsed
