import json
from functools import cached_property
from typing import Any, Optional

from pydantic import BaseModel, field_validator


class DatasetRecord(BaseModel):
    id: Optional[str] = None
    input: str
    output: Optional[str] = None
    metadata: Optional[dict[str, str]] = None

    @field_validator("input", mode="before")
    @classmethod
    def validate_input(cls, value: Any) -> str:
        if not isinstance(value, str):
            value = json.dumps(value)
        return value

    @field_validator("output", mode="before")
    @classmethod
    def validate_output(cls, value: Any) -> Optional[str]:
        if value is None:
            return None
        if not isinstance(value, str):
            value = json.dumps(value)
        return value

    @field_validator("metadata", mode="before")
    @classmethod
    def validate_metadata(cls, value: Any) -> Optional[dict[str, str]]:
        if value is None:
            return None
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.decoder.JSONDecodeError:
                value = {"metadata": value}
        if not isinstance(value, dict):
            raise ValueError("Dataset metadata field must be either a string or dictionary")
        for key, v in value.items():
            if not isinstance(v, str):
                raise ValueError("Dataset metadata field dictionary values must be strings")
        return value

    @cached_property
    def deserialized_input(self) -> Any:
        try:
            return json.loads(self.input)
        except json.decoder.JSONDecodeError:
            return self.input

    @cached_property
    def deserialized_output(self) -> Optional[Any]:
        if self.output is None:
            return None
        try:
            return json.loads(self.output)
        except json.decoder.JSONDecodeError:
            return self.output
