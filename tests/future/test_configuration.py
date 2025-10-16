import logging
import os
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from galileo.__future__ import Configuration, ConfigurationError
from galileo.__future__.configuration import _CONFIGURATION_KEYS
from galileo.config import GalileoPythonConfig


class TestConfigurationProperties:
    """Test suite for Configuration properties (getter/setter) - data-driven tests."""

    def test_property_set_and_get_all_types(self, clean_env: None, reset_configuration: None) -> None:
        """Test setting and getting all properties updates internal state and env vars correctly."""
        for config_key in _CONFIGURATION_KEYS:
            # Determine test value based on type
            if config_key.value_type is bool:
                test_value = True
                expected_env_value = "true"
            else:
                test_value = f"test-{config_key.name}-value"
                expected_env_value = test_value

            # Set via property
            setattr(Configuration, config_key.name, test_value)

            # Verify property getter returns value
            actual_value = getattr(Configuration, config_key.name)
            if config_key.value_type is bool:
                assert actual_value is test_value
            else:
                assert actual_value == test_value

            # Verify environment variable is set correctly
            assert os.environ[config_key.env_var] == expected_env_value

            # Verify internal state is updated
            internal_value = getattr(Configuration, f"_{config_key.name}")
            if config_key.value_type is bool:
                assert internal_value is test_value
            else:
                assert internal_value == test_value

            # Clean up for next iteration
            Configuration.reset()

    def test_properties_read_from_environment_all_types(
        self, monkeypatch: pytest.MonkeyPatch, reset_configuration: None
    ) -> None:
        """Test that all properties read from environment variables when internal state is not set."""
        for config_key in _CONFIGURATION_KEYS:
            # Determine test value based on type
            if config_key.value_type is bool:
                env_value = "true"
                expected_value = True
            else:
                env_value = f"env-{config_key.name}"
                expected_value = env_value

            # Set environment variable
            monkeypatch.setenv(config_key.env_var, env_value)

            # Access property (should read from env)
            value = getattr(Configuration, config_key.name)

            # Verify it returns the parsed environment variable value
            if config_key.value_type is bool:
                assert value is expected_value
            else:
                assert value == expected_value

            # Clean up for next iteration
            Configuration.reset()

    def test_property_precedence_internal_over_env(
        self, monkeypatch: pytest.MonkeyPatch, reset_configuration: None
    ) -> None:
        """Test that internal state takes precedence over environment variables for all keys."""
        # Test with a few representative keys
        test_cases = [
            ("galileo_api_key", "env-key", "internal-key"),
            ("console_url", "https://env.galileo.ai", "https://internal.galileo.ai"),
            ("default_project_name", "env-project", "internal-project"),
        ]

        for key_name, env_value, internal_value in test_cases:
            config_key = next(k for k in _CONFIGURATION_KEYS if k.name == key_name)
            monkeypatch.setenv(config_key.env_var, env_value)
            setattr(Configuration, key_name, internal_value)
            assert getattr(Configuration, key_name) == internal_value


