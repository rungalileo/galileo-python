import datetime
from http import HTTPStatus
from typing import Any, Optional

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
from ...models.audit_action import AuditAction
from ...models.audit_log_list_response import AuditLogListResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    start: datetime.datetime,
    end: datetime.datetime,
    action: AuditAction | None | Unset = UNSET,
    user_id: None | str | Unset = UNSET,
    path_contains: None | str | Unset = UNSET,
    cursor_id: int | None | Unset = UNSET,
    limit: int | Unset = 100,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_start = start.isoformat()
    params["start"] = json_start

    json_end = end.isoformat()
    params["end"] = json_end

    json_action: None | str | Unset
    if isinstance(action, Unset):
        json_action = UNSET
    elif isinstance(action, AuditAction):
        json_action = action.value
    else:
        json_action = action
    params["action"] = json_action

    json_user_id: None | str | Unset
    if isinstance(user_id, Unset):
        json_user_id = UNSET
    else:
        json_user_id = user_id
    params["user_id"] = json_user_id

    json_path_contains: None | str | Unset
    if isinstance(path_contains, Unset):
        json_path_contains = UNSET
    else:
        json_path_contains = path_contains
    params["path_contains"] = json_path_contains

    json_cursor_id: int | None | Unset
    if isinstance(cursor_id, Unset):
        json_cursor_id = UNSET
    else:
        json_cursor_id = cursor_id
    params["cursor_id"] = json_cursor_id

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/v2/audit-logs",
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(*, client: ApiClient, response: httpx.Response) -> AuditLogListResponse | HTTPValidationError:
    if response.status_code == 200:
        response_200 = AuditLogListResponse.from_dict(response.json())

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
) -> Response[AuditLogListResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: ApiClient,
    start: datetime.datetime,
    end: datetime.datetime,
    action: AuditAction | None | Unset = UNSET,
    user_id: None | str | Unset = UNSET,
    path_contains: None | str | Unset = UNSET,
    cursor_id: int | None | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[AuditLogListResponse | HTTPValidationError]:
    """List Audit Logs

     Query audit logs with filtering and cursor-based pagination.

    System-admin-only endpoint for retrieving audit logs.
    Use `cursor_id` from the previous response's `next_cursor_id` to get the next page.

    Args:
        start (datetime.datetime):
        end (datetime.datetime):
        action (AuditAction | None | Unset):
        user_id (None | str | Unset):
        path_contains (None | str | Unset):
        cursor_id (int | None | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuditLogListResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        start=start,
        end=end,
        action=action,
        user_id=user_id,
        path_contains=path_contains,
        cursor_id=cursor_id,
        limit=limit,
    )

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *,
    client: ApiClient,
    start: datetime.datetime,
    end: datetime.datetime,
    action: AuditAction | None | Unset = UNSET,
    user_id: None | str | Unset = UNSET,
    path_contains: None | str | Unset = UNSET,
    cursor_id: int | None | Unset = UNSET,
    limit: int | Unset = 100,
) -> Optional[AuditLogListResponse | HTTPValidationError]:
    """List Audit Logs

     Query audit logs with filtering and cursor-based pagination.

    System-admin-only endpoint for retrieving audit logs.
    Use `cursor_id` from the previous response's `next_cursor_id` to get the next page.

    Args:
        start (datetime.datetime):
        end (datetime.datetime):
        action (AuditAction | None | Unset):
        user_id (None | str | Unset):
        path_contains (None | str | Unset):
        cursor_id (int | None | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuditLogListResponse | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        start=start,
        end=end,
        action=action,
        user_id=user_id,
        path_contains=path_contains,
        cursor_id=cursor_id,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: ApiClient,
    start: datetime.datetime,
    end: datetime.datetime,
    action: AuditAction | None | Unset = UNSET,
    user_id: None | str | Unset = UNSET,
    path_contains: None | str | Unset = UNSET,
    cursor_id: int | None | Unset = UNSET,
    limit: int | Unset = 100,
) -> Response[AuditLogListResponse | HTTPValidationError]:
    """List Audit Logs

     Query audit logs with filtering and cursor-based pagination.

    System-admin-only endpoint for retrieving audit logs.
    Use `cursor_id` from the previous response's `next_cursor_id` to get the next page.

    Args:
        start (datetime.datetime):
        end (datetime.datetime):
        action (AuditAction | None | Unset):
        user_id (None | str | Unset):
        path_contains (None | str | Unset):
        cursor_id (int | None | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuditLogListResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        start=start,
        end=end,
        action=action,
        user_id=user_id,
        path_contains=path_contains,
        cursor_id=cursor_id,
        limit=limit,
    )

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: ApiClient,
    start: datetime.datetime,
    end: datetime.datetime,
    action: AuditAction | None | Unset = UNSET,
    user_id: None | str | Unset = UNSET,
    path_contains: None | str | Unset = UNSET,
    cursor_id: int | None | Unset = UNSET,
    limit: int | Unset = 100,
) -> Optional[AuditLogListResponse | HTTPValidationError]:
    """List Audit Logs

     Query audit logs with filtering and cursor-based pagination.

    System-admin-only endpoint for retrieving audit logs.
    Use `cursor_id` from the previous response's `next_cursor_id` to get the next page.

    Args:
        start (datetime.datetime):
        end (datetime.datetime):
        action (AuditAction | None | Unset):
        user_id (None | str | Unset):
        path_contains (None | str | Unset):
        cursor_id (int | None | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuditLogListResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            start=start,
            end=end,
            action=action,
            user_id=user_id,
            path_contains=path_contains,
            cursor_id=cursor_id,
            limit=limit,
        )
    ).parsed
