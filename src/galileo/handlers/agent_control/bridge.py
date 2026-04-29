from __future__ import annotations

import importlib
import logging
import threading
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from types import ModuleType
from typing import Any

from galileo.logger.control import ControlAppliesTo, ControlCheckStage, ControlResult
from galileo.logger.logger import GalileoLogger
from galileo.utils.serialization import serialize_to_str

logger = logging.getLogger(__name__)

_REGISTRATION_LOCK = threading.RLock()
_REGISTERED_BRIDGES: list[GalileoAgentControlBridge] = []
_PREVIOUS_TRACE_CONTEXT_PROVIDER: Any = None


@dataclass(frozen=True)
class _AgentControlModules:
    agent_control: ModuleType
    sinks: ModuleType
    trace_context: ModuleType


@dataclass(frozen=True)
class _ActiveContext:
    trace_id: str
    span_id: str


def _import_module(name: str) -> ModuleType:
    return importlib.import_module(name)


def _load_agent_control_modules() -> _AgentControlModules:
    try:
        return _AgentControlModules(
            agent_control=_import_module("agent_control"),
            sinks=_import_module("agent_control_telemetry.sinks"),
            trace_context=_import_module("agent_control_telemetry.trace_context"),
        )
    except ImportError as exc:
        raise ImportError(
            "Agent Control integration requires the agent-control SDK/telemetry packages to be installed."
        ) from exc


def _normalize_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
    return datetime.now(tz=timezone.utc)


def _duration_ms_to_ns(value: Any) -> int | None:
    if value is None:
        return None

    try:
        duration_ms = float(value)
    except (TypeError, ValueError):
        return None

    if duration_ms < 0:
        return None

    return int(duration_ms * 1_000_000)


def _stringify_metadata_value(value: Any) -> str:
    if value is None:
        return "None"
    if isinstance(value, str):
        return value
    return serialize_to_str(value)


def _stringify_metadata(metadata: dict[str, Any] | None) -> dict[str, str]:
    if not metadata:
        return {}
    return {str(key): _stringify_metadata_value(value) for key, value in metadata.items()}


def _extract_control_input(metadata: dict[str, Any] | None) -> str:
    if not metadata:
        return ""

    for key in ("selected_data", "selected_value", "value", "input"):
        if key in metadata and metadata[key] is not None:
            value = metadata[key]
            return value if isinstance(value, str) else serialize_to_str(value)

    return ""


def _normalize_context_id(value: Any) -> str | None:
    """Return a canonical UUID string, or None if value is absent or not a valid UUID."""
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    try:
        return str(uuid.UUID(text))
    except (TypeError, ValueError, AttributeError):
        return None


def _dispatch_trace_context() -> dict[str, str] | None:
    """Return the active Galileo trace context without letting idle loggers mask active ones.

    Agent Control exposes a single process-wide trace-context provider. Multiple
    ``GalileoLogger`` instances can coexist in the same process, so we keep one
    shared dispatcher installed and have it ask each registered bridge for an
    active context, newest registration first. This preserves the existing
    "latest active logger wins" behavior while allowing older active loggers to
    continue providing context if a newer logger is merely idle.

    When no Galileo bridge has an active parent, the dispatcher falls back to
    whatever provider was installed before Galileo registered itself.
    """
    with _REGISTRATION_LOCK:
        bridges = list(_REGISTERED_BRIDGES)
        previous_provider = _PREVIOUS_TRACE_CONTEXT_PROVIDER

    for bridge in reversed(bridges):
        active_context = bridge._active_context()
        if active_context is not None:
            return {"trace_id": active_context.trace_id, "span_id": active_context.span_id}

    if previous_provider is not None:
        return previous_provider()

    return None


class _GalileoControlEventSink:
    def __init__(self, bridge: GalileoAgentControlBridge) -> None:
        self._bridge = bridge

    def write_events(self, events: Any) -> Any:
        return self._bridge.write_events(events)