class TestConfigurationEnvFileLoading:
    """Test suite for .env file loading functionality."""

    def test_env_file_loading_sets_environment_variables(
        self, mock_env_file: Path, clean_env: None, reset_configuration: None
    ) -> None:
        """Test that .env file is loaded and environment variables are set correctly."""
        # Create .env file with test values
        mock_env_file.write_text(
            'GALILEO_API_KEY="env-file-key"\n'
            'GALILEO_CONSOLE_URL="https://envfile.galileo.ai"\n'
            'OPENAI_API_KEY="env-file-openai"\n'
        )

        # Access property to trigger env file loading
        api_key = Configuration.galileo_api_key

        # Verify env file was loaded
        assert api_key == "env-file-key"
        assert Configuration.console_url == "https://envfile.galileo.ai"
        assert Configuration.openai_api_key == "env-file-openai"

    def test_env_file_does_not_override_existing_env_vars(
        self, mock_env_file: Path, monkeypatch: pytest.MonkeyPatch, reset_configuration: None
    ) -> None:
        """Test that .env file does not override existing environment variables."""
        # Set existing environment variable
        monkeypatch.setenv("GALILEO_API_KEY", "existing-env-key")

        # Create .env file with different value
        mock_env_file.write_text('GALILEO_API_KEY="env-file-key"\n')

        # Access property to trigger env file loading
        api_key = Configuration.galileo_api_key

        # Verify existing env var is preserved
        assert api_key == "existing-env-key"

    def test_env_file_handles_comments_and_empty_lines(
        self, mock_env_file: Path, clean_env: None, reset_configuration: None
    ) -> None:
        """Test that .env file parser handles comments, empty lines, and various formats."""
        mock_env_file.write_text(
            "# This is a comment\n"
            "\n"
            "GALILEO_API_KEY=key-without-quotes\n"
            'GALILEO_CONSOLE_URL="url-with-double-quotes"\n'
            "OPENAI_API_KEY='key-with-single-quotes'\n"
            "  \n"
            "# Another comment\n"
        )

        # Trigger loading
        _ = Configuration.galileo_api_key

        # Verify all values are loaded correctly
        assert Configuration.galileo_api_key == "key-without-quotes"
        assert Configuration.console_url == "url-with-double-quotes"
        assert Configuration.openai_api_key == "key-with-single-quotes"

    def test_env_file_loading_is_idempotent(
        self, mock_env_file: Path, clean_env: None, reset_configuration: None
    ) -> None:
        """Test that env file is only loaded once even with multiple property accesses."""
        mock_env_file.write_text('GALILEO_API_KEY="test-key"\n')

        # Access multiple times
        _ = Configuration.galileo_api_key
        _ = Configuration.console_url
        _ = Configuration.openai_api_key

        # Verify env file was only loaded once
        assert Configuration._env_loaded is True

    def test_malformed_env_file_does_not_crash(
        self,
        mock_env_file: Path,
        clean_env: None,
        reset_configuration: None,
        capture_logs: tuple[logging.Logger, StringIO],
    ) -> None:
        """Test that malformed .env file logs error but doesn't crash the application."""
        _, log_stream = capture_logs

        # Create malformed env file (will cause parsing to fail)
        mock_env_file.write_text("INVALID_LINE_WITHOUT_EQUALS\n")

        # This should not raise an exception
        api_key = Configuration.galileo_api_key

        # Verify operation continues (returns None since no valid config)
        assert api_key is None


