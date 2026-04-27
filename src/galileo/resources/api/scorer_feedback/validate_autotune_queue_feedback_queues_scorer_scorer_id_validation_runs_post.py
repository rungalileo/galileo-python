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
from ...models.validate_autotune_queue_request import ValidateAutotuneQueueRequest
from ...models.validate_autotune_queue_response import ValidateAutotuneQueueResponse
from ...types import Response


def _get_kwargs(scorer_id: str, *, body: ValidateAutotuneQueueRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/feedback-queues/scorer/{scorer_id}/validation-runs".format(scorer_id=scorer_id),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> HTTPValidationError | ValidateAutotuneQueueResponse:
    if response.status_code == 202:
        response_202 = ValidateAutotuneQueueResponse.from_dict(response.json())

        return response_202

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
) -> Response[HTTPValidationError | ValidateAutotuneQueueResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    scorer_id: str, *, client: ApiClient, body: ValidateAutotuneQueueRequest
) -> Response[HTTPValidationError | ValidateAutotuneQueueResponse]:
    """Validate Autotune Queue

     Test a draft prompt against feedback records in the active queue.

    Creates a metrics testing run by copying the feedback records and running
    generated scorer validation with the provided prompt. Used in the AutoTune
    Data tab for 3-column comparison: Original | Expected (Annotated) | New Result.

    Works in any active queue state (pending, generating, or reviewing).

    **Response:**
    - 202 Accepted with metrics_testing_run_id for viewing results

    **Errors:**
    - 404 - Scorer not found or no active queue exists
    - 422 - Queue has no feedback items or scorer has no version
    - 500 - Record processing failure

    Args:
        scorer_id (str):
        body (ValidateAutotuneQueueRequest): Request to test a draft prompt against autotune
            feedback records.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ValidateAutotuneQueueResponse]
    """

    kwargs = _get_kwargs(scorer_id=scorer_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    scorer_id: str, *, client: ApiClient, body: ValidateAutotuneQueueRequest
) -> Optional[HTTPValidationError | ValidateAutotuneQueueResponse]:
    """Validate Autotune Queue

     Test a draft prompt against feedback records in the active queue.

    Creates a metrics testing run by copying the feedback records and running
    generated scorer validation with the provided prompt. Used in the AutoTune
    Data tab for 3-column comparison: Original | Expected (Annotated) | New Result.

    Works in any active queue state (pending, generating, or reviewing).

    **Response:**
    - 202 Accepted with metrics_testing_run_id for viewing results

    **Errors:**
    - 404 - Scorer not found or no active queue exists
    - 422 - Queue has no feedback items or scorer has no version
    - 500 - Record processing failure

    Args:
        scorer_id (str):
        body (ValidateAutotuneQueueRequest): Request to test a draft prompt against autotune
            feedback records.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ValidateAutotuneQueueResponse
    """

    return sync_detailed(scorer_id=scorer_id, client=client, body=body).parsed


async def asyncio_detailed(
    scorer_id: str, *, client: ApiClient, body: ValidateAutotuneQueueRequest
) -> Response[HTTPValidationError | ValidateAutotuneQueueResponse]:
    """Validate Autotune Queue

     Test a draft prompt against feedback records in the active queue.

    Creates a metrics testing run by copying the feedback records and running
    generated scorer validation with the provided prompt. Used in the AutoTune
    Data tab for 3-column comparison: Original | Expected (Annotated) | New Result.

    Works in any active queue state (pending, generating, or reviewing).

    **Response:**
    - 202 Accepted with metrics_testing_run_id for viewing results

    **Errors:**
    - 404 - Scorer not found or no active queue exists
    - 422 - Queue has no feedback items or scorer has no version
    - 500 - Record processing failure

    Args:
        scorer_id (str):
        body (ValidateAutotuneQueueRequest): Request to test a draft prompt against autotune
            feedback records.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ValidateAutotuneQueueResponse]
    """

    kwargs = _get_kwargs(scorer_id=scorer_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    scorer_id: str, *, client: ApiClient, body: ValidateAutotuneQueueRequest
) -> Optional[HTTPValidationError | ValidateAutotuneQueueResponse]:
    """Validate Autotune Queue

     Test a draft prompt against feedback records in the active queue.

    Creates a metrics testing run by copying the feedback records and running
    generated scorer validation with the provided prompt. Used in the AutoTune
    Data tab for 3-column comparison: Original | Expected (Annotated) | New Result.

    Works in any active queue state (pending, generating, or reviewing).

    **Response:**
    - 202 Accepted with metrics_testing_run_id for viewing results

    **Errors:**
    - 404 - Scorer not found or no active queue exists
    - 422 - Queue has no feedback items or scorer has no version
    - 500 - Record processing failure

    Args:
        scorer_id (str):
        body (ValidateAutotuneQueueRequest): Request to test a draft prompt against autotune
            feedback records.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ValidateAutotuneQueueResponse
    """

    return (await asyncio_detailed(scorer_id=scorer_id, client=client, body=body)).parsed
