from enum import Enum


class AnnotationQueueAction(str, Enum):
    DELETE = "delete"
    RECORD_ANNOTATION = "record_annotation"
    SHARE = "share"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
