import datetime
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
from ...models.databricks_observe_export_request import DatabricksObserveExportRequest
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    *,
    body: DatabricksObserveExportRequest,
    start_time: datetime.datetime | None | Unset = UNSET,
    end_time: datetime.datetime | None | Unset = UNSET,
    chain_id: None | str | Unset = UNSET,
    test_set: bool | Unset = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_start_time: None | str | Unset
    if isinstance(start_time, Unset):
        json_start_time = UNSET
    elif isinstance(start_time, datetime.datetime):
        json_start_time = start_time.isoformat()
    else:
        json_start_time = start_time
    params["start_time"] = json_start_time

    json_end_time: None | str | Unset
    if isinstance(end_time, Unset):
        json_end_time = UNSET
    elif isinstance(end_time, datetime.datetime):
        json_end_time = end_time.isoformat()
    else:
        json_end_time = end_time
    params["end_time"] = json_end_time

    json_chain_id: None | str | Unset
    if isinstance(chain_id, Unset):
        json_chain_id = UNSET
    else:
        json_chain_id = chain_id
    params["chain_id"] = json_chain_id

    params["test_set"] = test_set

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/projects/{project_id}/observe/export/databricks".format(project_id=project_id),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Any | HTTPValidationError:
    if response.status_code == 200:
        response_200 = response.json()
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


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: ApiClient,
    body: DatabricksObserveExportRequest,
    start_time: datetime.datetime | None | Unset = UNSET,
    end_time: datetime.datetime | None | Unset = UNSET,
    chain_id: None | str | Unset = UNSET,
    test_set: bool | Unset = False,
) -> Response[Any | HTTPValidationError]:
    """Export Rows Databricks

     Export rows from monitor_records to databricks.

    Args:
        project_id (str):
        start_time (datetime.datetime | None | Unset):
        end_time (datetime.datetime | None | Unset):
        chain_id (None | str | Unset):
        test_set (bool | Unset):  Default: False.
        body (DatabricksObserveExportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        project_id=project_id, body=body, start_time=start_time, end_time=end_time, chain_id=chain_id, test_set=test_set
    )

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: ApiClient,
    body: DatabricksObserveExportRequest,
    start_time: datetime.datetime | None | Unset = UNSET,
    end_time: datetime.datetime | None | Unset = UNSET,
    chain_id: None | str | Unset = UNSET,
    test_set: bool | Unset = False,
) -> Optional[Any | HTTPValidationError]:
    """Export Rows Databricks

     Export rows from monitor_records to databricks.

    Args:
        project_id (str):
        start_time (datetime.datetime | None | Unset):
        end_time (datetime.datetime | None | Unset):
        chain_id (None | str | Unset):
        test_set (bool | Unset):  Default: False.
        body (DatabricksObserveExportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        body=body,
        start_time=start_time,
        end_time=end_time,
        chain_id=chain_id,
        test_set=test_set,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: ApiClient,
    body: DatabricksObserveExportRequest,
    start_time: datetime.datetime | None | Unset = UNSET,
    end_time: datetime.datetime | None | Unset = UNSET,
    chain_id: None | str | Unset = UNSET,
    test_set: bool | Unset = False,
) -> Response[Any | HTTPValidationError]:
    """Export Rows Databricks

     Export rows from monitor_records to databricks.

    Args:
        project_id (str):
        start_time (datetime.datetime | None | Unset):
        end_time (datetime.datetime | None | Unset):
        chain_id (None | str | Unset):
        test_set (bool | Unset):  Default: False.
        body (DatabricksObserveExportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        project_id=project_id, body=body, start_time=start_time, end_time=end_time, chain_id=chain_id, test_set=test_set
    )

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: ApiClient,
    body: DatabricksObserveExportRequest,
    start_time: datetime.datetime | None | Unset = UNSET,
    end_time: datetime.datetime | None | Unset = UNSET,
    chain_id: None | str | Unset = UNSET,
    test_set: bool | Unset = False,
) -> Optional[Any | HTTPValidationError]:
    """Export Rows Databricks

     Export rows from monitor_records to databricks.

    Args:
        project_id (str):
        start_time (datetime.datetime | None | Unset):
        end_time (datetime.datetime | None | Unset):
        chain_id (None | str | Unset):
        test_set (bool | Unset):  Default: False.
        body (DatabricksObserveExportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            body=body,
            start_time=start_time,
            end_time=end_time,
            chain_id=chain_id,
            test_set=test_set,
        )
    ).parsed
