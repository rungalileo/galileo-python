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
from ...models.create_code_metric_generation_request import CreateCodeMetricGenerationRequest
from ...models.create_code_metric_generation_response import CreateCodeMetricGenerationResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(*, body: CreateCodeMetricGenerationRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/code-metric-generations",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> CreateCodeMetricGenerationResponse | HTTPValidationError:
    if response.status_code == 202:
        return CreateCodeMetricGenerationResponse.from_dict(response.json())

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
) -> Response[CreateCodeMetricGenerationResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, body: CreateCodeMetricGenerationRequest
) -> Response[CreateCodeMetricGenerationResponse | HTTPValidationError]:
    """Create Code Metric Generation.

     Generate scorer code from a user message (natural language, existing code, or combination).

    Creates a background job that calls an LLM with the code metric generation system prompt.
    Returns a generation ID for polling.

    **Response:** 202 Accepted with generation ID.

    Args:
        body (CreateCodeMetricGenerationRequest): Request to generate scorer code from a user
            message.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[CreateCodeMetricGenerationResponse | HTTPValidationError]
    """
    kwargs = _get_kwargs(body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, body: CreateCodeMetricGenerationRequest
) -> CreateCodeMetricGenerationResponse | HTTPValidationError | None:
    """Create Code Metric Generation.

     Generate scorer code from a user message (natural language, existing code, or combination).

    Creates a background job that calls an LLM with the code metric generation system prompt.
    Returns a generation ID for polling.

    **Response:** 202 Accepted with generation ID.

    Args:
        body (CreateCodeMetricGenerationRequest): Request to generate scorer code from a user
            message.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        CreateCodeMetricGenerationResponse | HTTPValidationError
    """
    return sync_detailed(client=client, body=body).parsed


async def asyncio_detailed(
    *, client: ApiClient, body: CreateCodeMetricGenerationRequest
) -> Response[CreateCodeMetricGenerationResponse | HTTPValidationError]:
    """Create Code Metric Generation.

     Generate scorer code from a user message (natural language, existing code, or combination).

    Creates a background job that calls an LLM with the code metric generation system prompt.
    Returns a generation ID for polling.

    **Response:** 202 Accepted with generation ID.

    Args:
        body (CreateCodeMetricGenerationRequest): Request to generate scorer code from a user
            message.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[CreateCodeMetricGenerationResponse | HTTPValidationError]
    """
    kwargs = _get_kwargs(body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, body: CreateCodeMetricGenerationRequest
) -> CreateCodeMetricGenerationResponse | HTTPValidationError | None:
    """Create Code Metric Generation.

     Generate scorer code from a user message (natural language, existing code, or combination).

    Creates a background job that calls an LLM with the code metric generation system prompt.
    Returns a generation ID for polling.

    **Response:** 202 Accepted with generation ID.

    Args:
        body (CreateCodeMetricGenerationRequest): Request to generate scorer code from a user
            message.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        CreateCodeMetricGenerationResponse | HTTPValidationError
    """
    return (await asyncio_detailed(client=client, body=body)).parsed
