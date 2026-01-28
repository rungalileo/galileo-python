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
from ...models.base_prompt_template_version import BasePromptTemplateVersion
from ...models.base_prompt_template_version_response import BasePromptTemplateVersionResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(project_id: str, template_id: str, *, body: BasePromptTemplateVersion) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": f"/projects/{project_id}/templates/{template_id}/versions",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

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
    project_id: str, template_id: str, *, client: ApiClient, body: BasePromptTemplateVersion
) -> Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Create Prompt Template Version.

     Create a prompt template version for a given prompt template.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    template_id : UUID4
        Prompt template ID.
    body : dict, optional
        Body of the request, by default Body( ...,
            examples=[CreatePromptTemplateVersionRequest.test_data()],
        )
    db_read : Session, optional
        Database session, by default Depends(get_db_read)

    Returns
    -------
    BasePromptTemplateVersionResponse
        Response with details about the created prompt template version.

    Args:
        project_id (str):
        template_id (str):
        body (BasePromptTemplateVersion):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(project_id=project_id, template_id=template_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, template_id: str, *, client: ApiClient, body: BasePromptTemplateVersion
) -> Optional[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Create Prompt Template Version.

     Create a prompt template version for a given prompt template.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    template_id : UUID4
        Prompt template ID.
    body : dict, optional
        Body of the request, by default Body( ...,
            examples=[CreatePromptTemplateVersionRequest.test_data()],
        )
    db_read : Session, optional
        Database session, by default Depends(get_db_read)

    Returns
    -------
    BasePromptTemplateVersionResponse
        Response with details about the created prompt template version.

    Args:
        project_id (str):
        template_id (str):
        body (BasePromptTemplateVersion):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[BasePromptTemplateVersionResponse, HTTPValidationError]
    """
    return sync_detailed(project_id=project_id, template_id=template_id, client=client, body=body).parsed


async def asyncio_detailed(
    project_id: str, template_id: str, *, client: ApiClient, body: BasePromptTemplateVersion
) -> Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Create Prompt Template Version.

     Create a prompt template version for a given prompt template.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    template_id : UUID4
        Prompt template ID.
    body : dict, optional
        Body of the request, by default Body( ...,
            examples=[CreatePromptTemplateVersionRequest.test_data()],
        )
    db_read : Session, optional
        Database session, by default Depends(get_db_read)

    Returns
    -------
    BasePromptTemplateVersionResponse
        Response with details about the created prompt template version.

    Args:
        project_id (str):
        template_id (str):
        body (BasePromptTemplateVersion):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(project_id=project_id, template_id=template_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, template_id: str, *, client: ApiClient, body: BasePromptTemplateVersion
) -> Optional[Union[BasePromptTemplateVersionResponse, HTTPValidationError]]:
    """Create Prompt Template Version.

     Create a prompt template version for a given prompt template.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    template_id : UUID4
        Prompt template ID.
    body : dict, optional
        Body of the request, by default Body( ...,
            examples=[CreatePromptTemplateVersionRequest.test_data()],
        )
    db_read : Session, optional
        Database session, by default Depends(get_db_read)

    Returns
    -------
    BasePromptTemplateVersionResponse
        Response with details about the created prompt template version.

    Args:
        project_id (str):
        template_id (str):
        body (BasePromptTemplateVersion):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[BasePromptTemplateVersionResponse, HTTPValidationError]
    """
    return (await asyncio_detailed(project_id=project_id, template_id=template_id, client=client, body=body)).parsed
