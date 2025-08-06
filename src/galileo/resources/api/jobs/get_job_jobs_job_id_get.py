from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.http_validation_error import HTTPValidationError
from ...models.job_db import JobDB
from ...types import Response


def _get_kwargs(job_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": RequestMethod.GET, "return_raw_response": True, "path": f"/jobs/{job_id}"}

    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Optional[Union[HTTPValidationError, JobDB]]:
    if response.status_code == 200:
        response_200 = JobDB.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[Union[HTTPValidationError, JobDB]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(job_id: str, *, client: ApiClient) -> Response[Union[HTTPValidationError, JobDB]]:
    """Get Job

     Get a job by id.

    Args:
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, JobDB]]
    """

    kwargs = _get_kwargs(job_id=job_id)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(job_id: str, *, client: ApiClient) -> Optional[Union[HTTPValidationError, JobDB]]:
    """Get Job

     Get a job by id.

    Args:
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, JobDB]
    """

    return sync_detailed(job_id=job_id, client=client).parsed


async def asyncio_detailed(job_id: str, *, client: ApiClient) -> Response[Union[HTTPValidationError, JobDB]]:
    """Get Job

     Get a job by id.

    Args:
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, JobDB]]
    """

    kwargs = _get_kwargs(job_id=job_id)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(job_id: str, *, client: ApiClient) -> Optional[Union[HTTPValidationError, JobDB]]:
    """Get Job

     Get a job by id.

    Args:
        job_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, JobDB]
    """

    return (await asyncio_detailed(job_id=job_id, client=client)).parsed
