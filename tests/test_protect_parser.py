import logging
import sys
from json import dumps
from typing import Any, Optional
from unittest.mock import patch

import pytest
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from pytest import LogCaptureFixture, mark

# Skip all tests in this module on Python 3.14+ (pydantic.v1 doesn't support it)
pytestmark = pytest.mark.skipif(sys.version_info >= (3, 14), reason="pydantic.v1 does not support Python 3.14+")

from galileo.handlers.langchain.tool import ProtectParser  # noqa: E402

A_TRACE_METADATA_DICT = {
    "trace_metadata": {
        "id": "57f7ec49-8e44-42cb-8825-4a971e44b252",
        "received_at": 1717538501568372000,
        "response_at": 1717538501568372000,
        "execution_time": 0.46,
    }
}


class ProtectLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "protect"

    def _call(
        self,
        prompt: str,
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        return prompt


@mark.parametrize(
    ("output", "ignore_trigger", "expected_return", "expected_call_count"),
    [
        (dumps({"text": "foo", "status": "not_triggered", **A_TRACE_METADATA_DICT}), False, "foo", 1),
        (dumps({"text": "foo", "status": "not_triggered", **A_TRACE_METADATA_DICT}), True, "foo", 1),
        (dumps({"text": "timeout", "status": "TIMEOUT", **A_TRACE_METADATA_DICT}), False, "timeout", 1),
        (dumps({"text": "timeout", "status": "TIMEOUT", **A_TRACE_METADATA_DICT}), True, "timeout", 1),
        (
            dumps({"text": "not_triggered", "status": "not_triggered", **A_TRACE_METADATA_DICT}),
            False,
            "not_triggered",
            1,
        ),
        (
            dumps({"text": "not_triggered", "status": "not_triggered", **A_TRACE_METADATA_DICT}),
            True,
            "not_triggered",
            1,
        ),
        (
            dumps({"text": "triggering text", "status": "TRIGGERED", **A_TRACE_METADATA_DICT}),
            False,
            "triggering text",
            0,
        ),
        (
            dumps({"text": "triggering text", "status": "TRIGGERED", **A_TRACE_METADATA_DICT}),
            True,
            "triggering text",
            1,
        ),
    ],
)
def test_parser(output: str, ignore_trigger: bool, expected_return: str, expected_call_count: int) -> None:
    # Verify that the ProtectParser invokes the ProtectLLM only if the status is not "TRIGGERED"
    # and ignore_trigger is False.
    parser = ProtectParser(chain=ProtectLLM(), ignore_trigger=ignore_trigger)
    with patch.object(ProtectLLM, "invoke", wraps=parser.chain.invoke) as mock_fn:
        return_value = parser.parser(output)
        assert return_value == expected_return
        assert mock_fn.call_count == expected_call_count


@mark.parametrize(("echo_output", "should_log"), [(True, True), (False, False)])
def test_echo(echo_output: bool, should_log: bool, caplog: LogCaptureFixture, enable_galileo_logging) -> None:
    """Verify that the ProtectParser echoes the output if echo_output is True."""
    parser = ProtectParser(chain=ProtectLLM(), echo_output=echo_output)

    with caplog.at_level(logging.DEBUG, logger="galileo.handlers.langchain.tool"):
        parser.parser(dumps({"text": "foo", "status": "not_triggered", **A_TRACE_METADATA_DICT}))

        if should_log:
            assert "> Raw response: foo" in caplog.text
        else:
            assert "> Raw response: foo" not in caplog.text
