from enum import Enum


class ComponentType(str, Enum):
    EXPERIMENTS_TABLE = "experiments_table"
    LOGSTREAM_TABLE = "logstream_table"

    def __str__(self) -> str:
        return str(self.value)
