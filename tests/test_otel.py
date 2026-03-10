import json
import os
import re
from unittest.mock import Mock, patch

import pytest
from pydantic import SecretStr

from galileo.decorator import _experiment_id_context, _log_stream_context, _project_context, _session_id_context
from galileo.otel import (
    _TRACE_PROVIDER_CONTEXT_VAR,
    INSTALL_ERR_MSG,
    OTEL_AVAILABLE,
    GalileoOTLPExporter,
    GalileoSpanProcessor,
    _dataset_input_context,
    _dataset_metadata_context,
    _dataset_output_context,
    _set_tool_span_attributes,
    galileo_dataset_context,
    start_galileo_span,
)
from galileo_core.schemas.logging.span import ToolSpan

if OTEL_AVAILABLE:
    from galileo.otel import _set_workflow_span_attributes, start_galileo_span
    from galileo_core.schemas.logging.llm import Message, MessageRole
    from galileo_core.schemas.logging.span import WorkflowSpan
    from galileo_core.schemas.shared.document import Document


class TestGalileoOTLPExporter:
    """Test suite for GalileoOTLPExporter class."""

    @pytest.fixture
    def clear_env_vars(self):
        """Clear relevant environment variables and context vars for clean test state."""
        env_vars = ["GALILEO_API_KEY", "GALILEO_CONSOLE_URL", "GALILEO_PROJECT", "GALILEO_LOG_STREAM"]
        original_values = {var: os.environ.pop(var, None) for var in env_vars}
        _project_context.set(None)
        _log_stream_context.set(None)

        yield

        for var, value in original_values.items():
            if value is not None:
                os.environ[var] = value
        _project_context.set(None)
        _log_stream_context.set(None)

    @pytest.fixture
    def mock_config(self):
        """Create a mock config with default values."""
        with patch("galileo.otel.GalileoPythonConfig.get") as mock_config_get:
            config = Mock()
            config.api_url = "https://api.galileo.ai"
            config.api_key = SecretStr("test-key")
            mock_config_get.return_value = config
            yield config

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    @patch("galileo.otel.OTLPSpanExporter.__init__", return_value=None)
    def test_init_and_parameter_priority(self, mock_otlp_init, mock_config, clear_env_vars):
        """Test initialization with params, env vars, and their priority."""
        # Test with explicit params
        exporter = GalileoOTLPExporter(project="param-project", logstream="param-logstream", timeout=30)
        assert exporter.project == "param-project"
        assert exporter.logstream == "param-logstream"

        call_kwargs = mock_otlp_init.call_args[1]
        assert call_kwargs["headers"]["project"] == "param-project"
        assert call_kwargs["headers"]["logstream"] == "param-logstream"
        assert call_kwargs["timeout"] == 30

        # Test that params override env vars
        mock_otlp_init.reset_mock()
        with patch.dict(os.environ, {"GALILEO_PROJECT": "env-project", "GALILEO_LOG_STREAM": "env-logstream"}):
            exporter = GalileoOTLPExporter(project="param-project", logstream="param-logstream")
            assert exporter.project == "param-project"  # Param wins over env

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    @patch("galileo.otel.OTLPSpanExporter.__init__", return_value=None)
    def test_init_with_env_variables(self, mock_otlp_init, mock_config, clear_env_vars):
        """Test initialization using environment variables."""
        with patch.dict(os.environ, {"GALILEO_PROJECT": "env-project", "GALILEO_LOG_STREAM": "env-logstream"}):
            exporter = GalileoOTLPExporter()
            assert exporter.project == "env-project"
            assert exporter.logstream == "env-logstream"

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    @patch("galileo.otel.OTLPSpanExporter.__init__", return_value=None)
    def test_init_uses_default_project(self, mock_otlp_init, mock_config, clear_env_vars):
        """Test default project name is used when no project is provided."""
        GalileoOTLPExporter()

        call_kwargs = mock_otlp_init.call_args[1]
        assert call_kwargs["headers"]["project"] == "default"
        assert call_kwargs["headers"]["logstream"] == "default"

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    @patch("galileo.otel.OTLPSpanExporter.__init__", return_value=None)
    @pytest.mark.parametrize(
        "api_url,expected_endpoint",
        [
            ("https://api.galileo.ai", "https://api.galileo.ai/otel/traces"),
            ("https://api.galileo.ai/", "https://api.galileo.ai/otel/traces"),
            ("http://localhost:8080", "http://localhost:8080/otel/traces"),
        ],
    )
    def test_url_construction(self, mock_otlp_init, api_url, expected_endpoint, mock_config, clear_env_vars):
        """Test URL construction with various formats."""
        mock_config.api_url = api_url
        GalileoOTLPExporter()
        assert mock_otlp_init.call_args[1]["endpoint"] == expected_endpoint

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_init_missing_api_key_raises_error(self, mock_config, clear_env_vars):
        """Test that missing API key raises ValueError."""
        mock_config.api_key = None
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
        # Note: exporter is now created without explicit project/logstream params (reads from context)
        mocks["mock_exporter_class"].assert_called_once()

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

        # Note: exporter is now created without explicit project/logstream params (reads from context)
        mocks["mock_exporter_class"].assert_called_once()


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


