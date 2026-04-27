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
from ...models.create_scorer_feedback_request import CreateScorerFeedbackRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.scorer_feedback_response import ScorerFeedbackResponse
from ...types import Response


def _get_kwargs(*, body: CreateScorerFeedbackRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": RequestMethod.POST, "return_raw_response": True, "path": "/scorer-feedbacks"}

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | ScorerFeedbackResponse:
    if response.status_code == 201:
        response_201 = ScorerFeedbackResponse.from_dict(response.json())

        return response_201

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
) -> Response[HTTPValidationError | ScorerFeedbackResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, body: CreateScorerFeedbackRequest
) -> Response[HTTPValidationError | ScorerFeedbackResponse]:
    """Create Scorer Feedback

     Creates a new feedback item in the global queue for the specified scorer.

    **Validation:**
    - Validates both original_value and annotated_value against scorer's output_type
    - Validates scorer_version_id exists and user has access
    - Validates user has access to the specified project
    - Auto-creates new queue if no active queue exists for this scorer
    - If active queue exists, adds feedback to that queue

    **Errors:**
    - 422 - Invalid annotated_value/original_value format or validation failure
    - 404 - Project, run, scorer, or scorer_version not found
    - 409 - Queue is currently locked (generating, reviewing, or completed)

    Args:
        body (CreateScorerFeedbackRequest): Request schema for creating scorer feedback.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ScorerFeedbackResponse]
    """

    kwargs = _get_kwargs(body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, body: CreateScorerFeedbackRequest
) -> Optional[HTTPValidationError | ScorerFeedbackResponse]:
    """Create Scorer Feedback

     Creates a new feedback item in the global queue for the specified scorer.

    **Validation:**
    - Validates both original_value and annotated_value against scorer's output_type
    - Validates scorer_version_id exists and user has access
    - Validates user has access to the specified project
    - Auto-creates new queue if no active queue exists for this scorer
    - If active queue exists, adds feedback to that queue

    **Errors:**
    - 422 - Invalid annotated_value/original_value format or validation failure
    - 404 - Project, run, scorer, or scorer_version not found
    - 409 - Queue is currently locked (generating, reviewing, or completed)

    Args:
        body (CreateScorerFeedbackRequest): Request schema for creating scorer feedback.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ScorerFeedbackResponse
    """

    return sync_detailed(client=client, body=body).parsed


async def asyncio_detailed(
    *, client: ApiClient, body: CreateScorerFeedbackRequest
) -> Response[HTTPValidationError | ScorerFeedbackResponse]:
    """Create Scorer Feedback

     Creates a new feedback item in the global queue for the specified scorer.

    **Validation:**
    - Validates both original_value and annotated_value against scorer's output_type
    - Validates scorer_version_id exists and user has access
    - Validates user has access to the specified project
    - Auto-creates new queue if no active queue exists for this scorer
    - If active queue exists, adds feedback to that queue

    **Errors:**
    - 422 - Invalid annotated_value/original_value format or validation failure
    - 404 - Project, run, scorer, or scorer_version not found
    - 409 - Queue is currently locked (generating, reviewing, or completed)

    Args:
        body (CreateScorerFeedbackRequest): Request schema for creating scorer feedback.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ScorerFeedbackResponse]
    """

    kwargs = _get_kwargs(body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, body: CreateScorerFeedbackRequest
) -> Optional[HTTPValidationError | ScorerFeedbackResponse]:
    """Create Scorer Feedback

     Creates a new feedback item in the global queue for the specified scorer.

    **Validation:**
    - Validates both original_value and annotated_value against scorer's output_type
    - Validates scorer_version_id exists and user has access
    - Validates user has access to the specified project
    - Auto-creates new queue if no active queue exists for this scorer
    - If active queue exists, adds feedback to that queue

    **Errors:**
    - 422 - Invalid annotated_value/original_value format or validation failure
    - 404 - Project, run, scorer, or scorer_version not found
    - 409 - Queue is currently locked (generating, reviewing, or completed)

    Args:
        body (CreateScorerFeedbackRequest): Request schema for creating scorer feedback.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ScorerFeedbackResponse
    """

    return (await asyncio_detailed(client=client, body=body)).parsed
