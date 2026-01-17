import base64
import json

from galileo_core.schemas.logging.span import MessageRole

from galileo_adk.data_converters import convert_adk_content_to_galileo_messages


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
        assert messages[0].role == MessageRole.tool
        payload = json.loads(messages[0].content)
        assert payload["type"] == "function_call"
        assert payload["name"] == "search"
        assert payload["args"] == {"query": "weather"}

    def test_function_response_part(self) -> None:
        func_resp = MockPart(name="search", response={"result": "sunny"})
        content = MockContent([MockPart(function_response=func_resp)])
        messages = convert_adk_content_to_galileo_messages(content)
        assert len(messages) == 1
        assert messages[0].role == MessageRole.tool
        payload = json.loads(messages[0].content)
        assert payload["type"] == "function_response"
        assert payload["response"] == {"result": "sunny"}

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
        assert json.loads(messages[1].content)["type"] == "function_call"
        assert json.loads(messages[2].content)["type"] == "function_response"
        assert messages[3].content == "Step 2"

    def test_empty_content(self) -> None:
        content = MockContent([])
        assert convert_adk_content_to_galileo_messages(content) == []

    def test_unknown_part_skipped(self) -> None:
        content = MockContent([MockPart(unknown_field="value")])
        assert convert_adk_content_to_galileo_messages(content) == []
