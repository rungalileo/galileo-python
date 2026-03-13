"""Tests for IngestTraces client (dedicated ingest service)."""

import logging
from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID

import httpx
import pytest
import respx

from galileo.logger import GalileoLogger
from galileo.schema.logged import LoggedLlmSpan, LoggedTrace
from galileo.schema.trace import LoggingMethod, SpansIngestRequest, TracesIngestRequest
from galileo.traces import IngestTraces
from galileo.utils.headers_data import get_package_version
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client, setup_mock_traces_client

LOGGER = logging.getLogger(__name__)

PROJECT_ID = "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a"
LOG_STREAM_ID = "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9b"
EXPERIMENT_ID = "6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9d"
INGEST_URL = "https://ingest.example.com"


class TestIngestTracesInit:
    @patch("galileo.traces.GalileoPythonConfig")
    def test_requires_log_stream_or_experiment(self, mock_config_class) -> None:
        mock_config_class.get.return_value = Mock()

        # When/Then: missing both raises ValueError
        with pytest.raises(ValueError, match="log_stream_id or experiment_id must be set"):
            IngestTraces(project_id=PROJECT_ID)

    @patch("galileo.traces.GalileoPythonConfig")
    def test_accepts_log_stream_id(self, mock_config_class) -> None:
        mock_config_class.get.return_value = Mock()

        client = IngestTraces(project_id=PROJECT_ID, log_stream_id=LOG_STREAM_ID)
        assert client.project_id == PROJECT_ID
        assert client.log_stream_id == LOG_STREAM_ID

    @patch("galileo.traces.GalileoPythonConfig")
    def test_accepts_experiment_id(self, mock_config_class) -> None:
        mock_config_class.get.return_value = Mock()

        client = IngestTraces(project_id=PROJECT_ID, experiment_id=EXPERIMENT_ID)
        assert client.experiment_id == EXPERIMENT_ID


class TestIngestBaseUrl:
    @patch("galileo.traces.GalileoPythonConfig")
    def test_uses_galileo_ingest_url_when_set(self, mock_config_class, monkeypatch) -> None:
        mock_config_class.get.return_value = Mock()
        monkeypatch.setenv("GALILEO_INGEST_URL", INGEST_URL)

        client = IngestTraces(project_id=PROJECT_ID, log_stream_id=LOG_STREAM_ID)
        assert client._get_ingest_base_url() == INGEST_URL

    @patch("galileo.traces.GalileoPythonConfig")
    def test_strips_trailing_slash(self, mock_config_class, monkeypatch) -> None:
        mock_config_class.get.return_value = Mock()
        monkeypatch.setenv("GALILEO_INGEST_URL", f"{INGEST_URL}/")

        client = IngestTraces(project_id=PROJECT_ID, log_stream_id=LOG_STREAM_ID)
        assert client._get_ingest_base_url() == INGEST_URL

    @patch("galileo.traces.GalileoPythonConfig")
    def test_falls_back_to_api_url(self, mock_config_class, monkeypatch) -> None:
        monkeypatch.delenv("GALILEO_INGEST_URL", raising=False)
        mock_config = Mock()
        mock_config.api_url = "https://api.galileo.ai"
        mock_config.console_url = "https://console.galileo.ai"
        mock_config_class.get.return_value = mock_config

        client = IngestTraces(project_id=PROJECT_ID, log_stream_id=LOG_STREAM_ID)
        assert client._get_ingest_base_url() == "https://api.galileo.ai"

    @patch("galileo.traces.GalileoPythonConfig")
    def test_falls_back_to_console_url_when_no_api_url(self, mock_config_class, monkeypatch) -> None:
        monkeypatch.delenv("GALILEO_INGEST_URL", raising=False)
        mock_config = Mock()
        mock_config.api_url = None
        mock_config.console_url = "https://console.galileo.ai"
        mock_config_class.get.return_value = mock_config

        client = IngestTraces(project_id=PROJECT_ID, log_stream_id=LOG_STREAM_ID)
        assert client._get_ingest_base_url() == "https://console.galileo.ai"


