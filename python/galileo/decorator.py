import asyncio
import inspect
import json
import logging
from collections import defaultdict
from contextvars import ContextVar
from datetime import datetime
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

import httpx
from pydantic import BaseModel
from typing_extensions import ParamSpec

from galileo.utils.serialization import EventSerializer

from galileo.utils.singleton import GalileoLoggerSingleton
from galileo_core.schemas.shared.traces.trace import (
    Trace,
    LlmSpan,
    WorkflowSpan,
    RetrieverSpan,
    ToolSpan,
)

from galileo.logger import GalileoLogger
from galileo.utils import _get_timestamp

# For users with mypy type checking, we need to define a TypeVar for the decorated function
# Otherwise, mypy will infer the return type of the decorated function as Any
# Docs: https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
F = TypeVar("F", bound=Callable[..., Any])

P = ParamSpec("P")
R = TypeVar("R")


class GalileoDecorator:
    @overload
    def log(self, func: F) -> F: ...

    @overload
    def log(
        self,
        func: None = None,
        *,
        name: Optional[str] = None,
        span_type: Optional[Literal["llm"]] = None,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

    def log(
        self,
        func: Optional[Callable[P, R]] = None,
        *,
        name: Optional[str] = None,
        span_type: Optional[Literal["llm"]] = None,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:

        def decorator(func: Callable[P, R]) -> Callable[P, R]:
            return (
                self._async_log(func, name=name, span_type=span_type)
                if asyncio.iscoroutinefunction(func)
                else self._sync_log(func, name=name, span_type=span_type)
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
        span_type: Optional[Literal["llm"]],
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
            result = None

            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                print("Error while executing function in async_wrapper: ", e)
            finally:
                result = self._finalize_call(span_type, input_params, result)

                if result is not None:
                    return result

        return cast(F, async_wrapper)

    def _sync_log(
        self,
        func: F,
        *,
        name: Optional[str],
        span_type: Optional[Literal["llm"]],
    ) -> F:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            input_params = self._prepare_input(
                name=name or func.__name__,
                is_method=self._is_method(func),
                func_args=args,
                func_kwargs=kwargs,
            )
            result = None

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                print("Error while executing function in sync_wrapper: ", e)
            finally:
                result = self._finalize_call(span_type, input_params, result)

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
            print(f"Failed to parse input params: {e}")

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
        span_type: Optional[Literal["llm"]],
        input_params: dict[str, str],
        result: Any,
    ):
        if inspect.isgenerator(result):
            return self._wrap_sync_generator_result(span_type, input_params, result)
        elif inspect.isasyncgen(result):
            return self._wrap_async_generator_result(span_type, input_params, result)
        else:
            return self._handle_call_result(span_type, input_params, result)

    def _handle_call_result(
        self,
        span_type: Optional[Literal["llm"]],
        input_params: dict[str, str],
        result: Any,
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

            traces = self.client_instance.traces

            created_at_ns = input_params.get("start_time").timestamp() * 1e9
            duration_ns = (
                end_time - input_params.get("start_time")
            ).total_seconds() * 1e9

            if not len(traces):
                trace = self.client_instance.add_trace(
                    input=input_params.get("input"),
                    name=input_params.get("name"),
                )
            else:
                trace = traces[-1]

            if span_type == "llm":
                trace.add_llm_span(
                    input=input_params.get("input"),
                    output=output,
                    name=input_params.get("name"),
                    model="",
                    created_at_ns=created_at_ns,
                    duration_ns=duration_ns,
                )
            elif span_type == "tool":
                trace.add_tool_span(
                    input=input_params.get("input"),
                    output=output,
                    name=input_params.get("name"),
                    created_at_ns=created_at_ns,
                    duration_ns=duration_ns,
                )
            else:
                trace.add_retriever_span(
                    input=input_params.get("input"),
                    output=output,
                    name=input_params.get("name"),
                    documents=[],
                    created_at_ns=created_at_ns,
                    duration_ns=duration_ns,
                )

            trace.conclude(output=output, duration_ns=duration_ns)

        except Exception as e:
            print(f"Failed to create trace: {e}")

        return result

    def _wrap_sync_generator_result(
        self,
        span_type: Optional[Literal["llm"]],
        input_params: dict[str, str],
        generator: Generator,
    ):
        items = []

        try:
            for item in generator:
                items.append(item)

                yield item
        except Exception as e:
            print(f"Failed to wrap generator result: {e}")
        finally:
            output = items

            if all(isinstance(item, str) for item in items):
                output = "".join(items)

            self._handle_call_result(span_type, input_params, output)

    async def _wrap_async_generator_result(
        self,
        span_type: Optional[Literal["llm"]],
        input_params: dict[str, str],
        generator: AsyncGenerator,
    ) -> AsyncGenerator:
        items = []

        try:
            async for item in generator:
                items.append(item)

                yield item
        except Exception as e:
            print(f"Failed to wrap generator result: {e}")
        finally:
            output = items

            if all(isinstance(item, str) for item in items):
                output = "".join(items)

            self._handle_call_result(span_type, input_params, output)

    def flush(self):
        if self.client_instance:
            self.client_instance.flush()
        else:
            print("No Galileo Logger instance found in the current context")

    def configure(
        self,
        *,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
    ):
        galileo_logger_singleton = GalileoLoggerSingleton()
        galileo_logger_singleton.reset()

        galileo_logger_singleton.get(
            project=project,
            log_stream=log_stream,
        )

    @property
    def client_instance(self) -> GalileoLogger:
        """Get the Galileo Logger instance for the current decorator context."""
        return GalileoLoggerSingleton().get()


galileo_context = GalileoDecorator()
log = galileo_context.log
