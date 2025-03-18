"""
Galileo Decorator Module

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
from typing import Any, Callable, Literal, Optional, TypeVar, Union, cast, overload

from typing_extensions import ParamSpec

from galileo.logger import GalileoLogger
from galileo.utils import _get_timestamp
from galileo.utils.serialization import EventSerializer, serialize_to_str
from galileo.utils.singleton import GalileoLoggerSingleton
from galileo_core.schemas.shared.traces.types import Trace, WorkflowSpan

_logger = logging.getLogger(__name__)

# Span types supported by the Galileo SDK
SPAN_TYPE = Literal["llm", "retriever", "tool", "workflow"]

# For users with mypy type checking, we need to define a TypeVar for the decorated function
# Otherwise, mypy will infer the return type of the decorated function as Any
# Docs: https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
F = TypeVar("F", bound=Callable[..., Any])

P = ParamSpec("P")
R = TypeVar("R")

_project_context: ContextVar[Optional[str]] = ContextVar("project_context", default=None)

_log_stream_context: ContextVar[Optional[str]] = ContextVar("log_stream_context", default=None)

_trace_context: ContextVar[Optional[Trace]] = ContextVar("trace_context", default=None)

_experiment_id_context: ContextVar[Optional[str]] = ContextVar("experiment_id_context", default=None)

_span_stack_context: ContextVar[list[WorkflowSpan]] = ContextVar("span_stack_context", default=[])


class GalileoDecorator:
    """
    Main decorator class that provides both decorator and context manager functionality
    for logging and tracing in Galileo.

    This class can be used as:
    1. A function decorator via the `log` method
    2. A context manager via the `__call__` method

    Attributes:
        _project (Optional[str]): The project name for the current context
        _log_stream (Optional[str]): The log stream name for the current context
        _previous_project_context (Optional[str]): Stored project context for restoration
        _previous_log_stream_context (Optional[str]): Stored log stream context for restoration
        _previous_trace_context (Optional[Trace]): Stored trace context for restoration
        _previous_span_stack_context (Optional[list[WorkflowSpan]]): Stored span stack for restoration
    """

    _project: Optional[str]
    _log_stream: Optional[str]
    _experiment_id: Optional[str]
    _previous_project_context: Optional[str]
    _previous_log_stream_context: Optional[str]
    _previous_experiment_id_context: Optional[str]
    _previous_trace_context: Optional[Trace]
    _previous_span_stack_context: Optional[list[WorkflowSpan]]

    #
    # Context manager methods
    #

    def __init__(self) -> None:
        """
        Initialize a new GalileoDecorator instance.
        Sets up the context variables for storing previous context state.
        """
        self._previous_project_context = None
        self._previous_log_stream_context = None
        self._previous_experiment_id_context = None
        self._previous_trace_context = None
        self._previous_span_stack_context = None

    def __enter__(self) -> "GalileoDecorator":
        """
        Entry point for the context manager.

        Saves the current context state and sets up a new context with the
        specified project and log stream.

        Returns:
            GalileoDecorator: The decorator instance for use in a with statement
        """
        self._previous_project_context = _project_context.get()
        self._previous_log_stream_context = _log_stream_context.get()
        self._previous_experiment_id_context = _experiment_id_context.get()
        self._previous_trace_context = _trace_context.get()
        self._previous_span_stack_context = _span_stack_context.get()

        _span_stack_context.set([])
        _trace_context.set(None)

        if self._project is not None:
            _project_context.set(self._project)
        if self._log_stream is not None:
            _log_stream_context.set(self._log_stream)
        if self._experiment_id is not None:
            _experiment_id_context.set(self._experiment_id)

        return self  # Allows `as galileo` usage

    def __exit__(
        self, exc_type: Optional[BaseException], exc_value: Optional[BaseException], traceback: Optional[TracebackType]
    ) -> None:
        """
        Exit point for the context manager.

        Flushes the current logger instance and restores the previous context state.

        Args:
            exc_type: Exception type if an exception was raised in the context
            exc_value: Exception value if an exception was raised in the context
            traceback: Traceback if an exception was raised in the context
        """
        # Flush the logger instance
        self.get_logger_instance(
            project=_project_context.get(),
            log_stream=_log_stream_context.get(),
            experiment_id=_experiment_id_context.get(),
        ).flush()

        # Restore the previous context values to avoid contamination across different usages
        _project_context.set(self._previous_project_context)
        _log_stream_context.set(self._previous_log_stream_context)
        _experiment_id_context.set(self._previous_experiment_id_context)
        _trace_context.set(self._previous_trace_context)
        _span_stack_context.set(self._previous_span_stack_context)

    def __call__(
        self, *, project: Optional[str] = None, log_stream: Optional[str] = None, experiment_id: Optional[str] = None
    ) -> "GalileoDecorator":
        """
        Allows context manager usage like `with galileo_context(project="my-project")`.

        Args:
            project: Optional project name to use for this context
            log_stream: Optional log stream name to use for this context

        Returns:
            GalileoDecorator: The decorator instance configured with the provided parameters
        """
        self._project = project
        self._log_stream = log_stream
        self._experiment_id = experiment_id
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
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        """
        Main decorator function for logging function calls.

        This decorator can be used with or without arguments:
        - @log
        - @log(name="my_function", span_type="llm")

        Args:
            func: The function to decorate (when used without parentheses)
            name: Optional custom name for the span (defaults to function name)
            span_type: Optional span type ("llm", "retriever", "tool", "workflow")
            params: Optional parameter mapping for extracting specific values

        Returns:
            A decorated function that logs its execution
        """

        def decorator(func: Callable[P, R]) -> Callable[P, R]:
            return (
                self._async_log(func, name=name, span_type=span_type, params=params)
                if asyncio.iscoroutinefunction(func)
                else self._sync_log(func, name=name, span_type=span_type, params=params)
            )

        # If the decorator is called without arguments, return the decorator function itself.
        # This allows the decorator to be used with or without arguments.
        if func is None:
            return decorator
        else:
            return decorator(func)

    def _async_log(
        self,
        func: F,
        *,
        name: Optional[str],
        span_type: Optional[SPAN_TYPE],
        params: Optional[dict[str, Union[str, Callable]]] = None,
    ) -> F:
        """
        Internal method to handle logging for async functions.

        Args:
            func: The async function to decorate
            name: Custom name for the span
            span_type: Type of span to create
            params: Parameter mapping for extracting specific values

        Returns:
            Decorated async function that logs its execution
        """

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            span_params = self._prepare_input(
                func=func,
                name=name or func.__name__,
                span_type=span_type,
                params=params,
                is_method=self._is_method(func),
                func_args=args,
                func_kwargs=kwargs,
            )
            self._prepare_call(span_type, span_params)
            result = None

            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                _logger.error(f"Error while executing function in async_wrapper: {e}", exc_info=True)
            finally:
                result = self._finalize_call(span_type, span_params, result)

                if result is not None:
                    return result

        return cast(F, async_wrapper)

    def _sync_log(
        self,
        func: F,
        *,
        name: Optional[str],
        span_type: Optional[SPAN_TYPE],
        params: Optional[dict[str, Union[str, Callable]]] = None,
    ) -> F:
        """
        Internal method to handle logging for synchronous functions.

        Args:
            func: The function to decorate
            name: Custom name for the span
            span_type: Type of span to create
            params: Parameter mapping for extracting specific values

        Returns:
            Decorated function that logs its execution
        """

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            span_params = self._prepare_input(
                func=func,
                name=name or func.__name__,
                span_type=span_type,
                params=params,
                is_method=self._is_method(func),
                func_args=args,
                func_kwargs=kwargs,
            )
            self._prepare_call(span_type, span_params)
            result = None

            try:
                result = func(*args, **kwargs)
            except Exception as exc:
                _logger.warning(f"Error while executing function in sync_wrapper: {exc}", exc_info=True)
                raise exc
            finally:
                self._finalize_call(span_type, span_params, result)
            return result

        return cast(F, sync_wrapper)

    @staticmethod
    def _is_method(func: Callable) -> bool:
        """
        Check if a callable is likely a class or instance method based on its signature.

        Args:
            func: The function to check

        Returns:
            bool: True if 'cls' or 'self' is in the callable's parameters, False otherwise
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
        func_kwargs: dict = {},
    ) -> Optional[dict[str, str]]:
        """
        Prepare the input parameters for logging.

        This method extracts and processes function arguments to create span parameters.

        Args:
            func: The function being decorated
            name: Name for the span
            span_type: Type of span to create
            params: Parameter mapping for extracting specific values
            is_method: Whether the function is a method
            func_args: Positional arguments passed to the function
            func_kwargs: Keyword arguments passed to the function

        Returns:
            Dictionary of parameters for the span, or None if preparation fails
        """
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

            # Auto-map matching parameters if they exist in merged_args
            # This will fill in any missing span parameters based on the function signature
            if span_type:
                span_param_names = self._get_span_param_names(span_type)
                for param_name in span_param_names:
                    if param_name in input_ and param_name not in span_params:
                        span_params[param_name] = input_[param_name]

            if "name" not in span_params:
                span_params["name"] = name

            if "input" not in span_params:
                span_params["input"] = input_

            span_params["input_serialized"] = serialize_to_str(span_params["input"])

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

        Args:
            func: The function being decorated
            is_method: Whether the function is a method
            func_args: Positional arguments passed to the function
            func_kwargs: Keyword arguments passed to the function

        Returns:
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
            param_names = [name for name in sig.parameters.keys() if name not in ("self", "cls")]
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

        Args:
            span_type: The type of span ("llm", "retriever", "tool", "workflow")

        Returns:
            List of parameter names that can be used with the specified span type
        """
        common_params = ["name", "input", "metadata", "tags"]
        span_params = {
            "llm": common_params + ["model", "temperature", "tools"],
            "retriever": common_params,
            "tool": common_params + ["tool_call_id"],
            "workflow": common_params,
        }
        return span_params.get(span_type, common_params)

    def _prepare_call(self, span_type: Optional[SPAN_TYPE], span_params: dict[str, str]):
        """
        Prepare the call for logging by setting up trace and span contexts.

        Args:
            span_type: Type of span to create
            span_params: Parameters for the span
        """
        client_instance = self.get_logger_instance()
        _logger.debug(f"client_instance {id(client_instance)} {client_instance}")

        stack = _span_stack_context.get().copy()
        trace = _trace_context.get()

        input_ = span_params.get("input_serialized", "")
        name = span_params.get("name", "")

        # If no trace is available, start a new one
        if not trace:
            trace = client_instance.start_trace(input=input_, name=name)
            _trace_context.set(trace)

        # If the user hasn't specified a span type, create and add a workflow span
        if not span_type or span_type == "workflow":
            created_at = span_params.get("created_at", _get_timestamp())

            span = client_instance.add_workflow_span(input=input_, name=name, created_at=created_at)
            _span_stack_context.set(stack + [span])

    def _get_input_from_func_args(
        self, *, is_method: bool = False, func_args: tuple = (), func_kwargs: dict = {}
    ) -> Any:
        """
        Extract input from function arguments.

        Args:
            is_method: Whether the function is a method
            func_args: Positional arguments passed to the function
            func_kwargs: Keyword arguments passed to the function

        Returns:
            Serialized representation of the function arguments
        """
        # Remove implicitly passed "self" or "cls" argument for instance or class methods
        logged_args = func_args[1:] if is_method else func_args
        raw_input = {"args": logged_args, "kwargs": func_kwargs}

        # Serialize and deserialize to ensure proper JSON serialization.
        return json.loads(json.dumps(raw_input, cls=EventSerializer))

    def _finalize_call(self, span_type: Optional[SPAN_TYPE], span_params: dict[str, str], result: Any):
        """
        Finalize the call logging by handling the result appropriately.

        This method determines how to handle different types of results (normal values,
        generators, async generators) and logs them accordingly.

        Args:
            span_type: Type of span
            span_params: Parameters for the span
            result: Result of the function call

        Returns:
            The original result, possibly wrapped if it's a generator
        """
        if inspect.isgenerator(result):
            return self._wrap_sync_generator_result(span_type, span_params, result)
        elif inspect.isasyncgen(result):
            return self._wrap_async_generator_result(span_type, span_params, result)
        else:
            return self._handle_call_result(span_type, span_params, result)

    def _handle_call_result(self, span_type: Optional[SPAN_TYPE], span_params: dict[str, str], result: Any):
        """
        Handle the result of a function call for logging.

        This method processes the result and creates the appropriate span or concludes
        the current span based on the span type.

        Args:
            span_type: Type of span
            span_params: Parameters for the span
            result: Result of the function call

        Returns:
            The original result
        """
        try:
            output = span_params.get("output", None)

            if output is None:
                # Process result when no output is provided
                if result is not None:
                    if not span_type or span_type in ["workflow", "tool"]:
                        # For workflow/tool spans, directly convert to string
                        output = serialize_to_str(result)
                    else:
                        # Serialize and deserialize to ensure proper JSON serialization.
                        # Objects are later serialized again so deserialization is necessary here to avoid unnecessary escaping of quotes.
                        output = json.loads(json.dumps(result, cls=EventSerializer))
                else:
                    output = ""
            elif not isinstance(output, str) and (not span_type or span_type in ["workflow", "tool"]):
                # Convert output to string if needed for workflow/tool spans
                output = serialize_to_str(output)

            stack = _span_stack_context.get()

            created_at = span_params.get("created_at")
            created_at_ns = created_at.timestamp() * 1e9 if created_at else 0
            end_time_ns = int(round(_get_timestamp().timestamp() * 1e9))
            if created_at_ns:
                span_params["duration_ns"] = int(round(end_time_ns - created_at_ns))
            else:
                span_params["created_at"] = created_at
                span_params["duration_ns"] = 0

            logger = self.get_logger_instance()

            # If the span type is a workflow, conclude it
            _logger.debug(f"{span_type=} {stack=} {span_params=}")
            if span_type == "workflow" or not span_type:
                if stack:
                    stack.pop()
                    _span_stack_context.set(stack)

                status_code = span_params.get("status_code", None)
                _logger.debug(f"conclude {output=} {status_code=}")
                logger.conclude(output=output, duration_ns=span_params["duration_ns"], status_code=status_code)
            else:
                # If the span type is not a workflow, add it to the current parent (trace or span)
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
            _logger.error(f"Failed to create trace: {e}", exc_info=True)

        return result

    def _wrap_sync_generator_result(
        self, span_type: Optional[SPAN_TYPE], span_params: dict[str, str], generator: Generator
    ) -> Generator:
        """
        Wrap a synchronous generator to log its results.

        This method collects all items yielded by the generator and logs them
        as a single result when the generator is exhausted.

        Args:
            span_type: Type of span
            span_params: Parameters for the span
            generator: The generator to wrap

        Returns:
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
        self, span_type: Optional[SPAN_TYPE], span_params: dict[str, str], generator: AsyncGenerator
    ) -> AsyncGenerator:
        """
        Wrap an asynchronous generator to log its results.

        This method collects all items yielded by the async generator and logs them
        as a single result when the generator is exhausted.

        Args:
            span_type: Type of span
            span_params: Parameters for the span
            generator: The async generator to wrap

        Returns:
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
        self, project: Optional[str] = None, log_stream: Optional[str] = None, experiment_id: Optional[str] = None
    ) -> GalileoLogger:
        """
        Get the Galileo Logger instance for the current decorator context.

        Args:
            project: Optional project name to use
            log_stream: Optional log stream name to use

        Returns:
            GalileoLogger instance configured with the specified project and log stream
        """

        return GalileoLoggerSingleton().get(
            project=project or _project_context.get(),
            log_stream=log_stream or _log_stream_context.get(),
            experiment_id=experiment_id or _experiment_id_context.get(),
        )

    def get_current_project(self) -> Optional[str]:
        """
        Retrieve the current project name from context.

        Returns:
            str | None: The current project context
        """
        return _project_context.get()

    def get_current_log_stream(self) -> Optional[str]:
        """
        Retrieve the current log stream name from context.

        Returns:
            str | None: The current log stream context
        """
        return _log_stream_context.get()

    def get_current_span_stack(self) -> list[WorkflowSpan]:
        """
        Retrieve the current span stack from context.

        Returns:
            List[WorkflowSpan]: The current span stack
        """
        return _span_stack_context.get()

    def get_current_trace(self) -> Optional[Trace]:
        """
        Retrieve the current trace from context.

        Returns:
            Trace | None: The current trace
        """
        return _trace_context.get()

    def flush(
        self, project: Optional[str] = None, log_stream: Optional[str] = None, experiment_id: Optional[str] = None
    ) -> None:
        """
        Upload all captured traces under a project and log stream context to Galileo.

        If no project or log stream is provided, then the currently initialized context is used.

        Args:
            project: The project name. Defaults to None.
            log_stream: The log stream name. Defaults to None.
        """
        self.get_logger_instance(project=project, log_stream=log_stream, experiment_id=experiment_id).flush()

        if project == _project_context.get() and log_stream == _log_stream_context.get():
            _span_stack_context.set([])
            _trace_context.set(None)

        elif project == _project_context.get() and experiment_id == _experiment_id_context.get():
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
        _project_context.set(None)
        _log_stream_context.set(None)
        _experiment_id_context.set(None)
        _span_stack_context.set([])
        _trace_context.set(None)

    def reset_trace_context(self) -> None:
        """
        Reset the trace context inside the decorator.
        """
        _span_stack_context.set([])
        _trace_context.set(None)

    def init(
        self, project: Optional[str] = None, log_stream: Optional[str] = None, experiment_id: Optional[str] = None
    ) -> None:
        """
        Initialize the context with a project and log stream. Optionally, it can also be used
        to start a trace.

        This method resets the existing active context with a new context with
        the specified project and log stream.

        Args:
            project: The project name. Defaults to None.
            log_stream: The log stream name. Defaults to None.
        """
        GalileoLoggerSingleton().reset(project=project, log_stream=log_stream, experiment_id=experiment_id)
        _project_context.set(project)
        _log_stream_context.set(log_stream)
        _experiment_id_context.set(experiment_id)
        _span_stack_context.set([])
        _trace_context.set(None)


galileo_context = GalileoDecorator()
log = galileo_context.log
