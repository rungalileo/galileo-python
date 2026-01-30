"""
Galileo Decorator Module.

This module provides decorators for logging and tracing function calls in your application.
Decorators allow you to add logging functionality to your existing code with minimal changes.

How to use decorators:

1. Basic usage - decorate any function to log its execution:
   ```python
   from galileo import log

   @log
   def my_function(arg1, arg2):
       return arg1 + arg2
   ```

2. You can annotate your logs to help categorize and search logs later on:
   ```python
   @log(span_type="llm", name="GPT-4 Call")
   def call_llm(prompt, temperature=0.7):
       # LLM call implementation
       return response
   ```
    In this case, we are using:
    1. span_type - This groups the logs here into the "llm" category.
    2. name - This assigns a searchable name to all logs within this function.


3. Using context manager for grouping related operations:
   ```python
   from galileo import galileo_context

   with galileo_context(project="my-project", log_stream="production"):
       result1 = my_function()
       result2 = another_function()
   ```

Setup requirements:
- Galileo API key must be set (via environment variable GALILEO_API_KEY or programmatically)
- Project and Log Stream names should be defined if using the `log` decorator (either via environment variables GALILEO_PROJECT and GALILEO_LOG_STREAM, or via `galileo_context.init()`)

For more examples and detailed usage, see the Galileo SDK documentation.
"""

import asyncio
import inspect
import json
import logging
from collections.abc import AsyncGenerator, Generator
from contextvars import ContextVar
from functools import wraps
from types import TracebackType
from typing import Any, Callable, Optional, TypeVar, Union, cast, overload

from typing_extensions import ParamSpec

from galileo.constants import LoggerModeType
from galileo.logger import GalileoLogger
from galileo.logger.logger import STUB_TRACE_NAME
from galileo.schema.datasets import DatasetRecord
from galileo.schema.metrics import LocalMetricConfig
from galileo.schema.trace import SPAN_TYPE
from galileo.utils import _get_timestamp
from galileo.utils.env_helpers import _get_mode_or_default
from galileo.utils.serialization import EventSerializer, convert_time_delta_to_ns, serialize_to_str
from galileo.utils.singleton import GalileoLoggerSingleton
from galileo.utils.span_utils import is_concludable_span_type, is_textual_span_type
from galileo_core.schemas.logging.span import WorkflowSpan
from galileo_core.schemas.logging.trace import Trace

_logger = logging.getLogger(__name__)


# For users with mypy type checking, we need to define a TypeVar for the decorated function
# Otherwise, mypy will infer the return type of the decorated function as Any
# Docs: https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
F = TypeVar("F", bound=Callable[..., Any])

P = ParamSpec("P")
R = TypeVar("R")

# TODO: We should have the context variables store valid values not optional values.
# Context variables for current values
_project_context: ContextVar[Optional[str]] = ContextVar("project_context", default=None)
_log_stream_context: ContextVar[Optional[str]] = ContextVar("log_stream_context", default=None)
_trace_context: ContextVar[Optional[Trace]] = ContextVar("trace_context", default=None)
_experiment_id_context: ContextVar[Optional[str]] = ContextVar("experiment_id_context", default=None)
_span_stack_context: ContextVar[Optional[list[WorkflowSpan]]] = ContextVar("span_stack_context", default=None)
_mode_context: ContextVar[Optional[LoggerModeType]] = ContextVar("mode_context", default=None)
_session_id_context: ContextVar[Optional[str]] = ContextVar("session_id_context", default=None)

# Distributed tracing context variables (for middleware)
_trace_id_context: ContextVar[Optional[str]] = ContextVar("trace_id_context", default=None)
_parent_id_context: ContextVar[Optional[str]] = ContextVar("parent_id_context", default=None)

# Stack variables for storing previous values (for proper nesting)
_project_stack: ContextVar[Optional[list[Optional[str]]]] = ContextVar("project_stack", default=None)
_log_stream_stack: ContextVar[Optional[list[Optional[str]]]] = ContextVar("log_stream_stack", default=None)
_trace_stack: ContextVar[Optional[list[Optional[Trace]]]] = ContextVar("trace_stack", default=None)
_experiment_id_stack: ContextVar[Optional[list[Optional[str]]]] = ContextVar("experiment_id_stack", default=None)
_session_id_stack: ContextVar[Optional[list[Optional[str]]]] = ContextVar("session_id_stack", default=None)
_mode_stack: ContextVar[Optional[list[LoggerModeType]]] = ContextVar("mode_stack", default=None)
_span_stack_stack: ContextVar[Optional[list[list[WorkflowSpan]]]] = ContextVar("span_stack_stack", default=None)


