import json
from http import HTTPStatus
from unittest.mock import ANY, Mock, patch

import pytest

from galileo import Message, MessageRole
from galileo.prompts import (
    PromptTemplateAPIException,
    create_prompt,
    create_prompt_template,
    delete_prompt,
    get_prompt,
    get_prompt_template,
    get_prompts,
    list_prompt_templates,
)
from galileo.resources.models import (
    BasePromptTemplateResponse,
    BasePromptTemplateVersionResponse,
    CreatePromptTemplateWithVersionRequestBody,
    HTTPValidationError,
    ListPromptTemplateParams,
    ListPromptTemplateResponse,
    ProjectDB,
    PromptTemplateNameFilter,
    PromptTemplateNameFilterOperator,
)
from galileo.resources.types import Response


def projects_response():
    project = ProjectDB.from_dict(
        {
            "created_by_user": {
                "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                "email": "andriisoldatenko@galileo.ai",
                "first_name": "Andrii",
                "last_name": "Soldatenko",
            },
            "created_at": "2025-03-03T21:17:44.232862+00:00",
            "created_by": "01ce18ac-3960-46e1-bb79-0e4965069add",
            "id": "e343ea54-4df3-4d0b-9bc5-7e8224be348f",
            "runs": [],
            "updated_at": "2025-03-03T21:17:44.232864+00:00",
            "bookmark": False,
            "name": "andrii-new-project",
            "permissions": [],
            "type": "gen_ai",
        }
    )
    return Response(
        content=json.dumps(project.to_dict()).encode("utf-8"),
        status_code=HTTPStatus.OK,
        headers={"Content-Type": "application/json"},
        parsed=[project],
    )


def prompt_template():
    return BasePromptTemplateResponse.from_dict(
        {
            "all_available_versions": [0],
            "id": "4793f4b9-eb56-4495-88a9-8cf57bfe737b",
            "max_version": 0,
            "name": "andrii-good-prompt",
            "created_at": "2025-03-03T21:17:44.232862+00:00",
            "updated_at": "2025-03-03T21:17:44.232862+00:00",
            "creator": {
                "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                "email": "andriisoldatenko@galileo.ai",
                "first_name": "Andrii",
                "last_name": "Soldatenko",
            },
            "permissions": [],
            "selected_version": {
                "id": "03487fd7-1032-4317-ac43-a68401c07ee9",
                "template": '[{"content":"you are a helpful assistant","role":"system"},{"content":"why is sky blue?","role":"user"}]',
                "version": 0,
                "lines_added": 2,
                "lines_edited": 0,
                "lines_removed": 0,
                "model_changed": False,
                "settings": {},
                "settings_changed": False,
                "created_at": "2025-03-03T21:17:44.232862+00:00",
                "updated_at": "2025-03-03T21:17:44.232862+00:00",
            },
            "selected_version_id": "03487fd7-1032-4317-ac43-a68401c07ee9",
            "template": '[{"content":"you are a helpful assistant","role":"system"},{"content":"why is sky blue?","role":"user"}]',
            "total_versions": 1,
            "all_versions": [
                {
                    "id": "03487fd7-1032-4317-ac43-a68401c07ee9",
                    "template": '[{"content":"you are a helpful assistant","role":"system"},{"content":"why is sky blue?","role":"user"}]',
                    "version": 0,
                    "lines_added": 2,
                    "lines_edited": 0,
                    "lines_removed": 0,
                    "model_changed": False,
                    "settings": {},
                    "settings_changed": False,
                    "created_at": "2025-03-03T21:17:44.232862+00:00",
                    "updated_at": "2025-03-03T21:17:44.232862+00:00",
                }
            ],
        }
    )


