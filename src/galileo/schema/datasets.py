import json
from functools import cached_property
from typing import Any, Optional

from pydantic import BaseModel


class DatasetRecord(BaseModel):
    id: Optional[str] = None
    input: str
    output: Optional[str] = None
    metadata: Optional[dict[str, str]] = None

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
