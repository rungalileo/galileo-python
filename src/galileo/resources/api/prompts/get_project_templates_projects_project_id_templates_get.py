from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.base_prompt_template_response import BasePromptTemplateResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(project_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": f"/projects/{project_id}/templates",
    }

    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["BasePromptTemplateResponse"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = BasePromptTemplateResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: ApiClient, response: httpx.Response
) -> Response[Union[HTTPValidationError, list["BasePromptTemplateResponse"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, *, client: ApiClient
) -> Response[Union[HTTPValidationError, list["BasePromptTemplateResponse"]]]:
    """Get Project Templates

     Get all prompt templates for a project.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    ctx : Context, optional
        User context with database session, by default Depends(get_user_context)

    Returns
    -------
    List[GetTemplateResponse]
        List of prompt template responses.

    Args:
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['BasePromptTemplateResponse']]]
    """

    kwargs = _get_kwargs(project_id=project_id)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, *, client: ApiClient
) -> Optional[Union[HTTPValidationError, list["BasePromptTemplateResponse"]]]:
    """Get Project Templates

     Get all prompt templates for a project.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    ctx : Context, optional
        User context with database session, by default Depends(get_user_context)

    Returns
    -------
    List[GetTemplateResponse]
        List of prompt template responses.

    Args:
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['BasePromptTemplateResponse']]
    """

    return sync_detailed(project_id=project_id, client=client).parsed


async def asyncio_detailed(
    project_id: str, *, client: ApiClient
) -> Response[Union[HTTPValidationError, list["BasePromptTemplateResponse"]]]:
    """Get Project Templates

     Get all prompt templates for a project.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    ctx : Context, optional
        User context with database session, by default Depends(get_user_context)

    Returns
    -------
    List[GetTemplateResponse]
        List of prompt template responses.

    Args:
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['BasePromptTemplateResponse']]]
    """

    kwargs = _get_kwargs(project_id=project_id)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, *, client: ApiClient
) -> Optional[Union[HTTPValidationError, list["BasePromptTemplateResponse"]]]:
    """Get Project Templates

     Get all prompt templates for a project.

    Parameters
    ----------
    project_id : UUID4
        Project ID.
    ctx : Context, optional
        User context with database session, by default Depends(get_user_context)

    Returns
    -------
    List[GetTemplateResponse]
        List of prompt template responses.

    Args:
        project_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['BasePromptTemplateResponse']]
    """

    return (await asyncio_detailed(project_id=project_id, client=client)).parsed
