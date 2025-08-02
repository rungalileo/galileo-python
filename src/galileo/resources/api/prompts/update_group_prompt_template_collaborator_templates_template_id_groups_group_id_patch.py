from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.collaborator_update import CollaboratorUpdate
from ...models.group_collaborator import GroupCollaborator
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(template_id: str, group_id: str, *, body: CollaboratorUpdate) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.PATCH,
        "return_raw_response": True,
        "path": f"/templates/{template_id}/groups/{group_id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[Union[GroupCollaborator, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GroupCollaborator.from_dict(response.json())

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
) -> Response[Union[GroupCollaborator, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    template_id: str, group_id: str, *, client: ApiClient, body: CollaboratorUpdate
) -> Response[Union[GroupCollaborator, HTTPValidationError]]:
    """Update Group Prompt Template Collaborator

     Update the sharing permissions of a group on a prompt template.

    Args:
        template_id (str):
        group_id (str):
        body (CollaboratorUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GroupCollaborator, HTTPValidationError]]
    """

    kwargs = _get_kwargs(template_id=template_id, group_id=group_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    template_id: str, group_id: str, *, client: ApiClient, body: CollaboratorUpdate
) -> Optional[Union[GroupCollaborator, HTTPValidationError]]:
    """Update Group Prompt Template Collaborator

     Update the sharing permissions of a group on a prompt template.

    Args:
        template_id (str):
        group_id (str):
        body (CollaboratorUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GroupCollaborator, HTTPValidationError]
    """

    return sync_detailed(template_id=template_id, group_id=group_id, client=client, body=body).parsed


async def asyncio_detailed(
    template_id: str, group_id: str, *, client: ApiClient, body: CollaboratorUpdate
) -> Response[Union[GroupCollaborator, HTTPValidationError]]:
    """Update Group Prompt Template Collaborator

     Update the sharing permissions of a group on a prompt template.

    Args:
        template_id (str):
        group_id (str):
        body (CollaboratorUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GroupCollaborator, HTTPValidationError]]
    """

    kwargs = _get_kwargs(template_id=template_id, group_id=group_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    template_id: str, group_id: str, *, client: ApiClient, body: CollaboratorUpdate
) -> Optional[Union[GroupCollaborator, HTTPValidationError]]:
    """Update Group Prompt Template Collaborator

     Update the sharing permissions of a group on a prompt template.

    Args:
        template_id (str):
        group_id (str):
        body (CollaboratorUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GroupCollaborator, HTTPValidationError]
    """

    return (await asyncio_detailed(template_id=template_id, group_id=group_id, client=client, body=body)).parsed
