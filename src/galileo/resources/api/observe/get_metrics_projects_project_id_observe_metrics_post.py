import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.filters_request_body import FiltersRequestBody
from ...models.http_validation_error import HTTPValidationError
from ...models.transaction_metrics_response import TransactionMetricsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    *,
    body: FiltersRequestBody,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    interval: Union[Unset, int] = 5,
    group_by: Union[None, Unset, str] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_start_time = start_time.isoformat()
    params["start_time"] = json_start_time

    json_end_time = end_time.isoformat()
    params["end_time"] = json_end_time

    params["interval"] = interval

    json_group_by: Union[None, Unset, str]
    if isinstance(group_by, Unset):
        json_group_by = UNSET
    else:
        json_group_by = group_by
    params["group_by"] = json_group_by

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "post", "url": f"/projects/{project_id}/observe/metrics", "params": params}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, TransactionMetricsResponse]]:
    if response.status_code == 200:
        response_200 = TransactionMetricsResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, TransactionMetricsResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: FiltersRequestBody,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    interval: Union[Unset, int] = 5,
    group_by: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, TransactionMetricsResponse]]:
    """Get Metrics

    Args:
        project_id (str):
        start_time (datetime.datetime):
        end_time (datetime.datetime):
        interval (Union[Unset, int]):  Default: 5.
        group_by (Union[None, Unset, str]):
        body (FiltersRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TransactionMetricsResponse]]
    """

    kwargs = _get_kwargs(
        project_id=project_id, body=body, start_time=start_time, end_time=end_time, interval=interval, group_by=group_by
    )

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: FiltersRequestBody,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    interval: Union[Unset, int] = 5,
    group_by: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, TransactionMetricsResponse]]:
    """Get Metrics

    Args:
        project_id (str):
        start_time (datetime.datetime):
        end_time (datetime.datetime):
        interval (Union[Unset, int]):  Default: 5.
        group_by (Union[None, Unset, str]):
        body (FiltersRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TransactionMetricsResponse]
    """

    return sync_detailed(
        project_id=project_id,
        client=client,
        body=body,
        start_time=start_time,
        end_time=end_time,
        interval=interval,
        group_by=group_by,
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: FiltersRequestBody,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    interval: Union[Unset, int] = 5,
    group_by: Union[None, Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, TransactionMetricsResponse]]:
    """Get Metrics

    Args:
        project_id (str):
        start_time (datetime.datetime):
        end_time (datetime.datetime):
        interval (Union[Unset, int]):  Default: 5.
        group_by (Union[None, Unset, str]):
        body (FiltersRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TransactionMetricsResponse]]
    """

    kwargs = _get_kwargs(
        project_id=project_id, body=body, start_time=start_time, end_time=end_time, interval=interval, group_by=group_by
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    body: FiltersRequestBody,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    interval: Union[Unset, int] = 5,
    group_by: Union[None, Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, TransactionMetricsResponse]]:
    """Get Metrics

    Args:
        project_id (str):
        start_time (datetime.datetime):
        end_time (datetime.datetime):
        interval (Union[Unset, int]):  Default: 5.
        group_by (Union[None, Unset, str]):
        body (FiltersRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TransactionMetricsResponse]
    """

    return (
        await asyncio_detailed(
            project_id=project_id,
            client=client,
            body=body,
            start_time=start_time,
            end_time=end_time,
            interval=interval,
            group_by=group_by,
        )
    ).parsed
