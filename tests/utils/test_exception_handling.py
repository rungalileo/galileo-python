"""Tests for exception handling decorators."""

import logging
from unittest.mock import Mock

import httpx
import pytest

from galileo.utils.decorators import (
    INFRASTRUCTURE_EXCEPTIONS,
    RETRYABLE_STATUS_CODES,
    async_warn_catch_exception,
    retry_on_transient_http_error,
    warn_catch_exception,
)
from galileo_core.exceptions.http import GalileoHTTPException


class TestWarnCatchException:
    """Tests for the warn_catch_exception decorator."""

    def test_returns_result_on_success(self) -> None:
        """Test that the decorator returns the function result when no exception occurs."""
        test_logger = Mock(spec=logging.Logger)

        @warn_catch_exception(logger=test_logger)
        def successful_func() -> str:
            return "success"

        result = successful_func()

        assert result == "success"
        test_logger.warning.assert_not_called()

    def test_catches_http_error_and_logs_warning(self) -> None:
        """Test that httpx.HTTPError is caught and logged as warning."""
        test_logger = Mock(spec=logging.Logger)

        @warn_catch_exception(logger=test_logger)
        def failing_func() -> str:
            raise httpx.HTTPError("connection failed")

        result = failing_func()

        assert result is None
        test_logger.warning.assert_called_once()
        assert "Ingestion error" in test_logger.warning.call_args[0][0]
        assert "failing_func" in test_logger.warning.call_args[0][0]

    def test_catches_timeout_error_and_logs_warning(self) -> None:
        """Test that TimeoutError is caught and logged as warning."""
        test_logger = Mock(spec=logging.Logger)

        @warn_catch_exception(logger=test_logger)
        def timeout_func() -> str:
            raise TimeoutError("request timed out")

        result = timeout_func()

        assert result is None
        test_logger.warning.assert_called_once()

    def test_catches_connection_error_and_logs_warning(self) -> None:
        """Test that ConnectionError is caught and logged as warning."""
        test_logger = Mock(spec=logging.Logger)

        @warn_catch_exception(logger=test_logger)
        def connection_func() -> str:
            raise ConnectionError("network unreachable")

        result = connection_func()

        assert result is None
        test_logger.warning.assert_called_once()

    def test_does_not_catch_non_infrastructure_exceptions(self) -> None:
        """Test that non-infrastructure exceptions are re-raised."""
        test_logger = Mock(spec=logging.Logger)

        @warn_catch_exception(logger=test_logger)
        def value_error_func() -> str:
            raise ValueError("invalid value")

        with pytest.raises(ValueError) as exc_info:
            value_error_func()

        assert "invalid value" in str(exc_info.value)
        test_logger.warning.assert_not_called()

    def test_custom_exceptions_parameter(self) -> None:
        """Test that custom exception types can be specified."""
        test_logger = Mock(spec=logging.Logger)

        @warn_catch_exception(logger=test_logger, exceptions=(ValueError,))
        def custom_exception_func() -> str:
            raise ValueError("caught by custom exceptions")

        result = custom_exception_func()

        assert result is None
        test_logger.warning.assert_called_once()


