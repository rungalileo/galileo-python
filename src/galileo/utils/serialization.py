import datetime as dt
import enum
import json
import logging
from asyncio import Queue
from collections.abc import Sequence
from dataclasses import is_dataclass
from datetime import date, datetime
from json import JSONEncoder
from pathlib import Path
from typing import Any
from uuid import UUID

from pydantic import BaseModel

from galileo.utils.dependencies import is_langchain_available, is_langgraph_available, is_proto_plus_available

_logger = logging.getLogger(__name__)


def serialize_datetime(v: dt.datetime) -> str:
    """
    Serialize a datetime including timezone info.

    Uses the timezone info provided if present, otherwise uses the current runtime's timezone info.

    UTC datetimes end in "Z" while all other timezones are represented as offset from UTC, e.g. +05:00.
    """

    def _serialize_zoned_datetime(v: dt.datetime) -> str:
        if v.tzinfo is not None and v.tzinfo.tzname(None) == dt.timezone.utc.tzname(None):
            # UTC is a special case where we use "Z" at the end instead of "+00:00"
            return v.isoformat().replace("+00:00", "Z")
        # Delegate to the typical +/- offset format
        return v.isoformat()

    if v.tzinfo is not None:
        return _serialize_zoned_datetime(v)
    local_tz = dt.datetime.now().astimezone().tzinfo
    localized_dt = v.replace(tzinfo=local_tz)
    return _serialize_zoned_datetime(localized_dt)


def map_langchain_role(role: str) -> str:
    role_map = {"ai": "assistant", "human": "user"}
    return role_map.get(role, role)


