import contextlib
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional

from galileo.__future__.shared.exceptions import ConfigurationError
from galileo.config import GalileoPythonConfig
from galileo.utils.log_config import enable_console_logging as _enable_console_logging
from galileo.utils.log_config import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class ConfigKey:
    """
    Metadata for a configuration key.

    Defines a single configuration option with its properties, validation rules,
    and relationship to environment variables. Used by the ConfigurationMeta
    metaclass to enable dynamic attribute access.

    Attributes
    ----------
    name : str
        The attribute name used in the Configuration class (e.g., "galileo_api_key").
    env_var : str
        The corresponding environment variable name (e.g., "GALILEO_API_KEY").
    description : str
        Human-readable description of the configuration key's purpose.
    required : bool
        Whether this key must be set for the configuration to be considered complete.
        Default: False.
    sensitive : bool
        Whether this key contains sensitive information (e.g., API keys, passwords).
        Sensitive values are masked in get_configuration() output. Default: False.
    default : Any
        The default value if no explicit value or environment variable is set.
        Default: None.
    value_type : type
        The expected Python type for this configuration value. Default: str.
    parser : Optional[Callable[[str], Any]]
        Optional function to convert string values from environment variables
        to the appropriate type. Default: None (no conversion).
    """

    name: str
    env_var: str
    description: str
    required: bool = False
    sensitive: bool = False
    default: Any = None
    value_type: type = str
    parser: Optional[Callable[[str], Any]] = None


VALID_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})


def parse_log_level(value: str) -> str:
    """Parse and validate a log level string; returns uppercase level name."""
    level = value.upper()
    if level not in VALID_LOG_LEVELS:
        raise ValueError(f"Invalid log level '{value}'. Must be one of: {', '.join(sorted(VALID_LOG_LEVELS))}")
    return level


_CONFIGURATION_KEYS = [
    ConfigKey(
        name="galileo_api_key",
        env_var="GALILEO_API_KEY",
        description="API key for authenticating with Galileo",
        required=True,
        sensitive=True,
    ),
    ConfigKey(
        name="console_url", env_var="GALILEO_CONSOLE_URL", description="URL of the Galileo console", required=True
    ),
    ConfigKey(
        name="openai_api_key",
        env_var="OPENAI_API_KEY",
        description="OpenAI API key for interoperability with OpenAI SDK",
        sensitive=True,
    ),
    ConfigKey(name="default_project_name", env_var="GALILEO_PROJECT", description="Default project name"),
    ConfigKey(name="default_project_id", env_var="GALILEO_PROJECT_ID", description="Default project ID"),
    ConfigKey(name="default_logstream_name", env_var="GALILEO_LOG_STREAM", description="Default log stream name"),
    ConfigKey(name="default_logstream_id", env_var="GALILEO_LOG_STREAM_ID", description="Default log stream ID"),
    ConfigKey(
        name="default_scorer_model",
        env_var="GALILEO_DEFAULT_SCORER_MODEL",
        description="Default model for LLM-based scorers/metrics",
        default="gpt-4.1-mini",
    ),
    ConfigKey(
        name="default_scorer_judges",
        env_var="GALILEO_DEFAULT_SCORER_JUDGES",
        description="Default number of judges for LLM-based scorers/metrics",
        default=3,
        value_type=int,
        parser=int,
    ),
    ConfigKey(
        name="logging_disabled",
        env_var="GALILEO_LOGGING_DISABLED",
        description="Disable all telemetry logging to Galileo",
        default=False,
        value_type=bool,
        parser=lambda v: v.lower() in ("true", "1", "t", "yes"),
    ),
    ConfigKey(
        name="log_level",
        env_var="GALILEO_LOG_LEVEL",
        description="Python logging level for SDK output (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
        default=None,
        value_type=str,
        parser=parse_log_level,
    ),
    ConfigKey(
        name="code_validation_timeout",
        env_var="GALILEO_CODE_VALIDATION_TIMEOUT",
        description="Timeout in seconds for code scorer validation",
        default=60.0,
        value_type=float,
        parser=float,
    ),
    ConfigKey(
        name="code_validation_initial_delay",
        env_var="GALILEO_CODE_VALIDATION_INITIAL_DELAY",
        description="Initial delay in seconds between validation polling attempts",
        default=5.0,
        value_type=float,
        parser=float,
    ),
    ConfigKey(
        name="code_validation_max_delay",
        env_var="GALILEO_CODE_VALIDATION_MAX_DELAY",
        description="Maximum delay in seconds between validation polling attempts",
        default=30.0,
        value_type=float,
        parser=float,
    ),
    ConfigKey(
        name="code_validation_backoff_multiplier",
        env_var="GALILEO_CODE_VALIDATION_BACKOFF_MULTIPLIER",
        description="Multiplier for exponential backoff between validation polling attempts",
        default=1.5,
        value_type=float,
        parser=float,
    ),
]

