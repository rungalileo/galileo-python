import os
import re
import uuid
from unittest.mock import Mock, patch
from urllib.parse import urljoin

import pytest
from pydantic import SecretStr

from galileo.otel import INSTALL_ERR_MSG, OTEL_AVAILABLE, GalileoOTLPExporter, GalileoSpanProcessor


class TestGalileoOTLPExporter:
    """Test suite for GalileoOTLPExporter class."""

    @pytest.fixture
    def clear_env_vars(self):
        """Clear relevant environment variables for clean test state."""
        env_vars = ["GALILEO_API_KEY", "GALILEO_CONSOLE_URL", "GALILEO_PROJECT", "GALILEO_LOGSTREAM"]
        original_values = {}

        for var in env_vars:
            original_values[var] = os.environ.get(var)
            if var in os.environ:
                del os.environ[var]

        yield

        # Restore original values
        for var, value in original_values.items():
            if value is not None:
                os.environ[var] = value
            elif var in os.environ:
                del os.environ[var]

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    @patch("galileo.otel.OTLPSpanExporter.__init__", return_value=None)
    @patch("galileo.otel.GalileoPythonConfig.get")
    def test_init_with_all_parameters(self, mock_config_get, mock_otlp_init, clear_env_vars):
        """Test initialization with all parameters provided."""
        project = "test-project"
        logstream = "test-logstream"
        api_key = "test-api-key"
        base_url = "https://custom.galileo.ai"

        # Mock the config
        mock_config = Mock()
        mock_config.api_url = base_url
        mock_config.api_key = SecretStr(api_key)
        mock_config_get.return_value = mock_config

        exporter = GalileoOTLPExporter(project=project, logstream=logstream, timeout=30)

        # Verify endpoint construction
        expected_endpoint = urljoin(base_url + "/", "/otel/traces")
        expected_headers = {"Galileo-API-Key": api_key, "project": project, "logstream": logstream}

        mock_otlp_init.assert_called_once_with(endpoint=expected_endpoint, headers=expected_headers, timeout=30)

        assert exporter.project == project
        assert exporter.logstream == logstream

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    @patch("galileo.otel.OTLPSpanExporter.__init__", return_value=None)
    @patch("galileo.otel.GalileoPythonConfig.get")
    def test_init_with_env_variables(self, mock_config_get, mock_otlp_init):
        """Test initialization using environment variables and that they prevent auto-generation."""
        # Mock the config
        mock_config = Mock()
        mock_config.api_url = "https://env.galileo.ai"
        mock_config.api_key = SecretStr("env-api-key")
        mock_config_get.return_value = mock_config

        with patch.dict(
            os.environ,
            {"GALILEO_API_KEY": "env-api-key", "GALILEO_PROJECT": "env-project", "GALILEO_LOGSTREAM": "env-logstream"},
        ):
            with patch("galileo.otel.uuid.uuid4") as mock_uuid:
                exporter = GalileoOTLPExporter()

                # Verify UUID generation was not called since project provided via env var
                mock_uuid.assert_not_called()

                expected_endpoint = urljoin("https://env.galileo.ai/", "/otel/traces")
                expected_headers = {
                    "Galileo-API-Key": "env-api-key",
                    "project": "env-project",
                    "logstream": "env-logstream",
                }

                mock_otlp_init.assert_called_once_with(endpoint=expected_endpoint, headers=expected_headers)

                # The instance variables should match the env values
                assert exporter.project == "env-project"
                assert exporter.logstream == "env-logstream"

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    @patch("galileo.otel.OTLPSpanExporter.__init__", return_value=None)
    @patch("galileo.otel.GalileoPythonConfig.get")
    def test_init_parameter_priority_over_env(self, mock_config_get, mock_otlp_init):
        """Test that parameters take priority over environment variables."""
        # Mock the config
        mock_config = Mock()
        mock_config.api_url = "https://config.galileo.ai"
        mock_config.api_key = SecretStr("env-key")
        mock_config_get.return_value = mock_config

        with patch.dict(
            os.environ,
            {"GALILEO_API_KEY": "env-key", "GALILEO_PROJECT": "env-project", "GALILEO_LOGSTREAM": "env-logstream"},
        ):
            GalileoOTLPExporter(project="param-project", logstream="param-logstream")

            expected_endpoint = urljoin("https://config.galileo.ai/", "/otel/traces")
            expected_headers = {
                "Galileo-API-Key": "env-key",
                "project": "param-project",
                "logstream": "param-logstream",
            }

            call_kwargs = mock_otlp_init.call_args[1]
            assert call_kwargs["endpoint"] == expected_endpoint
            assert call_kwargs["headers"] == expected_headers

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    @patch("galileo.otel.uuid.uuid4")
    @patch("galileo.otel.OTLPSpanExporter.__init__", return_value=None)
    @patch("galileo.otel.GalileoPythonConfig.get")
    def test_init_auto_generate_project(self, mock_config_get, mock_otlp_init, mock_uuid, clear_env_vars):
        """Test automatic project generation when no project is provided."""
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-9012-123456789012")

        # Mock the config
        mock_config = Mock()
        mock_config.api_url = "https://api.galileo.ai"
        mock_config.api_key = SecretStr("test-key")
        mock_config_get.return_value = mock_config

        GalileoOTLPExporter()

        expected_project = "project_12345678-1234-5678-9012-123456789012"
        call_kwargs = mock_otlp_init.call_args[1]
        assert call_kwargs["headers"]["project"] == expected_project

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    @patch("galileo.otel.OTLPSpanExporter.__init__", return_value=None)
    @patch("galileo.otel.GalileoPythonConfig.get")
    @pytest.mark.parametrize(
        "api_url,expected_endpoint",
        [
            ("https://api.galileo.ai", "https://api.galileo.ai/otel/traces"),
            ("https://api.galileo.ai/", "https://api.galileo.ai/otel/traces"),
            ("http://localhost:8080", "http://localhost:8080/otel/traces"),
            ("http://localhost:8080/", "http://localhost:8080/otel/traces"),
        ],
    )
    def test_url_construction_and_normalization(
        self, mock_config_get, mock_otlp_init, api_url, expected_endpoint, clear_env_vars
    ):
        """Test URL construction with various edge cases."""
        # Mock the config
        mock_config = Mock()
        mock_config.api_url = api_url
        mock_config.api_key = SecretStr("test-key")
        mock_config_get.return_value = mock_config

        GalileoOTLPExporter()

        call_kwargs = mock_otlp_init.call_args[1]
        assert call_kwargs["endpoint"] == expected_endpoint

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    @patch("galileo.otel.GalileoPythonConfig.get")
    def test_init_missing_api_key_raises_error(self, mock_config_get, clear_env_vars):
        """Test that missing API key raises ValueError."""
        # Mock the config
        mock_config = Mock()
        mock_config.api_url = "https://api.galileo.ai"
        mock_config.api_key = None
        mock_config_get.return_value = mock_config

        with pytest.raises(ValueError, match="API key is required"):
            GalileoOTLPExporter()


