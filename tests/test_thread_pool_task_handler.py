from concurrent.futures import Future
from unittest.mock import Mock, patch

import pytest
from src.galileo.logger.task_handler import ThreadPoolTaskHandler


class TestThreadPoolTaskHandler:
    """Test suite for ThreadPoolTaskHandler class."""

    @pytest.fixture
    def mock_pool(self):
        """Mock EventLoopThreadPool."""
        with patch("src.galileo.logger.task_handler.EventLoopThreadPool") as mock_pool_class:
            mock_pool = Mock()
            mock_pool_class.return_value = mock_pool
            yield mock_pool

    @pytest.fixture
    def handler(self, mock_pool):
        """Create ThreadPoolTaskHandler instance with mocked pool."""
        return ThreadPoolTaskHandler(num_threads=2)

    @pytest.fixture
    def mock_future(self):
        """Create a mock Future object."""
        future = Mock(spec=Future)
        future.done.return_value = False
        future.result.return_value = "test_result"
        future.add_done_callback = Mock()
        return future

    async def dummy_async_func(self) -> str:
        """Dummy async function for testing."""
        return "async_result"

    def test_init(self, mock_pool) -> None:
        """Test ThreadPoolTaskHandler initialization."""
        handler = ThreadPoolTaskHandler(num_threads=4)
        assert handler._tasks == {}
        assert handler._retry_counts == {}
        assert handler._pool is not None

    def test_submit_task_independent(self, handler, mock_pool, mock_future) -> None:
        """Test submitting an independent task (dependent_on_prev=False)."""
        mock_pool.submit.return_value = mock_future

        async_fn = self.dummy_async_func
        task_id = "test_task_1"

        handler.submit_task(task_id, async_fn, dependent_on_prev=False)

        # Verify task was submitted to pool
        mock_pool.submit.assert_called_once_with(async_fn, wait_for_result=False)

        # Verify done callback was added
        mock_future.add_done_callback.assert_called_once()

        # Verify task was tracked
        assert task_id in handler._tasks
        assert handler._tasks[task_id]["future"] == mock_future
        assert handler._tasks[task_id]["parent_task_id"] is None
        assert handler._retry_counts[task_id] == 0

    def test_submit_task_dependent_no_previous(self, handler, mock_pool, mock_future) -> None:
        """Test submitting a dependent task when no previous task exists."""
        mock_pool.submit.return_value = mock_future

        async_fn = self.dummy_async_func
        task_id = "test_task_1"

        handler.submit_task(task_id, async_fn, dependent_on_prev=True)

        # Should submit immediately since no previous task exists
        mock_pool.submit.assert_called_once_with(async_fn, wait_for_result=False)
        assert task_id in handler._tasks
        assert handler._tasks[task_id]["future"] == mock_future
        assert handler._tasks[task_id]["parent_task_id"] is None  # No parent since no previous tasks

    def test_submit_task_dependent_previous_completed(self, handler, mock_pool, mock_future) -> None:
        """Test submitting a dependent task when previous task is completed."""
        # Set up first task
        mock_pool.submit.return_value = mock_future
        first_task_id = "task_1"
        handler.submit_task(first_task_id, self.dummy_async_func, dependent_on_prev=False)

        # Mock the first task as completed
        with patch.object(handler, "get_status", return_value="completed"):
            second_mock_future = Mock(spec=Future)
            mock_pool.submit.return_value = second_mock_future

            second_task_id = "task_2"
            handler.submit_task(second_task_id, self.dummy_async_func, dependent_on_prev=True)

            # Should submit immediately since previous task is completed
            assert mock_pool.submit.call_count == 2
            assert second_task_id in handler._tasks
            assert handler._tasks[second_task_id]["future"] == second_mock_future

    def test_submit_task_dependent_previous_running(self, handler, mock_pool, mock_future) -> None:
        """Test submitting a dependent task when previous task is still running."""
        # Set up first task
        mock_pool.submit.return_value = mock_future
        first_task_id = "task_1"
        handler.submit_task(first_task_id, self.dummy_async_func, dependent_on_prev=False)

        # Mock the first task as still running
        with patch.object(handler, "get_status", return_value="running"):
            second_task_id = "task_2"
            handler.submit_task(second_task_id, self.dummy_async_func, dependent_on_prev=True)

            # Should not submit yet, but should be tracked as pending
            assert mock_pool.submit.call_count == 1  # Only first task submitted
            assert second_task_id in handler._tasks
            assert handler._tasks[second_task_id]["future"] is None
            assert handler._tasks[second_task_id]["parent_task_id"] == first_task_id
            assert handler._tasks[second_task_id]["callback"] is not None

    def test_handle_task_completion_triggers_children(self, handler, mock_pool) -> None:
        """Test that task completion triggers child tasks."""
        # Set up parent task
        parent_future = Mock(spec=Future)
        mock_pool.submit.return_value = parent_future
        parent_task_id = "parent_task"
        handler.submit_task(parent_task_id, self.dummy_async_func, dependent_on_prev=False)

        # Set up child task (dependent)
        with patch.object(handler, "get_status", return_value="running"):
            child_task_id = "child_task"
            handler.submit_task(child_task_id, self.dummy_async_func, dependent_on_prev=True)

        # Mock child task submission
        child_future = Mock(spec=Future)
        mock_pool.submit.return_value = child_future

        # Trigger parent task completion
        handler._handle_task_completion(parent_task_id)

        # Verify child task was submitted
        assert mock_pool.submit.call_count == 2  # Parent + child
        assert handler._tasks[child_task_id]["future"] == child_future

    def test_increment_retry(self, handler) -> None:
        """Test retry count increment."""
        task_id = "test_task"

        # Initially 0
        assert handler.get_retry_count(task_id) == 0

        # Increment retry
        handler.increment_retry(task_id)
        assert handler.get_retry_count(task_id) == 1

        # Increment again
        handler.increment_retry(task_id)
        assert handler.get_retry_count(task_id) == 2

    def test_get_status_not_found(self, handler) -> None:
        """Test get_status for non-existent task."""
        assert handler.get_status("non_existent") == "not_found"

    def test_get_status_pending(self, handler, mock_pool, mock_future) -> None:
        """Test get_status for pending task."""
        # Set up parent task
        mock_pool.submit.return_value = mock_future
        parent_task_id = "parent"
        handler.submit_task(parent_task_id, self.dummy_async_func, dependent_on_prev=False)

        # Set up child task as pending
        with patch.object(
            handler, "get_status", side_effect=lambda tid: "running" if tid == parent_task_id else "pending"
        ):
            child_task_id = "child"
            handler.submit_task(child_task_id, self.dummy_async_func, dependent_on_prev=True)

            # Reset side_effect and test actual status
            handler.get_status = handler.__class__.get_status.__get__(handler)
            assert handler.get_status(child_task_id) == "pending"

    def test_get_status_running(self, handler, mock_pool, mock_future) -> None:
        """Test get_status for running task."""
        mock_pool.submit.return_value = mock_future
        mock_future.done.return_value = False

        task_id = "running_task"
        handler.submit_task(task_id, self.dummy_async_func, dependent_on_prev=False)

        assert handler.get_status(task_id) == "running"

    def test_get_status_completed(self, handler, mock_pool, mock_future) -> None:
        """Test get_status for completed task."""
        mock_pool.submit.return_value = mock_future
        mock_future.done.return_value = True
        mock_future.result.return_value = "success"

        task_id = "completed_task"
        handler.submit_task(task_id, self.dummy_async_func, dependent_on_prev=False)

        assert handler.get_status(task_id) == "completed"

    def test_get_status_failed(self, handler, mock_pool, mock_future) -> None:
        """Test get_status for failed task."""
        mock_pool.submit.return_value = mock_future
        mock_future.done.return_value = True
        mock_future.result.side_effect = Exception("Task failed")

        task_id = "failed_task"
        handler.submit_task(task_id, self.dummy_async_func, dependent_on_prev=False)

        assert handler.get_status(task_id) == "failed"

    def test_get_result(self, handler, mock_pool, mock_future) -> None:
        """Test getting task result."""
        mock_pool.submit.return_value = mock_future
        expected_result = "test_result"
        mock_future.result.return_value = expected_result

        task_id = "test_task"
        handler.submit_task(task_id, self.dummy_async_func, dependent_on_prev=False)

        result = handler.get_result(task_id)
        assert result == expected_result

    def test_get_result_not_found(self, handler) -> None:
        """Test getting result for non-existent task."""
        with pytest.raises(ValueError, match="Task non_existent not found"):
            handler.get_result("non_existent")

    def test_get_children(self, handler, mock_pool, mock_future) -> None:
        """Test getting child tasks."""
        # Set up parent task
        mock_pool.submit.return_value = mock_future
        parent_task_id = "parent"
        handler.submit_task(parent_task_id, self.dummy_async_func, dependent_on_prev=False)

        # Manually add two child tasks that depend on the parent
        # (This simulates what would happen if we had a more complex dependency system)
        def child1_callback():
            return handler._pool.submit(self.dummy_async_func, wait_for_result=False)

        def child2_callback():
            return handler._pool.submit(self.dummy_async_func, wait_for_result=False)

        handler._add_or_update_task(
            task_id="child1", future=None, start_time=None, parent_task_id=parent_task_id, callback=child1_callback
        )

        handler._add_or_update_task(
            task_id="child2", future=None, start_time=None, parent_task_id=parent_task_id, callback=child2_callback
        )

        children = handler.get_children(parent_task_id)
        assert len(children) == 2

        # Verify both children have the correct parent_task_id
        child_task_ids = [
            task_id for task_id, task in handler._tasks.items() if task.get("parent_task_id") == parent_task_id
        ]
        assert len(child_task_ids) == 2
        assert "child1" in child_task_ids
        assert "child2" in child_task_ids

    def test_all_tasks_completed_empty(self, handler) -> None:
        """Test all_tasks_completed with no tasks."""
        assert handler.all_tasks_completed() is True

    def test_all_tasks_completed_true(self, handler, mock_pool, mock_future) -> None:
        """Test all_tasks_completed when all tasks are done."""
        mock_pool.submit.return_value = mock_future

        with patch.object(handler, "get_status", return_value="completed"):
            handler.submit_task("task1", self.dummy_async_func, dependent_on_prev=False)
            handler.submit_task("task2", self.dummy_async_func, dependent_on_prev=False)

            assert handler.all_tasks_completed() is True

    def test_all_tasks_completed_false(self, handler, mock_pool, mock_future) -> None:
        """Test all_tasks_completed when some tasks are still running."""
        mock_pool.submit.return_value = mock_future

        def mock_status(task_id) -> str:
            return "completed" if task_id == "task1" else "running"

        with patch.object(handler, "get_status", side_effect=mock_status):
            handler.submit_task("task1", self.dummy_async_func, dependent_on_prev=False)
            handler.submit_task("task2", self.dummy_async_func, dependent_on_prev=False)

            assert handler.all_tasks_completed() is False

    def test_terminate(self, handler, mock_pool) -> None:
        """Test handler termination."""
        handler.terminate()
        mock_pool.stop.assert_called_once()

    def test_complex_dependency_chain(self, handler, mock_pool) -> None:
        """Test a complex chain of dependent tasks."""
        # Create multiple futures for different tasks
        futures = [Mock(spec=Future) for _ in range(4)]
        future_index = 0

        def get_next_future(*args, **kwargs):
            nonlocal future_index
            future = futures[future_index]
            future_index += 1
            return future

        mock_pool.submit.side_effect = get_next_future

        # Submit task chain: A -> B -> C -> D
        task_ids = ["task_A", "task_B", "task_C", "task_D"]

        # Submit first task (independent)
        handler.submit_task(task_ids[0], self.dummy_async_func, dependent_on_prev=False)

        # Submit dependent tasks
        for i in range(1, len(task_ids)):
            with patch.object(handler, "get_status", return_value="running"):
                handler.submit_task(task_ids[i], self.dummy_async_func, dependent_on_prev=True)

        # Verify only first task was submitted initially
        assert mock_pool.submit.call_count == 1

        # Simulate completion of each task in sequence
        for i in range(len(task_ids) - 1):
            # Mock the current task as completed for next submission
            mock_pool.submit.side_effect = get_next_future
            handler._handle_task_completion(task_ids[i])

            # Verify next task was submitted
            expected_calls = i + 2  # +1 for initial task, +1 for current completion
            assert mock_pool.submit.call_count == expected_calls

    def test_done_callback_integration(self, handler, mock_pool) -> None:
        """Test that the done callback properly triggers task completion handling."""
        mock_future = Mock(spec=Future)
        mock_pool.submit.return_value = mock_future

        task_id = "callback_test"
        handler.submit_task(task_id, self.dummy_async_func, dependent_on_prev=False)

        # Get the callback that was registered
        callback_calls = mock_future.add_done_callback.call_args_list
        assert len(callback_calls) == 1
        registered_callback = callback_calls[0][0][0]

        # Mock _handle_task_completion to verify it's called
        with patch.object(handler, "_handle_task_completion") as mock_handle:
            # Trigger the callback
            registered_callback(mock_future)

            # Verify _handle_task_completion was called with correct task_id
            mock_handle.assert_called_once_with(task_id)
