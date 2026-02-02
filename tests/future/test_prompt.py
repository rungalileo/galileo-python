from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from galileo.__future__ import Prompt
from galileo.__future__.prompt import PromptVersion, _parse_template_to_messages
from galileo.__future__.shared.base import SyncState
from galileo.__future__.shared.exceptions import ValidationError
from galileo.resources.models.messages_list_item import MessagesListItem
from galileo.schema.message import Message
from galileo_core.schemas.logging.llm import MessageRole


class TestPromptInitialization:
    """Test suite for Prompt initialization."""

    def test_init_with_name_and_messages(self, reset_configuration: None) -> None:
        """Test initializing a prompt with name and messages creates a local-only instance."""
        # Given: valid name and messages
        messages = [
            Message(role=MessageRole.system, content="You are a helpful assistant."),
            Message(role=MessageRole.user, content="{{input}}"),
        ]

        # When: creating a new prompt
        prompt = Prompt(name="Test Prompt", messages=messages)

        # Then: the prompt is created with correct attributes
        assert prompt.name == "Test Prompt"
        assert prompt.messages == messages
        assert prompt.id is None
        assert prompt.sync_state == SyncState.LOCAL_ONLY
        # Version attributes should be None for local-only prompts
        assert prompt.selected_version_number is None
        assert prompt.selected_version_id is None
        assert prompt.total_versions is None
        assert prompt.all_available_versions is None
        assert prompt.max_version is None
        # Project attributes should be None
        assert prompt.project_id is None
        assert prompt.project_name is None

    def test_init_with_project_params(self, reset_configuration: None) -> None:
        """Test initializing a prompt with project parameters stores them."""
        # Given: valid name, messages, and project info
        messages = [Message(role=MessageRole.user, content="{{input}}")]
        project_id = str(uuid4())

        # When: creating a new prompt with project params
        prompt = Prompt(name="Test Prompt", messages=messages, project_id=project_id, project_name="Test Project")

        # Then: the project attributes are set
        assert prompt.project_id == project_id
        assert prompt.project_name == "Test Project"

    @pytest.mark.parametrize(
        "name,messages", [(None, [Message(role=MessageRole.user, content="{{input}}")]), ("Test Prompt", None)]
    )
    def test_init_without_required_fields_raises_error(
        self, name: str, messages: list, reset_configuration: None
    ) -> None:
        """Test initializing a prompt without required fields raises ValidationError."""
        # When/Then: creating a prompt without required fields raises ValidationError
        with pytest.raises(ValidationError, match="'name' and 'messages' must be provided"):
            Prompt(name=name, messages=messages)


