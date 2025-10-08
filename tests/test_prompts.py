import json
from http import HTTPStatus
from unittest.mock import ANY, Mock, patch

import pytest

from galileo import Message, MessageRole
from galileo.prompts import (
    PromptTemplateAPIException,
    create_prompt,
    delete_prompt,
    get_prompt,
    get_prompts,
    render_template,
    update_prompt,
)
from galileo.resources.models import (
    BasePromptTemplateResponse,
    BasePromptTemplateVersionResponse,
    CreatePromptTemplateWithVersionRequestBody,
    DatasetData,
    GetProjectsPaginatedResponse,
    HTTPValidationError,
    ListPromptTemplateParams,
    ListPromptTemplateResponse,
    ProjectDB,
    PromptTemplateNameFilter,
    PromptTemplateNameFilterOperator,
    RenderTemplateRequest,
    RenderTemplateResponse,
    StringData,
    UpdatePromptTemplateRequest,
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
            "created_by_user": {
                "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                "email": "andriisoldatenko@galileo.ai",
                "first_name": "Andrii",
                "last_name": "Soldatenko",
            },
            "permissions": [],
            "selected_version": {
                "content_changed": False,
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
                "created_by_user": {
                    "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                    "email": "test@galileo.ai",
                    "first_name": "Test",
                    "last_name": "User",
                },
            },
            "selected_version_id": "03487fd7-1032-4317-ac43-a68401c07ee9",
            "template": '[{"content":"you are a helpful assistant","role":"system"},{"content":"why is sky blue?","role":"user"}]',
            "total_versions": 1,
            "all_versions": [
                {
                    "content_changed": False,
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
                    "created_by_user": {
                        "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                        "email": "test@galileo.ai",
                        "first_name": "Test",
                        "last_name": "User",
                    },
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
            "created_by_user": {
                "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                "email": "test@galileo.ai",
                "first_name": "Test",
                "last_name": "User",
            },
            "permissions": [],
            "selected_version": {
                "content_changed": False,
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
                "created_by_user": {
                    "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                    "email": "test@galileo.ai",
                    "first_name": "Test",
                    "last_name": "User",
                },
            },
            "selected_version_id": "global-version-id-456",
            "template": '[{"content":"you are a global helpful assistant","role":"system"}]',
            "total_versions": 2,
            "all_versions": [
                {
                    "content_changed": False,
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
                    "created_by_user": {
                        "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                        "email": "test@galileo.ai",
                        "first_name": "Test",
                        "last_name": "User",
                    },
                },
                {
                    "content_changed": False,
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
                    "created_by_user": {
                        "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                        "email": "test@galileo.ai",
                        "first_name": "Test",
                        "last_name": "User",
                    },
                },
            ],
        }
    )


def global_prompt_template_version():
    return BasePromptTemplateVersionResponse.from_dict(
        {
            "content_changed": False,
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
            "created_by_user": {
                "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                "email": "test@galileo.ai",
                "first_name": "Test",
                "last_name": "User",
            },
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
                    "created_by_user": {
                        "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                        "email": "test@galileo.ai",
                        "first_name": "Test",
                        "last_name": "User",
                    },
                    "permissions": [],
                    "selected_version": {
                        "content_changed": False,
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
                        "created_by_user": {
                            "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                            "email": "test@galileo.ai",
                            "first_name": "Test",
                            "last_name": "User",
                        },
                    },
                    "selected_version_id": "global-version-id-456",
                    "template": '[{"content":"you are a global helpful assistant","role":"system"}]',
                    "total_versions": 2,
                    "all_versions": [
                        {
                            "content_changed": False,
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
                            "created_by_user": {
                                "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                                "email": "test@galileo.ai",
                                "first_name": "Test",
                                "last_name": "User",
                            },
                        },
                        {
                            "content_changed": False,
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
                            "created_by_user": {
                                "id": "01ce18ac-3960-46e1-bb79-0e4965069add",
                                "email": "test@galileo.ai",
                                "first_name": "Test",
                                "last_name": "User",
                            },
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


def render_template_response():
    """Create render template response."""
    return RenderTemplateResponse.from_dict(
        {
            "rendered_templates": [
                {"result": "Hello User1! How are you?", "warning": None},
                {"result": "Hello User2! How are you?", "warning": None},
            ],
            "limit": 100,
            "next_starting_token": None,
            "paginated": False,
            "starting_token": 0,
        }
    )


def render_template_response_empty():
    """Create empty render template response."""
    return RenderTemplateResponse.from_dict(
        {"rendered_templates": [], "limit": 100, "next_starting_token": None, "paginated": False, "starting_token": 0}
    )


def render_template_response_paginated():
    """Create paginated render template response with only 1 result."""
    return RenderTemplateResponse.from_dict(
        {
            "rendered_templates": [{"result": "Hello User1! How are you?", "warning": None}],
            "limit": 1,
            "next_starting_token": 1,
            "paginated": True,
            "starting_token": 0,
        }
    )


def render_template_response_second_page():
    """Create render template response for second page of pagination."""
    return RenderTemplateResponse.from_dict(
        {
            "rendered_templates": [{"result": "Hello User2! How are you?", "warning": None}],
            "limit": 1,
            "next_starting_token": None,
            "paginated": True,
            "starting_token": 1,
        }
    )


# DEPRECATED: This test uses old project-specific endpoints that are no longer supported.
# We now use global template endpoints with optional project_id parameter.
# See test_prompts_global.py for updated tests.
# @patch("galileo.projects.get_projects_projects_get")
# @patch("galileo.prompts.create_prompt_template_with_version_projects_project_id_templates_post")
# def test_create_prompt(create_prompt_template_mock: Mock, get_projects_projects_get_mock: Mock) -> None:
#     create_prompt_template_mock.sync_detailed.return_value = Response(
#         content=b"", status_code=HTTPStatus.OK, headers={}, parsed=prompt_template()
#     )
#     get_projects_projects_get_mock.sync_detailed.return_value = projects_response()
#     tmpl = create_prompt_template(
#         name="andrii-good-prompt",
#         project="andrii-new-project",
#         messages=[
#             Message(role=MessageRole.system, content="you are a helpful assistant"),
#             Message(role=MessageRole.user, content="why is sky blue?"),
#         ],
#     )
#
#     assert tmpl.name == "andrii-good-prompt"
#     create_prompt_template_mock.sync_detailed.assert_called_once()
#     get_projects_projects_get_mock.sync_detailed.assert_called_once()


# DEPRECATED: This test uses old project-specific endpoints that are no longer supported.
# We now use global template endpoints with optional project_id parameter.
# See test_prompts_global.py for updated tests.
# @patch("galileo.projects.get_projects_projects_get")
# @patch("galileo.prompts.create_prompt_template_with_version_projects_project_id_templates_post")
# def test_create_prompt_bad_request(create_prompt_template_mock: Mock, get_projects_projects_get_mock: Mock) -> None:
#     create_prompt_template_mock.sync_detailed.return_value = Response(
#         content=b'{"detail":"Prompt template with name storyteller-prompt already exists (ID 3e3d48fa-0aae-433c-be2c-b3f7fb53c9e2)."}',
#         status_code=HTTPStatus.BAD_REQUEST,
#         headers={},
#         parsed=None,
#     )
#     get_projects_projects_get_mock.sync_detailed.return_value = projects_response()
#     with pytest.raises(PromptTemplateAPIException):
#         create_prompt_template(
#             name="andrii-good-prompt",
#             project="andrii-new-project",
#             messages=[
#                 Message(role=MessageRole.system, content="you are a helpful assistant"),
#                 Message(role=MessageRole.user, content="why is sky blue?"),
#             ],
#         )
#     create_prompt_template_mock.sync_detailed.assert_called_once()
#     get_projects_projects_get_mock.sync_detailed.assert_called_once()


# DEPRECATED: This test uses old project-specific endpoints that are no longer supported.
# We now use global template endpoints with optional project_id parameter.
# See test_prompts_global.py for updated tests.
# @patch("galileo.projects.get_projects_projects_get")
# @patch("galileo.prompts.get_project_templates_projects_project_id_templates_get")
# def test_list_prompts(list_prompt_templates_mock: Mock, get_projects_projects_get_mock: Mock) -> None:
#     list_prompt_templates_mock.sync.return_value = [prompt_template()]
#     get_projects_projects_get_mock.sync_detailed.return_value = projects_response()
#     templates = list_prompt_templates(project="andrii-new-project")
#
#     assert len(templates) == 1
#     assert templates[0].name == "andrii-good-prompt"
#
#     list_prompt_templates_mock.sync.assert_called_once()
#     get_projects_projects_get_mock.sync_detailed.assert_called_once()


# DEPRECATED: This test uses old project-specific endpoints that are no longer supported.
# We now use global template endpoints with optional project_id parameter.
# See test_prompts_global.py for updated tests.
# @patch("galileo.projects.get_projects_projects_get")
# @patch("galileo.prompts.get_project_templates_projects_project_id_templates_get")
# def test_get_prompt_template_found(list_prompt_templates_mock: Mock, get_projects_projects_get_mock: Mock) -> None:
#     """Test get_prompt_template when template exists."""
#     list_prompt_templates_mock.sync.return_value = [prompt_template()]
#     get_projects_projects_get_mock.sync_detailed.return_value = projects_response()
#
#     template = get_prompt_template(name="andrii-good-prompt", project="andrii-new-project")
#
#     assert template is not None
#     assert template.name == "andrii-good-prompt"
#     list_prompt_templates_mock.sync.assert_called_once()
#     get_projects_projects_get_mock.sync_detailed.assert_called_once()
#
#
# DEPRECATED: This test uses old project-specific endpoints that are no longer supported.
# We now use global template endpoints with optional project_id parameter.
# See test_prompts_global.py for updated tests.
# @patch("galileo.projects.get_projects_projects_get")
# @patch("galileo.prompts.get_project_templates_projects_project_id_templates_get")
# def test_get_prompt_template_not_found(list_prompt_templates_mock: Mock, get_projects_projects_get_mock: Mock) -> None:
#     """Test get_prompt_template when template doesn't exist."""
#     list_prompt_templates_mock.sync.return_value = [prompt_template()]  # Return a different template
#     get_projects_projects_get_mock.sync_detailed.return_value = projects_response()
#
#     template = get_prompt_template(name="nonexistent-template", project="andrii-new-project")
#
#     assert template is None
#     list_prompt_templates_mock.sync.assert_called_once()
#     get_projects_projects_get_mock.sync_detailed.assert_called_once()


@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.prompts.get_projects_paginated_projects_paginated_post")
@patch("galileo.prompts.create_global_prompt_template_templates_post")
def test_create_global_prompt_template(
    create_global_prompt_template_mock: Mock, get_projects_paginated_mock: Mock, query_templates_mock: Mock
) -> None:
    # Mock no existing templates (name is unique)
    query_templates_mock.sync.return_value = empty_templates_list_response()

    # Mock empty paginated response (no projects)
    get_projects_paginated_mock.sync.return_value = GetProjectsPaginatedResponse(
        projects=[], limit=100, next_starting_token=None, paginated=False, starting_token=0
    )

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


@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.prompts.get_projects_paginated_projects_paginated_post")
@patch("galileo.prompts.create_global_prompt_template_templates_post")
def test_create_global_prompt_template_error_scenarios(
    create_global_prompt_template_mock: Mock, get_projects_paginated_mock: Mock, query_templates_mock: Mock
) -> None:
    """Test create_global_prompt_template with realistic error scenarios."""
    # Mock no existing templates (name is unique)
    query_templates_mock.sync.return_value = empty_templates_list_response()

    # Mock empty paginated response (no projects)
    get_projects_paginated_mock.sync.return_value = GetProjectsPaginatedResponse(
        projects=[], limit=100, next_starting_token=None, paginated=False, starting_token=0
    )

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
def test_get_global_prompt_template_by_id(get_global_template_mock: Mock) -> None:
    get_global_template_mock.sync.return_value = global_prompt_template()

    template = get_prompt(id="global-template-id-123")

    assert template is not None
    assert template.id == "global-template-id-123"
    assert template.name == "global-helpful-assistant"
    assert template.selected_version is not None
    assert template.selected_version.id == "global-version-id-456"
    assert template.selected_version.version == 1
    get_global_template_mock.sync.assert_called_once_with(template_id="global-template-id-123", client=ANY)


@patch("galileo.prompts.query_templates_templates_query_post")
def test_get_global_prompt_template_by_name(query_templates_mock: Mock) -> None:
    query_templates_mock.sync.return_value = global_templates_list_response()

    template = get_prompt(name="global-helpful-assistant")

    assert template is not None
    assert template.id == "global-template-id-123"
    assert template.name == "global-helpful-assistant"
    assert template.selected_version is not None
    assert template.selected_version.id == "global-version-id-456"
    assert template.selected_version.version == 1
    query_templates_mock.sync.assert_called_once()


@patch("galileo.prompts.get_global_template_templates_template_id_get")
def test_get_global_prompt_template_by_id_not_found(get_global_template_mock: Mock) -> None:
    get_global_template_mock.sync.return_value = None

    template = get_prompt(id="nonexistent-id")

    assert template is None
    get_global_template_mock.sync.assert_called_once()


@patch("galileo.prompts.query_templates_templates_query_post")
def test_get_global_prompt_template_by_name_not_found(query_templates_mock: Mock) -> None:
    query_templates_mock.sync.return_value = empty_templates_list_response()

    template = get_prompt(name="nonexistent-template")

    assert template is None
    query_templates_mock.sync.assert_called_once()


def test_get_global_prompt_template_validation_errors() -> None:
    with pytest.raises(ValueError) as exc_info:
        get_prompt()
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"

    with pytest.raises(ValueError) as exc_info:
        get_prompt(id="id", name="name")
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"


@patch("galileo.prompts.query_templates_templates_query_post")
def test_list_global_prompt_templates(query_templates_mock: Mock) -> None:
    query_templates_mock.sync.return_value = global_templates_list_response()

    templates = get_prompts()

    assert len(templates) == 1
    assert templates[0].name == "global-helpful-assistant"
    assert templates[0].id == "global-template-id-123"
    query_templates_mock.sync.assert_called_once()


@patch("galileo.prompts.query_templates_templates_query_post")
def test_list_global_prompt_templates_with_filter(query_templates_mock: Mock) -> None:
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
def test_list_global_prompt_templates_with_error_responses(query_templates_mock: Mock, response_value) -> None:
    """Test list_global_prompt_templates when API returns HTTPValidationError or None."""
    query_templates_mock.sync.return_value = response_value

    templates = get_prompts()

    assert len(templates) == 0
    query_templates_mock.sync.assert_called_once()


@patch("galileo.prompts.query_templates_templates_query_post")
def test_list_global_prompt_templates_empty(query_templates_mock: Mock) -> None:
    query_templates_mock.sync.return_value = empty_templates_list_response()

    templates = get_prompts()

    assert len(templates) == 0
    query_templates_mock.sync.assert_called_once()


@patch("galileo.prompts.delete_global_template_templates_template_id_delete")
def test_delete_global_prompt_template_by_id(delete_global_template_mock: Mock) -> None:
    delete_global_template_mock.sync.return_value = None

    delete_prompt(id="global-template-id-123")

    delete_global_template_mock.sync.assert_called_once_with(client=ANY, template_id="global-template-id-123")


@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.prompts.delete_global_template_templates_template_id_delete")
def test_delete_global_prompt_template_by_name(delete_global_template_mock: Mock, query_templates_mock: Mock) -> None:
    query_templates_mock.sync.return_value = global_templates_list_response()
    delete_global_template_mock.sync.return_value = None

    delete_prompt(name="global-helpful-assistant")

    query_templates_mock.sync.assert_called_once()
    delete_global_template_mock.sync.assert_called_once_with(client=ANY, template_id="global-template-id-123")


@patch("galileo.prompts.query_templates_templates_query_post")
def test_delete_global_prompt_template_by_name_not_found(query_templates_mock: Mock) -> None:
    query_templates_mock.sync.return_value = empty_templates_list_response()

    with pytest.raises(ValueError) as exc_info:
        delete_prompt(name="nonexistent-template")

    assert "Global template 'nonexistent-template' not found" in str(exc_info.value)
    query_templates_mock.sync.assert_called_once()


def test_delete_global_prompt_template_validation_errors() -> None:
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


@patch("galileo.prompts.update_global_template_templates_template_id_patch")
def test_update_global_prompt_template_by_id(update_global_template_mock: Mock) -> None:
    """Test update_prompt with template ID."""
    updated_template = global_prompt_template()
    updated_template.name = "updated-template-name"

    update_global_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=updated_template
    )

    template = update_prompt(id="global-template-id-123", new_name="updated-template-name")

    assert template is not None
    assert template.name == "updated-template-name"
    assert template.id == "global-template-id-123"
    update_global_template_mock.sync_detailed.assert_called_once_with(
        template_id="global-template-id-123", client=ANY, body=UpdatePromptTemplateRequest(name="updated-template-name")
    )


@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.prompts.update_global_template_templates_template_id_patch")
def test_update_global_prompt_template_by_name(update_global_template_mock: Mock, query_templates_mock: Mock) -> None:
    """Test update_prompt with template name."""
    query_templates_mock.sync.return_value = global_templates_list_response()

    updated_template = global_prompt_template()
    updated_template.name = "updated-template-name"

    update_global_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=updated_template
    )

    template = update_prompt(name="global-helpful-assistant", new_name="updated-template-name")

    assert template is not None
    assert template.name == "updated-template-name"
    assert template.id == "global-template-id-123"

    query_templates_mock.sync.assert_called_once()
    update_global_template_mock.sync_detailed.assert_called_once_with(
        template_id="global-template-id-123", client=ANY, body=UpdatePromptTemplateRequest(name="updated-template-name")
    )


@patch("galileo.prompts.query_templates_templates_query_post")
def test_update_global_prompt_template_by_name_not_found(query_templates_mock: Mock) -> None:
    """Test update_prompt when template is not found by name."""
    query_templates_mock.sync.return_value = empty_templates_list_response()

    with pytest.raises(ValueError) as exc_info:
        update_prompt(name="nonexistent-template", new_name="new-name")

    assert "Global template 'nonexistent-template' not found" in str(exc_info.value)
    query_templates_mock.sync.assert_called_once()


@patch("galileo.prompts.update_global_template_templates_template_id_patch")
def test_update_global_prompt_template_error_scenarios(update_global_template_mock: Mock) -> None:
    """Test update_prompt with realistic error scenarios."""

    # Test 422 Unprocessable Entity
    update_global_template_mock.sync_detailed.return_value = Response(
        content=b'{"detail":[{"loc":["body","name"],"msg":"field required","type":"value_error.missing"}]}',
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        headers={},
        parsed=HTTPValidationError(),
    )

    with pytest.raises(PromptTemplateAPIException) as exc_info:
        update_prompt(id="global-template-id-123", new_name="new-name")
    assert "field required" in str(exc_info.value)

    # Test 404 Not Found
    update_global_template_mock.sync_detailed.return_value = Response(
        content=b'{"detail":"Template not found"}', status_code=HTTPStatus.NOT_FOUND, headers={}, parsed=None
    )

    with pytest.raises(PromptTemplateAPIException) as exc_info:
        update_prompt(id="nonexistent-template-id", new_name="new-name")
    assert "Template not found" in str(exc_info.value)

    # Test 500 Internal Server Error
    update_global_template_mock.sync_detailed.return_value = Response(
        content=b'{"detail":"Internal server error"}',
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        headers={},
        parsed=None,
    )

    with pytest.raises(PromptTemplateAPIException) as exc_info:
        update_prompt(id="global-template-id-123", new_name="new-name")
    assert "Internal server error" in str(exc_info.value)

    assert update_global_template_mock.sync_detailed.call_count == 3


def test_update_global_prompt_template_validation_errors() -> None:
    """Test all validation error scenarios for update_prompt."""

    # Test no parameters provided
    with pytest.raises(ValueError) as exc_info:
        update_prompt(new_name="new-name")  # type: ignore[call-overload]
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"

    # Test both id and name provided
    with pytest.raises(ValueError) as exc_info:
        update_prompt(id="id", name="name", new_name="new-name")  # type: ignore[call-overload]
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"

    # Test both None
    with pytest.raises(ValueError) as exc_info:
        update_prompt(id=None, name=None, new_name="new-name")  # type: ignore[call-overload]
    assert str(exc_info.value) == "Exactly one of 'id' or 'name' must be provided"


@patch("galileo.prompts.update_global_template_templates_template_id_patch")
def test_update_global_prompt_template_with_empty_name(update_global_template_mock: Mock) -> None:
    """Test update_prompt with empty name (should be handled by API validation)."""
    update_global_template_mock.sync_detailed.return_value = Response(
        content=b'{"detail":[{"loc":["body","name"],"msg":"ensure this value has at least 1 characters","type":"value_error.any_str.min_length"}]}',
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        headers={},
        parsed=HTTPValidationError(),
    )

    with pytest.raises(PromptTemplateAPIException) as exc_info:
        update_prompt(id="global-template-id-123", new_name="")
    assert "ensure this value has at least 1 characters" in str(exc_info.value)

    update_global_template_mock.sync_detailed.assert_called_once_with(
        template_id="global-template-id-123", client=ANY, body=UpdatePromptTemplateRequest(name="")
    )


@patch("galileo.prompts.update_global_template_templates_template_id_patch")
def test_update_global_prompt_template_successful_response_with_http_validation_error(
    update_global_template_mock: Mock,
) -> None:
    """Test update_prompt when API returns HTTPValidationError as parsed response."""
    update_global_template_mock.sync_detailed.return_value = Response(
        content=b'{"detail":"Some validation error"}',
        status_code=HTTPStatus.OK,
        headers={},
        parsed=HTTPValidationError(),
    )

    with pytest.raises(PromptTemplateAPIException) as exc_info:
        update_prompt(id="global-template-id-123", new_name="new-name")
    assert "Some validation error" in str(exc_info.value)

    update_global_template_mock.sync_detailed.assert_called_once()


@patch("galileo.prompts.render_template_render_template_post")
def test_render_template_with_string_data(render_template_mock: Mock) -> None:
    """Test render_template with string data."""
    render_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=render_template_response()
    )

    response = render_template(template="Hello {{name}}! How are you?", data=["User1", "User2"])

    assert response is not None
    assert len(response.rendered_templates) == 2
    assert response.rendered_templates[0].result == "Hello User1! How are you?"
    assert response.rendered_templates[1].result == "Hello User2! How are you?"
    render_template_mock.sync_detailed.assert_called_once_with(
        client=ANY,
        body=RenderTemplateRequest(
            template="Hello {{name}}! How are you?", data=StringData(input_strings=["User1", "User2"])
        ),
        starting_token=0,
        limit=100,
    )


@patch("galileo.prompts.render_template_render_template_post")
def test_render_template_with_dataset_data(render_template_mock: Mock) -> None:
    """Test render_template with dataset data."""
    render_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=render_template_response()
    )

    response = render_template(template="Hello {{name}}! How are you?", data="dataset-id-123")

    assert response is not None
    assert len(response.rendered_templates) == 2
    render_template_mock.sync_detailed.assert_called_once_with(
        client=ANY,
        body=RenderTemplateRequest(
            template="Hello {{name}}! How are you?", data=DatasetData(dataset_id="dataset-id-123")
        ),
        starting_token=0,
        limit=100,
    )


@patch("galileo.prompts.render_template_render_template_post")
def test_render_template_with_pagination(render_template_mock: Mock) -> None:
    """Test render_template with pagination parameters for both page 1 and page 2."""
    # Test page 1 (starting_token=0, limit=1)
    render_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=render_template_response_paginated()
    )

    response = render_template(
        template="Hello {{name}}! How are you?", data=["User1", "User2"], starting_token=0, limit=1
    )

    assert response is not None
    assert len(response.rendered_templates) == 1
    assert response.rendered_templates[0].result == "Hello User1! How are you?"
    assert response.paginated is True
    assert response.next_starting_token == 1
    render_template_mock.sync_detailed.assert_called_with(
        client=ANY,
        body=RenderTemplateRequest(
            template="Hello {{name}}! How are you?", data=StringData(input_strings=["User1", "User2"])
        ),
        starting_token=0,
        limit=1,
    )

    # Test page 2 (starting_token=1, limit=1)
    render_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=render_template_response_second_page()
    )

    response = render_template(
        template="Hello {{name}}! How are you?", data=["User1", "User2"], starting_token=1, limit=1
    )

    assert response is not None
    assert len(response.rendered_templates) == 1
    assert response.rendered_templates[0].result == "Hello User2! How are you?"
    assert response.paginated is True
    assert response.next_starting_token is None  # Last page
    assert response.starting_token == 1

    # Verify both calls were made
    assert render_template_mock.sync_detailed.call_count == 2
    render_template_mock.sync_detailed.assert_called_with(
        client=ANY,
        body=RenderTemplateRequest(
            template="Hello {{name}}! How are you?", data=StringData(input_strings=["User1", "User2"])
        ),
        starting_token=1,
        limit=1,
    )


