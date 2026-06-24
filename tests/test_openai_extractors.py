"""Tests for OpenAI extractors utility functions."""

from __future__ import annotations

from typing import Any
from unittest.mock import Mock

import pytest

from galileo.openai.extractors import _openai_content_parts_to_blocks, _parse_usage, convert_to_galileo_message
from galileo.schema.content_blocks import DataContentBlock, TextContentBlock
from galileo.schema.message import LoggedMessage
from galileo_core.schemas.logging.llm import Message


class TestParseUsage:
    """Test _parse_usage function."""

    def test_none_returns_none(self) -> None:
        # Given: no usage data
        # When: parsing None usage
        result = _parse_usage(None)

        # Then: returns None
        assert result is None

    def test_new_field_names_unchanged(self) -> None:
        # Given: usage dict with current OpenAI field names
        usage = {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30}

        # When: parsing usage
        result = _parse_usage(usage)

        # Then: fields are preserved as-is
        assert result["input_tokens"] == 10
        assert result["output_tokens"] == 20
        assert result["total_tokens"] == 30

    def test_old_field_names_mapped(self) -> None:
        # Given: usage dict with legacy OpenAI field names
        usage = {"prompt_tokens": 15, "completion_tokens": 25, "total_tokens": 40}

        # When: parsing usage
        result = _parse_usage(usage)

        # Then: old fields are mapped to new names
        assert result["input_tokens"] == 15
        assert result["output_tokens"] == 25
        assert result["total_tokens"] == 40
        assert "prompt_tokens" not in result
        assert "completion_tokens" not in result

    def test_input_tokens_details_flattened(self) -> None:
        # Given: usage with input_tokens_details nested dict
        usage = {"input_tokens": 100, "output_tokens": 50, "input_tokens_details": {"cached_tokens": 80}}

        # When: parsing usage
        result = _parse_usage(usage)

        # Then: details are flattened into the top-level dict
        assert result["cached_tokens"] == 80
        assert "input_tokens_details" not in result

    def test_output_tokens_details_flattened(self) -> None:
        # Given: usage with output_tokens_details nested dict
        usage = {"input_tokens": 100, "output_tokens": 50, "output_tokens_details": {"reasoning_tokens": 30}}

        # When: parsing usage
        result = _parse_usage(usage)

        # Then: details are flattened into the top-level dict
        assert result["reasoning_tokens"] == 30
        assert "output_tokens_details" not in result

    def test_old_names_with_details(self) -> None:
        # Given: usage with both legacy field names and detail dicts
        usage = {
            "prompt_tokens": 100,
            "completion_tokens": 50,
            "total_tokens": 150,
            "input_tokens_details": {"cached_tokens": 80},
            "output_tokens_details": {"reasoning_tokens": 30},
        }

        # When: parsing usage
        result = _parse_usage(usage)

        # Then: old names are mapped and details are flattened
        assert result["input_tokens"] == 100
        assert result["output_tokens"] == 50
        assert result["total_tokens"] == 150
        assert result["cached_tokens"] == 80
        assert result["reasoning_tokens"] == 30
        assert "prompt_tokens" not in result
        assert "completion_tokens" not in result

    def test_object_with_dunder_dict(self) -> None:
        # Given: usage as an object (e.g. OpenAI Usage model) instead of a dict
        usage_obj = Mock()
        usage_obj.__dict__ = {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}

        # When: parsing usage object
        result = _parse_usage(usage_obj)

        # Then: fields are extracted and mapped correctly
        assert result["input_tokens"] == 10
        assert result["output_tokens"] == 20
        assert result["total_tokens"] == 30

    def test_does_not_mutate_original_dict(self) -> None:
        # Given: a usage dict
        usage = {"prompt_tokens": 10, "completion_tokens": 20}

        # When: parsing usage
        _parse_usage(usage)

        # Then: original dict is not modified
        assert "prompt_tokens" in usage
        assert "completion_tokens" in usage

    @pytest.mark.parametrize(
        "usage_data,expected_keys",
        [
            ({"input_tokens": 0, "output_tokens": 0}, {"input_tokens", "output_tokens"}),
            ({"total_tokens": 100}, {"total_tokens"}),
            ({}, set()),
        ],
        ids=["zeros", "only-total", "empty-dict"],
    )
    def test_edge_cases(self, usage_data: dict[str, Any], expected_keys: set[str]) -> None:
        # Given: various edge-case usage dicts
        # When: parsing usage
        result = _parse_usage(usage_data)

        # Then: result contains expected keys
        assert set(result.keys()) == expected_keys


