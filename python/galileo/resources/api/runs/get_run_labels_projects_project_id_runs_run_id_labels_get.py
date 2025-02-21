from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.label_response import LabelResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(project_id: str, run_id: str, *, task: Union[None, Unset, str] = UNSET) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_task: Union[None, Unset, str]
    if isinstance(task, Unset):
        json_task = UNSET
    else:
        json_task = task
    params["task"] = json_task

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "get", "url": f"/projects/{project_id}/runs/{run_id}/labels", "params": params}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, LabelResponse]]:
    if response.status_code == 200:
        response_200 = LabelResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, LabelResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, run_id: str, *, client: AuthenticatedClient, task: Union[None, Unset, str] = UNSET
) -> Response[Union[HTTPValidationError, LabelResponse]]:
    """Get Run Labels

     Gets labels for a given project_id/run_id.

    Split is not required because labels are the same across splits. If this is a multi-label run, a
    task is required,
    otherwise it is not expected

    Args:
        project_id (str):
        run_id (str):
        task (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LabelResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, task=task)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, run_id: str, *, client: AuthenticatedClient, task: Union[None, Unset, str] = UNSET
) -> Optional[Union[HTTPValidationError, LabelResponse]]:
    """Get Run Labels

     Gets labels for a given project_id/run_id.

    Split is not required because labels are the same across splits. If this is a multi-label run, a
    task is required,
    otherwise it is not expected

    Args:
        project_id (str):
        run_id (str):
        task (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, LabelResponse]
    """

    return sync_detailed(project_id=project_id, run_id=run_id, client=client, task=task).parsed


async def asyncio_detailed(
    project_id: str, run_id: str, *, client: AuthenticatedClient, task: Union[None, Unset, str] = UNSET
) -> Response[Union[HTTPValidationError, LabelResponse]]:
    """Get Run Labels

     Gets labels for a given project_id/run_id.

    Split is not required because labels are the same across splits. If this is a multi-label run, a
    task is required,
    otherwise it is not expected

    Args:
        project_id (str):
        run_id (str):
        task (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, LabelResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, run_id=run_id, task=task)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, run_id: str, *, client: AuthenticatedClient, task: Union[None, Unset, str] = UNSET
) -> Optional[Union[HTTPValidationError, LabelResponse]]:
    """Get Run Labels

     Gets labels for a given project_id/run_id.

    Split is not required because labels are the same across splits. If this is a multi-label run, a
    task is required,
    otherwise it is not expected

    Args:
        project_id (str):
        run_id (str):
        task (Union[None, Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, LabelResponse]
    """

    return (await asyncio_detailed(project_id=project_id, run_id=run_id, client=client, task=task)).parsed
