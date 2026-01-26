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
from ...models.get_integration_status_integrations_name_status_get_response_get_integration_status_integrations_name_status_get import (
    GetIntegrationStatusIntegrationsNameStatusGetResponseGetIntegrationStatusIntegrationsNameStatusGet,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.integration_name import IntegrationName
from ...types import Response


def _get_kwargs(name: IntegrationName) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": f"/integrations/{name}/status",
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Union[
    GetIntegrationStatusIntegrationsNameStatusGetResponseGetIntegrationStatusIntegrationsNameStatusGet,
    HTTPValidationError,
]:
    if response.status_code == 200:
        return GetIntegrationStatusIntegrationsNameStatusGetResponseGetIntegrationStatusIntegrationsNameStatusGet.from_dict(
            response.json()
        )

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
) -> Response[
    Union[
        GetIntegrationStatusIntegrationsNameStatusGetResponseGetIntegrationStatusIntegrationsNameStatusGet,
        HTTPValidationError,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: IntegrationName, *, client: ApiClient
) -> Response[
    Union[
        GetIntegrationStatusIntegrationsNameStatusGetResponseGetIntegrationStatusIntegrationsNameStatusGet,
        HTTPValidationError,
    ]
]:
    """Get Integration Status.

     Checks if the integration status is active or not.

    Args:
        name (IntegrationName):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[GetIntegrationStatusIntegrationsNameStatusGetResponseGetIntegrationStatusIntegrationsNameStatusGet, HTTPValidationError]]
    """
    kwargs = _get_kwargs(name=name)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    name: IntegrationName, *, client: ApiClient
) -> Optional[
    Union[
        GetIntegrationStatusIntegrationsNameStatusGetResponseGetIntegrationStatusIntegrationsNameStatusGet,
        HTTPValidationError,
    ]
]:
    """Get Integration Status.

     Checks if the integration status is active or not.

    Args:
        name (IntegrationName):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[GetIntegrationStatusIntegrationsNameStatusGetResponseGetIntegrationStatusIntegrationsNameStatusGet, HTTPValidationError]
    """
    return sync_detailed(name=name, client=client).parsed


async def asyncio_detailed(
    name: IntegrationName, *, client: ApiClient
) -> Response[
    Union[
        GetIntegrationStatusIntegrationsNameStatusGetResponseGetIntegrationStatusIntegrationsNameStatusGet,
        HTTPValidationError,
    ]
]:
    """Get Integration Status.

     Checks if the integration status is active or not.

    Args:
        name (IntegrationName):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[GetIntegrationStatusIntegrationsNameStatusGetResponseGetIntegrationStatusIntegrationsNameStatusGet, HTTPValidationError]]
    """
    kwargs = _get_kwargs(name=name)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: IntegrationName, *, client: ApiClient
) -> Optional[
    Union[
        GetIntegrationStatusIntegrationsNameStatusGetResponseGetIntegrationStatusIntegrationsNameStatusGet,
        HTTPValidationError,
    ]
]:
    """Get Integration Status.

     Checks if the integration status is active or not.

    Args:
        name (IntegrationName):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[GetIntegrationStatusIntegrationsNameStatusGetResponseGetIntegrationStatusIntegrationsNameStatusGet, HTTPValidationError]
    """
    return (await asyncio_detailed(name=name, client=client)).parsed