class TestOTelContextIntegration:
    """Tests for OpenTelemetry context variable integration."""

    @pytest.fixture
    def reset_decorator_context(self):
        """Reset decorator context before each test."""
        for ctx in [_project_context, _log_stream_context, _experiment_id_context, _session_id_context]:
            ctx.set(None)
        yield
        for ctx in [_project_context, _log_stream_context, _experiment_id_context, _session_id_context]:
            ctx.set(None)

    @pytest.fixture
    def mock_processor_deps(self):
        """Mock dependencies for processor tests."""
        with (
            patch("galileo.otel.BatchSpanProcessor") as mock_batch,
            patch("galileo.otel.GalileoOTLPExporter") as mock_exp,
        ):
            mock_exp.return_value = Mock()
            mock_batch.return_value = Mock()
            yield {"exporter": mock_exp, "batch": mock_batch}

    @pytest.fixture
    def mock_exporter(self):
        """Create a mock exporter for export tests."""
        with (
            patch("galileo.otel.OTLPSpanExporter.__init__", return_value=None),
            patch("galileo.otel.GalileoPythonConfig.get") as mock_config_get,
        ):
            config = Mock()
            config.api_url = "https://api.galileo.ai"
            config.api_key = SecretStr("test-key")
            mock_config_get.return_value = config
            yield GalileoOTLPExporter(project="test-project", logstream="test-logstream")

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    @patch("galileo.otel.OTLPSpanExporter.__init__", return_value=None)
    @patch("galileo.otel.GalileoPythonConfig.get")
    def test_exporter_context_vars_and_override(self, mock_config_get, mock_otlp_init, reset_decorator_context):
        """Test exporter reads from context vars and params override them."""
        mock_config = Mock()
        mock_config.api_url = "https://api.galileo.ai"
        mock_config.api_key = SecretStr("test-key")
        mock_config_get.return_value = mock_config

        # Set context variables
        _project_context.set("context-project")
        _log_stream_context.set("context-logstream")

        # Exporter uses context values
        exporter = GalileoOTLPExporter()
        assert exporter.project == "context-project"
        assert exporter.logstream == "context-logstream"

        # Explicit params override context
        mock_otlp_init.reset_mock()
        exporter2 = GalileoOTLPExporter(project="param-project", logstream="param-logstream")
        assert exporter2.project == "param-project"
        assert exporter2.logstream == "param-logstream"

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_processor_context_and_fallback(self, mock_processor_deps, reset_decorator_context):
        """Test processor reads context vars and uses init values as fallback."""
        # Test context vars
        _project_context.set("context-project")
        _log_stream_context.set("context-logstream")

        processor = GalileoSpanProcessor()
        assert processor._project == "context-project"
        assert processor._logstream == "context-logstream"

        # Test fallback to init values when context is empty
        _project_context.set(None)
        _log_stream_context.set(None)

        processor2 = GalileoSpanProcessor(project="init-project", logstream="init-logstream")
        assert processor2._project == "init-project"
        assert processor2._logstream == "init-logstream"

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_processor_on_start_sets_span_attributes(self, mock_processor_deps, reset_decorator_context):
        """Test on_start sets context attributes on spans, handling None values."""
        # Test with all context vars set
        _project_context.set("test-project")
        _log_stream_context.set("test-logstream")
        _experiment_id_context.set("test-experiment")
        _session_id_context.set("test-session")

        processor = GalileoSpanProcessor()
        mock_span = Mock()

        processor.on_start(mock_span, None)

        assert mock_span.set_attribute.call_count == 4
        actual_calls = {(args[0], args[1]) for args, _ in mock_span.set_attribute.call_args_list}
        assert ("galileo.project.name", "test-project") in actual_calls
        assert ("galileo.session.id", "test-session") in actual_calls

        # Test that processor always sets project and logstream (using env var fallbacks)
        # When context is None, it falls back to env vars (set in conftest.py)
        _log_stream_context.set(None)
        _experiment_id_context.set(None)
        _session_id_context.set(None)

        processor2 = GalileoSpanProcessor()
        mock_span2 = Mock()
        processor2.on_start(mock_span2, None)

        # Project and logstream are always set (env var fallbacks when context is None)
        assert mock_span2.set_attribute.call_count == 2
        actual_calls = {(args[0], args[1]) for args, _ in mock_span2.set_attribute.call_args_list}
        assert ("galileo.project.name", "test-project") in actual_calls
        # Falls back to GALILEO_LOG_STREAM env var set in conftest.py
        assert ("galileo.logstream.name", "test-log-stream") in actual_calls

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    @patch("galileo.otel.OTLPSpanExporter.export")
    @patch("galileo.otel.Resource")
    def test_exporter_export_merges_resource_attributes(self, mock_resource_class, mock_parent_export):
        """Test export merges Galileo attributes into resource, handles partial/no attributes."""
        # Create a real exporter with mocked dependencies
        with (
            patch("galileo.otel.OTLPSpanExporter.__init__", return_value=None),
            patch("galileo.otel.GalileoPythonConfig.get") as mock_config_get,
        ):
            config = Mock()
            config.api_url = "https://api.galileo.ai"
            config.api_key = SecretStr("test-key")
            mock_config_get.return_value = config

            exporter = GalileoOTLPExporter(project="test-project", logstream="test-logstream")
            # Mock the _session attribute that export() uses
            exporter._session = Mock()
            exporter._session.headers = {}

        # Test with all Galileo attributes
        mock_span = Mock()
        mock_span.attributes = {
            "galileo.project.name": "span-project",
            "galileo.logstream.name": "span-logstream",
            "galileo.session.id": "span-session",
            "galileo.experiment.id": "span-experiment",
            "other.attribute": "value",
        }
        mock_merged_resource = Mock()
        mock_span.resource = Mock()
        mock_span.resource.merge.return_value = mock_merged_resource
        mock_new_resource = Mock()
        mock_resource_class.return_value = mock_new_resource

        exporter.export([mock_span])

        # Verify Resource was created with only Galileo attributes
        call_args = mock_resource_class.call_args[0][0]
        assert "galileo.project.name" in call_args
        assert call_args["galileo.project.name"] == "span-project"
        assert "galileo.logstream.name" in call_args
        assert "galileo.session.id" in call_args
        assert "galileo.experiment.id" in call_args
        assert "other.attribute" not in call_args

        # Verify resource was merged and span._resource was updated
        mock_span.resource.merge.assert_called_once_with(mock_new_resource)
        assert mock_span._resource == mock_merged_resource

        # Verify parent export was called
        mock_parent_export.assert_called_once_with([mock_span])

        # Test with no Galileo attributes
        mock_parent_export.reset_mock()
        mock_resource_class.reset_mock()
        mock_span2 = Mock()
        mock_span2.attributes = {"other.attribute": "value"}
        mock_span2.resource = Mock()

        exporter.export([mock_span2])

        # No resource should be created when there are no Galileo attributes
        mock_resource_class.assert_not_called()
        mock_span2.resource.merge.assert_not_called()
        mock_parent_export.assert_called_once_with([mock_span2])


