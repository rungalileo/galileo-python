from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_prompt_rows_columnar_response import GetPromptRowsColumnarResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.prompt_filter_params import PromptFilterParams
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    run_id: str,
    *,
    body: PromptFilterParams,
    sort_by: Union[Unset, str] = "_id",
    sort_ascending: Union[Unset, bool] = True,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["sort_by"] = sort_by

    params["sort_ascending"] = sort_ascending

    params["starting_token"] = starting_token

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/projects/{project_id}/runs/{run_id}/prompts/rows/columnar",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetPromptRowsColumnarResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GetPromptRowsColumnarResponse.from_dict(response.json())

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
) -> Response[Union[GetPromptRowsColumnarResponse, HTTPValidationError]]:
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
    body: PromptFilterParams,
    sort_by: Union[Unset, str] = "_id",
    sort_ascending: Union[Unset, bool] = True,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[GetPromptRowsColumnarResponse, HTTPValidationError]]:
    """Get Rows As Columns With Filters

    Args:
        project_id (str):
        run_id (str):
        sort_by (Union[Unset, str]):  Default: '_id'.
        sort_ascending (Union[Unset, bool]):  Default: True.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (PromptFilterParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetPromptRowsColumnarResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        body=body,
        sort_by=sort_by,
        sort_ascending=sort_ascending,
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
    body: PromptFilterParams,
    sort_by: Union[Unset, str] = "_id",
    sort_ascending: Union[Unset, bool] = True,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[GetPromptRowsColumnarResponse, HTTPValidationError]]:
    """Get Rows As Columns With Filters

    Args:
        project_id (str):
        run_id (str):
        sort_by (Union[Unset, str]):  Default: '_id'.
        sort_ascending (Union[Unset, bool]):  Default: True.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (PromptFilterParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetPromptRowsColumnarResponse, HTTPValidationError]
    """

    return sync_detailed(
        project_id=project_id,
        run_id=run_id,
        client=client,
        body=body,
        sort_by=sort_by,
        sort_ascending=sort_ascending,
        starting_token=starting_token,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    run_id: str,
    *,
    client: AuthenticatedClient,
    body: PromptFilterParams,
    sort_by: Union[Unset, str] = "_id",
    sort_ascending: Union[Unset, bool] = True,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[GetPromptRowsColumnarResponse, HTTPValidationError]]:
    """Get Rows As Columns With Filters

    Args:
        project_id (str):
        run_id (str):
        sort_by (Union[Unset, str]):  Default: '_id'.
        sort_ascending (Union[Unset, bool]):  Default: True.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (PromptFilterParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetPromptRowsColumnarResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        run_id=run_id,
        body=body,
        sort_by=sort_by,
        sort_ascending=sort_ascending,
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
    body: PromptFilterParams,
    sort_by: Union[Unset, str] = "_id",
    sort_ascending: Union[Unset, bool] = True,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[GetPromptRowsColumnarResponse, HTTPValidationError]]:
    """Get Rows As Columns With Filters

    Args:
        project_id (str):
        run_id (str):
        sort_by (Union[Unset, str]):  Default: '_id'.
        sort_ascending (Union[Unset, bool]):  Default: True.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (PromptFilterParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetPromptRowsColumnarResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            run_id=run_id,
            client=client,
            body=body,
            sort_by=sort_by,
            sort_ascending=sort_ascending,
            starting_token=starting_token,
            limit=limit,
        )
    ).parsed
