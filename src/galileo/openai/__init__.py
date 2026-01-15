"""
Galileo wrapper for OpenAI that automatically logs prompts and responses.

This module provides a drop-in replacement for the OpenAI library that automatically
logs all prompts, responses, and related metadata to Galileo. It works by intercepting
calls to the OpenAI API and logging them using the Galileo logging system.

Note that the original OpenAI package is still required as a project dependency to use this wrapper.

Examples
--------
```python
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
```
"""

import logging
from typing import Any, Callable, Optional

import httpx
from wrapt import wrap_function_wrapper  # type: ignore[import-untyped]

from galileo.decorator import galileo_context
from galileo.logger import GalileoLogger
from galileo.openai.extractors import (
    OpenAiArgsExtractor,
    convert_to_galileo_message,
    extract_data_from_default_response,
    extract_input_data_from_kwargs,
    has_pending_function_calls,
    is_openai_v1,
    is_streaming_response,
    process_function_call_outputs,
    process_output_items,
)
from galileo.openai.models import OpenAiModuleDefinition
from galileo.openai.response_generator import ResponseGeneratorSync
from galileo.utils import _get_timestamp
from galileo.utils.serialization import serialize_to_str

try:
    import openai
    from openai import AsyncAzureOpenAI, AsyncOpenAI, AzureOpenAI, NoneType, OpenAI  # noqa: F401
except ImportError:
    AsyncAzureOpenAI = None  # type: ignore[assignment]
    AsyncOpenAI = None  # type: ignore[assignment]
    AzureOpenAI = None  # type: ignore[assignment]
    OpenAI = None  # type: ignore[assignment]
    raise ModuleNotFoundError("Please install OpenAI to use this feature: 'pip install openai'")


_logger = logging.getLogger(__name__)


OPENAI_CLIENT_METHODS = [
    OpenAiModuleDefinition(
        module="openai.resources.chat.completions", object="Completions", method="create", type="chat", sync=True
    ),
    OpenAiModuleDefinition(
        module="openai.resources.responses", object="Responses", method="create", type="response", sync=True
    ),
    # Eventually add more OpenAI client library methods here
]


def _galileo_wrapper(func: Callable) -> Callable:
    def _with_galileo(open_ai_definitions: OpenAiModuleDefinition, initialize: Callable) -> Callable:
        def wrapper(wrapped: Callable, instance: Any, args: dict, kwargs: dict) -> Any:
            return func(open_ai_definitions, initialize, wrapped, args, kwargs)

        return wrapper

    return _with_galileo


