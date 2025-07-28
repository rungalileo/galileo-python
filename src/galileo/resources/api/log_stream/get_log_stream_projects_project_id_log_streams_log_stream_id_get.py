from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.http_validation_error import HTTPValidationError
from ...models.log_stream_response import LogStreamResponse
from ...types import Response


def _get_kwargs(project_id: str, log_stream_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": f"/projects/{project_id}/log_streams/{log_stream_id}",
    }

    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[Union[HTTPValidationError, LogStreamResponse]]:
    if response.status_code == 200:
        response_200 = LogStreamResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, LogStreamResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, log_stream_id: str, *, client: ApiClient
) -> Response[Union[HTTPValidationError, LogStreamResponse]]:
    """Get Log Stream

     Retrieve a specific log stream.

    Args:
        project_id (str):
        log_stream_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogStreamResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, log_stream_id=log_stream_id)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, log_stream_id: str, *, client: ApiClient
) -> Optional[Union[HTTPValidationError, LogStreamResponse]]:
    """Get Log Stream

     Retrieve a specific log stream.

    Args:
        project_id (str):
        log_stream_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, LogStreamResponse]
    """

    return sync_detailed(project_id=project_id, log_stream_id=log_stream_id, client=client).parsed


async def asyncio_detailed(
    project_id: str, log_stream_id: str, *, client: ApiClient
) -> Response[Union[HTTPValidationError, LogStreamResponse]]:
    """Get Log Stream

     Retrieve a specific log stream.

    Args:
        project_id (str):
        log_stream_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LogStreamResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, log_stream_id=log_stream_id)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, log_stream_id: str, *, client: ApiClient
) -> Optional[Union[HTTPValidationError, LogStreamResponse]]:
    """Get Log Stream

     Retrieve a specific log stream.

    Args:
        project_id (str):
        log_stream_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, LogStreamResponse]
    """

    return (await asyncio_detailed(project_id=project_id, log_stream_id=log_stream_id, client=client)).parsed