def _get_or_init_list(context_var: ContextVar, default_factory: Callable = list) -> list:
    """Helper function to get or initialize a context variable with a list."""
    value = context_var.get()
    if value is None:
        value = default_factory()
        context_var.set(value)
    return value


class GalileoDecorator:
    """
    Main decorator class that provides both decorator and context manager functionality
    for logging and tracing in Galileo.

    This class can be used as:
    1. A function decorator via the `log` method
    2. A context manager via the `__call__` method
    """

    def __enter__(self) -> "GalileoDecorator":
        """
        Entry point for the context manager.

        Returns
        -------
        GalileoDecorator
            The decorator instance for use in a with statement
        """
        # Nothing to do here since __call__ has already set up the context
        return self  # Allows `as galileo` usage

    def __exit__(
        self, exc_type: Optional[BaseException], exc_value: Optional[BaseException], traceback: Optional[TracebackType]
    ) -> None:
        """
        Exit point for the context manager.

        Flushes the current logger instance and restores the previous context state.

        Parameters
        ----------
        exc_type
            Exception type if an exception was raised in the context
        exc_value
            Exception value if an exception was raised in the context
        traceback
            Traceback if an exception was raised in the context
        """
        # Flush the logger instance
        self.get_logger_instance(
            project=_project_context.get(),
            log_stream=_log_stream_context.get(),
            experiment_id=_experiment_id_context.get(),
        ).flush()

        _session_id_context.set(None)

        # Pop values from the stacks and restore the previous context
        _project_context.set(_get_or_init_list(_project_stack).pop())
        _log_stream_context.set(_get_or_init_list(_log_stream_stack).pop())
        _experiment_id_context.set(_get_or_init_list(_experiment_id_stack).pop())
        _trace_context.set(_get_or_init_list(_trace_stack).pop())
        _mode_context.set(_get_or_init_list(_mode_stack).pop())
        _span_stack_context.set(_get_or_init_list(_span_stack_stack).pop())
        _session_id_context.set(_get_or_init_list(_session_id_stack).pop())

    def __call__(
        self,
        *,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
        experiment_id: Optional[str] = None,
        mode: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> "GalileoDecorator":
        """
        Call method to use the decorator as a context manager.

        This allows usage like:
        ```python
        with galileo_context(project="my_project", log_stream="my_stream"):
            # Code to be traced
        ```

        Parameters
        ----------
        project
            The project name to use for this context
        log_stream: The log stream name to use for this context
            The log stream name to use for this context
        experiment_id
            The experiment ID to use for this context
        mode
            The logger mode
        session_id
            The session ID to use for this context

        Returns
        -------
        GalileoDecorator
            The decorator instance for use in a with statement
        """
        # Push current values onto the stacks
        _get_or_init_list(_project_stack).append(_project_context.get())
        _get_or_init_list(_log_stream_stack).append(_log_stream_context.get())
        _get_or_init_list(_experiment_id_stack).append(_experiment_id_context.get())
        _get_or_init_list(_trace_stack).append(_trace_context.get())
        _get_or_init_list(_mode_stack).append(_mode_context.get())
        _get_or_init_list(_span_stack_stack).append(_get_or_init_list(_span_stack_context).copy())
        _get_or_init_list(_session_id_stack).append(_session_id_context.get())

        # Reset trace context values
        _span_stack_context.set([])
        _trace_context.set(None)

        # Set request context values to defaults
        _project_context.set(None)
        _log_stream_context.set(None)
        _experiment_id_context.set(None)
        _mode_context.set(_get_mode_or_default(None))
        _session_id_context.set(None)

        # Override with explicitly provided values
        if project is not None:
            _project_context.set(project)
        if log_stream is not None:
            _log_stream_context.set(log_stream)
        if experiment_id is not None:
            _experiment_id_context.set(experiment_id)
        if mode is not None:
            _mode_context.set(_get_mode_or_default(mode))
        if session_id is not None:
            _session_id_context.set(session_id)
            self.set_session(session_id)

        return self

    #
    # Decorator methods
    #

    @overload
    def log(self, func: F) -> F: ...

    @overload
    def log(
        self,
        func: None = None,
        *,
        name: Optional[str] = None,
        span_type: Optional[SPAN_TYPE] = None,
        params: Optional[dict[str, Union[str, Callable]]] = None,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

    def log(
        self,
        func: Optional[Callable[P, R]] = None,
        *,
        name: Optional[str] = None,
        span_type: Optional[SPAN_TYPE] = None,
        params: Optional[dict[str, Union[str, Callable]]] = None,
        dataset_record: Optional[DatasetRecord] = None,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        """
        Main decorator function for logging function calls.

        This decorator can be used with or without arguments:
        - @log
        - @log(name="my_function", span_type="llm")

        Parameters
        ----------
        func
            The function to decorate (when used without parentheses)
        name
            Optional custom name for the span (defaults to function name)
        span_type
            Optional span type ("llm", "retriever", "tool", "workflow", "agent")
        params
            Optional parameter mapping for extracting specific values
        dataset_record
            Optional parameter for dataset values.  This is used by the local experiment module to set the dataset fields on the trace/spans and not generally provided for logging to log streams.

        Returns
        -------
        A decorated function that logs its execution
        """

        def decorator(func: Callable[P, R]) -> Callable[P, R]:
            return (
                self._async_log(func, name=name, span_type=span_type, params=params, dataset_record=dataset_record)
                if asyncio.iscoroutinefunction(func)
                else self._sync_log(func, name=name, span_type=span_type, params=params, dataset_record=dataset_record)
            )

        # If the decorator is called without arguments, return the decorator function itself.
        # This allows the decorator to be used with or without arguments.
        if func is None:
            return decorator
        return decorator(func)

    def _async_log(
        self,
        func: F,
        *,
        name: Optional[str],
        span_type: Optional[SPAN_TYPE],
        params: Optional[dict[str, Union[str, Callable]]] = None,
        dataset_record: Optional[DatasetRecord] = None,
    ) -> F:
        """
        Internal method to handle logging for async functions.

        Parameters
        ----------
        func
            The async function to decorate
        name
            Custom name for the span
        span_type
            Type of span to create
        params
            Parameter mapping for extracting specific values

        Returns
        -------
        Decorated async function that logs its execution
        """

        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            # Copy the span stack to isolate parallel async tasks
            # This prevents concurrent tasks from interfering with each other's span stacks
            current_stack = _get_or_init_list(_span_stack_context)
            _span_stack_context.set(current_stack.copy())

            # TODO: Parallel nested workflows are not fully supported yet
            # The logger's _parent_stack needs to use ContextVar for proper isolation
            # Currently, parallel child workflows within a parent workflow will have corrupted trace structure

            span_params = self._prepare_input(
                func=func,
                name=name or func.__name__,
                span_type=span_type,
                params=params,
                is_method=self._is_method(func),
                func_args=args,
                func_kwargs=kwargs,
            )

            logging_enabled = self._safe_prepare_call(span_type, span_params, dataset_record)

            result = None
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                _logger.error(f"Error while executing function in async_wrapper: {e}", exc_info=True)
                raise
            finally:
                if logging_enabled:
                    result = self._finalize_call(span_type, span_params, result)

            return result

        return cast(F, async_wrapper)

    def _sync_log(
        self,
        func: F,
        *,
        name: Optional[str],
        span_type: Optional[SPAN_TYPE],
        params: Optional[dict[str, Union[str, Callable]]] = None,
        dataset_record: Optional[DatasetRecord] = None,
    ) -> F:
        """
        Internal method to handle logging for synchronous functions.

        Parameters
        ----------
        func
            The function to decorate
        name
            Custom name for the span
        span_type
            Type of span to create
        params
            Parameter mapping for extracting specific values

        Returns
        -------
            Decorated function that logs its execution
        """

        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            span_params = self._prepare_input(
                func=func,
                name=name or func.__name__,
                span_type=span_type,
                params=params,
                is_method=self._is_method(func),
                func_args=args,
                func_kwargs=kwargs,
            )

            logging_enabled = self._safe_prepare_call(span_type, span_params, dataset_record)

            result = None
            try:
                result = func(*args, **kwargs)
            except Exception as exc:
                _logger.warning(f"Error while executing function in sync_wrapper: {exc}", exc_info=True)
                raise exc
            finally:
                if logging_enabled:
                    self._finalize_call(span_type, span_params, result)
            return result

        return cast(F, sync_wrapper)

    @staticmethod
    def _is_method(func: Callable) -> bool:
        """
        Check if a callable is likely a class or instance method based on its signature.

        Parameters
        ----------
        func
            The function to check

        Returns
        -------
        bool
            True if 'cls' or 'self' is in the callable's parameters, False otherwise
        """
        return "self" in inspect.signature(func).parameters or "cls" in inspect.signature(func).parameters

    def _prepare_input(
        self,
        *,
        func: Callable,
        name: str,
        span_type: Optional[SPAN_TYPE],
        params: Optional[dict[str, Union[str, Callable]]] = None,
        is_method: bool = False,
        func_args: tuple = (),
        func_kwargs: Optional[dict] = None,
    ) -> Optional[dict[str, Any]]:
        """
        Prepare the input parameters for logging.

        This method extracts and processes function arguments to create span parameters.

        Parameters
        ----------
        func
            The function being decorated
        name
            Name for the span
        span_type
            Type of span to create
        params
            Parameter mapping for extracting specific values
        is_method
            Whether the function is a method
        func_args
            Positional arguments passed to the function
        func_kwargs
            Keyword arguments passed to the function

        Returns
        -------
        Dictionary of parameters for the span, or None if preparation fails
        """
        if func_kwargs is None:
            func_kwargs = {}
        try:
            start_time = _get_timestamp()

            # Extract function args
            input_ = self._merge_args_with_kwargs(
                func=func, is_method=is_method, func_args=func_args, func_kwargs=func_kwargs
            )

            # Process parameter mappings supplied by the user via `params`
            span_params = {}
            if params:
                for span_param, mapping in params.items():
                    if callable(mapping):
                        # If mapping is a function, call it with the merged args
                        span_params[span_param] = mapping(input_)
                    else:
                        # If mapping is a string, use it as a key to get value from merged args
                        if mapping in input_:
                            span_params[span_param] = input_[mapping]
                        else:
                            # If it's not in the merged args, use the mapping as the value
                            span_params[span_param] = mapping

            # Auto-map matching parameters if they exist in merged_args
            # This will fill in any missing span parameters based on the function signature
            if span_type:
                span_param_names = self._get_span_param_names(span_type)
                for param_name in span_param_names:
                    if param_name in input_ and param_name not in span_params:
                        span_params[param_name] = input_[param_name]

            if "name" not in span_params:
                span_params["name"] = name

            span_params["input"] = input_

            input_serialized = serialize_to_str(span_params["input"])
            span_params["input_serialized"] = input_serialized
            span_params["input"] = json.loads(input_serialized)

            span_params["created_at"] = start_time

            return span_params
        except Exception as e:
            _logger.error(f"Failed to parse input params: {e}", exc_info=True)
            return None

    def _merge_args_with_kwargs(
        self, *, func: Callable, is_method: bool, func_args: tuple, func_kwargs: dict
    ) -> dict[str, Any]:
        """
        Merge positional and keyword arguments into a single dictionary.

        Parameters
        ----------
        func
            The function being decorated
        is_method
            Whether the function is a method
        func_args
            Positional arguments passed to the function
        func_kwargs
            Keyword arguments passed to the function

        Returns
        -------
        Dictionary containing all arguments with their parameter names as keys
        """
        try:
            # Get the actual function, handling wrapped functions
            actual_func = getattr(func, "__wrapped__", func)
            sig = inspect.signature(actual_func)

            # Create a dictionary of all parameters with their default values
            merged = {}
            for name, param in sig.parameters.items():
                if name not in ("self", "cls"):  # Skip self and cls
                    if param.default is not inspect.Parameter.empty:
                        merged[name] = param.default

            # Create dictionary of positional args
            param_names = [name for name in sig.parameters if name not in ("self", "cls")]
            for param_name, value in zip(param_names, func_args[1:] if is_method else func_args):
                merged[param_name] = value

            # Update with provided keyword arguments
            merged.update(func_kwargs)

            return merged
        except Exception as e:
            _logger.error(f"Error merging args and kwargs: {e}", exc_info=True)
            # Return just the kwargs if something goes wrong
            return func_kwargs

    def _get_span_param_names(self, span_type: SPAN_TYPE) -> list[str]:
        """
        Return the parameter names available for each span type.

        Parameters
        ----------
        span_type
            The type of span ("llm", "retriever", "tool", "workflow", "agent")

        Returns
        -------
        List of parameter names that can be used with the specified span type
        """
        common_params = ["name", "input", "metadata", "tags"]
        span_params = {
            "llm": [*common_params, "model", "temperature", "tools"],
            "retriever": common_params,
            "tool": [*common_params, "tool_call_id"],
            "workflow": common_params,
            "agent": [*common_params, "agent_type"],
        }
        return span_params.get(span_type, common_params)

    def _safe_prepare_call(
        self, span_type: Optional[SPAN_TYPE], span_params: dict[str, Any], dataset_record: Optional[DatasetRecord]
    ) -> bool:
        """
        Safely prepare telemetry, returning False if initialization fails.

        This method wraps _prepare_call with exception handling to ensure that
        telemetry initialization errors do not crash user code. Any exception
        during preparation is logged as a warning and the method returns False,
        allowing the caller to skip finalization.

        Parameters
        ----------
        span_type
            Type of span to create
        span_params
            Parameters for the span
        dataset_record
            Optional dataset record for experiment context

        Returns
        -------
        bool
            True if preparation succeeded, False if it failed
        """
        try:
            self._prepare_call(span_type, span_params, dataset_record)
            return True
        except Exception as e:
            _logger.warning(f"Galileo logging initialization failed, continuing without logging: {e}")
            return False

    def _prepare_call(
        self, span_type: Optional[SPAN_TYPE], span_params: dict[str, Any], dataset_record: Optional[DatasetRecord]
    ) -> None:
        """
        Prepare the call for logging by setting up trace and span contexts.

        Parameters
        ----------
        span_type
            Type of span to create
        span_params
            Parameters for the span
        """
        client_instance = self.get_logger_instance()
        _logger.debug(f"client_instance {id(client_instance)} {client_instance}")

        input_ = span_params.get("input_serialized", "")
        name = span_params.get("name", "")

        existing_trace = _trace_context.get()

        # Check if existing trace is still valid (not concluded/flushed)
        if existing_trace and client_instance.current_parent() is None:
            existing_trace = None
            _trace_context.set(None)

        if not existing_trace:
            # If the singleton logger has an active trace, use it
            if client_instance.has_active_trace():
                trace = client_instance.traces[-1]
            else:
                # If no trace is available, start a new one
                trace = client_instance.start_trace(
                    input=input_,
                    name=name,
                    # TODO: add dataset_row_id
                    dataset_input=dataset_record.input if dataset_record else None,
                    dataset_output=dataset_record.output if dataset_record else None,
                    dataset_metadata=dataset_record.metadata if dataset_record else None,
                )
            _trace_context.set(trace)

        # Start a workflow or agent span here
        # If the user hasn't specified a span type, create and add a workflow span
        if not span_type or span_type in ["workflow", "agent"]:
            created_at = span_params.get("created_at", _get_timestamp())
            if span_type == "agent":
                agent_type = span_params.get("agent_type")
                span = client_instance.add_agent_span(
                    input=input_, name=name, agent_type=agent_type, created_at=created_at
                )
            else:
                span = client_instance.add_workflow_span(input=input_, name=name, created_at=created_at)
            _get_or_init_list(_span_stack_context).append(span)

    def _get_input_from_func_args(
        self, *, is_method: bool = False, func_args: tuple = (), func_kwargs: Optional[dict] = None
    ) -> Any:
        """
        Extract input from function arguments.

        Parameters
        ----------
        is_method
            Whether the function is a method
        func_args
            Positional arguments passed to the function
        func_kwargs
            Keyword arguments passed to the function

        Returns
        -------
        Serialized representation of the function arguments
        """
        # Remove implicitly passed "self" or "cls" argument for instance or class methods
        if func_kwargs is None:
            func_kwargs = {}
        logged_args = func_args[1:] if is_method else func_args
        raw_input = {"args": logged_args, "kwargs": func_kwargs}

        # Serialize and deserialize to ensure proper JSON serialization.
        return json.loads(json.dumps(raw_input, cls=EventSerializer))

    def _finalize_call(
        self, span_type: Optional[SPAN_TYPE], span_params: dict[str, Any], result: Any
    ) -> Union[Generator, AsyncGenerator, Any]:
        """
        Finalize the call logging by handling the result appropriately.

        This method determines how to handle different types of results (normal values,
        generators, async generators) and logs them accordingly.

        Parameters
        ----------
        span_type
            Type of span
        span_params
            Parameters for the span
        result
            Result of the function call

        Returns
        -------
        The original result, possibly wrapped if it's a generator
        """
        if inspect.isgenerator(result):
            return self._wrap_sync_generator_result(span_type, span_params, result)
        if inspect.isasyncgen(result):
            return self._wrap_async_generator_result(span_type, span_params, result)
        return self._handle_call_result(span_type, span_params, result)

    def _serialize_output(self, output: Any, span_type: Optional[SPAN_TYPE]) -> Any:
        """
        Serialize output value for logging.

        Parameters
        ----------
        output
            Output value to serialize
        span_type
            Type of span (determines serialization strategy)

        Returns
        -------
        Serialized output (string or JSON-serializable dict/list)
        """
        if isinstance(output, str):
            return output

        # Check if this span type needs string serialization
        if (
            # an empty span_type means it's a workflow span
            not span_type
            # textual spans are spans with string-based input and output
            or is_textual_span_type(span_type)
            # llm spans don't accept list or tuple types as output
            or (span_type == "llm" and isinstance(output, (list, tuple)))
        ):
            # Convert output to string if needed for workflow/tool/agent spans
            return serialize_to_str(output)
        # Serialize and deserialize to ensure proper JSON serialization
        return json.loads(json.dumps(output, cls=EventSerializer))

    def _handle_call_result(self, span_type: Optional[SPAN_TYPE], span_params: dict[str, Any], result: Any) -> Any:
        """
        Handle the result of a function call for logging.

        This method processes the result and creates the appropriate span or concludes
        the current span based on the span type.

        Parameters
        ----------
            span_type
                Type of span
            span_params
                Parameters for the span
            result
                Result of the function call

        Returns
        -------
        The original result
        """
        # Initialize logger before try block
        logger = self.get_logger_instance()

        # Serialize output and redacted_output - set to None if serialization fails
        output = span_params.get("output")
        if output is None:
            output = result if result is not None else ""

        redacted_output = span_params.get("redacted_output")
        span_name = span_params.get("name", "unknown")

        try:
            # Serialize output and redacted_output
            output = self._serialize_output(output, span_type)
            if redacted_output is not None:
                redacted_output = self._serialize_output(redacted_output, span_type)

            stack = _get_or_init_list(_span_stack_context)

            created_at = span_params.get("created_at")
            created_at_ns = created_at.timestamp() * 1e9 if created_at else 0
            end_time_ns = round(_get_timestamp().timestamp() * 1e9)
            if created_at_ns:
                span_params["duration_ns"] = round(end_time_ns - created_at_ns)
            else:
                span_params["created_at"] = created_at
                span_params["duration_ns"] = 0

            # Workflow and agent spans are "concludable" - they need to be concluded
            # Default (no span_type) is treated as workflow
            if not span_type or is_concludable_span_type(span_type):
                # Pop from stack and conclude the workflow/agent span
                if stack:
                    stack.pop()
                    _span_stack_context.set(stack)

                status_code = span_params.get("status_code")
                logger.conclude(output=output, duration_ns=span_params["duration_ns"], status_code=status_code)

                # In distributed mode, update parent trace output after concluding a top-level workflow
                # This ensures the trace shows the latest workflow's output (last workflow wins)
                # Skip stub traces (created from distributed tracing headers - they're managed by the client)
                if logger.mode == "distributed" and not stack:
                    current_parent = logger.current_parent()
                    if current_parent is not None and isinstance(current_parent, Trace):
                        is_stub_trace = current_parent.name == STUB_TRACE_NAME

                        if not is_stub_trace:
                            current_parent.output = output
                            if redacted_output is not None:
                                current_parent.redacted_output = redacted_output

                            # Update trace duration
                            # Note: In distributed mode, trace.created_at may be set by the server
                            # Using max() to ensure parent is never shorter than its children.
                            if current_parent.created_at:
                                elapsed_ns = convert_time_delta_to_ns(_get_timestamp() - current_parent.created_at)
                                workflow_ns = span_params.get("duration_ns", 0)
                                prev_ns = current_parent.metrics.duration_ns or 0
                                current_parent.metrics.duration_ns = max(elapsed_ns, workflow_ns, prev_ns)

                            if status_code is not None:
                                current_parent.status_code = status_code

                            logger._update_trace_streaming(current_parent, is_complete=False)
            else:
                # Non-concludable spans (llm, tool, retriever) are  added to the parent
                span_methods = {"llm": "add_llm_span", "tool": "add_tool_span", "retriever": "add_retriever_span"}

                if span_type in span_methods:
                    method_name = span_methods[span_type]
                    method = getattr(logger, method_name)

                    # Get the parameters the function accepts
                    sig = inspect.signature(method)
                    valid_params = sig.parameters.keys()

                    kwargs = {"output": output, **span_params}

                    if span_type != "llm":
                        kwargs["input"] = kwargs.get("input_serialized", "")

                    if span_type == "llm" and "model" not in kwargs:
                        # TODO: Allow a model to be parsed from the span_params
                        # This only affects direct @log(span_type="llm") calls, not OpenAI
                        kwargs["model"] = ""

                    # Filter out kwargs that aren't in the function's parameters
                    filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_params}

                    method(**filtered_kwargs)
        except Exception as e:
            _logger.error(f"Failed to create trace for span '{span_name}' (type: {span_type}): {e}", exc_info=True)

        return result

    def _wrap_sync_generator_result(
        self, span_type: Optional[SPAN_TYPE], span_params: dict[str, Any], generator: Generator
    ) -> Generator:
        """
        Wrap a synchronous generator to log its results.

        This method collects all items yielded by the generator and logs them
        as a single result when the generator is exhausted.

        Parameters
        ----------
        span_type
            Type of span
        span_params
            Parameters for the span
        generator
            The generator to wrap

        Returns
        -------
        A wrapped generator that yields the same items as the original
        """
        items = []

        try:
            for item in generator:
                items.append(item)

                yield item
        except Exception as e:
            _logger.error(f"Failed to wrap generator result: {e}", exc_info=True)
        finally:
            output = items

            if all(isinstance(item, str) for item in items):
                output = "".join(items)

            self._handle_call_result(span_type, span_params, output)

    async def _wrap_async_generator_result(
        self, span_type: Optional[SPAN_TYPE], span_params: dict[str, Any], generator: AsyncGenerator
    ) -> AsyncGenerator:
        """
        Wrap an asynchronous generator to log its results.

        This method collects all items yielded by the async generator and logs them
        as a single result when the generator is exhausted.

        Parameters
        ----------
        span_type
            Type of span
        span_params
            Parameters for the span
        generator
            The async generator to wrap

        Returns
        -------
        A wrapped async generator that yields the same items as the original
        """
        items = []

        try:
            async for item in generator:
                items.append(item)

                yield item
        except Exception as e:
            _logger.error(f"Failed to wrap generator result: {e}", exc_info=True)
        finally:
            output = items

            if all(isinstance(item, str) for item in items):
                output = "".join(items)

            self._handle_call_result(span_type, span_params, output)

    def get_logger_instance(
        self,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
        experiment_id: Optional[str] = None,
        mode: Optional[str] = None,
    ) -> GalileoLogger:
        """
        Get the Galileo Logger instance for the current decorator context.

        Parameters
        ----------
        project
            Optional project name to use
        log_stream
            Optional log stream name to use
        experiment_id
            Optional experiment ID to use
        mode
            Optional logger mode to use

        Returns
        -------
        GalileoLogger instance configured with the specified project and log stream
        """
        kwargs = {
            "project": project or _project_context.get(),
            "log_stream": log_stream or _log_stream_context.get(),
            "experiment_id": experiment_id or _experiment_id_context.get(),
            "mode": _get_mode_or_default(mode) if mode is not None else _mode_context.get(),
        }
        trace_id_from_context = _trace_id_context.get()
        span_id_from_context = _parent_id_context.get()
        if trace_id_from_context:
            kwargs["trace_id"] = trace_id_from_context
        if span_id_from_context:
            kwargs["span_id"] = span_id_from_context

        return GalileoLoggerSingleton().get(**kwargs)

    def get_current_project(self) -> Optional[str]:
        """
        Retrieve the current project name from context.

        Returns
        -------
        str | None
            The current project context
        """
        return _project_context.get()

    def get_current_log_stream(self) -> Optional[str]:
        """
        Retrieve the current log stream name from context.

        Returns
        -------
        str | None
            The current log stream context
        """
        return _log_stream_context.get()

    def get_current_span_stack(self) -> list[WorkflowSpan]:
        """
        Retrieve the current span stack from context.

        Returns
        -------
        List[WorkflowSpan]
            The current span stack
        """
        return _get_or_init_list(_span_stack_context)

    def get_current_trace(self) -> Optional[Trace]:
        """
        Retrieve the current trace from context.

        Returns
        -------
        Trace | None
            The current trace
        """
        return _trace_context.get()

    def get_current_mode(self) -> Optional[LoggerModeType]:
        """
        Retrieve the current mode from context.

        Returns
        -------
        Optional[LoggerModeType]
            The current mode context, or None if not initialized
        """
        return _mode_context.get()

    def flush(
        self,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
        experiment_id: Optional[str] = None,
        mode: Optional[str] = None,
    ) -> None:
        """
        Upload all captured traces under a project and log stream context to Galileo.

        If no project or log stream is provided, then the currently initialized context is used.

        Parameters
        ----------
        project
            The project name. Defaults to None.
        log_stream
            The log stream name. Defaults to None.
        experiment_id
            The experiment ID. Defaults to None.
        mode
            The logger mode. Defaults to None.
        """
        # Telemetry initialization errors should not crash user code
        try:
            self.get_logger_instance(
                project=project, log_stream=log_stream, experiment_id=experiment_id, mode=mode
            ).flush()
        except Exception as e:
            _logger.warning(f"Galileo flush failed, continuing without flushing: {e}")

        # Reset trace state if we're flushing the current context
        current_mode = _get_mode_or_default(mode) if mode is not None else _mode_context.get()
        resolved_project = project if project is not None else _project_context.get()
        resolved_log_stream = log_stream if log_stream is not None else _log_stream_context.get()
        resolved_experiment_id = experiment_id if experiment_id is not None else _experiment_id_context.get()

        if (
            current_mode == _mode_context.get()
            and resolved_project == _project_context.get()
            and resolved_log_stream == _log_stream_context.get()
            and resolved_experiment_id == _experiment_id_context.get()
        ):
            _span_stack_context.set([])
            _trace_context.set(None)

    def flush_all(self) -> None:
        """
        Upload all captured traces under all contexts to Galileo.

        This method flushes all traces regardless of project or log stream.
        """
        GalileoLoggerSingleton().flush_all()
        _span_stack_context.set([])
        _trace_context.set(None)

    def reset(self) -> None:
        """
        Reset the entire context, which also deletes all traces that haven't been flushed.

        This method clears all context variables and resets the logger singleton.
        """
        GalileoLoggerSingleton().reset(
            project=_project_context.get(),
            log_stream=_log_stream_context.get(),
            experiment_id=_experiment_id_context.get(),
        )
        # Reset current context values
        _project_context.set(None)
        _log_stream_context.set(None)
        _experiment_id_context.set(None)
        _mode_context.set(_get_mode_or_default(None))
        _span_stack_context.set([])
        _trace_context.set(None)
        _session_id_context.set(None)
        # Reset distributed tracing context
        _trace_id_context.set(None)
        _parent_id_context.set(None)

        # Clear all stacks
        _get_or_init_list(_project_stack).clear()
        _get_or_init_list(_log_stream_stack).clear()
        _get_or_init_list(_trace_stack).clear()
        _get_or_init_list(_experiment_id_stack).clear()
        _get_or_init_list(_mode_stack).clear()
        _get_or_init_list(_span_stack_stack).clear()
        _get_or_init_list(_session_id_stack).clear()

    def reset_trace_context(self) -> None:
        """Reset the trace context inside the decorator."""
        _span_stack_context.set([])
        _trace_context.set(None)

    def init(
        self,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
        experiment_id: Optional[str] = None,
        local_metrics: Optional[list[LocalMetricConfig]] = None,
        mode: Optional[str] = None,
    ) -> None:
        """
        Initialize the context with a project and log stream. Optionally, it can also be used
        to start a trace.

        This method resets the existing active context with a new context with
        the specified project and log stream.

        Parameters
        ----------
        project
            The project name. Defaults to None.
        log_stream
            The log stream name. Defaults to None.
        experiment_id
            The experiment id. Defaults to None.
        local_metrics
            Local metrics configs to run on the traces/spans before submitting them for ingestion.  Defaults to None.
        mode
            The logger mode.
        """
        GalileoLoggerSingleton().reset(project=project, log_stream=log_stream, experiment_id=experiment_id)
        logger_instance = GalileoLoggerSingleton().get(
            project=project, log_stream=log_stream, experiment_id=experiment_id, local_metrics=local_metrics, mode=mode
        )
        # Reset the logger's parent tracking to ensure clean state
        # Each logger has its own ContextVar, so this resets only this instance
        logger_instance.reset_parent_tracking()

        _project_context.set(project)
        _log_stream_context.set(log_stream)
        _experiment_id_context.set(experiment_id)
        _mode_context.set(_get_mode_or_default(mode))
        _span_stack_context.set([])
        _trace_context.set(None)
        _session_id_context.set(None)

    def start_session(
        self, name: Optional[str] = None, previous_session_id: Optional[str] = None, external_id: Optional[str] = None
    ) -> str:
        """
        Start a session in the active context logger instance.

        Parameters
        ----------
        name
            The name of the session. If not provided, a session name will be generated automatically.
        previous_session_id
            The id of the previous session. Defaults to None.
        external_id
            The external id of the session. Defaults to None.

        Returns
        -------
        str
            The id of the newly created session.
        """
        session_id = self.get_logger_instance().start_session(
            name=name, previous_session_id=previous_session_id, external_id=external_id
        )

        _session_id_context.set(session_id)
        return session_id

    def clear_session(self) -> None:
        """Clear the session in the active context logger instance."""
        self.get_logger_instance().clear_session()

    def set_session(self, session_id: str) -> None:
        """
        Set the session in the active context logger instance. This is useful when you want to continue logging to an existing session.

        Parameters
        ----------
        session_id
            The id of the session to set.
        """
        self.get_logger_instance().set_session(session_id)


galileo_context = GalileoDecorator()
log = galileo_context.log
start_session = galileo_context.start_session
