"""Deprecated: use galileo.prompt instead of galileo.__future__.prompt."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.prompt is deprecated. Use galileo.prompt instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.prompt import Prompt, PromptVersion, _parse_template_to_messages  # noqa: E402

__all__ = ["Prompt", "PromptVersion", "_parse_template_to_messages"]