def global_prompt_template():
    return BasePromptTemplateResponse.from_dict(
        {
            "all_available_versions": [0, 1],
            "id": "global-template-id-123",
            "max_version": 1,
            "name": "global-helpful-assistant",
            "created_at": "2025-03-03T21:17:44.232862+00:00",
            "updated_at": "2025-03-03T21:17:44.232862+00:00",
            "creator": {
                "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                "email": "test@galileo.ai",
                "first_name": "Test",
                "last_name": "User",
            },
            "permissions": [],
            "selected_version": {
                "id": "global-version-id-456",
                "template": '[{"content":"you are a global helpful assistant","role":"system"}]',
                "version": 1,
                "lines_added": 1,
                "lines_edited": 0,
                "lines_removed": 0,
                "model_changed": False,
                "settings": {},
                "settings_changed": False,
                "created_at": "2025-03-03T21:17:44.232862+00:00",
                "updated_at": "2025-03-03T21:17:44.232862+00:00",
            },
            "selected_version_id": "global-version-id-456",
            "template": '[{"content":"you are a global helpful assistant","role":"system"}]',
            "total_versions": 2,
            "all_versions": [
                {
                    "id": "global-version-id-123",
                    "template": '[{"content":"you are a helpful assistant","role":"system"}]',
                    "version": 0,
                    "lines_added": 1,
                    "lines_edited": 0,
                    "lines_removed": 0,
                    "model_changed": False,
                    "settings": {},
                    "settings_changed": False,
                    "created_at": "2025-03-03T21:17:44.232862+00:00",
                    "updated_at": "2025-03-03T21:17:44.232862+00:00",
                },
                {
                    "id": "global-version-id-456",
                    "template": '[{"content":"you are a global helpful assistant","role":"system"}]',
                    "version": 1,
                    "lines_added": 1,
                    "lines_edited": 0,
                    "lines_removed": 0,
                    "model_changed": False,
                    "settings": {},
                    "settings_changed": False,
                    "created_at": "2025-03-03T21:17:44.232862+00:00",
                    "updated_at": "2025-03-03T21:17:44.232862+00:00",
                },
            ],
        }
    )


def global_prompt_template_version():
    return BasePromptTemplateVersionResponse.from_dict(
        {
            "id": "global-version-id-123",
            "template": '[{"content":"you are a helpful assistant","role":"system"}]',
            "version": 0,
            "lines_added": 1,
            "lines_edited": 0,
            "lines_removed": 0,
            "model_changed": False,
            "settings": {},
            "settings_changed": False,
            "created_at": "2025-03-03T21:17:44.232862+00:00",
            "updated_at": "2025-03-03T21:17:44.232862+00:00",
        }
    )


def global_templates_list_response():
    return ListPromptTemplateResponse.from_dict(
        {
            "templates": [
                {
                    "all_available_versions": [0, 1],
                    "id": "global-template-id-123",
                    "max_version": 1,
                    "name": "global-helpful-assistant",
                    "created_at": "2025-03-03T21:17:44.232862+00:00",
                    "updated_at": "2025-03-03T21:17:44.232862+00:00",
                    "creator": {
                        "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                        "email": "test@galileo.ai",
                        "first_name": "Test",
                        "last_name": "User",
                    },
                    "permissions": [],
                    "selected_version": {
                        "id": "global-version-id-456",
                        "template": '[{"content":"you are a global helpful assistant","role":"system"}]',
                        "version": 1,
                        "lines_added": 1,
                        "lines_edited": 0,
                        "lines_removed": 0,
                        "model_changed": False,
                        "settings": {},
                        "settings_changed": False,
                        "created_at": "2025-03-03T21:17:44.232862+00:00",
                        "updated_at": "2025-03-03T21:17:44.232862+00:00",
                    },
                    "selected_version_id": "global-version-id-456",
                    "template": '[{"content":"you are a global helpful assistant","role":"system"}]',
                    "total_versions": 2,
                    "all_versions": [
                        {
                            "id": "global-version-id-123",
                            "template": '[{"content":"you are a helpful assistant","role":"system"}]',
                            "version": 0,
                            "lines_added": 1,
                            "lines_edited": 0,
                            "lines_removed": 0,
                            "model_changed": False,
                            "settings": {},
                            "settings_changed": False,
                            "created_at": "2025-03-03T21:17:44.232862+00:00",
                            "updated_at": "2025-03-03T21:17:44.232862+00:00",
                        },
                        {
                            "id": "global-version-id-456",
                            "template": '[{"content":"you are a global helpful assistant","role":"system"}]',
                            "version": 1,
                            "lines_added": 1,
                            "lines_edited": 0,
                            "lines_removed": 0,
                            "model_changed": False,
                            "settings": {},
                            "settings_changed": False,
                            "created_at": "2025-03-03T21:17:44.232862+00:00",
                            "updated_at": "2025-03-03T21:17:44.232862+00:00",
                        },
                    ],
                }
            ],
            "limit": 100,
            "next_starting_token": None,
            "paginated": False,
            "starting_token": 0,
        }
    )


