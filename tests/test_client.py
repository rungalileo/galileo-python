"""Tests for the Galileo API client User-Agent functionality."""

import sys
from unittest.mock import patch

from galileo.resources.client import AuthenticatedClient, Client
from galileo.utils.user_agent import get_default_user_agent


# Read actual version from pyproject.toml for testing
def _get_version_from_pyproject() -> str:
    """Get version from pyproject.toml for testing."""
    import os
    import re

    # Find pyproject.toml
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)  # Go up from tests/ to project root
    pyproject_path = os.path.join(project_root, "pyproject.toml")

    if os.path.exists(pyproject_path):
        with open(pyproject_path) as f:
            content = f.read()
            # Look for version = "x.y.z" pattern
            match = re.search(r'version\s*=\s*"([^"]+)"', content)
            if match:
                return match.group(1)

    # Fallback if can't read pyproject.toml
    return "unknown"


class TestUserAgentGeneration:
    """Test User-Agent header generation and application."""

    def test_get_default_user_agent(self):
        """Test that the default User-Agent is correctly formatted."""
        user_agent = get_default_user_agent()

        # Test that it follows the expected format pattern
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

        # Should contain the basic structure
        assert user_agent.startswith("galileo-python-sdk")
        assert f"(Python {python_version})" in user_agent

        # If we can get version from pyproject.toml, test exact format
        expected_version = _get_version_from_pyproject()
        if expected_version != "unknown":
            expected = f"galileo-python-sdk/{expected_version} (Python {python_version})"
            assert user_agent == expected

    def test_get_default_user_agent_format(self):
        """Test that the User-Agent follows the correct format pattern."""
        user_agent = get_default_user_agent()

        # Should contain SDK name
        assert "galileo-python-sdk" in user_agent

        # Should contain Python version info
        assert "Python" in user_agent
        assert str(sys.version_info.major) in user_agent

    def test_version_fallback_in_test_environment(self):
        """Test that version detection works in test environments."""
        # Test the version detection directly
        version = _get_version_from_pyproject()

        # Should either get the real version or "unknown"
        assert isinstance(version, str)
        assert len(version) > 0

        # If we got a real version, it should be a valid semantic version pattern
        if version != "unknown":
            import re

            # Should match x.y.z pattern
            assert re.match(r"^\d+\.\d+\.\d+", version), f"Version {version} doesn't match semantic versioning pattern"


class TestClientUserAgent:
    """Test User-Agent header handling in the Client class."""

    def test_client_default_user_agent_sync(self):
        """Test that Client sets default User-Agent for sync httpx client."""
        client = Client(base_url="https://api.example.com")

        httpx_client = client.get_httpx_client()

        # Should have the default User-Agent header
        assert "User-Agent" in httpx_client.headers
        assert httpx_client.headers["User-Agent"] == get_default_user_agent()

    def test_client_default_user_agent_async(self):
        """Test that Client sets default User-Agent for async httpx client."""
        client = Client(base_url="https://api.example.com")

        async_client = client.get_async_httpx_client()

        # Should have the default User-Agent header
        assert "User-Agent" in async_client.headers
        assert async_client.headers["User-Agent"] == get_default_user_agent()

    def test_client_custom_user_agent_preserved_sync(self):
        """Test that custom User-Agent headers are preserved in sync client."""
        custom_user_agent = "MyCustomApp/1.0.0"
        client = Client(base_url="https://api.example.com", headers={"User-Agent": custom_user_agent})

        httpx_client = client.get_httpx_client()

        # Should preserve the custom User-Agent
        assert httpx_client.headers["User-Agent"] == custom_user_agent

    def test_client_custom_user_agent_preserved_async(self):
        """Test that custom User-Agent headers are preserved in async client."""
        custom_user_agent = "MyCustomApp/1.0.0"
        client = Client(base_url="https://api.example.com", headers={"User-Agent": custom_user_agent})

        async_client = client.get_async_httpx_client()

        # Should preserve the custom User-Agent
        assert async_client.headers["User-Agent"] == custom_user_agent

    def test_client_with_headers_user_agent_override(self):
        """Test that User-Agent can be overridden using with_headers method."""
        client = Client(base_url="https://api.example.com")

        # Initially should have default User-Agent
        initial_client = client.get_httpx_client()
        assert initial_client.headers["User-Agent"] == get_default_user_agent()

        # Override with custom User-Agent
        custom_user_agent = "OverriddenApp/2.0.0"
        updated_client = client.with_headers({"User-Agent": custom_user_agent})

        # Should have the overridden User-Agent
        httpx_client = updated_client.get_httpx_client()
        assert httpx_client.headers["User-Agent"] == custom_user_agent


