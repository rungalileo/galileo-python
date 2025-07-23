"""Galileo"""

# flake8: noqa: F401
# ruff: noqa: F401
from typing import Any, Dict
from pydantic import ValidationError
from json import dumps

import galileo_core.schemas.logging.llm
import galileo_core.schemas.logging.span


def _convert_dict_to_message(
    value: Dict[str, Any], default_role: galileo_core.schemas.logging.llm.MessageRole = galileo_core.schemas.logging.llm.MessageRole.user
) -> galileo_core.schemas.logging.llm.Message:
    """
    Converts a dict into a Message object.
    Will dump the dict to a json string if it unable to be deserialized into a Message object.

    Args:
        value (Dict[str, Any]): The dict to convert.
        default_role (Optional[MessageRole], optional): The role to use if the dict does not contain a role. Defaults to MessageRole.user.

    Returns:
        Message: The converted Message object.
    """
    print(f"Converting dict to message: {value}")
    try:
        ret = galileo_core.schemas.logging.llm.Message.model_validate(value)
        # print(f"success, returning {ret}")
        return ret
    except ValidationError as e:
        print(f"message validation error, value: {value}")
        raise e
    # try:
    #     return galileo_core.schemas.logging.llm.Message.model_validate(value)
    # except ValidationError:
    #     return galileo_core.schemas.logging.llm.Message(content=dumps(value), role=default_role)

galileo_core.schemas.logging.span.LlmSpan._convert_dict_to_message = _convert_dict_to_message


from galileo.decorator import GalileoDecorator, galileo_context, log
from galileo.logger import GalileoLogger
from galileo.schema.message import Message
from galileo.schema.metrics import GalileoScorers
from galileo_core.helpers.api_key import create_api_key, delete_api_key, list_api_keys
from galileo_core.helpers.dependencies import is_dependency_available
from galileo_core.schemas.logging.llm import MessageRole, ToolCall, ToolCallFunction
from galileo_core.schemas.logging.span import LlmSpan, RetrieverSpan, Span, StepWithChildSpans, ToolSpan, WorkflowSpan
from galileo_core.schemas.logging.step import StepType
from galileo_core.schemas.logging.trace import Trace
from galileo_core.schemas.protect.execution_status import ExecutionStatus
from galileo_core.schemas.protect.stage import StageType

__version__ = "1.10.0"
