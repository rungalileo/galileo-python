"""Tests for X-Galileo-SDK header in TracesClient."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from galileo.traces import IngestTraces, Traces
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
    async def test_make_async_request_includes_sdk_header(self, traces_client, mock_config) -> None:
        """Test that _make_async_request includes the X-Galileo-SDK header with dynamic method name."""
        # Call the private method directly to test header inclusion
        await traces_client._make_async_request(request_method=RequestMethod.GET, endpoint="/test-endpoint")

        # Verify the request was made with correct headers
        mock_config.api_client.arequest.assert_called_once()
        call_args = mock_config.api_client.arequest.call_args

        # Check that content_headers contains X-Galileo-SDK header
        content_headers = call_args.kwargs.get("content_headers", {})
        assert "X-Galileo-SDK" in content_headers
        # The header should include version and dynamic method name from get_method_name()
        header_value = content_headers["X-Galileo-SDK"]
        assert header_value.startswith(f"galileo-python/{get_package_version()}")
        # Should contain the method name (e.g., "_make_async_request@galileo.traces")
        assert "@galileo.traces" in header_value


class TestIngestTracesExtraHeaders:
    """Test that IngestTraces applies customer-supplied extra headers (e.g. IBM APIC)."""

    def test_extra_headers_included(self) -> None:
        # Given/When: an IngestTraces client configured with extra headers
        client = IngestTraces(
            project_id="p",
            base_url="http://ingest/",
            api_key="KEY",
            extra_headers={"ibm_client_id": "my_client_id", "ibm_client_secret": "my_client_secret"},
        )

        # Then: the extra headers are present alongside Galileo's own headers
        assert client._headers["ibm_client_id"] == "my_client_id"
        assert client._headers["ibm_client_secret"] == "my_client_secret"
        assert client._headers["Galileo-API-Key"] == "KEY"
        assert client._headers["Content-Type"] == "application/json"

    def test_extra_headers_cannot_override_galileo_headers(self) -> None:
        # Given/When: extra headers that collide with Galileo's own headers
        client = IngestTraces(
            project_id="p",
            base_url="http://ingest/",
            api_key="KEY",
            extra_headers={"Galileo-API-Key": "evil", "Content-Type": "text/evil"},
        )

        # Then: Galileo's own headers win on collision
        assert client._headers["Galileo-API-Key"] == "KEY"
        assert client._headers["Content-Type"] == "application/json"

    def test_no_extra_headers_by_default(self) -> None:
        # Given/When: an IngestTraces client with no extra headers
        client = IngestTraces(project_id="p", base_url="http://ingest/", api_key="KEY")

        # Then: only Galileo's own headers are present
        assert "ibm_client_id" not in client._headers
        assert client._headers["Galileo-API-Key"] == "KEY"
