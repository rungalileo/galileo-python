"""Shared mock classes for ADK tests."""

from __future__ import annotations

from unittest.mock import MagicMock
from uuid import uuid4


class MockPart:
    """Mock ADK Content Part."""

    def __init__(self, text: str | None = None) -> None:
        self.text = text


class MockContent:
    """Mock ADK Content."""

    def __init__(self, parts: list[MockPart] | None = None, role: str = "user", text: str | None = None) -> None:
        if text is not None:
            self.parts = [MockPart(text=text)]
        else:
            self.parts = parts or []
        self.role = role


class MockEvent:
    """Mock ADK Event."""

    def __init__(self, content: MockContent | None = None, is_final: bool = False) -> None:
        self.content = content
        self._is_final = is_final

    def is_final_response(self) -> bool:
        return self._is_final


class MockRunConfig:
    """Mock ADK RunConfig."""

    def __init__(self, custom_metadata: dict | None = None) -> None:
        self.custom_metadata = custom_metadata


class MockCallbackContext:
    """Mock ADK CallbackContext."""

    def __init__(
        self,
        agent_name: str = "test_agent",
        invocation_id: str | None = None,
        session_id: str = "test_session",
        run_config: MockRunConfig | None = None,
    ) -> None:
        self.agent_name = agent_name
        self.invocation_id = invocation_id or str(uuid4())
        self.session_id = session_id
        self.parent_context = MagicMock()
        self.parent_context.new_message = MagicMock()
        self.parent_context.new_message.parts = [MagicMock(text="test input")]
        self.session = MagicMock()
        self.session.id = session_id
        self.run_config = run_config


class MockInvocationContext:
    """Mock ADK InvocationContext."""

    def __init__(
        self,
        agent_name: str = "test_agent",
        invocation_id: str | None = None,
        run_config: MockRunConfig | None = None,
    ) -> None:
        self.agent_name = agent_name
        self.invocation_id = invocation_id or str(uuid4())
        self.session = MagicMock()
        self.session.id = "test_session"
        self.run_config = run_config


class MockLlmRequest:
    """Mock ADK LlmRequest."""

    def __init__(
        self,
        model: str = "gemini-2.0-flash",
        request_id: str | None = None,
        contents: list | None = None,
    ) -> None:
        self.model = model
        self.config = MagicMock()
        self.config.temperature = 0.7
        self.config.tools = None
        self.contents = contents or []
        self.request_id = request_id or str(uuid4())


class MockLlmResponse:
    """Mock ADK LlmResponse."""

    def __init__(
        self,
        text: str = "test response",
        request_id: str | None = None,
        content: object = None,
        usage_metadata: object = None,
    ) -> None:
        if content is not None:
            self.content = content
        else:
            self.content = MagicMock()
            self.content.parts = [MagicMock(text=text)]
            self.content.role = "model"
        if usage_metadata is not None:
            self.usage_metadata = usage_metadata
        else:
            self.usage_metadata = MagicMock()
            self.usage_metadata.prompt_token_count = 10
            self.usage_metadata.candidates_token_count = 20
            self.usage_metadata.total_token_count = 30
        self.request_id = request_id


class MockToolContext:
    """Mock ADK ToolContext."""

    def __init__(
        self,
        invocation_id: str | None = None,
        agent_name: str = "test_agent",
        session_id: str = "test_session",
        callback_context: MockCallbackContext | None = None,
    ) -> None:
        if callback_context is not None:
            self.callback_context = callback_context
        else:
            self.invocation_id = invocation_id or str(uuid4())
            self.callback_context = MagicMock()
            self.callback_context.agent_name = agent_name
            self.callback_context.invocation_id = self.invocation_id
            self.callback_context.session = MagicMock()
            self.callback_context.session.id = session_id


class MockTool:
    """Mock ADK BaseTool."""

    def __init__(self, name: str = "test_tool") -> None:
        self.name = name
