# ruff: noqa: F401
from typing import Any

from galileo_core.schemas.logging.llm import Message as CoreMessage

# These classes should not be removed. They are used to rebuild the new `Message` model
# we are defining below.
from galileo_core.schemas.logging.llm import ToolCall, ToolCallFunction


class Message(CoreMessage):
    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True)

    def __eq__(self, value: CoreMessage) -> bool:
        return (
            self.content == value.content
            and self.role == value.role
            and self.tool_calls == value.tool_calls
            and self.tool_call_id == value.tool_call_id
        )


# Without rebuilding the model, Message class we create here would not know and validate
# constituent classes defined in core which build up message.
Message.model_rebuild()
