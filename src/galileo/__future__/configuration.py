import logging
import os
from pathlib import Path
from typing import Optional

from galileo.__future__.exceptions import ConfigurationError
from galileo.config import GalileoPythonConfig

logger = logging.getLogger(__name__)


class Configuration:
    """
    Single source of truth for SDK configuration.

    This class manages environment variables, supports .env file loading, and provides
    methods for setting and checking configuration values. It provides a simplified
    interface that abstracts away the complexity of the underlying configuration system.

    Examples:
        # Set API keys explicitly
        Configuration.set_galileo_api_key("A valid API key")
        Configuration.set_openai_api_key("Another valid key")

        # Attempt connection
        Configuration.connect()  # Returns nothing on success, raises on failure

        # Get current configuration values
        api_key = Configuration.get_galileo_api_key()
        console_url = Configuration.get_console_url()
    """

    _galileo_api_key: Optional[str] = None
    _openai_api_key: Optional[str] = None
    _console_url: Optional[str] = None
    _env_loaded: bool = False

    @classmethod
    def _load_env_file(cls) -> None:
        """Load environment variables from .env file if present."""
        if cls._env_loaded:
            return

        env_file = Path(".env")
        if env_file.exists():
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Only set if not already in environment
                            if key not in os.environ:
                                os.environ[key] = value
            except Exception as e:
                # Log .env file parsing errors but continue
                logger.debug(f"Failed to parse .env file: {e}")

        cls._env_loaded = True

    @classmethod
    def set_galileo_api_key(cls, api_key: str) -> None:
        """
        Set the Galileo API key for the current session.

        Args:
            api_key (str): The Galileo API key to use.

        Examples:
            Configuration.set_galileo_api_key("your-api-key-here")
        """
        cls._galileo_api_key = api_key
        os.environ["GALILEO_API_KEY"] = api_key

    @classmethod
    def set_openai_api_key(cls, api_key: str) -> None:
        """
        Set the OpenAI API key for wrapper usage.

        Args:
            api_key (str): The OpenAI API key to use.

        Examples:
            Configuration.set_openai_api_key("your-openai-api-key-here")
        """
        cls._openai_api_key = api_key
        os.environ["OPENAI_API_KEY"] = api_key

    @classmethod
    def set_console_url(cls, console_url: str) -> None:
        """
        Set the Galileo console URL.

        Args:
            console_url (str): The Galileo console URL to use.

        Examples:
            Configuration.set_console_url("https://app.galileo.ai")
            Configuration.set_console_url("http://localhost:8088")
        """
        cls._console_url = console_url
        os.environ["GALILEO_CONSOLE_URL"] = console_url

    @classmethod
    def get_galileo_api_key(cls) -> Optional[str]:
        """
        Get the current Galileo API key.

        Returns:
            Optional[str]: The Galileo API key if set, None otherwise.
        """
        cls._load_env_file()
        return cls._galileo_api_key or os.environ.get("GALILEO_API_KEY")

    @classmethod
    def get_openai_api_key(cls) -> Optional[str]:
        """
        Get the current OpenAI API key.

        Returns:
            Optional[str]: The OpenAI API key if set, None otherwise.
        """
        cls._load_env_file()
        return cls._openai_api_key or os.environ.get("OPENAI_API_KEY")

    @classmethod
    def get_console_url(cls) -> Optional[str]:
        """
        Get the current Galileo console URL.

        Returns:
            Optional[str]: The Galileo console URL if set, None otherwise.
        """
        cls._load_env_file()
        return cls._console_url or os.environ.get("GALILEO_CONSOLE_URL")

    @classmethod
    def connect(cls) -> None:
        """
        Validate the current configuration by attempting a minimal API call.

        This method attempts to initialize the underlying configuration system and
        validate connectivity. It will raise an exception if the configuration is
        invalid or if the connection fails.

        Raises:
            ValueError: If required configuration values are missing.
            Exception: If the connection to Galileo fails.

        Examples:
            try:
                Configuration.connect()
                # Connection successful - check logs for details
            except Exception as e:
                # Handle connection failure
                pass
        """
        # Load environment variables first
        cls._load_env_file()

        # Check if we have required configuration
        api_key = cls.get_galileo_api_key()
        console_url = cls.get_console_url()

        if not console_url:
            raise ConfigurationError(
                "Galileo console URL is required. Set it using Configuration.set_console_url() "
                "or the GALILEO_CONSOLE_URL environment variable."
            )

        if not api_key:
            raise ConfigurationError(
                "Galileo API key is required. Set it using Configuration.set_galileo_api_key() "
                "or the GALILEO_API_KEY environment variable."
            )

        logger.info("Configuration.connect: started")

        try:
            # Use the underlying configuration system to validate connectivity
            # This will handle authentication, API URL resolution, and validation
            GalileoPythonConfig.get()

            # The GalileoPythonConfig.get() call will automatically:
            # 1. Load environment variables
            # 2. Resolve API URL from console URL
            # 3. Authenticate with the API key
            # 4. Validate connectivity by making a test API call
            # 5. Set up the validated API client

            # If we get here without an exception, the connection is successful
            logger.info("Configuration.connect: completed")
            return

        except Exception as e:
            # Provide a more user-friendly error message
            error_msg = str(e)
            logger.error(f"Configuration.connect: failed - {error_msg}")

            if "API key" in error_msg.lower():
                raise ConfigurationError(f"Invalid API key or authentication failed: {error_msg}") from e
            if "url" in error_msg.lower() or "connection" in error_msg.lower():
                raise ConfigurationError(f"Failed to connect to Galileo: {error_msg}") from e
            raise ConfigurationError(f"Configuration validation failed: {error_msg}") from e

    @classmethod
    def reset(cls) -> None:
        """
        Reset all configuration values to their defaults.

        This method clears all set configuration values and resets the underlying
        configuration system. Useful for testing or switching between different
        Galileo instances.

        Examples:
            Configuration.reset()
        """
        cls._galileo_api_key = None
        cls._openai_api_key = None
        cls._console_url = None
        cls._env_loaded = False

        # Clear environment variables that we might have set
        for key in ["GALILEO_API_KEY", "OPENAI_API_KEY", "GALILEO_CONSOLE_URL"]:
            if key in os.environ:
                del os.environ[key]

        # Reset the underlying configuration
        try:
            # Only reset if there's an existing instance
            if GalileoPythonConfig._instance is not None:
                config = GalileoPythonConfig._instance
                config.reset()
        except Exception as e:
            # If the config doesn't exist yet, that's fine
            logger.debug(f"Failed to reset config instance: {e}")

    @classmethod
    def is_configured(cls) -> bool:
        """
        Check if the minimum required configuration is present.

        Returns:
            bool: True if both API key and console URL are configured, False otherwise.

        Examples:
            if Configuration.is_configured():
                # Configuration is ready
                pass
            else:
                # Set required configuration
                pass
        """
        cls._load_env_file()
        return bool(cls.get_galileo_api_key() and cls.get_console_url())
