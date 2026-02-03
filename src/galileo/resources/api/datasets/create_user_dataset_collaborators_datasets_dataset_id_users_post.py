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
from ...models.http_validation_error import HTTPValidationError
from ...models.user_collaborator import UserCollaborator
from ...models.user_collaborator_create import UserCollaboratorCreate
from ...types import Response


def _get_kwargs(dataset_id: str, *, body: list["UserCollaboratorCreate"]) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.POST,
        "return_raw_response": True,
        "path": f"/datasets/{dataset_id}/users",
    }

    _kwargs["json"] = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _kwargs["json"].append(body_item)

    headers["Content-Type"] = "application/json"

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Union[HTTPValidationError, list["UserCollaborator"]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UserCollaborator.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

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
) -> Response[Union[HTTPValidationError, list["UserCollaborator"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_id: str, *, client: ApiClient, body: list["UserCollaboratorCreate"]
) -> Response[Union[HTTPValidationError, list["UserCollaborator"]]]:
    """Create User Dataset Collaborators.

    Args:
        dataset_id (str):
        body (list['UserCollaboratorCreate']):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, list['UserCollaborator']]]
    """
    kwargs = _get_kwargs(dataset_id=dataset_id, body=body)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str, *, client: ApiClient, body: list["UserCollaboratorCreate"]
) -> Optional[Union[HTTPValidationError, list["UserCollaborator"]]]:
    """Create User Dataset Collaborators.

    Args:
        dataset_id (str):
        body (list['UserCollaboratorCreate']):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, list['UserCollaborator']]
    """
    return sync_detailed(dataset_id=dataset_id, client=client, body=body).parsed


async def asyncio_detailed(
    dataset_id: str, *, client: ApiClient, body: list["UserCollaboratorCreate"]
) -> Response[Union[HTTPValidationError, list["UserCollaborator"]]]:
    """Create User Dataset Collaborators.

    Args:
        dataset_id (str):
        body (list['UserCollaboratorCreate']):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, list['UserCollaborator']]]
    """
    kwargs = _get_kwargs(dataset_id=dataset_id, body=body)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str, *, client: ApiClient, body: list["UserCollaboratorCreate"]
) -> Optional[Union[HTTPValidationError, list["UserCollaborator"]]]:
    """Create User Dataset Collaborators.

    Args:
        dataset_id (str):
        body (list['UserCollaboratorCreate']):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, list['UserCollaborator']]
    """
    return (await asyncio_detailed(dataset_id=dataset_id, client=client, body=body)).parsed
