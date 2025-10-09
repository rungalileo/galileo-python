"""Utility functions for prompt template operations."""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

_logger = logging.getLogger(__name__)


def check_name_exists_in_organization(name: str) -> bool:
    """
    Check if a prompt template name exists in the organization.

    Enforces organization-wide uniqueness by checking global templates.

    Parameters
    ----------
    name : str
        The template name to check.

    Returns
    -------
    bool
        True if the name exists, False otherwise.
    """
    # Import here to avoid circular dependency
    from galileo.prompts import GlobalPromptTemplates

    # Check global templates
    global_templates = GlobalPromptTemplates().list(name_filter=name, limit=1000)
    return any(template.name == name for template in global_templates)


def generate_unique_name(base_name: str) -> str:
    """
    Generate a unique template name by appending (N) if the base name exists.

    Ensures organization-wide uniqueness by checking global templates.
    Automatically increments the suffix until a unique name is found.

    Parameters
    ----------
    base_name : str
        The desired template name.

    Returns
    -------
    str
        A unique name. Returns the original name if unique, otherwise appends (1), (2), etc.

    Raises
    ------
    ValueError
        If unable to generate a unique name after 1000 attempts.

    Examples
    --------
    - If "my-template" doesn't exist → returns "my-template"
    - If "my-template" exists → returns "my-template (1)"
    - If "my-template" and "my-template (1)" exist → returns "my-template (2)"
    """
    if not check_name_exists_in_organization(base_name):
        return base_name

    counter = 1
    while True:
        candidate_name = f"{base_name} ({counter})"
        if not check_name_exists_in_organization(candidate_name):
            _logger.info(f"Name '{base_name}' already exists. Using '{candidate_name}' instead.")
            return candidate_name
        counter += 1
        # Safety limit to prevent infinite loops
        if counter > 1000:
            raise ValueError(f"Unable to generate unique name for '{base_name}' after 1000 attempts")
