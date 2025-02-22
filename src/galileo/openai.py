import logging
from dataclasses import dataclass
from datetime import datetime
from inspect import isclass
from typing import Any, Callable, Optional

import openai.resources
from openai._types import NotGiven
from packaging.version import Version
from pydantic import BaseModel
from wrapt import wrap_function_wrapper

from galileo import GalileoLogger
from galileo.decorator import galileo_context
from galileo.utils import _get_timestamp
from galileo.utils.singleton import GalileoLoggerSingleton

try:
    import openai
except ImportError:
    raise ModuleNotFoundError("Please install OpenAI to use this feature: 'pip install openai'")

try:
    from openai import AsyncAzureOpenAI, AsyncOpenAI, AzureOpenAI, OpenAI  # noqa: F401
except ImportError:
    AsyncAzureOpenAI = None  # type: ignore
    AsyncOpenAI = None  # type: ignore
    AzureOpenAI = None  # type: ignore
    OpenAI = None  # type: ignore


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
    model: str | None
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


def _extract_chat_prompt(kwargs: dict) -> list | dict:
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

    if kwargs.get("function_call") is not None:
        response.update({"function_call": kwargs["function_call"]})

    if kwargs.get("tool_calls") is not None:
        response.update({"tool_calls": kwargs["tool_calls"]})

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
        input=prompt,  # type: ignore
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


def _is_openai_v1() -> bool:
    return Version(openai.__version__) >= Version("1.0.0")


@_galileo_wrapper
def _wrap(
    open_ai_resource: OpenAiModuleDefinition, initialize: Callable, wrapped: Callable, args: dict, kwargs: dict
) -> Any:
    # Retrieve the decorator context
    decorator_context_project = galileo_context.get_current_project()
    decorator_context_log_stream = galileo_context.get_current_log_stream()
    decorator_context_span_stack = galileo_context.get_current_span_stack()
    decorator_context_trace = galileo_context.get_current_trace()

    start_time = _get_timestamp()
    arg_extractor = OpenAiArgsExtractor(*args, **kwargs)

    input_data = _extract_input_data_from_kwargs(open_ai_resource, start_time, arg_extractor.get_galileo_args())

    galileo_logger: GalileoLogger = initialize(
        project=decorator_context_project, log_stream=decorator_context_log_stream
    )

    complete_trace = False
    if decorator_context_trace:
        trace = decorator_context_trace
    else:
        # If we don't have an active trace, start a new trace
        # We will conclude it at the end
        trace = galileo_logger.start_trace(input=input_data.input, name=input_data.name)
        complete_trace = True

    try:
        openai_response = wrapped(**arg_extractor.get_openai_args())

        model, completion, usage = _extract_data_from_default_response(
            open_ai_resource, ((openai_response and openai_response.__dict__) if _is_openai_v1() else openai_response)
        )

        end_time = _get_timestamp()

        duration_ns = int(round((end_time - start_time).total_seconds() * 1e9))

        # Add a span to the current trace or span (if this is a nested trace)
        if len(decorator_context_span_stack):
            span = decorator_context_span_stack[-1]
            span.add_llm_span(
                input=input_data.input,
                output=completion,
                name=input_data.name,
                model=model,
                temperature=input_data.temperature,
                duration_ns=duration_ns,
                input_tokens=usage.get("prompt_tokens", 0),
                output_tokens=usage.get("completion_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
                metadata={str(k): str(v) for k, v in input_data.model_parameters.items()},
            )
        else:
            trace.add_llm_span(
                input=input_data.input,
                output=completion,
                name=input_data.name,
                model=model,
                temperature=input_data.temperature,
                duration_ns=duration_ns,
                input_tokens=usage.get("prompt_tokens", 0),
                output_tokens=usage.get("completion_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
                metadata={str(k): str(v) for k, v in input_data.model_parameters.items()},
            )

        # Conclude the trace if this is the top-level call
        if complete_trace:
            trace.conclude(output=completion, duration_ns=duration_ns)

        return openai_response
    except Exception as ex:
        _logger.error(f"Error while processing OpenAI request: {ex}")
        raise RuntimeError("Failed to process the OpenAI Request") from ex


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
