import datetime
from contextlib import contextmanager
from typing import Any, Callable, Optional
from unittest.mock import AsyncMock, Mock
from uuid import UUID

from galileo.experiments import Experiments
from galileo.log_streams import LogStream
from galileo.logger.logger import GalileoLogger
from galileo.projects import Project
from galileo.resources.models import ExperimentResponse, ProjectType
from galileo.resources.models.log_stream_response import LogStreamResponse
from galileo.resources.models.project_create_response import ProjectCreateResponse
from galileo.resources.models.task_type import TaskType


class ThreadPoolRequestCapture:
    """Helper class to capture requests submitted to the thread pool in streaming methods."""

    def __init__(self):
        self.captured_requests: list[Any] = []
        self.capture_count = 0
        self.mock_pool = None

    def capture_request(self, task_func: Callable, **kwargs) -> None:
        """Capture function that extracts requests from lambda closures."""
        self.capture_count += 1

        # Extract the request from the lambda's closure

        # Look for different types of request objects in the closure

        if task_func.__closure__:
            for cell in task_func.__closure__:
                cell_content = cell.cell_contents

                # Check if this is a request object by looking for common attributes
                if (
                    hasattr(cell_content, "traces")
                    or hasattr(cell_content, "spans")
                    or hasattr(cell_content, "trace_id")
                    or hasattr(cell_content, "span_id")
                ):
                    self.captured_requests.append(cell_content)
                    break

    def get_latest_request(self) -> Optional[Any]:
        """Get the most recently captured request."""
        return self.captured_requests[-1] if self.captured_requests else None

    def get_all_requests(self) -> list[Any]:
        """Get all captured requests."""
        return self.captured_requests.copy()

    def clear(self) -> None:
        """Clear all captured requests."""
        self.captured_requests.clear()
        self.capture_count = 0


def setup_thread_pool_request_capture(logger: GalileoLogger) -> ThreadPoolRequestCapture:
    """
    Set up request capture for a logger's thread pool.

    Args:
        logger: GalileoLogger instance to mock the thread pool for

    Returns:
        ThreadPoolRequestCapture instance that can be used to inspect captured requests
    """
    capture = ThreadPoolRequestCapture()
    mock_pool = Mock(side_effect=capture.capture_request)
    logger._pool.submit = mock_pool
    capture.mock_pool = mock_pool
    return capture


@contextmanager
def capture_streaming_requests(logger):
    """
    Context manager for capturing streaming requests.

    Usage:
        with capture_streaming_requests(logger) as capture:
            logger._ingest_trace_streaming(trace)
            request = capture.get_latest_request()
            assert isinstance(request, TracesIngestRequest)
    """
    capture = setup_thread_pool_request_capture(logger)
    try:
        yield capture
    finally:
        capture.clear()


def setup_mock_projects_client(mock_projects_client: Mock):
    now = datetime.datetime.now()
    mock_instance = mock_projects_client.return_value
    mock_instance.get = Mock(
        return_value=Project(
            ProjectCreateResponse(
                id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                type_=ProjectType.GEN_AI,
                name="test",
                created_at=now,
                updated_at=now,
            )
        )
    )
    mock_instance.create = Mock(
        return_value=Project(
            ProjectCreateResponse(
                id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                type_=ProjectType.GEN_AI,
                name="test",
                created_at=now,
                updated_at=now,
            )
        )
    )
    return mock_instance


def setup_mock_logstreams_client(mock_logstreams_client: Mock):
    now = datetime.datetime.now()
    mock_instance = mock_logstreams_client.return_value
    mock_instance.get = Mock(
        return_value=LogStream(
            LogStreamResponse(
                id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9b",
                project_id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                name="test",
                created_at=now,
                updated_at=now,
            )
        )
    )
    mock_instance.create = Mock(
        return_value=LogStream(
            LogStreamResponse(
                id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9b",
                project_id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                name="test",
                created_at=now,
                updated_at=now,
            )
        )
    )
    return mock_instance


def setup_mock_experiments_client(mock_experiment_client: Mock):
    now = datetime.datetime.now()
    mock_instance = mock_experiment_client.return_value
    mock_instance.get = Mock(
        return_value=Experiments(
            ExperimentResponse(
                id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                project_id="6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a",
                name="test",
                created_at=now,
                updated_at=now,
                task_type=TaskType.VALUE_16,
            )
        )
    )
    return mock_instance


def setup_mock_core_api_client(mock_core_api_client: Mock):
    mock_instance = mock_core_api_client.return_value
    mock_instance.get_project_by_name = Mock(return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a")})
    mock_instance.get_log_stream_by_name = Mock(return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9b")})
    mock_instance.ingest_traces_sync = Mock(return_value={})
    mock_instance.ingest_traces = AsyncMock(return_value={})
    mock_instance.ingest_spans = AsyncMock(return_value={})
    mock_instance.ingest_spans_sync = Mock(return_value={})
    mock_instance.update_trace = AsyncMock(return_value={})
    mock_instance.update_trace_sync = Mock(return_value={})
    mock_instance.update_span = AsyncMock(return_value={})
    mock_instance.update_span_sync = Mock(return_value={})
    mock_instance.create_session_sync = Mock(
        return_value={
            "id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9c"),
            "name": "test",
            "previous_session_id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9e"),
            "external_id": "test",
            "project_id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a"),
            "project_name": "test project",
            "log_stream_id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9b"),
        }
    )
    mock_instance.get_sessions_sync = Mock(
        return_value={"starting_token": 0, "limit": 100, "paginated": False, "records": [], "num_records": 0}
    )

    return mock_instance
