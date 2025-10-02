from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.bulk_delete_datasets_request import BulkDeleteDatasetsRequest
from ...models.bulk_delete_datasets_response import BulkDeleteDatasetsResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(*, body: BulkDeleteDatasetsRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.DELETE,
        "return_raw_response": True,
        "path": "/datasets/bulk_delete",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[Union[BulkDeleteDatasetsResponse, HTTPValidationError]]:
    if response.status_code == 200:
        return BulkDeleteDatasetsResponse.from_dict(response.json())

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[Union[BulkDeleteDatasetsResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, body: BulkDeleteDatasetsRequest
) -> Response[Union[BulkDeleteDatasetsResponse, HTTPValidationError]]:
    """Bulk Delete Datasets

     Delete multiple datasets in bulk.

    This endpoint allows efficient deletion of multiple datasets at once.
    It validates permissions for each dataset in the service and provides detailed feedback about
    successful and failed deletions for each dataset.

    Parameters
    ----------
    delete_request : BulkDeleteDatasetsRequest
        Request containing list of dataset IDs to delete (max 100)
    ctx : Context
        Request context including authentication information

    Returns
    -------
    BulkDeleteDatasetsResponse
        Details about the bulk deletion operation including:
        - Number of successfully deleted datasets
        - List of failed deletions with reasons
        - Summary message

    Args:
        body (BulkDeleteDatasetsRequest): Request to delete multiple datasets.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BulkDeleteDatasetsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, body: BulkDeleteDatasetsRequest
) -> Optional[Union[BulkDeleteDatasetsResponse, HTTPValidationError]]:
    """Bulk Delete Datasets

     Delete multiple datasets in bulk.

    This endpoint allows efficient deletion of multiple datasets at once.
    It validates permissions for each dataset in the service and provides detailed feedback about
    successful and failed deletions for each dataset.

    Parameters
    ----------
    delete_request : BulkDeleteDatasetsRequest
        Request containing list of dataset IDs to delete (max 100)
    ctx : Context
        Request context including authentication information

    Returns
    -------
    BulkDeleteDatasetsResponse
        Details about the bulk deletion operation including:
        - Number of successfully deleted datasets
        - List of failed deletions with reasons
        - Summary message

    Args:
        body (BulkDeleteDatasetsRequest): Request to delete multiple datasets.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BulkDeleteDatasetsResponse, HTTPValidationError]
    """

    return sync_detailed(client=client, body=body).parsed


async def asyncio_detailed(
    *, client: ApiClient, body: BulkDeleteDatasetsRequest
) -> Response[Union[BulkDeleteDatasetsResponse, HTTPValidationError]]:
    """Bulk Delete Datasets

     Delete multiple datasets in bulk.

    This endpoint allows efficient deletion of multiple datasets at once.
    It validates permissions for each dataset in the service and provides detailed feedback about
    successful and failed deletions for each dataset.

    Parameters
    ----------
    delete_request : BulkDeleteDatasetsRequest
        Request containing list of dataset IDs to delete (max 100)
    ctx : Context
        Request context including authentication information

    Returns
    -------
    BulkDeleteDatasetsResponse
        Details about the bulk deletion operation including:
        - Number of successfully deleted datasets
        - List of failed deletions with reasons
        - Summary message

    Args:
        body (BulkDeleteDatasetsRequest): Request to delete multiple datasets.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BulkDeleteDatasetsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, body: BulkDeleteDatasetsRequest
) -> Optional[Union[BulkDeleteDatasetsResponse, HTTPValidationError]]:
    """Bulk Delete Datasets

     Delete multiple datasets in bulk.

    This endpoint allows efficient deletion of multiple datasets at once.
    It validates permissions for each dataset in the service and provides detailed feedback about
    successful and failed deletions for each dataset.

    Parameters
    ----------
    delete_request : BulkDeleteDatasetsRequest
        Request containing list of dataset IDs to delete (max 100)
    ctx : Context
        Request context including authentication information

    Returns
    -------
    BulkDeleteDatasetsResponse
        Details about the bulk deletion operation including:
        - Number of successfully deleted datasets
        - List of failed deletions with reasons
        - Summary message

    Args:
        body (BulkDeleteDatasetsRequest): Request to delete multiple datasets.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BulkDeleteDatasetsResponse, HTTPValidationError]
    """

    return (await asyncio_detailed(client=client, body=body)).parsed
