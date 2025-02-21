from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.alert_status_response import AlertStatusResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(project_id: str, monitor_alert_config_id: str) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "delete", "url": f"/projects/{project_id}/alerts/{monitor_alert_config_id}"}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AlertStatusResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = AlertStatusResponse.from_dict(response.json())

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
) -> Response[Union[AlertStatusResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: str, monitor_alert_config_id: str, *, client: AuthenticatedClient
) -> Response[Union[AlertStatusResponse, HTTPValidationError]]:
    """Delete Alert

     Get all rows from monitor_records.

    Returns them in order of creation from newest to oldest.

    Args:
        project_id (str):
        monitor_alert_config_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AlertStatusResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, monitor_alert_config_id=monitor_alert_config_id)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    project_id: str, monitor_alert_config_id: str, *, client: AuthenticatedClient
) -> Optional[Union[AlertStatusResponse, HTTPValidationError]]:
    """Delete Alert

     Get all rows from monitor_records.

    Returns them in order of creation from newest to oldest.

    Args:
        project_id (str):
        monitor_alert_config_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AlertStatusResponse, HTTPValidationError]
    """

    return sync_detailed(project_id=project_id, monitor_alert_config_id=monitor_alert_config_id, client=client).parsed


async def asyncio_detailed(
    project_id: str, monitor_alert_config_id: str, *, client: AuthenticatedClient
) -> Response[Union[AlertStatusResponse, HTTPValidationError]]:
    """Delete Alert

     Get all rows from monitor_records.

    Returns them in order of creation from newest to oldest.

    Args:
        project_id (str):
        monitor_alert_config_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AlertStatusResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(project_id=project_id, monitor_alert_config_id=monitor_alert_config_id)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project_id: str, monitor_alert_config_id: str, *, client: AuthenticatedClient
) -> Optional[Union[AlertStatusResponse, HTTPValidationError]]:
    """Delete Alert

     Get all rows from monitor_records.

    Returns them in order of creation from newest to oldest.

    Args:
        project_id (str):
        monitor_alert_config_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AlertStatusResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(project_id=project_id, monitor_alert_config_id=monitor_alert_config_id, client=client)
    ).parsed
