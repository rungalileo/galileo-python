from typing import Optional, Union

from galileo.utils.nop_logger import nop_sync
from galileo.utils.serialization import serialize_to_str
from galileo_core.schemas.logging.span import StepWithChildSpans
from galileo_core.schemas.logging.step import BaseStep


@nop_sync
def get_last_output(node: Union[BaseStep, None]) -> Optional[str]:
    """
    Get the last output of a node or its child spans recursively.
    """
    if not node:
        return None

    if node.output:
        return node.output if isinstance(node.output, str) else serialize_to_str(node.output)
    elif isinstance(node, StepWithChildSpans) and len(node.spans):
        return get_last_output(node.spans[-1])
    return None
