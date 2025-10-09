from typing import Any, Callable

from galileo.handlers.langchain.async_handler import GalileoAsyncCallback
from galileo.handlers.redacting_async_handler import RedactingGalileoAsyncHandler
from galileo.logger import GalileoLogger


class RedactingGalileoAsyncCallback(GalileoAsyncCallback):
    """
    A custom Galileo async callback handler for Langchain that redacts trace
    data before sending it.

    This handler intercepts the trace data, applies a user-defined redaction
    function, and then uses a separate set of credentials (e.g., for a
    service account) to log the redacted data to Galileo.
    """

    def __init__(
        self, redaction_function: Callable[[Any], Any], service_account_logger: GalileoLogger, *args: Any, **kwargs: Any
    ):
        """
        Initializes the RedactingGalileoAsyncCallback.

        Parameters
        ----------
        redaction_function : Callable[[Any], Any]
            The function to apply to the trace data for redaction.
        service_account_logger : GalileoLogger
            A pre-configured GalileoLogger instance for the service account.
        *args : Any
            Positional arguments to pass to the parent GalileoAsyncCallback.
        **kwargs : Any
            Keyword arguments to pass to the parent GalileoAsyncCallback.
        """
        super().__init__(*args, **kwargs)
        self._handler = RedactingGalileoAsyncHandler(
            *args, redaction_function=redaction_function, service_account_logger=service_account_logger, **kwargs
        )
