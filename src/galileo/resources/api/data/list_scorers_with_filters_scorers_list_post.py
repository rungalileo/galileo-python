from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo.utils.headers_data import get_sdk_header
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.http_validation_error import HTTPValidationError
from ...models.list_scorers_request import ListScorersRequest
from ...models.list_scorers_response import ListScorersResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, body: ListScorersRequest, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["starting_token"] = starting_token

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/scorers/list",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[Union[HTTPValidationError, ListScorersResponse]]:
    if response.status_code == 200:
        return ListScorersResponse.from_dict(response.json())

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[Union[HTTPValidationError, ListScorersResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: ApiClient,
    body: ListScorersRequest,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, ListScorersResponse]]:
    """List Scorers With Filters.

    Args:
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (ListScorersRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, ListScorersResponse]]
    """
    kwargs = _get_kwargs(body=body, starting_token=starting_token, limit=limit)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *,
    client: ApiClient,
    body: ListScorersRequest,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, ListScorersResponse]]:
    """List Scorers With Filters.

    Args:
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (ListScorersRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, ListScorersResponse]
    """
    return sync_detailed(client=client, body=body, starting_token=starting_token, limit=limit).parsed


async def asyncio_detailed(
    *,
    client: ApiClient,
    body: ListScorersRequest,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, ListScorersResponse]]:
    """List Scorers With Filters.

    Args:
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (ListScorersRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, ListScorersResponse]]
    """
    kwargs = _get_kwargs(body=body, starting_token=starting_token, limit=limit)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: ApiClient,
    body: ListScorersRequest,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, ListScorersResponse]]:
    """List Scorers With Filters.

    Args:
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (ListScorersRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, ListScorersResponse]
    """
    return (await asyncio_detailed(client=client, body=body, starting_token=starting_token, limit=limit)).parsed
