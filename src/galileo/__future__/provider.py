"""Deprecated: use galileo.provider instead of galileo.__future__.provider."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.provider is deprecated. Use galileo.provider instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.provider import (  # noqa: E402
    AnthropicProvider,
    AzureProvider,
    BedrockProvider,
    GenericProvider,
    Model,
    OpenAIProvider,
    Provider,
    UnconfiguredProvider,
)

__all__ = [
    "AnthropicProvider",
    "AzureProvider",
    "BedrockProvider",
    "GenericProvider",
    "Model",
    "OpenAIProvider",
    "Provider",
    "UnconfiguredProvider",
]
