from types import SimpleNamespace
from uuid import uuid4

import pytest

from galileo import AgentControlTarget, AgentControlTargetUnresolvedError, get_agent_control_target, get_log_stream_id
from galileo.constants import DEFAULT_LOG_STREAM_NAME, DEFAULT_PROJECT_NAME
from galileo.decorator import galileo_context
from galileo.utils.singleton import GalileoLoggerSingleton


@pytest.fixture(autouse=True)
def reset_agent_control_helper_state(monkeypatch):
    # Given: no log stream ID environment override or cached logger state
    monkeypatch.delenv("GALILEO_PROJECT", raising=False)
    monkeypatch.delenv("GALILEO_LOG_STREAM", raising=False)
    monkeypatch.delenv("GALILEO_LOG_STREAM_ID", raising=False)
    monkeypatch.delenv("GALILEO_PROJECT_ID", raising=False)
    singleton = GalileoLoggerSingleton()
    original_loggers = singleton._galileo_loggers
    singleton._galileo_loggers = {}
    galileo_context.reset()

    yield

    # Then: context and singleton state are restored for following tests
    galileo_context.reset()
    singleton._galileo_loggers = original_loggers


def test_get_agent_control_target_uses_explicit_log_stream_id() -> None:
    # Given: an explicit Galileo log stream ID
    log_stream_id = str(uuid4())

    # When: resolving an Agent Control target
    target = get_agent_control_target(log_stream_id=log_stream_id)

    # Then: the target is log-stream scoped
    assert target == AgentControlTarget(target_type="log_stream", target_id=log_stream_id)


def test_get_agent_control_target_uses_env_project_id_with_explicit_log_stream_id(monkeypatch) -> None:
    # Given: an explicit Galileo log stream ID and project ID from the environment
    log_stream_id = str(uuid4())
    project_id = str(uuid4())
    monkeypatch.setenv("GALILEO_PROJECT_ID", project_id)

    # When: resolving an Agent Control target
    target = get_agent_control_target(log_stream_id=log_stream_id)

    # Then: the helper includes the informational project ID consistently
    assert target == AgentControlTarget(target_type="log_stream", target_id=log_stream_id, project_id=project_id)


def test_get_agent_control_target_uses_explicit_future_target() -> None:
    # Given: an explicit non-log-stream Agent Control target
    project_id = str(uuid4())

    # When: resolving the target
    target = get_agent_control_target(target_type="agent", target_id="agent-123", project_id=project_id)

    # Then: the helper packages the target without Galileo log-stream validation
    assert target == AgentControlTarget(target_type="agent", target_id="agent-123", project_id=project_id)


def test_get_agent_control_target_uses_env_log_stream_id(monkeypatch) -> None:
    # Given: a Galileo log stream ID in the environment
    log_stream_id = str(uuid4())
    project_id = str(uuid4())
    monkeypatch.setenv("GALILEO_LOG_STREAM_ID", log_stream_id)
    monkeypatch.setenv("GALILEO_PROJECT_ID", project_id)

    # When: resolving an Agent Control target
    target = get_agent_control_target()

    # Then: the target uses the env-provided IDs
    assert target == AgentControlTarget(target_type="log_stream", target_id=log_stream_id, project_id=project_id)


def test_get_agent_control_target_uses_cached_context_logger() -> None:
    # Given: an active Galileo context with an already-resolved logger
    project_id = str(uuid4())
    log_stream_id = str(uuid4())
    logger = SimpleNamespace(
        project_name="project-a",
        log_stream_name="stream-a",
        project_id=project_id,
        log_stream_id=log_stream_id,
        terminate=lambda: None,
    )
    GalileoLoggerSingleton()._galileo_loggers[("test",)] = logger
    # galileo_context(...) sets ContextVar state before returning the context manager.
    galileo_context(project="project-a", log_stream="stream-a")

    # When: resolving an Agent Control target
    target = get_agent_control_target()

    # Then: the helper reads the resolved IDs without creating a new logger
    assert target == AgentControlTarget(target_type="log_stream", target_id=log_stream_id, project_id=project_id)


