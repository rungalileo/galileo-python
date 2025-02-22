from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_export_request import EditExportRequest
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(*, body: EditExportRequest, ignore_conflicting_edits: Union[Unset, bool] = True) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["ignore_conflicting_edits"] = ignore_conflicting_edits

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "post", "url": "/edits/export", "params": params}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = cast(Any, None)
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
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, body: EditExportRequest, ignore_conflicting_edits: Union[Unset, bool] = True
) -> Response[Union[Any, HTTPValidationError]]:
    """Export Edits

     Exports the resulting dataframe after a series of edits.

    If overrides are provided, and the original edit had a task, the override MUST explicitly have a
    task set (typically
    the same task as the edit)

    Args:
        ignore_conflicting_edits (Union[Unset, bool]):  Default: True.
        body (EditExportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(body=body, ignore_conflicting_edits=ignore_conflicting_edits)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient, body: EditExportRequest, ignore_conflicting_edits: Union[Unset, bool] = True
) -> Optional[Union[Any, HTTPValidationError]]:
    """Export Edits

     Exports the resulting dataframe after a series of edits.

    If overrides are provided, and the original edit had a task, the override MUST explicitly have a
    task set (typically
    the same task as the edit)

    Args:
        ignore_conflicting_edits (Union[Unset, bool]):  Default: True.
        body (EditExportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(client=client, body=body, ignore_conflicting_edits=ignore_conflicting_edits).parsed


async def asyncio_detailed(
    *, client: AuthenticatedClient, body: EditExportRequest, ignore_conflicting_edits: Union[Unset, bool] = True
) -> Response[Union[Any, HTTPValidationError]]:
    """Export Edits

     Exports the resulting dataframe after a series of edits.

    If overrides are provided, and the original edit had a task, the override MUST explicitly have a
    task set (typically
    the same task as the edit)

    Args:
        ignore_conflicting_edits (Union[Unset, bool]):  Default: True.
        body (EditExportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(body=body, ignore_conflicting_edits=ignore_conflicting_edits)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, body: EditExportRequest, ignore_conflicting_edits: Union[Unset, bool] = True
) -> Optional[Union[Any, HTTPValidationError]]:
    """Export Edits

     Exports the resulting dataframe after a series of edits.

    If overrides are provided, and the original edit had a task, the override MUST explicitly have a
    task set (typically
    the same task as the edit)

    Args:
        ignore_conflicting_edits (Union[Unset, bool]):  Default: True.
        body (EditExportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (await asyncio_detailed(client=client, body=body, ignore_conflicting_edits=ignore_conflicting_edits)).parsed