class TestAuthHeaders:
    @patch("galileo.traces.GalileoPythonConfig")
    def test_uses_api_key_when_available(self, mock_config_class) -> None:
        mock_config = Mock()
        mock_config.api_key.get_secret_value.return_value = "my-api-key"
        mock_config.jwt_token = None
        mock_config_class.get.return_value = mock_config

        client = IngestTraces(project_id=PROJECT_ID, log_stream_id=LOG_STREAM_ID)
        headers = client._get_auth_headers()

        assert headers["Galileo-API-Key"] == "my-api-key"
        assert "Authorization" not in headers

    @patch("galileo.traces.GalileoPythonConfig")
    def test_uses_jwt_when_no_api_key(self, mock_config_class) -> None:
        mock_config = Mock()
        mock_config.api_key = None
        mock_config.jwt_token.get_secret_value.return_value = "my-jwt-token"
        mock_config_class.get.return_value = mock_config

        client = IngestTraces(project_id=PROJECT_ID, log_stream_id=LOG_STREAM_ID)
        headers = client._get_auth_headers()

        assert headers["Authorization"] == "Bearer my-jwt-token"
        assert "Galileo-API-Key" not in headers

    @patch("galileo.traces.GalileoPythonConfig")
    def test_includes_sdk_header(self, mock_config_class) -> None:
        mock_config = Mock()
        mock_config.api_key = None
        mock_config.jwt_token = None
        mock_config_class.get.return_value = mock_config

        client = IngestTraces(project_id=PROJECT_ID, log_stream_id=LOG_STREAM_ID)
        headers = client._get_auth_headers()

        assert headers["Content-Type"] == "application/json"
        assert headers["X-Galileo-SDK"].startswith(f"galileo-python/{get_package_version()}")


class TestIngestTracesRequest:
    @pytest.fixture
    def mock_config(self):
        with patch("galileo.traces.GalileoPythonConfig") as mock_config_class:
            mock_config = Mock()
            mock_config.api_key.get_secret_value.return_value = "test-key"
            mock_config.jwt_token = None
            mock_config.ssl_context = True
            mock_config.api_url = "https://api.galileo.ai"
            mock_config_class.get.return_value = mock_config
            yield mock_config

    @pytest.fixture
    def client(self, mock_config):
        return IngestTraces(project_id=PROJECT_ID, log_stream_id=LOG_STREAM_ID)

    @respx.mock
    @pytest.mark.asyncio
    async def test_ingest_traces_posts_to_correct_url(self, client, monkeypatch) -> None:
        # Given: an ingest URL is configured
        monkeypatch.setenv("GALILEO_INGEST_URL", INGEST_URL)

        expected_url = f"{INGEST_URL}/ingest/traces/{PROJECT_ID}"
        route = respx.post(expected_url).mock(return_value=httpx.Response(200, json={"status": "ok"}))

        trace = LoggedTrace(input="hello", output="world")
        request = TracesIngestRequest(traces=[trace])

        # When: ingesting traces
        result = await client.ingest_traces(request)

        # Then: request hits the ingest service URL
        assert route.called
        assert result == {"status": "ok"}

    @respx.mock
    @pytest.mark.asyncio
    async def test_ingest_traces_sets_logging_method(self, client, monkeypatch) -> None:
        monkeypatch.setenv("GALILEO_INGEST_URL", INGEST_URL)

        expected_url = f"{INGEST_URL}/ingest/traces/{PROJECT_ID}"
        route = respx.post(expected_url).mock(return_value=httpx.Response(200, json={}))

        trace = LoggedTrace(input="hello")
        request = TracesIngestRequest(traces=[trace])

        await client.ingest_traces(request)

        # Then: logging_method was set to python_client
        assert request.logging_method == LoggingMethod.python_client
        sent_body = route.calls[0].request.content
        assert b"python_client" in sent_body

    @respx.mock
    @pytest.mark.asyncio
    async def test_ingest_traces_sets_log_stream_id(self, client, monkeypatch) -> None:
        monkeypatch.setenv("GALILEO_INGEST_URL", INGEST_URL)
        expected_url = f"{INGEST_URL}/ingest/traces/{PROJECT_ID}"
        respx.post(expected_url).mock(return_value=httpx.Response(200, json={}))

        trace = LoggedTrace(input="hello")
        request = TracesIngestRequest(traces=[trace])

        await client.ingest_traces(request)

        # Then: log_stream_id was populated from the client
        assert request.log_stream_id == UUID(LOG_STREAM_ID)

    @respx.mock
    @pytest.mark.asyncio
    async def test_ingest_traces_sets_experiment_id(self, mock_config, monkeypatch) -> None:
        monkeypatch.setenv("GALILEO_INGEST_URL", INGEST_URL)
        client = IngestTraces(project_id=PROJECT_ID, experiment_id=EXPERIMENT_ID)

        expected_url = f"{INGEST_URL}/ingest/traces/{PROJECT_ID}"
        respx.post(expected_url).mock(return_value=httpx.Response(200, json={}))

        trace = LoggedTrace(input="hello")
        request = TracesIngestRequest(traces=[trace])

        await client.ingest_traces(request)

        assert request.experiment_id == UUID(EXPERIMENT_ID)

    @respx.mock
    @pytest.mark.asyncio
    async def test_ingest_traces_falls_back_to_api_url(self, client, monkeypatch) -> None:
        # Given: no GALILEO_INGEST_URL set
        monkeypatch.delenv("GALILEO_INGEST_URL", raising=False)

        expected_url = f"https://api.galileo.ai/ingest/traces/{PROJECT_ID}"
        route = respx.post(expected_url).mock(return_value=httpx.Response(200, json={"ok": True}))

        trace = LoggedTrace(input="hello")
        request = TracesIngestRequest(traces=[trace])

        result = await client.ingest_traces(request)

        assert route.called
        assert result == {"ok": True}


