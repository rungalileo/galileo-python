from collections.abc import Generator
from datetime import datetime
from typing import Any, Optional, Union

from galileo import GalileoLogger
from galileo.openai.extractors import (
    convert_to_galileo_message,
    extract_streamed_openai_response,
    has_pending_function_calls,
    process_function_call_outputs,
    process_output_items,
)
from galileo.openai.models import OpenAiInputData, OpenAiModuleDefinition
from galileo.utils import _get_timestamp
from galileo.utils.serialization import serialize_to_str

try:
    import openai
except ImportError:
    AsyncAzureOpenAI = None  # type: ignore[assignment]
    AsyncOpenAI = None  # type: ignore[assignment]
    AzureOpenAI = None  # type: ignore[assignment]
    OpenAI = None  # type: ignore[assignment]


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

    def __init__(
        self,
        *,
        resource: OpenAiModuleDefinition,
        response: Union[Generator, openai.Stream],
        input_data: OpenAiInputData,
        logger: GalileoLogger,
        should_complete_trace: bool,
        status_code: int = 200,
    ):
        self.items: list[Any] = []
        self.resource = resource
        self.response = response
        self.input_data = input_data
        self.logger = logger
        self.should_complete_trace = should_complete_trace
        self.completion_start_time: Optional[datetime] = None
        self.status_code = status_code

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

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        pass

    def _finalize(self) -> None:
        model, completion, usage = extract_streamed_openai_response(self.resource, self.items)

        if usage is None:
            usage = {}

        end_time = _get_timestamp()
        # TODO: make sure completion_start_time what we want
        duration_ns = (
            round((end_time - self.completion_start_time).total_seconds() * 1e9) if self.completion_start_time else 0
        )

        if isinstance(self.input_data.input, list):
            span_input = [convert_to_galileo_message(msg) for msg in self.input_data.input]
        else:
            span_input = [convert_to_galileo_message(self.input_data.input)]

        # probably can create a shared function for handling both streaming and non-streaming
        # Process Responses API output items sequentially if present (same as non-streaming)
        final_conversation_context = span_input.copy()
        output_items: list = []
        if self.resource.type == "response" and completion:
            # First, process any function_call_output items in the input to create tool spans
            # This represents tool executions that happened before this API call
            if isinstance(self.input_data.input, list):
                process_function_call_outputs(self.input_data.input, self.logger)

            # For streaming Responses API, we need to extract output items from the completion
            # The completion should contain the final response with output items
            if isinstance(completion, dict) and "output" in completion:
                output_items = completion.get("output", [])

                # Process all output items sequentially and get the final context
                final_conversation_context = process_output_items(
                    output_items,
                    self.logger,
                    model,
                    span_input,
                    self.input_data.model_parameters,
                    status_code=self.status_code,
                    tools=self.input_data.tools,
                    usage=usage,
                )
            else:
                # Fallback: create basic span if no output items
                span_output = convert_to_galileo_message(completion, "assistant")
                span = self.logger.add_llm_span(
                    input=span_input,
                    output=span_output,
                    tools=self.input_data.tools,
                    name=self.input_data.name,
                    model=model,
                    temperature=self.input_data.temperature,
                    duration_ns=duration_ns,
                    num_input_tokens=usage.get("input_tokens", 0),
                    num_output_tokens=usage.get("output_tokens", 0),
                    total_tokens=usage.get("total_tokens", 0),
                    metadata={str(k): str(v) for k, v in self.input_data.model_parameters.items()},
                    status_code=self.status_code,
                )
                span.metrics.num_reasoning_tokens = usage.get("reasoning_tokens", 0) if usage else 0
                span.metrics.num_cached_input_tokens = usage.get("cached_tokens", 0) if usage else 0
        else:
            # For non-Responses API (chat or completion), create the main span as before
            span_output = convert_to_galileo_message(completion, "assistant")

            # Add a span to the current trace or span (if this is a nested trace)
            span = self.logger.add_llm_span(
                input=span_input,
                output=span_output,
                tools=self.input_data.tools,
                name=self.input_data.name,
                model=model,
                temperature=self.input_data.temperature,
                duration_ns=duration_ns,
                num_input_tokens=usage.get("input_tokens", 0),
                num_output_tokens=usage.get("output_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
                metadata={str(k): str(v) for k, v in self.input_data.model_parameters.items()},
                status_code=self.status_code,
            )
            span.metrics.num_reasoning_tokens = usage.get("reasoning_tokens", 0) if usage else 0
            span.metrics.num_cached_input_tokens = usage.get("cached_tokens", 0) if usage else 0

        # Conclude the trace if this is the top-level call
        # For Responses API: don't conclude if there are pending function calls (model waiting for tool results)
        has_pending_calls = (
            self.resource.type == "response" and output_items and has_pending_function_calls(output_items)
        )

        if self.should_complete_trace and not has_pending_calls:
            if self.resource.type == "response":
                # For Responses API, use the final conversation context from processing
                full_conversation = final_conversation_context
            else:
                # For other APIs, add the final span output
                full_conversation = []
                if isinstance(self.input_data.input, list):
                    full_conversation.extend([convert_to_galileo_message(msg) for msg in self.input_data.input])
                else:
                    full_conversation.append(convert_to_galileo_message(self.input_data.input))
                full_conversation.append(convert_to_galileo_message(completion, "assistant"))

            # Serialize with "messages" wrapper for UI compatibility
            trace_output = {"messages": [msg.model_dump(exclude_none=True) for msg in full_conversation]}
            self.logger.conclude(
                output=serialize_to_str(trace_output), duration_ns=duration_ns, status_code=self.status_code
            )
