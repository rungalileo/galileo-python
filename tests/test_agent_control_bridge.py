from __future__ import annotations

import asyncio
import builtins
import dataclasses
import datetime
import importlib
import sys
import types
import uuid
from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest

import galileo.logger.control as control_module
import galileo.logger.logger as logger_module
import galileo.schema.logged as logged_module
from galileo.handlers.agent_control import setup_agent_control_bridge
from galileo.logger.control import ControlResult, ControlSpan
from galileo.logger.logger import GalileoLogger
from galileo.schema.trace import SpansIngestRequest, TracesIngestRequest
from tests.testutils.setup import (
    setup_mock_logstreams_client,
    setup_mock_projects_client,
    setup_mock_traces_client,
    setup_thread_pool_request_capture,
)


@dataclass
class FakeControlExecutionEvent:
    control_execution_id: str
    trace_id: str
    span_id: str
    agent_name: str
    control_id: int
    control_name: str
    check_stage: str
    applies_to: str
    action: str
    matched: bool
    confidence: float | None
    timestamp: datetime.datetime
    execution_duration_ms: float | None = None
    evaluator_name: str | None = None
    selector_path: str | None = None
    error_message: str | None = None
    metadata: dict[str, object] = dataclasses.field(default_factory=dict)


@pytest.fixture
def fake_agent_control_modules(monkeypatch):
    telemetry_module = types.ModuleType("agent_control_telemetry")
    sinks_module = types.ModuleType("agent_control_telemetry.sinks")
    trace_context_module = types.ModuleType("agent_control_telemetry.trace_context")
    agent_control_module = types.ModuleType("agent_control")

    @dataclass(frozen=True)
    class SinkResult:
        accepted: int
        dropped: int = 0

    registered_sinks: list[object] = []

    def register_control_event_sink(sink: object) -> None:
        if sink not in registered_sinks:
            registered_sinks.append(sink)

    def unregister_control_event_sink(sink: object) -> None:
        if sink in registered_sinks:
            registered_sinks.remove(sink)

    trace_context_module._trace_context_provider = None

    def set_trace_context_provider(provider) -> None:
        trace_context_module._trace_context_provider = provider

    def clear_trace_context_provider() -> None:
        trace_context_module._trace_context_provider = None

    def get_trace_context_from_provider():
        provider = trace_context_module._trace_context_provider
        if provider is None:
            return None
        return provider()

    sinks_module.SinkResult = SinkResult
    trace_context_module.set_trace_context_provider = set_trace_context_provider
    trace_context_module.clear_trace_context_provider = clear_trace_context_provider
    trace_context_module.get_trace_context_from_provider = get_trace_context_from_provider
    agent_control_module.register_control_event_sink = register_control_event_sink
    agent_control_module.unregister_control_event_sink = unregister_control_event_sink
    agent_control_module._registered_sinks = registered_sinks

    telemetry_module.sinks = sinks_module
    telemetry_module.trace_context = trace_context_module

    monkeypatch.setitem(sys.modules, "agent_control", agent_control_module)
    monkeypatch.setitem(sys.modules, "agent_control_telemetry", telemetry_module)
    monkeypatch.setitem(sys.modules, "agent_control_telemetry.sinks", sinks_module)
    monkeypatch.setitem(sys.modules, "agent_control_telemetry.trace_context", trace_context_module)

    yield {"agent_control": agent_control_module, "trace_context": trace_context_module, "sinks": sinks_module}

    bridge_module = sys.modules.get("galileo.handlers.agent_control.bridge")
    if bridge_module is not None:
        bridge_module._REGISTERED_BRIDGES.clear()
        bridge_module._PREVIOUS_TRACE_CONTEXT_PROVIDER = None


