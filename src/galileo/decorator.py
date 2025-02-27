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
from galileo.utils.serialization import EventSerializer
from galileo.utils.singleton import GalileoLoggerSingleton
from galileo_core.schemas.shared.traces.types import Trace, WorkflowSpan

_logger = logging.getLogger(__name__)

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

_span_stack_context: ContextVar[list[WorkflowSpan]] = ContextVar("span_stack_context", default=[])


class GalileoDecorator:
    _project: Optional[str]
    _log_stream: Optional[str]
    _previous_project_context: Optional[str]
    _previous_log_stream_context: Optional[str]
    _previous_trace_context: Optional[Trace]
    _previous_span_stack_context: Optional[list[WorkflowSpan]]

    #
    # Context manager methods
    #

    def __init__(self) -> None:
        self._previous_project_context = None
        self._previous_log_stream_context = None
        self._previous_trace_context = None
        self._previous_span_stack_context = None

    def __enter__(self) -> "GalileoDecorator":
        """
        Entry point for the context manager.
        """
        self._previous_project_context = _project_context.get()
        self._previous_log_stream_context = _log_stream_context.get()
        self._previous_trace_context = _trace_context.get()
        self._previous_span_stack_context = _span_stack_context.get()

        _span_stack_context.set([])
        _trace_context.set(None)

        if self._project is not None:
            _project_context.set(self._project)
        if self._log_stream is not None:
            _log_stream_context.set(self._log_stream)

        return self  # Allows `as galileo` usage

    def __exit__(
        self, exc_type: Optional[BaseException], exc_value: Optional[BaseException], traceback: Optional[TracebackType]
    ) -> None:
        # Flush the logger instance
        self.get_logger_instance(project=_project_context.get(), log_stream=_log_stream_context.get()).flush()

        # Restore the previous context values to avoid contamination across different usages
        _project_context.set(self._previous_project_context)
        _log_stream_context.set(self._previous_log_stream_context)
        _trace_context.set(self._previous_trace_context)
        _span_stack_context.set(self._previous_span_stack_context)

    def __call__(self, *, project: Optional[str] = None, log_stream: Optional[str] = None) -> "GalileoDecorator":
        """Allows context manager usage like `with galileo_context(...)`"""
        self._project = project
        self._log_stream = log_stream
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
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
        params: Optional[dict[str, Union[str, Callable]]] = None,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

    def log(
        self,
        func: Optional[Callable[P, R]] = None,
        *,
        name: Optional[str] = None,
        span_type: Optional[SPAN_TYPE] = None,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
        params: Optional[dict[str, Union[str, Callable]]] = None,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        def decorator(func: Callable[P, R]) -> Callable[P, R]:
            return (
                self._async_log(
                    func,
                    name=name,
                    span_type=span_type,
                    project=project or _project_context.get(),
                    log_stream=log_stream or _log_stream_context.get(),
                    params=params,
                )
                if asyncio.iscoroutinefunction(func)
                else self._sync_log(
                    func,
                    name=name,
                    span_type=span_type,
                    project=project or _project_context.get(),
                    log_stream=log_stream or _log_stream_context.get(),
                    params=params,
                )
            )

        """
        If the decorator is called without arguments, return the decorator function itself.
        This allows the decorator to be used with or without arguments.
        """
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
        project: Optional[str],
        log_stream: Optional[str],
        params: Optional[dict[str, Union[str, Callable]]] = None,
    ) -> F:
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
            self._prepare_call(span_type, span_params, project, log_stream)
            result = None

            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                _logger.error(f"Error while executing function in async_wrapper: {e}", exc_info=True)
            finally:
                result = self._finalize_call(span_type, span_params, result, project, log_stream)

                if result is not None:
                    return result

        return cast(F, async_wrapper)

    def _sync_log(
        self,
        func: F,
        *,
        name: Optional[str],
        span_type: Optional[SPAN_TYPE],
        project: Optional[str],
        log_stream: Optional[str],
        params: Optional[dict[str, Union[str, Callable]]] = None,
    ) -> F:
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
            self._prepare_call(span_type, span_params, project, log_stream)
            result = None

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                _logger.error(f"Error while executing function in sync_wrapper: {e}", exc_info=True)
            finally:
                result = self._finalize_call(span_type, span_params, result, project, log_stream)

                if result is not None:
                    return result

        return cast(F, sync_wrapper)

    @staticmethod
    def _is_method(func: Callable) -> bool:
        """Check if a callable is likely an class or instance method based on its signature.

        Returns:
        bool: True if 'cls' or 'self' is in the callable's parameters, False otherwise.
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

            span_params["created_at"] = start_time

            return span_params
        except Exception as e:
            _logger.error(f"Failed to parse input params: {e}", exc_info=True)
            return None

    def _merge_args_with_kwargs(
        self, *, func: Callable, is_method: bool, func_args: tuple, func_kwargs: dict
    ) -> dict[str, Any]:
        """Merge positional and keyword arguments into a single dictionary."""
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
        """Return the parameter names available for each span type."""
        common_params = ["name", "input", "metadata", "tags"]
        span_params = {
            "llm": common_params + ["model", "temperature", "tools"],
            "retriever": common_params,
            "tool": common_params + ["tool_call_id"],
            "workflow": common_params,
        }
        return span_params.get(span_type, common_params)

    def _prepare_call(
        self,
        span_type: Optional[SPAN_TYPE],
        span_params: dict[str, str],
        project: Optional[str],
        log_stream: Optional[str],
    ):
        client_instance = self.get_logger_instance(project=project, log_stream=log_stream)

        stack = _span_stack_context.get().copy()
        trace = _trace_context.get()

        input = span_params.get("input", "")
        name = span_params.get("name", "")

        # If no trace is available, start a new one
        if not trace:
            trace = client_instance.start_trace(input=json.dumps(input, cls=EventSerializer), name=name)
            _trace_context.set(trace)

        # If the user hasn't specified a span type, create and add a workflow span
        if not span_type or span_type == "workflow":
            created_at = span_params.get("created_at", _get_timestamp())

            logger = self.get_logger_instance(project=project, log_stream=log_stream)
            span = logger.add_workflow_span(
                input=json.dumps(input, cls=EventSerializer), name=name, created_at=created_at
            )
            _span_stack_context.set(stack + [span])

    def _get_input_from_func_args(
        self, *, is_method: bool = False, func_args: tuple = (), func_kwargs: dict = {}
    ) -> Any:
        # Remove implicitly passed "self" or "cls" argument for instance or class methods
        logged_args = func_args[1:] if is_method else func_args
        raw_input = {"args": logged_args, "kwargs": func_kwargs}

        # Serialize and deserialize to ensure proper JSON serialization.
        return json.loads(json.dumps(raw_input, cls=EventSerializer))

    def _finalize_call(
        self,
        span_type: Optional[SPAN_TYPE],
        span_params: dict[str, str],
        result: Any,
        project: Optional[str],
        log_stream: Optional[str],
    ):
        if inspect.isgenerator(result):
            return self._wrap_sync_generator_result(span_type, span_params, result, project, log_stream)
        elif inspect.isasyncgen(result):
            return self._wrap_async_generator_result(span_type, span_params, result, project, log_stream)
        else:
            return self._handle_call_result(span_type, span_params, result, project, log_stream)

    def _handle_call_result(
        self,
        span_type: Optional[SPAN_TYPE],
        span_params: dict[str, str],
        result: Any,
        project: Optional[str],
        log_stream: Optional[str],
    ):
        try:
            output = span_params.get("output") or (
                # Serialize and deserialize to ensure proper JSON serialization.
                # Objects are later serialized again so deserialization is necessary here to avoid unnecessary escaping of quotes.
                json.loads(json.dumps(result if result is not None else None, cls=EventSerializer))
            )

            stack = _span_stack_context.get()
            _trace_context.get()

            created_at = span_params.get("created_at")
            created_at_ns = created_at.timestamp() * 1e9 if created_at else 0
            end_time_ns = int(round(_get_timestamp().timestamp() * 1e9))
            if created_at_ns:
                span_params["duration_ns"] = int(round(end_time_ns - created_at_ns))
            else:
                span_params["created_at"] = created_at
                span_params["duration_ns"] = 0

            logger = self.get_logger_instance(project=project, log_stream=log_stream)

            # If the span type is a workflow, conclude it
            if span_type == "workflow" or not span_type:
                if stack:
                    stack.pop()
                    _span_stack_context.set(stack)

                status_code = span_params.get("status_code", None)
                logger.conclude(output=output, duration_ns=span_params["duration_ns"], status_code=status_code)
            else:
                # If the span type is not a workflow, add it to the current parent (trace or span)
                span_methods = {"llm": "add_llm_span", "tool": "add_tool_span", "retriever": "add_retriever_span"}

                if span_type in span_methods:
                    method = span_methods[span_type]
                    # target = span or trace

                    kwargs = {"output": output, **span_params}

                    if span_type != "llm":
                        kwargs["input"] = json.dumps(kwargs.get("input", None), cls=EventSerializer)

                    if span_type == "llm" and "model" not in kwargs:
                        # TODO: Allow a model to be parsed from the span_params
                        # This only affects direct @log(span_type="llm") calls, not OpenAI
                        kwargs["model"] = ""

                    getattr(logger, method)(**kwargs)
        except Exception as e:
            _logger.error(f"Failed to create trace: {e}", exc_info=True)

        return result

    def _wrap_sync_generator_result(
        self,
        span_type: Optional[SPAN_TYPE],
        span_params: dict[str, str],
        generator: Generator,
        project: Optional[str],
        log_stream: Optional[str],
    ) -> Generator:
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

            self._handle_call_result(span_type, span_params, output, project, log_stream)

    async def _wrap_async_generator_result(
        self,
        span_type: Optional[SPAN_TYPE],
        span_params: dict[str, str],
        generator: AsyncGenerator,
        project: Optional[str],
        log_stream: Optional[str],
    ) -> AsyncGenerator:
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

            self._handle_call_result(span_type, span_params, output, project, log_stream)

    def get_logger_instance(self, project: Optional[str] = None, log_stream: Optional[str] = None) -> GalileoLogger:
        """Get the Galileo Logger instance for the current decorator context."""
        return GalileoLoggerSingleton().get(
            project=project or _project_context.get(), log_stream=log_stream or _log_stream_context.get()
        )

    def get_current_project(self) -> Optional[str]:
        """Retrieve the current project name from context.

        Returns:
            str | None: The current project context.
        """
        return _project_context.get()

    def get_current_log_stream(self) -> Optional[str]:
        """Retrieve the current log stream name from context.

        Returns:
            str | None: The current log stream context.
        """
        return _log_stream_context.get()

    def get_current_span_stack(self) -> list[WorkflowSpan]:
        """Retrieve the current span stack from context.

        Returns:
            List[WorkflowSpan]: The current span stack.
        """
        return _span_stack_context.get()

    def get_current_trace(self) -> Optional[Trace]:
        """Retrieve the current trace from context.

        Returns:
            Trace | None: The current trace.
        """
        return _trace_context.get()

    def flush(self, project: Optional[str] = None, log_stream: Optional[str] = None) -> None:
        """
        Upload all captured traces under a project and log stream context to Galileo.
        If no project or log stream is provided, then the currently initialized context is used.

        Args:
            project (Optional[str], optional): The project name. Defaults to None.
            log_stream (Optional[str], optional): The log stream name. Defaults to None.
        """
        self.get_logger_instance(project=project, log_stream=log_stream).flush()

    def flush_all(self) -> None:
        """
        Upload all captured traces under all contexts to Galileo.

        Args:
            project (Optional[str], optional): The project name. Defaults to None.
            log_stream (Optional[str], optional): The log stream name. Defaults to None.
        """
        GalileoLoggerSingleton().flush_all()

    def reset(self) -> None:
        """
        Resets the entire context, which also deletes all traces that haven't been flushed.

        Args:
            project (Optional[str], optional): The project name. Defaults to None.
            log_stream (Optional[str], optional): The log stream name. Defaults to None.
        """
        GalileoLoggerSingleton().reset()
        _project_context.set(None)
        _log_stream_context.set(None)
        _span_stack_context.set([])
        _trace_context.set(None)

    def init(self, project: Optional[str] = None, log_stream: Optional[str] = None) -> None:
        """
        Initialize the context with a project and log stream.

        Args:
            project (Optional[str], optional): The project name. Defaults to None.
            log_stream (Optional[str], optional): The log stream name. Defaults to None.
        """
        GalileoLoggerSingleton().reset(project=project, log_stream=log_stream)
        _project_context.set(project)
        _log_stream_context.set(log_stream)
        _span_stack_context.set([])
        _trace_context.set(None)


galileo_context = GalileoDecorator()
log = galileo_context.log