class TestIngestSpansRequest:
    @pytest.fixture
    def mock_config(self):
        with patch("galileo.traces.GalileoPythonConfig") as mock_config_class:
            mock_config = Mock()
            mock_config.api_key.get_secret_value.return_value = "test-key"
            mock_config.jwt_token = None
            mock_config.ssl_context = True
            mock_config.api_url = "https://api.galileo.ai"
            mock_config_class.get.return_value = mock_config
            yield mock_config

    @pytest.fixture
    def client(self, mock_config):
        return IngestTraces(project_id=PROJECT_ID, log_stream_id=LOG_STREAM_ID)

    @respx.mock
    @pytest.mark.asyncio
    async def test_ingest_spans_posts_to_correct_url(self, client, monkeypatch) -> None:
        monkeypatch.setenv("GALILEO_INGEST_URL", INGEST_URL)

        expected_url = f"{INGEST_URL}/ingest/spans/{PROJECT_ID}"
        route = respx.post(expected_url).mock(return_value=httpx.Response(200, json={"status": "ok"}))

        span = LoggedLlmSpan(input="hello", output="world", model="gpt-4o")
        request = SpansIngestRequest(spans=[span], trace_id=UUID(PROJECT_ID), parent_id=UUID(LOG_STREAM_ID))

        result = await client.ingest_spans(request)

        assert route.called
        assert result == {"status": "ok"}

    @respx.mock
    @pytest.mark.asyncio
    async def test_ingest_spans_sets_log_stream_id(self, client, monkeypatch) -> None:
        monkeypatch.setenv("GALILEO_INGEST_URL", INGEST_URL)
        expected_url = f"{INGEST_URL}/ingest/spans/{PROJECT_ID}"
        respx.post(expected_url).mock(return_value=httpx.Response(200, json={}))

        span = LoggedLlmSpan(input="hello", output="world", model="gpt-4o")
        request = SpansIngestRequest(spans=[span], trace_id=UUID(PROJECT_ID), parent_id=UUID(LOG_STREAM_ID))

        await client.ingest_spans(request)

        assert request.log_stream_id == UUID(LOG_STREAM_ID)
        assert request.logging_method == LoggingMethod.python_client


