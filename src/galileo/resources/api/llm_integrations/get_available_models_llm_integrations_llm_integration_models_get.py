from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from galileo.exceptions import (
    AuthenticationError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from galileo.utils.headers_data import get_sdk_header
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.http_validation_error import HTTPValidationError
from ...models.llm_integration import LLMIntegration
from ...types import Response


def _get_kwargs(llm_integration: LLMIntegration) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": f"/llm_integrations/{llm_integration}/models",
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Union[HTTPValidationError, list[str]]:
    if response.status_code == 200:
        return cast(list[str], response.json())

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

    # Handle common HTTP errors with actionable messages
    if response.status_code == 400:
        raise BadRequestError(response.status_code, response.content)
    if response.status_code == 401:
        raise AuthenticationError(response.status_code, response.content)
    if response.status_code == 403:
        raise ForbiddenError(response.status_code, response.content)
    if response.status_code == 404:
        raise NotFoundError(response.status_code, response.content)
    if response.status_code == 409:
        raise ConflictError(response.status_code, response.content)
    if response.status_code == 429:
        raise RateLimitError(response.status_code, response.content)
    if response.status_code >= 500:
        raise ServerError(response.status_code, response.content)
    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[Union[HTTPValidationError, list[str]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    llm_integration: LLMIntegration, *, client: ApiClient
) -> Response[Union[HTTPValidationError, list[str]]]:
    """Get Available Models.

     Get the list of supported models for the LLM integration.

    Args:
        llm_integration (LLMIntegration):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, list[str]]]
    """
    kwargs = _get_kwargs(llm_integration=llm_integration)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(llm_integration: LLMIntegration, *, client: ApiClient) -> Optional[Union[HTTPValidationError, list[str]]]:
    """Get Available Models.

     Get the list of supported models for the LLM integration.

    Args:
        llm_integration (LLMIntegration):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, list[str]]
    """
    return sync_detailed(llm_integration=llm_integration, client=client).parsed


async def asyncio_detailed(
    llm_integration: LLMIntegration, *, client: ApiClient
) -> Response[Union[HTTPValidationError, list[str]]]:
    """Get Available Models.

     Get the list of supported models for the LLM integration.

    Args:
        llm_integration (LLMIntegration):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, list[str]]]
    """
    kwargs = _get_kwargs(llm_integration=llm_integration)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    llm_integration: LLMIntegration, *, client: ApiClient
) -> Optional[Union[HTTPValidationError, list[str]]]:
    """Get Available Models.

     Get the list of supported models for the LLM integration.

    Args:
        llm_integration (LLMIntegration):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, list[str]]
    """
    return (await asyncio_detailed(llm_integration=llm_integration, client=client)).parsed
