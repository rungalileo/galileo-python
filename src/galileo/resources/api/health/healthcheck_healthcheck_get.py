from http import HTTPStatus
from typing import Any, Optional

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.healthcheck_response import HealthcheckResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": RequestMethod.GET, "return_raw_response": True, "path": "/healthcheck"}

    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Optional[HealthcheckResponse]:
    if response.status_code == 200:
        return HealthcheckResponse.from_dict(response.json())

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[HealthcheckResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(*, client: ApiClient) -> Response[HealthcheckResponse]:
    """Healthcheck

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HealthcheckResponse]
    """

    kwargs = _get_kwargs()

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(*, client: ApiClient) -> Optional[HealthcheckResponse]:
    """Healthcheck

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HealthcheckResponse
    """

    return sync_detailed(client=client).parsed


async def asyncio_detailed(*, client: ApiClient) -> Response[HealthcheckResponse]:
    """Healthcheck

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HealthcheckResponse]
    """

    kwargs = _get_kwargs()

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(*, client: ApiClient) -> Optional[HealthcheckResponse]:
    """Healthcheck

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HealthcheckResponse
    """

    return (await asyncio_detailed(client=client)).parsed
