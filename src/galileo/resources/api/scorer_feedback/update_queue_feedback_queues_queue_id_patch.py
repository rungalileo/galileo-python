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
from ...models.update_queue_request import UpdateQueueRequest
from ...models.update_queue_response import UpdateQueueResponse
from ...types import Response


def _get_kwargs(queue_id: str, *, body: UpdateQueueRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.PATCH,
        "return_raw_response": True,
        "path": "/feedback-queues/{queue_id}".format(queue_id=queue_id),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | UpdateQueueResponse:
    if response.status_code == 200:
        response_200 = UpdateQueueResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | UpdateQueueResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    queue_id: str, *, client: ApiClient, body: UpdateQueueRequest
) -> Response[HTTPValidationError | UpdateQueueResponse]:
    r"""Update Queue

     Update a feedback queue by performing an action.

    **Supported actions:**
    - \"abort\": Abort the feedback application process and return the queue to pending state.
      Used when user clicks \"Back\" or \"Cancel\" during generation or review.
      Clears draft_prompt and generation_task_id. Same queue is reused.
      Can be called during 'generating' or 'reviewing' state.

    - \"complete\": Complete the queue after saving a new scorer version.
      Used when user saves a new version from the review flow.
      Sets status to completed (immutable) and links queue to the resulting version.
      Requires target_scorer_version_id, result_scorer_id, and result_scorer_version_id.
      Can only be called during 'reviewing' state.

    **Request body:**
    - action: The action to perform (\"abort\" or \"complete\")
    - target_scorer_version_id: Required for \"complete\" action - ID of the version feedback was
    applied to
    - result_scorer_id: Required for \"complete\" action - ID of the scorer that owns the result
    version.
      For custom LLM scorers this is the same as the queue's scorer. For preset scorers this is the
      new custom scorer duplicated from the preset.
    - result_scorer_version_id: Required for \"complete\" action - ID of the scorer version created

    **Response:**
    - 200 OK with queue details showing updated status

    **Errors:**
    - 404 - Queue not found or user doesn't have access
    - 409 - Queue is not in a valid state for the requested action
    - 422 - Invalid action or missing required parameters

    Args:
        queue_id (str):
        body (UpdateQueueRequest): Request schema for updating a feedback queue state via PATCH.

            Used to perform actions on a queue, such as aborting generation/review or completing the
            queue.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UpdateQueueResponse]
    """

    kwargs = _get_kwargs(queue_id=queue_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    queue_id: str, *, client: ApiClient, body: UpdateQueueRequest
) -> Optional[HTTPValidationError | UpdateQueueResponse]:
    r"""Update Queue

     Update a feedback queue by performing an action.

    **Supported actions:**
    - \"abort\": Abort the feedback application process and return the queue to pending state.
      Used when user clicks \"Back\" or \"Cancel\" during generation or review.
      Clears draft_prompt and generation_task_id. Same queue is reused.
      Can be called during 'generating' or 'reviewing' state.

    - \"complete\": Complete the queue after saving a new scorer version.
      Used when user saves a new version from the review flow.
      Sets status to completed (immutable) and links queue to the resulting version.
      Requires target_scorer_version_id, result_scorer_id, and result_scorer_version_id.
      Can only be called during 'reviewing' state.

    **Request body:**
    - action: The action to perform (\"abort\" or \"complete\")
    - target_scorer_version_id: Required for \"complete\" action - ID of the version feedback was
    applied to
    - result_scorer_id: Required for \"complete\" action - ID of the scorer that owns the result
    version.
      For custom LLM scorers this is the same as the queue's scorer. For preset scorers this is the
      new custom scorer duplicated from the preset.
    - result_scorer_version_id: Required for \"complete\" action - ID of the scorer version created

    **Response:**
    - 200 OK with queue details showing updated status

    **Errors:**
    - 404 - Queue not found or user doesn't have access
    - 409 - Queue is not in a valid state for the requested action
    - 422 - Invalid action or missing required parameters

    Args:
        queue_id (str):
        body (UpdateQueueRequest): Request schema for updating a feedback queue state via PATCH.

            Used to perform actions on a queue, such as aborting generation/review or completing the
            queue.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UpdateQueueResponse
    """

    return sync_detailed(queue_id=queue_id, client=client, body=body).parsed


