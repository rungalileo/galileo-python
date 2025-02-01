import os
from openai import OpenAI
from galileo import log
from galileo.logger import GalileoLogger

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# logger = GalileoLogger(project="gen-ai-project", log_stream="test")
# trace = logger.start_trace("Say this is a test")


@log(span_type="llm")
def call_openai():
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-4o",
    )

    return chat_completion.choices[0].message.content


content = call_openai()
print(content)

# print(chat_completion.choices[0].message.content)

# trace.add_llm_span(
#     input="Say this is a test",
#     output=chat_completion.choices[0].message.content,
#     model="gpt-4o",
#     input_tokens=10,
#     output_tokens=3,
#     total_tokens=13,
#     duration_ns=1000,
# )

# trace.conclude(
#     output=chat_completion.choices[0].message.content,
#     duration_ns=1000,
# )