def test_get_agent_control_target_uses_cached_default_logger() -> None:
    # Given: Galileo initialized a logger with default project and log-stream names
    project_id = str(uuid4())
    log_stream_id = str(uuid4())
    logger = SimpleNamespace(
        project_name=DEFAULT_PROJECT_NAME,
        log_stream_name=DEFAULT_LOG_STREAM_NAME,
        project_id=project_id,
        log_stream_id=log_stream_id,
        terminate=lambda: None,
    )
    GalileoLoggerSingleton()._galileo_loggers[("test",)] = logger

    # When: resolving an Agent Control target without explicit context names
    target = get_agent_control_target()

    # Then: the helper reuses the default logger's resolved log-stream ID
    assert target == AgentControlTarget(target_type="log_stream", target_id=log_stream_id, project_id=project_id)


def test_get_agent_control_target_uses_cached_env_default_logger(monkeypatch) -> None:
    # Given: Galileo initialized a logger using environment-provided default names
    project_id = str(uuid4())
    log_stream_id = str(uuid4())
    monkeypatch.setenv("GALILEO_PROJECT", "project-env")
    monkeypatch.setenv("GALILEO_LOG_STREAM", "stream-env")
    logger = SimpleNamespace(
        project_name="project-env",
        log_stream_name="stream-env",
        project_id=project_id,
        log_stream_id=log_stream_id,
        terminate=lambda: None,
    )
    GalileoLoggerSingleton()._galileo_loggers[("test",)] = logger

    # When: resolving an Agent Control target without explicit context names
    target = get_agent_control_target()

    # Then: the helper follows Galileo's env fallback and reuses the resolved ID
    assert target == AgentControlTarget(target_type="log_stream", target_id=log_stream_id, project_id=project_id)


def test_get_log_stream_id_returns_resolved_target_id() -> None:
    # Given: an explicit Galileo log stream ID
    log_stream_id = str(uuid4())

    # When: resolving the log stream ID shortcut
    resolved_log_stream_id = get_log_stream_id(log_stream_id=log_stream_id)

    # Then: the shortcut returns the target ID
    assert resolved_log_stream_id == log_stream_id


def test_get_agent_control_target_rejects_invalid_log_stream_id(monkeypatch) -> None:
    # Given: an invalid Galileo log stream ID in the environment
    monkeypatch.setenv("GALILEO_LOG_STREAM_ID", "prod")

    # When/Then: resolving the target fails before sending a malformed target to Agent Control
    with pytest.raises(AgentControlTargetUnresolvedError, match="GALILEO_LOG_STREAM_ID='prod' is not a valid UUID"):
        get_agent_control_target()


def test_get_agent_control_target_rejects_invalid_explicit_log_stream_id() -> None:
    # Given: an invalid explicit Galileo log stream ID

    # When/Then: resolving the target fails before sending a malformed target to Agent Control
    with pytest.raises(AgentControlTargetUnresolvedError, match="log_stream_id='prod' is not a valid UUID"):
        get_agent_control_target(log_stream_id="prod")


def test_get_agent_control_target_rejects_invalid_explicit_log_stream_target_id() -> None:
    # Given: an invalid explicit target ID for the default log-stream target type

    # When/Then: resolving the target fails before sending a malformed target to Agent Control
    with pytest.raises(AgentControlTargetUnresolvedError, match="log_stream_id='prod' is not a valid UUID"):
        get_agent_control_target(target_id="prod")


def test_get_agent_control_target_rejects_missing_future_target_id() -> None:
    # Given: a non-log-stream target type without an explicit target ID

    # When/Then: resolving the target fails with an actionable error
    with pytest.raises(AgentControlTargetUnresolvedError, match="Provide target_id=<id> explicitly"):
        get_agent_control_target(target_type="agent")


def test_get_agent_control_target_rejects_conflicting_ids() -> None:
    # Given: conflicting target ID inputs

    # When/Then: resolving the target fails before choosing one arbitrarily
    with pytest.raises(ValueError, match="target_id and log_stream_id must match"):
        get_agent_control_target(target_id=str(uuid4()), log_stream_id=str(uuid4()))


def test_get_agent_control_target_errors_when_unresolved() -> None:
    # Given: no explicit ID, env ID, or cached context logger

    # When/Then: resolving the target fails with the supported resolution options
    with pytest.raises(AgentControlTargetUnresolvedError, match="Could not resolve Galileo log stream ID"):
        get_agent_control_target()
