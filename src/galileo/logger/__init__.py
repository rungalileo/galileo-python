from __future__ import annotations

from typing import TYPE_CHECKING, Any

__all__ = ["GalileoLogger"]

if TYPE_CHECKING:
    from galileo.logger.logger import GalileoLogger


def __getattr__(name: str) -> Any:
    if name == "GalileoLogger":
        from galileo.logger.logger import GalileoLogger

        return GalileoLogger
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    return sorted(__all__)
