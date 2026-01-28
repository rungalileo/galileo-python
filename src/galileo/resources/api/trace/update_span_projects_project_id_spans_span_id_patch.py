from http import HTTPStatus
from typing import Any, Optional, Union

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
from ...models.log_span_update_request import LogSpanUpdateRequest
from ...models.log_span_update_response import LogSpanUpdateResponse
from ...types import Response


def _get_kwargs(project_id: str, span_id: str, *, body: LogSpanUpdateRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.PATCH,
        "return_raw_response": True,
        "path": f"/projects/{project_id}/spans/{span_id}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Union[HTTPValidationError, LogSpanUpdateResponse]:
    if response.status_code == 200:
        return LogSpanUpdateResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, LogSpanUpdateResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, span_id: str, *, client: ApiClient, body: LogSpanUpdateRequest
) -> Response[Union[HTTPValidationError, LogSpanUpdateResponse]]:
    """Update Span.

     Update a span with the given ID.

    Args:
        project_id (str):
        span_id (str):
        body (LogSpanUpdateRequest): Request model for updating a span.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, LogSpanUpdateResponse]]
    """
    kwargs = _get_kwargs(project_id=project_id, span_id=span_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, span_id: str, *, client: ApiClient, body: LogSpanUpdateRequest
) -> Optional[Union[HTTPValidationError, LogSpanUpdateResponse]]:
    """Update Span.

     Update a span with the given ID.

    Args:
        project_id (str):
        span_id (str):
        body (LogSpanUpdateRequest): Request model for updating a span.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, LogSpanUpdateResponse]
    """
    return sync_detailed(project_id=project_id, span_id=span_id, client=client, body=body).parsed


async def asyncio_detailed(
    project_id: str, span_id: str, *, client: ApiClient, body: LogSpanUpdateRequest
) -> Response[Union[HTTPValidationError, LogSpanUpdateResponse]]:
    """Update Span.

     Update a span with the given ID.

    Args:
        project_id (str):
        span_id (str):
        body (LogSpanUpdateRequest): Request model for updating a span.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, LogSpanUpdateResponse]]
    """
    kwargs = _get_kwargs(project_id=project_id, span_id=span_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, span_id: str, *, client: ApiClient, body: LogSpanUpdateRequest
) -> Optional[Union[HTTPValidationError, LogSpanUpdateResponse]]:
    """Update Span.

     Update a span with the given ID.

    Args:
        project_id (str):
        span_id (str):
        body (LogSpanUpdateRequest): Request model for updating a span.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, LogSpanUpdateResponse]
    """
    return (await asyncio_detailed(project_id=project_id, span_id=span_id, client=client, body=body)).parsed
