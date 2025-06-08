import datetime
from uuid import uuid4

import pytest
from openai.types import CompletionUsage
from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion, Choice

from galileo.resources.models import DatasetContent, DatasetRow, DatasetRowValuesDict, Rule
from galileo.resources.models.rule_operator import RuleOperator
from galileo.resources.models.ruleset import Ruleset


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


@pytest.fixture(
    params=[
        # Single ruleset with a single rule.
        [Ruleset(rules=[Rule(metric="toxicity", operator=RuleOperator.GT, target_value=0.5)])],
        # Single ruleset with multiple rules.
        [
            Ruleset(
                rules=[
                    Rule(metric="toxicity", operator=RuleOperator.GT, target_value=0.5),
                    Rule(metric="tone", operator=RuleOperator.LT, target_value=0.8),
                ]
            )
        ],
        # Single ruleset with an unknown metric.
        [Ruleset(rules=[Rule(metric="unknown", operator=RuleOperator.GT, target_value=0.5)])],
        # Multiple rulesets with a single rule each.
        [
            Ruleset(rules=[Rule(metric="toxicity", operator=RuleOperator.GT, target_value=0.5)]),
            Ruleset(rules=[Rule(metric="toxicity", operator=RuleOperator.LT, target_value=0.8)]),
        ],
    ]
)
def rulesets(request: pytest.FixtureRequest) -> list[Ruleset]:
    return request.param
