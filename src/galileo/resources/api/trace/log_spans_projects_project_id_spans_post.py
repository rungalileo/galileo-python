from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.http_validation_error import HTTPValidationError
from ...models.log_spans_ingest_request import LogSpansIngestRequest
from ...models.log_spans_ingest_response import LogSpansIngestResponse
from ...types import Response


def _get_kwargs(project_id: str, *, body: LogSpansIngestRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": f"/projects/{project_id}/spans",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[Union[HTTPValidationError, LogSpansIngestResponse]]:
    if response.status_code == 200:
        response_200 = LogSpansIngestResponse.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[Union[HTTPValidationError, LogSpansIngestResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, *, client: ApiClient, body: LogSpansIngestRequest
) -> Response[Union[HTTPValidationError, LogSpansIngestResponse]]:
    """Log Spans

    Args:
        project_id (str):
        body (LogSpansIngestRequest): Request model for ingesting spans.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogSpansIngestResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, *, client: ApiClient, body: LogSpansIngestRequest
) -> Optional[Union[HTTPValidationError, LogSpansIngestResponse]]:
    """Log Spans

    Args:
        project_id (str):
        body (LogSpansIngestRequest): Request model for ingesting spans.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, LogSpansIngestResponse]
    """

    return sync_detailed(project_id=project_id, client=client, body=body).parsed


async def asyncio_detailed(
    project_id: str, *, client: ApiClient, body: LogSpansIngestRequest
) -> Response[Union[HTTPValidationError, LogSpansIngestResponse]]:
    """Log Spans

    Args:
        project_id (str):
        body (LogSpansIngestRequest): Request model for ingesting spans.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogSpansIngestResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, *, client: ApiClient, body: LogSpansIngestRequest
) -> Optional[Union[HTTPValidationError, LogSpansIngestResponse]]:
    """Log Spans

    Args:
        project_id (str):
        body (LogSpansIngestRequest): Request model for ingesting spans.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, LogSpansIngestResponse]
    """

    return (await asyncio_detailed(project_id=project_id, client=client, body=body)).parsed
