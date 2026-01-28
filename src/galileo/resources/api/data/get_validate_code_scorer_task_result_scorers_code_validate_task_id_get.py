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
from ...models.registered_scorer_task_result_response import RegisteredScorerTaskResultResponse
from ...types import Response


def _get_kwargs(task_id: str) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": f"/scorers/code/validate/{task_id}",
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Union[HTTPValidationError, RegisteredScorerTaskResultResponse]:
    if response.status_code == 200:
        return RegisteredScorerTaskResultResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, RegisteredScorerTaskResultResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    task_id: str, *, client: ApiClient
) -> Response[Union[HTTPValidationError, RegisteredScorerTaskResultResponse]]:
    """Get Validate Code Scorer Task Result.

     Poll for a code-scorer validation task result (returns status/result).

    The validation job creates an entry in `registered_scorer_task_results` (pending) and the runner
    will PATCH the internal task-results endpoint when it finishes. This GET allows clients to poll
    the current task result.

    Args:
        task_id (str):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, RegisteredScorerTaskResultResponse]]
    """
    kwargs = _get_kwargs(task_id=task_id)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    task_id: str, *, client: ApiClient
) -> Optional[Union[HTTPValidationError, RegisteredScorerTaskResultResponse]]:
    """Get Validate Code Scorer Task Result.

     Poll for a code-scorer validation task result (returns status/result).

    The validation job creates an entry in `registered_scorer_task_results` (pending) and the runner
    will PATCH the internal task-results endpoint when it finishes. This GET allows clients to poll
    the current task result.

    Args:
        task_id (str):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, RegisteredScorerTaskResultResponse]
    """
    return sync_detailed(task_id=task_id, client=client).parsed


async def asyncio_detailed(
    task_id: str, *, client: ApiClient
) -> Response[Union[HTTPValidationError, RegisteredScorerTaskResultResponse]]:
    """Get Validate Code Scorer Task Result.

     Poll for a code-scorer validation task result (returns status/result).

    The validation job creates an entry in `registered_scorer_task_results` (pending) and the runner
    will PATCH the internal task-results endpoint when it finishes. This GET allows clients to poll
    the current task result.

    Args:
        task_id (str):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, RegisteredScorerTaskResultResponse]]
    """
    kwargs = _get_kwargs(task_id=task_id)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    task_id: str, *, client: ApiClient
) -> Optional[Union[HTTPValidationError, RegisteredScorerTaskResultResponse]]:
    """Get Validate Code Scorer Task Result.

     Poll for a code-scorer validation task result (returns status/result).

    The validation job creates an entry in `registered_scorer_task_results` (pending) and the runner
    will PATCH the internal task-results endpoint when it finishes. This GET allows clients to poll
    the current task result.

    Args:
        task_id (str):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, RegisteredScorerTaskResultResponse]
    """
    return (await asyncio_detailed(task_id=task_id, client=client)).parsed
