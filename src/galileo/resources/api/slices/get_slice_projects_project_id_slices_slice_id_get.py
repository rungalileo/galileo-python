from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.slice_db import SliceDB
from ...types import Response


def _get_kwargs(project_id: str, slice_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": f"/projects/{project_id}/slices/{slice_id}"}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, SliceDB]]:
    if response.status_code == 200:
        response_200 = SliceDB.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, SliceDB]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, slice_id: str, *, client: AuthenticatedClient
) -> Response[Union[HTTPValidationError, SliceDB]]:
    r"""Get Slice

     Gets a slice.

    The returned slice will have a \"logic\" field that will be directly usable in a ProcRequest
    (barring the run_id and
    Split. Those must be provided by the client).

    Args:
        project_id (str):
        slice_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SliceDB]]
    """

    kwargs = _get_kwargs(project_id=project_id, slice_id=slice_id)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, slice_id: str, *, client: AuthenticatedClient
) -> Optional[Union[HTTPValidationError, SliceDB]]:
    r"""Get Slice

     Gets a slice.

    The returned slice will have a \"logic\" field that will be directly usable in a ProcRequest
    (barring the run_id and
    Split. Those must be provided by the client).

    Args:
        project_id (str):
        slice_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SliceDB]
    """

    return sync_detailed(project_id=project_id, slice_id=slice_id, client=client).parsed


async def asyncio_detailed(
    project_id: str, slice_id: str, *, client: AuthenticatedClient
) -> Response[Union[HTTPValidationError, SliceDB]]:
    r"""Get Slice

     Gets a slice.

    The returned slice will have a \"logic\" field that will be directly usable in a ProcRequest
    (barring the run_id and
    Split. Those must be provided by the client).

    Args:
        project_id (str):
        slice_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SliceDB]]
    """

    kwargs = _get_kwargs(project_id=project_id, slice_id=slice_id)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, slice_id: str, *, client: AuthenticatedClient
) -> Optional[Union[HTTPValidationError, SliceDB]]:
    r"""Get Slice

     Gets a slice.

    The returned slice will have a \"logic\" field that will be directly usable in a ProcRequest
    (barring the run_id and
    Split. Those must be provided by the client).

    Args:
        project_id (str):
        slice_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SliceDB]
    """

    return (await asyncio_detailed(project_id=project_id, slice_id=slice_id, client=client)).parsed
