from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_user_latest_runs_db import GetUserLatestRunsDB
from ...models.http_validation_error import HTTPValidationError
from ...models.project_type import ProjectType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_id: str,
    *,
    project_type: Union[Unset, ProjectType] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_project_type: Union[Unset, str] = UNSET
    if not isinstance(project_type, Unset):
        json_project_type = project_type.value

    params["project_type"] = json_project_type

    params["starting_token"] = starting_token

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "get", "url": f"/users/{user_id}/runs/latest", "params": params}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetUserLatestRunsDB, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GetUserLatestRunsDB.from_dict(response.json())

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
) -> Response[Union[GetUserLatestRunsDB, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    *,
    client: AuthenticatedClient,
    project_type: Union[Unset, ProjectType] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[GetUserLatestRunsDB, HTTPValidationError]]:
    """Get Latest User Run

     Gets the most recent run for a User, ordered by last updated.

    Args:
        user_id (str):
        project_type (Union[Unset, ProjectType]):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetUserLatestRunsDB, HTTPValidationError]]
    """

    kwargs = _get_kwargs(user_id=user_id, project_type=project_type, starting_token=starting_token, limit=limit)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: AuthenticatedClient,
    project_type: Union[Unset, ProjectType] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[GetUserLatestRunsDB, HTTPValidationError]]:
    """Get Latest User Run

     Gets the most recent run for a User, ordered by last updated.

    Args:
        user_id (str):
        project_type (Union[Unset, ProjectType]):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetUserLatestRunsDB, HTTPValidationError]
    """

    return sync_detailed(
        user_id=user_id, client=client, project_type=project_type, starting_token=starting_token, limit=limit
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: AuthenticatedClient,
    project_type: Union[Unset, ProjectType] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[GetUserLatestRunsDB, HTTPValidationError]]:
    """Get Latest User Run

     Gets the most recent run for a User, ordered by last updated.

    Args:
        user_id (str):
        project_type (Union[Unset, ProjectType]):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetUserLatestRunsDB, HTTPValidationError]]
    """

    kwargs = _get_kwargs(user_id=user_id, project_type=project_type, starting_token=starting_token, limit=limit)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: AuthenticatedClient,
    project_type: Union[Unset, ProjectType] = UNSET,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[GetUserLatestRunsDB, HTTPValidationError]]:
    """Get Latest User Run

     Gets the most recent run for a User, ordered by last updated.

    Args:
        user_id (str):
        project_type (Union[Unset, ProjectType]):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetUserLatestRunsDB, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            user_id=user_id, client=client, project_type=project_type, starting_token=starting_token, limit=limit
        )
    ).parsed
