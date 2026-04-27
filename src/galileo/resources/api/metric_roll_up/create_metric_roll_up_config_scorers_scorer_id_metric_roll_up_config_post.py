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
from ...models.create_metric_roll_up_config_request import CreateMetricRollUpConfigRequest
from ...models.http_validation_error import HTTPValidationError
from ...models.metric_roll_up_config_response import MetricRollUpConfigResponse
from ...types import Response


def _get_kwargs(scorer_id: str, *, body: CreateMetricRollUpConfigRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": "/scorers/{scorer_id}/metric-roll-up-config".format(scorer_id=scorer_id),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | MetricRollUpConfigResponse:
    if response.status_code == 200:
        response_200 = MetricRollUpConfigResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | MetricRollUpConfigResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    scorer_id: str, *, client: ApiClient, body: CreateMetricRollUpConfigRequest
) -> Response[HTTPValidationError | MetricRollUpConfigResponse]:
    """Create Metric Roll Up Config

     Create or update a metric roll up configuration for a scorer.

    The metric name is derived from the scorer name.

    The scorer must have a compatible output type for the roll up methods:
    - Numeric roll up methods (average, sum, max, min) require numeric output types
      (boolean, percentage, number, discrete, count)
    - Categorical roll up methods (category_count) require categorical output types
      (categorical, freeform, multilabel)

    If a configuration already exists for this scorer, it will be updated.

    Args:
        scorer_id (str):
        body (CreateMetricRollUpConfigRequest): Request to create a metric roll up configuration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MetricRollUpConfigResponse]
    """

    kwargs = _get_kwargs(scorer_id=scorer_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    scorer_id: str, *, client: ApiClient, body: CreateMetricRollUpConfigRequest
) -> Optional[HTTPValidationError | MetricRollUpConfigResponse]:
    """Create Metric Roll Up Config

     Create or update a metric roll up configuration for a scorer.

    The metric name is derived from the scorer name.

    The scorer must have a compatible output type for the roll up methods:
    - Numeric roll up methods (average, sum, max, min) require numeric output types
      (boolean, percentage, number, discrete, count)
    - Categorical roll up methods (category_count) require categorical output types
      (categorical, freeform, multilabel)

    If a configuration already exists for this scorer, it will be updated.

    Args:
        scorer_id (str):
        body (CreateMetricRollUpConfigRequest): Request to create a metric roll up configuration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MetricRollUpConfigResponse
    """

    return sync_detailed(scorer_id=scorer_id, client=client, body=body).parsed


async def asyncio_detailed(
    scorer_id: str, *, client: ApiClient, body: CreateMetricRollUpConfigRequest
) -> Response[HTTPValidationError | MetricRollUpConfigResponse]:
    """Create Metric Roll Up Config

     Create or update a metric roll up configuration for a scorer.

    The metric name is derived from the scorer name.

    The scorer must have a compatible output type for the roll up methods:
    - Numeric roll up methods (average, sum, max, min) require numeric output types
      (boolean, percentage, number, discrete, count)
    - Categorical roll up methods (category_count) require categorical output types
      (categorical, freeform, multilabel)

    If a configuration already exists for this scorer, it will be updated.

    Args:
        scorer_id (str):
        body (CreateMetricRollUpConfigRequest): Request to create a metric roll up configuration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MetricRollUpConfigResponse]
    """

    kwargs = _get_kwargs(scorer_id=scorer_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    scorer_id: str, *, client: ApiClient, body: CreateMetricRollUpConfigRequest
) -> Optional[HTTPValidationError | MetricRollUpConfigResponse]:
    """Create Metric Roll Up Config

     Create or update a metric roll up configuration for a scorer.

    The metric name is derived from the scorer name.

    The scorer must have a compatible output type for the roll up methods:
    - Numeric roll up methods (average, sum, max, min) require numeric output types
      (boolean, percentage, number, discrete, count)
    - Categorical roll up methods (category_count) require categorical output types
      (categorical, freeform, multilabel)

    If a configuration already exists for this scorer, it will be updated.

    Args:
        scorer_id (str):
        body (CreateMetricRollUpConfigRequest): Request to create a metric roll up configuration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MetricRollUpConfigResponse
    """

    return (await asyncio_detailed(scorer_id=scorer_id, client=client, body=body)).parsed