def empty_templates_list_response():
    """Create empty template list response."""
    return ListPromptTemplateResponse.from_dict(
        {"templates": [], "limit": 100, "next_starting_token": None, "paginated": False, "starting_token": 0}
    )


@patch("galileo.projects.get_projects_projects_get")
@patch("galileo.prompts.create_prompt_template_with_version_projects_project_id_templates_post")
def test_create_prompt(create_prompt_template_mock: Mock, get_projects_projects_get_mock: Mock):
    create_prompt_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=prompt_template()
    )
    get_projects_projects_get_mock.sync_detailed.return_value = projects_response()
    tmpl = create_prompt_template(
        name="andrii-good-prompt",
        project="andrii-new-project",
        messages=[
            Message(role=MessageRole.system, content="you are a helpful assistant"),
            Message(role=MessageRole.user, content="why is sky blue?"),
        ],
    )

    assert tmpl.name == "andrii-good-prompt"
    create_prompt_template_mock.sync_detailed.assert_called_once()
    get_projects_projects_get_mock.sync_detailed.assert_called_once()


@patch("galileo.projects.get_projects_projects_get")
@patch("galileo.prompts.create_prompt_template_with_version_projects_project_id_templates_post")
def test_create_prompt_bad_request(create_prompt_template_mock: Mock, get_projects_projects_get_mock: Mock):
    create_prompt_template_mock.sync_detailed.return_value = Response(
        content=b'{"detail":"Prompt template with name storyteller-prompt already exists (ID 3e3d48fa-0aae-433c-be2c-b3f7fb53c9e2)."}',
        status_code=HTTPStatus.BAD_REQUEST,
        headers={},
        parsed=None,
    )
    get_projects_projects_get_mock.sync_detailed.return_value = projects_response()
    with pytest.raises(PromptTemplateAPIException):
        create_prompt_template(
            name="andrii-good-prompt",
            project="andrii-new-project",
            messages=[
                Message(role=MessageRole.system, content="you are a helpful assistant"),
                Message(role=MessageRole.user, content="why is sky blue?"),
            ],
        )
    create_prompt_template_mock.sync_detailed.assert_called_once()
    get_projects_projects_get_mock.sync_detailed.assert_called_once()


@patch("galileo.projects.get_projects_projects_get")
@patch("galileo.prompts.get_project_templates_projects_project_id_templates_get")
def test_list_prompts(list_prompt_templates_mock: Mock, get_projects_projects_get_mock: Mock):
    list_prompt_templates_mock.sync.return_value = [prompt_template()]
    get_projects_projects_get_mock.sync_detailed.return_value = projects_response()
    templates = list_prompt_templates(project="andrii-new-project")

    assert len(templates) == 1
    assert templates[0].name == "andrii-good-prompt"

    list_prompt_templates_mock.sync.assert_called_once()
    get_projects_projects_get_mock.sync_detailed.assert_called_once()


@patch("galileo.projects.get_projects_projects_get")
@patch("galileo.prompts.get_project_templates_projects_project_id_templates_get")
def test_get_prompt_template_found(list_prompt_templates_mock: Mock, get_projects_projects_get_mock: Mock):
    """Test get_prompt_template when template exists."""
    list_prompt_templates_mock.sync.return_value = [prompt_template()]
    get_projects_projects_get_mock.sync_detailed.return_value = projects_response()

    template = get_prompt_template(name="andrii-good-prompt", project="andrii-new-project")

    assert template is not None
    assert template.name == "andrii-good-prompt"
    list_prompt_templates_mock.sync.assert_called_once()
    get_projects_projects_get_mock.sync_detailed.assert_called_once()


@patch("galileo.projects.get_projects_projects_get")
@patch("galileo.prompts.get_project_templates_projects_project_id_templates_get")
def test_get_prompt_template_not_found(list_prompt_templates_mock: Mock, get_projects_projects_get_mock: Mock):
    """Test get_prompt_template when template doesn't exist."""
    list_prompt_templates_mock.sync.return_value = [prompt_template()]  # Return a different template
    get_projects_projects_get_mock.sync_detailed.return_value = projects_response()

    template = get_prompt_template(name="nonexistent-template", project="andrii-new-project")

    assert template is None
    list_prompt_templates_mock.sync.assert_called_once()
    get_projects_projects_get_mock.sync_detailed.assert_called_once()


