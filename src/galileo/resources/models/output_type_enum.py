from enum import Enum


class OutputTypeEnum(str, Enum):
    BOOLEAN = "boolean"
    BOOLEAN_MULTILABEL = "boolean_multilabel"
    CATEGORICAL = "categorical"
    COUNT = "count"
    DISCRETE = "discrete"
    FREEFORM = "freeform"
    MULTILABEL = "multilabel"
    PERCENTAGE = "percentage"
    RETRIEVED_CHUNK_LIST_BOOLEAN = "retrieved_chunk_list_boolean"

    def __str__(self) -> str:
        return str(self.value)