class TestPromptCreate:
    """Test suite for Prompt.create() method."""

    @patch("galileo.__future__.prompt.Projects")
    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_create_persists_prompt_to_api(
        self,
        mock_templates_class: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_prompt: MagicMock,
    ) -> None:
        """Test create() persists the prompt to the API and updates attributes."""
        # Given: mocked services and a valid prompt
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service
        mock_service.create.return_value = mock_prompt

        mock_projects_instance = MagicMock()
        mock_projects_class.return_value = mock_projects_instance
        mock_projects_instance.get_with_env_fallbacks.return_value = None

        messages = [Message(role=MessageRole.user, content="{{input}}")]

        # When: creating the prompt
        prompt = Prompt(name="Test Prompt", messages=messages).create()

        # Then: the prompt is persisted with correct parameters
        mock_service.create.assert_called_once_with(name="Test Prompt", template=messages, project_id=None)
        assert prompt.id == mock_prompt.id
        assert prompt.is_synced()
        # Version attributes should be populated
        assert prompt.selected_version_number == 1
        assert prompt.total_versions == 1

    @patch("galileo.__future__.prompt.Projects")
    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_create_with_project_association(
        self,
        mock_templates_class: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_prompt: MagicMock,
        mock_project: MagicMock,
    ) -> None:
        """Test create() passes project_id to the API when project is specified."""
        # Given: mocked services with a resolved project
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service
        mock_service.create.return_value = mock_prompt

        mock_projects_instance = MagicMock()
        mock_projects_class.return_value = mock_projects_instance
        mock_projects_instance.get_with_env_fallbacks.return_value = mock_project

        messages = [Message(role=MessageRole.user, content="{{input}}")]

        # When: creating the prompt with project_name
        prompt = Prompt(name="Test Prompt", messages=messages, project_name="Test Project").create()

        # Then: the project_id is passed to the API
        mock_projects_instance.get_with_env_fallbacks.assert_called_once_with(id=None, name="Test Project")
        mock_service.create.assert_called_once_with(name="Test Prompt", template=messages, project_id=mock_project.id)
        assert prompt.is_synced()

        # And: the prompt has the resolved project info
        assert prompt.project_id == mock_project.id
        assert prompt.project_name == mock_project.name

    @patch("galileo.__future__.prompt.Projects")
    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_create_handles_api_failure(
        self, mock_templates_class: MagicMock, mock_projects_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test create() handles API failures and sets state correctly."""
        # Given: mocked services that return an error
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service
        mock_service.create.side_effect = Exception("API Error")

        mock_projects_instance = MagicMock()
        mock_projects_class.return_value = mock_projects_instance
        mock_projects_instance.get_with_env_fallbacks.return_value = None

        messages = [Message(role=MessageRole.user, content="{{input}}")]
        prompt = Prompt(name="Test Prompt", messages=messages)

        # When/Then: create fails with an exception
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
    def test_update_name(
        self, mock_templates_class: MagicMock, reset_configuration: None, mock_prompt: MagicMock
    ) -> None:
        """Test update() updates the prompt name."""
        # Given: a synced prompt
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

        # When: updating the name
        result = prompt.update(name="New Name")

        # Then: the name is updated via the API and returns self for chaining
        mock_service.update.assert_called_once_with(template_id=mock_prompt.id, name="New Name")
        assert prompt.name == "New Name"
        assert prompt.is_synced()
        assert result is prompt

    def test_update_raises_error_for_local_only(self, reset_configuration: None) -> None:
        """Test update() raises ValueError for local-only prompt."""
        # Given: a local-only prompt
        messages = [Message(role=MessageRole.user, content="{{input}}")]
        prompt = Prompt(name="Test Prompt", messages=messages)

        # When/Then: updating raises ValueError
        with pytest.raises(ValueError, match="Prompt ID is not set"):
            prompt.update(name="New Name")


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

    @patch("galileo.__future__.prompt.GalileoPythonConfig")
    @patch("galileo.__future__.prompt.set_selected_global_template_version_templates_template_id_versions_version_put")
    @patch("galileo.__future__.prompt.create_global_prompt_template_version_templates_template_id_versions_post")
    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_create_version_creates_actual_version(
        self,
        mock_templates_class: MagicMock,
        mock_create_version_api: MagicMock,
        mock_select_version_api: MagicMock,
        mock_config: MagicMock,
        reset_configuration: None,
        mock_prompt: MagicMock,
        mock_prompt_version: MagicMock,
    ) -> None:
        """Test create_version() creates a new version and selects it."""
        # Given: a synced prompt
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service
        mock_service.get.return_value = mock_prompt

        mock_config.get.return_value = MagicMock()
        mock_prompt_version.version = 2
        mock_create_version_api.sync.return_value = mock_prompt_version

        # Mock for select_version call - update mock_prompt for the second get call
        updated_mock_prompt = MagicMock()
        updated_mock_prompt.id = mock_prompt.id
        updated_mock_prompt.name = mock_prompt.name
        updated_mock_prompt.selected_version = MagicMock()
        updated_mock_prompt.selected_version.version = 2
        # Use MagicMock objects for template items to match expected interface
        template_item = MagicMock()
        template_item.role = "user"
        template_item.content = "test"
        updated_mock_prompt.selected_version.template = [template_item]
        updated_mock_prompt.selected_version_id = "version-2-id"
        updated_mock_prompt.total_versions = 2
        updated_mock_prompt.all_available_versions = [1, 2]
        updated_mock_prompt.max_version = 2
        updated_mock_prompt.created_at = mock_prompt.created_at
        updated_mock_prompt.updated_at = mock_prompt.updated_at

        mock_select_version_api.sync.return_value = updated_mock_prompt

        prompt = Prompt.get(id=mock_prompt.id)

        # When: creating a new version
        result = prompt.create_version()

        # Then: API is called to create version and select it
        mock_create_version_api.sync.assert_called_once()
        mock_select_version_api.sync.assert_called_once()
        assert result is prompt  # Returns same instance
        assert prompt.is_synced()
        assert prompt.selected_version_number == 2

    @patch("galileo.__future__.prompt.GalileoPythonConfig")
    @patch("galileo.__future__.prompt.set_selected_global_template_version_templates_template_id_versions_version_put")
    @patch("galileo.__future__.prompt.create_global_prompt_template_version_templates_template_id_versions_post")
    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_create_version_with_new_messages(
        self,
        mock_templates_class: MagicMock,
        mock_create_version_api: MagicMock,
        mock_select_version_api: MagicMock,
        mock_config: MagicMock,
        reset_configuration: None,
        mock_prompt: MagicMock,
        mock_prompt_version: MagicMock,
    ) -> None:
        """Test create_version() with new messages passes them to API and selects the new version."""
        # Given: a synced prompt
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service
        mock_service.get.return_value = mock_prompt

        mock_config.get.return_value = MagicMock()
        mock_prompt_version.version = 2
        mock_create_version_api.sync.return_value = mock_prompt_version

        # Mock for select_version call
        updated_mock_prompt = MagicMock()
        updated_mock_prompt.id = mock_prompt.id
        updated_mock_prompt.name = mock_prompt.name
        updated_mock_prompt.selected_version = MagicMock()
        updated_mock_prompt.selected_version.version = 2
        # Use MagicMock objects for template items to match expected interface
        template_item = MagicMock()
        template_item.role = "system"
        template_item.content = "New system message"
        updated_mock_prompt.selected_version.template = [template_item]
        updated_mock_prompt.selected_version_id = "version-2-id"
        updated_mock_prompt.total_versions = 2
        updated_mock_prompt.all_available_versions = [1, 2]
        updated_mock_prompt.max_version = 2
        updated_mock_prompt.created_at = mock_prompt.created_at
        updated_mock_prompt.updated_at = mock_prompt.updated_at

        mock_select_version_api.sync.return_value = updated_mock_prompt

        prompt = Prompt.get(id=mock_prompt.id)

        # When: creating a version with new messages
        new_messages = [Message(role=MessageRole.system, content="New system message")]
        prompt.create_version(messages=new_messages)

        # Then: API is called with the new messages and version is selected
        mock_create_version_api.sync.assert_called_once()
        call_kwargs = mock_create_version_api.sync.call_args
        assert call_kwargs.kwargs["template_id"] == mock_prompt.id
        mock_select_version_api.sync.assert_called_once()
        assert prompt.selected_version_number == 2

    def test_create_version_raises_error_for_local_only(self, reset_configuration: None) -> None:
        """Test create_version() raises ValueError for local-only prompt."""
        # Given: a local-only prompt
        messages = [Message(role=MessageRole.user, content="{{input}}")]
        prompt = Prompt(name="Test Prompt", messages=messages)

        # When/Then: creating version raises ValueError
        with pytest.raises(ValueError, match="Prompt ID is not set"):
            prompt.create_version()

    @patch("galileo.__future__.prompt.Projects")
    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_save_creates_prompt_when_local_only(
        self,
        mock_templates_class: MagicMock,
        mock_projects_class: MagicMock,
        reset_configuration: None,
        mock_prompt: MagicMock,
    ) -> None:
        """Test save() creates the prompt when in LOCAL_ONLY state."""
        # Given: a local-only prompt and mocked services
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service
        mock_service.create.return_value = mock_prompt

        mock_projects_instance = MagicMock()
        mock_projects_class.return_value = mock_projects_instance
        mock_projects_instance.get_with_env_fallbacks.return_value = None

        messages = [Message(role=MessageRole.user, content="{{input}}")]
        prompt = Prompt(name="Test Prompt", messages=messages)

        # When: saving the prompt
        result = prompt.save()

        # Then: the prompt is created
        mock_service.create.assert_called_once()
        assert result is prompt
        assert prompt.is_synced()

    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_save_returns_self_when_already_synced(
        self, mock_templates_class: MagicMock, reset_configuration: None, mock_prompt: MagicMock
    ) -> None:
        """Test save() returns self without action when already synced."""
        # Given: a synced prompt
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service
        mock_service.get.return_value = mock_prompt

        prompt = Prompt.get(id=mock_prompt.id)

        # When: saving the already synced prompt
        result = prompt.save()

        # Then: no create/update is called, returns self
        mock_service.create.assert_not_called()
        mock_service.update.assert_not_called()
        assert result is prompt

    def test_save_raises_error_for_deleted_prompt(self, reset_configuration: None) -> None:
        """Test save() raises ValueError for deleted prompt."""
        # Given: a prompt marked as deleted
        messages = [Message(role=MessageRole.user, content="{{input}}")]
        prompt = Prompt(name="Test Prompt", messages=messages)
        prompt._set_state(SyncState.DELETED)

        # When/Then: save raises ValueError
        with pytest.raises(ValueError, match="Cannot save a deleted prompt"):
            prompt.save()

    def test_str_and_repr(self, reset_configuration: None) -> None:
        """Test __str__ and __repr__ return expected formats."""
        # Given: a prompt with messages
        messages = [
            Message(role=MessageRole.system, content="System"),
            Message(role=MessageRole.user, content="{{input}}"),
        ]
        prompt = Prompt(name="Test Prompt", messages=messages)
        prompt.id = "test-id-123"

        # Then: str and repr return expected formats
        assert str(prompt) == "Prompt(name='Test Prompt', id='test-id-123')"
        assert "2 messages" in repr(prompt)

    def test_repr_includes_version_when_available(self, reset_configuration: None) -> None:
        """Test __repr__ includes version number when available."""
        # Given: a prompt with version info
        messages = [Message(role=MessageRole.user, content="{{input}}")]
        prompt = Prompt(name="Test Prompt", messages=messages)
        prompt.id = "test-id-123"
        prompt.selected_version_number = 3

        # Then: repr includes version
        assert "version=3" in repr(prompt)


class TestJsonTemplateParsing:
    """Test suite for JSON string template parsing."""

    def test_parse_template_from_list(self) -> None:
        """Test _parse_template_to_messages with list input."""
        # Given: a list of MessagesListItem objects
        template = [
            MessagesListItem(role="system", content="System message"),
            MessagesListItem(role="user", content="{{input}}"),
        ]

        # When: parsing the template
        messages = _parse_template_to_messages(template)

        # Then: messages are correctly parsed
        assert len(messages) == 2
        assert messages[0].role == MessageRole.system
        assert messages[0].content == "System message"
        assert messages[1].role == MessageRole.user
        assert messages[1].content == "{{input}}"

    def test_parse_template_from_json_string(self) -> None:
        """Test _parse_template_to_messages with JSON string input."""
        # Given: a JSON string containing messages array
        template = '[{"role": "system", "content": "System message"}, {"role": "user", "content": "{{input}}"}]'

        # When: parsing the template
        messages = _parse_template_to_messages(template)

        # Then: messages are correctly parsed from JSON
        assert len(messages) == 2
        assert messages[0].role == MessageRole.system
        assert messages[0].content == "System message"
        assert messages[1].role == MessageRole.user
        assert messages[1].content == "{{input}}"

    def test_parse_template_from_plain_string(self) -> None:
        """Test _parse_template_to_messages with plain string input."""
        # Given: a plain string template
        template = "Tell me about {{topic}}"

        # When: parsing the template
        messages = _parse_template_to_messages(template)

        # Then: string is wrapped in a single user message
        assert len(messages) == 1
        assert messages[0].role == MessageRole.user
        assert messages[0].content == "Tell me about {{topic}}"

    def test_parse_template_with_invalid_json(self) -> None:
        """Test _parse_template_to_messages with invalid JSON string."""
        # Given: an invalid JSON string
        template = "{not valid json}"

        # When: parsing the template
        messages = _parse_template_to_messages(template)

        # Then: string is treated as plain text
        assert len(messages) == 1
        assert messages[0].role == MessageRole.user
        assert messages[0].content == "{not valid json}"

    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_get_parses_json_string_template_correctly(
        self, mock_templates_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test Prompt.get() correctly parses JSON string templates from API."""
        # Given: API returns template as JSON string
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service

        mock_version = MagicMock()
        mock_version.template = (
            '[{"role": "system", "content": "You are helpful"}, {"role": "user", "content": "{{input}}"}]'
        )
        mock_version.version = 1
        mock_version.id = str(uuid4())

        mock_pmt = MagicMock()
        mock_pmt.id = str(uuid4())
        mock_pmt.name = "Test Prompt"
        mock_pmt.created_at = MagicMock()
        mock_pmt.updated_at = MagicMock()
        mock_pmt.selected_version = mock_version
        mock_pmt.selected_version_id = mock_version.id
        mock_pmt.total_versions = 1
        mock_pmt.all_available_versions = [1]
        mock_pmt.max_version = 1

        mock_service.get.return_value = mock_pmt

        # When: getting the prompt
        prompt = Prompt.get(id=mock_pmt.id)

        # Then: messages are correctly parsed from JSON string
        assert len(prompt.messages) == 2
        assert prompt.messages[0].role == MessageRole.system
        assert prompt.messages[0].content == "You are helpful"
        assert prompt.messages[1].role == MessageRole.user


class TestVersionManagement:
    """Test suite for version management methods."""

    @patch("galileo.__future__.prompt.GalileoPythonConfig")
    @patch("galileo.__future__.prompt.query_template_versions_templates_template_id_versions_query_post")
    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_list_versions_returns_version_objects(
        self,
        mock_templates_class: MagicMock,
        mock_query_api: MagicMock,
        mock_config: MagicMock,
        reset_configuration: None,
        mock_prompt: MagicMock,
    ) -> None:
        """Test list_versions() returns list of PromptVersion objects."""
        # Given: a synced prompt with multiple versions
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service
        mock_service.get.return_value = mock_prompt

        mock_config.get.return_value = MagicMock()

        mock_v1 = MagicMock()
        mock_v1.id = str(uuid4())
        mock_v1.version = 1
        mock_v1.template = [MessagesListItem(role="user", content="v1")]

        mock_v2 = MagicMock()
        mock_v2.id = str(uuid4())
        mock_v2.version = 2
        mock_v2.template = [MessagesListItem(role="user", content="v2")]

        mock_response = MagicMock()
        mock_response.versions = [mock_v1, mock_v2]
        mock_query_api.sync.return_value = mock_response

        prompt = Prompt.get(id=mock_prompt.id)

        # When: listing versions
        versions = prompt.list_versions()

        # Then: returns list of PromptVersion objects
        assert len(versions) == 2
        assert all(isinstance(v, PromptVersion) for v in versions)
        assert versions[0].version == 1
        assert versions[1].version == 2

    def test_list_versions_raises_error_for_local_only(self, reset_configuration: None) -> None:
        """Test list_versions() raises ValueError for local-only prompt."""
        # Given: a local-only prompt
        messages = [Message(role=MessageRole.user, content="{{input}}")]
        prompt = Prompt(name="Test Prompt", messages=messages)

        # When/Then: listing versions raises ValueError
        with pytest.raises(ValueError, match="Prompt ID is not set"):
            prompt.list_versions()

    @patch("galileo.__future__.prompt.GalileoPythonConfig")
    @patch("galileo.__future__.prompt.set_selected_global_template_version_templates_template_id_versions_version_put")
    @patch("galileo.__future__.prompt.GlobalPromptTemplates")
    def test_select_version_sets_active_version(
        self,
        mock_templates_class: MagicMock,
        mock_select_api: MagicMock,
        mock_config: MagicMock,
        reset_configuration: None,
        mock_prompt: MagicMock,
    ) -> None:
        """Test select_version() sets a version as active."""
        # Given: a synced prompt
        mock_service = MagicMock()
        mock_templates_class.return_value = mock_service
        mock_service.get.return_value = mock_prompt

        mock_config.get.return_value = MagicMock()

        # Create updated response
        updated_prompt = MagicMock()
        updated_prompt.id = mock_prompt.id
        updated_prompt.name = mock_prompt.name
        updated_prompt.selected_version = MagicMock()
        updated_prompt.selected_version.version = 2
        updated_prompt.selected_version.template = [MessagesListItem(role="user", content="v2")]
        updated_prompt.selected_version_id = str(uuid4())
        updated_prompt.total_versions = 2
        updated_prompt.all_available_versions = [1, 2]
        updated_prompt.max_version = 2
        updated_prompt.created_at = mock_prompt.created_at
        updated_prompt.updated_at = MagicMock()

        mock_select_api.sync.return_value = updated_prompt

        prompt = Prompt.get(id=mock_prompt.id)

        # When: selecting version 2
        result = prompt.select_version(2)

        # Then: version is selected and prompt is updated
        mock_select_api.sync.assert_called_once()
        assert result is prompt
        assert prompt.selected_version_number == 2
        assert prompt.is_synced()

    def test_select_version_raises_error_for_local_only(self, reset_configuration: None) -> None:
        """Test select_version() raises ValueError for local-only prompt."""
        # Given: a local-only prompt
        messages = [Message(role=MessageRole.user, content="{{input}}")]
        prompt = Prompt(name="Test Prompt", messages=messages)

        # When/Then: selecting version raises ValueError
        with pytest.raises(ValueError, match="Prompt ID is not set"):
            prompt.select_version(1)


class TestPromptVersionClass:
    """Test suite for PromptVersion class."""

    def test_from_api_response(self, mock_prompt_version: MagicMock) -> None:
        """Test PromptVersion._from_api_response creates correct instance."""
        # When: creating from API response
        version = PromptVersion._from_api_response(mock_prompt_version)

        # Then: attributes are correctly set
        assert version.id == mock_prompt_version.id
        assert version.version == mock_prompt_version.version
        assert isinstance(version.messages, list)

    def test_str_and_repr(self, mock_prompt_version: MagicMock) -> None:
        """Test PromptVersion __str__ and __repr__."""
        # Given: a PromptVersion instance
        version = PromptVersion._from_api_response(mock_prompt_version)

        # Then: str and repr return expected formats
        assert f"version={mock_prompt_version.version}" in str(version)
        assert "messages" in repr(version)
