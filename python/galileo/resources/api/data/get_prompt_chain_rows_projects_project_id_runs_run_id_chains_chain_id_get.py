from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_prompt_rows_response import GetPromptRowsResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.task_type import TaskType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str, run_id: str, chain_id: str, *, task_type: Union[Unset, TaskType] = UNSET
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_task_type: Union[Unset, int] = UNSET
    if not isinstance(task_type, Unset):
        json_task_type = task_type.value

    params["task_type"] = json_task_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/runs/{run_id}/chains/{chain_id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetPromptRowsResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GetPromptRowsResponse.from_dict(response.json())

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
) -> Response[Union[GetPromptRowsResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    run_id: str,
    chain_id: str,
    *,
    client: AuthenticatedClient,
    task_type: Union[Unset, TaskType] = UNSET,
) -> Response[Union[GetPromptRowsResponse, HTTPValidationError]]:
    """Get Prompt Chain Rows

    Args:
        project_id (str):
        run_id (str):
        chain_id (str):
        task_type (Union[Unset, TaskType]): Valid task types for modeling.

            We store these as ints instead of strings because we will be looking this up in the
            database frequently.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetPromptRowsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, chain_id=chain_id, task_type=task_type)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    run_id: str,
    chain_id: str,
    *,
    client: AuthenticatedClient,
    task_type: Union[Unset, TaskType] = UNSET,
) -> Optional[Union[GetPromptRowsResponse, HTTPValidationError]]:
    """Get Prompt Chain Rows

    Args:
        project_id (str):
        run_id (str):
        chain_id (str):
        task_type (Union[Unset, TaskType]): Valid task types for modeling.

            We store these as ints instead of strings because we will be looking this up in the
            database frequently.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetPromptRowsResponse, HTTPValidationError]
    """

    return sync_detailed(
        project_id=project_id, run_id=run_id, chain_id=chain_id, client=client, task_type=task_type
    ).parsed


async def asyncio_detailed(
    project_id: str,
    run_id: str,
    chain_id: str,
    *,
    client: AuthenticatedClient,
    task_type: Union[Unset, TaskType] = UNSET,
) -> Response[Union[GetPromptRowsResponse, HTTPValidationError]]:
    """Get Prompt Chain Rows

    Args:
        project_id (str):
        run_id (str):
        chain_id (str):
        task_type (Union[Unset, TaskType]): Valid task types for modeling.

            We store these as ints instead of strings because we will be looking this up in the
            database frequently.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetPromptRowsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, chain_id=chain_id, task_type=task_type)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    run_id: str,
    chain_id: str,
    *,
    client: AuthenticatedClient,
    task_type: Union[Unset, TaskType] = UNSET,
) -> Optional[Union[GetPromptRowsResponse, HTTPValidationError]]:
    """Get Prompt Chain Rows

    Args:
        project_id (str):
        run_id (str):
        chain_id (str):
        task_type (Union[Unset, TaskType]): Valid task types for modeling.

            We store these as ints instead of strings because we will be looking this up in the
            database frequently.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetPromptRowsResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            project_id=project_id, run_id=run_id, chain_id=chain_id, client=client, task_type=task_type
        )
    ).parsed
