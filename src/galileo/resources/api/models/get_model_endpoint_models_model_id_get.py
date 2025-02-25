from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.training_model_response import TrainingModelResponse
from ...types import Response


def _get_kwargs(model_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": f"/models/{model_id}"}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, TrainingModelResponse]]:
    if response.status_code == 200:
        response_200 = TrainingModelResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, TrainingModelResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    model_id: str, *, client: AuthenticatedClient
) -> Response[Union[HTTPValidationError, TrainingModelResponse]]:
    """Get Model Endpoint

     Gets a model from the database and returns the presigned url to download it :param project_id:
    project id :param
    run_id: run id :param model_id: model id :param db_read: database session :param current_user:
    current user.

    Args:
        model_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TrainingModelResponse]]
    """

    kwargs = _get_kwargs(model_id=model_id)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(model_id: str, *, client: AuthenticatedClient) -> Optional[Union[HTTPValidationError, TrainingModelResponse]]:
    """Get Model Endpoint

     Gets a model from the database and returns the presigned url to download it :param project_id:
    project id :param
    run_id: run id :param model_id: model id :param db_read: database session :param current_user:
    current user.

    Args:
        model_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TrainingModelResponse]
    """

    return sync_detailed(model_id=model_id, client=client).parsed


async def asyncio_detailed(
    model_id: str, *, client: AuthenticatedClient
) -> Response[Union[HTTPValidationError, TrainingModelResponse]]:
    """Get Model Endpoint

     Gets a model from the database and returns the presigned url to download it :param project_id:
    project id :param
    run_id: run id :param model_id: model id :param db_read: database session :param current_user:
    current user.

    Args:
        model_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TrainingModelResponse]]
    """

    kwargs = _get_kwargs(model_id=model_id)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    model_id: str, *, client: AuthenticatedClient
) -> Optional[Union[HTTPValidationError, TrainingModelResponse]]:
    """Get Model Endpoint

     Gets a model from the database and returns the presigned url to download it :param project_id:
    project id :param
    run_id: run id :param model_id: model id :param db_read: database session :param current_user:
    current user.

    Args:
        model_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TrainingModelResponse]
    """

    return (await asyncio_detailed(model_id=model_id, client=client)).parsed