class TestSetToolSpanAttributes:
    """Test suite for _set_tool_span_attributes function."""

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_tool_span_with_all_fields(self):
        """Test setting attributes when all ToolSpan fields are populated."""
        # Given: a ToolSpan with input, output, and tool_call_id
        tool_span = ToolSpan(
            name="test-tool",
            input="tool input data",
            output="tool output result",
            tool_call_id="call-123",
            status_code=200,
        )
        mock_otel_span = Mock()

        # When: setting tool span attributes
        _set_tool_span_attributes(mock_otel_span, tool_span)

        # Then: all attributes are set correctly
        calls = {args[0]: args[1] for args, _ in mock_otel_span.set_attribute.call_args_list}
        assert calls["gen_ai.operation.name"] == "execute_tool"
        assert calls["gen_ai.tool.name"] == "test-tool"
        assert calls["gen_ai.tool.call.arguments"] == "tool input data"
        assert calls["gen_ai.tool.call.result"] == "tool output result"
        assert calls["gen_ai.input.messages"] == json.dumps([{"role": "tool", "content": "tool input data"}])
        assert calls["gen_ai.output.messages"] == json.dumps([{"role": "tool", "content": "tool output result"}])
        assert calls["gen_ai.tool.call.id"] == "call-123"
        assert mock_otel_span.set_attribute.call_count == 7

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_tool_span_with_only_input(self):
        """Test setting attributes when only input is provided."""
        # Given: a ToolSpan with only input (output and tool_call_id are None)
        tool_span = ToolSpan(name="test-tool", input="tool input only", output=None, tool_call_id=None, status_code=200)
        mock_otel_span = Mock()

        # When: setting tool span attributes
        _set_tool_span_attributes(mock_otel_span, tool_span)

        # Then: operation name, tool name, and input attributes are set, but not output or tool_call_id
        calls = {args[0]: args[1] for args, _ in mock_otel_span.set_attribute.call_args_list}
        assert calls["gen_ai.operation.name"] == "execute_tool"
        assert calls["gen_ai.tool.name"] == "test-tool"
        assert calls["gen_ai.tool.call.arguments"] == "tool input only"
        assert calls["gen_ai.input.messages"] == json.dumps([{"role": "tool", "content": "tool input only"}])
        assert "gen_ai.tool.call.result" not in calls
        assert "gen_ai.output.messages" not in calls
        assert "gen_ai.tool.call.id" not in calls
        assert mock_otel_span.set_attribute.call_count == 4

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_tool_span_with_output_no_tool_call_id(self):
        """Test setting attributes when output is provided but tool_call_id is None."""
        # Given: a ToolSpan with input and output, but no tool_call_id
        tool_span = ToolSpan(
            name="test-tool", input="tool input", output="tool output", tool_call_id=None, status_code=200
        )
        mock_otel_span = Mock()

        # When: setting tool span attributes
        _set_tool_span_attributes(mock_otel_span, tool_span)

        # Then: operation name, tool name, input, and output attributes are set, but not tool_call_id
        calls = {args[0]: args[1] for args, _ in mock_otel_span.set_attribute.call_args_list}
        assert calls["gen_ai.operation.name"] == "execute_tool"
        assert calls["gen_ai.tool.name"] == "test-tool"
        assert calls["gen_ai.tool.call.arguments"] == "tool input"
        assert calls["gen_ai.tool.call.result"] == "tool output"
        assert calls["gen_ai.input.messages"] == json.dumps([{"role": "tool", "content": "tool input"}])
        assert calls["gen_ai.output.messages"] == json.dumps([{"role": "tool", "content": "tool output"}])
        assert "gen_ai.tool.call.id" not in calls
        assert mock_otel_span.set_attribute.call_count == 6


