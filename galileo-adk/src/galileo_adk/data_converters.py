"""Data converters for ADK to Galileo format transformations."""

import base64
import json
import logging
import uuid
from typing import Any

from galileo_core.schemas.logging.llm import Message, MessageRole, ToolCall, ToolCallFunction

_logger = logging.getLogger(__name__)


def generate_tool_call_id(name: str, index: int = 0) -> str:
    """Generate a unique tool call ID for linking function calls and responses."""
    return f"call_{name}_{index}_{uuid.uuid4().hex[:8]}"


def convert_adk_content_to_galileo_messages(content: Any) -> list[Message]:
    """Convert ADK Content to list of Galileo Messages, preserving part order.

    Tracks call IDs for function calls and links them to their responses.
    """
    messages: list[Message] = []
    if not hasattr(content, "parts") or not content.parts:
        return messages

    base_role = _map_adk_role_to_galileo(getattr(content, "role", "user"))

    call_id_map: dict[str, str] = {}

    for i, part in enumerate(content.parts):
        message = _convert_part_to_message_with_call_id(part, base_role, i, call_id_map)
        if message:
            messages.append(message)

    return messages


def _convert_part_to_message_with_call_id(
    part: Any, base_role: MessageRole, index: int, call_id_map: dict[str, str]
) -> Message | None:
    """Convert a single ADK part to a Galileo Message with call ID tracking."""
    if hasattr(part, "text") and part.text:
        return Message(content=part.text, role=base_role)

    if hasattr(part, "inline_data") and part.inline_data:
        return _convert_inline_data(part.inline_data, base_role)

    if hasattr(part, "file_data") and part.file_data:
        return _convert_file_data(part.file_data, base_role)

    if hasattr(part, "function_call") and part.function_call:
        name = getattr(part.function_call, "name", "unknown")
        adk_call_id = getattr(part.function_call, "id", None)
        call_id = generate_tool_call_id(name, index)
        map_key = adk_call_id if adk_call_id else f"{name}_{index}"
        call_id_map[map_key] = call_id
        return _convert_function_call(part.function_call, call_id)

    if hasattr(part, "function_response") and part.function_response:
        adk_response_id = getattr(part.function_response, "id", None)
        name = getattr(part.function_response, "name", "unknown")
        map_key = adk_response_id if adk_response_id else f"{name}_{index}"
        call_id = call_id_map.get(map_key)
        return _convert_function_response(part.function_response, call_id)

    return None


def _convert_inline_data(inline_data: Any, base_role: MessageRole) -> Message:
    """Convert inline binary data to a Message with base64-encoded payload."""
    mime_type = getattr(inline_data, "mime_type", "application/octet-stream")
    data = getattr(inline_data, "data", b"")
    encoded = base64.b64encode(data).decode("utf-8") if isinstance(data, bytes) else str(data)
    return Message(
        content=json.dumps({"type": "inline_data", "mime_type": mime_type, "data": encoded}),
        role=base_role,
    )


def _convert_file_data(file_data: Any, base_role: MessageRole) -> Message:
    """Convert file reference to a Message."""
    payload: dict[str, Any] = {"type": "file_data", "file_uri": getattr(file_data, "file_uri", "")}
    if mime_type := getattr(file_data, "mime_type", None):
        payload["mime_type"] = mime_type
    return Message(content=json.dumps(payload), role=base_role)


def _convert_function_call(function_call: Any, call_id: str | None = None) -> Message:
    """Convert function call to a Message with structured tool_calls.

    Args:
        function_call: ADK function_call object with name and args
        call_id: Optional unique ID for linking to function response

    Returns:
        Message with role=assistant and tool_calls list
    """
    name = getattr(function_call, "name", "unknown")
    args = getattr(function_call, "args", {})
    if hasattr(args, "model_dump"):
        args = args.model_dump()
    elif not isinstance(args, dict):
        args = {"raw": str(args)}

    if call_id is None:
        call_id = generate_tool_call_id(name)

    tool_call = ToolCall(
        id=call_id,
        function=ToolCallFunction(
            name=name,
            arguments=json.dumps(args) if isinstance(args, dict) else str(args),
        ),
    )
    return Message(content="", role=MessageRole.assistant, tool_calls=[tool_call])


