"""
Galileo wrapper for OpenAI that automatically logs prompts and responses.

This module provides a drop-in replacement for the OpenAI library that automatically
logs all prompts, responses, and related metadata to Galileo. It works by intercepting
calls to the OpenAI API and logging them using the Galileo logging system.

Note that the original OpenAI package is still required as a project dependency to use this wrapper.

Examples
--------
# Import the wrapped OpenAI client instead of the original
from galileo.openai import openai

# Use it exactly as you would use the regular OpenAI client
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me about the solar system."}
    ]
)

# All prompts and responses are automatically logged to Galileo
print(response.choices[0].message.content)

# You can also use it with the galileo_context for more control
from galileo import galileo_context

with galileo_context(project="my-project", log_stream="my-log-stream"):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Tell me about the solar system."}
        ]
    )
"""

import logging
import types
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from inspect import isclass
from typing import Any, Callable, Optional

from pydantic import BaseModel
from wrapt import wrap_function_wrapper  # type: ignore[import-untyped]

from galileo import GalileoLogger
from galileo.decorator import galileo_context
from galileo.utils import _get_timestamp
from galileo.utils.serialization import serialize_to_str

try:
    import openai
    import openai.resources
    from openai._types import NotGiven
    from openai.types.chat import ChatCompletionMessageToolCall

    # it's used only for version check of OpenAI
    from packaging.version import Version
except ImportError:
    raise ModuleNotFoundError("Please install OpenAI to use this feature: 'pip install openai'")

try:
    from openai import AsyncAzureOpenAI, AsyncOpenAI, AzureOpenAI, NoneType, OpenAI  # noqa: F401
except ImportError:
    AsyncAzureOpenAI = None  # type: ignore[assignment]
    AsyncOpenAI = None  # type: ignore[assignment]
    AzureOpenAI = None  # type: ignore[assignment]
    OpenAI = None  # type: ignore[assignment]


@dataclass
class OpenAiModuleDefinition:
    module: str
    object: str
    method: str
    type: str
    sync: bool
    min_version: Optional[str] = None


@dataclass
class OpenAiInputData:
    name: str
    metadata: dict
    start_time: datetime
    input: str
    model_parameters: dict
    model: Optional[str]
    temperature: float
    tools: Optional[list[dict]]


_logger = logging.getLogger(__name__)


OPENAI_CLIENT_METHODS = [
    OpenAiModuleDefinition(
        module="openai.resources.chat.completions", object="Completions", method="create", type="chat", sync=True
    )
    # Eventually add more OpenAI client library methods here
]


class OpenAiArgsExtractor:
    def __init__(self, name: Optional[str] = None, metadata: Optional[dict] = None, **kwargs: Any) -> None:
        self.args = {
            "name": name,
            "metadata": (
                metadata
                if "response_format" not in kwargs
                else {
                    **(metadata or {}),
                    "response_format": (
                        kwargs["response_format"].model_json_schema()
                        if isclass(kwargs["response_format"]) and issubclass(kwargs["response_format"], BaseModel)
                        else kwargs["response_format"]
                    ),
                }
            ),
        }
        self.kwargs = kwargs

    def get_galileo_args(self) -> dict[str, Any]:
        return {**self.args, **self.kwargs}

    def get_openai_args(self) -> dict[str, Any]:
        # If OpenAI model distillation is enabled, we need to add the metadata to the kwargs
        # https://platform.openai.com/docs/guides/distillation
        if self.kwargs.get("store", False):
            self.kwargs["metadata"] = self.args.get("metadata", {})

            # OpenAI does not support non-string type values in metadata when using
            # model distillation feature
            self.kwargs["metadata"].pop("response_format", None)

        return self.kwargs


def _galileo_wrapper(func: Callable) -> Callable:
    def _with_galileo(open_ai_definitions: OpenAiModuleDefinition, initialize: Callable) -> Callable:
        def wrapper(wrapped: Callable, instance: Any, args: dict, kwargs: dict) -> Any:
            return func(open_ai_definitions, initialize, wrapped, args, kwargs)

        return wrapper

    return _with_galileo


