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
from ...models.http_validation_error import HTTPValidationError
from ...models.list_user_collaborators_response import ListUserCollaboratorsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    dataset_id: str, *, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["starting_token"] = starting_token

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": f"/datasets/{dataset_id}/users",
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Union[HTTPValidationError, ListUserCollaboratorsResponse]:
    if response.status_code == 200:
        return ListUserCollaboratorsResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ListUserCollaboratorsResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_id: str, *, client: ApiClient, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> Response[Union[HTTPValidationError, ListUserCollaboratorsResponse]]:
    """List User Dataset Collaborators.

     List the users with which the dataset has been shared.

    Args:
        dataset_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, ListUserCollaboratorsResponse]]
    """
    kwargs = _get_kwargs(dataset_id=dataset_id, starting_token=starting_token, limit=limit)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str, *, client: ApiClient, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> Optional[Union[HTTPValidationError, ListUserCollaboratorsResponse]]:
    """List User Dataset Collaborators.

     List the users with which the dataset has been shared.

    Args:
        dataset_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, ListUserCollaboratorsResponse]
    """
    return sync_detailed(dataset_id=dataset_id, client=client, starting_token=starting_token, limit=limit).parsed


async def asyncio_detailed(
    dataset_id: str, *, client: ApiClient, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> Response[Union[HTTPValidationError, ListUserCollaboratorsResponse]]:
    """List User Dataset Collaborators.

     List the users with which the dataset has been shared.

    Args:
        dataset_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, ListUserCollaboratorsResponse]]
    """
    kwargs = _get_kwargs(dataset_id=dataset_id, starting_token=starting_token, limit=limit)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str, *, client: ApiClient, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> Optional[Union[HTTPValidationError, ListUserCollaboratorsResponse]]:
    """List User Dataset Collaborators.

     List the users with which the dataset has been shared.

    Args:
        dataset_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, ListUserCollaboratorsResponse]
    """
    return (
        await asyncio_detailed(dataset_id=dataset_id, client=client, starting_token=starting_token, limit=limit)
    ).parsed
