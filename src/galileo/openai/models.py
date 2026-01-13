import datetime
from dataclasses import dataclass
from typing import Optional


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
    input: str
    model_parameters: dict
    model: Optional[str]
    temperature: float
    tools: Optional[list[dict]]
