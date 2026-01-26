from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo.exceptions import (
    AuthenticationError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from galileo.utils.headers_data import get_sdk_header
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.dataset_action import DatasetAction
from ...models.http_validation_error import HTTPValidationError
from ...models.list_dataset_params import ListDatasetParams
from ...models.list_dataset_response import ListDatasetResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ListDatasetParams,
    actions: Union[Unset, list[DatasetAction]] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_actions: Union[Unset, list[str]] = UNSET
    if not isinstance(actions, Unset):
        json_actions = []
        for actions_item_data in actions:
            actions_item = actions_item_data.value
            json_actions.append(actions_item)

    params["actions"] = json_actions

    params["starting_token"] = starting_token

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/datasets/query",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Union[HTTPValidationError, ListDatasetResponse]:
    if response.status_code == 200:
        return ListDatasetResponse.from_dict(response.json())

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

    # Handle common HTTP errors with actionable messages
    if response.status_code == 400:
        raise BadRequestError(response.status_code, response.content)
    if response.status_code == 401:
        raise AuthenticationError(response.status_code, response.content)
    if response.status_code == 403:
        raise ForbiddenError(response.status_code, response.content)
    if response.status_code == 404:
        raise NotFoundError(response.status_code, response.content)
    if response.status_code == 409:
        raise ConflictError(response.status_code, response.content)
    if response.status_code == 429:
        raise RateLimitError(response.status_code, response.content)
    if response.status_code >= 500:
        raise ServerError(response.status_code, response.content)
    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[Union[HTTPValidationError, ListDatasetResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: ApiClient,
    body: ListDatasetParams,
    actions: Union[Unset, list[DatasetAction]] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, ListDatasetResponse]]:
    """Query Datasets.

    Args:
        actions (Union[Unset, list[DatasetAction]]): Actions to include in the 'permissions'
            field.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (ListDatasetParams):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, ListDatasetResponse]]
    """
    kwargs = _get_kwargs(body=body, actions=actions, starting_token=starting_token, limit=limit)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *,
    client: ApiClient,
    body: ListDatasetParams,
    actions: Union[Unset, list[DatasetAction]] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, ListDatasetResponse]]:
    """Query Datasets.

    Args:
        actions (Union[Unset, list[DatasetAction]]): Actions to include in the 'permissions'
            field.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (ListDatasetParams):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, ListDatasetResponse]
    """
    return sync_detailed(client=client, body=body, actions=actions, starting_token=starting_token, limit=limit).parsed


async def asyncio_detailed(
    *,
    client: ApiClient,
    body: ListDatasetParams,
    actions: Union[Unset, list[DatasetAction]] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, ListDatasetResponse]]:
    """Query Datasets.

    Args:
        actions (Union[Unset, list[DatasetAction]]): Actions to include in the 'permissions'
            field.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (ListDatasetParams):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, ListDatasetResponse]]
    """
    kwargs = _get_kwargs(body=body, actions=actions, starting_token=starting_token, limit=limit)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: ApiClient,
    body: ListDatasetParams,
    actions: Union[Unset, list[DatasetAction]] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, ListDatasetResponse]]:
    """Query Datasets.

    Args:
        actions (Union[Unset, list[DatasetAction]]): Actions to include in the 'permissions'
            field.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        body (ListDatasetParams):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, ListDatasetResponse]
    """
    return (
        await asyncio_detailed(client=client, body=body, actions=actions, starting_token=starting_token, limit=limit)
    ).parsed
