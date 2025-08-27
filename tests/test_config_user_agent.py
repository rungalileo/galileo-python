"""Tests for User-Agent configuration at the config level."""

from unittest.mock import patch

from galileo.config import GalileoPythonConfig
from galileo.utils.user_agent import get_default_user_agent


class TestConfigUserAgent:
    """Test User-Agent header configuration at the config level."""

    def test_config_api_client_has_user_agent(self):
        """Test that the galileo_core ApiClient gets User-Agent from config."""
        config = GalileoPythonConfig.get()
        api_client = config.api_client

        # Should have User-Agent header configured
        assert hasattr(api_client, "_headers")
        assert "User-Agent" in api_client._headers
        assert api_client._headers["User-Agent"] == get_default_user_agent()

    def test_config_user_agent_not_overridden_if_exists(self):
        """Test that existing User-Agent headers are not overridden."""
        config = GalileoPythonConfig.get()
        api_client = config.api_client

        # Set a custom User-Agent
        custom_user_agent = "CustomClient/1.0.0"
        api_client._headers["User-Agent"] = custom_user_agent

        # Get client again - should preserve custom User-Agent
        api_client2 = config.api_client
        assert api_client2._headers["User-Agent"] == custom_user_agent

    @patch("galileo.utils.user_agent._get_package_version", return_value="2.0.0-config")
    def test_config_user_agent_reflects_version_changes(self, mock_version):
        """Test that config-level User-Agent reflects version changes."""
        # Reset config to get fresh instance
        config = GalileoPythonConfig.get()
        config.reset()

        config = GalileoPythonConfig.get()
        api_client = config.api_client

        # Should reflect the mocked version
        user_agent = api_client._headers["User-Agent"]
        assert "2.0.0-config" in user_agent
        assert "galileo-python-sdk/2.0.0-config" in user_agent

    def test_config_user_agent_survives_client_recreation(self):
        """Test that User-Agent persists when client is recreated."""
        config = GalileoPythonConfig.get()

        # Get client multiple times
        client1 = config.api_client
        client2 = config.api_client

        # Should have consistent User-Agent
        assert client1._headers["User-Agent"] == client2._headers["User-Agent"]
        assert client1._headers["User-Agent"] == get_default_user_agent()
