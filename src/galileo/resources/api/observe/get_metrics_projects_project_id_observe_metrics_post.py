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
from ...models.filters_request_body import FiltersRequestBody
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    *,
    body: FiltersRequestBody | Unset,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    interval: int | Unset = 5,
    group_by: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_start_time = start_time.isoformat()
    params["start_time"] = json_start_time

    json_end_time = end_time.isoformat()
    params["end_time"] = json_end_time

    params["interval"] = interval

    json_group_by: None | str | Unset
    if isinstance(group_by, Unset):
        json_group_by = UNSET
    else:
        json_group_by = group_by
    params["group_by"] = json_group_by

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/projects/{project_id}/observe/metrics".format(project_id=project_id),
        "params": params,
    }

    _kwargs["json"]: dict[str, Any] | Unset = UNSET
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError:
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


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[HTTPValidationError]:
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
    body: FiltersRequestBody | Unset,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    interval: int | Unset = 5,
    group_by: None | str | Unset = UNSET,
) -> Response[HTTPValidationError]:
    """Get Metrics

    Args:
        project_id (str):
        start_time (datetime.datetime):
        end_time (datetime.datetime):
        interval (int | Unset):  Default: 5.
        group_by (None | str | Unset):
        body (FiltersRequestBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        project_id=project_id, body=body, start_time=start_time, end_time=end_time, interval=interval, group_by=group_by
    )

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: ApiClient,
    body: FiltersRequestBody | Unset,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    interval: int | Unset = 5,
    group_by: None | str | Unset = UNSET,
) -> Optional[HTTPValidationError]:
    """Get Metrics

    Args:
        project_id (str):
        start_time (datetime.datetime):
        end_time (datetime.datetime):
        interval (int | Unset):  Default: 5.
        group_by (None | str | Unset):
        body (FiltersRequestBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
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
    client: ApiClient,
    body: FiltersRequestBody | Unset,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    interval: int | Unset = 5,
    group_by: None | str | Unset = UNSET,
) -> Response[HTTPValidationError]:
    """Get Metrics

    Args:
        project_id (str):
        start_time (datetime.datetime):
        end_time (datetime.datetime):
        interval (int | Unset):  Default: 5.
        group_by (None | str | Unset):
        body (FiltersRequestBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        project_id=project_id, body=body, start_time=start_time, end_time=end_time, interval=interval, group_by=group_by
    )

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: ApiClient,
    body: FiltersRequestBody | Unset,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    interval: int | Unset = 5,
    group_by: None | str | Unset = UNSET,
) -> Optional[HTTPValidationError]:
    """Get Metrics

    Args:
        project_id (str):
        start_time (datetime.datetime):
        end_time (datetime.datetime):
        interval (int | Unset):  Default: 5.
        group_by (None | str | Unset):
        body (FiltersRequestBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
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
