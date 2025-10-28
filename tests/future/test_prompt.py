from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from galileo.__future__ import Prompt
from galileo.__future__.shared.base import SyncState
from galileo.__future__.shared.exceptions import ValidationError
from galileo.resources.models.messages_list_item import MessagesListItem
from galileo.schema.message import Message
from galileo_core.schemas.logging.llm import MessageRole


class TestPromptInitialization:
    """Test suite for Prompt initialization."""

    def test_init_with_name_and_messages(self, reset_configuration: None) -> None:
        """Test initializing a prompt with name and messages creates a local-only instance."""
        messages = [
            Message(role=MessageRole.system, content="You are a helpful assistant."),
            Message(role=MessageRole.user, content="{{input}}"),
        ]
        prompt = Prompt(name="Test Prompt", messages=messages)

        assert prompt.name == "Test Prompt"
        assert prompt.messages == messages
        assert prompt.id is None
        assert prompt.sync_state == SyncState.LOCAL_ONLY

    @pytest.mark.parametrize(
        "name,messages", [(None, [Message(role=MessageRole.user, content="{{input}}")]), ("Test Prompt", None)]
    )
    def test_init_without_required_fields_raises_error(
        self, name: str, messages: list, reset_configuration: None
    ) -> None:
        """Test initializing a prompt without required fields raises ValidationError."""
        with pytest.raises(ValidationError, match="'name' and 'messages' must be provided"):
            Prompt(name=name, messages=messages)


class TestPromptCreate:
    """Test suite for Prompt.create() method."""

    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_create_persists_prompt_to_api(
        self, mock_templates_class: MagicMock, reset_configuration: None, mock_prompt: MagicMock
    ) -> None:
        """Test create() persists the prompt to the API and updates attributes."""
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service
        mock_service.create.return_value = mock_prompt

        messages = [Message(role=MessageRole.user, content="{{input}}")]
        prompt = Prompt(name="Test Prompt", messages=messages).create()

        mock_service.create.assert_called_once_with(name="Test Prompt", template=messages)
        assert prompt.id == mock_prompt.id
        assert prompt.is_synced()

    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_create_handles_api_failure(self, mock_templates_class: MagicMock, reset_configuration: None) -> None:
        """Test create() handles API failures and sets state correctly."""
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service
        mock_service.create.side_effect = Exception("API Error")

        messages = [Message(role=MessageRole.user, content="{{input}}")]
        prompt = Prompt(name="Test Prompt", messages=messages)

        with pytest.raises(Exception, match="API Error"):
            prompt.create()

        assert prompt.sync_state == SyncState.FAILED_SYNC


class TestPromptGet:
    """Test suite for Prompt.get() class method."""

    @pytest.mark.parametrize("lookup_key", ["name", "id"])
    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_get_returns_prompt(
        self, mock_templates_class: MagicMock, lookup_key: str, reset_configuration: None, mock_prompt: MagicMock
    ) -> None:
        """Test get() with name or id returns a synced prompt instance."""
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service
        mock_service.get.return_value = mock_prompt

        lookup_value = mock_prompt.id if lookup_key == "id" else mock_prompt.name
        prompt = Prompt.get(**{lookup_key: lookup_value})

        assert prompt is not None
        assert prompt.is_synced()

    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_get_returns_none_when_not_found(self, mock_templates_class: MagicMock, reset_configuration: None) -> None:
        """Test get() returns None when prompt is not found."""
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service
        mock_service.get.return_value = None

        prompt = Prompt.get(name="Nonexistent Prompt")

        assert prompt is None

    @pytest.mark.parametrize(
        "kwargs,expected_error",
        [
            ({"id": "test-id", "name": "Test"}, "Cannot specify both id and name"),
            ({}, "Must specify either id or name"),
        ],
    )
    def test_get_validates_parameters(self, kwargs: dict, expected_error: str, reset_configuration: None) -> None:
        """Test get() validates parameter combinations."""
        with pytest.raises(ValidationError, match=expected_error):
            Prompt.get(**kwargs)


class TestPromptList:
    """Test suite for Prompt.list() class method."""

    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_list_returns_all_prompts(self, mock_templates_class: MagicMock, reset_configuration: None) -> None:
        """Test list() returns a list of synced prompt instances."""
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service

        # Create 3 mock prompts
        mock_prompts = []
        for i in range(3):
            mock_version = MagicMock()
            mock_version.template = [MessagesListItem(role="user", content=f"{{input{i}}}")]
            mock_version.version = 1

            mock_pmt = MagicMock()
            mock_pmt.id = str(uuid4())
            mock_pmt.name = f"Prompt {i}"
            mock_pmt.created_at = MagicMock()
            mock_pmt.updated_at = MagicMock()
            mock_pmt.selected_version = mock_version
            mock_prompts.append(mock_pmt)
        mock_service.list.return_value = mock_prompts

        prompts = Prompt.list()

        assert len(prompts) == 3
        assert all(isinstance(p, Prompt) for p in prompts)
        assert all(p.is_synced() for p in prompts)


