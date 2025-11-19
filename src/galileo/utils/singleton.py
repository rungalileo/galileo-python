import logging
import threading
from typing import ClassVar, Optional

from galileo.logger import GalileoLogger
from galileo.schema.metrics import LocalMetricConfig
from galileo.utils.env_helpers import _get_log_stream_or_default, _get_mode_or_default, _get_project_or_default

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
                    # Initialize the logger dictionary in the new instance.
                    cls._instance._galileo_loggers = {}
        return cls._instance

    @staticmethod
    def _get_key(
        project: Optional[str],
        log_stream: Optional[str],
        mode: str,
        experiment_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
    ) -> tuple[str, ...]:
        """
        Generate a key tuple based on project, log_stream, and tracing parameters.

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
        mode:
            The logger mode.
        trace_id: (Optional[str])
            The distributed trace ID.
        span_id: (Optional[str])
            The distributed parent span ID.

        Returns
        -------
        Tuple[str, ...]
            A tuple key used for caching. Includes trace_id and span_id for proper
            isolation of concurrent requests in async web servers.
        """
        _logger.debug("current thread is %s", threading.current_thread().name)

        # GalileoLoggerSingleton must NOT be shared across different threads
        current_thread_name = threading.current_thread().name
        key = (current_thread_name, mode)

        # Get project and log_stream with environment variable fallbacks
        project = _get_project_or_default(project)
        log_stream = _get_log_stream_or_default(log_stream)

        # Include trace_id and span_id in key for async web server isolation
        # This ensures different concurrent requests on the same thread get separate loggers
        base_key: tuple[str, ...] = (*key, project)
        base_key = (*base_key, experiment_id) if experiment_id is not None else (*base_key, log_stream)

        # Add trace_id and span_id to key if present (for distributed tracing)
        if trace_id is not None:
            base_key = (*base_key, trace_id)
        if span_id is not None:
            base_key = (*base_key, span_id)

        return base_key

    def get(
        self,
        *,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
        experiment_id: Optional[str] = None,
        mode: Optional[str] = None,
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

        Returns
        -------
        GalileoLogger
            An instance of GalileoLogger corresponding to the key.
        """
        # Check for mode from environment variable if not provided
        mode = _get_mode_or_default(mode)

        # Compute the key based on provided parameters or environment variables.
        key = GalileoLoggerSingleton._get_key(project, log_stream, mode, experiment_id, trace_id, span_id)

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
                "mode": mode,
                "trace_id": trace_id,
                "span_id": span_id,
            }
            # Create the logger with filtered kwargs.
            logger = GalileoLogger(**{k: v for k, v in galileo_client_init_args.items() if v is not None})

            # Cache the newly created logger.
            if logger:
                self._galileo_loggers[key] = logger
            return logger

    def reset(
        self,
        project: Optional[str] = None,
        log_stream: Optional[str] = None,
        experiment_id: Optional[str] = None,
        mode: Optional[str] = None,
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
        mode (Optional[str], optional)
            The logger mode. Defaults to GALILEO_MODE env var, or "batch" if not set.
        """
        mode = _get_mode_or_default(mode)

        with self._lock:
            # Terminate and remove loggers matching the base key (project, log_stream, mode, experiment_id)
            # This will clean up all loggers including those with trace_id/span_id
            base_key = GalileoLoggerSingleton._get_key(project, log_stream, mode, experiment_id)
            keys_to_remove = [k for k in self._galileo_loggers if k[: len(base_key)] == base_key]
            for key in keys_to_remove:
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
        mode: Optional[str] = None,
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
        mode (Optional[str], optional)
            The logger mode. Defaults to GALILEO_MODE env var, or "batch" if not set.
        """
        mode = _get_mode_or_default(mode)

        with self._lock:
            # Flush loggers matching the base key (project, log_stream, mode, experiment_id)
            # This will flush all loggers including those with trace_id/span_id
            base_key = GalileoLoggerSingleton._get_key(project, log_stream, mode, experiment_id)
            keys_to_flush = [k for k in self._galileo_loggers if k[: len(base_key)] == base_key]
            for key in keys_to_flush:
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
            A dictionary mapping keys to their corresponding GalileoLogger instances.
        """
        # Return a shallow copy of the loggers dictionary to prevent external modifications.
        return dict(self._galileo_loggers)
