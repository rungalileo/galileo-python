from http import HTTPStatus
from typing import Any

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
from ...models.annotation_queue_export_request import AnnotationQueueExportRequest
from ...models.annotation_queue_export_url_response import AnnotationQueueExportUrlResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(queue_id: str, *, body: AnnotationQueueExportRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": f"/annotation_queues/{queue_id}/records/export/url",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> AnnotationQueueExportUrlResponse | HTTPValidationError:
    if response.status_code == 200:
        return AnnotationQueueExportUrlResponse.from_dict(response.json())

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

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
) -> Response[AnnotationQueueExportUrlResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    queue_id: str, *, client: ApiClient, body: AnnotationQueueExportRequest
) -> Response[AnnotationQueueExportUrlResponse | HTTPValidationError]:
    """Export Annotation Queue Records Url.

     Export selected records from an annotation queue and return a presigned download URL.

    The request must specify either a list of record IDs or a filter tree to select queue records.

    Permission checks:
    - User must have READ permission on the annotation queue

    Args:
        queue_id (str):
        body (AnnotationQueueExportRequest): Request to export selected annotation queue records.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[AnnotationQueueExportUrlResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(queue_id=queue_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    queue_id: str, *, client: ApiClient, body: AnnotationQueueExportRequest
) -> AnnotationQueueExportUrlResponse | HTTPValidationError | None:
    """Export Annotation Queue Records Url.

     Export selected records from an annotation queue and return a presigned download URL.

    The request must specify either a list of record IDs or a filter tree to select queue records.

    Permission checks:
    - User must have READ permission on the annotation queue

    Args:
        queue_id (str):
        body (AnnotationQueueExportRequest): Request to export selected annotation queue records.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[AnnotationQueueExportUrlResponse, HTTPValidationError]
    """
    return sync_detailed(queue_id=queue_id, client=client, body=body).parsed


async def asyncio_detailed(
    queue_id: str, *, client: ApiClient, body: AnnotationQueueExportRequest
) -> Response[AnnotationQueueExportUrlResponse | HTTPValidationError]:
    """Export Annotation Queue Records Url.

     Export selected records from an annotation queue and return a presigned download URL.

    The request must specify either a list of record IDs or a filter tree to select queue records.

    Permission checks:
    - User must have READ permission on the annotation queue

    Args:
        queue_id (str):
        body (AnnotationQueueExportRequest): Request to export selected annotation queue records.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[AnnotationQueueExportUrlResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(queue_id=queue_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    queue_id: str, *, client: ApiClient, body: AnnotationQueueExportRequest
) -> AnnotationQueueExportUrlResponse | HTTPValidationError | None:
    """Export Annotation Queue Records Url.

     Export selected records from an annotation queue and return a presigned download URL.

    The request must specify either a list of record IDs or a filter tree to select queue records.

    Permission checks:
    - User must have READ permission on the annotation queue

    Args:
        queue_id (str):
        body (AnnotationQueueExportRequest): Request to export selected annotation queue records.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[AnnotationQueueExportUrlResponse, HTTPValidationError]
    """
    return (await asyncio_detailed(queue_id=queue_id, client=client, body=body)).parsed
