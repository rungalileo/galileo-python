from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.base_prompt_template_response import BasePromptTemplateResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(template_id: str, version: int) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "put", "url": f"/templates/{template_id}/versions/{version}"}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = BasePromptTemplateResponse.from_dict(response.json())

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
) -> Response[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    template_id: str, version: int, *, client: AuthenticatedClient
) -> Response[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """Set Selected Global Template Version

     Set a global prompt template version as the selected version.

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
    BasePromptTemplateResponse
        Details about the prompt template.

    Args:
        template_id (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BasePromptTemplateResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(template_id=template_id, version=version)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    template_id: str, version: int, *, client: AuthenticatedClient
) -> Optional[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """Set Selected Global Template Version

     Set a global prompt template version as the selected version.

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
    BasePromptTemplateResponse
        Details about the prompt template.

    Args:
        template_id (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BasePromptTemplateResponse, HTTPValidationError]
    """

    return sync_detailed(template_id=template_id, version=version, client=client).parsed


async def asyncio_detailed(
    template_id: str, version: int, *, client: AuthenticatedClient
) -> Response[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """Set Selected Global Template Version

     Set a global prompt template version as the selected version.

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
    BasePromptTemplateResponse
        Details about the prompt template.

    Args:
        template_id (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BasePromptTemplateResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(template_id=template_id, version=version)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    template_id: str, version: int, *, client: AuthenticatedClient
) -> Optional[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """Set Selected Global Template Version

     Set a global prompt template version as the selected version.

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
    BasePromptTemplateResponse
        Details about the prompt template.

    Args:
        template_id (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BasePromptTemplateResponse, HTTPValidationError]
    """

    return (await asyncio_detailed(template_id=template_id, version=version, client=client)).parsed
