"""Resolve Galileo context for Agent Control calls.

This module produces generic Agent Control targets from Galileo state. It does
not import the Agent Control SDK; callers wire the two SDKs together explicitly.
"""

from __future__ import annotations

import os
import threading
from dataclasses import dataclass
from uuid import UUID

from galileo.decorator import galileo_context
from galileo.utils.env_helpers import _get_log_stream_or_default, _get_project_or_default
from galileo.utils.singleton import GalileoLoggerSingleton

LOG_STREAM_TARGET_TYPE = "log_stream"


class AgentControlTargetUnresolvedError(ValueError):
    """Raised when no Agent Control target can be resolved from available inputs."""


@dataclass(frozen=True)
class AgentControlTarget:
    """A target identifier that can be passed to Agent Control.

    Parameters
    ----------
    target_type
        Opaque Agent Control target type. Agent Control treats this value as
        deployer-defined; Galileo currently auto-resolves only ``log_stream``
        targets.
    target_id
        Opaque Agent Control target ID.
    project_id
        Galileo project ID for logs, debugging, and audit context only. Agent
        Control resolves project ownership from ``target_type`` and
        ``target_id``.
    """

    target_type: str
    target_id: str
    project_id: str | None = None


def get_agent_control_target(
    *,
    target_type: str = LOG_STREAM_TARGET_TYPE,
    target_id: str | None = None,
    log_stream_id: str | None = None,
    project_id: str | None = None,
) -> AgentControlTarget:
    """Resolve an Agent Control target from explicit inputs or Galileo context.

    Resolution order:

    1. Explicit ``target_id``.
    2. Explicit ``log_stream_id`` for ``log_stream`` targets.
    3. ``GALILEO_LOG_STREAM_ID`` for ``log_stream`` targets.
    4. An already-initialized ``galileo_context`` logger.

    This helper does not resolve log stream names over the network. If only a
    log stream name is available, resolve it with the Galileo SDK first and pass
    the resulting ID explicitly.
    """
    explicit_project_id = _strip_optional_string(project_id)
    env_project_id = _strip_optional_string(os.getenv("GALILEO_PROJECT_ID"))
    resolved_project_id = explicit_project_id or env_project_id

    if target_type == LOG_STREAM_TARGET_TYPE:
        target_id = _strip_optional_string(target_id)
    log_stream_id = _strip_optional_string(log_stream_id)

    if target_type != LOG_STREAM_TARGET_TYPE and log_stream_id is not None:
        raise AgentControlTargetUnresolvedError("log_stream_id can only be used with target_type='log_stream'.")

    if target_id is not None and log_stream_id is not None and target_id != log_stream_id:
        raise AgentControlTargetUnresolvedError("target_id and log_stream_id must match when both are provided.")

    resolved_target_id = target_id if target_id is not None else log_stream_id
    if resolved_target_id is not None:
        if target_type == LOG_STREAM_TARGET_TYPE:
            source_label = "target_id" if target_id is not None else "log_stream_id"
            _validate_uuid(resolved_target_id, source_label)
        return AgentControlTarget(target_type=target_type, target_id=resolved_target_id, project_id=resolved_project_id)

    if target_type != LOG_STREAM_TARGET_TYPE:
        raise AgentControlTargetUnresolvedError(
            f"Could not resolve Agent Control target for target_type={target_type!r}. "
            "Provide target_id=<id> explicitly."
        )

    env_log_stream_id = _strip_optional_string(os.getenv("GALILEO_LOG_STREAM_ID"))
    if env_log_stream_id:
        _validate_uuid(env_log_stream_id, "GALILEO_LOG_STREAM_ID")
        return AgentControlTarget(
            target_type=LOG_STREAM_TARGET_TYPE, target_id=env_log_stream_id, project_id=resolved_project_id
        )

    context_target = _resolve_log_stream_from_cached_context()
    if context_target is not None:
        return AgentControlTarget(
            target_type=context_target.target_type,
            target_id=context_target.target_id,
            project_id=explicit_project_id or context_target.project_id or env_project_id,
        )

    raise AgentControlTargetUnresolvedError(
        "Could not resolve Galileo log stream ID for Agent Control. Provide one of:\n"
        "  1. target_id=<uuid> or log_stream_id=<uuid> argument\n"
        "  2. GALILEO_LOG_STREAM_ID environment variable\n"
        "  3. An initialized galileo_context with a resolved log stream ID"
    )


def _validate_uuid(value: str, source: str) -> None:
    try:
        UUID(value)
    except (AttributeError, TypeError, ValueError) as exc:
        raise AgentControlTargetUnresolvedError(f"{source}={value!r} is not a valid UUID.") from exc


def _strip_optional_string(value: str | None) -> str | None:
    if value is None:
        return None
    return value.strip()


def _resolve_log_stream_from_cached_context() -> AgentControlTarget | None:
    current_project = _get_project_or_default(galileo_context.get_current_project())
    current_log_stream = _get_log_stream_or_default(galileo_context.get_current_log_stream())
    current_thread_name = threading.current_thread().name

    # Read cached logger state directly so this helper never creates or resolves
    # projects/log streams as a side effect of building an Agent Control target.
    # Use the same default/env fallback as GalileoLogger so callers that rely on
    # default project/log-stream creation can still reuse the resolved IDs.
    for key, logger in GalileoLoggerSingleton().get_all_loggers().items():
        if not key or key[0] != current_thread_name:
            continue
        if logger.project_name != current_project or logger.log_stream_name != current_log_stream:
            continue
        if logger.log_stream_id is None:
            continue
        return AgentControlTarget(
            target_type=LOG_STREAM_TARGET_TYPE, target_id=logger.log_stream_id, project_id=logger.project_id
        )

    return None


__all__ = ["AgentControlTarget", "AgentControlTargetUnresolvedError", "get_agent_control_target"]
