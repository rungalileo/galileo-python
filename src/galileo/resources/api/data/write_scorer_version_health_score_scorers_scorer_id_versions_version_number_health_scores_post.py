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
from ...models.scorer_version_health_score_entry import ScorerVersionHealthScoreEntry
from ...models.write_health_score_request import WriteHealthScoreRequest
from ...types import Response


def _get_kwargs(scorer_id: str, version_number: int, *, body: WriteHealthScoreRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/scorers/{scorer_id}/versions/{version_number}/health-scores".format(
            scorer_id=scorer_id, version_number=version_number
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Union[HTTPValidationError, ScorerVersionHealthScoreEntry]:
    if response.status_code == 200:
        response_200 = ScorerVersionHealthScoreEntry.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ScorerVersionHealthScoreEntry]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    scorer_id: str, version_number: int, *, client: ApiClient, body: WriteHealthScoreRequest
) -> Response[Union[HTTPValidationError, ScorerVersionHealthScoreEntry]]:
    """Write Scorer Version Health Score

     Persist the health score for a scorer version against a dataset.

    Called by the UI after saving a metric version, passing the score from the last compute.

    Args:
        scorer_id (str):
        version_number (int):
        body (WriteHealthScoreRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ScorerVersionHealthScoreEntry]]
    """

    kwargs = _get_kwargs(scorer_id=scorer_id, version_number=version_number, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    scorer_id: str, version_number: int, *, client: ApiClient, body: WriteHealthScoreRequest
) -> Optional[Union[HTTPValidationError, ScorerVersionHealthScoreEntry]]:
    """Write Scorer Version Health Score

     Persist the health score for a scorer version against a dataset.

    Called by the UI after saving a metric version, passing the score from the last compute.

    Args:
        scorer_id (str):
        version_number (int):
        body (WriteHealthScoreRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ScorerVersionHealthScoreEntry]
    """

    return sync_detailed(scorer_id=scorer_id, version_number=version_number, client=client, body=body).parsed


async def asyncio_detailed(
    scorer_id: str, version_number: int, *, client: ApiClient, body: WriteHealthScoreRequest
) -> Response[Union[HTTPValidationError, ScorerVersionHealthScoreEntry]]:
    """Write Scorer Version Health Score

     Persist the health score for a scorer version against a dataset.

    Called by the UI after saving a metric version, passing the score from the last compute.

    Args:
        scorer_id (str):
        version_number (int):
        body (WriteHealthScoreRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ScorerVersionHealthScoreEntry]]
    """

    kwargs = _get_kwargs(scorer_id=scorer_id, version_number=version_number, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    scorer_id: str, version_number: int, *, client: ApiClient, body: WriteHealthScoreRequest
) -> Optional[Union[HTTPValidationError, ScorerVersionHealthScoreEntry]]:
    """Write Scorer Version Health Score

     Persist the health score for a scorer version against a dataset.

    Called by the UI after saving a metric version, passing the score from the last compute.

    Args:
        scorer_id (str):
        version_number (int):
        body (WriteHealthScoreRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ScorerVersionHealthScoreEntry]
    """

    return (await asyncio_detailed(scorer_id=scorer_id, version_number=version_number, client=client, body=body)).parsed
