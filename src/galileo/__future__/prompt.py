from __future__ import annotations

import builtins
import logging
import time
from datetime import datetime
from typing import Any

from galileo.__future__.shared.base import StateManagementMixin, SyncState
from galileo.__future__.shared.exceptions import ValidationError
from galileo.prompts import GlobalPromptTemplates
from galileo.resources.types import Unset
from galileo.schema.message import Message
from galileo_core.schemas.logging.llm import MessageRole

logger = logging.getLogger(__name__)


class Prompt(StateManagementMixin):
    """
    Object-centric interface for Galileo prompts.

    This class provides an intuitive way to work with Galileo prompts,
    encapsulating prompt management operations.

    Attributes
    ----------
        id (str): The unique prompt identifier.
        name (str): The prompt name.
        messages (list[Message]): The prompt messages.
        created_at (datetime.datetime): When the prompt was created.
        updated_at (datetime.datetime): When the prompt was last updated.

    Examples
    --------
        # Create a new prompt locally, then persist
        prompt = Prompt(
            name="ml-expert-v1",
            messages=[
                Message(role=MessageRole.system, content="You are an expert in ML."),
                Message(role=MessageRole.user, content="{{input}}"),
            ],
        ).create()

        # Get an existing prompt
        prompt = Prompt.get(name="ml-expert-v1")

        # Update a prompt
        prompt.update(messages=[...])

        # Delete a prompt
        prompt.delete()
    """

    # Type annotations for instance attributes
    id: str | None
    name: str
    messages: list[Message]
    created_at: datetime | None
    updated_at: datetime | None

    def __str__(self) -> str:
        """String representation of the prompt."""
        return f"Prompt(name='{self.name}', id='{self.id}')"

    def __repr__(self) -> str:
        """Detailed string representation of the prompt."""
        return f"Prompt(name='{self.name}', id='{self.id}', messages={len(self.messages)} messages)"

    def __init__(self, name: str | None = None, messages: list[Message] | None = None) -> None:
        """
        Initialize a Prompt instance locally.

        Creates a local prompt object that exists only in memory until .create()
        is called to persist it to the API.

        Args:
            name (Optional[str]): The name of the prompt to create.
            messages (Optional[list[Message]]): The messages for the prompt.

        Raises
        ------
            ValidationError: If name or messages is not provided.
        """
        super().__init__()
        if name is None or messages is None:
            raise ValidationError(
                "'name' and 'messages' must be provided to create a prompt. Use Prompt.get() to retrieve an existing prompt."
            )

        # Initialize attributes locally
        self.name = name
        self.messages = messages
        self.id = None
        self.created_at = None
        self.updated_at = None

        # Set initial state
        self._set_state(SyncState.LOCAL_ONLY)

    @classmethod
    def _create_empty(cls) -> Prompt:
        """Internal constructor bypassing __init__ for API hydration."""
        instance = cls.__new__(cls)
        super(Prompt, instance).__init__()
        return instance

    @classmethod
    def _from_api_response(cls, retrieved_prompt: Any) -> Prompt:
        """
        Factory method to create a Prompt instance from an API response.

        Args:
            retrieved_prompt: The prompt data retrieved from the API.

        Returns
        -------
            Prompt: A new Prompt instance populated with the API data.
        """
        instance = cls._create_empty()
        instance.id = retrieved_prompt.id
        instance.name = retrieved_prompt.name
        # Extract messages from the selected_version template
        if isinstance(retrieved_prompt.selected_version.template, list):
            # Convert MessagesListItem to Message objects
            instance.messages = [
                Message(role=MessageRole(item.role), content=item.content)
                for item in retrieved_prompt.selected_version.template
            ]
        else:
            # If it's a string template, store it as a single message
            instance.messages = [Message(role=MessageRole.user, content=retrieved_prompt.selected_version.template)]
        instance.created_at = retrieved_prompt.created_at
        instance.updated_at = retrieved_prompt.updated_at
        # Set state to synced since we just retrieved from API
        instance._set_state(SyncState.SYNCED)
        return instance

    def create(self) -> Prompt:
        """
        Persist this prompt to the API.

        Returns
        -------
            Prompt: This prompt instance with updated attributes from the API.

        Raises
        ------
            Exception: If the API call fails.

        Examples
        --------
            prompt = Prompt(name="test", messages=[...]).create()
            assert prompt.is_synced()
        """
        try:
            logger.info(f"Prompt.create: name='{self.name}' - started")
            templates_service = GlobalPromptTemplates()
            created_prompt = templates_service.create(name=self.name, template=self.messages)

            # Update attributes from response
            self.id = created_prompt.id
            self.name = created_prompt.name
            # Extract messages from the selected_version template
            if isinstance(created_prompt.selected_version.template, list):
                # Convert MessagesListItem to Message objects
                self.messages = [
                    Message(role=MessageRole(item.role), content=item.content)
                    for item in created_prompt.selected_version.template
                ]
            else:
                # If it's a string template, store it as a single message
                self.messages = [Message(role=MessageRole.user, content=created_prompt.selected_version.template)]
            self.created_at = created_prompt.created_at
            self.updated_at = created_prompt.updated_at

            # Set state to synced
            self._set_state(SyncState.SYNCED)
            logger.info(f"Prompt.create: id='{self.id}' - completed")
            return self
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Prompt.create: name='{self.name}' - failed: {e}")
            raise

    @classmethod
    def get(cls, *, id: str | None = None, name: str | None = None) -> Prompt | None:
        """
        Get an existing prompt by ID or name.

        Args:
            id (Optional[str]): The prompt ID.
            name (Optional[str]): The prompt name.

        Returns
        -------
            Optional[Prompt]: The prompt if found, None otherwise.

        Raises
        ------
            ValidationError: If neither or both id and name are provided.

        Examples
        --------
            # Get by name
            prompt = Prompt.get(name="ml-expert-v1")

            # Get by ID
            prompt = Prompt.get(id="prompt-123")
        """
        if id is not None and name is not None:
            raise ValidationError("Cannot specify both id and name")
        if id is None and name is None:
            raise ValidationError("Must specify either id or name")

        templates_service = GlobalPromptTemplates()
        if id is not None:
            retrieved_prompt = templates_service.get(template_id=id)
        else:  # name is not None
            # name is guaranteed to be str here due to validation above
            assert name is not None
            retrieved_prompt = templates_service.get(name=name)

        if retrieved_prompt is None:
            return None

        return cls._from_api_response(retrieved_prompt)

    @classmethod
    def list(
        cls,
        *,
        name_filter: str | None = None,
        limit: Unset | int = 100,
        project_id: str | None = None,
        project_name: str | None = None,
    ) -> list[Prompt]:
        """
        List global prompt templates with optional filtering.

        Args:
            name_filter (Optional[str]): Filter prompts by name containing this string.
            limit (Union[Unset, int]): Maximum number of prompts to return.
            project_id (Optional[str]): Filter prompts used in this project by ID.
            project_name (Optional[str]): Filter prompts used in this project by name.

        Returns
        -------
            list[Prompt]: List of prompts matching the criteria.

        Examples
        --------
            # List all prompts
            prompts = Prompt.list()

            # List prompts with name filtering
            prompts = Prompt.list(name_filter="geography", limit=50)

            # List prompts used in a specific project
            prompts = Prompt.list(project_id="project-123")
            prompts = Prompt.list(project_name="My Project")
        """
        logger.debug(
            f"Prompt.list: name_filter='{name_filter}' project_id='{project_id}' "
            f"project_name='{project_name}' limit={limit} - started"
        )
        templates_service = GlobalPromptTemplates()
        retrieved_prompts = templates_service.list(
            name_filter=name_filter, limit=limit, project_id=project_id, project_name=project_name
        )
        logger.debug(f"Prompt.list: found {len(retrieved_prompts)} prompts - completed")

        return [cls._from_api_response(retrieved_prompt) for retrieved_prompt in retrieved_prompts]

    def update(self, *, messages: builtins.list[Message] | None = None, new_name: str | None = None) -> None:
        """
        Update this prompt's messages or name.

        Args:
            messages (Optional[list[Message]]): New messages for the prompt.
            new_name (Optional[str]): New name for the prompt.

        Examples
        --------
            prompt = Prompt.get(name="ml-expert-v1")
            prompt.update(new_name="ml-expert-v2")
        """
        if self.id is None:
            raise ValueError("Prompt ID is not set. Cannot update a local-only prompt.")
        try:
            if new_name is not None:
                # Update the prompt name using the service
                logger.info(f"Prompt.update: id='{self.id}' new_name='{new_name}' - started")
                templates_service = GlobalPromptTemplates()
                updated_prompt = templates_service.update(template_id=self.id, name=new_name)
                # Update our instance attributes
                self.name = updated_prompt.name
                self.updated_at = updated_prompt.updated_at
                # Set state to synced after successful update
                self._set_state(SyncState.SYNCED)
                logger.info(f"Prompt.update: id='{self.id}' - completed")

            if messages is not None:
                # For updating messages, we need to use the legacy prompt's update method
                # This is a limitation - the current service API doesn't support message updates
                # We'll need to recreate the prompt for now
                raise NotImplementedError(
                    "Updating prompt messages is not yet supported. "
                    "Consider creating a new version with create_version() instead."
                )
        except NotImplementedError:
            # Re-raise NotImplementedError without changing state
            raise
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Prompt.update: id='{self.id}' - failed: {e}")
            raise

    def create_version(self) -> Prompt:
        """
        Create a new version of this prompt.

        Returns
        -------
            Prompt: A new prompt instance that duplicates this one.

        Examples
        --------
            original_prompt = Prompt.get(name="ml-expert-v1")
            new_prompt = original_prompt.create_version()
        """
        # Create a new prompt with a versioned name
        timestamp = int(time.time())
        new_name = f"{self.name}-v{timestamp}"
        logger.info(f"Prompt.create_version: original_id='{self.id}' new_name='{new_name}' - started")
        new_prompt = Prompt(name=new_name, messages=self.messages).create()
        logger.info(f"Prompt.create_version: new_id='{new_prompt.id}' - completed")
        return new_prompt

    def delete(self) -> None:
        """
        Delete this prompt.

        Examples
        --------
            prompt = Prompt.get(name="ml-expert-v1")
            prompt.delete()
        """
        if self.id is None:
            raise ValueError("Prompt ID is not set. Cannot delete a local-only prompt.")
        try:
            logger.info(f"Prompt.delete: id='{self.id}' - started")
            templates_service = GlobalPromptTemplates()
            templates_service.delete(template_id=self.id)
            # Set state to deleted after successful deletion
            self._set_state(SyncState.DELETED)
            logger.info(f"Prompt.delete: id='{self.id}' - completed")
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Prompt.delete: id='{self.id}' - failed: {e}")
            raise

    def refresh(self) -> None:
        """
        Refresh this prompt's state from the API.

        Updates all attributes with the latest values from the remote API
        and sets the state to SYNCED.

        Raises
        ------
            Exception: If the API call fails or the prompt no longer exists.

        Examples
        --------
            prompt.refresh()
            assert prompt.is_synced()
        """
        if self.id is None:
            raise ValueError("Prompt ID is not set. Cannot refresh a local-only prompt.")
        try:
            logger.debug(f"Prompt.refresh: id='{self.id}' - started")
            templates_service = GlobalPromptTemplates()
            retrieved_prompt = templates_service.get(template_id=self.id)

            if retrieved_prompt is None:
                raise ValueError(f"Prompt with id '{self.id}' no longer exists")

            # Update all attributes from response
            self.id = retrieved_prompt.id
            self.name = retrieved_prompt.name
            # Extract messages from the selected_version template
            if isinstance(retrieved_prompt.selected_version.template, list):
                # Convert MessagesListItem to Message objects
                self.messages = [
                    Message(role=MessageRole(item.role), content=item.content)
                    for item in retrieved_prompt.selected_version.template
                ]
            else:
                # If it's a string template, store it as a single message
                self.messages = [Message(role=MessageRole.user, content=retrieved_prompt.selected_version.template)]
            self.created_at = retrieved_prompt.created_at
            self.updated_at = retrieved_prompt.updated_at

            # Set state to synced
            self._set_state(SyncState.SYNCED)
            logger.debug(f"Prompt.refresh: id='{self.id}' - completed")
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Prompt.refresh: id='{self.id}' - failed: {e}")
            raise

    def save(self) -> Prompt:
        """
        Save changes to this prompt.

        Currently delegates to update() for updating prompt properties.

        Returns
        -------
            Prompt: This prompt instance.

        Examples
        --------
            prompt.name = "new-name"
            prompt.save()
        """
        # For now, save() can be used if we implement property-based updates
        # Currently, users should use update() directly
        raise NotImplementedError("Direct save() is not yet implemented. Use update(new_name='...') instead.")