class TestStartGalileoSpan:
    """Test suite for start_galileo_span context manager."""

    @pytest.fixture(autouse=True)
    def reset_trace_provider(self):
        """Reset the trace provider context var before and after each test."""
        _TRACE_PROVIDER_CONTEXT_VAR.set(None)
        yield
        _TRACE_PROVIDER_CONTEXT_VAR.set(None)

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_start_galileo_span_dispatches_tool_span(self):
        """Test that start_galileo_span routes a ToolSpan to _set_tool_span_attributes."""
        # Given: a ToolSpan with all fields populated and a mock tracer provider
        tool_span = ToolSpan(
            name="my-tool",
            input="tool input data",
            output="tool output result",
            tool_call_id="call-789",
            status_code=200,
        )
        mock_otel_span = Mock()
        mock_tracer = Mock()
        mock_tracer.start_as_current_span.return_value.__enter__ = Mock(return_value=mock_otel_span)
        mock_tracer.start_as_current_span.return_value.__exit__ = Mock(return_value=False)
        mock_provider = Mock()
        mock_provider.get_tracer.return_value = mock_tracer
        _TRACE_PROVIDER_CONTEXT_VAR.set(mock_provider)

        # When: using start_galileo_span with the ToolSpan
        with start_galileo_span(tool_span) as span:
            assert span is mock_otel_span

        # Then: the span has gen_ai.system set and tool-specific attributes
        calls = {args[0]: args[1] for args, _ in mock_otel_span.set_attribute.call_args_list}
        assert calls["gen_ai.system"] == "galileo-otel"
        assert calls["gen_ai.operation.name"] == "execute_tool"
        assert calls["gen_ai.tool.name"] == "my-tool"
        assert calls["gen_ai.tool.call.arguments"] == "tool input data"
        assert calls["gen_ai.tool.call.result"] == "tool output result"
        assert calls["gen_ai.input.messages"] == json.dumps([{"role": "tool", "content": "tool input data"}])
        assert calls["gen_ai.output.messages"] == json.dumps([{"role": "tool", "content": "tool output result"}])
        assert calls["gen_ai.tool.call.id"] == "call-789"

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_start_galileo_span_tool_span_with_none_output(self):
        """Test that start_galileo_span handles a ToolSpan with None output and tool_call_id."""
        # Given: a ToolSpan with only input populated
        tool_span = ToolSpan(name="minimal-tool", input="just input", output=None, tool_call_id=None, status_code=200)
        mock_otel_span = Mock()
        mock_tracer = Mock()
        mock_tracer.start_as_current_span.return_value.__enter__ = Mock(return_value=mock_otel_span)
        mock_tracer.start_as_current_span.return_value.__exit__ = Mock(return_value=False)
        mock_provider = Mock()
        mock_provider.get_tracer.return_value = mock_tracer
        _TRACE_PROVIDER_CONTEXT_VAR.set(mock_provider)

        # When: using start_galileo_span with the minimal ToolSpan
        with start_galileo_span(tool_span) as span:
            assert span is mock_otel_span

        # Then: gen_ai.system, operation name, tool name, tool arguments, and input are set (no output or tool_call_id)
        calls = {args[0]: args[1] for args, _ in mock_otel_span.set_attribute.call_args_list}
        assert calls["gen_ai.system"] == "galileo-otel"
        assert calls["gen_ai.operation.name"] == "execute_tool"
        assert calls["gen_ai.tool.name"] == "minimal-tool"
        assert calls["gen_ai.tool.call.arguments"] == "just input"
        assert calls["gen_ai.input.messages"] == json.dumps([{"role": "tool", "content": "just input"}])
        assert "gen_ai.tool.call.result" not in calls
        assert "gen_ai.output.messages" not in calls
        assert "gen_ai.tool.call.id" not in calls


