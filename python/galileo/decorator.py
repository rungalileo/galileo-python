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

from galileo_core.schemas.shared.traces.types import StepWithChildSpans

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

_span_stack_context: ContextVar[List[StepWithChildSpans]] = ContextVar(
    "span_stack_context", default=[]
)


class GalileoDecorator:
    _project: Optional[str]
    _log_stream: Optional[str]
    _previous_project_context: Optional[str]
    _previous_log_stream_context: Optional[str]

    #
    # Context manager methods
    #

    def __init__(self):
        self._previous_project_context = None
        self._previous_log_stream_context = None

    def __enter__(self):
        """
        Entry point for the context manager.
        """
        self._previous_project_context = _project_context.get()
        self._previous_log_stream_context = _log_stream_context.get()

        if self._project is not None:
            _project_context.set(self._project)
        if self._log_stream is not None:
            _log_stream_context.set(self._log_stream)

        return self  # Allows `as galileo` usage

    def __exit__(self, exc_type, exc_value, traceback):
        # Restore the previous context values to avoid contamination across different usages
        _project_context.set(self._previous_project_context)
        _log_stream_context.set(self._previous_log_stream_context)

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
    ) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

    def log(
        self,
        func: Optional[Callable[P, R]] = None,
        *,
        name: Optional[str] = None,
        span_type: Optional[SPAN_TYPE] = None,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:

        def decorator(func: Callable[P, R]) -> Callable[P, R]:

            return (
                self._async_log(
                    func,
                    name=name,
                    span_type=span_type,
                    project=project or _project_context.get(),
                    log_stream=log_stream or _log_stream_context.get(),
                )
                if asyncio.iscoroutinefunction(func)
                else self._sync_log(
                    func,
                    name=name,
                    span_type=span_type,
                    project=project or _project_context.get(),
                    log_stream=log_stream or _log_stream_context.get(),
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
    ) -> F:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            input_params = self._prepare_input(
                name=name or func.__name__,
                span_type=span_type,
                is_method=self._is_method(func),
                func_args=args,
                func_kwargs=kwargs,
            )
            self._prepare_call(span_type, input_params, project, log_stream)
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
                    span_type, input_params, result, project, log_stream
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
    ) -> F:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            input_params = self._prepare_input(
                name=name or func.__name__,
                is_method=self._is_method(func),
                func_args=args,
                func_kwargs=kwargs,
            )
            self._prepare_call(span_type, input_params, project, log_stream)
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
                    span_type, input_params, result, project, log_stream
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
        is_method: bool = False,
        func_args: Tuple = (),
        func_kwargs: Dict = {},
    ) -> Optional[dict[str, str]]:
        try:
            start_time = _get_timestamp()

            input = self._get_input_from_func_args(
                is_method=is_method,
                func_args=func_args,
                func_kwargs=func_kwargs,
            )

            params = {
                "id": id,
                "name": name,
                "start_time": start_time,
                "input": input,
            }

            return params
        except Exception as e:
            _logger.error(f"Failed to parse input params: {e}", exc_info=True)

    def _prepare_call(
        self,
        span_type: Optional[SPAN_TYPE],
        input_params: dict[str, str],
        project: Optional[str],
        log_stream: Optional[str],
    ):
        client_instance = self.get_client_instance(
            project=project, log_stream=log_stream
        )

        traces = client_instance.traces

        stack = _span_stack_context.get().copy()

        # Check if we need to start a new trace (empty call stack)
        # If not, reuse the last trace
        if not len(stack) or not len(traces):
            trace = client_instance.start_trace(
                input=input_params.get("input"),
                name=input_params.get("name"),
            )
        else:
            trace = traces[-1]

        # If the user hasn't specified a span type, create and add a workflow span
        if not span_type or span_type == "workflow":
            created_at_ns = input_params.get("start_time").timestamp() * 1e9

            span = trace.add_workflow_span(
                input=input_params.get("input"),
                name=input_params.get("name"),
                created_at_ns=created_at_ns,
            )
            _span_stack_context.set(stack + [span])

    def _get_input_from_func_args(
        self,
        *,
        is_method: bool = False,
        func_args: Tuple = (),
        func_kwargs: Dict = {},
    ) -> Any:
        # Remove implicitly passed "self" or "cls" argument for instance or class methods
        logged_args = func_args[1:] if is_method else func_args
        raw_input = {
            "args": logged_args,
            "kwargs": func_kwargs,
        }

        # Serialize and deserialize to ensure proper JSON serialization.
        return json.loads(json.dumps(raw_input, cls=EventSerializer))

    def _finalize_call(
        self,
        span_type: Optional[SPAN_TYPE],
        input_params: dict[str, str],
        result: Any,
        project: Optional[str],
        log_stream: Optional[str],
    ):
        if inspect.isgenerator(result):
            return self._wrap_sync_generator_result(
                span_type, input_params, result, project, log_stream
            )
        elif inspect.isasyncgen(result):
            return self._wrap_async_generator_result(
                span_type, input_params, result, project, log_stream
            )
        else:
            return self._handle_call_result(
                span_type, input_params, result, project, log_stream
            )

    def _handle_call_result(
        self,
        span_type: Optional[SPAN_TYPE],
        input_params: dict[str, str],
        result: Any,
        project: Optional[str],
        log_stream: Optional[str],
    ):
        try:
            end_time = input_params.get("end_time") or _get_timestamp()

            output = input_params.get("output") or (
                # Serialize and deserialize to ensure proper JSON serialization.
                # Objects are later serialized again so deserialization is necessary here to avoid unnecessary escaping of quotes.
                json.loads(
                    json.dumps(
                        result if result is not None else None,
                        cls=EventSerializer,
                    )
                )
            )

            input_params.update(end_time=end_time, output=output)

            client_instance = self.get_client_instance(
                project=project, log_stream=log_stream
            )

            created_at_ns = int(round(input_params.get("start_time").timestamp() * 1e9))
            duration_ns = int(
                round((end_time - input_params.get("start_time")).total_seconds() * 1e9)
            )

            if span_type == "llm":
                client_instance.add_llm_span(
                    input=input_params.get("input"),
                    output=output,
                    name=input_params.get("name"),
                    model="",
                    created_at_ns=created_at_ns,
                    duration_ns=duration_ns,
                )
            elif span_type == "tool":
                client_instance.add_tool_span(
                    input=input_params.get("input"),
                    output=output,
                    name=input_params.get("name"),
                    created_at_ns=created_at_ns,
                    duration_ns=duration_ns,
                )
            elif span_type == "retriever":
                client_instance.add_retriever_span(
                    input=input_params.get("input"),
                    output=output,
                    name=input_params.get("name"),
                    documents=[],
                    created_at_ns=created_at_ns,
                    duration_ns=duration_ns,
                )
            else:
                # Conclude the workflow span
                client_instance.conclude(
                    output=output,
                    duration_ns=duration_ns,
                )

            # If the span type is a workflow, conclude it
            if span_type == "workflow" or not span_type:
                stack = _span_stack_context.get()
                span = None
                if stack:
                    span = stack.pop()
                    _span_stack_context.set(stack)

                if span:
                    span.conclude(
                        output=output,
                        duration_ns=duration_ns,
                    )
                if len(stack) == 0:
                    # Conclude the trace if the call stack is empty
                    client_instance.traces[-1].conclude(
                        output=output,
                        duration_ns=duration_ns,
                    )

        except Exception as e:
            _logger.error(f"Failed to create trace: {e}", exc_info=True)

        return result

    def _wrap_sync_generator_result(
        self,
        span_type: Optional[SPAN_TYPE],
        input_params: dict[str, str],
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
                span_type, input_params, output, project, log_stream
            )

    async def _wrap_async_generator_result(
        self,
        span_type: Optional[SPAN_TYPE],
        input_params: dict[str, str],
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
                span_type, input_params, output, project, log_stream
            )

    def get_client_instance(
        self, project: Optional[str], log_stream: Optional[str]
    ) -> GalileoLogger:
        """Get the Galileo Logger instance for the current decorator context."""
        return GalileoLoggerSingleton().get(
            project=project or _project_context.get(),
            log_stream=log_stream or _log_stream_context.get(),
        )


galileo_context = GalileoDecorator()
log = galileo_context.log
