from enum import Enum


class TransactionLoggingMethod(str, Enum):
    API_DIRECT = "api_direct"
    JS_LANGCHAIN = "js_langchain"
    JS_LOGGER = "js_logger"
    PY_LANGCHAIN = "py_langchain"
    PY_LANGCHAIN_ASYNC = "py_langchain_async"
    PY_LOGGER = "py_logger"
    WORKFLOWS = "workflows"

    def __str__(self) -> str:
        return str(self.value)
