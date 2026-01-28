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
from ...types import UNSET, Response, Unset


def _get_kwargs(scorer_id: str, *, version: Union[None, Unset, int] = UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_version: Union[None, Unset, int]
    json_version = UNSET if isinstance(version, Unset) else version
    params["version"] = json_version

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": f"/scorers/{scorer_id}/version/code",
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Union[Any, HTTPValidationError]:
    if response.status_code == 200:
        return response.json()

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


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    scorer_id: str, *, client: ApiClient, version: Union[None, Unset, int] = UNSET
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Scorer Version Code.

    Args:
        scorer_id (str):
        version (Union[None, Unset, int]): version number, defaults to latest version

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[Any, HTTPValidationError]]
    """
    kwargs = _get_kwargs(scorer_id=scorer_id, version=version)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    scorer_id: str, *, client: ApiClient, version: Union[None, Unset, int] = UNSET
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Scorer Version Code.

    Args:
        scorer_id (str):
        version (Union[None, Unset, int]): version number, defaults to latest version

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[Any, HTTPValidationError]
    """
    return sync_detailed(scorer_id=scorer_id, client=client, version=version).parsed


async def asyncio_detailed(
    scorer_id: str, *, client: ApiClient, version: Union[None, Unset, int] = UNSET
) -> Response[Union[Any, HTTPValidationError]]:
    """Get Scorer Version Code.

    Args:
        scorer_id (str):
        version (Union[None, Unset, int]): version number, defaults to latest version

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[Any, HTTPValidationError]]
    """
    kwargs = _get_kwargs(scorer_id=scorer_id, version=version)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    scorer_id: str, *, client: ApiClient, version: Union[None, Unset, int] = UNSET
) -> Optional[Union[Any, HTTPValidationError]]:
    """Get Scorer Version Code.

    Args:
        scorer_id (str):
        version (Union[None, Unset, int]): version number, defaults to latest version

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[Any, HTTPValidationError]
    """
    return (await asyncio_detailed(scorer_id=scorer_id, client=client, version=version)).parsed
