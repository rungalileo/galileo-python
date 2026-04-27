from enum import Enum


class Method(str, Enum):
    GET = "GET"
    PUT = "PUT"

    def __str__(self) -> str:
        return str(self.value)
