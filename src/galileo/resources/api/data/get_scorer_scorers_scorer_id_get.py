from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.scorer_response import ScorerResponse
from ...types import Response


def _get_kwargs(scorer_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": f"/scorers/{scorer_id}"}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ScorerResponse]]:
    if response.status_code == 200:
        response_200 = ScorerResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ScorerResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    scorer_id: str, *, client: AuthenticatedClient
) -> Response[Union[HTTPValidationError, ScorerResponse]]:
    """Get Scorer

    Args:
        scorer_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ScorerResponse]]
    """

    kwargs = _get_kwargs(scorer_id=scorer_id)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(scorer_id: str, *, client: AuthenticatedClient) -> Optional[Union[HTTPValidationError, ScorerResponse]]:
    """Get Scorer

    Args:
        scorer_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ScorerResponse]
    """

    return sync_detailed(scorer_id=scorer_id, client=client).parsed


async def asyncio_detailed(
    scorer_id: str, *, client: AuthenticatedClient
) -> Response[Union[HTTPValidationError, ScorerResponse]]:
    """Get Scorer

    Args:
        scorer_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ScorerResponse]]
    """

    kwargs = _get_kwargs(scorer_id=scorer_id)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    scorer_id: str, *, client: AuthenticatedClient
) -> Optional[Union[HTTPValidationError, ScorerResponse]]:
    """Get Scorer

    Args:
        scorer_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ScorerResponse]
    """

    return (await asyncio_detailed(scorer_id=scorer_id, client=client)).parsed
