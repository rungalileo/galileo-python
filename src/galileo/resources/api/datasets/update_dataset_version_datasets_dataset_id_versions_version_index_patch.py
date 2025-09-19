from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.dataset_version_db import DatasetVersionDB
from ...models.http_validation_error import HTTPValidationError
from ...models.update_dataset_version_request import UpdateDatasetVersionRequest
from ...types import Response


def _get_kwargs(dataset_id: str, version_index: int, *, body: UpdateDatasetVersionRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.PATCH,
        "return_raw_response": True,
        "path": f"/datasets/{dataset_id}/versions/{version_index}",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[Union[DatasetVersionDB, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = DatasetVersionDB.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[Union[DatasetVersionDB, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_id: str, version_index: int, *, client: ApiClient, body: UpdateDatasetVersionRequest
) -> Response[Union[DatasetVersionDB, HTTPValidationError]]:
    """Update Dataset Version

    Args:
        dataset_id (str):
        version_index (int):
        body (UpdateDatasetVersionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DatasetVersionDB, HTTPValidationError]]
    """

    kwargs = _get_kwargs(dataset_id=dataset_id, version_index=version_index, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str, version_index: int, *, client: ApiClient, body: UpdateDatasetVersionRequest
) -> Optional[Union[DatasetVersionDB, HTTPValidationError]]:
    """Update Dataset Version

    Args:
        dataset_id (str):
        version_index (int):
        body (UpdateDatasetVersionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DatasetVersionDB, HTTPValidationError]
    """

    return sync_detailed(dataset_id=dataset_id, version_index=version_index, client=client, body=body).parsed


async def asyncio_detailed(
    dataset_id: str, version_index: int, *, client: ApiClient, body: UpdateDatasetVersionRequest
) -> Response[Union[DatasetVersionDB, HTTPValidationError]]:
    """Update Dataset Version

    Args:
        dataset_id (str):
        version_index (int):
        body (UpdateDatasetVersionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DatasetVersionDB, HTTPValidationError]]
    """

    kwargs = _get_kwargs(dataset_id=dataset_id, version_index=version_index, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str, version_index: int, *, client: ApiClient, body: UpdateDatasetVersionRequest
) -> Optional[Union[DatasetVersionDB, HTTPValidationError]]:
    """Update Dataset Version

    Args:
        dataset_id (str):
        version_index (int):
        body (UpdateDatasetVersionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DatasetVersionDB, HTTPValidationError]
    """

    return (await asyncio_detailed(dataset_id=dataset_id, version_index=version_index, client=client, body=body)).parsed
