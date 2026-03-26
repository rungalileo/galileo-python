"""Tests for OpenAI extractors utility functions."""

from __future__ import annotations

from typing import Any
from unittest.mock import Mock

import pytest

from galileo.openai.extractors import _parse_usage


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
