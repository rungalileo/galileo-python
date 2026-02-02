from __future__ import annotations

import builtins
import json
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

from galileo.__future__.shared.base import StateManagementMixin, SyncState
from galileo.__future__.shared.exceptions import ValidationError
from galileo.config import GalileoPythonConfig
from galileo.projects import Projects
from galileo.prompts import GlobalPromptTemplates
from galileo.resources.api.prompts import (
    create_global_prompt_template_version_templates_template_id_versions_post,
    query_template_versions_templates_template_id_versions_query_post,
    set_selected_global_template_version_templates_template_id_versions_version_put,
)
from galileo.resources.models import (
    BasePromptTemplateVersion,
    HTTPValidationError,
    ListPromptTemplateVersionParams,
    MessagesListItem,
)
from galileo.resources.types import Unset
from galileo.schema.message import Message
from galileo.utils.env_helpers import _get_project_from_env, _get_project_id_from_env
from galileo_core.schemas.logging.llm import MessageRole

if TYPE_CHECKING:
    from galileo.resources.models import PromptRunSettings

logger = logging.getLogger(__name__)


def _parse_template_to_messages(template: Any) -> list[Message]:
    """
    Parse template (list or JSON string) into Message objects.

    Args:
        template: The template content from the API. Can be a list of message
            objects or a JSON string containing a messages array.

    Returns
    -------
        list[Message]: Parsed messages.
    """
    if isinstance(template, list):
        return [Message(role=MessageRole(item.role), content=item.content) for item in template]

    # Try to parse as JSON string containing messages array
    if isinstance(template, str):
        try:
            parsed = json.loads(template)
            if isinstance(parsed, list):
                return [Message(role=MessageRole(item["role"]), content=item["content"]) for item in parsed]
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
        # Fallback: treat as single user message
        return [Message(role=MessageRole.user, content=template)]

    return []


class PromptVersion:
    """
    Represents a single version of a prompt template.

    Attributes
    ----------
        id (str): The unique version identifier.
        version (int): The version number (1-indexed).
        messages (list[Message]): The prompt messages for this version.
        settings (PromptRunSettings | None): The prompt run settings.
        created_at (datetime | None): When the version was created.
        updated_at (datetime | None): When the version was last updated.
    """

    id: str
    version: int
    messages: list[Message]
    settings: PromptRunSettings | None
    created_at: datetime | None
    updated_at: datetime | None

    def __str__(self) -> str:
        """String representation of the prompt version."""
        return f"PromptVersion(version={self.version}, id='{self.id}')"

    def __repr__(self) -> str:
        """Detailed string representation of the prompt version."""
        return f"PromptVersion(version={self.version}, id='{self.id}', messages={len(self.messages)} messages)"

    @classmethod
    def _from_api_response(cls, response: Any) -> PromptVersion:
        """
        Factory method to create a PromptVersion instance from an API response.

        Args:
            response: The version data retrieved from the API.

        Returns
        -------
            PromptVersion: A new PromptVersion instance populated with the API data.
        """
        instance = cls.__new__(cls)
        instance.id = response.id
        instance.version = response.version
        instance.messages = _parse_template_to_messages(response.template)
        instance.settings = response.settings if hasattr(response, "settings") else None
        instance.created_at = response.created_at if hasattr(response, "created_at") else None
        instance.updated_at = response.updated_at if hasattr(response, "updated_at") else None
        return instance


