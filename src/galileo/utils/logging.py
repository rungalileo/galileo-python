import logging

from galileo.schema.trace import SPAN_TYPE


def is_textual_span_type(span_type: SPAN_TYPE) -> bool:
    """
    Check if the span type has a string-based input and output.

    Args:
        span_type: The type of span

    Returns:
        bool: True if the span type has a string-based input and output, False otherwise
    """
    return span_type in ["tool", "workflow", "agent"]


def is_concludable_span_type(span_type: SPAN_TYPE) -> bool:
    """
    Check if the span type requires conclusion (via `conclude()`).

    Args:
        span_type: The type of span

    Returns:
        bool: True if the span type requires conclusion, False otherwise
    """
    return span_type in ["workflow", "agent"]


## TODO: Move the functionality below to the proper utils file.


def _is_logger_configured(logger: logging.Logger) -> bool:
    """
    Check if a logger has been explicitly configured by the user.

    Returns True if the logger has handlers, a non-default level, or explicit propagate setting.
    """
    # Check if logger has any handlers
    if logger.handlers:
        return True

    # Check if level has been explicitly set (not using parent's level)
    if logger.level != logging.NOTSET:
        return True

    # Check if propagate has been explicitly set to False
    # (this is a heuristic - if someone set propagate=False, they likely configured logging)
    return bool(not logger.propagate and logger.parent and logger.parent.name == "root")


def _ensure_silent_by_default() -> None:
    """
    Ensure galileo loggers are silent by default, but only if they haven't been configured yet.
    This avoids interfering with existing logging configurations.
    """
    logger = logging.getLogger("galileo")

    # Only apply silent defaults if the logger hasn't been configured by the user
    if not _is_logger_configured(logger):
        # Set a high level by default to suppress all output
        logger.setLevel(logging.CRITICAL + 1)
        # Ensure no propagation to root logger
        logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with lazy initialization of silent defaults.

    This should be used by SDK modules instead of directly calling logging.getLogger()
    to ensure that silent defaults are applied if the user hasn't configured logging.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance with silent defaults applied if not already configured
    """
    # Ensure silent defaults are applied on first use
    _ensure_silent_by_default()
    return logging.getLogger(name)


def enable_console_logging(level: int = logging.INFO) -> None:
    """
    Enable console logging for interactive use.

    This function configures the root galileo logger to output to the console
    with a simple formatter. This is particularly useful for REPL, IPython,
    and Jupyter environments where users want to see SDK logs immediately.

    Args:
        level: Logging level (default: logging.INFO)

    Example:
        >>> import galileo
        >>> galileo.enable_console_logging()
        >>> # Now SDK operations will show progress and debug information
    """
    # Ensure we apply silent defaults first if logger wasn't configured
    _ensure_silent_by_default()

    logger = logging.getLogger("galileo")

    # Check if handler already exists to avoid duplicates
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s - %(name)s - %(message)s"))
        logger.addHandler(handler)

    logger.setLevel(level)
    logger.propagate = False  # Avoid duplicate logs
