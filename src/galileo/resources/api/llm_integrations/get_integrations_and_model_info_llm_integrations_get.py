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
from ...models.get_integrations_and_model_info_llm_integrations_get_response_get_integrations_and_model_info_llm_integrations_get import (
    GetIntegrationsAndModelInfoLlmIntegrationsGetResponseGetIntegrationsAndModelInfoLlmIntegrationsGet,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.multimodal_capability import MultimodalCapability
from ...types import UNSET, Response, Unset


def _get_kwargs(*, multimodal_capabilities: list[MultimodalCapability] | None | Unset = UNSET) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_multimodal_capabilities: list[str] | None | Unset
    if isinstance(multimodal_capabilities, Unset):
        json_multimodal_capabilities = UNSET
    elif isinstance(multimodal_capabilities, list):
        json_multimodal_capabilities = []
        for multimodal_capabilities_type_0_item_data in multimodal_capabilities:
            multimodal_capabilities_type_0_item = multimodal_capabilities_type_0_item_data.value
            json_multimodal_capabilities.append(multimodal_capabilities_type_0_item)

    else:
        json_multimodal_capabilities = multimodal_capabilities
    params["multimodal_capabilities"] = json_multimodal_capabilities

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/llm_integrations",
        "params": params,
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> (
    GetIntegrationsAndModelInfoLlmIntegrationsGetResponseGetIntegrationsAndModelInfoLlmIntegrationsGet
    | HTTPValidationError
):
    if response.status_code == 200:
        response_200 = GetIntegrationsAndModelInfoLlmIntegrationsGetResponseGetIntegrationsAndModelInfoLlmIntegrationsGet.from_dict(
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
    GetIntegrationsAndModelInfoLlmIntegrationsGetResponseGetIntegrationsAndModelInfoLlmIntegrationsGet
    | HTTPValidationError
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *, client: ApiClient, multimodal_capabilities: list[MultimodalCapability] | None | Unset = UNSET
) -> Response[
    GetIntegrationsAndModelInfoLlmIntegrationsGetResponseGetIntegrationsAndModelInfoLlmIntegrationsGet
    | HTTPValidationError
]:
    """Get Integrations And Model Info

     Get the list of supported scorer models for the user's llm integrations.

    Args:
        multimodal_capabilities (list[MultimodalCapability] | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetIntegrationsAndModelInfoLlmIntegrationsGetResponseGetIntegrationsAndModelInfoLlmIntegrationsGet | HTTPValidationError]
    """

    kwargs = _get_kwargs(multimodal_capabilities=multimodal_capabilities)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    *, client: ApiClient, multimodal_capabilities: list[MultimodalCapability] | None | Unset = UNSET
) -> Optional[
    GetIntegrationsAndModelInfoLlmIntegrationsGetResponseGetIntegrationsAndModelInfoLlmIntegrationsGet
    | HTTPValidationError
]:
    """Get Integrations And Model Info

     Get the list of supported scorer models for the user's llm integrations.

    Args:
        multimodal_capabilities (list[MultimodalCapability] | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetIntegrationsAndModelInfoLlmIntegrationsGetResponseGetIntegrationsAndModelInfoLlmIntegrationsGet | HTTPValidationError
    """

    return sync_detailed(client=client, multimodal_capabilities=multimodal_capabilities).parsed


async def asyncio_detailed(
    *, client: ApiClient, multimodal_capabilities: list[MultimodalCapability] | None | Unset = UNSET
) -> Response[
    GetIntegrationsAndModelInfoLlmIntegrationsGetResponseGetIntegrationsAndModelInfoLlmIntegrationsGet
    | HTTPValidationError
]:
    """Get Integrations And Model Info

     Get the list of supported scorer models for the user's llm integrations.

    Args:
        multimodal_capabilities (list[MultimodalCapability] | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetIntegrationsAndModelInfoLlmIntegrationsGetResponseGetIntegrationsAndModelInfoLlmIntegrationsGet | HTTPValidationError]
    """

    kwargs = _get_kwargs(multimodal_capabilities=multimodal_capabilities)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *, client: ApiClient, multimodal_capabilities: list[MultimodalCapability] | None | Unset = UNSET
) -> Optional[
    GetIntegrationsAndModelInfoLlmIntegrationsGetResponseGetIntegrationsAndModelInfoLlmIntegrationsGet
    | HTTPValidationError
]:
    """Get Integrations And Model Info

     Get the list of supported scorer models for the user's llm integrations.

    Args:
        multimodal_capabilities (list[MultimodalCapability] | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetIntegrationsAndModelInfoLlmIntegrationsGetResponseGetIntegrationsAndModelInfoLlmIntegrationsGet | HTTPValidationError
    """

    return (await asyncio_detailed(client=client, multimodal_capabilities=multimodal_capabilities)).parsed
