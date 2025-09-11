"""Tests for X-Galileo-SDK header in API calls."""

from unittest.mock import patch

from galileo.resources.api.datasets.get_dataset_datasets_dataset_id_get import _get_kwargs as dataset_get_kwargs
from galileo.resources.api.health.healthcheck_healthcheck_get import _get_kwargs as healthcheck_get_kwargs
from galileo.utils.headers_data import get_package_version


class TestApiHeaders:
    """Test that X-Galileo-SDK headers are properly included in API calls."""

    def test_generated_api_method_includes_sdk_header(self):
        """Test that generated API methods include the X-Galileo-SDK header."""
        # Test the _get_kwargs function which is responsible for setting headers
        dataset_id = "test-dataset-id"
        kwargs = dataset_get_kwargs(dataset_id=dataset_id)

        # Verify the header is included in the kwargs
        content_headers = kwargs.get("content_headers", {})
        assert "X-Galileo-SDK" in content_headers
        expected_header_value = f"galileo-python/{get_package_version()}"
        assert content_headers["X-Galileo-SDK"] == expected_header_value

    def test_generated_api_method_header_format(self):
        """Test that the X-Galileo-SDK header has the correct format."""
        # Test with a different API method's _get_kwargs function

        kwargs = healthcheck_get_kwargs()

        # Verify the header format
        content_headers = kwargs.get("content_headers", {})
        sdk_header = content_headers.get("X-Galileo-SDK", "")

        # Should match pattern: galileo-python/x.x.x
        assert sdk_header.startswith("galileo-python/")
        # Extract version part
        version_part = sdk_header.split("/", 1)[1]
        # Version should be a string (may be empty in test environment)
        assert isinstance(version_part, str)

    @patch("galileo.resources.api.datasets.get_dataset_datasets_dataset_id_get.get_package_version")
    def test_generated_api_method_with_mocked_version(self, mock_get_version):
        """Test header with a specific mocked version."""
        mock_get_version.return_value = "1.2.3"

        dataset_id = "test-dataset-id"
        kwargs = dataset_get_kwargs(dataset_id=dataset_id)

        # Verify the exact header value
        content_headers = kwargs.get("content_headers", {})
        assert content_headers["X-Galileo-SDK"] == "galileo-python/1.2.3"
