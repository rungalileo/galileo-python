import threading
from types import SimpleNamespace
from uuid import uuid4

import pytest

from galileo import AgentControlTarget, AgentControlTargetUnresolvedError, get_agent_control_target
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
    monkeypatch.setattr(GalileoLoggerSingleton, "get_all_loggers", lambda self: {})
    monkeypatch.setattr(
        galileo_context, "get_logger_instance", lambda *args, **kwargs: SimpleNamespace(flush=lambda: None)
    )
    galileo_context.reset()

    yield

    # Then: context and singleton state are restored for following tests
    galileo_context.reset()


def _stub_cached_logger(monkeypatch, logger: SimpleNamespace) -> None:
    key = (threading.current_thread().name, "batch", logger.project_name, logger.log_stream_name)
    monkeypatch.setattr(GalileoLoggerSingleton, "get_all_loggers", lambda self: {key: logger})


def _stub_cached_loggers(monkeypatch, loggers: dict[tuple[str, ...], SimpleNamespace]) -> None:
    monkeypatch.setattr(GalileoLoggerSingleton, "get_all_loggers", lambda self: loggers)


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


def test_get_agent_control_target_strips_env_ids(monkeypatch) -> None:
    # Given: Galileo ID environment values with accidental surrounding whitespace
    log_stream_id = str(uuid4())
    project_id = str(uuid4())
    monkeypatch.setenv("GALILEO_LOG_STREAM_ID", f"  {log_stream_id}  ")
    monkeypatch.setenv("GALILEO_PROJECT_ID", f"  {project_id}  ")

    # When: resolving an Agent Control target
    target = get_agent_control_target()

    # Then: the returned IDs are normalized before validation and use
    assert target == AgentControlTarget(target_type="log_stream", target_id=log_stream_id, project_id=project_id)


def test_get_agent_control_target_strips_explicit_log_stream_target_id() -> None:
    # Given: an explicit Galileo log stream target ID with accidental whitespace
    log_stream_id = str(uuid4())

    # When: resolving an Agent Control target
    target = get_agent_control_target(target_id=f"  {log_stream_id}  ")

    # Then: the explicit target ID is normalized before validation and use
    assert target == AgentControlTarget(target_type="log_stream", target_id=log_stream_id)


def test_get_agent_control_target_uses_cached_context_logger(monkeypatch) -> None:
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
    _stub_cached_logger(monkeypatch, logger)

    # When: resolving an Agent Control target
    with galileo_context(project="project-a", log_stream="stream-a"):
        target = get_agent_control_target()

    # Then: the helper reads the resolved IDs without creating a new logger
    assert target == AgentControlTarget(target_type="log_stream", target_id=log_stream_id, project_id=project_id)


def test_get_agent_control_target_uses_cached_default_logger(monkeypatch) -> None:
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
    _stub_cached_logger(monkeypatch, logger)

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
    _stub_cached_logger(monkeypatch, logger)

    # When: resolving an Agent Control target without explicit context names
    target = get_agent_control_target()

    # Then: the helper follows Galileo's env fallback and reuses the resolved ID
    assert target == AgentControlTarget(target_type="log_stream", target_id=log_stream_id, project_id=project_id)


def test_get_agent_control_target_ignores_cached_logger_from_other_thread(monkeypatch) -> None:
    # Given: a cached logger for the same default target but from another thread
    logger = SimpleNamespace(
        project_name=DEFAULT_PROJECT_NAME,
        log_stream_name=DEFAULT_LOG_STREAM_NAME,
        project_id=str(uuid4()),
        log_stream_id=str(uuid4()),
        terminate=lambda: None,
    )
    _stub_cached_loggers(
        monkeypatch, {("other-thread", "batch", DEFAULT_PROJECT_NAME, DEFAULT_LOG_STREAM_NAME): logger}
    )

    # When/Then: resolving the target does not use another thread's logger
    with pytest.raises(AgentControlTargetUnresolvedError, match="Could not resolve Galileo log stream ID"):
        get_agent_control_target()


def test_get_agent_control_target_prefers_cached_logger_project_id_over_env(monkeypatch) -> None:
    # Given: env project ID is stale but the cached logger has the resolved project ID
    cached_project_id = str(uuid4())
    env_project_id = str(uuid4())
    log_stream_id = str(uuid4())
    monkeypatch.setenv("GALILEO_PROJECT_ID", env_project_id)
    logger = SimpleNamespace(
        project_name=DEFAULT_PROJECT_NAME,
        log_stream_name=DEFAULT_LOG_STREAM_NAME,
        project_id=cached_project_id,
        log_stream_id=log_stream_id,
        terminate=lambda: None,
    )
    _stub_cached_logger(monkeypatch, logger)

    # When: resolving from cached logger state
    target = get_agent_control_target()

    # Then: the informational project ID matches the resolved log stream
    assert target == AgentControlTarget(target_type="log_stream", target_id=log_stream_id, project_id=cached_project_id)


def test_get_agent_control_target_uses_explicit_project_id_with_cached_logger(monkeypatch) -> None:
    # Given: a caller explicitly overrides the informational project ID
    cached_project_id = str(uuid4())
    explicit_project_id = str(uuid4())
    log_stream_id = str(uuid4())
    logger = SimpleNamespace(
        project_name=DEFAULT_PROJECT_NAME,
        log_stream_name=DEFAULT_LOG_STREAM_NAME,
        project_id=cached_project_id,
        log_stream_id=log_stream_id,
        terminate=lambda: None,
    )
    _stub_cached_logger(monkeypatch, logger)

    # When: resolving from cached logger state with an explicit project ID
    target = get_agent_control_target(project_id=explicit_project_id)

    # Then: explicit input wins over the cached informational project ID
    assert target == AgentControlTarget(
        target_type="log_stream", target_id=log_stream_id, project_id=explicit_project_id
    )


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
    with pytest.raises(AgentControlTargetUnresolvedError, match="target_id='prod' is not a valid UUID"):
        get_agent_control_target(target_id="prod")


def test_get_agent_control_target_rejects_missing_future_target_id() -> None:
    # Given: a non-log-stream target type without an explicit target ID

    # When/Then: resolving the target fails with an actionable error
    with pytest.raises(AgentControlTargetUnresolvedError, match="Provide target_id=<id> explicitly"):
        get_agent_control_target(target_type="agent")


def test_get_agent_control_target_rejects_conflicting_ids() -> None:
    # Given: conflicting target ID inputs

    # When/Then: resolving the target fails before choosing one arbitrarily
    with pytest.raises(AgentControlTargetUnresolvedError, match="target_id and log_stream_id must match"):
        get_agent_control_target(target_id=str(uuid4()), log_stream_id=str(uuid4()))


def test_get_agent_control_target_errors_when_unresolved() -> None:
    # Given: no explicit ID, env ID, or cached context logger

    # When/Then: resolving the target fails with the supported resolution options
    with pytest.raises(AgentControlTargetUnresolvedError, match="Could not resolve Galileo log stream ID"):
        get_agent_control_target()