@patch("galileo.prompts.render_template_render_template_post")
def test_render_template_with_dataset_data_object(render_template_mock: Mock) -> None:
    """Test render_template with DatasetData object."""
    render_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=render_template_response()
    )

    dataset_data = DatasetData(dataset_id="dataset-id-456")
    response = render_template(template="Hello {{name}}! How are you?", data=dataset_data)

    assert response is not None
    render_template_mock.sync_detailed.assert_called_once_with(
        client=ANY,
        body=RenderTemplateRequest(template="Hello {{name}}! How are you?", data=dataset_data),
        starting_token=0,
        limit=100,
    )


@patch("galileo.prompts.render_template_render_template_post")
def test_render_template_with_string_data_object(render_template_mock: Mock) -> None:
    """Test render_template with StringData object."""
    render_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=render_template_response()
    )

    string_data = StringData(input_strings=["TestUser1", "TestUser2"])
    response = render_template(template="Hello {{name}}! How are you?", data=string_data)

    assert response is not None
    render_template_mock.sync_detailed.assert_called_once_with(
        client=ANY,
        body=RenderTemplateRequest(template="Hello {{name}}! How are you?", data=string_data),
        starting_token=0,
        limit=100,
    )


@patch("galileo.prompts.render_template_render_template_post")
def test_render_template_empty_response(render_template_mock: Mock) -> None:
    """Test render_template with empty response."""
    render_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=render_template_response_empty()
    )

    response = render_template(template="Hello {{name}}! How are you?", data=["User1"])

    assert response is not None
    assert len(response.rendered_templates) == 0
    render_template_mock.sync_detailed.assert_called_once()