_KEYS_BY_NAME = {key.name: key for key in _CONFIGURATION_KEYS}


class ConfigurationMeta(type):
    """
    Metaclass for dynamic attribute handling based on CONFIGURATION_KEYS.

    This metaclass enables the Configuration class to provide dynamic attribute access
    with automatic resolution from multiple sources. When accessing a configuration
    attribute (e.g., `Configuration.galileo_api_key`), the metaclass:

    1. Checks if the attribute is in _CONFIGURATION_KEYS
    2. Resolves the value from: explicit value → environment variable → .env file → default
    3. Applies type conversion and validation if a parser is defined
    4. Returns the resolved value

    When setting a configuration attribute (e.g., `Configuration.galileo_api_key = "key"`),
    the metaclass:

    1. Stores the value internally (with underscore prefix: `_galileo_api_key`)
    2. Automatically updates the corresponding environment variable
    3. Ensures compatibility with libraries that read from os.environ

    This pattern provides:
    - Extensibility: New configuration keys can be added to _CONFIGURATION_KEYS
    - Consistency: All configuration uses the same resolution pattern
    - Compatibility: Environment variables are kept in sync for third-party libraries
    - Transparency: Configuration sources are clearly prioritized

    Reference: https://docs.python.org/3/reference/datamodel.html#customizing-attribute-access
    """

    def __getattribute__(cls, name: str) -> Any:
        """
        Get configuration attribute value with automatic source resolution.

        Resolution order: explicit value → env var → .env file → default.

        Args:
            name: The attribute name to retrieve.

        Returns
        -------
            The resolved configuration value, or the attribute itself if not a config key.
        """
        if name.startswith("_") or name in (
            "connect",
            "reset",
            "is_configured",
            "get_configuration",
            "get_key_info",
            "get_keys_by_category",
            "enable_console_logging",
            "disable_console_logging",
        ):
            return super().__getattribute__(name)

        if name in _KEYS_BY_NAME:
            key = _KEYS_BY_NAME[name]
            super().__getattribute__("_load_env_file")()
            internal_name = f"_{name}"

            try:
                explicit_value = super().__getattribute__(internal_name)
                if explicit_value is not None:
                    return explicit_value
            except AttributeError:
                pass

            env_value = os.environ.get(key.env_var)
            if env_value is not None:
                if key.parser:
                    return key.parser(env_value)
                return env_value

            return key.default

        return super().__getattribute__(name)

    def __setattr__(cls, name: str, value: Any) -> None:
        """
        Set configuration attribute and sync to environment variable.

        When setting a configuration key, the value is:
        1. Stored internally with underscore prefix (e.g., `_galileo_api_key`)
        2. Synced to the corresponding environment variable (e.g., `GALILEO_API_KEY`)

        This ensures that both the Configuration class and environment variables
        remain consistent, maintaining compatibility with third-party libraries.

        Args:
            name: The attribute name to set.
            value: The value to assign to the attribute.
        """
        if name in _KEYS_BY_NAME:
            key = _KEYS_BY_NAME[name]
            internal_name = f"_{name}"
            super().__setattr__(internal_name, value)

            if value is not None:
                if key.value_type is bool:
                    os.environ[key.env_var] = str(value).lower()
                else:
                    os.environ[key.env_var] = str(value)
        else:
            super().__setattr__(name, value)


