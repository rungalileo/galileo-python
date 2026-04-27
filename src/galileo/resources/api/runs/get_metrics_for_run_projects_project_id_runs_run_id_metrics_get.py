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
from ...models.http_validation_error import HTTPValidationError
from ...models.run_metric_db import RunMetricDB
from ...types import UNSET, Response, Unset


def _get_kwargs(project_id: str, run_id: str, *, key: None | str | Unset = UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_key: None | str | Unset
    if isinstance(key, Unset):
        json_key = UNSET
    else:
        json_key = key
    params["key"] = json_key

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/projects/{project_id}/runs/{run_id}/metrics".format(project_id=project_id, run_id=run_id),
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | list[RunMetricDB]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RunMetricDB.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[HTTPValidationError | list[RunMetricDB]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, run_id: str, *, client: ApiClient, key: None | str | Unset = UNSET
) -> Response[HTTPValidationError | list[RunMetricDB]]:
    """Get Metrics For Run

     List metrics for a run.

    Optionally provide a key to narrow the search

    Args:
        project_id (str):
        run_id (str):
        key (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[RunMetricDB]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, key=key)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, run_id: str, *, client: ApiClient, key: None | str | Unset = UNSET
) -> Optional[HTTPValidationError | list[RunMetricDB]]:
    """Get Metrics For Run

     List metrics for a run.

    Optionally provide a key to narrow the search

    Args:
        project_id (str):
        run_id (str):
        key (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[RunMetricDB]
    """

    return sync_detailed(project_id=project_id, run_id=run_id, client=client, key=key).parsed


async def asyncio_detailed(
    project_id: str, run_id: str, *, client: ApiClient, key: None | str | Unset = UNSET
) -> Response[HTTPValidationError | list[RunMetricDB]]:
    """Get Metrics For Run

     List metrics for a run.

    Optionally provide a key to narrow the search

    Args:
        project_id (str):
        run_id (str):
        key (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[RunMetricDB]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, key=key)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, run_id: str, *, client: ApiClient, key: None | str | Unset = UNSET
) -> Optional[HTTPValidationError | list[RunMetricDB]]:
    """Get Metrics For Run

     List metrics for a run.

    Optionally provide a key to narrow the search

    Args:
        project_id (str):
        run_id (str):
        key (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[RunMetricDB]
    """

    return (await asyncio_detailed(project_id=project_id, run_id=run_id, client=client, key=key)).parsed
