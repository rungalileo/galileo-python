from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_prompt_run_columns_response import GetPromptRunColumnsResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    *,
    sort_by: Union[Unset, str] = "id",
    sort_ascending: Union[Unset, bool] = True,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["sort_by"] = sort_by

    params["sort_ascending"] = sort_ascending

    params["starting_token"] = starting_token

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/prompts/runs/columnar",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetPromptRunColumnsResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GetPromptRunColumnsResponse.from_dict(response.json())

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
) -> Response[Union[GetPromptRunColumnsResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    sort_by: Union[Unset, str] = "id",
    sort_ascending: Union[Unset, bool] = True,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[GetPromptRunColumnsResponse, HTTPValidationError]]:
    """Get Project Prompt Runs As Columns

     Gets all prompt runs for a project in a columnar format.

    This is different from get_project_prompt_runs because it:
    1. Returns results in a columnar format instead of a key-value pair of arrays.
    2. Includes metadata about each of the columns.
    3. Includes mappings to each column's display names and super column names.

    Args:
        project_id (str):
        sort_by (Union[Unset, str]):  Default: 'id'.
        sort_ascending (Union[Unset, bool]):  Default: True.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetPromptRunColumnsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        sort_by=sort_by,
        sort_ascending=sort_ascending,
        starting_token=starting_token,
        limit=limit,
    )

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    sort_by: Union[Unset, str] = "id",
    sort_ascending: Union[Unset, bool] = True,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[GetPromptRunColumnsResponse, HTTPValidationError]]:
    """Get Project Prompt Runs As Columns

     Gets all prompt runs for a project in a columnar format.

    This is different from get_project_prompt_runs because it:
    1. Returns results in a columnar format instead of a key-value pair of arrays.
    2. Includes metadata about each of the columns.
    3. Includes mappings to each column's display names and super column names.

    Args:
        project_id (str):
        sort_by (Union[Unset, str]):  Default: 'id'.
        sort_ascending (Union[Unset, bool]):  Default: True.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetPromptRunColumnsResponse, HTTPValidationError]
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        sort_by=sort_by,
        sort_ascending=sort_ascending,
        starting_token=starting_token,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    sort_by: Union[Unset, str] = "id",
    sort_ascending: Union[Unset, bool] = True,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[GetPromptRunColumnsResponse, HTTPValidationError]]:
    """Get Project Prompt Runs As Columns

     Gets all prompt runs for a project in a columnar format.

    This is different from get_project_prompt_runs because it:
    1. Returns results in a columnar format instead of a key-value pair of arrays.
    2. Includes metadata about each of the columns.
    3. Includes mappings to each column's display names and super column names.

    Args:
        project_id (str):
        sort_by (Union[Unset, str]):  Default: 'id'.
        sort_ascending (Union[Unset, bool]):  Default: True.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetPromptRunColumnsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        sort_by=sort_by,
        sort_ascending=sort_ascending,
        starting_token=starting_token,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    sort_by: Union[Unset, str] = "id",
    sort_ascending: Union[Unset, bool] = True,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[GetPromptRunColumnsResponse, HTTPValidationError]]:
    """Get Project Prompt Runs As Columns

     Gets all prompt runs for a project in a columnar format.

    This is different from get_project_prompt_runs because it:
    1. Returns results in a columnar format instead of a key-value pair of arrays.
    2. Includes metadata about each of the columns.
    3. Includes mappings to each column's display names and super column names.

    Args:
        project_id (str):
        sort_by (Union[Unset, str]):  Default: 'id'.
        sort_ascending (Union[Unset, bool]):  Default: True.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetPromptRunColumnsResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            sort_by=sort_by,
            sort_ascending=sort_ascending,
            starting_token=starting_token,
            limit=limit,
        )
    ).parsed
