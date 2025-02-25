from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.base_prompt_template_version_response import BasePromptTemplateVersionResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(project_id: str, template_id: str, version: int) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/projects/{project_id}/templates/{template_id}/versions/{version}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = BasePromptTemplateVersionResponse.from_dict(response.json())

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
) -> Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, template_id: str, version: int, *, client: AuthenticatedClient
) -> Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Get Template Version

     Get a specific version of a prompt template.

    Parameters
    ----------
    template_id : UUID4
        Template ID.
    version : int
        Version number to fetch.
    current_user : User, optional
        User who is authorized, by default Depends(authentication_service.current_user).
    db_read : Session, optional
        Database session, by default Depends(get_db_read)

    Returns
    -------
    BasePromptTemplateVersionResponse
        Prompt template version response.

    Args:
        project_id (str):
        template_id (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, template_id=template_id, version=version)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, template_id: str, version: int, *, client: AuthenticatedClient
) -> Optional[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Get Template Version

     Get a specific version of a prompt template.

    Parameters
    ----------
    template_id : UUID4
        Template ID.
    version : int
        Version number to fetch.
    current_user : User, optional
        User who is authorized, by default Depends(authentication_service.current_user).
    db_read : Session, optional
        Database session, by default Depends(get_db_read)

    Returns
    -------
    BasePromptTemplateVersionResponse
        Prompt template version response.

    Args:
        project_id (str):
        template_id (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BasePromptTemplateVersionResponse, HTTPValidationError]
    """

    return sync_detailed(project_id=project_id, template_id=template_id, version=version, client=client).parsed


async def asyncio_detailed(
    project_id: str, template_id: str, version: int, *, client: AuthenticatedClient
) -> Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Get Template Version

     Get a specific version of a prompt template.

    Parameters
    ----------
    template_id : UUID4
        Template ID.
    version : int
        Version number to fetch.
    current_user : User, optional
        User who is authorized, by default Depends(authentication_service.current_user).
    db_read : Session, optional
        Database session, by default Depends(get_db_read)

    Returns
    -------
    BasePromptTemplateVersionResponse
        Prompt template version response.

    Args:
        project_id (str):
        template_id (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, template_id=template_id, version=version)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, template_id: str, version: int, *, client: AuthenticatedClient
) -> Optional[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Get Template Version

     Get a specific version of a prompt template.

    Parameters
    ----------
    template_id : UUID4
        Template ID.
    version : int
        Version number to fetch.
    current_user : User, optional
        User who is authorized, by default Depends(authentication_service.current_user).
    db_read : Session, optional
        Database session, by default Depends(get_db_read)

    Returns
    -------
    BasePromptTemplateVersionResponse
        Prompt template version response.

    Args:
        project_id (str):
        template_id (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BasePromptTemplateVersionResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(project_id=project_id, template_id=template_id, version=version, client=client)
    ).parsed
