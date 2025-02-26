import datetime

import pytest
from openai.types import CompletionUsage
from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion, Choice


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
