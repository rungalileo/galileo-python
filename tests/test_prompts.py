import json
from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest

from galileo import Message, MessageRole
from galileo.prompts import PromptTemplateAPIException, create_prompt_template
from galileo.resources.models import BasePromptTemplateResponse, ProjectDB
from galileo.resources.types import Response


def projects_response():
    project = ProjectDB.from_dict(
        {
            "created_by_user": {"id": "01ce18ac-3960-46e1-bb79-0e4965069add"},
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
            "selected_version": {
                "id": "03487fd7-1032-4317-ac43-a68401c07ee9",
                "template": '[{"content":"you are a helpful assistant","role":"system"},{"content":"why is sky blue?","role":"user"}]',
                "version": 0,
            },
            "selected_version_id": "03487fd7-1032-4317-ac43-a68401c07ee9",
            "template": '[{"content":"you are a helpful assistant","role":"system"},{"content":"why is sky blue?","role":"user"}]',
            "total_versions": 1,
            "all_versions": [
                {
                    "id": "03487fd7-1032-4317-ac43-a68401c07ee9",
                    "template": '[{"content":"you are a helpful assistant","role":"system"},{"content":"why is sky blue?","role":"user"}]',
                    "version": 0,
                }
            ],
        }
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
