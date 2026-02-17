import base64
import json
import logging

from galileo_core.schemas.logging.llm import MessageRole

from galileo_adk.data_converters import (
    _extract_tool_info,
    _try_direct_attributes,
    _try_function_declarations,
    _try_to_dict,
    convert_adk_content_to_galileo_messages,
)


class MockPart:
    def __init__(self, **kwargs: object) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


class MockContent:
    def __init__(self, parts: list[MockPart], role: str = "user") -> None:
        self.parts = parts
        self.role = role


class TestConvertADKContent:
    def test_text_part(self) -> None:
        content = MockContent([MockPart(text="hello")])
        messages = convert_adk_content_to_galileo_messages(content)
        assert len(messages) == 1
        assert messages[0].content == "hello"
        assert messages[0].role == MessageRole.user

    def test_inline_data_part(self) -> None:
        inline = MockPart(mime_type="image/png", data=b"\x89PNG")
        content = MockContent([MockPart(inline_data=inline)])
        messages = convert_adk_content_to_galileo_messages(content)
        assert len(messages) == 1
        payload = json.loads(messages[0].content)
        assert payload["type"] == "inline_data"
        assert payload["mime_type"] == "image/png"
        assert base64.b64decode(payload["data"]) == b"\x89PNG"

    def test_file_data_part(self) -> None:
        file_d = MockPart(file_uri="gs://bucket/file.pdf", mime_type="application/pdf")
        content = MockContent([MockPart(file_data=file_d)])
        messages = convert_adk_content_to_galileo_messages(content)
        assert len(messages) == 1
        payload = json.loads(messages[0].content)
        assert payload["type"] == "file_data"
        assert payload["file_uri"] == "gs://bucket/file.pdf"

    def test_function_call_part(self) -> None:
        func_call = MockPart(name="search", args={"query": "weather"})
        content = MockContent([MockPart(function_call=func_call)], role="model")
        messages = convert_adk_content_to_galileo_messages(content)
        assert len(messages) == 1
        assert messages[0].role == MessageRole.assistant
        assert messages[0].content == ""
        assert messages[0].tool_calls is not None
        assert len(messages[0].tool_calls) == 1
        assert messages[0].tool_calls[0].function.name == "search"
        assert json.loads(messages[0].tool_calls[0].function.arguments) == {"query": "weather"}

    def test_function_response_part(self) -> None:
        func_resp = MockPart(name="search", response={"result": "sunny"})
        content = MockContent([MockPart(function_response=func_resp)])
        messages = convert_adk_content_to_galileo_messages(content)
        assert len(messages) == 1
        assert messages[0].role == MessageRole.tool
        payload = json.loads(messages[0].content)
        assert payload == {"result": "sunny"}

    def test_mixed_parts_preserve_order(self) -> None:
        parts = [
            MockPart(text="Step 1"),
            MockPart(function_call=MockPart(name="tool", args={})),
            MockPart(function_response=MockPart(name="tool", response="done")),
            MockPart(text="Step 2"),
        ]
        content = MockContent(parts, role="model")
        messages = convert_adk_content_to_galileo_messages(content)
        assert len(messages) == 4
        assert messages[0].content == "Step 1"
        assert messages[1].role == MessageRole.assistant
        assert messages[1].tool_calls is not None
        assert messages[2].role == MessageRole.tool
        assert messages[2].content == "done"
        assert messages[3].content == "Step 2"

    def test_empty_content(self) -> None:
        content = MockContent([])
        assert convert_adk_content_to_galileo_messages(content) == []

    def test_unknown_part_skipped(self) -> None:
        content = MockContent([MockPart(unknown_field="value")])
        assert convert_adk_content_to_galileo_messages(content) == []

    def test_multiple_function_calls_same_name_with_unique_ids(self) -> None:
        """Multiple function calls with same name but unique IDs should link correctly."""
        parts = [
            MockPart(function_call=MockPart(id="call_1", name="search", args={"q": "first"})),
            MockPart(function_call=MockPart(id="call_2", name="search", args={"q": "second"})),
            MockPart(function_response=MockPart(id="call_1", name="search", response="result_1")),
            MockPart(function_response=MockPart(id="call_2", name="search", response="result_2")),
        ]
        content = MockContent(parts, role="model")
        messages = convert_adk_content_to_galileo_messages(content)

        assert len(messages) == 4
        # First call and its response should share the same call_id
        call_id_1 = messages[0].tool_calls[0].id
        assert messages[2].tool_call_id == call_id_1
        # Second call and its response should share a different call_id
        call_id_2 = messages[1].tool_calls[0].id
        assert messages[3].tool_call_id == call_id_2
        # The two call_ids should be different
        assert call_id_1 != call_id_2

    def test_function_call_response_without_id_no_linking(self) -> None:
        """When no id is available, responses don't link (per-part unique keys prevent overwrites)."""
        parts = [
            MockPart(function_call=MockPart(name="calc", args={"x": 1})),
            MockPart(function_response=MockPart(name="calc", response=42)),
        ]
        content = MockContent(parts, role="model")
        messages = convert_adk_content_to_galileo_messages(content)

        assert len(messages) == 2
        # Without ADK ids, responses can't link to calls (different part indices)
        assert messages[0].tool_calls[0].id is not None
        assert messages[1].tool_call_id is None