def _extract_chat_response(kwargs: dict) -> dict:
    """Extracts the llm output from the response."""
    response = {"role": kwargs.get("role", None)}

    if kwargs.get("function_call") is not None and type(kwargs["function_call"]) is dict:
        response.update(
            {
                "tool_calls": [
                    {
                        "id": "",
                        "function": {
                            "name": kwargs["function_call"].get("name", ""),
                            "arguments": kwargs["function_call"].get("arguments", ""),
                        },
                    }
                ]
            }
        )
    elif kwargs.get("tool_calls") is not None and type(kwargs["tool_calls"]) is list:
        tool_calls = []
        for tool_call in kwargs["tool_calls"]:
            try:
                tool_call = ChatCompletionMessageToolCall.model_validate(tool_call)
                tool_calls.append(
                    {
                        "id": tool_call.id,
                        "function": {"name": tool_call.function.name, "arguments": tool_call.function.arguments},
                    }
                )
            except Exception as e:
                _logger.error(f"Error processing tool call: {e}")

        response.update({"tool_calls": tool_calls if len(tool_calls) else None})

    response.update({"content": kwargs.get("content", "")})

    return response


def _extract_input_data_from_kwargs(
    resource: OpenAiModuleDefinition, start_time: datetime, kwargs: dict[str, Any]
) -> OpenAiInputData:
    name: str = kwargs.get("name", "openai-client-generation")

    if name is not None and not isinstance(name, str):
        raise TypeError("name must be a string")

    metadata: dict = kwargs.get("metadata", {})

    if metadata is not None and not isinstance(metadata, dict):
        raise TypeError("metadata must be a dictionary")

    model = kwargs.get("model", None) or None

    prompt = None

    if resource.type == "completion":
        prompt = kwargs.get("prompt", None)
    elif resource.type == "chat":
        prompt = kwargs.get("messages", [])

    parsed_temperature = float(
        kwargs.get("temperature", 1) if not isinstance(kwargs.get("temperature", 1), NotGiven) else 1
    )

    parsed_max_tokens = (
        kwargs.get("max_tokens", float("inf"))
        if not isinstance(kwargs.get("max_tokens", float("inf")), NotGiven)
        else float("inf")
    )

    parsed_top_p = kwargs.get("top_p", 1) if not isinstance(kwargs.get("top_p", 1), NotGiven) else 1

    parsed_frequency_penalty = (
        kwargs.get("frequency_penalty", 0) if not isinstance(kwargs.get("frequency_penalty", 0), NotGiven) else 0
    )

    parsed_presence_penalty = (
        kwargs.get("presence_penalty", 0) if not isinstance(kwargs.get("presence_penalty", 0), NotGiven) else 0
    )

    parsed_seed = kwargs.get("seed", None) if not isinstance(kwargs.get("seed", None), NotGiven) else None

    parsed_n = kwargs.get("n", 1) if not isinstance(kwargs.get("n", 1), NotGiven) else 1

    parsed_tools = kwargs.get("tools", None) if not isinstance(kwargs.get("tools", None), NotGiven) else None

    parsed_tool_choice = (
        kwargs.get("tool_choice", None) if not isinstance(kwargs.get("tool_choice", None), NotGiven) else None
    )

    # handle deprecated aliases (functions for tools, function_call for tool_choice)
    if parsed_tools is None and kwargs.get("functions") is not None:
        parsed_tools = kwargs["functions"]

    if parsed_tool_choice is None and kwargs.get("function_call") is not None:
        parsed_tool_choice = kwargs["function_call"]

    model_parameters = {
        "temperature": parsed_temperature,
        "max_tokens": parsed_max_tokens,
        "top_p": parsed_top_p,
        "frequency_penalty": parsed_frequency_penalty,
        "presence_penalty": parsed_presence_penalty,
        "tool_choice": parsed_tool_choice,
    }
    if parsed_n is not None and parsed_n > 1:
        model_parameters["n"] = parsed_n

    if parsed_seed is not None:
        model_parameters["seed"] = parsed_seed

    return OpenAiInputData(
        name=name,
        metadata=metadata,
        start_time=start_time,
        # TODO: galileo/openai.py:229: error:
        # Argument "input" to "OpenAiInputData" has incompatible type "Any | None"; expected "str"  [arg-type]
        input=prompt,  # type: ignore[arg-type]
        model_parameters=model_parameters,
        model=model or None,
        temperature=parsed_temperature,
        tools=parsed_tools,
    )


