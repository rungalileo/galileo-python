from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from galileo.__future__.shared.base import StateManagementMixin, SyncState
from galileo.__future__.shared.exceptions import APIError, ValidationError
from galileo.config import GalileoPythonConfig
from galileo.resources.api.integrations import (
    create_or_update_integration_integrations_anthropic_put,
    create_or_update_integration_integrations_aws_bedrock_put,
    create_or_update_integration_integrations_azure_put,
    create_or_update_integration_integrations_openai_put,
    delete_integration_integrations_name_delete,
    get_integration_integrations_name_get,
)
from galileo.resources.api.llm_integrations import get_available_models_llm_integrations_llm_integration_models_get
from galileo.resources.models import (
    AnthropicIntegrationCreate,
    AzureIntegrationCreate,
    BaseAwsIntegrationCreate,
    HTTPValidationError,
    IntegrationName,
    OpenAIIntegrationCreate,
)
from galileo.resources.types import Unset
from galileo.utils.exceptions import APIException

logger = logging.getLogger(__name__)


class Provider(StateManagementMixin, ABC):
    """
    Base class for provider-specific integration objects.

    Providers represent configured integrations (e.g., OpenAI, Azure, Bedrock)
    that are stored remotely in the Galileo API. Providers are immutable proxies
    that only store minimal metadata (id, name, timestamps). No credentials are
    stored locally for security reasons.

    Providers should only be obtained through Integration class methods, not
    instantiated directly by users.

    Attributes
    ----------
        id (str | None): The unique integration identifier.
        name (str): The integration name/type (e.g., "openai", "azure").
        created_at (datetime | None): When the integration was created.
        updated_at (datetime | None): When the integration was last updated.
        created_by (str | None): The user who created the integration.
        is_selected (bool): Whether this integration is selected by the current user.
        permissions (list | None): Integration permissions for the current user.
    """

    id: str | None
    name: str
    created_at: datetime | None
    updated_at: datetime | None
    created_by: str | None
    is_selected: bool
    permissions: list[Any] | None

    def __init__(self) -> None:
        """Initialize a Provider instance."""
        super().__init__()
        self.id = None
        self.name = ""
        self.created_at = None
        self.updated_at = None
        self.created_by = None
        self.is_selected = False
        self.permissions = None
        self._set_state(SyncState.LOCAL_ONLY)

    def __str__(self) -> str:
        """String representation of the provider."""
        return f"{self.__class__.__name__}(name='{self.name}', id='{self.id}')"

    def __repr__(self) -> str:
        """Detailed string representation of the provider."""
        return f"{self.__class__.__name__}(name='{self.name}', id='{self.id}', is_selected={self.is_selected})"

    @abstractmethod
    def _get_integration_name(self) -> IntegrationName:
        """Get the IntegrationName enum for this provider."""
        raise NotImplementedError

    def refresh(self) -> None:
        """
        Refresh the provider state from the remote API.

        Raises
        ------
            APIError: If the API call fails or the integration is not found.
            ValidationError: If the provider has no ID.
        """
        if self.id is None:
            error = ValidationError("Cannot refresh provider without an ID")
            self._set_state(SyncState.FAILED_SYNC, error)
            raise error

        logger.info(f"{self.__class__.__name__}.refresh: id='{self.id}' - started")

        try:
            config = GalileoPythonConfig.get()
            integration_name = self._get_integration_name()

            # Get the specific integration data
            response = get_integration_integrations_name_get.sync(name=integration_name, client=config.api_client)

            if response is None or isinstance(response, HTTPValidationError):
                api_error = APIError(f"Provider with ID {self.id} not found")
                self._set_state(SyncState.FAILED_SYNC, api_error)
                raise api_error

            # Update attributes from response
            self._update_from_api_response(response)
            self._set_state(SyncState.SYNCED)

            logger.info(f"{self.__class__.__name__}.refresh: id='{self.id}' - completed")

        except APIException as e:
            error_msg = f"Failed to refresh provider: {e!s}"
            logger.error(f"{self.__class__.__name__}.refresh: id='{self.id}' - failed: {error_msg}")
            api_error = APIError(error_msg)
            self._set_state(SyncState.FAILED_SYNC, api_error)
            raise api_error from e

    def _update_from_api_response(self, response: Any) -> None:
        """Update instance attributes from API response."""
        self.id = str(response.id) if hasattr(response, "id") else self.id
        self.name = str(response.name) if hasattr(response, "name") else self.name
        self.created_at = response.created_at if hasattr(response, "created_at") else self.created_at
        self.updated_at = response.updated_at if hasattr(response, "updated_at") else self.updated_at
        self.created_by = response.created_by if hasattr(response, "created_by") else self.created_by

        # Handle Unset for optional fields
        if hasattr(response, "is_selected"):
            self.is_selected = response.is_selected if not isinstance(response.is_selected, Unset) else False
        if hasattr(response, "permissions"):
            self.permissions = response.permissions if not isinstance(response.permissions, Unset) else None

    def delete(self) -> None:
        """
        Delete this provider integration.

        This permanently removes the integration from the API. After deletion,
        the object state is set to DELETED.

        WARNING: This operation cannot be undone!

        Raises
        ------
            APIError: If the API call fails.
            ValidationError: If the provider has not been created yet.
        """
        if self.id is None:
            error = ValidationError("Cannot delete provider without an ID. Create the provider first.")
            self._set_state(SyncState.FAILED_SYNC, error)
            raise error

        logger.info(f"{self.__class__.__name__}.delete: id='{self.id}' - started")

        try:
            config = GalileoPythonConfig.get()
            integration_name = self._get_integration_name()

            result = delete_integration_integrations_name_delete.sync(name=integration_name, client=config.api_client)

            if isinstance(result, HTTPValidationError):
                raise APIError(f"Failed to delete provider: {result.detail}")

            self._set_state(SyncState.DELETED)
            logger.info(f"{self.__class__.__name__}.delete: id='{self.id}' - completed")

        except APIException as e:
            error_msg = f"Failed to delete provider: {e!s}"
            logger.error(f"{self.__class__.__name__}.delete: id='{self.id}' - failed: {error_msg}")
            api_error = APIError(error_msg)
            self._set_state(SyncState.FAILED_SYNC, api_error)
            raise api_error from e

    @property
    def models(self) -> list[Model]:
        """
        Get available models for this provider.

        Returns
        -------
            list[Model]: List of available models for this provider.

        Raises
        ------
            APIError: If the API call fails.
            ValidationError: If the provider has not been synced with the API.
        """
        if not self.is_synced():
            error = ValidationError("Cannot get models for provider without syncing")
            raise error

        logger.info(f"{self.__class__.__name__}.models: Fetching models for '{self.name}'")

        try:
            config = GalileoPythonConfig.get()
            integration_name = self._get_integration_name()

            # Get models from API
            response = get_available_models_llm_integrations_llm_integration_models_get.sync(
                llm_integration=integration_name, client=config.api_client
            )

            if response is None or isinstance(response, HTTPValidationError):
                raise APIError(f"Failed to get models for provider '{self.name}'")

            # Convert list of model name strings to Model objects
            models = [Model(name=model_name, alias=model_name, provider_name=self.name) for model_name in response]

            logger.info(f"{self.__class__.__name__}.models: Found {len(models)} model(s) for '{self.name}'")
            return models

        except APIException as e:
            error_msg = f"Failed to get models for provider: {e!s}"
            logger.error(f"{self.__class__.__name__}.models: failed: {error_msg}")
            raise APIError(error_msg) from e

    def get_model(self, *, name: str | None = None, alias: str | None = None) -> Model | None:
        """
        Get a specific model by name or alias.

        Args:
            name (str | None): The model name to search for.
            alias (str | None): The model alias to search for.

        Returns
        -------
            Model | None: The matching Model object, or None if not found.

        Raises
        ------
            ValidationError: If neither name nor alias is provided, or if both are provided.
            APIError: If the API call to fetch models fails.

        Examples
        --------
            # Get model by alias
            openai = Integration.openai
            model = openai.get_model(alias="gpt-4o-mini")

            # Get model by name
            model = openai.get_model(name="gpt-4o-mini")
        """
        if name is None and alias is None:
            raise ValidationError("Must specify either 'name' or 'alias'")
        if name is not None and alias is not None:
            raise ValidationError("Cannot specify both 'name' and 'alias'")

        logger.debug(
            f"{self.__class__.__name__}.get_model: "
            f"Searching for model with {'name' if name else 'alias'}="
            f"'{name if name else alias}' in provider '{self.name}'"
        )

        # Get all available models
        available_models = self.models

        # Search by name or alias
        search_value = name if name is not None else alias
        search_attr = "name" if name is not None else "alias"

        for model in available_models:
            if getattr(model, search_attr) == search_value:
                logger.debug(
                    f"{self.__class__.__name__}.get_model: Found model '{model.name}' with alias '{model.alias}'"
                )
                return model

        logger.debug(
            f"{self.__class__.__name__}.get_model: "
            f"No model found with {search_attr}='{search_value}' in provider '{self.name}'"
        )
        return None