class TestConfigurationConnect:
    """Test suite for Configuration.connect() method."""

    def test_connect_succeeds_with_valid_configuration(
        self,
        mock_api_endpoints: MagicMock,
        monkeypatch: pytest.MonkeyPatch,
        reset_configuration: None,
        capture_logs: tuple[logging.Logger, StringIO],
    ) -> None:
        """Test successful connection with valid API key and console URL logs appropriately."""
        _, log_stream = capture_logs

        # Set valid configuration
        monkeypatch.setenv("GALILEO_API_KEY", "valid-key")
        monkeypatch.setenv("GALILEO_CONSOLE_URL", "https://app.galileo.ai")

        # Connect should succeed without raising
        Configuration.connect()

        # Verify logging occurred (no print statements)
        logs = log_stream.getvalue()
        assert "Validating Galileo configuration" in logs
        assert "Successfully connected to Galileo" in logs

    def test_connect_fails_without_console_url(
        self, monkeypatch: pytest.MonkeyPatch, reset_configuration: None, capture_logs: tuple[logging.Logger, StringIO]
    ) -> None:
        """Test connect() raises ConfigurationError when console URL is missing."""
        _, log_stream = capture_logs

        # Set only API key
        monkeypatch.setenv("GALILEO_API_KEY", "valid-key")

        # Should raise ConfigurationError
        with pytest.raises(ConfigurationError) as exc_info:
            Configuration.connect()

        # Verify error message provides helpful guidance
        assert "console url is required" in str(exc_info.value).lower()
        assert "configuration.console_url" in str(exc_info.value).lower()

        # Note: Early validation failures don't produce logs since they occur
        # before the logger.info call in connect()

    def test_connect_fails_without_api_key(
        self, monkeypatch: pytest.MonkeyPatch, reset_configuration: None, capture_logs: tuple[logging.Logger, StringIO]
    ) -> None:
        """Test connect() raises ConfigurationError when API key is missing."""
        _, log_stream = capture_logs

        # Set only console URL
        monkeypatch.setenv("GALILEO_CONSOLE_URL", "https://app.galileo.ai")

        # Should raise ConfigurationError
        with pytest.raises(ConfigurationError) as exc_info:
            Configuration.connect()

        # Verify error message provides helpful guidance
        assert "api key is required" in str(exc_info.value).lower()
        assert "Configuration.galileo_api_key" in str(exc_info.value)

    @pytest.mark.parametrize(
        "error_type,error_message,expected_in_error",
        [
            ("api_key", "Invalid API key provided", "Authentication failed"),
            ("url", "Connection refused", "Connection failed"),
            ("connection", "Connection timeout occurred", "Connection failed"),
            ("generic", "Unknown error", "Configuration validation failed"),
        ],
    )
    @patch("galileo.__future__.configuration.GalileoPythonConfig.get")
    def test_connect_handles_different_error_types(
        self,
        mock_config_get: Mock,
        error_type: str,
        error_message: str,
        expected_in_error: str,
        monkeypatch: pytest.MonkeyPatch,
        reset_configuration: None,
        capture_logs: tuple[logging.Logger, StringIO],
    ) -> None:
        """Test connect() properly wraps and reports different types of connection errors."""
        _, log_stream = capture_logs

        # Set valid configuration
        monkeypatch.setenv("GALILEO_API_KEY", "valid-key")
        monkeypatch.setenv("GALILEO_CONSOLE_URL", "https://app.galileo.ai")

        # Mock GalileoPythonConfig.get to raise appropriate error
        mock_config_get.side_effect = Exception(error_message)

        with pytest.raises(ConfigurationError) as exc_info:
            Configuration.connect()

        # Verify error is wrapped appropriately
        assert expected_in_error.lower() in str(exc_info.value).lower()

        # Verify error is logged
        logs = log_stream.getvalue()
        assert "Failed to connect to Galileo" in logs


class TestConfigurationReset:
    """Test suite for Configuration.reset() method - data-driven tests."""

    def test_reset_clears_all_state_and_env_vars(self, clean_env: None, reset_configuration: None) -> None:
        """Test reset() clears all internal configuration state and environment variables."""
        # Set all configuration keys
        for key in _CONFIGURATION_KEYS:
            if key.value_type is str:
                setattr(Configuration, key.name, f"test-{key.name}")
            elif key.value_type is bool:
                setattr(Configuration, key.name, True)

        # Verify state is set for all keys
        for key in _CONFIGURATION_KEYS:
            internal_attr = f"_{key.name}"
            assert hasattr(Configuration, internal_attr)
            assert getattr(Configuration, internal_attr) is not None
            assert key.env_var in os.environ

        # Reset
        Configuration.reset()

        # Verify _env_loaded is reset
        assert Configuration._env_loaded is False

        # Verify all internal state and environment variables are cleared
        for key in _CONFIGURATION_KEYS:
            value = getattr(Configuration, key.name)
            # Value should be None or default
            assert value in (None, key.default)
            # Environment variable should be cleared
            assert key.env_var not in os.environ

    def test_reset_handles_missing_config_instance_gracefully(self, reset_configuration: None) -> None:
        """Test reset() handles case when GalileoPythonConfig instance doesn't exist."""
        GalileoPythonConfig._instance = None
        Configuration.reset()

        # Verify all keys are reset
        for key in _CONFIGURATION_KEYS:
            value = getattr(Configuration, key.name)
            assert value in (None, key.default)


class TestConfigurationIsConfigured:
    """Test suite for Configuration.is_configured() method - data-driven tests."""

    def test_is_configured_with_all_required_keys(self, clean_env: None, reset_configuration: None) -> None:
        """Test is_configured() returns True when all required keys are set."""
        # Set all required keys dynamically
        for key in _CONFIGURATION_KEYS:
            if key.required:
                setattr(Configuration, key.name, f"test-{key.name}")

        assert Configuration.is_configured() is True

    def test_is_configured_missing_any_required_key(self, clean_env: None, reset_configuration: None) -> None:
        """Test is_configured() returns False when any required key is missing."""
        required_keys = [k for k in _CONFIGURATION_KEYS if k.required]

        # Test missing each required key individually
        for missing_key in required_keys:
            Configuration.reset()

            # Set all required keys except one
            for key in required_keys:
                if key.name != missing_key.name:
                    setattr(Configuration, key.name, f"test-{key.name}")

            # Should return False because one required key is missing
            assert Configuration.is_configured() is False

    def test_is_configured_with_no_keys_set(self, clean_env: None, reset_configuration: None) -> None:
        """Test is_configured() returns False when no keys are set."""
        assert Configuration.is_configured() is False


