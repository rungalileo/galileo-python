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
from ...models.autotune_validation_results_response import AutotuneValidationResultsResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(queue_id: str, *, metrics_testing_run_id: None | str | Unset = UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_metrics_testing_run_id: None | str | Unset
    if isinstance(metrics_testing_run_id, Unset):
        json_metrics_testing_run_id = UNSET
    else:
        json_metrics_testing_run_id = metrics_testing_run_id
    params["metrics_testing_run_id"] = json_metrics_testing_run_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/feedback-queues/{queue_id}/validation-results".format(queue_id=queue_id),
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> AutotuneValidationResultsResponse | HTTPValidationError:
    if response.status_code == 200:
        response_200 = AutotuneValidationResultsResponse.from_dict(response.json())

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
) -> Response[AutotuneValidationResultsResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    queue_id: str, *, client: ApiClient, metrics_testing_run_id: None | str | Unset = UNSET
) -> Response[AutotuneValidationResultsResponse | HTTPValidationError]:
    """Get Validation Results

     Poll autotune validation results for a feedback queue.

    Returns one row per feedback item with the new scorer output joined in from
    the metrics testing run. Used by the UI for the 3-column comparison table:
    Original Value | Expected (Annotated) | New Result.

    **Pollable:** Returns status=pending with null scores while validation is running.
    Transitions through pending → in_progress → completed as scores arrive.

    **Args:**
    - metrics_testing_run_id: Optional metrics testing run ID (from validate response).
      When provided, fetches scored records and joins with feedback items.

    **Errors:**
    - 404 - Queue not found or user doesn't have access

    Args:
        queue_id (str):
        metrics_testing_run_id (None | str | Unset): Metrics testing run ID for fetching
            validation scores

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AutotuneValidationResultsResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(queue_id=queue_id, metrics_testing_run_id=metrics_testing_run_id)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    queue_id: str, *, client: ApiClient, metrics_testing_run_id: None | str | Unset = UNSET
) -> Optional[AutotuneValidationResultsResponse | HTTPValidationError]:
    """Get Validation Results

     Poll autotune validation results for a feedback queue.

    Returns one row per feedback item with the new scorer output joined in from
    the metrics testing run. Used by the UI for the 3-column comparison table:
    Original Value | Expected (Annotated) | New Result.

    **Pollable:** Returns status=pending with null scores while validation is running.
    Transitions through pending → in_progress → completed as scores arrive.

    **Args:**
    - metrics_testing_run_id: Optional metrics testing run ID (from validate response).
      When provided, fetches scored records and joins with feedback items.

    **Errors:**
    - 404 - Queue not found or user doesn't have access

    Args:
        queue_id (str):
        metrics_testing_run_id (None | str | Unset): Metrics testing run ID for fetching
            validation scores

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AutotuneValidationResultsResponse | HTTPValidationError
    """

    return sync_detailed(queue_id=queue_id, client=client, metrics_testing_run_id=metrics_testing_run_id).parsed


async def asyncio_detailed(
    queue_id: str, *, client: ApiClient, metrics_testing_run_id: None | str | Unset = UNSET
) -> Response[AutotuneValidationResultsResponse | HTTPValidationError]:
    """Get Validation Results

     Poll autotune validation results for a feedback queue.

    Returns one row per feedback item with the new scorer output joined in from
    the metrics testing run. Used by the UI for the 3-column comparison table:
    Original Value | Expected (Annotated) | New Result.

    **Pollable:** Returns status=pending with null scores while validation is running.
    Transitions through pending → in_progress → completed as scores arrive.

    **Args:**
    - metrics_testing_run_id: Optional metrics testing run ID (from validate response).
      When provided, fetches scored records and joins with feedback items.

    **Errors:**
    - 404 - Queue not found or user doesn't have access

    Args:
        queue_id (str):
        metrics_testing_run_id (None | str | Unset): Metrics testing run ID for fetching
            validation scores

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AutotuneValidationResultsResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(queue_id=queue_id, metrics_testing_run_id=metrics_testing_run_id)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    queue_id: str, *, client: ApiClient, metrics_testing_run_id: None | str | Unset = UNSET
) -> Optional[AutotuneValidationResultsResponse | HTTPValidationError]:
    """Get Validation Results

     Poll autotune validation results for a feedback queue.

    Returns one row per feedback item with the new scorer output joined in from
    the metrics testing run. Used by the UI for the 3-column comparison table:
    Original Value | Expected (Annotated) | New Result.

    **Pollable:** Returns status=pending with null scores while validation is running.
    Transitions through pending → in_progress → completed as scores arrive.

    **Args:**
    - metrics_testing_run_id: Optional metrics testing run ID (from validate response).
      When provided, fetches scored records and joins with feedback items.

    **Errors:**
    - 404 - Queue not found or user doesn't have access

    Args:
        queue_id (str):
        metrics_testing_run_id (None | str | Unset): Metrics testing run ID for fetching
            validation scores

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AutotuneValidationResultsResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(queue_id=queue_id, client=client, metrics_testing_run_id=metrics_testing_run_id)
    ).parsed
