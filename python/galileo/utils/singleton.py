import threading
from typing import Optional, Dict, Tuple

from os import getenv

from galileo.logger import GalileoLogger


class GalileoLoggerSingleton:
    _instance = None
    _lock = threading.Lock()
    _galileo_loggers: Dict[Tuple[str, str], GalileoLogger] = {}

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(GalileoLoggerSingleton, cls).__new__(cls)
                    cls._instance._galileo_loggers = {}
        return cls._instance

    def _get_key(
        self, project: Optional[str], log_stream: Optional[str]
    ) -> Tuple[str, str]:
        if project is None:
            project = getenv("GALILEO_PROJECT", None)
        if log_stream is None:
            log_stream = getenv("GALILEO_LOG_STREAM", None)

        return (project or "default", log_stream or "default")

    def get(
        self,
        *,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
    ) -> GalileoLogger:
        key = self._get_key(project, log_stream)

        if key in self._galileo_loggers:
            return self._galileo_loggers[key]

        with self._lock:
            if key in self._galileo_loggers:
                return self._galileo_loggers[key]

            galileo_client_init_args = {
                "project": project,
                "log_stream": log_stream,
            }

            logger = GalileoLogger(
                **{k: v for k, v in galileo_client_init_args.items() if v is not None}
            )

            self._galileo_loggers[key] = logger
            return logger

    def reset(
        self,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
    ) -> None:
        with self._lock:
            if project is None and log_stream is None:
                # Reset all loggers
                for logger in self._galileo_loggers.values():
                    logger.terminate()
                self._galileo_loggers.clear()
            else:
                # Reset specific logger
                key = self._get_key(project, log_stream)
                if key in self._galileo_loggers:
                    self._galileo_loggers[key].terminate()
                    del self._galileo_loggers[key]

    def get_all_loggers(self) -> Dict[Tuple[str, str], GalileoLogger]:
        """Return a dictionary of all active loggers."""
        return dict(self._galileo_loggers)