class TestAsyncWarnCatchException:
    """Tests for the async_warn_catch_exception decorator."""

    @pytest.mark.asyncio
    async def test_returns_result_on_success(self) -> None:
        """Test that the decorator returns the function result when no exception occurs."""
        test_logger = Mock(spec=logging.Logger)

        @async_warn_catch_exception(logger=test_logger)
        async def successful_func() -> str:
            return "async success"

        result = await successful_func()

        assert result == "async success"
        test_logger.warning.assert_not_called()

    @pytest.mark.asyncio
    async def test_catches_http_error_and_logs_warning(self) -> None:
        """Test that httpx.HTTPError is caught and logged as warning."""
        test_logger = Mock(spec=logging.Logger)

        @async_warn_catch_exception(logger=test_logger)
        async def failing_func() -> str:
            raise httpx.HTTPError("async connection failed")

        result = await failing_func()

        assert result is None
        test_logger.warning.assert_called_once()
        assert "Ingestion error" in test_logger.warning.call_args[0][0]
        assert "failing_func" in test_logger.warning.call_args[0][0]

    @pytest.mark.asyncio
    async def test_catches_timeout_error_and_logs_warning(self) -> None:
        """Test that TimeoutError is caught and logged as warning."""
        test_logger = Mock(spec=logging.Logger)

        @async_warn_catch_exception(logger=test_logger)
        async def timeout_func() -> str:
            raise TimeoutError("async timeout")

        result = await timeout_func()

        assert result is None
        test_logger.warning.assert_called_once()

    @pytest.mark.asyncio
    async def test_does_not_catch_non_infrastructure_exceptions(self) -> None:
        """Test that non-infrastructure exceptions are re-raised."""
        test_logger = Mock(spec=logging.Logger)

        @async_warn_catch_exception(logger=test_logger)
        async def value_error_func() -> str:
            raise ValueError("async invalid value")

        with pytest.raises(ValueError) as exc_info:
            await value_error_func()

        assert "async invalid value" in str(exc_info.value)
        test_logger.warning.assert_not_called()


class TestRetryOnTransientHttpError:
    """Tests for the retry_on_transient_http_error decorator."""

    @pytest.mark.asyncio
    async def test_returns_result_on_success(self) -> None:
        """Test that the decorator returns the function result when no exception occurs."""

        @retry_on_transient_http_error
        async def successful_func() -> str:
            return "success"

        result = await successful_func()
        assert result == "success"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status_code", list(RETRYABLE_STATUS_CODES))
    async def test_reraises_retryable_status_codes(self, status_code: int) -> None:
        """Test that retryable status codes are re-raised for backoff retry."""

        @retry_on_transient_http_error
        async def retryable_func() -> str:
            raise GalileoHTTPException(
                message=f"HTTP {status_code}", status_code=status_code, response_text=f"Error {status_code}"
            )

        with pytest.raises(GalileoHTTPException) as exc_info:
            await retryable_func()

        assert exc_info.value.status_code == status_code

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status_code", [500, 502, 503, 504])
    async def test_reraises_server_errors(self, status_code: int) -> None:
        """Test that 5xx server errors are re-raised for retry."""

        @retry_on_transient_http_error
        async def server_error_func() -> str:
            raise GalileoHTTPException(
                message=f"HTTP {status_code}", status_code=status_code, response_text=f"Error {status_code}"
            )

        with pytest.raises(GalileoHTTPException) as exc_info:
            await server_error_func()

        assert exc_info.value.status_code == status_code

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status_code", [400, 401, 403, 405])
    async def test_returns_none_for_non_retryable_client_errors(self, status_code: int) -> None:
        """Test that non-retryable client errors return None."""

        @retry_on_transient_http_error
        async def client_error_func() -> str:
            raise GalileoHTTPException(
                message=f"HTTP {status_code}", status_code=status_code, response_text=f"Error {status_code}"
            )

        result = await client_error_func()
        assert result is None


class TestInfrastructureExceptions:
    """Tests for INFRASTRUCTURE_EXCEPTIONS constant."""

    def test_contains_expected_exception_types(self) -> None:
        """Test that INFRASTRUCTURE_EXCEPTIONS contains all expected types."""
        expected_types = (
            httpx.HTTPError,
            httpx.TimeoutException,
            httpx.ConnectError,
            httpx.ReadError,
            httpx.WriteError,
            ConnectionError,
            TimeoutError,
            OSError,
        )

        for exc_type in expected_types:
            assert exc_type in INFRASTRUCTURE_EXCEPTIONS


class TestRetryableStatusCodes:
    """Tests for RETRYABLE_STATUS_CODES constant."""

    def test_contains_expected_status_codes(self) -> None:
        """Test that RETRYABLE_STATUS_CODES contains expected codes."""
        expected_codes = {404, 408, 422, 429}

        assert RETRYABLE_STATUS_CODES == expected_codes

    def test_is_immutable(self) -> None:
        """Test that RETRYABLE_STATUS_CODES is a frozenset (immutable)."""
        assert isinstance(RETRYABLE_STATUS_CODES, frozenset)
