import datetime
from dataclasses import dataclass
from typing import Any

# Type for OpenAI input data - can be a string, list of strings (completion prompts),
# or list of message dicts (chat messages, response API input items)
OpenAiInputType = str | list[str | dict[str, Any]]


@dataclass
class OpenAiModuleDefinition:
    module: str
    object: str
    method: str
    type: str
    sync: bool
    min_version: str | None = None


@dataclass
class OpenAiInputData:
    name: str
    metadata: dict
    start_time: datetime.datetime
    input: OpenAiInputType
    model_parameters: dict
    model: str | None
    temperature: float
    tools: list[dict] | None
