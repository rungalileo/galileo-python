import json
from typing import Optional, Union

from galileo.base import BaseClientModel
from galileo.projects import Projects
from galileo.resources.api.prompts import (
    create_prompt_template_with_version_projects_project_id_templates_post,
    get_template_from_project_projects_project_id_templates_template_id_get,
)
from galileo.resources.models import (
    BasePromptTemplateResponse,
    CreatePromptTemplateWithVersionRequestBody,
    HTTPValidationError,
    Message,
)


class PromptTemplate(BaseClientModel):
    def get(
        self, *, project_name: str, template_id: str
    ) -> Optional[Union[BasePromptTemplateResponse, HTTPValidationError]]:
        project = Projects().get(name=project_name)
        if not project:
            raise ValueError(f"Project {project_name} does not exist")

        template = get_template_from_project_projects_project_id_templates_template_id_get.sync(
            # TODO: remove type ignore, when migrated to proper AuthenticatedClient
            project_id=project.id,
            template_id=template_id,
            client=self.client,  # type: ignore[arg-type]
        )
        return template

    def create(
        self, name: str, project_name: str, template: Union[list["Message"], str]
    ) -> Optional[Union[BasePromptTemplateResponse, HTTPValidationError]]:
        project = Projects().get(name=project_name)
        if not project:
            raise ValueError(f"Project {project_name} does not exist")

        body = CreatePromptTemplateWithVersionRequestBody(name=name, template=template)

        response = create_prompt_template_with_version_projects_project_id_templates_post.sync_detailed(
            project_id=project.id,
            client=self.client,  # type: ignore[arg-type]
            body=body,
        )

        if not response.parsed:
            raise ValueError(json.loads(response.content)["detail"])

        return response.parsed


def create_prompt_template(
    name: str, project: str, messages: Union[list["Message"], str]
) -> Optional[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    return PromptTemplate().create(name=name, project_name=project, template=messages)


def get_prompt_template(
    project: str, template_id: str
) -> Optional[Union[BasePromptTemplateResponse, HTTPValidationError]]:
    return PromptTemplate().get(project_name=project, template_id=template_id)
