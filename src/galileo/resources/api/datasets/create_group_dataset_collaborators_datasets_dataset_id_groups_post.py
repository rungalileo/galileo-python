from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.group_collaborator import GroupCollaborator
from ...models.group_collaborator_create import GroupCollaboratorCreate
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(dataset_id: str, *, body: list["GroupCollaboratorCreate"]) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": "post", "url": f"/datasets/{dataset_id}/groups"}

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
) -> Optional[Union[HTTPValidationError, list["GroupCollaborator"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GroupCollaborator.from_dict(response_200_item_data)

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
) -> Response[Union[HTTPValidationError, list["GroupCollaborator"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_id: str, *, client: AuthenticatedClient, body: list["GroupCollaboratorCreate"]
) -> Response[Union[HTTPValidationError, list["GroupCollaborator"]]]:
    """Create Group Dataset Collaborators

     Share a dataset with groups.

    Args:
        dataset_id (str):
        body (list['GroupCollaboratorCreate']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['GroupCollaborator']]]
    """

    kwargs = _get_kwargs(dataset_id=dataset_id, body=body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str, *, client: AuthenticatedClient, body: list["GroupCollaboratorCreate"]
) -> Optional[Union[HTTPValidationError, list["GroupCollaborator"]]]:
    """Create Group Dataset Collaborators

     Share a dataset with groups.

    Args:
        dataset_id (str):
        body (list['GroupCollaboratorCreate']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['GroupCollaborator']]
    """

    return sync_detailed(dataset_id=dataset_id, client=client, body=body).parsed


async def asyncio_detailed(
    dataset_id: str, *, client: AuthenticatedClient, body: list["GroupCollaboratorCreate"]
) -> Response[Union[HTTPValidationError, list["GroupCollaborator"]]]:
    """Create Group Dataset Collaborators

     Share a dataset with groups.

    Args:
        dataset_id (str):
        body (list['GroupCollaboratorCreate']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['GroupCollaborator']]]
    """

    kwargs = _get_kwargs(dataset_id=dataset_id, body=body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str, *, client: AuthenticatedClient, body: list["GroupCollaboratorCreate"]
) -> Optional[Union[HTTPValidationError, list["GroupCollaborator"]]]:
    """Create Group Dataset Collaborators

     Share a dataset with groups.

    Args:
        dataset_id (str):
        body (list['GroupCollaboratorCreate']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['GroupCollaborator']]
    """

    return (await asyncio_detailed(dataset_id=dataset_id, client=client, body=body)).parsed
