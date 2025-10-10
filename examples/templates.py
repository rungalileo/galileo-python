# /// script
# requires-python = ">=3.10"
# dependencies = ["galileo"]
# ///

from galileo import Message, MessageRole
from galileo.prompts import create_prompt, get_prompt, get_prompts

# Create a global template
prompt_template = create_prompt(
    name="helpful-assistant",
    template=[
        Message(role=MessageRole.SYSTEM, content="you are a helpful assistant"),
        Message(role=MessageRole.USER, content="why is sky blue?"),
    ],
)

# Create a global template associated with a project by ID
project_prompt = create_prompt(
    name="project-assistant",
    template=[
        Message(role=MessageRole.SYSTEM, content="you are a project assistant"),
        Message(role=MessageRole.USER, content="help me with my project"),
    ],
    project_id="your-project-id",  # Associate with a specific project by ID
)

# Create a global template associated with a project by name
project_prompt_by_name = create_prompt(
    name="project-assistant-2",
    template=[
        Message(role=MessageRole.SYSTEM, content="you are another project assistant"),
        Message(role=MessageRole.USER, content="help me with my project"),
    ],
    project_name="My Project",  # Associate with a specific project by name
)

# Get a specific template by name
retrieved_template = get_prompt(name="helpful-assistant")

# List all templates
all_templates = get_prompts()

# List templates filtered by name
filtered_templates = get_prompts(name_filter="assistant")

# List templates associated with a specific project by ID
project_templates = get_prompts(project_id="your-project-id")

# List templates associated with a specific project by name
project_templates_by_name = get_prompts(project_name="My Project")

# Combine filters: get templates with "assistant" in the name for a specific project (by ID)
combined_filters = get_prompts(name_filter="assistant", project_id="your-project-id", limit=10)

# Combine filters: get templates with "assistant" in the name for a specific project (by name)
combined_filters_by_name = get_prompts(name_filter="assistant", project_name="My Project", limit=10)

# Bulk delete multiple templates
# template_ids = [template.id for template in get_prompts(limit=5)]
# bulk_delete_prompts(template_ids)
