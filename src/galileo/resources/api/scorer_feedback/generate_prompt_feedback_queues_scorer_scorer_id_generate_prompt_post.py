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
from ...models.generate_prompt_response import GeneratePromptResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(scorer_id: str) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/feedback-queues/scorer/{scorer_id}/generate-prompt".format(scorer_id=scorer_id),
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> GeneratePromptResponse | HTTPValidationError:
    if response.status_code == 202:
        response_202 = GeneratePromptResponse.from_dict(response.json())

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
) -> Response[GeneratePromptResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(scorer_id: str, *, client: ApiClient) -> Response[GeneratePromptResponse | HTTPValidationError]:
    """Generate Prompt

     Generate improved scorer prompt using Autotune (CLHF).

    This endpoint:
    1. Fetches all feedback items from the active queue with ClickHouse context
    2. Assembles the current metric system prompt
    3. Constructs AutotuneInput with annotated examples
    4. Queues a background job to the runners service
    5. Returns task_id for polling

    The API prepares all data internally - no request body needed.

    **Validation:**
    - Scorer exists and user has access
    - Active queue exists in 'pending' state
    - Queue has at least one feedback item

    **Response:**
    - 202 Accepted with task_id for polling

    **Errors:**
    - 404 - Scorer not found or no active pending queue exists
    - 409 - Queue is already locked (generating or reviewing)
    - 422 - Scorer missing required configuration or queue has no feedback items

    Args:
        scorer_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GeneratePromptResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(scorer_id=scorer_id)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(scorer_id: str, *, client: ApiClient) -> Optional[GeneratePromptResponse | HTTPValidationError]:
    """Generate Prompt

     Generate improved scorer prompt using Autotune (CLHF).

    This endpoint:
    1. Fetches all feedback items from the active queue with ClickHouse context
    2. Assembles the current metric system prompt
    3. Constructs AutotuneInput with annotated examples
    4. Queues a background job to the runners service
    5. Returns task_id for polling

    The API prepares all data internally - no request body needed.

    **Validation:**
    - Scorer exists and user has access
    - Active queue exists in 'pending' state
    - Queue has at least one feedback item

    **Response:**
    - 202 Accepted with task_id for polling

    **Errors:**
    - 404 - Scorer not found or no active pending queue exists
    - 409 - Queue is already locked (generating or reviewing)
    - 422 - Scorer missing required configuration or queue has no feedback items

    Args:
        scorer_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GeneratePromptResponse | HTTPValidationError
    """

    return sync_detailed(scorer_id=scorer_id, client=client).parsed


async def asyncio_detailed(
    scorer_id: str, *, client: ApiClient
) -> Response[GeneratePromptResponse | HTTPValidationError]:
    """Generate Prompt

     Generate improved scorer prompt using Autotune (CLHF).

    This endpoint:
    1. Fetches all feedback items from the active queue with ClickHouse context
    2. Assembles the current metric system prompt
    3. Constructs AutotuneInput with annotated examples
    4. Queues a background job to the runners service
    5. Returns task_id for polling

    The API prepares all data internally - no request body needed.

    **Validation:**
    - Scorer exists and user has access
    - Active queue exists in 'pending' state
    - Queue has at least one feedback item

    **Response:**
    - 202 Accepted with task_id for polling

    **Errors:**
    - 404 - Scorer not found or no active pending queue exists
    - 409 - Queue is already locked (generating or reviewing)
    - 422 - Scorer missing required configuration or queue has no feedback items

    Args:
        scorer_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GeneratePromptResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(scorer_id=scorer_id)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(scorer_id: str, *, client: ApiClient) -> Optional[GeneratePromptResponse | HTTPValidationError]:
    """Generate Prompt

     Generate improved scorer prompt using Autotune (CLHF).

    This endpoint:
    1. Fetches all feedback items from the active queue with ClickHouse context
    2. Assembles the current metric system prompt
    3. Constructs AutotuneInput with annotated examples
    4. Queues a background job to the runners service
    5. Returns task_id for polling

    The API prepares all data internally - no request body needed.

    **Validation:**
    - Scorer exists and user has access
    - Active queue exists in 'pending' state
    - Queue has at least one feedback item

    **Response:**
    - 202 Accepted with task_id for polling

    **Errors:**
    - 404 - Scorer not found or no active pending queue exists
    - 409 - Queue is already locked (generating or reviewing)
    - 422 - Scorer missing required configuration or queue has no feedback items

    Args:
        scorer_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GeneratePromptResponse | HTTPValidationError
    """

    return (await asyncio_detailed(scorer_id=scorer_id, client=client)).parsed
