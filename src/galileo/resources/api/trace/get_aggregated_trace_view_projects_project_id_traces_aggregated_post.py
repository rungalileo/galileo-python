from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.aggregated_trace_view_request import AggregatedTraceViewRequest
from ...models.aggregated_trace_view_response import AggregatedTraceViewResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(project_id: str, *, body: AggregatedTraceViewRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": "post", "url": f"/projects/{project_id}/traces/aggregated"}

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AggregatedTraceViewResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = AggregatedTraceViewResponse.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[AggregatedTraceViewResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, *, client: AuthenticatedClient, body: AggregatedTraceViewRequest
) -> Response[Union[AggregatedTraceViewResponse, HTTPValidationError]]:
    """Get Aggregated Trace View

    Args:
        project_id (str):
        body (AggregatedTraceViewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AggregatedTraceViewResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, *, client: AuthenticatedClient, body: AggregatedTraceViewRequest
) -> Optional[Union[AggregatedTraceViewResponse, HTTPValidationError]]:
    """Get Aggregated Trace View

    Args:
        project_id (str):
        body (AggregatedTraceViewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AggregatedTraceViewResponse, HTTPValidationError]
    """

    return sync_detailed(project_id=project_id, client=client, body=body).parsed


async def asyncio_detailed(
    project_id: str, *, client: AuthenticatedClient, body: AggregatedTraceViewRequest
) -> Response[Union[AggregatedTraceViewResponse, HTTPValidationError]]:
    """Get Aggregated Trace View

    Args:
        project_id (str):
        body (AggregatedTraceViewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AggregatedTraceViewResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, *, client: AuthenticatedClient, body: AggregatedTraceViewRequest
) -> Optional[Union[AggregatedTraceViewResponse, HTTPValidationError]]:
    """Get Aggregated Trace View

    Args:
        project_id (str):
        body (AggregatedTraceViewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AggregatedTraceViewResponse, HTTPValidationError]
    """

    return (await asyncio_detailed(project_id=project_id, client=client, body=body)).parsed
