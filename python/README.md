# Galileo Python SDK

The Python client library for the Galileo AI platform.

## Getting Started

`pip install "galileo[all]"`

### Usage

```python
import os

import galileo
from galileo import galileo_context, openai
from galileo.logger import GalileoLogger

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def call_openai():
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Say this is a test"}], model="gpt-4o"
    )

    return chat_completion.choices[0].message.content


# This will create a single span trace with the OpenAI call
call_openai()

@galileo.log
def make_nested_call():
    return call_openai()


# This will create a trace with a workflow span and a nested LLM span
make_nested_call()

# This will log to the project and log stream specified in the context manager
with galileo_context(project="gen-ai-project", log_stream="test2"):
    content = make_nested_call()
    print(content)


# This will log to the project and log stream specified in the logger constructor
logger = GalileoLogger(project="gen-ai-project", log_stream="test3")
trace = logger.start_trace("Say this is a test")

trace.add_llm_span(
    input="Say this is a test",
    output="Hello, this is a test",
    model="gpt-4o",
    input_tokens=10,
    output_tokens=3,
    total_tokens=13,
    duration_ns=1000,
)

trace.conclude(output="Hello, this is a test", duration_ns=1000)
```

## Local Installation

### Pre-Requisites

1. Clone this repo locally.
2. Install [pyenv](https://github.com/pyenv/pyenv).
3. Install [`poetry`](https://python-poetry.org/): `curl -sSL https://install.python-poetry.org | python3 -`

### Setup

1. Setup a virtual environment:

```sh
pyenv install 3.10.13
pyenv local 3.10.13
```

`poetry` will create a virtual environment using that Python version when it installs dependencies. You can validate that with:

> **_NOTE:_** since The `shell` command was moved to a plugin: poetry-plugin-shell
> https://python-poetry.org/docs/cli/#shell

The easiest way to install the shell plugin is via the self add command of Poetry:
```shell
poetry self add poetry-plugin-shell
```

```sh
poetry shell
poetry run python --version
```

which should print out `Python 3.10.13`.

2. Install dependencies and setup pre-commit hooks:

```sh
pip3 install --upgrade invoke
inv setup
```

3. Copy .env.example to .env and populate the values.

## Auto-generating the API client

1. Run `./scripts/import_api_client.sh` to update the openapi.yml file with the latest
2. Run `./scripts/auto-generate-api-client.sh` to generate the API client
