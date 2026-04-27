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
from ...models.put_prompt_score_request import PutPromptScoreRequest
from ...models.put_prompt_score_response import PutPromptScoreResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    run_id: str,
    scorer_name: str,
    *,
    body: PutPromptScoreRequest,
    monitor_batch_id: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_monitor_batch_id: None | str | Unset
    if isinstance(monitor_batch_id, Unset):
        json_monitor_batch_id = UNSET
    else:
        json_monitor_batch_id = monitor_batch_id
    params["monitor_batch_id"] = json_monitor_batch_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.PUT,
        "return_raw_response": True,
        "path": "/projects/{project_id}/runs/{run_id}/prompts/scorers/{scorer_name}".format(
            project_id=project_id, run_id=run_id, scorer_name=scorer_name
        ),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | PutPromptScoreResponse:
    if response.status_code == 200:
        response_200 = PutPromptScoreResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | PutPromptScoreResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    run_id: str,
    scorer_name: str,
    *,
    client: ApiClient,
    body: PutPromptScoreRequest,
    monitor_batch_id: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PutPromptScoreResponse]:
    """Put Score

    Args:
        project_id (str):
        run_id (str):
        scorer_name (str):
        monitor_batch_id (None | str | Unset):
        body (PutPromptScoreRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PutPromptScoreResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id, run_id=run_id, scorer_name=scorer_name, body=body, monitor_batch_id=monitor_batch_id
    )

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    run_id: str,
    scorer_name: str,
    *,
    client: ApiClient,
    body: PutPromptScoreRequest,
    monitor_batch_id: None | str | Unset = UNSET,
) -> Optional[HTTPValidationError | PutPromptScoreResponse]:
    """Put Score

    Args:
        project_id (str):
        run_id (str):
        scorer_name (str):
        monitor_batch_id (None | str | Unset):
        body (PutPromptScoreRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PutPromptScoreResponse
    """

    return sync_detailed(
        project_id=project_id,
        run_id=run_id,
        scorer_name=scorer_name,
        client=client,
        body=body,
        monitor_batch_id=monitor_batch_id,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    run_id: str,
    scorer_name: str,
    *,
    client: ApiClient,
    body: PutPromptScoreRequest,
    monitor_batch_id: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PutPromptScoreResponse]:
    """Put Score

    Args:
        project_id (str):
        run_id (str):
        scorer_name (str):
        monitor_batch_id (None | str | Unset):
        body (PutPromptScoreRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PutPromptScoreResponse]
    """

    kwargs = _get_kwargs(
        project_id=project_id, run_id=run_id, scorer_name=scorer_name, body=body, monitor_batch_id=monitor_batch_id
    )

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    run_id: str,
    scorer_name: str,
    *,
    client: ApiClient,
    body: PutPromptScoreRequest,
    monitor_batch_id: None | str | Unset = UNSET,
) -> Optional[HTTPValidationError | PutPromptScoreResponse]:
    """Put Score

    Args:
        project_id (str):
        run_id (str):
        scorer_name (str):
        monitor_batch_id (None | str | Unset):
        body (PutPromptScoreRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PutPromptScoreResponse
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            run_id=run_id,
            scorer_name=scorer_name,
            client=client,
            body=body,
            monitor_batch_id=monitor_batch_id,
        )
    ).parsed
