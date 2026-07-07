import datetime
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
from ...models.cost_interval import CostInterval
from ...models.http_validation_error import HTTPValidationError
from ...models.integration_costs_response import IntegrationCostsResponse
from ...types import UNSET, Response


def _get_kwargs(
    *, start_time: datetime.datetime, end_time: datetime.datetime, interval: CostInterval
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_start_time = start_time.isoformat()
    params["start_time"] = json_start_time

    json_end_time = end_time.isoformat()
    params["end_time"] = json_end_time

    json_interval = interval.value
    params["interval"] = json_interval

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/integrations/costs/summary",
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Union[HTTPValidationError, IntegrationCostsResponse]:
    if response.status_code == 200:
        response_200 = IntegrationCostsResponse.from_dict(response.json())

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


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[Union[HTTPValidationError, IntegrationCostsResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, start_time: datetime.datetime, end_time: datetime.datetime, interval: CostInterval
) -> Response[Union[HTTPValidationError, IntegrationCostsResponse]]:
    """Get Integration Costs

    Args:
        start_time (datetime.datetime): Start of time range (UTC)
        end_time (datetime.datetime): End of time range (UTC)
        interval (CostInterval):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, IntegrationCostsResponse]]
    """

    kwargs = _get_kwargs(start_time=start_time, end_time=end_time, interval=interval)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, start_time: datetime.datetime, end_time: datetime.datetime, interval: CostInterval
) -> Optional[Union[HTTPValidationError, IntegrationCostsResponse]]:
    """Get Integration Costs

    Args:
        start_time (datetime.datetime): Start of time range (UTC)
        end_time (datetime.datetime): End of time range (UTC)
        interval (CostInterval):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, IntegrationCostsResponse]
    """

    return sync_detailed(client=client, start_time=start_time, end_time=end_time, interval=interval).parsed


async def asyncio_detailed(
    *, client: ApiClient, start_time: datetime.datetime, end_time: datetime.datetime, interval: CostInterval
) -> Response[Union[HTTPValidationError, IntegrationCostsResponse]]:
    """Get Integration Costs

    Args:
        start_time (datetime.datetime): Start of time range (UTC)
        end_time (datetime.datetime): End of time range (UTC)
        interval (CostInterval):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, IntegrationCostsResponse]]
    """

    kwargs = _get_kwargs(start_time=start_time, end_time=end_time, interval=interval)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, start_time: datetime.datetime, end_time: datetime.datetime, interval: CostInterval
) -> Optional[Union[HTTPValidationError, IntegrationCostsResponse]]:
    """Get Integration Costs

    Args:
        start_time (datetime.datetime): Start of time range (UTC)
        end_time (datetime.datetime): End of time range (UTC)
        interval (CostInterval):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, IntegrationCostsResponse]
    """

    return (await asyncio_detailed(client=client, start_time=start_time, end_time=end_time, interval=interval)).parsed
