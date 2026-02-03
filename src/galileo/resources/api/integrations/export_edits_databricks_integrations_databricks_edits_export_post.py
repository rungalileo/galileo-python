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
from ...models.databricks_edit_export_request import DatabricksEditExportRequest
from ...models.databricks_edit_export_response import DatabricksEditExportResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, body: DatabricksEditExportRequest, ignore_conflicting_edits: Union[Unset, bool] = True
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["ignore_conflicting_edits"] = ignore_conflicting_edits

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/integrations/databricks/edits/export",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Union[DatabricksEditExportResponse, HTTPValidationError]:
    if response.status_code == 200:
        return DatabricksEditExportResponse.from_dict(response.json())

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
) -> Response[Union[DatabricksEditExportResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, body: DatabricksEditExportRequest, ignore_conflicting_edits: Union[Unset, bool] = True
) -> Response[Union[DatabricksEditExportResponse, HTTPValidationError]]:
    """Export Edits Databricks.

     Exports the resulting dataframe after a series of edits to databricks delta lake.

    If overrides are provided, and the original edit had a task, the override MUST explicitly have a
    task set (typically
    the same task as the edit)

    Args:
        ignore_conflicting_edits (Union[Unset, bool]):  Default: True.
        body (DatabricksEditExportRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[DatabricksEditExportResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(body=body, ignore_conflicting_edits=ignore_conflicting_edits)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, body: DatabricksEditExportRequest, ignore_conflicting_edits: Union[Unset, bool] = True
) -> Optional[Union[DatabricksEditExportResponse, HTTPValidationError]]:
    """Export Edits Databricks.

     Exports the resulting dataframe after a series of edits to databricks delta lake.

    If overrides are provided, and the original edit had a task, the override MUST explicitly have a
    task set (typically
    the same task as the edit)

    Args:
        ignore_conflicting_edits (Union[Unset, bool]):  Default: True.
        body (DatabricksEditExportRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[DatabricksEditExportResponse, HTTPValidationError]
    """
    return sync_detailed(client=client, body=body, ignore_conflicting_edits=ignore_conflicting_edits).parsed


async def asyncio_detailed(
    *, client: ApiClient, body: DatabricksEditExportRequest, ignore_conflicting_edits: Union[Unset, bool] = True
) -> Response[Union[DatabricksEditExportResponse, HTTPValidationError]]:
    """Export Edits Databricks.

     Exports the resulting dataframe after a series of edits to databricks delta lake.

    If overrides are provided, and the original edit had a task, the override MUST explicitly have a
    task set (typically
    the same task as the edit)

    Args:
        ignore_conflicting_edits (Union[Unset, bool]):  Default: True.
        body (DatabricksEditExportRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[DatabricksEditExportResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(body=body, ignore_conflicting_edits=ignore_conflicting_edits)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, body: DatabricksEditExportRequest, ignore_conflicting_edits: Union[Unset, bool] = True
) -> Optional[Union[DatabricksEditExportResponse, HTTPValidationError]]:
    """Export Edits Databricks.

     Exports the resulting dataframe after a series of edits to databricks delta lake.

    If overrides are provided, and the original edit had a task, the override MUST explicitly have a
    task set (typically
    the same task as the edit)

    Args:
        ignore_conflicting_edits (Union[Unset, bool]):  Default: True.
        body (DatabricksEditExportRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[DatabricksEditExportResponse, HTTPValidationError]
    """
    return (await asyncio_detailed(client=client, body=body, ignore_conflicting_edits=ignore_conflicting_edits)).parsed
