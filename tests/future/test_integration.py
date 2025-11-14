from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from galileo.__future__ import Integration
from galileo.__future__.provider import AnthropicProvider, AzureProvider, BedrockProvider, OpenAIProvider, Provider
from galileo.__future__.shared.exceptions import ValidationError
from galileo.resources.models.available_integrations import AvailableIntegrations
from galileo.resources.models.integration_db import IntegrationDB
from galileo.resources.models.integration_name import IntegrationName

# Test data
INTEGRATION_TYPES = [
    ("openai", IntegrationName.OPENAI, OpenAIProvider),
    ("anthropic", IntegrationName.ANTHROPIC, AnthropicProvider),
    ("azure", IntegrationName.AZURE, AzureProvider),
    ("aws_bedrock", IntegrationName.AWS_BEDROCK, BedrockProvider),
]


def create_mock_integration(name: IntegrationName, is_selected: bool = False) -> IntegrationDB:
    """Create a mock integration DB response."""
    mock = MagicMock(spec=IntegrationDB)
    mock.id = str(uuid4())
    mock.name = name
    mock.created_at = datetime.now()
    mock.updated_at = datetime.now()
    mock.created_by = str(uuid4())
    mock.is_selected = is_selected
    mock.permissions = ["read"]
    return mock


class TestIntegrationInit:
    """Test Integration initialization."""

    def test_direct_init_raises_error(self):
        """Cannot instantiate Integration directly."""
        with pytest.raises(ValidationError, match="cannot be created directly"):
            Integration()


class TestIntegrationList:
    """Test Integration.list() methods."""

    @patch("galileo.__future__.integration.GalileoPythonConfig.get")
    @patch("galileo.__future__.integration.list_available_integrations_integrations_available_get")
    def test_list_all_returns_strings(self, mock_available, mock_config):
        """list(all=True) returns list of string type names."""
        mock_response = MagicMock(spec=AvailableIntegrations)
        mock_response.integrations = [IntegrationName.OPENAI, IntegrationName.ANTHROPIC, IntegrationName.AZURE]
        mock_available.sync.return_value = mock_response

        result = Integration.list(all=True)

        assert isinstance(result, list)
        assert all(isinstance(t, str) for t in result)
        assert "openai" in result
        assert "anthropic" in result
        assert "azure" in result

    @patch("galileo.__future__.integration.GalileoPythonConfig.get")
    @patch("galileo.__future__.integration.list_integrations_integrations_get")
    def test_list_returns_providers(self, mock_list, mock_config):
        """list() returns Provider objects."""
        mock_list.sync.return_value = [
            create_mock_integration(IntegrationName.OPENAI, is_selected=True),
            create_mock_integration(IntegrationName.ANTHROPIC),
        ]

        result = Integration.list()

        assert len(result) == 2
        assert isinstance(result[0], OpenAIProvider)
        assert isinstance(result[1], AnthropicProvider)
        assert result[0].name == "openai"
        assert result[0].is_selected is True
        assert result[1].name == "anthropic"
        assert result[1].is_selected is False

    @patch("galileo.__future__.integration.GalileoPythonConfig.get")
    @patch("galileo.__future__.integration.list_integrations_integrations_get")
    def test_list_empty_returns_empty_list(self, mock_list, mock_config):
        """list() returns empty list when no integrations."""
        mock_list.sync.return_value = []

        result = Integration.list()

        assert result == []

    @patch("galileo.__future__.integration.GalileoPythonConfig.get")
    @patch("galileo.__future__.integration.list_integrations_integrations_get")
    @pytest.mark.parametrize("name,enum_name,provider_class", INTEGRATION_TYPES)
    def test_list_creates_correct_provider_type(self, mock_list, mock_config, name, enum_name, provider_class):
        """list() creates correct Provider subclass for each type."""
        mock_list.sync.return_value = [create_mock_integration(enum_name)]

        result = Integration.list()

        assert len(result) == 1
        assert isinstance(result[0], provider_class)
        assert result[0].name == name


class TestIntegrationRefresh:
    """Test Integration.refresh() method."""

    @patch("galileo.__future__.integration.GalileoPythonConfig.get")
    @patch("galileo.__future__.integration.list_integrations_integrations_get")
    def test_refresh_updates_attributes(self, mock_list, mock_config):
        """refresh() updates integration attributes from API."""
        mock_integration = create_mock_integration(IntegrationName.OPENAI)
        integration = Integration._from_api_response(mock_integration)

        # Update mock for refresh
        updated_mock = create_mock_integration(IntegrationName.OPENAI)
        updated_mock.id = mock_integration.id
        updated_mock.is_selected = True
        updated_mock.permissions = ["read", "update"]
        mock_list.sync.return_value = [updated_mock]

        integration.refresh()

        assert integration.is_selected is True
        assert integration.permissions == ["read", "update"]

    def test_refresh_without_id_raises_error(self):
        """refresh() raises error if integration has no ID."""
        integration = Integration._create_empty()

        with pytest.raises(ValidationError, match="Cannot refresh integration without an ID"):
            integration.refresh()


