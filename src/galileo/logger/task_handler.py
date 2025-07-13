import time
from collections.abc import Awaitable, Coroutine
from concurrent.futures import Future
from typing import Any, Callable, Literal, Optional, Union

from galileo_core.helpers.event_loop_thread_pool import EventLoopThreadPool

NUM_THREADS = 4

TaskStatus = Literal["not_found", "pending", "running", "completed", "failed"]


class ThreadPoolTaskHandler:
    """
    A task handler that manages dependencies and executes tasks in a thread pool.
    """

    _pool: EventLoopThreadPool
    _tasks: dict[str, dict]
    _retry_counts: dict[str, int]

    def __init__(self, num_threads: int = NUM_THREADS):
        self._tasks = {}
        self._retry_counts = {}
        self._pool = EventLoopThreadPool(num_threads=num_threads)

    def _handle_task_completion(self, task_id: str):
        """
        Handle the completion of a task, triggering any children.
        """
        print(f"task completed: {task_id}")
        # Find all child tasks that depend on this task
        for child_task_id, task in list(self._tasks.items()):
            if task.get("parent_task_id") == task_id and task.get("callback"):
                # Execute the callback which will submit the child task
                print(f"triggering child task: {child_task_id}")
                task["callback"]()

    def _add_or_update_task(
        self,
        task_id: str,
        future: Optional[Future] = None,
        start_time: Optional[float] = None,
        parent_task_id: Optional[str] = None,
        callback: Optional[Callable] = None,
    ):
        """
        Track a submitted future.

        Args:
            task_id: The ID of the task.
            future: The future to track.
            start_time: The start time of the task.
            parent_task_id: The ID of the parent task.
            callback: The callback to run when the task is completed.
        """
        self._tasks[task_id] = {
            "future": future,
            "start_time": start_time,
            "parent_task_id": parent_task_id,
            "callback": callback,
        }
        self._retry_counts[task_id] = 0

    def submit_task(
        self,
        task_id: str,
        async_fn: Union[Callable[[], Awaitable[Any]], Coroutine],
        wait_for_result: bool = False,
        dependent_on_prev: bool = False,
    ):
        """
        Submit a task to the thread pool.

        Args:
            task_id: The ID of the task.
            pool: The thread pool to use.
            async_fn: The async function to submit to the thread pool.
            wait_for_result: Whether to wait for the result of the async function.
            dependent_on_prev: Whether the task depends on the previous task.
        """

        def _submit(*args):
            future = self._pool.submit(async_fn, wait_for_result=wait_for_result)
            future.add_done_callback(lambda f: self._handle_task_completion(task_id))
            self._add_or_update_task(task_id=task_id, future=future, start_time=time.time(), parent_task_id=None)

        if dependent_on_prev:
            last_task_id = list(self._tasks.keys())[-1]
            if self.get_status(last_task_id) == "completed":
                print(f"previous task completed, submitting task: {task_id}")
                _submit()
            else:
                print(f"previous task not completed, tracking task: {task_id}")
                self._add_or_update_task(
                    task_id=task_id, future=None, start_time=None, parent_task_id=last_task_id, callback=_submit
                )
        else:
            print(f"submitting task immediately: {task_id}")
            _submit()

    def get_children(self, parent_task_id: str) -> list[dict]:
        """
        Get the children of a task.
        """
        return [task for _, task in self._tasks.items() if task.get("parent_task_id") == parent_task_id]

    def increment_retry(self, task_id: str):
        """
        Increment the retry count for a task.

        Args:
            task_id: The ID of the task.
        """
        self._retry_counts[task_id] = self._retry_counts.get(task_id, 0) + 1

    def get_status(self, task_id: str) -> TaskStatus:
        """
        Returns the status of a task.

        Args:
            task_id: The ID of the task.

        Returns:
            The status of the task.
        """
        if task_id not in self._tasks:
            return "not_found"

        task = self._tasks[task_id]

        if task.get("parent_task_id"):
            return "pending"

        future = task["future"]
        if not future:
            return "not_found"

        if not future.done():
            return "running"

        try:
            future.result()  # This will raise exception if task failed
            return "completed"
        except Exception:
            return "failed"

    def get_result(self, task_id: str):
        """Get result if task completed, otherwise raises exception"""
        if task_id not in self._tasks:
            raise ValueError(f"Task {task_id} not found")
        return self._tasks[task_id]["future"].result()

    def get_retry_count(self, task_id: str) -> int:
        """
        Get the retry count for a task.
        """
        return self._retry_counts.get(task_id, 0)

    def all_tasks_completed(self) -> bool:
        """
        Check if all tasks are completed.

        Returns:
            True if all tasks are completed, False otherwise.
        """
        return all(self.get_status(task_id) not in ["running", "pending"] for task_id in self._tasks)

    def terminate(self):
        self._pool.stop()
