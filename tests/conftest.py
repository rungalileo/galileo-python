import datetime
from uuid import uuid4

import pytest
from openai.types import CompletionUsage
from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion, Choice

from galileo.resources.models import DatasetContent, DatasetRow, DatasetRowValuesDict
from galileo_core.schemas.protect.rule import Rule, RuleOperator
from galileo_core.schemas.protect.ruleset import Ruleset
from tests.testutils.setup import setup_thread_pool_request_capture


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "local")


@pytest.fixture
def create_chat_completion() -> ChatCompletion:
    return ChatCompletion(
        id="foo",
        model="gpt-3.5-turbo",
        object="chat.completion",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(content="The mock is working! ;)", role="assistant"),
            )
        ],
        created=int(datetime.datetime.now().timestamp()),
        usage=CompletionUsage(completion_tokens=13, prompt_tokens=12, total_tokens=25),
    )


@pytest.fixture
def test_dataset_row_id():
    str(uuid4())


@pytest.fixture
def dataset_content(test_dataset_row_id: str):
    row = DatasetRow(
        index=0,
        values=["Which continent is Spain in?", "Europe", '{"meta": "data"}'],
        values_dict=DatasetRowValuesDict.from_dict(
            {"input": "Which continent is Spain in?", "output": "Europe", "metadata": '{"meta": "data"}'}
        ),
        row_id=test_dataset_row_id,
        metadata=None,
    )

    column_names = ["input", "output", "metadata"]
    return DatasetContent(column_names=column_names, rows=[row])


@pytest.fixture
def dataset_content_with_question():
    row = DatasetRow(
        index=0,
        values=['{"question": "Which continent is Spain in?", "expected": "Europe"}', None, None],
        values_dict=DatasetRowValuesDict.from_dict(
            {
                "input": {"question": "Which continent is Spain in?", "expected": "Europe"},
                "output": None,
                "metadata": None,
            }
        ),
        row_id="",
        metadata=None,
    )

    column_names = ["input", "output", "metadata"]
    return DatasetContent(column_names=column_names, rows=[row])


@pytest.fixture
def local_dataset():
    return [
        {"input": "Which continent is Spain in?", "output": "Europe"},
        {"input": "Which continent is Japan in?", "output": "Asia"},
    ]


@pytest.fixture
def thread_pool_capture():
    """
    Pytest fixture that provides a function to capture thread pool requests from streaming methods.

    Usage:
        def test_streaming_method(thread_pool_capture):
            logger = GalileoLogger(project="test", log_stream="test", experimental={"mode": "streaming"})

            capture = thread_pool_capture(logger)

            logger._ingest_trace_streaming(trace)

            capture.mock_pool.assert_called_once()
            request = capture.get_latest_request()
            assert isinstance(request, TracesIngestRequest)
    """

    def _capture_factory(logger):
        return setup_thread_pool_request_capture(logger)

    return _capture_factory


@pytest.fixture(
    params=[
        # Single ruleset with a single rule.
        [Ruleset(rules=[Rule(metric="toxicity", operator=RuleOperator.gt, target_value=0.5)])],
        # Single ruleset with multiple rules.
        [
            Ruleset(
                rules=[
                    Rule(metric="toxicity", operator=RuleOperator.gt, target_value=0.5),
                    Rule(metric="tone", operator=RuleOperator.lt, target_value=0.8),
                ]
            )
        ],
        # Single ruleset with an unknown metric.
        [Ruleset(rules=[Rule(metric="unknown", operator=RuleOperator.gt, target_value=0.5)])],
        # Multiple rulesets with a single rule each.
        [
            Ruleset(rules=[Rule(metric="toxicity", operator=RuleOperator.gt, target_value=0.5)]),
            Ruleset(rules=[Rule(metric="toxicity", operator=RuleOperator.lt, target_value=0.8)]),
        ],
    ]
)
def rulesets(request: pytest.FixtureRequest) -> list[Ruleset]:
    return request.param
