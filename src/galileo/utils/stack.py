import inspect
import logging
from typing import Optional

from galileo_core.schemas.logging.code import LoggedStack, LoggedStackFrame

from sentry_sdk.utils import serialize_frame

_logger = logging.getLogger(__name__)


def get_stack_trace() -> Optional[LoggedStack]:
    """
    Get the stack trace for the current function.
    """
    _logger.info("Getting stack trace")
    frames = []
    for frame_info in inspect.stack():
        if any(
            subs in frame_info.filename
            for subs in ("galileo-python/src/galileo/", "galileo/src/galileo")
        ):
            continue
        try:
            serialized = serialize_frame(frame_info.frame)
            _logger.info(f"Stack frame: {serialized}")
            frames.append(LoggedStackFrame.model_validate(serialized))
            _logger.info("Stack frame added")
        except Exception as e:
            _logger.error(f"Error while serializing stack frame: {e}", exc_info=True)
            continue
    return LoggedStack(frames=frames)


