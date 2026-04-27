from http import HTTPStatus
from typing import Any, Optional

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
from ...models.model_with_prices import ModelWithPrices
from ...types import UNSET, Response, Unset


def _get_kwargs(*, search: None | str | Unset = UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_search: None | str | Unset
    if isinstance(search, Unset):
        json_search = UNSET
    else:
        json_search = search
    params["search"] = json_search

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/models",
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | list[ModelWithPrices]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ModelWithPrices.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

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
) -> Response[HTTPValidationError | list[ModelWithPrices]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, search: None | str | Unset = UNSET
) -> Response[HTTPValidationError | list[ModelWithPrices]]:
    """List Models

     Lists models and their prices.

    Notes:
    - The list of models used in the organization is cached and refreshed periodically.
    - All models with price overrides are listed, even if they have not been used.

    Args:
        search (None | str | Unset): Filter by model name substring

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ModelWithPrices]]
    """

    kwargs = _get_kwargs(search=search)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, search: None | str | Unset = UNSET
) -> Optional[HTTPValidationError | list[ModelWithPrices]]:
    """List Models

     Lists models and their prices.

    Notes:
    - The list of models used in the organization is cached and refreshed periodically.
    - All models with price overrides are listed, even if they have not been used.

    Args:
        search (None | str | Unset): Filter by model name substring

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ModelWithPrices]
    """

    return sync_detailed(client=client, search=search).parsed


async def asyncio_detailed(
    *, client: ApiClient, search: None | str | Unset = UNSET
) -> Response[HTTPValidationError | list[ModelWithPrices]]:
    """List Models

     Lists models and their prices.

    Notes:
    - The list of models used in the organization is cached and refreshed periodically.
    - All models with price overrides are listed, even if they have not been used.

    Args:
        search (None | str | Unset): Filter by model name substring

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ModelWithPrices]]
    """

    kwargs = _get_kwargs(search=search)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, search: None | str | Unset = UNSET
) -> Optional[HTTPValidationError | list[ModelWithPrices]]:
    """List Models

     Lists models and their prices.

    Notes:
    - The list of models used in the organization is cached and refreshed periodically.
    - All models with price overrides are listed, even if they have not been used.

    Args:
        search (None | str | Unset): Filter by model name substring

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ModelWithPrices]
    """

    return (await asyncio_detailed(client=client, search=search)).parsed
