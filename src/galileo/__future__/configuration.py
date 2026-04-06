"""Deprecated: use galileo.configuration instead of galileo.__future__.configuration."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.configuration is deprecated. Use galileo.configuration instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.configuration import (  # noqa: E402
    _CONFIGURATION_KEYS,
    _KEYS_BY_NAME,
    VALID_LOG_LEVELS,
    ConfigKey,
    Configuration,
    ConfigurationMeta,
    parse_log_level,
)

__all__ = [
    "VALID_LOG_LEVELS",
    "_CONFIGURATION_KEYS",
    "_KEYS_BY_NAME",
    "ConfigKey",
    "Configuration",
    "ConfigurationMeta",
    "parse_log_level",
]
