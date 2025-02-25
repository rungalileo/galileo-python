import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.transaction_rows_request_body import TransactionRowsRequestBody
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    *,
    body: TransactionRowsRequestBody,
    start_time: Union[None, Unset, datetime.datetime] = UNSET,
    end_time: Union[None, Unset, datetime.datetime] = UNSET,
    chain_id: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    offset: Union[Unset, int] = 0,
    include_chains: Union[Unset, bool] = False,
    return_col_schema: Union[Unset, bool] = True,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_start_time: Union[None, Unset, str]
    if isinstance(start_time, Unset):
        json_start_time = UNSET
    elif isinstance(start_time, datetime.datetime):
        json_start_time = start_time.isoformat()
    else:
        json_start_time = start_time
    params["start_time"] = json_start_time

    json_end_time: Union[None, Unset, str]
    if isinstance(end_time, Unset):
        json_end_time = UNSET
    elif isinstance(end_time, datetime.datetime):
        json_end_time = end_time.isoformat()
    else:
        json_end_time = end_time
    params["end_time"] = json_end_time

    json_chain_id: Union[None, Unset, str]
    if isinstance(chain_id, Unset):
        json_chain_id = UNSET
    else:
        json_chain_id = chain_id
    params["chain_id"] = json_chain_id

    params["limit"] = limit

    params["offset"] = offset

    params["include_chains"] = include_chains

    params["return_col_schema"] = return_col_schema

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "post", "url": f"/projects/{project_id}/observe/rows", "params": params}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[HTTPValidationError]:
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[HTTPValidationError]:
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
    body: TransactionRowsRequestBody,
    start_time: Union[None, Unset, datetime.datetime] = UNSET,
    end_time: Union[None, Unset, datetime.datetime] = UNSET,
    chain_id: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    offset: Union[Unset, int] = 0,
    include_chains: Union[Unset, bool] = False,
    return_col_schema: Union[Unset, bool] = True,
) -> Response[HTTPValidationError]:
    """Get Rows

     Get all rows from monitor_records.

    Returns them in order of creation from newest to oldest.

    Args:
        project_id (str):
        start_time (Union[None, Unset, datetime.datetime]):
        end_time (Union[None, Unset, datetime.datetime]):
        chain_id (Union[None, Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        offset (Union[Unset, int]):  Default: 0.
        include_chains (Union[Unset, bool]):  Default: False.
        return_col_schema (Union[Unset, bool]):  Default: True.
        body (TransactionRowsRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
        start_time=start_time,
        end_time=end_time,
        chain_id=chain_id,
        limit=limit,
        offset=offset,
        include_chains=include_chains,
        return_col_schema=return_col_schema,
    )

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: TransactionRowsRequestBody,
    start_time: Union[None, Unset, datetime.datetime] = UNSET,
    end_time: Union[None, Unset, datetime.datetime] = UNSET,
    chain_id: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    offset: Union[Unset, int] = 0,
    include_chains: Union[Unset, bool] = False,
    return_col_schema: Union[Unset, bool] = True,
) -> Optional[HTTPValidationError]:
    """Get Rows

     Get all rows from monitor_records.

    Returns them in order of creation from newest to oldest.

    Args:
        project_id (str):
        start_time (Union[None, Unset, datetime.datetime]):
        end_time (Union[None, Unset, datetime.datetime]):
        chain_id (Union[None, Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        offset (Union[Unset, int]):  Default: 0.
        include_chains (Union[Unset, bool]):  Default: False.
        return_col_schema (Union[Unset, bool]):  Default: True.
        body (TransactionRowsRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        body=body,
        start_time=start_time,
        end_time=end_time,
        chain_id=chain_id,
        limit=limit,
        offset=offset,
        include_chains=include_chains,
        return_col_schema=return_col_schema,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: TransactionRowsRequestBody,
    start_time: Union[None, Unset, datetime.datetime] = UNSET,
    end_time: Union[None, Unset, datetime.datetime] = UNSET,
    chain_id: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    offset: Union[Unset, int] = 0,
    include_chains: Union[Unset, bool] = False,
    return_col_schema: Union[Unset, bool] = True,
) -> Response[HTTPValidationError]:
    """Get Rows

     Get all rows from monitor_records.

    Returns them in order of creation from newest to oldest.

    Args:
        project_id (str):
        start_time (Union[None, Unset, datetime.datetime]):
        end_time (Union[None, Unset, datetime.datetime]):
        chain_id (Union[None, Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        offset (Union[Unset, int]):  Default: 0.
        include_chains (Union[Unset, bool]):  Default: False.
        return_col_schema (Union[Unset, bool]):  Default: True.
        body (TransactionRowsRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        project_id=project_id,
        body=body,
        start_time=start_time,
        end_time=end_time,
        chain_id=chain_id,
        limit=limit,
        offset=offset,
        include_chains=include_chains,
        return_col_schema=return_col_schema,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: TransactionRowsRequestBody,
    start_time: Union[None, Unset, datetime.datetime] = UNSET,
    end_time: Union[None, Unset, datetime.datetime] = UNSET,
    chain_id: Union[None, Unset, str] = UNSET,
    limit: Union[Unset, int] = 50,
    offset: Union[Unset, int] = 0,
    include_chains: Union[Unset, bool] = False,
    return_col_schema: Union[Unset, bool] = True,
) -> Optional[HTTPValidationError]:
    """Get Rows

     Get all rows from monitor_records.

    Returns them in order of creation from newest to oldest.

    Args:
        project_id (str):
        start_time (Union[None, Unset, datetime.datetime]):
        end_time (Union[None, Unset, datetime.datetime]):
        chain_id (Union[None, Unset, str]):
        limit (Union[Unset, int]):  Default: 50.
        offset (Union[Unset, int]):  Default: 0.
        include_chains (Union[Unset, bool]):  Default: False.
        return_col_schema (Union[Unset, bool]):  Default: True.
        body (TransactionRowsRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            body=body,
            start_time=start_time,
            end_time=end_time,
            chain_id=chain_id,
            limit=limit,
            offset=offset,
            include_chains=include_chains,
            return_col_schema=return_col_schema,
        )
    ).parsed