class EventSerializer(JSONEncoder):
    """Custom JSON encoder to assist in the serialization of a wide range of objects."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.seen: set[int] = set()  # Track seen objects to detect circular references

    def default(self, obj: Any) -> Any:
        try:
            if isinstance(obj, datetime):
                return serialize_datetime(obj)

            if isinstance(obj, (Exception, KeyboardInterrupt)):
                return f"{type(obj).__name__}: {obj!s}"

            if isinstance(obj, enum.Enum):
                return obj.value

            if isinstance(obj, Queue):
                return type(obj).__name__

            if isinstance(obj, UUID):
                return str(obj)

            if isinstance(obj, bytes):
                try:
                    return obj.decode("utf-8")
                except UnicodeDecodeError:
                    return "<not serializable bytes>"

            if isinstance(obj, date):
                return obj.isoformat()

            if isinstance(obj, Path):
                return str(obj)

            if is_langchain_available:
                from langchain_core.agents import AgentAction
                from langchain_core.documents import Document as LangchainDocument
                from langchain_core.load.serializable import Serializable
                from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage, ToolMessage
                from langchain_core.outputs import ChatGeneration, LLMResult
                from langchain_core.prompt_values import ChatPromptValue

                if isinstance(obj, (AgentAction, ChatPromptValue)):
                    return self.default(obj.messages)
                if isinstance(obj, ChatGeneration):
                    return self.default(obj.message)
                if isinstance(obj, LLMResult):
                    return self.default(obj.generations[0])
                if isinstance(obj, (AIMessageChunk, AIMessage)):
                    # Map the `type` to `role`.
                    if hasattr(obj, "model_dump"):
                        dumped = obj.model_dump(
                            mode="json", include={"content", "type", "additional_kwargs", "tool_calls"}
                        )
                    else:
                        # Fallback to using the dict method if model_dump is not available i.e pydantic v1
                        dumped = obj.dict(include={"content", "type", "additional_kwargs", "tool_calls"})
                    content = dumped.get("content")
                    if isinstance(content, list):
                        # Responses API returns content as a list of dicts
                        # Convert list content to string format for consistency
                        if content and isinstance(content[0], dict):
                            dumped["content"] = content[0].get("text", "")
                    dumped["role"] = map_langchain_role(dumped.pop("type"))
                    additional_kwargs = dumped.pop("additional_kwargs", {})
                    # Check both direct attribute and additional_kwargs for tool_calls
                    if not dumped.get("tool_calls") and "tool_calls" in additional_kwargs:
                        dumped["tool_calls"] = additional_kwargs.pop("tool_calls")

                    if dumped.get("tool_calls") == []:
                        dumped.pop("tool_calls")

                    # Transform LangChain tool_calls format to match Galileo's ToolCall schema
                    if "tool_calls" in dumped and isinstance(dumped["tool_calls"], list):
                        transformed_tool_calls = []
                        for tool_call in dumped["tool_calls"]:
                            if isinstance(tool_call, dict):
                                # Check if it's already in Galileo ToolCall format (has 'function' key)
                                if "function" in tool_call:
                                    transformed_tool_calls.append(tool_call)
                                # Otherwise transform from LangChain format
                                elif "name" in tool_call and "id" in tool_call:
                                    args = tool_call.get("args", {})
                                    # Convert args to JSON string if it's a dict
                                    arguments = args if isinstance(args, str) else json.dumps(args)
                                    transformed_tool_calls.append(
                                        {
                                            "id": tool_call["id"],
                                            "function": {"name": tool_call["name"], "arguments": arguments},
                                        }
                                    )
                                else:
                                    # Keep as-is if format is unknown
                                    transformed_tool_calls.append(tool_call)
                            else:
                                transformed_tool_calls.append(tool_call)
                        dumped["tool_calls"] = transformed_tool_calls

                    if "reasoning" in additional_kwargs:
                        dumped["reasoning"] = additional_kwargs.pop("reasoning")
                    return dumped
                if isinstance(obj, ToolMessage):
                    # Map the `type` to `role`.
                    if hasattr(obj, "model_dump"):
                        dumped = obj.model_dump(mode="json", include={"content", "type", "status", "tool_call_id"})
                    else:
                        # Fallback to using the dict method if model_dump is not available i.e pydantic v1
                        dumped = obj.dict(include={"content", "type", "status", "tool_call_id"})
                    dumped["role"] = map_langchain_role(dumped.pop("type"))
                    return dumped
                if isinstance(obj, BaseMessage):
                    # Map the `type` to `role`.
                    if hasattr(obj, "model_dump"):
                        dumped = obj.model_dump(mode="json", include={"content", "type"})
                    else:
                        # Fallback to using the dict method if model_dump is not available i.e pydantic v1
                        dumped = obj.dict(include={"content", "type"})
                    dumped["role"] = map_langchain_role(dumped.pop("type"))
                    return dumped

                if isinstance(obj, LangchainDocument):
                    if hasattr(obj, "model_dump"):
                        return self.default(obj.model_dump(mode="json", include={"page_content", "metadata"}))
                    # Fallback to using the dict method if model_dump is not available i.e pydantic v1
                    return self.default(obj.dict(include={"page_content", "metadata"}))

                if isinstance(obj, Serializable):
                    serialized = obj.to_json()
                    if "kwargs" in serialized:
                        kwargs = serialized["kwargs"]
                        kwargs.pop("type", None)
                        return kwargs
                    return serialized

            # Handle langgraph types before the generic dataclass check
            # Command is a dataclass with __slots__, so generic dataclass handling fails
            # Local import to avoid hard dependency on optional `langgraph`
            if is_langgraph_available:
                from langgraph.types import Command, Send

                if isinstance(obj, Command):
                    result = {}
                    for slot in ("graph", "update", "resume", "goto"):
                        value = getattr(obj, slot, None)
                        if value is not None:
                            result[slot] = self.default(value)
                    return result

                if isinstance(obj, Send):
                    return {"node": self.default(obj.node), "arg": self.default(obj.arg)}

            if is_dataclass(obj):
                return {self.default(k): self.default(v) for k, v in obj.__dict__.items()}

            # Handle Pydantic model classes (not instances)
            if isinstance(obj, type) and issubclass(obj, BaseModel):
                if hasattr(obj, "model_json_schema") and callable(obj.model_json_schema):
                    try:
                        return obj.model_json_schema()
                    except Exception:
                        # If schema generation fails, return class name
                        return f"<{obj.__name__}>"
                return f"<{obj.__name__}>"

            if isinstance(obj, BaseModel):
                if hasattr(obj, "model_dump"):
                    return self.default(
                        obj.model_dump(mode="json", exclude_none=True, exclude_unset=True, exclude_defaults=True)
                    )
                # Fallback to using the dict method if model_dump is not available i.e pydantic v1
                return self.default(obj.dict(exclude_none=True, exclude_unset=True, exclude_defaults=True))

            # 64-bit integers might overflow the JavaScript safe integer range.
            if isinstance(obj, int):
                return obj if self.is_js_safe_integer(obj) else str(obj)

            # Standard JSON-encodable types
            if isinstance(obj, (str, float, type(None))):
                return obj

            if isinstance(obj, (tuple, set, frozenset)):
                return list(obj)

            if isinstance(obj, dict):
                return {self.default(k): self.default(v) for k, v in obj.items()}

            if isinstance(obj, list):
                return [self.default(item) for item in obj]

            # Important: this needs to be always checked after str and bytes types.
            # Bare protobuf messages (google.protobuf.message.Message) implement
            # Sequence, so this branch handles them as iterables. Proto-plus
            # messages (proto.Message) are handled separately below.
            if isinstance(obj, Sequence):
                return [self.default(item) for item in obj]

            # Handle proto-plus messages (e.g. google.cloud.aiplatform types).
            # Their __dict__ only contains private attrs, so the generic
            # __dict__ serialization below would produce empty objects.
            if is_proto_plus_available:
                # Lazy import: proto-plus is an optional dependency used by GCP tool classes (e.g. google.cloud.aiplatform)
                import proto

                if isinstance(obj, proto.Message):
                    return self.default(proto.Message.to_dict(obj, use_integers_for_enums=False))

            if hasattr(obj, "__slots__") and len(obj.__slots__) > 0:
                return self.default({slot: getattr(obj, slot, None) for slot in obj.__slots__})

            if hasattr(obj, "__dict__"):
                obj_id = id(obj)

                if obj_id in self.seen:
                    # Break on circular references
                    return type(obj).__name__
                self.seen.add(obj_id)
                result = {k: self.default(v) for k, v in vars(obj).items() if not k.startswith("_")}
                self.seen.remove(obj_id)

                return result

            # Return object type rather than JSONEncoder.default(obj) which simply raises a TypeError
            return f"<{type(obj).__name__}>"

        except Exception:
            _logger.warning(f"Serialization failed for object of type {type(obj).__name__}")
            return f'"<not serializable object of type: {type(obj).__name__}>"'

    def encode(self, obj: Any) -> str:
        self.seen.clear()  # Clear seen objects before each encode call

        try:
            return super().encode(self.default(obj))
        except Exception:
            return f'"<not serializable object of type: {type(obj).__name__}>"'  # escaping the string to avoid JSON parsing errors

    @staticmethod
    def is_js_safe_integer(value: int) -> bool:
        """Ensure the value is within JavaScript's safe range for integers.

        Python's 64-bit integers can exceed this range, necessitating this check.
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER
        """
        max_safe_int = 2**53 - 1
        min_safe_int = -(2**53) + 1

        return min_safe_int <= value <= max_safe_int


def serialize_to_str(input_data: Any) -> str:
    """Safely serialize data to a JSON string."""
    if isinstance(input_data, str):
        return input_data

    if input_data is None or isinstance(input_data, (bool, int, float)):
        return json.dumps(input_data)

    try:
        # Use the EventSerializer for initial serialization
        serializer = EventSerializer()

        # First try to serialize directly using the serializer's default method
        processed_data = serializer.default(input_data)

        # Now encode it to a JSON string (this will always return a string)
        return serializer.encode(processed_data)
    except Exception:
        # Fallback if anything goes wrong
        _logger.warning(f"Serialization failed for object of type {type(input_data).__name__}")
        return ""


def convert_to_string_dict(input_: dict) -> dict[str, str]:
    """
    Convert a dict with arbitrary values to a dict[str, str] by converting
    all values to their string representations.
    """
    result: dict[str, str] = {}
    if not input_:
        return result
    for key, value in input_.items():
        # Ensure key is a string
        string_key = str(key)

        # Convert value to string based on type
        if value is None:
            string_value = ""
        elif isinstance(value, (dict, list, tuple)):
            # For complex types, use JSON serialization
            string_value = json.dumps(value, cls=EventSerializer)
        else:
            # For primitive types, convert directly to string
            string_value = str(value)

        result[string_key] = string_value

    return result


def convert_time_delta_to_ns(time_delta: dt.timedelta) -> int:
    """Convert a timedelta object to nanoseconds."""
    return int(time_delta.total_seconds() * 1e9)
