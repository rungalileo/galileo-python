from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.llm_integration import LLMIntegration
from ...types import Response


def _get_kwargs(llm_integration: LLMIntegration) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": f"/llm_integrations/{llm_integration}/models"}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list[str]]]:
    if response.status_code == 200:
        response_200 = cast(list[str], response.json())

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
) -> Response[Union[HTTPValidationError, list[str]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    llm_integration: LLMIntegration, *, client: AuthenticatedClient
) -> Response[Union[HTTPValidationError, list[str]]]:
    """Get Available Models

     Get the list of supported models for the LLM integration.

    Args:
        llm_integration (LLMIntegration):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list[str]]]
    """

    kwargs = _get_kwargs(llm_integration=llm_integration)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    llm_integration: LLMIntegration, *, client: AuthenticatedClient
) -> Optional[Union[HTTPValidationError, list[str]]]:
    """Get Available Models

     Get the list of supported models for the LLM integration.

    Args:
        llm_integration (LLMIntegration):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list[str]]
    """

    return sync_detailed(llm_integration=llm_integration, client=client).parsed


async def asyncio_detailed(
    llm_integration: LLMIntegration, *, client: AuthenticatedClient
) -> Response[Union[HTTPValidationError, list[str]]]:
    """Get Available Models

     Get the list of supported models for the LLM integration.

    Args:
        llm_integration (LLMIntegration):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list[str]]]
    """

    kwargs = _get_kwargs(llm_integration=llm_integration)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    llm_integration: LLMIntegration, *, client: AuthenticatedClient
) -> Optional[Union[HTTPValidationError, list[str]]]:
    """Get Available Models

     Get the list of supported models for the LLM integration.

    Args:
        llm_integration (LLMIntegration):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list[str]]
    """

    return (await asyncio_detailed(llm_integration=llm_integration, client=client)).parsed
