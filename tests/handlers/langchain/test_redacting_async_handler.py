import asyncio
import json
import unittest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from galileo.handlers.langchain.redacting_async_handler import RedactingGalileoAsyncCallback
from galileo.handlers.redacting_async_handler import RedactingGalileoAsyncHandler


class TestRedactingGalileoAsyncCallback(unittest.TestCase):
    def test_init_sets_up_redacting_handler(self):
        # Arrange
        mock_redaction_function = MagicMock()
        mock_service_account_logger = MagicMock()

        # Act
        callback = RedactingGalileoAsyncCallback(
            redaction_function=mock_redaction_function, service_account_logger=mock_service_account_logger
        )

        # Assert
        self.assertIsInstance(callback._handler, RedactingGalileoAsyncHandler)
        self.assertEqual(callback._handler.redaction_function, mock_redaction_function)
        self.assertEqual(callback._handler.service_account_logger, mock_service_account_logger)

    def test_langchain_flow_logs_original_and_redacted_data(self):
        # Arrange
        run_id = uuid4()

        def redaction_function(json_string):
            data = json.loads(json_string)
            redacted_data = {k: f"redacted_{v}" for k, v in data.items()}
            return json.dumps(redacted_data)

        mock_service_account_logger = MagicMock()
        mock_service_account_logger.async_flush = AsyncMock()

        callback = RedactingGalileoAsyncCallback(
            redaction_function=redaction_function,
            service_account_logger=mock_service_account_logger,
            flush_on_chain_end=True,
        )

        # Act
        async def run_langchain_simulation():
            await callback.on_chain_start(
                serialized={"id": ["test"]}, inputs={"input": "original_input"}, run_id=run_id
            )
            await callback.on_chain_end(outputs={"output": "original_output"}, run_id=run_id)

        asyncio.run(run_langchain_simulation())

        # Assert
        mock_service_account_logger.start_trace.assert_called_once_with(
            input='{"input": "original_input"}', redacted_input='{"input": "redacted_original_input"}'
        )
        mock_service_account_logger.conclude.assert_called_once_with(
            output='{"output": "original_output"}', redacted_output='{"output": "redacted_original_output"}'
        )
        mock_service_account_logger.async_flush.assert_called_once()


if __name__ == "__main__":
    unittest.main()
