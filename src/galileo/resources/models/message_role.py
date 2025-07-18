from typing import Literal, cast

MessageRole = Literal["agent", "assistant", "developer", "function", "system", "tool", "user"]

MESSAGE_ROLE_VALUES: set[MessageRole] = {"agent", "assistant", "developer", "function", "system", "tool", "user"}


def check_message_role(value: str) -> MessageRole:
    if value in MESSAGE_ROLE_VALUES:
        return cast(MessageRole, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {MESSAGE_ROLE_VALUES!r}")