def _parse_usage(usage: Optional[dict] = None) -> Optional[dict]:
    if usage is None:
        return None

    usage_dict = usage.copy() if isinstance(usage, dict) else usage.__dict__

    for tokens_details in ["prompt_tokens_details", "completion_tokens_details"]:
        if tokens_details in usage_dict and usage_dict[tokens_details] is not None:
            tokens_details_dict = (
                usage_dict[tokens_details]
                if isinstance(usage_dict[tokens_details], dict)
                else usage_dict[tokens_details].__dict__
            )
            usage_dict[tokens_details] = {k: v for k, v in tokens_details_dict.items() if v is not None}

    return usage_dict


def _extract_data_from_default_response(resource: OpenAiModuleDefinition, response: dict[str, Any]) -> Any:
    if response is None:
        return None, "<NoneType response returned from OpenAI>", None

    model = response.get("model", None) or None

    completion = None
    if resource.type == "completion":
        choices = response.get("choices", [])
        if len(choices) > 0:
            choice = choices[-1]

            completion = choice.text if _is_openai_v1() else choice.get("text", None)
    elif resource.type == "chat":
        choices = response.get("choices", [])
        if len(choices):
            if len(choices) > 1:
                completion = [
                    (
                        _extract_chat_response(choice.message.__dict__)
                        if _is_openai_v1()
                        else choice.get("message", None)
                    )
                    for choice in choices
                ]
            else:
                choice = choices[0]
                completion = (
                    _extract_chat_response(choice.message.__dict__) if _is_openai_v1() else choice.get("message", None)
                )

    usage = _parse_usage(response.get("usage", None))

    return model, completion, usage


def _extract_streamed_openai_response(resource, chunks):
    completion = defaultdict(str) if resource.type == "chat" else ""
    model, usage = None, None

    for chunk in chunks:
        if _is_openai_v1():
            chunk = chunk.__dict__

        model = model or chunk.get("model", None) or None
        usage = chunk.get("usage", None)

        choices = chunk.get("choices", [])

        for choice in choices:
            if _is_openai_v1():
                choice = choice.__dict__
            if resource.type == "chat":
                delta = choice.get("delta", None)

                if _is_openai_v1():
                    delta = delta.__dict__

                if delta.get("role", None) is not None:
                    completion["role"] = delta["role"]

                if delta.get("content", None) is not None:
                    completion["content"] = (
                        delta.get("content", None)
                        if completion["content"] is None
                        else completion["content"] + delta.get("content", None)
                    )
                elif delta.get("function_call", None) is not None:
                    curr = completion["function_call"]
                    tool_call_chunk = delta.get("function_call", None)

                    if not curr:
                        completion["function_call"] = {
                            "name": getattr(tool_call_chunk, "name", ""),
                            "arguments": getattr(tool_call_chunk, "arguments", ""),
                        }

                    else:
                        curr["name"] = curr["name"] or getattr(tool_call_chunk, "name", None)
                        curr["arguments"] += getattr(tool_call_chunk, "arguments", "")

                elif delta.get("tool_calls", None) is not None:
                    curr = completion["tool_calls"]
                    tool_call_chunk = getattr(delta.get("tool_calls", None)[0], "function", None)

                    if not curr:
                        completion["tool_calls"] = [
                            {
                                "name": getattr(tool_call_chunk, "name", ""),
                                "arguments": getattr(tool_call_chunk, "arguments", ""),
                            }
                        ]

                    elif getattr(tool_call_chunk, "name", None) is not None:
                        curr.append(
                            {
                                "name": getattr(tool_call_chunk, "name", None),
                                "arguments": getattr(tool_call_chunk, "arguments", None),
                            }
                        )

                    else:
                        curr[-1]["name"] = curr[-1]["name"] or getattr(tool_call_chunk, "name", None)
                        curr[-1]["arguments"] += getattr(tool_call_chunk, "arguments", None)

            if resource.type == "completion":
                completion += choice.get("text", None)

    def get_response_for_chat():
        return (
            completion["content"]
            or (completion["function_call"] and {"role": "assistant", "function_call": completion["function_call"]})
            or (
                completion["tool_calls"]
                and {"role": "assistant", "tool_calls": [{"function": data} for data in completion["tool_calls"]]}
            )
            or None
        )

    return (model, get_response_for_chat() if resource.type == "chat" else completion, usage)