class GalileoAgentControlBridge:
    """Bridge Agent Control telemetry into the active Galileo logger hierarchy.

    Bridge rules:
    - Events are converted only when the logger has an active trace parent.
    - Events are converted only when their ``trace_id`` and ``span_id`` match the
      current Galileo trace/span context advertised through the public provider.
    - Events that fail validation or do not match the active context are dropped
      safely rather than attached to the wrong logger hierarchy.
    """

    def __init__(self, galileo_logger: GalileoLogger) -> None:
        self._galileo_logger = galileo_logger
        self._modules = _load_agent_control_modules()
        self._sink = _GalileoControlEventSink(self)
        self._registered = False

    def register(self) -> GalileoAgentControlBridge:
        """Register this bridge and install the shared Galileo trace-context dispatcher."""
        with _REGISTRATION_LOCK:
            global _PREVIOUS_TRACE_CONTEXT_PROVIDER

            if self._registered:
                return self

            current_provider = getattr(self._modules.trace_context, "_trace_context_provider", None)
            if not _REGISTERED_BRIDGES and current_provider is not _dispatch_trace_context:
                _PREVIOUS_TRACE_CONTEXT_PROVIDER = current_provider

            self._modules.agent_control.register_control_event_sink(self._sink)
            _REGISTERED_BRIDGES.append(self)
            self._modules.trace_context.set_trace_context_provider(_dispatch_trace_context)
            self._registered = True

        return self

    def unregister(self) -> None:
        """Unregister this bridge and restore the previous provider when the last bridge exits."""
        with _REGISTRATION_LOCK:
            global _PREVIOUS_TRACE_CONTEXT_PROVIDER

            if not self._registered:
                return

            self._modules.agent_control.unregister_control_event_sink(self._sink)
            _REGISTERED_BRIDGES[:] = [bridge for bridge in _REGISTERED_BRIDGES if bridge is not self]

            if _REGISTERED_BRIDGES:
                self._modules.trace_context.set_trace_context_provider(_dispatch_trace_context)
            else:
                self._modules.trace_context.set_trace_context_provider(_PREVIOUS_TRACE_CONTEXT_PROVIDER)
                _PREVIOUS_TRACE_CONTEXT_PROVIDER = None

            self._registered = False

    def write_events(self, events: Any) -> Any:
        """Convert Agent Control events into Galileo control spans."""
        active_context = self._active_context()
        if active_context is None:
            return self._sink_result(accepted=0, dropped=len(events))

        accepted = 0
        dropped = 0

        for event in events:
            if not self._matches_active_context(event, active_context):
                dropped += 1
                continue

            try:
                result = self._galileo_logger.add_control_span(**self._control_span_kwargs(event))
            except Exception:
                logger.warning("Agent Control event conversion failed", exc_info=True)
                dropped += 1
                continue
            if result is None:
                dropped += 1
            else:
                accepted += 1

        return self._sink_result(accepted=accepted, dropped=dropped)

    def _sink_result(self, *, accepted: int, dropped: int) -> Any:
        return self._modules.sinks.SinkResult(accepted=accepted, dropped=dropped)

    def _active_context(self) -> _ActiveContext | None:
        current_parent = self._galileo_logger.current_parent()
        if current_parent is None or current_parent.id is None:
            return None

        root_parent = current_parent
        while getattr(root_parent, "_parent", None) is not None:
            root_parent = root_parent._parent

        if getattr(root_parent, "id", None) is None:
            return None

        return _ActiveContext(trace_id=str(root_parent.id), span_id=str(current_parent.id))

    @staticmethod
    def _matches_active_context(event: Any, active_context: _ActiveContext) -> bool:
        event_trace_id = _normalize_context_id(getattr(event, "trace_id", None))
        event_span_id = _normalize_context_id(getattr(event, "span_id", None))
        active_trace_id = _normalize_context_id(active_context.trace_id)
        active_span_id = _normalize_context_id(active_context.span_id)
        return event_trace_id == active_trace_id and event_span_id == active_span_id

    @staticmethod
    def _control_span_kwargs(event: Any) -> dict[str, Any]:
        raw_metadata = dict(getattr(event, "metadata", {}) or {})
        control_input = _extract_control_input(raw_metadata)

        metadata = _stringify_metadata(raw_metadata)
        metadata["control_execution_id"] = str(getattr(event, "control_execution_id", ""))
        metadata["agent_control_trace_id"] = str(getattr(event, "trace_id", ""))
        metadata["agent_control_span_id"] = str(getattr(event, "span_id", ""))

        error_message = getattr(event, "error_message", None)
        status_code = 500 if error_message else 200

        check_stage = getattr(event, "check_stage", None)
        applies_to = getattr(event, "applies_to", None)

        return {
            "input": control_input,
            "output": ControlResult(
                action=event.action,
                matched=event.matched,
                confidence=getattr(event, "confidence", None),
                error_message=error_message,
            ),
            "name": getattr(event, "control_name", None),
            "created_at": _normalize_datetime(getattr(event, "timestamp", None)),
            "duration_ns": _duration_ms_to_ns(getattr(event, "execution_duration_ms", None)),
            "metadata": metadata,
            "tags": ["agent_control", "control"],
            "status_code": status_code,
            "id": getattr(event, "control_execution_id", None),
            "control_id": getattr(event, "control_id", None),
            "agent_name": getattr(event, "agent_name", None),
            "check_stage": ControlCheckStage(check_stage) if check_stage else None,
            "applies_to": ControlAppliesTo(applies_to) if applies_to else None,
            "evaluator_name": getattr(event, "evaluator_name", None),
            "selector_path": getattr(event, "selector_path", None),
        }


def setup_agent_control_bridge(galileo_logger: GalileoLogger) -> GalileoAgentControlBridge:
    """Create and register an Agent Control bridge for a Galileo logger."""
    return galileo_logger.enable_agent_control()