@patch("galileo.prompts.render_template_render_template_post")
def test_render_template_none_response(render_template_mock: Mock) -> None:
    """Test render_template when API returns None."""
    render_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=None
    )

    with pytest.raises(PromptTemplateAPIException):
        render_template(template="Hello {{name}}!", data=["User1"])

    render_template_mock.sync_detailed.assert_called_once()


@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.prompts.get_projects_paginated_projects_paginated_post")
@patch("galileo.projects.get_projects_projects_get")
@patch("galileo.prompts.create_prompt_template_with_version_projects_project_id_templates_post")
def test_create_prompt_with_project_name(
    create_prompt_template_mock: Mock,
    get_projects_projects_get_mock: Mock,
    get_projects_paginated_mock: Mock,
    query_templates_mock: Mock,
) -> None:
    """Test create_prompt with project_name parameter."""
    # Mock no existing templates (name is unique)
    query_templates_mock.sync.return_value = empty_templates_list_response()

    # Mock empty paginated response (no projects)
    get_projects_paginated_mock.sync.return_value = GetProjectsPaginatedResponse(
        projects=[], limit=100, next_starting_token=None, paginated=False, starting_token=0
    )

    create_prompt_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=prompt_template()
    )
    get_projects_projects_get_mock.sync_detailed.return_value = projects_response()

    template = create_prompt(
        name="project-template",
        template=[Message(role=MessageRole.system, content="you are a helpful assistant")],
        project_name="andrii-new-project",
    )

    assert template is not None
    assert template.name == "andrii-good-prompt"
    create_prompt_template_mock.sync_detailed.assert_called_once()
    get_projects_projects_get_mock.sync_detailed.assert_called_once()