class TestIntegrationConvenienceProperties:
    """Test Integration convenience properties (openai, azure, etc)."""

    @patch("galileo.__future__.integration.GalileoPythonConfig.get")
    @patch("galileo.__future__.integration.list_integrations_integrations_get")
    def test_property_returns_configured_integration(self, mock_list, mock_config):
        """Integration.openai returns OpenAI provider if configured."""
        mock_list.sync.return_value = [create_mock_integration(IntegrationName.OPENAI)]

        result = Integration.openai

        assert isinstance(result, OpenAIProvider)
        assert result.name == "openai"

    @patch("galileo.__future__.integration.GalileoPythonConfig.get")
    @patch("galileo.__future__.integration.list_integrations_integrations_get")
    def test_property_returns_none_when_not_configured(self, mock_list, mock_config):
        """Integration.azure returns None if not configured."""
        mock_list.sync.return_value = []

        result = Integration.azure

        assert result is None

    @patch("galileo.__future__.integration.GalileoPythonConfig.get")
    @patch("galileo.__future__.integration.list_integrations_integrations_get")
    def test_property_prefers_selected_integration(self, mock_list, mock_config):
        """Property returns selected integration when multiple exist."""
        mock1 = create_mock_integration(IntegrationName.OPENAI, is_selected=False)
        mock2 = create_mock_integration(IntegrationName.OPENAI, is_selected=True)
        mock_list.sync.return_value = [mock1, mock2]

        result = Integration.openai

        assert result.id == str(mock2.id)
        assert result.is_selected is True


class TestIntegrationFactoryMethods:
    """Test Integration factory methods."""

    @patch("galileo.__future__.provider.GalileoPythonConfig.get")
    @patch("galileo.__future__.provider.create_or_update_integration_integrations_openai_put")
    def test_create_openai_returns_provider(self, mock_create, mock_config):
        """create_openai() returns OpenAIProvider."""
        mock_response = create_mock_integration(IntegrationName.OPENAI)
        mock_create.sync.return_value = mock_response

        result = Integration.create_openai(token="sk-test")

        assert isinstance(result, OpenAIProvider)
        assert result.id == str(mock_response.id)

    @patch("galileo.__future__.provider.GalileoPythonConfig.get")
    @patch("galileo.__future__.provider.create_or_update_integration_integrations_azure_put")
    def test_create_azure_returns_provider(self, mock_create, mock_config):
        """create_azure() returns AzureProvider."""
        mock_response = create_mock_integration(IntegrationName.AZURE)
        mock_create.sync.return_value = mock_response

        result = Integration.create_azure(token="key", endpoint="https://test.openai.azure.com")

        assert isinstance(result, AzureProvider)
        assert result.id == str(mock_response.id)

    @patch("galileo.__future__.provider.GalileoPythonConfig.get")
    @patch("galileo.__future__.provider.create_or_update_integration_integrations_aws_bedrock_put")
    def test_create_bedrock_returns_provider(self, mock_create, mock_config):
        """create_bedrock() returns BedrockProvider."""
        mock_response = create_mock_integration(IntegrationName.AWS_BEDROCK)
        mock_create.sync.return_value = mock_response

        result = Integration.create_bedrock(aws_access_key_id="AKIA", aws_secret_access_key="secret")

        assert isinstance(result, BedrockProvider)
        assert result.id == str(mock_response.id)

    @patch("galileo.__future__.provider.GalileoPythonConfig.get")
    @patch("galileo.__future__.provider.create_or_update_integration_integrations_anthropic_put")
    def test_create_anthropic_returns_provider(self, mock_create, mock_config):
        """create_anthropic() returns AnthropicProvider."""
        mock_response = create_mock_integration(IntegrationName.ANTHROPIC)
        mock_create.sync.return_value = mock_response

        result = Integration.create_anthropic(token="sk-ant-test")

        assert isinstance(result, AnthropicProvider)
        assert result.id == str(mock_response.id)


class TestIntegrationToProvider:
    """Test Integration._to_provider() method."""

    @pytest.mark.parametrize("name,enum_name,provider_class", INTEGRATION_TYPES)
    def test_creates_correct_provider_type(self, name, enum_name, provider_class):
        """_to_provider() creates correct Provider subclass."""
        mock_integration = create_mock_integration(enum_name)

        provider = Integration._to_provider(mock_integration)

        assert isinstance(provider, provider_class)
        assert provider.name == name
        assert provider.id == str(mock_integration.id)
        assert provider.is_synced()

    def test_creates_generic_provider_for_unknown_type(self):
        """_to_provider() creates GenericProvider for unsupported types."""
        mock_integration = create_mock_integration(IntegrationName.MISTRAL)

        provider = Integration._to_provider(mock_integration)

        assert isinstance(provider, Provider)
        assert provider.name == "mistral"
        assert provider.is_synced()
