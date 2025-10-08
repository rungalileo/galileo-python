import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from galileo.handlers.redacting_async_handler import RedactingGalileoAsyncHandler
from galileo.schema.handlers import Node, NodeType


class TestRedactingGalileoAsyncHandler(unittest.TestCase):
    def test_async_commit_redacts_and_uses_service_account_logger(self):
        # Arrange
        original_run_id = uuid4()
        redacted_run_id = uuid4()

        original_node = Node(run_id=original_run_id, node_type=NodeType.LLM, span_params={"input": "original_input"})
        redacted_node = Node(run_id=redacted_run_id, node_type=NodeType.LLM, span_params={"input": "redacted_input"})

        mock_redaction_function = MagicMock(return_value={str(redacted_run_id): redacted_node})
        mock_service_account_logger = MagicMock()
        mock_service_account_logger.async_flush = AsyncMock()

        handler = RedactingGalileoAsyncHandler(
            redaction_function=mock_redaction_function, service_account_logger=mock_service_account_logger
        )

        handler._nodes = {str(original_run_id): original_node}
        handler._root_node = redacted_node
        handler._start_new_trace = True
        handler._flush_on_chain_end = True

        # Act
        asyncio.run(handler.async_commit())

        # Assert
        mock_redaction_function.assert_called_once_with({str(original_run_id): original_node})
        mock_service_account_logger.start_trace.assert_called_once_with(input="redacted_input")
        mock_service_account_logger.conclude.assert_called_once()
        mock_service_account_logger.async_flush.assert_called_once()


if __name__ == "__main__":
    unittest.main()
