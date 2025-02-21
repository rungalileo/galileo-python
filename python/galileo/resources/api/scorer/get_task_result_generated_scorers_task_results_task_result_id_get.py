from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.generated_scorer_task_result_response import GeneratedScorerTaskResultResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(task_result_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": f"/generated-scorers/task-results/{task_result_id}"}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GeneratedScorerTaskResultResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GeneratedScorerTaskResultResponse.from_dict(response.json())

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
) -> Response[Union[GeneratedScorerTaskResultResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    task_result_id: str, *, client: AuthenticatedClient
) -> Response[Union[GeneratedScorerTaskResultResponse, HTTPValidationError]]:
    """Get Task Result

    Args:
        task_result_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GeneratedScorerTaskResultResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(task_result_id=task_result_id)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    task_result_id: str, *, client: AuthenticatedClient
) -> Optional[Union[GeneratedScorerTaskResultResponse, HTTPValidationError]]:
    """Get Task Result

    Args:
        task_result_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GeneratedScorerTaskResultResponse, HTTPValidationError]
    """

    return sync_detailed(task_result_id=task_result_id, client=client).parsed


async def asyncio_detailed(
    task_result_id: str, *, client: AuthenticatedClient
) -> Response[Union[GeneratedScorerTaskResultResponse, HTTPValidationError]]:
    """Get Task Result

    Args:
        task_result_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GeneratedScorerTaskResultResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(task_result_id=task_result_id)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    task_result_id: str, *, client: AuthenticatedClient
) -> Optional[Union[GeneratedScorerTaskResultResponse, HTTPValidationError]]:
    """Get Task Result

    Args:
        task_result_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GeneratedScorerTaskResultResponse, HTTPValidationError]
    """

    return (await asyncio_detailed(task_result_id=task_result_id, client=client)).parsed