@patch("galileo.prompts.create_global_prompt_template_templates_post")
def test_create_global_prompt_template(create_global_prompt_template_mock: Mock):
    create_global_prompt_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=global_prompt_template()
    )

    template = create_prompt(
        name="global-helpful-assistant",
        template=[Message(role=MessageRole.system, content="you are a global helpful assistant")],
    )

    assert template is not None
    assert template.name == "global-helpful-assistant"
    assert template.id == "global-template-id-123"
    create_global_prompt_template_mock.sync_detailed.assert_called_once_with(
        client=ANY,
        body=CreatePromptTemplateWithVersionRequestBody(
            name="global-helpful-assistant",
            template=[Message(role=MessageRole.system, content="you are a global helpful assistant")],
        ),
    )


@patch("galileo.prompts.create_global_prompt_template_templates_post")
def test_create_global_prompt_template_error_scenarios(create_global_prompt_template_mock: Mock):
    """Test create_global_prompt_template with realistic error scenarios."""

    # Test 422 Unprocessable Entity for missing fields, invalid data types, etc.
    create_global_prompt_template_mock.sync_detailed.return_value = Response(
        content=b'{"detail":[{"loc":["body","name"],"msg":"field required","type":"value_error.missing"}]}',
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        headers={},
        parsed=HTTPValidationError(),
    )

    with pytest.raises(PromptTemplateAPIException) as exc_info:
        create_prompt(name="test-template", template=[Message(role=MessageRole.system, content="test content")])
    assert "field required" in str(exc_info.value)

    # Test 500 Internal Server Error
    create_global_prompt_template_mock.sync_detailed.return_value = Response(
        content=b'{"detail":"Internal server error"}',
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        headers={},
        parsed=None,
    )

    with pytest.raises(PromptTemplateAPIException) as exc_info:
        create_prompt(name="test-template", template=[Message(role=MessageRole.system, content="test content")])
    assert "Internal server error" in str(exc_info.value)

    assert create_global_prompt_template_mock.sync_detailed.call_count == 2


@patch("galileo.prompts.get_global_template_templates_template_id_get")
def test_get_global_prompt_template_by_id(get_global_template_mock: Mock):
    get_global_template_mock.sync.return_value = global_prompt_template()

    version = get_prompt(id="global-template-id-123")

    assert version is not None
    assert version.id == "global-version-id-456"
    assert version.version == 1
    get_global_template_mock.sync.assert_called_once_with(template_id="global-template-id-123", client=ANY)


@patch("galileo.prompts.query_templates_templates_query_post")
def test_get_global_prompt_template_by_name(query_templates_mock: Mock):
    query_templates_mock.sync.return_value = global_templates_list_response()

    version = get_prompt(name="global-helpful-assistant")

    assert version is not None
    assert version.id == "global-version-id-456"
    assert version.version == 1
    query_templates_mock.sync.assert_called_once()


@patch("galileo.prompts.get_global_template_templates_template_id_get")
def test_get_global_prompt_template_by_id_not_found(get_global_template_mock: Mock):
    get_global_template_mock.sync.return_value = None

    template = get_prompt(id="nonexistent-id")

    assert template is None
    get_global_template_mock.sync.assert_called_once()


@patch("galileo.prompts.query_templates_templates_query_post")
def test_get_global_prompt_template_by_name_not_found(query_templates_mock: Mock):
    query_templates_mock.sync.return_value = empty_templates_list_response()

    template = get_prompt(name="nonexistent-template")

    assert template is None
    query_templates_mock.sync.assert_called_once()


def test_get_global_prompt_template_validation_errors():
    with pytest.raises(ValueError) as exc_info:
        get_prompt()
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"

    with pytest.raises(ValueError) as exc_info:
        get_prompt(id="id", name="name")
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"