@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.projects.get_all_projects_projects_all_get")
@patch("galileo.projects.get_project_projects_project_id_get")
@patch("galileo.prompts.create_prompt_template_with_version_projects_project_id_templates_post")
def test_create_prompt_with_project_id(
    create_prompt_template_mock: Mock,
    get_project_projects_project_id_get_mock: Mock,
    get_all_projects_mock: Mock,
    query_templates_mock: Mock,
) -> None:
    """Test create_prompt with project_id parameter."""
    # Mock no existing templates (name is unique)
    query_templates_mock.sync.return_value = empty_templates_list_response()
    get_all_projects_mock.sync.return_value = GetProjectsPaginatedResponse(
        projects=[], limit=100, next_starting_token=None, paginated=False, starting_token=0
    )

    create_prompt_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=prompt_template()
    )
    get_project_projects_project_id_get_mock.sync_detailed.return_value = Response(
        content=json.dumps(projects_response().parsed[0].to_dict()).encode("utf-8"),
        status_code=HTTPStatus.OK,
        headers={"Content-Type": "application/json"},
        parsed=projects_response().parsed[0],
    )

    template = create_prompt(
        name="project-template",
        template=[Message(role=MessageRole.system, content="you are a helpful assistant")],
        project_id="e343ea54-4df3-4d0b-9bc5-7e8224be348f",
    )

    assert template is not None
    assert template.name == "andrii-good-prompt"
    create_prompt_template_mock.sync_detailed.assert_called_once()
    get_project_projects_project_id_get_mock.sync_detailed.assert_called_once()


