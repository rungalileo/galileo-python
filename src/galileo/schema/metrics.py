from typing import Any, Callable

from pydantic import BaseModel

from galileo_core.schemas.logging.span import Span
from galileo_core.schemas.logging.trace import Trace


class LocalScorerConfig(BaseModel):
    name: str
    func: Callable[[Trace | Span], Any]
