from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.anthropic_integration import AnthropicIntegration
from ...models.aws_bedrock_integration import AwsBedrockIntegration
from ...models.aws_sage_maker_integration import AwsSageMakerIntegration
from ...models.azure_integration import AzureIntegration
from ...models.databricks_integration import DatabricksIntegration
from ...models.http_validation_error import HTTPValidationError
from ...models.integration_name import IntegrationName
from ...models.label_studio_integration import LabelStudioIntegration
from ...models.mistral_integration import MistralIntegration
from ...models.open_ai_integration import OpenAIIntegration
from ...models.vertex_ai_integration import VertexAIIntegration
from ...models.writer_integration import WriterIntegration
from ...types import Response


def _get_kwargs(name: IntegrationName) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {"method": "get", "url": f"/integrations/{name}"}

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        HTTPValidationError,
        Union[
            "AnthropicIntegration",
            "AwsBedrockIntegration",
            "AwsSageMakerIntegration",
            "AzureIntegration",
            "DatabricksIntegration",
            "LabelStudioIntegration",
            "MistralIntegration",
            "OpenAIIntegration",
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
            "DatabricksIntegration",
            "LabelStudioIntegration",
            "MistralIntegration",
            "OpenAIIntegration",
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
                response_200_type_3 = DatabricksIntegration.from_dict(data)

                return response_200_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_4 = LabelStudioIntegration.from_dict(data)

                return response_200_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_5 = OpenAIIntegration.from_dict(data)

                return response_200_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_6 = VertexAIIntegration.from_dict(data)

                return response_200_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_7 = WriterIntegration.from_dict(data)

                return response_200_type_7
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_8 = AnthropicIntegration.from_dict(data)

                return response_200_type_8
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_9 = MistralIntegration.from_dict(data)

            return response_200_type_9

        response_200 = _parse_response_200(response.json())

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
) -> Response[
    Union[
        HTTPValidationError,
        Union[
            "AnthropicIntegration",
            "AwsBedrockIntegration",
            "AwsSageMakerIntegration",
            "AzureIntegration",
            "DatabricksIntegration",
            "LabelStudioIntegration",
            "MistralIntegration",
            "OpenAIIntegration",
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
    name: IntegrationName, *, client: AuthenticatedClient
) -> Response[
    Union[
        HTTPValidationError,
        Union[
            "AnthropicIntegration",
            "AwsBedrockIntegration",
            "AwsSageMakerIntegration",
            "AzureIntegration",
            "DatabricksIntegration",
            "LabelStudioIntegration",
            "MistralIntegration",
            "OpenAIIntegration",
            "VertexAIIntegration",
            "WriterIntegration",
        ],
    ]
]:
    """Get Integration

     Gets the integration data formatted for the specified integration.

    Args:
        name (IntegrationName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['AnthropicIntegration', 'AwsBedrockIntegration', 'AwsSageMakerIntegration', 'AzureIntegration', 'DatabricksIntegration', 'LabelStudioIntegration', 'MistralIntegration', 'OpenAIIntegration', 'VertexAIIntegration', 'WriterIntegration']]]
    """

    kwargs = _get_kwargs(name=name)

    response = client.get_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


def sync(
    name: IntegrationName, *, client: AuthenticatedClient
) -> Optional[
    Union[
        HTTPValidationError,
        Union[
            "AnthropicIntegration",
            "AwsBedrockIntegration",
            "AwsSageMakerIntegration",
            "AzureIntegration",
            "DatabricksIntegration",
            "LabelStudioIntegration",
            "MistralIntegration",
            "OpenAIIntegration",
            "VertexAIIntegration",
            "WriterIntegration",
        ],
    ]
]:
    """Get Integration

     Gets the integration data formatted for the specified integration.

    Args:
        name (IntegrationName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['AnthropicIntegration', 'AwsBedrockIntegration', 'AwsSageMakerIntegration', 'AzureIntegration', 'DatabricksIntegration', 'LabelStudioIntegration', 'MistralIntegration', 'OpenAIIntegration', 'VertexAIIntegration', 'WriterIntegration']]
    """

    return sync_detailed(name=name, client=client).parsed


async def asyncio_detailed(
    name: IntegrationName, *, client: AuthenticatedClient
) -> Response[
    Union[
        HTTPValidationError,
        Union[
            "AnthropicIntegration",
            "AwsBedrockIntegration",
            "AwsSageMakerIntegration",
            "AzureIntegration",
            "DatabricksIntegration",
            "LabelStudioIntegration",
            "MistralIntegration",
            "OpenAIIntegration",
            "VertexAIIntegration",
            "WriterIntegration",
        ],
    ]
]:
    """Get Integration

     Gets the integration data formatted for the specified integration.

    Args:
        name (IntegrationName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['AnthropicIntegration', 'AwsBedrockIntegration', 'AwsSageMakerIntegration', 'AzureIntegration', 'DatabricksIntegration', 'LabelStudioIntegration', 'MistralIntegration', 'OpenAIIntegration', 'VertexAIIntegration', 'WriterIntegration']]]
    """

    kwargs = _get_kwargs(name=name)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: IntegrationName, *, client: AuthenticatedClient
) -> Optional[
    Union[
        HTTPValidationError,
        Union[
            "AnthropicIntegration",
            "AwsBedrockIntegration",
            "AwsSageMakerIntegration",
            "AzureIntegration",
            "DatabricksIntegration",
            "LabelStudioIntegration",
            "MistralIntegration",
            "OpenAIIntegration",
            "VertexAIIntegration",
            "WriterIntegration",
        ],
    ]
]:
    """Get Integration

     Gets the integration data formatted for the specified integration.

    Args:
        name (IntegrationName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['AnthropicIntegration', 'AwsBedrockIntegration', 'AwsSageMakerIntegration', 'AzureIntegration', 'DatabricksIntegration', 'LabelStudioIntegration', 'MistralIntegration', 'OpenAIIntegration', 'VertexAIIntegration', 'WriterIntegration']]
    """

    return (await asyncio_detailed(name=name, client=client)).parsed
