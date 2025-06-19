import abc
from datetime import datetime
from typing import Optional

from galileo_core.schemas.logging.span import StepWithChildSpans
from galileo_core.schemas.logging.step import StepAllowedInputType
from galileo_core.schemas.logging.trace import Trace


class IGalileoLogger(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "start_trace")
            and callable(subclass.start_trace)
            and hasattr(subclass, "conclude")
            and callable(subclass.conclude)
            and hasattr(subclass, "flush")
            and callable(subclass.flush)
            and hasattr(subclass, "async_flush")
            and callable(subclass.async_flush)
            or NotImplemented
        )

    @abc.abstractmethod
    def start_trace(
        self,
        input: StepAllowedInputType,
        name: Optional[str] = None,
        duration_ns: Optional[int] = None,
        created_at: Optional[datetime] = None,
        metadata: Optional[dict[str, str]] = None,
        tags: Optional[list[str]] = None,
        dataset_input: Optional[str] = None,
        dataset_output: Optional[str] = None,
        dataset_metadata: Optional[dict[str, str]] = None,
        external_id: Optional[str] = None,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    def conclude(
        self,
        output: Optional[str] = None,
        duration_ns: Optional[int] = None,
        status_code: Optional[int] = None,
        conclude_all: bool = False,
    ) -> Optional[StepWithChildSpans]:
        raise NotImplementedError

    @abc.abstractmethod
    def flush(self) -> list[Trace]:
        raise NotImplementedError

    @abc.abstractmethod
    async def async_flush(self) -> list[Trace]:
        raise NotImplementedError
