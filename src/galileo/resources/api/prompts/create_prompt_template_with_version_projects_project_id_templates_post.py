from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.base_prompt_template_response import BasePromptTemplateResponse
from ...models.create_prompt_template_with_version_request_body import CreatePromptTemplateWithVersionRequestBody
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(project_id: str, *, body: CreatePromptTemplateWithVersionRequestBody) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {"method": "post", "url": f"/projects/{project_id}/templates"}

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    project_id: str, *, client: AuthenticatedClient, body: CreatePromptTemplateWithVersionRequestBody
) -> Response[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """Create Prompt Template With Version

     For a given project, create a prompt template.

    We first create a prompt template version, and then create a prompt template that
    points to that version as the selected version.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    current_user : User, optional
        User who sent the request, by default Depends(authentication_service.current_user)
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

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BasePromptTemplateResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, *, client: AuthenticatedClient, body: CreatePromptTemplateWithVersionRequestBody
) -> Optional[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """Create Prompt Template With Version

     For a given project, create a prompt template.

    We first create a prompt template version, and then create a prompt template that
    points to that version as the selected version.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    current_user : User, optional
        User who sent the request, by default Depends(authentication_service.current_user)
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

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BasePromptTemplateResponse, HTTPValidationError]
    """

    return sync_detailed(project_id=project_id, client=client, body=body).parsed


async def asyncio_detailed(
    project_id: str, *, client: AuthenticatedClient, body: CreatePromptTemplateWithVersionRequestBody
) -> Response[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """Create Prompt Template With Version

     For a given project, create a prompt template.

    We first create a prompt template version, and then create a prompt template that
    points to that version as the selected version.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    current_user : User, optional
        User who sent the request, by default Depends(authentication_service.current_user)
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

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BasePromptTemplateResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, body=body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, *, client: AuthenticatedClient, body: CreatePromptTemplateWithVersionRequestBody
) -> Optional[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    """Create Prompt Template With Version

     For a given project, create a prompt template.

    We first create a prompt template version, and then create a prompt template that
    points to that version as the selected version.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    current_user : User, optional
        User who sent the request, by default Depends(authentication_service.current_user)
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

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BasePromptTemplateResponse, HTTPValidationError]
    """

    return (await asyncio_detailed(project_id=project_id, client=client, body=body)).parsed
