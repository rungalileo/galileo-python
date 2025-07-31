from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.http_validation_error import HTTPValidationError
from ...models.list_group_collaborators_response import ListGroupCollaboratorsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str, *, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["starting_token"] = starting_token

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": f"/projects/{project_id}/groups",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[Union[HTTPValidationError, ListGroupCollaboratorsResponse]]:
    if response.status_code == 200:
        response_200 = ListGroupCollaboratorsResponse.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[Union[HTTPValidationError, ListGroupCollaboratorsResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, *, client: ApiClient, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> Response[Union[HTTPValidationError, ListGroupCollaboratorsResponse]]:
    """List Group Project Collaborators

     List the groups with which the project has been shared.

    Args:
        project_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListGroupCollaboratorsResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, starting_token=starting_token, limit=limit)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, *, client: ApiClient, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> Optional[Union[HTTPValidationError, ListGroupCollaboratorsResponse]]:
    """List Group Project Collaborators

     List the groups with which the project has been shared.

    Args:
        project_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListGroupCollaboratorsResponse]
    """

    return sync_detailed(project_id=project_id, client=client, starting_token=starting_token, limit=limit).parsed


async def asyncio_detailed(
    project_id: str, *, client: ApiClient, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> Response[Union[HTTPValidationError, ListGroupCollaboratorsResponse]]:
    """List Group Project Collaborators

     List the groups with which the project has been shared.

    Args:
        project_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListGroupCollaboratorsResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, starting_token=starting_token, limit=limit)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, *, client: ApiClient, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> Optional[Union[HTTPValidationError, ListGroupCollaboratorsResponse]]:
    """List Group Project Collaborators

     List the groups with which the project has been shared.

    Args:
        project_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListGroupCollaboratorsResponse]
    """

    return (
        await asyncio_detailed(project_id=project_id, client=client, starting_token=starting_token, limit=limit)
    ).parsed
