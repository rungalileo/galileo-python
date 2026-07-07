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
from ...models.anthropic_integration import AnthropicIntegration
from ...models.aws_bedrock_integration import AwsBedrockIntegration
from ...models.aws_sage_maker_integration import AwsSageMakerIntegration
from ...models.azure_integration import AzureIntegration
from ...models.custom_integration import CustomIntegration
from ...models.databricks_integration import DatabricksIntegration
from ...models.http_validation_error import HTTPValidationError
from ...models.integration_provider import IntegrationProvider
from ...models.mistral_integration import MistralIntegration
from ...models.nvidia_integration import NvidiaIntegration
from ...models.open_ai_integration import OpenAIIntegration
from ...models.vegas_gateway_integration import VegasGatewayIntegration
from ...models.vertex_ai_integration import VertexAIIntegration
from ...models.writer_integration import WriterIntegration
from ...types import Response


def _get_kwargs(name: IntegrationProvider) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": "/integrations/{name}".format(name=name),
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
) -> Union[
    HTTPValidationError,
    Union[
        "AnthropicIntegration",
        "AwsBedrockIntegration",
        "AwsSageMakerIntegration",
        "AzureIntegration",
        "CustomIntegration",
        "DatabricksIntegration",
        "MistralIntegration",
        "NvidiaIntegration",
        "OpenAIIntegration",
        "VegasGatewayIntegration",
        "VertexAIIntegration",
        "WriterIntegration",
    ],
]:
    if response.status_code == 200:

        def _parse_response_200(
            data: object,
        ) -> Union[
            "AnthropicIntegration",
            "AwsBedrockIntegration",
            "AwsSageMakerIntegration",
            "AzureIntegration",
            "CustomIntegration",
            "DatabricksIntegration",
            "MistralIntegration",
            "NvidiaIntegration",
            "OpenAIIntegration",
            "VegasGatewayIntegration",
            "VertexAIIntegration",
            "WriterIntegration",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = AwsBedrockIntegration.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_1 = AwsSageMakerIntegration.from_dict(data)

                return response_200_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_2 = AzureIntegration.from_dict(data)

                return response_200_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_3 = AnthropicIntegration.from_dict(data)

                return response_200_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_4 = CustomIntegration.from_dict(data)

                return response_200_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_5 = DatabricksIntegration.from_dict(data)

                return response_200_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_6 = MistralIntegration.from_dict(data)

                return response_200_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_7 = NvidiaIntegration.from_dict(data)

                return response_200_type_7
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_8 = OpenAIIntegration.from_dict(data)

                return response_200_type_8
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_9 = VegasGatewayIntegration.from_dict(data)

                return response_200_type_9
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_10 = VertexAIIntegration.from_dict(data)

                return response_200_type_10
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_11 = WriterIntegration.from_dict(data)

            return response_200_type_11

        response_200 = _parse_response_200(response.json())

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
    Union[
        HTTPValidationError,
        Union[
            "AnthropicIntegration",
            "AwsBedrockIntegration",
            "AwsSageMakerIntegration",
            "AzureIntegration",
            "CustomIntegration",
            "DatabricksIntegration",
            "MistralIntegration",
            "NvidiaIntegration",
            "OpenAIIntegration",
            "VegasGatewayIntegration",
            "VertexAIIntegration",
            "WriterIntegration",
        ],
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: IntegrationProvider, *, client: ApiClient
) -> Response[
    Union[
        HTTPValidationError,
        Union[
            "AnthropicIntegration",
            "AwsBedrockIntegration",
            "AwsSageMakerIntegration",
            "AzureIntegration",
            "CustomIntegration",
            "DatabricksIntegration",
            "MistralIntegration",
            "NvidiaIntegration",
            "OpenAIIntegration",
            "VegasGatewayIntegration",
            "VertexAIIntegration",
            "WriterIntegration",
        ],
    ]
]:
    """Get Integration

     Gets the integration data formatted for the specified integration.

    Args:
        name (IntegrationProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['AnthropicIntegration', 'AwsBedrockIntegration', 'AwsSageMakerIntegration', 'AzureIntegration', 'CustomIntegration', 'DatabricksIntegration', 'MistralIntegration', 'NvidiaIntegration', 'OpenAIIntegration', 'VegasGatewayIntegration', 'VertexAIIntegration', 'WriterIntegration']]]
    """

    kwargs = _get_kwargs(name=name)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    name: IntegrationProvider, *, client: ApiClient
) -> Optional[
    Union[
        HTTPValidationError,
        Union[
            "AnthropicIntegration",
            "AwsBedrockIntegration",
            "AwsSageMakerIntegration",
            "AzureIntegration",
            "CustomIntegration",
            "DatabricksIntegration",
            "MistralIntegration",
            "NvidiaIntegration",
            "OpenAIIntegration",
            "VegasGatewayIntegration",
            "VertexAIIntegration",
            "WriterIntegration",
        ],
    ]
]:
    """Get Integration

     Gets the integration data formatted for the specified integration.

    Args:
        name (IntegrationProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['AnthropicIntegration', 'AwsBedrockIntegration', 'AwsSageMakerIntegration', 'AzureIntegration', 'CustomIntegration', 'DatabricksIntegration', 'MistralIntegration', 'NvidiaIntegration', 'OpenAIIntegration', 'VegasGatewayIntegration', 'VertexAIIntegration', 'WriterIntegration']]
    """

    return sync_detailed(name=name, client=client).parsed


async def asyncio_detailed(
    name: IntegrationProvider, *, client: ApiClient
) -> Response[
    Union[
        HTTPValidationError,
        Union[
            "AnthropicIntegration",
            "AwsBedrockIntegration",
            "AwsSageMakerIntegration",
            "AzureIntegration",
            "CustomIntegration",
            "DatabricksIntegration",
            "MistralIntegration",
            "NvidiaIntegration",
            "OpenAIIntegration",
            "VegasGatewayIntegration",
            "VertexAIIntegration",
            "WriterIntegration",
        ],
    ]
]:
    """Get Integration

     Gets the integration data formatted for the specified integration.

    Args:
        name (IntegrationProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['AnthropicIntegration', 'AwsBedrockIntegration', 'AwsSageMakerIntegration', 'AzureIntegration', 'CustomIntegration', 'DatabricksIntegration', 'MistralIntegration', 'NvidiaIntegration', 'OpenAIIntegration', 'VegasGatewayIntegration', 'VertexAIIntegration', 'WriterIntegration']]]
    """

    kwargs = _get_kwargs(name=name)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: IntegrationProvider, *, client: ApiClient
) -> Optional[
    Union[
        HTTPValidationError,
        Union[
            "AnthropicIntegration",
            "AwsBedrockIntegration",
            "AwsSageMakerIntegration",
            "AzureIntegration",
            "CustomIntegration",
            "DatabricksIntegration",
            "MistralIntegration",
            "NvidiaIntegration",
            "OpenAIIntegration",
            "VegasGatewayIntegration",
            "VertexAIIntegration",
            "WriterIntegration",
        ],
    ]
]:
    """Get Integration

     Gets the integration data formatted for the specified integration.

    Args:
        name (IntegrationProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['AnthropicIntegration', 'AwsBedrockIntegration', 'AwsSageMakerIntegration', 'AzureIntegration', 'CustomIntegration', 'DatabricksIntegration', 'MistralIntegration', 'NvidiaIntegration', 'OpenAIIntegration', 'VegasGatewayIntegration', 'VertexAIIntegration', 'WriterIntegration']]
    """

    return (await asyncio_detailed(name=name, client=client)).parsed
