import datetime
from dataclasses import dataclass
from typing import Any, Optional, Union

# Type for OpenAI input data - can be a string, list of strings (completion prompts),
# or list of message dicts (chat messages, response API input items)
OpenAiInputType = Union[str, list[Union[str, dict[str, Any]]]]


@dataclass
class OpenAiModuleDefinition:
    module: str
    object: str
    method: str
    type: str
    sync: bool
    min_version: Optional[str] = None


@dataclass
class OpenAiInputData:
    name: str
    metadata: dict
    start_time: datetime.datetime
    input: OpenAiInputType
    model_parameters: dict
    model: Optional[str]
    temperature: float
    tools: Optional[list[dict]]