def _make_event(logger: GalileoLogger, **overrides: object) -> FakeControlExecutionEvent:
    current_parent = logger.current_parent()
    assert current_parent is not None

    root_parent = current_parent
    while getattr(root_parent, "_parent", None) is not None:
        root_parent = root_parent._parent

    payload = {
        "control_execution_id": str(uuid.uuid4()),
        "trace_id": str(root_parent.id),
        "span_id": str(current_parent.id),
        "agent_name": "assistant",
        "control_id": 7,
        "control_name": "toxicity-guardrail",
        "check_stage": "pre",
        "applies_to": "llm_call",
        "action": "observe",
        "matched": True,
        "confidence": 0.91,
        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc),
        "execution_duration_ms": 12.5,
        "evaluator_name": "regex",
        "selector_path": "input",
        "error_message": None,
        "metadata": {
            "selected_data": "selected text",
            "primary_selector_path": "input",
            "all_selector_paths": ["input", "output"],
        },
    }
    payload.update(overrides)
    return FakeControlExecutionEvent(**payload)


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_enable_agent_control_registers_provider_and_sink(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, fake_agent_control_modules
) -> None:
    # Given: a logger with an active Galileo parent and Agent Control available
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(input="trace input")
    workflow = logger.add_workflow_span(input="workflow input", name="workflow")

    # When: enabling the Agent Control bridge
    bridge = setup_agent_control_bridge(logger)

    # Then: the Galileo-backed sink and trace-context provider are registered
    assert fake_agent_control_modules["agent_control"]._registered_sinks == [bridge._sink]
    assert fake_agent_control_modules["trace_context"].get_trace_context_from_provider() == {
        "trace_id": str(logger.traces[0].id),
        "span_id": str(workflow.id),
    }

    # When: disabling the bridge again
    logger.disable_agent_control()

    # Then: registration is cleaned up deterministically
    assert fake_agent_control_modules["agent_control"]._registered_sinks == []
    assert fake_agent_control_modules["trace_context"].get_trace_context_from_provider() is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_logger_auto_registers_agent_control_bridge_when_available(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, fake_agent_control_modules
) -> None:
    # Given: Agent Control modules are importable when the logger is created
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # When: creating a new Galileo logger
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")

    # Then: the Agent Control bridge is registered automatically
    bridge = logger._agent_control_bridge
    assert bridge is not None
    assert fake_agent_control_modules["agent_control"]._registered_sinks == [bridge._sink]


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_logger_init_does_not_raise_when_agent_control_is_missing(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Given: Agent Control modules are not importable
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    monkeypatch.setattr(
        "galileo.handlers.agent_control.bridge._import_module", lambda name: (_ for _ in ()).throw(ImportError(name))
    )

    # When: creating a new Galileo logger
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")

    # Then: logger initialization still succeeds without the optional integration
    assert getattr(logger, "_agent_control_bridge", None) is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_agent_control_cleanup_restores_previous_provider_across_loggers(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, fake_agent_control_modules
) -> None:
    # Given: an existing external provider and two Galileo loggers registering in sequence
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    def external_provider():
        return {"trace_id": "external-trace", "span_id": "external-span"}

    fake_agent_control_modules["trace_context"].set_trace_context_provider(external_provider)

    logger_a = GalileoLogger(project="project_a", log_stream="stream_a")
    logger_a.start_trace(input="trace a")
    logger_a.add_workflow_span(input="workflow a", name="workflow_a")
    bridge_a = setup_agent_control_bridge(logger_a)

    logger_b = GalileoLogger(project="project_b", log_stream="stream_b")
    logger_b.start_trace(input="trace b")
    workflow_b = logger_b.add_workflow_span(input="workflow b", name="workflow_b")
    bridge_b = setup_agent_control_bridge(logger_b)

    # When: the earlier bridge unregisters while the newer one remains active
    bridge_a.unregister()

    # Then: the top-of-stack logger still owns the provider
    assert fake_agent_control_modules["trace_context"].get_trace_context_from_provider() == {
        "trace_id": str(logger_b.traces[0].id),
        "span_id": str(workflow_b.id),
    }

    # When: the final Galileo bridge unregisters
    bridge_b.unregister()

    # Then: the original external provider is restored
    assert fake_agent_control_modules["trace_context"].get_trace_context_from_provider() == {
        "trace_id": "external-trace",
        "span_id": "external-span",
    }


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_agent_control_cleanup_does_not_clobber_provider_installed_while_active(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, fake_agent_control_modules
) -> None:
    # Given: Galileo registered after one external provider, then another provider takes over while active
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    def previous_provider():
        return {"trace_id": "previous-trace", "span_id": "previous-span"}

    def replacement_provider():
        return {"trace_id": "replacement-trace", "span_id": "replacement-span"}

    fake_agent_control_modules["trace_context"].set_trace_context_provider(previous_provider)
    logger_a = GalileoLogger(project="project_a", log_stream="stream_a")
    bridge_a = setup_agent_control_bridge(logger_a)

    # When: external code replaces the provider while the bridge is active, then the bridge unregisters
    fake_agent_control_modules["trace_context"].set_trace_context_provider(replacement_provider)
    bridge_a.unregister()

    # Then: Galileo leaves the replacement provider untouched instead of restoring its stale snapshot
    assert fake_agent_control_modules["trace_context"].get_trace_context_from_provider() == {
        "trace_id": "replacement-trace",
        "span_id": "replacement-span",
    }
    assert fake_agent_control_modules["agent_control"]._registered_sinks == []


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_idle_new_logger_does_not_mask_active_logger_context(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, fake_agent_control_modules
) -> None:
    # Given: one logger is actively tracing before another logger is constructed
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    logger_a = GalileoLogger(project="project_a", log_stream="stream_a")
    logger_a.start_trace(input="trace a")
    workflow_a = logger_a.add_workflow_span(input="workflow a", name="workflow_a")
    bridge_a = setup_agent_control_bridge(logger_a)

    # When: a second logger auto-registers without starting a trace
    GalileoLogger(project="project_b", log_stream="stream_b")
    active_context = fake_agent_control_modules["trace_context"].get_trace_context_from_provider()

    # Then: the shared provider still reports the active logger's context
    assert active_context == {"trace_id": str(logger_a.traces[0].id), "span_id": str(workflow_a.id)}

    # When: Agent Control stamps and emits an event using the shared provider
    event = _make_event(logger_a, trace_id=active_context["trace_id"], span_id=active_context["span_id"])
    result = bridge_a.write_events([event])

    # Then: the event is accepted instead of being dropped by the older active logger
    assert result.accepted == 1
    assert result.dropped == 0
    assert len(workflow_a.spans) == 1


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_agent_control_event_converts_to_control_span_in_batch_mode(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, fake_agent_control_modules
) -> None:
    # Given: a batch logger with an active parent and a matching Agent Control event
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(input="trace input")
    workflow = logger.add_workflow_span(input="workflow input", name="workflow")
    bridge = setup_agent_control_bridge(logger)
    event = _make_event(logger)

    # When: the bridge receives the event through the public sink contract
    result = bridge.write_events([event])

    # Then: the event is converted into a Galileo ControlSpan under the current parent
    assert result.accepted == 1
    assert result.dropped == 0
    assert mock_traces_client_instance.ingest_traces.call_count == 0

    control_span = workflow.spans[0]
    assert isinstance(control_span, ControlSpan)
    assert control_span.id == uuid.UUID(event.control_execution_id)
    assert control_span.trace_id == logger.traces[0].id
    assert control_span.parent_id == workflow.id
    assert control_span.name == "toxicity-guardrail"
    assert control_span.input == "selected text"
    assert control_span.output == ControlResult(action="observe", matched=True, confidence=0.91)
    assert control_span.metrics.duration_ns == 12_500_000
    assert control_span.user_metadata["control_execution_id"] == event.control_execution_id
    assert control_span.user_metadata["primary_selector_path"] == "input"
    assert control_span.user_metadata["all_selector_paths"] == '["input", "output"]'

    # When: the logger flushes in batch mode
    logger.flush()

    # Then: the control span is buffered normally and sent with the trace payload
    payload = mock_traces_client_instance.ingest_traces.call_args.args[0]
    assert isinstance(payload, TracesIngestRequest)
    flushed_control_span = payload.traces[0].spans[0].spans[0]
    assert isinstance(flushed_control_span, ControlSpan)
    assert flushed_control_span.id == uuid.UUID(event.control_execution_id)
    assert flushed_control_span.control_id == 7


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_agent_control_event_uses_empty_string_when_no_representative_input(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, fake_agent_control_modules
) -> None:
    # Given: an Agent Control event with metadata but no selected input value
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(input="trace input")
    workflow = logger.add_workflow_span(input="workflow input", name="workflow")
    bridge = setup_agent_control_bridge(logger)
    event = _make_event(logger, metadata={"primary_selector_path": "input"})

    # When: the bridge converts the event
    result = bridge.write_events([event])

    # Then: the control span uses the string input shape expected by ingestion
    assert result.accepted == 1
    assert result.dropped == 0
    assert workflow.spans[0].input == ""


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_agent_control_event_is_dropped_when_ids_are_not_valid_uuids(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, fake_agent_control_modules
) -> None:
    # Given: an active logger and an Agent Control event carrying non-UUID IDs
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(input="trace input")
    workflow = logger.add_workflow_span(input="workflow input", name="workflow")
    bridge = setup_agent_control_bridge(logger)
    event = _make_event(logger, trace_id="not-a-uuid", span_id="also-not-a-uuid")

    # When: the bridge receives the event
    result = bridge.write_events([event])

    # Then: the event is dropped because the IDs cannot be parsed as canonical UUIDs
    assert result.accepted == 0
    assert result.dropped == 1
    assert workflow.spans == []


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_agent_control_event_streams_immediately_in_distributed_mode(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, fake_agent_control_modules
) -> None:
    # Given: a distributed logger with request capture enabled
    mock_traces_client_instance = setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream", mode="distributed")
    capture = setup_thread_pool_request_capture(logger)
    logger.start_trace(input="trace input")
    workflow = logger.add_workflow_span(input="workflow input", name="workflow")
    bridge = setup_agent_control_bridge(logger)
    event = _make_event(logger)

    # When: the bridge receives the event
    result = bridge.write_events([event])

    # Then: the control span is attached locally and streamed immediately
    assert result.accepted == 1
    assert result.dropped == 0
    assert logger.current_parent() == workflow

    control_requests = [
        task.request
        for task in capture.get_all_tasks()
        if isinstance(task.request, SpansIngestRequest) and task.request.spans[0].type == "control"
    ]
    assert len(control_requests) == 1
    request = control_requests[0]
    assert isinstance(request.spans[0], ControlSpan)
    assert request.spans[0].id == uuid.UUID(event.control_execution_id)
    assert request.spans[0].trace_id == logger.traces[0].id
    assert request.spans[0].parent_id == workflow.id
    assert request.parent_id == workflow.id

    latest_control_task = next(
        task
        for task in capture.get_all_tasks()
        if isinstance(task.request, SpansIngestRequest) and task.request.spans[0].type == "control"
    )
    asyncio.run(latest_control_task.task_func())
    mock_traces_client_instance.ingest_spans.assert_called_with(request)


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_add_control_span_uses_model_default_name_in_fallback_mode(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Given: the logger is using the fallback ControlSpan model
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    original_import = builtins.__import__

    def force_fallback_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "galileo_core.schemas.logging.control":
            raise ImportError("forced fallback for test")
        return original_import(name, globals, locals, fromlist, level)

    try:
        with monkeypatch.context() as context:
            context.setattr(builtins, "__import__", force_fallback_import)
            importlib.reload(control_module)
            importlib.reload(logged_module)
            context.setattr(logger_module, "LoggedControlSpan", logged_module.LoggedControlSpan)

            logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
            logger.start_trace(input="trace input")
            workflow = logger.add_workflow_span(input="workflow input", name="workflow")

            # When: adding a control span without an explicit name
            control_span = logger.add_control_span(input="selected text", name=None)

            # Then: the fallback model default is applied and the span is preserved
            assert control_span is not None
            assert control_module.HAS_NATIVE_CONTROL_SPAN is False
            assert isinstance(control_span, logged_module.LoggedControlSpan)
            assert isinstance(control_span, control_module.ControlSpan)
            assert control_span.name == "control"
            assert workflow.spans == [control_span]
    finally:
        importlib.reload(control_module)
        importlib.reload(logged_module)
        logger_module.LoggedControlSpan = logged_module.LoggedControlSpan


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_agent_control_event_is_dropped_when_context_does_not_match(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, fake_agent_control_modules
) -> None:
    # Given: an active logger and an Agent Control event with stale trace context
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)
    logger = GalileoLogger(project="my_project", log_stream="my_log_stream")
    logger.start_trace(input="trace input")
    workflow = logger.add_workflow_span(input="workflow input", name="workflow")
    bridge = setup_agent_control_bridge(logger)
    event = _make_event(logger, span_id="not-the-current-parent")

    # When: the bridge receives the stale event
    result = bridge.write_events([event])

    # Then: the event is safely ignored instead of being attached to the wrong parent
    assert result.accepted == 0
    assert result.dropped == 1
    assert workflow.spans == []
