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
from ...models.annotation_template_db import AnnotationTemplateDB
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(queue_id: str) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/annotation_queues/{queue_id}/templates".format(queue_id=queue_id),
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | list[AnnotationTemplateDB]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AnnotationTemplateDB.from_dict(response_200_item_data)

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
) -> Response[HTTPValidationError | list[AnnotationTemplateDB]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(queue_id: str, *, client: ApiClient) -> Response[HTTPValidationError | list[AnnotationTemplateDB]]:
    """Get Queue Templates

     Get all templates for an annotation queue.

    Templates are returned ordered by position (ascending).

    Args:
        queue_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[AnnotationTemplateDB]]
    """

    kwargs = _get_kwargs(queue_id=queue_id)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(queue_id: str, *, client: ApiClient) -> Optional[HTTPValidationError | list[AnnotationTemplateDB]]:
    """Get Queue Templates

     Get all templates for an annotation queue.

    Templates are returned ordered by position (ascending).

    Args:
        queue_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[AnnotationTemplateDB]
    """

    return sync_detailed(queue_id=queue_id, client=client).parsed


async def asyncio_detailed(
    queue_id: str, *, client: ApiClient
) -> Response[HTTPValidationError | list[AnnotationTemplateDB]]:
    """Get Queue Templates

     Get all templates for an annotation queue.

    Templates are returned ordered by position (ascending).

    Args:
        queue_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[AnnotationTemplateDB]]
    """

    kwargs = _get_kwargs(queue_id=queue_id)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(queue_id: str, *, client: ApiClient) -> Optional[HTTPValidationError | list[AnnotationTemplateDB]]:
    """Get Queue Templates

     Get all templates for an annotation queue.

    Templates are returned ordered by position (ascending).

    Args:
        queue_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[AnnotationTemplateDB]
    """

    return (await asyncio_detailed(queue_id=queue_id, client=client)).parsed