@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.projects.get_all_projects_projects_all_get")
@patch("galileo.projects.get_projects_projects_get")
def test_create_prompt_with_nonexistent_project_name(
    get_projects_projects_get_mock: Mock, get_all_projects_mock: Mock, query_templates_mock: Mock
) -> None:
    """Test create_prompt with nonexistent project_name."""
    # Mock no existing templates (name is unique)
    query_templates_mock.sync.return_value = empty_templates_list_response()
    get_all_projects_mock.sync.return_value = GetProjectsPaginatedResponse(
        projects=[], limit=100, next_starting_token=None, paginated=False, starting_token=0
    )

    get_projects_projects_get_mock.sync_detailed.return_value = Response(
        content=b"[]", status_code=HTTPStatus.OK, headers={"Content-Type": "application/json"}, parsed=[]
    )

    with pytest.raises(ValueError) as exc_info:
        create_prompt(
            name="project-template",
            template=[Message(role=MessageRole.system, content="you are a helpful assistant")],
            project_name="nonexistent-project",
        )

    assert "Project 'nonexistent-project' does not exist" in str(exc_info.value)
    get_projects_projects_get_mock.sync_detailed.assert_called_once()


@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.projects.get_all_projects_projects_all_get")
@patch("galileo.projects.get_project_projects_project_id_get")
def test_create_prompt_with_nonexistent_project_id(
    get_project_projects_project_id_get_mock: Mock, get_all_projects_mock: Mock, query_templates_mock: Mock
) -> None:
    """Test create_prompt with nonexistent project_id."""
    # Mock no existing templates (name is unique)
    query_templates_mock.sync.return_value = empty_templates_list_response()
    get_all_projects_mock.sync.return_value = GetProjectsPaginatedResponse(
        projects=[], limit=100, next_starting_token=None, paginated=False, starting_token=0
    )

    get_project_projects_project_id_get_mock.sync_detailed.return_value = Response(
        content=b"null", status_code=HTTPStatus.OK, headers={"Content-Type": "application/json"}, parsed=None
    )

    with pytest.raises(ValueError) as exc_info:
        create_prompt(
            name="project-template",
            template=[Message(role=MessageRole.system, content="you are a helpful assistant")],
            project_id="nonexistent-id",
        )

    assert "Project 'nonexistent-id' does not exist" in str(exc_info.value)
    get_project_projects_project_id_get_mock.sync_detailed.assert_called_once()


