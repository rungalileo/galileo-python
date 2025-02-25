import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.filter_options_response import FilterOptionsResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    *,
    start_time: Union[None, Unset, datetime.datetime] = UNSET,
    end_time: Union[None, Unset, datetime.datetime] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_start_time: Union[None, Unset, str]
    if isinstance(start_time, Unset):
        json_start_time = UNSET
    elif isinstance(start_time, datetime.datetime):
        json_start_time = start_time.isoformat()
    else:
        json_start_time = start_time
    params["start_time"] = json_start_time

    json_end_time: Union[None, Unset, str]
    if isinstance(end_time, Unset):
        json_end_time = UNSET
    elif isinstance(end_time, datetime.datetime):
        json_end_time = end_time.isoformat()
    else:
        json_end_time = end_time
    params["end_time"] = json_end_time

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/observe/filter_options",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[FilterOptionsResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = FilterOptionsResponse.from_dict(response.json())

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
) -> Response[Union[FilterOptionsResponse, HTTPValidationError]]:
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
    start_time: Union[None, Unset, datetime.datetime] = UNSET,
    end_time: Union[None, Unset, datetime.datetime] = UNSET,
) -> Response[Union[FilterOptionsResponse, HTTPValidationError]]:
    """Get Filter Options

     Get filter options for the observe view.

    Args:
        project_id (str):
        start_time (Union[None, Unset, datetime.datetime]):
        end_time (Union[None, Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FilterOptionsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, start_time=start_time, end_time=end_time)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    start_time: Union[None, Unset, datetime.datetime] = UNSET,
    end_time: Union[None, Unset, datetime.datetime] = UNSET,
) -> Optional[Union[FilterOptionsResponse, HTTPValidationError]]:
    """Get Filter Options

     Get filter options for the observe view.

    Args:
        project_id (str):
        start_time (Union[None, Unset, datetime.datetime]):
        end_time (Union[None, Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FilterOptionsResponse, HTTPValidationError]
    """

    return sync_detailed(project_id=project_id, client=client, start_time=start_time, end_time=end_time).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    start_time: Union[None, Unset, datetime.datetime] = UNSET,
    end_time: Union[None, Unset, datetime.datetime] = UNSET,
) -> Response[Union[FilterOptionsResponse, HTTPValidationError]]:
    """Get Filter Options

     Get filter options for the observe view.

    Args:
        project_id (str):
        start_time (Union[None, Unset, datetime.datetime]):
        end_time (Union[None, Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FilterOptionsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, start_time=start_time, end_time=end_time)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    start_time: Union[None, Unset, datetime.datetime] = UNSET,
    end_time: Union[None, Unset, datetime.datetime] = UNSET,
) -> Optional[Union[FilterOptionsResponse, HTTPValidationError]]:
    """Get Filter Options

     Get filter options for the observe view.

    Args:
        project_id (str):
        start_time (Union[None, Unset, datetime.datetime]):
        end_time (Union[None, Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FilterOptionsResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(project_id=project_id, client=client, start_time=start_time, end_time=end_time)
    ).parsed
