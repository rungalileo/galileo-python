import logging
from functools import wraps
from typing import Any, Callable, Optional, Union

from galileo.utils.nop_logger import nop_sync
from galileo.utils.serialization import serialize_to_str
from galileo_core.exceptions.http import GalileoHTTPException
from galileo_core.schemas.logging.span import StepWithChildSpans
from galileo_core.schemas.logging.step import BaseStep

_logger = logging.getLogger(__name__)


@nop_sync
def get_last_output(node: Union[BaseStep, None]) -> Optional[str]:
    """DEPRECATED: Get the last output of a node or its child spans recursively."""
    _logger.warning("DEPRECATED: get_last_output is deprecated and will be removed in a future version.")
    if not node:
        return None

    if node.output:
        return node.output if isinstance(node.output, str) else serialize_to_str(node.output)
    if isinstance(node, StepWithChildSpans) and len(node.spans):
        return get_last_output(node.spans[-1])
    return None


def handle_galileo_http_exceptions_for_retry(func: Callable) -> Callable:
    """Decorator that catches and re-raises GalileoHTTPExceptions if the status code is 404, 408, 422, 429, or >= 500.
    Note: The decorator doesn't handle 401 (unauthorized) errors or (403) (forbidden) errors.

    This decorator will re-raise the exception so it can be handled by the
    `backoff` decorator.
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except GalileoHTTPException as e:
            if e.status_code == 404:
                _logger.info("Trace not found, retrying...")
                raise e
            if e.status_code == 408:
                _logger.info("Request timed out, retrying...")
                raise e
            if e.status_code == 422:
                _logger.info("Parent record not found, retrying...")
                raise e
            if e.status_code == 429:
                _logger.info("Rate limited, retrying...")
                raise e
            if e.status_code > 500:
                _logger.info("Server error, retrying...")
                raise e

            _logger.error(f"Unrecoverable failure or unrecognized error: {e}")

            return None

    return wrapper
