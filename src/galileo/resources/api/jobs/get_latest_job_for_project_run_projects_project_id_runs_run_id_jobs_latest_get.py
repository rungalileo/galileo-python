from http import HTTPStatus
from typing import Any, Optional, cast

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
from ...models.job_db import JobDB
from ...types import Response


def _get_kwargs(project_id: str, run_id: str) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/projects/{project_id}/runs/{run_id}/jobs/latest".format(project_id=project_id, run_id=run_id),
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> HTTPValidationError | JobDB | None:
    if response.status_code == 200:

        def _parse_response_200(data: object) -> JobDB | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = JobDB.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            return cast(JobDB | None, data)

        response_200 = _parse_response_200(response.json())

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


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[HTTPValidationError | JobDB | None]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(project_id: str, run_id: str, *, client: ApiClient) -> Response[HTTPValidationError | JobDB | None]:
    """Get Latest Job For Project Run

     Returns the most recently updated job for a run.

    Args:
        project_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | JobDB | None]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(project_id: str, run_id: str, *, client: ApiClient) -> Optional[HTTPValidationError | JobDB | None]:
    """Get Latest Job For Project Run

     Returns the most recently updated job for a run.

    Args:
        project_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | JobDB | None
    """

    return sync_detailed(project_id=project_id, run_id=run_id, client=client).parsed


async def asyncio_detailed(
    project_id: str, run_id: str, *, client: ApiClient
) -> Response[HTTPValidationError | JobDB | None]:
    """Get Latest Job For Project Run

     Returns the most recently updated job for a run.

    Args:
        project_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | JobDB | None]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(project_id: str, run_id: str, *, client: ApiClient) -> Optional[HTTPValidationError | JobDB | None]:
    """Get Latest Job For Project Run

     Returns the most recently updated job for a run.

    Args:
        project_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | JobDB | None
    """

    return (await asyncio_detailed(project_id=project_id, run_id=run_id, client=client)).parsed
