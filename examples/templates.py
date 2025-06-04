# /// script
# requires-python = ">=3.10"
# dependencies = ["galileo"]
# ///

from galileo import Message, MessageRole
from galileo.prompts import create_prompt_template, get_prompt_template

# Get existing template
prompt_template = get_prompt_template(name="good-prompt", project="My first project")

# Create template if it doesn't exist
if prompt_template is None:
    prompt_template = create_prompt_template(
        name="good-prompt",
        project="My first project",
        messages=[
            Message(role=MessageRole.SYSTEM, content="you are a helpful assistant"),
            Message(role=MessageRole.USER, content="why is sky blue?"),
        ],
    )

# Retrieve the template we just created
retrieved_template = get_prompt_template(project="My First Project", name="science-assistant")
