from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.split import Split
from ...models.threshold_request import ThresholdRequest
from ...models.threshold_response import ThresholdResponse
from ...types import Response


def _get_kwargs(project_id: str, run_id: str, split: Split, *, body: ThresholdRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/projects/{project_id}/runs/{run_id}/split/{split}/insights/thresholds",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ThresholdResponse]]:
    if response.status_code == 200:
        response_200 = ThresholdResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ThresholdResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, run_id: str, split: Split, *, client: AuthenticatedClient, body: ThresholdRequest
) -> Response[Union[HTTPValidationError, ThresholdResponse]]:
    """Get Thresholds

     Gets the DEP score hard/easy thresholds for a project/run/split.

    If in a multi-label model, you must provide a task

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        body (ThresholdRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ThresholdResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, split=split, body=body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, run_id: str, split: Split, *, client: AuthenticatedClient, body: ThresholdRequest
) -> Optional[Union[HTTPValidationError, ThresholdResponse]]:
    """Get Thresholds

     Gets the DEP score hard/easy thresholds for a project/run/split.

    If in a multi-label model, you must provide a task

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        body (ThresholdRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ThresholdResponse]
    """

    return sync_detailed(project_id=project_id, run_id=run_id, split=split, client=client, body=body).parsed


async def asyncio_detailed(
    project_id: str, run_id: str, split: Split, *, client: AuthenticatedClient, body: ThresholdRequest
) -> Response[Union[HTTPValidationError, ThresholdResponse]]:
    """Get Thresholds

     Gets the DEP score hard/easy thresholds for a project/run/split.

    If in a multi-label model, you must provide a task

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        body (ThresholdRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ThresholdResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, split=split, body=body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, run_id: str, split: Split, *, client: AuthenticatedClient, body: ThresholdRequest
) -> Optional[Union[HTTPValidationError, ThresholdResponse]]:
    """Get Thresholds

     Gets the DEP score hard/easy thresholds for a project/run/split.

    If in a multi-label model, you must provide a task

    Args:
        project_id (str):
        run_id (str):
        split (Split):
        body (ThresholdRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ThresholdResponse]
    """

    return (await asyncio_detailed(project_id=project_id, run_id=run_id, split=split, client=client, body=body)).parsed
