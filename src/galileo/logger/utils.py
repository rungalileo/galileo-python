import logging
from typing import Optional, Union

from galileo.utils.decorators import nop_sync
from galileo.utils.serialization import serialize_to_str
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
