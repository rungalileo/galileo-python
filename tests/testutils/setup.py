import copy
import datetime
from contextlib import contextmanager
from typing import Any, Callable, Optional
from unittest.mock import AsyncMock, Mock
from uuid import UUID

from pydantic import BaseModel

from galileo.experiments import Experiments
from galileo.log_streams import LogStream
from galileo.logger.logger import GalileoLogger
from galileo.projects import Project
from galileo.resources.models import ExperimentResponse, ProjectType
from galileo.resources.models.log_stream_response import LogStreamResponse
from galileo.resources.models.project_create_response import ProjectCreateResponse
from galileo.resources.models.task_type import TaskType


class ThreadPoolTaskInfo(BaseModel):
    task_id: str
    function_name: str
    request: Any
    task_func: Callable
    kwargs: dict


class ThreadPoolRequestCapture:
    """Helper class to capture requests submitted to the thread pool in streaming methods."""

    def __init__(self):
        self.captured_tasks: list[ThreadPoolTaskInfo] = []
        self.mock_pool = None

    def capture_request(self, task_id: str, async_fn: Callable, **kwargs) -> None:
        """Capture function that extracts requests and function names from ThreadPoolTaskHandler.submit_task calls."""

        # Extract both the request and function from the lambda
        captured_request = None
        captured_function_name = None
        captured_function = None

        # Get the first function name referenced in the lambda
        # Since lambdas follow pattern: lambda: function_name(request)
        code = async_fn.__code__

        if code.co_names:
            # The first (and typically only) name in co_names is our function
            captured_function_name = code.co_names[0]

        # Extract request from closure and also look for callable functions
        if async_fn.__closure__:
            for cell in async_fn.__closure__:
                cell_content = cell.cell_contents

                # Check for request object
                if isinstance(cell_content, BaseModel):
                    captured_request = copy.deepcopy(cell_content)

                # Check for callable function (if we didn't get function name from co_names)
                elif captured_function_name is None and callable(cell_content) and hasattr(cell_content, "__name__"):
                    captured_function_name = cell_content.__name__
                    captured_function = cell_content

                # If we have function name but not function reference, look for it
                elif (
                    captured_function_name
                    and callable(cell_content)
                    and hasattr(cell_content, "__name__")
                    and cell_content.__name__ == captured_function_name
                ):
                    captured_function = cell_content

        # Create a new lambda that uses the deep-copied request to avoid mutation issues
        if captured_function and captured_request:

            def isolated_task_func():
                return captured_function(captured_request)
        else:
            isolated_task_func = async_fn

        task_info = ThreadPoolTaskInfo(
            task_id=task_id,
            function_name=captured_function_name,
            request=captured_request,
            task_func=isolated_task_func,
            kwargs=kwargs,
        )
        self.captured_tasks.append(task_info)

    def get_request_by_function_name(self, function_name: str) -> Optional[Any]:
        return next((task.request for task in self.captured_tasks if task.function_name == function_name), None)

    def get_latest_task(self) -> Optional[ThreadPoolTaskInfo]:
        """Get the most recent task info (request + function name)."""
        return self.captured_tasks[-1] if self.captured_tasks else None

    def get_all_tasks(self) -> list[ThreadPoolTaskInfo]:
        """
        Get all captured tasks.

        Returns:
            list[ThreadPoolTaskInfo]: List of captured tasks.
        """
        return self.captured_tasks

    def get_all_requests(self) -> list[Any]:
        """Get all captured requests."""
        return [task.request for task in self.captured_tasks]

    def get_all_function_names(self) -> list[str]:
        """Get all captured function names."""
        return [task.function_name for task in self.captured_tasks]

    def get_task_by_function_name(self, function_name: str) -> Optional[ThreadPoolTaskInfo]:
        """Get the first task info that matches the given function name.

        Args:
            function_name (str): The name of the function to search for.

        Returns:
            Optional[ThreadPoolTaskInfo]: The first task info that matches the given function name, or None if no match is found.
        """
        return next((task for task in self.captured_tasks if task.function_name == function_name), None)

    def count_function_calls(self, function_name: str) -> int:
        """Count how many times a particular function was called."""
        functions = self.get_all_function_names()
        return sum(1 for func_name in functions if func_name == function_name)

    def clear(self) -> None:
        """Clear all captured tasks."""
        self.captured_tasks.clear()

    def assert_function_called(self, expected_function_name: str) -> None:
        """Assert that the latest captured function matches the expected name."""
        assert expected_function_name in self.get_all_function_names(), (
            f"Expected function '{expected_function_name}' not in '{self.get_all_function_names()}'"
        )

    def assert_functions_called(self, expected_function_names: list[str]) -> None:
        """Assert that the captured functions match the expected sequence."""
        actual_functions = self.get_all_function_names()
        assert actual_functions == expected_function_names, (
            f"Expected functions {expected_function_names}, but got {actual_functions}"
        )


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
    logger._task_handler.submit_task = mock_pool
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
    now = datetime.datetime.now()
    mock_instance = mock_core_api_client.return_value
    mock_instance.get_project_by_name = Mock(return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9a")})
    mock_instance.get_log_stream_by_name = Mock(return_value={"id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9b")})
    mock_instance.ingest_traces = AsyncMock(return_value={})
    mock_instance.ingest_spans = AsyncMock(return_value={})
    mock_instance.update_trace = AsyncMock(return_value={})
    mock_instance.update_span = AsyncMock(return_value={})
    mock_instance.create_session = AsyncMock(
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
    mock_instance.get_sessions = AsyncMock(
        return_value={"starting_token": 0, "limit": 100, "paginated": False, "records": [], "num_records": 0}
    )
    mock_instance.get_trace_sync = Mock(
        return_value={
            "id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9d"),
            "name": "test-trace",
            "type": "trace",
            "input": "test-input",
            "output": None,
            "created_at": now,
            "updated_at": now,
            "user_metadata": {},
            "spans": [],
            "metrics": {},
        }
    )
    mock_instance.get_span_sync = Mock(
        return_value={
            "id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9e"),
            "name": "test-workflow-span",
            "type": "workflow",
            "input": "test-input",
            "output": None,
            "created_at": now,
            "updated_at": now,
            "user_metadata": {},
            "metrics": {},
            "parent_id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9d"),
            "trace_id": UUID("6c4e3f7e-4a9a-4e7e-8c1f-3a9a3a9a3a9d"),
        }
    )

    return mock_instance
