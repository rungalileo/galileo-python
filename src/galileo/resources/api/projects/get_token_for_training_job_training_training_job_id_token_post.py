from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_token_for_training_job_training_training_job_id_token_post_request_body import (
    GetTokenForTrainingJobTrainingTrainingJobIdTokenPostRequestBody,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.train_job_auth_token_response import TrainJobAuthTokenResponse
from ...types import Response


def _get_kwargs(
    training_job_id: str, *, body: GetTokenForTrainingJobTrainingTrainingJobIdTokenPostRequestBody
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": "post", "url": f"/training/{training_job_id}/token"}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, TrainJobAuthTokenResponse]]:
    if response.status_code == 200:
        response_200 = TrainJobAuthTokenResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, TrainJobAuthTokenResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    training_job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: GetTokenForTrainingJobTrainingTrainingJobIdTokenPostRequestBody,
) -> Response[Union[HTTPValidationError, TrainJobAuthTokenResponse]]:
    """Get Token For Training Job

     Get the status for a training job.

    Args:
        training_job_id (str):
        body (GetTokenForTrainingJobTrainingTrainingJobIdTokenPostRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TrainJobAuthTokenResponse]]
    """

    kwargs = _get_kwargs(training_job_id=training_job_id, body=body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    training_job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: GetTokenForTrainingJobTrainingTrainingJobIdTokenPostRequestBody,
) -> Optional[Union[HTTPValidationError, TrainJobAuthTokenResponse]]:
    """Get Token For Training Job

     Get the status for a training job.

    Args:
        training_job_id (str):
        body (GetTokenForTrainingJobTrainingTrainingJobIdTokenPostRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TrainJobAuthTokenResponse]
    """

    return sync_detailed(training_job_id=training_job_id, client=client, body=body).parsed


async def asyncio_detailed(
    training_job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: GetTokenForTrainingJobTrainingTrainingJobIdTokenPostRequestBody,
) -> Response[Union[HTTPValidationError, TrainJobAuthTokenResponse]]:
    """Get Token For Training Job

     Get the status for a training job.

    Args:
        training_job_id (str):
        body (GetTokenForTrainingJobTrainingTrainingJobIdTokenPostRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TrainJobAuthTokenResponse]]
    """

    kwargs = _get_kwargs(training_job_id=training_job_id, body=body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    training_job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: GetTokenForTrainingJobTrainingTrainingJobIdTokenPostRequestBody,
) -> Optional[Union[HTTPValidationError, TrainJobAuthTokenResponse]]:
    """Get Token For Training Job

     Get the status for a training job.

    Args:
        training_job_id (str):
        body (GetTokenForTrainingJobTrainingTrainingJobIdTokenPostRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TrainJobAuthTokenResponse]
    """

    return (await asyncio_detailed(training_job_id=training_job_id, client=client, body=body)).parsed
