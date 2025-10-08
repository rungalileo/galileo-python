import logging
from typing import Any, Callable

from galileo.handlers.base_async_handler import GalileoAsyncBaseHandler
from galileo.logger import GalileoLogger
from galileo.utils.serialization import serialize_to_str

_logger = logging.getLogger(__name__)


class RedactingGalileoAsyncHandler(GalileoAsyncBaseHandler):
    """
    A custom Galileo async handler that redacts trace data before sending it.

    This handler intercepts the trace data, applies a user-defined redaction
    function, and then uses a separate set of credentials (e.g., for a
    service account) to log the redacted data to Galileo.

    Attributes
    ----------
    redaction_function : Callable[[Any], Any]
        A function that takes a value and returns a redacted version of it.
    service_account_logger : GalileoLogger
        A GalileoLogger instance configured with service account credentials.
    """

    def __init__(
        self, *args: Any, redaction_function: Callable[[Any], Any], service_account_logger: GalileoLogger, **kwargs: Any
    ):
        """
        Initializes the RedactingGalileoAsyncHandler.

        Parameters
        ----------
        *args : Any
            Positional arguments to pass to the parent GalileoAsyncBaseHandler.
        redaction_function : Callable[[Any], Any]
            The function to apply to the trace data for redaction.
        service_account_logger : GalileoLogger
            A pre-configured GalileoLogger instance for the service account.
        **kwargs : Any
            Keyword arguments to pass to the parent GalileoAsyncBaseHandler.
        """
        super().__init__(*args, **kwargs)
        self.redaction_function = redaction_function
        self.service_account_logger = service_account_logger

    async def async_commit(self) -> None:
        """
        Redacts the trace data and commits it using the service account logger.
        """
        if not self._nodes:
            _logger.warning("No nodes to commit")
            return

        # Apply the redaction function to the collected nodes
        for node in self._nodes.values():
            if "input" in node.span_params:
                node.span_params["redacted_input"] = self.redaction_function(node.span_params["input"])
            if "output" in node.span_params:
                node.span_params["redacted_output"] = self.redaction_function(node.span_params["output"])

        # The rest of this method is a re-implementation of the parent's
        # async_commit, but using the `service_account_logger`.

        root = self._root_node
        if root is None:
            _logger.warning("Unable to add nodes to trace: Root node not set")
            return

        root_node = self._nodes.get(str(root.run_id))
        if root_node is None:
            _logger.warning("Unable to add nodes to trace: Root node does not exist")
            return

        if self._start_new_trace:
            self.service_account_logger.start_trace(
                input=serialize_to_str(root_node.span_params.get("input", "")),
                redacted_input=serialize_to_str(root_node.span_params.get("redacted_input", "")),
            )

        self.log_node_tree(root_node)

        root_output = root_node.span_params.get("output", "")

        if self._start_new_trace:
            redacted_root_output = root_node.span_params.get("redacted_output", "")
            self.service_account_logger.conclude(
                output=serialize_to_str(root_output), redacted_output=serialize_to_str(redacted_root_output)
            )

        if self._flush_on_chain_end:
            await self.service_account_logger.async_flush()

        # Clear nodes after successful commit
        self._nodes.clear()
        self._root_node = None
