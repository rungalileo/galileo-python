from unittest.mock import Mock, patch
import pytest
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter
from galileo.constants import DEFAULT_API_URL, FALLBACK_API_URL
from galileo.otel import _set_destination, enable_tracing, _safe_instrument
import os
import logging

# A basic span exporter for testing
class MockSpanExporter(SpanExporter):
    def __init__(self):
        self.spans = []

    def export(self, spans):
        self.spans.extend(spans)

    def shutdown(self):
        pass

    def force_flush(self, timeout_millis=30000):
        return True


@pytest.fixture(autouse=True)
def reset_opentelemetry():
    """Reset OpenTelemetry tracer provider before and after each test."""
    trace.set_tracer_provider(TracerProvider())
    yield
    trace.set_tracer_provider(TracerProvider())


@pytest.fixture
def mock_otel_components():
    with patch("galileo.otel.OTLPSpanExporter") as mock_exporter, \
         patch("galileo.otel.BatchSpanProcessor") as mock_processor, \
         patch("galileo.otel.TracerProvider") as mock_provider, \
         patch("galileo.otel.trace.set_tracer_provider") as mock_set_provider:
        yield {
            "exporter": mock_exporter,
            "processor": mock_processor,
            "provider": mock_provider,
            "set_provider": mock_set_provider,
        }

@pytest.fixture
def clean_environment(monkeypatch):
    """Fixture to clean up environment variables set during tests."""
    keys_to_clean = [
        "GALILEO_API_KEY",
        "GALILEO_PROJECT",
        "GALILEO_LOG_STREAM",
        "OTEL_EXPORTER_OTLP_TRACES_HEADERS",
    ]
    for key in keys_to_clean:
        monkeypatch.delenv(key, raising=False)


@patch("galileo.otel._set_destination", return_value="my-custom-endpoint.com/traces")
@patch("galileo.otel._safe_instrument")
def test_enable_tracing_with_params(
    mock_safe_instrument, mock_set_destination, mock_otel_components, clean_environment
):
    enable_tracing(
        api_key="test_key",
        project_name="test_project",
        logstream="test_logstream",
        console_url="https://my-custom-endpoint.com/traces"
    )

    mock_otel_components["exporter"].assert_called_once_with(endpoint="my-custom-endpoint.com/traces")
    
    assert "OTEL_EXPORTER_OTLP_TRACES_HEADERS" in os.environ
    headers = os.environ["OTEL_EXPORTER_OTLP_TRACES_HEADERS"]
    assert "Galileo-API-Key=test_key" in headers
    assert "project=test_project" in headers
    assert "logstream=test_logstream" in headers

    mock_otel_components["processor"].assert_called_once_with(mock_otel_components["exporter"].return_value)
    mock_otel_components["provider"].return_value.add_span_processor.assert_called_once_with(mock_otel_components["processor"].return_value)
    mock_otel_components["set_provider"].assert_called_once_with(mock_otel_components["provider"].return_value)

    assert mock_safe_instrument.call_count == 7


@patch("galileo.otel._set_destination", return_value="dummy_endpoint")
@patch("galileo.otel._safe_instrument")
def test_enable_tracing_with_env_vars(
    mock_safe_instrument, mock_set_destination, mock_otel_components, monkeypatch
):
    monkeypatch.setenv("GALILEO_API_KEY", "env_key")
    monkeypatch.setenv("GALILEO_PROJECT", "env_project")
    monkeypatch.setenv("GALILEO_LOG_STREAM", "env_logstream")
    monkeypatch.delenv("OTEL_EXPORTER_OTLP_TRACES_HEADERS", raising=False)

    enable_tracing(console_url="https://my-custom-endpoint.com/traces")

    headers = os.environ["OTEL_EXPORTER_OTLP_TRACES_HEADERS"]
    assert "Galileo-API-Key=env_key" in headers
    assert "project=env_project" in headers
    assert "logstream=env_logstream" in headers


@patch("opentelemetry.exporter.otlp.proto.http.trace_exporter.OTLPSpanExporter")
@patch("galileo.otel._set_destination", return_value="dummy_endpoint")
def test_enable_tracing_missing_api_key(mock_set_destination, mock_exporter, clean_environment):
    with pytest.raises(ValueError, match="Galileo API key missing"):
        enable_tracing(project_name="p", logstream="l")