@_galileo_wrapper
def _wrap(
    open_ai_resource: OpenAiModuleDefinition, initialize: Callable, wrapped: Callable, args: dict, kwargs: dict
) -> Any:
    start_time = _get_timestamp()
    arg_extractor = OpenAiArgsExtractor(*args, **kwargs)

    input_data = extract_input_data_from_kwargs(open_ai_resource, start_time, arg_extractor.get_galileo_args())

    galileo_logger: GalileoLogger = initialize()

    should_complete_trace = False
    if galileo_logger.current_parent():
        pass
    else:
        # If we don't have an active trace, start a new trace
        # We will conclude it at the end
        # convert to list of galileo messages since we can't send list of messages to span and want consistency
        if isinstance(input_data.input, list):
            trace_input_messages = [convert_to_galileo_message(msg) for msg in input_data.input]
        else:
            trace_input_messages = [convert_to_galileo_message(input_data.input)]

        # Serialize with "messages" wrapper for UI compatibility
        trace_input = {"messages": [msg.model_dump(exclude_none=True) for msg in trace_input_messages]}
        galileo_logger.start_trace(input=serialize_to_str(trace_input), name=input_data.name)
        should_complete_trace = True

    try:
        openai_response = None
        exc_info = None
        status_code = httpx.codes.OK
        try:
            openai_response = wrapped(**arg_extractor.get_openai_args())
        except openai.APIStatusError as exc:
            status_code = exc.status_code
            exc_info = exc

        if is_streaming_response(openai_response):
            # extract data from streaming response
            return ResponseGeneratorSync(
                resource=open_ai_resource,
                response=openai_response,
                input_data=input_data,
                logger=galileo_logger,
                should_complete_trace=should_complete_trace,
                status_code=status_code,
            )
        model, completion, usage = extract_data_from_default_response(
            open_ai_resource, (openai_response.__dict__ if openai_response and is_openai_v1() else openai_response)
        )

        if usage is None:
            usage = {}

        end_time = _get_timestamp()

        duration_ns = round((end_time - start_time).total_seconds() * 1e9)

        # convert to list of galileo messages since we can't send a regular list to span input
        if isinstance(input_data.input, list):
            span_input = [convert_to_galileo_message(msg) for msg in input_data.input]
        else:
            span_input = [convert_to_galileo_message(input_data.input)]

        # Process Responses API output items sequentially if present
        final_conversation_context = span_input.copy()
        output_items: list = []
        if open_ai_resource.type == "response" and openai_response:
            # First, process any function_call_output items in the input to create tool spans
            # This represents tool executions that happened before this API call
            if isinstance(input_data.input, list):
                process_function_call_outputs(input_data.input, galileo_logger)

            # Get output_items safely for Responses API
            # First try direct attribute access (works for Pydantic models)
            output_attr = getattr(openai_response, "output", None)
            if output_attr is not None:
                output_items = output_attr
            elif is_openai_v1() or hasattr(openai_response, "model_dump"):
                # Use model_dump() for Pydantic models
                response_mapping = openai_response.model_dump()
                output_items = response_mapping.get("output", [])
            else:
                # Fall back to __dict__ for dict-like responses
                output_items = openai_response.__dict__.get("output", [])

            # Process all output items sequentially and get the final context
            final_conversation_context = process_output_items(
                output_items,
                galileo_logger,
                model,
                span_input,
                input_data.model_parameters,
                status_code=status_code,
                tools=input_data.tools,
                usage=usage,
            )
        else:
            # For non-Responses API (chat or completion), create the main span as before
            span_output = convert_to_galileo_message(completion, "assistant")

            # Add a span to the current trace or span (if this is a nested trace)
            span = galileo_logger.add_llm_span(
                input=span_input,
                output=span_output,
                tools=input_data.tools,
                name=input_data.name,
                model=model,
                temperature=input_data.temperature,
                duration_ns=duration_ns,
                num_input_tokens=usage.get("input_tokens", 0),
                num_output_tokens=usage.get("output_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
                metadata={str(k): str(v) for k, v in input_data.model_parameters.items()},
                # openai client library doesn't return http_status code, so we only can hardcode it here
                # because we if we parsed and extracted data from response it means we get it and it's 200OK
                status_code=status_code,
            )
            span.metrics.num_reasoning_tokens = usage.get("reasoning_tokens", 0) if usage else 0
            span.metrics.num_cached_input_tokens = usage.get("cached_tokens", 0) if usage else 0

        # Conclude the trace if this is the top-level call
        # For Responses API: don't conclude if there are pending function calls (model waiting for tool results)
        has_pending_calls = (
            open_ai_resource.type == "response" and output_items and has_pending_function_calls(output_items)
        )

        if should_complete_trace and not has_pending_calls:
            if open_ai_resource.type == "response":
                # For Responses API, use the final conversation context from processing
                full_conversation = final_conversation_context
            else:
                # For other APIs, add the final span output
                full_conversation = []
                if isinstance(input_data.input, list):
                    full_conversation.extend([convert_to_galileo_message(msg) for msg in input_data.input])
                else:
                    full_conversation.append(convert_to_galileo_message(input_data.input))
                full_conversation.append(span_output)

            # Serialize with "messages" wrapper for UI compatibility
            trace_output = {"messages": [msg.model_dump(exclude_none=True) for msg in full_conversation]}
            galileo_logger.conclude(
                output=serialize_to_str(trace_output), duration_ns=duration_ns, status_code=status_code
            )

        # we want to re-raise exception after we process openai_response
        if exc_info:
            raise exc_info
        return openai_response
    except Exception as ex:
        _logger.error(f"Error while processing OpenAI request: {ex}")
        raise RuntimeError("Failed to process the OpenAI Request") from ex


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