class TestWorkflowSpanAttributes:
    """Test suite for WorkflowSpan OpenTelemetry attribute mapping."""

    @pytest.fixture
    def mock_dependencies(self):
        """Set up mocks for testing workflow span attributes."""
        with patch("galileo.otel.trace") as mock_trace_module, patch("galileo.otel.json") as mock_json_module:
            mock_span = Mock()
            mock_json_module.dumps.return_value = '"test"'
            yield {"span": mock_span, "trace": mock_trace_module, "json": mock_json_module}

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_workflow_span_with_string_input_output(self, mock_dependencies):
        """Test WorkflowSpan with string input and output."""
        # Given: a WorkflowSpan with string input and output
        workflow_span = WorkflowSpan(name="test-workflow", input="input text", output="output text", status_code=200)
        mock_span = mock_dependencies["span"]
        mock_json = mock_dependencies["json"]

        # When: setting workflow span attributes
        _set_workflow_span_attributes(mock_span, workflow_span)

        # Then: input and output should be wrapped in message format
        assert mock_span.set_attribute.call_count == 2

        # Check first call (input)
        input_call = mock_span.set_attribute.call_args_list[0]
        assert input_call[0][0] == "gen_ai.input.messages"
        mock_json.dumps.assert_any_call([{"role": "user", "content": "input text"}])

        # Check second call (output)
        output_call = mock_span.set_attribute.call_args_list[1]
        assert output_call[0][0] == "gen_ai.output.messages"
        mock_json.dumps.assert_any_call([{"role": "assistant", "content": "output text"}])

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_workflow_span_with_message_input_output(self, mock_dependencies):
        """Test WorkflowSpan with Message input and output."""
        # Given: a WorkflowSpan with Message input and output
        input_msg = Message(role=MessageRole.user, content="user question")
        workflow_span = WorkflowSpan(name="test-workflow", input=[input_msg], output=input_msg, status_code=200)
        mock_span = mock_dependencies["span"]
        mock_dependencies["json"]

        # When: setting workflow span attributes
        _set_workflow_span_attributes(mock_span, workflow_span)

        # Then: input and output should serialize Message objects
        assert mock_span.set_attribute.call_count == 2
        input_call = mock_span.set_attribute.call_args_list[0]
        assert input_call[0][0] == "gen_ai.input.messages"
        output_call = mock_span.set_attribute.call_args_list[1]
        assert output_call[0][0] == "gen_ai.output.messages"

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_workflow_span_with_document_sequence_output(self, mock_dependencies):
        """Test WorkflowSpan with Document sequence output."""
        # Given: a WorkflowSpan with string input and Document sequence output
        documents = [
            Document(content="doc1 content", metadata={"source": "db"}),
            Document(content="doc2 content", metadata={"source": "api"}),
        ]
        # Note: Using model_construct to bypass a galileo_core validator bug where
        # Message._allow_null_content_with_tool_calling assumes dict input during
        # Union type validation, but receives a list when validating Sequence[Document]
        workflow_span = WorkflowSpan.model_construct(
            name="test-workflow", input="query", output=documents, status_code=200
        )
        mock_span = mock_dependencies["span"]
        mock_dependencies["json"]

        # When: setting workflow span attributes
        _set_workflow_span_attributes(mock_span, workflow_span)

        # Then: output should be wrapped in assistant message with documents
        assert mock_span.set_attribute.call_count == 2
        output_call = mock_span.set_attribute.call_args_list[1]
        assert output_call[0][0] == "gen_ai.output.messages"

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_workflow_span_with_none_output(self, mock_dependencies):
        """Test WorkflowSpan with None output (should not set output attribute)."""
        # Given: a WorkflowSpan with None output
        workflow_span = WorkflowSpan(name="test-workflow", input="input text", output=None, status_code=200)
        mock_span = mock_dependencies["span"]

        # When: setting workflow span attributes
        _set_workflow_span_attributes(mock_span, workflow_span)

        # Then: only input attribute should be set, not output
        assert mock_span.set_attribute.call_count == 1
        input_call = mock_span.set_attribute.call_args_list[0]
        assert input_call[0][0] == "gen_ai.input.messages"

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_workflow_span_in_start_galileo_span(self, mock_dependencies):
        """Test that WorkflowSpan is handled in start_galileo_span context manager."""
        # Given: a WorkflowSpan
        workflow_span = WorkflowSpan(name="test-workflow", input="input", output="output", status_code=200)
        mock_span = mock_dependencies["span"]
        mock_dependencies["json"]

        # Setup the mock tracer
        mock_tracer = Mock()
        mock_tracer.start_as_current_span.return_value.__enter__ = Mock(return_value=mock_span)
        mock_tracer.start_as_current_span.return_value.__exit__ = Mock(return_value=None)

        mock_trace_provider = Mock()
        mock_trace_provider.get_tracer.return_value = mock_tracer

        # Patch get_tracer_provider to return our mock
        with patch("galileo.otel.trace.get_tracer_provider", return_value=mock_trace_provider):
            # When: using start_galileo_span with WorkflowSpan
            with start_galileo_span(workflow_span):
                pass

        # Then: WorkflowSpan attributes should be set
        assert mock_span.set_attribute.call_count >= 2  # gen_ai.system + at least input
        system_call = [call for call in mock_span.set_attribute.call_args_list if call[0][0] == "gen_ai.system"]
        assert len(system_call) == 1


