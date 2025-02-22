from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.workflows_ingest_request import WorkflowsIngestRequest
from ...models.workflows_ingest_response import WorkflowsIngestResponse
from ...types import Response


def _get_kwargs(*, body: WorkflowsIngestRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": "post", "url": "/v1/observe/workflows"}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, WorkflowsIngestResponse]]:
    if response.status_code == 200:
        response_200 = WorkflowsIngestResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, WorkflowsIngestResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, body: WorkflowsIngestRequest
) -> Response[Union[HTTPValidationError, WorkflowsIngestResponse]]:
    """Log Workflows

     Log workflows to an Observe project.

    Use this endpoint to log workflows to an Observe project. The request body should contain the
    `workflows` to be ingested.

    Additionally, specify the `project_id` or `project_name` to which the workflows should be ingested.
    If the project does not exist, it will be created. If the project exists, the workflows will be
    logged to it.
    If both `project_id` and `project_name` are provided, `project_id` will take precedence.

    Args:
        body (WorkflowsIngestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, WorkflowsIngestResponse]]
    """

    kwargs = _get_kwargs(body=body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient, body: WorkflowsIngestRequest
) -> Optional[Union[HTTPValidationError, WorkflowsIngestResponse]]:
    """Log Workflows

     Log workflows to an Observe project.

    Use this endpoint to log workflows to an Observe project. The request body should contain the
    `workflows` to be ingested.

    Additionally, specify the `project_id` or `project_name` to which the workflows should be ingested.
    If the project does not exist, it will be created. If the project exists, the workflows will be
    logged to it.
    If both `project_id` and `project_name` are provided, `project_id` will take precedence.

    Args:
        body (WorkflowsIngestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, WorkflowsIngestResponse]
    """

    return sync_detailed(client=client, body=body).parsed


async def asyncio_detailed(
    *, client: AuthenticatedClient, body: WorkflowsIngestRequest
) -> Response[Union[HTTPValidationError, WorkflowsIngestResponse]]:
    """Log Workflows

     Log workflows to an Observe project.

    Use this endpoint to log workflows to an Observe project. The request body should contain the
    `workflows` to be ingested.

    Additionally, specify the `project_id` or `project_name` to which the workflows should be ingested.
    If the project does not exist, it will be created. If the project exists, the workflows will be
    logged to it.
    If both `project_id` and `project_name` are provided, `project_id` will take precedence.

    Args:
        body (WorkflowsIngestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, WorkflowsIngestResponse]]
    """

    kwargs = _get_kwargs(body=body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, body: WorkflowsIngestRequest
) -> Optional[Union[HTTPValidationError, WorkflowsIngestResponse]]:
    """Log Workflows

     Log workflows to an Observe project.

    Use this endpoint to log workflows to an Observe project. The request body should contain the
    `workflows` to be ingested.

    Additionally, specify the `project_id` or `project_name` to which the workflows should be ingested.
    If the project does not exist, it will be created. If the project exists, the workflows will be
    logged to it.
    If both `project_id` and `project_name` are provided, `project_id` will take precedence.

    Args:
        body (WorkflowsIngestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, WorkflowsIngestResponse]
    """

    return (await asyncio_detailed(client=client, body=body)).parsed
