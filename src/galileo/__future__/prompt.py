"""Re-export from galileo.prompt — will be deprecated once all __future__ modules are migrated."""

from galileo.prompt import Prompt, PromptVersion, _parse_template_to_messages

__all__ = ["Prompt", "PromptVersion", "_parse_template_to_messages"]
