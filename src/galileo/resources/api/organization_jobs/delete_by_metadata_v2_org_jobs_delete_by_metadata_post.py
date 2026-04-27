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
from ...models.org_metadata_delete_request import OrgMetadataDeleteRequest
from ...models.org_metadata_delete_response import OrgMetadataDeleteResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(*, body: OrgMetadataDeleteRequest, immediate: bool | Unset = False) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["immediate"] = immediate

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/v2/org-jobs/delete-by-metadata",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | OrgMetadataDeleteResponse:
    if response.status_code == 200:
        response_200 = OrgMetadataDeleteResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | OrgMetadataDeleteResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, body: OrgMetadataDeleteRequest, immediate: bool | Unset = False
) -> Response[HTTPValidationError | OrgMetadataDeleteResponse]:
    """Delete By Metadata

     Delete traces/sessions across all projects in the organization by metadata filters.

    This endpoint allows organization administrators to delete traces or sessions
    that match specific metadata key-value pairs across all projects in their
    organization.

    Args:
        immediate (bool | Unset):  Default: False.
        body (OrgMetadataDeleteRequest): Request body for organization-wide metadata-based
            deletion.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | OrgMetadataDeleteResponse]
    """

    kwargs = _get_kwargs(body=body, immediate=immediate)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, body: OrgMetadataDeleteRequest, immediate: bool | Unset = False
) -> Optional[HTTPValidationError | OrgMetadataDeleteResponse]:
    """Delete By Metadata

     Delete traces/sessions across all projects in the organization by metadata filters.

    This endpoint allows organization administrators to delete traces or sessions
    that match specific metadata key-value pairs across all projects in their
    organization.

    Args:
        immediate (bool | Unset):  Default: False.
        body (OrgMetadataDeleteRequest): Request body for organization-wide metadata-based
            deletion.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | OrgMetadataDeleteResponse
    """

    return sync_detailed(client=client, body=body, immediate=immediate).parsed


async def asyncio_detailed(
    *, client: ApiClient, body: OrgMetadataDeleteRequest, immediate: bool | Unset = False
) -> Response[HTTPValidationError | OrgMetadataDeleteResponse]:
    """Delete By Metadata

     Delete traces/sessions across all projects in the organization by metadata filters.

    This endpoint allows organization administrators to delete traces or sessions
    that match specific metadata key-value pairs across all projects in their
    organization.

    Args:
        immediate (bool | Unset):  Default: False.
        body (OrgMetadataDeleteRequest): Request body for organization-wide metadata-based
            deletion.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | OrgMetadataDeleteResponse]
    """

    kwargs = _get_kwargs(body=body, immediate=immediate)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, body: OrgMetadataDeleteRequest, immediate: bool | Unset = False
) -> Optional[HTTPValidationError | OrgMetadataDeleteResponse]:
    """Delete By Metadata

     Delete traces/sessions across all projects in the organization by metadata filters.

    This endpoint allows organization administrators to delete traces or sessions
    that match specific metadata key-value pairs across all projects in their
    organization.

    Args:
        immediate (bool | Unset):  Default: False.
        body (OrgMetadataDeleteRequest): Request body for organization-wide metadata-based
            deletion.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | OrgMetadataDeleteResponse
    """

    return (await asyncio_detailed(client=client, body=body, immediate=immediate)).parsed
