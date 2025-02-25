from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.run_metric_db import RunMetricDB
from ...types import UNSET, Response, Unset


def _get_kwargs(project_id: str, run_id: str, *, key: Union[None, Unset, str] = UNSET) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_key: Union[None, Unset, str]
    if isinstance(key, Unset):
        json_key = UNSET
    else:
        json_key = key
    params["key"] = json_key

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/runs/{run_id}/metrics",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["RunMetricDB"]]]:
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
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, list["RunMetricDB"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, run_id: str, *, client: AuthenticatedClient, key: Union[None, Unset, str] = UNSET
) -> Response[Union[HTTPValidationError, list["RunMetricDB"]]]:
    """Get Metrics For Run

     List metrics for a run.

    Optionally provide a key to narrow the search

    Args:
        project_id (str):
        run_id (str):
        key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['RunMetricDB']]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, key=key)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, run_id: str, *, client: AuthenticatedClient, key: Union[None, Unset, str] = UNSET
) -> Optional[Union[HTTPValidationError, list["RunMetricDB"]]]:
    """Get Metrics For Run

     List metrics for a run.

    Optionally provide a key to narrow the search

    Args:
        project_id (str):
        run_id (str):
        key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['RunMetricDB']]
    """

    return sync_detailed(project_id=project_id, run_id=run_id, client=client, key=key).parsed


async def asyncio_detailed(
    project_id: str, run_id: str, *, client: AuthenticatedClient, key: Union[None, Unset, str] = UNSET
) -> Response[Union[HTTPValidationError, list["RunMetricDB"]]]:
    """Get Metrics For Run

     List metrics for a run.

    Optionally provide a key to narrow the search

    Args:
        project_id (str):
        run_id (str):
        key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['RunMetricDB']]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, key=key)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, run_id: str, *, client: AuthenticatedClient, key: Union[None, Unset, str] = UNSET
) -> Optional[Union[HTTPValidationError, list["RunMetricDB"]]]:
    """Get Metrics For Run

     List metrics for a run.

    Optionally provide a key to narrow the search

    Args:
        project_id (str):
        run_id (str):
        key (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['RunMetricDB']]
    """

    return (await asyncio_detailed(project_id=project_id, run_id=run_id, client=client, key=key)).parsed
