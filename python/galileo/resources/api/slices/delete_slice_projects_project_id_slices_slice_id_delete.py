from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.slice_delete_response import SliceDeleteResponse
from ...types import Response


def _get_kwargs(project_id: str, slice_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "delete", "url": f"/projects/{project_id}/slices/{slice_id}"}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, SliceDeleteResponse]]:
    if response.status_code == 200:
        response_200 = SliceDeleteResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, SliceDeleteResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, slice_id: str, *, client: AuthenticatedClient
) -> Response[Union[HTTPValidationError, SliceDeleteResponse]]:
    """Delete Slice

    Args:
        project_id (str):
        slice_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SliceDeleteResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, slice_id=slice_id)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, slice_id: str, *, client: AuthenticatedClient
) -> Optional[Union[HTTPValidationError, SliceDeleteResponse]]:
    """Delete Slice

    Args:
        project_id (str):
        slice_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SliceDeleteResponse]
    """

    return sync_detailed(project_id=project_id, slice_id=slice_id, client=client).parsed


async def asyncio_detailed(
    project_id: str, slice_id: str, *, client: AuthenticatedClient
) -> Response[Union[HTTPValidationError, SliceDeleteResponse]]:
    """Delete Slice

    Args:
        project_id (str):
        slice_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SliceDeleteResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, slice_id=slice_id)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, slice_id: str, *, client: AuthenticatedClient
) -> Optional[Union[HTTPValidationError, SliceDeleteResponse]]:
    """Delete Slice

    Args:
        project_id (str):
        slice_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SliceDeleteResponse]
    """

    return (await asyncio_detailed(project_id=project_id, slice_id=slice_id, client=client)).parsed
