from enum import Enum


class LLMExportFormat(str, Enum):
    CSV = "csv"
    JSONL = "jsonl"
    JSONL_FLAT = "jsonl_flat"

    def __str__(self) -> str:
        return str(self.value)
