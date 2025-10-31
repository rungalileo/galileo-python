import json
from collections.abc import Generator
from typing import Any, Optional

from openai import BaseModel
from openai.types.chat import ChatCompletionChunk
from openai.types.responses import (
    Response,
    ResponseCompletedEvent,
    ResponseCreatedEvent,
    ResponseInProgressEvent,
    ResponseOutputMessage,
    ResponseOutputText,
    ResponseUsage,
)
from openai.types.responses.response_usage import InputTokensDetails, OutputTokensDetails


def model_dict(m: BaseModel, **kwargs: Any) -> dict[str, Any]:
    if hasattr(m, "model_dump"):
        return m.model_dump(**kwargs)
    return m.dict(**kwargs)


class EventStream:
    @staticmethod
    def _dump_event(event) -> tuple[Optional[bytes], Optional[bytes]]:
        if hasattr(event, "event") and hasattr(event, "data"):
            event_type: Optional[str] = getattr(event, "event", None)
            data = getattr(event, "data", None)
            if event_type is not None and data is not None:
                encoded_event = f"event: {event_type}\n".encode()
                encoded_data = f"data: {json.dumps(model_dict(data))}\n\n".encode()
                return encoded_event, encoded_data
        encoded_data = f"data: {json.dumps(model_dict(event))}\n\n".encode()
        return None, encoded_data

    def generate(self) -> Generator[ChatCompletionChunk, None, None]:
        yield ChatCompletionChunk.model_validate(
            {
                "id": "chatcmpl-123",
                "object": "chat.completion.chunk",
                "created": 1694268190,
                "model": "gpt-4o",
                "system_fingerprint": "fp_44709d6fcb",
                "choices": [
                    {"index": 0, "delta": {"role": "assistant", "content": ""}, "logprobs": None, "finish_reason": None}
                ],
            }
        )
        yield ChatCompletionChunk.model_validate(
            {
                "id": "chatcmpl-123",
                "object": "chat.completion.chunk",
                "created": 1694268190,
                "model": "gpt-4o",
                "system_fingerprint": "fp_44709d6fcb",
                "choices": [{"index": 0, "delta": {"content": "Hello"}, "logprobs": None, "finish_reason": None}],
            }
        )
        yield ChatCompletionChunk.model_validate(
            {
                "id": "chatcmpl-123",
                "object": "chat.completion.chunk",
                "created": 1694268190,
                "model": "gpt-4o",
                "system_fingerprint": "fp_44709d6fcb",
                "choices": [{"index": 0, "delta": {}, "logprobs": None, "finish_reason": "stop"}],
            }
        )

    def __iter__(self) -> Generator:
        for _event in self.generate():
            t, d = self._dump_event(_event)
            if t:
                yield t
            if d:
                yield d

        yield b"event: done\n"
        yield b"data: [DONE]\n\n"


class ResponsesEventStream:
    @staticmethod
    def _dump_event(event) -> tuple[Optional[bytes], Optional[bytes]]:
        """Format Responses API events for HTTP streaming."""
        encoded_data = f"data: {json.dumps(model_dict(event))}\n\n".encode()
        return None, encoded_data

    def generate(self) -> Generator[ResponseCompletedEvent, None, None]:
        """Generate Responses API streaming events using proper event objects."""
        # Create a mock response object with all required fields (copied from conftest.py fixture)
        mock_response = Response(
            id="resp_test123",
            created_at=1758822441.0,
            model="gpt-4o",
            object="response",
            output=[
                ResponseOutputMessage(
                    id="msg_test123",
                    content=[
                        ResponseOutputText(
                            text="This is a test response", type="output_text", annotations=[], logprobs=[]
                        )
                    ],
                    role="assistant",
                    status="completed",
                    type="message",
                )
            ],
            parallel_tool_calls=True,
            tool_choice="auto",
            tools=[],
            usage=ResponseUsage(
                input_tokens=10,
                input_tokens_details=InputTokensDetails(cached_tokens=0),
                output_tokens=5,
                output_tokens_details=OutputTokensDetails(reasoning_tokens=0),
                total_tokens=15,
            ),
            status="completed",
        )

        # Yield the streaming events using proper event classes
        yield ResponseCreatedEvent(response=mock_response, sequence_number=0, type="response.created")
        yield ResponseInProgressEvent(response=mock_response, sequence_number=1, type="response.in_progress")
        yield ResponseCompletedEvent(response=mock_response, sequence_number=2, type="response.completed")

    def __iter__(self) -> Generator[bytes, None, None]:
        """Format Responses API events for HTTP streaming."""
        for _event in self.generate():
            t, d = self._dump_event(_event)
            if t:
                yield t
            if d:
                yield d

        yield b"data: [DONE]\n\n"