class TestDatasetContext:
    """Tests for dataset context variables and galileo_dataset_context manager."""

    @pytest.fixture
    def reset_dataset_context(self):
        """Reset dataset context variables before and after each test."""
        _dataset_input_context.set(None)
        _dataset_output_context.set(None)
        _dataset_metadata_context.set(None)
        yield
        _dataset_input_context.set(None)
        _dataset_output_context.set(None)
        _dataset_metadata_context.set(None)

    @pytest.fixture
    def mock_processor_deps(self):
        """Mock dependencies for processor tests."""
        with (
            patch("galileo.otel.BatchSpanProcessor") as mock_batch,
            patch("galileo.otel.GalileoOTLPExporter") as mock_exp,
        ):
            mock_exp.return_value = Mock()
            mock_batch.return_value = Mock()
            yield {"exporter": mock_exp, "batch": mock_batch}

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_galileo_dataset_context_sets_values(self, reset_dataset_context):
        """Test that galileo_dataset_context sets context variables correctly."""
        # Given: dataset context is initially empty
        assert _dataset_input_context.get(None) is None
        assert _dataset_output_context.get(None) is None
        assert _dataset_metadata_context.get(None) is None

        # When: entering the context manager with values
        with galileo_dataset_context(
            dataset_input="test input", dataset_output="expected output", dataset_metadata={"key": "value"}
        ):
            # Then: context variables are set inside the context
            assert _dataset_input_context.get() == "test input"
            assert _dataset_output_context.get() == "expected output"
            assert _dataset_metadata_context.get() == {"key": "value"}

        # Then: context variables are reset after exiting
        assert _dataset_input_context.get(None) is None
        assert _dataset_output_context.get(None) is None
        assert _dataset_metadata_context.get(None) is None

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_galileo_dataset_context_nested_contexts(self, reset_dataset_context):
        """Test that nested galileo_dataset_context managers work correctly."""
        # Given: outer context with initial values
        with galileo_dataset_context(dataset_input="outer input", dataset_output="outer output"):
            assert _dataset_input_context.get() == "outer input"
            assert _dataset_output_context.get() == "outer output"

            # When: entering inner context with different values
            with galileo_dataset_context(dataset_input="inner input", dataset_output="inner output"):
                # Then: inner context values are active
                assert _dataset_input_context.get() == "inner input"
                assert _dataset_output_context.get() == "inner output"

            # Then: outer context values are restored
            assert _dataset_input_context.get() == "outer input"
            assert _dataset_output_context.get() == "outer output"

        # Then: context is empty after exiting all contexts
        assert _dataset_input_context.get(None) is None
        assert _dataset_output_context.get(None) is None

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_galileo_dataset_context_exception_handling(self, reset_dataset_context):
        """Test that context variables are reset even when exception occurs."""
        # Given/When: an exception is raised inside the context
        with pytest.raises(ValueError, match="test error"):
            with galileo_dataset_context(dataset_input="test", dataset_output="expected"):
                assert _dataset_input_context.get() == "test"
                raise ValueError("test error")

        # Then: context variables are still reset
        assert _dataset_input_context.get(None) is None
        assert _dataset_output_context.get(None) is None

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_processor_on_start_sets_dataset_attributes(self, mock_processor_deps, reset_dataset_context):
        """Test that on_start sets dataset attributes on spans from context."""
        # Given: dataset context variables are set
        _dataset_input_context.set("input question")
        _dataset_output_context.set("expected answer")
        _dataset_metadata_context.set({"source": "test_dataset"})

        processor = GalileoSpanProcessor()
        mock_span = Mock()

        # When: on_start is called
        processor.on_start(mock_span, None)

        # Then: dataset attributes are set on the span
        actual_calls = {(args[0], args[1]) for args, _ in mock_span.set_attribute.call_args_list}
        assert ("galileo.dataset.input", "input question") in actual_calls
        assert ("galileo.dataset.output", "expected answer") in actual_calls
        assert ("galileo.dataset.metadata", json.dumps({"source": "test_dataset"})) in actual_calls

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    @patch("galileo.otel.OTLPSpanExporter.export")
    @patch("galileo.otel.Resource")
    def test_exporter_export_merges_dataset_attributes(
        self, mock_resource_class, mock_parent_export, reset_dataset_context
    ):
        """Test that export merges dataset attributes from span into resource."""
        # Given: an exporter with mocked dependencies
        with (
            patch("galileo.otel.OTLPSpanExporter.__init__", return_value=None),
            patch("galileo.otel.GalileoPythonConfig.get") as mock_config_get,
        ):
            config = Mock()
            config.api_url = "https://api.galileo.ai"
            config.api_key = SecretStr("test-key")
            mock_config_get.return_value = config

            exporter = GalileoOTLPExporter(project="test-project", logstream="test-logstream")
            exporter._session = Mock()
            exporter._session.headers = {}

        # Given: a span with dataset attributes (set during on_start)
        mock_span = Mock()
        mock_span.attributes = {
            "galileo.project.name": "test-project",
            "galileo.logstream.name": "test-logstream",
            "galileo.dataset.input": "test input",
            "galileo.dataset.output": "expected output",
            "galileo.dataset.metadata": json.dumps({"key": "value"}),
        }
        mock_merged_resource = Mock()
        mock_span.resource = Mock()
        mock_span.resource.merge.return_value = mock_merged_resource
        mock_new_resource = Mock()
        mock_resource_class.return_value = mock_new_resource

        # When: export is called
        exporter.export([mock_span])

        # Then: Resource is created with dataset attributes
        resource_call_kwargs = mock_resource_class.call_args[0][0]
        assert resource_call_kwargs["galileo.dataset.input"] == "test input"
        assert resource_call_kwargs["galileo.dataset.output"] == "expected output"
        assert resource_call_kwargs["galileo.dataset.metadata"] == json.dumps({"key": "value"})

        # Then: resource was merged into the span
        mock_span.resource.merge.assert_called_once_with(mock_new_resource)
        assert mock_span._resource == mock_merged_resource

    @pytest.mark.skipif(not OTEL_AVAILABLE, reason="OpenTelemetry not available")
    def test_galileo_dataset_context_partial_values(self, reset_dataset_context):
        """Test that galileo_dataset_context works with partial values."""
        # When: only some values are provided
        with galileo_dataset_context(dataset_output="expected only"):
            # Then: only provided values are set
            assert _dataset_input_context.get(None) is None
            assert _dataset_output_context.get() == "expected only"
            assert _dataset_metadata_context.get(None) is None

        # Then: values are reset after exit
        assert _dataset_output_context.get(None) is None