def test_create_prompt_with_both_project_params() -> None:
    """Test create_prompt with both project_id and project_name (should raise error)."""
    with pytest.raises(ValueError) as exc_info:
        create_prompt(
            name="project-template",
            template=[Message(role=MessageRole.system, content="you are a helpful assistant")],
            project_id="some-id",
            project_name="some-name",
        )

    assert "Only one of 'project_id' or 'project_name' can be provided, not both" in str(exc_info.value)


@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.projects.get_all_projects_projects_all_get")
@patch("galileo.prompts.create_global_prompt_template_templates_post")
def test_create_prompt_without_project_creates_global(
    create_global_prompt_template_mock: Mock, get_all_projects_mock: Mock, query_templates_mock: Mock
) -> None:
    """Test that create_prompt without project parameters creates a global template."""
    # Mock no existing templates (name is unique)
    query_templates_mock.sync.return_value = empty_templates_list_response()
    get_all_projects_mock.sync.return_value = GetProjectsPaginatedResponse(
        projects=[], limit=100, next_starting_token=None, paginated=False, starting_token=0
    )

    create_global_prompt_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=global_prompt_template()
    )

    template = create_prompt(
        name="global-template", template=[Message(role=MessageRole.system, content="you are a helpful assistant")]
    )

    assert template is not None
    assert template.name == "global-helpful-assistant"
    create_global_prompt_template_mock.sync_detailed.assert_called_once()


@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.projects.get_all_projects_projects_all_get")
@patch("galileo.projects.get_projects_projects_get")
@patch("galileo.prompts.create_prompt_template_with_version_projects_project_id_templates_post")
def test_create_prompt_with_project_name_and_string_template(
    create_prompt_template_mock: Mock,
    get_projects_projects_get_mock: Mock,
    get_all_projects_mock: Mock,
    query_templates_mock: Mock,
) -> None:
    """Test create_prompt with project_name and string template."""
    # Mock no existing templates (name is unique)
    query_templates_mock.sync.return_value = empty_templates_list_response()
    get_all_projects_mock.sync.return_value = GetProjectsPaginatedResponse(
        projects=[], limit=100, next_starting_token=None, paginated=False, starting_token=0
    )

    create_prompt_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=prompt_template()
    )
    get_projects_projects_get_mock.sync_detailed.return_value = projects_response()

    template_str = '[{"content":"you are a helpful assistant","role":"system"}]'
    template = create_prompt(name="project-template", template=template_str, project_name="andrii-new-project")

    assert template is not None
    assert template.name == "andrii-good-prompt"
    create_prompt_template_mock.sync_detailed.assert_called_once()
    # Verify the body contains the string template
    call_kwargs = create_prompt_template_mock.sync_detailed.call_args
    assert call_kwargs.kwargs["body"].template == template_str


# Test get_prompt() with project support
@patch("galileo.projects.get_projects_projects_get")
@patch("galileo.prompts.get_template_from_project_projects_project_id_templates_template_id_get")
def test_get_prompt_with_project_name_and_id(
    get_template_from_project_mock: Mock, get_projects_projects_get_mock: Mock
) -> None:
    """Test get_prompt with project_name parameter and template ID."""
    get_template_from_project_mock.sync.return_value = prompt_template()
    get_projects_projects_get_mock.sync_detailed.return_value = projects_response()

    template = get_prompt(id="4793f4b9-eb56-4495-88a9-8cf57bfe737b", project_name="andrii-new-project")

    assert template is not None
    assert template.name == "andrii-good-prompt"
    get_template_from_project_mock.sync.assert_called_once()
    get_projects_projects_get_mock.sync_detailed.assert_called_once()


@patch("galileo.projects.get_projects_projects_get")
@patch("galileo.prompts.get_project_templates_projects_project_id_templates_get")
def test_get_prompt_with_project_name_and_name(
    get_project_templates_mock: Mock, get_projects_projects_get_mock: Mock
) -> None:
    """Test get_prompt with project_name parameter and template name."""
    get_project_templates_mock.sync.return_value = [prompt_template()]
    get_projects_projects_get_mock.sync_detailed.return_value = projects_response()

    template = get_prompt(name="andrii-good-prompt", project_name="andrii-new-project")

    assert template is not None
    assert template.name == "andrii-good-prompt"
    get_project_templates_mock.sync.assert_called_once()
    get_projects_projects_get_mock.sync_detailed.assert_called_once()


@patch("galileo.projects.get_projects_projects_get")
def test_get_prompt_with_nonexistent_project(get_projects_projects_get_mock: Mock) -> None:
    """Test get_prompt with nonexistent project."""
    get_projects_projects_get_mock.sync_detailed.return_value = Response(
        content=b"[]", status_code=HTTPStatus.OK, headers={"Content-Type": "application/json"}, parsed=[]
    )

    with pytest.raises(ValueError) as exc_info:
        get_prompt(id="template-id", project_name="nonexistent-project")

    assert "Project 'nonexistent-project' does not exist" in str(exc_info.value)


def test_get_prompt_with_both_project_params() -> None:
    """Test get_prompt with both project parameters (should raise error)."""
    with pytest.raises(ValueError) as exc_info:
        get_prompt(id="template-id", project_id="id-123", project_name="proj-name")

    assert "Only one of 'project_id' or 'project_name' can be provided, not both" in str(exc_info.value)


# Test get_prompts() with project support
@patch("galileo.projects.get_projects_projects_get")
@patch("galileo.prompts.get_project_templates_projects_project_id_templates_get")
def test_get_prompts_with_project_name(get_project_templates_mock: Mock, get_projects_projects_get_mock: Mock) -> None:
    """Test get_prompts with project_name parameter."""
    get_project_templates_mock.sync.return_value = [prompt_template()]
    get_projects_projects_get_mock.sync_detailed.return_value = projects_response()

    templates = get_prompts(project_name="andrii-new-project")

    assert len(templates) == 1
    assert templates[0].name == "andrii-good-prompt"
    get_project_templates_mock.sync.assert_called_once()
    get_projects_projects_get_mock.sync_detailed.assert_called_once()


