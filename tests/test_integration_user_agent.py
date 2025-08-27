"""Integration tests to verify User-Agent works across both client systems."""

from unittest.mock import patch

from galileo.base import BaseClientModel
from galileo.config import GalileoPythonConfig
from galileo.resources.client import AuthenticatedClient, Client
from galileo.utils.user_agent import get_default_user_agent


class TestUserAgentIntegration:
    """Test User-Agent integration across both client systems."""

    def test_both_client_systems_have_user_agent(self):
        """Test that both OpenAPI and galileo_core clients have User-Agent."""

        # Test OpenAPI-generated client (what we originally implemented)
        openapi_client = AuthenticatedClient(base_url="https://api.example.com", token="test-token")
        openapi_httpx = openapi_client.get_httpx_client()

        # Test galileo_core client via configuration
        base_model = BaseClientModel()
        galileo_core_client = base_model.client

        # Both should have User-Agent headers
        assert "User-Agent" in openapi_httpx.headers
        assert hasattr(galileo_core_client, "_headers")
        assert "User-Agent" in galileo_core_client._headers

        # Both should have the same User-Agent value
        expected_user_agent = get_default_user_agent()
        assert openapi_httpx.headers["User-Agent"] == expected_user_agent
        assert galileo_core_client._headers["User-Agent"] == expected_user_agent

    def test_user_agent_consistency_across_systems(self):
        """Test that User-Agent is consistent across different client instances."""

        # Create multiple client instances
        config = GalileoPythonConfig.get()
        galileo_core_1 = config.api_client

        base_model = BaseClientModel()
        galileo_core_2 = base_model.client

        openapi_client = Client(base_url="https://api.example.com")
        openapi_httpx = openapi_client.get_httpx_client()

        # All should have the same User-Agent
        expected_user_agent = get_default_user_agent()
        assert galileo_core_1._headers["User-Agent"] == expected_user_agent
        assert galileo_core_2._headers["User-Agent"] == expected_user_agent
        assert openapi_httpx.headers["User-Agent"] == expected_user_agent

    @patch("galileo.utils.user_agent._get_package_version", return_value="3.0.0-integration")
    def test_version_changes_propagate_to_both_systems(self, mock_version):
        """Test that version changes affect both client systems."""

        # Reset config to get fresh instances
        config = GalileoPythonConfig.get()
        config.reset()

        # Create fresh instances
        base_model = BaseClientModel()
        galileo_core_client = base_model.client

        openapi_client = AuthenticatedClient(base_url="https://api.example.com", token="test-token")
        openapi_httpx = openapi_client.get_httpx_client()

        # Both should reflect the mocked version
        assert "3.0.0-integration" in galileo_core_client._headers["User-Agent"]
        assert "3.0.0-integration" in openapi_httpx.headers["User-Agent"]

        # Both should have the full expected format
        expected_pattern = "galileo-python-sdk/3.0.0-integration"
        assert expected_pattern in galileo_core_client._headers["User-Agent"]
        assert expected_pattern in openapi_httpx.headers["User-Agent"]

    def test_custom_user_agent_override_works_independently(self):
        """Test that custom User-Agent can be set independently on each system."""

        # Set custom User-Agent on OpenAPI client
        custom_openapi_agent = "CustomOpenAPI/1.0.0"
        openapi_client = Client(base_url="https://api.example.com", headers={"User-Agent": custom_openapi_agent})
        openapi_httpx = openapi_client.get_httpx_client()

        # Set custom User-Agent on galileo_core client
        custom_core_agent = "CustomCore/2.0.0"
        base_model = BaseClientModel()
        galileo_core_client = base_model.client
        galileo_core_client._headers["User-Agent"] = custom_core_agent

        # Each should have its own custom User-Agent
        assert openapi_httpx.headers["User-Agent"] == custom_openapi_agent
        assert galileo_core_client._headers["User-Agent"] == custom_core_agent

    def test_configuration_level_takes_precedence_for_galileo_core(self):
        """Test that configuration-level User-Agent is set for galileo_core clients."""

        # Create fresh config and client
        config = GalileoPythonConfig.get()
        api_client = config.api_client

        # Should have default User-Agent from configuration
        assert "User-Agent" in api_client._headers
        assert api_client._headers["User-Agent"] == get_default_user_agent()

        # Verify it follows the expected format
        user_agent = api_client._headers["User-Agent"]
        assert user_agent.startswith("galileo-python-sdk")
        assert "Python" in user_agent
