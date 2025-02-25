from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.run_db import RunDB
from ...types import UNSET, Response, Unset


def _get_kwargs(project_id: str, *, run_name: Union[None, Unset, str] = UNSET) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_run_name: Union[None, Unset, str]
    if isinstance(run_name, Unset):
        json_run_name = UNSET
    else:
        json_run_name = run_name
    params["run_name"] = json_run_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "get", "url": f"/projects/{project_id}/runs", "params": params}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["RunDB"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RunDB.from_dict(response_200_item_data)

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
) -> Response[Union[HTTPValidationError, list["RunDB"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, *, client: AuthenticatedClient, run_name: Union[None, Unset, str] = UNSET
) -> Response[Union[HTTPValidationError, list["RunDB"]]]:
    """Get Project Runs

     Gets all runs for a project.

    If a run_name is provided, gets the run with that name, or []

    Args:
        project_id (str):
        run_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['RunDB']]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_name=run_name)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, *, client: AuthenticatedClient, run_name: Union[None, Unset, str] = UNSET
) -> Optional[Union[HTTPValidationError, list["RunDB"]]]:
    """Get Project Runs

     Gets all runs for a project.

    If a run_name is provided, gets the run with that name, or []

    Args:
        project_id (str):
        run_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['RunDB']]
    """

    return sync_detailed(project_id=project_id, client=client, run_name=run_name).parsed


async def asyncio_detailed(
    project_id: str, *, client: AuthenticatedClient, run_name: Union[None, Unset, str] = UNSET
) -> Response[Union[HTTPValidationError, list["RunDB"]]]:
    """Get Project Runs

     Gets all runs for a project.

    If a run_name is provided, gets the run with that name, or []

    Args:
        project_id (str):
        run_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['RunDB']]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_name=run_name)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, *, client: AuthenticatedClient, run_name: Union[None, Unset, str] = UNSET
) -> Optional[Union[HTTPValidationError, list["RunDB"]]]:
    """Get Project Runs

     Gets all runs for a project.

    If a run_name is provided, gets the run with that name, or []

    Args:
        project_id (str):
        run_name (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['RunDB']]
    """

    return (await asyncio_detailed(project_id=project_id, client=client, run_name=run_name)).parsed
