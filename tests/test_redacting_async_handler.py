import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from galileo.handlers.redacting_async_handler import RedactingGalileoAsyncHandler
from galileo.schema.handlers import Node, NodeType


class TestRedactingGalileoAsyncHandler(unittest.TestCase):
    def test_async_commit_adds_redacted_data_and_uses_service_account_logger(self):
        # Arrange
        run_id = uuid4()

        original_node = Node(
            run_id=run_id, node_type=NodeType.LLM, span_params={"input": "original_input", "output": "original_output"}
        )

        def redaction_function(value):
            return f"redacted_{value}"

        mock_service_account_logger = MagicMock()
        mock_service_account_logger.async_flush = AsyncMock()

        handler = RedactingGalileoAsyncHandler(
            redaction_function=redaction_function, service_account_logger=mock_service_account_logger
        )

        handler._nodes = {str(run_id): original_node}
        handler._root_node = original_node
        handler._start_new_trace = True
        handler._flush_on_chain_end = True

        # Act
        asyncio.run(handler.async_commit())

        # Assert
        mock_service_account_logger.start_trace.assert_called_once_with(
            input="original_input", redacted_input="redacted_original_input"
        )
        mock_service_account_logger.conclude.assert_called_once_with(
            output="original_output", redacted_output="redacted_original_output"
        )
        mock_service_account_logger.async_flush.assert_called_once()


if __name__ == "__main__":
    unittest.main()
