from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.get_projects_paginated_response_v2 import GetProjectsPaginatedResponseV2
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    scorer_version_id: str, *, scorer_id: str, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["scorer_id"] = scorer_id

    params["starting_token"] = starting_token

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": f"/scorers/versions/{scorer_version_id}/projects",
        "params": params,
    }

    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[Union[GetProjectsPaginatedResponseV2, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GetProjectsPaginatedResponseV2.from_dict(response.json())

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
) -> Response[Union[GetProjectsPaginatedResponseV2, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    scorer_version_id: str,
    *,
    client: ApiClient,
    scorer_id: str,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[GetProjectsPaginatedResponseV2, HTTPValidationError]]:
    """List Projects For Scorer Version Route

     List all projects associated with a specific scorer version.

    Args:
        scorer_version_id (str):
        scorer_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetProjectsPaginatedResponseV2, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        scorer_version_id=scorer_version_id, scorer_id=scorer_id, starting_token=starting_token, limit=limit
    )

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    scorer_version_id: str,
    *,
    client: ApiClient,
    scorer_id: str,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[GetProjectsPaginatedResponseV2, HTTPValidationError]]:
    """List Projects For Scorer Version Route

     List all projects associated with a specific scorer version.

    Args:
        scorer_version_id (str):
        scorer_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetProjectsPaginatedResponseV2, HTTPValidationError]
    """

    return sync_detailed(
        scorer_version_id=scorer_version_id,
        client=client,
        scorer_id=scorer_id,
        starting_token=starting_token,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    scorer_version_id: str,
    *,
    client: ApiClient,
    scorer_id: str,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[GetProjectsPaginatedResponseV2, HTTPValidationError]]:
    """List Projects For Scorer Version Route

     List all projects associated with a specific scorer version.

    Args:
        scorer_version_id (str):
        scorer_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetProjectsPaginatedResponseV2, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        scorer_version_id=scorer_version_id, scorer_id=scorer_id, starting_token=starting_token, limit=limit
    )

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    scorer_version_id: str,
    *,
    client: ApiClient,
    scorer_id: str,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[GetProjectsPaginatedResponseV2, HTTPValidationError]]:
    """List Projects For Scorer Version Route

     List all projects associated with a specific scorer version.

    Args:
        scorer_version_id (str):
        scorer_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetProjectsPaginatedResponseV2, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            scorer_version_id=scorer_version_id,
            client=client,
            scorer_id=scorer_id,
            starting_token=starting_token,
            limit=limit,
        )
    ).parsed
