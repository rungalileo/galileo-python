from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.databricks_unity_catalog_edit_export_request import DatabricksUnityCatalogEditExportRequest
from ...models.databricks_unity_catalog_export_edits_response import DatabricksUnityCatalogExportEditsResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *, body: DatabricksUnityCatalogEditExportRequest, ignore_conflicting_edits: Union[Unset, bool] = True
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["ignore_conflicting_edits"] = ignore_conflicting_edits

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/integrations/databricks/unity-catalog/edits/export",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[Union[DatabricksUnityCatalogExportEditsResponse, HTTPValidationError]]:
    if response.status_code == 200:
        return DatabricksUnityCatalogExportEditsResponse.from_dict(response.json())

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[Union[DatabricksUnityCatalogExportEditsResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: ApiClient,
    body: DatabricksUnityCatalogEditExportRequest,
    ignore_conflicting_edits: Union[Unset, bool] = True,
) -> Response[Union[DatabricksUnityCatalogExportEditsResponse, HTTPValidationError]]:
    """Export Edits Databricks Unity Catalog.

    Args:
        ignore_conflicting_edits (Union[Unset, bool]):  Default: True.
        body (DatabricksUnityCatalogEditExportRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[DatabricksUnityCatalogExportEditsResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(body=body, ignore_conflicting_edits=ignore_conflicting_edits)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *,
    client: ApiClient,
    body: DatabricksUnityCatalogEditExportRequest,
    ignore_conflicting_edits: Union[Unset, bool] = True,
) -> Optional[Union[DatabricksUnityCatalogExportEditsResponse, HTTPValidationError]]:
    """Export Edits Databricks Unity Catalog.

    Args:
        ignore_conflicting_edits (Union[Unset, bool]):  Default: True.
        body (DatabricksUnityCatalogEditExportRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[DatabricksUnityCatalogExportEditsResponse, HTTPValidationError]
    """
    return sync_detailed(client=client, body=body, ignore_conflicting_edits=ignore_conflicting_edits).parsed


async def asyncio_detailed(
    *,
    client: ApiClient,
    body: DatabricksUnityCatalogEditExportRequest,
    ignore_conflicting_edits: Union[Unset, bool] = True,
) -> Response[Union[DatabricksUnityCatalogExportEditsResponse, HTTPValidationError]]:
    """Export Edits Databricks Unity Catalog.

    Args:
        ignore_conflicting_edits (Union[Unset, bool]):  Default: True.
        body (DatabricksUnityCatalogEditExportRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[DatabricksUnityCatalogExportEditsResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(body=body, ignore_conflicting_edits=ignore_conflicting_edits)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: ApiClient,
    body: DatabricksUnityCatalogEditExportRequest,
    ignore_conflicting_edits: Union[Unset, bool] = True,
) -> Optional[Union[DatabricksUnityCatalogExportEditsResponse, HTTPValidationError]]:
    """Export Edits Databricks Unity Catalog.

    Args:
        ignore_conflicting_edits (Union[Unset, bool]):  Default: True.
        body (DatabricksUnityCatalogEditExportRequest):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[DatabricksUnityCatalogExportEditsResponse, HTTPValidationError]
    """
    return (await asyncio_detailed(client=client, body=body, ignore_conflicting_edits=ignore_conflicting_edits)).parsed
