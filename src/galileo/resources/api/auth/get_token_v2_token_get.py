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
from ...models.get_token_response import GetTokenResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, organization_id: None | str | Unset = UNSET, organization_slug: None | str | Unset = UNSET
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_organization_id: None | str | Unset
    if isinstance(organization_id, Unset):
        json_organization_id = UNSET
    else:
        json_organization_id = organization_id
    params["organization_id"] = json_organization_id

    json_organization_slug: None | str | Unset
    if isinstance(organization_slug, Unset):
        json_organization_slug = UNSET
    else:
        json_organization_slug = organization_slug
    params["organization_slug"] = json_organization_slug

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/v2/token",
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> GetTokenResponse | HTTPValidationError:
    if response.status_code == 200:
        response_200 = GetTokenResponse.from_dict(response.json())

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


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[GetTokenResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, organization_id: None | str | Unset = UNSET, organization_slug: None | str | Unset = UNSET
) -> Response[GetTokenResponse | HTTPValidationError]:
    """Get Token

    Args:
        organization_id (None | str | Unset):
        organization_slug (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetTokenResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(organization_id=organization_id, organization_slug=organization_slug)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, organization_id: None | str | Unset = UNSET, organization_slug: None | str | Unset = UNSET
) -> Optional[GetTokenResponse | HTTPValidationError]:
    """Get Token

    Args:
        organization_id (None | str | Unset):
        organization_slug (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetTokenResponse | HTTPValidationError
    """

    return sync_detailed(client=client, organization_id=organization_id, organization_slug=organization_slug).parsed


async def asyncio_detailed(
    *, client: ApiClient, organization_id: None | str | Unset = UNSET, organization_slug: None | str | Unset = UNSET
) -> Response[GetTokenResponse | HTTPValidationError]:
    """Get Token

    Args:
        organization_id (None | str | Unset):
        organization_slug (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetTokenResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(organization_id=organization_id, organization_slug=organization_slug)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, organization_id: None | str | Unset = UNSET, organization_slug: None | str | Unset = UNSET
) -> Optional[GetTokenResponse | HTTPValidationError]:
    """Get Token

    Args:
        organization_id (None | str | Unset):
        organization_slug (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetTokenResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(client=client, organization_id=organization_id, organization_slug=organization_slug)
    ).parsed
