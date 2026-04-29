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
from ...models.http_validation_error import HTTPValidationError
from ...models.log_records_metrics_query_request import LogRecordsMetricsQueryRequest
from ...models.log_records_metrics_response import LogRecordsMetricsResponse
from ...types import Response


def _get_kwargs(project_id: str, *, body: LogRecordsMetricsQueryRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": f"/projects/{project_id}/metrics/search/v2",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | LogRecordsMetricsResponse:
    if response.status_code == 200:
        return LogRecordsMetricsResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | LogRecordsMetricsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, *, client: ApiClient, body: LogRecordsMetricsQueryRequest
) -> Response[HTTPValidationError | LogRecordsMetricsResponse]:
    """Query Metrics V2.

     Same as /metrics/search but returns metrics with node-type counts: trace (requests_count),
    session_count, and span_count in aggregate_metrics and in each bucket, similar to
    /metrics/custom_search.

    Args:
        project_id (str):
        body (LogRecordsMetricsQueryRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, LogRecordsMetricsResponse]]
    """
    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, *, client: ApiClient, body: LogRecordsMetricsQueryRequest
) -> HTTPValidationError | LogRecordsMetricsResponse | None:
    """Query Metrics V2.

     Same as /metrics/search but returns metrics with node-type counts: trace (requests_count),
    session_count, and span_count in aggregate_metrics and in each bucket, similar to
    /metrics/custom_search.

    Args:
        project_id (str):
        body (LogRecordsMetricsQueryRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, LogRecordsMetricsResponse]
    """
    return sync_detailed(project_id=project_id, client=client, body=body).parsed


async def asyncio_detailed(
    project_id: str, *, client: ApiClient, body: LogRecordsMetricsQueryRequest
) -> Response[HTTPValidationError | LogRecordsMetricsResponse]:
    """Query Metrics V2.

     Same as /metrics/search but returns metrics with node-type counts: trace (requests_count),
    session_count, and span_count in aggregate_metrics and in each bucket, similar to
    /metrics/custom_search.

    Args:
        project_id (str):
        body (LogRecordsMetricsQueryRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, LogRecordsMetricsResponse]]
    """
    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, *, client: ApiClient, body: LogRecordsMetricsQueryRequest
) -> HTTPValidationError | LogRecordsMetricsResponse | None:
    """Query Metrics V2.

     Same as /metrics/search but returns metrics with node-type counts: trace (requests_count),
    session_count, and span_count in aggregate_metrics and in each bucket, similar to
    /metrics/custom_search.

    Args:
        project_id (str):
        body (LogRecordsMetricsQueryRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, LogRecordsMetricsResponse]
    """
    return (await asyncio_detailed(project_id=project_id, client=client, body=body)).parsed
