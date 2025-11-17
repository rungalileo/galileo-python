from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo.utils.headers_data import get_sdk_header
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.http_validation_error import HTTPValidationError
from ...models.log_stream_create_request import LogStreamCreateRequest
from ...models.log_stream_response import LogStreamResponse
from ...types import Response


def _get_kwargs(project_id: str, *, body: LogStreamCreateRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": f"/projects/{project_id}/log_streams",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[Union[HTTPValidationError, LogStreamResponse]]:
    if response.status_code == 200:
        return LogStreamResponse.from_dict(response.json())

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[Union[HTTPValidationError, LogStreamResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, *, client: ApiClient, body: LogStreamCreateRequest
) -> Response[Union[HTTPValidationError, LogStreamResponse]]:
    """Create Log Stream.

     Create a new log stream for a project.

    Args:
        project_id (str):
        body (LogStreamCreateRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, LogStreamResponse]]
    """
    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, *, client: ApiClient, body: LogStreamCreateRequest
) -> Optional[Union[HTTPValidationError, LogStreamResponse]]:
    """Create Log Stream.

     Create a new log stream for a project.

    Args:
        project_id (str):
        body (LogStreamCreateRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, LogStreamResponse]
    """
    return sync_detailed(project_id=project_id, client=client, body=body).parsed


async def asyncio_detailed(
    project_id: str, *, client: ApiClient, body: LogStreamCreateRequest
) -> Response[Union[HTTPValidationError, LogStreamResponse]]:
    """Create Log Stream.

     Create a new log stream for a project.

    Args:
        project_id (str):
        body (LogStreamCreateRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, LogStreamResponse]]
    """
    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, *, client: ApiClient, body: LogStreamCreateRequest
) -> Optional[Union[HTTPValidationError, LogStreamResponse]]:
    """Create Log Stream.

     Create a new log stream for a project.

    Args:
        project_id (str):
        body (LogStreamCreateRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, LogStreamResponse]
    """
    return (await asyncio_detailed(project_id=project_id, client=client, body=body)).parsed
