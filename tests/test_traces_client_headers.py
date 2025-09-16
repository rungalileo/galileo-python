"""Tests for X-Galileo-SDK header in TracesClient."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from galileo.traces import Traces
from galileo.utils.headers_data import get_package_version
from galileo_core.constants.request_method import RequestMethod


class TestTracesHeaders:
    """Test that X-Galileo-SDK headers are properly included in Trace requests."""

    @pytest.fixture
    def mock_config(self):
        """Mock GalileoPythonConfig."""
        with patch("galileo.traces.GalileoPythonConfig") as mock_config_class:
            mock_config = Mock()
            mock_api_client = Mock()
            mock_api_client.arequest = AsyncMock(return_value={"status": "ok"})
            mock_config.api_client = mock_api_client
            mock_config_class.get.return_value = mock_config
            yield mock_config

    @pytest.fixture
    def traces_client(self, mock_config):
        """Create a Traces instance for testing."""
        return Traces(
            project_id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a", log_stream_id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9b"
        )

    @pytest.mark.asyncio
    async def test_make_async_request_includes_sdk_header(self, traces_client, mock_config):
        """Test that _make_async_request includes the X-Galileo-SDK header."""
        # Call the private method directly to test header inclusion
        await traces_client._make_async_request(method=RequestMethod.GET, path="/test-endpoint")

        # Verify the request was made with correct headers
        mock_config.api_client.arequest.assert_called_once()
        call_args = mock_config.api_client.arequest.call_args

        # Check that content_headers contains X-Galileo-SDK header
        content_headers = call_args.kwargs.get("content_headers", {})
        assert "X-Galileo-SDK" in content_headers
        expected_header_value = f"galileo-python/{get_package_version()} Traces"
        assert content_headers["X-Galileo-SDK"] == expected_header_value