def _convert_function_response(function_response: Any, call_id: str | None = None) -> Message:
    """Convert function response to a Message with tool role and call_id linking.

    Args:
        function_response: ADK function_response object with name and response
        call_id: Optional ID linking to the original function call

    Returns:
        Message with role=tool and tool_call_id for linking
    """
    response = getattr(function_response, "response", {})
    if hasattr(response, "model_dump"):
        response = response.model_dump()
    elif not isinstance(response, dict | list | str | int | float | bool | type(None)):
        response = {"raw": str(response)}

    content = json.dumps(response) if not isinstance(response, str) else response
    return Message(content=content, role=MessageRole.tool, tool_call_id=call_id)


def convert_adk_content_to_galileo_message(content: Any) -> Message:
    """Convert ADK Content to single Galileo Message."""
    messages = convert_adk_content_to_galileo_messages(content)
    return messages[0] if messages else Message(content="", role=MessageRole.assistant)


def extract_text_from_adk_content(content: Any) -> str:
    """Extract text from ADK Content."""
    if not hasattr(content, "parts") or not content.parts:
        return ""
    text_parts = [part.text for part in content.parts if hasattr(part, "text") and part.text]
    return " ".join(text_parts)


def _map_adk_role_to_galileo(adk_role: str) -> MessageRole:
    """Map ADK role to Galileo MessageRole."""
    role_mapping = {"user": MessageRole.user, "model": MessageRole.assistant, "system": MessageRole.system}
    return role_mapping.get(adk_role.lower(), MessageRole.user)


def convert_adk_tools_to_galileo_format(tools: Any) -> list[dict[str, Any]]:
    """Convert ADK tools to OpenAI-compatible format."""
    galileo_tools: list[dict[str, Any]] = []
    for tool in tools:
        extracted = _extract_tool_info(tool)
        if extracted:
            galileo_tools.extend(extracted)
    return galileo_tools


def _extract_tool_info(tool: Any) -> list[dict[str, Any]]:
    """Extract tool information using multiple strategies."""
    if tool_entry := _try_direct_attributes(tool):
        return [tool_entry]

    if tool_entry := _try_to_dict(tool):
        return [tool_entry]

    if entries := _try_function_declarations(tool):
        return entries

    _logger.warning(f"Could not extract tool metadata from {type(tool).__name__}")
    return []


def _try_direct_attributes(tool: Any) -> dict[str, Any] | None:
    """Try extracting tool info from common public attributes."""
    name = getattr(tool, "name", None)
    if not name:
        return None

    description = getattr(tool, "description", "") or ""
    parameters = getattr(tool, "parameters_schema", None) or getattr(tool, "parameters", None) or {}

    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": _convert_schema(parameters),
        },
    }


def _try_to_dict(tool: Any) -> dict[str, Any] | None:
    """Try extracting tool info via to_dict() method."""
    if not hasattr(tool, "to_dict"):
        return None

    try:
        tool_dict = tool.to_dict()
        if not isinstance(tool_dict, dict):
            return None

        name = tool_dict.get("name")
        if not name:
            return None

        return {
            "type": "function",
            "function": {
                "name": name,
                "description": tool_dict.get("description", ""),
                "parameters": _convert_schema(tool_dict.get("parameters", {})),
            },
        }
    except Exception:
        return None


def _try_function_declarations(tool: Any) -> list[dict[str, Any]]:
    """Try extracting from function_declarations attribute."""
    declarations = getattr(tool, "function_declarations", None)
    if not declarations:
        return []

    entries: list[dict[str, Any]] = []
    for func_decl in declarations:
        name = getattr(func_decl, "name", None)
        if not name:
            continue

        entries.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": getattr(func_decl, "description", "") or "",
                    "parameters": _convert_schema(getattr(func_decl, "parameters", {})),
                },
            }
        )

    return entries


def _convert_schema(schema: Any) -> dict[str, Any]:
    """Convert ADK schema to JSON schema format."""
    if isinstance(schema, dict):
        return schema
    if hasattr(schema, "model_json_schema"):
        return schema.model_json_schema()
    return {}
