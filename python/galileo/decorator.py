import asyncio
import inspect
import json
import logging
from contextvars import ContextVar
from functools import wraps
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    DefaultDict,
    Dict,
    Generator,
    Iterable,
    List,
    Literal,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload,
)

from typing_extensions import ParamSpec

from galileo.utils.serialization import EventSerializer

from galileo.utils.singleton import GalileoLoggerSingleton

from galileo_core.schemas.shared.traces.types import (
    StepWithChildSpans,
    Trace,
    WorkflowSpan,
)

from galileo.logger import GalileoLogger
from galileo.utils import _get_timestamp

_logger = logging.getLogger(__name__)

SPAN_TYPE = Literal["llm", "retriever", "tool", "workflow"]

# For users with mypy type checking, we need to define a TypeVar for the decorated function
# Otherwise, mypy will infer the return type of the decorated function as Any
# Docs: https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
F = TypeVar("F", bound=Callable[..., Any])

P = ParamSpec("P")
R = TypeVar("R")

_project_context: ContextVar[Optional[str]] = ContextVar(
    "project_context", default=None
)

_log_stream_context: ContextVar[Optional[str]] = ContextVar(
    "log_stream_context", default=None
)

_trace_context: ContextVar[Optional[Trace]] = ContextVar("trace_context", default=None)

_span_stack_context: ContextVar[List[WorkflowSpan]] = ContextVar(
    "span_stack_context", default=[]
)


