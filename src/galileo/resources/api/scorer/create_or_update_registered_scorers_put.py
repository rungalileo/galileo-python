from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_create_or_update_registered_scorers_put import BodyCreateOrUpdateRegisteredScorersPut
from ...models.create_update_registered_scorer_response import CreateUpdateRegisteredScorerResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(*, body: BodyCreateOrUpdateRegisteredScorersPut, name: str) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["name"] = name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "put", "url": "/registered-scorers", "params": params}

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateUpdateRegisteredScorerResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = CreateUpdateRegisteredScorerResponse.from_dict(response.json())

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
) -> Response[Union[CreateUpdateRegisteredScorerResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: AuthenticatedClient, body: BodyCreateOrUpdateRegisteredScorersPut, name: str
) -> Response[Union[CreateUpdateRegisteredScorerResponse, HTTPValidationError]]:
    """Create Or Update

    Args:
        name (str):
        body (BodyCreateOrUpdateRegisteredScorersPut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateUpdateRegisteredScorerResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(body=body, name=name)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: AuthenticatedClient, body: BodyCreateOrUpdateRegisteredScorersPut, name: str
) -> Optional[Union[CreateUpdateRegisteredScorerResponse, HTTPValidationError]]:
    """Create Or Update

    Args:
        name (str):
        body (BodyCreateOrUpdateRegisteredScorersPut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateUpdateRegisteredScorerResponse, HTTPValidationError]
    """

    return sync_detailed(client=client, body=body, name=name).parsed


async def asyncio_detailed(
    *, client: AuthenticatedClient, body: BodyCreateOrUpdateRegisteredScorersPut, name: str
) -> Response[Union[CreateUpdateRegisteredScorerResponse, HTTPValidationError]]:
    """Create Or Update

    Args:
        name (str):
        body (BodyCreateOrUpdateRegisteredScorersPut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateUpdateRegisteredScorerResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(body=body, name=name)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: AuthenticatedClient, body: BodyCreateOrUpdateRegisteredScorersPut, name: str
) -> Optional[Union[CreateUpdateRegisteredScorerResponse, HTTPValidationError]]:
    """Create Or Update

    Args:
        name (str):
        body (BodyCreateOrUpdateRegisteredScorersPut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateUpdateRegisteredScorerResponse, HTTPValidationError]
    """

    return (await asyncio_detailed(client=client, body=body, name=name)).parsed
