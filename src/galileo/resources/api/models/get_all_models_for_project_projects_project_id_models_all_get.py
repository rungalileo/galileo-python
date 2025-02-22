from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.training_model_response import TrainingModelResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str, *, starting_token: Union[Unset, int] = 0, limit: Union[Unset, int] = 100
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["starting_token"] = starting_token

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "get", "url": f"/projects/{project_id}/models/all", "params": params}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["TrainingModelResponse"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = TrainingModelResponse.from_dict(response_200_item_data)

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
) -> Response[Union[HTTPValidationError, list["TrainingModelResponse"]]]:
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
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, list["TrainingModelResponse"]]]:
    """Get All Models For Project

     Gets all models for a run :param project_id: project id :param run_id: run id :param db_read:
    database
    session.

    Args:
        project_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['TrainingModelResponse']]]
    """

    kwargs = _get_kwargs(project_id=project_id, starting_token=starting_token, limit=limit)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: AuthenticatedClient,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, list["TrainingModelResponse"]]]:
    """Get All Models For Project

     Gets all models for a run :param project_id: project id :param run_id: run id :param db_read:
    database
    session.

    Args:
        project_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['TrainingModelResponse']]
    """

    return sync_detailed(project_id=project_id, client=client, starting_token=starting_token, limit=limit).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: AuthenticatedClient,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Response[Union[HTTPValidationError, list["TrainingModelResponse"]]]:
    """Get All Models For Project

     Gets all models for a run :param project_id: project id :param run_id: run id :param db_read:
    database
    session.

    Args:
        project_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['TrainingModelResponse']]]
    """

    kwargs = _get_kwargs(project_id=project_id, starting_token=starting_token, limit=limit)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: AuthenticatedClient,
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> Optional[Union[HTTPValidationError, list["TrainingModelResponse"]]]:
    """Get All Models For Project

     Gets all models for a run :param project_id: project id :param run_id: run id :param db_read:
    database
    session.

    Args:
        project_id (str):
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['TrainingModelResponse']]
    """

    return (
        await asyncio_detailed(project_id=project_id, client=client, starting_token=starting_token, limit=limit)
    ).parsed
