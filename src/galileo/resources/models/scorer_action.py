from enum import Enum


class ScorerAction(str, Enum):
    AUTOTUNE_APPLY = "autotune_apply"
    DELETE = "delete"
    EXPORT = "export"
    SHARE = "share"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
