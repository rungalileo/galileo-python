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


def _ensure_silent_by_default() -> None:
    """
    Ensure galileo loggers are silent by default by configuring the root galileo logger.
    This is called automatically when the module is imported.
    """
    logger = logging.getLogger("galileo")
    # Set a high level by default to suppress all output
    logger.setLevel(logging.CRITICAL + 1)
    # Ensure no propagation to root logger
    logger.propagate = False


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
    logger = logging.getLogger("galileo")

    # Check if handler already exists to avoid duplicates
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s - %(name)s - %(message)s"))
        logger.addHandler(handler)

    logger.setLevel(level)
    logger.propagate = False  # Avoid duplicate logs


# Initialize silent logging when module is imported
_ensure_silent_by_default()