async def asyncio_detailed(
    queue_id: str, *, client: ApiClient, body: UpdateQueueRequest
) -> Response[HTTPValidationError | UpdateQueueResponse]:
    r"""Update Queue

     Update a feedback queue by performing an action.

    **Supported actions:**
    - \"abort\": Abort the feedback application process and return the queue to pending state.
      Used when user clicks \"Back\" or \"Cancel\" during generation or review.
      Clears draft_prompt and generation_task_id. Same queue is reused.
      Can be called during 'generating' or 'reviewing' state.

    - \"complete\": Complete the queue after saving a new scorer version.
      Used when user saves a new version from the review flow.
      Sets status to completed (immutable) and links queue to the resulting version.
      Requires target_scorer_version_id, result_scorer_id, and result_scorer_version_id.
      Can only be called during 'reviewing' state.

    **Request body:**
    - action: The action to perform (\"abort\" or \"complete\")
    - target_scorer_version_id: Required for \"complete\" action - ID of the version feedback was
    applied to
    - result_scorer_id: Required for \"complete\" action - ID of the scorer that owns the result
    version.
      For custom LLM scorers this is the same as the queue's scorer. For preset scorers this is the
      new custom scorer duplicated from the preset.
    - result_scorer_version_id: Required for \"complete\" action - ID of the scorer version created

    **Response:**
    - 200 OK with queue details showing updated status

    **Errors:**
    - 404 - Queue not found or user doesn't have access
    - 409 - Queue is not in a valid state for the requested action
    - 422 - Invalid action or missing required parameters

    Args:
        queue_id (str):
        body (UpdateQueueRequest): Request schema for updating a feedback queue state via PATCH.

            Used to perform actions on a queue, such as aborting generation/review or completing the
            queue.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UpdateQueueResponse]
    """

    kwargs = _get_kwargs(queue_id=queue_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    queue_id: str, *, client: ApiClient, body: UpdateQueueRequest
) -> Optional[HTTPValidationError | UpdateQueueResponse]:
    r"""Update Queue

     Update a feedback queue by performing an action.

    **Supported actions:**
    - \"abort\": Abort the feedback application process and return the queue to pending state.
      Used when user clicks \"Back\" or \"Cancel\" during generation or review.
      Clears draft_prompt and generation_task_id. Same queue is reused.
      Can be called during 'generating' or 'reviewing' state.

    - \"complete\": Complete the queue after saving a new scorer version.
      Used when user saves a new version from the review flow.
      Sets status to completed (immutable) and links queue to the resulting version.
      Requires target_scorer_version_id, result_scorer_id, and result_scorer_version_id.
      Can only be called during 'reviewing' state.

    **Request body:**
    - action: The action to perform (\"abort\" or \"complete\")
    - target_scorer_version_id: Required for \"complete\" action - ID of the version feedback was
    applied to
    - result_scorer_id: Required for \"complete\" action - ID of the scorer that owns the result
    version.
      For custom LLM scorers this is the same as the queue's scorer. For preset scorers this is the
      new custom scorer duplicated from the preset.
    - result_scorer_version_id: Required for \"complete\" action - ID of the scorer version created

    **Response:**
    - 200 OK with queue details showing updated status

    **Errors:**
    - 404 - Queue not found or user doesn't have access
    - 409 - Queue is not in a valid state for the requested action
    - 422 - Invalid action or missing required parameters

    Args:
        queue_id (str):
        body (UpdateQueueRequest): Request schema for updating a feedback queue state via PATCH.

            Used to perform actions on a queue, such as aborting generation/review or completing the
            queue.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UpdateQueueResponse
    """

    return (await asyncio_detailed(queue_id=queue_id, client=client, body=body)).parsed