class TestPromptUpdate:
    """Test suite for Prompt.update() method."""

    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_update_with_new_name(
        self, mock_templates_class: MagicMock, reset_configuration: None, mock_prompt: MagicMock
    ) -> None:
        """Test update() with new_name updates the prompt name."""
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service

        updated_prompt = MagicMock()
        updated_prompt.id = mock_prompt.id
        updated_prompt.name = "New Name"
        updated_prompt.updated_at = MagicMock()
        updated_prompt.selected_version = mock_prompt.selected_version

        mock_service.get.return_value = mock_prompt
        mock_service.update.return_value = updated_prompt

        prompt = Prompt.get(id=mock_prompt.id)
        prompt.update(new_name="New Name")

        mock_service.update.assert_called_once_with(template_id=mock_prompt.id, name="New Name")
        assert prompt.name == "New Name"
        assert prompt.is_synced()

    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_update_with_messages_raises_not_implemented(
        self, mock_templates_class: MagicMock, reset_configuration: None, mock_prompt: MagicMock
    ) -> None:
        """Test update() with messages raises NotImplementedError."""
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service
        mock_service.get.return_value = mock_prompt

        prompt = Prompt.get(id=mock_prompt.id)

        new_messages = [Message(role=MessageRole.user, content="{{new_input}}")]
        with pytest.raises(NotImplementedError, match="Updating prompt messages"):
            prompt.update(messages=new_messages)

    def test_update_raises_error_for_local_only(self, reset_configuration: None) -> None:
        """Test update() raises ValueError for local-only prompt."""
        messages = [Message(role=MessageRole.user, content="{{input}}")]
        prompt = Prompt(name="Test Prompt", messages=messages)

        with pytest.raises(ValueError, match="Prompt ID is not set"):
            prompt.update(new_name="New Name")


class TestPromptDelete:
    """Test suite for Prompt.delete() method."""

    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_delete_removes_prompt(
        self, mock_templates_class: MagicMock, reset_configuration: None, mock_prompt: MagicMock
    ) -> None:
        """Test delete() removes the prompt."""
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service
        mock_service.get.return_value = mock_prompt

        prompt = Prompt.get(id=mock_prompt.id)
        prompt.delete()

        mock_service.delete.assert_called_once_with(template_id=mock_prompt.id)
        assert prompt.sync_state == SyncState.DELETED

    def test_delete_raises_error_for_local_only(self, reset_configuration: None) -> None:
        """Test delete() raises ValueError for local-only prompt."""
        messages = [Message(role=MessageRole.user, content="{{input}}")]
        prompt = Prompt(name="Test Prompt", messages=messages)

        with pytest.raises(ValueError, match="Prompt ID is not set"):
            prompt.delete()


class TestPromptRefresh:
    """Test suite for Prompt.refresh() method."""

    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_refresh_updates_attributes(self, mock_templates_class: MagicMock, reset_configuration: None) -> None:
        """Test refresh() updates all attributes from the API."""
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service

        prompt_id = str(uuid4())
        initial_version = MagicMock()
        initial_version.template = [MessagesListItem(role="user", content="{{input}}")]
        initial_version.version = 1

        initial = MagicMock()
        initial.id = prompt_id
        initial.name = "Test Prompt"
        initial.created_at = MagicMock()
        initial.updated_at = MagicMock()
        initial.selected_version = initial_version

        updated_version = MagicMock()
        updated_version.template = [
            MessagesListItem(role="system", content="System"),
            MessagesListItem(role="user", content="{{input}}"),
        ]
        updated_version.version = 2

        updated = MagicMock()
        updated.id = prompt_id
        updated.name = "Test Prompt"
        updated.created_at = initial.created_at
        updated.updated_at = MagicMock()
        updated.selected_version = updated_version

        mock_service.get.side_effect = [initial, updated]

        prompt = Prompt.get(id=prompt_id)
        assert len(prompt.messages) == 1

        prompt.refresh()

        assert len(prompt.messages) == 2
        assert prompt.is_synced()

    def test_refresh_raises_error_for_local_only(self, reset_configuration: None) -> None:
        """Test refresh() raises ValueError for local-only prompt."""
        messages = [Message(role=MessageRole.user, content="{{input}}")]
        prompt = Prompt(name="Test Prompt", messages=messages)

        with pytest.raises(ValueError, match="Prompt ID is not set"):
            prompt.refresh()


class TestPromptMethods:
    """Test suite for other Prompt methods."""

    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_create_version(
        self, mock_templates_class: MagicMock, reset_configuration: None, mock_prompt: MagicMock
    ) -> None:
        """Test create_version() creates a new versioned prompt."""
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service

        new_prompt = MagicMock()
        new_prompt.id = str(uuid4())
        new_prompt.name = "Test Prompt-v123"
        new_prompt.created_at = MagicMock()
        new_prompt.updated_at = MagicMock()
        new_prompt.selected_version = mock_prompt.selected_version

        mock_service.get.return_value = mock_prompt
        mock_service.create.return_value = new_prompt

        prompt = Prompt.get(id=mock_prompt.id)
        new_version = prompt.create_version()

        assert new_version.id == new_prompt.id
        assert "-v" in new_version.name
        assert new_version.is_synced()

    def test_save_raises_not_implemented_error(self, reset_configuration: None) -> None:
        """Test save() raises NotImplementedError."""
        messages = [Message(role=MessageRole.user, content="{{input}}")]
        prompt = Prompt(name="Test Prompt", messages=messages)

        with pytest.raises(NotImplementedError, match="not yet implemented"):
            prompt.save()

    def test_str_and_repr(self, reset_configuration: None) -> None:
        """Test __str__ and __repr__ return expected formats."""
        messages = [
            Message(role=MessageRole.system, content="System"),
            Message(role=MessageRole.user, content="{{input}}"),
        ]
        prompt = Prompt(name="Test Prompt", messages=messages)
        prompt.id = "test-id-123"

        assert str(prompt) == "Prompt(name='Test Prompt', id='test-id-123')"
        assert "2 messages" in repr(prompt)
