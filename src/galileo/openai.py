import json
import logging
import types
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from inspect import isclass
from typing import Any, Callable, Optional, Union

from packaging.version import Version
from pydantic import BaseModel
from wrapt import wrap_function_wrapper  # type: ignore[import-untyped]

from galileo import GalileoLogger
from galileo.decorator import galileo_context
from galileo.utils import _get_timestamp
from galileo.utils.serialization import EventSerializer
from galileo.utils.singleton import GalileoLoggerSingleton

try:
    import openai
    import openai.resources
    from openai._types import NotGiven
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


def _extract_chat_prompt(kwargs: dict) -> Union[list, dict]:
    """Extracts the user input from prompts. Returns a list of messages or dict with messages and functions"""
    prompt = {}

    if kwargs.get("functions") is not None:
        prompt.update({"functions": kwargs["functions"]})

    if kwargs.get("function_call") is not None:
        prompt.update({"function_call": kwargs["function_call"]})

    if kwargs.get("tools") is not None:
        prompt.update({"tools": kwargs["tools"]})

    if prompt:
        # if the user provided functions, we need to send these together with messages to Galileo
        prompt.update({"messages": [message for message in kwargs.get("messages", [])]})
        return prompt
    else:
        return [message for message in kwargs.get("messages", [])]


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
            if "function" in tool_call:
                function_ = {
                    "name": tool_call["function"].get("name", ""),
                    "arguments": tool_call["function"].get("arguments", ""),
                }
                tool_calls.append({"id": tool_call.get("id", ""), "function": function_})

        response.update({"tool_calls": tool_calls if len(tool_calls) else None})

    response.update({"content": kwargs.get("content", None)})

    return response


def _extract_input_data_from_kwargs(
    resource: OpenAiModuleDefinition, start_time: datetime, kwargs: dict[str, Any]
) -> OpenAiInputData:
    name: str = kwargs.get("name", "openai-client-generation")

    if name is None:
        name = "openai-client-generation"

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
        prompt = _extract_chat_prompt(kwargs)

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

    model_parameters = {
        "temperature": parsed_temperature,
        "max_tokens": parsed_max_tokens,
        "top_p": parsed_top_p,
        "frequency_penalty": parsed_frequency_penalty,
        "presence_penalty": parsed_presence_penalty,
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
    decorator_context_project = galileo_context.get_current_project()
    decorator_context_log_stream = galileo_context.get_current_log_stream()
    galileo_context.get_current_span_stack()
    decorator_context_trace = galileo_context.get_current_trace()

    start_time = _get_timestamp()
    arg_extractor = OpenAiArgsExtractor(*args, **kwargs)

    input_data = _extract_input_data_from_kwargs(open_ai_resource, start_time, arg_extractor.get_galileo_args())

    galileo_logger: GalileoLogger = initialize(
        project=decorator_context_project, log_stream=decorator_context_log_stream
    )

    should_complete_trace = False
    if decorator_context_trace:
        pass
    else:
        # If we don't have an active trace, start a new trace
        # We will conclude it at the end
        galileo_logger.start_trace(input=json.dumps(input_data.input, cls=EventSerializer), name=input_data.name)
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
                name=input_data.name,
                model=model,
                temperature=input_data.temperature,
                duration_ns=duration_ns,
                num_input_tokens=usage.get("prompt_tokens", 0),
                num_output_tokens=usage.get("completion_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
                metadata={str(k): str(v) for k, v in input_data.model_parameters.items()},
            )

            # Conclude the trace if this is the top-level call
            if should_complete_trace:
                galileo_logger.conclude(output=json.dumps(completion, cls=EventSerializer), duration_ns=duration_ns)

        return openai_response
    except Exception as ex:
        _logger.error(f"Error while processing OpenAI request: {ex}")
        raise RuntimeError("Failed to process the OpenAI Request") from ex


class ResponseGeneratorSync:
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
            name=self.input_data.name,
            model=model,
            temperature=self.input_data.temperature,
            duration_ns=duration_ns,
            num_input_tokens=usage.get("prompt_tokens", 0),
            num_output_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
            metadata={str(k): str(v) for k, v in self.input_data.model_parameters.items()},
        )

        # Conclude the trace if this is the top-level call
        if self.should_complete_trace:
            self.logger.conclude(output=completion, duration_ns=duration_ns)


class OpenAIGalileo:
    _galileo_logger: Optional[GalileoLogger] = None

    def initialize(self, project: Optional[str], log_stream: Optional[str]) -> Optional[GalileoLogger]:
        self._galileo_logger = GalileoLoggerSingleton().get(project=project or None, log_stream=log_stream or None)

        return self._galileo_logger

    def register_tracing(self) -> None:
        for resource in OPENAI_CLIENT_METHODS:
            wrap_function_wrapper(
                resource.module, f"{resource.object}.{resource.method}", (_wrap(resource, self.initialize))
            )


modifier = OpenAIGalileo()
modifier.register_tracing()
