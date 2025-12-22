from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any, cast

from galileo.__future__.shared.base import StateManagementMixin, SyncState
from galileo.__future__.shared.exceptions import APIError, ValidationError
from galileo.__future__.shared.utils import classproperty
from galileo.config import GalileoPythonConfig
from galileo.resources.api.integrations import (
    list_available_integrations_integrations_available_get,
    list_integrations_integrations_get,
)
from galileo.resources.models.integration_db import IntegrationDB
from galileo.resources.models.integration_name import IntegrationName
from galileo.resources.types import Unset
from galileo.utils.exceptions import APIException

if TYPE_CHECKING:
    from galileo.__future__.provider import (
        AnthropicProvider,
        AzureProvider,
        BedrockProvider,
        OpenAIProvider,
        Provider,
        UnconfiguredProvider,
    )

logger = logging.getLogger(__name__)


class Integration(StateManagementMixin):
    """
    Factory interface for managing Galileo integrations.

    Integration is the main entry point for working with LLM providers and other
    external services in the Galileo platform. It provides factory methods to create
    new integrations and list existing ones.

    The Integration class returns Provider objects, which are immutable proxies to
    integrations stored in the Galileo API. Provider classes should not be imported
    or instantiated directly - always use the Integration class methods.

    Attributes
    ----------
        id (str): The unique integration identifier.
        name (str): The integration name/type (e.g., "openai", "anthropic").
        created_at (datetime): When the integration was created.
        updated_at (datetime): When the integration was last updated.
        created_by (str): The user who created the integration.
        is_selected (bool): Whether this integration is selected by the current user.
        permissions (list): Integration permissions for the current user.

    Examples
    --------
        # List all available integration types (including unconnected)
        available_types = Integration.list(all=True)
        # Returns: ['anthropic', 'aws_bedrock', 'azure', 'openai', ...]

        # Create a new OpenAI integration
        openai = Integration.create_openai(
            token="sk-proj-...",
            organization_id="org-..."
        )
        print(f"Created: {openai.id}")

        # Create an Azure integration
        azure = Integration.create_azure(
            token="your-key",
            endpoint="https://your-resource.openai.azure.com"
        )

        # List all connected integrations (returns provider proxy objects)
        providers = Integration.list()
        for provider in providers:
            print(f"{provider.name}: {provider.id}")
            print(f"Created by: {provider.created_by}")
            print(f"Selected: {provider.is_selected}")

        # Update provider credentials
        openai.update(
            token="new-sk-proj-...",
            organization_id="new-org-..."
        )

        # Refresh provider state from API
        openai.refresh()

        # Get available models (placeholder - not yet implemented)
        # models = openai.models

        # Delete a provider
        openai.delete()

        # Create other providers
        bedrock = Integration.create_bedrock(
            aws_access_key_id="AKIA...",
            aws_secret_access_key="...",
            region="us-west-2"
        )

        anthropic = Integration.create_anthropic(token="sk-ant-...")
    """

    # Type annotations for instance attributes
    id: str | None
    name: str | None
    created_at: datetime | None
    updated_at: datetime | None
    created_by: str | None
    is_selected: bool
    permissions: list[Any] | None

    def __str__(self) -> str:
        """String representation of the integration."""
        return f"Integration(name='{self.name}', id='{self.id}')"

    def __repr__(self) -> str:
        """Detailed string representation of the integration."""
        return f"Integration(name='{self.name}', id='{self.id}', is_selected={self.is_selected})"

    def __init__(self) -> None:
        """
        Initialize an Integration instance.

        Note: Integration objects are read-only and typically retrieved via
        Integration.list(). Direct instantiation is not supported for end users.
        Use Integration.list() to get configured integrations.

        Raises
        ------
            ValidationError: Integration objects cannot be created directly.
                           Use Integration.list() instead.
        """
        super().__init__()
        raise ValidationError(
            "Integration objects cannot be created directly. "
            "Use Integration.list() to retrieve configured integrations or "
            "Integration.list(all=True) to get available integration types."
        )

    @classmethod
    def _create_empty(cls) -> Integration:
        """Internal constructor bypassing __init__ for API hydration."""
        instance = cls.__new__(cls)
        super(Integration, instance).__init__()
        # Initialize attributes
        instance.id = None
        instance.name = None
        instance.created_at = None
        instance.updated_at = None
        instance.created_by = None
        instance.is_selected = False
        instance.permissions = None
        return instance

    @classmethod
    def list(cls, *, all: bool = False) -> list[Provider] | list[str]:
        """
        List integrations.

        Args:
            all (bool): If True, returns all available integration types (including
                       unconnected ones) as a list of strings. If False, returns
                       only the configured integrations as Provider objects.
                       Defaults to False.

        Returns
        -------
            Union[list[Provider], list[str]]: List of Provider objects if
                all=False, or list of integration type names if all=True.

        Raises
        ------
            APIError: If the API call fails.

        Examples
        --------
            # List connected integrations (returns Provider objects)
            connected = Integration.list()
            for provider in connected:
                print(f"{provider.name}: {provider.id}")
                # You can now update, delete, or access models
                provider.refresh()

            # List all available integration types
            available = Integration.list(all=True)
            print(f"Available types: {available}")
        """
        config = GalileoPythonConfig.get()

        try:
            if all:
                logger.info("Integration.list: listing all available integration types")
                response = list_available_integrations_integrations_available_get.sync(client=config.api_client)
                if response and response.integrations:
                    # Convert IntegrationName enums to strings
                    available_integrations = [str(integration) for integration in response.integrations]
                    logger.info(f"Integration.list: found {len(available_integrations)} available types")
                    return available_integrations
                return []

            logger.info("Integration.list: listing configured integrations")
            retrieved_integrations = list_integrations_integrations_get.sync(client=config.api_client)

            if not retrieved_integrations:
                logger.info("Integration.list: found 0 configured integrations")
                return []

            logger.info(f"Integration.list: found {len(retrieved_integrations)} configured integrations")
            return [cls._to_provider(integration) for integration in retrieved_integrations]

        except APIException as e:
            error_msg = f"Failed to list integrations: {e!s}"
            logger.error(f"Integration.list: {error_msg}")
            raise APIError(error_msg) from e

    @classmethod
    def _from_api_response(cls, response: IntegrationDB) -> Integration:
        """
        Create an Integration instance from API response data.

        Args:
            response: IntegrationDB object from the API.

        Returns
        -------
            Integration: A new Integration instance populated with API data.
        """
        integration = cls._create_empty()
        integration.id = str(response.id)
        integration.name = str(response.name)
        integration.created_at = response.created_at
        integration.updated_at = response.updated_at
        integration.created_by = response.created_by

        # Handle Unset for optional fields
        integration.is_selected = response.is_selected if not isinstance(response.is_selected, Unset) else False
        integration.permissions = response.permissions if not isinstance(response.permissions, Unset) else None

        integration._set_state(SyncState.SYNCED)

        logger.debug(f"Integration._from_api_response: created integration {integration.name} (id={integration.id})")

        return integration

    def refresh(self) -> None:
        """
        Refresh the integration state from the remote API.

        Note: Currently, the API does not support fetching individual integrations
        by ID. This method will re-fetch all integrations and find the matching one.

        Raises
        ------
            APIError: If the API call fails or the integration is not found.
        """
        if self.id is None:
            error = ValidationError("Cannot refresh integration without an ID")
            self._set_state(SyncState.FAILED_SYNC, error)
            raise error

        logger.info(f"Integration.refresh: refreshing integration {self.id}")

        try:
            config = GalileoPythonConfig.get()
            all_integrations = list_integrations_integrations_get.sync(client=config.api_client)

            if not all_integrations:
                api_error = APIError(f"Integration with ID {self.id} not found")
                self._set_state(SyncState.FAILED_SYNC, api_error)
                raise api_error

            # Find this integration in the list
            for integration_data in all_integrations:
                if str(integration_data.id) == self.id:
                    # Update attributes
                    self.name = str(integration_data.name)
                    self.created_at = integration_data.created_at
                    self.updated_at = integration_data.updated_at
                    self.created_by = integration_data.created_by

                    # Handle Unset for optional fields
                    self.is_selected = (
                        integration_data.is_selected if not isinstance(integration_data.is_selected, Unset) else False
                    )
                    self.permissions = (
                        integration_data.permissions if not isinstance(integration_data.permissions, Unset) else None
                    )

                    self._set_state(SyncState.SYNCED)

                    logger.info(f"Integration.refresh: id={self.id} - completed")
                    return

            # If we didn't find it, raise an error
            api_error = APIError(f"Integration with ID {self.id} not found")
            self._set_state(SyncState.FAILED_SYNC, api_error)
            raise api_error

        except APIException as e:
            error_msg = f"Failed to refresh integration: {e!s}"
            logger.error(f"Integration.refresh: id={self.id} - failed: {error_msg}")
            api_error = APIError(error_msg)
            self._set_state(SyncState.FAILED_SYNC, api_error)
            raise api_error from e

    @classmethod
    def _to_provider(cls, integration_db: IntegrationDB) -> Provider:
        """
        Convert an IntegrationDB response to the appropriate Provider subclass.

        Args:
            integration_db: IntegrationDB object from the API.

        Returns
        -------
            Provider: A provider-specific instance (OpenAIProvider, AzureProvider, etc.).
                     For unsupported integration types, returns a GenericProvider.
        """
        name = str(integration_db.name)

        # Create appropriate provider instance based on name using __new__ to bypass __init__
        provider: Provider
        if name == IntegrationName.OPENAI:
            provider = OpenAIProvider.__new__(OpenAIProvider)
        elif name == IntegrationName.AZURE:
            provider = AzureProvider.__new__(AzureProvider)
        elif name == IntegrationName.AWS_BEDROCK:
            provider = BedrockProvider.__new__(BedrockProvider)
        elif name == IntegrationName.ANTHROPIC:
            provider = AnthropicProvider.__new__(AnthropicProvider)
        else:
            # For unsupported providers, use GenericProvider
            provider = GenericProvider.__new__(GenericProvider)
            # Store the integration name enum for _get_integration_name()
            provider._integration_name = integration_db.name

        # Initialize the StateManagementMixin parent class
        StateManagementMixin.__init__(provider)

        # Populate provider attributes from IntegrationDB
        provider.id = str(integration_db.id)
        provider.name = name
        provider.created_at = integration_db.created_at
        provider.updated_at = integration_db.updated_at
        provider.created_by = integration_db.created_by

        # Handle Unset for optional fields
        provider.is_selected = (
            integration_db.is_selected if not isinstance(integration_db.is_selected, Unset) else False
        )
        provider.permissions = integration_db.permissions if not isinstance(integration_db.permissions, Unset) else None

        provider._set_state(SyncState.SYNCED)

        logger.debug(f"Integration._to_provider: created {provider.__class__.__name__} (id={provider.id})")

        return provider

    # Convenience properties for accessing configured integrations by type

    @classmethod
    def _get_integration_by_name(cls, integration_name: str) -> Provider | UnconfiguredProvider:
        """
        Get a configured integration by name.

        Args:
            integration_name (str): The integration name (e.g., "openai", "azure").

        Returns
        -------
            Provider | UnconfiguredProvider: The provider if found, or an UnconfiguredProvider
                            that raises helpful errors when accessed.
                            If multiple integrations of the same type exist,
                            returns the selected one, or the first one if none selected.
        """
        try:
            providers_list = cls.list()
            # Type narrowing: list() without all=True returns list[Provider]
            if providers_list and isinstance(providers_list[0], str):
                return UnconfiguredProvider(integration_name)

            # Cast is safe because we checked for strings above
            providers = cast(list[Provider], providers_list)
            matching = [p for p in providers if p.name == integration_name]

            if not matching:
                logger.debug(f"Integration.{integration_name}: No '{integration_name}' integration configured.")
                return UnconfiguredProvider(integration_name)

            # If multiple matches, prefer the selected one
            selected = [p for p in matching if p.is_selected]
            if selected:
                return selected[0]

            # Otherwise return the first one
            return matching[0]
        except Exception as e:
            logger.error(f"Integration._get_integration_by_name: failed to get {integration_name}: {e}")
            return UnconfiguredProvider(integration_name)

    @classproperty
    def openai(cls) -> Provider | UnconfiguredProvider:
        """
        Get the configured OpenAI integration.

        Returns
        -------
            OpenAIProvider | UnconfiguredProvider: The OpenAI provider if configured,
                or UnconfiguredProvider that raises helpful errors when accessed.

        Examples
        --------
            openai = Integration.openai
            if openai:
                print(f"OpenAI integration: {openai.id}")
        """
        return cls._get_integration_by_name("openai")

    @classproperty
    def azure(cls) -> Provider | UnconfiguredProvider:
        """
        Get the configured Azure OpenAI integration.

        Returns
        -------
            AzureProvider | UnconfiguredProvider: The Azure provider if configured,
                or UnconfiguredProvider that raises helpful errors when accessed.

        Examples
        --------
            azure = Integration.azure
            if azure:
                print(f"Azure integration: {azure.id}")
        """
        return cls._get_integration_by_name("azure")

    @classproperty
    def bedrock(cls) -> Provider | UnconfiguredProvider:
        """
        Get the configured AWS Bedrock integration.

        Returns
        -------
            BedrockProvider | UnconfiguredProvider: The Bedrock provider if configured,
                or UnconfiguredProvider that raises helpful errors when accessed.

        Examples
        --------
            bedrock = Integration.bedrock
            if bedrock:
                print(f"Bedrock integration: {bedrock.id}")
        """
        return cls._get_integration_by_name("aws_bedrock")

    @classproperty
    def anthropic(cls) -> Provider | UnconfiguredProvider:
        """
        Get the configured Anthropic (Claude) integration.

        Returns
        -------
            AnthropicProvider | UnconfiguredProvider: The Anthropic provider if configured,
                or UnconfiguredProvider that raises helpful errors when accessed.

        Examples
        --------
            anthropic = Integration.anthropic
            if anthropic:
                print(f"Anthropic integration: {anthropic.id}")
        """
        return cls._get_integration_by_name("anthropic")

    @classproperty
    def vertex_ai(cls) -> Provider | UnconfiguredProvider:
        """
        Get the configured Google Vertex AI integration.

        Returns
        -------
            Provider | UnconfiguredProvider: The Vertex AI provider if configured,
                or UnconfiguredProvider that raises helpful errors when accessed.

        Examples
        --------
            vertex = Integration.vertex_ai
            if vertex:
                print(f"Vertex AI integration: {vertex.id}")
        """
        return cls._get_integration_by_name("vertex_ai")

    @classproperty
    def mistral(cls) -> Provider | UnconfiguredProvider:
        """
        Get the configured Mistral AI integration.

        Returns
        -------
            Provider | UnconfiguredProvider: The Mistral provider if configured,
                or UnconfiguredProvider that raises helpful errors when accessed.

        Examples
        --------
            mistral = Integration.mistral
            if mistral:
                print(f"Mistral integration: {mistral.id}")
        """
        return cls._get_integration_by_name("mistral")

    # Factory classmethods for creating providers

    @classmethod
    def create_openai(cls, *, token: str, organization_id: str | None = None) -> OpenAIProvider:
        """
        Create a new OpenAI integration.

        Args:
            token (str): OpenAI API token.
            organization_id (str | None): Optional organization ID.

        Returns
        -------
            OpenAIProvider: The created provider object.

        Raises
        ------
            APIError: If the API call fails.

        Examples
        --------
            provider = Integration.create_openai(
                token="sk-proj-...",
                organization_id="org-..."
            )
            print(f"Created: {provider.id}")
        """
        logger.info("Integration.create_openai: creating OpenAI integration")
        provider = OpenAIProvider(token=token, organization_id=organization_id)
        return provider.create()

    @classmethod
    def create_azure(cls, *, token: str, endpoint: str) -> AzureProvider:
        """
        Create a new Azure OpenAI integration.

        Args:
            token (str): Azure API key.
            endpoint (str): Azure OpenAI endpoint URL.

        Returns
        -------
            AzureProvider: The created provider object.

        Raises
        ------
            APIError: If the API call fails.

        Examples
        --------
            provider = Integration.create_azure(
                token="your-key",
                endpoint="https://your-resource.openai.azure.com"
            )
        """
        logger.info("Integration.create_azure: creating Azure integration")
        provider = AzureProvider(token=token, endpoint=endpoint)
        return provider.create()

    @classmethod
    def create_bedrock(
        cls,
        *,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region: str = "us-east-1",
        credential_type: str = "key_secret",
    ) -> BedrockProvider:
        """
        Create a new AWS Bedrock integration.

        Args:
            aws_access_key_id (str): AWS access key ID.
            aws_secret_access_key (str): AWS secret access key.
            region (str): AWS region. Defaults to "us-east-1".
            credential_type (str): Type of credentials. Defaults to "key_secret".

        Returns
        -------
            BedrockProvider: The created provider object.

        Raises
        ------
            APIError: If the API call fails.

        Examples
        --------
            provider = Integration.create_bedrock(
                aws_access_key_id="AKIA...",
                aws_secret_access_key="...",
                region="us-west-2"
            )
        """
        logger.info("Integration.create_bedrock: creating Bedrock integration")
        provider = BedrockProvider(
            credential_type=credential_type,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region=region,
        )
        return provider.create()

    @classmethod
    def create_anthropic(cls, *, token: str) -> AnthropicProvider:
        """
        Create a new Anthropic (Claude) integration.

        Args:
            token (str): Anthropic API token.

        Returns
        -------
            AnthropicProvider: The created provider object.

        Raises
        ------
            APIError: If the API call fails.

        Examples
        --------
            provider = Integration.create_anthropic(token="sk-ant-...")
        """
        logger.info("Integration.create_anthropic: creating Anthropic integration")
        provider = AnthropicProvider(token=token)
        return provider.create()


# Import Provider classes at end to avoid circular imports
from galileo.__future__.provider import (  # noqa: E402
    AnthropicProvider,
    AzureProvider,
    BedrockProvider,
    GenericProvider,
    OpenAIProvider,
    Provider,
    UnconfiguredProvider,
)
