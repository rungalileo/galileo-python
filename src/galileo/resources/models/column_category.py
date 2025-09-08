from enum import Enum


class ColumnCategory(str, Enum):
    DATASET = "dataset"
    DATASET_METADATA = "dataset_metadata"
    FEEDBACK = "feedback"
    METRIC = "metric"
    STANDARD = "standard"
    TAGS = "tags"
    USER_METADATA = "user_metadata"

    def __str__(self) -> str:
        return str(self.value)
