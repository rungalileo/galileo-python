# Galileo Python SDK

The Python client library for the Galileo AI platform.

## Getting Started

### Installation

`pip install galileo`

### Setup

Set the following environment variables:

- `GALILEO_API_KEY`: Your Galileo API key
- `GALILEO_PROJECT`: (Optional) Project name
- `GALILEO_LOG_STREAM`: (Optional) Log stream name

Note: if you would like to point to an environment other than app.galileo.ai, you'll need to set the GALILEO_CONSOLE_URL environment variable.

### Usage

```python
import os

from galileo import galileo_context, openai

# If you've set your GALILEO_PROJECT and GALILEO_LOG_STREAM env vars, you can skip this step
galileo_context.init(project="your-project-id", log_stream="your-log-stream-id")

# Initialize the Galileo wrapped OpenAI client
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def call_openai():
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Say this is a test"}], model="gpt-4o"
    )

    return chat_completion.choices[0].message.content


# This will create a single span trace with the OpenAI call
call_openai()
```

You can also use the `@log` decorator to log spans. Here's how to create a workflow span with two nested LLM spans:

```python
from galileo import log

@log
def make_nested_call():
    call_openai()
    call_openai()


# This will create a trace with a workflow span and two nested LLM spans containing the OpenAI calls
make_nested_call()
```

Here's how to create a retriever span using the decorator:

```python
from galileo import log

@log(span_type="retriever")
def retrieve_documents(query: str):
    return ["doc1", "doc2"]

# This will create a trace with a retriever span containing the documents in the output
retrieve_documents(query="history")
```

Here's how to create a tool span using the decorator:

```python
from galileo import log

@log(span_type="tool")
def tool_call(input: str = "tool call input"):
    return "tool call output"

# This will create a trace with a tool span containing the tool call output
tool_call(input="question")
```

In some cases, you may want to wrap a block of code to start and flush a trace automatically. You can do this using the `galileo_context` context manager:

```python
from galileo import galileo_context

# This will log to the project and log stream specified in the context manager
with galileo_context():
    content = make_nested_call()
    print(content)
```

`galileo_context` also allows you specify a separate project and log stream for the trace:

```python
from galileo import galileo_context

# This will log to the project and log stream specified in the context manager
with galileo_context(project="gen-ai-project", log_stream="test2"):
    content = make_nested_call()
    print(content)
```

You can also use the `GalileoLogger` for manual logging scenarios:

```python
from galileo.logger import GalileoLogger

# This will log to the project and log stream specified in the logger constructor
logger = GalileoLogger(project="gen-ai-project", log_stream="test3")
trace = logger.start_trace("Say this is a test")

logger.add_llm_span(
    input="Say this is a test",
    output="Hello, this is a test",
    model="gpt-4o",
    num_input_tokens=10,
    num_output_tokens=3,
    total_tokens=13,
    duration_ns=1000,
)

logger.conclude(output="Hello, this is a test", duration_ns=1000)
logger.flush() # This will upload the trace to Galileo
```

OpenAI streaming example:

```python
import os

from galileo import openai

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

stream = client.chat.completions.create(
    messages=[{"role": "user", "content": "Say this is a test"}], model="gpt-4o", stream=True,
)

# This will create a single span trace with the OpenAI call
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

In some cases (like long-running processes), it may be necessary to explicitly flush the trace to upload it to Galileo:

```python
import os

from galileo import galileo_context, openai

galileo_context.init(project="your-project-id", log_stream="your-log-stream-id")

# Initialize the Galileo wrapped OpenAI client
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def call_openai():
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Say this is a test"}], model="gpt-4o"
    )

    return chat_completion.choices[0].message.content


# This will create a single span trace with the OpenAI call
call_openai()

# This will upload the trace to Galileo
galileo_context.flush()
```


Langchain callback handler:

```python
from galileo.handlers.langchain import GalileoCallback
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

# You can optionally pass a GalileoLogger instance to the callback if you don't want to use the default context
callback = GalileoCallback()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, callbacks=[callback])

# Create a message with the user's query
messages = [HumanMessage(content="What is LangChain and how is it used with OpenAI?")]

# Make the API call
response = llm.invoke(messages)

print(response.content)
```


Run Experiment:

```python
from galileo.datasets import get_dataset
from galileo.experiments import run_experiment
from galileo.prompts import get_prompt_template, create_prompt_template
from galileo.resources.models import MessageRole, Message

prompt = get_prompt_template(
    name="andrii-good-prompt",
    project="andrii-new-project"
)

if prompt is None:
    prompt = create_prompt_template(
        name="andrii-good-prompt",
        project="andrii-new-project",
        messages=[
            Message(role=MessageRole.SYSTEM, content="you are a helpful assistant"),
            Message(role=MessageRole.USER, content="why is sky blue?")
        ]
    )

results = run_experiment(
    "my-experiment",
    dataset=get_dataset(name="storyteller-dataset"),
    prompt=prompt,
    metrics=["correctness"],
    project="andrii-new-project",
)
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
