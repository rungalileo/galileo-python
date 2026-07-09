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
from ...models.extended_trace_record_with_children import ExtendedTraceRecordWithChildren
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(project_id: str, trace_id: str, *, include_presigned_urls: bool | Unset = False) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["include_presigned_urls"] = include_presigned_urls

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/projects/{project_id}/traces/{trace_id}".format(project_id=project_id, trace_id=trace_id),
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> ExtendedTraceRecordWithChildren | HTTPValidationError:
    if response.status_code == 200:
        response_200 = ExtendedTraceRecordWithChildren.from_dict(response.json())

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
) -> Response[ExtendedTraceRecordWithChildren | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, trace_id: str, *, client: ApiClient, include_presigned_urls: bool | Unset = False
) -> Response[ExtendedTraceRecordWithChildren | HTTPValidationError]:
    """Get Trace

    Args:
        project_id (str):
        trace_id (str):
        include_presigned_urls (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExtendedTraceRecordWithChildren | HTTPValidationError]
    """

    kwargs = _get_kwargs(project_id=project_id, trace_id=trace_id, include_presigned_urls=include_presigned_urls)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, trace_id: str, *, client: ApiClient, include_presigned_urls: bool | Unset = False
) -> Optional[ExtendedTraceRecordWithChildren | HTTPValidationError]:
    """Get Trace

    Args:
        project_id (str):
        trace_id (str):
        include_presigned_urls (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExtendedTraceRecordWithChildren | HTTPValidationError
    """

    return sync_detailed(
        project_id=project_id, trace_id=trace_id, client=client, include_presigned_urls=include_presigned_urls
    ).parsed


async def asyncio_detailed(
    project_id: str, trace_id: str, *, client: ApiClient, include_presigned_urls: bool | Unset = False
) -> Response[ExtendedTraceRecordWithChildren | HTTPValidationError]:
    """Get Trace

    Args:
        project_id (str):
        trace_id (str):
        include_presigned_urls (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExtendedTraceRecordWithChildren | HTTPValidationError]
    """

    kwargs = _get_kwargs(project_id=project_id, trace_id=trace_id, include_presigned_urls=include_presigned_urls)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, trace_id: str, *, client: ApiClient, include_presigned_urls: bool | Unset = False
) -> Optional[ExtendedTraceRecordWithChildren | HTTPValidationError]:
    """Get Trace

    Args:
        project_id (str):
        trace_id (str):
        include_presigned_urls (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExtendedTraceRecordWithChildren | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            project_id=project_id, trace_id=trace_id, client=client, include_presigned_urls=include_presigned_urls
        )
    ).parsed