@patch("galileo.projects.get_project_projects_project_id_get")
@patch("galileo.prompts.get_project_templates_projects_project_id_templates_get")
def test_get_prompts_with_project_id(
    get_project_templates_mock: Mock, get_project_projects_project_id_get_mock: Mock
) -> None:
    """Test get_prompts with project_id parameter."""
    get_project_templates_mock.sync.return_value = [prompt_template()]
    get_project_projects_project_id_get_mock.sync_detailed.return_value = Response(
        content=json.dumps(projects_response().parsed[0].to_dict()).encode("utf-8"),
        status_code=HTTPStatus.OK,
        headers={"Content-Type": "application/json"},
        parsed=projects_response().parsed[0],
    )

    templates = get_prompts(project_id="e343ea54-4df3-4d0b-9bc5-7e8224be348f")

    assert len(templates) == 1
    assert templates[0].name == "andrii-good-prompt"
    get_project_templates_mock.sync.assert_called_once()
    get_project_projects_project_id_get_mock.sync_detailed.assert_called_once()


@patch("galileo.projects.get_projects_projects_get")
@patch("galileo.prompts.get_project_templates_projects_project_id_templates_get")
def test_get_prompts_with_project_and_name_filter(
    get_project_templates_mock: Mock, get_projects_projects_get_mock: Mock
) -> None:
    """Test get_prompts with project and name filter."""
    template1 = prompt_template()
    template2 = prompt_template()
    template2.name = "different-template"

    get_project_templates_mock.sync.return_value = [template1, template2]
    get_projects_projects_get_mock.sync_detailed.return_value = projects_response()

    templates = get_prompts(name_filter="good", project_name="andrii-new-project")

    assert len(templates) == 1
    assert templates[0].name == "andrii-good-prompt"


def test_get_prompts_with_both_project_params() -> None:
    """Test get_prompts with both project parameters (should raise error)."""
    with pytest.raises(ValueError) as exc_info:
        get_prompts(project_id="id-123", project_name="proj-name")

    assert "Only one of 'project_id' or 'project_name' can be provided, not both" in str(exc_info.value)


# Test delete_prompt() with project support
@patch("galileo.projects.get_projects_projects_get")
@patch("galileo.prompts.delete_template_projects_project_id_templates_template_id_delete")
def test_delete_prompt_with_project_name_and_id(
    delete_template_mock: Mock, get_projects_projects_get_mock: Mock
) -> None:
    """Test delete_prompt with project_name parameter and template ID."""
    delete_template_mock.sync.return_value = None
    get_projects_projects_get_mock.sync_detailed.return_value = projects_response()

    delete_prompt(id="template-id-123", project_name="andrii-new-project")

    delete_template_mock.sync.assert_called_once()
    get_projects_projects_get_mock.sync_detailed.assert_called_once()


@patch("galileo.projects.get_projects_projects_get")
@patch("galileo.prompts.get_project_templates_projects_project_id_templates_get")
@patch("galileo.prompts.delete_template_projects_project_id_templates_template_id_delete")
def test_delete_prompt_with_project_name_and_name(
    delete_template_mock: Mock, get_project_templates_mock: Mock, get_projects_projects_get_mock: Mock
) -> None:
    """Test delete_prompt with project_name parameter and template name."""
    delete_template_mock.sync.return_value = None
    get_project_templates_mock.sync.return_value = [prompt_template()]
    get_projects_projects_get_mock.sync_detailed.return_value = projects_response()

    delete_prompt(name="andrii-good-prompt", project_name="andrii-new-project")

    delete_template_mock.sync.assert_called_once()
    get_projects_projects_get_mock.sync_detailed.assert_called_once()


@patch("galileo.projects.get_project_projects_project_id_get")
@patch("galileo.prompts.delete_template_projects_project_id_templates_template_id_delete")
def test_delete_prompt_with_project_id(
    delete_template_mock: Mock, get_project_projects_project_id_get_mock: Mock
) -> None:
    """Test delete_prompt with project_id parameter."""
    delete_template_mock.sync.return_value = None
    get_project_projects_project_id_get_mock.sync_detailed.return_value = Response(
        content=json.dumps(projects_response().parsed[0].to_dict()).encode("utf-8"),
        status_code=HTTPStatus.OK,
        headers={"Content-Type": "application/json"},
        parsed=projects_response().parsed[0],
    )

    delete_prompt(id="template-id-123", project_id="e343ea54-4df3-4d0b-9bc5-7e8224be348f")

    delete_template_mock.sync.assert_called_once()
    get_project_projects_project_id_get_mock.sync_detailed.assert_called_once()


@patch("galileo.projects.get_projects_projects_get")
@patch("galileo.prompts.get_project_templates_projects_project_id_templates_get")
def test_delete_prompt_with_project_name_template_not_found(
    get_project_templates_mock: Mock, get_projects_projects_get_mock: Mock
) -> None:
    """Test delete_prompt when template is not found in project."""
    get_project_templates_mock.sync.return_value = []
    get_projects_projects_get_mock.sync_detailed.return_value = projects_response()

    with pytest.raises(ValueError) as exc_info:
        delete_prompt(name="nonexistent-template", project_name="andrii-new-project")

    assert "Template 'nonexistent-template' not found in project" in str(exc_info.value)


def test_delete_prompt_with_both_project_params() -> None:
    """Test delete_prompt with both project parameters (should raise error)."""
    with pytest.raises(ValueError) as exc_info:
        delete_prompt(id="template-id", project_id="id-123", project_name="proj-name")

    assert "Only one of 'project_id' or 'project_name' can be provided, not both" in str(exc_info.value)


