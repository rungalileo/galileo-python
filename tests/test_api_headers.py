"""Tests for X-Galileo-SDK header in API calls."""

from unittest.mock import patch

from galileo.__future__ import Project
from galileo.projects import list_projects
from galileo.resources.api.datasets.get_dataset_datasets_dataset_id_get import _get_kwargs as dataset_get_kwargs
from galileo.resources.api.health.healthcheck_healthcheck_get import _get_kwargs as healthcheck_get_kwargs
from galileo.resources.api.projects import get_all_projects_projects_all_get
from galileo.utils.headers_data import get_package_version


class TestApiHeaders:
    """Test that X-Galileo-SDK headers are properly included in API calls."""

    def test_generated_api_method_includes_sdk_header(self) -> None:
        """Test that generated API methods include the X-Galileo-SDK header with method name."""
        # Test the _get_kwargs function which is responsible for setting headers
        dataset_id = "test-dataset-id"
        kwargs = dataset_get_kwargs(dataset_id=dataset_id)

        # Verify the header is included in the kwargs
        content_headers = kwargs.get("content_headers", {})
        assert "X-Galileo-SDK" in content_headers
        header = content_headers["X-Galileo-SDK"]
        # Should include version and method name
        assert header.startswith(f"galileo-python/{get_package_version()}")
        # Direct call to resource should include the resource method name
        assert "@galileo.resources.api.datasets" in header

    def test_generated_api_method_header_format(self) -> None:
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

    @patch("galileo.utils.headers_data.get_package_version")
    def test_generated_api_method_with_mocked_version(self, mock_get_version) -> None:
        """Test header includes mocked version and method name."""
        mock_get_version.return_value = "1.2.3"

        dataset_id = "test-dataset-id"
        kwargs = dataset_get_kwargs(dataset_id=dataset_id)

        # Verify the header includes both version and method
        content_headers = kwargs.get("content_headers", {})
        header = content_headers["X-Galileo-SDK"]
        assert header.startswith("galileo-python/1.2.3")
        # Should also include the method name
        assert "@galileo.resources.api.datasets" in header

    def test_different_entry_points_produce_different_headers(self) -> None:
        """Test that Project.list() and list_projects() produce different headers using real calls."""
        captured_headers = []

        # Store original function before patching
        original_get_kwargs = get_all_projects_projects_all_get._get_kwargs

        # Configure a wrapper to capture headers
        def capture_and_call(*args, **kwargs):
            result = original_get_kwargs(*args, **kwargs)
            if "content_headers" in result and "X-Galileo-SDK" in result["content_headers"]:
                captured_headers.append(result["content_headers"]["X-Galileo-SDK"])
            return result

        # Apply the patch as a context manager
        with patch.object(
            get_all_projects_projects_all_get, "_get_kwargs", side_effect=capture_and_call
        ) as mock_get_kwargs:
            # Test 1: galileo.__future__.Project.list()
            try:
                Project.list()
            except Exception:
                pass  # API call might fail in test, we only care about headers

            # Test 2: galileo.projects.list_projects()
            try:
                list_projects()
            except Exception:
                pass  # API call might fail in test, we only care about headers

            # Verify _get_kwargs was called at least twice
            assert mock_get_kwargs.call_count >= 2, f"Expected at least 2 calls, got {mock_get_kwargs.call_count}"

        # Verify we captured different headers
        assert len(captured_headers) >= 2, f"Should have captured at least 2 headers, got {len(captured_headers)}"
        header1 = captured_headers[0]
        header2 = captured_headers[-1]  # Get last one in case there were more calls

        # Both should have the SDK name and version
        assert header1.startswith("galileo-python/")
        assert header2.startswith("galileo-python/")

        # But they should have different method names
        assert "list@galileo.__future__.project" in header1.lower()
        assert "list_projects@galileo.projects" in header2

        # Headers should be different
        assert header1 != header2, f"Headers should be different: '{header1}' vs '{header2}'"
