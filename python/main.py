import os

import galileo
from galileo import galileo_context, openai
from galileo.logger import GalileoLogger

from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@galileo.log
def call_openai():
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Say this is a test"}], model="gpt-4o"
    )

    return chat_completion.choices[0].message.content


@galileo.log
def make_nested_call():
    return call_openai()


# This will log to the default project and log stream specified in your environment variables
content = make_nested_call()
print(content)

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