class OpenAIProvider(Provider):
    """
    OpenAI integration provider.

    This is an immutable proxy to an OpenAI integration stored in the Galileo API.
    Credentials are never stored locally - they are only sent to the API during
    create/update operations.
    """

    # Temporary storage for credentials during creation (not persisted)
    _temp_token: str | None
    _temp_organization_id: str | None

    def __init__(self, *, token: str, organization_id: str | None = None) -> None:
        """
        Initialize an OpenAI provider for creation.

        Note: Credentials are only stored temporarily for the create() call.

        Args:
            token (str): OpenAI API token.
            organization_id (str | None): Optional organization ID.
        """
        super().__init__()
        self.name = "openai"
        # Store temporarily for create() call only
        self._temp_token = token
        self._temp_organization_id = organization_id

    def _get_integration_name(self) -> IntegrationName:
        return IntegrationName.OPENAI

    def create(self) -> OpenAIProvider:
        """
        Create or update this OpenAI integration in the API.

        Returns
        -------
            OpenAIProvider: Self, with updated state from API.

        Raises
        ------
            APIError: If the API call fails.
            ValidationError: If credentials are not available.
        """
        if not hasattr(self, "_temp_token") or self._temp_token is None:
            raise ValidationError("Cannot create OpenAI provider without token")

        logger.info(f"OpenAIProvider.create: name='{self.name}' - started")

        try:
            config = GalileoPythonConfig.get()
            body = OpenAIIntegrationCreate(token=self._temp_token, organization_id=self._temp_organization_id)

            response = create_or_update_integration_integrations_openai_put.sync(client=config.api_client, body=body)

            if isinstance(response, HTTPValidationError):
                raise APIError(f"Failed to create provider: {response.detail}")

            if response is None:
                raise APIError("Failed to create provider: no response")

            # Update attributes from response
            self._update_from_api_response(response)
            self._set_state(SyncState.SYNCED)

            # Clear temporary credentials
            self._temp_token = None
            self._temp_organization_id = None

            logger.info(f"OpenAIProvider.create: id='{self.id}' - completed")
            return self

        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"OpenAIProvider.create: failed: {e}")
            raise APIError(f"Failed to create OpenAI provider: {e}") from e

    def update(self, *, token: str, organization_id: str | None = None) -> OpenAIProvider:
        """
        Update this OpenAI integration credentials.

        Credentials are sent to the API but never stored locally.

        Args:
            token (str): New API token.
            organization_id (str | None): New organization ID.

        Returns
        -------
            OpenAIProvider: Self, with updated state.

        Raises
        ------
            APIError: If the API call fails.
            ValidationError: If the provider has not been created yet.
        """
        if self.id is None:
            raise ValidationError("Cannot update provider without an ID. Create the provider first.")

        logger.info(f"OpenAIProvider.update: id='{self.id}' - started")

        try:
            config = GalileoPythonConfig.get()
            body = OpenAIIntegrationCreate(token=token, organization_id=organization_id)

            response = create_or_update_integration_integrations_openai_put.sync(client=config.api_client, body=body)

            if isinstance(response, HTTPValidationError):
                raise APIError(f"Failed to update provider: {response.detail}")

            if response is None:
                raise APIError("Failed to update provider: no response")

            # Update attributes from response (does NOT include credentials)
            self._update_from_api_response(response)
            self._set_state(SyncState.SYNCED)

            logger.info(f"OpenAIProvider.update: id='{self.id}' - completed")
            return self

        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"OpenAIProvider.update: failed: {e}")
            raise APIError(f"Failed to update OpenAI provider: {e}") from e


