from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.http_validation_error import HTTPValidationError
from ...models.project_collection_params import ProjectCollectionParams
from ...types import Response


def _get_kwargs(*, body: ProjectCollectionParams) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": RequestMethod.POST, "return_raw_response": True, "path": "/projects/count"}

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Optional[Union[HTTPValidationError, int]]:
    if response.status_code == 200:
        return cast(int, response.json())
    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[Union[HTTPValidationError, int]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(*, client: ApiClient, body: ProjectCollectionParams) -> Response[Union[HTTPValidationError, int]]:
    """Get Projects Count

     Gets total count of projects for a user with applied filters.

    Args:
        body (ProjectCollectionParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, int]]
    """

    kwargs = _get_kwargs(body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(*, client: ApiClient, body: ProjectCollectionParams) -> Optional[Union[HTTPValidationError, int]]:
    """Get Projects Count

     Gets total count of projects for a user with applied filters.

    Args:
        body (ProjectCollectionParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, int]
    """

    return sync_detailed(client=client, body=body).parsed


async def asyncio_detailed(
    *, client: ApiClient, body: ProjectCollectionParams
) -> Response[Union[HTTPValidationError, int]]:
    """Get Projects Count

     Gets total count of projects for a user with applied filters.

    Args:
        body (ProjectCollectionParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, int]]
    """

    kwargs = _get_kwargs(body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(*, client: ApiClient, body: ProjectCollectionParams) -> Optional[Union[HTTPValidationError, int]]:
    """Get Projects Count

     Gets total count of projects for a user with applied filters.

    Args:
        body (ProjectCollectionParams):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, int]
    """

    return (await asyncio_detailed(client=client, body=body)).parsed
