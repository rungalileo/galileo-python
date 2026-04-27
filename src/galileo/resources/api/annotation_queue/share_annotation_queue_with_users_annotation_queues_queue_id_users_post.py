from http import HTTPStatus
from typing import Any, Optional

import httpx

from galileo.exceptions import (
    AuthenticationError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from galileo.utils.headers_data import get_sdk_header
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.annotation_queue_user_collaborator_create import AnnotationQueueUserCollaboratorCreate
from ...models.http_validation_error import HTTPValidationError
from ...models.user_annotation_queue_collaborator import UserAnnotationQueueCollaborator
from ...types import Response


def _get_kwargs(queue_id: str, *, body: list[AnnotationQueueUserCollaboratorCreate]) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/annotation_queues/{queue_id}/users".format(queue_id=queue_id),
    }

    _kwargs["json"] = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _kwargs["json"].append(body_item)

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> HTTPValidationError | list[UserAnnotationQueueCollaborator]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UserAnnotationQueueCollaborator.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    # Handle common HTTP errors with actionable messages
    if response.status_code == 400:
        raise BadRequestError(response.status_code, response.content)
    if response.status_code == 401:
        raise AuthenticationError(response.status_code, response.content)
    if response.status_code == 403:
        raise ForbiddenError(response.status_code, response.content)
    if response.status_code == 404:
        raise NotFoundError(response.status_code, response.content)
    if response.status_code == 409:
        raise ConflictError(response.status_code, response.content)
    if response.status_code == 429:
        raise RateLimitError(response.status_code, response.content)
    if response.status_code >= 500:
        raise ServerError(response.status_code, response.content)
    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[HTTPValidationError | list[UserAnnotationQueueCollaborator]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    queue_id: str, *, client: ApiClient, body: list[AnnotationQueueUserCollaboratorCreate]
) -> Response[HTTPValidationError | list[UserAnnotationQueueCollaborator]]:
    """Share Annotation Queue With Users

     Share an annotation queue with users by granting them specific roles.

    Users can be specified by user_id or email. If using email and the user doesn't exist
    in the organization, they will be invited automatically with the 'user' role.

    Roles: owner, annotator

    Args:
        queue_id (str):
        body (list[AnnotationQueueUserCollaboratorCreate]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[UserAnnotationQueueCollaborator]]
    """

    kwargs = _get_kwargs(queue_id=queue_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    queue_id: str, *, client: ApiClient, body: list[AnnotationQueueUserCollaboratorCreate]
) -> Optional[HTTPValidationError | list[UserAnnotationQueueCollaborator]]:
    """Share Annotation Queue With Users

     Share an annotation queue with users by granting them specific roles.

    Users can be specified by user_id or email. If using email and the user doesn't exist
    in the organization, they will be invited automatically with the 'user' role.

    Roles: owner, annotator

    Args:
        queue_id (str):
        body (list[AnnotationQueueUserCollaboratorCreate]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[UserAnnotationQueueCollaborator]
    """

    return sync_detailed(queue_id=queue_id, client=client, body=body).parsed


async def asyncio_detailed(
    queue_id: str, *, client: ApiClient, body: list[AnnotationQueueUserCollaboratorCreate]
) -> Response[HTTPValidationError | list[UserAnnotationQueueCollaborator]]:
    """Share Annotation Queue With Users

     Share an annotation queue with users by granting them specific roles.

    Users can be specified by user_id or email. If using email and the user doesn't exist
    in the organization, they will be invited automatically with the 'user' role.

    Roles: owner, annotator

    Args:
        queue_id (str):
        body (list[AnnotationQueueUserCollaboratorCreate]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[UserAnnotationQueueCollaborator]]
    """

    kwargs = _get_kwargs(queue_id=queue_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    queue_id: str, *, client: ApiClient, body: list[AnnotationQueueUserCollaboratorCreate]
) -> Optional[HTTPValidationError | list[UserAnnotationQueueCollaborator]]:
    """Share Annotation Queue With Users

     Share an annotation queue with users by granting them specific roles.

    Users can be specified by user_id or email. If using email and the user doesn't exist
    in the organization, they will be invited automatically with the 'user' role.

    Roles: owner, annotator

    Args:
        queue_id (str):
        body (list[AnnotationQueueUserCollaboratorCreate]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[UserAnnotationQueueCollaborator]
    """

    return (await asyncio_detailed(queue_id=queue_id, client=client, body=body)).parsed
