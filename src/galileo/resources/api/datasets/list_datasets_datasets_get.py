from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dataset_action import DatasetAction
from ...models.http_validation_error import HTTPValidationError
from ...models.list_dataset_response import ListDatasetResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    actions: Union[Unset, list[DatasetAction]] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> dict[str, Any]:
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

    _kwargs: dict[str, Any] = {"method": "get", "url": "/datasets", "params": params}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ListDatasetResponse]]:
    if response.status_code == 200:
        response_200 = ListDatasetResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ListDatasetResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    actions: Union[Unset, list[DatasetAction]] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, ListDatasetResponse]]:
    """List Datasets

    Args:
        actions (Union[Unset, list[DatasetAction]]): Actions to include in the 'permissions'
            field.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListDatasetResponse]]
    """

    kwargs = _get_kwargs(actions=actions, starting_token=starting_token, limit=limit)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    actions: Union[Unset, list[DatasetAction]] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, ListDatasetResponse]]:
    """List Datasets

    Args:
        actions (Union[Unset, list[DatasetAction]]): Actions to include in the 'permissions'
            field.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListDatasetResponse]
    """

    return sync_detailed(client=client, actions=actions, starting_token=starting_token, limit=limit).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    actions: Union[Unset, list[DatasetAction]] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, ListDatasetResponse]]:
    """List Datasets

    Args:
        actions (Union[Unset, list[DatasetAction]]): Actions to include in the 'permissions'
            field.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ListDatasetResponse]]
    """

    kwargs = _get_kwargs(actions=actions, starting_token=starting_token, limit=limit)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    actions: Union[Unset, list[DatasetAction]] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, ListDatasetResponse]]:
    """List Datasets

    Args:
        actions (Union[Unset, list[DatasetAction]]): Actions to include in the 'permissions'
            field.
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ListDatasetResponse]
    """

    return (await asyncio_detailed(client=client, actions=actions, starting_token=starting_token, limit=limit)).parsed
