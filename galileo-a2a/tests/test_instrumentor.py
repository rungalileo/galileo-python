"""Tests for A2AInstrumentor lifecycle."""

from unittest.mock import MagicMock, patch

from galileo_a2a.instrumentor import A2AInstrumentor


class TestA2AInstrumentor:
    def test_instrumentation_dependencies(self):
        # Given: an A2AInstrumentor instance
        instrumentor = A2AInstrumentor()

        # When: checking dependencies
        deps = instrumentor.instrumentation_dependencies()

        # Then: requires a2a-sdk
        assert "a2a-sdk>=0.3.0,<1.0.0" in deps

    @patch("galileo_a2a.instrumentor._patch_server")
    @patch("galileo_a2a.instrumentor._patch_client")
    def test_instrument_calls_patch_functions(self, mock_patch_client, mock_patch_server):
        # Given: an instrumentor
        instrumentor = A2AInstrumentor()

        # When: instrumenting
        instrumentor._instrument(agent_name="test-agent")

        # Then: both client and server patches are applied
        mock_patch_client.assert_called_once()
        mock_patch_server.assert_called_once()

        # And: agent_name is passed through
        _, kwargs = mock_patch_client.call_args
        assert kwargs["agent_name"] == "test-agent"

    @patch("galileo_a2a.instrumentor._unpatch_server")
    @patch("galileo_a2a.instrumentor._unpatch_client")
    def test_uninstrument_calls_unpatch_functions(self, mock_unpatch_client, mock_unpatch_server):
        # Given: an instrumentor
        instrumentor = A2AInstrumentor()

        # When: uninstrumenting
        instrumentor._uninstrument()

        # Then: both client and server patches are removed
        mock_unpatch_client.assert_called_once()
        mock_unpatch_server.assert_called_once()

    @patch("galileo_a2a.instrumentor._patch_server")
    @patch("galileo_a2a.instrumentor._patch_client")
    def test_instrument_passes_tracer_provider(self, mock_patch_client, mock_patch_server):
        # Given: a mock tracer provider
        mock_provider = MagicMock()
        instrumentor = A2AInstrumentor()

        # When: instrumenting with a tracer provider
        instrumentor._instrument(tracer_provider=mock_provider)

        # Then: patches are called (tracer is created internally from provider)
        mock_patch_client.assert_called_once()
        mock_patch_server.assert_called_once()
