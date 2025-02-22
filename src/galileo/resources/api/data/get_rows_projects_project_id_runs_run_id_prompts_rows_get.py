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
    project_id: str,
    run_id: str,
    *,
    task_type: Union[Unset, TaskType] = UNSET,
    sort_by: Union[Unset, str] = "_id",
    sort_ascending: Union[Unset, bool] = True,
    text_column: Union[None, Unset, str] = UNSET,
    text_pattern: Union[None, Unset, str] = UNSET,
    regex: Union[Unset, bool] = False,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_task_type: Union[Unset, int] = UNSET
    if not isinstance(task_type, Unset):
        json_task_type = task_type.value

    params["task_type"] = json_task_type

    params["sort_by"] = sort_by

    params["sort_ascending"] = sort_ascending

    json_text_column: Union[None, Unset, str]
    if isinstance(text_column, Unset):
        json_text_column = UNSET
    else:
        json_text_column = text_column
    params["text_column"] = json_text_column

    json_text_pattern: Union[None, Unset, str]
    if isinstance(text_pattern, Unset):
        json_text_pattern = UNSET
    else:
        json_text_pattern = text_pattern
    params["text_pattern"] = json_text_pattern

    params["regex"] = regex

    params["starting_token"] = starting_token

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/runs/{run_id}/prompts/rows",
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
    *,
    client: AuthenticatedClient,
    task_type: Union[Unset, TaskType] = UNSET,
    sort_by: Union[Unset, str] = "_id",
    sort_ascending: Union[Unset, bool] = True,
    text_column: Union[None, Unset, str] = UNSET,
    text_pattern: Union[None, Unset, str] = UNSET,
    regex: Union[Unset, bool] = False,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[GetPromptRowsResponse, HTTPValidationError]]:
    """Get Rows

    Args:
        project_id (str):
        run_id (str):
        task_type (Union[Unset, TaskType]): Valid task types for modeling.

            We store these as ints instead of strings because we will be looking this up in the
            database frequently.
        sort_by (Union[Unset, str]):  Default: '_id'.
        sort_ascending (Union[Unset, bool]):  Default: True.
        text_column (Union[None, Unset, str]):
        text_pattern (Union[None, Unset, str]):
        regex (Union[Unset, bool]):  Default: False.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetPromptRowsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        task_type=task_type,
        sort_by=sort_by,
        sort_ascending=sort_ascending,
        text_column=text_column,
        text_pattern=text_pattern,
        regex=regex,
        starting_token=starting_token,
        limit=limit,
    )

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    run_id: str,
    *,
    client: AuthenticatedClient,
    task_type: Union[Unset, TaskType] = UNSET,
    sort_by: Union[Unset, str] = "_id",
    sort_ascending: Union[Unset, bool] = True,
    text_column: Union[None, Unset, str] = UNSET,
    text_pattern: Union[None, Unset, str] = UNSET,
    regex: Union[Unset, bool] = False,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[GetPromptRowsResponse, HTTPValidationError]]:
    """Get Rows

    Args:
        project_id (str):
        run_id (str):
        task_type (Union[Unset, TaskType]): Valid task types for modeling.

            We store these as ints instead of strings because we will be looking this up in the
            database frequently.
        sort_by (Union[Unset, str]):  Default: '_id'.
        sort_ascending (Union[Unset, bool]):  Default: True.
        text_column (Union[None, Unset, str]):
        text_pattern (Union[None, Unset, str]):
        regex (Union[Unset, bool]):  Default: False.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetPromptRowsResponse, HTTPValidationError]
    """

    return sync_detailed(
        project_id=project_id,
        run_id=run_id,
        client=client,
        task_type=task_type,
        sort_by=sort_by,
        sort_ascending=sort_ascending,
        text_column=text_column,
        text_pattern=text_pattern,
        regex=regex,
        starting_token=starting_token,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    run_id: str,
    *,
    client: AuthenticatedClient,
    task_type: Union[Unset, TaskType] = UNSET,
    sort_by: Union[Unset, str] = "_id",
    sort_ascending: Union[Unset, bool] = True,
    text_column: Union[None, Unset, str] = UNSET,
    text_pattern: Union[None, Unset, str] = UNSET,
    regex: Union[Unset, bool] = False,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[GetPromptRowsResponse, HTTPValidationError]]:
    """Get Rows

    Args:
        project_id (str):
        run_id (str):
        task_type (Union[Unset, TaskType]): Valid task types for modeling.

            We store these as ints instead of strings because we will be looking this up in the
            database frequently.
        sort_by (Union[Unset, str]):  Default: '_id'.
        sort_ascending (Union[Unset, bool]):  Default: True.
        text_column (Union[None, Unset, str]):
        text_pattern (Union[None, Unset, str]):
        regex (Union[Unset, bool]):  Default: False.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetPromptRowsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        task_type=task_type,
        sort_by=sort_by,
        sort_ascending=sort_ascending,
        text_column=text_column,
        text_pattern=text_pattern,
        regex=regex,
        starting_token=starting_token,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    run_id: str,
    *,
    client: AuthenticatedClient,
    task_type: Union[Unset, TaskType] = UNSET,
    sort_by: Union[Unset, str] = "_id",
    sort_ascending: Union[Unset, bool] = True,
    text_column: Union[None, Unset, str] = UNSET,
    text_pattern: Union[None, Unset, str] = UNSET,
    regex: Union[Unset, bool] = False,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[GetPromptRowsResponse, HTTPValidationError]]:
    """Get Rows

    Args:
        project_id (str):
        run_id (str):
        task_type (Union[Unset, TaskType]): Valid task types for modeling.

            We store these as ints instead of strings because we will be looking this up in the
            database frequently.
        sort_by (Union[Unset, str]):  Default: '_id'.
        sort_ascending (Union[Unset, bool]):  Default: True.
        text_column (Union[None, Unset, str]):
        text_pattern (Union[None, Unset, str]):
        regex (Union[Unset, bool]):  Default: False.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetPromptRowsResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            run_id=run_id,
            client=client,
            task_type=task_type,
            sort_by=sort_by,
            sort_ascending=sort_ascending,
            text_column=text_column,
            text_pattern=text_pattern,
            regex=regex,
            starting_token=starting_token,
            limit=limit,
        )
    ).parsed
