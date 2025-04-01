import logging
import threading
from os import getenv
from typing import Optional

from galileo.constants import DEFAULT_LOG_STREAM_NAME, DEFAULT_PROJECT_NAME
from galileo.logger import GalileoLogger

_logger = logging.getLogger(__name__)


class GalileoLoggerSingleton:
    """
    A singleton class that manages a collection of GalileoLogger instances.

    This class ensures that only one instance exists across the application and
    provides a thread-safe way to retrieve or create GalileoLogger clients based on
    the given 'project' and 'log_stream' parameters. If the parameters are not provided,
    the class attempts to read the values from the environment variables
    GALILEO_PROJECT and GALILEO_LOG_STREAM. The loggers are stored in a dictionary
    using a tuple (project, log_stream) as the key.
    """

    _instance = None  # Class-level attribute to hold the singleton instance.
    _lock = threading.Lock()  # Lock for thread-safe instantiation and operations.
    _galileo_loggers: dict[tuple[str, str], GalileoLogger] = {}  # Cache for loggers.

    def __new__(cls) -> "GalileoLoggerSingleton":
        """
        Override __new__ to ensure only one instance of GalileoLoggerSingleton is created.

        Returns:
            GalileoLoggerSingleton: The singleton instance.
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:  # Double-checked locking.
                    cls._instance = super().__new__(cls)
                    # Initialize the logger dictionary in the new instance.
                    cls._instance._galileo_loggers = {}
        return cls._instance

    @staticmethod
    def _get_key(
        project: Optional[str], log_stream: Optional[str], experiment_id: Optional[str] = None
    ) -> tuple[str, str]:
        """
        Generate a key tuple based on project and log_stream parameters.

        If project or log_stream are None, the method attempts to retrieve them
        from environment variables (GALILEO_PROJECT and GALILEO_LOG_STREAM). If still
        None, defaults to "default".

        Args:
            project (Optional[str]): The project name.
            log_stream (Optional[str]): The log stream name.
            experiment_id (Optional[str]): The experiment ID.

        Returns:
            Tuple[str, str]: A tuple key (project, log_stream) used for caching.
        """
        _logger.debug("current thread is %s", threading.current_thread().name)

        # GalileoLoggerSingleton must NOT be shared across different threads
        current_thread_name = threading.current_thread().name
        key = (current_thread_name,)

        if project is None:
            project = getenv("GALILEO_PROJECT", DEFAULT_PROJECT_NAME)
        if log_stream is None:
            log_stream = getenv("GALILEO_LOG_STREAM", DEFAULT_LOG_STREAM_NAME)

        if experiment_id is not None:
            return key + (project, experiment_id)

        return key + (project, log_stream)

    def get(
        self, *, project: Optional[str] = None, log_stream: Optional[str] = None, experiment_id: Optional[str] = None
    ) -> GalileoLogger:
        """
        Retrieve an existing GalileoLogger or create a new one if it does not exist.

        This method first computes the key from the project and log_stream parameters,
        checks if a logger exists in the cache, and if not, creates a new GalileoLogger.
        The creation and caching are done in a thread-safe manner.

        Args:
            project (Optional[str], optional): The project name. Defaults to None.
            log_stream (Optional[str], optional): The log stream name. Defaults to None.
            experiment_id (Optional[str], optional): The experiment ID. Defaults to None.

        Returns:
            GalileoLogger: An instance of GalileoLogger corresponding to the key.
        """
        # Compute the key based on provided parameters or environment variables.
        key = GalileoLoggerSingleton._get_key(project, log_stream, experiment_id)

        # First check without acquiring lock for performance.
        if key in self._galileo_loggers:
            return self._galileo_loggers[key]

        # Acquire lock for thread-safe creation of new logger.
        with self._lock:
            # Double-check in case another thread created the logger while waiting.
            if key in self._galileo_loggers:
                return self._galileo_loggers[key]

            # Prepare initialization arguments, only including non-None values.
            galileo_client_init_args = {"project": project, "log_stream": log_stream, "experiment_id": experiment_id}
            # Create the logger with filtered kwargs.
            logger = GalileoLogger(**{k: v for k, v in galileo_client_init_args.items() if v is not None})

            # Cache the newly created logger.
            if logger:
                self._galileo_loggers[key] = logger
            return logger

    def reset(
        self, project: Optional[str] = None, log_stream: Optional[str] = None, experiment_id: Optional[str] = None
    ) -> None:
        """
        Reset (terminate and remove) one or all GalileoLogger instances.

        Args:
            project (Optional[str], optional): The project name. Defaults to None.
            log_stream (Optional[str], optional): The log stream name. Defaults to None.
            experiment_id (Optional[str], optional): The experiment ID. Defaults to None.
        """
        with self._lock:
            # Terminate and remove a specific logger.
            key = GalileoLoggerSingleton._get_key(project, log_stream, experiment_id)
            if key in self._galileo_loggers:
                self._galileo_loggers[key].terminate()
                del self._galileo_loggers[key]

    def reset_all(self) -> None:
        """
        Reset (terminate and remove) all GalileoLogger instances.
        """
        with self._lock:
            # Terminate and clear all logger instances.
            for logger in self._galileo_loggers.values():
                logger.terminate()
            self._galileo_loggers.clear()

    def flush(
        self, project: Optional[str] = None, log_stream: Optional[str] = None, experiment_id: Optional[str] = None
    ) -> None:
        """
        Flush (upload and clear) a GalileoLogger instance.

        If both project and log_stream are None, then all cached loggers are flushed
        and cleared. Otherwise, only the specific logger corresponding to the provided
        key (project, log_stream) is flushed and removed.

        Args:
            project (Optional[str], optional): The project name. Defaults to None.
            log_stream (Optional[str], optional): The log stream name. Defaults to None.
            experiment_id (Optional[str], optional): The experiment ID. Defaults to None.
        """
        with self._lock:
            # Terminate and remove a specific logger.
            key = GalileoLoggerSingleton._get_key(project, log_stream, experiment_id)
            if key in self._galileo_loggers:
                self._galileo_loggers[key].flush()

    def flush_all(self) -> None:
        """
        Flush (upload and clear) all GalileoLogger instances.
        """
        with self._lock:
            # Terminate and clear all logger instances.
            for logger in self._galileo_loggers.values():
                logger.flush()

    def get_all_loggers(self) -> dict[tuple[str, str], GalileoLogger]:
        """
        Retrieve a copy of the dictionary containing all active loggers.

        Returns:
            Dict[Tuple[str, str], GalileoLogger]: A dictionary mapping keys
            (project, log_stream) to their corresponding GalileoLogger instances.
        """
        # Return a shallow copy of the loggers dictionary to prevent external modifications.
        return dict(self._galileo_loggers)