class Prompt(StateManagementMixin):
    """
    Object-centric interface for Galileo prompts.

    This class provides an intuitive way to work with Galileo prompts,
    encapsulating prompt management operations including version management.

    Attributes
    ----------
        id (str): The unique prompt identifier.
        name (str): The prompt name.
        messages (list[Message]): The prompt messages (from selected version).
        project_id (str | None): The project ID associated with this prompt (see Known Limitations).
        project_name (str | None): The project name associated with this prompt (see Known Limitations).
        selected_version_number (int | None): The currently selected version number.
        selected_version_id (str | None): The ID of the selected version.
        total_versions (int | None): Total number of versions for this prompt.
        all_available_versions (list[int] | None): List of all available version numbers.
        max_version (int | None): The highest version number.
        created_at (datetime.datetime): When the prompt was created.
        updated_at (datetime.datetime): When the prompt was last updated.

    Known Limitations
    -----------------
        Project Association: The API response schema (BasePromptTemplateResponse) does not
        include project association information. Therefore, ``project_id`` and ``project_name``
        will only be populated for prompts created in the current session via ``create()``.
        Prompts retrieved via ``get()`` or ``list()`` will have these attributes set to ``None``,
        even if they were originally created with a project association.

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

        # Create a prompt associated with a project
        prompt = Prompt(
            name="ml-expert-v1",
            messages=[...],
            project_name="My Project",
        ).create()

        # Get an existing prompt
        prompt = Prompt.get(name="ml-expert-v1")

        # Create a new version with updated messages
        prompt.create_version(messages=[...])

        # List all versions
        versions = prompt.list_versions()

        # Select a specific version
        prompt.select_version(2)

        # Update a prompt
        prompt.update(messages=[...])

        # Delete a prompt
        prompt.delete()
    """

    # Type annotations for instance attributes
    id: str | None
    name: str
    messages: list[Message]
    project_id: str | None
    project_name: str | None
    selected_version_number: int | None
    selected_version_id: str | None
    total_versions: int | None
    all_available_versions: list[int] | None
    max_version: int | None
    created_at: datetime | None
    updated_at: datetime | None

    def __str__(self) -> str:
        """String representation of the prompt."""
        return f"Prompt(name='{self.name}', id='{self.id}')"

    def __repr__(self) -> str:
        """Detailed string representation of the prompt."""
        version_info = f", version={self.selected_version_number}" if self.selected_version_number else ""
        return f"Prompt(name='{self.name}', id='{self.id}', messages={len(self.messages)} messages{version_info})"

    def __init__(
        self,
        name: str | None = None,
        messages: list[Message] | None = None,
        project_id: str | None = None,
        project_name: str | None = None,
    ) -> None:
        """
        Initialize a Prompt instance locally.

        Creates a local prompt object that exists only in memory until .create()
        is called to persist it to the API.

        Args:
            name (Optional[str]): The name of the prompt to create.
            messages (Optional[list[Message]]): The messages for the prompt.
            project_id (Optional[str]): The project ID to associate with this prompt.
            project_name (Optional[str]): The project name to associate with this prompt.
                If not provided, falls back to GALILEO_PROJECT environment variable.

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
        self.project_id = project_id
        self.project_name = project_name
        self.selected_version_number = None
        self.selected_version_id = None
        self.total_versions = None
        self.all_available_versions = None
        self.max_version = None
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

        Note
        ----
            API Limitation: The prompt response schema (BasePromptTemplateResponse) does not
            include project association information. Therefore, project_id and project_name
            will be None for prompts retrieved via get() or list(). Project info is only
            available for prompts created in the current session via create().
        """
        instance = cls._create_empty()
        instance.id = retrieved_prompt.id
        instance.name = retrieved_prompt.name

        # Extract messages from the selected_version template using helper
        instance.messages = _parse_template_to_messages(retrieved_prompt.selected_version.template)

        # Version-related attributes
        instance.selected_version_number = retrieved_prompt.selected_version.version
        instance.selected_version_id = retrieved_prompt.selected_version_id
        instance.total_versions = retrieved_prompt.total_versions
        instance.all_available_versions = (
            list(retrieved_prompt.all_available_versions) if retrieved_prompt.all_available_versions else None
        )
        instance.max_version = retrieved_prompt.max_version

        # API Limitation: The GET /templates/{id} response does not include project
        # association. The API only accepts project_id as a query param during creation
        # (POST /templates?project_id=...) but does not return it in subsequent responses.
        # To fix this, the API would need to include project info in BasePromptTemplateResponse.
        instance.project_id = None
        instance.project_name = None

        instance.created_at = retrieved_prompt.created_at
        instance.updated_at = retrieved_prompt.updated_at

        # Set state to synced since we just retrieved from API
        instance._set_state(SyncState.SYNCED)
        return instance

    def _update_from_api_response(self, retrieved_prompt: Any) -> None:
        """
        Update this instance's attributes from an API response.

        Args:
            retrieved_prompt: The prompt data retrieved from the API.
        """
        self.id = retrieved_prompt.id
        self.name = retrieved_prompt.name

        # Extract messages from the selected_version template using helper
        self.messages = _parse_template_to_messages(retrieved_prompt.selected_version.template)

        # Version-related attributes
        self.selected_version_number = retrieved_prompt.selected_version.version
        self.selected_version_id = retrieved_prompt.selected_version_id
        self.total_versions = retrieved_prompt.total_versions
        self.all_available_versions = (
            list(retrieved_prompt.all_available_versions) if retrieved_prompt.all_available_versions else None
        )
        self.max_version = retrieved_prompt.max_version

        self.created_at = retrieved_prompt.created_at
        self.updated_at = retrieved_prompt.updated_at

        # Set state to synced
        self._set_state(SyncState.SYNCED)

    def create(self) -> Prompt:
        """
        Persist this prompt to the API.

        If project_id or project_name is set, associates the prompt with that project.
        If neither is set, falls back to GALILEO_PROJECT_ID or GALILEO_PROJECT env vars.

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

            # Resolve project using explicit params or env fallbacks (GALILEO_PROJECT_ID, GALILEO_PROJECT)
            resolved_project_id: str | None = None

            # Only attempt project resolution if we have explicit params or env vars
            has_project_context = (
                self.project_id is not None
                or self.project_name is not None
                or _get_project_id_from_env() is not None
                or _get_project_from_env() is not None
            )

            if has_project_context:
                project_obj = Projects().get_with_env_fallbacks(id=self.project_id, name=self.project_name)
                if project_obj:
                    resolved_project_id = project_obj.id
                    # Store resolved project info on the instance
                    self.project_id = project_obj.id
                    self.project_name = project_obj.name
                    logger.debug(f"Prompt.create: resolved project_id='{resolved_project_id}'")

            prompt_service = GlobalPromptTemplates()
            created_prompt = prompt_service.create(
                name=self.name, template=self.messages, project_id=resolved_project_id
            )

            # Update attributes from response using helper
            self._update_from_api_response(created_prompt)

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

        prompt_service = GlobalPromptTemplates()
        if id is not None:
            retrieved_prompt = prompt_service.get(template_id=id)
        else:  # name is not None
            # name is guaranteed to be str here due to validation above
            assert name is not None
            retrieved_prompt = prompt_service.get(name=name)

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
        prompt_service = GlobalPromptTemplates()
        retrieved_prompts = prompt_service.list(
            name_filter=name_filter, limit=limit, project_id=project_id, project_name=project_name
        )
        logger.debug(f"Prompt.list: found {len(retrieved_prompts)} prompts - completed")

        return [cls._from_api_response(retrieved_prompt) for retrieved_prompt in retrieved_prompts]

    def update(self, *, name: str) -> Prompt:
        """
        Update this prompt's name.

        Note
        ----
            The API only supports updating the prompt name. To update messages,
            use ``create_version()`` which creates a new immutable version.
            This design ensures traceability and allows rollback to previous versions.

        Args:
            name (str): New name for the prompt.

        Returns
        -------
            Prompt: This prompt instance (for method chaining).

        Raises
        ------
            ValueError: If called on a local-only prompt (no ID).

        Examples
        --------
            prompt = Prompt.get(name="ml-expert-v1")
            prompt.update(name="ml-expert-v2")

            # To update messages, use create_version() instead:
            prompt.create_version(messages=[
                Message(role=MessageRole.system, content="Updated system message"),
                Message(role=MessageRole.user, content="{{input}}"),
            ])
        """
        if self.id is None:
            raise ValueError("Prompt ID is not set. Cannot update a local-only prompt.")
        try:
            logger.info(f"Prompt.update: id='{self.id}' name='{name}' - started")
            prompt_service = GlobalPromptTemplates()
            updated_prompt = prompt_service.update(template_id=self.id, name=name)
            # Update our instance attributes
            self.name = updated_prompt.name
            self.updated_at = updated_prompt.updated_at
            # Set state to synced after successful update
            self._set_state(SyncState.SYNCED)
            logger.info(f"Prompt.update: id='{self.id}' - completed")
            return self
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Prompt.update: id='{self.id}' - failed: {e}")
            raise

    def _messages_to_api_format(self, messages: builtins.list[Message]) -> builtins.list[MessagesListItem]:
        """Convert Message objects to API-compatible MessagesListItem objects."""
        return [
            MessagesListItem(role=msg.role.value if hasattr(msg.role, "value") else str(msg.role), content=msg.content)
            for msg in messages
        ]

    def create_version(self, messages: builtins.list[Message] | None = None) -> Prompt:
        """
        Create a new version of this prompt template.

        This creates an actual new version in the prompt's version history,
        not a separate prompt. The new version becomes the selected version.

        Args:
            messages (Optional[list[Message]]): Messages for the new version.
                If not provided, uses the current messages.

        Returns
        -------
            Prompt: This prompt instance with updated version information.

        Raises
        ------
            ValueError: If the prompt has not been saved yet.

        Examples
        --------
            prompt = Prompt.get(name="ml-expert-v1")

            # Create new version with same messages
            prompt.create_version()

            # Create new version with updated messages
            prompt.create_version(messages=[
                Message(role=MessageRole.system, content="Updated system message"),
                Message(role=MessageRole.user, content="{{input}}"),
            ])
        """
        if self.id is None:
            raise ValueError("Prompt ID is not set. Cannot create version for a local-only prompt.")

        try:
            version_messages = messages if messages is not None else self.messages

            logger.info(f"Prompt.create_version: id='{self.id}' - started")

            config = GalileoPythonConfig.get()
            body = BasePromptTemplateVersion(template=self._messages_to_api_format(version_messages))

            response = create_global_prompt_template_version_templates_template_id_versions_post.sync(
                template_id=self.id, client=config.api_client, body=body
            )

            if response is None or isinstance(response, HTTPValidationError):
                raise ValueError(f"Failed to create version: {response}")

            # Select the newly created version to ensure the prompt reflects it
            new_version_number = response.version
            logger.debug(f"Prompt.create_version: id='{self.id}' selecting new version {new_version_number}")
            self.select_version(new_version_number)

            logger.info(f"Prompt.create_version: id='{self.id}' new_version={self.selected_version_number} - completed")
            return self
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Prompt.create_version: id='{self.id}' - failed: {e}")
            raise

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
            prompt_service = GlobalPromptTemplates()
            prompt_service.delete(template_id=self.id)
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
            prompt_service = GlobalPromptTemplates()
            retrieved_prompt = prompt_service.get(template_id=self.id)

            if retrieved_prompt is None:
                raise ValueError(f"Prompt with id '{self.id}' no longer exists")

            # Update all attributes from response
            self._update_from_api_response(retrieved_prompt)

            logger.debug(f"Prompt.refresh: id='{self.id}' - completed")
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Prompt.refresh: id='{self.id}' - failed: {e}")
            raise

    def list_versions(self) -> builtins.list[PromptVersion]:
        """
        List all versions of this prompt template.

        Note
        ----
            This method returns ``PromptVersion`` objects instead of ``Prompt`` objects
            to avoid an N+1 API call problem. Each version's full prompt data would require
            a separate API call. To work with a specific version, use
            ``select_version(version_number)`` which selects the version and updates
            the prompt's messages and version attributes.

        Returns
        -------
            list[PromptVersion]: List of all versions, ordered by version number descending.

        Raises
        ------
            ValueError: If the prompt has not been saved yet.

        Examples
        --------
            prompt = Prompt.get(name="ml-expert-v1")
            versions = prompt.list_versions()
            for v in versions:
                print(f"Version {v.version}: {len(v.messages)} messages")
        """
        if self.id is None:
            raise ValueError("Prompt ID is not set. Cannot list versions for a local-only prompt.")

        try:
            logger.debug(f"Prompt.list_versions: id='{self.id}' - started")

            config = GalileoPythonConfig.get()
            body = ListPromptTemplateVersionParams()

            response = query_template_versions_templates_template_id_versions_query_post.sync(
                template_id=self.id, client=config.api_client, body=body
            )

            if response is None or isinstance(response, HTTPValidationError):
                logger.warning(f"Prompt.list_versions: id='{self.id}' - no versions found or error")
                return []

            versions = [PromptVersion._from_api_response(v) for v in response.versions] if response.versions else []
            logger.debug(f"Prompt.list_versions: id='{self.id}' found {len(versions)} versions - completed")
            return versions
        except Exception as e:
            logger.error(f"Prompt.list_versions: id='{self.id}' - failed: {e}")
            raise

    def select_version(self, version: int) -> Prompt:
        """
        Set a specific version as the selected/active version.

        This updates the prompt's selected version, and the messages
        will be updated to reflect the content of the selected version.

        Args:
            version (int): The version number to select (1-indexed).

        Returns
        -------
            Prompt: This prompt instance with updated version information.

        Raises
        ------
            ValueError: If the prompt has not been saved yet or version not found.

        Examples
        --------
            prompt = Prompt.get(name="ml-expert-v1")
            # Switch to version 2
            prompt.select_version(2)
            print(f"Now using version {prompt.selected_version_number}")
        """
        if self.id is None:
            raise ValueError("Prompt ID is not set. Cannot select version for a local-only prompt.")

        try:
            logger.info(f"Prompt.select_version: id='{self.id}' version={version} - started")

            config = GalileoPythonConfig.get()

            response = set_selected_global_template_version_templates_template_id_versions_version_put.sync(
                template_id=self.id, version=version, client=config.api_client
            )

            if response is None or isinstance(response, HTTPValidationError):
                raise ValueError(f"Failed to select version {version}: {response}")

            # Update local state from response
            self._update_from_api_response(response)

            logger.info(f"Prompt.select_version: id='{self.id}' version={version} - completed")
            return self
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Prompt.select_version: id='{self.id}' version={version} - failed: {e}")
            raise

    def save(self) -> Prompt:
        """
        Save this prompt to the API.

        Behavior depends on the prompt's current state:
        - LOCAL_ONLY: Creates the prompt via create()
        - SYNCED: No action needed, already saved
        - DELETED: Raises ValueError

        For updating an existing prompt's messages, use update(messages=[...])
        or create_version(messages=[...]) instead.

        Returns
        -------
            Prompt: This prompt instance.

        Examples
        --------
            # Create and save a new prompt
            prompt = Prompt(name="my-prompt", messages=[...])
            prompt.save()  # Creates the prompt

            # For existing prompts, use update() for changes
            prompt = Prompt.get(name="my-prompt")
            prompt.update(new_name="renamed-prompt")
            prompt.update(messages=[...])  # Creates new version
        """
        if self.sync_state == SyncState.LOCAL_ONLY:
            # Prompt hasn't been created yet, create it
            return self.create()
        if self.sync_state == SyncState.SYNCED:
            # Already synced, nothing to do
            logger.debug(f"Prompt.save: id='{self.id}' - already synced, no action needed")
            return self
        if self.sync_state == SyncState.DELETED:
            raise ValueError("Cannot save a deleted prompt.")

        # DIRTY or FAILED_SYNC states
        # For now, we don't track dirty state for prompts
        # Users should use update() directly for changes
        raise NotImplementedError(
            "Saving modified prompts is not yet implemented. "
            "Use update(new_name='...') to rename or update(messages=[...]) to create a new version."
        )
