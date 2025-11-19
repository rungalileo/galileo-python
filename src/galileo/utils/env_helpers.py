"""Utilities for reading environment variables with defaults."""

from os import getenv
from typing import Literal, Optional

from galileo.constants import DEFAULT_LOG_STREAM_NAME, DEFAULT_MODE, DEFAULT_PROJECT_NAME
from galileo.exceptions import GalileoLoggerException


def _get_mode_or_default(mode: Optional[str]) -> Literal["batch", "distributed"]:
    """
    Validates the mode value. If the environment variable contains
    an invalid value, falls back to default.

    Parameters
    ----------
    mode : Optional[str]
        The mode value, or None to check environment variable.

    Returns
    -------
    Literal["batch", "distributed"]
        The mode value to use:
        - "batch": Batches traces and sends on flush() (default)
        - "distributed": Enables distributed tracing with immediate updates
    """
    if mode is None:
        mode = getenv("GALILEO_MODE", DEFAULT_MODE)

    if not isinstance(mode, str):
        raise GalileoLoggerException(f"Invalid mode: {mode}. Mode must be 'batch' or 'distributed'.")

    mode = mode.lower()
    if mode not in ("batch", "distributed"):
        raise GalileoLoggerException(f"Invalid mode: '{mode}'. Mode must be 'batch' or 'distributed'.")

    return mode  # type: ignore[return-value]


def _get_project_or_default(project: Optional[str]) -> str:
    """
    Get the project name, falling back to GALILEO_PROJECT env var or default.

    Parameters
    ----------
    project : Optional[str]
        The project name, or None to check environment variable.

    Returns
    -------
    str
        The project name to use.
    """
    if project is None:
        return getenv("GALILEO_PROJECT", DEFAULT_PROJECT_NAME)
    return project


def _get_log_stream_or_default(log_stream: Optional[str]) -> str:
    """
    Get the log stream name, falling back to GALILEO_LOG_STREAM env var or default.

    Parameters
    ----------
    log_stream : Optional[str]
        The log stream name, or None to check environment variable.

    Returns
    -------
    str
        The log stream name to use.
    """
    if log_stream is None:
        return getenv("GALILEO_LOG_STREAM", DEFAULT_LOG_STREAM_NAME)
    return log_stream


def _get_project_from_env() -> Optional[str]:
    """
    Get the project name from GALILEO_PROJECT environment variable.

    Returns
    -------
    Optional[str]
        The project name from environment variable, or None if not set.
    """
    return getenv("GALILEO_PROJECT")


def _get_project_id_from_env() -> Optional[str]:
    """
    Get the project ID from GALILEO_PROJECT_ID environment variable.

    Returns
    -------
    Optional[str]
        The project ID from environment variable, or None if not set.
    """
    return getenv("GALILEO_PROJECT_ID")


def _get_log_stream_from_env() -> Optional[str]:
    """
    Get the log stream name from GALILEO_LOG_STREAM environment variable.

    Returns
    -------
    Optional[str]
        The log stream name from environment variable, or None if not set.
    """
    return getenv("GALILEO_LOG_STREAM")


def _get_log_stream_id_from_env() -> Optional[str]:
    """
    Get the log stream ID from GALILEO_LOG_STREAM_ID environment variable.

    Returns
    -------
    Optional[str]
        The log stream ID from environment variable, or None if not set.
    """
    return getenv("GALILEO_LOG_STREAM_ID")
