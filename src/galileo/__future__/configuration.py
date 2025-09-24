import contextlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional

from galileo.__future__.exceptions import ConfigurationError
from galileo.config import GalileoPythonConfig
from galileo.utils.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class ConfigKey:
    """Metadata for a configuration key."""

    name: str
    env_var: str
    description: str
    required: bool = False
    sensitive: bool = False
    default: Any = None
    value_type: type = str
    parser: Optional[Callable[[str], Any]] = None


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
        name="logging_disabled",
        env_var="GALILEO_LOGGING_DISABLED",
        description="Disable all logging to Galileo",
        default=False,
        value_type=bool,
        parser=lambda v: v.lower() in ("true", "1", "t", "yes"),
    ),
]

_KEYS_BY_NAME = {key.name: key for key in _CONFIGURATION_KEYS}


class ConfigurationMeta(type):
    """
    Metaclass for dynamic attribute handling based on CONFIGURATION_KEYS.

    Reference: https://docs.python.org/3/reference/datamodel.html#customizing-attribute-access
    """

    def __getattribute__(cls, name: str) -> Any:
        """Generic getter. Returns from: explicit value → env var → .env file → default."""
        if name.startswith("_") or name in (
            "connect",
            "reset",
            "is_configured",
            "get_configuration",
            "get_key_info",
            "get_keys_by_category",
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
        """Generic setter. Stores value internally and syncs to environment variable."""
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

    Uses a data-driven approach with keys defined in CONFIGURATION_KEYS.
    Automatically syncs with environment variables and loads .env files.

    Examples:
        Configuration.galileo_api_key = "key"
        Configuration.console_url = "https://console.galileo.ai"

        if Configuration.is_configured():
            Configuration.connect()

        config = Configuration.get_configuration()
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
