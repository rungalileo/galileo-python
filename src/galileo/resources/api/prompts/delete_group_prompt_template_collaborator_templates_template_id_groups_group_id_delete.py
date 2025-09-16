from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient

from ... import errors
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(template_id: str, group_id: str) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.DELETE,
        "return_raw_response": True,
        "path": f"/templates/{template_id}/groups/{group_id}",
    }

    headers["X-Galileo-SDK"] = f"galileo-python/{get_package_version()}"

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: ApiClient, response: httpx.Response) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(template_id: str, group_id: str, *, client: ApiClient) -> Response[Union[Any, HTTPValidationError]]:
    """Delete Group Prompt Template Collaborator

     Remove a group's access to a prompt template.

    Args:
        template_id (str):
        group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(template_id=template_id, group_id=group_id)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(template_id: str, group_id: str, *, client: ApiClient) -> Optional[Union[Any, HTTPValidationError]]:
    """Delete Group Prompt Template Collaborator

     Remove a group's access to a prompt template.

    Args:
        template_id (str):
        group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(template_id=template_id, group_id=group_id, client=client).parsed


async def asyncio_detailed(
    template_id: str, group_id: str, *, client: ApiClient
) -> Response[Union[Any, HTTPValidationError]]:
    """Delete Group Prompt Template Collaborator

     Remove a group's access to a prompt template.

    Args:
        template_id (str):
        group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(template_id=template_id, group_id=group_id)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(template_id: str, group_id: str, *, client: ApiClient) -> Optional[Union[Any, HTTPValidationError]]:
    """Delete Group Prompt Template Collaborator

     Remove a group's access to a prompt template.

    Args:
        template_id (str):
        group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (await asyncio_detailed(template_id=template_id, group_id=group_id, client=client)).parsed
