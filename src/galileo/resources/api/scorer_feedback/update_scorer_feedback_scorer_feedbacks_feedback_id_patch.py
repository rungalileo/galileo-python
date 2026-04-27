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
from ...models.http_validation_error import HTTPValidationError
from ...models.scorer_feedback_response import ScorerFeedbackResponse
from ...models.update_scorer_feedback_request import UpdateScorerFeedbackRequest
from ...types import Response


def _get_kwargs(feedback_id: str, *, body: UpdateScorerFeedbackRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.PATCH,
        "return_raw_response": True,
        "path": "/scorer-feedbacks/{feedback_id}".format(feedback_id=feedback_id),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | ScorerFeedbackResponse:
    if response.status_code == 200:
        response_200 = ScorerFeedbackResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ScorerFeedbackResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    feedback_id: str, *, client: ApiClient, body: UpdateScorerFeedbackRequest
) -> Response[HTTPValidationError | ScorerFeedbackResponse]:
    """Update Scorer Feedback

     Updates an existing feedback item in the queue.

    Useful for refining values or rationale while reviewing feedback before applying.

    **Validation:**
    - Queue must be in pending state (not locked or completed)
    - annotated_value (if provided) must be valid for the scorer's output_type
    - At least one field must be provided

    **Errors:**
    - 422 - Invalid annotated_value for scorer output_type, or no fields provided
    - 404 - Feedback item not found
    - 409 - Queue is currently processing or finished (locked, cannot modify)

    Args:
        feedback_id (str):
        body (UpdateScorerFeedbackRequest): Request schema for updating scorer feedback.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ScorerFeedbackResponse]
    """

    kwargs = _get_kwargs(feedback_id=feedback_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    feedback_id: str, *, client: ApiClient, body: UpdateScorerFeedbackRequest
) -> Optional[HTTPValidationError | ScorerFeedbackResponse]:
    """Update Scorer Feedback

     Updates an existing feedback item in the queue.

    Useful for refining values or rationale while reviewing feedback before applying.

    **Validation:**
    - Queue must be in pending state (not locked or completed)
    - annotated_value (if provided) must be valid for the scorer's output_type
    - At least one field must be provided

    **Errors:**
    - 422 - Invalid annotated_value for scorer output_type, or no fields provided
    - 404 - Feedback item not found
    - 409 - Queue is currently processing or finished (locked, cannot modify)

    Args:
        feedback_id (str):
        body (UpdateScorerFeedbackRequest): Request schema for updating scorer feedback.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ScorerFeedbackResponse
    """

    return sync_detailed(feedback_id=feedback_id, client=client, body=body).parsed


async def asyncio_detailed(
    feedback_id: str, *, client: ApiClient, body: UpdateScorerFeedbackRequest
) -> Response[HTTPValidationError | ScorerFeedbackResponse]:
    """Update Scorer Feedback

     Updates an existing feedback item in the queue.

    Useful for refining values or rationale while reviewing feedback before applying.

    **Validation:**
    - Queue must be in pending state (not locked or completed)
    - annotated_value (if provided) must be valid for the scorer's output_type
    - At least one field must be provided

    **Errors:**
    - 422 - Invalid annotated_value for scorer output_type, or no fields provided
    - 404 - Feedback item not found
    - 409 - Queue is currently processing or finished (locked, cannot modify)

    Args:
        feedback_id (str):
        body (UpdateScorerFeedbackRequest): Request schema for updating scorer feedback.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ScorerFeedbackResponse]
    """

    kwargs = _get_kwargs(feedback_id=feedback_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    feedback_id: str, *, client: ApiClient, body: UpdateScorerFeedbackRequest
) -> Optional[HTTPValidationError | ScorerFeedbackResponse]:
    """Update Scorer Feedback

     Updates an existing feedback item in the queue.

    Useful for refining values or rationale while reviewing feedback before applying.

    **Validation:**
    - Queue must be in pending state (not locked or completed)
    - annotated_value (if provided) must be valid for the scorer's output_type
    - At least one field must be provided

    **Errors:**
    - 422 - Invalid annotated_value for scorer output_type, or no fields provided
    - 404 - Feedback item not found
    - 409 - Queue is currently processing or finished (locked, cannot modify)

    Args:
        feedback_id (str):
        body (UpdateScorerFeedbackRequest): Request schema for updating scorer feedback.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ScorerFeedbackResponse
    """

    return (await asyncio_detailed(feedback_id=feedback_id, client=client, body=body)).parsed