@patch("galileo.otel._set_destination", return_value="dummy_endpoint")
def test_enable_tracing_missing_project_name(mock_set_destination, clean_environment):
    with pytest.raises(ValueError, match="Galileo project name missing"):
        enable_tracing(api_key="key", logstream="l")


@patch("galileo.otel._set_destination", return_value="dummy_endpoint")
def test_enable_tracing_missing_logstream(mock_set_destination, clean_environment):
    with pytest.raises(ValueError, match="Galileo logstream name missing"):
        enable_tracing(api_key="key", project_name="p")


@patch("galileo.otel._set_destination", return_value="dummy_endpoint")
@patch("galileo.otel._safe_instrument")
def test_enable_tracing_no_auto_instrument(
    mock_safe_instrument, mock_set_destination, mock_otel_components, clean_environment
):
    enable_tracing(
        api_key="test_key",
        project_name="test_project",
        logstream="test_logstream",
        auto_instrument=False
    )
    mock_safe_instrument.assert_not_called()


@pytest.mark.parametrize(
    "console_url, get_console_url_return, expected_endpoint",
    [
        ("https://console.customer.com/env/prod", None, "console.customer.com/env/prod"),
        ("https://api.customer.com/otel/traces", None, "api.customer.com/otel/traces"),
        ("", DEFAULT_API_URL, "api.arize.com/otel/traces"),
        ("", FALLBACK_API_URL, "app.dev.galileo.ai/api/galileo/otel/traces"),
        (FALLBACK_API_URL, None, "app.dev.galileo.ai/"), # Because url.path is '/'
        ("https://console.arize.com/", None, "console.arize.com/"), # Because url.path is '/'
        ("https://console.arize.com", None, "api.arize.com/otel/traces"),
    ]
)
@patch('galileo.api_client.GalileoApiClient.get_console_url')
def test_set_destination(mock_get_console_url, console_url, get_console_url_return, expected_endpoint):
    if get_console_url_return:
        mock_get_console_url.return_value = get_console_url_return
    
    assert _set_destination(console_url) == expected_endpoint


@patch("importlib.import_module")
def test_safe_instrument_success(mock_import_module):
    mock_instrumentor_class = Mock()
    mock_instrumentor_instance = mock_instrumentor_class.return_value
    mock_instrumentor_instance.is_instrumented.return_value = False
    
    mock_module = Mock()
    mock_module.OpenAIInstrumentor = mock_instrumentor_class
    
    mock_import_module.return_value = mock_module

    _safe_instrument("openinference.instrumentation.openai", "OpenAIInstrumentor")

    mock_import_module.assert_called_once_with("openinference.instrumentation.openai")
    mock_instrumentor_class.assert_called_once()
    mock_instrumentor_instance.is_instrumented.assert_called_once()
    mock_instrumentor_instance.instrument.assert_called_once()


@patch("importlib.import_module")
def test_safe_instrument_already_instrumented(mock_import_module):
    mock_instrumentor_class = Mock()
    mock_instrumentor_instance = mock_instrumentor_class.return_value
    mock_instrumentor_instance.is_instrumented.return_value = True
    
    mock_module = Mock()
    mock_module.OpenAIInstrumentor = mock_instrumentor_class
    
    mock_import_module.return_value = mock_module

    _safe_instrument("openinference.instrumentation.openai", "OpenAIInstrumentor")

    mock_instrumentor_instance.instrument.assert_not_called()


@patch("importlib.import_module", side_effect=ModuleNotFoundError)
def test_safe_instrument_module_not_found(mock_import_module, caplog):
    with caplog.at_level(logging.DEBUG):
        _safe_instrument("non.existent.module", "NonExistentInstrumentor")
        assert "not installed – skipping instrumentation" in caplog.text


@patch("importlib.import_module")
def test_safe_instrument_general_exception(mock_import_module, caplog):
    mock_import_module.side_effect = Exception("unexpected error")
    _safe_instrument("any.module", "AnyInstrumentor")
    assert "Failed to auto-instrument any.module: unexpected error" in caplog.text 