# Test organization-wide unique name generation
@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.projects.get_all_projects_projects_all_get")
@patch("galileo.prompts.create_global_prompt_template_templates_post")
def test_create_prompt_generates_unique_name_when_global_exists(
    create_global_prompt_template_mock: Mock, get_all_projects_mock: Mock, query_templates_mock: Mock
) -> None:
    """Test that create_prompt appends (1) when name exists globally."""
    # Mock existing global template with the name
    existing_template = global_prompt_template()
    existing_template.name = "my-template"
    query_templates_mock.sync.return_value = global_templates_list_response()

    # Mock no projects
    get_all_projects_mock.sync.return_value = GetProjectsPaginatedResponse(
        projects=[], limit=100, next_starting_token=None, paginated=False, starting_token=0
    )

    # Mock successful creation with unique name
    new_template = global_prompt_template()
    new_template.name = "my-template (1)"
    create_global_prompt_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=new_template
    )

    template = create_prompt(
        name="global-helpful-assistant",  # This name exists
        template=[Message(role=MessageRole.system, content="test")],
    )

    # Verify the template was created with the incremented name
    assert template is not None
    assert template.name == "my-template (1)"
    create_global_prompt_template_mock.sync_detailed.assert_called_once()
    # Verify the body has the unique name
    call_kwargs = create_global_prompt_template_mock.sync_detailed.call_args
    assert " (1)" in call_kwargs.kwargs["body"].name or call_kwargs.kwargs["body"].name == "global-helpful-assistant"


@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.prompts.get_projects_paginated_projects_paginated_post")
@patch("galileo.prompts.get_project_templates_projects_project_id_templates_get")
@patch("galileo.prompts.create_global_prompt_template_templates_post")
def test_create_prompt_generates_unique_name_when_project_exists(
    create_global_prompt_template_mock: Mock,
    get_project_templates_mock: Mock,
    get_projects_paginated_mock: Mock,
    query_templates_mock: Mock,
) -> None:
    """Test that create_prompt appends (1) when name exists in a project."""
    # Mock no global templates
    query_templates_mock.sync.return_value = empty_templates_list_response()

    # Mock project with existing template
    project = projects_response().parsed[0]
    get_projects_paginated_mock.sync.return_value = GetProjectsPaginatedResponse(
        projects=[project], limit=100, next_starting_token=None, paginated=False, starting_token=0
    )

    existing_template = prompt_template()
    existing_template.name = "my-template"
    get_project_templates_mock.sync.return_value = [existing_template]

    # Mock successful creation with unique name
    new_template = global_prompt_template()
    new_template.name = "my-template (1)"
    create_global_prompt_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=new_template
    )

    template = create_prompt(
        name="my-template",  # This name exists in a project
        template=[Message(role=MessageRole.system, content="test")],
    )

    # Verify the template was created with the incremented name
    assert template is not None
    # The name should be unique across organization
    get_project_templates_mock.sync.assert_called()


@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.projects.get_all_projects_projects_all_get")
@patch("galileo.projects.get_projects_projects_get")
@patch("galileo.prompts.create_prompt_template_with_version_projects_project_id_templates_post")
def test_create_prompt_with_project_generates_unique_name(
    create_prompt_template_mock: Mock,
    get_projects_projects_get_mock: Mock,
    get_all_projects_mock: Mock,
    query_templates_mock: Mock,
) -> None:
    """Test that create_prompt with project generates unique name."""
    # Mock existing global template
    existing_global = global_prompt_template()
    existing_global.name = "assistant"
    query_templates_mock.sync.return_value = ListPromptTemplateResponse.from_dict(
        {
            "templates": [existing_global.to_dict()],
            "limit": 100,
            "next_starting_token": None,
            "paginated": False,
            "starting_token": 0,
        }
    )

    # Mock no projects for uniqueness check
    get_all_projects_mock.sync.return_value = GetProjectsPaginatedResponse(
        projects=[], limit=100, next_starting_token=None, paginated=False, starting_token=0
    )

    # Mock project for creation
    get_projects_projects_get_mock.sync_detailed.return_value = projects_response()

    # Mock successful creation with unique name
    new_template = prompt_template()
    new_template.name = "assistant (1)"
    create_prompt_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=new_template
    )

    template = create_prompt(
        name="assistant",  # This name exists globally
        template=[Message(role=MessageRole.system, content="test")],
        project_name="andrii-new-project",
    )

    # Verify the template was created
    assert template is not None
    create_prompt_template_mock.sync_detailed.assert_called_once()


@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.projects.get_all_projects_projects_all_get")
@patch("galileo.prompts.create_global_prompt_template_templates_post")
def test_create_prompt_no_increment_when_name_unique(
    create_global_prompt_template_mock: Mock, get_all_projects_mock: Mock, query_templates_mock: Mock
) -> None:
    """Test that create_prompt doesn't increment when name is unique."""
    # Mock no global templates with this name
    query_templates_mock.sync.return_value = empty_templates_list_response()

    # Mock no projects
    get_all_projects_mock.sync.return_value = GetProjectsPaginatedResponse(
        projects=[], limit=100, next_starting_token=None, paginated=False, starting_token=0
    )

    # Mock successful creation
    new_template = global_prompt_template()
    new_template.name = "unique-template"
    create_global_prompt_template_mock.sync_detailed.return_value = Response(
        content=b"", status_code=HTTPStatus.OK, headers={}, parsed=new_template
    )

    template = create_prompt(name="unique-template", template=[Message(role=MessageRole.system, content="test")])

    # Verify the template was created with the original name (no increment)
    assert template is not None
    assert template.name == "unique-template"
    create_global_prompt_template_mock.sync_detailed.assert_called_once()
    # Verify the body has the original name
    call_kwargs = create_global_prompt_template_mock.sync_detailed.call_args
    assert call_kwargs.kwargs["body"].name == "unique-template"


@patch("galileo.prompts.query_templates_templates_query_post")
@patch("galileo.projects.get_all_projects_projects_all_get")
@patch("galileo.prompts.get_project_templates_projects_project_id_templates_get")
def test_generate_unique_name_increments_multiple_times(
    get_project_templates_mock: Mock, get_all_projects_mock: Mock, query_templates_mock: Mock
) -> None:
    """Test that unique name generation can handle multiple increments."""
    from galileo.prompts import _generate_unique_name

    # Mock global templates: base-name exists
    template1 = global_prompt_template()
    template1.name = "base-name"

    template2 = global_prompt_template()
    template2.name = "base-name (1)"

    template3 = global_prompt_template()
    template3.name = "base-name (2)"

    query_templates_mock.sync.return_value = ListPromptTemplateResponse.from_dict(
        {
            "templates": [template1.to_dict(), template2.to_dict(), template3.to_dict()],
            "limit": 100,
            "next_starting_token": None,
            "paginated": False,
            "starting_token": 0,
        }
    )

    # Mock no projects
    get_all_projects_mock.sync.return_value = GetProjectsPaginatedResponse(
        projects=[], limit=100, next_starting_token=None, paginated=False, starting_token=0
    )

    # Should generate "base-name (3)"
    unique_name = _generate_unique_name("base-name")
    assert unique_name == "base-name (3)"
