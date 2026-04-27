from http import HTTPStatus
from typing import Any, Optional
from uuid import UUID

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
from ...models.component_type import ComponentType
from ...models.component_view_response import ComponentViewResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.view_visibility import ViewVisibility
from ...types import UNSET, Response, Unset


def _get_kwargs(
    project_id: str,
    *,
    component: ComponentType,
    run_id: UUID | Unset = UNSET,
    visibility: None | Unset | ViewVisibility = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_component = component.value
    params["component"] = json_component

    json_run_id: str | Unset = UNSET
    if not isinstance(run_id, Unset):
        json_run_id = str(run_id)
    params["run_id"] = json_run_id

    json_visibility: None | str | Unset
    if isinstance(visibility, Unset):
        json_visibility = UNSET
    elif isinstance(visibility, ViewVisibility):
        json_visibility = visibility.value
    else:
        json_visibility = visibility
    params["visibility"] = json_visibility

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/projects/{project_id}/views".format(project_id=project_id),
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> HTTPValidationError | list[ComponentViewResponse]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ComponentViewResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

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
) -> Response[HTTPValidationError | list[ComponentViewResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str,
    *,
    client: ApiClient,
    component: ComponentType,
    run_id: UUID | Unset = UNSET,
    visibility: None | Unset | ViewVisibility = UNSET,
) -> Response[HTTPValidationError | list[ComponentViewResponse]]:
    """List Views

     List all views the user can see for a component.

    Returns:
    - User's user views
    - All project-visible views (if visibility filter allows)

    Note: If no project views exist for the scope, a default project-visible view
    is automatically created. This ensures every user sees at least one shared view.

    Args:
        project_id (str):
        component (ComponentType): Types of components that can have saved views.
        run_id (UUID | Unset): Required run ID
        visibility (None | Unset | ViewVisibility): Filter by visibility: 'user', 'project', or
            null for all

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ComponentViewResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, component=component, run_id=run_id, visibility=visibility)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str,
    *,
    client: ApiClient,
    component: ComponentType,
    run_id: UUID | Unset = UNSET,
    visibility: None | Unset | ViewVisibility = UNSET,
) -> Optional[HTTPValidationError | list[ComponentViewResponse]]:
    """List Views

     List all views the user can see for a component.

    Returns:
    - User's user views
    - All project-visible views (if visibility filter allows)

    Note: If no project views exist for the scope, a default project-visible view
    is automatically created. This ensures every user sees at least one shared view.

    Args:
        project_id (str):
        component (ComponentType): Types of components that can have saved views.
        run_id (UUID | Unset): Required run ID
        visibility (None | Unset | ViewVisibility): Filter by visibility: 'user', 'project', or
            null for all

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ComponentViewResponse]
    """

    return sync_detailed(
        project_id=project_id, client=client, component=component, run_id=run_id, visibility=visibility
    ).parsed


async def asyncio_detailed(
    project_id: str,
    *,
    client: ApiClient,
    component: ComponentType,
    run_id: UUID | Unset = UNSET,
    visibility: None | Unset | ViewVisibility = UNSET,
) -> Response[HTTPValidationError | list[ComponentViewResponse]]:
    """List Views

     List all views the user can see for a component.

    Returns:
    - User's user views
    - All project-visible views (if visibility filter allows)

    Note: If no project views exist for the scope, a default project-visible view
    is automatically created. This ensures every user sees at least one shared view.

    Args:
        project_id (str):
        component (ComponentType): Types of components that can have saved views.
        run_id (UUID | Unset): Required run ID
        visibility (None | Unset | ViewVisibility): Filter by visibility: 'user', 'project', or
            null for all

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ComponentViewResponse]]
    """

    kwargs = _get_kwargs(project_id=project_id, component=component, run_id=run_id, visibility=visibility)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str,
    *,
    client: ApiClient,
    component: ComponentType,
    run_id: UUID | Unset = UNSET,
    visibility: None | Unset | ViewVisibility = UNSET,
) -> Optional[HTTPValidationError | list[ComponentViewResponse]]:
    """List Views

     List all views the user can see for a component.

    Returns:
    - User's user views
    - All project-visible views (if visibility filter allows)

    Note: If no project views exist for the scope, a default project-visible view
    is automatically created. This ensures every user sees at least one shared view.

    Args:
        project_id (str):
        component (ComponentType): Types of components that can have saved views.
        run_id (UUID | Unset): Required run ID
        visibility (None | Unset | ViewVisibility): Filter by visibility: 'user', 'project', or
            null for all

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ComponentViewResponse]
    """

    return (
        await asyncio_detailed(
            project_id=project_id, client=client, component=component, run_id=run_id, visibility=visibility
        )
    ).parsed
