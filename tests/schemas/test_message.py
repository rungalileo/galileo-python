from typing import Any

import pytest

from galileo import Message, MessageRole, ToolCall, ToolCallFunction


@pytest.mark.parametrize(
    ("message", "expected_to_dict"),
    [
        (
            Message(role=MessageRole.system, content="You are a helpful agent"),
            {"content": "You are a helpful agent", "role": MessageRole.system},
        ),
        (
            Message(role=MessageRole.system, content="You are a helpful agent enabling friction free flow"),
            {"content": "You are a helpful agent enabling friction free flow", "role": MessageRole.system},
        ),
        (
            Message(role=MessageRole.user, content="Why is the sky blue?"),
            {"content": "Why is the sky blue?", "role": MessageRole.user},
        ),
        (
            Message(role=MessageRole.user, content="Is sun getting colder?"),
            {"content": "Is sun getting colder?", "role": MessageRole.user},
        ),
        (
            Message(
                role=MessageRole.user,
                content="Who are you?",
                tool_call_id="my_helpful_tool_1",
                tool_calls=[
                    ToolCall(id="my_helpful_tool_1", function=ToolCallFunction(name="fun_a", arguments="arg1 arg2")),
                    ToolCall(id="my_helpful_tool_2", function=ToolCallFunction(name="fun_b", arguments="arg3")),
                ],
            ),
            {
                "content": "Who are you?",
                "role": MessageRole.user,
                "tool_call_id": "my_helpful_tool_1",
                "tool_calls": [
                    {"function": {"arguments": "arg1 arg2", "name": "fun_a"}, "id": "my_helpful_tool_1"},
                    {"function": {"arguments": "arg3", "name": "fun_b"}, "id": "my_helpful_tool_2"},
                ],
            },
        ),
    ],
)
def test_to_dict(message: Message, expected_to_dict: dict[str, Any]) -> None:
    assert message.to_dict() == expected_to_dict


def test_eq() -> None:
    m1 = Message(
        role=MessageRole.user,
        content="Who are you?",
        tool_call_id="my_helpful_tool_1",
        tool_calls=[
            ToolCall(id="my_helpful_tool_1", function=ToolCallFunction(name="fun_a", arguments="arg1 arg2")),
            ToolCall(id="my_helpful_tool_2", function=ToolCallFunction(name="fun_b", arguments="arg3")),
        ],
    )
    m2 = Message(
        role=MessageRole.user,
        content="Who are you?",
        tool_call_id="my_helpful_tool_1",
        tool_calls=[
            ToolCall(id="my_helpful_tool_1", function=ToolCallFunction(name="fun_a", arguments="arg1 arg2")),
            ToolCall(id="my_helpful_tool_2", function=ToolCallFunction(name="fun_b", arguments="arg3")),
        ],
    )
    assert m1 == m2