class TestConfigurationGetConfiguration:
    """Test suite for Configuration.get_configuration() method - data-driven tests."""

    def test_get_configuration_returns_all_keys(self, clean_env: None, reset_configuration: None) -> None:
        """Test get_configuration() returns all keys from CONFIGURATION_KEYS."""
        # Set a few values
        Configuration.galileo_api_key = "test-key"
        Configuration.console_url = "https://test.galileo.ai"

        config = Configuration.get_configuration()

        # Verify all keys from CONFIGURATION_KEYS are in the result
        for key in _CONFIGURATION_KEYS:
            assert key.name in config

        # Verify status keys
        assert "is_configured" in config
        assert "env_file_loaded" in config

    def test_get_configuration_masks_sensitive_values(self, clean_env: None, reset_configuration: None) -> None:
        """Test get_configuration() masks sensitive values."""
        # Set values for all sensitive keys
        for key in _CONFIGURATION_KEYS:
            if key.sensitive:
                setattr(Configuration, key.name, f"secret-{key.name}")

        config = Configuration.get_configuration()

        # Verify sensitive values are masked
        for key in _CONFIGURATION_KEYS:
            if key.sensitive:
                assert config[key.name] == "***"

    def test_get_configuration_shows_not_set_for_missing_values(
        self, clean_env: None, reset_configuration: None
    ) -> None:
        """Test get_configuration() shows 'Not set' for missing values."""
        config = Configuration.get_configuration()

        # All non-default keys should show "Not set"
        for key in _CONFIGURATION_KEYS:
            if key.default is None:
                assert config[key.name] == "Not set"


class TestConfigurationIntegration:
    """Integration tests for Configuration with full workflow - data-driven tests."""

    def test_complete_configuration_workflow(
        self,
        clean_env: None,
        reset_configuration: None,
        mock_api_endpoints: MagicMock,
        capture_logs: tuple[logging.Logger, StringIO],
    ) -> None:
        """Test complete configuration workflow from setup to connection."""
        _, log_stream = capture_logs

        # Start with unconfigured state
        assert not Configuration.is_configured()

        # Set all required keys dynamically
        for key in _CONFIGURATION_KEYS:
            if key.required:
                setattr(Configuration, key.name, f"test-{key.name}")

        # Set some optional keys
        Configuration.openai_api_key = "test-openai-key"
        Configuration.default_project_name = "my-project"

        # Verify configuration
        assert Configuration.is_configured()

        # Connect
        Configuration.connect()

        # Verify all configuration values are accessible
        config = Configuration.get_configuration()
        for key in _CONFIGURATION_KEYS:
            assert key.name in config
        assert config["is_configured"] is True

        # Verify logging was used throughout
        logs = log_stream.getvalue()
        assert "Validating Galileo configuration" in logs
        assert "Successfully connected to Galileo" in logs

    def test_configuration_with_env_file_workflow(
        self, mock_env_file: Path, clean_env: None, reset_configuration: None, mock_api_endpoints: MagicMock
    ) -> None:
        """Test configuration workflow using .env file."""
        # Create .env file with all required keys
        env_lines = []
        for key in _CONFIGURATION_KEYS:
            if key.required:
                env_lines.append(f'{key.env_var}="test-{key.name}"')

        mock_env_file.write_text("\n".join(env_lines))

        # Configuration should be available from env file
        assert Configuration.is_configured()

        # Connect should work
        Configuration.connect()

        # Verify values came from env file
        for key in _CONFIGURATION_KEYS:
            if key.required:
                value = getattr(Configuration, key.name)
                assert value == f"test-{key.name}"
