from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.job_db import JobDB
from ...types import UNSET, Response, Unset


def _get_kwargs(project_id: str, run_id: str, *, status: Union[None, Unset, str] = UNSET) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_status: Union[None, Unset, str]
    if isinstance(status, Unset):
        json_status = UNSET
    else:
        json_status = status
    params["status"] = json_status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "get", "url": f"/projects/{project_id}/runs/{run_id}/jobs", "params": params}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["JobDB"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = JobDB.from_dict(response_200_item_data)

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
) -> Response[Union[HTTPValidationError, list["JobDB"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, run_id: str, *, client: AuthenticatedClient, status: Union[None, Unset, str] = UNSET
) -> Response[Union[HTTPValidationError, list["JobDB"]]]:
    """Get Jobs For Project Run

     Get all jobs by for a project and run.

    Returns them in order of creation from newest to oldest.

    Args:
        project_id (str):
        run_id (str):
        status (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['JobDB']]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, status=status)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, run_id: str, *, client: AuthenticatedClient, status: Union[None, Unset, str] = UNSET
) -> Optional[Union[HTTPValidationError, list["JobDB"]]]:
    """Get Jobs For Project Run

     Get all jobs by for a project and run.

    Returns them in order of creation from newest to oldest.

    Args:
        project_id (str):
        run_id (str):
        status (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['JobDB']]
    """

    return sync_detailed(project_id=project_id, run_id=run_id, client=client, status=status).parsed


async def asyncio_detailed(
    project_id: str, run_id: str, *, client: AuthenticatedClient, status: Union[None, Unset, str] = UNSET
) -> Response[Union[HTTPValidationError, list["JobDB"]]]:
    """Get Jobs For Project Run

     Get all jobs by for a project and run.

    Returns them in order of creation from newest to oldest.

    Args:
        project_id (str):
        run_id (str):
        status (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['JobDB']]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, status=status)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, run_id: str, *, client: AuthenticatedClient, status: Union[None, Unset, str] = UNSET
) -> Optional[Union[HTTPValidationError, list["JobDB"]]]:
    """Get Jobs For Project Run

     Get all jobs by for a project and run.

    Returns them in order of creation from newest to oldest.

    Args:
        project_id (str):
        run_id (str):
        status (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['JobDB']]
    """

    return (await asyncio_detailed(project_id=project_id, run_id=run_id, client=client, status=status)).parsed
