import logging
import threading
from os import getenv
from typing import ClassVar, Optional

from galileo.constants import DEFAULT_LOG_STREAM_NAME, DEFAULT_PROJECT_NAME
from galileo.logger import GalileoLogger
from galileo.logger.logger import GalileoLoggerException
from galileo.schema.metrics import LocalMetricConfig

_logger = logging.getLogger(__name__)


def _validate_distributed_tracing_mode(trace_id: Optional[str], span_id: Optional[str], mode: str) -> None:
    """
    Validate that distributed tracing (trace_id/span_id) is only used in streaming mode.

    Parameters
    ----------
    trace_id
        Optional trace ID for distributed tracing
    span_id
        Optional span ID for distributed tracing
    mode
        The logger mode (should be "streaming" if trace_id or span_id are provided)

    Raises
    ------
    GalileoLoggerException
        If trace_id or span_id are provided but mode is not "streaming"
    """
    if trace_id or span_id:
        if mode != "streaming":
            raise GalileoLoggerException("trace_id or span_id can only be used in streaming mode")


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
    _galileo_loggers: ClassVar[dict[tuple[str, ...], GalileoLogger]] = {}  # Cache for loggers.

    def __new__(cls) -> "GalileoLoggerSingleton":
        """
        Override __new__ to ensure only one instance of GalileoLoggerSingleton is created.

        Returns
        -------
        GalileoLoggerSingleton
            The singleton instance.
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:  # Double-checked locking.
                    cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def _get_key(
        project: Optional[str],
        log_stream: Optional[str],
        experiment_id: Optional[str] = None,
        mode: str = "batch",
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
    ) -> tuple[str, ...]:
        """
        Generate a key tuple based on project and log_stream parameters.

        If project or log_stream are None, the method attempts to retrieve them
        from environment variables (GALILEO_PROJECT and GALILEO_LOG_STREAM). If still
        None, defaults to "default".

        Parameters
        ----------
        project: (Optional[str])
            The project name.
        log_stream: (Optional[str])
            The log stream name.
        experiment_id: (Optional[str])
            The experiment ID.
        mode: (Optional[str])
            The logger mode.
        trace_id: (Optional[str])
            Trace ID for distributed tracing (included in cache key for proper isolation).
        span_id: (Optional[str])
            Span ID for distributed tracing (included in cache key for proper isolation).

        Returns
        -------
        Tuple[str, ...]
            A tuple key used for caching. Includes trace_id/span_id when provided for distributed tracing
            to ensure nested calls within the same request reuse the same logger instance.
        """
        _logger.debug("current thread is %s", threading.current_thread().name)

        # GalileoLoggerSingleton must NOT be shared across different threads
        current_thread_name = threading.current_thread().name
        key = (current_thread_name, mode)

        if project is None:
            project = getenv("GALILEO_PROJECT", DEFAULT_PROJECT_NAME)
        if log_stream is None:
            log_stream = getenv("GALILEO_LOG_STREAM", DEFAULT_LOG_STREAM_NAME)

        base_key = (*key, project, experiment_id) if experiment_id is not None else (*key, project, log_stream)

        # For distributed tracing, include trace_id/span_id in the cache key
        # This allows nested calls within the same request to reuse the same logger instance
        if trace_id or span_id:
            # Assert that mode is streaming when distributed tracing is used
            _validate_distributed_tracing_mode(trace_id, span_id, mode)
            return (*base_key, trace_id or "", span_id or "")

        return base_key

    def get(
        self,
        *,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
        experiment_id: Optional[str] = None,
        mode: str = "batch",
        local_metrics: Optional[list[LocalMetricConfig]] = None,
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
    ) -> GalileoLogger:
        """
        Retrieve an existing GalileoLogger or create a new one if it does not exist.

        This method first computes the key from the project and log_stream parameters,
        checks if a logger exists in the cache, and if not, creates a new GalileoLogger.
        The creation and caching are done in a thread-safe manner.

        Parameters
        ----------
        project (Optional[str], optional)
            The project name. Defaults to None.
        log_stream (Optional[str], optional)
            The log stream name. Defaults to None.
        experiment_id (Optional[str], optional)
            The experiment ID. Defaults to None.
        local_metrics (Optional[list[LocalScorerConfig]], optional)
            Local scorers to run on traces/spans.
            Only used if initializing a new logger, ignored otherwise.  Defaults to None.
        trace_id (Optional[str], optional)
            Trace ID for distributed tracing. If provided, logger will use streaming mode.
            Defaults to None.
        span_id (Optional[str], optional)
            Span ID for distributed tracing. If provided, logger will use streaming mode.
            Defaults to None.

        Returns
        -------
        GalileoLogger
            An instance of GalileoLogger corresponding to the key.
        """
        # If trace_id or span_id is provided, use streaming mode
        if trace_id or span_id:
            mode = "streaming"
            # Assert that mode is streaming when distributed tracing is used
            _validate_distributed_tracing_mode(trace_id, span_id, mode)

        # Compute cache key (includes trace_id/span_id for distributed tracing)
        key = GalileoLoggerSingleton._get_key(project, log_stream, experiment_id, mode, trace_id, span_id)

        # First check without acquiring lock for performance.
        if key in self._galileo_loggers:
            return self._galileo_loggers[key]

        # Acquire lock for thread-safe creation of new logger.
        with self._lock:
            # Double-check in case another thread created the logger while waiting.
            if key in self._galileo_loggers:
                return self._galileo_loggers[key]

            # Prepare initialization arguments, only including non-None values.
            galileo_client_init_args = {
                "project": project,
                "log_stream": log_stream,
                "experiment_id": experiment_id,
                "local_metrics": local_metrics,
                "experimental": {"mode": mode},
                "trace_id": trace_id,
                "span_id": span_id,
            }
            # Create the logger with filtered kwargs.
            logger = GalileoLogger(**{k: v for k, v in galileo_client_init_args.items() if v is not None})

            # Cache the logger
            if logger:
                self._galileo_loggers[key] = logger
            return logger

    def reset(
        self,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
        experiment_id: Optional[str] = None,
        mode: str = "batch",
    ) -> None:
        """
        Reset (terminate and remove) one or all GalileoLogger instances.

        Parameters
        ----------
        project (Optional[str], optional)
            The project name. Defaults to None.
        log_stream (Optional[str], optional)
            The log stream name. Defaults to None.
        experiment_id (Optional[str], optional)
            The experiment ID. Defaults to None.
        """
        with self._lock:
            # Terminate and remove a specific logger.
            key = GalileoLoggerSingleton._get_key(project, log_stream, experiment_id, mode)
            if key in self._galileo_loggers:
                self._galileo_loggers[key].terminate()
                del self._galileo_loggers[key]

    def reset_all(self) -> None:
        """Reset (terminate and remove) all GalileoLogger instances."""
        with self._lock:
            # Terminate and clear all logger instances.
            for logger in self._galileo_loggers.values():
                logger.terminate()
            self._galileo_loggers.clear()

    def flush(
        self,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
        experiment_id: Optional[str] = None,
        mode: str = "batch",
    ) -> None:
        """
        Flush (upload and clear) a GalileoLogger instance.

        If both project and log_stream are None, then all cached loggers are flushed
        and cleared. Otherwise, only the specific logger corresponding to the provided
        key (project, log_stream) is flushed and removed.

        Parameters
        ----------
        project (Optional[str], optional)
            The project name. Defaults to None.
        log_stream (Optional[str], optional)
            The log stream name. Defaults to None.
        experiment_id (Optional[str], optional)
            The experiment ID. Defaults to None.
        """
        with self._lock:
            # Terminate and remove a specific logger.
            key = GalileoLoggerSingleton._get_key(project, log_stream, experiment_id, mode)
            if key in self._galileo_loggers:
                self._galileo_loggers[key].flush()

    def flush_all(self) -> None:
        """Flush (upload and clear) all GalileoLogger instances."""
        with self._lock:
            # Terminate and clear all logger instances.
            for logger in self._galileo_loggers.values():
                logger.flush()

    def get_all_loggers(self) -> dict[tuple[str, ...], GalileoLogger]:
        """
        Retrieve a copy of the dictionary containing all active loggers.

        Returns
        -------
        Dict[Tuple[str, ...], GalileoLogger]:
            A dictionary mapping keys (project, log_stream, ...) to their corresponding GalileoLogger instances.
        """
        # Return a shallow copy of the loggers dictionary to prevent external modifications.
        return self._galileo_loggers.copy()
