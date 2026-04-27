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
from ...models.get_integration_status_v2_integrations_name_status_get_response_get_integration_status_v2_integrations_name_status_get import (
    GetIntegrationStatusV2IntegrationsNameStatusGetResponseGetIntegrationStatusV2IntegrationsNameStatusGet,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.integration_name import IntegrationName
from ...types import Response


def _get_kwargs(name: IntegrationName) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/v2/integrations/{name}/status".format(name=name),
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> (
    GetIntegrationStatusV2IntegrationsNameStatusGetResponseGetIntegrationStatusV2IntegrationsNameStatusGet
    | HTTPValidationError
):
    if response.status_code == 200:
        response_200 = GetIntegrationStatusV2IntegrationsNameStatusGetResponseGetIntegrationStatusV2IntegrationsNameStatusGet.from_dict(
            response.json()
        )

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
) -> Response[
    GetIntegrationStatusV2IntegrationsNameStatusGetResponseGetIntegrationStatusV2IntegrationsNameStatusGet
    | HTTPValidationError
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
    GetIntegrationStatusV2IntegrationsNameStatusGetResponseGetIntegrationStatusV2IntegrationsNameStatusGet
    | HTTPValidationError
]:
    """Get Integration Status

     Checks if the integration status is active or not.

    Args:
        name (IntegrationName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetIntegrationStatusV2IntegrationsNameStatusGetResponseGetIntegrationStatusV2IntegrationsNameStatusGet | HTTPValidationError]
    """

    kwargs = _get_kwargs(name=name)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    name: IntegrationName, *, client: ApiClient
) -> Optional[
    GetIntegrationStatusV2IntegrationsNameStatusGetResponseGetIntegrationStatusV2IntegrationsNameStatusGet
    | HTTPValidationError
]:
    """Get Integration Status

     Checks if the integration status is active or not.

    Args:
        name (IntegrationName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetIntegrationStatusV2IntegrationsNameStatusGetResponseGetIntegrationStatusV2IntegrationsNameStatusGet | HTTPValidationError
    """

    return sync_detailed(name=name, client=client).parsed


async def asyncio_detailed(
    name: IntegrationName, *, client: ApiClient
) -> Response[
    GetIntegrationStatusV2IntegrationsNameStatusGetResponseGetIntegrationStatusV2IntegrationsNameStatusGet
    | HTTPValidationError
]:
    """Get Integration Status

     Checks if the integration status is active or not.

    Args:
        name (IntegrationName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetIntegrationStatusV2IntegrationsNameStatusGetResponseGetIntegrationStatusV2IntegrationsNameStatusGet | HTTPValidationError]
    """

    kwargs = _get_kwargs(name=name)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: IntegrationName, *, client: ApiClient
) -> Optional[
    GetIntegrationStatusV2IntegrationsNameStatusGetResponseGetIntegrationStatusV2IntegrationsNameStatusGet
    | HTTPValidationError
]:
    """Get Integration Status

     Checks if the integration status is active or not.

    Args:
        name (IntegrationName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetIntegrationStatusV2IntegrationsNameStatusGetResponseGetIntegrationStatusV2IntegrationsNameStatusGet | HTTPValidationError
    """

    return (await asyncio_detailed(name=name, client=client)).parsed