class GalileoDecorator:
    _project: Optional[str]
    _log_stream: Optional[str]
    _previous_project_context: Optional[str]
    _previous_log_stream_context: Optional[str]
    _previous_trace_context: Optional[Trace]
    _previous_span_stack_context: Optional[List[WorkflowSpan]]

    #
    # Context manager methods
    #

    def __init__(self):
        self._previous_project_context = None
        self._previous_log_stream_context = None
        self._previous_trace_context = None
        self._previous_span_stack_context = None

    def __enter__(self):
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

    def __exit__(self, exc_type, exc_value, traceback):
        # Flush the logger instance
        self.get_logger_instance(
            project=_project_context.get(), log_stream=_log_stream_context.get()
        ).flush()

        # Restore the previous context values to avoid contamination across different usages
        _project_context.set(self._previous_project_context)
        _log_stream_context.set(self._previous_log_stream_context)
        _trace_context.set(self._previous_trace_context)
        _span_stack_context.set(self._previous_span_stack_context)

    def __call__(
        self, *, project: Optional[str] = None, log_stream: Optional[str] = None
    ):
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
        params: Optional[Dict[str, Union[str, Callable]]] = None,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

    def log(
        self,
        func: Optional[Callable[P, R]] = None,
        *,
        name: Optional[str] = None,
        span_type: Optional[SPAN_TYPE] = None,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
        params: Optional[Dict[str, Union[str, Callable]]] = None,
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
        params: Optional[Dict[str, Union[str, Callable]]] = None,
    ) -> F:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            span_params = self._prepare_input(
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
                _logger.error(
                    f"Error while executing function in async_wrapper: {e}",
                    exc_info=True,
                )
            finally:
                result = self._finalize_call(
                    span_type, span_params, result, project, log_stream
                )

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
        params: Optional[Dict[str, Union[str, Callable]]] = None,
    ) -> F:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            span_params = self._prepare_input(
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
                _logger.error(
                    f"Error while executing function in sync_wrapper: {e}",
                    exc_info=True,
                )
            finally:
                result = self._finalize_call(
                    span_type, span_params, result, project, log_stream
                )

                if result is not None:
                    return result

        return cast(F, sync_wrapper)

    @staticmethod
    def _is_method(func: Callable) -> bool:
        """Check if a callable is likely an class or instance method based on its signature.

        Returns:
        bool: True if 'cls' or 'self' is in the callable's parameters, False otherwise.
        """
        return (
            "self" in inspect.signature(func).parameters
            or "cls" in inspect.signature(func).parameters
        )

    def _prepare_input(
        self,
        *,
        name: str,
        span_type: Optional[SPAN_TYPE],
        params: Optional[Dict[str, Union[str, Callable]]] = None,
        is_method: bool = False,
        func_args: Tuple = (),
        func_kwargs: Dict = {},
    ) -> Optional[dict[str, str]]:
        try:
            start_time = _get_timestamp()

            # input = self._get_input_from_func_args(
            #     is_method=is_method, func_args=func_args, func_kwargs=func_kwargs
            # )

            # Extract function args
            input = self._merge_args_with_kwargs(
                is_method=is_method,
                func_args=func_args,
                func_kwargs=func_kwargs,
            )

            # Process parameter mappings supplied by the user via `params`
            span_params = {}
            if params:
                for span_param, mapping in params.items():
                    if callable(mapping):
                        # If mapping is a function, call it with the merged args
                        span_params[span_param] = mapping(input)
                    elif span_param.startswith("$"):
                        # Handle static values (prefixed with $)
                        span_params[span_param] = func_param[1:]
                    else:
                        # If mapping is a string, use it as a key to get value from merged args
                        if mapping in input:
                            span_params[span_param] = input[mapping]

            # Auto-map matching parameters if they exist in merged_args
            # This will fill in any missing span parameters based on the function signature
            if span_type:
                span_param_names = self._get_span_param_names(span_type)
                for param_name in span_param_names:
                    if param_name in input and param_name not in span_params:
                        span_params[param_name] = input[param_name]

            if "name" not in span_params:
                span_params["name"] = name

            if "input" not in span_params:
                span_params["input"] = input

            span_params["created_at_ns"] = start_time.timestamp() * 1e9

            # params = {
            #     "name": name,
            #     "start_time": start_time,
            #     "input": input,
            #     "span_params": span_params,
            # }
            # return params

            return span_params
        except Exception as e:
            _logger.error(f"Failed to parse input params: {e}", exc_info=True)
            return None

    def _merge_args_with_kwargs(
        self,
        *,
        is_method: bool,
        func_args: Tuple,
        func_kwargs: Dict,
    ) -> Dict[str, Any]:
        """Merge positional and keyword arguments into a single dictionary."""
        # Get the function's signature
        func = func_args[0] if is_method else None
        if func:
            sig = inspect.signature(func)

            parameters = list(sig.parameters.keys())

            for name, param in sig.parameters.items():
                if name not in ("self", "cls"):  # Skip self and cls
                    if param.default is not inspect.Parameter.empty:
                        parameters[name] = param.default

            # Remove 'self' or 'cls' if it's a method
            # if is_method:
            #     parameters = parameters[1:]

            # Create dictionary of positional args
            args_dict = {
                param: value
                for param, value in zip(
                    parameters, func_args[1:] if is_method else func_args
                )
            }

            # Merge with kwargs
            return {**args_dict, **func_kwargs}
        return func_kwargs

    def _get_span_param_names(self, span_type: SPAN_TYPE) -> List[str]:
        """Return the parameter names available for each span type."""
        common_params = ["name", "input", "metadata"]
        span_params = {
            "llm": common_params + ["model", "temperature", "tools", "ground_truth"],
            "retriever": common_params + ["documents"],
            "tool": common_params,
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
        client_instance = self.get_logger_instance(
            project=project, log_stream=log_stream
        )

        stack = _span_stack_context.get().copy()
        trace = _trace_context.get()

        input = span_params.get("input", "")
        name = span_params.get("name", "")

        # If no trace is available, start a new one
        if not trace:
            trace = client_instance.start_trace(input=input, name=name)
            _trace_context.set(trace)

        # If the user hasn't specified a span type, create and add a workflow span
        if not span_type or span_type == "workflow":
            parent_span = stack[-1] if len(stack) else None
            created_at_ns = span_params.get(
                "created_at_ns", _get_timestamp().timestamp() * 1e9
            )

            if parent_span:
                span = parent_span.add_workflow_span(
                    input=input,
                    name=name,
                    created_at_ns=created_at_ns,
                )
            else:
                span = trace.add_workflow_span(
                    input=input,
                    name=name,
                    created_at_ns=created_at_ns,
                )
            _span_stack_context.set(stack + [span])

    def _get_input_from_func_args(
        self, *, is_method: bool = False, func_args: Tuple = (), func_kwargs: Dict = {}
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
            return self._wrap_sync_generator_result(
                span_type, span_params, result, project, log_stream
            )
        elif inspect.isasyncgen(result):
            return self._wrap_async_generator_result(
                span_type, span_params, result, project, log_stream
            )
        else:
            return self._handle_call_result(
                span_type, span_params, result, project, log_stream
            )

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
                json.loads(
                    json.dumps(
                        result if result is not None else None, cls=EventSerializer
                    )
                )
            )

            stack = _span_stack_context.get()
            trace = _trace_context.get()

            created_at_ns = span_params.get("created_at_ns")
            end_time_ns = int(round(_get_timestamp().timestamp() * 1e9))
            if created_at_ns:
                span_params["duration_ns"] = int(round((end_time_ns - created_at_ns)))
            else:
                # created_at_ns = None
                span_params["created_at_ns"] = end_time_ns
                span_params["duration_ns"] = 0

            span = None

            # If the span type is a workflow, conclude it
            if span_type == "workflow" or not span_type:
                if stack:
                    span = stack.pop()
                    _span_stack_context.set(stack)

                if span:
                    span.conclude(output=output, duration_ns=span_params["duration_ns"])
                if len(stack) == 0:
                    trace.conclude(
                        output=output, duration_ns=span_params["duration_ns"]
                    )
            else:
                # If the span type is not a workflow, add it to the current parent (trace or span)
                if len(stack):
                    span = stack[-1]
                span_methods = {
                    "llm": "add_llm_span",
                    "tool": "add_tool_span",
                    "retriever": "add_retriever_span",
                }

                if span_type in span_methods:
                    method = span_methods[span_type]
                    target = span or trace

                    # span_params.pop("start_time")

                    kwargs = {
                        # "input": span_params.get("input"),
                        "output": output,
                        # "name": span_params.get("name"),
                        # "created_at_ns": created_at_ns,
                        # "duration_ns": duration_ns,
                        **span_params,
                    }

                    print(kwargs)

                    if span_type == "llm" and "model" not in kwargs:
                        # TODO: Allow a model to be parsed from the span_params
                        # This only affects direct @log(span_type="llm") calls, not OpenAI
                        kwargs["model"] = ""

                    getattr(target, method)(**kwargs)
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
    ):
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

            self._handle_call_result(
                span_type, span_params, output, project, log_stream
            )

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

            self._handle_call_result(
                span_type, span_params, output, project, log_stream
            )

    def get_logger_instance(
        self, project: Optional[str] = None, log_stream: Optional[str] = None
    ) -> GalileoLogger:
        """Get the Galileo Logger instance for the current decorator context."""
        return GalileoLoggerSingleton().get(
            project=project or _project_context.get(),
            log_stream=log_stream or _log_stream_context.get(),
        )

    def get_current_project(self) -> str | None:
        """Retrieve the current project name from context.

        Returns:
            str | None: The current project context.
        """
        return _project_context.get()

    def get_current_log_stream(self) -> str | None:
        """Retrieve the current log stream name from context.

        Returns:
            str | None: The current log stream context.
        """
        return _log_stream_context.get()

    def get_current_span_stack(self) -> List[WorkflowSpan]:
        """Retrieve the current span stack from context.

        Returns:
            List[WorkflowSpan]: The current span stack.
        """
        return _span_stack_context.get()

    def get_current_trace(self) -> Trace | None:
        """Retrieve the current trace from context.

        Returns:
            Trace | None: The current trace.
        """
        return _trace_context.get()

    def flush(self, project: Optional[str] = None, log_stream: Optional[str] = None):
        """
        Upload all captured traces to Galileo.

        Args:
            project (Optional[str], optional): The project name. Defaults to None.
            log_stream (Optional[str], optional): The log stream name. Defaults to None.
        """
        self.get_logger_instance(project=project, log_stream=log_stream).flush()


galileo_context = GalileoDecorator()
log = galileo_context.log
