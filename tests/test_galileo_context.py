from unittest.mock import Mock, patch

import pytest

from galileo import splunk_ao_context
from galileo.decorator import _experiment_id_context, _log_stream_context, _project_context
from tests.testutils.setup import setup_mock_logstreams_client, setup_mock_projects_client, setup_mock_traces_client


@pytest.fixture
def reset_context() -> None:
    splunk_ao_context.reset()


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_nested_context_restoration(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """
    Test that nested splunk_ao_context calls correctly restore the previous context.
    This tests the stack-based approach for context nesting.
    """
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # Initial context values should be None
    assert _project_context.get() is None
    assert _log_stream_context.get() is None
    assert _experiment_id_context.get() is None

    # First level context
    with splunk_ao_context(project="project1", log_stream="log_stream1"):
        assert _project_context.get() == "project1"
        assert _log_stream_context.get() == "log_stream1"
        assert _experiment_id_context.get() is None

        # Second level context
        with splunk_ao_context(project="project2", log_stream="log_stream2"):
            assert _project_context.get() == "project2"
            assert _log_stream_context.get() == "log_stream2"
            assert _experiment_id_context.get() is None

            # Third level context
            with splunk_ao_context(project="project3", log_stream="log_stream3"):
                assert _project_context.get() == "project3"
                assert _log_stream_context.get() == "log_stream3"
                assert _experiment_id_context.get() is None

            # After exiting third level, should be back to second level
            assert _project_context.get() == "project2"
            assert _log_stream_context.get() == "log_stream2"
            assert _experiment_id_context.get() is None

        # After exiting second level, should be back to first level
        assert _project_context.get() == "project1"
        assert _log_stream_context.get() == "log_stream1"
        assert _experiment_id_context.get() is None

    # After exiting first level, should be back to None
    assert _project_context.get() is None
    assert _log_stream_context.get() is None
    assert _experiment_id_context.get() is None


@patch("galileo.logger.logger.LogStreams")
@patch("galileo.logger.logger.Projects")
@patch("galileo.logger.logger.Traces")
def test_context_update_with_defaults(
    mock_traces_client: Mock, mock_projects_client: Mock, mock_logstreams_client: Mock, reset_context
) -> None:
    """
    Test that updating only some context values in nested contexts works correctly.
    This tests that we only update the specified values and keep the rest from the parent context.
    """
    setup_mock_traces_client(mock_traces_client)
    setup_mock_projects_client(mock_projects_client)
    setup_mock_logstreams_client(mock_logstreams_client)

    # First level context with project and log_stream
    with splunk_ao_context(project="project1", log_stream="log_stream1"):
        assert _project_context.get() == "project1"
        assert _log_stream_context.get() == "log_stream1"
        assert _experiment_id_context.get() is None

        # Second level context with only project updated; log_stream should be default
        with splunk_ao_context(project="project2"):
            assert _project_context.get() == "project2"
            assert _log_stream_context.get() is None  # use env default
            assert _experiment_id_context.get() is None

            # Third level context with no params: should use defaults
            with splunk_ao_context():
                assert _project_context.get() is None
                assert _log_stream_context.get() is None
                assert _experiment_id_context.get() is None

            # After exiting third level, should restore second level context with default log_stream
            assert _project_context.get() == "project2"
            assert _log_stream_context.get() is None
            assert _experiment_id_context.get() is None

        # After exiting second level, should be back to first level
        assert _project_context.get() == "project1"
        assert _log_stream_context.get() == "log_stream1"
        assert _experiment_id_context.get() is None

    # After exiting first level, should be back to None
    assert _project_context.get() is None
    assert _log_stream_context.get() is None
    assert _experiment_id_context.get() is None
