import datetime as dt
import enum
import json
import uuid
from asyncio import Queue
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional
from unittest.mock import patch

import pytest
from pydantic import BaseModel

from galileo.utils.serialization import EventSerializer, serialize_datetime, serialize_to_str


class TestSerializeDateTime:
    def test_serialize_datetime_with_utc_timezone(self) -> None:
        # Test with UTC timezone
        dt_utc = dt.datetime(2023, 1, 1, 12, 0, 0, tzinfo=dt.timezone.utc)
        result = serialize_datetime(dt_utc)
        assert result.endswith("Z")
        assert "2023-01-01T12:00:00Z" == result

    def test_serialize_datetime_with_non_utc_timezone(self) -> None:
        # Test with non-UTC timezone
        tz = dt.timezone(dt.timedelta(hours=5, minutes=30))  # UTC+5:30
        dt_with_tz = dt.datetime(2023, 1, 1, 12, 0, 0, tzinfo=tz)
        result = serialize_datetime(dt_with_tz)
        assert "+05:30" in result
        assert "2023-01-01T12:00:00+05:30" == result


class TestEventSerializer:
    def test_default_datetime(self) -> None:
        # Test datetime serialization
        dt_obj = dt.datetime(2023, 1, 1, 12, 0, 0, tzinfo=dt.timezone.utc)
        result = json.dumps(dt_obj, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == "2023-01-01T12:00:00Z"

    def test_default_exception(self) -> None:
        # Test exception serialization
        exception = ValueError("Test error")
        result = json.dumps(exception, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == "ValueError: Test error"

    def test_default_enum(self) -> None:
        # Test enum serialization
        class TestEnum(enum.Enum):
            ONE = 1
            TWO = "two"

        result = json.dumps(TestEnum.ONE, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == 1

        result = json.dumps(TestEnum.TWO, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == "two"

    def test_default_queue(self) -> None:
        # Test Queue serialization
        # Test Queue serialization
        queue = Queue()
        result = json.dumps(queue, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == "Queue"

    def test_default_dataclass(self) -> None:
        # Test dataclass serialization
        @dataclass
        class TestDataClass:
            name: str
            value: int

        data = TestDataClass(name="test", value=42)
        result = json.dumps(data, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == {"name": "test", "value": 42}

    def test_default_uuid(self) -> None:
        # Test UUID serialization
        test_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")
        result = json.dumps(test_uuid, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == "12345678-1234-5678-1234-567812345678"

    def test_default_bytes(self) -> None:
        # Test bytes serialization
        # Valid UTF-8 bytes
        valid_bytes = b"hello world"
        decoded_result = json.loads(json.dumps(valid_bytes, cls=EventSerializer))
        assert decoded_result == "hello world"

        # Invalid UTF-8 bytes
        invalid_bytes = b"\xff\xfe\xfd"
        decoded_result = json.loads(json.dumps(invalid_bytes, cls=EventSerializer))
        assert decoded_result == "<not serializable bytes>"

    def test_default_date(self) -> None:
        # Test date serialization
        date_obj = dt.date(2023, 1, 1)
        result = json.dumps(date_obj, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == "2023-01-01"

    def test_default_pydantic_model(self) -> None:
        # Test Pydantic BaseModel serialization
        class TestModel(BaseModel):
            name: str
            value: int
            optional: Optional[str] = None

        model = TestModel(name="test", value=42)
        result = json.dumps(model, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == {"name": "test", "value": 42}

    def test_default_path(self) -> None:
        # Test Path serialization
        path = Path("/tmp/test/file.txt")
        result = json.dumps(path, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == "/tmp/test/file.txt"

    @pytest.mark.parametrize(
        "value,expected",
        [
            (123, 123),  # Within JS safe integer range
            (9007199254740991, 9007199254740991),  # Max safe integer
            (9007199254740992, "9007199254740992"),  # Outside JS safe integer range
            (-9007199254740991, -9007199254740991),  # Min safe integer
            (-9007199254740992, "-9007199254740992"),  # Outside JS safe integer range
        ],
    )
    def test_default_integer(self, value: int, expected: Any) -> None:
        # Test integer serialization
        result = json.dumps(value, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == expected

    def test_default_standard_json_types(self) -> None:
        # Test standard JSON-encodable types
        assert json.dumps("string", cls=EventSerializer) == '"string"'
        assert json.dumps(3.14, cls=EventSerializer) == "3.14"
        assert json.dumps(None, cls=EventSerializer) == "null"

    def test_default_collections(self) -> None:
        # Test collection types
        assert json.dumps((1, 2, 3), cls=EventSerializer) == "[1, 2, 3]"
        assert json.dumps({1, 2, 3}, cls=EventSerializer) == "[1, 2, 3]"
        assert json.dumps(frozenset([1, 2, 3]), cls=EventSerializer) == "[1, 2, 3]"

    def test_default_dict(self) -> None:
        # Test dict serialization
        test_dict = {"key1": "value1", "key2": 42}
        result = json.dumps(test_dict, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == {"key1": "value1", "key2": 42}

    def test_default_list(self) -> None:
        # Test list serialization
        test_list = [1, "two", 3.0]
        result = json.dumps(test_list, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == [1, "two", 3.0]

    def test_default_sequence(self) -> None:
        # Test Sequence serialization
        class TestSequence(Sequence):
            def __init__(self, data):
                self.data = data

            def __getitem__(self, index):
                return self.data[index]

            def __len__(self):
                return len(self.data)

        seq = TestSequence([1, 2, 3])
        result = json.dumps(seq, cls=EventSerializer)
        assert result == "[1, 2, 3]"

    def test_default_slots_object(self) -> None:
        # Test object with __slots__
        class SlotsObject:
            __slots__ = ["name", "value"]

            def __init__(self, name, value):
                self.name = name
                self.value = value

        obj = SlotsObject("test", 42)
        result = json.dumps(obj, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == {"name": "test", "value": 42}

    def test_default_dict_object(self) -> None:
        # Test object with __dict__
        class DictObject:
            def __init__(self, name, value):
                self.name = name
                self.name = name
                self.value = value

        obj = DictObject("test", 42)
        result = json.dumps(obj, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == {"name": "test", "value": 42}

    def test_default_circular_reference(self) -> None:
        # Test object with circular reference
        class Node:
            def __init__(self, name):
                self.name = name
                self.parent = None
                self.children = []

        parent = Node("parent")
        child = Node("child")
        parent.children.append(child)
        child.parent = parent  # Creates circular reference

        result = json.dumps(parent, cls=EventSerializer)
        decoded_result = json.loads(result)
        assert decoded_result == {
            "name": "parent",
            "parent": None,
            "children": [{"name": "child", "parent": "Node", "children": []}],
        }

    def test_encode(self) -> None:
        # Test encode method
        test_data = {"name": "test", "value": 42}
        serializer = EventSerializer()
        result = serializer.encode(test_data)
        assert json.loads(result) == test_data

        # Test with circular reference
        class Node:
            def __init__(self, name):
                self.name = name
                self.parent = None

        parent = Node("parent")
        child = Node("child")
        parent.children = [child]
        child.parent = parent  # Creates circular reference

        result = serializer.encode(parent)
        # Should not raise an error and should produce valid JSON
        parsed = json.loads(result)
        assert parsed["name"] == "parent"
        assert parsed["children"][0]["name"] == "child"
        assert parsed["children"][0]["parent"] == "Node"

    def test_encode_error(self) -> None:
        # Test encode method with error
        class BadObject:
            def __repr__(self):
                return "BadObject"

            def __str__(self):
                return "BadObject"

        # Mock the super().encode to raise an exception
        with patch.object(json.JSONEncoder, "encode", side_effect=Exception("Encoding error")):
            serializer = EventSerializer()
            result = serializer.encode(BadObject())
            assert "not serializable object of type: BadObject" in result

    @pytest.mark.parametrize(
        "value,expected",
        [
            (0, True),
            (42, True),
            (9007199254740991, True),  # Max safe integer
            (9007199254740992, False),  # Outside JS safe integer range
            (-9007199254740991, True),  # Min safe integer
            (-9007199254740992, False),  # Outside JS safe integer range
        ],
    )
    def test_is_js_safe_integer(self, value: int, expected: bool) -> None:
        # Test is_js_safe_integer method
        result = EventSerializer.is_js_safe_integer(value)
        assert result == expected


class TestSerializeToStr:
    def test_serialize_string(self) -> None:
        # Test with string input
        result = serialize_to_str("test")
        assert result == "test"

    def test_serialize_primitives(self) -> None:
        # Test with primitive types
        assert serialize_to_str(None) == "null"
        assert serialize_to_str(True) == "true"
        assert serialize_to_str(42) == "42"
        assert serialize_to_str(3.14) == "3.14"

    def test_serialize_complex_objects(self) -> None:
        # Test with complex objects
        test_data = {"string": "value", "number": 42, "list": [1, 2, 3], "nested": {"key": "value"}}
        result = serialize_to_str(test_data)
        # Should be a valid JSON string
        parsed = json.loads(result)
        assert parsed == test_data

    def test_serialize_non_serializable(self) -> None:
        # Test with non-serializable object
        class NonSerializable:
            def __repr__(self):
                raise Exception("Cannot represent")

        result = serialize_to_str(NonSerializable())
        assert result == "{}"

    def test_serialize_obj_with_empty_slots(self) -> None:
        class NoSlots:
            __slots__ = []

        assert serialize_to_str(NoSlots()) == '"<NoSlots>"'

    def test_serialize_non_serializable_class(self) -> None:
        # Test with non-serializable object
        from openai import OpenAI

        client = OpenAI(api_key="test")

        class NonSerializable:
            def __init__(self, client: Any) -> None:
                self.client = client

        n = NonSerializable(client=client)

        assert serialize_to_str(n) == (
            '{"client": {"api_key": "test", "organization": null, "project": null, '
            '"websocket_base_url": null, "max_retries": 2, "timeout": {"connect": 5.0, '
            '"read": 600, "write": 600, "pool": 600}, "completions": {}, "chat": {}, '
            '"embeddings": {}, "files": {}, "images": {}, "audio": {}, "moderations": {}, '
            '"models": {}, "fine_tuning": {}, "beta": {}, "batches": {}, "uploads": {}, '
            '"with_raw_response": {"completions": {"create": {}}, "chat": {}, '
            '"embeddings": {"create": {}}, "files": {"create": {}, "retrieve": {}, '
            '"list": {}, "delete": {}, "content": {}, "retrieve_content": {}}, "images": '
            '{"create_variation": {}, "edit": {}, "generate": {}}, "audio": {}, '
            '"moderations": {"create": {}}, "models": {"retrieve": {}, "list": {}, '
            '"delete": {}}, "fine_tuning": {}, "beta": {}, "batches": {"create": {}, '
            '"retrieve": {}, "list": {}, "cancel": {}}, "uploads": {"create": {}, '
            '"cancel": {}, "complete": {}}}, "with_streaming_response": {"completions": '
            '{"create": {}}, "chat": {}, "embeddings": {"create": {}}, "files": '
            '{"create": {}, "retrieve": {}, "list": {}, "delete": {}, "content": {}, '
            '"retrieve_content": {}}, "images": {"create_variation": {}, "edit": {}, '
            '"generate": {}}, "audio": {}, "moderations": {"create": {}}, "models": '
            '{"retrieve": {}, "list": {}, "delete": {}}, "fine_tuning": {}, "beta": {}, '
            '"batches": {"create": {}, "retrieve": {}, "list": {}, "cancel": {}}, '
            '"uploads": {"create": {}, "cancel": {}, "complete": {}}}}}'
        )


def test_serialize_complex_example_with_dataclasses():
    @dataclass
    class ModelConfig:
        model_name: str
        client: Any
        supports_tool_calling: bool = False
        max_tokens: int = 1024

    from openai import OpenAI

    client = OpenAI(api_key="test")

    model_config = ModelConfig(model_name="gpt-4o", client=client, supports_tool_calling=True)

    assert serialize_to_str(model_config) == (
        '{"model_name": "gpt-4o", "client": {"api_key": "test", "organization": null, '
        '"project": null, "websocket_base_url": null, "max_retries": 2, "timeout": '
        '{"connect": 5.0, "read": 600, "write": 600, "pool": 600}, "completions": {}, '
        '"chat": {}, "embeddings": {}, "files": {}, "images": {}, "audio": {}, '
        '"moderations": {}, "models": {}, "fine_tuning": {}, "beta": {}, "batches": '
        '{}, "uploads": {}, "with_raw_response": {"completions": {"create": {}}, '
        '"chat": {}, "embeddings": {"create": {}}, "files": {"create": {}, '
        '"retrieve": {}, "list": {}, "delete": {}, "content": {}, "retrieve_content": '
        '{}}, "images": {"create_variation": {}, "edit": {}, "generate": {}}, '
        '"audio": {}, "moderations": {"create": {}}, "models": {"retrieve": {}, '
        '"list": {}, "delete": {}}, "fine_tuning": {}, "beta": {}, "batches": '
        '{"create": {}, "retrieve": {}, "list": {}, "cancel": {}}, "uploads": '
        '{"create": {}, "cancel": {}, "complete": {}}}, "with_streaming_response": '
        '{"completions": {"create": {}}, "chat": {}, "embeddings": {"create": {}}, '
        '"files": {"create": {}, "retrieve": {}, "list": {}, "delete": {}, "content": '
        '{}, "retrieve_content": {}}, "images": {"create_variation": {}, "edit": {}, '
        '"generate": {}}, "audio": {}, "moderations": {"create": {}}, "models": '
        '{"retrieve": {}, "list": {}, "delete": {}}, "fine_tuning": {}, "beta": {}, '
        '"batches": {"create": {}, "retrieve": {}, "list": {}, "cancel": {}}, '
        '"uploads": {"create": {}, "cancel": {}, "complete": {}}}}, '
        '"supports_tool_calling": true, "max_tokens": 1024}'
    )