class TestOpenAiContentPartsToBlocks:
    """Tests for _openai_content_parts_to_blocks."""

    def test_text_part(self) -> None:
        # Given: a single text content part
        parts = [{"type": "text", "text": "hello"}]

        # When: converting parts to blocks
        result = _openai_content_parts_to_blocks(parts)

        # Then: a TextContentBlock is returned
        assert result is not None
        assert len(result) == 1
        assert isinstance(result[0], TextContentBlock)
        assert result[0].text == "hello"

    def test_image_url_data_uri(self) -> None:
        # Given: an image_url part containing a data URI
        parts = [{"type": "image_url", "image_url": {"url": "data:image/png;base64,abc123"}}]

        # When: converting parts to blocks
        result = _openai_content_parts_to_blocks(parts)

        # Then: a DataContentBlock is returned with the parsed mime type and base64 data
        assert result is not None
        assert len(result) == 1
        block = result[0]
        assert isinstance(block, DataContentBlock)
        assert block.mime_type == "image/png"
        assert block.base64 == "abc123"

    def test_image_url_plain_url(self) -> None:
        # Given: an image_url part with a plain HTTPS URL (not a data URI)
        parts = [{"type": "image_url", "image_url": {"url": "https://example.com/img.jpg"}}]

        # When: converting parts to blocks
        result = _openai_content_parts_to_blocks(parts)

        # Then: a DataContentBlock with a url field is returned
        assert result is not None
        block = result[0]
        assert isinstance(block, DataContentBlock)
        assert block.url == "https://example.com/img.jpg"

    def test_input_audio_part(self) -> None:
        # Given: an input_audio part with base64 PCM data
        parts = [{"type": "input_audio", "input_audio": {"data": "audiob64==", "format": "mp3"}}]

        # When: converting parts to blocks
        result = _openai_content_parts_to_blocks(parts)

        # Then: a DataContentBlock with audio mime type is returned
        assert result is not None
        block = result[0]
        assert isinstance(block, DataContentBlock)
        assert block.mime_type == "audio/mp3"
        assert block.base64 == "audiob64=="

    def test_unrecognized_part_returns_none(self) -> None:
        # Given: a list containing an unrecognized part type
        parts = [{"type": "text", "text": "hi"}, {"type": "video_url", "url": "..."}]

        # When: converting parts to blocks
        result = _openai_content_parts_to_blocks(parts)

        # Then: None is returned so the caller can fall back to string serialisation
        assert result is None

    def test_mixed_text_and_image(self) -> None:
        # Given: a list with a text part followed by an image data URI
        parts = [
            {"type": "text", "text": "look at this"},
            {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,xyz"}},
        ]

        # When: converting parts to blocks
        result = _openai_content_parts_to_blocks(parts)

        # Then: both blocks are returned in order
        assert result is not None
        assert len(result) == 2
        assert isinstance(result[0], TextContentBlock)
        assert isinstance(result[1], DataContentBlock)
        assert result[1].mime_type == "image/jpeg"


class TestConvertToGalileoMessage:
    """Tests for convert_to_galileo_message — tool linkage with multimodal content."""

    def test_tool_role_with_list_content_preserves_tool_call_id(self) -> None:
        # Given: a tool-role message where content is an array of parts (not a string)
        msg = {"role": "tool", "tool_call_id": "call_abc123", "content": [{"type": "text", "text": "result"}]}

        # When: converting to a Galileo message
        result = convert_to_galileo_message(msg)

        # Then: tool_call_id is preserved on the returned LoggedMessage
        assert isinstance(result, LoggedMessage)
        assert result.tool_call_id == "call_abc123"

    def test_assistant_with_list_content_and_tool_calls_preserves_linkage(self) -> None:
        # Given: an assistant message with array content and a tool_calls list
        msg = {
            "role": "assistant",
            "content": [{"type": "text", "text": "I'll call the tool"}],
            "tool_calls": [{"id": "call_xyz", "function": {"name": "my_tool", "arguments": '{"x": 1}'}}],
        }

        # When: converting to a Galileo message
        result = convert_to_galileo_message(msg)

        # Then: tool_calls are preserved on the returned LoggedMessage
        assert isinstance(result, LoggedMessage)
        assert result.tool_calls is not None
        assert len(result.tool_calls) == 1
        assert result.tool_calls[0].id == "call_xyz"

    def test_string_content_with_tool_call_id_falls_through_to_message(self) -> None:
        # Given: a tool-role message with plain string content (not a list)
        msg = {"role": "tool", "tool_call_id": "call_def456", "content": "plain result"}

        # When: converting to a Galileo message
        result = convert_to_galileo_message(msg)

        # Then: a standard Message is returned (not LoggedMessage) with tool_call_id
        assert isinstance(result, Message)
        assert result.tool_call_id == "call_def456"