class TestAuthenticatedClientUserAgent:
    """Test User-Agent header handling in the AuthenticatedClient class."""

    def test_authenticated_client_default_user_agent_sync(self):
        """Test that AuthenticatedClient sets default User-Agent for sync httpx client."""
        client = AuthenticatedClient(base_url="https://api.example.com", token="test-token")

        httpx_client = client.get_httpx_client()

        # Should have both Authorization and User-Agent headers
        assert "Authorization" in httpx_client.headers
        assert "User-Agent" in httpx_client.headers
        assert httpx_client.headers["User-Agent"] == get_default_user_agent()

    def test_authenticated_client_default_user_agent_async(self):
        """Test that AuthenticatedClient sets default User-Agent for async httpx client."""
        client = AuthenticatedClient(base_url="https://api.example.com", token="test-token")

        async_client = client.get_async_httpx_client()

        # Should have both Authorization and User-Agent headers
        assert "Authorization" in async_client.headers
        assert "User-Agent" in async_client.headers
        assert async_client.headers["User-Agent"] == get_default_user_agent()

    def test_authenticated_client_custom_user_agent_preserved_sync(self):
        """Test that custom User-Agent headers are preserved in AuthenticatedClient sync."""
        custom_user_agent = "AuthenticatedApp/1.0.0"
        client = AuthenticatedClient(
            base_url="https://api.example.com", token="test-token", headers={"User-Agent": custom_user_agent}
        )

        httpx_client = client.get_httpx_client()

        # Should preserve the custom User-Agent
        assert httpx_client.headers["User-Agent"] == custom_user_agent
        # Should still have authentication
        assert httpx_client.headers["Authorization"] == "Bearer test-token"

    def test_authenticated_client_custom_user_agent_preserved_async(self):
        """Test that custom User-Agent headers are preserved in AuthenticatedClient async."""
        custom_user_agent = "AuthenticatedApp/1.0.0"
        client = AuthenticatedClient(
            base_url="https://api.example.com", token="test-token", headers={"User-Agent": custom_user_agent}
        )

        async_client = client.get_async_httpx_client()

        # Should preserve the custom User-Agent
        assert async_client.headers["User-Agent"] == custom_user_agent
        # Should still have authentication
        assert async_client.headers["Authorization"] == "Bearer test-token"

    def test_authenticated_client_custom_auth_prefix(self):
        """Test that custom auth prefix works with User-Agent."""
        client = AuthenticatedClient(
            base_url="https://api.example.com",
            token="test-token",
            prefix="Token",  # Custom prefix instead of Bearer
        )

        httpx_client = client.get_httpx_client()

        # Should have custom auth header and default User-Agent
        assert httpx_client.headers["Authorization"] == "Token test-token"
        assert httpx_client.headers["User-Agent"] == get_default_user_agent()

    def test_authenticated_client_with_headers_user_agent_override(self):
        """Test that User-Agent can be overridden using with_headers method on AuthenticatedClient."""
        client = AuthenticatedClient(base_url="https://api.example.com", token="test-token")

        # Initially should have default User-Agent
        initial_client = client.get_httpx_client()
        assert initial_client.headers["User-Agent"] == get_default_user_agent()

        # Override with custom User-Agent
        custom_user_agent = "OverriddenAuthApp/2.0.0"
        updated_client = client.with_headers({"User-Agent": custom_user_agent})

        # Should have the overridden User-Agent and keep auth
        httpx_client = updated_client.get_httpx_client()
        assert httpx_client.headers["User-Agent"] == custom_user_agent
        assert httpx_client.headers["Authorization"] == "Bearer test-token"


class TestUserAgentIntegration:
    """Integration tests for User-Agent across different scenarios."""

    def test_user_agent_with_mixed_headers(self):
        """Test User-Agent behavior with other custom headers."""
        client = AuthenticatedClient(
            base_url="https://api.example.com",
            token="test-token",
            headers={"X-Custom-Header": "custom-value", "Accept": "application/json"},
        )

        httpx_client = client.get_httpx_client()

        # Should have all headers including auto-generated User-Agent
        assert httpx_client.headers["X-Custom-Header"] == "custom-value"
        assert httpx_client.headers["Accept"] == "application/json"
        assert httpx_client.headers["Authorization"] == "Bearer test-token"
        assert httpx_client.headers["User-Agent"] == get_default_user_agent()

    def test_user_agent_consistency_across_client_instances(self):
        """Test that User-Agent is consistent across multiple client instances."""
        client1 = Client(base_url="https://api.example.com")
        client2 = AuthenticatedClient(base_url="https://api.example.com", token="token")

        httpx_client1 = client1.get_httpx_client()
        httpx_client2 = client2.get_httpx_client()

        # Both should have the same default User-Agent
        assert httpx_client1.headers["User-Agent"] == httpx_client2.headers["User-Agent"]
        assert httpx_client1.headers["User-Agent"] == get_default_user_agent()

    @patch("galileo.utils.user_agent._get_package_version", return_value="1.0.0-test")
    def test_user_agent_reflects_version_changes(self, mock_version):
        """Test that User-Agent reflects version changes when mocked."""
        client = Client(base_url="https://api.example.com")
        httpx_client = client.get_httpx_client()

        # Should reflect the mocked version
        user_agent = httpx_client.headers["User-Agent"]
        assert "1.0.0-test" in user_agent
        assert "galileo-python-sdk/1.0.0-test" in user_agent

    @patch("galileo.utils.user_agent._get_package_version", return_value="")
    def test_user_agent_handles_empty_version(self, mock_version):
        """Test that User-Agent handles empty version gracefully."""
        client = Client(base_url="https://api.example.com")
        httpx_client = client.get_httpx_client()

        # Should handle empty version gracefully (no slash after sdk name)
        user_agent = httpx_client.headers["User-Agent"]
        assert user_agent.startswith("galileo-python-sdk (Python")
        assert "/" not in user_agent.split("(")[0]  # No slash before the Python version

    def test_user_agent_headers_are_copied_not_mutated(self):
        """Test that the internal headers dict is not mutated during User-Agent addition."""
        client = Client(base_url="https://api.example.com")

        # Get the original headers
        original_headers = client._headers.copy()

        # Create httpx client (this should add User-Agent)
        httpx_client = client.get_httpx_client()

        # Original headers should not be modified
        assert client._headers == original_headers
        assert "User-Agent" not in client._headers

        # But the httpx client should have User-Agent
        assert "User-Agent" in httpx_client.headers
