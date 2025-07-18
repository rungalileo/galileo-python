from typing import Literal, cast

MessageListItemRole = Literal["agent", "assistant", "function", "system", "tool", "user"]

MESSAGE_LIST_ITEM_ROLE_VALUES: set[MessageListItemRole] = {"agent", "assistant", "function", "system", "tool", "user"}


def check_message_list_item_role(value: str) -> MessageListItemRole:
    if value in MESSAGE_LIST_ITEM_ROLE_VALUES:
        return cast(MessageListItemRole, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {MESSAGE_LIST_ITEM_ROLE_VALUES!r}")
