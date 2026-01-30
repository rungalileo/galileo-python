from http import HTTPStatus
from typing import Any, Optional, Union

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
from ...models.base_prompt_template_version_response import BasePromptTemplateVersionResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(template_id: str, version: int) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": f"/templates/{template_id}/versions/{version}",
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Union[BasePromptTemplateVersionResponse, HTTPValidationError]:
    if response.status_code == 200:
        return BasePromptTemplateVersionResponse.from_dict(response.json())

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


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    template_id: str, version: int, *, client: ApiClient
) -> Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Get Global Template Version.

     Get a global prompt template version given a template ID and version number.

    Parameters
    ----------
    template_id : UUID4
        Prompt template id.
    version : int
        Version number.
    ctx : Context
        Request context including authentication information

    Returns
    -------
    BasePromptTemplateVersionResponse
        Details about the prompt template version.

    Args:
        template_id (str):
        version (int):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(template_id=template_id, version=version)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    template_id: str, version: int, *, client: ApiClient
) -> Optional[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Get Global Template Version.

     Get a global prompt template version given a template ID and version number.

    Parameters
    ----------
    template_id : UUID4
        Prompt template id.
    version : int
        Version number.
    ctx : Context
        Request context including authentication information

    Returns
    -------
    BasePromptTemplateVersionResponse
        Details about the prompt template version.

    Args:
        template_id (str):
        version (int):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[BasePromptTemplateVersionResponse, HTTPValidationError]
    """
    return sync_detailed(template_id=template_id, version=version, client=client).parsed


async def asyncio_detailed(
    template_id: str, version: int, *, client: ApiClient
) -> Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Get Global Template Version.

     Get a global prompt template version given a template ID and version number.

    Parameters
    ----------
    template_id : UUID4
        Prompt template id.
    version : int
        Version number.
    ctx : Context
        Request context including authentication information

    Returns
    -------
    BasePromptTemplateVersionResponse
        Details about the prompt template version.

    Args:
        template_id (str):
        version (int):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(template_id=template_id, version=version)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    template_id: str, version: int, *, client: ApiClient
) -> Optional[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Get Global Template Version.

     Get a global prompt template version given a template ID and version number.

    Parameters
    ----------
    template_id : UUID4
        Prompt template id.
    version : int
        Version number.
    ctx : Context
        Request context including authentication information

    Returns
    -------
    BasePromptTemplateVersionResponse
        Details about the prompt template version.

    Args:
        template_id (str):
        version (int):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[BasePromptTemplateVersionResponse, HTTPValidationError]
    """
    return (await asyncio_detailed(template_id=template_id, version=version, client=client)).parsed