@patch("galileo.prompts.get_global_template_version_templates_template_id_versions_version_get")
def test_get_global_prompt_template_version(get_global_template_version_mock: Mock):
    get_global_template_version_mock.sync.return_value = global_prompt_template_version()

    version = get_prompt(id="global-template-id-123", version=0)

    assert version is not None
    assert version.id == "global-version-id-123"
    assert version.version == 0
    assert version.template == '[{"content":"you are a helpful assistant","role":"system"}]'
    get_global_template_version_mock.sync.assert_called_once_with(
        template_id="global-template-id-123", version=0, client=ANY
    )


@patch("galileo.prompts.get_global_template_version_templates_template_id_versions_version_get")
def test_get_global_prompt_template_version_not_found(get_global_template_version_mock: Mock):
    get_global_template_version_mock.sync.return_value = None

    version = get_prompt(id="global-template-id-123", version=99)

    assert version is None
    get_global_template_version_mock.sync.assert_called_once()


@patch("galileo.prompts.query_templates_templates_query_post")
def test_list_global_prompt_templates(query_templates_mock: Mock):
    query_templates_mock.sync.return_value = global_templates_list_response()

    templates = get_prompts()

    assert len(templates) == 1
    assert templates[0].name == "global-helpful-assistant"
    assert templates[0].id == "global-template-id-123"
    query_templates_mock.sync.assert_called_once()


@patch("galileo.prompts.query_templates_templates_query_post")
def test_list_global_prompt_templates_with_filter(query_templates_mock: Mock):
    query_templates_mock.sync.return_value = global_templates_list_response()

    templates = get_prompts(name_filter="global-helpful", limit=50)

    assert len(templates) == 1
    assert templates[0].name == "global-helpful-assistant"
    query_templates_mock.sync.assert_called_once_with(
        client=ANY,
        body=ListPromptTemplateParams(
            filters=[
                PromptTemplateNameFilter(operator=PromptTemplateNameFilterOperator.CONTAINS, value="global-helpful")
            ]
        ),
        limit=50,
        starting_token=0,
    )


@patch("galileo.prompts.query_templates_templates_query_post")
@pytest.mark.parametrize("response_value", [HTTPValidationError(), None])
def test_list_global_prompt_templates_with_error_responses(query_templates_mock: Mock, response_value):
    """Test list_global_prompt_templates when API returns HTTPValidationError or None."""
    query_templates_mock.sync.return_value = response_value

    templates = get_prompts()

    assert len(templates) == 0
    query_templates_mock.sync.assert_called_once()


@patch("galileo.prompts.query_templates_templates_query_post")
def test_list_global_prompt_templates_empty(query_templates_mock: Mock):
    query_templates_mock.sync.return_value = empty_templates_list_response()

    templates = get_prompts()

    assert len(templates) == 0
    query_templates_mock.sync.assert_called_once()


@patch("galileo.prompts.delete_global_template_templates_template_id_delete")
def test_delete_global_prompt_template_by_id(delete_global_template_mock: Mock):
    delete_global_template_mock.sync.return_value = None

    delete_prompt(id="global-template-id-123")

    delete_global_template_mock.sync.assert_called_once_with(client=ANY, template_id="global-template-id-123")


@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.prompts.delete_global_template_templates_template_id_delete")
def test_delete_global_prompt_template_by_name(delete_global_template_mock: Mock, query_templates_mock: Mock):
    query_templates_mock.sync.return_value = global_templates_list_response()
    delete_global_template_mock.sync.return_value = None

    delete_prompt(name="global-helpful-assistant")

    query_templates_mock.sync.assert_called_once()
    delete_global_template_mock.sync.assert_called_once_with(client=ANY, template_id="global-template-id-123")


@patch("galileo.prompts.query_templates_templates_query_post")
def test_delete_global_prompt_template_by_name_not_found(query_templates_mock: Mock):
    query_templates_mock.sync.return_value = empty_templates_list_response()

    with pytest.raises(ValueError) as exc_info:
        delete_prompt(name="nonexistent-template")

    assert "Global template 'nonexistent-template' not found" in str(exc_info.value)
    query_templates_mock.sync.assert_called_once()


def test_delete_global_prompt_template_validation_errors():
    """Test all validation error scenarios for delete_global_prompt_template."""
    with pytest.raises(ValueError) as exc_info:
        delete_prompt()
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"

    with pytest.raises(ValueError) as exc_info:
        delete_prompt(id="id", name="name")
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"

    with pytest.raises(ValueError) as exc_info:
        delete_prompt(id=None, name=None)
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"
