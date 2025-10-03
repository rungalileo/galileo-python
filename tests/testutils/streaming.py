import json
from collections.abc import Generator
from typing import Any, Optional

from openai import BaseModel
from openai.types.chat import ChatCompletionChunk


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