class AzureProvider(Provider):
    """
    Azure OpenAI integration provider.

    This is an immutable proxy to an Azure integration stored in the Galileo API.
    Credentials are never stored locally - they are only sent to the API during
    create/update operations.
    """

    # Temporary storage for credentials during creation (not persisted)
    _temp_token: str | None
    _temp_endpoint: str | None

    def __init__(self, *, token: str, endpoint: str) -> None:
        """
        Initialize an Azure provider for creation.

        Note: Credentials are only stored temporarily for the create() call.

        Args:
            token (str): Azure API key.
            endpoint (str): Azure OpenAI endpoint URL.
        """
        super().__init__()
        self.name = "azure"
        # Store temporarily for create() call only
        self._temp_token = token
        self._temp_endpoint = endpoint

    def _get_integration_name(self) -> IntegrationName:
        return IntegrationName.AZURE

    def create(self) -> AzureProvider:
        """
        Create or update this Azure integration in the API.

        Returns
        -------
            AzureProvider: Self, with updated state from API.

        Raises
        ------
            APIError: If the API call fails.
            ValidationError: If credentials are not available.
        """
        if not hasattr(self, "_temp_token") or self._temp_token is None:
            raise ValidationError("Cannot create Azure provider without token")
        if not hasattr(self, "_temp_endpoint") or self._temp_endpoint is None:
            raise ValidationError("Cannot create Azure provider without endpoint")

        logger.info(f"AzureProvider.create: name='{self.name}' - started")

        try:
            config = GalileoPythonConfig.get()
            body = AzureIntegrationCreate(token=self._temp_token, endpoint=self._temp_endpoint)

            response = create_or_update_integration_integrations_azure_put.sync(client=config.api_client, body=body)

            if isinstance(response, HTTPValidationError):
                raise APIError(f"Failed to create provider: {response.detail}")

            if response is None:
                raise APIError("Failed to create provider: no response")

            self._update_from_api_response(response)
            self._set_state(SyncState.SYNCED)

            # Clear temporary credentials
            self._temp_token = None
            self._temp_endpoint = None

            logger.info(f"AzureProvider.create: id='{self.id}' - completed")
            return self

        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"AzureProvider.create: failed: {e}")
            raise APIError(f"Failed to create Azure provider: {e}") from e

    def update(self, *, token: str, endpoint: str) -> AzureProvider:
        """
        Update this Azure integration credentials.

        Credentials are sent to the API but never stored locally.

        Args:
            token (str): New API key.
            endpoint (str): New endpoint URL.

        Returns
        -------
            AzureProvider: Self, with updated state.

        Raises
        ------
            APIError: If the API call fails.
            ValidationError: If the provider has not been created yet.
        """
        if self.id is None:
            raise ValidationError("Cannot update provider without an ID. Create the provider first.")

        logger.info(f"AzureProvider.update: id='{self.id}' - started")

        try:
            config = GalileoPythonConfig.get()
            body = AzureIntegrationCreate(token=token, endpoint=endpoint)

            response = create_or_update_integration_integrations_azure_put.sync(client=config.api_client, body=body)

            if isinstance(response, HTTPValidationError):
                raise APIError(f"Failed to update provider: {response.detail}")

            if response is None:
                raise APIError("Failed to update provider: no response")

            # Update attributes from response (does NOT include credentials)
            self._update_from_api_response(response)
            self._set_state(SyncState.SYNCED)

            logger.info(f"AzureProvider.update: id='{self.id}' - completed")
            return self

        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"AzureProvider.update: failed: {e}")
            raise APIError(f"Failed to update Azure provider: {e}") from e


