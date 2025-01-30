import threading
from typing import Optional

from galileo.logger import GalileoLogger


class GalileoLoggerSingleton:
    _instance = None
    _lock = threading.Lock()
    _galileo_logger: Optional[GalileoLogger] = None

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(GalileoLoggerSingleton, cls).__new__(cls)
        return cls._instance

    def get(
        self,
        *,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
    ) -> GalileoLogger:
        if self._galileo_logger:
            return self._galileo_logger

        with self._lock:
            if self._galileo_logger:
                return self._galileo_logger

            galileo_client_init_args = {
                "project": project,
                "log_stream": log_stream,
            }

            self._galileo_logger = GalileoLogger(
                **{k: v for k, v in galileo_client_init_args.items() if v is not None}
            )

            return self._galileo_logger

    def reset(self) -> None:
        with self._lock:
            if self._galileo_logger:
                self._galileo_logger.terminate()

            self._galileo_logger = None