def _is_openai_v1() -> bool:
    return Version(openai.__version__) >= Version("1.0.0")


def _is_streaming_response(response):
    return isinstance(response, types.GeneratorType) or (_is_openai_v1() and isinstance(response, openai.Stream))


@_galileo_wrapper
def _wrap(
    open_ai_resource: OpenAiModuleDefinition, initialize: Callable, wrapped: Callable, args: dict, kwargs: dict
) -> Any:
    # Retrieve the decorator context
    decorator_context_trace = galileo_context.get_current_trace()

    start_time = _get_timestamp()
    arg_extractor = OpenAiArgsExtractor(*args, **kwargs)

    input_data = _extract_input_data_from_kwargs(open_ai_resource, start_time, arg_extractor.get_galileo_args())

    galileo_logger: GalileoLogger = initialize()

    should_complete_trace = False
    if decorator_context_trace:
        pass
    else:
        # If we don't have an active trace, start a new trace
        # We will conclude it at the end
        galileo_logger.start_trace(input=serialize_to_str(input_data.input), name=input_data.name)
        should_complete_trace = True

    try:
        openai_response = wrapped(**arg_extractor.get_openai_args())

        if _is_streaming_response(openai_response):
            # extract data from streaming reponse
            return ResponseGeneratorSync(
                resource=open_ai_resource,
                response=openai_response,
                input_data=input_data,
                logger=galileo_logger,
                should_complete_trace=should_complete_trace,
            )
        else:
            model, completion, usage = _extract_data_from_default_response(
                open_ai_resource,
                ((openai_response and openai_response.__dict__) if _is_openai_v1() else openai_response),
            )

            if usage is None:
                usage = {}

            end_time = _get_timestamp()

            duration_ns = int(round((end_time - start_time).total_seconds() * 1e9))

            # Add a span to the current trace or span (if this is a nested trace)
            galileo_logger.add_llm_span(
                input=input_data.input,
                output=completion,
                tools=input_data.tools,
                name=input_data.name,
                model=model,
                temperature=input_data.temperature,
                duration_ns=duration_ns,
                num_input_tokens=usage.get("prompt_tokens", 0),
                num_output_tokens=usage.get("completion_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
                metadata={str(k): str(v) for k, v in input_data.model_parameters.items()},
                # openai client library doesn't return http_status code, so we only can hardcode it here
                # because we if we parsed and extracted data from response it means we get it and it's 200OK
                status_code=200,
            )

            # Conclude the trace if this is the top-level call
            if should_complete_trace:
                galileo_logger.conclude(output=serialize_to_str(completion), duration_ns=duration_ns)

        return openai_response
    except Exception as ex:
        _logger.error(f"Error while processing OpenAI request: {ex}")
        raise RuntimeError("Failed to process the OpenAI Request") from ex


class ResponseGeneratorSync:
    """
    A wrapper for OpenAI streaming responses that logs the response to Galileo.

    This class wraps the OpenAI streaming response generator and logs the response
    to Galileo when the generator is exhausted. It implements the iterator protocol
    to allow for streaming responses.

    Attributes
    ----------
    resource : OpenAiModuleDefinition
        The OpenAI resource definition.
    response : Generator or openai.Stream
        The OpenAI streaming response.
    input_data : OpenAiInputData
        The input data for the OpenAI request.
    logger : GalileoLogger
        The Galileo logger instance.
    should_complete_trace : bool
        Whether to complete the trace when the generator is exhausted.
    """

    def __init__(self, *, resource, response, input_data, logger: GalileoLogger, should_complete_trace: bool):
        self.items = []
        self.resource = resource
        self.response = response
        self.input_data = input_data
        self.logger = logger
        self.should_complete_trace = should_complete_trace
        self.completion_start_time = None

    def __iter__(self):
        try:
            for i in self.response:
                self.items.append(i)

                if self.completion_start_time is None:
                    self.completion_start_time = _get_timestamp()

                yield i
        finally:
            self._finalize()

    def __next__(self):
        try:
            item = self.response.__next__()
            self.items.append(item)

            if self.completion_start_time is None:
                self.completion_start_time = _get_timestamp()

            return item

        except StopIteration:
            self._finalize()

            raise

    def __enter__(self):
        return self.__iter__()

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _finalize(self):
        model, completion, usage = _extract_streamed_openai_response(self.resource, self.items)

        if usage is None:
            usage = {}

        end_time = _get_timestamp()
        # TODO: make sure completion_start_time what we want
        duration_ns = int(round((end_time - self.completion_start_time).total_seconds() * 1e9))

        # Add a span to the current trace or span (if this is a nested trace)
        self.logger.add_llm_span(
            input=self.input_data.input,
            output=completion,
            tools=self.input_data.tools,
            name=self.input_data.name,
            model=model,
            temperature=self.input_data.temperature,
            duration_ns=duration_ns,
            num_input_tokens=usage.get("prompt_tokens", 0),
            num_output_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
            metadata={str(k): str(v) for k, v in self.input_data.model_parameters.items()},
            status_code=200,
        )

        # Conclude the trace if this is the top-level call
        if self.should_complete_trace:
            self.logger.conclude(output=completion, duration_ns=duration_ns)


class OpenAIGalileo:
    """
    This class is responsible for logging OpenAI API calls and logging them to Galileo.
    It wraps the OpenAI client methods to add logging functionality without changing
    the original API behavior.

    Attributes
    ----------
    _galileo_logger : Optional[GalileoLogger]
        The Galileo logger instance used for logging OpenAI API calls.
    """

    _galileo_logger: Optional[GalileoLogger] = None

    def initialize(self) -> Optional[GalileoLogger]:
        """
        Initialize a Galileo logger.

        Parameters
        ----------
        project : Optional[str]
            The project to log to. If None, uses the default project.
        log_stream : Optional[str]
            The log stream to log to. If None, uses the default log stream.

        Returns
        -------
        Optional[GalileoLogger]
            The initialized Galileo logger instance.
        """
        self._galileo_logger = galileo_context.get_logger_instance()

        return self._galileo_logger

    def register_tracing(self) -> None:
        """
        This method wraps the OpenAI client methods to intercept calls and log them to Galileo.
        It is called automatically when the module is imported.

        The wrapped methods include:
        - openai.resources.chat.completions.Completions.create

        Additional methods can be added to the OPENAI_CLIENT_METHODS list.
        """
        for resource in OPENAI_CLIENT_METHODS:
            wrap_function_wrapper(
                resource.module, f"{resource.object}.{resource.method}", (_wrap(resource, self.initialize))
            )


modifier = OpenAIGalileo()
modifier.register_tracing()
