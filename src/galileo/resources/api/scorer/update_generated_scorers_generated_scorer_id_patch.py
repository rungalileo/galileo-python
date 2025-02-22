from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.generated_scorer_response import GeneratedScorerResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.update_generated_scorer_request import UpdateGeneratedScorerRequest
from ...types import Response


def _get_kwargs(generated_scorer_id: str, *, body: UpdateGeneratedScorerRequest) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": "patch", "url": f"/generated-scorers/{generated_scorer_id}"}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GeneratedScorerResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GeneratedScorerResponse.from_dict(response.json())

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
) -> Response[Union[GeneratedScorerResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    generated_scorer_id: str, *, client: AuthenticatedClient, body: UpdateGeneratedScorerRequest
) -> Response[Union[GeneratedScorerResponse, HTTPValidationError]]:
    """Update

    Args:
        generated_scorer_id (str):
        body (UpdateGeneratedScorerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GeneratedScorerResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(generated_scorer_id=generated_scorer_id, body=body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    generated_scorer_id: str, *, client: AuthenticatedClient, body: UpdateGeneratedScorerRequest
) -> Optional[Union[GeneratedScorerResponse, HTTPValidationError]]:
    """Update

    Args:
        generated_scorer_id (str):
        body (UpdateGeneratedScorerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GeneratedScorerResponse, HTTPValidationError]
    """

    return sync_detailed(generated_scorer_id=generated_scorer_id, client=client, body=body).parsed


async def asyncio_detailed(
    generated_scorer_id: str, *, client: AuthenticatedClient, body: UpdateGeneratedScorerRequest
) -> Response[Union[GeneratedScorerResponse, HTTPValidationError]]:
    """Update

    Args:
        generated_scorer_id (str):
        body (UpdateGeneratedScorerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GeneratedScorerResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(generated_scorer_id=generated_scorer_id, body=body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    generated_scorer_id: str, *, client: AuthenticatedClient, body: UpdateGeneratedScorerRequest
) -> Optional[Union[GeneratedScorerResponse, HTTPValidationError]]:
    """Update

    Args:
        generated_scorer_id (str):
        body (UpdateGeneratedScorerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GeneratedScorerResponse, HTTPValidationError]
    """

    return (await asyncio_detailed(generated_scorer_id=generated_scorer_id, client=client, body=body)).parsed