class Configuration(metaclass=ConfigurationMeta):
    """
    Single source of truth for SDK configuration.

    This class uses a metaclass pattern to provide dynamic attribute access to configuration
    keys defined in _CONFIGURATION_KEYS. Each configuration key can be accessed as a class
    attribute, with values resolved in the following priority order:

    1. Explicitly set value (via `Configuration.key = value`)
    2. Environment variable (e.g., GALILEO_API_KEY)
    3. .env file (loaded automatically on first access)
    4. Default value (defined in the key configuration)

    The metaclass automatically:
    - Syncs attribute assignments to environment variables
    - Loads .env files on first configuration access
    - Provides type conversion and validation via parsers

    Attributes
    ----------
    Configuration attributes are dynamically provided based on _CONFIGURATION_KEYS:
        galileo_api_key (str): API key for Galileo authentication (sensitive)
        console_url (str): URL of the Galileo console
        openai_api_key (str): OpenAI API key for SDK interoperability (sensitive)
        default_project_name (str): Default project name
        default_project_id (str): Default project ID
        default_logstream_name (str): Default log stream name
        default_logstream_id (str): Default log stream ID
        logging_disabled (bool): Disable all telemetry logging to Galileo
        log_level (str): Python logging level for SDK console output

    Examples
    --------
    Reading configuration values:
    ```python
    # Access via class attribute (reads from env vars, .env, or defaults)
    api_key = Configuration.galileo_api_key
    url = Configuration.console_url
    ```

    Setting configuration values:
    ```python
    # Set explicitly (also updates environment variables)
    Configuration.galileo_api_key = "your-api-key"
    Configuration.console_url = "https://console.galileo.ai"
    ```

    Checking and connecting:
    ```python
    # Check if required configuration is present
    if Configuration.is_configured():
        Configuration.connect()
    ```

    Getting all configuration:
    ```python
    # Get all configuration values (sensitive values are masked)
    config = Configuration.get_configuration()
    print(config["galileo_api_key"])  # Output: "***"
    print(config["console_url"])       # Output: actual URL
    ```

    Resetting configuration:
    ```python
    # Clear all configuration values and environment variables
    Configuration.reset()
    ```

    Configuring console logging:
    ```python
    # Enable console logging for debugging
    Configuration.enable_console_logging()  # INFO level by default
    Configuration.enable_console_logging("DEBUG")  # Verbose output

    # Disable console logging
    Configuration.disable_console_logging()
    ```

    Notes
    -----
    - The Configuration class should not be instantiated; use it as a static class
    - Direct attribute access (e.g., `Configuration.galileo_api_key`) is the recommended pattern
    - The `get_configuration()` method masks sensitive values for safe display/logging
    - Setting an attribute automatically updates the corresponding environment variable
    - This design maintains compatibility with third-party libraries expecting env vars
    """

    _env_loaded: bool = False

    @classmethod
    def _load_env_file(cls) -> None:
        """Load .env file if present. Called automatically on first access."""
        if cls._env_loaded:
            return

        env_file = Path(".env")
        if env_file.exists():
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            if key not in os.environ:
                                os.environ[key] = value
            except Exception as e:
                logger.debug(f"Failed to parse .env file: {e}")

        cls._env_loaded = True

    @classmethod
    def connect(cls) -> None:
        """Validate configuration and connect to Galileo."""
        cls._load_env_file()

        if not cls.console_url:
            raise ConfigurationError(
                "Galileo console URL is required. Set Configuration.console_url or GALILEO_CONSOLE_URL."
            )

        if not cls.galileo_api_key:
            raise ConfigurationError(
                "Galileo API key is required. Set Configuration.galileo_api_key or GALILEO_API_KEY."
            )

        logger.info("Validating Galileo configuration and connectivity...")

        try:
            GalileoPythonConfig.get()
            logger.info("Successfully connected to Galileo")
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to connect to Galileo: {error_msg}")

            error_lower = error_msg.lower()
            if ("api" in error_lower and "key" in error_lower) or "auth" in error_lower:
                raise ConfigurationError(f"Authentication failed: {error_msg}") from e
            if "url" in error_lower or "connection" in error_lower:
                raise ConfigurationError(f"Connection failed: {error_msg}") from e
            raise ConfigurationError(f"Configuration validation failed: {error_msg}") from e

    @classmethod
    def reset(cls) -> None:
        """Reset all configuration values and clear environment variables."""
        for key in _CONFIGURATION_KEYS:
            with contextlib.suppress(AttributeError):
                delattr(cls, f"_{key.name}")
            if key.env_var in os.environ:
                del os.environ[key.env_var]

        cls._env_loaded = False

        try:
            if GalileoPythonConfig._instance is not None:
                GalileoPythonConfig._instance.reset()
        except Exception as e:
            logger.debug(f"Could not reset GalileoPythonConfig instance: {e}")

    @classmethod
    def is_configured(cls) -> bool:
        """Check if all required configuration keys are set."""
        cls._load_env_file()
        return all(getattr(cls, key.name) for key in _CONFIGURATION_KEYS if key.required)

    @classmethod
    def get_configuration(cls) -> dict[str, Any]:
        """Get all configuration values (sensitive values are masked)."""
        cls._load_env_file()
        result: dict[str, Any] = {}

        for key in _CONFIGURATION_KEYS:
            value = getattr(cls, key.name)
            if key.sensitive and value:
                result[key.name] = "***"
            elif value is None:
                result[key.name] = "Not set"
            else:
                result[key.name] = value

        result["is_configured"] = cls.is_configured()
        result["env_file_loaded"] = cls._env_loaded
        return result

    @classmethod
    def enable_console_logging(cls, level: Optional[str] = None) -> None:
        """
        Enable console logging for SDK output.

        This is useful for debugging and interactive use (REPL, Jupyter, etc.)
        to see SDK progress and diagnostic information.

        Parameters
        ----------
        level : Optional[str]
            Logging level as string: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL".
            If not provided, uses Configuration.log_level or defaults to "INFO".

        Examples
        --------
        ```python
        # Enable with default INFO level
        Configuration.enable_console_logging()

        # Enable with DEBUG level for verbose output
        Configuration.enable_console_logging("DEBUG")

        # Or set via configuration and enable
        Configuration.log_level = "DEBUG"
        Configuration.enable_console_logging()
        ```
        """
        # Resolve level from parameter, config, or default
        level_str = level or cls.log_level or "INFO"
        level_int = getattr(logging, level_str.upper(), logging.INFO)

        _enable_console_logging(level=level_int)

        # Store the level in configuration for consistency
        cls.log_level = level_str.upper()

    @classmethod
    def disable_console_logging(cls) -> None:
        """
        Disable console logging for SDK output.

        This restores the SDK to its default silent behavior where no
        log messages are printed to the console.

        Examples
        --------
        ```python
        Configuration.disable_console_logging()
        ```
        """
        galileo_logger = logging.getLogger("galileo")

        # Remove all stream handlers
        for handler in galileo_logger.handlers[:]:
            if isinstance(handler, logging.StreamHandler):
                galileo_logger.removeHandler(handler)

        # Set level to suppress all output
        galileo_logger.setLevel(logging.CRITICAL + 1)
        galileo_logger.propagate = False

        # Clear the stored log level
        cls.log_level = None
