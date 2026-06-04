from __future__ import annotations

from typing import TYPE_CHECKING, Any

__all__ = ["SplunkAOLogger"]

if TYPE_CHECKING:
    from galileo.logger.logger import SplunkAOLogger


def __getattr__(name: str) -> Any:
    if name == "SplunkAOLogger":
        from galileo.logger.logger import SplunkAOLogger

        return SplunkAOLogger
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(__all__)
