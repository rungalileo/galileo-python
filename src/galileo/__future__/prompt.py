"""
Prompt class for the Galileo Future API.

This module provides an object-centric interface for managing Galileo prompts,
offering a more intuitive alternative to the service-based functions.
"""

from __future__ import annotations

from galileo.prompts import PromptTemplate as LegacyPromptTemplate
from galileo.prompts import create_prompt as service_create_prompt
from galileo.prompts import delete_prompt as service_delete_prompt
from galileo.prompts import get_prompt as service_get_prompt
from galileo.prompts import get_prompts as service_get_prompts
from galileo.prompts import update_prompt as service_update_prompt
from galileo.resources.types import Unset
from galileo.schema.message import Message


class Prompt:
    """
    Object-centric interface for Galileo prompts.

    This class provides an intuitive way to work with Galileo prompts,
    encapsulating prompt management operations.

    Attributes:
        id (str): The unique prompt identifier.
        name (str): The prompt name.
        messages (list[Message]): The prompt messages.
        created_at (datetime.datetime): When the prompt was created.
        updated_at (datetime.datetime): When the prompt was last updated.

    Examples:
        # Create a new prompt
        prompt = Prompt(
            name="ml-expert-v1",
            messages=[
                Message(role=MessageRole.system, content="You are an expert in ML."),
                Message(role=MessageRole.user, content="{{input}}"),
            ],
        )

        # Get an existing prompt
        prompt = Prompt.get(name="ml-expert-v1")

        # Update a prompt
        prompt.update(messages=[...])

        # Delete a prompt
        prompt.delete()
    """

    def __init__(
        self,
        name: str | None = None,
        messages: list[Message] | None = None,
        *,
        _legacy_prompt: LegacyPromptTemplate | None = None,
    ) -> None:
        """
        Initialize a Prompt instance.

        When called with name and messages, this creates a new prompt.
        To get an existing prompt, use Prompt.get() instead.

        Args:
            name (Optional[str]): The name of the prompt to create.
            messages (Optional[list[Message]]): The messages for the prompt.
            _legacy_prompt (Optional[LegacyPromptTemplate]): Internal parameter for
                wrapping existing prompt instances.
        """
        # Import MessageRole at the method level to avoid UnboundLocalError
        from galileo_core.schemas.logging.llm import MessageRole

        if _legacy_prompt is not None:
            # Initialize from existing legacy prompt
            self._legacy_prompt = _legacy_prompt
            self.id = _legacy_prompt.id
            self.name = _legacy_prompt.name
            # Extract messages from the selected_version template
            if isinstance(_legacy_prompt.selected_version.template, list):
                # Convert MessagesListItem to Message objects
                self.messages = [
                    Message(role=MessageRole(item.role), content=item.content)
                    for item in _legacy_prompt.selected_version.template
                ]
            else:
                # If it's a string template, store it as a single message
                self.messages = [Message(role=MessageRole.user, content=_legacy_prompt.selected_version.template)]
            self.created_at = _legacy_prompt.created_at
            self.updated_at = _legacy_prompt.updated_at
        elif name is not None and messages is not None:
            # Create a new prompt
            self._legacy_prompt = service_create_prompt(name=name, template=messages)
            self.id = self._legacy_prompt.id
            self.name = self._legacy_prompt.name
            # Extract messages from the selected_version template
            if isinstance(self._legacy_prompt.selected_version.template, list):
                # Convert MessagesListItem to Message objects
                self.messages = [
                    Message(role=MessageRole(item.role), content=item.content)
                    for item in self._legacy_prompt.selected_version.template
                ]
            else:
                # If it's a string template, store it as a single message
                self.messages = [Message(role=MessageRole.user, content=self._legacy_prompt.selected_version.template)]
            self.created_at = self._legacy_prompt.created_at
            self.updated_at = self._legacy_prompt.updated_at
        else:
            raise ValueError(
                "Either 'name' and 'messages' must be provided to create a prompt, "
                "or use Prompt.get() to retrieve an existing prompt"
            )

    @classmethod
    def get(cls, *, id: str | None = None, name: str | None = None) -> Prompt | None:
        """
        Get an existing prompt by ID or name.

        Args:
            id (Optional[str]): The prompt ID.
            name (Optional[str]): The prompt name.

        Returns:
            Optional[Prompt]: The prompt if found, None otherwise.

        Raises:
            ValueError: If neither or both id and name are provided.

        Examples:
            # Get by name
            prompt = Prompt.get(name="ml-expert-v1")

            # Get by ID
            prompt = Prompt.get(id="prompt-123")
        """
        legacy_prompt = service_get_prompt(id=id, name=name)  # type: ignore[call-overload]
        if legacy_prompt is None:
            return None
        return cls(_legacy_prompt=legacy_prompt)

    @classmethod
    def get_prompts(cls, *, name_filter: str | None = None, limit: Unset | int = 100) -> list[Prompt]:
        """
        List global prompt templates with optional filtering.

        Args:
            name_filter (Optional[str]): Filter prompts by name containing this string.
            limit (Union[Unset, int]): Maximum number of prompts to return.

        Returns:
            list[Prompt]: List of prompts matching the criteria.

        Examples:
            # List all prompts
            prompts = Prompt.get_prompts()

            # List prompts with name filtering
            prompts = Prompt.get_prompts(name_filter="geography", limit=50)
        """
        legacy_prompts = service_get_prompts(name_filter=name_filter, limit=limit)
        return [cls(_legacy_prompt=legacy_prompt) for legacy_prompt in legacy_prompts]

    def update(self, *, messages: list[Message] | None = None, new_name: str | None = None) -> None:
        """
        Update this prompt's messages or name.

        Args:
            messages (Optional[list[Message]]): New messages for the prompt.
            new_name (Optional[str]): New name for the prompt.

        Examples:
            prompt = Prompt.get(name="ml-expert-v1")
            prompt.update(messages=[...])
        """
        if new_name is not None:
            # Update the prompt name using the service function
            updated_prompt = service_update_prompt(id=self.id, new_name=new_name)
            # Update our instance attributes
            self._legacy_prompt = updated_prompt
            self.name = updated_prompt.name
            self.updated_at = updated_prompt.updated_at

        if messages is not None:
            # For updating messages, we need to use the legacy prompt's update method
            # This is a limitation - the current service API doesn't support message updates
            # We'll need to recreate the prompt for now
            raise NotImplementedError(
                "Updating prompt messages is not yet supported. "
                "Consider creating a new version with new_version() instead."
            )

    def new_version(self) -> Prompt:
        """
        Create a new version of this prompt.

        Returns:
            Prompt: A new prompt instance that duplicates this one.

        Examples:
            original_prompt = Prompt.get(name="ml-expert-v1")
            new_prompt = original_prompt.new_version()
        """
        # Create a new prompt with a versioned name
        import time

        timestamp = int(time.time())
        new_name = f"{self.name}-v{timestamp}"
        return Prompt(name=new_name, messages=self.messages)

    def delete(self) -> None:
        """
        Delete this prompt.

        Examples:
            prompt = Prompt.get(name="ml-expert-v1")
            prompt.delete()
        """
        service_delete_prompt(id=self.id)

    def __str__(self) -> str:
        """String representation of the prompt."""
        return f"Prompt(name='{self.name}', id='{self.id}')"

    def __repr__(self) -> str:
        """Detailed string representation of the prompt."""
        return f"Prompt(name='{self.name}', id='{self.id}', messages={len(self.messages)} messages)"