class BedrockProvider(Provider):
    """
    AWS Bedrock integration provider.

    This is an immutable proxy to a Bedrock integration stored in the Galileo API.
    Credentials are never stored locally - they are only sent to the API during
    create/update operations.
    """

    # Temporary storage for credentials during creation (not persisted)
    _temp_credential_type: str | None
    _temp_region: str | None
    _temp_token_dict: dict[str, str] | None

    def __init__(
        self,
        *,
        credential_type: str = "key_secret",
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region: str = "us-east-1",
    ) -> None:
        """
        Initialize a Bedrock provider for creation.

        Note: Credentials are only stored temporarily for the create() call.

        Args:
            credential_type (str): Type of credentials ("key_secret" or "assume_role").
            aws_access_key_id (str): AWS access key ID.
            aws_secret_access_key (str): AWS secret access key.
            region (str): AWS region.
        """
        super().__init__()
        self.name = "aws_bedrock"
        # Store temporarily for create() call only
        self._temp_credential_type = credential_type
        self._temp_region = region
        self._temp_token_dict = {"aws_access_key_id": aws_access_key_id, "aws_secret_access_key": aws_secret_access_key}

    def _get_integration_name(self) -> IntegrationName:
        return IntegrationName.AWS_BEDROCK

    def create(self) -> BedrockProvider:
        """
        Create or update this Bedrock integration in the API.

        Returns
        -------
            BedrockProvider: Self, with updated state from API.

        Raises
        ------
            APIError: If the API call fails.
            ValidationError: If credentials are not available.
        """
        if not hasattr(self, "_temp_token_dict") or self._temp_token_dict is None:
            raise ValidationError("Cannot create Bedrock provider without credentials")

        logger.info(f"BedrockProvider.create: name='{self.name}' - started")

        try:
            config = GalileoPythonConfig.get()
            body = BaseAwsIntegrationCreate(
                credential_type=self._temp_credential_type or "key_secret",
                token=self._temp_token_dict,
                region=self._temp_region or "us-east-1",
            )

            response = create_or_update_integration_integrations_aws_bedrock_put.sync(
                client=config.api_client, body=body
            )

            if isinstance(response, HTTPValidationError):
                raise APIError(f"Failed to create provider: {response.detail}")

            if response is None:
                raise APIError("Failed to create provider: no response")

            self._update_from_api_response(response)
            self._set_state(SyncState.SYNCED)

            # Clear temporary credentials
            self._temp_credential_type = None
            self._temp_region = None
            self._temp_token_dict = None

            logger.info(f"BedrockProvider.create: id='{self.id}' - completed")
            return self

        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"BedrockProvider.create: failed: {e}")
            raise APIError(f"Failed to create Bedrock provider: {e}") from e

    def update(
        self,
        *,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region: str = "us-east-1",
        credential_type: str = "key_secret",
    ) -> BedrockProvider:
        """
        Update this Bedrock integration credentials.

        Credentials are sent to the API but never stored locally.

        Args:
            aws_access_key_id (str): New AWS access key ID.
            aws_secret_access_key (str): New AWS secret access key.
            region (str): New AWS region.
            credential_type (str): Type of credentials.

        Returns
        -------
            BedrockProvider: Self, with updated state.

        Raises
        ------
            APIError: If the API call fails.
            ValidationError: If the provider has not been created yet.
        """
        if self.id is None:
            raise ValidationError("Cannot update provider without an ID. Create the provider first.")

        logger.info(f"BedrockProvider.update: id='{self.id}' - started")

        try:
            config = GalileoPythonConfig.get()
            token_dict = {"aws_access_key_id": aws_access_key_id, "aws_secret_access_key": aws_secret_access_key}
            body = BaseAwsIntegrationCreate(credential_type=credential_type, token=token_dict, region=region)

            response = create_or_update_integration_integrations_aws_bedrock_put.sync(
                client=config.api_client, body=body
            )

            if isinstance(response, HTTPValidationError):
                raise APIError(f"Failed to update provider: {response.detail}")

            if response is None:
                raise APIError("Failed to update provider: no response")

            # Update attributes from response (does NOT include credentials)
            self._update_from_api_response(response)
            self._set_state(SyncState.SYNCED)

            logger.info(f"BedrockProvider.update: id='{self.id}' - completed")
            return self

        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"BedrockProvider.update: failed: {e}")
            raise APIError(f"Failed to update Bedrock provider: {e}") from e


