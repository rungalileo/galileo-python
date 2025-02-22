from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.base_prompt_template_version_response import BasePromptTemplateVersionResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(project_id: str, *, template_name: str, version: Union[None, Unset, int] = UNSET) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["template_name"] = template_name

    json_version: Union[None, Unset, int]
    if isinstance(version, Unset):
        json_version = UNSET
    else:
        json_version = version
    params["version"] = json_version

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {"method": "get", "url": f"/projects/{project_id}/templates/versions", "params": params}

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
    project_id: str, *, client: AuthenticatedClient, template_name: str, version: Union[None, Unset, int] = UNSET
) -> Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Get Template Version By Name

     Get a prompt template from a project.

    Parameters
    ----------
    project_id : UUID4
        Prokect ID.
    template_name : str
        Prompt template name.
    version : Optional[int]
        Version number to fetch. defaults to selected version.
    db_read : Session, optional
        Session object to execute DB reads, by default Depends(get_db_read).


    Returns
    -------
    GetTemplateResponse
        Prompt template response.

    Args:
        project_id (str):
        template_name (str):
        version (Union[None, Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, template_name=template_name, version=version)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, *, client: AuthenticatedClient, template_name: str, version: Union[None, Unset, int] = UNSET
) -> Optional[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Get Template Version By Name

     Get a prompt template from a project.

    Parameters
    ----------
    project_id : UUID4
        Prokect ID.
    template_name : str
        Prompt template name.
    version : Optional[int]
        Version number to fetch. defaults to selected version.
    db_read : Session, optional
        Session object to execute DB reads, by default Depends(get_db_read).


    Returns
    -------
    GetTemplateResponse
        Prompt template response.

    Args:
        project_id (str):
        template_name (str):
        version (Union[None, Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BasePromptTemplateVersionResponse, HTTPValidationError]
    """

    return sync_detailed(project_id=project_id, client=client, template_name=template_name, version=version).parsed


async def asyncio_detailed(
    project_id: str, *, client: AuthenticatedClient, template_name: str, version: Union[None, Unset, int] = UNSET
) -> Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Get Template Version By Name

     Get a prompt template from a project.

    Parameters
    ----------
    project_id : UUID4
        Prokect ID.
    template_name : str
        Prompt template name.
    version : Optional[int]
        Version number to fetch. defaults to selected version.
    db_read : Session, optional
        Session object to execute DB reads, by default Depends(get_db_read).


    Returns
    -------
    GetTemplateResponse
        Prompt template response.

    Args:
        project_id (str):
        template_name (str):
        version (Union[None, Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, template_name=template_name, version=version)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, *, client: AuthenticatedClient, template_name: str, version: Union[None, Unset, int] = UNSET
) -> Optional[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Get Template Version By Name

     Get a prompt template from a project.

    Parameters
    ----------
    project_id : UUID4
        Prokect ID.
    template_name : str
        Prompt template name.
    version : Optional[int]
        Version number to fetch. defaults to selected version.
    db_read : Session, optional
        Session object to execute DB reads, by default Depends(get_db_read).


    Returns
    -------
    GetTemplateResponse
        Prompt template response.

    Args:
        project_id (str):
        template_name (str):
        version (Union[None, Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BasePromptTemplateVersionResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(project_id=project_id, client=client, template_name=template_name, version=version)
    ).parsed
