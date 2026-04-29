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
from ...models.base_prompt_template_response import BasePromptTemplateResponse
from ...models.create_prompt_template_with_version_request_body import CreatePromptTemplateWithVersionRequestBody
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(project_id: str, *, body: CreatePromptTemplateWithVersionRequestBody) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": f"/projects/{project_id}/templates",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Union[BasePromptTemplateResponse, HTTPValidationError]:
    if response.status_code == 200:
        return BasePromptTemplateResponse.from_dict(response.json())

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
) -> Response[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, *, client: ApiClient, body: CreatePromptTemplateWithVersionRequestBody
) -> Response[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """Create Prompt Template With Version.

     For a given project, create a prompt template.

    We first create a prompt template version, and then create a prompt template that
    points to that version as the selected version.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    create_request : CreatePromptTemplateWithVersionRequestBody, optional
        Request body, by default Body( ...,
            examples=
            [BasePromptTemplateVersion.test_data() | BasePromptTemplate.test_data()],
        )
    db_read : Session, optional
        Session object to execute DB reads, by default Depends(get_db_read)

    Returns
    -------
    CreatePromptTemplateResponse
        Details about the created prompt template.

    Args:
        project_id (str):
        body (CreatePromptTemplateWithVersionRequestBody): Body to create a new prompt template
            with version.

            This is only used for parsing the body from the request.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[BasePromptTemplateResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, *, client: ApiClient, body: CreatePromptTemplateWithVersionRequestBody
) -> Optional[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """Create Prompt Template With Version.

     For a given project, create a prompt template.

    We first create a prompt template version, and then create a prompt template that
    points to that version as the selected version.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    create_request : CreatePromptTemplateWithVersionRequestBody, optional
        Request body, by default Body( ...,
            examples=
            [BasePromptTemplateVersion.test_data() | BasePromptTemplate.test_data()],
        )
    db_read : Session, optional
        Session object to execute DB reads, by default Depends(get_db_read)

    Returns
    -------
    CreatePromptTemplateResponse
        Details about the created prompt template.

    Args:
        project_id (str):
        body (CreatePromptTemplateWithVersionRequestBody): Body to create a new prompt template
            with version.

            This is only used for parsing the body from the request.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[BasePromptTemplateResponse, HTTPValidationError]
    """
    return sync_detailed(project_id=project_id, client=client, body=body).parsed


async def asyncio_detailed(
    project_id: str, *, client: ApiClient, body: CreatePromptTemplateWithVersionRequestBody
) -> Response[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """Create Prompt Template With Version.

     For a given project, create a prompt template.

    We first create a prompt template version, and then create a prompt template that
    points to that version as the selected version.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    create_request : CreatePromptTemplateWithVersionRequestBody, optional
        Request body, by default Body( ...,
            examples=
            [BasePromptTemplateVersion.test_data() | BasePromptTemplate.test_data()],
        )
    db_read : Session, optional
        Session object to execute DB reads, by default Depends(get_db_read)

    Returns
    -------
    CreatePromptTemplateResponse
        Details about the created prompt template.

    Args:
        project_id (str):
        body (CreatePromptTemplateWithVersionRequestBody): Body to create a new prompt template
            with version.

            This is only used for parsing the body from the request.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[BasePromptTemplateResponse, HTTPValidationError]]
    """
    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, *, client: ApiClient, body: CreatePromptTemplateWithVersionRequestBody
) -> Optional[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """Create Prompt Template With Version.

     For a given project, create a prompt template.

    We first create a prompt template version, and then create a prompt template that
    points to that version as the selected version.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    create_request : CreatePromptTemplateWithVersionRequestBody, optional
        Request body, by default Body( ...,
            examples=
            [BasePromptTemplateVersion.test_data() | BasePromptTemplate.test_data()],
        )
    db_read : Session, optional
        Session object to execute DB reads, by default Depends(get_db_read)

    Returns
    -------
    CreatePromptTemplateResponse
        Details about the created prompt template.

    Args:
        project_id (str):
        body (CreatePromptTemplateWithVersionRequestBody): Body to create a new prompt template
            with version.

            This is only used for parsing the body from the request.

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[BasePromptTemplateResponse, HTTPValidationError]
    """
    return (await asyncio_detailed(project_id=project_id, client=client, body=body)).parsed