class AnthropicProvider(Provider):
    """
    Anthropic (Claude) integration provider.

    This is an immutable proxy to an Anthropic integration stored in the Galileo API.
    Credentials are never stored locally - they are only sent to the API during
    create/update operations.
    """

    # Temporary storage for credentials during creation (not persisted)
    _temp_token: str | None

    def __init__(self, *, token: str) -> None:
        """
        Initialize an Anthropic provider for creation.

        Note: Credentials are only stored temporarily for the create() call.

        Args:
            token (str): Anthropic API token.
        """
        super().__init__()
        self.name = "anthropic"
        # Store temporarily for create() call only
        self._temp_token = token

    def _get_integration_name(self) -> IntegrationName:
        return IntegrationName.ANTHROPIC

    def create(self) -> AnthropicProvider:
        """
        Create or update this Anthropic integration in the API.

        Returns
        -------
            AnthropicProvider: Self, with updated state from API.

        Raises
        ------
            APIError: If the API call fails.
            ValidationError: If credentials are not available.
        """
        if not hasattr(self, "_temp_token") or self._temp_token is None:
            raise ValidationError("Cannot create Anthropic provider without token")

        logger.info(f"AnthropicProvider.create: name='{self.name}' - started")

        try:
            config = GalileoPythonConfig.get()
            body = AnthropicIntegrationCreate(token=self._temp_token)

            response = create_or_update_integration_integrations_anthropic_put.sync(client=config.api_client, body=body)

            if isinstance(response, HTTPValidationError):
                raise APIError(f"Failed to create provider: {response.detail}")

            if response is None:
                raise APIError("Failed to create provider: no response")

            self._update_from_api_response(response)
            self._set_state(SyncState.SYNCED)

            # Clear temporary credentials
            self._temp_token = None

            logger.info(f"AnthropicProvider.create: id='{self.id}' - completed")
            return self

        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"AnthropicProvider.create: failed: {e}")
            raise APIError(f"Failed to create Anthropic provider: {e}") from e

    def update(self, *, token: str) -> AnthropicProvider:
        """
        Update this Anthropic integration credentials.

        Credentials are sent to the API but never stored locally.

        Args:
            token (str): New API token.

        Returns
        -------
            AnthropicProvider: Self, with updated state.

        Raises
        ------
            APIError: If the API call fails.
            ValidationError: If the provider has not been created yet.
        """
        if self.id is None:
            raise ValidationError("Cannot update provider without an ID. Create the provider first.")

        logger.info(f"AnthropicProvider.update: id='{self.id}' - started")

        try:
            config = GalileoPythonConfig.get()
            body = AnthropicIntegrationCreate(token=token)

            response = create_or_update_integration_integrations_anthropic_put.sync(client=config.api_client, body=body)

            if isinstance(response, HTTPValidationError):
                raise APIError(f"Failed to update provider: {response.detail}")

            if response is None:
                raise APIError("Failed to update provider: no response")

            # Update attributes from response (does NOT include credentials)
            self._update_from_api_response(response)
            self._set_state(SyncState.SYNCED)

            logger.info(f"AnthropicProvider.update: id='{self.id}' - completed")
            return self

        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"AnthropicProvider.update: failed: {e}")
            raise APIError(f"Failed to update Anthropic provider: {e}") from e


class GenericProvider(Provider):
    """
    Generic provider for integration types that don't have specialized implementations.

    This provider is used for integration types like 'mistral', 'nvidia', 'writer',
    'vertex_ai', 'aws_sagemaker', 'databricks', 'labelstudio', etc. that are available
    in the API but don't yet have dedicated Provider subclasses.

    GenericProvider is read-only and only supports basic operations:
    - Listing (returned from Integration.list())
    - Refreshing state
    - Deleting

    It does not support creation or updates through the SDK.
    """

    _integration_name: IntegrationName

    def _get_integration_name(self) -> IntegrationName:
        return self._integration_name


# Import Model here to avoid circular imports
from galileo.__future__.model import Model  # noqa: E402
