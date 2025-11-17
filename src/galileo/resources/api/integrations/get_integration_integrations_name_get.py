from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

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
from ...models.integration_name import IntegrationName
from ...models.label_studio_integration import LabelStudioIntegration
from ...models.mistral_integration import MistralIntegration
from ...models.nvidia_integration import NvidiaIntegration
from ...models.open_ai_integration import OpenAIIntegration
from ...models.vegas_gateway_integration import VegasGatewayIntegration
from ...models.vertex_ai_integration import VertexAIIntegration
from ...models.writer_integration import WriterIntegration
from ...types import Response


def _get_kwargs(name: IntegrationName) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": RequestMethod.GET,
        "return_raw_response": True,
        "path": f"/integrations/{name}",
    }

    headers["X-Galileo-SDK"] = get_sdk_header()

    _kwargs["content_headers"] = headers
    return _kwargs


def _parse_response(
    *, client: ApiClient, response: httpx.Response
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
            "LabelStudioIntegration",
            "MistralIntegration",
            "NvidiaIntegration",
            "OpenAIIntegration",
            "VegasGatewayIntegration",
            "VertexAIIntegration",
            "WriterIntegration",
        ],
    ]
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
            "LabelStudioIntegration",
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
                return AwsBedrockIntegration.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AwsSageMakerIntegration.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AzureIntegration.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AnthropicIntegration.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CustomIntegration.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return DatabricksIntegration.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return LabelStudioIntegration.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return MistralIntegration.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return NvidiaIntegration.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return OpenAIIntegration.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return VegasGatewayIntegration.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return VertexAIIntegration.from_dict(data)

            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            return WriterIntegration.from_dict(data)

        return _parse_response_200(response.json())

    if response.status_code == 422:
        return HTTPValidationError.from_dict(response.json())

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


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
            "LabelStudioIntegration",
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
    name: IntegrationName, *, client: ApiClient
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
            "LabelStudioIntegration",
            "MistralIntegration",
            "NvidiaIntegration",
            "OpenAIIntegration",
            "VegasGatewayIntegration",
            "VertexAIIntegration",
            "WriterIntegration",
        ],
    ]
]:
    """Get Integration.

     Gets the integration data formatted for the specified integration.

    Args:
        name (IntegrationName):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, Union['AnthropicIntegration', 'AwsBedrockIntegration', 'AwsSageMakerIntegration', 'AzureIntegration', 'CustomIntegration', 'DatabricksIntegration', 'LabelStudioIntegration', 'MistralIntegration', 'NvidiaIntegration', 'OpenAIIntegration', 'VegasGatewayIntegration', 'VertexAIIntegration', 'WriterIntegration']]]
    """
    kwargs = _get_kwargs(name=name)

    response = client.request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    name: IntegrationName, *, client: ApiClient
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
            "LabelStudioIntegration",
            "MistralIntegration",
            "NvidiaIntegration",
            "OpenAIIntegration",
            "VegasGatewayIntegration",
            "VertexAIIntegration",
            "WriterIntegration",
        ],
    ]
]:
    """Get Integration.

     Gets the integration data formatted for the specified integration.

    Args:
        name (IntegrationName):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, Union['AnthropicIntegration', 'AwsBedrockIntegration', 'AwsSageMakerIntegration', 'AzureIntegration', 'CustomIntegration', 'DatabricksIntegration', 'LabelStudioIntegration', 'MistralIntegration', 'NvidiaIntegration', 'OpenAIIntegration', 'VegasGatewayIntegration', 'VertexAIIntegration', 'WriterIntegration']]
    """
    return sync_detailed(name=name, client=client).parsed


async def asyncio_detailed(
    name: IntegrationName, *, client: ApiClient
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
            "LabelStudioIntegration",
            "MistralIntegration",
            "NvidiaIntegration",
            "OpenAIIntegration",
            "VegasGatewayIntegration",
            "VertexAIIntegration",
            "WriterIntegration",
        ],
    ]
]:
    """Get Integration.

     Gets the integration data formatted for the specified integration.

    Args:
        name (IntegrationName):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Response[Union[HTTPValidationError, Union['AnthropicIntegration', 'AwsBedrockIntegration', 'AwsSageMakerIntegration', 'AzureIntegration', 'CustomIntegration', 'DatabricksIntegration', 'LabelStudioIntegration', 'MistralIntegration', 'NvidiaIntegration', 'OpenAIIntegration', 'VegasGatewayIntegration', 'VertexAIIntegration', 'WriterIntegration']]]
    """
    kwargs = _get_kwargs(name=name)

    response = await client.arequest(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: IntegrationName, *, client: ApiClient
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
            "LabelStudioIntegration",
            "MistralIntegration",
            "NvidiaIntegration",
            "OpenAIIntegration",
            "VegasGatewayIntegration",
            "VertexAIIntegration",
            "WriterIntegration",
        ],
    ]
]:
    """Get Integration.

     Gets the integration data formatted for the specified integration.

    Args:
        name (IntegrationName):

    Raises
    ------
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns
    -------
        Union[HTTPValidationError, Union['AnthropicIntegration', 'AwsBedrockIntegration', 'AwsSageMakerIntegration', 'AzureIntegration', 'CustomIntegration', 'DatabricksIntegration', 'LabelStudioIntegration', 'MistralIntegration', 'NvidiaIntegration', 'OpenAIIntegration', 'VegasGatewayIntegration', 'VertexAIIntegration', 'WriterIntegration']]
    """
    return (await asyncio_detailed(name=name, client=client)).parsed
