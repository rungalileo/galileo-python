from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.collaborator_update import CollaboratorUpdate
from ...models.http_validation_error import HTTPValidationError
from ...models.user_collaborator import UserCollaborator
from ...types import Response


def _get_kwargs(dataset_id: str, user_id: str, *, body: CollaboratorUpdate) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": "patch", "url": f"/datasets/{dataset_id}/users/{user_id}"}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, UserCollaborator]]:
    if response.status_code == 200:
        response_200 = UserCollaborator.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, UserCollaborator]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_id: str, user_id: str, *, client: AuthenticatedClient, body: CollaboratorUpdate
) -> Response[Union[HTTPValidationError, UserCollaborator]]:
    """Update User Dataset Collaborator

     Update the sharing permissions of a user on a dataset.

    Args:
        dataset_id (str):
        user_id (str):
        body (CollaboratorUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UserCollaborator]]
    """

    kwargs = _get_kwargs(dataset_id=dataset_id, user_id=user_id, body=body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str, user_id: str, *, client: AuthenticatedClient, body: CollaboratorUpdate
) -> Optional[Union[HTTPValidationError, UserCollaborator]]:
    """Update User Dataset Collaborator

     Update the sharing permissions of a user on a dataset.

    Args:
        dataset_id (str):
        user_id (str):
        body (CollaboratorUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UserCollaborator]
    """

    return sync_detailed(dataset_id=dataset_id, user_id=user_id, client=client, body=body).parsed


async def asyncio_detailed(
    dataset_id: str, user_id: str, *, client: AuthenticatedClient, body: CollaboratorUpdate
) -> Response[Union[HTTPValidationError, UserCollaborator]]:
    """Update User Dataset Collaborator

     Update the sharing permissions of a user on a dataset.

    Args:
        dataset_id (str):
        user_id (str):
        body (CollaboratorUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UserCollaborator]]
    """

    kwargs = _get_kwargs(dataset_id=dataset_id, user_id=user_id, body=body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str, user_id: str, *, client: AuthenticatedClient, body: CollaboratorUpdate
) -> Optional[Union[HTTPValidationError, UserCollaborator]]:
    """Update User Dataset Collaborator

     Update the sharing permissions of a user on a dataset.

    Args:
        dataset_id (str):
        user_id (str):
        body (CollaboratorUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UserCollaborator]
    """

    return (await asyncio_detailed(dataset_id=dataset_id, user_id=user_id, client=client, body=body)).parsed