class TestLoggerIngestClientWiring:
    """Test that GalileoLogger creates and uses IngestTraces when GALILEO_INGEST_URL is set."""

    @patch("galileo.logger.logger.LogStreams")
    @patch("galileo.logger.logger.Projects")
    @patch("galileo.logger.logger.Traces")
    def test_no_ingest_client_without_env_var(
        self, mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, monkeypatch
    ) -> None:
        # Given: GALILEO_INGEST_URL is not set
        monkeypatch.delenv("GALILEO_INGEST_URL", raising=False)
        setup_mock_traces_client(mock_traces_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)

        # When: creating a logger
        logger = GalileoLogger(project="my_project", log_stream="my_log_stream", mode="batch")

        # Then: ingest client is not created
        assert logger._ingest_client is None
        assert logger._traces_client is not None

    @patch("galileo.logger.logger.IngestTraces")
    @patch("galileo.logger.logger.LogStreams")
    @patch("galileo.logger.logger.Projects")
    @patch("galileo.logger.logger.Traces")
    def test_ingest_client_created_with_env_var(
        self,
        mock_traces_client: Mock,
        mock_projects_client: Mock,
        mock_logstreams_client: Mock,
        mock_ingest_client: Mock,
        monkeypatch,
    ) -> None:
        # Given: GALILEO_INGEST_URL is set
        monkeypatch.setenv("GALILEO_INGEST_URL", INGEST_URL)
        setup_mock_traces_client(mock_traces_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)

        # When: creating a logger
        logger = GalileoLogger(project="my_project", log_stream="my_log_stream", mode="batch")

        # Then: ingest client is created
        assert logger._ingest_client is not None
        mock_ingest_client.assert_called_once()

    @patch("galileo.logger.logger.IngestTraces")
    @patch("galileo.logger.logger.LogStreams")
    @patch("galileo.logger.logger.Projects")
    @patch("galileo.logger.logger.Traces")
    def test_flush_uses_ingest_client_when_available(
        self,
        mock_traces_client: Mock,
        mock_projects_client: Mock,
        mock_logstreams_client: Mock,
        mock_ingest_client: Mock,
        monkeypatch,
    ) -> None:
        # Given: GALILEO_INGEST_URL is set, logger has a trace
        monkeypatch.setenv("GALILEO_INGEST_URL", INGEST_URL)
        mock_traces_instance = setup_mock_traces_client(mock_traces_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)

        mock_ingest_instance = Mock()
        mock_ingest_instance.ingest_traces = AsyncMock(return_value={})
        mock_ingest_client.return_value = mock_ingest_instance

        logger = GalileoLogger(project="my_project", log_stream="my_log_stream", mode="batch")
        logger.start_trace(input="hello")
        logger.add_llm_span(input="hello", output="world", model="gpt-4o")
        logger.conclude(output="world")

        # When: flushing
        logger.flush()

        # Then: ingest client was used, not the traces client
        mock_ingest_instance.ingest_traces.assert_called_once()
        mock_traces_instance.ingest_traces.assert_not_called()

    @patch("galileo.logger.logger.LogStreams")
    @patch("galileo.logger.logger.Projects")
    @patch("galileo.logger.logger.Traces")
    def test_flush_falls_back_to_traces_client_without_env_var(
        self, mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, monkeypatch
    ) -> None:
        # Given: GALILEO_INGEST_URL is not set
        monkeypatch.delenv("GALILEO_INGEST_URL", raising=False)
        mock_traces_instance = setup_mock_traces_client(mock_traces_client)
        setup_mock_projects_client(mock_projects_client)
        setup_mock_logstreams_client(mock_logstreams_client)

        logger = GalileoLogger(project="my_project", log_stream="my_log_stream", mode="batch")
        logger.start_trace(input="hello")
        logger.add_llm_span(input="hello", output="world", model="gpt-4o")
        logger.conclude(output="world")

        # When: flushing
        logger.flush()

        # Then: traces client was used (fallback)
        mock_traces_instance.ingest_traces.assert_called_once()