class TestGalileoSpanProcessor:
    """Test suite for GalileoSpanProcessor class."""

    @pytest.fixture
    def mock_processor_setup(self):
        """Set up common mocks for span processor tests."""
        with (
            patch("galileo.otel.BatchSpanProcessor") as mock_batch_processor,
            patch("galileo.otel.GalileoOTLPExporter") as mock_exporter_class,
        ):
            mock_exporter_instance = Mock()
            mock_processor_instance = Mock()
            mock_exporter_class.return_value = mock_exporter_instance
            mock_batch_processor.return_value = mock_processor_instance

            yield {
                "mock_exporter_class": mock_exporter_class,
                "mock_processor_class": mock_batch_processor,
                "mock_exporter_instance": mock_exporter_instance,
                "mock_processor_instance": mock_processor_instance,
            }

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_init_with_default_processor(self, mock_processor_setup):
        """Test initialization with default BatchSpanProcessor."""
        mocks = mock_processor_setup

        processor = GalileoSpanProcessor(project="test-project", logstream="test-logstream")

        # Verify exporter was created with correct parameters
        mocks["mock_exporter_class"].assert_called_once_with(project="test-project", logstream="test-logstream")

        # Verify BatchSpanProcessor was created with the exporter
        mocks["mock_processor_class"].assert_called_once_with(mocks["mock_exporter_instance"])

        # Verify properties
        assert processor.exporter == mocks["mock_exporter_instance"]
        assert processor.processor == mocks["mock_processor_instance"]

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    @patch("galileo.otel.GalileoOTLPExporter")
    def test_init_with_custom_processor(self, mock_exporter_class):
        """Test initialization with custom span processor class."""
        mock_exporter_instance = Mock()
        mock_exporter_class.return_value = mock_exporter_instance

        # Create a mock custom processor class
        mock_custom_processor_class = Mock()
        mock_custom_processor_instance = Mock()
        mock_custom_processor_class.return_value = mock_custom_processor_instance

        processor = GalileoSpanProcessor(project="test-project", SpanProcessor=mock_custom_processor_class)

        # Verify custom processor was used
        mock_custom_processor_class.assert_called_once_with(mock_exporter_instance)
        assert processor.processor == mock_custom_processor_instance

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_on_start_delegates_to_processor(self, mock_processor_setup):
        """Test that on_start delegates to the underlying processor."""
        mocks = mock_processor_setup
        processor = GalileoSpanProcessor(project="test")

        mock_span = Mock()
        mock_context = Mock()
        processor.on_start(mock_span, mock_context)

        mocks["mock_processor_instance"].on_start.assert_called_once_with(mock_span, mock_context)

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_on_end_delegates_to_processor(self, mock_processor_setup):
        """Test that on_end delegates to the underlying processor."""
        mocks = mock_processor_setup
        processor = GalileoSpanProcessor(project="test")

        mock_span = Mock()
        processor.on_end(mock_span)

        mocks["mock_processor_instance"].on_end.assert_called_once_with(mock_span)

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_shutdown_delegates_to_processor(self, mock_processor_setup):
        """Test that shutdown delegates to the underlying processor."""
        mocks = mock_processor_setup
        processor = GalileoSpanProcessor(project="test")

        processor.shutdown()

        mocks["mock_processor_instance"].shutdown.assert_called_once()

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_force_flush_delegates_to_processor(self, mock_processor_setup):
        """Test that force_flush delegates to the underlying processor."""
        mocks = mock_processor_setup
        mocks["mock_processor_instance"].force_flush.return_value = True
        processor = GalileoSpanProcessor(project="test")

        result = processor.force_flush(30000)

        mocks["mock_processor_instance"].force_flush.assert_called_once_with(30000)
        assert result is True

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_force_flush_default_timeout(self, mock_processor_setup):
        """Test that force_flush uses default timeout when not specified."""
        mocks = mock_processor_setup
        processor = GalileoSpanProcessor(project="test")

        processor.force_flush()

        mocks["mock_processor_instance"].force_flush.assert_called_once_with(40000)

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_init_passes_all_parameters_to_exporter(self, mock_processor_setup):
        """Test that all initialization parameters are passed to the exporter."""
        mocks = mock_processor_setup

        GalileoSpanProcessor(project="test-project", logstream="test-logstream")

        mocks["mock_exporter_class"].assert_called_once_with(project="test-project", logstream="test-logstream")


