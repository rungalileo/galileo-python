"""Tests for HTTP status code extraction and classification."""

import pytest

from galileo_adk import GalileoADKPlugin
from galileo_adk.plugin import _extract_status_code, _is_http_status_code


class TestIsHttpStatusCode:
    """Tests for HTTP status code validation."""

    @pytest.mark.parametrize(
        ("code", "expected"),
        [
            (100, True),  # Continue
            (200, True),  # OK
            (201, True),  # Created
            (301, True),  # Moved Permanently
            (400, True),  # Bad Request
            (401, True),  # Unauthorized
            (403, True),  # Forbidden
            (404, True),  # Not Found
            (429, True),  # Too Many Requests
            (500, True),  # Internal Server Error
            (502, True),  # Bad Gateway
            (503, True),  # Service Unavailable
            (599, True),  # Upper bound
            (99, False),  # Below range
            (600, False),  # Above range
            (8, False),  # gRPC code (RESOURCE_EXHAUSTED)
            (0, False),  # Zero
            (-1, False),  # Negative
        ],
    )
    def test_is_http_status_code(self, code: int, expected: bool) -> None:
        """Validate HTTP status code range checking."""
        # Given: a status code value from the parametrized input
        # When: we call _is_http_status_code(code)
        # Then: the function returns the expected boolean
        assert _is_http_status_code(code) == expected


class TestExtractStatusCode:
    """Tests for status code extraction from various error types."""

    def test_extract_from_code_attribute(self) -> None:
        """Extract status code from error.code attribute."""
        error = Exception("Rate limit exceeded")
        error.code = 429  # type: ignore[attr-defined]
        assert _extract_status_code(error) == 429

    def test_extract_from_enum_value(self) -> None:
        """Extract status code from enum-like code attribute."""

        class MockEnum:
            value = 401

        error = Exception("Auth error")
        error.code = MockEnum()  # type: ignore[attr-defined]
        assert _extract_status_code(error) == 401

    def test_extract_from_status_code_attribute(self) -> None:
        """Extract from error.status_code attribute."""
        error = Exception("HTTP error")
        error.status_code = 503  # type: ignore[attr-defined]
        assert _extract_status_code(error) == 503

    def test_extract_from_error_message_429(self) -> None:
        """Extract 429 from error message string."""
        error = Exception("429 RESOURCE_EXHAUSTED: Rate limit exceeded")
        assert _extract_status_code(error) == 429

    def test_extract_from_error_message_500(self) -> None:
        """Extract 500 from error message string."""
        error = Exception("500 Internal Server Error")
        assert _extract_status_code(error) == 500

    def test_extract_from_error_message_with_http_prefix(self) -> None:
        """Extract status code from 'HTTP 404' pattern."""
        error = Exception("Error: HTTP 404 Not Found - model does not exist")
        assert _extract_status_code(error) == 404

    def test_extract_from_error_message_with_status_prefix(self) -> None:
        """Extract status code from 'status: 503' pattern."""
        error = Exception("Request failed with status: 503")
        assert _extract_status_code(error) == 503

    def test_defaults_to_500_for_unknown_error(self) -> None:
        """Default to 500 when no status code found."""
        error = Exception("Something went wrong")
        assert _extract_status_code(error) == 500

    def test_grpc_codes_not_treated_as_http(self) -> None:
        """gRPC codes (< 100) should not be treated as HTTP codes."""
        # gRPC RESOURCE_EXHAUSTED = 8
        error = Exception("gRPC error")
        error.code = 8  # type: ignore[attr-defined]
        assert _extract_status_code(error) == 500  # Falls back to default

    def test_code_takes_precedence_over_message(self) -> None:
        """error.code attribute takes precedence over message parsing."""
        error = Exception("500 Internal Server Error")
        error.code = 429  # type: ignore[attr-defined]
        assert _extract_status_code(error) == 429

    def test_status_code_attribute_used_when_code_invalid(self) -> None:
        """status_code used when code attribute is not valid HTTP."""
        error = Exception("Error")
        error.code = 8  # Invalid HTTP (gRPC)  # type: ignore[attr-defined]
        error.status_code = 503  # type: ignore[attr-defined]
        assert _extract_status_code(error) == 503

    def test_regex_does_not_match_embedded_numbers(self) -> None:
        """Regex does not false-positive on embedded numbers like '500ms'."""
        error = Exception("Failed after 500ms timeout")
        assert _extract_status_code(error) == 500  # Default, NOT extracted from "500ms"

    def test_regex_matches_leading_status_code(self) -> None:
        """Leading status code at start of message is extracted."""
        error = Exception("503 Service Unavailable")
        assert _extract_status_code(error) == 503

    def test_code_beats_status_code_beats_message(self) -> None:
        """error.code takes precedence over status_code and message."""
        error = Exception("404 Not Found")
        error.code = 429  # type: ignore[attr-defined]
        error.status_code = 503  # type: ignore[attr-defined]
        assert _extract_status_code(error) == 429

    def test_status_code_beats_message(self) -> None:
        """error.status_code takes precedence over message parsing."""
        error = Exception("404 Not Found")
        error.status_code = 503  # type: ignore[attr-defined]
        assert _extract_status_code(error) == 503


class TestFatalErrorClassification:
    """Tests for fatal error detection logic."""

    @pytest.fixture
    def plugin(self):
        return GalileoADKPlugin(ingestion_hook=lambda r: None)

    def test_401_is_fatal(self, plugin) -> None:
        """401 Unauthorized is a fatal error."""
        assert plugin._is_fatal_error(401) is True

    def test_403_is_fatal(self, plugin) -> None:
        """403 Forbidden is a fatal error."""
        assert plugin._is_fatal_error(403) is True

    def test_429_is_fatal(self, plugin) -> None:
        """429 Too Many Requests is a fatal error."""
        assert plugin._is_fatal_error(429) is True

    def test_500_is_not_fatal(self, plugin) -> None:
        """500 Internal Server Error is not fatal (may be retried)."""
        assert plugin._is_fatal_error(500) is False

    def test_404_is_not_fatal(self, plugin) -> None:
        """404 Not Found is not fatal."""
        assert plugin._is_fatal_error(404) is False

    def test_502_is_not_fatal(self, plugin) -> None:
        """502 Bad Gateway is not fatal."""
        assert plugin._is_fatal_error(502) is False
