from enum import Enum


class WebhookStatus(str, Enum):
    ACTIVE = "active"
    FAILED = "failed"
    PAUSED = "paused"
    UNTESTED = "untested"

    def __str__(self) -> str:
        return str(self.value)