class TestOTelUnavailable:
    """Test behavior when OpenTelemetry is not available."""

    @patch("galileo.otel.OTEL_AVAILABLE", False)
    def test_galileo_span_processor_raises_import_error_when_otel_unavailable(self):
        """Test that GalileoSpanProcessor raises ImportError when OpenTelemetry is not available."""
        with pytest.raises(ImportError, match=re.escape(INSTALL_ERR_MSG)):
            GalileoSpanProcessor(project="test")

    def test_stub_classes_raise_import_error(self):
        """Test that stub classes raise ImportError when instantiated."""
        # This test only applies when OTEL is not available, but since we're testing
        # with OTEL available, we'll skip this test
        if OTEL_AVAILABLE:
            pytest.skip("OpenTelemetry is available, stub classes are not used")


class TestOTelIntegration:
    """Integration tests for OpenTelemetry functionality."""

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    @patch("galileo.otel.BatchSpanProcessor")
    @patch("galileo.otel.OTLPSpanExporter.__init__", return_value=None)
    @patch("galileo.otel.GalileoPythonConfig.get")
    def test_exporter_and_processor_integration(self, mock_config_get, mock_otlp_init, mock_batch_processor):
        """Test that GalileoSpanProcessor correctly integrates with GalileoOTLPExporter."""
        mock_batch_instance = Mock()
        mock_batch_processor.return_value = mock_batch_instance

        # Mock the config
        mock_config = Mock()
        mock_config.api_url = "https://api.galileo.ai"
        mock_config.api_key = SecretStr("test-key")
        mock_config_get.return_value = mock_config

        processor = GalileoSpanProcessor(project="integration-test", logstream="integration-logstream")

        # Verify the exporter was created and passed to the processor
        assert mock_otlp_init.called
        mock_batch_processor.assert_called_once()

        # Verify the processor has access to both components
        assert hasattr(processor, "exporter")
        assert hasattr(processor, "processor")
        assert processor.processor == mock_batch_instance