class MockTool:
    """Mock tool for extraction tests."""

    def __init__(
        self,
        name: str | None = None,
        description: str | None = None,
        parameters_schema: dict | None = None,
    ) -> None:
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if parameters_schema is not None:
            self.parameters_schema = parameters_schema


class MockFunctionDeclaration:
    """Mock function declaration for tool extraction."""

    def __init__(self, name: str, description: str = "", parameters: dict | None = None) -> None:
        self.name = name
        self.description = description
        self.parameters = parameters or {}


class TestExtractToolInfo:
    """Tests for tool extraction strategies."""

    def test_try_direct_attributes_strategy(self) -> None:
        # Given: a tool with direct attributes
        tool = MockTool(
            name="calculator",
            description="Perform calculations",
            parameters_schema={"type": "object", "properties": {"expression": {"type": "string"}}},
        )

        # When: extracting via direct attributes
        result = _try_direct_attributes(tool)

        # Then: tool info is extracted correctly
        assert result is not None
        assert result["type"] == "function"
        assert result["function"]["name"] == "calculator"
        assert result["function"]["description"] == "Perform calculations"
        assert result["function"]["parameters"]["type"] == "object"

    def test_try_to_dict_strategy_fallback(self) -> None:
        # Given: a tool with to_dict method
        class DictTool:
            def to_dict(self) -> dict:
                return {
                    "name": "weather",
                    "description": "Get weather",
                    "parameters": {"type": "object"},
                }

        tool = DictTool()

        # When: extracting via to_dict
        result = _try_to_dict(tool)

        # Then: tool info is extracted
        assert result is not None
        assert result["function"]["name"] == "weather"
        assert result["function"]["description"] == "Get weather"

    def test_try_function_declarations_strategy(self) -> None:
        # Given: a tool with function_declarations
        class DeclarationsTool:
            function_declarations = [
                MockFunctionDeclaration(
                    name="search",
                    description="Search the web",
                    parameters={"type": "object", "properties": {"query": {"type": "string"}}},
                ),
                MockFunctionDeclaration(
                    name="browse",
                    description="Browse a URL",
                ),
            ]

        tool = DeclarationsTool()

        # When: extracting via function_declarations
        result = _try_function_declarations(tool)

        # Then: all declarations are extracted
        assert len(result) == 2
        assert result[0]["function"]["name"] == "search"
        assert result[1]["function"]["name"] == "browse"

    def test_logs_warning_when_no_strategy_works(self, caplog: object) -> None:
        # Given: a tool with no extractable info
        class UnknownTool:
            pass

        tool = UnknownTool()

        # When: extracting tool info
        with caplog.at_level(logging.WARNING):  # type: ignore[union-attr]
            result = _extract_tool_info(tool)

        # Then: empty list returned and warning logged
        assert result == []
        assert "Could not extract tool metadata" in caplog.text  # type: ignore[union-attr]
