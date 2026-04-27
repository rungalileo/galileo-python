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
from ...models.annotation_queue_response import AnnotationQueueResponse
from ...models.create_annotation_queue_request import CreateAnnotationQueueRequest
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(*, body: CreateAnnotationQueueRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": RequestMethod.POST, "return_raw_response": True, "path": "/annotation_queues"}

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> AnnotationQueueResponse | HTTPValidationError:
    if response.status_code == 200:
        response_200 = AnnotationQueueResponse.from_dict(response.json())

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
) -> Response[AnnotationQueueResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, body: CreateAnnotationQueueRequest
) -> Response[AnnotationQueueResponse | HTTPValidationError]:
    """Create Annotation Queue

     Create an annotation queue at the organization level.

    The creator will automatically be granted the 'owner' role.
    Optionally accepts a list of annotator emails. Users that don't exist in the organization will be
    invited.
    Optionally copies templates from an existing queue if copy_templates_from_queue_id is provided.

    Args:
        body (CreateAnnotationQueueRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnotationQueueResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, body: CreateAnnotationQueueRequest
) -> Optional[AnnotationQueueResponse | HTTPValidationError]:
    """Create Annotation Queue

     Create an annotation queue at the organization level.

    The creator will automatically be granted the 'owner' role.
    Optionally accepts a list of annotator emails. Users that don't exist in the organization will be
    invited.
    Optionally copies templates from an existing queue if copy_templates_from_queue_id is provided.

    Args:
        body (CreateAnnotationQueueRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnnotationQueueResponse | HTTPValidationError
    """

    return sync_detailed(client=client, body=body).parsed


async def asyncio_detailed(
    *, client: ApiClient, body: CreateAnnotationQueueRequest
) -> Response[AnnotationQueueResponse | HTTPValidationError]:
    """Create Annotation Queue

     Create an annotation queue at the organization level.

    The creator will automatically be granted the 'owner' role.
    Optionally accepts a list of annotator emails. Users that don't exist in the organization will be
    invited.
    Optionally copies templates from an existing queue if copy_templates_from_queue_id is provided.

    Args:
        body (CreateAnnotationQueueRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnnotationQueueResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, body: CreateAnnotationQueueRequest
) -> Optional[AnnotationQueueResponse | HTTPValidationError]:
    """Create Annotation Queue

     Create an annotation queue at the organization level.

    The creator will automatically be granted the 'owner' role.
    Optionally accepts a list of annotator emails. Users that don't exist in the organization will be
    invited.
    Optionally copies templates from an existing queue if copy_templates_from_queue_id is provided.

    Args:
        body (CreateAnnotationQueueRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnnotationQueueResponse | HTTPValidationError
    """

    return (await asyncio_detailed(client=client, body=body)).parsed
